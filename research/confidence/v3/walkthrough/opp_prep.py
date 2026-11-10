"""Opposite-evidence exit examples ex12 / ex13: recompute the 60-min evidence grid with the REAL v2 code
(v2/dataset.py:155-169 load_frames, :221-237 evidence_types, :240-247 evidence_counts) on a 1-minute window
[entry - 45 days, hold exit + 3 h] (EMA50 seed weight after ~700 60-min bars is < 1e-12, so values equal the full-
history ones), and redo the 1-minute exit walk (labels.py:295-334 rules: stop first, min(open, stop) -/+ 1 tick).
Run ONCE under the heavy lock (loads 1-minute data, one market at a time). Writes opp_cache/<example_id>.pkl and
re-cuts slices/<example_id>_1m.parquet wide enough for the 1-min panel around the EXIT decision."""
import gc
import os
import pickle
import sys

import numpy as np
import pandas as pd

import research_lib as rl
import signals as sg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "v2"))
import dataset as ds  # noqa: E402

HOLDOUT = pd.Timestamp("2025-06-30 18:00")
V3MODE = os.environ.get("OPP_V3") == "1"
OUT = os.path.join(HERE, "opp_cache")
os.makedirs(OUT, exist_ok=True)
EX = pd.read_csv(os.path.join(HERE, "examples.csv"), parse_dates=["decision_time", "entry_time", "exit_time",
                                                                   "signal_bar", "hold_exit_time"])
EX = EX[EX.example_id.str.contains("oppexit")]
if os.environ.get("OPP_ONLY"):
    EX = EX[EX.example_id.str.startswith(os.environ["OPP_ONLY"])]
_BARS_1M = rl.bars_1m                       # keep the real loader (signals.rl IS research_lib)
NAMES = ["reversal candle against", "Momentum moved against (vs prev bar)", "close on wrong side of EMA20",
         "EMA8 on wrong side of EMA20", "close beyond last confirmed swing", "latest closed 60-min trend not with trade",
         "5-min trigger the other way inside this bar"]

