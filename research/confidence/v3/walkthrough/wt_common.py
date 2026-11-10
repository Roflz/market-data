"""Shared helpers for the visual walkthrough (dark NinjaTrader-like style from research/signals/chart_style.py).
All data is pre-holdout (< 2025-06-30 18:00 ET). Bars are stamped with their START time (NinjaTrader stamps the END)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import chart_style as cs
import signals as sg

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(HERE, "cards")
os.makedirs(CARDS, exist_ok=True)
V3 = os.path.join(HERE, "..", "data")
HOLDOUT = pd.Timestamp("2025-06-30 18:00")
USD = {"NQ": 2.0, "ES": 5.0, "YM": 0.5}
TICK = {"NQ": 0.25, "ES": 0.25, "YM": 1.0}
COST = {"NQ": 2.0, "ES": 3.5, "YM": 2.0}
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
DPI = 88
W, H = 1600 / DPI, 900 / DPI
plt.rcParams.update({"font.size": 13, "font.family": "DejaVu Sans", "text.parse_math": False})

_bars = {}


def bars(sym, tf):
    k = (sym, tf)
    if k not in _bars:
        b = pd.read_parquet(os.path.join(V3, f"bars_{sym}_{tf}.parquet"))
        assert b.index.max() < HOLDOUT
        _bars[k] = b
    return _bars[k]


def sessions(sym):
    s = pd.read_parquet(os.path.join(V3, f"sessions_{sym}.parquet"))
    return s


def style_ax(a):
    a.set_facecolor(cs.BG)
    a.grid(color=cs.GRID, linewidth=0.8)
    a.set_axisbelow(True)
    for sp in a.spines.values():
        sp.set_color("#333333")
    a.tick_params(colors=cs.TXT, labelsize=12)
    a.yaxis.tick_right()
    a.yaxis.set_label_position("right")


def candles(a, B, width=0.62, lw=1.2):
    n = len(B)
    x = np.arange(n)
    O, Hh, L, C = (B[c].to_numpy() for c in "OHLC")
    rr = np.nanmax(Hh) - np.nanmin(L)
    col = np.where(C >= O, cs.UP, cs.DN)
    a.vlines(x, L, Hh, color=col, linewidth=lw, zorder=3)
    a.bar(x, np.where(np.abs(C - O) > 0, C - O, rr * 0.003), bottom=O, width=width, color=col, edgecolor="none",
          zorder=3)
    return x


def emas(a, x, B, lw_scale=1.0, label=True):
    for e, st in cs.EMA_STYLE.items():
        a.plot(x, B[f"ema{e}"].to_numpy(), color=st["color"], linewidth=st["lw"] * lw_scale, linestyle=(0, (5, 3)),
               zorder=2, label=f"EMA {e}" if label else None)


def time_ticks(a, idx, nt=9, fs=12):
    n = len(idx)
    ticks = np.linspace(0, n - 1, nt).round().astype(int)
    prev = None
    lab = []
    for t in ticks:
        ts = idx[t]
        lab.append(ts.strftime("%H:%M\n%a %m/%d/%y") if ts.date() != prev else ts.strftime("%H:%M"))
        prev = ts.date()
    a.set_xticks(ticks)
    a.set_xticklabels(lab, fontsize=fs, color=cs.TXT)


def tag(a, xi, y, txt, color, dy=18, fs=12.5, ha="center", va=None, dx=0):
    a.annotate(txt, (xi, y), xytext=(dx, dy), textcoords="offset points", ha=ha,
               va=va or ("bottom" if dy > 0 else "top"), fontsize=fs, color=color, fontweight="bold", zorder=12,
               bbox=dict(boxstyle="round,pad=0.25", fc="#111111", ec=color, lw=0.9, alpha=0.93),
               arrowprops=dict(arrowstyle="-", color=color, lw=0.9) if (dy or dx) else None)


def legend(a, loc="upper left", ncol=4, fs=12, **kw):
    lg = a.legend(loc=loc, ncol=ncol, fontsize=fs, frameon=True, facecolor="#0b0b0b", edgecolor="#333333", **kw)
    for t in lg.get_texts():
        t.set_color(cs.TXT)
    return lg


def save(fig, name):
    p = os.path.join(HERE, name)
    fig.savefig(p, dpi=DPI, facecolor=cs.BG)
    plt.close(fig)
    return p


def card(name, obj):
    def conv(v):
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            return None if not np.isfinite(v) else float(v)
        if isinstance(v, float) and not np.isfinite(v):
            return None
        if isinstance(v, (pd.Timestamp,)):
            return str(v)
        if isinstance(v, dict):
            return {k: conv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [conv(x) for x in v]
        return v
    p = os.path.join(CARDS, name + ".json")
    with open(p, "w") as f:
        json.dump(conv(obj), f, indent=1, default=str)
    return p
