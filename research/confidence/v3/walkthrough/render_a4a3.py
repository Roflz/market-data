"""Render the A4 (CPI/NFP 08:30 fade, MNQ) and A3 (options-expiry Friday short, MES leg) walkthrough examples
ex16-ex19 with the shared toolkit (mtf_chart.py). Every labelled value is recomputed here from the data:
  mark prices px_HHMM = OPEN of the 1-minute bar starting at HH:MM (v3/build_data.py:52-58), recomputed from the
  per-example 1-minute slice and compared with v3/data/sessions_{sym}.parquet and v3/out/trades/{A4,A3}.parquet.
  A4 rule: v3/exp_G4/g4lib.py:58-88 (m = px_0845 - px_0830 at :74, side = -sign(m) at :84, skips at :58-63,:71-73).
  A3 rule: v3/exp_g3_expiry/g3.py:80-106 (A3_LEG at :104), opex day = calendar_days.py:11-24 (repo root).
  Costs: v3/harness.py:114-117 (MNQ $2.00, MES $3.50); pnl = side x (exit - entry) x $/pt - cost (harness.py:300-302).
  C1 matched control: harness.py:419-451 (random same-year sessions, same marks and side). Here its EXACT expectation
  (mean over all usable same-year sessions) is recomputed and compared with the stored 999-draw c1.
Outputs (only these files): walkthrough/ex_NN_mtf.png, walkthrough/ex_NN_card.png, walkthrough/cards/ex_NN_card.json
(NN = 16..19).
Usage (from research/confidence): python3 -W ignore v3/walkthrough/render_a4a3.py"""
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

import chart_style as cs
import mtf_chart as mc
from mtf_chart import COST, USD, fp
_WIN1_DEFAULT = mc.WIN[1]   # skeptic fix: A3 must not inherit the A4 75-min 1-min window (order-dependent)

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.abspath(os.path.join(HERE, "..", ".."))
V3 = os.path.join(CONF, "v3")
CARDS = os.path.join(HERE, "cards")
os.makedirs(CARDS, exist_ok=True)
HOLDOUT = pd.Timestamp("2025-06-30 18:00")
EX = pd.read_csv(os.path.join(HERE, "examples.csv"), parse_dates=["decision_time", "entry_time", "exit_time"])
EX = EX[EX.example_id.str.match(r"ex1[6-9]_")]
SESS = {s: pd.read_parquet(os.path.join(V3, "data", f"sessions_{s}.parquet")) for s in ("NQ", "ES", "YM")}
TR = {k: pd.read_parquet(os.path.join(V3, "out", "trades", f"{k}.parquet")) for k in ("A4", "A3")}
MKT = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
DISC = []   # discrepancies found


def mark(m1, session, hhmm):
    """px_HHMM from the 1-minute slice: open of the minute starting at HH:MM (build_data.py:52-58); if no bar in that
    minute, the last traded price before it (close of the previous bar). Returns (price, age minutes)."""
    h, mi = int(hhmm[:2]), int(hhmm[2:])
    t = session + pd.Timedelta(hours=h, minutes=mi) - (pd.Timedelta(days=1) if h >= 18 else pd.Timedelta(0))
    if t in m1.index:
        return float(m1.loc[t, "O"]), 0
    prev = m1[m1.index < t]
    return float(prev.C.iloc[-1]), int((t - prev.index[-1]) / pd.Timedelta(minutes=1)) - 1


def check(name, mine, stored, tol=1e-9):
    ok = (mine == stored) if isinstance(mine, (bool, np.bool_, str)) else abs(float(mine) - float(stored)) <= tol
    if not ok:
        DISC.append(f"{name}: recomputed {mine} vs stored {stored}")
    return ok


def c1_expect(sym, year, e_mk, x_mk, d, skip_marks=None):
    """Exact mean of the C1 replay (same year, same marks, same side) over every same-year session with both prices."""
    S = SESS[sym]
    S = S[S.index.year == year]
    e, x = S[f"px_{e_mk}"].to_numpy(float), S[f"px_{x_mk}"].to_numpy(float)
    ok = np.isfinite(e) & np.isfinite(x)
    pnl = d * (x[ok] - e[ok]) * USD[sym] - COST[sym]
    return float(pnl.mean()), int(ok.sum())


