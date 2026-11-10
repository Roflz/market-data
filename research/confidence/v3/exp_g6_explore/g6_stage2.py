"""
v3/exp_g6_explore/g6_stage2.py - G6 stage 2 (light): StepM within G6 (per family and all 24 columns), DSR, Tier B
verdicts, eval odds (fixed 1/3/5 micros; 10 C1 twins at the same size; v2 luck bar), standard outputs, trial log,
summary. Reads exp_g6_explore/g6_stage1.pkl written by g6_run.py.
"""
import json
import os
import pickle
import time
import warnings

import numpy as np
import pandas as pd

import harness as H
import stats_protocol as sp
from g6_run import CAL, SEEDK, MK, MOFF, NOTE, OUT, G6DIR, HERE, SEED_BOOT, log

warnings.simplefilter("ignore")
FLOOR = {"F1": 15, "F2": 45, "F3": 45}
SIZES = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
N_TWIN = 10
RULE = {"X1a": "ES prev_ret_cc <= -2%: long 09:30 -> 16:00",
        "X1b": "ES prev_ret_cc <= -2%: at 10:00 fade the 09:30->10:00 move, exit 16:00",
        "X2": "0.15% < |gap 09:30 vs prev 16:00| < 0.50%: fade at 09:30, target prev close, stop = gap beyond, exit 11:00",
        "X3": "first 15-min close beyond the 18:00-02:00 range (02:00-04:45 bars): enter next mark, stop range mid, exit 09:30",
        "X4": "RTH 30-min slot with the largest |20-day mean| / sd, trade its sign at the slot marks",
        "X5": "calm (prev_rv_rth bottom tercile of 250 sessions) and |09:30->12:00| > 0.5 x 20-day mean: fade at 12:00, exit 15:30"}


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, pd.Timestamp):
        return str(o.date())
    return o


def eval_summary(tr, entries_by_sym, hid, single):
    """H.eval on the column's trades and on N_TWIN C1 twins (same marks/side/size, random same-year sessions)."""
    ev = H.eval(tr, SIZES)
    tw = []
    for rep in range(N_TWIN):
        parts = []
        for sym, e in entries_by_sym.items():
            rt = H.random_time_trades(sym, e, n_rep=1, seed=1000 * SEEDK[hid] + 900 + rep + MOFF[sym],
                                      keep_session=False, keep_marks=True, keep_side=True)
            parts.append(rt)
        t = pd.concat(parts, ignore_index=True)
        t = t[pd.DatetimeIndex(t["session"]) <= CAL[-1]]
        tw.append(H.eval(t, SIZES, calendar_=CAL if not single else None).assign(rep=rep))
    tw = pd.concat(tw)
    g = tw.groupby(["policy", "consistency", "window"])[["pass_pct", "within_10", "bust_pct"]].mean()
    g.columns = ["twin_pass_pct", "twin_within_10", "twin_bust_pct"]
    q = tw.groupby(["policy", "consistency", "window"])["within_10"].quantile(0.9).rename("twin_within_10_p90")
    ev = ev.join(g, on=["policy", "consistency", "window"]).join(q, on=["policy", "consistency", "window"])
    return ev


