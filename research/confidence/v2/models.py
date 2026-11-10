"""
v2/models.py - LEARNED CONFIDENCE WEIGHTS on the v2 dataset (meta-labeling: the user's pullback rule union proposes
every event, a model scores it, the walk-forward keeps the events whose score clears a threshold chosen inside
training).

DATA   v2/out/v2_events_{NQ,ES,YM}_{tf}.parquet pooled per timeframe (MNQ + MES + MYM; features are in R20 units and
       oriented + = with the trade; market one-hots mkt_ES / mkt_YM and cost_R / cost_bar tell the markets apart).
       Every row is entirely before the locked holdout (signal bar and exit < 2025-06-30 18:00; asserted).
EXITS  per tf: 'hold' (stop only, to 16:45), the stage-3 best opposite-evidence exit (60 / 5 min: opp3_1b,
       15 min: opp4_1b) and 'ema_cross'. One model per exit (the label is what the trade makes under that exit).
TARGETS  cls = P(net R > 0) with sample weight |R| (clipped at 5) x uniqueness (walkforward.sample_weights: overlap
       within a market and the same bar/side in several markets share weight);  reg = least squares on R clipped at
       +-5R (winsorized = robust to the few huge trades) with uniqueness weights;  edge (extra, not in the agreed
       design) = the same regression on R minus the matched drift null's mean R (nmR), so the model cannot earn by
       learning drift / hour / stop size.
LADDER  M0 equal-weight count of the SIGNALS below (agree +1, disagree -1; no training; the count cut-off is chosen on
          the training years)
        M1 SIGN-CONSTRAINED linear scorecard on the same SIGNALS (agree weights >= 0, disagree weights >= 0 on a -1
          indicator, cost_R <= 0, market one-hots free; L2 penalty chosen on inner validation; scipy L-BFGS-B) ->
          points table (cls: 20 points doubles the odds; reg: hundredths of R)
        M2 L2 logistic (cls) / ridge (reg) on all raw features + rule flags + one-hots (winsorized +-20, NaN -> 0,
          standardized; C / alpha chosen on inner validation)
        M3 HistGradientBoosting with MONOTONE constraints (more agreement can only raise the score: MONO_POS +1,
          MONO_NEG -1, others free), depth 3, min leaf LEAF[tf], number of trees chosen on inner validation
        M4 the same HistGradientBoosting unconstrained (reference only, never chosen as 'best')
WALK-FORWARD  expanding yearly folds 2013 .. 2024 + 2025H1 (walkforward.make_folds / train_mask: training rows end a
       day (PURGE) before the test year). Inner split: validation = the last 2 training years, inner training =
       the earlier years purged against the validation start. Hyper-parameters by validation loss; KEEP SHARE q from
       KEEP_GRID by the mean net R (clipped +-10) of the top-q validation rows (q = 1 means 'take everything');
       the model is refit on all training rows and the test threshold = the (1 - q) quantile of its scores on the
       training rows. Rolling variant: train_years=5 (the last 5 calendar years only).
BASELINES (per kept trade, same market and exit; reported as edges with week-clustered t)
       drift  = mean of 100 matched rows of the TREND POOL (v2_trend_*: being in the trend at that time without a
                setup) with the same side, session year, entry hour and stop-size quintile (ema50_check.matched_draws)
       rskip  = MATCHED RANDOM SKIP: the expectation of drawing the same number of trades from the year's events of
                the same market, side, stop-size decile (within market-year) and time-of-day block = the mean of
                that cell (exact expectation of the draw; the clustered t of pnl - cell mean is its test)
       all    = every event (the fold's test rows, no model)
REPORTING  net $ per micro and R per trade, trades/yr, by market (MNQ / MES / MYM / pooled) and side, by year
       2013..2025H1 and the windows 2018+, 2022+, 2013-20, 2021-25H1, all, all w/o top 10 days (the group's own 10
       best days removed; nulls of the same remaining trades), all w/o 2025H1; AUC (score vs R > 0) only as a side
       column. Every configuration is logged to out/trials.csv (module 'v2-models').
OUTPUTS (v2/out)  models_results.csv (one row per config x market x side x span), models_folds.csv (per fold:
       hyper-parameters, keep share, threshold, AUC), models_points.csv (M0/M1 weights per fold), models_scores_{tf}
       .parquet (OOS score and take per config, row = event key), oos_<name>.parquet (kept trades of the 3 best
       configs, for stage 5: market, t_entry, t_exit, session, risk_usd, pnl_usd + extras).

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 -u \
      v2/models.py run --tf 60 [--models M0,M1,M2,M3,M4] [--targets cls,reg] [--exits hold,opp3_1b,ema_cross]
      [--rolling 5] [--no-log]
  ... v2/models.py trunc-check --tf 60      (real-data truncation test of the decisions)
  ... v2/models.py finalize                  (pick the 3 best configs, write oos_*.parquet, hand-check them)
"""
import argparse
import json
import math
import os
import time
import warnings
import zlib

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score

import dataset as ds
import ema50_check as ec
import walkforward as wf

