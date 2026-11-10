"""v3 significance toolkit (numpy/scipy only). All tests work on DAILY net $ per micro on a common session calendar.

Conventions
- x / D: daily P&L (or daily P&L MINUS a matched control), shape (T,) or (T, K) for K strategies, 0 on no-trade days.
  One row = one Globex session (18:00 -> 16:45 ET); sessions from 2025-06-30 18:00 ET on (holdout) must never be passed.
- Positive = strategy beats the benchmark. Null hypothesis for every test: true mean <= 0 (one-sided).
- Bootstrap = stationary bootstrap (Politis & Romano 1994): blocks of geometric length with mean `mean_block` days,
  wrapped circularly; the SAME resampled day indices are used for every column, so cross-strategy correlation is kept.

Sources: Politis & Romano (1994); Politis & White (2004) + Patton, Politis & White (2009) block length;
White (2000) Reality Check; Hansen (2005) SPA; Romano & Wolf (2005, 2016) StepM; Holm (1979);
Benjamini & Hochberg (1995), Benjamini & Yekutieli (2001); Bailey & Lopez de Prado (2012) PSR / MinTRL and (2014) DSR;
Harvey, Liu & Zhu (2016); Newey & West (1987/1994); Li & Ji (2005) effective number of tests.
"""
import math

import numpy as np
from scipy.stats import norm, chi2

EULER_GAMMA = 0.5772156649015329


# ----------------------------------------------------------------------------------------------- basics
def _2d(D):
    D = np.asarray(D, np.float64)
    return D[:, None] if D.ndim == 1 else D


def nw_lags(T):
    """Newey-West (1994) automatic lag rule floor(4 (T/100)^(2/9)); about 9 for 15 years of sessions."""
    return int(math.floor(4 * (T / 100.0) ** (2.0 / 9.0)))


def hac_t(x, lags=None):
    """t-stat of the mean with Newey-West (Bartlett) long-run variance. Returns (t, se, iid_se)."""
    x = np.asarray(x, np.float64)
    T = len(x)
    L = nw_lags(T) if lags is None else int(lags)
    e = x - x.mean()
    lrv = e @ e / T
    for k in range(1, L + 1):
        lrv += 2 * (1 - k / (L + 1)) * (e[:-k] @ e[k:]) / T
    se = math.sqrt(max(lrv, 1e-300) / T)
    return x.mean() / se, se, e.std(ddof=1) / math.sqrt(T)


# ----------------------------------------------------------------------------------------------- block length
def politis_white_block(x):
    """Automatic mean block length (Politis & White 2004 with the Patton-Politis-White 2009 correction).
    Returns (b_stationary, b_circular). Near-zero autocorrelation gives ~1: use a floor (see recommend_block)."""
    x = np.asarray(x, np.float64)
    x = x - x.mean()
    n = len(x)
    Kn = max(5, int(math.ceil(math.sqrt(math.log10(n)))))
    mmax = int(math.ceil(math.sqrt(n))) + Kn
    bmax = int(math.ceil(min(3 * math.sqrt(n), n / 3)))
    acov = np.array([x[: n - k] @ x[k:] / n for k in range(mmax + Kn + 1)])
    rho = acov / acov[0]
    thr = 2.0 * math.sqrt(math.log10(n) / n)
    mhat = mmax
    for m in range(0, mmax + 1):
        if np.all(np.abs(rho[m + 1: m + Kn + 1]) < thr):
            mhat = m
            break
    M = min(2 * mhat, mmax)
    if M == 0:
        return 1.0, 1.0
    k = np.arange(1, M + 1)
    s = k / M
    lam = np.where(s <= 0.5, 1.0, 2 * (1 - s))
    G = 2 * np.sum(lam * k * acov[1: M + 1])
    g0 = acov[0] + 2 * np.sum(lam * acov[1: M + 1])
    b_sb = (2 * G ** 2 / (2 * g0 ** 2)) ** (1 / 3) * n ** (1 / 3)
    b_cb = (2 * G ** 2 / ((4 / 3) * g0 ** 2)) ** (1 / 3) * n ** (1 / 3)
    return float(min(max(b_sb, 1.0), bmax)), float(min(max(b_cb, 1.0), bmax))


