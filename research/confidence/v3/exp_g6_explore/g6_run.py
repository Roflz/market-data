"""
v3/exp_g6_explore/g6_run.py - G6 EXPLORATORY group (Tier B only): X1a, X1b, X2, X3, X4, X5 (PREREG.md section 3).
Light (v3/data only, <= 3 threads). For every hypothesis: the 3-market basket (1 MES + 1 MNQ + 1 MYM, MYM 2018+) is the
primary column, MES / MNQ / MYM alone are reported columns. Each column: C1 matched control (R = 200, chunks of 100,
seed 1000 k + chunk + market offset), d_t, conservative bootstrap p, NW t, DSR, gates 1-9, drift / hour drift /
C2 random side / standard_report controls, cost stress (+1 tick each way), eval (fixed 1/3/5) vs 10 C1 twins and the
v2 luck bar. Outputs: v3/out/{daily,trades,results}/<hid>.*, v3/exp_G6/daily_<hid>.csv, exp_g6_explore/*.

Run (from research/confidence):
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/exp_g6_explore OMP_NUM_THREADS=3 \
      nice -n 5 python3 -W ignore v3/exp_g6_explore/g6_run.py
"""
import json
import os
import pickle
import sys
import time
import warnings

import numpy as np
import pandas as pd

import harness as H
import stats_protocol as sp
import g6_signals as G

warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
OUT = os.path.join(V3, "out")
G6DIR = os.path.join(V3, "exp_G6")
for d_ in ("daily", "trades", "results"):
    os.makedirs(os.path.join(OUT, d_), exist_ok=True)
os.makedirs(G6DIR, exist_ok=True)
SHA = open(os.path.join(OUT, "prereg", "PREREG.md.sha256")).read().split()[0]
NOTE = f"G6 exploratory Tier B; prereg sha256 {SHA}"
LAST = pd.Timestamp("2025-06-27")
CAL = H.calendar(("NQ", "ES"))
CAL = CAL[CAL <= LAST]
assert len(CAL) == 3876, len(CAL)
P_REF = {"NQ": 20789.6, "ES": 5843.2, "YM": 42516.3}
MK = {"ES": "MES", "NQ": "MNQ", "YM": "MYM"}
SYMS = ("ES", "NQ", "YM")
SEEDK = {"X1a": 611, "X1b": 612, "X2": 62, "X3": 63, "X4": 64, "X5": 65}
MOFF = {"ES": 0, "NQ": 10, "YM": 20}
R_C1 = 200
B_BOOT = 5000
SEED_BOOT = 20261109
YRS = CAL.year.to_numpy()
H1 = YRS <= 2017
H2 = YRS >= 2018
H22 = YRS >= 2022


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def daily(tr, col="pnl_usd"):
    if tr is None or not len(tr):
        return pd.Series(0.0, index=CAL)
    return H.daily_pnl(tr, calendar_=CAL, col=col)


