"""
v2/luck_baseline.py - "what does luck alone get you?": random trades with no edge, run through the eval judge.

For each market (NQ, ES, YM = MNQ, MES, MYM) and timeframe (15, 60 min):
  POOL   a random sample of PER_DAY (8) eligible bars per trading day (labels.eligible: enterable at the next bar's
         open in the same session, not after the 16:45 forced-exit bar), 2010 (YM 2018) .. 2025-06-30, each bar
         labelled BOTH ways (long and short). Stop = trigger_scan's rule: 1 tick beyond the lowest low (long) /
         highest high (short) of the last 5 bars of the same contract, but at least 1 R20 (mean range of the 20 bars
         before) from the signal bar's close. Entry at the next bar's open. Two exits, walked on the 1-minute path
         (labels.label_entries == exit_study.simulate, checked below):
           hold  'stop only, hold to 16:45' (the 16:45 forced-exit bar's close: 16:45 on 15-min, 16:00 on 60-min)
           old   '1.5R target, 16 bars'
         Costs $1 + 1 tick each way, +1 tick on stop fills. Flat by 16:45: v2/lucid.py's session frame (the old
         one let 2010-2015 trades run to 17:15-17:30). Saved: out/luck_pool_<sym>_<tf>.parquet.
  DRAWS  frequency f in (0.5, 1, 3) trades per trading day: every pool bar is kept with probability f / PER_DAY;
         direction random 50/50 ('random') or always long ('long'); SEEDS independent draws (draw() is
         deterministic, so any draw's trade list can be rebuilt from the pool: luck_trades()).
  EVAL   every draw x sizing policy (1/2/3/5 micros; $100/150/250/400 risk) through eval_sim.evaluate (20-micro cap,
         $600 daily limit, Lucid rules, consistency 40% and 50%, starts in 2013+, 2018+, 2022+).
  Outputs (v2/out/): luck_eval.csv (one row per draw x policy x consistency x window), luck_table.csv (mean over
  the draws, with the min / p90 / max pass % across draws and p90 of within_10 / within_20), luck_bar.csv (per
  market / window / consistency: the best luck configuration's value of each metric = the bar to beat),
  luck_handcheck_<sym>_<tf>.csv (independent re-walk of a few trades), luck_pnl_by_year.csv ($/trade by year and window for each
  pool, exit and side), calendar_<sym>.csv (the trading calendar every later stage should use).
Holdout: bars and 1-minute data are cut at walkforward.HOLDOUT_SESSION_START before anything is computed.

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 -u \
      v2/luck_baseline.py NQ ES YM --tf 15,60 [--seeds 6] [--table-only]
"""
import argparse
import gc
import json
import os
import time
import warnings

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
PER_DAY = 8
FREQS = (0.5, 1.0, 3.0)
MODES = ("random", "long")
EXITS = {"hold": "stop only, hold to 16:45", "old": "1.5R target, 16 bars"}
STOP_LOOKBACK = 5
HOLD_R, HOLD_BARS = 1e6, 10 ** 6                       # 'no target', 'no bar limit' (the 16:45 bar ends it)
MKT_CODE = {"NQ": 1, "ES": 2, "YM": 3}


def luck_stops(b, tick):
    """(stop_long, stop_short, valid) per bar, known at the bar's close: trigger_scan's stop rule."""
    L, H, C = (b[c].to_numpy(np.float64) for c in "LHC")
    R = fe.r20(b, tick)
    lo5 = pd.Series(L).rolling(STOP_LOOKBACK).min().to_numpy()
    hi5 = pd.Series(H).rolling(STOP_LOOKBACK).max().to_numpy()
    valid = fe._run_ok(b.run.to_numpy(), STOP_LOOKBACK - 1) & np.isfinite(R)
    return np.minimum(lo5 - tick, C - R), np.maximum(hi5 + tick, C + R), valid


def pool_events(b, tf, tick, per_day=PER_DAY, seed=0):
    """Random eligible bars (per_day per trading day on average), both directions: DataFrame t, i, d, stop."""
    ok, _ = lb.eligible(b, tf)
    sl, ss, valid = luck_stops(b, tick)
    cand = np.flatnonzero(ok & valid)
    n_days = len(np.unique(wf.session_label(b.index[cand])))
    n = min(len(cand), int(round(per_day * n_days)))
    rng = np.random.default_rng(seed)
    i = np.sort(rng.choice(cand, size=n, replace=False))
    ev = pd.DataFrame({"i": np.r_[i, i], "d": np.r_[np.ones(n, np.int8), -np.ones(n, np.int8)],
                       "stop": np.r_[sl[i], ss[i]]})
    ev.insert(0, "t", b.index[ev.i.to_numpy()])
    return ev.sort_values(["i", "d"]).reset_index(drop=True)


