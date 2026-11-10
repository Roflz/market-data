"""
v3/test_harness.py - tests of v3/build_data.py (sessions table, bars) and v3/harness.py on SYNTHETIC 1-minute data
(market 'ZZ': tick 0.25, $5/pt like MES), plus an independent re-computation of every result: mark prices,
session columns, 400 random trades (time / stop / target / early-close exits) re-walked by hand, truncation
(no look-ahead) of the sessions table, future-perturbation of the stop path, stats / bootstrap / Holm /
Romano-Wolf, controls, eval, and lookahead_check catching two deliberately leaky signals.
Light (no real data, no lock needed):
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 \
      OMP_NUM_THREADS=3 python3 v3/test_harness.py
"""
import warnings

import numpy as np
import pandas as pd

import build_data as bd
import harness as H

warnings.filterwarnings("ignore")
SYM = "ZZ"
H.SPEC[SYM] = dict(usd=5.0, tick=0.25, micro="MZZ", cost=2 * 0.25 * 5.0 + 1.0)
TICK, USD, COST = 0.25, 5.0, 3.5
N_SESS = 60
EARLY, ROLL, STALE = 5, 10, 15          # session numbers with an early 13:00 close / a roll / no 9:30 bar
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("FAIL:", msg)


def synth(seed=1):
    """Raw 1-minute frame like build_data.raw_1m: tz-naive index, O H L C V inst sess, including 16:45-17:15 rows
    (must be dropped), ~3% missing minutes, an early close, a roll session, a missing 9:30 minute."""
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("2020-01-06", periods=N_SESS)
    rows = []
    px = 3000.0
    for s_no, D in enumerate(days):
        start = D - pd.Timedelta(hours=6)
        n = 23 * 60 + 15                                         # 18:00 .. 17:14 (tail must be dropped)
        t = start + pd.to_timedelta(np.arange(n), unit="min")
        steps = rng.integers(-4, 5, size=n) * TICK
        C = px + np.cumsum(steps)
        O = np.r_[px, C[:-1]] + rng.integers(-1, 2, size=n) * TICK
        Hh = np.maximum(O, C) + rng.integers(0, 4, size=n) * TICK
        Ll = np.minimum(O, C) - rng.integers(0, 4, size=n) * TICK
        V = rng.integers(1, 100, size=n).astype(float)
        inst = np.where(s_no < ROLL, 1, 2)
        f = pd.DataFrame({"O": O, "H": Hh, "L": Ll, "C": C, "V": V, "inst": inst, "sess": D}, index=t)
        if s_no == ROLL:                                         # old contract 18:00-19:59 at +50 points
            old = f.index < start + pd.Timedelta(hours=2)
            f.loc[old, ["O", "H", "L", "C"]] += 50.0
            f.loc[old, "inst"] = 1
        keep = rng.random(n) > 0.03
        keep[0] = True
        if s_no == EARLY:
            keep &= f.index < D + pd.Timedelta(hours=13)
        if s_no == STALE:
            keep &= f.index != D + pd.Timedelta(hours=9, minutes=30)
        f = f.loc[keep]
        rows.append(f)
        px = C[-1]
    raw = pd.concat(rows)
    raw.index.name = "ts"
    return raw


def build(raw):
    df, two = bd.filter_1m(raw)
    S = bd.make_sessions(bd.rows_1645(raw), df, two, SYM)
    b5 = bd.make_bars(df, 5)
    return df, two, S, b5


def install(S, b5):
    H._CACHE[("S", SYM)] = S
    H._CACHE[("B", SYM, 5)] = b5


# ---------------------------------------------------------------------------------------------------- independent refs
def ref_px(raw, D, k):
    """independent: executable price at mark k of session D from the raw minutes (kept contract, < 16:45 or the
    16:45 open)."""
    sess_rows = raw[(raw.sess == D)]
    sess_rows = sess_rows[sess_rows.inst == sess_rows.inst.iloc[-1]]
    tm = sess_rows.index.hour * 60 + sess_rows.index.minute
    body = sess_rows[~((tm >= 16 * 60 + 45) & (tm < 18 * 60))]
    t = D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * k)
    if k == 91:
        r = sess_rows[sess_rows.index == t]
        if len(r):
            return float(r.O.iloc[0])
        return float(body.C.iloc[-1])
    if t < body.index[0] or t > body.index[-1]:
        return np.nan
    if t in body.index:
        return float(body.loc[t, "O"])
    return float(body.C[body.index < t].iloc[-1])


