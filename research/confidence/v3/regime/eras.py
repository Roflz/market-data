"""eras.py - era summary (median of quarterly values) + noise baseline for the similarity score. Reads out/*.csv."""
import os, pandas as pd, numpy as np
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
Q = pd.read_csv(os.path.join(OUT, "by_quarter.csv"))
Q = Q[Q.n_rth_bars > 300]
def era(p):
    if p < "2018Q1": return "A 2010-17"
    if p < "2024Q3": return "B 2018-24Q2"
    return "C last12m (24Q3-25Q2)"
Q["era"] = Q.period.map(era)
cols = ["rng_cost", "vol_ann", "ac15", "ac60", "vr4", "ema_persist", "pb_cont", "ushape", "on_rth_vol", "on_ret", "day_ret", "corr_es_nq"]
E = Q.groupby(["sym", "era"])[cols].median().round(3)
# quarter-to-quarter spread (IQR) inside era B, to judge whether era differences exceed normal noise
IQR = Q[Q.era == "B 2018-24Q2"].groupby("sym")[cols].quantile(.75) - Q[Q.era == "B 2018-24Q2"].groupby("sym")[cols].quantile(.25)
E.to_csv(os.path.join(OUT, "eras.csv"))
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(E.to_string()); print("\nIQR of quarterly values inside 2018-24Q2:\n", IQR.round(3).to_string())
S = pd.read_csv(os.path.join(OUT, "similarity_quarters.csv"))
rec = ["2024Q3", "2024Q4", "2025Q1", "2025Q2"]
rows = []
for s, d in S.groupby("sym"):
    rows.append(dict(sym=s, recent_qtrs_to_own_avg=d[d.quarter.isin(rec)].dist_no_cost.mean(),
                     past_2018plus_median=d[(d.quarter >= "2018") & ~d.quarter.isin(rec)].dist_no_cost.median(),
                     past_pre2018_median=d[d.quarter < "2018"].dist_no_cost.median(),
                     share_past_qtrs_closer_than_avg_recent_qtr=(d[~d.quarter.isin(rec)].dist_no_cost < d[d.quarter.isin(rec)].dist_no_cost.mean()).mean()))
B = pd.DataFrame(rows).round(2); B.to_csv(os.path.join(OUT, "similarity_noise_baseline.csv"), index=False); print("\n", B.to_string())
