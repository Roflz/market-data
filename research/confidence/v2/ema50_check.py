"""
v2/ema50_check.py - is the 60-min EMA 50 pullback (trigger_scan rule ema50_pb) a real edge, NQ's / the trend's drift,
or noise?  Per market (NQ, ES, YM = MNQ, MES, MYM).

SETUP (long; short = mirror), everything known at the CLOSE of signal bar t, entry at the open of t+1:
    trend  EMA20 > EMA50 and EMA50 higher than 5 bars ago (the rule's own, looser trend: EMA8 not required)
    touch  low <= EMA50 + tol * R20   (tol 0 = trigger_scan; +0.25 = near miss allowed; -0.25 = must pierce)
    close  close > EMA50 and close > open
    stop   1 tick beyond the lowest low of the last `lookback` bars, at least 1 R20 from the close (trigger_scan's rule)
  tol 0 / lookback 5 reproduces trigger_scan.detect's ema50_pb events and stops exactly (checked on the real data).

UNIVERSE  every eligible bar (labels.eligible, warm-up done: same base as trigger_scan) BOTH ways, labelled with three
  exits on the 1-minute path (v2/lucid.py installed: flat 16:45-18:00):
    hold   'stop only, hold to 16:45'   (labels.label_entries with no target / no bar limit)
    3R     '3R target, hold to 16:45'   (same call, 3R column)
    cross  'EMA 8 crosses EMA 20 against the trade -> out at the next bar's open', entry stop kept, flat by 16:45
           (exit_study.simulate with rule_exit; its exit time: stop/time exits = the hold exit's minute, which is the
           same event; cross exits = end of the first minute of the next bar)
  Costs $1 + 1 tick each way, +1 tick on stop fills. Saved: out/ema50_universe_<sym>_<tf>_lb<k>.parquet.

CONTROLS (per setup variant, exit and side; null = draws of one matched pool trade per setup trade, 200 draws):
  A 'trend drift'  pool = every bar IN THE SAME TREND (trend condition, no pullback), matched on side, session year,
                    entry hour and stop size (risk_usd quintile within the session year) -> what being with the
                    trend at the same hours, with the same stop rule and exit, earns.
  B 'random'       pool = every eligible bar (no trend), same matching -> random entries at the same hours.
  The setup's own bars are left out of both pools. edge = setup $/trade - null mean; p = share of null draws whose
  mean >= the setup's mean. Reported by year 2013..2025H1 and for 2018+, 2022+, 2010-20, 2021-25H1, all, all w/o the
  top 10 days (the setup's best days, removed from the setup AND its matched draws), all w/o 2025H1.
GRID (all logged to out/trials.csv, module 'v2-ema50_check'): tf 30/60/120 x lookback 3/5/8 x touch tol 0/+0.25/-0.25
  x exit hold/cross/3R x side long/short/both x hours all / evening (entries 18:00-02:00 ET).
EVAL  base setup (60 min, lookback 5, tol 0) per side / hours / exit through eval_sim at 1/2/3 micros and $150/$250
  risk, against EVAL_DRAWS matched draws of each null (same count, side, year, hour and stop size = matched frequency).
Holdout: bars and 1-minute data are cut at walkforward.HOLDOUT_SESSION_START before anything is computed.

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 -u \
      v2/ema50_check.py [NQ ES YM] --phase label|analyze|eval|report|all   (label ~5 min, analyze ~4, eval ~16)
"""
import argparse
import gc
import json
import os
import time
import warnings
import zlib

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import eval_sim as es
import features as fe
import labels as lb
import lucid
import signals as sg
import walkforward as wf

lucid.install()                                        # flat 16:45-18:00 (see v2/lucid.py)

OUT = es.OUT
MARKETS = ("NQ", "ES", "YM")
TFS = (30, 60, 120)
LOOKBACKS = (3, 5, 8)
TOLS = {"tol0": 0.0, "tolp": 0.25, "tolm": -0.25}
TOL_NAME = {"tol0": "low <= EMA50", "tolp": "low <= EMA50 + 0.25 R20", "tolm": "low <= EMA50 - 0.25 R20"}
EXITS = {"hold": "stop only, hold to 16:45", "cross": "EMA 8/20 cross", "3R": "3R target, hold to 16:45"}
SIDES = {"long": (1,), "short": (-1,), "both": (1, -1)}
EVE_HOURS = (18, 19, 20, 21, 22, 23, 0, 1)
HOURS = ("all", "eve")
BASE = dict(tf=60, lookback=5, tol="tol0")
HOLD_R, HOLD_BARS = 1e6, 10 ** 6
N_DRAWS = 200
EVAL_DRAWS = 30
EVAL_POLICIES = [("fixed", 1), ("fixed", 2), ("fixed", 3), ("risk", 150), ("risk", 250)]
_MIN = pd.Timedelta(minutes=1)


