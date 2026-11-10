"""
Module 1 of the confidence study (SPEC.md): one feature row per tf-bar, every value known at the CLOSE of its bar.

  build_features(sym, tf, others=("ES","NQ","YM"), cache=True) -> (b, F)
      b = signals.bars(sym, tf) plus the signals.context columns and R20 (the scale unit, see below).
      F = DataFrame on b.index, float32, columns COLUMNS(sym, others) in the order below.
  compute_features(b, ctx, P, tf, b60=None, ctx60=None, xmk=None) -> F
      the same from frames you already have (used by the tests on hand-made bars).
  SIGNED       directional columns (+ = bullish, - = bearish reading).
  MIRROR       column pairs that swap places for shorts: {dist_swhi_k: dist_swlo_k}.
  CLIP         {column: c}: F values are winsorized to [-c, c] (see "Winsorizing" below).
  orient(F, d) the frame seen from a trade of direction d (+1 long / -1 short, scalar or one per row): SIGNED columns
               times d and, for shorts, the MIRROR pairs swapped (a short's dist_swhi_k = -dist_swlo_k: the distance
               to the swing on its target side, as dist_swhi_k is for a long; dist_swlo_k = -dist_swhi_k likewise for
               the stop side), so + means "with the trade". This is the ONE direction convention of the study:
               walkforward.orient(X, d, SIGNED, MIRROR) - walkforward's default, mirror="auto" reads MIRROR from
               here - gives the identical frame (test_features.py checks it, through walkforward._prepare too).
               Do not multiply by d yourself: that gets the swing-distance pair wrong for shorts.
  clear_cache() drops the in-memory bar cache (the 1-minute source is cached by research_lib).

Mirror symmetry - what orient(F of the upside-down chart, -1) equals (prices p -> K - p; the tests check every column
of the full compute_features output, 60-min and other markets included):
  * the same column of F for all columns except the two groups below (SIGNED ones are antisymmetric, the MIRROR
    pair is mapped by the swap, unsigned ones are symmetric; exact up to float rounding);
  * the PARTNER column of F for the one-sided pattern pairs hammer <-> shooting_star, inverted_hammer <->
    hanging_man, dragonfly_doji <-> gravestone_doji, piercing <-> dark_cloud: they are NOT in MIRROR, on purpose -
    each keeps its own column and coefficient ("a bullish hammer, oriented"); the fam_ sums are antisymmetric;
  * no exact relation for mom, mom_slope3, h1_mom: ratios (100 x C / C[t-14]); mom and h1_mom keep their sign.
So "a short sees what a long sees on the upside-down chart" holds for every column except those two groups.

Timing (no look-ahead; checked by test_features.py's perturbation test):
  * bar t starts at b.index[t] and closes at start + tf; a row uses only bars that closed by then.
  * swing pivots (signals.pivots, k bars each side) are used only from the close of bar p+k on.
  * 60-minute values come from the latest 60-min bar of the SAME contract whose (nominal) close start+60 <= t's close.
  * other markets: only their bar with the same start time (it closes at the same moment); missing -> NaN.
Units: prices of different eras differ a lot, so distances are in R20 = mean (H - L) of the 20 bars BEFORE t in the
same contract run (floored at 2 ticks), called "average bars" in the report.
Winsorizing (CLIP): when the 20 bars before t were nearly flat (holiday sessions, limit-locked markets such as the
2020-03-16 open, where R20 sits at its 2-tick floor) R20 is tiny and the R20-unit columns explode (ES dist_swhi_5 down
to -517, NQ -1473), and fibpos_k explodes when the swing leg is only a tick or two long. Such values would dominate a
StandardScaler + logit, so F clips the R20-unit and ratio columns to +-50 (no legitimate 2010-2012 ES/NQ value of a
distance column reaches it; it touches < 0.1% of rows) and fibpos_k to +-10 leg lengths (~0.5% of rows; 1-99% range
is about +-4.5). Clipping is elementwise and symmetric, so it adds no look-ahead and keeps the mirror relations.
b.R20 itself and the helper functions (structure, session_features, ...) return raw values.
Missing values: NaN means "not computable yet" (warm-up after a contract roll, no swing confirmed, no bar in the other
market ...). Pattern and family columns are never NaN (0 = did not fire).

Columns (SIGNED marked +-):
  pat_<name>          +- the 24 directional patterns (signals.patterns: +1/-1/0); 0/1 for doji, spinning_top,
                      inside_bar, nr7.
  fam_<family>        +- sum of the member patterns clipped to [-1, 1] (FAMILIES).
  dist_swhi_k/swlo_k  +- (close - latest confirmed swing high/low) / R20, k = 5, 10 (pivot k bars each side).
  brk_k               +- +1 on the FIRST close above the latest confirmed swing high since it was confirmed, -1 first
                      close below the latest swing low (0 if both or neither).
  struct_k            +- +1 if the last two confirmed swing highs AND the last two lows are rising, -1 if both falling.
  fibpos_k            +- leg = the latest confirmed swing low and swing high, from the earlier to the later pivot;
                      pos = (close - leg start) / (leg end - leg start) (0 = start, 1 = end), times +1 for an up leg
                      (low then high), -1 for a down leg. NaN when both pivots are the SAME bar (an outside bar such
                      as an 8:30 news bar is both): the leg has no known direction. Clipped to +-10.
  atfib_k                1 if the close is within 0.15 R20 of the leg's 0.382 / 0.5 / 0.618 level (the level set is
                         the same for both leg directions, so it is defined for the same-bar case too).
  ema_stack           +- +1 EMA8 > EMA20 > EMA50, -1 mirror, 0 otherwise (NaN before EMA50 is valid).
  ema20_slope         +- (EMA20 - EMA20 10 bars ago) / R20.
  dist_ema8/20/50     +- (close - EMA) / R20.
  above_ema20_share   +- 2 x (share of the last 20 closes above EMA20) - 1.
  mom                 +- mom14 - 100 (mom14 = 100 x close / close 14 bars ago).
  mom_slope3          +- mom14 - mom14 3 bars ago.
  mom_x100            +- +1 if mom14 crosses above 100 on this bar, -1 below, else 0. "Crosses" compares with the
                      side of the last mom14 != 100 before t in the run, so 101 -> 100 -> 101 is no cross while
                      99 -> 100 -> 101 is +1 on the 101 bar (mom14 is exactly 100 on ~2% of bars on the tick grid);
                      leaving 100 when no earlier side is known counts as a cross. NaN while mom14[t-1] is NaN.
  dist_vwap           +- (close - session VWAP from 1-min bars) / R20.
  rng_rel                (H - L) / R20.
  body_frac              |C - O| / (H - L) (0 if the range is 0).
  clv                 +- 2 x (C - L) / (H - L) - 1 (0 if the range is 0).
  vol_rel                volume / mean volume of the prior 20 bars (same run).
  gap_open            +- (open of the session segment's first bar - close of the bar before it) / R20 at that first
                      bar; constant through the segment; NaN if the bar before is another contract.
  day_range_rel          (segment high - low so far) / mean full range of the prior 20 segments.
  day_ret             +- (close - open of the segment's first bar) / R20.
  tod_<bucket>           one-hot of the bar's start time: asia 18-2, europe 2-8, uspre 8-9:30, open 9:30-10:30,
                         midday 10:30-15, close 15-18 (the 16:45-17:00 tail takes no entries anyway).
  dow_<0..4>             session weekday (the Sunday-evening session is Monday = 0).
  h1_ema_stack        +- 60-min ema_stack;  h1_mom +- 60-min mom14 - 100;  h1_struct_5 +- 60-min struct_5.
  x_<SYM>_ret         +- (C - O) / R20 of the other market's same-start bar (its own R20).
  x_<SYM>_ema_stack   +- that bar's ema_stack in the other market.
A "segment" is signals' seg: one Globex session of one contract (a roll at 19:00/20:00 splits a session in two).
"""
import warnings

