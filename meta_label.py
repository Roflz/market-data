"""
Step 3 of the pre-registration: machine-learning filter on BASE ("meta-labeling").
Primary signal = BASE (overnight-level break + daily trend). A classifier estimates P(trade ends with net R > 0) from
the 88 entry-time measures of the futures pipeline + the HAR volatility forecast + direction + market flag.
Every signal is simulated on its own (2 ATR stop, hold to the 5 PM close) to get its label; the policy then filters
or sizes signals and the normal one-position-at-a-time engine is rerun, so the trade sequence is exact.
  M1 skip signals whose probability is below a cut-off (none / 20th / 35th / 50th percentile of training predictions)
  M2 size 0.5x / 1x / 1.5x by prediction tercile (training cut-offs)
Walk-forward 2013-2026: fit on years < Y-2, choose M1's cut-off on Y-2..Y-1, refit on < Y, apply to year Y.
Control: identical pipeline with labels shuffled between signals.
Usage:  PYTHONPATH=./pylib python3 meta_label.py
"""
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

import exits_compare as ec
import exits_engine as ee
import setup_rule
from vol_module import har_forecast

warnings.filterwarnings("ignore")
SETUP, K0 = "Overnight break + daily trend", 2.0
PARAMS = dict(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=100, l2_regularization=1.0,
              early_stopping=False, random_state=0)
CUTS = [None, 0.20, 0.35, 0.50]


def signals_with_features(sym):
    D, sp = ec.G[sym], ee.SPEC[sym]
    F = pd.read_pickle(f"data/fut_features_{sym}.pkl")
    X = F["X"].copy()
    bar = D.pos.get_indexer(pd.DatetimeIndex(F["ts"]) - pd.Timedelta(minutes=4))
    sig = setup_rule.overnight_break(X, F["ts"])
    m = (sig != 0) & (bar >= 0)
    S = X[m].copy()
    S["bar"], S["dir"] = bar[m], sig[m]
    f, _ = har_forecast(sym)
    S["sess"] = D.sess[S.bar.to_numpy()]
    S["har_vol"] = S.sess.map(f.fc_vol.to_dict())
    S["har_tercile"] = S.sess.map(f.tercile.to_dict())
    S["is_nq"] = 1.0 if sym == "NQ" else 0.0
    S["sym"], S["year"] = sym, D.year[S.bar.to_numpy()]
    # label: each signal simulated on its own
    R = []
    for i, d in zip(S.bar.to_numpy(), S.dir.to_numpy()):
        r = ee.simulate(D, int(i), int(d), "hold", K0)
        R.append(np.nan if r is None else (r[1] - sp["comm"] / sp["usd"]) / (K0 * D.atr5[i]))
    S["R"] = R
    S = S.dropna(subset=["R"]).sort_values("bar").reset_index(drop=True)
    S["win"] = (S.R > 0).astype(int)
    return S


def run_policy(sym, S_sym, keep, size):
    """Rerun the sequential engine on the kept signals; return per-trade net R (sized) with year."""
    D, sp = ec.G[sym], ee.SPEC[sym]
    sigs = sorted(zip(S_sym.bar[keep].tolist(), S_sym.dir[keep].tolist()))
    sz = dict(zip(S_sym.bar[keep].tolist(), size[keep].tolist()))
    t = ee.run(D, sigs, "hold", k0=K0)
    if t.empty:
        return t.assign(R=[], year=[])
    bb = t.bar.to_numpy()
    t["R"] = (t.pts - sp["comm"] / sp["usd"]) / (K0 * D.atr5[bb]) * np.array([sz[b] for b in bb])
    t["year"] = D.year[bb]
    return t


