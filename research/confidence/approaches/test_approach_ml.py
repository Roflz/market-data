"""
Tests for approach_ml.py (run: cd approaches && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../../pylib:../../..:../../signals:..:.
python3 test_approach_ml.py   - also works under pytest).

Synthetic rows with SPEC.md column names, timestamps 2014-2021, label windows of 1-4 hours, three markets:
  * planted: y ~ Bernoulli(sigmoid(f(X))) with a known with-trade signal (entries) or against-trade signal (exits);
    every scorer must rank out-of-sample (2020-2021) planted winners clearly higher (AUC well above 0.5);
  * noise:   y independent of X; out-of-sample AUC must stay near 0.5.
Also: probabilities in [0, 1]; weights_table well-formed; entry AND exit tasks; AFML helpers (uniqueness, sequential
bootstrap, time decay, bet sizing) against hand-computed values; prior shrinkage reproduces the prior when s -> 0.
A small dummy prior Scorer with known weights stands in for the hand/stat priors written by other agents.
"""
from __future__ import annotations

import math
import time

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

import approach_ml as am
from scorer_api import REGISTRY, Scorer, platt, register

ENTRY_COLS = ["pat_engulfing", "pat_hammer", "pat_doji", "fam_reversal", "fam_breakout", "dist_swhi_5", "dist_swlo_5",
              "brk_5", "struct_5", "ema_stack", "ema20_slope", "dist_ema20", "mom", "dist_vwap", "rng_rel", "vol_rel",
              "clv", "tod_open", "tod_midday", "tod_close", "dow_0", "h1_ema_stack", "x_NQ_ret", "x_NQ_ema_stack"]
EXIT_COLS = ENTRY_COLS + ["open_R", "mfe_R", "mae_R", "bars_held", "dist_stop_R", "mins_to_1645"]
TABLE_COLS = {"signal", "weight", "points", "meaning", "source"}


def make_data(n=4000, task="entry", planted=True, seed=0):
    rng = np.random.default_rng(seed)
    cols = ENTRY_COLS if task == "entry" else EXIT_COLS
    X = pd.DataFrame(index=range(n))
    for c in cols:
        if c.startswith("pat_doji") or c.startswith(("tod_", "dow_")):
            X[c] = (rng.random(n) < 0.2).astype(float)
        elif c.startswith(("pat_", "fam_")):
            X[c] = rng.choice([-1.0, 0.0, 1.0], n, p=[0.1, 0.8, 0.1])
        elif c in ("brk_5", "struct_5", "ema_stack", "h1_ema_stack", "x_NQ_ema_stack"):
            X[c] = rng.choice([-1.0, 0.0, 1.0], n)
        elif c in ("rng_rel", "vol_rel", "bars_held", "mins_to_1645"):
            X[c] = rng.gamma(2.0, 0.5, n)
        else:
            X[c] = rng.normal(0, 1, n)
    X.loc[rng.random(n) < 0.05, "dist_swhi_5"] = np.nan             # unconfirmed swing -> NaN, like features.py
    X = X.astype(np.float32)
    if task == "entry":
        f = -0.3 + 0.9 * X["ema_stack"] + 0.6 * X["struct_5"] + 0.5 * X["dist_vwap"] + 0.7 * X["pat_engulfing"]
    else:                                                             # exit: evidence AGAINST the open trade
        f = -0.4 - 0.9 * X["ema_stack"] - 0.6 * X["struct_5"] + 0.6 * X["open_R"]
    p = 1 / (1 + np.exp(-f.to_numpy(float))) if planted else np.full(n, 0.45)
    y = (rng.random(n) < p).astype(int)
    t0 = pd.Timestamp("2014-01-02 09:30", tz="America/New_York")
    t = t0 + pd.to_timedelta(np.sort(rng.uniform(0, 8 * 365.25 * 24, n)), unit="h")
    meta = pd.DataFrame({
        "t": t, "t_end": t + pd.to_timedelta(rng.uniform(1, 4, n), unit="h"),
        "d": rng.choice([-1, 1], n), "market": rng.choice(["ES", "NQ", "YM"], n), "year": t.year})
    gain = np.where(y == 1, rng.uniform(20, 80, n), -rng.uniform(15, 60, n))
    if task == "entry":
        meta["pnl_usd"] = gain
    else:
        meta["exit_gain_usd"] = gain
        meta["trade_id"] = np.arange(n) // 8
    w = am.label_uniqueness(meta)
    return X, y, w, meta


