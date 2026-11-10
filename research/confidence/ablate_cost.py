"""MNQ entry logit/gbm without the planned-risk features (stop_R20, cost_R): how much signal is left beyond
'skip trades whose stop is too tight for the costs'? Also the same models on events with a sane stop only."""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import run_pipeline as rp
import walkforward as wf
data = rp.load("entry", "NQ")
feats = rp.feature_list("entry", "NQ")
no_cost = [f for f in feats if f not in ("stop_R20", "cost_R")]
sane = data[data["cost_R"] <= 0.15].copy()          # cost at most 15% of the planned risk
rows = []
for name, d, f in (("all events, no stop/cost features", data, no_cost),
                   ("cost<=15% of risk, all features", sane, feats),
                   ("cost<=15% of risk, no stop/cost features", sane, no_cost)):
    for m in ("logit", "gbm"):
        r = wf.walk_forward(d, f, model=m, verbose=False, **rp.wf_args("entry"), **rp.WF_KW).pooled
        rows.append(dict(test=name, model=m, n_events=int(r.all_n), auc=round(r.auc, 3), kept=int(r.n_kept),
                         usd_trade=round(r.pnl_per_trade, 2), all_usd_trade=round(r.all_pnl_per_trade, 2),
                         random_usd_trade=round(r.random_pnl_per_trade, 2), usd_year=round(r.usd_per_year)))
        print(rows[-1], flush=True)
        rp.log_trial(module="entry-ablation", scope="NQ", model=m, target="y_1.5", n_folds=int(r.n_folds),
                     oos_rows=int(r.all_n), oos_auc=round(float(r.auc), 4), oos_kept=int(r.n_kept),
                     oos_keep_share=round(float(r.keep_share), 4), oos_usd_total=round(float(r.total_usd), 2),
                     oos_usd_per_trade=round(float(r.pnl_per_trade), 3), oos_usd_per_year=round(float(r.usd_per_year), 1),
                     baseline_usd_per_trade=round(float(r.all_pnl_per_trade), 3), runtime_s=0, parameters=name,
                     note="cost-feature ablation")
pd.DataFrame(rows).to_csv("out/ablation_cost_NQ.csv", index=False)
