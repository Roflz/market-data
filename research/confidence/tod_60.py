"""Profit by entry time of day for the 60-min long triggers (does entering earlier in the 23-hour session, with more
room before the 16:45 close, pay more?). Writes out/tod_60.csv."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, features as fe, labels as lb, walkforward as wf, exit_study as es
rows = []
for sym in ("NQ", "YM", "ES"):
    T = pd.read_parquet(f"out/triggers_{sym}_60.parquet", columns=["t", "i", "d", "rule", "stop"])
    m1 = lb.load_1m(sym); m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
    b, ctx = fe._load(sym, 60); k = b.index < wf.HOLDOUT_SESSION_START; b, ctx = b.loc[k], ctx.loc[k]
    sig = es.exit_signals(sym, 60, b, ctx)
    for rule in ("ema50_pb", "trend_all", "ema20_pb", "pb_break"):
        ev = T[(T.rule == rule) & (T.d > 0)].reset_index(drop=True)
        for name in ("1.5R target, 16 bars (old)", "stop only, hold to 16:45", "opp: EMA 8 crosses EMA 20"):
            spec = es.EXITS[name]
            res, sel = es.simulate(sym, 60, b, ctx, ev, m1, *spec[:5], rule_exit=sig[spec[5]] if len(spec) > 5 else None)
            e = ev.iloc[sel].reset_index(drop=True)
            entry_hr = (pd.DatetimeIndex(e.t) + pd.Timedelta(minutes=60)).hour      # entry = next bar's open
            rows.append(pd.DataFrame({"market": sym, "rule": rule, "exit": name, "entry_hour": entry_hr,
                                      "pnl": res.pnl.to_numpy(), "bars": res.bars_held.to_numpy(),
                                      "year": pd.DatetimeIndex(e.t).year}))
    del m1
D = pd.concat(rows)
D.to_parquet("out/tod_60_trades.parquet")
S = D.groupby(["market", "rule", "exit", "entry_hour"]).agg(n=("pnl", "size"), usd=("pnl", "mean"), bars=("bars", "mean")).reset_index()
S.to_csv("out/tod_60.csv", index=False)
print("done")
