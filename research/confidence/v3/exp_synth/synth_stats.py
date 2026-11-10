"""
v3/exp_synth/synth_stats.py - SYNTHESIS step 1-4 of PREREG.md section 5 (light: reads v3/out/daily + results only).

1. Collect p_d of A1-A5 from their saved daily files (recomputed here with the frozen bootstrap), build P0
   (w_k = 1/sd of daily U1 net over 2010-06-07..2017-12-31, normalised) and its p_d.
2. Holm at 0.03 over {A1..A5, P0}; Romano-Wolf StepM and Hansen SPA_c on the 6-column d matrix (block 10, B 5000).
3. Intersection rule (p_net <= 0.05) + gates (from each group's verified results JSON; recomputed for P0) +
   selection-history DSR gates (A2 N_eff 30, A4 N_eff 9) -> SIGNIFICANT / PROMISING / NOT SIGNIFICANT, kill rule.
4. Tier B: per family (F1 daily/drift, F2 events, F3 momentum) StepM over ALL its secondary + exploratory columns
   at 0.004, NW t of d >= 3, DSR(d) >= 0.95 with N_eff = family floor + Li-Ji count of the family's v3 columns.

Outputs: v3/out/daily/P0.csv, v3/out/results/P0.json, v3/out/synthesis/{tierA.csv, tierB.csv, synth_stats.json}.
Holdout never touched: every series is asserted to end on 2025-06-27.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
sys.path.insert(0, V3)
import stats_protocol as sp  # noqa: E402

OUT = os.path.join(V3, "out")
SYN = os.path.join(OUT, "synthesis")
os.makedirs(SYN, exist_ok=True)
SEED = 20261109
B = 5000
PREREG_SHA = "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
END = pd.Timestamp("2025-06-27")
HOLM_ALPHA = 0.03
TIERB_ALPHA = 0.004
COLS = ["net_U1", "net_U2", "gross_U1", "ctrl_C1", "d", "n_trades"]

assert hashlib.sha256(open(os.path.join(V3, "PREREG.md"), "rb").read()).hexdigest() == PREREG_SHA, "PREREG changed"


def load_daily(hid):
    x = pd.read_csv(os.path.join(OUT, "daily", f"{hid}.csv"), parse_dates=["session"]).set_index("session")
    assert x.index.max() <= END, f"{hid}: session after 2025-06-27"
    return x


CAL = load_daily("A1").index
assert len(CAL) == 3876 and CAL.min() == pd.Timestamp("2010-06-07") and CAL.max() == END
YR = CAL.year.to_numpy()
H1 = YR <= 2017
H2 = YR >= 2018
Y22 = YR >= 2022


def daily(hid):
    x = load_daily(hid).reindex(CAL, fill_value=0.0)
    return x


def cp(x):
    p, bl = sp.conservative_p(sp.boot_pvalue_mean, np.asarray(x, float), B=B, seed=SEED)
    return float(p), {int(k): float(v) for k, v in bl.items()}


def t_nw(x):
    return float(sp.hac_t(np.asarray(x, float))[0])


def ok_of(v):
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float, np.bool_)):
        return bool(v)
    if isinstance(v, dict):
        return v.get("ok")
    return None


def gates_of(j):
    g = j.get("gates") or {}
    out = {k: ok_of(v) for k, v in g.items()}
    failed = [k for k, v in out.items() if v is False]
    return out, failed


def kill_of(j):
    k = j.get("kill", j.get("killed"))
    if isinstance(k, dict):
        k = k.get("killed", k.get("kill", k.get("ok")))
    return bool(k) if k is not None else None


def rj(hid):
    p = os.path.join(OUT, "results", f"{hid}.json")
    return json.load(open(p)) if os.path.exists(p) else {}


# =============================================================================================== 1. Tier A + P0
TA = ["A1", "A2", "A3", "A4", "A5"]
DA = {h: daily(h) for h in TA}
sd17 = {h: float(DA[h].loc[H1, "net_U1"].std(ddof=1)) for h in TA}
w_raw = {h: 1.0 / sd17[h] for h in TA}
wsum = sum(w_raw.values())
W = {h: w_raw[h] / wsum for h in TA}
P0 = pd.DataFrame(index=CAL)
for c in ["net_U1", "net_U2", "gross_U1", "ctrl_C1", "d"]:
    P0[c] = sum(W[h] * DA[h][c] for h in TA)
P0["n_trades"] = sum(DA[h]["n_trades"] for h in TA)
for h in TA:
    P0[f"net_{h}"] = DA[h]["net_U1"]
P0.index.name = "session"
P0.to_csv(os.path.join(OUT, "daily", "P0.csv"))
DA["P0"] = P0
FAM = TA + ["P0"]

rows = {}
for h in FAM:
    x = DA[h]
    p_d, p_d_bl = cp(x["d"])
    p_net, p_net_bl = cp(x["net_U1"])
    rows[h] = dict(hid=h, p_d=p_d, p_d_blocks=p_d_bl, p_net=p_net, p_net_blocks=p_net_bl, t_d=t_nw(x["d"]),
                   t_net=t_nw(x["net_U1"]), mean_d_day=float(x["d"].mean()), mean_net_day=float(x["net_U1"].mean()),
                   n_trades=int(x["n_trades"].sum()))

# reproduce the groups' reported p_d (sanity)
REPORTED_PD = {"A1": 0.0002, "A2": 0.0070, "A3": 0.0108, "A4": 0.0012, "A5": 0.0708}
for h, v in REPORTED_PD.items():
    assert abs(rows[h]["p_d"] - v) < 0.0006, (h, rows[h]["p_d"], v)

pvec = np.array([rows[h]["p_d"] for h in FAM])
holm_adj = sp.holm(pvec)
order = np.argsort(pvec, kind="stable")
thr = {FAM[i]: HOLM_ALPHA / (len(FAM) - r) for r, i in enumerate(order)}
# Holm step-down decision (stop at the first non-rejection)
holm_rej = {h: False for h in FAM}
for r, i in enumerate(order):
    if pvec[i] <= HOLM_ALPHA / (len(FAM) - r):
        holm_rej[FAM[i]] = True
    else:
        break
Dm = np.column_stack([DA[h]["d"].to_numpy() for h in FAM])
st = sp.stepm(Dm, mean_block=10, B=B, seed=SEED, alpha=HOLM_ALPHA)
spa = sp.spa(Dm, mean_block=10, B=B, seed=SEED)
rc = sp.reality_check(Dm, mean_block=10, B=B, seed=SEED)
corr_d = pd.DataFrame(Dm, columns=FAM).corr()
corr_net = pd.DataFrame(np.column_stack([DA[h]["net_U1"].to_numpy() for h in FAM]), columns=FAM).corr()
for i, h in enumerate(FAM):
    rows[h].update(holm_adj=float(holm_adj[i]), holm_threshold=float(thr[h]), holm_reject=bool(holm_rej[h]),
                   stepm_adj=float(st["p_adj"][i]), stepm_reject=bool(st["reject"][i]))

# ---------------------------------------------------------------- P0 gates (recomputed; P0 has no trade table)
x = P0
rep_d = sp.robust_report(x["d"].to_numpy(), CAL.to_numpy().astype("datetime64[D]"))
rep_u1 = sp.robust_report(x["net_U1"].to_numpy(), CAL.to_numpy().astype("datetime64[D]"))
rep_u2 = sp.robust_report(x["net_U2"].to_numpy(), CAL.to_numpy().astype("datetime64[D]"))
T = len(CAL)


def comp_null(h):
    """(mean, sd) of the C1 null distribution of a component's mean daily net (one C1 rep = one random strategy)."""
    j = rj(h)
    if h == "A1":
        return j["c1_null_mean"], j["c1_null_sd"]
    if h == "A4":
        return j["c1_strategy_mean_daily"]["mean"], j["c1_strategy_mean_daily"]["sd"]
    if h == "A5":
        return j["c1_rep_means_day_summary"]["mean"], j["c1_rep_means_day_summary"]["sd"]
    if h == "A2":
        m = float(DA["A2"]["ctrl_C1"].mean())
        return m, (j["c1_strategy_mean_day_q95"] - m) / norm.ppf(0.95)
    if h == "A3":
        reps = []
        for s in ("ES", "NQ", "YM"):
            c = pd.read_parquet(os.path.join(V3, "exp_g3_expiry", "cache", f"c1_A3_{s}_999.parquet"),
                                columns=["rep", "session", "pnl_usd"])
            c = c[pd.DatetimeIndex(c.session) <= END]
            reps.append(c.groupby("rep").pnl_usd.sum())
        tot = pd.concat(reps, axis=1).fillna(0).sum(axis=1) / T
        return float(tot.mean()), float(tot.std(ddof=1))


