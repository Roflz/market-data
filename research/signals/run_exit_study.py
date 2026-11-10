"""
Exit study: every directional pattern as an entry, with many exit rules compared on the very same entries.
One market and timeframe per run.   PYTHONPATH=../../pylib:../..:. python3 run_exit_study.py ES 15
Timing, cutoff (flat by 16:45 ET), stop/target fills: see exits.py. Long rules below; shorts are the mirror.

family     exit                 rule
baseline   fixed_5/10/20        close of the 5th/10th/20th bar after the signal bar
baseline   hold_1645            hold until 16:45
opposite   opp_same             the same pattern fires the other way
opposite   opp_classic          any classic candle pattern fires the other way (exits.CLASSIC)
opposite   opp_any              any directional pattern fires the other way (incl. the very frequent ones)
opposite   opp_any2             2+ different directional patterns fire the other way on one bar
opposite   opp_classic_at_level a bearish classic pattern whose high reaches the latest confirmed 5-bar swing high
                                (within half an average bar range, or above it) = reversal signal AT resistance
opposite   choch_3 / choch_5    change of character: a close below the latest confirmed swing low (3- / 5-bar swings)
fading     mom_turn             Momentum(14) falls two bars in a row
fading     mom_cross100         Momentum(14) closes below 100
fading     ema8_cross/ema20_cross  a close below EMA 8 / EMA 20
trailing   trail_3/5/10         stop starts 1 tick beyond the pattern; moves up to 1 tick under every NEW confirmed
                                3/5/10-bar swing low (never down)
target     tgt_swing            limit at the latest confirmed 5-bar swing high (the "next swing")
target     tgt_fib382/618/1272  limit at the 0.382 / 0.618 retracement, or 1.272 extension, of the leg from that swing
                                high down to the pattern's low
control    shuffle_<rule>       same entries, holding times drawn at random from <rule>'s own holding times
"Fading"/"opposite" close rules trigger on the bar the condition BECOMES true after entry (a pullback long that is
already below EMA 8 at entry is not exited until price closes back above and then below it again).
Close rules are run without a stop and with the pattern stop; trailing and target rules always use the pattern stop.
Writes out/exits_{SYM}_{TF}.csv: $ per micro contract after costs, per pattern/direction/exit/stop.
"""
import sys
import time
import warnings

import numpy as np
import pandas as pd

import exits as ex
import signals as sg

warnings.filterwarnings("ignore")
SYM, TF = sys.argv[1], int(sys.argv[2])
t0 = time.time()
spec = sg.SPEC[SYM]
USD, COST, TICK = spec["usd"], spec["cost"], spec["tick"]
b = sg.bars(SYM, TF)
c = sg.context(b, tick=TICK)
p = sg.patterns(b, c, tick=TICK)
O, H, L, C = (b[x].to_numpy() for x in "OHLC")
seg = b.seg.to_numpy(); run = b.run.to_numpy(); n = len(b)
allowed, forced = ex.session_frame(b, TF)
raw_ok = (b.H - b.L).rolling(14).mean().gt(TICK).to_numpy()
years = (b.index[-1] - b.index[0]).days / 365.25
yr = b.index.year.to_numpy()
ema8, ema20, mom, atr = (c[x].to_numpy() for x in ("ema8", "ema20", "mom14", "atr14"))
del c
P = {k: p[k].to_numpy() for k in ex.DIRECTIONAL}
del p

# swing structure for k = 3, 5, 10: level confirmed at each bar (NaN otherwise) and the latest confirmed level
SW = {}
for k in (3, 5, 10):
    lo, hi = sg.pivots(b, k)
    clo = np.full(n, np.nan); chi = np.full(n, np.nan)
    q = np.flatnonzero(lo); clo[q + k] = L[q]
    q = np.flatnonzero(hi); chi[q + k] = H[q]
    last_lo = pd.Series(clo).groupby(run).ffill().to_numpy()
    last_hi = pd.Series(chi).groupby(run).ffill().to_numpy()
    SW[k] = dict(conf_lo=clo, conf_hi=chi, lo=last_lo, hi=last_hi)