import numpy as np
import pandas as pd

import exits as ex
import signals as sg

DIRECTIONAL = list(ex.DIRECTIONAL)                                  # 24 textbook-direction patterns
NEUTRAL = [k for k, (kind, _) in sg.PATTERN_RULES.items() if kind == "neutral"]
FAMILIES = {
    "reversal": ["hammer", "inverted_hammer", "hanging_man", "shooting_star", "dragonfly_doji", "gravestone_doji",
                 "engulfing", "harami", "piercing", "dark_cloud", "morning_evening_star", "three_inside", "tweezer",
                 "pin_bar"],
    "continuation": ["three_soldiers_crows", "marubozu", "tall_trend_bar"],
    "breakout": ["inside_bar_breakout", "nr7_breakout", "outside_bar"],
    "closeloc": ["clv_extreme", "clv5_extreme", "bar_80_20"],
    "exhaustion": ["five_lower_lows_higher_highs"],
}
SWING_K = (5, 10)
FIB_LEVELS = (0.382, 0.5, 0.618)
FIB_TOL = 0.15                                                       # R20 units
TOD = {"asia": None, "europe": (120, 480), "uspre": (480, 570), "open": (570, 630), "midday": (630, 900),
       "close": (900, 1080)}                                         # minutes of the bar start; asia = the rest
