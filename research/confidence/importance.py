"""
Feature importance for the ENTRY confidence model (AFML ch.8, MLAM 2020 ch.6) under the study's purged walk-forward.

Everything is computed fold by fold on the walk-forward folds (walkforward.make_folds: test years 2013..2024 + 2025H1;
the locked holdout 2025-07-01+ is refused and its rows dropped), training rows purged by walkforward.train_mask
(label end t_end at least 1 day before the test window), features oriented by the trade direction
(walkforward.orient, signed columns x d, swing-distance pair mirrored for shorts).

Definitions
  * Fold model: exactly the walk-forward's model of that fold (walkforward._fit_and_threshold): `logit` = median
    imputation + StandardScaler + L2 LogisticRegression with C picked on the last 2 training years; `gbm` = shallow
    HistGradientBoosting + isotonic calibration on the last training year. The entry threshold thr is chosen on the
    TRAINING period's inner out-of-sample predictions (max mean $ per trade, >= 5% kept). Sample weights =
    walkforward.sample_weights (uniqueness, cross-market).
  * Base OOS scores of a fold (test rows only, unweighted, like walk_forward's metrics):
        logloss  = mean binary log loss of p (clipped to [1e-4, 1-1e-4]) against y_1.5
        auc      = ROC AUC
        usd_kept = mean net $ per 1 micro of the trades with p >= thr ("$ per kept trade")
  * MDA (mean decrease accuracy) of a GROUP of columns (one feature, one correlation cluster, or one family): in the
    fold's TEST rows only, the group's columns are shuffled with ONE row permutation shared by all columns of the
    group (keeps the group's own joint distribution - e.g. the time-of-day one-hots stay valid - and breaks its link
    to the label and to the other features); the fitted model and its threshold are unchanged; repeated n_rep times
    and averaged.
        mda_ll   = logloss(permuted) - logloss(base)          (> 0: the model needs the group; in nats)
        mda_auc  = auc(base) - auc(permuted)
        mda_usd  = usd_kept(base) - usd_kept(permuted)        (> 0: the group makes the kept trades better, $/trade)
        mda_tot  = total $ kept (base) - total $ kept (permuted), per fold
    Summaries over folds: mean, sd, t = mean / (sd / sqrt(n_folds)), share of folds > 0.
  * Clustered MDA (Lopez de Prado, Machine Learning for Asset Managers 2020, 6.5): features are clustered by
    correlation on the oriented, median-imputed feature matrix (no labels used): distance = 1 - |Pearson corr|,
    average-linkage hierarchical clustering, cut where clusters have average |corr| >= 0.3 (distance 0.7), with
    the cluster count clipped into [min_k, max_k] = [15, 30] (merging / splitting along the same tree). A cluster's MDA permutes all its members
    together, so a signal carried by several near-duplicate columns is credited to the cluster instead of being
    split (and hidden) across its members.
  * SFI (single feature importance, AFML 8.4.1): for every feature alone, per fold, fitted on the purged training
    rows with the same sample weights, scored on the test rows:
        logit1: median imputation + StandardScaler + LogisticRegression(C=1) on the one column (monotone effects)
        bin1:   per-bin win rate (<= n_bins quantile bins from training, or one bin per value when the feature has
                <= n_bins distinct values, NaN its own bin), shrunk toward the training base rate with `shrink`
                pseudo-weight (non-monotone effects)
        sfi_ll_* = logloss(training base rate) - logloss(single-feature model)   (> 0 = the feature alone helps)
        sfi_auc_* = AUC of the single-feature model
    SFI does not suffer from substitution (each feature is judged alone) but misses joint effects.
"""
import math
import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, silhouette_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import walkforward as wf

