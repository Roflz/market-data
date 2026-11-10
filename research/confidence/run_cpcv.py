"""
CPCV + overfitting statistics for the MNQ (NQ) v1 entry models (cpcv.py has the methods and the paper references).

Stages (default: both):
    python3 run_cpcv.py [cpcv] [stats] [--models logit,gbm] [--groups 8] [--k 2]
    cpcv   out/entries_NQ_15.parquet, run_pipeline.feature_list('entry', 'NQ') (82 features), the walk-forward's own
           preparation (walkforward._prepare: holdout rows dropped, sorted, signed features x d, overlap weights) and
           its own fit + threshold rule (cpcv.wf_fitter -> walkforward._fit_and_threshold: C / calibration and the
           $-maximising threshold chosen on the TRAINING rows' last 1-2 years only). CPCV with N = 8 time groups
           (session-aligned), k = 2 test groups -> 28 splits, 7 paths; purge = label windows overlapping a test
           block (+ the walk-forward's 1-day margin); embargo = the next 1% of events after each test block (~2.5
           months of NQ events, longer than the ~20-session memory of the features).
           -> out/cpcv_NQ.csv (tables: split, path, path_2013on, year, summary), one trials.csv row per model
           (module 'entry-cpcv').
    stats  deflated Sharpe ratio of the WALK-FORWARD daily $ (out/oos_entry_NQ_<model>.parquet) with N = the trial
           counts in out/trials.csv; PBO by CSCV over the MNQ entry configurations whose out-of-sample yearly
           results are on file; -> out/overfit_stats_NQ.md (also reads out/cpcv_NQ.csv).

Money: net $ per 1 micro (MNQ, $2/pt) after costs, label y_1.5 / pnl_usd_1.5 (1.5 R target, 16-bar limit).
Never touches the locked holdout (2025-07-01 sessions on): the datasets are cut before it and _prepare(final=False)
drops any row whose label reaches it.
Run: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 run_cpcv.py
"""
import argparse
import glob
import json
import math
import os
import time
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

import cpcv
import run_pipeline as rp
import walkforward as wf

warnings.filterwarnings("ignore", category=UserWarning)
SYM = "NQ"
TF = 15
N_GROUPS, K = 8, 2
EMBARGO_FRAC = 0.01
N_RANDOM = 200
MIN_AVAIL_MB = 7000
CSV = os.path.join(rp.OUT, f"cpcv_{SYM}.csv")
MD = os.path.join(rp.OUT, f"overfit_stats_{SYM}.md")
WF_FIRST_YEAR = 2013


