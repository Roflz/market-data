"""
v2/eval_sim.py - the judge: per-trade table -> sized trades -> daily P&L by Lucid trading day -> LucidFlex 25K eval
outcomes from EVERY start day (prop_sim.run_starts, the same engine as the GUI's Eval sandbox).

TRADE TABLE (one row per trade, money per ONE micro):
    market    'NQ' / 'ES' / 'YM' (MNQ / MES / MYM)
    t_entry   entry time (New York, tz-naive)          t_exit   exit time (end of the exit minute / bar)
    session   Lucid trading day = walkforward.session_label(t_entry) (the 18:00-17:00 session; added if missing)
    risk_usd  entry-to-stop distance in $ per micro (nothing else added)
    pnl_usd   net $ per micro after costs ($1 commission + 1 tick each way, +1 tick on stop fills)
  Every trade must be flat by 16:45 of its own session (so t_exit is in the session of t_entry) and must end before
  the locked holdout (walkforward.HOLDOUT_SESSION_START = 2025-06-30 18:00 ET); size_trades() refuses anything else.

SIZING   size_trades(trades, policy, max_micros=20, dll=600)
    policy ('fixed', k): k micros per trade;  ('risk', B): micros = floor(B / risk_usd), skipped if 0.
    Trades are taken in t_entry order. Open micros never exceed max_micros: a trade gets min(wanted, 20 - open) micros
    (skipped if that is 0). Daily loss limit: a trade is not taken once the day's REALIZED P&L (trades of the same
    session that exited at or before its entry) is <= -dll. Only information known at the entry time is used.
DAILY    daily_pnl(sized, calendar, dll=600): sum of micros x pnl by session over the full trading calendar (days
    without trades = 0, they still count as trading days), each day floored at -dll (prop_sim's soft daily limit).
EVAL     eval_daily(daily, consistencies=(0.40, 0.50), windows=WINDOWS) -> one row per (consistency, window):
    an account started on every trading day of the window runs forward (to the end of the pre-holdout data) with
    prop_sim.Rules(dll=600, consistency=c) (start 25,000, target 1,250, $1,000 EOD trailing drawdown locking at
    25,100 once a close exceeds 26,100). Columns: n_starts, pass_pct / fail_pct / open_pct (of all starts),
    pass_rate (passes / finished, prop_sim's definition), days_pass_p25 / median / p75, days_fail_median,
    within_5 / within_10 / within_20 (% of starts passed within N trading days, over the starts that have at least N
    trading days of data left).
    evaluate(trades, policies, calendar) = all of the above for several sizing policies (one long table).
REPORT   pnl_report(trades): net $ per micro-trade by year 2013-2025H1 and for the windows 2018+, 2022+, 2010-20,
    2021-25H1, all, all without the top 10 days, all without 2025H1 (the research rules' standard view).

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 v2/test_eval_sim.py
"""
import heapq
import os
from dataclasses import replace

import numpy as np
import pandas as pd

import prop_sim as ps
import walkforward as wf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DATA_END = pd.Timestamp("2025-06-30")                     # last pre-holdout session (trade date)
WINDOWS = {"2013+": ("2013-01-01", "2025-06-30"), "2018+": ("2018-01-01", "2025-06-30"),
           "2022+": ("2022-01-01", "2025-06-30")}
POLICIES = [("fixed", 1), ("fixed", 2), ("fixed", 3), ("fixed", 5),
            ("risk", 100), ("risk", 150), ("risk", 250), ("risk", 400)]
RULES = ps.Rules(dll=600.0, consistency=0.40, max_micros=20)
WITHIN = (5, 10, 20)
REQUIRED = ["market", "t_entry", "t_exit", "risk_usd", "pnl_usd"]


def policy_name(policy):
    kind, x = policy
    return f"{int(x)} micro{'s' if x != 1 else ''}" if kind == "fixed" else f"${int(x)} risk"