def split(X, y, w, meta):
    tr = (meta["year"] < 2020).to_numpy()
    return (X[tr].reset_index(drop=True), y[tr], w[tr], meta[tr].reset_index(drop=True),
            X[~tr].reset_index(drop=True), y[~tr])


@register
class DummyLinearPrior(Scorer):
    """Stand-in prior: fixed hand weights, Platt-calibrated on the training rows (like a hand_* scorer)."""
    name = "test_dummy_prior"
    family = "hand"
    source = "test fixture"

    def __init__(self, task="entry", **params):
        super().__init__(task, **params)
        default = ({"ema_stack": 1.0, "struct_5": 0.5, "pat_engulfing": 0.5} if task == "entry"
                   else {"ema_stack": -1.0, "struct_5": -0.5})
        self.w = params.get("weights", default)

    def fit(self, X, y, w=None, meta=None):
        self._cal = platt(self.score(X), y, w)
        return self

    def score(self, X):
        return sum(v * X[c].fillna(0).to_numpy(float) for c, v in self.w.items())

    def predict_proba(self, X):
        return self._cal(self.score(X))

    def weights_table(self):
        return pd.DataFrame({"signal": list(self.w), "weight": list(self.w.values()),
                             "points": [v / am.LN2_20 for v in self.w.values()], "meaning": "", "source": "test"})


FAST = {
    "ml_logit_l2": {},
    "ml_afml_rf": {"n_estimators": 150},
    "ml_creamer_boost": {"max_rounds": 12},
    "ml_creamer_experts": {"rounds": 8, "every_months": 6, "max_experts": 6},
    "prior_logit_offset": {"prior": "test_dummy_prior"},
    "prior_logit_shrink": {"prior": "test_dummy_prior"},
    "prior_gbm": {"prior": "test_dummy_prior", "max_trees": 120},
}
RESULTS = {}


def run_one(name, task, planted, seed=1):
    X, y, w, meta = make_data(task=task, planted=planted, seed=seed)
    Xtr, ytr, wtr, mtr, Xte, yte = split(X, y, w, meta)
    s = REGISTRY[name](task=task, **FAST[name])
    t0 = time.time()
    s.fit(Xtr, ytr, wtr, mtr)
    p = s.predict_proba(Xte)
    sc = s.score(Xte)
    assert p.shape == (len(Xte),) and np.all(np.isfinite(p)) and p.min() >= 0 and p.max() <= 1, name
    assert sc.shape == (len(Xte),) and np.all(np.isfinite(sc)), name
    tab = s.weights_table()
    assert isinstance(tab, pd.DataFrame) and len(tab) > 0 and TABLE_COLS <= set(tab.columns), name
    assert tab["signal"].notna().all() and np.isfinite(tab["weight"].to_numpy(float)).all(), name
    auc = roc_auc_score(yte, p)
    auc_s = roc_auc_score(yte, sc)
    RESULTS[(name, task, "planted" if planted else "noise")] = (auc, auc_s, time.time() - t0)
    return s, auc, auc_s, tab


def _check_planted(name, task):
    _, auc, auc_s, _ = run_one(name, task, True)
    assert auc > 0.66 and auc_s > 0.66, (name, task, auc, auc_s)


def _check_noise(name, task):
    _, auc, auc_s, _ = run_one(name, task, False, seed=7)
    assert abs(auc - 0.5) < 0.07 and abs(auc_s - 0.5) < 0.07, (name, task, auc, auc_s)


# ------------------------------------------------------------------------------- every scorer, both tasks
def test_logit_l2():
    for task in ("entry", "exit"):
        _check_planted("ml_logit_l2", task)
    _check_noise("ml_logit_l2", "entry")


