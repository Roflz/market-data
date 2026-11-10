"""
STATISTICALLY DERIVED confidence weights (family "stat"): every signal's weight is estimated from the TRAINING rows by
a published statistical method. Ten scorers are registered (see stat_NOTES.md for the full source trail):

  A. Hassanniakalager, Sermpinis & Stasinakis (2021), "Trading the foreign exchange market with technical analysis
     and Bayesian statistics", Journal of Empirical Finance 63, 230-251 (eprint https://eprints.gla.ac.uk/246954/,
     thesis ch. 2 https://theses.gla.ac.uk/30934/). Their pipeline, replicated on our signals:
       1. a universe of simple rules (their 7,846 technical rules -> our "rule = one feature condition", built from
          every X column: each value of a {-1,0,1}/{0,1} flag, and > / <= each training quintile cut of a continuous
          column, both directions);
       2. a data-snooping screen: the Romano, Shaikh & Wolf (2008) k-FWER StepM test (one-sided, studentized
          statistic of the mean excess return, paper eq. 1-3) "combined with the balancing procedure of Romano and
          Wolf (2010)" (Annals of Statistics 38, 598-633: prepivoted critical values, eq. 5.1, streamlined stepdown
          Algorithm 4.2), k = 0.5% of the number of rules (paper sec. 2.1 and footnote 5: 39 of 7,846), on the
          per-session-day excess net $ of each rule over a random skip of the same activity; circular block
          bootstrap with natural-variance studentization (Romano & Wolf 2005, their empirical application), block by
          Politis & White (2004); alpha = 0.10 and B = max(1000, 20 x rules) are labelled fallbacks;
       3. combination of the survivors by the paper's five Bayesian combiners plus its naive benchmark:
            stat_screen_nb   Naive Bayes (paper sec. 2.5), best N survivors by in-sample accuracy (N = 15)
            stat_screen_rvm  Relevance Vector Machine (Tipping 2001; paper sec. 2.2, eq. 4-18), ALL survivors
            stat_screen_dma  Dynamic Model Averaging (Raftery, Karny & Ettler 2010; paper sec. 2.3, eq. 19-24)
            stat_screen_dms  Dynamic Model Selection (same recursion, highest-probability model)
            stat_screen_bma  conventional Bayesian Model Averaging = DMA with delta = lambda = 1 (paper sec. 2.3)
            stat_screen_bnn  Bayesian-regularised neural network (MacKay 1992; Foresee & Hagan 1997; Ticknor 2013;
                             paper sec. 2.4, eq. 25-26)
            stat_screen_sa   Simple Average of the best N rules (the paper's naive benchmark, sec. 4.2)
  B. stat_nb_woe        naive Bayes / weight-of-evidence sum (Good 1950; Spiegelhalter & Knill-Jones 1984):
                        WoE = ln(P(bin | y=1) / P(bin | y=0)) with Laplace add-one smoothing; raw score = prior
                        log-odds + sum of WoE.
  C. stat_woe_scorecard credit-risk scorecard (Siddiqi 2006, Credit Risk Scorecards, Wiley; Anderson 2007, The Credit
                        Scoring Toolkit): fine classing -> monotone coarse classing -> WoE per bin -> Information
                        Value filter IV >= 0.02 (Siddiqi's "unpredictive" cut, quoted by du Pisanie, Allison &
                        Visagie 2023, arXiv 2303.01227) -> logistic regression on WoE codes -> points, PDO = 20.
  D. stat_shrink_combo  forecast combination with shrinkage toward equal weights (Diebold & Pauly 1990, IJF 6:
                        posterior-mean weights beta0 + delta (beta_OLS - beta0), beta0 = equal weights, as restated by
                        Diebold & Shin 2019 IJF 35; Smith & Wallis 2009; Claeskens et al. 2016): one logistic forecast
                        per signal family, logistic combination weights shrunk toward 1/K, delta chosen on an inner
                        purged time split of the training rows.

Interface (scorer_api.Scorer): fit(X, y, w, meta) uses ONLY the rows it is given; score(X) returns LOG-ODDS (the
method's raw output passed through the monotone Platt map a*raw + b fitted on the training rows, so for every linear
method score = intercept + sum(weight x indicator) exactly as listed in weights_table); raw_score(X) gives the method's
own raw output (e.g. prior + sum WoE for stat_nb_woe, the DMA linear-probability forecast for stat_screen_dma);
predict_proba(X) = sigmoid(score). weights_table() columns: signal, weight (log-odds), points (= weight / (ln 2 / 20)),
meaning, source. task="exit": identical machinery on the exit rows (y = exit beats hold, payoff = exit_gain_usd), so a
high score = evidence against the open trade.

Adaptations (daily FX -> intraday futures candidates) and every fallback number are labelled where they are used and
listed in stat_NOTES.md. Nothing here reads data outside (X, y, w, meta).
"""
from __future__ import annotations

import hashlib
import math
import re

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import rankdata
from sklearn.linear_model import LogisticRegression

from scorer_api import Scorer, register

LN2_20 = math.log(2.0) / 20.0             # scorer_api / Siddiqi scaling: +20 points doubles the odds (PDO = 20)
EXIT_STATE = ("open_R", "mfe_R", "mae_R", "bars_held", "dist_stop_R", "mins_to_1645")

SRC_HSS = ("Hassanniakalager, Sermpinis & Stasinakis (2021) J. Empirical Finance 63:230-251 (eprint 246954; thesis "
           "ch. 2); screen = Romano, Shaikh & Wolf (2008) k-StepM + Romano & Wolf (2010) balancing")


# ===================================================================================================== small helpers
def _col(X: pd.DataFrame, c: str) -> np.ndarray:
    if c not in X.columns:
        return np.full(len(X), np.nan)
    return X[c].to_numpy(dtype=float, na_value=np.nan)


def _weights(w, n):
    """Sample weights normalised to mean 1 (None -> ones). Non-finite / negative -> 0."""
    if w is None:
        return np.ones(n)
    w = np.asarray(w, float).copy()
    w[~np.isfinite(w) | (w < 0)] = 0.0
    m = w.mean()
    return w / m if m > 0 else np.ones(n)


def _wmean(x, w):
    sw = w.sum()
    return float((x * w).sum() / sw) if sw > 0 else float(np.mean(x))


def _logit(p):
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return np.log(p / (1 - p))


def _platt_ab(s, y, w):
    """Platt (1999) map P(y=1) = sigmoid(a*s + b) fitted on TRAINING rows; same estimator as scorer_api.platt, but the
    two numbers are kept so score() can be returned in log-odds units. Constant s -> a = 0, b = base log-odds."""
    s = np.asarray(s, float)
    if not np.isfinite(s).all() or np.ptp(s) <= 1e-12 or len(np.unique(y)) < 2:
        return 0.0, float(_logit(_wmean(y, w)))
    sd = s.std()
    m = LogisticRegression(C=1e6, max_iter=1000).fit(((s - s.mean()) / sd).reshape(-1, 1), y, sample_weight=w)
    a = float(m.coef_[0, 0] / sd)
    return a, float(m.intercept_[0] - a * s.mean())


def _payoff(y, meta, task, metric="auto"):
    """Per-row payoff for the data-snooping screen: net $ of the labelled trade (entries: pnl_usd; exits: exit_gain_usd
    = $ from exiting now minus $ from holding) -- the analogue of the paper's per-period rule return after costs.
    Fallback (no $ in meta, or metric="hit"): +1 win / -1 loss."""
    names = ("pnl_usd", "exit_gain_usd") if task == "entry" else ("exit_gain_usd", "pnl_usd")
    if metric in ("auto", "usd") and meta is not None:
        for c in names:
            if c in meta.columns:
                v = pd.to_numeric(meta[c], errors="coerce").to_numpy(float)
                if np.isfinite(v).mean() > 0.5:
                    return np.nan_to_num(v), "usd:" + c
    if metric == "usd":
        raise ValueError("metric='usd' needs pnl_usd / exit_gain_usd in meta")
    return 2.0 * np.asarray(y, float) - 1.0, "hit"


def _time_ns(meta, n):
    if meta is not None and "t" in meta.columns:
        t = pd.to_datetime(meta["t"])
        if getattr(t.dt, "tz", None) is not None:
            t = t.dt.tz_convert("UTC").dt.tz_localize(None)
        return t.to_numpy(dtype="datetime64[ns]").astype(np.int64)
    return np.arange(n, dtype=np.int64)


def _tend_ns(meta, n, t):
    if meta is not None and "t_end" in meta.columns:
        te = pd.to_datetime(meta["t_end"])
        if getattr(te.dt, "tz", None) is not None:
            te = te.dt.tz_convert("UTC").dt.tz_localize(None)
        v = te.to_numpy(dtype="datetime64[ns]").astype(np.int64)
        bad = pd.isna(meta["t_end"]).to_numpy()
        return np.where(bad, t, v)
    return t.copy()


