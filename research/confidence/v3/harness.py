"""
v3/harness.py - shared test harness for the v3 experiments (time trades, daily P&L, statistics, controls,
family-wise corrections, Lucid eval, trial log). Light: reads only the small v3/data parquet files (no lock needed).

DATA  (built by v3/build_data.py, holdout cut, 16:45-18:00 removed, one contract per session)
  sessions(sym)             v3/data/sessions_{sym}.parquet (one row per Globex session; px_HHMM = executable price at
                            every 15-minute mark 18:00 .. 16:45; see build_data.SESSION_DOC or sessions(sym).attrs)
  bars(sym, tf)             v3/data/bars_{sym}_{tf}.parquet, tf in 5 / 15 / 60 (index = bar START, New York naive;
                            O H L C V vwap ema8 ema20 ema50 mom14 atr14 trend inst sess seg run session)
  calendar(markets)         union of the markets' session dates (the full trading calendar, 0-P&L days included)
  MARKS / mark_index(x) / mark_time(session, k)
                            92 marks: k = 0 is 18:00 (previous evening), k = 62 is 9:30, k = 88 is 16:00,
                            k = 91 is 16:45. x may be an int k, 'HHMM', 'HH:MM' or datetime.time.

TRADES
  time_trades(sym, entries, path_tf=5) -> DataFrame (one row per trade, money per ONE micro)
      entries: DataFrame / list of dicts / list of tuples (session, entry, exit, d[, stop_pts[, target_pts]]).
      Columns of a DataFrame: session (trading day), entry, exit (marks), d (+1 long / -1 short; 'direction' also
      accepted), optional stop_pts / target_pts (distance from the entry price in points; NaN = none). Other columns
      are passed through (e.g. rep, signal name).
      Entry at the entry mark's price (open of that 1-minute bar = executable at the mark), exit at the exit mark's
      price, both from the sessions table. If the market closed early before the exit mark (no bar in the 15
      minutes before it, e.g. a 13:00 holiday close), the exit is the session's last price (px_1645) at the last
      bar's end (exit_kind 'close'). With a stop (and/or target) the
      5-minute bars starting in [entry time, exit time) are walked in order: stop first (long: L <= stop -> fill at
      min(O, stop) - 1 tick; short mirror), then target (limit: needs H >= target + 1 tick, fills at the target).
      Costs: signals.SPEC[sym]['cost'] = $1 commission + 1 tick slippage each way (the stop's extra tick is in its
      fill). Entries are dropped (counted in out.attrs['dropped']) when the session is unknown, the entry price is
      NaN (market not open at that mark: before the first bar, after an early close, or the roll session's first
      hour), or exit <= entry. Output columns: market, session, t_entry, t_exit, d, entry, exit, entry_px, exit_px,
      exit_kind (time / stop / target / close), stop_pts, target_pts, risk_usd (stop distance x $/pt; NaN without
      a stop), pnl_pts (gross points, signed), gross_usd, cost_usd, pnl_usd (NET $ per micro) + pass-through columns.
      The output is a valid v2 eval_sim trade table (market, t_entry, t_exit, risk_usd, pnl_usd, session).

DAILY / STATS
  daily_pnl(trades, calendar=None, col='pnl_usd', micros=None) -> Series over the full calendar (0 on no-trade days)
  stats(x, calendar=None, col='pnl_usd', n_boot=5000, block=5.0, seed=0, top_days=10) -> DataFrame
      x = per-trade DataFrame (unit = trade; t clustered by trading day) or a daily Series (unit = day).
      Rows: all, 2010 ... 2025H1, 2010-17, 2018-25H1, 2018+, 2022+, all w/o top 10 days. Columns: span, n_trades,
      n_days (calendar days in the span), mean (per trade or per day), total, t, sharpe_ann (daily P&L over the
      calendar, mean/sd x sqrt(252)), usd_year, win_pct, p_boot (stationary bootstrap, Politis-Romano, mean block
      `block` days, one-sided H0 mean <= 0; computed for the non-year rows only, NaN for single years).
  boot_p(S, N, ...)         the bootstrap p-value of sum(S)/sum(N) (daily sums S, daily counts N)

CONTROLS
  random_time_trades(sym, entries, n_rep=20, seed=0, keep_session=True, keep_marks=False, keep_side=False,
                     same_length=True) -> time_trades output for n_rep random copies (column rep)
      keep_session False draws a random session of the same calendar year; keep_marks False draws a random entry mark
      with the same holding length in marks (same_length) or random entry < exit; keep_side False draws the side.
      Stops/targets in points are kept.
  drift_trades(sym, entries, keep_stops=True) -> time_trades output: same sessions and marks, always long (paired;
      the paired difference is 0 for a long-only signal)
  hour_drift_trades(sym, entries, n_rep=20, seed=0, keep_stops=True) -> long at the same marks on random sessions
      of the same calendar year (unconditional drift at those hours; column rep)
  control_report(actual, controls, col='pnl_usd') -> DataFrame by window (all, 2010-17, 2018-25H1, 2018+, 2022+):
      actual $/trade, control mean of the per-rep $/trade, its sd, excess = actual - control, p_ctrl = share of reps
      with $/trade >= actual (for drift: n_rep = 1, p_ctrl NaN).

FAMILY CORRECTION
  holm(pvals) -> adjusted p-values (Holm step-down)
  romano_wolf(D, n_boot=5000, block=5.0, seed=0) -> DataFrame per column of D (days x strategies daily P&L on a
      common calendar): mean, t, p_raw (bootstrap), p_rw (Romano-Wolf step-down, studentized max-t, same stationary
      bootstrap days for all strategies), p_holm (Holm on p_raw).

EVAL
  eval(trades, sizing=('fixed', 1), consistencies=(0.40, 0.50), windows=None, calendar=None) -> DataFrame
      v2/eval_sim.evaluate (LucidFlex 25K: $1,250 target, $1,000 EOD trailing DD locking at 25,100, $600 daily
      limit, max 20 micros, start on every trading day). sizing: one policy ('fixed', k) / ('risk', $) or a list.
      ('risk', $) sizes floor($ / risk_usd) micros and needs stop_pts (trades without a stop get 0 micros).
      Daily P&L is per Lucid trading day on the market(s)' full calendar; the $600 limit stops new trades once the
      day's realized loss reaches it and floors the day at -$600.
      Columns: policy, consistency, window, n_starts, pass_pct, bust_pct, open_pct, days_pass_median, within_5,
      within_10, within_20, trades_taken, micros_mean, usd_day_mean, luck_within_10 (best no-edge value, v2 luck bar,
      when the market's row exists).

REPORT / NO LOOK-AHEAD
  standard_report(sym, entries, n_rep=20, seed=0, sizing=None) -> dict(trades, stats, drift, vs_drift,
      excess_vs_drift (stats of the paired per-trade difference vs the same-time long trade), random, vs_random,
      hour_drift, vs_hour_drift, eval)
  truncate(sym, cut_session, cut_mark) -> (S_cut, {tf: bars_cut}) = the data as known at that mark
  lookahead_check(fn, sym, n_cuts=10, seed=0) -> DataFrame; fn(S, B) -> entries (B = {5|15|60: bars}); raises if
      any entry at or before a random cut changes when the data after the cut is removed. Signals must read
      everything through S and B (no other data source), e.g. "long at 9:30 if px_0930 > prev_last_px".

LOG
  log(exp_id, scope, model, trades=None, baseline=None, params=None, note='', **extra) -> run_pipeline.log_trial(
      module='v3-<exp_id>', oos_rows = n trades, oos_usd_per_trade, oos_usd_total, oos_usd_per_year,
      baseline_usd_per_trade, parameters = json(params), note)

USAGE
    import harness as H
    S = H.sessions("ES")
    ent = pd.DataFrame({"session": S.index, "entry": "18:00", "exit": "09:30", "d": 1})       # long overnight MES
    tr = H.time_trades("ES", ent)
    print(H.stats(tr))                                    # $/micro per trade by year/window + bootstrap p
    drift = H.drift_trades("ES", ent); rnd = H.random_time_trades("ES", ent, n_rep=20)
    print(H.control_report(tr, rnd))
    print(H.eval(tr, ("fixed", 5)))
    H.log("demo", "ES", "long 18:00->9:30", trades=tr, params={"entry": "18:00"}, note="usage example")

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 \
      OMP_NUM_THREADS=3 python3 v3/test_harness.py
"""
import datetime as _dt
import json
import os
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SPEC = {"ES": dict(usd=5.0, tick=0.25, micro="MES"), "NQ": dict(usd=2.0, tick=0.25, micro="MNQ"),
        "YM": dict(usd=0.5, tick=1.0, micro="MYM")}
