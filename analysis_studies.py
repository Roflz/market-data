"""
Analysis studies for the Studies tab of model_heatmap_gui.py: how the two breakout models' results change with the
stop size, a stop cap, the time and width of the stop, the entry time, the day type, the year and the skip rules.
Every value is NET $ AT 1 MNQ MICRO after costs (1 tick each way + $1.00 per round trip = 1 NQ point = $2.00),
because the account trades a fixed contract size.

Trade sets
  live trades     chosen_models_trades.csv / chosen_models_skipped.csv as written by chosen_models.py.
  overnight_break re-simulated with chosen_models.py's own engine call (exits_engine.run, 'hold', setup_rule signals)
                  and its filters (cash days, no expiry Fridays, R1); at the live stop (2 x ATR) it is the live set
                  trade for trade. Other stops / caps re-run the engine (one position at a time, so a different stop
                  can change which later signal is taken). Caps: initial risk = min(2 x ATR, cap x raw price).
  opening_range   stop size and cap sweeps use the research grid simulator (scratchpad orb_grid.py, copied here) on
                  the live opening_range dates that have no data gap in the session (the grid skips gap days), so
                  its 'current' total differs a little from the live CSV. The stop is k x the first candle's range
                  measured from the entry fill; a cap shrinks it to cap x entry price when that is smaller.
                  Stop time and stop width use the live rule itself (chosen_models.opening_range, with the exit
                  minute kept), i.e. exactly the live trades.
Studies (study id: title)
  S1  Stop size                      x = stop multiple (opening range x candle, overnight break x ATR)
  S2  Stop cap (share of price)      x = cap as % of price, 'none' = the live rule
  S3  When stops are hit             count of stop-outs by the time the stop filled (start of the bar, NY time)
  S3b When stops are hit: $ lost     total $ of those stop-outs
  S4  Stop width: total $            deciles of the stop width (risk as a share of price), cut points from the
  S4b Stop width: $ per trade        model's trades of the previous 250 trading days (expanding before that;
                                     the first 30 trades have no history and are left out)
  S5  Entry time: total $            overnight break only, by hour of the entry fill
  S5b Entry time: $ per trade
  S6  Day type: $ per day            both breakout models summed per date (model 'all')
  S6b Day type: total $
  S7  By year                        live CSV, each model and the 3-model book (model 'all')
  S8  Skip rules                     $ saved by each rule = minus the net $ of the trades it removed; band = the
                                     same for skipping as many random trades of that model (5th-95th percentile)
  S1/S2 also carry an 'all years (2-tick fills)' series (2 ticks slippage per fill instead of 1).
Output data/analysis/studies.csv, long format, one row per point:
  model, study, title, x_label, x, x_order, y_label, y, series, y_lo, y_hi, is_current, note, source
  Append-safe: save_studies() replaces only the (model, study) pairs it is given and keeps every other row, so
  another script can add a study with
      from analysis_studies import save_studies
      save_studies(frame_with_those_columns)
  and the GUI shows it (x numeric -> line chart, x text -> bars; is_current marks the live setting).
Usage  PYTHONPATH=./pylib python3 analysis_studies.py [--out data/analysis/studies.csv] [--skip-sweeps]
       --skip-sweeps keeps the existing S1/S2 rows (the slow part) and recomputes the rest.
"""
import argparse
import gc
import os
import time
import warnings

import numpy as np
import pandas as pd

import calendar_days as cd
import chosen_models as cm
import exits_engine as ee
import lit_p5_orb as p5
import setup_rule

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "analysis", "studies.csv")
COLUMNS = ["model", "study", "title", "x_label", "x", "x_order", "y_label", "y", "series", "y_lo", "y_hi",
           "is_current", "note", "source"]
SYM, TK = "NQ", p5.TICK
OB_FIRST_YEAR = 2011                        # exits_compare.FIRST_YEAR: first year of the 5-min engine data
ERAS = [("all years", None, None), ("2010-2017", 2010, 2017), ("2018-2026", 2018, 2026), ("2024-2026", 2024, 2026)]
TWO_TICK = " (2-tick fills)"
OB_STOPS = [1.0, 1.5, 2.0, 3.0, 4.0]
ORB_STOPS = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, None]          # None = no stop
CAPS = [0.0010, 0.0015, 0.0020, 0.0025, 0.0030, 0.0040, 0.0050]
TIME_BUCKETS = [(575, 585, "9:35-9:45"), (585, 600, "9:45-10:00"), (600, 630, "10:00-10:30"),
                (630, 660, "10:30-11:00"), (660, 720, "11:00-12:00"), (720, 780, "12:00-13:00"),
                (780, 840, "13:00-14:00"), (840, 900, "14:00-15:00"), (900, 24 * 60, "after 15:00")]
