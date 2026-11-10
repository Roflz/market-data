"""
Pullback gallery: random real pullbacks (fixed seed), bullish and bearish, each drawn as one big chart with the impulse
leg, Fibonacci retracement lines, the pullback low, the event bar, patterns, Momentum(14), volume, a stats box and what
happened next. Also a summary table over ALL detected pullbacks per market / timeframe and a CSV per market / timeframe.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:. python3 pullback_gallery.py [k_leg]      (k_leg 3, 5, 10; default 5)
Writes pullbacks/ (k_leg 5) or pullbacks_k{k}/: index.html, pullbacks_N.html, img/*.jpg; out/pullbacks_{SYM}_{TF}[_k{k}].csv
"""
import base64
import html
import os
import sys
import textwrap
import warnings

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse

import chart_style as cs
import exits as ex
import pullbacks as pb
import signals as sg

warnings.filterwarnings("ignore", category=RuntimeWarning)
K = int(sys.argv[1]) if len(sys.argv) > 1 else 5
SUF = "" if K == 5 else f"_k{K}"
OUT = "pullbacks" + SUF
IMG = f"{OUT}/img"
os.makedirs(IMG, exist_ok=True); os.makedirs("out", exist_ok=True)
PLAN = [("NQ", 5, 6), ("NQ", 15, 6), ("NQ", 60, 6), ("ES", 15, 4), ("YM", 15, 4)]   # (market, TF, examples per side)
BEFORE, AFTER = 25, 25
PAGE_BYTES = 1_800_000
FIB_LEVELS = (0, 0.236, 0.382, 0.5, 0.618, 0.786, 1)
ABBR = {"doji": "Dj", "dragonfly_doji": "DfDj", "gravestone_doji": "GvDj", "hammer": "Ham", "hanging_man": "HgM",
        "inverted_hammer": "IHam", "shooting_star": "SStar", "marubozu": "Maru", "spinning_top": "Spin",
        "engulfing": "Eng", "harami": "Har", "piercing": "Pierce", "dark_cloud": "DkCl", "morning_evening_star": "Star",
        "three_soldiers_crows": "3S/3C", "three_inside": "3In", "inside_bar": "IB", "outside_bar": "OB", "pin_bar": "Pin",
        "nr7": "NR7", "tweezer": "Twz", "inside_bar_breakout": "IB-brk", "nr7_breakout": "NR7-brk",
        "clv_extreme": "CLV", "bar_80_20": "80/20", "tall_trend_bar": "Tall", "five_lower_lows_higher_highs": "5LL/5HH",
        "clv5_extreme": "CLV5"}
OUTCOME_COL = {"continuation": "#1baf7a", "failure": "#e34948", "neither": "#898781", "no_time": "#898781"}
rng = np.random.default_rng(11)
LEG_BUCKETS = [(0, 50, "< $50"), (50, 100, "$50-100"), (100, 200, "$100-200"), (200, 500, "$200-500"), (500, np.inf, ">= $500")]


def fp(sym, x):
    return f"{x:,.0f}" if sym == "YM" else f"{x:,.2f}"


def sgn(x, dec=2):
    return f"{x:+,.{dec}f}"


def outcome_text(r, micro):
    if r.outcome == "continuation":
        s = f"CONTINUATION: went past the leg's {'high' if r.direction > 0 else 'low'} (SH) after {int(r.bars_to_outcome)} bars"
    elif r.outcome == "failure":
        s = f"FAILURE: closed beyond the pullback {'low' if r.direction > 0 else 'high'} (PL) after {int(r.bars_to_outcome)} bars"
    elif r.outcome == "neither":
        s = f"NEITHER within {int(r.n_window)} bars"
    else:
        s = "no bars left before 16:45"
    return s


