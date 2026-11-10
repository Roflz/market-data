"""
Tests for approach_stat.py (statistically derived weights). Synthetic candidates with SPEC.md column names.

  * planted entry signal (win odds rise with pat_engulfing = +1, ema_stack, dist_vwap): every stat_* scorer must rank
    out-of-sample winners higher (AUC well above 0.5) and give the planted signals positive weight where linear;
  * pure noise: out-of-sample AUC near 0.5, and the data-snooping screen keeps (almost) nothing;
  * exits: trade-state columns present, planted "with-trade evidence -> do not exit" (negative weight on ema_stack);
  * probabilities in [0, 1], weights_table well-formed (points = weight / (ln 2 / 20)), linear tables reproduce
    score(); the k-StepM screen rejects planted rules and controls false rejections on null columns.
Run:  cd approaches && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../../pylib:../../..:../../signals:..:. \
      python3 test_approach_stat.py
"""
from __future__ import annotations

import math
import time

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

import approach_stat as st
from scorer_api import REGISTRY

NAMES = sorted(k for k in REGISTRY if k.startswith("stat_"))
LINEAR = {"stat_screen_nb", "stat_screen_sa", "stat_screen_dma", "stat_screen_dms", "stat_screen_bma"}
FAILS = []


def check(msg, ok):
    print(f"  [{'ok' if ok else 'FAIL'}] {msg}")
    if not ok:
        FAILS.append(msg)