MARKETS = ("ES", "NQ", "YM")

_SWING_COLS = [f"{c}_{k}" for k in SWING_K for c in ("dist_swhi", "dist_swlo", "brk", "struct", "fibpos", "atfib")]
_BASE_COLS = ([f"pat_{p}" for p in DIRECTIONAL + NEUTRAL] + [f"fam_{f}" for f in FAMILIES] + _SWING_COLS
              + ["ema_stack", "ema20_slope", "dist_ema8", "dist_ema20", "dist_ema50", "above_ema20_share",
                 "mom", "mom_slope3", "mom_x100", "dist_vwap",
                 "rng_rel", "body_frac", "clv", "vol_rel", "gap_open", "day_range_rel", "day_ret"]
              + [f"tod_{t}" for t in TOD] + [f"dow_{i}" for i in range(5)]
              + ["h1_ema_stack", "h1_mom", "h1_struct_5"])
_UNSIGNED = set([f"pat_{p}" for p in NEUTRAL] + [f"atfib_{k}" for k in SWING_K]
                + ["rng_rel", "body_frac", "vol_rel", "day_range_rel"]
                + [f"tod_{t}" for t in TOD] + [f"dow_{i}" for i in range(5)])


def _x_cols(m):
    return [f"x_{m}_ret", f"x_{m}_ema_stack"]


# every signed column name any market can have (the x_ columns of all MARKETS included)
SIGNED = [c for c in _BASE_COLS if c not in _UNSIGNED] + [c for m in MARKETS for c in _x_cols(m)]
MIRROR = {f"dist_swhi_{k}": f"dist_swlo_{k}" for k in SWING_K}      # swapped for shorts by orient()

# winsorizing bounds of F (module docstring, "Winsorizing"): R20-unit and ratio columns +-50, fibpos +-10 leg lengths
CLIP_R20, CLIP_FIB = 50.0, 10.0
CLIP = {**{f"{c}_{k}": CLIP_R20 for k in SWING_K for c in ("dist_swhi", "dist_swlo")},
        **{f"fibpos_{k}": CLIP_FIB for k in SWING_K},
        **{c: CLIP_R20 for c in ("ema20_slope", "dist_ema8", "dist_ema20", "dist_ema50", "dist_vwap", "rng_rel",
                                 "vol_rel", "gap_open", "day_range_rel", "day_ret")},
        **{f"x_{m}_ret": CLIP_R20 for m in MARKETS}}


def COLUMNS(sym, others=MARKETS):
    """Column order of build_features(sym, ..., others)."""
    return _BASE_COLS + [c for m in others if m != sym for c in _x_cols(m)]


# --------------------------------------------------------------------------------------------- small helpers
def _run_ok(run, k):
    """ok[t] = bar t-k exists and is in the same contract run as bar t."""
    out = np.zeros(len(run), bool)
    if k < len(run):
        out[k:] = run[k:] == run[:-k] if k else True
    return out


def _lag(a, k):
    out = np.full(len(a), np.nan)
    if k < len(a):
        out[k:] = a[:-k]
    return out


def _last_true(mask):
    """j[t] = largest index <= t where mask is True, -1 if none."""
    return np.maximum.accumulate(np.where(mask, np.arange(len(mask)), -1))


def _div(a, b):
    with np.errstate(divide="ignore", invalid="ignore"):
        out = a / b
    return np.where(np.isfinite(out), out, np.nan)


