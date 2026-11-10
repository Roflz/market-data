"""Holdout / forward-test power for P1 (A1+A3+A4), pre-holdout daily P&L only.
MinTRL (Bailey & Lopez de Prado 2012), power of a 340-session holdout, SPRT expected days,
O'Brien-Fleming style sample sizes, and how a recency-weighted vs full-sample estimate differ."""
import json, numpy as np, pandas as pd
from scipy import stats
d = pd.read_csv("v3/out/daily/P0.csv", parse_dates=["session"])
assert d.session.max() < pd.Timestamp("2025-06-30")
d["P1"] = d.net_A1 + d.net_A3 + d.net_A4
out = {}
def sr_stats(x):
    x = np.asarray(x); sr = x.mean()/x.std(ddof=1)
    return dict(n=len(x), mean=x.mean(), sd=x.std(ddof=1), sr=sr, skew=stats.skew(x), kurt=stats.kurtosis(x, fisher=False))
def mintrl(sr, g3, g4, sr0=0.0, alpha=0.05):
    z = stats.norm.ppf(1-alpha)
    return 1 + (1 - g3*sr + (g4-1)/4*sr**2) * (z/(sr-sr0))**2
def n_for_power(sr, g3, g4, alpha=0.05, power=0.8):
    v = 1 - g3*sr + (g4-1)/4*sr**2
    return v*((stats.norm.ppf(1-alpha)+stats.norm.ppf(power))/sr)**2
rows = []
for lab, m in [("all 2010-25H1", d.session>="2010"), ("2018-25H1", d.session>="2018"), ("2022-25H1", d.session>="2022"), ("2010-17", d.session<"2018")]:
    s = sr_stats(d.loc[m,"P1"]); s["label"]=lab
    if s["sr"]>0:
        s["MinTRL_days_95"] = mintrl(s["sr"], s["skew"], s["kurt"])
        s["days_80pct_power"] = n_for_power(s["sr"], s["skew"], s["kurt"])
        v = 1 - s["skew"]*s["sr"] + (s["kurt"]-1)/4*s["sr"]**2
        ez = s["sr"]*np.sqrt(340/v)
        s["holdout340_expected_z"] = ez
        s["holdout340_expected_z_noskewcredit"] = s["sr"]*np.sqrt(340)
        s["days_80pct_power_noskewcredit"] = ((stats.norm.ppf(0.95)+stats.norm.ppf(0.8))/s["sr"])**2
        s["holdout340_power_1sided_5pct"] = 1-stats.norm.cdf(stats.norm.ppf(0.95)-ez)
        # SPRT (Wald) H0 SR=0 vs H1 SR=s, alpha .05 beta .2, normal approx
        a, b, dl = 0.05, 0.2, s["sr"]
        A, B = np.log((1-b)/a), np.log(b/(1-a))
        s["SPRT_E_days_if_edge_real"] = ((1-b)*A + b*B)/(dl**2/2)
        s["SPRT_E_days_if_no_edge"] = (a*A + (1-a)*B)/(-dl**2/2)
    rows.append(s)
t = pd.DataFrame(rows).set_index("label")
pd.set_option("display.width", 200)
print(t.round(3).T)
# recency-weighted estimate of daily mean (exponential half-lives) vs equal weight
x = d.set_index("session")["P1"]
age_y = np.asarray((x.index.max()-x.index).days)/365.25
hl = {}
for h in [1,2,3,5,8,None]:
    w = np.ones(len(x)) if h is None else 0.5**(age_y/h)
    m = np.sum(w*x)/np.sum(w); neff = w.sum()**2/np.sum(w**2)
    hl["equal" if h is None else f"halflife_{h}y"] = dict(mean_per_day=float(m), effective_days=float(neff))
print(pd.DataFrame(hl).T.round(2))
# year-to-year stability of the edge since 2018 (is the recent window homogeneous?)
yr = x.groupby(x.index.year).agg(["mean","std","count"])
yr["t"] = yr["mean"]/yr["std"]*np.sqrt(yr["count"])
print(yr.round(2))
post = x[x.index>="2018"]; g = post.groupby(post.index.year)
F = stats.f_oneway(*[v.values for _,v in g])
kw = stats.kruskal(*[v.values for _,v in g])
print("2018-25H1 equal-mean across years: ANOVA p=%.3f  Kruskal p=%.3f" % (F.pvalue, kw.pvalue))
allg = x.groupby(x.index.year)
print("2010-25H1 equal-mean across years: ANOVA p=%.3f" % stats.f_oneway(*[v.values for _,v in allg]).pvalue)
out = dict(table=t.reset_index().to_dict("records"), recency=hl, years=yr.reset_index().to_dict("records"),
           anova_2018plus_p=float(F.pvalue), kruskal_2018plus_p=float(kw.pvalue))
json.dump(out, open("v3/regime/holdout_power.json","w"), indent=1, default=float)
