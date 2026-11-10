"""
Published MACHINE-LEARNING confidence scorers, plus ML that STARTS FROM A PRIOR (hand-set or statistical weights).
All classes implement scorer_api.Scorer and are registered in scorer_api.REGISTRY. They work for task="entry" and
task="exit" alike (X arrives oriented by trade direction; for exits y = 1 means "exiting now beat holding", so a high
confidence is evidence AGAINST the open trade). fit() uses only the rows it is given (no look-ahead): every
hyper-parameter and calibration map is chosen on an INNER TIME SPLIT of those rows (later rows validate earlier ones,
purged by label end time), then the model is refit on all given rows.

Registered scorers (details, page references and every adaptation are in ml_NOTES.md):

  ml_logit_l2         StandardScaler + L2 LogisticRegression, C chosen on the inner time split by log loss
                      (the SPEC.md walk-forward 'logit' reference model).
  ml_afml_rf          Lopez de Prado, Advances in Financial Machine Learning (2018): meta-labeling secondary model
                      (ch. 3), uniqueness-based sample weights / bagging (ch. 4), random forest set up as in ch. 6
                      (entropy, class_weight='balanced_subsample', max_samples = average uniqueness, early stopping via
                      min_weight_fraction_leaf, few features per split, 1000 trees), probabilities calibrated
                      (isotonic, as in Meyer, Barziy & Joubert 2023 code) and bet sizing from ch. 10
                      (bet_size(p) = 2*Phi(z) - 1, z = (p - 1/2) / sqrt(p (1 - p))).
  ml_creamer_boost    Creamer & Freund: LogitBoost-grown Alternating Decision Tree over the indicator features
                      (weights w = 1/(1 + exp(y F)), rule values a = 1/2 ln(W+/W-); Freund & Mason 1999 ADT),
                      number of rounds chosen on a later validation block (Creamer 2007 thesis ch. 7), at most 20
                      rounds (Creamer 2012, Euro futures), Platt-calibrated.
  ml_creamer_experts  The same ADTs as "experts" trained on moving 2-year windows, combined with Creamer & Freund's
                      expert-weighting layer (thesis ch. 6, QF 2010): w_i = I_i * ramp * exp(C cart_i / sqrt(n)),
                      C = 1, signal W = L - S in [-1, 1]; gamma0 = 0.20 weak-signal filter exposed by trade_signal().
  prior_logit_offset  logistic regression with OFFSET = the prior's (calibrated) log-odds; the model learns only
                      corrections, Gaussian prior N(0, s^2) on Gelman-scaled inputs (Gelman et al. 2008), s chosen on
                      the inner time split (s -> 0 returns the prior itself).
  prior_logit_shrink  logistic regression whose Gaussian prior is centred on the PRIOR's per-feature log-odds weights
                      (Gelman et al. 2008 sec. 3.1 "informative prior N(mu_j, sigma_j^2)") instead of zero; s chosen on
                      the inner time split.
  prior_gbm           sklearn GradientBoostingClassifier(init=<wrapper of the fitted, calibrated prior>) so boosting
                      starts from the prior's log-odds; shallow trees, shrinkage 0.05, subsample 0.5, number of trees
                      chosen on the inner time split (0 trees allowed = keep the prior).

The prior for prior_* is given by name, e.g. Scorer(task, prior="hand_bulkowski", prior_params={...}); it is built
from scorer_api.REGISTRY (approach_hand / approach_stat are imported on demand) and FIT on the same training rows
inside fit() (and, for the inner split, on the inner-training rows only).

Useful module functions: bet_size(p), label_uniqueness(meta), sequential_bootstrap(t, t_end, n), time_decay(u, t, c),
inner_split(meta, y).
"""
from __future__ import annotations

import copy
import importlib
import math
import warnings

import numpy as np
import pandas as pd
from scipy import optimize, special, stats
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

from scorer_api import REGISTRY, Scorer, register

LN2_20 = math.log(2) / 20          # credit-scorecard scaling: +20 points doubles the odds (scorer_api)
P_EPS = 1e-6
SENTINEL = -1e9                    # NaN code for sklearn GradientBoosting (it rejects NaN): "missing = very low"
YEAR_NS = 365.25 * 86400e9

AFML = "Lopez de Prado (2018) Advances in Financial Machine Learning"
CREAMER = ("Creamer & Freund (2010) Automated trading with boosting and expert weighting, Quant. Finance 10(4); "
           "Creamer (2007) Columbia PhD thesis 'Using boosting for automated planning and trading systems'; "
           "Creamer (2012) Model calibration and automated trading agent for Euro futures, Quant. Finance 12(4); "
           "Freund & Mason (1999) The alternating decision tree learning algorithm, ICML")
GELMAN = "Gelman, Jakulin, Pittau & Su (2008) A weakly informative default prior distribution for logistic regression"


# ============================================================================================ small helpers
def _sig(z):
    return special.expit(z)


def _logit(p):
    p = np.clip(np.asarray(p, float), P_EPS, 1 - P_EPS)
    return np.log(p / (1 - p))


def _weights(w, n):
    if w is None:
        return np.ones(n)
    w = np.asarray(w, float).copy()
    w[~np.isfinite(w) | (w < 0)] = 0.0
    return w if w.sum() > 0 else np.ones(n)


def wlogloss(y, p, w=None):
    y = np.asarray(y, float)
    p = np.clip(np.asarray(p, float), P_EPS, 1 - P_EPS)
    w = _weights(w, len(y))
    return float(np.sum(w * -(y * np.log(p) + (1 - y) * np.log(1 - p))) / w.sum())


def _ts(s) -> np.ndarray:
    """Timestamps -> float64 nanoseconds (tz-aware ok); numeric columns pass through."""
    s = pd.Series(s)
    if pd.api.types.is_numeric_dtype(s):
        return s.to_numpy(np.float64)
    return pd.DatetimeIndex(pd.to_datetime(s)).as_unit("ns").asi8.astype(np.float64)


def _has(meta, *cols):
    return meta is not None and all(c in meta.columns for c in cols)


def _pnl(meta):
    if meta is None:
        return None
    for c in ("pnl_usd", "exit_gain_usd"):
        if c in meta.columns:
            v = pd.to_numeric(meta[c], errors="coerce").to_numpy(float)
            if np.isfinite(v).any():
                return np.nan_to_num(v)
    return None


def _rows(df, idx):
    return None if df is None else df.iloc[idx]


def _subsample(n, max_rows, seed):
    if max_rows is None or n <= max_rows:
        return np.arange(n)
    return np.sort(np.random.default_rng(seed).choice(n, int(max_rows), replace=False))


# ============================================================================================ AFML ch. 4 / ch. 10
def label_uniqueness(meta: pd.DataFrame, by: str = "market") -> np.ndarray:
    """AFML ch. 4.3-4.4 (snippets 4.1-4.2): uniqueness of label i = average over its lifespan [t_i, t_end_i] of
    1 / c(tau), c = number of labels (same market) alive at tau. The book averages over bars; we average over clock
    time (continuous-time version, no bar grid needed). Returns 1.0 for everything if t / t_end are missing."""
    n = 0 if meta is None else len(meta)
    if not _has(meta, "t", "t_end"):
        return np.ones(n)
    t, te = _ts(meta["t"]), _ts(meta["t_end"])
    te = np.where(np.isfinite(te), te, t)
    te = np.maximum(te, t + 1.0)                                    # zero-length labels get 1 ns
    grp = pd.factorize(meta[by])[0] if by in meta.columns else np.zeros(n, int)
    out = np.ones(n)
    for g in np.unique(grp):
        idx = np.flatnonzero(grp == g)
        s, e = t[idx], te[idx]
        bp = np.unique(np.concatenate([s, e]))
        c = np.searchsorted(np.sort(s), bp[:-1], "right") - np.searchsorted(np.sort(e), bp[:-1], "right")
        inv = np.where(c > 0, 1.0 / np.maximum(c, 1), 0.0)
        integ = np.concatenate([[0.0], np.cumsum(inv * np.diff(bp))])
        out[idx] = (integ[np.searchsorted(bp, e)] - integ[np.searchsorted(bp, s)]) / (e - s)
    return np.clip(out, 0.0, 1.0)