OUT = ds.OUT
MARKETS = ("NQ", "ES", "YM")
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
EXITS_BY_TF = {60: ("hold", "opp3_1b", "ema_cross"), 15: ("hold", "opp4_1b", "ema_cross"),
               5: ("hold", "opp3_1b", "ema_cross")}
MODELS = ("M0", "M1", "M2", "M3", "M4")
TARGETS = ("cls", "reg")                            # "edge" is available as an extra target
CLIP_R = 5.0                      # target clip (reg) and |R| weight clip (cls)
CLIP_SEL = 10.0                   # R clip for choosing the keep share on validation
WINSOR = 20.0                     # feature winsorization for linear models
KEEP_GRID = (0.1, 0.2, 0.3, 0.5, 0.75, 1.0)
N_DRAWS = 100
LEAF = {60: 300, 15: 1000, 5: 3000}
HGB = dict(max_depth=3, learning_rate=0.1, max_iter=200, l2_regularization=1.0, max_bins=255,
           early_stopping=False, random_state=0)
MIN_ITER = 10
LAM_GRID = (1e-4, 1e-3, 1e-2, 1e-1)                  # M1 L2 penalty on standardized columns
C_GRID = (1e-3, 1e-2, 1e-1, 1.0)                     # M2 logistic
ALPHA_GRID = (1e-4, 1e-3, 1e-2, 1e-1)                # M2 ridge: alpha = a * n rows (penalty per row)
POINT = wf.POINT                                     # ln2/20: 20 points double the odds
YEAR_SPANS = [str(y) for y in range(2013, 2025)] + ["2025H1"]
WIN_SPANS = ["2018+", "2022+", "2013-20", "2021-25H1", "all", "all w/o top 10 days", "all w/o 2025H1"]
OOS_END = pd.Timestamp("2025-07-01")

# ------------------------------------------------------------------------------------------------ signals
# (name, kind, description, function of the event frame -> bool). kind 'agree' -> column = 1 when true;
# 'disagree' -> column = -1 when true. M0 = sum of columns; M1 = non-negative weights on every column.
SIGNALS = [
    ("trend5", "agree", "5-min EMA 8/20/50 stack + EMA50 slope with the trade", lambda E: E.m5_trend > 0),
    ("trend15", "agree", "15-min trend with the trade", lambda E: E.m15_trend > 0),
    ("trend60", "agree", "60-min trend with the trade", lambda E: E.m60_trend > 0),
    ("struct15", "agree", "15-min swings: higher highs AND higher lows (mirror for shorts)", lambda E: E.m15_struct > 0),
    ("struct60", "agree", "60-min swings with the trade", lambda E: E.m60_struct > 0),
    ("mom5_up", "agree", "5-min Momentum(14) rising over 3 bars (with the trade)", lambda E: E.m5_mslope3 > 0),
    ("mom15_up", "agree", "15-min Momentum(14) rising over 3 bars", lambda E: E.m15_mslope3 > 0),
    ("mom60_up", "agree", "60-min Momentum(14) rising over 3 bars", lambda E: E.m60_mslope3 > 0),
    ("vwap", "agree", "close on the trade's side of VWAP", lambda E: E.vwap_side > 0),
    ("candles", "agree", "more candle patterns with than against the trade (last 3 bars)",
     lambda E: E.pat_with3 > E.pat_against3),
    ("rev_low", "agree", "reversal candle at the pullback low (or the bar after)", lambda E: E.rev_at_low == 1),
    ("room60", "agree", ">= 1 R20 room to the 60-min swing on the target side", lambda E: E.m60_sw_room >= 1),
    ("room_day", "agree", ">= 1 R20 room to the high (low) of day", lambda E: E.day_room >= 1),
    ("trig5", "agree", "a 5-min pullback trigger the same way in the last 6 five-min bars", lambda E: E.mtf_trig5 == 1),
    ("mom5_bar", "agree", "last 5-min bar: Momentum up and EMA8 > EMA20", lambda E: E.mtf_mom5 == 1),
    ("multi_rule", "agree", "2+ pullback rules fire on the bar", lambda E: E.n_rules >= 2),
    ("pb_div", "agree", "pullback detector: momentum divergence at the pullback low", lambda E: E.pb_div == 1),
    ("x_trend5", "disagree", "5-min trend against the trade", lambda E: E.m5_trend < 0),
    ("x_trend15", "disagree", "15-min trend against the trade", lambda E: E.m15_trend < 0),
    ("x_trend60", "disagree", "60-min trend against the trade", lambda E: E.m60_trend < 0),
    ("x_struct15", "disagree", "15-min swings against the trade", lambda E: E.m15_struct < 0),
    ("x_struct60", "disagree", "60-min swings against the trade", lambda E: E.m60_struct < 0),
    ("x_candles", "disagree", "more candle patterns against than with the trade", lambda E: E.pat_against3 > E.pat_with3),
    ("x_res60", "disagree", "60-min swing on the target side less than 0.5 R20 away (into resistance)",
     lambda E: (E.m60_sw_room >= 0) & (E.m60_sw_room < 0.5)),
    ("x_hod", "disagree", "within 0.25 R20 of the high (low) of day", lambda E: E.day_room < 0.25),
]
SIG_COLS = [f"sig_{n}" for n, *_ in SIGNALS]
M1_EXTRA = ["cost_R", "mkt_ES", "mkt_YM"]
MONO_POS = {"m5_trend", "m15_trend", "m60_trend", "m5_struct", "m15_struct", "m60_struct", "m5_mslope3",
            "m15_mslope3", "m60_mslope3", "n_tf_agree", "mtf_trend60", "mtf_trig5", "mtf_mom5", "mtf_score",
            "pat_with3", "rev_at_low", "vwap_side", "pb_div", "n_rules"}