def r20(b, tick):
    """Scale unit: mean (H - L) of the 20 bars before t (same run), floored at 2 ticks; NaN in the first 20 bars."""
    rng = (b.H - b.L).to_numpy(np.float64)
    m = pd.Series(rng).rolling(20).mean().to_numpy()
    out = np.full(len(rng), np.nan)
    out[1:] = m[:-1]
    out = np.where(_run_ok(b.run.to_numpy(), 20), out, np.nan)
    return np.maximum(out, 2 * tick)                                 # NaN stays NaN


def _swing_side(piv, vals, run, k):
    """Latest CONFIRMED swing on one side (pivot p known at the close of p+k), per bar:
    level, previous level (same run), pivot bar index (-1 if none), confirmation bar index j (-1 if none)."""
    n = len(run)
    idx = np.flatnonzero(piv)
    conf = idx + k
    lvl_at = np.full(n, np.nan); prev_at = np.full(n, np.nan); p_at = np.full(n, -1)
    lvl_at[conf] = vals[idx]
    prev = np.r_[np.nan, vals[idx[:-1]]]
    if len(idx):
        prev[np.r_[True, run[idx[1:]] != run[idx[:-1]]]] = np.nan
    prev_at[conf] = prev
    p_at[conf] = idx
    mask = np.zeros(n, bool); mask[conf] = True
    j = _last_true(mask)
    ok = (j >= 0) & (run[np.maximum(j, 0)] == run)
    jj = np.maximum(j, 0)
    level = np.where(ok, lvl_at[jj], np.nan)
    prevl = np.where(ok, prev_at[jj], np.nan)
    pbar = np.where(ok, p_at[jj], -1)
    return level, prevl, pbar, np.where(ok, j, -1)


def _first_since(cond, j):
    """cond[t] AND it is the first bar in (j[t], t] where cond holds (j = -1 -> False)."""
    cs = np.cumsum(cond.astype(np.int64))
    since = cs - cs[np.maximum(j, 0)]
    return cond & (j >= 0) & (since == 1)


def struct_k(b, k):
    """+1 / -1 / 0 market structure from the last two confirmed swing highs and lows (NaN until both have two)."""
    run = b.run.to_numpy()
    lo_piv, hi_piv = sg.pivots(b, k)
    hi, hi_p, _, _ = _swing_side(hi_piv, b.H.to_numpy(np.float64), run, k)
    lo, lo_p, _, _ = _swing_side(lo_piv, b.L.to_numpy(np.float64), run, k)
    s = np.where((hi > hi_p) & (lo > lo_p), 1.0, np.where((hi < hi_p) & (lo < lo_p), -1.0, 0.0))
    return np.where(np.isfinite(hi) & np.isfinite(hi_p) & np.isfinite(lo) & np.isfinite(lo_p), s, np.nan)


def structure(b, k, R):
    """dist_swhi/dist_swlo/brk/struct/fibpos/atfib for pivot size k (dict of arrays)."""
    run = b.run.to_numpy()
    C = b.C.to_numpy(np.float64)
    lo_piv, hi_piv = sg.pivots(b, k)
    hi, hi_p, hi_bar, hi_j = _swing_side(hi_piv, b.H.to_numpy(np.float64), run, k)
    lo, lo_p, lo_bar, lo_j = _swing_side(lo_piv, b.L.to_numpy(np.float64), run, k)
    out = {}
    out[f"dist_swhi_{k}"] = (C - hi) / R
    out[f"dist_swlo_{k}"] = (C - lo) / R
    up = _first_since(np.nan_to_num(C - hi, nan=-1.0) > 0, hi_j)
    dn = _first_since(np.nan_to_num(C - lo, nan=1.0) < 0, lo_j)
    out[f"brk_{k}"] = up.astype(float) - dn.astype(float)
    s = np.where((hi > hi_p) & (lo > lo_p), 1.0, np.where((hi < hi_p) & (lo < lo_p), -1.0, 0.0))
    out[f"struct_{k}"] = np.where(np.isfinite(hi) & np.isfinite(hi_p) & np.isfinite(lo) & np.isfinite(lo_p), s, np.nan)
    have = np.isfinite(hi) & np.isfinite(lo)
    legup = hi_bar > lo_bar
    start = np.where(legup, lo, hi); end = np.where(legup, hi, lo)
    span = end - start
    pos = _div(C - start, span)
    # one bar that is both the latest swing high and low (big outside bar): the leg's direction is unknown -> NaN
    # (treating it as a down leg would be an arbitrary, systematically bearish sign)
    out[f"fibpos_{k}"] = np.where(have & (hi_bar != lo_bar), pos * np.where(legup, 1.0, -1.0), np.nan)
    near = np.zeros(len(C), bool)
    for f in FIB_LEVELS:
        near |= np.abs(C - (start + f * span)) <= FIB_TOL * R
    out[f"atfib_{k}"] = np.where(have & np.isfinite(R) & (span != 0), near.astype(float), np.nan)
    return out


