"""
Market context for each S&P 500 trading day, using ONLY information available before that day's 9:30 ET open.
Output: data/market_context.pkl (index = trading date, 1928-2026; most columns start later, see below).

Sources (all already in data/):
  yahoo_daily/*.csv        daily closes: S&P 500 (1928-), Nasdaq-100 (1985-), VIX (1990-), 10-yr yield (1962-),
                           dollar index (1971-), crude oil and gold front futures (2000-)
  events/All_Daily_Policy_Data.csv     daily US Economic Policy Uncertainty index, Baker-Bloom-Davis (1985-)
  events/data_gpr_daily_recent.csv     daily Geopolitical Risk index, Caldara-Iacoviello (1985-), incl. 11 labeled events
  {CL,ZN,ZB,6E,GC,ES,NQ}_fut_1h.csv    CME hourly bars from Databento (2010-), for overnight cross-market moves (optional)

Timing rules (no look-ahead):
  *_prev columns    value as of the previous trading day's close (or the latest observation strictly before the date);
                    EPU and GPR, which have a value for every calendar day, average everything since the previous
                    trading day (so Friday and weekend readings reach Monday)
  on_*              overnight move from the previous trading day's 16:00 ET to 9:00 ET on the date (known at 9:00)
  regime flags      percentiles over earlier rows only, so each day is compared with the past, never with the future:
                    VIX against all earlier days (250-row burn-in); EPU and GPR against the previous ~5 years (1,260
                    rows), because those indexes trend upward over the decades
  gpr_event_label_sameday_HINDSIGHT   the authors' label for an event ON that date: for describing event days only,
                    never as a trading input
Caveat for live use: the EPU and GPR indexes are published with a delay (GPR is updated about weekly), so a 1-day lag
is optimistic in real time. Treat those columns as research descriptors; for live rules, lag them by at least a week.
Usage:  PYTHONPATH=./pylib python3 market_context.py
"""
import os

import numpy as np
import pandas as pd

Y = "data/yahoo_daily"


def ycl(name):
    d = pd.read_csv(f"{Y}/{name}.csv", parse_dates=["Date"], index_col="Date")
    s = d["Close"].astype(float)
    s.index = s.index.normalize()
    return s[s > 0].dropna().sort_index()


def prev_value(series, dates):
    """Latest value of `series` strictly before each date (NaN if none)."""
    pos = np.searchsorted(series.index.values, dates.values, side="left") - 1
    out = np.where(pos >= 0, series.values[np.clip(pos, 0, None)], np.nan)
    return pd.Series(out, index=dates)


def since_prev(series, dates, how="mean"):
    """Combine every observation dated from the previous trading date up to the day before each date (so Friday,
    Saturday and holiday readings reach the next trading day). how = 'mean' or 'max'."""
    s = series.dropna().sort_index()
    idx = np.searchsorted(dates.values, s.index.values, side="right")   # first trading date strictly after the obs
    ok = idx < len(dates)
    g = pd.Series(s.values[ok]).groupby(idx[ok])
    agg = g.mean() if how == "mean" else g.max()
    out = pd.Series(np.nan, index=dates)
    out.iloc[agg.index.to_numpy()] = agg.to_numpy(float)
    return out


def expanding_rank(x, burn=250):
    """Percentile (0-1) of each value among all earlier non-NaN values incl. itself; NaN during the burn-in."""
    v = x.to_numpy(float)
    out = np.full(len(v), np.nan)
    seen = []
    import bisect
    for i, val in enumerate(v):
        if np.isnan(val):
            continue
        bisect.insort(seen, val)
        if len(seen) > burn:
            out[i] = bisect.bisect_right(seen, val) / len(seen)
    return pd.Series(out, index=x.index)


