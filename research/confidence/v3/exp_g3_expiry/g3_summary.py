"""G3 summary: Tier B StepM over the G3 secondary columns (part of F2), DSR, labels, neighbour signs, eval-math
target check and per-market eval vs the luck bar for A3, by-year tables. Light. Writes v3/exp_g3_expiry/summary.json
and summary.txt."""
import json
import os

import numpy as np
import pandas as pd

import g3
import harness as H
import stats_protocol as sp

OUT = g3.OUT
R = lambda h: json.load(open(os.path.join(OUT, "results", f"{h}.json")))  # noqa: E731
DLY = lambda h: pd.read_csv(os.path.join(OUT, "daily", f"{h}.csv"), index_col=0, parse_dates=True)  # noqa: E731
TIER_B = ["S3.1", "S3.2", "S3.3", "S3.4", "S3.5", "S3.6-ES", "S3.6-NQ", "S3.6-YM", "S3.7"]
NEIGH = ["A3-N0945", "A3-N1500", "A3-ES", "A3-NQ", "A3-YM"]
lines = []
P = lambda *a: lines.append(" ".join(str(x) for x in a))  # noqa: E731
res = {h: R(h) for h in ["A3"] + TIER_B + NEIGH + ["A3-C3"]}

# ---------------------------------------------------------------- StepM (Tier B) on the d matrix
Dd = pd.DataFrame({h: DLY(h)["d"] for h in TIER_B})
sm = sp.stepm(Dd.to_numpy(), mean_block=10, B=5000, seed=g3.SEED)
Dd2 = pd.DataFrame({h: DLY(h)["d"] for h in TIER_B + NEIGH})
sm2 = sp.stepm(Dd2.to_numpy(), mean_block=10, B=5000, seed=g3.SEED)
corr = Dd.corr().to_numpy()
neff_g3 = sp.effective_n(corr)
tierb = {}
for j, h in enumerate(TIER_B):
    r = res[h]
    fails_b = []
    if sm["p_adj"][j] > 0.004:
        fails_b.append(f"StepM p {sm['p_adj'][j]:.4f} > 0.004")
    if r["t_d_nw"] < 3:
        fails_b.append(f"NW t {r['t_d_nw']:.2f} < 3")
    if r["dsr_d_neff45"] < 0.95:
        fails_b.append(f"DSR {r['dsr_d_neff45']:.2f} < 0.95")
    gate_fails = list(r["failed_gates"])
    n_fail = len(gate_fails) + (1 if fails_b else 0)
    if not fails_b and not gate_fails:
        label = "SIGNIFICANT (Tier B: candidate for next round)"
    elif r["t_d_nw"] >= 2 and n_fail <= 2:
        label = "PROMISING (forward paper test only)"
    else:
        label = "NOT SIGNIFICANT"
    if r["kill"]:
        label += "; KILLED (mean d <= 0 or 2018-25H1 net <= 0)"
    tierb[h] = dict(stepm_p=float(sm["p_adj"][j]), stepm_t=float(sm["t"][j]), tierb_fails=fails_b,
                    gate_fails=gate_fails, label=label)

# ---------------------------------------------------------------- A3 (Tier A)
a3 = res["A3"]
others = {h: R(h)["p_d"] for h in ("A1", "A2", "A4", "A5", "P0") if os.path.exists(os.path.join(OUT, "results", f"{h}.json"))}
holm_thr = [0.005, 0.006, 0.0075, 0.010, 0.015, 0.030]
a3_fail = list(a3["failed_gates"])
holm_note = ("A3 p_d %.4f: Holm at 0.03 over K=6 needs p_d <= 0.005 if it is the smallest p, at best <= 0.03 if it is "
             "the largest and all others are rejected" % a3["p_d"])
prov = None
if all(os.path.exists(os.path.join(OUT, "daily", f"A{k}.csv")) for k in range(1, 6)) and "P0" not in others:
    # PROVISIONAL P0 (the synthesis step owns P0; this only informs A3's conditional Holm status, not logged)
    comp = [f"A{k}" for k in range(1, 6)]
    dd = pd.DataFrame({h: DLY(h)["d"] for h in comp}).reindex(g3.CAL).fillna(0.0)
    nn = pd.DataFrame({h: DLY(h)["net_U1"] for h in comp}).reindex(g3.CAL).fillna(0.0)
    sd_ = nn.loc[:"2017-12-31"].std(ddof=1)
    w_ = (1 / sd_) / (1 / sd_).sum()
    p0 = sp.conservative_p(sp.boot_pvalue_mean, (dd @ w_).to_numpy(), B=5000, seed=g3.SEED)[0]
    pv = {h: R(h)["p_d"] for h in comp}
    pv["P0"] = p0
    adj_ = sp.holm(np.array(list(pv.values())))
    prov = dict(weights=w_.round(4).to_dict(), p_d=pv, holm_adj=dict(zip(pv, np.round(adj_, 4).tolist())),
                A3_reject=bool(adj_[comp.index("A3")] <= 0.03))
    others = dict(others, P0_provisional=p0)
