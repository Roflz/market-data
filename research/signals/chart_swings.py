"""
Example charts: the same recent stretch of candles with the swing points found by each swing size k marked, so the
sizes can be compared by eye. One PNG per market/timeframe in charts/.
  PYTHONPATH=../../pylib:../..:. python3 chart_swings.py ES 15 [n_bars]
Markers: triangle under a swing low, triangle over a swing high, at the pivot bar (the point is only KNOWN k bars
later, shown by a faint dot). EMA 8/20/50 drawn for orientation.
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import signals as sg

SYM, TF = sys.argv[1], int(sys.argv[2])
NB = int(sys.argv[3]) if len(sys.argv) > 3 else 160
KS = (3, 5, 10, 15)
b = sg.bars(SYM, TF)
c = sg.context(b, tick=sg.SPEC[SYM]["tick"])
piv = {k: sg.pivots(b, k) for k in KS}
w = slice(len(b) - NB, len(b))
x = np.arange(NB)
B = b.iloc[w]
fig, axes = plt.subplots(len(KS), 1, figsize=(16, 4.2 * len(KS)), sharex=True)
for ax, k in zip(axes, KS):
    O, H, L, C = (B[col].to_numpy() for col in "OHLC")
    up = C >= O
    ax.vlines(x, L, H, color=np.where(up, "#1baf7a", "#e34948"), linewidth=0.8)
    ax.bar(x, np.where(np.abs(C - O) > 0, C - O, 0.0001 * C), bottom=O, width=0.6,
           color=np.where(up, "#1baf7a", "#e34948"), edgecolor="none")
    for e, col in ((8, "#e34948"), (20, "#eda100"), (50, "#2a78d6")):
        ax.plot(x, c[f"ema{e}"].iloc[w].to_numpy(), color=col, linewidth=1, alpha=0.8, label=f"EMA{e}")
    lo, hi = piv[k][0][w], piv[k][1][w]
    pad = (np.nanmax(H) - np.nanmin(L)) * 0.015
    ax.scatter(x[lo], L[lo] - pad, marker="^", s=60, color="#2a78d6", zorder=5, label="swing low")
    ax.scatter(x[hi], H[hi] + pad, marker="v", s=60, color="#6250d6", zorder=5, label="swing high")
    known_lo = np.flatnonzero(lo) + k; known_hi = np.flatnonzero(hi) + k
    known_lo = known_lo[known_lo < NB]; known_hi = known_hi[known_hi < NB]
    ax.scatter(known_lo, C[known_lo], s=12, color="#2a78d6", alpha=0.35, zorder=4)
    ax.scatter(known_hi, C[known_hi], s=12, color="#6250d6", alpha=0.35, zorder=4)
    sess = B.sess.to_numpy()
    for i in np.flatnonzero(sess[1:] != sess[:-1]) + 1:
        ax.axvline(i - 0.5, color="#898781", linewidth=0.6, linestyle=":")
    ax.set_title(f"{SYM} {TF}-minute, swing size k = {k} bars each side ({lo.sum()} lows, {hi.sum()} highs shown; "
                 f"each is known {k * TF} min after the turn)", fontsize=11, loc="left")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper left", fontsize=8, ncol=5)
ticks = np.arange(0, NB, max(1, NB // 12))
axes[-1].set_xticks(ticks)
axes[-1].set_xticklabels([B.index[i].strftime("%m-%d %H:%M") for i in ticks], rotation=0, fontsize=8)
plt.tight_layout()
out = f"charts/swings_{SYM}_{TF}.png"
plt.savefig(out, dpi=90)
print(out)
