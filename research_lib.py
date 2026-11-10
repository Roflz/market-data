"""
research_lib.py - shared, tested research toolkit for the live MNQ models (chosen_models.py), so a new trading-rule
test takes seconds: cached data, every live trade with its full details, a cache of each trade's price path, an
exact fast re-simulator (replay) and the standard evaluation helpers. Tests: test_research_lib.py.

Units: everything is NET $ AT 1 MNQ MICRO after costs ($2/point; 1 tick slippage per fill + $1.00 commission per
round trip = $2.00 per trade at 1 tick), plus max drawdown and worst day on daily net $ (the prop-firm view).

Run scripts from the project folder:
    cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 my_test.py

Quick start
    import research_lib as rl
    T = rl.live_trades()                                  # every live trade (+ skipped ones: T.skipped)
    on = rl.replay("overnight_break")                     # == the live overnight-break trades, exactly
    cap = rl.replay("overnight_break", stop_cap_frac=0.002)   # stop capped at 0.20% of price
    print(rl.daily_stats(cap), rl.by_period(cap))
    print(rl.paired_daily_diff(cap, on))                  # daily $ difference vs live, with t
    print(rl.sweep("opening_range", "stop_mult", [0.5, 0.75, 1, 1.5, 2]))      # tidy table, ready to plot
    print(rl.book(replace={"overnight_break": cap}))      # the 3-model book with that change
    keep = ~some_rule(T[T.model == "overnight_break"])    # a keep/skip filter: True = keep the trade
    rep = rl.keep_filter_report(T[(T.model == "overnight_break") & ~T.skipped], keep)
    rl.print_report(rep)

CACHED LOADERS (folder data/cache/; a cache file is rebuilt automatically when any of its source files - data or
code - is newer than it; delete data/cache/ to force a rebuild; CACHE_VERSION is part of every file name). The
live-trades/path cache also lists research_lib.py itself as a source (an edit here costs a ~2 s rebuild). A full
build from scratch takes ~15 s and ~2 GB of memory at its peak (parsing the 1-minute CSV); afterwards replay() only
loads the ~30 MB live/path cache.
    bars_1m(sym="NQ")           all 1-minute bars (New York time index; Open High Low Close Volume instrument_id,
                                sess = Globex session date, tmin = minute of day)           <- data/{sym}_fut_1m.csv
    rth(sym="NQ")               lit_p5_orb day matrices: dict(dates, g = {Open,High,Low,Close,Volume} as
                                (days x 390 minute slots from 9:30), inst, sess, Cff = forward-filled close, info)
    engine(sym="NQ")            (D, signals): exits_engine.Day of 5-min bars 2011+ (as exits_compare.init builds it,
                                with D.pos) and the overnight-break signals [(bar, dir), ...]
    daily_sessions(sym), market_context()   the project's pickles (built by daily_sessions.py / market_context.py;
                                this module never rewrites them, it warns when they look older than their inputs)
    cash_days(), expiry_days(), skip_days() -> (after S&P -2% set, Fed-day set)   as chosen_models.py uses them
    build_all()                 builds every cache (and checks live_trades against the CSVs)

LIVE TRADES
    live_trades()   one row per live trade AND per trade removed by the skip rules R1/R2 (skipped=True), with
        model, date, side, skip_rule, skipped, signal_time, entry_time, entry_ref_raw (bar open), entry_px_raw (fill),
        stop_px_raw, stop_pts (entry fill to stop), R_pts (the model's risk unit), exit_time, exit_px_raw (fill), exit,
        net_pts, usd, R, bp, and the replay indices path_row (row in the model's path cache), sig_bar
        (overnight_break: signal bar in engine()'s D), di (row in rth() matrices).
        Times are New York wall-clock; exit_time is the bar close for close exits and the START of the bar in which
        a stop filled (paper_log.py's convention). Raw prices = unadjusted contract prices.
        Built by calling chosen_models.py's own functions on the cached data and asserted equal (every column of the
        CSVs, exact floats) to chosen_models_trades.csv and chosen_models_skipped.csv.
    trade_paths(model)  dict of padded float32 arrays sO/sH/sL/sC (SIGNED prices: shorts are mirrored, so a stop
        is always below; sH of a short = -Low), n (bars per path) and per-path metadata; 5-min bars from the entry
        bar to the 17:00 session end for overnight_break (one path per SIGNAL, taken or not, see replay), 1-min
        bars from the 9:35 entry to the 15:59 (12:59 early-close) exit bar for opening_range, 9:30 -> 15:59 for
        expiry_fade. sC is the forward-filled close for the 1-min models.

REPLAY  replay(model, stop_mult=None, stop_cap_frac=None, stop_pts=None, stop_usd=None, exit_time=None,
               slippage_ticks=1, include_skipped=False, engine=False, stop=None)
    Re-simulates the model's trades from the path cache with the engines' own fill rules: entry at the entry bar's
    open + slippage; stop snapped to the tick grid (exits_engine.snap_stop: longs round down, shorts up); a stop
    hit fills at the stop, or at the bar's open if the bar opened through it (the entry bar fills at the stop for
    the 1-min models, as lit_p5_orb.run_trade); a stop in the exit bar beats the exit; time/close exits fill at the
    bar close; slippage_ticks ticks against you on EVERY fill (entry and exit); $1.00 commission.
    Stop distance (points from the entry FILL): base = live stop distance (overnight_break 2 x ATR(5-min) at the
        signal; opening_range the distance to the first candle's other end; expiry_fade none = infinite), or
        stop_pts, or stop_usd / $2 (a $ distance per micro, excluding costs); then x stop_mult; then capped at
        stop_cap_frac x price (price = raw signal-bar close for overnight_break, as the stop-cap study did; the raw
        entry fill for the 1-min models). `stop` is a shorthand: "mult:1.5", "cap:0.002", "pts:20", "usd:40".
        overnight_break: stop_mult m is computed as exits_engine k0 = 2m (R = (2m) x ATR), exactly as ee.run(k0=2m).
    exit_time: "HH:MM" (or minute of day) - leave at the close of the bar that closes at/after that time (the
        exits_engine clock rule for overnight_break; the 1-min bar ending at that time for the others). Never later
        than the model's forced exit. Exit reason "time" when it is earlier than the forced exit.
    Which trades exist:
      overnight_break  EXACT including re-entries. The path cache holds every signal of the engine (1,884), not just
          the taken ones; replay simulates all of them, then applies exits_engine.run's own sequencing (one position
          at a time, a new signal only from the exit bar's close on, max 3 trades per session, invalid stop -> no
          trade). So a different stop/exit that frees the position earlier or later changes the later same-day
          entries exactly as the engine would. engine=True runs exits_engine.run itself with the same per-signal
          stops (slow, the reference); test_research_lib.py asserts both give identical trades.
      opening_range / expiry_fade  one trade per day; the take/skip decision (direction, 9:34-close cost filter at
          1 tick) is the live rule's and does not depend on the stop, so the trade set is fixed. A trade whose 9:35
          open was already through the stop exits at once at that open (live rule); this keeps happening under
          stop_mult / stop_cap_frac (the distance stays <= 0) but not under stop_pts / stop_usd (a fresh positive
          distance). engine=True runs the live rule's own per-trade code (lit_p5_orb.run_trade) as the reference.
      Trades on expiry Fridays are never in the breakout sets; include_skipped=True adds the R1/R2-skipped trades.
    Returns a DataFrame like live_trades (model, date, side, skip_rule, skipped, path_row, usd, net_pts, R, bp,
    exit, stopped, stop_pts, exit_time). With every option at its default it equals the live trades exactly.

EVALUATION (all in $ at 1 micro; `x` = a trades DataFrame with date and usd columns, or arrays usd + dates)
    by_period(x, dates=None)          Series: total, eras 2010-13 2014-17 2018-20 2021-23 2024-26, halves
                                      2010-17 2018-26, and 2023-26
    daily(x, dates=None)              daily net $ Series
    daily_stats(x, dates=None)        dict(net, trades, days, max_dd, worst_day, worst_month, per_trade)
                                      max_dd = largest drop of daily-$ equity measured from a start at $0
    book(replace=None, extra_cost_usd=0, models=MODELS)   the 3-model book (live trades; `replace` = {model: trades
                                      frame} swaps one model's trades) -> dict(daily stats, by_period, per model net)
    book_trades(replace=None, models=MODELS)               the combined trades frame
    welch_t(a, b)                     Welch t of mean(a) - mean(b)
    keep_filter_report(trades, keep, t_min=2.0, extra_tick_usd=1.0)
        a keep/skip filter on ONE model's trades (keep=True keeps): kept/removed counts and $, per period, $ per
        trade and Welch t (kept minus removed), model and 3-model-book stats before/after, the SPEC.md pass rule
        (a) removed $ < 0 in full, 2010-17 and 2018-26, (b) t >= t_min, (c) model max DD and worst day no worse;
        and the same at 2 ticks per fill ($1 less per trade, all models) under "two_tick".   print_report(rep)
    random_skip_control(trades, n_removed, removed_usd=None, eligible=None, draws=1000, seed=12345)
        remove the same number of trades at random from the eligible trades (random keys over ALL trades,
        then the n eligible trades with the smallest key, as filters/SWEEP.md builder X); percentile of the actual
        removed $ in that distribution (low = the rule removes worse trades than chance)
    familywise(variants, trades, eligible=None, draws=1000, seed=12345)
        variants = {name: removed mask}; per draw every variant is replaced by a random removal of its count
        (keys shared across variants within a draw); where the actual best (most negative) removed $ falls among
        the draws' best values
    removed_by_year(trades, variants) -> years x variants frame of gain = kept $ - all $ (= -removed $)
    walk_forward(gains_by_year, start=2013)   each year uses the variant with the best cumulative gain in all
        earlier years (ties, or best <= 0 -> no filter); returns (per-year table, summary dict)
    paired_daily_diff(a, b)           daily $ of a minus b over the union of days (missing day = 0): total, mean, t,
                                      by period
    sweep(model, param, values, two_tick=True, book_stats=True, **fixed)
        replay for each value (None = live) -> tidy DataFrame: value, trades, net, eras, halves, 2023-26, max_dd,
        worst_day, worst_month, stopped_share, net_2tick (a true re-simulation at 2 ticks per fill), book_net,
        book_max_dd, book_worst_day
"""
import contextlib
import os
import pickle
import sys
import time
import warnings

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)
CACHE = os.path.join(BASE, "data", "cache")
CACHE_VERSION = 1                     # bump when a cache's layout or the build logic changes
SYM = "NQ"
TICK = 0.25
USD_PT = 2.0                          # MNQ $ per point
COMM_USD = 1.0
COMM_PTS = COMM_USD / USD_PT
K = 5                                 # opening-range candle (minutes)
MODELS = ("overnight_break", "opening_range", "expiry_fade")
ERAS = {"2010-13": (2010, 2013), "2014-17": (2014, 2017), "2018-20": (2018, 2020), "2021-23": (2021, 2023),
        "2024-26": (2024, 2026)}
