"""v5/sizing_report.py - summary tables of v5/sizing.py outputs + trial log (module 'v5-sizing').
Writes v5/out/sizing_summary.txt and v5/out/sizing_frontier.csv."""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 40)
R = pd.read_csv(os.path.join(OUT, "sizing_real.csv"))
T = pd.read_csv(os.path.join(OUT, "sizing_tests.csv"))
W = pd.read_csv(os.path.join(OUT, "sizing_twins.csv"))
lines = []


def P(s=""):
    lines.append(str(s))


MET = ["pass_pct", "bust_pct", "days_pass_median", "within_5", "within_10", "within_20", "worst_day", "sharpe_d",
       "sharpe_ann", "maxdd", "sd_day", "usd_day", "micros_mean", "trades_taken", "want_risk_ratio"]
for port in ("P1", "A1"):
    for c in (0.4, 0.5):
        for w in ("2018+", "2022+"):
            x = R[(R.portfolio == port) & (R.consistency == c) & (R.window == w)]
            P(f"=== REAL {port} consistency {c} start days {w} (n_starts {int(x.n_starts.iloc[0])})")
            P(x.sort_values(["policy", "level"])[["policy", "level"] + MET].round(2).to_string(index=False))
            P()
# twin means per policy/level (luck baseline)
g = W.groupby(["portfolio", "consistency", "window", "policy", "level"])[
    ["pass_pct", "bust_pct", "within_20", "days_pass_median", "sharpe_ann"]].mean().reset_index()
P("=== TWINS (mean over 200 C1 reps)")
for port in ("P1", "A1"):
    x = g[(g.portfolio == port) & (g.consistency == 0.4) & (g.window == "2018+")]
    P(f"-- {port} c0.4 2018+")
    P(x.round(2).to_string(index=False))
    P()
# frontier: per policy, pass vs median days, within_20 vs bust across levels
fr = R[R.policy != "FIXRISK"].copy()
fr.to_csv(os.path.join(OUT, "sizing_frontier.csv"), index=False)
# tests
P("=== PRIMARY TESTS (P1, c 0.40, 2018+ starts, levels 3/5; D = policy - FIXED, pp)")
pr = T[T.primary].copy()
P(pr[["policy", "level", "metric", "diff_real", "ci_lo", "ci_hi", "p_boot", "p_holm", "diff_twin_mean",
      "diff_twin_p95", "p_twin", "excess_vs_twins"]].round(3).to_string(index=False))
P()
bust = T[(T.portfolio == "P1") & (T.consistency == 0.4) & (T.window == "2018+") & T.level.isin([3, 5]) &
         (T.metric == "bust_pct")]
P("=== bust guard (P1 c0.40 2018+): D bust pp, CI, twin mean")
P(bust[["policy", "level", "diff_real", "ci_lo", "ci_hi", "p_boot", "diff_twin_mean", "p_twin"]].round(3)
  .to_string(index=False))
P()
P("=== SECONDARY tests (all cells; p_boot raw, p_twin)")
sec = T[~T.primary & (T.metric != "bust_pct")]
P(sec[["portfolio", "consistency", "window", "level", "policy", "metric", "diff_real", "ci_lo", "ci_hi", "p_boot",
       "diff_twin_mean", "p_twin"]].round(3).to_string(index=False))
P()
winners = []
for (pol, lv), q in pr.groupby(["policy", "level"]):
    b = bust[(bust.policy == pol) & (bust.level == lv)].iloc[0]
    okb = b.ci_lo <= 0
    for _, r in q.iterrows():
        if r.diff_real > 0 and r.p_holm < 0.05 and r.p_twin < 0.05 and okb:
            winners.append((pol, lv, r.metric))
P(f"DECISION (PLAN section 6): policies beating FIXED = {winners if winners else 'none -> fixed sizing stands'}")
txt = "\n".join(lines)
open(os.path.join(OUT, "sizing_summary.txt"), "w").write(txt + "\n")
print(txt)

if len(sys.argv) > 1 and sys.argv[1] == "log":
    import run_pipeline as rp
    for pol in ["VT", "CVT", "CVTDN", "IV", "EV"]:
        q = pr[pr.policy == pol]
        for _, r in q.iterrows():
            rp.log_trial(module="v5-sizing", scope="P1 c0.40 2018+", model=f"{pol} n0={int(r.level)} vs FIXED",
                         target=r.metric, oos_rows=int(R[(R.portfolio == 'P1') & (R.policy == pol) &
                                                         (R.level == r.level)].trades_taken.iloc[0]),
                         parameters=f"PLAN.md sha256 in v5/out/PLAN.sha256; forecast A1 sigma*rv_60, A3 HAR-log x "
                                    f"share, A4 sigma*rv_240; expanding stats, min 20 prior",
                         note=f"D={r.diff_real:.2f}pp CI[{r.ci_lo:.2f},{r.ci_hi:.2f}] p_boot={r.p_boot:.3f} "
                              f"p_holm={r.p_holm:.3f} twinD={r.diff_twin_mean:.2f} p_twin={r.p_twin:.3f}")
    print("logged", len(pr), "trials")