def recommend_block(D, floor=10, cap=20):
    """Primary block length: max over columns of the Politis-White stationary length of the P&L itself, floored at 10
    sessions (two weeks) and capped at 20. (|P&L| has long memory: its PW length hits the 60+ cap on every series we
    checked, but that is volatility clustering, which barely moves a mean test.) Calibration on v2 series
    (v3/out/stats_calibration_series.csv): daily P&L has lag-1 autocorrelation -0.02..-0.11, so LONGER blocks give
    SMALLER p-values there; hence the final p of the protocol is the MAX over block lengths {1, 5, 10, 20}
    (see conservative_p)."""
    D = _2d(D)
    b = [politis_white_block(D[:, j])[0] for j in range(D.shape[1])]
    return float(min(max(max(b), floor), cap))


def conservative_p(test, *args, blocks=(1, 5, 10, 20), **kw):
    """Run test(*args, mean_block=L, **kw) for each L and return (max p, {L: p}). `test` must return a p-value or
    a dict with 'p_boot' / 'p_c'."""
    ps = {}
    for L in blocks:
        r = test(*args, mean_block=L, **kw)
        ps[L] = r if np.isscalar(r) else r.get("p_boot", r.get("p_c"))
    return max(ps.values()), ps


# ----------------------------------------------------------------------------------------------- bootstrap engine
def stationary_indices(T, mean_block, B, seed=0):
    """(B, T) int32 day indices of the stationary bootstrap: each day starts a new block with prob 1/mean_block,
    otherwise continues the previous block (circular wrap)."""
    rng = np.random.default_rng(seed)
    p = 1.0 / max(float(mean_block), 1.0)
    new = rng.random((B, T)) < p
    new[:, 0] = True
    pos = np.broadcast_to(np.arange(T), (B, T))
    last = np.maximum.accumulate(np.where(new, pos, 0), axis=1)
    starts = rng.integers(0, T, (B, T))
    first = np.take_along_axis(starts, last, axis=1)
    return ((first + pos - last) % T).astype(np.int32)


def boot_means(D, mean_block=10, B=2000, seed=0, chunk=250):
    """(B, K) bootstrap means of every column, all columns resampled on the same day indices.
    Uses resample COUNTS @ D, so memory is chunk*T, not B*T*K."""
    D = _2d(D)
    T, K = D.shape
    out = np.empty((B, K))
    for c0 in range(0, B, chunk):
        nb = min(chunk, B - c0)
        idx = stationary_indices(T, mean_block, nb, seed + c0)
        flat = (np.arange(nb)[:, None] * T + idx).ravel()
        cnt = np.bincount(flat, minlength=nb * T).reshape(nb, T).astype(np.float64)
        out[c0: c0 + nb] = cnt @ D / T
    return out


def boot_pvalue_mean(x, mean_block=10, B=4000, seed=0):
    """One-sided p-value for mean(x) > 0 from the stationary bootstrap (null imposed by recentring),
    p = (1 + #{m*_b - m >= m}) / (1 + B). Also returns the HAC t and a 90% percentile interval for the mean."""
    x = np.asarray(x, np.float64)
    m = x.mean()
    mb = boot_means(x, mean_block, B, seed)[:, 0]
    p = (1 + np.sum(mb - m >= m)) / (1 + B)
    t, se, se_iid = hac_t(x)
    return dict(mean=m, p_boot=float(p), t_hac=t, se_hac=se, se_iid=se_iid, z_boot=float(norm.isf(p)),
                ci90=(float(np.quantile(mb, 0.05)), float(np.quantile(mb, 0.95))), boot_sd=float(mb.std(ddof=1)))


# ----------------------------------------------------------------------------------------------- family tests
def _family_boot(D, mean_block, B, seed):
    D = _2d(D)
    T = D.shape[0]
    m = D.mean(0)
    mb = boot_means(D, mean_block, B, seed)
    om = np.sqrt(T) * (mb - m).std(0, ddof=1)  # omega_k: bootstrap sd of sqrt(T) * mean
    om = np.where(om > 0, om, np.inf)
    return D, T, m, mb, om