def _session_day(meta, n):
    """Integer code 0..T-1 of the Globex session day of each row (time unit of the paper's daily return series).
    A session runs 18:00 ET (prev. day) -> 17:00 ET, so day = date(t + 6 h) in New York time. Without meta['t'] the
    rows are taken as time-ordered and grouped in blocks of 20 (labelled fallback)."""
    if meta is not None and "t" in meta.columns:
        t = pd.to_datetime(meta["t"])
        if getattr(t.dt, "tz", None) is not None:
            t = t.dt.tz_convert("America/New_York").dt.tz_localize(None)
        d = (t + pd.Timedelta(hours=6)).dt.normalize()
        codes, _ = pd.factorize(d, sort=True)
        return codes.astype(np.int64)
    return (np.arange(n) // 20).astype(np.int64)


def _inner_blocks(meta, n):
    """Inner time split of the TRAINING rows into blocks A < B < C (0/1/2). As SPEC.md's logit inner split: the last
    two training years are B and C when >= 4 years exist; otherwise time quantiles 60% / 80% (labelled fallback)."""
    t = _time_ns(meta, n)
    blk = None
    if meta is not None and "year" in meta.columns:
        yr = pd.to_numeric(meta["year"], errors="coerce").to_numpy()
        ys = np.unique(yr[np.isfinite(yr)])
        if len(ys) >= 4:
            Y = ys.max()
            blk = np.where(yr <= Y - 2, 0, np.where(yr == Y - 1, 1, 2))
    if blk is None or min((blk == i).sum() for i in range(3)) < 20:
        q1, q2 = np.quantile(t, [0.6, 0.8])
        blk = np.where(t < q1, 0, np.where(t < q2, 1, 2))
    return blk, t, _tend_ns(meta, n, t)


def _inner_folds(meta, n):
    """Expanding, purged folds: fit on A -> predict B; fit on A+B -> predict C. Training rows whose label end
    (t_end) reaches the start of the predicted block are purged (SPEC.md purge rule)."""
    blk, t, te = _inner_blocks(meta, n)
    folds = []
    for b in (1, 2):
        test = np.flatnonzero(blk == b)
        if len(test) == 0:
            continue
        t0 = t[test].min()
        train = np.flatnonzero((blk < b) & (te < t0))
        if len(train) >= 20:
            folds.append((train, test))
    return folds


def _wtable(rows):
    df = pd.DataFrame(rows, columns=["signal", "weight", "points", "meaning", "source"])
    df["weight"] = df["weight"].astype(float)
    df["points"] = df["points"].astype(float)
    return df


def _pts(wt):
    return float(wt) / LN2_20


def _toward(task):
    return "a winning trade" if task == "entry" else "exiting now (evidence against the open trade)"


# ============================================================================================ A1. the rule universe
class _Rules:
    """The rule universe: rule = (column, op, threshold) -> fires (1) or not (0) on each candidate. NaN never fires.

    Paper analogue: their 7,846 rules are parameter grids of five classic families (filter rules, moving averages,
    support/resistance, channel breakouts, on-balance volume; appendix A), each emitting long/short/hold. Our
    candidates already carry a direction (textbook pattern), so a 'rule' is a feature condition that says TAKE (fires)
    or SKIP. Grid (our adaptation, labelled): each value of a discrete flag ({-1,0,1} -> '=+1', '=-1'; {0,1} -> '=1',
    '=0'), and for continuous columns '> q' and '<= q' at the training-sample quintile cuts q20..q80."""

    def __init__(self, X: pd.DataFrame, quantiles=(0.2, 0.4, 0.6, 0.8)):
        self.rules = []
        for c in X.columns:
            v = _col(X, c)
            fin = v[np.isfinite(v)]
            if fin.size == 0:
                continue
            u = np.unique(fin)
            if len(u) < 2:
                continue
            if len(u) <= 3 and set(u.tolist()) <= {-1.0, 0.0, 1.0}:
                vals = [x for x in (1.0, -1.0) if x in u] if (u < 0).any() and (u > 0).any() else list(u[::-1])
                self.rules += [(c, "==", float(x)) for x in vals]
            else:
                for q in np.unique(np.quantile(fin, quantiles)):
                    if q < fin.max():
                        self.rules += [(c, ">", float(q)), (c, "<=", float(q))]

    def __len__(self):
        return len(self.rules)

    @staticmethod
    def fire(v, op, thr):
        with np.errstate(invalid="ignore"):
            if op == "==":
                return v == thr
            if op == ">":
                return v > thr
            return v <= thr          # NaN <= thr is False

    def name(self, j):
        c, op, thr = self.rules[j]
        if op == "==":
            return f"{c} = {thr:+g}" if thr != 0 else f"{c} = 0"
        return f"{c} {op} {thr:.4g}"

    def matrix(self, X: pd.DataFrame, idx) -> np.ndarray:
        out = np.zeros((len(X), len(idx)), np.float32)          # float32: 1M rows x 100 survivors = 400 MB max
        cache = {}
        for k, j in enumerate(idx):
            c, op, thr = self.rules[j]
            if c not in cache:
                cache[c] = _col(X, c)
            out[:, k] = self.fire(cache[c], op, thr)
        return out


# ========================================================================= A2. stationary bootstrap and the screen
def politis_white_block(x) -> float:
    """Automatic expected block length for the stationary bootstrap: Politis & White (2004, Econometric Reviews 23)
    with the Patton, Politis & White (2009) correction; constants as in the `arch` package (kn = max(5, log10 n),
    m_max = ceil(sqrt n) + kn, band 2 sqrt(log10 n / n), flat-top window, D_SB = 2 g(0)^2, cap min(3 sqrt n, n/3))."""
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    if n < 11 or not np.any(x):
        return 1.0
    kn = max(5, int(np.log10(n)))
    m_max = int(np.ceil(np.sqrt(n))) + kn
    b_max = float(np.ceil(min(3 * np.sqrt(n), n / 3)))
    cv = 2 * np.sqrt(np.log10(n) / n)
    acv = np.array([x[: n - k] @ x[k:] / n for k in range(m_max + 1)])
    if acv[0] <= 0:
        return 1.0
    abs_acorr = np.abs(acv[1:] / acv[0])
    opt_m = None
    for i in range(kn, m_max + 1):
        if np.all(abs_acorr[i - kn:i] < cv):
            opt_m = i - kn
            break
    m = 2 * max(opt_m, 1) if opt_m is not None else m_max
    m = min(m, m_max)
    g, lr = 0.0, acv[0]
    for k in range(1, m + 1):
        lam = 1.0 if k / m <= 0.5 else 2 * (1 - k / m)
        g += 2 * lam * k * acv[k]
        lr += 2 * lam * acv[k]
    d_sb = 2 * lr ** 2
    if d_sb <= 0:
        return 1.0
    b = ((2 * g ** 2) / d_sb) ** (1 / 3) * n ** (1 / 3)
    return float(min(max(b, 1.0), b_max))


def stationary_bootstrap_counts(T, B, block, rng) -> np.ndarray:
    """Politis & Romano (1994) stationary bootstrap of a length-T series, returned as a (B, T) matrix of how often
    each period is drawn (so bootstrap means are C @ W / T). Blocks start uniformly, length ~ Geometric(1/block),
    wrapping circularly."""
    p = 1.0 / max(block, 1.0)
    ar = np.arange(T)
    new = rng.random((B, T)) < p
    new[:, 0] = True
    starts = rng.integers(0, T, size=(B, T))
    last = np.maximum.accumulate(np.where(new, ar[None, :], 0), axis=1)
    idx = (np.take_along_axis(starts, last, axis=1) + (ar[None, :] - last)) % T
    flat = (np.arange(B)[:, None] * T + idx).ravel()
    return np.bincount(flat, minlength=B * T).reshape(B, T).astype(np.float64)


def politis_white_cbb(x) -> int:
    """Integer block length for the circular block bootstrap: same Politis & White (2004) / Patton et al. (2009)
    machinery with D_CB = (4/3) g(0)^2 instead of 2 g(0)^2."""
    b_sb = politis_white_block(x)
    return max(1, int(round(b_sb * (2.0 / (4.0 / 3.0)) ** (1 / 3)))) if b_sb > 1 else 1


def _cbb_roots(W, b, B, rng, chunk=1000):
    """Studentized circular-block-bootstrap roots with the 'natural' block variance in the bootstrap world (Goetze &
    Kuensch 1996; Romano & Wolf 2005 sec. 4.1 and their empirical application: circular block bootstrap, natural
    variance estimator). Real-world statistic studentized by the matching circular block-sum (Bartlett, bandwidth b)
    long-run variance. Returns Z (S,), roots (B, S)."""
    T, S = W.shape
    b = int(max(1, min(b, T)))
    Kb = int(math.ceil(T / b))
    cs = np.vstack([np.zeros((1, S)), np.cumsum(np.vstack([W, W[:b]]), axis=0)])
    Sb = cs[b:b + T] - cs[:T]                       # (T, S) circular block sums starting at each t
    xbar = W.mean(0)
    lrv = np.maximum((Sb ** 2).mean(0) - (b * xbar) ** 2, 0.0) / b
    ok = lrv > 1e-18
    Z = np.where(ok, np.sqrt(T) * xbar / np.sqrt(np.where(ok, lrv, 1.0)), 0.0)
    Sb2 = Sb ** 2
    R = np.empty((B, S))
    for b0 in range(0, B, chunk):
        nb = min(chunk, B - b0)
        starts = rng.integers(0, T, size=(nb, Kb))
        flat = (np.arange(nb)[:, None] * T + starts).ravel()
        C = np.bincount(flat, minlength=nb * T).reshape(nb, T).astype(np.float64)
        m1 = C @ Sb / Kb                                # mean block sum
        m2 = C @ Sb2 / Kb
        var = np.maximum(m2 - m1 ** 2, 0.0) / b         # natural variance of sqrt(b) x block mean
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.sqrt(Kb * b) * (m1 / b - xbar) / np.sqrt(var)
        r[~np.isfinite(r)] = 0.0
        R[b0:b0 + nb] = r
    return Z, R, ok


def balanced_kstepm(W, k=1, alpha=0.10, B=1000, block=None, seed=0, chunk=1000, bootstrap="cbb"):
    """One-sided studentized k-FWER stepdown with balanced (prepivoted) critical values.

    W: (T, S) per-period excess payoff of S rules over the benchmark (paper eq. 1-3: w_t = r_t,s - r_t,benchmark).
    Statistic Z_s = sqrt(T) mean / sigma_s (paper eq. 1-3 studentize by the plain sd; with serially dependent periods
    we use the long-run sd that matches the bootstrap, see below). Bootstrap roots (resampling FROM THE DATA, Romano &
    Wolf 2010 sec. 5) R*_s = sqrt(T)(mean*_s - mean_s)/sigma*_s; marginal cdf H_s; prepivoted values U = H_s(R*_s);
    critical gamma_K = (1-alpha) quantile of the k-th largest U over K (eq. 3.6 / 5.1); reject H_s if H_s(Z_s) >
    gamma_K; streamlined stepdown (Algorithm 4.2): K = not-rejected plus the k-1 least significant rejected.
    bootstrap="cbb" (default): circular block bootstrap, bootstrap-world 'natural' block variance, real-world
    Bartlett block-sum long-run variance, integer block from Politis-White (Romano & Wolf 2005's own empirical
    choice). bootstrap="sb": Politis-Romano stationary bootstrap with plain-sd studentization in both worlds.
    Measured size at nominal alpha = 0.10 (k = 1, 40 rules, B = 1000, 150-200 simulated null panels; our check, not a
    published number): iid days 0.08-0.115; AR(1) phi = 0.3 days 0.18 (T = 500) and 0.15 (T = 2,500); finite-sample
    oversize of block bootstraps under dependence is known; Romano & Wolf (2005) Algorithm 6.1 (calibrated block size)
    is the published remedy and is NOT implemented (compute).
    Returns dict(Z, p (marginal, 1 - H_s(Z_s)), rejected, block, B, steps)."""
    W = np.asarray(W, float)
    T, S = W.shape
    rng = np.random.default_rng(seed)
    mu = W.mean(0)
    sd = W.std(0, ddof=1) if T > 1 else np.zeros(S)
    ok = sd > 1e-12
    if block is None:
        cols = np.flatnonzero(ok)
        if len(cols) > 50:
            cols = rng.choice(cols, 50, replace=False)
        pw = politis_white_cbb if bootstrap == "cbb" else politis_white_block
        block = float(np.median([pw(W[:, j]) for j in cols])) if len(cols) else 1.0
    if bootstrap == "cbb":
        Z, R, ok2 = _cbb_roots(W, int(round(block)), B, rng, chunk)
        ok &= ok2
    else:                                                   # stationary bootstrap, iid-sd studentization
        Z = np.where(ok, np.sqrt(T) * mu / np.where(ok, sd, 1.0), 0.0)
        R = np.empty((B, S))
        W2 = W * W
        for b0 in range(0, B, chunk):
            nb = min(chunk, B - b0)
            C = stationary_bootstrap_counts(T, nb, block, rng)
            m1 = C @ W / T
            m2 = C @ W2 / T
            sds = np.sqrt(np.maximum(m2 - m1 ** 2, 0.0) * T / max(T - 1, 1))
            with np.errstate(divide="ignore", invalid="ignore"):
                r = np.sqrt(T) * (m1 - mu) / sds
            r[~np.isfinite(r)] = 0.0
            R[b0:b0 + nb] = r
    Rs = np.sort(R, axis=0)
    Hz = np.array([np.searchsorted(Rs[:, s], Z[s], side="right") / B for s in range(S)])
    p = 1.0 - Hz
    U = rankdata(R, axis=0, method="max") / B
    active = ok.copy()
    rejected = np.zeros(S, bool)
    K = np.flatnonzero(active)
    steps = 0
    while len(K) >= k and active.any():
        steps += 1
        kmax = np.partition(U[:, K], len(K) - k, axis=1)[:, len(K) - k]
        gamma = float(np.quantile(kmax, 1 - alpha, method="inverted_cdf"))
        new = active & (Hz > gamma)
        if not new.any():
            break
        rejected |= new
        active &= ~new
        if rejected.sum() < k:
            break
        rej = np.flatnonzero(rejected)
        least = rej[np.argsort(-p[rej], kind="stable")[: k - 1]] if k > 1 else np.array([], int)
        K = np.union1d(np.flatnonzero(active), least).astype(int)
    return dict(Z=Z, p=p, rejected=rejected, block=float(block), B=int(B), steps=steps, mean=mu)


# ============================================================================== A3. the screen (shared by A-scorers)
class _ScreenBase(Scorer):
    """Shared pipeline: rule universe -> balanced k-StepM screen on per-session-day excess net $ -> combiner."""
    family = "stat"
    combiner = "base"
    default_n = 15
    source = SRC_HSS

    def __init__(self, task: str = "entry", **params):
        super().__init__(task, **params)
        p = self.params
        self.alpha = float(p.get("alpha", 0.10))
        self.k_frac = float(p.get("k_frac", 0.005))
        self.B = p.get("B", None)
        self.benchmark = p.get("benchmark", "random_skip")
        self.metric = p.get("metric", "auto")
        self.quantiles = tuple(p.get("quantiles", (0.2, 0.4, 0.6, 0.8)))
        self.n_inputs = p.get("n_inputs", self.default_n)
        self.rank_by = p.get("rank_by", "accuracy")
        self.block = p.get("block", None)
        self.bootstrap = p.get("bootstrap", "cbb")
        self.seed = int(p.get("seed", 0))

    # ------------------------------------------------------------------------------------------------- screen
    def _screen(self, X, y, w, meta):
        """Run (or reuse, for the same training rows and settings) the screen, then pick the combiner's inputs."""
        n = len(y)
        pay, kind = _payoff(y, meta, self.task, self.metric)
        day = _session_day(meta, n)
        cfg = (self.task, self.alpha, self.k_frac, self.B, self.benchmark, kind, self.quantiles, self.rank_by,
               self.block, self.bootstrap, self.seed)
        key = ("screen", _fingerprint(y, w, pay, day, X=X), cfg)
        hit = _cache_get(key)
        if hit is None:
            hit = self._run_screen(X, y, w, pay, day)
            _cache_put(key, hit)
        (self.rules_, self.screen_, surv, self.k_, self.T_days_, self.B_, self.block_) = hit
        self.payoff_kind_ = kind
        self.survivors_ = surv
        nin = self.n_inputs
        self.selected_ = surv if nin is None else surv[: int(nin)]
        return self.selected_

    def _run_screen(self, X, y, w, pay, day):
        R = _Rules(X, self.quantiles)
        S = len(R)
        T = int(day.max()) + 1 if len(day) else 0
        base = w * pay
        sw = w.sum()
        Wd = np.empty((T, S))
        acc = np.empty(S)
        share = np.empty(S)
        lift = np.empty(S)
        y1 = y > 0.5
        cache = {}
        for j, (c, op, thr) in enumerate(R.rules):
            if c not in cache:
                cache = {c: _col(X, c)}
            m = R.fire(cache[c], op, thr)
            f = float(w[m].sum() / sw)
            share[j] = f
            contrib = base * (m - f) if self.benchmark == "random_skip" else base * m
            Wd[:, j] = np.bincount(day, weights=contrib, minlength=T)
            acc[j] = float(w[m == y1].sum() / sw)
            lift[j] = (_wmean(pay[m], w[m]) - _wmean(pay, w)) if m.any() else 0.0
        k = max(1, int(round(self.k_frac * S)))
        B = int(self.B) if self.B else max(1000, 20 * S)
        res = balanced_kstepm(Wd, k=k, alpha=self.alpha, B=B, block=self.block, seed=self.seed,
                              bootstrap=self.bootstrap) if S and T > 2 \
            else dict(Z=np.zeros(S), p=np.ones(S), rejected=np.zeros(S, bool), block=1.0, B=B, steps=0)
        screen = pd.DataFrame({
            "rule": [R.name(j) for j in range(S)], "t_stat": res["Z"], "p_marginal": res["p"],
            "survivor": res["rejected"], "accuracy": acc, "fire_share": share, "lift_per_trade": lift})
        surv = np.flatnonzero(res["rejected"])
        # drop exact duplicates among survivors (identical firing columns would make the combiners singular)
        if len(surv) > 1:
            seen, keep = set(), []
            for j in surv:
                c, op, thr = R.rules[j]
                h = hashlib.sha1(np.packbits(R.fire(_col(X, c), op, thr)).tobytes()).hexdigest()
                if h not in seen:
                    seen.add(h)
                    keep.append(j)
            surv = np.asarray(keep, int)
        key = acc if self.rank_by == "accuracy" else res["Z"]
        surv = surv[np.argsort(-key[surv], kind="stable")]
        return R, screen, surv, k, T, res["B"], res["block"]

    # -------------------------------------------------------------------------------------------- interface
    def fit(self, X, y, w=None, meta=None):
        y = np.asarray(y, float)
        w = _weights(w, len(y))
        self._screen(X, y, w, meta)
        self.base_rate_ = _wmean(y, w)
        if len(self.selected_) == 0:
            self.a_, self.b_ = 0.0, float(_logit(self.base_rate_))
            return self
        Xr = self.rules_.matrix(X, self.selected_)
        self._fit_combiner(Xr, y, w, meta)
        self.a_, self.b_ = _platt_ab(self._raw(Xr), y, w)
        return self

    def raw_score(self, X):
        if len(self.selected_) == 0:
            return np.zeros(len(X))
        return self._raw(self.rules_.matrix(X, self.selected_))

    def score(self, X):
        return self.a_ * self.raw_score(X) + self.b_

    def predict_proba(self, X):
        return expit(self.score(X))

    # ---------------------------------------------------------------------------------------- weights table
    def _rule_rows(self, coefs, intercept, src):
        rows = [("intercept (no rule fires)", intercept, _pts(intercept),
                 f"base log-odds of {_toward(self.task)} when none of the selected rules fires", src)]
        for j, cf in zip(self.selected_, coefs):
            nm = self.rules_.name(j)
            r = self.screen_.iloc[int(j)]
            rows.append((nm, cf, _pts(cf),
                         f"when '{nm}' holds: {cf:+.3f} log-odds ({_pts(cf):+.1f} pts) toward {_toward(self.task)}; "
                         f"screen t={r.t_stat:.2f}, marginal p={r.p_marginal:.4f}, fires on {r.fire_share:.1%}, "
                         f"IS accuracy {r.accuracy:.3f}", src))
        return _wtable(rows)

    def _empty_table(self):
        return _wtable([("intercept (no rule survived the screen)", self.b_, _pts(self.b_),
                         f"no rule survived the k-FWER screen (k={self.k_}, alpha={self.alpha}); the score is the "
                         f"training base rate {self.base_rate_:.3f}", self.source)])

    def weights_table(self):
        if len(self.selected_) == 0:
            return self._empty_table()
        coef, icpt = self._linear()
        return self._rule_rows(self.a_ * coef, self.a_ * icpt + self.b_, self.source)

    def _linearised_table(self, X_fit):
        """For the NONLINEAR combiners (RVM, BNN): least-squares projection of the log-odds score on the rule
        indicators over the fit sample, flagged as an approximation (not the model's own weights)."""
        if len(self.selected_) == 0:
            return self._empty_table()
        s = self.a_ * self._raw(X_fit) + self.b_
        A = np.column_stack([np.ones(len(X_fit)), X_fit])
        beta, *_ = np.linalg.lstsq(A, s, rcond=None)
        r2 = 1 - np.var(s - A @ beta) / max(np.var(s), 1e-12)
        df = self._rule_rows(beta[1:], beta[0], self.source)
        df["meaning"] = df["meaning"] + f" [LINEARISED summary of a nonlinear model, R^2={r2:.2f}]"
        return df


# --------------------------------------------------------------------------------------------- A4. the combiners
@register
class StatScreenNB(_ScreenBase):
    """Naive Bayes on the best N screen survivors (paper sec. 2.5, eq. 27-28; benchmark of the Bayesian models).
    Inputs are the rule indicators (Bernoulli/multinomial NB); class-conditional probabilities with Laplace add-one
    smoothing (labelled fallback: the paper does not state its smoothing). Linear in log-odds."""
    name = "stat_screen_nb"
    combiner = "Naive Bayes"
    default_n = 15
    source = SRC_HSS + "; NB sec. 2.5"

    def _fit_combiner(self, Xr, y, w, meta):
        n1, n0 = w[y > 0.5].sum(), w[y <= 0.5].sum()
        t1 = (Xr[y > 0.5] * w[y > 0.5, None]).sum(0)
        t0 = (Xr[y <= 0.5] * w[y <= 0.5, None]).sum(0)
        th1, th0 = (t1 + 1) / (n1 + 2), (t0 + 1) / (n0 + 2)
        self.coef_ = np.log(th1 / th0) - np.log((1 - th1) / (1 - th0))
        self.icpt_ = float(np.log((n1 + 1) / (n0 + 1)) + np.log((1 - th1) / (1 - th0)).sum())

    def _raw(self, Xr):
        return self.icpt_ + Xr @ self.coef_

    def _linear(self):
        return self.coef_, self.icpt_


@register
class StatScreenSA(_ScreenBase):
    """Simple Average of the best N survivors' signals (the paper's naive SA benchmark, sec. 4.2): raw score = share
    of the top-N rules that fire on the candidate."""
    name = "stat_screen_sa"
    combiner = "Simple Average"
    default_n = 15
    source = SRC_HSS + "; SA benchmark sec. 4.2"

    def _fit_combiner(self, Xr, y, w, meta):
        self.coef_ = np.full(Xr.shape[1], 1.0 / Xr.shape[1])

    def _raw(self, Xr):
        return Xr @ self.coef_

    def _linear(self):
        return self.coef_, 0.0


# ----------------------------------------------------------------------------------------------- A4b. RVM
def _rvm_regression(Phi, t, max_iter=300, tol=1e-3, prune=1e9):
    """Tipping (2001, JMLR 1) sparse Bayesian regression, the paper's eq. 10-11 (posterior), 15 (alpha_m = gamma_m /
    mu_m^2), 16 (sigma^2 = ||t - Phi mu||^2 / (T - sum gamma)). Basis functions with alpha > `prune` are removed
    ('many alpha_j approach infinity', paper sec. 2.2). Initial alpha = 1, beta = 1/var(t), tol and prune are
    labelled fallbacks (not given in the paper)."""
    N, M = Phi.shape
    PtP, Ptt, tt = Phi.T @ Phi, Phi.T @ t, float(t @ t)
    alpha = np.ones(M)
    beta = 1.0 / max(float(np.var(t)), 1e-6)
    act = np.ones(M, bool)
    mu, ia = np.zeros(M), np.arange(M)
    for _ in range(max_iter):
        ia = np.flatnonzero(act)
        A = beta * PtP[np.ix_(ia, ia)] + np.diag(alpha[ia])
        try:
            L = np.linalg.cholesky(A)
        except np.linalg.LinAlgError:
            L = np.linalg.cholesky(A + 1e-8 * np.eye(len(ia)))
        Linv = np.linalg.inv(L)
        Sigma = Linv.T @ Linv
        m = beta * Sigma @ Ptt[ia]
        gamma = 1 - alpha[ia] * np.diag(Sigma)
        new_alpha = gamma / np.maximum(m ** 2, 1e-300)
        resid = tt - 2 * m @ Ptt[ia] + m @ PtP[np.ix_(ia, ia)] @ m
        beta = max(N - gamma.sum(), 1e-6) / max(resid, 1e-12)
        delta = np.max(np.abs(np.log(np.maximum(new_alpha, 1e-300)) - np.log(alpha[ia])))
        alpha[ia] = new_alpha
        mu = np.zeros(M)
        mu[ia] = m
        keep = new_alpha < prune
        if not keep.any():
            keep[np.argmin(new_alpha)] = True
        act[ia] = keep
        if delta < tol:
            break
    ia = np.flatnonzero(act)
    A = beta * PtP[np.ix_(ia, ia)] + np.diag(alpha[ia])
    mu = np.zeros(M)
    mu[ia] = beta * np.linalg.solve(A + 1e-10 * np.eye(len(ia)), Ptt[ia])
    return mu, act, beta


@register
class StatScreenRVM(_ScreenBase):
    """Relevance Vector Machine (Tipping 2001) fed with ALL screen survivors (paper sec. 4: 'the RVM ... is fed with
    all the identified genuine profitable technical rules'). Gaussian (regression) RVM on the 0/1 label as in the
    paper's eq. 4-18, RBF kernel basis (paper: 'RBF is mostly considered'). Compute adaptation (labelled): the
    kernel basis is a random sample of <= 300 distinct training input patterns (Tipping uses every training point)
    and the evidence iterations run on <= 5,000 weighted-sampled training rows; RBF width r^2 = median pairwise
    squared distance between basis patterns (median heuristic; the paper gives no width)."""
    name = "stat_screen_rvm"
    combiner = "Relevance Vector Machine"
    default_n = None
    source = SRC_HSS + "; RVM sec. 2.2 (Tipping 2001)"

    def _fit_combiner(self, Xr, y, w, meta):
        rng = np.random.default_rng(self.seed + 1)
        n = len(y)
        nfit = int(self.params.get("rvm_rows", 5000))
        idx = rng.choice(n, nfit, replace=True, p=w / w.sum()) if n > nfit else np.arange(n)
        Xs = Xr[idx]
        ys = y[idx]
        uniq = np.unique(Xs, axis=0)
        mb = int(self.params.get("rvm_basis", 300))
        if len(uniq) > mb:
            uniq = uniq[rng.choice(len(uniq), mb, replace=False)]
        self.basis_ = uniq
        d2 = ((uniq[:, None, :] - uniq[None, :, :]) ** 2).sum(-1)
        nz = d2[np.triu_indices(len(uniq), 1)]
        nz = nz[nz > 0]
        self.r2_ = float(np.median(nz)) if nz.size else 1.0
        Phi = self._phi(Xs)
        self.mu_, self.active_, self.beta_ = _rvm_regression(Phi, ys)
        self._fit_rows = Xs

    def _phi(self, Xr):
        out = np.empty((len(Xr), len(self.basis_) + 1))
        out[:, 0] = 1.0
        bb = (self.basis_ ** 2).sum(1)
        for s in range(0, len(Xr), 100_000):
            x = Xr[s:s + 100_000]
            d2 = np.maximum((x ** 2).sum(1)[:, None] + bb[None, :] - 2 * x @ self.basis_.T, 0)
            out[s:s + 100_000, 1:] = np.exp(-d2 / self.r2_)
        return out

    def _raw(self, Xr):
        return self._phi(Xr) @ self.mu_

    def weights_table(self):
        if len(self.selected_) == 0:
            return self._empty_table()
        df = self._linearised_table(self._fit_rows)
        df.attrs["note"] = (f"{int(self.active_[1:].sum())} relevance vectors kept of {len(self.basis_)} basis "
                            f"patterns; RBF r^2={self.r2_:.3g}; weights are a linearised summary")
        return df


# --------------------------------------------------------------------------------------- A4c. DMA / DMS / BMA
def _spd_inv_logdet(Q):
    """Inverse and log-determinant of a stack of SPD matrices via one batched Cholesky and a vectorised forward
    substitution (about 3x faster than np.linalg.inv + slogdet for many small matrices)."""
    L = np.linalg.cholesky(Q)
    p = Q.shape[-1]
    d = np.diagonal(L, axis1=1, axis2=2)
    Li = np.zeros_like(L)
    for i in range(p):
        r = -(L[:, i:i + 1, :i] @ Li[:, :i, :])[:, 0, :] if i else np.zeros((len(Q), p))
        r[:, i] += 1.0
        Li[:, i, :] = r / d[:, i:i + 1]
    return Li.transpose(0, 2, 1) @ Li, 2 * np.log(d).sum(1)


_CACHE: dict = {}


def _cache_get(key):
    return _CACHE.get(key)


def _cache_put(key, val, max_items=6):
    if len(_CACHE) >= max_items:
        _CACHE.pop(next(iter(_CACHE)))
    _CACHE[key] = val


def _fingerprint(*arrays, X=None):
    """Cheap fingerprint of the training rows: full hash of y / w / time arrays and of ~10,000 evenly spaced X rows
    plus the column names and shape. Used only to reuse an identical screen / DMA run across the scorers of one
    fold (the same training rows), never across different data."""
    h = hashlib.sha1()
    for a in arrays:
        a = np.ascontiguousarray(np.asarray(a))
        h.update(str(a.shape).encode())
        h.update(a.tobytes())
    if X is not None:
        h.update(repr((X.shape, list(X.columns))).encode())
        step = max(1, len(X) // 10_000)
        h.update(np.ascontiguousarray(X.iloc[::step].to_numpy(dtype=np.float64, na_value=np.nan)).tobytes())
    return h.hexdigest()


def _dma_run(Xr, y, w, day, combos, eval_frac=0.2):
    """Raftery, Karny & Ettler (2010, Technometrics 52) DMA over all 2^N subsets of the N inputs (intercept always in),
    for several (delta = model forgetting, lambda = parameter forgetting, c) combos at once.

    Per model: y ~ N(x' theta, V), theta random walk with R_t = C_{t-1} / lambda (their eq. 5); Kalman update; V by
    their recursive method-of-moments estimator (A_t, eq. after (10)); model prediction pi_{t|t-1} = (pi^delta + c)
    / sum (their eq. 17, c = 0.001/K); update by the predictive likelihood (paper eq. 22). Prior (their sec. 4):
    theta_0 = 0, Sigma_0 = diag(beta0^2 + Var y, Var y / Var x_j) with beta0 = intercept of a static OLS on the
    (training) data. V_0 = Var y (labelled fallback: not stated). Time step = one session day: all candidates of a
    day update the state as one batch (adaptation: the paper's daily FX observation <-> our many candidates/day).
    Returns per combo: final model probs (one step ahead), states, and the day-by-day one-step-ahead squared error
    of the DMA and DMS forecasts over the last `eval_frac` of the days."""
    n, N = Xr.shape
    p = N + 1
    order = np.argsort(day, kind="stable")
    F = np.column_stack([np.ones(n), Xr])[order]
    y, w, day = y[order], w[order], day[order]
    pos = w > 0
    F, y, w, day = F[pos], y[pos], w[pos], day[pos]
    _, day = np.unique(day, return_inverse=True)
    n = len(y)
    T = int(day.max()) + 1
    starts = np.searchsorted(day, np.arange(T))
    ends = np.r_[starts[1:], n]
    G = np.zeros((T, p, p))
    for i in range(p):
        for j in range(i, p):
            G[:, i, j] = G[:, j, i] = np.bincount(day, w * F[:, i] * F[:, j], minlength=T)
    gv = np.stack([np.bincount(day, w * F[:, i] * y, minlength=T) for i in range(p)], 1)
    yy = np.bincount(day, w * y * y, minlength=T)
    sw = np.bincount(day, w, minlength=T)
    cnt = np.bincount(day, minlength=T).astype(float)
    slw = np.bincount(day, np.log(w), minlength=T)
    # prior (Raftery et al. 2010 sec. 4)
    vy = _wmean((y - _wmean(y, w)) ** 2, w)
    vy = max(vy, 1e-6)
    vx = np.array([_wmean((F[:, j] - _wmean(F[:, j], w)) ** 2, w) for j in range(1, p)])
    sqw = np.sqrt(w)
    b_ols, *_ = np.linalg.lstsq(F * sqw[:, None], y * sqw, rcond=None)
    s2 = np.r_[b_ols[0] ** 2 + vy, vy / np.maximum(vx, 1e-6)]
    U = 2 ** N
    A = np.column_stack([np.ones(U, bool), ((np.arange(U)[:, None] >> np.arange(N)[None, :]) & 1).astype(bool)])
    nc = len(combos)
    Mi = nc * U
    Am = np.tile(A, (nc, 1)).astype(float)
    AA = Am[:, :, None] * Am[:, None, :]
    di = np.arange(p)
    Iin = np.zeros((Mi, p, p))
    Iin[:, di, di] = 1 - Am
    dlt = np.array([c[0] for c in combos], float)
    lam = np.repeat(np.array([c[1] for c in combos], float), U)
    cc = np.array([c[2] for c in combos], float)
    Cov = np.zeros((Mi, p, p))
    Cov[:, di, di] = np.where(Am > 0, s2[None, :], 1.0)
    Prec = np.zeros((Mi, p, p))
    Prec[:, di, di] = 1.0 / Cov[:, di, di]
    logdetPrec = np.where(Am > 0, -np.log(s2)[None, :], 0.0).sum(1)
    pu = Am.sum(1)
    m = np.zeros((Mi, p))
    V = np.full(Mi, vy)
    cntV = np.zeros(Mi)
    pi = np.full((nc, U), 1.0 / U)
    e0 = min(max(int(math.floor((1 - eval_frac) * T)), 1), T - 1) if T > 1 else T
    sse = np.zeros((2, nc))
    swe = 0.0
    log2pi = math.log(2 * math.pi)
    for t in range(T):
        pid = np.exp(dlt[:, None] * np.log(np.maximum(pi, 1e-300))) * (pi > 0) + cc[:, None]
        pipred = pid / pid.sum(1, keepdims=True)
        if t >= e0:
            r0, r1 = starts[t], ends[t]
            Fd, yd, wd = F[r0:r1], y[r0:r1], w[r0:r1]
            mm = m.reshape(nc, U, p)
            mbar = np.einsum("cu,cup->cp", pipred, mm)
            mbest = mm[np.arange(nc), pipred.argmax(1)]
            sse[0] += (wd[:, None] * (yd[:, None] - Fd @ mbar.T) ** 2).sum(0)
            sse[1] += (wd[:, None] * (yd[:, None] - Fd @ mbest.T) ** 2).sum(0)
            swe += wd.sum()
        Gu = AA * G[t]
        gu = Am * gv[t]
        Rinv = lam[:, None, None] * Prec * AA + Iin
        logdetRinv = pu * np.log(lam) + logdetPrec
        trRG = (Cov * Gu).sum((1, 2)) / lam
        Gm = (Gu @ m[:, :, None])[:, :, 0]
        eWe = yy[t] - 2 * (m * gu).sum(1) + (m * Gm).sum(1)
        Fe = gu - Gm
        Q = Rinv + Gu / V[:, None, None]
        Qinv, logdetQ = _spd_inv_logdet(Q)
        quad = eWe / V - (Fe[:, None, :] @ Qinv @ Fe[:, :, None])[:, 0, 0] / V ** 2
        ll = -0.5 * (cnt[t] * (log2pi + np.log(V)) - slw[t] + logdetQ - logdetRinv + quad)
        rhs = (Rinv @ m[:, :, None])[:, :, 0] + gu / V[:, None]
        m = (Qinv @ rhs[:, :, None])[:, :, 0]
        lp = np.log(np.maximum(pipred, 1e-300)) + ll.reshape(nc, U)
        lp -= lp.max(1, keepdims=True)
        pi = np.exp(lp) * (pipred > 0)
        pi /= pi.sum(1, keepdims=True)
        Anew = (cntV * V + (eWe - trRG)) / (cntV + sw[t])
        V = np.where(Anew > 0, Anew, V)
        cntV = cntV + sw[t]
        Cov, Prec, logdetPrec = Qinv, Q, logdetQ
    pid = np.exp(dlt[:, None] * np.log(np.maximum(pi, 1e-300))) * (pi > 0) + cc[:, None]
    pinext = pid / pid.sum(1, keepdims=True)
    mse = sse / swe if swe > 0 else np.full((2, nc), np.nan)
    return dict(pi=pinext, m=m.reshape(nc, U, p), mse_dma=mse[0], mse_dms=mse[1], masks=A, T=T)


DMA_GRID = (0.90, 0.95, 0.99, 1.0)        # paper sec. 2.3: {0.90, 0.95, 0.99, 1} for both forgetting factors


class _DMABase(_ScreenBase):
    default_n = 10
    select = "dma"

    def _combos(self, N):
        return [(d, l, 0.001 / 2 ** N) for d in DMA_GRID for l in DMA_GRID]

    def _fit_combiner(self, Xr, y, w, meta):
        day = _session_day(meta, len(y))
        N = Xr.shape[1]
        combos = self._combos(N)
        U = 2 ** N
        per_run = max(1, int(2 ** 15 // U))
        key = ("dma", _fingerprint(Xr, y, w, day), tuple(combos))
        out = _cache_get(key)
        if out is None:                       # DMA and DMS share one recursion on the same fold
            out = [_dma_run(Xr, y, w, day, combos[s:s + per_run], eval_frac=0.2)
                   for s in range(0, len(combos), per_run)]
            _cache_put(key, out)
        mse = np.concatenate([o["mse_dma" if self.select != "dms" else "mse_dms"] for o in out])
        pis = np.concatenate([o["pi"] for o in out])
        ms = np.concatenate([o["m"] for o in out])
        A = out[0]["masks"]
        if len(combos) > 1 and np.isfinite(mse).any():
            ci = int(np.nanargmin(mse))
        else:
            ci = next((i for i, c in enumerate(combos) if c[0] == 0.99 and c[1] == 0.99), 0)
        self.combo_, self.combo_mse_ = combos[ci], (float(mse[ci]) if np.isfinite(mse[ci]) else np.nan)
        self.grid_mse_ = {(c[0], c[1]): float(v) for c, v in zip(combos, mse)}
        pi, mm = pis[ci], ms[ci]
        if self.select == "dms":
            u = int(np.argmax(pi))
            beta = mm[u]
            self.model_desc_ = f"model {u} (p={pi[u]:.3f}) inputs {np.flatnonzero(A[u, 1:]).tolist()}"
        else:
            beta = pi @ mm
            top = np.argsort(-pi)[:3]
            self.model_desc_ = "; ".join(f"p={pi[u]:.3f} inputs {np.flatnonzero(A[u, 1:]).tolist()}" for u in top)
        self.pi_ = pi
        self.inclusion_ = (pi[:, None] * A[:, 1:]).sum(0)
        self.icpt_, self.coef_ = float(beta[0]), beta[1:].copy()

    def _raw(self, Xr):
        return self.icpt_ + Xr @ self.coef_

    def _linear(self):
        return self.coef_, self.icpt_

    def weights_table(self):
        df = super().weights_table()
        if len(self.selected_):
            for k in range(len(self.selected_)):           # rows: 0 = intercept, k + 1 = selected rule k
                df.loc[k + 1, "meaning"] = df.loc[k + 1, "meaning"] + \
                    f"; posterior inclusion prob {self.inclusion_[k]:.3f}"
            df.attrs["note"] = (f"delta={self.combo_[0]}, lambda={self.combo_[1]} (chosen by one-step-ahead MSE on "
                                f"the last 20% of training days); top models: {self.model_desc_}")
        return df


@register
class StatScreenDMA(_DMABase):
    """Dynamic Model Averaging (Raftery et al. 2010; paper sec. 2.3) over all 2^N subsets of the best N = 10
    survivors (paper uses N in {5, 10, 15}; 15 -> 32,768 models x 16 forgetting pairs is impractical at our row
    count, cf. the paper's own footnote 9 on DMA run time), forgetting factors delta, lambda in {0.90, 0.95, 0.99, 1}
    chosen on the last 20% of training days (paper footnote 6: 'IS in the DMA and DMS cases is the first 80%').
    The DMA forecast is a probability-weighted average of linear models, hence linear in the rule indicators."""
    name = "stat_screen_dma"
    combiner = "Dynamic Model Averaging"
    select = "dma"
    source = SRC_HSS + "; DMA sec. 2.3 (Raftery, Karny & Ettler 2010)"


@register
class StatScreenDMS(_DMABase):
    """Dynamic Model Selection: same recursion as DMA; the forecast uses only the highest-probability model
    (paper sec. 2.3); forgetting pair chosen by the DMS one-step-ahead MSE."""
    name = "stat_screen_dms"
    combiner = "Dynamic Model Selection"
    select = "dms"
    source = SRC_HSS + "; DMS sec. 2.3 (Raftery, Karny & Ettler 2010)"


@register
class StatScreenBMA(_DMABase):
    """Conventional Bayesian Model Averaging = DMA with delta = lambda = 1 (paper sec. 2.3: 'by setting delta = lambda
    = 1, the DMA is simplified to conventional Bayesian Model Averaging') and c = 0 (no flattening)."""
    name = "stat_screen_bma"
    combiner = "Bayesian Model Averaging"
    select = "dma"
    source = SRC_HSS + "; BMA = DMA(delta=lambda=1) sec. 2.3"

    def _combos(self, N):
        return [(1.0, 1.0, 0.0)]


# ---------------------------------------------------------------------------------------------------- A4d. BNN
def _bnn_fit(Xtr, ttr, Xva, tva, H=5, max_epochs=1000, max_fail=6, seed=0):
    """One-hidden-layer tanh network, linear output, trained by Levenberg-Marquardt with Bayesian regularisation
    (MacKay 1992; Foresee & Hagan 1997 Gauss-Newton approximation, as cited by the paper via Ticknor 2013):
    F = beta*E_D + alpha*E_W (paper eq. 25); after each LM step gamma = N_w - 2 alpha tr(H^-1), alpha = gamma /
    (2 E_W), beta = (n - gamma) / (2 E_D), with H = 2 beta J'J + 2 alpha I; start alpha = 0, beta = 1 (Foresee &
    Hagan). Early stopping on a later validation block (paper sec. 2.4: 'the early stopping procedure in the IS is
    applied'). LM mu schedule 0.005 / x0.1 / x10 / max 1e10, epochs 1000, max_fail 6 are MATLAB trainbr/trainlm
    defaults (labelled: from MathWorks documentation, not from the paper)."""
    rng = np.random.default_rng(seed)
    n, d = Xtr.shape
    nw = H * d + 2 * H + 1

    def unpack(th):
        W1 = th[:H * d].reshape(H, d)
        b1 = th[H * d:H * d + H]
        W2 = th[H * d + H:H * d + 2 * H]
        return W1, b1, W2, th[-1]

    def fwd(th, X):
        W1, b1, W2, b2 = unpack(th)
        A = np.tanh(X @ W1.T + b1)
        return A @ W2 + b2, A

    def jac(th, X, A):
        _, _, W2, _ = unpack(th)
        dA = (1 - A ** 2) * W2[None, :]
        return np.hstack([(dA[:, :, None] * X[:, None, :]).reshape(len(X), H * d), dA, A, np.ones((len(X), 1))])

    th = np.concatenate([rng.normal(0, 1 / np.sqrt(d), H * d), rng.normal(0, 0.5, H), rng.normal(0, 0.5, H), [0.0]])
    alpha, beta, mu = 0.0, 1.0, 0.005
    out, A = fwd(th, Xtr)
    e = ttr - out
    ED, EW = e @ e, th @ th
    Fobj = beta * ED + alpha * EW
    best = (np.inf, th.copy())
    fails = 0
    I = np.eye(nw)
    for _ in range(max_epochs):
        J = jac(th, Xtr, A)
        JtJ, Jte = J.T @ J, J.T @ e
        grad = -2 * beta * Jte + 2 * alpha * th
        Hm = 2 * beta * JtJ + 2 * alpha * I
        accepted = False
        while mu <= 1e10:
            step = np.linalg.solve(Hm + mu * I, -grad)
            th_n = th + step
            out_n, A_n = fwd(th_n, Xtr)
            e_n = ttr - out_n
            F_n = beta * (e_n @ e_n) + alpha * (th_n @ th_n)
            if F_n < Fobj:
                th, out, A, e = th_n, out_n, A_n, e_n
                mu *= 0.1
                accepted = True
                break
            mu *= 10
        if not accepted:
            break
        J = jac(th, Xtr, A)
        ED, EW = e @ e, th @ th
        Hm = 2 * beta * (J.T @ J) + 2 * alpha * I
        if alpha > 0:
            gamma = nw - 2 * alpha * np.trace(np.linalg.pinv(Hm))
        else:
            gamma = float(nw)
        gamma = float(np.clip(gamma, 1e-6, nw))
        alpha = gamma / (2 * EW) if EW > 0 else alpha
        beta = (n - gamma) / (2 * ED) if ED > 0 else beta
        Fobj = beta * ED + alpha * EW
        if len(tva):
            v = float(np.mean((tva - fwd(th, Xva)[0]) ** 2))
            if v < best[0] - 1e-12:
                best, fails = (v, th.copy()), 0
            else:
                fails += 1
                if fails >= max_fail:
                    break
        else:
            best = (0.0, th.copy())
    th = best[1] if np.isfinite(best[0]) else th
    return lambda X: fwd(th, X)[0]


@register
class StatScreenBNN(_ScreenBase):
    """Bayesian-regularised neural network (paper sec. 2.4, after Ticknor 2013) on the best N = 15 survivors (the
    paper's best BNN size in Table 6). H = 5 hidden tanh units: labelled fallback from a secondary summary of Ticknor
    (2013) (5 or 20 hidden neurons), not verified against the paper. Inputs mapped 0/1 -> -1/+1 (MATLAB mapminmax
    convention). Compute adaptation: LM runs on <= 20,000 weighted-sampled rows of the first 80% of training time,
    early-stopping on <= 5,000 rows of the last 20% (labelled fallbacks). Nonlinear: weights_table is a flagged
    linearisation."""
    name = "stat_screen_bnn"
    combiner = "Bayesian regularised neural network"
    default_n = 15
    source = SRC_HSS + "; BNN sec. 2.4 (Ticknor 2013; Foresee & Hagan 1997)"

    def _fit_combiner(self, Xr, y, w, meta):
        rng = np.random.default_rng(self.seed + 2)
        n = len(y)
        t = _time_ns(meta, n)
        cut = np.quantile(t, 0.8)
        tr, va = np.flatnonzero(t < cut), np.flatnonzero(t >= cut)
        if len(tr) < 50 or len(va) < 10:
            tr, va = np.arange(n), np.array([], int)
        ntr, nva = int(self.params.get("bnn_rows", 20000)), 5000
        if len(tr) > ntr:
            tr = rng.choice(tr, ntr, replace=True, p=w[tr] / w[tr].sum())
        if len(va) > nva:
            va = rng.choice(va, nva, replace=True, p=w[va] / w[va].sum())
        X2 = 2 * Xr - 1
        self.net_ = _bnn_fit(X2[tr], y[tr], X2[va], y[va], H=int(self.params.get("hidden", 5)),
                             max_epochs=int(self.params.get("epochs", 1000)), seed=self.seed)
        self._fit_rows = Xr[tr]

    def _raw(self, Xr):
        out = np.empty(len(Xr))
        for s in range(0, len(Xr), 200_000):
            out[s:s + 200_000] = self.net_(2 * Xr[s:s + 200_000] - 1)
        return out

    def weights_table(self):
        if len(self.selected_) == 0:
            return self._empty_table()
        return self._linearised_table(self._fit_rows)


# ============================================================================ B/C. binning + weight-of-evidence tools
def _is_discrete(fin, max_vals=5):
    u = np.unique(fin)
    return len(u) <= max_vals, u


class _Binner:
    """Per-column bin codes. Discrete columns (<= 5 distinct values): one class per value. Continuous: equal-frequency
    bins on training quantiles. NaN gets its own class (last code). Unseen discrete values -> NaN class."""

    def __init__(self, v, n_bins):
        fin = v[np.isfinite(v)]
        self.discrete, u = _is_discrete(fin) if fin.size else (True, np.array([]))
        if self.discrete:
            self.values = u
            self.nb = len(u)
        else:
            e = np.unique(np.quantile(fin, np.linspace(0, 1, n_bins + 1)[1:-1]))
            self.edges = e
            self.nb = len(e) + 1

    def codes(self, v):
        nanc = self.nb
        if self.discrete:
            c = np.full(len(v), nanc, np.int64)
            if self.nb:
                i = np.searchsorted(self.values, v)
                i = np.clip(i, 0, self.nb - 1)
                hit = np.isfinite(v) & (self.values[i] == v)
                c[hit] = i[hit]
            return c
        c = np.searchsorted(self.edges, v, side="right").astype(np.int64)
        c[~np.isfinite(v)] = nanc
        return c

    def label(self, k):
        if k == self.nb:
            return "missing"
        if self.discrete:
            return f"= {self.values[k]:+g}" if self.values[k] != 0 else "= 0"
        lo = "-inf" if k == 0 else f"{self.edges[k - 1]:.4g}"
        hi = "+inf" if k == self.nb - 1 else f"{self.edges[k]:.4g}"
        return f"in ({lo}, {hi}]"


def _woe_from_counts(n1, n0, N1, N0):
    """WoE = ln(P(bin|y=1) / P(bin|y=0)) with Laplace add-one smoothing per class (V = number of classes)."""
    V = len(n1)
    return np.log((n1 + 1) / (N1 + V)) - np.log((n0 + 1) / (N0 + V))


# ------------------------------------------------------------------------------------------------- B. stat_nb_woe
@register
class StatNBWoE(Scorer):
    """Naive Bayes as a weight-of-evidence sum (Good 1950, Probability and the Weighing of Evidence; Spiegelhalter &
    Knill-Jones 1984, JRSS A 147:35-77): every feature (binned) contributes WoE = ln(P(bin|y=1)/P(bin|y=0)), Laplace
    add-one smoothing; raw score = ln(prior odds) + sum WoE (assumes conditional independence, so correlated signals
    are double counted). Bins: each value for <= 5-valued features, else training deciles (labelled fallback), NaN
    its own class. score() = Platt map of the raw sum (one global shrinkage factor fitted on training rows)."""
    name = "stat_nb_woe"
    family = "stat"
    source = "Good (1950); Spiegelhalter & Knill-Jones (1984) JRSS A 147:35-77; Laplace add-one smoothing"

    def fit(self, X, y, w=None, meta=None):
        y = np.asarray(y, float)
        w = _weights(w, len(y))
        nb = int(self.params.get("n_bins", 10))
        y1 = y > 0.5
        N1, N0 = w[y1].sum(), w[~y1].sum()
        self.prior_ = float(np.log((N1 + 1) / (N0 + 1)))
        self.cols_, self.bins_, self.woe_, self.share_ = [], [], [], []
        raw = np.full(len(y), self.prior_)
        for c in X.columns:
            v = _col(X, c)
            if not np.isfinite(v).any():
                continue
            b = _Binner(v, nb)
            code = b.codes(v)
            K = b.nb + 1
            n1 = np.bincount(code[y1], w[y1], minlength=K)
            n0 = np.bincount(code[~y1], w[~y1], minlength=K)
            woe = _woe_from_counts(n1, n0, N1, N0)
            if n1[-1] + n0[-1] == 0:
                woe[-1] = 0.0               # never-seen missing class: no evidence
            self.cols_.append(c)
            self.bins_.append(b)
            self.woe_.append(woe)
            self.share_.append((n1 + n0) / (N1 + N0))
            raw += woe[code]
        self.a_, self.b_ = _platt_ab(raw, y, w)
        return self

    def raw_score(self, X):
        raw = np.full(len(X), self.prior_)
        for c, b, woe in zip(self.cols_, self.bins_, self.woe_):
            raw += woe[b.codes(_col(X, c))]
        return raw

    def score(self, X):
        return self.a_ * self.raw_score(X) + self.b_

    def predict_proba(self, X):
        return expit(self.score(X))

    def weights_table(self):
        b0 = self.a_ * self.prior_ + self.b_
        rows = [("prior (base)", b0, _pts(b0), f"calibrated log-odds base; raw prior log-odds {self.prior_:+.3f}, "
                 f"Platt global shrinkage factor a={self.a_:.3f} applied to every WoE", self.source)]
        for c, b, woe, sh in zip(self.cols_, self.bins_, self.woe_, self.share_):
            for k in range(len(woe)):
                if sh[k] == 0:
                    continue
                wt = self.a_ * woe[k]
                rows.append((f"{c} {b.label(k)}", wt, _pts(wt),
                             f"{c} {b.label(k)} ({sh[k]:.1%} of rows): raw WoE {woe[k]:+.3f}; {wt:+.3f} log-odds "
                             f"({_pts(wt):+.1f} pts) toward {_toward(self.task)}", self.source))
        return _wtable(rows)


# ------------------------------------------------------------------------------------------- C. stat_woe_scorecard
def _monotone_merge(n1, n0, min_share, N):
    """Coarse classing of ordered fine classes: (1) pool adjacent violators so the event rate is monotone in the
    direction of its rank correlation with the bin order; (2) merge any class below `min_share` of rows into the
    adjacent class with the closer event rate. Returns a list of index groups."""
    groups = [[i] for i in range(len(n1))]
    g1, g0 = list(n1.astype(float)), list(n0.astype(float))
    tot = np.array(g1) + np.array(g0)
    if len(groups) <= 1 or tot.sum() == 0:
        return groups
    rate = np.where(tot > 0, np.array(g1) / np.maximum(tot, 1e-300), 0.5)
    r = np.corrcoef(np.arange(len(rate)), rate)[0, 1] if np.ptp(rate) > 0 else 1.0
    sgn = 1.0 if (not np.isfinite(r) or r >= 0) else -1.0
    changed = True
    while changed and len(groups) > 1:
        changed = False
        for i in range(len(groups) - 1):
            ra = g1[i] / max(g1[i] + g0[i], 1e-300)
            rb = g1[i + 1] / max(g1[i + 1] + g0[i + 1], 1e-300)
            if sgn * (rb - ra) < 0:
                groups[i] += groups.pop(i + 1)
                g1[i] += g1.pop(i + 1)
                g0[i] += g0.pop(i + 1)
                changed = True
                break
    while len(groups) > 1:
        tot = np.array(g1) + np.array(g0)
        i = int(np.argmin(tot))
        if tot[i] >= min_share * N:
            break
        ri = g1[i] / max(tot[i], 1e-300)
        cand = [j for j in (i - 1, i + 1) if 0 <= j < len(groups)]
        j = min(cand, key=lambda j: abs(g1[j] / max(g1[j] + g0[j], 1e-300) - ri))
        a, b = min(i, j), max(i, j)
        groups[a] += groups.pop(b)
        g1[a] += g1.pop(b)
        g0[a] += g0.pop(b)
    return groups


@register
class StatWoEScorecard(Scorer):
    """Credit-risk scorecard (Siddiqi 2006, Credit Risk Scorecards, Wiley; Anderson 2007, The Credit Scoring
    Toolkit, OUP), 'good' = y = 1 (winning trade / exit beats hold):
      * fine classing: 20 equal-frequency classes for continuous features (labelled fallback: the common '5% fine
        classes' practice, not verified against the book); discrete flags keep one class per value (our choice, so
        rare patterns are not pooled away); missing values a class of their own;
      * coarse classing: adjacent classes merged until the WoE trend is monotone (Siddiqi's 'logical trend',
        operationalised as monotone) and every class holds >= 5% of rows (labelled fallback, unverified);
      * WoE = ln(%good / %bad) per class (Laplace add-one, as stat_nb_woe), IV = sum (%good - %bad) x WoE;
      * IV filter: drop features with IV < 0.02 ('unpredictive', Siddiqi 2006, as quoted by du Pisanie, Allison &
        Visagie 2023, arXiv 2303.01227; bands 0.02-0.1 weak, 0.1-0.3 medium, >= 0.3 strong);
      * logistic regression on the WoE-coded survivors (near-unpenalised, C = 1e6); features whose coefficient comes
        out NEGATIVE (a WoE-coded variable must enter with a positive sign; a reversal signals collinearity) are
        dropped and the model refitted (common scorecard practice; labelled, not verified against the books);
      * scaling: points = Factor x coef x WoE with Factor = PDO / ln 2, PDO = 20 (scorer_api convention; Siddiqi's
        Score = Offset + Factor ln(odds)). Offset is 0 here (the intercept row carries the base points).
    Fits on <= 400,000 weighted-sampled rows when larger (compute fallback)."""
    name = "stat_woe_scorecard"
    family = "stat"
    source = ("Siddiqi (2006) Credit Risk Scorecards, Wiley; Anderson (2007) The Credit Scoring Toolkit; IV cuts via "
              "du Pisanie, Allison & Visagie (2023) arXiv 2303.01227; PDO = 20")

    def fit(self, X, y, w=None, meta=None):
        y = np.asarray(y, float)
        w = _weights(w, len(y))
        fine = int(self.params.get("fine_bins", 20))
        min_share = float(self.params.get("min_share", 0.05))
        self.iv_min = float(self.params.get("iv_min", 0.02))
        y1 = y > 0.5
        N1, N0 = w[y1].sum(), w[~y1].sum()
        N = N1 + N0
        self.cols_all_, self.iv_ = [], {}
        feats = []
        for c in X.columns:
            v = _col(X, c)
            if not np.isfinite(v).any():
                continue
            b = _Binner(v, fine)
            code = b.codes(v)
            K = b.nb + 1
            n1 = np.bincount(code[y1], w[y1], minlength=K)
            n0 = np.bincount(code[~y1], w[~y1], minlength=K)
            if b.discrete:
                groups = [[i] for i in range(b.nb)]
            else:
                groups = _monotone_merge(n1[:-1], n0[:-1], min_share, N)
            gmap = np.empty(K, np.int64)
            for gi, g in enumerate(groups):
                gmap[g] = gi
            gmap[-1] = len(groups)                       # missing class
            G = len(groups) + 1
            c1 = np.bincount(gmap, n1, minlength=G)
            c0 = np.bincount(gmap, n0, minlength=G)
            used = (c1 + c0) > 0
            woe = np.zeros(G)
            woe[used] = _woe_from_counts(c1[used], c0[used], N1, N0)
            p1, p0 = c1[used] / N1, c0[used] / N0
            iv = float(((p1 - p0) * woe[used]).sum())
            self.iv_[c] = iv
            labels = []
            for gi, g in enumerate(groups):
                if b.discrete:
                    labels.append(b.label(g[0]))
                else:
                    lo = "-inf" if g[0] == 0 else f"{b.edges[g[0] - 1]:.4g}"
                    hi = "+inf" if g[-1] == b.nb - 1 else f"{b.edges[g[-1]]:.4g}"
                    labels.append(f"in ({lo}, {hi}]")
            labels.append("missing")
            feats.append(dict(col=c, binner=b, gmap=gmap, woe=woe, share=(c1 + c0) / N, labels=labels, iv=iv))
        self.iv_table_ = pd.DataFrame({"feature": list(self.iv_), "IV": list(self.iv_.values())}).sort_values(
            "IV", ascending=False, ignore_index=True)
        kept = [f for f in feats if f["iv"] >= self.iv_min]
        rng = np.random.default_rng(int(self.params.get("seed", 0)))
        n = len(y)
        mx = int(self.params.get("max_rows", 400_000))
        idx = rng.choice(n, mx, replace=False) if n > mx else np.arange(n)
        self.dropped_negative_ = []
        while kept:
            Z = np.column_stack([f["woe"][f["gmap"][f["binner"].codes(_col(X, f["col"]))[idx]]] for f in kept])
            if len(np.unique(y[idx])) < 2:
                break
            lr = LogisticRegression(C=1e6, max_iter=2000).fit(Z, y[idx], sample_weight=w[idx])
            coef = lr.coef_[0]
            if (coef < 0).any():
                self.dropped_negative_ += [f["col"] for f, cf in zip(kept, coef) if cf < 0]
                kept = [f for f, cf in zip(kept, coef) if cf >= 0]
                continue
            self.coef_, self.icpt_ = coef, float(lr.intercept_[0])
            break
        if not kept:
            self.coef_, self.icpt_ = np.zeros(0), float(_logit(_wmean(y, w)))
        self.feats_ = kept
        return self

    def score(self, X):
        s = np.full(len(X), self.icpt_)
        for f, cf in zip(self.feats_, self.coef_):
            s += cf * f["woe"][f["gmap"][f["binner"].codes(_col(X, f["col"]))]]
        return s

    raw_score = score

    def predict_proba(self, X):
        return expit(self.score(X))

    def weights_table(self):
        rows = [("intercept (base points)", self.icpt_, _pts(self.icpt_),
                 f"base log-odds of {_toward(self.task)}; {len(self.feats_)} features passed IV >= {self.iv_min} and "
                 f"kept a positive coefficient", self.source)]
        for f, cf in zip(self.feats_, self.coef_):
            for gi, lab in enumerate(f["labels"]):
                if f["share"][gi] == 0:
                    continue
                wt = cf * f["woe"][gi]
                rows.append((f"{f['col']} {lab}", wt, _pts(wt),
                             f"{f['col']} {lab} ({f['share'][gi]:.1%} of rows): {round(_pts(wt)):+d} points "
                             f"(WoE {f['woe'][gi]:+.3f} x coef {cf:.3f}; feature IV {f['iv']:.3f}); +20 points "
                             f"doubles the odds of {_toward(self.task)}", self.source))
        return _wtable(rows)


# ---------------------------------------------------------------------------------------------- D. stat_shrink_combo
_FAMILY_MEMBERS = {   # mirrors features.FAMILIES (SPEC.md module 1)
    "reversal": ["hammer", "inverted_hammer", "hanging_man", "shooting_star", "dragonfly_doji", "gravestone_doji",
                 "engulfing", "harami", "piercing", "dark_cloud", "morning_evening_star", "three_inside", "tweezer",
                 "pin_bar"],
    "continuation": ["three_soldiers_crows", "marubozu", "tall_trend_bar"],
    "breakout": ["inside_bar_breakout", "nr7_breakout", "outside_bar"],
    "closeloc": ["clv_extreme", "clv5_extreme", "bar_80_20"],
    "exhaustion": ["five_lower_lows_higher_highs"],
}
_NEUTRAL_PATS = {"doji", "spinning_top", "inside_bar", "nr7"}
_TREND = {"ema_stack", "ema20_slope", "dist_ema8", "dist_ema20", "dist_ema50", "above_ema20_share"}
_MOM = {"mom", "mom_slope3", "mom_x100"}
_BAR = {"rng_rel", "body_frac", "clv", "vol_rel"}
_DAY = {"gap_open", "day_range_rel", "day_ret"}


def signal_family(col: str) -> str:
    """Signal family of a SPEC.md column (the unit whose own forecast enters the combination)."""
    if col.startswith("fam_"):
        return col[4:]
    if col.startswith("pat_"):
        p = col[4:]
        for f, mem in _FAMILY_MEMBERS.items():
            if p in mem:
                return f
        return "neutral_pattern" if p in _NEUTRAL_PATS else "pattern_other"
    if col in EXIT_STATE:
        return "trade_state"
    m = re.match(r"(dist_swhi|dist_swlo|brk|struct|fibpos|atfib)_(\d+)$", col)
    if m:
        return f"swing_{m.group(2)}"
    if col in _TREND:
        return "trend"
    if col in _MOM:
        return "momentum"
    if col == "dist_vwap":
        return "vwap"
    if col in _BAR:
        return "bar"
    if col in _DAY:
        return "day"
    if col.startswith("tod_") or col.startswith("dow_"):
        return "time"
    if col.startswith("h1_"):
        return "htf"
    if col.startswith("x_"):
        return "cross_market"
    return "other"


class _FamilyModel:
    """One family's own forecast: L2 logistic regression (sklearn default C = 1.0, labelled) of y on the family's
    standardised columns; NaN -> 0 for signed columns (has negative values: 0 = neutral), training median otherwise."""

    def __init__(self, cols):
        self.cols = cols

    def _mat(self, X):
        Z = np.column_stack([_col(X, c) for c in self.cols])
        return np.where(np.isfinite(Z), Z, self.fill[None, :])

    def fit(self, X, y, w, idx):
        Z = np.column_stack([_col(X, c)[idx] for c in self.cols])
        fin = np.isfinite(Z)
        neg = np.array([(Z[fin[:, j], j] < 0).any() for j in range(Z.shape[1])])
        med = np.array([np.median(Z[fin[:, j], j]) if fin[:, j].any() else 0.0 for j in range(Z.shape[1])])
        self.fill = np.where(neg, 0.0, med)
        Z = np.where(fin, Z, self.fill[None, :])
        self.mu, sd = Z.mean(0), Z.std(0)
        self.sd = np.where(sd > 1e-12, sd, 1.0)
        yy = y[idx]
        if len(np.unique(yy)) < 2:
            self.beta, self.b0 = np.zeros(len(self.cols)), float(_logit(_wmean(yy, w[idx])))
            return self
        lr = LogisticRegression(C=1.0, max_iter=1000).fit((Z - self.mu) / self.sd, yy, sample_weight=w[idx])
        self.beta = lr.coef_[0] / self.sd                        # per raw unit
        self.b0 = float(lr.intercept_[0] - (lr.coef_[0] * self.mu / self.sd).sum())
        return self

    def logodds(self, X):
        return self.b0 + self._mat(X) @ self.beta


@register
class StatShrinkCombo(Scorer):
    """Forecast combination with shrinkage toward equal weights.

    Each signal family k (signal_family()) gives its own forecast f_k = P(y=1 | family k) (logistic). The combined
    forecast is logistic in the centred family log-odds z_k = logit f_k - logit(base): s = sum_k w_k z_k, then the
    Platt map. Combination weights: logistic-regression ('OLS') weights w_hat on OUT-OF-SAMPLE family forecasts,
    shrunk toward equal weights w0 = 1/K: w = w0 + delta (w_hat - w0), delta in [0, 1] (Diebold & Pauly 1990 Bayes
    posterior mean with the prior centred on the simple average, as restated by Diebold & Shin 2019 IJF 35: beta1 =
    beta0 + delta (beta_OLS - beta0)). delta chosen on an inner purged expanding time split of the TRAINING rows
    (family models fit on A -> forecasts on B -> weights estimated on B; each delta scored by out-of-sample log loss
    on C with family models fit on A+B) -- the task's instruction, instead of Diebold & Pauly's empirical-Bayes
    estimate. Motivation: the forecast-combination puzzle (Smith & Wallis 2009; Claeskens et al. 2016): estimated
    weights often lose to equal weights out of sample. Final: family models refit on all training rows; weights
    re-estimated on the stacked OOS forecasts of B and C and shrunk with the chosen delta. delta grid 0, 0.1, ..., 1
    and the A/B/C split are labelled fallbacks (SPEC.md's 'last 2 training years' when available). Linear: each
    signal's log-odds weight = Platt slope x w_k x its family coefficient."""
    name = "stat_shrink_combo"
    family = "stat"
    source = ("Diebold & Pauly (1990) IJF 6:503-508 (shrink to equal weights; form beta0 + delta(beta_OLS - beta0) per "
              "Diebold & Shin 2019); Smith & Wallis (2009) OBES 71; Claeskens, Magnus, Vasnev & Wang (2016) IJF 32")

    def fit(self, X, y, w=None, meta=None):
        y = np.asarray(y, float)
        w = _weights(w, len(y))
        n = len(y)
        rng = np.random.default_rng(int(self.params.get("seed", 0)))
        mx = int(self.params.get("max_rows", 300_000))
        grid = np.asarray(self.params.get("delta_grid", np.round(np.linspace(0, 1, 11), 2)), float)
        fams: dict[str, list] = {}
        for c in X.columns:
            if np.isfinite(_col(X, c)).any():
                fams.setdefault(signal_family(c), []).append(c)
        self.fam_names_ = sorted(fams)
        K = len(self.fam_names_)
        self.base_ = _wmean(y, w)
        if K == 0:
            self.models_, self.w_, self.a_, self.b_, self.delta_ = [], np.zeros(0), 0.0, float(_logit(self.base_)), 0
            return self

        def sub(idx):
            return rng.choice(idx, mx, replace=False) if len(idx) > mx else idx

        def fit_models(idx):
            return [_FamilyModel(fams[f]).fit(X, y, w, sub(idx)) for f in self.fam_names_]

        def zmat(models, rows, base):
            Xs = X.iloc[rows]
            return np.column_stack([m.logodds(Xs) for m in models]) - _logit(base)

        folds = _inner_folds(meta, n)
        w0 = np.full(K, 1.0 / K)
        self.delta_curve_ = {}
        oos = []
        for tr, te in folds:
            mods = fit_models(tr)
            oos.append((te, zmat(mods, te, _wmean(y[tr], w[tr]))))

        def comb_weights(Z, yy, ww):
            if len(np.unique(yy)) < 2:
                return np.zeros(K)
            lr = LogisticRegression(C=1e6, max_iter=2000).fit(Z, yy, sample_weight=ww)
            return lr.coef_[0]

        if len(oos) == 2:
            (tB, zB), (tC, zC) = oos
            wh = comb_weights(zB, y[tB], w[tB])
            best = (np.inf, 1.0)
            for d in grid:
                wd = w0 + d * (wh - w0)
                a, b = _platt_ab(zB @ wd, y[tB], w[tB])
                pC = np.clip(expit(a * (zC @ wd) + b), 1e-9, 1 - 1e-9)
                yc, wc = y[tC], w[tC]
                ll = float(-(wc * (yc * np.log(pC) + (1 - yc) * np.log(1 - pC))).sum() / wc.sum())
                self.delta_curve_[float(d)] = ll
                if ll < best[0] - 1e-12:
                    best = (ll, float(d))
            self.delta_ = best[1]
        else:
            self.delta_ = 0.0                                   # no honest split possible: equal weights
        if oos:
            te_all = np.concatenate([t for t, _ in oos])
            z_all = np.vstack([z for _, z in oos])
            wh = comb_weights(z_all, y[te_all], w[te_all])
            self.w_hat_ = wh
            self.w_ = w0 + self.delta_ * (wh - w0)
            self.a_, self.b_ = _platt_ab(z_all @ self.w_, y[te_all], w[te_all])
        else:
            self.w_hat_ = w0
            self.w_ = w0
        self.models_ = fit_models(np.arange(n))
        if not oos:
            self.a_, self.b_ = _platt_ab(self._z(X) @ self.w_, y, w)
        return self

    def _z(self, X):
        return np.column_stack([m.logodds(X) for m in self.models_]) - _logit(self.base_)

    def raw_score(self, X):
        if not self.models_:
            return np.zeros(len(X))
        return self._z(X) @ self.w_

    def score(self, X):
        return self.a_ * self.raw_score(X) + self.b_

    def predict_proba(self, X):
        return expit(self.score(X))

    def weights_table(self):
        if not self.models_:
            return _wtable([("intercept", self.b_, _pts(self.b_), "no usable feature", self.source)])
        icpt = self.b_ + self.a_ * sum(wk * (m.b0 - _logit(self.base_)) for wk, m in zip(self.w_, self.models_))
        rows = [("intercept", icpt, _pts(icpt), f"base log-odds of {_toward(self.task)} with every feature at 0 "
                 f"(NaN -> 0 / median); shrinkage delta={self.delta_} (0 = equal weights, 1 = estimated weights)",
                 self.source)]
        for f, wk, wh, m in zip(self.fam_names_, self.w_, self.w_hat_, self.models_):
            rows.append((f"family:{f}", self.a_ * wk, _pts(self.a_ * wk),
                         f"weight on the '{f}' family's own log-odds forecast (equal {1 / len(self.w_):.3f}, "
                         f"estimated {wh:.3f}, shrunk {wk:.3f}, x Platt {self.a_:.3f})", self.source))
            for c, bc in zip(m.cols, m.beta):
                wt = self.a_ * wk * bc
                rows.append((c, wt, _pts(wt), f"{c}: {wt:+.4f} log-odds ({_pts(wt):+.2f} pts) per unit toward "
                             f"{_toward(self.task)} (family '{f}')", self.source))
        return _wtable(rows)


__all__ = ["StatScreenNB", "StatScreenSA", "StatScreenRVM", "StatScreenDMA", "StatScreenDMS", "StatScreenBMA",
           "StatScreenBNN", "StatNBWoE", "StatWoEScorecard", "StatShrinkCombo", "balanced_kstepm",
           "politis_white_block", "stationary_bootstrap_counts", "signal_family"]