def stats_text(sym, tf, r, P):
    usd = sg.SPEC[sym]["usd"]; micro = sg.SPEC[sym]["micro"]
    d = r.direction
    lo_w, hi_w = ("low", "high") if d > 0 else ("high", "low")
    dec = 0 if sym == "YM" else 2
    def pts(x):
        return f"{x:,.{dec}f} pts = ${x * usd:,.2f}"
    def line_dist(x):
        if not np.isfinite(x):
            return "n/a"
        return f"{abs(x):,.{dec}f} pts {'short of it' if x > 0 else 'through it'}"
    with_, against, minor = [], [], 0
    for tok in r.patterns.split():
        nm = tok.rstrip("+-")
        if nm in pb.FREQUENT:
            minor += 1; continue
        (with_ if tok.endswith("+") else against if tok.endswith("-") else with_).append(nm.replace("_", " "))
    fibd = r.fib_dist_pts
    L = [f"{'BULLISH' if d > 0 else 'BEARISH'} PULLBACK  {micro} {tf}-min",
         f"Event {r.t_event:%Y-%m-%d %H:%M} ET",
         f"  ({r.tod})",
         "",
         "IMPULSE LEG",
         f" Start swing {lo_w} SL {fp(sym, r.SL)}",
         f"   {r.t_SL:%m-%d %H:%M}",
         f" End swing {hi_w} SH  {fp(sym, r.SH)}",
         f"   {r.t_SH:%m-%d %H:%M}",
         f" Leg {pts(r.leg_pts)}",
         f" {r.bars_impulse} bars",
         "PULLBACK",
         f" Pullback {lo_w} PL {fp(sym, r.PL)}",
         f"   {r.t_PL:%m-%d %H:%M}",
         f" Gave back {pts(r.pb_pts)}",
         f" Depth {r.depth:.2f} of the leg",
         f" Nearest Fib {r.fib_near}: {abs(fibd):,.{dec}f} pts",
         f"   {'deeper' if fibd > 0 else 'shallower'} than the line",
         f" {r.bars_pullback} bars; avg volume {r.vol_ratio:.2f}x",
         "   the leg's avg volume",
         f"PL vs lines (at the PL bar)",
         f" EMA20: {line_dist(r.PL_to_ema20)}",
         f" EMA50: {line_dist(r.PL_to_ema50)}",
         f" VWAP:  {line_dist(r.PL_to_vwap)}",
         "MOMENTUM(14)",
         f" SL {r.mom_SL:.2f}  SH {r.mom_SH:.2f}  PL {r.mom_PL:.2f}",
         f" Hidden divergence: {'YES' if r.divergence else 'no'}",
         f"   (PL momentum {'beyond' if r.divergence else 'not beyond'} SL's)",
         f"Trend at event: {'still ' + ('up' if d > 0 else 'down') if r.trend_still else 'no longer ' + ('up' if d > 0 else 'down')}",
         "PATTERNS PL-2..event"]
    L += textwrap.wrap(" with: " + (", ".join(with_) or "none"), 34, subsequent_indent="   ")
    L += textwrap.wrap(" against: " + (", ".join(against) or "none"), 34, subsequent_indent="   ")
    L.append(f" + {minor} frequent minor ones")
    L.append(f"At event: {r.to_SH_pts:,.{dec}f} pts to SH,")
    L.append(f"   {r.to_PL_pts:,.{dec}f} pts to PL")
    L += ["", "WHAT HAPPENED NEXT", f" from the event close {fp(sym, r.event_close)}"]
    L += textwrap.wrap(" " + outcome_text(r, micro), 34, subsequent_indent="   ")
    if r.n_window > 0:
        L += [f" Best  {sgn(r.mfe_pts, dec)} pts (${r.mfe_usd:,.2f})",
              f" Worst {sgn(-r.mae_pts, dec)} pts (-${r.mae_usd:,.2f})",
              f" Window end {sgn(r.end_pts, dec)} pts (${r.end_usd:+,.2f})",
              f" Window: {int(r.n_window)} bars"]
    L.append(f" $ per 1 {micro} contract")
    return "\n".join(L)


# palette (light surface): candles, lines, accents
UP, DN = "#2e9d6b", "#d8574f"
INK, INK2, INK3, GRID = "#1f1e1c", "#55534e", "#8a8780", "#ecebe7"
EMA_COL = {8: "#c9c6bd", 20: "#e39a26", 50: "#3b73c4"}
VWAP_COL = "#9a6fc1"
ACC = "#6a3fb5"                      # pullback point / setup
OUT_COL = {"continuation": "#2e9d6b", "failure": "#d8574f", "neither": "#8a8780", "no_time": "#8a8780"}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": "#d6d4ce", "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK})



# ------------------------------------------------------------------------------------------- trade from each setup
EXIT_RULES = [("opp_classic", "Opposite candle pattern"), ("opp_classic_at_level", "Opposite pattern at a swing level"),
              ("choch_5", "Close past the last 5-bar swing (CHoCH)"), ("ema20_cross", "Close back through EMA 20"),
              ("mom_cross100", "Momentum back through 100")]
TRADES = {}


def prep_exits(b, c, p, tf, tick):
    """bar-level exit conditions (for longs, for shorts), as next-occurrence arrays, plus what the trade needs."""
    O, H, L, C = (b[x].to_numpy() for x in "OHLC")
    run = b.run.to_numpy(); n = len(b)
    allowed, forced = ex.session_frame(b, tf)
    P = {k: p[k].to_numpy() for k in ex.DIRECTIONAL}
    lo5, hi5 = sg.pivots(b, 5)
    clo = np.full(n, np.nan); chi = np.full(n, np.nan)
    q = np.flatnonzero(lo5); clo[q + 5] = L[q]; q = np.flatnonzero(hi5); chi[q + 5] = H[q]
    sl5 = pd.Series(clo).groupby(run).ffill().to_numpy(); sh5 = pd.Series(chi).groupby(run).ffill().to_numpy()
    ema20, mom, atr = c.ema20.to_numpy(), c.mom14.to_numpy(), c.atr14.to_numpy()
    cb = sum((P[k] == -1).astype(np.int16) for k in ex.CLASSIC); cu = sum((P[k] == 1).astype(np.int16) for k in ex.CLASSIC)
    with np.errstate(invalid="ignore"):
        cond = {"opp_classic": (cb >= 1, cu >= 1),
                "opp_classic_at_level": ((cb >= 1) & (H >= sh5 - 0.5 * atr), (cu >= 1) & (L <= sl5 + 0.5 * atr)),
                "choch_5": (ex.fresh(C < sl5), ex.fresh(C > sh5)),
                "ema20_cross": (ex.fresh(C < ema20), ex.fresh(C > ema20)),
                "mom_cross100": (ex.fresh(mom < 100), ex.fresh(mom > 100))}
    nxt = {k: (ex.next_true(a_), ex.next_true(z_)) for k, (a_, z_) in cond.items()}
    return dict(O=O, H=H, L=L, C=C, allowed=allowed, forced=forced, P=P, sl5=sl5, sh5=sh5, ema20=ema20, mom=mom,
                nxt=nxt, tick=tick, seg=b.seg.to_numpy())


