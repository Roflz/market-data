"""
Paper-trading (forward-test) log for the three live MNQ models and two forward-test leads, 1 micro per trade.
Each run looks at the data already in data/ (it never downloads anything), finds every cash session not yet in the
log, works out what each model and lead did or would have done that day, and appends one row per session per
model/lead to paper_log.csv (overnight_break gets one row per trade on the rare days it trades twice, after a
stop-out). Re-running never duplicates a row: a (date, model_or_lead) pair already in the log is never redone.

Live models (kind = live): computed by chosen_models.py's own functions, so the log matches its backtest exactly
  overnight_break   first 5-min close beyond the overnight high/low with the 20-day trend, 9:35-15:00, stop
                    2 x ATR(5-min), hold to the 5 PM close
  opening_range     first 5-minute candle direction at 9:35, stop at the candle's other end, exit at the 15:59 close
  expiry_fade       monthly options-expiry day: short at the 9:30 open, cover at the 15:59 close, no stop
  Skip rules, in chosen_models.py's order: expiry Friday (only expiry_fade trades), then R1 (no breakout trade the
  day after the S&P 500 fell 2% or more), then R2 (no opening_range trade on a scheduled Fed statement day).
  A skipped row (signal = skipped) shows the trade the rule removed; its P&L is NOT part of the model's result.
Leads (kind = lead): being forward-tested, NOT live models; never trade them for real on this log alone
  lead_calm_lasthalfhour_fade   variant F1 of the last-half-hour study (lit_p2_lasthalfhour.py and its summary,
                    volatility breakdown; tested in p2_regime.py): on calm days only (trailing 20-day 5-min realised
                    volatility in the bottom third of all earlier days, 250-session burn-in), take the OPPOSITE side
                    of sign(prior close -> 15:29 close) at the 15:30 open, exit at the 15:59 close. NQ 2020-06..2026-11:
                    136 trades, +$10.91 per trade, t 1.45. Day calendar, signal and exclusions come from
                    lit_p2_lasthalfhour.prepare() unchanged.
  lead_cpi_jobs_fade   CPI days (calendar_days.cpi_days) and jobs-report days (data/nfp_dates.csv, official BLS dates;
                    first-Friday proxy only for dates past the end of that list, flagged in the note), each day once:
                    move = 8:44 bar close - 8:30 bar open (only bars closed before 8:45); if nonzero, enter the
                    opposite way at the 8:45 bar open, exit at the 9:45 bar open, no stop (the pre-registered primary,
                    section 13 'strict' build). Skipped if a bar at 8:30, 8:44, 8:45 or 9:45 is missing, the
                    contract changes inside 8:30-9:45, or there is a gap of more than 5 minutes.
Costs: 1 tick slippage each way + $1.00 commission per round trip = 1.0 NQ point = $2.00 per MNQ.
Columns: date, model_or_lead, kind (live/lead), signal (long/short/none/skipped), skip_rule, entry_time, entry_px,
  stop_px, exit_time, exit_px, exit_reason, net_pts, net_usd (1 micro), net_bp, logged_at, note.
  Times are New York time. Prices are raw (unadjusted) contract prices and are FILL prices (1 tick slippage
  included). exit_time is the bar close for time/close exits and the start of the bar in which a stop filled.
  net_pts/net_usd are after all costs; net_bp = 1e4 x net points / raw entry price (chosen_models.py's bp for the
  live models).
A session is logged for a model only when every input it needs covers that day; otherwise it is held back (and
listed) until the inputs are refreshed, so a row, once written, is final:
  NQ 1-minute bars with the full Globex session; daily_sessions_NQ.pkl (cash-day calendar); market_context.pkl (R1);
  fomc_dates.csv (R2 and the overnight-break Fed blackout); x5_NQ.pkl + fut_features_NQ.pkl (overnight_break);
  cpi_dates.csv (lead_cpi_jobs_fade); and the latest session waits a day when it could still turn out to be an
  options-expiry day (third Friday a holiday).
Report: per model/lead trades and net $, skipped trades, and for the live models the difference from
chosen_models_trades.csv on overlapping dates (must be $0 and 0 mismatches; rerun chosen_models.py to extend it).

Data refresh is done by you (this script never downloads):
  PYTHONPATH=./pylib python3 refresh_data.py     (new bars only: about half a cent a day of Databento credit; the
  free Yahoo daily files; then rebuilds everything and runs this script). Do NOT use 'fetch_databento.py ohlcv'
  for a refresh: it re-downloads 2010-now (about $41).
Usage:  PYTHONPATH=./pylib python3 paper_log.py [--since 2026-11-09] [--last N] [--out paper_log.csv] [--report-only]
        --since  first session to log (default 2026-11-09, the forward-test start); earlier = backfill for checking
        --last   only the last N cash sessions on or after --since
        --out    log file (default paper_log.csv in the project folder)
"""
import argparse
import contextlib
import gc
import io
import os
import sys
import warnings

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

