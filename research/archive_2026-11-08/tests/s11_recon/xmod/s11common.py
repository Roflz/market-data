"""Shared helpers for Section 11 (builder X)."""
import json
import os

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
TICK = 0.25
SEED = 12345
NREP = 1000
S0 = 480                     # slot 0 = 08:00 ET
LAST_DATE = pd.Timestamp("2026-11-06")
SPEC = {"NQ": dict(micro="MNQ", usd=2.0, cost=1.0), "ES": dict(micro="MES", usd=5.0, cost=0.70)}

BLOCKS = [("Jun2010-2011", "2010-01-01", "2011-12-31"), ("2012-13", "2012-01-01", "2013-12-31"),
          ("2014-15", "2014-01-01", "2015-12-31"), ("2016-17", "2016-01-01", "2017-12-31"),
          ("2018-19", "2018-01-01", "2019-12-31"), ("2020-21", "2020-01-01", "2021-12-31"),
          ("2022-23", "2022-01-01", "2023-12-31"), ("2024-Nov2026", "2024-01-01", "2026-12-31")]
ERAS = [("Jun2010-Dec2017", "2010-01-01", "2017-12-31"), ("2018-01-01..2022-05-18", "2018-01-01", "2022-05-18"),
        ("2022-05-19..2024-12", "2022-05-19", "2024-12-31"), ("2025-01..latest", "2025-01-01", "2026-12-31")]


def slot(hhmm):
    h, m = divmod(hhmm, 100)
    return h * 60 + m - S0


def slot_time(s):
    m = int(s) + S0
    return f"{m // 60:02d}:{m % 60:02d}"


def load(sym):
    return pd.read_pickle(f"{OUT}/cache_{sym}.pkl")


def ffill_close(C):
    """forward-filled close within each day (a minute with no trade carries the last close)."""
    nd, ns = C.shape
    present = ~np.isnan(C)
    idx = np.where(present, np.arange(ns)[None, :], -1)
    idx = np.maximum.accumulate(idx, axis=1)
    out = C[np.arange(nd)[:, None], np.maximum(idx, 0)]
    out[idx < 0] = np.nan
    return out


def next_valid(O):
    """nv[d, s] = first slot >= s with a bar (non-NaN open), or NS (none)."""
    nd, ns = O.shape
    present = ~np.isnan(O)
    idx = np.where(present, np.arange(ns)[None, :], ns)
    return np.minimum.accumulate(idx[:, ::-1], axis=1)[:, ::-1]


def vix_calm(days):
    """calm[D] = VIX close on D-1 <= median of the 252 VIX closes ending D-1 (Yahoo VIX_index, dates < D)."""
    v = pd.read_csv("data/yahoo_daily/VIX_index.csv", usecols=["Date", "Close"]).dropna()
    v["Date"] = pd.to_datetime(v.Date)
    v = v.set_index("Date").Close.sort_index()
    med = v.rolling(252, min_periods=252).median()
    pos = v.index.searchsorted(pd.DatetimeIndex(days), side="left") - 1      # last VIX date strictly before D
    last = v.to_numpy()[pos]
    m = med.to_numpy()[pos]
    return pd.Series(last <= m, index=days), pd.Series(last, index=days), pd.Series(m, index=days)


def calendar_flags(days):
    import calendar_days as cd
    days = pd.DatetimeIndex(days)
    fomc = days.isin(list(cd.fomc_days()))
    opex = days.isin(list(cd.expiry_fridays(days)))
    return fomc, opex


def nw_t(x, lags=5):
    x = np.asarray(x, float)
    T = len(x)
    if T < 10 or np.allclose(x, x[0]):
        return float("nan")
    u = x - x.mean()
    s = u @ u / T
    for j in range(1, lags + 1):
        s += 2.0 * (1.0 - j / (lags + 1.0)) * (u[j:] @ u[:-j]) / T
    return float(x.mean() / np.sqrt(s / T)) if s > 0 else float("nan")


def iid_t(x):
    x = np.asarray(x, float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def max_dd(daily):
    eq = np.cumsum(np.asarray(daily, float))
    if len(eq) == 0:
        return 0.0
    return float((np.maximum.accumulate(np.r_[0.0, eq]) - np.r_[0.0, eq]).max())


def period_stats(tr, lo, hi, col_usd="net_usd", col_bp="net_bp"):
    m = (tr.date >= pd.Timestamp(lo)) & (tr.date <= pd.Timestamp(hi))
    t = tr[m]
    return dict(trades=int(len(t)), net_usd=float(t[col_usd].sum()), usd_per_trade=float(t[col_usd].mean()) if len(t) else None,
                bp_per_trade=float(t[col_bp].mean()) if len(t) else None,
                gross_usd=float(t.gross_usd.sum()) if "gross_usd" in t else None,
                hit=float((t[col_usd] > 0).mean()) if len(t) else None)


def headline(tr, first_day, by_day=True):
    """standard headline: $/trade, total, bp/trade, trades/yr, t (day-level NW5 on daily bps; also iid), eras, blocks."""
    if len(tr) == 0:
        return dict(trades=0)
    years = (LAST_DATE - pd.Timestamp(first_day)).days / 365.25
    daily_bp = tr.groupby("date").net_bp.sum()
    daily_usd = tr.groupby("date").net_usd.sum()
    out = dict(trades=int(len(tr)), days=int(len(daily_bp)), net_usd_per_trade=float(tr.net_usd.mean()),
               total_usd=float(tr.net_usd.sum()), gross_usd_total=float(tr.gross_usd.sum()),
               net_bp_per_trade=float(tr.net_bp.mean()), gross_bp_per_trade=float(tr.gross_bp.mean()),
               trades_per_year=float(len(tr) / years), hit_rate=float((tr.net_usd > 0).mean()),
               t_nw5_daily_bp=nw_t(daily_bp.to_numpy()), t_iid_daily_bp=iid_t(daily_bp.to_numpy()),
               t_iid_daily_usd=iid_t(daily_usd.to_numpy()), max_dd_usd=max_dd(daily_usd.to_numpy()),
               exit_mix={k: int(v) for k, v in tr.exit_reason.value_counts().items()},
               stress_total_usd=float(tr.stress_usd.sum()) if "stress_usd" in tr else None,
               stress_bp_per_trade=float(tr.stress_bp.mean()) if "stress_bp" in tr else None)
    out["eras"] = {n: period_stats(tr, a, b) for n, a, b in ERAS}
    out["blocks"] = {n: period_stats(tr, a, b) for n, a, b in BLOCKS}
    out["blocks_positive"] = int(sum(v["net_usd"] > 0 for v in out["blocks"].values()))
    out["gross_blocks_positive"] = int(sum((v["gross_usd"] or 0) > 0 for v in out["blocks"].values()))
    out["pts_per_trade_by_era"] = {n: (float(tr[(tr.date >= a) & (tr.date <= b)].net_pts.mean())
                                       if ((tr.date >= a) & (tr.date <= b)).any() else None) for n, a, b in ERAS}
    return out


def dump(name, obj):
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, pd.Timestamp):
            return str(o.date())
        raise TypeError(type(o))
    with open(f"{OUT}/{name}", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
