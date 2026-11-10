"""
Compare stop options (out/stops_<SYM>_15.parquet from stop_options.py) for the same entry events:
  1) every event taken: $ per trade (target 1 / 1.5 / 2 R), hit rate, stopped share, median risk $, by year
  2) model-filtered: the v1 logit walk-forward (same features from out/entries_<SYM>_15.parquet, with stop_R20 and
     cost_R recomputed for THIS stop) -> out-of-sample $ per trade on the kept trades, vs all and random skip.
Events dated in the locked holdout are never present (the entries were cut before it).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 compare_stops.py NQ [--no-model]
Writes out/stops_compare_<SYM>.csv and out/stops_by_year_<SYM>.csv
"""
import gc
import sys
import warnings

import numpy as np
import pandas as pd

import run_pipeline as rp
import signals as sg
import walkforward as wf

warnings.filterwarnings("ignore")
SYM = sys.argv[1] if len(sys.argv) > 1 else "NQ"
MODEL = "--no-model" not in sys.argv
spec = sg.SPEC[SYM]; USD, COST = spec["usd"], spec["cost"]
S = pd.read_parquet(f"out/stops_{SYM}_15.parquet")
C = sg.bars(SYM, 15).C.to_numpy()
feats = rp.feature_list("entry", SYM)
if MODEL:
    E = rp.load("entry", SYM)
    drop = [c for c in E.columns if c.startswith(("pnl_usd_", "y_", "exit_kind_", "t_end_", "target_", "exit_px_"))]
    E = E.drop(columns=drop + ["risk_pts", "risk_usd", "past_stop", "stop", "stop_R20", "cost_R", "t_entry", "entry",
                               "patterns", "n_patterns", "market"], errors="ignore")

rows, yrs = [], []
for opt, g in S.groupby("stop_option", sort=False):
    r = dict(stop_option=opt, n=len(g), median_risk_usd=g.risk_usd.median(), mean_risk_usd=g.risk_usd.mean())
    for R in ("1", "1.5", "2"):
        r[f"usd_trade_{R}R"] = g[f"pnl_usd_{R}"].mean()
    r["hit_1.5R"] = g["y_1.5"].mean()
    r["stopped_1.5R"] = (g["exit_kind_1.5"] == "stop").mean()
    r["time_exit_1.5R"] = (g["exit_kind_1.5"] == "time").mean()
    for yr, gg in g.groupby(pd.DatetimeIndex(g.t).year):
        yrs.append(dict(stop_option=opt, year=yr, n=len(gg), usd_trade=gg["pnl_usd_1.5"].mean()))
    if MODEL:
        lab_cols = [c for c in g.columns if c.startswith(("pnl_usd_", "y_", "exit_kind_", "t_end_"))] + ["stop", "market"]
        d = g[["i", "d", "t"] + lab_cols].merge(E.drop(columns=["t"]), on=["i", "d"], how="inner")
        dist = d["d"].to_numpy() * (C[d.i.to_numpy()] - d["stop"].to_numpy())          # signal close -> stop, pts
        d["stop_R20"] = dist / d["R20"].to_numpy()
        d["cost_R"] = COST / np.maximum(dist * USD, 1e-9)
        res = wf.walk_forward(d, feats, model="logit", verbose=False, **rp.wf_args("entry"), **rp.WF_KW).pooled
        r.update(model_auc=res.auc, model_kept=res.n_kept, model_keep_share=res.keep_share,
                 model_usd_trade=res.pnl_per_trade, model_usd_year=res.usd_per_year,
                 oos_all_usd_trade=res.all_pnl_per_trade, oos_random_usd_trade=res.random_pnl_per_trade)
        rp.log_trial(module="entry-stop-option", scope=SYM, model="logit", target="y_1.5", n_folds=int(res.n_folds),
                     oos_rows=int(res.all_n), oos_auc=round(float(res.auc), 4), oos_kept=int(res.n_kept),
                     oos_keep_share=round(float(res.keep_share), 4), oos_usd_total=round(float(res.total_usd), 2),
                     oos_usd_per_trade=round(float(res.pnl_per_trade), 3),
                     oos_usd_per_year=round(float(res.usd_per_year), 1),
                     baseline_usd_per_trade=round(float(res.all_pnl_per_trade), 3), runtime_s=0,
                     parameters=f"stop_option={opt}", note="stop option comparison")
        del d; gc.collect()
    rows.append(r)
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
pd.DataFrame(rows).to_csv(f"out/stops_compare_{SYM}.csv", index=False)
pd.DataFrame(yrs).pivot(index="year", columns="stop_option", values="usd_trade").to_csv(f"out/stops_by_year_{SYM}.csv")
