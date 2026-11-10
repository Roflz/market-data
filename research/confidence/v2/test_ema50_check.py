"""
Synthetic-data tests for v2/ema50_check.py (no market data). Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_ema50_check.py
"""
import warnings

import numpy as np
import pandas as pd

import ema50_check as ec
import signals as sg

warnings.filterwarnings("ignore")
TICK = 0.25


def _m1(n_days=45, seed=0, drift=None, mu=0.06, reg_len=3000):
    """1-minute bars 18:00 -> 16:59 per session (one contract), trending regimes so EMA50 pullbacks occur."""
    rng = np.random.default_rng(seed)
    idx, sess = [], []
    for k, day in enumerate(pd.bdate_range("2021-03-01", periods=n_days)):
        start = day - pd.Timedelta(hours=6)
        t = start + pd.to_timedelta(np.arange(23 * 60), unit="min")
        idx.append(t)
        sess += [k] * len(t)
    idx = pd.DatetimeIndex(np.concatenate(idx))
    n = len(idx)
    reg = np.repeat(rng.choice([-1, 1], size=n // reg_len + 1), reg_len)[:n] if drift is None else np.full(n, drift)
    C = 4000 + np.cumsum(rng.normal(mu * reg, 1.0, n))
    C = np.round(C * 4) / 4
    O = np.r_[C[0], C[:-1]]
    H = np.maximum(O, C) + np.round(rng.uniform(0, 1, n) * 4) / 4
    L = np.minimum(O, C) - np.round(rng.uniform(0, 1, n) * 4) / 4
    return pd.DataFrame({"O": O, "H": H, "L": L, "C": C, "inst": 1, "sess": sess}, index=idx)


def _bars(m1, tf=60):
    """Aggregate like signals.bars."""
    g = m1.groupby([m1.sess, m1.inst, m1.index.floor(f"{tf}min")], sort=False)
    b = g.agg(O=("O", "first"), H=("H", "max"), L=("L", "min"), C=("C", "last"))
    b.index = b.index.get_level_values(2)
    b["sess"] = g.sess.first().to_numpy()
    b["inst"] = 1
    b["V"] = 1.0
    b["vwap"] = b.C
    b = b.sort_index()
    b["seg"] = (b.sess.ne(b.sess.shift()) | b.inst.ne(b.inst.shift())).cumsum()
    b["run"] = 1
    return b


def _ctx(b):
    return sg.context(b, tick=TICK)


M1 = _m1(60, mu=0.01, reg_len=12000)
B = _bars(M1)
CTX = _ctx(B)


def test_matches_trigger_scan():
    same, gap, n = ec.check_vs_trigger_scan(B, CTX, TICK, 60)
    assert same and n > 5 and gap == 0.0, (same, gap, n)


def test_truncation():
    assert ec.truncation_check(B, TICK, 60, start=0, length=len(B), cuts=(120, 400, 700, len(B) - 1)) == 0


def test_mirror_long_short():
    K = 9000.0
    bm = B.copy()
    bm["O"], bm["C"] = K - B.O, K - B.C
    bm["H"], bm["L"] = K - B.L, K - B.H
    bm["vwap"] = bm.C
    S, Sm = ec.bar_signals(B, CTX, TICK, 5, 60), ec.bar_signals(bm, _ctx(bm), TICK, 5, 60)
    for tol in ec.TOLS.values():
        a, c = ec.setup_mask(S, 1, tol), ec.setup_mask(Sm, -1, tol)
        assert np.array_equal(a, c)
        assert np.array_equal(ec.setup_mask(S, -1, tol), ec.setup_mask(Sm, 1, tol))
        assert np.allclose(S["stop"][1][a], K - Sm["stop"][-1][a])


def test_tolerance_nested_and_stop_lookback():
    S = ec.bar_signals(B, CTX, TICK, 5, 60)
    m0, mp, mm = (ec.setup_mask(S, 1, t) for t in (0.0, 0.25, -0.25))
    assert (mm <= m0).all() and (m0 <= mp).all() and mp.sum() > m0.sum() >= mm.sum()
    L = B.L.to_numpy()
    i = np.flatnonzero(m0)
    assert (L[i] <= CTX.ema50.to_numpy()[i]).all()
    for k in (3, 8):
        Sk = ec.bar_signals(B, CTX, TICK, k, 60)
        j = np.flatnonzero(Sk["base"])
        lo = pd.Series(L).rolling(k).min().to_numpy()
        assert (Sk["stop"][1][j] <= lo[j] - TICK + 1e-9).all()
        assert (Sk["stop"][1][j] <= B.C.to_numpy()[j] - S["R"][j] + 1e-9).all()


def test_labels_match_hand_walk():
    import labels as lb
    ev = ec.universe_events(B, CTX, TICK, 5, 60)
    ev = ev[ev.trend | ev.tol0].reset_index(drop=True)
    U = ec.label_universe("ES", 60, B, CTX, M1, ev)
    assert len(U) > 50
    assert (U.kind_cross == "cross").any() and (U.kind_3R == "target").any()
    spec = sg.SPEC["ES"]
    cr = ec.ema_cross(CTX)
    rng = np.random.default_rng(1)
    for k in rng.choice(len(U), size=40, replace=False):
        r = U.iloc[k]
        for ex in ec.EXITS:
            p, why = ec.hand_walk(r, M1, B, 60, TICK, spec["usd"], spec["cost"], ex, cr)
            assert abs(p - r[f"pnl_{ex}"]) < 1e-6, (ex, k, p, r[f"pnl_{ex}"], why, r[f"kind_{ex}"])
    # exit times: inside the session, after the entry, flat by 16:45
    for ex in ec.EXITS:
        te, tx = pd.DatetimeIndex(U.t_entry), pd.DatetimeIndex(U[f"t_exit_{ex}"])
        assert (tx >= te).all()
        tod = (tx - tx.normalize()) / pd.Timedelta(minutes=1)
        assert not ((tod > 16 * 60 + 45) & (tod < 18 * 60)).any()
    _, forced = lb.eligible(B, 60)
    assert (U.i.to_numpy() < forced[U.i.to_numpy()]).all()


def test_matched_draws():
    rng = np.random.default_rng(0)
    pool = pd.DataFrame({"d": rng.choice([-1, 1], 5000), "year": rng.choice([2015, 2016], 5000),
                         "hour": rng.integers(0, 24, 5000), "rb": rng.integers(0, 5, 5000)})
    pool = pool[~((pool.hour == 3) & (pool.year == 2016))].reset_index(drop=True)   # an empty (year, hour) cell
    setup = pd.DataFrame({"d": [1, -1, 1, 1], "year": [2015, 2016, 2016, 2015], "hour": [5, 7, 3, 23],
                          "rb": [0, 4, 2, 1]})
    idx, lev = ec.matched_draws(setup, pool, 50, seed=3)
    idx2, _ = ec.matched_draws(setup, pool, 50, seed=3)
    assert np.array_equal(idx, idx2)
    assert list(lev) == [4, 4, 2, 4]
    for r in (0, 1, 3):
        P = pool.iloc[idx[r]]
        assert (P[["d", "year", "hour", "rb"]].to_numpy() == setup.iloc[r].to_numpy()).all()
    P = pool.iloc[idx[2]]
    assert (P.d == 1).all() and (P.year == 2016).all()
    assert len(np.unique(idx[0])) > 1


def test_compare_edges_and_top_days():
    n = 300
    rng = np.random.default_rng(2)
    sess = pd.DatetimeIndex(pd.bdate_range("2015-01-01", periods=n))
    setup = pd.DataFrame({"session": sess, "pnl_hold": rng.normal(3, 10, n)})
    setup.loc[5, "pnl_hold"] = 500.0
    pool = np.full(1000, 1.0)
    idx = rng.integers(0, 1000, (n, 20))
    T = ec.compare(setup, "pnl_hold", {"trend": (pool, idx, np.arange(1000) % 50)}).set_index("span")
    assert np.isclose(T.loc["all", "trend_usd"], 1.0)
    assert np.isclose(T.loc["all", "trend_edge"], setup.pnl_hold.mean() - 1.0)
    assert T.loc["all", "n"] == n and T.loc["all w/o top 10 days", "n"] == n - 10
    assert T.loc["all w/o top 10 days", "usd_trade"] < T.loc["all", "usd_trade"]
    assert T.loc["all", "trend_p"] == 0.0
    assert np.isclose(T.loc["all w/o top 10 days", "trend_usd"], 1.0)


def test_cluster_t():
    rng = np.random.default_rng(0)
    x = rng.normal(1, 3, 400)
    g = np.arange(400)
    t_iid = x.mean() / (x.std(ddof=1) / np.sqrt(400))
    assert abs(ec.cluster_t(x, g) - t_iid) / t_iid < 0.01           # singleton clusters == plain t
    xc = np.repeat(rng.normal(1, 3, 40), 10)                         # 40 clusters of 10 identical trades
    gc_ = np.repeat(np.arange(40), 10)
    t_naive = xc.mean() / (xc.std(ddof=1) / np.sqrt(400))
    assert ec.cluster_t(xc, gc_) < 0.5 * t_naive


def test_trimmed_means():
    pnl = np.array([[1.0, 5.0], [2.0, 1.0], [10.0, 1.0], [3.0, 1.0]])
    sc = np.array([[0, 0], [0, 1], [1, 2], [2, 3]])
    # col 0: day sums {0: 3, 1: 10, 2: 3} -> drop day 1 -> mean(1, 2, 3); col 1: drop day 0 (5) -> mean(1, 1, 1)
    assert np.allclose(ec.trimmed_means(pnl, sc, k=1), [2.0, 1.0])


if __name__ == "__main__":
    import lucid
    lucid.install()
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
    print("all tests passed")