def reality_check(D, mean_block=10, B=2000, seed=0):
    """White (2000): p-value that the BEST column beats the benchmark, non-studentized.
    V = max_k sqrt(T) m_k ;  V*_b = max_k sqrt(T)(m*_bk - m_k) ;  p = (1+#{V* >= V})/(1+B)."""
    D, T, m, mb, _ = _family_boot(D, mean_block, B, seed)
    V = np.sqrt(T) * m.max()
    Vs = (np.sqrt(T) * (mb - m)).max(1)
    return float((1 + np.sum(Vs >= V)) / (1 + B))


def spa(D, mean_block=10, B=2000, seed=0):
    """Hansen (2005) Superior Predictive Ability test, studentized. Returns p-values (lower, consistent, upper).
    T_SPA = max(0, max_k sqrt(T) m_k / w_k). Bootstrap stat centred at mu_k:
      upper u: mu=0 (= studentized RC); consistent c: mu=m_k if t_k <= -sqrt(2 ln ln T) else 0; lower l: mu=min(m_k,0).
    Bad columns (clearly negative) are centred at their own negative mean, so junk variants do not dilute the test.
    Use p_c as THE answer."""
    D, T, m, mb, om = _family_boot(D, mean_block, B, seed)
    t = np.sqrt(T) * m / om
    Tspa = max(0.0, float(t.max()))
    thr = math.sqrt(2 * math.log(math.log(T)))
    out = {}
    for name, mu in (("l", np.minimum(m, 0)), ("c", np.where(t <= -thr, m, 0.0)), ("u", np.zeros_like(m))):
        Z = np.sqrt(T) * (mb - m + mu) / om
        Ts = np.maximum(Z.max(1), 0.0)
        out["p_" + name] = float((1 + np.sum(Ts >= Tspa)) / (1 + B)) if Tspa > 0 else 1.0
    out["t_max"] = float(t.max())
    out["best"] = int(t.argmax())
    return out


def stepm(D, mean_block=10, B=2000, seed=0, alpha=0.05):
    """Romano-Wolf StepM (studentized), with the 2016 adjusted p-values: WHICH columns beat the benchmark while
    keeping the chance of ANY false claim <= alpha. Sort t descending; for the j-th largest t,
    p_raw_j = (1+#{max_{l in j..K} t*_bl >= t_j})/(1+B); p_adj_j = max(p_raw_j, p_adj_{j-1})."""
    D, T, m, mb, om = _family_boot(D, mean_block, B, seed)
    t = np.sqrt(T) * m / om
    Z = np.sqrt(T) * (mb - m) / om  # (B, K), null-centred
    order = np.argsort(-t)
    Zs = Z[:, order]
    tail_max = np.maximum.accumulate(Zs[:, ::-1], axis=1)[:, ::-1]  # max over columns j..K-1 (in sorted order)
    p_raw = (1 + np.sum(tail_max >= t[order][None, :], axis=0)) / (1 + B)
    p_adj_sorted = np.maximum.accumulate(p_raw)
    p_adj = np.empty_like(p_adj_sorted)
    p_adj[order] = p_adj_sorted
    return dict(t=t, p_adj=p_adj, reject=p_adj <= alpha)


def holm(p):
    """Holm step-down adjusted p-values (familywise error, any dependence)."""
    p = np.asarray(p, np.float64)
    K = len(p)
    o = np.argsort(p)
    adj = np.minimum(1, np.maximum.accumulate((K - np.arange(K)) * p[o]))
    out = np.empty(K)
    out[o] = adj
    return out


def bh(p, dependent=False):
    """Benjamini-Hochberg FDR adjusted p-values; dependent=True gives Benjamini-Yekutieli (any dependence)."""
    p = np.asarray(p, np.float64)
    K = len(p)
    c = np.sum(1.0 / np.arange(1, K + 1)) if dependent else 1.0
    o = np.argsort(p)
    raw = p[o] * K * c / np.arange(1, K + 1)
    adj = np.minimum(1, np.minimum.accumulate(raw[::-1])[::-1])
    out = np.empty(K)
    out[o] = adj
    return out


def bonferroni_t(K, alpha=0.05, one_sided=True):
    """t (z) needed for familywise alpha over K independent-looking tests."""
    return float(norm.isf(alpha / K / (1 if one_sided else 0.5)))


# ----------------------------------------------------------------------------------------------- Sharpe-based tools
def moments(x):
    x = np.asarray(x, np.float64)
    m = x.mean()
    s2 = ((x - m) ** 2).mean()
    return float(((x - m) ** 3).mean() / s2 ** 1.5), float(((x - m) ** 4).mean() / s2 ** 2)


