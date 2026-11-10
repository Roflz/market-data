"""
Shared calendar definitions, so every script uses the same days (review item 7.4).
  expiry_fridays(trading_days)  monthly options expiry: the third Friday, or the last trading day before it in that
                                week when the Friday is a holiday (e.g. Good Friday)
  fomc_days(), cpi_days()       scheduled FOMC statement dates and CPI release dates from data/*.csv
All take/return pandas Timestamps (dates, no time).
"""
import pandas as pd


def expiry_fridays(trading_days):
    ds = pd.DatetimeIndex(sorted(set(pd.to_datetime(list(trading_days)).normalize())))
    out = set()
    for (y, m), _ in pd.Series(ds, index=ds).groupby([ds.year, ds.month]):
        first = pd.Timestamp(y, m, 1)
        third_fri = first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)
        if third_fri in ds:
            out.add(third_fri)
        elif ds.max() > third_fri:                  # Friday missing inside the data = a holiday: use the day before
            cand = ds[(ds < third_fri) & (ds >= third_fri - pd.Timedelta(days=4))]
            if len(cand):
                out.add(cand.max())
        # Friday beyond the end of the data: no expiry for that month yet
    return out


def fomc_days(scheduled_only=True):
    f = pd.read_csv("data/fomc_dates.csv")
    if scheduled_only:
        f = f[f.scheduled]
    return set(pd.to_datetime(f.date).dt.normalize())


def cpi_days():
    return set(pd.to_datetime(pd.read_csv("data/cpi_dates.csv").date).dt.normalize())