HALVES = {"2010-17": (2010, 2017), "2018-26": (2018, 2026)}
RECENT = {"2023-26": (2023, 2026)}
PERIODS = {**ERAS, **HALVES, **RECENT}
_MEM = {}


# ----------------------------------------------------------------------------------------------------------------
# cache machinery
# ----------------------------------------------------------------------------------------------------------------
@contextlib.contextmanager
def _in_project():
    """The project's modules read data/... relative to the working folder."""
    old = os.getcwd()
    os.chdir(BASE)
    try:
        yield
    finally:
        os.chdir(old)


@contextlib.contextmanager
def _quiet():
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def _p(rel):
    return os.path.join(BASE, rel)


def _cache_path(name, ext="pkl"):
    return os.path.join(CACHE, f"{name}.v{CACHE_VERSION}.{ext}")


def _fresh(path, sources):
    if not os.path.exists(path):
        return False
    newest = max(os.path.getmtime(_p(s)) for s in sources)
    return os.path.getmtime(path) >= newest


def _cached(name, sources, build, ext="pkl", save=None, load=None, verbose=True):
    """Load data/cache/<name> unless a source file is newer; otherwise build, save atomically, return."""
    key = (name, ext)
    path = _cache_path(name, ext)
    if key in _MEM and _fresh(path, sources):
        return _MEM[key]
    if _fresh(path, sources):
        obj = load(path) if load else pd.read_pickle(path)
    else:
        os.makedirs(CACHE, exist_ok=True)
        t0 = time.time()
        obj = build()
        tmp = path + ".tmp"
        if save:
            save(obj, tmp)
        else:
            with open(tmp, "wb") as f:
                pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, path)
        if verbose:
            print(f"[research_lib] built cache {os.path.basename(path)} in {time.time() - t0:.1f}s", file=sys.stderr)
    _MEM[key] = obj
    return obj


def _warn_if_stale(pkl, inputs, how):
    t = os.path.getmtime(_p(pkl))
    old = [s for s in inputs if os.path.exists(_p(s)) and os.path.getmtime(_p(s)) > t]
    if old:
        warnings.warn(f"{pkl} is older than {', '.join(old)}; rebuild it with: {how}")


# ----------------------------------------------------------------------------------------------------------------
# cached loaders
# ----------------------------------------------------------------------------------------------------------------
def bars_1m(sym=SYM):
    """All 1-minute bars of data/{sym}_fut_1m.csv, New York time index (cached as parquet)."""
    src = f"data/{sym}_fut_1m.csv"

    def build():
        d = pd.read_csv(_p(src))
        ts = pd.DatetimeIndex(pd.to_datetime(d.pop("ts_event"), utc=True, format="ISO8601")).tz_convert(
            "America/New_York")
        d.index = ts
        d.index.name = "ts"
        d = d[~d.index.duplicated()].sort_index()
        d["sess"] = (d.index + pd.Timedelta(hours=6)).tz_localize(None).normalize()
        d["tmin"] = (d.index.hour * 60 + d.index.minute).astype(np.int16)
        return d

    return _cached(f"bars1m_{sym}", [src], build, ext="parquet",
                   save=lambda o, p: o.to_parquet(p, compression="zstd"), load=pd.read_parquet)


