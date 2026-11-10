"""Research only: stop sizes x trailing / breakeven rules on the main model's entries (current engine, hold to 5 PM).
R = equal risk per trade; $ at 1 contract for reference. Walk-forward: each year uses the combo with the most R in all
earlier years (from 2013), so the chosen combo is never picked on the year it trades. Run from the project folder."""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import exits_compare as ec
import exits_engine as ee

pd.set_option("display.width", 220)
STOPS = [1.0, 1.5, 2.0, 3.0, 4.0]
EXITS = {"hold": "hold (no management)", "lock_1_0": "breakeven at +1R", "lock_2_0": "breakeven at +2R",
         "lock_1_3": "breakeven at +1R, then trail 3 ATR", "lock_2_3": "breakeven at +2R, then trail 3 ATR",
         "trail_3": "trail 3 ATR from entry", "trail_4": "trail 4 ATR from entry", "trail_6": "trail 6 ATR from entry"}
BASE = ("hold", 2.0)
ec.init()

for sym in ("NQ", "ES"):
    D, sp = ec.G[sym], ee.SPEC[sym]
    sigs = ec.G[("sets", sym)]["Overnight break + daily trend"]
    T = {}
    for k in STOPS:
        for x in EXITS:
            t = ee.run(D, sigs, x, k0=k)
            b = t.bar.to_numpy()
            t["R"] = (t.pts - sp["comm"] / sp["usd"]) / t.R_pts
            t["usd"] = t.pts * sp["usd"] - sp["comm"]
            t["year"], t["sess"] = D.year[b], D.sess[b]
            T[(x, k)] = t
    base = T[BASE]
    bd, by = base.groupby("sess").R.sum(), base.groupby("year").R.sum()
    rows = []
    for (x, k), t in T.items():
        d, y = t.groupby("sess").R.sum(), t.groupby("year").R.sum()
        days = d.index.union(bd.index)
        dl = d.reindex(days, fill_value=0) - bd.reindex(days, fill_value=0)
        rows.append({"exit": EXITS[x], "stop ATR": k, "trades": len(t), "win %": 100 * (t.R > 0).mean(),
                     "total R": t.R.sum(), "t": d.mean() / (d.std() / np.sqrt(len(d))),
                     "years up": f"{int((y > 0).sum())}/{len(y)}", "R 2011-17": y.loc[:2017].sum(),
                     "R 2018-26": y.loc[2018:].sum(), "$ 1 contract": t.usd.sum(),
                     "vs current: R diff": dl.sum(), "diff t": dl.mean() / (dl.std() / np.sqrt(len(dl))),
                     "years better": f"{int((y.reindex(by.index, fill_value=0) > by).sum())}/{len(by)}"})
    r = pd.DataFrame(rows).sort_values("total R", ascending=False)
    print(f"\n################ {sp['micro']}: {len(T)} combos, sorted by total R (current = hold, 2 ATR) ################")
    print(r.to_string(index=False, float_format=lambda v: f"{v:,.2f}" if abs(v) < 100 else f"{v:,.0f}"))
    print(f"  combos beating current in total R: {(r['vs current: R diff'] > 0).sum()} of {len(r) - 1}; "
          f"with diff t > 2: {(r['diff t'] > 2).sum()}")
    # walk-forward selection
    Y = pd.DataFrame({key: t.groupby("year").R.sum() for key, t in T.items()}).fillna(0)
    wf, picks = [], []
    for yr in range(2013, 2027):
        best = Y.loc[:yr - 1].sum().idxmax()
        wf.append(Y.loc[yr, best]); picks.append(f"{yr}: {best[0]}/{best[1]:g}")
    print(f"  WALK-FORWARD 2013-2026: chosen combos total {sum(wf):.1f} R vs current {Y.loc[2013:, BASE].sum():.1f} R; "
          f"better in {sum(a > b for a, b in zip(wf, Y.loc[2013:, BASE]))}/14 years")
    print("  picks: " + ", ".join(picks))
