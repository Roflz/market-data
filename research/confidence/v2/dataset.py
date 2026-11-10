"""
v2/dataset.py - the v2 dataset of the user's setup: trend pullbacks on 5 / 15 / 60-min bars of MNQ / MES / MYM,
one row per signal bar and direction, with features known at the signal bar's CLOSE and labels under 11 exits.

EVENTS (base timeframe B in 5, 15, 60; longs in uptrends, shorts in downtrends; entry = open of the next bar)
  pb        pullbacks.detect (impulse leg, first pullback low PL, depth 0.1-1; event bar = PL + 3 bars, or later when
            the leg's swing high is confirmed later). Stop = 1 tick beyond PL.
  ema8_pb, ema20_pb, ema50_pb, mom_turn, pb_break   trigger_scan.detect rules. Stop = 1 tick beyond the lowest low of
            the last 5 bars (highest high for shorts).
  Every stop is at least 1 R20 from the signal bar's close (R20 = mean range of the 20 bars before, fe.r20).
  Several rules on the same bar and direction -> ONE row with a 0/1 flag per rule (n_rules = how many fired); the
  stop is then the pb stop if pb fired, else the 5-bar stop (stop_src 'pb_low' / 'low5'). Only enterable bars
  (labels.eligible with v2/lucid.py installed: flat 16:45-18:00).
POOL ('drift benchmark' rows): every other bar in trigger_scan's trend (EMA8 > EMA20 > EMA50 and EMA50 rising vs 5
  bars before, mirror for shorts) that is NOT an event, with the 5-bar stop rule and the same exits:
  v2/out/v2_trend_{sym}_{tf}.parquet. Matched on side / year / hour / stop size it answers "what does simply being in
  the trend at those hours earn with the same stop and exit".

FEATURES (all at the signal bar's close; other timeframes through mtf_scan.latest_closed = the latest bar of that
  timeframe of the SAME contract that has CLOSED by the signal bar's close; + = in the trade's direction)
  m{5,15,60}_trend     +1 the EMA stack + EMA50 slope agrees with the trade, -1 opposite, 0 neither (NaN warm-up)
  m*_s820, m*_s2050    (EMA8 - EMA20) / R20, (EMA20 - EMA50) / R20 of that timeframe (its own R20)
  m*_c20, m*_c50       (close - EMA20) / R20, (close - EMA50) / R20
  m*_mom, m*_mslope3   Momentum(14) - 100, and Momentum(14) minus its value 3 bars before
  m*_struct            +1 the last two confirmed swing highs AND lows rise with the trade, -1 both against, 0 mixed
  m*_sw_room           distance from the close to the last confirmed swing on the TARGET side (long: swing high -
                       close) in R20 (negative = already beyond it);  m*_sw_cushion = to the stop-side swing (long:
                       close - swing low). Swings = signals' 3-bar fractals, known 3 bars after the pivot.
  day_room, day_cushion  (session high so far - close) / R20 and (close - session low so far) / R20 (mirror for
                       shorts); day_pos = position in the session's range so far (1 = at the with-trade extreme);
                       day_range_R = range so far / R20; vwap_side (+1 / -1), vwap_dist = (close - VWAP) / R20;
                       gap = (session open - prior session close) / R20; prior_range = prior session range / R20.
                       Session = one Globex session of one contract (signals' seg), base timeframe bars.
  pat_with3, pat_against3  number of directional candle patterns (signals.patterns, 24) pointing with / against the
                       trade on the last 3 bars; rev_at_low = a reversal-family pattern pointing with the trade on the
                       pullback-low bar or the bar after it (low bar = PL for pb rows, else the 5-bar low bar).
  pb_depth, pb_bars, pb_div, pb_momflip   pullback geometry of the detector (NaN when pb did not fire).
  min_since_18, tod_18_22 / tod_23_02 / tod_03_08 / tod_09_11 / tod_12_16 (hour of the signal bar's close = entry
                       time), dow (session weekday, 0 = Monday).
  risk_R20 = (close - stop) / R20 (oriented), cost_R = cost $ / (close-to-stop $), cost_bar = cost $ / (R20 $).
  n_tf_agree = number of 5/15/60 trends agreeing (0-3); mtf_score = mtf_scan's 3 signals: mtf_trend60 (60-min trend
                       agrees) + mtf_trig5 (a 5-min pullback trigger the same way in the last 6 five-min bars) +
                       mtf_mom5 (last 5-min bar: Momentum rose and EMA8 > EMA20; mirror for shorts).
LABELS (exit_study.simulate on the 1-minute path; costs $1 + 1 tick each way, +1 tick on stop fills; entry stop
  always kept; flat at the last bar closing by 16:45; evening entries may run into the next day):
  hold        stop only, to the 16:45 forced-exit bar
  ema_cross   EMA8 crosses EMA20 against the trade -> out at the next bar's open
  fixed15     the old 1.5R target, 16-bar limit (reference only)
  opp{N}_1b / opp{N}_2b, N = 1..4   OPPOSITE-EVIDENCE exits: at each bar close count how many of these 7 point
              against the trade: (1) a reversal-family pattern against it, (2) Momentum(14) moved against it this bar,
              (3) close on the wrong side of EMA20, (4) EMA8 on the wrong side of EMA20, (5) close beyond the last
              confirmed swing low (high for shorts), (6) the latest closed 60-min trend not agreeing (no 60-min
              value yet = no evidence), (7) a 5-min pullback trigger the other way inside this bar. Exit at the next
              bar's open when the count >= N. _1b counts this bar only; _2b counts each kind once if it showed on
              this bar or the bar before (the bar before can be the signal bar).
  Columns pnl_<x> (net $ per micro), R_<x> (= pnl / entry-to-stop $), bars_<x> (bars held), kind_<x> (0 time /
  1 stop / 2 target / 3 rule exit), t_exit_<x> (rule exits: end of the next bar's first minute; time exits: the
  bar close; stop / target exits: the CLOSE of the bar in which the fill happened - up to tf minutes late).

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 -u \
      v2/dataset.py NQ ES YM --tf 60,15,5 [--check]
"""
import argparse
import gc
import os
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import lucid

