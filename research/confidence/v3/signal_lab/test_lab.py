"""
Synthetic-data proof that the signal lab measures what it claims (no market data needed, ~1-2 minutes):
  1. a planted DIRECTION effect is found with the right sign and size (true value inside the 95% CI)
  2. a planted SIZE effect (more movement after an event) is found, and is not mistaken for direction
  3. pure noise gives ~uniform p-values: false-positive rate ~5% at 0.05 (persistent signals, volatility clustering)
  4. overlapping horizons do not inflate the honest t (the naive bar-level t IS inflated)
  5. a future-peeking signal is caught by the truncation check (an honest one passes)
  6. power injection recovers the injected effect; batch false-discovery control + impact card render
  7. (v1.1) a RARE yes/no leak is caught at every seed and a failed check makes every verdict INVALID
  8. (v1.1) tradability is judged in $ per trade against the real $ cost (break-even = cost / mean R20)

Run (from research/confidence):
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/signal_lab OMP_NUM_THREADS=3 \
      python3 v3/signal_lab/test_lab.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import kstest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab as L  # noqa: E402

TF = 15
NS = 400
RESULTS = {}


def _within_session_lagsum(x, sess_code, lags):
    """sum_{k in lags} x[j-k] restricted to the same session (the planted forward effect of x)."""
    out = np.zeros_like(x)
    for k in lags:
        s = np.r_[np.zeros(k), x[:-k]]
        same = np.r_[np.zeros(k, bool), sess_code[k:] == sess_code[:-k]]
        out += np.where(same, s, 0.0)
    return out


def _codes(n_sessions, tf=TF):
    P = int(np.ceil(L.SESSION_MIN / tf))
    return np.repeat(np.arange(n_sessions), P)


def test_direction_planted():
    rng = np.random.default_rng(11)
    sc = _codes(NS)
    x = rng.standard_normal(len(sc))
    beta = 0.03                                                         # per bar, in units of the bar sd (=1)
    b = L.synthetic_bars(NS, TF, seed=12, extra_ret=beta * _within_session_lagsum(x, sc, (1, 2, 3, 4)))
    P = L.Panel(b, "ES", TF, n_boot=600)
    r = L.evaluate(P, x, "continuous", name="planted_dir")
    t = r["table"]
    # true effect: E[fwd_4 | x_i] = beta * (bars of i+1..i+4 inside the session) * x_i, in R20 units
    idx = np.arange(P.n)
    m4 = np.minimum(idx + 4, P.seg_end) - idx
    truth = beta * m4 * x / P.r20
    xv = np.where(P.ok, x, np.nan)
    q = np.nanquantile(xv, [0.2, 0.8])
    top, bot = P.ok & (x > q[1]), P.ok & (x <= q[0])
    true_e = truth[top].mean() - truth[bot].mean()
    e, lo, hi = t.at["dir_h4", "effect"], t.at["dir_h4", "ci_lo"], t.at["dir_h4", "ci_hi"]
    assert e > 0 and lo <= true_e <= hi, (e, lo, hi, true_e)
    assert abs(e / true_e - 1) < 0.35, (e, true_e)
    assert r["p_dir"] < 1e-4, r["p_dir"]
    assert t.at["dir_h4", "p_placebo_emp"] < 0.01
    # 1-bar effect is ~1/4 of the 4-bar effect; IC positive
    assert 0.1 < t.at["dir_h1", "effect"] / e < 0.45, t.at["dir_h1", "effect"] / e
    assert t.at["dir_h4", "ic"] > 0
    # no size effect planted
    assert r["p_size"] > 0.001, r["p_size"]
    RESULTS["direction"] = dict(true=true_e, est=e, ci=(lo, hi), p_dir=r["p_dir"], best=r["best_dir"])
    # sided version: long events when x > 1.5, short when x < -1.5
    sided = np.where(x > 1.5, 1.0, np.where(x < -1.5, -1.0, 0.0))
    r2 = L.evaluate(P, sided, "sided", name="planted_sided", power=False)
    ev = P.ok & (sided != 0)
    true_s = np.mean((sided * truth)[ev])
    t2 = r2["table"]
    # 99% interval (a single seed misses a 95% interval 1 time in 20 by design)
    assert abs(t2.at["dir_h4", "effect"] - true_s) < 2.58 * t2.at["dir_h4", "se_boot"], (t2.loc["dir_h4"], true_s)
    assert t2.at["path", "effect"] > 0                                  # favourable side touched first more often
    RESULTS["sided"] = dict(true=true_s, est=t2.at["dir_h4", "effect"], p_dir=r2["p_dir"])
    return P, x


def test_size_planted():
    rng = np.random.default_rng(21)
    sc = _codes(NS)
    ev = (rng.random(len(sc)) < 0.05).astype(float)
    hit = _within_session_lagsum(ev, sc, (1, 2, 3, 4)) > 0
    vm = np.where(hit, 1.6, 1.0)
    b = L.synthetic_bars(NS, TF, seed=22, vol_mult=vm)
    P = L.Panel(b, "ES", TF, n_boot=600)
    r = L.evaluate(P, ev, "event", name="planted_size")
    t = r["table"]
    assert r["p_size"] < 1e-6, r["p_size"]
    assert t.at["abs_h4", "effect"] > 0 and t.at["rng_h4", "effect"] > 0
    pct = t.at["abs_h4", "pct_vs_avg"]
    # planted: the 4 bars after an event have 1.6x volatility. Non-event bars are also hit ~14% of the time by a
    # nearby earlier event, so the expected contrast is ~1.6 / 1.1 -> about +45% (not +60%)
    assert 30 < pct < 65, pct
    assert r["p_dir"] > 0.01, r["p_dir"]                                # not mistaken for a direction effect
    RESULTS["size"] = dict(pct_abs_h4=pct, rng_h4=t.at["rng_h4", "effect"], p_size=r["p_size"], p_dir=r["p_dir"])


def _ar_within(rng, sc, rho):
    e = rng.standard_normal(len(sc))
    x = np.empty_like(e)
    x[0] = e[0]
    new = np.r_[True, sc[1:] != sc[:-1]]
    s = np.sqrt(1 - rho ** 2)
    for i in range(1, len(e)):
        x[i] = e[i] if new[i] else rho * x[i - 1] + s * e[i]
    return x


def test_noise_and_overlap(n_sig=160):
    b = L.synthetic_bars(NS, TF, seed=31, vol_cluster=0.9, u_shape=0.5)
    P = L.Panel(b, "ES", TF, n_boot=600)
    rng = np.random.default_rng(32)
    sc = P.sess_code
    rows = []
    for i in range(n_sig):
        a = _ar_within(rng, sc, 0.95)
        if i % 2 == 0:
            x, kind = a, "continuous"
        else:
            x, kind = np.where(a > 1.2, 1.0, np.where(a < -1.2, -1.0, 0.0)), "sided"
        r = L.evaluate(P, x, kind, name=f"noise{i}", power=False, event_study=False)
        t = r["table"]
        for c in ("dir_h4", "dir_h16", "abs_h4"):
            rows.append(dict(sig=i, kind=kind, col=c, p_boot=t.at[c, "p_boot"], p_nw=t.at[c, "p_nw"],
                             p_pl=t.at[c, "p_placebo"], p_pl_emp=t.at[c, "p_placebo_emp"], p=t.at[c, "p"],
                             p_rep=t.at[c, "p_repair"], p_rep_emp=t.at[c, "p_repair_emp"],
                             t_honest=t.at[c, "effect"] / t.at[c, "se_boot"], t_iid=t.at[c, "t_iid_bar"],
                             t_nwbar=t.at[c, "t_nw_bar"]))
        rows.append(dict(sig=i, kind=kind, col="p_dir", p=r["p_dir"]))
    D = pd.DataFrame(rows)
    fpr = D[D.col != "p_dir"].groupby("col")[["p_boot", "p_nw", "p_pl", "p_pl_emp", "p_rep", "p_rep_emp", "p"]].apply(lambda g: (g < 0.05).mean())
    pooled = D[D.col != "p_dir"]
    ks_boot = kstest(pooled.p_boot, "uniform").pvalue
    ks_pl = kstest(pooled.p_pl_emp, "uniform").pvalue
    fpr_dir = (D[D.col == "p_dir"].p < 0.05).mean()
    h16 = D[D.col == "dir_h16"]
    sd_honest, sd_iid = h16.t_honest.std(), h16.t_iid.std()
    RESULTS["noise"] = dict(fpr=fpr.round(3).to_dict(), ks_boot=ks_boot, ks_placebo=ks_pl, fpr_p_dir=fpr_dir,
                            sd_t_honest_h16=sd_honest, sd_t_naive_h16=sd_iid, sd_t_nwbar_h16=h16.t_nwbar.std())
    # 3. calibration: each method's false-positive rate ~5% (binomial sd with 480 tests ~1%)
    for col in ("p_boot", "p_nw", "p_pl", "p_pl_emp", "p_rep", "p_rep_emp"):
        rate = (pooled[col] < 0.05).mean()
        assert 0.02 <= rate <= 0.09, (col, rate)
    assert (pooled.p < 0.05).mean() <= 0.09
    assert fpr_dir <= 0.09, fpr_dir
    assert ks_boot > 0.001 and ks_pl > 0.001, (ks_boot, ks_pl)
    # 4. overlapping 16-bar horizons + persistent signal: naive t inflated, honest t ~ N(0,1)
    assert 0.75 < sd_honest < 1.3, sd_honest
    assert sd_iid > 1.5 * sd_honest, (sd_iid, sd_honest)


def test_lookahead():
    b = L.synthetic_bars(120, TF, seed=41)

    def peek(bb):                                    # uses the NEXT bar's close: future information
        return np.sign(bb.C.shift(-1) - bb.C)

    def zscore_global(bb):                           # full-sample normalisation: also look-ahead
        g = bb.C - bb.ema20
        return (g - g.mean()) / g.std()

    def honest(bb):
        return (bb.C - bb.ema20) / bb.atr14

    r_peek = L.lookahead_check(peek, b, n_cuts=4)
    r_z = L.lookahead_check(zscore_global, b, n_cuts=4)
    r_ok = L.lookahead_check(honest, b, n_cuts=4)
    assert not r_peek["ok"] and not r_z["ok"] and r_ok["ok"], (r_peek, r_z, r_ok)
    # a peeking signal also shows an absurd 1-bar effect: the check is what flags it as invalid
    P = L.Panel(b, "ES", TF, n_boot=200)
    r = L.evaluate(P, peek(b).to_numpy(), "sided", name="peek", power=False, placebo=False)
    RESULTS["lookahead"] = dict(peek=r_peek, zscore=r_z, honest=r_ok, peek_effect_h1=r["table"].at["dir_h1", "effect"])


def test_power_and_batch(P=None, x=None):
    if P is None:
        P, x = test_direction_planted()
    r = L.evaluate(P, np.random.default_rng(51).standard_normal(P.n), "continuous", name="n", delta=0.10, n_power=30)
    pw = r["power"]
    assert abs(pw["injected_recovered"] - 0.10) < 0.002, pw         # ~exact (weights use the unshifted shares)
    r_small = L.evaluate(P, np.random.default_rng(51).standard_normal(P.n), "continuous", name="n", delta=0.02,
                         n_power=30, placebo=False)
    assert pw["detect_rate"] >= r_small["power"]["detect_rate"], (pw, r_small["power"])
    rng = np.random.default_rng(52)
    sig = {"planted": (x, "continuous")}
    for i in range(8):
        sig[f"noise{i}"] = (rng.standard_normal(P.n), "continuous")
    out = os.path.join(L.OUT, "test")
    B, res = L.evaluate_many(sig, panels={("ES", TF): P}, out_dir=out, verbose=False, n_power=10)
    planted = B[B.metric == "planted"].iloc[0]
    assert planted.q_dir < 0.05 and planted.rw_dir < 0.05, planted
    assert (B[B.metric != "planted"].q_dir > 0.05).all(), B[["metric", "q_dir"]]
    # v1 four-way verdict: the planted (real) effect is REAL; noise metrics are never called REAL
    assert planted.dir_class.startswith(("REAL BUT TOO SMALL", "REAL & TRADABLE")), planted.dir_class
    assert planted.lookahead == "UNCHECKED" and planted.dir_class.endswith(L.UNCHECKED_TAG), planted  # given as numbers
    assert not B[B.metric != "planted"].dir_class.str.startswith("REAL").any(), B[["metric", "dir_class"]]
    # v1 injection into a real-data-like panel: a +0.10 R20 jump after +-1 events is recovered by the full pipeline
    rng = np.random.default_rng(77)
    sd = np.where(rng.random(P.n) < 0.03, np.where(rng.random(P.n) < 0.5, 1.0, -1.0), 0.0)
    Q = P.injected(0.10 * sd)
    r0 = L.evaluate(P, sd, "sided", name="inj0", power=False, event_study=False)
    r1 = L.evaluate(Q, sd, "sided", name="inj1", power=False, event_study=False)
    d = r1["table"].loc[L.DIR, "effect"] - r0["table"].loc[L.DIR, "effect"]
    assert np.allclose(d, 0.10, atol=0.01), d
    assert r1["table"].at["dir_h1", "p_repair_emp"] < 0.05, r1["table"].loc["dir_h1"]
    card = open(os.path.join(out, "cards", "planted.md")).read()
    assert "Impact card: planted" in card and "moves price up" in card, card[:2000]
    RESULTS["power"] = dict(delta=0.10, detect=pw["detect_rate"], mde80=pw["mde80"],
                            detect_at_0_02=r_small["power"]["detect_rate"])
    RESULTS["batch"] = dict(planted_q=planted.q_dir, planted_rw=planted.rw_dir, planted_verdict=planted.dir_verdict,
                            planted_class=planted.dir_class, injected_recovered=float(d.mean()),
                            min_noise_q=float(B[B.metric != "planted"].q_dir.min()))


def _inside_breakout(leak):
    """Inside bar (H < prev H, L > prev L) traded in a breakout direction. leak=True labels it with the direction its
    NEXT bar closes beyond the inside bar (future information, ~ the realistic candle-pattern leak); leak=False uses
    this bar's own close vs its midpoint (honest)."""
    def fn(bb):
        ins = (bb.H < bb.H.shift(1)) & (bb.L > bb.L.shift(1)) & bb.seg.eq(bb.seg.shift(1))
        if leak:
            up, dn = ins & (bb.C.shift(-1) > bb.H), ins & (bb.C.shift(-1) < bb.L)
        else:
            mid = (bb.H + bb.L) / 2
            up, dn = ins & (bb.C > mid), ins & (bb.C < mid)
        return pd.Series(np.where(up, 1.0, np.where(dn, -1.0, 0.0)), index=bb.index)
    return fn


