"""Shared toolkit for the walkthrough examples: the 5-panel multi-timeframe figure and the decision-card renderer.

FIGURE STANDARD (one tall figure per example): five stacked panels 1-min / 5-min / 15-min / 60-min / 120-min, each
centred on the DECISION TIME (yellow vertical line 'decision'), each with candles, EMA 8/20/50 (dashed red/orange/green),
session VWAP (light blue, anchored 18:00 ET), session high/low so far (white dotted steps), confirmed 3-bar swing
highs/lows (triangle at the pivot bar, dotted tail to the bar where it became KNOWN; hollow = not yet confirmed at the
decision), a Momentum(14) strip, and the region after the decision dimmed and labelled 'what happened next (not known
at decision)'. Entry / stop / exit are drawn on every panel where visible; each system's own overlays are passed in per
timeframe; every panel title says whether the system actually used that timeframe.

Data (all pre-holdout, < 2025-06-30 18:00 ET):
  5/15/60-min  research/confidence/v3/data/bars_{sym}_{tf}.parquet (v3/build_data.py:123-145; EMA/Momentum per contract run)
  120-min      bars120(): session-aligned 2-hour buckets of the v3 60-min bars starting 18:00 ET (18-20, 20-22, ...,
               16:00-16:45 short last bar), indicators recomputed with signals.context (signals.py:92-129)
  1-min        slices/<example_id>_1m.parquet cut once under the heavy lock by make_slices.py; VWAP rebuilt exactly as
               signals.py:46-48 (typical price x volume, reset per session and contract), EMAs via signals.context
Bar timestamps are bar START times (NinjaTrader labels the END)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import chart_style as cs
import signals as sg
from wt_common import (COST, HOLDOUT, MICRO, TICK, USD, bars, style_ax, time_ticks)  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
SLICES = os.path.join(HERE, "slices")
OUTD = os.path.join(HERE, "examples")
os.makedirs(OUTD, exist_ok=True)
DIM = "#0a1230"
SWL, SWH = "#7fd6ff", "#ffb3f5"
FIG_W = 15.5
DPI = 90
plt.rcParams.update({"font.size": 13, "font.family": "DejaVu Sans", "text.parse_math": False})

# window before / after the decision, per timeframe (FIGURE STANDARD)
WIN = {1: (pd.Timedelta(hours=2), pd.Timedelta(hours=1)), 5: (pd.Timedelta(hours=12), pd.Timedelta(hours=3)),
       15: (pd.Timedelta(hours=44), pd.Timedelta(hours=8)), 60: (pd.Timedelta(days=14), pd.Timedelta(days=1)),
       120: (pd.Timedelta(days=36), pd.Timedelta(days=2))}
AFTER_CAP = {1: pd.Timedelta(hours=1), 5: pd.Timedelta(hours=8), 15: pd.Timedelta(hours=10),
             60: pd.Timedelta(days=1), 120: pd.Timedelta(days=2)}


# ============================================================================================ data helpers
_b120 = {}


def bars120(sym):
    """120-min bars = session-aligned 2-hour groups of the v3 60-min bars (bucket = hours since 18:00 // 2, inside
    one session and one contract). O first, H max, L min, C last, V sum, vwap = vwap of the last 60-min bar (the
    session VWAP at the 2-hour bar's last minute, as signals.py:55). EMA/Momentum/swings: signals.context."""
    if sym in _b120:
        return _b120[sym]
    b = bars(sym, 60)
    hs = ((b.index.hour - 18) % 24) // 2
    key = [b.sess.to_numpy(), b.inst.to_numpy(), hs.to_numpy()]
    g = b.assign(ts=b.index).groupby(key, sort=False)
    o = g.agg(ts=("ts", "first"), O=("O", "first"), H=("H", "max"), L=("L", "min"), C=("C", "last"),
              V=("V", "sum"), vwap=("vwap", "last"), sess=("sess", "first"), inst=("inst", "first"))
    o = o.set_index("ts").sort_index()
    o.index.name = "ts"
    o["seg"] = (o.sess.ne(o.sess.shift()) | o.inst.ne(o.inst.shift())).cumsum()
    o["run"] = o.inst.ne(o.inst.shift()).cumsum()
    c = sg.context(o, tick=TICK[sym])
    for k in ("ema8", "ema20", "ema50", "mom14", "trend"):
        o[k] = c[k]
    assert o.index.max() < HOLDOUT
    _b120[sym] = o
    return o


def slice_1m(example_id, sym):
    """1-minute slice of one example with session VWAP (signals.py:46-48) and EMA/Momentum (signals.py:92-105)."""
    m = pd.read_parquet(os.path.join(SLICES, f"{example_id}_1m.parquet"))
    assert m.index.max() < HOLDOUT
    tp = (m.H + m.L + m.C) / 3
    key = [m.sess, m.inst]
    m["vwap"] = (tp * m.V).groupby(key, sort=False).cumsum() / m.V.groupby(key, sort=False).cumsum().replace(0, np.nan)
    m["seg"] = (m.sess.ne(m.sess.shift()) | m.inst.ne(m.inst.shift())).cumsum()
    m["run"] = m.inst.ne(m.inst.shift()).cumsum()
    c = sg.context(m, tick=TICK[sym])
    for k in ("ema8", "ema20", "ema50", "mom14", "trend"):
        m[k] = c[k]
    return m


def tf_bars(sym, tf, example_id=None):
    if tf == 1:
        return slice_1m(example_id, sym)
    if tf == 120:
        return bars120(sym)
    return bars(sym, tf)


def window(B, tf, decision, extend_to=None):
    before, after = WIN[tf]
    if extend_to is not None and tf > 1:
        after = min(max(after, extend_to - decision + pd.Timedelta(minutes=tf)), AFTER_CAP[tf])
    lo, hi = decision - before, min(decision + after, HOLDOUT)
    return B[(B.index >= lo) & (B.index < hi)]


class XMap:
    """maps a timestamp to a fractional x position on a panel whose bars are drawn at 0, 1, 2, ... (bar START times).
    A time inside bar i maps to i - 0.5 + (time - start)/tf; a time in a closed-market gap maps to the end of the
    previous bar."""

    def __init__(self, idx, tf):
        self.st = idx.to_numpy()
        self.tf = tf

    def __call__(self, ts):
        ts = np.datetime64(pd.Timestamp(ts))
        i = int(np.searchsorted(self.st, ts, side="right")) - 1
        if i < 0:   # before the window: not drawn
            return float("nan")
        if ts >= self.st[-1] + np.timedelta64(self.tf, "m"):   # after the window ends: not drawn (no clamping)
            return float("nan")
        frac = (ts - self.st[i]) / np.timedelta64(self.tf, "m")
        return i - 0.5 + float(min(max(frac, 0.0), 1.0))

    def i(self, ts):
        return int(np.searchsorted(self.st, np.datetime64(pd.Timestamp(ts)), side="right")) - 1


def fp(sym, v):
    return cs.fp(sym, v)


# ============================================================================================ one panel
def draw_panel(ax, axm, B, tf, sym, decision, trade, used_note, used=True):
    """B = window bars (O H L C vwap sess run ema8 ema20 ema50 mom14). Returns the XMap."""
    for a in (ax, axm):
        style_ax(a)
        a.tick_params(labelsize=12)
    n = len(B)
    x = np.arange(n)
    X = XMap(B.index, tf)
    O, Hh, L, C = (B[c].to_numpy() for c in "OHLC")
    rr = np.nanmax(Hh) - np.nanmin(L)
    col = np.where(C >= O, cs.UP, cs.DN)
    wid = 0.62 if n < 150 else 0.7
    ax.vlines(x, L, Hh, color=col, linewidth=1.1 if n < 150 else 0.8, zorder=3)
    ax.bar(x, np.where(np.abs(C - O) > 0, C - O, rr * 0.003), bottom=O, width=wid, color=col, edgecolor="none", zorder=3)
    for e, st in cs.EMA_STYLE.items():
        ax.plot(x, B[f"ema{e}"].to_numpy(), color=st["color"], linewidth=st["lw"], linestyle=(0, (5, 3)), zorder=2,
                label=f"EMA {e}")
    sess = B.sess.to_numpy()
    run = B.run.to_numpy()
    br = np.flatnonzero((sess[1:] != sess[:-1]) | (run[1:] != run[:-1])) + 1
    ax.plot(np.insert(x.astype(float), br, np.nan), np.insert(B.vwap.to_numpy(), br, np.nan), color=cs.VWAP_COL,
            lw=1.5, zorder=2, label="session VWAP (from 18:00 ET)")
    sm = pd.Series(sess)
    hod = pd.Series(Hh).groupby(sm).cummax().to_numpy()
    lod = pd.Series(L).groupby(sm).cummin().to_numpy()
    ax.plot(np.insert(x.astype(float), br, np.nan), np.insert(hod, br, np.nan), color="#ffffff", lw=1.0, alpha=0.6,
            ls=(0, (1, 2)), drawstyle="steps-mid", label="session high / low so far")
    ax.plot(np.insert(x.astype(float), br, np.nan), np.insert(lod, br, np.nan), color="#ffffff", lw=1.0, alpha=0.6,
            ls=(0, (1, 2)), drawstyle="steps-mid")
    for j in br:
        newrun = run[j] != run[j - 1]
        for a in (ax, axm):
            a.axvline(j - 0.5, color="#ff9900" if newrun else "#555555", lw=1.4 if newrun else 0.8, ls=(0, (2, 3)), zorder=1)
        if newrun:
            ax.text(j - 0.4, 0.5, " contract roll:\n EMAs restart", transform=ax.get_xaxis_transform(), color="#ff9900",
                    fontsize=11)
    if tf <= 15:
        for j in br:
            if run[j] == run[j - 1] and n < 400:
                ax.text(j - 0.4, 0.99, " 18:00 new session", transform=ax.get_xaxis_transform(), color=cs.TXT2,
                        fontsize=10.5, va="top")
    # swings: 3-bar fractals (signals.py:64-79); known at the close of pivot+3
    lo_p, hi_p = sg.pivots(B, 3)
    st = B.index
    dec = pd.Timestamp(decision)
    for piv, yv, colr, mk, off in ((lo_p, L, SWL, "^", -1), (hi_p, Hh, SWH, "v", 1)):
        for p in np.flatnonzero(piv):
            known = st[p + 3] + pd.Timedelta(minutes=tf)
            conf = known <= dec
            y = yv[p] + off * rr * 0.025
            ax.plot(p, y, marker=mk, ms=9 if n < 200 else 7, color=colr, mfc=colr if conf else "none", zorder=6, ls="none")
            if conf:
                ax.plot([p, p + 3], [y, y], color=colr, lw=1.0, ls=":", zorder=5)
                ax.plot(p + 3, y, marker="o", ms=3.5, color=colr, zorder=6)
    ax.plot([], [], marker="^", color=SWL, ls=":", label="swing low: pivot ... known 3 bars later (o)")
    ax.plot([], [], marker="v", color=SWH, ls=":", label="swing high (hollow = not yet confirmed at decision)")
    # decision line + dimmed future
    xd = X(dec)
    ax.axvspan(xd, n + 5, color=DIM, alpha=0.55, zorder=4, lw=0)
    axm.axvspan(xd, n + 5, color=DIM, alpha=0.55, zorder=4, lw=0)
    for a in (ax, axm):
        a.axvline(xd, color=cs.HILITE, lw=2.0, zorder=7)
    ax.text(xd, 1.005, "decision", transform=ax.get_xaxis_transform(), color=cs.HILITE, fontsize=13, ha="center",
            va="bottom", fontweight="bold")
    if xd < n - 0.6:
        ax.text(xd + 0.6, 0.965, "what happened next\n(not known at decision)", transform=ax.get_xaxis_transform(),
                color="#9fb3ff", fontsize=12, va="top", zorder=8)
    i_dec = X.i(dec)
    if 0 <= i_dec < n and dec > st[i_dec] and dec < st[i_dec] + pd.Timedelta(minutes=tf):
        ax.text(0.995, 0.02, f"the {tf}-min bar cut by the line was still forming at the decision:\n"
                "systems only read CLOSED bars", transform=ax.transAxes, color="#9fb3ff", fontsize=10.5, ha="right",
                va="bottom", zorder=9)
    # trade marks
    ys = [np.nanmin(L), np.nanmax(Hh)]
    if trade:
        d = trade["side"]
        xe = X(trade["entry_time"]) if trade.get("entry_time") is not None else None
        xx = X(trade["exit_time"]) if trade.get("exit_time") is not None else None
        inwin = lambda xv: xv is not None and -0.5 <= xv <= n - 0.5  # noqa: E731
        if trade.get("stop") is not None and np.isfinite(trade["stop"]) and inwin(xe):
            x1 = xx if inwin(xx) else n - 0.5
            ax.hlines(trade["stop"], xe, x1, color=cs.BAD, lw=2.0, zorder=8)
            ax.text(xe, trade["stop"], f" STOP {fp(sym, trade['stop'])}", color=cs.BAD, fontsize=11, va="top" if d > 0 else "bottom",
                    zorder=9, fontweight="bold")
            ys.append(trade["stop"])
        if inwin(xe):
            ax.plot(xe, trade["entry_px"], marker=">", color=cs.HILITE, ms=14, mec="#000000", zorder=10)
            ax.annotate(f"ENTRY {'LONG' if d > 0 else 'SHORT'} {fp(sym, trade['entry_px'])}", (xe, trade["entry_px"]),
                        xytext=(-12, 28 if d < 0 else -28), textcoords="offset points", ha="right", color=cs.HILITE,
                        fontsize=11.5, fontweight="bold", zorder=11, va="center",
                        bbox=dict(boxstyle="round,pad=0.2", fc="#111111", ec=cs.HILITE, lw=0.8, alpha=0.9))
            ys.append(trade["entry_px"])
        if inwin(xx) and trade.get("exit_px") is not None:
            pc = cs.GOOD if trade["pnl"] > 0 else cs.BAD
            ax.plot(xx, trade["exit_px"], marker="X", color="#ffffff", mec=pc, mew=1.5, ms=14, zorder=10)
            ax.annotate(f"EXIT {fp(sym, trade['exit_px'])}  {trade['pnl']:+.2f} $", (xx, trade["exit_px"]),
                        xytext=(-14, -30 if d > 0 else 30), textcoords="offset points", ha="right", color=pc,
                        fontsize=11.5, fontweight="bold", zorder=11, va="center",
                        bbox=dict(boxstyle="round,pad=0.2", fc="#111111", ec=pc, lw=0.8, alpha=0.9))
            ys.append(trade["exit_px"])
        for mk in trade.get("extra", []):          # e.g. A1 reversals: dict(time, px, label, color)
            xm = X(mk["time"])
            if inwin(xm):
                ax.plot(xm, mk["px"], marker=mk.get("marker", "D"), color=mk.get("color", cs.EXITC), ms=10, zorder=10,
                        mec="#000000")
                ys.append(mk["px"])
    lo_, hi_ = np.nanmin(ys), np.nanmax(ys)
    span = hi_ - lo_
    ax.set_ylim(lo_ - span * 0.10, hi_ + span * 0.16)
    ax.set_xlim(-1, n + max(2, 0.015 * n))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fp(sym, v)))
    ax.tick_params(labelbottom=False)
    # momentum strip
    mom = B.mom14.to_numpy()
    axm.plot(x, mom, color=cs.MOM_COL, lw=1.4)
    axm.axhline(100, color="#777777", lw=0.9, ls=(0, (3, 3)))
    axm.text(0.003, 0.9, "Momentum(14) = 100 x close / close 14 bars ago", transform=axm.transAxes, color=cs.TXT2,
             fontsize=10.5, va="top")
    fm = np.isfinite(mom)
    if fm.any():
        lo_m, hi_m = np.nanmin(mom), np.nanmax(mom)
        pad = (hi_m - lo_m) * 0.1 + 1e-3
        axm.set_ylim(min(lo_m, 100) - pad, max(hi_m, 100) + pad)
    axm.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.2f}"))
    axm.tick_params(labelsize=10)
    time_ticks(axm, B.index, nt=9, fs=11)
    tcol = cs.HILITE if used else cs.TXT2
    ax.set_title(f"{tf}-MIN" + ("" if tf < 60 else f" ({tf // 60} h)") + f"  |  {used_note}", loc="left", color=tcol,
                 fontsize=14.5, fontweight="bold", pad=16)
    return X


