"""G1 Tier B summary (preliminary, G1 columns only; the binding F3 StepM over G1+G2 columns is the synthesis step):
StepM (studentized, mean block 10, B 5000) on the daily d series of the G1 secondary/neighbour columns at 0.004,
Newey-West t of d, DSR(d) with N_eff 45, raw-net p, gates; neighbours: same sign as A1."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g1lib as G                        # noqa: E402
from g1lib import sp                     # noqa: E402

OUT = os.path.join(G.V3, "out")
COLS = ["S1.1", "S1.2", "S1.3", "S1.4", "S1.5", "S1.6", "N1.lb10", "N1.lb20", "N1.hour", "N1.cost"]
SEC = ["S1.1", "S1.2", "S1.3", "S1.4", "S1.5", "S1.6"]
D = pd.concat({c: pd.read_csv(os.path.join(OUT, "daily", f"{c}.csv"), index_col="session")["d"] for c in COLS},
              axis=1)
N = pd.concat({c: pd.read_csv(os.path.join(OUT, "daily", f"{c}.csv"), index_col="session")["net_U1"] for c in COLS},
              axis=1)
A1 = json.load(open(os.path.join(OUT, "results", "A1.json")))
rows = []
fam = [c for c in COLS if c != "N1.cost"]          # N1.cost has the same d as A1 (cost shifts net and C1 equally)
sm = sp.stepm(D[fam].to_numpy(), mean_block=10, B=5000, seed=G.SEED_BOOT, alpha=0.004)
sm_sec = sp.stepm(D[SEC].to_numpy(), mean_block=10, B=5000, seed=G.SEED_BOOT, alpha=0.004)
p_stepm = dict(zip(fam, sm["p_adj"]))
p_stepm_sec = dict(zip(SEC, sm_sec["p_adj"]))
for c in COLS:
    r = json.load(open(os.path.join(OUT, "results", f"{c}.json")))
    x = D[c].to_numpy()
    if c == "S1.2":
        x = x[pd.DatetimeIndex(D.index) >= pd.Timestamp("2018-01-01")]
    ds = sp.dsr(x, 45)
    tierB = (p_stepm.get(c, np.nan) <= 0.004 and r["t_nw_d"] >= 3 and ds["dsr"] >= 0.95 and r["p_net"] <= 0.05
             and not r["failed_gates"] and not r["kill"])
    rows.append(dict(col=c, kind=r["kind"], n_trades=r["n_trades"], usd_per_trade=r["usd_per_trade"],
                     d_per_trade=r["d_per_trade"], p_d=r["p_d"], p_net=r["p_net"], t_nw_d=r["t_nw_d"],
                     t_nw_net=r["t_nw_net"], stepm_p_G1=p_stepm.get(c, np.nan),
                     stepm_p_secondaries=p_stepm_sec.get(c, np.nan), dsr45=ds["dsr"], mc_rank_p=r["mc_rank_p"],
                     failed_gates=";".join(r["failed_gates"]), kill=r["kill"],
                     same_sign_as_A1=bool(np.sign(r["d_per_trade"]) == np.sign(A1["d_per_trade"])
                                          and np.sign(r["usd_per_trade"]) == np.sign(A1["usd_per_trade"])),
                     tierB_pass_prelim=bool(tierB)))
T = pd.DataFrame(rows)
T.to_csv(os.path.join(HERE, "tierB_G1.csv"), index=False)
pd.set_option("display.width", 250)
print(T.round(4).to_string())
