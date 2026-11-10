"""
v3/exp_g2_onbreak/run_g2.py - G2 (overnight-range break + trend, F3): A2 primary + S2.1-S2.6 + neighbours.
Pre-registered in v3/PREREG.md (sha256 c9aef6629ccc...). Light (v3/data only, <= 3 threads).

Outputs per column <hid>: v3/out/daily/<hid>.csv, v3/out/trades/<hid>.parquet, v3/out/results/<hid>.json,
v3/exp_G2/daily_<hid>.csv (session, pnl_usd at 1 micro, full calendar); summary in exp_g2_onbreak/summary_*.csv.
C1 seeds: 1000*k + chunk; k = 2 for A2 (PREREG 0.3); k = 21..26 for S2.1..S2.6, 31..35 for N2.1..N2.5 (G2 choice).
"""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g2lib as G  # noqa: E402
import harness as H  # noqa: E402
import stats_protocol as sp  # noqa: E402

warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(V3, "out")
EXPG2 = os.path.join(V3, "exp_G2")
SHA = "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
SEED = 20261109
CAL = H.calendar(("NQ", "ES"))
CAL = CAL[CAL <= G.LAST_SESSION]
assert len(CAL) == 3876
YRS = CAL.year.to_numpy()


def cp(x):
    p, ps = sp.conservative_p(sp.boot_pvalue_mean, np.asarray(x, float), B=5000, seed=SEED)
    return float(p), {int(k): float(v) for k, v in ps.items()}


def daily(tr, col):
    g = tr[col].astype(float).groupby(pd.DatetimeIndex(tr["session"])).sum()
    assert g.index.difference(CAL).empty
    return g.reindex(CAL, fill_value=0.0)


def win_mean(x, a, b):
    m = (CAL >= a) & (CAL <= b)
    return float(np.asarray(x)[m].mean())


def per_trade_window(tr, col, a, b):
    s = pd.DatetimeIndex(tr["session"])
    m = (s >= a) & (s <= b)
    return float(tr.loc[m, col].mean()) if m.any() else float("nan")


WINS = {"all": ("2010-01-01", "2025-06-30"), "2010-17": ("2010-01-01", "2017-12-31"),
        "2018-25H1": ("2018-01-01", "2025-06-30"), "2022+": ("2022-01-01", "2025-06-30")}