for r in EX.itertuples():
    sym = r.sym
    d = 1 if r.side == "LONG" else -1
    t0 = r.entry_time - pd.Timedelta(days=45)
    t1 = min(r.hold_exit_time + pd.Timedelta(hours=3), HOLDOUT)
    if V3MODE:   # fallback without the lock: v3 bars (build_data.py) instead of signals.bars on 1-minute data
        def _v3(_sym, tf, _t0=t0, _t1=t1):
            b = pd.read_parquet(os.path.join(HERE, "..", "data", f"bars_{_sym}_{tf}.parquet"))
            b = b[(b.index >= _t0) & (b.index < _t1)][["O", "H", "L", "C", "V", "vwap", "sess", "inst"]].copy()
            b["seg"] = (b.sess.ne(b.sess.shift()) | b.inst.ne(b.inst.shift())).cumsum()
            b["run"] = b.inst.ne(b.inst.shift()).cumsum()
            return b
        sg.bars = _v3
        one = _v3(sym, 5)
        one = one[one.index >= r.entry_time - pd.Timedelta(hours=1)]
        BARLEN = 5
    else:
        BARLEN = 1
    full = None if V3MODE else _BARS_1M(sym)
    if V3MODE:
        F = ds.load_frames(sym, tfs=(5, 15, 60))
    if not V3MODE:
      idx = full.index.tz_localize(None)
      m = full[(idx >= t0) & (idx < t1)].copy()
      del full
      gc.collect()
      assert m.index.tz_localize(None).max() < HOLDOUT
    if not V3MODE:
      # wider 1-minute slice for the 1-min panel (decision = the exit decision)
      mi = m.index.tz_localize(None)
      s = pd.DataFrame({"O": m.Open.to_numpy(float), "H": m.High.to_numpy(float), "L": m.Low.to_numpy(float),
                        "C": m.Close.to_numpy(float), "V": m.Volume.to_numpy(float), "inst": m.instrument_id.to_numpy(),
                        "sess": m.sess.to_numpy()}, index=mi)
      s = s[(s.index >= r.entry_time - pd.Timedelta(hours=30)) & (s.index < r.hold_exit_time + pd.Timedelta(hours=1, minutes=30))]
      s.index.name = "ts"
      s.to_parquet(os.path.join(HERE, "slices", f"{r.example_id}_1m.parquet"))
      sg.rl.bars_1m = lambda _sym, _m=m: _m          # signals.bars reads this window only
      F = ds.load_frames(sym, tfs=(5, 15, 60))
    b60 = F[60]["b"]
    types = ds.evidence_types(F, 60)[d]
    cnt = ds.evidence_counts({d: types})
    t60 = ds.at_base(F, 60, 60, F[60]["raw"]["trend"])[:, 0]
    i_sig = b60.index.get_loc(r.signal_bar)
    sess = b60.sess.iloc[i_sig]
    rows = np.flatnonzero((b60.sess.to_numpy() == sess) & (np.arange(len(b60)) >= i_sig))
    # 5-min opposite triggers (names) inside each 60-min bar
    T5 = F[5]["T"]
    T5 = T5[(T5.rule != "trend_all") & (T5.d == -d)]
    b5 = F[5]["b"]
    t5 = pd.Series(T5.rule.to_numpy(), index=b5.index[T5.i.to_numpy()])
    grid = []
    for k in rows:
        st = b60.index[k]
        inside = t5[(t5.index >= st) & (t5.index < st + pd.Timedelta(minutes=60))]
        rv = [c for c in F[60]["P"].columns if c in sg.PATTERN_RULES and F[60]["P"][c].iloc[k] == -d]
        grid.append(dict(bar=st, close=st + pd.Timedelta(minutes=60), O=b60.O.iloc[k], H=b60.H.iloc[k],
                         L=b60.L.iloc[k], C=b60.C.iloc[k], ema8=F[60]["ctx"].ema8.iloc[k], ema20=F[60]["ctx"].ema20.iloc[k],
                         mom=F[60]["ctx"].mom14.iloc[k], swing_lo=F[60]["ctx"].swing_lo.iloc[k],
                         swing_hi=F[60]["ctx"].swing_hi.iloc[k], t60=t60[k],
                         ev=[bool(x) for x in types[k]], c1=int(cnt[(d, 1)][k]), c2=int(cnt[(d, 2)][k]),
                         pats_against=rv, trig5_against=sorted(set(inside.tolist())),
                         trig5_times=[str(x) for x in inside.index]))
    # 1-minute walk from entry: stop first, then rule exit at the next bar's first-minute open, time exit at 16:00 bar close
    tick = sg.SPEC[sym]["tick"]
    usd = {"NQ": 2.0, "ES": 5.0, "YM": 0.5}[sym]
    cost = 1.0 + 2 * tick * usd
    row = pd.read_parquet(os.path.join(HERE, "..", "..", "v2", "out", f"v2_events_{sym}_60.parquet"),
                          filters=[("t", "==", r.signal_bar)])
    row = row[row.d == d].iloc[0]
    if not V3MODE:
        one = s
    entry = float(one.O[one.index >= r.entry_time].iloc[0])
    stop = float(row.stop)

    def walk(rule_exit_bar_close):
        for ts_, o_, h_, l_, c_ in zip(one.index, one.O, one.H, one.L, one.C):
            if ts_ < r.entry_time:
                continue
            if rule_exit_bar_close is not None and ts_ >= rule_exit_bar_close:
                return ts_, o_, "rule exit at the next bar's first-minute open"
            if (d > 0 and l_ <= stop) or (d < 0 and h_ >= stop):
                return ts_, (min(o_, stop) - tick) if d > 0 else (max(o_, stop) + tick), "stop (1-minute walk, +1 tick slip)"
            if ts_ >= r.hold_exit_time - pd.Timedelta(minutes=1) and ts_.hour * 60 + ts_.minute + BARLEN >= 16 * 60:
                return ts_, c_, "time exit: close of the 15:00-16:00 bar (60-min Lucid flat)"
        return None, np.nan, "?"
    first3 = next((g for g in grid[1:] if g["c1"] >= 3 and g["close"] < pd.Timestamp(sess) + pd.Timedelta(hours=16)), None)
    rx = walk(first3["close"] if first3 else None)
    hx = walk(None)
    pnl = lambda px: d * (px - entry) * usd - cost  # noqa: E731
    res = dict(mode="v3 bars, 5-min walk" if V3MODE else "1-minute (signals.bars), 1-minute walk", example_id=r.example_id, sym=sym, d=d, entry=entry, stop=stop, cost=cost, usd=usd, tick=tick,
               R20=float(row.R20), row=row.to_dict(), grid=grid, names=NAMES,
               first3=first3, rule_exit=dict(t=rx[0], px=rx[1], how=rx[2], pnl=pnl(rx[1])),
               hold_exit=dict(t=hx[0], px=hx[1], how=hx[2], pnl=pnl(hx[1])))
    with open(os.path.join(OUT, f"{r.example_id}{'_v3' if V3MODE else ''}.pkl"), "wb") as f:  # noqa
        pickle.dump(res, f)
    print(r.example_id, "entry", entry, "rule", res["rule_exit"], "hold", res["hold_exit"],
          "stored opp3", row.pnl_opp3_1b, row.t_exit_opp3_1b, "hold", row.pnl_hold, row.t_exit_hold, flush=True)
    for g in grid:
        print("  ", g["bar"], g["c1"], g["c2"], "".join("X" if e else "." for e in g["ev"]), g["pats_against"], g["trig5_against"])
    F = None
    gc.collect()
