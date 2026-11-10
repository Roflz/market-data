"""Supplement: R-unit check, per-year breakdown, outlier dependence, system effect (MNQ as traded and MES analog).
Reads the trade files written by replicate.py (scratchpad) plus project files (read-only)."""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, ".")
import calendar_days as cd
import exits_compare as ec
import exits_engine as ee

OUT = Path("/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/skiprules/replication")


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


ctx = pd.read_pickle("data/market_context.pkl")
ctx.index = pd.to_datetime(ctx.index).normalize()
spx = ctx.spx_ret_1d_prev
fomc = cd.fomc_days()

# ---- R units: MNQ from chosen csv (R col), MES opening_range from lit csv (net_R), MES overnight_break recomputed
C = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
P = pd.read_csv("lit_p5_orb_trades.csv", parse_dates=["date"])
ds_es = pd.read_pickle("data/daily_sessions_ES.pkl"); ds_es.index = pd.to_datetime(ds_es.index).normalize()
cash_es = ds_es.index[ds_es.cash_day]; exp_es = cd.expiry_fridays(cash_es)
ec.init()
D = ec.G["ES"]; sp = ee.SPEC["ES"]
t = ee.run(D, ec.G[("sets", "ES")]["Overnight break + daily trend"], "hold", k0=2.0)
date = pd.to_datetime(D.sess[t.bar.to_numpy()]).normalize()
net_pts = t.pts.to_numpy() - sp["comm"] / sp["usd"]
es_ob = pd.DataFrame({"model": "overnight_break", "date": date, "usd": t.pts.to_numpy() * sp["usd"] - sp["comm"],
                      "R": net_pts / t.R_pts.to_numpy()})
es_ob = es_ob[es_ob.date.isin(cash_es) & ~es_ob.date.isin(exp_es)]
es_or = P[(P.variant == "A5T") & (P.kind == "strategy") & (P.market == "ES")]
es_or = pd.DataFrame({"model": "opening_range", "date": es_or.date, "usd": es_or.net_usd, "R": es_or.net_R})
es_or = es_or[~es_or.date.isin(exp_es)]
MES = pd.concat([es_ob, es_or], ignore_index=True)
MNQ = C[C.model != "expiry_fade"][["model", "date", "usd", "R"]].copy()

for nm, T in (("MNQ", MNQ), ("MES", MES)):
    T["r1"] = (spx.reindex(T.date).to_numpy() <= -2)
    T["r2"] = T.date.isin(fomc).to_numpy()
    T["year"] = T.date.dt.year

print("=== R-unit (net R per trade) and robustness of the condition-day means ===")
for nm, T in (("MNQ", MNQ), ("MES", MES)):
    for model, rule in (("overnight_break", "r1"), ("opening_range", "r1"), ("opening_range", "r2"), ("overnight_break", "r2")):
        g = T[T.model == model]
        c, o = g[g[rule]], g[~g[rule]]
        # outlier dependence: drop the 3 worst condition-day trades
        cs = c.usd.sort_values()
        print(f"{nm} {model:15s} {rule}: n={len(c):3d}  R/trade {c.R.mean():6.3f} vs {o.R.mean():6.3f} (t {welch(c.R, o.R):5.2f}) | "
              f"median $ {c.usd.median():7.2f} vs {o.usd.median():7.2f} | ex-3-worst $ {cs.iloc[3:].mean():7.2f} "
              f"(t {welch(cs.iloc[3:], o.usd):5.2f})")

print("\n=== per-year condition-day trades (n, $/trade) ===")
for nm, T in (("MNQ", MNQ), ("MES", MES)):
    for model, rule in (("overnight_break", "r1"), ("opening_range", "r1"), ("opening_range", "r2")):
        g = T[(T.model == model) & T[rule]]
        y = g.groupby("year").usd.agg(["size", "mean", "sum"])
        print(f"{nm} {model} {rule}: " + "  ".join(f"{yy}:{int(r['size'])}/{r['mean']:.0f}" for yy, r in y.iterrows()))
        # excluding 2022 (bear market year)
        g2 = T[(T.model == model)]
        m = g2.year != 2022
        print(f"     ex-2022: n={int((g2[rule] & m).sum())} ${g2.usd[g2[rule] & m].mean():.2f}/tr  t {welch(g2.usd[g2[rule] & m], g2.usd[~g2[rule] & m]):.2f}")


# ---- system effect
def system(T, label):
    d = T.groupby("date").usd.sum().sort_index()
    eq = d.cumsum()
    dd = (eq.cummax().clip(lower=0) - eq).max()
    return dict(label=label, trades=len(T), total=T.usd.sum(), maxdd=dd, worst_day=d.min())


def fmt(s, base=None):
    x = f"{s['label']:44s} trades {s['trades']:5d}  total ${s['total']:9,.0f}  maxDD ${s['maxdd']:7,.0f}  worst day ${s['worst_day']:7,.0f}"
    if base:
        x += f"  | removed {base['trades'] - s['trades']:4d} trades, d$ {s['total'] - base['total']:+8,.0f}, dDD {s['maxdd'] - base['maxdd']:+7,.0f}"
    return x


print("\n=== system effect ===")
FULL = C.copy()
FULL["r1"] = spx.reindex(FULL.date).to_numpy() <= -2
FULL["r2"] = FULL.date.isin(fomc).to_numpy()
bk = FULL.model.isin(["overnight_break", "opening_range"])
base = system(FULL, "MNQ 3-model system (as traded)")
print(fmt(base))
s1 = system(FULL[~(bk & FULL.r1)], "  + R1 (skip both breakouts after SPX<=-2%)"); print(fmt(s1, base))
s2 = system(FULL[~((FULL.model == "opening_range") & FULL.r2)], "  + R2 (skip opening_range on FOMC)"); print(fmt(s2, base))
s12 = system(FULL[~((bk & FULL.r1) | ((FULL.model == "opening_range") & FULL.r2))], "  + R1 + R2"); print(fmt(s12, base))
for pname, y0, y1 in (("2010-2015", 2010, 2015), ("2016-2020", 2016, 2020), ("2021-2026", 2021, 2026)):
    F = FULL[(FULL.date.dt.year >= y0) & (FULL.date.dt.year <= y1)]
    bkp = F.model.isin(["overnight_break", "opening_range"])
    b = system(F, f"   MNQ {pname} base")
    s = system(F[~((bkp & F.r1) | ((F.model == "opening_range") & F.r2))], f"   MNQ {pname} R1+R2")
    print(fmt(b)); print(fmt(s, b))

MES["r1"] = MES["r1"].astype(bool)
mb = system(MES, "MES analog (overnight_break + opening_range)")
print(fmt(mb))
m1 = system(MES[~MES.r1], "  + R1"); print(fmt(m1, mb))
m2 = system(MES[~((MES.model == "opening_range") & MES.r2)], "  + R2"); print(fmt(m2, mb))
m12 = system(MES[~(MES.r1 | ((MES.model == "opening_range") & MES.r2))], "  + R1 + R2"); print(fmt(m12, mb))
