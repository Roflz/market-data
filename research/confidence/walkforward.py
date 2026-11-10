"""
Module 3 (SPEC.md): walk-forward training and evaluation of the confidence models for ENTRY events and EXIT rows.

Inputs are plain DataFrames, one row per event (entries) or per open-trade bar (exits), with
    t        timestamp of the signal bar (bar START, New York time). Its values are known at its close.
    t_end    timestamp at which the row's label is known (label end, used for purging), e.g. `t_end_1.5`.
    d        trade direction (+1 long / -1 short).
    market   market symbol ("ES", "NQ", "YM"); used for the overlap weights.
    features the feature columns (features.py F columns + trade-state columns for exits). SIGNED features use
             +1 = bullish; walkforward multiplies them by d, so + means "with the trade" (orient()).
    label    0/1 outcome (`y_1.5` for entries, `y_exit` for exits) and the matching net $ column
             (`pnl_usd_1.5` for entries, `exit_gain_usd` for exits = $ of exiting now minus $ of holding).
    trade    (exits only) trade id; rows of one trade are the bars the trade is open, in time order.

What it does (each item is a public function; walk_forward() runs them all):
  * make_folds()         expanding window by calendar year: test years 2013..2024 and 2025H1. The LOCKED HOLDOUT
                         (Globex sessions dated 2025-07-01 onward = from the 2025-06-30 18:00 bar) is refused
                         (HoldoutError) unless final=True is passed; with final=False, before_holdout() also drops
                         every row whose signal bar, label end or (exits) any trade bar is at/after 2025-06-30 18:00.
                         $/year divides by the part of the test window the data covers (Fold.span_years), so the
                         open-ended final fold is measured to the end of the data.
  * train_mask()         purge: a training row must have t_end <= test start - 1 day; embargo: rows in the first
                         `embargo_sessions` trading sessions after the test window are not used for training (only
                         relevant when training after the test window is allowed; expanding windows never are).
  * sample_weights()     (a) uniqueness = average of 1/concurrency over the row's [t, t_end] window, per market
                         (Lopez de Prado), (b) divided by the number of markets with an event at the same t and d.
    exit_weights()       every trade's rows share a total weight of 1.
  * orient()             signed features x d.
  * models               "vote"  = equal-weight family vote (sum of d*fam_*, d*ema_stack, d*struct_5, d*brk_5,
                                   d*h1_ema_stack), turned into a probability by a 1-feature logistic fit;
                         "logit" = median imputation + StandardScaler + L2 LogisticRegression, C chosen on log loss
                                   by an inner time split (fit on years < Y-1, validate on the last 2 training years);
                         "gbm"   = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=300,
                                   l2_regularization=1, min_samples_leaf=500) fitted on the training years except
                                   the last one, + isotonic calibration fitted on the last training year.
  * thresholds           chosen on the TRAINING period's inner out-of-sample predictions (the validation years
                         above): entries maximise mean net $ per trade with >= 5% of events kept
                         (select_threshold); exits maximise mean $ gain per trade of "exit at the first bar with
                         p >= thr" with >= 5% of trades exited early (select_exit_threshold).
  * metrics              AUC, Brier, log loss, 10-bin calibration table, trades kept, net $/trade, total $, hit rate,
                         $/year, per fold and pooled. Baselines at the SAME number of trades: all events, vote top-N,
                         random skip (mean and 5-95% of 200 draws), single best training pattern.
  * permutation_test()   y (and its $) shuffled within each calendar year, the whole procedure refitted, OOS $ kept.
  * weight_table(), scorecard()   logit coefficients per fold (standardized and raw), sign stability, and points
                         = round(raw coef / (ln 2 / 20)) per unit (+20 points doubles the odds).
  * evaluate_exit_policies()      learned exit vs hold vs "exit on any opposite classic pattern" vs random-time exits
                         drawn from the learned exit's own timing distribution; $ per trade.

No look-ahead: every model, C, threshold, calibration and best-pattern choice of a fold uses only rows whose labels
are known (t_end) at least 1 day before the test window starts; holdout rows (and rows whose label or trade bars
reach into the holdout) are dropped before anything else unless final=True. Rows with a missing label or $ are
dropped.

Run: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 x.py
"""
import math
import warnings
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

try:                                                   # the classic (non-frequent) candle patterns, as exits.py
    import exits as _ex
    CLASSIC = list(_ex.CLASSIC)
except Exception:                                      # pragma: no cover - fallback if signals/ is not on the path
    CLASSIC = ["dragonfly_doji", "gravestone_doji", "hammer", "hanging_man", "inverted_hammer", "shooting_star",
               "marubozu", "engulfing", "harami", "piercing", "dark_cloud", "morning_evening_star",
               "three_soldiers_crows", "three_inside", "pin_bar", "tweezer", "five_lower_lows_higher_highs"]

HOLDOUT_START = pd.Timestamp("2025-07-01")             # first Globex SESSION (trade date) of the locked holdout
HOLDOUT_SESSION_START = HOLDOUT_START - pd.Timedelta(hours=6)   # its first bar: 2025-06-30 18:00 ET (session_label)
TEST_YEARS = tuple(range(2013, 2025))
FAR_FUTURE = pd.Timestamp("2100-01-01")                 # test_end of the open-ended holdout fold (not a data date)
YEAR = pd.Timedelta(days=365.25)
PURGE = pd.Timedelta(days=1)
POINT = math.log(2) / 20                 # scorecard: one point of log-odds; +20 points doubles the odds
C_GRID = (1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0)
GBM_PARAMS = dict(max_depth=3, learning_rate=0.05, max_iter=300, l2_regularization=1.0, min_samples_leaf=500,
                  early_stopping=False, random_state=0)
VOTE_BASE = ("ema_stack", "struct_5", "brk_5", "h1_ema_stack")
P_CLIP = 1e-4


class HoldoutError(RuntimeError):
    """Raised when anything would be evaluated on the locked 2025-07-01+ holdout without final=True."""


# ============================================================================================ folds and purging
@dataclass(frozen=True)
class Fold:
    """One walk-forward fold. Test window = [test_start, test_end). Training = rows with t < train_end (expanding
    window: train_end = test_start), purged by train_mask()."""
    name: str
    test_start: pd.Timestamp
    test_end: pd.Timestamp
    train_end: pd.Timestamp = None

    @property
    def open_ended(self):
        """True for a fold whose test window has no real end (the final holdout fold, test_end = FAR_FUTURE)."""
        return self.test_end >= FAR_FUTURE

    @property
    def years(self):
        """Calendar length of the test window in years. NaN for an open-ended fold: its length depends on where the
        data ends, so $/year must use span_years(data_end) (walk_forward does)."""
        if self.open_ended:
            return np.nan
        return (self.test_end - self.test_start) / YEAR

    def span_years(self, data_end=None):
        """Length in years of the part of the test window the data covers: [test_start, min(test_end, data_end)).
        This is the denominator of every $/year number of the fold (an open-ended fold measured to FAR_FUTURE
        would divide by ~75 years)."""
        end = self.test_end if data_end is None else min(self.test_end, pd.Timestamp(data_end))
        if end >= FAR_FUTURE:
            raise ValueError(f"fold {self.name} is open-ended: pass data_end to measure its span")
        return max((end - self.test_start) / YEAR, 0.0)


