"""
Chart gallery for the morning report: candidate B (15-min, model M3 cls, 'stop only, hold to 16:45', one position per
market, 1 micro, no adds) from v2/out/evalc_candlegs_B_<sym>.parquet (out-of-sample 2013..2025H1, YM 2018+).

  12 random kept trades (4 per market) + 6 losing trades (2 per market), seed 7.
  Each PNG: 15-min candles, EMA 8/20/50, VWAP, Momentum(14) (research/signals/chart_style.py);
  signal bar ringed, entry price (yellow), first stop (red dashed), stop after any move (none: no adds), exit (magenta).

Bars are cut before walkforward.HOLDOUT_SESSION_START before anything is computed. Loads 1-minute data (heavy):
one market at a time.
  v2/gallery.py            -> v2/out/gallery/*.png + v2/out/gallery/gallery.csv
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

import chart_style as cs
import signals as sg
import walkforward as wf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "gallery")
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
KIND = {0: "time exit (16:45 flat)", 1: "stopped", 3: "rule exit"}
TF = 15


def pick(seed=7):
    rows = []
    rng = np.random.default_rng(seed)
    for sym in ("NQ", "ES", "YM"):
        L = pd.read_parquet(os.path.join(HERE, "out", f"evalc_candlegs_B_{sym}.parquet"))
        L = L[(L["mode"] == "none") & (L.policy == "1 micro") & (L.leg == 0)].reset_index(drop=True)
        assert (L.t_exit < wf.HOLDOUT_SESSION_START).all()
        r = L.loc[rng.choice(len(L), 4, replace=False)].assign(group="random")
        los = L[(L.pnl_usd < 0) & ~L.index.isin(r.index)]
        lo = los.loc[rng.choice(los.index.to_numpy(), 2, replace=False)].assign(group="loser")
        rows += [r, lo]
    return pd.concat(rows, ignore_index=True)


def chart(sym, b, ctx, r, path):
    i_sig = b.index.get_loc(r.t_sig)
    i_ent = b.index.get_loc(r.t_entry)
    i_ex = int(b.index.searchsorted(r.t_exit - pd.Timedelta(minutes=1), side="right") - 1)   # bar holding the exit minute
    lo, hi = max(0, i_sig - 60), min(len(b), i_ex + 12)
    B, C_ = b.iloc[lo:hi], ctx.iloc[lo:hi]
    fig, ax, axm = cs.new_figure()
    x, O, H, L, C = cs.draw_base(ax, axm, B, C_, sym)
    rr = np.nanmax(H) - np.nanmin(L)
    s, e, xx = i_sig - lo, i_ent - lo, i_ex - lo
    cs.ring(ax, s, s, L[s], H[s], cs.HILITE, rr)
    ax.hlines(r.stop0, e - 0.5, xx + 0.5, color=cs.BAD, lw=1.6, linestyles=(0, (4, 2)), zorder=6)
    ax.hlines(r.entry, e - 0.5, xx + 0.5, color=cs.HILITE, lw=1.2, zorder=6)
    side = "LONG" if r.d > 0 else "SHORT"
    cs.label(ax, e, r.entry, f"{side} entry {cs.fp(sym, r.entry)}", cs.HILITE, above=r.d < 0)
    cs.label(ax, e, r.stop0, f"stop {cs.fp(sym, r.stop0)}", cs.BAD, above=r.d < 0, fs=9.5, ha="right")
    ax.plot([xx], [r.exit_px], marker="X", ms=12, color=cs.EXITC, zorder=10)
    cs.label(ax, xx, r.exit_px, f"exit {cs.fp(sym, r.exit_px)}", cs.EXITC, above=r.d > 0)
    col = cs.GOOD if r.pnl_usd > 0 else cs.BAD
    ax.set_title(f"{MICRO[sym]} 15-min  |  signal {r.t_sig:%Y-%m-%d %H:%M} ET  |  {side}  |  {KIND.get(r.kind, r.kind)} "
                 f"{r.t_exit:%m-%d %H:%M}  |  net {r.pnl_usd:+.2f} USD per micro (stop risk {r.risk_usd:.0f} USD)",
                 color=col, fontsize=11.5, loc="left", pad=28)
    cs.save(fig, path)


def main():
    os.makedirs(OUT, exist_ok=True)
    P = pick()
    recs = []
    for sym in ("NQ", "ES", "YM"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            b = sg.bars(sym, TF)
            b = b[b.index < wf.HOLDOUT_SESSION_START]
            ctx = sg.context(b, tick=sg.SPEC[sym]["tick"])
        for k, r in P[P.market == sym].iterrows():
            name = f"{r.group}_{MICRO[sym]}_{r.t_sig:%Y%m%d_%H%M}_{'long' if r.d > 0 else 'short'}.png"
            # hand check: entry = open of the bar after the signal bar (+/- 1 tick slippage is in pnl, not in entry)
            i_ent = b.index.get_loc(r.t_entry)
            assert b.index.get_loc(r.t_sig) + 1 == i_ent, (sym, r.t_sig)
            chart(sym, b, ctx, r, os.path.join(OUT, name))
            recs.append(dict(file=name, group=r.group, market=MICRO[sym], side="long" if r.d > 0 else "short",
                             signal=r.t_sig, entry_time=r.t_entry, exit_time=r.t_exit, entry=r.entry,
                             bar_open=float(b.O.iloc[i_ent]), stop=r.stop0, exit=r.exit_px,
                             exit_kind=KIND.get(r.kind, r.kind), pnl_usd=r.pnl_usd, risk_usd=r.risk_usd))
            print(name, flush=True)
        del b, ctx
    pd.DataFrame(recs).to_csv(os.path.join(OUT, "gallery.csv"), index=False)


if __name__ == "__main__":
    sys.exit(main())
