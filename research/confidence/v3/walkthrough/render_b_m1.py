"""Render walkthrough examples 1-11 (Model B kept, Model B skips, M1 points scorecard) with the shared toolkit
(mtf_chart.py). Every labelled number is RECOMPUTED here, not copied from examples.csv:
  score / kept flag   v2/out/models_scores_15.parquet  (s|15|hold|M3|cls|exp, s|15|hold|M1|cls|exp) for the exact
                      (market, t, d) row; Model B also cross-checked against v2/out/oos_M3_cls_hold_15m_exp.parquet
  threshold           v2/out/models_folds.csv (cfg, fold = calendar year of the signal bar; 2025 -> 2025H1)
  entry / stop / exit our own 1-minute walk on the example's 1-minute slice (labels.py:295-334 rules: entry = open of
                      the first minute of the next 15-min bar, stop checked first each minute, fill min(open, stop)
                      -1 tick for longs, else time exit at the close of the last minute before 16:45 of the trade's
                      session, v2/lucid.py:24-37), net of costs (signals.py:30-33), compared with v2_events pnl_hold
  chart features      R20, VWAP side, room to high/low of day, 60-min trend recomputed from v3/data bars and compared
                      with the v2_events values the model read
  M1 points           coef x signal / (ln2/20) with the fold's own coefficients (v2/models.py:101-155,
                      v2/out/models_points.csv); the implied intercept logit(score) - sum(coef x signal) is checked to be
                      the same constant for other rows of the same fold (proves the points reproduce the stored score)
Outputs: v3/walkthrough/ex_NN_mtf.png, ex_NN_card.png, cards/ex_NN_card.json.
Usage (from research/confidence): python3 v3/walkthrough/render_b_m1.py [ex01 ex02 ...]"""
import json
import math
import os
import shutil
import sys

import numpy as np
import pandas as pd

import chart_style as cs
import mtf_chart as mc
import render_examples as RE
from mtf_chart import COST, MICRO, USD, fp
from wt_common import TICK, bars

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.abspath(os.path.join(HERE, "..", ".."))
CARDS = os.path.join(HERE, "cards")
os.makedirs(CARDS, exist_ok=True)
PTS = math.log(2) / 20
CFG = {"B": "15|hold|M3|cls|exp", "M1": "15|hold|M1|cls|exp"}
FOLDS = pd.read_csv(os.path.join(CONF, "v2", "out", "models_folds.csv"))
PCOEF = pd.read_csv(os.path.join(CONF, "v2", "out", "models_points.csv"))
MKT = {"ES": "MES", "NQ": "MNQ", "YM": "MYM"}


_window0 = mc.window
MIN_BEFORE = {5: 100, 15: 110}


def _window(B, tf, decision, extend_to=None):
    """same as mtf_chart.window, but on 5/15-min reach back far enough to show >= MIN_BEFORE bars before the decision
    (decisions right after a weekend or holiday otherwise have an empty left half). Local to this script."""
    W = _window0(B, tf, decision, extend_to)
    n = MIN_BEFORE.get(tf)
    if n:
        prev = B.index[B.index < decision]
        have = int((W.index < decision).sum())
        if have < n and len(prev) > have:
            lo = prev[-min(n, len(prev))]
            W = B[(B.index >= lo) & (B.index <= W.index.max())]
    return W


mc.window = _window


def fold_of(t):
    return "2025H1" if t >= pd.Timestamp("2025-01-01") else str(t.year)


def scores_row(sym, t, d):
    cols = ["market", "t", "d"] + [f"{p}|{c}" for c in CFG.values() for p in ("s", "k")]
    s = pd.read_parquet(os.path.join(CONF, "v2", "out", "models_scores_15.parquet"), columns=cols,
                        filters=[("t", "==", t)])
    s = s[(s.d == d)]
    s = s[s.market.isin([sym, MKT[sym]])]
    assert len(s) == 1, (sym, t, d, len(s))
    return s.iloc[0]


def threshold(cfg, fy):
    f = FOLDS[(FOLDS.cfg == cfg) & (FOLDS.fold.astype(str) == fy)]
    assert len(f) == 1
    return float(f.threshold.iloc[0])