def main():
    t0 = time.time()
    st = pickle.load(open(os.path.join(HERE, "g6_stage1.pkl"), "rb"))
    R, Dd, T, runs = st["results"], st["dailies"], st["trades"], st["runs"]
    cols = list(R)
    # ---------------- StepM within G6 (per family and over all 24 columns) + Li-Ji effective count
    Dm = pd.DataFrame({c: Dd[c]["d"].to_numpy() for c in cols})
    sm_all = sp.stepm(Dm.to_numpy(), mean_block=10, B=5000, seed=SEED_BOOT, alpha=0.004)
    for c, p in zip(cols, sm_all["p_adj"]):
        R[c]["stepm_p_all_G6"] = float(p)
    for fam in ("F1", "F2", "F3"):
        fc = [c for c in cols if R[c]["family"] == fam]
        sm = sp.stepm(Dm[fc].to_numpy(), mean_block=10, B=5000, seed=SEED_BOOT, alpha=0.004)
        corr = np.corrcoef(Dm[fc].to_numpy().T)
        liji = sp.effective_n(corr)[1]
        for c, p in zip(fc, sm["p_adj"]):
            R[c]["stepm_p_family_G6"] = float(p)
            R[c]["liji_G6_family"] = float(liji)
            neff = FLOOR[fam] + liji
            R[c]["N_eff"] = float(neff)
            R[c]["dsr_d"] = sp.dsr(Dd[c]["d"].to_numpy(), neff)["dsr"]
            R[c]["dsr_d_at_floor"] = sp.dsr(Dd[c]["d"].to_numpy(), FLOOR[fam])["dsr"]
            R[c]["dsr_net"] = sp.dsr(Dd[c]["net_U1"].to_numpy(), neff)["dsr"]
    log(f"stepm/dsr done {time.time() - t0:.0f}s")
    # ---------------- verdicts
    for c in cols:
        r = R[c]
        tb = dict(stepm=r["stepm_p_family_G6"] <= 0.004, t3=r["nw_t_d"] >= 3, dsr=r["dsr_d"] >= 0.95)
        r["tierB"] = tb
        r["qualifies_next_round"] = bool(all(tb.values()) and r["n_gates_failed"] == 0)
        fails = [k for k, v in tb.items() if not v] + [k for k, v in r["gates"].items() if not v]
        r["failed"] = fails
        if r["qualifies_next_round"]:
            r["verdict"] = "edge"
            r["label"] = "QUALIFIES for next-round pre-registration (Tier B cleared; not proven)"
        elif r["kill"]:
            r["verdict"] = "no_edge"
            r["label"] = "KILLED (mean d <= 0 or 2018-25H1 net <= 0)"
        else:
            r["verdict"] = "inconclusive"
            r["label"] = ("hypothesis-generating only" + (" (PROMISING-type: t>=2, <=2 failed gates)"
                          if r["nw_t_d"] >= 2 and len(fails) <= 2 else ""))
    # ---------------- eval odds
    for c in cols:
        hid = R[c]["hypothesis"]
        syms = [s for s in ("ES", "NQ", "YM") if MK[s] in R[c]["markets"]]
        ents = {s: runs[(hid, s)]["entries"] for s in syms}
        tr = T[c]
        ev = eval_summary(tr, ents, hid, single=len(syms) == 1)
        ev.to_csv(os.path.join(HERE, f"eval_{c}.csv"), index=False)
        sub = ev[(ev.window == "2018+") & (ev.consistency == 0.4)]
        R[c]["eval_2018_c40"] = jsonable(sub[[x for x in ("policy", "pass_pct", "within_10", "bust_pct", "twin_pass_pct",
                                                           "twin_within_10", "twin_within_10_p90", "twin_bust_pct",
                                                           "luck_within_10", "days_pass_median") if x in sub.columns]]
                                          .round(2).to_dict(orient="records"))
        sub5 = ev[(ev.window == "2018+") & (ev.consistency == 0.5)]
        R[c]["eval_2018_c50"] = jsonable(sub5[[x for x in ("policy", "pass_pct", "within_10", "bust_pct", "twin_within_10",
                                                            "luck_within_10") if x in sub5.columns]].round(2)
                                         .to_dict(orient="records"))
        sub22 = ev[(ev.window == "2022+") & (ev.consistency == 0.4)]
        R[c]["eval_2022_c40"] = jsonable(sub22[[x for x in ("policy", "pass_pct", "within_10", "bust_pct", "twin_within_10",
                                                             "luck_within_10") if x in sub22.columns]].round(2)
                                         .to_dict(orient="records"))
        log(f"eval {c}")
    # ---------------- standard outputs + trial log
    for c in cols:
        r = R[c]
        D = Dd[c]
        D.to_csv(os.path.join(OUT, "daily", f"{c}.csv"), index=False)
        D[["session", "net_U1"]].rename(columns={"net_U1": "pnl_usd"}).to_csv(os.path.join(G6DIR, f"daily_{c}.csv"),
                                                                               index=False)
        tr = T[c].copy()
        for x in tr.columns:
            if tr[x].dtype == object:
                tr[x] = tr[x].astype(str)
        tr.to_parquet(os.path.join(OUT, "trades", f"{c}.parquet"))
        with open(os.path.join(OUT, "results", f"{c}.json"), "w") as f:
            json.dump(jsonable(r), f, indent=1)
        H.log(c, "+".join(r["markets"]), f"{r['hypothesis']}: {RULE[r['hypothesis']]}", trades=T[c],
              baseline=float(T[c]["c1"].mean()),
              params=dict(rule=RULE[r["hypothesis"]], markets=r["markets"], C1_R=200, c1_seed_k=SEEDK[r["hypothesis"]],
                          stepm_p_family_G6=round(r["stepm_p_family_G6"], 4), nw_t_d=round(r["nw_t_d"], 3),
                          p_d=round(r["p_d"], 4), dsr_d=round(r["dsr_d"], 3), verdict=r["verdict"]),
              note=NOTE)
    with open(os.path.join(HERE, "g6_results.json"), "w") as f:
        json.dump(jsonable(R), f, indent=1)
    # ---------------- summary table
    rows = []
    for c in cols:
        r = R[c]
        e = {x["policy"]: x for x in r["eval_2018_c40"]}
        e3 = e.get("3 micros") or e.get("3 micro") or list(e.values())[1]
        rows.append(dict(col=c, n=r["n_trades"], tr_yr=round(r["trades_per_year"], 1), usd_tr=round(r["usd_per_trade"], 2),
                         c1_tr=round(r["controls_per_trade"]["C1"], 2), d_tr=round(r["mean_d_per_trade"], 2),
                         win=round(r["win_pct"], 1), p_d=round(r["p_d"], 4), t_d=round(r["nw_t_d"], 2),
                         t_net=round(r["nw_t_net"], 2), stepm=round(r["stepm_p_family_G6"], 3), dsr=round(r["dsr_d"], 3),
                         h1=round(r["first_half_usd"]), h2=round(r["second_half_usd"]), y22=round(r["usd_2022plus"]),
                         wo10=round(r["without_top10_usd"]), stress_tr=round(r["cost_stress"]["usd_per_trade"], 2),
                         drift_tr=round(r["controls_per_trade"]["plain_drift"], 2),
                         hdrift_tr=round(r["controls_per_trade"]["hour_drift"], 2), gates_fail=r["n_gates_failed"],
                         ev3_w10=e3.get("within_10"), ev3_twin_w10=e3.get("twin_within_10"),
                         ev3_bust=e3.get("bust_pct"), verdict=r["verdict"]))
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(HERE, "summary_table.csv"), index=False)
    pd.set_option("display.width", 320); pd.set_option("display.max_columns", 40)
    print(tab.to_string())
    log(f"stage 2 done {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
