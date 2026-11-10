"""
Tests for approach_hand.py (hand-set weights + Platt). Run:
  cd research/confidence/approaches && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../../pylib:../../..:../../signals:..:. \
      python3 test_approach_hand.py
Synthetic X with SPEC column names (oriented: + = with the trade). Each scorer must rank planted winners higher out of
sample (fit on the first half, AUC on the second), stay near AUC 0.5 on pure noise, give probabilities in [0, 1], a
well-formed weights_table, and run for task="entry" and task="exit".
"""
import math
import os
import sys
import tempfile
import time
import traceback

import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError
from sklearn.metrics import roc_auc_score

import approach_hand as ah
from scorer_api import REGISTRY

SCORERS = ["hand_bulkowski", "hand_morris_woe", "hand_ndr_composite", "hand_user"]
N = 20000


# ------------------------------------------------------------------------------------------------ synthetic data
def make_X(n=N, task="entry", seed=0, sym="ES"):
    rng = np.random.default_rng(seed)
    cols = [c for c in ah.spec_columns() if c not in ah.EXIT_STATE and not c.startswith(f"x_{sym}_")]
    X = {}
    for c in cols:
        if c in ("pat_doji", "pat_spinning_top", "pat_inside_bar", "pat_nr7") or c.startswith("atfib_"):
            X[c] = (rng.random(n) < 0.1).astype(float)
        elif c.startswith("pat_"):
            X[c] = np.where(rng.random(n) < 0.12, rng.choice([-1.0, 1.0], n), 0.0)
        elif c.startswith(("fam_", "brk_", "struct_", "mom_x100")) or c.endswith("ema_stack") or c == "h1_struct_5":
            X[c] = rng.choice([-1.0, 0.0, 1.0], n)
        elif c.startswith(("tod_", "dow_")):
            X[c] = (rng.random(n) < 0.2).astype(float)
        elif c in ("rng_rel", "vol_rel", "day_range_rel", "body_frac"):
            X[c] = rng.gamma(2.0, 0.5, n)
        else:
            X[c] = rng.normal(0, 1, n)
    X = pd.DataFrame(X, dtype="float32")
    X.iloc[:50, X.columns.get_loc("h1_mom")] = np.nan          # warm-up NaNs must be tolerated
    X.iloc[:50, X.columns.get_loc("x_NQ_ret")] = np.nan
    if task == "exit":
        X["open_R"] = rng.normal(0, 1, n)
        X["mfe_R"] = np.abs(rng.normal(0, 1, n))
        X["mae_R"] = -np.abs(rng.normal(0, 1, n))
        X["bars_held"] = rng.integers(0, 32, n).astype(float)
        X["dist_stop_R"] = np.abs(rng.normal(1, 0.5, n))
        X["mins_to_1645"] = rng.integers(0, 400, n).astype(float)
    return X


