"""
Unit tests for v2/eval_candidates.py on synthetic 1-minute paths (no market data). Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_eval_candidates.py
"""
import numpy as np
import pandas as pd

import eval_candidates as evc
import eval_sim as es

TF = 5
T0 = pd.Timestamp("2020-03-02 18:00")


def synth(n_bars=200, seed=0, prices=None, rule=None):
    """One segment of n_bars 5-minute bars made of contiguous 1-minute rows (NQ spec)."""
    n1 = n_bars * TF
    if prices is None:
        rng = np.random.default_rng(seed)
        C = 100 + np.round(np.cumsum(rng.normal(0, 0.6, n1)) * 4) / 4
    else:
        C = np.asarray(prices, float)
        n1 = len(C)
        n_bars = n1 // TF
    O = np.r_[C[0], C[:-1]]
    rng = np.random.default_rng(seed + 1)
    H = np.maximum(O, C) + np.round(rng.uniform(0, 0.5, n1) * 4) / 4
    L = np.minimum(O, C) - np.round(rng.uniform(0, 0.5, n1) * 4) / 4
    if prices is not None:
        H, L = np.maximum(O, C), np.minimum(O, C)
    tmin = (T0 + pd.to_timedelta(np.arange(n1), "min")).as_unit("ns").asi8
    first = np.arange(n_bars) * TF
    last = first + TF - 1
    ok = np.arange(n_bars) < n_bars - 1
    forced = np.full(n_bars, n_bars - 1)
    Ob, Cb = O[first], C[last]
    bstart = tmin[first]
    return evc.Mkt("NQ", TF, O, H, L, C, tmin, first, last, ok, forced, Ob, Cb, bstart, rule)


def sigs(M, i, d, stop, score=None):
    n = len(i)
    sess = np.full(n, pd.Timestamp("2020-03-03"))
    return evc.make_signals(M, i, d, stop, sess, np.zeros(n) if score is None else score)


def test_standalone_stop_and_time():
    # flat at 100 for 4 bars, then down to 90 -> the long's stop at 97 fills at 97 - 1 tick
    p = [100.0] * 20 + list(np.linspace(100, 90, 20)) + [90.0] * 20
    M = synth(prices=p)
    S = sigs(M, [0], [1], [97.0])
    assert S["sa_kind"][0] == evc.K_STOP
    assert abs(S["sa_pnl"][0] - ((97 - 0.25 - 100) * 2 - 2.0)) < 1e-9
    # a short is held to the close of the last bar (time exit)
    S = sigs(M, [0], [-1], [103.0])
    assert S["sa_kind"][0] == evc.K_TIME
    assert abs(S["sa_pnl"][0] - ((100 - 90) * 2 - 2.0)) < 1e-9


def test_rule_exit_next_open():
    p = list(np.linspace(100, 110, 60))
    flag = np.zeros(12, bool)
    flag[4] = True                                             # rule fires at the close of bar 4 -> out at open of 5
    M = synth(prices=p, rule=(flag, np.zeros(12, bool)))
    S = sigs(M, [1], [1], [95.0])
    assert S["sa_kind"][0] == evc.K_RULE
    assert abs(S["sa_px"][0] - M.O1[M.first[5]]) < 1e-12
    assert S["sa_t"][0] == M.tmin[M.first[5]] + evc.MIN_NS


def test_add_breakeven_whole_position():
    # up from 100 to 110, pull back to 106 (add signal), then collapse: both legs stopped -> whole position nets $0
    p = list(np.linspace(100, 110, 25)) + list(np.linspace(110, 106, 10)) + [106.0] * 5 + \
        list(np.linspace(106, 90, 20))
    M = synth(prices=p)
    i_add = 6                                                  # entry bar 7: open = p[35] = 106
    S = sigs(M, [0, i_add], [1, 1], [95.0, 105.0])
    L, cnt = evc.walk_book(M, S, "add1", ("fixed", 1))
    D = pd.DataFrame(L)
    assert cnt["adds"] == 1 and len(D) == 2 and D.moved.iloc[0]
    tot = float((D.micros * D.pnl_usd).sum())
    assert abs(tot) < 1e-9, tot
    # expected moved stop: avg + (tick + cost/usd) + (1/1)*((106 - 103) + tick + cost/usd)
    e0, e1 = M.Ob[1], M.Ob[i_add + 1]
    c = 0.25 + 2.0 / 2.0
    assert abs(D.stop_last.iloc[0] - (e0 + c + (e1 - 105.0) + c)) < 1e-9
    # same-size add with 3 micros: ratio 1 -> the same stop; total still $0
    L, _ = evc.walk_book(M, S, "addsame", ("fixed", 3))
    D = pd.DataFrame(L)
    assert list(D.micros) == [3, 3] and abs(float((D.micros * D.pnl_usd).sum())) < 1e-9


def test_add_skipped_when_underwater_or_capped():
    p = list(np.linspace(100, 98, 30)) + [98.0] * 30
    M = synth(prices=p)
    S = sigs(M, [0, 3], [1, 1], [95.0, 96.0])
    L, cnt = evc.walk_book(M, S, "add1", ("fixed", 1))
    assert cnt["adds"] == 0 and cnt["add_cushion"] == 1 and len(L["gid"]) == 1
    p = list(np.linspace(100, 120, 60))
    M = synth(prices=p)
    S = sigs(M, [0, 3, 6], [1, 1, 1], [95.0, 101.0, 104.0])
    L, cnt = evc.walk_book(M, S, "addsame", ("fixed", 15))
    D = pd.DataFrame(L)
    assert list(D.micros) == [15, 5] and cnt["add_cap"] == 1