def make_folds(test_years=TEST_YEARS, h1_2025=True, final=False):
    """Expanding-window folds by calendar year: one per test year Y (test = [Y-01-01, Y+1-01-01)), then 2025H1
    (2025-01-01 up to the holdout's first bar, HOLDOUT_SESSION_START = 2025-06-30 18:00). With final=True, adds the
    locked-holdout fold '2025H2+' = every Globex session dated 2025-07-01 onward, i.e. [2025-06-30 18:00, open end):
    the evening of 2025-06-30 belongs to the 2025-07-01 session, so it is holdout, not 2025H1.
    Raises HoldoutError if a requested test year reaches into the holdout and final is False."""
    folds = []
    for y in test_years:
        f = Fold(str(y), pd.Timestamp(y, 1, 1), pd.Timestamp(y + 1, 1, 1))
        folds.append(f)
    if h1_2025:
        folds.append(Fold("2025H1", pd.Timestamp("2025-01-01"), HOLDOUT_SESSION_START))
    if final:
        folds.append(Fold("2025H2+", HOLDOUT_SESSION_START, FAR_FUTURE))
    folds = [Fold(f.name, f.test_start, f.test_end, f.test_start if f.train_end is None else f.train_end)
             for f in folds]
    for f in folds:
        check_holdout(f, final)
    return folds


def check_holdout(fold, final=False):
    """Refuse (HoldoutError) a fold whose test window, or training window, reaches past 2025-07-01, or that starts
    inside the holdout (at/after its first bar 2025-06-30 18:00), unless final=True. A fold ending exactly at
    2025-07-01 is accepted: its holdout-session rows (2025-06-30 18:00-24:00) are removed from the DATA by
    before_holdout(), which is the guard that matters."""
    if final:
        return
    if fold.test_end > HOLDOUT_START or fold.test_start >= HOLDOUT_SESSION_START or \
            (fold.train_end is not None and fold.train_end > HOLDOUT_START):
        raise HoldoutError(f"fold {fold.name} touches the locked holdout ({HOLDOUT_START.date()}+); "
                           "pass final=True only for the one final evaluation")


def session_label(t):
    """Globex session date of timestamps (New York): the session starting at 18:00 belongs to the next day."""
    return (pd.DatetimeIndex(t) + pd.Timedelta(hours=6)).normalize()


def before_holdout(df, kind="entry", t="t", t_end="t_end", trade="trade", ts="ts"):
    """Boolean mask (numpy) of rows that are ENTIRELY before the locked holdout, whose first bar is
    HOLDOUT_SESSION_START (2025-06-30 18:00 ET = the start of the 2025-07-01 Globex session):
    * entries: the signal bar t and the label end t_end (the end of the exit minute: the 1-minute path walked for the
      label) are both before it - an event on the evening of 2025-06-30 is a 2025-07-01 session event, and an event
      whose label path runs past 18:00 uses holdout prices;
    * exits: the same for EVERY row of the trade (all t, t_end and bar times `ts` when present): a trade is kept or
      dropped whole, so neither its features (bar ts) nor its labels touch holdout prices.
    walk_forward(final=False) keeps only these rows, before anything else is computed. A missing t_end counts as
    not-before (those rows have no label and are dropped anyway)."""
    cut = HOLDOUT_SESSION_START.to_datetime64()
    if kind == "exit":
        g = df.groupby(trade, sort=False)
        last = [g[t].transform("max"), g[t_end].transform("max")]
        if ts in df.columns:
            last.append(g[ts].transform("max"))
        ok = np.ones(len(df), bool)
        for s in last:
            ok &= np.asarray(pd.DatetimeIndex(s).as_unit("ns").to_numpy() < cut)   # NaT compares False
        return ok
    tt = pd.DatetimeIndex(df[t]).as_unit("ns").to_numpy()
    te = pd.DatetimeIndex(df[t_end]).as_unit("ns").to_numpy()
    return (tt < cut) & (te < cut)


def train_mask(t, t_end, test_start, test_end, train_end=None, purge=PURGE, embargo_sessions=1, sessions=None):
    """Boolean mask of rows eligible for training around one test window [test_start, test_end).
    * before the test window: t < test_start AND t_end <= test_start - purge (purge: the label must be known a day
      before the test starts);
    * after the test window (only when train_end > test_end, i.e. not an expanding window): rows whose session is
      among the first `embargo_sessions` trading sessions after the test window are embargoed (all later sessions
      when the data has fewer than that); later rows are eligible (their t is after test_end, so their labels never
      overlap the test rows' features).
    `sessions`: sorted unique session labels of the data (default: from t) used to count trading sessions.
    Rows with t >= train_end are never eligible."""
    t = pd.DatetimeIndex(t)
    t_end = pd.DatetimeIndex(t_end)
    train_end = test_start if train_end is None else train_end
    before = (t < test_start) & (t_end <= test_start - purge)
    ok = before & (t < train_end)
    if train_end > test_end:
        lab = session_label(t)
        if sessions is None:
            sessions = np.unique(lab.to_numpy())
        last_test = session_label([test_end - pd.Timedelta(1, "ns")])[0]
        later = sessions[sessions > last_test.to_datetime64()]
        if embargo_sessions > 0 and len(later):            # fewer later sessions than the embargo: embargo all
            emb_last = later[min(embargo_sessions, len(later)) - 1]
        else:
            emb_last = last_test.to_datetime64()
        after = (t >= test_end) & (lab.to_numpy() > emb_last) & (t < train_end)
        ok = ok | after
    return np.asarray(ok)


# ============================================================================================ sample weights
def _ns(x):
    """int64 nanoseconds of timestamps (pandas 3 may store s/ms/us resolutions; never mix them)."""
    return pd.DatetimeIndex(x).as_unit("ns").asi8


def _avg_uniqueness(s, e):
    """Average of 1/concurrency over each window [s_i, e_i) (int64 ns arrays, one market). Concurrency at time x =
    number of windows with s <= x < e. Zero-length windows get 1 / (number of windows containing that instant,
    closed)."""
    e = np.maximum(e, s)
    grid = np.unique(np.r_[s, e])
    ss, es = np.sort(s), np.sort(e)
    conc = np.searchsorted(ss, grid, "right") - np.searchsorted(es, grid, "right")
    inv = np.where(conc > 0, 1.0 / np.maximum(conc, 1), 0.0)
    dur = np.diff(grid).astype(np.float64)
    cum = np.r_[0.0, np.cumsum(inv[:-1] * dur)]
    I_s = cum[np.searchsorted(grid, s)]
    I_e = cum[np.searchsorted(grid, e)]
    length = (e - s).astype(np.float64)
    out = np.empty(len(s))
    pos = length > 0
    out[pos] = (I_e[pos] - I_s[pos]) / length[pos]
    if (~pos).any():
        z = s[~pos]
        n_cover = np.searchsorted(ss, z, "right") - np.searchsorted(es, z, "left")
        out[~pos] = 1.0 / np.maximum(n_cover, 1)
    return out


def sample_weights(ev, t="t", t_end="t_end", market="market", d="d", cross_market=True):
    """Per-row training weight for entry events (not normalized; fits rescale to mean 1).
    (a) uniqueness: average over the row's [t, t_end] window of 1/(number of same-market rows whose windows cover
        that moment) - 3 events with identical windows get 1/3 each, a lone event gets 1;
    (b) cross-market: divided by the number of markets with an event at the same t and direction d (the same
        pattern on the same bar in ES, NQ and YM is close to one trade).
    Uses only timestamps (t, t_end), no outcomes. Computed on the whole data set: with purging, a training row's
    window never overlaps a test row's, so its weight is the same as if computed on the training rows alone."""
    tt = _ns(ev[t])
    te = _ns(ev[t_end])
    w = np.ones(len(ev))
    mk = ev[market].to_numpy() if market in ev else np.zeros(len(ev))
    for m in pd.unique(mk):
        i = np.flatnonzero(mk == m)
        w[i] = _avg_uniqueness(tt[i], te[i])
    if cross_market and market in ev:
        n_mk = ev.groupby([ev[t], ev[d]])[market].transform("nunique").to_numpy()
        w = w / np.maximum(n_mk, 1)
    return w