nulls = {h: comp_null(h) for h in TA}
null_mu = sum(W[h] * nulls[h][0] for h in TA)
null_sd = math.sqrt(sum((W[h] * nulls[h][1]) ** 2 for h in TA))
real = float(x["net_U1"].mean())
mc_p_P0 = float(norm.sf((real - null_mu) / null_sd))


def drift_day(h):
    j = rj(h)
    n = DA[h]["n_trades"].sum()
    if h == "A4":
        c = j["controls_per_trade"]["all"]
        return c["drift"] * n / T, c["hour_drift"] * n / T
    if h == "A5":
        return j["drift_mean_day"], j["hour_drift_mean_day"]
    return j["drift_per_trade"] * n / T, j["hour_drift_per_trade"] * n / T


dd = {h: drift_day(h) for h in TA}
P0_drift = sum(W[h] * dd[h][0] for h in TA)
P0_hdrift = sum(W[h] * dd[h][1] for h in TA)
cost = x["gross_U1"] - x["net_U1"]
g_over_c = float(x.loc[H2, "gross_U1"].sum() / cost[H2].sum())
yrs_u2 = pd.Series(x["net_U2"].to_numpy(), index=YR).groupby(level=0).sum()
P0_gates = {
    "1_d_pos_both_halves": bool(x.loc[H1, "d"].mean() > 0 and x.loc[H2, "d"].mean() > 0),
    "2_u2_pos_both_halves_u1_pos_2018_2022": bool(x.loc[H1, "net_U2"].mean() > 0 and x.loc[H2, "net_U2"].mean() > 0
                                                  and x.loc[H2, "net_U1"].mean() > 0 and x.loc[Y22, "net_U1"].mean() > 0),
    "3_years_pos_u2_ge_60pct": bool((yrs_u2 > 0).mean() >= 0.6),
    "4_u1_pos_wo_10_best": bool(rep_u1["drop_best"][0] > 0),
    "5_winsorised_pos": bool(rep_u1["winsor"][0] > 0),
    "6_c1_rank_p_le_005": bool(mc_p_P0 <= 0.05),
    "7_gross_ge_1.5x_cost_2018": bool(g_over_c >= 1.5),
    "8_beats_drift_and_hour_drift": bool(real > P0_drift and real > P0_hdrift),
}
P0_kill = bool(x["d"].mean() <= 0 or x.loc[H2, "net_U1"].mean() <= 0)
P0_detail = dict(weights=W, sd_2010_17=sd17, d_halves=[float(x.loc[H1, "d"].mean()), float(x.loc[H2, "d"].mean())],
                 u2_halves=[float(x.loc[H1, "net_U2"].mean()), float(x.loc[H2, "net_U2"].mean())],
                 u1_2018=float(x.loc[H2, "net_U1"].mean()), u1_2022=float(x.loc[Y22, "net_U1"].mean()),
                 share_years_pos_u2=float((yrs_u2 > 0).mean()), u1_wo_best10=rep_u1["drop_best"],
                 u1_winsor=rep_u1["winsor"], mc_rank_p_normal_approx=mc_p_P0, null_mu=null_mu, null_sd=null_sd,
                 component_nulls=nulls, gross_over_cost_2018=g_over_c, drift_day=P0_drift, hour_drift_day=P0_hdrift,
                 net_day=real, by_year_u1=rep_u1["by_year"], by_year_u2={int(k): float(v) for k, v in yrs_u2.items()},
                 robust_d=rep_d, robust_u1=rep_u1, portfolio_test=sp.portfolio_test(
                     np.column_stack([DA[h]["d"] for h in TA]), np.array([W[h] for h in TA]), 10, B, SEED))

