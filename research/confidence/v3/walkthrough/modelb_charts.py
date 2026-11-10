"""Model B (15|hold|M3|cls|exp) example charts + decision cards + the opposite-evidence exit chart.
Examples: kept OOS trades from v2/out/oos_M3_cls_hold_15m_exp.parquet (pre-holdout), picked at random
(numpy default_rng(20261109)) among trades whose R is between the 25th and 75th percentile of their group
(MES winners, MES losers, MNQ winners), i.e. typical, not best/worst. All inputs come from v2/out/v2_events_{sym}_15.parquet;
chart values are recomputed from research/confidence/v3/data/bars_{sym}_{5,15,60}.parquet and compared."""
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from wt_common import *  # noqa
import chart_style as cs
import signals as sg
import trigger_scan as ts_
import features as fe

ROOT = os.path.join(HERE, "..", "..")
OOS = os.path.join(ROOT, "v2", "out", "oos_M3_cls_hold_15m_exp.parquet")
FOLDS = os.path.join(ROOT, "v2", "out", "models_folds.csv")
REV = ["hammer", "inverted_hammer", "hanging_man", "shooting_star", "dragonfly_doji", "gravestone_doji", "engulfing",
       "harami", "piercing", "dark_cloud", "morning_evening_star", "three_inside", "tweezer", "pin_bar"]
DIRP = [k for k, (kind, _) in sg.PATTERN_RULES.items() if kind == "dir"]

# ---------------------------------------------------------------------------------------------- plain-word inputs
TFN = {"m5": "5-min", "m15": "15-min", "m60": "60-min"}
PER_TF = [("trend", "trend (EMA8>20>50 and EMA50 rising)", "s"), ("s820", "EMA8 minus EMA20", "s"),
          ("s2050", "EMA20 minus EMA50", "s"), ("c20", "close minus EMA20", "s"), ("c50", "close minus EMA50", "s"),
          ("mom", "Momentum - 100 (14-bar % change)", "s"), ("mslope3", "Momentum change over 3 bars", "s"),
          ("struct", "swing structure (HH+HL = +1)", "s"), ("sw_room", "room to next swing ahead", "room"),
          ("sw_cushion", "distance to last swing behind", "info")]
OTHER = [("day_room", "room to high/low of day (R20)", "room"), ("day_cushion", "distance to other end of day range", "info"),
         ("day_pos", "place in day range (1 = at trade-side extreme)", "info"), ("day_range_R", "day range so far (R20)", "info"),
         ("vwap_side", "side of session VWAP (+1 = trade side)", "s"), ("vwap_dist", "distance from VWAP (R20)", "s"),
         ("gap", "18:00 reopen gap, with trade (R20)", "s"), ("prior_range", "yesterday's range (R20)", "info"),
         ("pat_with3", "candle patterns WITH trade, last 3 bars", "s"),
         ("pat_against3", "candle patterns AGAINST trade, last 3 bars", "neg"),
         ("rev_at_low", "reversal candle at the pullback low", "s"), ("pb_depth", "pullback depth (SH-PL)/(SH-SL)", "info"),
         ("pb_bars", "pullback length (bars)", "info"), ("pb_div", "hidden Momentum divergence", "s"),
         ("pb_momflip", "Momentum crossed 100 in pullback", "info"),
         ("min_since_18", "minutes since 18:00 at entry", "info"), ("tod_18_22", "time block 18-22h", "info"),
         ("tod_23_02", "time block 23-02h", "info"), ("tod_03_08", "time block 03-08h", "info"),
         ("tod_09_11", "time block 09-11h", "info"), ("tod_12_16", "time block 12-16h", "info"),
         ("dow", "weekday (0 = Monday)", "info"), ("risk_R20", "stop distance from close (R20)", "info"),
         ("cost_R", "round-trip cost / stop distance", "neg"), ("cost_bar", "round-trip cost / R20", "neg"),
         ("n_tf_agree", "how many of 5/15/60 trends agree", "s"), ("mtf_trend60", "60-min trend agrees (0/1)", "s"),
         ("mtf_trig5", "5-min trigger same way, last 6 bars", "s"), ("mtf_mom5", "5-min Momentum up & EMA8>20", "s"),
         ("mtf_score", "sum of the 3 above", "s"), ("pb", "rule: swing pullback detector", "flag"),
         ("ema8_pb", "rule: EMA8 pullback", "flag"), ("ema20_pb", "rule: EMA20 pullback", "flag"),
         ("ema50_pb", "rule: EMA50 pullback", "flag"), ("mom_turn", "rule: Momentum turn", "flag"),
         ("pb_break", "rule: pullback-bar break", "flag"), ("n_rules", "number of rules that fired", "s"),
         ("mkt_ES", "market is MES (0/1)", "info"), ("mkt_YM", "market is MYM (0/1)", "info")]
MONO_UP = {"m5_trend", "m15_trend", "m60_trend", "m5_struct", "m15_struct", "m60_struct", "m5_mslope3", "m15_mslope3",
           "m60_mslope3", "n_tf_agree", "mtf_trend60", "mtf_trig5", "mtf_mom5", "mtf_score", "pat_with3", "rev_at_low",
           "vwap_side", "pb_div", "n_rules"}
MONO_DN = {"pat_against3", "cost_R", "cost_bar"}


