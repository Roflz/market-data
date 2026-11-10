"""
v3/signal_lab/zoo.py - SIGNAL ZOO: the calibrated signal lab (lab.py v1.1) run on every metric the user trades with
plus the obvious candidates, ES/NQ/YM x 5/15/60-min, direction AND size targets, one Benjamini-Yekutieli batch.

Every metric is a FUNCTION of the bars (value known at the bar's close), so each one is truncation-tested for
look-ahead (lab.lookahead_check, on ES 60-min bars, the most recent >= 20,000 bars when slow).

CONTROLS. The lab measures each metric against matched bars (15-min slot, weekday, volatility decile, EMA 8/20/50
trend state, last-bar sign, year). A metric that IS one of those controls would be measured as zero, so:
  base   = all six controls                      (most metrics)
  noctx  = slot, weekday, year only              (EMA stack state, 5/15/60 trend agreement, realized volatility)
  cal    = volatility, trend, last-bar sign, year (time-of-day blocks and weekdays)
The year control stays everywhere: it removes plain drift ('NQ went up in 2023').

USAGE (from research/confidence with the standard PYTHONPATH)
  python3 v3/signal_lab/zoo.py run 60,15 [ES,NQ,YM] [--no-la]   # results -> out/zoo_parts/res_<tf>.pkl
  python3 v3/signal_lab/zoo.py run 5                             # 5-min: run under the shared heavy flock
  python3 v3/signal_lab/zoo.py combine [nolog]                   # one batch: BY q-values, halves, cards, ranking
"""
import json
import os
import pickle
import sys
import time
from collections import OrderedDict

import numpy as np
import pandas as pd

import harness as H
import lab as L
import signals as sg
import pullbacks as pb

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
PARTS = os.path.join(OUT, "zoo_parts")
ZOO = os.path.join(OUT, "zoo")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))          # market_data/
DATA = os.path.join(HERE, "..", "data")
FE = {"base": L.FE_DEFAULT, "noctx": ("slot", "dow", "year"), "cal": ("vol", "trend", "prev", "year")}
FE_TEXT = {"base": "controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year",
           "noctx": "controls: 15-min slot, weekday, year (trend state / volatility NOT controlled: they are the metric)",
           "cal": "controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)"}
TICK = {"ES": 0.25, "NQ": 0.25, "YM": 1.0}

# ------------------------------------------------------------------------------------------------ cache
_C = OrderedDict()


def _cached(tag, b, f):
    k = (tag, len(b), b.index[0], b.index[-1], float(b.C.iloc[-1]), float(b.C.iloc[0]))
    if k in _C:
        _C.move_to_end(k)
        return _C[k]
    v = f(b)
    _C[k] = v
    while len(_C) > 16:
        _C.popitem(last=False)
    return v


def _tick(b):
    # ES / NQ quote in 0.25, YM in 1.0 (YM > 10,000 and never fractional)
    return 1.0 if float(b.C.iloc[-1]) > 10000 and (b.C.iloc[-200:] % 1 == 0).all() else 0.25


def ctx(b):
    return _cached("ctx", b, lambda x: sg.context(x, tick=_tick(x)))


def pats(b):
    return _cached("pats", b, lambda x: sg.patterns(x, ctx(x), tick=_tick(x)))


def r20(b):
    def f(x):
        rng = (x.H - x.L)
        r = rng.groupby(x.run.to_numpy()).transform(lambda s: s.rolling(20, min_periods=20).mean())
        return r.clip(lower=2 * _tick(x))
    return _cached("r20", b, f)


def lag(s, b, k=1):
    return s.shift(k).where(b.run.eq(b.run.shift(k)))


def _sided(up, dn, valid):
    v = np.where(up & ~dn, 1.0, np.where(dn & ~up, -1.0, 0.0))
    return pd.Series(v, index=valid.index).where(valid)


def _close_min(b):
    tf = int(round((b.index[1:] - b.index[:-1]).to_series().dt.total_seconds().median() / 60)) if len(b) > 2 else 5
    tf = min((5, 15, 60), key=lambda t: abs(t - tf))
    return (b.index.hour * 60 + b.index.minute + tf).to_numpy() % 1440, tf


# ------------------------------------------------------------------------------------------------ EMA
def dist_ema(n):
    return lambda b: (b.C - b[f"ema{n}"]) / r20(b)


def slope_ema(n, k=5):
    """k-bar change of the EMA in R20. (A 1-bar EMA slope is EXACTLY proportional to the close's distance from the
    EMA: ema_t - ema_t-1 = a/(1-a) x (C_t - ema_t), so it would only duplicate dist_ema<n>.)"""
    return lambda b: (b[f"ema{n}"] - lag(b[f"ema{n}"], b, k)) / r20(b)


def x_ema(a, c):
    def f(b):
        d = np.sign(b[f"ema{a}"] - b[f"ema{c}"])
        d1 = lag(d, b)
        valid = d.notna() & d1.notna()
        return _sided((d > 0) & (d1 <= 0), (d < 0) & (d1 >= 0), valid)
    return f


def x_close_ema20(b):
    d = np.sign(b.C - b.ema20)
    d1 = lag(d, b)
    return _sided((d > 0) & (d1 <= 0), (d < 0) & (d1 >= 0), d.notna() & d1.notna())


def ema_stack(b):
    return b.trend.astype(float).where(b.ema50.notna())


# ------------------------------------------------------------------------------------------------ momentum
def mom_level(b):
    return b.mom14 - 100.0


def mom_slope(b):
    return (b.mom14 - lag(b.mom14, b))


def mom_turn(b):
    s = np.sign(b.mom14 - lag(b.mom14, b))
    s1 = lag(s, b)
    return _sided((s > 0) & (s1 < 0), (s < 0) & (s1 > 0), s.notna() & s1.notna())