def index_features(c, prefix):
    r = np.log(c).diff()
    f = pd.DataFrame({
        f"{prefix}_ret_1d": c.pct_change() * 100,
        f"{prefix}_ret_5d": c.pct_change(5) * 100,
        f"{prefix}_ma200_gap": (c / c.rolling(200).mean() - 1) * 100,
        f"{prefix}_drawdown": (c / c.cummax() - 1) * 100,                      # from the all-time high
        f"{prefix}_off_52w_high": (c / c.rolling(252, min_periods=1).max() - 1) * 100,
        f"{prefix}_rv20": r.rolling(20).std() * np.sqrt(252) * 100,
    })
    return f


def overnight(sym, dates):
    """Overnight log move 16:00 (prior trading day) -> 9:00 ET from hourly bars, and its z-score vs the prior 60."""
    path = f"data/{sym}_fut_1h.csv"
    if not os.path.exists(path):
        return None
    h = pd.read_csv(path, index_col=0)
    h.index = pd.to_datetime(h.index, utc=True).tz_convert("America/New_York")
    h = h[~h.index.duplicated()].sort_index()
    day = h.index.tz_localize(None).normalize()
    hour = h.index.hour
    close_1600 = h[hour == 15].assign(d=day[hour == 15]).groupby("d").agg(px=("Close", "last"), inst=("instrument_id", "last"))
    close_0900 = h[hour == 8].assign(d=day[hour == 8]).groupby("d").agg(px=("Close", "last"), inst=("instrument_id", "last"))
    prev_px = prev_value(close_1600.px, dates)
    prev_inst = prev_value(close_1600.inst.astype(float), dates)
    # the 16:00 reference must come from the previous trading day itself, not from an older day (data gaps,
    # early closes without a 15:00 bar), or the "overnight" move would span extra sessions
    pos = np.searchsorted(close_1600.index.values, dates.values, side="left") - 1
    src = pd.Series(np.where(pos >= 0, close_1600.index.values[np.clip(pos, 0, None)], np.datetime64("NaT")),
                    index=dates)
    stale = ~(src.values >= dates.to_series().shift(1).values)
    now = close_0900.reindex(dates)
    ret = np.log(now.px / prev_px) * 100
    ret[now.inst.astype(float) != prev_inst] = np.nan                    # contract roll overnight: no clean move
    ret[stale] = np.nan
    z = ret / ret.rolling(60, min_periods=40).std().shift(1)
    return pd.DataFrame({f"on_{sym}_ret": ret, f"on_{sym}_z": z})