def make(task="entry", planted=True, n_days=320, per_day=22, seed=0):
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("2017-01-02", periods=n_days)
    n = n_days * per_day
    day = np.repeat(np.arange(n_days), per_day)
    minutes = rng.integers(0, 6 * 60, n)
    t = pd.DatetimeIndex(days[day]) + pd.to_timedelta(9 * 60 + 30 + minutes, unit="min")
    t = t.tz_localize("America/New_York")
    X = pd.DataFrame({
        "pat_engulfing": rng.choice([-1.0, 0.0, 1.0], n, p=[0.1, 0.65, 0.25]),
        "pat_hammer": rng.choice([-1.0, 0.0, 1.0], n, p=[0.1, 0.7, 0.2]),
        "pat_doji": rng.choice([0.0, 1.0], n, p=[0.85, 0.15]),
        "brk_5": rng.choice([-1.0, 0.0, 1.0], n, p=[0.1, 0.8, 0.1]),
        "struct_5": rng.choice([-1.0, 0.0, 1.0], n, p=[0.3, 0.4, 0.3]),
        "ema_stack": rng.choice([-1.0, 0.0, 1.0], n, p=[0.35, 0.3, 0.35]),
        "dist_vwap": rng.normal(0, 1, n),
        "mom": rng.normal(0, 1, n),
        "rng_rel": rng.lognormal(0, 0.4, n),
        "tod_open": rng.choice([0.0, 1.0], n, p=[0.8, 0.2]),
        "h1_ema_stack": rng.choice([-1.0, 0.0, 1.0], n),
        "x_NQ_ret": rng.normal(0, 1, n),
    })
    X["fam_reversal"] = np.clip(X.pat_engulfing + X.pat_hammer, -1, 1)
    X.loc[rng.random(n) < 0.05, "x_NQ_ret"] = np.nan
    if task == "exit":
        X["open_R"] = rng.normal(0.2, 1.0, n)
        X["mfe_R"] = np.abs(rng.normal(0.8, 0.6, n))
        X["mae_R"] = -np.abs(rng.normal(0.5, 0.4, n))
        X["bars_held"] = rng.integers(1, 33, n).astype(float)
        X["dist_stop_R"] = 1 + X["open_R"].clip(lower=-0.9)
        X["mins_to_1645"] = rng.integers(15, 400, n).astype(float)
    X = X.astype("float32")
    if planted and task == "entry":
        lo = -0.3 + 1.2 * (X.pat_engulfing == 1) + 0.7 * X.ema_stack + 0.5 * X.dist_vwap
    elif planted:
        lo = -0.3 - 0.9 * X.ema_stack + 0.8 * (X.open_R > 1.0) - 0.4 * X.dist_vwap
    else:
        lo = pd.Series(-0.2, index=X.index)
    y = (rng.random(n) < 1 / (1 + np.exp(-lo.to_numpy(float)))).astype(int)
    pnl = np.where(y == 1, 30.0, -20.0) + rng.normal(0, 5, n)
    meta = pd.DataFrame({"t": t, "t_end": t + pd.Timedelta(hours=2), "d": rng.choice([-1, 1], n),
                         "market": rng.choice(["ES", "NQ", "YM"], n), "year": t.year,
                         ("pnl_usd" if task == "entry" else "exit_gain_usd"): pnl,
                         "trade_id": np.arange(n) // 8})
    w = rng.uniform(0.5, 1.5, n)
    tr = day < int(0.7 * n_days)
    return X, y, w, meta, tr


def split(X, y, w, meta, tr):
    te = ~tr
    return (X[tr].reset_index(drop=True), y[tr], w[tr], meta[tr].reset_index(drop=True),
            X[te].reset_index(drop=True), y[te])


def table_ok(name, wt):
    cols = {"signal", "weight", "points", "meaning", "source"}
    ok = wt is not None and cols <= set(wt.columns) and len(wt) >= 1
    ok = ok and np.isfinite(wt["weight"]).all() and np.isfinite(wt["points"]).all()
    ok = ok and np.allclose(wt["points"], wt["weight"] / (math.log(2) / 20), rtol=1e-9, atol=1e-9)
    ok = ok and wt["signal"].map(lambda s: isinstance(s, str) and len(s) > 0).all()
    return ok


def run_task(task, planted, seed):
    X, y, w, meta, tr = make(task, planted, seed=seed)
    Xa, ya, wa, ma, Xb, yb = split(X, y, w, meta, tr)
    X0 = Xa.copy()
    out = {}
    for nm in NAMES:
        t0 = time.time()
        sc = REGISTRY[nm](task=task).fit(Xa, ya, wa, ma)
        p = sc.predict_proba(Xb)
        s = sc.score(Xb)
        auc = roc_auc_score(yb, p) if np.ptp(p) > 0 else 0.5
        wt = sc.weights_table()
        out[nm] = (sc, auc, p, s, wt, time.time() - t0)
    check(f"{task}: fit() leaves the training frame untouched", Xa.equals(X0))
    return out, (Xa, ya, Xb, yb)


def test_kstepm():
    rng = np.random.default_rng(3)
    T, S = 400, 60
    W = rng.normal(0, 1, (T, S))
    W[:, :3] += 0.35                                         # three genuinely profitable rules
    r = st.balanced_kstepm(W, k=1, alpha=0.10, B=2000, seed=1)
    check(f"k-StepM rejects the 3 planted rules (rejected {np.flatnonzero(r['rejected']).tolist()})",
          r["rejected"][:3].all())
    check("k-StepM: at most 1 false rejection among 57 nulls", r["rejected"][3:].sum() <= 1)
    nulls = [st.balanced_kstepm(rng.normal(0, 1, (300, 40)), k=1, alpha=0.10, B=1000, seed=s)["rejected"].any()
             for s in range(40)]
    check(f"k-StepM pure nulls: FWER {np.mean(nulls):.3f} over 40 runs (nominal 0.10)", np.mean(nulls) <= 0.225)
    r = st.balanced_kstepm(W, k=3, alpha=0.10, B=2000, seed=2, bootstrap="sb")
    check(f"k-StepM k=3, stationary bootstrap: planted rules rejected ({int(r['rejected'].sum())} rejections)",
          r["rejected"][:3].all())
    b = st.politis_white_block(np.convolve(rng.normal(size=600), np.ones(8) / 8, "same"))
    check(f"Politis-White block length > 1 on an MA(7) series ({b:.1f})", b > 2)
    C = st.stationary_bootstrap_counts(50, 30, 5.0, rng)
    check("stationary bootstrap draws T periods per replicate", np.all(C.sum(1) == 50))


def test_entry_planted():
    out, (Xa, ya, Xb, yb) = run_task("entry", True, seed=11)
    for nm, (sc, auc, p, s, wt, dt) in out.items():
        print(f"     {nm:20s} AUC {auc:.3f}  ({dt:.1f} s)")
        check(f"entry planted {nm}: OOS AUC well above 0.5", auc > 0.62)
        check(f"entry planted {nm}: probabilities in [0,1] and finite",
              np.isfinite(p).all() and p.min() >= 0 and p.max() <= 1)
        check(f"entry planted {nm}: weights_table well-formed", table_ok(nm, wt))
    sc = out["stat_screen_nb"][0]
    surv = sc.screen_[sc.screen_.survivor]
    print(f"     screen: {len(sc.screen_)} rules, k={sc.k_}, B={sc.B_}, block={sc.block_:.2f}, "
          f"{len(surv)} survivors: {surv.rule.tolist()[:8]}")
    check("screen keeps pat_engulfing = +1", "pat_engulfing = +1" in set(surv.rule))
    check("screen keeps ema_stack = +1", "ema_stack = +1" in set(surv.rule))
    for nm in LINEAR:
        sc, *_, wt, _ = out[nm]
        if len(sc.selected_):
            Xr = sc.rules_.matrix(Xb, sc.selected_)
            rec = wt.weight.iloc[0] + Xr @ wt.weight.iloc[1:1 + len(sc.selected_)].to_numpy()
            check(f"{nm}: weights_table reproduces score()", np.allclose(rec, out[nm][3], atol=1e-6))
            ww = dict(zip(wt.signal, wt.weight))
            check(f"{nm}: planted 'ema_stack = +1' weight > 0",
                  ww.get("ema_stack = +1", 1.0) > 0)
    wt = out["stat_shrink_combo"][4].set_index("signal")
    check("shrink_combo: ema_stack and dist_vwap weights > 0",
          wt.loc["ema_stack", "weight"] > 0 and wt.loc["dist_vwap", "weight"] > 0)
    print(f"     shrink_combo delta={out['stat_shrink_combo'][0].delta_}  "
          f"curve={ {k: round(v, 4) for k, v in out['stat_shrink_combo'][0].delta_curve_.items()} }")
    sc = out["stat_woe_scorecard"][0]
    print(f"     scorecard IV: {sc.iv_table_.head(5).round(4).to_dict('records')}")
    check("scorecard: ema_stack and dist_vwap pass IV >= 0.02",
          {"ema_stack", "dist_vwap"} <= {f['col'] for f in sc.feats_})
    sc = out["stat_screen_dma"][0]
    print(f"     DMA chose delta,lambda={sc.combo_[:2]} over {len(sc.grid_mse_)} pairs; {sc.model_desc_}")


def test_entry_noise():
    out, _ = run_task("entry", False, seed=22)
    for nm, (sc, auc, p, s, wt, dt) in out.items():
        print(f"     {nm:20s} AUC {auc:.3f}  ({dt:.1f} s)")
        check(f"entry noise {nm}: OOS AUC near 0.5", abs(auc - 0.5) < 0.06)
        check(f"entry noise {nm}: probabilities in [0,1]", np.isfinite(p).all() and 0 <= p.min() <= p.max() <= 1)
        check(f"entry noise {nm}: weights_table well-formed", table_ok(nm, wt))
    sc = out["stat_screen_nb"][0]
    check(f"noise: screen keeps <= 2 rules of {len(sc.screen_)} (kept {int(sc.screen_.survivor.sum())})",
          sc.screen_.survivor.sum() <= 2)
    sc = out["stat_woe_scorecard"][0]
    print(f"     noise scorecard kept {[f['col'] for f in sc.feats_]} (IV >= 0.02)")


def test_exit():
    out, _ = run_task("exit", True, seed=33)
    for nm, (sc, auc, p, s, wt, dt) in out.items():
        print(f"     {nm:20s} AUC {auc:.3f}  ({dt:.1f} s)")
        check(f"exit planted {nm}: OOS AUC well above 0.5", auc > 0.6)
        check(f"exit planted {nm}: probabilities in [0,1]", np.isfinite(p).all() and 0 <= p.min() <= p.max() <= 1)
        check(f"exit planted {nm}: weights_table well-formed", table_ok(nm, wt))
    wt = out["stat_shrink_combo"][4].set_index("signal")
    check("exit shrink_combo: with-trade ema_stack weight NEGATIVE (evidence to stay in)",
          wt.loc["ema_stack", "weight"] < 0)
    check("exit shrink_combo: trade_state family present", "family:trade_state" in wt.index)
    sc = out["stat_screen_nb"][0]
    surv = set(sc.screen_[sc.screen_.survivor].rule)
    check("exit screen keeps 'ema_stack = -1' (against-trade trend -> exit pays)", "ema_stack = -1" in surv)
    wtn = dict(zip(out["stat_screen_nb"][4].signal, out["stat_screen_nb"][4].weight))
    check("exit NB: 'ema_stack = +1' weight negative if selected", wtn.get("ema_stack = +1", -1.0) < 0)
    check("exit: payoff column used is exit_gain_usd", sc.payoff_kind_ == "usd:exit_gain_usd")


if __name__ == "__main__":
    T0 = time.time()
    print("registered:", NAMES)
    for fn in [test_kstepm, test_entry_planted, test_entry_noise, test_exit]:
        t = time.time()
        print(f"--- {fn.__name__}")
        fn()
        print(f"    ({time.time() - t:.1f} s)")
    if FAILS:
        print(f"{len(FAILS)} FAILED:")
        for f in FAILS:
            print("  -", f)
        raise SystemExit(1)
    print(f"ALL PASS ({time.time() - T0:.1f} s)")
