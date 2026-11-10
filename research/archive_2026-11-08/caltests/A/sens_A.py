# Sensitivity (not trials): how much do the ambiguous early-close conventions move test 1?
import os, sys, numpy as np, pandas as pd
O = os.path.dirname(os.path.abspath(__file__))
src = open(f"{O}/caltests_A.py").read()
head = src.split("# TEST 2:")[0]          # data + test-1 code only
alt = os.environ.get("ALT")
if alt == "zn_last":   # ZN close/pre-close as-of 16:00/15:00 even on early-close days (i.e. ZN's own last bar)
    head = head.replace('("C", 16, 13), ("P", 15, 12)', '("C", 16, 16), ("P", 15, 15)')
if alt == "es_pre_1259":   # ES pre-close on early-close days = 12:59 close (no 5-min lag)
    head = head.replace('("P", 954, 774)', '("P", 954, 779)').replace('cache_{sym}_daily.pkl', 'cache_{sym}_daily_alt.pkl')
head = head.replace('ev.to_csv', 'pass  #')
exec(compile(head, "head", "exec"))
base = pd.read_csv(f"{O}/events_1_primary.csv")
print(alt, "net mean", round(ev1p.net_usd.mean(), 3), "t", round(tstat(ev1p.net_usd), 3), "total", ev1p.net_usd.sum(),
      "| events with different net$ vs base:", int((np.abs(ev1p.net_usd.values - base.net_usd.values) > 1e-9).sum()),
      "| 1b net mean", round(ev1b.net_usd.mean(), 3))