def rth(sym=SYM):
    """lit_p5_orb.load_market + build_sessions (the 1-min RTH day matrices), cached. Prices stored as float32
    (exact: every price is on the 0.25 tick grid) and returned as float64."""
    srcs = [f"data/{sym}_fut_1m.csv", "lit_p5_orb.py"]

    def build():
        import lit_p5_orb as p5
        with _in_project(), _quiet():
            dates, g, inst = p5.load_market(sym)
            sess, Cff, info = p5.build_sessions(sym, dates, g, inst)
        for c in ("Open", "High", "Low", "Close"):
            m = ~np.isnan(g[c])
            assert np.all((g[c][m] * 4) % 1 == 0), f"{c}: off-grid price, float32 storage would not be exact"
        return dict(dates=dates, g={c: a.astype(np.float32) for c, a in g.items()}, inst=inst, sess=sess,
                    Cff=Cff.astype(np.float32), info=info)

    key = ("rth64", sym)
    raw = _cached(f"rth_{sym}", srcs, build)
    if key not in _MEM or _MEM[key][0] is not raw:
        out = dict(raw)
        out["g"] = {c: a.astype(np.float64) for c, a in raw["g"].items()}
        out["Cff"] = raw["Cff"].astype(np.float64)
        _MEM[key] = (raw, out)
    return _MEM[key][1]


def engine(sym=SYM):
    """(D, signals): exits_engine.Day of the 5-min bars from exits_compare.FIRST_YEAR on, with D.pos, exactly as
    exits_compare.init builds it, and the overnight-break signals (setup_rule.overnight_break) as exits_compare's
    'Overnight break + daily trend' entry set."""
    srcs = [f"data/x5_{sym}.pkl", f"data/fut_features_{sym}.pkl", "exits_engine.py", "exits_compare.py",
            "setup_rule.py", "data/fomc_dates.csv"]

    def build():
        import exits_compare as ec
        import exits_engine as ee
        import setup_rule
        with _in_project():
            b = pd.read_pickle(f"data/x5_{sym}.pkl")
            D = ee.Day(b[b.index.year >= ec.FIRST_YEAR])
            del b
            D.pos = pd.Index(D.idx)
            F = pd.read_pickle(f"data/fut_features_{sym}.pkl")
            bar = D.pos.get_indexer(pd.DatetimeIndex(F["ts"]) - pd.Timedelta(minutes=4))
            sig = setup_rule.overnight_break(F["X"], F["ts"])
            m = (sig != 0) & (bar >= 0)
            sigs = sorted(zip(bar[m].tolist(), sig[m].tolist()))
            del F
        return D, sigs

    return _cached(f"engine_{sym}", srcs, build)


def daily_sessions(sym=SYM):
    key = ("ds", sym)
    if key not in _MEM:
        f = f"data/daily_sessions_{sym}.pkl"
        _warn_if_stale(f, [f"data/{sym}_fut_1m.csv", "daily_sessions.py"], "PYTHONPATH=./pylib python3 daily_sessions.py")
        _MEM[key] = pd.read_pickle(_p(f))
    return _MEM[key]


def market_context():
    if "ctx" not in _MEM:
        f = "data/market_context.pkl"
        _warn_if_stale(f, ["market_context.py"], "PYTHONPATH=./pylib python3 market_context.py")
        _MEM["ctx"] = pd.read_pickle(_p(f))
    return _MEM["ctx"]


def cash_days(sym=SYM):
    ds = daily_sessions(sym)
    return ds.index[ds.cash_day]


def expiry_days(sym=SYM):
    import calendar_days as cd
    return cd.expiry_fridays(cash_days(sym))


def skip_days():
    """(dates after an S&P 500 drop of 2%+ (R1), scheduled Fed statement days (R2)) - chosen_models.skip_days."""
    import chosen_models as cm
    if "skipdays" not in _MEM:
        with _in_project():
            _MEM["skipdays"] = cm.skip_days()
    return _MEM["skipdays"]


# ----------------------------------------------------------------------------------------------------------------
# live trades + trade paths (one cache file)
# ----------------------------------------------------------------------------------------------------------------
_LIVE_SRCS = ["data/NQ_fut_1m.csv", "data/x5_NQ.pkl", "data/fut_features_NQ.pkl", "data/daily_sessions_NQ.pkl",
              "data/market_context.pkl", "data/fomc_dates.csv", "lit_p5_orb.py", "exits_engine.py",
              "exits_compare.py", "setup_rule.py", "calendar_days.py", "chosen_models.py",
              "chosen_models_trades.csv", "chosen_models_skipped.csv", "research_lib.py"]
_CSV_COLS = ["model", "date", "side", "exit", "usd", "R", "bp"]


def _naive(ts):
    ts = pd.DatetimeIndex(ts)
    return ts.tz_localize(None) if ts.tz is not None else ts


def _signed(O, H, L, C, d):
    """Mirror shorts so that a stop is always below the price: (sO, sH, sL, sC)."""
    d = np.asarray(d, float)[:, None]
    return O * d, np.where(d > 0, H, -L), np.where(d > 0, L, -H), C * d


def _pad(rows, n, L):
    out = np.full((len(rows), L), np.nan, np.float32)
    for j, (r, k) in enumerate(zip(rows, n)):
        out[j, :k] = r[:k]
    return out


