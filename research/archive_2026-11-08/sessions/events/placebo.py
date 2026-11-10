"""Placebo: same scan at every :00/:30 ET clock time on all cash sessions (18:00 ET evening before .. 15:30 ET)."""
import sys
sys.path.insert(0, "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/sessions/events")
import numpy as np, pandas as pd
import event_cont as ec
cash = ec.sess.index[ec.sess.cash_day]
ev = []
for hh in list(range(18, 24)) + list(range(0, 16)):
    for mm in (0, 30):
        days = cash - pd.Timedelta(days=1) if hh >= 18 else cash
        ev.append((f"{hh:02d}:{mm:02d} ET", ec.et_event_on_sessions(f"{hh:02d}:{mm:02d}", days), "any"))
res = pd.concat([ec.run_market(s, ev) for s in ("NQ", "ES")], ignore_index=True)
res.to_csv(f"{ec.OUT}/placebo_clock_times.csv", index=False)
print(len(res))