def time_decay(u: np.ndarray, t: np.ndarray, last_w: float = 1.0) -> np.ndarray:
    """AFML ch. 4.7 (snippet 4.11 getTimeDecay): piecewise-linear decay on CUMULATIVE uniqueness in time order; the
    newest observation gets weight 1, the oldest last_w (1.0 = no decay; negative values zero out the oldest part)."""
    u = np.asarray(u, float)
    if last_w == 1.0 or len(u) == 0:
        return np.ones(len(u))
    order = np.argsort(t, kind="stable")
    cum = np.empty(len(u))
    cum[order] = np.cumsum(u[order])
    tot = cum[order[-1]]
    slope = (1.0 - last_w) / tot if last_w >= 0 else 1.0 / ((last_w + 1.0) * tot)
    const = 1.0 - slope * tot
    return np.maximum(const + slope * cum, 0.0)


def sequential_bootstrap(t, t_end, n_draws: int | None = None, rng=None) -> np.ndarray:
    """AFML ch. 4.5 (snippets 4.5-4.6 seqBootstrap): draw labels one at a time with probability proportional to the
    average uniqueness each label WOULD have given the labels drawn so far, so overlapping labels are rarely drawn
    together. Continuous-time version (time-weighted average uniqueness). Cost O(n_draws * n): use on samples of up to
    a few thousand labels (the book's method is not practical at 1M rows - see ml_NOTES.md)."""
    rng = np.random.default_rng(rng)
    t, te = np.asarray(t, float), np.asarray(t_end, float)
    te = np.maximum(te, t + 1.0)
    n = len(t)
    n_draws = n if n_draws is None else int(n_draws)
    bp = np.unique(np.concatenate([t, te]))
    dt = np.diff(bp)
    a, b = np.searchsorted(bp, t), np.searchsorted(bp, te)            # label i covers segments a_i .. b_i - 1
    life = te - t
    c = np.zeros(len(dt))
    out = np.empty(n_draws, int)
    for k in range(n_draws):
        integ = np.concatenate([[0.0], np.cumsum(dt / (c + 1.0))])
        u = (integ[b] - integ[a]) / life
        i = rng.choice(n, p=u / u.sum())
        out[k] = i
        c[a[i]:b[i]] += 1.0
    return out


def bet_size(p, num_classes: int = 2, step: float | None = None, meta_label: bool = True) -> np.ndarray:
    """AFML ch. 10.3 (snippet 10.1 getSignal): z = (p - 1/numClasses) / sqrt(p (1 - p)), size = 2 Phi(z) - 1.
    With meta-labeling the side comes from the primary rule, so a size below 0 means 'pass' -> clipped to 0 (the
    Hudson & Thames calibration code clips the same way). step: AFML snippet 10.3 discreteSignal (round to steps)."""
    p = np.clip(np.asarray(p, float), P_EPS, 1 - P_EPS)
    m = 2.0 * stats.norm.cdf((p - 1.0 / num_classes) / np.sqrt(p * (1 - p))) - 1.0
    if meta_label:
        m = np.clip(m, 0.0, 1.0)
    if step:
        m = np.clip(np.round(m / step) * step, -1.0, 1.0)
    return m


# ============================================================================================ inner time split
def inner_split(meta: pd.DataFrame | None, y, frac: float = 0.25, min_rows: int = 30):
    """(train_idx, val_idx) of an inner TIME split of the training rows, used to choose hyper-parameters and fit the
    calibration map (SPEC.md walkforward 'logit': inner time split on the last 2 training years).
    * meta has >= 4 distinct years: validate on the last 2 years; 2-3 years: the last year;
    * otherwise: the last `frac` of rows by time (meta t, else row order).
    Purge (AFML ch. 7.4): inner-training rows whose label ends (t_end) at or after the first validation t are dropped."""
    y = np.asarray(y)
    n = len(y)
    t = _ts(meta["t"]) if _has(meta, "t") else np.arange(n, dtype=float)

    def by_frac():
        order = np.argsort(t, kind="stable")
        v = np.zeros(n, bool)
        v[order[int(round(n * (1 - frac))):]] = True
        return v

    val = None
    if _has(meta, "year"):
        yr = pd.to_numeric(meta["year"], errors="coerce").to_numpy()
        yrs = np.unique(yr[np.isfinite(yr)])
        if len(yrs) >= 2:
            val = np.isin(yr, yrs[-2:] if len(yrs) >= 4 else yrs[-1:])
    if val is None:
        val = by_frac()

    def finish(val):
        tr = ~val
        if _has(meta, "t_end") and val.any():
            te = _ts(meta["t_end"])
            tr &= ~(te >= t[val].min())
        return tr

    tr = finish(val)
    if tr.sum() < min_rows or val.sum() < min_rows or len(np.unique(y[val])) < 2 or len(np.unique(y[tr])) < 2:
        val = by_frac()
        tr = finish(val)
    return np.flatnonzero(tr), np.flatnonzero(val)


# ============================================================================================ preprocessing
class _Imputer:
    """Median imputation with TRAINING medians (all-NaN column -> 0)."""

    def fit(self, A):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            med = np.nanmedian(A, axis=0)
        self.med = np.where(np.isfinite(med), med, 0.0)
        return self

    def transform(self, A):
        A = np.array(A, float, copy=True)
        bad = ~np.isfinite(A)
        if bad.any():
            A[bad] = np.broadcast_to(self.med, A.shape)[bad]
        return A


class _GelmanScaler:
    """Gelman et al. (2008) sec. 2.1: binary inputs shifted to mean 0 and differing by 1 between their two values;
    other inputs shifted to mean 0 and scaled to standard deviation 0.5. Constant columns: centred only."""

    def fit(self, A):
        self.center = A.mean(axis=0)
        self.scale = np.ones(A.shape[1])
        self.binary = np.zeros(A.shape[1], bool)
        for j in range(A.shape[1]):
            col = A[:, j]
            lo, hi = col.min(), col.max()
            if hi > lo and np.all((col == lo) | (col == hi)):
                self.binary[j] = True
                self.scale[j] = hi - lo
            else:
                sd = A[:, j].std()
                self.scale[j] = 2 * sd if sd > 1e-12 else 1.0
        return self

    def transform(self, A):
        return (A - self.center) / self.scale


class _Calib:
    """Monotone score -> probability map fitted on held-out (inner-validation) rows: 'platt' (Platt 1999; scorer_api)
    or 'isotonic' (Zadrozny & Elkan 2002; used by Meyer, Barziy & Joubert 2023)."""

    def __init__(self, kind="platt"):
        self.kind = kind
        self.a, self.b = 1.0, 0.0
        self.iso = None

    def fit(self, s, y, w=None):
        s, y = np.asarray(s, float), np.asarray(y, float)
        w = _weights(w, len(y))
        if len(np.unique(y)) < 2:                                 # degenerate: keep the identity log-odds map
            return self
        if self.kind == "isotonic":
            self.iso = IsotonicRegression(y_min=P_EPS, y_max=1 - P_EPS, out_of_bounds="clip").fit(s, y, sample_weight=w)
        self.a, self.b = _platt_ab(s, y, w)
        return self

    def __call__(self, s):
        s = np.asarray(s, float)
        if self.iso is not None:
            return np.clip(self.iso.predict(s), 0.0, 1.0)
        return _sig(self.a * s + self.b)


def _platt_ab(s, y, w):
    """Weighted 1-d logistic fit P = sigmoid(a s + b) by Newton steps (tiny ridge for separable data)."""
    a, b = 0.0, float(_logit(np.sum(w * y) / np.sum(w)))
    sd = s.std() or 1.0
    for _ in range(50):
        p = _sig(a * s + b)
        r = w * (p - y)
        h = w * p * (1 - p) + 1e-12
        g = np.array([np.sum(r * s) + 1e-6 * a * sd * sd, np.sum(r)])
        H = np.array([[np.sum(h * s * s) + 1e-6 * sd * sd, np.sum(h * s)], [np.sum(h * s), np.sum(h)]])
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        a, b = a - step[0], b - step[1]
        if np.max(np.abs(step)) < 1e-9:
            break
    return float(a), float(b)


