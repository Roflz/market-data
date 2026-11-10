"""Feature blocks A (multi-horizon returns) and B (range position) vs v1 on MNQ 15-min entries.

Stage 1 (heavy, once): features_extra.build_blocks('NQ', 15) -> out/blocks_AB_NQ_15.parquet (+ R20 check column).
Stage 2: join to out/entries_NQ_15.parquet by i (verifies t == bar start and R20 == entries.R20), orient the block
columns by d HERE (features_extra.orient_blocks; they are not in features.SIGNED so walkforward leaves them alone),
then walk-forwards one at a time: {logit, gbm} x {v1, v1+A, v1+B, v1+A+B} on all events, then v1 and v1+A+B on the
cost_R <= 0.15 subset. Each run logged with run_pipeline.log_trial(module='entry-features').
Results: out/feature_blocks_NQ.csv (pooled + per test year rows), out/feature_blocks_NQ.md.
Usage: python3 run_feature_blocks.py [build|wf|md|all]
"""
import json
import os
import subprocess
import sys
import time
import warnings

import numpy as np
import pandas as pd

import features_extra as fx
import run_pipeline as rp
import walkforward as wf

SYM, TF = "NQ", 15
BLK = rp._path(f"blocks_AB_{SYM}_{TF}.parquet")
CSV = rp._path(f"feature_blocks_{SYM}.csv")
MD = rp._path(f"feature_blocks_{SYM}.md")
MIN_AVAIL = 7000


def wait_mem(what):
    while True:
        out = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout.splitlines()[1].split()
        avail = int(out[6])
        if avail >= MIN_AVAIL:
            print(f"[mem] available {avail} MB -> start {what}", flush=True)
            return
        print(f"[mem] available {avail} MB < {MIN_AVAIL}, waiting 60s before {what}", flush=True)
        time.sleep(60)


def build():
    import signals as sg                                    # noqa: PLC0415
    wait_mem("build blocks")
    t0 = time.time()
    b = sg.bars(SYM, TF)
    X = fx.compute_blocks(b, sg.SPEC[SYM]["tick"])
    X["R20_check"] = fx.r20(b, sg.SPEC[SYM]["tick"])
    X["run"] = b["run"].to_numpy()
    X.to_parquet(BLK, compression="zstd")
    print(f"blocks: {len(X):,} bars ({time.time() - t0:.0f}s) -> {BLK}", flush=True)


def joined():
    data = rp.load("entry", SYM)
    X = pd.read_parquet(BLK)
    i = data["i"].to_numpy(np.int64)
    Xi = X.iloc[i]
    assert (Xi.index.to_numpy() == pd.DatetimeIndex(data["t"]).to_numpy()).all(), "t != bar start of i"
    r_ent = data["R20"].to_numpy(np.float64); r_blk = Xi["R20_check"].to_numpy(np.float64)
    eq = (r_ent == r_blk) | (np.isnan(r_ent) & np.isnan(r_blk))
    print(f"R20 check: {eq.sum():,}/{len(eq):,} rows bit-identical to entries.R20 "
          f"(NaN rows {np.isnan(r_ent).sum():,})", flush=True)
    assert eq.all(), "R20 mismatch"
    O = fx.orient_blocks(Xi[fx.COLUMNS].reset_index(drop=True), data["d"].to_numpy())
    O.index = data.index
    print("block NaN share at entries: " + ", ".join(f"{c} {O[c].isna().mean():.3f}" for c in fx.COLUMNS), flush=True)
    return pd.concat([data, O], axis=1)


def configs():
    v1 = rp.feature_list("entry", SYM)
    sets = {"v1": v1, "v1+A": v1 + fx.BLOCK_A, "v1+B": v1 + fx.BLOCK_B, "v1+A+B": v1 + fx.BLOCK_A + fx.BLOCK_B}
    out = [(s, "all", m, f) for s, f in sets.items() for m in ("logit", "gbm")]
    out += [(s, "cost_R<=0.15", m, sets[s]) for s in ("v1", "v1+A+B") for m in ("logit", "gbm")]
    return out


