"""
Pattern gallery: for every pattern and direction, a few randomly chosen real occurrences (MES/MNQ/MYM, any year),
each drawn with everything: candles, EMA 8/20/50, session VWAP, swing points (3- and 10-bar), Momentum(14), the
pattern's bars highlighted, the entry (next bar's open) and the result 5 bars later. One PNG per pattern/direction in
gallery/, plus gallery/gallery.html (all images embedded, with each pattern's exact rule).
  PYTHONPATH=../../pylib:../..:. python3 gallery.py [TF] [examples]
"""
import base64
import html
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

import signals as sg

TF = int(sys.argv[1]) if len(sys.argv) > 1 else 15
NEX = int(sys.argv[2]) if len(sys.argv) > 2 else 4
BEFORE, AFTER = 20, 8
SPAN = {"engulfing": 2, "harami": 2, "piercing": 2, "dark_cloud": 2, "inside_bar": 2, "outside_bar": 2, "tweezer": 2,
        "morning_evening_star": 3, "three_soldiers_crows": 3, "three_inside": 3, "five_lower_lows_higher_highs": 6,
        "clv5_extreme": 5, "nr7": 7, "inside_bar_breakout": 3, "nr7_breakout": 3}
os.makedirs("gallery", exist_ok=True)
rng = np.random.default_rng(7)

data = {}
for sym in ("ES", "NQ", "YM"):
    spec = sg.SPEC[sym]
    b = sg.bars(sym, TF)
    c = sg.context(b, tick=spec["tick"], k_swing=10)
    p = sg.patterns(b, c, tick=spec["tick"])
    data[sym] = dict(b=b, c=c, p=p, lo3=sg.pivots(b, 3), lo10=sg.pivots(b, 10))
    print(f"{sym}: {len(b):,} bars", flush=True)


def draw(ax, axm, sym, i, name, d):
    D = data[sym]; b, c = D["b"], D["c"]
    a, z = i - BEFORE, i + AFTER + 1
    B = b.iloc[a:z]; n = len(B); x = np.arange(n); k0 = BEFORE
    O, H, L, C = (B[col].to_numpy() for col in "OHLC")
    up = C >= O; col = np.where(up, "#1baf7a", "#e34948")
    span = SPAN.get(name, 1)
    ax.axvspan(k0 - span + 0.5, k0 + 0.5, color="#f5c542", alpha=0.35, zorder=0)
    ax.axvspan(k0 + 0.5, k0 + 5.5, color="#cfe3f7", alpha=0.35, zorder=0)
    ax.vlines(x, L, H, color=col, linewidth=1.6)
    lo_p, hi_p = np.nanmin(L[k0 - span + 1:k0 + 1]), np.nanmax(H[k0 - span + 1:k0 + 1])
    rr = np.nanmax(H) - np.nanmin(L)
    ax.add_patch(Ellipse(((2 * k0 - span + 1) / 2, (lo_p + hi_p) / 2), width=span + 1.4,
                         height=(hi_p - lo_p) + 0.12 * rr, fill=False, edgecolor="#7a1fa2", linewidth=2.4, zorder=8))
    ax.bar(x, np.where(np.abs(C - O) > 0, C - O, 1e-6 * C), bottom=O, width=0.7, color=col, edgecolor="none")
    for e, cc in ((8, "#e34948"), (20, "#eda100"), (50, "#2a78d6")):
        ax.plot(x, c[f"ema{e}"].iloc[a:z].to_numpy(), color=cc, linewidth=1.6, alpha=0.85)
    vw = B.vwap.to_numpy().copy(); br = np.flatnonzero(B.sess.to_numpy()[1:] != B.sess.to_numpy()[:-1]) + 1
    ax.plot(np.insert(x.astype(float), br, np.nan), np.insert(vw, br, np.nan), color="#6db5e8", linewidth=1.2)
    for j in br:
        ax.axvline(j - 0.5, color="#898781", linewidth=0.7, linestyle=":")
    rngp = np.nanmax(H) - np.nanmin(L)
    for key, mk, sz, kk in (("lo3", "o", 40, 3), ("lo10", "D", 90, 10)):
        lo, hi = D[key]
        for arr, side, cc in ((lo, 1, "#2a78d6"), (hi, -1, "#6250d6")):
            for j in np.flatnonzero(arr[a:z]):
                if j + kk <= k0:     # only swing points already CONFIRMED at the pattern bar
                    ax.scatter(j, (L[j] if side > 0 else H[j]) - side * rngp * 0.02, marker=mk, s=sz, color=cc, zorder=6)
    entry = O[k0 + 1] if k0 + 1 < n else np.nan
    ex = C[k0 + 5] if k0 + 5 < n else np.nan
    if np.isfinite(entry) and np.isfinite(ex):
        mv = (ex - entry) * (d if d != 0 else 1)
        ax.annotate("", xy=(k0 + 5, ex), xytext=(k0 + 1, entry), arrowprops=dict(arrowstyle="->", color="#222", lw=1.2))
        ax.scatter([k0 + 1], [entry], s=18, color="#222", zorder=7)
        txt = f"{'+' if mv >= 0 else ''}{mv:.2f} pts in the signal's direction" if d != 0 else f"{ex - entry:+.2f} pts"
        ax.set_title(f"{sb_name(sym)} {TF}-min, pattern bar {b.index[i]:%Y-%m-%d %H:%M} ET    next 5 bars: {txt}", fontsize=13, loc="left")
    ax.set_ylim(np.nanmin(L) - rngp * 0.08, np.nanmax(H) + rngp * 0.08)
    ax.tick_params(labelsize=10); ax.grid(alpha=0.2); ax.set_xticks([]); ax.ticklabel_format(axis="y", useOffset=False)
    mom = c.mom14.iloc[a:z].to_numpy()
    axm.plot(x, mom, color="#6db5e8", linewidth=1); axm.axhline(100, color="#898781", linewidth=0.7)
    axm.fill_between(x, 100, mom, where=mom >= 100, color="#1baf7a", alpha=0.15)
    axm.fill_between(x, 100, mom, where=mom < 100, color="#e34948", alpha=0.15)
    axm.axvspan(k0 - span + 0.5, k0 + 0.5, color="#f5c542", alpha=0.35)
    axm.tick_params(labelsize=9); axm.set_xticks([]); axm.ticklabel_format(axis="y", useOffset=False)