# ============================================================================================ MAP logistic regression
def map_logit(Z, y, w, offset=None, mu=None, s=1.0, dist="normal", theta0=None, maxiter=1000):
    """Posterior mode of a logistic regression with an optional OFFSET and independent priors on the slopes centred at
    mu: 'normal' N(mu_j, s^2) (Gelman et al. 2008 sec. 3.1) or 'cauchy' with scale s (their default family, sec. 2.2).
    The intercept is unpenalized. Weighted negative log-likelihood; L-BFGS (scipy). Returns (b0, beta)."""
    n, k = Z.shape
    off = np.zeros(n) if offset is None else np.asarray(offset, float)
    mu = np.zeros(k) if mu is None else np.asarray(mu, float)
    W = w.sum()
    s2 = float(s) ** 2

    def f(theta):
        b0, beta = theta[0], theta[1:]
        eta = Z @ beta + b0 + off
        nll = np.dot(w, np.logaddexp(0.0, eta) - y * eta)
        r = w * (_sig(eta) - y)
        d = beta - mu
        if dist == "cauchy":
            pen = np.sum(np.log1p(d * d / s2))
            gp = 2.0 * d / (s2 + d * d)
        else:
            pen = 0.5 * np.dot(d, d) / s2
            gp = d / s2
        return (nll + pen) / W, np.concatenate([[r.sum()], Z.T @ r + gp]) / W

    if theta0 is None:
        p0 = np.clip(np.sum(w * y) / W, 1e-3, 1 - 1e-3)
        theta0 = np.concatenate([[math.log(p0 / (1 - p0)) - (np.average(off, weights=w) if offset is not None else 0.0)],
                                 mu])
    res = optimize.minimize(f, theta0, jac=True, method="L-BFGS-B",
                            options={"maxiter": maxiter, "gtol": 1e-7, "ftol": 1e-12})
    return float(res.x[0]), res.x[1:].copy()


# ============================================================================================ readable weights
_R20 = ("dist_", "ema20_slope", "day_ret", "gap_open", "rng_rel")


def _unit(col):
    if col.startswith(("pat_", "fam_")):
        return "when it fires (+1 = with the trade)"
    if col.startswith(("brk_", "struct_", "mom_x100")) or col.endswith("ema_stack"):
        return "per step (+1 = with the trade)"
    if col.startswith(("tod_", "dow_", "atfib_")):
        return "when true"
    if col.startswith(_R20) or (col.startswith("x_") and col.endswith("_ret")):
        return "per 1 average bar (R20)"
    if col in ("open_R", "mfe_R", "mae_R", "dist_stop_R"):
        return "per 1 R of the open trade"
    if col == "bars_held":
        return "per bar held"
    if col == "mins_to_1645":
        return "per minute left to 16:45"
    return "per unit"


def _meaning(col, beta, task):
    what = "the chance the trade pays" if task == "entry" else "the case for exiting now"
    if not np.isfinite(beta) or abs(beta) < 1e-12:
        return f"{_unit(col)}: no effect on {what}"
    return f"{_unit(col)}: {'raises' if beta > 0 else 'lowers'} {what} (odds x{math.exp(beta):.2f})"


def _linear_table(cols, beta_raw, task, source, extra=None):
    beta_raw = np.asarray(beta_raw, float)
    df = pd.DataFrame({"signal": list(cols), "weight": beta_raw, "points": np.round(beta_raw / LN2_20, 1),
                       "meaning": [_meaning(c, b, task) for c, b in zip(cols, beta_raw)], "source": source})
    for k, v in (extra or {}).items():
        df[k] = v
    return df.reindex(df["weight"].abs().sort_values(ascending=False).index).reset_index(drop=True)


# ============================================================================================ base class
class _MLBase(Scorer):
    family = "ml"

    def _setup(self, X):
        X = X if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        self.columns_ = list(X.columns)
        return X

    def _align(self, X):
        X = X if isinstance(X, pd.DataFrame) else pd.DataFrame(X, columns=self.columns_)
        if list(X.columns) != self.columns_:
            X = X.reindex(columns=self.columns_)
        return X

    def _arr(self, X):
        return self._align(X).to_numpy(np.float64, na_value=np.nan)

    def p(self, key, default):
        return self.params.get(key, default)


# ============================================================================================ 0) reference logit
@register
class LogitL2(_MLBase):
    name = "ml_logit_l2"
    source = ("SPEC.md walk-forward 'logit': StandardScaler + L2 LogisticRegression (scikit-learn), C chosen on an "
              "inner time split (last 2 training years) by log loss")

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, int)
        w = _weights(w, len(y))
        A = X.to_numpy(np.float64, na_value=np.nan)
        tr, va = inner_split(meta, y)
        grid = self.p("C_grid", (1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0))
        prep = self._prep(A[tr])
        Ztr, Zva = prep(A[tr]), prep(A[va])
        self.val_loss_ = {}
        for C in grid:
            m = LogisticRegression(C=C, max_iter=2000).fit(Ztr, y[tr], sample_weight=w[tr])
            self.val_loss_[C] = wlogloss(y[va], m.predict_proba(Zva)[:, 1], w[va])
        self.C_ = min(self.val_loss_, key=self.val_loss_.get)
        self.prep_ = self._prep(A)
        self.model_ = LogisticRegression(C=self.C_, max_iter=2000).fit(self.prep_(A), y, sample_weight=w)
        return self

    def _prep(self, A):
        imp = _Imputer().fit(A)
        B = imp.transform(A)
        mu, sd = B.mean(0), B.std(0)
        sd = np.where(sd > 1e-12, sd, 1.0)
        f = lambda Q: (imp.transform(Q) - mu) / sd
        f.sd = sd
        return f

    def score(self, X):
        return self.model_.decision_function(self.prep_(self._arr(X)))

    def predict_proba(self, X):
        return self.model_.predict_proba(self.prep_(self._arr(X)))[:, 1]

    def weights_table(self):
        b_std = self.model_.coef_[0]
        return _linear_table(self.columns_, b_std / self.prep_.sd, self.task, f"learned (L2 logit, C={self.C_:g})",
                             {"weight_std": b_std})


