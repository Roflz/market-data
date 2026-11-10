"""
Charts with every signal drawn: candles, EMA 8/20/50, session VWAP, swing highs/lows (two sizes) with their levels
drawn until price closes through them, every detected candle pattern labelled on its bar, and Momentum(14) below.
  PYTHONPATH=../../pylib:../..:. python3 chart_signals.py ES 15 [n_bars] [end 'YYYY-MM-DD HH:MM'] [k_small k_big]
Writes charts/signals_{SYM}_{TF}_{end}.png
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import signals as sg

SYM, TF = sys.argv[1], int(sys.argv[2])
NB = int(sys.argv[3]) if len(sys.argv) > 3 else 120
END = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "last" else None
KS, KB = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (3, 10)
MAJOR_ONLY = '--major' in sys.argv
if MAJOR_ONLY: sys.argv.remove('--major')
FREQUENT = {'clv_extreme', 'clv5_extreme', 'bar_80_20', 'nr7', 'inside_bar', 'doji', 'spinning_top'}
ABBR = {"doji": "Dj", "dragonfly_doji": "DfDj", "gravestone_doji": "GvDj", "hammer": "Ham", "hanging_man": "HgM",
        "inverted_hammer": "IHam", "shooting_star": "SStar", "marubozu": "Maru", "spinning_top": "Spin",
        "engulfing": "Eng", "harami": "Har", "piercing": "Pierce", "dark_cloud": "DkCl", "morning_evening_star": "Star",
        "three_soldiers_crows": "3S/3C", "three_inside": "3In", "inside_bar": "IB", "outside_bar": "OB", "pin_bar": "Pin",
        "nr7": "NR7", "tweezer": "Twz", "inside_bar_breakout": "IB-brk", "nr7_breakout": "NR7-brk",
        "clv_extreme": "CLV", "bar_80_20": "80/20", "tall_trend_bar": "Tall", "five_lower_lows_higher_highs": "5LL/5HH",
        "clv5_extreme": "CLV5"}

spec = sg.SPEC[SYM]
b = sg.bars(SYM, TF)
c = sg.context(b, tick=spec["tick"], k_swing=KB)
p = sg.patterns(b, c, tick=spec["tick"])
end_i = len(b) if END is None else int(b.index.searchsorted(pd.Timestamp(END), side="right"))
w = slice(max(0, end_i - NB), end_i)
B, Cx, Px = b.iloc[w], c.iloc[w], p.iloc[w]
n = len(B); x = np.arange(n)
O, H, L, C = (B[col].to_numpy() for col in "OHLC")
fig, (ax, axm) = plt.subplots(2, 1, figsize=(18, 10), sharex=True, gridspec_kw={"height_ratios": [4, 1.2]})
up = C >= O
col = np.where(up, "#1baf7a", "#e34948")
ax.vlines(x, L, H, color=col, linewidth=0.9)
ax.bar(x, np.where(np.abs(C - O) > 0, C - O, spec["tick"] * 0.2), bottom=O, width=0.62, color=col, edgecolor="none")
for e, cc in ((8, "#e34948"), (20, "#eda100"), (50, "#2a78d6")):
    ax.plot(x, Cx[f"ema{e}"].to_numpy(), color=cc, linewidth=1.2, alpha=0.85, label=f"EMA {e}")
vw = B.vwap.to_numpy().copy()
_br = np.flatnonzero(B.sess.to_numpy()[1:] != B.sess.to_numpy()[:-1]) + 1
xv = np.insert(x.astype(float), _br, np.nan); vv = np.insert(vw, _br, np.nan)      # break the line between sessions
ax.plot(xv, vv, color="#6db5e8", linewidth=1.4, alpha=0.9, label="session VWAP")
rngp = np.nanmax(H) - np.nanmin(L)
# swing points (two sizes) and their levels, drawn from the moment they are known until a close through them
for k, mk, sz, a, lw in ((KS, "o", 22, 0.55, 0.6), (KB, "D", 46, 0.95, 1.1)):
    lo, hi = sg.pivots(b, k)
    for arr, side, cc in ((lo, 1, "#2a78d6"), (hi, -1, "#6250d6")):
        idx = np.flatnonzero(arr[w])
        for i in idx:
            lvl = L[i] if side > 0 else H[i]
            ax.scatter(i, lvl - side * rngp * 0.012, marker=mk, s=sz, color=cc, alpha=a, zorder=6)
            kn = i + k
            if kn >= n:
                continue
            brk = np.flatnonzero((C[kn:] < lvl) if side > 0 else (C[kn:] > lvl))
            stop = kn + (brk[0] if len(brk) else n - kn)
            ax.hlines(lvl, kn, stop, color=cc, linewidth=lw, alpha=a * 0.8, linestyles="--")
# pattern labels: directional above/below the bar, neutral in grey
offs_up = np.zeros(n); offs_dn = np.zeros(n)
for name, (kind, _) in sg.PATTERN_RULES.items():
    if MAJOR_ONLY and name in FREQUENT:
        continue
    v = Px[name].to_numpy()
    for i in np.flatnonzero(v != 0):
        lab = ABBR[name]
        if kind == "dir" and v[i] > 0:
            yy = L[i] - rngp * (0.035 + offs_dn[i]); offs_dn[i] += 0.028
            ax.annotate(lab + "↑", (i, yy), ha="center", va="top", fontsize=6.5, color="#0f7a52", fontweight="bold")
        elif kind == "dir":
            yy = H[i] + rngp * (0.035 + offs_up[i]); offs_up[i] += 0.028
            ax.annotate(lab + "↓", (i, yy), ha="center", va="bottom", fontsize=6.5, color="#b8322f", fontweight="bold")
        else:
            yy = H[i] + rngp * (0.035 + offs_up[i]); offs_up[i] += 0.028
            ax.annotate(lab, (i, yy), ha="center", va="bottom", fontsize=6.5, color="#6b6a66")
sess = B.sess.to_numpy()
for i in np.flatnonzero(sess[1:] != sess[:-1]) + 1:
    ax.axvline(i - 0.5, color="#898781", linewidth=0.8, linestyle=":")
    axm.axvline(i - 0.5, color="#898781", linewidth=0.8, linestyle=":")
ax.scatter([], [], marker="o", color="#2a78d6", s=22, label=f"swing low/high, {KS} bars each side (small)")
ax.scatter([], [], marker="D", color="#2a78d6", s=46, label=f"swing low/high, {KB} bars each side (large); dashed = level until closed through")
ax.set_ylim(np.nanmin(L) - rngp * 0.25, np.nanmax(H) + rngp * 0.25)
ax.legend(loc="upper left", fontsize=8, ncol=3)
ax.grid(alpha=0.2)
ax.set_title(f"{SYM} ({spec['micro']}) {TF}-minute bars, {B.index[0]:%Y-%m-%d %H:%M} to {B.index[-1]:%Y-%m-%d %H:%M} ET. "
             f"Green ↑ = bullish pattern, red ↓ = bearish, grey = neutral" + (" (most frequent labels hidden: close-location, 80/20, NR7, inside bar, doji, spinning top)" if MAJOR_ONLY else ""), loc="left", fontsize=11)
mom = Cx.mom14.to_numpy()
axm.plot(x, mom, color="#6db5e8", linewidth=1.3)
axm.axhline(100, color="#898781", linewidth=0.8)
axm.fill_between(x, 100, mom, where=mom >= 100, color="#1baf7a", alpha=0.15)
axm.fill_between(x, 100, mom, where=mom < 100, color="#e34948", alpha=0.15)
axm.set_ylabel("Momentum (14)")
axm.grid(alpha=0.2)
ticks = np.arange(0, n, max(1, n // 14))
axm.set_xticks(ticks)
axm.set_xticklabels([B.index[i].strftime("%m-%d %H:%M") for i in ticks], fontsize=8)
key = "  ".join(f"{v}={k.replace('_', ' ')}" for k, v in ABBR.items())
fig.text(0.01, 0.005, "Labels: " + key, fontsize=6.5, wrap=True, color="#52514e")
plt.tight_layout(rect=(0, 0.04, 1, 1))
tag = B.index[-1].strftime("%Y%m%d_%H%M")
out = f"charts/signals_{SYM}_{TF}_{tag}{'_major' if MAJOR_ONLY else ''}.png"
plt.savefig(out, dpi=95)
print(out)