def c1(sym, e, hid):
    """C1 draws: same marks, side, stop/target distance, random session of the same year. Returns (c_i per tid,
    per-rep daily-mean net over CAL (length R), C1 trades frame (rep, tid, pnl))."""
    parts = []
    for ch in range(R_C1 // 100):
        rt = H.random_time_trades(sym, e, n_rep=100, seed=1000 * SEEDK[hid] + ch + MOFF[sym], keep_session=False,
                                  keep_marks=True, keep_side=True)
        rt["rep"] = rt["rep"] + 100 * ch
        parts.append(rt[["tid", "rep", "session", "pnl_usd"]])
    C = pd.concat(parts, ignore_index=True)
    ci = C.groupby("tid")["pnl_usd"].mean()
    rep_sum = C.groupby("rep")["pnl_usd"].sum().reindex(range(R_C1), fill_value=0.0)
    return ci, rep_sum, C


def per_trade_u2(tr, sym):
    g = tr["d"].to_numpy() * (tr["exit_px"].to_numpy() - tr["entry_px"].to_numpy()) / tr["entry_px"].to_numpy()
    return g * P_REF[sym] * H.SPEC[sym]["usd"] - tr["cost_usd"].to_numpy()


def run_market(hid, sym, fn, S_es):
    S = H.sessions(sym)
    B = {15: H.bars(sym, 15)} if hid == "X3" else {}
    e = fn(S, B)
    e = e[pd.DatetimeIndex(e["session"]) <= LAST].reset_index(drop=True)
    e["tid"] = np.arange(len(e))
    tr = H.time_trades(sym, e)
    dropped = tr.attrs.get("dropped", {})
    tr["net_u2"] = per_trade_u2(tr, sym)
    ci, rep_sum, C = c1(sym, e, hid)
    tr["c1"] = tr["tid"].map(ci)
    nmiss = int(tr["c1"].isna().sum())
    tr["c1"] = tr["c1"].fillna(tr["c1"].mean())
    tr["dval"] = tr["pnl_usd"] - tr["c1"]
    tr["stress"] = tr["pnl_usd"] - 2 * H.SPEC[sym]["tick"] * H.SPEC[sym]["usd"]
    # controls
    rep = H.standard_report(sym, e.drop(columns=["tid"]), n_rep=100, seed=1000 * SEEDK[hid] + 500 + MOFF[sym])
    c2 = H.random_time_trades(sym, e.drop(columns=["tid"]), n_rep=100, seed=1000 * SEEDK[hid] + 700 + MOFF[sym],
                              keep_session=True, keep_marks=True, keep_side=False)
    out = dict(sym=sym, entries=e, trades=tr, c1_rep_sum=rep_sum, c1_trades=C, dropped=dropped, c1_missing=nmiss,
               drift=rep["drift"], hour_drift=rep["hour_drift"], random=rep["random"], c2=c2,
               vs_drift=rep["vs_drift"], vs_hour_drift=rep["vs_hour_drift"],
               vs_random=rep["vs_random"], vs_c2=H.control_report(tr, c2), vs_c1=H.control_report(
                   tr, C.assign(pnl_usd=C["pnl_usd"])), stats=rep["stats"])
    return out


def yearly_share(x, two_year=False):
    yr = YRS.copy()
    if two_year:
        yr = 2010 + (yr - 2010) // 2 * 2
    s = pd.Series(x).groupby(yr).sum()
    return float((s > 0).mean()), {int(k): round(float(v), 2) for k, v in s.items()}


def column_report(hid, col, parts, fam):
    """parts: list of run_market dicts (one per market of this column). Returns (results dict, daily frame)."""
    tr = pd.concat([p["trades"] for p in parts], ignore_index=True)
    net = daily(tr).to_numpy()
    u2 = daily(tr, "net_u2").to_numpy()
    gross = daily(tr, "gross_usd").to_numpy()
    ctrl = daily(tr, "c1").to_numpy()
    dd = daily(tr, "dval").to_numpy()
    stress = daily(tr, "stress").to_numpy()
    ntr = tr.groupby(pd.DatetimeIndex(tr["session"])).size().reindex(CAL, fill_value=0).to_numpy()
    D = pd.DataFrame({"session": CAL.strftime("%Y-%m-%d"), "net_U1": net, "net_U2": u2, "gross_U1": gross,
                      "ctrl_C1": ctrl, "d": dd, "n_trades": ntr})
    for s in SYMS:
        sub = tr[tr["market"] == s]
        D[f"net_{s}"] = daily(sub).to_numpy() if len(sub) else 0.0
    # primary statistic
    p_d, p_d_blocks = sp.conservative_p(sp.boot_pvalue_mean, dd, B=B_BOOT, seed=SEED_BOOT)
    p_net, _ = sp.conservative_p(sp.boot_pvalue_mean, net, B=B_BOOT, seed=SEED_BOOT)
    t_d = sp.hac_t(dd)[0]
    t_net = sp.hac_t(net)[0]
    t_stress = sp.hac_t(stress)[0]
    rr_net = sp.robust_report(net, CAL.to_numpy())
    rr_d = sp.robust_report(dd, CAL.to_numpy())
    # C1 rank p: real mean daily net vs R C1 strategy means (basket: same rep index summed over markets)
    rep_tot = sum(p["c1_rep_sum"] for p in parts) / len(CAL)
    mc_p = sp.mc_rank_p(net.mean(), rep_tot.to_numpy())
    # gross / cost 2018-25H1
    s2 = pd.DatetimeIndex(tr["session"]).year >= 2018
    g2 = float(tr.loc[s2, "gross_usd"].mean()) if s2.any() else np.nan
    c2_ = float(tr.loc[s2, "cost_usd"].mean()) if s2.any() else np.nan
    # drift / hour drift per trade (pooled)
    dr = pd.concat([p["drift"] for p in parts]); hd = pd.concat([p["hour_drift"] for p in parts])
    c2t = pd.concat([p["c2"] for p in parts])
    rnd = pd.concat([p["random"] for p in parts])
    net_pt = float(tr["pnl_usd"].mean())
    drift_pt = float(dr["pnl_usd"].mean())
    hdrift_pt = float(hd["pnl_usd"].mean())
    c1_pt = float(tr["c1"].mean())
    c2_pt = float(c2t["pnl_usd"].mean())
    rnd_pt = float(rnd["pnl_usd"].mean())
    two = hid.startswith("X1")
    share_u2, yr_u2 = yearly_share(u2)
    share_u2_2y, yr_u2_2y = yearly_share(u2, two_year=True)
    lo, hi = np.quantile(net[net != 0], [0.01, 0.99])
    wins = float(np.clip(net, lo, hi).mean())
    keep = np.ones(len(net), bool); keep[np.argsort(-net)[:10]] = False
    wo10 = float(np.where(keep, net, 0).sum())
    stat_tab = H.stats(tr, calendar_=CAL)
    stress_tab = H.stats(tr.assign(pnl_usd=tr["stress"]), calendar_=CAL, n_boot=1000)
    gates = {
        "1_d_pos_both_halves": bool(dd[H1].mean() > 0 and dd[H2].mean() > 0),
        "2_u2_pos_both_halves_u1_pos_2018_2022": bool(u2[H1].mean() > 0 and u2[H2].mean() > 0 and net[H2].mean() > 0
                                                      and net[H22].mean() > 0),
        "3_years_pos_u2_ge_60pct": bool((share_u2_2y if two else share_u2) >= 0.6),
        "4_net_pos_wo_10_best": bool(wo10 > 0),
        "5_winsor_pos": bool(wins > 0),
        "6_c1_rank_p_le_0.05": bool(mc_p <= 0.05),
        "7_gross_ge_1.5x_cost_2018": bool(g2 >= 1.5 * c2_) if np.isfinite(g2) else False,
        "8_beats_drift_and_hour_drift": bool(net_pt > drift_pt and net_pt > hdrift_pt),
    }
    mk_net = {}
    for s in SYMS:
        sub = tr[tr["market"] == s]
        if len(sub):
            mk_net[MK[s]] = float(sub["pnl_usd"].mean())
    if len(parts) > 1:
        gates["9_net_pos_2of3_markets"] = bool(sum(v > 0 for v in mk_net.values()) >= 2)
    kill = bool(dd.mean() <= 0 or net[H2].mean() <= 0)
    res = dict(hid=col, hypothesis=hid, family=fam, tier="B-exploratory", markets=[MK[p["sym"]] for p in parts],
               n_trades=int(len(tr)), trades_per_year=float(len(tr) / (len(CAL) / 252.0)),
               usd_per_trade=net_pt, gross_per_trade=float(tr["gross_usd"].mean()),
               cost_per_trade=float(tr["cost_usd"].mean()), win_pct=float(100 * (tr["pnl_usd"] > 0).mean()),
               mean_d_day=float(dd.mean()), mean_d_per_trade=float(tr["dval"].mean()), p_d=p_d,
               p_d_blocks={str(k): v for k, v in p_d_blocks.items()}, p_net=p_net, nw_t_d=float(t_d),
               nw_t_net=float(t_net), sharpe_annual=float(net.mean() / net.std(ddof=1) * np.sqrt(252)),
               sharpe_annual_d=float(dd.mean() / dd.std(ddof=1) * np.sqrt(252)),
               first_half_usd=float(net[H1].sum()), second_half_usd=float(net[H2].sum()),
               usd_2022plus=float(net[H22].sum()), total_usd=float(net.sum()), without_top10_usd=wo10,
               per_trade_2010_17=float(tr.loc[~s2, "pnl_usd"].mean()) if (~s2).any() else None,
               per_trade_2018_25H1=float(tr.loc[s2, "pnl_usd"].mean()) if s2.any() else None,
               per_trade_2022plus=float(tr.loc[pd.DatetimeIndex(tr["session"]).year >= 2022, "pnl_usd"].mean()),
               u2_mean_day_halves=[float(u2[H1].mean()), float(u2[H2].mean())],
               d_mean_day_halves=[float(dd[H1].mean()), float(dd[H2].mean())],
               share_years_pos_u2=share_u2, share_2yr_blocks_pos_u2=share_u2_2y, by_year_u2=yr_u2,
               by_year_u1={int(k): round(float(v), 2) for k, v in pd.Series(net).groupby(YRS).sum().items()},
               winsor_mean_day=wins, mc_rank_p=mc_p, gross_2018=g2, cost_2018=c2_,
               controls_per_trade=dict(net=net_pt, C1=c1_pt, C2_random_side=c2_pt, plain_drift=drift_pt,
                                       hour_drift=hdrift_pt, random_marks_side=rnd_pt),
               per_market_usd_per_trade=mk_net,
               cost_stress=dict(usd_per_trade=float(tr["stress"].mean()), nw_t_net=float(t_stress),
                                total=float(stress.sum())),
               robust_net=rr_net, robust_d=rr_d, gates=gates, n_gates_failed=int(sum(not v for v in gates.values())),
               kill=kill, dropped=[p["dropped"] for p in parts], c1_missing=sum(p["c1_missing"] for p in parts),
               stats_table=stat_tab.round(4).to_dict(orient="records"),
               stress_table=stress_tab[["span", "n_trades", "mean", "t", "p_boot"]].round(4).to_dict(orient="records"))
    return res, D, tr


def main():
    t0 = time.time()
    es = H.sessions("ES")
    runs = {}
    for sym in SYMS:
        for hid, (fn, fam, _) in G.signal_fns(sym, es).items():
            log(f"run {hid} {sym}")
            runs[(hid, sym)] = run_market(hid, sym, fn, es)
    fams = {h: f for h, (_, f, _) in G.signal_fns("ES", es).items()}
    results, dailies, trades = {}, {}, {}
    for hid in SEEDK:
        cols = [(hid, SYMS)] + [(f"{hid}_{MK[s]}", (s,)) for s in SYMS]
        for col, ss in cols:
            log(f"report {col}")
            res, D, tr = column_report(hid, col, [runs[(hid, s)] for s in ss], fams[hid])
            results[col], dailies[col], trades[col] = res, D, tr
    with open(os.path.join(HERE, "g6_stage1.pkl"), "wb") as f:
        pickle.dump(dict(results=results, dailies=dailies, trades=trades,
                         runs={k: {kk: v for kk, v in r.items() if kk in ("entries", "c1_rep_sum", "sym", "dropped")}
                               for k, r in runs.items()}), f)
    log(f"stage 1 done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
