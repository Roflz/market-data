"""
Tests for stop_chooser.py (synthetic data only; no market data is loaded).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_stop_chooser.py
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")    # the machine is shared: oversubscribed OpenMP is ~40x slower
import numpy as np
import pandas as pd

import stop_chooser as sc
import walkforward as wf

FOLDS = wf.make_folds(test_years=(2013, 2014, 2015, 2016), h1_2025=False)
FAST = dict(max_depth=3, learning_rate=0.1, max_iter=80, l2_regularization=1.0, min_samples_leaf=50,
            early_stopping=False, random_state=0)
OPTS = ["tight", "wide", "fixed"]


def synth(n=14000, signal=True, seed=0, start="2010-01-01", end="2016-12-31"):
    """3 stop options. signal: option 0 pays -1 + 3 x1, option 1 pays -1 - 3 x1, option 2 pays -1.5 (+ noise sd 3),
    so the best option depends on the sign of feature x1 and no fixed option is good. noise: every option's $ is
    -1 + noise sd 5, independent of every feature."""
    rng = np.random.default_rng(seed)
    a, b = pd.Timestamp(start).value, pd.Timestamp(end).value
    t = pd.DatetimeIndex(np.sort(rng.integers(a, b, n))).floor("15min")
    te = t + pd.Timedelta(hours=2)
    X = rng.normal(size=(n, 5)).astype(np.float32)
    Xopt = np.stack([np.stack([np.full(n, s) + rng.normal(0, .1, n), rng.normal(size=n)], axis=1)
                     for s in (0.5, 2.0, 1.0)], axis=1).astype(np.float32)
    if signal:
        x1 = X[:, 0]
        P = np.stack([-1 + 3 * x1, -1 - 3 * x1, np.full(n, -1.5)], axis=1) + rng.normal(0, 3, (n, 3))
    else:
        P = -1 + rng.normal(0, 5, (n, 3))
    return X, Xopt, P, t, te


def run(method, model, signal, seed=0):
    X, Xopt, P, t, te = synth(signal=signal, seed=seed)
    cfg = sc.Config(method=method, model=model, hgb=dict(FAST), n_random=100)
    O, F = sc.run_chooser(X, Xopt, P, t, te, cfg=cfg, folds=FOLDS)
    T = sc.evaluate(O, F, OPTS, cfg.name, n_random=100)
    return X, O, F, T


def pooled(T, strat, col="usd_per_trade"):
    return float(T.loc[(T.period == "pooled") & (T.strategy == strat), col].iloc[0])


def check_finds(method, model):
    X, O, F, T = run(method, model, True)
    ca, bf, ro = pooled(T, "chooser_all"), pooled(T, "best_fixed_train"), pooled(T, "random_option")
    # chosen option must follow the sign of x1 (0 when x1 > 0, 1 when x1 < 0) on clear cases
    x = X[O.row.to_numpy(), 0]                                         # O.row = position in the input arrays
    clear = np.abs(x) > 0.5
    right = np.where(x > 0, 0, 1)
    acc = float((O.choice.to_numpy()[clear] == right[clear]).mean())
    print(f"  {method}-{model} signal: chooser_all {ca:+.2f}  best_fixed {bf:+.2f}  random {ro:+.2f}  "
          f"thr {pooled(T, 'chooser_thr'):+.2f} (n {pooled(T, 'chooser_thr', 'n'):.0f})  oracle "
          f"{pooled(T, 'oracle'):+.2f}  accuracy |x1|>0.5: {acc:.1%}")
    assert ca > bf + 1.0, (ca, bf)
    assert ca > ro + 1.0, (ca, ro)
    assert acc > 0.85, acc
    assert pooled(T, "chooser_thr") >= ca - 0.3
    assert F.purge_ok.all()
    assert len(F) == 4


def test_reg_hgb_finds_feature():
    check_finds("reg", "hgb")


def test_reg_ridge_finds_feature():
    check_finds("reg", "ridge")


def test_clf_hgb_finds_feature():
    check_finds("clf", "hgb")


def check_noise(method, model, seed):
    _, O, F, T = run(method, model, False, seed=seed)
    ca, bf = pooled(T, "chooser_all"), pooled(T, "best_fixed_train")
    row = T.loc[(T.period == "pooled") & (T.strategy == "chooser_all")].iloc[0]
    thr, n_thr = pooled(T, "chooser_thr"), pooled(T, "chooser_thr", "n")
    sd = 5.0
    print(f"  {method}-{model} noise seed {seed}: chooser_all {ca:+.2f}  best_fixed {bf:+.2f}  diff "
          f"{row.diff_vs_best_fixed:+.2f} (se {row.diff_se:.2f})  thr {thr:+.2f} (n {n_thr:.0f}) "
          f"rskip 5-95% {pooled(T, 'rskip_chosen', 'p5_usd_per_trade'):+.2f}..{pooled(T, 'rskip_chosen', 'p95_usd_per_trade'):+.2f}")
    assert row.diff_vs_best_fixed < 3 * row.diff_se, row
    assert abs(ca - (-1)) < 3 * sd / np.sqrt(len(O)) + 0.05          # true value of every option is -1
    assert thr - (-1) < 3 * sd / np.sqrt(max(n_thr, 1)) + 0.05


def test_noise_no_gain():
    for m in (("reg", "hgb"), ("clf", "hgb"), ("reg", "ridge")):
        for seed in (1, 2):
            check_noise(*m, seed)


def test_holdout_and_purge():
    """Rows at/after the holdout's first bar (and rows whose label ends there) are never used; a fold touching the
    holdout is refused; every training row's label ends >= 1 day before its test window."""
    X, Xopt, P, t, te = synth(n=9000, start="2010-01-01", end="2026-03-01", seed=3)
    te = te.to_numpy().copy()
    near = np.flatnonzero((t < wf.HOLDOUT_SESSION_START) & (t > wf.HOLDOUT_SESSION_START - pd.Timedelta(hours=3)))
    te[near] = wf.HOLDOUT_SESSION_START + pd.Timedelta(hours=1)        # label reaching into the holdout
    cfg = sc.Config(hgb=dict(FAST), n_random=20, model="ridge")
    folds = wf.make_folds(test_years=(2013, 2024), h1_2025=True)
    O, F = sc.run_chooser(X, Xopt, P, t, te, cfg=cfg, folds=folds)
    cut = wf.HOLDOUT_SESSION_START
    assert (pd.DatetimeIndex(O.t) < cut).all()
    assert not pd.DatetimeIndex(O.t).isin(t[near]).any()
    assert F.purge_ok.all()
    assert (pd.DatetimeIndex(F.max_train_t_end) <= pd.DatetimeIndex(F.test_start) - wf.PURGE).all()
    try:
        sc.run_chooser(X, Xopt, P, t, te, cfg=cfg, folds=[wf.Fold("2025H2", cut, pd.Timestamp("2026-01-01"), cut)])
    except wf.HoldoutError:
        pass
    else:
        raise AssertionError("holdout fold was not refused")


