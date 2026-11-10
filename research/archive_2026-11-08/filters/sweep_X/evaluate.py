"""Stage 2: evaluate every variant (SWEEP.md). M2 kept (see m2_overlap.csv: decisions differ materially from M1)."""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats as st

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{OUT}/decisions", exist_ok=True)
T = pd.read_pickle(f"{OUT}/base_trades.pkl")
P = pd.read_pickle(f"{OUT}/decisions.pkl")
dec, thr, elig, meas = P["dec"], P["thr"], P["elig"], P["meas"]
V = list(dec)                                                    # 42 variants (M1, M2, M4 x 12; M3 x 6)
PRIMARY = "M1_q67_L250"
C = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
other = C[C.model != "overnight_break"]
usd = T.usd.to_numpy()
yr = T.date.dt.year.to_numpy()
ERAS = {"2010-13": (2010, 2013), "2014-17": (2014, 2017), "2018-20": (2018, 2020), "2021-23": (2021, 2023),
        "2024-26": (2024, 2026)}
N = len(T)


def dd_worst(dates, u):
    d = pd.Series(u).groupby(pd.Series(dates)).sum().sort_index()
    eq = np.r_[0.0, d.cumsum().to_numpy()]
    return float((np.maximum.accumulate(eq) - eq).max()), float(d.min())


def book(skip, extra_cost=0.0):
    keep = ~skip
    m_dd, m_w = dd_worst(T.date[keep].to_numpy(), usd[keep] - extra_cost)
    bd = np.r_[T.date[keep].to_numpy(), other.date.to_numpy()]
    bu = np.r_[usd[keep], other.usd.to_numpy()] - extra_cost
    b_dd, b_w = dd_worst(bd, bu)
    return m_dd, m_w, b_dd, b_w, float(bu.sum())


# random keys shared by all variants: random removal of n eligible trades = the n eligible trades with smallest key
rng = np.random.default_rng(12345)
U = rng.random((1000, N))
base = dict(zip(["dd", "worst", "book_dd", "book_worst", "book_net"], book(np.zeros(N, bool))))
base2 = dict(zip(["dd", "worst", "book_dd", "book_worst", "book_net"], book(np.zeros(N, bool), 1.0)))
rows, rand_removed = [], {}
for v in V:
    s, e = dec[v], elig[v]
    n, ne = int(s.sum()), int(e.sum())
    kept, rem = usd[~s], usd[s]
    r = dict(variant=v, measure=v.split("_")[0], q=np.nan, L=np.nan, X=np.nan, eligible=ne, removed_n=n,
             removed_share=n / N, removed_share_of_eligible=n / ne if ne else np.nan,
             removed_usd=rem.sum(), kept_usd=kept.sum(), kept_per_trade=kept.mean(),
             removed_per_trade=rem.mean() if n else np.nan)
    if v.startswith("M3"):
        r["X"] = int(v.split("X")[1])
    else:
        r["q"], r["L"] = int(v.split("_q")[1].split("_")[0]), int(v.split("_L")[1])
    r["welch_t_kept_minus_removed"] = st.ttest_ind(kept, rem, equal_var=False).statistic if n > 1 else np.nan
    ke = usd[e & ~s]
    r["welch_t_eligible_kept_minus_removed"] = st.ttest_ind(ke, rem, equal_var=False).statistic if n > 1 else np.nan
    for name, (a, b) in ERAS.items():
        r[f"removed_usd_{name}"] = usd[s & (yr >= a) & (yr <= b)].sum()
        r[f"removed_n_{name}"] = int((s & (yr >= a) & (yr <= b)).sum())
    r["removed_usd_2010_2017"] = usd[s & (yr <= 2017)].sum()
    r["removed_usd_2018_2026"] = usd[s & (yr >= 2018)].sum()
    m_dd, m_w, b_dd, b_w, b_net = book(s)
    r.update(model_max_dd=m_dd, model_worst_day=m_w, book_net=b_net, book_max_dd=b_dd, book_worst_day=b_w)
    # 2 ticks per fill: $1 less per trade (all trades, all three models)
    r["removed_usd_2tick"] = (rem - 1).sum()
    r["kept_usd_2tick"] = (kept - 1).sum()
    r["welch_t_2tick"] = r["welch_t_kept_minus_removed"]                          # a constant shift: t unchanged
    m_dd, m_w, b_dd, b_w, b_net = book(s, 1.0)
    r.update(model_max_dd_2tick=m_dd, model_worst_day_2tick=m_w, book_net_2tick=b_net, book_max_dd_2tick=b_dd,
             book_worst_day_2tick=b_w)
    # random-skip control
    if n:
        cols = np.flatnonzero(e)
        sub = U[:, cols]
        idx = np.argpartition(sub, n - 1, axis=1)[:, :n]
        rr = usd[cols][idx].sum(axis=1)
    else:
        rr = np.zeros(1000)
    rand_removed[v] = rr
    r["random_removed_mean"] = rr.mean()
    r["random_pctile"] = 100 * np.mean(rr <= r["removed_usd"])
    r["pass_both_halves"] = bool(r["removed_usd_2010_2017"] < 0 and r["removed_usd_2018_2026"] < 0)
    r["pass_random_5pct"] = bool(r["random_pctile"] <= 5)
    rows.append(r)
    out = T[["date", "entry_time", "exit_time", "side", "entry", "exit", "exit_reason", "gross_pts", "net_pts",
             "usd", "bp", "R_pts", "raw_signal_close", "atr5_signal", "atr_med60"]].copy()
    out = out.rename(columns={"usd": "net_usd", "bp": "net_bp"})
    out["measure"] = T[meas[v]].to_numpy()
    out["threshold"] = thr[v]
    out["eligible"] = e
    out["skip"] = s
    out.to_csv(f"{OUT}/decisions/{v}.csv", index=False)