for _s in SPEC.values():
    _s["cost"] = 2 * _s["tick"] * _s["usd"] + 1.0              # = signals.SPEC cost: $1 + 1 tick each way
MARK_STEP = 15
N_MARKS = 92                                                    # 18:00 .. 16:45
MARKS = [f"{(18 * 60 + MARK_STEP * k) // 60 % 24:02d}{(MARK_STEP * k) % 60:02d}" for k in range(N_MARKS)]
_MARK_POS = {m: k for k, m in enumerate(MARKS)}
HOLDOUT_SESSION_START = pd.Timestamp("2025-06-30 18:00")        # = walkforward.HOLDOUT_SESSION_START
LAST_SESSION = pd.Timestamp("2025-06-30")
SPANS = {"2010-17": ("2010-01-01", "2017-12-31"), "2018-25H1": ("2018-01-01", "2025-06-30"),
         "2018+": ("2018-01-01", "2025-06-30"), "2022+": ("2022-01-01", "2025-06-30")}
_CACHE = {}


# ============================================================================================ data
def sessions(sym):
    key = ("S", sym)
    if key not in _CACHE:
        S = pd.read_parquet(os.path.join(DATA, f"sessions_{sym}.parquet"))
        assert S.index.max() <= LAST_SESSION, "sessions file reaches into the holdout"
        _CACHE[key] = S
    return _CACHE[key]


