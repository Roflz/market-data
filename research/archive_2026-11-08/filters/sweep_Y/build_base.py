"""
Sweep Y, step 1: rebuild the live overnight-break trades exactly as chosen_models.overnight_break does, check them
against chosen_models_trades.csv, and attach every width measure the sweep needs (all known at entry).
Output: base_trades.pkl / base_trades.csv in this folder.
"""
import os
import sys
sys.path.insert(0, os.getcwd())   # project modules (read-only import)
import numpy as np
import pandas as pd

import chosen_models as cm
import exits_compare as ec
import exits_engine as ee

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/sweep_Y"
SYM = "NQ"

# ---- same setup as chosen_models.main (NQ only; ec.init would also load ES, identical code otherwise) ----
ds = cm.sessions()
cash_days = ds.index[ds.cash_day]
expiry = cm.cd.expiry_fridays(cash_days)
after_drop, _fed = cm.skip_days()

x5 = pd.read_pickle(f"data/x5_{SYM}.pkl")
D = ee.Day(x5[x5.index.year >= ec.FIRST_YEAR])
D.pos = pd.Index(D.idx)
ec.G[SYM] = D
ec.G[("sets", SYM)] = ec.entry_sets(SYM)
sp = ee.SPEC[SYM]

t = ee.run(D, ec.G[("sets", SYM)]["Overnight break + daily trend"], "hold", k0=2.0)
b = t.bar.to_numpy()
date = pd.to_datetime(D.sess[b])
adj = (ds.close_adj - ds.close_raw).reindex(date).to_numpy()
net_pts = t.pts - sp["comm"] / sp["usd"]

rows = []
for k in range(len(t)):
    i = int(b[k])                      # signal bar (decision at its close)
    d = int(t.dir.iloc[k])
    e = i + 1                          # entry bar (fill at its open)
    x = i + int(t.hold_bars.iloc[k])   # exit bar
    entry_adj = D.Open[e] + d * ee.SLIP
    gross = float(t.pts.iloc[k])
    rows.append(dict(
        date=date[k], sig_bar=i, sig_time=D.idx[i], entry_time=D.idx[e], exit_time=D.idx[x] + pd.Timedelta(minutes=5),
        side="long" if d > 0 else "short", dir=d,
        entry=entry_adj - adj[k], exit=entry_adj - adj[k] + d * gross, exit_reason=t.exit.iloc[k],
        gross_pts=gross, net_pts=float(net_pts[k]), usd=float(net_pts[k]) * sp["usd"],
        R=float(net_pts[k]) / float(t.R_pts.iloc[k]),
        bp=1e4 * float(net_pts[k]) / (D.Close[i] - adj[k]),
        atr5=D.atr5[i], stop_pts=float(t.R_pts.iloc[k]),           # 2 x ATR(5-min) at the signal bar
        raw_px=D.Close[i] - adj[k],                                   # raw price at the signal close (as chosen_models' bp)
        raw_entry_fill=entry_adj - adj[k],
    ))
T = pd.DataFrame(rows)
T = T[T.date.isin(cash_days) & ~T.date.isin(expiry)]
T = T[~T.date.isin(after_drop)].reset_index(drop=True)                 # R1

# ---- check against the live file ----
L = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
L = L[L.model == "overnight_break"].reset_index(drop=True)
ok = (len(L) == len(T) and (L.date.values == T.date.values).all() and (L.side.values == T.side.values).all()
      and (L.exit.values == T.exit_reason.values).all() and np.allclose(L.usd, T.usd, atol=1e-9)
      and np.allclose(L.R, T.R, atol=1e-9) and np.allclose(L.bp, T.bp, atol=1e-9))
print(f"rebuilt {len(T)} trades ${T.usd.sum():,.2f}; live file {len(L)} trades ${L.usd.sum():,.2f}; exact match: {ok}")
if not ok:
    sys.exit("MISMATCH")

# ---- width measures ----
T["M1"] = T.stop_pts / T.raw_px                     # share of raw price
T["M1_fill"] = T.stop_pts / T.raw_entry_fill        # same with the actual entry fill (sensitivity only)
T["M3"] = T.stop_pts * sp["usd"] + 2.0              # $ risk of 1 micro incl. $2 cost
assert np.allclose(T.stop_pts, 2.0 * T.atr5)

# M4: signal-bar ATR / median ATR(5-min) of all bars in the previous 60 Globex sessions (whole x5 file, from 2010)
sess_all = x5.sess.to_numpy()
atr_all = x5.atr5.to_numpy(float)
sess_list = pd.Index(pd.unique(sess_all))
sess_pos = pd.Series(np.arange(len(sess_list)), index=sess_list)
starts = np.searchsorted(pd.factorize(sess_all)[0], np.arange(len(sess_list)))   # first bar of each session
codes = pd.factorize(sess_all)[0]
assert (np.diff(codes) >= 0).all()
med60, first_hist_bar, last_hist_bar = [], [], []
for k in range(len(T)):
    s = D.sess[T.sig_bar[k]]
    p = int(sess_pos[s])
    if p < 60:
        med60.append(np.nan); first_hist_bar.append(None); last_hist_bar.append(None)
        continue
    lo, hi = starts[p - 60], starts[p]                # bars of sessions p-60 .. p-1
    med60.append(float(np.median(atr_all[lo:hi])))
    first_hist_bar.append(x5.index[lo]); last_hist_bar.append(x5.index[hi - 1])
T["M4_med60"] = med60
T["M4"] = T.atr5 / T.M4_med60
T["M4_hist_last_bar"] = last_hist_bar
assert all(lb < st for lb, st in zip(T.M4_hist_last_bar, T.sig_time)), "M4 history must end before the signal"
assert (T.sig_time < T.entry_time).all()

pd.to_pickle(T, f"{OUT}/base_trades.pkl")
T.to_csv(f"{OUT}/base_trades.csv", index=False)
print(T[["date", "side", "usd", "stop_pts", "raw_px", "M1", "M3", "M4"]].describe().T.to_string())
