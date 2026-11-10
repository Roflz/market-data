"""
Builder X, filters T1-T4: per-session filter inputs, all known at 9:35 ET on the session date.
Writes T_X/inputs.pkl (one row per Globex session in the 1-min data) and T_X/bars.pkl (cached 1-min bars).

Back-adjustment, session labels and the daily trend replicate fut_build.load_raw / fut_build.build exactly.
"""
import os
import numpy as np
import pandas as pd

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/T_X"
BARS = f"{OUT}/bars.pkl"


def load_bars():
    if os.path.exists(BARS):
        return pd.read_pickle(BARS)
    d = pd.read_csv("data/NQ_fut_1m.csv", index_col=0,
                    usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"])
    d.index = pd.to_datetime(d.index, utc=True).tz_convert("America/New_York")
    d = d[~d.index.duplicated()].sort_index()
    # back-adjust rolls exactly as fut_build.load_raw / daily_sessions.py
    roll = d.instrument_id.ne(d.instrument_id.shift()) & d.instrument_id.shift().notna()
    jump = (d.Open - d.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    d["adj"] = adj
    for c in ("Open", "High", "Low", "Close"):
        d["a" + c[0]] = d[c] + adj
    d["sess"] = pd.to_datetime((d.index + pd.Timedelta(hours=6)).date)
    d["tmin"] = d.index.hour * 60 + d.index.minute
    d["cal"] = pd.to_datetime(d.index.date)
    d.to_pickle(BARS)
    return d


def build(d, ds):
    """Inputs per session date; uses only bars stamped before 9:35 ET of that date for that date's values."""
    sess_dates = pd.DatetimeIndex(sorted(d.sess.unique()))
    out = pd.DataFrame(index=sess_dates)
    out.index.name = "date"
    on_date = d.cal == d.sess                    # bar's calendar day is the session day (i.e. after midnight)

    # ---- T1: overnight-break model trend = sign(C_9:34 - EMA20 of prior session closes) (fut_build.build) ----
    daily_c = d.groupby("sess").aC.last()        # every Globex session in the data, as fut_build does
    ema20 = daily_c.ewm(span=20, adjust=False).mean()
    prev_ema = ema20.shift()                     # previous session's EMA (known before today's session starts)
    c934 = d.aC[on_date & (d.tmin == 574)].groupby(d.sess[on_date & (d.tmin == 574)]).last()
    # fallback when the 9:34 bar is missing: last close stamped 9:30-9:34 (still closed by 9:35)
    w = on_date & (d.tmin >= 570) & (d.tmin < 575)
    c_last_or = d.aC[w].groupby(d.sess[w]).last()
    out["c934"] = c934.reindex(sess_dates)
    out["c934_fallback"] = out.c934.isna() & c_last_or.reindex(sess_dates).notna()
    out["c934"] = out.c934.fillna(c_last_or.reindex(sess_dates))
    out["prev_ema20"] = prev_ema.reindex(sess_dates)
    out["trend_diff"] = out.c934 - out.prev_ema20
    out["trend"] = np.sign(out.trend_diff)

    # ---- T3: first-candle range, 9:30-9:34 bars (adjusted prices: exact within a contract) ----
    g = d[w].groupby(d.sess[w])
    out["fc_range"] = (g.aH.max() - g.aL.min()).reindex(sess_dates)
    out["fc_nbars"] = g.size().reindex(sess_dates).fillna(0).astype(int)

    # ---- T4: overnight range, 18:00 ET prior evening -> 9:29 bar ----
    start = d.sess - pd.Timedelta(days=1) + pd.Timedelta(hours=18)
    naive = d.index.tz_localize(None)
    won = (naive >= start.to_numpy()) & ((~on_date) | (d.tmin < 570))
    # session label = calendar day of (ts + 6h): every bar of sess D is stamped after D-1 18:00; this enforces it
    g = d[won].groupby(d.sess[won])
    out["on_range"] = (g.aH.max() - g.aL.min()).reindex(sess_dates)
    out["on_nbars"] = g.size().reindex(sess_dates).fillna(0).astype(int)
    out["on_first"] = g.apply(lambda x: x.index[0]).reindex(sess_dates)

    # ---- T2 parts: today's 9:30 open, and this session's 15:59 / 12:59 close (adjusted) ----
    o930 = d.aO[on_date & (d.tmin == 570)]
    out["open930_adj"] = o930.groupby(d.sess[on_date & (d.tmin == 570)]).first().reindex(sess_dates)
    for nm, last_t in (("close1559_adj", 959), ("close1259_adj", 779)):
        m = on_date & (d.tmin >= 570) & (d.tmin <= last_t)
        x = d[m].groupby(d.sess[m]).agg(c=("aC", "last"), t=("tmin", "last"))
        out[nm] = x.c.reindex(sess_dates)
        out[nm.replace("adj", "tmin")] = x.t.reindex(sess_dates)

    # restrict to cash days and attach session flags
    cash = ds[ds.cash_day]
    out = out.reindex(cash.index)
    out.index.name = "date"
    out["early_close"] = cash.early_close
    out["close_adj_sess"] = np.where(out.early_close, out.close1259_adj, out.close1559_adj)
    out["close_tmin_sess"] = np.where(out.early_close, out.close1259_tmin, out.close1559_tmin)
    out["prev_cash_date"] = pd.Series(out.index, index=out.index).shift()
    out["prev_close_adj"] = out.close_adj_sess.shift()
    out["gap"] = out.open930_adj - out.prev_close_adj

    # ---- rolling medians over the previous 20 cash sessions (strictly before today; NaN values skipped) ----
    for col, nm in (("fc_range", "fc_med20"), ("on_range", "on_med20")):
        v = out[col].to_numpy()
        pos = np.flatnonzero(~np.isnan(v))                       # cash sessions with a value
        rmed = pd.Series(v[pos]).rolling(20).median().to_numpy()  # median of valid values pos[k-19..k]
        cnt = np.searchsorted(pos, np.arange(len(v)), side="left")  # number of valid sessions strictly before i
        med = np.full(len(v), np.nan)
        ok = cnt >= 20
        med[ok] = rmed[cnt[ok] - 1]
        out[nm] = med
        out[nm.replace("med20", "nprior")] = cnt
    return out


if __name__ == "__main__":
    d = load_bars()
    ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
    inp = build(d, ds)
    inp.to_pickle(f"{OUT}/inputs.pkl")
    print(inp.describe().T)
    print(inp.isna().sum())