def bars(sym, tf):
    key = ("B", sym, tf)
    if key not in _CACHE:
        b = pd.read_parquet(os.path.join(DATA, f"bars_{sym}_{tf}.parquet"))
        assert b.index.max() < HOLDOUT_SESSION_START, "bars file reaches into the holdout"
        _CACHE[key] = b
    return _CACHE[key]


def calendar(markets=("NQ", "ES", "YM")):
    cal = None
    for s in ([markets] if isinstance(markets, str) else markets):
        c = sessions(s).index
        cal = c if cal is None else cal.union(c)
    return pd.DatetimeIndex(cal, name="session")


def mark_index(x):
    """int k (0..91), 'HHMM', 'HH:MM' or datetime.time -> mark index k (0 = 18:00, 91 = 16:45)."""
    if isinstance(x, (int, np.integer)):
        k = int(x)
    elif isinstance(x, _dt.time):
        k = _MARK_POS.get(f"{x.hour:02d}{x.minute:02d}", -1)
    else:
        k = _MARK_POS.get(str(x).replace(":", "").zfill(4), -1)
    if not 0 <= k < N_MARKS:
        raise ValueError(f"not a 15-minute mark between 18:00 and 16:45: {x!r}")
    return k


def _marks(v):
    v = pd.Series(v)
    if pd.api.types.is_integer_dtype(v):
        k = v.to_numpy(np.int64)
        if ((k < 0) | (k >= N_MARKS)).any():
            raise ValueError("mark index out of range 0..91")
        return k
    return np.array([mark_index(x) for x in v], np.int64)


def mark_time(session, k):
    """wall-clock time of mark k of a session (Timestamp or DatetimeIndex; k scalar or array)."""
    s = pd.DatetimeIndex(np.atleast_1d(session)) if not isinstance(session, pd.Timestamp) else session
    t = s - pd.Timedelta(hours=6) + pd.to_timedelta(np.asarray(k) * MARK_STEP, unit="min")
    return t


# ============================================================================================ trades
def _as_frame(entries):
    if isinstance(entries, pd.DataFrame):
        e = entries.copy()
    else:
        rows = list(entries)
        if rows and not isinstance(rows[0], dict):
            cols = ["session", "entry", "exit", "d", "stop_pts", "target_pts"][:len(rows[0])]
            rows = [dict(zip(cols, r)) for r in rows]
        e = pd.DataFrame(rows)
    if "d" not in e.columns and "direction" in e.columns:
        e = e.rename(columns={"direction": "d"})
    for c in ("session", "entry", "exit", "d"):
        if c not in e.columns:
            raise ValueError(f"entries lack column {c!r}")
    for c in ("stop_pts", "target_pts"):
        if c not in e.columns:
            e[c] = np.nan
    return e.reset_index(drop=True)