# ------------------------------------------------------------------------------------------------ setup
def bar_signals(b, ctx, tick, lookback=5, tf=None):
    """Per-bar arrays known at the bar's close. base: warm-up done (stop lookback, R20, EMA50 and its 5-bar lag) and
    enterable (labels.eligible). For d in (1, -1): trend[d], pen[d] = (low - EMA50) / R20 oriented with the trade
    (<= 0: touched), close_ok[d] (close beyond EMA50 and a bar closing with the trade), stop[d]."""
    n = len(b)
    O, H, L, C = (b[c].to_numpy(np.float64) for c in "OHLC")
    run = b.run.to_numpy()
    e20, e50 = ctx["ema20"].to_numpy(np.float64), ctx["ema50"].to_numpy(np.float64)
    R = fe.r20(b, tick)
    tf = lb.infer_tf(b) if tf is None else tf
    ok, _ = lb.eligible(b, tf)
    e50_5 = np.full(n, np.nan)
    e50_5[5:] = e50[:-5]
    e50_5 = np.where(fe._run_ok(run, 5), e50_5, np.nan)
    lo = pd.Series(L).rolling(lookback).min().to_numpy()
    hi = pd.Series(H).rolling(lookback).max().to_numpy()
    full = fe._run_ok(run, lookback - 1) & np.isfinite(R) & np.isfinite(e50) & np.isfinite(e50_5)
    S = dict(base=ok & full, R=R, trend={}, pen={}, close_ok={}, stop={})
    with np.errstate(invalid="ignore"):
        for d in (1, -1):
            o, c = d * O, d * C
            l = np.where(d > 0, L, -H)
            a20, a50, a50_5 = d * e20, d * e50, d * e50_5
            S["trend"][d] = (a20 > a50) & (a50 > a50_5)
            S["pen"][d] = (l - a50) / R
            S["close_ok"][d] = (c > a50) & (c > o)
            S["stop"][d] = np.minimum(lo - tick, C - R) if d > 0 else np.maximum(hi + tick, C + R)
    return S


def setup_mask(S, d, tol=0.0):
    """ema50 pullback on each bar for side d with touch tolerance tol (in R20)."""
    with np.errstate(invalid="ignore"):
        return S["base"] & S["trend"][d] & (S["pen"][d] <= tol) & S["close_ok"][d]


def universe_events(b, ctx, tick, lookback=5, tf=None):
    """Every base bar both ways: DataFrame t, i, d, stop, trend, tol0, tolp, tolm (setup flags)."""
    S = bar_signals(b, ctx, tick, lookback, tf)
    i = np.flatnonzero(S["base"])
    parts = []
    for d in (1, -1):
        p = pd.DataFrame({"i": i, "d": np.int8(d), "stop": S["stop"][d][i], "trend": S["trend"][d][i]})
        for k, tol in TOLS.items():
            p[k] = setup_mask(S, d, tol)[i]
        parts.append(p)
    ev = pd.concat(parts, ignore_index=True).sort_values(["i", "d"], kind="stable").reset_index(drop=True)
    ev.insert(0, "t", b.index[ev.i.to_numpy()])
    return ev


def ema_cross(ctx):
    """(exit_long[j], exit_short[j]): EMA 8 crosses EMA 20 against the trade at bar j's close (exit_study's rule)."""
    diff = ctx["ema8"].to_numpy(np.float64) - ctx["ema20"].to_numpy(np.float64)
    prev = np.r_[np.nan, diff[:-1]]
    with np.errstate(invalid="ignore"):
        return (diff < 0) & (prev >= 0), (diff > 0) & (prev <= 0)


