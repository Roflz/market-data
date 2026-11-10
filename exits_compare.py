"""
Compare exit methods x initial stop sizes on the same entries, ES and NQ futures, 2011-2026.
Trades run across the Globex session (overnight included) and are flattened at the 5:00 PM ET close.

Entry sets
  RANDOM s1..s3   : ~1 random entry per session, random direction (shows what exits do on their own)
  classic setups  : IB / opening-range / overnight-level break + trend filter, and the 15m+60m trend pullback
                    (decisions at 5-min closes, 9:35-15:00 ET)
Grid: 14 exit methods x initial stop {1, 2, 3, 4, 6} x 5-min ATR. One position at a time, max 3 trades per session.

Outputs exits_compare_raw.csv (one row per market x entry set x exit x stop x year).
Usage:  PYTHONPATH=./pylib python3 exits_compare.py
"""
import os
import time
import warnings
from multiprocessing import Pool

import numpy as np
import pandas as pd

import exits_engine as ee
from common import stats
import setup_rule

warnings.filterwarnings("ignore")
STOPS = [1, 2, 3, 4, 6]
SEEDS = [1, 2, 3]
FIRST_YEAR = 2011
G = {}


def entry_sets(sym):
    D = G[sym]
    sets = {}
    ok = np.ones(D.n, bool)
    ok[D.day_end] = False                                       # need at least one bar after the signal
    for s in SEEDS:
        r = np.random.default_rng(s)
        pick = np.flatnonzero(ok & (r.random(D.n) < 1 / 276))
        sets[f"RANDOM s{s}"] = list(zip(pick.tolist(), r.choice([-1, 1], len(pick)).tolist()))
    F = pd.read_pickle(f"data/fut_features_{sym}.pkl")
    bar = D.pos.get_indexer(pd.DatetimeIndex(F["ts"]) - pd.Timedelta(minutes=4))
    sig = setup_rule.overnight_break(F["X"], F["ts"])
    m = (sig != 0) & (bar >= 0)
    sets[setup_rule.NAME] = sorted(zip(bar[m].tolist(), sig[m].tolist()))
    return sets


def init():
    for sym in ("ES", "NQ"):
        b = pd.read_pickle(f"data/x5_{sym}.pkl")
        D = ee.Day(b[b.index.year >= FIRST_YEAR])
        D.pos = pd.Index(D.idx)
        G[sym] = D
        G[("sets", sym)] = entry_sets(sym)


def work(task):
    sym, ename, rule, k0 = task
    D = G[sym]
    t = ee.run(D, G[("sets", sym)][ename], rule, k0=k0)
    if t.empty:
        return []
    sp = ee.SPEC[sym]
    t["usd"] = t.pts * sp["usd"] - sp["comm"]
    bars = t.bar.to_numpy()
    t["year"], t["date"] = D.year[bars], D.sess[bars]
    rows = []
    for y, g in t.groupby("year"):
        s = stats(g.usd.to_numpy(), g.date.to_numpy())
        rows.append({"sym": sp["micro"], "entry": ename, "exit": rule, "stop_atr": k0, "year": int(y), **s,
                     "avg_hold_min": float(g.hold_bars.mean() * 5), "avg_mfe_R": float(g.mfe_R.mean())})
    return rows


def main():
    t0 = time.time()
    init()
    tasks = [(sym, e, x, k) for sym in ("ES", "NQ") for e in G[("sets", sym)] for x in ee.EXITS for k in STOPS]
    n_sets = len(G[("sets", "ES")])
    print(f"{len(tasks)} runs = 2 markets x {n_sets} entry sets x {len(ee.EXITS)} exits x {len(STOPS)} stops, "
          f"{os.cpu_count()} cores", flush=True)
    rows = []
    with Pool(os.cpu_count(), initializer=init) as p:          # Python 3.14 starts workers fresh: load data in each
        for i, res in enumerate(p.imap_unordered(work, tasks, chunksize=2), 1):
            rows += res
            if i % 100 == 0:
                print(f"  {i}/{len(tasks)} runs done ({time.time() - t0:.0f}s)", flush=True)
    pd.DataFrame(rows).to_csv("exits_compare_raw.csv", index=False)
    print(f"done in {time.time() - t0:.0f}s; saved exits_compare_raw.csv", flush=True)


if __name__ == "__main__":
    main()
