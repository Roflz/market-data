"""
Combinatorial purged cross-validation (CPCV) and backtest-overfitting statistics (deflated Sharpe ratio, probability
of backtest overfitting by CSCV) for the confidence study.

References (formulas checked against the papers' text, 2026-11-09):
  [AFML]  M. Lopez de Prado, "Advances in Financial Machine Learning", Wiley 2018, ch. 7 (purging, embargo) and
          ch. 12 (CPCV): split T observations into N groups in time order, test on every combination of k groups and
          train on the other N - k (purged + embargoed). That gives C(N, k) splits; every group is tested in
          C(N-1, k-1) of them, so the out-of-sample predictions can be stitched into
          phi[N, k] = k / N * C(N, k) = C(N-1, k-1) complete backtest PATHS (each path covers every group once).
          AFML's path assignment (snippet 12.1 / fig. 12.1): the j-th time group g appears in a test set, its
          predictions go to path j.
  [DSR]   D. Bailey, M. Lopez de Prado, "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest
          Overfitting and Non-Normality", Journal of Portfolio Management 40(5), 2014, 94-107. Eq. (2):
              DSR = Z[ (SR^ - SR0) * sqrt(T - 1) / sqrt(1 - g3 * SR^ + (g4 - 1) / 4 * SR^2) ]
              SR0 = sqrt(V[{SR_n}]) * ((1 - gamma) * Z^-1[1 - 1/N] + gamma * Z^-1[1 - 1/(N e)])
          SR^ = the selected strategy's NON-annualized Sharpe ratio (per observation), T = number of observations,
          g3 = skewness, g4 = kurtosis (NOT excess: 3 for Normal returns), V[{SR_n}] = variance of the N trials'
          estimated SRs (same frequency), N = number of independent trials, gamma = 0.5772... (Euler-Mascheroni),
          e = Euler's number, Z = standard Normal CDF. Paper's worked example (N=100, V = 1/2 annualized, T = 1250
          daily, 250 obs/year, annualized SR 2.5, g3 = -3, g4 = 10): DSR = 0.9004; with N = 46: 0.9505
          (test_cpcv.py checks both). With SR0 = 0 the formula is the probabilistic Sharpe ratio (PSR).
  [PBO]   D. Bailey, J. Borwein, M. Lopez de Prado, Q. J. Zhu, "The Probability of Backtest Overfitting", Journal of
          Computational Finance 20(4), 2017 (SSRN 2326253), Algorithm 2.3 (CSCV): M = T x N matrix of the N trials'
          performance series on SYNCHRONOUS rows; split the rows into an even number S of disjoint submatrices;
          for each of the C(S, S/2) combinations c: J = the S/2 blocks of c (in-sample), J-bar = the rest
          (out-of-sample); n* = the best configuration on J; omega_c = (OOS rank of n* among the N, 1 = worst) /
          (N + 1); logit lambda_c = ln(omega_c / (1 - omega_c)); PBO = share of combinations with lambda_c <= 0
          (the IS-best configuration is at or below the OOS median). Also reported (their section 3): probability
          of loss = share of combinations where n*'s OOS performance < 0, and performance degradation = slope of
          OOS on IS performance of n*.

Public functions
  make_groups(t, n_groups, sessions)        group id (0..N-1) per time-sorted row, near-equal counts, boundaries
                                            moved to the nearest Globex session start (a session is never split).
  split_combinations(n_groups, k)           the C(N, k) test-group tuples, in itertools order.
  n_paths(n_groups, k)                      phi = k/N * C(N, k).
  path_matrix(n_groups, splits)             (n_paths, n_groups): split index whose predictions fill path j, group g.
  test_blocks(groups, test_groups)          maximal runs of adjacent test groups -> (first row, last row) pairs.
  cpcv_train_mask(...)                      training rows of one split: not in a test group, purged, embargoed.
  run_cpcv(X, y, pnl, t, t_end, fit, ...)   fit/threshold on every split's training rows, predict its test rows,
                                            assemble the paths -> CPCVResult (per-split table, path p / take).
  wf_fitter(...)                            the walk-forward's own fit + threshold rule (walkforward._fit_and_threshold:
                                            inner validation = last 2 training years for logit, last year for gbm;
                                            threshold = max mean $ per trade with >= 5% kept, on those inner
                                            out-of-sample predictions only) for use as run_cpcv's `fit`.
  path_stats / path_by_year / random_skip_paths   $ per path and by year, random-skip baseline at each path's
                                            trade count.
  sharpe, expected_max_sharpe, psr, deflated_sharpe   DSR [DSR].
  pbo_cscv(M, S, metric)                    PBO by CSCV [PBO].

Conventions: rows are events sorted by signal time t (bar start, New York). A row's label window is [t, t_end]
(t_end = the end of its label path). Purging removes every training row whose window [t, t_end] overlaps a test
block's window [first t - purge, last t_end] (`purge` = extra margin before the block: the walk-forward's 1 day).
The embargo removes, after each test block, the next ceil(embargo_frac * T) rows and/or the rows of the next
`embargo_sessions` sessions (features look back up to ~20 sessions, so rows right after a test block carry
test-period prices in their features). Nothing here reads the locked holdout: callers pass pre-holdout rows only
(run_cpcv.py uses walkforward._prepare(final=False), which drops them).
"""
import inspect
import itertools
import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