def exit_weights(rows, trade="trade"):
    """Exit rows: every trade's rows share a total weight of 1 (weight = 1 / rows of that trade)."""
    return 1.0 / rows.groupby(trade)[trade].transform("size").to_numpy(np.float64)


# ============================================================================================ features
def default_signed():
    """features.SIGNED (Module 1)."""
    import features as _f                                  # noqa: PLC0415
    return list(_f.SIGNED)


def default_mirror():
    """features.MIRROR (dist_swhi_k <-> dist_swlo_k), the pairs swapped for shorts by features.orient.
    Never silently empty: if features.py cannot be imported, or has no MIRROR, this raises (ImportError /
    AttributeError) instead of quietly dropping the short-side swap, which is part of the study's one direction
    convention. To run without features.py (e.g. synthetic data without swing columns) pass walk_forward(mirror={})."""
    import features as _f                                  # noqa: PLC0415
    if not hasattr(_f, "MIRROR"):
        raise AttributeError("features.MIRROR is missing: walk_forward(mirror='auto') cannot orient the swing-distance "
                             "pair for shorts; fix features.py or pass mirror explicitly")
    return dict(_f.MIRROR)


def orient(X, d, signed, mirror=None):
    """Return a float32 copy of X seen from the trade direction d (+ = with the trade): every signed column is
    multiplied by d and, for shorts, each `mirror` pair (a, c) swaps places (a short's a = -c and c = -a), exactly as
    features.orient: a short's distance to the swing high is a long's distance to the swing low, mirrored."""
    d = np.asarray(d, np.float32)
    out = X.astype(np.float32, copy=True)
    cols = [c for c in signed if c in out.columns]
    if cols:
        out[cols] = out[cols].to_numpy(np.float32) * d[:, None]
    short = d < 0
    for a, c in (mirror or {}).items():
        if a in X.columns and c in X.columns:
            va, vc = X[a].to_numpy(np.float32), X[c].to_numpy(np.float32)
            sa = d if a in signed else 1.0                 # long side keeps the (signed) value
            sc = d if c in signed else 1.0
            out[a] = np.where(short, -vc, va * sa).astype(np.float32)
            out[c] = np.where(short, -va, vc * sc).astype(np.float32)
    return out


def vote_columns(features, vote_cols=None):
    """Columns of the equal-weight vote: fam_* plus ema_stack, struct_5, brk_5, h1_ema_stack (those present)."""
    if vote_cols is not None:
        return [c for c in vote_cols if c in features]
    return [c for c in features if c.startswith("fam_")] + [c for c in VOTE_BASE if c in features]


def vote_score(Xo, cols, kind="entry"):
    """Equal-weight vote on ORIENTED features: sum of the columns (NaN = 0). For exits the sign is flipped
    (evidence against the trade = reason to exit)."""
    a = np.nan_to_num(np.asarray(Xo, np.float64)[:, cols] if not isinstance(Xo, pd.DataFrame)
                      else Xo[cols].to_numpy(np.float64)).sum(axis=1)
    return -a if kind == "exit" else a


# ============================================================================================ models
class VoteModel:
    """Vote baseline: p = logistic(a + b * vote score); only the 2 calibration numbers are fitted."""
    def __init__(self, cols_idx, kind):
        self.cols_idx, self.kind = cols_idx, kind
        self.lr = LogisticRegression(C=1e4, max_iter=200)

    def score(self, X):
        return vote_score(X, self.cols_idx, self.kind)

    def fit(self, X, y, w):
        s = self.score(X)[:, None]
        if np.ptp(s) == 0:
            self.const = float(np.average(y, weights=w))
        else:
            self.const = None
            self.lr.fit(s, y, sample_weight=w)
        return self

    def predict(self, X):
        if self.const is not None:
            return np.full(len(X), np.clip(self.const, P_CLIP, 1 - P_CLIP))
        return self.lr.predict_proba(self.score(X)[:, None])[:, 1]


class LogitModel:
    """Median imputation + StandardScaler + L2 LogisticRegression(C)."""
    def __init__(self, C):
        self.C = C
        self.pipe = make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True), StandardScaler(),
                                  LogisticRegression(C=C, max_iter=500))

    def fit(self, X, y, w):
        self.pipe.fit(X, y, logisticregression__sample_weight=w)
        return self

    def predict(self, X):
        return self.pipe.predict_proba(X)[:, 1]

    def coefficients(self, names):
        """DataFrame: feature, coef_std (per 1 SD), coef_raw (per unit), scale (SD), mean; '(intercept)' row has
        the intercept on the standardized and on the raw scale."""
        sc = self.pipe.named_steps["standardscaler"]
        lr = self.pipe.named_steps["logisticregression"]
        b = lr.coef_.ravel()
        scale = np.where(sc.scale_ > 0, sc.scale_, 1.0)
        raw = b / scale
        icpt_raw = lr.intercept_[0] - float(np.sum(b * sc.mean_ / scale))
        df = pd.DataFrame({"feature": list(names) + ["(intercept)"], "coef_std": np.r_[b, lr.intercept_[0]],
                           "coef_raw": np.r_[raw, icpt_raw], "scale": np.r_[sc.scale_, np.nan],
                           "mean": np.r_[sc.mean_, np.nan]})
        return df


def informative_columns(X, w=None):
    """Indices of the columns of X with at least two distinct finite values among the rows with weight > 0.
    Trees cannot split on the others, and scikit-learn 1.9's HistGradientBoosting binning CRASHES on a column with no
    finite value ("window shape cannot be larger than input array shape"), e.g. x_YM_* in a fold trained before YM's
    data starts (2018) or a pooled run's mkt_YM in those years."""
    X = np.asarray(X)
    if w is not None and not np.all(np.asarray(w) > 0):
        X = X[np.asarray(w) > 0]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)          # all-NaN column -> NaN
        lo, hi = np.nanmin(X, axis=0), np.nanmax(X, axis=0)
    return np.flatnonzero(np.isfinite(lo) & np.isfinite(hi) & (hi > lo))


class GBMModel:
    """Shallow HistGradientBoosting + isotonic calibration (fitted on a later period than the trees). The trees use
    only the columns that vary in their training rows (informative_columns); predict() selects the same ones."""
    def __init__(self, params):
        self.hgb = HistGradientBoostingClassifier(**params)
        self.iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        self.cols = None

    def fit_trees(self, X, y, w):
        self.cols = informative_columns(X, w)
        self.hgb.fit(np.asarray(X)[:, self.cols], y, sample_weight=w)
        return self

    def raw(self, X):
        return self.hgb.predict_proba(np.asarray(X)[:, self.cols])[:, 1]

    def fit_calibration(self, X, y, w):
        self.iso.fit(self.raw(X), y, sample_weight=w)
        return self

    def predict(self, X):
        return np.clip(self.iso.predict(self.raw(X)), P_CLIP, 1 - P_CLIP)


def _norm(w):
    w = np.asarray(w, np.float64)
    return w / w.mean() if len(w) and w.mean() > 0 else w


def weighted_log_loss(y, p, w=None):
    """Mean (weighted) binary log loss with p clipped to [1e-4, 1-1e-4]."""
    p = np.clip(p, P_CLIP, 1 - P_CLIP)
    ll = -(y * np.log(p) + (1 - y) * np.log(1 - p))
    return float(np.average(ll, weights=w))


