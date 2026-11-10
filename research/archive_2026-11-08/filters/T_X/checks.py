"""Sanity checks for builder X: base-set rebuild, look-ahead truncation test, hand spot-checks from raw 1-min bars."""
import sys
import numpy as np
import pandas as pd

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/T_X"
sys.path.insert(0, OUT)
sys.path.insert(0, "/run/media/roflz/Disk 2/_/market_data")
import build_inputs as bi  # noqa: E402

allt = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
orb = allt[allt.model == "opening_range"].reset_index(drop=True)
inp = pd.read_pickle(f"{OUT}/inputs.pkl")
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")

# ---- 1. rebuild the opening_range trades with chosen_models (nothing written) and compare ----
import chosen_models as cm  # noqa: E402
import calendar_days as cd  # noqa: E402
import lit_p5_orb as p5  # noqa: E402
cash_days = ds.index[ds.cash_day]
expiry = cd.expiry_fridays(cash_days)
dates, g, inst = p5.load_market("NQ")
sess, Cff, _ = p5.build_sessions("NQ", dates, g, inst)
sess = sess[sess.date.isin(cash_days)]
R = cm.opening_range(expiry, sess, g, Cff)
after_drop, fed = cm.skip_days()
R = R[~R.date.isin(after_drop) & ~R.date.isin(fed)].sort_values("date").reset_index(drop=True)
m = R.merge(orb, on="date", how="outer", suffixes=("_re", "_csv"), indicator=True)
print(f"[1] rebuilt {len(R)} trades ${R.usd.sum():,.2f} vs csv {len(orb)} ${orb.usd.sum():,.2f}; "
      f"only-one-side rows {int((m._merge != 'both').sum())}; side mismatches {(m.side_re != m.side_csv).sum()}; "
      f"max |usd diff| {np.nanmax(np.abs(m.usd_re - m.usd_csv)):.6f}")
# p5 first-candle range (raw, 9:30 contract only) vs ours on trade days
di = sess.set_index("date").di.reindex(orb.date).to_numpy()
p5r = np.nanmax(g["High"][di, :5], 1) - np.nanmin(g["Low"][di, :5], 1)
ours = inp.fc_range.reindex(orb.date).to_numpy()
print(f"    first-candle range vs lit_p5_orb grid on trade days: max |diff| {np.nanmax(np.abs(p5r - ours)):.6f}")
del g, Cff

# ---- 2. look-ahead: rebuild inputs from bars truncated at D 9:35 ET, compare D's inputs ----
d = bi.load_bars()
cols = ["trend_diff", "trend", "fc_range", "fc_med20", "on_range", "on_med20", "gap", "fc_nprior", "on_nprior"]
rng = np.random.default_rng(12345)
test_dates = list(pd.DatetimeIndex(rng.choice(orb.date.to_numpy(), 12, replace=False))) + \
    [orb.date.iloc[25], orb.date.iloc[-1]]
