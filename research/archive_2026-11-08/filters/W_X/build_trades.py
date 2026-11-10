"""Rebuild the live overnight_break trades exactly as chosen_models.overnight_break, keeping R_pts, signal bar and raw price."""
import warnings, numpy as np, pandas as pd
import sys, os; sys.path.insert(0, os.getcwd())
import calendar_days as cd, exits_compare as ec, exits_engine as ee, chosen_models as cm
warnings.filterwarnings("ignore")
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/W_X/"
SYM = "NQ"
# NQ-only version of ec.init() (same code, skips loading ES to save memory)
b5 = pd.read_pickle(f"data/x5_{SYM}.pkl")
D = ee.Day(b5[b5.index.year >= ec.FIRST_YEAR]); D.pos = pd.Index(D.idx)
ec.G[SYM] = D
ec.G[("sets", SYM)] = ec.entry_sets(SYM)
ds = cm.sessions()
cash_days = ds.index[ds.cash_day]
expiry = cd.expiry_fridays(cash_days)
sp = ee.SPEC[SYM]
t = ee.run(D, ec.G[("sets", SYM)]["Overnight break + daily trend"], "hold", k0=2.0)
b = t.bar.to_numpy()
date = pd.to_datetime(D.sess[b])
adj = (ds.close_adj - ds.close_raw).reindex(date).to_numpy()
net_pts = t.pts - sp["comm"] / sp["usd"]
raw_px = D.Close[b] - adj
out = pd.DataFrame({"model": "overnight_break", "date": date, "side": np.where(t.dir > 0, "long", "short"),
                    "exit": t.exit, "usd": net_pts * sp["usd"], "R": net_pts / t.R_pts,
                    "bp": 1e4 * net_pts / raw_px,
                    "signal_bar_open": D.idx[b], "entry_bar_open": D.idx[b + 1], "exit_bar_open": D.idx[t.bar + 0].values,
                    "R_pts": t.R_pts.to_numpy(), "atr5_signal": D.atr5[b], "close_adj_signal": D.Close[b],
                    "back_adj": adj, "raw_px": raw_px, "entry_fill_adj": D.Open[b + 1] + t.dir.to_numpy() * ee.SLIP,
                    "gross_pts": t.pts.to_numpy(), "net_pts": net_pts, "bar": b})
out["exit_bar_open"] = D.idx[b + t.hold_bars.to_numpy()]      # exit bar = entry bar + hold_bars - 1
out["width"] = out.R_pts / out.raw_px
allob = out.copy()
out = out[out.date.isin(cash_days) & ~out.date.isin(expiry)]
after_drop, fed = cm.skip_days()
out = out[~out.date.isin(after_drop)].reset_index(drop=True)
pd.to_pickle({"live": out, "all_pre_skip": allob, "cash_days": cash_days, "first_sess": pd.Timestamp(D.sess[0]),
              "sess_all": pd.DatetimeIndex(pd.unique(D.sess))}, OUT + "ob_trades.pkl")
ref = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
ref = ref[ref.model == "overnight_break"].reset_index(drop=True)
print("mine", len(out), out.usd.sum(), "ref", len(ref), ref.usd.sum())
m = ref.merge(out, on=["date", "side"], suffixes=("_r", "_m"), how="outer", indicator=True)
print(m._merge.value_counts())
print("max |usd diff|", (m.usd_r - m.usd_m).abs().max(), "max |bp diff|", (m.bp_r - m.bp_m).abs().max(),
      "exit equal", (m.exit_r == m.exit_m).all(), "dup dates", out.date.duplicated().sum())
print("first session in D", D.sess[0], "first trade", out.date.min())