def test_lookahead_rare():
    """v1.1: a RARE yes/no leak (changes the value only on event bars) is caught at every seed; the honest twin passes;
    the old 3-random-cut test missed it most of the time."""
    b = L.synthetic_bars(400, TF, seed=43)
    leaky, honest = _inside_breakout(True), _inside_breakout(False)
    share = float((leaky(b) != 0).mean())
    caught = [not L.lookahead_check(leaky, b, seed=s)["ok"] for s in range(10)]
    clean = [L.lookahead_check(honest, b, seed=s)["ok"] for s in range(5)]
    old_missed = sum(L.lookahead_check(leaky, b, n_cuts=3, seed=s)["ok"] for s in range(20))
    r = L.lookahead_check(leaky, b)
    assert all(caught), caught
    assert all(clean), clean
    assert r["n_bad_target"] > 0.9 * r["n_target"], r                   # every cut at an event bar exposes the leak

    def crashes(bb):                                                   # crash on truncated data = cannot verify
        if len(bb) < len(b):
            raise RuntimeError("needs the full sample")
        return bb.C - bb.ema20
    assert not L.lookahead_check(crashes, b, n_random=3, n_target=0)["ok"]
    RESULTS["lookahead_rare"] = dict(event_share=round(share, 4), caught_new=f"{sum(caught)}/10",
                                     honest_passed=f"{sum(clean)}/5", old_3cut_missed=f"{old_missed}/20",
                                     target_cuts_failed=f"{r['n_bad_target']}/{r['n_target']}",
                                     random_cuts_failed=f"{r['n_bad_random']}/{r['n_random']}")