def ctx15(sym, t):
    """the user's indicators on the last CLOSED 15-min bar at time t (v3 bars, build_data.py:123-145)."""
    B = mc.bars(sym, 15)
    k = int(np.flatnonzero(B.index + pd.Timedelta(minutes=15) <= t)[-1])
    b = B.iloc[k].copy()
    prev = B.iloc[max(0, k - 20):k]
    prev = prev[prev.run == b.run]
    # R20 = mean(H - L) of the 20 bars before, same contract run, floor 2 ticks (features.py:176-183)
    b["R20"] = max(float((prev.H - prev.L).mean()), 2 * mc.TICK[sym]) if len(prev) == 20 else np.nan
    tr = int(b.trend) if np.isfinite(b.trend) else 0
    return b, tr


def shade(ax, X, t0, t1, color, label, y=0.05, fs=11):
    x0, x1 = X(t0), X(t1)
    if not (np.isfinite(x0) or np.isfinite(x1)):
        return
    x0 = x0 if np.isfinite(x0) else -0.5
    x1 = x1 if np.isfinite(x1) else ax.get_xlim()[1]
    ax.axvspan(x0, x1, color=color, alpha=0.33, zorder=0.5, lw=0)
    if label:
        ax.text(x0, y, " " + label, transform=ax.get_xaxis_transform(), color="#ffffff", fontsize=fs, va="bottom",
                zorder=12, bbox=dict(fc="#111111", ec=color, boxstyle="round,pad=0.2", alpha=0.9))


