"""
v3/exp_g5_reversal/g5.py - group G5 (family F1): A5 daily index reversal (Tier A) + S5.1-S5.6 + A5 neighbours
+ the long 18:00->09:30 benchmark, exactly as pre-registered in v3/PREREG.md (sha256 c9aef662...).

Light (v3/data only, through the harness). Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 OMP_NUM_THREADS=3 nice -n 5 \
      python3 v3/exp_g5_reversal/g5.py A5|SEC|EVAL|FAMILY

Interpretation choices (made before seeing any result, written here so they are visible):
- r_k = ret_cc of the k-th previous ROW of the market's sessions table (= prev_ret_cc for k=1; verified identical).
- S5.2 "sd of the 20 previous ret_cc" = sd of r1..r20 (the 20 sessions before the decision), >= 15 non-missing.
- S5.3/S5.4 index: chained from within-contract 16:00-close returns close_1600/prev_close_1600-1, falling back
  to ret_cc, then ret_oc, then 0 (the A2 chaining rule) when the 16:00 pair is missing (roll sessions).
  RSI(2) = Wilder RSI with period 2 (smoothing alpha 1/2). State machine: enter when the condition holds at the
  prior close, stay in (one 18:00->16:45 trade per session) until the exit condition holds at a prior close.
- Neighbours keep the A5 side; "day part only" enters at 09:30 and exits 16:00 with the side decided at 18:00.
- C1 seeds: A5 = 1000*5 + chunk (all three markets, prereg 0.3); secondaries/neighbours = 5000 + 100*ci + chunk.
- MYM columns: 0 before 2018 on the common calendar; gates needing 2010-17 are judged N/A (2018+ only) for MYM-only
  columns, year shares are computed over years with trades.
"""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

import harness as H
import stats_protocol as sp

warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
OUT = os.path.join(V3, "out")
EXPG5 = os.path.join(V3, "exp_G5")
for d in (os.path.join(OUT, "daily"), os.path.join(OUT, "trades"), os.path.join(OUT, "results"), EXPG5,
          os.path.join(HERE, "work")):
    os.makedirs(d, exist_ok=True)
SHA = "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
SEED = 20261109
CAL = H.calendar(("NQ", "ES"))
CAL = CAL[CAL <= pd.Timestamp("2025-06-27")]
T = len(CAL)
PREF = {"NQ": 20789.6, "ES": 5843.2, "YM": 42516.3}
MK_ORDER = ("ES", "NQ", "YM")
MICRO = {"ES": "MES", "NQ": "MNQ", "YM": "MYM"}
R_C1 = 999
WIN = {"all": ("2010-01-01", "2025-06-30"), "2010-17": ("2010-01-01", "2017-12-31"),
       "2018-25H1": ("2018-01-01", "2025-06-30"), "2018+": ("2018-01-01", "2025-06-30"),
       "2022+": ("2022-01-01", "2025-06-30")}


# ============================================================================================ signals fn(S, B)
def _r(S):
    return S["ret_cc"].astype(float)


def sig_weighted(S, B, w=(4, 3, 2, 1), entry=0, exit_=91):
    r = _r(S)
    s = sum(wk * r.shift(k + 1).fillna(0.0) for k, wk in enumerate(w))
    s = s[s != 0]
    return pd.DataFrame({"session": s.index, "entry": entry, "exit": exit_, "d": (-np.sign(s)).astype(int).to_numpy()})


def sig_A5(S, B):
    return sig_weighted(S, B, (4, 3, 2, 1))


def sig_N_5lags(S, B):
    return sig_weighted(S, B, (5, 4, 3, 2, 1))


def sig_N_equal(S, B):
    return sig_weighted(S, B, (1, 1, 1, 1))


def sig_N_overnight(S, B):
    return sig_weighted(S, B, (4, 3, 2, 1), entry=0, exit_=62)


def sig_N_day(S, B):
    return sig_weighted(S, B, (4, 3, 2, 1), entry=62, exit_=88)