def time_trades(sym, entries, path_tf=5):
    """See module docstring. Returns one row per kept entry, net $ per micro (pnl_usd)."""
    sp = SPEC[sym]
    tick, usd, cost = sp["tick"], sp["usd"], sp["cost"]
    e = _as_frame(entries)
    S = sessions(sym)
    n0 = len(e)
    sess = pd.DatetimeIndex(pd.to_datetime(e["session"])).normalize()
    si = S.index.get_indexer(sess)
    ke, kx = _marks(e["entry"]), _marks(e["exit"])
    d = e["d"].to_numpy(np.int64)
    if not np.isin(d, (-1, 1)).all():
        raise ValueError("d must be +1 or -1")
    PX = S[[f"px_{m}" for m in MARKS]].to_numpy(np.float64)
    ok = (si >= 0) & (kx > ke)
    epx = np.full(n0, np.nan); xpx = np.full(n0, np.nan)
    epx[ok] = PX[si[ok], ke[ok]]
    xpx[ok] = PX[si[ok], kx[ok]]
    ok &= np.isfinite(epx)
    reasons = {"unknown_session": int((si < 0).sum()), "exit_not_after_entry": int(((si >= 0) & (kx <= ke)).sum()),
               "no_entry_price": int(((si >= 0) & (kx > ke) & ~np.isfinite(epx)).sum())}
    e = e.loc[ok].reset_index(drop=True)
    si, ke, kx, d, epx, xpx, sess = si[ok], ke[ok], kx[ok], d[ok], epx[ok], xpx[ok], sess[ok]
    n = len(e)
    t_entry = mark_time(sess, ke)
    t_exit_mark = mark_time(sess, kx)
    kind = np.zeros(n, np.int8)                                    # 0 time, 1 stop, 2 target, 3 close
    # early close: exit mark after the last bar -> last price at the end of the last bar
    last_t = S["last_t"].to_numpy(np.int64)[si]
    # market closed before the exit mark: no price at the mark, or (16:45) no bar in the last 15 minutes before it
    closed = ~np.isfinite(xpx) | (MARK_STEP * kx > last_t + MARK_STEP)
    t_exit = np.asarray(t_exit_mark, dtype="datetime64[ns]").copy()
    if closed.any():
        xpx[closed] = S["px_1645"].to_numpy(np.float64)[si[closed]]
        tl = (sess[closed] - pd.Timedelta(hours=6) + pd.to_timedelta(last_t[closed] + 1, unit="min"))
        t_exit[closed] = np.minimum(np.asarray(tl, dtype="datetime64[ns]"), t_exit[closed])
        kind[closed] = 3
    stop_pts = e["stop_pts"].to_numpy(np.float64)
    tgt_pts = e["target_pts"].to_numpy(np.float64)
    walk = np.isfinite(stop_pts) | np.isfinite(tgt_pts)
    if walk.any():
        b = bars(sym, path_tf)
        bt = b.index.to_numpy("datetime64[ns]").view(np.int64)
        O, Hh, Ll = (b[c].to_numpy(np.float64) for c in ("O", "H", "L"))
        bs = b["session"].to_numpy("datetime64[ns]")
        w = np.flatnonzero(walk)
        i0 = np.searchsorted(bt, np.asarray(t_entry, dtype="datetime64[ns]").view(np.int64)[w], "left")
        i1 = np.searchsorted(bt, t_exit[w].view(np.int64), "left")      # bars starting before the exit time
        stop = epx[w] - d[w] * stop_pts[w]
        tgt = epx[w] + d[w] * tgt_pts[w]
        dw = d[w]
        sw = np.asarray(sess[w], dtype="datetime64[ns]")
        act = np.arange(len(w))
        k = 0
        while len(act):
            j = i0[act] + k
            live = j < i1[act]
            act, j = act[live], j[live]
            if not len(act):
                break
            if (bs[j] != sw[act]).any():
                raise AssertionError("5-minute path left the trade's session")
            dd = dw[act]
            s_ = stop[act]; g_ = tgt[act]
            hs = np.where(dd > 0, Ll[j] <= s_, Hh[j] >= s_)                  # NaN stop -> False
            sfill = np.where(dd > 0, np.minimum(O[j], s_) - tick, np.maximum(O[j], s_) + tick)
            ht = ~hs & np.where(dd > 0, Hh[j] >= g_ + tick, Ll[j] <= g_ - tick)
            done = hs | ht
            if done.any():
                a = act[done]
                ww = w[a]
                xpx[ww] = np.where(hs[done], sfill[done], g_[done])
                kind[ww] = np.where(hs[done], 1, 2)
                t_exit[ww] = (bt[j[done]] + np.int64(path_tf) * 60 * 10 ** 9).view("datetime64[ns]")
                t_exit[ww] = np.minimum(t_exit[ww], np.asarray(t_exit_mark, dtype="datetime64[ns]")[ww])
            act = act[~done]
            k += 1
    pnl_pts = d * (xpx - epx)
    out = e.drop(columns=[c for c in ("session", "entry", "exit", "d", "stop_pts", "target_pts") if c in e.columns])
    out.insert(0, "market", sym)
    out.insert(1, "session", sess)
    out.insert(2, "t_entry", pd.DatetimeIndex(t_entry))
    out.insert(3, "t_exit", pd.DatetimeIndex(t_exit))
    out.insert(4, "d", d.astype(np.int8))
    out.insert(5, "entry", np.array(MARKS)[ke])
    out.insert(6, "exit", np.array(MARKS)[kx])
    out["entry_px"] = epx
    out["exit_px"] = xpx
    out["exit_kind"] = np.array(["time", "stop", "target", "close"])[kind]
    out["stop_pts"] = stop_pts
    out["target_pts"] = tgt_pts
    out["risk_usd"] = stop_pts * usd
    out["pnl_pts"] = pnl_pts
    out["gross_usd"] = pnl_pts * usd
    out["cost_usd"] = cost
    out["pnl_usd"] = pnl_pts * usd - cost
    out.attrs["dropped"] = reasons
    if sum(reasons.values()):
        warnings.warn(f"time_trades({sym}): dropped {reasons}", stacklevel=2)
    return out


# ============================================================================================ daily / stats
def daily_pnl(trades, calendar_=None, col="pnl_usd", micros=None):
    """Sum of col (x micros column if given) by session over the full calendar (0 on days without trades)."""
    cal = calendar(sorted(trades["market"].unique())) if calendar_ is None else pd.DatetimeIndex(calendar_)
    v = trades[col].astype(float)
    if micros is not None:
        v = v * trades[micros].astype(float)
    g = v.groupby(pd.DatetimeIndex(trades["session"]).normalize()).sum()
    extra = g.index.difference(cal)
    if len(extra):
        raise ValueError(f"{len(extra)} trade sessions are not in the calendar (e.g. {extra[0].date()})")
    out = g.reindex(cal, fill_value=0.0).astype(float)
    out.index.name = "session"
    return out


