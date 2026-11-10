"""Stage 1 (no P&L used): per-trade skip decisions for every variant + the M1 vs M2 overlap used to keep/drop M2.
Lookback window for a trade on cash day k = live trades dated on cash days k-L .. k-1 (strictly before the date).
A trade is eligible (can be skipped) only if at least L cash days lie between the model's first live trade date and
the trade date (k - k_first >= L). Skip if measure > np.percentile(window measures, q) (numpy linear interpolation).
Outputs: decisions.pkl (trade x variant booleans), thresholds.pkl, m2_overlap.csv."""
import os

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
T = pd.read_pickle(f"{OUT}/base_trades.pkl")
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
cash = pd.DatetimeIndex(ds.index[ds.cash_day]).as_unit("ns")
k = cash.get_indexer(pd.DatetimeIndex(T.date).as_unit("ns"))
assert (k >= 0).all()
k_first = k.min()
QS, LS = (50, 67, 80, 90), (125, 250, 500)
XS = (75, 100, 150, 200, 250, 300)


def lookback_skip(meas, q, L):
    m = T[meas].to_numpy()
    lo = np.searchsorted(k, k - L, side="left")          # first trade with cash index >= k-L
    hi = np.searchsorted(k, k, side="left")              # first trade on the trade's own date (exclusive)
    elig = (k - k_first) >= L
    thr = np.full(len(T), np.nan)
    for i in np.flatnonzero(elig):
        assert k[hi[i] - 1] < k[i] and k[lo[i]] >= k[i] - L     # window strictly before the date, within L days
        thr[i] = np.percentile(m[lo[i]:hi[i]], q)
    return elig, thr, elig & (m > thr)


dec, thr_all, elig_all, meas_all = {}, {}, {}, {}
for meas, tag in (("M1", "M1"), ("M2_pts", "M2"), ("M4", "M4")):
    for L in LS:
        for q in QS:
            v = f"{tag}_q{q}_L{L}"
            elig_all[v], thr_all[v], dec[v] = lookback_skip(meas, q, L)
            meas_all[v] = meas
for X in XS:
    v = f"M3_X{X}"
    elig_all[v] = np.ones(len(T), bool)
    thr_all[v] = np.full(len(T), float(X))
    dec[v] = T.M3.to_numpy() > X
    meas_all[v] = "M3"

# M1 vs M2 decision overlap (decided before any P&L is looked at)
rows = []
for L in LS:
    for q in QS:
        a, b = dec[f"M1_q{q}_L{L}"], dec[f"M2_q{q}_L{L}"]
        rows.append(dict(q=q, L=L, n_M1=a.sum(), n_M2=b.sum(), both=(a & b).sum(), jaccard=(a & b).sum() / (a | b).sum(),
                         differ_share_of_eligible=(a != b).sum() / elig_all[f"M1_q{q}_L{L}"].sum()))
ov = pd.DataFrame(rows)
ov.to_csv(f"{OUT}/m2_overlap.csv", index=False)
print(ov.to_string())
pd.to_pickle(dict(dec=dec, thr=thr_all, elig=elig_all, meas=meas_all, cash_k=k, k_first=k_first), f"{OUT}/decisions.pkl")