warnings.filterwarnings("ignore")
FORWARD_START = "2026-11-09"
DEFAULT_LOG = os.path.join(BASE, "paper_log.csv")
SYM = "NQ"
TICK = 0.25
USD_PT = 2.0                                   # MNQ $ per point
COMM_PTS = 1.00 / USD_PT                       # $1.00 commission per round trip, in points
LIVE = ["overnight_break", "opening_range", "expiry_fade"]
CALM = "lead_calm_lasthalfhour_fade"
L1 = "lead_cpi_jobs_fade"
LEADS = [CALM, L1]
COLUMNS = ["date", "model_or_lead", "kind", "signal", "skip_rule", "entry_time", "entry_px", "stop_px", "exit_time",
           "exit_px", "exit_reason", "net_pts", "net_usd", "net_bp", "logged_at", "note"]
SKIP_EXPIRY = "expiry Friday (only expiry_fade trades)"
SKIP_R1 = "R1 after S&P -2%"
SKIP_R2 = "R2 Fed day"
T0830, T0844, T0845, T0945 = 510, 524, 525, 585     # minutes after midnight, New York time
L1_MAX_GAP = 5
REFRESH = "PYTHONPATH=./pylib python3 refresh_data.py"


@contextlib.contextmanager
def quiet():
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def hhmm(minute):
    return f"{int(minute) // 60:02d}:{int(minute) % 60:02d}"


def fmt_px(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 2)


def row(date, name, signal, note="", skip_rule="", **kw):
    r = dict.fromkeys(COLUMNS)
    r.update(date=pd.Timestamp(date).strftime("%Y-%m-%d"), model_or_lead=name,
             kind="live" if name in LIVE else "lead", signal=signal, skip_rule=skip_rule, note=note)
    r.update(kw)
    return r


def trade_fields(entry_time, entry_px, stop_px, exit_time, exit_px, exit_reason, net_pts, net_bp):
    return dict(entry_time=entry_time, entry_px=fmt_px(entry_px), stop_px=fmt_px(stop_px), exit_time=exit_time,
                exit_px=fmt_px(exit_px), exit_reason=exit_reason, net_pts=round(float(net_pts), 4),
                net_usd=round(float(net_pts) * USD_PT, 4), net_bp=round(float(net_bp), 6))


# ----------------------------------------------------------------------------------------------------------------
# What the data covers (cheap checks first; nothing heavy is loaded unless there is work to do)
# ----------------------------------------------------------------------------------------------------------------
def last_csv_bar(path):
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        f.seek(max(0, f.tell() - 4096))
        line = f.read().decode().strip().splitlines()[-1]
    return pd.Timestamp(line.split(",")[0]).tz_convert("America/New_York")


def coverage():
    """Last date each input covers. Session date = Globex session (bars from 6 PM the evening before)."""
    last = last_csv_bar(f"data/{SYM}_fut_1m.csv")
    sess = (last + pd.Timedelta(hours=6)).normalize().tz_localize(None)
    complete = sess if last.hour * 60 + last.minute >= 16 * 60 + 55 else sess - pd.Timedelta(days=1)
    ds = pd.read_pickle(f"data/daily_sessions_{SYM}.pkl")
    ctx = pd.read_pickle("data/market_context.pkl")[["spx_ret_1d_prev"]]
    fomc = pd.to_datetime(pd.read_csv("data/fomc_dates.csv").date)
    cpi = pd.to_datetime(pd.read_csv("data/cpi_dates.csv").date)
    return dict(last_bar=last, bars=complete, ds=ds.index.max(), ctx=ctx.spx_ret_1d_prev.dropna().index.max(),
                fomc=fomc.max(), cpi=cpi.max(), ds_frame=ds,
                mtime={k: os.path.getmtime(p) for k, p in [
                    ("csv", f"data/{SYM}_fut_1m.csv"), ("daily_sessions.py", f"data/daily_sessions_{SYM}.pkl"),
                    ("exits_data.py", f"data/x5_{SYM}.pkl"), ("fut_build.py", f"data/fut_features_{SYM}.pkl"),
                    ("market_context.py", "data/market_context.pkl")]})


