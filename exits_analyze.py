"""
Analyze exits_compare_raw.csv.
  1. What do exits / stop sizes do on RANDOM entries (averaged over 3 seeds)?
  2. Best stop size per exit
  3. Do the classic setups beat random entries with the SAME exit + stop?
  4. Honest walk-forward: each year uses the exit + stop that did best in all EARLIER years (from 2013), incl. 2026
Usage:  PYTHONPATH=./pylib python3 exits_analyze.py
"""
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)
r = pd.read_csv("exits_compare_raw.csv")
r["rand"] = r.entry.str.startswith("RANDOM")
r["entry_g"] = np.where(r.rand, "RANDOM (avg 3 seeds)", r.entry)
per = r.groupby(["sym", "entry_g", "exit", "stop_atr", "year"]).agg(net=("net", "mean"), trades=("trades", "mean"),
                                                                      hold=("avg_hold_min", "mean"), win=("win", "mean")).reset_index()
tot = per.groupby(["sym", "entry_g", "exit", "stop_atr"]).agg(
    net=("net", "sum"), trades=("trades", "sum"), years_up=("net", lambda x: int((x > 0).sum())),
    years=("net", "size"), hold_min=("hold", "mean"), win=("win", "mean"),
    y2026=("net", lambda x: float(x.iloc[-1]) if len(x) else np.nan)).reset_index()
tot["per_trade"] = tot.net / tot.trades

print("=== 1. RANDOM entries: net $ 2011-2026 by exit (rows) x initial stop in 5-min ATRs (cols), 1 micro, after costs ===")
for sym in ("MES", "MNQ"):
    t = tot[(tot.sym == sym) & (tot.entry_g == "RANDOM (avg 3 seeds)")]
    print(f"\n{sym}  (per-trade $ in brackets for the 3-ATR stop)")
    pv = t.pivot(index="exit", columns="stop_atr", values="net").round(0)
    pv["$/trade @3"] = t[t.stop_atr == 3].set_index("exit").per_trade.round(2)
    pv["hold min @3"] = t[t.stop_atr == 3].set_index("exit").hold_min.round(0)
    print(pv.sort_values(3, ascending=False).to_string())

print("\n=== 2/3. Classic setups: best 5 exit+stop combos over 2011-2026 (IN-SAMPLE, for orientation only) and the "
      "same combo on random entries ===")
rand = tot[tot.entry_g == "RANDOM (avg 3 seeds)"].set_index(["sym", "exit", "stop_atr"])
for (sym, ent), t in tot[tot.entry_g != "RANDOM (avg 3 seeds)"].groupby(["sym", "entry_g"]):
    top = t.sort_values("net", ascending=False).head(5).copy()
    top["random_same_exit_$/tr"] = [rand.loc[(sym, x, k)].per_trade for x, k in zip(top.exit, top.stop_atr)]
    print(f"\n{sym} | {ent}")
    print(top[["exit", "stop_atr", "net", "trades", "per_trade", "random_same_exit_$/tr", "years_up", "years",
               "hold_min", "y2026"]].round(2).to_string(index=False))

print("\n=== 4. HONEST WALK-FORWARD: each year trades the exit+stop with the best total over all EARLIER years ===")
rows = []
for (sym, ent), t in per.groupby(["sym", "entry_g"]):
    for y in range(2013, 2027):
        past = t[t.year < y].groupby(["exit", "stop_atr"]).net.sum()
        if past.empty:
            continue
        x, k = past.idxmax()
        cur = t[(t.year == y) & (t.exit == x) & (t.stop_atr == k)]
        rows.append({"sym": sym, "entry": ent, "year": y, "chosen": f"{x} / stop {k}",
                     "net": float(cur.net.sum()), "trades": float(cur.trades.sum())})
wf = pd.DataFrame(rows)
wf.to_csv("exits_walkforward.csv", index=False)
summ = wf.groupby(["sym", "entry"]).agg(net_2013_2026=("net", "sum"), trades=("trades", "sum"),
                                         years_up=("net", lambda x: int((x > 0).sum())), years=("net", "size")).reset_index()
summ["2026"] = [wf[(wf.sym == s) & (wf.entry == e) & (wf.year == 2026)].net.sum() for s, e in zip(summ.sym, summ.entry)]
summ["chosen for 2026"] = [wf[(wf.sym == s) & (wf.entry == e) & (wf.year == 2026)].chosen.iloc[0] for s, e in zip(summ.sym, summ.entry)]
print(summ.round(0).to_string(index=False))
print("\nSaved exits_walkforward.csv")
