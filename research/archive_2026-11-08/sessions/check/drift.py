"""Signed-drift leads: which slots have |t|>3, era/market consistency, and $ value per MNQ/MES trade."""
import sys, os
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from grid import grid, pevent, biggap_cum, ROOT
D = os.path.dirname(__file__)


def hm(x):
    return f"{x // 60:02d}:{x % 60:02d}"


sl = {s: pd.read_parquet(f"{D}/slots_{s}.parquet") for s in ("NQ", "ES")}
tab = {}
for s, df in sl.items():
    for era, sub in (("all", df), ("e1", df[df.yr <= 2017]), ("e2", df[df.yr >= 2018])):
        g = sub.groupby("et_min").mv
        tab[(s, era)] = g.mean() / (g.std() / np.sqrt(g.count()))
T = pd.DataFrame(tab)
T.columns = [f"{a}_{b}" for a, b in T.columns]
T.index = [hm(i) for i in T.index]
print("slots with |t|>3 on NQ or ES (all years):")
print(T[(T.NQ_all.abs() > 3) | (T.ES_all.abs() > 3)].round(2).to_string())
# consistency: same sign in 4 cells (NQ e1,e2, ES e1,e2) and |t|>1.5 in each
c = T[["NQ_e1", "NQ_e2", "ES_e1", "ES_e2"]]
cons = c[((c > 1.5).all(axis=1)) | ((c < -1.5).all(axis=1))]
print("\nslots with |t|>1.5 and same sign in all four market-era cells:")
print(T.loc[cons.index].round(2).to_string())
# null expectation of such 4-cell agreement given NQ-ES correlation is not computed analytically; report count
print("count:", len(cons), "of", len(T))
# NQ/ES correlation at slot level
m = sl["NQ"].merge(sl["ES"], on=["sess", "et_min"], suffixes=("_nq", "_es"))
print("NQ-ES slot-move correlation:", round(np.corrcoef(m.mv_nq, m.mv_es)[0, 1], 3))