# ------------------------------------------------------------------------------------------------ labels
def label_universe(sym, tf, b, ctx, m1, ev):
    """Three exits for every event (see module docstring). Returns the enterable events with t_entry, session, year,
    hour, risk_usd, past_stop, pnl_/t_exit_/kind_ for hold, 3R, cross."""
    import exit_study as xs                                               # noqa: PLC0415
    L = lb.label_entries(sym, tf, b, ev, target_R=(3.0, HOLD_R), max_bars=HOLD_BARS, m1=m1)
    hk = f"{HOLD_R:g}"
    res, sel = xs.simulate(sym, tf, b, ctx, ev, m1, None, None, False, None, "day", max_bars=HOLD_BARS,
                           rule_exit=ema_cross(ctx))
    if not np.array_equal(ev.index.to_numpy()[sel], L.index.to_numpy()):
        raise RuntimeError("label_entries and exit_study.simulate kept different events")
    out = L[["t", "i", "d", "stop", "trend", *TOLS, "t_entry", "risk_usd", "past_stop"]].copy()
    out["pnl_hold"] = L[f"pnl_usd_{hk}"].to_numpy()
    out["t_exit_hold"] = L[f"t_end_{hk}"].to_numpy()
    out["kind_hold"] = L[f"exit_kind_{hk}"].to_numpy()
    out["pnl_3R"] = L["pnl_usd_3"].to_numpy()
    out["t_exit_3R"] = L["t_end_3"].to_numpy()
    out["kind_3R"] = L["exit_kind_3"].to_numpy()
    kc = res.kind.to_numpy()
    pc = res.pnl.to_numpy()
    same = kc != 3
    gap = np.nanmax(np.abs(pc[same] - out.pnl_hold.to_numpy()[same])) if same.any() else 0.0
    if gap > 1e-6:
        raise RuntimeError(f"cross exit's stop/time exits differ from the hold exit by {gap}")
    first = lb.map_1m(m1, b, tf)[0]
    j_next = out.i.to_numpy() + 1 + res.bars_held.to_numpy()          # e + held = the bar after the signal bar j
    j_next = np.minimum(j_next, len(b) - 1)
    nx = first[j_next]
    t_cross = np.where(nx >= 0, (m1.index[np.maximum(nx, 0)] + _MIN).to_numpy(),
                       (b.index[j_next - 1] + pd.Timedelta(minutes=tf)).to_numpy())
    out["pnl_cross"] = pc
    out["t_exit_cross"] = np.where(same, out.t_exit_hold.to_numpy(), t_cross)
    out["kind_cross"] = np.where(kc == 3, "cross", out.kind_hold.to_numpy())
    out["bars_cross"] = res.bars_held.to_numpy()
    out["session"] = wf.session_label(out.t_entry)
    out["year"] = pd.DatetimeIndex(out.session).year
    out["hour"] = pd.DatetimeIndex(out.t_entry).hour
    out.insert(0, "market", sym)
    out.insert(1, "tf", tf)
    return out.reset_index(drop=True)


def add_risk_bucket(U, q=5):
    """risk_usd quintile within each session year (over the whole universe, both sides); scode = session code."""
    U = U.copy()
    U["scode"] = pd.factorize(U.session)[0]
    U["rb"] = U.groupby("year").risk_usd.transform(
        lambda s: pd.qcut(s.rank(method="first"), q, labels=False)).astype(np.int8)
    return U


def universe_path(sym, tf, k):
    return os.path.join(OUT, f"ema50_universe_{sym}_{tf}_lb{k}.parquet")


# ------------------------------------------------------------------------------------------------ matching
def matched_draws(setup, pool, n_draws=N_DRAWS, seed=0, keys=("d", "year", "hour", "rb")):
    """For each setup row, n_draws random rows of `pool` (with replacement) from the cell with the same keys; if that
    cell is empty, the last key is dropped, and so on (to ("d",) at the least). Returns (idx (n_setup, n_draws) of
    positional rows of pool, level (n_setup,) = number of keys matched)."""
    keys = list(keys)
    rng = np.random.default_rng(seed)
    n = len(setup)
    idx = np.full((n, n_draws), -1, np.int64)
    level = np.zeros(n, np.int8)
    todo = np.arange(n)
    for nk in range(len(keys), 0, -1):
        if not len(todo):
            break
        kk = keys[:nk]
        pk = pd.MultiIndex.from_frame(pool[kk].reset_index(drop=True))
        codes, uniq = pd.factorize(pk)
        order = np.argsort(codes, kind="stable")
        cnt = np.bincount(codes, minlength=len(uniq))
        start = np.r_[0, np.cumsum(cnt)[:-1]]
        sk = pd.MultiIndex.from_frame(setup[kk].iloc[todo].reset_index(drop=True))
        pos = uniq.get_indexer(sk)
        hit = pos >= 0
        rows = todo[hit]
        if len(rows):
            c = cnt[pos[hit]]
            u = rng.random((len(rows), n_draws))
            pick = start[pos[hit]][:, None] + np.floor(u * c[:, None]).astype(np.int64)
            idx[rows] = order[pick]
            level[rows] = nk
        todo = todo[~hit]
    if len(todo):
        raise ValueError("setup rows with no pool row of the same side")
    return idx, level


