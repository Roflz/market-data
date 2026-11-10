"""Rebuild the live overnight-break trades (chosen_models.overnight_break + R1) with per-trade stop width fields.
NQ only (chosen_models' ec.init() also builds ES, which overnight_break does not use; same code path for NQ).
Also computes the M4 volatility-shock input (median atr5 over the previous 60 Globex sessions, any time of day).
Output: base_trades.pkl / base_trades.csv in this dir."""
import os
import warnings

import numpy as np
import pandas as pd

import calendar_days as cd
import chosen_models as cm
import exits_compare as ec
import exits_engine as ee

warnings.filterwarnings("ignore")
OUT = os.path.dirname(os.path.abspath(__file__))
SYM = "NQ"

ds = cm.sessions()
cash_days = ds.index[ds.cash_day]
expiry = cd.expiry_fridays(cash_days)
after_drop, _ = cm.skip_days()

# --- same as ec.init() for NQ only
b5 = pd.read_pickle(f"data/x5_{SYM}.pkl")
D = ee.Day(b5[b5.index.year >= ec.FIRST_YEAR])
D.pos = pd.Index(D.idx)
ec.G[SYM] = D
ec.G[("sets", SYM)] = ec.entry_sets(SYM)
sp = ee.SPEC[SYM]
t = ee.run(D, ec.G[("sets", SYM)]["Overnight break + daily trend"], "hold", k0=2.0)

b = t.bar.to_numpy()
e = b + 1
x = b + t.hold_bars.to_numpy()                       # exit bar (simulate: hold = t - e + 1)
date = pd.to_datetime(D.sess[b])
adj = (ds.close_adj - ds.close_raw).reindex(date).to_numpy()
d = t.dir.to_numpy()
net_pts = t.pts.to_numpy() - sp["comm"] / sp["usd"]
entry_adj = D.Open[e] + d * ee.SLIP
T = pd.DataFrame({
    "model": "overnight_break", "date": date, "side": np.where(d > 0, "long", "short"), "dir": d,
    "signal_bar_time": D.idx[b], "entry_time": D.idx[e], "exit_time": D.idx[x] + pd.Timedelta(minutes=5),
    "entry": entry_adj - adj, "exit": None, "exit_reason": t.exit.to_numpy(),
    "gross_pts": t.pts.to_numpy(), "net_pts": net_pts, "usd": net_pts * sp["usd"], "R": net_pts / t.R_pts.to_numpy(),
    "bp": 1e4 * net_pts / (D.Close[b] - adj),
    "R_pts": t.R_pts.to_numpy(), "atr5_signal": D.atr5[b], "raw_signal_close": D.Close[b] - adj, "adj": adj,
    "bar": b, "sess_same": D.sess[x] == D.sess[b]})
T["exit"] = T.entry + T.dir * T.gross_pts
T["exit_time_note"] = "exit_time = close time of the exit bar (stop fills happen inside that bar)"
T = T[T.date.isin(cash_days) & ~T.date.isin(expiry)]
T = T[~T.date.isin(after_drop)].reset_index(drop=True)          # R1 (chosen_models applies it in main())

# --- M4 input: median of atr5 over all 5-min bars of the previous 60 Globex sessions (strictly before the session)
s_all = b5[["sess", "atr5"]].copy()
sess_list = np.sort(s_all.sess.unique())
sid = np.searchsorted(sess_list, s_all.sess.to_numpy())
atr = s_all.atr5.to_numpy()
med60 = np.full(len(sess_list), np.nan)
order = np.argsort(sid, kind="stable")
starts = np.searchsorted(sid[order], np.arange(len(sess_list) + 1))
for k in range(60, len(sess_list)):
    med60[k] = np.median(atr[order[starts[k - 60]:starts[k]]])
med60 = pd.Series(med60, index=pd.to_datetime(sess_list))
T["atr_med60"] = med60.reindex(T.date).to_numpy()

T["M1"] = T.R_pts / T.raw_signal_close
T["M2_pts"] = T.R_pts
T["M3"] = T.R_pts * sp["usd"] + 2.0
T["M4"] = T.atr5_signal / T.atr_med60

# --- check against chosen_models_trades.csv
C = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
C = C[C.model == "overnight_break"].reset_index(drop=True)
assert len(C) == len(T), (len(C), len(T))
for c in ("date", "side", "exit"):
    pass
chk = {"n": len(T), "usd_sum": T.usd.sum(), "csv_usd_sum": C.usd.sum(),
       "dates_equal": bool((C.date.to_numpy() == T.date.to_numpy()).all()),
       "side_equal": bool((C.side.to_numpy() == T.side.to_numpy()).all()),
       "exit_equal": bool((C.exit.to_numpy() == T.exit_reason.to_numpy()).all()),
       "usd_maxabs": float(np.abs(C.usd.to_numpy() - T.usd.to_numpy()).max()),
       "R_maxabs": float(np.nanmax(np.abs(C.R.to_numpy() - T.R.to_numpy()))),
       "bp_maxabs": float(np.abs(C.bp.to_numpy() - T.bp.to_numpy()).max()),
       "all_exit_same_session": bool(T.sess_same.all()), "m4_nan": int(T.M4.isna().sum())}
print(chk)
T.to_pickle(f"{OUT}/base_trades.pkl")
T.to_csv(f"{OUT}/base_trades.csv", index=False)