R = pd.DataFrame(rows)
# M3: share of trades skipped by year
m3y = pd.DataFrame({v: pd.Series(dec[v]).groupby(yr).mean() for v in V if v.startswith("M3")})
m3y.index.name = "year"
m3y.to_csv(f"{OUT}/m3_skip_share_by_year.csv")

# family-wise: best (most negative) removed $ across all variants under random replacement
RR = np.column_stack([rand_removed[v] for v in V])
best_rand = RR.min(axis=1)
best_v = R.loc[R.removed_usd.idxmin(), "variant"]
best_val = R.removed_usd.min()
fw = dict(best_variant=best_v, best_removed_usd=float(best_val), family_size=len(V),
          fw_pctile=float(100 * np.mean(best_rand <= best_val)),
          random_best_p5=float(np.percentile(best_rand, 5)), random_best_median=float(np.median(best_rand)))
R["fw_pass_5pct"] = fw["fw_pctile"] <= 5

# walk-forward: from 2013, each year the variant with the best cumulative (kept $ - all $) = -removed $ in all
# earlier years; ties for best, or best <= 0 (no variant beats no filter), -> no filter
years = np.arange(yr.min(), yr.max() + 1)
REM = pd.DataFrame({v: pd.Series(np.where(dec[v], usd, 0.0)).groupby(yr).sum().reindex(years, fill_value=0) for v in V})
REMn = pd.DataFrame({v: pd.Series(dec[v].astype(int)).groupby(yr).sum().reindex(years, fill_value=0) for v in V})
allY = pd.Series(usd).groupby(yr).sum().reindex(years)
wf_rows, wf_skip = [], np.zeros(N, bool)
for y in years[years >= 2013]:
    cum = -REM.loc[REM.index < y].sum()
    best = cum.max()
    pick = None if (best <= 0 or (cum == best).sum() > 1) else cum.idxmax()
    rem_y = REM.loc[y, pick] if pick else 0.0
    n_y = int(REMn.loc[y, pick]) if pick else 0
    if pick:
        wf_skip |= dec[pick] & (yr == y)
    wf_rows.append(dict(year=int(y), chosen=pick or "no filter", prior_cum_gain=float(best), no_filter_usd=float(allY[y]),
                        wf_usd=float(allY[y] - rem_y), diff=float(-rem_y), removed_n=n_y,
                        wf_usd_2tick=float(allY[y] - rem_y - (yr == y).sum() + n_y),
                        no_filter_usd_2tick=float(allY[y] - (yr == y).sum())))
WF = pd.DataFrame(wf_rows)
WF.to_csv(f"{OUT}/walk_forward.csv", index=False)
w13 = yr >= 2013
m_nf = dd_worst(T.date[w13].to_numpy(), usd[w13])
m_wf = dd_worst(T.date[w13 & ~wf_skip].to_numpy(), usd[w13 & ~wf_skip])
o13 = other[other.date.dt.year >= 2013]
b_nf = dd_worst(np.r_[T.date[w13].to_numpy(), o13.date.to_numpy()], np.r_[usd[w13], o13.usd])
b_wf = dd_worst(np.r_[T.date[w13 & ~wf_skip].to_numpy(), o13.date.to_numpy()], np.r_[usd[w13 & ~wf_skip], o13.usd])
wf = dict(total_no_filter=float(WF.no_filter_usd.sum()), total_wf=float(WF.wf_usd.sum()), diff=float(WF["diff"].sum()),
          total_no_filter_2tick=float(WF.no_filter_usd_2tick.sum()), total_wf_2tick=float(WF.wf_usd_2tick.sum()),
          years_better=int((WF["diff"] > 0).sum()), years_worse=int((WF["diff"] < 0).sum()),
          years_no_filter=int((WF.chosen == "no filter").sum()), trades_removed=int(wf_skip.sum()),
          model_dd_nf=m_nf[0], model_dd_wf=m_wf[0], model_worst_nf=m_nf[1], model_worst_wf=m_wf[1],
          book_dd_nf=b_nf[0], book_dd_wf=b_wf[0], book_worst_nf=b_nf[1], book_worst_wf=b_wf[1])
wf["beats_no_filter"] = wf["diff"] > 0

R["adopt"] = R.pass_both_halves & R.pass_random_5pct & R.fw_pass_5pct & wf["beats_no_filter"]
R = R.round(4)
R.to_csv(f"{OUT}/variants.csv", index=False)
summary = dict(base=dict(n=N, usd=float(usd.sum()), **base), base_2tick=dict(usd=float(usd.sum() - N), **base2),
               primary=R[R.variant == PRIMARY].iloc[0].to_dict(), familywise=fw, walk_forward=wf,
               n_adopt=int(R.adopt.sum()))
json.dump(summary, open(f"{OUT}/summary.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
pd.set_option("display.width", 300, "display.max_columns", 40, "display.max_rows", 100)
print(json.dumps(dict(base=summary["base"], base2=summary["base_2tick"], fw=fw, wf=wf), indent=1, default=str))
print(R[["variant", "eligible", "removed_n", "removed_share", "removed_usd", "removed_usd_2010_2017",
         "removed_usd_2018_2026", "kept_usd", "kept_per_trade", "removed_per_trade", "welch_t_kept_minus_removed",
         "model_max_dd", "model_worst_day", "book_max_dd", "random_pctile", "adopt"]].sort_values("removed_usd").to_string())
print(WF.to_string())
print(m3y.round(3).to_string())
