"""
G1 runner: builds every pre-registered G1 column (A1, S1.1-S1.6, neighbours), runs the C1 matched control
(R = 999 draws, chunks of 100), the reported controls, gates, and writes the standard outputs.

  stage 'build'  : signals + look-ahead checks + trades + C1 matrices -> exp_g1_noiseband/cache/
  stage 'report' : statistics, gates, controls, eval, outputs, trial log

Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 OMP_NUM_THREADS=3 \
      python3 v3/exp_g1_noiseband/run_g1.py build|report
"""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g1lib as G                        # noqa: E402
from g1lib import H, sp                  # noqa: E402

CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)
OUT = os.path.join(G.V3, "out")
for d_ in ("daily", "trades", "results"):
    os.makedirs(os.path.join(OUT, d_), exist_ok=True)
EXPG1 = os.path.join(G.V3, "exp_G1")
os.makedirs(EXPG1, exist_ok=True)
warnings.filterwarnings("ignore", message="time_trades")

# --------------------------------------------------------------------------------------------- column specs
ES_S = H.sessions("ES")
ES_DROP = frozenset(ES_S.index[ES_S["prev_ret_cc"] <= -0.02])          # S1.5: known at the open (prev_ column)


def vol_skip(sym="NQ", burn=250):
    """S1.4: trade only when mean prev_rv_rth over the 20 previous sessions (rolling 20 of prev_rv_rth incl. the
    current row = rv_rth of sessions d-20..d-1, all known at the open) is in the middle or top tercile of its
    expanding history (quantiles of strictly earlier values; burn-in 250 sessions as the lit_p1 reference).
    Returns the fixed set of sessions to SKIP."""
    S = H.sessions(sym)
    v = S["prev_rv_rth"].rolling(20, min_periods=15).mean().to_numpy()
    skip = set()
    hist = []
    for i, s in enumerate(S.index):
        x = v[i]
        if not np.isfinite(x):
            skip.add(s)
            continue
        if len(hist) >= burn:
            q1 = np.quantile(hist, 1 / 3)
            if x <= q1:
                skip.add(s)
        else:
            skip.add(s)
        hist.append(x)
    return frozenset(skip)


COLS = {
    # hid: (market(s), make_signal kwargs, C1 seed base, kind)
    "A1": ("NQ", {}, 1000, "primary"),
    "S1.1": ("ES", {}, 1100, "secondary"),
    "S1.2": ("YM", {}, 1200, "secondary"),
    "S1.6": ("NQ", {"final_exit": "1645"}, 1600, "secondary"),
    "N1.lb10": ("NQ", {"lookback": 10}, 1700, "neighbour"),
    "N1.lb20": ("NQ", {"lookback": 20}, 1800, "neighbour"),
    "N1.hour": ("NQ", {"dec": G.DEC_HOUR}, 1900, "neighbour"),
}
SUBSETS = {"S1.4": "vol", "S1.5": "esdrop"}                                 # subsets of A1's trades (same C1)
LABELS = {
    "A1": "noise band variant A, MNQ (Tier A primary)",
    "S1.1": "noise band A on MES", "S1.2": "noise band A on MYM", "S1.3": "noise band A, 3-market basket",
    "S1.4": "A1 MNQ, only mid/top tercile of trailing 20-session RTH vol",
    "S1.5": "A1 MNQ, skip sessions after ES prev_ret_cc <= -2%", "S1.6": "A1 MNQ, exit 16:45 instead of 16:00",
    "N1.lb10": "neighbour: lookback 10", "N1.lb20": "neighbour: lookback 20",
    "N1.hour": "neighbour: decisions on the hour only", "N1.cost": "neighbour: +1 tick each way cost",
}