def make_meta(n, seed=0, task="entry"):
    rng = np.random.default_rng(seed + 99)
    t = pd.date_range("2015-01-01", periods=n, freq="15min")
    m = pd.DataFrame({"t": t, "t_end": t + pd.Timedelta("2h"), "d": rng.choice([-1, 1], n), "market": "ES",
                      "year": t.year, "trade_id": np.arange(n) // 10})
    m["pnl_usd" if task == "entry" else "exit_gain_usd"] = rng.normal(0, 20, n)
    return m


def planted_logit(X, scorer, task):
    """A signal the scorer's own (published) logic can see. For exits the evidence is turned around."""
    on = lambda c: (X[c].to_numpy(float) > 0).astype(float)
    v = lambda c: np.nan_to_num(X[c].to_numpy(float))
    if scorer == "hand_bulkowski":
        z = 1.5 * (v("pat_engulfing") + v("pat_morning_evening_star") + v("pat_three_soldiers_crows") + v("pat_piercing")
                   + v("pat_hammer")) - 1.5 * v("pat_inverted_hammer")
    elif scorer == "hand_morris_woe":
        z = 1.2 * (on("ema_stack") + on("h1_ema_stack") + on("x_NQ_ema_stack") + on("struct_5") - 2)
    elif scorer == "hand_ndr_composite":
        z = 0.6 * sum(np.sign(v(c)) for c in ("ema_stack", "mom", "dist_ema20", "h1_ema_stack", "dist_vwap", "x_YM_ret"))
    else:  # hand_user: weights written by user_csv() below
        z = (1.0 * v("ema_stack") + 0.5 * v("mom")) if task == "entry" else (-1.5 * v("pat_engulfing") + 0.8 * v("open_R"))
    return -z if (task == "exit" and scorer != "hand_user") else z


def user_csv(tmpdir):
    cols = ah.spec_columns()
    t = pd.DataFrame({"signal": cols, "entry_weight": "", "exit_weight": "", "note": ""})
    t.loc[t.signal == "ema_stack", "entry_weight"] = "1.0"
    t.loc[t.signal == "mom", "entry_weight"] = "0.5"
    t.loc[t.signal == "pat_engulfing", "exit_weight"] = "-1.5"
    t.loc[t.signal == "open_R", "exit_weight"] = "0.8"
    p = os.path.join(tmpdir, "user_weights.csv")
    t.to_csv(p, index=False)
    return p


def build(name, task, tmpdir):
    kw = {"path": user_csv(tmpdir)} if name == "hand_user" else {}
    return REGISTRY[name](task=task, **kw)


def split_fit_auc(name, task, y_fn, seed, tmpdir):
    X = make_X(N, task, seed)
    rng = np.random.default_rng(seed + 7)
    y = y_fn(X, rng)
    meta = make_meta(N, seed, task)
    h = N // 2
    s = build(name, task, tmpdir)
    w = rng.uniform(0.5, 1.5, h)
    s.fit(X.iloc[:h], y[:h], w, meta.iloc[:h])
    p = s.predict_proba(X.iloc[h:])
    return s, roc_auc_score(y[h:], p), p, X, y


# ------------------------------------------------------------------------------------------------ tests
def test_bulkowski_table_and_csv():
    t = ah.bulkowski_table()
    import features
    assert set(t.pattern) == set(features.DIRECTIONAL), "every directional pattern must be mapped (weight 0 if none)"
    assert set(t.basis) <= set(ah.ALL_BASIS)
    use = t.basis.isin(ah.USABLE_BASIS)
    assert (t.rate_textbook[use] > 0).all() and (t.rate_textbook[use] < 1).all()
    assert np.allclose(t.weight_logodds[use], np.log(t.rate_textbook[use] / (1 - t.rate_textbook[use])))
    assert (t.weight_logodds[~use] == 0).all()
    assert (t.url[t.basis.isin(("published", "complement", "published_trade"))] != "").all()
    # spot checks against the pages (rates as read 2026-11-08)
    r = t.set_index(["pattern", "side"]).rate_textbook
    assert r["engulfing", "bull"] == 0.63 and r["engulfing", "bear"] == 0.79
    assert r["hanging_man", "bear"] == 0.41 and r["inverted_hammer", "bull"] == 0.35
    assert r["harami", "bear"] == 0.47 and r["marubozu", "bear"] == 0.66
    csv = pd.read_csv(ah.BULKOWSKI_CSV)
    assert len(csv) == len(t) and np.allclose(csv.weight_logodds, t.weight_logodds, atol=1e-4), \
        "bulkowski_weights.csv is stale: run python3 approach_hand.py --write-csv"


def test_planted_signal_ranked_higher():
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for name in SCORERS:
            for task in ("entry", "exit"):
                yf = lambda X, rng, name=name, task=task: (
                    rng.random(len(X)) < 1 / (1 + np.exp(-(planted_logit(X, name, task) - 0.2)))).astype(int)
                s, auc, p, _, _ = split_fit_auc(name, task, yf, seed=1, tmpdir=tmp)
                out[(name, task)] = auc
                assert auc > 0.6, f"{name}/{task}: planted AUC {auc:.3f} too low"
                assert np.isfinite(p).all() and (p >= 0).all() and (p <= 1).all()
                assert s.platt_a_ > 0, f"{name}/{task}: Platt slope must be positive for a planted signal"
    return out


def test_noise_stays_near_half():
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for name in SCORERS:
            for task in ("entry", "exit"):
                yf = lambda X, rng: (rng.random(len(X)) < 0.45).astype(int)
                _, auc, p, _, _ = split_fit_auc(name, task, yf, seed=3, tmpdir=tmp)
                out[(name, task)] = auc
                assert 0.46 < auc < 0.54, f"{name}/{task}: noise AUC {auc:.3f}"
                assert (p >= 0).all() and (p <= 1).all()
                assert abs(p.mean() - 0.45) < 0.03, f"{name}/{task}: calibration should sit at the base rate"
    return out


def test_weights_tables():
    with tempfile.TemporaryDirectory() as tmp:
        for name in SCORERS:
            for task in ("entry", "exit"):
                s = build(name, task, tmp)
                X = make_X(4000, task, seed=5)
                y = (np.random.default_rng(5).random(4000) < 0.5).astype(int)
                s.fit(X, y, None, make_meta(4000, 5, task))
                t = s.weights_table()
                assert isinstance(t, pd.DataFrame) and len(t) > 0, name
                for c in ("signal", "weight", "points", "meaning", "source"):
                    assert c in t.columns, (name, c)
                assert t.signal.is_unique, name
                assert np.isfinite(t.weight.astype(float)).all() and np.isfinite(t.points.astype(float)).all(), name
                assert t.meaning.astype(str).str.len().gt(0).all() and t.source.astype(str).str.len().gt(0).all(), name
                if name in ("hand_bulkowski", "hand_user"):              # log-odds weights -> scorecard points
                    assert np.allclose(t.points, t.weight / (math.log(2) / 20)), name
                if name == "hand_morris_woe":
                    used = t[t.weight != 0]
                    assert abs(abs(used.weight).sum() - 100) < 1e-6, "Morris weights must sum to 100"
                if name == "hand_bulkowski" and task == "exit":           # exit table = entry table turned around
                    te = REGISTRY[name](task="entry").weights_table().set_index("signal").weight
                    assert np.allclose(t.set_index("signal").weight, -te)


def test_bulkowski_directional_and_exit_sign():
    t = ah.bulkowski_table().set_index(["pattern", "side"]).weight_logodds
    X = pd.DataFrame({"pat_engulfing": [1.0, 1.0, -1.0, 0.0], "pat_hanging_man": [0.0, 0.0, 0.0, -1.0]})
    d = np.array([1, -1, 1, 1])
    sd = REGISTRY["hand_bulkowski"](directional=True).score(X, d=d)
    # row0: bullish engulfing on a long; row1: bearish engulfing on a short; row2: bearish engulfing against a long;
    # row3: hanging man (bearish, Bulkowski: 59% up) against a long -> SUBTRACTS a negative weight -> helps the long
    assert np.allclose(sd, [t["engulfing", "bull"], t["engulfing", "bear"], -t["engulfing", "bear"],
                            -t["hanging_man", "bear"]])
    ss = REGISTRY["hand_bulkowski"]().score(X)
    sym = (t["engulfing", "bull"] + t["engulfing", "bear"]) / 2
    assert np.allclose(ss, [sym, sym, -sym, -t["hanging_man", "bear"]])
    assert np.allclose(REGISTRY["hand_bulkowski"](task="exit").score(X), -ss)
    try:
        REGISTRY["hand_bulkowski"](directional=True).score(X)
        raise AssertionError("directional without d must raise")
    except ValueError:
        pass
    # directional fit takes d from meta
    Xs = make_X(3000, seed=8)
    y = (np.random.default_rng(8).random(3000) < 0.5).astype(int)
    m = make_meta(3000, 8)
    s = REGISTRY["hand_bulkowski"](directional=True).fit(Xs, y, None, m)
    assert ((s.predict_proba(Xs, d=m.d.to_numpy()) >= 0) & (s.predict_proba(Xs, d=m.d.to_numpy()) <= 1)).all()
    # optional (unpublished) structure weight for exits
    Xb = pd.DataFrame({"pat_engulfing": [0.0, 0.0], "brk_5": [-1.0, 1.0], "brk_10": [0.0, 0.0]})
    assert np.allclose(REGISTRY["hand_bulkowski"](task="exit", structure_weight=0.7).score(Xb), [0.7, 0.0])
    assert np.allclose(REGISTRY["hand_bulkowski"](task="exit").score(Xb), [0.0, 0.0])


def test_morris_levels_and_bands():
    s = REGISTRY["hand_morris_woe"]()
    cols = ["dist_ema8", "dist_ema20", "dist_ema50", "ema_stack", "struct_5", "h1_ema_stack", "h1_struct_5", "mom",
            "x_NQ_ret", "x_NQ_ema_stack", "x_YM_ret", "x_YM_ema_stack"]
    up = {"dist_ema8": 0.5, "dist_ema20": 1.0, "dist_ema50": 2.0, "ema_stack": 1, "struct_5": 1, "h1_ema_stack": 1,
          "h1_struct_5": 1, "mom": 1.0, "x_NQ_ret": 1, "x_NQ_ema_stack": 1, "x_YM_ret": 1, "x_YM_ema_stack": 1}
    down = {k: -v for k, v in up.items()}
    half = dict(up, x_NQ_ret=-1, x_NQ_ema_stack=-1, x_YM_ret=-1, x_YM_ema_stack=-1)       # price on, breadth off
    nan_breadth = dict(up, x_NQ_ret=np.nan, x_NQ_ema_stack=np.nan, x_YM_ret=np.nan, x_YM_ema_stack=np.nan)
    X = pd.DataFrame([up, down, half, nan_breadth])[cols]
    lv = s.level(X)
    assert np.allclose(lv, [100, 0, 200 / 3, 100]), lv              # breadth NaN -> re-normalised over price horizons
    b = s.bands(X)
    assert list(b.band) == ["green", "red", "yellow", "green"]
    assert list(b.exit_zone) == [False, True, False, False] and list(b.entry_zone) == [True, False, True, True]
    assert np.allclose(REGISTRY["hand_morris_woe"](task="exit").score(X), 100 - lv)
    # Price Short excluded by default (Morris part 6): flipping only mom / close-vs-EMA8 changes nothing
    X2 = X.copy()
    X2["mom"] = -X2["mom"]
    assert np.allclose(s.level(X2), lv)
    assert not np.allclose(REGISTRY["hand_morris_woe"](include_short=True).level(X2), lv)
    # band boundaries 30 / 50 / 80 (inclusive upper ends as in 0-30, 31-50, 51-80, 81-100)
    sb = REGISTRY["hand_morris_woe"](score_mode="band")
    assert list(sb.score(X)) == [3.0, 0.0, 2.0, 3.0]


def test_ndr_composite_and_zones():
    s = REGISTRY["hand_ndr_composite"]()
    st = ah.NDR_STATE
    row = {c: 1.0 for c in st}
    X = pd.DataFrame([row, {c: -1.0 for c in st}, {**row, **{c: -1.0 for c in st[:7]}}])
    X["fam_reversal"] = [1.0, 0.0, -1.0]                     # event votes only when it fires
    c = s.composite(X)
    n = len(st)
    assert np.allclose(c, [100, 0, 100 * (n - 7) / (n + 1)]), c
    z = s.zones(X)
    assert list(z.zone_bullish) == [True, False, False] and list(z.zone_bearish) == [False, True, True]
    assert np.allclose(REGISTRY["hand_ndr_composite"](task="exit").score(X), 100 - c)


def test_user_template_and_blank_skip():
    t = pd.read_csv(ah.USER_CSV, dtype=str, keep_default_na=False)
    assert list(t.columns) == ["signal", "entry_weight", "exit_weight", "note"]
    assert set(ah.spec_columns()) <= set(t.signal), "template must list every signal/feature"
    import features
    assert set(features.COLUMNS("ES")) <= set(t.signal)
    X = make_X(500)
    y = np.r_[np.zeros(250), np.ones(250)].astype(int)
    if (t.entry_weight.str.strip() == "").all():
        try:
            REGISTRY["hand_user"]().fit(X, y)
            raise AssertionError("blank template must raise")
        except HandWeightsMissingAlias as e:
            assert isinstance(e, NotFittedError) and getattr(e, "skip", False)
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "u.csv")
        pd.DataFrame({"signal": ["ema_stack"], "entry_weight": ["abc"], "exit_weight": [""], "note": [""]}).to_csv(p, index=False)
        try:
            REGISTRY["hand_user"](path=p).fit(X, y)
            raise AssertionError("non-numeric weight must raise ValueError")
        except ah.HandWeightsMissing:
            raise AssertionError("non-numeric weight is an error, not a skip")
        except ValueError:
            pass
        try:
            REGISTRY["hand_user"](path=os.path.join(tmp, "missing.csv")).fit(X, y)
            raise AssertionError("missing file must raise")
        except NotFittedError:
            pass
        assert REGISTRY["hand_user"](path=os.path.join(tmp, "missing.csv")).weights_table() is None


HandWeightsMissingAlias = ah.HandWeightsMissing


# ------------------------------------------------------------------------------------------------ review regressions
def test_calibration_survives_deepcopy_refit_and_pickle():
    """[major] The calibration must live in plain attributes: a deepcopy of a fitted scorer keeps ITS fold's
    calibration when the original is refit on other labels (no fold-to-fold leakage), and fitted scorers pickle."""
    import copy
    import pickle
    with tempfile.TemporaryDirectory() as tmp:
        for name in SCORERS:
            for task in ("entry", "exit"):
                X = make_X(4000, task, seed=21)
                rng = np.random.default_rng(21)
                yA = (rng.random(4000) < 1 / (1 + np.exp(-planted_logit(X, name, task)))).astype(int)
                yB = (rng.random(4000) < 0.15).astype(int)              # other fold: different base rate, no signal
                Xq = X.iloc[:200]
                A = build(name, task, tmp).fit(X, yA)
                pA = A.predict_proba(Xq)
                B = copy.deepcopy(A)
                A.fit(X, yB)                                            # refit the ORIGINAL
                assert not np.allclose(A.predict_proba(Xq), pA), f"{name}/{task}: refit should change A"
                assert np.allclose(B.predict_proba(Xq), pA), f"{name}/{task}: deepcopy changed after refitting A"
                C = pickle.loads(pickle.dumps(B))
                assert np.allclose(C.predict_proba(Xq), pA), f"{name}/{task}: pickle round trip changed predictions"
                assert not any(callable(v) for v in vars(A).values()), f"{name}/{task}: no closures on the instance"


def test_breakout_trade_tests_used():
    """[major] nr7.html Table 3 and InsideDays.html Table 7 (7% target / 7% stop, enter at the next open after a close
    beyond the pattern) feed inside_bar_breakout / nr7_breakout, pooled by trade count per breakout side."""
    r = ah.bulkowski_table().set_index(["pattern", "side"])
    expect = {("nr7_breakout", "bull"): (7600 + 920) / (7600 + 5791 + 920 + 1112),            # 55.2%
              ("nr7_breakout", "bear"): (4990 + 166) / (4990 + 6218 + 166 + 186),             # 44.6%
              ("inside_bar_breakout", "bull"): (7082 + 1315) / (7082 + 5375 + 1315 + 1514),   # 54.9%
              ("inside_bar_breakout", "bear"): (4837 + 1665) / (4837 + 6349 + 1665 + 1445)}   # 45.5%
    for k, p in expect.items():
        assert r.basis[k] == "published_trade", k
        assert abs(r.rate_textbook[k] - p) < 1e-12, (k, r.rate_textbook[k], p)
        assert abs(r.weight_logodds[k] - math.log(p / (1 - p))) < 1e-12 and r.weight_logodds[k] != 0, k
        assert "nr7.html" in r.url[k] or "InsideDays.html" in r.url[k], k
    assert abs(ah.trade_rate("inside_bar_breakout", "up", "pattern_stop") - 7237 / 15324) < 1e-12   # reference only
    # directional weights reach the score: an upward NR7 breakout on a long scores logit(55.2%)
    X = pd.DataFrame({"pat_nr7_breakout": [1.0, 1.0], "pat_inside_bar_breakout": [0.0, 0.0]})
    sd = REGISTRY["hand_bulkowski"](directional=True).score(X, d=np.array([1, -1]))
    assert np.allclose(sd, [r.weight_logodds["nr7_breakout", "bull"], r.weight_logodds["nr7_breakout", "bear"]])
    # outside_bar: the trade test enters after a LATER close beyond the range -> no number maps to our rule
    assert (r.weight_logodds.loc["outside_bar"] == 0).all() and r.note["outside_bar", "bull"].count("Table 7")
    # reviewer's preferred variant (InsideDays Table 8, pattern stop) is available on request; NR7 keeps Table 3
    ps = ah.bulkowski_table("pattern_stop").set_index(["pattern", "side"])
    up, dn = (5915 + 1322) / (5915 + 6580 + 1322 + 1507), (4266 + 1680) / (4266 + 6942 + 1680 + 1429)   # 47.2%, 41.5%
    assert abs(ps.rate_textbook["inside_bar_breakout", "bull"] - up) < 1e-12
    assert abs(ps.rate_textbook["inside_bar_breakout", "bear"] - dn) < 1e-12
    sym = (math.log(up / (1 - up)) + math.log(dn / (1 - dn))) / 2
    assert abs(sym - (-0.227)) < 5e-4 and abs(ps.weight_symmetric["inside_bar_breakout", "bull"] - sym) < 1e-9
    assert np.allclose(ps.weight_logodds.loc["nr7_breakout"], r.weight_logodds.loc["nr7_breakout"])
    others = ~ps.index.get_level_values(0).isin(["inside_bar_breakout"])
    assert np.allclose(ps.weight_logodds[others], r.weight_logodds[others])
    Xi = pd.DataFrame({"pat_inside_bar_breakout": [1.0, -1.0]})
    assert np.allclose(REGISTRY["hand_bulkowski"](breakout_table="pattern_stop").score(Xi), [sym, -sym])
    assert "pattern stop" in REGISTRY["hand_bulkowski"](breakout_table="pattern_stop", directional=True) \
        .weights_table().set_index("signal").meaning["pat_inside_bar_breakout:bull"]
    try:
        ah.bulkowski_table("bogus")
        raise AssertionError("unknown breakout_table must raise")
    except ValueError:
        pass


def test_marubozu_symmetric_not_mirrored():
    """[major] Default (symmetric) mode must not give the white marubozu the black marubozu's derived 66%: an
    unpublished side counts 0 in the mean, so the symmetric weight is logit(0.66) / 2."""
    t = ah.bulkowski_table()
    sym = t.groupby("pattern").weight_logodds.mean()
    assert np.allclose(t.weight_symmetric, t.pattern.map(sym).round(12)), "symmetric = mean over ALL sides (0 if unpublished)"
    w_black = math.log(0.66 / 0.34)
    X = pd.DataFrame({"pat_marubozu": [1.0, 1.0]})
    s = REGISTRY["hand_bulkowski"]().score(X)
    assert np.allclose(s, w_black / 2), s
    sd = REGISTRY["hand_bulkowski"](directional=True).score(X, d=np.array([1, -1]))     # white on a long, black on a short
    assert np.allclose(sd, [0.0, w_black]), sd
    csv = pd.read_csv(ah.BULKOWSKI_CSV).set_index(["pattern", "side"])
    assert abs(csv.weight_symmetric["marubozu", "bull"] - w_black / 2) < 1e-4, "regenerate bulkowski_weights.csv"


def test_gravestone_same_rule_as_dragonfly():
    """[minor] Neither page requires a prior trend, so neither reversal rate is a direction rate: both weight 0."""
    r = ah.bulkowski_table().set_index("pattern")
    for p in ("gravestone_doji", "dragonfly_doji"):
        assert r.basis[p] == "not_published" and r.weight_logodds[p] == 0 and r.weight_symmetric[p] == 0, p


def test_user_signal_names_checked():
    """[minor] hand_user must not drop misspelled weights silently."""
    import warnings
    X = make_X(500)
    y = np.r_[np.zeros(250), np.ones(250)].astype(int)
    with tempfile.TemporaryDirectory() as tmp:
        def csv(rows):
            p = os.path.join(tmp, "u.csv")
            pd.DataFrame(rows, columns=["signal", "entry_weight", "exit_weight", "note"]).to_csv(p, index=False)
            return p
        typo = csv([["ema_stak", "1.0", "", ""], ["pat_engulfng", "0.5", "", ""]])
        try:
            REGISTRY["hand_user"](path=typo).fit(X, y)
            raise AssertionError("typo in a signal name must raise")
        except ah.HandWeightsMissing:
            raise AssertionError("a typo is an error, not a skip")
        except ValueError as e:
            assert "ema_stak" in str(e) and "pat_engulfng" in str(e)
        one_typo = csv([["ema_stack", "1.0", "", ""], ["pat_engulfng", "0.5", "", ""]])
        try:
            REGISTRY["hand_user"](path=one_typo).fit(X, y)
            raise AssertionError("one typo among good names must still raise")
        except ValueError as e:
            assert not isinstance(e, ah.HandWeightsMissing) and "pat_engulfng" in str(e)
        exit_only = csv([["open_R", "0.8", "", ""]])                     # SPEC column, absent from entry rows
        try:
            REGISTRY["hand_user"](path=exit_only).fit(X, y)
            raise AssertionError("no weighted signal in X must raise HandWeightsMissing")
        except ah.HandWeightsMissing:
            pass
        partial = csv([["ema_stack", "1.0", "", ""], ["open_R", "0.8", "", ""]])
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            s = REGISTRY["hand_user"](path=partial).fit(X, y)
        assert any("open_R" in str(w.message) for w in wl), "absent SPEC column must warn"
        assert s.missing_ == ["open_R"] and np.isfinite(s.predict_proba(X)).all()
        ok = csv([["ema_stack", "1.0", "", ""]])
        with warnings.catch_warnings():
            warnings.simplefilter("error")                              # clean file: no warning at all
            REGISTRY["hand_user"](path=ok).fit(X, y)


def test_morris_published_hurdle_and_labels():
    """[minor] Morris part 13 hurdle per band is exposed; entry/exit zones and the omitted Adaptive Trend are labelled."""
    s = REGISTRY["hand_morris_woe"]()
    X = make_X(3000, seed=4)
    b = s.bands(X)
    assert set(b.band) <= {"red", "orange", "yellow", "green"}
    assert (b.buy_hurdle == b.band.map({"red": 60.0, "orange": 55.0, "yellow": 50.0, "green": 50.0})).all()
    t = s.weights_table()
    assert "(adaptive_trend)" in set(t.signal) and float(t.set_index("signal").weight["(adaptive_trend)"]) == 0.0
    assert all("Many times" in m for m in t.meaning[t.horizon == "short"]), "quote part 6 in full"
    assert "printed p.11" in ah.NDR_SRC and "p.10" not in ah.NDR_SRC


def test_rowwise_no_lookahead():
    """fit() sees only the rows it is given; a row's prediction depends on that row alone (no cross-row leakage)."""
    with tempfile.TemporaryDirectory() as tmp:
        for name in SCORERS:
            for task in ("entry", "exit"):
                X = make_X(6000, task, seed=11)
                y = (np.random.default_rng(11).random(6000) < 0.4).astype(int)
                Xtr, ytr = X.iloc[:3000], y[:3000]
                Xc = Xtr.copy()
                s1 = build(name, task, tmp).fit(Xtr, ytr)
                assert Xtr.equals(Xc), "fit must not modify X"
                y2 = y.copy()
                y2[3000:] = 1 - y2[3000:]                       # changing future labels cannot matter
                s2 = build(name, task, tmp).fit(X.iloc[:3000], y2[:3000])
                p_all = s1.predict_proba(X.iloc[3000:])
                assert np.allclose(p_all, s2.predict_proba(X.iloc[3000:]))
                assert np.allclose(p_all[:10], s1.predict_proba(X.iloc[3000:3010]))


def test_calibration_never_reverses_published_sign():
    """If the training rows contradict the hand weights, Platt is clipped to a flat base rate (unless allowed)."""
    X = make_X(N, seed=17)
    rng = np.random.default_rng(17)
    y = (rng.random(N) < 1 / (1 + np.exp(planted_logit(X, "hand_bulkowski", "entry")))).astype(int)   # reversed
    s = REGISTRY["hand_bulkowski"]().fit(X, y)
    p = s.predict_proba(X)
    assert s.platt_clipped_ and s.platt_a_ == 0 and np.allclose(p, y.mean(), atol=1e-6)
    s2 = REGISTRY["hand_bulkowski"](allow_negative_slope=True).fit(X, y)
    assert s2.platt_a_ < 0 and not s2.platt_clipped_


def test_unfitted_raises_and_speed():
    try:
        REGISTRY["hand_morris_woe"]().predict_proba(make_X(10))
        raise AssertionError("predict before fit must raise")
    except NotFittedError:
        pass
    X = make_X(200000, "entry", seed=13)
    y = (np.random.default_rng(13).random(len(X)) < 0.45).astype(int)
    out = {}
    for name in ("hand_bulkowski", "hand_morris_woe", "hand_ndr_composite"):
        t0 = time.time()
        REGISTRY[name]().fit(X, y).predict_proba(X)
        out[name] = time.time() - t0
        assert out[name] < 20, f"{name}: {out[name]:.1f}s for 200k rows"
    return out


if __name__ == "__main__":
    t0 = time.time()
    fails = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                r = f()
                print(f"PASS {k}" + (f"  {({kk: round(v, 3) for kk, v in r.items()})}" if isinstance(r, dict) else ""))
            except Exception:
                fails += 1
                print(f"FAIL {k}")
                traceback.print_exc()
    print(f"{'ALL PASSED' if not fails else f'{fails} FAILED'} in {time.time() - t0:.1f}s")
    sys.exit(1 if fails else 0)