def exit_text(rule, j, d, D, sym):
    want = -d
    if rule in ("opp_classic", "opp_classic_at_level"):
        t = " + ".join(cs.pname(k, want) for k in ex.CLASSIC if D["P"][k][j] == want)
        if rule == "opp_classic_at_level":
            t += f" at swing {'high' if d > 0 else 'low'} {cs.fp(sym, D['sh5'][j] if d > 0 else D['sl5'][j])}"
        return t
    if rule == "choch_5":
        return (f"close {cs.fp(sym, D['C'][j])} {'below' if d > 0 else 'above'} swing {'low' if d > 0 else 'high'} "
                f"{cs.fp(sym, D['sl5'][j] if d > 0 else D['sh5'][j])}")
    if rule == "ema20_cross":
        return f"close {cs.fp(sym, D['C'][j])} {'below' if d > 0 else 'above'} EMA 20 ({cs.fp(sym, D['ema20'][j])})"
    return f"Momentum {D['mom'][j]:.2f} crossed {'below' if d > 0 else 'above'} 100"


def sim_trades(sym, D, r):
    """Enter at the open of the bar after the setup is known, stop 1 tick past the pullback point; exit by each rule."""
    d = int(r.direction); ev = int(r.i_event); e = ev + 1
    if e >= len(D["O"]) or D["seg"][e] != D["seg"][ev] or not D["allowed"][e] or D["forced"][e] < e:
        return None
    spec = sg.SPEC[sym]
    stop = r.PL - d * D["tick"]
    out = dict(e=e, entry=D["O"][e], stop=stop, d=d, rules=[])
    for k, (rule, label) in enumerate(EXIT_RULES, 1):
        nb, nu = D["nxt"][rule]
        x_end, x_px, sig = ex.plan_exits(np.array([e]), np.array([d]), D["forced"], nb, nu, D["O"], D["C"])
        px, xb, how, mfe = ex.simulate(D["O"], D["H"], D["L"], D["C"], np.array([e]), np.array([d]), x_end, x_px,
                                       np.array([stop]))
        how, j = int(how[0]), int(x_end[0])
        if how == 1:
            kind, fill, sig_bar, txt = "stop", int(xb[0]), None, "stop hit (1 tick past the pullback point)"
        elif sig[0] == 1:
            kind, fill, sig_bar, txt = "signal", j + 1, j, exit_text(rule, j, d, D, sym)
        else:
            kind, fill, sig_bar, txt = "1645", j, None, "no exit signal: closed at 16:45 ET"
        pnl = d * (px[0] - out["entry"]) * spec["usd"] - spec["cost"]
        out["rules"].append(dict(k=k, rule=rule, label=label, kind=kind, fill=fill, sig_bar=sig_bar, px=px[0], txt=txt,
                                 pnl=pnl, bars=fill - e))
    return out