def inputs_table(row, sym):
    out = []
    for p, pn in TFN.items():
        for k, lab, kind in PER_TF:
            out.append((f"{p}_{k}", f"{pn} {lab}" + (" (R20)" if k in ("s820", "s2050", "c20", "c50", "sw_room", "sw_cushion") else ""), kind))
    out += OTHER
    rows = []
    for k, lab, kind in out:
        if k == "mkt_ES":
            v = float(sym == "ES")
        elif k == "mkt_YM":
            v = float(sym == "YM")
        else:
            v = row.get(k, np.nan)
            v = float(v) if v is not None and pd.notna(v) else np.nan
        if not np.isfinite(v):
            rd = "no value (NaN)"
        elif kind == "s":
            rd = "agrees" if v > 0.05 else ("against" if v < -0.05 else "neutral")
        elif kind == "neg":
            rd = "against" if v > 0 else "neutral"
        elif kind == "room":
            rd = "agrees (room to run)" if v > 0.25 else "against (at/through it)"
        elif kind == "flag":
            rd = "fired" if v > 0 else "-"
        else:
            rd = "info"
        mono = "can only raise score" if k in MONO_UP else ("can only lower score" if k in MONO_DN else "free shape")
        rows.append(dict(key=k, plain=lab, value=v, read=rd, model_constraint=mono, source=f"v2_events_{sym}_15.parquet:{k}"))
    return rows


def rd_color(rd):
    return cs.GOOD if rd.startswith("agree") or rd == "fired" else (cs.BAD if rd.startswith("against") else cs.TXT2)


def fmtv(v):
    if not np.isfinite(v):
        return "NaN"
    return f"{v:+.2f}" if abs(v) < 100 else f"{v:.0f}"


# ---------------------------------------------------------------------------------------------- data per example
def load_event(sym, t, d):
    ev = pd.read_parquet(os.path.join(ROOT, "v2", "out", f"v2_events_{sym}_15.parquet"), filters=[("t", "==", t)])
    ev = ev[ev.d == d]
    assert len(ev) == 1, (sym, t, d, len(ev))
    return ev.iloc[0]


def trend_b(B):
    e8, e20, e50 = B.ema8, B.ema20, B.ema50
    e50_5 = e50.shift(5).where(B.run.eq(B.run.shift(5)))
    up = (e8 > e20) & (e20 > e50) & (e50 > e50_5)
    dn = (e8 < e20) & (e20 < e50) & (e50 < e50_5)
    return pd.Series(np.select([up, dn], [1, -1], 0), index=B.index).where(e50_5.notna())


def prep(sym, t, d):
    tick = TICK[sym]
    b = bars(sym, 15)
    i = b.index.get_loc(t)
    run = b.run.iloc[i]
    s0 = max(i - 2500, int(np.flatnonzero(b.run.to_numpy() == run)[0]))
    sess = b.sess.iloc[i]
    send = int(np.flatnonzero((b.sess.to_numpy() == sess) & (b.run.to_numpy() == run))[-1])
    bs = b.iloc[s0:send + 1].copy()
    ii = i - s0
    ctx = sg.context(bs, tick=tick)
    pats = sg.patterns(bs, ctx, tick=tick)
    R = fe.r20(bs, tick)
    return dict(b=bs, i=ii, ctx=ctx, pats=pats, R=np.asarray(R, float), tick=tick)


def fired_triggers(P, sym, d):
    try:
        ev = ts_.detect(P["b"], P["ctx"], P["tick"], 15)
        ev = ev[(ev.i == P["i"]) & (ev.d == d) & (ev.rule != "trend_all")]
        return sorted(ev.rule.tolist()), ev
    except Exception as e:  # noqa
        return [f"recompute failed: {e}"], None


def exit_walk(P, sym, d, entry, stop):
    b = P["b"]; i = P["i"]; tick = P["tick"]
    m = (b.index.hour * 60 + b.index.minute)
    sess = b.sess.iloc[i]
    same = np.flatnonzero((b.sess.to_numpy() == sess) & (m.to_numpy() <= 16 * 60 + 30) & (np.arange(len(b)) > i))
    F = int(same[-1])
    for k in range(i + 1, F + 1):
        lo, hi, o = b.L.iloc[k], b.H.iloc[k], b.O.iloc[k]
        if (d > 0 and lo <= stop) or (d < 0 and hi >= stop):
            px = (min(o, stop) - tick) if d > 0 else (max(o, stop) + tick)
            return k, px, "stop (checked on 15-min bars here; v2 walks 1-minute bars)", F
    return F, b.C.iloc[F], "time exit at close of 16:30-16:45 bar (Lucid flat 16:45)", F