def spans(session, top_days_mask=None):
    """{span name: boolean mask} - the research rules' standard view."""
    s = pd.DatetimeIndex(session)
    y = s.year
    out = {str(yy): (y == yy) for yy in range(2013, 2025)}
    out["2025H1"] = y == 2025
    out.update({"2018+": s >= "2018-01-01", "2022+": s >= "2022-01-01", "2010-20": s < "2021-01-01",
                "2021-25H1": s >= "2021-01-01", "all": np.ones(len(s), bool)})
    if top_days_mask is not None:
        out["all w/o top 10 days"] = ~top_days_mask
    out["all w/o 2025H1"] = s < "2025-01-01"
    return {k: np.asarray(v) for k, v in out.items()}


def top_days(session, pnl, k=10):
    day = pd.Series(pnl).groupby(pd.DatetimeIndex(session)).sum()
    top = day.sort_values(ascending=False).index[:k]
    return pd.DatetimeIndex(session).isin(top)


def trimmed_means(pnl, sess_codes, k=10):
    """Per column q of pnl (n, D): mean after removing the rows of that column's own k best days (sessions by summed
    pnl). sess_codes (n, D) int session codes."""
    n, D = pnl.shape
    out = np.empty(D)
    for q in range(D):
        u, inv = np.unique(sess_codes[:, q], return_inverse=True)
        day = np.bincount(inv, weights=pnl[:, q], minlength=len(u))
        top = np.argsort(-day, kind="stable")[:k]
        keep = ~np.isin(inv, top)
        out[q] = pnl[keep, q].mean() if keep.any() else np.nan
    return out


def cluster_t(x, groups):
    """t-stat of mean(x) with a cluster-robust (by group, e.g. week) standard error: trades of the same week share
    market moves, so the plain t (and the iid null draws' p) overstate significance."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return np.nan
    u, inv = np.unique(groups, return_inverse=True)
    G = len(u)
    if G < 3:
        return np.nan
    mu = x.mean()
    e = np.bincount(inv, weights=x - mu, minlength=G)
    se = np.sqrt((e ** 2).sum() * G / (G - 1)) / n
    return mu / se if se > 0 else np.nan


def compare(setup, pnl_col, nulls, span_names=None):
    """Setup $/trade vs each null by span. nulls: {name: (pool_pnl array, idx matrix, pool session codes)}.
    One row per span. For 'all w/o top 10 days' the setup loses its 10 best days and EACH null draw loses its own 10
    best days (a like-for-like trimmed mean)."""
    p = setup[pnl_col].to_numpy(float)
    wk = pd.factorize(pd.DatetimeIndex(setup.session).to_period("W"))[0]
    td = top_days(setup.session, p)
    sp = spans(setup.session, td)
    rows = []
    for name, m in sp.items():
        if span_names is not None and name not in span_names:
            continue
        n = int(m.sum())
        r = dict(span=name, n=n, usd_trade=p[m].mean() if n else np.nan,
                 t_stat=p[m].mean() / (p[m].std() / np.sqrt(n)) if n > 2 and p[m].std() > 0 else np.nan)
        for nm, (pp, idx, ps) in nulls.items():
            if n:
                if name == "all w/o top 10 days":
                    draws = trimmed_means(pp[idx], ps[idx])
                else:
                    draws = pp[idx[m]].mean(axis=0)
                r[f"{nm}_usd"] = draws.mean()
                r[f"{nm}_edge"] = r["usd_trade"] - draws.mean()
                r[f"{nm}_p"] = float((draws >= r["usd_trade"]).mean())
                r[f"{nm}_tc"] = np.nan if name == "all w/o top 10 days" else \
                    cluster_t(p[m] - pp[idx[m]].mean(axis=1), wk[m])
            else:
                r[f"{nm}_usd"] = r[f"{nm}_edge"] = r[f"{nm}_p"] = r[f"{nm}_tc"] = np.nan
        rows.append(r)
    return pd.DataFrame(rows)


def select(U, tol, side, hours):
    m = U[tol].to_numpy() & U.d.isin(SIDES[side]).to_numpy()
    if hours == "eve":
        m &= U.hour.isin(EVE_HOURS).to_numpy()
    return m


def pools(U, setup_flag):
    """(trend pool mask, random pool mask): the setup's own bars excluded."""
    own = U[setup_flag].to_numpy()
    return U.trend.to_numpy() & ~own, ~own


