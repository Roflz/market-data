#!/usr/bin/env python3
"""
Pre-registered test (PREREG.md, sha256 b42e85c4...335b): rebalancing-pressure signal traded at 16:05 ET, held to
16:05 next NYSE day. Primary P (trailing-252 decile reversal), variant A (z-scaled 0-3 MNQ), variant B (long only).
Run: cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this file>
Reads project data read-only; writes only into OUT.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

PROJ = "/run/media/roflz/Disk 2/_/market_data"
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/next/rebal"
OLD_SIG = ("/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/"
           "caltests2/B/t12_signal.csv")
os.chdir(PROJ)
NY = "America/New_York"
MULT = {"NQ": 2.0, "ES": 5.0}
SIDE = {"NQ": 1.00, "ES": 1.75}          # $ per contract per side, 1 tick
SIDE2 = {"NQ": 1.50, "ES": 3.00}         # 2 ticks
SEED, NREP, WIN = 12345, 1000, 252
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------------------------------------------------------- calendar & daily closes
D = {s: pd.read_pickle(f"data/daily_sessions_{s}.pkl").sort_index() for s in ("ES", "NQ")}
CAL = D["ES"].index[D["ES"].cash_day]
assert CAL.equals(D["NQ"].index[D["NQ"].cash_day])
N = len(CAL)
EARLY = D["ES"].early_close.reindex(CAL).fillna(False).values.astype(bool)
log(f"cash days {N}: {CAL[0].date()}..{CAL[-1].date()}; early-close days {EARLY.sum()}")


# ---------------------------------------------------------------- ZN 16:00 price (same as test 12)
def zn_daily():
    pk = f"{OUT}/zn_daily.pkl"
    if os.path.exists(pk):
        return pd.read_pickle(pk)
    z = pd.read_csv("data/ZN_fut_1h.csv", usecols=["ts_event", "Open", "Close", "instrument_id"])
    z.index = pd.to_datetime(z.ts_event, utc=True).dt.tz_convert(NY)
    z = z.drop(columns="ts_event")
    z = z[~z.index.duplicated()].sort_index()
    roll = z.instrument_id.ne(z.instrument_id.shift()) & z.instrument_id.shift().notna()
    jump = (z.Open - z.Close.shift()).where(roll, 0.0)
    z["aC"] = z.Close + jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    zt = z.reset_index().rename(columns={"ts_event": "ts"})
    zt = zt.rename(columns={zt.columns[0]: "ts"})
    tgt = pd.DataFrame({"tgt": (CAL + pd.Timedelta(hours=15)).tz_localize(NY), "day": CAL})
    zd = pd.merge_asof(tgt.sort_values("tgt"), zt[["ts", "Close", "aC"]].sort_values("ts"),
                       left_on="tgt", right_on="ts", direction="backward").set_index("day")
    zd.to_pickle(pk)
    return zd


zd = zn_daily()
assert zd.Close.notna().all()
rZN = np.r_[np.nan, (zd.aC.values[1:] - zd.aC.values[:-1]) / zd.Close.values[:-1]]


def build_signal(stock):
    s = D[stock].reindex(CAL)
    r = np.r_[np.nan, (s.close_adj.values[1:] - s.close_adj.values[:-1]) / s.close_raw.values[:-1]]
    deltas = np.round(np.arange(26) * 0.001, 4)
    w = np.full(26, 0.60)
    sig = np.full(N, np.nan)
    for k in range(1, N):
        a = w * (1 + r[k])
        b = (1 - w) * (1 + rZN[k])
        wpre = a / (a + b)
        dev = wpre - 0.60
        sig[k] = dev.mean()
        w = np.where(np.abs(dev) >= deltas - 1e-12, 0.60, wpre)
    return sig


SIG = build_signal("ES")
old = pd.read_csv(OLD_SIG, index_col=0, parse_dates=True).signal.reindex(CAL).values
log(f"signal check vs test-12 B output: max abs diff {np.nanmax(np.abs(SIG - old)):.2e}")
SIG_NQ = build_signal("NQ")


# ---------------------------------------------------------------- 1-min decision prices (16:05 / 13:05 bar open)
def decision_prices(sym):
    pk = f"{OUT}/px_{sym}.pkl"
    if os.path.exists(pk):
        return pd.read_pickle(pk)
    df = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "instrument_id"],
                     dtype={"Open": "float64", "instrument_id": "int64"})
    ts = pd.to_datetime(df.ts_event, utc=True).dt.tz_convert(NY)
    df = df.drop(columns="ts_event")
    df["ts"] = ts
    df = df.drop_duplicates("ts").sort_values("ts").reset_index(drop=True)
    df["rc"] = (df.instrument_id.ne(df.instrument_id.shift()) & df.instrument_id.shift().notna()).cumsum()
    ts = df.ts.dt.tz_convert(NY)
    df["date"] = ts.dt.tz_localize(None).dt.normalize().values
    df["tmin"] = (ts.dt.hour * 60 + ts.dt.minute).values
    calset = pd.DataFrame({"date": CAL, "early": EARLY})
    x = df[((df.tmin >= 965) & (df.tmin < 980)) | ((df.tmin >= 785) & (df.tmin < 795))].merge(calset, on="date")
    x = x[np.where(x.early, (x.tmin >= 785) & (x.tmin < 795), (x.tmin >= 965) & (x.tmin < 980))]
    first = x.sort_values(["date", "tmin"]).groupby("date").head(1).set_index("date")
    out = first[["Open", "instrument_id", "rc", "tmin"]].reindex(CAL)
    out.to_pickle(pk)
    del df
    return out


PX = {s: decision_prices(s) for s in ("NQ", "ES")}
for s in ("NQ", "ES"):
    p = PX[s]
    exact = np.where(EARLY, 785, 965)
    log(f"{s} decision bars: present {p.Open.notna().sum()}/{N}; not the exact minute "
        f"{int((p.tmin.notna() & (p.tmin != exact)).sum())}")


def segments(sym):
    """Segment k: decision day k -> next cash day k+1. Returns gross pts per long contract, valid flag, entry raw."""
    p = PX[sym]
    o, rc = p.Open.values, p.rc.values
    g = np.full(N - 1, np.nan)
    valid = np.zeros(N - 1, bool)
    reason = np.array([""] * (N - 1), dtype=object)
    for k in range(N - 1):
        if EARLY[k]:
            reason[k] = "early_close_decision"
        elif np.isnan(o[k]) or np.isnan(o[k + 1]):
            reason[k] = "missing_bar"
        elif rc[k] != rc[k + 1]:
            reason[k] = "roll"
        else:
            valid[k] = True
            g[k] = o[k + 1] - o[k]
    return g, valid, o[:-1], reason


SEG = {s: segments(s) for s in ("NQ", "ES")}
gNQ, vNQ, eNQ, rsn = SEG["NQ"]
log("NQ flat-forced segments:", pd.Series(rsn[~vNQ]).value_counts().to_dict())


# ---------------------------------------------------------------- reference distribution & positions
def ref_stats(sig):
    pct = np.full(N, np.nan)
    z = np.full(N, np.nan)
    for t in range(1, N):
        if t - WIN < 1:
            continue
        ref = sig[t - WIN:t]
        if np.isnan(ref).any() or np.isnan(sig[t]):
            continue
        pct[t] = (ref <= sig[t]).mean()
        z[t] = (sig[t] - ref.mean()) / ref.std(ddof=1)
    return pct, z


def positions(rule, pct, z):
    p = np.zeros(N)
    ok = ~np.isnan(pct)
    if rule == "P":
        p[ok & (pct <= 0.10)] = 1
        p[ok & (pct >= 0.90)] = -1
    elif rule == "A":
        zz = np.where(np.isnan(z), 0, z)
        p = -np.sign(zz) * np.minimum(3, np.floor(np.abs(zz)))
    elif rule == "B":
        p[ok & (pct <= 0.10)] = 1
    return p[:-1]          # one per segment (decision day k)


def run(pos, sym, sign_flip=None, side=None):
    """pos per segment (already zeroed where invalid). Returns trades DataFrame-ready arrays."""
    g, valid, eraw, _ = SEG[sym]
    side = SIDE[sym] if side is None else side
    pos = np.where(valid, pos, 0.0)
    trades = []
    k, M = 0, len(pos)
    while k < M:
        if pos[k] == 0:
            k += 1
            continue
        sg = np.sign(pos[k])
        j = k
        while j + 1 < M and np.sign(pos[j + 1]) == sg:
            j += 1
        seg = pos[k:j + 1]
        gross_pts = float(np.sum(seg * g[k:j + 1]))
        sides = abs(seg[0]) + np.abs(np.diff(seg)).sum() + abs(seg[-1])
        trades.append((k, j, sg, gross_pts, sides, float(np.abs(seg).max())))
        k = j + 1
    return trades


def trade_frame(trades, sym, side=None):
    g, valid, eraw, _ = SEG[sym]
    side = SIDE[sym] if side is None else side
    m = MULT[sym]
    rows = []
    for (k, j, sg, gp, sides, mx) in trades:
        net_usd = gp * m - sides * side
        rows.append(dict(date=CAL[k], entry_time=f"{CAL[k].date()} {'13:05' if EARLY[k] else '16:05'}",
                         exit_time=f"{CAL[j + 1].date()} {'13:05' if EARLY[j + 1] else '16:05'}",
                         side="long" if sg > 0 else "short", max_contracts=mx, days=j - k + 1,
                         entry=PX[sym].Open.values[k], exit=PX[sym].Open.values[j + 1],
                         exit_reason="signal_off" if (j + 1 < N - 1 and valid[j + 1]) else
                         ("forced_flat_next_segment" if j + 1 < N - 1 else "data_end"),
                         gross_pts=gp, sides=sides, net_pts=net_usd / m, net_usd=net_usd,
                         net_bp=1e4 * (net_usd / m) / PX[sym].Open.values[k],
                         net_usd_2tick=gp * m - sides * SIDE2[sym]))
    return pd.DataFrame(rows)


def tstat(x):
    x = np.asarray(x, float)
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 1 and x.std(ddof=1) > 0 else float("nan")


def block_of(y):
    return np.where(y >= 2024, 7, (np.asarray(y) - 2010) // 2)


BLOCK_NAMES = ["2010-11", "2012-13", "2014-15", "2016-17", "2018-19", "2020-21", "2022-23", "2024-26"]


def daily_pnl(pos, sym):
    """Net $ per segment (cost of each position change charged to the segment it opens; final exit to last)."""
    g, valid, _, _ = SEG[sym]
    pos = np.where(valid, pos, 0.0)
    prev = np.r_[0.0, pos[:-1]]
    pnl = pos * np.nan_to_num(g) * MULT[sym] - np.abs(pos - prev) * SIDE[sym]
    # exit side when going flat is charged to the last held segment
    nxt = np.r_[pos[1:], 0.0]
    goes_flat = (pos != 0) & (nxt == 0)
    pnl = pnl - np.where(goes_flat, np.abs(pos) * SIDE[sym], 0) + np.where((pos == 0) & (prev != 0), np.abs(prev) * SIDE[sym], 0)
    return pnl


def summarize(name, pos, sym, tr, need_t, controls=True):
    yrs = tr.date.dt.year.values
    blk = pd.Series(tr.net_usd.values).groupby(block_of(yrs)).sum().reindex(range(8), fill_value=0.0)
    full_t = tstat(tr.net_usd)
    m18 = tr.date >= "2018-01-01"
    m23 = tr.date >= "2023-01-01"
    res = dict(rule=name, market=sym, trades=int(len(tr)), trades_per_year=round(len(tr) / ((CAL[-1] - tr.date.min()).days / 365.25), 1),
               long_trades=int((tr.side == "long").sum()), short_trades=int((tr.side == "short").sum()),
               days_in_position=int(tr.days.sum()), avg_days_per_trade=round(float(tr.days.mean()), 2),
               net_usd_per_trade=round(float(tr.net_usd.mean()), 2), net_usd_total=round(float(tr.net_usd.sum()), 2),
               gross_usd_total=round(float((tr.gross_pts * MULT[sym]).sum()), 2),
               net_bp_per_trade=round(float(tr.net_bp.mean()), 2), t_trade=round(full_t, 3),
               net_usd_total_2tick=round(float(tr.net_usd_2tick.sum()), 2), t_trade_2tick=round(tstat(tr.net_usd_2tick), 3),
               era_2018_2026=dict(n=int(m18.sum()), total=round(float(tr.net_usd[m18].sum()), 2),
                                  per_trade=round(float(tr.net_usd[m18].mean()), 2), t=round(tstat(tr.net_usd[m18]), 2)),
               era_2023_2026=dict(n=int(m23.sum()), total=round(float(tr.net_usd[m23].sum()), 2),
                                  per_trade=round(float(tr.net_usd[m23].mean()), 2), t=round(tstat(tr.net_usd[m23]), 2)),
               blocks={BLOCK_NAMES[i]: round(float(v), 2) for i, v in blk.items()},
               blocks_positive=int((blk > 0).sum()),
               by_year={str(k): round(float(v), 2) for k, v in tr.groupby(yrs).net_usd.sum().items()},
               legs={sd: dict(n=int((tr.side == sd).sum()), total=round(float(tr.net_usd[tr.side == sd].sum()), 2),
                              t=round(tstat(tr.net_usd[tr.side == sd]), 2)) for sd in ("long", "short")})
    dp = daily_pnl(pos, sym)
    act = dp[(np.where(SEG[sym][1], pos, 0) != 0) | (dp != 0)]
    res["t_day_level"] = round(tstat(act), 3)
    if controls:
        rng = np.random.default_rng(SEED)
        # random direction: flip each trade's side by coin
        net = tr.net_usd.values
        gross = tr.gross_pts.values * MULT[sym]
        cost = gross - net
        rd = np.array([np.sum(np.where(rng.random(len(net)) < 0.5, 1, -1) * gross - cost) for _ in range(NREP)])
        p95 = float(np.percentile(rd, 95))
        res["random_direction"] = dict(p95=round(p95, 2), mean=round(float(rd.mean()), 2),
                                       pctile_of_rule=round(float((rd < net.sum()).mean() * 100), 1))
        # shuffled-date placebo: circular shift of segment-position path
        rng2 = np.random.default_rng(SEED)
        M = len(pos)
        valid = SEG[sym][1]
        base = np.where(valid, pos, 0.0)
        offs = rng2.integers(WIN, M - WIN + 1, NREP)
        pl = []
        for o in offs:
            sh = np.where(valid, np.roll(base, o), 0.0)
            pl.append(sum(t[3] * MULT[sym] - t[4] * SIDE[sym] for t in run(sh, sym)))
        pl = np.array(pl)
        res["shuffled_date_placebo"] = dict(p95=round(float(np.percentile(pl, 95)), 2), mean=round(float(pl.mean()), 2),
                                            pctile_of_rule=round(float((pl < net.sum()).mean() * 100), 1))
        c = dict(C1=bool(full_t >= need_t), C2=bool(tr.net_usd[m18].sum() > 0), C3=bool(tr.net_usd[m23].sum() > 0),
                 C4=bool(res["blocks_positive"] >= 6), C5=bool(net.sum() > p95))
        res["criteria"] = c
        res["t_needed"] = need_t
        res["PASS"] = all(c.values())
        res["beats_drift_extra"] = bool(net.sum() > res["shuffled_date_placebo"]["p95"])
    return res


def show(r):
    log(f"\n[{r['rule']} {r['market']}] trades {r['trades']} ({r['trades_per_year']}/yr; long {r['long_trades']}, short "
        f"{r['short_trades']}; {r['days_in_position']} days in position, {r['avg_days_per_trade']} days/trade)")
    log(f"  net ${r['net_usd_per_trade']}/trade, total ${r['net_usd_total']} (gross ${r['gross_usd_total']}), "
        f"{r['net_bp_per_trade']} bp/trade, t {r['t_trade']} (day-level t {r['t_day_level']}); 2-tick total "
        f"${r['net_usd_total_2tick']} t {r['t_trade_2tick']}")
    log(f"  2018-26: {r['era_2018_2026']}   2023-26: {r['era_2023_2026']}")
    log(f"  blocks: {r['blocks']}  positive {r['blocks_positive']}/8")
    log(f"  by year: {r['by_year']}")
    log(f"  legs: {r['legs']}")
    if "criteria" in r:
        log(f"  random-direction: {r['random_direction']}; shuffled-date placebo: {r['shuffled_date_placebo']}")
        log(f"  criteria (t>= {r['t_needed']}): {r['criteria']} -> PASS={r['PASS']}; beats drift (extra): "
            f"{r['beats_drift_extra']}")


PCT, Z = ref_stats(SIG)
first = CAL[np.argmax(~np.isnan(PCT))]
log(f"first decision day {first.date()}; signal mean {np.nanmean(SIG) * 100:.3f}pp sd {np.nanstd(SIG) * 100:.3f}pp")
RES = {}
for rule, need in (("P", 2.0), ("A", 2.4), ("B", 2.4)):
    pos = positions(rule, PCT, Z)
    for sym in ("NQ", "ES"):
        tr = trade_frame(run(pos, sym), sym)
        r = summarize(rule, pos, sym, tr, need, controls=True)
        if sym == "ES":
            r["note"] = "MES report-only"
            for kk in ("criteria", "PASS", "beats_drift_extra"):
                r[kk + "_reportonly"] = r.pop(kk)
        RES[f"{rule}_{'MNQ' if sym == 'NQ' else 'MES'}"] = r
        show(r)
        tr.to_csv(f"{OUT}/trades_{rule}_{'MNQ' if sym == 'NQ' else 'MES'}.csv", index=False)
        if sym == "NQ":
            dp = pd.Series(daily_pnl(pos, "NQ"), index=CAL[1:])   # segment P&L dated by its exit day
            RES[f"{rule}_MNQ"]["_daily"] = dp

# report-only: NQ-built signal through rule P
pctn, zn_ = ref_stats(SIG_NQ)
posn = positions("P", pctn, zn_)
trn = trade_frame(run(posn, "NQ"), "NQ")
r = summarize("P_NQbuilt_signal", posn, "NQ", trn, 2.0, controls=True)
r["note"] = "report-only (signal built from NQ, the nq run's t=-2.94 version); cannot rescue"
for kk in ("criteria", "PASS", "beats_drift_extra"):
    r[kk + "_reportonly"] = r.pop(kk)
RES["P_MNQ_NQbuilt"] = r
show(r)
trn.to_csv(f"{OUT}/trades_P_MNQ_NQbuilt_signal.csv", index=False)

# correlation with live models
cm = pd.read_csv("chosen_models_trades.csv", usecols=["model", "date", "usd"], parse_dates=["date"])
live = cm.groupby("date").usd.sum().reindex(CAL[1:], fill_value=0.0)
for rule in ("P", "A", "B"):
    dp = RES[f"{rule}_MNQ"].pop("_daily")
    msk = CAL[1:] >= first
    cc = float(np.corrcoef(dp[msk], live[msk])[0, 1])
    RES[f"{rule}_MNQ"]["corr_daily_with_live_models"] = round(cc, 3)
    both = (dp[msk] != 0)
    RES[f"{rule}_MNQ"]["live_models_pnl_on_rule_days"] = round(float(live[msk][both].sum()), 2)
    log(f"[{rule}] daily P&L correlation with the 3 live models: {cc:.3f}")

pd.DataFrame({"signal": SIG, "pct252": PCT, "z252": Z, "signal_NQbuilt": SIG_NQ}, index=CAL).to_csv(f"{OUT}/signal.csv")
json.dump(dict(prereg_sha256="b42e85c407e5b7b30ea83c52135b9fdcc0f66e84ad7623c69df86d4083da335b", results=RES,
               log=LOG), open(f"{OUT}/summary.json", "w"), indent=1, default=str)
log("saved", OUT)
