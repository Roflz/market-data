"""
prop_sim.py - fast prop-firm evaluation simulator (LucidFlex 25K by default) and the daily-P&L builder for the three
live models. Used by the Eval sandbox tab of model_heatmap_gui.py; tests in test_prop_sim.py.

SIMULATOR   simulate(daily, rules, start_from, start_to, eras) -> dict
    An evaluation account is started on EVERY trading day of the start window; each runs forward day by day until it
    passes, fails or the data ends ("still open"). All starts are simulated at once (a loop over account age, numpy
    vectors over the starts that are still open), so 2,200 starts take ~10-50 ms. Same rules and order of checks as
    the loop in research/eval_short_trades.py (passrate) and research/prop_lucid_flex_dd.py (evaluate), which it
    reproduces exactly (test_prop_sim.py asserts this):
      each day: balance += day P&L; best day = max(best day, day P&L); high = max(high, balance) (END-OF-DAY high);
      locked once high > lock_trigger; FAIL if balance <= (lock_at if locked else high - max_loss);
      else PASS if profit >= target and best day <= consistency x profit.
    Rules (LucidFlex 25K defaults): start $25,000, target $1,250, max loss $1,000 trailing the highest end-of-day
    balance, locking at start + $100 ($25,100) once a closing balance exceeds lock_at + max_loss ($26,100);
    consistency 40% (50% with the add-on; None = no rule); daily loss limit (dll) off by default - when set, each
    day's P&L is floored at -dll before the simulation (a soft limit: no more trading that day).
    Pass rate = passes / (passes + fails); starts still open at the end of the data are left out of it (as in the
    research scripts) and reported as open_share. Eras group the starts by start date.

DAILY SERIES   daily_series(Params) -> (dates, daily $, trades per day) over the full trading calendar (every date
    with a live trade, 2010-06 to the end of the data, as the research scripts use it)
    Models: overnight_break (stop multiple of the live 2 x ATR, stop cap as % of price, latest entry time, exit time
    <= 16:45 when Lucid flattens), opening_range (stop multiple of the first candle, cap, exit time or the live
    15:59 close), expiry_fade (no stop); micros per model; slippage ticks per fill; money at today's NQ price (each
    trade's price move rescaled to nq_price; costs stay fixed $ amounts - the research scripts' 'today' rule) or as
    traded. Trades come from research_lib.replay (exact engine fills). An overnight-break trade whose entry is at or
    after the exit time is dropped (you would not take a trade that must exit at once).
    Caching: each replay is cached by its own arguments and each model's daily series by its own parameters, so a
    change to one model, to micros or to a rule only recomputes what changed (a fresh replay ~10-30 ms).

CONVENIENCE
    evaluate(params, rules, start_from, start_to) -> dict: simulate() plus the series stats (net $/year, trades/year,
        day mean/sd, worst day, max drawdown) over the start window's days
    sweep(params, rules, key, values, ...) -> DataFrame, one row per value (key = any Params or Rules field)
    PRESETS, SPECS (slider grids, sweep values and labels for every parameter), ERAS

Usage (examples)
    cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib:. python3 prop_sim.py
    import prop_sim as ps
    r = ps.evaluate(ps.PRESETS["Eval plan: ONB 9:xx entries, cap 0.15%"][0])
    print(r["pass_rate"], r["eras"]["2018-21"]["pass_rate"], r["days_pass"])
    print(ps.sweep(ps.Params(), ps.Rules(), "onb_cap_pct", [0.1, 0.15, 0.2, None]))
"""
import functools
import math
import time
from dataclasses import dataclass, fields, replace

import numpy as np
import pandas as pd

P_NOW = 27_100.0                      # NQ price the research scripts rescale every trade to ("today's prices")
TICK, USD_PT, COMM_USD = 0.25, 2.0, 1.0
ERAS = {"2018-21": ("2018-01-01", "2021-12-31"), "2022-26": ("2022-01-01", "2026-12-31")}
DEFAULT_FROM = "2018-01-01"
OUT_PASS, OUT_FAIL, OUT_OPEN = 1, -1, 0


