"""
G1 report stage: statistics, gates, controls, eval, standard outputs, trial log (reads exp_g1_noiseband/cache/).

Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/exp_g1_noiseband OMP_NUM_THREADS=3 \
      python3 v3/exp_g1_noiseband/report_g1.py [cols...] [--no-twins]
"""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g1lib as G                        # noqa: E402
from g1lib import H, sp                  # noqa: E402

warnings.filterwarnings("ignore")
CACHE = os.path.join(HERE, "cache")
OUT = os.path.join(G.V3, "out")
EXPG1 = os.path.join(G.V3, "exp_G1")
CAL = G.cal()
YM_START = pd.Timestamp("2018-01-01")
LABELS = {
    "A1": "noise band variant A, MNQ (Tier A primary)",
    "S1.1": "noise band A on MES", "S1.2": "noise band A on MYM", "S1.3": "noise band A, 3-market basket",
    "S1.4": "A1 MNQ, only mid/top tercile of trailing 20-session RTH vol",
    "S1.5": "A1 MNQ, skip sessions after ES prev_ret_cc <= -2%", "S1.6": "A1 MNQ, exit 16:45 instead of 16:00",
    "N1.lb10": "neighbour: lookback 10", "N1.lb20": "neighbour: lookback 20",
    "N1.hour": "neighbour: decisions on the hour only", "N1.cost": "neighbour: +1 tick each way cost (A1 trades)",
}
KIND = {"A1": "primary", "S1.1": "secondary", "S1.2": "secondary", "S1.3": "secondary", "S1.4": "secondary",
        "S1.5": "secondary", "S1.6": "secondary", "N1.lb10": "neighbour", "N1.lb20": "neighbour",
        "N1.hour": "neighbour", "N1.cost": "neighbour"}
PARAMS = {
    "A1": dict(market="MNQ", lookback=14, decisions="10:00-15:30 every 30 min", exit="16:00 (early 13:00)"),
    "S1.1": dict(market="MES", lookback=14), "S1.2": dict(market="MYM", lookback=14),
    "S1.3": dict(market="MES+MNQ+MYM", lookback=14),
    "S1.4": dict(market="MNQ", filter="mean prev_rv_rth 20 sessions in mid/top tercile of expanding history",
                 burn_in=250),
    "S1.5": dict(market="MNQ", filter="skip ES prev_ret_cc <= -0.02"), "S1.6": dict(market="MNQ", exit="16:45"),
    "N1.lb10": dict(market="MNQ", lookback=10), "N1.lb20": dict(market="MNQ", lookback=20),
    "N1.hour": dict(market="MNQ", decisions="10:00-15:00 on the hour"),
    "N1.cost": dict(market="MNQ", extra_cost="+1 tick each way"),
}


def load_col(hid):
    """-> list of (sym, trades, M) components."""
    if hid == "S1.3":
        return load_col("A1") + load_col("S1.1") + load_col("S1.2")
    if hid in ("S1.4", "S1.5"):
        (sym, tr, M), = load_col("A1")
        mk = np.load(os.path.join(CACHE, f"mask_{hid}.npy"))
        return [(sym, tr.loc[mk].reset_index(drop=True), M[mk])]
    if hid == "N1.cost":
        (sym, tr, M), = load_col("A1")
        extra = 2 * H.SPEC[sym]["tick"] * H.SPEC[sym]["usd"]
        tr = tr.copy()
        tr["cost_usd"] = tr["cost_usd"] + extra
        tr["pnl_usd"] = tr["pnl_usd"] - extra
        return [(sym, tr, M - extra)]
    tr = pd.read_parquet(os.path.join(CACHE, f"tr_{hid}.parquet"))
    M = np.load(os.path.join(CACHE, f"M_{hid}.npy"))
    return [(tr["market"].iloc[0], tr, M)]


def entries_of(tr):
    return tr[["session", "entry", "exit", "d"]].copy()