lucid.install()                                         # flat 16:45-18:00, before labels / exit_study are used

import exit_study as xs                                  # noqa: E402
import features as fe                                    # noqa: E402
import labels as lb                                      # noqa: E402
import mtf_scan as ms                                    # noqa: E402
import pullbacks as pbk                                  # noqa: E402
import signals as sg                                     # noqa: E402
import trigger_scan as ts                                # noqa: E402
import walkforward as wf                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TFS = (5, 15, 60)
RULES = ["ema8_pb", "ema20_pb", "ema50_pb", "mom_turn", "pb_break"]
FLAGS = ["pb"] + RULES
N_LIST = (1, 2, 3, 4)
WINDOWS_B = (1, 2)
EXITS = ["hold", "ema_cross", "fixed15"] + [f"opp{n}_{w}b" for n in N_LIST for w in WINDOWS_B]
HOLD_BARS = 10 ** 6
TOD_BLOCKS = {"18_22": (18, 19, 20, 21, 22), "23_02": (23, 0, 1, 2), "03_08": (3, 4, 5, 6, 7, 8),
              "09_11": (9, 10, 11), "12_16": (12, 13, 14, 15, 16)}
EVIDENCE = ["rev_pattern", "mom_against", "close_vs_ema20", "ema8_vs_ema20", "beyond_swing", "trend60_lost",
            "opp_trigger5"]
RAW_SIGNED = ["trend", "s820", "s2050", "c20", "c50", "mom", "mslope3", "struct"]
RAW_KEYS = RAW_SIGNED + ["up", "dn"]                  # up = (swing high - C) / R, dn = (C - swing low) / R
_MIN = pd.Timedelta(minutes=1)


# ------------------------------------------------------------------------------------------------ per-timeframe
def _lagr(x, k, run):
    """x[t-k] if bar t-k is in the same run as t, else NaN."""
    return np.where(fe._run_ok(run, k), fe._lag(np.asarray(x, np.float64), k), np.nan)


def trend_nan(ctx, run):
    """trigger_scan's trend: +1 EMA8 > EMA20 > EMA50 and EMA50 above its value 5 bars before (same run), -1 mirror,
    0 neither; NaN while EMA50 or its 5-bar lag is not valid."""
    e8, e20, e50 = (ctx[c].to_numpy(np.float64) for c in ("ema8", "ema20", "ema50"))
    e50_5 = _lagr(e50, 5, run)
    up = (e8 > e20) & (e20 > e50) & (e50 > e50_5)
    dn = (e8 < e20) & (e20 < e50) & (e50 < e50_5)
    out = np.where(up, 1.0, np.where(dn, -1.0, 0.0))
    out[~(np.isfinite(e50) & np.isfinite(e50_5) & np.isfinite(e8))] = np.nan
    return out