def _build_live():
    import calendar_days as cd
    import chosen_models as cm
    import exits_compare as ec
    import exits_engine as ee
    import lit_p5_orb as p5
    import setup_rule

    ds = daily_sessions()
    cash = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash)
    after_drop, fed = skip_days()
    M = rth()
    dates, g, Cff = M["dates"], M["g"], M["Cff"]
    sess = M["sess"][M["sess"].date.isin(cash)]
    D, sigs = engine()

    # ---- the official model functions, on the cached data -----------------------------------------------------
    saved_G, saved_init = dict(ec.G), ec.init
    ec.G.clear()
    ec.G[SYM], ec.G[("sets", SYM)] = D, {setup_rule.NAME: sigs}
    ec.init = lambda: None                                  # NQ only: chosen_models.overnight_break uses ec.G[NQ]
    try:
        with _in_project():
            onb = cm.overnight_break(expiry, cash, ds)
    finally:
        ec.init = saved_init
        ec.G.clear()
        ec.G.update(saved_G)
    orb = cm.opening_range(expiry, sess, g, Cff)
    exf = cm.expiry_fade(expiry, sess, g, Cff)

    # ---- overnight_break: details + paths for EVERY signal --------------------------------------------------------
    t = ee.run(D, sigs, "hold", k0=2.0)                     # the call chosen_models.overnight_break makes
    sp = ee.SPEC[SYM]
    adj_s = ds.close_adj - ds.close_raw
    sig_bar = np.array([i for i, _ in sigs], np.int64)
    sig_dir = np.array([d for _, d in sigs], np.int64)
    assert len(np.unique(sig_bar)) == len(sig_bar)
    e = sig_bar + 1
    end = D.day_end[e]
    n_on = end - e + 1
    Lon = int(n_on.max())
    sdate = pd.DatetimeIndex(pd.to_datetime(D.sess[sig_bar]))
    adj = adj_s.reindex(sdate).to_numpy()
    rows_ = [np.arange(a, a + Lon).clip(max=D.n - 1) for a in e]
    idxm = np.vstack(rows_)
    sO, sH, sL, sC = _signed(D.Open[idxm], D.High[idxm], D.Low[idxm], D.Close[idxm], sig_dir)
    colm = np.arange(Lon)[None, :] < n_on[:, None]
    for a in (sO, sH, sL, sC):
        a[~colm] = np.nan
    tmin = np.where(colm, D.tmin[idxm], -1).astype(np.int16)
    ts_ns = _naive(D.idx).as_unit("ns").asi8[idxm]
    P_on = dict(sO=sO.astype(np.float32), sH=sH.astype(np.float32), sL=sL.astype(np.float32),
                sC=sC.astype(np.float32), n=n_on, tmin=tmin, ts=ts_ns,
                meta=pd.DataFrame({"sig_bar": sig_bar, "d": sig_dir, "e": e, "day": D.day[sig_bar], "date": sdate,
                                   "atr5": D.atr5[sig_bar], "adj": adj, "raw_close": D.Close[sig_bar] - adj,
                                   "sig_time": _naive(D.idx[sig_bar]) + pd.Timedelta(minutes=5)}))
    for c in ("sO", "sH", "sL", "sC"):
        assert np.array_equal(P_on[c].astype(np.float64), locals()[c], equal_nan=True)
    k_of_bar = {b: k for k, b in enumerate(sig_bar)}
    det = []
    for r in t.loc[onb.index].itertuples():
        i, d = int(r.bar), int(r.dir)
        x = i + int(r.hold_bars)
        a = adj_s.get(pd.Timestamp(D.sess[i]), np.nan)
        entry = D.Open[i + 1] + d * ee.SLIP
        stop = ee.snap_stop(entry - d * r.R_pts, d)
        xt = D.idx[x] if r.exit == "stop" else D.idx[x] + pd.Timedelta(minutes=5)
        det.append(dict(signal_time=D.idx[i] + pd.Timedelta(minutes=5), entry_time=D.idx[i + 1],
                        entry_ref_raw=D.Open[i + 1] - a, entry_px_raw=entry - a, stop_px_raw=stop - a,
                        stop_pts=d * (entry - stop), R_pts=r.R_pts, exit_time=xt, exit_px_raw=entry + d * r.pts - a,
                        net_pts=r.pts - sp["comm"] / sp["usd"], path_row=k_of_bar[i], sig_bar=i, di=-1))
    det = pd.DataFrame(det, index=onb.index)
    for c in ("signal_time", "entry_time", "exit_time"):
        det[c] = _naive(det[c])
    onb = onb.join(det)

    # ---- opening_range: details (the steps of chosen_models.opening_range) + paths -------------------------------
    O, H, L = g["Open"], g["High"], g["Low"]
    ppt = p5.MARKETS[SYM]["ppt"]
    sb = sess.set_index("date")
    od, prow = [], []
    for j, r in enumerate(orb.itertuples(index=False)):
        s = sb.loc[r.date]
        i, s_x = int(s.di), int(s.exit_slot)
        oc, cc = O[i, 0], Cff[i, K - 1]
        d = 1 if cc > oc else -1
        stop = np.nanmin(L[i, :K]) if d > 0 else np.nanmax(H[i, :K])
        ref, fill = O[i, K], O[i, K] + d * p5.TICK
        if d * (fill - stop) <= 0:
            xs, xfill, why = K, ref - d * p5.TICK, "stop"
        else:
            xs, _, xfill, why = p5.run_trade(H[i], L[i], O[i], Cff[i, s_x], K, s_x, d, stop, None, True)
        net = d * (xfill - fill) - p5.COMM / ppt
        assert net * ppt == r.usd and why == r.exit and (d > 0) == (r.side == "long")
        day = pd.Timestamp(r.date)
        od.append(dict(signal_time=day + pd.Timedelta(minutes=570 + K), entry_time=day + pd.Timedelta(minutes=570 + K),
                       entry_ref_raw=ref, entry_px_raw=fill, stop_px_raw=stop, stop_pts=d * (fill - stop),
                       R_pts=d * (fill - stop), exit_time=day + pd.Timedelta(minutes=570 + xs + (why != "stop")),
                       exit_px_raw=xfill, net_pts=net, path_row=j, sig_bar=-1, di=i))
        prow.append((i, d, s_x, ref, cc, stop, day))
    orb = pd.concat([orb.reset_index(drop=True), pd.DataFrame(od)], axis=1)
    di_o = np.array([p[0] for p in prow])
    d_o = np.array([p[1] for p in prow])
    sx_o = np.array([p[2] for p in prow])
    n_o = sx_o - K + 1
    Lo = int(n_o.max())
    cols = (K + np.arange(Lo))[None, :].clip(max=p5.NSLOT - 1)
    sO, sH, sL, sC = _signed(O[di_o[:, None], cols], H[di_o[:, None], cols], L[di_o[:, None], cols],
                             Cff[di_o[:, None], cols], d_o)
    colm = np.arange(Lo)[None, :] < n_o[:, None]
    for a in (sO, sH, sL, sC):
        a[~colm] = np.nan
    P_orb = dict(sO=sO.astype(np.float32), sH=sH.astype(np.float32), sL=sL.astype(np.float32),
                 sC=sC.astype(np.float32), n=n_o, first_slot=K,
                 meta=pd.DataFrame({"di": di_o, "d": d_o, "exit_slot": sx_o, "ref": [p[3] for p in prow],
                                    "cc": [p[4] for p in prow], "stop": [p[5] for p in prow],
                                    "date": pd.DatetimeIndex([p[6] for p in prow])}))

    # ---- expiry_fade -----------------------------------------------------------------------------------------
    ed, erow = [], []
    for j, r in enumerate(exf.itertuples(index=False)):
        s = sb.loc[r.date]
        i = int(s.di)
        xs = min(p5.FULL_EXIT_SLOT, int(s.exit_slot))
        ent, ext = O[i, 0], Cff[i, xs]
        day = pd.Timestamp(r.date)
        ed.append(dict(signal_time=day + pd.Timedelta(minutes=570), entry_time=day + pd.Timedelta(minutes=570),
                       entry_ref_raw=ent, entry_px_raw=ent - p5.TICK, stop_px_raw=np.nan, stop_pts=np.inf,
                       R_pts=np.nan, exit_time=day + pd.Timedelta(minutes=570 + xs + 1), exit_px_raw=ext + p5.TICK,
                       net_pts=(ent - p5.TICK) - (ext + p5.TICK) - p5.COMM / ppt, path_row=j, sig_bar=-1, di=i))
        erow.append((i, xs, ent, day))
    exf = pd.concat([exf.reset_index(drop=True), pd.DataFrame(ed)], axis=1)
    di_e = np.array([p[0] for p in erow])
    n_e = np.array([p[1] for p in erow]) + 1
    Le = int(n_e.max())
    cols = np.arange(Le)[None, :]
    d_e = -np.ones(len(erow), int)
    sO, sH, sL, sC = _signed(O[di_e[:, None], cols], H[di_e[:, None], cols], L[di_e[:, None], cols],
                             Cff[di_e[:, None], cols], d_e)
    colm = cols < n_e[:, None]
    for a in (sO, sH, sL, sC):
        a[~colm] = np.nan
    P_exf = dict(sO=sO.astype(np.float32), sH=sH.astype(np.float32), sL=sL.astype(np.float32),
                 sC=sC.astype(np.float32), n=n_e, first_slot=0,
                 meta=pd.DataFrame({"di": di_e, "d": d_e, "exit_slot": n_e - 1, "ref": [p[2] for p in erow],
                                    "date": pd.DatetimeIndex([p[3] for p in erow])}))

    # ---- combine exactly as chosen_models.main does ---------------------------------------------------------------
    T = pd.concat([onb, orb, exf], ignore_index=True)
    T = T.sort_values(["date", "model"]).reset_index(drop=True)
    breakout = T.model.isin(["overnight_break", "opening_range"])
    T["skip_rule"] = np.where(breakout & T.date.isin(after_drop), "R1 after S&P -2%",
                              np.where((T.model == "opening_range") & T.date.isin(fed), "R2 Fed day", ""))
    T["skipped"] = T.skip_rule != ""
    T["date"] = pd.DatetimeIndex(T.date).astype("datetime64[ns]")
    for c in ("signal_time", "entry_time", "exit_time"):
        T[c] = pd.DatetimeIndex(T[c]).astype("datetime64[ns]")
    T = T[["model", "date", "side", "skip_rule", "skipped", "signal_time", "entry_time", "entry_ref_raw",
           "entry_px_raw", "stop_px_raw", "stop_pts", "R_pts", "exit_time", "exit_px_raw", "exit", "net_pts", "usd",
           "R", "bp", "path_row", "sig_bar", "di"]]
    _check_vs_csv(T)
    return dict(trades=T, paths={"overnight_break": P_on, "opening_range": P_orb, "expiry_fade": P_exf})


