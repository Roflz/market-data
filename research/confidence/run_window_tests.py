"""Does training on recent years help? v1 entry logit per market with
  expanding (all years since 2010, the v1 default), rolling 3 / 5 years, time-decay half-life 2 / 4 years.
Out of sample 2013..2025H1 (and the 2019+ part, the years micro contracts exist), net $ per micro after costs.
Writes out/window_tests.csv (pooled + 2019+ per market x config) and out/window_folds.csv (by year).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 -u run_window_tests.py [NQ ES YM]
"""
import sys
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import run_pipeline as rp
import walkforward as wf

CONFIGS = {"expanding": {}, "rolling 3y": dict(train_years=3), "rolling 5y": dict(train_years=5),
           "decay 2y": dict(decay_half_life=2.0), "decay 4y": dict(decay_half_life=4.0)}


def part(folds, start):
    f = folds[pd.to_datetime(folds.test_start) >= pd.Timestamp(start)]
    n = f.n_kept.sum()
    tot = (f.pnl_per_trade.fillna(0) * f.n_kept).sum()
    yrs = f.years.sum()
    allp = (f.all_pnl_per_trade * f.n_test).sum() / f.n_test.sum()
    pos = int((f.pnl_per_trade * f.n_kept > 0).sum())
    return dict(kept=int(n), usd_trade=tot / n if n else np.nan, total_usd=tot, usd_year=tot / yrs,
                all_usd_trade=allp, years_positive=f"{pos}/{len(f)}")


def main(markets):
    rows, folds_all = [], []
    for m in markets:
        t0 = time.time()
        data = rp.load("entry", m)
        feats = rp.feature_list("entry", m)
        print(f"{m}: {len(data):,} events, {len(feats)} features ({time.time() - t0:.0f}s)", flush=True)
        for name, kw in CONFIGS.items():
            t1 = time.time()
            r = wf.walk_forward(data, feats, model="logit", verbose=False, **kw, **rp.wf_args("entry"), **rp.WF_KW)
            F = r.folds.assign(market=m, config=name)
            folds_all.append(F)
            P = r.pooled
            for span, start in (("2013-2025H1", "2013-01-01"), ("2019-2025H1", "2019-01-01")):
                row = dict(market=m, config=name, span=span, **part(r.folds, start))
                if span.startswith("2013"):
                    row.update(auc=round(float(P.auc), 4), random_usd_trade=round(float(P.random_pnl_per_trade), 3))
                rows.append(row)
            print(f"  {name:11s} all years {rows[-2]['usd_trade']:+.2f} $/tr ({rows[-2]['kept']:,} kept, "
                  f"{rows[-2]['years_positive']} yrs +)   2019+ {rows[-1]['usd_trade']:+.2f} $/tr "
                  f"({rows[-1]['kept']:,} kept, {rows[-1]['years_positive']} yrs +)  ({time.time() - t1:.0f}s)",
                  flush=True)
            rp.log_trial(module="entry-window", scope=m, model="logit", target="y_1.5", n_folds=int(P.n_folds),
                         oos_rows=int(P.all_n), oos_auc=round(float(P.auc), 4), oos_kept=int(P.n_kept),
                         oos_keep_share=round(float(P.keep_share), 4), oos_usd_total=round(float(P.total_usd), 2),
                         oos_usd_per_trade=round(float(P.pnl_per_trade), 3),
                         oos_usd_per_year=round(float(P.usd_per_year), 1),
                         baseline_usd_per_trade=round(float(P.all_pnl_per_trade), 3),
                         runtime_s=round(time.time() - t1), parameters=f"training window: {name} {kw}",
                         note="rolling window / time decay test")
            pd.DataFrame(rows).to_csv("out/window_tests.csv", index=False)
            pd.concat(folds_all).to_csv("out/window_folds.csv", index=False)
        del data
    print("done", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["NQ", "ES", "YM"])