def mom_x100(b):
    d = np.sign(b.mom14 - 100)
    d1 = lag(d, b)
    return _sided((d > 0) & (d1 <= 0), (d < 0) & (d1 >= 0), d.notna() & d1.notna())


def mom_div(b):
    """price at a 20-bar closing high while Momentum(14) is below its 20-bar high -> bearish (-1); mirror bullish."""
    g = b.run.to_numpy()
    cmax = b.C.groupby(g).transform(lambda s: s.rolling(20, min_periods=20).max())
    cmin = b.C.groupby(g).transform(lambda s: s.rolling(20, min_periods=20).min())
    mprev_max = b.mom14.groupby(g).transform(lambda s: s.shift(1).rolling(19, min_periods=19).max())
    mprev_min = b.mom14.groupby(g).transform(lambda s: s.shift(1).rolling(19, min_periods=19).min())
    valid = cmax.notna() & mprev_max.notna() & b.mom14.notna()
    return _sided((b.C <= cmin) & (b.mom14 > mprev_min), (b.C >= cmax) & (b.mom14 < mprev_max), valid)


# ------------------------------------------------------------------------------------------------ swings (k = 5)
def swings(b, k=5):
    def f(x):
        lo, hi = sg.pivots(x, k)
        n = len(x)
        g = x.run.to_numpy()
        out = {}
        for nm, piv, px in (("sl", lo, x.L.to_numpy()), ("sh", hi, x.H.to_numpy())):
            p = np.flatnonzero(piv)
            last = pd.Series(np.nan, index=x.index)
            last.iloc[p + k] = px[p]
            prevv = pd.Series(np.nan, index=x.index)
            vals = pd.Series(px[p], index=p + k)
            prevv.iloc[p + k] = vals.groupby(g[p + k]).shift(1).to_numpy()
            out[nm] = last.groupby(g).ffill()
            out[nm + "_prev"] = prevv.groupby(g).ffill()
        return pd.DataFrame(out, index=x.index)
    return _cached(f"sw{k}", b, f)


def swing_struct(b):
    s = swings(b)
    hh, hl = s.sh > s.sh_prev, s.sl > s.sl_prev
    lh, ll = s.sh < s.sh_prev, s.sl < s.sl_prev
    valid = s[["sh", "sh_prev", "sl", "sl_prev"]].notna().all(axis=1)
    return pd.Series(np.where(hh & hl, 1.0, np.where(lh & ll, -1.0, 0.0)), index=b.index).where(valid)


def dist_swing_hi(b):
    return (swings(b).sh - b.C) / r20(b)


def dist_swing_lo(b):
    return (b.C - swings(b).sl) / r20(b)


def swing_break(b):
    s = swings(b)
    up = b.C > s.sh
    dn = b.C < s.sl
    up1, dn1 = lag(up.astype(float), b), lag(dn.astype(float), b)
    valid = s.sh.notna() & s.sl.notna() & up1.notna()
    return _sided(up & (up1 == 0), dn & (dn1 == 0), valid)


# ------------------------------------------------------------------------------------------------ session high/low
def sess_hl(b):
    def f(x):
        g = x.session.to_numpy()
        hi = x.H.groupby(g).cummax()
        lo = x.L.groupby(g).cummin()
        pos = x.groupby(g).cumcount()
        return pd.DataFrame(dict(hi=hi, lo=lo, phi=hi.groupby(g).shift(1), plo=lo.groupby(g).shift(1), pos=pos),
                            index=x.index)
    return _cached("sesshl", b, f)


def dist_sess_hi(b):
    return (sess_hl(b).hi - b.C) / r20(b)


def dist_sess_lo(b):
    return (b.C - sess_hl(b).lo) / r20(b)


def sess_range_pos(b):
    s = sess_hl(b)
    return ((b.C - s.lo) / (s.hi - s.lo)).where(s.hi > s.lo)


