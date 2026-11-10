"""
Exit examples: random real trades from the exit study, each charted in the dark platform style with the ENTRY pattern
(yellow box) and the exact OPPOSITE SIGNAL that closed the trade (magenta box, named), entry/exit fills, P&L, EMAs,
VWAP and Momentum(14). No stop (pure signal exit, or 16:45 ET), entries = classic candle patterns.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:. python3 exit_gallery.py
Writes exit_examples/exits_N.html (+ img/).
"""
import base64
import html
import os

import numpy as np
import pandas as pd

import chart_style as cs
import exits as ex
import signals as sg

OUT = "exit_examples"; IMG = f"{OUT}/img"
os.makedirs(IMG, exist_ok=True)
PLAN = [("NQ", 15), ("ES", 15), ("NQ", 5)]
PER_RULE = 3
BEFORE, AFTER, MAXBARS = 25, 12, 170
RULES = {
    "opp_classic": "exit when ANY classic candle pattern fires in the opposite direction",
    "opp_same": "exit when the SAME pattern fires in the opposite direction",
    "opp_any2": "exit when 2+ different patterns fire in the opposite direction on one bar",
    "opp_classic_at_level": "exit when an opposite classic pattern fires AT the latest 5-bar swing high (low for shorts)",
    "choch_5": "change of character: exit on a close past the latest confirmed 5-bar swing low (high for shorts)",
    "ema20_cross": "exit on a close back through EMA 20",
    "mom_cross100": "exit when Momentum(14) crosses back through 100",
}
rng = np.random.default_rng(5)


def nice(nm):
    return nm.replace("_", " ")


