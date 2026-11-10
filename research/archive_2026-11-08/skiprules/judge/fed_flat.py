"""Rebuild opening_range (chosen_models.py logic) on Fed days and compare: hold to close (as traded) vs flat at 13:58 close.
Also R1 days: compare. Reads project only."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.getcwd())
import calendar_days as cd
import lit_p5_orb as p5
import chosen_models as cm

SYM = "NQ"; K = 5
ds = cm.sessions()
cash_days = ds.index[ds.cash_day]
expiry = cd.expiry_fridays(cash_days)
dates, g, inst = p5.load_market(SYM)
sess, Cff, _ = p5.build_sessions(SYM, dates, g, inst)
sess = sess[sess.date.isin(cash_days)]
fomc = set(pd.to_datetime(list(cd.fomc_days())))
ppt, min_R = p5.MARKETS[SYM]["ppt"], p5.MARKETS[SYM]["min_R"]
O, H, L = g["Open"], g["High"], g["Low"]
FLAT = 268  # 9:30 + 268 min = 13:58 bar; exit at its close (13:59)
rows = []
for r in sess.itertuples(index=False):
    if r.date not in fomc:
        continue
    i = r.di
    if r.date in expiry or np.isnan(O[i, 0]) or np.isnan(O[i, K]):
        continue
    oc, cc = O[i, 0], Cff[i, K - 1]
    if cc == oc:
        continue
    d = 1 if cc > oc else -1
    stop = np.nanmin(L[i, :K]) if d > 0 else np.nanmax(H[i, :K])
    if d * (cc + d * p5.TICK - stop) < min_R:
        continue
    ref, fill = O[i, K], O[i, K] + d * p5.TICK
    out = {}
    for lab, sx in [("hold", r.exit_slot), ("flat1358", min(FLAT, r.exit_slot))]:
        if d * (fill - stop) <= 0:
            xs, xfill, why = K, ref - d * p5.TICK, "stop"
        else:
            xs, _, xfill, why = p5.run_trade(H[i], L[i], O[i], Cff[i, sx], K, sx, d, stop, None, True)
        out[lab] = (d * (xfill - fill) - p5.COMM / ppt) * ppt
        out[lab + "_why"] = why
        out[lab + "_slot"] = xs
    rows.append(dict(date=r.date, side=d, **out))
F = pd.DataFrame(rows)
T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
orx = T[(T.model == "opening_range") & T.date.isin(fomc)].set_index("date").usd
F = F.set_index("date")
print("rebuilt Fed-day trades", len(F), "csv", len(orx), "match hold usd:", np.allclose(F.hold.reindex(orx.index), orx.values))
F["year"] = F.index.year
print(f"hold to close: n={len(F)} ${F.hold.mean():+.2f}/trade; flat at 13:59: ${F.flat1358.mean():+.2f}/trade")
print("stopped before 13:59 under hold:", ((F.hold_why == 'stop') & (F.hold_slot <= FLAT)).sum(), "; stopped after:", ((F.hold_why == 'stop') & (F.hold_slot > FLAT)).sum(), "; held to close:", (F.hold_why == 'close').sum())
for lab, gg in [("2010-2017", F[F.year < 2018]), ("2018-2026", F[F.year >= 2018]), ("2021-2026", F[F.year >= 2021])]:
    print(f"  {lab}: n={len(gg)} hold ${gg.hold.mean():+.2f}  flat13:59 ${gg.flat1358.mean():+.2f}  (after-14:00 part ${(gg.hold-gg.flat1358).mean():+.2f})")
oth = T[(T.model == "opening_range") & ~T.date.isin(fomc)]
print(f"other days mean ${oth.usd.mean():+.2f}; 2018+ ${oth[oth.date.dt.year>=2018].usd.mean():+.2f}; 2021+ ${oth[oth.date.dt.year>=2021].usd.mean():+.2f}")