def one(data, fset, subset, model, feats):
    d = data if subset == "all" else data[data["cost_R"] <= 0.15]
    wait_mem(f"{fset} {subset} {model}")
    t0 = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = wf.walk_forward(d, feats, model=model, verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
    rt = time.time() - t0
    s = res.pooled
    params = dict(tf=TF, scope=SYM, model=model, feature_set=fset, subset=subset, n_features=len(feats),
                  blocks={"A": fx.BLOCK_A if "A" in fset else [], "B": fx.BLOCK_B if "B" in fset else []},
                  orientation="features_extra.orient_blocks before walk_forward (signed=features.SIGNED default)",
                  min_keep=rp.WF_KW["min_keep"], n_random=rp.N_RANDOM, seed=rp.SEED, **rp.wf_args("entry"))
    rp.log_trial(module="entry-features", scope=SYM, model=model, target="y_1.5", n_folds=int(s.n_folds),
                 oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                 oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                 oos_usd_per_trade=round(float(s.pnl_per_trade), 3), oos_usd_per_year=round(float(s.usd_per_year), 1),
                 baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(rt),
                 parameters=json.dumps(params), note=f"feature blocks A/B: {fset} on {subset}")
    rows = [dict(feature_set=fset, subset=subset, model=model, period="pooled", n_events=int(s.all_n),
                 auc=s.auc, logloss=s.logloss, brier=s.brier, kept=int(s.n_kept), keep_share=s.keep_share,
                 usd_trade=s.pnl_per_trade, total_usd=s.total_usd, usd_year=s.usd_per_year,
                 all_usd_trade=s.all_pnl_per_trade, random_usd_trade=s.random_pnl_per_trade,
                 random_p5=s.random_p5, random_p95=s.random_p95, runtime_s=round(rt))]
    for _, f in res.folds.iterrows():
        rows.append(dict(feature_set=fset, subset=subset, model=model, period=f["fold"], n_events=int(f["n_test"]),
                         auc=f["auc"], logloss=f["logloss"], brier=f["brier"], kept=int(f["n_kept"]),
                         keep_share=f["keep_share"], usd_trade=f["pnl_per_trade"], total_usd=f["total_usd"],
                         usd_year=f["usd_per_year"], all_usd_trade=f["all_pnl_per_trade"],
                         random_usd_trade=f["random_pnl_per_trade"], random_p5=f["random_p5"],
                         random_p95=f["random_p95"], runtime_s=np.nan))
    print(f"{fset:7s} {subset:12s} {model:5s}: auc {s.auc:.4f}  kept {int(s.n_kept):,}  $/tr {s.pnl_per_trade:.2f}  "
          f"all {s.all_pnl_per_trade:.2f}  random {s.random_pnl_per_trade:.2f}  $/yr {s.usd_per_year:.0f}  "
          f"({rt:.0f}s)", flush=True)
    return pd.DataFrame(rows)


def run_wf():
    data = joined()
    done = pd.read_csv(CSV) if os.path.exists(CSV) else pd.DataFrame(columns=["feature_set", "subset", "model"])
    have = set(zip(done.feature_set, done.subset, done.model))
    for fset, subset, model, feats in configs():
        if (fset, subset, model) in have:
            print(f"skip (done): {fset} {subset} {model}", flush=True)
            continue
        df = one(data, fset, subset, model, feats)
        done = pd.concat([done, df], ignore_index=True) if len(done) else df
        done.to_csv(CSV, index=False)


def _f(v, d=2):
    return "" if pd.isna(v) else f"{v:,.{d}f}"


def write_md():
    R = pd.read_csv(CSV)
    P = R[R.period == "pooled"]
    L = ["# Feature blocks A and B vs v1, MNQ 15-min entries (out of sample, 2013 - 2025H1)", "",
         "Net $ per trade = 1 MNQ micro after costs. 'all' = taking every event; 'random' = skipping events at random "
         "down to the same number of trades (mean of 200 draws). Holdout (2025-07+) untouched.", "",
         "## Pooled", "",
         "| set | subset | model | AUC | log loss | kept | $/trade | all $/tr | random $/tr | $/year | "
         "years better than v1 ($ total) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    Y = R[R.period != "pooled"]
    for _, r in P.iterrows():
        base = Y[(Y.feature_set == "v1") & (Y.subset == r.subset) & (Y.model == r.model)].set_index("period")
        me = Y[(Y.feature_set == r.feature_set) & (Y.subset == r.subset) & (Y.model == r.model)].set_index("period")
        if r.feature_set != "v1" and len(base):
            j = me.total_usd.to_frame("m").join(base.total_usd.to_frame("b"), how="inner")
            better = f"{int((j.m > j.b).sum())}/{len(j)} (worst year {_f(j.m.min(), 0)} vs {_f(j.b.min(), 0)})"
        else:
            better = "-"
        L.append(f"| {r.feature_set} | {r.subset} | {r.model} | {_f(r.auc, 4)} | {_f(r.logloss, 4)} | {int(r.kept):,} | "
                 f"{_f(r.usd_trade)} | {_f(r.all_usd_trade)} | {_f(r.random_usd_trade)} | {_f(r.usd_year, 0)} | {better} |")
    for subset in R.subset.unique():
        for model in ("logit", "gbm"):
            S = Y[(Y.subset == subset) & (Y.model == model)]
            if S.empty:
                continue
            L += ["", f"## By year: {model}, {subset} events ($/trade, kept trades in brackets)", ""]
            sets = [s for s in ("v1", "v1+A", "v1+B", "v1+A+B") if s in set(S.feature_set)]
            L.append("| year | all $/tr | " + " | ".join(sets) + " |")
            L.append("|---|---|" + "---|" * len(sets))
            for per in sorted(S.period.unique()):
                cells = []
                for s in sets:
                    x = S[(S.feature_set == s) & (S.period == per)]
                    cells.append(f"{_f(x.usd_trade.iloc[0])} ({int(x.kept.iloc[0]):,})" if len(x) else "")
                a = S[S.period == per].all_usd_trade.iloc[0]
                L.append(f"| {per} | {_f(a)} | " + " | ".join(cells) + " |")
    L += ["", "## Definitions (features_extra.py)", "",
          "R20 = mean (high - low) of the 20 bars before the signal bar, same contract (= entries R20, verified "
          "bit-identical). Block A: retN = (close now - close N bars ago) / R20, N = 1, 2, 3, 5, 10, 20; "
          "ret60_volscaled = (close now - close 60 bars ago) / (R20 x sqrt 60). Block B: rsvN = where the close sits in "
          "the high-low range of the last N bars (0 = at the low, 1 = at the high), N = 5, 20, 60; prev_close_rsv20 = "
          "rsv20 one bar earlier; bars_since_high/lowN = bars since the most recent bar that made the N-bar high/low, "
          "divided by N (N = 20, 60); range20_width = 20-bar high-low range / R20. All oriented to the trade: shorts "
          "get returns x -1, rsv -> 1 - rsv, bars_since_high <-> bars_since_low."]
    open(MD, "w").write("\n".join(L) + "\n")
    print(f"wrote {MD}", flush=True)


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("build", "all") and not os.path.exists(BLK):
        build()
    if stage in ("wf", "all"):
        run_wf()
    if stage in ("md", "wf", "all"):
        write_md()
