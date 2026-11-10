"""
Structure triggers (BOS / CHoCH / level reclaim, structure_triggers.py) on real data: detect -> next-bar-open entries
labelled on the 1-minute path (labels.label_entries, targets 1 / 1.5 / 2 R, 16-bar limit) -> v1 features at the
signal bar + trigger one-hots -> unfiltered $ per trigger (and by year) -> logit / gbm walk-forward on all triggers
together (same folds, purge, threshold and baselines as v1), with the kept trades broken down by trigger and year.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 run_structure.py NQ [--reuse]
Writes out/structure_<SYM>_15.parquet, out/structure_<SYM>_models.csv, out/structure_<SYM>_summary.csv,
out/structure_<SYM>_by_year.csv, out/structure_<SYM>_folds.csv. --reuse skips detection/labelling if the parquet exists.
"""
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

import run_pipeline as rp
import walkforward as wf

warnings.filterwarnings("ignore")
SYM = next((a for a in sys.argv[1:] if not a.startswith("--")), "NQ")
REUSE = "--reuse" in sys.argv
TF = 15
K = 5
OUT = f"out/structure_{SYM}"
PQ = f"{OUT}_{TF}.parquet"
ONEHOT = ["trg_bos", "trg_choch", "trg_reclaim"]
t0 = time.time()


def build():
    import features as fe
    import labels as lb
    import signals as sg
    import structure_triggers as st
    spec = sg.SPEC[SYM]
    b, F = fe.build_features(SYM, TF, others=rp.MARKETS)
    b, F = rp.holdout_cut(b, F)
    ev = st.detect(b, spec["tick"], TF, k=K)
    print(f"{SYM}: {len(b):,} bars, {len(ev):,} structure events ({time.time() - t0:.0f}s)", flush=True)
    print(ev.groupby(["trigger", "d"]).size().to_string(), flush=True)
    m1 = lb.load_1m(SYM); m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
    L = lb.label_entries(SYM, TF, b, ev, target_R=rp.TARGET_R, max_bars=rp.MAX_BARS_ENTRY, m1=m1)
    del m1
    L["patterns"] = L["patterns"].map("|".join)
    i = L["i"].to_numpy()
    L["session"] = wf.session_label(L["t"])
    L["R20"] = b["R20"].to_numpy(np.float64)[i]
    L["stop_R20"], L["cost_R"] = rp.entry_trade_features(b, L, SYM)
    L = L.reset_index(drop=True)
    L = pd.concat([L, st.one_hots(L), F.iloc[i].reset_index(drop=True)], axis=1)
    L.to_parquet(PQ, compression="zstd")
    print(f"saved {len(L):,} labelled trades to {PQ} ({time.time() - t0:.0f}s)", flush=True)
    return L


L = pd.read_parquet(PQ) if (REUSE and os.path.exists(PQ)) else build()
L["year"] = pd.DatetimeIndex(L["session"]).year

# ---- unfiltered (no model): every event of each trigger, all pre-holdout years and the walk-forward test span
def agg(g):
    return pd.Series(dict(n=len(g), usd_1R=g["pnl_usd_1"].mean(), usd_15R=g["pnl_usd_1.5"].mean(),
                          usd_2R=g["pnl_usd_2"].mean(), hit_15R=g["y_1.5"].mean(),
                          risk_usd_med=g["risk_usd"].median(), past_stop=g["past_stop"].mean(),
                          usd_year_15R=g["pnl_usd_1.5"].sum() / max(g["year"].nunique(), 1)))
rows = []
for span, m in (("2010-2025H1", np.ones(len(L), bool)), ("2013-2025H1 (WF test span)", L["t"] >= "2013-01-01")):
    for (trg, d), g in L[m].groupby(["trigger", "d"]):
        rows.append(dict(span=span, trigger=trg, side="long" if d > 0 else "short", **agg(g)))
    for trg, g in L[m].groupby("trigger"):
        rows.append(dict(span=span, trigger=trg, side="both", **agg(g)))
    rows.append(dict(span=span, trigger="all", side="both", **agg(L[m])))
