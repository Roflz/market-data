"""
Independent re-implementation of scratchpad/next/rebal/PREREG.md (rebalancing-pressure signal, rules P, A, B).
Written from the PREREG text only. Outputs go to this folder.
"""
import json, os
import numpy as np
import pandas as pd

W = os.path.dirname(os.path.abspath(__file__))
TZ = "America/New_York"
NW = 26
THR = np.arange(NW) * 0.001          # 0.0% .. 2.5%


# ---------------------------------------------------------------- signal
def zn_close_by_day(days):
    z = pd.read_csv("data/ZN_fut_1h.csv", usecols=["ts_event", "Open", "Close", "instrument_id"])
    z.index = pd.to_datetime(z.ts_event, utc=True, format="ISO8601").dt.tz_convert(TZ)
    z = z[~z.index.duplicated()].sort_index()
    roll = z.instrument_id.ne(z.instrument_id.shift()) & z.instrument_id.shift().notna()
    jump = (z.Open - z.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)          # additive back-adjustment (newest = 0)
    z["aC"] = z.Close + adj
    # last bar opening at or before 15:00 ET on day t (as-of lookup; on 2014-10-03 ZN has no bars at all that day,
    # so the as-of rule falls back to the 2014-10-02 17:00 bar)
    tgt = (pd.DatetimeIndex(days).as_unit("ns") + pd.Timedelta(hours=15)).tz_localize(TZ).as_unit("ns").asi8
    zt = z.index.as_unit("ns").asi8
    j = np.searchsorted(zt, tgt, side="right") - 1
    last = z.iloc[j].copy()
    last["bar_ts"] = last.index
    last["tmin"] = last.index.hour * 60 + last.index.minute
    last["same_day"] = last.index.tz_localize(None).normalize() == pd.DatetimeIndex(days)
    last.index = days
    return last


def build_signal(sym_eq="ES"):
    ds = pd.read_pickle(f"data/daily_sessions_{sym_eq}.pkl")
    ds = ds[ds.cash_day]
    days = ds.index
    rEQ = (ds.close_adj.diff() / ds.close_raw.shift()).to_numpy()
    zn = zn_close_by_day(days)
    rZN = (zn.aC.diff() / zn.Close.shift()).to_numpy()
    w = np.full(NW, 0.60)
    s = np.full(len(days), np.nan)
    for i in range(1, len(days)):
        a = w * (1 + rEQ[i]); b = (1 - w) * (1 + rZN[i])
        wp = a / (a + b)
        dev = wp - 0.60
        s[i] = dev.mean()
        w = np.where(np.abs(dev) >= THR, 0.60, wp)
    out = pd.DataFrame({"s": s, "rEQ": rEQ, "rZN": rZN, "zn_bar_tmin": zn.tmin.to_numpy(), "zn_same_day": zn.same_day.to_numpy(),
                        "early_close": ds.early_close.to_numpy()}, index=days)
    return out


# ---------------------------------------------------------------- price segments
def load_m1(sym):
    return pd.read_pickle(f"{W}/m1_{sym}.pkl")


def bar_at(ts_ns, target_ns, window_min):
    j = np.searchsorted(ts_ns, target_ns, side="left")
    ok = (j < len(ts_ns))
    jj = np.minimum(j, len(ts_ns) - 1)
    ok &= ts_ns[jj] <= target_ns + window_min * 60 * 10**9
    return np.where(ok, jj, -1)