def test_verdict_override(P):
    """v1.1: a FAILED look-ahead test overrides a statistically strong result to INVALID everywhere."""
    leaky = _inside_breakout(True)
    out = os.path.join(L.OUT, "test")
    B, res = L.evaluate_many({"leaky_inside": dict(fn=leaky, kind="sided"),
                              "honest_inside": dict(fn=_inside_breakout(False), kind="sided")},
                             panels={("ES", TF): P}, out_dir=out, verbose=False, n_power=5)
    lk = B[B.metric == "leaky_inside"].iloc[0]
    ho = B[B.metric == "honest_inside"].iloc[0]
    assert lk.p_dir < 1e-6, lk.p_dir                                     # the peek fakes a huge 'edge' ...
    assert lk.lookahead == "FAILED" and lk.dir_verdict == "INVALID" and lk.size_verdict == "INVALID", lk
    assert lk.dir_class == L.INVALID_CLASS, lk.dir_class                 # ... which the verdict refuses
    assert ho.lookahead == "passed" and ho.dir_verdict != "INVALID", ho
    card = open(os.path.join(out, "cards", "leaky_inside.md")).read()
    assert "INVALID" in card and "FAILED" in card and "CONFIRMED" not in card, card[:3000]
    # evaluate() with a function runs the check too
    r = L.evaluate(P, leaky, "sided", name="leaky_single", power=False, event_study=False)
    assert r["lookahead"]["status"] == "FAILED" and L.batch_table([r]).iloc[0].dir_class == L.INVALID_CLASS
    RESULTS["override"] = dict(leaky_p_dir=float(lk.p_dir), leaky_effect=float(lk.dir_effect),
                               leaky_verdict=lk.dir_verdict, leaky_class=lk.dir_class, honest_class=ho.dir_class)