def expected_max_sr(N, var_sr):
    """E[max of N zero-skill Sharpe estimates] (Bailey & Lopez de Prado 2014), per-day units."""
    if N <= 1:
        return 0.0
    return math.sqrt(var_sr) * ((1 - EULER_GAMMA) * norm.ppf(1 - 1 / N) + EULER_GAMMA * norm.ppf(1 - 1 / (N * math.e)))


def psr(sr, sr0, T, skew=0.0, kurt=3.0):
    den = 1 - skew * sr + (kurt - 1) / 4 * sr ** 2
    return float(norm.cdf((sr - sr0) * math.sqrt(T - 1) / math.sqrt(den)))


def dsr(x, N_eff, var_sr=None):
    """Deflated Sharpe ratio of daily series x after N_eff effective trials. var_sr defaults to the null sampling
    variance 1/(T-1) (trials that differ only by noise); pass the cross-trial variance when it is larger."""
    x = np.asarray(x, np.float64)
    T = len(x)
    sr = x.mean() / x.std(ddof=1)
    g3, g4 = moments(x)
    v = 1.0 / (T - 1) if var_sr is None else var_sr
    sr0 = expected_max_sr(N_eff, v)
    return dict(sr=sr, sr_ann=sr * math.sqrt(252), sr0=sr0, sr0_ann=sr0 * math.sqrt(252), psr0=psr(sr, 0, T, g3, g4),
                dsr=psr(sr, sr0, T, g3, g4), skew=g3, kurt=g4, T=T)


def dsr_t_bar(N_eff, conf=0.95):
    """With var_sr = 1/(T-1) and ~normal days, DSR >= conf  <=>  t >= E[max z of N_eff] + z_conf. Handy threshold."""
    return expected_max_sr(N_eff, 1.0) + norm.ppf(conf)


def min_trl(sr, sr_star=0.0, skew=0.0, kurt=3.0, conf=0.95):
    """Minimum track record length in DAYS (Bailey & Lopez de Prado 2012), per-day SRs, raw kurtosis."""
    if sr <= sr_star:
        return np.inf
    return 1 + (1 - skew * sr + (kurt - 1) / 4 * sr ** 2) * (norm.ppf(conf) / (sr - sr_star)) ** 2


def days_needed(sr_ann, t_bar=3.0, power=0.5, vif=1.0):
    """Sessions needed so that a strategy with TRUE annualized Sharpe sr_ann reaches t >= t_bar with the given
    probability (power 0.5 = on average). T = vif * ((t_bar + z_power) / SR_day)^2, SR_day = sr_ann / sqrt(252).
    vif = long-run variance / variance (HAC inflation) of the daily series."""
    sr_d = sr_ann / math.sqrt(252)
    return vif * ((t_bar + norm.ppf(power)) / sr_d) ** 2


def trades_needed(edge_usd, sd_usd, t_bar=3.0, power=0.5):
    """Independent trades needed for a per-trade edge of edge_usd with per-trade sd sd_usd to reach t >= t_bar."""
    return ((t_bar + norm.ppf(power)) * sd_usd / edge_usd) ** 2


def effective_n(corr):
    """Effective number of independent trials from a K x K correlation matrix of daily P&L columns.
    Returns (rho_bar formula rho + (1-rho) K, Li & Ji 2005 eigenvalue count)."""
    C = np.asarray(corr, np.float64)
    K = C.shape[0]
    rho = (C.sum() - K) / (K * (K - 1)) if K > 1 else 0.0
    lam = np.abs(np.linalg.eigvalsh(C))
    liji = float(np.sum((lam >= 1) + (lam - np.floor(lam))))
    return float(rho + (1 - rho) * K), liji


def haircut_sharpe(sr_ann, t, p_adj):
    """Harvey & Liu (2015): Sharpe after the multiple-testing adjustment, sr * t_adj / t (two-sided p_adj)."""
    t_adj = norm.isf(p_adj / 2)
    return sr_ann * t_adj / t if t > 0 else 0.0