def prep_tf(b, ctx, P, tick, tf):
    """Everything per bar of one timeframe that needs no other timeframe (dict)."""
    run = b.run.to_numpy()
    seg = b.seg.to_numpy()
    R = fe.r20(b, tick)
    C = b.C.to_numpy(np.float64)
    e8, e20, e50 = (ctx[c].to_numpy(np.float64) for c in ("ema8", "ema20", "ema50"))
    mom = ctx.mom14.to_numpy(np.float64)
    st = fe.structure(b, 3, R)
    raw = dict(trend=trend_nan(ctx, run), s820=(e8 - e20) / R, s2050=(e20 - e50) / R, c20=(C - e20) / R,
               c50=(C - e50) / R, mom=mom - 100, mslope3=mom - _lagr(mom, 3, run), struct=st["struct_3"],
               up=-st["dist_swhi_3"], dn=st["dist_swlo_3"])
    dirc = [c for c in fe.DIRECTIONAL if c in P.columns]
    rev = [c for c in fe.FAMILIES["reversal"] if c in P.columns]
    A = P[dirc].to_numpy(np.int8)
    Rv = P[rev].to_numpy(np.int8)
    nb, ns = (A == 1).sum(1).astype(np.float64), (A == -1).sum(1).astype(np.float64)
    # last 3 bars of the same segment
    nb3, ns3 = nb.copy(), ns.copy()
    for k in (1, 2):
        okk = fe._run_ok(seg, k)
        nb3 += np.where(okk, fe._lag(nb, k), 0.0)
        ns3 += np.where(okk, fe._lag(ns, k), 0.0)
    T = ts.detect(b, ctx, tick, tf)
    trig = T[T.rule != "trend_all"]
    n = len(b)
    fired = {d: np.zeros(n, bool) for d in (1, -1)}
    for d in (1, -1):
        fired[d][trig.loc[trig.d == d, "i"].to_numpy()] = True
    return dict(b=b, ctx=ctx, P=P, R=R, raw=raw, run=run, seg=seg, tf=tf, T=T, fired=fired,
                rev_bull=(Rv == 1).any(1), rev_bear=(Rv == -1).any(1), nb3=nb3, ns3=ns3)


def load_frames(sym, tfs=TFS, end=wf.HOLDOUT_SESSION_START):
    """{tf: prep_tf(...)} from signals.bars (research_lib.bars_1m), cut BEFORE the locked holdout before any
    indicator is computed."""
    tick = sg.SPEC[sym]["tick"]
    F = {}
    for tf in tfs:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            b = sg.bars(sym, tf)
            b = b.loc[b.index < end]
            ctx = sg.context(b, tick=tick)
            P = sg.patterns(b, ctx, tick=tick)
        F[tf] = prep_tf(b, ctx, P, tick, tf)
        gc.collect()
    return F


def at_base(F, B, tf, vals, rows=None):
    """vals (per bar of timeframe tf) seen from base-timeframe bars (all, or positions `rows`): the latest bar of tf
    of the same contract that closed by the base bar's close."""
    bB = F[B]["b"] if rows is None else F[B]["b"].iloc[rows]
    vals = np.asarray(vals, np.float64)
    if tf == B:
        v = vals.reshape(len(F[B]["b"]), -1)
        return v if rows is None else v[rows]
    return ms.latest_closed(bB, B, F[tf]["b"], tf, vals)


def recent5(F, k=6):
    """5-min trigger fired the same way in the last k five-min bars (same run): {d: float array per 5-min bar}."""
    f5 = F[5]
    out = {}
    for d in (1, -1):
        x = f5["fired"][d].astype(np.float64)
        r = x.copy()
        for q in range(1, k):
            r = np.fmax(r, np.where(fe._run_ok(f5["run"], q), fe._lag(x, q), 0.0))
        out[d] = r
    return out


def mom5(F):
    f5 = F[5]
    mom = f5["ctx"].mom14.to_numpy(np.float64)
    dm = mom - _lagr(mom, 1, f5["run"])
    e8, e20 = (f5["ctx"][c].to_numpy(np.float64) for c in ("ema8", "ema20"))
    return np.where((dm > 0) & (e8 > e20), 1.0, np.where((dm < 0) & (e8 < e20), -1.0, 0.0))


def within_bar(F, B, flags5):
    """any(flags5) over the 5-min bars inside each base bar (same contract, 5-min start floored to B minutes):
    those 5-min bars all close by the base bar's close."""
    if B == 5:
        return flags5.astype(bool)
    b5, bB = F[5]["b"], F[B]["b"]
    kB = pd.MultiIndex.from_arrays([bB.inst.to_numpy(), bB.index])
    if not kB.is_unique:
        raise ValueError("base bars not unique per (contract, start)")
    k5 = pd.MultiIndex.from_arrays([b5.inst.to_numpy(), b5.index.floor(f"{B}min")])
    pos = kB.get_indexer(k5)
    ok = (pos >= 0) & flags5.astype(bool)
    out = np.zeros(len(bB), bool)
    out[pos[ok]] = True
    return out


def evidence_types(F, B):
    """{d: (n_B, 7) bool}: the 7 kinds of opposite evidence AGAINST a trade of direction d at each base bar's close."""
    f = F[B]
    b, ctx = f["b"], f["ctx"]
    C = b.C.to_numpy(np.float64)
    e8, e20 = (ctx[c].to_numpy(np.float64) for c in ("ema8", "ema20"))
    mom = ctx.mom14.to_numpy(np.float64)
    dm = mom - _lagr(mom, 1, f["run"])
    swl, swh = ctx.swing_lo.to_numpy(np.float64), ctx.swing_hi.to_numpy(np.float64)
    t60 = at_base(F, B, 60, F[60]["raw"]["trend"])[:, 0]
    opp5 = {d: within_bar(F, B, F[5]["fired"][-d]) for d in (1, -1)}   # trigger the OTHER way inside the bar
    with np.errstate(invalid="ignore"):
        L = np.column_stack([f["rev_bear"], dm < 0, C < e20, e8 < e20, C < swl,
                             np.isfinite(t60) & (t60 != 1), opp5[1]])
        S = np.column_stack([f["rev_bull"], dm > 0, C > e20, e8 > e20, C > swh,
                             np.isfinite(t60) & (t60 != -1), opp5[-1]])
    return {1: L, -1: S}