def test_dollar_tradability():
    """v1.1: tradability is judged in $ per trade against the real $ cost. Bars whose size varies a lot (volatility
    clustering): an edge of e R20 per trade earns e x MEAN R20 x $/pt, and the break-even edge is cost / mean R20,
    below the old mean(cost / R20) bar."""
    b = L.synthetic_bars(700, TF, seed=61, vol_cluster=0.9, start="2016-06-01")
    rng = np.random.default_rng(62)
    n = len(b)
    sd = np.where(rng.random(n) < 0.05, np.where(rng.random(n) < 0.5, 1.0, -1.0), 0.0)
    out = {}
    for cost, edge, want in ((1.0, 0.30, "REAL & TRADABLE"), (6.0, 0.30, "REAL BUT TOO SMALL"),
                             (3.0, 0.0, "CONFIDENTLY NOTHING")):
        spec = dict(tick=0.01, usd=5.0, cost=cost)
        P = L.Panel(b, "ES", TF, n_boot=400, spec=spec)
        Q = P.injected(edge * sd) if edge else P
        r = L.evaluate(Q, sd, "sided", name="dollar", power=False, event_study=False, ic=False)
        r["lookahead"] = dict(ok=True)                                 # synthetic numbers: honest by construction
        row = L.batch_table([r]).iloc[0]
        ev = P.ok & (sd != 0)
        eraB = P.year_s[P.sess_code] >= 2018
        mean_r20 = P.r20[ev].mean()
        old_bar = np.mean(P.cost_pts / P.r20[ev])
        assert abs(r["breakeven_r20"] - P.cost_pts / max(mean_r20, P.r20[ev & eraB].mean())) < 1e-9
        assert r["breakeven_r20"] < old_bar, (r["breakeven_r20"], old_bar)          # Jensen: old bar too high
        t = r["table"]
        truth_B = edge * P.r20[ev & eraB].mean() * P.usd
        assert abs(t.at["dir_h1", "trade_usd_B"] - truth_B) < 3 * t.at["dir_h1", "trade_usd_B_se"] + 1e-9, \
            (t.at["dir_h1", "trade_usd_B"], truth_B)
        assert row.dir_class == want, (cost, edge, row.dir_class, row.edge_usd_B_lo80, row.cost_usd)
        out[want] = dict(cost=cost, edge_r20=edge, edge_usd_B=round(float(row.edge_usd_B), 2),
                         lo80=round(float(row.edge_usd_B_lo80), 2), breakeven_r20=round(r["breakeven_r20"], 4),
                         old_bar_r20=round(float(old_bar), 4))
    RESULTS["dollars"] = out


