"""Research only: opening-range breakout grid (not part of the trading system). Run from the project folder.
Entries exactly as lit_p5_orb.py: family A = trade the first k-minute candle's direction at the next bar's open;
family B = stop orders 1 tick beyond the first k-minute range until 11:00, first fill wins. k in {1, 3, 5}.
Published stop = the range's other end (risk R0). Grid on top of each entry:
  stop size   0.5 / 1 / 1.5 / 2 x R0 from the entry fill
  target      1, 2, 3, 5, 10 R (limit, needs a 1-tick trade-through) or none (exit at the close)
  management  none | breakeven once +1R | stop to +1R once +2R | trail 1R behind the best price | trail 2R
Fills as lit_p5: market/stop 1 tick adverse, a stop gapped through fills at the open, stop beats target in the same
bar, a stop-order entry's own bar can stop out but not reach the target, management moves apply from the next bar.
Exit at the 15:59 close (12:59 on early-close days). Skip trades whose risk is under the published minimum (2 x cost).
Costs: 1 tick each way + $1.00 per round trip. Results in R (equal risk per trade) and $ at 1 micro.
Walk-forward: each year from 2013 trades the combination with the most R in all earlier years."""
import sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import lit_p5_orb as p5

pd.set_option("display.width", 230)
TK = p5.TICK
SL = TK * float(sys.argv[1]) if len(sys.argv) > 1 else TK      # slippage per fill
ONLY = sys.argv[2].split(",") if len(sys.argv) > 2 else ["NQ", "ES"]
STOPS, TARGETS = [0.5, 1.0, 1.5, 2.0], [1, 2, 3, 5, 10, None]
MGMT = ["none", "be@1R", "+1R@2R", "trail1R", "trail2R"]
COMBOS = [(t, m) for t in TARGETS for m in MGMT]


def entries(fam, k, sess, g, Cff, min_R):
    """Per trading day: direction, entry slot, entry fill, published risk R0, exit slot (NaN where no trade)."""
    O, H, L = g["Open"], g["High"], g["Low"]
    rows = []
    for row in sess.itertuples(index=False):
        if not row.trade_ok:
            continue
        i = row.di
        hi, lo = np.nanmax(H[i, :k]), np.nanmin(L[i, :k])
        if fam == "A":
            oc, cc = O[i, 0], Cff[i, k - 1]
            if np.isnan(O[i, k]) or cc == oc:
                continue
            d = 1 if cc > oc else -1
            s_e, ref = k, O[i, k]
        else:
            if (hi + 2 * TK) - lo < min_R:
                continue
            up = H[i, k:p5.B_LAST_SLOT + 1] >= hi + TK
            dn = L[i, k:p5.B_LAST_SLOT + 1] <= lo - TK
            iu = int(np.argmax(up)) if up.any() else p5.BIG
            idn = int(np.argmax(dn)) if dn.any() else p5.BIG
            if iu == p5.BIG and idn == p5.BIG:
                continue
            if iu != idn:
                d = 1 if iu < idn else -1
            else:
                o = O[i, k + iu]
                d = 1 if (hi + TK - o) <= (o - (lo - TK)) else -1
            s_e = k + (iu if d > 0 else idn)
            o = O[i, s_e]
            ref = max(hi + TK, o) if d > 0 else min(lo - TK, o)
        fill = ref + d * SL
        R0 = d * (fill - (lo if d > 0 else hi))
        rows.append((i, row.date, d, s_e, fill, R0, row.exit_slot))
    return pd.DataFrame(rows, columns=["di", "date", "d", "s_e", "fill", "R0", "sx"])


def simulate(E, g, Cff, stop_mult, fam, min_R, ppt):
    """All target x management combos for one (family, k, stop size); vectorized across days and combos."""
    E = E[E.R0 * stop_mult >= min_R].reset_index(drop=True)
    n, nc = len(E), len(COMBOS)
    di, d = E.di.to_numpy(), E.d.to_numpy(float)[:, None]
    # signed prices: shorts become longs in a mirrored world
    O = g["Open"][di] * d; Cc = Cff[di] * d
    H = np.where(d > 0, g["High"][di], -g["Low"][di]); L = np.where(d > 0, g["Low"][di], -g["High"][di])
    fill = (E.fill.to_numpy() * E.d.to_numpy())[:, None] * np.ones((1, nc))
    R = (E.R0.to_numpy() * stop_mult)[:, None] * np.ones((1, nc))
    stop = np.floor((fill - R) / TK + 1e-9) * TK                         # stop order sits on the tick grid
    tgt_mult = np.array([np.nan if t is None else t for t, _ in COMBOS])[None, :]
    tgt = np.ceil((fill + tgt_mult * R) / TK - 1e-9) * TK
    mg = np.array([m for _, m in COMBOS])[None, :]
    s_e, sx = E.s_e.to_numpy()[:, None], E.sx.to_numpy()[:, None]
    best = fill.copy()
    out = np.full((n, nc), np.nan)
    open_ = np.ones((n, nc), bool)
    for t in range(int(s_e.min()), p5.NSLOT):
        act = open_ & (t >= s_e) & (t <= sx)
        if not act.any():
            continue
        lo, hi, op = L[:, t:t + 1], H[:, t:t + 1], O[:, t:t + 1]
        first = t == s_e
        hit = act & (lo <= stop)
        px = np.where(first, stop, np.minimum(stop, np.where(np.isnan(op), stop, op))) - SL
        out = np.where(hit, px - fill, out); open_ &= ~hit; act &= ~hit
        can_tgt = act & ~np.isnan(tgt) & ~(first & (fam == "B"))
        th = can_tgt & (hi >= tgt + TK)
        out = np.where(th, tgt - fill, out); open_ &= ~th; act &= ~th
        endnow = act & (t == sx)
        out = np.where(endnow, Cc[:, t:t + 1] - SL - fill, out); open_ &= ~endnow; act &= ~endnow
        # management for the next bar (uses this bar's high only after it has closed)
        best = np.where(act, np.fmax(best, hi), best)
        gain = (best - fill) / R
        new = stop.copy()
        new = np.where((mg == "be@1R") & (gain >= 1), np.maximum(new, fill), new)
        new = np.where((mg == "+1R@2R") & (gain >= 2), np.maximum(new, fill + R), new)
        for m, w in (("trail1R", 1.0), ("trail2R", 2.0)):
            new = np.where(mg == m, np.maximum(new, np.floor((best - w * R) / TK + 1e-9) * TK), new)
        stop = np.where(act, new, stop)
    net_pts = out - p5.COMM / ppt
    return E, net_pts / R, net_pts * ppt