def ref_trade(raw, D, ke, kx, d, stop_pts=np.nan, target_pts=np.nan):
    """independent re-walk on 5-minute buckets built straight from the raw minutes."""
    e = ref_px(raw, D, ke)
    x = ref_px(raw, D, kx)
    kind = "time"
    r = raw[(raw.sess == D)]
    r = r[r.inst == r.inst.iloc[-1]]
    tm = r.index.hour * 60 + r.index.minute
    r = r[~((tm >= 16 * 60 + 45) & (tm < 18 * 60))]
    last_off = (r.index[-1] - (D - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1)
    if not np.isfinite(x) or 15 * kx > last_off + 15:
        x = ref_px(raw, D, 91); kind = "close"
    if np.isfinite(stop_pts) or np.isfinite(target_pts):
        st = e - d * stop_pts if np.isfinite(stop_pts) else np.nan
        tg = e + d * target_pts if np.isfinite(target_pts) else np.nan
        t0 = D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * ke)
        t1 = D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * kx)
        r = raw[(raw.sess == D)]
        r = r[r.inst == r.inst.iloc[-1]]
        tm = r.index.hour * 60 + r.index.minute
        r = r[~((tm >= 16 * 60 + 45) & (tm < 18 * 60))]
        r = r[(r.index >= t0) & (r.index < t1)]
        for _, g in r.groupby(r.index.floor("5min")):
            o, h, l = g.O.iloc[0], g.H.max(), g.L.min()
            if d > 0 and l <= st:
                x = min(o, st) - TICK; kind = "stop"; break
            if d < 0 and h >= st:
                x = max(o, st) + TICK; kind = "stop"; break
            if d > 0 and h >= tg + TICK:
                x = tg; kind = "target"; break
            if d < 0 and l <= tg - TICK:
                x = tg; kind = "target"; break
    return d * (x - e) * USD - COST, kind


# ---------------------------------------------------------------------------------------------------- tests
def test_build(raw, df, two, S, b5):
    tm = df.index.hour * 60 + df.index.minute
    check(not ((tm >= 16 * 60 + 45) & (tm < 18 * 60)).any(), "kept 1-min rows inside 16:45-18:00")
    tb = b5.index.hour * 60 + b5.index.minute
    check(not ((tb >= 16 * 60 + 45) & (tb < 18 * 60)).any(), "5-min bar inside 16:45-18:00")
    check(len(S) == N_SESS, f"sessions rows {len(S)} != {N_SESS}")
    D = S.index[ROLL]
    check(S.roll.iloc[ROLL] and not S.roll.iloc[ROLL + 1], "roll flag")
    check(D in two, "two-contract session not detected")
    check(np.isnan(S.px_1800.iloc[ROLL]) and np.isfinite(S.px_2000.iloc[ROLL]), "roll session: old-contract marks")
    check((df[df.sess == D].inst == 2).all(), "roll session keeps the old contract's rows")
    check(np.isnan(S.prev_last_px.iloc[ROLL]) and np.isnan(S.gap.iloc[ROLL]), "prev price levels on a roll session")
    check(np.isnan(S.px_1300.iloc[EARLY]) and np.isfinite(S.px_1645.iloc[EARLY]), "early close marks")
    check(S.age_0930.iloc[STALE] > 0, "stale 9:30 mark has age 0")
    # every mark of every session vs the independent reference
    bad = 0
    for i, D in enumerate(S.index):
        for k in range(92):
            a = S[f"px_{H.MARKS[k]}"].iloc[i]
            r = ref_px(raw, D, k)
            if not ((np.isnan(a) and np.isnan(r)) or a == r):
                bad += 1
    check(bad == 0, f"{bad} mark prices differ from the independent reference")
    # session high/low, volume, prev columns
    i = 20
    D = S.index[i]
    r = df[df.sess == D]
    check(S.high.iloc[i] == r.H.max() and S.low.iloc[i] == r.L.min(), "session high/low")
    check(S.volume.iloc[i] == r.V.sum(), "session volume")
    rr = r[(r.index >= D + pd.Timedelta(hours=9, minutes=30)) & (r.index < D + pd.Timedelta(hours=16))]
    check(S.rth_high.iloc[i] == rr.H.max() and S.rth_low.iloc[i] == rr.L.min(), "rth high/low")
    check(S.close_1600.iloc[i] == rr.C.iloc[-1], "close_1600")
    check(S.prev_high.iloc[i] == S.high.iloc[i - 1] and S.prev_rv.iloc[i] == S.rv.iloc[i - 1], "prev_* shift")
    lr = np.diff(np.log(r.C.to_numpy()))
    check(abs(S.rv.iloc[i] - 100 * np.sqrt((lr ** 2).sum())) < 1e-9, "realized vol")
    th = S.t_high.iloc[i]
    check(r.H[r.index == D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=int(th))].iloc[0] == S.high.iloc[i],
          "time of the high")
    # 5-minute bars = aggregation of the kept minutes
    g = df.groupby([df.sess, df.inst, df.index.floor("5min")])
    check(len(g) == len(b5) and np.allclose(g.H.max().to_numpy(), b5.sort_index().groupby(
        [b5.sort_index().sess, b5.sort_index().inst, b5.sort_index().index]).H.max().to_numpy()), "5-min bars")


