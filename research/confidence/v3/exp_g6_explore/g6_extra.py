"""
v3/exp_g6_explore/g6_extra.py - EXTRA EXPLORATORY decompositions (NOT pre-registered; labelled exploratory, logged as
trials, hypothesis-generating only; never part of the pre-registered G6 columns or their StepM).
Chosen after seeing the G6 primaries (X1a = the only positive-sign idea; X2 MES = the only column whose timing beats C1
with t > 2 while the net loses), to tell the next round where the effect sits, not to rescue anything:
  X1ax_on   : ES prev_ret_cc <= -2%: long 18:00 -> 09:30 (is the rebound overnight?)
  X1ax_full : ES prev_ret_cc <= -2%: long 18:00 -> 16:45 (whole next session)
  X2x_nostop: X2 without the stop (target = prev 16:00 close, else exit 11:00) - the practitioner 'gaps fill' claim
  X2x_time  : X2 side, no stop and no target, 09:30 -> 11:00 (pure direction information of the gap)
Same machinery as g6_run / g6_stage2 (C1 R = 200, conservative bootstrap, gates, eval vs 10 C1 twins).
"""
import json
import os
import time
import warnings

import numpy as np
import pandas as pd

import harness as H
import stats_protocol as sp
import g6_signals as G
import g6_run as R6
import g6_stage2 as S2

warnings.simplefilter("ignore")
HERE = R6.HERE


def x1ax(es_S, entry, exit_):
    def fn(S, B):
        cond = (S["prev_ret_cc"] if es_S is None else es_S["prev_ret_cc"].reindex(S.index)) <= -0.02
        return G._ent(S, cond, entry, exit_, np.ones(len(S)))
    return fn


def x2x(use_target):
    def fn(S, B):
        e = G.x2_fn(S, B)
        e["stop_pts"] = np.nan
        if not use_target:
            e["target_pts"] = np.nan
        return e
    return fn


EXTRA = {"X1ax_on": ("F2", "ES prev_ret_cc <= -2%: long 18:00 -> 09:30"),
         "X1ax_full": ("F2", "ES prev_ret_cc <= -2%: long 18:00 -> 16:45"),
         "X2x_nostop": ("F3", "X2 gap fade without stop: target prev 16:00 close, else exit 11:00"),
         "X2x_time": ("F3", "X2 gap fade side, no stop/target, 09:30 -> 11:00")}
SEEDX = {"X1ax_on": 71, "X1ax_full": 72, "X2x_nostop": 73, "X2x_time": 74}


def fns(sym, es):
    ext = None if sym == "ES" else es
    return {"X1ax_on": x1ax(ext, "1800", "0930"), "X1ax_full": x1ax(ext, "1800", "1645"),
            "X2x_nostop": x2x(True), "X2x_time": x2x(False)}