worst = 0.0
for D in test_dates:
    cut = pd.Timestamp(D.date()).tz_localize("America/New_York") + pd.Timedelta(hours=9, minutes=35)
    dt = d[d.index < cut]
    # recompute back-adjustment from the truncated bars only (later rolls unknown at the decision)
    dt = dt[["Open", "High", "Low", "Close", "Volume", "instrument_id"]].copy()
    roll = dt.instrument_id.ne(dt.instrument_id.shift()) & dt.instrument_id.shift().notna()
    jump = (dt.Open - dt.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    for c in ("Open", "High", "Low", "Close"):
        dt["a" + c[0]] = dt[c] + adj
    dt["sess"] = pd.to_datetime((dt.index + pd.Timedelta(hours=6)).date)
    dt["tmin"] = dt.index.hour * 60 + dt.index.minute
    dt["cal"] = pd.to_datetime(dt.index.date)
    it = bi.build(dt, ds[ds.index <= D]).loc[D, cols]
    full = inp.loc[D, cols]
    diff = np.nanmax(np.abs(it.astype(float).to_numpy() - full.astype(float).to_numpy()))
    worst = max(worst, diff)
    print(f"[2] {D:%Y-%m-%d} truncated-at-9:35 vs full: max |diff| {diff:.2e}")
print(f"    worst over {len(test_dates)} dates: {worst:.2e}")

# ---- 3. hand spot-checks from the RAW 1-min CSV rows (no back-adjustment unless a roll falls inside a window) ----
raw = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"])
raw["ts"] = pd.to_datetime(raw.ts_event, utc=True).dt.tz_convert("America/New_York")
raw = raw.drop_duplicates("ts").set_index("ts").sort_index()
tz = "America/New_York"
picks = [orb.date.iloc[i] for i in (30, 900, 1800, 2700, 3400)]
cash = list(cash_days)
for D in picks:
    t0 = pd.Timestamp(D.date()).tz_localize(tz)
    side = orb.set_index("date").side[D]
    fc = raw[(raw.index >= t0 + pd.Timedelta("9h30min")) & (raw.index < t0 + pd.Timedelta("9h35min"))]
    fc_range = fc.High.max() - fc.Low.min()
    prevD = cash[cash.index(D) - 1]
    on = raw[(raw.index >= t0 - pd.Timedelta("6h")) & (raw.index < t0 + pd.Timedelta("9h30min"))]
    on_range = on.High.max() - on.Low.min()
    # prior 20 cash sessions' first-candle and overnight ranges, by hand
    i = cash.index(D)
    fcs, ons = [], []
    for P in cash[i - 20:i]:
        p0 = pd.Timestamp(P.date()).tz_localize(tz)
        b = raw[(raw.index >= p0 + pd.Timedelta("9h30min")) & (raw.index < p0 + pd.Timedelta("9h35min"))]
        fcs.append(b.High.max() - b.Low.min())
        b = raw[(raw.index >= p0 - pd.Timedelta("6h")) & (raw.index < p0 + pd.Timedelta("9h30min"))]
        ons.append(b.High.max() - b.Low.min())
    # gap: raw 9:30 open minus raw previous cash close (15:59 or 12:59); roll gap removed if contracts differ
    p0 = pd.Timestamp(prevD.date()).tz_localize(tz)
    last_t = "12h59min" if ds.early_close[prevD] else "15h59min"
    pc_bar = raw[(raw.index >= p0 + pd.Timedelta("9h30min")) & (raw.index <= p0 + pd.Timedelta(last_t))].iloc[-1]
    o_bar = raw.loc[t0 + pd.Timedelta("9h30min")]
    gap_raw = o_bar.Open - pc_bar.Close
    between = raw[(raw.index > pc_bar.name) & (raw.index <= o_bar.name)]
    ids = between.instrument_id
    rolls = ids.ne(ids.shift()) & ids.shift().notna()
    roll_note = ""
    if pc_bar.instrument_id != o_bar.instrument_id or rolls.any():
        seq = pd.concat([raw.loc[[pc_bar.name]], between])
        r_ = seq.instrument_id.ne(seq.instrument_id.shift()) & seq.instrument_id.shift().notna()
        jumps = (seq.Open - seq.Close.shift())[r_].sum()
        gap_raw -= jumps
        roll_note = f" (roll jump {jumps:+.2f} removed)"
    # T1 by hand: session closes -> EMA20 loop -> previous session's EMA vs today's 9:34 close (back-adjusted)
    c934_raw = raw.loc[t0 + pd.Timedelta("9h34min")].Close
    x = inp.loc[D]
    print(f"[3] {D:%Y-%m-%d} {side}: fc {fc_range:.2f} (ours {x.fc_range:.2f}) med20 {np.median(fcs):.3f} "
          f"(ours {x.fc_med20:.3f}); on {on_range:.2f} (ours {x.on_range:.2f}) med20 {np.median(ons):.3f} "
          f"(ours {x.on_med20:.3f}); gap {gap_raw:+.2f}{roll_note} (ours {x.gap:+.2f}); "
          f"9:34 close raw {c934_raw} (ours adj {x.c934:.2f}, adj offset {x.c934 - c934_raw:+.2f})")

# T1 by hand for the same dates: plain loop EMA over every Globex session's last back-adjusted close
dc = d.groupby("sess").aC.last()
ema, e = {}, None
for s_, c in dc.items():
    e = c if e is None else e + 2 / 21 * (c - e)
    ema[s_] = e
keys = list(ema)
for D in picks:
    k = keys.index(D)
    c934 = d.aC[(d.sess == D) & (d.tmin == 574) & (d.cal == D)].iloc[0]
    tr = np.sign(c934 - ema[keys[k - 1]])
    print(f"[3] T1 {D:%Y-%m-%d}: prev session {keys[k - 1]:%Y-%m-%d} EMA20 {ema[keys[k - 1]]:.3f} (ours "
          f"{inp.prev_ema20[D]:.3f}), 9:34 close {c934:.2f}, trend {tr:+.0f} (ours {inp.trend[D]:+.0f})")
