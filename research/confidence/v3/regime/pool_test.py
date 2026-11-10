# Pool-vs-separate diagnostics across ES/NQ/YM on 15-min pullback events (pre-holdout only).
import numpy as np, pandas as pd
HOLD = pd.Timestamp("2025-06-30 18:00")
fr = []
for s in ["ES","NQ","YM"]:
    d = pd.read_csv(f"../signals/out/pullbacks_{s}_15.csv", parse_dates=["t_event"])
    d = d[d.t_event < HOLD]
    d["sym"] = s
    fr.append(d)
d = pd.concat(fr)
d = d[d.outcome.isin(["continuation","failure"])]
d["win"] = (d.outcome=="continuation").astype(float)
d["R"] = (d.end_pts / d.pb_pts.replace(0,np.nan)).clip(-5,5)   # outcome in pullback-depth units (unit-free)
d["day"] = d.t_event.dt.floor("D")
d = d[d.t_event >= "2018-01-01"]
print("outcomes:", d.outcome.value_counts().to_dict())
def meta(est, se):
    w = 1/se**2; mu = (w*est).sum()/w.sum(); Q = (w*(est-mu)**2).sum(); k=len(est)
    I2 = max(0,(Q-(k-1))/Q) if Q>0 else 0
    C = w.sum()-(w**2).sum()/w.sum(); tau2 = max(0,(Q-(k-1))/C)
    from scipy.stats import chi2
    return mu, np.sqrt(1/w.sum()), Q, chi2.sf(Q,k-1), I2, tau2
rows=[]
for var in ["win","R"]:
    for scope,sub in [("2018-25H1 all",d)]+[(f"{y}",d[d.year==y]) for y in sorted(d.year.unique())]:
        g = sub.groupby("sym")[var]
        est = g.mean(); n = g.size()
        # cluster-robust SE by day (events on same day are not independent)
        se = sub.groupby("sym").apply(lambda x: x.groupby("day")[var].mean().std(ddof=1)/np.sqrt(x.day.nunique()))
        mu,semu,Q,p,I2,tau2 = meta(est.values, se.values)
        rows.append(dict(var=var,scope=scope,**{f"{k}_mean":round(v,4) for k,v in est.items()},
                         **{f"{k}_n":int(v) for k,v in n.items()},pooled=round(mu,4),Q=round(Q,2),p=round(p,3),I2=round(I2,2),tau=round(np.sqrt(tau2),4)))
r = pd.DataFrame(rows); pd.set_option("display.width",250); print(r.to_string(index=False))
# cross-ticker correlation of daily average outcome (same days) -> effective number of independent tickers
for var in ["win","R"]:
    dm = d.groupby(["day","sym"])[var].mean().unstack().dropna()
    c = dm.corr(); rho = c.values[np.triu_indices(3,1)].mean(); m=3
    print(f"\n{var}: daily-mean corr across tickers (days with all 3, n={len(dm)}):\n{c.round(3)}\n avg rho={rho:.3f}; effective tickers = 3/(1+2*rho) = {3/(1+2*rho):.2f}")
# same-direction co-occurrence: share of ES events with an NQ/YM event same direction within same 15-min bar
key = d.groupby(["t_event","direction"]).sym.nunique()
print("\nevents sharing identical bar+direction across tickers:", (key>1).mean().round(3), " (share of bar-direction keys with >=2 tickers)")
r.to_csv("v3/regime/pool_test_out.csv", index=False)
