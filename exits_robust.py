"""Robustness checks for the classic setups with run-to-close / trailing exits:
  - direction- and time-matched random control (same direction, same time of day, random session in the same year)
  - longs vs shorts
  - 2 ticks slippage per side instead of 1
Usage:  PYTHONPATH=./pylib python3 exits_robust.py"""
import warnings
import numpy as np
import pandas as pd
import exits_compare as ec
import exits_engine as ee
warnings.filterwarnings("ignore")
ec.init()
CHECK = [("NQ", "Overnight break + daily trend", "trail_6", 2), ("NQ", "Overnight break + daily trend", "hold", 2),
         ("NQ", "OR break + 60m trend", "ema60", 2), ("NQ", "IB break + 60m trend", "target_2", 4),
         ("ES", "Overnight break + daily trend", "trail_6", 4)]
rows = []
for sym, ent, ex, k in CHECK:
    D = ec.G[sym]; sp = ee.SPEC[sym]; sig = ec.G[("sets", sym)][ent]
    t = ee.run(D, sig, ex, k0=k)
    t["usd"] = t.pts * sp["usd"] - sp["comm"]; t["year"] = D.year[t.bar]
    # direction/time-matched random control: 20 draws per trade
    rng = np.random.default_rng(0)
    by_year_tmin = pd.DataFrame({"i": np.arange(D.n), "y": D.year, "tm": D.tmin}).query("i not in @D.day_end")
    groups = {k_: g.i.to_numpy() for k_, g in by_year_tmin.groupby(["y", "tm"])}
    ctrl = []
    for _, tr in t.iterrows():
        pool = groups.get((D.year[tr.bar], D.tmin[tr.bar]))
        for j in rng.choice(pool, 20):
            r = ee.simulate(D, int(j), int(tr.dir), ex, k)
            if r: ctrl.append((int(tr.dir), r[1] * sp["usd"] - sp["comm"]))
    c = pd.DataFrame(ctrl, columns=["dir", "usd"])
    # 2 ticks slippage
    ee.SLIP = 0.5; t2 = ee.run(D, sig, ex, k0=k); ee.SLIP = 0.25
    u2 = t2.pts * sp["usd"] - sp["comm"]
    rows.append({"market": sp["micro"], "setup": ent, "exit/stop": f"{ex} / {k}", "trades": len(t),
                 "$/trade": t.usd.mean(), "matched-random $/trade": c.usd.mean(),
                 "edge vs matched random": t.usd.mean() - c.usd.mean(),
                 "longs n": int((t.dir > 0).sum()), "longs $/tr": t[t.dir > 0].usd.mean(),
                 "matched-random longs $/tr": c[c.dir > 0].usd.mean(),
                 "shorts n": int((t.dir < 0).sum()), "shorts $/tr": t[t.dir < 0].usd.mean(),
                 "matched-random shorts $/tr": c[c.dir < 0].usd.mean(),
                 "net @1 tick": t.usd.sum(), "net @2 ticks": u2.sum()})
    yr = t.groupby("year").usd.sum().round(0)
    print(f"{sp['micro']} | {ent} | {ex}/{k}: by year " + ", ".join(f"{y}: {v:+,.0f}" for y, v in yr.items()), flush=True)
pd.set_option("display.width", 260)
print(pd.DataFrame(rows).round(2).T.to_string())