def build_pool(sym, tf, b, m1, per_day=PER_DAY, seed=0):
    tick = sg.SPEC[sym]["tick"]
    ev = pool_events(b, tf, tick, per_day, seed)
    a = lb.label_entries(sym, tf, b, ev, target_R=(1.5,), max_bars=16, m1=m1)
    h = lb.label_entries(sym, tf, b, ev, target_R=(HOLD_R,), max_bars=HOLD_BARS, m1=m1)
    hk = f"{HOLD_R:g}"
    a = a[["t", "i", "d", "stop", "market", "t_entry", "entry", "risk_usd", "past_stop", "pnl_usd_1.5",
           "t_end_1.5", "exit_kind_1.5"]].rename(columns={"pnl_usd_1.5": "pnl_old", "t_end_1.5": "t_exit_old",
                                                          "exit_kind_1.5": "kind_old"})
    h = h[["i", "d", f"pnl_usd_{hk}", f"t_end_{hk}", f"exit_kind_{hk}"]].rename(
        columns={f"pnl_usd_{hk}": "pnl_hold", f"t_end_{hk}": "t_exit_hold", f"exit_kind_{hk}": "kind_hold"})
    p = a.merge(h, on=["i", "d"], how="inner")
    p.insert(1, "tf", tf)
    p["session"] = wf.session_label(p.t_entry)
    p["hour"] = pd.DatetimeIndex(p.t_entry).hour
    return p.reset_index(drop=True)


def draw(pool, freq, mode, seed, per_day=PER_DAY):
    """Rows of the pool for one draw (deterministic in market, tf, freq, mode, seed)."""
    sym, tf = pool.market.iloc[0], int(pool.tf.iloc[0])
    ss = np.random.SeedSequence([MKT_CODE[sym], tf, int(round(freq * 10)), MODES.index(mode), int(seed)])
    rng = np.random.default_rng(ss)
    bars = np.unique(pool.i.to_numpy())
    keep = bars[rng.random(len(bars)) < freq / per_day]
    side = rng.choice(np.array([-1, 1], np.int8), size=len(keep)) if mode == "random" else np.ones(len(keep), np.int8)
    want = pd.DataFrame({"i": keep, "d": side})
    return pool.merge(want, on=["i", "d"], how="inner")


def trade_table(rows, exit_name):
    return pd.DataFrame({"market": rows.market.to_numpy(), "t_entry": rows.t_entry.to_numpy(),
                         "t_exit": rows[f"t_exit_{exit_name}"].to_numpy(), "session": rows.session.to_numpy(),
                         "risk_usd": rows.risk_usd.to_numpy(), "pnl_usd": rows[f"pnl_{exit_name}"].to_numpy()})


def luck_trades(sym, tf, freq, mode, exit_name, seed):
    """The trade table of one draw, rebuilt from the saved pool (for later stages / the GUI)."""
    pool = pd.read_parquet(os.path.join(OUT, f"luck_pool_{sym}_{tf}.parquet"))
    return trade_table(draw(pool, freq, mode, seed), exit_name)


# ------------------------------------------------------------------------------------------------ checks
def check_against_exit_study(sym, tf, b, ctx, m1, pool, n=3000, seed=0):
    """labels.label_entries (used for the pool) == exit_study.simulate on a sample, for both exits."""
    import exit_study as xs                                               # noqa: PLC0415
    rng = np.random.default_rng(seed)
    s = pool.iloc[np.sort(rng.choice(len(pool), size=min(n, len(pool)), replace=False))].reset_index(drop=True)
    ev = s[["t", "i", "d", "stop"]]
    worst = {}
    for name, args in {"old": (1.5, None, False, None, "16"), "hold": (None, None, False, None, "day")}.items():
        res, sel = xs.simulate(sym, tf, b, ctx, ev, m1, *args)
        diff = np.abs(res.pnl.to_numpy() - s[f"pnl_{name}"].to_numpy()[sel])
        worst[name] = (float(np.nanmax(diff)), len(sel), len(s))
    return worst


