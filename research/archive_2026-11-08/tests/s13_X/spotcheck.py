"""Independent spot check: re-read raw 1-min CSV rows by text (no arrays) and recompute chosen trades."""
import sys, subprocess, pandas as pd, numpy as np
X = sys.argv[1]; D = "data/"
def raw(sym, date):
    out = subprocess.run(["grep", f"^{date} 0[89]:", D + f"{sym}_fut_1m.csv"], capture_output=True, text=True).stdout
    rows = [l.split(",") for l in out.strip().splitlines()]
    df = pd.DataFrame(rows, columns=["ts", "O", "H", "L", "C", "V", "inst"])
    df["hm"] = df.ts.str[11:16]
    for c in "OHLC": df[c] = df[c].astype(float)
    return df.set_index("hm")
picks = []
q = pd.read_csv(X + "L1-NFP_judged_MNQ_2018_2026.csv", parse_dates=["date"])
picks += [("NQ", q.loc[q.net_usd.idxmax()]), ("NQ", q.loc[q.net_usd.idxmin()]), ("NQ", q.iloc[0]), ("NQ", q.iloc[57])]
e = pd.read_csv(X + "L1-NFP_judged_MES_2018_2026.csv", parse_dates=["date"]); picks += [("ES", e.iloc[30])]
s = pd.read_csv(X + "L1_disaster_stop_MNQ_NFP.csv", parse_dates=["date"]); s = s[s.exit_reason == "disaster_stop"]
picks += [("NQ", s.iloc[-1]), ("NQ", s.iloc[3])]
c = pd.read_csv(X + "L1_primary_time_MNQ_CPI.csv", parse_dates=["date"]); picks += [("NQ", c.iloc[-1])]
ppt = {"NQ": 2.0, "ES": 5.0}; cost = {"NQ": 2.0, "ES": 3.5}
for sym, t in picks:
    r = raw(sym, t.date.strftime("%Y-%m-%d"))
    w = r.loc["08:30":"09:45"]
    o830, c844, o845, o945 = r.at["08:30", "O"], r.at["08:44", "C"], r.at["08:45", "O"], r.at["09:45", "O"]
    mv = c844 - o830; d = -np.sign(mv)
    ex = o945; why = "time_9:45"; xt = "09:45"
    if t.exit_reason == "disaster_stop":
        stp = o845 - d * 2 * abs(mv); stp = np.floor(stp / .25) * .25 if d > 0 else np.ceil(stp / .25) * .25
        for hm, b in r.loc["08:45":"09:44"].iterrows():
            if (d > 0 and b.L <= stp) or (d < 0 and b.H >= stp):
                ex = b.O if ((d > 0 and b.O < stp) or (d < 0 and b.O > stp)) else stp; why = "disaster_stop"; xt = hm; break
    net = (d * (ex - o845)) * ppt[sym] - cost[sym]
    print(f"{sym} {t.date:%Y-%m-%d} raw: o830={o830} c844={c844} move={mv:+} side={'long' if d>0 else 'short'} entry 08:45 {o845} exit {xt} {ex} {why} net${net:+.2f} "
          f"insts={sorted(set(w.inst))} nbars={len(w)}/76 tz={r.at['08:30','ts'][-6:]} | file: {t.side} {t.entry}->{t.exit} {t.exit_time} {t.exit_reason} net${t.net_usd:+.2f} "
          f"{'MATCH' if abs(net - t.net_usd) < 1e-6 and ex == t.exit and o845 == t.entry and xt == t.exit_time else 'MISMATCH'}")
