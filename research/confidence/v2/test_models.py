"""Synthetic tests for v2/models.py.
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_models.py
"""
import numpy as np
import pandas as pd

import dataset as ds
import models as M
import walkforward as wf


def synth(n_days=2600, per_day=6, seed=0, edge_col="sig_trend60"):
    """Fake pooled event table 2010-01 .. 2017: random features; R depends on one agree signal and on cost_R."""
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("2010-01-04", periods=n_days)
    days = days[days < "2018-01-01"]
    rows = []
    for k, dday in enumerate(days):
        for j in range(per_day):
            t = dday + pd.Timedelta(hours=9, minutes=15 * j)
            rows.append((t, ["NQ", "ES", "YM"][j % 3], 1 if j % 2 == 0 else -1))
    D = pd.DataFrame(rows, columns=["t", "market", "d"])
    n = len(D)
    for c in ds.feature_columns() + ds.FLAGS + ["n_rules"]:
        D[c] = rng.normal(size=n).astype(np.float32)
    for c in ("m5_trend", "m15_trend", "m60_trend", "m15_struct", "m60_struct"):
        D[c] = rng.integers(-1, 2, n).astype(np.float32)
    D["cost_R"] = rng.uniform(0, 0.3, n).astype(np.float32)
    D["mkt_ES"] = (D.market == "ES").astype(np.float32)
    D["mkt_YM"] = (D.market == "YM").astype(np.float32)
    D = pd.concat([D, M.signal_frame(D)], axis=1)
    R = rng.normal(-0.05, 1.0, n) + 0.4 * (D[edge_col].to_numpy() != 0) - 1.0 * D.cost_R.to_numpy()
    x = "hold"
    D[f"R_{x}"] = R
    D["risk_usd"] = 50.0
    D[f"pnl_{x}"] = R * 50
    D[f"t_exit_{x}"] = D.t + pd.Timedelta(minutes=30)
    D["session"] = wf.session_label(D.t)
    D["year"] = pd.DatetimeIndex(D.session).year
    D["nm_hold"] = 0.0
    D["rs_hold"] = 0.0
    return D


FOLDS = wf.make_folds(test_years=range(2013, 2018), h1_2025=False)


def test_signal_frame_signs():
    E = pd.DataFrame({c: [0.0, 0.0] for c in ds.feature_columns() + ["n_rules"]})
    E.loc[0, "m60_trend"] = 1
    E.loc[1, "m60_trend"] = -1
    S = M.signal_frame(E)
    assert S.loc[0, "sig_trend60"] == 1 and S.loc[0, "sig_x_trend60"] == 0
    assert S.loc[1, "sig_trend60"] == 0 and S.loc[1, "sig_x_trend60"] == -1
    assert len(M.SIGNALS) == 25 and set(np.unique(S.to_numpy())) <= {-1.0, 0.0, 1.0}


def test_sign_constraint():
    """A column that truly hurts gets weight exactly 0 under a >= 0 bound (and a negative one without it)."""
    rng = np.random.default_rng(1)
    X = rng.integers(0, 2, (5000, 3)).astype(float)
    y = (rng.random(5000) < 1 / (1 + np.exp(-(0.8 * X[:, 0] - 0.8 * X[:, 1])))).astype(float)
    m = M.LinScore("cls", 1e-4, [(0, None)] * 3).fit(X, y, np.ones(5000))
    assert m.coef_[0] > 0.5 and abs(m.coef_[1]) < 1e-8 and m.coef_[2] >= 0
    u = M.LinScore("cls", 1e-4, [(None, None)] * 3).fit(X, y, np.ones(5000))
    assert u.coef_[1] < -0.5
    r = M.LinScore("reg", 1e-4, [(0, None)] * 3).fit(X, 0.8 * X[:, 0] - 0.8 * X[:, 1] + rng.normal(0, .1, 5000),
                                                     np.ones(5000))
    assert r.coef_[0] > 0.7 and abs(r.coef_[1]) < 1e-8


def test_monotone_hgb():
    rng = np.random.default_rng(2)
    D = synth(n_days=900)
    cols = M.raw_features()
    X = M.tree_matrix(D, cols)
    y = (D.R_hold.to_numpy() > 0).astype(float)
    m = M.hgb("cls", 100, M.mono_vector(cols), 50).fit(X, y)
    j = cols.index("m60_trend")
    Xa = X[:500].copy()
    lo, hi = Xa.copy(), Xa.copy()
    lo[:, j], hi[:, j] = -1, 1
    assert (M.hgb_predict(m, hi) >= M.hgb_predict(m, lo) - 1e-12).all()
    k = cols.index("cost_R")
    lo, hi = Xa.copy(), Xa.copy()
    lo[:, k], hi[:, k] = 0.0, 0.5
    assert (M.hgb_predict(m, hi) <= M.hgb_predict(m, lo) + 1e-12).all()


