"""v5/sizing.py - runs v5/PLAN.md (frozen; sha256 in v5/out/PLAN.sha256): volatility-forecast sizing policies vs fixed
sizing for P1 = A1 + A3 + A4 and A1 alone, LucidFlex 25K eval from every start day, real stream + 200 C1 twins.

Policies (see PLAN.md section 3 for sources): FIXED n0, FIXRISK B, VT, CVT, CVTDN, IV, EV.
Outputs (v5/out): sizing_real.csv, sizing_twins.csv, sizing_tests.csv, sizing_diag.csv, sizing_checks.txt,
                  _sizing_perstart.npz (per-start outcomes of the real stream).
usage: python3 v5/sizing.py [n_twins] [n_workers]
"""
import json
import os
import sys
import time
import warnings
from dataclasses import replace
from multiprocessing import Pool

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.dirname(HERE)
V3 = os.path.join(CONF, "v3")
OUT = os.path.join(HERE, "out")
sys.path.insert(0, os.path.join(V3, "exp_G4"))
import eval_sim as E  # noqa: E402
import harness as H  # noqa: E402
import prop_sim as ps  # noqa: E402

END = pd.Timestamp("2025-06-27")
FIRST = pd.Timestamp("2018-01-01")
NT = int(sys.argv[1]) if len(sys.argv) > 1 else 200
NW = int(sys.argv[2]) if len(sys.argv) > 2 else 3
PV = {"ES": 5.0, "NQ": 2.0, "YM": 0.5}
WINDOWS = {"2018+": ("2018-01-01", "2025-06-30"), "2022+": ("2022-01-01", "2025-06-30")}
CONS = (0.40, 0.50)
LEVELS_REAL = [1, 2, 3, 4, 5, 6, 8, 10]
LEVELS_TWIN = [1, 2, 3, 5]
B_REAL = [100, 150, 250, 400, 600]
B_TWIN = [150, 250, 400]
VOLPOL = ["VT", "CVT", "CVTDN", "IV", "EV"]
MIN_HIST, MIN_EV = 20, 50
NMAX, DLL = 20, 600.0

CAL = pd.read_csv(os.path.join(V3, "out", "daily", "A1.csv"), parse_dates=["session"])["session"]
CAL = pd.DatetimeIndex(CAL[(CAL >= FIRST) & (CAL <= END)])
CALPOS = {d: i for i, d in enumerate(CAL.to_numpy().astype("datetime64[ns]").view(np.int64).tolist())}
NCAL = len(CAL)
WMASK = {w: (CAL >= pd.Timestamp(a)) & (CAL <= pd.Timestamp(b)) for w, (a, b) in WINDOWS.items()}
SIDX = np.flatnonzero(WMASK["2018+"])                         # all start days (2018+ includes 2022+)


# =========================================================================================== forecasts
_FEAT = None


def feat_nq():
    global _FEAT
    if _FEAT is None:
        f = pd.read_parquet(os.path.join(CONF, "v4", "out", "feat_NQ.parquet"), columns=["ts", "sigma", "rv_60", "rv_240"])
        f.index = pd.DatetimeIndex(f.pop("ts")).as_unit("ns")
        assert f.index.is_unique
        _FEAT = f
    return _FEAT


def v4_s(t, col):
    """sigma x rv_{col} at the last 5-minute mark <= entry (v4 feature, causal)."""
    f = feat_nq()
    mark = pd.DatetimeIndex(t.t_entry).floor("5min")
    x = f.reindex(mark.to_numpy().astype("datetime64[ns]"))
    return (x.sigma * x[col]).to_numpy()


_HAR = None


def har_s(t):
    """sqrt(HAR-log daily RV forecast x 09:30-16:00 share) of the trade's session and market (A3)."""
    global _HAR
    if _HAR is None:
        _HAR = pd.concat([pd.read_parquet(os.path.join(OUT, f"_sess_har_{s}.parquet")) for s in ("ES", "NQ", "YM")])
        _HAR["s"] = np.sqrt(np.maximum(_HAR.har_log_d, 0) * _HAR.share)
        _HAR["session"] = pd.DatetimeIndex(_HAR.session).as_unit("ns")
        _HAR = _HAR.set_index(["market", "session"])["s"]
    k = pd.MultiIndex.from_arrays([t.market.to_numpy(), pd.DatetimeIndex(t.session).normalize().as_unit("ns")])
    return _HAR.reindex(k).to_numpy()


