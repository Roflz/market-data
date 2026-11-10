"""
Exit styles for the two leads (fixed 1.5R / 16-bar exit replaced by trend-style exits). No new entries, no model change:
  A  raw 60-min long pullback triggers (trigger_scan.py, rule ema50_pb and the other long rules), MNQ/MES/MYM
  B  v1 entry-logit kept trades on 120-min charts (MES, MYM), out of sample 2013..2025H1
Every exit is walked on the 1-minute path (labels.walk_1m: stop first in every minute, stop fills slip 1 tick).
Trailing / breakeven / EMA rules only use bars that have CLOSED (updated at each bar's close). Everything is out by
the 16:45 ET bar's close (Lucid rule). Costs: $1 + 1 tick each way (+1 tick on stop fills).
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 -u exit_study.py
"""
import gc
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import features as fe
import labels as lb
import run_pipeline as rp
import signals as sg
import walkforward as wf

# name: (target R or None, trail N bars or None, breakeven at +1R, EMA exit column or None, time limit '16' / 'day')
EXITS = {
    "1.5R target, 16 bars (old)": (1.5, None, False, None, "16"),
    "2R target, hold to 16:45": (2.0, None, False, None, "day"),
    "3R target, hold to 16:45": (3.0, None, False, None, "day"),
    "stop only, hold to 16:45": (None, None, False, None, "day"),
    "trail under last 3 bars": (None, 3, False, None, "day"),
    "trail under last 5 bars": (None, 5, False, None, "day"),
    "breakeven at +1R, then trail 3": (None, 3, True, None, "day"),
    "exit on close below EMA 20": (None, None, False, "ema20", "day"),
    "exit on close below EMA 8": (None, None, False, "ema8", "day"),
    "3R target + trail 3": (3.0, 3, False, None, "day"),
    # hold until an OPPOSITE signal appears (exit at the next bar's open); the entry stop stays; flat by 16:45
    "opp: any opposite candle pattern": (None, None, False, None, "day", "opp_pattern"),
    "opp: opposite reversal pattern": (None, None, False, None, "day", "opp_reversal"),
    "opp: reversal pattern + momentum falling": (None, None, False, None, "day", "opp_reversal_mom"),
    "opp: opposite entry trigger": (None, None, False, None, "day", "opp_trigger"),
    "opp: EMA 8 crosses EMA 20": (None, None, False, None, "day", "ema_cross"),
}


def exit_signals(sym, tf, b, ctx):
    """Opposite-signal exits, known at each bar's close: {name: (exit_long[j], exit_short[j])} boolean arrays.
    opp_pattern       any textbook-direction candle pattern pointing against the trade
    opp_reversal      a reversal-family pattern against the trade (features.FAMILIES['reversal'])
    opp_reversal_mom  that, AND Momentum(14) moving against the trade this bar (needs 2 pieces of evidence)
    opp_trigger       any of trigger_scan's 5 pullback rules firing in the opposite direction (the entry, mirrored)
    ema_cross         EMA 8 crosses EMA 20 against the trade"""
    import trigger_scan as ts                                          # noqa: PLC0415
    tick = sg.SPEC[sym]["tick"]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        P = sg.patterns(b, ctx, tick=tick)
    dirc = [c for c in fe.DIRECTIONAL if c in P.columns]
    rev = [c for c in fe.FAMILIES["reversal"] if c in P.columns]
    A = P[dirc].to_numpy(np.int8); Rv = P[rev].to_numpy(np.int8)
    mom = ctx["mom14"].to_numpy(np.float64)
    dm = np.r_[np.nan, np.diff(mom)]
    ev = ts.detect(b, ctx, tick, tf)
    ev = ev[ev.rule != "trend_all"]
    n = len(b)
    trig = {1: np.zeros(n, bool), -1: np.zeros(n, bool)}
    for d in (1, -1):
        trig[d][ev.loc[ev.d == d, "i"].to_numpy()] = True
    e8, e20 = ctx["ema8"].to_numpy(np.float64), ctx["ema20"].to_numpy(np.float64)
    diff = e8 - e20
    prev = np.r_[np.nan, diff[:-1]]
    out = {}
    out["opp_pattern"] = ((A == -1).any(1), (A == 1).any(1))
    out["opp_reversal"] = ((Rv == -1).any(1), (Rv == 1).any(1))
    out["opp_reversal_mom"] = ((Rv == -1).any(1) & (dm < 0), (Rv == 1).any(1) & (dm > 0))
    out["opp_trigger"] = (trig[-1], trig[1])
    out["ema_cross"] = ((diff < 0) & (prev >= 0), (diff > 0) & (prev <= 0))
    return out