def draw(sym, tf, D, r, path):
    b, c = D["b"], D["c"]
    d = r.direction
    sl, sh, pl, ev = int(r.i_SL), int(r.i_SH), int(r.i_PL), int(r.i_event)
    tr = sim_trades(sym, D, r); TRADES[path] = tr
    last = max([t["fill"] for t in tr["rules"]], default=ev) if tr else ev
    a = max(0, sl - 15); z = min(len(b), max(ev + int(max(r.n_window, 10)) + 4, last + 6), sl - 15 + 190)
    B = b.iloc[a:z]; Cx = c.iloc[a:z]
    fig, ax, axm = cs.new_figure()
    x, O, H, L, C = cs.draw_base(ax, axm, B, Cx, sym)
    n = len(B); rr = np.nanmax(H) - np.nanmin(L); lo_v, hi_v = np.nanmin(L), np.nanmax(H)
    s_, h_, p_, e_ = sl - a, sh - a, pl - a, ev - a
    end_word = "high" if d > 0 else "low"; pb_word = "low" if d > 0 else "high"
    for axx in (ax, axm):
        axx.axvspan(e_ + 0.5, n - 0.5, color="#1b2a3a", alpha=0.5, zorder=0, lw=0)
        axx.axvline(e_ + 0.5, color="#e6e6e6", linewidth=1.1, zorder=4)
    ax.text(e_ + 0.7, hi_v + rr * 0.14, "setup known \u2192 what happened next", color="#e6e6e6", fontsize=10.5, va="center")
    # Fibonacci 38.2 / 50 / 61.8 of the leg, leg end (continuation level) and pullback point (failure level)
    for f in (0.382, 0.5, 0.618):
        y = r.SH + f * (r.SL - r.SH)
        ax.hlines(y, h_, n - 0.5, color="#8c8c8c", linewidth=0.9, linestyles=(0, (4, 3)), zorder=1)
    ax.hlines(r.SH, h_, n - 0.5, color="#e6e6e6", linewidth=1.1, zorder=1)
    ax.hlines(r.PL, p_, n - 0.5, color=cs.HILITE, linewidth=1.1, linestyles=(0, (6, 3)), zorder=1)
    labs = [(r.SH, f"leg {end_word}", "#e6e6e6"), (r.PL, f"pullback {pb_word}", cs.HILITE)]
    labs += [(r.SH + f * (r.SL - r.SH), f"fib {f * 100:.1f}%", "#a0a0a0") for f in (0.382, 0.5, 0.618)]
    labs.sort(key=lambda t: t[0]); gap = rr * 1.3 * 0.045; ys = []
    for y, _, _ in labs:
        ys.append(max(y, ys[-1] + gap) if ys else y)
    shift = max(0.0, ys[-1] - labs[-1][0]) / 2
    for (y, t, cl), yl in zip(labs, ys):
        ax.annotate(t, xy=(n - 0.6, y), xytext=(n - 1.0, yl - shift), fontsize=9.5, color=cl, va="center", ha="right",
                    zorder=12, bbox=dict(boxstyle="round,pad=0.15", fc="#000000", ec="none", alpha=0.8))
    # impulse leg arrow and key points
    ax.annotate("", xy=(h_, r.SH), xytext=(s_, r.SL),
                arrowprops=dict(arrowstyle="-|>", color="#e6e6e6", lw=2.2, alpha=0.7, mutation_scale=18), zorder=5)
    for xi, y, txt, cl, below in ((s_, r.SL, f"leg start {cs.fp(sym, r.SL)}", "#e6e6e6", d > 0),
                                  (h_, r.SH, f"leg {end_word} {cs.fp(sym, r.SH)}", "#e6e6e6", d < 0),
                                  (p_, r.PL, f"pullback {pb_word} {cs.fp(sym, r.PL)}", cs.HILITE, d > 0)):
        ax.scatter([xi], [y], s=60, color=cl, edgecolor="black", zorder=9)
        cs.label(ax, xi, y, txt, cl, above=not below)
    ax.scatter([p_], [r.PL], s=520, facecolor="none", edgecolor=cs.HILITE, linewidth=2, zorder=8)
    if r.outcome in ("continuation", "failure") and np.isfinite(r.i_outcome):
        oi = int(r.i_outcome) - a
        if 0 <= oi < n:
            ok = r.outcome == "continuation"
            oc = cs.GOOD if ok else cs.BAD
            y = r.SH if ok else C[oi]
            ax.scatter([oi], [y], s=130, marker="o" if ok else "X", color=oc, edgecolor="black", zorder=10)
            txt = (f"reached leg {end_word} after {int(r.bars_to_outcome)} bars" if ok
                   else f"closed past pullback {pb_word} after {int(r.bars_to_outcome)} bars")
            right = oi > 0.6 * n
            ax.annotate(txt, (oi, y), xytext=(-10 if right else 10, 16 if ok == (d > 0) else -16),
                        textcoords="offset points", ha="right" if right else "left",
                        va="bottom" if ok == (d > 0) else "top", fontsize=10.5, color=oc, fontweight="bold", zorder=12,
                        bbox=dict(boxstyle="round,pad=0.25", fc="#0a0a0a", ec=oc, lw=0.9))
    if tr:
        n_ = len(B); e0 = tr["e"] - a
        ax.scatter([e0], [tr["entry"]], marker="^" if d > 0 else "v", s=150, color=cs.HILITE, edgecolor="black", zorder=11)
        ax.annotate("entry", (e0, tr["entry"]), xytext=(-8, 0), textcoords="offset points", ha="right", va="center",
                    color=cs.HILITE, fontsize=10, fontweight="bold", zorder=12)
        ax.hlines(tr["stop"], e0, n_ - 0.5, color=cs.BAD, linewidth=1.1, linestyles=(0, (1, 2)), zorder=2)
        # group rules that exit on the same bar
        groups = {}
        for t in tr["rules"]:
            groups.setdefault((t["kind"], t["fill"], t["sig_bar"]), []).append(t)
        hi_v2 = np.nanmax(H)
        for (kind, fill, sig_bar), ts in groups.items():
            f0 = fill - a
            if not (0 <= f0 < n_):
                continue
            nums = ",".join(str(t["k"]) for t in ts)
            colr = cs.EXITC if kind == "signal" else (cs.BAD if kind == "stop" else "#cfcfcf")
            ax.scatter([f0], [ts[0]["px"]], marker="X", s=120, color=colr, edgecolor="black", zorder=11)
            if kind == "signal" and 0 <= sig_bar - a < n_:
                s0 = sig_bar - a
                cs.ring(ax, s0, s0, L[s0], H[s0], cs.EXITC, rr)
                yb = H[s0] if d > 0 else L[s0]
                cs.label(ax, s0, yb, f"exit {nums}", cs.EXITC, above=d > 0, fs=10)
            else:
                cs.label(ax, f0, ts[0]["px"], ("stop " if kind == "stop" else "16:45 ") + nums, colr, above=d < 0, fs=10)
    for xi, v, cl in ((s_, r.mom_SL, "#e6e6e6"), (h_, r.mom_SH, "#e6e6e6"), (p_, r.mom_PL, cs.HILITE)):
        axm.scatter([xi], [v], s=36, color=cl, edgecolor="black", zorder=5)
    if r.divergence:
        axm.plot([s_, p_], [r.mom_SL, r.mom_PL], color=cs.HILITE, linewidth=1.3, linestyle=(0, (4, 2)))
        axm.text(p_, r.mom_PL, "  hidden divergence", fontsize=9, color=cs.HILITE, va="center")
    cs.save(fig, path)