def evidence_counts(types):
    """{(d, w): count per bar}: w = 1 this bar only; w = 2 each kind once if on this bar or the bar before."""
    out = {}
    for d, X in types.items():
        out[(d, 1)] = X.sum(1)
        prev = np.vstack([np.zeros((1, X.shape[1]), bool), X[:-1]])
        out[(d, 2)] = (X | prev).sum(1)
    return out


def exit_rules(F, B):
    """{exit name: (simulate args, max_bars, rule_exit or None)}."""
    cnt = evidence_counts(evidence_types(F, B))
    ctx = F[B]["ctx"]
    diff = ctx.ema8.to_numpy(np.float64) - ctx.ema20.to_numpy(np.float64)
    prev = np.r_[np.nan, diff[:-1]]
    with np.errstate(invalid="ignore"):
        cross = ((diff < 0) & (prev >= 0), (diff > 0) & (prev <= 0))
    day = (None, None, False, None, "day")
    out = {"hold": (day, HOLD_BARS, None), "ema_cross": (day, HOLD_BARS, cross),
           "fixed15": ((1.5, None, False, None, "16"), 16, None)}
    for n in N_LIST:
        for w in WINDOWS_B:
            out[f"opp{n}_{w}b"] = (day, HOLD_BARS, (cnt[(1, w)] >= n, cnt[(-1, w)] >= n))
    return out


# ------------------------------------------------------------------------------------------------ events
def union_events(F, B, sym):
    """One row per (bar, direction): flags per rule, stop, pullback geometry; and the trend pool."""
    f = F[B]
    b, ctx, P, R = f["b"], f["ctx"], f["P"], f["R"]
    tick = sg.SPEC[sym]["tick"]
    C = b.C.to_numpy(np.float64)
    ok, _ = lb.eligible(b, B)
    T = f["T"]
    trg = T[T.rule.isin(RULES)]
    E = (trg.assign(v=1).pivot_table(index=["i", "d"], columns="rule", values="v", aggfunc="max", fill_value=0)
         .reindex(columns=RULES, fill_value=0))
    st5 = trg.groupby(["i", "d"]).stop.first()
    E["stop_low5"] = st5.reindex(E.index).to_numpy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        D = pbk.detect(b, ctx, k_leg=5, sym=sym, tf=B, pats=P)
    if len(D):
        D = D.rename(columns={"i_event": "i", "direction": "d"})
        D = D[ok[D.i.to_numpy()] & np.isfinite(R[D.i.to_numpy()])]
        D = D.sort_values(["i", "d", "i_SH"]).drop_duplicates(["i", "d"], keep="last")
        i, d = D.i.to_numpy(), D.d.to_numpy()
        pl = D.PL.to_numpy(np.float64)
        D["stop_pb"] = np.where(d > 0, np.minimum(pl - tick, C[i] - R[i]), np.maximum(pl + tick, C[i] + R[i]))
        D = D.set_index(["i", "d"])[["stop_pb", "i_PL", "depth", "bars_pullback", "divergence", "mom_flip",
                                     "event_wait"]]
        D["pb"] = 1
        E = E.join(D, how="outer")
    else:
        for c in ("stop_pb", "i_PL", "depth", "bars_pullback", "divergence", "mom_flip", "event_wait"):
            E[c] = np.nan
        E["pb"] = 0
    E[FLAGS] = E[FLAGS].fillna(0).astype(np.int8)
    E = E.reset_index()
    E["stop"] = np.where(E.pb == 1, E.stop_pb, E.stop_low5)
    E["stop_src"] = np.where(E.pb == 1, "pb_low", "low5")
    E["n_rules"] = E[FLAGS].sum(1).astype(np.int8)
    tr = T[T.rule == "trend_all"]
    tk = pd.MultiIndex.from_arrays([tr.i.to_numpy(), tr.d.to_numpy()])
    ek = pd.MultiIndex.from_arrays([E.i.to_numpy(), E.d.to_numpy()])
    E["in_trend"] = ek.isin(tk).astype(np.int8)
    E.insert(0, "t", b.index[E.i.to_numpy()])
    E = E.sort_values(["i", "d"]).reset_index(drop=True)
    pool = tr.loc[~tk.isin(ek), ["t", "i", "d", "stop"]].reset_index(drop=True)
    return E, pool


