"""(1) Log the diagnostic variant S3.7-dropLD (v1 events minus the 5 Labor Day holiday sessions) in out/trials.csv.
(2) Lucid eval of corrected S3.7 (basket, fixed 1/3/5 micros, 40% and 50% rules) vs 100 C1 twins. Light-moderate."""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import g3
import harness as H

LD = pd.DatetimeIndex(["2012-09-03", "2014-09-01", "2018-09-03", "2019-09-02", "2024-09-02"])
v1 = pd.read_parquet(os.path.join(HERE, "v1_outputs", "S3.7.parquet"))
drop = v1[~pd.DatetimeIndex(v1.session).isin(LD)].reset_index(drop=True)
H.log("S3.7-dropLD", "MES+MNQ+MYM", "DIAGNOSTIC S3.7 v1 with the 5 Labor Day holiday-session events removed",
      trades=drop, baseline=float(drop.c1.mean()),
      params=dict(legs=[("1800", "0930", 1)], which="tom_v1_minus_laborday", markets=list(g3.MKTS), tier="diag"),
      note=f"{g3.NOTE}; skeptic Labor Day fix sensitivity; not a new hypothesis; t_d 1.98 p_d 0.0328")
print("logged S3.7-dropLD")

tr = pd.read_parquet(os.path.join(g3.OUT, "trades", "S3.7.parquet"))
sizing = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
cols = ["market", "t_entry", "t_exit", "risk_usd", "pnl_usd", "session"]
real = H.eval(tr[cols], sizing=sizing, calendar_=g3.CAL)
c1 = pd.concat([pd.read_parquet(os.path.join(g3.CACHE, f"c1_S3.7_{s}_999.parquet")) for s in g3.MKTS], ignore_index=True)
tw = []
for r in range(100):
    t = c1.loc[(c1.rep == r) & (pd.DatetimeIndex(c1.session) <= g3.LAST), cols]
    e = H.eval(t, sizing=sizing, calendar_=g3.CAL); e["rep"] = r; tw.append(e)
tw = pd.concat(tw, ignore_index=True)
key = ["policy", "consistency", "window"]
agg = tw.groupby(key)[["pass_pct", "within_10", "bust_pct"]].mean().add_prefix("twin_").reset_index()
m = real.merge(agg, on=key, how="left")
m["rank_p_pass"] = [float((1 + (tw[(tw.policy == r.policy) & (tw.consistency == r.consistency) & (tw.window == r.window)].pass_pct >= r.pass_pct).sum()) / 101) for r in m.itertuples()]
pd.set_option("display.width", 250)
print(m[["policy", "consistency", "window", "n_starts", "pass_pct", "twin_pass_pct", "within_10", "twin_within_10",
         "bust_pct", "twin_bust_pct", "days_pass_median", "rank_p_pass"]].round(3).to_string())
m.to_csv(os.path.join(HERE, "eval_S3.7_v2.csv"), index=False)
