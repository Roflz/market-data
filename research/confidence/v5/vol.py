"""v5 per-trade volatility forecasts for the proven rules A1, A3, A4 (sessions 2018-01-01 .. 2025-06-27).

For every trade, at its ENTRY time and from data strictly before it:
  (a) HAR-RV forecast of the session's realized variance (Corsi 2009, J. Financial Econometrics 7(2) 174-196):
      RV_d = sum of squared 5-minute log returns over the day window 08:30-16:00 ET (90 returns; Andersen,
      Bollerslev, Diebold & Labys 2001/2003 realized-variance construction; 5-minute sampling per Liu, Patton &
      Sheppard 2015, J. Econometrics 187, who find 5-min RV hard to beat).  Regressors: RV of the previous session
      (daily), mean of the previous 5 (weekly), mean of the previous 22 (monthly).  OLS coefficients are refitted
      for every session on an expanding window of PAST sessions only (first fits use 2010-2017).
        har_lvl : the original Corsi (2009) levels regression.
        har_log : the log-HAR of Andersen, Bollerslev & Diebold (2007, REStat 89(4)) "Roughing it up",
                  back-transformed with exp(mu + s^2/2) (lognormal mean; s^2 = in-sample residual variance).
        rw      : naive benchmark, yesterday's RV (random-walk forecast; Hansen & Lunde 2005 style benchmark).
  (b) intraday periodicity (Andersen & Bollerslev 1997, J. Empirical Finance 4, 115-158): average over the previous
      60 sessions of the share of the day-window variance that fell in the trade's clock window
      [entry, scheduled end) - scheduled end = 16:00 for A1 / A3, 09:45 for A4.  The actual A1 exit time is NOT
      known at entry, so the scheduled end (the rule's latest exit) is used.
      Window variance forecast = daily forecast x share (the multiplicative model of Andersen & Bollerslev 1997).
  (c) v4 causal features at the last 5-minute mark <= entry (features use bars that started before the mark):
      sigma, rv_60, rv_240, rng_60, rng_60_z (out/feat_{sym}.parquet).
  (d) realized outcomes: rv_win_real (variance over [entry, scheduled end) from 5-min returns), rng_trade (log
      high/low over the actual holding [t_entry, t_exit)), rng_win (log high/low over [entry, scheduled end)),
      absret = |pnl_pts| / entry_px, abs_pnl_usd.

OUR ASSUMPTIONS (not from a source): the 08:30-16:00 day window (chosen so A4's 08:45 entry lies inside it);
sessions with < 60 one-minute bars in the window are not used as HAR observations; the 60-session periodicity
lookback and 2010 start were given by the task; the contract in the window = the most frequent instrument there
(rolls happen at 19:00/20:00 ET, outside the window).

Usage (from research/confidence; heavy -> under heavy.lock, one market at a time):
  python3 v5/vol.py build ES|NQ|YM     -> out/_vol_{sym}.parquet + truncation test
  python3 v5/vol.py merge              -> out/trades_vol.parquet + correlation table out/vol_corr.csv
"""
import importlib.util
import os
import sys
import time

import numpy as np
import pandas as pd

import research_lib as rl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
CONF = os.path.dirname(HERE)
FIRST, LAST = pd.Timestamp("2018-01-01"), pd.Timestamp("2025-06-27")
HOLDOUT_SESSION_START = pd.Timestamp("2025-06-30 18:00")
CONF_START = pd.Timestamp("2022-01-01")
W0, W1 = 8 * 60 + 30, 16 * 60          # day window 08:30-16:00 (clock minutes)
PRE = 8 * 60                            # minutes from 08:00 kept to price the 08:30 boundary
NB = (W1 - W0) // 5                     # 90 five-minute returns
MIN_BARS = 60
PER_LOOKBACK = 60
FIT_START = pd.Timestamp("2010-01-01")
MULT = {"ES": 5.0, "NQ": 2.0, "YM": 0.5}
SCHED_END = {"A1": W1, "A3": W1, "A4": 9 * 60 + 45}
V4_COLS = ["sigma", "rv_60", "rv_240", "rng_60", "rng_60_z"]