def build_features(F, B, E, sym):
    """Feature frame (float32) for the event rows E (columns i, d, stop, i_PL, flags, pb geometry)."""
    f = F[B]
    b, R = f["b"], f["R"]
    spec = sg.SPEC[sym]
    i = E.i.to_numpy(np.int64)
    d = E.d.to_numpy(np.float64)
    long_ = d > 0
    X = {}
    for tf in TFS:
        raw = F[tf]["raw"]
        M = at_base(F, B, tf, np.column_stack([raw[k] for k in RAW_KEYS]), rows=i)
        for q, k in enumerate(RAW_SIGNED):
            X[f"m{tf}_{k}"] = M[:, q] * d
        up, dn = M[:, RAW_KEYS.index("up")], M[:, RAW_KEYS.index("dn")]
        X[f"m{tf}_sw_room"] = np.where(long_, up, dn)
        X[f"m{tf}_sw_cushion"] = np.where(long_, dn, up)
    # day context (base timeframe, segment = one session of one contract)
    seg = f["seg"]
    H, L, C = (b[c].to_numpy(np.float64) for c in "HLC")
    hod = pd.Series(H).groupby(seg).cummax().to_numpy()[i]
    lod = pd.Series(L).groupby(seg).cummin().to_numpy()[i]
    c, r = C[i], R[i]
    rng = hod - lod
    X["day_room"] = np.where(long_, hod - c, c - lod) / r
    X["day_cushion"] = np.where(long_, c - lod, hod - c) / r
    with np.errstate(invalid="ignore", divide="ignore"):
        X["day_pos"] = np.where(rng > 0, np.where(long_, c - lod, hod - c) / rng, 0.5)
    X["day_range_R"] = rng / r
    vw = b.vwap.to_numpy(np.float64)[i]
    X["vwap_side"] = np.sign(d * (c - vw))
    X["vwap_dist"] = d * (c - vw) / r
    sf = fe.session_features(b, R)
    X["gap"] = d * sf["gap_open"][i]
    codes, _ = pd.factorize(seg)
    full = (pd.Series(H).groupby(codes).max() - pd.Series(L).groupby(codes).min()).to_numpy()
    cd = codes[i]
    X["prior_range"] = np.where(cd > 0, full[np.maximum(cd - 1, 0)], np.nan) / r
    # candles
    X["pat_with3"] = np.where(long_, f["nb3"][i], f["ns3"][i])
    X["pat_against3"] = np.where(long_, f["ns3"][i], f["nb3"][i])
    win = np.stack([np.maximum(i - q, 0) for q in range(ts.STOP_LOOKBACK - 1, -1, -1)], 1)   # i-4 .. i
    lo_bar = win[np.arange(len(i)), np.argmin(L[win], 1)]
    hi_bar = win[np.arange(len(i)), np.argmax(H[win], 1)]
    lows = np.where(long_, lo_bar, hi_bar).astype(np.int64)
    has_pl = E.pb.to_numpy() == 1
    lows[has_pl] = E.i_PL.to_numpy()[has_pl].astype(np.int64)
    rw = np.where(long_, f["rev_bull"][lows], f["rev_bear"][lows])
    nxt = np.minimum(lows + 1, i)
    rw |= np.where(long_, f["rev_bull"][nxt], f["rev_bear"][nxt]) & (nxt > lows)
    X["rev_at_low"] = rw.astype(np.float64)
    # pullback geometry (NaN without pb)
    X["pb_depth"] = np.where(has_pl, E.depth.to_numpy(np.float64), np.nan)
    X["pb_bars"] = np.where(has_pl, E.bars_pullback.to_numpy(np.float64), np.nan)
    X["pb_div"] = np.where(has_pl, E.divergence.astype(float).to_numpy(), np.nan)
    X["pb_momflip"] = np.where(has_pl, E.mom_flip.astype(float).to_numpy(), np.nan)
    # time (signal bar's close = entry time)
    tc = b.index[i] + pd.Timedelta(minutes=B)
    mins = (tc.hour * 60 + tc.minute).to_numpy()
    X["min_since_18"] = ((mins - 18 * 60) % 1440).astype(np.float64)
    hr = tc.hour.to_numpy()
    for k, hs in TOD_BLOCKS.items():
        X[f"tod_{k}"] = np.isin(hr, hs).astype(np.float64)
    X["dow"] = (b.index[i] + pd.Timedelta(hours=6)).dayofweek.to_numpy().astype(np.float64)
    # costs
    dist = d * (c - E.stop.to_numpy(np.float64))
    X["risk_R20"] = dist / r
    with np.errstate(divide="ignore", invalid="ignore"):
        X["cost_R"] = np.where(dist > 0, spec["cost"] / (dist * spec["usd"]), np.nan)
    X["cost_bar"] = spec["cost"] / (r * spec["usd"])
    # agreement
    X["n_tf_agree"] = sum((X[f"m{tf}_trend"] == 1).astype(np.float64) for tf in TFS)
    rec = recent5(F)
    V = at_base(F, B, 5, np.column_stack([rec[1], rec[-1], mom5(F)]), rows=i)
    X["mtf_trend60"] = (X["m60_trend"] == 1).astype(np.float64)
    X["mtf_trig5"] = (np.where(long_, V[:, 0], V[:, 1]) == 1).astype(np.float64)
    X["mtf_mom5"] = (V[:, 2] == d).astype(np.float64)
    X["mtf_score"] = X["mtf_trend60"] + X["mtf_trig5"] + X["mtf_mom5"]
    X["R20"] = r
    return pd.DataFrame({k: np.asarray(v, np.float64).astype(np.float32) for k, v in X.items()}, index=E.index)


