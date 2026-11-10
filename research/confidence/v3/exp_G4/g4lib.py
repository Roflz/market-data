"""
v3/exp_G4/g4lib.py - G4 (macro releases & FOMC, family F2): signals and the pre-registered analysis of PREREG.md.

Light: reads only v3/data through the harness (no 1-minute data; no lock needed).
Signals are fn(S, B) -> entries (session, entry, exit, d[, stop_pts]) using only the sessions table S and bars B,
so they can be passed to H.lookahead_check and to the targeted truncation check (check_trunc).

Column ids (each logged once with H.log, module v3-<hid>):
  A4      Tier A: CPI/NFP 08:30 -> 08:45 move faded 08:45 -> 09:45, MNQ
  S4.1    NFP only (MNQ)            S4.2  CPI only (MNQ)
  S4.3    big-move only: |m| in bp above the expanding median of all EARLIER eligible events (MNQ)
  S4.4    A4 on MES                 S4.5  A4 on MYM (2018+)
  S4.6    A4 with a disaster stop at 2|m| from entry (MNQ)
  S4.7    archive NFP rule: NFP sessions, at 09:30 against the 08:30 -> 09:30 move, exit 16:00 (MNQ)
  S4.8    FOMC reversal basket (MES+MNQ+MYM): entry = statement - 15 min, side = -sign(px(entry mark) /
          px(same mark, previous session) - 1), exit 16:00, +1 extra tick on the exit
  S4.9_ES / S4.9_NQ / S4.9_YM   long 18:00 -> 16:45 on FOMC, NFP and CPI sessions (MES first, MNQ, MYM)
  N4.1    A4 exit 09:30    N4.2  A4 exit 10:00    N4.3  A4 entry 09:00 (signal 08:30 -> 09:00)   (neighbours)
  C3      A4 rule on all non-release sessions (reported control, logged for completeness)
Seeds: C1 chunk c of column with seed id k -> seed 1000*k + c (A4 -> k = 4, as PREREG 0.3; secondaries k = 41..).
"""
import json
import math
import os
import warnings

import numpy as np
import pandas as pd

import harness as H
import stats_protocol as sp

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = H.HERE
OUT = os.path.join(V3, "out")
END = pd.Timestamp("2025-06-27")
CAL = H.calendar(("NQ", "ES"))
CAL = CAL[CAL <= END]
PREF = {"NQ": 20789.6, "ES": 5843.2, "YM": 42516.3}
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
BASE_SEED = 20261109
PREREG_SHA = "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
N_EFF_F2 = 45
BLOCKS2 = [(2010, 2011), (2012, 2013), (2014, 2015), (2016, 2017), (2018, 2019), (2020, 2021), (2022, 2023),
           (2024, 2025)]
warnings.filterwarnings("ignore", message="time_trades")

# FOMC scheduled statement times (exchange calendar, known in advance; used like the event flags)
_F = pd.read_csv(os.path.join(V3, "..", "..", "..", "data", "fomc_dates.csv"))
_F = _F[_F.scheduled.astype(bool)]
_F["date"] = pd.to_datetime(_F.date).dt.normalize()
_F = _F[_F.date <= END]
FOMC_ENTRY = {d: {"14:00": "1345", "14:15": "1400", "12:30": "1215"}[t]
              for d, t in zip(_F.date, _F.statement_time_et)}


# ============================================================================================ signals
def _skip_stale(S, marks):
    ok = ~S["roll"].astype(bool).to_numpy()
    for mk in marks:
        a = S[f"age_{mk}"].to_numpy()
        ok &= ~(a > 5)
    return ok