# ---------------------------------------------------------------------------------------------- the chart
def chart(name, sym, t, d, oos_row, thr, year_q):
    row = load_event(sym, t, d)
    P = prep(sym, t, d)
    b, i, ctx, pats, R = P["b"], P["i"], P["ctx"], P["pats"], P["R"]
    tick, usd = P["tick"], USD[sym]
    rec = {}
    disc = []
    # ---- recompute
    Rr = R[i]
    rec["R20"] = (Rr, row.R20)
    lo5 = b.L.iloc[i - 4:i + 1].min(); hi5 = b.H.iloc[i - 4:i + 1].max(); Ci = b.C.iloc[i]
    stop_rc = min(lo5 - tick, Ci - Rr) if d > 0 else max(hi5 + tick, Ci + Rr)
    rec["stop"] = (stop_rc, row.stop)
    entry_rc = b.O.iloc[i + 1]
    rec["entry"] = (entry_rc, row.entry)
    rec["m15_c20"] = (d * (Ci - b.ema20.iloc[i]) / Rr, row.m15_c20)
    rec["m15_c50"] = (d * (Ci - b.ema50.iloc[i]) / Rr, row.m15_c50)
    rec["m15_mom"] = (d * (b.mom14.iloc[i] - 100), row.m15_mom)
    rec["vwap_dist"] = (d * (Ci - b.vwap.iloc[i]) / Rr, row.vwap_dist)
    sess_mask = b.sess.to_numpy() == b.sess.iloc[i]
    hod = b.H.where(sess_mask).cummax(); lod = b.L.where(sess_mask).cummin()
    rec["day_room"] = (((hod.iloc[i] - Ci) if d > 0 else (Ci - lod.iloc[i])) / Rr, row.day_room)
    tb = trend_b(b)
    rec["m15_trend"] = (d * tb.iloc[i], row.m15_trend)
    swl, swh = ctx.swing_lo.iloc[i], ctx.swing_hi.iloc[i]
    rec["m15_sw_room"] = (((swh - Ci) if d > 0 else (Ci - swl)) / Rr, row.m15_sw_room)
    rec["m15_sw_cushion"] = (((Ci - swl) if d > 0 else (swh - Ci)) / Rr, row.m15_sw_cushion)
    trig, _ = fired_triggers(P, sym, d)
    flags = [r for r in ["pb", "ema8_pb", "ema20_pb", "ema50_pb", "mom_turn", "pb_break"] if row[r] == 1]
    rec["rules_fired"] = (",".join(trig), ",".join(flags))
    xk, xpx, why, F = exit_walk(P, sym, d, row.entry, row.stop)
    pnl_rc = d * (xpx - row.entry) * usd - COST[sym]
    rec["pnl_usd"] = (pnl_rc, oos_row.pnl_usd)
    for k, (a, bb) in rec.items():
        if isinstance(a, str):
            if set(a.split(",")) != set(bb.split(",")):
                disc.append(f"{k}: recomputed {a} vs stored {bb}")
        elif not (np.isfinite(a) and np.isfinite(bb) and abs(a - bb) <= max(1e-3, 0.02 * abs(bb))):
            disc.append(f"{k}: recomputed {a:.4f} vs stored {bb:.4f}")
    # ---- other-timeframe snapshot at the signal close
    tclose = t + pd.Timedelta(minutes=15)
    snaps = {}
    for tf, nb in ((5, 40), (60, 30)):
        bt = bars(sym, tf)
        bt = bt[(bt.run == b.run.iloc[i])]
        cl = bt.index + pd.Timedelta(minutes=tf)
        j = int(np.flatnonzero(cl <= tclose)[-1])
        snaps[tf] = (bt.iloc[max(0, j - nb + 1):j + 1].copy(), trend_b(bt.iloc[max(0, j - 200):j + 1]).iloc[-1])
        rec[f"m{tf}_trend"] = (d * snaps[tf][1], row[f"m{tf}_trend"])
        a_, b_ = rec[f"m{tf}_trend"][0], row[f"m{tf}_trend"]
        if not ((np.isnan(a_) and np.isnan(b_)) or a_ == b_):
            disc.append(f"m{tf}_trend: recomputed {rec[f'm{tf}_trend'][0]} vs stored {row[f'm{tf}_trend']}")

    # ---- figure
    w0 = max(0, i - 40); w1 = min(len(b) - 1, F + 1)
    B = b.iloc[w0:w1 + 1]
    off = w0
    fig = plt.figure(figsize=(W, H), facecolor=cs.BG)
    gs = fig.add_gridspec(3, 2, width_ratios=[3.05, 1.25], height_ratios=[1.0, 1.0, 1.15], wspace=0.12, hspace=0.2,
                          left=0.03, right=0.955, top=0.9, bottom=0.08)
    gl = gs[:, 0].subgridspec(2, 1, height_ratios=[4.2, 1.2], hspace=0.04)
    ax = fig.add_subplot(gl[0]); axm = fig.add_subplot(gl[1], sharex=ax)
    for a in (ax, axm):
        style_ax(a)
    x = candles(ax, B)
    emas(ax, x, B)
    sb = B.sess.to_numpy(); br = np.flatnonzero(sb[1:] != sb[:-1]) + 1
    ax.plot(np.insert(x.astype(float), br, np.nan), np.insert(B.vwap.to_numpy(), br, np.nan), color=cs.VWAP_COL,
            lw=1.6, label="VWAP (from 18:00)")
    for j in br:
        for a in (ax, axm):
            a.axvline(j - 0.5, color="#666666", lw=1.0, ls=(0, (2, 3)))
        ax.text(j - 0.4, 0.99, " 18:00 new session", transform=ax.get_xaxis_transform(), color=cs.TXT2, fontsize=11, va="top")
    hh = hod.iloc[w0:w1 + 1].to_numpy(); ll = lod.iloc[w0:w1 + 1].to_numpy()
    ax.step(x, hh, where="mid", color="#ffffff", lw=1.0, alpha=0.55, ls=(0, (1, 2)), label="high / low of day so far")
    ax.step(x, ll, where="mid", color="#ffffff", lw=1.0, alpha=0.55, ls=(0, (1, 2)))
    lo_rng, hi_rng = np.nanmin(B.L), np.nanmax(B.H)
    rr = hi_rng - lo_rng
    # time-of-day block shading
    blocks = {"tod_18_22": (18, 22), "tod_23_02": (23, 2), "tod_03_08": (3, 8), "tod_09_11": (9, 11), "tod_12_16": (12, 16)}
    blk = [k for k in blocks if row[k] == 1]
    if blk:
        h0, h1 = blocks[blk[0]]
        hc = ((B.index + pd.Timedelta(minutes=15)).hour).to_numpy()
        inb = (hc >= h0) & (hc <= h1) if h0 <= h1 else ((hc >= h0) | (hc <= h1))
        if inb.any():
            xs = np.flatnonzero(inb)
            ax.axvspan(xs[0] - 0.5, xs[-1] + 0.5, color="#3a3a10", alpha=0.35, zorder=0)
            ax.text(xs[0] - 0.4, 0.035, f"time block {h0:02d}-{h1:02d}h (by bar close hour)", transform=ax.get_xaxis_transform(),
                    color="#e8e08a", fontsize=11.5)
    xi = i - off
    # swing points (3-bar fractals) with their confirmation lag
    lo_p, hi_p = sg.pivots(b, 3)
    for p in np.flatnonzero(lo_p[w0:min(w1, i) + 1]) + w0:
        if p + 3 > i:
            continue
        px = p - off
        ax.plot(px, b.L.iloc[p], marker="^", color="#7fd6ff", ms=10, zorder=6, ls="none")
        ax.plot([px, px + 3], [b.L.iloc[p] - rr * 0.03] * 2, color="#7fd6ff", lw=1.2, ls=":")
        ax.plot(px + 3, b.L.iloc[p] - rr * 0.03, marker="|", color="#7fd6ff", ms=12, mew=2)
    for p in np.flatnonzero(hi_p[w0:min(w1, i) + 1]) + w0:
        if p + 3 > i:
            continue
        px = p - off
        ax.plot(px, b.H.iloc[p], marker="v", color="#ffb3f5", ms=10, zorder=6, ls="none")
        ax.plot([px, px + 3], [b.H.iloc[p] + rr * 0.03] * 2, color="#ffb3f5", lw=1.2, ls=":")
        ax.plot(px + 3, b.H.iloc[p] + rr * 0.03, marker="|", color="#ffb3f5", ms=12, mew=2)
    ax.plot([], [], marker="^", color="#7fd6ff", ls=":", label="swing low  ...| = known 3 bars later")
    ax.plot([], [], marker="v", color="#ffb3f5", ls=":", label="swing high ...| = known 3 bars later")
    # the swings the inputs read
    for lvl, nm, colr, ab in ((swh, "last confirmed swing HIGH", "#ffb3f5", True), (swl, "last confirmed swing LOW", "#7fd6ff", False)):
        if np.isfinite(lvl):
            ax.hlines(lvl, xi - 8, xi + 0.5, color=colr, lw=1.6, ls="--")
            dist = (lvl - Ci) / Rr
            tag(ax, xi - 8, lvl, f"{nm} {cs.fp(sym, lvl)} ({dist:+.1f} R20 from close)", colr, dy=12 if ab else -12, fs=11, ha="left")
    # stop window + R20 ruler
    ax.axvspan(xi - 4.5, xi + 0.5, color="#202050", alpha=0.35, zorder=0)
    ax.text(xi - 4.4, 0.08, "5-bar stop window", transform=ax.get_xaxis_transform(), color="#aab0ff", fontsize=11)
    ax.annotate("", (xi + 0.75, Ci), (xi + 0.75, Ci - d * Rr), arrowprops=dict(arrowstyle="<->", color="#ffffff", lw=1.4))
    ax.text(xi + 0.95, Ci - d * Rr / 2, f"1 R20\n{Rr:.2f}", color="#ffffff", fontsize=10.5, va="center")
    # signal bar
    cs.ring(ax, xi, xi, b.L.iloc[i], b.H.iloc[i], cs.EXITC, rr)
    ttxt = " + ".join(flags) if flags else "?"
    tag(ax, xi, b.H.iloc[i] if d > 0 else b.L.iloc[i],
        f"SIGNAL bar {t:%H:%M}-{tclose:%H:%M}\n{'LONG' if d > 0 else 'SHORT'}: {ttxt}", cs.EXITC,
        dy=60 if d > 0 else -60, fs=12)
    # entry / stop / exit
    xe = xi + 1
    xx = xk - off
    ax.hlines(row.stop, xe - 0.4, xx + 0.4, color=cs.BAD, lw=2.0)
    tag(ax, xx, row.stop, f"STOP {cs.fp(sym, row.stop)} (risk ${row.risk_usd:.0f})", cs.BAD, dy=-22 if d > 0 else 22, fs=11.5, ha="right")
    ax.plot(xe, row.entry, marker=">", color=cs.HILITE, ms=13, zorder=10)
    tag(ax, xe, row.entry, f"ENTRY {cs.fp(sym, row.entry)}\nnext bar open {row.t_entry:%H:%M}", cs.HILITE,
        dy=-55 if d > 0 else 55, fs=11.5, dx=35)
    ax.plot(xx, xpx, marker="X", color="#ffffff", ms=13, zorder=10)
    pc = cs.GOOD if oos_row.pnl_usd > 0 else cs.BAD
    tag(ax, xx, xpx, f"EXIT {cs.fp(sym, xpx)}\n{why.split('(')[0].strip()}\nP&L ${oos_row.pnl_usd:+.2f} after ${COST[sym]:.2f} costs",
        pc, dy=50 if d > 0 else -50, fs=11.5, ha="right", dx=-10)
    # candle patterns, last 3 bars
    ptxt = []
    for k in range(i - 2, i + 1):
        for pn in DIRP:
            v = int(pats[pn].iloc[k])
            if v:
                ptxt.append(f"{b.index[k]:%H:%M} {cs.pname(pn, v)} {'WITH' if v == d else 'AGAINST'}")
    ax.text(0.005, 0.015, "Candle patterns, last 3 bars:\n" + ("\n".join(ptxt[:7]) if ptxt else "none"),
            transform=ax.transAxes, color=cs.TXT, fontsize=10.5, va="bottom",
            bbox=dict(fc="#0b0b0b", ec="#333333", boxstyle="round,pad=0.3"))
    ax.set_ylim(lo_rng - rr * 0.18, hi_rng + rr * 0.22)
    ax.set_xlim(-0.8, len(B) + 3)
    ax.tick_params(labelbottom=False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: cs.fp(sym, v)))
    legend(ax, loc="upper left", ncol=3, fs=10.5)
    # momentum
    mom = B.mom14.to_numpy()
    axm.plot(x, mom, color=cs.MOM_COL, lw=1.7)
    axm.axhline(100, color="#777777", lw=1.0, ls=(0, (3, 3)))
    axm.plot(xi, mom[xi], "o", color=cs.EXITC, ms=8)
    sl = "rising" if mom[xi] > mom[xi - 1] else "falling"
    axm.text(0.005, 0.93, f"Momentum(14) = 100 x C / C[14]   at signal {mom[xi]:.2f} ({sl}; 3-bar change {mom[xi]-mom[xi-3]:+.2f})",
             transform=axm.transAxes, color=cs.TXT, fontsize=11.5, va="top")
    time_ticks(axm, B.index)
    # insets
    for r_, tf in ((0, 5), (1, 60)):
        a = fig.add_subplot(gs[r_, 1]); style_ax(a)
        Bt, tr = snaps[tf]
        xt = candles(a, Bt, lw=1.0); emas(a, xt, Bt, lw_scale=0.8, label=False)
        a.plot(xt, Bt.vwap.to_numpy(), color=cs.VWAP_COL, lw=1.0)
        a.tick_params(labelbottom=False, labelsize=9)
        a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        trw = {1: "UP", -1: "DOWN", 0: "none"}.get(int(tr) if np.isfinite(tr) else 0)
        ag = d * tr
        colr = cs.GOOD if ag > 0 else (cs.BAD if ag < 0 else cs.TXT2)
        a.set_title(f"{tf}-min at signal close: trend {trw} -> {'agrees' if ag > 0 else ('AGAINST' if ag < 0 else 'neutral')}",
                    color=colr, fontsize=12, loc="left", pad=3)
        a.text(0.01, 0.03, f"last bar {Bt.index[-1]:%H:%M}-{Bt.index[-1] + pd.Timedelta(minutes=tf):%H:%M}", transform=a.transAxes,
               color=cs.TXT2, fontsize=10)
    # card
    ac = fig.add_subplot(gs[2, 1]); ac.set_facecolor("#0b0b0b"); ac.set_xticks([]); ac.set_yticks([])
    for sp in ac.spines.values():
        sp.set_color("#333333")
    tbl = inputs_table(row, sym)
    agree = sum(r["read"].startswith("agree") for r in tbl); against = sum(r["read"].startswith("against") for r in tbl)
    keyk = ["m60_trend", "m15_trend", "m5_trend", "vwap_side", "day_room", "m15_sw_room", "m15_struct", "pat_with3",
            "pat_against3", "rev_at_low", "mtf_trig5", "cost_R"]
    lines = [(f"MODEL SCORE {oos_row.score:.3f}  vs  {t.year} threshold {thr:.3f}", cs.HILITE),
             (f"-> KEPT (>= threshold = top {year_q:.0%} of training)", cs.HILITE),
             (f"69 inputs: {agree} agree, {against} against (full list: card image)", cs.TXT)]
    for k in keyk:
        r = next(z for z in tbl if z["key"] == k)
        lines.append((f"{r['plain'][:31]:<31} {fmtv(r['value']):>6} {r['read'].split(' ')[0]}", rd_color(r["read"])))
    lines.append((f"P&L {oos_row.pnl_usd:+.2f} $ per micro = {oos_row.R:+.2f} R (net)", pc))
    for n_, (s_, c_) in enumerate(lines):
        ac.text(0.02, 0.965 - n_ * 0.064, s_, transform=ac.transAxes, color=c_, fontsize=9.8, va="top", family="DejaVu Sans Mono")
    fig.suptitle(f"MODEL B example ({name.replace('_', ' ')}): {MICRO[sym]} 15-min, {t:%a %Y-%m-%d}, "
                 f"{'LONG' if d > 0 else 'SHORT'}  ->  {oos_row.pnl_usd:+.2f} $ per micro",
                 color=cs.TXT, fontsize=17, x=0.015, ha="left", y=0.985)
    fig.text(0.015, 0.935, "Bar times = bar START (NinjaTrader shows the END: add 15 min). VWAP & high/low of day start at 18:00 ET. "
             "Every value is read at the signal bar's CLOSE; entry is the next bar's open.", color=cs.TXT2, fontsize=11.5)
    p1 = save(fig, f"modelB_{name}.png")
    # full card image
    fig2 = plt.figure(figsize=(W, 1300 / DPI), facecolor=cs.BG)
    fig2.text(0.01, 0.985, f"DECISION CARD  {MICRO[sym]} {t:%Y-%m-%d} signal bar {t:%H:%M}-{tclose:%H:%M} "
              f"{'LONG' if d > 0 else 'SHORT'}: all 69 model inputs at the signal close (+ = good for the trade)",
              color=cs.TXT, fontsize=15, va="top")
    fig2.text(0.01, 0.955, "green = reads as agreeing, red = against, grey = neutral / info. 'can only raise/lower score' = monotone "
              "constraint in M3 (models.py:132-135). Plain reading, NOT the model's learned weight.", color=cs.TXT2, fontsize=11.5, va="top")
    per = 24
    for c_ in range(3):
        for n_, r in enumerate(tbl[c_ * per:(c_ + 1) * per]):
            y = 0.92 - n_ * 0.0345
            fig2.text(0.01 + c_ * 0.333, y, f"{r['plain'][:40]}", color=cs.TXT, fontsize=10.8, va="top")
            fig2.text(0.24 + c_ * 0.333, y, fmtv(r["value"]), color=rd_color(r["read"]), fontsize=10.8, va="top",
                      family="DejaVu Sans Mono", ha="right")
            fig2.text(0.245 + c_ * 0.333, y, r["read"].split(" (")[0][:12], color=rd_color(r["read"]), fontsize=10.3, va="top")
    fig2.text(0.01, 0.06, f"Score {oos_row.score:.4f} (M3 tree model fit on years before {t.year}) vs threshold {thr:.4f} -> KEPT.  "
              f"Entry {cs.fp(sym, row.entry)}, stop {cs.fp(sym, row.stop)}, exit {cs.fp(sym, xpx)} ({why.split('(')[0].strip()}).  "
              f"Net P&L {oos_row.pnl_usd:+.2f} $ per micro after ${COST[sym]:.2f} round-trip cost.", color=cs.HILITE, fontsize=12.5)
    p2 = save(fig2, f"modelB_{name}_card.png")
    caption = (f"Model B {MICRO[sym]} 15-min {'long' if d > 0 else 'short'} on {t:%Y-%m-%d}. Signal bar {t:%H:%M}-{tclose:%H:%M}: "
               f"rule(s) {ttxt}. Score {oos_row.score:.3f} >= {t.year} threshold {thr:.3f}, so kept. Entry at the {row.t_entry:%H:%M} "
               f"open {cs.fp(sym, row.entry)}, stop {cs.fp(sym, row.stop)}, {why.split('(')[0].strip()} at {cs.fp(sym, xpx)}: "
               f"{oos_row.pnl_usd:+.2f} $ per micro after costs.")
    card(f"modelB_{name}", dict(
        chart=os.path.basename(p1), card_image=os.path.basename(p2), caption=caption,
        how_picked="numpy default_rng(20261109); among kept OOS trades (pre-holdout) of this market and outcome whose R is "
                   "between the group's 25th and 75th percentile; one drawn at random",
        market=MICRO[sym], signal_bar_start=str(t), signal_bar_close=str(tclose), direction=int(d),
        score=float(oos_row.score), threshold=float(thr), keep_share_q=float(year_q),
        score_source="v2/out/oos_M3_cls_hold_15m_exp.parquet:score (copied; model not refit)",
        threshold_source="v2/out/models_folds.csv:threshold (cfg 15|hold|M3|cls|exp, fold %d)" % t.year,
        entry=float(row.entry), stop=float(row.stop), exit_price=float(xpx), exit_reason=why,
        pnl_usd_stored=float(oos_row.pnl_usd), R_stored=float(oos_row.R), risk_usd=float(row.risk_usd),
        rules_fired_stored=flags, rules_fired_recomputed=trig,
        patterns_last3=ptxt, last_swing_high=float(swh), last_swing_low=float(swl),
        recompute_check={k: dict(recomputed=a if isinstance(a, str) else float(a), stored=bb if isinstance(bb, str) else float(bb))
                         for k, (a, bb) in rec.items()},
        discrepancies=disc or ["none above tolerance (2% or 0.001)"],
        recompute_sources={"R20": "features.py:176-183 on v3 bars", "stop": "trigger_scan.py:78-81", "entry": "labels.py:353",
                           "trend": "v2/dataset.py:110-119", "swings": "signals.py:64-79,106-116", "day_room": "features.py:278-293",
                           "exit": "exit walk on v3 15-min bars (v2 uses 1-minute walk, labels.py:295-334)"},
        inputs=tbl))
    print(name, "disc:", disc)
    return dict(P=P, row=row, F=F, xk=xk, xpx=xpx, oos=oos_row)