def feature_columns():
    cols = [f"m{tf}_{k}" for tf in TFS for k in RAW_SIGNED + ["sw_room", "sw_cushion"]]
    cols += ["day_room", "day_cushion", "day_pos", "day_range_R", "vwap_side", "vwap_dist", "gap", "prior_range",
             "pat_with3", "pat_against3", "rev_at_low", "pb_depth", "pb_bars", "pb_div", "pb_momflip",
             "min_since_18"] + [f"tod_{k}" for k in TOD_BLOCKS] + ["dow", "risk_R20", "cost_R", "cost_bar",
                                                                    "n_tf_agree", "mtf_trend60", "mtf_trig5",
                                                                    "mtf_mom5", "mtf_score"]
    return cols


# ------------------------------------------------------------------------------------------------ labels
def label(sym, B, F, rows, m1, exits=None):
    """Labels for rows (t, i, d, stop) under every exit. Returns (rows kept, label frame aligned with them)."""
    b, ctx = F[B]["b"], F[B]["ctx"]
    spec = sg.SPEC[sym]
    rules = exit_rules(F, B)
    if exits is not None:
        rules = {k: v for k, v in rules.items() if k in exits}
    z = lb._prepare(sym, B, b, rows, HOLD_BARS, m1)
    rows = rows.iloc[z["sel"]].reset_index(drop=True)
    first = lb.map_1m(m1, b, B)[0]
    i = rows.i.to_numpy(np.int64)
    d = rows.d.to_numpy(np.int64)
    entry = b.O.to_numpy(np.float64)[i + 1]
    risk_usd = d * (entry - rows.stop.to_numpy(np.float64)) * spec["usd"]
    t_entry = b.index[i + 1]
    out = {"t_entry": t_entry, "entry": entry, "risk_usd": np.abs(risk_usd), "past_stop": risk_usd < 0}
    end_bar = (b.index + pd.Timedelta(minutes=B)).to_numpy()
    for name, (args, mb, rx) in rules.items():
        t0 = time.time()
        res, sel = xs.simulate(sym, B, b, ctx, rows, m1, *args, max_bars=mb, rule_exit=rx)
        if len(sel) != len(rows):
            raise RuntimeError(f"{name}: simulate kept {len(sel)} of {len(rows)} rows")
        pnl = res.pnl.to_numpy()
        kind = res.kind.to_numpy()
        held = res.bars_held.to_numpy()
        jx = np.minimum(i + held, len(b) - 1)                       # bar whose close ended (or signalled) the exit
        nx = first[np.minimum(jx + 1, len(b) - 1)]
        t_rule = np.where(nx >= 0, (m1.index[np.maximum(nx, 0)] + _MIN).to_numpy(), end_bar[jx])
        tx = np.where(kind == 3, t_rule, end_bar[jx])
        tx = np.where(held == 0, t_entry.to_numpy(), tx)            # past the stop at entry
        out[f"pnl_{name}"] = pnl
        with np.errstate(divide="ignore", invalid="ignore"):
            out[f"R_{name}"] = np.where(risk_usd > 0, pnl / risk_usd, np.nan)
        out[f"bars_{name}"] = held
        out[f"kind_{name}"] = kind
        out[f"t_exit_{name}"] = tx
        print(f"    {name:10s} {time.time() - t0:5.0f}s  ${np.nanmean(pnl):+.2f}/trade", flush=True)
    Lb = pd.DataFrame(out)
    Lb["session"] = wf.session_label(Lb.t_entry)
    Lb["year"] = pd.DatetimeIndex(Lb.session).year
    Lb["hour"] = pd.DatetimeIndex(Lb.t_entry).hour
    blk = np.full(len(Lb), "", object)
    for k, hs in TOD_BLOCKS.items():
        blk[np.isin(Lb.hour.to_numpy(), hs)] = k
    Lb["tod_block"] = blk
    return rows, Lb


def events_path(sym, tf):
    return os.path.join(OUT, f"v2_events_{sym}_{tf}.parquet")


def trend_path(sym, tf):
    return os.path.join(OUT, f"v2_trend_{sym}_{tf}.parquet")


