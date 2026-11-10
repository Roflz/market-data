import os, sys, json
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.append(os.getcwd())
import calendar_days as cd
from l1_fade import run, build

DATA_START, DATA_END = pd.Timestamp("2010-06-07"), pd.Timestamp("2026-11-06")
ERA1 = (pd.Timestamp("2010-01-01"), pd.Timestamp("2017-12-31"))
ERA2 = (pd.Timestamp("2018-01-01"), DATA_END)

cpi = cd.cpi_days()
nfp = set(pd.to_datetime(pd.read_csv(f"{HERE}/nfp_dates.csv").date))
release = cpi | nfp
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
cash_days = set(ds.index[ds.cash_day])


def tags(d):
    return dict(cpi=d in cpi, nfp=d in nfp, both=(d in cpi and d in nfp), cash_day=d in cash_days)


def years_span(a, b):
    return ((min(b, DATA_END) - max(a, DATA_START)).days + 1) / 365.25


def summarize(T, a, b):
    if len(T) == 0:
        return dict(n=0)
    x = T.net_usd.to_numpy()
    n = len(x); m = x.mean(); sd = x.std(ddof=1) if n > 1 else np.nan
    t = m / (sd / np.sqrt(n)) if n > 1 and sd > 0 else np.nan
    tot = x.sum()
    best5 = np.sort(x)[-5:].sum()
    dt = pd.to_datetime(T.date)
    by_year = T.groupby(dt.dt.year).net_usd.agg(["count", "mean", "sum"]).round(2)
    blk = (dt.dt.year // 2 * 2)
    by_blk = T.groupby(blk.map(lambda y: f"{y}-{y+1}")).net_usd.agg(["count", "mean", "sum"]).round(2)
    return dict(n=n, mean_net_usd=round(m, 3), total_net_usd=round(tot, 2), mean_gross_usd=round(T.gross_usd.mean(), 3),
                mean_net_bp=round(T.net_bp.mean(), 3), mean_gross_pts=round(T.gross_pts.mean(), 3), t=round(t, 3),
                median_net_usd=round(float(np.median(x)), 2), hit_rate=round((x > 0).mean(), 3),
                worst=round(x.min(), 2), best=round(x.max(), 2),
                best5_share_of_total=round(best5 / tot, 3) if tot != 0 else None,
                trades_per_year=round(n / years_span(a, b), 2),
                exit_reasons=T.exit_reason.value_counts().to_dict(),
                by_year={int(k): v for k, v in by_year.to_dict("index").items()},
                by_2yr_block=by_blk.to_dict("index"))


def sl(T, a, b, mask=None):
    dt = pd.to_datetime(T.date)
    k = (dt >= a) & (dt <= b)
    if mask is not None:
        k &= mask(T)
    return T[k].reset_index(drop=True)


def random_dir_control(T, cost_usd, seed=12345, reps=1000):
    rng = np.random.default_rng(seed)
    g = T.gross_usd.to_numpy()
    sims = np.array([(rng.choice([-1, 1], size=len(g)) * g).mean() - cost_usd for _ in range(reps)])
    actual = T.net_usd.mean()
    return dict(reps=reps, seed=seed, actual_mean_net=round(actual, 3), random_mean=round(sims.mean(), 3),
                random_p95=round(np.percentile(sims, 95), 3), p_one_sided=float((sims >= actual).mean()))


OUT = {"nfp_dates_source": "official BLS Employment Situation archive (https://www.bls.gov/bls/news-release/empsit.htm, fetched 2026-11-08), 202 dates 2010-01-08..2026-11-06; proxy NOT used; saved nfp_dates.csv", "cpi_dates_source": "calendar_days.cpi_days() (project data/cpi_dates.csv)", "primary_signal": "8:30 bar open -> 8:45 bar open (as written); strict variant = 8:30 open -> 8:44 bar close"}
RULES = []
os.makedirs(f"{HERE}/trades", exist_ok=True)


def save(name, T):
    p = f"{HERE}/trades/{name}.csv"
    T.to_csv(p, index=False)
    return p


# ---------------- L1 runs over all release days ----------------
runs = {}
skips = {}
for sym in ["NQ", "ES"]:
    for var, kw in {"time": {}, "stop2x": dict(stop_mult=2.0), "strict_time": dict(signal="close844"),
                    "strict_stop2x": dict(signal="close844", stop_mult=2.0)}.items():
        runs[(sym, var)], skips[(sym, var)] = run(sym, release, tags, **kw)
# ES traded with the NQ direction (report only)
nq = runs[("NQ", "time")]
fmap = {pd.Timestamp(d): (1 if s == "long" else -1) for d, s in zip(nq.date, nq.side)}
runs[("ES", "time_nqsig")], skips[("ES", "time_nqsig")] = run("ES", release, tags, force_map=fmap)
for k, v in skips.items():
    v.to_csv(f"{HERE}/trades/skips_{k[0]}_{k[1]}.csv", index=False)

is_nfp = lambda T: T.nfp.astype(bool)
is_cpi = lambda T: T.cpi.astype(bool)
sets = {"NFP": is_nfp, "CPI": is_cpi, "CPIorNFP": None}
eras = {"2018-2026": ERA2, "2010-2017": ERA1, "2010-2026": (ERA1[0], DATA_END)}
INSTR = {"NQ": "MNQ", "ES": "MES"}
COST_USD = {"NQ": 2.0, "ES": 3.5}

L1 = {}
for (sym, var), T in runs.items():
    for sname, msk in sets.items():
        for ename, (a, b) in eras.items():
            S = sl(T, a, b, msk)
            key = f"L1-{sname}-{ename}-{INSTR[sym]}-{var}"
            L1[key] = summarize(S, a, b)
            L1[key]["csv"] = save(key, S)
OUT["L1"] = L1

# judged
J_mnq = sl(runs[("NQ", "time")], *ERA2, is_nfp)
J_mes = sl(runs[("ES", "time")], *ERA2, is_nfp)
sm, se = summarize(J_mnq, *ERA2), summarize(J_mes, *ERA2)
c1 = sm["mean_net_usd"] > 0; c2 = sm["t"] > 2; c3 = np.sign(se["mean_net_usd"]) == np.sign(sm["mean_net_usd"])
OUT["L1_judged"] = dict(mnq=sm, mes=se, mnq_mean_gt0=bool(c1), mnq_t_gt2=bool(c2), mes_same_sign=bool(c3),
                        PASS=bool(c1 and c2 and c3),
                        random_direction_control_mnq=random_dir_control(J_mnq, 2.0),
                        random_direction_control_mes=random_dir_control(J_mes, 3.5))
# skip reasons on judged set
nfp2 = sorted(d for d in nfp if ERA2[0] <= d <= ERA2[1])
for sym in ["NQ", "ES"]:
    sk = skips[(sym, "time")]
    sk2 = sk[pd.to_datetime(sk.date).isin(nfp2)]
    OUT["L1_judged"][f"skipped_nfp_2018_2026_{sym}"] = sk2.assign(date=sk2.date.astype(str)).to_dict("records")
OUT["L1_judged"]["nfp_days_2018_2026_in_list"] = len(nfp2)

# placebo: same fade on non-release cash days (report only)
non_rel = {d for d in cash_days if d not in release and d >= DATA_START}
for sym in ["NQ", "ES"]:
    P, _ = run(sym, non_rel, tags)
    for ename, (a, b) in eras.items():
        key = f"L1-PLACEBO_nonrelease-{ename}-{INSTR[sym]}-time"
        S = sl(P, a, b)
        s = summarize(S, a, b); s.pop("by_year"); s.pop("by_2yr_block")
        OUT.setdefault("L1_placebo", {})[key] = s
    save(f"L1-PLACEBO_nonrelease-2010-2026-{INSTR[sym]}-time", P)

# combined exposure with existing models on judged days
cm = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
jd = pd.to_datetime(J_mnq.date)
exp = {}
for m in ["overnight_break", "opening_range", "expiry_fade"]:
    dd = set(cm.date[cm.model == m])
    same = jd.isin(dd)
    exp[m] = dict(days_with_both=int(same.sum()), of=len(jd))
x = J_mnq.assign(date=jd).merge(cm.groupby("date").usd.sum().rename("existing_usd"), left_on="date", right_index=True, how="left").fillna({"existing_usd": 0})
exp["corr_L1_vs_existing_same_day_usd"] = round(float(np.corrcoef(x.net_usd, x.existing_usd)[0, 1]), 3)
exp["worst_combined_day_usd"] = round(float((x.net_usd + x.existing_usd).min()), 2)
OUT["L1_overlap_existing"] = exp

# ---------------- L2 ----------------
L2 = {}
for model in ["overnight_break", "opening_range"]:
    t = cm[cm.model == model].copy()
    t["release"] = t.date.isin(release); t["cpi"] = t.date.isin(cpi); t["nfp"] = t.date.isin(nfp)
    save(f"L2-{model}-labeled", t)
    res = {}
    for ename, (a, b) in [("2010-2017", ERA1), ("2018-2026", ERA2), ("2010-2026", (ERA1[0], DATA_END))]:
        u = t[(t.date >= a) & (t.date <= b)]
        r_, o_ = u[u.release], u[~u.release]
        e = {}
        for col in ["usd", "R", "bp"]:
            w = stats.ttest_ind(r_[col].dropna(), o_[col].dropna(), equal_var=False)
            e[col] = dict(release_mean=round(r_[col].mean(), 3), other_mean=round(o_[col].mean(), 3),
                          diff=round(r_[col].mean() - o_[col].mean(), 3), welch_t=round(float(w.statistic), 3),
                          p_two_sided=round(float(w.pvalue), 4))
        e["n_release"], e["n_other"] = len(r_), len(o_)
        e["release_total_usd"] = round(r_.usd.sum(), 2)
        for sub, col in [("cpi_days", "cpi"), ("nfp_days", "nfp")]:
            s = u[u[col]]
            e[sub] = dict(n=len(s), mean_usd=round(s.usd.mean(), 3) if len(s) else None)
        # permutation control on the usd difference (report only)
        rng = np.random.default_rng(12345)
        lab = u.release.to_numpy(); v = u.usd.to_numpy(); obs = v[lab].mean() - v[~lab].mean()
        perm = []
        for _ in range(1000):
            pl = rng.permutation(lab); perm.append(v[pl].mean() - v[~pl].mean())
        e["perm_p_two_sided_usd"] = float((np.abs(perm) >= abs(obs)).mean())
        res[ename] = e
    worse1 = res["2010-2017"]["usd"]["diff"] < 0 and res["2010-2017"]["usd"]["p_two_sided"] < 0.05
    worse2 = res["2018-2026"]["usd"]["diff"] < 0 and res["2018-2026"]["usd"]["p_two_sided"] < 0.05
    res["adopt_skip"] = bool(worse1 and worse2)
    res["worse_p05_2010_2017"], res["worse_p05_2018_2026"] = bool(worse1), bool(worse2)
    L2[model] = res
OUT["L2"] = L2

json.dump(OUT, open(f"{HERE}/summary.json", "w"), indent=1, default=str)
print(json.dumps(OUT["L1_judged"], indent=1, default=str)[:4000])
for k in L1:
    if k.endswith("-time") or k.endswith("stop2x") or "nqsig" in k:
        s = L1[k]
        if s["n"]:
            print(f"{k:45s} n={s['n']:4d} mean={s['mean_net_usd']:8.2f} tot={s['total_net_usd']:9.1f} t={s['t']:6.2f} gross={s['mean_gross_usd']:7.2f} bp={s['mean_net_bp']:6.2f} hit={s['hit_rate']:.2f} b5={s['best5_share_of_total']}")
print(json.dumps(OUT["L1_placebo"], indent=0, default=str)[:3000])
print(json.dumps(OUT["L1_overlap_existing"], default=str))
print(json.dumps(L2, indent=1, default=str))