def nfp_days():
    """Official jobs-report dates from data/nfp_dates.csv; (set, last date, source)."""
    p = "data/nfp_dates.csv"
    if os.path.exists(p):
        f = pd.read_csv(p)
        return set(pd.to_datetime(f.date)), pd.to_datetime(f.date).max(), str(f.source.iloc[-1])
    return set(), pd.Timestamp("1900-01-01"), "none (data/nfp_dates.csv missing: first-Friday proxy for every date)"


def first_friday_proxy(day, trading_days):
    """Spec's proxy: the first Friday of the month that is a trading day."""
    first = pd.Timestamp(day.year, day.month, 1)
    fri = [first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 7 * k) for k in range(5)]
    for f in fri:
        if f.month == day.month and f in trading_days:
            return day == f
    return False


def third_friday(day):
    first = pd.Timestamp(day.year, day.month, 1)
    return first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)


# ----------------------------------------------------------------------------------------------------------------
# Live models: chosen_models.py's functions, plus the entry/stop/exit details of each trade
# ----------------------------------------------------------------------------------------------------------------
def live_rows(days, cash_days, ds):
    import calendar_days as cd
    import chosen_models as cm
    import exits_compare as ec
    import exits_engine as ee
    import lit_p5_orb as p5

    expiry = cd.expiry_fridays(cash_days)
    after_drop, fed = cm.skip_days()
    with quiet():
        dates, g, inst = p5.load_market(SYM)
        sess, Cff, _ = p5.build_sessions(SYM, dates, g, inst)
    sess = sess[sess.date.isin(cash_days)]

    # the official functions; the *_all versions ignore the expiry-Friday rule so skipped trades can be shown
    orb_off, orb_all = cm.opening_range(expiry, sess, g, Cff), cm.opening_range(set(), sess, g, Cff)
    exf = cm.expiry_fade(expiry, sess, g, Cff)
    onb_off, onb_all = cm.overnight_break(expiry, cash_days, ds), cm.overnight_break(set(), cash_days, ds)
    for off, al in [(orb_off, orb_all), (onb_off, onb_all)]:          # the *_all trick must not change anything
        chk = al[~al.date.isin(expiry)].reset_index(drop=True)
        assert chk.equals(off.reset_index(drop=True)), "expiry-Friday filtering is not post-hoc"
    orb_all, onb_all, exf = (x.set_index("date") for x in (orb_all, onb_all, exf))

    # overnight_break details: rerun the same engine call chosen_models.overnight_break makes
    D, sp = ec.G[SYM], ee.SPEC[SYM]
    t = ee.run(D, ec.G[("sets", SYM)]["Overnight break + daily trend"], "hold", k0=2.0)
    t["date"] = pd.to_datetime(D.sess[t.bar.to_numpy()])
    adj = (ds.close_adj - ds.close_raw)
    onb_det = {}
    for r in t.itertuples(index=False):
        if r.date not in days:
            continue
        i, d = int(r.bar), int(r.dir)
        e, x = i + 1, i + int(r.hold_bars)
        a = float(adj.get(r.date, np.nan))
        entry = D.Open[e] + d * ee.SLIP
        stop = ee.snap_stop(entry - d * r.R_pts, d)
        xt = D.idx[x] if r.exit == "stop" else D.idx[x] + pd.Timedelta(minutes=5)
        onb_det.setdefault(r.date, []).append(dict(entry_time=D.idx[e].strftime("%H:%M"), entry_px=entry - a, stop_px=stop - a,
                               exit_time=xt.strftime("%H:%M"), exit_px=entry + d * r.pts - a, exit_reason=r.exit,
                               net_pts_chk=r.pts - sp["comm"] / sp["usd"],
                               signal_time=(D.idx[i] + pd.Timedelta(minutes=5)).strftime("%H:%M")))

    ppt, min_R, K = p5.MARKETS[SYM]["ppt"], p5.MARKETS[SYM]["min_R"], cm.K
    O, H, L = g["Open"], g["High"], g["Low"]

    def orb_detail(r):
        """Same steps as chosen_models.opening_range for one session, keeping the prices and the no-trade reason."""
        i = r.di
        if np.isnan(O[i, 0]) or np.isnan(O[i, K]):
            return None, "no 9:30 or 9:35 bar"
        oc, cc = O[i, 0], Cff[i, K - 1]
        if cc == oc:
            return None, "first 5-minute candle closed where it opened (no direction)"
        d = 1 if cc > oc else -1
        stop = np.nanmin(L[i, :K]) if d > 0 else np.nanmax(H[i, :K])
        risk = d * (cc + d * p5.TICK - stop)
        if risk < min_R:
            return None, f"candle too small: risk {risk:.2f} pts < {min_R} pt cost filter"
        ref, fill = O[i, K], O[i, K] + d * p5.TICK
        s_x = r.exit_slot
        if d * (fill - stop) <= 0:
            xs, xfill, why, note = K, ref - d * p5.TICK, "stop", "opened through the stop: out at once"
        else:
            xs, _, xfill, why = p5.run_trade(H[i], L[i], O[i], Cff[i, s_x], K, s_x, d, stop, None, True)
            note = ""
        net = d * (xfill - fill) - p5.COMM / ppt
        xt = 570 + xs if why == "stop" else 570 + s_x + 1
        return dict(side="long" if d > 0 else "short", entry_time="09:35", entry_px=fill, stop_px=stop,
                    exit_time=hhmm(xt), exit_px=xfill, exit_reason=why, net_pts=net, bp=1e4 * net / ref), note

    sess_by_date = sess.set_index("date")
    rows = []
    for day in sorted(days):
        is_exp = day in expiry
        # ---------------- overnight_break
        if day in onb_all.index:                 # up to 3 trades a day: after a stop-out a later signal can trade
            trs, dets = onb_all.loc[[day]], onb_det[day]
            assert len(trs) == len(dets)
            for k, (tr, det) in enumerate(zip(trs.itertuples(index=False), dets)):
                net = tr.usd / USD_PT
                assert abs(net - det["net_pts_chk"]) < 1e-9
                f = trade_fields(det["entry_time"], det["entry_px"], det["stop_px"], det["exit_time"],
                                 det["exit_px"], tr.exit, net, tr.bp)
                note = (f"trade {k + 1} of {len(trs)} today; " if len(trs) > 1 else "") + \
                    f"signal: 5-min close at {det['signal_time']}; R = {tr.R:+.2f}"
                rule = SKIP_EXPIRY if is_exp else (SKIP_R1 if day in after_drop else "")
                rows.append(row(day, "overnight_break", "skipped" if rule else tr.side, note, rule, **f))
        else:
            rows.append(row(day, "overnight_break", "none",
                            "no fresh 5-min close beyond the overnight high/low in the 20-day trend direction "
                            "9:35-15:00" + (" (expiry Friday: model off anyway)" if is_exp else "")))
        # ---------------- opening_range
        r = sess_by_date.loc[day] if day in sess_by_date.index else None
        det, why_none = (orb_detail(r) if r is not None else (None, "no RTH session in the ORB calendar"))
        if det is not None:
            tr = orb_all.loc[day]
            assert tr.side == det["side"] and abs(tr.usd - det["net_pts"] * USD_PT) < 1e-9
            f = trade_fields(det["entry_time"], det["entry_px"], det["stop_px"], det["exit_time"], det["exit_px"],
                             tr.exit, tr.usd / USD_PT, tr.bp)
            rule = SKIP_EXPIRY if is_exp else (SKIP_R1 if day in after_drop else (SKIP_R2 if day in fed else ""))
            note = f"R = {tr.R:+.2f}" + (f"; {why_none}" if why_none else "")
            rows.append(row(day, "opening_range", "skipped" if rule else tr.side, note, rule, **f))
        else:
            assert day not in orb_all.index
            rows.append(row(day, "opening_range", "none", why_none + (" (expiry Friday: model off anyway)"
                                                                      if is_exp else "")))
        # ---------------- expiry_fade
        if is_exp and day in exf.index:
            tr = exf.loc[day]
            ent = O[r.di, 0]
            xs = min(p5.FULL_EXIT_SLOT, r.exit_slot)
            ext = Cff[r.di, xs]
            f = trade_fields("09:30", ent - p5.TICK, None, hhmm(570 + xs + 1), ext + p5.TICK, tr.exit,
                             tr.usd / USD_PT, tr.bp)
            rows.append(row(day, "expiry_fade", tr.side, "monthly options-expiry day", **f))
        else:
            rows.append(row(day, "expiry_fade", "none", "missing 9:30 or closing bar on expiry day" if is_exp
                            else "not an options-expiry day"))
    ec.G.clear()
    return rows


