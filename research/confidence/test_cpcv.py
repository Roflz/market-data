"""Tests for cpcv.py on synthetic data (no market data):
  groups / splits / paths (C(8,2) = 28 splits, phi = 7 paths, every path covers every group once), purge + embargo
  correctness, a PLANTED signal (most CPCV paths positive), PURE NOISE (paths centred on 0), DSR against the paper's
  worked example and on noise / planted trials, PBO on noise (~0.5) and with a real best configuration (~0).
Run:
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_cpcv.py
"""
import math
import warnings

import numpy as np
import pandas as pd

import cpcv
import walkforward as wf

warnings.filterwarnings("ignore")


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    assert cond, name


def make_events(beta, per_year=1500, years=range(2010, 2026), seed=1):
    """One market, events on random weekday minutes; outcome depends on the oriented feature f_sig (beta);
    win +$27 / loss -$23, break-even win rate 0.46 (with beta = 0 the expected $ is 0)."""
    rng = np.random.default_rng(seed)
    t = []
    for y in years:
        day = rng.integers(0, 181 if y == 2025 else 360, per_year)
        minute = rng.integers(9 * 60 + 30, 15 * 60 + 30, per_year)
        t.append(pd.Timestamp(y, 1, 1) + pd.to_timedelta(day, "D") + pd.to_timedelta(minute, "min"))
    t = pd.DatetimeIndex(np.sort(np.concatenate([x.to_numpy() for x in t])))
    n = len(t)
    t_end = t + pd.to_timedelta(rng.integers(15, 240, n), "min")
    f_sig, f_n1, f_n2 = rng.normal(0, 1, (3, n))
    if beta == 0:
        win = rng.random(n) < 23 / 50
    else:
        win = rng.random(n) < 1 / (1 + np.exp(-(-0.2 + beta * f_sig)))
    pnl = np.where(win, 27.0, -23.0)
    X = np.c_[f_sig, f_n1, f_n2].astype(np.float32)
    return dict(t=t, t_end=t_end, X=X, y=win.astype(np.int8), pnl=pnl, year=t.year.to_numpy(),
                w=np.ones(n), sess=(t + pd.Timedelta(hours=6)).normalize())


def test_structure():
    splits = cpcv.split_combinations(8, 2)
    check("C(8,2) = 28 splits", len(splits) == 28)
    check("phi[8,2] = 7 paths", cpcv.n_paths(8, 2) == 7 and cpcv.n_paths(6, 2) == 5 and cpcv.n_paths(10, 3) == 36)
    P = cpcv.path_matrix(8, splits)
    check("path matrix 7 x 8", P.shape == (7, 8))
    ok = all(8 > g and g in splits[P[j, g]] for j in range(7) for g in range(8))
    check("path j / group g uses a split that tests group g", ok)
    check("each group's 7 paths use 7 different splits", all(len(set(P[:, g])) == 7 for g in range(8)))
    used = np.bincount(P.ravel(), minlength=28)
    check("every split feeds exactly k = 2 path cells", (used == 2).all())
    ev = make_events(0.0, per_year=300)
    g = cpcv.make_groups(ev["t"], 8)
    check("8 contiguous non-empty groups", (np.diff(g) >= 0).all() and set(g) == set(range(8)))
    sz = np.bincount(g)
    check(f"near-equal group sizes {sz.min()}..{sz.max()}", sz.max() / sz.min() < 1.1)
    s = np.asarray(ev["sess"])
    b = np.flatnonzero(np.diff(g)) + 1
    check("group boundaries fall on session starts (no session split)", all(s[i] != s[i - 1] for i in b))
    blocks = cpcv.test_blocks(g, (2, 3))
    check("adjacent test groups form one block", len(blocks) == 1)
    check("separate test groups form two blocks", len(cpcv.test_blocks(g, (1, 5))) == 2)