def new_sess_extreme(b):
    s = sess_hl(b)
    _, tf = _close_min(b)
    late = s.pos >= max(60 // tf, 1)                                    # at least 1 hour into the session
    return _sided((b.H > s.phi) & late, (b.L < s.plo) & late, s.phi.notna())


# ------------------------------------------------------------------------------------------------ VWAP
def above_vwap(b):
    return (b.C > b.vwap).astype(float).where(b.vwap.notna())


def dist_vwap(b):
    return (b.C - b.vwap) / r20(b)


def x_vwap(b):
    d = np.sign(b.C - b.vwap)
    d1 = d.shift(1).where(b.session.eq(b.session.shift(1)))
    return _sided((d > 0) & (d1 <= 0), (d < 0) & (d1 >= 0), d.notna() & d1.notna())


# ------------------------------------------------------------------------------------------------ candles
DIRECTIONAL = [p for p, (k, _) in sg.PATTERN_RULES.items() if k == "dir"]
NEUTRAL = [p for p, (k, _) in sg.PATTERN_RULES.items() if k == "neutral"]
FAMILIES = {"reversal": ["hammer", "inverted_hammer", "hanging_man", "shooting_star", "dragonfly_doji",
                         "gravestone_doji", "engulfing", "harami", "piercing", "dark_cloud", "morning_evening_star",
                         "three_inside", "tweezer", "pin_bar"],
            "continuation": ["three_soldiers_crows", "marubozu", "tall_trend_bar"],
            "breakout": ["inside_bar_breakout", "nr7_breakout", "outside_bar"],
            "closeloc": ["clv_extreme", "clv5_extreme", "bar_80_20"]}


def _pat_valid(b):
    return r20(b).notna()


def pat(name, neutral=False):
    def f(b):
        v = pats(b)[name].astype(float)
        return v.where(_pat_valid(b))
    return f


def fam(name, side=0):
    def f(b):
        P = pats(b)
        s = np.sign(P[FAMILIES[name]].sum(axis=1)).astype(float)
        if side > 0:
            s = s.clip(lower=0)
        elif side < 0:
            s = s.clip(upper=0)
        return s.where(_pat_valid(b))
    return f


def compression(b):
    P = pats(b)
    return (P[NEUTRAL].sum(axis=1) > 0).astype(float).where(_pat_valid(b))


# ------------------------------------------------------------------------------------------------ pullbacks
def pullbacks(b):
    def f(x):
        _, tf = _close_min(x)
        sym = "YM" if _tick(x) == 1.0 else ("NQ" if float(x.C.iloc[-1]) > 9000 else "ES")
        return pb.detect(x, ctx(x), k_leg=5, sym=sym, tf=tf, pats=pats(x))
    return _cached("pb", b, f)


def pb_event(sel=None):
    def f(b):
        d = pullbacks(b)
        v = np.zeros(len(b))
        if len(d):
            dd = d if sel is None else d[sel(d)]
            for i, s in zip(dd.i_event.to_numpy(), dd.direction.to_numpy()):
                v[i] = s if v[i] in (0, s) else 0.0           # opposite events on one bar cancel
        return pd.Series(v, index=b.index).where(r20(b).notna())
    return f


# ------------------------------------------------------------------------------------------------ volume / range / vol
def vol_rel_slot(b):
    slot = b.index.hour * 60 + b.index.minute
    avg = b.V.groupby(slot).transform(lambda s: s.shift(1).rolling(20, min_periods=10).mean())
    return (b.V / avg).where(avg > 0)


def vol_spike_follow(b):
    vr = vol_rel_slot(b)
    side = np.sign(b.C - b.O)
    return pd.Series(np.where(vr > 2.0, side, 0.0), index=b.index).where(vr.notna())


def range_rel(b):
    return ((b.H - b.L) / lag(r20(b), b))


def big_bar_follow(b):
    rr = range_rel(b)
    return pd.Series(np.where(rr > 2.0, np.sign(b.C - b.O), 0.0), index=b.index).where(rr.notna())


def rvol_ratio(b):
    ret = np.log(b.C / lag(b.C, b))
    g = b.run.to_numpy()
    s20 = ret.groupby(g).transform(lambda s: s.rolling(20, min_periods=20).std())
    s200 = ret.groupby(g).transform(lambda s: s.rolling(200, min_periods=200).std())
    return (s20 / s200).where(s200 > 0)


# ------------------------------------------------------------------------------------------------ daily
def daily(b):
    def f(x):
        g = x.session.to_numpy()
        cm, tf = _close_min(x)
        agg = pd.DataFrame(dict(o=x.O, h=x.H, l=x.L, c=x.C, run=x.run)).groupby(g).agg(
            o=("o", "first"), h=("h", "max"), l=("l", "min"), c=("c", "last"), run0=("run", "first"),
            run1=("run", "last"))
        rng = agg.h - agg.l
        agg["adr20"] = rng.shift(1).rolling(20, min_periods=15).mean()
        same = agg.run0.eq(agg.run1.shift(1))
        agg["pc"] = agg.c.shift(1).where(same)
        agg["gap"] = (agg.o - agg.pc) / agg.adr20
        agg["pret"] = ((agg.c.shift(1) - agg.o.shift(1)) / agg.adr20).where(same)
        agg["prng"] = rng.shift(1) / rng.shift(2).rolling(20, min_periods=15).mean()
        # price at the first bar close at / after 09:30 (09:30 on 5/15-min bars, 10:00 on 60-min bars)
        at = (cm >= 570) & (cm < 1080)
        first = pd.Series(np.where(at, x.C.to_numpy(), np.nan), index=x.index).groupby(g).transform("first")
        firstpos = pd.Series(np.where(at, np.arange(len(x)), np.nan), index=x.index).groupby(g).transform("min")
        out = pd.DataFrame(index=x.index)
        for c in ("gap", "pret", "prng", "pc", "adr20"):
            out[c] = agg[c].reindex(g).to_numpy()
        on = (first - out.pc) / out.adr20
        out["onight"] = on.where(np.arange(len(x)) >= firstpos.to_numpy())
        return out
    return _cached("daily", b, f)


def gap_reopen(b):
    return daily(b).gap


def overnight_move(b):
    return daily(b).onight


def prior_sess_ret(b):
    return daily(b).pret


def prior_day_range(b):
    return daily(b).prng


# ------------------------------------------------------------------------------------------------ calendar
TOD_BLOCKS = {"asia_18_02": lambda m: (m > 1080) | (m <= 120), "europe_02_08": lambda m: (m > 120) & (m <= 480),
              "uspre_08_0930": lambda m: (m > 480) & (m <= 570), "open_0930_1030": lambda m: (m > 570) & (m <= 630),
              "midday_1030_15": lambda m: (m > 630) & (m <= 900), "close_15_1645": lambda m: (m > 900) & (m <= 1020)}


def tod(block):
    def f(b):
        cm, _ = _close_min(b)
        return pd.Series(TOD_BLOCKS[block](cm).astype(float), index=b.index)
    return f


def dow(d):
    return lambda b: pd.Series((pd.DatetimeIndex(b.session).day_of_week == d).astype(float), index=b.index)


_CAL = {}


def _calendar():
    if not _CAL:
        cal = pd.DatetimeIndex(sorted(H.calendar(("ES", "NQ", "YM")).normalize().unique()))
        s = pd.Series(cal, index=cal)
        ym = cal.year * 100 + cal.month
        rank_fwd = s.groupby(ym).cumcount().to_numpy()
        rank_bwd = s[::-1].groupby(ym[::-1]).cumcount().to_numpy()[::-1]
        _CAL["tom"] = set(cal[(rank_fwd < 3) | (rank_bwd == 0)])
        _CAL["fomc"] = set(pd.to_datetime(pd.read_csv(os.path.join(ROOT, "data", "fomc_dates.csv"))
                                          .query("scheduled").date).dt.normalize())
        _CAL["cpi"] = set(pd.to_datetime(pd.read_csv(os.path.join(ROOT, "data", "cpi_dates.csv")).date).dt.normalize())
        # NFP (BLS employment situation): third Friday after the week (Sun-Sat) that contains the 12th; if that day is
        # not a trading day, the trading day before it (approximation: ignores rare shutdown delays, e.g. Oct 2013)
        nfp = set()
        cs = set(cal)
        for y in range(2009, 2026):
            for mth in range(1, 13):
                d12 = pd.Timestamp(y, mth, 12)
                sat = d12 + pd.Timedelta(days=(5 - d12.weekday()) % 7)
                rel = sat + pd.Timedelta(days=20)
                if rel.month == 1 and rel.day <= 3:                 # January: BLS moves Jan 1-3 to the next Friday
                    rel += pd.Timedelta(days=7)                       # (2014/15/16/20/21/25 checked)
                k = 0
                while rel not in cs and k < 4 and rel <= cal.max():
                    rel -= pd.Timedelta(days=1)
                    k += 1
                if rel in cs:
                    nfp.add(rel)
        _CAL["nfp"] = nfp
    return _CAL


def cal_day(kind):
    def f(b):
        days = _calendar()[kind]
        return pd.Series(pd.DatetimeIndex(b.session).normalize().isin(list(days)).astype(float), index=b.index)
    return f


# ------------------------------------------------------------------------------------------------ 5/15/60 agreement
_TR = {}


def _trend_tf(sym, tf):
    if (sym, tf) not in _TR:
        t = pd.read_parquet(os.path.join(DATA, f"bars_{sym}_{tf}.parquet"), columns=["trend", "ema50"])
        tr = t.trend.where(t.ema50.notna(), 0).to_numpy(np.float64)
        close = (t.index + pd.Timedelta(minutes=tf)).to_numpy()
        _TR[(sym, tf)] = (close, tr)
    return _TR[(sym, tf)]


def tf_agree(sym):
    def f(b):
        cm_t = (b.index + pd.Timedelta(minutes=_close_min(b)[1])).to_numpy()
        tot = np.zeros(len(b))
        for tf in (5, 15, 60):
            close, tr = _trend_tf(sym, tf)
            j = np.searchsorted(close, cm_t, side="right") - 1
            tot += np.where(j >= 0, tr[np.maximum(j, 0)], np.nan)
        lvl = np.select([tot <= -3, tot < 0, tot == 0, tot < 3], [-2.0, -1.0, 0.0, 1.0], 2.0)
        return pd.Series(np.where(np.isfinite(tot), lvl, np.nan), index=b.index).where(b.ema50.notna())
    return f


# ------------------------------------------------------------------------------------------------ registry
def registry(sym):
    """name -> dict(fn, kind, desc, group, fe)."""
    R = OrderedDict()

    def add(name, fn, kind, group, desc, fe="base"):
        R[name] = dict(fn=fn, kind=kind, group=group, fe=fe, desc=f"{desc} [{FE_TEXT[fe]}]")

    add("ema_stack", ema_stack, "state", "EMA", "EMA 8/20/50 stack: +1 = 8>20>50 (up), -1 = 8<20<50 (down), 0 mixed; "
        "up stack vs down stack", fe="noctx")
    for n in (8, 20, 50):
        add(f"dist_ema{n}", dist_ema(n), "continuous", "EMA", f"(close - EMA{n}) in R20 (average bars)")
    for n in (8, 20, 50):
        add(f"slope_ema{n}", slope_ema(n), "continuous", "EMA", f"5-bar change of EMA{n} in R20")
    add("x_ema8_20", x_ema(8, 20), "sided", "EMA", "EMA8 crosses EMA20: up cross long, down cross short")
    add("x_ema20_50", x_ema(20, 50), "sided", "EMA", "EMA20 crosses EMA50: up cross long, down cross short")
    add("x_close_ema20", x_close_ema20, "sided", "EMA", "close crosses EMA20: above long, below short")
    add("mom14_level", mom_level, "continuous", "Momentum", "Momentum(14) - 100 (% change over 14 bars)")
    add("mom14_slope", mom_slope, "continuous", "Momentum", "1-bar change of Momentum(14)")
    add("mom14_turn", mom_turn, "sided", "Momentum", "Momentum(14) turns up (long) / down (short)")
    add("mom14_x100", mom_x100, "sided", "Momentum", "Momentum(14) crosses 100: up long, down short")
    add("mom14_div", mom_div, "sided", "Momentum", "divergence: close at a 20-bar high while Momentum(14) below its "
        "prior 19-bar high -> short; mirror -> long")
    add("swing_struct", swing_struct, "state", "Swing", "swing structure (5-bar fractals): higher high AND higher low "
        "(+1) vs lower high AND lower low (-1)")
    add("dist_swing_hi", dist_swing_hi, "continuous", "Swing", "(last swing high - close) in R20")
    add("dist_swing_lo", dist_swing_lo, "continuous", "Swing", "(close - last swing low) in R20")
    add("swing_break", swing_break, "sided", "Swing", "first close above the last swing high (long) / below the last "
        "swing low (short)")
    add("dist_sess_hi", dist_sess_hi, "continuous", "Session H/L", "(session high so far - close) in R20")
    add("dist_sess_lo", dist_sess_lo, "continuous", "Session H/L", "(close - session low so far) in R20")
    add("sess_range_pos", sess_range_pos, "continuous", "Session H/L", "close position in the session's range so far "
        "(0 = at low, 1 = at high)")
    add("new_sess_extreme", new_sess_extreme, "sided", "Session H/L", "bar makes a new session high (long) / low "
        "(short), at least 1 hour into the session")
    add("above_vwap", above_vwap, "state", "VWAP", "close above session VWAP (1) vs below (0)")
    add("dist_vwap", dist_vwap, "continuous", "VWAP", "(close - VWAP) in R20")
    add("x_vwap", x_vwap, "sided", "VWAP", "close crosses VWAP: above long, below short")
    for p in DIRECTIONAL:
        add(f"pat_{p}", pat(p), "sided", "Candle", f"candle pattern {p} in its textbook direction: "
            f"{sg.PATTERN_RULES[p][1]}")
    for p in NEUTRAL:
        add(f"pat_{p}", pat(p), "event", "Candle", f"candle pattern {p} (no direction): {sg.PATTERN_RULES[p][1]}")
    for fm in FAMILIES:
        add(f"fam_{fm}", fam(fm), "sided", "Candle family", f"any {fm} pattern, textbook direction (both sides)")
        add(f"fam_{fm}_long", fam(fm, 1), "sided", "Candle family", f"bullish {fm} patterns only (long side)")
        add(f"fam_{fm}_short", fam(fm, -1), "sided", "Candle family", f"bearish {fm} patterns only (short side)")
    add("fam_compression", compression, "event", "Candle family", "any of doji / spinning top / inside bar / NR7")
    add("pb_all", pb_event(), "sided", "Pullback", "pullback detector (pullbacks.detect, 5-bar legs): every setup "
        "in its trend direction at the event bar")
    add("pb_shallow", pb_event(lambda d: d.depth < 0.382), "sided", "Pullback", "pullback setups with depth < 38.2%")
    add("pb_deep", pb_event(lambda d: d.depth >= 0.618), "sided", "Pullback", "pullback setups with depth >= 61.8%")
    add("pb_hidden_div", pb_event(lambda d: d.divergence.astype(bool)), "sided", "Pullback",
        "pullback setups with hidden Momentum(14) divergence (higher low in price, lower momentum)")
    add("vol_rel_slot", vol_rel_slot, "continuous", "Volume/range", "volume / average volume of the same time slot "
        "over the previous 20 sessions")
    add("vol_spike_follow", vol_spike_follow, "sided", "Volume/range", "volume > 2x slot average, traded in the bar's "
        "colour")
    add("range_rel", range_rel, "continuous", "Volume/range", "bar range / average range of the previous 20 bars")
    add("big_bar_follow", big_bar_follow, "sided", "Volume/range", "bar range > 2x previous 20-bar average, traded in "
        "the bar's colour")
    add("rvol_ratio", rvol_ratio, "continuous", "Volatility", "realized volatility of the last 20 bars / last 200 "
        "bars", fe="noctx")
    add("gap_reopen", gap_reopen, "continuous", "Daily", "18:00 reopen gap vs prior session close, in average "
        "daily ranges (ADR20)")
    add("overnight_move", overnight_move, "continuous", "Daily", "move from prior session close to the US cash open "
        "(09:30; 10:00 on 60-min bars), in ADR20; known from that bar on")
    add("prior_sess_ret", prior_sess_ret, "continuous", "Daily", "prior session's open-to-close return in ADR20")
    add("prior_day_range", prior_day_range, "continuous", "Daily", "prior session's range / its 20-session average")
    for blk in TOD_BLOCKS:
        add(f"tod_{blk}", tod(blk), "event", "Time of day", f"bar closes in the {blk} block (ET) vs all other bars",
            fe="cal")
    for d, nm in enumerate(("mon", "tue", "wed", "thu", "fri")):
        add(f"dow_{nm}", dow(d), "event", "Day of week", f"session weekday = {nm} vs other days", fe="cal")
    add("turn_of_month", cal_day("tom"), "event", "Calendar", "last trading day of a month and first 3 of the next")
    add("nfp_day", cal_day("nfp"), "event", "Calendar", "US jobs report (NFP) session (computed BLS schedule)")
    add("cpi_day", cal_day("cpi"), "event", "Calendar", "CPI release session (data/cpi_dates.csv)")
    add("fomc_day", cal_day("fomc"), "event", "Calendar", "scheduled FOMC statement session (data/fomc_dates.csv)")
    add("tf_agree", tf_agree(sym), "state", "Trend agreement", "5/15/60-min EMA stack agreement: +2 = all three up, "
        "-2 = all three down (levels -2..2)", fe="noctx")
    return R


# ------------------------------------------------------------------------------------------------ run / combine
def run(tfs, syms, do_la=True, only=None):
    os.makedirs(PARTS, exist_ok=True)
    for tf in tfs:
        results = []
        t_tf = time.time()
        for sym in syms:
            reg = registry(sym)
            if only:
                reg = OrderedDict((k, v) for k, v in reg.items() if k in only)
            bars = H.bars(sym, tf)
            for fe in ("base", "noctx", "cal"):
                names = [k for k, v in reg.items() if v["fe"] == fe]
                if not names:
                    continue
                t0 = time.time()
                P = L.Panel(bars, sym, tf, fe=FE[fe])
                print(f"[zoo] {sym} {tf}m {fe}: panel {P.n} bars {P.T} sessions in {time.time() - t0:.1f}s",
                      flush=True)
                for nm in names:
                    s = reg[nm]
                    t1 = time.time()
                    try:
                        out = s["fn"](P.bars)
                        x, side = out if isinstance(out, tuple) else (out, None)
                        r = L.evaluate(P, np.asarray(x, dtype=float), s["kind"], side=side, name=nm, desc=s["desc"],
                                       n_power=20, check_lookahead=False)
                    except Exception as err:                       # noqa: BLE001
                        print(f"[zoo]   {nm} {sym} {tf}: FAILED {type(err).__name__}: {err}", flush=True)
                        continue
                    r.pop("A_dir", None)
                    r["group"], r["fe"] = s["group"], fe
                    results.append(r)
                    print(f"[zoo]   {nm:24s} {sym} {tf:>2}m {fe:5s} n={r['n_valid']:7d} top={r['n_top']:6d} "
                          f"p_dir={r['p_dir']:.3g} p_size={r['p_size']:.3g} {time.time() - t1:.1f}s", flush=True)
                del P
            _C.clear()
            H._CACHE.pop(("B", sym, tf), None)
        fn_ = f"res_{tf}.pkl" if not only else f"res_{tf}_extra_{'_'.join(sorted(only))[:60]}.pkl"
        with open(os.path.join(PARTS, fn_), "wb") as f:
            pickle.dump(results, f, protocol=5)
        print(f"[zoo] tf {tf}: {len(results)} results in {time.time() - t_tf:.0f}s", flush=True)
    if do_la:
        lookahead(only)


def lookahead(only=None):
    """truncation test of every metric's code on ES 60-min bars (the most recent >= 20,000 bars when slow)."""
    reg = registry("ES")
    if only:
        reg = OrderedDict((k, v) for k, v in reg.items() if k in only)
    bars = H.bars("ES", 60)
    res = {}
    for nm, s in reg.items():
        t0 = time.time()
        _C.clear()
        la = L.lookahead_check(s["fn"], bars, budget_s=8.0)
        la = {k: (v if not isinstance(v, (np.generic,)) else v.item()) for k, v in la.items()}
        res[nm] = la
        print(f"[zoo] look-ahead {nm:24s} {la['status']:7s} cuts={la['n_cuts']} rows={la['n_rows']} "
              f"bad={la['n_bad']} {time.time() - t0:.1f}s", flush=True)
    path = os.path.join(PARTS, "lookahead.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(res)
    with open(path, "w") as f:
        json.dump(old, f, indent=1, default=str)


def combine(log=True):
    results = []
    import glob
    for tf in (5, 15, 60):
        p = os.path.join(PARTS, f"res_{tf}.pkl")
        if os.path.exists(p):
            results += pickle.load(open(p, "rb"))
    for p in sorted(glob.glob(os.path.join(PARTS, "res_*_extra_*.pkl"))):    # re-runs of single metrics replace
        extra = pickle.load(open(p, "rb"))
        keys = {(r["name"], r["sym"], r["tf"]) for r in extra}
        results = [r for r in results if (r["name"], r["sym"], r["tf"]) not in keys] + extra
        print(f"[zoo] {os.path.basename(p)}: replaced/added {len(extra)} results")
    results.sort(key=lambda r: (r["name"], r["sym"], r["tf"]))
    la = json.load(open(os.path.join(PARTS, "lookahead.json")))
    for r in results:
        r["lookahead"] = la.get(r["name"])
    batch = L.batch_table(results)
    # explicit split-half check at the best direction hold: chronological halves (2010-17 / 2018-25H1) when the metric
    # has data in both, else interleaved calendar quarters (YM: 2018+ only). both_halves = same sign as the full-sample
    # effect AND one-sided p < 0.05 in EACH half.
    zh1, zh2, eh1, eh2, spl = [], [], [], [], []
    for r in results:
        t = r["table"]
        bd = r["best_dir"]
        if np.isfinite(t.at[bd, "z_2010-17"]) and np.isfinite(t.at[bd, "z_2018-25H1"]):
            a, b_, sp = "2010-17", "2018-25H1", "chronological"
        else:
            a, b_, sp = "Qodd", "Qeven", "odd/even quarters"
        zh1.append(t.at[bd, f"z_{a}"]); zh2.append(t.at[bd, f"z_{b_}"])
        eh1.append(t.at[bd, f"effect_{a}"] if f"effect_{a}" in t else np.nan)
        eh2.append(t.at[bd, f"effect_{b_}"] if f"effect_{b_}" in t else np.nan)
        spl.append(sp)
    batch["half_split"], batch["z_half1"], batch["z_half2"] = spl, zh1, zh2
    batch["eff_half1"], batch["eff_half2"] = eh1, eh2
    sgn = np.sign(batch.dir_effect)
    batch["both_halves"] = ((np.sign(batch.z_half1) == sgn) & (np.sign(batch.z_half2) == sgn)
                            & (batch.z_half1.abs() > 1.645) & (batch.z_half2.abs() > 1.645))
    batch["usd_per_r20"] = [r.get("usd_per_r20_recent", np.nan) for r in results]
    meta = {r["name"]: (r["group"], r["fe"]) for r in results}
    batch.insert(1, "group", batch.metric.map(lambda m: meta[m][0]))
    batch.insert(2, "controls", batch.metric.map(lambda m: meta[m][1]))
    os.makedirs(ZOO, exist_ok=True)
    L.write_outputs(batch, results, ZOO)
    batch.to_csv(os.path.join(ZOO, "zoo_batch.csv"), index=False)
    rk = rank(batch)
    rk.to_csv(os.path.join(OUT, "zoo_ranked.csv"), index=False)
    if log:
        L.log_trials(batch, "zoo")
    print(f"[zoo] combined {len(results)} results, {batch.metric.nunique()} metrics; BY over {2 * len(batch)} p-values")
    return batch, rk


def rank(B):
    rows = []
    for m, g in B.groupby("metric", sort=False):
        sg_ = np.sign(g.dir_effect)
        maj = np.sign(sg_.sum()) or 1.0
        conf_any = g[g.dir_verdict == "CONFIRMED"]
        conf = conf_any[conf_any.both_halves]
        csign = np.sign(conf.dir_effect.sum()) if len(conf) else 0.0
        same_panels = int((sg_ == (csign or maj)).sum())
        mk_same = int(sum((np.sign(gg.dir_effect) == (csign or maj)).mean() > 0.5 for _, gg in g.groupby("market")))
        szc = g[g.size_verdict == "CONFIRMED"]
        lab_ = g.lookahead.iloc[0]
        dir_conf = (len(conf) > 0 and same_panels >= 6 and mk_same >= 2 and lab_ == "passed"
                    and bool((conf.dir_effect.apply(np.sign) == csign).all()))
        if lab_ == "FAILED":
            overall = "INVALID (look-ahead)"
        elif dir_conf:
            tr = (conf.dir_class.str.startswith("REAL & TRADABLE")).any()
            overall = "DIRECTION: confident, beats costs" if tr else "DIRECTION: confident, smaller than costs"
        elif len(conf_any):
            overall = "DIRECTION: confirmed in some panels but not consistent (halves / markets / timeframes)"
        elif len(szc):
            overall = "SIZE ONLY"
        elif (g.dir_class == "CONFIDENTLY NOTHING").sum() >= 1 and (g.dir_verdict == "none").all():
            overall = "NONE (confident 'nothing' in some panels)"
        else:
            overall = "NONE / inconclusive"
        best = (conf if len(conf) else (conf_any if len(conf_any) else g)).sort_values("q_dir").iloc[0]
        rows.append(dict(
            metric=m, group=g.group.iloc[0], kind=g.kind.iloc[0], controls=g.controls.iloc[0], lookahead=lab_,
            overall=overall, n_panels=len(g), dir_confirmed=len(conf_any), dir_confirmed_both_halves=len(conf),
            dir_confirmed_panels=";".join(f"{r.market}{r.tf}" for r in conf_any.itertuples()),
            signs_by_panel=";".join(f"{r.market}{r.tf}{'+' if r.dir_effect > 0 else '-'}" for r in g.itertuples()),
            dir_q05=int((g.q_dir < 0.05).sum()), replicated=int(g.replicated.sum()),
            dir_sign=("+" if (csign or maj) > 0 else "-"), sign_same_panels=same_panels, sign_same_markets=mk_same,
            min_q_dir=g.q_dir.min(), best_panel=f"{best.market}{best.tf}", best_hold=best.best_dir,
            best_dir_effect_r20=best.dir_effect, best_dir_ci=f"[{best.dir_lo:.3f}, {best.dir_hi:.3f}]",
            best_years_same=f"{int(best.dir_years_same)}/{int(best.years_n)}", best_both_halves=bool(best.both_halves),
            best_z_halves=f"{best.z_half1:.2f} / {best.z_half2:.2f} ({best.half_split})",
            best_dir_effect_usd=best.dir_effect * best.usd_per_r20 if np.isfinite(best.usd_per_r20) else np.nan,
            best_edge_usd_2018_25=best.edge_usd_B, best_edge_usd_lo80=best.edge_usd_B_lo80,
            best_cost_usd=best.cost_usd, best_dir_class=best.dir_class,
            n_tradable=int(g.dir_class.str.startswith("REAL & TRADABLE").sum()),
            n_too_small=int(g.dir_class.str.startswith("REAL BUT TOO SMALL").sum()),
            n_nothing=int((g.dir_class == "CONFIDENTLY NOTHING").sum()),
            n_inconclusive=int((g.dir_class == "INCONCLUSIVE").sum()),
            max_ruled_out_usd=g.edge_usd_ci90_max_h1_8.max(),
            size_confirmed=len(szc), size_confirmed_panels=";".join(f"{r.market}{r.tf}" for r in szc.itertuples()),
            min_q_size=g.q_size.min(), size_pct_median=g.size_pct.median(),
            size_pct_range=f"[{g.size_pct.min():.0f}%, {g.size_pct.max():.0f}%]",
            size_best_target=g.sort_values("q_size").best_size.iloc[0]))
    R = pd.DataFrame(rows)
    order = {"DIRECTION: confident, beats costs": 0, "DIRECTION: confident, smaller than costs": 1,
             "DIRECTION: confirmed in some panels but not consistent (halves / markets / timeframes)": 2, "SIZE ONLY": 3,
             "NONE / inconclusive": 4, "NONE (confident 'nothing' in some panels)": 5, "INVALID (look-ahead)": 6}
    R["_o"] = R.overall.map(order)
    R = R.sort_values(["_o", "dir_confirmed", "min_q_dir", "size_confirmed", "min_q_size"],
                      ascending=[True, False, True, False, True]).drop(columns="_o")
    R.insert(0, "rank", np.arange(1, len(R) + 1))
    return R


def dollar_check(names=None, n_boot=500):
    """PLAIN-$ CROSS-CHECK of direction-confirmed metrics (added after the zoo run, see the doji note).
    The lab measures moves in R20 units (move / average bar). At long holds (16 bars, to 16:45) that scaling lets
    quiet bars with a tiny average bar (overnight) dominate, so a metric that fires on quiet bars can look strong in
    R20 units without earning more DOLLARS. Here: every signal bar traded in its side at the lab's best hold, entry =
    next bar's open, exit = close h bars later (or 16:45); $ per micro; excess = minus the mean $ move of all
    NON-signal bars in the same (year x 15-min slot) cell (year only for time-of-day / weekday metrics); session
    bootstrap se. Writes out/zoo/dollar_check.csv and adds dollar_check columns to out/zoo_ranked.csv."""
    B = pd.read_csv(os.path.join(ZOO, "zoo_batch.csv"))
    R = pd.read_csv(os.path.join(OUT, "zoo_ranked.csv"))
    if names is None:
        names = list(B[B.dir_verdict == "CONFIRMED"].metric.unique())
    rows = []
    for (sym, tf), g in B[B.metric.isin(names)].groupby(["market", "tf"]):
        reg = registry(sym)
        bars = H.bars(sym, tf)
        P = L.Panel(bars, sym, tf, fe=("year",), n_boot=10)
        n = P.n
        idx = np.arange(n)
        O, C = bars.O.to_numpy(), bars.C.to_numpy()
        yr = P.year_s[P.sess_code]
        slot = (bars.index.hour * 60 + bars.index.minute).to_numpy() // 15
        for r in g.itertuples():
            if r.kind not in ("event", "sided"):
                continue
            x = np.asarray(reg[r.metric]["fn"](P.bars), dtype=float)
            h = 0 if r.best_dir == "dir_eod" else int(r.best_dir.split("_h")[1])
            j = P.seg_end if h == 0 else np.minimum(idx + h, P.seg_end)
            fwd = (C[j] - O[np.minimum(idx + 1, n - 1)]) * P.usd
            ok = P.ok & np.isfinite(x)
            sig = ok & (x != 0)
            side = np.where(r.kind == "sided", np.sign(np.nan_to_num(x)), 1.0)
            side = side * (np.sign(r.dir_effect) or 1.0) if r.kind == "event" else side
            cell = yr * 1000 + (0 if r.group in ("Time of day", "Day of week") else slot)
            df = pd.DataFrame(dict(f=fwd, cell=cell, s=P.sess_code))
            base = df[ok & ~sig].groupby("cell").f.mean()
            ex = side * (df.f - df.cell.map(base).to_numpy())
            for lab_, sel in (("all", sig), ("2018-25H1", sig & (yr >= 2018))):
                e = pd.DataFrame(dict(ex=ex[sel], s=P.sess_code[sel])).dropna()
                if len(e) < 30:
                    continue
                gg = e.groupby("s").ex.agg(["sum", "count"])
                S, N = gg["sum"].to_numpy(), gg["count"].to_numpy()
                rng = np.random.default_rng(0)
                bs = [S[k].sum() / N[k].sum() for k in (rng.integers(0, len(S), len(S)) for _ in range(n_boot))]
                m, se = S.sum() / N.sum(), float(np.std(bs))
                rows.append(dict(metric=r.metric, market=r.market, tf=tf, hold=r.best_dir, era=lab_, trades=len(e),
                                 lab_dir_verdict=r.dir_verdict, lab_dir_class=r.dir_class,
                                 lab_edge_usd_2018_25=r.edge_usd_B, usd_excess=m, usd_se=se, z=m / se if se else np.nan,
                                 cost_usd=r.cost_usd, usd_lo80=m - 1.2816 * se))
        del P
        _C.clear()
    D = pd.DataFrame(rows)
    D.to_csv(os.path.join(ZOO, "dollar_check.csv"), index=False)
    if len(D):
        rec = D[D.era == "2018-25H1"]
        for m in R.metric:
            q = rec[rec.metric == m]
            if not len(q):
                continue
            conf_panels = set(B[(B.metric == m) & (B.dir_verdict == "CONFIRMED")].apply(lambda t: (t.market, t.tf), axis=1))
            q = q[q.apply(lambda t: (t.market, t.tf) in conf_panels, axis=1)]
            R.loc[R.metric == m, "dollar_check_2018_25"] = "; ".join(
                f"{t.market}{t.tf} {t.hold}: ${t.usd_excess:+.2f} +- {t.usd_se:.2f} (z {t.z:+.1f}, cost ${t.cost_usd:.2f})"
                for t in q.itertuples())
            R.loc[R.metric == m, "dollar_check_beats_cost"] = bool((q.usd_lo80 > q.cost_usd).any())
            R.loc[R.metric == m, "dollar_check_any_z2"] = bool((q.z.abs() > 2).any())
            # final word on direction: the lab's verdict must survive the plain-$ check (same sign, |z| > 2)
            if str(R.loc[R.metric == m, "overall"].iloc[0]).startswith("DIRECTION: confident"):
                sgn = 1.0 if R.loc[R.metric == m, "dir_sign"].iloc[0] == "+" else -1.0
                ok_ = q[(np.sign(q.usd_excess) == sgn) & (q.z.abs() > 2)]
                if not len(ok_):
                    fin = "DIRECTION: R20 units only - NOT confirmed in plain $ (treat as none)"
                elif (ok_.usd_lo80 > ok_.cost_usd).any():
                    fin = "DIRECTION: confirmed in R20 and $, beats costs"
                else:
                    fin = (f"DIRECTION: confirmed in R20 and $, far below costs "
                           f"(${ok_.usd_excess.abs().max():.2f} vs ${ok_.cost_usd.min():.2f})")
                R.loc[R.metric == m, "final_direction_word"] = fin
        R.to_csv(os.path.join(OUT, "zoo_ranked.csv"), index=False)
        mark = "\n## Plain-$ cross-check (zoo.dollar_check)\n"
        for m in D.metric.unique():
            path = os.path.join(ZOO, "cards", f"{m}.md")
            if not os.path.exists(path):
                continue
            txt = open(path).read().split(mark)[0]
            q = D[(D.metric == m)]
            fin = R.loc[R.metric == m, "final_direction_word"]
            lines = [mark, "Each signal bar traded in its side at the lab's best hold, in $ per micro, minus the average $ "
                     "move of non-signal bars in the same year x 15-min slot (session bootstrap se). The lab's R20 "
                     "units can overweight quiet bars at long holds; a direction claim must survive this check.", "",
                     f"FINAL WORD: {fin.iloc[0] if len(fin) and isinstance(fin.iloc[0], str) else 'n/a'}", "",
                     "| market | tf | hold | era | trades | lab verdict | lab $ edge 2018-25 | $ excess | se | z | cost |",
                     "|---|---|---|---|---|---|---|---|---|---|---|"]
            for t in q.itertuples():
                lines.append(f"| {t.market} | {t.tf} | {t.hold} | {t.era} | {t.trades} | {t.lab_dir_class} | "
                             f"{t.lab_edge_usd_2018_25:+.2f} | {t.usd_excess:+.2f} | {t.usd_se:.2f} | {t.z:+.1f} | "
                             f"{t.cost_usd:.2f} |")
            with open(path, "w") as f:
                f.write(txt + "\n".join(lines) + "\n")
    print(D.round(3).to_string())
    return D


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "run":
        tfs = tuple(int(x) for x in a[1].split(","))
        syms = tuple(a[2].split(",")) if len(a) > 2 and not a[2].startswith("-") else ("ES", "NQ", "YM")
        only = None
        for x in a:
            if x.startswith("--only="):
                only = set(x[7:].split(","))
        run(tfs, syms, do_la="--no-la" not in a, only=only)
    elif a and a[0] == "lookahead":
        lookahead()
    elif a and a[0] == "dollarcheck":
        dollar_check()
    elif a and a[0] == "combine":
        combine(log="nolog" not in a)
