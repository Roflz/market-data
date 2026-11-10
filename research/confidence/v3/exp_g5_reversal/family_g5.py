"""G5 family step (light): Tier B decision for the G5 secondaries + A5 neighbours (family F1, G5 columns only;
the synthesis step adds the other F1 columns, which can only make it stricter), A5 Tier A label (Holm status
from p_d alone: p_d <= 0.005 always rejected, > 0.03 never; in between it depends on A1-A4/P0), summary table."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness as H            # noqa: E402
import stats_protocol as sp    # noqa: E402
import g5                      # noqa: E402

OUT = os.path.join(H.HERE, "out")


def load(cid):
    with open(os.path.join(OUT, "results", f"{cid}.json")) as f:
        r = json.load(f)
    D = pd.read_csv(os.path.join(OUT, "daily", f"{cid}.csv"), parse_dates=["session"]).set_index("session")
    return r, D


def label_A(r):
    p = r["p_d"]
    holm = "rejected" if p <= 0.005 else ("not rejected" if p > 0.03 else "pending (depends on A1-A4, P0)")
    fails = list(r["failed_gates"])
    if holm != "rejected":
        fails = ["Holm"] + fails
    if r["p_net"] > 0.05:
        fails = fails + ["intersection p_net > 0.05"]
    if r["kill"]:
        lab = "NOT SIGNIFICANT (killed)"
    elif not fails:
        lab = "SIGNIFICANT"
    elif r["t_nw_d"] >= 2 and len(fails) <= 2:
        lab = "PROMISING"
    else:
        lab = "NOT SIGNIFICANT"
    return lab, holm, fails


def main():
    cols = [c for c in g5.COL_LIST if g5.COLS[c][2] in ("N", "S")]
    R, Dd, Dn = {}, {}, {}
    for c in cols:
        r, D = load(c)
        R[c] = r; Dd[c] = D["d"]; Dn[c] = D["net_U1"]
    Dd = pd.DataFrame(Dd); Dn = pd.DataFrame(Dn)
    st = sp.stepm(Dd.to_numpy(), mean_block=10, B=5000, seed=g5.SEED, alpha=0.004)
    corr = np.corrcoef(Dd.to_numpy().T)
    rho_n, liji = sp.effective_n(corr)
    N_eff = max(15.0, liji)
    rA, DA = load("A5")
    labA, holm, failsA = label_A(rA)
    rows = []
    for j, c in enumerate(cols):
        r = R[c]
        ds = sp.dsr(Dd[c].to_numpy(), N_eff)
        tierB_fail = []
        if st["p_adj"][j] > 0.004:
            tierB_fail.append(f"StepM p {st['p_adj'][j]:.3f} > 0.004")
        if r["t_nw_d"] < 3:
            tierB_fail.append(f"NW t {r['t_nw_d']:.2f} < 3")
        if ds["dsr"] < 0.95:
            tierB_fail.append(f"DSR {ds['dsr']:.2f} < 0.95")
        fails = (["Tier B bar"] if tierB_fail else []) + list(r["failed_gates"])
        if r["kill"]:
            lab = "NOT SIGNIFICANT (killed)"
        elif not fails:
            lab = "SIGNIFICANT (Tier B candidate for next round)"
        elif r["t_nw_d"] >= 2 and len(fails) <= 2:
            lab = "PROMISING"
        else:
            lab = "NOT SIGNIFICANT"
        same_sign = None
        if g5.COLS[c][2] == "N":
            same_sign = bool(np.sign(r["mean_d_day"]) == np.sign(rA["mean_d_day"]))
        rows.append(dict(col=c, kind=g5.COLS[c][2], n=r["n_trades"], tr_yr=round(r["trades_per_year"], 1),
                         usd_tr=round(r["usd_per_trade"], 2), d_tr=round(r["d_per_trade"], 2),
                         c1_tr=round(r["ctrl_C1_per_trade"], 2), t_d=round(r["t_nw_d"], 2),
                         p_d=r["p_d"], t_net=round(r["t_nw_net"], 2), p_net=r["p_net"],
                         stepm=float(st["p_adj"][j]), dsr=round(ds["dsr"], 3),
                         net_10_17=r["windows_net_trade"]["2010-17"], net_18_25=r["windows_net_trade"]["2018-25H1"],
                         net_22=r["windows_net_trade"]["2022+"],
                         wo_top10=r["net_wo_top10_per_trade"], stress_tr=r["stress"]["usd_per_trade"],
                         drift_tr=r["drift_per_trade"], hour_drift_tr=r["hour_drift_per_trade"],
                         failed=";".join(fails + tierB_fail), kill=r["kill"], label=lab, same_sign_as_A5=same_sign))
        r["tierB"] = dict(stepm_p=float(st["p_adj"][j]), N_eff=N_eff, liji=liji, dsr=ds, fails=tierB_fail,
                          label=lab, same_sign_as_A5=same_sign)
        with open(os.path.join(OUT, "results", f"{c}.json"), "w") as f:
            json.dump(g5.jsonable(r), f, indent=1)
    T = pd.DataFrame(rows)
    rA["tierA"] = dict(label=labA, holm_status=holm, fails=failsA,
                       dsr_N15=sp.dsr(DA["d"].to_numpy(), 15))
    with open(os.path.join(OUT, "results", "A5.json"), "w") as f:
        json.dump(g5.jsonable(rA), f, indent=1)
    T.to_csv(os.path.join(H.HERE, "exp_G5", "summary_G5.csv"), index=False)
    pd.set_option("display.width", 300); pd.set_option("display.max_columns", 40)
    print(f"F1/G5 Tier B: {len(cols)} columns, Li-Ji {liji:.1f}, rho-formula {rho_n:.1f}, N_eff used {N_eff:.1f}")
    print(T.drop(columns=["failed"]).to_string())
    print(T[["col", "failed"]].to_string())
    print("A5:", labA, "| Holm:", holm, "| fails:", failsA)


if __name__ == "__main__":
    main()