# ============================================================================================ 1) AFML meta-labeling RF
@register
class AFMLRandomForest(_MLBase):
    name = "ml_afml_rf"
    source = (f"{AFML}: ch. 3.6 meta-labeling (secondary model sizes/filters a primary rule's bets); ch. 4 sample "
              "weights by average uniqueness + bagging with max_samples = average uniqueness; ch. 6.4 RF set-up "
              "(criterion='entropy', class_weight='balanced_subsample', low max_features, min_weight_fraction_leaf "
              "early stopping, n_estimators=1000; Snippet 6.2); ch. 10.3 bet sizing 2*Phi(z)-1. Calibration: "
              "isotonic, Meyer, Barziy & Joubert (2023) JFDS 5(2) code")

    DEFAULTS = dict(n_estimators=1000, criterion="entropy", class_weight="balanced_subsample", max_features="sqrt",
                    min_weight_fraction_leaf=0.05, bootstrap="avgU", calib="isotonic", time_decay=1.0,
                    return_attribution=False, max_rows=None, min_tree_rows=200, seq_max_rows=3000, n_jobs=-1,
                    random_state=0)

    def p(self, key, default=None):
        return self.params.get(key, self.DEFAULTS.get(key, default))

    def _sample_weight(self, w, meta, n):
        sw = _weights(w, n)
        u = label_uniqueness(meta)
        if self.p("time_decay") != 1.0 and _has(meta, "t"):
            sw = sw * time_decay(u, _ts(meta["t"]), self.p("time_decay"))
        pnl = _pnl(meta)
        if self.p("return_attribution") and pnl is not None:     # AFML ch. 4.6: weight ~ |return| attributed
            sw = sw * np.abs(pnl) / max(np.mean(np.abs(pnl)), 1e-12)
        return sw, (float(np.mean(u)) if _has(meta, "t", "t_end") else 1.0)

    def _forest(self, avgU, n):
        """max_samples is passed as an INT number of draws = avgU x n (AFML: bag size = average uniqueness x number
        of observations), floored at min_tree_rows. Reason: in scikit-learn 1.9 a FLOAT max_samples is relative to
        sample_weight.sum() (not n) when weights are given, and with uniqueness weights (mean ~ avgU) that would give
        avgU^2 x n draws. scikit-learn 1.9 also draws bootstrap rows with probability proportional to sample_weight
        and fits each tree on the draw counts (x balanced_subsample class weights), so the uniqueness weights act
        through the sampling - AFML's own intent for bagging under overlapping labels (ch. 4.5)."""
        n_boot = int(np.clip(round(max(avgU * n, self.p("min_tree_rows"))), 1, max(n, 1)))
        return RandomForestClassifier(
            n_estimators=self.p("n_estimators"), criterion=self.p("criterion"), max_features=self.p("max_features"),
            class_weight=self.p("class_weight"), min_weight_fraction_leaf=self.p("min_weight_fraction_leaf"),
            bootstrap=True, max_samples=n_boot, n_jobs=self.p("n_jobs"),
            random_state=self.p("random_state"))

    def _fit_one(self, X, y, w, meta):
        n = len(y)
        keep = _subsample(n, self.p("max_rows"), self.p("random_state"))
        if len(keep) < n:
            X, y, meta, w = X.iloc[keep], y[keep], _rows(meta, keep), None if w is None else w[keep]
        sw, avgU = self._sample_weight(w, meta, len(y))
        if self.p("bootstrap") == "sequential" and _has(meta, "t", "t_end"):
            return _SeqBootForest(self, avgU).fit(X, y, sw, meta), avgU
        return self._forest(avgU, len(y)).fit(X, y, sample_weight=sw), avgU

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, int)
        w = None if w is None else np.asarray(w, float)
        tr, va = inner_split(meta, y)
        m_in, _ = self._fit_one(X.iloc[tr], y[tr], None if w is None else w[tr], _rows(meta, tr))
        self.cal_ = _Calib(self.p("calib")).fit(m_in.predict_proba(X.iloc[va])[:, 1], y[va],
                                                 None if w is None else w[va])
        self.model_, self.avgU_ = self._fit_one(X, y, w, meta)
        self._train_sample = X.iloc[_subsample(len(X), 20000, 1)]
        return self

    def _raw(self, X):
        return self.model_.predict_proba(self._align(X))[:, 1]

    def score(self, X):
        return _logit(self._raw(X))

    def predict_proba(self, X):
        return self.cal_(self._raw(X))

    def bet_size(self, X, step=None):
        """AFML ch. 10 size in [0, 1] from the calibrated probability (0 = pass)."""
        return bet_size(self.predict_proba(X), step=step)

    def weights_table(self):
        est = getattr(self.model_, "estimators_", [])
        imp = np.array([e.feature_importances_ for e in est]) if len(est) else np.zeros((1, len(self.columns_)))
        mean, sd = imp.mean(0), imp.std(0) * len(imp) ** -0.5            # AFML snippet 8.2 (MDI) mean, std/sqrt(n)
        tot = mean.sum() or 1.0
        Xs = self._train_sample
        s = self.score(Xs)
        sign = []
        for c in self.columns_:
            v = Xs[c].to_numpy(float)
            ok = np.isfinite(v)
            r = stats.spearmanr(v[ok], s[ok])[0] if ok.sum() > 10 and np.nanstd(v[ok]) > 0 else np.nan
            sign.append(r)
        what = "the chance the trade pays" if self.task == "entry" else "the case for exiting now"
        mean_n = mean / tot
        df = pd.DataFrame({
            "signal": self.columns_, "weight": mean_n, "points": np.nan,
            "meaning": [f"MDI importance {m:.1%} (NOT a log-odds weight); higher values tend to "
                        f"{'raise' if np.nan_to_num(r) > 0 else 'lower'} {what} (Spearman {r:+.2f})"
                        for m, r in zip(mean_n, sign)],
            "source": f"feature importance (MDI, AFML snippet 8.2) of the {len(imp)}-tree forest; avgU={self.avgU_:.3f}",
            "importance_se": sd / tot, "direction_spearman": sign})
        return df.sort_values("weight", ascending=False).reset_index(drop=True)


class _SeqBootForest:
    """AFML ch. 6.4 item 5 / ch. 4.5: bagged entropy trees whose bootstrap samples are drawn by the SEQUENTIAL
    bootstrap. Each tree draws from a random subset of at most seq_max_rows labels (the exact method is O(n^2))."""

    def __init__(self, owner, avgU):
        self.o, self.avgU = owner, avgU

    def fit(self, X, y, sw, meta):
        from sklearn.tree import DecisionTreeClassifier
        o = self.o
        rng = np.random.default_rng(o.p("random_state"))
        t, te = _ts(meta["t"]), _ts(meta["t_end"])
        n = len(y)
        m = min(n, o.p("seq_max_rows"))
        self.estimators_ = []
        A = X
        for k in range(int(o.p("n_estimators"))):
            pool = rng.choice(n, m, replace=False) if m < n else np.arange(n)
            draw = pool[sequential_bootstrap(t[pool], te[pool], m, rng)]
            cnt = np.bincount(draw, minlength=n).astype(float)
            idx = np.flatnonzero(cnt)
            if len(np.unique(y[idx])) < 2:
                continue
            tree = DecisionTreeClassifier(criterion=o.p("criterion"), max_features=o.p("max_features"),
                                          class_weight="balanced", min_weight_fraction_leaf=o.p("min_weight_fraction_leaf"),
                                          random_state=int(rng.integers(1 << 30)))
            self.estimators_.append(tree.fit(A.iloc[idx], y[idx], sample_weight=sw[idx] * cnt[idx]))
        return self

    def predict_proba(self, X):
        p = np.mean([e.predict_proba(X)[:, list(e.classes_).index(1)] if 1 in e.classes_ else np.zeros(len(X))
                     for e in self.estimators_], axis=0)
        return np.column_stack([1 - p, p])


# ============================================================================================ 2) Creamer & Freund
class _Binner:
    """Candidate thresholds per feature: midpoints between distinct values when a feature has <= n_bins values
    (pattern flags keep every split), else training quantiles. Code 0 = missing, codes 1.. = bins; the rule
    'x < e_k' is 'code <= k'."""

    def __init__(self, n_bins=32):
        self.n_bins = n_bins

    def fit(self, A):
        qs = np.linspace(0, 1, self.n_bins + 1)[1:-1]
        self.edges = []
        for j in range(A.shape[1]):
            v = A[:, j][np.isfinite(A[:, j])]
            u = np.unique(v)
            if len(u) <= 1:
                e = np.array([])
            elif len(u) <= self.n_bins:
                e = (u[:-1] + u[1:]) / 2
            else:
                e = np.unique(np.quantile(v, qs))
                e = e[(e > u[0])]                                    # 'x < e' must leave something on the left
            self.edges.append(e.astype(float))
        self.n_edges = np.array([len(e) for e in self.edges])
        self.nb = self.n_bins + 1
        return self

    def transform(self, A):
        B = np.zeros(A.shape, np.uint8)
        for j, e in enumerate(self.edges):
            col = A[:, j]
            ok = np.isfinite(col)
            B[ok, j] = 1 + np.searchsorted(e, col[ok], "right")
        return B