def _sb_counts(n, n_boot, block, rng, chunk=500):
    """yield (chunk x n) count matrices of stationary-bootstrap resamples (Politis-Romano: blocks of geometric length
    with mean `block`, random start, circular)."""
    p = 1.0 / float(block)
    done = 0
    ar = np.arange(n)
    while done < n_boot:
        m = min(chunk, n_boot - done)
        new = rng.random((m, n)) < p
        new[:, 0] = True
        starts = rng.integers(0, n, size=(m, n))
        last = np.maximum.accumulate(np.where(new, ar[None, :], 0), axis=1)
        idx = (starts[np.arange(m)[:, None], last] + (ar[None, :] - last)) % n
        flat = (idx + (np.arange(m) * n)[:, None]).ravel()
        yield np.bincount(flat, minlength=m * n).reshape(m, n).astype(np.float64)
        done += m


def boot_p(S, N=None, n_boot=5000, block=5.0, seed=0):
    """One-sided stationary-bootstrap p-value of H0: sum(S)/sum(N) <= 0 (S = daily sums, N = daily counts; N=None ->
    daily series, mean per day). Centered bootstrap: p = (1 + #{m* - m >= m}) / (1 + n_boot)."""
    S = np.asarray(S, np.float64)
    N = np.ones_like(S) if N is None else np.asarray(N, np.float64)
    if N.sum() <= 0 or len(S) < 3:
        return np.nan
    m = S.sum() / N.sum()
    Z = S - m * N
    rng = np.random.default_rng(seed)
    hits = 0
    for W in _sb_counts(len(S), n_boot, block, rng):
        num = W @ Z
        den = W @ N
        st = np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)
        hits += int((st >= m).sum())
    return (1 + hits) / (1 + n_boot)


def _span_masks(days):
    y = days.year
    out = {"all": np.ones(len(days), bool)}
    for yr in range(int(y.min()), int(y.max()) + 1):
        out["2025H1" if yr == 2025 else str(yr)] = np.asarray(y == yr)
    for k, (a, b) in SPANS.items():
        out[k] = np.asarray((days >= pd.Timestamp(a)) & (days <= pd.Timestamp(b)))
    return out


def stats(x, calendar_=None, col="pnl_usd", n_boot=5000, block=5.0, seed=0, top_days=10):
    """See module docstring. x: per-trade DataFrame (with session and col) or a daily Series indexed by session."""
    if isinstance(x, pd.Series):
        daily = x.astype(float)
        days = pd.DatetimeIndex(daily.index)
        S_ = daily.to_numpy(np.float64)
        N_ = np.ones(len(S_))
        unit_trade = False
    else:
        cal = calendar(sorted(x["market"].unique())) if calendar_ is None else pd.DatetimeIndex(calendar_)
        sess = pd.DatetimeIndex(x["session"]).normalize()
        v = x[col].astype(float)
        S_ = v.groupby(sess).sum().reindex(cal, fill_value=0.0).to_numpy(np.float64)
        N_ = v.groupby(sess).size().reindex(cal, fill_value=0).to_numpy(np.float64)
        days = cal
        unit_trade = True
        wins = (v > 0).groupby(sess).sum().reindex(cal, fill_value=0).to_numpy(np.float64)
    masks = _span_masks(days)
    top = np.argsort(-S_, kind="stable")[:top_days]
    wo = np.ones(len(S_), bool); wo[top] = False
    masks[f"all w/o top {top_days} days"] = wo
    rows = []
    for name, m in masks.items():
        Sm, Nm = S_[m], N_[m]
        nt, nd = Nm.sum(), int(m.sum())
        if nt == 0 or nd == 0:
            rows.append(dict(span=name, n_trades=int(nt), n_days=nd))
            continue
        mean = Sm.sum() / nt
        if unit_trade:
            se = np.sqrt(((Sm - mean * Nm) ** 2).sum()) / nt          # clustered by trading day (CR0)
            win = 100 * wins[m].sum() / nt
        else:
            sd = Sm.std(ddof=1) if nd > 1 else np.nan
            se = sd / np.sqrt(nd)
            win = 100 * (Sm > 0).sum() / max((Sm != 0).sum(), 1)
        dsd = Sm.std(ddof=1) if nd > 1 else np.nan
        is_year = name[:4].isdigit() and len(name) in (4, 6)
        rows.append(dict(span=name, n_trades=int(nt), n_days=nd, mean=mean, total=Sm.sum(),
                         t=mean / se if se and se > 0 else np.nan,
                         sharpe_ann=Sm.mean() / dsd * np.sqrt(252) if dsd and dsd > 0 else np.nan,
                         usd_year=Sm.mean() * 252, win_pct=win,
                         p_boot=np.nan if is_year else boot_p(Sm, Nm, n_boot, block, seed)))
    return pd.DataFrame(rows)


