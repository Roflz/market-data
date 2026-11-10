"""Render walkthrough examples end to end (5-panel figure + decision card PNG/JSON) from examples.csv.
Templates implemented here: Model B kept trade (render_modelB) and A1 noise-band day (render_a1).
Usage (from research/confidence with the project PYTHONPATH):  python3 v3/walkthrough/render_examples.py ex01 ex14"""
import math
import os
import sys

import numpy as np
import pandas as pd

import chart_style as cs
import mtf_chart as mc
from mtf_chart import COST, MICRO, USD, fp

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.abspath(os.path.join(HERE, "..", ".."))
EX = pd.read_csv(os.path.join(HERE, "examples.csv"),
                 parse_dates=["decision_time", "entry_time", "exit_time", "signal_bar", "hold_exit_time"])
PTS = math.log(2) / 20


def _rd(s):
    s = str(s)
    for k in ("agrees", "against", "fired", "info", "neutral"):
        if s.startswith(k):
            return k
    return "neutral"


def m1_points(row, fy):
    """M1 points of THIS trade with that year's M1 coefficients (v2/models.py:101-127 signals, :150-155 points;
    coefficients v2/out/models_points.csv cfg 15|hold|M1|cls|exp). Used as a readable proxy for 'what weighs most'."""
    import models as mdl
    pts = pd.read_csv(os.path.join(CONF, "v2", "out", "models_points.csv"))
    cf = pts[(pts.cfg == "15|hold|M1|cls|exp") & (pts.fold.astype(str) == fy)].set_index("column").coef
    E = pd.DataFrame([row])
    S = mdl.signal_frame(E).iloc[0]
    desc = {f"sig_{n}": dsc for n, _, dsc, _ in mdl.SIGNALS}
    out = []
    for c in list(mdl.SIG_COLS) + ["cost_R"]:
        v = float(row["cost_R"]) if c == "cost_R" else float(S[c])
        p = v * cf.get(c, 0.0) / PTS
        if abs(p) >= 0.05:
            out.append((c, desc.get(c, "round-trip cost / stop distance"), v, p))
    return sorted(out, key=lambda z: -abs(z[3]))