# ----------------------------------------------------------------------------------------------- combining edges
def stouffer(z, w=None):
    """Weighted Stouffer Z for INDEPENDENT tests: sum w z / sqrt(sum w^2). Use w = sqrt(n_days) or equal.
    Correlated components: do NOT use; test the summed daily P&L series instead (portfolio_test)."""
    z = np.asarray(z, np.float64)
    w = np.ones_like(z) if w is None else np.asarray(w, np.float64)
    return float(np.sum(w * z) / math.sqrt(np.sum(w ** 2)))


def fisher(p):
    """Fisher's combined p for independent p-values: -2 sum ln p ~ chi2(2K)."""
    p = np.asarray(p, np.float64)
    return float(chi2.sf(-2 * np.sum(np.log(p)), 2 * len(p)))


def portfolio_test(D, w=None, mean_block=10, B=4000, seed=0):
    """ONE test of a pre-specified portfolio: daily P&L = D @ w (weights fixed BEFORE looking; e.g. equal risk
    from pre-2018 vol). Correlation between components is handled automatically because the sum is tested."""
    D = _2d(D)
    w = np.ones(D.shape[1]) / D.shape[1] if w is None else np.asarray(w, np.float64)
    return boot_pvalue_mean(D @ w, mean_block, B, seed)


def pipeline_null(D, pipeline, mean_block=10, B=1000, seed=0):
    """Honest test of a portfolio whose components/weights were CHOSEN FROM THE DATA: rerun the whole selection
    `pipeline(D) -> scalar statistic` on null bootstrap samples (every column recentred to mean 0, same day indices
    for all columns). p = (1 + #{stat* >= stat_real}) / (1 + B). Generalizes White's Reality Check."""
    D = _2d(D)
    T = D.shape[0]
    real = pipeline(D)
    D0 = D - D.mean(0)
    stats = np.empty(B)
    for c0 in range(0, B, 100):
        nb = min(100, B - c0)
        idx = stationary_indices(T, mean_block, nb, seed + c0)
        for j in range(nb):
            stats[c0 + j] = pipeline(D0[idx[j]])
    return dict(stat=real, p=float((1 + np.sum(stats >= real)) / (1 + B)), null_q95=float(np.quantile(stats, 0.95)))


def mc_rank_p(real, null_draws):
    """Empirical p from matched random controls (each draw = one full random strategy run):
    (1 + #{null >= real}) / (1 + R). R = 999 gives a floor p = 0.001 (z 3.09)."""
    null_draws = np.asarray(null_draws, np.float64)
    return float((1 + np.sum(null_draws >= real)) / (1 + len(null_draws)))


# ----------------------------------------------------------------------------------------------- round protocol helpers
def robust_report(x, sessions, n_best=10, winsor=0.01):
    """The splits every v3 result must report, from a daily series x on session dates `sessions` (datetime64[D]).
    Returns dict: whole-sample mean/t_hac, by-year means, halves 2010-17 / 2018-25H1, 2018+, 2022+, without the
    n_best best days, winsorized-mean t (tails clipped at the winsor/1-winsor quantiles), share of positive years."""
    x = np.asarray(x, np.float64)
    s = np.asarray(sessions, "datetime64[D]")
    assert s.max() < np.datetime64("2025-06-30"), "holdout sessions passed in"
    yr = s.astype("datetime64[Y]").astype(int) + 1970

    def tt(v):
        return (float(v.mean()), float(hac_t(v)[0])) if len(v) > 20 and v.std() > 0 else (float("nan"),) * 2
    out = dict(all=tt(x))
    out["by_year"] = {int(y): float(x[yr == y].sum()) for y in np.unique(yr)}
    out["2010_17"] = tt(x[yr <= 2017])
    out["2018_25H1"] = tt(x[yr >= 2018])
    out["2022+"] = tt(x[yr >= 2022])
    keep = np.ones(len(x), bool)
    keep[np.argsort(-x)[:n_best]] = False
    out["drop_best"] = tt(np.where(keep, x, 0.0))
    lo, hi = np.quantile(x[x != 0], [winsor, 1 - winsor]) if np.any(x != 0) else (0, 0)
    out["winsor"] = tt(np.clip(x, lo, hi))
    yrs = np.array(list(out["by_year"].values()))
    out["share_years_pos"] = float(np.mean(yrs > 0))
    return out