def stats(R, usd, dates, years):
    d = pd.Series(R).groupby(dates).sum()
    y = pd.Series(R).groupby(years).sum()
    return dict(trades=len(R), avg_R=R.mean(), total_R=R.sum(), t=d.mean() / (d.std() / np.sqrt(len(d))),
                usd=usd.sum(), yrs_up=f"{int((y > 0).sum())}/{len(y)}", R_2010_17=y.loc[:2017].sum(),
                R_2018_26=y.loc[2018:].sum())


for sym in ONLY:
    mk = p5.MARKETS[sym]
    dates, g, inst = p5.load_market(sym)
    sess, Cff, _ = p5.build_sessions(sym, dates, g, inst)
    rows, yearly, riskpts = [], {}, {}
    for fam in ("A", "B"):
        for k in (1, 3, 5):
            E0 = entries(fam, k, sess, g, Cff, mk["min_R"])
            for sm in STOPS:
                E, Rm, Um = simulate(E0, g, Cff, sm, fam, mk["min_R"], mk["ppt"])
                yrs = pd.DatetimeIndex(E.date).year.to_numpy()
                riskpts[(f"{fam}{k}", sm)] = (E.R0 * sm).median()
                for c, (tg, m) in enumerate(COMBOS):
                    key = (f"{fam}{k}", sm, "close" if tg is None else f"{tg}R", m)
                    rows.append(dict(entry=key[0], stop=sm, target=key[2], manage=m,
                                     **stats(Rm[:, c], Um[:, c], E.date.to_numpy(), yrs)))
                    yearly[key] = pd.Series(Rm[:, c]).groupby(yrs).sum()
    r = pd.DataFrame(rows)
    pub = r[(r.entry == "A5") & (r.stop == 1.0) & (r.target == "10R") & (r.manage == "none")].iloc[0]
    print(f"\n################ {mk['micro']}: {len(r)} combinations ################")
    print(f"Check vs lit_p5 published A5 (10R target, stop at range end): {pub.trades} trades, ${pub.usd:,.2f}, "
          f"{pub.total_R:.1f} R, t {pub.t:.2f}")
    print(f"Combinations with positive total R: {(r.total_R > 0).sum()} of {len(r)}; with t > 2: {(r.t > 2).sum()}; "
          f"t > 3: {(r.t > 3).sum()}")
    print(f"Slippage {SL / TK:g} tick(s) per fill. Median stop distance (points): " + ", ".join(f"{a}/{b:g}x {v:.2f}" for (a, b), v in riskpts.items() if a in ("A1", "A3", "A5")))
    print("\nTop 15 by total R (in-sample, 2010-2026):")
    print(r.sort_values("total_R", ascending=False).head(15).to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
    for col in ("entry", "stop", "target", "manage"):
        s = r.groupby(col).agg(combos=("total_R", "size"), median_total_R=("total_R", "median"),
                               best_total_R=("total_R", "max"), share_positive=("total_R", lambda x: (x > 0).mean()))
        print(f"\nBy {col}:\n" + s.round(2).to_string())
    Y = pd.DataFrame(yearly).fillna(0.0)
    pubk = ("A5", 1.0, "10R", "none")
    wf, picks = [], []
    for yr in range(2013, 2027):
        best = Y.loc[:yr - 1].sum().idxmax()
        wf.append(Y.loc[yr, best]); picks.append(f"{yr}: {best[0]}/{best[1]:g}x/{best[2]}/{best[3]}")
    wfs = pd.Series(wf, index=range(2013, 2027))
    print(f"\nWALK-FORWARD 2013-2026 (each year uses the best combination of all earlier years): "
          f"{wfs.sum():.1f} R, years up {(wfs > 0).sum()}/14 | published A5 same years: {Y.loc[2013:, pubk].sum():.1f} R")
    print("picks: " + "; ".join(picks))