def add_s(t):
    t = t.copy()
    s = np.full(len(t), np.nan)
    for rule, col in (("A1", "rv_60"), ("A4", "rv_240")):
        m = (t.rule == rule).to_numpy()
        if m.any():
            s[m] = v4_s(t[m], col)
    m = (t.rule == "A3").to_numpy()
    if m.any():
        s[m] = har_s(t[m])
    s[~(s > 0)] = np.nan
    t["s"] = s
    t["s_usd"] = s * t.entry_px.to_numpy(float) * t.market.map(PV).to_numpy(float)
    return t


# =========================================================================================== policies
def ratios(t):
    """Pre-rounding size multipliers r (n = round(n0 * r)) for every vol policy; t sorted by t_entry.
    Expanding statistics over PRIOR trades of the same (rule, market); EV fit over prior EXITED trades of the rule."""
    n = len(t)
    R = {p: np.ones(n) for p in VOLPOL}
    s = t.s.to_numpy(float)
    su = t.s_usd.to_numpy(float)
    pnl = t.pnl_usd.to_numpy(float)
    te = t.t_entry.to_numpy("datetime64[ns]")
    tx = t.t_exit.to_numpy("datetime64[ns]")
    rule = t.rule.to_numpy()
    mkt = t.market.to_numpy()
    for (ru, mk) in sorted(set(zip(rule, mkt))):
        idx = np.flatnonzero((rule == ru) & (mkt == mk))
        hist = []
        for i in idx:
            si = s[i]
            if np.isfinite(si) and len(hist) >= MIN_HIST:
                h = np.asarray(hist)
                mb = h.mean()
                q20, q80 = np.quantile(h, [0.2, 0.8])
                R["VT"][i] = mb / si
                R["CVT"][i] = min(mb / si, 2.0) if (si >= q80 or si <= q20) else 1.0
                R["CVTDN"][i] = min(mb / si, 1.0) if si >= q80 else 1.0
                R["IV"][i] = mb / (np.mean(1.0 / h) * si * si)
            if np.isfinite(si):
                hist.append(si)
    # EV: muhat = a + b * s_usd, fitted on prior exited trades of the same rule (markets pooled)
    for ru in sorted(set(rule)):
        idx = np.flatnonzero(rule == ru)
        for i in idx:
            if not np.isfinite(su[i]):
                continue
            P = idx[(tx[idx] <= te[i]) & np.isfinite(su[idx])]
            Q = P[mkt[P] == mkt[i]]
            if len(P) < MIN_EV or len(Q) < MIN_HIST:
                continue
            x, y = su[P], pnl[P]
            xm = x.mean()
            b = ((x - xm) * (y - y.mean())).sum() / ((x - xm) ** 2).sum()
            a = y.mean() - b * xm
            mu_i = max(a + b * su[i], 0.0)
            xq = su[Q]
            den = np.mean(np.maximum(a + b * xq, 0.0) / xq)
            R["EV"][i] = 0.0 if den <= 0 else (mu_i / su[i] ** 2) * xq.mean() / den
    return R


def wants(t, R, levels, budgets):
    """dict (policy, level) -> wanted micros array."""
    W = {}
    for n0 in levels:
        W[("FIXED", n0)] = np.full(len(t), n0, np.int64)
        for p in VOLPOL:
            W[(p, n0)] = np.clip(np.floor(n0 * R[p] + 0.5), 0, NMAX).astype(np.int64)
    risk = t.risk_usd.to_numpy(float)
    for B in budgets:
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.floor(B / risk + 1e-9)
        W[("FIXRISK", B)] = np.where(np.isfinite(q) & (risk > 0), q, 0).astype(np.int64)
    return W


