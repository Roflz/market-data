"""HEAVY (raw 1-minute data; run under the shared flock): re-price corrected S3.7 trades by hand from the RAW
research_lib.bars_1m rows: the 3 'Tuesday after Labor Day' trades ES 2019-09-03, NQ 2024-09-03, YM 2018-09-04 plus
1 random other v2 trade per market. Also prints the raw 09:30 bar volume on the Labor Day vs Tuesday sessions.
Output: fix_labor_day/handcheck_S3.7.csv"""
import gc, os
import numpy as np, pandas as pd
import harness as H
import handcheck_harness as hh
import research_lib as rl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "out", "trades")
t = pd.read_parquet(os.path.join(OUT, "S3.7.parquet"))
rng = np.random.default_rng(20261109)
fixed = {"ES": "2019-09-03", "NQ": "2024-09-03", "YM": "2018-09-04"}
rows = []
for sym in ("ES", "NQ", "YM"):
    ts = t[t.market == sym].reset_index(drop=True)
    pick = [ts[pd.DatetimeIndex(ts.session) == pd.Timestamp(fixed[sym])].iloc[0]]
    others = ts[pd.DatetimeIndex(ts.session) != pd.Timestamp(fixed[sym])]
    pick.append(others.iloc[int(rng.integers(len(others)))])
    m = rl.bars_1m(sym)
    for tr in pick:
        D = pd.Timestamp(tr.session)
        e, x, kind, pnl, _, _ = hh.hand(m, sym, D, H.mark_index(tr.entry), H.mark_index(tr.exit), int(tr.d), np.nan)
        rows.append(dict(market=sym, session=D.date(), entry=tr.entry, exit=tr.exit, d=int(tr.d),
                         h_entry_px=tr.entry_px, hand_entry_px=e, h_exit_px=tr.exit_px, hand_exit_px=x,
                         h_kind=tr.exit_kind, hand_kind=kind, h_pnl=tr.pnl_usd, hand_pnl=pnl,
                         match=bool(abs(pnl - tr.pnl_usd) < 1e-9 and kind == tr.exit_kind)))
    # raw 09:30 1-minute volume on the Labor Day session vs the Tuesday (thin holiday trading)
    idx = m.index.tz_convert("America/New_York").tz_localize(None) if m.index.tz is not None else m.index
    ld = pd.Timestamp(fixed[sym]) - pd.Timedelta(days=1)
    for day in (ld, pd.Timestamp(fixed[sym])):
        sel = m.Volume[(idx >= day + pd.Timedelta(hours=9, minutes=30)) & (idx < day + pd.Timedelta(hours=9, minutes=31))]
        print(sym, day.date(), day.day_name()[:3], "09:30 1-min volume:", sel.sum(), flush=True)
    del m, idx
    gc.collect()
out = pd.DataFrame(rows)
out.to_csv(os.path.join(HERE, "handcheck_S3.7.csv"), index=False)
pd.set_option("display.width", 250)
print(out.to_string())
print(f"hand-check: {out.match.sum()} / {len(out)} trades match")
