"""(1) post-hoc numbers of builder from my trade files; (2) ES early-close close = 12:59 bar (PREREG text) instead of 13:14."""
import sys, os, subprocess, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import check as C
W = C.W
t = pd.read_csv(f"{W}/my_trades_A_MNQ.csv", parse_dates=["date"])
eq = t.net_usd.cumsum()
print("A_MNQ top10", t.net_usd.nlargest(10).sum(), "worst", t.net_usd.min(), "maxDD", (eq - eq.cummax()).min(),
      "size3 trades", t[t.maxsize == 3].net_usd.sum(), "2026", t[t.date.dt.year == 2026].net_usd.sum())
print(t.groupby("maxsize").net_usd.agg(["count", "sum"]))
sig = pd.read_csv(f"{W}/my_signal.csv", index_col=0, parse_dates=True)
print("ZN bar not on same calendar day:", list(sig.index[~sig.zn_same_day]))
print("ZN bar earlier than 15:00 on normal days:", list(sig.index[(sig.zn_bar_tmin != 900) & ~sig.early_close]))
# ES 12:59 bar close on early-close days
ds = pd.read_pickle("data/daily_sessions_ES.pkl"); ds = ds[ds.cash_day]
ec = ds.index[ds.early_close]
out = subprocess.run(["grep", " 12:59:00", "data/ES_fut_1m.csv"], capture_output=True, text=True).stdout
e = pd.read_csv(io.StringIO(out), header=None, names=["ts", "O", "H", "L", "C", "V", "inst"])
e["date"] = pd.to_datetime(e.ts.str[:10])
e = e.drop_duplicates("date").set_index("date").reindex(ec)
print("12:59 bars found on early-close days:", e.C.notna().sum(), "/", len(ec), "| same contract as session:", (e.inst == ds.inst.reindex(ec)).sum())
ds2 = ds.copy()
adj = ds2.close_adj - ds2.close_raw
ds2.loc[ec, "close_raw"] = e.C.values
ds2.loc[ec, "close_adj"] = e.C.values + adj.loc[ec].values
orig = pd.read_pickle
C.pd.read_pickle = lambda p, *a, **k: ds2 if p.endswith("daily_sessions_ES.pkl") else orig(p, *a, **k)
sig2 = C.build_signal("ES")
C.pd.read_pickle = orig
print("signal max abs change", (sig2.s - sig.s).abs().max())
seg = pd.read_pickle(f"{W}/seg_NQ.pkl")
pos1, _, dec = C.positions(sig.drop(columns=[c for c in sig.columns if c not in ("s", "early_close")]), seg)
pos2, _, _ = C.positions(sig2, seg)
first = int(np.argmax(dec)); sg = seg.iloc[first:].reset_index(drop=True)
for r, tb in (("P", 2.0), ("A", 2.4), ("B", 2.4)):
    print(r, "positions changed on", int((pos1[r] != pos2[r]).sum()), "segments", end=" | ")
    T, q, gu, sn, d = C.run(sg, pos2[r][first:], 2.0, 1.0)
    res = C.evaluate(T, q, d, (sg.status == "ok").to_numpy(), 2.0, 1.0, tb)
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res.items() if k in
           ("n", "total_usd", "t", "since2018", "since2023", "blocks_pos", "randdir_pct", "placebo_pct", "PASS", "beats_drift")})
T, q, gu, sn, d = C.run(sg, pos2["A"][first:], 2.0, 1.0)
res = C.evaluate(T, q, d, (sg.status == "ok").to_numpy(), 2.0, 1.0, 2.4)
print("A blocks (12:59 version):", res["blocks"])
T0 = pd.read_csv(f"{W}/my_trades_A_MNQ.csv"); 
ch = np.where(pos1["A"] != pos2["A"])[0]
print("A changed segments:", [(str(seg.date.iat[i].date()), int(pos1['A'][i]), int(pos2['A'][i])) for i in ch])
