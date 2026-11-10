"""v5/sess_har.py - per-SESSION HAR-log daily RV forecast and 09:30-16:00 periodicity share for every session
2018-01-01 .. 2025-06-27 (needed to give the A3 C1 twins - random sessions - their own forecast).
Uses the v5/vol.py functions unchanged (same data, same causal construction as trades_vol.parquet).
Check: on the real A3 trade sessions the values must equal trades_vol.parquet's har_log_d / share.
Heavy (1-minute load): run under the heavy.lock flock, one market at a time.
  python3 v5/sess_har.py ES|NQ|YM  -> v5/out/_sess_har_{sym}.parquet
"""
import os
import sys

import numpy as np
import pandas as pd

import vol as V

sym = sys.argv[1]
import harness as H  # noqa: E402

S = H.sessions(sym)
tg = S.index[(S.index >= V.FIRST) & (S.index <= V.LAST)].to_numpy().astype("datetime64[ns]")
d = V.load(sym)
sessions, r2, valid = V.grid(d)
del d
F = V.har_forecasts(sessions, r2, valid, tg)
F["share"] = [V.per_share(sessions, r2, valid, t, 9 * 60 + 30, V.W1) for t in tg]
F.index.name = "session"
F = F.reset_index()
F["market"] = sym
F.to_parquet(os.path.join(V.OUT, f"_sess_har_{sym}.parquet"))
tv = pd.read_parquet(os.path.join(V.OUT, "trades_vol.parquet"))
tv = tv[(tv.rule == "A3") & (tv.market == sym)]
m = tv.merge(F, on="session", suffixes=("", "_s"))
ok = np.isclose(m.har_log_d, m.har_log_d_s, rtol=1e-9, equal_nan=True) & np.isclose(m.share, m.share_s, rtol=1e-9,
                                                                                      equal_nan=True)
print(sym, "sessions", len(F), "A3 check", int(ok.sum()), "/", len(m), "har NaN", int(F.har_log_d.isna().sum()))
assert ok.all(), "per-session forecast differs from trades_vol"