def release_fade(days="both", sig=("0830", "0845"), entry="0845", exit_="0945", stop_mult=None, bigmove=False):
    """A4 family. days: 'both' (nfp|cpi), 'nfp', 'cpi', 'non' (all non-release sessions = C3)."""
    def fn(S, B):
        nfp, cpi = S["nfp"].astype(bool).to_numpy(), S["cpi"].astype(bool).to_numpy()
        ev = {"both": nfp | cpi, "nfp": nfp, "cpi": cpi, "non": ~(nfp | cpi)}[days]
        a, b = S[f"px_{sig[0]}"].to_numpy(float), S[f"px_{sig[1]}"].to_numpy(float)
        marks = sorted({sig[0], sig[1], entry, exit_})
        ok = ev & _skip_stale(S, marks) & np.isfinite(a) & np.isfinite(b) & np.isfinite(S[f"px_{entry}"].to_numpy(float))
        m = b - a
        trade = ok & (m != 0)
        if bigmove:
            bp = np.abs(m) / a * 1e4
            hist = pd.Series(np.where(ok, bp, np.nan), index=S.index)
            med = hist.expanding(min_periods=1).median().shift(1).ffill().to_numpy()   # median of EARLIER events
            # expanding() over NaN rows keeps the last value; shift(1) -> strictly earlier sessions only
            trade &= np.isfinite(med) & (bp > med)
        idx = np.flatnonzero(trade)
        e = pd.DataFrame({"session": S.index[idx], "entry": entry, "exit": exit_,
                          "d": -np.sign(m[idx]).astype(int), "m_pts": m[idx]})
        if stop_mult is not None:
            e["stop_pts"] = stop_mult * np.abs(m[idx])
        return e
    return fn


def nfp_930_fade(S, B):
    """S4.7 archive NFP rule: NFP sessions, at 09:30 trade against px_0930 - px_0830, exit 16:00."""
    nfp = S["nfp"].astype(bool).to_numpy()
    a, b = S["px_0830"].to_numpy(float), S["px_0930"].to_numpy(float)
    ok = nfp & _skip_stale(S, ["0830", "0930", "1600"]) & np.isfinite(a) & np.isfinite(b)
    m = b - a
    idx = np.flatnonzero(ok & (m != 0))
    return pd.DataFrame({"session": S.index[idx], "entry": "0930", "exit": "1600",
                         "d": -np.sign(m[idx]).astype(int), "m_pts": m[idx]})


def fomc_reversal(S, B):
    """S4.8: scheduled FOMC sessions; entry mark = statement time - 15 min; signal = px(mark) / px(same mark of the
    previous session) - 1; side = -sign(signal); exit 16:00. Roll sessions skipped (previous price = other contract)."""
    rows = []
    roll = S["roll"].astype(bool)
    pos = {s: i for i, s in enumerate(S.index)}
    for s, mk in FOMC_ENTRY.items():
        i = pos.get(s)
        if i is None or i == 0 or roll.iloc[i]:
            continue
        p1 = S[f"px_{mk}"].iloc[i]
        p0 = S[f"px_{mk}"].iloc[i - 1]
        if not (np.isfinite(p1) and np.isfinite(p0)) or p1 == p0:
            continue
        rows.append(dict(session=s, entry=mk, exit="1600", d=-int(np.sign(p1 / p0 - 1)), sig_ret=p1 / p0 - 1))
    return pd.DataFrame(rows, columns=["session", "entry", "exit", "d", "sig_ret"])


def announcement_long(S, B):
    """S4.9: long 18:00 -> 16:45 on FOMC, NFP and CPI sessions (sessions with an 18:00 price)."""
    ev = (S["fomc"].astype(bool) | S["nfp"].astype(bool) | S["cpi"].astype(bool)).to_numpy()
    ok = ev & np.isfinite(S["px_1800"].to_numpy(float))
    idx = np.flatnonzero(ok)
    return pd.DataFrame({"session": S.index[idx], "entry": "1800", "exit": "1645", "d": 1})


# ---------------------------------------------------------------------------------- EXPLORATORY (labelled, logged)
def release_fade_close844(S, B):
    """E4.1 EXPLORATORY execution check of A4: m = close of the 5-minute bar 08:40-08:45 (the last 08:44 price, known
    BEFORE the 08:45 fill) - px_0830; enter at the 08:45 mark, exit 09:45. Same skips as A4."""
    b = B[5]
    sel = (b.index.hour == 8) & (b.index.minute == 40)
    c = pd.Series(b.loc[sel, "C"].to_numpy(float), index=pd.DatetimeIndex(b.loc[sel, "session"]).normalize())
    c = c[~c.index.duplicated(keep="last")].reindex(S.index)
    nfp, cpi = S["nfp"].astype(bool).to_numpy(), S["cpi"].astype(bool).to_numpy()
    a = S["px_0830"].to_numpy(float)
    ok = (nfp | cpi) & _skip_stale(S, ["0830", "0845", "0945"]) & np.isfinite(a) & np.isfinite(c.to_numpy()) \
        & np.isfinite(S["px_0845"].to_numpy(float))
    m = c.to_numpy() - a
    idx = np.flatnonzero(ok & (m != 0))
    return pd.DataFrame({"session": S.index[idx], "entry": "0845", "exit": "0945",
                         "d": -np.sign(m[idx]).astype(int), "m_pts": m[idx]})