def test_logit_l2_signs():
    s, _, _, tab = run_one("ml_logit_l2", "entry", True)
    wt = tab.set_index("signal")["weight"]
    assert wt["ema_stack"] > 0.4 and wt["struct_5"] > 0.2 and wt["pat_engulfing"] > 0.2
    s, _, _, tab = run_one("ml_logit_l2", "exit", True)
    wt = tab.set_index("signal")["weight"]
    assert wt["ema_stack"] < -0.4 and wt["open_R"] > 0.2      # exit: with-trade evidence gets a NEGATIVE weight


def test_afml_rf():
    for task in ("entry", "exit"):
        _check_planted("ml_afml_rf", task)
    _check_noise("ml_afml_rf", "entry")
    s, _, _, tab = run_one("ml_afml_rf", "entry", True)
    assert tab.iloc[0]["signal"] in ("ema_stack", "struct_5", "dist_vwap", "pat_engulfing")
    assert 0 < s.avgU_ <= 1
    X, y, w, meta = make_data(seed=3)
    b = s.bet_size(X.iloc[:200])
    assert b.min() >= 0 and b.max() <= 1


def test_afml_rf_bag_size_is_avgU_times_n():
    """Overlapping labels (avgU ~ 0.1-0.3): each tree must draw avgU x n rows. scikit-learn 1.9 reads a FLOAT
    max_samples relative to sample_weight.sum(), which would give avgU^2 x n with uniqueness weights."""
    X, y, w, meta = make_data(seed=13, n=3000)
    meta["t_end"] = meta["t"] + pd.Timedelta(days=20)
    w = am.label_uniqueness(meta)
    s = REGISTRY["ml_afml_rf"](task="entry", n_estimators=10, min_tree_rows=50).fit(X, y, w, meta)
    assert s.avgU_ < 0.5 and s.model_.max_samples == int(round(s.avgU_ * len(X))), (s.avgU_, s.model_.max_samples)


def test_afml_rf_sequential_bootstrap_option():
    X, y, w, meta = make_data(seed=12, n=2500)
    Xtr, ytr, wtr, mtr, Xte, yte = split(X, y, w, meta)
    s = REGISTRY["ml_afml_rf"](task="entry", bootstrap="sequential", n_estimators=25,
                               seq_max_rows=400).fit(Xtr, ytr, wtr, mtr)
    assert isinstance(s.model_, am._SeqBootForest) and roc_auc_score(yte, s.predict_proba(Xte)) > 0.66


def test_creamer_boost():
    for task in ("entry", "exit"):
        _check_planted("ml_creamer_boost", task)
    _check_noise("ml_creamer_boost", "entry")
    s, _, _, tab = run_one("ml_creamer_boost", "entry", True)
    assert tab.iloc[0]["signal"] == "(always)" and 1 <= s.rounds_ <= 12
    assert any("ema_stack" in r for r in tab["signal"])            # the strongest planted feature is used in a rule
    X, y, w, meta = make_data(seed=4, n=2500)                      # Creamer's 'one splitter per node' variant
    Xtr, ytr, wtr, mtr, Xte, yte = split(X, y, w, meta)
    s1 = REGISTRY["ml_creamer_boost"](task="entry", single_splitter=True, max_rounds=10).fit(Xtr, ytr, wtr, mtr)
    pids = [r[0] for r in s1.model_.rules]
    assert len(pids) == len(set(pids)) and roc_auc_score(yte, s1.predict_proba(Xte)) > 0.66


def test_creamer_experts():
    for task in ("entry", "exit"):
        _check_planted("ml_creamer_experts", task)
    _check_noise("ml_creamer_experts", "entry")
    s, _, _, tab = run_one("ml_creamer_experts", "entry", True)
    assert len(s.experts_) >= 2 and abs(tab["weight"].sum() - 1) < 1e-9
    X, y, w, meta = make_data(seed=3)
    sig = s.trade_signal(X.iloc[:300])
    assert np.all(np.abs(sig) <= 1) and np.all((sig == 0) | (np.abs(sig) >= 0.2))