def sb_name(sym):
    return sg.SPEC[sym]["micro"]


items = []
for name, (kind, rule) in sg.PATTERN_RULES.items():
    for d in ([1, -1] if kind == "dir" else [0]):
        pool = []
        for sym in data:
            P, b = data[sym]["p"], data[sym]["b"]
            v = P[name].to_numpy()
            idx = np.flatnonzero(v == d) if d != 0 else np.flatnonzero(v != 0)
            idx = idx[(idx >= BEFORE) & (idx < len(b) - AFTER - 1)]
            pool += [(sym, i) for i in idx]
        if not pool:
            continue
        pick = [pool[j] for j in rng.choice(len(pool), size=min(NEX, len(pool)), replace=False)]
        lab = ("bullish" if d > 0 else "bearish") if d != 0 else "neutral"
        out = []
        for e, (sym, i) in enumerate(pick):
            fig = plt.figure(figsize=(14, 6.2))
            gs = fig.add_gridspec(2, 1, height_ratios=[4, 1], hspace=0.12)
            draw(fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), sym, i, name, d)
            path = f"gallery/{name}_{lab}_{e + 1}.jpg"
            fig.savefig(path, dpi=85, bbox_inches="tight", pil_kwargs={"quality": 72}); plt.close(fig)
            out.append(path)
        items.append((name, lab, rule, out, len(pool)))
        print(name, lab, flush=True)

STYLE = ("<style>body{font-family:system-ui,sans-serif;margin:16px;background:#fcfcfb;color:#0b0b0b}"
         "h2{margin-top:32px}p.rule{color:#52514e;max-width:1100px}"
         "img{width:100%;max-width:1400px;display:block;margin:10px 0 22px;border:1px solid #e1e0d9}"
         "nav a{margin-right:12px;font-size:14px}</style>")
LEGEND = ("<p>Purple circle = the detected pattern; yellow = its bars; light blue = the 5 bars after; arrow = entry at the "
          "next open to the close 5 bars later. EMA 8 red, 20 orange, 50 blue; VWAP light blue; dots = 3-bar swing points, "
          "diamonds = 10-bar swing points (only those already confirmed when the pattern appears). Momentum(14) below.</p>")
PER = 6
pages = [items[i:i + PER] for i in range(0, len(items), PER)]
for pi, page in enumerate(pages, 1):
    nav = " ".join(f"<a href='gallery_{j}.html'>page {j}</a>" for j in range(1, len(pages) + 1))
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><title>Pattern gallery {pi}</title>{STYLE}</head><body>",
             f"<h1>Pattern gallery, page {pi} of {len(pages)} ({TF}-minute bars, MES / MNQ / MYM)</h1>{LEGEND}<nav>{nav}</nav>"]
    for n, l, rule, paths, cnt in page:
        parts.append(f"<h2>{html.escape(n.replace('_', ' '))} ({l})</h2><p class='rule'>Rule: {html.escape(rule)}. "
                     f"{cnt:,} occurrences on {TF}-minute bars across the three markets.</p>")
        for path in paths:
            parts.append(f"<img src='data:image/jpeg;base64,{base64.b64encode(open(path, 'rb').read()).decode()}'>")
    parts.append(f"<nav>{nav}</nav></body></html>")
    open(f"gallery/gallery_{pi}.html", "w").write("\n".join(parts))
index = [f"<!doctype html><html><head><meta charset='utf-8'><title>Pattern gallery</title>{STYLE}</head><body><h1>Pattern gallery</h1>{LEGEND}<ul>"]
for pi, page in enumerate(pages, 1):
    index.append(f"<li><a href='gallery_{pi}.html'>Page {pi}</a>: " + ", ".join(f"{n.replace('_', ' ')} ({l})" for n, l, *_ in page) + "</li>")
index.append("</ul></body></html>")
open("gallery/index.html", "w").write("\n".join(index))
print(f"gallery: {len(pages)} pages written")