def _check_vs_csv(T):
    """live trades == chosen_models_trades.csv / chosen_models_skipped.csv, every column, exact floats."""
    for f, sel, cols in [("chosen_models_trades.csv", ~T.skipped, _CSV_COLS),
                         ("chosen_models_skipped.csv", T.skipped, _CSV_COLS + ["skip_rule"])]:
        ref = pd.read_csv(_p(f), parse_dates=["date"], float_precision="round_trip", keep_default_na=False,
                          na_values={"R": [""], "bp": [""], "usd": [""]})
        mine = T.loc[sel, cols].reset_index(drop=True)
        last = ref.date.max()
        if mine.date.max() > last:
            warnings.warn(f"data extends past {f} ({last:%Y-%m-%d}); compared up to that date - rerun chosen_models.py")
            mine = mine[mine.date <= last].reset_index(drop=True)
        assert len(mine) == len(ref), f"{f}: {len(mine)} rows rebuilt vs {len(ref)} in the file (rerun chosen_models.py?)"
        assert (mine.date.to_numpy() == ref.date.to_numpy().astype("datetime64[ns]")).all(), f"{f}: dates differ"
        for c in cols:
            if c == "date":
                continue
            a, b = mine[c].to_numpy(), ref[c].to_numpy()
            if a.dtype.kind == "f" or b.dtype.kind == "f":
                ok = np.array_equal(a.astype(float), b.astype(float), equal_nan=True)
            else:
                ok = np.array_equal(a.astype(str), b.astype(str))
            assert ok, f"{f}: column {c} differs from the rebuilt live trades"


def _live():
    return _cached("live_NQ", _LIVE_SRCS, _build_live)


def live_trades(include_skipped=True):
    """Every live trade (and, by default, the R1/R2-skipped ones, skipped=True). Equals the chosen_models CSVs."""
    T = _live()["trades"]
    return (T if include_skipped else T[~T.skipped].reset_index(drop=True)).copy()


def trade_paths(model):
    """Path cache of one model (see the module docstring); signed float32 arrays."""
    return _live()["paths"][model]


def _paths64(model):
    key = ("p64", model)
    raw = trade_paths(model)
    if key not in _MEM or _MEM[key][0] is not raw:
        out = dict(raw)
        for c in ("sO", "sH", "sL", "sC"):
            out[c] = raw[c].astype(np.float64)
        _MEM[key] = (raw, out)
    return _MEM[key][1]


def build_all():
    """Build (or validate) every cache. Returns {name: seconds}."""
    out = {}
    for name, fn in [("bars_1m", bars_1m), ("rth", rth), ("engine", engine), ("live+paths", _live)]:
        t0 = time.time()
        fn()
        out[name] = time.time() - t0
    return out


# ----------------------------------------------------------------------------------------------------------------
# replay
# ----------------------------------------------------------------------------------------------------------------
def _minutes(t):
    if t is None:
        return None
    if isinstance(t, str):
        h, m = t.split(":")
        return int(h) * 60 + int(m)
    return int(t)


def _parse_stop(stop, kw):
    if stop is None:
        return kw
    kind, val = stop.split(":")
    name = {"mult": "stop_mult", "cap": "stop_cap_frac", "pts": "stop_pts", "usd": "stop_usd"}[kind]
    if kw.get(name) is not None:
        raise ValueError(f"stop={stop!r} and {name} both given")
    kw[name] = float(val)
    return kw


def _first_true(m):
    """(any, first index) per row of a bool matrix."""
    a = m.any(1)
    return a, np.where(a, m.argmax(1), -1)


def _dist(orig, price, mult, cap, pts, usd_, k0_orig=None, atr=None):
    """Stop distance in points from the entry fill (see the module docstring)."""
    if pts is not None or usd_ is not None:
        base = np.full(len(orig), float(pts if pts is not None else usd_ / USD_PT))
        if mult is not None:
            base = base * mult
    elif mult is not None:
        base = (k0_orig * mult) * atr if atr is not None else orig * mult
    else:
        base = orig
    if cap is not None:
        base = np.minimum(base, cap * price)
    return base


def replay(model, stop_mult=None, stop_cap_frac=None, stop_pts=None, stop_usd=None, exit_time=None,
           slippage_ticks=1, include_skipped=False, engine=False, stop=None):
    """Re-simulate a live model's trades under a changed stop / exit time / slippage (see the module docstring).
    Default settings reproduce the live trades exactly."""
    kw = _parse_stop(stop, dict(stop_mult=stop_mult, stop_cap_frac=stop_cap_frac, stop_pts=stop_pts,
                                stop_usd=stop_usd))
    T = _minutes(exit_time)
    slip = slippage_ticks * TICK
    fn = {"overnight_break": _replay_on, "opening_range": _replay_1m, "expiry_fade": _replay_1m}[model]
    out = fn(model, kw, T, slip, engine)
    if not include_skipped:
        out = out[~out.skipped].reset_index(drop=True)
    return out


def _frame(model, date, d, net, R, bp, why, dist, exit_time, path_row):
    r1, fed = skip_days()
    date = pd.DatetimeIndex(date)
    rule = np.where(date.isin(r1), "R1 after S&P -2%",
                    np.where(date.isin(fed) & (model == "opening_range"), "R2 Fed day", ""))
    if model == "expiry_fade":
        rule = np.full(len(date), "")
    return pd.DataFrame({"model": model, "date": date.astype("datetime64[ns]"),
                         "side": np.where(np.asarray(d) > 0, "long", "short"), "skip_rule": rule,
                         "skipped": rule != "", "path_row": path_row, "usd": net * USD_PT, "net_pts": net, "R": R,
                         "bp": bp, "exit": why, "stopped": np.asarray(why) == "stop", "stop_pts": dist,
                         "exit_time": pd.DatetimeIndex(exit_time).astype("datetime64[ns]")})


