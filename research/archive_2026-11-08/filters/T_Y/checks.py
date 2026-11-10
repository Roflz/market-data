"""Sanity checks for builder Y's T1-T4 inputs (read-only use of the project)."""
import os
import subprocess
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
OUT = os.path.dirname(os.path.abspath(__file__))
P = pd.read_csv(os.path.join(OUT, "all_inputs_per_trade.csv"), parse_dates=["date"])
S = pd.read_pickle(os.path.join(OUT, "session_inputs.pkl"))
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")

# ---- 1. base trade set: regenerate with chosen_models' own functions (no file written) and compare to the CSV
import sys
sys.path.insert(0, os.getcwd())                                  # project modules (read-only import)
import calendar_days as cd
import chosen_models as cm
import lit_p5_orb as p5
csv = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
cash_days = ds.index[ds.cash_day]
expiry = cd.expiry_fridays(cash_days)
dates, g, inst = p5.load_market("NQ")
sess, Cff, _ = p5.build_sessions("NQ", dates, g, inst)
sess = sess[sess.date.isin(cash_days)]
orb = cm.opening_range(expiry, sess, g, Cff)
after_drop, fed = cm.skip_days()
orb = orb[~orb.date.isin(after_drop) & ~orb.date.isin(fed)].reset_index(drop=True)
c_orb = csv[csv.model == "opening_range"].reset_index(drop=True)
same = (len(orb) == len(c_orb)) and (orb.date.values == c_orb.date.values).all() and (orb.side.values == c_orb.side.values).all() \
    and np.allclose(orb.usd.values, c_orb.usd.values)
print(f"[1] regenerated opening_range: {len(orb)} trades ${orb.usd.sum():,.2f} | CSV {len(c_orb)} ${c_orb.usd.sum():,.2f} | "
      f"row-by-row identical: {same}; my per-trade file {len(P)} ${P.usd.sum():,.2f}")

# ---- 2. coverage / missing inputs on trade days
print(f"[2] trade days with missing inputs: trend {P.trend.isna().sum()}, gap {P.gap.isna().sum()}, "
      f"zero gap {(P.gap == 0).sum()}, fc {P.fc_range.isna().sum()}, on {P.on_range.isna().sum()}, "
      f"fc_med NaN (keep) {P.fc_med20.isna().sum()}, on_med NaN (keep) {P.on_med20.isna().sum()}, trend==0 {(P.trend == 0).sum()}")
print(f"    9:34 close taken from an earlier bar: {(P.c934_tmin != 574).sum()}; overnight bars min {P.on_nbars.min()}")
Sd = S.loc[P.date]
print(f"    session bars before 18:00 prior evening (excluded from T4): max {S.n_pre_eve.max()} "
      f"(sessions with any: {(S.n_pre_eve > 0).sum()})")
print(f"    roll inside first candle: {(Sd.fc_inst_n > 1).sum()}; inside overnight window: {(Sd.on_inst_n > 1).sum()}")
dfc = (Sd.fc_range - Sd.fc_range_raw).abs() > 1e-9
don = (Sd.on_range - Sd.on_range_raw).abs() > 1e-9
print(f"    adjusted vs raw range differs: fc {dfc.sum()} (all on roll windows: {(Sd.fc_inst_n[dfc] > 1).all()}), "
      f"overnight {don.sum()} (all on roll windows: {(Sd.on_inst_n[don] > 1).all()})")
print(f"    early-close cash sessions: {S.early_close.sum()}, their close bar tmin: {sorted(S.close_tmin[S.early_close].unique())}; "
      f"normal days close bar != 959: {((S.close_tmin != 959) & ~S.early_close).sum()}")
print(f"    all inputs from bars closed by 9:35: {bool(P.inputs_before_935.all())}")

# ---- 3. T1 against the overnight-break model's own feature (fut_features day_vs_ema20 at the 9:34 decision bar)
F = pd.read_pickle("data/fut_features_NQ.pkl")
X = F["X"]
m = (F["tmin"] == 574)
ff = pd.Series(np.sign(X.day_vs_ema20.to_numpy()[m]), index=pd.to_datetime(F["date"][m]))
ff = ff[~ff.index.duplicated()]
cmp_ = P.set_index("date").trend.to_frame().join(ff.rename("ff"), how="left")
both = cmp_.dropna()
print(f"[3] T1 trend vs fut_features sign(day_vs_ema20 @9:34): compared {len(both)}, agree {(both.trend == both.ff).sum()}, "
      f"missing in fut_features {cmp_.ff.isna().sum()}")
dis = both[both.trend != both.ff]
if len(dis):
    print("    disagreements:", dis.head(10).to_dict("index"))