# ============================================================================================ Model B (v2 M3, 15-min)
def render_modelB(r):
    import modelb_charts as mb
    sym, d = r.sym, (1 if r.side == "LONG" else -1)
    t = pd.Timestamp(r.signal_bar)
    row = mb.load_event(sym, t, d)
    dec = t + pd.Timedelta(minutes=15)
    entry = float(row.entry)
    pnl = float(r.pnl_usd_per_micro)
    xpx = entry + (pnl + COST[sym]) / (d * USD[sym])
    kept = "SKIP" not in r.category
    trade = dict(side=d, entry_time=row.t_entry, entry_px=entry, stop=float(row.stop), exit_time=r.exit_time,
                 exit_px=xpx, pnl=pnl)
    flags = [k for k in ["pb", "ema8_pb", "ema20_pb", "ema50_pb", "mom_turn", "pb_break"] if row[k] == 1]
    R20 = float(row.R20)

    def ov15(ax, axm, B, X):
        i = X.i(t)
        ax.axvspan(i - 4.5, i + 0.5, color="#202050", alpha=0.45, zorder=0)
        ax.text(i - 4.4, 0.05, "5-bar stop window", transform=ax.get_xaxis_transform(), color="#aab0ff", fontsize=11)
        cs.ring(ax, i, i, B.L.iloc[i], B.H.iloc[i], cs.EXITC, B.H.max() - B.L.min())
        ax.annotate(f"SIGNAL bar {t:%H:%M}-{dec:%H:%M}: {' + '.join(flags)}", (i, B.H.iloc[i] if d > 0 else B.L.iloc[i]),
                    xytext=(-40, 70 if d > 0 else -70), textcoords="offset points", ha="right", color=cs.EXITC,
                    fontsize=12, fontweight="bold", zorder=12, arrowprops=dict(arrowstyle="-", color=cs.EXITC),
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
                ax.hlines(lvl, i - 12, i + 0.5, color=colr, lw=1.6, ls="--", zorder=8)
                ax.text(i - 12, lvl, f"{nm} {fp(sym, lvl)} ({v:+.1f} R20)", color=colr, fontsize=10.5,
                        va="bottom", zorder=12)

    def ov5(ax, axm, B, X):
        x0, x1 = X(dec - pd.Timedelta(minutes=30)), X(dec)
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

    used = {1: (False, "NOT used for the decision; the stop is checked on these 1-minute bars after entry"),
            5: (True, f"USED: 5-min inputs (trend {trtxt('m5_trend')}, Momentum, swings, 5-min trigger)"),
            15: (True, f"USED: Model B's base chart - signal bar, rules, stop, most inputs (trend {trtxt('m15_trend')})"),
            60: (True, f"USED: 60-min inputs from the last CLOSED 60-min bar (trend {trtxt('m60_trend')})"),
            120: (False, "NOT used by Model B (context only)")}
    notes = {15: f"VWAP side {'+1 agrees' if row.vwap_side > 0 else '-1 against'} ({row.vwap_dist:+.2f} R20)\n"
                 f"room to high/low of day {row.day_room:+.2f} R20\ncandles with/against (3 bars): "
                 f"{int(row.pat_with3)}/{int(row.pat_against3)}\ncost / stop distance {row.cost_R:.3f}"}
    side_w = "LONG" if d > 0 else "SHORT"
    title = (f"{r.example_id}: MODEL B {'KEPT' if kept else 'SKIPPED'} {MICRO[sym]} {side_w}  {dec:%a %Y-%m-%d %H:%M} ET  "
             f"->  {pnl:+.2f} $ per micro")
    sub = (f"{r.category}. Score {r.score:.3f} vs {t.year} threshold {r.threshold:.3f} -> "
           f"{'KEPT' if r.score >= r.threshold else 'SKIPPED'}. Entry next 15-min open, stop only, flat at 16:45. "
           f"Picked by: {r.selection_rule}, {r.seed}.")
    png = os.path.join(mc.OUTD, f"{r.example_id}_chart.png")
    mc.mtf_figure(png, r.example_id, sym, dec, trade, title, sub, used,
                  overlays={15: ov15, 5: ov5, 60: ov60}, extend_to=pd.Timestamp(r.exit_time), panel_notes=notes)
    # ---- card
    fy = str(t.year) if t < pd.Timestamp("2025-01-01") else "2025H1"
    pts = m1_points(row, fy)
    inputs = [dict(plain=z["plain"], value=z["value"], read=_rd(z["read"]),
                   where=f"{z['key']} ({z['model_constraint']})") for z in mb.inputs_table(row, sym)]
    agree = sum(z["read"] == "agrees" for z in inputs); against = sum(z["read"] == "against" for z in inputs)
    drivers = [f"Rules that fired on the signal bar: {', '.join(flags)} (any rule firing makes the bar a candidate)",
               f"Model score {r.score:.3f} vs threshold {r.threshold:.3f}: the tree model has no per-input weights, so the "
               f"readable proxy below is the M1 points table (same target) applied to this trade:"]
    drivers += [f"{p:+5.1f} points  {dsc}" for c, dsc, v, p in pts[:5]]
    drivers.append(f"Plain count over all 69 inputs: {agree} agree, {against} against")
    win = pnl > 0
    why = (("The short" if d < 0 else "The long") + (" worked: price moved our way after entry and the stop was never hit, "
           "so holding to 16:45 kept the gain." if win else " failed: price went against us after entry " +
           ("and hit the stop." if r.exit_time < pd.Timestamp(dec.date()) + pd.Timedelta(hours=16, minutes=45)
            else "and was still against us at 16:45.")))
    card = dict(title=f"DECISION CARD  {r.example_id}  {MICRO[sym]} {side_w}  signal bar {t:%Y-%m-%d %H:%M}-{dec:%H:%M}",
                decision=f"Model B score {r.score:.4f} {'>=' if r.score >= r.threshold else '<'} {t.year} threshold "
                         f"{r.threshold:.4f}  ->  {'KEPT: enter' if r.score >= r.threshold else 'SKIPPED'} at the "
                         f"{row.t_entry:%H:%M} open {fp(sym, entry)}, stop {fp(sym, row.stop)}",
                drivers=drivers,
                outcome=f"OUTCOME: exit {fp(sym, xpx)} at {pd.Timestamp(r.exit_time):%H:%M} -> {pnl:+.2f} $ per micro after "
                        f"${COST[sym]:.2f} costs ({r.R:+.2f} R)  =  {'RIGHT' if win else 'WRONG'}",
                why=why, win=win,
                notes=["Score source: v2/out/oos_M3_cls_hold_15m_exp.parquet:score (model not refit). Threshold: "
                       "v2/out/models_folds.csv. Inputs: v2/out/v2_events_%s_15.parquet. Values are 'with the trade' "
                       "(+ = good for this side), distances in R20 (average bar range)." % sym],
                inputs=inputs, example=r.example_id, m1_points=[dict(signal=c, plain=dsc, value=v, points=p) for c, dsc, v, p in pts])
    mc.decision_card(os.path.join(mc.OUTD, f"{r.example_id}_card.png"), card)
    return png


# ============================================================================================ A1 noise band (MNQ, v3)
def a1_day(session):
    """Per-check table for one session, replicating v3/exp_g1_noiseband/g1lib.py:86-135 exactly (sigma over the 14
    previous FULL sessions, UB/LB, close of the 5-min bar ending at each check, RTH VWAP, position logic), and the
    legs from g1lib.make_signal itself for a cross-check."""
    import harness as H
    sys.path.insert(0, os.path.join(CONF, "v3", "exp_g1_noiseband"))
    import g1lib as G
    S = H.sessions("NQ")
    B5 = H.bars("NQ", 5)
    early = G.early_set("NQ")
    dec = G.DEC_HALF
    C, VW = G.decision_grid(S, B5, dec)
    O = S["px_0930"].to_numpy(float)
    pc, pl = S["prev_close_1600"].to_numpy(float), S["prev_last_px"].to_numpy(float)
    cprev = np.where(np.isfinite(pc), pc, pl)
    is_early = np.array([s in early for s in S.index])
    move = np.abs(C / O[:, None] - 1.0)
    full_ok = (~is_early) & np.isfinite(O) & np.isfinite(move).all(axis=1)
    i = S.index.get_loc(pd.Timestamp(session))
    prev_full = np.flatnonzero(full_ok[:i])[-14:]
    sig = move[prev_full].mean(axis=0)
    UB = max(O[i], cprev[i]) * (1 + sig)
    LB = min(O[i], cprev[i]) * (1 - sig)
    pos = 0
    rows = []
    for j, hhmm in enumerate(dec):
        c, vw, u, lo = C[i, j], VW[i, j], UB[j], LB[j]
        before = pos
        if pos == 1:
            new = -1 if c < lo else (0 if c < np.fmax(u, vw) else 1)
        elif pos == -1:
            new = 1 if c > u else (0 if c > np.fmin(lo, vw) else -1)
        else:
            new = 1 if c > u else (-1 if c < lo else 0)
        if is_early[i] and int(hhmm) > 1230:
            new = before
        act = {(0, 1): "ENTER LONG", (0, -1): "ENTER SHORT", (1, 0): "EXIT long (inside)",
               (-1, 0): "EXIT short (inside)", (1, -1): "REVERSE to short", (-1, 1): "REVERSE to long"}.get(
            (before, new), "hold long" if new == 1 else ("hold short" if new == -1 else "stay flat"))
        rows.append(dict(check=hhmm, time=pd.Timestamp(session) + pd.Timedelta(hours=int(hhmm[:2]), minutes=int(hhmm[2:])),
                         close_5m=c, upper_band=u, lower_band=lo, rth_vwap=vw, sigma_pct=sig[j] * 100, pos_before=before,
                         pos_after=new, action=act))
        pos = new
    T = pd.DataFrame(rows)
    legs = G.make_signal(early)(S.iloc[max(0, i - 40):i + 1], {5: B5[(B5.index >= S.index[max(0, i - 40)] - pd.Timedelta(hours=6))
                                                                    & (B5.index < S.index[i] + pd.Timedelta(hours=18))]})
    legs = legs[legs.session == S.index[i]]
    return T, dict(open_0930=O[i], prev_close=cprev[i], prev_close_src="prev_close_1600" if np.isfinite(pc[i]) else
                   "prev_last_px", early=bool(is_early[i]), sigma_sessions=[str(S.index[k].date()) for k in prev_full]), legs


def render_a1(r):
    sym = "NQ"
    session = pd.Timestamp(r.decision_time).normalize()
    T, info, legs = a1_day(session)
    a1 = pd.read_parquet(os.path.join(CONF, "v3", "out", "trades", "A1.parquet"))
    tr = a1[a1.session == session].sort_values("t_entry")
    # cross-checks: replicated position path vs g1lib legs vs stored trades
    held = T[T.pos_after != 0]
    chk_legs = sorted(zip(legs.entry.astype(str), legs.d.astype(int))) == sorted(
        zip(held.check.astype(str), held.pos_after.astype(int)))
    first = tr.iloc[0]
    dec = pd.Timestamp(first.t_entry)
    tot = float(tr.pnl_usd.sum())
    extra = [dict(time=t_, px=p_, label="", color=cs.HILITE if dd > 0 else cs.EXITC, marker="^" if dd > 0 else "v")
             for t_, p_, dd in zip(tr.t_entry, tr.entry_px, tr.d)]
    extra += [dict(time=t_, px=p_, label="", color="#ffffff", marker="X") for t_, p_ in zip(tr.t_exit, tr.exit_px)]
    trade = dict(side=int(first.d), entry_time=first.t_entry, entry_px=float(first.entry_px), stop=None,
                 exit_time=tr.t_exit.iloc[-1], exit_px=float(tr.exit_px.iloc[-1]), pnl=tot, extra=extra)
    T_end = T.time + pd.Timedelta(0)

    def bands(ax, axm, B, X):
        xs, ub, lb = [], [], []
        for k, rr in T.iterrows():
            x0 = X(rr.time - pd.Timedelta(minutes=30) if k else session + pd.Timedelta(hours=9, minutes=30))
            x1 = X(rr.time)
            xs += [x0, x1]; ub += [rr.upper_band] * 2; lb += [rr.lower_band] * 2
        ax.plot(xs, ub, color="#ffd24d", lw=2.2, zorder=7, label="A1 upper band")
        ax.plot(xs, lb, color="#ff9d4d", lw=2.2, zorder=7, label="A1 lower band")
        ax.text(xs[-1], ub[-1], " upper band", color="#ffd24d", fontsize=11, va="bottom", zorder=12)
        ax.text(xs[-1], lb[-1], " lower band", color="#ff9d4d", fontsize=11, va="top", zorder=12)
        xo = X(session + pd.Timedelta(hours=9, minutes=30))
        ax.hlines([info["open_0930"]], xo, xs[-1], color="#ffffff", lw=1.0, ls="--", zorder=6)
        ax.hlines([info["prev_close"]], xo, xs[-1], color="#bbbbbb", lw=1.0, ls="-.", zorder=6)
        ax.text(xo, info["open_0930"], f"09:30 open {fp(sym, info['open_0930'])}", color="#ffffff", fontsize=10.5,
                ha="right", va="bottom", zorder=12)
        ax.text(xo, info["prev_close"], f"prev 16:00 close {fp(sym, info['prev_close'])}", color="#bbbbbb",
                fontsize=10.5, ha="right", va="top", zorder=12)
        ax.plot([X(t_) for t_ in T.time], T.rth_vwap, color="#00e5ff", lw=0, marker="s", ms=6, zorder=8,
                label="A1 RTH VWAP (from 09:30) at checks")
        for _, rr in T.iterrows():
            xc = X(rr.time)
            ax.axvline(xc, color="#666699", lw=0.7, ls=":", zorder=1)
            colr = cs.GOOD if rr.pos_after == 1 else (cs.BAD if rr.pos_after == -1 else cs.TXT2)
            ax.plot(xc, rr.close_5m, "o", color=colr, ms=8, mec="#000000", zorder=9)
            if rr.action not in ("stay flat",):
                ax.text(xc, 0.93 if rr.pos_after >= 0 else 0.86, rr.action.split(" (")[0].replace("hold ", "hold\n"),
                        transform=ax.get_xaxis_transform(), color=colr, fontsize=9.5, ha="center", va="top", zorder=12,
                        rotation=0)

    used = {1: (False, "NOT used: A1 only looks every 30 minutes (lines show the bands for reference)"),
            5: (True, "USED: A1 reads the CLOSE of the 5-min bar ending at each half-hour check (dots)"),
            15: (False, "NOT used by A1 (context only)"), 60: (False, "NOT used by A1 (context only)"),
            120: (False, "NOT used by A1 (context only)")}
    leg_txt = "; ".join(f"{a:%H:%M}->{b:%H:%M} {'long' if dd > 0 else 'short'} {p:+.1f}$" for a, b, dd, p in
                        zip(tr.t_entry, tr.t_exit, tr.d, tr.pnl_usd))
    title = f"{r.example_id}: A1 NOISE BAND  MNQ  {session:%a %Y-%m-%d}  ->  day total {tot:+.2f} $ per micro"
    sub = (f"{r.category}. Trades: {leg_txt}. Picked by: {r.selection_rule}, {r.seed}.")
    png = os.path.join(mc.OUTD, f"{r.example_id}_chart.png")
    mc.mtf_figure(png, r.example_id, sym, dec, trade, title, sub, used, overlays={5: bands, 1: bands},
                  extend_to=pd.Timestamp(tr.t_exit.iloc[-1]),
                  panel_notes={5: "dots = 5-min close at each check (green = long after the check, red = short,\n"
                                  "grey = flat); yellow/orange steps = bands for that half hour; cyan squares = RTH "
                                  "VWAP\n(the A1 exit line, anchored 09:30, NOT the 18:00 session VWAP drawn in blue)"})
    # card at the first decision
    k0 = int(np.flatnonzero(T.time == dec)[0]) if (T.time == dec).any() else 0
    c0 = T.iloc[k0]
    d0 = int(first.d)
    inputs = [dict(plain="09:30 open (band anchor)", value=info["open_0930"], read="info", where="px_0930, g1lib.py:91"),
              dict(plain=f"previous close ({info['prev_close_src']})", value=info["prev_close"], read="info",
                   where="g1lib.py:92-94"),
              dict(plain=f"noise sigma at {c0.check[:2]}:{c0.check[2:]} (% avg |move from open|, 14 days)",
                   value=c0.sigma_pct, read="info", where="g1lib.py:95-103"),
              dict(plain="upper band = max(open, prev close) x (1 + sigma)", value=c0.upper_band,
                   read="agrees" if (d0 > 0 and c0.close_5m > c0.upper_band) else "info", where="g1lib.py:107"),
              dict(plain="lower band = min(open, prev close) x (1 - sigma)", value=c0.lower_band,
                   read="agrees" if (d0 < 0 and c0.close_5m < c0.lower_band) else "info", where="g1lib.py:108"),
              dict(plain=f"close of 5-min bar ending {c0.check[:2]}:{c0.check[2:]}", value=c0.close_5m,
                   read="agrees", where="g1lib.py:48-75"),
              dict(plain="RTH VWAP from 09:30 (exit line only)", value=c0.rth_vwap,
                   read="agrees" if d0 * (c0.close_5m - c0.rth_vwap) > 0 else "against", where="g1lib.py:49-60,119-120"),
              dict(plain="position before the check", value=float(c0.pos_before), read="info", where="g1lib.py:111-125")]
    for _, rr in T.iterrows():
        inputs.append(dict(plain=("AFTER: " if rr.check > c0.check else "") +
                                 f"{rr.check[:2]}:{rr.check[2:]} close {fp(sym, rr.close_5m)} band "
                                 f"{fp(sym, rr.lower_band)}-{fp(sym, rr.upper_band)} VWAP {fp(sym, rr.rth_vwap)}",
                           value=rr.action, read="agrees" if rr.pos_after != 0 else "neutral", where=""))
    win = tot > 0
    why = ("The breakout out of the normal-noise zone kept going, so the position stayed outside the band and on the "
           "right side of VWAP long enough to pay." if win else
           "The move out of the noise zone did not follow through: price fell back inside the band or through VWAP, so "
           "A1 exited (or reversed) at a loss; most A1 trades lose small, the edge comes from a few big trend days.")
    card = dict(title=f"DECISION CARD  {r.example_id}  A1 noise band  MNQ  {session:%Y-%m-%d}",
                decision=f"Rule at {c0.check[:2]}:{c0.check[2:]}: 5-min close {fp(sym, c0.close_5m)} "
                         f"{'>' if d0 > 0 else '<'} {'upper' if d0 > 0 else 'lower'} band "
                         f"{fp(sym, c0.upper_band if d0 > 0 else c0.lower_band)}  ->  {'LONG' if d0 > 0 else 'SHORT'} 1 MNQ "
                         f"at the {dec:%H:%M} mark {fp(sym, first.entry_px)} (no stop)",
                drivers=["Only one thing: did the 5-min close at the half-hour check leave the noise band? sigma = how "
                         "far MNQ is usually from its 09:30 open by this time of day (last 14 full sessions).",
                         "After entry: hold while the close stays beyond BOTH the band and the 09:30 VWAP; flat or "
                         "reverse otherwise; everything closed at the 16:00 mark."],
                outcome=f"OUTCOME: {len(tr)} trade(s) today, total {tot:+.2f} $ per micro after $2.00 per trade  =  "
                        f"{'RIGHT' if win else 'WRONG'}",
                why=why, win=win,
                notes=[f"Cross-check: replicated position path matches g1lib.make_signal legs: {chk_legs}. "
                       f"sigma sessions: {info['sigma_sessions'][0]} .. {info['sigma_sessions'][-1]}. "
                       "Trades: v3/out/trades/A1.parquet."],
                inputs=inputs, example=r.example_id, checks=T.to_dict("records"))
    mc.decision_card(os.path.join(mc.OUTD, f"{r.example_id}_card.png"), card)
    print("A1 cross-check legs==replica:", chk_legs)
    return png


RENDER = {"modelB": render_modelB, "modelBskip": render_modelB, "a1": render_a1}

if __name__ == "__main__":
    want = sys.argv[1:]
    for r in EX.itertuples():
        if want and not any(r.example_id.startswith(w) for w in want):
            continue
        kind = r.example_id.split("_")[1]
        if kind in RENDER:
            print(r.example_id, RENDER[kind](r), flush=True)
        else:
            print(r.example_id, "no renderer yet for", kind)