items = []
for SYM, TF in PLAN:
    spec = sg.SPEC[SYM]; USD, COST, TICK = spec["usd"], spec["cost"], spec["tick"]
    b = sg.bars(SYM, TF); c = sg.context(b, tick=TICK); p = sg.patterns(b, c, tick=TICK)
    O, H, L, C = (b[x].to_numpy() for x in "OHLC")
    seg = b.seg.to_numpy(); run = b.run.to_numpy(); n = len(b)
    allowed, forced = ex.session_frame(b, TF)
    raw_ok = (b.H - b.L).rolling(14).mean().gt(TICK).to_numpy()
    ema20, mom, atr = c.ema20.to_numpy(), c.mom14.to_numpy(), c.atr14.to_numpy()
    P = {k: p[k].to_numpy() for k in ex.DIRECTIONAL}
    lo5, hi5 = sg.pivots(b, 5)
    clo = np.full(n, np.nan); chi = np.full(n, np.nan)
    q = np.flatnonzero(lo5); clo[q + 5] = L[q]; q = np.flatnonzero(hi5); chi[q + 5] = H[q]
    sl5 = pd.Series(clo).groupby(run).ffill().to_numpy(); sh5 = pd.Series(chi).groupby(run).ffill().to_numpy()
    cb = sum((P[k] == -1).astype(np.int16) for k in ex.CLASSIC); cu = sum((P[k] == 1).astype(np.int16) for k in ex.CLASSIC)
    ab = sum((P[k] == -1).astype(np.int16) for k in ex.DIRECTIONAL); au = sum((P[k] == 1).astype(np.int16) for k in ex.DIRECTIONAL)
    with np.errstate(invalid="ignore"):
        COND = {"opp_classic": (cb >= 1, cu >= 1), "opp_any2": (ab >= 2, au >= 2),
                "opp_classic_at_level": ((cb >= 1) & (H >= sh5 - 0.5 * atr), (cu >= 1) & (L <= sl5 + 0.5 * atr)),
                "choch_5": (ex.fresh(C < sl5), ex.fresh(C > sh5)),
                "ema20_cross": (ex.fresh(C < ema20), ex.fresh(C > ema20)),
                "mom_cross100": (ex.fresh(mom < 100), ex.fresh(mom > 100))}
    # every classic-pattern entry
    ent = []
    for name in ex.CLASSIC:
        for d0 in (1, -1):
            i = np.flatnonzero(P[name] == d0); i = i[i < n - 1]; e = i + 1
            ok = (seg[e] == seg[i]) & allowed[e] & raw_ok[i] & (forced[e] >= e)
            ent += [(name, d0, k) for k in i[ok]]
    ent = pd.DataFrame(ent, columns=["pattern", "d", "i"])
    for rule in RULES:
        rows = []
        for name, g in ent.groupby("pattern"):
            for d0, gg in g.groupby("d"):
                i = gg.i.to_numpy(); e = i + 1; d = np.full(len(i), d0)
                if rule == "opp_same":
                    nb, nu = ex.next_true(P[name] == -1), ex.next_true(P[name] == 1)
                else:
                    nb, nu = ex.next_true(COND[rule][0]), ex.next_true(COND[rule][1])
                x_end, x_px, sig = ex.plan_exits(e, d, forced, nb, nu, O, C)
                for k in np.flatnonzero(sig == 1):
                    if x_end[k] + 1 - i[k] <= MAXBARS - BEFORE - AFTER:
                        rows.append((name, d0, i[k], x_end[k]))
        if not rows:
            continue
        pick = [rows[j] for j in rng.choice(len(rows), size=min(PER_RULE, len(rows)), replace=False)]
        for t, (name, d0, i, j) in enumerate(pick):
            e = i + 1; fill = j + 1
            entry, exitp = O[e], O[fill]
            pnl = d0 * (exitp - entry) * USD - COST
            path_hi, path_lo = H[e:fill].max(), L[e:fill].min()
            mfe = (path_hi - entry) if d0 > 0 else (entry - path_lo)
            mae = (entry - path_lo) if d0 > 0 else (path_hi - entry)
            # which signal(s) fired at bar j
            want = -d0
            if rule in ("opp_classic", "opp_classic_at_level"):
                names = [k for k in ex.CLASSIC if P[k][j] == want]
            elif rule == "opp_any2":
                names = [k for k in ex.DIRECTIONAL if P[k][j] == want]
            elif rule == "opp_same":
                names = [name]
            else:
                names = []
            word = "bearish" if want < 0 else "bullish"
            if names:
                sig_txt = " + ".join(cs.pname(k, want) for k in names)
                if rule == "opp_classic_at_level":
                    lvl = sh5[j] if d0 > 0 else sl5[j]
                    sig_txt += f" at the swing {'high' if d0 > 0 else 'low'} {cs.fp(SYM, lvl)}"
            elif rule == "choch_5":
                lvl = sl5[j] if d0 > 0 else sh5[j]
                sig_txt = f"close {cs.fp(SYM, C[j])} {'below' if d0 > 0 else 'above'} the swing {'low' if d0 > 0 else 'high'} {cs.fp(SYM, lvl)}"
            elif rule == "ema20_cross":
                sig_txt = f"close {cs.fp(SYM, C[j])} {'below' if d0 > 0 else 'above'} EMA 20 ({cs.fp(SYM, ema20[j])})"
            else:
                sig_txt = f"Momentum {mom[j]:.2f} crossed {'below' if d0 > 0 else 'above'} 100"
            span_e = max([ex.SPAN.get(k, 1) for k in names] or [1])
            # ---- chart
            a = max(0, i - BEFORE); z = min(n, fill + AFTER + 1)
            B = b.iloc[a:z]; Cx = c.iloc[a:z]
            fig, ax, axm = cs.new_figure()
            x, Ob, Hb, Lb, Cb = cs.draw_base(ax, axm, B, Cx, SYM)
            rr = np.nanmax(Hb) - np.nanmin(Lb)
            sp = ex.SPAN.get(name, 1)
            i0, j0, e0, f0 = i - a, j - a, e - a, fill - a
            ax.axvspan(e0 - 0.5, f0 - 0.5, color="#1b2a3a", alpha=0.55, zorder=0, lw=0)      # time in the trade
            axm.axvspan(e0 - 0.5, f0 - 0.5, color="#1b2a3a", alpha=0.55, zorder=0, lw=0)
            lo_v, hi_v = np.nanmin(Lb), np.nanmax(Hb)
            def callout(xc, y_edge, y_row, txt, colr):
                ha = "right" if xc > 0.78 * len(x) else ("left" if xc < 0.22 * len(x) else "center")
                ax.annotate(txt, xy=(xc, y_edge), xytext=(xc, y_row), textcoords="data", ha=ha, va="center",
                            fontsize=11, color=colr, fontweight="bold", zorder=12,
                            bbox=dict(boxstyle="round,pad=0.3", fc="#0a0a0a", ec=colr, lw=1),
                            arrowprops=dict(arrowstyle="-|>", color=colr, lw=1.2, shrinkA=0, shrinkB=3))
            e_lo, e_hi = Lb[i0 - sp + 1:i0 + 1].min(), Hb[i0 - sp + 1:i0 + 1].max()
            cs.ring(ax, i0 - sp + 1, i0, e_lo, e_hi, cs.HILITE, rr)
            js = max(e0, j0 - span_e + 1)
            x_lo, x_hi = Lb[js:j0 + 1].min(), Hb[js:j0 + 1].max()
            cs.ring(ax, js, j0, x_lo, x_hi, cs.EXITC, rr)
            # structure level that the exit used
            if rule in ("choch_5", "opp_classic_at_level"):
                lv = (sl5 if (d0 > 0) == (rule == "choch_5") else sh5)
                lvl = lv[j]
                if np.isfinite(lvl):
                    ax.hlines(lvl, e0 - 0.5, j0 + 0.5, color=cs.EXITC, linewidth=1.2, linestyles=(0, (4, 3)), zorder=5)
                    ax.text(e0 - 0.4, lvl, f"swing {'low' if lv is sl5 else 'high'} {cs.fp(SYM, lvl)} ", color=cs.EXITC,
                            fontsize=9.5, ha="right", va="center", zorder=12,
                            bbox=dict(boxstyle="round,pad=0.15", fc="#0a0a0a", ec="none"))
            callout(i0 - (sp - 1) / 2, e_lo - rr * 0.02, lo_v - rr * 0.07,
                    f"ENTRY: {cs.pname(name, d0)}", cs.HILITE)
            short_sig = sig_txt if len(sig_txt) <= 60 else sig_txt[:58] + "\u2026"
            callout((js + j0) / 2, x_hi + rr * 0.02, hi_v + rr * 0.11, f"EXIT SIGNAL: {short_sig}", cs.EXITC)
            pc = cs.GOOD if pnl > 0 else cs.BAD
            ax.plot([e0, f0], [entry, exitp], color=pc, linewidth=1.8, linestyle=(0, (1, 2)), zorder=6)
            ax.scatter([e0], [entry], marker="^" if d0 > 0 else "v", s=130, color=cs.HILITE, edgecolor="black", zorder=10)
            ax.scatter([f0], [exitp], marker="X", s=130, color=cs.EXITC, edgecolor="black", zorder=10)
            ax.annotate(f"{'+' if pnl >= 0 else '\u2212'}${abs(pnl):,.2f}", (f0, exitp), xytext=(12, 0),
                        textcoords="offset points", ha="left", va="center", color=pc, fontsize=12.5,
                        fontweight="bold", bbox=dict(boxstyle="round,pad=0.25", fc="#000", ec=pc, lw=0.9), zorder=11)
            for xx, mk in ((i0 - (sp - 1) / 2, cs.HILITE), ((js + j0) / 2, cs.EXITC)):
                axm.axvline(xx, color=mk, linewidth=1, alpha=0.6)
            path = f"{IMG}/{SYM}_{TF}_{rule}_{t + 1}.jpg"
            cs.save(fig, path)
            items.append(dict(sym=SYM, tf=TF, rule=rule, path=path, name=name, d=d0, t_entry=b.index[e],
                              t_exit=b.index[fill], entry=entry, exitp=exitp, pnl=pnl, bars=fill - e, sig=sig_txt,
                              mfe=mfe * USD, mae=mae * USD, micro=spec["micro"], cost=COST))
    print(f"{SYM} {TF}m done", flush=True)
    del b, c, p, P


