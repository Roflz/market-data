"""
Module 4 of the confidence study (SPEC.md): the integration run.

For each market (ES, NQ, YM) at tf minutes (v1: 15):
    features.build_features -> labels.entry_events + label_entries -> labels.exit_rows
    -> walkforward.walk_forward on the ENTRY events and on the EXIT rows (pooled over the markets with a `market`
       column, and per market), models vote / logit / gbm
    -> out/ datasets (parquet), result CSVs, weight tables + scorecards, permutation tests, the prop-firm simulation
       (prop_sim.simulate, LucidFlex 25K defaults) of the chosen entry rule's daily $, out/trials.csv and REPORT.md.

Stages (name any; default = all, in this order):
    python3 run_pipeline.py [data] [entry] [exit] [perm] [prop] [report] [--tf 15] [--scopes pooled,ES,NQ,YM]
                            [--models vote,logit,gbm] [--perm entry:pooled:logit,exit:pooled:logit]
    data    out/entries_<SYM>_<tf>.parquet, out/exits_<SYM>_<tf>.parquet (one per market). The locked holdout is cut
            off BEFORE anything is labelled: bars from 2025-06-30 18:00 ET on are dropped, so no holdout price is used.
    entry   walk-forwards on the entry events -> out/entry_results.csv (pooled OOS numbers, one row per scope x
            model), out/entry_folds.csv (fold by fold, with every baseline), out/entry_calibration.csv,
            out/coefs_entry_<scope>.csv, out/weights_entry_<scope>.csv, out/scorecard_entry_<scope>.csv,
            out/oos_entry_<scope>_<model>.parquet (one row per out-of-sample event: p, take, $, ...)
    exit    the same for the exit rows (out/exit_*.csv, ...) plus out/exit_by_src.csv (signal vs random entries)
    perm    permutation tests (y and its $ shuffled within each calendar year, the whole walk-forward refitted,
            20 shuffles, run in parallel processes) -> out/permutation.csv
    prop    daily $ (1 micro per trade) of the chosen entry rule's out-of-sample trades -> prop_sim.simulate with
            the LucidFlex 25K defaults: every-start-day pass odds on the real day order and on day-block bootstraps,
            next to taking every event, random skipping, and the other models -> out/prop_results.csv,
            out/prop_daily.csv
    report  REPORT.md from the CSVs (no refitting)

Conventions
  * Money: net $ per ONE micro contract (MES $5/pt, MNQ $2/pt, MYM $0.50/pt) after costs (signals.SPEC cost: $1.00
    commission + 1 tick slippage each way; + 1 extra tick on stop fills; labels.py), at the prices of the day.
  * Distances: R20 units = mean bar range of the 20 bars before the signal ("average bars").
  * The CHOSEN entry rule (declared before any full result was seen) is the pooled logit model: take an event when its
    p >= the fold's threshold. gbm / vote and the per-market models are reported next to it, not chosen from.
  * The LOCKED HOLDOUT (Globex sessions dated 2025-07-01 onward, first bar 2025-06-30 18:00 ET) is never labelled,
    fitted or evaluated here (walk_forward(final=False) refuses it and before_holdout() drops it again).
  * Every walk-forward run and permutation test is appended to out/trials.csv (the data-snooping count).

Additions to the SPEC feature list (all known at the close of the signal bar; stated in REPORT.md):
  * entries: stop_R20 = distance from the signal bar's close to the stop in R20 units (the size of the planned risk);
    cost_R = round-trip cost in units of that planned risk ($ cost / $ distance close -> stop). (The trade's real
    risk uses the NEXT bar's open, which is not known at the signal, so these use the signal bar's close.)
  * pooled runs: mkt_ES / mkt_NQ / mkt_YM one-hots (each market has its own base rate and cost per point), and the
    x_<SYM>_ columns of all three markets (a market's own x_ columns are NaN there and median-imputed / ignored).

Run: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 run_pipeline.py
"""
import argparse
import json
import multiprocessing as mp
import os
import time
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

import features as fe
import labels as lb
import signals as sg
import walkforward as wf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MARKETS = ("ES", "NQ", "YM")
MICRO = {s: sg.SPEC[s]["micro"] for s in MARKETS}
TF = 15
TARGET_R = (1.0, 1.5, 2.0)
PRIMARY_R = "1.5"
MAX_BARS_ENTRY = 16
MAX_BARS_EXIT = 32
EXIT_FRAC = 0.25
SEED = 0
MODELS = ("vote", "logit", "gbm")
SCOPES = ("pooled",) + MARKETS
CHOSEN = ("pooled", "logit")                  # the entry rule run through prop_sim (declared up front)
STATE_COLS = ["open_R", "mfe_R", "mae_R", "bars_held", "dist_stop_R", "mins_to_1645"]
ENTRY_EXTRA = ["stop_R20", "cost_R"]
N_PERM = 20
N_RANDOM = 200
WF_KW = dict(min_keep=0.05, n_random=N_RANDOM, seed=SEED)
PERM_DEFAULT = ("entry:pooled:logit", "exit:pooled:logit")
ERAS_OOS = {"2013-17": ("2013-01-01", "2017-12-31"), "2018-21": ("2018-01-01", "2021-12-31"),
            "2022-25H1": ("2022-01-01", "2025-06-30")}
BLOCKS = (5, 20)                               # day-block bootstrap block lengths (trading days)
N_BOOT = 200
N_SKIP_DRAWS = 100
ENTRY_META = ["t", "market", "session", "t_entry", f"t_end_{PRIMARY_R}", "patterns", f"exit_kind_{PRIMARY_R}",
              "risk_usd", "stop_R20", "cost_R"]
EXIT_META = ["t", "ts", "market", "src", "session", "hold_pnl_usd", "end_kind", "bars_held"]