# ============================================================================================ A4
def render_a4(r):
    sym, session = "NQ", pd.Timestamp(r.decision_time).normalize()
    m1 = pd.read_parquet(os.path.join(HERE, "slices", f"{r.example_id}_1m.parquet"))
    m1 = m1[m1.sess == session] if "sess" in m1 else m1
    S = SESS[sym].loc[session]
    px = {k: mark(m1, session, k) for k in ("0830", "0845", "0930", "0945")}
    for k, (p, a) in px.items():
        check(f"{r.example_id} px_{k}", p, S[f"px_{k}"]); check(f"{r.example_id} age_{k}", a, S[f"age_{k}"])
    m = px["0845"][0] - px["0830"][0]
    d = -int(np.sign(m))
    entry, exitp = px["0845"][0], px["0945"][0]
    pnl = d * (exitp - entry) * USD[sym] - COST[sym]
    t = TR["A4"][TR["A4"].session == session].iloc[0]
    for nm, mine, st in (("m_pts", m, t.m_pts), ("side", d, t.d), ("entry", entry, t.entry_px), ("exit", exitp, t.exit_px),
                         ("pnl", pnl, t.pnl_usd), ("csv pnl", pnl, r.pnl_usd_per_micro), ("csv m", m, r.m_pts)):
        check(f"{r.example_id} {nm}", mine, st)
    kinds = [k.upper() for k in ("nfp", "cpi") if bool(S[k])]
    rule_ok = bool(S.nfp or S.cpi) and not bool(S.roll) and all(px[k][1] <= 5 for k in ("0830", "0845", "0945"))
    c1e, c1n = c1_expect(sym, session.year, "0845", "0945", d)
    p930 = d * (px["0930"][0] - entry) * USD[sym] - COST[sym]
    # path while in the trade (1-minute, 08:45-09:44): worst and best open P&L (no stop, so information only)
    path = m1[(m1.index >= session + pd.Timedelta(hours=8, minutes=45)) & (m1.index < session + pd.Timedelta(hours=9, minutes=45))]
    worst = (path.L.min() - entry) * USD[sym] if d > 0 else (entry - path.H.max()) * USD[sym]
    best = (path.H.max() - entry) * USD[sym] if d > 0 else (entry - path.L.min()) * USD[sym]
    b15, tr15 = ctx15(sym, session + pd.Timedelta(hours=8, minutes=45))
    A4all = TR["A4"]
    dec = session + pd.Timedelta(hours=8, minutes=45)
    t830, t930, t945 = (session + pd.Timedelta(hours=h, minutes=mm) for h, mm in ((8, 30), (9, 30), (9, 45)))
    trade = dict(side=d, entry_time=dec, entry_px=entry, stop=None, exit_time=t945, exit_px=exitp, pnl=pnl)

    def ov(ax, axm, B, X, big=True, lab=True):
        shade(ax, X, t830, dec, "#b8860b", f"08:30 release -> 08:45: move m = {m:+.2f} pts" if (big and lab) else "",
              y=0.80)
        shade(ax, X, dec, t945, "#2a6fdb", "held 08:45 -> 09:45 (no stop)" if big else "", y=0.86)
        x0, x1 = X(t830), X(dec)
        if big and np.isfinite(x0) and np.isfinite(x1):
            ax.hlines(px["0830"][0], x0 - 3, x1, color="#ffffff", lw=1.6, ls="--", zorder=9)
            ax.text(x0 - 3, px["0830"][0], f"px 08:30 {fp(sym, px['0830'][0])} ", color="#ffffff", fontsize=11, ha="right",
                    va="center", zorder=12)
            ax.annotate("", (x1, px["0845"][0]), (x1, px["0830"][0]),
                        arrowprops=dict(arrowstyle="->", color="#ffd24d", lw=2.4), zorder=12)
            ax.text(x1 + 0.3, (px["0830"][0] + px["0845"][0]) / 2,
                    f" m = {m:+.2f} pts -> fade = {'LONG' if d > 0 else 'SHORT'}", color="#ffd24d", fontsize=12,
                    fontweight="bold", va="center", zorder=12, bbox=dict(fc="#111111", ec="#ffd24d", alpha=0.9))
            x9 = X(t930)
            if np.isfinite(x9):
                ax.axvline(x9, color="#bbbbbb", lw=1.0, ls="--", zorder=3)
                ax.text(x9, 0.80, " 09:30 cash open", transform=ax.get_xaxis_transform(), color="#bbbbbb", fontsize=10.5,
                        va="top", zorder=12)
        elif np.isfinite(x1):
            ax.axvline(x1, color="#ffd24d", lw=0.8, ls=":", zorder=3)

    ovs = {1: ov, 5: lambda ax, axm, B, X: ov(ax, axm, B, X, lab=False),
           15: lambda ax, axm, B, X: ov(ax, axm, B, X, big=False),
           60: lambda ax, axm, B, X: ov(ax, axm, B, X, big=False), 120: lambda ax, axm, B, X: ov(ax, axm, B, X, big=False)}
    used = {1: (True, "USED: the rule reads only 3 prices = the OPEN of the 08:30, 08:45 and 09:45 minutes"),
            5: (False, "NOT used by A4 (same move shown on 5-min bars)"),
            15: (False, "NOT used by A4; note the 08:30 bar here IS the 08:30-08:45 move"),
            60: (False, "NOT used by A4 (context only)"), 120: (False, "NOT used by A4 (context only)")}
    notes = {1: f"A4 reads: px 08:30 {fp(sym, px['0830'][0])}, px 08:45 {fp(sym, px['0845'][0])} -> m {m:+.2f}\n"
                f"enter {'LONG' if d > 0 else 'SHORT'} at px 08:45, exit at px 09:45 {fp(sym, exitp)}\n"
                f"open P&L while held: worst {worst:+.1f} $, best {best:+.1f} $ (1-min highs/lows)"}
    mc.WIN[1] = (pd.Timedelta(hours=2), pd.Timedelta(minutes=75))   # local only: show the 09:45 exit on the 1-min panel
    win = pnl > 0
    title = (f"{r.example_id}: A4 {'/'.join(kinds)} 08:30 FADE  MNQ {'LONG' if d > 0 else 'SHORT'}  "
             f"{dec:%a %Y-%m-%d %H:%M} ET  ->  {pnl:+.2f} $ per micro")
    sub = (f"{r.category}. {', '.join(kinds)} released 08:30 ET; MNQ moved {m:+.2f} pts by 08:45, so A4 took the OPPOSITE "
           f"side at the 08:45 mark and exited at the 09:45 mark, no stop. Picked by: {r.selection_rule}, {r.seed}.")
    png = os.path.join(HERE, f"ex_{r.example:02d}_mtf.png")
    mc.mtf_figure(png, r.example_id, sym, dec, trade, title, sub, used, overlays=ovs, extend_to=t945, panel_notes=notes)
    inputs = [
        dict(plain=f"scheduled release today ({'/'.join(kinds)})", value="yes", read="fired",
             where="sessions nfp/cpi; build_data.py:252-259"),
        dict(plain="contract-roll session? (skip if yes)", value=str(bool(S.roll)), read="neutral", where="g4lib.py:58-60"),
        dict(plain="price age at 08:30 / 08:45 / 09:45 (skip if > 5 min)",
             value=f"{px['0830'][1]} / {px['0845'][1]} / {px['0945'][1]} min", read="neutral", where="g4lib.py:61-63,71"),
        dict(plain="px 08:30 = open of the 08:30 minute", value=px["0830"][0], read="info", where="build_data.py:52-58"),
        dict(plain="px 08:45 = open of the 08:45 minute", value=px["0845"][0], read="info", where="build_data.py:52-58"),
        dict(plain="m = px 08:45 - px 08:30 (points)", value=m, read="fired", where="g4lib.py:74"),
        dict(plain=f"side = opposite of m -> {'LONG' if d > 0 else 'SHORT'}", value=float(d), read="fired",
             where="g4lib.py:84"),
        dict(plain="m in 15-min R20 units (size of move, NOT used)", value=m / float(b15.R20),
             read="neutral", where="context only; features.py:176-183"),
        dict(plain=f"15-min EMA stack at 08:30 bar (NOT used): "
                   f"{ {1: 'up', -1: 'down', 0: 'mixed'}[tr15]}", value=float(tr15),
             read="neutral", where="context only; signals.py:98-99 (+1 up, -1 down, 0 mixed)"),
        dict(plain="15-min close vs 18:00 session VWAP (NOT used)", value=float(b15.C - b15.vwap),
             read="neutral", where="context only; signals.py:46-48"),
        dict(plain="AFTER decision: px 09:30 (cash open)", value=px["0930"][0], read="info", where=""),
        dict(plain="AFTER decision: P&L if exited at 09:30 instead", value=p930, read="info", where=""),
        dict(plain="AFTER decision: px 09:45 = exit", value=exitp, read="info", where="g4lib.py:66 exit_='0945'"),
        dict(plain="AFTER decision: worst open P&L while held", value=worst, read="info", where="1-minute lows/highs"),
        dict(plain="AFTER decision: best open P&L while held", value=best, read="info", where="1-minute lows/highs"),
        dict(plain=f"C1: same trade on random {session.year} days (exact mean, n={c1n})", value=c1e, read="info",
             where="harness.py:419-451; stored c1 %.2f" % t.c1),
    ]
    why = ((f"The first reaction to the {'/'.join(kinds)} number ({m:+.2f} pts by 08:45) overshot and partly reversed "
            f"within the hour: price was {fp(sym, exitp)} at 09:45 vs {fp(sym, entry)} at entry, so the fade earned "
            f"{pnl:+.2f} $.") if win else
           (f"The {m:+.2f}-point first reaction did NOT reverse: it kept going the same way to {fp(sym, exitp)} by 09:45, "
            f"so fading it lost {pnl:+.2f} $. A4 has no stop and only a 52% win rate; it relies on reversals being "
            f"bigger than continuations on average."))
    card = dict(
        title=f"DECISION CARD  {r.example_id}  A4 release fade  MNQ  {session:%Y-%m-%d} 08:45",
        decision=f"Rule: m = px 08:45 {fp(sym, entry)} - px 08:30 {fp(sym, px['0830'][0])} = {m:+.2f} pts "
                 f"{'<' if m < 0 else '>'} 0  ->  {'LONG' if d > 0 else 'SHORT'} 1 MNQ at {fp(sym, entry)}, exit 09:45 "
                 f"mark, no stop (all skip checks passed: {rule_ok})",
        drivers=[f"Only the sign of the 08:30-08:45 move on a {'/'.join(kinds)} day decides the side. Its size, the "
                 "trend, VWAP and the EMAs are NOT inputs (listed below as context, marked NOT used).",
                 f"A4 overall (v3/out/trades/A4.parquet): {len(A4all)} trades, mean {A4all.pnl_usd.mean():+.2f} $ per "
                 f"trade, {100 * (A4all.pnl_usd > 0).mean():.0f}% winners, {100 * (A4all.d > 0).mean():.0f}% long."],
        outcome=f"OUTCOME: exit {fp(sym, exitp)} at 09:45 -> {pnl:+.2f} $ per micro after $2.00 costs "
                f"({d * (exitp - entry):+.2f} pts)  =  {'RIGHT' if win else 'WRONG'}",
        why=why, win=win,
        notes=[f"Edge vs an ordinary day: this trade {pnl:+.2f} $ minus C1 {c1e:+.2f} $ = {pnl - c1e:+.2f} $ "
               f"(stored d_i {t.d_i:+.2f} uses the 999-draw c1 {t.c1:+.2f}). Prices recomputed from 1-minute bars and "
               f"matched to sessions_NQ.parquet and A4.parquet."],
        inputs=inputs, example=r.example_id,
        recomputed=dict(px_0830=px["0830"][0], px_0845=entry, px_0930=px["0930"][0], px_0945=exitp, m_pts=m, side=d,
                        pnl_usd=pnl, c1_exact=c1e, c1_stored=float(t.c1), worst_open_usd=worst, best_open_usd=best))
    return png, card