def load(sym):
    m = rl.bars_1m(sym)
    keep = (m.sess <= LAST).to_numpy() & (m.tmin >= PRE).to_numpy() & (m.tmin < W1).to_numpy()
    m = m[keep]
    d = pd.DataFrame({"O": m.Open.to_numpy(np.float64), "H": m.High.to_numpy(np.float64),
                      "L": m.Low.to_numpy(np.float64), "C": m.Close.to_numpy(np.float64),
                      "inst": m.instrument_id.to_numpy(), "sess": m.sess.to_numpy()},
                     index=m.index.tz_localize(None))
    del m
    assert d.index.max() < HOLDOUT_SESSION_START, "holdout data loaded"
    return d


def grid(d):
    """Per session: 5-minute squared returns r2 (S, 90) over 08:30-16:00 and a validity flag."""
    mod = (d.index.hour * 60 + d.index.minute).to_numpy()
    sess = d.sess.to_numpy()
    # contract: most frequent instrument of the session inside the window
    win = (mod >= W0)
    cnt = pd.DataFrame({"s": sess[win], "i": d.inst.to_numpy()[win]}).value_counts()
    main = cnt.reset_index().drop_duplicates("s").set_index("s")["i"]
    inst_ok = d.inst.to_numpy() == main.reindex(sess).to_numpy()
    d, mod, sess = d[inst_ok], mod[inst_ok], sess[inst_ok]
    sessions, si = np.unique(sess, return_inverse=True)
    S, NM = len(sessions), W1 - PRE
    k = mod - PRE
    C = np.full((S, NM), np.nan)
    O = np.full((S, NM), np.nan)
    C[si, k], O[si, k] = d.C.to_numpy(), d.O.to_numpy()
    has = ~np.isnan(C)
    idx = np.maximum.accumulate(np.where(has, np.arange(NM), -1), axis=1)
    rows = np.arange(S)
    Cff = np.where(idx >= 0, C[rows[:, None], np.maximum(idx, 0)], np.nan)
    # boundary price at 08:30 + 5j = close of the last bar that started before it; if none, open of first bar
    kb = (W0 - PRE) + 5 * np.arange(NB + 1)                    # boundary minute indices 30, 35, ..., 480
    B = np.full((S, NB + 1), np.nan)
    B[:, :NB] = Cff[:, kb[:NB] - 1]
    B[:, NB] = Cff[:, NM - 1]
    kfirst = np.argmax(has[:, W0 - PRE:], axis=1) + (W0 - PRE)
    nob = np.isnan(B[:, 0])
    B[nob, 0] = O[nob, kfirst[nob]]
    B = pd.DataFrame(B).ffill(axis=1).to_numpy()
    r2 = np.diff(np.log(B), axis=1) ** 2
    nbars = has[:, W0 - PRE:].sum(1)
    valid = (nbars >= MIN_BARS) & ~np.isnan(r2).any(1)
    r2[~valid] = np.nan
    return sessions, r2, valid


def har_forecasts(sessions, r2, valid, targets):
    """Forecasts for each target session label from strictly earlier VALID sessions (expanding-window OLS)."""
    vs = sessions[valid]
    rv = np.nansum(r2[valid], axis=1)
    n = len(rv)
    s = pd.Series(rv)
    xd, xw, xm = s.to_numpy(), s.rolling(5).mean().to_numpy(), s.rolling(22).mean().to_numpy()
    # observation i: y = rv[i], x = (1, xd[i-1], xw[i-1], xm[i-1])
    X = np.column_stack([np.ones(n), np.r_[np.nan, xd[:-1]], np.r_[np.nan, xw[:-1]], np.r_[np.nan, xm[:-1]]])
    ok = ~np.isnan(X).any(1) & (vs >= FIT_START)
    XL = np.column_stack([np.ones(n), np.log(X[:, 1:])])
    yl = np.log(np.maximum(rv, 1e-12))
    # cumulative cross-products: fit for session t uses observations i with vs[i] < t
    def cum(Xm, y):
        Xo, yo = np.where(ok[:, None], Xm, 0.0), np.where(ok, y, 0.0)
        return (np.cumsum(Xo[:, :, None] * Xo[:, None, :], axis=0), np.cumsum(Xo * yo[:, None], axis=0),
                np.cumsum(yo * yo), np.cumsum(ok.astype(float)))
    cl, cg = cum(X, rv), cum(XL, yl)
    # predictors for a target session t: last valid sessions before t
    out = []
    for t in targets:
        j = np.searchsorted(vs, t)          # number of valid sessions strictly before t
        if j < 23 or cl[3][j - 1] < 250:
            out.append((np.nan,) * 3)
            continue
        xt = np.array([1.0, xd[j - 1], xw[j - 1], xm[j - 1]])
        res = []
        for (A, b, yy, nn), x in ((cl, xt), (cg, np.r_[1.0, np.log(xt[1:])])):
            beta = np.linalg.solve(A[j - 1], b[j - 1])
            sse = yy[j - 1] - 2 * beta @ b[j - 1] + beta @ A[j - 1] @ beta
            res.append((float(x @ beta), float(sse / (nn[j - 1] - 4))))
        lvl = res[0][0]
        lg = float(np.exp(res[1][0] + 0.5 * res[1][1]))
        out.append((lvl, lg, xd[j - 1]))
    o = np.array(out, float)
    return pd.DataFrame({"har_lvl_d": o[:, 0], "har_log_d": o[:, 1], "rw_d": o[:, 2]}, index=targets)