# ----------------------------------------------------------------------------------------------------------------
# Lead 1: calm-day last-half-hour fade (variant F1), from lit_p2_lasthalfhour.prepare()
# ----------------------------------------------------------------------------------------------------------------
def calm_rows(days):
    import lit_p2_lasthalfhour as p2
    fomc_df = pd.read_csv("data/fomc_dates.csv")
    fomc_sched = pd.DatetimeIndex(pd.to_datetime(fomc_df.loc[fomc_df.scheduled, "date"]))
    cpi = pd.DatetimeIndex(pd.to_datetime(pd.read_csv("data/cpi_dates.csv")["date"]))
    log = []
    raw = p2.load_market(SYM, log)
    s, _, _ = p2.prepare(SYM, raw, log, fomc_sched, cpi, np.random.default_rng(p2.SEED))
    del raw
    s = s.set_index("date")
    rows = []
    for day in sorted(days):
        if day not in s.index:
            rows.append(row(day, CALM, "none", "not a session in the study's calendar"))
            continue
        r = s.loc[day]
        why = ("early-close day" if r.early else "first day after a roll (no same-contract prior close)"
               if r.roll_skip else "abnormal RTH gap (> 10 missing minutes)" if r.abnormal
               else "more than one contract inside RTH" if r.multi else "no prior session" if r.no_prior
               else "missing price or zero signal" if not r.base else "")
        if not why:
            if np.isnan(r.vol_terc):
                why = "volatility tercile not defined yet (burn-in)"
            elif r.vol_terc != 1:
                why = f"not a calm day (volatility tercile {int(r.vol_terc)} of 3; trades only in tercile 1)"
        sig_note = f"prior close -> 15:29 = {1e4 * r.sig:+.1f} bp" if np.isfinite(r.sig) else ""
        if why:
            rows.append(row(day, CALM, "none", "; ".join(x for x in [why, sig_note] if x)))
            continue
        f = -int(r.side)                                                     # fade = opposite of the momentum side
        entry, exit_ = r.e_ref + f * TICK, r.x_ref - f * TICK
        net = f * (exit_ - entry) - COMM_PTS
        rows.append(row(day, CALM, "long" if f > 0 else "short", f"calm day (vol tercile 1); {sig_note}, faded",
                        **trade_fields("15:30", entry, None, "16:00", exit_, "close", net, 1e4 * net / r.e_ref)))
    return rows