class ADTLogitBoost:
    """Alternating decision tree (Freund & Mason 1999) grown by LogitBoost as in Creamer & Freund (Creamer 2007 thesis
    fig. 2.2): each round, example weights w_i = s_i / (1 + exp(y_i F(x_i))) (y in {-1,+1}, s_i = sample weight);
    choose the precondition c1 (any existing prediction node) and condition c2 = 'x_j < thr' minimising
    Z = 2 (sqrt(W+(c1&c2) W-(c1&c2)) + sqrt(W+(c1&~c2) W-(c1&~c2))) + W(~c1); add the two prediction nodes with values
    a = 1/2 ln((W+ + eps) / (W- + eps)); F += a for rows reaching them. Missing values abstain (do not descend).
    eps = eps_frac x the current mean example weight (smoothing of Schapire & Singer 1999; see ml_NOTES.md).
    single_splitter=True: a prediction node may carry only one splitter (Creamer thesis sec. 2.2.4 wording; faster);
    False (default): Freund & Mason's original, any prediction node may take further splitters."""

    def __init__(self, n_rounds=20, eps_frac=0.5, single_splitter=False):
        self.n_rounds, self.eps_frac, self.single_splitter = n_rounds, eps_frac, single_splitter

    def fit(self, B, y01, sw, n_edges, nb, val=None):
        n, F = B.shape
        y = np.where(np.asarray(y01) > 0, 1.0, -1.0)
        keys = ((B.astype(np.int32) + (np.arange(F, dtype=np.int32) * nb)[None, :]) * 2
                + (y > 0).astype(np.int32)[:, None])
        size = F * nb * 2
        kk = np.arange(1, nb - 1)
        invalid = kk[None, :] > n_edges[:, None]                       # split index beyond this feature's edges
        Fs = np.zeros(n)
        w = sw / 2.0
        eps = self.eps_frac * w.mean()
        self.a0 = 0.5 * math.log((w[y > 0].sum() + eps) / (w[y < 0].sum() + eps))
        Fs += self.a0
        pres = [np.arange(n)]
        self.rules = []
        staged = []
        if val is not None:
            Bv = val
            Fv = np.full(len(Bv), self.a0)
            pres_v = [np.arange(len(Bv))]
        for _ in range(self.n_rounds):
            w = sw / (1.0 + np.exp(np.clip(y * Fs, -50, 50)))
            Wtot = w.sum()
            eps = self.eps_frac * Wtot / n
            best = (np.inf,)
            used = {r[0] for r in self.rules} if self.single_splitter else ()
            for pid, idx in enumerate(pres):
                if len(idx) < 2 or pid in used:
                    continue
                H = np.bincount(keys[idx].ravel(), weights=np.repeat(w[idx], F), minlength=size).reshape(F, nb, 2)
                Cm, Cp = np.cumsum(H[:, 1:, 0], axis=1), np.cumsum(H[:, 1:, 1], axis=1)
                Tm, Tp = Cm[:, -1:], Cp[:, -1:]
                Lm, Lp = Cm[:, :-1], Cp[:, :-1]
                Rm, Rp = Tm - Lm, Tp - Lp
                Z = 2.0 * (np.sqrt(np.maximum(Lp * Lm, 0)) + np.sqrt(np.maximum(Rp * Rm, 0))) + (Wtot - Tp - Tm)
                Z[invalid | ((Lp + Lm) <= 0) | ((Rp + Rm) <= 0)] = np.inf
                j, k0 = np.unravel_index(np.argmin(Z), Z.shape)
                if Z[j, k0] < best[0] - 1e-12 * Wtot:
                    best = (Z[j, k0], pid, j, k0 + 1, Lp[j, k0], Lm[j, k0], Rp[j, k0], Rm[j, k0])
            if not np.isfinite(best[0]):
                break
            _, pid, j, k, lp, lm, rp, rm = best
            aL = 0.5 * math.log((lp + eps) / (lm + eps))
            aR = 0.5 * math.log((rp + eps) / (rm + eps))
            idx = pres[pid]
            c = B[idx, j]
            L, R = idx[(c >= 1) & (c <= k)], idx[c > k]
            Fs[L] += aL
            Fs[R] += aR
            pres += [L, R]
            self.rules.append((pid, int(j), int(k), aL, aR))
            if val is not None:
                iv = pres_v[pid]
                cv = Bv[iv, j]
                Lv, Rv = iv[(cv >= 1) & (cv <= k)], iv[cv > k]
                Fv[Lv] += aL
                Fv[Rv] += aR
                pres_v += [Lv, Rv]
                staged.append(Fv.copy())
        self.staged_val = staged
        return self

    def decision_function(self, B, n_rules=None):
        F = np.full(len(B), self.a0)
        pres = [np.arange(len(B))]
        for pid, j, k, aL, aR in self.rules[: n_rules if n_rules is not None else len(self.rules)]:
            idx = pres[pid]
            c = B[idx, j]
            L, R = idx[(c >= 1) & (c <= k)], idx[c > k]
            F[L] += aL
            F[R] += aR
            pres += [L, R]
        return F

    def describe(self, cols, edges):
        text = ["(always)"]
        rows = [("(always)", self.a0, 0)]
        for r, (pid, j, k, aL, aR) in enumerate(self.rules):
            thr = edges[j][k - 1]
            pre = "" if pid == 0 else text[pid] + " & "
            l, rr = f"{pre}{cols[j]} < {thr:.4g}", f"{pre}{cols[j]} >= {thr:.4g}"
            text += [l, rr]
            rows += [(l, aL, r + 1), (rr, aR, r + 1)]
        return rows


@register
class CreamerFreundBoost(_MLBase):
    name = "ml_creamer_boost"
    source = (f"{CREAMER}. LogitBoost-grown alternating decision tree over the indicator features; rounds chosen on a "
              "later validation block (thesis ch. 7), max 20 rounds (Creamer 2012 sec. 6.1); Platt calibration")
    DEFAULTS = dict(max_rounds=20, rounds=None, n_bins=32, max_rows=100_000, eps_frac=0.5, calib="platt",
                    single_splitter=False, random_state=0)

    def p(self, key, default=None):
        return self.params.get(key, self.DEFAULTS.get(key, default))

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, int)
        w = _weights(w, len(y))
        A = X.to_numpy(np.float64, na_value=np.nan)
        self.binner_ = _Binner(self.p("n_bins")).fit(A[_subsample(len(A), 200_000, self.p("random_state"))])
        B = self.binner_.transform(A)
        tr, va = inner_split(meta, y)
        tr = tr[_subsample(len(tr), self.p("max_rows"), self.p("random_state"))]
        T = self.p("rounds")
        m_in = ADTLogitBoost(T or self.p("max_rounds"), self.p("eps_frac"), self.p("single_splitter")).fit(
            B[tr], y[tr], w[tr], self.binner_.n_edges, self.binner_.nb, val=B[va])
        losses = []
        for Fv in m_in.staged_val:                                     # Platt-calibrated validation log loss
            cal = _Calib("platt").fit(Fv, y[va], w[va])
            losses.append(wlogloss(y[va], cal(Fv), w[va]))
        self.val_loss_ = losses
        if T is None:
            T = int(np.argmin(losses)) + 1 if losses else 0
        T = min(T, len(m_in.staged_val))
        self.rounds_ = T
        Fv = m_in.staged_val[T - 1] if T > 0 else np.full(len(va), m_in.a0)
        self.cal_ = _Calib(self.p("calib")).fit(Fv, y[va], w[va])
        keep = _subsample(len(y), self.p("max_rows"), self.p("random_state"))
        self.model_ = ADTLogitBoost(T, self.p("eps_frac"), self.p("single_splitter")).fit(
            B[keep], y[keep], w[keep], self.binner_.n_edges, self.binner_.nb)
        return self

    def _F(self, X):
        return self.model_.decision_function(self.binner_.transform(self._arr(X)))

    def score(self, X):
        F = self._F(X)
        return self.cal_.a * F + self.cal_.b

    def predict_proba(self, X):
        return self.cal_(self._F(X))

    def weights_table(self):
        rows = self.model_.describe(self.columns_, self.binner_.edges)
        a = self.cal_.a
        what = "the chance the trade pays" if self.task == "entry" else "the case for exiting now"
        return pd.DataFrame({
            "signal": [r[0] for r in rows], "weight": [a * r[1] for r in rows],
            "points": [round(a * r[1] / LN2_20, 1) for r in rows],
            "meaning": [("baseline score" if r[2] == 0 else
                         f"rule fires: {'raises' if a * r[1] > 0 else 'lowers'} {what} (odds x{math.exp(a * r[1]):.2f})")
                        for r in rows],
            "source": [f"learned, ADT {'root' if r[2] == 0 else f'round {r[2]}'} (boost score x Platt slope {a:.3f})"
                       for r in rows],
            "boost_value": [r[1] for r in rows]})