def per_share(sessions, r2, valid, t, a, b):
    """Mean over the previous 60 valid sessions (< t) of sum r2 over buckets [a, b) / day RV."""
    vs = np.nonzero(valid & (sessions < t))[0][-PER_LOOKBACK:]
    if len(vs) < PER_LOOKBACK:
        return np.nan
    ja, jb = (a - W0) // 5, (b - W0) // 5
    x = r2[vs]
    return float(np.mean(x[:, ja:jb].sum(1) / x.sum(1)))


def load_trades(sym):
    rows = []
    for r in ("A1", "A3", "A4"):
        t = pd.read_parquet(os.path.join(CONF, "v3", "out", "trades", f"{r}.parquet"))
        t = t[(t.market == sym) & (t.session >= FIRST) & (t.session <= LAST)].copy()
        t["rule"] = r
        rows.append(t[["rule", "market", "session", "t_entry", "t_exit", "d", "entry_px", "exit_px", "pnl_pts",
                       "pnl_usd"]])
    t = pd.concat(rows, ignore_index=True)
    t["t_exit"] = t.t_exit.astype("datetime64[us]")
    t["t_entry"] = t.t_entry.astype("datetime64[us]")
    t["session"] = t.session.astype("datetime64[us]")
    return t


def forecasts(d, trades):
    """Forecast columns (a)+(b) for every trade, from d alone (d may be truncated)."""
    sessions, r2, valid = grid(d)
    tg = np.unique(trades.session.to_numpy().astype("datetime64[ns]"))
    H = har_forecasts(sessions, r2, valid, tg)
    out = trades[["rule", "session", "t_entry"]].copy()
    for c in H.columns:
        out[c] = H[c].reindex(trades.session.to_numpy().astype("datetime64[ns]")).to_numpy()
    a = (trades.t_entry.dt.hour * 60 + trades.t_entry.dt.minute).to_numpy()
    b = trades.rule.map(SCHED_END).to_numpy()
    out["share"] = [per_share(sessions, r2, valid, np.datetime64(s, "ns"), ai, bi)
                    for s, ai, bi in zip(trades.session.to_numpy(), a, b)]
    for c in ("har_lvl", "har_log", "rw"):
        out[f"{c}_win"] = np.maximum(out[f"{c}_d"], 0) * out.share
    return out