# ============================================================================================ controls
def random_time_trades(sym, entries, n_rep=20, seed=0, keep_session=True, keep_marks=False, keep_side=False,
                       same_length=True, path_tf=5):
    """See module docstring. Returns time_trades output of all reps (column rep)."""
    e = _as_frame(entries)
    S = sessions(sym)
    ke, kx = _marks(e["entry"]), _marks(e["exit"])
    sess = pd.DatetimeIndex(pd.to_datetime(e["session"])).normalize()
    rng = np.random.default_rng(seed)
    years = S.index.year.to_numpy()
    by_year = {y: S.index[years == y] for y in np.unique(years)}
    reps = []
    for r in range(n_rep):
        c = e.copy()
        if not keep_session:
            c["session"] = [by_year[y][rng.integers(len(by_year[y]))] if y in by_year else s
                            for y, s in zip(sess.year, sess)]
        if not keep_marks:
            if same_length:
                L = np.maximum(kx - ke, 1)
                ne = rng.integers(0, N_MARKS - L)                 # entry in 0 .. 91 - L
                c["entry"], c["exit"] = ne, ne + L
            else:
                a = rng.integers(0, N_MARKS, size=(len(c), 2))
                a[:, 1] = np.where(a[:, 1] == a[:, 0], (a[:, 0] + 1) % N_MARKS, a[:, 1])
                c["entry"], c["exit"] = a.min(axis=1), a.max(axis=1)
        if not keep_side:
            c["d"] = rng.choice(np.array([-1, 1]), size=len(c))
        c["rep"] = r
        reps.append(c)
    allc = pd.concat(reps, ignore_index=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return time_trades(sym, allc, path_tf=path_tf)


def drift_trades(sym, entries, keep_stops=True, path_tf=5):
    """Same sessions and marks, always long (plain drift); stops/targets kept (keep_stops) or removed."""
    c = _as_frame(entries)
    c["d"] = 1
    if not keep_stops:
        c["stop_pts"] = np.nan; c["target_pts"] = np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return time_trades(sym, c, path_tf=path_tf)


def hour_drift_trades(sym, entries, n_rep=20, seed=0, keep_stops=True, path_tf=5):
    """Unconditional drift at the same hours: each entry re-placed LONG on a random session of the same calendar
    year, same entry/exit marks (and stop/target unless keep_stops=False), n_rep copies (column rep). The control
    for 'is the signal better than just being long at these hours?' (for long-only signals, where the paired
    drift_trades difference is 0 by construction)."""
    c = _as_frame(entries)
    c["d"] = 1
    if not keep_stops:
        c["stop_pts"] = np.nan; c["target_pts"] = np.nan
    return random_time_trades(sym, c, n_rep=n_rep, seed=seed, keep_session=False, keep_marks=True, keep_side=True,
                              path_tf=path_tf)


def control_report(actual, controls, col="pnl_usd"):
    """actual vs control $/trade by window (see module docstring)."""
    rows = []
    sa = pd.DatetimeIndex(actual["session"])
    sc = pd.DatetimeIndex(controls["session"])
    rep = controls["rep"].to_numpy() if "rep" in controls.columns else np.zeros(len(controls), int)
    wins = {"all": ("1900-01-01", "2100-01-01"), **SPANS}
    for w, (a, b) in wins.items():
        ma = (sa >= a) & (sa <= b)
        mc = (sc >= a) & (sc <= b)
        act = actual.loc[ma, col].astype(float).mean() if ma.any() else np.nan
        per = controls.loc[mc, col].astype(float).groupby(rep[mc]).mean() if mc.any() else pd.Series(dtype=float)
        rows.append(dict(window=w, n_actual=int(ma.sum()), actual=act, n_reps=len(per),
                         control=per.mean() if len(per) else np.nan,
                         control_sd=per.std(ddof=1) if len(per) > 1 else np.nan,
                         excess=act - per.mean() if len(per) else np.nan,
                         p_ctrl=(1 + (per >= act).sum()) / (1 + len(per)) if len(per) > 1 else np.nan))
    return pd.DataFrame(rows)


# ============================================================================================ family corrections
def holm(pvals):
    p = np.asarray(pvals, np.float64)
    m = len(p)
    order = np.argsort(p, kind="stable")
    adj = np.empty(m)
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * p[i]))
        adj[i] = run
    return adj