def test_prior_offset():
    for task in ("entry", "exit"):
        _check_planted("prior_logit_offset", task)
    _check_noise("prior_logit_offset", "entry")


def test_prior_shrink():
    for task in ("entry", "exit"):
        _check_planted("prior_logit_shrink", task)
    _check_noise("prior_logit_shrink", "entry")
    s, _, _, tab = run_one("prior_logit_shrink", "entry", True)
    assert "own per-feature weights" in s.mu_how_                   # exact prior weights were found and used
    pw = tab.set_index("signal")["prior_weight"]
    assert pw["ema_stack"] > 0 and abs(pw["dist_vwap"]) < 1e-12


def test_prior_gbm():
    for task in ("entry", "exit"):
        _check_planted("prior_gbm", task)
    _check_noise("prior_gbm", "entry")


def test_gbm_monitor_matches_sklearn_and_starts_at_prior():
    """The early-stopping monitor's running log-odds must equal GradientBoosting's own decision_function, and stage 0
    must be the prior's log-odds (i.e. boosting really starts from the prior)."""
    X, y, w, meta = make_data(seed=11, n=2000)
    pr = DummyLinearPrior("entry").fit(X, y, w)
    E = am.PriorGBM._enc(X)
    s = am.PriorGBM(task="entry", prior="test_dummy_prior", max_trees=40)
    s.columns_ = list(X.columns)
    raw0 = am._logit(am._PriorInit(pr, s.columns_).predict_proba(E)[:, 1])
    assert np.allclose(raw0, am._logit(pr.predict_proba(X)), atol=1e-5)
    mon = am._ValMonitor(E, y, w, raw0, patience=10 ** 6)
    g = s._gbm(pr, 40, len(y)).fit(E, y, sample_weight=w, monitor=mon)
    assert np.allclose(mon.raw, g.decision_function(E), atol=1e-4)
    assert len(mon.losses) == 41


def test_prior_shrink_tiny_scale_returns_prior():
    """With s -> 0 the shrink model must reproduce the prior's calibrated log-odds; the offset model the prior +
    an intercept shift."""
    X, y, w, meta = make_data(seed=5)
    Xtr, ytr, wtr, mtr, Xte, yte = split(X, y, w, meta)
    pr = DummyLinearPrior("entry").fit(Xtr, ytr, wtr)
    for name in ("prior_logit_shrink", "prior_logit_offset"):
        s = REGISTRY[name](task="entry", prior="test_dummy_prior", scales=(1e-5,)).fit(Xtr, ytr, wtr, mtr)
        d = np.abs(s.predict_proba(Xte) - pr.predict_proba(Xte))
        assert d.max() < 0.03, (name, d.max())


def test_prior_crossfit_and_cauchy_run():
    X, y, w, meta = make_data(seed=6, n=2500)
    Xtr, ytr, wtr, mtr, Xte, yte = split(X, y, w, meta)
    s = REGISTRY["prior_logit_offset"](task="entry", prior="test_dummy_prior", crossfit=3,
                                       prior_dist="cauchy").fit(Xtr, ytr, wtr, mtr)
    assert roc_auc_score(yte, s.predict_proba(Xte)) > 0.66


def test_prior_projection_for_nonlinear_prior():
    """A prior without usable per-feature weights falls back to a least-squares projection of its log-odds."""
    @register
    class SquaredPrior(DummyLinearPrior):
        name = "test_squared_prior"

        def score(self, X):
            return np.sign(X["ema_stack"].to_numpy(float)) * X["ema_stack"].to_numpy(float) ** 2

        def weights_table(self):
            return None
    X, y, w, meta = make_data(seed=8, n=2500)
    Xtr, ytr, wtr, mtr, Xte, yte = split(X, y, w, meta)
    s = REGISTRY["prior_logit_shrink"](task="entry", prior="test_squared_prior").fit(Xtr, ytr, wtr, mtr)
    assert "projection" in s.mu_how_ and s.mu_r2_ > 0.5


def test_no_meta_still_runs():
    X, y, w, meta = make_data(seed=9, n=1500)
    for name in FAST:
        s = REGISTRY[name](task="entry", **FAST[name]).fit(X, y)
        p = s.predict_proba(X)
        assert np.all((p >= 0) & (p <= 1)), name