def _replay_on(model, kw, T, slip, use_engine):
    P = _paths64(model)
    m = P["meta"]
    dist = _dist(2.0 * m.atr5.to_numpy(), m.raw_close.to_numpy(), kw["stop_mult"], kw["stop_cap_frac"],
                 kw["stop_pts"], kw["stop_usd"], k0_orig=2.0, atr=m.atr5.to_numpy())
    if use_engine:
        k, pts, why, xbar = _on_engine(P, dist, T, slip)
        ts = _naive(engine()[0].idx).as_unit("ns").asi8[xbar]
    else:
        k, pts, why, xcol = _on_fast(P, dist, T, slip)
        ts = P["ts"][k, xcol]
    ts = pd.to_datetime(ts) + pd.to_timedelta(np.where(why == "stop", 0, 5), unit="m")
    date = m.date.to_numpy()[k]
    cash, expiry = cash_days(), expiry_days()
    keep = pd.DatetimeIndex(date).isin(cash) & ~pd.DatetimeIndex(date).isin(expiry)
    k, pts, why, ts, date = k[keep], pts[keep], why[keep], ts[keep], date[keep]
    net = pts - COMM_PTS
    R = dist[k]
    return _frame(model, date, m.d.to_numpy()[k], net, net / R, 1e4 * net / m.raw_close.to_numpy()[k], why, R, ts, k)


def _on_fast(P, R, T, slip):
    """Every signal simulated at once (vectorized), then exits_engine.run's sequencing."""
    sO, sL, sC, n = P["sO"], P["sL"], P["sC"], P["n"]
    S, L = sO.shape
    rows, col = np.arange(S), np.arange(L)[None, :]
    with np.errstate(invalid="ignore"):
        valid = np.isfinite(R) & (R > 0)
    sentry = sO[:, 0] + slip
    sstop = np.floor((sentry - R) / TICK + 1e-9) * TICK
    xc = n - 1
    if T is not None:
        has, first = _first_true((P["tmin"] + 5 >= T) & (col < n[:, None]))
        xc = np.where(has, first, n - 1)
    with np.errstate(invalid="ignore"):
        hit, hc = _first_true((sL <= sstop[:, None]) & (col <= xc[:, None]))
    xcol = np.where(hit, hc, xc)
    o = sO[rows, np.maximum(hc, 0)]
    sx = np.where(hit, np.minimum(sstop, o) - slip, sC[rows, xc] - slip)
    pts = sx - sentry
    why = np.where(hit, "stop", np.where(xc < n - 1, "time", "close"))
    # exits_engine.run: one position at a time; a signal may come from the exit bar's close; max 3 per session
    e, day = P["meta"].e.to_numpy(), P["meta"].day.to_numpy()
    sig_bar = P["meta"].sig_bar.to_numpy()
    xbar = e + xcol
    taken, free, per_day = [], -1, {}
    for j in range(S):
        if sig_bar[j] < free or per_day.get(day[j], 0) >= 3:
            continue
        if not valid[j]:
            continue
        taken.append(j)
        per_day[day[j]] = per_day.get(day[j], 0) + 1
        free = xbar[j]
    k = np.array(taken, int)
    return k, pts[k], why[k], xcol[k]


def _on_engine(P, R, T, slip):
    """Reference: exits_engine.run itself with the same per-signal stop distances."""
    import exits_engine as ee
    D, sigs = engine()
    extra = {i: {"R_pts": float(r)} for (i, _), r in zip(sigs, R)}
    rule = "hold" if T is None else f"clock_{T}"
    old = ee.SLIP
    ee.SLIP = slip
    try:
        t = ee.run(D, sigs, rule, k0=2.0, extra=extra)
    finally:
        ee.SLIP = old
    k_of_bar = {b: j for j, b in enumerate(P["meta"].sig_bar.to_numpy())}
    k = np.array([k_of_bar[b] for b in t.bar], int)
    why = t.exit.replace({"clock": "time"}).to_numpy().astype(object)
    xbar = (t.bar + t.hold_bars).to_numpy()
    assert np.allclose(t.R_pts.to_numpy(), R[k], equal_nan=True)
    return k, t.pts.to_numpy(), why, xbar


def _replay_1m(model, kw, T, slip, use_engine):
    P = _paths64(model)
    m = P["meta"]
    s0 = P["first_slot"]
    d = m.d.to_numpy()
    ref = m.ref.to_numpy()
    sfill = d * ref + slip                                 # signed entry fill
    changed = any(kw[c] is not None for c in ("stop_mult", "stop_cap_frac", "stop_pts", "stop_usd"))
    if model == "opening_range":
        sstop0 = d * m.stop.to_numpy()
        orig = sfill - sstop0
    else:
        sstop0 = np.full(len(d), -np.inf)
        orig = np.full(len(d), np.inf)
    if changed:
        dist = _dist(orig, d * sfill, kw["stop_mult"], kw["stop_cap_frac"], kw["stop_pts"], kw["stop_usd"])
        with np.errstate(invalid="ignore"):
            sstop = np.floor((sfill - dist) / TICK + 1e-9) * TICK
    else:
        sstop = sstop0
    xslot = m.exit_slot.to_numpy()
    if T is not None:
        ts = T - 571                                        # the 1-min bar that closes at T
        if ts < s0:
            raise ValueError(f"exit_time {T // 60}:{T % 60:02d} is before the entry")
        xslot = np.minimum(xslot, ts)
    timed = xslot < m.exit_slot.to_numpy()
    imm = (sfill - sstop) <= 0                             # opened through the stop: out at once at the open
    if use_engine:
        xs, sx, why = _1m_reference(P, d, sfill, sstop, xslot, slip, imm, model)
    else:
        xs, sx, why = _1m_fast(P, sstop, xslot - s0, slip, imm)
        xs = xs + s0
    why = np.where((why == "close") & timed, "time", why)
    net = (sx - sfill) - COMM_PTS
    if model == "opening_range":
        R = np.where(imm, (d * m.cc.to_numpy() + TICK) - sstop, sfill - sstop)
        bp = 1e4 * net / ref
    else:
        R = np.full(len(d), np.nan)
        bp = 1e4 * net / ref
    dist_out = sfill - sstop
    et = pd.DatetimeIndex(m.date) + pd.to_timedelta(570 + xs + (why != "stop"), unit="m")
    with np.errstate(invalid="ignore", divide="ignore"):
        Rr = net / R
    return _frame(model, m.date, d, net, Rr, bp, why, dist_out, et, np.arange(len(d)))