def segments(days, early, sym):
    """Segment i: from 16:05 on day i to 16:05 (13:05 if early) on day i+1. Returns entry/exit idx & prices & status."""
    m = load_m1(sym)
    ts = pd.DatetimeIndex(m.ts).as_unit("ns").asi8
    O = m.Open.to_numpy().astype("float64")
    inst = m.inst.to_numpy()
    nchg = np.concatenate([[0], np.cumsum(inst[1:] != inst[:-1])])
    D = pd.DatetimeIndex(days).as_unit("ns")
    t1605 = (D + pd.Timedelta(hours=16, minutes=5)).tz_localize(TZ).as_unit("ns").asi8
    t1305 = (D + pd.Timedelta(hours=13, minutes=5)).tz_localize(TZ).as_unit("ns").asi8
    n = len(days)
    ent = bar_at(ts, t1605, 15)
    ext_target = np.where(early, t1305, t1605)
    ext_w = np.where(early, 10, 15)
    ext = np.array([bar_at(ts, np.array([ext_target[k]]), ext_w[k])[0] for k in range(n)])
    rows = []
    for i in range(n - 1):
        st = "ok"
        e, x = ent[i], ext[i + 1]
        if early[i]:
            st = "early_close"
        elif e < 0 or x < 0:
            st = "missing"
        elif nchg[x] != nchg[e]:
            st = "roll"
        rows.append(dict(date=days[i], exit_date=days[i + 1], status=st,
                         e_ts=pd.Timestamp(ts[e], tz="UTC").tz_convert(TZ) if e >= 0 else pd.NaT,
                         x_ts=pd.Timestamp(ts[x], tz="UTC").tz_convert(TZ) if x >= 0 else pd.NaT,
                         px_e=O[e] if e >= 0 else np.nan, px_x=O[x] if x >= 0 else np.nan,
                         exact_e=(e >= 0 and ts[e] == t1605[i]),
                         exact_x=(x >= 0 and ts[x] == ext_target[i + 1])))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- engine
def run(seg, pos, ppt, side_cost):
    """seg: DataFrame of segments; pos: raw rule positions per segment. Returns trades df, per-segment arrays."""
    ok = (seg.status == "ok").to_numpy()
    q = np.where(ok, pos, 0).astype(int)
    d = np.where(ok, seg.px_x.to_numpy() - seg.px_e.to_numpy(), 0.0)
    gross_usd = q * d * ppt
    M = len(q)
    prev = np.concatenate([[0], q[:-1]])
    trades = []
    cur = None
    for i in range(M + 1):
        qi = q[i] if i < M else 0
        pi = prev[i] if i < M else q[M - 1]
        # boundary between pi and qi
        if pi != 0 and (qi == 0 or np.sign(qi) != np.sign(pi)):     # close current trade
            cur["cost"] += abs(pi) * side_cost
            if i < M:
                st = seg.status.iat[i]
                cur["exit_reason"] = ("flip" if qi != 0 else ("signal" if st == "ok" else st))
            else:
                cur["exit_reason"] = "end"
            cur["exit_ts"] = seg.x_ts.iat[i - 1]; cur["exit"] = seg.px_x.iat[i - 1]
            trades.append(cur); cur = None
        if qi != 0 and (pi == 0 or np.sign(qi) != np.sign(pi)):     # open new trade
            cur = dict(date=seg.date.iat[i], entry_ts=seg.e_ts.iat[i], entry=seg.px_e.iat[i],
                       side="long" if qi > 0 else "short", cost=abs(qi) * side_cost, gross_usd=0.0,
                       nseg=0, maxsize=0)
        elif qi != 0 and qi != pi:                                    # resize inside run
            cur["cost"] += abs(qi - pi) * side_cost
        if qi != 0:
            cur["gross_usd"] += gross_usd[i]; cur["nseg"] += 1; cur["maxsize"] = max(cur["maxsize"], abs(qi))
    T = pd.DataFrame(trades)
    T["gross_pts"] = T.gross_usd / ppt
    T["net_usd"] = T.gross_usd - T.cost
    T["net_pts"] = T.net_usd / ppt
    T["net_bp"] = 1e4 * T.net_pts / T.entry
    # per-segment net (boundary costs: exit part to previous segment, entry/resize part to new segment)
    seg_cost = np.zeros(M)
    for i in range(M + 1):
        qi = q[i] if i < M else 0
        pi = prev[i] if i < M else q[M - 1]
        if qi == pi:
            continue
        if pi != 0 and qi != 0 and np.sign(pi) == np.sign(qi):
            seg_cost[i] += abs(qi - pi) * side_cost
        else:
            if pi != 0: seg_cost[i - 1] += abs(pi) * side_cost
            if qi != 0: seg_cost[i] += abs(qi) * side_cost
    return T, q, gross_usd, gross_usd - seg_cost, d


def tstat(x):
    x = np.asarray(x, float)
    return x.mean() / x.std(ddof=1) * np.sqrt(len(x)) if len(x) > 1 else np.nan