# ============================================================================================ decisions
def select_threshold(p, pnl, min_keep=0.05):
    """Entry threshold on inner out-of-sample predictions: among all cut-offs `take p >= thr` that keep at least
    `min_keep` of the rows, the one with the highest mean net $ per kept row (ties in p are kept together).
    Returns (thr, info) with info = dict(keep_share, mean_usd, n)."""
    p = np.asarray(p, np.float64); pnl = np.asarray(pnl, np.float64)
    n = len(p)
    if n == 0:
        return 0.0, dict(keep_share=np.nan, mean_usd=np.nan, n=0)
    o = np.argsort(-p, kind="stable")
    ps, cs = p[o], np.cumsum(pnl[o])
    ends = np.r_[np.flatnonzero(ps[1:] != ps[:-1]), n - 1]          # last index of each tie group
    k = ends + 1
    ok = k >= math.ceil(min_keep * n)
    if not ok.any():
        ok = k == n
    k, ends = k[ok], ends[ok]
    mean = cs[ends] / k
    j = int(np.argmax(mean))
    thr = float(ps[ends[j]]) if k[j] < n else 0.0
    return thr, dict(keep_share=k[j] / n, mean_usd=float(mean[j]), n=n)


def group_starts(codes):
    """Start positions of runs of equal values in `codes` (rows of one trade must be contiguous)."""
    codes = np.asarray(codes)
    if len(codes) == 0:
        return np.zeros(0, np.int64)
    return np.flatnonzero(np.r_[True, codes[1:] != codes[:-1]])


def first_hit(mask, starts, n):
    """Per group (rows starts[g] .. starts[g+1]-1): position of the first True in mask, or -1 when none."""
    if len(starts) == 0:
        return np.zeros(0, np.int64)
    idx = np.where(mask, np.arange(n), n)
    f = np.minimum.reduceat(idx, starts)
    ends = np.r_[starts[1:], n]
    return np.where(f < ends, f, -1)


def policy_gain(mask, gain, starts):
    """$ gain vs holding per trade of 'exit at the first row where mask is True' (0 when the trade is held).
    Returns (gain_per_trade, exited bool)."""
    f = first_hit(mask, starts, len(gain))
    ex = f >= 0
    return np.where(ex, np.asarray(gain, np.float64)[np.maximum(f, 0)], 0.0), ex


def select_exit_threshold(p, gain, codes, min_keep=0.05, n_grid=100):
    """Exit threshold on inner out-of-sample rows: among candidate cut-offs (quantiles of p), the one whose policy
    'exit at the first bar with p >= thr' has the highest mean $ gain per trade vs holding, with at least
    `min_keep` of the trades exited early. Returns (thr, info)."""
    p = np.asarray(p, np.float64); gain = np.asarray(gain, np.float64)
    starts = group_starts(codes)
    n_tr = len(starts)
    if n_tr == 0:
        return np.inf, dict(exit_share=np.nan, mean_usd=np.nan, n=0)
    cands = np.unique(np.quantile(p, np.linspace(0.0, 1.0, n_grid + 1), method="lower"))   # actual p values
    best = (-np.inf, np.inf, 0.0)
    for thr in cands:                                          # loop over <= 101 thresholds, each vectorized
        g, ex = policy_gain(p >= thr, gain, starts)
        share = ex.mean()
        if share < min_keep:
            continue
        m = g.mean()
        if m > best[0]:
            best = (m, float(thr), share)
    if not np.isfinite(best[0]):                               # nothing exits >= min_keep: exit on the lowest p
        thr = float(cands[0]); g, ex = policy_gain(p >= thr, gain, starts)
        best = (g.mean(), thr, ex.mean())
    return best[1], dict(exit_share=best[2], mean_usd=float(best[0]), n=n_tr)


# ============================================================================================ metrics
def classification_metrics(y, p):
    """AUC (NaN if one class), Brier score, log loss."""
    y = np.asarray(y, np.float64); p = np.asarray(p, np.float64)
    if len(y) == 0:
        return dict(auc=np.nan, brier=np.nan, logloss=np.nan)
    auc = roc_auc_score(y, p) if 0 < y.sum() < len(y) else np.nan
    return dict(auc=float(auc), brier=float(np.mean((p - y) ** 2)), logloss=weighted_log_loss(y, p))


def trade_metrics(pnl, years):
    """n trades, net $ per trade, total $, hit rate (pnl > 0), $ per year."""
    pnl = np.asarray(pnl, np.float64)
    n = len(pnl)
    tot = float(pnl.sum())
    return dict(n_kept=n, pnl_per_trade=tot / n if n else np.nan, total_usd=tot,
                hit_rate=float((pnl > 0).mean()) if n else np.nan,
                usd_per_year=tot / years if years > 0 else np.nan)


