"""
Unit tests for v2/eval_sim.py on hand-made data (no market data loaded). Run from research/confidence:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_eval_sim.py
"""
import numpy as np
import pandas as pd

import eval_sim as es
import prop_sim as ps

CAL = pd.bdate_range("2020-01-02", periods=60)


def _daily(vals, start="2020-01-02"):
    return pd.Series(np.asarray(vals, float), index=pd.bdate_range(start, periods=len(vals)))


def _one(vals, cons=0.40, dll=600.0):
    """Outcome and days of the account started on day 0."""
    v = np.maximum(np.asarray(vals, float), -dll) if dll else np.asarray(vals, float)
    o, d = ps.run_starts(v, [0], ps.Rules(dll=dll, consistency=cons))
    return int(o[0]), int(d[0])


# ------------------------------------------------------------------------------------------------ prop rules
def test_pass_steady():
    # 5 days of +300: profit 1,500 >= 1,250, best day 300 <= 40% x 1,500 = 600 -> pass on day 5 (1,250 reached at 1,500)
    assert _one([300] * 6) == (ps.OUT_PASS, 5)


def test_consistency_block():
    # +1,250 on day 1: target reached but best day 1,250 > 40% x 1,250 -> no pass yet. Needs profit >= 1,250/0.4 = 3,125
    vals = [1250] + [100] * 30
    o, d = _one(vals)
    # profit after k extra days = 1250 + 100k >= 3125 -> k = 19 (3,150) -> day 20
    assert (o, d) == (ps.OUT_PASS, 20)
    # 50% consistency: profit >= 2,500 -> k = 13 -> day 14
    assert _one(vals, cons=0.50) == (ps.OUT_PASS, 14)
    # no rule: pass on day 1
    assert _one(vals, cons=None) == (ps.OUT_PASS, 1)


def test_trailing_bust():
    # up 900 (high 25,900, floor 24,900), then -999 -> 24,901 ok, then -1 -> 24,900 <= floor -> fail on day 4
    assert _one([500, 400, -999, -1, 0], dll=None) == (ps.OUT_FAIL, 4)
    # with the 600 daily limit the -999 day is floored at -600: 25,300; then -1 -> 25,299 (floor 24,900): still open
    assert _one([500, 400, -999, -1, 0], dll=600.0) == (ps.OUT_OPEN, 5)


def test_lock_at_25100():
    # close at 26,150 (> 26,100) locks the floor at 25,100 (not 26,150 - 1,000 = 25,150)
    # days: +450 x 2 = 25,900 ... need best day <= 40% to avoid passing: use 3 days of 400 then +50 -> 26,250
    # profit 1,250 at 26,250 with best 400 <= 500 -> that would pass; so stop just below target: 26,150 (profit 1,150)
    vals = [400, 400, 350, -590, -460]          # 26,150 locked; 25,560; 25,100 -> fail (<= 25,100) on day 5
    assert _one(vals) == (ps.OUT_FAIL, 5)
    vals2 = [400, 400, 350, -590, -459]         # 25,101 > 25,100 -> still open (a trailing floor would be 25,150)
    assert _one(vals2) == (ps.OUT_OPEN, 5)
    vals3 = [400, 400, 299, -590, -459]         # high 26,099: NOT locked, floor 25,099; balance 25,050 -> fail
    assert _one(vals3) == (ps.OUT_FAIL, 5)


def test_daily_limit_floor():
    # a -900 day counts as -600 (soft daily limit): 25,000 -> 24,400 > 24,000 floor -> open; without dll -> 24,100
    assert _one([-900], dll=600.0) == (ps.OUT_OPEN, 1)
    assert _one([-900, -350], dll=600.0) == (ps.OUT_OPEN, 2)    # 24,050 > 24,000
    assert _one([-900, -400], dll=600.0) == (ps.OUT_FAIL, 2)    # 24,000 <= 24,000


def test_eval_daily_metrics():
    d = _daily([300] * 40)
    e = es.eval_daily(d, consistencies=(0.4,), windows={"w": ("2020-01-01", "2030-01-01")})
    r = e.iloc[0]
    # every start with >= 5 days left passes on its 5th day; the last 4 starts stay open
    assert r.n_starts == 40 and r.days_pass_median == 5
    assert abs(r.pass_pct - 100 * 36 / 40) < 1e-9 and abs(r.open_pct - 10) < 1e-9 and r.fail_pct == 0
    assert r.within_5 == 100 and r.within_10 == 100 and r.within_20 == 100 and r.pass_rate == 100
    # matches prop_sim.simulate's pass rate on the same series
    s = ps.simulate(d, ps.Rules(dll=600, consistency=0.4), start_from="2020-01-01", eras={})
    assert abs(s["pass_rate"] * 100 - r.pass_rate) < 1e-9 and s["n_open"] == 4


# ------------------------------------------------------------------------------------------------ sizing
def _T(rows):
    """rows: (entry 'YYYY-mm-dd HH:MM', exit, risk_usd, pnl_usd)"""
    return pd.DataFrame([dict(market="ES", t_entry=pd.Timestamp(a), t_exit=pd.Timestamp(b), risk_usd=r, pnl_usd=p)
                         for a, b, r, p in rows])