if prov is not None:
    holm_note += (f"; PROVISIONAL Holm with P0 rebuilt here from the other groups' current files: "
                  f"A3 Holm-adjusted p {prov['holm_adj']['A3']:.4f} -> {'reject' if prov['A3_reject'] else 'no reject'}"
                  f" (p_d: {', '.join(f'{k} {v:.4f}' for k, v in prov['p_d'].items())})")
holm_provisional = prov is not None
if prov is not None:
    holm_pass = prov["A3_reject"]
elif len(others) == 5:
    ps = np.array([a3["p_d"]] + list(others.values()))
    adj = sp.holm(ps)
    holm_pass = bool(adj[0] <= 0.03)
    holm_note += f"; full family available: Holm-adjusted p {adj[0]:.4f} -> {'reject' if holm_pass else 'no reject'}"
else:
    holm_pass = None
    holm_note += f"; other Tier A p_d available now: {others} (final Holm in the synthesis step)"
best_case = a3["p_d"] <= 0.03
fails_a = []
if not best_case or holm_pass is False:
    fails_a.append("Holm not passed")
elif holm_pass is None and a3["p_d"] > 0.005:
    fails_a.append("Holm depends on the other A p-values (p_d > 0.005)")
if a3["p_net"] > 0.05:
    fails_a.append(f"intersection: p_net {a3['p_net']:.4f} > 0.05")
n_fail = len(a3_fail) + (1 if any(f.startswith("Holm not") for f in fails_a) else 0) + \
    (1 if any(f.startswith("intersection") for f in fails_a) else 0)
if a3["kill"]:
    a3_label = "KILLED"
elif not a3_fail and not fails_a:
    a3_label = ("SIGNIFICANT (PROVISIONAL: Holm uses a P0 rebuilt from the other groups' current files; "
                "final in the synthesis step)") if holm_provisional else "SIGNIFICANT"
elif not a3_fail and fails_a == ["Holm depends on the other A p-values (p_d > 0.005)"]:
    a3_label = "SIGNIFICANT if Holm rejects in the synthesis (all gates + intersection pass), else PROMISING"
elif a3["t_d_nw"] >= 2 and n_fail <= 2:
    a3_label = "PROMISING (forward paper test only)"
else:
    a3_label = "NOT SIGNIFICANT"

# eval-math target check for A3 (basket stream, 1 micro each)
D3 = DLY("A3")
x = D3["net_U1"]
tr3 = pd.read_parquet(os.path.join(OUT, "trades", "A3.parquet"))
emt = dict(daily_sharpe=float(x.mean() / x.std(ddof=1)), share_sessions_with_trade=float((D3.n_trades > 0).mean()),
           win_rate=float((tr3.pnl_usd > 0).mean()),
           usd_per_trade_by_market={s: float(tr3.loc[tr3.market == s, "pnl_usd"].mean()) for s in g3.MKTS},
           share_profit_kept_wo_10_best=float(np.sort(x.to_numpy())[:-10].sum() / x.sum()) if x.sum() > 0 else None)
# per-market eval vs the v2 luck bar at matched size (single-market books)
pm_eval = {}
for s in g3.MKTS:
    t = tr3[tr3.market == s]
    e = H.eval(t, sizing=[("fixed", 1), ("fixed", 3), ("fixed", 5)], calendar_=g3.CAL)
    pm_eval[s] = e[e.consistency == 0.4][["policy", "window", "pass_pct", "within_10", "bust_pct", "luck_within_10",
                                         "luck_pass_pct"]].round(2).to_dict(orient="records")
# by-year table (U1 net per year, $ per micro summed over the basket; d per year)
yr = pd.DataFrame({"net_U1": D3.net_U1.groupby(D3.index.year).sum(), "net_U2": D3.net_U2.groupby(D3.index.year).sum(),
                   "d": D3.d.groupby(D3.index.year).sum(),
                   **{f"net_{s}": D3[f"net_{s}"].groupby(D3.index.year).sum() for s in g3.MKTS},
                   "n_trades": D3.n_trades.groupby(D3.index.year).sum()})
neigh = {h: dict(usd_per_trade=res[h]["usd_per_trade"], d_per_trade=res[h]["d_per_trade"], p_d=res[h]["p_d"],
                 t_d=res[h]["t_d_nw"], same_sign=bool(np.sign(res[h]["mean_d_day"]) == np.sign(a3["mean_d_day"])))
         for h in NEIGH}