EULER_GAMMA = 0.5772156649015329


# ============================================================================================ CPCV: groups, splits, paths
def make_groups(t, n_groups, sessions=None):
    """Group id 0..n_groups-1 for each row of time-sorted timestamps t: contiguous blocks of near-equal row counts
    whose boundaries are moved to the nearest session start (sessions = per-row session labels, default: calendar
    date of t + 6 h, the Globex session). Raises if t is not sorted or there are fewer sessions than groups."""
    t = pd.DatetimeIndex(t)
    n = len(t)
    if n == 0 or n_groups < 2:
        raise ValueError("need rows and at least 2 groups")
    if not t.is_monotonic_increasing:
        raise ValueError("rows must be sorted by t")
    if sessions is None:
        sessions = (t + pd.Timedelta(hours=6)).normalize()
    s = np.asarray(pd.factorize(np.asarray(sessions))[0])
    starts = np.r_[0, np.flatnonzero(s[1:] != s[:-1]) + 1]           # first row of each session
    if len(starts) < n_groups:
        raise ValueError(f"{len(starts)} sessions < {n_groups} groups")
    bounds = [0]
    for i in range(1, n_groups):
        target = i * n / n_groups
        j = int(np.argmin(np.abs(starts - target)))
        b = int(starts[j])
        if b <= bounds[-1]:                                          # keep strictly increasing
            nxt = starts[starts > bounds[-1]]
            b = int(nxt[0])
        bounds.append(b)
    bounds.append(n)
    if np.any(np.diff(bounds) <= 0):
        raise ValueError("could not form non-empty groups")
    g = np.empty(n, np.int16)
    for i in range(n_groups):
        g[bounds[i]:bounds[i + 1]] = i
    return g


def split_combinations(n_groups, k):
    """All C(n_groups, k) test-group combinations (sorted tuples), itertools order."""
    return list(itertools.combinations(range(n_groups), k))


def n_paths(n_groups, k):
    """phi[N, k] = k / N * C(N, k) = C(N-1, k-1) backtest paths [AFML ch. 12]."""
    return math.comb(n_groups, k) * k // n_groups


def path_matrix(n_groups, splits):
    """(n_paths, n_groups) int array: P[j, g] = index of the split whose test predictions of group g form path j.
    AFML's assignment: walk the splits in order; the j-th split that tests group g feeds path j."""
    k = len(splits[0])
    P = np.full((n_paths(n_groups, k), n_groups), -1, np.int64)
    cnt = np.zeros(n_groups, np.int64)
    for s, comb in enumerate(splits):
        for g in comb:
            P[cnt[g], g] = s
            cnt[g] += 1
    if (P < 0).any():
        raise AssertionError("incomplete path matrix")
    return P


def test_blocks(groups, test_groups):
    """Maximal runs of ADJACENT test groups (e.g. (2, 3) -> one block) as (first row, last row) index pairs; rows are
    time-sorted and groups contiguous."""
    tg = sorted(set(int(x) for x in test_groups))
    runs, cur = [], [tg[0]]
    for g in tg[1:]:
        if g == cur[-1] + 1:
            cur.append(g)
        else:
            runs.append(cur); cur = [g]
    runs.append(cur)
    groups = np.asarray(groups)
    out = []
    for r in runs:
        idx = np.flatnonzero((groups >= r[0]) & (groups <= r[-1]))
        out.append((int(idx[0]), int(idx[-1])))
    return out


def _ns(x):
    return pd.DatetimeIndex(x).as_unit("ns").asi8