# =========================================================================================== sizing + eval
def size_loop(te, tx, day, want):
    """eval_sim.size_trades loop with a wanted-micros array (20 open-micro cap, $600 realized-loss stop)."""
    import heapq
    n = len(te)
    micros = np.zeros(n, np.int64)
    heap, realized, open_m = [], {}, 0
    pnl = size_loop.pnl
    for k in range(n):
        now = te[k]
        while heap and heap[0][0] <= now:
            _, m, p, dy = heapq.heappop(heap)
            open_m -= m
            realized[dy] = realized.get(dy, 0.0) + p
        if realized.get(day[k], 0.0) <= -DLL:
            continue
        w = want[k]
        if w <= 0:
            continue
        m = min(w, NMAX - open_m)
        if m <= 0:
            continue
        micros[k] = m
        open_m += m
        heapq.heappush(heap, (tx[k], m, m * pnl[k], day[k]))
    return micros


def stream_arrays(t):
    t = E.prepare(t)
    te = t.t_entry.to_numpy("datetime64[ns]").view(np.int64).tolist()
    tx = t.t_exit.to_numpy("datetime64[ns]").view(np.int64).tolist()
    day = t.session.to_numpy("datetime64[ns]").view(np.int64).tolist()
    ci = np.array([CALPOS[d] for d in day])
    return t, te, tx, day, ci


def daily_from(ci, micros, pnl):
    v = np.bincount(ci, weights=micros * pnl, minlength=NCAL)
    return np.maximum(v, -DLL)


def eval_v(v, keep=False):
    """Aggregates per (consistency, window) + optionally per-start arrays (2018+ starts)."""
    rows, per = [], {}
    left = NCAL - SIDX
    for c in CONS:
        o, d = ps.run_starts(v, SIDX, replace(E.RULES, consistency=c))
        if keep:
            per[c] = (o, d)
        for w, wm in WMASK.items():
            sel = wm[SIDX]
            oo, dd, lf = o[sel], d[sel], left[sel]
            ns = len(oo)
            pas, fail = oo == ps.OUT_PASS, oo == ps.OUT_FAIL
            dp = dd[pas]
            r = dict(consistency=c, window=w, n_starts=ns, pass_pct=100 * pas.mean(), bust_pct=100 * fail.mean(),
                     open_pct=100 * (1 - pas.mean() - fail.mean()),
                     days_pass_median=float(np.median(dp)) if len(dp) else np.nan)
            for N in (5, 10, 20):
                ok = lf >= N
                r[f"within_{N}"] = 100 * (pas[ok] & (dd[ok] <= N)).mean()
            x = v[wm]
            sd = x.std(ddof=1)
            cum = np.cumsum(x)
            r.update(worst_day=float(x.min()), sd_day=float(sd), usd_day=float(x.mean()),
                     sharpe_d=float(x.mean() / sd) if sd > 0 else np.nan,
                     sharpe_ann=float(x.mean() / sd * np.sqrt(252)) if sd > 0 else np.nan,
                     maxdd=float((np.maximum.accumulate(np.r_[0.0, cum]) - np.r_[0.0, cum]).max()))
            rows.append(r)
    return rows, per


def run_stream(t, levels, budgets, keep=False):
    """All policies on one trade stream. Returns (DataFrame rows, per-start dict)."""
    t = add_s(t) if "s" not in t.columns else t
    t = t.sort_values(["t_entry", "market"], kind="stable").reset_index(drop=True)
    R = ratios(t)
    W = wants(t, R, levels, budgets)
    tt, te, tx, day, ci = stream_arrays(t)
    # prepare() sorts by (t_entry, original order) - t is already in that order
    assert (tt.index.to_numpy() == np.arange(len(t))).all()
    pnl = tt.pnl_usd.to_numpy(float)
    size_loop.pnl = pnl.tolist()
    s = tt.s.to_numpy(float)
    rows, PER = [], {}
    for (pol, lv), w in W.items():
        mic = size_loop(te, tx, day, w.tolist())
        v = daily_from(ci, mic, pnl)
        rr, per = eval_v(v, keep)
        tk = mic > 0
        ok = np.isfinite(s)
        risk_ratio = float((w[ok] * s[ok]).mean() / (lv * s[ok].mean())) if pol != "FIXRISK" else np.nan
        for r in rr:
            r.update(policy=pol, level=lv, trades_taken=int(tk.sum()), micros_mean=float(mic[tk].mean()) if tk.any() else 0.0,
                     want_risk_ratio=risk_ratio, skipped_size0=int((w <= 0).sum()))
            rows.append(r)
        if keep:
            PER[(pol, lv)] = per
    return rows, PER