# ---------------------------------------------------------------------------------------------------- rules
@dataclass(frozen=True)
class Rules:
    start: float = 25_000.0
    target: float = 1_250.0
    max_loss: float = 1_000.0             # trails the highest end-of-day balance
    lock_at: float = None                 # None = start + 100
    lock_trigger: float = None            # None = lock_at + max_loss (a closing balance above it locks the limit)
    consistency: float = 0.40             # best day <= this share of total profit to pass; None = no rule
    dll: float = None                     # daily loss limit ($, soft): day P&L floored at -dll; None = off
    max_micros: int = 20                  # firm limit on open micros (the sandbox only warns about it)

    @property
    def lock_level(self):
        return self.start + 100.0 if self.lock_at is None else float(self.lock_at)

    @property
    def lock_trigger_level(self):
        return self.lock_level + self.max_loss if self.lock_trigger is None else float(self.lock_trigger)


def run_starts(v, start_idx, rules=Rules()):
    """Vectorized core. v = daily P&L (already floored by any daily loss limit), start_idx = day index of each
    start. Returns (outcome per start: 1 pass, -1 fail, 0 still open; days run, counting the final day)."""
    v = np.asarray(v, float)
    s = np.asarray(start_idx, np.int64)
    n, m = len(v), len(s)
    out = np.zeros(m, np.int8)
    days = np.zeros(m, np.int64)
    start, target, mll = float(rules.start), float(rules.target), float(rules.max_loss)
    lock_at, trig, cons = rules.lock_level, rules.lock_trigger_level, rules.consistency
    idx = np.arange(m)
    bal = np.full(m, start)
    hi = bal.copy()
    best = np.zeros(m)
    locked = np.zeros(m, bool)
    k = 0
    while len(idx):
        i = s[idx] + k
        alive = i < n
        if not alive.all():                         # ran out of data: still open after k days
            days[idx[~alive]] = k
            idx, i, bal, hi, best, locked = idx[alive], i[alive], bal[alive], hi[alive], best[alive], locked[alive]
            if not len(idx):
                break
        x = v[i]
        bal = bal + x
        best = np.maximum(best, x)
        hi = np.maximum(hi, bal)
        locked = locked | (hi > trig)
        fail = bal <= np.where(locked, lock_at, hi - mll)
        p = bal - start
        ok = p >= target
        if cons is not None:
            ok &= best <= cons * p
        ok &= ~fail
        done = fail | ok
        if done.any():
            out[idx[fail]] = OUT_FAIL
            out[idx[ok]] = OUT_PASS
            days[idx[done]] = k + 1
            keep = ~done
            idx, bal, hi, best, locked = idx[keep], bal[keep], hi[keep], best[keep], locked[keep]
        k += 1
    return out, days


def run_starts_loop(v, start_idx, rules=Rules()):
    """Plain-Python reference: the loop of research/eval_short_trades.py (passrate) with the rules as parameters."""
    v = np.asarray(v, float)
    n = len(v)
    lock_at, trig, cons = rules.lock_level, rules.lock_trigger_level, rules.consistency
    out, days = [], []
    for s in start_idx:
        bal, hi, best, locked, o, d = rules.start, rules.start, 0.0, False, OUT_OPEN, 0
        for i in range(s, n):
            d += 1
            bal += v[i]
            best = max(best, v[i])
            hi = max(hi, bal)
            locked = locked or hi > trig
            if bal <= (lock_at if locked else hi - rules.max_loss):
                o = OUT_FAIL
                break
            p = bal - rules.start
            if p >= rules.target and (cons is None or best <= cons * p):
                o = OUT_PASS
                break
        out.append(o)
        days.append(d)
    return np.array(out, np.int8), np.array(days, np.int64)


