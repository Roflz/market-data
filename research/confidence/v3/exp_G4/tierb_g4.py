"""
v3/exp_G4/tierb_g4.py - G4 roll-up: A4 Tier A decision inputs; Tier B (StepM at 0.004 over the G4 d columns,
NW t >= 3, DSR >= 0.95 with N_eff 45, gates) - PROVISIONAL, because the synthesis step runs StepM over the whole F2
family (G3 + G4 + exploratory F2 columns; more columns can only raise the adjusted p). Light.
Writes v3/exp_G4/g4_table.csv and v3/out/results/G4_rollup.json.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g4lib as G  # noqa: E402
import stats_protocol as sp  # noqa: E402

TIERB = ["S4.1", "S4.2", "S4.3", "S4.4", "S4.5", "S4.6", "S4.7", "S4.8", "S4.9_ES", "S4.9_NQ", "S4.9_YM",
         "N4.1", "N4.2", "N4.3", "E4.1", "S4.8x"]
HOLM_T = [0.005, 0.006, 0.0075, 0.010, 0.015, 0.030]


def load(h):
    with open(os.path.join(G.OUT, "results", f"{h}.json")) as f:
        r = json.load(f)
    d = pd.read_csv(os.path.join(G.OUT, "daily", f"{h}.csv"), parse_dates=["session"]).set_index("session")
    return r, d


def main():
    D = {}
    R = {}
    for h in ["A4"] + TIERB + ["C3"]:
        R[h], dd = load(h)
        D[h] = dd["d"]
    Dm = pd.DataFrame({h: D[h] for h in TIERB}).fillna(0.0)
    st = sp.stepm(Dm.to_numpy(), mean_block=10, B=5000, seed=G.BASE_SEED, alpha=0.004)
    pst = dict(zip(TIERB, st["p_adj"]))
    corr = np.corrcoef(Dm.to_numpy().T)
    neff_g4 = sp.effective_n(corr)
    rows = []
    a4 = R["A4"]
    for h in ["A4"] + TIERB + ["C3"]:
        r = R[h]
        if h == "A4":
            fails = list(r["failed_gates"])
            holm_ok = r["p_d"] <= HOLM_T[0]          # <= 0.005: rejected by Holm at any rank (see notes)
            if not holm_ok:
                fails.append(f"Holm: p_d {r['p_d']:.4f} > 0.005 (depends on the other Tier A p-values)")
            if r["p_net"] > 0.05:
                fails.append(f"p_net {r['p_net']:.4f} > 0.05")
            if not r["dsr_d"] >= 0.95:
                fails.append(f"DSR(N_eff 9) {r['dsr_d']:.3f} < 0.95")
            if r["killed"]:
                lab = "KILLED"
            elif not fails:
                lab = "SIGNIFICANT (Tier A; Holm guaranteed since p_d <= 0.005)"
            elif r["t_d_nw"] >= 2 and len(fails) <= 2:
                lab = "PROMISING"
            else:
                lab = "NOT SIGNIFICANT"
            stp = np.nan
        elif h == "C3":
            fails, lab, stp = [], "control (reported)", np.nan
        else:
            stp = float(pst[h])
            lab, fails = G.tier_b_label(r, stp)
        same_sign = (np.sign(r["mean_d_per_trade"]) == np.sign(a4["mean_d_per_trade"])) if h.startswith("N4") else None
        bw = r["by_window_per_trade"]
        rows.append(dict(hid=h, tier=r["tier"], markets="+".join(r["markets"]), n=r["n_trades"],
                         per_year=round(r["trades_per_year"], 1), net_trade=round(r["mean_net_per_trade"], 2),
                         d_trade=round(r["mean_d_per_trade"], 2), c1_trade=round(r["mean_c1_per_trade"], 2),
                         net_10_17=round(bw["2010-17"]["net"], 2) if bw["2010-17"]["n"] else np.nan,
                         net_18_25=round(bw["2018-25H1"]["net"], 2), net_22p=round(bw["2022+"]["net"], 2),
                         u2_trade=round(r["mean_u2_per_trade"], 2), win=round(r["win_pct"], 1),
                         p_d=round(r["p_d"], 4), p_net=round(r["p_net"], 4), t_d=round(r["t_d_nw"], 2),
                         t_net=round(r["t_net_nw"], 2), sharpe=round(r["sharpe_ann_net"], 2),
                         dsr=round(r["dsr_d"], 3), stepm_p=None if np.isnan(stp) else round(stp, 4),
                         mc_p=round(r["mc_rank_p"], 3), wo10=round(r["net_wo_10_best_total"], 0),
                         total=round(r["net_total"], 0),
                         stress_trade=round(r["cost_stress_plus1tick"]["mean_per_trade"], 2),
                         drift=round(r["controls_per_trade"]["all"]["drift"], 2),
                         hour_drift=round(r["controls_per_trade"]["all"]["hour_drift"], 2),
                         c2=round(r["controls_per_trade"]["all"]["C2_random_side"], 2),
                         same_sign_as_A4=same_sign, failed="; ".join(fails), label=lab))
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(G.HERE, "g4_table.csv"), index=False)
    pd.set_option("display.width", 300)
    pd.set_option("display.max_columns", 40)
    pd.set_option("display.max_colwidth", 200)
    print(tab.drop(columns=["failed"]).to_string(index=False))
    print()
    for _, r in tab.iterrows():
        print(f"{r.hid}: {r.label} | failed: {r.failed}")
    print(f"\nG4 Tier B columns: {len(TIERB)}; effective number (rho-bar, Li-Ji) = {neff_g4}")
    roll = dict(stepm_g4_only={k: float(v) for k, v in pst.items()}, neff_g4=neff_g4,
                table=tab.to_dict(orient="records"),
                note="StepM here is within the G4 columns only; the synthesis repeats it over all F2 columns.")
    with open(os.path.join(G.OUT, "results", "G4_rollup.json"), "w") as f:
        json.dump(roll, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))


if __name__ == "__main__":
    main()