def check_trigger_scan_stops(b, ctx, tick, tf):
    """luck_stops == the stop column of trigger_scan.detect on its 'trend_all' events."""
    import trigger_scan as ts                                             # noqa: PLC0415
    ev = ts.detect(b, ctx, tick, tf)
    ev = ev[ev.rule == "trend_all"]
    sl, ss, _ = luck_stops(b, tick)
    mine = np.where(ev.d > 0, sl[ev.i], ss[ev.i])
    return float(np.max(np.abs(mine - ev.stop.to_numpy()))) if len(ev) else 0.0, len(ev)


def hand_check(sym, tf, pool, m1, b, n=12, seed=3):
    """Independent minute-by-minute re-walk of the 'hold' exit for a few pool rows from the raw 1-minute bars.
    Returns a DataFrame with the pool's pnl and the re-computed one."""
    spec = sg.SPEC[sym]
    tick, usd, cost = spec["tick"], spec["usd"], spec["cost"]
    rng = np.random.default_rng(seed)
    rows = []
    _, forced = lb.eligible(b, tf)
    for k in rng.choice(len(pool), size=n, replace=False):
        r = pool.iloc[k]
        inst = b.inst.iloc[int(r.i)]
        end = b.index[forced[int(r.i)]] + pd.Timedelta(minutes=tf)       # close of the 16:45 forced-exit bar
        mm = m1[(m1.index >= r.t_entry) & (m1.index < end) & (m1.inst == inst)]
        entry, d, stop = mm.O.iloc[0], int(r.d), float(r.stop)
        x, why = None, "time"
        if d * (entry - stop) < 0:
            x, why = entry, "past"
        else:
            for _, q in mm.iterrows():
                if (d > 0 and q.L <= stop) or (d < 0 and q.H >= stop):
                    x = (min(q.O, stop) - tick) if d > 0 else (max(q.O, stop) + tick)
                    why = "stop"
                    break
            if x is None:
                x = mm.C.iloc[-1]
        pnl = -cost if why == "past" else d * (x - entry) * usd - cost
        rows.append(dict(market=sym, tf=tf, t=r.t, d=d, entry=entry, stop=stop, exit=x, why=why,
                         pool_pnl=r.pnl_hold, hand_pnl=pnl, pool_kind=r.kind_hold))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ eval
def run_draws(pool, cal, seeds):
    sym, tf = pool.market.iloc[0], int(pool.tf.iloc[0])
    out = []
    for freq in FREQS:
        for mode in MODES:
            for seed in range(seeds):
                rows = draw(pool, freq, mode, seed)
                for ex in EXITS:
                    tr = trade_table(rows, ex)
                    e = es.evaluate(tr, cal)
                    e.insert(0, "seed", seed)
                    e.insert(0, "exit", ex)
                    e.insert(0, "mode", mode)
                    e.insert(0, "freq", freq)
                    e.insert(0, "tf", tf)
                    e.insert(0, "market", sym)
                    e["n_trades"] = len(tr)
                    e["usd_trade"] = tr.pnl_usd.mean()
                    out.append(e)
    return pd.concat(out, ignore_index=True)


def upsert(name, df, keys):
    p = os.path.join(OUT, name)
    if os.path.exists(p):
        old = pd.read_csv(p)
        hit = pd.MultiIndex.from_frame(old[keys].astype(str)).isin(
            pd.MultiIndex.from_frame(df[keys].astype(str)).unique())
        df = pd.concat([old.loc[~hit], df], ignore_index=True)
    df.to_csv(p, index=False)


def table():
    E = pd.read_csv(os.path.join(OUT, "luck_eval.csv"))
    keys = ["market", "tf", "freq", "mode", "exit", "policy", "consistency", "window"]
    g = E.groupby(keys, sort=False)
    T = g[["pass_pct", "fail_pct", "open_pct", "pass_rate", "days_pass_median", "within_5", "within_10",
           "within_20", "n_starts", "trades_taken", "micros_mean", "usd_day_mean", "usd_trade"]].mean()
    T["pass_pct_min"] = g.pass_pct.min()
    T["pass_pct_p90"] = g.pass_pct.quantile(0.9)
    T["pass_pct_max"] = g.pass_pct.max()
    T["within_10_p90"] = g.within_10.quantile(0.9)
    T["within_20_p90"] = g.within_20.quantile(0.9)
    T["draws"] = g.size()
    T = T.reset_index()
    T.to_csv(os.path.join(OUT, "luck_table.csv"), index=False)
    # the bar to beat: per market / window / consistency, the BEST luck configuration (mean over draws) and the
    # 90th percentile of single draws, for each metric separately
    b = T.groupby(["market", "window", "consistency"])
    bar = b[["pass_pct", "within_5", "within_10", "within_20", "pass_pct_p90", "within_10_p90",
             "within_20_p90"]].max().add_prefix("best_")
    bar["best_days_pass_median"] = b.days_pass_median.min()
    bar.reset_index().to_csv(os.path.join(OUT, "luck_bar.csv"), index=False)
    return T