def _say(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def _path(name):
    os.makedirs(OUT, exist_ok=True)
    return os.path.join(OUT, name)


def upsert(name, df, keys):
    """Write df to out/<name>, replacing the rows of an existing file whose `keys` values occur in df."""
    p = _path(name)
    if os.path.exists(p):
        old = pd.read_csv(p)
        if all(k in old.columns for k in keys) and len(old):
            new_keys = pd.MultiIndex.from_frame(df[keys].astype(str)).unique()
            hit = pd.MultiIndex.from_frame(old[keys].astype(str)).isin(new_keys)
            df = pd.concat([old.loc[~hit], df], ignore_index=True)
    df.to_csv(p, index=False)


TRIAL_COLS = ["date", "module", "scope", "model", "target", "n_folds", "oos_rows", "oos_auc", "oos_kept",
              "oos_keep_share", "oos_usd_total", "oos_usd_per_trade", "oos_usd_per_year", "baseline_usd_per_trade",
              "runtime_s", "parameters", "note"]


def log_trial(**row):
    """Append one configuration to out/trials.csv (date, module, parameters, OOS result) - the data-snooping log."""
    p = _path("trials.csv")
    row.setdefault("date", f"{datetime.now():%Y-%m-%d %H:%M}")
    pd.DataFrame([{c: row.get(c, "") for c in TRIAL_COLS}]).to_csv(p, mode="a", header=not os.path.exists(p),
                                                                   index=False)


# ============================================================================================ stage 1: datasets
def holdout_cut(b, F):
    """Drop every bar at/after the locked holdout's first bar (2025-06-30 18:00 ET) from b and F. Features use only
    the past, so the remaining rows equal the full-history ones; labels then never touch holdout prices (a label never
    crosses a session: the last one ends by 2025-06-30 16:45)."""
    keep = b.index < wf.HOLDOUT_SESSION_START
    return b.loc[keep], F.loc[keep]


def patterns_from_F(F):
    """signals.patterns values back from F's pat_ columns (exact: F stores the int8 values as float32)."""
    return pd.DataFrame({p: F[f"pat_{p}"].to_numpy().astype(np.int8) for p in fe.DIRECTIONAL + fe.NEUTRAL},
                        index=F.index)


def entry_trade_features(b, ev, sym):
    """(stop_R20, cost_R) per event, from the signal bar's close C_t and R20_t (both known at t's close):
    stop_R20 = d * (C_t - stop) / R20 (clipped to [0, 50]); cost_R = cost $ / (d * (C_t - stop) * $ per point)."""
    i = ev["i"].to_numpy(np.int64)
    d = ev["d"].to_numpy(np.float64)
    C = b["C"].to_numpy(np.float64)[i]
    R = b["R20"].to_numpy(np.float64)[i]
    dist = d * (C - ev["stop"].to_numpy(np.float64))               # >= 1 tick (stop beyond the pattern's extreme)
    spec = sg.SPEC[sym]
    with np.errstate(divide="ignore", invalid="ignore"):
        stop_r20 = np.clip(dist / R, 0.0, fe.CLIP_R20)
        cost_r = np.where(dist > 0, spec["cost"] / (np.maximum(dist, spec["tick"]) * spec["usd"]), np.nan)
    return stop_r20.astype(np.float32), cost_r.astype(np.float32)


def add_cost_bar(df):
    """cost_bar = round-trip cost $ / (R20 x $ per point): what costs take out of an average bar of that market at
    that time (known at the signal bar's close). MNQ 15-min 2024 ~0.05, MES/MYM ~0.15, 2010-2015 ~0.4-0.5.
    Not in ENTRY_EXTRA (keeps v1 reproducible): add it explicitly to the feature list where wanted."""
    usd = df["market"].map({s: sg.SPEC[s]["usd"] for s in sg.SPEC}).to_numpy(np.float64)
    cost = df["market"].map({s: sg.SPEC[s]["cost"] for s in sg.SPEC}).to_numpy(np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        df["cost_bar"] = np.where(df["R20"].to_numpy(np.float64) > 0,
                                  cost / (df["R20"].to_numpy(np.float64) * usd), np.nan).astype(np.float32)
    return df


def build_entries(sym, tf, others=MARKETS):
    """Entry dataset only (no exit rows) of one market at timeframe tf - same steps as build_market."""
    t0 = time.time()
    b, F = fe.build_features(sym, tf, others=others)
    b, F = holdout_cut(b, F)
    ev = lb.entry_events(b, patterns_from_F(F), tf=tf, sym=sym)
    m1 = lb.load_1m(sym)
    m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
    lab = lb.label_entries(sym, tf, b, ev, target_R=TARGET_R, max_bars=MAX_BARS_ENTRY, m1=m1)
    lab["patterns"] = lab["patterns"].map("|".join)
    lab["session"] = wf.session_label(lab["t"])
    lab["R20"] = b["R20"].to_numpy(np.float64)[lab["i"].to_numpy()]
    lab["stop_R20"], lab["cost_R"] = entry_trade_features(b, lab, sym)
    Fi = F.iloc[lab["i"].to_numpy()].reset_index(drop=True)
    lab = pd.concat([lab.reset_index(drop=True), Fi], axis=1)
    _say(f"{sym} {tf}m: {len(b):,} bars, {len(lab):,} labelled entries ({time.time() - t0:.0f}s)")
    return lab


def build_market(sym, tf=TF, others=MARKETS, exit_frac=EXIT_FRAC, seed=SEED):
    """Entry and exit datasets of one market (both cut before the locked holdout).
    entries: labels.label_entries output (t, i, d, patterns as 'a|b' text, n_patterns, stop, market, t_entry, entry,
             risk_pts, risk_usd, past_stop, per target R: target/exit_px/pnl_usd/y/exit_kind/t_end) + session
             + R20 + stop_R20 + cost_R + every F column at the signal bar.
    exits:   labels.exit_rows output (trade, market, src, t, k, ts, d, F at bar k, trade state, exit_gain_usd,
             y_exit, hold_pnl_usd, end_kind, t_end) + session. The random entries use a different seed per market
             (the same seed would put ES and NQ random trades on the same bars and directions)."""
    t0 = time.time()
    b, F = fe.build_features(sym, tf, others=others)
    b, F = holdout_cut(b, F)
    ev = lb.entry_events(b, patterns_from_F(F), tf=tf, sym=sym)
    _say(f"{sym}: {len(b):,} bars, {len(ev):,} entry events ({time.time() - t0:.0f}s)")
    m1 = lb.load_1m(sym)
    m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
    lab = lb.label_entries(sym, tf, b, ev, target_R=TARGET_R, max_bars=MAX_BARS_ENTRY, m1=m1)
    lab["patterns"] = lab["patterns"].map("|".join)
    lab["session"] = wf.session_label(lab["t"])
    lab["R20"] = b["R20"].to_numpy(np.float64)[lab["i"].to_numpy()]
    lab["stop_R20"], lab["cost_R"] = entry_trade_features(b, lab, sym)
    Fi = F.iloc[lab["i"].to_numpy()].reset_index(drop=True)
    lab = pd.concat([lab.reset_index(drop=True), Fi], axis=1)
    _say(f"{sym}: {len(lab):,} labelled entries ({time.time() - t0:.0f}s)")
    mseed = seed + 1000 * (MARKETS.index(sym) + 1) if sym in MARKETS else seed
    ex = lb.exit_rows(sym, tf, b, F, ev, max_bars=MAX_BARS_EXIT, frac=exit_frac, seed=mseed, m1=m1)
    ex["session"] = wf.session_label(ex["t"])
    _say(f"{sym}: {len(ex):,} exit rows from {ex.trade.nunique():,} trades ({time.time() - t0:.0f}s)")
    return lab, ex


def stage_data(tf=TF, markets=MARKETS):
    for sym in markets:
        lab, ex = build_market(sym, tf)
        lab.to_parquet(_path(f"entries_{sym}_{tf}.parquet"), compression="zstd")
        ex.to_parquet(_path(f"exits_{sym}_{tf}.parquet"), compression="zstd")
        del lab, ex
        fe.clear_cache()


# ============================================================================================ loading
def feature_list(kind, scope):
    """Model inputs: F's columns (per market: its own x_ columns of the two others; pooled: all three markets'),
    + stop_R20, cost_R (entries) or the trade state (exits), + mkt_ one-hots (pooled)."""
    base = fe.COLUMNS(None if scope == "pooled" else scope, MARKETS)
    extra = ENTRY_EXTRA if kind == "entry" else STATE_COLS
    mk = [f"mkt_{s}" for s in MARKETS] if scope == "pooled" else []
    return base + extra + mk


def load(kind, scope, tf=TF, columns=None):
    """Dataset of one scope ('pooled' = ES + NQ + YM stacked, RangeIndex)."""
    syms = MARKETS if scope == "pooled" else (scope,)
    name = "entries" if kind == "entry" else "exits"
    parts = [pd.read_parquet(_path(f"{name}_{s}_{tf}.parquet"), columns=columns) for s in syms]
    df = pd.concat(parts, ignore_index=True) if len(parts) > 1 else parts[0]
    if scope == "pooled" and (columns is None or "market" in columns):
        for s in MARKETS:
            df[f"mkt_{s}"] = (df["market"] == s).astype(np.float32)
    return df


def wf_args(kind):
    if kind == "entry":
        return dict(kind="entry", label=f"y_{PRIMARY_R}", pnl=f"pnl_usd_{PRIMARY_R}", t_end=f"t_end_{PRIMARY_R}")
    return dict(kind="exit", label="y_exit", pnl="exit_gain_usd", t_end="t_end")


def _params(kind, scope, model, feats, tf):
    p = dict(tf=tf, scope=scope, model=model, n_features=len(feats), min_keep=WF_KW["min_keep"],
             min_train_years=3, purge_days=1, n_random=N_RANDOM, seed=SEED, folds="2013..2024 + 2025H1")
    p.update(wf_args(kind))
    if model == "logit":
        p["C_grid"] = list(wf.C_GRID)
    if model == "gbm":
        p["gbm"] = {k: v for k, v in wf.GBM_PARAMS.items()}
    if kind == "entry":
        p.update(target_R=list(TARGET_R), max_bars=MAX_BARS_ENTRY, extra=ENTRY_EXTRA)
    else:
        p.update(max_bars=MAX_BARS_EXIT, exit_frac=EXIT_FRAC, state=STATE_COLS)
    return json.dumps(p)


# ============================================================================================ stage 2/3: walk-forward
def run_walkforward(kind, scope, model, data, tf=TF):
    """One walk-forward (all folds) + everything saved: fold rows, pooled row, calibration, OOS rows, logit weights
    and scorecard, one trials.csv row. Returns the WalkForwardResult."""
    feats = feature_list(kind, scope)
    missing = [c for c in feats if c not in data.columns]
    if missing:
        raise KeyError(f"{kind}/{scope}: missing feature columns {missing}")
    t0 = time.time()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = wf.walk_forward(data, feats, model=model, verbose=True, **wf_args(kind), **WF_KW)
    n_conv = sum("converge" in str(w.message).lower() for w in caught)
    rt = time.time() - t0
    key = dict(scope=scope, model=model)
    F = res.folds.copy()
    F.insert(0, "model", model); F.insert(0, "scope", scope)
    upsert(f"{kind}_folds.csv", F, ["scope", "model"])
    P = res.pooled.to_frame().T
    P.insert(0, "model", model); P.insert(0, "scope", scope)
    P["runtime_s"] = round(rt, 1)
    P["convergence_warnings"] = n_conv
    P["skipped"] = "; ".join(f"{a}: {b}" for a, b in res.skipped)
    upsert(f"{kind}_results.csv", P, ["scope", "model"])
    C = res.calibration.copy()
    C.insert(0, "model", model); C.insert(0, "scope", scope)
    upsert(f"{kind}_calibration.csv", C, ["scope", "model"])
    meta = [c for c in (ENTRY_META if kind == "entry" else EXIT_META) if c in data.columns]
    o = res.oos.join(data.loc[res.oos.index, meta])
    o.reset_index(names="row").to_parquet(_path(f"oos_{kind}_{scope}_{model}.parquet"), compression="zstd")
    if model == "logit" and len(res.coefs):
        res.coefs.to_csv(_path(f"coefs_{kind}_{scope}.csv"), index=False)
        wt = wf.weight_table(res.coefs)
        wt.to_csv(_path(f"weights_{kind}_{scope}.csv"), index=False)
        scorecard_table(wt, kind).to_csv(_path(f"scorecard_{kind}_{scope}.csv"), index=False)
    if kind == "exit":
        upsert("exit_by_src.csv", exit_by_src(res, data).assign(**key), ["scope", "model"])
    s = res.pooled
    if kind == "entry":
        log_trial(module="entry", scope=scope, model=model, target=f"y_{PRIMARY_R}", n_folds=int(s.n_folds),
                  oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                  oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                  oos_usd_per_trade=round(float(s.pnl_per_trade), 3), oos_usd_per_year=round(float(s.usd_per_year), 1),
                  baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(rt),
                  parameters=_params(kind, scope, model, feats, tf), note="baseline = all events")
    else:
        log_trial(module="exit", scope=scope, model=model, target="y_exit", n_folds=int(s.n_folds),
                  oos_rows=len(res.oos), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_trades),
                  oos_keep_share=round(float(s.learned_exit_share), 4),
                  oos_usd_total=round(float(s.learned_gain * s.n_trades), 2),
                  oos_usd_per_trade=round(float(s.learned_gain), 3),
                  oos_usd_per_year=round(float(s.learned_gain_per_year), 1),
                  baseline_usd_per_trade=round(float(s.random_gain), 3), runtime_s=round(rt),
                  parameters=_params(kind, scope, model, feats, tf),
                  note="$ = gain vs holding per trade (kept = trades, keep_share = exited early); baseline = random-"
                       "time exit")
    _say(f"{kind} {scope} {model}: done in {rt:.0f}s  " + _short(kind, s))
    return res


def _short(kind, s):
    if kind == "entry":
        return (f"AUC {s.auc:.3f}, kept {int(s.n_kept):,} ({s.keep_share:.1%}), {s.pnl_per_trade:+.2f} $/trade, "
                f"{s.usd_per_year:+,.0f} $/yr; all {s.all_pnl_per_trade:+.2f}, random {s.random_pnl_per_trade:+.2f}")
    return (f"AUC {s.auc:.3f}, exit share {s.learned_exit_share:.1%}, gain {s.learned_gain:+.3f} $/trade vs hold; "
            f"random {s.random_gain:+.3f}, opp {s.opp_gain:+.3f}; net learned {s.get('learned_net', np.nan):+.2f} vs "
            f"hold {s.get('hold_net', np.nan):+.2f}")


def exit_by_src(res, data, n_random=N_RANDOM, seed=SEED):
    """Exit policies on the OOS trades split by how the trade was entered (src: 'signal' = a pattern entry,
    'random' = a random entry), with the fold's own threshold. Same numbers as walkforward's exit evaluation."""
    o = res.oos
    src = data.loc[o.index, "src"].to_numpy()
    hold = data.loc[o.index, "hold_pnl_usd"].to_numpy(np.float64)
    thr = res.folds.set_index("fold").threshold
    rng = np.random.default_rng(seed)
    rows = []
    for s in ("signal", "random", "all"):
        m = np.ones(len(o), bool) if s == "all" else src == s
        tot = dict(n=0, learned=0.0, opp=0.0, hold=0.0, ex=0.0, exo=0.0, rand=np.zeros(n_random))
        for f, idx in pd.Series(np.flatnonzero(m)).groupby(o.fold.to_numpy()[m], sort=False):
            g = o.iloc[idx.to_numpy()]
            codes = pd.factorize(g.trade)[0]
            st = wf.group_starts(codes)
            ev = wf.evaluate_exit_policies(g.p.to_numpy(), thr[f], g.pnl.to_numpy(), codes, g.opp.to_numpy(),
                                           hold[idx.to_numpy()][st], n_random, rng)
            n = ev["n_trades"]
            tot["n"] += n
            tot["learned"] += ev["_g_learned"].sum(); tot["opp"] += ev["_g_opp"].sum()
            tot["hold"] += ev["hold_net"] * n; tot["rand"] += ev["_g_random_tot"]
            tot["ex"] += ev["learned_exit_share"] * n; tot["exo"] += ev["opp_exit_share"] * n
        n = max(tot["n"], 1)
        rows.append(dict(src=s, n_trades=tot["n"], hold_net=tot["hold"] / n, learned_exit_share=tot["ex"] / n,
                         learned_gain=tot["learned"] / n, learned_net=(tot["hold"] + tot["learned"]) / n,
                         opp_exit_share=tot["exo"] / n, opp_gain=tot["opp"] / n,
                         random_gain=tot["rand"].mean() / n, random_p5=np.quantile(tot["rand"], 0.05) / n,
                         random_p95=np.quantile(tot["rand"], 0.95) / n))
    return pd.DataFrame(rows)


def stage_walkforward(kind, tf=TF, scopes=SCOPES, models=MODELS):
    for scope in scopes:
        data = load(kind, scope, tf)
        _say(f"{kind} {scope}: {len(data):,} rows")
        for model in models:
            run_walkforward(kind, scope, model, data, tf)
        del data


# ============================================================================================ stage 4: permutation
_PERM = {}


def _perm_worker(i):
    """One permutation run in a forked worker (i = -1: the real, unshuffled run). Returns (i, OOS score)."""
    from threadpoolctl import threadpool_limits                   # noqa: PLC0415
    data, feats, kw = _PERM["data"], _PERM["feats"], _PERM["kw"]
    rng = None if i < 0 else np.random.default_rng([_PERM["seed"], i])
    with threadpool_limits(limits=_PERM["threads"]), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = wf.walk_forward(data, feats, shuffle_rng=rng, baselines=False, **kw)
    return i, wf._oos_score(res)


def permutation(kind, scope, model, tf=TF, n_perm=N_PERM, workers=4, seed=SEED):
    """walkforward.permutation_test's procedure with the shuffles run in parallel processes: y and its $ shuffled
    jointly within each calendar year (fitting and threshold choice only; test metrics use the true outcomes), the
    whole walk-forward refitted, the OOS score kept (entries: pooled total $ of the taken trades; exits: $ gain vs hold
    per trade of the learned exit). p = (1 + #shuffles >= real or NaN) / (1 + n_perm)."""
    data = load(kind, scope, tf)
    feats = feature_list(kind, scope)
    _PERM.update(data=data, feats=feats, kw=dict(model=model, **wf_args(kind), **WF_KW), seed=seed,
                 threads=max(1, 12 // workers))
    t0 = time.time()
    with mp.get_context("fork").Pool(workers) as pool:            # fork: workers share `data` copy-on-write
        out = dict(pool.imap_unordered(_perm_worker, [-1] + list(range(n_perm))))
    _PERM.clear()
    real = out.pop(-1)
    perm = np.array([out[i] for i in range(n_perm)], np.float64)
    fin = np.isfinite(perm)
    pv = (1 + np.sum(~fin | (perm >= real))) / (1 + n_perm) if np.isfinite(real) else np.nan
    r = dict(kind=kind, scope=scope, model=model, score="total OOS $ of taken trades" if kind == "entry"
             else "OOS $ gain vs hold per trade", real=real, p_value=pv, n_perm=n_perm, n_valid=int(fin.sum()),
             perm_mean=float(perm[fin].mean()) if fin.any() else np.nan,
             perm_p5=float(np.quantile(perm[fin], 0.05)) if fin.any() else np.nan,
             perm_p95=float(np.quantile(perm[fin], 0.95)) if fin.any() else np.nan,
             perm_max=float(perm[fin].max()) if fin.any() else np.nan, perm_values=json.dumps(np.round(perm, 3).tolist()),
             runtime_s=round(time.time() - t0))
    log_trial(module="perm", scope=scope, model=model, target=wf_args(kind)["label"], oos_usd_total=round(real, 3),
              runtime_s=r["runtime_s"], parameters=json.dumps(dict(kind=kind, n_perm=n_perm, seed=seed)),
              note=f"permutation test p = {pv:.3f}; shuffle mean {r['perm_mean']:.2f}, 95% {r['perm_p95']:.2f} "
                   "(refits of the same configuration, not new configurations)")
    _say(f"perm {kind} {scope} {model}: real {real:.2f}, shuffles mean {r['perm_mean']:.2f} p95 {r['perm_p95']:.2f}, "
         f"p = {pv:.3f} ({r['runtime_s']}s)")
    return r


def stage_perm(tf=TF, which=PERM_DEFAULT, n_perm=N_PERM, workers=None):
    """Permutation tests of the given kind:scope:model runs. workers: parallel processes (default 4 for entries,
    2 for exits: a pooled exit walk-forward needs ~7 GB)."""
    for spec in which:
        kind, scope, model = spec.split(":")
        nw = workers or (4 if kind == "entry" else 2)
        r = permutation(kind, scope, model, tf, n_perm, nw)
        upsert("permutation.csv", pd.DataFrame([r]), ["kind", "scope", "model"])


# ============================================================================================ stage 5: prop sim
def _ns(x):
    return pd.DatetimeIndex(x).as_unit("ns").asi8


def concurrency(t_entry, t_end):
    """(max, 95th percentile over days of the daily max) number of trades open at the same time."""
    s, e = _ns(t_entry), _ns(t_end)
    if not len(s):
        return 0, 0.0
    tm = np.r_[s, e]
    dl = np.r_[np.ones(len(s)), -np.ones(len(e))]
    o = np.lexsort((dl, tm))                                      # at equal times, exits (-1) before entries
    c = np.cumsum(dl[o])
    day = wf.session_label(pd.DatetimeIndex(tm[o]))
    dmax = pd.Series(c).groupby(day.to_numpy()).max()
    return int(c.max()), float(np.quantile(dmax, 0.95))


def _simulate(v, dates, rules, eras=ERAS_OOS):
    import prop_sim as ps                                         # noqa: PLC0415
    return ps.simulate(pd.Series(v, index=dates), rules, start_from=dates[0], eras=eras, outcomes=False)


def block_bootstrap_pass(v, dates, rules, block, n_boot=N_BOOT, seed=SEED):
    """Pass odds on day-block bootstraps: n_boot synthetic histories of len(v) trading days, each made of randomly
    chosen runs of `block` CONSECUTIVE days of the real series (circular), so streaks of losing days stay together
    (shuffling single trades or days would break them up and overstate the pass odds). Each history is simulated
    with an account started on every day. Returns the array of pass rates (NaN when no account finished)."""
    rng = np.random.default_rng([seed, block])
    v = np.asarray(v, np.float64)
    n = len(v)
    nb = -(-n // block)
    out = np.empty(n_boot)
    for k in range(n_boot):                                       # 200 draws, each simulated vectorized
        st = rng.integers(0, n, nb)
        idx = ((st[:, None] + np.arange(block)[None, :]) % n).ravel()[:n]
        out[k] = _simulate(v[idx], dates, rules, eras=None)["pass_rate"]
    return out


def _prop_row(rule, view, v, dates, n_tr, rules, extra=None):
    import prop_sim as ps                                         # noqa: PLC0415
    r = _simulate(v, dates, rules)
    st = ps.series_stats(dates, np.asarray(v, np.float64), np.asarray(n_tr, np.float64))
    row = dict(rule=rule, view=view, pass_rate=r["pass_rate"], fail_rate=r["fail_rate"],
               open_share=r["open_share"], n_starts=r["n_starts"], days_pass_median=r["days_pass"][1],
               days_fail_median=r["days_fail"][1], net_yr=st["net_yr"], trades_yr=st["trades_yr"],
               day_mean=st["day_mean"], day_sd=st["day_sd"], worst_day=st["worst_day"], best_day=st["best_day"],
               max_dd=st["max_dd"])
    for name, e in r["eras"].items():
        row[f"pass_{name}"] = e["pass_rate"]
    row.update(extra or {})
    return row


def stage_prop(tf=TF):
    """Daily $ at 1 micro per trade of the chosen entry rule's OOS trades (and of the comparison rules) through
    prop_sim.simulate (LucidFlex 25K defaults), on the real order of days and on day-block bootstraps."""
    import prop_sim as ps                                         # noqa: PLC0415
    rules = ps.Rules()
    scope, model = CHOSEN
    oos = pd.read_parquet(_path(f"oos_entry_{scope}_{model}.parquet"))
    sess = pd.DatetimeIndex(oos["session"])
    cal = pd.DatetimeIndex(np.unique(sess.to_numpy()))           # every Globex session with an OOS event
    code = cal.get_indexer(sess)
    pnl = oos["pnl"].to_numpy(np.float64)
    nd = len(cal)

    def daily(mask):
        return (np.bincount(code[mask], weights=pnl[mask], minlength=nd),
                np.bincount(code[mask], minlength=nd).astype(np.float64))

    rows, daily_out = [], {"date": cal}
    rules_to_run = [(f"{scope} {model} (chosen)", oos["take"].to_numpy(bool), oos)]
    for m in MODELS:
        if m != model and os.path.exists(_path(f"oos_entry_{scope}_{m}.parquet")):
            o2 = pd.read_parquet(_path(f"oos_entry_{scope}_{m}.parquet"))
            if len(o2) == len(oos) and np.array_equal(o2["row"].to_numpy(), oos["row"].to_numpy()):
                rules_to_run.append((f"{scope} {m}", o2["take"].to_numpy(bool), o2))
    rules_to_run.append(("all events", np.ones(len(oos), bool), oos))
    t_end_col = f"t_end_{PRIMARY_R}"
    for name, take, o in rules_to_run:
        v, n = daily(take)
        mx, p95 = concurrency(o.loc[take, "t_entry"], o.loc[take, t_end_col])
        extra = dict(n_trades=int(take.sum()), usd_per_trade=float(pnl[take].mean()) if take.any() else np.nan,
                     max_open=mx, p95_daily_max_open=p95)
        rows.append(_prop_row(name, "history", v, cal, n, rules, extra))
        for blk in BLOCKS:
            pr = block_bootstrap_pass(v, cal, rules, blk)
            rows.append(dict(rule=name, view=f"day-block {blk}", pass_rate=float(np.nanmedian(pr)),
                             pass_p5=float(np.nanquantile(pr, 0.05)), pass_p95=float(np.nanquantile(pr, 0.95)),
                             n_boot=N_BOOT, **extra))
        daily_out[f"{name} $"] = v
        daily_out[f"{name} trades"] = n
        _say(f"prop {name}: history pass {rows[-1 - len(BLOCKS)]['pass_rate']:.1%}, "
             f"net/yr {rows[-1 - len(BLOCKS)]['net_yr']:+,.0f}, block-20 median {rows[-1]['pass_rate']:.1%}")
    # random skip: the chosen rule's number of trades per fold, drawn at random from the fold's events
    take = oos["take"].to_numpy(bool)
    fold = oos["fold"].to_numpy()
    rng = np.random.default_rng(SEED)
    groups = [(np.flatnonzero(fold == f), int(take[fold == f].sum())) for f in pd.unique(fold)]
    pr_hist, pr_blk, nets = [], [], []
    for k in range(N_SKIP_DRAWS):                                 # 100 draws
        m = np.zeros(len(oos), bool)
        for idx, nt in groups:
            if nt:
                m[rng.choice(idx, nt, replace=False)] = True
        v, n = daily(m)
        r = _simulate(v, cal, rules)
        pr_hist.append(r["pass_rate"])
        nets.append(v.sum() / ((cal[-1] - cal[0]).days / 365.25))
        if k < 20:                                                # 20 draws x 50 bootstraps for the block view
            pr_blk.extend(block_bootstrap_pass(v, cal, rules, 20, n_boot=50, seed=SEED + k))
    pr_hist, pr_blk = np.array(pr_hist), np.array(pr_blk)
    extra = dict(n_trades=int(take.sum()), n_draws=N_SKIP_DRAWS)
    rows.append(dict(rule="random skip (same count per fold)", view="history", pass_rate=float(np.nanmean(pr_hist)),
                     pass_p5=float(np.nanquantile(pr_hist, 0.05)), pass_p95=float(np.nanquantile(pr_hist, 0.95)),
                     net_yr=float(np.mean(nets)), **extra))
    rows.append(dict(rule="random skip (same count per fold)", view="day-block 20", pass_rate=float(np.nanmedian(pr_blk)),
                     pass_p5=float(np.nanquantile(pr_blk, 0.05)), pass_p95=float(np.nanquantile(pr_blk, 0.95)),
                     n_boot=len(pr_blk), **extra))
    _say(f"prop random skip: history pass mean {np.nanmean(pr_hist):.1%}, net/yr {np.mean(nets):+,.0f}")
    pd.DataFrame(rows).to_csv(_path("prop_results.csv"), index=False)
    pd.DataFrame(daily_out).to_csv(_path("prop_daily.csv"), index=False)
    log_trial(module="prop", scope=scope, model=model, target=f"y_{PRIMARY_R}",
              oos_usd_per_year=round(rows[0]["net_yr"], 1), parameters=json.dumps(dict(
                  rules="LucidFlex 25K defaults (prop_sim.Rules())", blocks=list(BLOCKS), n_boot=N_BOOT,
                  micros_per_trade=1)),
              note=f"prop_sim pass rate (history) {rows[0]['pass_rate']:.3f}; not a new model configuration")


# ============================================================================================ scorecard words
TOD_WORDS = {"asia": "Asia hours (18:00-02:00 ET)", "europe": "Europe hours (02:00-08:00 ET)",
             "uspre": "US pre-market (08:00-09:30 ET)", "open": "the US open hour (09:30-10:30 ET)",
             "midday": "US midday (10:30-15:00 ET)", "close": "the US close (15:00-16:45 ET)"}
DOW_WORDS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
UNIT_SCALE = {"mins_to_1645": 60.0}                              # scorecard unit: per hour instead of per minute


def unit_words(f):
    """What 'one unit' of a feature is, in a trader's words (the scorecard's points are per this unit)."""
    if f.startswith(("pat_", "fam_")):
        return "per firing (+1 with / -1 against)" if f in fe.SIGNED else "when present"
    if f.startswith(("tod_", "dow_", "mkt_")) or f.startswith("atfib"):
        return "when true"
    if f.startswith(("brk_", "mom_x100", "struct_", "h1_struct")) or f.endswith("ema_stack"):
        return "per +1 (with the trade)"
    if f.startswith("fibpos"):
        return "per whole swing leg"
    if f == "cost_R":
        return "per 1R of cost"
    if f.endswith("_R"):
        return "per 1R"
    if f.startswith(("dist_", "ema20_slope", "gap_open", "day_ret", "stop_R20")) or \
            (f.startswith("x_") and f.endswith("_ret")):
        return "per average bar"
    if f in ("rng_rel",):
        return "per 1 average bar of range"
    if f in ("vol_rel", "day_range_rel"):
        return "per 1x the average"
    if f in ("mom", "h1_mom", "mom_slope3"):
        return "per 1% move"
    if f in ("body_frac",):
        return "from 0 (no body) to 1 (all body)"
    if f in ("clv", "above_ema20_share"):
        return "per 1 on a -1..+1 scale"
    if f == "bars_held":
        return "per bar held"
    if f == "mins_to_1645":
        return "per hour left"
    return "per unit"


def meaning(f):
    """Plain-English meaning of a model input (all signed inputs are seen from the trade: + = in the trade's
    direction)."""
    if f == "(intercept)":
        return "base score"
    if f.startswith("pat_"):
        p = f[4:]
        nm = p.replace("_", " ")
        if p in fe.NEUTRAL:
            return f"the signal bar is a {nm} (no direction)"
        return f"{nm} fired on the signal bar in the trade's direction (+1) or against it (-1)"
    if f.startswith("fam_"):
        return f"any {f[4:]}-type pattern fired with the trade (+1) or against it (-1)"
    if f.startswith(("dist_swhi_", "dist_swlo_")):
        k = f.rsplit("_", 1)[1]
        if f.startswith("dist_swhi"):
            return (f"how far price is beyond the last {k}-bar swing on the PROFIT side (long: swing high, short: "
                    "swing low); negative = that swing is still ahead")
        return (f"how far price is from the last {k}-bar swing on the STOP side (long: swing low, short: swing "
                "high); positive = that many average bars of room")
    if f.startswith("brk_"):
        return f"this bar is the first close through the last {f[4:]}-bar swing, in the trade's direction"
    if f.startswith("struct_"):
        return f"{f[7:]}-bar swings: higher highs AND higher lows in the trade's direction (+1), opposite (-1)"
    if f.startswith("fibpos_"):
        return (f"where price sits inside the last {f[7:]}-bar swing leg (0 = leg start, 1 = leg end), "
                "positive when the leg runs in the trade's direction")
    if f.startswith("atfib_"):
        return f"price is at a 38.2/50/61.8% retracement of the last {f[6:]}-bar swing leg"
    words = {
        "ema_stack": "EMA 8/20/50 stacked in the trade's direction (+1) or against (-1)",
        "ema20_slope": "slope of the 20-bar EMA over 10 bars, in the trade's direction",
        "dist_ema8": "price beyond the 8-bar EMA in the trade's direction",
        "dist_ema20": "price beyond the 20-bar EMA in the trade's direction",
        "dist_ema50": "price beyond the 50-bar EMA in the trade's direction",
        "above_ema20_share": "share of the last 20 closes on the trade's side of the 20-bar EMA",
        "mom": "14-bar momentum (% move over 14 bars) in the trade's direction",
        "mom_slope3": "change of 14-bar momentum over the last 3 bars, in the trade's direction",
        "mom_x100": "14-bar momentum just turned in the trade's direction (crossed zero)",
        "dist_vwap": "price beyond the session VWAP in the trade's direction",
        "rng_rel": "signal bar's range compared with the average bar",
        "body_frac": "signal bar's body as a share of its range",
        "clv": "where the signal bar closed in its range (+1 = at the trade's end of the bar)",
        "vol_rel": "signal bar's volume compared with the 20-bar average",
        "gap_open": "today's opening gap, in the trade's direction",
        "day_range_rel": "today's range so far compared with an average day's full range",
        "day_ret": "move since today's session open, in the trade's direction",
        "h1_ema_stack": "60-minute EMA 8/20/50 stacked in the trade's direction",
        "h1_mom": "60-minute 14-bar momentum in the trade's direction",
        "h1_struct_5": "60-minute swing structure in the trade's direction",
        "stop_R20": "stop distance from the signal close (size of the risk)",
        "cost_R": "round-trip cost as a share of the planned risk (close to stop)",
        "open_R": "open profit now, in R (1R = the initial risk)",
        "mfe_R": "best open profit so far, in R",
        "mae_R": "worst open loss so far, in R",
        "bars_held": "15-minute bars held so far",
        "dist_stop_R": "distance from price to the stop, in R",
        "mins_to_1645": "time left until the 16:45 flat time",
    }
    if f in words:
        return words[f]
    if f.startswith("tod_"):
        return f"signal bar is in {TOD_WORDS.get(f[4:], f[4:])}"
    if f.startswith("dow_"):
        return f"session is a {DOW_WORDS[int(f[4:])]}"
    if f.startswith("mkt_"):
        return f"the trade is in {MICRO.get(f[4:], f[4:])}"
    if f.startswith("x_") and f.endswith("_ret"):
        m = f.split("_")[1]
        return f"{m}'s same 15-minute bar (close minus open) in the trade's direction, in {m}'s average bars"
    if f.startswith("x_") and f.endswith("_ema_stack"):
        return f"{f.split('_')[1]}'s EMA 8/20/50 stack in the trade's direction"
    return f


def scorecard_table(wt, kind):
    """Scorecard from walkforward.weight_table: points per unit of the median (over folds) raw logit coefficient
    (+20 points doubles the odds), points per 1 standard deviation (comparable across features), sign stability,
    unit and meaning. Sorted by |points per unit| (then |points per SD|); the intercept is last."""
    df = wt[["feature", "coef_raw_median", "coef_std_median", "sign_stability", "share_pos", "n_folds"]].copy()
    scale = df.feature.map(UNIT_SCALE).fillna(1.0).to_numpy()
    df["points"] = wf.points(df.coef_raw_median.to_numpy() * scale)
    df["points_1sd"] = wf.points(df.coef_std_median.to_numpy())
    df["unit"] = [unit_words(f) for f in df.feature]
    df["meaning"] = [meaning(f) for f in df.feature]
    icpt = df.feature == "(intercept)"
    df["_k1"] = -np.abs(df.points); df["_k2"] = -np.abs(df.points_1sd); df["_k0"] = icpt.astype(int)
    df = df.sort_values(["_k0", "_k1", "_k2"], kind="stable").drop(columns=["_k0", "_k1", "_k2"])
    df.attrs["kind"] = kind
    return df.reset_index(drop=True)


# ============================================================================================ stage 6: report
def md_table(df, fmt=None, align=None):
    """Markdown table of df; fmt = {column: format function or format spec}."""
    fmt = fmt or {}
    cols = list(df.columns)

    def cell(c, v):
        if c in fmt:
            f = fmt[c]
            try:
                return f(v) if callable(f) else ("" if pd.isna(v) else format(v, f))
            except (TypeError, ValueError):
                return str(v)
        if isinstance(v, float):
            return "" if np.isnan(v) else f"{v:,.2f}"
        return "" if v is None or (isinstance(v, float) and np.isnan(v)) else str(v)

    al = align or ["---:" if pd.api.types.is_numeric_dtype(df[c]) else "---" for c in cols]
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join(al) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(cell(c, r[c]) for c in cols) + " |")
    return "\n".join(lines)


def usd(v, d=2):
    return "" if v is None or pd.isna(v) else f"{'-' if v < 0 else '+'}${abs(v):,.{d}f}"


def usd0(v):
    return usd(v, 0)


def pct(v, d=1):
    return "" if v is None or pd.isna(v) else f"{100 * v:.{d}f}%"


def _read(name):
    p = _path(name)
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


def _row(df, **kv):
    m = np.ones(len(df), bool)
    for k, v in kv.items():
        m &= (df[k].astype(str) == str(v)).to_numpy()
    return df[m].iloc[0] if m.any() else None


def data_summary(tf=TF):
    """Per market: years, entry events, events per session, win rate and $ of taking every event, exit trades/rows."""
    rows = []
    for s in MARKETS:
        e = pd.read_parquet(_path(f"entries_{s}_{tf}.parquet"),
                            columns=["t", "session", f"y_{PRIMARY_R}", f"pnl_usd_{PRIMARY_R}", "risk_usd",
                                     f"exit_kind_{PRIMARY_R}", "cost_R", "stop_R20"])
        x = pd.read_parquet(_path(f"exits_{s}_{tf}.parquet"), columns=["trade", "src", "hold_pnl_usd"])
        h = x.groupby("trade", sort=False).agg(src=("src", "first"), hold=("hold_pnl_usd", "first"))
        rows.append({"market": f"{s} ({MICRO[s]})", "data": f"{e.t.min():%Y-%m} to {e.t.max():%Y-%m}",
                     "entry events": f"{len(e):,}", "events / day": f"{len(e) / e.session.nunique():.0f}",
                     "win rate (1.5R)": pct(e[f"y_{PRIMARY_R}"].mean()),
                     "$ / event": usd(e[f"pnl_usd_{PRIMARY_R}"].mean()),
                     "median risk $": f"${e.risk_usd.median():.2f}",
                     "median stop (avg bars)": f"{e.stop_R20.median():.2f}",
                     "median cost / risk": f"{e.cost_R.median():.2f}R",
                     "exit trades (signal / random)": f"{(h.src == 'signal').sum():,} / {(h.src == 'random').sum():,}",
                     "exit rows": f"{len(x):,}"})
    return pd.DataFrame(rows)


def stage_report(tf=TF):
    """Write REPORT.md (plain language, for a trader) from the CSVs and parquet files in out/."""
    for kind in ("entry", "exit"):                                # scorecards from the saved weight tables
        for scope in SCOPES:
            wt = _read(f"weights_{kind}_{scope}.csv")
            if len(wt):
                scorecard_table(wt, kind).to_csv(_path(f"scorecard_{kind}_{scope}.csv"), index=False)
    ER, EF, EC = _read("entry_results.csv"), _read("entry_folds.csv"), _read("entry_calibration.csv")
    XR, XF, XC = _read("exit_results.csv"), _read("exit_folds.csv"), _read("exit_calibration.csv")
    XS, PM, PR, TR = _read("exit_by_src.csv"), _read("permutation.csv"), _read("prop_results.csv"), _read("trials.csv")
    cs, cm = CHOSEN
    L = []
    w = L.append
    er = _row(ER, scope=cs, model=cm)
    xr = _row(XR, scope=cs, model=cm)

    # ---------------------------------------------------------------- headline
    w("# Confidence scores for pattern entries and exits: walk-forward results")
    w("")
    w(f"15-minute bars; ES, NQ and YM traded as MES, MNQ and MYM. All money is **net $ per 1 micro contract after "
      f"costs**: $1.00 commission, 1 tick of slippage on entry and on exit, and 1 more tick when a stop fills. "
      f"Results are **out of sample**: every number for a year comes from a model trained only on earlier years. The "
      f"test years are 2013 to 2024 and the first half of 2025. The locked holdout (2025-07-01 onward) was never "
      f"labelled, fitted or looked at. Generated by `run_pipeline.py` on {datetime.now():%Y-%m-%d}.")
    w("")
    w("## The short version")
    w("")
    bullets = headline(ER, XR, XS, PM, PR, TR)
    L.extend(bullets)
    w("")

    # ---------------------------------------------------------------- method
    w("## What was tested")
    w("")
    w("* **Entry events.** An event is any 15-minute bar where at least one of the 24 textbook directional "
      "candlestick patterns fires. The trade goes in the pattern's textbook direction. The patterns fire often, "
      "so there are about 80 events per market per day.")
    w("* **The trade.** Enter at the open of the next bar. The stop goes 1 tick beyond the pattern's extreme. "
      "The target is 1.5 times the risk (1.5R). The time limit is 16 bars (4 hours) or 16:45 ET, whichever comes "
      "first. The path is checked minute by minute; if one minute touches both the stop and the target, the stop "
      "counts. A trade is a **win** (y = 1) when it makes money after costs.")
    w("* **The confidence model.** For every event the model estimates the chance the trade is a win, using "
      "everything known at the close of the signal bar: all patterns, pattern families, swing structure, EMAs, "
      "momentum, VWAP, the bar's shape and volume, the day so far, time of day, the 60-minute trend and the other "
      "two markets. Every input is seen from the trade's side, so + means \"in the trade's direction\".")
    w("  * `logit` is the main model: a regularised logistic regression whose weights become the **scorecard**.")
    w("  * `gbm` is shallow boosted trees with isotonic calibration.")
    w("  * `vote` is an equal-weight family vote. It is the simple baseline the learned models must beat.")
    w("* **Decision.** Take an event when its score is at or above a threshold. Each fold picks its threshold on "
      "its own training years (out-of-sample predictions there) to maximise $ per trade, keeping at least 5% of "
      "events. The test year never sets its own threshold.")
    w("* **Walk-forward.** Expanding window by calendar year. Labels that end within 1 day of the test start are "
      "purged. YM data starts in 2018, so YM's own folds start in 2021. Events are weighted by how much their "
      "trade windows overlap and by how many markets fire on the same bar, since ES/NQ/YM events on the same bar "
      "are close to one trade.")
    w("* **Exit model.** Trades from 25% of the entry events plus random-time entries are held with the stop only "
      "(no target), up to 32 bars or 16:45. At the close of every bar the trade is open, the model scores "
      "\"exit at the next open beats holding to the end\". The learned exit closes the trade at the first bar where "
      "that score clears the fold's threshold.")
    w("* **Units.** Distances are in **average bars**: 1 average bar is the mean high-low range of the 20 bars "
      "before the signal. R is the trade's initial risk (entry to stop).")
    w("* **Two inputs added beyond SPEC.md** (both known at the signal close): `stop_R20` is the stop distance in "
      "average bars, and `cost_R` is the round-trip cost as a share of the planned risk. The pooled models also get "
      "a market flag (`mkt_ES/NQ/YM`).")
    w("")
    w("### The data")
    w("")
    w(md_table(data_summary(tf)))
    w("")
    w("Taking every event loses money in every market. The stops are tight: the median stop sits about half an "
      "average bar from the close, so costs are a large share of the risk on a typical event.")
    w("")

    # ---------------------------------------------------------------- entries
    w("## 1. Entry model: does the confidence score pick better trades?")
    w("")
    w("Pooled results over all test folds. The baselines take the **same number of trades** as the model:")
    w("")
    w("* **all events**: take everything.")
    w("* **vote top-N**: the N events with the highest family vote.")
    w("* **random skip**: N events picked at random, repeated 200 times, showing the mean and the 5-95% range.")
    w("* **best pattern**: the single pattern with the best $ per trade in the training years.")
    w("")
    if len(ER):
        t = ER.copy()
        t["scope"] = t.scope.map(lambda s: "pooled (ES+NQ+YM)" if s == "pooled" else s)
        t["random skip (5-95%)"] = [f"{usd(a)} ({usd(b)} to {usd(c)})" for a, b, c in
                                    zip(t.random_pnl_per_trade, t.random_p5, t.random_p95)]
        cols = {"scope": "scope", "model": "model", "auc": "AUC", "n_kept": "trades kept", "keep_share": "kept share",
                "pnl_per_trade": "model $/trade", "usd_per_year": "model $/year", "all_pnl_per_trade": "all events $/trade",
                "vote_topN_pnl_per_trade": "vote top-N $/trade", "random skip (5-95%)": "random skip $/trade (5-95%)",
                "pattern_pnl_per_trade": "best pattern $/trade"}
        t = t[list(cols)].rename(columns=cols)
        w(md_table(t, {"AUC": ".3f", "trades kept": lambda v: f"{int(v):,}", "kept share": pct,
                       "model $/trade": usd, "model $/year": usd0, "all events $/trade": usd,
                       "vote top-N $/trade": usd, "best pattern $/trade": usd}))
        w("")
        w("AUC measures how well the score ranks winners above losers: 0.5 is a coin flip and 1.0 is perfect. "
          "A trader should read the **$/trade** columns. Every model figure is out of sample.")
        w("")
        w(entry_commentary(ER, EF))
        w("")
    if len(EF):
        f = EF[(EF.scope == cs) & (EF.model == cm)].copy()
        w(f"### Fold by fold: chosen model ({cs} {cm})")
        w("")
        f["random (5-95%)"] = [f"{usd(a)} ({usd(b)} to {usd(c)})" for a, b, c in
                               zip(f.random_pnl_per_trade, f.random_p5, f.random_p95)]
        f["best pattern (train)"] = [f"{str(p).replace('pat_', '')} {usd(v)} (n={int(n):,})" if isinstance(p, str)
                                     else "" for p, v, n in zip(f.best_pattern, f.pattern_pnl_per_trade, f.pattern_n)]
        cols = {"fold": "test year", "n_test": "events", "n_kept": "kept", "threshold": "threshold p",
                "pnl_per_trade": "model $/trade", "total_usd": "model total $", "all_pnl_per_trade": "all events $/trade",
                "vote_topN_pnl_per_trade": "vote top-N $/trade", "random (5-95%)": "random skip $/trade (5-95%)",
                "best pattern (train)": "best training pattern, its test $/trade", "auc": "AUC"}
        w(md_table(f[list(cols)].rename(columns=cols),
                   {"events": lambda v: f"{int(v):,}", "kept": lambda v: f"{int(v):,}", "threshold p": ".3f",
                    "model $/trade": usd, "model total $": usd0, "all events $/trade": usd,
                    "vote top-N $/trade": usd, "AUC": ".3f"}))
        w("")
        good = int((f.pnl_per_trade > f.all_pnl_per_trade).sum())
        pos = int((f.total_usd > 0).sum())
        beat_r = int((f.pnl_per_trade > f.random_p95).sum())
        w(f"The model beat taking every event in {good} of {len(f)} test years and beat the 95th percentile of "
          f"random skipping in {beat_r}. It made money after costs in {pos} of {len(f)} years.")
        if "C" in f.columns and f.C.notna().any():
            lo = int((f.C == min(wf.C_GRID)).sum())
            w(f"The inner time split chose the strongest shrinkage on the grid (C = {min(wf.C_GRID):g}) in {lo} of "
              f"{len(f)} folds. That is a sign that, apart from a few inputs, the data supports only small weights.")
        w("")
        bt = chosen_breakdown()
        if bt is not None:
            w("What the chosen model keeps, by market. These are its out-of-sample trades compared with every "
              "event in the same test years:")
            w("")
            w(md_table(bt))
            w("")
    w("### Calibration: when the model says 40%, do about 40% win?")
    w("")
    for m in ("logit", "gbm"):
        c = EC[(EC.scope == cs) & (EC.model == m)] if len(EC) else EC
        if len(c):
            w(f"**{cs} {m}**: all test events in 10 equal-size groups by predicted chance.")
            w("")
            c = c.rename(columns={"bin": "group", "n": "events", "p_mean": "predicted win %",
                                  "y_rate": "actual win %", "pnl_mean": "avg $/event"})
            w(md_table(c[["group", "events", "predicted win %", "actual win %", "avg $/event"]],
                       {"group": lambda v: str(int(v) + 1), "events": lambda v: f"{int(v):,}",
                        "predicted win %": pct, "actual win %": pct, "avg $/event": usd}))
            w("")
    w(calibration_commentary(EC, cs))
    w("")

    # ---------------------------------------------------------------- exits
    w("## 2. Exit model: does the score know when to get out?")
    w("")
    w("Each trade is held with its stop only, and the exit policy can close it earlier at a bar's next open. "
      "The table shows **$ gained per trade compared with holding**:")
    w("")
    w("* **learned**: exit at the first bar where the model's score clears its threshold.")
    w("* **opposite pattern**: exit at the first bar where any classic candle pattern fires against the trade.")
    w("* **random time**: exit at a random bar, with the same exit share and the same timing as the learned exit "
      "(200 draws).")
    w("")
    w("*Net $/trade* is the whole trade's result after costs.")
    w("")
    sv = first_bar_stops(tf)
    if sv is not None:
        w(f"**Read the net columns with care.** An exit decision happens at a bar's close, so the exit study only "
          f"contains trades still open at the close of their entry bar. {pct(sv['share'])} of the pattern entries "
          f"are stopped out inside their entry bar. Those trades average {usd(sv['first'])} on the 1.5R entry "
          f"labels, while the trades that survive the entry bar average {usd(sv['surv'])}. That is why *hold net* "
          f"is positive here although taking every event loses money: it describes the survivors only. The "
          f"*vs hold* columns are not affected, because the first-bar stops are the same under every exit rule.")
        w("")
    if len(XR):
        t = XR.copy()
        t["scope"] = t.scope.map(lambda s: "pooled (ES+NQ+YM)" if s == "pooled" else s)
        t["random (5-95%)"] = [f"{usd(a)} ({usd(b)} to {usd(c)})" for a, b, c in
                               zip(t.random_gain, t.random_p5, t.random_p95)]
        cols = {"scope": "scope", "model": "model", "auc": "AUC", "n_trades": "test trades",
                "learned_exit_share": "exits early", "learned_gain": "learned vs hold",
                "opp_gain": "opposite pattern vs hold", "random (5-95%)": "random time vs hold (5-95%)",
                "hold_net": "hold net $/trade", "learned_net": "learned net $/trade",
                "learned_gain_per_year": "learned gain $/year"}
        w(md_table(t[list(cols)].rename(columns=cols),
                   {"AUC": ".3f", "test trades": lambda v: f"{int(v):,}", "exits early": pct,
                    "learned vs hold": usd, "opposite pattern vs hold": usd, "hold net $/trade": usd,
                    "learned net $/trade": usd, "learned gain $/year": usd0}))
        w("")
    if len(XS):
        s = XS[(XS.scope == cs) & (XS.model == cm)].copy()
        if len(s):
            w(f"Split by how the trade was entered ({cs} {cm}):")
            w("")
            s["random (5-95%)"] = [f"{usd(a)} ({usd(b)} to {usd(c)})" for a, b, c in
                                   zip(s.random_gain, s.random_p5, s.random_p95)]
            cols = {"src": "entry", "n_trades": "trades", "hold_net": "hold net $/trade",
                    "learned_exit_share": "exits early", "learned_gain": "learned vs hold",
                    "learned_net": "learned net $/trade", "opp_gain": "opposite pattern vs hold",
                    "random (5-95%)": "random time vs hold (5-95%)"}
            w(md_table(s[list(cols)].rename(columns=cols),
                       {"trades": lambda v: f"{int(v):,}", "hold net $/trade": usd, "exits early": pct,
                        "learned vs hold": usd, "learned net $/trade": usd, "opposite pattern vs hold": usd}))
            w("")
    w(exit_commentary(XR, XF, XS))
    w("")
    hb = hold_baseline_table(tf)
    if hb is not None:
        w("**The exit study's baseline trade.** This table is descriptive: it uses all years of data and no model. "
          "It covers only trades still open at the close of their entry bar, each held with the stop only for up "
          "to 32 bars (8 hours) or until 16:45. *Stopped* is the share that end at the stop later on. Because the "
          "first-bar stops are left out, these numbers are not the $ of trading the pattern entries this way.")
        w("")
        w(md_table(hb))
        w("")
    if len(XF):
        f = XF[(XF.scope == cs) & (XF.model == cm)].copy()
        w(f"### Fold by fold: {cs} {cm} exit")
        w("")
        f["random (5-95%)"] = [f"{usd(a)} ({usd(b)} to {usd(c)})" for a, b, c in
                               zip(f.random_gain, f.random_p5, f.random_p95)]
        cols = {"fold": "test year", "n_trades": "trades", "threshold": "threshold p", "auc": "AUC",
                "learned_exit_share": "exits early", "learned_gain": "learned vs hold",
                "opp_gain": "opposite pattern vs hold", "random (5-95%)": "random time vs hold (5-95%)",
                "hold_net": "hold net $/trade", "learned_net": "learned net $/trade"}
        w(md_table(f[list(cols)].rename(columns=cols),
                   {"trades": lambda v: f"{int(v):,}", "threshold p": ".3f", "AUC": ".3f", "exits early": pct,
                    "learned vs hold": usd, "opposite pattern vs hold": usd, "hold net $/trade": usd,
                    "learned net $/trade": usd}))
        w("")
    c = XC[(XC.scope == cs) & (XC.model == cm)] if len(XC) else XC
    if len(c):
        w(f"Exit calibration ({cs} {cm}): predicted vs actual share of bars where exiting beat holding.")
        w("")
        c = c.rename(columns={"bin": "group", "n": "bars", "p_mean": "predicted %", "y_rate": "actual %",
                              "pnl_mean": "avg $ gain of exiting"})
        w(md_table(c[["group", "bars", "predicted %", "actual %", "avg $ gain of exiting"]],
                   {"group": lambda v: str(int(v) + 1), "bars": lambda v: f"{int(v):,}", "predicted %": pct,
                    "actual %": pct, "avg $ gain of exiting": usd}))
        w("")

    # ---------------------------------------------------------------- permutation
    w("## 3. Could it be luck? Permutation test")
    w("")
    w("The outcomes (win/loss and $) were shuffled at random within each year, which destroys any real link "
      "between the inputs and the outcome. The whole procedure (model, C, threshold) was then refitted, and the "
      "shuffled model was scored on the **true** test outcomes. A real edge should beat almost every shuffle. "
      "With 20 shuffles the smallest possible p-value is 1/21 = 0.048.")
    w("")
    if len(PM):
        t = PM.copy()
        t["test"] = t.kind + " " + t.scope + " " + t.model
        cols = {"test": "model", "score": "score compared", "real": "real model", "perm_mean": "shuffles: mean",
                "perm_p95": "shuffles: 95th pct", "perm_max": "shuffles: best", "p_value": "p-value",
                "n_valid": "valid shuffles"}
        w(md_table(t[list(cols)].rename(columns=cols),
                   {"real model": lambda v: f"{v:,.2f}", "shuffles: mean": lambda v: f"{v:,.2f}",
                    "shuffles: 95th pct": lambda v: f"{v:,.2f}", "shuffles: best": lambda v: f"{v:,.2f}",
                    "p-value": ".3f", "valid shuffles": lambda v: str(int(v))}))
        w("")
        w(perm_commentary(PM))
        w("")
    else:
        w("(not run)")
        w("")

    # ---------------------------------------------------------------- stability + scorecards
    w("## 4. Are the weights stable from year to year?")
    w("")
    w("Each fold refits the logistic regression. *Sign stability* is the share of folds in which a weight has the "
      "same sign as its median. 1.0 means it always points the same way; 0.5 means it flips half the time.")
    w("")
    for kind in ("entry", "exit"):
        wt = _read(f"weights_{kind}_{cs}.csv")
        if not len(wt):
            continue
        wt = wt[wt.feature != "(intercept)"]
        big = wt.coef_std_median.abs() >= 0.05
        w(f"* **{kind} model ({cs})**: {len(wt)} inputs, {int(wt.n_folds.max())} folds. "
          f"{(wt.sign_stability >= 0.999).sum()} inputs keep their sign in every fold, and "
          f"{(wt.sign_stability >= 0.8).sum()} do in at least 80% of folds. Of the {int(big.sum())} inputs with a "
          f"sizeable weight (|weight per 1 SD| >= 0.05), {int((big & (wt.sign_stability >= 0.8)).sum())} are stable "
          f"in at least 80% of folds.")
    w("")
    w("## 5. The scorecards")
    w("")
    w("**How to read a scorecard.** Every input has a number of points per unit, taken from the median logistic "
      "weight across the folds.")
    w("")
    w("* A trade's score is the sum of points times the input's value.")
    w("* **+20 points doubles the odds** (odds = chance / (1 - chance)), and -20 halves them. For example, odds of "
      "1:2 (a 33% chance) become 2:2 (50%) at +20 points.")
    w("* Signed inputs are seen from the trade, so \"+1\" means \"in the trade's direction\": a bullish pattern on a "
      "long, a bearish one on a short.")
    w("* *Points per 1 SD* gives the points for a typical-size change in the input, which lets you compare inputs "
      "measured in different units.")
    w("* *Stable* is the sign stability defined in section 4.")
    w("")
    w("These are the 25 inputs with the most points per unit.")
    w("")
    for kind, title, note in (("entry", "Entry scorecard: points toward \"this trade wins\"",
                               "Positive points mean the input makes a winning trade more likely."),
                              ("exit", "Exit scorecard: points toward \"exiting now beats holding\"",
                               "Positive points mean the input makes exiting at the next open better than holding. "
                               "Negative points mean it argues for staying in.")):
        sc = _read(f"scorecard_{kind}_{cs}.csv")
        if not len(sc):
            continue
        w(f"### {title} ({cs} logit)")
        w("")
        w(note)
        w("")
        top = sc[sc.feature != "(intercept)"].head(25)
        t = top[["feature", "points", "unit", "points_1sd", "sign_stability", "meaning"]].rename(
            columns={"feature": "input", "points_1sd": "points per 1 SD", "sign_stability": "stable"})
        w(md_table(t, {"points": lambda v: f"{int(v):+d}", "points per 1 SD": lambda v: f"{int(v):+d}",
                       "stable": ".2f"}, align=["---", "---:", "---", "---:", "---:", "---"]))
        ic = sc[sc.feature == "(intercept)"]
        if len(ic):
            w("")
            w(f"Base score (intercept on the raw scale): {int(ic.points.iloc[0]):+d} points. The full table "
              f"is in `out/scorecard_{kind}_{cs}.csv`, and the fold-by-fold weights are in "
              f"`out/coefs_{kind}_{cs}.csv`.")
        w("")
        w(scorecard_commentary(sc, kind))
        w("")

    # ---------------------------------------------------------------- prop
    w("## 6. Prop-firm odds: LucidFlex 25K")
    w("")
    w("The chosen entry rule's out-of-sample trades are summed per trading day at **1 micro per trade**. That daily "
      "$ series is run through `prop_sim.simulate` with the LucidFlex 25K defaults:")
    w("")
    w("* $1,250 profit target.")
    w("* $1,000 maximum loss, trailing the highest end-of-day balance and locking at $25,100.")
    w("* 40% consistency rule.")
    w("")
    w("An account is started on every trading day of the test period. **Pass odds** = passes / (passes + fails); "
      "accounts still open when the data ends are left out.")
    w("")
    w("**Day-block views.** These rebuild 200 alternative histories from runs of 5 or 20 *consecutive* trading days "
      "of the real series, then start an account on every day of each history. Keeping days in blocks keeps losing "
      "streaks together; shuffling single trades would break them up and make passing look easier. The table "
      "shows the median pass rate with its 5-95% range.")
    w("")
    if len(PR):
        w(md_table(prop_table(PR), align=["---"] + ["---:"] * 11))
        w("")
        w(prop_commentary(PR))
        w("")
        w("*Max open* is the largest number of these trades open at once, counting all three markets. LucidFlex "
          "caps open positions at 20 micros. Taking every event would need far more than that, so its row only "
          "shows what the raw events are worth.")
        w("")

    # ---------------------------------------------------------------- caveats
    w("## 7. Caveats and the data-snooping count")
    w("")
    n_cfg = int(TR.module.isin(["entry", "exit"]).sum()) if len(TR) else 0
    w(f"* **Trials.** `out/trials.csv` logs {n_cfg} model configurations evaluated out of sample. These are "
      f"{int((TR.module == 'entry').sum()) if len(TR) else 0} entry and "
      f"{int((TR.module == 'exit').sum()) if len(TR) else 0} exit walk-forwards: 3 models x 4 scopes, plus 3 "
      f"two-fold timing tests run before the full run. Permutation and prop runs are logged too, but they are "
      f"tests of those configurations, not new ones. The earlier single-pattern, filter and timeframe studies in "
      f"`research/signals` also count against this data, and they touched 2013-2025. Treat a borderline result as "
      f"not proven.")
    w(f"* **The chosen model was fixed in advance.** It is the pooled logit, because it produces the scorecard. "
      f"The other models and scopes are shown for comparison, not picked by their results.")
    w("* **Prices of the day.** $ are at the prices of the time, with fixed $ costs. The same move is worth fewer "
      "$ in 2013 than in 2025, so costs weigh more in early years. The models see costs through `cost_R`.")
    w("* **No position limit in the labels.** Every event is its own trade, so overlapping trades in the same or "
      "another market all count. Section 6 shows how many are open at once.")
    w("* **Exits are judged on the baseline trade** (stop only, no target). A learned exit that beats holding is not "
      "automatically better than the 1.5R target used for entries.")
    w("* **Module fix made during this run.** scikit-learn 1.9's HistGradientBoosting crashes on a feature column "
      "with no finite value in the training rows. Pooled folds trained before 2018 hit this, because YM's "
      "cross-market columns are empty then. `walkforward.GBMModel` now fits only on columns that vary in the "
      "training rows (`informative_columns`); regression test `test_gbm_constant_and_empty_columns` in "
      "`test_walkforward.py`.")
    w("* The locked holdout (Globex sessions from 2025-07-01) was cut from the bars before any labelling.")
    w("")
    w("## Files")
    w("")
    w("All files are in `research/confidence/out/`:")
    w("")
    w("* **Datasets:** `entries_<SYM>_15.parquet` (one row per entry event: labels and features) and "
      "`exits_<SYM>_15.parquet` (one row per open-trade bar).")
    w("* **Results:** `entry_results.csv` / `exit_results.csv` (pooled out-of-sample results, one row per scope and "
      "model), `entry_folds.csv` / `exit_folds.csv` (fold by fold, with baselines), `entry_calibration.csv` / "
      "`exit_calibration.csv`, and `exit_by_src.csv`.")
    w("* **Weights:** `coefs_*.csv` (logit weights per fold), `weights_*.csv` (medians and sign stability) and "
      "`scorecard_*.csv`.")
    w("* **Out-of-sample rows:** `oos_<kind>_<scope>_<model>.parquet`, with p, take and $ for every test row.")
    w("* **Tests and logs:** `permutation.csv`, `prop_results.csv`, `prop_daily.csv`, and `trials.csv` (the "
      "data-snooping log).")
    w("")
    w("To rerun: `cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. "
      "python3 run_pipeline.py [data entry exit perm prop report]`")
    with open(os.path.join(HERE, "REPORT.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    _say(f"wrote REPORT.md ({len(L)} lines)")


def chosen_breakdown():
    """By market: kept trades vs all events of the chosen entry model's OOS rows (count, win rate, $/trade, median
    stop distance and cost/risk)."""
    cs, cm = CHOSEN
    p = _path(f"oos_entry_{cs}_{cm}.parquet")
    if not os.path.exists(p):
        return None
    o = pd.read_parquet(p, columns=["market", "take", "y", "pnl", "stop_R20", "cost_R"])
    rows = []
    for m, g in list(o.groupby("market", sort=False)) + [("all", o)]:
        k = g[g["take"].to_numpy(bool)]
        rows.append({"market": m, "test events": f"{len(g):,}", "kept": f"{len(k):,} ({pct(len(k) / len(g))})",
                     "win rate kept / all": f"{pct(k.y.mean())} / {pct(g.y.mean())}",
                     "$/trade kept / all": f"{usd(k.pnl.mean())} / {usd(g.pnl.mean())}",
                     "median stop, avg bars (kept / all)": f"{k.stop_R20.median():.2f} / {g.stop_R20.median():.2f}",
                     "median cost / risk (kept / all)": f"{k.cost_R.median():.2f}R / {g.cost_R.median():.2f}R"})
    return pd.DataFrame(rows)


def first_bar_stops(tf=TF):
    """Share of pattern entries stopped inside their entry bar (1.5R labels: a stop whose exit minute ends by the
    entry bar's close) and the mean 1.5R $ of those vs the survivors. None if the datasets are missing."""
    parts = []
    for s in MARKETS:
        p = _path(f"entries_{s}_{tf}.parquet")
        if not os.path.exists(p):
            return None
        parts.append(pd.read_parquet(p, columns=["t_entry", f"t_end_{PRIMARY_R}", f"exit_kind_{PRIMARY_R}",
                                                 f"pnl_usd_{PRIMARY_R}"]))
    e = pd.concat(parts, ignore_index=True)
    first = ((e[f"exit_kind_{PRIMARY_R}"] == "stop") &
             (e[f"t_end_{PRIMARY_R}"] <= e["t_entry"] + pd.Timedelta(minutes=tf))).to_numpy()
    pnl = e[f"pnl_usd_{PRIMARY_R}"].to_numpy(np.float64)
    return dict(share=float(first.mean()), first=float(pnl[first].mean()), surv=float(pnl[~first].mean()))


def hold_baseline_table(tf=TF):
    """Descriptive (all data, no model): the exit study's baseline trade per market and entry type - trades, share
    stopped, mean net $ held to the end, by era."""
    rows = []
    for s in MARKETS:
        p = _path(f"exits_{s}_{tf}.parquet")
        if not os.path.exists(p):
            return None
        x = pd.read_parquet(p, columns=["trade", "src", "t", "hold_pnl_usd", "end_kind"])
        h = x.groupby("trade", sort=False).first()
        for src in ("signal", "random"):
            g = h[h.src == src]
            early, late = g[g.t < pd.Timestamp("2018-01-01")], g[g.t >= pd.Timestamp("2018-01-01")]
            rows.append({"market": s, "entry": src, "trades": f"{len(g):,}",
                         "stopped": pct((g.end_kind == "stop").mean()),
                         "net $/trade held": usd(g.hold_pnl_usd.mean()),
                         "2010-17": usd(early.hold_pnl_usd.mean()) if len(early) else "",
                         "2018-25H1": usd(late.hold_pnl_usd.mean()),
                         "median trade": usd(g.hold_pnl_usd.median())})
    return pd.DataFrame(rows)


def prop_table(PR):
    """One row per rule: trades, $/trade, net $/yr, day stats, max open, pass odds (history, by era, day-block)."""
    rows = []
    for rule in pd.unique(PR.rule):
        g = PR[PR.rule == rule]
        h = g[g.view == "history"].iloc[0]
        b = {v: g[g.view == v].iloc[0] for v in g.view if v.startswith("day-block")}
        rr = {"rule": rule, "trades": f"{int(h.n_trades):,}" if pd.notna(h.get("n_trades")) else "",
              "$/trade": usd(h.get("usd_per_trade")), "net $/year": usd0(h.get("net_yr")),
              "worst day": usd0(h.get("worst_day")), "max drawdown": usd0(-h.get("max_dd", np.nan)),
              "max open": "" if pd.isna(h.get("max_open")) else f"{int(h.max_open)}"}
        if "pass_p5" in h and pd.notna(h.get("pass_p5")):
            rr["pass odds (history)"] = f"{pct(h.pass_rate)} ({pct(h.pass_p5)}-{pct(h.pass_p95)})"
        else:
            rr["pass odds (history)"] = pct(h.pass_rate)
        for e in ERAS_OOS:
            rr[f"pass {e}"] = pct(h.get(f"pass_{e}"))
        for v in (f"day-block {k}" for k in BLOCKS):
            rr[f"pass, {v} (5-95%)"] = (f"{pct(b[v].pass_rate)} ({pct(b[v].pass_p5)}-{pct(b[v].pass_p95)})"
                                        if v in b else "")
        rows.append(rr)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- data-driven sentences
def headline(ER, XR, XS, PM, PR, TR):
    cs, cm = CHOSEN
    out = []
    er = _row(ER, scope=cs, model=cm) if len(ER) else None
    if er is not None:
        verdict = "make money" if er.pnl_per_trade > 0 else "still lose money"
        out.append(f"* **Entries.** The chosen confidence model ({cs} logistic regression) kept {pct(er.keep_share)} "
                   f"of the {int(er.all_n):,} test events. Its trades averaged **{usd(er.pnl_per_trade)} per trade** "
                   f"({usd0(er.usd_per_year)} a year at 1 micro each). Taking every event averaged "
                   f"{usd(er.all_pnl_per_trade)}, and random skipping to the same count averaged "
                   f"{usd(er.random_pnl_per_trade)} (5-95%: {usd(er.random_p5)} to {usd(er.random_p95)}). "
                   f"The score ranks trades well (AUC {er.auc:.3f}), but the selected trades {verdict} after costs.")
        best = ER.loc[ER.pnl_per_trade.idxmax()]
        out.append(f"* The best row of all {len(ER)} entry runs is {best.scope} {best.model} at "
                   f"{usd(best.pnl_per_trade)} per trade. The count of runs matters, see section 7. "
                   f"{'No' if (ER.pnl_per_trade <= 0).all() else 'Some'} entry configuration made money out of "
                   f"sample.")
    xr = _row(XR, scope=cs, model=cm) if len(XR) else None
    if xr is not None:
        out.append(f"* **Exits.** The learned exit ({cs} logit) closed {pct(xr.learned_exit_share)} of trades early "
                   f"and gained **{usd(xr.learned_gain)} per trade** over holding to the stop or time limit. "
                   f"Exiting at random times with the same timing gained {usd(xr.random_gain)} (5-95%: "
                   f"{usd(xr.random_p5)} to {usd(xr.random_p95)}), and exiting on any opposite classic pattern gained "
                   f"{usd(xr.opp_gain)}. Whole trades: {usd(xr.get('hold_net'))} per trade when held, "
                   f"{usd(xr.get('learned_net'))} with the learned exit.")
    if len(PM):
        for _, p in PM.iterrows():
            out.append(f"* **Permutation test, {p.kind} {p.scope} {p.model}:** p = {p.p_value:.3f} "
                       f"(real {p.real:,.2f} vs shuffled mean {p.perm_mean:,.2f}; "
                       f"{'better than every shuffle' if p.real > p.perm_max else 'not better than every shuffle'}).")
    if len(PR):
        h = PR[(PR.view == "history")]
        ch = h[h.rule.str.contains("chosen")]
        al = h[h.rule == "all events"]
        if len(ch):
            c = ch.iloc[0]
            b20 = PR[(PR.rule == c.rule) & (PR.view == "day-block 20")]
            out.append(f"* **LucidFlex 25K pass odds** for the chosen rule at 1 micro per trade: {pct(c.pass_rate)} "
                       f"over every start day of 2013-2025H1, and a {pct(b20.pass_rate.iloc[0]) if len(b20) else '?'} "
                       f"median on 20-day-block bootstraps. Taking every event gives "
                       f"{pct(al.pass_rate.iloc[0]) if len(al) else '?'}. Net {usd0(c.net_yr)} a year from "
                       f"{c.trades_yr:,.0f} trades a year.")
    if len(TR):
        out.append(f"* **Data-snooping count:** {int(TR.module.isin(['entry', 'exit']).sum())} out-of-sample "
                   f"configurations are logged in `out/trials.csv`.")
    return out


def entry_commentary(ER, EF):
    cs, cm = CHOSEN
    s = []
    lg = ER[ER.model == "logit"]
    gb = ER[ER.model == "gbm"]
    vt = ER[ER.model == "vote"]
    if len(lg) and len(vt):
        s.append(f"The learned models rank events much better than the equal-weight vote: logit AUC "
                 f"{lg.auc.min():.3f}-{lg.auc.max():.3f} and gbm {gb.auc.min():.3f}-{gb.auc.max():.3f}, against "
                 f"{vt.auc.min():.3f}-{vt.auc.max():.3f} for the vote.")
    better = (ER.pnl_per_trade > ER.random_p95).sum()
    s.append(f"In {better} of {len(ER)} runs the kept trades beat the 95th percentile of random skipping, so the "
             f"selection is not luck. {'Every' if (ER.pnl_per_trade <= 0).all() else 'Not every'} run is still "
             f"negative after costs. Ranking which events are less bad is easier than finding events that pay.")
    return " ".join(s)


def calibration_commentary(EC, scope):
    if not len(EC):
        return ""
    c = EC[(EC.scope == scope) & (EC.model == "logit")]
    if not len(c):
        return ""
    gap = float(np.average(np.abs(c.p_mean - c.y_rate), weights=c.n))
    top = c.iloc[-1]
    return (f"The logit's average gap between predicted and actual win rate is {pct(gap)}. Its top 10% of events "
            f"won {pct(top.y_rate)} against a predicted {pct(top.p_mean)}, averaging {usd(top.pnl_mean)} per event. "
            f"A higher win chance does not always mean more $: a wide-stop trade can win more often and still risk "
            f"more.")


def exit_commentary(XR, XF, XS):
    cs, cm = CHOSEN
    xr = _row(XR, scope=cs, model=cm) if len(XR) else None
    if xr is None:
        return ""
    edge = xr.learned_gain - xr.random_gain
    s = [f"Most of the gain from exiting early does not come from the model. With the stop as the only exit, the "
         f"baseline trade usually ends at the stop and pays an extra tick of slippage there, so exiting at a random "
         f"bar also beats holding ({usd(xr.random_gain)} per trade). The learned exit's own contribution is the "
         f"difference: {usd(edge)} per trade, which is "
         f"{'above' if xr.learned_gain > xr.random_p95 else 'not above'} the random draws' 95th percentile."]
    if len(XF):
        f = XF[(XF.scope == cs) & (XF.model == cm)]
        s.append(f"The learned exit beat random timing in {int((f.learned_gain > f.random_gain).sum())} of {len(f)} "
                 f"years and beat the opposite-pattern exit in {int((f.learned_gain > f.opp_gain).sum())}.")
    return " ".join(s)


def perm_commentary(PM):
    s = []
    for _, p in PM.iterrows():
        if p.p_value <= 0.05:
            s.append(f"{p.kind} {p.scope} {p.model}: the real model beat the shuffles (p = {p.p_value:.3f}), so its "
                     f"out-of-sample selection reflects a real link between inputs and outcomes.")
        else:
            s.append(f"{p.kind} {p.scope} {p.model}: p = {p.p_value:.3f}, so the real model is not clearly "
                     f"better than chance.")
    s.append("A significant permutation test shows the model ranks events better than chance. It does not show the "
             "selected trades make money; the $ tables answer that.")
    return " ".join(s)


def scorecard_commentary(sc, kind):
    s = sc[sc.feature != "(intercept)"]
    top_sd = s.reindex(s.points_1sd.abs().sort_values(ascending=False).index).head(6)
    names = ", ".join(f"`{f}` ({p:+d} per SD)" for f, p in zip(top_sd.feature, top_sd.points_1sd))
    stable = s[(s.sign_stability >= 0.999) & (s.points_1sd.abs() >= 3)]
    return (f"Biggest effects for a typical change: {names}. {len(stable)} inputs have a sizeable effect "
            f"(at least 3 points per SD) and the same sign in every fold.")


def prop_commentary(PR):
    h = PR[PR.view == "history"].set_index("rule")
    ch = [r for r in h.index if "chosen" in r]
    if not ch:
        return ""
    c = h.loc[ch[0]]
    s = [f"The chosen rule averages {usd(c.day_mean)} a day with a day-to-day spread (SD) of {usd0(c.day_sd)}. Its "
         f"worst day is {usd0(c.worst_day)}, and its deepest drawdown over the whole test is {usd0(-c.max_dd)}, "
         f"against the account's $1,000 trailing limit."]
    dp = _path("prop_daily.csv")
    if os.path.exists(dp):
        d = pd.read_csv(dp, parse_dates=["date"])
        n = d[f"{ch[0]} trades"]
        v = d[f"{ch[0]} $"]
        worst = d.loc[v.nsmallest(4).index]
        days = ", ".join(f"{r.date:%Y-%m-%d} ({usd0(r[f'{ch[0]} $'])}, {int(r[f'{ch[0]} trades'])} trades)"
                         for _, r in worst.iterrows())
        s.append(f"Trades per day are very uneven: median {n.median():.0f}, 99th percentile {n.quantile(0.99):.0f}, "
                 f"maximum {n.max():.0f}. The model prefers stops that are wide relative to costs, and those are "
                 f"most common on violent days. The worst days were {days}. A few such days decide many account "
                 f"outcomes. At most {int(c.max_open)} of the rule's trades were open at the same moment; the "
                 f"95th percentile of the daily peak was {c.p95_daily_max_open:.0f}.")
    if c.net_yr <= 0:
        s.append("A rule that loses money over time can only pass on a lucky run. Its pass odds measure luck, not "
                 "edge.")
    return " ".join(s)


# ============================================================================================ main
STAGES = ("data", "entry", "exit", "perm", "prop", "report")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("stages", nargs="*", default=list(STAGES), help=" ".join(STAGES))
    ap.add_argument("--tf", type=int, default=TF)
    ap.add_argument("--markets", default=",".join(MARKETS), help="data stage markets")
    ap.add_argument("--scopes", default=",".join(SCOPES))
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--perm", default=",".join(PERM_DEFAULT), help="kind:scope:model list")
    ap.add_argument("--n-perm", type=int, default=N_PERM)
    ap.add_argument("--workers", type=int, default=None, help="perm stage: parallel processes")
    a = ap.parse_args(argv)
    bad = [s for s in a.stages if s not in STAGES]
    if bad:
        ap.error(f"unknown stage(s) {bad}")
    scopes, models = tuple(a.scopes.split(",")), tuple(a.models.split(","))
    warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
    T0 = time.time()
    for st in STAGES:
        if st not in a.stages:
            continue
        _say(f"=== stage {st}")
        if st == "data":
            stage_data(a.tf, tuple(a.markets.split(",")))
        elif st in ("entry", "exit"):
            stage_walkforward(st, a.tf, scopes, models)
        elif st == "perm":
            stage_perm(a.tf, tuple(a.perm.split(",")), a.n_perm, a.workers)
        elif st == "prop":
            stage_prop(a.tf)
        elif st == "report":
            stage_report(a.tf)
    _say(f"done in {time.time() - T0:.0f}s")


if __name__ == "__main__":
    main()