def fomc_reversal_chained(S, B):
    """S4.8x EXPLORATORY: S4.8 plus the roll sessions, whose 24-hour signal is chained within contracts:
    (old contract: px_1645[prev] / px_mark[prev]) x (new contract: px_mark / first priced mark of the session) - 1
    (the 16:45 -> first-bar gap is taken as 0)."""
    rows = []
    roll = S["roll"].astype(bool)
    pos = {s: i for i, s in enumerate(S.index)}
    for s, mk in FOMC_ENTRY.items():
        i = pos.get(s)
        if i is None or i == 0:
            continue
        p1 = S[f"px_{mk}"].iloc[i]
        p0 = S[f"px_{mk}"].iloc[i - 1]
        if not (np.isfinite(p1) and np.isfinite(p0)):
            continue
        if roll.iloc[i]:
            k = H.mark_index(mk)
            row = S.iloc[i][[f"px_{x}" for x in H.MARKS[:k + 1]]].to_numpy(float)
            fin = np.flatnonzero(np.isfinite(row))
            last_old = S["px_1645"].iloc[i - 1]
            if not len(fin) or not np.isfinite(last_old):
                continue
            sig = (last_old / p0) * (p1 / row[fin[0]]) - 1
        else:
            sig = p1 / p0 - 1
        if sig == 0:
            continue
        rows.append(dict(session=s, entry=mk, exit="1600", d=-int(np.sign(sig)), sig_ret=sig, roll=bool(roll.iloc[i])))
    return pd.DataFrame(rows, columns=["session", "entry", "exit", "d", "sig_ret", "roll"])


# ============================================================================================ look-ahead
def check_trunc(fn, sym, entries, n=20, seed=0, tfs=(5,)):
    """Targeted truncation check: for n random actual entries, cut the data AT the entry mark of that session and
    re-run fn; every entry with entry time <= cut must be identical. Returns n checked."""
    rng = np.random.default_rng(seed)
    e = entries.reset_index(drop=True)
    pick = rng.choice(len(e), size=min(n, len(e)), replace=False)
    cols = [c for c in ("session", "entry", "exit", "d", "stop_pts") if c in e.columns]
    for j in pick:
        s, mk = pd.Timestamp(e.session.iloc[j]), e.entry.iloc[j]
        Sc, B = H.truncate(sym, s, mk, tfs=tfs)
        cut = fn(Sc, B)
        T = H.mark_time(s, H.mark_index(mk))
        def keep(x):
            if not len(x):
                return x[cols]
            t = H.mark_time(pd.DatetimeIndex(pd.to_datetime(x.session)), H._marks(x.entry))
            y = x.loc[np.asarray(t <= T), cols].reset_index(drop=True)
            y["entry"] = H._marks(y["entry"])
            return y
        a, b = keep(e), keep(cut)
        if not (len(a) == len(b) and a.astype(str).equals(b.astype(str))):
            raise AssertionError(f"look-ahead in {fn} at {s.date()} {mk}: {len(a)} vs {len(b)}")
    return len(pick)


# ============================================================================================ trades + controls
def _adj(tr, sym, extra_ticks):
    """+extra ticks of cost per trade (S4.8 exit tick; cost stress)."""
    if extra_ticks:
        x = extra_ticks * H.SPEC[sym]["tick"] * H.SPEC[sym]["usd"]
        tr = tr.copy()
        tr["cost_usd"] = tr["cost_usd"] + x
        tr["pnl_usd"] = tr["pnl_usd"] - x
    return tr