def build(sym, B, F, m1):
    t0 = time.time()
    E, pool = union_events(F, B, sym)
    print(f"  {sym} {B}m: {len(E):,} events, {len(pool):,} trend-pool rows ({time.time() - t0:.0f}s)", flush=True)
    E["src"] = "event"
    pool["src"] = "trend"
    allr = pd.concat([E[["t", "i", "d", "stop", "src"]], pool], ignore_index=True)
    allr["key"] = np.arange(len(allr))
    rows, Lb = label(sym, B, F, allr, m1)
    lab = pd.concat([rows, Lb], axis=1)
    ev = lab[lab.src == "event"]
    Ek = E.iloc[ev.key.to_numpy()].reset_index(drop=True)          # key = position in E (events come first)
    if not (np.array_equal(Ek.i.to_numpy(), ev.i.to_numpy()) and np.array_equal(Ek.d.to_numpy(), ev.d.to_numpy())):
        raise RuntimeError("event rows misaligned")
    X = build_features(F, B, Ek, sym)
    keep_meta = ["t", "i", "d", "stop", "stop_src", *FLAGS, "n_rules", "in_trend", "event_wait"]
    labc = [c for c in Lb.columns]
    evl = ev.reset_index(drop=True)
    out = pd.concat([Ek[keep_meta].reset_index(drop=True), X.reset_index(drop=True), evl[labc]], axis=1)
    out.insert(0, "market", sym)
    out.insert(1, "tf", B)
    out.to_parquet(events_path(sym, B), compression="zstd")
    pl = lab[lab.src == "trend"].drop(columns=["src", "key"]).reset_index(drop=True)
    pl = pl.drop(columns=[c for c in pl.columns if c.startswith("R_") or c.startswith("kind_")])
    pl.insert(0, "market", sym)
    pl.insert(1, "tf", B)
    pl.to_parquet(trend_path(sym, B), compression="zstd")
    print(f"  {sym} {B}m saved: {len(out):,} events x {out.shape[1]} cols, {len(pl):,} pool rows "
          f"({time.time() - t0:.0f}s)", flush=True)
    return out, pl


# ------------------------------------------------------------------------------------------------ checks
def evidence_check(F, B, n=300, seed=1):
    """Independent scalar re-computation of the 7 evidence kinds at random base bars. Returns mismatch count."""
    rng = np.random.default_rng(seed)
    f = F[B]
    b, ctx, P = f["b"], f["ctx"], f["P"]
    types = evidence_types(F, B)
    rev = [c for c in fe.FAMILIES["reversal"] if c in P.columns]
    b60, c60 = F[60]["b"], F[60]["ctx"]
    T5 = F[5]["T"]
    T5 = T5[T5.rule != "trend_all"]
    bad = 0
    for j in rng.choice(np.arange(60, len(b)), n, replace=False):
        t = b.index[j]
        inst = b.inst.iloc[j]
        close_t = t + pd.Timedelta(minutes=B)
        m, m0 = ctx.mom14.iloc[j], ctx.mom14.iloc[j - 1] if b.run.iloc[j - 1] == b.run.iloc[j] else np.nan
        # 60-min: latest bar of the same contract closed by close_t
        h = np.flatnonzero((b60.inst.to_numpy() == inst) & ((b60.index + pd.Timedelta(minutes=60)) <= close_t))
        tr60 = np.nan
        if len(h):
            q = h[-1]
            e8, e20, e50 = c60.ema8.iloc[q], c60.ema20.iloc[q], c60.ema50.iloc[q]
            same5 = q >= 5 and b60.run.iloc[q - 5] == b60.run.iloc[q]
            e50_5 = c60.ema50.iloc[q - 5] if same5 else np.nan
            if np.isfinite(e50) and np.isfinite(e50_5) and np.isfinite(e8):
                tr60 = 1 if (e8 > e20 > e50 and e50 > e50_5) else (-1 if (e8 < e20 < e50 and e50 < e50_5) else 0)
        in_bar = (T5.t >= t) & (T5.t < close_t)
        s5 = T5[in_bar]
        s5 = s5[F[5]["b"].inst.to_numpy()[s5.i.to_numpy()] == inst]
        C, E20, E8 = b.C.iloc[j], ctx.ema20.iloc[j], ctx.ema8.iloc[j]
        for d in (1, -1):
            exp = [bool((P[rev].iloc[j] == -d).any()),
                   bool(np.isfinite(m) and np.isfinite(m0) and d * (m - m0) < 0),
                   bool(d * (C - E20) < 0), bool(d * (E8 - E20) < 0),
                   bool((C < ctx.swing_lo.iloc[j]) if d > 0 else (C > ctx.swing_hi.iloc[j])),
                   bool(np.isfinite(tr60) and tr60 != d),
                   bool((s5.d == -d).any())]
            bad += int((np.array(exp) != types[d][j]).sum())
    return bad


