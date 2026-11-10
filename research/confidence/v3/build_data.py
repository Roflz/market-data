"""
v3/build_data.py - the shared v3 data files (HEAVY: loads the 1-minute data; run it under the shared flock).

  v3/data/bars_{sym}_{tf}.parquet   sym in NQ / ES / YM, tf in 5 / 15 / 60 minutes
      Same construction as signals.bars(sym, tf) (1-minute CME bars grouped by (session, contract, floor(ts, tf)),
      session VWAP from the 1-minute bars) with three differences, all applied to the 1-MINUTE rows BEFORE
      aggregation:
        * the Lucid daily close is removed: 1-minute rows starting in [16:45, 18:00) are dropped, so no bar contains
          a minute of 16:45-18:00 (a 60-min 16:00 bar = 16:00-16:44; the 5-min 16:40 bar is the last of a session);
        * one contract per session: on the ~66 roll sessions the data has the expiring contract from 18:00 to
          19:00/20:00 and the new front month after that; only the contract of the session's LAST minute (the new
          front month) is kept, so the roll session starts at 19:00/20:00;
        * the locked holdout is cut: only 1-minute rows before 2025-06-30 18:00 ET (walkforward.HOLDOUT_SESSION_START).
      Columns: O H L C V vwap inst sess seg run session ema8 ema20 ema50 mom14 atr14 trend (context from
      signals.context, computed per contract run on these bars; every value uses bars up to and including the row's
      own bar, i.e. it is known at the bar's CLOSE = index + tf). Index ts = bar START time (New York, tz-naive).
      `session` = the Lucid trading day (= sess).
  v3/data/sessions_{sym}.parquet    one row per Globex session (18:00-16:45 ET, label = trading day), same rows as
      above (one contract per session, holdout cut). See SESSION_DOC below for every column.

Run (from research/confidence):
  flock <heavy.lock> env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 \
      OMP_NUM_THREADS=3 nice -n 5 python3 v3/build_data.py [NQ ES YM]
"""
import os
import sys
import time

import numpy as np
import pandas as pd