def calibration_table(p, y, pnl=None, bins=10):
    """Equal-count bins of p: n, mean p, observed rate of y, mean $ (if pnl given)."""
    p = np.asarray(p, np.float64); y = np.asarray(y, np.float64)
    if len(p) == 0:
        return pd.DataFrame(columns=["bin", "n", "p_mean", "y_rate", "pnl_mean"])
    r = pd.Series(p).rank(method="first").to_numpy()
    b = np.minimum((r - 1) * bins // len(p), bins - 1).astype(int)
    df = pd.DataFrame({"bin": b, "p": p, "y": y, "pnl": np.nan if pnl is None else np.asarray(pnl, np.float64)})
    g = df.groupby("bin")
    return pd.DataFrame({"n": g.size(), "p_mean": g.p.mean(), "y_rate": g.y.mean(),
                         "pnl_mean": g.pnl.mean()}).reset_index()


def random_skip(pnl, n_take, n_draws=200, rng=None):
    """Totals of `n_draws` random subsets of n_take rows (without replacement). Returns an array (n_draws,)."""
    rng = np.random.default_rng(0) if rng is None else rng
    pnl = np.asarray(pnl, np.float64)
    n = len(pnl)
    if n_take <= 0 or n == 0:
        return np.zeros(n_draws)
    n_take = min(n_take, n)
    keys = rng.random((n_draws, n))
    pick = np.argpartition(keys, n_take - 1, axis=1)[:, :n_take]
    return pnl[pick].sum(axis=1)


def top_n(score, n_take, rng=None):
    """Indices of the n_take highest scores (random tie-break)."""
    rng = np.random.default_rng(0) if rng is None else rng
    score = np.asarray(score, np.float64)
    o = np.lexsort((rng.random(len(score)), -score))
    return o[:n_take]


def best_pattern(Xo, pnl, pat_cols, min_n=200, min_frac=0.005):
    """Single best directional pattern on TRAINING rows: the oriented pat_* column whose rows with value > 0
    (pattern fired in the trade direction) have the highest mean $, among patterns with >= max(min_n, min_frac*n)
    rows. Returns the column name or None."""
    best, best_m = None, -np.inf
    need = max(min_n, int(min_frac * len(pnl)))
    for c in pat_cols:                                         # ~25 columns
        f = np.asarray(Xo[c]) > 0
        if f.sum() >= need:
            m = pnl[f].mean()
            if m > best_m:
                best, best_m = c, m
    return best


def evaluate_exit_policies(p, thr, gain, codes, opp_mask, hold_usd=None, n_random=200, rng=None):
    """Exit evaluation on test trades (rows sorted by trade, then time; gain = $ of exiting at this row's next open
    minus $ of holding to the baseline end).
    Policies, as $ gain vs hold per trade (and net $ per trade when hold_usd, one value per trade, is given):
      learned   exit at the first row with p >= thr
      hold      never exit early (gain 0)
      opp       exit at the first row where any opposite classic pattern fires (opp_mask)
      random    exit at a random row: with the learned policy's exit share, at a within-trade row offset drawn from
                the learned exits' offsets (a trade too short for the drawn offset is held); n_random draws.
    Returns a dict of numbers and the per-trade learned gains."""
    rng = np.random.default_rng(0) if rng is None else rng
    gain = np.asarray(gain, np.float64)
    starts = group_starts(codes)
    n, n_tr = len(gain), len(starts)
    g_l, ex_l = policy_gain(np.asarray(p) >= thr, gain, starts)
    g_o, ex_o = policy_gain(np.asarray(opp_mask, bool), gain, starts)
    f = first_hit(np.asarray(p) >= thr, starts, n)
    nrows = np.diff(np.r_[starts, n])
    offs = (f - starts)[ex_l]
    share = ex_l.mean() if n_tr else 0.0
    if n_tr and len(offs):
        draw_off = rng.choice(offs, size=(n_random, n_tr))
        do_exit = rng.random((n_random, n_tr)) < share
        valid = do_exit & (draw_off < nrows[None, :])
        pos = np.where(valid, starts[None, :] + draw_off, 0)
        g_r = np.where(valid, gain[pos], 0.0).mean(axis=1)
    else:
        g_r = np.zeros(n_random)
    out = dict(n_trades=n_tr, learned_exit_share=float(share), learned_gain=float(g_l.mean()) if n_tr else np.nan,
               hold_gain=0.0, opp_exit_share=float(ex_o.mean()) if n_tr else np.nan,
               opp_gain=float(g_o.mean()) if n_tr else np.nan,
               random_gain=float(g_r.mean()), random_p5=float(np.quantile(g_r, 0.05)),
               random_p95=float(np.quantile(g_r, 0.95)))
    if hold_usd is not None and n_tr:
        h = np.asarray(hold_usd, np.float64)
        hm = float(h.mean())
        out.update(hold_net=hm, learned_net=hm + out["learned_gain"], opp_net=hm + out["opp_gain"],
                   random_net=hm + out["random_gain"])
    out["_g_learned"] = g_l
    out["_g_opp"] = g_o
    out["_g_random_tot"] = g_r * n_tr
    return out


# ============================================================================================ walk-forward
@dataclass
class WalkForwardResult:
    """folds: one row per fold (metrics, threshold, C, baselines); pooled: the same over all OOS rows;
    oos: per test row (fold, p, take, vote, y, pnl); coefs: logit coefficients per fold (long format);
    calibration: pooled 10-bin table; skipped: folds skipped (reason)."""
    kind: str
    model: str
    folds: pd.DataFrame
    pooled: pd.Series
    oos: pd.DataFrame
    coefs: pd.DataFrame
    calibration: pd.DataFrame
    skipped: list = field(default_factory=list)


def _fit_and_threshold(model, X, y, w, pnl, year, t_end, tr, kind, codes, min_keep, C_grid, gbm_params, vote_idx,
                       purge, min_inner):
    """Fit one fold's model on training rows `tr` (already purged) and pick its threshold on inner out-of-sample
    rows. Inner split: validation = last 2 training years (logit, vote) or last training year (gbm); inner
    training = earlier years, purged against the validation start. Returns (model, thr, info) or a skip reason."""
    Y = int(year[tr].max())
    val_first = Y if model == "gbm" else Y - 1
    val_start = pd.Timestamp(val_first, 1, 1)
    isv = year[tr] >= val_first
    va = tr[isv]
    it = tr[(~isv) & (t_end[tr] <= (val_start - purge).to_datetime64())]
    if len(it) < min_inner or len(va) < min_inner or len(np.unique(y[it])) < 2 or len(np.unique(y[va])) < 2:
        return None, None, f"inner split too small (inner train {len(it)}, validation {len(va)})"
    info = dict(n_inner=len(it), n_val=len(va), C=np.nan)
    if model == "logit":
        prep = make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True), StandardScaler())
        Zi = prep.fit_transform(X[it]).astype(np.float64)
        Zv = prep.transform(X[va]).astype(np.float64)
        lr = LogisticRegression(max_iter=500, warm_start=True)   # same model as LogitModel; warm C path
        wi = _norm(w[it])
        best = (np.inf, None, None)
        for C in sorted(C_grid):                               # a handful of C values, strong -> weak penalty
            lr.set_params(C=C).fit(Zi, y[it], sample_weight=wi)
            pv = lr.predict_proba(Zv)[:, 1]
            ll = weighted_log_loss(y[va], pv, w[va])
            if ll < best[0]:
                best = (ll, C, pv)
        del Zi, Zv
        info["C"], info["val_logloss"], pv = best[1], best[0], best[2]
        final = LogitModel(best[1]).fit(X[tr], y[tr], _norm(w[tr]))
    elif model == "vote":
        pv = VoteModel(vote_idx, kind).fit(X[it], y[it], _norm(w[it])).predict(X[va])
        final = VoteModel(vote_idx, kind).fit(X[tr], y[tr], _norm(w[tr]))
    elif model == "gbm":
        final = GBMModel(gbm_params).fit_trees(X[it], y[it], _norm(w[it]))
        final.fit_calibration(X[va], y[va], _norm(w[va]))
        pv = final.predict(X[va])                              # isotonic is monotone: cut-off on OOS tree scores
    elif isinstance(model, str) and model.startswith("sc:"):
        name, *kv = model[3:].split("|")                   # "sc:name|key=value|key=value"
        prm = {}
        for a in kv:
            k_, v_ = a.split("=", 1)
            prm[k_] = int(v_) if v_.isdigit() else v_
        final = ScorerModel(name, kind, **prm).fit_idx(X, y, w, pnl, it)
        pv = final.predict(X[va])
        final = ScorerModel(name, kind, **prm).fit_idx(X, y, w, pnl, tr)
    else:
        raise ValueError(f"unknown model {model!r}")
    if kind == "entry":
        thr, ti = select_threshold(pv, pnl[va], min_keep)
    else:
        thr, ti = select_exit_threshold(pv, pnl[va], codes[va], min_keep)
    info.update({f"val_{k}": v for k, v in ti.items()})
    return final, thr, info


def _prepare(data, features, kind, label, pnl, t_end, signed, final, trade, weights, mirror):
    """Drop rows without a label, drop the holdout unless final (before_holdout: signal bar, label end and, for
    exits, every bar of the trade before 2025-06-30 18:00), sort (exits: by trade start, trade, then bar time `ts`,
    else `k`, else `t`), orient features. Returns a dict."""
    df = data
    if "t" not in df.columns:
        raise KeyError("data needs a 't' column (signal bar start timestamp)")
    keep = df[label].notna().to_numpy() & df[pnl].notna().to_numpy() & df[t_end].notna().to_numpy()
    if kind == "exit":
        t0 = df.groupby(trade)["t"].transform("min")
    else:
        t0 = df["t"]
    if not final:
        keep &= before_holdout(df, kind, "t", t_end, trade)   # the holdout is never even looked at
    w_all = None
    if weights is not None:
        w_all = np.asarray(weights, np.float64)[keep]
    df = df.loc[keep]
    t0 = t0[keep]
    if kind == "exit":
        within = (_ns(df["ts"]) if "ts" in df.columns else df["k"].to_numpy() if "k" in df.columns
                  else _ns(df["t"]))
        order = np.lexsort((within, pd.factorize(df[trade])[0], _ns(t0)))
    else:
        order = np.argsort(_ns(df["t"]), kind="stable")
    df = df.iloc[order]
    t0 = pd.DatetimeIndex(t0.iloc[order])
    if w_all is not None:
        w = w_all[order]
    elif kind == "exit":
        w = exit_weights(df, trade)
    else:
        w = sample_weights(df, t_end=t_end)
    if signed is None:
        signed = default_signed()
    Xo = orient(df[features], df["d"].to_numpy(), signed, default_mirror() if mirror == "auto" else mirror)
    codes = pd.factorize(df[trade])[0] if kind == "exit" else np.arange(len(df))
    return dict(df=df, Xo=Xo, X=Xo.to_numpy(np.float32), y=df[label].astype(float).to_numpy().astype(np.int8),
                pnl=df[pnl].to_numpy(np.float64), w=w, t=t0.as_unit("ns"),
                t_end=pd.DatetimeIndex(df[t_end]).as_unit("ns").to_numpy(),
                year=t0.year.to_numpy(), codes=codes, signed=signed)


