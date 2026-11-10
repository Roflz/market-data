"""
Section 11 builder Y: shared data loading and statistics helpers.
Run from the project dir (read only) with PYTHONPATH=./pylib; everything is written to OUT (this file's folder).

Day grid: for every NY calendar date, 1-minute bars stamped 08:00 .. 15:59 ET (480 slots), slot s = minute 480 + s.
  slot 90 = 09:30, slot 150 = 10:30, slot 420 = 15:00, slot 479 = 15:59.
Prices are raw (not back-adjusted). The contract of day D is the Databento NQ.v.0 / ES.v.0 front contract of that
Globex session (chosen by Databento from the prior session's volume); the loader checks that every bar 08:00-15:59
of a day carries the same instrument_id.
"""
import os
import pickle
import sys

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
PROJ = "/run/media/roflz/Disk 2/_/market_data"
sys.path.insert(1, PROJ)
import calendar_days as cdays  # noqa: E402  (project module, read only)

TICK = 0.25
NSLOT = 480
S0930, S1030, S1500, S1559 = 90, 150, 420, 479
SPEC = {"NQ": dict(micro="MNQ", usd=2.0, cost_pts=1.0), "ES": dict(micro="MES", usd=5.0, cost_pts=0.70)}
SEED = 12345
NREP = 1000
NW_LAGS = 5

BLOCKS = [("2010-2011", "2010-06-01", "2011-12-31"), ("2012-2013", "2012-01-01", "2013-12-31"),
          ("2014-2015", "2014-01-01", "2015-12-31"), ("2016-2017", "2016-01-01", "2017-12-31"),
          ("2018-2019", "2018-01-01", "2019-12-31"), ("2020-2021", "2020-01-01", "2021-12-31"),
          ("2022-2023", "2022-01-01", "2023-12-31"), ("2024-2026", "2024-01-01", "2026-12-31")]
ERAS = [("Jun2010-Dec2017", "2010-06-01", "2017-12-31"), ("Jan2018-18May2022", "2018-01-01", "2022-05-18"),
        ("19May2022-Dec2024", "2022-05-19", "2024-12-31"), ("Jan2025-latest", "2025-01-01", "2026-12-31")]


def hhmm(slot):
    m = 480 + int(slot)
    return f"{m // 60:02d}:{m % 60:02d}"


def slot_of(h, m):
    return h * 60 + m - 480