def walk_1m(m, sym, d, t_entry, stop):
    """labels.py:295-334 hold walk on the example's 1-minute slice. Returns entry, exit px, exit minute, kind, pnl."""
    sess = (pd.Timestamp(t_entry) + pd.Timedelta(hours=6)).normalize()
    end = sess + pd.Timedelta(hours=16, minutes=45)
    p = m[(m.index >= t_entry) & (m.index < end)]
    assert len(p) and p.index[0] == pd.Timestamp(t_entry), "entry minute missing from slice"
    entry = float(p.O.iloc[0])
    tk = TICK[sym]
    for ts, o, h, l in zip(p.index, p.O.to_numpy(), p.H.to_numpy(), p.L.to_numpy()):
        if d > 0 and l <= stop:
            x = min(o, stop) - tk
            return entry, x, ts, "stop", d * (x - entry) * USD[sym] - COST[sym]
        if d < 0 and h >= stop:
            x = max(o, stop) + tk
            return entry, x, ts, "stop", d * (x - entry) * USD[sym] - COST[sym]
    x = float(p.C.iloc[-1])
    lab = "time (16:45 flat)" if p.index[-1] >= end - pd.Timedelta(minutes=1) else \
        f"time (last minute of the session, early close {p.index[-1] + pd.Timedelta(minutes=1):%H:%M})"
    return entry, x, p.index[-1], lab, d * (x - entry) * USD[sym] - COST[sym]


def chart_checks(sym, t, d, row):
    """Recompute a few inputs from the v3 bars and compare with the v2 event values the model read."""
    out = []
    b15 = bars(sym, 15)
    i = b15.index.get_loc(t)
    w = b15.iloc[i - 20:i]
    same_run = (w.inst == b15.inst.iloc[i]).all()
    r20 = max(float((w.H - w.L).mean()), 2 * TICK[sym]) if same_run else np.nan
    out.append(("R20 (15-min, pts)", r20, float(row.R20)))
    c = float(b15.C.iloc[i])
    vw = float(b15.vwap.iloc[i])
    out.append(("VWAP side (+1 = trade side)", float(np.sign(d * (c - vw))), float(row.vwap_side)))
    s = b15[(b15.sess == b15.sess.iloc[i]) & (b15.index <= t)]
    room = ((s.H.max() - c) if d > 0 else (c - s.L.min())) / float(row.R20)
    out.append(("room to high/low of day (R20)", room, float(row.day_room)))
    b60 = bars(sym, 60)
    cl = b60.index + pd.Timedelta(minutes=60)
    j = int(np.flatnonzero((cl <= t + pd.Timedelta(minutes=15)) & (b60.inst == b15.inst.iloc[i]).to_numpy())[-1])
    e8, e20, e50 = b60.ema8.iloc[j], b60.ema20.iloc[j], b60.ema50.iloc[j]
    e50l = b60.ema50.iloc[j - 5] if b60.run.iloc[j - 5] == b60.run.iloc[j] else np.nan
    tb = 1 if (e8 > e20 > e50 and e50 > e50l) else (-1 if (e8 < e20 < e50 and e50 < e50l) else 0)
    out.append(("60-min trend (with trade)", float(tb * d), float(row.m60_trend)))
    return out


def m1_detail(row, sym, fy, score_m1):
    """Points per signal with the fold's coefficients, plus market offset, and the implied intercept."""
    import models as mdl
    cf = PCOEF[(PCOEF.cfg == CFG["M1"]) & (PCOEF.fold.astype(str) == fy)].set_index("column").coef
    E = pd.DataFrame([row])
    S = mdl.signal_frame(E).iloc[0]
    desc = {f"sig_{n}": dsc for n, _, dsc, _ in mdl.SIGNALS}
    x = {c: float(S[c]) for c in mdl.SIG_COLS}
    x["cost_R"] = float(row.cost_R)
    x["mkt_ES"] = float(sym == "ES")
    x["mkt_YM"] = float(sym == "YM")
    lin = sum(cf.get(c, 0.0) * v for c, v in x.items())
    icpt = math.log(score_m1 / (1 - score_m1)) - lin
    rows = []
    for c, v in x.items():
        p = v * cf.get(c, 0.0) / PTS
        nm = {**{"cost_R": "round-trip cost / stop distance", "mkt_ES": "market offset (MES)",
                 "mkt_YM": "market offset (MYM)"}, **desc}[c]
        rows.append(dict(signal=c, plain=nm, value=v, coef=float(cf.get(c, 0.0)), points=p))
    rows.sort(key=lambda z: -abs(z["points"]))
    return rows, icpt, lin / PTS