def analyze(hid, name, sym, tr, tier, k, R=999, n_twins=100, n_eff=45, params=None, slot_range=(187, 252)):
    t0 = time.time()
    tr = tr.copy().reset_index(drop=True)
    sp_ = H.SPEC[sym]
    ym = sym == "YM"
    # ---- C1 (primary control) and hour drift
    c1 = G.c1_draws(sym, tr, R=R, k=k, keep_twins=n_twins)
    tr["c1"] = c1["c_mean"]
    tr["c1_n"] = c1["n_valid"]
    tr["d_c1"] = np.where(np.isfinite(tr["c1"]), tr["pnl_usd"] - tr["c1"], 0.0)
    tr["net_U2"] = G.u2(tr)
    hd = G.c1_draws(sym, tr, R=100, k=k + 500, side_mode="long")
    tr["hour_drift"] = hd["c_mean"]
    tr["drift"] = G.drift_paired(sym, tr)
    c2_rep, _ = G.same_session_controls(sym, tr, n_rep=100, seed=k + 700, mode="random_side")
    rs_rep, _ = G.same_session_controls(sym, tr, n_rep=100, seed=k + 900, mode="random_slot", slot_range=slot_range)
    # ---- daily series (common calendar)
    net = daily(tr, "pnl_usd"); net2 = daily(tr, "net_U2"); gross = daily(tr, "gross_usd")
    ctrl = daily(tr.assign(c=tr["c1"].fillna(0.0)), "c"); dd = daily(tr, "d_c1")
    ntr = tr.groupby(pd.DatetimeIndex(tr["session"])).size().reindex(CAL, fill_value=0)
    D = pd.DataFrame({"net_U1": net, "net_U2": net2, "gross_U1": gross, "ctrl_C1": ctrl, "d": dd, "n_trades": ntr})
    for m in ("ES", "NQ", "YM"):
        D[f"net_{m}"] = net if m == sym else 0.0
    D.index.name = "session"
    D.to_csv(os.path.join(OUT, "daily", f"{hid}.csv"))
    net.rename("pnl_usd").to_frame().to_csv(os.path.join(EXPG2, f"daily_{hid}.csv"))
    tr.to_parquet(os.path.join(OUT, "trades", f"{hid}.parquet"))
    # ---- the judged window (MYM: 2018+ only, PREREG 0.1)
    jm = (CAL >= "2018-01-01") if ym else np.ones(len(CAL), bool)
    x_d, x_n, x_2 = dd.to_numpy()[jm], net.to_numpy()[jm], net2.to_numpy()[jm]
    sess_j = CAL[jm]
    p_d, ps_d = cp(x_d)
    p_net, ps_net = cp(x_n)
    t_d = float(sp.hac_t(x_d)[0]); t_net = float(sp.hac_t(x_n)[0])
    rr_d = sp.robust_report(x_d, sess_j.to_numpy())
    rr_n = sp.robust_report(x_n, sess_j.to_numpy())
    rr_2 = sp.robust_report(x_2, sess_j.to_numpy())
    dsr_d = sp.dsr(x_d, n_eff)
    strat_mean = c1["strat_total"] / len(x_n)
    mc_p = sp.mc_rank_p(x_n.mean(), strat_mean)
    s18 = pd.DatetimeIndex(tr["session"]) >= "2018-01-01"
    g_c = float(tr.loc[s18, "gross_usd"].mean() / tr.loc[s18, "cost_usd"].mean())
    net_pt = float(tr["pnl_usd"].mean()); drift_pt = float(np.nanmean(tr["drift"]))
    hd_pt = float(np.nanmean(tr["hour_drift"]))
    # ---- gates (PREREG 0.5)
    def half(rr, key):
        return rr[key][0]
    gates = {}
    if ym:
        gates["1_d_halves"] = bool(half(rr_d, "2018_25H1") > 0)
        gates["2_net_halves_U2_2018_2022"] = bool(half(rr_2, "2018_25H1") > 0 and half(rr_n, "2018_25H1") > 0
                                                  and rr_n["2022+"][0] > 0)
    else:
        gates["1_d_halves"] = bool(half(rr_d, "2010_17") > 0 and half(rr_d, "2018_25H1") > 0)
        gates["2_net_halves_U2_2018_2022"] = bool(half(rr_2, "2010_17") > 0 and half(rr_2, "2018_25H1") > 0
                                                  and half(rr_n, "2018_25H1") > 0 and rr_n["2022+"][0] > 0)
    yrs_u2 = {y: v for y, v in rr_2["by_year"].items()}
    gates["3_years_pos_U2"] = bool(np.mean([v > 0 for v in yrs_u2.values()]) >= 0.6)
    gates["4_wo_best10"] = bool(rr_n["drop_best"][0] > 0)
    gates["5_winsor"] = bool(rr_n["winsor"][0] > 0)
    gates["6_mc_rank"] = bool(mc_p <= 0.05)
    gates["7_gross_1.5x_cost"] = bool(g_c >= 1.5)
    gates["8_beats_drift"] = bool(net_pt > drift_pt and net_pt > hd_pt)
    n_fail_gates = sum(not v for v in gates.values())
    kill = bool(x_d.mean() <= 0 or rr_n["2018_25H1"][0] <= 0)
    # ---- cost stress (+1 tick each way: fills unchanged, cost + 2 ticks)
    extra = 2 * sp_["tick"] * sp_["usd"]
    x_ns = x_n - (D["n_trades"].to_numpy()[jm] * extra)
    p_net_stress, _ = cp(x_ns)
    # ---- harness stats tables
    calm = H.calendar(sym); calm = calm[calm <= G.LAST_SESSION]
    st = H.stats(tr, calendar_=calm)
    st_d = H.stats(pd.Series(x_d, index=sess_j))
    # ---- eval: fixed 1/3/5 vs C1 twins (zero-timing-edge) and the luck bar
    pols = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
    ev = H.eval(tr, sizing=pols, calendar_=calm)
    tw = [H.eval(t, sizing=pols, calendar_=calm) for t in c1["twins"]]
    if tw:
        keycols = ["pass_pct", "within_10", "bust_pct"]
        T = pd.concat(tw, keys=range(len(tw)), names=["twin"]).reset_index(level=0)
        for c in keycols:
            g = T.groupby(["policy", "consistency", "window"])[c]
            ev[f"twin_{c}_mean"] = [g.mean().get((a, b, w), np.nan) for a, b, w in zip(ev.policy, ev.consistency, ev.window)]
            arr = {kk: v.to_numpy() for kk, v in g}
            ev[f"twin_{c}_rankp"] = [float((1 + np.sum(arr[(a, b, w)] >= r)) / (1 + len(arr[(a, b, w)])))
                                     for a, b, w, r in zip(ev.policy, ev.consistency, ev.window, ev[c])]
    ev.to_csv(os.path.join(HERE, f"eval_{hid}.csv"), index=False)
    # ---- eval-math target check
    dn = net.to_numpy()[jm]
    em = dict(daily_sharpe=float(dn.mean() / dn.std(ddof=1)), share_sessions_traded=float((D["n_trades"].to_numpy()[jm] > 0).mean()),
              win_rate=float((tr["pnl_usd"] > 0).mean()), net_per_trade=net_pt,
              share_profit_wo_best10=float(rr_n["drop_best"][0] / rr_n["all"][0]) if rr_n["all"][0] > 0 else float("nan"))
    res = dict(hid=hid, name=name, market=sym, tier=tier, prereg_sha256=SHA, n_trades=int(len(tr)),
               trades_per_year=float(len(tr) / (len(sess_j) / 252.0)), c1_R=R, c1_seed_k=k,
               c1_valid_draws_min=float(np.nanmin(tr["c1_n"])),
               p_d=p_d, p_d_by_block=ps_d, t_d=t_d, mean_d_day=float(x_d.mean()), mean_d_trade=float(tr["d_c1"].mean()),
               p_net=p_net, p_net_by_block=ps_net, t_net=t_net, mean_net_day=float(x_n.mean()), net_per_trade=net_pt,
               gross_per_trade=float(tr["gross_usd"].mean()), c1_per_trade=float(np.nanmean(tr["c1"])),
               sharpe_ann=float(dn.mean() / dn.std(ddof=1) * np.sqrt(252)),
               dsr_d=dsr_d["dsr"], dsr_N_eff=n_eff, dsr_sr0_ann=dsr_d["sr0_ann"], dsr_sr_ann=dsr_d["sr_ann"],
               mc_rank_p=mc_p, c1_strategy_mean_day_q95=float(np.quantile(strat_mean, 0.95)),
               gross_over_cost_2018=g_c,
               drift_per_trade=drift_pt, hour_drift_per_trade=hd_pt,
               c2_random_side_per_trade=float(c2_rep.mean()), c2_p=float((1 + (c2_rep >= net_pt).sum()) / 101),
               random_slot_same_session_per_trade=float(rs_rep.mean()),
               random_slot_p=float((1 + (rs_rep >= net_pt).sum()) / 101),
               cost_stress_net_per_trade=net_pt - extra, cost_stress_p_net=p_net_stress,
               cost_stress_net_2018_per_trade=per_trade_window(tr, "pnl_usd", "2018-01-01", "2025-06-30") - extra,
               windows_net_per_trade={w: per_trade_window(tr, "pnl_usd", a, b) for w, (a, b) in WINS.items()},
               windows_d_per_trade={w: per_trade_window(tr, "d_c1", a, b) for w, (a, b) in WINS.items()},
               windows_U2_per_trade={w: per_trade_window(tr, "net_U2", a, b) for w, (a, b) in WINS.items()},
               robust_net_U1=rr_n, robust_d=rr_d, robust_net_U2=rr_2,
               net_wo_best10_total=float(rr_n["drop_best"][0] * len(x_n)),
               by_year_net_per_trade={int(y): float(v) for y, v in
                                      tr.groupby(pd.DatetimeIndex(tr["session"]).year)["pnl_usd"].mean().items()},
               by_year_n={int(y): int(v) for y, v in tr.groupby(pd.DatetimeIndex(tr["session"]).year).size().items()},
               long_leg=dict(n=int((tr.d > 0).sum()), net=float(tr.loc[tr.d > 0, "pnl_usd"].mean()),
                             d=float(tr.loc[tr.d > 0, "d_c1"].mean())),
               short_leg=dict(n=int((tr.d < 0).sum()), net=float(tr.loc[tr.d < 0, "pnl_usd"].mean()),
                              d=float(tr.loc[tr.d < 0, "d_c1"].mean())),
               exit_kinds=tr["exit_kind"].value_counts().to_dict(),
               gates=gates, n_failed_gates=n_fail_gates, kill=kill, evalmath=em,
               eval=ev.to_dict(orient="records"), params=params or {}, runtime_s=round(time.time() - t0, 1))
    with open(os.path.join(OUT, "results", f"{hid}.json"), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    st.to_csv(os.path.join(HERE, f"stats_{hid}.csv"), index=False)
    st_d.to_csv(os.path.join(HERE, f"stats_d_{hid}.csv"), index=False)
    H.log(hid, f"M{sym}" if sym != "YM" else "MYM", name, trades=tr, baseline=float(np.nanmean(tr["c1"])),
          params=dict(params or {}, tier=tier, c1_R=R, c1_k=k),
          note=f"prereg sha256 {SHA}; p_d {p_d:.4f} t_d {t_d:.2f} p_net {p_net:.4f}; baseline = C1 mean $/trade")
    H.log(hid + "-cost+1tick", f"M{sym}" if sym != "YM" else "MYM", name + " [cost stress +1 tick each way]",
          trades=tr.assign(pnl_usd=tr["pnl_usd"] - extra), baseline=float(np.nanmean(tr["c1"])) - extra,
          params=dict(params or {}, tier=tier, cost_stress_ticks=1), note=f"prereg sha256 {SHA}; cost stress of {hid}")
    print(f"[{hid}] {name}: n={len(tr)} net/trade ${net_pt:.2f} d/trade ${tr['d_c1'].mean():.2f} p_d {p_d:.4f} "
          f"t_d {t_d:.2f} p_net {p_net:.4f} t_net {t_net:.2f} DSR {dsr_d['dsr']:.3f} mc_p {mc_p:.3f} "
          f"fails {n_fail_gates} kill {kill} ({time.time() - t0:.0f}s)", flush=True)
    return res, dd


def columns():
    """(hid, name, sym, tier, k, builder, params, n_twins)"""
    S_es = H.sessions("ES")
    es_drop = set(S_es.index[S_es["prev_ret_cc"] <= -0.02])
    S_nq = H.sessions("NQ")
    opex = set(S_nq.index[S_nq["opex"].astype(bool)])
    base = dict(stop_mult=2.0, last_end=1260, trend_kind="ema20", exit="16:45")
    return [
        ("A2", "overnight-range break + EMA20 trend, stop 2xATR5, exit 16:45, MNQ", "NQ", "A", 2,
         lambda: G.onbreak_trades("NQ"), base, 200),
        ("S2.1", "A2 rule on MES", "ES", "B", 21, lambda: G.onbreak_trades("ES"), base, 100),
        ("S2.2", "A2 rule on MYM (2018+)", "YM", "B", 22, lambda: G.onbreak_trades("YM"), base, 100),
        ("S2.3", "A2 MNQ skipping sessions after an ES drop <= -2%", "NQ", "B", 23,
         lambda: G.onbreak_trades("NQ", skip=es_drop), dict(base, skip="ES prev_ret_cc <= -0.02"), 100),
        ("S2.4", "A2 MNQ skipping monthly-expiry Fridays", "NQ", "B", 24,
         lambda: G.onbreak_trades("NQ", skip=opex), dict(base, skip="opex"), 100),
        ("S2.5", "5-min opening-range breakout MNQ (09:30 bar side, 09:35 entry, stop other end, exit 16:00)", "NQ",
         "B", 25, lambda: G.orb_trades("NQ"), dict(rule="ORB5", exit="16:00"), 100),
        ("S2.6", "5-min opening-range breakout MES", "ES", "B", 26, lambda: G.orb_trades("ES"),
         dict(rule="ORB5", exit="16:00"), 100),
        ("N2.1", "A2 neighbour: stop 1.5xATR", "NQ", "N", 31, lambda: G.onbreak_trades("NQ", stop_mult=1.5),
         dict(base, stop_mult=1.5), 0),
        ("N2.2", "A2 neighbour: stop 3xATR", "NQ", "N", 32, lambda: G.onbreak_trades("NQ", stop_mult=3.0),
         dict(base, stop_mult=3.0), 0),
        ("N2.3", "A2 neighbour: break bar ending up to 15:30", "NQ", "N", 33,
         lambda: G.onbreak_trades("NQ", last_end=1290), dict(base, last_end="15:30"), 0),
        ("N2.4", "A2 neighbour: trend = sign of the 5-session return", "NQ", "N", 34,
         lambda: G.onbreak_trades("NQ", trend_kind="ret5"), dict(base, trend_kind="ret5"), 0),
        ("N2.5", "A2 neighbour: exit 16:00", "NQ", "N", 35, lambda: G.onbreak_trades("NQ", kx=88),
         dict(base, exit="16:00"), 0),
    ]


def main(only=None):
    os.makedirs(EXPG2, exist_ok=True)
    allres, Dd = {}, {}
    for hid, name, sym, tier, k, build, params, ntw in columns():
        if only and hid not in only:
            continue
        tr = build()
        sr = (187, 187) if params.get("rule") == "ORB5" else (187, 252)
        res, dd = analyze(hid, name, sym, tr, tier, k, R=999, n_twins=ntw,
                          n_eff=30 if hid == "A2" else 45, params=params, slot_range=sr)
        allres[hid] = res
        Dd[hid] = dd
    # Tier B StepM within the G2 columns (the synthesis step redoes it over all of F3)
    tb = [h for h in Dd if h != "A2"]
    if tb:
        DM = np.column_stack([Dd[h].to_numpy() for h in tb])
        sm = sp.stepm(DM, mean_block=10, B=5000, seed=SEED, alpha=0.004)
        for h, t_, p_ in zip(tb, sm["t"], sm["p_adj"]):
            allres[h]["stepm_G2_p_adj"] = float(p_)
            allres[h]["stepm_G2_t"] = float(t_)
            with open(os.path.join(OUT, "results", f"{h}.json")) as f:
                r = json.load(f)
            r["stepm_G2_p_adj"] = float(p_)
            with open(os.path.join(OUT, "results", f"{h}.json"), "w") as f:
                json.dump(r, f, indent=1)
    rows = []
    for h, r in allres.items():
        rows.append(dict(hid=h, market=r["market"], tier=r["tier"], n=r["n_trades"], per_yr=round(r["trades_per_year"], 1),
                         net_trade=r["net_per_trade"], d_trade=r["mean_d_trade"], c1_trade=r["c1_per_trade"],
                         p_d=r["p_d"], t_d=r["t_d"], p_net=r["p_net"], t_net=r["t_net"], sharpe=r["sharpe_ann"],
                         dsr=r["dsr_d"], mc_p=r["mc_rank_p"], g_c=r["gross_over_cost_2018"],
                         net_1017=r["windows_net_per_trade"]["2010-17"], net_1825=r["windows_net_per_trade"]["2018-25H1"],
                         net_22=r["windows_net_per_trade"]["2022+"], d_1017=r["windows_d_per_trade"]["2010-17"],
                         d_1825=r["windows_d_per_trade"]["2018-25H1"], wo10_total=r["net_wo_best10_total"],
                         drift=r["drift_per_trade"], hour_drift=r["hour_drift_per_trade"],
                         stress_net=r["cost_stress_net_per_trade"], stress_p=r["cost_stress_p_net"],
                         stepm=r.get("stepm_G2_p_adj", np.nan), fails=r["n_failed_gates"], kill=r["kill"]))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "summary_g2.csv"), index=False)
    pd.set_option("display.width", 300)
    print(out.round(4).to_string())


if __name__ == "__main__":
    main(sys.argv[1:] or None)