def main():
    spx = ycl("SP500_index")
    dates = pd.DatetimeIndex(spx.index)
    ctx = pd.DataFrame(index=dates)
    # previous-day index state: S&P on its own calendar (shift one row), Nasdaq-100 aligned to strictly-before
    sf = index_features(spx, "spx").shift(1)
    ctx = ctx.join(sf.add_suffix("_prev"))
    nf = index_features(ycl("NASDAQ100_index"), "ndx")
    for col in nf.columns:
        ctx[f"{col}_prev"] = prev_value(nf[col].dropna(), dates)
    vix = ycl("VIX_index")
    ctx["vix_prev"] = prev_value(vix, dates)
    ctx["vix_chg_prev"] = prev_value(vix.diff().dropna(), dates)
    tnx = ycl("US10Y_yield")
    ctx["us10y_prev"] = prev_value(tnx, dates)
    ctx["us10y_chg_bp_prev"] = prev_value((tnx.diff() * 100).dropna(), dates)
    for name, col in (("dollar_index", "dollar"), ("crude_oil_front", "oil"), ("gold_front", "gold")):
        s = ycl(name)
        ctx[f"{col}_ret_1d_prev"] = prev_value((s.pct_change() * 100).dropna(), dates)
    # uncertainty indexes
    e = pd.read_csv("data/events/All_Daily_Policy_Data.csv")
    epu = pd.Series(e.daily_policy_index.values, index=pd.to_datetime(dict(year=e.year, month=e.month, day=e.day))).sort_index()
    # these indexes have a value for every calendar day: average (or max) everything since the previous trading day
    ctx["epu_prev"] = since_prev(epu, dates, "mean")
    ctx["epu_7d_prev"] = prev_value(epu.rolling(7).mean().dropna(), dates)
    g = pd.read_csv("data/events/data_gpr_daily_recent.csv", parse_dates=["date"]).dropna(subset=["GPRD"])
    gs = g.set_index("date").sort_index()
    for src, col in (("GPRD", "gpr"), ("GPRD_ACT", "gpr_act"), ("GPRD_THREAT", "gpr_threat")):
        ctx[f"{col}_prev"] = since_prev(gs[src], dates, "mean")
    ratio = (gs.GPRD / gs.GPRD.rolling(30).mean().shift(1)).dropna()       # on the GPR calendar
    ctx["gpr_spike_prev"] = since_prev(ratio, dates, "max")
    ctx["gpr_event_label_sameday_HINDSIGHT"] = gs.event.reindex(dates)
    # overnight cross-market moves (2010-)
    have = []
    for sym in ("CL", "ZN", "ZB", "6E", "GC", "ES", "NQ"):
        o = overnight(sym, dates)
        if o is not None:
            ctx = ctx.join(o)
            have.append(sym)
    # regime flags (expanding, past-only)
    ctx["vix_pct"] = expanding_rank(ctx.vix_prev)
    ctx["vix_tercile"] = np.ceil(ctx.vix_pct * 3).clip(1, 3)
    ctx["trend_up"] = (ctx.spx_ma200_gap_prev > 0).where(ctx.spx_ma200_gap_prev.notna())
    ctx["in_correction_10"] = (ctx.spx_off_52w_high_prev <= -10).where(ctx.spx_off_52w_high_prev.notna())
    # uncertainty indexes drift upward over the decades, so compare each day with the previous ~5 years, not all history
    ctx["epu_top10"] = (ctx.epu_prev.rolling(1260, min_periods=250).rank(pct=True) >= 0.9).where(ctx.epu_prev.notna())
    ctx["gpr_top10"] = (ctx.gpr_prev.rolling(1260, min_periods=250).rank(pct=True) >= 0.9).where(ctx.gpr_prev.notna())
    ctx["gpr_spike2x"] = (ctx.gpr_spike_prev >= 2).where(ctx.gpr_spike_prev.notna())     # any 2x day since prev trading day
    ctx["gpr_spike_last3"] = ctx.gpr_spike2x.rolling(3, min_periods=1).max()            # ... within the last 3 trading days
    shock_syms = [s for s in ("CL", "ZN", "6E", "GC") if s in have]
    zc = [f"on_{s}_z" for s in shock_syms]
    if zc:
        ctx["cross_shock_3sd"] = (ctx[zc].abs() >= 3).any(axis=1).where(ctx[zc].notna().any(axis=1))
    ctx.attrs["cross_shock_syms"] = shock_syms
    ctx.to_pickle("data/market_context.pkl")
    print(f"market_context: {len(ctx):,} trading days {ctx.index.min():%Y-%m-%d} -> {ctx.index.max():%Y-%m-%d}, "
          f"{ctx.shape[1]} columns; hourly cross-market data used: {', '.join(have) or 'none yet'}")
    since = ctx.loc["2010-06-07":]
    print("2010-2026 coverage: " + ", ".join(f"{c} {since[c].notna().mean():.0%}" for c in
                                            ("vix_prev", "epu_prev", "gpr_prev", "ndx_drawdown_prev") + tuple(zc)))
    for c in ("trend_up", "in_correction_10", "epu_top10", "gpr_top10", "gpr_spike2x", "gpr_spike_last3") + (("cross_shock_3sd",) if zc else ()):
        print(f"  {c}: {since[c].mean():.1%} of 2010-2026 days")


if __name__ == "__main__":
    main()
