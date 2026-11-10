"""v4 raw-statistics feature dataset (pure market statistics, no hand-made indicators).

Sample point t = every 5-minute mark 18:05..16:40 ET of a Globex session (18:00-17:00, session_label).
Features use ONLY 1-minute bars that closed by t (bar start < t), same session and contract.
Targets start at the open of the minute that starts at t and end by 16:45.

Grid: per session a (S, 1380) matrix of minutes 18:00..16:59 (k = minutes since 18:00).  Boundary price
B[k] = price at clock time 18:00+k = close of the last bar that closed by then (forward-filled inside the session);
B[k_first] = open of the session's first bar.  1-minute log returns r[k] = log B[k+1] - log B[k] (0 for a minute
without trades).  sigma = population std of r over the previous 5 sessions (bars up to 16:44).

Contracts: one row per minute (front contract by volume).  In the ~31 sessions where the contract switches inside
the session (always at 19:00/20:00 ET), the bars of the old contract are dropped (known at t: the current bar's
contract), and in every roll session (switch inside it, or contract differs from the previous session) the samples
before first-bar + 60 min are dropped.

Usage (from research/confidence, heavy -> under the heavy.lock flock):
  python3 v4/features.py build ES     -> out/_own_ES.parquet + truncation test
  python3 v4/features.py cross        -> out/feat_{ES,NQ,YM}.parquet (adds the other markets' 15/60-min returns)
"""
import os
import sys
import time

import numpy as np
import pandas as pd

import research_lib as rl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
NK = 1380                        # minutes 18:00..16:59
K1645 = 1365                     # boundary index of 16:45
K0930 = 930                      # boundary index of 09:30
KS = np.arange(5, 1361, 5)       # sample boundaries 18:05..16:40 (272)
MULT = {"ES": 5.0, "NQ": 2.0, "YM": 0.5}         # $ per point per micro (MES, MNQ, MYM)
COST = {"ES": 3.50, "NQ": 2.00, "YM": 2.00}      # $ per micro round trip (+1 tick on stop fills)
TICK = {"ES": 0.25, "NQ": 0.25, "YM": 1.0}
FIRST, LAST = pd.Timestamp("2018-01-01"), pd.Timestamp("2025-06-27")    # session labels kept
LOAD_FROM = pd.Timestamp("2017-10-01")                                   # warm-up for sigma / volume baselines
CONF_START = pd.Timestamp("2022-01-01")
HOLDOUT_SESSION_START = pd.Timestamp("2025-06-30 18:00")
RET_N = (1, 5, 15, 30, 60, 120, 240)
WIN = (15, 60, 240)
VOL_W = (5, 15, 60)
FWD = (5, 15, 60)


def load(sym):
    m = rl.bars_1m(sym)
    keep = ((m.sess >= LOAD_FROM) & (m.sess <= LAST)).to_numpy()
    m = m[keep]
    d = pd.DataFrame({"O": m.Open.to_numpy(np.float64), "H": m.High.to_numpy(np.float64),
                      "L": m.Low.to_numpy(np.float64), "C": m.Close.to_numpy(np.float64),
                      "V": m.Volume.to_numpy(np.float64), "inst": m.instrument_id.to_numpy(),
                      "sess": m.sess.to_numpy()}, index=m.index.tz_localize(None))
    del m
    assert d.index.max() < HOLDOUT_SESSION_START, "holdout data loaded"
    return d


def _cs(x):
    """cumulative sum along minutes with a leading 0: window sum of minutes [a, b) = cs[:, b] - cs[:, a]."""
    return np.concatenate([np.zeros((x.shape[0], 1)), np.cumsum(x, axis=1)], axis=1)


def _wsum(cs, w):
    out = cs[:, KS] - cs[:, np.clip(KS - w, 0, None)]
    out[:, KS < w] = np.nan
    return out


def _roll(a, w, how):
    """rolling max/min over the last w minutes ending at each minute (NaN = no bar, skipped)."""
    r = pd.DataFrame(a.T).rolling(w, min_periods=1)
    return (r.max() if how == "max" else r.min()).to_numpy().T