def m1_intercept_spread(fy, n=200):
    """implied intercept of M1 over n random rows of the same fold: should be a constant if the points reproduce it."""
    import models as mdl
    cf = PCOEF[(PCOEF.cfg == CFG["M1"]) & (PCOEF.fold.astype(str) == fy)].set_index("column").coef
    s = pd.read_parquet(os.path.join(CONF, "v2", "out", "models_scores_15.parquet"),
                        columns=["market", "t", "d", f"s|{CFG['M1']}"])
    yr0 = pd.Timestamp(fy[:4] + "-01-01")
    s = s[(s.t >= yr0) & (s.t < yr0 + pd.DateOffset(months=6 if fy.endswith("H1") else 12))]
    s = s.sample(n, random_state=0)
    out = []
    for mk, g in s.groupby("market"):
        sym = {"MES": "ES", "MNQ": "NQ", "MYM": "YM"}.get(mk, mk)
        ev = pd.read_parquet(os.path.join(CONF, "v2", "out", f"v2_events_{sym}_15.parquet"),
                             filters=[("t", "in", list(g.t.unique()))])
        E = g.merge(ev, on=["t", "d"])
        S = mdl.signal_frame(E)
        lin = (S[mdl.SIG_COLS] * cf.reindex(mdl.SIG_COLS).fillna(0).to_numpy()).sum(1) + cf["cost_R"] * E.cost_R + \
            cf["mkt_ES"] * (sym == "ES") + cf["mkt_YM"] * (sym == "YM")
        sc = E[f"s|{CFG['M1']}"].clip(1e-9, 1 - 1e-9)
        out.append(np.log(sc / (1 - sc)) - lin)
    v = pd.concat(out)
    return float(v.min()), float(v.max())