# =========================================================================================== data
def load_real_risk(h):
    """v3 synth_p1 load_real: virtual risk_usd = sd of the component's previous 100 per-micro net $ (from 2010)."""
    t = pd.read_parquet(os.path.join(V3, "out", "trades", f"{h}.parquet"))
    t = t[pd.DatetimeIndex(t.session) <= END].copy()
    if "tid" not in t.columns:
        t["tid"] = np.arange(len(t))
    t = t.sort_values(["t_entry", "market"], kind="stable").reset_index(drop=True)
    t["risk_usd"] = t["pnl_usd"].shift(1).rolling(100, min_periods=100).std()
    t["rule"] = h
    return t


def real_trades():
    tv = pd.read_parquet(os.path.join(OUT, "trades_vol.parquet"))
    tv = tv[(tv.session >= FIRST) & (tv.session <= END)].copy()
    for c in ("t_entry", "t_exit", "session"):
        tv[c] = pd.DatetimeIndex(tv[c]).as_unit("ns")
    rk = pd.concat([load_real_risk(h)[["rule", "market", "t_entry", "risk_usd", "tid"]] for h in ("A1", "A3", "A4")])
    rk["t_entry"] = pd.DatetimeIndex(rk.t_entry).as_unit("ns")
    assert not rk.duplicated(["rule", "market", "t_entry"]).any()
    t = tv.merge(rk, on=["rule", "market", "t_entry"], how="left", validate="1:1")
    assert t.risk_usd.notna().all(), "real trade without risk_usd"
    keep = ["rule", "market", "session", "t_entry", "t_exit", "d", "entry_px", "pnl_usd", "risk_usd",
            "sigma", "rv_60", "rv_240", "har_log_d", "share"]
    return t[keep].copy()