def shuffle_within_year(year, *arrays, rng):
    """Permute rows jointly within each calendar year (the same permutation for every array)."""
    year = np.asarray(year)
    by_year = np.argsort(year, kind="stable")
    shuffled = np.lexsort((rng.random(len(year)), year))
    out = []
    for a in arrays:
        b = np.empty_like(a)
        b[by_year] = a[shuffled]
        out.append(b)
    return out


def walk_forward(data, features, *, kind="entry", model="logit", label="y_1.5", pnl="pnl_usd_1.5",
                 t_end="t_end_1.5", signed=None, folds=None, final=False, weights=None, min_keep=0.05,
                 C_grid=C_GRID, gbm_params=None, vote_cols=None, baselines=True, n_random=200, seed=0,
                 min_train_years=3, min_inner=200, purge=PURGE, trade="trade", hold="auto", classic=None,
                 mirror="auto", data_end=None, train_years=None, decay_half_life=None,
                 shuffle_rng=None, verbose=False):
    """Run the expanding-window walk-forward for one model on entry events (kind='entry') or exit rows
    (kind='exit').

    data      DataFrame with t, d, market, t_end column, label, pnl, features. Exits (labels.exit_rows format):
              also `trade` (id), `ts` (bar k start; else `k`, else `t`, orders a trade's rows) and the `hold` column
              = $ of holding the trade to its baseline end (hold="auto" uses hold_pnl_usd when present), for net $
              per trade of the exit policies. Exit rows are assigned to folds by their trade's first `t`.
    features  feature column names (raw; signed ones are oriented with d here).
    signed    names of signed features (default: features.SIGNED).
    mirror    column pairs swapped for shorts (default "auto" = features.MIRROR), as features.orient does.
    folds     list of Fold (default make_folds(final=final)); any fold touching the holdout raises HoldoutError
              unless final=True. Folds with fewer than min_train_years training years are skipped.
              With final=False, rows not entirely before the holdout (before_holdout) are dropped first.
    data_end  end (exclusive) of the period the data covers; every fold's $/year divides by the years of
              [test_start, min(test_end, data_end)) (Fold.span_years), so the open-ended holdout fold is measured
              to the end of the data, not to FAR_FUTURE. Default: midnight after the Globex session of the last
              row (session_label(last t) + 1 day). The fold rows and `pooled` report this as `years`.
    weights   optional per-row weights (default: sample_weights for entries, exit_weights for exits).
    train_years  ROLLING window: if given, each fold trains only on the last `train_years` calendar years before its
              test start (e.g. 3: the 2016 fold trains on 2013-2015, the 2025H1 fold on 2022-2024). Default: expanding.
    decay_half_life  TIME-DECAY weights: if given (years), each training row's weight is multiplied by
              0.5 ** (age / half_life), age = years from the row's signal time to the fold's test start, so a row
              `half_life` years old counts half as much as a row just before the test (re-done for every fold).
    shuffle_rng  (permutation test) if given, y and pnl are shuffled jointly within each calendar year for FITTING
              and threshold choice; test metrics always use the true y and pnl.
    Returns WalkForwardResult."""
    gbm_params = dict(GBM_PARAMS if gbm_params is None else gbm_params)
    folds = make_folds(final=final) if folds is None else list(folds)
    for f in folds:
        check_holdout(f, final)
    S = _prepare(data, features, kind, label, pnl, t_end, signed, final, trade, weights, mirror)
    if hold == "auto":
        hold = "hold_pnl_usd" if "hold_pnl_usd" in data.columns else None
    df, X, y, pn, w, t, te, year, codes = (S[k] for k in ("df", "X", "y", "pnl", "w", "t", "t_end", "year", "codes"))
    Xo = S["Xo"]
    if data_end is None and len(t):
        data_end = session_label([t.max()])[0] + pd.Timedelta(days=1)
    y_fit, pnl_fit = (y, pn) if shuffle_rng is None else shuffle_within_year(year, y, pn, rng=shuffle_rng)
    feats = list(features)
    _CTX.clear()
    _CTX.update(feats=feats, t=t, t_end=te, year=year, d=df["d"].to_numpy(), codes=codes,
                market=df["market"].to_numpy() if "market" in df.columns else None)
    vcols = vote_columns(feats, vote_cols)
    vote_idx = [feats.index(c) for c in vcols]
    vote_all = vote_score(X, vote_idx, kind) if vote_idx else np.zeros(len(df))
    pat_cols = [c for c in feats if c.startswith("pat_") and c in S["signed"]]
    classic = CLASSIC if classic is None else classic
    if kind == "exit":
        cl = [f"pat_{c}" for c in classic if f"pat_{c}" in df.columns]
        opp_all = ((df[cl].to_numpy(np.float64) * df["d"].to_numpy()[:, None]) < 0).any(axis=1) if cl \
            else np.zeros(len(df), bool)
    rng = np.random.default_rng(seed)
    rows, oos, coefs, skipped = [], [], [], []
    for f in folds:
        test = np.flatnonzero((t >= f.test_start) & (t < f.test_end))
        tr = np.flatnonzero(train_mask(t, te, f.test_start, f.test_end, f.train_end, purge=purge))
        if train_years is not None:                                   # rolling window: last N calendar years only
            tr = tr[year[tr] >= f.test_start.year - int(train_years)]
        if len(test) == 0:
            skipped.append((f.name, "no test rows")); continue
        if len(np.unique(year[tr])) < min_train_years:
            skipped.append((f.name, f"{len(np.unique(year[tr]))} training years < {min_train_years}")); continue
        w_f = w
        if decay_half_life is not None:                               # older rows count less, per fold
            age = (np.datetime64(f.test_start, "ns") - t.to_numpy()) / np.timedelta64(1, "D") / 365.25
            w_f = w * np.power(0.5, np.clip(age, 0, None) / float(decay_half_life))
        m, thr, info = _fit_and_threshold(model, X, y_fit, w_f, pnl_fit, year, te, tr, kind, codes, min_keep, C_grid,
                                          gbm_params, vote_idx, purge, min_inner)
        if m is None:
            skipped.append((f.name, info)); continue
        p = m.predict(X[test])
        take = p >= thr
        yrs = f.span_years(data_end)                       # covered part of the test window (open-ended: to data)
        r = dict(fold=f.name, test_start=f.test_start, test_end=f.test_end, years=yrs, n_train=len(tr),
                 n_test=len(test), threshold=thr, **info, **classification_metrics(y[test], p))
        o = pd.DataFrame({"fold": f.name, "p": p, "take": take, "vote": vote_all[test], "y": y[test],
                          "pnl": pn[test], "d": df["d"].to_numpy()[test]}, index=df.index[test])
        if kind == "entry":
            r.update(trade_metrics(pn[test][take], yrs))
            r["keep_share"] = take.mean()
            if baselines:
                r.update(_entry_baselines(pn, vote_all, Xo, pat_cols, tr, test, int(take.sum()), yrs, n_random,
                                          rng))
        else:
            o["trade"] = df[trade].to_numpy()[test]
            o["opp"] = opp_all[test]
            h = None
            if hold is not None:
                st = group_starts(codes[test])
                h = df[hold].to_numpy(np.float64)[test][st]
            ev = evaluate_exit_policies(p, thr, pn[test], codes[test], opp_all[test], h, n_random, rng)
            r.update({k: v for k, v in ev.items() if not k.startswith("_")})
            r["learned_total"] = float(ev["_g_learned"].sum())
            r["learned_gain_per_year"] = r["learned_total"] / yrs if yrs > 0 else np.nan
            r["_rand_tot"] = ev["_g_random_tot"]
            r["opp_total"] = float(ev["_g_opp"].sum())
            r["hold_total"] = float(h.sum()) if h is not None else np.nan
        if model == "logit":
            c = m.coefficients(feats)
            c.insert(0, "fold", f.name)
            c["C"] = m.C
            coefs.append(c)
        rows.append(r)
        oos.append(o)
        if verbose:
            print(f"  {kind} {model} fold {f.name}: n_train={len(tr)} n_test={len(test)} thr={thr:.4f} "
                  f"auc={r['auc']:.3f}")
    F = pd.DataFrame(rows)
    O = pd.concat(oos) if oos else pd.DataFrame(columns=["fold", "p", "take", "vote", "y", "pnl"])
    C = pd.concat(coefs, ignore_index=True) if coefs else pd.DataFrame()
    pooled = _pooled(F, O, kind, baselines)
    if "_rand_tot" in F:
        F = F.drop(columns="_rand_tot")
    cal = calibration_table(O.p.to_numpy(), O.y.to_numpy(), O.pnl.to_numpy()) if len(O) else pd.DataFrame()
    return WalkForwardResult(kind, model, F, pooled, O, C, cal, skipped)