def cpcv_train_mask(t, t_end, groups, test_groups, purge=pd.Timedelta(0), embargo_frac=0.01, embargo_sessions=0,
                    sessions=None):
    """Training rows of one CPCV split (boolean array):
       * not in a test group;
       * PURGED: for every test block [a, b] (rows), with window W = [t_a - purge, max t_end over a..b], a row is
         dropped when its own [t, t_end] overlaps W, i.e. t <= max_end and t_end > t_a - purge (its label is not
         known `purge` before the block starts, or it starts before the block's last label ends);
       * EMBARGOED: after every test block, the next ceil(embargo_frac * T) rows (b+1 ...) and the rows of the first
         `embargo_sessions` sessions after the block's last session are dropped.
    t must be sorted. sessions = per-row session labels (default t + 6 h normalized)."""
    tt, te = _ns(t), _ns(t_end)
    n = len(tt)
    groups = np.asarray(groups)
    if np.any(np.diff(tt) < 0):
        raise ValueError("rows must be sorted by t")
    ok = ~np.isin(groups, list(test_groups))
    h = int(math.ceil(embargo_frac * n)) if embargo_frac else 0
    sess = None
    if embargo_sessions:
        sess = np.asarray(pd.factorize(np.asarray(sessions if sessions is not None else
                                                   (pd.DatetimeIndex(t) + pd.Timedelta(hours=6)).normalize()))[0])
    pg = pd.Timedelta(purge).value
    for a, b in test_blocks(groups, test_groups):
        t0 = tt[a] - pg
        t1 = te[a:b + 1].max()
        ok &= ~((tt <= t1) & (te > t0))
        if h:
            ok[b + 1:b + 1 + h] = False
        if embargo_sessions and b + 1 < n:
            last = sess[b]
            later = np.flatnonzero(sess[b + 1:] != last) + b + 1     # rows of later sessions (sorted -> increasing)
            if len(later):
                codes_after = sess[later]
                uniq = pd.unique(codes_after)[:embargo_sessions]
                ok[later[np.isin(codes_after, uniq)]] = False
    return ok


# ============================================================================================ CPCV: run
@dataclass
class CPCVResult:
    splits: pd.DataFrame            # one row per split: test groups, n_train, n_test, threshold, fit info, test $
    groups: np.ndarray              # group id per row
    P: np.ndarray                   # (n_paths, n_groups) split index per path and group
    p: np.ndarray                   # (n_paths, n_rows) float32 out-of-sample probability of each row on each path
    take: np.ndarray                # (n_paths, n_rows) bool: p >= the threshold of the split that predicted it
    n_groups: int
    k: int
    info: dict = field(default_factory=dict)


def run_cpcv(X, y, pnl, t, t_end, fit, n_groups=8, k=2, sessions=None, purge=pd.Timedelta(0), embargo_frac=0.01,
             embargo_sessions=0, verbose=False):
    """CPCV of one model. `fit(train_idx)` -> (predict, threshold, info dict) or (None, None, reason): it may use
    ONLY the rows train_idx (the model, its hyper-parameters and its decision threshold are chosen there).
    For each of the C(N, k) splits: training rows = cpcv_train_mask, the test rows (k groups) are predicted;
    take = p >= threshold. Paths are assembled with path_matrix. A failed split raises (every path needs it)."""
    X = np.asarray(X)
    y = np.asarray(y)
    pnl = np.asarray(pnl, np.float64)
    groups = make_groups(t, n_groups, sessions)
    splits = split_combinations(n_groups, k)
    P = path_matrix(n_groups, splits)
    n = len(y)
    pred = {}                                                        # (split, group) -> (p, thr)
    takes_test_start = "test_start" in inspect.signature(fit).parameters
    rows = []
    for s, comb in enumerate(splits):
        tr_mask = cpcv_train_mask(t, t_end, groups, comb, purge, embargo_frac, embargo_sessions, sessions)
        tr = np.flatnonzero(tr_mask)
        te_idx = np.flatnonzero(np.isin(groups, comb))
        if takes_test_start:                                         # lets the fitter tune before the test
            predict, thr, info = fit(tr, test_start=np.min(np.asarray(t)[te_idx]))
        else:
            predict, thr, info = fit(tr)
        if predict is None:
            raise RuntimeError(f"split {s} {comb}: fit failed ({info})")
        p = np.asarray(predict(X[te_idx]), np.float64)
        take = p >= thr
        for g in comb:
            sel = groups[te_idx] == g
            pred[(s, g)] = (p[sel], thr)
        pt = pnl[te_idx]
        r = dict(split=s, test_groups="+".join(map(str, comb)), n_train=len(tr), n_purged_embargoed=
                 int(n - len(te_idx) - len(tr)), n_test=len(te_idx), threshold=float(thr), n_kept=int(take.sum()),
                 usd_per_trade=float(pt[take].mean()) if take.any() else np.nan, total_usd=float(pt[take].sum()),
                 all_usd_per_trade=float(pt.mean()))
        r.update({k_: v for k_, v in (info or {}).items() if np.isscalar(v)})
        rows.append(r)
        if verbose:
            print(f"  split {s:2d} test {comb}: n_train={len(tr)} n_test={len(te_idx)} thr={thr:.4f} "
                  f"kept={int(take.sum())} $/tr={r['usd_per_trade']:.2f}", flush=True)
    n_p = P.shape[0]
    p_all = np.full((n_p, n), np.nan, np.float32)
    take_all = np.zeros((n_p, n), bool)
    for j in range(n_p):
        for g in range(n_groups):
            pg, thr = pred[(int(P[j, g]), g)]
            idx = np.flatnonzero(groups == g)
            p_all[j, idx] = pg
            take_all[j, idx] = pg >= thr
    return CPCVResult(pd.DataFrame(rows), groups, P, p_all, take_all, n_groups, k,
                      dict(purge=str(purge), embargo_frac=embargo_frac, embargo_sessions=embargo_sessions))


