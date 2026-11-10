#!/usr/bin/env python3
"""
P5. Opening-range breakout using the first 1-5 minutes  (literature_report.md section 7, heading "P5.").

Pre-registered specification, implemented without tuning:
  Family A (Zarattini-Aziz first-candle direction), k in {1,3,5}:
    first k-minute candle 09:30..09:30+k (bars 09:30 .. 09:30+k-1); direction = sign(close - open); close == open -> no trade.
    Enter at market at the open of the 09:30+k bar, 1 tick adverse. Resting stop at the candle's opposite extreme,
    filled 1 tick adverse. R = |entry fill - stop|. Target 10R as a limit (needs a 1-tick trade-through, no slippage);
    otherwise exit at the 15:59 bar close, 1 tick adverse.
  Family B (Tsai-style timely ORB, TORB), k in {1,3,5}:
    range = high/low of the first k minutes. From 09:30+k, OCO buy-stop at range high + 1 tick and sell-stop at
    range low - 1 tick, active until 11:00 ET. First fill enters, 1 tick beyond the stop price. Stop at the opposite
    range extreme, 10R target and close exit as in A.
  Exit variant A5T: A5 with the time exit only (no 10R target).
  Cost filter: skip trades with R < 2 x round-trip cost in points (1.6 MES, 2.5 MNQ).
  Roles: A5 = primary (published rule).  1-minute range (A1, B1) = secondary (task); B1, B3 = secondary (report);
         A3, B5, A5T = reported and counted.
  Controls: random-direction bracket at the same decision (entry) time with the same R, the same 10R target and the
            same close exit; and the average of both directions.  Conditioners (reported only): relative volume,
            prior-day NR4/NR7, volatility tercile (VIX fallback = trailing 20-day RV from 5-min RTH returns), gap/ATR.

Costs (fixed): MES $5/pt, MNQ $2/pt, tick 0.25. Market and stop fills 1 tick adverse; limit fills need a 1-tick
trade-through and pay no slippage; $1.00 commission per round trip per micro.  Results per 1 micro.

Intrabar ordering (report section 5.3): when a stop and the entry or target fall inside the same 1-minute bar,
assume the worst case (stop first; a stop-entry's own bar can stop it out but cannot reach the target).

Usage:  cd <project> && PYTHONPATH=./pylib python3 lit_p5_orb.py
Outputs (new files only): lit_p5_orb_trades.csv, lit_p5_orb_summary.txt
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
TRADES_CSV = ROOT / "lit_p5_orb_trades.csv"
SUMMARY_TXT = ROOT / "lit_p5_orb_summary.txt"

TICK = 0.25
COMM = 1.00
MARKETS = {"ES": {"micro": "MES", "ppt": 5.0, "min_R": 1.6},
           "NQ": {"micro": "MNQ", "ppt": 2.0, "min_R": 2.5}}
NSLOT = 390                 # RTH minutes 09:30 .. 15:59 (bar starts)
B_LAST_SLOT = 89            # family B orders live on bars 09:30+k .. 10:59 (cancelled at 11:00)
FULL_EXIT_SLOT = 389        # 15:59 bar close
EARLY_EXIT_SLOT = 209       # 12:59 bar close on early-close days (cash close 13:00; P1's early-close rule)
HOLIDAY_LAST_SLOT = 215     # RTH bars stop at/before 13:05 -> exchange holiday, Globex-only session, no cash open
ABNORMAL_GAP = 6            # >= 5 consecutive missing RTH minutes -> abnormal day (excluded and logged)
TARGET_R = 10.0
BURN = 250                  # trading-day burn-in for expanding tercile cut-offs
NW_LAGS = 5
SEED = 20261108
N_MC = 2000                 # random-direction control replications (distribution of the control)
BIG = 10 ** 9

# (name, family, k, use 10R target, role)
VARIANTS = [
    ("A5", "A", 5, True, "PRIMARY: published rule (5-minute first candle)"),
    ("A1", "A", 1, True, "secondary (task: 1-minute range); counted in report grid"),
    ("B1", "B", 1, True, "secondary (report: closest to Tsai; task: 1-minute range)"),
    ("B3", "B", 3, True, "secondary (report)"),
    ("A3", "A", 3, True, "reported and counted"),
    ("B5", "B", 5, True, "reported and counted"),
    ("A5T", "A", 5, False, "exit variant (counted): A5 with time exit only, no 10R target"),
]

PERIODS = [
    ("FULL 2010-06..2026-11", "2010-01-01", "2026-12-31"),
    ("POST-BURN-IN (after first 250 sessions)", None, "2026-12-31"),
    ("2010-2014", "2010-01-01", "2014-12-31"),
    ("2015-2026 ([25] sample)", "2015-01-01", "2026-12-31"),
    ("2015-2017 ([25] negative stretch)", "2015-01-01", "2017-12-31"),
    ("2016-2023 ([22] in-sample)", "2016-01-01", "2023-12-31"),
    ("2024-2026 (after [22] sample)", "2024-01-01", "2026-12-31"),
]

OUT = []


def say(s=""):
    OUT.append(s)
    print(s, flush=True)


# ----------------------------------------------------------------------------------------------------------------
# statistics helpers
# ----------------------------------------------------------------------------------------------------------------
def nw_t(x, lags=NW_LAGS):
    x = np.asarray(x, float)
    T = len(x)
    if T < 10 or np.allclose(x, x[0]):
        return np.nan
    u = x - x.mean()
    s = u @ u / T
    for j in range(1, lags + 1):
        s += 2.0 * (1.0 - j / (lags + 1.0)) * (u[j:] @ u[:-j]) / T
    if s <= 0:
        return np.nan
    return x.mean() / np.sqrt(s / T)


def prior_mean(values, mask, n):
    """mean of `values` over the last n positions p < i with mask[p] (positions in valid-session order)."""
    pos = np.where(mask & ~np.isnan(values))[0]
    cs = np.concatenate([[0.0], np.cumsum(values[pos])])
    cnt = np.searchsorted(pos, np.arange(len(values)), side="left")
    out = np.full(len(values), np.nan)
    ok = cnt >= n
    out[ok] = (cs[cnt[ok]] - cs[cnt[ok] - n]) / n
    return out


def prior_last(values, mask):
    """value at the last position p < i with mask[p]."""
    pos = np.where(mask)[0]
    cnt = np.searchsorted(pos, np.arange(len(values)), side="left")
    out = np.full(len(values), np.nan)
    ok = cnt >= 1
    out[ok] = values[pos[cnt[ok] - 1]]
    return out


def expanding_tercile(v, burn=BURN, min_hist=100):
    """tercile 1/2/3 of v[i] against cut-offs from all prior non-NaN values; NaN in the first `burn` sessions."""
    out = np.full(len(v), np.nan)
    for i in range(burn, len(v)):
        if np.isnan(v[i]):
            continue
        prior = v[:i]
        prior = prior[~np.isnan(prior)]
        if len(prior) < min_hist:
            continue
        c1, c2 = np.percentile(prior, [100.0 / 3.0, 200.0 / 3.0])
        out[i] = 1 + (v[i] > c1) + (v[i] > c2)
    return out


# ----------------------------------------------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------------------------------------------
def load_market(sym):
    t0 = time.time()
    d = pd.read_csv(DATA / f"{sym}_fut_1m.csv")
    ts = pd.DatetimeIndex(pd.to_datetime(d["ts_event"], utc=True, format="ISO8601")).tz_convert("America/New_York")
    tm = np.asarray(ts.hour * 60 + ts.minute)
    m = (tm >= 570) & (tm < 960)
    r = d.loc[m, ["Open", "High", "Low", "Close", "Volume", "instrument_id"]].reset_index(drop=True)
    dates = pd.Index(ts[m].strftime("%Y-%m-%d"))
    slot = tm[m] - 570
    di, udates = pd.factorize(dates, sort=True)
    nd = len(udates)
    g = {}
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        a = np.full((nd, NSLOT), np.nan)
        a[di, slot] = r[c].to_numpy(float)
        g[c] = a
    inst_bar = np.full((nd, NSLOT), -1, dtype=np.int64)
    inst_bar[di, slot] = r["instrument_id"].to_numpy()
    inst = inst_bar[:, 0].copy()                       # contract traded that day = instrument at the 09:30 bar
    foreign = (inst_bar >= 0) & (inst_bar != inst[:, None])
    n_foreign = int(foreign.sum())
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        g[c][foreign] = np.nan                         # keep only the 09:30 contract's bars (none expected)
    say(f"  {sym}: {len(d):,} 1-min bars, {nd} dates with RTH bars, bars from a non-09:30 contract inside RTH: "
        f"{n_foreign}  (load {time.time() - t0:.1f}s)")
    return pd.to_datetime(np.asarray(udates)), g, inst


def build_sessions(sym, dates, g, inst):
    O, H, L, C, V = g["Open"], g["High"], g["Low"], g["Close"], g["Volume"]
    nd = len(dates)
    present = ~np.isnan(C)
    last = NSLOT - 1 - np.argmax(present[:, ::-1], axis=1)
    first_ok = present[:, 0]
    maxgap = np.zeros(nd, int)
    for i in range(nd):
        idx = np.where(present[i])[0]
        maxgap[i] = int(np.diff(idx).max()) if len(idx) > 1 else 0
    holiday = last <= HOLIDAY_LAST_SLOT
    early = (~holiday) & (last < FULL_EXIT_SLOT)
    full = last == FULL_EXIT_SLOT
    abnormal = (~holiday) & ((maxgap >= ABNORMAL_GAP) | (~first_ok) | (early & ((last < 220) | (last > 240))))
    valid = ~holiday                                   # trading-day calendar (cash session exists)
    trade_ok = valid & ~abnormal
    exit_slot = np.where(full, FULL_EXIT_SLOT, EARLY_EXIT_SLOT)

    # forward-filled close for price levels (minutes without trades carry the last close)
    idx = np.where(present, np.arange(NSLOT)[None, :], 0)
    idx = np.maximum.accumulate(idx, axis=1)
    Cff = C[np.arange(nd)[:, None], idx]

    cols = np.arange(NSLOT)[None, :]
    inrth = cols <= exit_slot[:, None]
    day_open = O[:, 0]
    day_close = Cff[np.arange(nd), exit_slot]
    day_hi = np.nanmax(np.where(inrth, H, np.nan), axis=1)
    day_lo = np.nanmin(np.where(inrth, L, np.nan), axis=1)
    rv = np.full(nd, np.nan)
    for i in range(nd):
        if holiday[i]:
            continue
        p = np.concatenate([[day_open[i]], Cff[i, 4:exit_slot[i] + 1:5]])
        rv[i] = np.sum(np.diff(np.log(p)) ** 2)

    # ---- everything below is in valid-session order (exchange holidays removed) -------------------------------
    v = np.where(valid)[0]
    nv = len(v)
    vfull = full[v] & ~abnormal[v]
    vtrade = trade_ok[v]
    vinst = inst[v]
    same_prev = np.zeros(nv, bool)
    same_prev[1:] = vinst[1:] == vinst[:-1]
    prev_close = np.full(nv, np.nan)
    prev_close[1:] = np.where(same_prev[1:], day_close[v][:-1], np.nan)
    gap = day_open[v] - prev_close
    hi_v, lo_v = day_hi[v], day_lo[v]
    tr = np.where(same_prev, np.maximum(hi_v, prev_close) - np.minimum(lo_v, prev_close), hi_v - lo_v)
    atr14 = prior_mean(tr, full[v], 14)
    rv20 = np.sqrt(252.0 * prior_mean(rv[v], full[v], 20))
    rng_v = hi_v - lo_v
    nr4_s = np.full(nv, np.nan)
    nr7_s = np.full(nv, np.nan)
    fpos = np.where(full[v])[0]
    fr = rng_v[fpos]
    for j in range(len(fpos)):
        if j >= 3:
            nr4_s[fpos[j]] = float(fr[j] <= fr[j - 3:j].min())
        if j >= 6:
            nr7_s[fpos[j]] = float(fr[j] <= fr[j - 6:j].min())
    nr4 = prior_last(nr4_s, full[v])                   # prior full session was NR4 / NR7
    nr7 = prior_last(nr7_s, full[v])
    vol_terc = expanding_tercile(rv20)
    gap_atr = gap / atr14
    gap_terc = expanding_tercile(np.abs(gap_atr))
    relvol, relvol_terc = {}, {}
    for k in (1, 3, 5):
        vk = np.nansum(V[v][:, :k], axis=1)
        rvk = vk / prior_mean(vk, vtrade, 14)
        relvol[k] = rvk
        relvol_terc[k] = expanding_tercile(rvk)
    burn_date = dates[v][BURN] if nv > BURN else dates[v][-1]

    sess = pd.DataFrame({
        "date": dates[v], "di": v, "inst": vinst, "full": full[v], "early": early[v], "abnormal": abnormal[v],
        "trade_ok": vtrade, "exit_slot": exit_slot[v], "same_prev": same_prev, "gap": gap, "atr14": atr14,
        "gap_atr": gap_atr, "gap_terc": gap_terc, "rv20": rv20, "vol_terc": vol_terc, "nr4": nr4, "nr7": nr7,
        "day_open": day_open[v], "day_close": day_close[v],
    })
    for k in (1, 3, 5):
        sess[f"relvol{k}"] = relvol[k]
        sess[f"relvol_terc{k}"] = relvol_terc[k]
    info = {
        "n_dates": nd, "holidays": dates[holiday], "early": dates[early & ~abnormal], "abnormal": dates[abnormal],
        "abnormal_gap": {str(dates[i].date()): int(maxgap[i]) for i in np.where(abnormal)[0]},
        "n_valid": nv, "n_trade_ok": int(vtrade.sum()),
        "roll_days_no_prev_close": int((vtrade & ~same_prev).sum()) - 1,   # minus the very first session
        "first_session": dates[v][0], "burn_date": burn_date,
    }
    return sess, Cff, info


# ----------------------------------------------------------------------------------------------------------------
# trade simulation
# ----------------------------------------------------------------------------------------------------------------
def run_trade(Hd, Ld, Od, close_x, s_e, s_x, d, stop, target, entry_at_open):
    """returns (exit_slot, exit_ref (no slippage), exit_fill, reason) for one bracket on one day."""
    h = Hd[s_e:s_x + 1]
    lo = Ld[s_e:s_x + 1]
    if d > 0:
        sh = lo <= stop
        th = (h >= target + TICK) if target is not None else None
    else:
        sh = h >= stop
        th = (lo <= target - TICK) if target is not None else None
    i_s = int(np.argmax(sh)) if sh.any() else BIG
    i_t = BIG
    if th is not None:
        if not entry_at_open:
            th[0] = False                     # worst case: a stop entry's own bar never reaches the target
        if th.any():
            i_t = int(np.argmax(th))
    if i_t < i_s:                             # stop and target in the same bar -> stop (worst case)
        return s_e + i_t, target, target, "target"
    if i_s < BIG:
        slot = s_e + i_s
        o = Od[slot]
        ref = stop
        if i_s > 0 and not np.isnan(o) and ((d > 0 and o < stop) or (d < 0 and o > stop)):
            ref = o                           # gapped through the stop: fill at the open
        return slot, ref, ref - d * TICK, "stop"
    return s_x, close_x, close_x - d * TICK, "close"


def simulate_variant(sym, var, sess, g, Cff):
    name, fam, k, use_tgt, _ = var
    O, H, L = g["Open"], g["High"], g["Low"]
    ppt, min_R = MARKETS[sym]["ppt"], MARKETS[sym]["min_R"]
    recs = []
    skips = {"doji": 0, "cost_filter": 0, "no_breakout": 0, "missing_bar": 0, "both_sides_same_bar": 0}
    for row in sess.itertuples(index=False):
        if not row.trade_ok:
            continue
        i = row.di
        s_x = row.exit_slot
        hi = np.nanmax(H[i, :k])
        lo = np.nanmin(L[i, :k])
        oc = O[i, 0]
        cc = Cff[i, k - 1]
        tie = False
        if fam == "A":
            if np.isnan(O[i, k]):
                skips["missing_bar"] += 1
                continue
            if cc == oc:
                skips["doji"] += 1
                continue
            d = 1 if cc > oc else -1
            s_e = k
            ref = O[i, k]
            fill = ref + d * TICK
            stop = lo if d > 0 else hi
            R = d * (fill - stop)
            if R < min_R:
                skips["cost_filter"] += 1
                continue
        else:
            if (hi + 2 * TICK) - lo < min_R:     # planned R = range + 2 ticks, known before the orders are placed
                skips["cost_filter"] += 1
                continue
            hw = H[i, k:B_LAST_SLOT + 1]
            lw = L[i, k:B_LAST_SLOT + 1]
            up = hw >= hi + TICK
            dn = lw <= lo - TICK
            iu = int(np.argmax(up)) if up.any() else BIG
            idn = int(np.argmax(dn)) if dn.any() else BIG
            if iu == BIG and idn == BIG:
                skips["no_breakout"] += 1
                continue
            if iu < idn:
                d = 1
            elif idn < iu:
                d = -1
            else:                                 # both stop orders inside one bar: take the side nearer the open
                tie = True
                skips["both_sides_same_bar"] += 1
                o = O[i, k + iu]
                d = 1 if (hi + TICK - o) <= (o - (lo - TICK)) else -1
            s_e = k + (iu if d > 0 else idn)
            o = O[i, s_e]
            ref = max(hi + TICK, o) if d > 0 else min(lo - TICK, o)   # gap through the stop price -> open
            fill = ref + d * TICK
            stop = lo if d > 0 else hi
            R = d * (fill - stop)
        close_x = Cff[i, s_x]
        rec = {"date": row.date, "di": i, "dir": d, "ref": ref, "R": R, "s_e": s_e, "s_x": s_x, "hi": hi, "lo": lo,
               "oc": oc, "cc": cc, "tie": tie, "early": row.early, "inst": row.inst,
               "loose_doji": abs(cc - oc) <= 0.1 * (hi - lo)}
        # both directions of the same bracket (same entry time, same R, same target multiple, same close exit)
        for bd, tag in ((1, "L"), (-1, "S")):
            f = ref + bd * TICK
            st = f - bd * R
            tg = f + bd * TARGET_R * R if use_tgt else None
            xs, xref, xfill, why = run_trade(H[i], L[i], O[i], close_x, s_e, s_x, bd, st, tg, fam == "A")
            rec[f"{tag}_fill"] = f
            rec[f"{tag}_stop"] = st
            rec[f"{tag}_tgt"] = tg if tg is not None else np.nan
            rec[f"{tag}_xs"] = xs
            rec[f"{tag}_xref"] = xref
            rec[f"{tag}_xfill"] = xfill
            rec[f"{tag}_why"] = why
            rec[f"{tag}_gpts"] = bd * (xref - ref)
            rec[f"{tag}_net"] = bd * (xfill - f) * ppt - COMM
        recs.append(rec)
    df = pd.DataFrame(recs)
    # strategy direction picks one side of the bracket
    s = np.where(df["dir"] > 0, "L", "S")
    for c in ["fill", "stop", "tgt", "xs", "xref", "xfill", "why", "gpts", "net"]:
        df[c] = np.where(s == "L", df[f"L_{c}"], df[f"S_{c}"])
    return df, skips


# ----------------------------------------------------------------------------------------------------------------
# reporting helpers
# ----------------------------------------------------------------------------------------------------------------
def trade_frame(df, sym, name, dirs, kind, sess):
    """turn per-day records + a direction vector into a trade table."""
    ppt = MARKETS[sym]["ppt"]
    side = np.where(dirs > 0, "L", "S")
    out = pd.DataFrame({"date": df["date"].dt.strftime("%Y-%m-%d"), "market": sym,
                        "micro": MARKETS[sym]["micro"], "variant": name, "kind": kind,
                        "side": np.where(dirs > 0, "long", "short")})
    pick = lambda c: np.where(side == "L", df[f"L_{c}"], df[f"S_{c}"])  # noqa: E731
    xs = pick("xs").astype(int)
    why = pick("why")
    base = df["date"] + pd.Timedelta(minutes=570)
    out["entry_time"] = (base + pd.to_timedelta(df["s_e"], unit="m")).dt.strftime("%Y-%m-%d %H:%M")
    exit_min = xs + np.where(why == "close", 1, 0)          # close exits happen at the end of the bar
    out["exit_time"] = (base + pd.to_timedelta(exit_min, unit="m")).dt.strftime("%Y-%m-%d %H:%M")
    out["entry_ref"] = df["ref"].to_numpy()
    out["entry_price"] = pick("fill")
    out["exit_ref"] = pick("xref")
    out["exit_price"] = pick("xfill")
    out["exit_reason"] = why
    out["stop_price"] = pick("stop")
    out["target_price"] = pick("tgt")
    out["R_pts"] = df["R"].to_numpy()
    out["gross_pts"] = pick("gpts")
    out["gross_usd"] = out["gross_pts"] * ppt
    out["net_usd"] = pick("net")
    out["net_pts"] = out["net_usd"] / ppt
    out["gross_bp"] = out["gross_pts"] / out["entry_ref"] * 1e4
    out["net_bp"] = out["net_pts"] / out["entry_ref"] * 1e4
    out["gross_R"] = out["gross_pts"] / out["R_pts"]
    out["net_R"] = out["net_pts"] / out["R_pts"]
    out["contract_id"] = df["inst"].to_numpy()
    out["early_close_day"] = df["early"].to_numpy()
    out["range_hi"] = df["hi"].to_numpy()
    out["range_lo"] = df["lo"].to_numpy()
    out["candle_open"] = df["oc"].to_numpy()
    out["candle_close"] = df["cc"].to_numpy()
    out["loose_doji"] = df["loose_doji"].to_numpy()
    out["both_sides_same_bar"] = df["tie"].to_numpy()
    k = int(name[1])
    sx = sess.set_index("date")
    dd = df["date"]
    out["rv20"] = sx.loc[dd, "rv20"].to_numpy()
    out["vol_tercile"] = sx.loc[dd, "vol_terc"].to_numpy()
    out["relvol"] = sx.loc[dd, f"relvol{k}"].to_numpy()
    out["relvol_tercile"] = sx.loc[dd, f"relvol_terc{k}"].to_numpy()
    out["prior_nr4"] = sx.loc[dd, "nr4"].to_numpy()
    out["prior_nr7"] = sx.loc[dd, "nr7"].to_numpy()
    out["gap_atr"] = sx.loc[dd, "gap_atr"].to_numpy()
    out["abs_gap_atr_tercile"] = sx.loc[dd, "gap_terc"].to_numpy()
    return out


def summarize(tr, cal):
    """per-trade and day-level statistics; `cal` = trading-day calendar (DatetimeIndex) of the period."""
    n = len(tr)
    keys = pd.to_datetime(tr["date"]) if n else pd.DatetimeIndex([])
    daily = (tr.groupby(keys)["net_usd"].sum().reindex(cal, fill_value=0.0)) if n else pd.Series(0.0, index=cal)
    dgross = (tr.groupby(keys)["gross_usd"].sum().reindex(cal, fill_value=0.0)) if n else pd.Series(0.0, index=cal)
    res = {"trades": n, "days": len(cal)}
    if n == 0:
        res.update({k: np.nan for k in ["long", "short", "win", "gpts", "gusd", "gbp", "nusd", "nbp", "tot_net",
                                        "tot_gross", "gR", "nR", "cost", "t_net", "t_gross", "sharpe", "p_tgt",
                                        "p_stop", "p_close"]})
        return res
    res.update({
        "long": int((tr.side == "long").sum()), "short": int((tr.side == "short").sum()),
        "win": (tr.net_usd > 0).mean(), "gpts": tr.gross_pts.mean(), "gusd": tr.gross_usd.mean(),
        "gbp": tr.gross_bp.mean(), "nusd": tr.net_usd.mean(), "nbp": tr.net_bp.mean(),
        "tot_net": tr.net_usd.sum(), "tot_gross": tr.gross_usd.sum(), "gR": tr.gross_R.mean(), "nR": tr.net_R.mean(),
        "cost": (tr.gross_usd - tr.net_usd).mean(),
        "t_net": nw_t(daily.to_numpy()), "t_gross": nw_t(dgross.to_numpy()),
        "sharpe": daily.mean() / daily.std() * np.sqrt(252) if daily.std() > 0 else np.nan,
        "p_tgt": (tr.exit_reason == "target").mean(), "p_stop": (tr.exit_reason == "stop").mean(),
        "p_close": (tr.exit_reason == "close").mean(),
    })
    return res


def years_positive(tr, min_trades=20):
    if len(tr) == 0:
        return 0, 0
    y = pd.to_datetime(tr["date"]).dt.year
    g = tr.groupby(y)["net_usd"].agg(["count", "mean"])
    g = g[g["count"] >= min_trades]
    return int((g["mean"] > 0).sum()), int(len(g))


def fmt(x, nd=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "nan"
    return f"{x:,.{nd}f}"


# ----------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------
def main():
    t_start = time.time()
    say("=" * 118)
    say("P5  OPENING-RANGE BREAKOUT USING THE FIRST 1-5 MINUTES   (literature_report.md section 7 'P5.'; "
        "preregistration.md Step 5)")
    say("=" * 118)
    say("Data: Databento CME 1-min bars, continuous front by volume, unadjusted; ES -> MES ($5/pt), NQ -> MNQ ($2/pt).")
    say("Costs: market/stop fills 1 tick adverse; limit target needs a 1-tick trade-through, no slippage; "
        "$1.00 per round trip. Per 1 micro.")
    say("Gross = no slippage, no commission (entry at bar open / stop-order price, exit at stop/target/close price).")
    say("bp per trade = points / entry reference price x 1e4. R-multiples use R = |entry fill - stop|.")
    say("Day-level t = mean daily net $ / Newey-West(5 lags, Bartlett) SE, over ALL trading days of the period "
        "(no-trade days = 0).")
    say("Exchange holidays (RTH bars end <= 13:05: Globex-only session, no cash open) are not trading days. "
        "Early-close days (RTH bars end 13:14/13:15)")
    say("  are traded with the report's early-close rule from P1 (flat at the 12:59 bar close; P5 itself names none, "
        "and all P5 entries are before 11:00).")
    say("Abnormal days (>= 5 consecutive missing RTH minutes) are excluded and logged (report section 5.6).")
    say("Random-direction control: on every strategy trade, the same entry bar and reference price, a coin-flip "
        "direction (1 tick adverse), the same R,")
    say("  stop R away, 10R target (if the variant has one) and the same close exit. For family B the opposite side "
        "enters at market at the breakout price.")
    say("  'Average of both directions' = mean of the always-long and always-short versions of that bracket.")
    say("Family B cost filter uses the planned R (range + 2 ticks), known before the OCO orders are placed; "
        "family A uses R from the actual entry fill.")
    say("")

    markets = {}
    say("SESSION CALENDAR")
    for sym in MARKETS:
        dates, g, inst = load_market(sym)
        sess, Cff, info = build_sessions(sym, dates, g, inst)
        markets[sym] = (dates, g, inst, sess, Cff, info)
        say(f"  {sym}: dates with RTH bars {info['n_dates']}, exchange holidays excluded {len(info['holidays'])}, "
            f"trading days {info['n_valid']} ({info['first_session']:%Y-%m-%d} .. {sess.date.iloc[-1]:%Y-%m-%d}), "
            f"early-close days traded {len(info['early'])}, abnormal days excluded {len(info['abnormal'])}")
        say(f"      abnormal days (max consecutive gap in minutes): {info['abnormal_gap']}")
        say(f"      early-close days: {', '.join(d.strftime('%Y-%m-%d') for d in info['early'])}")
        say(f"      first-day-after-roll sessions without the same contract's prior close (gap/ATR conditioner "
            f"unavailable, trade NOT skipped because the P5 rules do not use the prior close): "
            f"{info['roll_days_no_prev_close']}")
        say(f"      250-session burn-in for tercile cut-offs ends {info['burn_date']:%Y-%m-%d}")
    say("")

    # ------------------------------------------------------------------------------------------------------------
    # STEP 1: R distribution, before any P&L
    # ------------------------------------------------------------------------------------------------------------
    say("=" * 118)
    say("STEP 1 (before any P&L): opening candle / range height R in points, by year and instrument (trading days)")
    say("  'A pass' = share of non-doji days whose family-A R = |entry fill - opposite extreme| >= cost filter; "
        "'B pass' = range + 2 ticks >= filter.")
    say("  Filter: MES 1.6 pts, MNQ 2.5 pts.  Illustrative net $/trade at the literature's +0.147R gross [25]: "
        "0.147 x mean R(pass) x $/pt - cost $")
    say("  (cost $ = 2 ticks + $1.00 = $3.50 MES / $2.00 MNQ; assumes the R-multiple does not depend on R).")
    say("=" * 118)
    step1_rows = []
    for sym, (dates, g, inst, sess, Cff, info) in markets.items():
        ppt, min_R = MARKETS[sym]["ppt"], MARKETS[sym]["min_R"]
        cost_usd = 2 * TICK * ppt + COMM
        O, H, L = g["Open"], g["High"], g["Low"]
        st = sess[sess.trade_ok]
        di = st.di.to_numpy()
        yrs = st.date.dt.year.to_numpy()
        for k in (1, 3, 5):
            hi = np.nanmax(H[di, :k], axis=1)
            lo = np.nanmin(L[di, :k], axis=1)
            rng = hi - lo
            oc = O[di, 0]
            cc = Cff[di, k - 1]
            d = np.sign(cc - oc)
            fill = O[di, k] + d * TICK
            RA = np.where(d > 0, fill - lo, hi - fill)
            passA = (d != 0) & (RA >= min_R)
            passB = (rng + 2 * TICK) >= min_R
            px = oc
            tab = []
            for y in sorted(set(yrs)) + ["2015-2026", "ALL"]:
                if y == "ALL":
                    m = np.ones(len(yrs), bool)
                elif y == "2015-2026":
                    m = yrs >= 2015
                else:
                    m = yrs == y
                r = rng[m]
                ra = RA[m & passA]
                rb = rng[m & passB] + 2 * TICK
                tab.append({"year": y, "days": int(m.sum()), "mean": r.mean(), "median": np.median(r),
                            "p10": np.percentile(r, 10), "p90": np.percentile(r, 90),
                            "mean_bp": np.mean(r / px[m]) * 1e4,
                            "A_pass%": 100 * passA[m].mean(), "A_meanR_pass": ra.mean() if len(ra) else np.nan,
                            "B_pass%": 100 * passB[m].mean(), "B_meanR_pass": rb.mean() if len(rb) else np.nan,
                            "cost/R_A": (2 * TICK + COMM / ppt) / ra.mean() if len(ra) else np.nan,
                            "illus_net$_A": 0.147 * ra.mean() * ppt - cost_usd if len(ra) else np.nan})
                step1_rows.append({"market": sym, "k": k, **tab[-1]})
            say(f"\n{sym} ({MARKETS[sym]['micro']}), k = {k} minute(s)")
            say(pd.DataFrame(tab).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    say("")

    # ------------------------------------------------------------------------------------------------------------
    # P&L
    # ------------------------------------------------------------------------------------------------------------
    all_trades = []
    results = {}           # (sym, name) -> dict
    for sym, (dates, g, inst, sess, Cff, info) in markets.items():
        cal_all = pd.DatetimeIndex(sess.date)
        for vi, var in enumerate(VARIANTS):
            name = var[0]
            t0 = time.time()
            df, skips = simulate_variant(sym, var, sess, g, Cff)
            dirs = df["dir"].to_numpy()
            strat = trade_frame(df, sym, name, dirs, "strategy", sess)
            rng = np.random.default_rng(SEED + 100 * (sym == "NQ") + vi)
            rdir = rng.choice(np.array([1, -1]), size=len(df))
            rand = trade_frame(df, sym, name, rdir, "random_control", sess)
            longb = trade_frame(df, sym, name, np.ones(len(df), int), "always_long", sess)
            shortb = trade_frame(df, sym, name, -np.ones(len(df), int), "always_short", sess)
            # Monte Carlo distribution of the random-direction control's total net $
            mc = np.random.default_rng(SEED + 7 + 100 * (sym == "NQ") + vi).integers(0, 2, size=(N_MC, len(df)))
            Ln = df["L_net"].to_numpy()
            Sn = df["S_net"].to_numpy()
            results[(sym, name)] = {"df": df, "skips": skips, "strat": strat, "rand": rand, "longb": longb,
                                    "shortb": shortb, "mc": mc.astype(np.float32), "Ln": Ln, "Sn": Sn,
                                    "cal": cal_all, "sess": sess, "var": var}
            all_trades.append(strat)
            all_trades.append(rand)
            print(f"  simulated {sym} {name}: {len(df)} trades  skips={skips}  ({time.time() - t0:.1f}s)", flush=True)

    trades = pd.concat(all_trades, ignore_index=True)
    trades.to_csv(TRADES_CSV, index=False, float_format="%.10g")

    def period_mask(sess, p):
        lab, a, b = p
        dd = sess.date
        if a is None:
            a = sess.date.iloc[BURN]
        return (dd >= pd.Timestamp(a)) & (dd <= pd.Timestamp(b))

    def sub(tr, a, b):
        d = pd.to_datetime(tr["date"])
        return tr[(d >= a) & (d <= b)]

    # ------------------------------------------------------------------------------------------------------------
    # headline table
    # ------------------------------------------------------------------------------------------------------------
    headline = []
    say("=" * 118)
    say("RESULTS BY PERIOD  (per 1 micro; gross first, then net; t = day-level Newey-West(5) t of net daily P&L)")
    say("  rand = random-direction control (one fixed seed; same days, entry time, R, target, close exit); "
        "p_rand = share of 2000 random-direction")
    say("  replications with total net >= strategy (one-sided, (1+#)/(1+N));  both = average of always-long and "
        "always-short brackets, $/trade;")
    say("  t_vs_both = NW t of the daily difference strategy - average-of-both-directions.")
    say("=" * 118)
    for p in PERIODS:
        say(f"\n--- {p[0]} ---")
        rows = []
        for (sym, name), R in results.items():
            sess = R["sess"]
            pm = period_mask(sess, p)
            cal = pd.DatetimeIndex(sess.date[pm])
            a, b = cal.min(), cal.max()
            st = sub(R["strat"], a, b)
            rd = sub(R["rand"], a, b)
            s = summarize(st, cal)
            sr = summarize(rd, cal)
            dmask = ((R["df"]["date"] >= a) & (R["df"]["date"] <= b)).to_numpy()
            diffLS = (R["Ln"] - R["Sn"]) * dmask
            tot_mc = (R["Sn"] * dmask).sum() + R["mc"] @ diffLS.astype(np.float32)
            p_rand = (1 + np.sum(tot_mc >= s["tot_net"] - 1e-6)) / (1 + N_MC) if s["trades"] else np.nan
            both = 0.5 * (R["Ln"] + R["Sn"])
            both_d = pd.Series(both[dmask], index=R["df"]["date"][dmask]).reindex(cal, fill_value=0.0)
            st_d = st.groupby(pd.to_datetime(st["date"]))["net_usd"].sum().reindex(cal, fill_value=0.0)
            t_vs_both = nw_t((st_d - both_d).to_numpy())
            yp, yn = years_positive(st)
            rows.append({"mkt": sym, "var": name, "trades": s["trades"], "L/S": f"{s['long']}/{s['short']}",
                         "win%": 100 * s["win"], "g_pts": s["gpts"], "g_bp": s["gbp"], "g$/tr": s["gusd"],
                         "g_R": s["gR"], "n$/tr": s["nusd"], "n_bp": s["nbp"], "n_R": s["nR"],
                         "net$": s["tot_net"], "t_net": s["t_net"], "t_gross": s["t_gross"],
                         "yrs+": f"{yp}/{yn}", "rand_n$/tr": sr["nusd"], "rand_net$": sr["tot_net"],
                         "p_rand": p_rand, "both$/tr": both[dmask].mean() if dmask.any() else np.nan,
                         "t_vs_both": t_vs_both})
            if p[0].startswith("FULL") or (name == "A5" and (p[0].startswith("2015-2026")
                                                             or p[0].startswith("2024-2026"))):
                headline.append({"market": f"{sym} ({MARKETS[sym]['micro']})", "variant": name, "period": p[0],
                                 "trades": int(s["trades"]), "gross_usd": round(float(s["tot_gross"]), 2),
                                 "net_usd": round(float(s["tot_net"]), 2),
                                 "net_per_trade_usd": round(float(s["nusd"]), 3),
                                 "t_stat": round(float(s["t_net"]), 3),
                                 "random_control_net_usd": round(float(sr["tot_net"]), 2),
                                 "years_positive": f"{yp}/{yn}"})
        say(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    # pooled ES + NQ
    say("\n--- POOLED 1 MES + 1 MNQ (day-level sum of both markets) ---")
    prow = []
    for p in PERIODS:
        for var in VARIANTS:
            name = var[0]
            parts, cals = [], []
            for sym in MARKETS:
                R = results[(sym, name)]
                sess = R["sess"]
                cal = pd.DatetimeIndex(sess.date[period_mask(sess, p)])
                cals.append(cal)
                parts.append(sub(R["strat"], cal.min(), cal.max()))
            cal = cals[0].union(cals[1])
            st = pd.concat(parts)
            s = summarize(st, cal)
            yp, yn = years_positive(st, 40)
            prow.append({"period": p[0], "var": name, "trades": s["trades"], "win%": 100 * s["win"],
                         "g$/tr": s["gusd"], "n$/tr": s["nusd"], "net$": s["tot_net"], "t_net": s["t_net"],
                         "yrs+(>=40tr)": f"{yp}/{yn}"})
            if name == "A5" and p[0].startswith("FULL"):
                headline.append({"market": "POOLED (1 MES + 1 MNQ)", "variant": name, "period": p[0],
                                 "trades": int(s["trades"]), "gross_usd": round(float(s["tot_gross"]), 2),
                                 "net_usd": round(float(s["tot_net"]), 2),
                                 "net_per_trade_usd": round(float(s["nusd"]), 3),
                                 "t_stat": round(float(s["t_net"]), 3), "years_positive": f"{yp}/{yn}"})
    say(pd.DataFrame(prow).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    # ------------------------------------------------------------------------------------------------------------
    # per-variant detail
    # ------------------------------------------------------------------------------------------------------------
    for var in VARIANTS:
        name, fam, k, use_tgt, role = var
        for sym in MARKETS:
            R = results[(sym, name)]
            sess, st, rd, lb, sb = R["sess"], R["strat"], R["rand"], R["longb"], R["shortb"]
            cal = pd.DatetimeIndex(sess.date)
            say("\n" + "=" * 118)
            say(f"{sym} ({MARKETS[sym]['micro']})  variant {name}  [{role}]")
            say(f"  family {fam}, k = {k}, target = {'10R limit' if use_tgt else 'none (time exit only)'}; "
                f"skips: {R['skips']}")
            say("=" * 118)
            s = summarize(st, cal)
            say(f"  FULL: trades {s['trades']} (long {s['long']}, short {s['short']}), win {100 * s['win']:.1f}%, "
                f"exits target/stop/close = {100 * s['p_tgt']:.1f}/{100 * s['p_stop']:.1f}/{100 * s['p_close']:.1f}%")
            say(f"        gross {fmt(s['gpts'], 3)} pts = {fmt(s['gbp'], 2)} bp = ${fmt(s['gusd'])} = "
                f"{fmt(s['gR'], 4)}R per trade;  net ${fmt(s['nusd'])} = {fmt(s['nbp'], 2)} bp = {fmt(s['nR'], 4)}R "
                f"per trade; cost ${fmt(s['cost'])}/trade")
            say(f"        total gross ${fmt(s['tot_gross'], 0)}, total net ${fmt(s['tot_net'], 0)}, day-level NW t "
                f"net {fmt(s['t_net'])} (gross {fmt(s['t_gross'])}), annualized Sharpe (daily) {fmt(s['sharpe'])}")
            say(f"        gross edge / cost = {fmt(s['gusd'] / s['cost'] if s['cost'] else np.nan)}  "
                f"(gate: >= 1.5)")

            # per year
            yrows = []
            years = sorted(set(cal.year))
            for y in years:
                ycal = cal[cal.year == y]
                a, b = ycal.min(), ycal.max()
                ys = summarize(sub(st, a, b), ycal)
                yr = summarize(sub(rd, a, b), ycal)
                yrows.append({"year": y, "trades": ys["trades"], "win%": 100 * ys["win"], "g_pts": ys["gpts"],
                              "g$/tr": ys["gusd"], "g_bp": ys["gbp"], "g_R": ys["gR"], "n$/tr": ys["nusd"],
                              "n_bp": ys["nbp"], "net$": ys["tot_net"], "t_net": ys["t_net"],
                              "rand_net$": yr["tot_net"]})
            say("  Per calendar year:")
            say(pd.DataFrame(yrows).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
            yp, yn = years_positive(st)
            say(f"  Years with net mean > 0 (years with >= 20 trades): {yp}/{yn}  (gate: >= 2/3)")

            # legs and controls
            say("  Long / short legs vs the unconditional bracket in the same direction (same days, same R/exits):")
            lrows = []
            for lab, t in [("strategy long leg", st[st.side == "long"]), ("strategy short leg", st[st.side == "short"]),
                           ("always-long bracket (all signal days)", lb), ("always-short bracket (all signal days)", sb),
                           ("random-direction control (seed)", rd)]:
                ss = summarize(t, cal)
                lrows.append({"leg": lab, "trades": ss["trades"], "win%": 100 * ss["win"], "g_pts": ss["gpts"],
                              "g_bp": ss["gbp"], "g$/tr": ss["gusd"], "g_R": ss["gR"], "n$/tr": ss["nusd"],
                              "net$": ss["tot_net"], "t_net": ss["t_net"]})
            say(pd.DataFrame(lrows).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
            # unconditional drift from the entry bar open to the close exit on every trading day
            di = sess[sess.trade_ok].di.to_numpy()
            xs = sess[sess.trade_ok].exit_slot.to_numpy()
            g = markets[sym][1]
            Cff = markets[sym][4]
            drift = Cff[di, xs] - g["Open"][di, k]
            say(f"  Unconditional drift 09:3{k}-open -> close exit, all trading days: mean {np.nanmean(drift):.3f} "
                f"pts, {np.nanmean(drift / g['Open'][di, k]) * 1e4:.2f} bp (long-only, no stop, gross)")
            tot_mc = R["Sn"].sum() + R["mc"] @ (R["Ln"] - R["Sn"]).astype(np.float32)
            say(f"  Random-direction control distribution (2000 seeds, total net $): mean {tot_mc.mean():,.0f}, "
                f"p5 {np.percentile(tot_mc, 5):,.0f}, p95 {np.percentile(tot_mc, 95):,.0f}; strategy "
                f"{s['tot_net']:,.0f}; p = {(1 + np.sum(tot_mc >= s['tot_net'] - 1e-6)) / (1 + N_MC):.4f}")

            # volatility terciles and conditioners (reported, not used for selection)
            say("  Conditioners (reported only; terciles from expanding history after the 250-session burn-in; "
                "NaN = burn-in/unavailable):")
            crow = []
            gsign = np.sign(st["gap_atr"].to_numpy())
            aligned = np.where(np.isnan(gsign), "n/a", np.where(gsign == np.where(st.side == "long", 1, -1),
                                                                 "with gap", "against gap/zero"))
            groups = [("vol tercile (RV20 fallback for VIX)", st["vol_tercile"]),
                      (f"relative volume first {k} min tercile", st["relvol_tercile"]),
                      ("prior full day NR4", st["prior_nr4"]), ("prior full day NR7", st["prior_nr7"]),
                      ("|gap|/ATR14 tercile", st["abs_gap_atr_tercile"]),
                      ("trade direction vs gap", pd.Series(aligned, index=st.index))]
            for lab, key in groups:
                kk = key.astype(object).where(key.notna(), "n/a")
                for val, t in st.groupby(kk.to_numpy()):
                    ss = summarize(t, cal)
                    crow.append({"conditioner": lab, "group": val, "trades": ss["trades"], "win%": 100 * ss["win"],
                                 "g_R": ss["gR"], "g$/tr": ss["gusd"], "n$/tr": ss["nusd"], "net$": ss["tot_net"],
                                 "t_net": ss["t_net"]})
            say(pd.DataFrame(crow).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
            if fam == "A":
                nd_ = st[~st.loose_doji.astype(bool)]
                ss = summarize(nd_, cal)
                say(f"  Diagnostic, loose doji (|C-O| <= 10% of range) removed: trades {ss['trades']}, "
                    f"g$/tr {fmt(ss['gusd'])}, n$/tr {fmt(ss['nusd'])}, net ${fmt(ss['tot_net'], 0)}, "
                    f"t {fmt(ss['t_net'])}  (diagnostic only)")
            ee = st[st.early_close_day.astype(bool)]
            say(f"  Early-close-day trades: {len(ee)}, net ${ee.net_usd.sum():,.0f}; "
                f"both-sides-in-one-bar (family B, worst case applied): {int(st.both_sides_same_bar.sum())}")

    # ------------------------------------------------------------------------------------------------------------
    # acceptance gates for the primary and the 1-minute secondaries
    # ------------------------------------------------------------------------------------------------------------
    say("\n" + "=" * 118)
    say("ACCEPTANCE GATES (common protocol), FULL period. Single pre-registered replication: t >= 2 'promising'; "
        "searched: t >= 3.")
    say("=" * 118)
    grow = []
    for var in VARIANTS:
        name = var[0]
        for sym in MARKETS:
            R = results[(sym, name)]
            cal = pd.DatetimeIndex(R["sess"].date)
            s = summarize(R["strat"], cal)
            yp, yn = years_positive(R["strat"])
            tot_mc = R["Sn"].sum() + R["mc"] @ (R["Ln"] - R["Sn"]).astype(np.float32)
            pr = (1 + np.sum(tot_mc >= s["tot_net"] - 1e-6)) / (1 + N_MC)
            grow.append({"mkt": sym, "var": name, "t_net": s["t_net"], "t>=2": s["t_net"] >= 2,
                         "yrs+": f"{yp}/{yn}", "yrs>=2/3": yn > 0 and yp >= 2 * yn / 3,
                         "gross/cost": s["gusd"] / s["cost"], "g/c>=1.5": s["gusd"] / s["cost"] >= 1.5,
                         "p_vs_random": pr, "beats_random(p<.05)": pr < 0.05})
    say(pd.DataFrame(grow).to_string(index=False, float_format=lambda x: f"{x:,.3f}"))
    say("\nHEADLINE (per 1 micro; t = day-level Newey-West(5) t of net daily P&L)")
    say(pd.DataFrame(headline).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    say("\nNot computed here: SPA, DSR (need the full trial ledger), PBO (not defined for a single pre-registered "
        "replication), FOMC-cycle split (P4c).")
    say(f"Trial count for this family: 7 (report grid A1/A3/A5/B1/B3/B5 + A5T) x 2 markets; preregistration.md "
        f"logged P5 as 2 trials.")
    say(f"\nTrades CSV: {TRADES_CSV.name} (kind = strategy | random_control; exit_time of close exits = bar end).")
    say(f"Runtime {time.time() - t_start:.0f}s")
    SUMMARY_TXT.write_text("\n".join(OUT) + "\n")
    import json
    print("HEADLINE_JSON " + json.dumps(headline))


if __name__ == "__main__":
    sys.exit(main())