def card_html(sym, tf, r, tr=None):
    usd = sg.SPEC[sym]["usd"]; micro = sg.SPEC[sym]["micro"]; d = r.direction
    dec = 0 if sym == "YM" else 2
    end_word = "high" if d > 0 else "low"; pb_word = "low" if d > 0 else "high"
    def money(p):
        return f"${p * usd:,.2f}"
    def pts(p):
        return f"{p:,.{dec}f} pts"
    def line(v, touched):
        if not np.isfinite(v):
            return "n/a"
        return (f"touched ({pts(abs(v))} through)" if v <= 0 else f"stayed {pts(v)} short")
    oc = {"continuation": ("Continued", "✔", "ok"), "failure": ("Failed", "✖", "bad"),
          "neither": ("Neither", "–", "mid"), "no_time": ("No time left", "–", "mid")}[r.outcome]
    with_, against, minor = [], [], 0
    for tok in str(r.patterns).split():
        nm = tok.rstrip("+-")
        if nm in pb.FREQUENT:
            minor += 1; continue
        (against if tok.endswith("-") else with_).append(nm.replace("_", " "))
    trend = ("still " if r.trend_still else "no longer ") + ("up" if d > 0 else "down")
    res = ""
    if r.n_window > 0:
        res = (f"<tr><td>Best / worst after setup</td><td>+{money(r.mfe_pts)} / &minus;{money(r.mae_pts)}</td></tr>"
               f"<tr><td>At window end ({int(r.n_window)} bars)</td><td>{r.end_usd:+,.2f} $</td></tr>")
    return f"""<div class='card'>
<div class='hd'><span class='badge {oc[2]}'>{oc[1]} {oc[0]}</span>
<b>{micro} {tf}-min, {'bullish' if d > 0 else 'bearish'} pullback</b><br>
<span class='mut'>setup known {r.t_event:%a %Y-%m-%d %H:%M} ET ({r.tod})</span></div>
<div class='kpis'>
<div><span class='k'>{r.depth * 100:.0f}%</span><span class='l'>depth of the leg</span></div>
<div><span class='k'>{money(r.leg_pts)}</span><span class='l'>leg size ({pts(r.leg_pts)})</span></div>
<div><span class='k'>{money(r.to_SH_pts)}</span><span class='l'>to leg {end_word}</span></div>
<div><span class='k'>{money(r.to_PL_pts)}</span><span class='l'>to pullback {pb_word}</span></div>
</div>
<table>
<tr><th colspan=2>Pullback</th></tr>
<tr><td>Nearest Fibonacci level</td><td>{float(r.fib_near) * 100:.1f}% ({pts(abs(r.fib_dist_pts))} {'deeper' if r.fib_dist_pts > 0 else 'shallower'})</td></tr>
<tr><td>Bars: leg / pullback</td><td>{int(r.bars_impulse)} / {int(r.bars_pullback)}</td></tr>
<tr><td>Pullback volume vs leg</td><td>{r.vol_ratio:.2f}&times;</td></tr>
<tr><td>Trend (EMA 8/20/50) at setup</td><td>{trend}</td></tr>
<tr><th colspan=2>Pullback {pb_word} vs lines</th></tr>
<tr><td>EMA 20</td><td>{line(r.PL_to_ema20, r.touch_ema20)}</td></tr>
<tr><td>EMA 50</td><td>{line(r.PL_to_ema50, r.touch_ema50)}</td></tr>
<tr><td>VWAP</td><td>{line(r.PL_to_vwap, r.touch_vwap)}</td></tr>
<tr><th colspan=2>Momentum (14)</th></tr>
<tr><td>Leg start / leg {end_word} / pullback</td><td>{r.mom_SL:.2f} / {r.mom_SH:.2f} / {r.mom_PL:.2f}</td></tr>
<tr><td>Hidden divergence</td><td>{'yes' if r.divergence else 'no'}</td></tr>
<tr><th colspan=2>Candle patterns near the pullback {pb_word}</th></tr>
<tr><td>With the trade</td><td>{', '.join(with_) or 'none'}</td></tr>
<tr><td>Against the trade</td><td>{', '.join(against) or 'none'}</td></tr>
<tr><td>Frequent minor ones</td><td>{minor}</td></tr>
<tr><th colspan=2>What happened next</th></tr>
<tr><td>Result</td><td>{html.escape(outcome_text(r, micro))}</td></tr>
{res}
</table>{trade_html(sym, tf, tr)}<p class='mut'>$ per 1 {micro} contract; pullback stats before costs.</p></div>"""


