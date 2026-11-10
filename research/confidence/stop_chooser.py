"""
ML STOP CHOOSER (NEXT_STEPS item 16): for every MNQ 15-min candle entry event, pick ONE of the 9 stop options of
stop_options.py (pattern, pattern_min1, pattern_cost, swing5, swing10, avg1, avg2, usd40, usd100) from what is known
at the signal bar's close, and optionally skip the trade. Labels = out/stops_<SYM>_15.parquet (pnl_usd_1.5 per
option: entry at the next bar's open, target 1.5 x risk, 16-bar / 16:45 limit, 1-minute path, costs + stop tick).

Features per event (known at the signal bar's close): the v1 entry features (run_pipeline.feature_list('entry'),
oriented by the trade direction d with features.SIGNED / MIRROR) from out/entries_<SYM>_15.parquet, plus per option
o, as compare_stops.py: dist_o = d * (C_t - stop_o) (points), stop_R20_o = dist_o / R20_t, cost_R_o = cost $ /
max(dist_o * $/pt, 1e-9).

Approaches
  reg  (approach 1)  one regression model per option o, inputs = common features + (stop_R20_o, cost_R_o),
                     target = pnl_usd_1.5 of option o. Pick o* = argmax predicted $; score = predicted $ of o*.
                     model 'hgb' = HistGradientBoostingRegressor(max_depth=3, lr=0.05, 200 iters, leaf>=500, l2=1)
                     model 'ridge' = median impute + standardize + Ridge, alpha chosen on the inner validation MSE.
  clf  (approach 2)  one multi-class HistGradientBoostingClassifier (same settings), inputs = common features + all
                     9 options' (stop_R20, cost_R); class = the option with the highest realised pnl_usd_1.5 (ties ->
                     first in OPTIONS order). Pick o* = argmax probability; score = that probability.
  Decision: 'all'  = take every event with o*;  'thr' = take only if score >= threshold, the threshold chosen by
  walkforward.select_threshold (max mean realised $ of o* with >= 5% kept) on the INNER validation predictions.

Walk-forward (own loop, reusing walkforward.make_folds / train_mask / sample_weights / before_holdout):
  folds 2013..2024 + 2025H1 (expanding by calendar year); training rows purged (t_end <= test start - 1 day), where
  t_end = the LATEST label end over the 9 options of that event (the most conservative purge); >= 3 training years.
  Inner split per fold: validation = last 2 training years, inner training = earlier years purged against the
  validation start. Inner models -> threshold; final models refitted on all training rows -> test predictions.
  Sample weights: walkforward.sample_weights (uniqueness over [t, t_end]); one weight per event for all options.
  The locked holdout (2025-06-30 18:00 onward) is dropped (before_holdout) and make_folds refuses it.

Baselines on the SAME test events (out of sample, $ per 1 micro after costs):
  fixed_<o>          always option o, every event (9 rows)
  best_fixed_train   the single option with the highest mean $ on the fold's training rows, every event
  random_option      a uniformly random option per event (expected value = mean over options; 5-95% of 200 draws)
  oracle             the ex-post best option per event (NOT achievable; scale of what a perfect chooser could do)
  chooser_all / chooser_thr   the approach above
  rskip_chosen       random skip: as many random test events as chooser_thr takes, with the chooser's option
  rskip_bestfixed    the same with the best fixed training option

  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 stop_chooser.py NQ [reg-hgb clf-hgb reg-ridge]
Writes out/stop_chooser_<SYM>.csv (long table: approach, strategy, period = test year or 'pooled', n, trades/year,
$/trade, $/year, ...) and logs one trials.csv row per approach (module 'entry-stop-chooser').
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")    # the machine is shared: oversubscribed OpenMP is ~40x slower
import gc
import json
import sys
import time
import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import walkforward as wf

warnings.filterwarnings("ignore")
OPTIONS = ["pattern", "pattern_min1", "pattern_cost", "swing5", "swing10", "avg1", "avg2", "usd40", "usd100"]
HGB = dict(max_depth=3, learning_rate=0.05, max_iter=200, l2_regularization=1.0, min_samples_leaf=500,
           early_stopping=False, random_state=0)
ALPHAS = (1.0, 10.0, 100.0, 1e3, 1e4, 1e5)
PNL, TEND = "pnl_usd_1.5", "t_end_1.5"


@dataclass
class Config:
    method: str = "reg"               # 'reg' (approach 1) or 'clf' (approach 2)
    model: str = "hgb"                # 'hgb' or 'ridge' (reg only)
    hgb: dict = field(default_factory=lambda: dict(HGB))
    alphas: tuple = ALPHAS
    min_keep: float = 0.05
    inner_years: int = 2
    min_train_years: int = 3
    min_inner: int = 200
    n_random: int = 200
    seed: int = 0

    @property
    def name(self):
        return f"{self.method}-{self.model}"


# ============================================================================================ data
def load_events(sym="NQ", tf=15, bars_close=None):
    """Wide event table for the chooser. Returns dict:
    Xc (DataFrame n x f, oriented common features), Xopt (n, K, 2) float32 = per option (stop_R20, cost_R),
    P (n, K) pnl_usd_1.5, TE (n, K) label ends (datetime64), t, t_end (= max over options), d, i, options.
    bars_close: the signal-bar closes C of signals.bars(sym, tf) (loaded here when None - heavy)."""
    import features as fe                                    # noqa: PLC0415
    import run_pipeline as rp                                 # noqa: PLC0415
    import signals as sg                                      # noqa: PLC0415
    spec = sg.SPEC[sym]; usd, cost = spec["usd"], spec["cost"]
    feats = [c for c in rp.feature_list("entry", sym) if c not in rp.ENTRY_EXTRA]
    E = pd.read_parquet(f"out/entries_{sym}_{tf}.parquet", columns=["t", "i", "d", "market", "R20"] + feats)
    E["key"] = E["i"].to_numpy(np.int64) * 4 + (E["d"].to_numpy(np.int64) + 1)
    E = E.sort_values("key", kind="stable").reset_index(drop=True)
    assert E["key"].is_unique, "duplicate (i, d) in entries"
    S = pd.read_parquet(f"out/stops_{sym}_{tf}.parquet", columns=["i", "d", "t", "stop", PNL, TEND, "stop_option"])
    S["key"] = S["i"].to_numpy(np.int64) * 4 + (S["d"].to_numpy(np.int64) + 1)
    n, K = len(E), len(OPTIONS)
    P = np.full((n, K), np.nan); STOP = np.full((n, K), np.nan)
    TE = np.full((n, K), np.datetime64("NaT"), dtype="datetime64[ns]")
    key = E["key"].to_numpy()
    for k, o in enumerate(OPTIONS):
        g = S.loc[S.stop_option == o]
        pos = np.searchsorted(key, g["key"].to_numpy())
        ok = (pos < n) & (key[np.minimum(pos, n - 1)] == g["key"].to_numpy())
        assert ok.all(), f"{o}: {(~ok).sum()} stop rows without an entry row"
        P[pos, k] = g[PNL].to_numpy(np.float64)
        STOP[pos, k] = g["stop"].to_numpy(np.float64)
        TE[pos, k] = pd.DatetimeIndex(g[TEND]).as_unit("ns").to_numpy()
        tt = pd.DatetimeIndex(g["t"]).as_unit("ns").to_numpy()
        assert (tt == pd.DatetimeIndex(E["t"]).as_unit("ns").to_numpy()[pos]).all(), f"{o}: t mismatch"
    del S; gc.collect()
    full = np.isfinite(P).all(axis=1) & ~np.isnat(TE).any(axis=1)
    if bars_close is None:
        bars_close = sg.bars(sym, tf).C.to_numpy(np.float64)
    i = E["i"].to_numpy(np.int64); d = E["d"].to_numpy(np.float64)
    C = np.asarray(bars_close, np.float64)[i]
    Xopt, dist = option_features(C, STOP, d, E["R20"].to_numpy(np.float64), usd, cost)
    Xc = wf.orient(E[feats], d, list(fe.SIGNED), dict(fe.MIRROR))
    t = pd.DatetimeIndex(E["t"]).as_unit("ns")
    out = dict(Xc=Xc, Xopt=Xopt, P=P, TE=TE, t=t, d=d, i=i, options=list(OPTIONS), features=feats,
               dist_min=float(np.nanmin(dist)))
    return subset(out, full)


def option_features(C, STOP, d, R20, usd, cost):
    """Per-option trade features, as compare_stops.py: dist = d * (C - stop) points (signal close -> stop),
    stop_R20 = dist / R20, cost_R = cost $ / max(dist * $/pt, 1e-9). C, d, R20 (n,), STOP (n, K).
    Returns (Xopt (n, K, 2) float32, dist (n, K))."""
    C = np.asarray(C, np.float64); d = np.asarray(d, np.float64); R20 = np.asarray(R20, np.float64)
    dist = d[:, None] * (C[:, None] - np.asarray(STOP, np.float64))
    with np.errstate(divide="ignore", invalid="ignore"):
        X = np.stack([dist / R20[:, None], cost / np.maximum(dist * usd, 1e-9)], axis=2).astype(np.float32)
    return X, dist


def subset(D, mask):
    m = np.asarray(mask, bool)
    out = dict(D)
    out["Xc"] = D["Xc"].loc[m].reset_index(drop=True) if isinstance(D["Xc"], pd.DataFrame) else D["Xc"][m]
    for k in ("Xopt", "P", "TE", "d", "i"):
        out[k] = D[k][m]
    out["t"] = D["t"][m]
    return out


# ============================================================================================ models
def _option_matrix(Xc, Xopt, k):
    return np.hstack([Xc, Xopt[:, k, :]]).astype(np.float32)


def _ridge(alpha):
    return make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True), StandardScaler(),
                         Ridge(alpha=alpha))


def _fit_reg(cfg, X, y, w, alpha=None):
    if cfg.model == "hgb":
        return HistGradientBoostingRegressor(**cfg.hgb).fit(X, y, sample_weight=w)
    m = _ridge(alpha)
    return m.fit(X, y, ridge__sample_weight=w)


def fit_predict_reg(cfg, Xc, Xopt, P, w, fit_idx, pred_idx, alphas=None, val_idx=None):
    """Approach 1. One model per option fitted on fit_idx; returns (pred (len(pred_idx), K), alphas used).
    Ridge: when val_idx is given, alpha per option is chosen on val_idx MSE (fit on fit_idx); else `alphas`."""
    K = P.shape[1]
    S = np.empty((len(pred_idx), K))
    used = []
    wf_ = wf._norm(w[fit_idx])
    for k in range(K):
        Xf = _option_matrix(Xc[fit_idx], Xopt[fit_idx], k)
        a = None
        if cfg.model == "ridge":
            if val_idx is not None:
                Xv = _option_matrix(Xc[val_idx], Xopt[val_idx], k)
                best = (np.inf, None)
                for a_ in cfg.alphas:
                    pv = _fit_reg(cfg, Xf, P[fit_idx, k], wf_, a_).predict(Xv)
                    mse = float(np.average((pv - P[val_idx, k]) ** 2, weights=w[val_idx]))
                    if mse < best[0]:
                        best = (mse, a_)
                a = best[1]
            else:
                a = alphas[k]
        # trees: drop columns with < 2 distinct finite values in the fit rows (e.g. x_YM_* before 2018);
        # scikit-learn's HGB binning crashes on an all-NaN column. Same rule as walkforward.GBMModel.
        cols = wf.informative_columns(Xf, wf_) if cfg.model == "hgb" else slice(None)
        m = _fit_reg(cfg, Xf[:, cols], P[fit_idx, k], wf_, a)
        S[:, k] = m.predict(_option_matrix(Xc[pred_idx], Xopt[pred_idx], k)[:, cols])
        used.append(a)
        del Xf, m
    return S, used


def winner(P):
    """Index of the option with the highest realised $ per event (ties -> first in order)."""
    return np.argmax(P, axis=1)


def fit_predict_clf(cfg, Xc, Xopt, P, w, fit_idx, pred_idx):
    """Approach 2. Multi-class classifier of the winning option. Returns probabilities (len(pred_idx), K)."""
    K = P.shape[1]
    flat = lambda idx: np.hstack([Xc[idx], Xopt[idx].reshape(len(idx), -1)]).astype(np.float32)  # noqa: E731
    y = winner(P[fit_idx])
    Xf, wn = flat(fit_idx), wf._norm(w[fit_idx])
    cols = wf.informative_columns(Xf, wn)          # drop all-NaN / constant columns (HGB binning crash)
    m = HistGradientBoostingClassifier(**cfg.hgb).fit(Xf[:, cols], y, sample_weight=wn)
    pr = m.predict_proba(flat(pred_idx)[:, cols])
    out = np.zeros((len(pred_idx), K))
    out[:, m.classes_] = pr
    return out


def fit_predict(cfg, Xc, Xopt, P, w, fit_idx, pred_idx, val_idx=None, alphas=None):
    if cfg.method == "reg":
        return fit_predict_reg(cfg, Xc, Xopt, P, w, fit_idx, pred_idx, alphas=alphas, val_idx=val_idx)
    if cfg.method == "clf":
        return fit_predict_clf(cfg, Xc, Xopt, P, w, fit_idx, pred_idx), None
    raise ValueError(cfg.method)


def threshold(score, pnl, min_keep):
    """walkforward.select_threshold on (score, realised $), but 'keep everything' -> -inf (select_threshold returns
    0.0 there, which on a $ scale would wrongly drop every negative prediction)."""
    thr, info = wf.select_threshold(score, pnl, min_keep)
    if info.get("keep_share", 0) >= 1.0:
        thr = -np.inf
    return thr, info


# ============================================================================================ walk-forward
def run_chooser(Xc, Xopt, P, t, t_end, cfg=None, w=None, d=None, folds=None, final=False, data_end=None,
                verbose=False):
    """Walk-forward stop chooser. Xc (n, f) common features (already oriented), Xopt (n, K, g) option features,
    P (n, K) realised $ per option, t signal-bar times, t_end label ends (latest over the options).
    Returns (O, F): O = one row per OOS event (fold, row = position in the inputs, t, choice, score, take, best_fixed, pnl of every option),
    F = one row per fold (threshold, inner info, training sizes, purge check)."""
    cfg = cfg or Config()
    Xc = np.asarray(Xc, np.float32); Xopt = np.asarray(Xopt, np.float32); P = np.asarray(P, np.float64)
    t = pd.DatetimeIndex(t).as_unit("ns"); te = pd.DatetimeIndex(t_end).as_unit("ns")
    d = np.ones(len(t)) if d is None else np.asarray(d)
    df = pd.DataFrame({"t": t, "t_end": te, "d": d, "market": "X"})
    keep = np.isfinite(P).all(axis=1) & ~pd.isna(te)
    if not final:
        keep &= wf.before_holdout(df)
    idx_all = np.flatnonzero(keep)
    Xc, Xopt, P, df = Xc[idx_all], Xopt[idx_all], P[idx_all], df.iloc[idx_all].reset_index(drop=True)
    t, te = pd.DatetimeIndex(df.t), pd.DatetimeIndex(df.t_end)
    if w is None:
        w = wf.sample_weights(df)
    else:
        w = np.asarray(w, np.float64)[idx_all]
    year = t.year.to_numpy()
    folds = wf.make_folds(final=final) if folds is None else list(folds)
    for f in folds:
        wf.check_holdout(f, final)
    if data_end is None and len(t):
        data_end = wf.session_label([t.max()])[0] + pd.Timedelta(days=1)
    O, F = [], []
    K = P.shape[1]
    cache = {}
    every = np.arange(len(t))

    def cached(fit_idx):
        key = (len(fit_idx), int(fit_idx.sum()), int(fit_idx[0]), int(fit_idx[-1]))
        if key not in cache:
            cache[key] = fit_predict(cfg, Xc, Xopt, P, w, fit_idx, every)[0].astype(np.float32)
        return cache[key]
    for f in folds:
        t0 = time.time()
        test = np.flatnonzero((t >= f.test_start) & (t < f.test_end))
        tr = np.flatnonzero(wf.train_mask(t, te, f.test_start, f.test_end, f.train_end))
        if len(test) == 0 or len(np.unique(year[tr])) < cfg.min_train_years:
            continue
        Y = int(year[tr].max())
        val_first = Y - cfg.inner_years + 1
        val_start = pd.Timestamp(val_first, 1, 1)
        va = tr[year[tr] >= val_first]
        it = tr[(year[tr] < val_first) & (te[tr] <= val_start - wf.PURGE)]
        if len(it) < cfg.min_inner or len(va) < cfg.min_inner:
            continue
        if cfg.model == "hgb":
            # the inner training set of fold Y equals the full training set of fold Y - inner_years (same purged
            # expanding window), so one fit per training set, predicting every row, serves both roles
            al = None
            Sv = cached(it)[va]
            St = cached(tr)[test]
        else:
            Sv, al = fit_predict(cfg, Xc, Xopt, P, w, it, va, val_idx=va)
            St, _ = fit_predict(cfg, Xc, Xopt, P, w, tr, test, alphas=al)
        cv = np.argmax(Sv, axis=1)
        thr, tinfo = threshold(Sv[np.arange(len(va)), cv], P[va, cv], cfg.min_keep)
        ch = np.argmax(St, axis=1)
        sc = St[np.arange(len(test)), ch]
        bf = int(np.argmax(P[tr].mean(axis=0)))                       # best fixed option on the training years
        o = pd.DataFrame({"fold": f.name, "row": idx_all[test], "t": t[test], "choice": ch, "score": sc, "take": sc >= thr,
                          "best_fixed": bf})
        for k in range(K):
            o[f"pnl_{k}"] = P[test, k]
        O.append(o)
        F.append(dict(fold=f.name, years=f.span_years(data_end), n_train=len(tr), n_inner=len(it), n_val=len(va),
                      n_test=len(test), threshold=thr, val_keep_share=tinfo.get("keep_share"),
                      val_usd_trade=tinfo.get("mean_usd"), best_fixed=bf,
                      alphas=json.dumps(al) if al and al[0] is not None else "",
                      max_train_t_end=te[tr].max(), test_start=f.test_start,
                      purge_ok=bool((te[tr] <= f.test_start - wf.PURGE).all()), secs=round(time.time() - t0)))
        if verbose:
            print(f"  {cfg.name} fold {f.name}: train {len(tr):,} test {len(test):,} thr {thr:.3f} "
                  f"keep {np.mean(sc >= thr):.1%} ({time.time() - t0:.0f}s)", flush=True)
        gc.collect()
    O = pd.concat(O, ignore_index=True) if O else pd.DataFrame()
    return O, pd.DataFrame(F)


# ============================================================================================ evaluation
def evaluate(O, F, options, approach, n_random=200, seed=0):
    """Long table: per test year (fold) and pooled, for every strategy: n, trades/year, $/trade, $/year (+ 5-95%
    of the random baselines, pooled)."""
    rng = np.random.default_rng(seed)
    K = len(options)
    rows = []
    pooled = {}
    rand_tot = {"random_option": 0.0, "rskip_chosen": 0.0, "rskip_bestfixed": 0.0}

    def add(period, strat, pnl, years, extra=None):
        pnl = np.asarray(pnl, np.float64)
        r = dict(approach=approach, strategy=strat, period=period, n=len(pnl), years=years,
                 trades_per_year=len(pnl) / years if years else np.nan,
                 usd_per_trade=pnl.mean() if len(pnl) else np.nan, usd_total=pnl.sum(),
                 usd_per_year=pnl.sum() / years if years else np.nan, hit=(pnl > 0).mean() if len(pnl) else np.nan)
        r.update(extra or {})
        rows.append(r)
        if period != "pooled":
            pooled.setdefault(strat, []).append(pnl)

    for _, fr in F.iterrows():
        g = O.loc[O.fold == fr.fold]
        if g.empty:
            continue
        Pt = g[[f"pnl_{k}" for k in range(K)]].to_numpy()
        m = len(g); ar = np.arange(m)
        ch = g.choice.to_numpy(); take = g["take"].to_numpy(bool); bf = int(fr.best_fixed); yrs = fr.years
        for k, o in enumerate(options):
            add(fr.fold, f"fixed_{o}", Pt[:, k], yrs)
        add(fr.fold, "best_fixed_train", Pt[:, bf], yrs, dict(option=options[bf]))
        add(fr.fold, "random_option", Pt.mean(axis=1), yrs)
        add(fr.fold, "oracle", Pt.max(axis=1), yrs)
        add(fr.fold, "chooser_all", Pt[ar, ch], yrs)
        add(fr.fold, "chooser_thr", Pt[ar, ch][take], yrs, dict(threshold=fr.threshold))
        n_take = int(take.sum())
        draws = rng.integers(0, K, size=(n_random, m))
        rand_tot["random_option"] = rand_tot["random_option"] + Pt[ar[None, :], draws].sum(axis=1)
        rand_tot["rskip_chosen"] = rand_tot["rskip_chosen"] + wf.random_skip(Pt[ar, ch], n_take, n_random, rng)
        rand_tot["rskip_bestfixed"] = rand_tot["rskip_bestfixed"] + wf.random_skip(Pt[:, bf], n_take, n_random, rng)
        add(fr.fold, "rskip_chosen", np.full(n_take, Pt[ar, ch].mean()), yrs)
        add(fr.fold, "rskip_bestfixed", np.full(n_take, Pt[:, bf].mean()), yrs)
    years = float(F.years.sum())
    for strat, parts in pooled.items():
        pnl = np.concatenate(parts)
        ex = {}
        if strat in rand_tot:
            tot = np.asarray(rand_tot[strat], np.float64)
            ex = dict(p5_usd_per_trade=np.quantile(tot, 0.05) / max(len(pnl), 1),
                      p95_usd_per_trade=np.quantile(tot, 0.95) / max(len(pnl), 1))
        add("pooled", strat, pnl, years, ex)
    T = pd.DataFrame(rows)
    # paired comparison chooser_all vs best_fixed_train on the same events (naive SE: events treated independently)
    ca, bfx = np.concatenate(pooled["chooser_all"]), np.concatenate(pooled["best_fixed_train"])
    diff = ca - bfx
    se = diff.std(ddof=1) / np.sqrt(len(diff))
    pick = np.bincount(O.choice.to_numpy(), minlength=K) / len(O)
    msk = (T.period == "pooled") & (T.strategy == "chooser_all")
    T.loc[msk, "diff_vs_best_fixed"] = diff.mean()
    T.loc[msk, "diff_se"] = se
    T.loc[msk, "picks"] = ",".join(f"{o}:{p:.0%}" for o, p in zip(options, pick))
    return T


def summary(T):
    """Pooled table: strategy -> n, trades/yr, $/trade, $/year, random 5-95%."""
    p = T.loc[T.period == "pooled"].set_index("strategy")
    cols = [c for c in ("n", "trades_per_year", "usd_per_trade", "usd_per_year", "p5_usd_per_trade",
                        "p95_usd_per_trade") if c in p]
    return p[cols]


def by_year(T, strategies):
    t = T.loc[(T.period != "pooled") & T.strategy.isin(strategies)]
    return t.pivot(index="period", columns="strategy", values="usd_per_year")[list(strategies)]


# ============================================================================================ main
def main(sym="NQ", approaches=("reg-hgb", "clf-hgb", "reg-ridge")):
    import subprocess                                         # noqa: PLC0415
    import run_pipeline as rp                                 # noqa: PLC0415

    def wait_ram(need=7000):
        while True:
            avail = int(subprocess.run(["free", "-m"], capture_output=True, text=True).stdout.split("\n")[1].split()[6])
            if avail >= need:
                return avail
            print(f"waiting for RAM: {avail} MB available", flush=True)
            time.sleep(60)

    t0 = time.time()
    wait_ram()
    import signals as sg                                      # noqa: PLC0415
    Cb = sg.bars(sym, 15).C.to_numpy(np.float64)
    gc.collect()
    D = load_events(sym, bars_close=Cb)
    del Cb; gc.collect()
    te = D["TE"].max(axis=1)
    print(f"{sym}: {len(D['P']):,} events x {len(OPTIONS)} options, {D['Xc'].shape[1]} common features, "
          f"min stop dist {D['dist_min']:.2f} pts ({time.time() - t0:.0f}s)", flush=True)
    out_path = f"out/stop_chooser_{sym}.csv"
    allT = []
    for a in approaches:
        method, model = a.split("-")
        cfg = Config(method=method, model=model)
        wait_ram()
        ta = time.time()
        O, F = run_chooser(D["Xc"].to_numpy(np.float32), D["Xopt"], D["P"], D["t"], te, cfg=cfg, d=D["d"],
                           verbose=True)
        assert F.purge_ok.all()
        T = evaluate(O, F, OPTIONS, a, n_random=cfg.n_random, seed=cfg.seed)
        allT.append(T)
        pd.concat(allT, ignore_index=True).to_csv(out_path, index=False)
        F.to_csv(f"out/stop_chooser_folds_{sym}_{a}.csv", index=False)
        s = summary(T)
        print(s.round(2).to_string(), flush=True)
        print(T.loc[(T.period == "pooled") & (T.strategy == "chooser_all"), ["diff_vs_best_fixed", "diff_se",
                                                                             "picks"]].to_string(), flush=True)
        for dec in ("chooser_all", "chooser_thr"):
            r = s.loc[dec]
            rp.log_trial(module="entry-stop-chooser", scope=sym, model=a, target=PNL, n_folds=len(F),
                         oos_rows=int(s.loc["chooser_all", "n"]), oos_auc="", oos_kept=int(r.n),
                         oos_keep_share=round(float(r.n / s.loc["chooser_all", "n"]), 4),
                         oos_usd_total=round(float(r.usd_per_trade * r.n), 2),
                         oos_usd_per_trade=round(float(r.usd_per_trade), 3),
                         oos_usd_per_year=round(float(r.usd_per_year), 1),
                         baseline_usd_per_trade=round(float(s.loc["best_fixed_train", "usd_per_trade"]), 3),
                         runtime_s=round(time.time() - ta),
                         parameters=json.dumps(dict(approach=a, decision=dec, options=OPTIONS, hgb=cfg.hgb,
                                                    alphas=list(cfg.alphas) if model == "ridge" else None,
                                                    min_keep=cfg.min_keep, inner_years=cfg.inner_years,
                                                    purge="t_end=max over options, 1 day",
                                                    folds="2013..2024 + 2025H1")),
                         note="ML stop chooser; baseline = best fixed option chosen on training years")
        del O; gc.collect()
    print(f"saved {out_path} in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    args = sys.argv[1:]
    sym = args[0] if args else "NQ"
    main(sym, tuple(args[1:]) or ("reg-hgb", "clf-hgb", "reg-ridge"))