# ---------------------------------------------------------------------------------------------------- input checks
def prepare(trades):
    """Validate a trade table and return a copy sorted by (t_entry, original order) with a `session` column."""
    miss = [c for c in REQUIRED if c not in trades.columns]
    if miss:
        raise ValueError(f"trade table lacks columns {miss}")
    t = trades.copy()
    t["t_entry"] = pd.DatetimeIndex(t["t_entry"])
    t["t_exit"] = pd.DatetimeIndex(t["t_exit"])
    if "session" not in t.columns:
        t["session"] = wf.session_label(t["t_entry"])
    t["session"] = pd.DatetimeIndex(t["session"]).normalize()
    if len(t):
        if (t.t_exit < t.t_entry).any():
            raise ValueError("t_exit before t_entry")
        if (t.t_exit > wf.HOLDOUT_SESSION_START).any() or (t.t_entry >= wf.HOLDOUT_SESSION_START).any():
            raise ValueError("trade table reaches into the locked holdout (2025-06-30 18:00 ET on)")
        if (wf.session_label(t.t_exit - pd.Timedelta(seconds=1)) != wf.session_label(t.t_entry)).any():
            raise ValueError("a trade crosses the 16:45-18:00 daily close (must be flat by 16:45)")
        tod = (t.t_exit - t.t_exit.dt.normalize()) / pd.Timedelta(minutes=1)
        if ((tod > 16 * 60 + 45) & (tod < 18 * 60)).any():
            raise ValueError("a trade exits after 16:45 (Lucid: flat during 16:45-18:00)")
        if not np.isfinite(t.pnl_usd.to_numpy(float)).all():
            raise ValueError("non-finite pnl_usd")
    t["_ord"] = np.arange(len(t))
    return t.sort_values(["t_entry", "_ord"], kind="stable").drop(columns="_ord")


# ---------------------------------------------------------------------------------------------------- sizing
def size_trades(trades, policy, max_micros=20, dll=600.0, checked=False):
    """Add micros (0 = not taken), skip ('' / 'size0' / 'cap' / 'dll') and pnl_total (= micros x pnl_usd).
    See the module docstring. `checked`=True skips prepare() when the table is already prepared."""
    t = trades if checked else prepare(trades)
    kind, x = policy
    te = t.t_entry.to_numpy("datetime64[ns]").view(np.int64)
    tx = t.t_exit.to_numpy("datetime64[ns]").view(np.int64)
    day = t.session.to_numpy("datetime64[ns]").view(np.int64)
    pnl = t.pnl_usd.to_numpy(float)
    risk = t.risk_usd.to_numpy(float)
    if kind == "fixed":
        want = np.full(len(t), int(x), np.int64)
    elif kind == "risk":
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.floor(float(x) / risk + 1e-9)
        want = np.where(np.isfinite(q) & (risk > 0), q, 0).astype(np.int64)
    else:
        raise ValueError(policy)
    micros = np.zeros(len(t), np.int64)
    skip = np.full(len(t), "", object)
    heap, realized, open_m = [], {}, 0
    te_l, tx_l, day_l, pnl_l, want_l = te.tolist(), tx.tolist(), day.tolist(), pnl.tolist(), want.tolist()
    for k in range(len(t)):
        now = te_l[k]
        while heap and heap[0][0] <= now:
            _, m, p, dy = heapq.heappop(heap)
            open_m -= m
            realized[dy] = realized.get(dy, 0.0) + p
        if dll is not None and realized.get(day_l[k], 0.0) <= -dll:
            skip[k] = "dll"
            continue
        w = want_l[k]
        if w <= 0:
            skip[k] = "size0"
            continue
        m = min(w, max_micros - open_m)
        if m <= 0:
            skip[k] = "cap"
            continue
        micros[k] = m
        open_m += m
        heapq.heappush(heap, (tx_l[k], m, m * pnl_l[k], day_l[k]))
    out = t.copy()
    out["micros"] = micros
    out["skip"] = skip
    out["pnl_total"] = micros * pnl
    return out


def build_calendar(index):
    """Trading calendar (session days, ascending) from bar start times, cut before the locked holdout."""
    idx = pd.DatetimeIndex(index)
    idx = idx[idx < wf.HOLDOUT_SESSION_START]
    return pd.DatetimeIndex(np.unique(wf.session_label(idx)))


def load_calendar(markets):
    """Union of the saved calendars v2/out/calendar_<sym>.csv (written by luck_baseline.py)."""
    cal = None
    for s in ([markets] if isinstance(markets, str) else markets):
        c = pd.DatetimeIndex(pd.read_csv(os.path.join(OUT, f"calendar_{s}.csv"), parse_dates=["session"]).session)
        cal = c if cal is None else cal.union(c)
    return cal


def daily_pnl(sized, calendar, dll=600.0):
    """Series of day P&L over the calendar (0 on days without trades), floored at -dll."""
    cal = pd.DatetimeIndex(calendar)
    g = sized.groupby("session")["pnl_total"].sum()
    extra = g.index.difference(cal)
    if len(extra):
        raise ValueError(f"{len(extra)} trade sessions are not in the calendar (e.g. {extra[0].date()})")
    v = g.reindex(cal, fill_value=0.0).astype(float)
    if dll is not None:
        v = v.clip(lower=-float(dll))
    return v