def wf_fitter(model, X, y, w, pnl, year, t_end, kind="entry", min_keep=0.05, C_grid=None, gbm_params=None,
              vote_idx=None, purge=None, min_inner=200):
    """`fit` for run_cpcv using the walk-forward's own procedure (walkforward._fit_and_threshold): inner validation
    = the last 2 calendar years present in the training rows (logit/vote) or the last one (gbm, also its isotonic
    calibration), inner training = earlier training rows purged against the validation start; logit C by validation
    log loss; threshold = max mean net $ per trade with >= min_keep kept, on the validation predictions; final model
    refitted on all training rows (logit/vote; gbm keeps the inner trees + isotonic, as in walkforward)."""
    import walkforward as wf                                         # noqa: PLC0415
    C_grid = wf.C_GRID if C_grid is None else C_grid
    gbm_params = dict(wf.GBM_PARAMS if gbm_params is None else gbm_params)
    purge = wf.PURGE if purge is None else purge
    te = pd.DatetimeIndex(t_end).as_unit("ns").to_numpy() if not isinstance(t_end, np.ndarray) else t_end
    codes = np.arange(len(y))

    def fit(tr, test_start=None):
        # Pick C and the threshold on validation years BEFORE the tested period when the training rows that end
        # before it allow an inner split; otherwise (tests at the start of the data) fall back to the last training
        # years, which come AFTER the test, and flag the split (val_after_test = 1). Without this, 21 of 28 splits
        # chose C / threshold on 2024-2025 while testing 2010-2023 (review finding cpcv-1).
        args = (kind, codes, min_keep, C_grid, gbm_params, vote_idx or [], purge, min_inner)
        m = None
        if test_start is not None:
            ts = pd.Timestamp(test_start).to_datetime64()
            pre = tr[te[tr] <= ts - pd.Timedelta(purge).to_timedelta64()]
            if len(pre):
                m, thr, info = wf._fit_and_threshold(model, X, y, w, pnl, year, te, pre, *args)
                sel, after = pre, 0
        if m is None:
            m, thr, info = wf._fit_and_threshold(model, X, y, w, pnl, year, te, tr, *args)
            sel, after = tr, 1
        if m is None:
            return None, None, info
        info = dict(info)
        if sel is not tr and model in ("logit", "vote"):
            # final model refitted on ALL training rows with the C chosen before the test (walk-forward design)
            m = (wf.LogitModel(info["C"]) if model == "logit" else wf.VoteModel(vote_idx or [], kind)
                 ).fit(X[tr], y[tr], wf._norm(w[tr]))
        info["val_years"] = f"{int(year[sel].max()) - (0 if model == 'gbm' else 1)}-{int(year[sel].max())}"
        info["val_after_test"] = after
        return m.predict, thr, info
    return fit


# ============================================================================================ path evaluation
def daily_series(take, pnl, sessions, all_sessions):
    """$ per session of the taken rows, on the full session calendar all_sessions (0 on days with no trade)."""
    s = pd.Series(np.where(take, pnl, 0.0)).groupby(np.asarray(sessions)).sum()
    return s.reindex(all_sessions, fill_value=0.0).to_numpy(np.float64)