# ============================================================================================ feature families
FAMILY_RULES = (
    ("candle pattern", lambda f: f.startswith("pat_")),
    ("candle family", lambda f: f.startswith("fam_")),
    ("swing structure", lambda f: f.startswith(("dist_swhi", "dist_swlo", "brk_", "struct_", "fibpos_", "atfib_"))),
    ("trend (EMAs)", lambda f: f.startswith(("ema_stack", "ema20_slope", "dist_ema", "above_ema20"))),
    ("momentum", lambda f: f.startswith("mom")),
    ("VWAP", lambda f: f.startswith("dist_vwap")),
    ("signal bar shape/volume", lambda f: f in ("rng_rel", "body_frac", "clv", "vol_rel")),
    ("day so far", lambda f: f in ("gap_open", "day_range_rel", "day_ret")),
    ("time of day", lambda f: f.startswith("tod_")),
    ("day of week", lambda f: f.startswith("dow_")),
    ("60-min trend", lambda f: f.startswith("h1_")),
    ("cross-market", lambda f: f.startswith("x_")),
    ("stop size / cost", lambda f: f in ("stop_R20", "cost_R")),
    ("market", lambda f: f.startswith("mkt_")),
)


def family_of(f):
    for name, rule in FAMILY_RULES:
        if rule(f):
            return name
    return "other"


def families(features):
    """{family: [features]} in feature order."""
    out = {}
    for f in features:
        out.setdefault(family_of(f), []).append(f)
    return out


