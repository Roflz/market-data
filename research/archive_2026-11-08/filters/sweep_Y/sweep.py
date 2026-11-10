"""
Sweep Y, step 2: the W sweep of SWEEP.md (which wide-stop overnight-break trades to skip).
Reads base_trades.pkl (built and checked by build_base.py) and chosen_models_trades.csv (for the 3-model book).
Writes: sweep_variants.csv (one row per variant), decisions/<variant>.csv (per-trade decisions),
        m3_skip_by_year.csv, walk_forward.csv, m1_vs_m2.csv, summary.json.
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.getcwd())
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/sweep_Y"
os.makedirs(f"{OUT}/decisions", exist_ok=True)

QS = [50, 67, 80, 90]
LS = [125, 250, 500]
XS = [75, 100, 150, 200, 250, 300]
ERAS = [("2010-13", 2010, 2013), ("2014-17", 2014, 2017), ("2018-20", 2018, 2020), ("2021-23", 2021, 2023),
        ("2024-26", 2024, 2026)]
N_DRAWS, SEED = 1000, 12345
M2_MATERIAL = 0.05     # M2 kept only if its skip decisions differ from M1's on >= 5% of eligible trades (avg over q, L)

T = pd.read_pickle(f"{OUT}/base_trades.pkl")
N = len(T)
usd = T.usd.to_numpy(float)
year = T.date.dt.year.to_numpy()
ALL = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
OTHER = ALL[ALL.model != "overnight_break"]
assert len(ALL[ALL.model == "overnight_break"]) == N

# ---- trading-day calendar: cash days from the model's first data year (2011) on ----
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
cal = ds.index[ds.cash_day & (ds.index >= "2011-01-01")]
day_no = pd.Series(np.arange(len(cal)), index=cal)
T["day_no"] = T.date.map(day_no).astype(int)
assert T.day_no.notna().all()
dn = T.day_no.to_numpy()


# ---------------------------------------------------------------- decisions
def lookback_decisions(values, q, L, mode="pct"):
    """For every trade: skip if its value is above the q-th percentile of the values of the live trades dated in the
    previous L trading days (strictly before its date). No skipping until L trading days of history exist.
    mode 'points_rel_median' = M2: value / median(window) against the q-th pct of window / median(window)."""
    rows = []
    for k in range(N):
        p = dn[k]
        if p < L:
            rows.append(dict(eligible=False, n_window=0, threshold=np.nan, measure=values[k], skip=False))
            continue
        in_win = (dn >= p - L) & (dn <= p - 1)                   # strictly before the trade's date
        win = values[in_win]
        assert (T.date.to_numpy()[in_win] < T.date.to_numpy()[k]).all()
        if len(win) == 0:
            rows.append(dict(eligible=True, n_window=0, threshold=np.nan, measure=values[k], skip=False))
            continue
        if mode == "points_rel_median":
            med = np.median(win)
            meas = values[k] / med
            thr = np.percentile(win / med, q)
        else:
            meas = values[k]
            thr = np.percentile(win, q)
        rows.append(dict(eligible=True, n_window=int(in_win.sum()), threshold=thr, measure=meas, skip=bool(meas > thr)))
    return pd.DataFrame(rows)


def fixed_decisions(values, X):
    return pd.DataFrame(dict(eligible=True, n_window=0, threshold=float(X), measure=values, skip=values > X))


variants = []      # (name, measure, q, L, X, decisions)
for q in QS:
    for L in LS:
        variants.append((f"M1_q{q}_L{L}", "M1", q, L, None, lookback_decisions(T.M1.to_numpy(), q, L)))

# M2: kept only if it differs materially from M1 (judged on skip decisions only, never on P&L)
m2 = {}
cmp_rows = []
for q in QS:
    for L in LS:
        d2 = lookback_decisions(T.stop_pts.to_numpy(), q, L, mode="points_rel_median")
        d1 = [v for v in variants if v[0] == f"M1_q{q}_L{L}"][0][5]
        el = d1.eligible.to_numpy()
        diff = (d1.skip.to_numpy() != d2.skip.to_numpy())[el].mean()
        cmp_rows.append(dict(q=q, L=L, eligible=int(el.sum()), m1_skips=int(d1.skip.sum()), m2_skips=int(d2.skip.sum()),
                             disagree=int((d1.skip != d2.skip).sum()), disagree_share=diff))
        m2[(q, L)] = d2
cmp = pd.DataFrame(cmp_rows)
cmp.to_csv(f"{OUT}/m1_vs_m2.csv", index=False)
keep_m2 = cmp.disagree_share.mean() >= M2_MATERIAL
print(f"M1 vs M2 skip decisions differ on {cmp.disagree_share.mean():.1%} of eligible trades on average "
      f"(range {cmp.disagree_share.min():.1%}-{cmp.disagree_share.max():.1%}); M2 {'KEPT' if keep_m2 else 'DROPPED'}")
if keep_m2:
    for q in QS:
        for L in LS:
            variants.append((f"M2_q{q}_L{L}", "M2", q, L, None, m2[(q, L)]))
for X in XS:
    variants.append((f"M3_X{X}", "M3", None, None, X, fixed_decisions(T.M3.to_numpy(), X)))
for q in QS:
    for L in LS:
        variants.append((f"M4_q{q}_L{L}", "M4", q, L, None, lookback_decisions(T.M4.to_numpy(), q, L)))
PRIMARY = "M1_q67_L250"


# ---------------------------------------------------------------- metrics
def dd_and_worst(daily):
    c = daily.sort_index().cumsum()
    return float((c.cummax() - c).max()), float(daily.min())


def model_daily(keep_mask, extra_cost=0.0):
    k = T[keep_mask]
    return (k.usd - extra_cost).groupby(k.date).sum()


def book_daily(keep_mask, extra_cost=0.0):
    k = T[keep_mask]
    parts = pd.concat([pd.Series((k.usd - extra_cost).to_numpy(), index=k.date),
                       pd.Series((OTHER.usd - extra_cost).to_numpy(), index=OTHER.date)])
    return parts.groupby(level=0).sum()


all_keep = np.ones(N, bool)
base = {}
for cost, tag in ((0.0, ""), (1.0, "_2tick")):
    base["model_mdd" + tag], base["model_worst_day" + tag] = dd_and_worst(model_daily(all_keep, cost))
    base["book_mdd" + tag], base["book_worst_day" + tag] = dd_and_worst(book_daily(all_keep, cost))
base["model_usd"] = float(usd.sum())
base["model_usd_2tick"] = float(usd.sum() - N)
base["book_usd"] = float(ALL.usd.sum())
base["book_usd_2tick"] = float(ALL.usd.sum() - len(ALL))
print("base:", json.dumps({k: round(v, 2) for k, v in base.items()}))

rng = np.random.default_rng(SEED)
results, rand_store, m3_years = [], {}, []
for name, meas, q, L, X, dec in variants:
    skip = dec.skip.to_numpy()
    elig = dec.eligible.to_numpy()
    keep = ~skip
    n_rm = int(skip.sum())
    rm, kp = usd[skip], usd[keep]
    r = dict(variant=name, measure=meas, q=q, L=L, X=X, primary=(name == PRIMARY),
             n_eligible=int(elig.sum()), n_removed=n_rm, share_removed=n_rm / N,
             share_removed_of_eligible=n_rm / max(1, elig.sum()),
             removed_usd=float(rm.sum()), kept_usd=float(kp.sum()))
    for era, a, z in ERAS:
        m = skip & (year >= a) & (year <= z)
        r[f"removed_usd_{era}"] = float(usd[m].sum())
        r[f"n_removed_{era}"] = int(m.sum())
    r["removed_usd_2010-2017"] = float(usd[skip & (year <= 2017)].sum())
    r["removed_usd_2018-2026"] = float(usd[skip & (year >= 2018)].sum())
    r["removed_usd_2023-2026"] = float(usd[skip & (year >= 2023)].sum())
    r["usd_per_trade_kept"] = float(kp.mean())
    r["usd_per_trade_removed"] = float(rm.mean()) if n_rm else np.nan
    r["welch_t_kept_minus_removed"] = float(stats.ttest_ind(kp, rm, equal_var=False).statistic) if n_rm >= 2 else np.nan
    for cost, tag in ((0.0, ""), (1.0, "_2tick")):
        r["model_mdd" + tag], r["model_worst_day" + tag] = dd_and_worst(model_daily(keep, cost))
        r["book_mdd" + tag], r["book_worst_day" + tag] = dd_and_worst(book_daily(keep, cost))
    r["removed_usd_2tick"] = r["removed_usd"] - n_rm
    r["kept_usd_2tick"] = r["kept_usd"] - (N - n_rm)
    r["removed_usd_2010-2017_2tick"] = r["removed_usd_2010-2017"] - int((skip & (year <= 2017)).sum())
    r["removed_usd_2018-2026_2tick"] = r["removed_usd_2018-2026"] - int((skip & (year >= 2018)).sum())
    r["book_usd"] = base["book_usd"] - r["removed_usd"]
    r["book_usd_2tick"] = base["book_usd_2tick"] - r["removed_usd_2tick"]
    # random-skip control: same count, same eligible trades
    pool = np.flatnonzero(elig)
    draws = np.empty(N_DRAWS)
    for j in range(N_DRAWS):
        pick = rng.choice(pool, size=n_rm, replace=False)
        draws[j] = usd[pick].sum()
    rand_store[name] = draws
    r["random_median_removed_usd"] = float(np.median(draws))
    r["random_pct"] = float((draws <= r["removed_usd"]).mean() * 100) if n_rm else np.nan
    # pass checks (per variant; the family-wise and walk-forward checks are global, below)
    r["pass_removed_lt0_2010_2017"] = r["removed_usd_2010-2017"] < 0
    r["pass_removed_lt0_2018_2026"] = r["removed_usd_2018-2026"] < 0
    r["pass_random_pct_le5"] = bool(n_rm and r["random_pct"] <= 5)
    results.append(r)
    if meas == "M3":
        for y in sorted(set(year)):
            m = year == y
            m3_years.append(dict(variant=name, year=int(y), trades=int(m.sum()), removed=int(skip[m].sum()),
                                 share_removed=float(skip[m].mean()), removed_usd=float(usd[skip & m].sum())))
    # per-trade decision file
    f = T[["date", "sig_time", "entry_time", "exit_time", "side", "entry", "exit", "exit_reason", "gross_pts",
           "net_pts", "usd", "bp", "R", "atr5", "stop_pts", "raw_px", "M1", "M3", "M4"]].copy()
    f = f.rename(columns={"sig_time": "signal_time", "usd": "net_usd", "bp": "net_bp"})
    f["variant"] = name
    f["measure_used"] = dec.measure.to_numpy()
    f["threshold"] = dec.threshold.to_numpy()
    f["n_window_trades"] = dec.n_window.to_numpy()
    f["eligible"] = elig
    f["skip"] = skip
    f.to_csv(f"{OUT}/decisions/{name}.csv", index=False)

R = pd.DataFrame(results)

# ---------------------------------------------------------------- family-wise control
names = R.variant.tolist()
mat = np.vstack([rand_store[n] for n in names])            # variants x draws
fam_min = mat.min(axis=0)
best_i = int(R.removed_usd.idxmin())
best_name, best_val = R.variant[best_i], float(R.removed_usd[best_i])
fam_pct = float((fam_min <= best_val).mean() * 100)
familywise = dict(n_variants=len(names), best_variant=best_name, best_removed_usd=best_val,
                  random_best_median=float(np.median(fam_min)), random_best_p5=float(np.percentile(fam_min, 5)),
                  percentile_of_actual_best=fam_pct, pass_le5=fam_pct <= 5)
print("family-wise:", familywise)

# ---------------------------------------------------------------- walk-forward
years = sorted(set(year))
rm_by_year = {n: {y: 0.0 for y in years} for n in names}
dec_by_name = {v[0]: v[5].skip.to_numpy() for v in variants}
for n in names:
    s = dec_by_name[n]
    for k in range(N):
        if s[k]:
            rm_by_year[n][year[k]] += usd[k]
all_by_year = {y: float(usd[year == y].sum()) for y in years}


def walk_forward(allow_no_filter_when_negative):
    rows = []
    for y in years:
        if y < 2013:
            continue
        cum = {n: -sum(rm_by_year[n][yy] for yy in years if yy < y) for n in names}    # kept$ - all$ so far
        top = max(cum.values())
        leaders = [n for n in names if cum[n] == top]
        if len(leaders) > 1 or (allow_no_filter_when_negative and top <= 0):
            pick = "none"
        else:
            pick = leaders[0]
        rem = 0.0 if pick == "none" else rm_by_year[pick][y]
        rows.append(dict(year=y, variant_used=pick, cum_edge_before=top, no_filter_usd=all_by_year[y],
                         wf_usd=all_by_year[y] - rem, wf_minus_no_filter=-rem))
    return pd.DataFrame(rows)


WF = walk_forward(True)
WF2 = walk_forward(False)
WF.to_csv(f"{OUT}/walk_forward.csv", index=False)
WF2.to_csv(f"{OUT}/walk_forward_no_none_option.csv", index=False)


def wf_daily(wf):
    keep = np.ones(N, bool)
    for r in wf.itertuples():
        if r.variant_used != "none":
            keep &= ~((year == r.year) & dec_by_name[r.variant_used])
    keep13 = keep & (year >= 2013)
    return keep, keep13


wf_keep, wf_keep13 = wf_daily(WF)
nf13 = year >= 2013
walk = dict(rule="each year from 2013 use the variant with the best cumulative (kept$ - all$) over all earlier years; "
                 "ties or best <= 0 -> no filter",
            wf_usd_2013_on=float(WF.wf_usd.sum()), no_filter_usd_2013_on=float(WF.no_filter_usd.sum()),
            wf_minus_no_filter=float(WF.wf_minus_no_filter.sum()),
            wf_mdd_2013_on=dd_and_worst(model_daily(wf_keep13))[0],
            no_filter_mdd_2013_on=dd_and_worst(model_daily(nf13))[0],
            wf_worst_day_2013_on=dd_and_worst(model_daily(wf_keep13))[1],
            no_filter_worst_day_2013_on=dd_and_worst(model_daily(nf13))[1],
            years_better=int((WF.wf_minus_no_filter > 0).sum()), years_worse=int((WF.wf_minus_no_filter < 0).sum()),
            pass_beats_no_filter=bool(WF.wf_minus_no_filter.sum() > 0),
            sensitivity_always_best_variant_minus_no_filter=float(WF2.wf_minus_no_filter.sum()))
print("walk-forward:", walk)
print(WF.to_string())

R["familywise_pass"] = familywise["pass_le5"]
R["walkforward_pass"] = walk["pass_beats_no_filter"]
R["worth_adopting"] = (R.pass_removed_lt0_2010_2017 & R.pass_removed_lt0_2018_2026 & R.pass_random_pct_le5
                       & R.familywise_pass & R.walkforward_pass)
R.to_csv(f"{OUT}/sweep_variants.csv", index=False)
pd.DataFrame(m3_years).to_csv(f"{OUT}/m3_skip_by_year.csv", index=False)

# no-look-ahead audit
audit = dict(signal_before_entry=bool((T.sig_time < T.entry_time).all()),
             m4_history_ends_before_signal=bool((T.M4_hist_last_bar < T.sig_time).all()),
             lookback_windows_strictly_before_trade_date="asserted for every trade in lookback_decisions",
             walk_forward_uses_only_earlier_years=True)
summary = dict(base=base, m1_vs_m2=dict(mean_disagree_share=float(cmp.disagree_share.mean()), kept=bool(keep_m2),
                                        rule=f">= {M2_MATERIAL:.0%} of eligible trades"),
               primary=R[R.variant == PRIMARY].iloc[0].to_dict(), familywise=familywise, walk_forward=walk,
               audit=audit, n_variants=len(R))
json.dump(summary, open(f"{OUT}/summary.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
pd.set_option("display.width", 250)
print(R[["variant", "n_removed", "share_removed", "removed_usd", "removed_usd_2010-2017", "removed_usd_2018-2026",
         "usd_per_trade_kept", "usd_per_trade_removed", "welch_t_kept_minus_removed", "random_pct", "model_mdd",
         "model_worst_day", "book_mdd", "book_worst_day", "worth_adopting"]].round(2).to_string())
