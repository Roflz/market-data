"""Section 13 reconciler. Both builds agree trade-for-trade; this computes the final numbers and diagnostics
from the agreed trade lists (Y's files; identical to X's), plus L2 from chosen_models_trades.csv."""
import json, sys
import numpy as np, pandas as pd
from scipy import stats
import calendar_days as cd
S = sys.argv[1]; R = S + "/s13_recon/"; Y = S + "/s13_Y/trades/"; X = S + "/s13_X/"
OUT = {}
def tt(x):
    x = np.asarray(x, float); return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan
def summ(T, years=None):
    x = T.net_usd.to_numpy(); s = np.sort(x)[::-1]
    d = dict(n=len(x), mean=round(x.mean(), 2), total=round(x.sum(), 2), t=round(tt(x), 2), median=float(np.median(x)),
             hit=round((x > 0).mean(), 3), worst=float(x.min()), best=float(x.max()),
             gross_mean=round(T.gross_usd.mean(), 2), gross_t=round(tt(T.gross_usd), 2),
             net_bp=round(T.net_bp.mean(), 2), gross_bp=round((1e4 * T.gross_pts / T.entry).mean(), 2),
             best5_share=round(s[:5].sum() / x.sum(), 2) if x.sum() else None)
    if years: d["per_year"] = round(len(x) / years, 2)
    return d