# ---------------------------------------------------------------- labels
DSR_GATE = {"A2": 30, "A4": 9}
tierA = []
for h in FAM:
    r = rows[h]
    if h == "P0":
        g, failed, kill = P0_gates, [k for k, v in P0_gates.items() if not v], P0_kill
    else:
        g, failed = gates_of(rj(h))
        kill = kill_of(rj(h))
        kill = bool(DA[h]["d"].mean() <= 0 or DA[h].loc[H2, "net_U1"].mean() <= 0) if kill is None else kill
    sel = None
    if h in DSR_GATE:
        sel = float(sp.dsr(DA[h]["d"].to_numpy(), DSR_GATE[h])["dsr"])
        if sel < 0.95:
            failed = failed + [f"selection-history DSR {sel:.3f} < 0.95 (N_eff {DSR_GATE[h]})"]
    inter = r["p_net"] <= 0.05
    n_fail = len(failed) + (0 if r["holm_reject"] else 1) + (0 if inter else 1)
    if kill:
        label = "KILLED"
    elif r["holm_reject"] and inter and not failed:
        label = "SIGNIFICANT"
    elif (r["t_d"] >= 2 and n_fail <= 2) or (r["stepm_reject"] and not r["holm_reject"]):
        label = "PROMISING"
    else:
        label = "NOT SIGNIFICANT"
    r.update(gates=g, failed_gates=failed, kill=kill, intersection_p_net_le_005=bool(inter), dsr_selection=sel,
             n_failures=n_fail, label=label)
    tierA.append(r)