def twins():
    """C1 twins rep < NT, sessions 2018-01-01 .. END, each with the real trade's risk_usd (v3 convention)."""
    out = []
    # A1
    t = pd.read_parquet(os.path.join(V3, "exp_g1_noiseband", "cache", "twins_A1.parquet"),
                        columns=["market", "session", "t_entry", "t_exit", "d", "entry", "exit", "tid", "entry_px",
                                 "pnl_usd", "rep"])
    base = pd.read_parquet(os.path.join(V3, "out", "trades", "A1.parquet"))
    base = base[pd.DatetimeIndex(base.session) <= END].reset_index(drop=True)
    chk = t[t.rep == 0].merge(base[["entry", "exit", "d"]].reset_index().rename(columns={"index": "tid"}), on="tid",
                              suffixes=("", "_b"))
    assert (chk.entry.astype(str) == chk.entry_b.astype(str)).all() and (chk.d == chk.d_b).all(), "A1 tid mismatch"
    r1 = load_real_risk("A1")[["t_entry", "risk_usd"]].drop_duplicates("t_entry")
    key = base.reset_index().rename(columns={"index": "tid"})[["tid", "t_entry"]].merge(r1, on="t_entry", how="left")
    t = t.merge(key[["tid", "risk_usd"]], on="tid", how="left")
    t["rule"] = "A1"
    out.append(t)
    # A3
    r3 = load_real_risk("A3")[["market", "tid", "risk_usd", "d"]].rename(columns={"d": "d_real"})
    for s in ("ES", "NQ", "YM"):
        c = pd.read_parquet(os.path.join(V3, "exp_g3_expiry", "cache", f"c1_A3_{s}_999.parquet"))
        c = c[c.rep < NT].drop(columns=["risk_usd"]).copy()
        c["market"] = s
        c = c.merge(r3, on=["market", "tid"], how="left")
        assert (c.d == c.d_real).all(), "A3 twin side mismatch"
        c["rule"] = "A3"
        out.append(c)
    # A4 (v3 synth_p1 procedure)
    import g4lib as G
    S = H.sessions("NQ")
    ent = G.release_fade()(S, {})
    ent = ent[pd.DatetimeIndex(ent.session) <= G.END].reset_index(drop=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        L = G.run_leg("NQ", ent, 4, R=NT, nrep_ctrl=2)
    r4 = load_real_risk("A4")
    assert len(L["trades"]) == len(r4)
    c = L["c1"].drop(columns=["risk_usd"]).merge(r4[["tid", "risk_usd", "d"]].rename(columns={"d": "d_real"}),
                                                  on="tid", how="left")
    assert (c.d == c.d_real).all(), "A4 twin side mismatch"
    c["rule"] = "A4"
    out.append(c)
    cols = ["rule", "market", "session", "t_entry", "t_exit", "d", "entry_px", "pnl_usd", "risk_usd", "rep"]
    tw = pd.concat([x[cols] for x in out], ignore_index=True)
    tw["session"] = pd.DatetimeIndex(tw.session).normalize()
    tw = tw[(tw.session >= FIRST) & (tw.session <= END) & (tw.rep < NT)].reset_index(drop=True)
    return tw


# =========================================================================================== workers
_TW = None


def _init(tw):
    global _TW
    _TW = tw


def _twin_job(r):
    x = _TW[_TW.rep == r]
    rows = []
    for name, sub in (("P1", x), ("A1", x[x.rule == "A1"])):
        rr, _ = run_stream(sub.drop(columns="rep"), LEVELS_TWIN, B_TWIN)
        for q in rr:
            q.update(portfolio=name, rep=r)
        rows += rr
    return rows


# =========================================================================================== stats
def sb_index(n, B, L, rng):
    """Stationary bootstrap (Politis & Romano 1994) index matrix (B, n), mean block L, circular."""
    idx = np.empty((B, n), np.int64)
    idx[:, 0] = rng.integers(0, n, B)
    new = rng.random((B, n)) < 1.0 / L
    fresh = rng.integers(0, n, (B, n))
    for j in range(1, n):
        idx[:, j] = np.where(new[:, j], fresh[:, j], (idx[:, j - 1] + 1) % n)
    return idx


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(o):
        run = max(run, (m - k) * p[i])
        adj[i] = min(1.0, run)
    return adj


def diagnostic(t):
    """2018-2021: per rule, 1-micro net $ by forecast quintile (within rule x market) + OLS slope of $ on s_usd."""
    t = t[t.session <= "2021-12-31"].copy()
    t = t[np.isfinite(t.s)]
    rows = []
    for ru, g in t.groupby("rule"):
        q = g.groupby("market")["s"].transform(lambda z: pd.qcut(z.rank(method="first"), 5, labels=False))
        for k in range(5):
            m = q == k
            rows.append(dict(rule=ru, bucket=f"Q{k + 1}", n=int(m.sum()), usd_trade=g.pnl_usd[m].mean(),
                             usd_per_sd=(g.pnl_usd[m] / g.s_usd[m]).mean(), s_usd_mean=g.s_usd[m].mean()))
        x, y = g.s_usd.to_numpy(), g.pnl_usd.to_numpy()
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        V = XtXi @ (X.T * e ** 2) @ X @ XtXi                         # White (1980) HC0
        z = g.pnl_usd / g.s_usd
        zx = np.column_stack([np.ones(len(x)), x])
        bz, *_ = np.linalg.lstsq(zx, z.to_numpy(), rcond=None)
        ez = z.to_numpy() - zx @ bz
        Vz = XtXi @ (zx.T * ez ** 2) @ zx @ XtXi
        rows.append(dict(rule=ru, bucket="OLS $ on s_usd", n=len(x), slope=beta[1], t_slope=beta[1] / np.sqrt(V[1, 1]),
                         slope_sharpe=bz[1], t_slope_sharpe=bz[1] / np.sqrt(Vz[1, 1])))
    return pd.DataFrame(rows)


# =========================================================================================== main
def main():
    t0 = time.time()
    checks = []
    real = add_s(real_trades())
    # check: v4 forecasts recomputed from feat files equal trades_vol's (A1: sigma*rv_60, A4: sigma*rv_240)
    for ru, col in (("A1", "rv_60"), ("A4", "rv_240")):
        m = real.rule == ru
        ok = np.isclose(real.s[m], real.sigma[m] * real[col][m], rtol=1e-9, equal_nan=True).mean()
        checks.append(f"{ru} s from feat file == trades_vol sigma*{col}: {ok:.4f}")
    m = real.rule == "A3"
    ok = np.isclose(real.s[m], np.sqrt(real.har_log_d[m] * real.share[m]), rtol=1e-9, equal_nan=True).mean()
    checks.append(f"A3 s from _sess_har == trades_vol sqrt(har_log_d*share): {ok:.4f}; s NaN by rule: "
                  f"{real.groupby('rule').s.apply(lambda z: int(z.isna().sum())).to_dict()}")
    diag = diagnostic(real)
    diag.to_csv(os.path.join(OUT, "sizing_diag.csv"), index=False)
    # check: size_loop == eval_sim.size_trades for FIXED and FIXRISK
    tr = real.sort_values(["t_entry", "market"], kind="stable").reset_index(drop=True)
    tt, te, tx, day, ci = stream_arrays(tr)
    size_loop.pnl = tt.pnl_usd.tolist()
    for pol in (("fixed", 3), ("fixed", 10), ("risk", 250)):
        ref = E.size_trades(tt, pol, max_micros=NMAX, dll=DLL, checked=True)
        w = np.full(len(tt), pol[1]) if pol[0] == "fixed" else np.where(
            tt.risk_usd > 0, np.floor(pol[1] / tt.risk_usd + 1e-9), 0).astype(np.int64)
        mic = size_loop(te, tx, day, w.tolist())
        same = (mic == ref.micros.to_numpy()).all()
        v = daily_from(ci, mic, tt.pnl_usd.to_numpy(float))
        e_ref = E.eval_daily(E.daily_pnl(ref, CAL, DLL), CONS, WINDOWS)
        mine = pd.DataFrame(eval_v(v)[0])
        dif = np.nanmax(np.abs(e_ref[["pass_pct", "within_10", "within_20"]].to_numpy()
                               - mine[["pass_pct", "within_10", "within_20"]].to_numpy()))
        checks.append(f"size_loop vs eval_sim {pol}: micros identical={same}, max |eval diff|={dif:.2e}")
        assert same and dif < 1e-9
    print("\n".join(checks), flush=True)

    # real streams
    allrows, PER = [], {}
    for name, sub in (("P1", real), ("A1", real[real.rule == "A1"])):
        rr, per = run_stream(sub, LEVELS_REAL, B_REAL, keep=True)
        for q in rr:
            q["portfolio"] = name
        allrows += rr
        PER[name] = per
    realdf = pd.DataFrame(allrows)
    realdf.to_csv(os.path.join(OUT, "sizing_real.csv"), index=False)
    print("real done", round(time.time() - t0, 1), "s", flush=True)

    # twins
    tw = twins()
    tw = add_s(tw)
    checks.append(f"twins: {len(tw)} trades, reps {tw.rep.nunique()}, by rule {tw.groupby('rule').size().to_dict()}, "
                  f"s NaN share by rule {tw.groupby('rule').s.apply(lambda z: round(float(z.isna().mean()), 4)).to_dict()}, "
                  f"risk NaN {int(tw.risk_usd.isna().sum())}")
    print(checks[-1], flush=True)
    rows = []
    with Pool(NW, initializer=_init, initargs=(tw,)) as pool:
        for k, rr in enumerate(pool.imap_unordered(_twin_job, range(NT))):
            rows += rr
            if k % 20 == 0:
                print("twin", k, round(time.time() - t0, 1), "s", flush=True)
    twdf = pd.DataFrame(rows)
    twdf.to_csv(os.path.join(OUT, "sizing_twins.csv"), index=False)
    print("twins done", round(time.time() - t0, 1), "s", flush=True)

    # tests: paired difference vs FIXED at the same level, per-start bootstrap + twin rank p
    rng = np.random.default_rng(20261109)
    nS = len(SIDX)
    left = NCAL - SIDX
    BOOT = {L: sb_index(nS, 2000, L, rng) for L in (20, 60)}
    tests = []
    for port in ("P1", "A1"):
        for c in CONS:
            for wname in WINDOWS:
                sel = WMASK[wname][SIDX]
                for lv in LEVELS_TWIN:
                    of, df_ = PER[port][("FIXED", lv)][c]
                    for pol in VOLPOL:
                        op, dp_ = PER[port][(pol, lv)][c]
                        for met in ("pass_pct", "within_20", "bust_pct"):
                            if met == "pass_pct":
                                xa, xb, el = (op == ps.OUT_PASS), (of == ps.OUT_PASS), sel
                            elif met == "bust_pct":
                                xa, xb, el = (op == ps.OUT_FAIL), (of == ps.OUT_FAIL), sel
                            else:
                                xa = (op == ps.OUT_PASS) & (dp_ <= 20)
                                xb = (of == ps.OUT_PASS) & (df_ <= 20)
                                el = sel & (left >= 20)
                            D = 100 * (xa.astype(float) - xb.astype(float))
                            D = np.where(el, D, 0.0)
                            nel = el.astype(float)
                            dbar = D.sum() / nel.sum()
                            pb, ci = [], None
                            for L, I in BOOT.items():
                                bm = D[I].sum(1) / np.maximum(nel[I].sum(1), 1)
                                if met == "bust_pct":
                                    pb.append(float((1 + ((bm - dbar) <= -dbar).sum()) / (1 + len(bm))))   # H0 D >= 0
                                else:
                                    pb.append(float((1 + ((bm - dbar) >= dbar).sum()) / (1 + len(bm))))
                                lo, hi = np.percentile(bm, [2.5, 97.5])
                                ci = (min(ci[0], lo), max(ci[1], hi)) if ci else (lo, hi)
                            g = twdf[(twdf.portfolio == port) & (twdf.consistency == c) & (twdf.window == wname)
                                     & (twdf.level == lv)]
                            gp = g[g.policy == pol].set_index("rep")[met]
                            gf = g[g.policy == "FIXED"].set_index("rep")[met]
                            dt = (gp - gf).dropna()
                            if met == "bust_pct":
                                ptw = float((1 + (dt <= dbar).sum()) / (1 + len(dt)))
                            else:
                                ptw = float((1 + (dt >= dbar).sum()) / (1 + len(dt)))
                            tests.append(dict(portfolio=port, consistency=c, window=wname, level=lv, policy=pol,
                                              metric=met, diff_real=dbar, ci_lo=ci[0], ci_hi=ci[1], p_boot=max(pb),
                                              diff_twin_mean=float(dt.mean()), diff_twin_p95=float(dt.quantile(0.95)),
                                              diff_twin_p05=float(dt.quantile(0.05)), p_twin=ptw,
                                              excess_vs_twins=dbar - float(dt.mean())))
    tests = pd.DataFrame(tests)
    prim = (tests.portfolio == "P1") & (tests.consistency == 0.40) & (tests.window == "2018+") & \
        tests.level.isin([3, 5]) & tests.metric.isin(["pass_pct", "within_20"])
    tests["primary"] = prim
    tests["p_holm"] = np.nan
    tests.loc[prim, "p_holm"] = holm(tests.loc[prim, "p_boot"].to_numpy())
    tests.to_csv(os.path.join(OUT, "sizing_tests.csv"), index=False)
    np.savez_compressed(os.path.join(OUT, "_sizing_perstart.npz"),
                        **{f"{p}|{pol}|{lv}|{c}|{k}": arr for p in PER for (pol, lv), per in PER[p].items()
                           for c, (o, d) in per.items() for k, arr in (("out", o), ("days", d))})
    with open(os.path.join(OUT, "sizing_checks.txt"), "w") as fh:
        fh.write("\n".join(checks) + "\n")
    print("all done", round(time.time() - t0, 1), "s", flush=True)


if __name__ == "__main__":
    main()
