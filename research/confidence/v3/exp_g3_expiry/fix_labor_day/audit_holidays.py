"""Audit: which G3 event days / control draws fall on NYSE holiday Globex sessions. Light (v3/data + cache)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import g3
import harness as H
from nyse_holidays import HOLIDAYS

CAL = g3.CAL
hol_in_cal = CAL[CAL.isin(HOLIDAYS)]
print("calendar sessions:", len(CAL), "| NYSE-holiday Globex sessions in the calendar:", len(hol_in_cal))
S = {s: H.sessions(s) for s in g3.MKTS}
rows = []
for d in hol_in_cal:
    r = {"session": d.strftime("%Y-%m-%d %a")}
    for s in ("ES", "NQ"):
        if d in S[s].index:
            x = S[s].loc[d]
            r[f"{s}_last_t"] = int(x.last_t); r[f"{s}_rthvol"] = int(x.rth_volume); r[f"{s}_vol"] = int(x.volume)
    rows.append(r)
hv = pd.DataFrame(rows)
print(hv.to_string())
# typical ES volume for comparison
print("ES median session volume, all sessions:", S["ES"].volume.median(), "| holiday sessions:", hv.ES_vol.median())
missing = HOLIDAYS[(HOLIDAYS >= CAL.min()) & (HOLIDAYS <= CAL.max()) & (HOLIDAYS.dayofweek < 5) & ~HOLIDAYS.isin(CAL)]
print("NYSE holidays (weekdays) with NO Globex session in the calendar:", len(missing), missing.strftime("%Y-%m-%d").tolist())

print("\n--- TOM_DAYS (S3.7) on holiday sessions:")
tom = g3.TOM_DAYS[g3.TOM_DAYS <= g3.LAST]
print([d.strftime("%Y-%m-%d %a") for d in tom[tom.isin(HOLIDAYS)]])
print("\n--- opex / quad sessions on holidays (any market):")
for s in g3.MKTS:
    o = S[s].index[S[s].opex.astype(bool)]
    print(s, "opex on holiday:", o[o.isin(HOLIDAYS)].strftime("%Y-%m-%d").tolist())
print("third Fridays that are NYSE holidays and the opex day used:")
for d in HOLIDAYS[(HOLIDAYS.dayofweek == 4) & (HOLIDAYS.day >= 15) & (HOLIDAYS.day <= 21) & (HOLIDAYS <= g3.LAST) & (HOLIDAYS >= CAL.min())]:
    used = {s: S[s].index[(S[s].opex.astype(bool)) & (S[s].index.year == d.year) & (S[s].index.month == d.month)].strftime("%Y-%m-%d %a").tolist() for s in g3.MKTS}
    print(" ", d.strftime("%Y-%m-%d %a"), "in calendar:", d in CAL, "| opex used:", used)
print("\n--- C3 (non-expiry Fridays) on holiday sessions:")
e = g3.entries("A3-C3", "ES")
print(pd.DatetimeIndex(e.session)[pd.DatetimeIndex(e.session).isin(HOLIDAYS)].strftime("%Y-%m-%d").tolist())

print("\n--- C1 cached draws landing on holiday sessions (share; per-trade C1 mean with vs without them):")
for f in sorted(os.listdir(g3.CACHE)):
    c = pd.read_parquet(os.path.join(g3.CACHE, f), columns=["session", "pnl_usd"])
    m = pd.DatetimeIndex(c.session).isin(HOLIDAYS)
    print(f"{f:32s} share {m.mean():.4f}  C1 $/tr all {c.pnl_usd.mean():7.3f}  excl. holidays {c.pnl_usd[~m].mean():7.3f}")
