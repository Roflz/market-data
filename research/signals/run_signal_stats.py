"""
Detect every pattern on one market and timeframe and measure what followed. One market/timeframe per run, so memory
stays small; run_all.sh runs them one after another with a memory cap.

  PYTHONPATH=../../pylib:../..:. python3 run_signal_stats.py ES 15

Writes to out/:
  stats_{SYM}_{TF}.csv     per pattern and direction: count, per year, share of bars; signed forward move (ATRs) at
                           1/3/5/10/20 bars and the EDGE over all bars (signed drift removed); hit rate; t; points and
                           $ per micro at 5 bars after costs (all years and 2022-26); best rise / worst fall over 10 bars;
                           by era. Neutral patterns: average absolute move vs all bars (does a big move follow?).
  context_{SYM}_{TF}.csv   per pattern and direction: share of signals in each state of every context signal (trend
                           with/against, momentum turning with/against, near support/resistance, above/below VWAP,
                           close location, time of day, volatility regime) next to the share among all bars.
  cond_{SYM}_{TF}.csv      forward results of directional patterns split by context agreement (the "more confirming
                           signals" test): trend, momentum slope, nearby level, VWAP side, and the number agreeing (0-4).
  events_{SYM}_{TF}.parquet  every bar with at least one pattern (15-minute and slower): patterns, context, forward moves.
Entry is at the next bar's open after the signal bar closes; forward moves never cross a session end or contract roll.
"""
import sys
import time
import warnings

import numpy as np
import pandas as pd

import signals as sg

warnings.filterwarnings("ignore")
SYM, TF = sys.argv[1], int(sys.argv[2])
OUT = "out"
ERAS = {"2010-17": ("2010", "2017"), "2018-21": ("2018", "2021"), "2022-26": ("2022", "2026")}
t0 = time.time()
spec = sg.SPEC[SYM]
b = sg.bars(SYM, TF)
c = sg.context(b, tick=spec["tick"])
p = sg.patterns(b, c, tick=spec["tick"])
f = sg.forward(b, c)
years = (b.index[-1] - b.index[0]).days / 365.25
valid = f.fwd5_atr.notna() & c.atr14.notna()
raw_ok = (b.H - b.L).rolling(14).mean().gt(spec["tick"])   # skip dead stretches (average 1-bar range <= 1 tick)
valid &= raw_ok
base = {h: f[f"fwd{h}_atr"][valid].mean() for h in sg.HORIZONS}
base_abs5 = f.fwd5_atr[valid].abs().mean()
base_pts5 = f.fwd5_pts[valid].mean()
base_up, base_dn = f.up10_atr[valid].mean(), f.down10_atr[valid].mean()
print(f"{SYM} {TF}m: {len(b):,} bars {b.index[0]:%Y-%m-%d} -> {b.index[-1]:%Y-%m-%d}, built in {time.time() - t0:.0f}s", flush=True)

# context states (relative to the signal's direction where it has one)
def ctx_states(d):
    """d: +1/-1 array per row (direction), or 0 for neutral. Returns dict of categorical Series."""
    tr, ms = c.trend, c.mom_slope
    near_sup, near_res = c.dist_sup.lt(0.5), c.dist_res.lt(0.5)
    above_vwap = c.dist_vwap.gt(0)
    s = {}
    if d is None:
        s["trend"] = tr.map({1: "up", 0: "mixed", -1: "down"})
        s["momentum"] = ms.map({1: "rising", 0: "flat", -1: "falling"})
        s["near support (<0.5 ATR)"] = near_sup.map({True: "yes", False: "no"})
        s["near resistance (<0.5 ATR)"] = near_res.map({True: "yes", False: "no"})
        s["vs VWAP"] = above_vwap.map({True: "above", False: "below"})
    else:
        s["trend"] = np.where(tr == 0, "mixed", np.where(tr == d, "with", "against"))
        s["momentum"] = np.where(ms == 0, "flat", np.where(ms == d, "turning with", "turning against"))
        s["level in signal direction"] = np.where(np.where(d > 0, near_sup, near_res), "at support/resistance", "not near")
        s["vs VWAP"] = np.where(np.where(d > 0, ~above_vwap, above_vwap), "on the cheap side", "on the rich side")
    s["mom14 above 100"] = c.mom14.gt(100).map({True: "yes", False: "no"})
    s["close location"] = pd.cut(c.clv, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]).astype(str)
    s["volatility"] = pd.cut(c.vol_regime, [0, 0.8, 1.2, 99], labels=["calm (<0.8x)", "normal", "high (>1.2x)"]).astype(str)
    s["time of day"] = c.tod
    return {k: pd.Series(v, index=b.index) for k, v in s.items()}


