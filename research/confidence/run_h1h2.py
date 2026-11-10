"""
H1/H2 pullback entries on real data: detect -> stop-order fills + labels on the 1-minute path -> v1 features at the
signal bar + trigger features -> unfiltered results by attempt -> logit / gbm walk-forward (same folds and $ rules).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 run_h1h2.py NQ
Writes out/h1h2_<SYM>_15.parquet, out/h1h2_<SYM>_summary.csv, out/h1h2_<SYM>_models.csv
"""
import sys
import time
import warnings

import numpy as np
import pandas as pd

import features as fe
import h1h2
import labels as lb
import run_pipeline as rp
import signals as sg
import walkforward as wf

warnings.filterwarnings("ignore")
SYM = sys.argv[1] if len(sys.argv) > 1 else "NQ"
TF = 15
t0 = time.time()
spec = sg.SPEC[SYM]
b, F = fe.build_features(SYM, TF, others=rp.MARKETS)
b, F = rp.holdout_cut(b, F)
ctx = sg.context(b, tick=spec["tick"])
ev = h1h2.detect(b, ctx, spec["tick"], TF, k=5)
print(f"{SYM}: {len(ev):,} pending H/L orders ({time.time() - t0:.0f}s)", flush=True)
m1 = lb.load_1m(SYM); m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
parts = []
for stop_col in ("stop", "stop_sig"):
    lab = h1h2.label_stop_entries(SYM, TF, b, ev, target_R=rp.TARGET_R, max_bars=rp.MAX_BARS_ENTRY, m1=m1,
                                  stop_col=stop_col)
    print(f"  stop={stop_col}: {lab.attrs['n_triggered']:,} of {lab.attrs['n_orders']:,} orders triggered", flush=True)
    lab["stop_kind"] = stop_col
    parts.append(lab)
del m1
L = pd.concat(parts, ignore_index=True)
i = L["i"].to_numpy()
L["session"] = wf.session_label(L["t"])
L["R20"] = b["R20"].to_numpy(np.float64)[i]
L["stop"] = L["stop_used"]
L["stop_R20"], L["cost_R"] = rp.entry_trade_features(b, L, SYM)
for a in (1, 2):
    L[f"att_{a}"] = (L.attempt == a).astype(np.float32)
L["att_3plus"] = (L.attempt >= 3).astype(np.float32)
L = pd.concat([L.reset_index(drop=True), F.iloc[i].reset_index(drop=True)], axis=1)
L.to_parquet(f"out/h1h2_{SYM}_{TF}.parquet", compression="zstd")
print(f"saved {len(L):,} labelled trades ({time.time() - t0:.0f}s)", flush=True)

# unfiltered: by stop kind x attempt (all years before the holdout)
S = (L.assign(att=np.where(L.attempt >= 3, "3+", L.attempt.astype(str)))
     .groupby(["stop_kind", "att"]).agg(n=("pnl_usd_1.5", "size"), usd_trade=("pnl_usd_1.5", "mean"),
                                       hit=("y_1.5", "mean"), usd_1R=("pnl_usd_1", "mean"), usd_2R=("pnl_usd_2", "mean"),
                                       risk_usd=("risk_usd", "median")).reset_index())
S.to_csv(f"out/h1h2_{SYM}_summary.csv", index=False)
print(S.round(2).to_string(index=False), flush=True)

feats = rp.feature_list("entry", SYM) + ["att_1", "att_2", "att_3plus", "depth", "bars_pb"]
rows = []
for stop_col in ("stop", "stop_sig"):
    d = L[L.stop_kind == stop_col].reset_index(drop=True)
    for m in ("logit", "gbm"):
        # the v1 defaults (gbm leaf >= 500 rows, inner sets >= 200 rows) are sized for ~300k events; with ~4k H1/H2
        # trades the gbm could not split in its early folds (took every trade) and the logit skipped 2013, so the two
        # were scored on different years. Scale both down so the models can fit and cover the same test years.
        res = wf.walk_forward(d, feats, model=m, verbose=False, min_inner=100,
                              gbm_params=dict(wf.GBM_PARAMS, min_samples_leaf=50),
                              **rp.wf_args("entry"), **rp.WF_KW)
        s = res.pooled
        r = dict(stop_kind=stop_col, model=m, n=int(s.all_n), auc=s.auc, kept=int(s.n_kept), keep_share=s.keep_share,
                 usd_trade=s.pnl_per_trade, usd_year=s.usd_per_year, all_usd_trade=s.all_pnl_per_trade,
                 random_usd_trade=s.random_pnl_per_trade)
        rows.append(r)
        res.folds.assign(stop_kind=stop_col, model=m).to_csv(f"out/h1h2_{SYM}_folds_{stop_col}_{m}.csv", index=False)
        rp.log_trial(module="entry-h1h2", scope=SYM, model=m, target="y_1.5", n_folds=int(s.n_folds),
                     oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                     oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                     oos_usd_per_trade=round(float(s.pnl_per_trade), 3), oos_usd_per_year=round(float(s.usd_per_year), 1),
                     baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(time.time() - t0),
                     parameters=f"H1/H2 stop={stop_col}, entry slips 1 tick, min_inner=100, gbm leaf=50", note="H1/H2 stop-order entries")
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
pd.DataFrame(rows).to_csv(f"out/h1h2_{SYM}_models.csv", index=False)
print(f"done in {time.time() - t0:.0f}s")