def main(markets, tfs, seeds, table_only=False):
    import run_pipeline as rp                                             # noqa: PLC0415
    if not table_only:
        for sym in markets:
            t0 = time.time()
            tick = sg.SPEC[sym]["tick"]
            m1 = lb.load_1m(sym)
            m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
            for tf in tfs:
                t1 = time.time()
                b, ctx = fe._load(sym, tf)
                keep = b.index < wf.HOLDOUT_SESSION_START
                b, ctx = b.loc[keep], ctx.loc[keep]
                if tf == tfs[0]:
                    cal = es.build_calendar(b.index)
                    pd.DataFrame({"session": cal}).to_csv(os.path.join(OUT, f"calendar_{sym}.csv"), index=False)
                cal = es.load_calendar(sym)
                d_stop, n_ts = check_trigger_scan_stops(b, ctx, tick, tf)
                pool = build_pool(sym, tf, b, m1)
                pool.to_parquet(os.path.join(OUT, f"luck_pool_{sym}_{tf}.parquet"), compression="zstd")
                chk = check_against_exit_study(sym, tf, b, ctx, m1, pool)
                hc = hand_check(sym, tf, pool, m1, b)
                hc.to_csv(os.path.join(OUT, f"luck_handcheck_{sym}_{tf}.csv"), index=False)
                print(f"{sym} {tf}m: pool {len(pool):,} rows ({len(pool) / 2 / len(cal):.1f} bars/day) "
                      f"[{time.time() - t1:.0f}s]; stop == trigger_scan: max diff {d_stop} on {n_ts:,} events; "
                      f"label_entries vs exit_study.simulate max |diff| {chk}; hand check max |diff| "
                      f"{np.abs(hc.pool_pnl - hc.hand_pnl).max():.4f}", flush=True)
                # $/trade by year per exit and side
                rep = []
                for ex in EXITS:
                    for side, m in (("both", np.ones(len(pool), bool)), ("long", pool.d > 0), ("short", pool.d < 0)):
                        r = es.pnl_report(trade_table(pool[m], ex))
                        r.insert(0, "side", side); r.insert(0, "exit", ex); r.insert(0, "tf", tf)
                        r.insert(0, "market", sym)
                        rep.append(r)
                upsert("luck_pnl_by_year.csv", pd.concat(rep, ignore_index=True), ["market", "tf"])
                del ctx; gc.collect()
                t2 = time.time()
                E = run_draws(pool, cal, seeds)
                upsert("luck_eval.csv", E, ["market", "tf"])
                for (fq, md, ex), g in E.groupby(["freq", "mode", "exit"]):
                    x = g[(g.window == "2013+") & (g.consistency == 0.4)]
                    rp.log_trial(module="v2-luck_baseline", scope=f"{sym}{tf}", model="random entries",
                                 target=EXITS[ex], oos_rows=int(g.n_trades.mean()),
                                 oos_usd_per_trade=round(float(g.usd_trade.mean()), 2),
                                 runtime_s=round(time.time() - t2),
                                 parameters=json.dumps(dict(freq_per_day=fq, mode=md, seeds=seeds,
                                                            policies=[es.policy_name(p) for p in es.POLICIES],
                                                            per_day_pool=PER_DAY)),
                                 note="luck baseline (no edge); pass% 2013+ starts, 40% cons, by policy: "
                                      + ", ".join(f"{p} {v:.0f}" for p, v in
                                                  x.groupby("policy", sort=False).pass_pct.mean().items()))
                print(f"   draws evaluated in {time.time() - t2:.0f}s", flush=True)
                fe.clear_cache(); del b, pool, E; gc.collect()
            del m1; gc.collect()
            print(f"{sym} done in {time.time() - t0:.0f}s", flush=True)
    T = table()
    v = T[(T.window == "2013+") & (T.consistency == 0.4)]
    pd.set_option("display.width", 250)
    print(v.pivot_table(index=["market", "tf", "exit", "mode", "freq"], columns="policy", values="pass_pct",
                        sort=False).round(0).to_string())
    print("done", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("markets", nargs="*", default=["NQ", "ES", "YM"])
    ap.add_argument("--tf", default="15,60")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--table-only", action="store_true")
    a = ap.parse_args()
    main(a.markets, [int(x) for x in a.tf.split(",")], a.seeds, a.table_only)