del b
print(f"{SYM} {TF}m: {n:,} bars, prepared in {time.time() - t0:.0f}s", flush=True)


def prev(a):
    return np.r_[np.nan, a[:-1]]


# bar-level exit conditions: (exit for LONGS, exit for SHORTS)
cnt_bear = {}; cnt_bull = {}
for name, cols in (("classic", ex.CLASSIC), ("any", ex.DIRECTIONAL)):
    cnt_bear[name] = sum((P[k] == -1).astype(np.int16) for k in cols)
    cnt_bull[name] = sum((P[k] == 1).astype(np.int16) for k in cols)
lvl5 = SW[5]
with np.errstate(invalid="ignore"):
    COND = {
        "opp_classic": (cnt_bear["classic"] >= 1, cnt_bull["classic"] >= 1),
        "opp_any": (cnt_bear["any"] >= 1, cnt_bull["any"] >= 1),
        "opp_any2": (cnt_bear["any"] >= 2, cnt_bull["any"] >= 2),
        "opp_classic_at_level": ((cnt_bear["classic"] >= 1) & (H >= lvl5["hi"] - 0.5 * atr),
                                 (cnt_bull["classic"] >= 1) & (L <= lvl5["lo"] + 0.5 * atr)),
        "choch_3": (ex.fresh(C < SW[3]["lo"]), ex.fresh(C > SW[3]["hi"])),
        "choch_5": (ex.fresh(C < SW[5]["lo"]), ex.fresh(C > SW[5]["hi"])),
        "mom_turn": (ex.fresh((mom < prev(mom)) & (prev(mom) < prev(prev(mom)))),
                     ex.fresh((mom > prev(mom)) & (prev(mom) > prev(prev(mom))))),
        "mom_cross100": (ex.fresh(mom < 100), ex.fresh(mom > 100)),
        "ema8_cross": (ex.fresh(C < ema8), ex.fresh(C > ema8)),
        "ema20_cross": (ex.fresh(C < ema20), ex.fresh(C > ema20)),
    }
NEXT = {k: (ex.next_true(a), ex.next_true(z)) for k, (a, z) in COND.items()}
del COND, cnt_bear, cnt_bull
FAMILY = {"opp_same": "opposite", "opp_classic": "opposite", "opp_any": "opposite", "opp_any2": "opposite",
          "opp_classic_at_level": "opposite", "choch_3": "opposite", "choch_5": "opposite", "mom_turn": "fading",
          "mom_cross100": "fading", "ema8_cross": "fading", "ema20_cross": "fading"}
CLOSE_RULES = list(FAMILY)
rng = np.random.default_rng(2026)


def stats(pnl, hold_bars, by_signal, how, mfe_pts, ent_idx):
    w, l = pnl[pnl > 0], pnl[pnl <= 0]
    y = yr[ent_idx]
    sd = pnl.std(ddof=1)
    out = dict(n=len(pnl), per_year=len(pnl) / years, usd=pnl.mean(), usd_median=np.median(pnl), hit=(pnl > 0).mean(),
               t=pnl.mean() / (sd / np.sqrt(len(pnl))) if len(pnl) > 2 and sd > 0 else np.nan,
               pf=w.sum() / -l.sum() if l.sum() < 0 else np.nan, avg_win=w.mean() if len(w) else np.nan,
               avg_loss=l.mean() if len(l) else np.nan, worst=pnl.min(), best=pnl.max(),
               usd_per_year=pnl.sum() / years, hold_min_mean=hold_bars.mean() * TF,
               hold_min_median=np.median(hold_bars) * TF, exit_by_rule=by_signal.mean(),
               exit_by_stop=(how == 1).mean(), exit_by_target=(how == 2).mean(),
               mfe_usd=(mfe_pts * USD).mean(), gave_back_usd=(mfe_pts * USD - (pnl + COST)).mean())
    for lab, a, z in (("2010_17", 0, 2017), ("2018_21", 2018, 2021), ("2022_26", 2022, 9999), ("2018plus", 2018, 9999)):
        m = (y >= a) & (y <= z)
        out[f"usd_{lab}"] = pnl[m].mean() if m.sum() >= 20 else np.nan
        out[f"n_{lab}"] = int(m.sum())
    return out