BLOCKS = [(2010, 2011), (2012, 2013), (2014, 2015), (2016, 2017), (2018, 2019), (2020, 2021), (2022, 2023), (2024, 2026)]


def evaluate(T, q, d, ok, ppt, side_cost, tbar, rng_seed=12345):
    y = pd.to_datetime(T.date).dt.year
    yrs = (pd.Timestamp("2026-11-06") - pd.Timestamp(T.date.min())).days / 365.25
    blk = {f"{a}-{b % 100:02d}": float(T.net_usd[(y >= a) & (y <= b)].sum()) for a, b in BLOCKS}
    res = dict(n=len(T), n_long=int((T.side == "long").sum()), n_short=int((T.side == "short").sum()),
               per_year=len(T) / yrs, mean_usd=T.net_usd.mean(), total_usd=T.net_usd.sum(),
               mean_bp=T.net_bp.mean(), t=tstat(T.net_usd), t_bp=tstat(T.net_bp),
               since2018=float(T.net_usd[pd.to_datetime(T.date) >= "2018-01-01"].sum()),
               since2023=float(T.net_usd[pd.to_datetime(T.date) >= "2023-01-01"].sum()),
               t_since2023=tstat(T.net_usd[pd.to_datetime(T.date) >= "2023-01-01"]),
               blocks=blk, blocks_pos=int(sum(v > 0 for v in blk.values())),
               long_usd=float(T.net_usd[T.side == "long"].sum()), short_usd=float(T.net_usd[T.side == "short"].sum()),
               by_year={int(k): float(v) for k, v in T.net_usd.groupby(y).sum().items()},
               max_size=int(T.maxsize.max()))
    res["ex2020_total"] = float(T.net_usd[y != 2020].sum()); res["ex2020_t"] = tstat(T.net_usd[y != 2020])
    # random direction
    rng = np.random.default_rng(rng_seed)
    g, c = T.gross_usd.to_numpy(), T.cost.to_numpy()
    sims = np.array([(rng.choice([-1, 1], len(g)) * g - c).sum() for _ in range(1000)])
    res["randdir_pct"] = float((sims < res["total_usd"]).mean()); res["randdir_p95"] = float(np.percentile(sims, 95))
    # shuffled-date placebo on the segment path
    M = len(q)
    rng2 = np.random.default_rng(rng_seed)
    pl = []
    for _ in range(1000):
        k = rng2.integers(252, M - 252 + 1)
        qq = np.roll(q, k) * ok
        dq = np.abs(np.diff(np.concatenate([[0], qq, [0]]))).sum()
        pl.append((qq * d * ppt).sum() - dq * side_cost)
    pl = np.array(pl)
    res["placebo_pct"] = float((pl < res["total_usd"]).mean()); res["placebo_p95"] = float(np.percentile(pl, 95))
    res["C1"] = bool(res["t"] >= tbar); res["C2"] = res["since2018"] > 0; res["C3"] = res["since2023"] > 0
    res["C4"] = res["blocks_pos"] >= 6; res["C5"] = res["total_usd"] > res["randdir_p95"]
    res["PASS"] = all(res[k] for k in ("C1", "C2", "C3", "C4", "C5"))
    res["beats_drift"] = res["total_usd"] > res["placebo_p95"]
    return res


def positions(sig, seg):
    s = sig.s.to_numpy()
    days = sig.index
    n = len(s)
    pct = np.full(n, np.nan); z = np.full(n, np.nan)
    for i in range(1, n):
        if i - 252 < 1:
            continue
        ref = s[i - 252:i]
        pct[i] = (ref <= s[i]).mean()
        z[i] = (s[i] - ref.mean()) / ref.std(ddof=1)
    sig = sig.assign(pct=pct, z=z)
    sig = sig.reindex(seg.date)
    dec = sig.pct.notna().to_numpy() & ~sig.early_close.to_numpy()
    P = np.where(dec & (sig.pct <= 0.10), 1, np.where(dec & (sig.pct >= 0.90), -1, 0))
    zz = sig.z.to_numpy()
    zz0 = np.nan_to_num(zz)
    A = np.where(dec, -np.sign(zz0) * np.minimum(3, np.floor(np.abs(zz0))), 0).astype(int)
    B = np.where(dec & (sig.pct <= 0.10), 1, 0)
    return dict(P=P, A=A, B=B), sig, dec