import research_lib as rl
import signals as sg
import walkforward as wf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
TFS = (5, 15, 60)
CUT_MIN = 16 * 60 + 45                 # 16:45 wall clock
OPEN_MIN = 18 * 60                     # 18:00 wall clock
SESS_LEN = 22 * 60 + 45                # minutes from 18:00 to 16:45 = 1365
MARK_STEP = 15
MARKS = [f"{(18 * 60 + MARK_STEP * k) // 60 % 24:02d}{(MARK_STEP * k) % 60:02d}" for k in range(SESS_LEN // MARK_STEP + 1)]
RTH0, RTH1 = 15 * 60 + 30, 22 * 60     # 9:30 and 16:00 as minutes after 18:00 (930, 1320)
CTX_COLS = ["ema8", "ema20", "ema50", "mom14", "atr14", "trend"]

SESSION_DOC = """
sessions_{sym}.parquet - one row per Globex session; index `session` = trading day (the 18:00 ET open of the
previous calendar day belongs to it). Built from the kept 1-minute rows (one contract, 18:00 <= t < 16:45 of the
session's day, holdout cut). Times are New York wall clock; minute offsets count from the session's 18:00 open
(0 = 18:00, 930 = 9:30, 1320 = 16:00, 1365 = 16:45).
  px_HHMM (92 columns, HHMM = 1800, 1815, ..., 1645): executable price at that 15-minute mark = the OPEN of the
      1-minute bar starting at the mark; when that minute has no bar, the last traded price before it (the close of
      the latest earlier bar) - provided the market is still trading (there is a bar at or after the mark: this
      uses only the session's schedule, e.g. a 13:00 holiday close, which is known in advance, never a price);
      NaN before the session's first bar and after its last bar (early closes, late opens, roll sessions before the
      new contract's first minute). px_1645 = the open of the 16:45 bar, or else the close of the last bar before
      16:45 (= the last executable price, always set).
  age_HHMM (int16): minutes since the price of px_HHMM was set (0 = a bar exists at the mark; -1 where px is NaN).
  inst: contract id; roll: True when the session's contract differs from the previous session's (or the
      session's 1-minute data had two contracts); first_t / last_t: minute offsets of the first / last kept bar;
      n_min: number of 1-minute bars; first_px: open of the first bar; open_1800 = px_1800.
  rth_open = px_0930; close_1600 = close of the last bar starting before 16:00 (cash close); last_px = px_1645.
  high / low / t_high / t_low: session extremes (18:00-16:45) and the minute offsets of their first occurrence;
  rth_high / rth_low / t_rth_high / t_rth_low: same for 9:30-16:00 (NaN if no RTH bars); on_high / on_low:
      overnight 18:00-9:30.
  volume / rth_volume: contracts traded in the session / in 9:30-16:00.
  rv / rv_rth / rv_on: realized volatility in % = 100 x sqrt(sum of squared 1-minute log returns) over the session /
      9:30-16:00 / 18:00-9:30 (returns between consecutive bars of the session).
  ret_oc = last_px / first_px - 1; ret_cc = last_px / previous session's last_px - 1 (NaN on roll sessions);
  gap = first_px / previous last_px - 1 (NaN on roll sessions); ret_rth = close_1600 / rth_open - 1.
  prev_* (known at the session's open): prev_ret_cc, prev_ret_oc, prev_ret_rth, prev_rv, prev_rv_rth, prev_high,
      prev_low, prev_rth_high, prev_rth_low, prev_close_1600, prev_last_px, prev_volume - the previous session's
      values; price-level columns (prev_high ... prev_last_px) are NaN on roll sessions (other contract).
  dow: weekday of the trading day (0 = Monday); fomc / nfp / cpi: scheduled release on that trading day
      (data/fomc_dates.csv scheduled only, nfp_dates.csv, cpi_dates.csv); opex: monthly options expiry
      (calendar_days.expiry_fridays); quad: opex in Mar/Jun/Sep/Dec.
NO LOOK-AHEAD: everything except the prev_* columns, the event flags, dow, inst and roll is only known at (or after)
the time it refers to; px_HHMM is known at the mark; high/low/rv/volume/ret_* only at the session's end. Use
the current session's values only for marks already passed, or the prev_* columns.
"""


def raw_1m(sym):
    """research_lib.bars_1m(sym) as a tz-naive (New York wall clock) frame O H L C V inst sess, cut before the locked
    holdout (2025-06-30 18:00 ET). All rows (the 16:45-18:00 rows are still there)."""
    m = rl.bars_1m(sym)
    m = m.loc[m.index < wf.HOLDOUT_SESSION_START.tz_localize("America/New_York")]
    df = pd.DataFrame({"O": m.Open.to_numpy(np.float64), "H": m.High.to_numpy(np.float64),
                       "L": m.Low.to_numpy(np.float64), "C": m.Close.to_numpy(np.float64),
                       "V": m.Volume.to_numpy(np.float64), "inst": m.instrument_id.to_numpy(),
                       "sess": m.sess.to_numpy()}, index=m.index.tz_localize(None))
    df.index.name = "ts"
    return df


def filter_1m(raw):
    """The 1-minute rows used by every v3 file: [16:45, 18:00) dropped, holdout cut, one contract per session (the
    contract of the session's last row), duplicate wall-clock minutes dropped (first kept).
    Returns (frame, set of sessions that had two contracts)."""
    tm = raw.index.hour * 60 + raw.index.minute
    df = raw.loc[~((tm >= CUT_MIN) & (tm < OPEN_MIN))]
    df = df.loc[df.index < wf.HOLDOUT_SESSION_START]
    last_inst = df.groupby("sess", sort=False).inst.transform("last")
    two = set(df.loc[df.inst.ne(last_inst), "sess"].unique())
    df = df.loc[df.inst.eq(last_inst)]
    df = df[~df.index.duplicated(keep="first")]
    assert df.index.is_monotonic_increasing
    return df, two


def rows_1645(raw):
    """the 16:45 1-minute rows (their OPEN is px_1645), holdout cut."""
    d = raw.loc[(raw.index.hour == 16) & (raw.index.minute == 45), ["O", "inst", "sess"]]
    return d.loc[d.index < wf.HOLDOUT_SESSION_START]


def load_kept_1m(sym):
    """filter_1m(raw_1m(sym)) -> (kept rows, two-contract sessions)."""
    return filter_1m(raw_1m(sym))


def make_bars(df, tf):
    """signals.bars on the kept 1-minute rows (same code path, see module docstring)."""
    d = df.copy()
    tp = (d.H + d.L + d.C) / 3
    g = d.groupby([d.sess, d.inst], sort=False)
    d["vwap"] = (tp * d.V).groupby([d.sess, d.inst], sort=False).cumsum() / g.V.cumsum().replace(0, np.nan)
    bucket = d.index.floor(f"{tf}min")
    out = d.groupby([d.sess, d.inst, bucket], sort=False).agg(O=("O", "first"), H=("H", "max"), L=("L", "min"),
                                                              C=("C", "last"), V=("V", "sum"), vwap=("vwap", "last"))
    out = out.reset_index()
    out = out.rename(columns={out.columns[2]: "ts"}).set_index("ts").sort_index(kind="stable")
    out["seg"] = (out.sess.ne(out.sess.shift()) | out.inst.ne(out.inst.shift())).cumsum()
    out["run"] = out.inst.ne(out.inst.shift()).cumsum()
    out["session"] = out["sess"]
    return out


def add_context(b, sym):
    c = sg.context(b, tick=sg.SPEC[sym]["tick"])
    for col in CTX_COLS:
        b[col] = c[col].to_numpy()
    b["trend"] = b["trend"].astype(np.int8)
    return b


def _ffill_rows(a):
    """forward-fill NaNs along axis 1; returns (filled, index of the source column, -1 where none)."""
    n, m = a.shape
    idx = np.where(np.isfinite(a), np.arange(m)[None, :], -1)
    idx = np.maximum.accumulate(idx, axis=1)
    out = np.where(idx >= 0, a[np.arange(n)[:, None], np.maximum(idx, 0)], np.nan)
    return out, idx


def make_sessions(df_all, df, two, sym):
    """sessions table (SESSION_DOC). df_all: kept rows plus the 16:45 minute (for px_1645); df: kept rows."""
    sess_idx, sessions = pd.factorize(df.sess, sort=True)
    ns = len(sessions)
    base = sessions - pd.Timedelta(hours=6)                        # 18:00 of the previous calendar day
    off = ((df.index - base[sess_idx]) // pd.Timedelta(minutes=1)).to_numpy()
    assert off.min() >= 0 and off.max() < SESS_LEN, (off.min(), off.max())
    W = SESS_LEN
    O = np.full((ns, W), np.nan); C = np.full((ns, W), np.nan)
    H = np.full((ns, W), np.nan); L = np.full((ns, W), np.nan); V = np.zeros((ns, W))
    O[sess_idx, off] = df.O.to_numpy(); C[sess_idx, off] = df.C.to_numpy()
    H[sess_idx, off] = df.H.to_numpy(); L[sess_idx, off] = df.L.to_numpy(); V[sess_idx, off] = df.V.to_numpy()
    inst = df.groupby(sess_idx).inst.last().to_numpy()
    # the 16:45 minute's open, same contract
    t1645 = df_all.loc[(df_all.index.hour == 16) & (df_all.index.minute == 45)]
    s1645 = t1645.sess.to_numpy()
    pos = sessions.get_indexer(pd.DatetimeIndex(s1645))
    ok = (pos >= 0)
    ok[ok] &= t1645.inst.to_numpy()[ok] == inst[pos[ok]]
    o1645 = np.full(ns, np.nan)
    o1645[pos[ok]] = t1645.O.to_numpy()[ok]

    has = np.isfinite(O)
    first_t = np.argmax(has, axis=1)
    last_t = W - 1 - np.argmax(has[:, ::-1], axis=1)
    Cf, src = _ffill_rows(C)
    out = pd.DataFrame(index=pd.DatetimeIndex(sessions, name="session"))
    px = {}; age = {}
    for k, name in enumerate(MARKS):
        mm = MARK_STEP * k
        if mm < W:
            p = np.where(has[:, mm], O[:, mm], Cf[:, mm - 1] if mm > 0 else np.nan)
            a = np.where(has[:, mm], 0, mm - (src[:, mm - 1] if mm > 0 else 0))
            live = (mm >= first_t) & (mm <= last_t)
            p = np.where(live, p, np.nan)
        else:                                                      # 16:45
            p = np.where(np.isfinite(o1645), o1645, Cf[:, W - 1])
            a = np.where(np.isfinite(o1645), 0, mm - src[:, W - 1])
        a = np.where(np.isfinite(p), a, -1)
        px[f"px_{name}"] = p
        age[f"age_{name}"] = a.astype(np.int16)
    out = pd.concat([out, pd.DataFrame(px, index=out.index), pd.DataFrame(age, index=out.index)], axis=1)
    out["inst"] = inst
    prev_inst = np.r_[-1, inst[:-1]]
    out["roll"] = (inst != prev_inst) | np.isin(sessions, list(two))
    out.iloc[0, out.columns.get_loc("roll")] = True
    out["first_t"] = first_t.astype(np.int16)
    out["last_t"] = last_t.astype(np.int16)
    out["n_min"] = has.sum(axis=1).astype(np.int16)
    out["first_px"] = O[np.arange(ns), first_t]
    out["open_1800"] = out["px_1800"]
    out["rth_open"] = out["px_0930"]
    rthm = np.zeros(W, bool); rthm[RTH0:RTH1] = True
    onm = np.zeros(W, bool); onm[:RTH0] = True
    c_pre = C[:, :RTH1]
    cpf, _ = _ffill_rows(c_pre)
    has_rth = has[:, RTH0:RTH1].any(axis=1)
    out["close_1600"] = np.where(has_rth, cpf[:, -1], np.nan)
    out["last_px"] = out["px_1645"]
    with np.errstate(all="ignore"):
        for nm, msk in (("", np.ones(W, bool)), ("rth_", rthm), ("on_", onm)):
            Hm = np.where(msk[None, :], H, np.nan); Lm = np.where(msk[None, :], L, np.nan)
            anyb = np.isfinite(Hm).any(axis=1)
            hi = np.nanmax(np.where(anyb[:, None], Hm, 0.0), axis=1)
            lo = np.nanmin(np.where(anyb[:, None], Lm, 0.0), axis=1)
            th = np.argmax(np.where(np.isfinite(Hm), Hm, -np.inf), axis=1)
            tl = np.argmin(np.where(np.isfinite(Lm), Lm, np.inf), axis=1)
            out[f"{nm}high"] = np.where(anyb, hi, np.nan)
            out[f"{nm}low"] = np.where(anyb, lo, np.nan)
            out[f"t_{nm}high"] = np.where(anyb, th, -1).astype(np.int16)
            out[f"t_{nm}low"] = np.where(anyb, tl, -1).astype(np.int16)
        out["volume"] = V.sum(axis=1)
        out["rth_volume"] = V[:, RTH0:RTH1].sum(axis=1)
        lc = np.log(Cf)
        r = np.diff(lc, axis=1)                                     # consecutive-bar log returns (ffilled = 0)
        r = np.where(has[:, 1:] & (src[:, :-1] >= 0), r, 0.0)
        # return of a bar = log(C_bar / previous bar's close)
        out["rv"] = 100 * np.sqrt((r ** 2).sum(axis=1))
        out["rv_rth"] = 100 * np.sqrt((r[:, RTH0 - 1:RTH1 - 1] ** 2).sum(axis=1))
        out["rv_on"] = 100 * np.sqrt((r[:, :RTH0 - 1] ** 2).sum(axis=1))
    same = ~out["roll"].to_numpy()
    lp = out["last_px"].to_numpy()
    prev_lp = np.r_[np.nan, lp[:-1]]
    out["ret_oc"] = lp / out["first_px"].to_numpy() - 1
    out["ret_cc"] = np.where(same, lp / prev_lp - 1, np.nan)
    out["gap"] = np.where(same, out["first_px"].to_numpy() / prev_lp - 1, np.nan)
    out["ret_rth"] = out["close_1600"] / out["rth_open"] - 1
    for c in ("ret_cc", "ret_oc", "ret_rth", "rv", "rv_rth", "volume"):
        out[f"prev_{c}"] = out[c].shift(1)
    for c in ("high", "low", "rth_high", "rth_low", "close_1600", "last_px"):
        out[f"prev_{c}"] = np.where(same, out[c].shift(1), np.nan)
    out["dow"] = out.index.day_of_week.astype(np.int8)
    root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    f = pd.read_csv(os.path.join(root, "data", "fomc_dates.csv"))
    fomc = set(pd.to_datetime(f.loc[f.scheduled, "date"]).dt.normalize())
    nfp = set(pd.to_datetime(pd.read_csv(os.path.join(root, "data", "nfp_dates.csv")).date).dt.normalize())
    cpi = set(pd.to_datetime(pd.read_csv(os.path.join(root, "data", "cpi_dates.csv")).date).dt.normalize())
    sys.path.insert(0, root)
    import calendar_days as cd
    opex = cd.expiry_fridays(out.index)
    out["fomc"] = out.index.isin(list(fomc))
    out["nfp"] = out.index.isin(list(nfp))
    out["cpi"] = out.index.isin(list(cpi))
    out["opex"] = out.index.isin(list(opex))
    out["quad"] = out["opex"] & out.index.month.isin([3, 6, 9, 12])
    out.attrs["doc"] = SESSION_DOC
    return out


def build(sym):
    t0 = time.time()
    raw = raw_1m(sym)
    df, two = filter_1m(raw)
    d1645 = rows_1645(raw)
    del raw
    print(f"{sym}: {len(df):,} kept 1-min rows, {df.sess.nunique()} sessions, {len(two)} two-contract sessions "
          f"({time.time() - t0:.0f}s)", flush=True)
    S = make_sessions(d1645, df, two, sym)
    S.to_parquet(os.path.join(DATA, f"sessions_{sym}.parquet"), compression="zstd")
    print(f"  sessions_{sym}: {S.shape} {S.index[0].date()} .. {S.index[-1].date()} ({time.time() - t0:.0f}s)",
          flush=True)
    for tf in TFS:
        b = add_context(make_bars(df, tf), sym)
        assert (b.index < wf.HOLDOUT_SESSION_START).all()
        tm = b.index.hour * 60 + b.index.minute
        assert not ((tm >= CUT_MIN) & (tm < OPEN_MIN)).any(), "a bar starts in 16:45-18:00"
        b.to_parquet(os.path.join(DATA, f"bars_{sym}_{tf}.parquet"), compression="zstd")
        print(f"  bars_{sym}_{tf}: {b.shape} ({time.time() - t0:.0f}s)", flush=True)
        del b
    del df


if __name__ == "__main__":
    os.makedirs(DATA, exist_ok=True)
    for s in (sys.argv[1:] or ["NQ", "ES", "YM"]):
        build(s)