def render(r):
    import modelb_charts as mb
    kind = "M1" if "_m1_" in r.example_id else ("skip" if "skip" in r.example_id else "B")
    num = r.example_id[2:4]
    sym, d = r.sym, (1 if r.side == "LONG" else -1)
    t = pd.Timestamp(r.signal_bar)
    dec = t + pd.Timedelta(minutes=15)
    row = mb.load_event(sym, t, d)
    fy = fold_of(t)
    S = scores_row(sym, t, d)
    cfg = CFG["M1" if kind == "M1" else "B"]
    score, kept = float(S[f"s|{cfg}"]), bool(S[f"k|{cfg}"])
    thr = threshold(cfg, fy)
    scoreB, thrB = float(S[f"s|{CFG['B']}"]), threshold(CFG["B"], fy)
    scoreM1, thrM1 = float(S[f"s|{CFG['M1']}"]), threshold(CFG["M1"], fy)
    disc = []
    if kind == "B":
        o = pd.read_parquet(os.path.join(CONF, "v2", "out", "oos_M3_cls_hold_15m_exp.parquet"), filters=[("t", "==", t)])
        o = o[(o.d == d) & (o.market.isin([sym, MKT[sym]]))]
        if len(o) != 1 or abs(float(o.score.iloc[0]) - score) > 1e-6:
            disc.append(f"oos file score mismatch: {o.score.tolist()} vs {score}")
    if kept != (score >= thr):
        disc.append(f"kept flag {kept} but score {score:.4f} vs threshold {thr:.4f}")
    if kind in ("B", "M1") and not kept:
        disc.append("example is not kept by its model")
    if kind == "skip" and kept:
        disc.append("skip example is actually kept")
    m = mc.slice_1m(r.example_id, sym)
    stop = float(row.stop)
    entry, xpx, xts, xkind, pnl = walk_1m(m, sym, d, pd.Timestamp(row.t_entry), stop)
    if abs(entry - float(row.entry)) > 1e-6:
        disc.append(f"entry {entry} vs events entry {row.entry}")
    if abs(pnl - float(row.pnl_hold)) > 0.01:
        disc.append(f"1-min walk pnl {pnl:.2f} vs events pnl_hold {row.pnl_hold:.2f}")
    if abs(pnl - float(r.pnl_usd_per_micro)) > 0.01:
        disc.append(f"1-min walk pnl {pnl:.2f} vs examples.csv {r.pnl_usd_per_micro:.2f}")
    if abs(score - float(r.score)) > 1e-6:
        disc.append(f"score {score:.6f} vs examples.csv {r.score:.6f}")
    risk_usd = abs(entry - stop) * USD[sym]
    Rm = pnl / risk_usd
    xt_bar = pd.Timestamp(row.t_exit_hold)
    if xkind == "stop" and not (xt_bar - pd.Timedelta(minutes=15) <= xts < xt_bar):
        disc.append(f"stop minute {xts} not inside the bar ending {xt_bar}")
    checks = chart_checks(sym, t, d, row)
    for nm, ours, theirs in checks:
        if np.isfinite(ours) and np.isfinite(theirs) and abs(ours - theirs) > (0.02 if "R20 (" in nm else 0.05):
            disc.append(f"{nm}: v3-bar recompute {ours:+.3f} vs v2 event {theirs:+.3f}")
    pts, icpt, lin_pts = m1_detail(row, sym, fy, scoreM1)
    if kind == "M1":
        top = pts[0]["signal"]
        if top != r.driver or abs(pts[0]["points"] - float(r.driver_points)) > 0.06:
            disc.append(f"M1 biggest input recomputed {top} {pts[0]['points']:+.2f} vs csv {r.driver} {r.driver_points}")
        lo, hi = m1_intercept_spread(fy)
        icpt_chk = f"implied M1 intercept {icpt:+.4f}; same fold, 200 random rows: {lo:+.4f} .. {hi:+.4f}"
        if not (lo - 1e-3 <= icpt <= hi + 1e-3) or hi - lo > 1e-3:
            disc.append("M1 intercept not constant: " + icpt_chk)
    else:
        icpt_chk = ""

    trade = dict(side=d, entry_time=pd.Timestamp(row.t_entry), entry_px=entry, stop=stop,
                 exit_time=xts + pd.Timedelta(seconds=59), exit_px=xpx, pnl=pnl)
    flags = [k for k in ["pb", "ema8_pb", "ema20_pb", "ema50_pb", "mom_turn", "pb_break"] if row[k] == 1]
    R20 = float(row.R20)

    def ov15(ax, axm, B, X):
        i = X.i(t)
        ax.axvspan(i - 4.5, i + 0.5, color="#202050", alpha=0.45, zorder=0)
        ax.text(i - 4.4, 0.05, "5-bar stop window", transform=ax.get_xaxis_transform(), color="#aab0ff", fontsize=11)
        cs.ring(ax, i, i, B.L.iloc[i], B.H.iloc[i], cs.EXITC, B.H.max() - B.L.min())
        ax.annotate(f"SIGNAL bar {t:%H:%M}-{dec:%H:%M}: {' + '.join(flags)}",
                    (i, B.H.iloc[i] if d > 0 else B.L.iloc[i]), xytext=(-40, 70 if d > 0 else -70),
                    textcoords="offset points", ha="right", color=cs.EXITC, fontsize=12, fontweight="bold", zorder=12,
                    arrowprops=dict(arrowstyle="-", color=cs.EXITC),
                    bbox=dict(boxstyle="round,pad=0.25", fc="#111111", ec=cs.EXITC))
        c = B.C.iloc[i]
        ax.annotate("", (i + 0.8, c), (i + 0.8, c - d * R20), arrowprops=dict(arrowstyle="<->", color="#ffffff", lw=1.3),
                    zorder=12)
        ax.text(i + 1.0, c - d * R20 / 2, f"1 R20 = {R20:.2f} pts\n(avg range of the 20 bars before)", color="#ffffff",
                fontsize=10.5, va="center", zorder=12)
        for key, colr, nm in (("m15_sw_room", mc.SWH if d > 0 else mc.SWL, "next swing ahead"),
                              ("m15_sw_cushion", mc.SWL if d > 0 else mc.SWH, "last swing behind")):
            v = row[key]
            if np.isfinite(v):
                lvl = c + d * v * R20 if key == "m15_sw_room" else c - d * v * R20
                ax.hlines(lvl, max(i - 12, 0), i + 0.5, color=colr, lw=1.6, ls="--", zorder=8)
                ax.text(max(i - 12, 0), lvl, f"{nm} {fp(sym, lvl)} ({v:+.1f} R20)", color=colr, fontsize=10.5,
                        va="bottom", zorder=12)

    def ov5(ax, axm, B, X):
        x0, x1 = X(dec - pd.Timedelta(minutes=30)), X(dec)
        if np.isfinite(x0) and np.isfinite(x1):
            ax.axvspan(x0, x1, color="#3a3a10", alpha=0.5, zorder=0)
            ax.text(x0, 0.06, "last 6 five-min bars:\n'5-min trigger same way?'", transform=ax.get_xaxis_transform(),
                    color="#e8e08a", fontsize=10.5, ha="right")

    def ov60(ax, axm, B, X):
        cl = B.index + pd.Timedelta(minutes=60)
        j = int(np.flatnonzero(cl <= dec)[-1])
        ax.axvspan(j - 0.5, j + 0.5, color="#3a3a10", alpha=0.6, zorder=0)
        ax.annotate(f"last CLOSED 60-min bar {B.index[j]:%H:%M}-{cl[j]:%H:%M}\n= what the 60-min inputs read",
                    (j, B.H.iloc[j]), xytext=(-30, 40), textcoords="offset points", ha="right", color="#e8e08a",
                    fontsize=11, zorder=12, arrowprops=dict(arrowstyle="-", color="#e8e08a"),
                    bbox=dict(boxstyle="round,pad=0.2", fc="#111111", ec="#e8e08a"))

    tw = {1: "UP", -1: "DOWN", 0: "none"}

    def trtxt(k):
        v = row[k]
        if not np.isfinite(v):
            return "no value"
        return f"{tw[int(v * d)]} -> {'agrees' if v > 0 else ('AGAINST' if v < 0 else 'neutral')}"

    sysname = "M1 points scorecard" if kind == "M1" else "Model B"
    used = {1: (False, "NOT used for the decision; the stop is checked on these 1-minute bars after entry"),
            5: (True, f"USED by {sysname}: 5-min inputs (trend {trtxt('m5_trend')}, Momentum, 5-min trigger)"),
            15: (True, f"USED: base chart - signal bar, rules, stop, most inputs (trend {trtxt('m15_trend')})"),
            60: (True, f"USED: 60-min inputs from the last CLOSED 60-min bar (trend {trtxt('m60_trend')})"),
            120: (False, f"NOT used by {sysname} (context only)")}
    notes = {15: f"VWAP side {'+1 agrees' if row.vwap_side > 0 else '-1 against'} ({row.vwap_dist:+.2f} R20)\n"
                 f"room to high/low of day {row.day_room:+.2f} R20\ncandles with/against (3 bars): "
                 f"{int(row.pat_with3)}/{int(row.pat_against3)}\ncost / stop distance {row.cost_R:.3f}"}
    b15 = bars(sym, 15)
    i15 = b15.index.get_loc(t)
    if b15.sess.iloc[i15 - 4:i15 + 1].nunique() > 1:
        gapnote = (f"NOTE: the 5-bar stop window reaches back into the previous session "
                   f"({b15.index[i15 - 4]:%a %m-%d %H:%M}), so the stop sits {abs(entry - stop):.2f} pts away "
                   f"= {row.risk_R20:.1f} R20, far wider than usual")
        import textwrap
        notes[15] = textwrap.fill(gapnote, 46) + "\n" + notes[15]   # narrow box: keep the signal bar visible
    side_w = "LONG" if d > 0 else "SHORT"
    verdict = "KEPT" if kept else "SKIPPED"
    if kind == "M1":
        title = f"{r.example_id}: M1 SCORECARD {verdict} {MICRO[sym]} {side_w} {dec:%a %Y-%m-%d %H:%M} ET -> {pnl:+.2f} $"
        sub = (f"{r.category}. M1 score {score:.3f} vs {fy} threshold {thr:.3f} -> {verdict}. Biggest input: "
               f"{pts[0]['plain']} ({pts[0]['points']:+.1f} points). Same events, entry and hold-to-16:45 exit as Model B. "
               f"Picked by: {r.selection_rule}, {r.seed}.")
    else:
        title = (f"{r.example_id}: MODEL B {verdict if kept else 'SKIP'} {MICRO[sym]} {side_w} {dec:%a %Y-%m-%d %H:%M} ET -> " +
                 (f"{pnl:+.2f} $/micro" if kept else f"if taken {pnl:+.2f} $"))
        sub = (f"{r.category}. Score {score:.3f} vs {fy} threshold {thr:.3f} -> {verdict}. "
               + ("Entry next 15-min open, stop only, flat at 16:45. " if kept else
                  "Shown: what the trade WOULD have done (entry next open, stop only, flat 16:45). ")
               + f"Picked by: {r.selection_rule}, {r.seed}.")
    png = os.path.join(HERE, f"ex_{num}_mtf.png")
    mc.mtf_figure(png, r.example_id, sym, dec, trade, title, sub, used,
                  overlays={15: ov15, 5: ov5, 60: ov60}, extend_to=xts + pd.Timedelta(minutes=1), panel_notes=notes)

    # ---------------------------------------------------------------- card
    inputs = [dict(plain=z["plain"], value=z["value"], read=RE._rd(z["read"]),
                   where=f"{z['key']} ({z['model_constraint']})") for z in mb.inputs_table(row, sym)]
    agree = sum(z["read"] == "agrees" for z in inputs)
    against = sum(z["read"] == "against" for z in inputs)
    shown = [p for p in pts if abs(p["points"]) >= 0.05]
    if kind == "M1":
        drivers = [f"Rules that fired on the signal bar: {', '.join(flags)} (any rule firing makes the bar a candidate)",
                   f"M1 adds fixed points per yes/no signal (+20 points = double the weighted odds of a winner). "
                   f"This trade's points ({fy} coefficients), biggest first; total {lin_pts:+.1f} points:"]
        drivers += [f"{p['points']:+5.1f} points  {p['plain']}" for p in shown[:7]]
        decision = (f"M1 score {score:.4f} {'>=' if kept else '<'} {fy} threshold {thr:.4f}  ->  "
                    f"{'KEPT: enter' if kept else 'SKIPPED'} at the {pd.Timestamp(row.t_entry):%H:%M} open "
                    f"{fp(sym, entry)}, stop {fp(sym, stop)}")
    else:
        drivers = [f"Rules that fired on the signal bar: {', '.join(flags)} (any rule firing makes the bar a candidate)",
                   f"Model B score {score:.3f} vs threshold {thr:.3f}: the tree model has no per-input weights, so the "
                   f"readable proxy below is the M1 points table (same target, {fy} coefficients) applied to this trade:"]
        drivers += [f"{p['points']:+5.1f} points  {p['plain']}" for p in shown[:5]]
        decision = (f"Model B score {score:.4f} {'>=' if kept else '<'} {fy} threshold {thr:.4f}  ->  "
                    + (f"KEPT: enter at the {pd.Timestamp(row.t_entry):%H:%M} open {fp(sym, entry)}, stop {fp(sym, stop)}"
                       if kept else f"SKIPPED (would have entered {fp(sym, entry)} at "
                                    f"{pd.Timestamp(row.t_entry):%H:%M}, stop {fp(sym, stop)})"))
    drivers.append(f"Plain count over all 69 Model B inputs: {agree} agree, {against} against")
    win = pnl > 0
    right = win if kept else not win
    if kind == "skip":
        verdict_w = "RIGHT to skip" if right else "WRONG to skip"
        outcome = (f"OUTCOME IF TAKEN: exit {fp(sym, xpx)} at {xts:%H:%M} ({xkind}) -> {pnl:+.2f} $ per micro after "
                   f"${COST[sym]:.2f} costs ({Rm:+.2f} R)  =  skipping was {verdict_w.split()[0]}")
        why = ("The model scored this setup well below its cut-off, and it would have " +
               ("made money: the skip left a winner on the table. A low score only means 'weaker than the best 10-30% "
                "of setups', not 'will lose'." if win else
                "lost: price went the other way and hit the stop, so the low score kept us out of a loser."))
    else:
        outcome = (f"OUTCOME: exit {fp(sym, xpx)} at {xts:%H:%M} ({xkind}) -> {pnl:+.2f} $ per micro after "
                   f"${COST[sym]:.2f} costs ({Rm:+.2f} R)  =  {'RIGHT' if win else 'WRONG'}")
        why = (("The short" if d < 0 else "The long") +
               (" worked: price moved our way after entry and the stop was never hit, so holding to 16:45 kept the gain."
                if win else (" failed: price went against us after entry and hit the stop." if xkind == "stop" else
                             " failed: price drifted against us and was still on the wrong side at 16:45.")))
    note1 = ("Score: v2/out/models_scores_15.parquet (%s, model not refit); threshold: v2/out/models_folds.csv fold %s. "
             "Inputs: v2/out/v2_events_%s_15.parquet. Entry/exit/P&L recomputed by a stop-first 1-minute walk "
             "(labels.py:295-334). Values are 'with the trade' (+ = good for this side), distances in R20." % (cfg, fy, sym))
    other = (f"For comparison: Model B score {scoreB:.3f} vs {thrB:.3f} ({'kept' if scoreB >= thrB else 'skipped'}); "
             f"M1 score {scoreM1:.3f} vs {thrM1:.3f} ({'kept' if scoreM1 >= thrM1 else 'skipped'}).")
    chk = "Recomputed from v3 bars vs value the model read: " + "; ".join(
        f"{nm} {a:+.2f} vs {b:+.2f}" for nm, a, b in checks)
    cnotes = [note1, other, chk] + ([icpt_chk] if icpt_chk else []) + (
        ["DISCREPANCIES: " + " | ".join(disc)] if disc else ["No discrepancies between recomputed and stored values."])
    card = dict(title=f"DECISION CARD  {r.example_id}  {MICRO[sym]} {side_w}  signal bar {t:%Y-%m-%d %H:%M}-{dec:%H:%M}",
                decision=decision, drivers=drivers, outcome=outcome, why=why, win=right, notes=cnotes,
                inputs=inputs, example=r.example_id, system=sysname, score=score, threshold=thr, kept=kept,
                entry_time=pd.Timestamp(row.t_entry), entry_px=entry, stop=stop, exit_minute=xts, exit_px=xpx,
                exit_kind=xkind, pnl_usd_per_micro=pnl, R=Rm, risk_usd=risk_usd,
                m1_points=pts, recompute_checks=[dict(item=a, recomputed=b, model_value=c) for a, b, c in checks],
                discrepancies=disc, selection_rule=r.selection_rule, seed=r.seed)
    cpng = os.path.join(HERE, f"ex_{num}_card.png")
    mc.decision_card(cpng, card)
    shutil.move(os.path.join(HERE, f"ex_{num}_card.json"), os.path.join(CARDS, f"ex_{num}_card.json"))
    return dict(id=r.example_id, kind=kind, score=round(score, 4), thr=round(thr, 4), kept=kept, entry=entry, stop=stop,
                exit=xpx, exit_min=str(xts), xkind=xkind, pnl=round(pnl, 2), R=round(Rm, 3), disc=disc)


if __name__ == "__main__":
    want = sys.argv[1:] or [f"ex{k:02d}" for k in range(1, 12)]
    res = []
    for r in RE.EX.itertuples():
        if any(r.example_id.startswith(w) for w in want):
            out = render(r)
            print(json.dumps(out, default=str), flush=True)
            res.append(out)
