"""Check the v2 TOM_DAYS list against the theoretical first NYSE business day of each month (weekday, not an NYSE
holiday) and list the differences from v1. Light."""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import g3
tom = g3.TOM_DAYS[g3.TOM_DAYS <= g3.LAST]
v1 = g3.TOM_DAYS_V1[g3.TOM_DAYS_V1 <= g3.LAST]
print("v1", len(v1), "v2", len(tom))
print("in v1 not v2:", v1.difference(tom).strftime("%Y-%m-%d %a").tolist())
print("in v2 not v1:", tom.difference(v1).strftime("%Y-%m-%d %a").tolist())
bd = pd.bdate_range("2010-07-01", g3.LAST)
bd = bd[~bd.isin(g3.NYSE_HOLIDAYS)]
theo = pd.DatetimeIndex(pd.Series(bd, index=bd).groupby([bd.year, bd.month]).min().to_numpy())
theo = theo[theo <= g3.LAST]
print("theoretical first NYSE days:", len(theo), "| equal to v2:", theo.equals(tom))
print("theoretical not in v2:", theo.difference(tom).strftime("%Y-%m-%d").tolist(), "| v2 not theoretical:", tom.difference(theo).strftime("%Y-%m-%d").tolist())