# ------------------------------------------------------------------------------------------------------------
# data
# ------------------------------------------------------------------------------------------------------------
def load_grid(sym):
    """dict with dates (DatetimeIndex), O,H,L,C,V (nd x 480, NaN where no bar), Cff (forward-filled close within
    the day, NaN before the first bar), inst (per day), n_inst_mix (days with >1 instrument 08:00-15:59)."""
    cache = os.path.join(OUT, f"grid_{sym}.pkl")
    if os.path.exists(cache):
        with open(cache, "rb") as f:
            return pickle.load(f)
    d = pd.read_csv(os.path.join(PROJ, "data", f"{sym}_fut_1m.csv"),
                    usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"])
    ts = pd.DatetimeIndex(pd.to_datetime(d["ts_event"], utc=True, format="ISO8601")).tz_convert("America/New_York")
    tm = np.asarray(ts.hour * 60 + ts.minute)
    m = (tm >= 480) & (tm < 960)
    d = d.loc[m].reset_index(drop=True)
    ts = ts[m]
    slot = tm[m] - 480
    dates = pd.Index(ts.strftime("%Y-%m-%d"))
    di, ud = pd.factorize(dates, sort=True)
    nd = len(ud)
    g = {"dates": pd.DatetimeIndex(pd.to_datetime(np.asarray(ud)))}
    for c, k in [("Open", "O"), ("High", "H"), ("Low", "L"), ("Close", "C"), ("Volume", "V")]:
        a = np.full((nd, NSLOT), np.nan)
        a[di, slot] = d[c].to_numpy(float)
        g[k] = a
    ib = np.full((nd, NSLOT), -1, dtype=np.int64)
    ib[di, slot] = d["instrument_id"].to_numpy()
    first = np.argmax(ib >= 0, axis=1)
    inst = ib[np.arange(nd), first]
    mix = ((ib >= 0) & (ib != inst[:, None])).any(axis=1)
    g["inst"] = inst
    g["inst_mix"] = mix
    # forward-filled close within the day
    present = ~np.isnan(g["C"])
    idx = np.where(present, np.arange(NSLOT)[None, :], -1)
    idx = np.maximum.accumulate(idx, axis=1)
    Cff = np.where(idx >= 0, g["C"][np.arange(nd)[:, None], np.maximum(idx, 0)], np.nan)
    g["Cff"] = Cff
    with open(cache, "wb") as f:
        pickle.dump(g, f, protocol=4)
    return g


def calendar(sym="NQ"):
    """Per-date flags from daily_sessions: cash_day, early_close, plus FOMC and monthly opex sets."""
    ds = pd.read_pickle(os.path.join(PROJ, "data", f"daily_sessions_{sym}.pkl"))
    ds.index = pd.DatetimeIndex(ds.index).normalize()
    cash = ds.index[ds.cash_day]
    cwd = os.getcwd()
    os.chdir(PROJ)
    try:
        fomc = cdays.fomc_days()
    finally:
        os.chdir(cwd)
    opex = cdays.expiry_fridays(cash)
    return ds, set(fomc), set(opex)


def vix_calm():
    """Series indexed by trading date D: True if VIX close on D-1 <= median of the 252 VIX closes ending D-1.
    Returned as a function of D (uses only closes dated strictly before D)."""
    v = pd.read_csv(os.path.join(PROJ, "data", "yahoo_daily", "VIX_index.csv"), usecols=["Date", "Close"])
    v["Date"] = pd.to_datetime(v.Date)
    v = v.dropna().set_index("Date").Close.sort_index()
    med = v.rolling(252, min_periods=252).median()
    tab = pd.DataFrame({"vix": v, "med": med})

    def f(dates):
        dates = pd.DatetimeIndex(dates)
        pos = tab.index.searchsorted(dates, side="left") - 1          # last VIX close strictly before D
        ok = pos >= 0
        vv = np.full(len(dates), np.nan)
        mm = np.full(len(dates), np.nan)
        vv[ok] = tab.vix.to_numpy()[pos[ok]]
        mm[ok] = tab.med.to_numpy()[pos[ok]]
        prevdate = np.array([tab.index[p] if p >= 0 else pd.NaT for p in pos])
        return pd.DataFrame({"vix_prev": vv, "vix_med252": mm, "vix_date": prevdate,
                             "calm": (vv <= mm) & ~np.isnan(mm)}, index=dates)
    return f


# ------------------------------------------------------------------------------------------------------------
# statistics
# ------------------------------------------------------------------------------------------------------------
def nw_t(x, lags=NW_LAGS):
    x = np.asarray(x, float)
    T = len(x)
    if T < 3:
        return np.nan
    u = x - x.mean()
    s = u @ u / T
    for j in range(1, lags + 1):
        if j < T:
            s += 2.0 * (1.0 - j / (lags + 1.0)) * (u[j:] @ u[:-j]) / T
    if s <= 0:
        return np.nan
    return float(x.mean() / np.sqrt(s / T))


def plain_t(x):
    x = np.asarray(x, float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def max_dd(daily):
    c = np.cumsum(np.asarray(daily, float))
    if len(c) == 0:
        return 0.0
    peak = np.maximum.accumulate(np.concatenate([[0.0], c]))[1:]
    return float((peak - c).max())


def span_years(dates):
    dates = pd.DatetimeIndex(dates)
    return (dates.max() - dates.min()).days / 365.25 if len(dates) > 1 else np.nan


def by_period(T, periods, col_usd="net_usd", col_gross="gross_usd"):
    out = []
    for name, a, b in periods:
        m = (T.date >= a) & (T.date <= b)
        g = T[m]
        out.append({"period": name, "trades": int(len(g)), "net_usd": float(g[col_usd].sum()),
                    "gross_usd": float(g[col_gross].sum()) if col_gross in g else None,
                    "net_usd_per_trade": float(g[col_usd].mean()) if len(g) else None,
                    "net_bp_per_trade": float(g.net_bp.mean()) if len(g) else None,
                    "net_pts_per_trade": float(g.net_pts.mean()) if len(g) else None,
                    "t_plain_bp": plain_t(g.net_bp) if len(g) > 2 else None})
    return out


def headline(T, sample_years=None):
    """Headline numbers for a trade frame with date, net_usd, net_bp, gross_usd."""
    if len(T) == 0:
        return {"trades": 0}
    yrs = sample_years if sample_years else span_years(T.date)
    day = T.groupby("date").agg(net_bp=("net_bp", "sum"), net_usd=("net_usd", "sum"))
    return {"trades": int(len(T)), "first": str(T.date.min().date()), "last": str(T.date.max().date()),
            "net_usd_per_trade": float(T.net_usd.mean()), "total_usd": float(T.net_usd.sum()),
            "gross_usd_total": float(T.gross_usd.sum()), "net_bp_per_trade": float(T.net_bp.mean()),
            "gross_bp_per_trade": float(T.gross_bp.mean()), "net_pts_per_trade": float(T.net_pts.mean()),
            "trades_per_year": float(len(T) / yrs) if yrs else None,
            "hit_rate": float((T.net_usd > 0).mean()),
            "t_trade_plain": plain_t(T.net_bp), "t_trade_nw5": nw_t(T.net_bp),
            "t_day_nw5": nw_t(day.net_bp.to_numpy()), "t_day_plain": plain_t(day.net_bp.to_numpy()),
            "days_traded": int(len(day)), "max_dd_usd": max_dd(day.net_usd.to_numpy()),
            "exit_mix": T.exit_reason.value_counts().to_dict() if "exit_reason" in T else None}


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, float):
        return None if np.isnan(o) else o
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp,)):
        return str(o.date())
    return o