def say(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def wait_for_ram(min_mb=MIN_AVAIL_MB):
    """Block until MemAvailable >= min_mb (re-check every 60 s): the machine runs several jobs at once."""
    while True:
        with open("/proc/meminfo") as f:
            avail = next(int(l.split()[1]) // 1024 for l in f if l.startswith("MemAvailable"))
        if avail >= min_mb:
            say(f"RAM available {avail} MB")
            return
        say(f"RAM available {avail} MB < {min_mb}: waiting 60 s")
        time.sleep(60)


# ============================================================================================ stage cpcv
def load_prepared():
    feats = rp.feature_list("entry", SYM)
    a = rp.wf_args("entry")
    cols = list(dict.fromkeys(["t", "d", "market", "session", a["t_end"], a["label"], a["pnl"]] + feats))
    wait_for_ram()
    data = rp.load("entry", SYM, TF, columns=cols)
    S = wf._prepare(data, feats, "entry", a["label"], a["pnl"], a["t_end"], None, False, "trade", None, "auto")
    del data
    return feats, S


def summarize(model, res, S, years_span, all_n, all_ppt):
    pn = S["pnl"]
    sess = S["df"]["session"].to_numpy()
    cal = np.unique(sess)
    ps = cpcv.path_stats(res, pn, sess, years_span, cal)
    rnd = cpcv.random_skip_paths(pn, ps.n_trades.to_numpy(), N_RANDOM, seed=0)
    ps["random_usd_per_trade"] = np.nanmean(rnd, axis=1)
    ps["random_p5"] = np.nanpercentile(rnd, 5, axis=1)
    ps["random_p95"] = np.nanpercentile(rnd, 95, axis=1)
    ps["all_usd_per_trade"] = all_ppt
    ps["all_n"] = all_n
    # the same paths restricted to the walk-forward's test period (2013 .. 2025H1), for a like-for-like comparison
    yr = S["year"]
    later = yr >= WF_FIRST_YEAR
    sub = cpcv.CPCVResult(res.splits, res.groups[later], res.P, res.p[:, later], res.take[:, later], res.n_groups,
                          res.k)
    span2 = (S["data_end"] - pd.Timestamp(WF_FIRST_YEAR, 1, 1)) / wf.YEAR   # calendar span 2013-01-01 .. data end
    ps2 = cpcv.path_stats(sub, pn[later], sess[later], span2, np.unique(sess[later]))
    ps2["all_usd_per_trade"] = float(pn[later].mean())
    ps2["all_n"] = int(later.sum())
    by = cpcv.path_by_year(res, pn, yr)
    allyr = pd.DataFrame({"year": yr, "pnl": pn}).groupby("year")["pnl"].agg(["size", "sum", "mean"])
    g = by.groupby("year")
    Y = pd.DataFrame({"all_n": allyr["size"], "all_total_usd": allyr["sum"], "all_usd_per_trade": allyr["mean"],
                      "path_n_median": g.n_trades.median(), "path_total_min": g.total_usd.min(),
                      "path_total_median": g.total_usd.median(), "path_total_max": g.total_usd.max(),
                      "path_usd_per_trade_median": g.usd_per_trade.median(),
                      "share_paths_positive": g.total_usd.apply(lambda s: float((s > 0).mean()))}).reset_index()
    out = []
    for name, df in (("split", res.splits), ("path", ps), ("path_2013on", ps2), ("year", Y)):
        d = df.copy()
        d.insert(0, "model", model)
        d.insert(0, "table", name)
        out.append(d)
    return pd.concat(out, ignore_index=True), ps, ps2, rnd


def q(s):
    s = pd.Series(s).dropna()
    return dict(min=s.min(), p5=s.quantile(0.05), median=s.median(), p95=s.quantile(0.95), max=s.max())


def stage_cpcv(models):
    feats, S = load_prepared()
    t, te = S["t"], S["t_end"]
    S["data_end"] = wf.session_label([t.max()])[0] + pd.Timedelta(days=1)
    years_span = (S["data_end"] - wf.session_label([t.min()])[0]) / wf.YEAR
    pn = S["pnl"]
    say(f"{len(pn):,} pre-holdout NQ events {t.min()} .. {t.max()} ({years_span:.2f} years), {len(feats)} features; "
        f"all events {pn.mean():.3f} $/trade")
    vote_idx = [feats.index(c) for c in wf.vote_columns(feats)]
    tables = []
    for model in models:
        wait_for_ram()
        t0 = time.time()
        fit = cpcv.wf_fitter(model, S["X"], S["y"], S["w"], pn, S["year"], te, kind="entry",
                             min_keep=rp.WF_KW["min_keep"], vote_idx=vote_idx)
        res = cpcv.run_cpcv(S["X"], S["y"], pn, t, pd.DatetimeIndex(te), fit, n_groups=N_GROUPS, k=K,
                            sessions=S["df"]["session"].to_numpy(), purge=wf.PURGE, embargo_frac=EMBARGO_FRAC,
                            verbose=True)
        rt = time.time() - t0
        tab, ps, ps2, rnd = summarize(model, res, S, years_span, len(pn), float(pn.mean()))
        g = res.groups
        bounds = [str(S["df"]["session"].iloc[np.flatnonzero(g == i)[0]])[:10] for i in range(N_GROUPS)]
        summ = dict(model=model, n_events=len(pn), n_splits=len(res.splits), n_paths=res.P.shape[0],
                    group_starts="|".join(bounds), median_train=float(res.splits.n_train.median()),
                    median_purged_embargoed=float(res.splits.n_purged_embargoed.median()),
                    share_paths_positive=float((ps.total_usd > 0).mean()),
                    share_paths_beat_random_p95=float((ps.usd_per_trade > ps.random_p95).mean()),
                    runtime_s=round(rt, 1),
                    **{f"usd_trade_{k_}": v for k_, v in q(ps.usd_per_trade).items()},
                    **{f"usd_year_{k_}": v for k_, v in q(ps.usd_per_year).items()},
                    **{f"sharpe_ann_{k_}": v for k_, v in q(ps.sharpe_ann).items()},
                    **{f"usd_trade_2013on_{k_}": v for k_, v in q(ps2.usd_per_trade).items()},
                    **{f"usd_year_2013on_{k_}": v for k_, v in q(ps2.usd_per_year).items()},
                    trades_median=float(ps.n_trades.median()), all_usd_per_trade=float(pn.mean()),
                    random_usd_per_trade=float(np.nanmean(rnd)), split_auc_median=float(res.splits.get(
                        "auc", pd.Series(dtype=float)).median()) if "auc" in res.splits else np.nan)
        tables.append(tab)
        tables.append(pd.DataFrame([dict(table="summary", **summ)]))
        say(f"{model}: paths $/trade {ps.usd_per_trade.round(2).tolist()} ; $/year {ps.usd_per_year.round(0).tolist()} "
            f"({rt:.0f}s)")
        params = dict(tf=TF, scope=SYM, model=model, n_features=len(feats), cv="CPCV", n_groups=N_GROUPS, k=K,
                      n_splits=len(res.splits), n_paths=int(res.P.shape[0]), purge_days=1,
                      embargo_frac=EMBARGO_FRAC, min_keep=rp.WF_KW["min_keep"],
                      threshold_rule="walkforward._fit_and_threshold on training rows (last 1-2 training years)",
                      period="2010..2025H1 (pre-holdout)", **rp.wf_args("entry"))
        rp.log_trial(module="entry-cpcv", scope=SYM, model=model, target=rp.wf_args("entry")["label"],
                     n_folds=len(res.splits), oos_rows=len(pn), oos_auc="", oos_kept=int(ps.n_trades.median()),
                     oos_keep_share=round(float(ps.n_trades.median()) / len(pn), 4),
                     oos_usd_total=round(float(ps.total_usd.median()), 1),
                     oos_usd_per_trade=round(float(ps.usd_per_trade.median()), 3),
                     oos_usd_per_year=round(float(ps.usd_per_year.median()), 1),
                     baseline_usd_per_trade=round(float(pn.mean()), 3), runtime_s=round(rt), parameters=json.dumps(params),
                     note=f"CPCV {N_GROUPS}/{K}: {res.P.shape[0]} paths; values = median path; positive paths "
                          f"{(ps.total_usd > 0).sum()}/{len(ps)}; same evaluation of an existing configuration")
        pd.concat(tables, ignore_index=True).to_csv(CSV, index=False)     # save after each model
        del res, fit
    return pd.concat(tables, ignore_index=True)


# ============================================================================================ stage stats
def wf_daily(model):
    """Session-level daily $ of the walk-forward's taken trades (0 on sessions without a trade), on the calendar of
    sessions that have any NQ event in the OOS file (2013 .. 2025H1)."""
    o = pd.read_parquet(os.path.join(rp.OUT, f"oos_entry_{SYM}_{model}.parquet"),
                        columns=["fold", "take", "pnl", "session", "market"])
    o = o[o.market == SYM] if "market" in o else o
    cal = np.unique(o.session.to_numpy())
    return pd.Series(cpcv.daily_series(o["take"].to_numpy(), o.pnl.to_numpy(), o.session.to_numpy(), cal), index=cal)


def pooled_nq_daily(model, cal):
    o = pd.read_parquet(os.path.join(rp.OUT, f"oos_entry_pooled_{model}.parquet"),
                        columns=["fold", "take", "pnl", "session", "market"])
    o = o[o.market == SYM]
    return pd.Series(cpcv.daily_series(o["take"].to_numpy(), o.pnl.to_numpy(), o.session.to_numpy(), cal), index=cal)


YEARS = [str(y) for y in range(2013, 2025)] + ["2025H1"]


def yearly_configs():
    """{config name: pd.Series(total OOS $ by fold label '2013'..'2025H1')} for every MNQ entry configuration with
    yearly out-of-sample results on file. Duplicated series (same configuration logged twice) are dropped later."""
    C = {}
    ef = pd.read_csv(os.path.join(rp.OUT, "entry_folds.csv"))
    ef["fold"] = ef["fold"].astype(str)
    for m, d in ef[ef.scope == SYM].groupby("model"):
        C[f"entry NQ {m}"] = d.set_index("fold")["total_usd"]
    for m in ("vote", "logit", "gbm"):
        p = os.path.join(rp.OUT, f"oos_entry_pooled_{m}.parquet")
        if os.path.exists(p):
            o = pd.read_parquet(p, columns=["fold", "take", "pnl", "market"])
            o = o[(o.market == SYM) & o["take"]]
            C[f"entry pooled {m} (NQ trades)"] = o.groupby(o.fold.astype(str))["pnl"].sum()
    for p in sorted(glob.glob(os.path.join(rp.OUT, f"approach_folds_{SYM}_*.csv"))):
        d = pd.read_csv(p)
        d["fold"] = d["fold"].astype(str)
        C["approach " + os.path.basename(p)[len(f"approach_folds_{SYM}_"):-4]] = d.set_index("fold")["total_usd"]
    p = os.path.join(rp.OUT, f"feature_blocks_{SYM}.csv")
    if os.path.exists(p):
        d = pd.read_csv(p)
        d = d[d.period.astype(str).isin(YEARS)]
        for key, g in d.groupby(["feature_set", "subset", "model"]):
            C["features " + "/".join(map(str, key))] = g.set_index(g.period.astype(str))["total_usd"]
    p = os.path.join(rp.OUT, f"context_rule_{SYM}.csv")
    if os.path.exists(p):
        d = pd.read_csv(p)
        d = d[(d.section == "wf_by_year") & d.period.astype(str).isin(YEARS)]
        for key, g in d.groupby("group"):
            C["context " + key] = g.set_index(g.period.astype(str))["usd_total"]
    for p in sorted(glob.glob(os.path.join(rp.OUT, f"h1h2_{SYM}_folds_*.csv"))):
        d = pd.read_csv(p)
        d["fold"] = d["fold"].astype(str)
        C["h1h2 " + os.path.basename(p)[len(f"h1h2_{SYM}_folds_"):-4]] = d.set_index("fold")["total_usd"]
    return C


def build_matrix(C, years):
    """T x N matrix on `years` of the configurations covering all of them; identical columns dropped."""
    cols, names = [], []
    for k_, s in C.items():
        s = s.reindex(years)
        if s.isna().any():
            continue
        v = s.to_numpy(np.float64)
        if any(np.allclose(v, c, atol=1.0) for c in cols):
            continue
        cols.append(v); names.append(k_)
    return np.column_stack(cols), names


def trial_counts():
    t = pd.read_csv(os.path.join(rp.OUT, "trials.csv"))
    ent = t[t.module.astype(str).str.startswith("entry") & (t.module != "entry-cpcv")]
    nq = ent[ent.scope.astype(str).isin([SYM, "pooled"])]
    return dict(all_rows=len(t), entry=len(ent), entry_nq=len(nq),
                by_module=ent.module.value_counts().to_dict())


def fmt(v, d=2):
    return "n/a" if v is None or (isinstance(v, float) and not np.isfinite(v)) else f"{v:,.{d}f}"


def md_table(df, floatfmt=2):
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(fmt(v, floatfmt) if isinstance(v, (float, np.floating)) else str(v)
                                        for v in r.to_numpy()) + " |")
    return "\n".join(lines)


def stage_stats():
    lines = [f"# Overfitting statistics: MNQ v1 entry models (CPCV, deflated Sharpe ratio, PBO)", "",
             f"Generated {datetime.now():%Y-%m-%d %H:%M} by run_cpcv.py (methods: cpcv.py). Money = net $ per 1 MNQ "
             "micro after costs, label = 1.5 R target / 16-bar limit (v1). Everything is out of sample and before "
             "the locked holdout (sessions from 2025-07-01 are never used).", ""]
    # ---------------------------------------------------------------- CPCV
    if os.path.exists(CSV):
        T = pd.read_csv(CSV, low_memory=False)
        sm = T[T.table == "summary"].dropna(axis=1, how="all")
        lines += ["## 1. Combinatorial purged cross-validation (CPCV)", "",
                  f"N = {N_GROUPS} time groups of the pre-holdout NQ events (2010-01 .. 2025-06, session-aligned), "
                  f"every pair of groups as the test set (k = {K}) -> {math.comb(N_GROUPS, K)} splits, "
                  f"{cpcv.n_paths(N_GROUPS, K)} complete backtest paths. Training rows whose label window overlaps a "
                  "test block (+1 day) are purged; the next 1% of events after each test block are embargoed. Model, C "
                  "/ calibration and the threshold use only the training rows (the walk-forward's own rule: "
                  "threshold = best mean $/trade with >= 5% kept on the last 1-2 training years). Unlike the "
                  "walk-forward, CPCV also trains on data AFTER the test period, and covers 2010-2012.", ""]
        if len(sm):
            gs = sm.iloc[0].get("group_starts", "")
            lines += [f"Group start sessions: {str(gs).replace('|', ', ')}.", ""]
        rows = []
        for _, r in sm.iterrows():
            rows.append({"model": r.model, "paths +": f"{int(round(r.share_paths_positive * 7))}/7",
                         "$/trade min": r.usd_trade_min, "p5": r.usd_trade_p5, "median": r.usd_trade_median,
                         "p95": r.usd_trade_p95, "$/year min": r.usd_year_min, "$/year p5": r.usd_year_p5,
                         "$/year median": r.usd_year_median, "$/year p95": r.usd_year_p95,
                         "trades/path": r.trades_median, "all events $/trade": r.all_usd_per_trade,
                         "random skip $/trade": r.random_usd_per_trade,
                         "paths > random p95": f"{int(round(r.share_paths_beat_random_p95 * 7))}/7"})
        if rows:
            lines += ["### Path distribution, 2010 - 2025H1 (7 paths)", "", md_table(pd.DataFrame(rows)), "",
                      "(p5 / p95 over 7 paths are interpolated between the lowest/highest two; min and max are the "
                      "actual extremes.)", ""]
            rows2 = []
            for _, r in sm.iterrows():
                rows2.append({"model": r.model, "$/trade min": r.usd_trade_2013on_min,
                              "$/trade median": r.usd_trade_2013on_median, "$/trade max": r.usd_trade_2013on_max,
                              "$/year min": r.usd_year_2013on_min, "$/year median": r.usd_year_2013on_median,
                              "$/year max": r.usd_year_2013on_max})
            lines += ["### Same paths, 2013 - 2025H1 only (the walk-forward's test period)", "",
                      md_table(pd.DataFrame(rows2)), ""]
            P = T[T.table == "path"].dropna(axis=1, how="all")
            cols = ["model", "path", "n_trades", "usd_per_trade", "usd_per_year", "hit_rate", "sharpe_ann",
                    "random_usd_per_trade", "random_p5", "random_p95"]
            lines += ["### Every path", "", md_table(P[[c for c in cols if c in P]]), ""]
            Y = T[T.table == "year"].dropna(axis=1, how="all")
            cols = ["model", "year", "all_n", "all_usd_per_trade", "path_n_median", "path_usd_per_trade_median",
                    "path_total_min", "path_total_median", "path_total_max", "share_paths_positive"]
            lines += ["### By year (each year is tested on all 7 paths)", "", md_table(Y[[c for c in cols if c in Y]]),
                      ""]
    # ---------------------------------------------------------------- DSR
    tc = trial_counts()
    lines += ["## 2. Deflated Sharpe ratio of the walk-forward daily $ (Bailey & Lopez de Prado 2014)", "",
              "DSR = Z[(SR - SR0) sqrt(T-1) / sqrt(1 - skew*SR + (kurt-1)/4 * SR^2)], "
              "SR0 = sqrt(V[SR_n]) * ((1-g) Z^-1(1-1/N) + g Z^-1(1-1/(N e))), all Sharpe ratios per SESSION "
              "(non-annualized; annualized = x sqrt(252) shown for reading), kurt not excess. The daily series = $ "
              "of the walk-forward's taken trades per Globex session 2013-01 .. 2025-06, 0 on sessions without a "
              "trade.", "",
              f"Trials in out/trials.csv: {tc['all_rows']} rows, {tc['entry']} entry configurations "
              f"(modules {tc['by_module']}), {tc['entry_nq']} of them on NQ or pooled (which includes NQ). The "
              "CPCV rows (module entry-cpcv) re-evaluate existing configurations and are not counted.", ""]
    cal_d = wf_daily("logit")
    daily = {}
    for m in ("vote", "logit", "gbm"):
        p = os.path.join(rp.OUT, f"oos_entry_{SYM}_{m}.parquet")
        if os.path.exists(p):
            daily[f"entry NQ {m}"] = wf_daily(m).reindex(cal_d.index, fill_value=0.0)
        p = os.path.join(rp.OUT, f"oos_entry_pooled_{m}.parquet")
        if os.path.exists(p):
            daily[f"entry pooled {m} (NQ trades)"] = pooled_nq_daily(m, cal_d.index)
    sr_daily = {k_: cpcv.sharpe(v.to_numpy()) for k_, v in daily.items()}
    C = yearly_configs()
    sr_year = {}
    for k_, s in C.items():
        s = s.reindex([y for y in YEARS if y != "2025H1"]).dropna()
        if len(s) >= 8 and k_ not in sr_daily:
            sr_year[k_] = cpcv.sharpe(s.to_numpy()) / math.sqrt(252)
    srs = np.array(list(sr_daily.values()) + list(sr_year.values()), float)
    srs = srs[np.isfinite(srs)]
    V_emp = float(np.var(srs, ddof=1))
    Td = len(cal_d)
    lines += [f"V[SR_n] (variance of the trials' per-session Sharpe ratios): {V_emp:.3g} from {len(srs)} "
              f"configurations: {len(sr_daily)} with a daily series on file (exact) and {len(sr_year)} with only "
              "yearly results (APPROXIMATION: per-session SR ~ Sharpe of the 12 yearly totals 2013-2024 / sqrt(252), "
              "which has about the same sampling error as a daily estimate under i.i.d. days). Alternative: the "
              f"sampling variance of one SR estimate under the null, 1/(T-1) = {1 / (Td - 1):.3g} (T = {Td} "
              "sessions), i.e. trials that differ only by noise.", ""]
    rows = []
    for m in ("logit", "gbm", "vote"):
        k_ = f"entry NQ {m}"
        if k_ not in daily:
            continue
        x = daily[k_].to_numpy()
        for nname, N in (("all entry trials", tc["entry"]), ("NQ/pooled entry trials", tc["entry_nq"])):
            for vname, V in (("cross-trial V", V_emp), ("null V = 1/(T-1)", 1 / (Td - 1))):
                d = cpcv.deflated_sharpe(x, N, V)
                rows.append({"model": m, "N": f"{N} ({nname})", "V": vname, "T sessions": d["T"],
                             "$ total": float(x.sum()), "SR/session": d["sr"], "SR ann.": d["sr_ann"],
                             "skew": d["skew"], "kurt": d["kurt"], "SR0 ann.": d["sr0_ann"], "PSR(0)": d["psr0"],
                             "DSR": d["dsr"]})
    D = pd.DataFrame(rows)
    lines += [md_table(D, 3), "",
              "Read: PSR(0) = probability the true Sharpe is above 0 ignoring how many things were tried; DSR = the "
              "same against the best Sharpe expected from N tries of zero-skill rules. DSR >= 0.95 would be a "
              "discovery at 95%.", ""]
    srows = [{"configuration": k_, "SR/session": v, "SR ann.": v * math.sqrt(252), "source": "daily"}
             for k_, v in sr_daily.items()]
    srows += [{"configuration": k_, "SR/session": v, "SR ann.": v * math.sqrt(252), "source": "yearly approx."}
              for k_, v in sr_year.items()]
    lines += ["Trial Sharpe ratios used for V[SR_n]:", "",
              md_table(pd.DataFrame(srows).sort_values("SR ann.", ascending=False), 3), ""]
    # ---------------------------------------------------------------- PBO
    lines += ["## 3. Probability of backtest overfitting by CSCV (Bailey, Borwein, Lopez de Prado, Zhu 2015/2017)", "",
              "M = years x configurations matrix of out-of-sample $ (each configuration's walk-forward test-year "
              "totals). All C(S, S/2) halvings of the S row-blocks: pick the configuration with the best in-sample "
              "half, find its rank in the other half; PBO = share of halvings where that pick lands at or below the "
              "median (logit <= 0). Also: probability of loss = share of halvings where the pick loses money in the "
              "other half; degradation = slope of out-half on in-half performance of the pick.", ""]
    years12 = [str(y) for y in range(2013, 2025)]
    M, names = build_matrix(C, years12)
    incomplete = [k_ for k_ in C if k_ not in names and C[k_].reindex(years12).isna().any()]
    excluded = [k_ for k_ in C if k_ not in names and k_ not in incomplete]
    pres = []
    for label, Mx, nm, S_, metric in (
            ("main: 2013-2024, 12 one-year blocks, total $", M, names, 12, "sum"),
            ("2013-2024, 12 blocks, Sharpe of yearly $", M, names, 12, "sharpe"),
            ("2013-2024, 6 two-year blocks, total $", M, names, 6, "sum")):
        r = cpcv.pbo_cscv(Mx, S=S_, metric=metric)
        top = np.argsort(-r["chosen"])[:3]
        pres.append({"matrix": label, "configs": Mx.shape[1], "combinations": r["n_combos"], "PBO": r["pbo"],
                     "P(loss OOS)": r["prob_loss"], "degradation slope": r["degradation_slope"],
                     "most often picked": "; ".join(f"{nm[i]} ({r['chosen'][i]})" for i in top if r["chosen"][i])})
    y11 = [str(y) for y in range(2015, 2025)]
    M2, names2 = build_matrix(C, y11)
    if M2.shape[1] > M.shape[1]:
        r = cpcv.pbo_cscv(M2, S=10, metric="sum")
        top = np.argsort(-r["chosen"])[:3]
        pres.append({"matrix": "2015-2024 incl. configs starting 2014 (h1h2), 10 blocks, total $",
                     "configs": M2.shape[1], "combinations": r["n_combos"], "PBO": r["pbo"],
                     "P(loss OOS)": r["prob_loss"], "degradation slope": r["degradation_slope"],
                     "most often picked": "; ".join(f"{names2[i]} ({r['chosen'][i]})" for i in top if r["chosen"][i])})
    if len(daily) >= 2:
        Md = np.column_stack([v.to_numpy() for v in daily.values()])
        dn = list(daily)
        r = cpcv.pbo_cscv(Md, S=16, metric="sharpe")
        top = np.argsort(-r["chosen"])[:3]
        pres.append({"matrix": f"daily $ 2013-2025H1, 16 blocks, Sharpe ({len(dn)} configs with daily series)",
                     "configs": Md.shape[1], "combinations": r["n_combos"], "PBO": r["pbo"],
                     "P(loss OOS)": r["prob_loss"], "degradation slope": r["degradation_slope"],
                     "most often picked": "; ".join(f"{dn[i]} ({r['chosen'][i]})" for i in top if r["chosen"][i])})
    lines += [md_table(pd.DataFrame(pres), 3), "",
              f"Configurations in the main matrix ({len(names)}): " + "; ".join(names) + ".", "",
              "Approximations: (a) only configurations with out-of-sample results BY YEAR on file can enter M: "
              "entry NQ vote/logit/gbm (entry_folds.csv), the pooled models' NQ trades (oos_entry_pooled_*), the "
              "approach comparison (approach_folds_NQ_*), feature blocks and context rule walk-forwards (by-year rows),"
              " and h1h2 (from 2014, so only in the 2015-2024 matrix). The stop-option (9) and cost-ablation (7) "
              "trials saved only pooled numbers, and the two 2-fold timing tests cover 2013-2014 only: they are "
              "counted in N for the DSR but are not in M. "
              f"(b) Identical yearly series (the same configuration logged twice, or the same take-set) are kept once; "
              f"dropped as duplicates: {'; '.join(excluded) if excluded else 'none'}; missing some of 2013-2024: "
              f"{'; '.join(incomplete) if incomplete else 'none'}. (c) Rows are calendar years (synchronous across "
              "configurations, as CSCV requires), 2025H1 is left out so the 12 blocks are equal; with 12 rows the "
              "in/out halves are 6 years each, so PBO is coarse (924 halvings). (d) Configurations trade different "
              "event sets (e.g. stop options, H1/H2 triggers); CSCV only needs synchronous rows, not identical "
              "events.", ""]
    with open(MD, "w") as f:
        f.write("\n".join(lines) + "\n")
    say(f"wrote {MD}")
    print("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("stages", nargs="*", default=["cpcv", "stats"])
    ap.add_argument("--models", default="logit,gbm")
    a = ap.parse_args(argv)
    if "cpcv" in a.stages:
        stage_cpcv(a.models.split(","))
    if "stats" in a.stages:
        stage_stats()


if __name__ == "__main__":
    main()
