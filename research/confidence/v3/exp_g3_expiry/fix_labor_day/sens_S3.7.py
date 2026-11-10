"""S3.7 Labor Day fix: sensitivity table. Light (trade tables + C1 cache, no 1-minute data).
v1 = old rule (5 Labor Day holiday sessions used), v2 = corrected rule (first NYSE trading day = the Tuesday),
v1-drop = v1 with the 5 Labor Day events removed (no replacement), v2-C1x = v2 with C1 recomputed from the same
999 draws excluding draws that land on NYSE-holiday Globex sessions."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import g3
import stats_protocol as sp
from nyse_holidays import HOLIDAYS

LD = pd.DatetimeIndex(["2012-09-03", "2014-09-01", "2018-09-03", "2019-09-02", "2024-09-02"])
v1 = pd.read_parquet(os.path.join(HERE, "v1_outputs", "S3.7.parquet"))
v2 = pd.read_parquet(os.path.join(g3.OUT, "trades", "S3.7.parquet"))


def summ(tr, label):
    D = pd.DataFrame(index=g3.CAL)
    D["net"] = g3.dser(tr, "pnl_usd"); D["d"] = g3.dser(tr, "d_c1")
    p_d = g3.cons_p(D["d"])[0]; p_net = g3.cons_p(D["net"])[0]
    s = pd.DatetimeIndex(tr.session)
    out = dict(variant=label, n=len(tr), usd_tr=tr.pnl_usd.mean(), d_tr=tr.d_c1.mean(), c1_tr=tr.c1.mean(),
               p_d=p_d, p_net=p_net, t_d=sp.hac_t(D["d"].to_numpy())[0], t_net=sp.hac_t(D["net"].to_numpy())[0],
               **{f"t_d_lag{L}": sp.hac_t(D["d"].to_numpy(), lags=L)[0] for L in (0, 5, 10, 20)},
               usd_1017=tr.pnl_usd[s.year <= 2017].mean(), usd_1825=tr.pnl_usd[s.year >= 2018].mean(),
               usd_22p=tr.pnl_usd[s.year >= 2022].mean())
    return out


rows = [summ(v1, "v1 (old: Labor Day holiday sessions)"), summ(v2, "v2 (corrected: first NYSE trading day)")]
rows.append(summ(v1[~pd.DatetimeIndex(v1.session).isin(LD)].reset_index(drop=True), "v1-drop (Labor Day events removed)"))
# C1 excluding holiday draws (same 999 draws, reweighted per trade)
v2x = []
for sym in g3.MKTS:
    c = pd.read_parquet(os.path.join(g3.CACHE, f"c1_S3.7_{sym}_999.parquet"), columns=["session", "tid", "pnl_usd"])
    c = c[~pd.DatetimeIndex(c.session).isin(HOLIDAYS)]
    t = v2[v2.market == sym].copy()
    t["c1"] = t["tid"].map(c.groupby("tid").pnl_usd.mean()).to_numpy()
    t["d_c1"] = t["pnl_usd"] - t["c1"]
    v2x.append(t)
rows.append(summ(pd.concat(v2x, ignore_index=True), "v2-C1x (C1 without holiday-session draws)"))
# the swapped trades themselves
sw = pd.concat([v1[pd.DatetimeIndex(v1.session).isin(LD)].assign(version="v1 Labor Day"),
                v2[pd.DatetimeIndex(v2.session).isin(LD + pd.Timedelta(days=1))].assign(version="v2 Tuesday")])
tab = pd.DataFrame(rows)
pd.set_option("display.width", 250)
print(tab.round(4).to_string())
print("\nswapped trades ($ per micro):")
print(sw[["version", "market", "session", "entry_px", "exit_px", "pnl_usd", "c1", "d_c1"]].to_string())
print("sum v1 Labor Day trades:", round(sw[sw.version == "v1 Labor Day"].pnl_usd.sum(), 2),
      "| sum v2 Tuesday trades:", round(sw[sw.version == "v2 Tuesday"].pnl_usd.sum(), 2))
tab.to_csv(os.path.join(HERE, "sens_S3.7.csv"), index=False)
sw.to_csv(os.path.join(HERE, "swapped_trades_S3.7.csv"), index=False)