def mom_cross_100(m14, run):
    """mom_x100: +1 if mom14 is above 100 on bar t and the last mom14 != 100 before t (same run) was below 100,
    -1 for the mirror, else 0. A run of exact 100s in between is skipped, so touching 100 and going back to the same
    side is no cross; with no earlier side known (only 100s since the warm-up) leaving 100 counts as a cross.
    NaN while mom14[t] or mom14[t-1] (same run) is NaN. Uses bars <= t only."""
    m14 = np.asarray(m14, np.float64)
    run = np.asarray(run)
    n = len(m14)
    mp = np.where(_run_ok(run, 1), _lag(m14, 1), np.nan)
    j = _last_true(np.isfinite(m14) & (m14 != 100))                    # last bar <= t with mom14 off 100
    jp = np.r_[-1, j[:-1]] if n else j                                  # ... strictly before t
    jj = np.maximum(jp, 0)
    side = np.where((jp >= 0) & (run[jj] == run), np.sign(m14[jj] - 100), 0.0)   # -1 / +1, 0 = none known yet
    x = np.where((m14 > 100) & (side <= 0), 1.0, np.where((m14 < 100) & (side >= 0), -1.0, 0.0))
    return np.where(np.isfinite(m14) & np.isfinite(mp), x, np.nan)


def _ema_stack(ctx):
    t = ctx.trend.to_numpy(np.float64)
    return np.where(ctx.ema50.notna().to_numpy(), t, np.nan)


def session_features(b, R):
    """gap_open, day_range_rel, day_ret (segment = one session of one contract)."""
    seg = b.seg.to_numpy(); run = b.run.to_numpy()
    O, H, L, C = (b[x].to_numpy(np.float64) for x in "OHLC")
    n = len(b)
    start = np.r_[True, seg[1:] != seg[:-1]] if n else np.zeros(0, bool)
    fi = _last_true(start)
    prev = fi - 1
    okp = (prev >= 0) & (run[np.maximum(prev, 0)] == run[fi])
    gap = np.where(okp, (O[fi] - C[np.maximum(prev, 0)]) / R[fi], np.nan)
    hi = pd.Series(H).groupby(seg).cummax().to_numpy()
    lo = pd.Series(L).groupby(seg).cummin().to_numpy()
    codes, _ = pd.factorize(seg)
    full = (pd.Series(H).groupby(codes).max() - pd.Series(L).groupby(codes).min()).to_numpy()
    prior = pd.Series(full).rolling(20).mean().shift(1).to_numpy()
    return {"gap_open": gap, "day_range_rel": _div(hi - lo, prior[codes]), "day_ret": (C - O[fi]) / R}


def time_features(index):
    m = (index.hour * 60 + index.minute).to_numpy()
    out = {}
    rest = np.ones(len(m), bool)
    for name, rng in TOD.items():
        if rng is not None:
            x = (m >= rng[0]) & (m < rng[1])
            rest &= ~x
            out[f"tod_{name}"] = x
    out["tod_asia"] = rest
    out = {f"tod_{t}": out[f"tod_{t}"].astype(float) for t in TOD}
    dow = (index + pd.Timedelta(hours=6)).day_of_week.to_numpy()
    for i in range(5):
        out[f"dow_{i}"] = (dow == i).astype(float)
    return out