# ============================================================================================ A3
def third_friday(session):
    first = pd.Timestamp(session.year, session.month, 1)
    return first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)


def render_a3(r):
    sym, session = "ES", pd.Timestamp(r.decision_time).normalize()
    m1 = pd.read_parquet(os.path.join(HERE, "slices", f"{r.example_id}_1m.parquet"))
    m1 = m1[m1.sess == session]
    S = SESS[sym].loc[session]
    px = {k: mark(m1, session, k) for k in ("0930", "1200", "1600")}
    for k, (p, a) in px.items():
        check(f"{r.example_id} px_{k}", p, S[f"px_{k}"])
    d = -1
    entry, exitp = px["0930"][0], px["1600"][0]
    pnl = d * (exitp - entry) * USD[sym] - COST[sym]
    A3 = TR["A3"]
    day = A3[A3.session == session]
    t = day[day.market == sym].iloc[0]
    for nm, mine, st in (("entry", entry, t.entry_px), ("exit", exitp, t.exit_px), ("pnl", pnl, t.pnl_usd),
                         ("csv pnl", pnl, r.pnl_usd_per_micro)):
        check(f"{r.example_id} {nm}", mine, st)
    tf3 = third_friday(session)
    check(f"{r.example_id} opex flag", bool(S.opex), True)
    check(f"{r.example_id} third Friday", str(tf3.date()), str(session.date()))
    # other basket legs, recomputed from their sessions tables
    legs = []
    for s2 in ("NQ", "YM"):
        if session in SESS[s2].index and (s2 != "YM" or session.year >= 2018):
            e2, x2 = SESS[s2].loc[session, "px_0930"], SESS[s2].loc[session, "px_1600"]
            p2 = -(x2 - e2) * USD[s2] - COST[s2]
            st = day[day.market == s2]
            if len(st):
                check(f"{r.example_id} {s2} leg pnl", p2, st.pnl_usd.iloc[0])
            legs.append((MKT[s2], e2, x2, p2))
    c1e, c1n = c1_expect(sym, session.year, "0930", "1600", d)
    path = m1[(m1.index >= session + pd.Timedelta(hours=9, minutes=30)) & (m1.index < session + pd.Timedelta(hours=16))]
    worst = (entry - path.H.max()) * USD[sym]
    best = (entry - path.L.min()) * USD[sym]
    t_worst, t_best = path.H.idxmax(), path.L.idxmin()
    p1200 = d * (px["1200"][0] - entry) * USD[sym] - COST[sym]
    on = entry - float(S.open_1800)
    dec = session + pd.Timedelta(hours=9, minutes=30)
    t1600 = session + pd.Timedelta(hours=16)
    mc.WIN[1] = _WIN1_DEFAULT
    b15, tr15 = ctx15(sym, dec)
    trade = dict(side=d, entry_time=dec, entry_px=entry, stop=None, exit_time=t1600, exit_px=exitp, pnl=pnl)
    # earlier expiry days visible on the 60/120-min panels
    prev_opex = [s for s in SESS[sym].index[SESS[sym].opex.astype(bool)] if session - pd.Timedelta(days=45) <= s < session]

    def ov(ax, axm, B, X, big=True, lab=True, marks=False):
        shade(ax, X, dec, t1600, "#8b1a1a", ("EXPIRY FRIDAY: short 09:30 -> cover 16:00 (no stop)" if lab else "")
              if big else "", y=0.05)
        if big:
            x0 = X(dec)
            if np.isfinite(x0):
                x1 = X(t1600)
                x1 = x1 if np.isfinite(x1) else ax.get_xlim()[1]
                ax.hlines(entry, x0, x1, color=cs.HILITE, lw=1.2, ls="--", zorder=8)
        if marks:
            for tt, yv, txt, colr, off, ha_ in ((t_worst, path.H.max(), f"worst point {t_worst:%H:%M}: {worst:+.1f} $", cs.BAD, (-30, 14), "right"),
                                           (t_best, path.L.min(), f"best point {t_best:%H:%M}: {best:+.1f} $", cs.GOOD, (30, 24), "left")):
                xw = X(tt)
                # skeptic fix: keep after-decision labels on the after-decision side and inside the axes:
                # label goes right if room, else left if it stays after the decision line, else circle only
                if np.isfinite(xw):
                    _lo, _hi = ax.get_xlim(); _xd = X(dec)
                    _room_right = (_hi - xw) / (_hi - _lo) > 0.17          # enough space right of the point
                    _room_left = (not np.isfinite(_xd)) or (xw - _xd) / (_hi - _lo) > 0.17   # label stays after decision
                    _right = _room_right or not _room_left
                    off, ha_ = ((abs(off[0]), off[1]), "left") if _right else ((-abs(off[0]), off[1]), "right")
                    _txt_ok = _room_right or _room_left     # narrow after-decision strip: circle only (text on 5-min + card)
                    ax.plot(xw, yv, "o", ms=11, mfc="none", mec=colr, mew=2, zorder=12)
                    if _txt_ok:
                        ax.annotate(txt, (xw, yv), xytext=off, textcoords="offset points", ha=ha_, va="center",
                                color=colr, fontsize=11, zorder=12, arrowprops=dict(arrowstyle="-", color=colr),
                                bbox=dict(fc="#111111", ec=colr, boxstyle="round,pad=0.2", alpha=0.9))
        for s in prev_opex:
            shade(ax, X, s + pd.Timedelta(hours=9, minutes=30), s + pd.Timedelta(hours=16), "#5a3a3a",
                  f"previous expiry {s:%m-%d}", y=0.86, fs=10)

    ovs = {1: ov, 5: lambda ax, axm, B, X: ov(ax, axm, B, X, marks=True),
           15: lambda ax, axm, B, X: ov(ax, axm, B, X, lab=False, marks=True),
           60: lambda ax, axm, B, X: ov(ax, axm, B, X, big=False),
           120: lambda ax, axm, B, X: ov(ax, axm, B, X, big=False)}
    used = {1: (True, "USED: only the OPEN of the 09:30 minute (entry) and of the 16:00 minute (exit)"),
            5: (False, "NOT used by A3: there is no price signal at all, only the calendar"),
            15: (False, "NOT used by A3 (context only)"), 60: (False, "NOT used by A3 (context only)"),
            120: (False, "NOT used by A3; shaded = expiry days")}
    notes = {5: f"A3 = calendar trade: 3rd Friday of {session:%B %Y} = {tf3:%Y-%m-%d}\nshort at px 09:30 "
                f"{fp(sym, entry)}, cover at px 16:00 {fp(sym, exitp)}\nwhile held: worst {worst:+.1f} $, best "
                f"{best:+.1f} $ (1-min highs/lows)"}
    win = pnl > 0
    title = (f"{r.example_id}: A3 EXPIRY-FRIDAY SHORT  MES  {dec:%a %Y-%m-%d %H:%M} ET  ->  {pnl:+.2f} $ per micro")
    sub = (f"{r.category}. Monthly options expiry (third Friday). Short 1 micro of each market at the 09:30 mark, cover at "
           f"the 16:00 mark, no stop; this chart is the MES leg. Picked by: {r.selection_rule}, {r.seed}.")
    png = os.path.join(HERE, f"ex_{r.example:02d}_mtf.png")
    mc.mtf_figure(png, r.example_id, sym, dec, trade, title, sub, used, overlays=ovs, extend_to=t1600, panel_notes=notes)
    inputs = [
        dict(plain=f"first day of month {session:%Y-%m}: weekday", value=pd.Timestamp(session.year, session.month, 1)
             .day_name(), read="info", where="calendar_days.py:16"),
        dict(plain="3rd Friday = 1st + (4 - weekday) mod 7 + 14 days", value=str(tf3.date()), read="fired",
             where="calendar_days.py:16-18"),
        dict(plain="is today a trading day? (else use day before)", value="yes", read="neutral",
             where="calendar_days.py:17-21"),
        dict(plain="quarterly (Mar/Jun/Sep/Dec) expiry? (NOT used)", value=str(bool(S.quad)), read="neutral",
             where="build_data.py:261"),
        dict(plain="px 09:30 = open of the 09:30 minute (entry)", value=entry, read="info", where="build_data.py:52-58"),
        dict(plain="overnight move 18:00 -> 09:30 (pts, NOT used)", value=on, read="neutral", where="context only"),
        dict(plain=f"15-min EMA stack at 09:15 bar (NOT used): {({1: 'up', -1: 'down', 0: 'mixed'})[tr15]}",
             value=float(tr15), read="neutral", where="context only; signals.py:98-99 (+1 up, -1 down, 0 mixed)"),
        dict(plain="15-min close vs 18:00 session VWAP (NOT used)", value=float(b15.C - b15.vwap), read="neutral",
             where="context only; signals.py:46-48"),
        dict(plain="AFTER decision: P&L if covered at 12:00", value=p1200, read="info", where=""),
        dict(plain="AFTER decision: worst open P&L while held", value=worst, read="info", where="1-minute highs"),
        dict(plain="AFTER decision: best open P&L while held", value=best, read="info", where="1-minute lows"),
        dict(plain="AFTER decision: px 16:00 = cover", value=exitp, read="info", where="g3.py:104 A3_LEG"),
    ]
    for mk, e2, x2, p2 in legs:
        inputs.append(dict(plain=f"same day, {mk} leg: short {e2:,.2f} -> {x2:,.2f}", value=p2, read="info",
                           where="A3 basket, g3.py:106"))
    inputs.append(dict(plain=f"C1: same trade on random {session.year} days (exact mean, n={c1n})", value=c1e,
                       read="info", where="harness.py:419-451; stored c1 %.2f" % t.c1))
    tot = pnl + sum(z[3] for z in legs)
    mes = A3[A3.market == sym]
    why = ((f"As the expiry idea expects, MES drifted down through the day: {fp(sym, entry)} at 09:30 to "
            f"{fp(sym, exitp)} at 16:00, so the short earned {pnl:+.2f} $.") if win else
           (f"MES rose from {fp(sym, entry)} at 09:30 to {fp(sym, exitp)} at 16:00, so the short lost {pnl:+.2f} $. "
            "Nothing in A3 looks at price, so it cannot avoid such days; only about half of expiry days are positive "
            "and the profit comes from a few big down days."))
    card = dict(
        title=f"DECISION CARD  {r.example_id}  A3 expiry-Friday short  MES leg  {session:%Y-%m-%d} 09:30",
        decision=f"Rule: today {session:%Y-%m-%d} is the monthly options expiry ({tf3:%a} {tf3:%Y-%m-%d})  ->  SHORT "
                 f"1 MES at the 09:30 mark {fp(sym, entry)}, cover at the 16:00 mark, no stop",
        drivers=["Only the calendar decides: no price, trend, VWAP or EMA is read. The trade is the same every month "
                 "(also on MNQ and MYM); the idea is that option-hedging flows that lift prices into the morning "
                 "settlement fade during the day.",
                 f"A3 MES leg overall (v3/out/trades/A3.parquet): {len(mes)} trades, mean {mes.pnl_usd.mean():+.2f} $, "
                 f"{100 * (mes.pnl_usd > 0).mean():.0f}% winners."],
        outcome=f"OUTCOME: cover {fp(sym, exitp)} at 16:00 -> {pnl:+.2f} $ per micro after $3.50 costs "
                f"({d * (exitp - entry):+.2f} pts)  =  {'RIGHT' if win else 'WRONG'}.  Whole basket that day: {tot:+.2f} $",
        why=why, win=win,
        notes=[f"Edge vs an ordinary day: {pnl:+.2f} $ minus C1 {c1e:+.2f} $ = {pnl - c1e:+.2f} $ (stored d_c1 "
               f"{t.d_c1:+.2f} uses the 999-draw c1 {t.c1:+.2f}). Prices recomputed from 1-minute bars and matched to "
               "sessions_ES.parquet and A3.parquet."],
        inputs=inputs, example=r.example_id,
        recomputed=dict(px_0930=entry, px_1200=px["1200"][0], px_1600=exitp, pnl_usd=pnl, third_friday=str(tf3.date()),
                        c1_exact=c1e, c1_stored=float(t.c1), worst_open_usd=worst, best_open_usd=best,
                        basket_total=tot, other_legs=[dict(market=a, entry=b, exit=c, pnl=e) for a, b, c, e in legs]))
    return png, card