def _entry_baselines(pn, vote_all, Xo, pat_cols, tr, test, n_take, years, n_random, rng):
    """Baselines for one entry fold at the model's trade count n_take."""
    pt = pn[test]
    out = dict(all_n=len(test), all_pnl_per_trade=float(pt.mean()), all_total=float(pt.sum()),
               all_usd_per_year=float(pt.sum()) / years if years > 0 else np.nan)
    if n_take > 0:
        top = top_n(vote_all[test], n_take, rng)
        out["vote_topN_pnl_per_trade"] = float(pt[top].mean())
        out["vote_topN_total"] = float(pt[top].sum())
        rt = random_skip(pt, n_take, n_random, rng)
        out.update(random_pnl_per_trade=float(rt.mean() / n_take), random_p5=float(np.quantile(rt, 0.05) / n_take),
                   random_p95=float(np.quantile(rt, 0.95) / n_take), _rand_tot=rt)
    else:
        out.update(vote_topN_pnl_per_trade=np.nan, vote_topN_total=0.0, random_pnl_per_trade=np.nan,
                   random_p5=np.nan, random_p95=np.nan, _rand_tot=np.zeros(n_random))
    bp = best_pattern(Xo.iloc[tr], pn[tr], pat_cols) if pat_cols else None
    out["best_pattern"] = bp
    if bp is not None:
        fired = Xo[bp].to_numpy()[test] > 0
        out.update(pattern_n=int(fired.sum()), pattern_pnl_per_trade=float(pt[fired].mean()) if fired.any()
                   else np.nan, pattern_total=float(pt[fired].sum()))
    else:
        out.update(pattern_n=0, pattern_pnl_per_trade=np.nan, pattern_total=0.0)
    return out


def _pooled(F, O, kind, baselines):
    """Pooled metrics over all OOS rows / folds. years = sum of the folds' covered test spans (F.years)."""
    if F.empty:
        return pd.Series(dtype=float)
    years = float(F["years"].sum())
    s = dict(n_folds=len(F), years=years, **classification_metrics(O.y.to_numpy(), O.p.to_numpy()))
    if kind == "entry":
        s.update(trade_metrics(O.pnl.to_numpy()[O["take"].to_numpy(bool)], years))
        s["keep_share"] = float(O["take"].mean())
        if baselines and "all_total" in F:
            n = s["n_kept"]
            s.update(all_n=int(F.all_n.sum()), all_pnl_per_trade=float(O.pnl.mean()),
                     all_usd_per_year=float(O.pnl.sum()) / years,
                     vote_topN_pnl_per_trade=float(F.vote_topN_total.sum()) / n if n else np.nan)
            rt = np.sum(np.stack(F["_rand_tot"].to_list()), axis=0)
            s.update(random_pnl_per_trade=float(rt.mean() / n) if n else np.nan,
                     random_p5=float(np.quantile(rt, 0.05) / n) if n else np.nan,
                     random_p95=float(np.quantile(rt, 0.95) / n) if n else np.nan)
            pn_ = int(F.pattern_n.sum())
            s.update(pattern_n=pn_, pattern_pnl_per_trade=float(F.pattern_total.sum()) / pn_ if pn_ else np.nan)
    else:
        nt = int(F.n_trades.sum())
        s.update(n_trades=nt, learned_gain=float(F.learned_total.sum()) / nt,
                 learned_exit_share=float((F.learned_exit_share * F.n_trades).sum()) / nt,
                 opp_gain=float(F.opp_total.sum()) / nt,
                 opp_exit_share=float((F.opp_exit_share * F.n_trades).sum()) / nt, hold_gain=0.0,
                 learned_gain_per_year=float(F.learned_total.sum()) / years)
        rt = np.sum(np.stack(F["_rand_tot"].to_list()), axis=0)
        s.update(random_gain=float(rt.mean() / nt), random_p5=float(np.quantile(rt, 0.05) / nt),
                 random_p95=float(np.quantile(rt, 0.95) / nt))
        if F.hold_total.notna().all():
            hm = float(F.hold_total.sum()) / nt
            s.update(hold_net=hm, learned_net=hm + s["learned_gain"], opp_net=hm + s["opp_gain"],
                     random_net=hm + s["random_gain"])
    return pd.Series(s)


# ============================================================================================ permutation test
def _oos_score(res):
    """The $ number a permutation test compares: entries - pooled total OOS $ of the taken trades;
    exits - pooled $ gain vs hold per trade of the learned exit."""
    if res.kind == "entry":
        return float(res.pooled.get("total_usd", np.nan))
    return float(res.pooled.get("learned_gain", np.nan))