def trade_html(sym, tf, tr):
    if not tr:
        return "<p class='mut'>No trade: no bar left before 16:45 ET.</p>"
    rows = "".join(
        f"<tr><td><b>{t['k']}</b> {t['label']}<br><span class='{'sig' if t['kind'] == 'signal' else 'mut'}'>"
        f"{html.escape(t['txt'])}</span><br><span class='mut'>{t['bars']} bars held</span></td>"
        f"<td style='color:{'#5cff6a' if t['pnl'] > 0 else '#ff7b8c'};white-space:nowrap'>"
        f"{'+' if t['pnl'] > 0 else '&minus;'}${abs(t['pnl']):,.2f}</td></tr>" for t in tr["rules"])
    return (f"<table><tr><th colspan=2>Trade from this setup, 5 exit rules</th></tr>"
            f"<tr><td>Entry (next bar's open)</td><td>{cs.fp(sym, tr['entry'])}</td></tr>"
            f"<tr><td>Stop (past the pullback point)</td><td>{cs.fp(sym, tr['stop'])}</td></tr>{rows}</table>"
            f"<p class='mut'>Exit $ after ${sg.SPEC[sym]['cost']:.2f} costs. Magenta box on the chart = the bar whose "
            f"signal triggered that numbered exit; the X = the fill at the next bar's open.</p>")


# ------------------------------------------------------------------------------------------- summary tables
def grp_table(df):
    """rows: (group, bucket, stats) over pullbacks that had an outcome window (outcome != no_time)."""
    g = df[df.outcome != "no_time"]
    out = []
    def add(group, label, s):
        if len(s) == 0:
            return
        out.append(dict(group=group, bucket=label, n=len(s), cont=100 * (s.outcome == "continuation").mean(),
                        fail=100 * (s.outcome == "failure").mean(), neither=100 * (s.outcome == "neither").mean(),
                        mfe_usd=s.mfe_usd.mean(), mae_usd=s.mae_usd.mean(), mfe_pts=s.mfe_pts.mean(),
                        mae_pts=s.mae_pts.mean(), to_sh=s.to_SH_pts.mean() * s.usd.iloc[0], to_pl=s.to_PL_pts.mean() * s.usd.iloc[0]))
    add("All", "all", g)
    for dv, lab in ((1, "bullish"), (-1, "bearish")):
        add("Direction", lab, g[g.direction == dv])
    bk = pb.depth_bucket(g.depth.to_numpy())
    for _, _, lab in pb.DEPTH_BUCKETS:
        add("Depth (share of the leg given back)", lab, g[bk == lab])
    for lo_, hi_, lab in LEG_BUCKETS:
        add("Leg size ($ per micro)", lab, g[(g.leg_usd >= lo_) & (g.leg_usd < hi_)])
    add("Trend at the event", "still with the leg", g[g.trend_still])
    add("Trend at the event", "not any more", g[~g.trend_still])
    add("Hidden momentum divergence", "yes", g[g.divergence])
    add("Hidden momentum divergence", "no", g[~g.divergence])
    for col, nm in (("touch_ema20", "EMA20"), ("touch_ema50", "EMA50"), ("touch_vwap", "VWAP")):
        add(f"PL touched {nm}", "yes", g[g[col]])
        add(f"PL touched {nm}", "no", g[~g[col]])
    for t in ("Asia (18-2)", "Europe (2-8)", "US pre (8-9:30)", "Open (9:30-10:30)", "Midday (10:30-15)", "Close (15-16)", "Post (16-17)"):
        add("Time of day of the event", t, g[g.tod == t])
    return out


def summary_html(sym, tf, df):
    micro = sg.SPEC[sym]["micro"]
    yr = df.groupby("year").agg(n=("direction", "size"), bull=("direction", lambda s: (s > 0).sum()),
                                bear=("direction", lambda s: (s < 0).sum()),
                                cont=("outcome", lambda s: 100 * (s == "continuation").sum() / max(1, (s != "no_time").sum())))
    h = [f"<h2 id='{sym}{tf}'>{micro} ({sym}) {tf}-minute bars: {len(df):,} pullbacks</h2>"]
    h.append("<div class='two'><div><h3>Count per year</h3><table><tr><th>Year</th><th>All</th><th>Bullish</th><th>Bearish</th>"
             "<th>Continuation %</th></tr>")
    for y, rw in yr.iterrows():
        h.append(f"<tr><td>{y}</td><td>{int(rw.n):,}</td><td>{int(rw.bull):,}</td><td>{int(rw.bear):,}</td><td>{rw.cont:.0f}</td></tr>")
    h.append("</table></div><div><h3>What happened next, by group</h3><table><tr><th>Group</th><th></th><th>n</th>"
             "<th>Continuation %</th><th>Failure %</th><th>Neither %</th><th>Avg best move $</th><th>Avg worst move $</th>"
             "<th>Avg best pts</th><th>Avg worst pts</th><th>Avg $ to SH at event</th><th>Avg $ to PL at event</th></tr>")
    last = None
    for t in grp_table(df):
        gname = t["group"] if t["group"] != last else ""
        last = t["group"]
        cls = " class='gs'" if gname else ""
        h.append(f"<tr{cls}><td>{html.escape(gname)}</td><td>{html.escape(t['bucket'])}</td><td>{t['n']:,}</td>"
                 f"<td><b>{t['cont']:.1f}</b></td><td>{t['fail']:.1f}</td><td>{t['neither']:.1f}</td>"
                 f"<td>{t['mfe_usd']:,.0f}</td><td>{t['mae_usd']:,.0f}</td><td>{t['mfe_pts']:,.1f}</td><td>{t['mae_pts']:,.1f}</td>"
                 f"<td>{t['to_sh']:,.0f}</td><td>{t['to_pl']:,.0f}</td></tr>")
    h.append(f"</table><p class='note'>$ per 1 {micro} contract (${sg.SPEC[sym]['usd']:g} per point). Outcome columns use only "
             f"pullbacks with at least one bar left before 16:45 ET ({(df.outcome != 'no_time').sum():,} of {len(df):,}).</p></div></div>")
    return "\n".join(h)