def card(it):
    win = it["pnl"] > 0
    return f"""<div class='card'><div class='hd'><span class='badge {'ok' if win else 'bad'}'>{'+' if win else '−'}${abs(it['pnl']):,.2f}</span>
<b>{it['micro']} {it['tf']}-min, {'long' if it['d'] > 0 else 'short'}</b><br>
<span class='mut'>{it['t_entry']:%a %Y-%m-%d %H:%M} ET</span></div>
<table>
<tr><th colspan=2>Entry</th></tr>
<tr><td>Pattern</td><td class='ent'>{cs.pname(it['name'], it['d'])}</td></tr>
<tr><td>Filled (next bar's open)</td><td>{cs.fp(it['sym'], it['entry'])} at {it['t_entry']:%H:%M}</td></tr>
<tr><th colspan=2>Exit</th></tr>
<tr><td>Rule</td><td>{html.escape(RULES[it['rule']])}</td></tr>
<tr><td>Signal that fired</td><td class='sig'>{html.escape(it['sig'])}</td></tr>
<tr><td>Filled (next bar's open)</td><td>{cs.fp(it['sym'], it['exitp'])} at {it['t_exit']:%m-%d %H:%M}</td></tr>
<tr><th colspan=2>Result, 1 {it['micro']}</th></tr>
<tr><td>Held</td><td>{it['bars']} bars ({it['bars'] * it['tf']} min)</td></tr>
<tr><td>P&amp;L after ${it['cost']:.2f} costs</td><td>{'+' if win else '−'}${abs(it['pnl']):,.2f}</td></tr>
<tr><td>Best / worst while open</td><td>+${it['mfe']:,.2f} / −${it['mae']:,.2f}</td></tr>
</table></div>"""