def sig_S51(S, B):
    r1 = _r(S).shift(1).fillna(0.0)
    r1 = r1[r1 != 0]
    return pd.DataFrame({"session": r1.index, "entry": 0, "exit": 91, "d": (-np.sign(r1)).astype(int).to_numpy()})


def sig_S52(S, B):
    rs = _r(S).shift(1)
    sd = rs.rolling(20, min_periods=15).std()
    r1 = rs.fillna(0.0)
    m = (r1.abs() > sd) & sd.notna() & (r1 != 0)
    r1 = r1[m]
    return pd.DataFrame({"session": r1.index, "entry": 0, "exit": 91, "d": (-np.sign(r1)).astype(int).to_numpy()})


def chained_index_1600(S):
    a = S["close_1600"].astype(float) / S["prev_close_1600"].astype(float) - 1.0
    r = a.where(np.isfinite(a), S["ret_cc"].astype(float))
    r = r.where(np.isfinite(r), S["ret_oc"].astype(float)).fillna(0.0)
    return (1.0 + r).cumprod()


def rsi2(I):
    ch = I.diff()
    g = ch.clip(lower=0).fillna(0.0)
    l_ = (-ch).clip(lower=0).fillna(0.0)
    ag = g.ewm(alpha=0.5, adjust=False).mean()
    al = l_.ewm(alpha=0.5, adjust=False).mean()
    rs = ag / al.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.where(al > 0, 100.0)


def _rsi_state(S, side):
    I = chained_index_1600(S)
    R = rsi2(I).shift(1)                      # value at the PRIOR close (known at 18:00)
    sma = I.rolling(200, min_periods=200).mean().shift(1)
    Ip = I.shift(1)
    Rv, Sv, Iv = R.to_numpy(), sma.to_numpy(), Ip.to_numpy()
    pos = False
    keep = np.zeros(len(S), bool)
    for i in range(len(S)):
        if not np.isfinite(Rv[i]):
            continue
        if side > 0:
            if not pos and np.isfinite(Sv[i]) and Rv[i] < 10 and Iv[i] > Sv[i]:
                pos = True
            elif pos and Rv[i] > 70:
                pos = False
        else:
            if not pos and np.isfinite(Sv[i]) and Rv[i] > 90 and Iv[i] < Sv[i]:
                pos = True
            elif pos and Rv[i] < 30:
                pos = False
        keep[i] = pos
    idx = S.index[keep]
    return pd.DataFrame({"session": idx, "entry": 0, "exit": 91, "d": side})


def sig_S53(S, B):
    return _rsi_state(S, +1)


def sig_S54(S, B):
    return _rsi_state(S, -1)


def _late_drop(S):
    return (S["px_1600"].astype(float) / S["px_1515"].astype(float) - 1.0).shift(1)


def sig_S55(S, B):
    q = _late_drop(S)
    idx = q.index[(q < 0).to_numpy()]
    return pd.DataFrame({"session": idx, "entry": 32, "exit": 36, "d": 1})


def sig_S56(S, B):
    q = _late_drop(S)
    idx = q.index[(q < 0).to_numpy()]
    return pd.DataFrame({"session": idx, "entry": 32, "exit": 62, "d": 1})


def sig_BENCH(S, B):
    return pd.DataFrame({"session": S.index, "entry": 0, "exit": 62, "d": 1})


# column id -> (signal fn, markets, kind)
COLS = {
    "A5": (sig_A5, MK_ORDER, "A"),
    "A5_N1_5lags": (sig_N_5lags, MK_ORDER, "N"),
    "A5_N2_equal": (sig_N_equal, MK_ORDER, "N"),
    "A5_N3_overnight": (sig_N_overnight, MK_ORDER, "N"),
    "A5_N4_daypart": (sig_N_day, MK_ORDER, "N"),
}
for sid, fn in (("S5.1", sig_S51), ("S5.2", sig_S52), ("S5.3", sig_S53), ("S5.4", sig_S54), ("S5.5", sig_S55),
                ("S5.6", sig_S56)):
    for m in MK_ORDER:
        COLS[f"{sid}_{MICRO[m]}"] = (fn, (m,), "S")