def htf_features(b, tf, b60, ctx60):
    """60-min ema_stack, mom, struct_5 from the latest 60-min bar of the same contract that closed by t's close."""
    vals = np.column_stack([_ema_stack(ctx60), (ctx60.mom14 - 100).to_numpy(np.float64), struct_k(b60, 5)])
    out = np.full((len(b), 3), np.nan)
    close_t = (b.index + pd.Timedelta(minutes=tf)).to_numpy()
    close60 = (b60.index + pd.Timedelta(minutes=60)).to_numpy()
    inst, inst60 = b.inst.to_numpy(), b60.inst.to_numpy()
    for u in np.unique(inst):
        r = np.flatnonzero(inst == u)
        r60 = np.flatnonzero(inst60 == u)
        if not len(r60):
            continue
        j = np.searchsorted(close60[r60], close_t[r], side="right") - 1
        ok = j >= 0
        out[r[ok]] = vals[r60[j[ok]]]
    return {"h1_ema_stack": out[:, 0], "h1_mom": out[:, 1], "h1_struct_5": out[:, 2]}


def cross_features(b, m, bo, ctxo, Ro):
    """x_<m>_ret and x_<m>_ema_stack from market m's bar with the same start time (NaN if it has none)."""
    keep = ~bo.index.duplicated(keep="last")
    ret = ((bo.C - bo.O).to_numpy(np.float64) / Ro)[keep]
    st = _ema_stack(ctxo)[keep]
    pos = bo.index[keep].get_indexer(b.index)
    ok = pos >= 0
    p = np.maximum(pos, 0)
    return {f"x_{m}_ret": np.where(ok, ret[p] if len(ret) else np.nan, np.nan),
            f"x_{m}_ema_stack": np.where(ok, st[p] if len(st) else np.nan, np.nan)}


# --------------------------------------------------------------------------------------------- main
def compute_features(b, ctx, P, tf, tick, b60=None, ctx60=None, xmk=None):
    """Feature frame from frames already built. b: signals.bars-like frame (O H L C V inst sess vwap seg run),
    ctx: signals.context(b), P: signals.patterns(b, ctx). b60/ctx60: 60-min bars and context (h1_ columns NaN if
    None). xmk: {market: (bars, context, R20 array)} for the cross-market columns."""
    n = len(b)
    R = r20(b, tick)
    run = b.run.to_numpy()
    O, H, L, C = (b[x].to_numpy(np.float64) for x in "OHLC")
    V = b.V.to_numpy(np.float64)
    f = {}
    for p in DIRECTIONAL + NEUTRAL:
        f[f"pat_{p}"] = P[p].to_numpy(np.float64)
    for fam, mem in FAMILIES.items():
        f[f"fam_{fam}"] = np.clip(sum(P[p].to_numpy(np.float64) for p in mem), -1, 1)
    for k in SWING_K:
        f.update(structure(b, k, R))
    e8, e20, e50 = (ctx[c].to_numpy(np.float64) for c in ("ema8", "ema20", "ema50"))
    f["ema_stack"] = _ema_stack(ctx)
    f["ema20_slope"] = np.where(_run_ok(run, 10), (e20 - _lag(e20, 10)) / R, np.nan)
    f["dist_ema8"], f["dist_ema20"], f["dist_ema50"] = (C - e8) / R, (C - e20) / R, (C - e50) / R
    ab = np.where(np.isfinite(e20), (C > e20).astype(float), np.nan)
    f["above_ema20_share"] = 2 * pd.Series(ab).rolling(20).mean().to_numpy() - 1      # NaN unless 20 valid EMAs
    m14 = ctx.mom14.to_numpy(np.float64)
    f["mom"] = m14 - 100
    f["mom_slope3"] = np.where(_run_ok(run, 3), m14 - _lag(m14, 3), np.nan)
    f["mom_x100"] = mom_cross_100(m14, run)
    f["dist_vwap"] = (C - b.vwap.to_numpy(np.float64)) / R
    rng = H - L
    f["rng_rel"] = rng / R
    f["body_frac"] = np.where(rng > 0, np.abs(C - O) / np.where(rng > 0, rng, 1), 0.0)
    f["clv"] = np.where(rng > 0, 2 * (C - L) / np.where(rng > 0, rng, 1) - 1, 0.0)
    vm = np.where(_run_ok(run, 20), _lag(pd.Series(V).rolling(20).mean().to_numpy(), 1), np.nan)
    f["vol_rel"] = _div(V, vm)
    f.update(session_features(b, R))
    f.update(time_features(b.index))
    if b60 is not None:
        f.update(htf_features(b, tf, b60, ctx60))
    else:
        f.update({c: np.full(n, np.nan) for c in ("h1_ema_stack", "h1_mom", "h1_struct_5")})
    for m, (bo, ctxo, Ro) in (xmk or {}).items():
        f.update(cross_features(b, m, bo, ctxo, Ro))
    cols = _BASE_COLS + [c for m in (xmk or {}) for c in _x_cols(m)]
    for c in cols:
        if c in CLIP:                                                   # winsorize (NaN stays NaN)
            f[c] = np.clip(np.asarray(f[c], np.float64), -CLIP[c], CLIP[c])
    F = pd.DataFrame({c: np.asarray(f[c], np.float64).astype(np.float32) for c in cols}, index=b.index)
    return F