def permutation_test(data, features, n_perm=20, seed=0, real=None, verbose=False, **kw):
    """Shuffle y (jointly with its $ column) within each calendar year, rerun the whole walk-forward (model, C,
    threshold), and record the OOS $ on the TRUE outcomes. Returns dict(real, perm (array), p_value, perm_mean,
    perm_p95, n_valid) with p_value = (1 + #perm >= real) / (1 + n_perm).
    Degenerate runs are never reported as significant: if the real score is not finite (every fold skipped, no exit
    trades, ...) nothing is refitted and p_value is NaN (with a warning); a shuffle whose score is NaN counts as
    ">= real" (conservative). n_valid = number of finite shuffle scores; perm_mean / perm_p95 are over those.
    Pass `real` (a WalkForwardResult) to skip refitting the real model; other keyword arguments go to walk_forward."""
    kw = dict(kw, baselines=False)
    if real is None:
        real = walk_forward(data, features, **kw)
    r = _oos_score(real)
    if not np.isfinite(r):
        warnings.warn(f"permutation_test: the real OOS score is {r} (no fold evaluated?); p_value is NaN",
                      RuntimeWarning, stacklevel=2)
        return dict(real=r, perm=np.full(n_perm, np.nan), p_value=np.nan, perm_mean=np.nan, perm_p95=np.nan,
                    n_valid=0)
    rng = np.random.default_rng(seed)
    perm = np.empty(n_perm)
    for i in range(n_perm):                                    # 20 refits of the whole procedure
        res = walk_forward(data, features, shuffle_rng=rng, **kw)
        perm[i] = _oos_score(res)
        if verbose:
            print(f"  permutation {i + 1}/{n_perm}: {perm[i]:.1f} (real {r:.1f})")
    fin = np.isfinite(perm)
    pv = (1 + np.sum(~fin | (perm >= r))) / (1 + n_perm)
    return dict(real=r, perm=perm, p_value=float(pv), n_valid=int(fin.sum()),
                perm_mean=float(perm[fin].mean()) if fin.any() else np.nan,
                perm_p95=float(np.quantile(perm[fin], 0.95)) if fin.any() else np.nan)


# ============================================================================================ weights + scorecard
def weight_table(coefs):
    """Per feature over folds: n_folds, median and last standardized / raw coefficient, share of folds positive,
    sign_stability = share of folds whose sign equals the sign of the median (0 = never), and points of the median
    raw coefficient."""
    if coefs is None or len(coefs) == 0:
        return pd.DataFrame()
    g = coefs.groupby("feature", sort=False)
    last_fold = coefs.fold.iloc[-1]
    last = coefs[coefs.fold == last_fold].set_index("feature")
    med_std, med_raw = g.coef_std.median(), g.coef_raw.median()
    sgn = np.sign(med_raw)
    stab = coefs.assign(s=np.sign(coefs.coef_raw)).groupby("feature", sort=False).s.apply(list)
    stability = pd.Series({k: (np.mean(np.array(v) == sgn[k]) if sgn[k] != 0 else 0.0) for k, v in stab.items()})
    wt = pd.DataFrame({"n_folds": g.size(), "coef_std_median": med_std, "coef_raw_median": med_raw,
                       "coef_std_last": last.coef_std.reindex(med_std.index),
                       "coef_raw_last": last.coef_raw.reindex(med_std.index),
                       "share_pos": g.coef_raw.apply(lambda s: float((s > 0).mean())),
                       "sign_stability": stability.reindex(med_std.index)})
    wt["points_median"] = np.round(wt.coef_raw_median / POINT).astype(int)
    wt["points_last"] = np.round(wt.coef_raw_last.fillna(0) / POINT).astype(int)
    order = wt.coef_std_median.abs().sort_values(ascending=False).index
    return wt.loc[order].reset_index().rename(columns={"index": "feature"})


def points(coef):
    """Credit-scorecard points of a log-odds coefficient: round(coef / (ln 2 / 20)); +20 points doubles the odds."""
    return np.round(np.asarray(coef, np.float64) / POINT).astype(int)


def feature_unit(name, signed=()):
    """Plain-words unit of one feature (what 'one unit' means) for the scorecard."""
    with_trade = " pointing with the trade" if name in signed else ""
    if name == "(intercept)":
        return "base score (all features 0)"
    if name.startswith(("tod_", "dow_")):
        return "when the bar is in this time bucket"
    if name.startswith(("pat_", "fam_")):
        return f"when the pattern fires{with_trade}" if name in signed else "when present"
    if name.startswith(("brk_", "mom_x100")):
        return f"for a fresh break/cross{with_trade}"
    if name.startswith(("struct_", "h1_struct")) or name.endswith("ema_stack"):
        return f"per +1 state{with_trade}"
    if name.startswith("atfib"):
        return "when at a 0.382/0.5/0.618 level"
    if name.startswith("fibpos"):
        return "per full swing leg"
    if name.startswith(("dist_", "ema20_slope", "gap_open", "day_ret")) or (name.startswith("x_") and
                                                                            name.endswith("_ret")):
        return f"per average bar (R20){with_trade}"
    if name in ("rng_rel", "vol_rel", "day_range_rel"):
        return "per 1x the average"
    if name in ("mom", "h1_mom", "mom_slope3"):
        return f"per momentum point (mom14 - 100){with_trade}"
    if name.endswith("_R"):
        return "per 1R (initial risk)"
    if name == "bars_held":
        return "per bar held"
    if name == "mins_to_1645":
        return "per minute left to 16:45"
    return f"per unit{with_trade}"


def scorecard(wt, signed=(), kind="entry", use="median"):
    """Scorecard from a weight_table: one row per feature with points (per unit, from the median or last-fold raw
    coefficient), the unit and a plain-words line. Sorted by |points|."""
    if wt is None or len(wt) == 0:
        return pd.DataFrame(columns=["feature", "points", "unit", "sign_stability", "words"])
    col = "coef_raw_median" if use == "median" else "coef_raw_last"
    target = "the trade reaching its target (y=1)" if kind == "entry" else "exiting now beating holding"
    df = pd.DataFrame({"feature": wt.feature, "coef": wt[col].fillna(0.0)})
    df["points"] = points(df.coef)
    df["unit"] = [feature_unit(f, set(signed)) for f in df.feature]
    df["sign_stability"] = wt.sign_stability.to_numpy()
    df["words"] = [f"{f}: {p:+d} points {u}" for f, p, u in zip(df.feature, df.points, df.unit)]
    df = df.iloc[np.argsort(-np.abs(df.points.to_numpy()), kind="stable")].reset_index(drop=True)
    df.attrs["note"] = f"+20 points doubles the odds of {target}; points are per unit of each feature"
    return df

# ------------------------------------------------------------------ published weighting approaches (approaches/)
_CTX = {}


class ScorerModel:
    """Adapter: any approaches.scorer_api Scorer (model name 'sc:<scorer name>') inside the walk-forward. Gets the
    oriented features as a DataFrame with their names and a meta frame (t, t_end, d, market, year, payoff, trade_id)
    built from the training rows only."""

    def __init__(self, name, kind, **params):
        import sys as _sys, os as _os
        here = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "approaches")
        if here not in _sys.path:
            _sys.path.insert(0, here)
        import scorer_api
        import approach_hand, approach_stat, approach_ml   # noqa: F401  (registration)
        self.sc = scorer_api.REGISTRY[name](task=kind, **params)
        self.kind = kind

    def _frame(self, X):
        return pd.DataFrame(np.asarray(X), columns=_CTX["feats"])

    def fit_idx(self, X, y, w, pnl, idx):
        c = _CTX
        meta = pd.DataFrame({"t": pd.DatetimeIndex(c["t"][idx]), "t_end": pd.DatetimeIndex(c["t_end"][idx]),
                             "d": c["d"][idx], "year": c["year"][idx],
                             ("pnl_usd" if self.kind == "entry" else "exit_gain_usd"): pnl[idx],
                             "trade_id": c["codes"][idx]})
        if c.get("market") is not None:
            meta["market"] = c["market"][idx]
        self.sc.fit(self._frame(X[idx]), y[idx], _norm(w[idx]), meta)
        return self

    def predict(self, X):
        return np.asarray(self.sc.predict_proba(self._frame(X)), float)

    def weights_table(self):
        return self.sc.weights_table()