def test_walker_matches_hand_walk_random():
    bad = 0
    for seed in range(12):
        rng = np.random.default_rng(seed)
        flag = (rng.random((2, 200)) < 0.04)
        M = synth(seed=seed, rule=(flag[0], flag[1]) if seed % 2 else None)
        i = np.sort(rng.choice(np.arange(5, 190), 60, replace=False))
        d = np.where(rng.random(60) < 0.6, 1, -1)
        e = M.Ob[i + 1]
        stop = e - d * np.round(rng.uniform(0.5, 4, 60) * 4) / 4
        S = sigs(M, i, d, stop, score=rng.random(60))
        for mode, pol in (("add1", ("fixed", 1)), ("addsame", ("fixed", 2)), ("add1", ("fixed", 4))):
            L, _ = evc.walk_book(M, S, mode, pol)
            D = pd.DataFrame(L)
            for g, P in D.groupby("gid"):
                k0 = int(np.flatnonzero(S["key"] == P.key.iloc[0])[0])
                hw = evc.hand_walk_position(M, S, k0, int(P.micros.iloc[0]), mode)
                tot_h = sum(q * x for _, q, x in hw)
                tot_w = float((P.micros * P.pnl_usd).sum())
                bad += int(abs(tot_h - tot_w) > 1e-9 or len(hw) != len(P))
    assert bad == 0, bad


def test_none_mode_book_equals_eval_sim():
    rng = np.random.default_rng(3)
    M = synth(seed=3)
    i = np.sort(rng.choice(np.arange(5, 190), 80, replace=False))
    d = np.where(rng.random(80) < 0.5, 1, -1)
    stop = M.Ob[i + 1] - d * np.round(rng.uniform(0.5, 3, 80) * 4) / 4
    S = sigs(M, i, d, stop)
    L, cnt = evc.walk_book(M, S, "none", ("fixed", 3))
    D = pd.DataFrame(L)
    assert cnt["busy"] > 0 and (D.t_entry.to_numpy()[1:] >= D.t_exit.to_numpy()[:-1] - evc.MIN_NS).all()
    taken, _ = evc.book(D.t_entry.to_numpy(), D.t_exit.to_numpy(), D.sess.to_numpy(), D.micros.to_numpy(),
                        D.pnl_usd.to_numpy(), D.gid.to_numpy(), D.is_add.to_numpy(), dll=5.0)
    T = pd.DataFrame({"market": "NQ", "t_entry": pd.to_datetime(D.t_entry), "t_exit": pd.to_datetime(D.t_exit),
                      "risk_usd": D.risk_usd, "pnl_usd": D.pnl_usd, "session": pd.to_datetime(D.sess)})
    s = es.size_trades(T, ("fixed", 3), dll=5.0)
    assert np.array_equal(taken, s.micros.to_numpy()), (taken, s.micros.to_numpy())


def test_book_cross_market_cap_and_dead_groups():
    te = np.array([0, 1, 2, 3]) * evc.MIN_NS
    tx = np.array([10, 10, 10, 10]) * evc.MIN_NS
    sess = np.zeros(4, np.int64)
    want = np.array([15, 15, 2, 1])
    pnl = np.ones(4)
    gid = np.array([0, 10 ** 7, 10 ** 7, 1])
    is_add = np.array([False, False, True, True])
    taken, approx = evc.book(te, tx, sess, want, pnl, gid, is_add)
    # base 15; second market base gets 5 (cap); its add finds the cap full (approx); market-1 add finds the cap full
    assert list(taken) == [15, 5, 0, 0] and approx == 2


def test_truncation_synthetic():
    rng = np.random.default_rng(9)
    flag = rng.random((2, 200)) < 0.05
    M = synth(seed=9, rule=(flag[0], flag[1]))
    i = np.sort(rng.choice(np.arange(5, 190), 70, replace=False))
    d = np.where(rng.random(70) < 0.6, 1, -1)
    stop = M.Ob[i + 1] - d * np.round(rng.uniform(0.5, 3, 70) * 4) / 4
    sc = rng.random(70)
    S = sigs(M, i, d, stop, score=sc)
    cut_row = 520
    Mt = synth(seed=9, rule=(flag[0], flag[1]))
    for a in ("O1", "H1", "L1", "C1"):
        x = getattr(Mt, a).copy()
        x[cut_row:] = np.nan
        setattr(Mt, a, x)
    keep = M.first[i + 1] < cut_row
    St = sigs(Mt, i[keep], d[keep], stop[keep], score=sc[keep])
    ct = M.tmin[cut_row]
    for mode in evc.MODES:
        A = pd.DataFrame(evc.walk_book(M, S, mode, ("fixed", 1))[0])
        B = pd.DataFrame(evc.walk_book(Mt, St, mode, ("fixed", 1))[0])
        done = A.groupby("gid").t_exit.max() <= ct
        a = A[A.gid.isin(done[done].index)]
        b = B[B.gid.isin(a.gid.unique())]
        assert len(a) > 3 and len(a) == len(b)
        assert np.allclose(a.pnl_usd.to_numpy(), b.pnl_usd.to_numpy())
        assert np.array_equal(a.t_exit.to_numpy(), b.t_exit.to_numpy())


def test_eval_book_robust_windows():
    cal = pd.bdate_range("2013-01-01", "2025-06-30")
    rng = np.random.default_rng(0)
    sess = rng.choice(cal, 3000)
    pnl = rng.normal(5, 150, 3000)
    E = evc.eval_book(sess.astype("datetime64[ns]"), pnl, cal)
    assert set(E.window) == {"2013+", "2018+", "2022+", "2013-24", "2013+ -top10"}
    raw = pd.Series(pnl, index=pd.DatetimeIndex(sess)).groupby(level=0).sum()
    assert abs(E[E.window == "2013+"].worst_day_raw.iloc[0] - raw.min()) < 1e-6


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} tests passed")