def config_draws(U, tol, side, hours, seed=0, n_draws=N_DRAWS):
    """Setup rows of one variant and their matched null draws (the same draws serve every exit)."""
    S = U[select(U, tol, side, hours)].reset_index(drop=True)
    pA, pB = pools(U, tol)
    PA, PB = U[pA].reset_index(drop=True), U[pB].reset_index(drop=True)
    iA, lA = matched_draws(S, PA, n_draws, seed)
    iB, lB = matched_draws(S, PB, n_draws, seed + 1)
    return dict(S=S, PA=PA, iA=iA, lA=lA, PB=PB, iB=iB, lB=lB)


def config_tables(D, exit_name):
    """compare() of one variant (config_draws output) under one exit."""
    col = f"pnl_{exit_name}"
    T = compare(D["S"], col, {"trend": (D["PA"][col].to_numpy(float), D["iA"], D["PA"].scode.to_numpy()),
                              "random": (D["PB"][col].to_numpy(float), D["iB"], D["PB"].scode.to_numpy())})
    T["match_full_A"] = (D["lA"] == 4).mean() if len(D["lA"]) else np.nan
    T["match_full_B"] = (D["lB"] == 4).mean() if len(D["lB"]) else np.nan
    return T


# ------------------------------------------------------------------------------------------------ checks
def check_vs_trigger_scan(b, ctx, tick, tf):
    """ema50 setup at tol 0 / lookback 5 == trigger_scan.detect's ema50_pb events and stops."""
    import trigger_scan as ts                                             # noqa: PLC0415
    ev = ts.detect(b, ctx, tick, tf)
    ev = ev[ev.rule == "ema50_pb"]
    S = bar_signals(b, ctx, tick, 5, tf)
    mine = []
    for d in (1, -1):
        i = np.flatnonzero(setup_mask(S, d, 0.0))
        mine.append(pd.DataFrame({"i": i, "d": d, "stop": S["stop"][d][i]}))
    mine = pd.concat(mine).sort_values(["i", "d"]).reset_index(drop=True)
    ref = ev[["i", "d", "stop"]].sort_values(["i", "d"]).reset_index(drop=True)
    same = len(mine) == len(ref) and (mine[["i", "d"]].to_numpy() == ref[["i", "d"]].to_numpy()).all()
    gap = float(np.max(np.abs(mine.stop.to_numpy() - ref.stop.to_numpy()))) if same and len(ref) else np.nan
    return same, gap, len(ref)