def _q(a):
    a = np.asarray(a, float)
    if not len(a):
        return (np.nan, np.nan, np.nan)
    return tuple(float(x) for x in np.percentile(a, [25, 50, 75]))


def _rates(out, days):
    n = len(out)
    n_pass, n_fail = int((out == OUT_PASS).sum()), int((out == OUT_FAIL).sum())
    done = n_pass + n_fail
    return dict(pass_rate=n_pass / done if done else np.nan, fail_rate=n_fail / done if done else np.nan,
                open_share=(n - done) / n if n else np.nan, n_starts=n, n_pass=n_pass, n_fail=n_fail,
                n_open=n - done, days_pass=_q(days[out == OUT_PASS]), days_fail=_q(days[out == OUT_FAIL]))


def simulate(daily, rules=Rules(), dates=None, start_from=DEFAULT_FROM, start_to=None, eras=ERAS, outcomes=True):
    """Start an account on every trading day in [start_from, start_to] (and in every era) and run each to pass/fail.
    daily: Series of day P&L indexed by date (the trading calendar), or an array with `dates`.
    Returns dict: pass_rate, fail_rate (of the finished starts), open_share, n_starts/n_pass/n_fail/n_open,
    days_pass / days_fail = (25th pct, median, 75th pct) trading days, eras = {name: same keys}, and
    outcomes (DataFrame per start date: out 'pass'/'fail'/'open', days, end = date of the last day run)."""
    if isinstance(daily, pd.Series):
        dates, v = pd.DatetimeIndex(daily.index), daily.to_numpy(float)
    else:
        dates, v = pd.DatetimeIndex(dates), np.asarray(daily, float)
    if rules.dll is not None:
        v = np.maximum(v, -float(rules.dll))
    lo = pd.Timestamp(start_from) if start_from else dates[0]
    hi = pd.Timestamp(start_to) if start_to else dates[-1]
    win = (dates >= lo) & (dates <= hi)
    sel = win.copy()
    era_masks = {}
    for name, (a, b) in (eras or {}).items():
        era_masks[name] = (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))
        sel |= era_masks[name]
    sidx = np.flatnonzero(sel)
    out_all, days_all = run_starts(v, sidx, rules)
    pos = np.full(len(dates), -1)
    pos[sidx] = np.arange(len(sidx))
    w = pos[np.flatnonzero(win)]
    res = _rates(out_all[w], days_all[w])
    res["eras"] = {}
    for name, mk in era_masks.items():
        e = pos[np.flatnonzero(mk)]
        res["eras"][name] = _rates(out_all[e], days_all[e])
    res["window"] = (lo, hi)
    if outcomes:
        lab = np.array(["fail", "open", "pass"])[out_all[w] + 1]
        si = sidx[w]
        end = dates[np.minimum(si + np.maximum(days_all[w], 1) - 1, len(dates) - 1)]
        res["outcomes"] = pd.DataFrame({"out": lab, "days": days_all[w], "end": end}, index=dates[si])
    return res


# ---------------------------------------------------------------------------------------------------- daily series
@dataclass(frozen=True)
class Params:
    onb_on: bool = True
    onb_micros: int = 1
    onb_stop_mult: float = 1.0            # x the live stop (2 x ATR of 5-min bars): 0.5 = 1 ATR
    onb_cap_pct: float = None             # stop cap, % of price (0.15 = 0.15%); None = no cap
    onb_latest_entry: int = 900           # minute of day: entries at or before (900 = 15:00 = every signal)
    onb_exit: int = 1005                  # minute of day, <= 16:45 (Lucid flattens at 16:45)
    orb_on: bool = True
    orb_micros: int = 1
    orb_stop_mult: float = 1.0            # x the live stop (the first 5-min candle's other end)
    orb_cap_pct: float = None
    orb_exit: int = None                  # minute of day; None = the live 15:59 close
    exp_on: bool = True
    exp_micros: int = 1
    slippage_ticks: int = 1               # per fill (entry and exit), plus $1.00 commission per round trip
    money: str = "today"                  # "today" = rescaled to nq_price, "actual" = as traded
    nq_price: float = P_NOW

    def micros_open(self):
        return (self.onb_micros if self.onb_on else 0) + (self.orb_micros if self.orb_on else 0) + \
            (self.exp_micros if self.exp_on else 0)