def main():
    ec.init()
    S = pd.concat([signals_with_features("NQ"), signals_with_features("ES")], ignore_index=True)
    feats = [c for c in S.columns if c not in ("bar", "sess", "sym", "year", "R", "win")]
    print(f"{len(S):,} signals ({(S.sym == 'NQ').sum()} NQ, {(S.sym == 'ES').sum()} ES), {len(feats)} features; "
          f"base win rate {S.win.mean():.1%}", flush=True)
    rng = np.random.default_rng(0)
    S["win_ctrl"] = rng.permutation(S.win.to_numpy())
    rows = []
    for ty in range(2013, 2027):
        for name, lab in (("meta-label", "win"), ("CONTROL (shuffled)", "win_ctrl")):
            tr_in = S[S.year < ty - 2] if (S.year < ty - 2).sum() > 300 else S[S.year < ty - 1]
            va = S[(S.year >= ty - 2) & (S.year < ty)] if (S.year < ty - 2).sum() > 300 else S[S.year == ty - 1]
            m_in = HistGradientBoostingClassifier(**PARAMS).fit(tr_in[feats], tr_in[lab])
            p_tr_in = m_in.predict_proba(tr_in[feats])[:, 1]
            pv = m_in.predict_proba(va[feats])[:, 1]
            best_c, best_v = None, -np.inf
            for c in CUTS:                                 # choose M1's cut-off on validation (pooled NQ+ES, real R)
                keep = np.ones(len(va), bool) if c is None else pv >= np.quantile(p_tr_in, c)
                v = va.R[keep].sum()
                if v > best_v:
                    best_c, best_v = c, v
            full = S[S.year < ty]
            m = HistGradientBoostingClassifier(**PARAMS).fit(full[feats], full[lab])
            p_full = m.predict_proba(full[feats])[:, 1]
            q1, q2 = np.quantile(p_full, [1 / 3, 2 / 3])
            for sym in ("NQ", "ES"):
                te = S[(S.year == ty) & (S.sym == sym)].reset_index(drop=True)
                if te.empty:
                    continue
                p = m.predict_proba(te[feats])[:, 1]
                base = run_policy(sym, te, np.ones(len(te), bool), np.ones(len(te)))
                keep1 = np.ones(len(te), bool) if best_c is None else p >= np.quantile(p_full, best_c)
                m1 = run_policy(sym, te, keep1, np.ones(len(te)))
                size2 = np.where(p < q1, 0.5, np.where(p < q2, 1.0, 1.5))
                m2 = run_policy(sym, te, np.ones(len(te), bool), size2)
                rows.append({"market": ee.SPEC[sym]["micro"], "year": ty, "model": name, "cut": best_c,
                             "BASE_R": base.R.sum(), "M1_R": m1.R.sum(), "M1_trades": len(m1), "M2_R": m2.R.sum(),
                             "BASE_trades": len(base)})
        print(f"  {ty} done", flush=True)
    res = pd.DataFrame(rows)
    res.to_csv("meta_label_results.csv", index=False)
    pd.set_option("display.width", 220)
    print("\n=== Net R per year: BASE vs ML filter (M1) and ML sizing (M2), walk-forward ===")
    print(res.round(1).to_string(index=False))
    tot = res.groupby(["market", "model"]).agg(BASE=("BASE_R", "sum"), M1=("M1_R", "sum"), M2=("M2_R", "sum"),
                                               M1_better=("M1_R", lambda x: None), trades_base=("BASE_trades", "sum"),
                                               trades_M1=("M1_trades", "sum")).drop(columns="M1_better")
    for (mk, md), g in res.groupby(["market", "model"]):
        tot.loc[(mk, md), "M1 years better"] = f"{int((g.M1_R > g.BASE_R).sum())}/{len(g)}"
        tot.loc[(mk, md), "M2 years better"] = f"{int((g.M2_R > g.BASE_R).sum())}/{len(g)}"
        g26 = g[g.year == 2026]
        tot.loc[(mk, md), "2026 BASE/M1/M2"] = f"{g26.BASE_R.sum():.1f} / {g26.M1_R.sum():.1f} / {g26.M2_R.sum():.1f}"
    print("\n=== Totals 2013-2026 (net R) ===")
    print(tot.round(1).to_string())


if __name__ == "__main__":
    main()
