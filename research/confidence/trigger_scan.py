"""
Raw trend-pullback triggers, NO model: does any entry rule make money on its own after costs?

Long rules (shorts are the mirror image). Everything is known at the CLOSE of signal bar t; entry = open of t+1.
  trend      EMA8 > EMA20 > EMA50 and EMA50 higher than 5 bars ago (EMAs as on the trader's charts).
  ema8_pb    trend; the bar dips to EMA8 (L <= EMA8), closes back above it, closes up (C > O), and stays above EMA20.
  ema20_pb   trend; the bar dips to EMA20 (L <= EMA20), closes back above it and closes up.
  ema50_pb   EMA20 > EMA50, EMA50 rising; the bar dips to EMA50, closes back above it and closes up (deep pullback).
  mom_turn   trend; Momentum(14) rose this bar after falling the 2 bars before, close above EMA20.
  pb_break   trend; after a pullback bar (its high below the bar before it), this bar CLOSES above that bar's high,
             and no low of the last 3 bars broke EMA50 (Brooks-style H1/H2 on a close, not a stop order).
  trend_all  benchmark: every bar in trend (what simply being with the trend + NQ's drift earns).
Stop = 1 tick beyond the lowest low of the last 5 bars (same contract), but at least 1 average bar (R20) from the
close. Labels: labels.label_entries (1-minute path, costs $1 + 1 tick each way, +1 tick on stop fills, target
1 / 1.5 / 2 R, 16-bar limit or 16:45 flat). Holdout (2025-06-30 18:00 on) never touched.
Judged by period: 2010-2020 = discovery, 2021-2025H1 = confirmation (a rule must hold up in BOTH).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 -u trigger_scan.py [NQ ES YM] [--tf 15,60]
"""
import argparse
import gc
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import features as fe
import labels as lb
import signals as sg
import walkforward as wf

RULES = ["ema8_pb", "ema20_pb", "ema50_pb", "mom_turn", "pb_break", "trend_all"]
STOP_LOOKBACK = 5


def detect(b, ctx, tick, tf):
    """Trigger events: DataFrame [t, i, d, rule, stop] (one row per rule, bar and direction)."""
    n = len(b)
    O, H, L, C = (b[c].to_numpy(np.float64) for c in "OHLC")
    run = b.run.to_numpy()
    e8, e20, e50 = (ctx[c].to_numpy(np.float64) for c in ("ema8", "ema20", "ema50"))
    mom = ctx["mom14"].to_numpy(np.float64)
    R = fe.r20(b, tick)
    ok, _ = lb.eligible(b, tf)

    def lag(x, k):
        out = np.full(n, np.nan)
        out[k:] = x[:-k]
        return np.where(fe._run_ok(run, k), out, np.nan)

    e50_5 = lag(e50, 5)
    lo5 = pd.Series(L).rolling(STOP_LOOKBACK).min().to_numpy()
    hi5 = pd.Series(H).rolling(STOP_LOOKBACK).max().to_numpy()
    full = fe._run_ok(run, STOP_LOOKBACK - 1) & np.isfinite(R) & np.isfinite(e50) & np.isfinite(e50_5)
    H1, L1, H2, L2 = lag(H, 1), lag(L, 1), lag(H, 2), lag(L, 2)
    m1, m2, m3 = lag(mom, 1), lag(mom, 2), lag(mom, 3)
    lo3, hi3 = np.fmin(L, np.fmin(L1, L2)), np.fmax(H, np.fmax(H1, H2))
    parts = []
    for d in (1, -1):
        # orient everything so that "up" means "with the trade": x -> d * x
        o, h, l, c = d * O, np.where(d > 0, H, -L), np.where(d > 0, L, -H), d * C
        a8, a20, a50, a50_5 = d * e8, d * e20, d * e50, d * e50_5
        h1, h2 = (np.where(d > 0, H1, -L1), np.where(d > 0, H2, -L2))
        lo3d = np.where(d > 0, lo3, -hi3)
        mo, mo1, mo2, mo3 = d * mom, d * m1, d * m2, d * m3          # momentum ratio around 100: sign via d
        trend = (a8 > a20) & (a20 > a50) & (a50 > a50_5)
        up_bar = c > o
        rules = {
            "ema8_pb": trend & (l <= a8) & (c > a8) & up_bar & (l > a20),
            "ema20_pb": trend & (l <= a20) & (c > a20) & up_bar,
            "ema50_pb": (a20 > a50) & (a50 > a50_5) & (l <= a50) & (c > a50) & up_bar,
            "mom_turn": trend & (mo > mo1) & (mo1 < mo2) & (mo2 < mo3) & (c > a20),
            "pb_break": trend & (h1 < h2) & (c > h1) & (lo3d > a50),
            "trend_all": trend,
        }
        base = ok & full
        if d > 0:
            stop = np.minimum(lo5 - tick, C - R)
        else:
            stop = np.maximum(hi5 + tick, C + R)
        for name, m in rules.items():
            i = np.flatnonzero(base & np.nan_to_num(m, nan=0).astype(bool))
            parts.append(pd.DataFrame({"i": i, "d": d, "rule": name, "stop": stop[i]}))
    ev = pd.concat(parts, ignore_index=True)
    ev.insert(0, "t", b.index[ev.i.to_numpy()])
    return ev.sort_values(["i", "d", "rule"]).reset_index(drop=True)