TA_df = pd.DataFrame([{k: v for k, v in r.items() if k not in ("gates", "p_d_blocks", "p_net_blocks")} for r in tierA])
TA_df.to_csv(os.path.join(SYN, "tierA.csv"), index=False)

# P0 results json (standard output)
json.dump(dict(prereg_sha256=PREREG_SHA, **{k: v for k, v in rows["P0"].items()}, detail=P0_detail),
          open(os.path.join(OUT, "results", "P0.json"), "w"), indent=1, default=float)

# =============================================================================================== 4. Tier B
MK = ["", "_MES", "_MNQ", "_MYM"]
F3_sec = [f"S1.{i}" for i in range(1, 7)] + [f"S2.{i}" for i in range(1, 7)]
F3_exp = [f"{x}{m}" for x in ("X2", "X3", "X5") for m in MK]
F3_post = [f"{x}{m}" for x in ("X2x_nostop", "X2x_time") for m in MK]
F3_nb = ["N1.lb10", "N1.lb20", "N1.hour", "N1.cost", "N2.1", "N2.2", "N2.3", "N2.4", "N2.5"]
F2_sec = ["S3.1", "S3.2", "S3.3", "S3.4", "S3.5", "S3.6-ES", "S3.6-NQ", "S3.6-YM", "S3.7"] + \
         [f"S4.{i}" for i in range(1, 9)] + ["S4.9_ES", "S4.9_NQ", "S4.9_YM"]