all_states = ctx_states(None)
rows, ctx_rows, cond_rows = [], [], []
for name, (kind, rule) in sg.PATTERN_RULES.items():
    col = p[name]
    dirs = [1, -1] if kind == "dir" else [1]
    for d in dirs:
        m = (col == d) & valid
        n = int(m.sum())
        lab = ("bullish" if d > 0 else "bearish") if kind == "dir" else "present"
        r = dict(market=SYM, tf=TF, pattern=name, direction=lab, rule=rule, n=n, per_year=n / years,
                 share_of_bars=n / valid.sum())
        if n < 30:
            rows.append(r); continue
        sgn = d if kind == "dir" else 1
        for h in sg.HORIZONS:
            r[f"pts{h}"] = (sgn * f[f"fwd{h}_pts"][m]).mean()
            x = sgn * f[f"fwd{h}_atr"][m]
            r[f"move{h}_atr"] = x.mean()
            r[f"edge{h}_atr"] = x.mean() - sgn * base[h]
        x5 = sgn * f.fwd5_atr[m]
        r["hit5"] = (x5 > 0).mean()
        r["t5"] = r["edge5_atr"] / (x5.std() / np.sqrt(n))
        pts5 = sgn * f.fwd5_pts[m]
        r["pts5"] = pts5.mean()
        r["edge5_pts"] = pts5.mean() - sgn * base_pts5
        r["hit5_all"] = (sgn * f.fwd5_pts[valid] > 0).mean()
        r["usd5_per_micro"] = pts5.mean() * spec["usd"] - spec["cost"]
        late = m & (b.index >= "2022-01-01")
        r["usd5_per_micro_2022_26"] = (sgn * f.fwd5_pts[late]).mean() * spec["usd"] - spec["cost"] if late.sum() >= 30 else np.nan
        if kind == "dir":
            fav, adv = (f.up10_atr, f.down10_atr) if d > 0 else (f.down10_atr, f.up10_atr)
            r["best_move10_atr"], r["worst_move10_atr"] = fav[m].mean(), adv[m].mean()
            r["best_move10_all"] = base_up if d > 0 else base_dn
        else:
            r["abs_move5_atr"], r["abs_move5_all"] = f.fwd5_atr[m].abs().mean(), base_abs5
        for e, (a, z) in ERAS.items():
            mm = m & (b.index >= a) & (b.index <= f"{z}-12-31 23:59")
            r[f"edge5_{e}"] = (sgn * f.fwd5_atr[mm]).mean() - sgn * base[5] if mm.sum() >= 30 else np.nan
            r[f"n_{e}"] = int(mm.sum())
        rows.append(r)
        # context shares at the signal vs all bars
        st = ctx_states(d if kind == "dir" else None)
        for feat, ser in st.items():
            sh = ser[m].value_counts(normalize=True)
            if kind == "dir":                       # baseline: same relative state for a random bar with this direction
                allsh = ser[valid].value_counts(normalize=True)
            else:
                allsh = all_states[feat][valid].value_counts(normalize=True)
            for lvl in sorted(set(sh.index) | set(allsh.index)):
                if lvl in ("nan", "None"):
                    continue
                ctx_rows.append(dict(market=SYM, tf=TF, pattern=name, direction=lab, signal=feat, state=lvl,
                                     share_at_pattern=sh.get(lvl, 0.0), share_all_bars=allsh.get(lvl, 0.0)))
        # forward results split by context agreement (directional patterns only)
        if kind == "dir":
            agree = {"trend": (c.trend == d), "momentum": (c.mom_slope == d),
                     "level": (c.dist_sup.lt(0.5) if d > 0 else c.dist_res.lt(0.5)),
                     "vwap": (c.dist_vwap.lt(0) if d > 0 else c.dist_vwap.gt(0))}
            for k, a in agree.items():
                for flag in (True, False):
                    mm = m & (a == flag)
                    if mm.sum() >= 30:
                        x = d * f.fwd5_atr[mm]
                        cond_rows.append(dict(market=SYM, tf=TF, pattern=name, direction=lab, split=k,
                                              group="agrees" if flag else "does not agree", n=int(mm.sum()),
                                              edge5_atr=x.mean() - d * base[5], hit5=(x > 0).mean(),
                                              usd5_per_micro=(d * f.fwd5_pts[mm]).mean() * spec["usd"] - spec["cost"]))
            score = sum(a.astype(int) for a in agree.values())
            for sc in range(5):
                mm = m & (score == sc)
                if mm.sum() >= 30:
                    x = d * f.fwd5_atr[mm]
                    cond_rows.append(dict(market=SYM, tf=TF, pattern=name, direction=lab, split="confirmations (0-4)",
                                          group=str(sc), n=int(mm.sum()), edge5_atr=x.mean() - d * base[5],
                                          hit5=(x > 0).mean(),
                                          usd5_per_micro=(d * f.fwd5_pts[mm]).mean() * spec["usd"] - spec["cost"]))

pd.DataFrame(rows).to_csv(f"{OUT}/stats_{SYM}_{TF}.csv", index=False)
pd.DataFrame(ctx_rows).to_csv(f"{OUT}/context_{SYM}_{TF}.csv", index=False)
pd.DataFrame(cond_rows).to_csv(f"{OUT}/cond_{SYM}_{TF}.csv", index=False)
if TF >= 15:
    anyp = (p != 0).any(axis=1)
    ev = pd.concat([b[["O", "H", "L", "C"]], p, c.drop(columns=["ema10"]), f], axis=1)[anyp]
    for col in ev.columns:
        if ev[col].dtype == np.float64:
            ev[col] = ev[col].astype(np.float32)
    ev.to_parquet(f"{OUT}/events_{SYM}_{TF}.parquet")
print(f"{SYM} {TF}m done in {time.time() - t0:.0f}s: {len(rows)} pattern rows", flush=True)