@register
class CreamerFreundExperts(_MLBase):
    name = "ml_creamer_experts"
    source = (f"{CREAMER}. Layer 1: ADT/LogitBoost experts on moving 2-year windows (thesis sec. 6.3), 20 rounds "
              "(Creamer 2012); layer 2: expert weighting w_i = I_i ramp exp(C cart_i / sqrt(n)), C = 1, W = L - S "
              "(thesis sec. 6.2.2.1, fig. 6.2); layer 3: |W| < gamma0 = 0.20 -> no trade (trade_signal)")
    DEFAULTS = dict(rounds=20, window_years=2.0, every_months=3.0, max_experts=11, C=1.0, version="base",
                    gamma0=0.20, max_rows_expert=50_000, min_expert_rows=200, val_years=1.0, n_bins=32,
                    calib="platt", single_splitter=False, random_state=0)

    def p(self, key, default=None):
        return self.params.get(key, self.DEFAULTS.get(key, default))

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, int)
        w = _weights(w, len(y))
        A = X.to_numpy(np.float64, na_value=np.nan)
        n = len(y)
        self.binner_ = _Binner(self.p("n_bins")).fit(A[_subsample(n, 200_000, self.p("random_state"))])
        B = self.binner_.transform(A)
        if not _has(meta, "t"):                                        # no clock: one expert, Platt on inner split
            t = np.arange(n, dtype=float)
            te = t.copy()
            span = max(n, 1)
            win, step = float(span), float(span) / 4
        else:
            t = _ts(meta["t"])
            te = _ts(meta["t_end"]) if _has(meta, "t_end") else t.copy()
            te = np.where(np.isfinite(te), te, t)
            win, step = self.p("window_years") * YEAR_NS, self.p("every_months") / 12 * YEAR_NS
        pnl = _pnl(meta)
        r = pnl if pnl is not None else 2.0 * y - 1.0
        r = r / (np.std(r) or 1.0)                                     # cart_i ~ sum of ~N(eps, 1) terms (thesis)
        t_hi = t.max()
        ends = [t_hi - j * step for j in range(1, 10_000) if t_hi - j * step > t.min()]
        experts = []
        for e in sorted(ends)[::-1]:                                   # newest first, keep max_experts
            rows = np.flatnonzero((t >= e - win) & (t < e) & (te < e))
            if len(rows) < self.p("min_expert_rows") or len(np.unique(y[rows])) < 2:
                continue
            rows = rows[_subsample(len(rows), self.p("max_rows_expert"), self.p("random_state"))]
            m = ADTLogitBoost(self.p("rounds"), single_splitter=self.p("single_splitter")).fit(
                B[rows], y[rows], w[rows], self.binner_.n_edges, self.binner_.nb)
            experts.append((e, m))
            if len(experts) >= self.p("max_experts"):
                break
        if not experts:                                                # too little history: one expert on all
            keep = _subsample(n, self.p("max_rows_expert"), self.p("random_state"))
            m = ADTLogitBoost(self.p("rounds"), single_splitter=self.p("single_splitter")).fit(
                B[keep], y[keep], w[keep], self.binner_.n_edges, self.binner_.nb)
            experts = [(t.min(), m)]
            self.fallback_expert_ = True
        experts.sort(key=lambda z: z[0])
        self.experts_ = experts
        S = np.array([np.sign(m.decision_function(B)) for _, m in experts])   # E x n votes on training rows
        self._t, self._te, self._r, self._S, self._step = t, te, r, S, step
        self._I = [1.0]                                                # I_i = mean weight of experts < i at t_i
        for i in range(1, len(experts)):
            self._I.append(float(self._weights_at(experts[i][0])[:i].mean()))

        T_val = t_hi - self.p("val_years") * YEAR_NS if _has(meta, "t") else np.quantile(t, 0.75)
        wv = self._weights_at(T_val)
        val = np.flatnonzero(t >= T_val)
        if wv.sum() > 0 and len(np.unique(y[val])) == 2 and not getattr(self, "fallback_expert_", False):
            Wv = (wv[:, None] * S[:, val]).sum(0) / wv.sum()
            self.cal_ = _Calib(self.p("calib")).fit(Wv, y[val], w[val])
            self.calib_note_ = f"calibrated on {len(val)} rows after {pd.Timestamp(T_val)} (weights frozen there)"
        else:                                                          # fallback: in-sample W (optimistic)
            wa = self._weights_at(t_hi + 1)
            Wa = (wa[:, None] * S).sum(0) / max(wa.sum(), 1e-12)
            self.cal_ = _Calib(self.p("calib")).fit(Wa, y, w)
            self.calib_note_ = "FALLBACK: calibrated in-sample (too little history for an out-of-sample block)"
        self.w_ = self._weights_at(t_hi + 1)
        if self.w_.sum() <= 0:
            self.w_ = np.ones(len(experts))
        del self._S, self._t, self._te, self._r
        return self

    def _weights_at(self, T):
        """Expert weights at time T from outcomes resolved by T (t_end <= T) after each expert's training end
        (Creamer thesis 6.2.2.1): first expert exp(C cart/den); expert i > 1: I_i ramp(T - t_i) exp(C cart_i/den),
        den = sqrt(n) 'base', n 'simple time adjustment', 1 'no time adjustment' (n = outcomes counted)."""
        C, ver = self.p("C"), self.p("version")
        ends = [e for e, _ in self.experts_]
        out = np.zeros(len(ends))
        for i, e in enumerate(ends):
            if e > T or i >= len(self._I):
                continue
            ok = (self._t >= e) & (self._te <= T)
            n_i = int(ok.sum())
            cart = float(np.sum(self._S[i, ok] * self._r[ok]))
            den = {"base": math.sqrt(max(n_i, 1)), "simple": max(n_i, 1), "none": 1.0}[ver]
            g = math.exp(float(np.clip(C * cart / den, -50, 50)))
            if i == 0:
                out[i] = g
                continue
            nxt = ends[i + 1] if i + 1 < len(ends) else e + self._step
            ramp = min((T - e) / max(nxt - e, 1.0), 1.0)
            out[i] = self._I[i] * ramp * g
        return out

    def _W(self, X):
        B = self.binner_.transform(self._arr(X))
        S = np.array([np.sign(m.decision_function(B)) for _, m in self.experts_])
        return (self.w_[:, None] * S).sum(0) / self.w_.sum()

    def trade_signal(self, X):
        """Creamer & Freund layer 3: W = L - S in [-1, 1] with |W| < gamma0 set to 0 (no trade)."""
        W = self._W(X)
        return np.where(np.abs(W) < self.p("gamma0"), 0.0, W)

    def score(self, X):
        return self.cal_.a * self._W(X) + self.cal_.b

    def predict_proba(self, X):
        return self.cal_(self._W(X))

    def weights_table(self):
        tot = self.w_.sum()
        return pd.DataFrame({
            "signal": [f"expert {i + 1}: ADT trained on the 2 years to {pd.Timestamp(e).date() if e > 1e17 else e}"
                       for i, (e, _) in enumerate(self.experts_)],
            "weight": self.w_ / tot, "points": np.nan,
            "meaning": ["share of the expert vote (NOT a log-odds weight); rules: see that expert's ADT"] * len(self.w_),
            "source": f"expert weighting (Creamer thesis 6.2.2.1, C={self.p('C')}); {self.calib_note_}"})


# ============================================================================================ 3) prior-informed ML
def _build_prior(spec, task, prior_params):
    if isinstance(spec, Scorer):
        return copy.deepcopy(spec)
    if isinstance(spec, type) and issubclass(spec, Scorer):
        return spec(task=task, **prior_params)
    if spec is None:
        raise ValueError("prior-informed scorers need params prior=<registered scorer name>")
    if spec not in REGISTRY:
        for mod in ("approach_hand", "approach_stat"):
            try:
                importlib.import_module(mod)
            except Exception:                                           # noqa: BLE001 - other agents' modules
                pass
    if spec not in REGISTRY:
        raise KeyError(f"prior {spec!r} is not registered; known: {sorted(REGISTRY)}")
    return REGISTRY[spec](task=task, **prior_params)