for m in MK_ORDER:
    COLS[f"G5_BENCH_long1800_0930_{MICRO[m]}"] = (sig_BENCH, (m,), "BENCH")
COL_LIST = list(COLS)


# ============================================================================================ helpers
def entries_for(fn, sym):
    S = H.sessions(sym)
    B = {}
    e = fn(S, B)
    e = e[pd.DatetimeIndex(e["session"]) <= CAL[-1]].reset_index(drop=True)
    e["entry"] = e["entry"].astype(int)
    e["exit"] = e["exit"].astype(int)
    e["d"] = e["d"].astype(int)
    e["tid"] = np.arange(len(e))
    return e


def c1_control(sym, ent, R, seed_base, keep_twins=0):
    """C1: same marks, side, stop; random session of the same year. Returns (c_i per tid, n draws per tid,
    per-rep total net (R,), twin trade frames (first keep_twins reps) or None)."""
    n = int(ent["tid"].max()) + 1 if len(ent) else 0
    sums = np.zeros(n); cnts = np.zeros(n); rep_tot = np.zeros(R); rep_n = np.zeros(R)
    twins = []
    for ch in range((R + 99) // 100):
        nr = min(100, R - 100 * ch)
        r = H.random_time_trades(sym, ent, n_rep=nr, seed=seed_base + ch, keep_session=False, keep_marks=True,
                                 keep_side=True)
        tid = r["tid"].to_numpy(np.int64)
        v = r["pnl_usd"].to_numpy(np.float64)
        sums += np.bincount(tid, weights=v, minlength=n)
        cnts += np.bincount(tid, minlength=n)
        gr = r["rep"].to_numpy(np.int64) + 100 * ch
        rep_tot += np.bincount(gr, weights=v, minlength=R)
        rep_n += np.bincount(gr, minlength=R)
        if keep_twins and 100 * ch < keep_twins:
            k = r[gr < keep_twins][["market", "session", "t_entry", "t_exit", "risk_usd", "pnl_usd"]].copy()
            k["rep"] = gr[gr < keep_twins]
            twins.append(k)
        del r
    c = np.where(cnts > 0, sums / np.maximum(cnts, 1), np.nan)
    return c, cnts, rep_tot, rep_n, (pd.concat(twins, ignore_index=True) if twins else None)


def u2(tr):
    pref = tr["market"].map(PREF).to_numpy(np.float64)
    usd = tr["market"].map({k: v["usd"] for k, v in H.SPEC.items()}).to_numpy(np.float64)
    gr = tr["d"].to_numpy(np.float64) * (tr["exit_px"] - tr["entry_px"]).to_numpy() / tr["entry_px"].to_numpy()
    return gr * pref * usd - tr["cost_usd"].to_numpy(np.float64)


def dsum(tr, col):
    if not len(tr):
        return pd.Series(0.0, index=CAL)
    return tr.groupby(pd.DatetimeIndex(tr["session"]))[col].sum().reindex(CAL, fill_value=0.0).astype(float)


def win_mean(x, w):
    a, b = WIN[w]
    m = (x.index >= a) & (x.index <= b)
    return float(x[m].mean())


def by_year(x):
    return {str(y) if y < 2025 else "2025H1": float(v) for y, v in x.groupby(x.index.year).sum().items()}


def cons_p(x):
    p, ps = sp.conservative_p(sp.boot_pvalue_mean, np.asarray(x, float), B=5000, seed=SEED)
    return float(p), {int(k): float(v) for k, v in ps.items()}


def trade_table_stats(tr, col="pnl_usd"):
    st = H.stats(tr, calendar_=CAL, col=col, n_boot=2000)
    return st


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
    if isinstance(o, pd.DataFrame):
        return jsonable(o.to_dict(orient="records"))
    if isinstance(o, pd.Timestamp):
        return str(o.date())
    return o


# ============================================================================================ one column
def run_column(cid, R=R_C1, keep_twins=0, ci=0):
    fn, mkts, kind = COLS[cid]
    t0 = time.time()
    trs, ctrl_tid = [], []
    rep_tot = np.zeros(R)
    info = {}
    twins = []
    drift_tr, hd_tr, c2_tr, rnd_tr = [], [], [], []
    for m in mkts:
        ent = entries_for(fn, m)
        tr = H.time_trades(m, ent)
        info[m] = dict(n_entries=len(ent), dropped=tr.attrs["dropped"])
        seed_base = 1000 * 5 if cid == "A5" else 5000 + 100 * ci
        c, cnt, rt, rn, tw = c1_control(m, ent, R, seed_base, keep_twins=keep_twins)
        tr["c_i"] = c[tr["tid"].to_numpy(np.int64)]
        tr["c_draws"] = cnt[tr["tid"].to_numpy(np.int64)]
        tr["u2"] = u2(tr)
        trs.append(tr)
        rep_tot += rt
        if tw is not None:
            twins.append(tw)
        # reported controls (n_rep = 100)
        dr = H.drift_trades(m, ent); drift_tr.append(dr)
        hd = H.hour_drift_trades(m, ent, n_rep=100, seed=SEED + 1); hd_tr.append(hd)
        c2 = H.random_time_trades(m, ent, n_rep=100, seed=SEED + 2, keep_session=True, keep_marks=True,
                                  keep_side=False); c2_tr.append(c2)
        rd = H.random_time_trades(m, ent, n_rep=100, seed=SEED + 3); rnd_tr.append(rd)
    tr = pd.concat(trs, ignore_index=True)
    tr = tr[pd.DatetimeIndex(tr["session"]) <= CAL[-1]].reset_index(drop=True)
    tr["dc"] = tr["pnl_usd"] - tr["c_i"]
    dr = pd.concat(drift_tr, ignore_index=True); hd = pd.concat(hd_tr, ignore_index=True)
    c2 = pd.concat(c2_tr, ignore_index=True); rd = pd.concat(rnd_tr, ignore_index=True)
    dr = dr[pd.DatetimeIndex(dr["session"]) <= CAL[-1]]

    D = pd.DataFrame(index=CAL)
    D.index.name = "session"
    D["net_U1"] = dsum(tr, "pnl_usd")
    D["net_U2"] = dsum(tr, "u2")
    D["gross_U1"] = dsum(tr, "gross_usd")
    D["ctrl_C1"] = dsum(tr, "c_i")
    D["d"] = dsum(tr, "dc")
    D["n_trades"] = tr.groupby(pd.DatetimeIndex(tr["session"])).size().reindex(CAL, fill_value=0) if len(tr) else 0
    for m in MK_ORDER:
        D[f"net_{m}"] = dsum(tr[tr.market == m], "pnl_usd")
    D.reset_index().to_csv(os.path.join(OUT, "daily", f"{cid}.csv"), index=False)
    pd.DataFrame({"session": CAL.strftime("%Y-%m-%d"), "pnl_usd": D["net_U1"].to_numpy()}).to_csv(
        os.path.join(EXPG5, f"daily_{cid}.csv"), index=False)
    tr.to_parquet(os.path.join(OUT, "trades", f"{cid}.parquet"))

    ym_only = tuple(mkts) == ("YM",)
    res = dict(id=cid, kind=kind, markets=[MICRO[m] for m in mkts], prereg_sha256=SHA, info=info,
               n_trades=int(len(tr)), trades_per_year=float(len(tr) / ((CAL[-1] - (pd.Timestamp("2018-01-02") if ym_only else CAL[0])).days / 365.25)))
    d = D["d"]; net = D["net_U1"]
    res["p_d"], res["p_d_by_block"] = cons_p(d)
    res["p_net"], res["p_net_by_block"] = cons_p(net)
    res["t_nw_d"] = float(sp.hac_t(d.to_numpy())[0])
    res["t_nw_net"] = float(sp.hac_t(net.to_numpy())[0])
    res["mean_d_day"] = float(d.mean()); res["mean_net_day"] = float(net.mean())
    res["usd_per_trade"] = float(tr["pnl_usd"].mean()); res["d_per_trade"] = float(tr["dc"].mean())
    res["gross_per_trade"] = float(tr["gross_usd"].mean()); res["cost_per_trade"] = float(tr["cost_usd"].mean())
    res["ctrl_C1_per_trade"] = float(tr["c_i"].mean())
    res["windows_net_day"] = {w: win_mean(net, w) for w in WIN}
    res["windows_d_day"] = {w: win_mean(d, w) for w in WIN}
    res["windows_u2_day"] = {w: win_mean(D["net_U2"], w) for w in WIN}
    sess_tr = pd.DatetimeIndex(tr["session"])
    res["windows_net_trade"] = {w: float(tr.loc[(sess_tr >= WIN[w][0]) & (sess_tr <= WIN[w][1]), "pnl_usd"].mean())
                                for w in WIN}
    res["by_year_net"] = by_year(net); res["by_year_d"] = by_year(d); res["by_year_u2"] = by_year(D["net_U2"])
    res["per_market"] = {}
    for m in mkts:
        tm = tr[tr.market == m]
        st = trade_table_stats(tm)
        res["per_market"][MICRO[m]] = dict(
            usd_per_trade=float(tm.pnl_usd.mean()), d_per_trade=float(tm.dc.mean()), n=int(len(tm)),
            stats=st[["span", "n_trades", "mean", "total", "t", "sharpe_ann", "usd_year", "win_pct", "p_boot"]])
    st_all = trade_table_stats(tr)
    res["stats_trades"] = st_all[["span", "n_trades", "mean", "total", "t", "sharpe_ann", "usd_year", "win_pct",
                                  "p_boot"]]
    # legs
    res["legs"] = {}
    for lg, sgn in (("long", 1), ("short", -1)):
        tl = tr[tr.d == sgn]
        if len(tl):
            res["legs"][lg] = dict(n=int(len(tl)), usd_per_trade=float(tl.pnl_usd.mean()),
                                   d_per_trade=float(tl.dc.mean()),
                                   t_nw_d=float(sp.hac_t(dsum(tl, "dc").to_numpy())[0]),
                                   t_nw_net=float(sp.hac_t(dsum(tl, "pnl_usd").to_numpy())[0]),
                                   net_2010_17=win_mean(dsum(tl, "pnl_usd"), "2010-17"),
                                   net_2018_25H1=win_mean(dsum(tl, "pnl_usd"), "2018-25H1"))
    # robust report
    rep_n = sp.robust_report(net.to_numpy(), CAL.values)
    rep_d = sp.robust_report(d.to_numpy(), CAL.values)
    rep_u2 = sp.robust_report(D["net_U2"].to_numpy(), CAL.values)
    res["robust_net"] = rep_n; res["robust_d"] = rep_d; res["robust_u2"] = rep_u2
    # without the 10 best days
    keep = np.ones(T, bool); keep[np.argsort(-net.to_numpy())[:10]] = False
    res["net_wo_top10_total"] = float(net.to_numpy()[keep].sum())
    res["net_total"] = float(net.sum())
    res["net_wo_top10_per_trade"] = float(net.to_numpy()[keep].sum() / max(len(tr), 1))
    # controls
    res["c1_rep_means_day"] = (rep_tot / T)
    res["mc_rank_p"] = sp.mc_rank_p(net.mean(), rep_tot / T)
    drift_day = dsum(dr, "pnl_usd")
    hd_mean_day = float(hd["pnl_usd"].sum() / 100 / T)
    res["drift_mean_day"] = float(drift_day.mean()); res["hour_drift_mean_day"] = hd_mean_day
    res["drift_per_trade"] = float(dr.pnl_usd.mean()); res["hour_drift_per_trade"] = float(hd.pnl_usd.mean())
    res["vs_drift"] = H.control_report(tr, dr); res["vs_hour_drift"] = H.control_report(tr, hd)
    res["vs_C2_random_side"] = H.control_report(tr, c2)
    res["vs_random_time"] = H.control_report(tr, rd)
    # cost stress (+1 tick each way)
    extra = tr["market"].map({k: 2 * v["tick"] * v["usd"] for k, v in H.SPEC.items()}).to_numpy()
    tr_s = tr.assign(pnl_stress=tr["pnl_usd"] - extra)
    ns = dsum(tr_s, "pnl_stress")
    res["stress"] = dict(usd_per_trade=float(tr_s.pnl_stress.mean()), t_nw=float(sp.hac_t(ns.to_numpy())[0]),
                         p=cons_p(ns)[0], net_2018_25H1_day=win_mean(ns, "2018-25H1"), net_2022_day=win_mean(ns, "2022+"))
    # gates
    G = {}
    if ym_only:
        G["1_d_halves"] = dict(ok=bool(rep_d["2018_25H1"][0] > 0), note="MYM: 2010-17 N/A, judged on 2018-25H1")
        G["2_net_halves"] = dict(ok=bool(rep_u2["2018_25H1"][0] > 0 and rep_n["2018_25H1"][0] > 0
                                         and rep_n["2022+"][0] > 0), note="MYM: 2010-17 N/A")
        yrs = {k: v for k, v in res["by_year_u2"].items() if (k[:4] >= "2018")}
    else:
        G["1_d_halves"] = dict(ok=bool(rep_d["2010_17"][0] > 0 and rep_d["2018_25H1"][0] > 0))
        G["2_net_halves"] = dict(ok=bool(rep_u2["2010_17"][0] > 0 and rep_u2["2018_25H1"][0] > 0
                                         and rep_n["2018_25H1"][0] > 0 and rep_n["2022+"][0] > 0))
        yrs = res["by_year_u2"]
    share = float(np.mean([v > 0 for v in yrs.values()]))
    G["3_years_pos_U2"] = dict(ok=share >= 0.6, share=share)
    G["4_wo_top10"] = dict(ok=bool(rep_n["drop_best"][0] > 0), mean=rep_n["drop_best"][0])
    G["5_winsor"] = dict(ok=bool(rep_n["winsor"][0] > 0), mean=rep_n["winsor"][0])
    G["6_mc_rank"] = dict(ok=res["mc_rank_p"] <= 0.05, p=res["mc_rank_p"])
    m18 = (sess_tr >= "2018-01-01")
    g18 = float(tr.loc[m18, "gross_usd"].mean()); c18 = float(tr.loc[m18, "cost_usd"].mean())
    G["7_gross_vs_cost"] = dict(ok=bool(g18 >= 1.5 * c18), gross_2018=g18, cost=c18, ratio=g18 / c18)
    G["8_beats_drift"] = dict(ok=bool(net.mean() > res["drift_mean_day"] and net.mean() > hd_mean_day),
                              net=float(net.mean()), drift=res["drift_mean_day"], hour_drift=hd_mean_day)
    if len(mkts) > 1:
        pos = {}
        for m in mkts:
            x = D[f"net_{m}"]
            pos[MICRO[m]] = float(x[x.index >= "2018-01-01"].sum() if m == "YM" else x.sum())
        G["9_markets"] = dict(ok=sum(v > 0 for v in pos.values()) >= 2, totals=pos)
    res["gates"] = G
    res["failed_gates"] = [k for k, v in G.items() if not v["ok"]]
    res["kill"] = bool(d.mean() <= 0 or rep_n["2018_25H1"][0] <= 0)
    # eval (fixed 1/3/5, descriptive)
    try:
        ev = H.eval(tr, [("fixed", 1), ("fixed", 3), ("fixed", 5)], calendar_=CAL)
        res["eval"] = ev
    except Exception as ex:  # noqa: BLE001
        res["eval"] = f"error {ex!r}"
    # eval-math targets
    sd_day = float(net.std(ddof=1))
    res["evalmath"] = dict(daily_sharpe=float(net.mean() / sd_day) if sd_day > 0 else None,
                           share_sessions_traded=float((D["n_trades"] > 0).mean()),
                           win_rate=float((tr.pnl_usd > 0).mean()),
                           usd_per_trade_by_market={MICRO[m]: float(tr[tr.market == m].pnl_usd.mean()) for m in mkts},
                           share_profit_wo_top10=float(res["net_wo_top10_total"] / res["net_total"])
                           if res["net_total"] != 0 else None)
    res["seconds"] = time.time() - t0
    # log the column
    base = tr.assign(pnl_usd=tr["c_i"])
    H.log(cid, "+".join(MICRO[m] for m in mkts), f"G5 {kind} {cid}", trades=tr, baseline=base,
          params=dict(col=cid, kind=kind, R_C1=R, p_d=res["p_d"], p_net=res["p_net"], t_nw_d=res["t_nw_d"]),
          note=f"prereg sha256 {SHA}")
    tw = pd.concat(twins, ignore_index=True) if twins else None
    return res, tr, D, tw


def save_result(cid, res):
    r = {k: v for k, v in res.items() if k != "c1_rep_means_day"}
    r["c1_rep_means_day_summary"] = dict(mean=float(np.mean(res["c1_rep_means_day"])),
                                         sd=float(np.std(res["c1_rep_means_day"], ddof=1)),
                                         q95=float(np.quantile(res["c1_rep_means_day"], 0.95)))
    with open(os.path.join(OUT, "results", f"{cid}.json"), "w") as f:
        json.dump(jsonable(r), f, indent=1)
    np.save(os.path.join(HERE, "work", f"c1rep_{cid}.npy"), res["c1_rep_means_day"])


# ============================================================================================ look-ahead
def lookahead_all():
    rows = []
    fns = {"A5": sig_A5, "N1": sig_N_5lags, "N2": sig_N_equal, "N3": sig_N_overnight, "N4": sig_N_day,
           "S5.1": sig_S51, "S5.2": sig_S52, "S5.3": sig_S53, "S5.4": sig_S54, "S5.5": sig_S55, "S5.6": sig_S56}
    for name, fn in fns.items():
        for m in MK_ORDER:
            r = H.lookahead_check(fn, m, n_cuts=20, seed=0, tfs=())
            rows.append(dict(signal=name, market=MICRO[m], cuts=len(r), all_same=bool(r.same.all()),
                             entries_compared=int(r.n_full.sum())))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "lookahead.csv"), index=False)
    return out