def realized(d, trades):
    sessions, r2, valid = grid(d)
    pos = {s: i for i, s in enumerate(sessions.astype("datetime64[ns]"))}
    a = (trades.t_entry.dt.hour * 60 + trades.t_entry.dt.minute).to_numpy()
    b = trades.rule.map(SCHED_END).to_numpy()
    rvw, rt, rw = [], [], []
    idx = d.index
    for s, ai, bi, te, tx in zip(trades.session.to_numpy().astype("datetime64[ns]"), a, b, trades.t_entry,
                                 trades.t_exit):
        i = pos.get(s)
        rvw.append(np.nan if i is None or not valid[i] else float(r2[i, (ai - W0) // 5:(bi - W0) // 5].sum()))
        lo_, hi_ = idx.searchsorted(te), idx.searchsorted(tx)
        seg = d.iloc[lo_:hi_]
        rt.append(np.log(seg.H.max() / seg.L.min()) if len(seg) else np.nan)
        end = te.normalize() + pd.Timedelta(minutes=int(bi))
        seg = d.iloc[lo_:idx.searchsorted(end)]
        rw.append(np.log(seg.H.max() / seg.L.min()) if len(seg) else np.nan)
    return pd.DataFrame({"rv_win_real": rvw, "rng_trade": rt, "rng_win": rw}, index=trades.index)


def v4_build():
    spec = importlib.util.spec_from_file_location("v4features", os.path.join(CONF, "v4", "features.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def v4_feats(sym, trades):
    f = pd.read_parquet(os.path.join(CONF, "v4", "out", f"feat_{sym}.parquet"), columns=["ts"] + V4_COLS)
    mark = trades.t_entry.dt.floor("5min")
    assert (mark <= trades.t_entry).all()
    x = f.set_index("ts").reindex(mark.to_numpy().astype("datetime64[ns]"))
    x.index = trades.index
    x["v4_ts"] = mark.to_numpy()
    return x


def truncation_test(sym, trades, base, n=20, n_v4=4, seed=0):
    """Rebuild the forecasts from the 1-minute data cut strictly before each sampled trade's entry and require
    identical values; control: the realized outcome must NOT be reproducible from the cut data.  Also rebuild the
    v4 features (v4/features.build) from bars before entry for a few trades."""
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(trades), min(n, len(trades)), replace=False)
    fcols = ["har_lvl_d", "har_log_d", "rw_d", "share", "har_lvl_win", "har_log_win", "rw_win"]
    full = load(sym)
    bad, ctrl = [], 0
    for i in pick:
        tr = trades.iloc[[i]]
        te = tr.t_entry.iloc[0]
        cut = full[full.index < te]
        assert cut.index.max() < te
        f = forecasts(cut, tr)
        a, b = f[fcols].to_numpy(float)[0], base.loc[tr.index, fcols].to_numpy(float)[0]
        if not np.allclose(a, b, rtol=1e-9, atol=0, equal_nan=True):
            bad.append((str(te), [c for c, x, y in zip(fcols, a, b) if not np.isclose(x, y, equal_nan=True)]))
        rr = realized(cut, tr)
        ctrl += int(np.isclose(rr.rng_trade.iloc[0], base.loc[tr.index[0], "rng_trade"]))
    # v4 features from truncated raw data (v4's own loader incl. volume)
    v4 = v4_build()
    d4 = v4.load(sym)
    sess_all = np.unique(d4.sess.to_numpy())
    bad4 = []
    for i in pick[:n_v4]:
        tr = trades.iloc[i]
        mark = tr.t_entry.floor("5min")
        j = np.searchsorted(sess_all, tr.session.to_datetime64())
        sub = d4[(d4.sess >= sess_all[max(j - 30, 0)]) & (d4.index < tr.t_entry)]
        hit = v4.build(sub, sym)
        hit = hit[hit.ts == mark]
        a = hit[V4_COLS].to_numpy(float)[0] if len(hit) else np.full(len(V4_COLS), -1.0)
        b = base.loc[trades.index[i], V4_COLS].to_numpy(float)
        if not np.allclose(a, b, rtol=1e-9, equal_nan=True):
            bad4.append((str(tr.t_entry), a.tolist(), b.tolist()))
    print(f"{sym} truncation: forecasts {len(pick) - len(bad)}/{len(pick)} identical; control (realized range "
          f"reproduced from cut data) {ctrl}/{len(pick)} (expect 0); v4 features {n_v4 - len(bad4)}/{n_v4} identical")
    return len(pick), bad, ctrl, n_v4, bad4


def main_build(sym):
    t0 = time.time()
    trades = load_trades(sym)
    d = load(sym)
    f = forecasts(d, trades)
    r = realized(d, trades)
    del d
    v = v4_feats(sym, trades)
    out = pd.concat([trades, f.drop(columns=["rule", "session", "t_entry"]), r, v], axis=1)
    out["absret"] = (out.pnl_pts.abs() / out.entry_px)
    out["abs_pnl_usd"] = out.pnl_usd.abs()
    out["abs_pnl_pts_usd"] = out.pnl_pts.abs() * MULT[sym]
    out["sched_end"] = out.rule.map(SCHED_END)
    n, bad, ctrl, n4, bad4 = truncation_test(sym, trades, out)
    out.attrs = {}
    os.makedirs(OUT, exist_ok=True)
    out.to_parquet(os.path.join(OUT, f"_vol_{sym}.parquet"), compression="zstd")
    msg = (f"{sym}: trades={len(out)} trunc {n - len(bad)}/{n} ctrl {ctrl} v4 {n4 - len(bad4)}/{n4} "
           f"bad={bad[:2]} bad4={bad4[:1]} s={time.time() - t0:.0f}")
    print(msg)
    with open(os.path.join(OUT, "vol_build.log"), "a") as fh:
        fh.write(msg + "\n")


def corr_table(t):
    fc = {"har_lvl_win": "sqrt", "har_log_win": "sqrt", "rw_win": "sqrt", "share": "sqrt",
          "har_lvl_d": "sqrt", "har_log_d": "sqrt", "sigma": "id", "sig_rv60": "id", "sig_rv240": "id",
          "rng_60": "id"}
    tg = ["rv_win_real", "rng_win", "rng_trade", "absret"]
    t = t.copy()
    t["sig_rv60"] = t.sigma * t.rv_60
    t["sig_rv240"] = t.sigma * t.rv_240
    rows = []
    groups = [("A1", t.rule == "A1"), ("A3", t.rule == "A3"), ("A4", t.rule == "A4")]
    groups += [(f"A3-{m}", (t.rule == "A3") & (t.market == m)) for m in ("ES", "NQ", "YM")]
    for g, msk in groups:
        for per, pm in (("2018+", t.session >= FIRST), ("2022+", t.session >= CONF_START)):
            x = t[msk & pm]
            for f, how in fc.items():
                fv = np.sqrt(x[f].clip(lower=0)) if how == "sqrt" else x[f]
                for y in tg:
                    yv = np.sqrt(x[y]) if y == "rv_win_real" else x[y]
                    ok = fv.notna() & yv.notna() & (fv > 0)
                    sp = fv[ok].rank().corr(yv[ok].rank())
                    lp = np.log(fv[ok]).corr(np.log(yv[ok].clip(lower=1e-9))) if y != "absret" else np.nan
                    rows.append(dict(group=g, period=per, forecast=f, target=y, n=int(ok.sum()),
                                     spearman=round(sp, 3), pearson_log=round(lp, 3) if lp == lp else np.nan))
    return pd.DataFrame(rows)


def main_merge():
    t = pd.concat([pd.read_parquet(os.path.join(OUT, f"_vol_{s}.parquet")) for s in ("ES", "NQ", "YM")],
                  ignore_index=True).sort_values(["t_entry", "rule", "market"]).reset_index(drop=True)
    assert t.t_exit.max() < HOLDOUT_SESSION_START
    t.to_parquet(os.path.join(OUT, "trades_vol.parquet"), compression="zstd")
    c = corr_table(t)
    c.to_csv(os.path.join(OUT, "vol_corr.csv"), index=False)
    pv = c[c.target.isin(["rv_win_real", "rng_trade", "absret"])].pivot_table(
        index=["group", "period", "forecast"], columns="target", values="spearman")
    pd.set_option("display.width", 200)
    print(pv.to_string())
    print("missing per column:", t[["har_lvl_win", "har_log_win", "share", "sigma", "rng_trade", "rv_win_real"]]
          .isna().sum().to_dict())
    try:
        import run_pipeline as rp
        for g in ("A1", "A3", "A4"):
            r = c[(c.group == g) & (c.period == "2018+") & (c.forecast == "har_log_win") & (c.target == "absret")]
            rp.log_trial(module="v5-vol", scope=g, model="HAR-RV(log) x periodicity", target="|ret| per trade",
                         oos_rows=int(r.n.iloc[0]), oos_auc=float(r.spearman.iloc[0]),
                         parameters="day window 08:30-16:00, 5-min RV, expanding OLS from 2010, 60-session share",
                         note="spearman(forecast sd, |trade return|) 2018-2025H1; causal; see v5/out/vol_corr.csv")
    except Exception as e:
        print("log_trial failed:", e)


if __name__ == "__main__":
    if sys.argv[1] == "build":
        main_build(sys.argv[2])
    elif sys.argv[1] == "merge":
        main_merge()