def hhmm(minute):
    return f"{int(minute) // 60}:{int(minute) % 60:02d}"


_CAL = None


def calendar():
    """Trading calendar: every date with a live trade (as the research scripts build it)."""
    global _CAL
    if _CAL is None:
        import research_lib as rl
        _CAL = pd.DatetimeIndex(sorted(rl.live_trades().date.unique()))
    return _CAL


@functools.lru_cache(maxsize=512)
def _replay(model, stop_mult, cap_frac, exit_min, slip):
    """research_lib.replay, cached. Returns date, net_pts, bp, usd (+ entry minute of day for overnight_break)."""
    import research_lib as rl
    r = rl.replay(model, stop_mult=stop_mult, stop_cap_frac=cap_frac,
                  exit_time=None if exit_min is None else hhmm(exit_min), slippage_ticks=slip)
    out = pd.DataFrame({"date": pd.DatetimeIndex(r.date), "net_pts": r.net_pts.to_numpy(float),
                        "bp": r.bp.to_numpy(float), "usd": r.usd.to_numpy(float)})
    if model == "overnight_break":
        ent = pd.DatetimeIndex(rl.trade_paths("overnight_break")["ts"][r.path_row.to_numpy(), 0])
        out["entry_min"] = ent.hour * 60 + ent.minute
    return out