# ------------------------------------------------------------------------------------------- main
items = []          # (sym, tf, side, path, row)
summaries = []
for sym in dict.fromkeys(s for s, *_ in PLAN):
    spec = sg.SPEC[sym]
    for _, tf, nex in [p for p in PLAN if p[0] == sym]:
        b = sg.bars(sym, tf)
        c = sg.context(b, tick=spec["tick"])
        p = sg.patterns(b, c, tick=spec["tick"])
        df = pb.detect(b, c, k_leg=K, sym=sym, tf=tf, pats=p)
        df.insert(0, "market", spec["micro"]); df.insert(1, "tf", tf)
        df.to_csv(f"out/pullbacks_{sym}_{tf}{SUF}.csv", index=False)
        df["usd"] = spec["usd"]
        summaries.append((sym, tf, summary_html(sym, tf, df), len(df)))
        D = dict(b=b, c=c, p=p, piv3=sg.pivots(b, 3), pivK=sg.pivots(b, K))
        D.update(prep_exits(b, c, p, tf, spec["tick"]))
        ok = df[(df.i_SL >= BEFORE) & (df.i_event + AFTER < len(b)) & (df.outcome != "no_time")]
        for dv, side in ((1, "bullish"), (-1, "bearish")):
            pool = ok[ok.direction == dv]
            pick = pool.iloc[np.sort(rng.choice(len(pool), size=min(nex, len(pool)), replace=False))]
            for e, (_, r) in enumerate(pick.iterrows()):
                path = f"{IMG}/{sym}_{tf}_{side}_{e + 1}.jpg"
                draw(sym, tf, D, r, path)
                items.append((sym, tf, side, path, r))
        print(f"{sym} {tf}-min: {len(b):,} bars, {len(df):,} pullbacks, charts done", flush=True)
        del b, c, p, D, df

STYLE = ("<style>body{font-family:system-ui,sans-serif;margin:0 auto;padding:16px;background:#fcfcfb;color:#1f1e1c;max-width:1600px}"
         "h1{font-size:24px}h2{margin-top:40px;font-size:20px;border-bottom:1px solid #e1e0d9;padding-bottom:6px}"
         "h3{margin:10px 0 6px}p,li{max-width:1150px;line-height:1.5}"
         "nav{margin:10px 0}nav a{margin-right:14px;font-size:15px}"
         "table{border-collapse:collapse;font-size:13px;margin:6px 0}"
         "td,th{border:1px solid #e1e0d9;padding:3px 7px;text-align:right}th{background:#f1f0eb}"
         "td:first-child,td:nth-child(2){text-align:left}tr.gs td{border-top:2px solid #b9b7ae}"
         ".two{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start}.note{color:#55534e;font-size:13px}"
         ".ex{display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:18px;align-items:start;margin:18px 0 34px;"
         "padding:14px;background:#fff;border:1px solid #e6e4de;border-radius:10px}"
         "@media(max-width:1100px){.ex{grid-template-columns:1fr}}"
         ".ex img{width:100%;display:block}"
         ".card{font-size:14px}.card .hd{margin-bottom:10px;line-height:1.5}.mut{color:#8a8780;font-size:13px}"
         ".badge{display:inline-block;padding:2px 10px;border-radius:12px;font-weight:600;margin-right:6px;font-size:13px}"
         ".badge.ok{background:#e3f4ec;color:#1d7a50}.badge.bad{background:#fbe6e4;color:#a8352e}.badge.mid{background:#efeeea;color:#55534e}"
         ".kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 12px}"
         ".kpis div{background:#f6f5f1;border-radius:8px;padding:8px 10px}.kpis .k{display:block;font-size:20px;font-weight:650}"
         ".kpis .l{font-size:12px;color:#55534e}"
         ".card table{width:100%;font-size:13px}.card td,.card th{border:none;border-bottom:1px solid #efeeea;padding:4px 4px;"
         "text-align:left;vertical-align:top}.card th{background:none;color:#55534e;font-size:12px;text-transform:uppercase;"
         "letter-spacing:.04em;padding-top:12px}.card td:last-child{text-align:right;color:#1f1e1c}</style>")
