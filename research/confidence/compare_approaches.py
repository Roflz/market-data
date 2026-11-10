"""
Compare every published weighting approach (approaches/: hand-set, statistical, ML, prior-started ML) with our
vote / logit / gbm on the SAME entry events, folds, thresholds rule and $ scoring (walkforward.walk_forward).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 compare_approaches.py SCOPE GROUP
  SCOPE: NQ | ES | YM | pooled      GROUP: hand | stat | ml | prior | one scorer spec like "sc:stat_nb_woe"
One CSV per scorer: out/approach_<scope>_<spec>.csv (pooled out-of-sample row); trials logged to out/trials.csv.
"""
import sys
import time
import traceback
import warnings

import pandas as pd

import run_pipeline as rp
import walkforward as wf

warnings.filterwarnings("ignore")
SCOPE, GROUP = sys.argv[1], sys.argv[2]
GROUPS = {
    "hand": ["sc:hand_bulkowski", "sc:hand_morris_woe", "sc:hand_ndr_composite", "sc:hand_user"],
    "stat": ["sc:stat_nb_woe", "sc:stat_woe_scorecard", "sc:stat_shrink_combo", "sc:stat_screen_nb",
             "sc:stat_screen_sa", "sc:stat_screen_rvm", "sc:stat_screen_dma", "sc:stat_screen_dms",
             "sc:stat_screen_bma", "sc:stat_screen_bnn"],
    "ml": ["sc:ml_logit_l2", "sc:ml_creamer_boost", "sc:ml_creamer_experts", "sc:ml_afml_rf|max_rows=150000"],
    "prior": [f"sc:{m}|prior={p}" for p in ("hand_bulkowski", "stat_nb_woe")
              for m in ("prior_logit_offset", "prior_logit_shrink", "prior_gbm")],
}
specs = GROUPS.get(GROUP, [GROUP])
data = rp.load("entry", SCOPE)
feats = rp.feature_list("entry", SCOPE)
for spec in specs:
    t0 = time.time()
    tag = spec[3:].replace("|", "_").replace("=", "-")
    try:
        res = wf.walk_forward(data, feats, model=spec, verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
    except Exception as e:
        print(f"{spec}: FAILED {type(e).__name__}: {str(e)[:200]}", flush=True)
        traceback.print_exc(limit=2)
        continue
    rt = time.time() - t0
    P = res.pooled.to_frame().T
    P.insert(0, "model", spec); P.insert(0, "scope", SCOPE)
    P["runtime_s"] = round(rt)
    P.to_csv(f"out/approach_{SCOPE}_{tag}.csv", index=False)
    res.folds.assign(model=spec, scope=SCOPE).to_csv(f"out/approach_folds_{SCOPE}_{tag}.csv", index=False)
    s = res.pooled
    rp.log_trial(module="entry-approach", scope=SCOPE, model=spec, target=f"y_{rp.PRIMARY_R}", n_folds=int(s.n_folds),
                 oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                 oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                 oos_usd_per_trade=round(float(s.pnl_per_trade), 3), oos_usd_per_year=round(float(s.usd_per_year), 1),
                 baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(rt),
                 parameters=spec, note="approach comparison")
    print(f"{spec}: AUC {s.auc:.3f}  kept {int(s.n_kept):,} ({s.keep_share:.1%})  {s.pnl_per_trade:+.2f} $/trade  "
          f"all {s.all_pnl_per_trade:+.2f}  random {s.random_pnl_per_trade:+.2f}  ({rt:.0f}s)", flush=True)
