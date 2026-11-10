"""NYSE full-closure holidays 2009-2026 from the published exchange rules (known years in advance; no prices used).
Used by G3 to define 'trading day' as an NYSE trading day: CME Globex trades a short session on most of these days,
but CME books that activity to the NEXT trade date, so a Globex holiday session is not a trading day.
Rules: New Year (Sun -> Mon; Sat -> not observed), MLK (3rd Mon Jan), Washington (3rd Mon Feb), Good Friday,
Memorial (last Mon May), Juneteenth (2022+; Sat -> Fri, Sun -> Mon), Independence (Sat -> Fri, Sun -> Mon),
Labor (1st Mon Sep), Thanksgiving (4th Thu Nov), Christmas (Sat -> Fri, Sun -> Mon), plus the special closures
2012-10-29/30 (Hurricane Sandy), 2018-12-05 (G.H.W. Bush), 2025-01-09 (J. Carter)."""
import datetime as dt

import pandas as pd
from dateutil.easter import easter


def _nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def _last_weekday(y, m, wd):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def _obs(d, sat_to_fri=True):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1) if sat_to_fri else None
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def nyse_holidays(y0=2009, y1=2026):
    out = set()
    for y in range(y0, y1 + 1):
        out |= {_obs(dt.date(y, 1, 1), sat_to_fri=False), _nth_weekday(y, 1, 0, 3), _nth_weekday(y, 2, 0, 3),
                easter(y) - dt.timedelta(days=2), _last_weekday(y, 5, 0), _obs(dt.date(y, 7, 4)),
                _nth_weekday(y, 9, 0, 1), _nth_weekday(y, 11, 3, 4), _obs(dt.date(y, 12, 25))}
        if y >= 2022:
            out.add(_obs(dt.date(y, 6, 19)))
    out |= {dt.date(2012, 10, 29), dt.date(2012, 10, 30), dt.date(2018, 12, 5), dt.date(2025, 1, 9)}
    out.discard(None)
    return pd.DatetimeIndex(sorted(pd.Timestamp(d) for d in out))


HOLIDAYS = nyse_holidays()

if __name__ == "__main__":
    h = HOLIDAYS
    print(len(h), h[(h.year >= 2024) & (h.year <= 2025)].strftime("%Y-%m-%d %a").tolist())