def round_verdict(z_primary, tier, holm_or_stepm_p, rep, mc_p=None, dsr_val=None, gross_over_cost=None,
                  alpha_A=0.03, alpha_B_family=0.004):
    """Apply the v3 acceptance gates (see protocol). tier 'A' = pre-registered (Holm p from the Tier-A list),
    'B' = mined (StepM adjusted p within its family). Returns (label, list of failed gates)."""
    fails = []
    if tier == "A":
        if holm_or_stepm_p > alpha_A:
            fails.append(f"Holm p {holm_or_stepm_p:.3f} > {alpha_A}")
    else:
        if holm_or_stepm_p > alpha_B_family:
            fails.append(f"StepM p {holm_or_stepm_p:.4f} > {alpha_B_family}")
        if z_primary < 3.0:
            fails.append(f"t {z_primary:.2f} < 3")
        if dsr_val is not None and dsr_val < 0.95:
            fails.append(f"DSR {dsr_val:.2f} < 0.95")
    for k in ("2010_17", "2018_25H1", "drop_best", "winsor"):
        if not rep[k][0] > 0:
            fails.append(f"{k} mean <= 0")
    if rep["share_years_pos"] < 0.6:
        fails.append(f"only {rep['share_years_pos']:.0%} years positive")
    if mc_p is not None and mc_p > 0.05:
        fails.append(f"matched random control p {mc_p:.3f} > 0.05")
    if gross_over_cost is not None and gross_over_cost < 1.5:
        fails.append(f"gross edge {gross_over_cost:.2f}x cost < 1.5x")
    label = "SIGNIFICANT (send to holdout/forward test)" if not fails else (
        "PROMISING (forward test only)" if len(fails) <= 2 and z_primary >= 2 else "NOT SIGNIFICANT")
    return label, fails


# ----------------------------------------------------------------------------------------------- pre-registration
PREREG_CHECKLIST = """Before running anything (write it, hash it with prereg_record, then run):
 1 id, family (F1 drift/time-of-day, F2 event days, F3 intraday momentum/breakout, F4 pullback/patterns/ML,
   F5 cross-market/relative value, F6 sizing/eval mechanics), tier A (exact literature/earlier spec, no tuning) or B (mined).
 2 economic reason in one sentence, the source paper/earlier file, and the expected SIGN and rough size ($/micro/trade).
 3 exact rules: market(s) (MES first-class), bar size, entry time/condition, side, stop, exit, flat by 16:45,
   max trades/session, one position at a time; costs ($1 + 1 tick each way + 1 tick on stops).
 4 the FULL list of variants that will be run (each = one trial) and which one is primary.
 5 data window (2010-07..2025-06-27; YM 2018+; for literature ideas also the post-publication window), no holdout.
 6 primary statistic: mean daily net $ per micro MINUS the matched control (random entries same time/side/exit,
   >= 20 draws averaged per day), one-sided; plus the raw daily net $.
 7 test: stationary bootstrap, p = max over blocks {1,5,10,20}, B >= 5000; Tier A: Holm over the Tier-A list;
   Tier B: StepM within the family + t >= 3 + DSR >= 0.95.
 8 robustness gates: both halves > 0, >= 60% of years > 0 (2-year blocks for events), > 0 without the 10 best days,
   winsorized mean > 0, matched random control rank p <= 0.05 (R >= 999), gross edge >= 1.5x cost.
 9 eval relevance: pass-within-10/20-days vs matched luck (R >= 200 draws), reported, not used as significance.
10 what result would make us DROP the idea (kill criterion), and the no-look-ahead check that will be run.
"""


def prereg_record(exp_id, spec: dict, out_dir="v3/out/prereg"):
    """Freeze a pre-registration: writes <out_dir>/<exp_id>.json with the spec, a UTC timestamp and its sha256.
    Refuses to overwrite (a changed spec is a new id = a new trial)."""
    import hashlib, json, os, datetime
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, f"{exp_id}.json")
    if os.path.exists(p):
        raise FileExistsError(f"{p} exists: a changed spec needs a new id (and counts as a new trial)")
    body = json.dumps(spec, sort_keys=True, default=str)
    rec = dict(id=exp_id, utc=datetime.datetime.utcnow().isoformat(timespec="seconds"), spec=spec,
               sha256=hashlib.sha256(body.encode()).hexdigest())
    with open(p, "w") as f:
        json.dump(rec, f, indent=1, default=str)
    return rec["sha256"]