# ---------------------------------------------------------------------------------------------------- eval
def eval_daily(daily, consistencies=(0.40, 0.50), windows=WINDOWS, rules=RULES, within=WITHIN):
    """Eval outcomes from every start day of each window (see module docstring). daily: Series by session."""
    dates = pd.DatetimeIndex(daily.index)
    v = daily.to_numpy(float)
    if rules.dll is not None:
        v = np.maximum(v, -float(rules.dll))
    n = len(v)
    masks = {w: (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b)) for w, (a, b) in windows.items()}
    anyw = np.zeros(n, bool)
    for m in masks.values():
        anyw |= m
    sidx = np.flatnonzero(anyw)
    left = n - sidx                                          # trading days of data from the start day on (incl.)
    rows = []
    for c in consistencies:
        out, days = ps.run_starts(v, sidx, replace(rules, consistency=c))
        for w, m in masks.items():
            sel = m[sidx]
            o, d, lf = out[sel], days[sel], left[sel]
            ns = len(o)
            npass, nfail = int((o == ps.OUT_PASS).sum()), int((o == ps.OUT_FAIL).sum())
            dp = d[o == ps.OUT_PASS]
            r = dict(consistency=c, window=w, n_starts=ns,
                     pass_pct=100 * npass / ns if ns else np.nan, fail_pct=100 * nfail / ns if ns else np.nan,
                     open_pct=100 * (ns - npass - nfail) / ns if ns else np.nan,
                     pass_rate=100 * npass / (npass + nfail) if npass + nfail else np.nan,
                     days_pass_p25=np.percentile(dp, 25) if len(dp) else np.nan,
                     days_pass_median=np.median(dp) if len(dp) else np.nan,
                     days_pass_p75=np.percentile(dp, 75) if len(dp) else np.nan,
                     days_fail_median=np.median(d[o == ps.OUT_FAIL]) if nfail else np.nan)
            for N in within:
                ok = lf >= N
                r[f"within_{N}"] = 100 * ((o[ok] == ps.OUT_PASS) & (d[ok] <= N)).mean() if ok.any() else np.nan
            rows.append(r)
    return pd.DataFrame(rows)


def evaluate(trades, calendar, policies=POLICIES, consistencies=(0.40, 0.50), windows=WINDOWS, rules=RULES):
    """eval_daily for every sizing policy. Adds policy, trades_taken, micros_mean, skipped by reason, $/day mean."""
    t = prepare(trades)
    rows = []
    for pol in policies:
        s = size_trades(t, pol, max_micros=rules.max_micros, dll=rules.dll, checked=True)
        dly = daily_pnl(s, calendar, rules.dll)
        e = eval_daily(dly, consistencies, windows, rules)
        tk = s.micros > 0
        e.insert(0, "policy", policy_name(pol))
        e["trades_taken"] = int(tk.sum())
        e["micros_mean"] = float(s.micros[tk].mean()) if tk.any() else 0.0
        for why in ("size0", "cap", "dll"):
            e[f"skip_{why}"] = int((s.skip == why).sum())
        e["usd_day_mean"] = float(dly.mean())
        rows.append(e)
    return pd.concat(rows, ignore_index=True)


# ---------------------------------------------------------------------------------------------------- $ report
def pnl_report(trades, pnl="pnl_usd", top_days=10):
    """Net $ per micro-trade by year and window (one row each): n, usd_trade, total, t_stat."""
    t = trades.copy()
    if "session" not in t.columns:
        t["session"] = wf.session_label(t["t_entry"])
    s = pd.DatetimeIndex(t["session"])
    t["_y"] = s.year
    p = t[pnl].astype(float)

    def row(name, m):
        x = p[m]
        n = len(x)
        return dict(span=name, n=n, usd_trade=x.mean() if n else np.nan, total=x.sum(),
                    t_stat=x.mean() / (x.std() / np.sqrt(n)) if n > 2 and x.std() > 0 else np.nan)
    rows = [row(str(y), (t._y == y).to_numpy()) for y in range(2013, 2026)]
    rows[-1]["span"] = "2025H1"
    day = p.groupby(s).sum()
    top = day.sort_values(ascending=False).index[:top_days]
    spans = {"2018+": s >= "2018-01-01", "2022+": s >= "2022-01-01", "2010-20": s < "2021-01-01",
             "2021-25H1": s >= "2021-01-01", "all": np.ones(len(t), bool),
             f"all w/o top {top_days} days": ~s.isin(top), "all w/o 2025H1": s < "2025-01-01"}
    rows += [row(k, np.asarray(m)) for k, m in spans.items()]
    return pd.DataFrame(rows)