def _prior_logodds(prior, X, source="proba"):
    if source == "score":
        return np.asarray(prior.score(X), float)
    return _logit(prior.predict_proba(X))


class _PriorBase(_MLBase):
    family = "prior_ml"

    def _new_prior(self):
        return _build_prior(self.params.get("prior"), self.task, self.params.get("prior_params", {}) or {})

    def _fit_prior(self, X, y, w, meta):
        pr = self._new_prior()
        pr.fit(X, y, w, meta)
        return pr

    def _prep(self, A):
        imp = _Imputer().fit(A)
        Ai = imp.transform(A)
        gs = _GelmanScaler().fit(Ai)
        return imp, gs

    def _Z(self, A, imp, gs):
        return gs.transform(imp.transform(A))


@register
class PriorLogitOffset(_PriorBase):
    name = "prior_logit_offset"
    source = (f"Logistic regression with an OFFSET (GLM offset, McCullagh & Nelder 1989) = the prior's calibrated "
              f"log-odds, so it learns corrections to the prior; Gaussian prior N(0, s^2) on {GELMAN} sec. 2.1-scaled "
              "inputs (sec. 3.1 normal prior; 'cauchy' optional, sec. 2.2), s chosen on the inner time split")
    DEFAULTS = dict(prior=None, prior_params={}, offset_source="proba", prior_dist="normal",
                    scales=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5), crossfit=0)

    def p(self, key, default=None):
        return self.params.get(key, self.DEFAULTS.get(key, default))

    def _offset_train(self, X, y, w, meta, prior):
        """Offset for the TRAINING rows: the prior fit on all of them (default), or stacking-style cross-fitting in
        k contiguous time blocks (crossfit=k; Wolpert 1992 / Breiman 1996 level-one data)."""
        k = int(self.p("crossfit") or 0)
        if k < 2:
            return _prior_logodds(prior, X, self.p("offset_source"))
        n = len(y)
        order = np.argsort(_ts(meta["t"]) if _has(meta, "t") else np.arange(n), kind="stable")
        off = np.empty(n)
        for blk in np.array_split(order, k):
            rest = np.setdiff1d(order, blk)
            pr = self._fit_prior(X.iloc[rest], y[rest], w[rest], _rows(meta, rest))
            off[blk] = _prior_logodds(pr, X.iloc[blk], self.p("offset_source"))
        return off

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, float)
        w = _weights(w, len(y))
        A = X.to_numpy(np.float64, na_value=np.nan)
        dist = self.p("prior_dist")
        tr, va = inner_split(meta, y)
        pr_in = self._fit_prior(X.iloc[tr], y[tr], w[tr], _rows(meta, tr))
        off_tr = self._offset_train(X.iloc[tr], y[tr], w[tr], _rows(meta, tr), pr_in)
        off_va = _prior_logodds(pr_in, X.iloc[va], self.p("offset_source"))
        imp, gs = self._prep(A[tr])
        Ztr, Zva = self._Z(A[tr], imp, gs), self._Z(A[va], imp, gs)
        self.val_loss_ = {"prior_only": wlogloss(y[va], _sig(off_va), w[va])}
        theta = None
        for s in sorted(self.p("scales")):
            b0, beta = map_logit(Ztr, y[tr], w[tr], offset=off_tr, s=s, dist=dist, theta0=theta)
            theta = np.concatenate([[b0], beta])
            self.val_loss_[s] = wlogloss(y[va], _sig(off_va + b0 + Zva @ beta), w[va])
        self.s_ = min((k for k in self.val_loss_ if k != "prior_only"), key=self.val_loss_.get)
        self.prior_ = self._fit_prior(X, y, w, meta)
        off = self._offset_train(X, y, w, meta, self.prior_)
        self.imp_, self.gs_ = self._prep(A)
        self.b0_, self.beta_ = map_logit(self._Z(A, self.imp_, self.gs_), y, w, offset=off, s=self.s_, dist=dist)
        return self

    def score(self, X):
        X = self._align(X)
        return (_prior_logodds(self.prior_, X, self.p("offset_source")) + self.b0_
                + self._Z(X.to_numpy(np.float64, na_value=np.nan), self.imp_, self.gs_) @ self.beta_)

    def predict_proba(self, X):
        return _sig(self.score(X))

    def weights_table(self):
        raw = self.beta_ / self.gs_.scale
        t = _linear_table(self.columns_, raw, self.task,
                          f"learned CORRECTION added to prior {self.params.get('prior')!r} log-odds (s={self.s_:g})",
                          {"weight_gelman_scaled": self.beta_})
        t["meaning"] = "correction to the prior, " + t["meaning"]
        extra = pd.DataFrame([{"signal": "(intercept shift)", "weight": self.b0_, "points": round(self.b0_ / LN2_20, 1),
                               "meaning": "added to the prior's log-odds for every row",
                               "source": "learned", "weight_gelman_scaled": self.b0_}])
        return pd.concat([t, extra], ignore_index=True)


def prior_linear_weights(prior, X: pd.DataFrame, Ai: np.ndarray):
    """Per-feature LOG-ODDS weights implied by a fitted prior, in raw feature units, plus how they were obtained.
    1) prior.linear_weights() -> {column: weight} or 2) prior.weights_table() rows whose 'signal' is a column of X:
       accepted when the prior's score() is ~linear in them (corr >= 0.98 on these rows), then converted to log-odds
       units by the OLS slope of the prior's calibrated log-odds on its score;
    3) otherwise: least-squares projection of the prior's calibrated log-odds on the (imputed) features (+ R^2)."""
    cols = list(X.columns)
    target = _logit(prior.predict_proba(X))
    cand = None
    if callable(getattr(prior, "linear_weights", None)):
        cand = pd.Series(prior.linear_weights(), dtype=float)
    else:
        try:
            wt = prior.weights_table()
        except Exception:                                               # noqa: BLE001
            wt = None
        if isinstance(wt, pd.DataFrame) and {"signal", "weight"} <= set(wt.columns):
            wt = wt[wt["signal"].isin(cols)]
            if len(wt) and wt["signal"].is_unique:
                cand = pd.Series(pd.to_numeric(wt["weight"], errors="coerce").to_numpy(), index=wt["signal"])
    if cand is not None:
        cand = cand[cand.index.isin(cols)].fillna(0.0)
        wv = np.array([cand.get(c, 0.0) for c in cols])
        s = np.asarray(prior.score(X), float)
        lin = Ai @ wv
        if np.std(s) > 0 and np.std(lin) > 0 and np.corrcoef(s, lin)[0, 1] >= 0.98:
            a = np.cov(target, s)[0, 1] / np.var(s, ddof=1)
            return a * wv, f"prior's own per-feature weights x calibration slope {a:.3f}", 1.0
    Z = np.column_stack([np.ones(len(Ai)), Ai])
    lam = 1e-6 * len(Ai)
    coef = np.linalg.solve(Z.T @ Z + lam * np.diag(np.r_[0.0, np.ones(Ai.shape[1])]), Z.T @ target)
    resid = target - Z @ coef
    r2 = 1 - resid.var() / max(target.var(), 1e-12)
    return coef[1:], f"least-squares projection of the prior's log-odds on the features (R^2={r2:.3f})", float(r2)


