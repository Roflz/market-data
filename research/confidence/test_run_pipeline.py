"""Checks of run_pipeline.py's own pieces (the modules it calls have their own tests):
  * patterns_from_F reproduces signals.patterns exactly (the entry events are built from it);
  * the saved datasets never reach the locked holdout (signal bars, label ends, exit-trade bars);
  * stop_R20 / cost_R on a hand-made event; feature lists per scope;
  * concurrency() and the day-block bootstrap on hand-made series; upsert(); scorecard units.
Run: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_run_pipeline.py
"""
import os
import tempfile
import warnings

import numpy as np
import pandas as pd

import features as fe
import run_pipeline as rp
import signals as sg
import walkforward as wf

warnings.filterwarnings("ignore", category=RuntimeWarning)


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    assert cond, name


def test_patterns_from_F():
    b, F = fe.build_features("YM", 15)
    P = sg.patterns(b, b, tick=sg.SPEC["YM"]["tick"])
    Q = rp.patterns_from_F(F)
    check("patterns_from_F == signals.patterns (YM, every bar, every pattern)",
          all(np.array_equal(P[c].to_numpy(), Q[c].to_numpy()) for c in Q.columns))
    b2, F2 = rp.holdout_cut(b, F)
    check("holdout_cut: last bar before 2025-06-30 18:00, rows identical",
          b2.index.max() < wf.HOLDOUT_SESSION_START and F2.equals(F.loc[b2.index]))


def test_datasets_before_holdout():
    cut = wf.HOLDOUT_SESSION_START
    for s in rp.MARKETS:
        p = rp._path(f"entries_{s}_15.parquet")
        if not os.path.exists(p):
            print(f"skip {s}: no dataset"); continue
        e = pd.read_parquet(p, columns=["t", "t_entry"] + [f"t_end_{rp.lb._rkey(r)}" for r in rp.TARGET_R])
        x = pd.read_parquet(rp._path(f"exits_{s}_15.parquet"), columns=["t", "ts", "t_end"])
        ok = (e.max() < cut).all() and (x.max() < cut).all()
        check(f"{s}: entries and exit rows end before the holdout (max t_end {e.iloc[:, 2:].max().max()})", ok)


def test_trade_features_and_lists():
    idx = pd.date_range("2024-01-02 10:00", periods=3, freq="15min")
    b = pd.DataFrame({"C": [100.0, 101.0, 102.0], "R20": [2.0, 2.0, np.nan]}, index=idx)
    ev = pd.DataFrame({"i": [0, 1, 2], "d": [1, -1, 1], "stop": [99.0, 101.25, 101.0]})
    s, c = rp.entry_trade_features(b, ev, "ES")
    check("stop_R20: long 1 pt / R20 2 = 0.5; short 0.25 / 2 = 0.125; NaN R20 -> NaN",
          np.allclose(s[:2], [0.5, 0.125]) and np.isnan(s[2]))
    check("cost_R: $3.50 / ($5 x 1 pt) = 0.7; / ($5 x 0.25) = 2.8", np.allclose(c[:2], [0.7, 2.8]))
    fp = rp.feature_list("entry", "pooled")
    fx = rp.feature_list("exit", "ES")
    check("feature lists: pooled entry has all x_ columns + mkt_ + stop_R20/cost_R; ES exit has no x_ES_",
          all(f"x_{m}_ret" in fp for m in rp.MARKETS) and "mkt_YM" in fp and "cost_R" in fp
          and "x_ES_ret" not in fx and "x_NQ_ret" in fx and "mins_to_1645" in fx and "mkt_ES" not in fx)
    check("no duplicate feature names", len(set(fp)) == len(fp) and len(set(fx)) == len(fx))


def test_concurrency_bootstrap_upsert():
    t = pd.to_datetime(["2024-01-02 10:00", "2024-01-02 10:15", "2024-01-02 11:00", "2024-01-03 10:00"])
    e = pd.to_datetime(["2024-01-02 10:30", "2024-01-02 11:00", "2024-01-02 11:30", "2024-01-03 10:15"])
    mx, p95 = rp.concurrency(t, e)
    check("concurrency: 2 overlapping trades; one ending exactly when another starts is not overlap", mx == 2)
    import prop_sim as ps
    dates = pd.bdate_range("2020-01-01", periods=300)
    v = np.full(300, 50.0)
    pr = rp.block_bootstrap_pass(v, dates, ps.Rules(), 20, n_boot=5)
    base = rp._simulate(v, dates, ps.Rules(), eras=None)["pass_rate"]
    check(f"day-block bootstrap of a constant series = the series' own pass rate ({base:.3f})",
          np.allclose(pr, base))
    v2 = np.r_[np.full(150, -60.0), np.full(150, 60.0)]
    pr2 = rp.block_bootstrap_pass(v2, dates, ps.Rules(), 20, n_boot=30)
    check("day-block bootstrap: draws differ when the series has streaks", np.nanstd(pr2) > 0)
    with tempfile.TemporaryDirectory() as d:
        old = rp.OUT
        rp.OUT = d
        try:
            rp.upsert("x.csv", pd.DataFrame({"scope": ["a", "b"], "model": ["m", "m"], "v": [1, 2]}), ["scope", "model"])
            rp.upsert("x.csv", pd.DataFrame({"scope": ["a"], "model": ["m"], "v": [9]}), ["scope", "model"])
            x = pd.read_csv(os.path.join(d, "x.csv")).sort_values("scope")
            check("upsert replaces matching rows and keeps the rest", x.v.tolist() == [9, 2])
        finally:
            rp.OUT = old


def test_scorecard_units():
    wt = pd.DataFrame({"feature": ["mins_to_1645", "pat_hammer", "(intercept)"],
                       "coef_raw_median": [0.002, wf.POINT * 10, -1.0], "coef_std_median": [0.3, 0.1, -1.0],
                       "sign_stability": [1.0, 0.8, 1.0], "share_pos": [1.0, 0.8, 0.0], "n_folds": [13, 13, 13]})
    sc = rp.scorecard_table(wt, "exit")
    m = sc.set_index("feature")
    check("scorecard: mins_to_1645 in points per HOUR (0.002 x 60 / (ln2/20) = 3)", m.loc["mins_to_1645", "points"] == 3)
    check("scorecard: pattern 10 points per firing; intercept last", m.loc["pat_hammer", "points"] == 10
          and sc.feature.iloc[-1] == "(intercept)")
    check("every SIGNED feature has a meaning and unit",
          all(rp.meaning(f) != f and rp.unit_words(f) for f in rp.feature_list("exit", "pooled")))


if __name__ == "__main__":
    for fn in [test_trade_features_and_lists, test_concurrency_bootstrap_upsert, test_scorecard_units,
               test_datasets_before_holdout, test_patterns_from_F]:
        print(f"--- {fn.__name__}")
        fn()
    print("ALL PASS")