def blocks(T):
    y = pd.to_datetime(T.date).dt.year
    by = {int(k): dict(n=len(g), mean=round(g.net_usd.mean(), 2), total=round(g.net_usd.sum(), 2)) for k, g in T.groupby(y)}
    b = (y // 2 * 2).map(lambda v: f"{v}-{v+1}" if v < 2026 else "2026")
    bb = {k: dict(n=len(g), mean=round(g.net_usd.mean(), 2), total=round(g.net_usd.sum(), 2), t=round(tt(g.net_usd), 2)) for k, g in T.groupby(b)}
    return by, bb
def load(set_, era, inst, var):
    T = pd.read_csv(f"{Y}L1-{set_}-{era}-{inst}-{var}.csv"); T["date"] = pd.to_datetime(T.date); return T
YRS2 = ((pd.Timestamp("2026-11-06") - pd.Timestamp("2018-01-01")).days + 1) / 365.25
YRS1 = ((pd.Timestamp("2017-12-31") - pd.Timestamp("2010-06-07")).days + 1) / 365.25
# ---------- judged + variants
J = {}
for var in ["strict_time", "time", "strict_stop2x", "stop2x"]:
    for inst in ["MNQ", "MES"]:
        T = load("NFP", "2018-2026", inst, var); s = summ(T, YRS2); s["by_year"], s["by_2yr"] = blocks(T)
        if "stop" in var: s["stop_exits"] = int(T.exit_reason.str.contains("stop").sum())
        J[f"NFP_2018_2026_{inst}_{var}"] = s
for set_ in ["NFP", "CPI", "CPIorNFP"]:
    for era, yrs in [("2010-2017", YRS1), ("2018-2026", YRS2), ("2010-2026", YRS1 + YRS2)]:
        for inst in ["MNQ", "MES"]:
            for var in ["strict_time", "time"]:
                T = load(set_, era, inst, var)
                J[f"{set_}_{era}_{inst}_{var}"] = summ(T, yrs)
OUT["L1"] = J
def crit(var):
    q, e = J[f"NFP_2018_2026_MNQ_{var}"], J[f"NFP_2018_2026_MES_{var}"]
    return dict(mnq_mean_gt0=q["mean"] > 0, mnq_t_gt2=q["t"] > 2, mes_same_sign=np.sign(e["mean"]) == np.sign(q["mean"]),
                PASS=bool(q["mean"] > 0 and q["t"] > 2 and np.sign(e["mean"]) == np.sign(q["mean"])))
OUT["criteria_strict_primary"] = crit("strict_time"); OUT["criteria_literal"] = crit("time")
# ---------- stress tests on the judged MNQ set (primary = strict)
st = {}
for var in ["strict_time", "time"]:
    q = load("NFP", "2018-2026", "MNQ", var); e = load("NFP", "2018-2026", "MES", var); x = q.net_usd.to_numpy(); xe = e.net_usd.to_numpy()
    d = {}
    for k in (2, 3): d[f"cost_x{k}_mnq"] = dict(mean=round(x.mean() - 2 * (k - 1), 2), t=round(tt(x - 2 * (k - 1)), 2)); d[f"cost_x{k}_mes_mean"] = round(xe.mean() - 3.5 * (k - 1), 2)
    srt = np.argsort(x)[::-1]
    for k in (1, 3, 5): r = np.delete(x, srt[:k]); d[f"drop_best{k}"] = dict(mean=round(r.mean(), 2), t=round(tt(r), 2))
    r = q[q.date != "2026-11-06"].net_usd; d["drop_2026-11-06"] = dict(n=len(r), mean=round(r.mean(), 2), t=round(tt(r), 2))
    yrs = q.date.dt.year
    loyo = {int(y): round(tt(q.net_usd[yrs != y]), 2) for y in sorted(yrs.unique())}
    d["leave_one_year_out_t"] = loyo; d["leave_one_year_out_min_t"] = min(loyo.values())
    rng = np.random.default_rng(12345); bs = np.array([rng.choice(x, len(x)).mean() for _ in range(1000)])
    d["bootstrap_mean_95ci"] = [round(np.percentile(bs, 2.5), 2), round(np.percentile(bs, 97.5), 2)]
    d["wilcoxon_p_two_sided"] = round(float(stats.wilcoxon(x).pvalue), 3)
    d["sign_test_p"] = round(float(stats.binomtest(int((x > 0).sum()), len(x)).pvalue), 3)
    rng = np.random.default_rng(12345); g = q.gross_usd.to_numpy()
    sims = np.array([(g * rng.choice([-1, 1], len(g))).mean() - 2 for _ in range(1000)])
    d["random_direction_p_one_sided"] = float((sims >= x.mean()).mean())
    # MES on NQ signal days with ES follow-through is reported by Y (+8.21); MES on common days:
    st[var] = d
OUT["stress"] = st
# ---------- non-release controls (both builds' definitions)
cx = pd.read_csv(X + "L1_primary_time_MNQ_control_nonrelease_days.csv", parse_dates=["date"])
cy = pd.read_csv(Y + "L1-PLACEBO_nonrelease-2010-2026-MNQ-time.csv", parse_dates=["date"])
ctl = {}
for nm, c in [("X_strict_all_nonrelease_days", cx), ("Y_literal_nonrelease_cash_days", cy)]:
    for era, (a, b) in {"2010-2017": ("2010", "2017-12-31"), "2018-2026": ("2018", "2027")}.items():
        u = c[(c.date >= a) & (c.date <= b)]; ctl[f"{nm}_{era}"] = dict(n=len(u), mean=round(u.net_usd.mean(), 2), t=round(tt(u.net_usd), 2))
# first-Friday non-NFP days 2018-26 (days that look like NFP by calendar but are not) - same fade, strict
fr = cx[(cx.date >= "2018") & (cx.date.dt.weekday == 4) & (cx.date.dt.day <= 7)]
ctl["X_strict_first_fridays_not_NFP_2018_2026"] = dict(n=len(fr), mean=round(fr.net_usd.mean(), 2), t=round(tt(fr.net_usd), 2))
# 8:30-slot volatility proxy: NFP judged |move| vs control |move|
q = load("NFP", "2018-2026", "MNQ", "strict_time")
ctl["abs_signal_move_pts_median_NFP_vs_control_2018_26"] = [float(q.eval("abs(o830-entry)").median()), float(cx[cx.date >= "2018"].move_830_signal.abs().median())]
OUT["controls"] = ctl
# ---------- correlation with existing models' daily P&L
cm = pd.read_csv(S.split("/tmp")[0] + "chosen_models_trades.csv" if False else "chosen_models_trades.csv", parse_dates=["date"])
ses = pd.read_pickle("data/daily_sessions_NQ.pkl"); days = ses.index[(ses.cash_day) & (ses.index >= "2018-01-01") & (ses.index <= "2026-11-06")]
ex = cm.pivot_table(index="date", columns="model", values="usd", aggfunc="sum").reindex(days).fillna(0); ex["all3"] = ex.sum(axis=1)
corr = {}
for nm, T in [("L1_NFP_strict", load("NFP", "2018-2026", "MNQ", "strict_time")), ("L1_CPIorNFP_strict", load("CPIorNFP", "2018-2026", "MNQ", "strict_time"))]:
    l = T.set_index("date").net_usd.groupby(level=0).sum().reindex(days).fillna(0)
    missing = set(T.date) - set(days)
    c = {m: round(float(np.corrcoef(l, ex[m])[0, 1]), 3) for m in ex.columns}
    on = l != 0
    c_on = {m: round(float(np.corrcoef(l[on], ex[m][on])[0, 1]), 3) for m in ex.columns}
    comb = ex.all3 + l
    def mdd(s): cs = s.cumsum(); return round(float((cs - cs.cummax()).min()), 1)
    corr[nm] = dict(all_cash_days_corr=c, L1_days_only_corr=c_on, n_L1_days=int(on.sum()), L1_days_not_in_cash_calendar=[str(d.date()) for d in missing],
                    existing_days_traded_on_L1_days={m: int(((ex[m] != 0) & on).sum()) for m in ["opening_range", "overnight_break", "expiry_fade"]},
                    existing_usd_on_L1_days=round(float(ex.all3[on].sum()), 1), worst_combined_day=round(float(comb[on].min()), 1),
                    maxDD_existing=mdd(ex.all3), maxDD_existing_plus_L1=mdd(comb),
                    daily_sharpe_existing=round(float(ex.all3.mean() / ex.all3.std() * np.sqrt(252)), 2),
                    daily_sharpe_plus_L1=round(float(comb.mean() / comb.std() * np.sqrt(252)), 2))
OUT["correlation_existing"] = corr
# ---------- L2
cpi = set(cd.cpi_days()); nfp = set(pd.to_datetime(pd.read_csv(S + "/s13_Y/nfp_dates.csv").date)); rel = cpi | nfp
L2 = {}
for mdl in ["overnight_break", "opening_range"]:
    t = cm[cm.model == mdl].copy(); t["rel"] = t.date.isin(rel); r = {}
    for era, (a, b) in {"2010-2017": ("2010", "2017-12-31"), "2018-2026": ("2018", "2027"), "all": ("2000", "2100")}.items():
        u = t[(t.date >= a) & (t.date <= b)]; A, B = u[u.rel], u[~u.rel]; e = dict(n_rel=len(A), n_other=len(B))
        for col in ["usd", "R", "bp"]:
            w = stats.ttest_ind(A[col].dropna(), B[col].dropna(), equal_var=False)
            e[col] = dict(rel=round(A[col].mean(), 3), other=round(B[col].mean(), 3), welch_t=round(float(w.statistic), 2), p=round(float(w.pvalue), 3))
        e["rel_plain_t_usd"] = round(tt(A.usd), 2); e["rel_total_usd"] = round(A.usd.sum(), 1)
        e["worse_p05"] = bool(e["usd"]["rel"] < e["usd"]["other"] and e["usd"]["p"] < 0.05); r[era] = e
    r["adopt_skip"] = bool(r["2010-2017"]["worse_p05"] and r["2018-2026"]["worse_p05"]); L2[mdl] = r
OUT["L2"] = L2
json.dump(OUT, open(R + "recon_summary.json", "w"), indent=1, default=str)
print(json.dumps(OUT, indent=1, default=str))