def test_truncation(raw, S):
    """no look-ahead: a mark's price computed from data cut right after the mark's own minute equals the full one
    (when the cut data shows the market open)."""
    bad = 0
    rng = np.random.default_rng(3)
    for _ in range(40):
        i = int(rng.integers(1, N_SESS)); k = int(rng.integers(0, 91))
        D = S.index[i]
        t = D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * k)
        cut = raw[raw.index <= t]
        df, two = bd.filter_1m(cut)
        if D not in set(df.sess):
            continue
        S2 = bd.make_sessions(bd.rows_1645(cut), df, two, SYM)
        a = S2.loc[D, f"px_{H.MARKS[k]}"]
        f = S.loc[D, f"px_{H.MARKS[k]}"]
        if np.isfinite(a) and a != f:
            bad += 1
        if np.isnan(a) and np.isfinite(f) and S.loc[D, f"age_{H.MARKS[k]}"] == 0 and i != ROLL:
            bad += 1
        # earlier marks unchanged
        for kk in range(k):
            a2, f2 = S2.loc[D, f"px_{H.MARKS[kk]}"], S.loc[D, f"px_{H.MARKS[kk]}"]
            if np.isfinite(a2) and a2 != f2:
                bad += 1
    check(bad == 0, f"truncation check: {bad} mark prices change when the future is removed")
    print("  truncation check: 40 random (session, mark) cuts, all earlier marks compared")