def summarize(lab, sym, tf):
    lab = lab.assign(year=pd.DatetimeIndex(lab["t"]).year)
    rows = []
    for (rule, d), g in lab.groupby(["rule", "d"]):
        for span, (y0, y1) in {"2010-2020": (2010, 2020), "2021-2025H1": (2021, 2025), "all": (2010, 2025)}.items():
            s = g[(g.year >= y0) & (g.year <= y1)]
            if not len(s):
                continue
            by = s.groupby("year")["pnl_usd_1.5"].sum()
            rows.append(dict(market=sym, tf=tf, rule=rule, side="long" if d > 0 else "short", span=span,
                             n=len(s), per_year=round(len(s) / max(by.size, 1)),
                             usd_1R=s["pnl_usd_1"].mean(), usd_15R=s["pnl_usd_1.5"].mean(),
                             usd_2R=s["pnl_usd_2"].mean(), hit_15R=s["y_1.5"].mean(),
                             years_pos=f"{int((by > 0).sum())}/{by.size}", risk_med=s["risk_usd"].median(),
                             t_stat=s["pnl_usd_1.5"].mean() / (s["pnl_usd_1.5"].std() / np.sqrt(len(s)))))
    return pd.DataFrame(rows)


def main(markets, tfs):
    out = []
    for sym in markets:
        tick = sg.SPEC[sym]["tick"]
        m1 = lb.load_1m(sym)
        m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
        for tf in tfs:
            t0 = time.time()
            b, ctx = fe._load(sym, tf)
            keep = b.index < wf.HOLDOUT_SESSION_START
            b, ctx = b.loc[keep], ctx.loc[keep]
            ev = detect(b, ctx, tick, tf)
            lab = lb.label_entries(sym, tf, b, ev, m1=m1)
            lab.to_parquet(f"out/triggers_{sym}_{tf}.parquet", compression="zstd")
            S = summarize(lab, sym, tf)
            out.append(S)
            pd.concat(out).to_csv("out/trigger_scan.csv", index=False)
            v = S[S.span != "all"].pivot_table(index=["rule", "side"], columns="span", values="usd_15R").round(2)
            print(f"\n{sym} {tf}m: {len(lab):,} labelled trades ({time.time() - t0:.0f}s); $/trade at 1.5R:\n"
                  f"{v.to_string()}", flush=True)
            fe.clear_cache(); gc.collect()
        del m1; gc.collect()
    print("done", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("markets", nargs="*", default=["NQ", "ES", "YM"])
    ap.add_argument("--tf", default="15,60")
    a = ap.parse_args()
    main(a.markets, [int(x) for x in a.tf.split(",")])