# ----------------------------------------------------------------------------------------------------------------
# Lead 2: CPI / jobs-report 8:30 fade (section 13 L1, strict signal, time exit)
# ----------------------------------------------------------------------------------------------------------------
def load_window(days):
    lo = (min(days) - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
    parts = []
    for ch in pd.read_csv(f"data/{SYM}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close",
                                                               "instrument_id"],
                          dtype={"ts_event": str}, chunksize=1_000_000):
        ch = ch[ch.ts_event.str.slice(0, 10) >= lo]
        if ch.empty:
            continue
        ts = pd.to_datetime(ch.ts_event, utc=True).dt.tz_convert("America/New_York")
        tmin = (ts.dt.hour * 60 + ts.dt.minute).to_numpy()
        keep = (tmin >= T0830) & (tmin <= T0945)
        ch = ch[keep].copy()
        ch["date"] = ts[keep].dt.tz_localize(None).dt.normalize().to_numpy()
        ch["tmin"] = tmin[keep]
        parts.append(ch.drop(columns="ts_event"))
    w = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["date", "tmin"])
    return {d: x.sort_values("tmin") for d, x in w.groupby("date")}


def l1_rows(days, release):
    bars = load_window(days)
    rows = []
    for day in sorted(days):
        kinds = release[day]
        if not kinds:
            rows.append(row(day, L1, "none", "not a CPI or jobs-report day"))
            continue
        tag = " + ".join(kinds)
        w = bars.get(day)
        t = set(w.tmin) if w is not None else set()
        why = ("no 8:30-9:45 bars" if w is None or w.empty
               else "8:30 bar missing" if T0830 not in t else "8:44 bar missing" if T0844 not in t
               else "8:45 bar missing" if T0845 not in t else "9:45 bar missing" if T0945 not in t
               else "contract roll inside 8:30-9:45" if w.instrument_id.nunique() != 1
               else "gap > 5 min inside 8:30-9:45" if np.diff(w.tmin.to_numpy()).max() > L1_MAX_GAP else "")
        if why:
            rows.append(row(day, L1, "none", f"{tag} day; skipped: {why}"))
            continue
        b = w.set_index("tmin")
        o830, c844 = b.loc[T0830, "Open"], b.loc[T0844, "Close"]
        move = c844 - o830
        if move == 0:
            rows.append(row(day, L1, "none", f"{tag} day; 8:30-8:45 move was zero"))
            continue
        pos = -1 if move > 0 else 1
        ref, xref = b.loc[T0845, "Open"], b.loc[T0945, "Open"]
        entry, exit_ = ref + pos * TICK, xref - pos * TICK
        net = pos * (exit_ - entry) - COMM_PTS
        rows.append(row(day, L1, "long" if pos > 0 else "short", f"{tag} day; 8:30-8:45 move {move:+.2f} pts, faded",
                        **trade_fields("08:45", entry, None, "09:45", exit_, "time", net, 1e4 * net / ref)))
    return rows