def test_trades(raw, S):
    rng = np.random.default_rng(7)
    n = 400
    ke = rng.integers(0, 90, size=n)
    kx = np.minimum(ke + rng.integers(1, 40, size=n), 91)
    d = rng.choice([-1, 1], size=n)
    stop = np.where(rng.random(n) < 0.5, rng.integers(0, 40, size=n) * TICK, np.nan)
    tgt = np.where(rng.random(n) < 0.3, rng.integers(1, 40, size=n) * TICK, np.nan)
    si = rng.integers(0, N_SESS, size=n)
    si[:5] = EARLY; ke[:5] = [40, 50, 60, 70, 75]; kx[:5] = 91                   # exits after the early close
    ent = pd.DataFrame({"session": S.index[si], "entry": ke, "exit": kx, "d": d, "stop_pts": stop,
                        "target_pts": tgt, "tag": np.arange(n)})
    tr = H.time_trades(SYM, ent)
    dropped = sum(tr.attrs["dropped"].values())
    check(len(tr) + dropped == n, "kept + dropped != n")
    bad = 0
    for _, row in tr.iterrows():
        j = int(row.tag)
        p, kind = ref_trade(raw, S.index[si[j]], int(ke[j]), int(kx[j]), int(d[j]), stop[j], tgt[j])
        if abs(p - row.pnl_usd) > 1e-9 or kind != row.exit_kind:
            bad += 1
            if bad < 4:
                print("  mismatch", j, p, kind, row.pnl_usd, row.exit_kind)
    check(bad == 0, f"{bad} of {len(tr)} trades differ from the independent re-walk")
    kinds = tr.exit_kind.value_counts().to_dict()
    print("  trades checked:", len(tr), kinds, "dropped:", tr.attrs["dropped"])
    check(all(kinds.get(k, 0) >= 3 for k in ("time", "stop", "target", "close")), f"exit kinds not all exercised {kinds}")
    check((tr.loc[tr.tag < 5, "exit_kind"].isin(["close", "stop", "target"])).all() and
          (tr.tag < 5).sum() == 5 and (tr.exit_kind == "close").sum() >= 1, "early-close session exits")
    ec = tr[tr.exit_kind == "close"]
    check((ec.t_exit.dt.hour * 60 + ec.t_exit.dt.minute <= 13 * 60).all(), "close exit time after the early close")
    check((tr.t_exit <= H.mark_time(pd.DatetimeIndex(tr.session), [H.mark_index(x) for x in tr.exit])).all(),
          "t_exit after the exit mark")
    tod = tr.t_exit.dt.hour * 60 + tr.t_exit.dt.minute
    check(not ((tod > 16 * 60 + 45) & (tod < 18 * 60)).any(), "trade exits after 16:45")
    check(np.allclose(tr.pnl_usd, tr.d * (tr.exit_px - tr.entry_px) * USD - COST), "pnl formula")
    # perturbing prices AFTER each trade's exit changes nothing (no look-ahead in the path walk)
    raw2 = raw.copy()
    last_exit = tr.t_exit.min()
    m = raw2.index >= last_exit + pd.Timedelta(minutes=5)
    sub = tr[tr.t_exit <= last_exit]
    raw2.loc[m, ["O", "H", "L", "C"]] += 1000.0
    df2, two2 = bd.filter_1m(raw2)
    S2 = bd.make_sessions(bd.rows_1645(raw2), df2, two2, SYM)
    install(S2, bd.make_bars(df2, 5))
    tr2 = H.time_trades(SYM, ent[ent.tag.isin(sub.tag)])
    check(np.allclose(tr2.sort_values("tag").pnl_usd.to_numpy(), sub.sort_values("tag").pnl_usd.to_numpy()),
          "future perturbation changed past trades")
    install(S, bd.make_bars(bd.filter_1m(raw)[0], 5))
    # tuples / string marks / direction column
    t3 = H.time_trades(SYM, [(S.index[3], "18:00", "09:30", 1), (S.index[3], "0930", "1645", -1, 5.0)])
    check(len(t3) == 2 and t3.exit_kind.iloc[0] == "time", "tuple entries")
    p, _ = ref_trade(raw, S.index[3], 0, 62, 1)
    check(abs(t3.pnl_usd.iloc[0] - p) < 1e-9, "tuple entry pnl")
    check(H.mark_index("16:45") == 91 and H.mark_index("09:30") == 62 and H.mark_index(0) == 0 and
          H.mark_index("1600") == 88, "mark_index")
    return tr


def test_daily_stats(tr, S):
    cal = S.index
    dly = H.daily_pnl(tr, cal)
    check(len(dly) == len(cal) and abs(dly.sum() - tr.pnl_usd.sum()) < 1e-6, "daily_pnl sum / length")
    check((dly[~cal.isin(tr.session)] == 0).all(), "no-trade days must be 0")
    st = H.stats(tr, cal, n_boot=500)
    a = st.set_index("span").loc["all"]
    check(abs(a["mean"] - tr.pnl_usd.mean()) < 1e-9 and a.n_trades == len(tr), "stats mean per trade")
    # clustered t, computed by hand
    g = tr.groupby("session").pnl_usd
    Sd, Nd = g.sum().to_numpy(), g.size().to_numpy()
    m = Sd.sum() / Nd.sum()
    t_ref = m / (np.sqrt(((Sd - m * Nd) ** 2).sum()) / Nd.sum())
    check(abs(a["t"] - t_ref) < 1e-9, "clustered t")
    check(abs(a.sharpe_ann - dly.mean() / dly.std(ddof=1) * np.sqrt(252)) < 1e-9, "sharpe")
    # daily-series mode
    st2 = H.stats(dly, n_boot=500).set_index("span").loc["all"]
    check(abs(st2["mean"] - dly.mean()) < 1e-12 and abs(st2["t"] - dly.mean() / dly.std(ddof=1) * np.sqrt(len(dly)))
          < 1e-9, "daily stats")