def romano_wolf(D, n_boot=5000, block=5.0, seed=0):
    """Romano-Wolf step-down (one-sided, H0_k: mean_k <= 0) on a days x strategies daily P&L frame (common days)."""
    X = np.asarray(D, np.float64)
    T, K = X.shape
    names = list(D.columns) if isinstance(D, pd.DataFrame) else list(range(K))
    m = X.mean(axis=0)
    sd = X.std(axis=0, ddof=1)
    se = np.where(sd > 0, sd / np.sqrt(T), np.inf)
    t = m / se
    rng = np.random.default_rng(seed)
    Ts = []
    for W in _sb_counts(T, n_boot, block, rng):
        mb = (W @ X) / T
        Ts.append((mb - m[None, :]) / se[None, :])
    Ts = np.vstack(Ts)                                             # n_boot x K centered bootstrap t
    p_raw = (1 + (Ts >= t[None, :]).sum(axis=0)) / (1 + n_boot)
    order = np.argsort(-t, kind="stable")
    Tsort = Ts[:, order]
    revmax = np.maximum.accumulate(Tsort[:, ::-1], axis=1)[:, ::-1]   # max over hypotheses ranked r .. K
    p_step = (1 + (revmax >= t[order][None, :]).sum(axis=0)) / (1 + n_boot)
    p_adj_sorted = np.maximum.accumulate(p_step)
    p_rw = np.empty(K); p_rw[order] = p_adj_sorted
    return pd.DataFrame(dict(strategy=names, mean=m, t=t, p_raw=p_raw, p_rw=p_rw, p_holm=holm(p_raw)))


# ============================================================================================ eval
def _luck_bar():
    p = os.path.join(HERE, "..", "v2", "out", "luck_bar.csv")
    return pd.read_csv(p) if os.path.exists(p) else None


def eval(trades, sizing=("fixed", 1), consistencies=(0.40, 0.50), windows=None, calendar_=None):  # noqa: A001
    """Lucid eval of a trade table via v2/eval_sim.evaluate (see module docstring)."""
    import eval_sim as es
    pols = [sizing] if isinstance(sizing, tuple) else list(sizing)
    cal = calendar(sorted(trades["market"].unique())) if calendar_ is None else pd.DatetimeIndex(calendar_)
    cols = ["market", "t_entry", "t_exit", "risk_usd", "pnl_usd", "session"]
    t = trades[cols].copy()
    t["risk_usd"] = t["risk_usd"].fillna(0.0)
    r = es.evaluate(t, cal, policies=pols, consistencies=consistencies, windows=windows or es.WINDOWS)
    r = r.rename(columns={"fail_pct": "bust_pct"})
    lb = _luck_bar()
    mk = sorted(trades["market"].unique())
    if lb is not None and len(mk) == 1 and (lb.market == mk[0]).any():
        key = lb[lb.market == mk[0]].set_index(["window", "consistency"])
        r["luck_within_10"] = [key["best_within_10"].get((w, c), np.nan) for w, c in zip(r.window, r.consistency)]
        r["luck_pass_pct"] = [key["best_pass_pct"].get((w, c), np.nan) for w, c in zip(r.window, r.consistency)]
    keep = ["policy", "consistency", "window", "n_starts", "pass_pct", "bust_pct", "open_pct", "days_pass_median",
            "within_5", "within_10", "within_20", "trades_taken", "micros_mean", "usd_day_mean",
            "luck_within_10", "luck_pass_pct"]
    return r[[c for c in keep if c in r.columns]]


# ============================================================================================ report / look-ahead
def standard_report(sym, entries, n_rep=20, seed=0, sizing=None, n_boot=5000, path_tf=5):
    """Everything the research rules ask for, for one market and one entry list:
    dict(trades, stats (stats(trades)), drift (drift_trades), vs_drift (control_report vs drift),
         excess_vs_drift (stats of the PAIRED per-trade difference trade - same-time long drift trade),
         random (random_time_trades: same sessions, random marks with the same length, random side),
         vs_random (control_report), hour_drift (hour_drift_trades: long at the same marks on random sessions of
         the same year), vs_hour_drift, eval (eval(trades, sizing) if sizing is given))."""
    tr = time_trades(sym, entries, path_tf=path_tf)
    dr = drift_trades(sym, entries, path_tf=path_tf)
    rd = random_time_trades(sym, entries, n_rep=n_rep, seed=seed, path_tf=path_tf)
    hd = hour_drift_trades(sym, entries, n_rep=n_rep, seed=seed + 1, path_tf=path_tf)
    out = dict(trades=tr, stats=stats(tr, n_boot=n_boot), drift=dr, vs_drift=control_report(tr, dr),
               random=rd, vs_random=control_report(tr, rd), hour_drift=hd, vs_hour_drift=control_report(tr, hd))
    if len(tr) == len(dr) and (tr.t_entry.to_numpy() == dr.t_entry.to_numpy()).all():
        ex = tr[["market", "session"]].copy()
        ex["pnl_usd"] = tr.pnl_usd.to_numpy() - dr.pnl_usd.to_numpy()
        out["excess_vs_drift"] = stats(ex, n_boot=n_boot)
    if sizing is not None:
        out["eval"] = eval(tr, sizing)
    return out


KNOWN_AT_OPEN = ("inst", "roll", "dow", "fomc", "nfp", "cpi", "opex", "quad")