def simulate(sym, tf, b, ctx, events, m1, target_R, trail, breakeven, ema, limit, max_bars=16, rule_exit=None):
    """Net $ per micro for each event under one exit style. events: i (signal bar), d, stop. Returns DataFrame
    [pnl, kind (0 time / 1 stop / 2 target / 3 rule exit), bars_held] aligned with the enterable events (sel)."""
    z = lb._prepare(sym, tf, b, events, max_bars, m1)
    spec = z["spec"]; tick, usd, cost = spec["tick"], spec["usd"], spec["cost"]
    d, entry, risk, e = z["d"], z["entry"], z["risk"], z["e"]
    first = z["first"]; last = lb.map_1m(m1, b, tf)[1]
    O1, H1, L1, C1 = z["O1"], z["H1"], z["L1"], z["C1"]
    T = np.minimum(z["i"] + max_bars, z["forced"][z["i"]]) if limit == "16" else z["forced"][z["i"]]
    n = len(d)
    Hb, Lb, Cb = (b[c].to_numpy(np.float64) for c in "HLC")
    E = ctx[ema].to_numpy(np.float64) if ema else None
    stop = np.where(risk < 0, np.nan, z["stop"].astype(np.float64))
    tgt = entry + d * (target_R or np.nan) * np.maximum(risk, 0)
    pnl = np.full(n, np.nan); kind = np.zeros(n, np.int8); held = np.zeros(n, np.int64)
    past = risk < 0
    pnl[past] = -cost; kind[past] = 1
    act = np.flatnonzero(~past)
    k = 0
    while len(act):
        j = e[act] + k
        r0, r1 = first[j], last[j]
        has = r0 >= 0
        kd, xp, _ = lb.walk_1m(O1, H1, L1, C1, np.where(has, r0, 0), np.where(has, r1, -1), d[act],
                               stop[act], tgt[act][:, None], tick)
        kd, xp = kd[:, 0], xp[:, 0]
        hit = has & (kd > 0)
        if hit.any():
            a = act[hit]
            pnl[a] = d[a] * (xp[hit] - entry[a]) * usd - cost
            kind[a] = kd[hit]; held[a] = k + 1
        still = ~hit
        act, j = act[still], j[still]
        if not len(act):
            break
        # bar j closed without a stop/target fill
        end = j >= T[act]
        if end.any():
            a = act[end]
            px = Cb[j[end]]
            pnl[a] = d[a] * (px - entry[a]) * usd - cost
            kind[a] = 0; held[a] = k + 1
        act, j = act[~end], j[~end]
        if not len(act):
            break
        dd = d[act]
        if ema is not None or rule_exit is not None:      # exit signal at this close -> out at the next open
            if ema is not None:
                out = dd * (Cb[j] - E[j]) < 0
            else:
                out = np.where(dd > 0, rule_exit[0][j], rule_exit[1][j])
            if out.any():
                a = act[out]
                nxt = first[j[out] + 1]
                px = np.where(nxt >= 0, O1[np.maximum(nxt, 0)], Cb[j[out]])
                pnl[a] = d[a] * (px - entry[a]) * usd - cost
                kind[a] = 3; held[a] = k + 1
                act, j, dd = act[~out], j[~out], dd[~out]
        if breakeven and len(act):
            best = np.where(dd > 0, Hb[j], Lb[j])
            reach = dd * (best - entry[act]) >= risk[act]
            s = stop[act]
            stop[act] = np.where(reach, np.where(dd > 0, np.fmax(s, entry[act]), np.fmin(s, entry[act])), s)
        if trail and len(act):
            lo = np.full(len(act), np.inf); hi = np.full(len(act), -np.inf)
            for q in range(trail):                        # bars j-q, only bars at/after the signal bar's segment
                jj = j - q
                lo = np.fmin(lo, Lb[jj]); hi = np.fmax(hi, Hb[jj])
            s = stop[act]
            stop[act] = np.where(dd > 0, np.fmax(s, lo - tick), np.fmin(s, hi + tick))
        k += 1
    return pd.DataFrame({"pnl": pnl, "kind": kind, "bars_held": held}), z["sel"]


