"""
Synthetic-data tests for v2/luck_baseline.py (no market data). Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_luck_baseline.py
"""
import numpy as np
import pandas as pd

import labels as lb
import luck_baseline as lk


def _bars(n_days=12, tf=60, seed=0):
    """Hourly-ish bars 18:00 -> 16:00 next day per session (23 bars incl. the 16:00 tail bar), one contract."""
    rng = np.random.default_rng(seed)
    idx, sess = [], []
    for k, day in enumerate(pd.bdate_range("2021-03-01", periods=n_days)):
        start = day - pd.Timedelta(hours=6)
        for h in range(23):
            idx.append(start + pd.Timedelta(minutes=tf * h))
            sess.append(k)
    n = len(idx)
    C = 4000 + np.cumsum(rng.normal(0, 4, n)).round(2)
    C = np.round(C * 4) / 4
    O = np.r_[C[0], C[:-1]]
    H = np.maximum(O, C) + np.round(rng.uniform(0, 6, n) * 4) / 4
    L = np.minimum(O, C) - np.round(rng.uniform(0, 6, n) * 4) / 4
    b = pd.DataFrame({"O": O, "H": H, "L": L, "C": C, "inst": 1, "sess": sess}, index=pd.DatetimeIndex(idx))
    b["seg"] = (b.sess.ne(b.sess.shift()) | b.inst.ne(b.inst.shift())).cumsum()
    b["run"] = 1
    return b


def test_stops_truncation_and_distance():
    b = _bars()
    sl, ss, ok = lk.luck_stops(b, 0.25)
    for cut in (30, 77, 150, 200):
        a, c, v = lk.luck_stops(b.iloc[:cut + 1], 0.25)
        assert np.array_equal(v, ok[:cut + 1])
        m = ok[:cut + 1]
        assert np.allclose(a[m], sl[:cut + 1][m]) and np.allclose(c[m], ss[:cut + 1][m])
    C, L, H = b.C.to_numpy(), b.L.to_numpy(), b.H.to_numpy()
    i = np.flatnonzero(ok)
    assert (sl[i] <= np.minimum.reduce([L[i - k] for k in range(5)]) - 0.25 + 1e-9).all()
    assert (ss[i] >= np.maximum.reduce([H[i - k] for k in range(5)]) + 0.25 - 1e-9).all()
    assert (sl[i] < C[i]).all() and (ss[i] > C[i]).all()


def test_pool_events_only_eligible_bars():
    b = _bars()
    ev = lk.pool_events(b, 60, 0.25, per_day=4, seed=1)
    ok, _ = lb.eligible(b, 60)
    assert ok[ev.i].all()
    assert set(ev.groupby("i").d.apply(lambda s: tuple(sorted(s)))) == {(-1, 1)}
    n_days = ev.t.dt.normalize().nunique()
    assert abs(len(ev) / 2 - 4 * 12) <= 1 and n_days > 5


def test_draw_deterministic_and_rate():
    n = 20000
    pool = pd.DataFrame({"market": "ES", "tf": 60, "i": np.repeat(np.arange(n), 2), "d": np.tile([1, -1], n)})
    a = lk.draw(pool, 1.0, "random", 0, per_day=8)
    b = lk.draw(pool, 1.0, "random", 0, per_day=8)
    c = lk.draw(pool, 1.0, "random", 1, per_day=8)
    assert a.equals(b) and not a.equals(c)
    assert abs(len(a) / n - 1 / 8) < 0.01 and abs((a.d > 0).mean() - 0.5) < 0.03
    assert a.i.is_unique                                         # one direction per bar
    lo = lk.draw(pool, 3.0, "long", 0, per_day=8)
    assert (lo.d == 1).all() and abs(len(lo) / n - 3 / 8) < 0.015


def test_lucid_session_frame():
    import lucid
    # one session 18:00 .. 17:15 (old CME schedule): 15-min bars
    idx = pd.date_range("2012-03-04 18:00", "2012-03-05 17:15", freq="15min")
    b = pd.DataFrame({"seg": 1}, index=idx)
    al, fo = lucid.session_frame(b, 15)
    m = idx.hour * 60 + idx.minute
    assert not al[(m >= 1005) & (m < 1080)].any() and al[m < 1005].all()
    assert idx[fo[0]] == pd.Timestamp("2012-03-05 16:30")                # last bar closing by 16:45
    al60, fo60 = lucid.session_frame(pd.DataFrame({"seg": 1}, index=idx[::4]), 60)
    assert idx[::4][fo60[0]] == pd.Timestamp("2012-03-05 15:00")
    _, fo_old = lucid._ORIG(b, 15)
    assert idx[fo_old[0]] == pd.Timestamp("2012-03-05 17:15")            # the old frame let it run to 17:30
    lucid.install()
    assert lb.eligible(b.assign(seg=1), 15)[1][0] == fo[0]
    ok, _ = lb.eligible(b, 15)
    assert not ok[(m >= 990) & (m < 1080)].any()                          # no entry after the 16:30 bar's open


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_") and callable(f):
            f()
            print("ok", name)
    print("all passed")
