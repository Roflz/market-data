"""Sanity tests for stats_protocol.py (synthetic data only; light). Run: python3 v3/test_stats_protocol.py"""
import numpy as np

import stats_protocol as sp


def test_indices():
    idx = sp.stationary_indices(500, 10, 50, seed=1)
    assert idx.shape == (50, 500) and idx.min() >= 0 and idx.max() < 500
    starts = np.mean(np.diff(idx, axis=1) != 1) - np.mean(np.diff(idx, axis=1) == -499)
    assert 0.07 < starts < 0.13, starts  # ~1/10 of days start a new block


def test_holm_bh():
    p = np.array([0.01, 0.04, 0.03, 0.005])
    assert np.allclose(sp.holm(p), [0.03, 0.06, 0.06, 0.02])
    assert np.allclose(sp.bh(p), [0.02, 0.04, 0.04, 0.02])


def test_block_length():
    rng = np.random.default_rng(0)
    e = rng.standard_normal(3000)
    ar = np.empty(3000)
    ar[0] = e[0]
    for i in range(1, 3000):
        ar[i] = 0.6 * ar[i - 1] + e[i]
    b_ar = sp.politis_white_block(ar)[0]
    b_iid = sp.politis_white_block(e)[0]
    assert b_ar > 4 and b_iid < 3, (b_ar, b_iid)


def test_size_and_power():
    rng = np.random.default_rng(2)
    rej_spa = rej_step = rej_one = 0
    reps = 60
    for r in range(reps):
        D = rng.standard_t(4, (800, 20)) * 50
        rej_spa += sp.spa(D, 10, 300, seed=r)["p_c"] <= 0.05
        rej_step += sp.stepm(D, 10, 300, seed=r)["reject"].any()
        rej_one += sp.boot_pvalue_mean(D[:, 0], 10, 300, seed=r)["p_boot"] <= 0.05
    # familywise error near or below 5% (loose bounds for 60 reps)
    assert rej_spa / reps <= 0.15 and rej_step / reps <= 0.15 and rej_one / reps <= 0.15, (rej_spa, rej_step, rej_one)
    D = rng.standard_t(4, (2500, 20)) * 50
    D[:, 3] += 50 * np.sqrt(2) * 0.12  # one real edge, t ~ 4.2
    out = sp.stepm(D, 10, 500, seed=9)
    assert out["reject"][3] and out["reject"].sum() <= 2, out["p_adj"]
    assert sp.spa(D, 10, 500, seed=9)["p_c"] <= 0.01


def test_pipeline_null_and_dsr():
    rng = np.random.default_rng(3)
    D = rng.standard_normal((600, 10))
    res = sp.pipeline_null(D, lambda X: np.sqrt(len(X)) * X.mean(0).max() / X.std(0).mean(), 10, 200, seed=1)
    assert 0.0 < res["p"] <= 1.0
    assert abs(sp.dsr_t_bar(1) - 1.645) < 1e-3
    assert sp.days_needed(1.0, 3.0, 0.5) > 2200


if __name__ == "__main__":
    for f in [test_indices, test_holm_bh, test_block_length, test_size_and_power, test_pipeline_null_and_dsr]:
        f()
        print("ok", f.__name__)
