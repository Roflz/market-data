"""
Synthetic-data tests of v2/dataset.py (no real market data is read: research_lib.bars_1m is replaced by a generated
1-minute random walk with trending regimes and one contract roll).
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_dataset.py
"""
import numpy as np
import pandas as pd

import research_lib as rl
import dataset as ds
import ema50_check as ec
import labels as lb
import signals as sg

SYM = "ES"


def synth_1m(days=45, seed=0, start="2021-03-01", mirror_k=None):
    """Globex-like 1-minute bars: sessions 18:00-17:00 ET (Sun-Fri evenings), drift regimes, a roll at day 25."""
    rng = np.random.default_rng(seed)
    sess = pd.bdate_range(start, periods=days)
    rows = []
    px = 4000.0
    for q, s in enumerate(sess):
        t0 = s - pd.Timedelta(hours=6)                                 # 18:00 the evening before
        idx = t0 + pd.to_timedelta(np.arange(23 * 60), unit="min")     # 18:00 .. 16:59
        drift = rng.choice([-0.06, 0.0, 0.06]) * np.ones(len(idx))
        drift[len(idx) // 2:] = rng.choice([-0.06, 0.0, 0.06])
        steps = np.round((drift + rng.normal(0, 0.9, len(idx))) * 4) / 4
        C = px + np.cumsum(steps)
        O = np.r_[px, C[:-1]]
        H = np.maximum(O, C) + np.round(rng.exponential(0.4, len(idx)) * 4) / 4
        L = np.minimum(O, C) - np.round(rng.exponential(0.4, len(idx)) * 4) / 4
        px = C[-1] + np.round(rng.normal(0, 2) * 4) / 4
        inst = 1 if q < 25 else 2
        if q == 25:
            O, H, L, C = O + 10, H + 10, L + 10, C + 10                 # the new contract trades 10 points higher
            px += 10
        rows.append(pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C,
                                  "Volume": rng.integers(50, 500, len(idx)).astype(float),
                                  "instrument_id": inst}, index=idx))
    d = pd.concat(rows)
    if mirror_k is not None:
        o, h, l, c = d.Open.copy(), d.High.copy(), d.Low.copy(), d.Close.copy()
        d["Open"], d["Close"], d["High"], d["Low"] = mirror_k - o, mirror_k - c, mirror_k - l, mirror_k - h
    d.index = d.index.tz_localize("America/New_York")
    d.index.name = "ts"
    d["sess"] = (d.index + pd.Timedelta(hours=6)).tz_localize(None).normalize()
    d["tmin"] = (d.index.hour * 60 + d.index.minute).astype(np.int16)
    return d


class Patch:
    def __init__(self, m):
        self.m = m

    def __enter__(self):
        self.orig = rl.bars_1m
        rl.bars_1m = lambda s=None: self.m
        return self

    def __exit__(self, *a):
        rl.bars_1m = self.orig