def analyse(hid, n_twins=200, do_eval=True):
    t0 = time.time()
    comps = load_col(hid)
    syms = [c[0] for c in comps]
    ym_only = syms == ["YM"]
    cal = CAL[CAL >= YM_START] if ym_only else CAL
    n_days = len(cal)
    sess_all = np.datetime_as_string(cal.to_numpy(), unit="D")
    trs = []
    net = pd.Series(0.0, index=CAL); u2d = net.copy(); gross = net.copy(); ctrl = net.copy(); dd = net.copy()
    ntr = net.copy()
    per_mkt = {m: net.copy() for m in ("ES", "NQ", "YM")}
    null_tot = np.zeros(999)
    for sym, tr, M in comps:
        c = np.nanmean(M, axis=1)
        tr = tr.copy()
        tr["c1"] = c
        tr["d_c1"] = tr["pnl_usd"].to_numpy() - c
        tr["u2"] = G.u2(tr, sym)
        trs.append(tr)
        net += G.daily(tr.pnl_usd, tr.session, CAL)
        u2d += G.daily(tr.u2, tr.session, CAL)
        gross += G.daily(tr.gross_usd, tr.session, CAL)
        ctrl += G.daily(c, tr.session, CAL)
        dd += G.daily(tr.d_c1, tr.session, CAL)
        ntr += G.daily(np.ones(len(tr)), tr.session, CAL)
        per_mkt[sym] += G.daily(tr.pnl_usd, tr.session, CAL)
        null_tot += np.nansum(M, axis=0)
    T = pd.concat(trs, ignore_index=True)
    # ---- standard daily output (full common calendar)
    daily_df = pd.DataFrame({"session": CAL.strftime("%Y-%m-%d"), "net_U1": net.values, "net_U2": u2d.values,
                             "gross_U1": gross.values, "ctrl_C1": ctrl.values, "d": dd.values,
                             "n_trades": ntr.values.astype(int), "net_ES": per_mkt["ES"].values,
                             "net_NQ": per_mkt["NQ"].values, "net_YM": per_mkt["YM"].values})
    daily_df.to_csv(os.path.join(OUT, "daily", f"{hid}.csv"), index=False)
    pd.DataFrame({"session": daily_df.session, "pnl_usd": daily_df.net_U1}).to_csv(
        os.path.join(EXPG1, f"daily_{hid}.csv"), index=False)
    T.to_parquet(os.path.join(OUT, "trades", f"{hid}.parquet"))
    # ---- tests on the column's own calendar (MYM: 2018+)
    x_d, x_n, x_u2 = dd.reindex(cal).values, net.reindex(cal).values, u2d.reindex(cal).values
    p_d, p_d_blocks = G.cons_p(x_d)
    p_net, p_net_blocks = G.cons_p(x_n)
    t_d, t_n = float(sp.hac_t(x_d)[0]), float(sp.hac_t(x_n)[0])
    rep_n = sp.robust_report(x_n, sess_all if not ym_only else np.datetime_as_string(cal.to_numpy(), unit="D"))
    rep_d = sp.robust_report(x_d, np.datetime_as_string(cal.to_numpy(), unit="D"))
    rep_u2 = sp.robust_report(x_u2, np.datetime_as_string(cal.to_numpy(), unit="D"))
    real_mean = x_n.mean()
    null_means = null_tot / n_days
    mc_p = sp.mc_rank_p(real_mean, null_means)
    s_tr = pd.DatetimeIndex(T.session)
    h2 = (s_tr >= pd.Timestamp("2018-01-01"))
    g_over_c = float(T.loc[h2, "gross_usd"].mean() / T.loc[h2, "cost_usd"].mean()) if h2.any() else np.nan
    # ---- controls (per market, summed over the basket)
    drift_n = hd_n = c2_n = 0.0
    drift_tot = hd_tot = c2_tot = 0.0
    std_tables = {}
    ctrl_by_win = {}
    for sym, tr, M in comps:
        e = entries_of(tr)
        dr = H.drift_trades(sym, e)
        hd = H.hour_drift_trades(sym, e, n_rep=100, seed=11)
        c2 = H.random_time_trades(sym, e, n_rep=100, seed=12, keep_session=True, keep_marks=True, keep_side=False)
        drift_tot += dr.pnl_usd.sum(); drift_n += len(dr)
        hd_tot += hd.pnl_usd.sum() / 100.0; hd_n += len(hd) / 100.0
        c2_tot += c2.pnl_usd.sum() / 100.0; c2_n += len(c2) / 100.0
        if len(comps) == 1:
            ctrl_by_win = dict(drift=H.control_report(tr, dr).round(3).to_dict("records"),
                               hour_drift=H.control_report(tr, hd).round(3).to_dict("records"),
                               random_side_C2=H.control_report(tr, c2).round(3).to_dict("records"))
    net_pt = float(T.pnl_usd.mean())
    drift_pt, hd_pt, c2_pt = drift_tot / drift_n, hd_tot / hd_n, c2_tot / c2_n
    # ---- harness stats tables
    st = H.stats(T, calendar_=cal)
    st_u2 = H.stats(T, calendar_=cal, col="u2")
    st_d = H.stats(T, calendar_=cal, col="d_c1")
    legs = {}
    for side, nm in ((1, "long"), (-1, "short")):
        sub = T[T.d == side]
        legs[nm] = dict(n=len(sub), usd_per_trade=float(sub.pnl_usd.mean()),
                        d_per_trade=float(sub.d_c1.mean()),
                        t_net=float(H.stats(sub, calendar_=cal, n_boot=10).set_index("span").loc["all", "t"]))
    by_mkt = {}
    for sym, tr, M in comps:
        m_ = T.market == sym
        by_mkt[H.SPEC[sym]["micro"]] = dict(n=int(m_.sum()), usd_per_trade=float(T.loc[m_, "pnl_usd"].mean()),
                                            d_per_trade=float(T.loc[m_, "d_c1"].mean()))
    # ---- gates (PREREG 0.5)
    yrs_u2 = {y: v for y, v in rep_u2["by_year"].items() if (not ym_only) or y >= 2018}
    share_pos_u2 = float(np.mean([v > 0 for v in yrs_u2.values()]))
    gates = {
        "1_d_pos_both_halves": bool((ym_only or rep_d["2010_17"][0] > 0) and rep_d["2018_25H1"][0] > 0),
        "2_u2_pos_both_halves_u1_pos_2018_2022": bool((ym_only or rep_u2["2010_17"][0] > 0)
                                                       and rep_u2["2018_25H1"][0] > 0
                                                       and rep_n["2018_25H1"][0] > 0 and rep_n["2022+"][0] > 0),
        "3_years_pos_u2_ge_60pct": bool(share_pos_u2 >= 0.6),
        "4_u1_pos_wo_10_best": bool(rep_n["drop_best"][0] > 0),
        "5_winsorised_pos": bool(rep_n["winsor"][0] > 0),
        "6_c1_rank_p_le_005": bool(mc_p <= 0.05),
        "7_gross_ge_1.5x_cost_2018": bool(g_over_c >= 1.5),
        "8_beats_drift_and_hour_drift": bool(net_pt > drift_pt and net_pt > hd_pt),
    }
    if hid == "S1.3":
        pos_mk = sum(1 for k, v in by_mkt.items() if v["usd_per_trade"] > 0)
        gates["9_basket_pos_2of3"] = bool(pos_mk >= 2)
    failed = [k for k, v in gates.items() if not v]
    kill = bool(x_d.mean() <= 0 or rep_n["2018_25H1"][0] <= 0)
    dsr45 = sp.dsr(x_d, 45)
    res = dict(
        hid=hid, label_text=LABELS[hid], kind=KIND[hid], markets=[H.SPEC[s]["micro"] for s in syms],
        prereg_sha256=G.PREREG_SHA, calendar=f"{cal[0].date()}..{cal[-1].date()} ({n_days} sessions)",
        n_trades=int(len(T)), trades_per_year=float(len(T) / (n_days / 252.0)),
        share_sessions_traded=float((ntr.reindex(cal) > 0).mean()),
        usd_per_trade=net_pt, gross_per_trade=float(T.gross_usd.mean()), cost_per_trade=float(T.cost_usd.mean()),
        d_per_trade=float(T.d_c1.mean()), c1_per_trade=float(T.c1.mean()),
        mean_daily_d=float(x_d.mean()), mean_daily_net=float(x_n.mean()),
        p_d=p_d, p_d_blocks=p_d_blocks, p_net=p_net, p_net_blocks=p_net_blocks, t_nw_d=t_d, t_nw_net=t_n,
        sharpe_ann_net=float(x_n.mean() / x_n.std(ddof=1) * np.sqrt(252)),
        daily_sharpe_net=float(x_n.mean() / x_n.std(ddof=1)),
        mc_rank_p=mc_p, c1_null_mean=float(null_means.mean()), c1_null_sd=float(null_means.std(ddof=1)),
        gross_over_cost_2018=g_over_c,
        drift_per_trade=drift_pt, hour_drift_per_trade=hd_pt, random_side_C2_per_trade=c2_pt,
        robust_net_U1=rep_n, robust_d=rep_d, robust_net_U2=rep_u2, share_years_pos_u2=share_pos_u2,
        stats_net_U1=st.round(4).to_dict("records"), stats_net_U2=st_u2.round(4).to_dict("records"),
        stats_d=st_d.round(4).to_dict("records"),
        legs=legs, by_market=by_mkt, controls_by_window=ctrl_by_win,
        gates=gates, failed_gates=failed, kill=kill, dsr_d_neff45=dsr45,
        cost_stress_usd_per_trade=float(net_pt - np.mean([2 * H.SPEC[s]["tick"] * H.SPEC[s]["usd"]
                                                          for s in T.market])),
        win_pct=float(100 * (T.pnl_usd > 0).mean()),
        wo_top10_total=float(st.set_index("span").loc["all w/o top 10 days", "total"]),
        total=float(st.set_index("span").loc["all", "total"]),
    )
    # ---- eval (Tier A rule and MES first-class secondary): fixed 1/3/5 vs 200 C1 twins
    if do_eval and hid in ("A1", "S1.1"):
        pols = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
        ev = H.eval(T.drop(columns=["c1", "d_c1", "u2"]), pols)
        res["eval"] = ev.round(3).to_dict("records")
        tw_path = os.path.join(CACHE, f"twins_{hid}.parquet")
        if n_twins and os.path.exists(tw_path):
            tw = pd.read_parquet(tw_path)
            keys = ["policy", "consistency", "window"]
            mets = ["pass_pct", "within_10", "within_20", "bust_pct"]
            rows = []
            for r, g in tw.groupby("rep"):
                if r >= n_twins:
                    break
                e2 = H.eval(g.drop(columns=["rep"]), pols, calendar_=H.calendar((syms[0],)))
                rows.append(e2[keys + mets].assign(rep=r))
            TW = pd.concat(rows, ignore_index=True)
            TW.to_parquet(os.path.join(HERE, f"eval_twins_{hid}.parquet"))
            cmp_rows = []
            for _, a in ev.iterrows():
                g = TW[(TW.policy == a.policy) & (TW.consistency == a.consistency) & (TW.window == a.window)]
                row = {k: a[k] for k in keys}
                for mt in mets:
                    row[mt] = float(a[mt])
                    row[f"{mt}_twin_mean"] = float(g[mt].mean())
                    sgn = -1 if mt == "bust_pct" else 1
                    row[f"{mt}_rank_p"] = float((1 + (sgn * g[mt] >= sgn * a[mt]).sum()) / (1 + len(g)))
                row["luck_within_10"] = float(a.get("luck_within_10", np.nan))
                row["luck_pass_pct"] = float(a.get("luck_pass_pct", np.nan))
                cmp_rows.append(row)
            res["eval_vs_twins"] = cmp_rows
            res["n_twins"] = int(TW.rep.nunique())
        top = st.set_index("span")
        res["evalmath_targets"] = dict(
            daily_sharpe=res["daily_sharpe_net"], target_daily_sharpe=0.15,
            share_sessions_with_trade=res["share_sessions_traded"], target_share=0.80,
            win_rate=res["win_pct"], target_win_rate=45.0, usd_per_trade=net_pt,
            target_usd_per_trade=10.0 if syms == ["NQ"] else 6.0,
            share_of_profit_left_wo_10_best=float(top.loc["all w/o top 10 days", "total"] / top.loc["all", "total"]))
    res["runtime_s"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, "results", f"{hid}.json"), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    base_c1 = float(T.c1.mean())
    H.log(hid, "+".join(res["markets"]), LABELS[hid], trades=T, baseline=base_c1, params=PARAMS[hid],
          note=(f"prereg sha256 {G.PREREG_SHA[:16]}; {KIND[hid]}; p_d={p_d:.4f} p_net={p_net:.4f} "
                f"t_d={t_d:.2f} t_net={t_n:.2f} mc_p={mc_p:.3f} failed={failed} kill={kill}"),
          runtime_s=res["runtime_s"])
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cols = args or ["A1", "S1.1", "S1.2", "S1.3", "S1.4", "S1.5", "S1.6", "N1.lb10", "N1.lb20", "N1.hour",
                    "N1.cost"]
    nt = 0 if "--no-twins" in sys.argv else 200
    for hid in cols:
        r = analyse(hid, n_twins=nt)
        print(f"{hid:8s} n={r['n_trades']:5d} $/tr={r['usd_per_trade']:7.2f} d/tr={r['d_per_trade']:6.2f} "
              f"p_d={r['p_d']:.4f} p_net={r['p_net']:.4f} t_d={r['t_nw_d']:.2f} t_net={r['t_nw_net']:.2f} "
              f"mc_p={r['mc_rank_p']:.3f} kill={r['kill']} failed={r['failed_gates']} ({r['runtime_s']}s)",
              flush=True)