if __name__ == "__main__":
    t0 = time.time()
    P, x = test_direction_planted()
    print("direction ok", RESULTS["direction"], RESULTS["sided"], f"{time.time() - t0:.1f}s", flush=True)
    test_size_planted()
    print("size ok", RESULTS["size"], f"{time.time() - t0:.1f}s", flush=True)
    test_lookahead()
    print("lookahead ok", RESULTS["lookahead"], f"{time.time() - t0:.1f}s", flush=True)
    test_power_and_batch(P, x)
    print("power/batch ok", RESULTS["power"], RESULTS["batch"], f"{time.time() - t0:.1f}s", flush=True)
    test_lookahead_rare()
    print("lookahead rare ok", RESULTS["lookahead_rare"], f"{time.time() - t0:.1f}s", flush=True)
    test_verdict_override(P)
    print("verdict override ok", RESULTS["override"], f"{time.time() - t0:.1f}s", flush=True)
    test_dollar_tradability()
    print("dollar tradability ok", RESULTS["dollars"], f"{time.time() - t0:.1f}s", flush=True)
    test_noise_and_overlap()
    print("noise/overlap ok", RESULTS["noise"], f"{time.time() - t0:.1f}s", flush=True)
    print(f"ALL PASSED in {time.time() - t0:.1f}s")
