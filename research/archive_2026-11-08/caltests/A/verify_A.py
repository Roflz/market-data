# Independent spot checks straight from the raw files (string timestamps = ET wall time)
import pandas as pd, numpy as np
O = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/caltests/A"
es = pd.read_csv("data/ES_fut_1m.csv", usecols=["ts_event", "Open", "Close", "instrument_id"]).set_index("ts_event")
nq = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "Close", "instrument_id"]).set_index("ts_event")
zn = pd.read_csv("data/ZN_fut_1h.csv", usecols=["ts_event", "Open", "Close", "instrument_id"]).set_index("ts_event")
def bar(df, day, hhmm):
    k = [x for x in df.index[df.index.str.startswith(f"{day} {hhmm}")]]
    assert len(k) == 1, (day, hhmm, k)
    return df.loc[k[0]]
# --- Test 1, Nov 2013 (T = 2013-11-29 early close); T_prev = 2013-10-31
ev = pd.read_csv(f"{O}/events_1_primary.csv")
days = ["2013-11-22", "2013-11-25", "2013-11-26", "2013-11-27", "2013-11-29"]
c0E = bar(es, "2013-10-31", "15:59").Close; c0Z = bar(zn, "2013-10-31", "15:00").Close
cal = []
for d in days:
    early = d == "2013-11-29"
    pE = bar(es, d, "12:54" if early else "15:54"); pZ = bar(zn, d, "11:00" if early else "14:00")
    assert pE.instrument_id == bar(es, "2013-10-31", "15:59").instrument_id
    assert pZ.instrument_id == bar(zn, "2013-10-31", "15:00").instrument_id
    cal.append(int(np.sign(pE.Close / c0E - pZ.Close / c0Z)))
closes = [bar(es, d, "12:59" if d == "2013-11-29" else "15:59").Close for d in days + ["2013-12-02"]]
pos = [-c for c in cal]
g = sum(p * (closes[j + 1] - closes[j]) for j, p in enumerate(pos))
seq = [0] + pos + [0]; sides = sum(abs(seq[j+1]-seq[j]) for j in range(len(seq)-1))
row = ev[ev.month == "2013-11"].iloc[0]
print("T1 Nov2013 cal", cal, "gross pts", g, "net$", g*5 - sides*1.75, "| script:", row.gross_pts, row.net_usd, row.sides)
# --- Test 2: 2025-06-20 (entry 2025-06-18) and 2014-04-17 (entry 04-16)
ev2 = pd.read_csv(f"{O}/events_2_primary.csv")
for E, P in (("2025-06-20", "2025-06-18"), ("2014-04-17", "2014-04-16"), ("2019-03-15", "2019-03-14")):
    c = bar(es, P, "15:59"); o = bar(es, E, "09:30")
    r = ev2[ev2.date == E].iloc[0]
    print("T2", E, o.Open - c.Close, c.instrument_id == o.instrument_id, "| script:", r.gross_pts, r.entry, r.flag)
# --- Test 3: Aug 2017 L=Aug25 exit Aug30; Sep 2017 L=Sep26 exit Sep28; May 2024 L=May29 exit May30
ev3 = pd.read_csv(f"{O}/events_3_primary.csv")
for m, L, X in (("2017-08", "2017-08-25", "2017-08-30"), ("2017-09", "2017-09-26", "2017-09-28"), ("2024-05", "2024-05-29", "2024-05-30")):
    a = bar(es, L, "15:59"); b = bar(es, X, "15:59")
    r = ev3[ev3.month == m].iloc[0]
    print("T3", m, b.Close - a.Close, "| script:", r.gross_pts, r.entry, r.exit, r.h)
# --- Test 4: Dec 2013 (T=Dec31 2013, T+1=Jan 2 2014), Jun 2017 (T+1 = 2017-07-03 early close)
ev4 = pd.read_csv(f"{O}/events_4_primary.csv")
for m, T, T1 in (("2013-12", "2013-12-31", "2014-01-02"), ("2017-06", "2017-06-30", "2017-07-03")):
    a = bar(es, T, "15:59"); b = bar(es, T1, "12:59" if T1 == "2017-07-03" else "15:59")
    r = ev4[ev4.month == m].iloc[0]
    print("T4", m, b.Close - a.Close, "| script:", r.gross_pts)