def test_evidence_counts():
    X = np.array([[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], bool)
    c = ds.evidence_counts({1: X, -1: ~X})
    assert list(c[(1, 1)]) == [1, 1, 3, 0]
    assert list(c[(1, 2)]) == [1, 2, 3, 3]           # union of kinds over this bar and the one before
    assert list(c[(-1, 1)]) == [6, 6, 4, 7]
    print("evidence_counts ok")


def test_pipeline():
    m = synth_1m()
    with Patch(m):
        F = ds.load_frames(SYM)
        m1 = lb.load_1m(SYM)
    B = 15
    E, pool = ds.union_events(F, B, SYM)
    assert len(E) > 50, len(E)
    assert not E.duplicated(["i", "d"]).any()
    T = F[B]["T"]
    for r in ds.RULES:                                                 # flags = trigger_scan's events, once each
        a = set(map(tuple, T.loc[T.rule == r, ["i", "d"]].to_numpy()))
        bset = set(map(tuple, E.loc[E[r] == 1, ["i", "d"]].to_numpy()))
        assert a == bset, r
    assert not (set(map(tuple, pool[["i", "d"]].to_numpy())) & set(map(tuple, E[["i", "d"]].to_numpy())))
    C = F[B]["b"].C.to_numpy()
    R = F[B]["R"]
    i, d = E.i.to_numpy(), E.d.to_numpy()
    assert (d * (C[i] - E.stop.to_numpy()) >= R[i] - 1e-9).all()        # stop at least 1 R20 from the close
    pbr = E[E.pb == 1]
    assert len(pbr) > 0
    print(f"pipeline events ok: {len(E)} events ({int(E.pb.sum())} pb), {len(pool)} pool rows")
    X = ds.build_features(F, B, E, SYM)
    assert list(X.columns[:len(ds.feature_columns())]) == ds.feature_columns() or \
        set(ds.feature_columns()) <= set(X.columns)
    assert X.n_tf_agree.between(0, 3).all() and X.mtf_score.between(0, 3).all()
    tb = X[[c for c in X.columns if c.startswith("tod_")]].sum(1)
    assert (tb == 1).all()
    # labels and hand walks
    rows = pd.concat([E[["t", "i", "d", "stop"]], pool], ignore_index=True)
    rows_k, Lb = ds.label(SYM, B, F, rows, m1)
    assert len(rows_k) == len(Lb)
    lab = pd.concat([rows_k, Lb], axis=1)
    for x in ds.EXITS:
        assert np.isfinite(lab[f"pnl_{x}"]).all(), x
        tx = pd.DatetimeIndex(lab[f"t_exit_{x}"])
        assert (wf_session(tx - pd.Timedelta(minutes=1)) == pd.DatetimeIndex(lab.session)).all(), x
        mins = tx.hour * 60 + tx.minute
        assert not ((mins > 16 * 60 + 45) & (mins < 18 * 60)).any(), x
    spec = sg.SPEC[SYM]
    rules = ds.exit_rules(F, B)
    bad = 0
    rng = np.random.default_rng(0)
    for x in ("hold", "ema_cross", "opp1_1b", "opp2_2b", "opp3_1b"):
        rx = rules[x][2]
        for k in rng.choice(len(lab), 25, replace=False):
            r = lab.iloc[k]
            p, _ = ec.hand_walk(r, m1, F[B]["b"], B, spec["tick"], spec["usd"], spec["cost"],
                                "hold" if rx is None else "cross", rx)
            bad += abs(p - r[f"pnl_{x}"]) > 1e-6
    assert bad == 0, bad
    # opp exits: tighter N exits no later than looser N (same window)
    for w in ds.WINDOWS_B:
        for n in (1, 2, 3):
            assert (lab[f"bars_opp{n}_{w}b"] <= lab[f"bars_opp{n + 1}_{w}b"]).all()
        # 2-bar window counts >= 1-bar counts -> exits no later
    for n in ds.N_LIST:
        assert (lab[f"bars_opp{n}_2b"] <= lab[f"bars_opp{n}_1b"]).all()
    print("labels ok (125 hand walks match, exits monotone in N and window)")
    bad = ds.evidence_check(F, B, n=150)
    assert bad == 0, bad
    bad60 = ds.evidence_check(F, 60, n=100)
    bad5 = ds.evidence_check(F, 5, n=150)
    assert bad60 == 0 and bad5 == 0, (bad60, bad5)
    print("evidence check ok")


def wf_session(t):
    return (pd.DatetimeIndex(t) + pd.Timedelta(hours=6)).normalize()


def test_truncation():
    m = synth_1m(days=30, seed=3)
    with Patch(m):
        for B in (5, 15, 60):
            bad, n = ds.truncation_check(SYM, B, "2021-03-01", days=40, cuts=3, seed=B)
            assert n > 0
            assert bad == 0, (B, bad)
            print(f"truncation {B}m ok ({n} rows compared)")


def test_mirror():
    """Long features of a chart = short features of the upside-down chart (except Momentum, a ratio, and the candle
    counts, whose pattern definitions are not exactly symmetric)."""
    K = 9000.0
    m = synth_1m(days=30, seed=5)
    mm = synth_1m(days=30, seed=5, mirror_k=K)
    with Patch(m):
        F = ds.load_frames(SYM)
    with Patch(mm):
        G = ds.load_frames(SYM)
    B = 15
    b = F[B]["b"]
    ok, _ = lb.eligible(b, B)
    i = np.flatnonzero(ok & np.isfinite(F[B]["R"]))[::7]
    C = b.C.to_numpy()[i]
    base = pd.DataFrame({"i": i, "stop": C - 3.0, "pb": 0, "i_PL": np.nan, "depth": np.nan, "bars_pullback": np.nan,
                         "divergence": np.nan, "mom_flip": np.nan})
    XL = ds.build_features(F, B, base.assign(d=1), SYM)
    XS = ds.build_features(G, B, base.assign(d=-1, stop=K - base.stop), SYM)
    skip = {c for c in XL.columns if "mom" in c or "mslope" in c or c.startswith("pat_") or c in ("rev_at_low", "mtf_trig5",
                                                                                 "mtf_score")}
    for c in XL.columns:
        if c in skip:
            continue
        a, s = XL[c].to_numpy(np.float64), XS[c].to_numpy(np.float64)
        same = (np.abs(a - s) <= 1e-3 * np.maximum(1, np.abs(a))) | (np.isnan(a) & np.isnan(s))
        assert same.all(), (c, int((~same).sum()))
    print(f"mirror ok ({len(i)} bars, {len(XL.columns) - len(skip)} columns)")


if __name__ == "__main__":
    test_evidence_counts()
    test_pipeline()
    test_truncation()
    test_mirror()
    print("all dataset tests passed")
