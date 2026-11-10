"""Independent checks of a backfilled paper log (work dir only)."""
import sys
import numpy as np, pandas as pd
W = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/"
lg = pd.read_csv(sys.argv[1], parse_dates=["date"])
print("rows", len(lg), "dup (date,model) groups with >1 row:",
      lg.groupby(["date", "model_or_lead"]).size().gt(1).sum(), "(overnight_break double-trade days only?)",
      set(lg[lg.duplicated(["date", "model_or_lead"], keep=False)].model_or_lead))
# 1) calm fade vs lit_p2 trades (variant a, NQ, vol tercile 1, side flipped)
p2 = pd.read_csv("lit_p2_lasthalfhour_trades.csv", parse_dates=["date"],
                 usecols=["date", "market", "variant", "side", "gross_points", "vol20_tercile", "entry_ref_price"])
p2 = p2[(p2.market == "NQ") & (p2.variant == "a") & (p2.vol20_tercile == 1) & p2.date.between(lg.date.min(), lg.date.max())]
p2["fade_side"] = np.where(p2.side == "long", "short", "long")
p2["fade_usd"] = (-p2.gross_points - 0.5) * 2 - 1
c = lg[(lg.model_or_lead == "lead_calm_lasthalfhour_fade") & lg.signal.isin(["long", "short"])]
m = c.merge(p2, on="date", how="outer", indicator=True)
print("calm fade: log", len(c), "research", len(p2), "only one side", (m._merge != "both").sum(),
      "side diffs", (m.signal != m.fade_side).sum(), "max |$ diff|", (m.net_usd - m.fade_usd).abs().max())
# 2) CPI/jobs fade vs section-13 strict build (s13_Y)
y = pd.read_csv(W + "tests/s13_Y/trades/L1-CPIorNFP-2010-2026-MNQ-strict_time.csv", parse_dates=["date"])
y = y[y.date.between(lg.date.min(), lg.date.max()) & y.cash_day]
l = lg[(lg.model_or_lead == "lead_cpi_jobs_fade") & lg.signal.isin(["long", "short"])]
m = l.merge(y, on="date", how="outer", indicator=True, suffixes=("", "_y"))
print("cpi/jobs fade: log", len(l), "s13_Y", len(y), "only one side", (m._merge != "both").sum(),
      m.loc[m._merge != "both", ["date", "_merge"]].to_dict("records")[:5],
      "side diffs", (m.signal != m.side).sum(), "max |$ diff|", (m.net_usd - m.net_usd_y).abs().max(),
      "max |bp diff|", (m.net_bp - m.net_bp_y).abs().max())
# 3) price consistency of every traded/skipped row
t = lg[lg.signal.isin(["long", "short", "skipped"])].copy()
d = np.where(t.signal == "short", -1, 1)
side_known = t.signal != "skipped"
calc = d * (t.exit_px - t.entry_px) - 0.5
bad = (calc - t.net_pts).abs() > 1e-6
print("net_pts = side x (exit - entry) - 0.5 holds on", (~bad[side_known]).sum(), "of", side_known.sum(), "traded rows")
for col in ["entry_px", "exit_px", "stop_px"]:
    v = t[col].dropna()
    print(f"  {col} on 0.25 tick grid: {np.allclose((v * 4) % 1, 0) or ((v * 4 - np.round(v * 4)).abs().max() < 1e-6)}")
# 4) entry fill = 1-min bar open +/- 1 tick at entry_time (raw prices), for live models
b = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open"], dtype={"ts_event": str})
b = b[b.ts_event.str.slice(0, 10) >= lg.date.min().strftime("%Y-%m-%d")]
ts = pd.to_datetime(b.ts_event, utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
op = pd.Series(b.Open.to_numpy(), index=ts.to_numpy())
tr = t[side_known & t.model_or_lead.isin(["overnight_break", "opening_range", "lead_cpi_jobs_fade", "lead_calm_lasthalfhour_fade", "expiry_fade"])]
when = pd.to_datetime(tr.date.dt.strftime("%Y-%m-%d") + " " + tr.entry_time)
o = op.reindex(when.to_numpy()).to_numpy()
dd = np.where(tr.signal == "short", -1, 1)
ok = np.abs(tr.entry_px.to_numpy() - (o + dd * 0.25)) < 1e-6
print("entry fill = 1-min open at entry_time +/- 1 tick:", pd.Series(ok).groupby(tr.model_or_lead.to_numpy()).agg(["sum", "size"]).to_dict())
