"""Collect v3/out/results/{A2,S2.*,N2.*}.json -> exp_g2_onbreak/summary_all.csv + labels (PREREG 0.4/0.5)."""
import json, os, glob
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "out", "results")
ids = ["A2", "S2.1", "S2.2", "S2.3", "S2.4", "S2.5", "S2.6", "N2.1", "N2.2", "N2.3", "N2.4", "N2.5"]
rows = []
for h in ids:
    p = os.path.join(RES, f"{h}.json")
    if not os.path.exists(p):
        continue
    r = json.load(open(p))
    fails = [k for k, v in r["gates"].items() if not v]
    if r["tier"] == "A":
        holm = "pass for sure" if r["p_d"] <= 0.005 else ("fail for sure" if r["p_d"] > 0.03 else "depends on A1/A3-A5/P0 p-values")
        dsr_ok = r["dsr_d"] >= 0.95
        nf = len(fails) + (0 if dsr_ok else 1) + (0 if holm == "pass for sure" else 1)
        if r["kill"]:
            lab = "KILLED"
        elif holm == "pass for sure" and dsr_ok and not fails and r["p_net"] <= 0.05:
            lab = "SIGNIFICANT"
        elif r["t_d"] >= 2 and nf <= 2:
            lab = "PROMISING (forward paper test only)"
        else:
            lab = "NOT SIGNIFICANT"
        extra = f"Holm: {holm}; DSR(N_eff 30) {r['dsr_d']:.3f}"
    else:
        sm = r.get("stepm_G2_p_adj", np.nan)
        tb = [sm <= 0.004, r["t_d"] >= 3, r["dsr_d"] >= 0.95]
        nf = len(fails) + sum(not x for x in tb)
        if r["kill"]:
            lab = "KILLED"
        elif all(tb) and not fails and r["p_net"] <= 0.05:
            lab = "SIGNIFICANT (Tier B candidate)"
        elif r["t_d"] >= 2 and nf <= 2:
            lab = "PROMISING (forward paper test only)"
        else:
            lab = "NOT SIGNIFICANT"
        if r["tier"] == "N":
            lab = ("same sign as A2: " + ("yes" if r["mean_d_trade"] > 0 and r["net_per_trade"] > 0 else "no")) + "; " + lab
        extra = f"StepM(G2 cols) {sm:.4f}; DSR(N_eff 45) {r['dsr_d']:.3f}"
    w = r["windows_net_per_trade"]
    rows.append(dict(hid=h, market="M" + r["market"] if r["market"] != "YM" else "MYM", tier=r["tier"], n=r["n_trades"],
                     per_yr=round(r["trades_per_year"], 1), net_trade=round(r["net_per_trade"], 2),
                     d_trade=round(r["mean_d_trade"], 2), c1_trade=round(r["c1_per_trade"], 2),
                     net_1017=round(w["2010-17"], 2), net_1825=round(w["2018-25H1"], 2), net_22=round(w["2022+"], 2),
                     p_d=round(r["p_d"], 4), t_d=round(r["t_d"], 2), p_net=round(r["p_net"], 4), t_net=round(r["t_net"], 2),
                     sharpe=round(r["sharpe_ann"], 2), mc_p=r["mc_rank_p"], drift=round(r["drift_per_trade"], 2),
                     hour_drift=round(r["hour_drift_per_trade"], 2), c2_side=round(r["c2_random_side_per_trade"], 2),
                     stress_net=round(r["cost_stress_net_per_trade"], 2), stress_p=round(r["cost_stress_p_net"], 4),
                     wo10_total=round(r["net_wo_best10_total"]), failed_gates=";".join(fails) or "-", label=lab, detail=extra))
out = pd.DataFrame(rows)
out.to_csv(os.path.join(HERE, "summary_all.csv"), index=False)
pd.set_option("display.width", 400); pd.set_option("display.max_colwidth", 80)
print(out.drop(columns=["detail", "failed_gates", "label"]).to_string())
print(out[["hid", "failed_gates", "label", "detail"]].to_string())
