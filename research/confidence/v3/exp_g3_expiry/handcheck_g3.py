"""HEAVY (loads raw 1-minute data; run under the shared flock): re-price 10 G3 trades by hand from the RAW
research_lib.bars_1m rows (handcheck_harness.hand: open of the 1-minute bar at the mark, else the last close before
it, same contract) and compare with the harness trade tables written by g3.py.
10 trades: A3 3 MES + 3 MNQ + 2 MYM, S3.2 1 MES (18:00 -> 09:30), S3.6-NQ 1 MNQ (15:00 -> 16:00).
Output: v3/exp_g3_expiry/handcheck_g3.csv"""
import gc
import os

import numpy as np
import pandas as pd

import harness as H
import handcheck_harness as hh
import research_lib as rl

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", "trades")
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261109)
pick = {"ES": [], "NQ": [], "YM": []}
for hid, sym, n in (("A3", "ES", 3), ("A3", "NQ", 3), ("A3", "YM", 2), ("S3.2", "ES", 1), ("S3.6-NQ", "NQ", 1)):
    t = pd.read_parquet(os.path.join(OUT, f"{hid}.parquet"))
    t = t[t.market == sym]
    for i in rng.choice(len(t), size=n, replace=False):
        pick[sym].append((hid, t.iloc[i]))
rows = []
for sym in ("ES", "NQ", "YM"):
    if not pick[sym]:
        continue
    m = rl.bars_1m(sym)
    for hid, t in pick[sym]:
        D = pd.Timestamp(t.session)
        e, x, kind, pnl, _, _ = hh.hand(m, sym, D, H.mark_index(t.entry), H.mark_index(t.exit), int(t.d), np.nan)
        rows.append(dict(hid=hid, market=sym, session=D.date(), entry=t.entry, exit=t.exit, d=int(t.d),
                         h_entry_px=t.entry_px, hand_entry_px=e, h_exit_px=t.exit_px, hand_exit_px=x,
                         h_kind=t.exit_kind, hand_kind=kind, h_pnl=t.pnl_usd, hand_pnl=pnl,
                         match=bool(abs(pnl - t.pnl_usd) < 1e-9 and kind == t.exit_kind)))
    del m
    gc.collect()
out = pd.DataFrame(rows)
out.to_csv(os.path.join(HERE, "handcheck_g3.csv"), index=False)
pd.set_option("display.width", 250)
print(out.to_string())
print(f"hand-check: {out.match.sum()} / {len(out)} trades match")