# ----------------------------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------------------------
def report(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print(f"\nLog {path}: empty (forward test starts {FORWARD_START}).")
        return
    lg = pd.read_csv(path, parse_dates=["date"])
    print(f"\nLOG SO FAR  {path}: {lg.date.nunique()} sessions, {lg.date.min():%Y-%m-%d} -> {lg.date.max():%Y-%m-%d}"
          f"  (MNQ, 1 micro, after $2.00 round-trip cost)")
    print(f"  {'model / lead':30s} {'kind':5s} {'days':>5s} {'trades':>6s} {'won':>4s} {'net $':>9s} {'$/trade':>8s}"
          f" {'skipped':>7s} {'skipped would have made':>24s}")
    for name in LIVE + LEADS:
        g = lg[lg.model_or_lead == name]
        if g.empty:
            continue
        tr = g[g.signal.isin(["long", "short"])]
        sk = g[g.signal == "skipped"]
        avg = f"{tr.net_usd.mean():8.2f}" if len(tr) else f"{'-':>8s}"
        print(f"  {name:30s} {g.kind.iloc[0]:5s} {g.date.nunique():5d} {len(tr):6d} {int((tr.net_usd > 0).sum()):4d} "
              f"{tr.net_usd.sum():9.2f} {avg} {len(sk):7d} {sk.net_usd.sum():24.2f}")
    live = lg[(lg.kind == "live") & lg.signal.isin(["long", "short"])]
    print(f"  all 3 live models together: {len(live)} trades, net ${live.net_usd.sum():,.2f}")

    ref = pd.read_csv(os.path.join(BASE, "chosen_models_trades.csv"), parse_dates=["date"])
    skp = os.path.join(BASE, "chosen_models_skipped.csv")
    cmax = max(ref.date.max(), pd.read_csv(skp, parse_dates=["date"]).date.max() if os.path.exists(skp) else ref.date.min())
    print(f"\nCHECK against chosen_models_trades.csv (its last trade or skipped trade: {cmax:%Y-%m-%d}; "
          f"rerun chosen_models.py to extend it)")
    for name in LIVE:
        g = lg[(lg.model_or_lead == name) & (lg.date <= cmax)]
        if g.empty:
            print(f"  {name:16s} no overlapping dates")
            continue
        a = g[g.signal.isin(["long", "short"])]
        b = ref[(ref.model == name) & ref.date.isin(g.date)]
        ka = {d: sorted(zip(x.signal, x.exit_reason, x.net_usd, x.net_bp)) for d, x in a.groupby("date")}
        kb = {d: sorted(zip(x.side, x.exit, x.usd, x.bp)) for d, x in b.groupby("date")}
        both = set(ka) & set(kb)
        only = len(set(ka) ^ set(kb))
        bad = sum(1 for d in both if len(ka[d]) != len(kb[d]) or any(
            p[0] != q[0] or p[1] != q[1] or abs(p[2] - q[2]) > 1e-6 or abs(p[3] - q[3]) > 1e-4
            for p, q in zip(ka[d], kb[d])))
        diff = a.net_usd.sum() - b.usd.sum()
        ok = "OK" if (only == 0 and bad == 0 and abs(diff) < 1e-6) else "MISMATCH"
        print(f"  {name:16s} {g.date.nunique():4d} overlapping dates, log trades {len(a):3d}, backtest trades {len(b):3d},"
              f" on one side only {only}, field mismatches {bad}, $ difference {diff:+.2f}  {ok}")
        if os.path.exists(skp) and name != "expiry_fade":          # R1/R2 skips vs chosen_models_skipped.csv
            sa = g[(g.signal == "skipped") & g.skip_rule.isin([SKIP_R1, SKIP_R2])]
            sb = pd.read_csv(skp, parse_dates=["date"])
            sb = sb[(sb.model == name) & sb.date.isin(g.date)]
            same = sorted(zip(sa.date, sa.skip_rule, sa.net_usd)) == sorted(zip(sb.date, sb.skip_rule, sb.usd))
            print(f"  {'':16s} R1/R2-skipped trades: log {len(sa)}, chosen_models_skipped.csv {len(sb)}  "
                  f"{'OK' if same else 'MISMATCH'}")


def preview(cov, nfp, nfp_last, cash_days):
    """What is already known about the next session (pre-open rules)."""
    last = cash_days.max()
    nxt = last + pd.offsets.BDay(1)
    fomc = set(pd.to_datetime(pd.read_csv("data/fomc_dates.csv").query("scheduled").date))
    cpi = set(pd.to_datetime(pd.read_csv("data/cpi_dates.csv").date))
    bits = []
    if nxt == third_friday(nxt):
        bits.append("third Friday = options expiry: only expiry_fade trades (unless an exchange holiday)")
    if nxt > cov["fomc"]:
        bits.append(f"Fed calendar ends {cov['fomc']:%Y-%m-%d}: add the next meetings to data/fomc_dates.csv")
    elif nxt in fomc:
        bits.append("scheduled Fed statement day: opening_range skips (R2)")
    if nxt in cpi:
        bits.append("CPI day: lead_cpi_jobs_fade active")
    elif nxt > cov["cpi"]:
        bits.append(f"CPI calendar ends {cov['cpi']:%Y-%m-%d}: add upcoming CPI dates to data/cpi_dates.csv")
    if nxt in nfp or (nxt > nfp_last and first_friday_proxy(nxt, set(cash_days) | {nxt})):
        bits.append("jobs-report day: lead_cpi_jobs_fade active" + (" (first-Friday proxy)" if nxt > nfp_last else ""))
    try:
        spx = pd.read_csv("data/yahoo_daily/SP500_index.csv", parse_dates=["Date"]).set_index("Date").Close
        spx = spx[spx.index.normalize() <= last]      # R1 for the next session = S&P change ON `last`, not a later row
        if len(spx) >= 2 and spx.index.max().normalize() == last:
            ch = 100 * (spx.iloc[-1] / spx.iloc[-2] - 1)
            bits.append(f"S&P 500 last close {ch:+.2f}%: " + ("R1 ON, no breakout trades" if ch <= -2.0 else "R1 off"))
        else:
            bits.append("S&P 500 daily file not current: R1 status unknown")
    except Exception:
        bits.append("S&P 500 daily file unreadable: R1 status unknown")
    print(f"\nNEXT SESSION {nxt:%a %Y-%m-%d} (known before the open): " + "; ".join(bits))


# ----------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Append forward-test rows for the live MNQ models and leads.")
    ap.add_argument("--since", default=FORWARD_START)
    ap.add_argument("--last", type=int, default=None)
    ap.add_argument("--out", default=DEFAULT_LOG)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    os.chdir(BASE)
    since = pd.Timestamp(a.since)

    cov = coverage()
    ds = cov.pop("ds_frame")
    cash_days = ds.index[ds.cash_day]
    print(f"PAPER LOG  data: {SYM} 1-min bars to {cov['last_bar']:%Y-%m-%d %H:%M} ET. Nothing is downloaded here; "
          f"refresh it yourself with:\n  {REFRESH}\n  (new bars only, about half a cent a day; it also updates the "
          f"Yahoo daily files, rebuilds everything and runs this log)")
    stale = [k for k, m in cov["mtime"].items() if k != "csv" and m < cov["mtime"]["csv"]]
    if stale:
        print("  NOTE: built before the latest 1-min download, rerun: " + ", ".join(stale))
    nfp, nfp_last, nfp_src = nfp_days()

    done = set()
    if os.path.exists(out) and os.path.getsize(out) > 0:
        old = pd.read_csv(out, usecols=["date", "model_or_lead"])
        done = set(zip(old.date.astype(str), old.model_or_lead))

    days = cash_days[cash_days >= since]
    if a.last:
        days = days[-a.last:]
    names = LIVE + LEADS
    todo = {n: [d for d in days if (d.strftime("%Y-%m-%d"), n) not in done] for n in names}

    # readiness: every input a model needs must cover the day
    exp_pending = set()
    lastday = cash_days.max()
    tf = third_friday(lastday)
    if tf - pd.Timedelta(days=4) <= lastday < tf:
        exp_pending.add(lastday)                    # could still become expiry day if that Friday is a holiday
    need = {"overnight_break": min(cov["bars"], cov["ds"], cov["ctx"], cov["fomc"]),
            "opening_range": min(cov["bars"], cov["ds"], cov["ctx"], cov["fomc"]),
            "expiry_fade": min(cov["bars"], cov["ds"]), CALM: min(cov["bars"], cov["ds"]),
            L1: min(cov["bars"], cov["ds"])}
    held = {}
    release = {}
    cpi = set(pd.to_datetime(pd.read_csv("data/cpi_dates.csv").date))
    trading = set(cash_days)
    pending = {n: set(todo[n]) for n in names}
    for n in names:
        ok = []
        for d in todo[n]:
            why = ""
            if d > need[n]:
                why = "inputs not refreshed through this day"
            elif n in LIVE and d in exp_pending:
                why = "expiry status not final until the next session is in the data"
            elif n == L1:
                kinds = ["CPI"] if d in cpi else []
                if d in nfp:
                    kinds.append("jobs report")
                elif d > nfp_last and first_friday_proxy(d, trading):
                    kinds.append("jobs report (first-Friday proxy: official list ends "
                                 f"{nfp_last:%Y-%m-%d})")
                if d > cov["cpi"] and not kinds:
                    why = f"CPI calendar ends {cov['cpi']:%Y-%m-%d}: add the next CPI dates to data/cpi_dates.csv"
                release[d] = kinds
            (held.setdefault(n, []).append((d, why)) if why else ok.append(d))
        todo[n] = ok
    if "overnight_break" in todo and todo["overnight_break"] and not a.report_only:
        x5 = pd.read_pickle(f"data/x5_{SYM}.pkl")["sess"].max()
        ff = pd.read_pickle(f"data/fut_features_{SYM}.pkl")["date"].max()
        lim = min(pd.Timestamp(x5), pd.Timestamp(ff))
        gc.collect()
        for d in [d for d in todo["overnight_break"] if d > lim]:
            held.setdefault("overnight_break", []).append((d, "x5_NQ.pkl / fut_features_NQ.pkl not rebuilt"))
        todo["overnight_break"] = [d for d in todo["overnight_break"] if d <= lim]
    # the live models are computed together; a day is computed when every live model still missing it is ready
    cand = set().union(*(pending[n] for n in LIVE))
    live_days = {d for d in cand if all(d not in pending[n] or d in set(todo[n]) for n in LIVE)}
    for n in LIVE:
        for d in set(todo[n]) - live_days:
            held.setdefault(n, []).append((d, "waiting for the other live models' inputs"))
        todo[n] = sorted(set(todo[n]) & live_days)

    n_new = sum(len(v) for v in todo.values())
    if held:
        print("HELD BACK (logged on a later run once the inputs cover them):")
        for n, v in held.items():
            by = {}
            for d, w in sorted(v):
                by.setdefault(w, []).append(d)
            print(f"  {n}: " + "; ".join(
                (f"{ds[0]:%Y-%m-%d}" if len(ds) == 1 else f"{len(ds)} days {ds[0]:%Y-%m-%d}..{ds[-1]:%Y-%m-%d}")
                + f" ({w})" for w, ds in by.items()))
    if a.report_only or n_new == 0:
        print(f"No new sessions to log (from {since:%Y-%m-%d}; data's last cash session {lastday:%Y-%m-%d}).")
    else:
        rows = []
        if live_days:
            print(f"Computing live models for {len(live_days)} session(s) ...", flush=True)
            rows += [r for r in live_rows(set(live_days), cash_days, ds)]
            gc.collect()
        if todo[CALM]:
            print(f"Computing {CALM} for {len(todo[CALM])} session(s) ...", flush=True)
            rows += calm_rows(set(todo[CALM]))
            gc.collect()
        if todo[L1]:
            print(f"Computing {L1} for {len(todo[L1])} session(s) (jobs-report dates: {nfp_src[:60]}...) ...",
                  flush=True)
            rows += l1_rows(set(todo[L1]), release)
        stamp = pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d %H:%M:%S")
        new = pd.DataFrame(rows, columns=COLUMNS)
        new["logged_at"] = stamp
        new["_o"] = new.model_or_lead.map({n: i for i, n in enumerate(names)})
        new = new.sort_values(["date", "_o"]).drop(columns="_o")
        new = new[[(d, n) not in done for d, n in zip(new.date, new.model_or_lead)]]      # never duplicate
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        header = not (os.path.exists(out) and os.path.getsize(out) > 0)
        new.to_csv(out, mode="a", header=header, index=False)
        print(f"Appended {len(new)} rows ({new.date.nunique()} sessions) to {out}")
        last = new[new.date == new.date.max()]
        print(f"\nLATEST SESSION {last.date.iloc[0]}:")
        for r in last.itertuples(index=False):
            if r.signal in ("long", "short", "skipped"):
                what = (f"{r.signal:7s} {r.entry_time} @ {r.entry_px:.2f} -> {r.exit_time} @ {r.exit_px:.2f} "
                        f"({r.exit_reason}) ${r.net_usd:+.2f}" + (f"  [{r.skip_rule}: not taken]" if r.skip_rule else ""))
            else:
                what = f"none     {r.note}"
            print(f"  {r.model_or_lead:30s} {what}")
    report(out)
    preview(cov, nfp, nfp_last, cash_days)


if __name__ == "__main__":
    main()