# ---------------------------------------------------------------------------------------------- opposite evidence
def opp_chart(sym, t, d, oos_row, src_name):
    row = load_event(sym, t, d)
    P = prep(sym, t, d)
    b, i, ctx, pats = P["b"], P["i"], P["ctx"], P["pats"]
    tick = P["tick"]
    xk, xpx, why, F = exit_walk(P, sym, d, row.entry, row.stop)
    rev_against = np.zeros(len(b), bool)
    for pn in REV:
        rev_against |= pats[pn].to_numpy() == -d
    mom = b.mom14.to_numpy(); dm = mom - np.r_[np.nan, mom[:-1]]
    C = b.C.to_numpy(); e8, e20 = b.ema8.to_numpy(), b.ema20.to_numpy()
    swl, swh = ctx.swing_lo.to_numpy(), ctx.swing_hi.to_numpy()
    b60 = bars(sym, 60); b60 = b60[b60.run == b.run.iloc[i]]
    t60 = trend_b(b60); cl60 = b60.index + pd.Timedelta(minutes=60)
    b5 = bars(sym, 5); b5 = b5[b5.run == b.run.iloc[i]]
    b5 = b5[(b5.index >= b.index[max(0, i - 900)]) & (b5.index <= b.index[F] + pd.Timedelta(minutes=15))]
    ctx5 = sg.context(b5, tick=tick)
    ev5 = ts_.detect(b5, ctx5, tick, 5)
    ev5 = ev5[(ev5.d == -d) & (ev5.rule != "trend_all")]
    t5 = set(b5.index[ev5.i.to_numpy()])
    names = ["1 reversal candle against", "2 Momentum fell (vs prev bar)" if d > 0 else "2 Momentum rose",
             "3 close beyond EMA20 (wrong side)", "4 EMA8 crossed EMA20 (wrong side)", "5 close beyond last swing",
             "6 60-min trend not with trade", "7 5-min trigger the other way"]
    rows = []
    rng_ = list(range(i, F + 1))
    for k in rng_:
        tcl = b.index[k] + pd.Timedelta(minutes=15)
        j = np.flatnonzero(cl60 <= tcl)
        tr60 = t60.iloc[j[-1]] if len(j) else np.nan
        inside = [tt for tt in t5 if b.index[k] <= tt < tcl]
        if d > 0:
            ev = [rev_against[k], dm[k] < 0, C[k] < e20[k], e8[k] < e20[k], C[k] < swl[k], np.isfinite(tr60) and tr60 != 1, len(inside) > 0]
        else:
            ev = [rev_against[k], dm[k] > 0, C[k] > e20[k], e8[k] > e20[k], C[k] > swh[k], np.isfinite(tr60) and tr60 != -1, len(inside) > 0]
        rows.append([bool(v) for v in ev])
    X = np.array(rows)
    c1 = X.sum(1)
    prev = np.vstack([np.zeros((1, 7), bool), X[:-1]]); c2 = (X | prev).sum(1)
    # bars after entry: index 0 is signal bar (counts only via the 2-bar window); checks start at the entry bar
    first = {}
    for N in (3, 4):
        hit = [n for n in range(1, len(rng_)) if c1[n] >= N and rng_[n] < F]
        first[N] = hit[0] if hit else None
    stored = {k: str(row[k]) for k in ["t_exit_opp3_1b", "t_exit_opp4_1b", "t_exit_opp3_2b", "pnl_opp3_1b", "pnl_opp4_1b", "pnl_hold"]}
    # figure
    w0 = i - 12; B = b.iloc[w0:F + 2]; off = w0
    fig = plt.figure(figsize=(W, H), facecolor=cs.BG)
    gs = fig.add_gridspec(2, 1, height_ratios=[2.2, 1.55], hspace=0.06, left=0.20, right=0.94, top=0.9, bottom=0.08)
    ax = fig.add_subplot(gs[0]); style_ax(ax)
    x = candles(ax, B); emas(ax, x, B)
    ax.plot(x, B.vwap.to_numpy(), color=cs.VWAP_COL, lw=1.4, label="VWAP")
    ax.plot(x, ctx.swing_lo.iloc[w0:F + 2].to_numpy() if d > 0 else ctx.swing_hi.iloc[w0:F + 2].to_numpy(), color="#7fd6ff",
            lw=1.2, ls=":", drawstyle="steps-mid", label="last confirmed swing low" if d > 0 else "last confirmed swing high")
    xi = i - off
    ax.plot(xi + 1, row.entry, ">", color=cs.HILITE, ms=13); tag(ax, xi + 1, row.entry, f"ENTRY {row.t_entry:%H:%M}", cs.HILITE, dy=-30)
    ax.hlines(row.stop, xi + 1, F - off, color=cs.BAD, lw=1.8); tag(ax, xi + 2, row.stop, "stop", cs.BAD, dy=-16, fs=11)
    ax.plot(F - off, xpx, "X", color="#ffffff", ms=12)
    tag(ax, F - off, xpx, f"hold exit 16:45\n{oos_row.pnl_usd:+.2f} $", cs.GOOD if oos_row.pnl_usd > 0 else cs.BAD, dy=-45, ha="right")
    colN = {3: "#ffa500", 4: cs.EXITC}
    for N, n in first.items():
        if n is None:
            continue
        k = rng_[n]; xx = k - off
        ax.axvline(xx + 0.5, color=colN[N], lw=1.6, ls="--")
        pxe = b.O.iloc[k + 1]
        pnl = d * (pxe - row.entry) * USD[sym] - COST[sym]
        tag(ax, xx + 1, pxe, f"N={N}: {c1[n]} kinds at {b.index[k] + pd.Timedelta(minutes=15):%H:%M} close\n"
            f"-> exit next open {cs.fp(sym, pxe)} = {pnl:+.2f} $", colN[N], dy=45 if N == 3 else -45, fs=11.5)
    for N, n in first.items():
        if n is None:
            ax.text(0.01, 0.04 if N == 4 else 0.11, f"N={N}: count never reached {N} before the 16:45 bar -> same as hold",
                    transform=ax.transAxes, color=colN[N], fontsize=12.5, fontweight="bold")
    lo_, hi_ = np.nanmin(B.L), np.nanmax(B.H); rr = hi_ - lo_
    ax.set_ylim(lo_ - rr * 0.15, hi_ + rr * 0.25); ax.set_xlim(-0.8, len(B) - 0.2)
    ax.tick_params(labelbottom=False); legend(ax, ncol=5, fs=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: cs.fp(sym, v)))
    ag = fig.add_subplot(gs[1], sharex=ax); ag.set_facecolor(cs.BG)
    for sp in ag.spines.values():
        sp.set_color("#333333")
    for r_ in range(7):
        ag.text(-1.2, r_, names[r_], ha="right", va="center", color=cs.TXT, fontsize=11.5, transform=ag.transData, clip_on=False)
        for n, k in enumerate(rng_):
            xx = k - off
            on = X[n, r_]
            ag.add_patch(plt.Rectangle((xx - 0.42, r_ - 0.4), 0.84, 0.8, color=(cs.BAD if on else "#1a1a1a"), alpha=0.9 if on else 1))
    for n, k in enumerate(rng_):
        xx = k - off
        cc = colN[4] if c1[n] >= 4 else (colN[3] if c1[n] >= 3 else cs.TXT)
        ag.text(xx, 7.1, f"{c1[n]}", ha="center", va="center", color=cc, fontsize=13, fontweight="bold")
    ag.text(-1.2, 7.1, "count this bar (_1b)", ha="right", va="center", color=cs.HILITE, fontsize=12, clip_on=False)
    ag.text(xi, -0.9, "signal\nbar", ha="center", va="top", color=cs.EXITC, fontsize=10.5)
    ag.set_ylim(7.7, -1.6); ag.set_yticks([])
    ag.tick_params(colors=cs.TXT)
    time_ticks(ag, B.index, nt=9, fs=11)
    fig.suptitle(f"OPPOSITE-EVIDENCE EXIT, bar by bar: {MICRO[sym]} 15-min {t:%Y-%m-%d} {'long' if d > 0 else 'short'} "
                 "(Model B itself HOLDS to 16:45)", color=cs.TXT, fontsize=16.5, x=0.01, ha="left", y=0.985)
    fig.text(0.01, 0.935, "Red square = that kind of evidence AGAINST the trade at that 15-min bar's close (v2/dataset.py:221-237). "
             "If the count reaches N, exit at the next bar's open. N=4 is the 15-min setting, N=3 the 60-min one.",
             color=cs.TXT2, fontsize=11.5)
    p = save(fig, "opp_evidence_exit.png")
    res = {}
    for N, n in first.items():
        if n is None:
            res[N] = None
            continue
        k = rng_[n]
        res[N] = dict(bar=str(b.index[k]), bar_close=str(b.index[k] + pd.Timedelta(minutes=15)), count=int(c1[n]),
                      exit_open=float(b.O.iloc[k + 1]),
                      pnl=float(d * (b.O.iloc[k + 1] - row.entry) * USD[sym] - COST[sym]))
    grid = {str(b.index[k]): {names[r_]: bool(X[n, r_]) for r_ in range(7)} | {"count_1b": int(c1[n]), "count_2b": int(c2[n])}
            for n, k in enumerate(rng_)}
    disc = []
    for N in (3, 4):
        st = row[f"t_exit_opp{N}_1b"]; rc = res[N]
        if rc is None and pd.Timestamp(st).strftime("%H:%M") == "16:45":
            continue
        if rc is None:
            disc.append(f"opp{N}_1b: recomputed no trigger, stored exit {st}")
        elif str(pd.Timestamp(st)) != str(pd.Timestamp(rc["bar_close"])) and abs(rc["pnl"] - row[f"pnl_opp{N}_1b"]) > 0.01:
            disc.append(f"opp{N}_1b: recomputed exit at {rc['bar_close']} pnl {rc['pnl']:.2f} vs stored t_exit {st} pnl {row[f'pnl_opp{N}_1b']:.2f}")
    card("opp_evidence_exit", dict(
        chart=os.path.basename(p), market=MICRO[sym], signal_bar_start=str(t), direction=int(d),
        how_picked=f"the first of the three random Model B examples (order mes_loss, mes_win, mnq_win) whose stored opp3_1b or opp4_1b exit fires before 16:45: modelB_{src_name}",
        caption=(f"The same {MICRO[sym]} {t:%Y-%m-%d} trade, with the 7 opposite-evidence kinds checked at each 15-min close. "
                 f"N=3 would first trigger at {res[3]['bar_close'] if res[3] else 'never'}; N=4 at {res[4]['bar_close'] if res[4] else 'never'}. "
                 f"Model B ignores these and holds to 16:45 ({oos_row.pnl_usd:+.2f} $)."),
        evidence_kinds_source="v2/dataset.py:221-237 (recomputed here on v3 bars)",
        first_reach=res, grid=grid, stored_labels=stored, discrepancies=disc or ["none"]))
    print("opp disc:", disc, res)