LEGEND = """<h3>How to read a chart</h3><ul>
<li><b>White arrow</b> = the impulse leg, from the leg start to the leg high (low for bearish). <b>Yellow ring</b> = the pullback
low (high for bearish); its yellow dashed line is the level that, if price CLOSES past it, counts as a failure. The solid grey
line at the leg high is the level that counts as a continuation once price trades past it.</li>
<li><b>Dashed grey lines</b> = Fibonacci retracements of the leg (38.2%, 50%, 61.8%), labelled on the right.</li>
<li><b>White vertical line</b> = the moment the setup is known (3 bars after the pullback low). Everything in the blue-grey area
to its right is what happened next; the green dot / red X marks the bar where it continued or failed.</li>
<li>EMA 8 red dashed, EMA 20 orange dashed, EMA 50 green dashed, VWAP cyan. Thin dashed vertical lines = a new session (18:00 ET).</li>
<li>Bottom panel: Momentum(14) = 100 &times; close / close 14 bars earlier; dots at the leg start, leg end and pullback.
A yellow dashed line = hidden divergence (higher low in price, lower momentum).</li>
<li><b>Trade:</b> yellow triangle = entry at the next bar's open after the setup is known; red dotted line = stop 1 tick past
the pullback point. Each numbered exit rule (listed in the panel) is marked where it fired: a <b style='color:#ff5cf0'>magenta box
"exit N"</b> = the bar whose opposite signal triggered rule N, magenta X = its fill at the next open; "stop N" = rule N was
stopped out first; "16:45 N" = no signal came before the daily cutoff.</li>
<li>The panel on the right lists every stat; $ are per 1 micro contract (MES $5, MNQ $2, MYM $0.50 per point), before costs.</li></ul>"""
DEF = f"""<h3>Pullback definition (bullish; bearish is the mirror)</h3><ol>
<li>Impulse leg: a {K}-bar swing low SL, then a {K}-bar swing high SH, same contract; SL is the lowest and SH the highest price
between them; EMA 8 &gt; EMA 20 &gt; EMA 50 at the SH bar.</li>
<li>Pullback low PL: the first 3-bar swing low after SH. It must stay above SL, be the lowest price since SH, and no bar may close
above SH before the setup is known.</li>
<li>Depth = (SH - PL) / (SH - SL), kept between 0.1 and 1.</li>
<li>Event = PL + 3 bars (the swing low is confirmed); if SH itself is confirmed later, the event waits for that.</li>
<li>What happened next: from the event close, up to {pb.HORIZON} bars in the same session, flat by 16:45 ET.</li></ol>"""

# pages: about 6 examples each (embedded images keep each page under ~1 MB)
PER = 6
pages = [items[i:i + PER] for i in range(0, len(items), PER)]
nav = "<nav><a href='index.html'>summary</a>" + "".join(f"<a href='pullbacks_{j}.html'>page {j}</a>" for j in range(1, len(pages) + 1)) + "</nav>"
for pi, page in enumerate(pages, 1):
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>Pullbacks {pi}</title>{cs.PAGE_STYLE}</head><body>",
             f"<h1>Pullback examples, page {pi} of {len(pages)}</h1>{nav}<details><summary>How to read a chart</summary>{LEGEND}</details>"]
    last = None
    for sym, tf, side, path, r in page:
        key = (sym, tf, side)
        if key != last:
            parts.append(f"<h2>{sg.SPEC[sym]['micro']} {tf}-minute, {side} pullbacks</h2>")
            last = key
        img = base64.b64encode(open(path, 'rb').read()).decode()
        parts.append(f"<div class='ex'><img src='data:image/jpeg;base64,{img}'>{card_html(sym, tf, r, TRADES.get(path))}</div>")
    parts.append(f"{nav}</body></html>")
    open(f"{OUT}/pullbacks_{pi}.html", "w").write("\n".join(parts))

idx = [f"<!doctype html><html><head><meta charset='utf-8'><title>Pullback study</title>{STYLE}</head><body>",
       f"<h1>Pullbacks in a trend: summary over all detected pullbacks ({K}-bar swings for the leg)</h1>",
       "<p>Each market / timeframe below counts every pullback found in the whole data set. "
       "<b>Continuation %</b> = share that went past SH (the leg's extreme) before closing past PL (the pullback low/high); "
       "<b>Failure %</b> = closed past PL first; <b>Neither</b> = neither within the window. "
       "<b>Avg best / worst move</b> = largest move for / against the trade from the event close within the window "
       f"(up to {pb.HORIZON} bars, same session, flat 16:45 ET), measured over the whole window in any order; "
       "<b>Avg $ to SH / to PL</b> = how far SH and PL were from the event close (what a target at SH would make and a stop at PL "
       "would risk, before costs). All $ are per 1 micro contract.</p>",
       "<p>Jump to: " + " ".join(f"<a href='#{s}{t}'>{sg.SPEC[s]['micro']} {t}-min</a>" for s, t, *_ in summaries) + "</p>",
       f"<h2>Example charts</h2><ul>"]
for pi, page in enumerate(pages, 1):
    keys = list(dict.fromkeys(f"{sg.SPEC[s]['micro']} {t}-min {sd}" for s, t, sd, *_ in page))
    idx.append(f"<li><a href='pullbacks_{pi}.html'>Page {pi}</a>: {len(page)} charts ({', '.join(keys)})</li>")
idx.append("</ul>" + DEF)
for sym, tf, h, _ in summaries:
    idx.append(h)
idx.append(LEGEND + "</body></html>")
open(f"{OUT}/index.html", "w").write("\n".join(idx))
print(f"{len(items)} charts on {len(pages)} pages in {OUT}/")
for pi in range(1, len(pages) + 1):
    print(f"  pullbacks_{pi}.html {os.path.getsize(f'{OUT}/pullbacks_{pi}.html') / 1e6:.2f} MB")