_CACHE = {}


def clear_cache():
    _CACHE.clear()


def _load(sym, tf, cache=True):
    """(bars, context) of sym at tf, memoised in-process."""
    key = (sym, tf)
    if cache and key in _CACHE:
        return _CACHE[key]
    tick = sg.SPEC[sym]["tick"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        b = sg.bars(sym, tf)
        ctx = sg.context(b, tick=tick)
    if cache:
        _CACHE[key] = (b, ctx)
    return b, ctx


def build_features(sym, tf, others=MARKETS, cache=True):
    """(b, F) for market sym at tf minutes. b = signals.bars(sym, tf) + signals.context columns + R20 (scale unit);
    F = float32 feature frame on b.index (see the module docstring). others: markets for the x_<SYM>_ columns
    (sym itself is skipped). cache=False rebuilds every bar frame from research_lib.bars_1m."""
    tick = sg.SPEC[sym]["tick"]
    b, ctx = _load(sym, tf, cache)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        P = sg.patterns(b, ctx, tick=tick)
    b60, ctx60 = _load(sym, 60, cache)
    xmk = {}
    for m in others:
        if m == sym:
            continue
        bo, co = _load(m, tf, cache)
        xmk[m] = (bo, co, r20(bo, sg.SPEC[m]["tick"]))
    F = compute_features(b, ctx, P, tf, tick, b60, ctx60, xmk)
    # ctx is computed row by row from b: attach by position. b.join(ctx) duplicated rows when two contracts share a
    # bar time (120-min bars on December roll Sundays: old and new contract both have an 18:00 bar).
    assert len(ctx) == len(b) and (ctx.index == b.index).all()
    bb = b.copy()
    for c in ctx.columns.difference(b.columns, sort=False):
        bb[c] = ctx[c].to_numpy()
    bb["R20"] = r20(b, tick)
    return bb, F


def orient(F, d):
    """F seen from direction d (+1 long, -1 short; scalar or array of len(F)), float32: SIGNED columns times d; for
    shorts each MIRROR pair swaps (a short's dist_swhi_k = -dist_swlo_k, dist_swlo_k = -dist_swhi_k). Identical to
    walkforward.orient(F, d, SIGNED, MIRROR); see the module docstring for what is and is not mirror-symmetric."""
    d = np.broadcast_to(np.asarray(d, np.float32), (len(F),)).astype(np.float32)
    G = F.astype(np.float32, copy=True)
    cols = [c for c in SIGNED if c in F.columns]
    if cols:
        G[cols] = G[cols].to_numpy(np.float32) * d[:, None]
    short = d < 0
    for a, c in MIRROR.items():
        if a in F.columns and c in F.columns:
            va, vc = F[a].to_numpy(np.float32), F[c].to_numpy(np.float32)
            G[a] = np.where(short, -vc, va).astype(np.float32)
            G[c] = np.where(short, -va, vc).astype(np.float32)
    return G


if __name__ == "__main__":
    import time
    for s in MARKETS:
        t0 = time.time()
        b, F = build_features(s, 15)
        print(f"{s}: {len(F)} rows x {F.shape[1]} cols in {time.time() - t0:.1f}s; "
              f"NaN share {F.isna().to_numpy().mean():.3f}")
    print(list(F.columns))
