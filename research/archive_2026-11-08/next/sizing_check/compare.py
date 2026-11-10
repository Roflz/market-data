import os, numpy as np, pandas as pd
W = os.path.dirname(os.path.abspath(__file__))
os.chdir("/run/media/roflz/Disk 2/_/market_data")
X = pd.read_pickle(f"{W}/rebuild.pkl")
C = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
print("row order model/date/side identical to chosen_models_trades.csv:",
      bool((X.model.values == C.model.values).all() and (X.date.values == C.date.values).all() and (X.side.values == C.side.values).all()))
for m in ["overnight_break", "opening_range", "expiry_fade"]:
    g = X[X.model == m]
    print(f"\n{m}: {len(g)} trades")
    print("  1-micro $ reproduced from raw vs chosen_models_trades.csv: max |diff| =", float((g.usd2 - g.usd_csv).abs().max()),
          " n diff>0.01:", int(((g.usd2 - g.usd_csv).abs() > 0.01).sum()))
    if m != "expiry_fade":
        dd = (g.stop_ind - g.stop_pts).abs()
        print("  stop pts independent vs builder: max |diff| =", float(dd.max()), " n>1e-6:", int((dd > 1e-6).sum()))
        dx = (g.exit_time2 - g.exit_time).abs()
        print("  exit time independent vs builder: n differ =", int((dx > pd.Timedelta(0)).sum()))
        print("  price (for scaling) diff max:", float((g.price2 - g.price).abs().max()))
    else:
        dd = (g.adr20_2 - g.adr20).abs()
        print("  ADR20 independent vs builder: max |diff| =", float(dd.max()), " n>1e-6:", int((dd > 1e-6).sum()), " nan:", int(g.adr20.isna().sum()), int(g.adr20_2.isna().sum()))
        print("  ADR20 INCLUDING today vs builder: n>1e-6:", int(((g.adr20_incl_today - g.adr20).abs() > 1e-6).sum()))
    if m == "overnight_break":
        print("  look-ahead variant (ATR incl. entry bar) matches builder:", int(((g.stop_pts_lookahead - g.stop_pts).abs() < 1e-6).sum()), "of", len(g))
        print("  signal close beyond overnight extreme:", int(g.beyond_on.sum()), "of", len(g), "; entry - signal bar = 5 min:",
              int(((g.entry_time - g.sig_bar) == pd.Timedelta(minutes=5)).sum()))
        print("  entry times range:", g.entry_time.dt.time.min(), g.entry_time.dt.time.max())
    bad = g[(g.usd2 - g.usd_csv).abs() > 0.01]
    if len(bad): print(bad[["date", "side", "entry_time", "exit", "usd_csv", "usd2", "stop_pts", "stop_ind"]].head(10).to_string())