def truncation_check(b, tick, tf, start, length=3000, cuts=(700, 1500, 2999), lookback=5):
    """Cut the data after bar t (recomputing the context from the cut bars): the setup flags and stops at or before t
    must not change. Returns the number of mismatching values (0 = pass)."""
    bb = b.iloc[start:start + length].copy()
    bb.attrs.clear()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        full = universe_events(bb, sg.context(bb, tick=tick), tick, lookback, tf)
    bad = 0
    for cut in cuts:
        bc = bb.iloc[:cut + 1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            part = universe_events(bc, sg.context(bc, tick=tick), tick, lookback, tf)
        f = full[full.i < cut]          # the last bar of a cut is never 'eligible' (no next bar): compare before it
        p = part[part.i < cut]
        if len(f) != len(p):
            bad += abs(len(f) - len(p)) + 1
            continue
        for c in ("i", "d", "trend", *TOLS):
            bad += int((f[c].to_numpy() != p[c].to_numpy()).sum())
        bad += int((np.abs(f.stop.to_numpy() - p.stop.to_numpy()) > 1e-9).sum())
    return bad


def hand_walk(row, m1, b, tf, tick, usd, cost, exit_name, cross=None):
    """Independent minute-by-minute re-walk of one universe row from the raw 1-minute bars (pure Python loop)."""
    i, d, stop = int(row.i), int(row.d), float(row.stop)
    _, forced = lb.eligible(b, tf)
    inst = b.inst.iloc[i]
    t_entry = b.index[i + 1]
    end = b.index[forced[i]] + pd.Timedelta(minutes=tf)
    mm = m1[(m1.index >= t_entry) & (m1.index < end) & (m1.inst == inst)]
    entry = mm.O.iloc[0]
    if d * (entry - stop) < 0:
        return -cost, "past"
    risk = d * (entry - stop)
    tgt = entry + d * 3 * risk if exit_name == "3R" else None
    bar_pos = {ts: k for k, ts in enumerate(b.index) if i < k <= forced[i] and b.inst.iloc[k] == inst} \
        if exit_name == "cross" else {}
    rows = list(mm.itertuples())
    for q, r in enumerate(rows):
        if (d > 0 and r.L <= stop) or (d < 0 and r.H >= stop):
            x = (min(r.O, stop) - tick) if d > 0 else (max(r.O, stop) + tick)
            return d * (x - entry) * usd - cost, "stop"
        if tgt is not None and ((d > 0 and r.H >= tgt + tick) or (d < 0 and r.L <= tgt - tick)):
            return d * (tgt - entry) * usd - cost, "target"
        if exit_name == "cross":
            j = bar_pos.get(r.Index.floor(f"{tf}min"))
            last_of_bar = q + 1 == len(rows) or rows[q + 1].Index.floor(f"{tf}min") != r.Index.floor(f"{tf}min")
            if j is not None and last_of_bar and j < forced[i]:
                sig = cross[0][j] if d > 0 else cross[1][j]
                if sig and q + 1 < len(rows):
                    return d * (rows[q + 1].O - entry) * usd - cost, "cross"
    return d * (rows[-1].C - entry) * usd - cost, "time"


def hand_check(sym, tf, U, m1, b, ctx, n=8, seed=5):
    spec = sg.SPEC[sym]
    cr = ema_cross(ctx)
    rng = np.random.default_rng(seed)
    S = U[U.tol0]
    rows = []
    for ex in EXITS:
        for k in rng.choice(len(S), size=min(n, len(S)), replace=False):
            r = S.iloc[k]
            p, why = hand_walk(r, m1, b, tf, spec["tick"], spec["usd"], spec["cost"], ex, cr)
            rows.append(dict(market=sym, tf=tf, exit=ex, t=r.t, d=int(r.d), stop=r.stop, label_pnl=r[f"pnl_{ex}"],
                             hand_pnl=p, hand_kind=why, label_kind=r[f"kind_{ex}"]))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ phases
def phase_label(markets, relabel=False):
    log = []
    for sym in markets:
        tick = sg.SPEC[sym]["tick"]
        m1 = None
        for tf in TFS:
            if not relabel and all(os.path.exists(universe_path(sym, tf, k)) for k in LOOKBACKS):
                print(f"{sym} {tf}m: universes exist, skipped", flush=True)
                continue
            if m1 is None:
                m1 = lb.load_1m(sym)
                m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
            t0 = time.time()
            b, ctx = fe._load(sym, tf)
            keep = b.index < wf.HOLDOUT_SESSION_START
            b, ctx = b.loc[keep], ctx.loc[keep]
            same, gap, nref = check_vs_trigger_scan(b, ctx, tick, tf)
            trunc = truncation_check(b, tick, tf, start=len(b) // 2)
            msg = f"{sym} {tf}m: == trigger_scan ema50_pb: {same} (stop gap {gap}, {nref:,} events); truncation " \
                  f"mismatches: {trunc}"
            print(msg, flush=True)
            log.append(msg)
            if not same or trunc:
                raise RuntimeError(msg)
            for k in LOOKBACKS:
                t1 = time.time()
                ev = universe_events(b, ctx, tick, k, tf)
                U = label_universe(sym, tf, b, ctx, m1, ev)
                U.to_parquet(universe_path(sym, tf, k), compression="zstd")
                msg = f"   lb{k}: {len(U):,} universe rows, setups tol0 {int(U.tol0.sum()):,} [{time.time() - t1:.0f}s]"
                print(msg, flush=True)
                log.append(msg)
                if tf == BASE["tf"] and k == BASE["lookback"]:
                    hc = hand_check(sym, tf, U, m1, b, ctx)
                    hc.to_csv(os.path.join(OUT, f"ema50_handcheck_{sym}.csv"), index=False)
                    msg = f"   hand check ({len(hc)} trades): max |label - hand| {np.abs(hc.label_pnl - hc.hand_pnl).max():.4f}"
                    print(msg, flush=True)
                    log.append(msg)
                del U, ev; gc.collect()
            fe.clear_cache(); del b, ctx; gc.collect()
            print(f"{sym} {tf}m done [{time.time() - t0:.0f}s]", flush=True)
        del m1; gc.collect()
    with open(os.path.join(OUT, "ema50_label.log"), "a") as f:
        f.write("\n".join(log) + "\n")


def load_universe(sym, tf, k):
    return add_risk_bucket(pd.read_parquet(universe_path(sym, tf, k)))


def phase_analyze(markets, log_trials=True):
    import run_pipeline as rp                                             # noqa: PLC0415
    grid, years = [], []
    for sym in markets:
        for tf in TFS:
            for k in LOOKBACKS:
                t0 = time.time()
                U = load_universe(sym, tf, k)
                n_yr = U.year.nunique()
                for tol in TOLS:
                    for side in SIDES:
                        for hours in HOURS:
                            D = config_draws(U, tol, side, hours,
                                             seed=zlib.crc32(f"{sym}{tf}{k}{tol}{side}{hours}".encode()))
                            for ex in EXITS:
                                T = config_tables(D, ex)
                                key = dict(market=sym, tf=tf, lookback=k, tol=tol, side=side, hours=hours, exit=ex)
                                is_base = tf == BASE["tf"] and k == BASE["lookback"] and tol == BASE["tol"]
                                if is_base:
                                    years.append(T.assign(**key))
                                a = T.set_index("span")
                                g = dict(key, n=int(a.loc["all", "n"]), per_year=a.loc["all", "n"] / n_yr)
                                for sp, tag in (("all", ""), ("2010-20", "_10_20"), ("2021-25H1", "_21_25"),
                                                ("all w/o top 10 days", "_notop10"), ("all w/o 2025H1", "_no2025"),
                                                ("2018+", "_2018"), ("2022+", "_2022")):
                                    if sp not in a.index:
                                        continue
                                    g[f"usd{tag}"] = a.loc[sp, "usd_trade"]
                                    for nm in ("trend", "random"):
                                        g[f"edge_{nm}{tag}"] = a.loc[sp, f"{nm}_edge"]
                                        g[f"p_{nm}{tag}"] = a.loc[sp, f"{nm}_p"]
                                        g[f"tc_{nm}{tag}"] = a.loc[sp, f"{nm}_tc"]
                                yr = a.loc[[str(y) for y in range(2013, 2025)] + ["2025H1"]]
                                yr = yr[yr.n > 0]
                                g["years_pos"] = f"{int((yr.usd_trade > 0).sum())}/{len(yr)}"
                                g["years_beat_trend"] = f"{int((yr.trend_edge > 0).sum())}/{len(yr)}"
                                g["t_stat"] = a.loc["all", "t_stat"]
                                g["match_full_A"] = a["match_full_A"].iloc[0]
                                grid.append(g)
                                if log_trials:
                                    rp.log_trial(module="v2-ema50_check", scope=f"{sym}{tf}", model="rule ema50_pb",
                                                 target=EXITS[ex], oos_rows=g["n"],
                                                 oos_usd_per_trade=round(float(g["usd"]), 2),
                                                 baseline_usd_per_trade=round(float(g["usd"] - g["edge_trend"]), 2),
                                                 parameters=json.dumps(dict(tf=tf, stop_lookback=k, touch=TOL_NAME[tol],
                                                                            side=side, hours=hours)),
                                                 note=f"no model; baseline = trend-drift null (side/year/hour/stop "
                                                      f"matched); edge_trend {g['edge_trend']:.2f} p {g['p_trend']:.3f}"
                                                      f"; edge_random {g['edge_random']:.2f}")
                del U; gc.collect()
                print(f"{sym} {tf}m lb{k} analysed [{time.time() - t0:.0f}s]", flush=True)
        pd.DataFrame(grid).to_csv(os.path.join(OUT, "ema50_grid.csv"), index=False)
        pd.concat(years, ignore_index=True).to_csv(os.path.join(OUT, "ema50_years.csv"), index=False)
    return pd.DataFrame(grid)


def eval_table(trades, cal):
    e = es.evaluate(trades, cal, policies=EVAL_POLICIES)
    return e[["policy", "consistency", "window", "n_starts", "pass_pct", "fail_pct", "pass_rate", "days_pass_median",
              "within_5", "within_10", "within_20", "trades_taken", "micros_mean"]]


def to_trades(R, ex):
    return pd.DataFrame({"market": R.market.to_numpy(), "t_entry": R.t_entry.to_numpy(),
                         "t_exit": R[f"t_exit_{ex}"].to_numpy(), "session": R.session.to_numpy(),
                         "risk_usd": R.risk_usd.to_numpy(), "pnl_usd": R[f"pnl_{ex}"].to_numpy()})


def phase_eval(markets, n_draws=EVAL_DRAWS):
    keys = ["policy", "consistency", "window"]
    mets = ["pass_pct", "within_5", "within_10", "within_20", "days_pass_median"]
    rows = []
    for sym in markets:
        cal = es.load_calendar(sym)
        U = load_universe(sym, BASE["tf"], BASE["lookback"])
        for side in ("long", "short", "both"):
            for hours in HOURS:
                D = config_draws(U, BASE["tol"], side, hours, seed=11, n_draws=n_draws)
                S, PA, iA, PB, iB = D["S"], D["PA"], D["iA"], D["PB"], D["iB"]
                for ex in EXITS:
                    t0 = time.time()
                    E = eval_table(to_trades(S, ex), cal).set_index(keys)
                    for nm, (P, idx) in (("trend", (PA, iA)), ("random", (PB, iB))):
                        DD = pd.concat([eval_table(to_trades(P.iloc[idx[:, q]], ex), cal).assign(draw=q)
                                       for q in range(idx.shape[1])])
                        g = DD.groupby(keys)
                        for mt in mets:
                            E[f"{nm}_{mt}_mean"] = g[mt].mean()
                            E[f"{nm}_{mt}_p90"] = g[mt].quantile(0.9)
                        sp = DD.set_index(keys)
                        for mt in ("pass_pct", "within_10"):
                            E[f"{nm}_{mt}_rank"] = (sp[mt] < E[mt].reindex(sp.index)).groupby(keys).mean()
                    E = E.reset_index()
                    E.insert(0, "exit", ex); E.insert(0, "hours", hours); E.insert(0, "side", side)
                    E.insert(0, "market", sym)
                    E["n_setup_trades"] = len(S)
                    E["usd_trade"] = S[f"pnl_{ex}"].mean()
                    rows.append(E)
                    pd.concat(rows, ignore_index=True).to_csv(os.path.join(OUT, "ema50_eval.csv"), index=False)
                    print(f"{sym} {side} {hours} {ex}: {len(S)} trades, eval + {2 * n_draws} null draws "
                          f"[{time.time() - t0:.0f}s]", flush=True)
        del U; gc.collect()
    return pd.concat(rows, ignore_index=True)


def phase_report():
    """Evidence table per market (base setup, hold exit) + robustness counts + eval vs matched luck -> ema50_evidence.csv"""
    G = pd.read_csv(os.path.join(OUT, "ema50_grid.csv"))
    E = pd.read_csv(os.path.join(OUT, "ema50_eval.csv"))
    rows = []
    for sym in MARKETS:
        for side in ("long", "short", "both"):
            for hours in HOURS:
                for ex in EXITS:
                    g = G[(G.market == sym) & (G.side == side) & (G.hours == hours) & (G.exit == ex)]
                    b = g[(g.tf == BASE["tf"]) & (g.lookback == BASE["lookback"]) & (g.tol == BASE["tol"])].iloc[0]
                    r = {k: b[k] for k in ("market", "side", "hours", "exit", "n", "per_year", "usd", "edge_trend",
                                           "tc_trend", "p_trend", "edge_random", "tc_random", "usd_10_20",
                                           "edge_trend_10_20", "usd_21_25", "edge_trend_21_25", "usd_notop10",
                                           "edge_trend_notop10", "p_trend_notop10", "usd_no2025",
                                           "edge_trend_no2025", "usd_2018", "usd_2022", "years_pos",
                                           "years_beat_trend")}
                    r["variants_edge_pos"] = f"{int((g.edge_trend > 0).sum())}/{len(g)}"
                    r["variants_edge_pos_both_halves"] = \
                        f"{int(((g.edge_trend_10_20 > 0) & (g.edge_trend_21_25 > 0)).sum())}/{len(g)}"
                    r["variants_tc_gt2"] = f"{int((g.tc_trend > 2).sum())}/{len(g)}"
                    r["variants_60m_edge_pos"] = f"{int((g[g.tf == 60].edge_trend > 0).sum())}/{int((g.tf == 60).sum())}"
                    e = E[(E.market == sym) & (E.side == side) & (E.hours == hours) & (E.exit == ex) &
                          (E.window == "2013+") & (E.consistency == 0.4)]
                    for _, q in e.iterrows():
                        pol = q.policy.replace(" ", "")
                        r[f"pass_{pol}"] = q.pass_pct
                        r[f"w10_{pol}"] = q.within_10
                        r[f"w10_trend_p90_{pol}"] = q.trend_within_10_p90
                        r[f"w10_random_p90_{pol}"] = q.random_within_10_p90
                        r[f"w10_rank_trend_{pol}"] = q.trend_within_10_rank
                        r[f"w10_rank_random_{pol}"] = q.random_within_10_rank
                        r[f"pass_rank_trend_{pol}"] = q.trend_pass_pct_rank
                    rows.append(r)
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(OUT, "ema50_evidence.csv"), index=False)
    return R


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("markets", nargs="*", default=list(MARKETS))
    ap.add_argument("--phase", default="all", choices=["label", "analyze", "eval", "report", "all"])
    ap.add_argument("--relabel", action="store_true")
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    if a.phase in ("label", "all"):
        phase_label(a.markets, a.relabel)
    if a.phase in ("analyze", "all"):
        phase_analyze(a.markets, log_trials=not a.no_log)
    if a.phase in ("eval", "all"):
        phase_eval(a.markets)
    if a.phase in ("report", "all"):
        phase_report()
    print("done", flush=True)