summary = dict(A3=dict(label=a3_label, holm_note=holm_note, holm_provisional=prov, tierA_fails=fails_a, gate_fails=a3_fail,
                       eval_math_targets=emt, per_market_eval_40pct=pm_eval, neighbours=neigh,
                       c3_non_expiry_fridays=dict(usd_per_trade=res["A3-C3"]["usd_per_trade"],
                                                  p_net=res["A3-C3"]["p_net"], t_net=res["A3-C3"]["t_net_nw"])),
               tierB=tierb, stepm_with_neighbours={h: float(p) for h, p in zip(TIER_B + NEIGH, sm2["p_adj"])},
               neff_g3_secondaries=neff_g3, by_year_A3=yr.round(2).to_dict(orient="index"))
json.dump(summary, open(os.path.join(g3.HERE, "summary.json"), "w"), indent=1, default=str)

pd.set_option("display.width", 250)
P("=== G3 expiry-day flows: summary", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), "===")
P(f"A3 label: {a3_label}")
P(holm_note)
for k in ("n_trades", "trades_per_year", "usd_per_trade", "usd_per_trade_U2", "d_per_trade", "c1_per_trade", "p_d",
          "p_net", "t_d_nw", "t_net_nw", "sharpe_ann_net", "mc_rank_p", "drift_per_trade", "hour_drift_per_trade",
          "c2_random_side_per_trade", "c2_rank_p", "gross_2018_25H1", "cost_2018_25H1", "dsr_d_neff45"):
    P(f"  {k:28s} {a3[k]}")
P("  windows per trade U1:", a3["per_trade_windows"])
P("  windows per trade U2:", a3["per_trade_windows_U2"])
P("  robust net U1:", {k: a3["robust_net_U1"][k] for k in ("all", "2010_17", "2018_25H1", "2022+", "drop_best", "winsor")})
P("  robust d     :", {k: a3["robust_d"][k] for k in ("all", "2010_17", "2018_25H1", "2022+", "drop_best", "winsor")})
P("  2-year blocks U2:", a3["u2_2yr_blocks"])
P("  gates:", a3["gates"])
P("  cost stress +1 tick:", a3["cost_stress_plus1tick"])
P("  by market:", json.dumps(a3["by_market"], indent=None))
P("  eval-math targets:", emt)
P("  C3 non-expiry Fridays:", summary["A3"]["c3_non_expiry_fridays"])
P("  neighbours:", neigh)
P("\nA3 by year ($ per micro, basket summed):\n" + yr.round(1).to_string())
if "eval" in a3:
    ev = pd.DataFrame(a3["eval"])
    P("\nA3 basket eval vs 200 C1 twins (40% rule):\n" + ev[ev.consistency == 0.4][
        ["policy", "window", "pass_pct", "twin_pass_pct", "within_10", "twin_within_10", "within_20", "bust_pct",
         "twin_bust_pct", "rank_p_pass"]].to_string())
    P("A3 basket eval (50% rule):\n" + ev[ev.consistency == 0.5][
        ["policy", "window", "pass_pct", "twin_pass_pct", "within_10", "twin_within_10", "bust_pct", "rank_p_pass"]].to_string())
P("\nPer-market eval (40%) vs v2 luck bar:")
for s, v in pm_eval.items():
    P(s, pd.DataFrame(v).to_string())
P("\nTier B (StepM over the 9 G3 secondary columns, mean block 10, B 5000; N_eff Li-Ji of these columns %s):" % (neff_g3,))
rows = []
for h in TIER_B:
    r = res[h]
    rows.append(dict(hid=h, n=r["n_trades"], usd_tr=round(r["usd_per_trade"], 2), d_tr=round(r["d_per_trade"], 2),
                     p_d=round(r["p_d"], 4), p_net=round(r["p_net"], 4), t_d=round(r["t_d_nw"], 2),
                     stepm=round(tierb[h]["stepm_p"], 4), dsr=round(r["dsr_d_neff45"], 3), mc_p=r["mc_rank_p"],
                     n_gate_fail=len(r["failed_gates"]), label=tierb[h]["label"]))
P(pd.DataFrame(rows).to_string())
for h in TIER_B:
    P(f"  {h}: gate fails {res[h]['failed_gates']}; tier-B fails {tierb[h]['tierb_fails']}")
P("\nStepM incl. neighbours (14 cols):", {k: round(v, 4) for k, v in summary["stepm_with_neighbours"].items()})
open(os.path.join(g3.HERE, "summary.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
