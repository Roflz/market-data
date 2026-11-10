"""Targeted no-look-ahead check for the v2 TOM rule at the 10 swapped sessions: truncate each market's data at the
18:00 mark (k = 0) of the Labor Day session and of the following Tuesday and recompute the first-trading-day list
from the truncated calendar only. Light."""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import g3
import harness as H
LD = pd.DatetimeIndex(["2012-09-03", "2014-09-01", "2018-09-03", "2019-09-02", "2024-09-02"])
ok = True
for sym in g3.MKTS:
    idx = H.sessions(sym).index
    for d in list(LD) + list(LD + pd.Timedelta(days=1)):
        if d not in idx:
            continue
        Sc, _ = H.truncate(sym, d, 0, tfs=())
        tom_c = g3.first_trading_days(Sc.index)
        e = g3.sig_event([("1800", "0930", 1)], "tom")(Sc, {})
        want = d.dayofweek == 1
        r = (d in tom_c) == want and (d in set(pd.DatetimeIndex(e.session))) == want and (Sc.index.max() == d)
        ok &= bool(r)
        print(sym, d.date(), d.day_name()[:3], "TOM from truncated data:", d in tom_c, "| expected:", want, "| ok", r)
print("ALL TARGETED TOM CUTS PASSED" if ok else "FAILURE")
assert ok