def u2(tr, sym):
    usd = H.SPEC[sym]["usd"]
    g = tr["d"].to_numpy(float) * (tr["exit_px"].to_numpy(float) - tr["entry_px"].to_numpy(float)) / tr["entry_px"].to_numpy(float)
    return g * PREF[sym] * usd - tr["cost_usd"].to_numpy(float)


def run_leg(sym, ent, kseed, R=999, extra_ticks=0, nrep_ctrl=100):
    """Actual trades, C1 (R draws in chunks of <= 100), plain drift, hour drift, C2 (random side) and the standard
    random-marks control, for one market."""
    e = ent.copy().reset_index(drop=True)
    e["tid"] = np.arange(len(e))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tr = _adj(H.time_trades(sym, e), sym, extra_ticks)
    dropped = tr.attrs.get("dropped", {})
    ek = e[e.tid.isin(tr.tid)].reset_index(drop=True)
    c1 = []
    for c in range(int(math.ceil(R / 100))):
        nr = min(100, R - 100 * c)
        rd = H.random_time_trades(sym, ek, n_rep=nr, seed=1000 * kseed + c, keep_session=False, keep_marks=True,
                                  keep_side=True)
        rd = _adj(rd, sym, extra_ticks)
        rd = rd[pd.DatetimeIndex(rd.session) <= END]          # protocol calendar: draws on 2025-06-30 dropped
        rd["rep"] = rd["rep"] + 100 * c
        c1.append(rd[["tid", "rep", "session", "pnl_usd", "gross_usd", "cost_usd", "d", "entry_px", "exit_px",
                      "t_entry", "t_exit", "risk_usd", "market"]])
    c1 = pd.concat(c1, ignore_index=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dr = _adj(H.drift_trades(sym, ek), sym, extra_ticks)
        hd = _adj(H.hour_drift_trades(sym, ek, n_rep=nrep_ctrl, seed=1000 * kseed + 900), sym, extra_ticks)
        hd = hd[pd.DatetimeIndex(hd.session) <= END]
        c2 = _adj(H.random_time_trades(sym, ek, n_rep=nrep_ctrl, seed=1000 * kseed + 901, keep_session=True,
                                       keep_marks=True, keep_side=False), sym, extra_ticks)
        rnd = _adj(H.random_time_trades(sym, ek, n_rep=nrep_ctrl, seed=1000 * kseed + 902), sym, extra_ticks)
    return dict(sym=sym, ent=ek, trades=tr, c1=c1, drift=dr, hour_drift=hd, c2=c2, rnd=rnd, dropped=dropped, R=R)


# ============================================================================================ analysis
def _dsr_safe(x, n):
    try:
        return float(sp.dsr(x, n)["dsr"])
    except Exception:
        return float("nan")


def _win_mean(x, days, a, b):
    m = (days >= pd.Timestamp(a)) & (days <= pd.Timestamp(b))
    return float(x[m].mean()) if m.any() else float("nan")


def _tt(v):
    v = np.asarray(v, float)
    return (float(v.mean()), float(sp.hac_t(v)[0])) if len(v) > 20 and v.std() > 0 else (float("nan"), float("nan"))


def analyze(hid, legs, tier="B", n_eff=N_EFF_F2, kill_window_years=None, desc="", params=None, cost_stress=True):
    """legs: list of run_leg outputs (several = basket). Builds the standard daily file, results JSON, trades parquet.
    Returns the result dict (also written to v3/out/results/<hid>.json)."""
    T = len(CAL)
    days = CAL
    yrs = days.year.to_numpy()
    allt = []
    net = pd.Series(0.0, index=CAL); gross = net.copy(); netu2 = net.copy(); ctrl = net.copy(); ntr = net.copy()
    per_mkt = {s: pd.Series(0.0, index=CAL) for s in ("ES", "NQ", "YM")}
    rep_tot = None
    stress = net.copy()
    ctrl_rows = {}
    for L in legs:
        sym, tr, c1 = L["sym"], L["trades"].copy(), L["c1"]
        tr = tr[pd.DatetimeIndex(tr.session) <= END]
        tr["net_U2"] = u2(tr, sym)
        ci = c1.groupby("tid")["pnl_usd"].mean()
        tr["c1"] = tr["tid"].map(ci).to_numpy()
        tr["c1_n"] = tr["tid"].map(c1.groupby("tid").size()).to_numpy()
        tr["d_i"] = tr["pnl_usd"] - tr["c1"]
        allt.append(tr)
        sess = pd.DatetimeIndex(tr.session)
        g = lambda col: tr[col].groupby(sess).sum().reindex(CAL, fill_value=0.0)
        net += g("pnl_usd"); gross += g("gross_usd"); netu2 += g("net_U2"); ctrl += g("c1")
        ntr += tr.groupby(sess).size().reindex(CAL, fill_value=0)
        per_mkt[sym] += g("pnl_usd")
        st = tr["pnl_usd"] - 2 * H.SPEC[sym]["tick"] * H.SPEC[sym]["usd"]
        stress += st.groupby(sess).sum().reindex(CAL, fill_value=0.0)
        # C1 strategy totals per rep (missing draws filled with that trade's c_i)
        P = c1.pivot_table(index="tid", columns="rep", values="pnl_usd", aggfunc="first")
        P = P.reindex(index=tr.tid.to_numpy())
        P = P.apply(lambda col: col.fillna(pd.Series(tr.c1.to_numpy(), index=tr.tid.to_numpy())))
        tot = P.sum(axis=0).to_numpy()
        rep_tot = tot if rep_tot is None else rep_tot + tot
        for name in ("drift", "hour_drift", "c2", "rnd"):
            ctrl_rows.setdefault(name, []).append(L[name])
    trades = pd.concat(allt, ignore_index=True)
    d = (net - ctrl)
    x_d, x_net, x_u2 = d.to_numpy(), net.to_numpy(), netu2.to_numpy()
    p_d, p_d_bl = sp.conservative_p(sp.boot_pvalue_mean, x_d, B=5000, seed=BASE_SEED)
    p_net, p_net_bl = sp.conservative_p(sp.boot_pvalue_mean, x_net, B=5000, seed=BASE_SEED)
    p_st, _ = sp.conservative_p(sp.boot_pvalue_mean, stress.to_numpy(), B=5000, seed=BASE_SEED)
    rr_d = sp.robust_report(x_d, days.to_numpy())
    rr_net = sp.robust_report(x_net, days.to_numpy())
    rr_u2 = sp.robust_report(x_u2, days.to_numpy())
    t_d, t_net = float(sp.hac_t(x_d)[0]), float(sp.hac_t(x_net)[0])
    # trade-level views
    tdays = pd.DatetimeIndex(trades.session)
    first_trade_year = int(tdays.year.min())
    def per_trade(mask):
        sub = trades[mask]
        return dict(n=int(len(sub)), net=float(sub.pnl_usd.mean()) if len(sub) else float("nan"),
                    gross=float(sub.gross_usd.mean()) if len(sub) else float("nan"),
                    d=float(sub.d_i.mean()) if len(sub) else float("nan"),
                    u2=float(sub.net_U2.mean()) if len(sub) else float("nan"),
                    win=float((sub.pnl_usd > 0).mean() * 100) if len(sub) else float("nan"))
    wins = {"all": ("2010-01-01", "2025-06-30"), "2010-17": ("2010-01-01", "2017-12-31"),
            "2018-25H1": ("2018-01-01", "2025-06-30"), "2018+": ("2018-01-01", "2025-06-30"),
            "2022+": ("2022-01-01", "2025-06-30")}
    by_win = {w: per_trade((tdays >= a) & (tdays <= b)) for w, (a, b) in wins.items()}
    by_year = {int(y): per_trade(tdays.year == y) for y in sorted(set(tdays.year))}
    by_year_daytot = {int(y): float(x_net[yrs == y].sum()) for y in sorted(set(yrs))}
    blocks = {}
    for a, b in BLOCKS2:
        m = (yrs >= a) & (yrs <= b)
        tm = (tdays.year >= a) & (tdays.year <= b)
        if tm.sum() == 0:
            continue
        blocks[f"{a}-{str(b)[2:]}"] = dict(u2=float(x_u2[m].sum()), u1=float(x_net[m].sum()), d=float(x_d[m].sum()),
                                           n=int(tm.sum()))
    share_blocks_u2 = float(np.mean([v["u2"] > 0 for v in blocks.values()]))
    # matched-control rank p and C1 summary
    rep_means = rep_tot / T
    mc_p = sp.mc_rank_p(x_net.mean(), rep_means)
    # controls per trade
    def cmean(name, a="1900-01-01", b="2100-01-01"):
        frames = ctrl_rows[name]
        v = []
        for f in frames:
            s = pd.DatetimeIndex(f.session)
            v.append(f.loc[(s >= a) & (s <= b), "pnl_usd"])
        v = pd.concat(v)
        return float(v.mean()) if len(v) else float("nan")
    controls = {}
    for w, (a, b) in wins.items():
        controls[w] = dict(actual=by_win[w]["net"], C1=float(trades.loc[(tdays >= a) & (tdays <= b), "c1"].mean())
                           if ((tdays >= a) & (tdays <= b)).any() else float("nan"),
                           drift=cmean("drift", a, b), hour_drift=cmean("hour_drift", a, b),
                           C2_random_side=cmean("c2", a, b), random_marks=cmean("rnd", a, b))
    # gates (U1 unless stated); halves N/A when the column has no trades in 2010-17 (MYM)
    has_h1 = first_trade_year <= 2017
    m17 = yrs <= 2017
    gates = {}
    gates["1_d_both_halves"] = bool((not has_h1 or x_d[m17].mean() > 0) and x_d[~m17].mean() > 0)
    gates["2_u2_halves_u1_18_22"] = bool((not has_h1 or x_u2[m17].mean() > 0) and x_u2[~m17].mean() > 0
                                         and x_net[~m17].mean() > 0 and x_net[yrs >= 2022].mean() > 0)
    gates["3_share_2yr_blocks_u2>=60%"] = bool(share_blocks_u2 >= 0.6)
    gates["4_net_wo_10_best>0"] = bool(rr_net["drop_best"][0] > 0)
    gates["5_winsor_net>0"] = bool(rr_net["winsor"][0] > 0)
    gates["6_mc_rank_p<=0.05"] = bool(mc_p <= 0.05)
    t18 = trades[tdays >= pd.Timestamp("2018-01-01")]
    g_over_c = float(t18.gross_usd.mean() / t18.cost_usd.mean()) if len(t18) else float("nan")
    gates["7_gross>=1.5x_cost_2018"] = bool(g_over_c >= 1.5)
    gates["8_beats_drift_and_hour_drift"] = bool(by_win["all"]["net"] > controls["all"]["drift"]
                                                 and by_win["all"]["net"] > controls["all"]["hour_drift"])
    failed = [k for k, v in gates.items() if not v]
    dsr_d = _dsr_safe(x_d, n_eff)
    killed = bool(x_d.mean() <= 0 or x_net[~m17].mean() <= 0)
    stats_tab = H.stats(trades.assign(market=trades.market), calendar_=CAL)
    res = dict(hid=hid, desc=desc, tier=tier, params=params or {}, prereg_sha256=PREREG_SHA,
               markets=[MICRO[L["sym"]] for L in legs], R_C1=int(legs[0]["R"]),
               n_trades=int(len(trades)), trades_per_year=float(len(trades) / (T / 252.0)),
               sessions_with_trade_pct=float((ntr > 0).mean() * 100),
               mean_net_per_trade=float(trades.pnl_usd.mean()), mean_d_per_trade=float(trades.d_i.mean()),
               mean_c1_per_trade=float(trades.c1.mean()), mean_gross_per_trade=float(trades.gross_usd.mean()),
               mean_u2_per_trade=float(trades.net_U2.mean()), win_pct=float((trades.pnl_usd > 0).mean() * 100),
               mean_d_daily=float(x_d.mean()), mean_net_daily=float(x_net.mean()),
               p_d=float(p_d), p_d_blocks={str(k): float(v) for k, v in p_d_bl.items()},
               p_net=float(p_net), p_net_blocks={str(k): float(v) for k, v in p_net_bl.items()},
               t_d_nw=t_d, t_net_nw=t_net,
               sharpe_ann_net=float(x_net.mean() / x_net.std(ddof=1) * math.sqrt(252)),
               sharpe_daily_net=float(x_net.mean() / x_net.std(ddof=1)),
               dsr_d=dsr_d, n_eff=n_eff, mc_rank_p=float(mc_p),
               c1_strategy_mean_daily=dict(mean=float(rep_means.mean()), sd=float(rep_means.std(ddof=1))),
               gross_over_cost_2018=g_over_c,
               robust_d=rr_d, robust_net=rr_net, robust_u2=rr_u2,
               by_window_per_trade=by_win, by_year_per_trade=by_year, by_year_net_total=by_year_daytot,
               blocks_2yr=blocks, share_blocks_u2_pos=share_blocks_u2,
               net_wo_10_best_total=float(np.where(np.isin(np.arange(T), np.argsort(-x_net)[:10]), 0, x_net).sum()),
               net_total=float(x_net.sum()),
               controls_per_trade=controls,
               cost_stress_plus1tick=dict(mean_per_trade=float(stress.sum() / len(trades)), p_net=float(p_st),
                                          t_nw=float(sp.hac_t(stress.to_numpy())[0]),
                                          per_trade_2018=float(stress[days >= "2018-01-01"].sum()
                                                               / max(1, (tdays >= "2018-01-01").sum())),
                                          per_trade_2010_17=float(stress[days <= "2017-12-31"].sum()
                                                                  / max(1, (tdays <= "2017-12-31").sum()))),
               per_market={MICRO[s]: dict(total=float(per_mkt[s].sum()),
                                          per_trade=float(trades.loc[trades.market == s, "pnl_usd"].mean())
                                          if (trades.market == s).any() else float("nan"),
                                          per_trade_2018=float(trades.loc[(trades.market == s) & (tdays >= "2018-01-01"),
                                                                          "pnl_usd"].mean())
                                          if ((trades.market == s) & (tdays >= "2018-01-01")).any() else float("nan"),
                                          n=int((trades.market == s).sum()))
                           for s in ("ES", "NQ", "YM")},
               gates=gates, failed_gates=failed, killed=killed,
               dropped={L["sym"]: L["dropped"] for L in legs},
               stats_table=stats_tab.round(4).to_dict(orient="records"))
    # standard outputs
    daily = pd.DataFrame({"session": CAL.date, "net_U1": x_net, "net_U2": x_u2, "gross_U1": gross.to_numpy(),
                          "ctrl_C1": ctrl.to_numpy(), "d": x_d, "n_trades": ntr.to_numpy().astype(int),
                          "net_ES": per_mkt["ES"].to_numpy(), "net_NQ": per_mkt["NQ"].to_numpy(),
                          "net_YM": per_mkt["YM"].to_numpy()})
    for sub in ("daily", "trades", "results"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    daily.to_csv(os.path.join(OUT, "daily", f"{hid}.csv"), index=False)
    daily[["session", "net_U1"]].rename(columns={"net_U1": "pnl_usd"}).to_csv(
        os.path.join(HERE, f"daily_{hid}.csv"), index=False)
    tsave = trades.copy()
    for c in tsave.columns:
        if tsave[c].dtype == object:
            tsave[c] = tsave[c].astype(str)
    tsave.to_parquet(os.path.join(OUT, "trades", f"{hid}.parquet"), index=False)
    with open(os.path.join(OUT, "results", f"{hid}.json"), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    res["_daily"] = daily
    res["_trades"] = trades
    res["_rep_tot"] = rep_tot
    return res


def tier_b_label(res, stepm_p):
    fails = list(res["failed_gates"])
    if stepm_p > 0.004:
        fails.append(f"StepM p {stepm_p:.4f} > 0.004")
    if res["t_d_nw"] < 3:
        fails.append(f"NW t(d) {res['t_d_nw']:.2f} < 3")
    if not res["dsr_d"] >= 0.95:
        fails.append(f"DSR {res['dsr_d']:.2f} < 0.95 (N_eff {res['n_eff']})")
    if res["killed"]:
        lab = "KILLED (mean d <= 0 or 2018-25H1 net <= 0)"
    elif not fails:
        lab = "SIGNIFICANT (Tier B)"
    elif res["t_d_nw"] >= 2 and len(fails) <= 2:
        lab = "PROMISING (forward paper only)"
    else:
        lab = "NOT SIGNIFICANT"
    return lab, fails