def _1m_fast(P, sstop, xc, slip, imm):
    sO, sL, sC = P["sO"], P["sL"], P["sC"]
    S, L = sO.shape
    rows, col = np.arange(S), np.arange(L)[None, :]
    with np.errstate(invalid="ignore"):
        hit, hc = _first_true((sL <= sstop[:, None]) & (col <= xc[:, None]))
    o = sO[rows, np.maximum(hc, 0)]
    with np.errstate(invalid="ignore"):
        gap = (hc > 0) & ~np.isnan(o) & (o < sstop)
    sx = np.where(hit, np.where(gap, o, sstop) - slip, sC[rows, xc] - slip)
    xs = np.where(hit, hc, xc)
    why = np.where(hit, "stop", "close").astype(object)
    sx = np.where(imm, sO[:, 0] - slip, sx)
    xs = np.where(imm, 0, xs)
    why = np.where(imm, "stop", why)
    return xs, sx, why


def _1m_reference(P, d, sfill, sstop, xslot, slip, imm, model):
    """Reference: the live rule's per-trade code (lit_p5_orb.run_trade on the rth() matrices), slow."""
    import lit_p5_orb as p5
    M = rth()
    g, Cff = M["g"], M["Cff"]
    m = P["meta"]
    s0 = P["first_slot"]
    xs_o, sx_o, why_o = [], [], []
    for j in range(len(m)):
        i, dd = int(m.di.iat[j]), int(d[j])
        stop = dd * sstop[j]
        s_x = int(xslot[j])
        if imm[j]:
            xs, xref, why = s0, g["Open"][i, s0], "stop"
        else:
            xs, xref, _, why = p5.run_trade(g["High"][i], g["Low"][i], g["Open"][i], Cff[i, s_x], s0, s_x, dd, stop,
                                            None, True)
        xs_o.append(xs)
        sx_o.append(dd * (xref - dd * slip))
        why_o.append(why)
    return np.array(xs_o), np.array(sx_o), np.array(why_o, dtype=object)


# ----------------------------------------------------------------------------------------------------------------
# evaluation helpers ($ at 1 micro)
# ----------------------------------------------------------------------------------------------------------------
def _ud(x, dates=None):
    if isinstance(x, pd.DataFrame):
        return x.usd.to_numpy(float), pd.DatetimeIndex(x.date)
    if isinstance(x, pd.Series) and dates is None:
        return x.to_numpy(float), pd.DatetimeIndex(x.index)
    return np.asarray(x, float), pd.DatetimeIndex(dates)


def by_period(x, dates=None, periods=None):
    """Net $ in total and per standard period (eras, halves, 2023-26)."""
    u, dt = _ud(x, dates)
    y = dt.year
    out = {"total": u.sum()}
    for k, (a, b) in (periods or PERIODS).items():
        out[k] = u[(y >= a) & (y <= b)].sum()
    return pd.Series(out)


def daily(x, dates=None):
    u, dt = _ud(x, dates)
    return pd.Series(u, index=dt).groupby(level=0).sum().sort_index()


def max_drawdown(day_usd):
    eq = np.r_[0.0, np.cumsum(np.asarray(day_usd, float))]
    return float((np.maximum.accumulate(eq) - eq).max())


def daily_stats(x, dates=None):
    u, dt = _ud(x, dates)
    d = daily(u, dt)
    mo = d.groupby(d.index.to_period("M")).sum()
    return dict(net=float(u.sum()), trades=int(len(u)), days=int(len(d)),
                per_trade=float(u.mean()) if len(u) else np.nan, max_dd=max_drawdown(d.to_numpy()),
                worst_day=float(d.min()) if len(d) else 0.0, worst_month=float(mo.min()) if len(mo) else 0.0)


def book_trades(replace=None, models=MODELS):
    T = live_trades(include_skipped=False)
    parts = []
    for mname in models:
        src = (replace or {}).get(mname)
        if src is None:
            src = T[T.model == mname]
        f = src[["date", "usd"]].copy()
        f["model"] = mname
        parts.append(f)
    return pd.concat(parts, ignore_index=True)


def book(replace=None, extra_cost_usd=0.0, models=MODELS):
    """3-model book stats on daily net $. replace={model: trades frame} swaps a model's trades."""
    B = book_trades(replace, models)
    u = B.usd.to_numpy() - extra_cost_usd
    out = daily_stats(u, B.date)
    out["by_period"] = by_period(u, B.date)
    out["per_model"] = (B.assign(usd=u).groupby("model").usd.sum()).to_dict()
    return out