rows = []
for name in ex.DIRECTIONAL:
    v = P[name]
    same = (ex.next_true(v == -1), ex.next_true(v == 1))
    for d0 in (1, -1):
        i = np.flatnonzero(v == d0)
        i = i[i < n - 1]
        e = i + 1
        ok = (seg[e] == seg[i]) & allowed[e] & raw_ok[i] & (forced[e] >= e)
        i, e = i[ok], e[ok]
        if len(i) < 30:
            continue
        d = np.full(len(i), d0)
        F = forced[e]
        ref = ex.pattern_extreme(L, H, i, ex.SPAN.get(name, 1), d)
        stop_lvl = ref - d * TICK
        sims = []          # (exit, family, x_end, x_price, by_signal, stop, extra kwargs)
        for rule in CLOSE_RULES:
            nb, nu = same if rule == "opp_same" else NEXT[rule]
            x_end, x_price, sig = ex.plan_exits(e, d, forced, nb, nu, O, C)
            for st_name in ("none", "pattern"):
                sims.append((rule, FAMILY[rule], x_end, x_price, sig, st_name, {}))
            hold = np.where(sig == 1, x_end + 1 - e, F + 1 - e)
            tgt = e + rng.permutation(hold)
            early = tgt <= F
            sims.append((f"shuffle_{rule}", "control", np.where(early, tgt - 1, F),
                         np.where(early, O[np.minimum(tgt, n - 1)], C[F]), np.zeros(len(i), np.int8), "none", {}))
        zero = np.zeros(len(i), np.int8)
        for h in (5, 10, 20):
            tgt = np.minimum(i + h, F)
            for st_name in ("none", "pattern"):
                sims.append((f"fixed_{h}", "baseline", tgt, C[tgt], zero, st_name, {}))
        for st_name in ("none", "pattern"):
            sims.append(("hold_1645", "baseline", F, C[F], zero, st_name, {}))
        for k in (3, 5, 10):
            sims.append((f"trail_{k}", "trailing", F, C[F], zero, "pattern",
                         dict(trail_lo=SW[k]["conf_lo"], trail_hi=SW[k]["conf_hi"], tick=TICK)))
        swing = np.where(d > 0, lvl5["hi"][i], lvl5["lo"][i])
        leg = swing - ref                                   # signed: + for longs (swing high above the low)
        for tname, frac in (("tgt_swing", 1.0), ("tgt_fib382", 0.382), ("tgt_fib618", 0.618), ("tgt_fib1272", 1.272)):
            tg = ref + frac * leg
            valid = np.isfinite(tg) & (d * (tg - O[e]) > TICK)
            tg = np.where(valid, tg, np.nan)
            sims.append((tname, "target", F, C[F], zero, "pattern", dict(target=tg, tick=TICK, _valid=valid.mean())))
        for rule, fam, x_end, x_price, sig, st_name, kw in sims:
            kw = dict(kw); tv = kw.pop("_valid", np.nan)
            st = stop_lvl if st_name == "pattern" else None
            px, xb, how, mfe = ex.simulate(O, H, L, C, e, d, x_end, x_price, st, **kw)
            pnl = d * (px - O[e]) * USD - COST
            hold = np.where(how > 0, xb + 1 - e, x_end + 1 - e)
            r = dict(market=SYM, micro=spec["micro"], tf=TF, pattern=name,
                     direction="bullish" if d0 > 0 else "bearish", family=fam, exit=rule, stop=st_name,
                     target_valid=tv)
            r.update(stats(pnl, hold, (sig == 1) & (how == 0), how, mfe, i))
            rows.append(r)
    print(f"  {name} done ({time.time() - t0:.0f}s)", flush=True)

pd.DataFrame(rows).to_csv(f"out/exits_{SYM}_{TF}.csv", index=False)
print(f"{SYM} {TF}m exit study: {len(rows)} rows in {time.time() - t0:.0f}s", flush=True)