def test_purge_embargo():
    rng = np.random.default_rng(5)
    ev = make_events(0.0, per_year=400, seed=5)
    t, n = ev["t"], len(ev["t"])
    # some labels last up to 30 days so that purging is visible
    t_end = t + pd.to_timedelta(np.where(rng.random(n) < 0.05, rng.integers(1, 30 * 24 * 60, n),
                                         rng.integers(15, 240, n)), "min")
    g = cpcv.make_groups(t, 8)
    tt, te = t.as_unit("ns").asi8, t_end.as_unit("ns").asi8
    purge = pd.Timedelta(days=1)
    for comb in [(0, 1), (2, 5), (3, 4), (6, 7), (0, 7)]:
        m = cpcv.cpcv_train_mask(t, t_end, g, comb, purge=purge, embargo_frac=0.01)
        test = np.isin(g, comb)
        bad_overlap = False
        emb_ok = True
        for a, b in cpcv.test_blocks(g, comb):
            t0, t1 = tt[a] - purge.value, te[a:b + 1].max()
            bad_overlap |= bool((m & (tt <= t1) & (te > t0)).any())
            h = math.ceil(0.01 * n)
            emb_ok &= not m[b + 1:b + 1 + h].any()
        check(f"split {comb}: train and test disjoint", not (m & test).any())
        check(f"split {comb}: no training label window overlaps a test block (+1 day purge)", not bad_overlap)
        check(f"split {comb}: 1% embargo after each test block", emb_ok)
        # nothing else removed: every non-test row that is neither overlapping nor embargoed is kept
        drop = test.copy()
        for a, b in cpcv.test_blocks(g, comb):
            drop |= (tt <= te[a:b + 1].max()) & (te > tt[a] - purge.value)
            drop[b + 1:b + 1 + math.ceil(0.01 * n)] = True
        check(f"split {comb}: only test / purged / embargoed rows are removed", (m == ~drop).all())
    # hand-made: a training row before the block whose label runs into the block is purged
    t2 = pd.DatetimeIndex(pd.date_range("2020-01-01 10:00", periods=40, freq="D"))
    te2 = t2 + pd.Timedelta(hours=1)
    te2 = te2.where(np.arange(40) != 9, t2[11] + pd.Timedelta(hours=2))   # row 9's label ends inside group 1
    g2 = cpcv.make_groups(t2, 4)                                        # 10 rows per group
    m2 = cpcv.cpcv_train_mask(t2, te2, g2, (1,), embargo_frac=0.0, embargo_sessions=2)
    check("hand: row 9 (label ends inside the test block) purged", not m2[9])
    check("hand: row 8 kept", m2[8])
    check("hand: 2-session embargo drops rows 20, 21, keeps 22", (not m2[20]) and (not m2[21]) and m2[22])


def _cpcv(beta, seed):
    ev = make_events(beta, seed=seed)
    fit = cpcv.wf_fitter("logit", ev["X"], ev["y"], ev["w"], ev["pnl"], ev["year"],
                         ev["t_end"].as_unit("ns").to_numpy(), min_keep=0.05)
    res = cpcv.run_cpcv(ev["X"], ev["y"], ev["pnl"], ev["t"], ev["t_end"], fit, n_groups=8, k=2,
                        purge=pd.Timedelta(days=1), embargo_frac=0.01)
    yrs = (ev["t"].max() - ev["t"].min()) / pd.Timedelta(days=365.25)
    ps = cpcv.path_stats(res, ev["pnl"], np.asarray(ev["sess"]), yrs)
    return ev, res, ps


def test_planted_and_noise():
    ev, res, ps = _cpcv(0.6, seed=11)
    check("planted: 28 splits fitted", len(res.splits) == 28)
    check("planted: every row predicted on all 7 paths", np.isfinite(res.p).all())
    check(f"planted: all 7 paths positive (min $/trade {ps.usd_per_trade.min():.2f})", (ps.usd_per_trade > 0).all())
    check(f"planted: median path $/trade {ps.usd_per_trade.median():.2f} > all-events "
          f"{ev['pnl'].mean():.2f}", ps.usd_per_trade.median() > ev["pnl"].mean() + 2)
    ev0, res0, ps0 = _cpcv(0.0, seed=12)
    med = ps0.usd_per_trade.median()
    se = 50 / math.sqrt(max(ps0.n_trades.median(), 1))
    check(f"noise: median path $/trade {med:.2f} within 3 SE ({3 * se:.2f}) of 0", abs(med) < 3 * se)
    check(f"noise: paths not uniformly positive ({(ps0.usd_per_trade > 0).sum()}/7)",
          (ps0.usd_per_trade > 0).sum() < 7 or med < 2 * se)
    rnd = cpcv.random_skip_paths(ev0["pnl"], ps0.n_trades.to_numpy(), n_draws=50)
    check("random-skip baseline shape", rnd.shape == (7, 50))