def trade_usd(df, slip, money, price):
    """Net $ per trade at 1 micro. 'today': the price move (net points + costs in points) rescaled from the trade's
    own price to `price`, minus the fixed $ costs; at 1 tick this is research/eval_short_trades.py's today()."""
    if money == "actual":
        return df.usd.to_numpy(float)
    cost_pts = 2 * slip * TICK + COMM_USD / USD_PT
    cost_usd = 2 * slip * TICK * USD_PT + COMM_USD
    net, bp = df.net_pts.to_numpy(float), df.bp.to_numpy(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        px = 1e4 * net / bp
        u = ((net + cost_pts) / px) * price * USD_PT - cost_usd
    return np.where(bp != 0, u, -cost_usd)


def _mult(x):
    return None if x is None or abs(float(x) - 1.0) < 1e-12 else round(float(x), 10)


def _cap(pct):
    return None if pct is None or pct <= 0 else round(float(pct) / 100.0, 10)


@functools.lru_cache(maxsize=1024)
def model_daily(model, stop_mult=None, cap_frac=None, exit_min=None, latest_entry=None, slip=1, money="today",
                price=P_NOW):
    """(daily $ at 1 micro, trades per day) for one model over calendar(). Cached by every argument."""
    df = _replay(model, stop_mult, cap_frac, exit_min, slip)
    if model == "overnight_break":
        keep = np.ones(len(df), bool)
        if exit_min is not None:
            keep &= df.entry_min.to_numpy() < exit_min
        if latest_entry is not None:
            keep &= df.entry_min.to_numpy() <= latest_entry
        df = df[keep]
    u = pd.Series(trade_usd(df, slip, money, price), index=df.date.to_numpy())
    cal = calendar()
    g = u.groupby(level=0)
    day = g.sum().reindex(cal, fill_value=0.0).to_numpy(float)
    cnt = g.size().reindex(cal, fill_value=0).to_numpy(np.int64)
    day.setflags(write=False)
    cnt.setflags(write=False)
    return day, cnt


def model_args(p):
    """{model: (micros, model_daily kwargs)} for the models switched on."""
    slip, money, price = int(p.slippage_ticks), p.money, float(p.nq_price)
    out = {}
    if p.onb_on and p.onb_micros > 0:
        out["overnight_break"] = (p.onb_micros, dict(stop_mult=_mult(p.onb_stop_mult), cap_frac=_cap(p.onb_cap_pct),
                                                     exit_min=int(p.onb_exit), latest_entry=int(p.onb_latest_entry),
                                                     slip=slip, money=money, price=price))
    if p.orb_on and p.orb_micros > 0:
        out["opening_range"] = (p.orb_micros, dict(stop_mult=_mult(p.orb_stop_mult), cap_frac=_cap(p.orb_cap_pct),
                                                   exit_min=None if p.orb_exit is None else int(p.orb_exit),
                                                   slip=slip, money=money, price=price))
    if p.exp_on and p.exp_micros > 0:
        out["expiry_fade"] = (p.exp_micros, dict(slip=slip, money=money, price=price))
    return out


def daily_series(p=Params()):
    """(dates, daily $, trades per day) of the models switched on in Params, micros applied."""
    cal = calendar()
    tot = np.zeros(len(cal))
    n = np.zeros(len(cal), np.int64)
    for model, (micros, kw) in model_args(p).items():
        d, c = model_daily(model, **kw)
        tot = tot + d * micros if micros != 1 else tot + d
        n = n + c
    return cal, tot, n


def series_stats(dates, v, n_trades):
    """Stats of a daily $ series as the research scripts compute them (row() in eval_short_trades.py)."""
    if len(v) < 2:
        return dict(net_yr=np.nan, trades_yr=np.nan, day_mean=np.nan, day_sd=np.nan, edge_per_var=np.nan,
                    worst_day=np.nan, best_day=np.nan, max_dd=np.nan, net=np.nan, days=len(v))
    yrs = (dates[-1] - dates[0]).days / 365.25
    cum = np.cumsum(v)
    dd = float((np.maximum.accumulate(np.r_[0.0, cum])[1:] - cum).max())
    mu, sd = float(np.mean(v)), float(np.std(v, ddof=1))
    return dict(net_yr=float(v.sum()) / yrs, trades_yr=float(n_trades.sum()) / yrs, day_mean=mu, day_sd=sd,
                edge_per_var=1e4 * mu / sd ** 2 if sd > 0 else np.nan, worst_day=float(v.min()),
                best_day=float(v.max()), max_dd=dd, net=float(v.sum()), days=len(v))


def evaluate(p=Params(), rules=Rules(), start_from=DEFAULT_FROM, start_to=None, eras=ERAS, outcomes=True):
    """simulate() on daily_series(p), plus series_stats over the start window's days (after any daily loss limit)."""
    dates, v, n = daily_series(p)
    res = simulate(v, rules, dates, start_from, start_to, eras, outcomes)
    lo, hi = res["window"]
    w = (dates >= lo) & (dates <= hi)
    vv = np.maximum(v[w], -float(rules.dll)) if rules.dll is not None else v[w]
    res.update(series_stats(dates[w], vv, n[w]))
    res["micros_open"] = p.micros_open()
    return res


def with_value(p, rules, key, value):
    """(params, rules) with one field set, whichever of the two has it."""
    if key in {f.name for f in fields(Params)}:
        return replace(p, **{key: value}), rules
    if key in {f.name for f in fields(Rules)}:
        return p, replace(rules, **{key: value})
    raise KeyError(key)


def get_value(p, rules, key):
    return getattr(p, key) if hasattr(p, key) else getattr(rules, key)


def sweep(p, rules, key, values, start_from=DEFAULT_FROM, start_to=None, eras=ERAS, should_stop=None):
    """One evaluate() per value of `key` (a Params or Rules field), everything else as given. Returns a DataFrame:
    value, pass_rate, fail_rate, open_share, pass_<era>, days_pass_med/_q1/_q3, worst_day, max_dd, net_yr, trades_yr.
    should_stop(): optional callable checked between values; returns None when it says stop."""
    rows = []
    for val in values:
        if should_stop is not None and should_stop():
            return None
        pp, rr = with_value(p, rules, key, val)
        r = evaluate(pp, rr, start_from, start_to, eras, outcomes=False)
        row = dict(value=val, pass_rate=r["pass_rate"], fail_rate=r["fail_rate"], open_share=r["open_share"],
                   days_pass_q1=r["days_pass"][0], days_pass_med=r["days_pass"][1], days_pass_q3=r["days_pass"][2],
                   n_done=r["n_pass"] + r["n_fail"], worst_day=r["worst_day"], max_dd=r["max_dd"],
                   net_yr=r["net_yr"], trades_yr=r["trades_yr"])
        for name, e in r["eras"].items():
            row[f"pass_{name}"] = e["pass_rate"]
            row[f"days_{name}"] = e["days_pass"][1]
            row[f"done_{name}"] = e["n_pass"] + e["n_fail"]
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------------------------------- presets, specs
PRESETS = {
    "Current live models": (Params(), Rules()),
    "Eval plan: ONB 9:xx entries, cap 0.15%": (Params(onb_cap_pct=0.15, onb_latest_entry=595, orb_on=False,
                                                      exp_on=False), Rules()),
    "ONB + expiry fade": (Params(orb_on=False), Rules()),
}


def _pct(v):
    return "no cap" if v is None else f"{v:.3f}".rstrip("0").rstrip(".") + "%"


def _money(v):
    return "off" if v is None else f"${v:,.0f}"


def _grid(a, b, step):
    k = int(round((b - a) / step))
    return [round(a + j * step, 6) for j in range(k + 1)]


# Every parameter the sandbox shows: label, group, kind ('bool', 'slider', 'choice'), the slider grid (None at the
# end = 'off' / 'no cap' / 'close'), the default sweep values (8-12, all on the grid), a value formatter, a short
# axis label and a tooltip. Numeric sweep x positions: the value itself; None is drawn one step past the end.
SPECS = {
    "onb_on": dict(label="Overnight break", group="onb", kind="bool"),
    "onb_micros": dict(label="Micros", group="onb", kind="slider", grid=list(range(1, 21)),
                       sweep=[1, 2, 3, 4, 5, 6, 8, 10], fmt=lambda v: f"{v}", axis="Overnight break: micros",
                       tip="Contracts (MNQ micros) per overnight-break trade"),
    "onb_stop_mult": dict(label="Stop", group="onb", kind="slider", grid=_grid(0.25, 2.0, 0.125),
                          sweep=[0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.25, 1.5, 2.0],
                          fmt=lambda v: f"{2 * v:g} ATR ({v:g} x live)",
                          axis="Overnight break: stop (ATRs of 5-min bars; live = 2)",
                          tick=lambda v: f"{2 * v:g}",
                          tip="Stop distance as a multiple of the live stop (2 x ATR of 5-minute bars at the signal)"),
    "onb_cap_pct": dict(label="Stop cap", group="onb", kind="slider", grid=_grid(0.05, 0.5, 0.025) + [None],
                        sweep=[0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, None], fmt=_pct,
                        axis="Overnight break: stop cap (% of price)", tick=lambda v: "none" if v is None else f"{v:g}",
                        tip="The stop is never wider than this share of the price (0.15% = about 40 NQ points at "
                            "27,000). Right end = no cap"),
    "onb_latest_entry": dict(label="Latest entry", group="onb", kind="slider", grid=list(range(575, 901, 5)),
                             sweep=[575, 585, 595, 615, 630, 660, 720, 780, 840, 900],
                             fmt=lambda v: hhmm(v) + (" (9:xx only)" if 595 <= v < 600 else
                                                      " (every signal)" if v >= 900 else ""),
                             axis="Overnight break: latest entry (ET)", tick=hhmm,
                             tip="Only take overnight-break entries at or before this time (entries are at 5-minute "
                                 "bar opens, 9:35 to 15:00). 9:55 = the 9 o'clock entries only"),
    "onb_exit": dict(label="Exit at", group="onb", kind="slider", grid=list(range(585, 1006, 5)),
                     sweep=[600, 630, 660, 720, 780, 840, 900, 960, 1005],
                     fmt=lambda v: hhmm(v) + (" (Lucid flat)" if v >= 1005 else ""),
                     axis="Overnight break: exit time (ET)", tick=hhmm,
                     tip="Leave at the close of the 5-minute bar that closes at or after this time; signals at or "
                         "after it are not taken. 16:45 = when Lucid flattens (the live model holds to 17:00)"),
    "orb_on": dict(label="Opening range", group="orb", kind="bool"),
    "orb_micros": dict(label="Micros", group="orb", kind="slider", grid=list(range(1, 21)),
                       sweep=[1, 2, 3, 4, 5, 6, 8, 10], fmt=lambda v: f"{v}", axis="Opening range: micros",
                       tip="Contracts (MNQ micros) per opening-range trade"),
    "orb_stop_mult": dict(label="Stop", group="orb", kind="slider", grid=_grid(0.25, 2.0, 0.125),
                          sweep=[0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.25, 1.5, 2.0],
                          fmt=lambda v: f"{v:g} x first candle", axis="Opening range: stop (x the first candle)",
                          tick=lambda v: f"{v:g}",
                          tip="Stop distance as a multiple of the live stop (the first 5-minute candle's other end)"),
    "orb_cap_pct": dict(label="Stop cap", group="orb", kind="slider", grid=_grid(0.05, 0.5, 0.025) + [None],
                        sweep=[0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, None], fmt=_pct,
                        axis="Opening range: stop cap (% of price)", tick=lambda v: "none" if v is None else f"{v:g}",
                        tip="The stop is never wider than this share of the entry price. Right end = no cap"),
    "orb_exit": dict(label="Exit at", group="orb", kind="slider", grid=list(range(580, 956, 5)) + [None],
                     sweep=[600, 630, 660, 720, 780, 840, 900, None],
                     fmt=lambda v: "15:59 close (live)" if v is None else hhmm(v),
                     axis="Opening range: exit time (ET)", tick=lambda v: "close" if v is None else hhmm(v),
                     tip="Leave at the close of the 1-minute bar ending at this time. Right end = the live 15:59 close"),
    "exp_on": dict(label="Expiry-Friday fade", group="exp", kind="bool"),
    "exp_micros": dict(label="Micros", group="exp", kind="slider", grid=list(range(1, 21)),
                       sweep=[1, 2, 3, 4, 5, 6, 8, 10], fmt=lambda v: f"{v}", axis="Expiry fade: micros",
                       tip="Contracts (MNQ micros) per expiry-fade trade (no stop)"),
    "slippage_ticks": dict(label="Slippage", group="cost", kind="slider", grid=[0, 1, 2, 3, 4],
                           sweep=[0, 1, 2, 3, 4], fmt=lambda v: f"{v} tick{'s' if v != 1 else ''} per fill",
                           axis="Slippage (ticks per fill)", tick=lambda v: f"{v}",
                           tip="Ticks lost on every fill (entry and exit), plus $1.00 commission per round trip"),
    "money": dict(label="Money", group="cost", kind="choice",
                  choices=[("today", "Today's NQ price"), ("actual", "As traded")],
                  tip="Today's price: each trade's points are rescaled to the NQ price below (so 2018 trades count "
                      "at today's size); as traded: the $ actually made at the time"),
    "nq_price": dict(label="NQ price", group="cost", kind="slider", grid=list(range(15000, 35001, 100)),
                     sweep=[15000, 18000, 21000, 24000, 27100, 30000, 33000], fmt=lambda v: f"{v:,.0f}",
                     axis="NQ price used for today's $", tick=lambda v: f"{v / 1000:g}K",
                     tip="Price every trade is rescaled to when money = today's NQ price"),
    "target": dict(label="Profit target", group="rules", kind="slider", grid=list(range(500, 3001, 50)),
                   sweep=[750, 1000, 1250, 1500, 1750, 2000, 2500, 3000], fmt=_money,
                   axis="Profit target ($)", tick=lambda v: f"{v:,.0f}", tip="Profit needed to pass (LucidFlex 25K: $1,250)"),
    "max_loss": dict(label="Max loss", group="rules", kind="slider", grid=list(range(500, 2501, 50)),
                     sweep=[500, 750, 1000, 1250, 1500, 1750, 2000, 2500], fmt=_money,
                     axis="Max loss limit ($)", tick=lambda v: f"{v:,.0f}",
                     tip="Trailing max loss from the highest end-of-day balance (LucidFlex 25K: $1,000); it locks "
                         "at start + $100 once a closing balance exceeds start + max loss + $100"),
    "consistency": dict(label="Consistency", group="rules", kind="slider", grid=_grid(0.2, 1.0, 0.05) + [None],
                        sweep=[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, None],
                        fmt=lambda v: "no rule" if v is None else f"{v:.0%}" + (" (standard)" if abs(v - 0.4) < 1e-9
                                                                                 else " (add-on)" if abs(v - 0.5) < 1e-9
                                                                                 else ""),
                        axis="Consistency rule (best day as % of profit)",
                        tick=lambda v: "none" if v is None else f"{v:.0%}",
                        tip="To pass, the best day may be at most this share of the total profit (Lucid: 40%, 50% "
                            "with the add-on). Right end = no rule"),
    "dll": dict(label="Daily loss limit", group="rules", kind="slider", grid=list(range(200, 1001, 50)) + [None],
                sweep=[200, 300, 400, 500, 600, 700, 800, 1000, None], fmt=_money,
                axis="Daily loss limit ($, soft)", tick=lambda v: "off" if v is None else f"{v:,.0f}",
                tip="Soft daily loss limit: no more trading that day. Approximated by flooring each day's P&L at "
                    "-limit (Lucid 25K: $600 when switched on). Right end = off"),
}
SWEEPABLE = [k for k, s in SPECS.items() if s["kind"] == "slider"]


def _main():
    t0 = time.time()
    calendar()
    model_daily("overnight_break", exit_min=1005, latest_entry=900)
    print(f"load {time.time() - t0:.2f}s")
    for name, (p, r) in PRESETS.items():
        t = time.time()
        res = evaluate(p, r)
        e = res["eras"]
        print(f"{name:42s} pass {res['pass_rate']:.1%}  2018-21 {e['2018-21']['pass_rate']:.1%}  "
              f"2022-26 {e['2022-26']['pass_rate']:.1%}  median days {res['days_pass'][1]:.0f}  "
              f"worst day {res['worst_day']:,.0f}  max DD {res['max_dd']:,.0f}  net/yr {res['net_yr']:,.0f}  "
              f"({time.time() - t:.2f}s)")
    p = PRESETS["Eval plan: ONB 9:xx entries, cap 0.15%"][0]
    for key in ("onb_cap_pct", "onb_stop_mult", "onb_exit", "onb_latest_entry", "target", "dll"):
        t = time.time()
        s = sweep(p, Rules(), key, SPECS[key]["sweep"])
        print(f"sweep {key} ({len(s)} values) {time.time() - t:.2f}s: " +
              ", ".join(f"{SPECS[key]['fmt'](v)} {x:.0%}" for v, x in zip(s.value, s.pass_rate)))


if __name__ == "__main__":
    _main()