def hand_check(sym, B, F, m1, ev, n=50, seed=7, exits=("hold", "ema_cross", "opp2_2b")):
    """Re-walk n random event trades per exit minute by minute from the raw 1-minute bars (ema50_check.hand_walk:
    its 'cross' branch takes any per-bar exit arrays)."""
    import ema50_check as ec                                          # noqa: PLC0415
    spec = sg.SPEC[sym]
    b = F[B]["b"]
    rules = exit_rules(F, B)
    rng = np.random.default_rng(seed)
    rows = []
    for x in exits:
        rx = rules[x][2]
        for k in rng.choice(len(ev), size=min(n, len(ev)), replace=False):
            r = ev.iloc[k]
            p, why = ec.hand_walk(r, m1, b, B, spec["tick"], spec["usd"], spec["cost"],
                                  "hold" if rx is None else "cross", rx)
            rows.append(dict(market=sym, tf=B, exit=x, t=r.t, d=int(r.d), stop=r.stop, label_pnl=r[f"pnl_{x}"],
                             hand_pnl=p, hand_kind=why, label_kind=int(r[f"kind_{x}"]),
                             bars=int(r[f"bars_{x}"])))
    H = pd.DataFrame(rows)
    H["diff"] = (H.label_pnl - H.hand_pnl).abs()
    return H


def truncation_check(sym, B, start, days=40, cuts=3, seed=0):
    """Cut the 1-minute data after a random minute T (partial higher-timeframe bars included), rebuild everything:
    events and features of signal bars before the cut's last bar must not change. Returns mismatch count."""
    import research_lib as rl                                         # noqa: PLC0415
    full = rl.bars_1m(sym)
    lo = full.index.searchsorted(pd.Timestamp(start, tz="America/New_York"))
    hi = full.index.searchsorted(pd.Timestamp(start, tz="America/New_York") + pd.Timedelta(days=days))
    sl = full.iloc[lo:hi]
    orig = rl.bars_1m
    rng = np.random.default_rng(seed)

    def run(m):
        sg.rl.bars_1m = lambda s: m
        try:
            Fx = load_frames(sym)
            E, _ = union_events(Fx, B, sym)
            X = build_features(Fx, B, E, sym)
        finally:
            sg.rl.bars_1m = orig
        return Fx, pd.concat([E[["t", "i", "d", "stop", *FLAGS]], X], axis=1)

    _, A = run(sl)
    bad = 0
    n_cmp = 0
    for _ in range(cuts):
        cut = sl.index[int(rng.integers(len(sl) // 2, len(sl) - 10))]
        Fx, Bc = run(sl.loc[sl.index <= cut])
        last_start = Fx[B]["b"].index[-1]
        a = A[A.t < last_start].reset_index(drop=True)
        c = Bc[Bc.t < last_start].reset_index(drop=True)
        if len(a) != len(c):
            bad += abs(len(a) - len(c)) + 1
            continue
        for col in a.columns:
            x, y = a[col].to_numpy(), c[col].to_numpy()
            if x.dtype.kind in "fc":
                bad += int((~((x == y) | (np.isnan(x) & np.isnan(y)) | (np.abs(x - y) <= 1e-5 * np.abs(x)))).sum())
            else:
                bad += int((x != y).sum())
        n_cmp += len(a)
    return bad, n_cmp


# ------------------------------------------------------------------------------------------------ main
def main(markets, tfs, check=False):
    os.makedirs(OUT, exist_ok=True)
    for sym in markets:
        t0 = time.time()
        F = load_frames(sym)
        m1 = lb.load_1m(sym)
        m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
        print(f"{sym}: frames + 1-minute loaded ({time.time() - t0:.0f}s)", flush=True)
        for B in tfs:
            if check:
                ev = pd.read_parquet(events_path(sym, B))
                bad = evidence_check(F, B)
                print(f"  {sym} {B}m evidence check: {bad} mismatches", flush=True)
                H = hand_check(sym, B, F, m1, ev)
                H.to_csv(os.path.join(OUT, f"v2_handcheck_{sym}_{B}.csv"), index=False)
                print(f"  {sym} {B}m hand check: {len(H)} trades, max |diff| ${H['diff'].max():.6f}, "
                      f"{int((H['diff'] > 1e-6).sum())} differ", flush=True)
                for k, start in enumerate(("2014-05-05", "2023-02-06")):
                    if sym == "YM" and start < "2018":
                        start = "2019-09-09"
                    bad, n = truncation_check(sym, B, start, days=40, cuts=3, seed=B + k)
                    print(f"  {sym} {B}m truncation check from {start}: {bad} mismatches over {n} rows", flush=True)
            else:
                build(sym, B, F, m1)
            gc.collect()
        del F, m1
        fe.clear_cache()
        gc.collect()
        print(f"{sym} done ({time.time() - t0:.0f}s)", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("markets", nargs="*", default=["NQ", "ES", "YM"])
    ap.add_argument("--tf", default="60,15,5")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    main(a.markets, [int(x) for x in a.tf.split(",")], a.check)