def build(d, sym):
    """Feature + target rows for every session in d (a load() frame, possibly truncated)."""
    mod = (d.index.hour * 60 + d.index.minute).to_numpy()
    k = (mod - 1080) % 1440
    d = d[k < NK]
    k = k[k < NK]
    g = d.groupby("sess", sort=True)
    multi = (g.inst.transform("nunique") > 1).to_numpy()
    last_inst = g.inst.transform("last").to_numpy()
    keep = d.inst.to_numpy() == last_inst            # current contract = latest bar's contract
    d, k, multi = d[keep], k[keep], multi[keep]
    sessions, si = np.unique(d.sess.to_numpy(), return_inverse=True)
    S = len(sessions)
    rows = np.arange(S)

    def grid(col, fill=np.nan):
        a = np.full((S, NK), fill)
        a[si, k] = d[col].to_numpy()
        return a

    O, H, L, C = grid("O"), grid("H"), grid("L"), grid("C")
    V = grid("V", 0.0)
    has = ~np.isnan(C)
    sess_inst = pd.Series(d.inst.to_numpy()).groupby(si).last().to_numpy()
    multi_s = pd.Series(multi).groupby(si).any().to_numpy()
    roll = multi_s | np.r_[False, sess_inst[1:] != sess_inst[:-1]]
    kfirst = np.argmax(has, axis=1)

    # forward-filled close and boundary prices
    idx = np.maximum.accumulate(np.where(has, np.arange(NK), 0), axis=1)
    Cff = C[rows[:, None], idx]
    B = np.full((S, NK + 1), np.nan)
    B[:, 1:] = Cff
    B[rows, kfirst] = O[rows, kfirst]
    lB = np.log(B)
    r = np.diff(lB, axis=1)
    r0 = np.nan_to_num(r)
    live = ~np.isnan(r)

    # sigma: previous 5 sessions' 1-minute returns (bars up to 16:44)
    agg = pd.DataFrame({"n": live[:, :K1645].sum(1), "s1": r0[:, :K1645].sum(1),
                        "s2": (r0[:, :K1645] ** 2).sum(1)}).rolling(5, min_periods=5).sum().shift(1)
    sig = np.sqrt(agg.s2 / agg.n - (agg.s1 / agg.n) ** 2).to_numpy()[:, None]

    F = {}
    lBt = lB[:, KS]
    valid = lambda w: (KS >= w) & True       # noqa: E731
    for n in RET_N:
        x = lBt - lB[:, np.clip(KS - n, 0, None)]
        x[:, KS < n] = np.nan
        F[f"ret_{n}"] = x
        F[f"ret_{n}_z"] = x / sig
    x = lBt - lB[rows, kfirst][:, None]
    F["ret_sess"], F["ret_sess_z"] = x, x / sig
    x = lBt - lB[:, [K0930]]
    x[:, KS <= K0930] = np.nan
    F["ret_0930"], F["ret_0930_z"] = x, x / sig
    last_c = Cff[:, -1]
    prev = np.r_[np.nan, (np.log(last_c) - lB[rows, kfirst])[:-1]][:, None] * np.ones((1, len(KS)))
    F["ret_prev"], F["ret_prev_z"] = prev, prev / sig

    start_ok = {w: ~np.isnan(lB[:, np.clip(KS - w, 0, None)]) & valid(w)[None, :] for w in (15, 30, 60, 240)}

    # realized vol, range, position in range
    c1, c2 = _cs(r0), _cs(r0 ** 2)
    ct = B[:, KS]
    for w in WIN:
        s1, s2 = _wsum(c1, w), _wsum(c2, w)
        rv = np.sqrt(np.maximum(s2 / w - (s1 / w) ** 2, 0)) / sig
        rv[~start_ok[w]] = np.nan
        F[f"rv_{w}"] = rv
        hi = _roll(H, w, "max")[:, KS - 1]
        lo = _roll(L, w, "min")[:, KS - 1]
        bad = ~start_ok[w]
        hi[bad], lo[bad] = np.nan, np.nan
        F[f"rng_{w}"] = np.log(hi / lo)
        F[f"rng_{w}_z"] = F[f"rng_{w}"] / sig
        with np.errstate(invalid="ignore", divide="ignore"):
            F[f"pos_{w}"] = np.where(hi > lo, (ct - lo) / (hi - lo), np.nan)

    # session high / low so far, VWAP
    sh = np.fmax.accumulate(H, axis=1)[:, KS - 1]
    sl = np.fmin.accumulate(L, axis=1)[:, KS - 1]
    F["dist_shi_z"] = np.log(sh / ct) / sig
    F["dist_slo_z"] = np.log(ct / sl) / sig
    with np.errstate(invalid="ignore", divide="ignore"):
        F["pos_sess"] = np.where(sh > sl, (ct - sl) / (sh - sl), np.nan)
    tp = np.nan_to_num((H + L + C) / 3.0)
    cv, cpv = _cs(V), _cs(tp * V)
    with np.errstate(invalid="ignore", divide="ignore"):
        vwap = np.where(cv[:, KS] > 0, cpv[:, KS] / cv[:, KS], np.nan)
    F["dist_vwap_z"] = np.log(ct / vwap) / sig

    # volume relative to the same clock time over the previous 20 sessions
    for w in VOL_W:
        x = _wsum(cv, w)
        xb = x.copy()
        xb[roll[:, None] & (KS[None, :] - w < kfirst[:, None])] = np.nan   # windows touching dropped bars
        base = pd.DataFrame(xb).rolling(20, min_periods=15).mean().shift(1).to_numpy()
        with np.errstate(invalid="ignore", divide="ignore"):
            F[f"relvol_{w}"] = np.where(base > 0, x / base, np.nan)

    # signed-volume imbalance, up-minute share, lag-1 autocorrelation
    csv_ = _cs(V * np.sign(r0))
    for w in (15, 60):
        with np.errstate(invalid="ignore", divide="ignore"):
            vw = _wsum(cv, w)
            F[f"imb_{w}"] = np.where(vw > 0, _wsum(csv_, w) / vw, np.nan)
    nup, ndn = _wsum(_cs((r0 > 0) * 1.0), 30), _wsum(_cs((r0 < 0) * 1.0), 30)
    with np.errstate(invalid="ignore", divide="ignore"):
        F["upshare_30"] = np.where(nup + ndn > 0, nup / (nup + ndn), np.nan)
    F["upshare_30"][~start_ok[30]] = np.nan
    x, y = r0[:, :-1], r0[:, 1:]                       # pair p = (r[p], r[p+1])
    cs = {n: _cs(a) for n, a in dict(x=x, y=y, xx=x * x, yy=y * y, xy=x * y).items()}
    lo_i, hi_i = np.clip(KS - 60, 0, None), np.clip(KS - 1, 0, None)   # pairs p in [kt-60, kt-2]
    Sm = {n: c[:, hi_i] - c[:, lo_i] for n, c in cs.items()}
    n = 59.0
    with np.errstate(invalid="ignore", divide="ignore"):
        cov = Sm["xy"] - Sm["x"] * Sm["y"] / n
        den = np.sqrt((Sm["xx"] - Sm["x"] ** 2 / n) * (Sm["yy"] - Sm["y"] ** 2 / n))
        ac = np.where(den > 1e-300, cov / den, np.nan)
    ac[~start_ok[60]] = np.nan
    F["ac1_60"] = ac

    # path shape: last 60 one-minute closes (log), z-normalised, averaged into 12 points of 5
    shp = np.full((S, len(KS), 12), np.nan)
    sel = np.nonzero(KS >= 60)[0]
    P = lB[:, KS[sel][:, None] + np.arange(-59, 1)[None, :]]       # B[kt-59..kt] = closes of bars kt-60..kt-1
    mu, sd = P.mean(2, keepdims=True), P.std(2, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        z = np.where(sd > 0, (P - mu) / sd, np.nan)
    shp[:, sel, :] = z.reshape(S, len(sel), 12, 5).mean(3)
    for j in range(12):
        F[f"shape_{j:02d}"] = shp[:, :, j]
    del P, z

    # targets: entry = open of the minute starting at t (else the last price), exits by 16:45
    T = {}
    ot = O[:, np.minimum(KS, NK - 1)]
    entry = np.where(np.isnan(ot), ct, ot)
    T["entry"] = entry
    for h in FWD + ("eod",):
        kk = np.full(len(KS), K1645) if h == "eod" else KS + h
        ex = B[:, np.minimum(kk, NK)]
        ex[:, kk > K1645] = np.nan
        T[f"fwd_{h}"] = np.log(ex / entry)
        T[f"fwd_{h}_z"] = T[f"fwd_{h}"] / sig
        T[f"fwd_{h}_usd"] = (ex - entry) * MULT[sym]
    for h in (15, 60):
        hi = _roll(H, h, "max")[:, np.minimum(KS + h - 1, NK - 1)]
        lo = _roll(L, h, "min")[:, np.minimum(KS + h - 1, NK - 1)]
        x = np.log(hi / lo) / sig
        x[:, KS + h > K1645] = np.nan
        T[f"frng_{h}_z"] = x

    # assemble rows
    sess_rep = np.repeat(sessions, len(KS))
    kt_rep = np.tile(KS, S)
    ts = pd.DatetimeIndex(sess_rep) - pd.Timedelta(hours=6) + pd.to_timedelta(kt_rep, unit="min")
    out = pd.DataFrame({"ts": ts, "sess": sess_rep, "sym": sym,
                        "clock_min": ((kt_rep + 1080) % 1440).astype(np.int16),
                        "weekday": pd.DatetimeIndex(sess_rep).day_of_week.astype(np.int8),
                        "roll": np.repeat(roll, len(KS)), "sigma": np.repeat(sig[:, 0], len(KS)),
                        "price": ct.ravel()})
    for name, a in F.items():
        out[name] = a.ravel().astype(np.float32 if name.startswith(("shape", "rel", "imb", "up", "ac", "pos"))
                                     else np.float64)
    for name, a in T.items():
        out[name] = a.ravel()
    out["cost_rt_usd"] = COST[sym]
    drop = np.isnan(ct.ravel()) | np.isnan(out.sigma.to_numpy())
    drop |= np.repeat(roll, len(KS)) & (kt_rep < np.repeat(kfirst, len(KS)) + 60)
    return out[~drop].reset_index(drop=True)


FEAT_EXCLUDE = {"ts", "sess", "sym", "clock_min", "weekday", "roll", "cost_rt_usd", "entry"}


def feature_cols(df):
    return [c for c in df.columns if c not in FEAT_EXCLUDE and not c.startswith(("fwd_", "frng_"))]


def truncation_test(d, full, n=30, seed=0):
    """Rebuild from bars that closed strictly before t (the session's 30 prior sessions + the bars of t's session
    before t, nothing later) and require identical features at t."""
    rng = np.random.default_rng(seed)
    cand = full[full.sess >= FIRST]
    pick = np.r_[rng.choice(len(cand), n - 5, replace=False),
                 rng.choice(np.nonzero(cand.roll.to_numpy())[0], 5, replace=False)]
    sess_all = np.unique(d.sess.to_numpy())
    cols = feature_cols(full)
    bad, ctrl = [], 0
    for i in pick:
        row = cand.iloc[i]
        j = np.searchsorted(sess_all, row.sess.to_datetime64())
        sub = d[(d.sess >= sess_all[max(j - 30, 0)]) & (d.index < row.ts)]
        assert sub.index.max() < row.ts
        tr = build(sub, full.sym.iloc[0])
        hit = tr[tr.ts == row.ts]
        if len(hit) != 1:
            bad.append((row.ts, "missing"))
            continue
        a = hit[cols].to_numpy(np.float64)[0]
        b = row[cols].to_numpy(np.float64)
        ok = np.isclose(a, b, rtol=1e-9, atol=1e-12, equal_nan=True)
        if not ok.all():
            bad.append((row.ts, [c for c, o in zip(cols, ok) if not o]))
        # control: the target (future bars) must NOT be reproducible from the truncated data
        ctrl += int(np.isclose(hit.fwd_15.iloc[0], row.fwd_15, rtol=1e-9) and not np.isnan(row.fwd_15))
    print(f"truncation control: {ctrl}/{len(pick)} rows reproduced fwd_15 from truncated data (expect 0)")
    return len(pick), bad


def main_build(sym):
    t0 = time.time()
    d = load(sym)
    full = build(d, sym)
    t1 = time.time()
    ntest, bad = truncation_test(d, full)
    out = full[(full.sess >= FIRST) & (full.sess <= LAST)].reset_index(drop=True)
    out.insert(3, "period", np.where(out.sess >= CONF_START, "confirmation", "discovery"))
    assert out.ts.max() < HOLDOUT_SESSION_START
    os.makedirs(OUT, exist_ok=True)
    out.to_parquet(os.path.join(OUT, f"_own_{sym}.parquet"), compression="zstd")
    print(f"{sym}: rows={len(out)} sessions={out.sess.nunique()} feats={len(feature_cols(out))} "
          f"build_s={t1 - t0:.1f} total_s={time.time() - t0:.1f} trunc_tests={ntest} failures={len(bad)} {bad[:3]}")
    try:
        import run_pipeline as rp
        rp.log_trial(module="v4-features", scope=sym, oos_rows=len(out), runtime_s=round(time.time() - t0, 1),
                     note=f"feature dataset build; truncation test {ntest - len(bad)}/{ntest} pass")
    except Exception as e:                                  # logging must not break the build
        print("log_trial failed:", e)


def main_cross():
    own = {s: pd.read_parquet(os.path.join(OUT, f"_own_{s}.parquet")) for s in ("ES", "NQ", "YM")}
    for s, df in own.items():
        for o in own:
            if o == s:
                continue
            x = own[o][["ts", "ret_15_z", "ret_60_z"]].rename(
                columns={"ret_15_z": f"x{o}_ret_15_z", "ret_60_z": f"x{o}_ret_60_z"})
            df = df.merge(x, on="ts", how="left")
        df.to_parquet(os.path.join(OUT, f"feat_{s}.parquet"), compression="zstd")
        print(s, df.shape, "cross NaN share:",
              {c: round(df[c].isna().mean(), 3) for c in df.columns if c.startswith("x")})


if __name__ == "__main__":
    if sys.argv[1] == "build":
        main_build(sys.argv[2])
    else:
        main_cross()