# ============================================================================================ clustering
def correlation_matrix(X, max_rows=200_000, seed=0):
    """|Pearson| correlation of the columns of X (DataFrame), NaN -> column median, on <= max_rows random rows.
    Constant columns get correlation 0 with everything (distance 1)."""
    A = X.to_numpy(np.float64)
    if len(A) > max_rows:
        A = A[np.sort(np.random.default_rng(seed).choice(len(A), max_rows, replace=False))]
    med = np.nanmedian(np.where(np.isfinite(A), A, np.nan), axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    A = np.where(np.isfinite(A), A, med)
    sd = A.std(axis=0)
    Z = (A - A.mean(axis=0)) / np.where(sd > 0, sd, 1.0)
    C = (Z.T @ Z) / len(Z)
    C[:, sd == 0] = 0.0
    C[sd == 0, :] = 0.0
    np.fill_diagonal(C, 1.0)
    return pd.DataFrame(np.clip(C, -1, 1), index=X.columns, columns=X.columns)


def correlation_clusters(X, min_k=15, max_k=30, max_dist=0.7, method="average", max_rows=200_000, seed=0):
    """Cluster the columns of X by distance 1 - |corr| (hierarchical, `method` linkage). Cut: the clusters whose
    average within-cluster distance is <= max_dist (default 0.7 = average |corr| >= 0.3), with the count then clipped
    into [min_k, max_k] (more than max_k: the closest clusters are merged further until max_k remain; fewer than
    min_k: split until min_k). Silhouette scores are reported, not used: on near-uncorrelated columns the silhouette
    is ~0 whether they are singletons or arbitrarily paired, so it cannot choose between those cuts.
    Returns (clusters, info): clusters = {"c01": [features], ...} numbered in order of each cluster's first feature
    in X; info = dict(k, k_natural (count at max_dist), silhouette, corr, linkage)."""
    C = correlation_matrix(X, max_rows, seed)
    D = 1.0 - np.abs(C.to_numpy())
    D = (D + D.T) / 2
    np.fill_diagonal(D, 0.0)
    D = np.clip(D, 0.0, None)
    n = D.shape[0]
    cols = list(X.columns)
    if n < 2:
        return {"c01": cols}, dict(k=1, k_natural=1, silhouette=np.nan, corr=C, linkage=None)
    Z = linkage(squareform(D, checks=False), method=method)
    k_nat = len(np.unique(fcluster(Z, max_dist, criterion="distance")))
    k = int(np.clip(k_nat, min(min_k, n), min(max_k, n)))
    lab = fcluster(Z, k, criterion="maxclust")
    sil = float(silhouette_score(D, lab, metric="precomputed")) if 2 <= len(np.unique(lab)) < n else np.nan
    order = []
    for c in lab:
        if c not in order:
            order.append(c)
    clusters = {f"c{i + 1:02d}": [cols[j] for j in range(n) if lab[j] == c] for i, c in enumerate(order)}
    return clusters, dict(k=len(clusters), k_natural=k_nat, silhouette=sil, corr=C, linkage=Z)


def cluster_label(members, max_names=4):
    """Short readable name of a cluster: its families and first members."""
    fams = []
    for f in members:
        if family_of(f) not in fams:
            fams.append(family_of(f))
    names = ", ".join(members[:max_names]) + (f" +{len(members) - max_names}" if len(members) > max_names else "")
    return f"{' + '.join(fams)}: {names}"


# ============================================================================================ fold models
@dataclass
class FoldFit:
    name: str
    tr: np.ndarray
    test: np.ndarray
    model: object
    thr: float
    info: dict
    p: np.ndarray            # base OOS probabilities of the test rows
    years: float


def prepare(data, features, label="y_1.5", pnl="pnl_usd_1.5", t_end="t_end_1.5", signed=None, mirror="auto",
            weights=None):
    """walkforward._prepare for entries with final=False: drops unlabelled and holdout rows, sorts by t, orients
    the features by d, computes the sample weights. Returns its dict (X, y, pnl, w, t, t_end, year, ...)."""
    return wf._prepare(data, list(features), "entry", label, pnl, t_end, signed, False, "trade", weights, mirror)


def fit_folds(S, model="logit", folds=None, min_keep=0.05, min_train_years=3, min_inner=200, purge=wf.PURGE,
              C_grid=wf.C_GRID, gbm_params=None, verbose=False):
    """One fitted model per walk-forward fold, exactly as walk_forward fits it (purged training rows, inner
    C / calibration / threshold choice). Returns (list of FoldFit, skipped)."""
    folds = wf.make_folds() if folds is None else list(folds)
    for f in folds:
        wf.check_holdout(f, False)                           # the holdout is never evaluated here
    gbm_params = dict(wf.GBM_PARAMS if gbm_params is None else gbm_params)
    X, y, pn, w, t, te, year, codes = (S[k] for k in ("X", "y", "pnl", "w", "t", "t_end", "year", "codes"))
    data_end = wf.session_label([t.max()])[0] + pd.Timedelta(days=1)
    fits, skipped = [], []
    for f in folds:
        test = np.flatnonzero((t >= f.test_start) & (t < f.test_end))
        tr = np.flatnonzero(wf.train_mask(t, te, f.test_start, f.test_end, f.train_end, purge=purge))
        if len(test) == 0:
            skipped.append((f.name, "no test rows")); continue
        if len(np.unique(year[tr])) < min_train_years:
            skipped.append((f.name, "too few training years")); continue
        t0 = time.time()
        m, thr, info = wf._fit_and_threshold(model, X, y, w, pn, year, te, tr, "entry", codes, min_keep, C_grid,
                                             gbm_params, [], purge, min_inner)
        if m is None:
            skipped.append((f.name, info)); continue
        p = m.predict(X[test])
        fits.append(FoldFit(f.name, tr, test, m, float(thr), info, p, f.span_years(data_end)))
        if verbose:
            print(f"  fit {model} {f.name}: train {len(tr)} test {len(test)} thr {thr:.4f} ({time.time() - t0:.0f}s)",
                  flush=True)
    return fits, skipped


def oos_scores(y, p, pnl, thr):
    """logloss, auc, n_kept, usd_kept ($ per kept trade, NaN when nothing is kept), tot_kept."""
    y = np.asarray(y, np.float64)
    take = np.asarray(p) >= thr
    auc = roc_auc_score(y, p) if 0 < y.sum() < len(y) else np.nan
    nk = int(take.sum())
    tot = float(np.asarray(pnl)[take].sum())
    return dict(logloss=wf.weighted_log_loss(y, p), auc=float(auc), n_kept=nk, usd_kept=tot / nk if nk else np.nan,
                tot_kept=tot)


def base_table(S, fits, n_random=200, seed=0):
    """Per fold: the full model's OOS scores and the baselines at the same number of trades ($ per 1 micro):
    all events, random skip (mean, 5% and 95% of n_random draws)."""
    rng = np.random.default_rng(seed)
    rows = []
    for fit in fits:
        y, pn = S["y"][fit.test], S["pnl"][fit.test]
        s = oos_scores(y, fit.p, pn, fit.thr)
        r = dict(fold=fit.name, years=fit.years, n_test=len(fit.test), threshold=fit.thr, C=fit.info.get("C"), **s,
                 keep_share=s["n_kept"] / len(fit.test), usd_per_year=s["tot_kept"] / fit.years if fit.years else np.nan,
                 all_usd=float(pn.mean()), all_total=float(pn.sum()))
        if s["n_kept"]:
            rt = wf.random_skip(pn, s["n_kept"], n_random, rng)
            r.update(random_usd=float(rt.mean() / s["n_kept"]), random_p5=float(np.quantile(rt, .05) / s["n_kept"]),
                     random_p95=float(np.quantile(rt, .95) / s["n_kept"]))
        rows.append(r)
    return pd.DataFrame(rows)


# ============================================================================================ MDA
def mda(S, fits, groups, features, n_rep=3, seed=0, verbose=False):
    """Mean decrease accuracy of each group of columns ({name: [features]}) per fold (see module doc).
    Returns a long DataFrame: fold, group, n_cols, base_*, perm_*, mda_ll, mda_auc, mda_usd, mda_tot,
    perm_kept."""
    idx = {f: i for i, f in enumerate(features)}
    rng = np.random.default_rng(seed)
    rows = []
    for fit in fits:
        t0 = time.time()
        Xt = S["X"][fit.test].copy()
        y, pn = S["y"][fit.test], S["pnl"][fit.test]
        base = oos_scores(y, fit.p, pn, fit.thr)
        n = len(Xt)
        for g, cols in groups.items():
            ci = [idx[c] for c in cols]
            orig = Xt[:, ci].copy()
            acc = []
            for _ in range(n_rep):
                Xt[:, ci] = orig[rng.permutation(n)]
                acc.append(oos_scores(y, fit.model.predict(Xt), pn, fit.thr))
            Xt[:, ci] = orig
            pm = {k: float(np.nanmean([a[k] for a in acc])) if any(np.isfinite(a[k]) for a in acc) else np.nan
                  for k in acc[0]}
            rows.append(dict(fold=fit.name, group=g, n_cols=len(cols), base_ll=base["logloss"], base_auc=base["auc"],
                             base_usd=base["usd_kept"], base_kept=base["n_kept"], perm_ll=pm["logloss"],
                             perm_auc=pm["auc"], perm_usd=pm["usd_kept"], perm_kept=pm["n_kept"],
                             mda_ll=pm["logloss"] - base["logloss"], mda_auc=base["auc"] - pm["auc"],
                             mda_usd=base["usd_kept"] - pm["usd_kept"], mda_tot=base["tot_kept"] - pm["tot_kept"]))
        if verbose:
            print(f"  mda {fit.name}: {len(groups)} groups x {n_rep} ({time.time() - t0:.0f}s)", flush=True)
    return pd.DataFrame(rows)


# ============================================================================================ SFI
def _bin_codes(x_tr, x_te, n_bins):
    """Bin codes of training / test values: one code per distinct value when there are <= n_bins of them (others
    -> nearest code by searchsorted), else quantile bins from the training values; NaN -> its own last code."""
    fin = np.isfinite(x_tr)
    u = np.unique(x_tr[fin])
    if len(u) <= n_bins:
        edges = (u[1:] + u[:-1]) / 2                       # midpoints between the distinct values
    else:
        edges = np.unique(np.quantile(x_tr[fin], np.linspace(0, 1, n_bins + 1))[1:-1])
    nb = len(edges) + 1

    def code(x):
        c = np.searchsorted(edges, x, side="right")
        return np.where(np.isfinite(x), c, nb)
    return code(x_tr), code(x_te), nb + 1


def sfi(S, fits, features, C=1.0, n_bins=10, shrink=50.0, verbose=False):
    """Single feature importance per fold and feature (see module doc). `fits` gives the folds' train / test rows.
    Returns a long DataFrame: fold, feature, ll0, ll_logit1, ll_bin1, sfi_ll_logit1, sfi_ll_bin1, auc_logit1,
    auc_bin1."""
    X, y, w = S["X"], S["y"].astype(np.float64), S["w"]
    rows = []
    for fit in fits:
        t0 = time.time()
        tr, te = fit.tr, fit.test
        wt = wf._norm(w[tr])
        ytr, yte = y[tr], y[te]
        p0 = float(np.average(ytr, weights=wt))
        ll0 = wf.weighted_log_loss(yte, np.full(len(te), p0))
        for j, f in enumerate(features):
            xtr, xte = X[tr, j].astype(np.float64), X[te, j].astype(np.float64)
            r = dict(fold=fit.name, feature=f, ll0=ll0)
            ok = np.isfinite(xtr)
            if len(np.unique(xtr[ok])) < 2:
                r.update(ll_logit1=np.nan, ll_bin1=np.nan, auc_logit1=np.nan, auc_bin1=np.nan)
                rows.append(r); continue
            pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                                 LogisticRegression(C=C, max_iter=300))
            pipe.fit(xtr[:, None], ytr, logisticregression__sample_weight=wt)
            p1 = pipe.predict_proba(xte[:, None])[:, 1]
            ctr, cte, nb = _bin_codes(xtr, xte, n_bins)
            sw = np.bincount(ctr, weights=wt, minlength=nb)
            sy = np.bincount(ctr, weights=wt * ytr, minlength=nb)
            rate = (sy + shrink * p0) / (sw + shrink)
            p2 = rate[cte]
            auc = lambda p: roc_auc_score(yte, p) if 0 < yte.sum() < len(yte) and np.ptp(p) > 0 else np.nan
            r.update(ll_logit1=wf.weighted_log_loss(yte, p1), ll_bin1=wf.weighted_log_loss(yte, p2),
                     auc_logit1=auc(p1), auc_bin1=auc(p2))
            rows.append(r)
        if verbose:
            print(f"  sfi {fit.name}: {len(features)} features ({time.time() - t0:.0f}s)", flush=True)
    df = pd.DataFrame(rows)
    df["sfi_ll_logit1"] = df["ll0"] - df["ll_logit1"]
    df["sfi_ll_bin1"] = df["ll0"] - df["ll_bin1"]
    return df


# ============================================================================================ summaries
def summarize(long, key, cols):
    """Per `key` value: for every metric in cols, mean, sd, t (= mean / (sd / sqrt(n))), share of folds > 0,
    over the folds. Returns a DataFrame indexed by key."""
    out = {}
    g = long.groupby(key, sort=False)
    for c in cols:
        m, s, n = g[c].mean(), g[c].std(ddof=1), g[c].count()
        out[f"{c}_mean"] = m
        out[f"{c}_sd"] = s
        out[f"{c}_t"] = m / (s / np.sqrt(n)).replace(0, np.nan)
        out[f"{c}_pos"] = g[c].apply(lambda v: float((v > 0).mean()))
    out["n_folds"] = g[cols[0]].count()
    return pd.DataFrame(out)


def rank(df, by="mda_ll_mean"):
    return df.sort_values(by, ascending=False)