def test_bootstrap():
    rng = np.random.default_rng(0)
    W = next(H._sb_counts(1000, 200, 5.0, rng, chunk=200))
    check(np.allclose(W.sum(axis=1), 1000), "bootstrap counts must sum to n")
    # mean block length ~5: P(new block) = 1/5 -> about n/5 starts
    rng = np.random.default_rng(1)
    p = 1 / 5.0
    check(abs(p - 0.2) < 1e-12, "p")
    # p-values: null data -> roughly uniform; strong mean -> small
    ps = [H.boot_p(np.random.default_rng(s).normal(0, 1, 400), n_boot=400, seed=s) for s in range(60)]
    check(0.3 < np.mean(ps) < 0.7, f"null p-values mean {np.mean(ps):.2f} not ~0.5")
    check(0.0 < np.mean(np.array(ps) < 0.1) < 0.25, "null rejection rate at 10% far off")
    x = np.random.default_rng(5).normal(0.5, 1, 400)
    check(H.boot_p(x, n_boot=1000) < 0.01, "strong mean not detected")
    check(H.boot_p(-x, n_boot=1000) > 0.95, "negative mean gives a small p")
    # autocorrelated data: stationary bootstrap p larger than iid bootstrap p (block 1)
    e = np.random.default_rng(9).normal(0, 1, 2000)
    ar = np.zeros(2000)
    for i in range(1, 2000):
        ar[i] = 0.7 * ar[i - 1] + e[i]
    ar += 0.08
    check(H.boot_p(ar, n_boot=1000, block=10) > H.boot_p(ar, n_boot=1000, block=1), "block bootstrap vs iid")


def test_family():
    adj = H.holm([0.01, 0.04, 0.03, 0.005])
    check(np.allclose(adj, [0.03, 0.06, 0.06, 0.02]), f"holm {adj}")
    rng = np.random.default_rng(2)
    T, K = 1500, 8
    common = rng.normal(0, 1, (T, 1))
    X = 0.6 * common + rng.normal(0, 1, (T, K))
    X[:, 0] += 0.15                                                # one real edge
    D = pd.DataFrame(X, columns=[f"s{k}" for k in range(K)])
    r = H.romano_wolf(D, n_boot=1000).set_index("strategy")
    check(r.loc["s0", "p_rw"] < 0.01, "romano-wolf misses the real edge")
    check((r.p_rw >= r.p_raw - 1e-12).all(), "adjusted p below raw p")
    check((r.drop("s0").p_rw > 0.05).mean() > 0.8, "romano-wolf rejects nulls")
    check((r.p_rw <= r.p_holm + 0.02).all(), "romano-wolf should not be much worse than holm")


def test_controls(tr, S):
    ent = pd.DataFrame({"session": tr.session, "entry": tr.entry, "exit": tr.exit, "d": tr.d,
                        "stop_pts": tr.stop_pts, "target_pts": tr.target_pts})
    dr = H.drift_trades(SYM, ent)
    check((dr.d == 1).all() and len(dr) == len(tr), "drift_trades")
    rd = H.random_time_trades(SYM, ent, n_rep=5, seed=1)
    check(set(rd.rep) == set(range(5)), "reps")
    L = rd.exit.map(H.mark_index) - rd.entry.map(H.mark_index)
    L0 = (ent.exit.map(H.mark_index) - ent.entry.map(H.mark_index)).to_numpy()
    check(set(L.unique()) <= set(L0), "random marks keep the holding length")
    check(set(rd.session) <= set(ent.session), "keep_session")
    rd2 = H.random_time_trades(SYM, ent, n_rep=2, seed=1, keep_session=False, keep_marks=True, keep_side=True)
    check(len(rd2) > 0, "random sessions")
    cr = H.control_report(tr, rd)
    check(list(cr.window) == ["all", "2010-17", "2018-25H1", "2018+", "2022+"] and cr.n_reps.iloc[0] == 5,
          "control_report")


