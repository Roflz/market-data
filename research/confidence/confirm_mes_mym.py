"""Quick confirmation on MES / MYM of the two MNQ leads, on recent data only (faster):
  (1) candle signals whose pattern stop leaves costs <= 15% of risk, logit filter
  (2) H1/H2 pullback entries, pullback-low stop, logit filter
Data from 2013 (ES) / 2018 (YM); test years 2016.. / 2021.. to 2025H1 (holdout untouched). Logit only.
  python3 confirm_mes_mym.py ES   (or YM)"""
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
SYM = sys.argv[1]
t0 = time.time()
START = pd.Timestamp("2013-01-01")
folds = wf.make_folds(test_years=range(2016 if SYM != "YM" else 2021, 2025))
rows = []


def run(name, d, feats):
    res = wf.walk_forward(d, feats, model="logit", folds=folds, verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
    s = res.pooled
    r = dict(market=SYM, test=name, n_test=int(s.all_n), auc=round(s.auc, 3), kept=int(s.n_kept),
             usd_trade=round(s.pnl_per_trade, 2), all_usd_trade=round(s.all_pnl_per_trade, 2),
             random_usd_trade=round(s.random_pnl_per_trade, 2), usd_year=round(s.usd_per_year))
    yr = res.folds[["fold", "n_kept", "pnl_per_trade"]].round(2)
    r["by_year"] = "; ".join(f"{a}:{c:+.2f}({b})" for a, b, c in yr.itertuples(index=False))
    rows.append(r)
    rp.log_trial(module="entry-confirm", scope=SYM, model="logit", target="y_1.5", n_folds=int(s.n_folds),
                 oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                 oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                 oos_usd_per_trade=round(float(s.pnl_per_trade), 3), oos_usd_per_year=round(float(s.usd_per_year), 1),
                 baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(time.time() - t0),
                 parameters=name, note="quick MES/MYM confirmation, recent data")
    print(r, flush=True)


# (1) cost <= 15% candle signals
E = rp.load("entry", SYM)
E = E[(pd.DatetimeIndex(E.t) >= START) & (E.cost_R <= 0.15)].reset_index(drop=True)
run("candles, cost<=15% of risk", E, rp.feature_list("entry", SYM))
del E

# (2) H1/H2 with the pullback-low stop
spec = sg.SPEC[SYM]
b, F = fe.build_features(SYM, 15, others=rp.MARKETS)
b, F = rp.holdout_cut(b, F)
ctx = sg.context(b, tick=spec["tick"])
ev = h1h2.detect(b, ctx, spec["tick"], 15, k=5)
ev = ev[ev.t >= START].reset_index(drop=True)
m1 = lb.load_1m(SYM); m1 = m1.loc[(m1.index < wf.HOLDOUT_SESSION_START) & (m1.index >= START - pd.Timedelta(days=5))]
L = h1h2.label_stop_entries(SYM, 15, b, ev, target_R=rp.TARGET_R, max_bars=rp.MAX_BARS_ENTRY, m1=m1, stop_col="stop")
del m1
i = L["i"].to_numpy()
L["session"] = wf.session_label(L["t"]); L["R20"] = b["R20"].to_numpy(np.float64)[i]
L["stop"] = L["stop_used"]; L["stop_R20"], L["cost_R"] = rp.entry_trade_features(b, L, SYM)
for a in (1, 2):
    L[f"att_{a}"] = (L.attempt == a).astype(np.float32)
L["att_3plus"] = (L.attempt >= 3).astype(np.float32)
L = pd.concat([L.reset_index(drop=True), F.iloc[i].reset_index(drop=True)], axis=1)
print(f"H1/H2 {SYM}: {len(L):,} triggered trades; unfiltered $/trade {L['pnl_usd_1.5'].mean():+.2f}", flush=True)
run("H1/H2, pullback-low stop", L, rp.feature_list("entry", SYM) + ["att_1", "att_2", "att_3plus", "depth", "bars_pb"])
pd.DataFrame(rows).to_csv(f"out/confirm_{SYM}.csv", index=False)
print(f"done in {time.time() - t0:.0f}s")