if __name__ == "__main__":
    want = sys.argv[1:]
    for r in EX.itertuples():
        if want and not any(r.example_id.startswith(w) for w in want):
            continue
        assert r.decision_time < HOLDOUT and r.exit_time < HOLDOUT
        png, card = (render_a4 if "_a4_" in r.example_id else render_a3)(r)
        import textwrap
        card["decision"] = "\n".join(textwrap.wrap(card["decision"], 118, subsequent_indent="    "))
        card["outcome"] = "\n".join(textwrap.wrap(card["outcome"], 118, subsequent_indent="    "))
        card["notes"].append("C1 here = exact average over ALL same-year sessions with both prices; the stored c1 is the "
                             "average of 999 random draws from those sessions, so the two differ by sampling noise "
                             "(harness.py:419-451; early-close days use the last price there, dropped here).")
        cpng = os.path.join(HERE, f"ex_{r.example:02d}_card.png")
        mc.decision_card(cpng, card)
        js = os.path.splitext(cpng)[0] + ".json"
        shutil.move(js, os.path.join(CARDS, f"ex_{r.example:02d}_card.json"))
        print(r.example_id, png, cpng, flush=True)
    a3es = TR["A3"][TR["A3"].market == "ES"]
    print("A3 ES wins/losses:", int((a3es.pnl_usd > 0).sum()), int((a3es.pnl_usd <= 0).sum()))
    a4 = TR["A4"]
    print("A4 wins/losses:", int((a4.pnl_usd > 0).sum()), int((a4.pnl_usd <= 0).sum()))
    print("DISCREPANCIES:", json.dumps(DISC, indent=1) if DISC else "none")
