"""Cut small per-example 1-minute slices (run ONCE, under the heavy lock). Each market's 1-minute file is loaded once
(research_lib.bars_1m, research_lib.py:223-239: Databento 1-minute bars, New York time, sess = (ts + 6h).date).
Slice per example = [decision - 30 h, max(exit, decision + 1 h) + 30 min], cut before the locked holdout
(2025-06-30 18:00 ET). Output: slices/<example_id>_1m.parquet with O H L C V inst sess (tz-naive New York time)."""
import os

import numpy as np
import pandas as pd

import research_lib as rl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slices")
os.makedirs(OUT, exist_ok=True)
HOLDOUT = pd.Timestamp("2025-06-30 18:00")
ex = pd.read_csv(os.path.join(HERE, "examples.csv"), parse_dates=["decision_time", "entry_time", "exit_time"])
for sym, g in ex.groupby("sym"):
    m = rl.bars_1m(sym)
    idx = m.index.tz_localize(None)
    f = pd.DataFrame({"O": m.Open.to_numpy(np.float64), "H": m.High.to_numpy(np.float64), "L": m.Low.to_numpy(np.float64),
                      "C": m.Close.to_numpy(np.float64), "V": m.Volume.to_numpy(np.float64),
                      "inst": m.instrument_id.to_numpy(), "sess": m.sess.to_numpy()}, index=idx)
    del m
    for r in g.itertuples():
        t0 = r.decision_time - pd.Timedelta(hours=30)
        ex_t = r.exit_time if pd.notna(r.exit_time) else r.decision_time
        t1 = min(max(ex_t, r.decision_time + pd.Timedelta(hours=1)) + pd.Timedelta(minutes=30), HOLDOUT)
        s = f[(f.index >= t0) & (f.index < t1)]
        assert s.index.max() < HOLDOUT
        s.to_parquet(os.path.join(OUT, f"{r.example_id}_1m.parquet"))
        print(sym, r.example_id, len(s), s.index.min(), s.index.max(), flush=True)
    del f