S = pd.DataFrame(rows)
S.to_csv(f"{OUT}_summary.csv", index=False)
print("\nUNFILTERED $ per trade per 1 MNQ after costs\n" + S.round(2).to_string(index=False), flush=True)
Y = L.pivot_table(index="year", columns="trigger", values="pnl_usd_1.5", aggfunc="mean")
Y["all"] = L.groupby("year")["pnl_usd_1.5"].mean()
Yn = L.pivot_table(index="year", columns="trigger", values="pnl_usd_1.5", aggfunc="size").add_prefix("n_")
print("\nUNFILTERED by year, $/trade at 1.5R\n" + pd.concat([Y, Yn], axis=1).round(2).to_string(), flush=True)

# ---- walk-forward: all triggers together, trigger one-hots as features
feats = rp.feature_list("entry", SYM) + ONEHOT
models, folds, years = [], [], []
for m in ("logit", "gbm"):
    t1 = time.time()
    res = wf.walk_forward(L, feats, model=m, verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
    s = res.pooled
    models.append(dict(model=m, trigger="all", n_oos=int(s.all_n), auc=s.auc, kept=int(s.n_kept),
                       keep_share=s.keep_share, usd_trade=s.pnl_per_trade, usd_year=s.usd_per_year,
                       hit=s.get("hit_rate", np.nan), all_usd_trade=s.all_pnl_per_trade, random_usd_trade=s.random_pnl_per_trade,
                       vote_topN_usd_trade=s.get("vote_topN_pnl_per_trade", np.nan)))
    O = res.oos.join(L[["trigger", "year"]])
    for trg, g in O.groupby("trigger"):
        k = g[g["take"].astype(bool)]
        models.append(dict(model=m, trigger=trg, n_oos=len(g), kept=len(k), keep_share=len(k) / len(g),
                           usd_trade=k.pnl.mean() if len(k) else np.nan, hit=(k.pnl > 0).mean() if len(k) else np.nan,
                           all_usd_trade=g.pnl.mean()))
    folds.append(res.folds.assign(model=m))
    yy = O.groupby("year").apply(lambda g: pd.Series(dict(
        n=len(g), kept=int(g["take"].sum()), usd_trade_kept=g.loc[g["take"].astype(bool), "pnl"].mean(),
        usd_kept_total=g.loc[g["take"].astype(bool), "pnl"].sum(), all_usd_trade=g.pnl.mean(),
        all_total=g.pnl.sum())))
    years.append(yy.assign(model=m).reset_index())
    rp.log_trial(module="entry-structure", scope=SYM, model=m, target="y_1.5", n_folds=int(s.n_folds),
                 oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                 oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                 oos_usd_per_trade=round(float(s.pnl_per_trade), 3), oos_usd_per_year=round(float(s.usd_per_year), 1),
                 baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(time.time() - t1),
                 parameters=f"structure triggers bos/choch/reclaim k={K}, next-bar-open, stop as defined, "
                            f"targets {list(rp.TARGET_R)} max_bars {rp.MAX_BARS_ENTRY}, v1 features + trigger one-hots",
                 note="structure triggers (BOS / CHoCH / reclaim) pooled with one-hots")
    print(f"\n{m}: " + str({k_: (round(v, 3) if isinstance(v, float) else v) for k_, v in models[-4].items()}),
          flush=True)
M = pd.DataFrame(models)
M.to_csv(f"{OUT}_models.csv", index=False)
FD = pd.concat(folds, ignore_index=True)
FD.to_csv(f"{OUT}_folds.csv", index=False)
YY = pd.concat(years, ignore_index=True)
YY.to_csv(f"{OUT}_by_year.csv", index=False)
print("\nMODELS (OOS, $/trade per 1 MNQ after costs)\n" + M.round(3).to_string(index=False))
print("\nFOLDS\n" + FD[["model", "fold", "auc", "n_test", "n_kept", "pnl_per_trade", "all_pnl_per_trade",
                        "random_pnl_per_trade", "random_p5", "random_p95", "total_usd"]].round(2).to_string(index=False))
print(f"done in {time.time() - t0:.0f}s")
