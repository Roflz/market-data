"""DST natural experiment re-check (London open, Tokyo open), day-normalised; plus first-Friday 8:30 and CPI-fade concentration."""
import sys, os
from zoneinfo import ZoneInfo
from datetime import datetime
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from events import event, cpi, MULT, COST
D = os.path.dirname(__file__)
ET, LON, TYO = ZoneInfo("America/New_York"), ZoneInfo("Europe/London"), ZoneInfo("Asia/Tokyo")


def et_min_of(local_tz, h, m, date):
    t = datetime(date.year, date.month, date.day, h, m, tzinfo=local_tz).astimezone(ET)
    return t.hour * 60 + t.minute


for sym in ("NQ", "ES"):
    df = pd.read_parquet(f"{D}/slots_{sym}.parquet")
    df["a"] = df.mv.abs()
    dn = df.groupby("sess").a.transform("mean")
    df["r"] = df.a / dn                      # day-normalised: each day's average slot = 1
    days = pd.DatetimeIndex(sorted(df.sess.unique()))
    lon = pd.Series([et_min_of(LON, 8, 0, d) for d in days], index=days)       # London open in ET minutes (same date)
    # Tokyo 09:00 JST on session date d = ET evening of d-1
    tyo = pd.Series([et_min_of(TYO, 9, 0, d) for d in days], index=days)
    piv = df.pivot_table(index="sess", columns="et_min", values="r")
    piv.index = pd.DatetimeIndex(piv.index)
    print(f"\n{sym}: London open ET minute counts:", lon.value_counts().to_dict())
    for lab, mask in (("normal (03:00 ET)", lon == 180), ("mismatch (04:00 ET)", lon == 240)):
        sub = piv[mask.reindex(piv.index).fillna(False).to_numpy()]
        print(f"  London {lab} n={len(sub)}: 02:30-02:55 avg {sub[[150,155,160,165,170,175]].mean().mean():.2f}x | "
              f"03:00 {sub[180].mean():.2f}x | 03:30-03:55 avg {sub[[210,215,220,225,230,235]].mean().mean():.2f}x | "
              f"04:00 {sub[240].mean():.2f}x | 02:00 {sub[120].mean():.2f}x")
    print(f"  Tokyo open ET minute counts:", tyo.value_counts().to_dict())
    for lab, mask, t in (("winter 19:00 ET", tyo == 19 * 60, 19 * 60), ("summer 20:00 ET", tyo == 20 * 60, 20 * 60)):
        sub = piv[mask.reindex(piv.index).fillna(False).to_numpy()]
        print(f"  Tokyo {lab} n={len(sub)}: 19:00 {sub[1140].mean():.2f}x  20:00 {sub[1200].mean():.2f}x  "
              f"30min before event {sub[[t - 30, t - 25, t - 20, t - 15, t - 10, t - 5]].mean().mean():.2f}x")
    # first-Friday proxy at 8:30
    s830 = df[df.et_min == 510].copy()
    sd = pd.DatetimeIndex(s830.sess)
    ff = (sd.day_of_week == 4) & (sd.day <= 7)
    print(f"  8:30 first-Friday n={ff.sum()} mean {s830.a[ff].mean():.1f} bp; Thursdays {s830.a[sd.day_of_week == 3].mean():.1f}")

# CPI fade concentration (k15/h60, NQ and ES)
for sym in ("NQ", "ES"):
    d = event(sym, 510, 15, 60, days=cpi)
    d = d[d.imp != 0]
    d["fade_usd"] = -np.sign(d.imp) * d.fol_pts * MULT[sym] - COST[sym]
    y = d.groupby("yr").fade_usd.agg(["size", "mean", "sum"]).round(1)
    print(f"\n{sym} CPI fade 08:45->09:45 ET net $/trade by year:\n", y.T.to_string())
    no22 = d[d.yr != 2022]
    print(f"  all {d.fade_usd.mean():+.2f} (t {d.fade_usd.mean() / (d.fade_usd.std() / np.sqrt(len(d))):.2f}); "
          f"ex-2022 {no22.fade_usd.mean():+.2f}; median {d.fade_usd.median():+.2f}; hit {np.mean(d.fade_usd > 0):.2f}; "
          f"top-5 trades sum {d.fade_usd.nlargest(5).sum():.0f} of total {d.fade_usd.sum():.0f}")