MONO_NEG = {"pat_against3", "cost_R", "cost_bar"}


def signal_frame(E):
    out = {}
    for (n, kind, _, f) in SIGNALS:
        v = np.asarray(f(E), bool).astype(np.float32)
        out[f"sig_{n}"] = v if kind == "agree" else -v
    return pd.DataFrame(out, index=E.index)


def raw_features():
    return ds.feature_columns() + ds.FLAGS + ["n_rules", "mkt_ES", "mkt_YM"]


def m1_columns():
    return SIG_COLS + M1_EXTRA


def m1_bounds():
    return [(0.0, None)] * len(SIG_COLS) + [(None, 0.0), (None, None), (None, None)]


# ------------------------------------------------------------------------------------------------ data
def micro(sym):
    return MICRO.get(sym, sym)


def load_market(sym, tf, exits, n_draws=N_DRAWS):
    """Events of one market with the drift null (nm_<x>, nmR_<x>) and the matched random skip (rs_<x>, rsR_<x>)."""
    E = pd.read_parquet(ds.events_path(sym, tf))
    ok = (E.risk_usd.to_numpy() > 0) & (E.past_stop.to_numpy() == 0)
    for x in exits:
        ok &= np.isfinite(E[f"R_{x}"].to_numpy(np.float64))
    E = E.loc[ok].reset_index(drop=True)       # a handful of rows (entry gapped past the stop): no trade
    P = pd.read_parquet(ds.trend_path(sym, tf))
    cut = wf.HOLDOUT_SESSION_START
    for x in exits:
        assert (pd.DatetimeIndex(E[f"t_exit_{x}"]) < cut).all() and (pd.DatetimeIndex(E.t) < cut).all(), \
            "holdout rows in the events file"
    A = ec.add_risk_bucket(pd.concat([E[["session", "year", "risk_usd"]], P[["session", "year", "risk_usd"]]],
                                     ignore_index=True))
    E["rb"] = A.rb.to_numpy()[:len(E)]
    P["rb"] = A.rb.to_numpy()[len(E):]
    idx, _ = ec.matched_draws(E, P, n_draws=n_draws, seed=zlib.crc32(f"{sym}{tf}".encode()))
    prisk = P.risk_usd.to_numpy(np.float64)
    E["dec"] = E.groupby("year").risk_usd.transform(
        lambda s: pd.qcut(s.rank(method="first"), 10, labels=False)).astype(np.int8)
    cell = [E.year, E.d, E.dec, E.tod_block]
    for x in exits:
        pp = P[f"pnl_{x}"].to_numpy(np.float64)
        E[f"nm_{x}"] = pp[idx].mean(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            pr = np.where(prisk > 0, pp / prisk, np.nan)
        E[f"nmR_{x}"] = np.nanmean(pr[idx], 1)
        E[f"rs_{x}"] = E.groupby(cell)[f"pnl_{x}"].transform("mean")
        E[f"rsR_{x}"] = E.groupby(cell)[f"R_{x}"].transform("mean")
    del P, idx
    return E


def load_tf(tf, exits=None, markets=MARKETS):
    exits = EXITS_BY_TF[tf] if exits is None else exits
    keep = (["market", "tf", "t", "d", "stop", "t_entry", "entry", "risk_usd", "session", "year", "hour", "tod_block",
             "dec", "rb"] + ds.FLAGS + ["n_rules"] + ds.feature_columns() +
            [f"{p}_{x}" for x in exits for p in ("pnl", "R", "bars", "kind", "t_exit", "nm", "nmR", "rs", "rsR")])
    parts = []
    for sym in markets:
        E = load_market(sym, tf, exits)
        parts.append(E[[c for c in keep if c in E.columns]])
        del E
    D = pd.concat(parts, ignore_index=True)
    D["mkt_ES"] = (D.market == "ES").astype(np.float32)
    D["mkt_YM"] = (D.market == "YM").astype(np.float32)
    D = pd.concat([D, signal_frame(D)], axis=1)
    D = D.sort_values(["t", "market", "d"], kind="stable").reset_index(drop=True)
    return D


def linear_matrix(D, cols):
    X = D[cols].to_numpy(np.float64)
    X = np.clip(X, -WINSOR, WINSOR)
    return np.nan_to_num(X, nan=0.0)


def tree_matrix(D, cols):
    X = D[cols].to_numpy(np.float32)
    return np.clip(X, -1e4, 1e4)


# ------------------------------------------------------------------------------------------------ models
def _sigmoid(z):
    return 0.5 * (1 + np.tanh(0.5 * z))


def w_logloss(y, p, w):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return float(np.average(-(y * np.log(p) + (1 - y) * np.log(1 - p)), weights=w))


def w_mse(y, f, w):
    return float(np.average((y - f) ** 2, weights=w))


class LinScore:
    """Bounded L2-penalized linear model (cls: logistic, reg: least squares) on standardized columns.
    bounds: list of (lo, hi) per column (None = free); the intercept is free. coef_ is in the original units."""

    def __init__(self, kind, lam, bounds):
        self.kind, self.lam, self.bounds = kind, lam, bounds

    def fit(self, X, y, w):
        w = np.asarray(w, np.float64)
        w = w / w.mean()
        n, p = X.shape
        s = X.std(0)
        s[s == 0] = 1.0
        Z = X / s
        lam = self.lam

        def f(b):
            eta = Z @ b[:-1] + b[-1]
            if self.kind == "cls":
                loss = np.mean(w * (np.logaddexp(0, eta) - y * eta))
                r = w * (_sigmoid(eta) - y)
            else:
                r0 = eta - y
                loss = 0.5 * np.mean(w * r0 ** 2)
                r = w * r0
            g = np.r_[Z.T @ r / n + 2 * lam * b[:-1], r.mean()]
            return loss + lam * np.sum(b[:-1] ** 2), g

        b0 = np.zeros(p + 1)
        if self.kind == "reg":
            b0[-1] = np.average(y, weights=w)
        res = minimize(f, b0, jac=True, method="L-BFGS-B", bounds=list(self.bounds) + [(None, None)],
                       options=dict(maxiter=2000))
        self.coef_ = res.x[:-1] / s
        self.intercept_ = res.x[-1]
        return self

    def decision(self, X):
        return X @ self.coef_ + self.intercept_

    def predict(self, X):
        z = self.decision(X)
        return _sigmoid(z) if self.kind == "cls" else z


class StdLinear:
    """M2: standardized L2 logistic (cls) or ridge (reg)."""

    def __init__(self, kind, c):
        self.kind, self.c = kind, c

    def fit(self, X, y, w):
        w = np.asarray(w, np.float64) / np.mean(w)
        self.mu, self.sd = X.mean(0), X.std(0)
        self.sd[self.sd == 0] = 1.0
        Z = (X - self.mu) / self.sd
        if self.kind == "cls":
            self.m = LogisticRegression(C=self.c, max_iter=1000).fit(Z, y, sample_weight=w)
        else:
            self.m = Ridge(alpha=self.c * len(Z)).fit(Z, y, sample_weight=w)
        return self

    def predict(self, X):
        Z = (X - self.mu) / self.sd
        return self.m.predict_proba(Z)[:, 1] if self.kind == "cls" else self.m.predict(Z)


def hgb(kind, leaf, mono=None, n_iter=None):
    prm = dict(HGB, min_samples_leaf=leaf)
    if n_iter is not None:
        prm["max_iter"] = int(n_iter)
    if mono is not None:
        prm["monotonic_cst"] = list(mono)
    if kind == "cls":
        return HistGradientBoostingClassifier(**prm)
    return HistGradientBoostingRegressor(loss="squared_error", **prm)


def hgb_predict(m, X):
    return m.predict_proba(X)[:, 1] if isinstance(m, HistGradientBoostingClassifier) else m.predict(X)


def mono_vector(cols):
    return [1 if c in MONO_POS else -1 if c in MONO_NEG else 0 for c in cols]


# ------------------------------------------------------------------------------------------------ fold logic
def choose_keep(score, r_sel, grid=KEEP_GRID):
    """Keep share q (from grid) whose top-q rows by score have the highest mean r_sel (ties at the cut kept)."""
    best = (-np.inf, 1.0)
    o = np.argsort(-score, kind="stable")
    cs = np.cumsum(r_sel[o])
    n = len(score)
    for q in grid:
        k = max(int(math.ceil(q * n)), 1)
        m = cs[k - 1] / k
        if m > best[0] + 1e-12:
            best = (m, q)
    return best[1], best[0]


def threshold_for(train_scores, q):
    return -np.inf if q >= 1.0 else float(np.quantile(train_scores, 1.0 - q))


def fit_fold(model, target, Xa, y, w, tr, it, va, tf, cols):
    """Fit one fold. Returns (predict function of the final model, validation scores, info dict)."""
    target = "reg" if target == "edge" else target
    info = {}
    if model in ("M1", "M2"):
        grid = LAM_GRID if model == "M1" else (C_GRID if target == "cls" else ALPHA_GRID)
        best = (np.inf, None, None)
        for g in grid:
            m = (LinScore(target, g, m1_bounds()) if model == "M1" else StdLinear(target, g)).fit(Xa[it], y[it], w[it])
            pv = m.predict(Xa[va])
            loss = w_logloss(y[va], pv, w[va]) if target == "cls" else w_mse(y[va], pv, w[va])
            if loss < best[0]:
                best = (loss, g, pv)
        info.update(hp=best[1], val_loss=best[0])
        final = (LinScore(target, best[1], m1_bounds()) if model == "M1" else StdLinear(target, best[1])).fit(
            Xa[tr], y[tr], w[tr])
        if model == "M1":
            info["coef"] = final.coef_.tolist()
            info["intercept"] = float(final.intercept_)
        return final.predict, best[2], info
    mono = mono_vector(cols) if model == "M3" else None
    m = hgb(target, LEAF[tf], mono).fit(Xa[it], y[it], sample_weight=w[it] / w[it].mean())
    stages = m.staged_predict_proba(Xa[va]) if target == "cls" else m.staged_predict(Xa[va])
    best = (np.inf, None, None)
    for k, pv in enumerate(stages, 1):
        pv = pv[:, 1] if target == "cls" else pv
        if k < MIN_ITER:
            continue
        loss = w_logloss(y[va], pv, w[va]) if target == "cls" else w_mse(y[va], pv, w[va])
        if loss < best[0]:
            best = (loss, k, pv)
    info.update(hp=best[1], val_loss=best[0])
    final = hgb(target, LEAF[tf], mono, best[1]).fit(Xa[tr], y[tr], sample_weight=w[tr] / w[tr].mean())
    return (lambda X: hgb_predict(final, X)), best[2], info


def walk(D, tf, exit, model, target, train_years=None, folds=None, min_train_years=3, purge=wf.PURGE,
         verbose=True):
    """Walk-forward of one configuration. Returns (score Series, take Series) over D's test rows and fold info."""
    folds = wf.make_folds() if folds is None else folds
    for f in folds:
        wf.check_holdout(f)
    t = pd.DatetimeIndex(D.t).as_unit("ns")
    te = pd.DatetimeIndex(D[f"t_exit_{exit}"]).as_unit("ns")
    if (t >= wf.HOLDOUT_SESSION_START).any() or (te >= wf.HOLDOUT_SESSION_START).any():
        raise wf.HoldoutError("rows reach the locked holdout")
    year = t.year.to_numpy()
    R = D[f"R_{exit}"].to_numpy(np.float64)
    rsel = np.clip(R, -CLIP_SEL, CLIP_SEL)
    wu = wf.sample_weights(pd.DataFrame({"t": t, "t_end": te, "market": D.market.to_numpy(), "d": D.d.to_numpy()}))
    if target == "cls":
        y = (R > 0).astype(np.float64)
        w = wu * np.minimum(np.abs(R), CLIP_R)
    elif target == "edge":                       # R minus the matched drift null's mean R (cannot learn drift)
        y = np.clip(R - D[f"nmR_{exit}"].to_numpy(np.float64), -CLIP_R, CLIP_R)
        w = wu.copy()
    else:
        y = np.clip(R, -CLIP_R, CLIP_R)
        w = wu.copy()
    w = np.maximum(w, 1e-6)
    if model == "M0":
        cols, Xa = SIG_COLS, D[SIG_COLS].to_numpy(np.float64)
    elif model == "M1":
        cols = m1_columns()
        Xa = linear_matrix(D, cols)
    elif model == "M2":
        cols = raw_features()
        Xa = linear_matrix(D, cols)
    else:
        cols = raw_features()
        Xa = tree_matrix(D, cols)
    score = np.full(len(D), np.nan)
    take = np.zeros(len(D), bool)
    infos = []
    for f in folds:
        tc0 = time.time()
        test = np.flatnonzero((t >= f.test_start) & (t < f.test_end))
        tr = np.flatnonzero(wf.train_mask(t, te, f.test_start, f.test_end, f.train_end, purge=purge))
        if train_years is not None:
            tr = tr[year[tr] >= f.test_start.year - int(train_years)]
        if len(test) == 0 or len(np.unique(year[tr])) < min_train_years:
            continue
        Y = int(year[tr].max())
        val_start = pd.Timestamp(Y - 1, 1, 1)
        va = tr[year[tr] >= Y - 1]
        it = tr[(year[tr] < Y - 1) & (te[tr] <= val_start - purge)]
        info = dict(fold=f.name, n_train=len(tr), n_test=len(test), n_inner=len(it), n_val=len(va))
        if model == "M0":
            s_tr = Xa[tr].sum(1)
            cuts = np.unique(s_tr)
            best = (-np.inf, -np.inf, 1.0)
            for c in cuts:
                m = s_tr >= c
                if m.mean() < KEEP_GRID[0]:
                    continue
                v = rsel[tr][m].mean()
                if v > best[0] + 1e-12:
                    best = (v, c, m.mean())
            thr, q = best[1], best[2]
            s_te = Xa[test].sum(1)
            info.update(hp=np.nan, keep_q=q, val_sel_R=best[0])
        else:
            pred, pv, fi = fit_fold(model, target, Xa, y, w, tr, it, va, tf, cols)
            info.update(fi)
            q, vR = choose_keep(pv, rsel[va])
            s_trn = pred(Xa[tr])
            thr = threshold_for(s_trn, q)
            s_te = pred(Xa[test])
            info.update(keep_q=q, val_sel_R=vR)
        score[test] = s_te
        take[test] = s_te >= thr
        yy = (R[test] > 0).astype(int)
        info.update(threshold=thr, test_keep=float(take[test].mean()),
                    auc=roc_auc_score(yy, s_te) if 0 < yy.mean() < 1 and np.ptp(s_te) > 0 else np.nan,
                    secs=round(time.time() - tc0, 1))
        infos.append(info)
        if verbose:
            print(f"    {f.name}: train {len(tr):,} test {len(test):,} hp {info.get('hp')} q {info['keep_q']:.2f} "
                  f"kept {take[test].mean():.1%} auc {info['auc']:.3f} ({info['secs']}s)", flush=True)
    return score, take, infos


# ------------------------------------------------------------------------------------------------ reporting
def _market_years(D):
    """first OOS-relevant session date per market (data start)."""
    return {m: pd.DatetimeIndex(D.session[D.market == m]).min() for m in D.market.unique()}


def span_masks(sess):
    s = pd.DatetimeIndex(sess)
    y = s.year
    out = {str(yy): np.asarray(y == yy) for yy in range(2013, 2025)}
    out["2025H1"] = np.asarray(y == 2025)
    out.update({"2018+": np.asarray(s >= "2018-01-01"), "2022+": np.asarray(s >= "2022-01-01"),
                "2013-20": np.asarray(s < "2021-01-01"), "2021-25H1": np.asarray(s >= "2021-01-01"),
                "all": np.ones(len(s), bool), "all w/o 2025H1": np.asarray(s < "2025-01-01")})
    return out


def span_years(sp, first):
    """Years an OOS span covers for a market whose data starts at `first` (OOS starts 2013, ends 2025-06-30)."""
    lo = {"2018+": 2018, "2022+": 2022, "2021-25H1": 2021}.get(sp, 2013)
    hi = {"2013-20": 2021.0, "all w/o 2025H1": 2025.0}.get(sp, 2025.5)
    if sp in YEAR_SPANS:
        lo = 2025 if sp == "2025H1" else int(sp)
        hi = lo + (0.5 if sp == "2025H1" else 1.0)
    start = max(lo, first.year + (first.dayofyear - 1) / 365.25)
    return max(hi - start, 0.0)


def top10(p, sess, m, k=10):
    day = pd.Series(p[m]).groupby(sess[m]).sum()
    top = day.sort_values(ascending=False).index[:k]
    return m & ~np.isin(sess, top.to_numpy())


def report(D, take, exit, key, sides=("all", "long", "short")):
    """Rows: market (MNQ/MES/MYM/pooled) x side x span. take: bool mask over D (kept OOS trades)."""
    p = D[f"pnl_{exit}"].to_numpy(np.float64)
    R = D[f"R_{exit}"].to_numpy(np.float64)
    nm = D[f"nm_{exit}"].to_numpy(np.float64)
    rs = D[f"rs_{exit}"].to_numpy(np.float64)
    nmR = D[f"nmR_{exit}"].to_numpy(np.float64)
    rsR = D[f"rsR_{exit}"].to_numpy(np.float64)
    sess = pd.DatetimeIndex(D.session).to_numpy()
    week = pd.factorize(pd.DatetimeIndex(D.session).to_period("W"))[0]
    SP = span_masks(D.session)
    first = _market_years(D)
    d = D.d.to_numpy()
    rows = []
    groups = [(micro(m), D.market.to_numpy() == m, [first[m]]) for m in MARKETS if m in first]
    groups.append(("pooled", np.ones(len(D), bool), list(first.values())))
    for gname, gm, firsts in groups:
        for side in sides:
            sm = gm & take & (np.ones(len(D), bool) if side == "all" else (d > 0) if side == "long" else (d < 0))
            spans = YEAR_SPANS + WIN_SPANS if side == "all" else WIN_SPANS
            for sp in spans:
                if sp == "all w/o top 10 days":
                    m = top10(p, sess, sm)
                    yrs_sp = "all"
                else:
                    m = sm & SP[sp]
                    yrs_sp = sp
                n = int(m.sum())
                if gname == "pooled":                  # trades per year summed over the markets
                    py = sum(int((m & (D.market.to_numpy() == mk)).sum()) / span_years(yrs_sp, f)
                             for mk, f in first.items() if span_years(yrs_sp, f) > 0)
                else:
                    yrs = span_years(yrs_sp, firsts[0])
                    py = n / yrs if yrs > 0 else np.nan
                r = dict(key, market=gname, side=side, span=sp, n=n, per_year=py)
                if n:
                    ed, er = p[m] - nm[m], p[m] - rs[m]
                    r.update(usd=p[m].mean(), R=R[m].mean(), drift_usd=nm[m].mean(), edge_drift=ed.mean(),
                             tc_drift=ec.cluster_t(ed, week[m]), rskip_usd=rs[m].mean(), edge_rskip=er.mean(),
                             tc_rskip=ec.cluster_t(er, week[m]), win=(p[m] > 0).mean())
                    eRd, eRr = R[m] - nmR[m], R[m] - rsR[m]          # the same in R (what $-risk sizing earns)
                    r.update(R_drift=np.nanmean(nmR[m]), edgeR_drift=np.nanmean(eRd),
                             tcR_drift=ec.cluster_t(np.nan_to_num(eRd), week[m]), R_rskip=rsR[m].mean(),
                             edgeR_rskip=eRr.mean(), tcR_rskip=ec.cluster_t(eRr, week[m]))
                rows.append(r)
    return rows


def cfg_name(tf, exit, model, target, variant="exp"):
    return f"{tf}|{exit}|{model}|{target}|{variant}"


def _merge_csv(path, new, keys):
    if os.path.exists(path):
        old = pd.read_csv(path)
        old = old[~old.cfg.isin(set(new.cfg))]
        new = pd.concat([old, new], ignore_index=True)
    new.to_csv(path, index=False)


def run(tf, models=MODELS, targets=TARGETS, exits=None, rolling=None, log=True):
    exits = EXITS_BY_TF[tf] if exits is None else exits
    t0 = time.time()
    D = load_tf(tf, exits)
    print(f"tf {tf}: {len(D):,} pooled events loaded ({time.time() - t0:.0f}s)", flush=True)
    sp = os.path.join(OUT, f"models_scores_{tf}.parquet")
    S = pd.read_parquet(sp) if os.path.exists(sp) else D[["market", "t", "d"]].copy()
    if len(S) != len(D) or not (S.t.to_numpy() == D.t.to_numpy()).all():
        S = D[["market", "t", "d"]].copy()
    variant = "exp" if rolling is None else f"roll{rolling}"
    res_rows, fold_rows, pt_rows = [], [], []
    oos = pd.DatetimeIndex(D.t) >= pd.Timestamp("2013-01-01")
    for x in exits:
        # all-events baseline (no model): every OOS-period event
        allm = oos.copy()
        res_rows += report(D, allm, x, dict(cfg=cfg_name(tf, x, "ALL", "-", "-"), tf=tf, exit=x, model="ALL",
                                            target="-", variant="-"))
        for model in models:
            for target in (("-",) if model == "M0" else targets):
                name = cfg_name(tf, x, model, target, variant)
                tc0 = time.time()
                print(f"  {name}", flush=True)
                score, take, infos = walk(D, tf, x, model, target if target != "-" else "cls", train_years=rolling)
                S[f"s|{name}"] = score.astype(np.float32)
                S[f"k|{name}"] = take
                key = dict(cfg=name, tf=tf, exit=x, model=model, target=target, variant=variant)
                rr = report(D, take, x, key)
                res_rows += rr
                for inf in infos:
                    fr = dict(key, **{k: v for k, v in inf.items() if k not in ("coef", "intercept")})
                    fold_rows.append(fr)
                    if model in ("M0", "M1"):
                        cf = inf.get("coef", [1.0] * len(SIG_COLS))
                        cols = SIG_COLS if model == "M0" else m1_columns()
                        for c, v in zip(cols, cf):
                            pt_rows.append(dict(key, fold=inf["fold"], column=c, coef=v))
                a = {(r["market"], r["side"], r["span"]): r for r in rr}
                P_ = a[("pooled", "all", "all")]
                aucs = [i["auc"] for i in infos if np.isfinite(i.get("auc", np.nan))]
                print(f"  -> {name}: kept {P_['n']:,} ({P_['per_year']:.0f}/yr) ${P_.get('usd', np.nan):+.2f}/trade "
                      f"R {P_.get('R', np.nan):+.3f} edge drift {P_.get('edge_drift', np.nan):+.2f} "
                      f"(tc {P_.get('tc_drift', np.nan):.2f}) edge rskip {P_.get('edge_rskip', np.nan):+.2f} "
                      f"(tc {P_.get('tc_rskip', np.nan):.2f}) auc {np.mean(aucs) if aucs else np.nan:.3f} "
                      f"({time.time() - tc0:.0f}s)", flush=True)
                if log:
                    import run_pipeline as rp                                 # noqa: PLC0415
                    mk = "; ".join(f"{g} ${a[(g, 'all', 'all')].get('usd', np.nan):+.2f} n {a[(g, 'all', 'all')]['n']}"
                                   for g in ("MNQ", "MES", "MYM") if (g, "all", "all") in a)
                    allr = a[("pooled", "all", "all")]
                    rp.log_trial(module="v2-models", scope=f"pooled{tf}", model=f"{model}/{target}/{variant}",
                                 target=x, n_folds=len(infos), oos_rows=int(oos.sum()),
                                 oos_auc=round(float(np.mean(aucs)), 4) if aucs else "",
                                 oos_kept=allr["n"], oos_keep_share=round(allr["n"] / max(int(oos.sum()), 1), 4),
                                 oos_usd_total=round(float(allr.get("usd", 0) * allr["n"]), 1),
                                 oos_usd_per_trade=round(float(allr.get("usd", np.nan)), 2),
                                 oos_usd_per_year=round(float(allr.get("usd", np.nan) * allr["per_year"]), 1),
                                 baseline_usd_per_trade=round(float(allr.get("rskip_usd", np.nan)), 2),
                                 runtime_s=round(time.time() - tc0),
                                 parameters=json.dumps(dict(tf=tf, exit=x, model=model, target=target,
                                                            variant=variant, keep_grid=KEEP_GRID, leaf=LEAF[tf])),
                                 note=f"baseline = matched random skip; edge drift {allr.get('edge_drift', np.nan):.2f}"
                                      f" tc {allr.get('tc_drift', np.nan):.2f}; edge rskip "
                                      f"{allr.get('edge_rskip', np.nan):.2f} tc {allr.get('tc_rskip', np.nan):.2f}; "
                                      f"{mk}")
                # save as we go
                _merge_csv(os.path.join(OUT, "models_results.csv"), pd.DataFrame(res_rows), ["cfg"])
                if fold_rows:
                    _merge_csv(os.path.join(OUT, "models_folds.csv"), pd.DataFrame(fold_rows), ["cfg"])
                if pt_rows:
                    _merge_csv(os.path.join(OUT, "models_points.csv"), pd.DataFrame(pt_rows), ["cfg"])
                S.to_parquet(sp)
    print(f"tf {tf} done ({time.time() - t0:.0f}s)", flush=True)
    return D, S


def rereport(tf):
    """Rebuild the models_results.csv rows of timeframe tf from the saved OOS takes (no refitting)."""
    exits = EXITS_BY_TF[tf]
    D = load_tf(tf, exits)
    S = pd.read_parquet(os.path.join(OUT, f"models_scores_{tf}.parquet"))
    assert (S.t.to_numpy() == D.t.to_numpy()).all() and (S.market.to_numpy() == D.market.to_numpy()).all()
    rows = []
    oos = np.asarray(pd.DatetimeIndex(D.t) >= pd.Timestamp("2013-01-01"))
    for x in exits:
        rows += report(D, oos, x, dict(cfg=cfg_name(tf, x, "ALL", "-", "-"), tf=tf, exit=x, model="ALL",
                                       target="-", variant="-"))
    for c in S.columns:
        if not c.startswith("k|"):
            continue
        name = c[2:]
        _, x, model, target, variant = name.split("|")
        rows += report(D, S[c].to_numpy(bool), x, dict(cfg=name, tf=tf, exit=x, model=model, target=target,
                                                        variant=variant))
    _merge_csv(os.path.join(OUT, "models_results.csv"), pd.DataFrame(rows), ["cfg"])
    print(f"rereport tf {tf}: {len(rows):,} rows", flush=True)


# ------------------------------------------------------------------------------------------------ checks
def trunc_check(tf=60, cut="2019-07-01", models=("M0", "M1", "M2", "M3"), exit=None):
    """Real-data truncation test of the decisions: drop every row from `cut` on and scramble the labels of the
    2019 test rows; the scores and takes of every row before the cut (folds 2013..2019) must not change."""
    exit = EXITS_BY_TF[tf][1] if exit is None else exit
    D = load_tf(tf, (exit,))
    folds = wf.make_folds(test_years=range(2013, 2020), h1_2025=False)
    cutt = pd.Timestamp(cut)
    D2 = D[pd.DatetimeIndex(D.t) < cutt].copy()
    rng = np.random.default_rng(0)
    m19 = pd.DatetimeIndex(D2.t) >= pd.Timestamp("2019-01-01")
    for c in (f"R_{exit}", f"pnl_{exit}"):
        v = D2.loc[m19, c].to_numpy()
        D2.loc[m19, c] = rng.permutation(v)
    bad = {}
    for model in models:
        for target in (("cls",) if model == "M0" else ("cls", "reg")):
            s1, k1, _ = walk(D, tf, exit, model, target, folds=folds, verbose=False)
            s2, k2, _ = walk(D2, tf, exit, model, target, folds=folds, verbose=False)
            n = len(D2)
            a, b = s1[:n], s2
            ok = np.isfinite(a)
            mis = int((~np.isclose(a[ok], b[ok], rtol=1e-6, atol=1e-9)).sum() + (k1[:n] != k2).sum() +
                      (np.isfinite(a) != np.isfinite(b)).sum())
            bad[f"{model}/{target}"] = (mis, int(ok.sum()))
            print(f"  trunc {model}/{target}: {mis} mismatches over {int(ok.sum()):,} scored rows before {cut}",
                  flush=True)
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "trunc-check", "finalize", "rereport"])
    ap.add_argument("--tf", type=int, default=60)
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--targets", default=",".join(TARGETS))
    ap.add_argument("--exits", default=None)
    ap.add_argument("--rolling", type=int, default=None)
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    if a.cmd == "run":
        run(a.tf, a.models.split(","), a.targets.split(","), a.exits.split(",") if a.exits else None, a.rolling,
            log=not a.no_log)
    elif a.cmd == "trunc-check":
        trunc_check(a.tf)
    elif a.cmd == "rereport":
        rereport(a.tf)
    else:
        import models_final                                                  # noqa: PLC0415
        models_final.main()