def test_choose_keep_and_threshold():
    s = np.arange(10.0)
    r = np.r_[-np.ones(8), 5, 5]                      # the top 2 rows are the good ones
    q, v = M.choose_keep(s, r, grid=(0.2, 0.5, 1.0))
    assert q == 0.2 and v == 5
    assert M.threshold_for(np.arange(100.0), 1.0) == -np.inf
    assert abs(M.threshold_for(np.arange(101.0), 0.2) - 80) < 1e-9


def test_walk_finds_planted_signal():
    D = synth()
    for model in ("M1", "M2", "M3"):
        s, k, inf = M.walk(D, 60, "hold", model, "cls", folds=FOLDS, verbose=False)
        test = np.isfinite(s)
        kept = D.R_hold.to_numpy()[k].mean()
        allr = D.R_hold.to_numpy()[test].mean()
        assert kept > allr + 0.1, (model, kept, allr)
        assert all(i["n_train"] > 0 for i in inf)
    sM0, kM0, _ = M.walk(D, 60, "hold", "M0", "cls", folds=FOLDS, verbose=False)
    assert np.allclose(sM0[np.isfinite(sM0)], D[M.SIG_COLS].to_numpy().sum(1)[np.isfinite(sM0)])


def test_purge_and_training_rows():
    """Training rows of a fold end at least a day before the test start (wf.train_mask) - checked via a planted
    label that is only learnable from test-year rows: scores must not use it."""
    D = synth(seed=3)
    s1, _, _ = M.walk(D, 60, "hold", "M1", "cls", folds=FOLDS, verbose=False)
    D2 = D.copy()
    m = pd.DatetimeIndex(D2.t).year == 2016
    D2.loc[m, "R_hold"] = 10.0 * D2.loc[m, "sig_x_trend5"].to_numpy()   # rewrite 2016 labels only
    s2, _, _ = M.walk(D2, 60, "hold", "M1", "cls", folds=FOLDS, verbose=False)
    yr = pd.DatetimeIndex(D.t).year
    assert np.allclose(s1[yr <= 2016], s2[yr <= 2016], equal_nan=True)
    assert not np.allclose(s1[yr == 2017], s2[yr == 2017], equal_nan=True)


def test_truncation():
    """Cutting the data after time T changes nothing at or before T."""
    D = synth(seed=4)
    cut = pd.Timestamp("2016-07-01")
    for model, target in (("M0", "cls"), ("M1", "reg"), ("M2", "cls"), ("M3", "reg")):
        s1, k1, _ = M.walk(D, 60, "hold", model, target, folds=FOLDS, verbose=False)
        D2 = D[D.t < cut].copy()
        s2, k2, _ = M.walk(D2, 60, "hold", model, target, folds=FOLDS, verbose=False)
        n = len(D2)
        assert np.allclose(s1[:n], s2, equal_nan=True), model
        assert (k1[:n] == k2).all(), model


def test_holdout_refused():
    D = synth(n_days=900)
    D.loc[D.index[-1], "t_exit_hold"] = pd.Timestamp("2025-07-02 10:00")
    try:
        M.walk(D, 60, "hold", "M1", "cls", folds=FOLDS, verbose=False)
    except wf.HoldoutError:
        return
    raise AssertionError("holdout row accepted")


def test_report_spans_and_rskip():
    D = synth(n_days=1500)
    D["d"] = 1
    D["tod_block"] = "09_11"
    take = np.zeros(len(D), bool)
    take[np.flatnonzero(pd.DatetimeIndex(D.t).year >= 2013)[:30]] = True
    rows = M.report(D, take, "hold", dict(cfg="x"))
    a = {(r["market"], r["side"], r["span"]): r for r in rows}
    assert a[("pooled", "all", "all")]["n"] == 30
    assert abs(a[("pooled", "all", "all")]["usd"] - D.pnl_hold.to_numpy()[take].mean()) < 1e-9
    assert a[("pooled", "all", "all w/o top 10 days")]["n"] < 30
    assert M.span_years("all", pd.Timestamp("2010-01-01")) == 12.5
    assert M.span_years("all", pd.Timestamp("2018-01-02")) < 7.5 + 1e-9


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            print("ok", k, flush=True)
    print("all tests passed")