def test_threshold_keep_all_is_minus_inf():
    p = np.array([-3.0, -2.0, -1.0]); pnl = np.array([10.0, 10.0, -5.0])   # keeping all is best
    thr, info = sc.threshold(p, pnl, 0.05)
    assert info["keep_share"] == 1.0 and thr == -np.inf
    thr, _ = sc.threshold(p, np.array([-5.0, -5.0, 4.0]), 0.05)
    assert thr == -1.0


def test_winner_and_option_features():
    P = np.array([[1.0, 2.0, 2.0], [-1.0, -3.0, -1.0]])
    assert sc.winner(P).tolist() == [1, 0]                             # ties -> first option
    C = np.array([100.0, 100.0]); d = np.array([1, -1]); R20 = np.array([4.0, 2.0])
    STOP = np.array([[98.0, 96.0], [101.0, 104.0]])
    X, dist = sc.option_features(C, STOP, d, R20, usd=2.0, cost=2.0)
    assert np.allclose(dist, [[2, 4], [1, 4]])
    assert np.allclose(X[..., 0], [[0.5, 1.0], [0.5, 2.0]])
    assert np.allclose(X[..., 1], [[0.5, 0.25], [1.0, 0.25]])


def test_hgb_survives_all_nan_column():
    """A feature that is empty before some date (x_YM_* before 2018) must not crash the tree models (sklearn's HGB
    binning raises on an all-NaN column): it is dropped from the fit and the prediction of that fold."""
    X, Xopt, P, t, te = synth(signal=True, seed=3)
    X = np.hstack([X, np.full((len(X), 1), np.nan, np.float32)])
    X[t >= pd.Timestamp("2015-01-01"), -1] = 1.0                    # empty in every training set before 2015
    for method in ("reg", "clf"):
        cfg = sc.Config(method=method, model="hgb", hgb=dict(FAST), n_random=20)
        O, F = sc.run_chooser(X, Xopt, P, t, te, cfg=cfg, folds=FOLDS)
        assert len(F) == 4 and len(O) > 0, (method, len(F))


if __name__ == "__main__":
    import time
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            t0 = time.time()
            fn()
            print(f"PASS {name} ({time.time() - t0:.0f}s)", flush=True)
    print("all tests passed")