def test_dsr():
    # paper example [DSR]: N=100, V[SR] = 1/2 (annualized), T = 1250 daily obs, SR 2.5 annualized, skew -3, kurt 10
    sr = 2.5 / math.sqrt(250)
    sr0 = cpcv.expected_max_sharpe(100, 0.5 / 250)
    check(f"expected-max bracket for N=100, V=1: {cpcv.expected_max_sharpe(100, 1.0):.3f} ~ 2.531",
          abs(cpcv.expected_max_sharpe(100, 1.0) - 2.531) < 0.002)
    check(f"paper SR0 = {sr0:.4f} ~ 0.1132", abs(sr0 - 0.1132) < 0.0005)
    d = cpcv.psr(sr, sr0, 1250, -3, 10)
    check(f"paper DSR (N=100) = {d:.4f} ~ 0.9004", abs(d - 0.9004) < 0.001)
    d46 = cpcv.psr(sr, cpcv.expected_max_sharpe(46, 0.5 / 250), 1250, -3, 10)
    check(f"paper DSR (N=46) = {d46:.4f} ~ 0.9505", abs(d46 - 0.9505) < 0.001)
    check("SR0 = 0 for one trial (DSR = PSR)", cpcv.expected_max_sharpe(1, 1.0) == 0.0)
    # noise trials: pick the best of 100; its DSR must be low
    rng = np.random.default_rng(3)
    R = rng.normal(0, 1, (1250, 100))
    srs = np.array([cpcv.sharpe(R[:, i]) for i in range(100)])
    best = int(np.argmax(srs))
    out = cpcv.deflated_sharpe(R[:, best], 100, srs.var(ddof=1))
    check(f"noise: best-of-100 PSR(0) {out['psr0']:.3f} looks good but DSR {out['dsr']:.3f} < 0.9",
          out["dsr"] < 0.9 and out["psr0"] > out["dsr"])
    # a real edge (daily SR 0.15, ~2.4 annualized) survives 100 trials
    R[:, 0] = rng.normal(0.15, 1, 1250)
    srs[0] = cpcv.sharpe(R[:, 0])
    out2 = cpcv.deflated_sharpe(R[:, 0], 100, srs.var(ddof=1))
    check(f"planted: DSR {out2['dsr']:.3f} > 0.95", out2["dsr"] > 0.95)
    sk, ku = cpcv.moments(rng.normal(0, 1, 200000))
    check(f"moments of Normal: skew {sk:.3f} ~ 0, kurtosis {ku:.3f} ~ 3 (not excess)", abs(sk) < 0.03 and abs(ku - 3) < 0.05)


def test_pbo():
    rng = np.random.default_rng(7)
    pbos = [cpcv.pbo_cscv(rng.normal(0, 1, (480, 40)), S=12)["pbo"] for _ in range(6)]
    m = float(np.mean(pbos))
    check(f"noise: mean PBO {m:.3f} near 0.5 (each {np.round(pbos, 2).tolist()})", 0.35 < m < 0.65)
    M = rng.normal(0, 1, (480, 40))
    M[:, 17] += 0.5
    r = cpcv.pbo_cscv(M, S=12)
    check(f"one real best config: PBO {r['pbo']:.3f} < 0.05, chosen mostly #17", r["pbo"] < 0.05 and
          r["chosen"].argmax() == 17)
    check(f"C(12, 6) = 924 combinations ({r['n_combos']})", r["n_combos"] == 924)
    r2 = cpcv.pbo_cscv(M, S=12, metric="sharpe")
    check(f"sharpe metric works (PBO {r2['pbo']:.3f})", r2["pbo"] < 0.05)
    # hand check of the logit/rank: N = 3 configurations, S = 2
    M3 = np.array([[1.0, 0.0, 0.5], [0.0, 1.0, 0.5]])
    r3 = cpcv.pbo_cscv(M3, S=2)
    # combo (0,): IS row 0 -> n*=0, OOS row 1 values (0,1,.5) -> rank 1 -> w = 1/4 -> logit < 0; same mirrored
    check("hand: IS-best is OOS-worst in both halves -> PBO 1, logit ln(1/3)",
          r3["pbo"] == 1.0 and np.allclose(r3["logits"], math.log(1 / 3)))


def test_threshold_chosen_before_test():
    """C and the threshold come from validation years BEFORE the tested groups whenever the earlier training rows
    allow it; only splits whose tests start too early to allow that fall back to later years, and are flagged."""
    ev = make_events(0.3, seed=21)
    fit = cpcv.wf_fitter("logit", ev["X"], ev["y"], ev["w"], ev["pnl"], ev["year"],
                         ev["t_end"].as_unit("ns").to_numpy(), min_keep=0.05)
    res = cpcv.run_cpcv(ev["X"], ev["y"], ev["pnl"], ev["t"], ev["t_end"], fit, n_groups=8, k=2,
                        purge=pd.Timedelta(days=1), embargo_frac=0.01)
    S = res.splits
    grp_start = {g: pd.Timestamp(np.min(np.asarray(ev["t"])[res.groups == g])) for g in range(8)}
    before = S[S.val_after_test == 0]
    ok_years = all(int(str(r.val_years).split("-")[1]) <= grp_start[int(r.test_groups.split("+")[0])].year
                   for r in before.itertuples())
    check(f"{len(before)}/28 splits tune before their test; their validation years end by the test start", ok_years)
    check("splits whose first test group is 0 or 1 cannot tune before the test and are flagged",
          (S[S.test_groups.str.startswith(("0+", "1+"))].val_after_test == 1).all())
    check("most splits tune before the test", len(before) >= 14)


if __name__ == "__main__":
    test_structure()
    test_purge_embargo()
    test_dsr()
    test_pbo()
    test_planted_and_noise()
    test_threshold_chosen_before_test()
    print("ALL PASS")
