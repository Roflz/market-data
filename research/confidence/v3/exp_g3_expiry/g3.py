"""
v3/exp_g3_expiry/g3.py - experiment group G3 (family F2): expiry-day option-hedging flows.

Implements EXACTLY the pre-registered tests of PREREG.md (sha256 c9aef662...) section 1 A3 and section 2 G3:
  A3      short 1 MES + 1 MNQ + 1 MYM (MYM 2018+) at the 09:30 mark, cover at the 16:00 mark, on opex sessions
          (third Friday, or the prior trading day if that Friday is a holiday). No stop. Tier A (confirmatory).
  S3.1    A3 with the cover at 12:00.
  S3.2    long 18:00 -> 09:30 on the expiry session (basket).
  S3.3    S3.2 + A3 (the paper's round trip; two trades per market per event).
  S3.4    A3 on monthly non-quarterly expiries only.     S3.5  A3 on quarterly expiries only.
  S3.6    quarterly-expiry last-hour short 15:00 -> 16:00: MES first (S3.6-ES), then MNQ (S3.6-NQ), MYM (S3.6-YM).
  S3.7    long 18:00 -> 09:30 on the session that closes on the first trading day of each month (basket).
  Neighbours of A3 (stability, reported as same sign yes/no, logged): entry 09:45 (A3-N0945); cover 15:00
          (A3-N1500); MES alone (A3-ES), MNQ alone (A3-NQ), MYM alone (A3-YM).
  C3 (reported for A3): the same short on all non-expiry Fridays (A3-C3).

Light: reads only v3/data through the harness (no flock). Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 OMP_NUM_THREADS=3 python3 v3/exp_g3_expiry/g3.py
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

warnings.filterwarnings("ignore", message="time_trades")
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
OUT = os.path.join(V3, "out")
G3DIR = os.path.join(V3, "exp_G3")
for d_ in ("daily", "trades", "results"):
    os.makedirs(os.path.join(OUT, d_), exist_ok=True)
os.makedirs(G3DIR, exist_ok=True)
CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)

PREREG_SHA = open(os.path.join(OUT, "prereg", "PREREG.md.sha256")).read().split()[0]
assert PREREG_SHA == "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
NOTE = f"prereg sha256 {PREREG_SHA}"
SEED = 20261109
K_HYP = 3                                                     # A3 -> k = 3 (C1 seeds 1000*k + chunk)
R_C1 = 999
LAST = pd.Timestamp("2025-06-27")
CAL = H.calendar(("NQ", "ES"))
CAL = CAL[CAL <= LAST]
assert len(CAL) == 3876, len(CAL)
T = len(CAL)
PREF = {"NQ": 20789.6, "ES": 5843.2, "YM": 42516.3}
MKTS = ("ES", "NQ", "YM")                                     # MES first
MICRO = {"ES": "MES", "NQ": "MNQ", "YM": "MYM"}
# first trading day of each month = a fixed exchange schedule (known in advance), from the NQ/ES calendar.
# FIX (skeptic, 2026-11-09): a 'trading day' is an NYSE trading day. CME Globex trades a short session on most NYSE
# holidays (e.g. Labor Day, halt 13:00 ET) but books that activity to the NEXT trade date, so a holiday Globex session
# is not a trading day. v1 (TOM_DAYS_V1) took the first Globex session of the month and so used 5 Labor Day holiday
# sessions (2012-09-03, 2014-09-01, 2018-09-03, 2019-09-02, 2024-09-02); v2 uses the next session (the Tuesday).
sys.path.insert(0, HERE)
from nyse_holidays import HOLIDAYS as NYSE_HOLIDAYS          # noqa: E402  (published rule-based schedule)
_c = H.calendar(("NQ", "ES"))
TOM_DAYS_V1 = pd.DatetimeIndex(_c[1:][_c.month[1:] != _c.month[:-1]])


def first_trading_days(cal):
    """first NYSE trading day (not an NYSE holiday) of each month in `cal`; the calendar's first month is skipped
    when it starts mid-month (as in v1)."""
    c = pd.DatetimeIndex(cal)
    c = c[~c.isin(NYSE_HOLIDAYS)]
    return pd.DatetimeIndex(c[1:][c.month[1:] != c.month[:-1]])


TOM_DAYS = first_trading_days(_c)


# ============================================================================================ signals fn(S, B)
def sig_event(legs, which="opex"):
    """legs: list of (entry, exit, d). which: opex | monthly (opex, not quarterly) | quad | tom | fri_nonopex."""
    def fn(S, B):
        if which == "opex":
            m = S["opex"].astype(bool).to_numpy()
        elif which == "monthly":
            m = (S["opex"].astype(bool) & ~S["quad"].astype(bool)).to_numpy()
        elif which == "quad":
            m = S["quad"].astype(bool).to_numpy()
        elif which == "tom":
            m = S.index.isin(TOM_DAYS)
        elif which == "fri_nonopex":
            m = ((S["dow"] == 4) & ~S["opex"].astype(bool)).to_numpy()
        else:
            raise ValueError(which)
        idx = S.index[m]
        rows = [pd.DataFrame({"session": idx, "entry": e, "exit": x, "d": d, "leg": j})
                for j, (e, x, d) in enumerate(legs)]
        out = pd.concat(rows, ignore_index=True)
        out["_k"] = [H.mark_index(v) for v in out["entry"]]
        return out.sort_values(["session", "_k"]).drop(columns="_k").reset_index(drop=True)
    return fn


A3_LEG = [("0930", "1600", -1)]
COLS = {  # hid: (description, legs, which, markets, tier)
    "A3": ("opex-Friday short 09:30-16:00, basket", A3_LEG, "opex", MKTS, "A"),
    "S3.1": ("A3 cover 12:00, basket", [("0930", "1200", -1)], "opex", MKTS, "B"),
    "S3.2": ("long 18:00-09:30 on the expiry session, basket", [("1800", "0930", 1)], "opex", MKTS, "B"),
    "S3.3": ("round trip: long 18:00-09:30 + short 09:30-16:00 on expiry, basket",
             [("1800", "0930", 1), ("0930", "1600", -1)], "opex", MKTS, "B"),
    "S3.4": ("A3 monthly non-quarterly expiries only, basket", A3_LEG, "monthly", MKTS, "B"),
    "S3.5": ("A3 quarterly expiries only, basket", A3_LEG, "quad", MKTS, "B"),
    "S3.6-ES": ("quarterly-expiry last-hour short 15:00-16:00, MES", [("1500", "1600", -1)], "quad", ("ES",), "B"),
    "S3.6-NQ": ("quarterly-expiry last-hour short 15:00-16:00, MNQ", [("1500", "1600", -1)], "quad", ("NQ",), "B"),
    "S3.6-YM": ("quarterly-expiry last-hour short 15:00-16:00, MYM", [("1500", "1600", -1)], "quad", ("YM",), "B"),
    "S3.7": ("turn-of-month long 18:00-09:30 into the first trading day, basket", [("1800", "0930", 1)], "tom",
             MKTS, "B"),
    "A3-N0945": ("NEIGHBOUR A3 entry 09:45, basket", [("0945", "1600", -1)], "opex", MKTS, "N"),
    "A3-N1500": ("NEIGHBOUR A3 cover 15:00, basket", [("0930", "1500", -1)], "opex", MKTS, "N"),
    "A3-ES": ("NEIGHBOUR A3 MES alone", A3_LEG, "opex", ("ES",), "N"),
    "A3-NQ": ("NEIGHBOUR A3 MNQ alone", A3_LEG, "opex", ("NQ",), "N"),
    "A3-YM": ("NEIGHBOUR A3 MYM alone", A3_LEG, "opex", ("YM",), "N"),
    "A3-C3": ("C3 control: A3 short on all non-expiry Fridays, basket", A3_LEG, "fri_nonopex", MKTS, "C"),
}
SEED_OFF = {h: j for j, h in enumerate(COLS)}                 # A3 -> 0: seeds 3000 + chunk exactly as pre-registered


def entries(hid, sym):
    _, legs, which, _, _ = COLS[hid]
    e = sig_event(legs, which)(H.sessions(sym), {})
    e = e[pd.DatetimeIndex(e.session) <= LAST].reset_index(drop=True)
    e["tid"] = np.arange(len(e))
    return e


# ============================================================================================ trades + C1
def trades_c1(hid, sym, R=R_C1, keep_reps=False):
    e = entries(hid, sym)
    tr = H.time_trades(sym, e)
    cp = os.path.join(CACHE, f"c1_{hid}_{sym}_{R}.parquet")
    if os.path.exists(cp):
        c1 = pd.read_parquet(cp)
    else:
        parts, done, chunk = [], 0, 0
        base = 1000 * K_HYP + 100 * SEED_OFF[hid]
        while done < R:
            n = min(100, R - done)
            r = H.random_time_trades(sym, e, n_rep=n, seed=base + chunk, keep_session=False, keep_marks=True,
                                     keep_side=True)
            r["rep"] = r["rep"] + done
            parts.append(r[["market", "session", "t_entry", "t_exit", "tid", "rep", "d", "entry_px", "exit_px",
                            "risk_usd", "gross_usd", "cost_usd", "pnl_usd"]])
            done += n
            chunk += 1
        c1 = pd.concat(parts, ignore_index=True)
        c1.to_parquet(cp)
    c = c1.groupby("tid")["pnl_usd"].mean()
    tr["c1"] = tr["tid"].map(c).to_numpy()
    tr["d_c1"] = tr["pnl_usd"] - tr["c1"]
    sp_ = H.SPEC[sym]
    tr["ret"] = tr["d"] * (tr["exit_px"] - tr["entry_px"]) / tr["entry_px"]
    tr["net_U2"] = tr["ret"] * PREF[sym] * sp_["usd"] - tr["cost_usd"]
    tr["n_c1"] = tr["tid"].map(c1.groupby("tid").size()).to_numpy()
    return tr, c1


def dser(tr, col):
    if len(tr) == 0:
        return pd.Series(0.0, index=CAL)
    return H.daily_pnl(tr, calendar_=CAL, col=col)


# ============================================================================================ statistics
def cons_p(x):
    p, ps = sp.conservative_p(sp.boot_pvalue_mean, np.asarray(x, float), B=5000, seed=SEED)
    return float(p), {int(k): float(v) for k, v in ps.items()}


def year_mask(idx, a, b):
    y = idx.year
    return (y >= a) & (y <= b)


def window_means(x):
    """x: daily Series over CAL -> mean per session by window."""
    idx = x.index
    out = {"all": float(x.mean())}
    out["2010-17"] = float(x[year_mask(idx, 2010, 2017)].mean())
    out["2018-25H1"] = float(x[year_mask(idx, 2018, 2025)].mean())
    out["2022+"] = float(x[year_mask(idx, 2022, 2025)].mean())
    return out


def per_trade_windows(tr, col="pnl_usd"):
    s = pd.DatetimeIndex(tr.session)
    w = {"all": np.ones(len(tr), bool), "2010-17": s.year <= 2017, "2018-25H1": s.year >= 2018,
         "2022+": s.year >= 2022}
    return {k: (float(tr.loc[m, col].mean()) if m.any() else float("nan"), int(m.sum())) for k, m in w.items()}


def two_year_blocks(x):
    """sum of daily x in 2-year blocks 2010-11 ... 2024-25H1."""
    y = x.index.year
    return {f"{a}-{a + 1 - 2000:02d}": float(x[(y >= a) & (y <= a + 1)].sum()) for a in range(2010, 2026, 2)}


def analyse(hid, R=R_C1, do_eval=False, n_twins=200):
    desc, legs, which, mkts, tier = COLS[hid]
    t0 = time.time()
    trs, c1s = {}, {}
    for sym in mkts:
        trs[sym], c1s[sym] = trades_c1(hid, sym, R)
    tr = pd.concat([trs[s] for s in mkts], ignore_index=True)
    c1all = pd.concat([c1s[s] for s in mkts], ignore_index=True)
    # ---------------- daily series on the full calendar (YM 0 before 2018)
    D = pd.DataFrame(index=CAL)
    D["net_U1"] = dser(tr, "pnl_usd")
    D["net_U2"] = dser(tr, "net_U2")
    D["gross_U1"] = dser(tr, "gross_usd")
    D["ctrl_C1"] = dser(tr, "c1")
    D["d"] = dser(tr, "d_c1")
    D["n_trades"] = tr.groupby(pd.DatetimeIndex(tr.session)).size().reindex(CAL, fill_value=0)
    for s in MKTS:
        D[f"net_{s}"] = dser(trs[s], "pnl_usd") if s in trs else 0.0
    D.index.name = "session"
    assert np.allclose(D["d"], D["net_U1"] - D["ctrl_C1"])
    # ---------------- primary + raw net tests
    p_d, p_d_blocks = cons_p(D["d"])
    p_net, p_net_blocks = cons_p(D["net_U1"])
    t_d = float(sp.hac_t(D["d"].to_numpy())[0])
    t_net = float(sp.hac_t(D["net_U1"].to_numpy())[0])
    rep_d = sp.robust_report(D["d"].to_numpy(), CAL.to_numpy())
    rep_net = sp.robust_report(D["net_U1"].to_numpy(), CAL.to_numpy())
    rep_u2 = sp.robust_report(D["net_U2"].to_numpy(), CAL.to_numpy())
    dsr_d = sp.dsr(D["d"].to_numpy(), 45)
    dsr_net = sp.dsr(D["net_U1"].to_numpy(), 45)
    # ---------------- matched-control rank p (999 C1 strategies; basket = sum over markets of rep r)
    rep_tot = c1all.groupby("rep")["pnl_usd"].sum().reindex(range(R), fill_value=0.0)
    real_mean = float(D["net_U1"].mean())
    mc_p = sp.mc_rank_p(real_mean, rep_tot.to_numpy() / T)
    # ---------------- per-trade numbers
    st = H.stats(tr[["market", "session", "pnl_usd"]], calendar_=CAL)
    gross_1825 = float(tr.loc[pd.DatetimeIndex(tr.session).year >= 2018, "gross_usd"].mean())
    cost_1825 = float(tr.loc[pd.DatetimeIndex(tr.session).year >= 2018, "cost_usd"].mean())
    # plain drift (long at the same sessions & marks) and hour drift (long at the same marks, random same-year sessions)
    dr = pd.concat([H.drift_trades(s, entries(hid, s)) for s in mkts], ignore_index=True)
    hd = pd.concat([H.hour_drift_trades(s, entries(hid, s), n_rep=100, seed=SEED + 7) for s in mkts],
                   ignore_index=True)
    # C2 random side, same sessions and marks
    c2 = pd.concat([H.random_time_trades(s, entries(hid, s), n_rep=100, seed=SEED + 11, keep_session=True,
                                         keep_marks=True, keep_side=False) for s in mkts], ignore_index=True)
    net_pt = float(tr["pnl_usd"].mean())
    drift_pt = float(dr["pnl_usd"].mean())
    hdrift_pt = float(hd["pnl_usd"].mean())
    c1_pt = float(c1all["pnl_usd"].mean())
    c2_by_rep = c2.groupby("rep")["pnl_usd"].mean()
    c2_p = float((1 + (c2_by_rep >= net_pt).sum()) / (1 + len(c2_by_rep)))
    # ---------------- per market
    bym = {}
    for s in mkts:
        t_ = trs[s]
        ds = dser(t_, "d_c1")
        pw = per_trade_windows(t_)
        bym[s] = dict(n=len(t_), usd_per_trade=float(t_.pnl_usd.mean()), total=float(t_.pnl_usd.sum()),
                      u2_per_trade=float(t_.net_U2.mean()), d_per_trade=float(t_.d_c1.mean()),
                      c1_per_trade=float(t_.c1.mean()), t_d=float(sp.hac_t(ds.to_numpy())[0]),
                      t_net=float(sp.hac_t(dser(t_, "pnl_usd").to_numpy())[0]),
                      usd_per_trade_2010_17=pw["2010-17"][0], usd_per_trade_2018_25H1=pw["2018-25H1"][0],
                      usd_per_trade_2022p=pw["2022+"][0], net_pos=bool(t_.pnl_usd.sum() > 0))
    # ---------------- cost stress (+1 tick each way)
    extra = tr["market"].map({s: 2 * H.SPEC[s]["tick"] * H.SPEC[s]["usd"] for s in MKTS})
    trs_ = tr.assign(pnl_usd=tr["pnl_usd"] - extra)
    D_stress = dser(trs_, "pnl_usd")
    stress = dict(usd_per_trade=float(trs_.pnl_usd.mean()), t_net=float(sp.hac_t(D_stress.to_numpy())[0]),
                  p_net=cons_p(D_stress)[0], by_window_per_trade={k: v[0] for k, v in per_trade_windows(trs_).items()})
    # ---------------- gates (PREREG 0.5)
    blocks = two_year_blocks(D["net_U2"])
    share_blocks = float(np.mean([v > 0 for v in blocks.values()]))
    yrs_u2 = rep_u2["by_year"]
    share_years = float(np.mean([v > 0 for v in yrs_u2.values()]))
    event = which in ("opex", "monthly", "quad")
    n_pos_mkts = sum(bym[s]["net_pos"] for s in mkts)
    gates = {
        "1 d>0 in 2010-17 and 2018-25H1": bool(rep_d["2010_17"][0] > 0 and rep_d["2018_25H1"][0] > 0),
        "2 U2 net>0 both halves; U1 net>0 2018-25H1 and 2022+": bool(
            rep_u2["2010_17"][0] > 0 and rep_u2["2018_25H1"][0] > 0 and rep_net["2018_25H1"][0] > 0
            and rep_net["2022+"][0] > 0),
        "3 >=60% of (2-year blocks if event) U2 positive": bool((share_blocks if event else share_years) >= 0.6),
        "4 U1 net>0 w/o 10 best days": bool(rep_net["drop_best"][0] > 0),
        "5 winsorised U1 net>0": bool(rep_net["winsor"][0] > 0),
        "6 C1 rank p<=0.05": bool(mc_p <= 0.05),
        "7 gross 2018-25H1 >= 1.5x cost": bool(gross_1825 >= 1.5 * cost_1825),
        "8 net beats plain drift and hour drift": bool(net_pt > drift_pt and net_pt > hdrift_pt),
    }
    if len(mkts) == 3:
        gates["9 basket: U1 net>0 in >=2 of 3 markets"] = bool(n_pos_mkts >= 2)
    failed = [k for k, v in gates.items() if not v]
    kill = bool(D["d"].mean() <= 0 or rep_net["2018_25H1"][0] <= 0)
    res = dict(hid=hid, description=desc, tier=tier, family="F2", markets=list(mkts), legs=legs, which=which,
               prereg_sha256=PREREG_SHA, R_C1=R, c1_seed_base=1000 * K_HYP + 100 * SEED_OFF[hid],
               n_trades=len(tr), n_event_sessions=int((D.n_trades > 0).sum()),
               trades_per_year=float(len(tr) / (T / 252)),
               usd_per_trade=net_pt, usd_per_trade_U2=float(tr.net_U2.mean()), gross_per_trade=float(tr.gross_usd.mean()),
               d_per_trade=float(tr.d_c1.mean()), c1_per_trade=c1_pt, mean_d_day=float(D["d"].mean()),
               mean_net_day=real_mean,
               p_d=p_d, p_d_blocks=p_d_blocks, p_net=p_net, p_net_blocks=p_net_blocks, t_d_nw=t_d, t_net_nw=t_net,
               sharpe_ann_net=float(D.net_U1.mean() / D.net_U1.std(ddof=1) * np.sqrt(252)),
               sharpe_ann_d=float(D.d.mean() / D.d.std(ddof=1) * np.sqrt(252)),
               dsr_d_neff45=dsr_d["dsr"], dsr_net_neff45=dsr_net["dsr"],
               robust_d=rep_d, robust_net_U1=rep_net, robust_net_U2=rep_u2, u2_2yr_blocks=blocks,
               share_2yr_blocks_pos=share_blocks, share_years_pos_U2=share_years,
               mc_rank_p=mc_p, gross_2018_25H1=gross_1825, cost_2018_25H1=cost_1825,
               drift_per_trade=drift_pt, hour_drift_per_trade=hdrift_pt, c2_random_side_per_trade=float(c2_by_rep.mean()),
               c2_rank_p=c2_p, per_trade_windows=per_trade_windows(tr),
               per_trade_windows_U2=per_trade_windows(tr, "net_U2"),
               by_market=bym, cost_stress_plus1tick=stress, gates=gates, failed_gates=failed, kill=kill,
               stats_table=st.round(4).to_dict(orient="records"))
    # ---------------- outputs
    D.to_csv(os.path.join(OUT, "daily", f"{hid}.csv"))
    pd.DataFrame({"session": CAL, "pnl_usd": D["net_U1"].to_numpy()}).to_csv(
        os.path.join(G3DIR, f"daily_{hid}.csv"), index=False)
    tr.to_parquet(os.path.join(OUT, "trades", f"{hid}.parquet"))
    if do_eval:
        res["eval"] = eval_block(tr, c1all, mkts, n_twins)
    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, "results", f"{hid}.json"), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    H.log(hid, "+".join(MICRO[s] for s in mkts), desc, trades=tr, baseline=c1all,
          params=dict(legs=legs, which=which, markets=list(mkts), tier=tier, R_C1=R, prereg_id="v3round1_A3"
                      if hid == "A3" else "v3round1_G3-secondary",
                      **({"tom_rule": "v2: first NYSE trading day (Globex holiday sessions excluded; Labor Day fix)"}
                         if which == "tom" else {})),
          note=f"{NOTE}; p_d {p_d:.4f} p_net {p_net:.4f} t_d {t_d:.2f}")
    return res, D, tr, c1all


# ============================================================================================ eval
def eval_block(tr, c1all, mkts, n_twins=200):
    sizing = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
    cols = ["market", "t_entry", "t_exit", "risk_usd", "pnl_usd", "session"]
    real = H.eval(tr[cols], sizing=sizing, calendar_=CAL)
    twins = []
    for r in range(n_twins):
        tw = c1all.loc[(c1all.rep == r) & (pd.DatetimeIndex(c1all.session) <= LAST), cols]   # 2025-06-30 off-calendar
        e = H.eval(tw, sizing=sizing, calendar_=CAL)
        e["rep"] = r
        twins.append(e)
    tw = pd.concat(twins, ignore_index=True)
    keyc = ["policy", "consistency", "window"]
    agg = tw.groupby(keyc)[["pass_pct", "within_10", "within_20", "bust_pct"]].mean().add_prefix("twin_")
    m = real.merge(agg.reset_index(), on=keyc, how="left")
    rp = []
    for _, row in m.iterrows():
        sel = tw[(tw.policy == row.policy) & (tw.consistency == row.consistency) & (tw.window == row.window)]
        rp.append(dict(rank_p_pass=float((1 + (sel.pass_pct >= row.pass_pct).sum()) / (1 + len(sel))),
                       rank_p_within_10=float((1 + (sel.within_10 >= row.within_10).sum()) / (1 + len(sel)))))
    m = pd.concat([m, pd.DataFrame(rp)], axis=1)
    return m.round(3).to_dict(orient="records")


if __name__ == "__main__":
    which = sys.argv[1:] or list(COLS)
    for h in which:
        r, *_ = analyse(h, do_eval=(h == "A3"))
        print(f"{h:9s} n={r['n_trades']:4d} $/tr {r['usd_per_trade']:8.2f} d/tr {r['d_per_trade']:7.2f} "
              f"p_d {r['p_d']:.4f} p_net {r['p_net']:.4f} t_d {r['t_d_nw']:5.2f} t_net {r['t_net_nw']:5.2f} "
              f"mc_p {r['mc_rank_p']:.3f} kill {r['kill']} failed {r['failed_gates']} ({r['seconds']}s)", flush=True)
