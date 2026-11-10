import numpy as np, pandas as pd, sys, os
sys.path.insert(0, os.getcwd())
from calendar_days import expiry_fridays
S = {}
for s in ("ES","NQ"):
    d = pd.read_pickle(f"data/daily_sessions_{s}.pkl").sort_index()
    S[s] = d[d.cash_day].copy()
days = S["ES"].index; N=len(days)
END = pd.Timestamp("2026-10-30")
EXP = set(pd.Timestamp(x) for x in expiry_fridays(days))
print("cash days", N, days[0].date(), days[-1].date(), "days<=END", (days<=END).sum())
# --- 7/8: the Oct30->Nov2 overnight
for s in ("ES","NQ"):
    x = S[s]
    on = (x.open_adj.values[1:] - x.close_adj.values[:-1]) / x.close_raw.values[:-1]*1e4
    arr = days[1:]; prv = days[:-1]
    i = list(arr).index(pd.Timestamp("2026-11-02"))
    print(s, "overnight Oct30->Nov2 bp", round(on[i],3))
    # 8 benchmark: A (arrival<=END) vs B (prev<=END), excluding arrival in EXP
    nexp = np.array([d not in EXP for d in arr])
    a = on[(arr<=END) & nexp]; b = on[(prv<=END) & nexp]
    print(s, "bench8 A n,mean", len(a), round(a.mean(),4), " B n,mean", len(b), round(b.mean(),4))
# --- 10 ES close-to-10am comparison decomposition
h = pd.read_csv("data/ES_fut_1h.csv")
h.index = pd.to_datetime(h.ts_event, utc=True).dt.tz_convert("America/New_York")
h = h[~h.index.duplicated()].sort_index()
h["date"] = h.index.tz_localize(None).normalize(); h["hr"]=h.index.hour; h["mi"]=h.index.minute
top = h[h.mi==0]
c09 = top[top.hr==9].groupby("date").tail(1).set_index("date")[["Close","instrument_id"]].reindex(days)
c15 = top[top.hr==15].groupby("date").tail(1).set_index("date")[["Close","instrument_id"]].reindex(days)
x = S["ES"]
R = set()
for y in range(2017, 2027):
    f = pd.Timestamp(y,6,1); f = f + pd.Timedelta(days=(4-f.weekday())%7 + 21)
    R.add(days[days<=f][-1])
rows=[]
for i in range(N-1):
    d = days[i]
    if d < pd.Timestamp("2017-01-01") or d > END or d.weekday()!=4 or d in R: continue
    p9, i9 = c09.Close.iloc[i+1], c09.instrument_id.iloc[i+1]
    if np.isnan(p9) or i9 != x.inst.iloc[i+1]: continue
    p9a = p9 + (x.open_adj.iloc[i+1]-x.open_raw.iloc[i+1])
    bpA = (p9a - x.close_adj.iloc[i]) / x.close_raw.iloc[i]*1e4
    early = bool(x.early_close.iloc[i])
    has15 = not np.isnan(c15.Close.iloc[i])
    same = has15 and c15.instrument_id.iloc[i] == i9
    roll = x.inst.iloc[i] != x.inst.iloc[i+1]
    rows.append(dict(d=d, bp=bpA, early=early, has15=has15, same=same, roll=roll))
r = pd.DataFrame(rows)
print("A-style comparison n", len(r), "mean", round(r.bp.mean(),3))
print("early-close Fridays", int(r.early.sum()), list(r[r.early].d.dt.date.astype(str)))
print("roll-crossing Fridays (session inst differs)", int(r.roll.sum()))
print("B-style (has15 & same inst) n", int(r.same.sum()), "mean", round(r[r.same].bp.mean(),3))
print("early & roll overlap", int((r.early & r.roll).sum()), " excluded by B not early/roll:", int((~r.same & ~r.early & ~r.roll).sum()))
ne = r[~r.early]
print("exclude early-close only (keep roll weekends adj): n", len(ne), "mean", round(ne.bp.mean(),3))
# event values
ev=[]
for d in sorted(R):
    i = days.get_loc(d)
    p9a = c09.Close.iloc[i+1] + (x.open_adj.iloc[i+1]-x.open_raw.iloc[i+1])
    ev.append((p9a - x.close_adj.iloc[i]) / x.close_raw.iloc[i]*1e4)
ev=np.array(ev)
def welch(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return (a.mean()-b.mean())/np.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))
print("event n", len(ev), "mean", round(ev.mean(),4))
for nm, c in (("A all", r.bp), ("B same-inst", r[r.same].bp), ("no early-close, rolls kept", ne.bp), ("no early, no roll", r[~r.early & ~r.roll].bp)):
    print(f"  {nm}: n={len(c)} cmp={c.mean():.3f} excess={ev.mean()-c.mean():.3f} welch t={welch(ev,c):.3f}")