def report(name, ev, res, years):
    s = ev.assign(pnl=res.pnl.to_numpy(), held=res.bars_held.to_numpy(), year=years)
    by = s.groupby("year").pnl.sum()
    def span(y0, y1):
        x = s[(s.year >= y0) & (s.year <= y1)]
        return x.pnl.mean() if len(x) else np.nan
    no25 = s[s.year < 2025]
    return dict(usd_trade=s.pnl.mean(), usd_2010_20=span(2010, 2020), usd_2021_25=span(2021, 2025),
                usd_without_2025=no25.pnl.mean(), total=s.pnl.sum(), years_pos=f"{int((by > 0).sum())}/{by.size}",
                n=len(s), per_year=round(len(s) / by.size), bars_held=s.held.mean(),
                worst=s.pnl.min(), t_stat=s.pnl.mean() / (s.pnl.std() / np.sqrt(len(s))))


def trade_sets():
    """(label, sym, tf, events with i, d, stop)"""
    sets = []
    for sym in ("NQ", "ES", "YM"):
        T = pd.read_parquet(f"out/triggers_{sym}_60.parquet", columns=["t", "i", "d", "rule", "stop"])
        for rule in ("ema50_pb", "ema20_pb", "ema8_pb", "pb_break", "mom_turn", "trend_all"):
            sets.append((f"A {rule} long", sym, 60, T[(T.rule == rule) & (T.d > 0)].reset_index(drop=True)))
    for sym in ("ES", "YM"):
        data = rp.load("entry", sym, tf=120)
        r = wf.walk_forward(data, rp.feature_list("entry", sym), model="logit", verbose=False,
                            **rp.wf_args("entry"), **rp.WF_KW)
        kept = r.oos.index[r.oos["take"].astype(bool)]
        sets.append(("B model-kept 120m", sym, 120, data.loc[kept, ["t", "i", "d", "stop"]].reset_index(drop=True)))
        del data; gc.collect()
    return sets


def main():
    rows = []
    sets = trade_sets()
    m1s, bars = {}, {}
    for label, sym, tf, ev in sets:
        t0 = time.time()
        if sym not in m1s:
            m1 = lb.load_1m(sym); m1s[sym] = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
        if (sym, tf) not in bars:
            b, ctx = fe._load(sym, tf)
            keep = b.index < wf.HOLDOUT_SESSION_START
            bars[(sym, tf)] = (b.loc[keep], ctx.loc[keep])
        b, ctx = bars[(sym, tf)]
        if (sym, tf, "sig") not in bars:
            bars[(sym, tf, "sig")] = exit_signals(sym, tf, b, ctx)
        sigs = bars[(sym, tf, "sig")]
        for name, spec in EXITS.items():
            tR, trail, be, ema, lim = spec[:5]
            rx = sigs[spec[5]] if len(spec) > 5 else None
            res, sel = simulate(sym, tf, b, ctx, ev, m1s[sym], tR, trail, be, ema, lim, rule_exit=rx)
            e = ev.iloc[sel].reset_index(drop=True)
            rows.append(dict(set=label, market=sym, tf=tf, exit=name,
                             **report(name, e, res, pd.DatetimeIndex(e["t"]).year.to_numpy())))
        pd.DataFrame(rows).to_csv("out/exit_study.csv", index=False)
        R = pd.DataFrame([r for r in rows if r["set"] == label and r["market"] == sym])
        print(f"\n{label} {sym} {tf}m ({len(ev):,} trades, {time.time() - t0:.0f}s)\n"
              + R[["exit", "usd_trade", "usd_2010_20", "usd_2021_25", "usd_without_2025", "years_pos", "bars_held",
                   "t_stat"]].round(2).to_string(index=False), flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