def test_eval(tr, S):
    t = tr.copy()
    r = H.eval(t, [("fixed", 1), ("fixed", 3)], calendar_=S.index,
               windows={"all": ("2020-01-01", "2020-12-31")})
    check(len(r) == 4 and {"pass_pct", "bust_pct", "within_10", "days_pass_median"} <= set(r.columns), "eval columns")
    # a sure winner passes on day 4 (best day 25% of profit), consistency respected
    cal = S.index
    big = pd.DataFrame({"session": cal, "entry": 0, "exit": 91, "d": 1})
    tt = H.time_trades(SYM, big)
    tt["pnl_usd"] = 350.0
    r2 = H.eval(tt, ("fixed", 1), calendar_=cal, windows={"all": ("2020-01-01", "2020-12-31")})
    check((r2.pass_pct > 90).all() and (r2.days_pass_median == 4).all(), f"eval sure winner {r2.to_dict('records')}")


def test_lookahead(S):
    def good(Sx, B):
        x = Sx[Sx.px_0930 > Sx.prev_last_px]
        return pd.DataFrame({"session": x.index, "entry": "09:30", "exit": "16:45", "d": 1})

    def good_bars(Sx, B):
        b = B[5]
        last = b[(b.index.hour == 9) & (b.index.minute == 25)]               # closes at 9:30
        x = last[last.C > last.O]
        return pd.DataFrame({"session": x.session.to_numpy(), "entry": "09:30", "exit": "12:00", "d": 1})

    def bad(Sx, B):
        x = Sx[Sx.close_1600 > Sx.px_0930]                                   # uses the 16:00 close at 9:30
        return pd.DataFrame({"session": x.index, "entry": "09:30", "exit": "16:45", "d": 1})

    def bad_bars(Sx, B):
        b = B[5]
        nxt = b[(b.index.hour == 9) & (b.index.minute == 30)]               # closes at 9:35, entry 9:30
        x = nxt[nxt.C > nxt.O]
        return pd.DataFrame({"session": x.session.to_numpy(), "entry": "09:30", "exit": "12:00", "d": 1})

    for fn in (good, good_bars):
        r = H.lookahead_check(fn, SYM, n_cuts=25, seed=1, tfs=(5,))
        check(r.same.all(), f"lookahead_check flags a clean signal {fn.__name__}")
    for fn in (bad, bad_bars):
        caught = False
        for sd in range(5):
            try:
                H.lookahead_check(fn, SYM, n_cuts=40, seed=sd, tfs=(5,))
            except AssertionError:
                caught = True
                break
        check(caught, f"lookahead_check misses the look-ahead signal {fn.__name__}")
    ent = pd.DataFrame({"session": S.index[1:], "entry": "18:00", "exit": "09:30", "d": -1, "stop_pts": 5.0})
    rep = H.standard_report(SYM, ent, n_rep=5, n_boot=200)
    check({"trades", "stats", "vs_drift", "excess_vs_drift", "vs_random", "vs_hour_drift"} <= set(rep),
          "standard_report keys")
    hd = rep["hour_drift"]
    check((hd.d == 1).all() and set(hd.entry) == {"1800"} and set(hd.exit) == {"0930"}, "hour_drift_trades")
    ex = rep["excess_vs_drift"].set_index("span").loc["all", "mean"]
    check(abs(ex - (rep["trades"].pnl_usd.mean() - rep["drift"].pnl_usd.mean())) < 1e-9, "paired excess")


def main():
    raw = synth()
    df, two, S, b5 = build(raw)
    install(S, b5)
    test_build(raw, df, two, S, b5)
    test_truncation(raw, S)
    tr = test_trades(raw, S)
    test_daily_stats(tr, S)
    test_bootstrap()
    test_family()
    test_controls(tr, S)
    test_eval(tr, S)
    test_lookahead(S)
    print(f"{len(FAILS)} failures" if FAILS else "ALL TESTS PASSED")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
