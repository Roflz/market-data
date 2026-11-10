"""Year by year: MNQ entry models on the 'cost <= 15% of the planned risk' signals (the stop/cost test's best lead).
Also the same with the labels shuffled within each year (5 shuffles) as a luck check."""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import run_pipeline as rp
import walkforward as wf
data = rp.load("entry", "NQ")
feats = rp.feature_list("entry", "NQ")
sane = data[data["cost_R"] <= 0.15].copy()
out = []
for m in ("gbm", "logit"):
    res = wf.walk_forward(sane, feats, model=m, verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
    F = res.folds
    cols = [c for c in ("fold", "n_test", "auc", "n_kept", "keep_share", "pnl_per_trade", "total_usd", "hit_rate",
                        "all_pnl_per_trade", "random_pnl_per_trade", "random_p5", "random_p95") if c in F.columns]
    F = F[cols].assign(model=m)
    out.append(F)
    print(m, "pooled:", round(res.pooled.pnl_per_trade, 2), "$/trade,", int(res.pooled.n_kept), "kept", flush=True)
    print(F.round(3).to_string(index=False), flush=True)
    perm = []
    for k in range(5):
        r = wf.walk_forward(sane, feats, model=m, verbose=False, shuffle_rng=np.random.default_rng(100 + k),
                            **rp.wf_args("entry"), **rp.WF_KW).pooled
        perm.append(r.pnl_per_trade)
    print(m, "shuffled-label $/trade:", [round(x, 2) for x in perm], flush=True)
pd.concat(out).to_csv("out/sane_by_year_NQ.csv", index=False)