def main(what):
    if what == "LOOK":
        print(lookahead_all().to_string())
        return
    if what == "A5":
        res, tr, D, tw = run_column("A5", keep_twins=200)
        save_result("A5", res)
        tw = tw[pd.DatetimeIndex(tw["session"]) <= CAL[-1]]
        tw.to_parquet(os.path.join(HERE, "work", "A5_twins200.parquet"))
        print(json.dumps(jsonable({k: res[k] for k in ("p_d", "p_net", "t_nw_d", "t_nw_net", "usd_per_trade",
                                                         "d_per_trade", "failed_gates", "kill", "seconds")}), indent=1))
        return
    if what.startswith("SEC"):
        todo = [c for c in COL_LIST if COLS[c][2] in ("N", "S", "BENCH")]
        part = what[3:]
        if part:
            todo = [c for c in todo if c.startswith(part)]
        for c in todo:
            ci = COL_LIST.index(c)
            R = 200 if COLS[c][2] == "BENCH" else R_C1
            res, tr, D, _ = run_column(c, R=R, ci=ci)
            save_result(c, res)
            print(c, f"n={res['n_trades']} $/tr={res['usd_per_trade']:.2f} d/tr={res['d_per_trade']:.2f} "
                     f"t_d={res['t_nw_d']:.2f} p_d={res['p_d']:.4f} p_net={res['p_net']:.4f} "
                     f"fails={res['failed_gates']} kill={res['kill']} {res['seconds']:.0f}s", flush=True)
        return


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "A5")