def build():
    t0 = time.time()
    log = []
    for hid, (sym, kw, seed, kind) in COLS.items():
        early = G.early_set(sym)
        fn = G.make_signal(early, **kw)
        S = H.sessions(sym)
        B = {5: H.bars(sym, 5)}
        legs = fn(S, B)
        # mandatory no-look-ahead check on the decision legs (exit = calendar-fixed next decision)
        if hid in ("A1", "S1.1", "S1.2", "S1.6", "N1.hour"):
            chk = H.lookahead_check(fn, sym, n_cuts=20, seed=0, tfs=(5,))
            log.append(f"{hid}: lookahead_check 20 cuts OK, legs compared {int(chk.n_full.sum())}")
        ent = G.merge_legs(legs)
        ent = ent[pd.DatetimeIndex(ent.session) <= G.LAST].reset_index(drop=True)
        ent["tid0"] = np.arange(len(ent))
        tr = H.time_trades(sym, ent)
        log.append(f"{hid}: time_trades dropped {tr.attrs.get('dropped')}")
        ent = ent.loc[tr["tid0"].to_numpy()].reset_index(drop=True)
        tr = tr.drop(columns=["tid0"]).reset_index(drop=True)
        ent = ent.drop(columns=["tid0"])
        assert len(tr) == len(ent)
        tr.to_parquet(os.path.join(CACHE, f"tr_{hid}.parquet"))
        M, tabs = G.c1_matrix(sym, ent, R=999, seed_base=seed, keep_tables=200 if hid in ("A1", "S1.1") else 0)
        np.save(os.path.join(CACHE, f"M_{hid}.npy"), M)
        if tabs:
            pd.concat([t.assign(rep=i) for i, t in enumerate(tabs)], ignore_index=True).to_parquet(
                os.path.join(CACHE, f"twins_{hid}.parquet"))
        log.append(f"{hid}: {len(tr)} trades, legs {len(legs)}, C1 drawn {np.isfinite(M).mean():.4f} "
                   f"({time.time() - t0:.0f}s)")
        print(log[-1], flush=True)
    # subsets: rebuild through the signal with a fixed skip set and check they equal the A1 subset
    trA = pd.read_parquet(os.path.join(CACHE, "tr_A1.parquet"))
    for hid, which in SUBSETS.items():
        skip = vol_skip("NQ") if which == "vol" else ES_DROP
        fn = G.make_signal(G.early_set("NQ"), skip=skip)
        ent = G.merge_legs(fn(H.sessions("NQ"), {5: H.bars("NQ", 5)}))
        ent = ent[pd.DatetimeIndex(ent.session) <= G.LAST].reset_index(drop=True)
        ent["tid0"] = np.arange(len(ent))
        ent = ent.loc[H.time_trades("NQ", ent)["tid0"].to_numpy()].reset_index(drop=True)
        mask = ~pd.DatetimeIndex(trA.session).isin(pd.DatetimeIndex(sorted(skip)))
        sub = trA.loc[mask]
        same = (len(sub) == len(ent) and (pd.DatetimeIndex(sub.session) == pd.DatetimeIndex(ent.session)).all()
                and (sub.entry.to_numpy() == np.array(H.MARKS)[ent.entry.to_numpy()]).all())
        assert same, f"{hid} subset mismatch"
        np.save(os.path.join(CACHE, f"mask_{hid}.npy"), mask.to_numpy() if hasattr(mask, "to_numpy") else mask)
        if which == "vol":
            chk = H.lookahead_check(fn, "NQ", n_cuts=20, seed=1, tfs=(5,))
            log.append(f"{hid}: lookahead_check OK")
        log.append(f"{hid}: subset of A1, {int(np.sum(mask))} trades (rebuilt through the signal: identical)")
        print(log[-1], flush=True)
    # truncation re-check of 20 random merged A1 trades: cut at the trade's EXIT mark, rebuild, same trade
    rng = np.random.default_rng(7)
    fn = G.make_signal(G.early_set("NQ"))
    pick = rng.choice(len(trA), 20, replace=False)
    ok = 0
    for i in pick:
        r = trA.iloc[i]
        Sc, Bc = H.truncate("NQ", r.session, r.exit, tfs=(5,))
        e2 = G.merge_legs(fn(Sc, Bc))
        e2 = e2[pd.DatetimeIndex(e2.session) == r.session]
        hit = e2[(np.array(H.MARKS)[e2.entry.to_numpy()] == r.entry) & (e2.d.to_numpy() == r.d)
                 & (np.array(H.MARKS)[e2.exit.to_numpy()] == r.exit)]
        ok += int(len(hit) == 1)
    log.append(f"A1 truncation re-check (cut at exit mark): {ok}/20 trades reproduced")
    print(log[-1], flush=True)
    with open(os.path.join(HERE, "build_log.txt"), "w") as f:
        f.write("\n".join(log) + f"\nbuild time {time.time() - t0:.0f}s\n")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "build"
    if stage == "build":
        build()