def main():
    o = pd.read_parquet(OOS)
    o = o[o.t_exit < HOLDOUT]
    f = pd.read_csv(FOLDS)
    f = f[f.cfg == "15|hold|M3|cls|exp"].set_index("fold")
    rng = np.random.default_rng(20261109)
    picks = {}
    for name, m, w in [("mes_win", "ES", True), ("mes_loss", "ES", False), ("mnq_win", "NQ", True)]:
        g = o[(o.market == m) & ((o.pnl_usd > 0) == w)]
        q = g.R.quantile([0.25, 0.75])
        c = g[(g.R >= q.iloc[0]) & (g.R <= q.iloc[1])]
        picks[name] = (m, c.iloc[rng.integers(len(c))])
    which = sys.argv[1:] or list(picks) + ["opp"]
    for name, (m, r) in picks.items():
        if name not in which:
            continue
        fold = str(r.t.year) if r.t < pd.Timestamp("2025-01-01") else "2025H1"
        chart(name, m, r.t, int(r.d), r, float(f.loc[fold, "threshold"]), float(f.loc[fold, "keep_q"]))
    if "opp" in which:
        # first of the 3 random examples (MES first: the user's main market) whose stored opp4_1b or opp3_1b exit fires before 16:45
        for name in ("mes_loss", "mes_win", "mnq_win"):
            m, r = picks[name]
            ev = load_event(m, r.t, int(r.d))
            if pd.Timestamp(ev.t_exit_opp4_1b).strftime("%H:%M") != "16:45" or pd.Timestamp(ev.t_exit_opp3_1b).strftime("%H:%M") != "16:45":
                print("opp example:", name)
                opp_chart(m, r.t, int(r.d), r, name)
                break


if __name__ == "__main__":
    main()