def path_stats(res, pnl, sessions, years_span, all_sessions=None):
    """One row per path: n trades, $ per trade, total $, $ per year (total / years_span), hit rate, daily Sharpe
    (per session, non-annualized, 0 on no-trade sessions) and its annualized value (x sqrt(252))."""
    pnl = np.asarray(pnl, np.float64)
    sessions = np.asarray(sessions)
    all_sessions = np.unique(sessions) if all_sessions is None else all_sessions
    rows = []
    for j in range(res.take.shape[0]):
        tk = res.take[j]
        x = pnl[tk]
        dly = daily_series(tk, pnl, sessions, all_sessions)
        sr = sharpe(dly)
        rows.append(dict(path=j, n_trades=int(tk.sum()), usd_per_trade=float(x.mean()) if len(x) else np.nan,
                         total_usd=float(x.sum()), usd_per_year=float(x.sum()) / years_span,
                         hit_rate=float((x > 0).mean()) if len(x) else np.nan, daily_sharpe=sr,
                         sharpe_ann=sr * math.sqrt(252)))
    return pd.DataFrame(rows)


def path_by_year(res, pnl, year):
    """Long table: path, year, n trades, total $, $ per trade."""
    pnl = np.asarray(pnl, np.float64)
    year = np.asarray(year)
    out = []
    for j in range(res.take.shape[0]):
        tk = res.take[j]
        df = pd.DataFrame({"year": year[tk], "pnl": pnl[tk]}).groupby("year")["pnl"].agg(["size", "sum"])
        df = df.reindex(np.unique(year), fill_value=0)
        for yy, r in df.iterrows():
            out.append(dict(path=j, year=int(yy), n_trades=int(r["size"]), total_usd=float(r["sum"]),
                            usd_per_trade=float(r["sum"]) / r["size"] if r["size"] else np.nan))
    return pd.DataFrame(out)


def random_skip_paths(pnl, n_takes, n_draws=200, seed=0):
    """Random-skip baseline: for each trade count in n_takes, $ per trade of n_draws random subsets (without
    replacement) of all rows. Returns (n_paths, n_draws) array of $ per trade. Memory-light (one draw at a time)."""
    rng = np.random.default_rng(seed)
    pnl = np.asarray(pnl, np.float64)
    out = np.full((len(n_takes), n_draws), np.nan)
    for i, m in enumerate(n_takes):
        if m <= 0:
            continue
        for d in range(n_draws):
            out[i, d] = pnl[rng.choice(len(pnl), int(m), replace=False)].mean()
    return out


# ============================================================================================ deflated Sharpe ratio
def sharpe(x):
    """Non-annualized Sharpe ratio mean / std (ddof=1) of a return series; NaN if std is 0 or < 2 values."""
    x = np.asarray(x, np.float64)
    x = x[np.isfinite(x)]
    if len(x) < 2:
        return np.nan
    sd = x.std(ddof=1)
    return float(x.mean() / sd) if sd > 0 else np.nan


def moments(x):
    """(skewness, kurtosis) of x, population moments; kurtosis is NOT excess (Normal = 3), as in [DSR]."""
    x = np.asarray(x, np.float64)
    x = x[np.isfinite(x)]
    m = x.mean()
    s2 = ((x - m) ** 2).mean()
    if s2 <= 0:
        return 0.0, 3.0
    return float(((x - m) ** 3).mean() / s2 ** 1.5), float(((x - m) ** 4).mean() / s2 ** 2)


def expected_max_sharpe(n_trials, var_sr):
    """SR0 of [DSR] eq. (2): expected maximum of n_trials zero-skill SR estimates with cross-trial variance var_sr,
    sqrt(V) * ((1 - gamma) Z^-1[1 - 1/N] + gamma Z^-1[1 - 1/(N e)]). 0 for N <= 1."""
    if n_trials <= 1:
        return 0.0
    N = float(n_trials)
    return math.sqrt(var_sr) * ((1 - EULER_GAMMA) * norm.ppf(1 - 1 / N) + EULER_GAMMA * norm.ppf(1 - 1 / (N * math.e)))


