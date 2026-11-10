"""Per-session features for S1 and S3 (all known at the decision time): hedge beta, residuals, z, filters.
Saves features.pkl (DataFrame indexed by session) and sessions.pkl (the Sessions object)."""
import os, sys, pickle
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y12lib import *
sys.path.insert(0, PROJ)
from calendar_days import fomc_days, cpi_days, expiry_fridays

S = Sessions()
b = hedge_betas(S)
n = S.n
fomc, cpi = fomc_days(), cpi_days()
dates = S.dates


def resid(t, i):
    """e at P(close of bar i) for session t, using that day's b; NaN if any required bar is missing"""
    pN, pE, oN, oE = S.CN[t, i], S.CE[t, i], S.ON[t, 0], S.OE[t, 0]
    return np.log(pN / oN) - b[t] * np.log(pE / oE)


e14 = np.array([resid(t, 299) for t in range(n)])
e15 = np.array([resid(t, 359) for t in range(n)])
full_idx = np.flatnonzero(S.full)


def trailing_sd(vals, t, pool, need_b=True):
    prior = pool[pool < t][-60:]
    if len(prior) < 60 or (need_b and np.isnan(b[prior]).any()):
        return np.nan, 0
    v = vals[prior]; v = v[np.isfinite(v)]
    return (v.std(ddof=1), len(v)) if len(v) >= 2 else (np.nan, len(v))


s14 = np.full(n, np.nan); s15 = np.full(n, np.nan); s_cnt = np.zeros(n, int)
for t in range(n):
    s14[t], s_cnt[t] = trailing_sd(e14, t, full_idx)
    s15[t], _ = trailing_sd(e15, t, full_idx)

# eligibility (S1 conditions 1-5)
gap = np.array([S.max_gap(t) if S.full[t] else 999 for t in range(n)])
bars_ok = np.array([all(np.isfinite(getattr(S, "C" + l)[t, i]) for l in "NE" for i in (299, 389))
                    and np.isfinite(S.ON[t, 0]) and np.isfinite(S.OE[t, 0]) for t in range(n)])
bars15_ok = np.array([np.isfinite(S.CN[t, 359]) and np.isfinite(S.CE[t, 359]) for t in range(n)])
is_fomc = np.array([d in fomc for d in dates]); is_cpi = np.array([d in cpi for d in dates])
# prior cash session must be a cash session with a close bar (prior close); roll flag already vs prior cash session
pc_ok = np.isfinite(S.pcN) & np.isfinite(S.pcE)
c1 = S.full
c2 = ~S.roll
c3 = bars_ok & (gap <= 10)
c4 = ~is_fomc & ~is_cpi
c5 = np.isfinite(b)
elig = c1 & c2 & c3 & c4 & c5 & pc_ok

# overnight residual and its sd over prior 60 eligible sessions (each with its own b)
on = np.array([np.log(S.ON[t, 0] / S.pcN[t]) - b[t] * np.log(S.OE[t, 0] / S.pcE[t]) if elig[t] else np.nan
               for t in range(n)])
elig_idx = np.flatnonzero(elig)
zo_sd = np.full(n, np.nan)
for t in range(n):
    prior = elig_idx[elig_idx < t][-60:]
    if len(prior) == 60:
        zo_sd[t] = on[prior].std(ddof=1)
zo = on / zo_sd

# VIX regime (Yahoo close on last trading day before today vs median of 252 closes ending that day)
vx = pd.read_csv(f"{PROJ}/data/yahoo_daily/VIX_index.csv", parse_dates=["Date"]).set_index("Date").Close.dropna()
vmed = vx.rolling(252).median()
vix_prev = np.full(n, np.nan); vix_med = np.full(n, np.nan); vix_date = []
for t, d in enumerate(dates):
    j = vx.index.searchsorted(d) - 1          # last VIX date strictly before today
    vix_prev[t] = vx.iloc[j]; vix_med[t] = vmed.iloc[j]; vix_date.append(vx.index[j])

esret14 = np.log(S.CE[:, 299] / S.pcE); esret15 = np.log(S.CE[:, 359] / S.pcE)
F = pd.DataFrame({
    "b": b, "e14": e14, "e15": e15, "s14": s14, "s15": s15, "s_cnt": s_cnt,
    "z14": e14 / s14, "z15": e15 / s15, "on": on, "zo_sd": zo_sd, "zo": zo,
    "es_ret14": esret14, "es_ret15": esret15,
    "nq_ret15": np.log(S.CN[:, 359] / S.pcN),
    "vix_prev": vix_prev, "vix_med252": vix_med, "vix_date": vix_date,
    "full": S.full, "roll": S.roll, "gap": gap, "bars_ok": bars_ok, "bars15_ok": bars15_ok,
    "fomc": is_fomc, "cpi": is_cpi, "pc_ok": pc_ok, "elig": elig,
    "c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5,
}, index=dates)
F["F2_14"] = np.abs(F.es_ret14) < 0.0075
F["F2_15"] = np.abs(F.es_ret15) < 0.0075
F["F3"] = F.vix_prev < F.vix_med252
F["F4"] = np.abs(F.zo) < 2
exp = expiry_fridays(dates)
F["expiry"] = [d in exp for d in dates]
F.to_pickle(f"{HERE}/features.pkl")
with open(f"{HERE}/sessions.pkl", "wb") as f:
    pickle.dump(S, f)
print("sessions", n, "full", S.full.sum(), "eligible", elig.sum())
print("first b", dates[np.flatnonzero(np.isfinite(b))[0]], "first s14", dates[np.flatnonzero(np.isfinite(s14))[0]],
      "first zo", dates[np.flatnonzero(np.isfinite(zo_sd))[0]])
print("b by year:", F.b.groupby(F.index.year).mean().round(2).to_dict())
print("gap>10 days among full non-roll with bars:", F.index[(F.full & ~F.roll & F.bars_ok & (F.gap > 10))].strftime("%Y-%m-%d").tolist())
print("gap>11 days:", F.index[(F.full & ~F.roll & F.bars_ok & (F.gap > 11))].strftime("%Y-%m-%d").tolist())
print("roll days (first session after either leg rolled):", int(F.roll.sum()), "of which full:", int((F.roll & F.full).sum()))
print("full sessions missing a required bar:", F.index[F.full & ~F.bars_ok].strftime("%Y-%m-%d").tolist())