def truncate(sym, cut_session, cut_mark, tfs=(5, 15, 60)):
    """(S_cut, {tf: bars_cut}): the data as it was known at mark `cut_mark` of `cut_session`: later sessions removed;
    in the cut session the marks after the cut and every end-of-session column (high, low, rv, volume, ret_*,
    close_1600, last_px, first_px if not yet traded ...) are NaN (prev_* and the KNOWN_AT_OPEN columns are kept);
    bars kept only if CLOSED by the cut time (start + tf <= cut)."""
    k = mark_index(cut_mark)
    c = pd.Timestamp(cut_session).normalize()
    T = mark_time(c, k)
    S = sessions(sym)
    Sc = S.loc[S.index <= c].copy()
    keep = set(KNOWN_AT_OPEN) | {x for x in Sc.columns if x.startswith("prev_")}
    keep |= {f"px_{m}" for m in MARKS[:k + 1]} | {f"age_{m}" for m in MARKS[:k + 1]}
    for col in Sc.columns:
        if col not in keep:
            if col.startswith("age_") or col in ("first_t", "last_t", "n_min") or col.startswith("t_"):
                Sc.loc[c, col] = -1
            elif Sc[col].dtype == bool:
                Sc.loc[c, col] = False
            else:
                Sc.loc[c, col] = np.nan
    B = {}
    for tf in tfs:
        b = bars(sym, tf)
        B[tf] = b.loc[b.index + pd.Timedelta(minutes=tf) <= T]
    return Sc, B


def lookahead_check(fn, sym, n_cuts=10, seed=0, tfs=(5, 15, 60), start="2012-01-01"):
    """Truncation test for a signal: fn(S, B) -> entries DataFrame (session, entry mark, d, ...) where S is a sessions
    table and B = {tf: bars}. For n_cuts random (session, mark) cut points, entries with entry time <= the cut must
    be IDENTICAL when fn sees only the data known at the cut (truncate()). Returns a DataFrame (one row per cut,
    n_full, n_cut, same) and raises AssertionError on any difference."""
    rng = np.random.default_rng(seed)
    S = sessions(sym)
    full = _as_frame(fn(S, {tf: bars(sym, tf) for tf in tfs}))
    full["_t"] = mark_time(pd.DatetimeIndex(pd.to_datetime(full["session"])).normalize(), _marks(full["entry"]))
    cand = S.index[S.index >= pd.Timestamp(start)]
    rows = []
    for _ in range(n_cuts):
        c = cand[rng.integers(len(cand))]
        k = int(rng.integers(0, N_MARKS))
        T = mark_time(c, k)
        Sc, B = truncate(sym, c, k, tfs)
        cut = _as_frame(fn(Sc, B))
        cut["_t"] = mark_time(pd.DatetimeIndex(pd.to_datetime(cut["session"])).normalize(), _marks(cut["entry"]))
        cols = [x for x in ("session", "entry", "exit", "d", "stop_pts", "target_pts") if x in full.columns]
        a = full.loc[full["_t"] <= T, cols].reset_index(drop=True)
        b = cut.loc[cut["_t"] <= T, cols].reset_index(drop=True)
        a["entry"] = _marks(a["entry"]) if len(a) else a["entry"]
        b["entry"] = _marks(b["entry"]) if len(b) else b["entry"]
        same = len(a) == len(b) and a.astype(str).equals(b.astype(str))
        rows.append(dict(cut_session=c.date(), cut_mark=MARKS[k], n_full=len(a), n_cut=len(b), same=same))
    r = pd.DataFrame(rows)
    if not r.same.all():
        raise AssertionError(f"look-ahead: entries change when the future is removed\n{r[~r.same]}")
    return r


# ============================================================================================ log
def log(exp_id, scope, model, trades=None, baseline=None, params=None, note="", **extra):
    """Append one configuration to out/trials.csv via run_pipeline.log_trial(module='v3-<exp_id>').
    trades / baseline: per-trade frames (pnl_usd) or floats ($/trade)."""
    import run_pipeline as rp
    row = dict(module=f"v3-{exp_id}", scope=scope, model=model, note=note)
    if isinstance(trades, pd.DataFrame) and len(trades):
        s = pd.DatetimeIndex(trades["session"])
        yrs = max((s.max() - s.min()).days / 365.25, 1 / 252)
        row.update(oos_rows=len(trades), oos_usd_per_trade=round(float(trades["pnl_usd"].mean()), 4),
                   oos_usd_total=round(float(trades["pnl_usd"].sum()), 2),
                   oos_usd_per_year=round(float(trades["pnl_usd"].sum()) / yrs, 2))
    elif trades is not None and np.isscalar(trades):
        row.update(oos_usd_per_trade=float(trades))
    if isinstance(baseline, pd.DataFrame) and len(baseline):
        row["baseline_usd_per_trade"] = round(float(baseline["pnl_usd"].mean()), 4)
    elif baseline is not None and np.isscalar(baseline):
        row["baseline_usd_per_trade"] = float(baseline)
    row["parameters"] = json.dumps(params or {}, default=str)
    row.update(extra)
    rp.log_trial(**row)