LEGEND = """<details open><summary>How to read a chart</summary><ul>
<li><b style='color:#ffe14d'>Yellow box</b> = the entry pattern; yellow triangle = entry fill at the next bar's open.</li>
<li><b style='color:#ff5cf0'>Magenta box</b> = the opposite signal that closed the trade (named on the chart and in the panel);
magenta X = exit fill at the next bar's open. Dotted line between them = the trade, green if it made money after costs.</li>
<li>Blue-grey shading = time in the trade. EMA 8 red dashed, EMA 20 orange dashed, EMA 50 green dashed, VWAP cyan,
Momentum(14) underneath. Dashed vertical lines = new session (18:00 ET).</li>
<li>No stop is used here, so each trade shows the pure signal exit. $ per 1 micro contract.</li></ul></details>"""
PER = 6
groups = {}
for it in items:
    groups.setdefault(it["rule"], []).append(it)
order = [it for r in RULES for it in groups.get(r, [])]
pages = [order[k:k + PER] for k in range(0, len(order), PER)]
nav = "<nav>" + "".join(f"<a href='exits_{j}.html'>page {j}</a>" for j in range(1, len(pages) + 1)) + "</nav>"
for pi, page in enumerate(pages, 1):
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
             f"<title>Exit examples {pi}</title>{cs.PAGE_STYLE}</head><body><h1>Exit examples, page {pi} of {len(pages)}</h1>{nav}{LEGEND}"]
    last = None
    for it in page:
        if it["rule"] != last:
            parts.append(f"<h2>{html.escape(RULES[it['rule']])}</h2>"); last = it["rule"]
        img = base64.b64encode(open(it["path"], "rb").read()).decode()
        parts.append(f"<div class='ex'><img src='data:image/jpeg;base64,{img}'>{card(it)}</div>")
    parts.append(nav + "</body></html>")
    open(f"{OUT}/exits_{pi}.html", "w").write("\n".join(parts))
print(f"{len(items)} charts on {len(pages)} pages")
for pi in range(1, len(pages) + 1):
    print(f"  exits_{pi}.html {os.path.getsize(f'{OUT}/exits_{pi}.html') / 1e6:.2f} MB")