@register
class PriorLogitShrink(_PriorBase):
    name = "prior_logit_shrink"
    source = (f"Bayesian logistic regression with an INFORMATIVE Gaussian prior beta_j ~ N(mu_j, s^2) ({GELMAN} "
              "sec. 3.1), mu_j = the prior scorer's per-feature log-odds weights, inputs scaled per sec. 2.1, s chosen "
              "on the inner time split; 'cauchy' (sec. 2.2 default family) optional")
    DEFAULTS = dict(prior=None, prior_params={}, prior_dist="normal",
                    scales=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5))

    def p(self, key, default=None):
        return self.params.get(key, self.DEFAULTS.get(key, default))

    def _mu(self, prior, X, A, imp, gs):
        raw, how, r2 = prior_linear_weights(prior, X, imp.transform(A))
        return raw * gs.scale, raw, how, r2                             # Gelman-scaled and raw units

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, float)
        w = _weights(w, len(y))
        A = X.to_numpy(np.float64, na_value=np.nan)
        dist = self.p("prior_dist")
        tr, va = inner_split(meta, y)
        pr_in = self._fit_prior(X.iloc[tr], y[tr], w[tr], _rows(meta, tr))
        imp, gs = self._prep(A[tr])
        mu, _, _, _ = self._mu(pr_in, X.iloc[tr], A[tr], imp, gs)
        Ztr, Zva = self._Z(A[tr], imp, gs), self._Z(A[va], imp, gs)
        self.val_loss_ = {"prior_only": wlogloss(y[va], pr_in.predict_proba(X.iloc[va]), w[va])}
        theta = None
        for s in sorted(self.p("scales")):
            b0, beta = map_logit(Ztr, y[tr], w[tr], mu=mu, s=s, dist=dist, theta0=theta)
            theta = np.concatenate([[b0], beta])
            self.val_loss_[s] = wlogloss(y[va], _sig(b0 + Zva @ beta), w[va])
        self.s_ = min((k for k in self.val_loss_ if k != "prior_only"), key=self.val_loss_.get)
        self.prior_ = self._fit_prior(X, y, w, meta)
        self.imp_, self.gs_ = self._prep(A)
        self.mu_, self.mu_raw_, self.mu_how_, self.mu_r2_ = self._mu(self.prior_, X, A, self.imp_, self.gs_)
        self.b0_, self.beta_ = map_logit(self._Z(A, self.imp_, self.gs_), y, w, mu=self.mu_, s=self.s_, dist=dist)
        return self

    def score(self, X):
        return self.b0_ + self._Z(self._arr(X), self.imp_, self.gs_) @ self.beta_

    def predict_proba(self, X):
        return _sig(self.score(X))

    def weights_table(self):
        raw = self.beta_ / self.gs_.scale
        return _linear_table(self.columns_, raw, self.task,
                             f"learned, shrunk toward prior {self.params.get('prior')!r} (s={self.s_:g}); "
                             f"prior weights from {self.mu_how_}",
                             {"prior_weight": self.mu_raw_, "delta": raw - self.mu_raw_,
                              "weight_gelman_scaled": self.beta_})


class _PriorInit(ClassifierMixin, BaseEstimator):
    """GradientBoostingClassifier init: the already-fitted prior scorer. GradientBoosting hands over float32 arrays
    with NaN encoded as SENTINEL; we rebuild the DataFrame (NaN restored) for the prior."""

    def __init__(self, prior=None, columns=None):
        self.prior = prior
        self.columns = columns

    def fit(self, X, y, sample_weight=None):                           # prior already fit on these training rows
        self.classes_ = np.array([0, 1])
        return self

    def predict_proba(self, X):
        A = np.asarray(X, np.float64)
        A = np.where(A <= SENTINEL / 10, np.nan, A)
        p = np.clip(self.prior.predict_proba(pd.DataFrame(A, columns=self.columns)), P_EPS, 1 - P_EPS)
        return np.column_stack([1 - p, p])


class _ValMonitor:
    """GradientBoostingClassifier.fit(monitor=...) hook: tracks the held-out (later-in-time) log loss after every tree
    (raw += learning_rate x tree output, starting from the prior's log-odds) and stops after `patience` trees without
    improvement. best = number of trees with the lowest held-out loss (0 = the prior alone)."""

    def __init__(self, Ev, yv, wv, raw0, patience):
        self.Ev, self.yv, self.wv, self.patience = Ev, yv, wv, patience
        self.raw = raw0.astype(float).copy()
        self.best_raw = self.raw.copy()
        self.losses = [wlogloss(yv, _sig(self.raw), wv)]
        self.best = 0

    def __call__(self, i, est, _locals):
        self.raw += est.learning_rate * est.estimators_[i, 0].predict(self.Ev)
        self.losses.append(wlogloss(self.yv, _sig(self.raw), self.wv))
        if self.losses[-1] < self.losses[self.best]:
            self.best = i + 1
            self.best_raw = self.raw.copy()
        return (i + 1 - self.best) >= self.patience


@register
class PriorGBM(_PriorBase):
    name = "prior_gbm"
    source = ("scikit-learn GradientBoostingClassifier(init=<fitted, calibrated prior>) - Friedman (2001) gradient "
              "boosting started from the prior's log-odds; depth 3, learning_rate 0.05, <= 300 trees, "
              "min_samples_leaf 500 (SPEC.md gbm), subsample 0.5 (Friedman 2002; Ridgeway gbm guide); number of "
              "trees on the inner time split (0 = keep the prior); isotonic calibration on that split (SPEC.md)")
    DEFAULTS = dict(prior=None, prior_params={}, max_trees=300, learning_rate=0.05, max_depth=3, subsample=0.5,
                    min_samples_leaf=500, max_rows=100_000, patience=50, calib="isotonic", random_state=0)

    def p(self, key, default=None):
        return self.params.get(key, self.DEFAULTS.get(key, default))

    @staticmethod
    def _enc(X):
        A = X.to_numpy(np.float32, na_value=np.nan)
        return np.where(np.isfinite(A), A, np.float32(SENTINEL)).astype(np.float32)

    def _gbm(self, prior, n_trees, n_rows):
        leaf = int(max(5, min(self.p("min_samples_leaf"), n_rows // 50)))   # small-sample guard
        return GradientBoostingClassifier(
            loss="log_loss", init=_PriorInit(prior, self.columns_), n_estimators=max(int(n_trees), 1),
            learning_rate=self.p("learning_rate"), max_depth=self.p("max_depth"), subsample=self.p("subsample"),
            min_samples_leaf=leaf, random_state=self.p("random_state"))

    def fit(self, X, y, w=None, meta=None):
        X = self._setup(X)
        y = np.asarray(y, int)
        w = _weights(w, len(y))
        E = self._enc(X)
        tr, va = inner_split(meta, y)
        pr_in = self._fit_prior(X.iloc[tr], y[tr], w[tr], _rows(meta, tr))
        sub = tr[_subsample(len(tr), self.p("max_rows"), self.p("random_state"))]
        raw0 = _logit(_PriorInit(pr_in, self.columns_).predict_proba(E[va])[:, 1])
        mon = _ValMonitor(E[va], y[va], w[va], raw0, self.p("patience"))
        self._gbm(pr_in, self.p("max_trees"), len(sub)).fit(E[sub], y[sub], sample_weight=w[sub], monitor=mon)
        self.val_loss_ = mon.losses
        self.n_trees_ = mon.best
        self.cal_ = _Calib(self.p("calib")).fit(mon.best_raw, y[va], w[va])
        self.prior_ = self._fit_prior(X, y, w, meta)
        if self.n_trees_ > 0:
            keep = _subsample(len(y), self.p("max_rows"), self.p("random_state"))
            self.model_ = self._gbm(self.prior_, self.n_trees_, len(keep)).fit(E[keep], y[keep], sample_weight=w[keep])
        else:
            self.model_ = None
        return self

    def _raw(self, X):
        X = self._align(X)
        if self.model_ is None:
            return _logit(self.prior_.predict_proba(X))
        return _logit(self.model_.predict_proba(self._enc(X))[:, 1])

    def score(self, X):
        return self._raw(X)

    def predict_proba(self, X):
        return self.cal_(self._raw(X))

    def weights_table(self):
        if self.model_ is None:
            imp = np.zeros(len(self.columns_))
        else:
            imp = self.model_.feature_importances_
        return pd.DataFrame({
            "signal": self.columns_, "weight": imp, "points": np.nan,
            "meaning": [f"impurity importance {v:.1%} of the {self.n_trees_} correction trees on top of the prior "
                        "(NOT a log-odds weight)" for v in imp],
            "source": f"feature importance of boosting started at prior {self.params.get('prior')!r}"
        }).sort_values("weight", ascending=False).reset_index(drop=True)