WIDTH_WINDOW, WIDTH_MIN_HIST = 250, 30
N_RANDOM, SEED = 5000, 20261108
NAMES = {"overnight_break": "Overnight break", "opening_range": "Opening range", "expiry_fade": "Expiry fade",
         "all": "All three models"}
SRC = "analysis_studies.py"


# ---------------------------------------------------------------------------------------------- output
def save_studies(new, path=OUT):
    """Write study rows; rows of other (model, study) pairs already in the file are kept unchanged."""
    new = pd.DataFrame(new).reindex(columns=COLUMNS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        old = pd.read_csv(path, dtype={"x": str})
        keys = set(zip(new.model.astype(str), new.study.astype(str)))
        old = old[[(m, s) not in keys for m, s in zip(old.model.astype(str), old.study.astype(str))]]
        new = pd.concat([old.reindex(columns=COLUMNS), new], ignore_index=True)
    tmp = path + ".tmp"
    new.to_csv(tmp, index=False)
    os.replace(tmp, path)
    return new


class Rows:
    """Collects the long-format rows of one run."""

    def __init__(self):
        self.rows = []

    def add(self, model, study, title, x_label, y_label, note, source, points):
        """points: iterable of (x, y, series[, is_current[, y_lo, y_hi]]); x_order follows first appearance."""
        order = {}
        for p in points:
            x, y, series = p[0], p[1], p[2]
            cur = bool(p[3]) if len(p) > 3 else False
            lo, hi = (p[4], p[5]) if len(p) > 5 else (np.nan, np.nan)
            order.setdefault(x, len(order))
            self.rows.append(dict(model=model, study=study, title=title, x_label=x_label, x=x, x_order=order[x],
                                  y_label=y_label, y=round(float(y), 2) if np.isfinite(y) else np.nan, series=series,
                                  y_lo=lo, y_hi=hi, is_current=cur, note=note, source=source))

    def frame(self):
        return pd.DataFrame(self.rows, columns=COLUMNS)


def era_sums(dates, usd, eras=ERAS):
    s = pd.Series(np.asarray(usd, float), index=pd.DatetimeIndex(dates))
    out = {}
    for name, a, b in eras:
        out[name] = s.sum() if a is None else s[(s.index.year >= a) & (s.index.year <= b)].sum()
    return out


# ---------------------------------------------------------------------------------------------- overnight break
class Overnight:
    """chosen_models.overnight_break's engine run for NQ only, with the stop size, cap and slippage as inputs."""

    def __init__(self, cash, expiry, after_drop, ds):
        b = pd.read_pickle(f"data/x5_{SYM}.pkl")
        self.D = D = ee.Day(b[b.index.year >= OB_FIRST_YEAR])
        del b
        D.pos = pd.Index(D.idx)
        F = pd.read_pickle(f"data/fut_features_{SYM}.pkl")      # same entry set as exits_compare.entry_sets
        bar = D.pos.get_indexer(pd.DatetimeIndex(F["ts"]) - pd.Timedelta(minutes=4))
        sig = setup_rule.overnight_break(F["X"], F["ts"])
        m = (sig != 0) & (bar >= 0)
        self.sigs = sorted(zip(bar[m].tolist(), sig[m].tolist()))
        del F
        gc.collect()
        self.cash, self.expiry, self.after_drop = cash, expiry, after_drop
        self.adj = (ds.close_adj - ds.close_raw)
        self.mins = (D.idx.hour * 60 + D.idx.minute).to_numpy()

    def run(self, k0=2.0, cap=None, slip_ticks=1):
        D, sp = self.D, ee.SPEC[SYM]
        extra = None
        if cap is not None:
            extra = {}
            for i, _ in self.sigs:
                raw = D.Close[i] - self.adj.get(pd.Timestamp(D.sess[i]), 0.0)
                extra[i] = {"R_pts": min(k0 * D.atr5[i], cap * raw)}
        ee.SLIP = slip_ticks * TK
        try:
            t = ee.run(D, self.sigs, "hold", k0=k0, extra=extra)
        finally:
            ee.SLIP = TK
        b = t.bar.to_numpy()
        date = pd.to_datetime(D.sess[b])
        raw = D.Close[b] - self.adj.reindex(date).to_numpy()
        net = t.pts.to_numpy() - sp["comm"] / sp["usd"]
        out = pd.DataFrame({"date": date, "side": np.where(t.dir > 0, "long", "short"), "exit": t.exit.to_numpy(),
                            "usd": net * sp["usd"], "width": t.R_pts.to_numpy() / raw,
                            "entry_min": self.mins[b + 1], "exit_min": self.mins[b + t.hold_bars.to_numpy()]})
        keep = date.isin(self.cash) & ~date.isin(self.expiry) & ~date.isin(self.after_drop)
        return out[keep].reset_index(drop=True)


# ---------------------------------------------------------------------------------------------- opening range
def orb_entries(sess, g, Cff, slip, days):
    """orb_grid.entries('A', 5, ...): first 5-min candle direction, entry at the 9:35 open + slippage, risk R0 from
    the fill to the candle's other end; only days without a data gap (trade_ok) that are in `days`."""
    k = cm.K
    O, H, L = g["Open"], g["High"], g["Low"]
    rows = []
    for r in sess.itertuples(index=False):
        if not r.trade_ok or r.date not in days:
            continue
        i = r.di
        hi, lo = np.nanmax(H[i, :k]), np.nanmin(L[i, :k])
        oc, cc = O[i, 0], Cff[i, k - 1]
        if np.isnan(O[i, k]) or cc == oc:
            continue
        d = 1 if cc > oc else -1
        fill = O[i, k] + d * slip
        rows.append((i, r.date, d, k, fill, d * (fill - (lo if d > 0 else hi)), r.exit_slot))
    return pd.DataFrame(rows, columns=["di", "date", "d", "s_e", "fill", "R0", "sx"])


def orb_simulate(E, g, Cff, stop_mult, slip, ppt):
    """orb_grid.simulate for the live exit only (no target, no management, out at the close), vectorised across
    days. stop_mult None = no stop. Returns net $ per trade at 1 micro."""
    di, d = E.di.to_numpy(), E.d.to_numpy(float)[:, None]
    O, Cc = g["Open"][di] * d, Cff[di] * d                          # mirrored prices: shorts become longs
    L = np.where(d > 0, g["Low"][di], -g["High"][di])                # only the adverse side matters here
    fill = E.fill.to_numpy() * E.d.to_numpy()
    if stop_mult is None:
        stop = np.full(len(E), -np.inf)
    else:
        stop = np.floor((fill - E.R0.to_numpy() * stop_mult) / TK + 1e-9) * TK
    s_e, sx = E.s_e.to_numpy(), E.sx.to_numpy()
    out = np.full(len(E), np.nan)
    open_ = np.ones(len(E), bool)
    for t in range(int(s_e.min()), p5.NSLOT):
        act = open_ & (t >= s_e) & (t <= sx)
        if not act.any():
            continue
        lo, op = L[:, t], O[:, t]
        hit = act & (lo <= stop)
        px = np.where(t == s_e, stop, np.minimum(stop, np.where(np.isnan(op), stop, op))) - slip
        out = np.where(hit, px - fill, out)
        open_ &= ~hit
        act &= ~hit
        end = act & (t == sx)
        out = np.where(end, Cc[:, t] - slip - fill, out)
        open_ &= ~end
    return (out - p5.COMM / ppt) * ppt


def orb_live(expiry, sess, g, Cff, days):
    """chosen_models.opening_range unchanged, plus the exit minute and the stop width; only dates in `days`."""
    ppt, min_R, K = p5.MARKETS[SYM]["ppt"], p5.MARKETS[SYM]["min_R"], cm.K
    O, H, L = g["Open"], g["High"], g["Low"]
    rows = []
    for r in sess.itertuples(index=False):
        i = r.di
        if r.date in expiry or r.date not in days or np.isnan(O[i, 0]) or np.isnan(O[i, K]):
            continue
        oc, cc = O[i, 0], Cff[i, K - 1]
        if cc == oc:
            continue
        d = 1 if cc > oc else -1
        stop = np.nanmin(L[i, :K]) if d > 0 else np.nanmax(H[i, :K])
        if d * (cc + d * p5.TICK - stop) < min_R:
            continue
        ref, fill = O[i, K], O[i, K] + d * p5.TICK
        s_x = r.exit_slot
        if d * (fill - stop) <= 0:
            xs, xfill, why, R = K, ref - d * p5.TICK, "stop", d * (cc + d * p5.TICK - stop)
        else:
            xs, _, xfill, why = p5.run_trade(H[i], L[i], O[i], Cff[i, s_x], K, s_x, d, stop, None, True)
            R = d * (fill - stop)
        net_pts = d * (xfill - fill) - p5.COMM / ppt
        rows.append(dict(date=r.date, side="long" if d > 0 else "short", exit=why, usd=net_pts * ppt,
                         width=R / ref, exit_min=570 + int(xs)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------------------------- studies
def bucket_label(m):
    for a, b, lab in TIME_BUCKETS:
        if a <= m < b:
            return lab
    return None


def study_stop_times(R, model, T, source):
    s = T[T.exit == "stop"].assign(bucket=lambda x: x.exit_min.map(bucket_label))
    n = s.groupby("bucket").size()
    u = s.groupby("bucket").usd.sum()
    first = 9 * 60 + 35 if model == "opening_range" else 9 * 60 + 40
    labels = [lab for (a, b, lab) in TIME_BUCKETS if b > first]
    R.add(model, "S3", "When stops are hit", "time the stop filled (NY, start of the bar)", "stop-outs",
          f"Number of the {len(s):,} stop-outs ({len(s) / len(T):.0%} of {len(T):,} live trades) by the time of day "
          "the stop filled; a tall early bar means many trades are stopped soon after entry.", source,
          [(lab, float(n.get(lab, 0)), "all years") for lab in labels])
    R.add(model, "S3b", "When stops are hit: $ lost", "time the stop filled (NY, start of the bar)",
          "net $ of those stop-outs (1 micro)",
          f"Total net $ of the stop-outs that filled in each time window (all {len(s):,} add up to "
          f"${s.usd.sum():,.0f}); it shows when the stop costs the most.", source,
          [(lab, float(u.get(lab, 0.0)), "all years") for lab in labels])


def width_deciles(T, cal):
    """Decile (1..10) of each trade's stop width against the same model's trades of the previous WIDTH_WINDOW
    trading days (expanding before that); NaN when fewer than WIDTH_MIN_HIST earlier trades."""
    pos = cal.get_indexer(pd.DatetimeIndex(T.date))
    w, dec = T.width.to_numpy(float), np.full(len(T), np.nan)
    for k in range(len(T)):
        hist = (pos < pos[k]) & (pos >= pos[k] - WIDTH_WINDOW) & np.isfinite(w)
        if hist.sum() < WIDTH_MIN_HIST or not np.isfinite(w[k]):
            continue
        cuts = np.quantile(w[hist], np.arange(1, 10) / 10)
        dec[k] = np.searchsorted(cuts, w[k], side="right") + 1
    return dec


def study_widths(R, model, T, cal, source):
    T = T.sort_values("date").reset_index(drop=True)
    T["dec"] = width_deciles(T, cal)
    U = T.dropna(subset=["dec"])
    g = U.groupby("dec").usd
    lab = {1: "D1 narrowest", 10: "D10 widest"}
    xs = [(lab.get(k, f"D{k}"), k) for k in range(1, 11)]                # text labels: drawn as bars
    med = U.width.median() * 100
    note_tail = (f"Deciles are cut from the trades of the previous {WIDTH_WINDOW} trading days, so they are known "
                 f"at entry ({len(U):,} trades; median stop {med:.2f}% of price).")
    R.add(model, "S4", "Stop width: total $", "stop width decile (1 = narrowest stop)", "net $ (1 micro)",
          "Total net $ of the trades in each stop-width decile. " + note_tail, source,
          [(x, g.sum().get(k, np.nan), "total $") for x, k in xs])
    R.add(model, "S4b", "Stop width: $ per trade", "stop width decile (1 = narrowest stop)",
          "net $ per trade (1 micro)",
          "Average net $ per trade in each stop-width decile. " + note_tail, source,
          [(x, g.mean().get(k, np.nan), "$ per trade") for x, k in xs])


def study_entry_hour(R, T, source):
    h = (T.entry_min // 60).astype(int)
    g = T.groupby(h).usd
    xs = [(f"{k}:00-{k + 1}:00" if k > 9 else "9:40-10:00", k) for k in sorted(h.unique())]
    n = g.size()
    R.add("overnight_break", "S5", "Entry time: total $", "time of the entry fill (NY)", "net $ (1 micro)",
          "Total net $ of the live trades by the hour they were entered; "
          + ", ".join(f"{x.split('-')[0]} {n[k]:,}" for x, k in xs) + " trades.", source,
          [(x, g.sum()[k], "total $") for x, k in xs])
    R.add("overnight_break", "S5b", "Entry time: $ per trade", "time of the entry fill (NY)",
          "net $ per trade (1 micro)",
          "Average net $ per trade by the hour of entry; later hours have fewer trades, so their averages are "
          "noisier.", source, [(x, g.mean()[k], "$ per trade") for x, k in xs])


def study_day_type(R, live):
    B = live[live.model.isin(["overnight_break", "opening_range"])]
    ob = B[B.model == "overnight_break"].groupby("date").agg(ob_side=("side", "first"), ob_usd=("usd", "sum"))
    orb = B[B.model == "opening_range"].groupby("date").agg(or_side=("side", "first"), or_usd=("usd", "sum"))
    D = ob.join(orb, how="outer")
    D["usd"] = D.ob_usd.fillna(0) + D.or_usd.fillna(0)
    D["kind"] = np.where(D.ob_side.isna(), "only opening range", np.where(
        D.or_side.isna(), "only overnight break",
        np.where(D.ob_side == D.or_side, "both, same direction", "both, opposite")))
    kinds = ["both, same direction", "both, opposite", "only opening range", "only overnight break"]
    y = D.index.year
    eras = [("2010-2017", y <= 2017), ("2018-2026", y >= 2018)]
    n = D.kind.value_counts()
    cnt = ", ".join(f"{k} {n.get(k, 0):,}" for k in kinds)
    src = f"{SRC} (chosen_models_trades.csv)"
    R.add("all", "S6", "Day type: $ per day", "day type (overnight break vs opening range)",
          "net $ per day, both models (1 micro each)",
          f"Average combined net $ of the two breakout models on each kind of day (overnight break side = its first "
          f"trade); days: {cnt}.", src,
          [(k, D[m & (D.kind == k)].usd.mean(), name) for name, m in eras for k in kinds])
    R.add("all", "S6b", "Day type: total $", "day type (overnight break vs opening range)",
          "net $, both models (1 micro each)",
          "Total combined net $ of the two breakout models on each kind of day; with the $ per day study it shows "
          "whether a day type matters because it is common or because it is good.", src,
          [(k, D[m & (D.kind == k)].usd.sum(), name) for name, m in eras for k in kinds])


def study_by_year(R, live):
    src = f"{SRC} (chosen_models_trades.csv)"
    for m in ["overnight_break", "opening_range", "expiry_fade"]:
        s = live[live.model == m]
        y = s.groupby(s.date.dt.year).usd.sum()
        R.add(m, "S7", "By year", "year", "net $ (1 micro)",
              f"Net $ of the live trades in each calendar year ({len(s):,} trades, total ${s.usd.sum():,.0f}; "
              f"{int((y > 0).sum())} of {len(y)} years up); first and last years are partial.", src,
              [(str(k), v, NAMES[m]) for k, v in y.items()])
    y = live.groupby(live.date.dt.year).usd.sum()
    R.add("all", "S7", "By year", "year", "net $ (1 micro each)",
          f"Net $ of all three live models together, 1 micro per trade (total ${live.usd.sum():,.0f}; "
          f"{int((y > 0).sum())} of {len(y)} years up); first and last years are partial.", src,
          [(str(k), v, NAMES["all"]) for k, v in y.items()])


def study_skip_rules(R, live, skipped):
    rng = np.random.default_rng(SEED)
    src = f"{SRC} (chosen_models_skipped.csv)"
    groups = [("overnight_break", ["overnight_break"]), ("opening_range", ["opening_range"]),
              ("all", ["overnight_break", "opening_range"])]
    for model, members in groups:
        pool = pd.concat([live[live.model.isin(members)], skipped[skipped.model.isin(members)]]).usd.to_numpy()
        pts = []
        for rule in sorted(skipped[skipped.model.isin(members)].skip_rule.unique()):
            s = skipped[skipped.model.isin(members) & (skipped.skip_rule == rule)]
            n = len(s)
            draws = np.array([rng.choice(pool, n, replace=False).sum() for _ in range(N_RANDOM)])
            lo, hi = np.percentile(draws, [5, 95])
            pts.append((f"{rule} ({n} trades)", -s.usd.sum(), "$ saved by the rule", False,
                        round(-hi, 2), round(-lo, 2)))
        R.add(model, "S8", "Skip rules", "skip rule", "net $ saved by skipping (1 micro)",
              "Net $ each rule saved = minus what the removed trades would have made (above zero = the rule "
              "helped); the band is the 5th-95th percentile of skipping the same number of random trades instead.",
              src, pts)


# ---------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--skip-sweeps", action="store_true", help="keep the existing S1/S2 rows")
    a = ap.parse_args()
    t0 = time.time()
    os.chdir(HERE)
    R = Rows()
    live = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    skipped = pd.read_csv("chosen_models_skipped.csv", parse_dates=["date"])
    ds = cm.sessions()
    cash = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash)
    after_drop, _ = cm.skip_days()
    cal = pd.DatetimeIndex(cash).sort_values()
    live_ob = live[live.model == "overnight_break"]
    live_or = live[live.model == "opening_range"]
    or_days = set(live_or.date)
    checks = []

    # ---- overnight break
    ob = Overnight(cash, expiry, after_drop, ds)
    cur = ob.run(2.0)
    checks.append(f"overnight break at 2 x ATR: {len(cur):,} trades ${cur.usd.sum():,.0f} "
                  f"(live CSV {len(live_ob):,} trades ${live_ob.usd.sum():,.0f})")
    src_ob = f"{SRC} (exits_engine.run 'hold', chosen_models filters)"
    if not a.skip_sweeps:
        pts1, pts2 = [], []
        for k in OB_STOPS:
            for slip in (1, 2):
                t = cur if (k == 2.0 and slip == 1) else ob.run(k, slip_ticks=slip)
                for name, v in era_sums(t.date, t.usd, ERAS if slip == 1 else ERAS[:1]).items():
                    pts1.append((k, v, name + ("" if slip == 1 else TWO_TICK), k == 2.0))
        for cap in [None] + CAPS:
            for slip in (1, 2):
                t = cur if (cap is None and slip == 1) else ob.run(2.0, cap=cap, slip_ticks=slip)
                x = "none" if cap is None else round(cap * 100, 2)
                for name, v in era_sums(t.date, t.usd, ERAS if slip == 1 else ERAS[:1]).items():
                    pts2.append((x, v, name + ("" if slip == 1 else TWO_TICK), cap is None))
        R.add("overnight_break", "S1", "Stop size", "initial stop (x ATR of 5-min bars)", "net $ (1 micro)",
              "Net $ at 1 micro for each initial stop size, held to the 5 PM close; the live rule uses 2 x ATR. "
              "The eras show whether the best size is stable over time.", src_ob, pts1)
        cap_pts = sorted(pts2, key=lambda p: (p[0] == "none", 0 if p[0] == "none" else p[0]))
        R.add("overnight_break", "S2", "Stop cap (share of price)", "stop capped at (% of price)", "net $ (1 micro)",
              "Net $ at 1 micro when the 2 x ATR stop is capped at a share of the entry price (a smaller cap = a "
              "tighter stop on volatile days); 'none' is the live rule.", src_ob, cap_pts)
    study_stop_times(R, "overnight_break", cur, src_ob)
    study_widths(R, "overnight_break", cur.assign(model="overnight_break"), cal, src_ob)
    study_entry_hour(R, cur, src_ob)
    del ob
    gc.collect()

    # ---- opening range
    dates, g, inst = p5.load_market(SYM)
    sess, Cff, _ = p5.build_sessions(SYM, dates, g, inst)
    sess = sess[sess.date.isin(cash)]
    ppt = p5.MARKETS[SYM]["ppt"]
    src_grid = f"{SRC} (orb_grid simulator on the live opening_range dates without data gaps)"
    if not a.skip_sweeps:
        pts1, pts2 = [], []
        for slip in (1, 2):
            E0 = orb_entries(sess, g, Cff, slip * TK, or_days)
            if slip == 1:
                checks.append(f"opening range grid set: {len(E0):,} trades of {len(live_or):,} live")
            for k in ORB_STOPS:
                usd = orb_simulate(E0, g, Cff, k, slip * TK, ppt)
                x = "no stop" if k is None else k
                for name, v in era_sums(E0.date, usd, ERAS if slip == 1 else ERAS[:1]).items():
                    pts1.append((x, v, name + ("" if slip == 1 else TWO_TICK), k == 1.0))
                if k == 1.0 and slip == 1:
                    checks.append(f"opening range grid at 1 x candle: ${usd.sum():,.0f} "
                                  f"(live CSV ${live_or.usd.sum():,.0f})")
            for cap in [None] + CAPS:
                E = E0 if cap is None else E0.assign(R0=np.minimum(E0.R0, cap * E0.fill))
                usd = orb_simulate(E, g, Cff, 1.0, slip * TK, ppt)
                x = "none" if cap is None else round(cap * 100, 2)
                for name, v in era_sums(E0.date, usd, ERAS if slip == 1 else ERAS[:1]).items():
                    pts2.append((x, v, name + ("" if slip == 1 else TWO_TICK), cap is None))
        R.add("opening_range", "S1", "Stop size", "stop (x the first 5-min candle's range, from the entry)",
              "net $ (1 micro)",
              "Net $ at 1 micro for each stop size, out at the 15:59 close; the live rule puts the stop at the "
              "candle's other end (1 x). The eras show whether the best size is stable over time.", src_grid, pts1)
        cap_pts = sorted(pts2, key=lambda p: (p[0] == "none", 0 if p[0] == "none" else p[0]))
        R.add("opening_range", "S2", "Stop cap (share of price)", "stop capped at (% of price)", "net $ (1 micro)",
              "Net $ at 1 micro when the candle stop is capped at a share of the entry price (a smaller cap = a "
              "tighter stop on wide-candle days); 'none' is the live rule.", src_grid, cap_pts)
    orl = orb_live(expiry, sess, g, Cff, or_days)
    checks.append(f"opening range live rule re-run: {len(orl):,} trades ${orl.usd.sum():,.0f} "
                  f"(live CSV {len(live_or):,} trades ${live_or.usd.sum():,.0f})")
    del g, Cff, inst
    gc.collect()
    src_or = f"{SRC} (chosen_models.opening_range rule)"
    study_stop_times(R, "opening_range", orl, src_or)
    study_widths(R, "opening_range", orl.assign(model="opening_range"), cal, src_or)

    # ---- live-CSV studies
    study_day_type(R, live)
    study_by_year(R, live)
    study_skip_rules(R, live, skipped)

    F = R.frame()
    allrows = save_studies(F, a.out)
    print(f"Saved {a.out}: {len(F):,} rows from this run, {len(allrows):,} rows in the file, "
          f"{allrows.groupby(['model', 'study']).ngroups} studies")
    print("Checks:\n  " + "\n  ".join(checks))
    print("Summary (first series; best vs the live setting where the study has one):")
    for (m, s), d in F.groupby(["model", "study"], sort=False):
        first = d[d.series == d.series.iloc[0]]
        best = first.loc[first.y.idxmax()]
        cur_ = first[first.is_current]
        money = (lambda v: f"${v:,.0f}") if "$" in d.y_label.iloc[0] else (lambda v: f"{v:,.0f}")
        word = "best" if len(cur_) else "highest"
        txt = f"  {m:16s} {s:4s} {d.title.iloc[0]:28s} {word} {best.x}: {money(best.y)}"
        if len(cur_):
            txt += f"; current {cur_.x.iloc[0]}: {money(cur_.y.iloc[0])}"
        print(txt)
    print(f"Run time {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