def mtf_figure(path, ex_id, sym, decision, trade, title, subtitle, used, overlays=None, extend_to=None,
               panel_notes=None):
    """used: {tf: (bool used, note)}; overlays: {tf: fn(ax, axm, B, X)}; panel_notes: {tf: text in the panel corner}."""
    overlays = overlays or {}
    panel_notes = panel_notes or {}
    tfs = (1, 5, 15, 60, 120)
    fig = plt.figure(figsize=(FIG_W, 31), facecolor=cs.BG)
    outer = fig.add_gridspec(5, 1, hspace=0.30, left=0.03, right=0.93, top=0.928, bottom=0.025)
    fig.text(0.015, 0.993, title, color=cs.TXT, fontsize=19, fontweight="bold", va="top")
    import textwrap
    fig.text(0.015, 0.981, "\n".join(textwrap.wrap(subtitle, 150)[:2]), color=cs.TXT2, fontsize=12.5, va="top",
             linespacing=1.25)
    fig.text(0.015, 0.964, "Bar times = bar START (NinjaTrader shows the END). VWAP and session high/low start at "
             "18:00 ET (Globex day). Dimmed area = after the decision.", color=cs.TXT2, fontsize=12, va="top")
    handles = None
    for r, tf in enumerate(tfs):
        g = outer[r].subgridspec(2, 1, height_ratios=[4.0, 1.0], hspace=0.03)
        ax = fig.add_subplot(g[0])
        axm = fig.add_subplot(g[1], sharex=ax)
        B = window(tf_bars(sym, tf, ex_id), tf, decision, extend_to)
        u, note = used.get(tf, (False, "not used by this system (context only)"))
        X = draw_panel(ax, axm, B, tf, sym, decision, trade, note, used=u)
        if tf in overlays:
            overlays[tf](ax, axm, B, X)
        if tf in panel_notes:
            ax.text(0.003, 0.02, panel_notes[tf], transform=ax.transAxes, color=cs.TXT, fontsize=11.5, va="bottom",
                    zorder=12, bbox=dict(fc="#0b0b0b", ec="#444444", boxstyle="round,pad=0.3", alpha=0.92))
        if handles is None:
            handles = ax.get_legend_handles_labels()
    lg = fig.legend(*handles, loc="upper left", bbox_to_anchor=(0.012, 0.958), ncol=max(4, (len(handles[0]) + 1) // 2),
                    fontsize=11.5 if len(handles[0]) <= 8 else 10.2, columnspacing=1.0, frameon=False)
    for t in lg.get_texts():
        t.set_color(cs.TXT)
    fig.savefig(path, dpi=DPI, facecolor=cs.BG)
    plt.close(fig)
    return path


# ============================================================================================ decision card
RD_COL = {"agrees": cs.GOOD, "against": cs.BAD, "neutral": cs.TXT2, "info": "#9fb3ff", "fired": cs.HILITE}


def _conv(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        return None if not np.isfinite(v) else round(float(v), 4)
    if isinstance(v, (pd.Timestamp, np.datetime64)):
        return str(pd.Timestamp(v))
    if isinstance(v, dict):
        return {k: _conv(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_conv(x) for x in v]
    return v


def decision_card(path_png, card):
    """card: dict(title, decision (rule/score line), drivers [str], outcome, why, inputs [dict(plain, value, read,
    where)], notes [str]). read in agrees / against / neutral / info / fired. Writes PNG + JSON (same stem)."""
    import textwrap
    wrapw = lambda t, fs: "\n".join(textwrap.wrap(t, int(1950 / fs), subsequent_indent="    "))  # noqa: E731
    card = dict(card)
    card["drivers"] = [wrapw(d_, 13) for d_ in card.get("drivers", [])]
    card["why"] = wrapw(card["why"], 13.5)
    card["notes"] = [wrapw(n_, 11.5) for n_ in card.get("notes", [])]
    inp = card["inputs"]
    ncol = 2 if len(inp) > 22 else 1
    per = int(np.ceil(len(inp) / ncol))
    nl = lambda t: 1 + t.count("\n")  # noqa: E731
    head = (2 + sum(nl(d_) for d_ in card["drivers"]) + 3 + nl(card["why"]) + sum(nl(n_) for n_ in card["notes"])
            + nl(card["decision"]))
    h = 1.2 + 0.36 * (head + per + 2)
    fig = plt.figure(figsize=(FIG_W, h), facecolor=cs.BG)
    yy = [1 - 0.25 / h]
    lh = 0.36 / h

    def line(txt, color=cs.TXT, fs=13.5, bold=False, x=0.012, family=None):
        fig.text(x, yy[0], txt, color=color, fontsize=fs, va="top", fontweight="bold" if bold else "normal",
                 family=family)
        yy[0] -= lh * (fs / 13.5) * (1 + txt.count("\n"))

    line(card["title"], fs=18, bold=True)
    line(card["decision"], color=cs.HILITE, fs=15, bold=True)
    line("WHAT DROVE IT MOST:", color=cs.TXT, fs=13.5, bold=True)
    for d_ in card.get("drivers", []):
        line("  - " + d_, fs=13)
    line(card["outcome"], color=cs.GOOD if card.get("win") else cs.BAD, fs=15, bold=True)
    line("WHY: " + card["why"], fs=13.5)
    for n_ in card.get("notes", []):
        line(n_, color=cs.TXT2, fs=11.5)
    line("EVERY INPUT READ AT THE DECISION  (green = agrees with the trade, red = against, grey = neutral, "
         "blue = information only, yellow = rule fired)", color=cs.TXT, fs=12.5, bold=True)
    y0 = yy[0]
    cw = 0.985 / ncol
    for c in range(ncol):
        for k, r in enumerate(inp[c * per:(c + 1) * per]):
            y = y0 - k * lh
            colr = RD_COL.get(r["read"], cs.TXT)
            v = r["value"]
            vs = v if isinstance(v, str) else ("NaN" if v is None or not np.isfinite(v) else
                                               (f"{v:+.2f}" if abs(v) < 1000 else f"{v:,.2f}"))
            fig.text(0.012 + c * cw, y, r["plain"][:46 if ncol == 2 else 86], color=cs.TXT, fontsize=11.8, va="top")
            fig.text(0.012 + c * cw + (0.335 if ncol == 2 else 0.55), y, vs, color=colr, fontsize=11.8, va="top",
                     ha="right", family="DejaVu Sans Mono")
            fig.text(0.012 + c * cw + (0.342 if ncol == 2 else 0.56), y, r["read"], color=colr, fontsize=11.5, va="top")
            if ncol == 1 and r.get("where"):
                fig.text(0.68, y, r["where"][:48], color=cs.TXT2, fontsize=10.5, va="top")
    fig.savefig(path_png, dpi=DPI, facecolor=cs.BG)
    plt.close(fig)
    with open(os.path.splitext(path_png)[0] + ".json", "w") as f:
        json.dump(_conv(card), f, indent=1, default=str)
    return path_png


def reading(v, kind="s"):
    """plain reading of a with-the-trade signed value: 's' sign, 'neg' bigger = worse, 'room' room-to-run (R20),
    'flag' rule, 'info' none."""
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "neutral"
    if kind == "s":
        return "agrees" if v > 0.05 else ("against" if v < -0.05 else "neutral")
    if kind == "neg":
        return "against" if v > 0 else "neutral"
    if kind == "room":
        return "agrees" if v > 0.25 else "against"
    if kind == "flag":
        return "fired" if v > 0 else "neutral"
    return "info"
