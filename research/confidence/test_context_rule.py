"""Hand-made bar checks for context_rule.prior_move / strong_flags.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_context_rule.py"""
import numpy as np
import pandas as pd

import context_rule as cr
import signals as sg


def frame(C, run=None, ema=None, H=None, L=None):
    C = np.asarray(C, float)
    n = len(C)
    idx = pd.date_range("2020-01-06 09:30", periods=n, freq="15min")
    b = pd.DataFrame({"O": C, "H": C + 0.5 if H is None else np.asarray(H, float),
                      "L": C - 0.5 if L is None else np.asarray(L, float), "C": C, "V": 1.0, "vwap": C,
                      "run": np.zeros(n, int) if run is None else np.asarray(run)}, index=idx)
    ctx = pd.DataFrame({"ema10": C.copy() if ema is None else np.asarray(ema, float)}, index=idx)
    return b, ctx


R1 = lambda n: np.ones(n)
DECL = 20 - 0.5 * np.arange(13)          # steady decline: C[11] = 14.5, max H of bars 2..11 = 19.5 -> 5 R20 below


def test_decline_true():
    b, ctx = frame(DECL)
    for X in (1.5, 3.0):
        m = cr.prior_move(b, ctx, 1, X=X, N=10, R=R1(13))
        assert m[12], X
        assert not m[:10].any()                     # windows not complete yet (needs bar t-10 in the run)
    assert not cr.prior_move(b, ctx, 1, X=6.0, N=10, R=R1(13))[12]   # move 5 < 6
    assert not cr.prior_move(b, ctx, -1, X=1.5, N=10, R=R1(13))[12]  # no rise for a bearish pattern


def test_threshold_between():
    C = 20 - 0.25 * np.arange(13)        # C[11] = 17.25, max H bars 2..11 = 20.0 -> 2.75 R20
    b, ctx = frame(C)
    assert cr.prior_move(b, ctx, 1, X=1.5, R=R1(13))[12]
    assert not cr.prior_move(b, ctx, 1, X=3.0, R=R1(13))[12]
    # R20 = 2 -> 1.375 R20: fails 1.5 (and 0.5-R20 near rule still holds)
    assert not cr.prior_move(b, ctx, 1, X=1.5, R=2 * R1(13))[12]


def test_ema_not_falling():
    ema = DECL.copy(); ema[8:12] = [10, 10.1, 10.2, 10.3]      # EMA10[11] > EMA10[8]
    b, ctx = frame(DECL, ema=ema)
    assert not cr.prior_move(b, ctx, 1, X=1.5, R=R1(13))[12]
    ema[11] = 9.9                                                # now EMA10[11] < EMA10[8] -> falling
    b, ctx = frame(DECL, ema=ema)
    assert cr.prior_move(b, ctx, 1, X=1.5, R=R1(13))[12]


def test_not_near_low():
    C = DECL.copy(); C[12] = 16.0                         # pattern bar low 15.5, 10-bar low = 13.5 (bar 11)
    b, ctx = frame(C, ema=DECL)
    assert not cr.prior_move(b, ctx, 1, X=1.5, R=R1(13))[12]
    L = C - 0.5; L[12] = 13.9                              # long lower tail back near the low: gap 0.4 <= 0.5
    b, ctx = frame(C, ema=DECL, L=L)
    assert cr.prior_move(b, ctx, 1, X=1.5, R=R1(13))[12]
    # two-bar pattern: span 2 uses min(L[11], L[12]) = 13.5 -> at the low
    b, ctx = frame(C, ema=DECL)
    assert cr.prior_move(b, ctx, 1, X=1.5, R=R1(13), span=2)[12]


def test_run_break():
    run = np.zeros(13, int); run[5:] = 1                   # contract roll inside the 10-bar window
    b, ctx = frame(DECL, run=run)
    assert not cr.prior_move(b, ctx, 1, X=1.5, R=R1(13))[12]


def test_lag2_three_bar():
    # morning star: reference bar = t-2 (bar 10, C 15), N bars 1..10 -> max H 20.0 -> 5 R20
    C = DECL.copy(); C[11] = 14.4; C[12] = 15.2
    b, ctx = frame(C, ema=DECL)
    m = cr.prior_move(b, ctx, 1, X=3.0, N=10, lag=2, span=3, R=R1(13))
    assert m[12]
    assert not cr.prior_move(b, ctx, 1, X=5.5, N=10, lag=2, span=3, R=R1(13))[12]


def test_mirror():
    rng = np.random.default_rng(1)
    C = 100 + np.cumsum(rng.normal(0, 1, 400))
    H = C + rng.uniform(0, 1, 400); L = C - rng.uniform(0, 1, 400)
    b, ctx = frame(C, H=H, L=L)
    bm, cm = frame(-C, H=-L, L=-H)
    for X in (1.5, 3.0):
        for lag, span in ((1, 1), (1, 2), (2, 3)):
            a = cr.prior_move(b, ctx, 1, X=X, lag=lag, span=span, R=R1(400))
            m = cr.prior_move(bm, cm, -1, X=X, lag=lag, span=span, R=R1(400))
            assert (a == m).all() and a.any()


def test_no_lookahead():
    rng = np.random.default_rng(2)
    n = 600
    C = 100 + np.cumsum(rng.normal(0, 1, n))
    H = C + rng.uniform(0, 1, n); L = C - rng.uniform(0, 1, n)
    b, _ = frame(C, H=H, L=L)
    ctx = sg.context(b)
    t = 400
    b2 = b.copy()
    b2.iloc[t + 1:, :4] = b2.iloc[t + 1:, :4] * 0 + 50 + rng.normal(0, 5, (n - t - 1, 1))
    b2["H"] = b2[["O", "H", "C"]].max(axis=1); b2["L"] = b2[["O", "L", "C"]].min(axis=1)
    ctx2 = sg.context(b2)
    for d in (1, -1):
        for X in (1.5, 3.0):
            for lag, span in ((1, 1), (1, 2), (2, 3)):
                a = cr.prior_move(b, ctx, d, X=X, lag=lag, span=span)
                c = cr.prior_move(b2, ctx2, d, X=X, lag=lag, span=span)
                assert (a[:t + 1] == c[:t + 1]).all()


def test_strong_flags():
    b, ctx = frame(DECL)
    cols = {f"pat_{p}": np.zeros(4) for p in cr.REVERSAL}
    cols["pat_marubozu"] = np.zeros(4)
    E = pd.DataFrame({"i": [12, 12, 12, 11], "d": [1, -1, 1, 1], **cols})
    E.loc[0, "pat_hammer"] = 1                 # bullish hammer after a decline -> strong
    E.loc[1, "pat_hanging_man"] = -1           # bearish hanging man with no rise -> reversal, not strong
    E.loc[2, "pat_marubozu"] = 1               # not a reversal pattern
    E.loc[3, "pat_engulfing"] = -1             # fired against the event's direction -> ignored
    rev, st = cr.strong_flags(b, ctx, E, X=1.5, R=R1(13))
    assert rev.tolist() == [True, True, False, False]
    assert st.tolist() == [True, False, False, False]


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f(); print("ok", k)