def test_fixed_and_risk_sizing():
    T = _T([("2020-01-02 09:30", "2020-01-02 10:00", 60.0, 10.0),
            ("2020-01-02 11:00", "2020-01-02 12:00", 300.0, -5.0),
            ("2020-01-02 13:00", "2020-01-02 14:00", 0.0, -2.0)])
    s = es.size_trades(T, ("fixed", 3))
    assert s.micros.tolist() == [3, 3, 3] and s.pnl_total.tolist() == [30.0, -15.0, -6.0]
    s = es.size_trades(T, ("risk", 250))
    assert s.micros.tolist() == [4, 0, 0] and s.skip.tolist() == ["", "size0", "size0"]
    s = es.size_trades(T, ("risk", 400))
    assert s.micros.tolist() == [6, 1, 0]


def test_cap_20_open_micros():
    # three overlapping trades at 8 micros: 8, 8, then only 4 fit; after the first closes, 8 fit again
    T = _T([("2020-01-02 09:00", "2020-01-02 12:00", 10.0, 1.0),
            ("2020-01-02 09:30", "2020-01-02 12:00", 10.0, 1.0),
            ("2020-01-02 10:00", "2020-01-02 11:00", 10.0, 1.0),
            ("2020-01-02 10:30", "2020-01-02 12:00", 10.0, 1.0),
            ("2020-01-02 11:00", "2020-01-02 12:00", 10.0, 1.0)])     # entry at the 3rd's exit time: it is closed
    s = es.size_trades(T, ("risk", 80))
    assert s.micros.tolist() == [8, 8, 4, 0, 4] and s.skip.tolist()[3] == "cap"


def test_daily_loss_limit_stops_new_trades():
    T = _T([("2020-01-02 09:00", "2020-01-02 09:30", 100.0, -250.0),
            ("2020-01-02 09:40", "2020-01-02 10:00", 100.0, -400.0),     # realized -500 > -600: taken -> -900
            ("2020-01-02 10:30", "2020-01-02 11:00", 100.0, 500.0),      # realized -900 <= -600: skipped
            ("2020-01-02 18:30", "2020-01-03 09:00", 100.0, 50.0)])      # next session (01-03): taken
    s = es.size_trades(T, ("fixed", 1))
    assert s.micros.tolist() == [1, 1, 0, 1] and s.skip.tolist()[2] == "dll"
    d = es.daily_pnl(s, pd.DatetimeIndex(["2020-01-02", "2020-01-03", "2020-01-06"]))
    assert d.tolist() == [-600.0, 50.0, 0.0]                              # floored at -600, empty day = 0
    # a trade still OPEN when the limit is reached is not "realized": the next entry is still taken
    T2 = _T([("2020-01-02 09:00", "2020-01-02 11:00", 100.0, -700.0),
             ("2020-01-02 10:00", "2020-01-02 10:30", 100.0, 20.0),
             ("2020-01-02 11:30", "2020-01-02 12:00", 100.0, 20.0)])
    assert es.size_trades(T2, ("fixed", 1)).micros.tolist() == [1, 1, 0]


def test_sizing_uses_only_the_past():
    # truncation test: dropping every trade entered after time T never changes a decision at or before T
    rng = np.random.default_rng(1)
    rows = []
    for k in range(400):
        day = CAL[k // 8]
        a = day + pd.Timedelta(hours=9) + pd.Timedelta(minutes=int(rng.integers(0, 400)))
        b = min(a + pd.Timedelta(minutes=int(rng.integers(1, 300))), day + pd.Timedelta(hours=16, minutes=45))
        rows.append((str(a), str(b), float(rng.uniform(5, 300)), float(rng.normal(-5, 150))))
    T = _T(rows)
    for pol in [("fixed", 5), ("risk", 400), ("risk", 100)]:
        full = es.size_trades(T, pol)
        for cut in rng.choice(len(T), 15, replace=False):
            tcut = full.t_entry.iloc[cut]
            part = es.size_trades(T[T.t_entry <= tcut], pol)
            f = full[full.t_entry <= tcut]
            assert f.micros.tolist() == part.micros.tolist(), pol


def test_rejects_holdout_and_close_crossing():
    for bad in [_T([("2025-06-30 18:05", "2025-06-30 19:00", 10.0, 1.0)]),
                _T([("2020-01-02 15:00", "2020-01-02 17:10", 10.0, 1.0)]),
                _T([("2020-01-02 15:00", "2020-01-02 18:10", 10.0, 1.0)])]:
        try:
            es.prepare(bad)
        except ValueError:
            continue
        raise AssertionError("bad trade accepted")
    es.prepare(_T([("2020-01-02 18:05", "2020-01-03 16:45", 10.0, 1.0)]))   # evening entry held to 16:45: fine


def test_evaluate_end_to_end():
    # one +100 trade per day, 2 micros: +200/day -> passes on day 7 (1,400 >= 1,250; 200 <= 560)
    rows = [(str(d + pd.Timedelta(hours=10)), str(d + pd.Timedelta(hours=11)), 50.0, 100.0) for d in CAL]
    e = es.evaluate(_T(rows), CAL, policies=[("fixed", 2), ("risk", 100)], consistencies=(0.4,),
                    windows={"w": ("2020-01-01", "2021-01-01")})
    assert e.days_pass_median.tolist() == [7, 7] and e.trades_taken.tolist() == [60, 60]
    rep = es.pnl_report(_T(rows))
    assert rep.set_index("span").loc["all", "usd_trade"] == 100.0


if __name__ == "__main__":
    n = 0
    for name, f in list(globals().items()):
        if name.startswith("test_") and callable(f):
            f()
            n += 1
            print("ok", name)
    print(f"{n} tests passed")