def test_unknown_prior_raises():
    try:
        REGISTRY["prior_logit_offset"](task="entry", prior="no_such_prior").fit(*make_data(n=500)[:2])
    except KeyError as e:
        assert "no_such_prior" in str(e)
    else:
        raise AssertionError("expected KeyError")


# ------------------------------------------------------------------------------- AFML helpers
def test_uniqueness_hand_example():
    # A = [0, 2), B = [1, 3) overlap on [1, 2): u = (1 * 1 + 1 * 1/2) / 2 = 0.75 each; C = [10, 11) alone: 1.
    meta = pd.DataFrame({"t": [0.0, 1.0, 10.0], "t_end": [2.0, 3.0, 11.0], "market": ["ES", "ES", "ES"]})
    assert np.allclose(am.label_uniqueness(meta), [0.75, 0.75, 1.0])
    meta["market"] = ["ES", "NQ", "ES"]                       # different markets do not overlap
    assert np.allclose(am.label_uniqueness(meta), [1.0, 1.0, 1.0])


def test_sequential_bootstrap_prefers_unique():
    # labels 0 and 1 identical, label 2 disjoint: once 0 or 1 is drawn, 2 becomes twice as likely as the other.
    t, te = np.array([0.0, 0.0, 20.0]), np.array([10.0, 10.0, 30.0])
    draws = np.array([am.sequential_bootstrap(t, te, 3, rng=s) for s in range(400)])
    share2 = (draws == 2).mean()
    assert share2 > 0.36, share2                                # standard bootstrap would give 1/3
    assert draws.min() >= 0 and draws.max() <= 2


def test_time_decay():
    u = np.ones(4)
    tt = np.array([3.0, 0.0, 1.0, 2.0])
    assert np.allclose(am.time_decay(u, tt, 1.0), 1.0)
    d = am.time_decay(u, tt, 0.0)                              # newest -> 1, linear in cumulative uniqueness
    assert np.isclose(d[0], 1.0) and np.isclose(d[1], 0.25) and np.all(np.diff(d[[1, 2, 3, 0]]) > 0)


def test_bet_size():
    assert am.bet_size(0.5) == 0 and am.bet_size(0.3) == 0                  # meta-labeling: below 1/2 = pass
    p = np.array([0.55, 0.6, 0.7, 0.9])
    m = am.bet_size(p)
    z = (p - 0.5) / np.sqrt(p * (1 - p))
    assert np.allclose(m, 2 * am.stats.norm.cdf(z) - 1) and np.all(np.diff(m) > 0)
    assert np.allclose(am.bet_size(p, step=0.1), np.round(m / 0.1) * 0.1)
    assert am.bet_size(0.3, meta_label=False) < 0


def test_inner_split_purges():
    X, y, w, meta = make_data(n=1000)
    tr, va = am.inner_split(meta, y)
    t, te = am._ts(meta["t"]), am._ts(meta["t_end"])
    assert len(np.intersect1d(tr, va)) == 0 and te[tr].max() < t[va].min()
    assert set(meta["year"].iloc[va]) == {2020, 2021}           # last 2 of >= 4 years


def _all_tests():
    return [(k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)]


if __name__ == "__main__":
    t0 = time.time()
    fails = 0
    for k, f in _all_tests():
        t1 = time.time()
        try:
            f()
            print(f"PASS {k} ({time.time() - t1:.1f}s)")
        except Exception as e:                                   # noqa: BLE001
            fails += 1
            print(f"FAIL {k}: {type(e).__name__}: {e}")
    print("\nout-of-sample AUC (predict_proba / score), fit seconds:")
    for (name, task, kind), (a, b, sec) in sorted(RESULTS.items()):
        print(f"  {name:20s} {task:5s} {kind:7s} AUC {a:.3f} / {b:.3f}  fit {sec:.1f}s")
    print(f"\n{len(_all_tests()) - fails} passed, {fails} failed in {time.time() - t0:.0f}s")
    raise SystemExit(1 if fails else 0)