def psr(sr, sr0, T, skew=0.0, kurt=3.0):
    """Probabilistic Sharpe ratio Z[(SR^ - SR0) sqrt(T-1) / sqrt(1 - g3 SR^ + (g4-1)/4 SR^2)] (non-annualized SRs,
    g4 = kurtosis, not excess) [DSR eq. 2]."""
    den = 1 - skew * sr + (kurt - 1) / 4 * sr ** 2
    if not np.isfinite(sr) or den <= 0:
        return np.nan
    return float(norm.cdf((sr - sr0) * math.sqrt(T - 1) / math.sqrt(den)))


def deflated_sharpe(returns, n_trials, var_sr):
    """DSR of a return series (e.g. daily $) given the number of independent trials and the variance of the trials'
    (non-annualized, same-frequency) Sharpe estimates [DSR]. Returns a dict with sr, sr_ann (x sqrt 252), T, skew,
    kurt, sr0, sr0_ann, psr0 (PSR against 0), dsr."""
    x = np.asarray(returns, np.float64)
    x = x[np.isfinite(x)]
    sr = sharpe(x)
    g3, g4 = moments(x)
    sr0 = expected_max_sharpe(n_trials, var_sr)
    T = len(x)
    return dict(sr=sr, sr_ann=sr * math.sqrt(252), T=T, skew=g3, kurt=g4, n_trials=n_trials, var_sr=var_sr,
                sr0=sr0, sr0_ann=sr0 * math.sqrt(252), psr0=psr(sr, 0.0, T, g3, g4), dsr=psr(sr, sr0, T, g3, g4))


# ============================================================================================ PBO by CSCV
def _perf(M, metric):
    if metric == "mean":
        return M.mean(axis=0)
    if metric == "sum":
        return M.sum(axis=0)
    if metric == "sharpe":
        sd = M.std(axis=0, ddof=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, M.mean(axis=0) / sd, 0.0)
    return np.apply_along_axis(metric, 0, M)


def pbo_cscv(M, S=16, metric="mean", max_combos=None, seed=0):
    """Probability of backtest overfitting by CSCV [PBO, Algorithm 2.3].
    M: (T, N) array, row t = a synchronous period, column n = one configuration's performance (e.g. $ that period).
    S: even number of row blocks (np.array_split: blocks differ by at most one row when S does not divide T).
    metric: 'mean' (= total $ per row), 'sum', 'sharpe' or a callable on a column.
    For every combination c of S/2 blocks: J = those blocks (IS), J-bar = the others (OOS, original order); n* =
    argmax IS performance (first on ties); omega = rank of n*'s OOS performance among the N (average ranks for
    ties, 1 = worst) / (N + 1); lambda = ln(omega / (1 - omega)). PBO = mean(lambda <= 0).
    max_combos: if C(S, S/2) is larger, a random subset of that many combinations is used.
    Returns dict(pbo, n_combos, logits, is_perf, oos_perf (of n*), prob_loss = mean(oos_perf < 0), degradation
    slope of oos on is, chosen = counts of n*)."""
    M = np.asarray(M, np.float64)
    T, N = M.shape
    if S % 2 or S < 2 or S > T:
        raise ValueError("S must be even and <= T")
    blocks = np.array_split(np.arange(T), S)
    combos = list(itertools.combinations(range(S), S // 2))
    if max_combos and len(combos) > max_combos:
        rng = np.random.default_rng(seed)
        combos = [combos[i] for i in sorted(rng.choice(len(combos), max_combos, replace=False))]
    logits, is_p, oos_p, chosen = [], [], [], []
    for c in combos:
        cs = set(c)
        J = np.concatenate([blocks[s] for s in range(S) if s in cs])
        Jb = np.concatenate([blocks[s] for s in range(S) if s not in cs])
        r_is = _perf(M[J], metric)
        r_oos = _perf(M[Jb], metric)
        n_star = int(np.argmax(r_is))
        rk = rankdata(r_oos)[n_star]
        w = rk / (N + 1)
        logits.append(math.log(w / (1 - w)))
        is_p.append(r_is[n_star]); oos_p.append(r_oos[n_star]); chosen.append(n_star)
    logits, is_p, oos_p = map(np.asarray, (logits, is_p, oos_p))
    slope = float(np.polyfit(is_p, oos_p, 1)[0]) if np.ptp(is_p) > 0 else np.nan
    return dict(pbo=float(np.mean(logits <= 0)), n_combos=len(combos), logits=logits, is_perf=is_p, oos_perf=oos_p,
                prob_loss=float(np.mean(oos_p < 0)), degradation_slope=slope,
                chosen=np.bincount(np.asarray(chosen), minlength=N))
