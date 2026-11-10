"""Can MES / MYM work on bigger charts? Costs are ~15% of a 15-min bar on MES/MYM vs ~5% on MNQ.
For ES and YM at 15 / 60 / 120 minutes (and NQ 15 for reference): the v1 entry logit, with and without the new
cost_bar input (cost / average bar in $). Builds out/entries_{ES,YM}_{60,120}.parquet if missing (entries only).
Same v1 rules: pattern stop, 1.5R target, 16-bar limit / 16:45 flat, costs, expanding walk-forward 2013..2025H1.
Writes out/bigger_charts.csv (pooled + 2019+) and out/bigger_charts_folds.csv.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 -u run_bigger_charts.py
"""
import gc
import os
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import features as fe
import run_pipeline as rp
import signals as sg
import walkforward as wf
from run_window_tests import part

RUNS = [("NQ", 15), ("ES", 15), ("ES", 60), ("ES", 120), ("YM", 15), ("YM", 60), ("YM", 120)]


def main():
    rows, folds_all = [], []
    for sym, tf in RUNS:
        t0 = time.time()
        path = rp._path(f"entries_{sym}_{tf}.parquet")
        if not os.path.exists(path):
            rp.build_entries(sym, tf).to_parquet(path, compression="zstd")
            fe.clear_cache(); gc.collect()
        data = rp.add_cost_bar(rp.load("entry", sym, tf=tf))
        cb = data.groupby(pd.DatetimeIndex(data["t"]).year)["cost_bar"].median()
        print(f"{sym} {tf}m: {len(data):,} events; cost as share of an average bar: "
              + " ".join(f"{y}:{v:.0%}" for y, v in cb.items() if y in (2013, 2016, 2019, 2022, 2024, 2025)),
              flush=True)
        base = rp.feature_list("entry", sym)
        for name, feats in (("v1", base), ("v1 + cost_bar", base + ["cost_bar"])):
            t1 = time.time()
            r = wf.walk_forward(data, feats, model="logit", verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
            folds_all.append(r.folds.assign(market=sym, tf=tf, config=name))
            P = r.pooled
            for span, start in (("2013-2025H1", "2013-01-01"), ("2019-2025H1", "2019-01-01")):
                row = dict(market=sym, tf=tf, config=name, span=span, events=int(P.all_n),
                           cost_share_2024=round(float(cb.get(2024, np.nan)), 3), **part(r.folds, start))
                if span.startswith("2013"):
                    row.update(auc=round(float(P.auc), 4), random_usd_trade=round(float(P.random_pnl_per_trade), 3))
                rows.append(row)
            print(f"  {name:14s} all years {rows[-2]['usd_trade']:+.2f} $/tr ({rows[-2]['kept']:,} kept, "
                  f"{rows[-2]['years_positive']} yrs +; every signal {rows[-2]['all_usd_trade']:+.2f})   "
                  f"2019+ {rows[-1]['usd_trade']:+.2f} $/tr ({rows[-1]['kept']:,} kept)  ({time.time() - t1:.0f}s)",
                  flush=True)
            rp.log_trial(module="entry-bigger-charts", scope=sym, model="logit", target="y_1.5",
                         n_folds=int(P.n_folds), oos_rows=int(P.all_n), oos_auc=round(float(P.auc), 4),
                         oos_kept=int(P.n_kept), oos_keep_share=round(float(P.keep_share), 4),
                         oos_usd_total=round(float(P.total_usd), 2), oos_usd_per_trade=round(float(P.pnl_per_trade), 3),
                         oos_usd_per_year=round(float(P.usd_per_year), 1),
                         baseline_usd_per_trade=round(float(P.all_pnl_per_trade), 3),
                         runtime_s=round(time.time() - t1), parameters=f"tf={tf} features={name}",
                         note="MES/MYM on bigger charts + cost_bar")
            pd.DataFrame(rows).to_csv("out/bigger_charts.csv", index=False)
            pd.concat(folds_all).to_csv("out/bigger_charts_folds.csv", index=False)
        del data; gc.collect()
    print("done", flush=True)


if __name__ == "__main__":
    main()