def main():
    t0 = time.time()
    es = H.sessions("ES")
    R6.SEEDK.update(SEEDX)
    S2.RULE.update({k: v[1] for k, v in EXTRA.items()})
    la = []
    for sym in ("ES", "NQ"):
        for hid, fn in fns(sym, es).items():
            r = H.lookahead_check(fn, sym, n_cuts=20, seed=1, tfs=(15,))
            la.append(dict(sym=sym, hid=hid, ok=bool(r.same.all()), n=int(r.n_full.sum())))
    print(pd.DataFrame(la).to_string(), flush=True)
    runs = {}
    for sym in R6.SYMS:
        for hid, fn in fns(sym, es).items():
            R6.log(f"run {hid} {sym}")
            runs[(hid, sym)] = R6.run_market(hid, sym, fn, es)
    res, Dd, T = {}, {}, {}
    for hid in EXTRA:
        for col, ss in [(hid, R6.SYMS)] + [(f"{hid}_{R6.MK[s]}", (s,)) for s in R6.SYMS]:
            r, D, tr = R6.column_report(hid, col, [runs[(hid, s)] for s in ss], EXTRA[hid][0])
            r["tier"] = "EXTRA-exploratory (not pre-registered)"
            res[col], Dd[col], T[col] = r, D, tr
            R6.log(f"report {col}")
    cols = list(res)
    Dm = pd.DataFrame({c: Dd[c]["d"].to_numpy() for c in cols})
    sm = sp.stepm(Dm.to_numpy(), mean_block=10, B=5000, seed=R6.SEED_BOOT, alpha=0.004)
    for c, p in zip(cols, sm["p_adj"]):
        r = res[c]
        r["stepm_p_extra16"] = float(p)
        neff = S2.FLOOR[r["family"]] + 16
        r["N_eff"] = neff
        r["dsr_d"] = sp.dsr(Dd[c]["d"].to_numpy(), neff)["dsr"]
        r["verdict"] = "no_edge" if r["kill"] else "inconclusive"
        ents = {s: runs[(r["hypothesis"], s)]["entries"] for s in R6.SYMS if R6.MK[s] in r["markets"]}
        ev = S2.eval_summary(T[c], ents, r["hypothesis"], single=len(ents) == 1)
        ev.to_csv(os.path.join(HERE, f"eval_{c}.csv"), index=False)
        sub = ev[(ev.window == "2018+") & (ev.consistency == 0.4)]
        r["eval_2018_c40"] = S2.jsonable(sub[[x for x in ("policy", "pass_pct", "within_10", "bust_pct", "twin_pass_pct",
                                                          "twin_within_10", "twin_bust_pct", "luck_within_10")
                                              if x in sub.columns]].round(2).to_dict(orient="records"))
        Dd[c].to_csv(os.path.join(R6.OUT, "daily", f"{c}.csv"), index=False)
        Dd[c][["session", "net_U1"]].rename(columns={"net_U1": "pnl_usd"}).to_csv(
            os.path.join(R6.G6DIR, f"daily_{c}.csv"), index=False)
        tr = T[c].copy()
        for x in tr.columns:
            if tr[x].dtype == object:
                tr[x] = tr[x].astype(str)
        tr.to_parquet(os.path.join(R6.OUT, "trades", f"{c}.parquet"))
        with open(os.path.join(R6.OUT, "results", f"{c}.json"), "w") as f:
            json.dump(S2.jsonable(r), f, indent=1)
        H.log(c, "+".join(r["markets"]), f"{r['hypothesis']} (EXTRA exploratory): {EXTRA[r['hypothesis']][1]}",
              trades=T[c], baseline=float(T[c]["c1"].mean()),
              params=dict(rule=EXTRA[r["hypothesis"]][1], markets=r["markets"], C1_R=200, seed_k=SEEDX[r["hypothesis"]],
                          nw_t_d=round(r["nw_t_d"], 3), p_d=round(r["p_d"], 4), stepm_extra=round(float(p), 4)),
              note=R6.NOTE + "; EXTRA exploratory decomposition chosen after seeing the primaries")
    with open(os.path.join(HERE, "g6_extra_results.json"), "w") as f:
        json.dump(S2.jsonable(res), f, indent=1)
    rows = []
    for c in cols:
        r = res[c]
        cp = r["controls_per_trade"]
        e = {x["policy"]: x for x in r["eval_2018_c40"]}
        e3 = list(e.values())[1]
        rows.append(dict(col=c, n=r["n_trades"], tr_yr=round(r["trades_per_year"], 1), usd_tr=round(r["usd_per_trade"], 2),
                         c1=round(cp["C1"], 2), d_tr=round(r["mean_d_per_trade"], 2), hdrift=round(cp["hour_drift"], 2),
                         win=round(r["win_pct"], 1), p_d=round(r["p_d"], 4), t_d=round(r["nw_t_d"], 2),
                         t_net=round(r["nw_t_net"], 2), stepm=round(r["stepm_p_extra16"], 3), dsr=round(r["dsr_d"], 3),
                         h1=round(r["first_half_usd"]), h2=round(r["second_half_usd"]), y22=round(r["usd_2022plus"]),
                         wo10=round(r["without_top10_usd"]), stress=round(r["cost_stress"]["usd_per_trade"], 2),
                         gf=r["n_gates_failed"], ev3_w10=e3.get("within_10"), ev3_twin=e3.get("twin_within_10"),
                         verdict=r["verdict"]))
    tab = pd.DataFrame(rows)
    tab.to_csv(os.path.join(HERE, "summary_extra.csv"), index=False)
    pd.set_option("display.width", 320); pd.set_option("display.max_columns", 40)
    print(tab.to_string())
    for c in ("X1ax_on", "X1ax_full", "X2x_nostop_MES"):
        print(c, res[c]["by_year_u1"])
    R6.log(f"extra done {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