# magnitude check: (C - ema)/datr from features vs mine
dv = pd.Series(X.day_vs_ema20.to_numpy()[m], index=pd.to_datetime(F["date"][m]))
dv = dv[~dv.index.duplicated()]
mine = (P.set_index("date").c934 - P.set_index("date").ema20_prev)
print(f"    near-zero cases |C-ema|<2pt among trades: {(mine.abs() < 2).sum()}")

# ---- 4. T2 against daily_sessions_NQ.pkl (open_adj, close_adj = last RTH bar; differs only on early-close days)
j = P.set_index("date")
o_ok = np.isclose(j.open930, ds.open_adj.reindex(j.index)).mean()
pc = ds.close_adj.reindex(pd.to_datetime(j.prev_cash))
c_ok = np.isclose(j.prev_close1600.to_numpy(), pc.to_numpy())
early_prev = ds.early_close.reindex(pd.to_datetime(j.prev_cash)).to_numpy()
print(f"[4] 9:30 open == ds.open_adj: {o_ok:.4f}; prev close == ds.close_adj on non-early prev days: "
      f"{c_ok[~early_prev].mean():.4f}; early prev days {early_prev.sum()} (differ: {(~c_ok[early_prev]).sum()})")
gap_ds = ds.open_adj.reindex(j.index).to_numpy() - pc.to_numpy()
print(f"    gap sign agreement with ds-based gap: {(np.sign(gap_ds) == np.sign(j.gap.to_numpy())).mean():.4f}")
prev_is_prev_cash = all(pd.Timestamp(a) == cash_days[cash_days.get_loc(b) - 1] for a, b in zip(j.prev_cash, j.index))
print(f"    prev_cash is the previous cash_day session for every trade: {prev_is_prev_cash}")

# ---- 5. hand spot-check of 5 trades from the raw CSV text (no pandas back-adjust; raw lines grep'd)
rng = np.random.default_rng(12345)
pick = sorted(rng.choice(len(P), 5, replace=False))
def raw_lines(prefixes):
    out = []
    for pf in prefixes:
        r = subprocess.run(["grep", "^" + pf, "data/NQ_fut_1m.csv"], capture_output=True, text=True).stdout.split("\n")
        for ln in r:
            if ln:
                ts, o, h, l, c, v, iid = ln.split(",")
                out.append((pd.Timestamp(ts).tz_convert("America/New_York"), float(o), float(h), float(l), float(c), int(iid)))
    return out
for i in pick:
    t = P.iloc[i]
    D = t.date
    pd_ = pd.Timestamp(t.prev_cash)
    prevday = D - pd.Timedelta(days=1)
    # timestamps in the file are written with an ET offset; grep both calendar days by text prefix
    bars = raw_lines(sorted({prevday.strftime("%Y-%m-%d"), D.strftime("%Y-%m-%d"), pd_.strftime("%Y-%m-%d")}))
    eve = pd.Timestamp(prevday.strftime("%Y-%m-%d") + " 18:00", tz="America/New_York")
    t930 = pd.Timestamp(D.strftime("%Y-%m-%d") + " 09:30", tz="America/New_York")
    fc = [b for b in bars if t930 <= b[0] < t930 + pd.Timedelta(minutes=5)]
    on = [b for b in bars if eve <= b[0] < t930]
    o930 = [b for b in bars if b[0] == t930]
    close_t = pd.Timestamp(pd_.strftime("%Y-%m-%d") + (" 12:59" if ds.early_close.get(pd_, False) else " 15:59"),
                           tz="America/New_York")
    cl = [b for b in bars if b[0] == close_t]
    fc_r = max(b[2] for b in fc) - min(b[3] for b in fc)
    on_r = max(b[2] for b in on) - min(b[3] for b in on)
    ids = {b[5] for b in on + fc + o930 + cl}
    gap_raw = o930[0][1] - cl[0][4]
    c934 = [b for b in fc if b[0].minute == 34][0][4]
    print(f"[5] {D.date()} {t.side:5s}: first-candle {fc_r:.2f} (mine {t.fc_range:.2f}); overnight {on_r:.2f} "
          f"(mine {t.on_range:.2f}, {len(on)} bars vs {t.on_nbars}); raw gap {gap_raw:+.2f} (mine {t.gap:+.2f}, "
          f"contracts in windows {len(ids)}); 9:34 close raw {c934} (mine adj {t.c934}) "
          f"-> T1 {t.T1} T2 {t.T2} T3 {t.T3} (med {t.fc_med20:.2f}) T4 {t.T4} (med {t.on_med20:.2f})")
    # verify the T3/T4 medians directly from the session table (previous 20 cash sessions, strictly before D)
    prior = S[S.index < D].tail(20)
    assert np.isclose(np.median(prior.fc_range), t.fc_med20) and np.isclose(np.median(prior.on_range), t.on_med20)
print("    medians re-derived from the 20 prior cash sessions: OK")