def main():
    sig = build_signal("ES")
    sig.to_csv(f"{W}/my_signal.csv")
    days = sig.index
    early = sig.early_close.to_numpy()
    out = {}
    segs = {}
    for sym in ("NQ", "ES"):
        cp = f"{W}/seg_{sym}.pkl"
        if os.path.exists(cp):
            segs[sym] = pd.read_pickle(cp)
        else:
            segs[sym] = segments(days, early, sym); segs[sym].to_pickle(cp)
    pos, sigx, dec = positions(sig, segs["NQ"])
    first = np.argmax(dec)
    print("first decision", segs["NQ"].date.iat[first])
    for sym in ("NQ", "ES"):
        sg = segs[sym].iloc[first:].reset_index(drop=True)
        print(sym, "segments", len(sg), sg.status.value_counts().to_dict(),
              "exact entry", sg.exact_e.mean(), "exact exit", sg.exact_x.mean())
    for sym, ppt, sc, sc2 in (("NQ", 2.0, 1.0, 1.5), ("ES", 5.0, 1.75, 1.75 + 0.5 * 5 * 0.25 * 2 / 2)):
        sg = segs[sym].iloc[first:].reset_index(drop=True)
        ok = (sg.status == "ok").to_numpy()
        lbl = "MNQ" if sym == "NQ" else "MES"
        for r in ("P", "A", "B"):
            p = pos[r][first:]
            T, q, gu, segnet, d = run(sg, p, ppt, sc)
            res = evaluate(T, q, d, ok, ppt, sc, 2.0 if r == "P" else 2.4)
            T2, *_ = run(sg, p, ppt, sc2 if sym == "NQ" else 1.75 + 1.25)
            res["stress2tick_total"] = float(T2.net_usd.sum()); res["stress2tick_t"] = tstat(T2.net_usd)
            inmk = q != 0
            res["day_t"] = tstat(segnet[inmk]); res["n_days_in"] = int(inmk.sum())
            out[f"{r}_{lbl}"] = res
            T.to_csv(f"{W}/my_trades_{r}_{lbl}.csv", index=False)
            pd.DataFrame({"date": sg.date, "exit_date": sg.exit_date, "status": sg.status, "pos_rule": p, "q": q,
                          "d_pts": d, "gross_usd": gu, "net_usd": segnet}).to_csv(f"{W}/my_segs_{r}_{lbl}.csv", index=False)
    # NQ-built signal through P (report only)
    sigN = build_signal("NQ")
    posN, _, decN = positions(sigN, segs["NQ"])
    sg = segs["NQ"].iloc[first:].reset_index(drop=True)
    T, q, gu, segnet, d = run(sg, posN["P"][first:], 2.0, 1.0)
    out["P_MNQ_NQbuilt"] = dict(n=len(T), total_usd=T.net_usd.sum(), t=tstat(T.net_usd), mean_usd=T.net_usd.mean())
    T.to_csv(f"{W}/my_trades_P_MNQ_NQbuilt.csv", index=False)
    # correlation with live models (daily, exit-dated and entry-dated)
    cm = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"]).groupby("date").usd.sum()
    for r in ("P", "A", "B"):
        S = pd.read_csv(f"{W}/my_segs_{r}_MNQ.csv", parse_dates=["date", "exit_date"])
        cal = pd.DatetimeIndex(sorted(set(S.exit_date)))
        x = S.groupby("exit_date").net_usd.sum().reindex(cal, fill_value=0)
        out[f"{r}_MNQ"]["corr_live_exitdated"] = float(x.corr(cm.reindex(cal, fill_value=0)))
        x2 = S.groupby("date").net_usd.sum()
        cal2 = x2.index
        out[f"{r}_MNQ"]["corr_live_entrydated"] = float(x2.corr(cm.reindex(cal2, fill_value=0)))
    json.dump(out, open(f"{W}/my_summary.json", "w"), indent=1, default=float)
    for k, v in out.items():
        print("\n==", k)
        for kk, vv in v.items():
            print(f"  {kk}: {vv}")


if __name__ == "__main__":
    main()