F2_exp = [f"{x}{m}" for x in ("X1a", "X1b") for m in MK]
F2_post = ["E4.1", "S4.8x"] + [f"{x}{m}" for x in ("X1ax_full", "X1ax_on") for m in MK]
F2_nb = ["A3-N0945", "A3-N1500", "A3-ES", "A3-NQ", "A3-YM", "N4.1", "N4.2", "N4.3"]
F1_sec = [f"S5.{i}_{m}" for i in range(1, 7) for m in ("MES", "MNQ", "MYM")]
F1_exp = [f"X4{m}" for m in MK]
F1_nb = ["A5_N1_5lags", "A5_N2_equal", "A5_N3_overnight", "A5_N4_daypart"]
FAMS = {
    "F3": dict(floor=45, primary=["A1", "A2"], sec=F3_sec, exp=F3_exp, post=F3_post, nb=F3_nb),
    "F2": dict(floor=45, primary=["A3", "A4"], sec=F2_sec, exp=F2_exp, post=F2_post, nb=F2_nb),
    "F1": dict(floor=15, primary=["A5"], sec=F1_sec, exp=F1_exp, post=[], nb=F1_nb),
}
tierB = []
fam_info = {}
for fam, f in FAMS.items():
    binding = f["sec"] + f["exp"] + f["post"]
    narrow = f["sec"] + f["exp"]
    allv3 = f["primary"] + binding + f["nb"]
    Dd = {h: daily(h) for h in allv3}
    Mb = np.column_stack([Dd[h]["d"].to_numpy() for h in binding])
    st_b = sp.stepm(Mb, mean_block=10, B=B, seed=SEED, alpha=TIERB_ALPHA)
    st_n = sp.stepm(np.column_stack([Dd[h]["d"].to_numpy() for h in narrow]), mean_block=10, B=B, seed=SEED,
                    alpha=TIERB_ALPHA)
    st_w = sp.stepm(np.column_stack([Dd[h]["d"].to_numpy() for h in binding + f["nb"]]), mean_block=10, B=B,
                    seed=SEED, alpha=TIERB_ALPHA)
    C = pd.DataFrame({h: Dd[h]["d"] for h in allv3}).corr().fillna(0).to_numpy()
    liji = sp.effective_n(C)[1]
    neff = f["floor"] + liji
    fam_info[fam] = dict(n_binding=len(binding), n_narrow=len(narrow), n_all_v3=len(allv3), liji=liji, N_eff=neff,
                         dsr_t_bar=sp.dsr_t_bar(neff))
    nar_idx = {h: i for i, h in enumerate(narrow)}
    wide_idx = {h: i for i, h in enumerate(binding + f["nb"])}
    for i, h in enumerate(binding):
        x = Dd[h]
        j = rj(h)
        g, failed = gates_of(j)
        kill = kill_of(j)
        if kill is None:
            kill = bool(x["d"].mean() <= 0 or x.loc[H2, "net_U1"].mean() <= 0)
        td = t_nw(x["d"])
        tn = t_nw(x["net_U1"])
        dsr_v = float(sp.dsr(x["d"].to_numpy(), neff)["dsr"])
        bar_f = []
        if st_b["p_adj"][i] > TIERB_ALPHA:
            bar_f.append("StepM")
        if td < 3:
            bar_f.append("t<3")
        if dsr_v < 0.95:
            bar_f.append("DSR")
        n_fail = len(bar_f) + len(failed)
        ntr = int(x["n_trades"].sum())
        if kill:
            label = "KILLED"
        elif n_fail == 0:
            label = "PASSES TIER B BAR"
        elif td >= 2 and n_fail <= 2:
            label = "PROMISING"
        else:
            label = "NOT SIGNIFICANT"
        tierB.append(dict(family=fam, hid=h, kind=("secondary" if h in f["sec"] else "exploratory (prereg)"
                                                   if h in f["exp"] else "exploratory (post-hoc)"),
                          n_trades=ntr, usd_per_trade=float(x["net_U1"].sum() / max(ntr, 1)),
                          d_per_trade=float(x["d"].sum() / max(ntr, 1)), t_d=td, t_net=tn,
                          p_d=cp(x["d"])[0] if td > 1.5 else np.nan,
                          p_net=cp(x["net_U1"])[0] if tn > 1.5 else np.nan,
                          stepm_binding=float(st_b["p_adj"][i]),
                          stepm_narrow=float(st_n["p_adj"][nar_idx[h]]) if h in nar_idx else np.nan,
                          stepm_with_neighbours=float(st_w["p_adj"][wide_idx[h]]), dsr=dsr_v, N_eff=neff,
                          bar_failed=";".join(bar_f), gates_failed=";".join(failed), kill=kill, label=label,
                          net_2010_17_day=float(x.loc[H1, "net_U1"].mean()), net_2018_day=float(x.loc[H2, "net_U1"].mean())))
TB = pd.DataFrame(tierB)
TB.to_csv(os.path.join(SYN, "tierB.csv"), index=False)

json.dump(dict(prereg_sha256=PREREG_SHA, tierA=tierA, P0=P0_detail, spa=spa, reality_check=rc,
               stepm_tierA=dict(zip(FAM, map(float, st["p_adj"]))), corr_d=corr_d.round(3).to_dict(),
               corr_net=corr_net.round(3).to_dict(), tierB_families=fam_info),
          open(os.path.join(SYN, "synth_stats.json"), "w"), indent=1, default=float)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
print("P0 weights:", {h: round(v, 3) for h, v in W.items()})
print(TA_df[["hid", "p_d", "p_net", "t_d", "t_net", "holm_adj", "holm_threshold", "holm_reject", "stepm_adj",
             "dsr_selection", "n_failures", "label"]].round(4).to_string(index=False))
for h in FAM:
    print(h, "failed:", next(r for r in tierA if r["hid"] == h)["failed_gates"])
print("SPA:", {k: round(v, 4) if isinstance(v, float) else v for k, v in spa.items()}, "RC:", rc)
print("P0 gates:", P0_gates, "kill", P0_kill)
print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in P0_detail.items()
       if k in ("d_halves", "u2_halves", "u1_2018", "u1_2022", "share_years_pos_u2", "u1_wo_best10", "u1_winsor",
                "mc_rank_p_normal_approx", "gross_over_cost_2018", "drift_day", "hour_drift_day", "net_day")})
print("corr d:\n", corr_d.round(2))
print("corr net:\n", corr_net.round(2))
print("families:", fam_info)
print(TB.sort_values(["family", "t_d"], ascending=[True, False]).round(4).to_string(index=False))
