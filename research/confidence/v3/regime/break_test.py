"""Is the 2018 split a real break or a cherry-picked one? Unknown-date break test (Andrews 1993 sup-type)
on P1 daily P&L in risk units (P&L / trailing-250-day sd, no look-ahead). p-value by 20-day block permutation."""
import json, numpy as np, pandas as pd
d = pd.read_csv("v3/out/daily/P0.csv", parse_dates=["session"])
d["P1"] = d.net_A1 + d.net_A3 + d.net_A4
sd = d.P1.rolling(250, min_periods=120).std().shift(1)
r = (d.P1/sd).dropna(); dates = d.session[r.index].values; x = r.values; n = len(x)
def supstat(x, trim=0.15):
    c = np.cumsum(x); k = np.arange(int(n*trim), int(n*(1-trim)))
    m1 = c[k-1]/k; m2 = (c[-1]-c[k-1])/(n-k); s = x.std(ddof=1)
    t = (m2-m1)/(s*np.sqrt(1/k+1/(n-k)))
    i = np.argmax(np.abs(t)); return np.abs(t[i]), k[i]
T, kb = supstat(x)
rng = np.random.default_rng(7); B = 20; nb = n//B; blocks = x[:nb*B].reshape(nb, B)
null = []
for _ in range(2000):
    xp = blocks[rng.permutation(nb)].ravel(); null.append(supstat(xp)[0])
null = np.array(null); p = (1+np.sum(null>=T))/(1+len(null))
t18 = None
k18 = np.searchsorted(dates, np.datetime64("2018-01-01")); c = np.cumsum(x)
m1, m2 = c[k18-1]/k18, (c[-1]-c[k18-1])/(n-k18); t18 = (m2-m1)/(x.std(ddof=1)*np.sqrt(1/k18+1/(n-k18)))
res = dict(best_break=str(pd.Timestamp(dates[kb]).date()), sup_t=float(T), perm_p=float(p),
           t_at_2018=float(t18), naive_p_at_2018=float(2*(1-__import__("scipy.stats").stats.norm.cdf(abs(t18)))),
           mean_risk_units_before=float(x[:kb].mean()), mean_risk_units_after=float(x[kb:].mean()))
print(res); json.dump(res, open("v3/regime/break_test.json","w"), indent=1)