def welch_t(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


def keep_filter_report(trades, keep, t_min=2.0, extra_tick_usd=1.0, _extra=0.0):
    """Keep/skip filter on one model's trades (keep=True keeps). See the module docstring."""
    trades = trades.reset_index(drop=True)
    keep = np.asarray(keep, bool)
    assert len(keep) == len(trades)
    u = trades.usd.to_numpy(float) - _extra
    dt = pd.DatetimeIndex(trades.date)
    rem = ~keep
    model = trades.model.iloc[0] if "model" in trades and trades.model.nunique() == 1 else None
    rp, kp = by_period(u[rem], dt[rem]), by_period(u[keep], dt[keep])
    before, after = daily_stats(u, dt), daily_stats(u[keep], dt[keep])
    r = dict(n=len(u), kept_n=int(keep.sum()), removed_n=int(rem.sum()), share_removed=float(rem.mean()),
             all_usd=float(u.sum()), kept_usd=float(u[keep].sum()), removed_usd=float(u[rem].sum()),
             kept_per_trade=float(u[keep].mean()) if keep.any() else np.nan,
             removed_per_trade=float(u[rem].mean()) if rem.any() else np.nan,
             welch_t=welch_t(u[keep], u[rem]), removed_by_period=rp, kept_by_period=kp,
             share_removed_by_period=pd.Series({k: float(rem[(dt.year >= a) & (dt.year <= b)].mean())
                                                if ((dt.year >= a) & (dt.year <= b)).any() else np.nan
                                                for k, (a, b) in PERIODS.items()}),
             model_before=before, model_after=after)
    if model is not None:
        kept = trades[keep].assign(usd=u[keep] + _extra)
        r["book_before"] = book(extra_cost_usd=_extra)
        r["book_after"] = book(replace={model: kept}, extra_cost_usd=_extra)
    r["pass_a_removed_lose"] = bool(r["removed_usd"] < 0 and rp["2010-17"] < 0 and rp["2018-26"] < 0)
    r["pass_b_t"] = bool(r["welch_t"] >= t_min)
    r["pass_c_risk"] = bool(after["max_dd"] <= before["max_dd"] and after["worst_day"] >= before["worst_day"])
    r["PASS"] = r["pass_a_removed_lose"] and r["pass_b_t"] and r["pass_c_risk"]
    if _extra == 0.0 and extra_tick_usd:
        r["two_tick"] = keep_filter_report(trades, keep, t_min, 0.0, _extra=extra_tick_usd)
    return r


def print_report(r, name="filter"):
    def line(rr, tag):
        b0, b1 = rr["model_before"], rr["model_after"]
        s = (f"{tag}: removed {rr['removed_n']} of {rr['n']} ({rr['share_removed']:.0%}) = ${rr['removed_usd']:+,.1f}; "
             f"kept ${rr['kept_usd']:+,.1f}; $/trade kept {rr['kept_per_trade']:+.2f} vs removed "
             f"{rr['removed_per_trade']:+.2f}, Welch t {rr['welch_t']:+.3f}\n"
             f"   model DD ${b0['max_dd']:,.1f} -> ${b1['max_dd']:,.1f}, worst day ${b0['worst_day']:,.1f} -> "
             f"${b1['worst_day']:,.1f}")
        if "book_before" in rr:
            a, b = rr["book_before"], rr["book_after"]
            s += (f"\n   book net ${a['net']:,.1f} -> ${b['net']:,.1f}, DD ${a['max_dd']:,.1f} -> ${b['max_dd']:,.1f}, "
                  f"worst day ${a['worst_day']:,.1f} -> ${b['worst_day']:,.1f}")
        s += "\n   removed $ by period: " + ", ".join(f"{k} {v:+,.0f}" for k, v in rr["removed_by_period"].items())
        s += (f"\n   pass: (a) removed lose {rr['pass_a_removed_lose']}  (b) t {rr['pass_b_t']}  "
              f"(c) risk {rr['pass_c_risk']}  => {'PASS' if rr['PASS'] else 'FAIL'}")
        return s
    print(f"== {name}\n" + line(r, "1 tick") + ("\n" + line(r["two_tick"], "2 ticks") if "two_tick" in r else ""))


def _usd(trades):
    return trades.usd.to_numpy(float) if isinstance(trades, pd.DataFrame) else np.asarray(trades, float)


def random_skip_control(trades, n_removed, removed_usd=None, eligible=None, draws=1000, seed=12345):
    """Random-skip control (filters/SWEEP.md). n_removed: count, or the removed bool mask (then removed_usd is
    taken from it). Random keys are drawn for ALL trades (draws x N) and each draw removes the n eligible trades
    with the smallest keys. Returns dict(pctile = % of draws removing <= the actual $, mean, median, p5, actual,
    draws)."""
    u = _usd(trades)
    N = len(u)
    if not np.isscalar(n_removed):
        mask = np.asarray(n_removed, bool)
        removed_usd = u[mask].sum() if removed_usd is None else removed_usd
        n_removed = int(mask.sum())
    elig = np.ones(N, bool) if eligible is None else np.asarray(eligible, bool)
    rng = np.random.default_rng(seed)
    U = rng.random((draws, N))
    rr = _random_removed(U, u, elig, int(n_removed))
    out = dict(mean=float(rr.mean()), median=float(np.median(rr)), p5=float(np.percentile(rr, 5)), draws=rr)
    if removed_usd is not None:
        out["actual"] = float(removed_usd)
        out["pctile"] = float(100 * np.mean(rr <= removed_usd))
    return out


def _random_removed(U, u, elig, n):
    if n == 0:
        return np.zeros(len(U))
    cols = np.flatnonzero(elig)
    idx = np.argpartition(U[:, cols], n - 1, axis=1)[:, :n]
    return u[cols][idx].sum(axis=1)


def familywise(variants, trades, eligible=None, draws=1000, seed=12345):
    """variants: {name: removed bool mask}; eligible: None, one mask, or {name: mask}. Common random keys per draw
    (filters/SWEEP.md builder X). Returns dict(best_variant, best_removed_usd, fw_pctile, random_best_p5,
    random_best_median, family_size)."""
    u = _usd(trades)
    N = len(u)
    rng = np.random.default_rng(seed)
    U = rng.random((draws, N))
    actual, rand = {}, []
    for v, mask in variants.items():
        mask = np.asarray(mask, bool)
        el = eligible.get(v) if isinstance(eligible, dict) else eligible
        el = np.ones(N, bool) if el is None else np.asarray(el, bool)
        actual[v] = u[mask].sum()
        rand.append(_random_removed(U, u, el, int(mask.sum())))
    best_rand = np.column_stack(rand).min(axis=1)
    bv = min(actual, key=actual.get)
    return dict(best_variant=bv, best_removed_usd=float(actual[bv]), family_size=len(variants),
                fw_pctile=float(100 * np.mean(best_rand <= actual[bv])),
                random_best_p5=float(np.percentile(best_rand, 5)), random_best_median=float(np.median(best_rand)))


def removed_by_year(trades, variants, years=None):
    """years x variants frame of gain vs no filter = kept $ - all $ = -removed $ (input for walk_forward)."""
    u = _usd(trades)
    yr = pd.DatetimeIndex(trades.date).year.to_numpy()
    years = np.arange(yr.min(), yr.max() + 1) if years is None else years
    return pd.DataFrame({v: pd.Series(-np.where(np.asarray(m, bool), u, 0.0)).groupby(yr).sum()
                         .reindex(years, fill_value=0.0) for v, m in variants.items()})


def walk_forward(gains_by_year, start=2013):
    """Each year from `start`: use the variant with the best cumulative gain in all earlier years; ties for best,
    or best <= 0, -> no filter. Returns (table, summary)."""
    G = gains_by_year.sort_index()
    rows = []
    for y in G.index[G.index >= start]:
        cum = G.loc[G.index < y].sum()
        best = cum.max()
        pick = None if (best <= 0 or (cum == best).sum() > 1) else cum.idxmax()
        rows.append(dict(year=int(y), chosen=pick or "no filter", prior_cum_gain=float(best),
                         gain=float(G.loc[y, pick]) if pick else 0.0))
    W = pd.DataFrame(rows)
    return W, dict(total_gain=float(W.gain.sum()), years_better=int((W.gain > 0).sum()),
                   years_worse=int((W.gain < 0).sum()), years_no_filter=int((W.chosen == "no filter").sum()),
                   beats_no_filter=bool(W.gain.sum() > 0))


def paired_daily_diff(a, b, dates_a=None, dates_b=None):
    """Daily net $ of a minus b over the union of their days (a missing day counts $0); t of the mean."""
    da, db = daily(a, dates_a), daily(b, dates_b)
    da, db = da.align(db, fill_value=0.0)
    diff = da - db
    t = diff.mean() / (diff.std() / np.sqrt(len(diff))) if len(diff) > 1 and diff.std() > 0 else np.nan
    return dict(total=float(diff.sum()), mean=float(diff.mean()), t=float(t), days=int(len(diff)),
                by_period=by_period(diff.to_numpy(), diff.index), diff=diff)


def sweep(model, param, values, two_tick=True, book_stats=True, **fixed):
    """Replay `model` for each value of `param` (None = live setting) -> tidy DataFrame (one row per value)."""
    rows = []
    for v in values:
        kw = dict(fixed)
        if v is not None:
            kw[param] = v
        tr = replay(model, **kw)
        st = daily_stats(tr)
        row = dict(value=v, trades=st["trades"], net=st["net"])
        row.update(by_period(tr).drop("total").to_dict())
        row.update(max_dd=st["max_dd"], worst_day=st["worst_day"], worst_month=st["worst_month"],
                   stopped_share=float(tr.stopped.mean()))
        if two_tick:
            kw2 = dict(kw, slippage_ticks=kw.get("slippage_ticks", 1) + 1)
            row["net_2tick"] = float(replay(model, **kw2).usd.sum())
        if book_stats:
            b = book(replace={model: tr})
            row.update(book_net=b["net"], book_max_dd=b["max_dd"], book_worst_day=b["worst_day"])
        rows.append(row)
    return pd.DataFrame(rows)
