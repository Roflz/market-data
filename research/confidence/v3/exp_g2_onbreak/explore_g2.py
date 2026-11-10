"""
EXPLORATORY (not pre-registered; Tier B at best; logged as trials 'v3-G2X-*'). Light (v3/data only).
1) Mechanism decomposition of A2 on MNQ: is it the break, or the trend filter?
   X-none   : first overnight-range break per side, NO trend filter
   X-against: first break only when the 20-day trend DISAGREES (the complement of A2)
2) Fill-convention check: A2 with the stop snapped to the tick grid away from the entry (real stop orders).
3) Eval (descriptive): A2 with stop-based risk sizing ('risk', $) vs the same sizing on 200 C1 twins (k = 2 seeds,
   identical to the A2 run), 40% and 50% consistency.
4) Delayed-entry control: same session/side/stop, entry at a random 5-min slot between the real entry and 14:55.
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g2lib as G  # noqa: E402
import harness as H  # noqa: E402
import stats_protocol as sp  # noqa: E402
from run_g2 import CAL, SHA, cp, daily  # noqa: E402

warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

# 1) decomposition
base = G.onbreak_trades("NQ")
for mode in ("none", "against"):
    tr = G.onbreak_trades("NQ", trend_mode=mode)
    c1 = G.c1_draws("NQ", tr, R=200, k=60 + (mode == "against"))
    tr["c1"] = c1["c_mean"]
    tr["d_c1"] = tr["pnl_usd"] - tr["c1"].fillna(tr["pnl_usd"])
    dn, dd = daily(tr, "pnl_usd").to_numpy(), daily(tr, "d_c1").to_numpy()
    s18 = pd.DatetimeIndex(tr.session) >= "2018-01-01"
    r = dict(n=len(tr), net=float(tr.pnl_usd.mean()), d=float(tr.d_c1.mean()), t_d=float(sp.hac_t(dd)[0]),
             p_d=cp(dd)[0], t_net=float(sp.hac_t(dn)[0]), net_1017=float(tr.pnl_usd[~s18].mean()),
             net_1825=float(tr.pnl_usd[s18].mean()), d_1017=float(tr.d_c1[~s18].mean()), d_1825=float(tr.d_c1[s18].mean()))
    out[f"X-{mode}"] = r
    H.log(f"G2X-{mode}", "MNQ", f"EXPLORATORY overnight-range break, trend_mode={mode}", trades=tr,
          baseline=float(tr.c1.mean()), params=dict(trend_mode=mode, c1_R=200),
          note=f"exploratory decomposition of A2 (prereg {SHA[:12]}); p_d {r['p_d']:.4f}")
    print(f"X-{mode}: {r}", flush=True)

# 2) snapped stops
S, b, M, A, PX, last_t, _ = G.data("NQ")
tick = H.SPEC["NQ"]["tick"]
cand = G.onbreak_candidates(S, b)
cand["stop_pts"] = np.ceil(cand["stop_pts"] / tick - 1e-9) * tick
trs = G.onbreak_trades("NQ", cand=cand)
s18 = pd.DatetimeIndex(trs.session) >= "2018-01-01"
dn = daily(trs, "pnl_usd").to_numpy()
out["snapped_stop"] = dict(n=len(trs), net=float(trs.pnl_usd.mean()), net_1825=float(trs.pnl_usd[s18].mean()),
                           t_net=float(sp.hac_t(dn)[0]), p_net=cp(dn)[0], base_net=float(base.pnl_usd.mean()))
H.log("G2X-snapstop", "MNQ", "A2 with stops snapped to the tick grid (fill-convention check)", trades=trs,
      params=dict(stop="ceil to tick"), note=f"exploratory convention check of A2 (prereg {SHA[:12]})")
print("snapped stops:", out["snapped_stop"], flush=True)

# 3) eval with stop-based risk sizing vs 200 C1 twins
tr = pd.read_parquet(os.path.join(HERE, "..", "out", "trades", "A2.parquet"))
calm = H.calendar("NQ"); calm = calm[calm <= G.LAST_SESSION]
pols = [("risk", 100), ("risk", 150), ("risk", 250), ("risk", 400)]
ev = H.eval(tr, sizing=pols, calendar_=calm)
tw = G.c1_draws("NQ", tr, R=200, k=2, keep_twins=200)["twins"]
T = pd.concat([H.eval(t, sizing=pols, calendar_=calm) for t in tw], keys=range(len(tw)), names=["twin"]).reset_index(level=0)
for c in ("pass_pct", "within_10", "bust_pct"):
    g = T.groupby(["policy", "consistency", "window"])[c]
    arr = {k: v.to_numpy() for k, v in g}
    ev[f"twin_{c}_mean"] = [arr[(a, b_, w)].mean() for a, b_, w in zip(ev.policy, ev.consistency, ev.window)]
    ev[f"twin_{c}_rankp"] = [float((1 + np.sum(arr[(a, b_, w)] >= r)) / (1 + len(arr[(a, b_, w)])))
                             for a, b_, w, r in zip(ev.policy, ev.consistency, ev.window, ev[c])]
ev.to_csv(os.path.join(HERE, "eval_A2_risk.csv"), index=False)
pd.set_option("display.width", 300)
print(ev[["policy", "consistency", "window", "pass_pct", "bust_pct", "within_10", "micros_mean", "twin_pass_pct_mean",
          "twin_within_10_mean", "twin_bust_pct_mean", "twin_pass_pct_rankp", "twin_within_10_rankp",
          "luck_within_10"]].round(3).to_string())
H.log("G2X-evalrisk", "MNQ", "A2 eval with stop-based risk sizing 100/150/250/400 (descriptive)", trades=tr,
      params=dict(sizing=[list(p) for p in pols]), note="descriptive eval only; never a significance test")

# 4) delayed-entry control
si = S.index.get_indexer(pd.DatetimeIndex(tr.session))
rng = np.random.default_rng(55)
reps, reps18 = [], []
s18 = (pd.DatetimeIndex(tr.session) >= "2018-01-01")
for r_ in range(200):
    sl = np.array([rng.integers(a, max(a, 252) + 1) for a in tr.slot])
    w = G.walk("NQ", si, sl, tr.kx.to_numpy(), tr.d.to_numpy(), tr.stop_pts.to_numpy())
    net = np.where(w["ok"], w["net"], np.nan)
    reps.append(np.nanmean(net)); reps18.append(np.nanmean(net[s18]))
reps = np.array(reps)
out["delayed_entry"] = dict(mean=float(reps.mean()), sd=float(reps.std()), actual=float(tr.pnl_usd.mean()),
                            p=float((1 + (reps >= tr.pnl_usd.mean()).sum()) / (1 + len(reps))),
                            mean_2018=float(np.mean(reps18)), actual_2018=float(tr.pnl_usd[s18].mean()))
print("delayed entry:", out["delayed_entry"])
json.dump(out, open(os.path.join(HERE, "explore_g2.json"), "w"), indent=1)
