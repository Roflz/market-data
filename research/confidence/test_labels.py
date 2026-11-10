"""Hand-made 1-minute paths for labels.py: stop, target, same-minute tie, gap through stop / target, time exit, 16:45
cutoff, entry past stop, short mirror, segment rules, event generators and exit-row labels.
Regression tests for the review findings: entry exactly at the stop (risk 0) is a stop fill with the extra tick;
exit-row trade ids are unique across markets (+ market column); R-unit trade state is clipped; breakout stops reach
the mother / NR7 bar; the tick comes from sym= / tick= (inference warns on short frames).

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_labels.py

research_lib.bars_1m is replaced by a synthetic 1-minute frame, so signals.bars and labels.load_1m run their real code
on hand-made prices. ES spec: tick 0.25, $5/pt, cost $3.50 per round trip (1 tick each way + $1).
"""
import warnings

import numpy as np
import pandas as pd

import research_lib as rl
import signals as sg
import labels as lb

TICK, USD, COST = 0.25, 5.0, 3.5
assert sg.SPEC["ES"]["cost"] == COST


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    assert cond, name


def approx(a, b):
    return bool(np.isclose(a, b, atol=1e-9))


class Path:
    """A synthetic 1-minute tape (New York wall time) with a flat default price; override single minutes."""

    def __init__(self, spans, px=100.0, inst=1):
        idx = pd.DatetimeIndex(np.concatenate([pd.date_range(a, z, freq="1min").to_numpy() for a, z in spans]))
        self.df = pd.DataFrame({"Open": px, "High": px, "Low": px, "Close": px}, index=idx)
        self.inst = pd.Series(inst, index=idx)

    def set(self, ts, O, H, L, C):
        self.df.loc[pd.Timestamp(ts), ["Open", "High", "Low", "Close"]] = [O, H, L, C]
        return self

    def level(self, a, z, px):
        """flat price px on minutes a..z (inclusive)."""
        self.df.loc[pd.Timestamp(a):pd.Timestamp(z), ["Open", "High", "Low", "Close"]] = px
        return self

    def frame(self):
        d = self.df.copy()
        d["Volume"] = 1
        d["instrument_id"] = self.inst.to_numpy()
        ts = d.index.tz_localize("America/New_York")
        d.index = ts
        d.index.name = "ts"
        d["sess"] = (d.index + pd.Timedelta(hours=6)).tz_localize(None).normalize()
        d["tmin"] = (d.index.hour * 60 + d.index.minute).astype(np.int16)
        return d


def install(path):
    """route research_lib.bars_1m (used by signals.bars and labels.load_1m) to the synthetic tape."""
    fr = path.frame()
    rl.bars_1m = lambda sym=None: fr.copy()


def ev(b, rows):
    """events frame from [(signal bar start, d, stop), ...]."""
    i = b.index.get_indexer(pd.DatetimeIndex([r[0] for r in rows]))
    assert (i >= 0).all()
    return pd.DataFrame({"t": b.index[i], "i": i, "d": np.array([r[1] for r in rows], np.int8),
                         "patterns": [[] for _ in rows], "n_patterns": 0, "stop": [float(r[2]) for r in rows]})


DAY = "2024-03-05"
T = lambda hm: pd.Timestamp(f"{DAY} {hm}")

# ============================================================================ 1. long: stop, target, tie, gaps
# one RTH-ish session 09:00-16:59; flat 100. Signal bar 09:45 (closes 10:00) -> entry = open of 10:00 bar = 100.
p = Path([(T("09:00"), T("16:59"))])
install(p)
b = sg.bars("ES", 15)
check("synthetic bars: 15-min bars 09:00..16:45", len(b) == 32 and b.index[0] == T("09:00"))

# (a) plain stop: long stop 99; minute 10:07 opens 99.5, trades down to 98.75 -> fill min(99.5, 99) - 1 tick = 98.75
p = Path([(T("09:00"), T("16:59"))])
p.set(f"{DAY} 10:07", 99.5, 99.5, 98.75, 99.0)
install(p); b = sg.bars("ES", 15)
# a touch of the stop INSIDE the signal bar (before the entry) must be ignored
p.set(f"{DAY} 09:50", 100, 100, 98.0, 100)
install(p); b = sg.bars("ES", 15)
lab = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)]))
r = lab.iloc[0]
check("stop: entry = open of next bar", r.entry == 100.0 and r.t_entry == T("10:00"))
check("stop: risk 1 pt = $5", r.risk_pts == 1.0 and r.risk_usd == 5.0)
check("stop: fill = stop - 1 extra tick", all(r[f"exit_px_{k}"] == 98.75 for k in ("1", "1.5", "2")))
check("stop: pnl = (98.75-100)*5 - 3.50 = -9.75", all(approx(r[f"pnl_usd_{k}"], -9.75) for k in ("1", "1.5", "2")))
check("stop: kind/y/t_end (end of the 10:07 minute)", r.exit_kind_1 == "stop" and not r.y_1 and r["t_end_1.5"] == T("10:08"))
check("stop: pre-entry touch in the signal bar ignored (not stopped at 10:00)", r.t_end_2 == T("10:08"))

# (b) stop touched exactly (low == stop) counts; open above stop -> fill at stop - tick
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:03", 100, 100, 99.0, 99.5)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)])).iloc[0]
check("stop: low == stop triggers", r.exit_kind_1 == "stop" and r.exit_px_1 == 98.75 and r.t_end_1 == T("10:04"))

# (c) targets: R=1 -> 101 (needs high >= 101.25), R=1.5 -> 101.5 (needs >= 101.75), R=2 -> 102 never -> time
p = Path([(T("09:00"), T("16:59"))])
p.set(f"{DAY} 10:05", 100, 101.0, 100, 100.5)          # touches 101 exactly: NOT a fill for R=1
p.set(f"{DAY} 10:12", 100.5, 101.5, 100.5, 101.0)      # 1 tick through 101 -> R=1 filled at 101; 101.5 only touched
p.set(f"{DAY} 10:31", 101.0, 101.75, 101.0, 101.25)    # 101.75 -> R=1.5 filled at 101.5
p.level(f"{DAY} 10:32", f"{DAY} 16:59", 100.5)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)]), max_bars=4).iloc[0]
check("target R1: exact touch is not a fill; filled at 10:12 at 101",
      r.exit_kind_1 == "target" and r.exit_px_1 == 101.0 and r.t_end_1 == T("10:13"))
check("target R1 pnl = 1*5 - 3.5 = 1.5, y True", approx(r.pnl_usd_1, 1.5) and r.y_1)
check("target R1.5 filled at 10:31 at 101.5, pnl 4.0",
      r["exit_kind_1.5"] == "target" and r["exit_px_1.5"] == 101.5 and approx(r["pnl_usd_1.5"], 4.0) and r["t_end_1.5"] == T("10:32"))
# R=2: time limit = close of bar t+4 = 10:45 bar (close 11:00), exit at its last minute's close 100.5
check("time exit R2: at close of bar t+max_bars", r.exit_kind_2 == "time" and r.exit_px_2 == 100.5 and r.t_end_2 == T("11:00"))
check("time exit R2 pnl = 0.5*5 - 3.5 = -1.0, y False", approx(r.pnl_usd_2, -1.0) and not r.y_2)
check("targets stored", r.target_1 == 101.0 and r["target_1.5"] == 101.5 and r.target_2 == 102.0)

# (d) same-minute tie: one minute spans the stop AND every target -> stop first for all
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:20", 100.0, 103.0, 98.5, 102.0)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)])).iloc[0]
check("tie: stop wins in every R column", all(r[f"exit_kind_{k}"] == "stop" and r[f"exit_px_{k}"] == 98.75
                                              for k in ("1", "1.5", "2")))
# a target hit in an EARLIER minute stays a target; the later stop only ends the still-open targets
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:10", 100, 101.25, 100, 101).set(f"{DAY} 10:20", 101, 101, 98.5, 99)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)])).iloc[0]
check("target first, later stop ends the others", r.exit_kind_1 == "target" and r["exit_kind_1.5"] == "stop"
      and r.exit_kind_2 == "stop" and r["t_end_1.5"] == T("10:21"))

# (e) gap through the stop: minute opens at 98 (below stop 99) -> fill 98 - 1 tick = 97.75
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:15", 98.0, 98.5, 97.5, 98.25)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)])).iloc[0]
check("gap through stop: fill at open - 1 tick", r.exit_px_1 == 97.75 and approx(r.pnl_usd_1, (97.75 - 100) * USD - COST))
# gap through the target: limit order fills at the target, not at the better open
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:15", 103.0, 103.5, 102.5, 103.0)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)])).iloc[0]
check("gap through target: fill at target", r.exit_px_1 == 101.0 and r.exit_px_2 == 102.0 and r.exit_kind_2 == "target")

# (f) entry already past the stop: next bar opens at 98.5 below stop 99 -> exit at the entry open, loss = costs
p = Path([(T("09:00"), T("16:59"))]).level(f"{DAY} 10:00", f"{DAY} 16:59", 98.5)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 99.0)])).iloc[0]
check("entry past stop: pnl = -cost, kind stop, t_end = entry", r.past_stop and all(
    approx(r[f"pnl_usd_{k}"], -COST) and r[f"exit_kind_{k}"] == "stop" and r[f"t_end_{k}"] == T("10:00")
    for k in ("1", "1.5", "2")))
# REGRESSION (review: risk 0 was labelled "past", pnl -cost): an entry exactly AT the stop is walked; its first
# minute (open 98.5 = stop, low 98.5 <= stop) touches the stop -> stop fill 98.5 - 1 tick = 98.25,
# pnl = -0.25*5 - 3.5 = -4.75, t_end = end of the entry minute (10:01); risk_pts = risk_usd = 0
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), 1, 98.5)])).iloc[0]
check("entry == stop (long): not past, stopped in the entry minute at stop - 1 tick, pnl -4.75",
      not r.past_stop and r.risk_pts == 0 and r.risk_usd == 0 and all(
          r[f"exit_kind_{k}"] == "stop" and r[f"exit_px_{k}"] == 98.25 and approx(r[f"pnl_usd_{k}"], -COST - TICK * USD)
          and not r[f"y_{k}"] and r[f"t_end_{k}"] == T("10:01") for k in ("1", "1.5", "2")))

# ============================================================================ 2. short mirror
p = Path([(T("09:00"), T("16:59"))])
p.set(f"{DAY} 10:05", 100, 100, 99.0, 99.5)          # R1 target 99 needs low <= 98.75: exact 99 is no fill
p.set(f"{DAY} 10:09", 99.5, 99.5, 98.75, 99.0)        # R1 filled at 99
p.set(f"{DAY} 10:40", 99.0, 101.5, 99.0, 101.0)       # stop 101 (high >= 101) -> fill max(99, 101) + tick = 101.25
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), -1, 101.0)])).iloc[0]
check("short: risk = stop - entry = 1", r.risk_pts == 1.0 and r.target_1 == 99.0 and r["target_1.5"] == 98.5)
check("short: R1 target at 99 (needs 1 tick through)", r.exit_kind_1 == "target" and r.exit_px_1 == 99.0
      and r.t_end_1 == T("10:10") and approx(r.pnl_usd_1, 1.5))
check("short: stop fill = stop + 1 tick, pnl -9.75", r["exit_kind_1.5"] == "stop" and r["exit_px_1.5"] == 101.25
      and approx(r["pnl_usd_1.5"], -9.75) and r["t_end_1.5"] == T("10:41"))
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:15", 102.0, 102.5, 101.5, 102.0)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), -1, 101.0)])).iloc[0]
check("short: gap through stop fills at open + tick", r.exit_px_1 == 102.25)
p = Path([(T("09:00"), T("16:59"))]).set(f"{DAY} 10:20", 100.0, 101.25, 97.0, 98.0)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), -1, 101.0)])).iloc[0]
check("short: tie -> stop", r.exit_kind_2 == "stop" and r.exit_px_2 == 101.25)
p = Path([(T("09:00"), T("16:59"))]).level(f"{DAY} 10:00", f"{DAY} 16:59", 101.5)
install(p); b = sg.bars("ES", 15)
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), -1, 101.0)])).iloc[0]
check("short: entry past stop", r.past_stop and approx(r.pnl_usd_2, -COST))
# REGRESSION: short entry exactly AT the stop -> stop fill 101.5 + 1 tick = 101.75, pnl -4.75, not past
r = lb.label_entries("ES", 15, b, ev(b, [(T("09:45"), -1, 101.5)])).iloc[0]
check("short: entry == stop -> stop at stop + 1 tick in the entry minute", not r.past_stop and r.risk_pts == 0
      and r.exit_kind_2 == "stop" and r.exit_px_2 == 101.75 and approx(r.pnl_usd_2, -COST - TICK * USD)
      and r.t_end_2 == T("10:01"))

# ============================================================================ 3. 16:45 cutoff and sessions
# session A 09:00-16:59 (sess Mar 5), session B 18:00-19:59 (sess Mar 6)
p = Path([(T("09:00"), T("16:59")), (T("18:00"), T("19:59"))])
p.level(f"{DAY} 16:00", f"{DAY} 16:44", 100.25)
p.set(f"{DAY} 16:44", 100.25, 100.25, 100.25, 100.75)  # last minute before 16:45 closes at 100.75
p.level(f"{DAY} 16:45", f"{DAY} 16:59", 90.0)          # crash after the cutoff must be invisible
install(p); b = sg.bars("ES", 15)
lab = lb.label_entries("ES", 15, b, ev(b, [(T("16:00"), 1, 99.0), (T("16:15"), 1, 99.0)]), max_bars=16)
check("16:45: both trades end at the 16:30 bar's close (16:45), price 100.75, not stopped by the 16:45+ crash",
      (lab.exit_kind_2 == "time").all() and (lab.exit_px_2 == 100.75).all() and (lab.t_end_2 == T("16:45")).all())
check("16:45: 16:00 signal enters 16:15 at 100.25", lab.entry.iloc[0] == 100.25 and lab.t_entry.iloc[0] == T("16:15"))
ok, forced = lb.eligible(b, 15)
check("16:30 bar (entry would be 16:45) and later are not enterable; last session bar neither",
      not ok[b.index.get_loc(T("16:30"))] and not ok[b.index.get_loc(T("16:45"))] and ok[b.index.get_loc(T("16:15"))]
      and not ok[-1])
lab2 = lb.label_entries("ES", 15, b, ev(b, [(T("16:30"), 1, 99.0), (T("16:45"), 1, 99.0), (T("16:15"), 1, 99.0)]))
check("labeler drops non-enterable events", len(lab2) == 1 and lab2.t.iloc[0] == T("16:15"))
# time limit on 5-minute bars (generic tf): signal 10:00 bar, max_bars 3 -> exit at close of the 10:15 bar (10:20)
p = Path([(T("09:00"), T("16:59"))]).level(f"{DAY} 10:15", f"{DAY} 10:19", 100.5).level(f"{DAY} 10:20", f"{DAY} 16:59", 120)
install(p); b5 = sg.bars("ES", 5)
r = lb.label_entries("ES", 5, b5, ev(b5, [(T("10:00"), 1, 99.0)]), max_bars=3).iloc[0]
check("5-min: time exit at close of bar t+3 (10:20) at 100.5", r.exit_kind_2 == "time" and r.exit_px_2 == 100.5
      and r.t_end_2 == T("10:20") and r.t_entry == T("10:05"))
# contract roll inside a session: new contract = new segment, no entry across it
p = Path([(T("09:00"), T("16:59"))])
p.inst.loc[T("12:00"):] = 2
install(p); b = sg.bars("ES", 15)
ok, forced = lb.eligible(b, 15)
check("roll: 11:45 bar not enterable (next bar is another contract)", not ok[b.index.get_loc(T("11:45"))]
      and ok[b.index.get_loc(T("11:30"))])
r = lb.label_entries("ES", 15, b, ev(b, [(T("11:00"), 1, 99.0)])).iloc[0]
check("roll: time limit = last bar of the old contract (11:45, close 12:00)", r.exit_kind_2 == "time"
      and r.t_end_2 == T("12:00"))

# ============================================================================ 4. YM (tick 1, $0.5/pt)
p = Path([(T("09:00"), T("16:59"))], px=39000.0).set(f"{DAY} 10:10", 39000, 39000, 38989, 38990)
install(p); bY = sg.bars("YM", 15)
r = lb.label_entries("YM", 15, bY, ev(bY, [(T("09:45"), 1, 38990.0)])).iloc[0]
cY = sg.SPEC["YM"]["cost"]
check("YM: stop fill = 38990 - 1 = 38989, pnl = -11*0.5 - cost", r.exit_px_1 == 38989
      and approx(r.pnl_usd_1, -11 * 0.5 - cY) and approx(r.risk_usd, 5.0))

# ============================================================================ 5. entry_events / random_events
p = Path([(T("09:00"), T("16:59")), (T("18:00"), T("19:59"))])
rng = np.random.default_rng(1)
steps = rng.integers(-4, 5, len(p.df)) * TICK
c = 100 + np.cumsum(steps)
o = np.r_[100, c[:-1]]
p.df["Open"], p.df["Close"] = o, c
p.df["High"] = np.maximum(o, c) + TICK * rng.integers(0, 3, len(c))
p.df["Low"] = np.minimum(o, c) - TICK * rng.integers(0, 3, len(c))
install(p); b = sg.bars("ES", 15)
P = pd.DataFrame(0, index=b.index, columns=list(sg.PATTERN_RULES), dtype=np.int8)
L, H = b.L.to_numpy(), b.H.to_numpy()
pos = lambda hm: b.index.get_loc(T(hm))
P.loc[T("10:00"), "engulfing"] = 1                         # span 2
P.loc[T("11:00"), ["hammer", "five_lower_lows_higher_highs"]] = 1        # span 6 wins
P.loc[T("11:00"), "clv_extreme"] = -1                      # short on the same bar, span 1
P.loc[T("11:00"), "doji"] = 1                              # neutral: ignored
P.loc[T("16:30"), "marubozu"] = 1                          # entry would be 16:45: no event
P.loc[T("18:15"), "clv5_extreme"] = -1                     # span 5 but only 2 bars into the new session: clamped
P.loc[T("12:00"), "inside_bar"] = 1                        # neutral only: no event
E = lb.entry_events(b, P, sym="ES")
check("entry_events: 4 rows sorted by (bar, d): 10:00 L, 11:00 S+L, 18:15 S",
      len(E) == 4 and list(E.d) == [1, -1, 1, -1] and list(E.t) == [T("10:00"), T("11:00"), T("11:00"), T("18:15")])
e0 = E.iloc[0]
check("engulfing: stop = min L of 2 bars - tick", e0.t == T("10:00") and e0.patterns == ["engulfing"]
      and approx(e0.stop, min(L[pos("09:45")], L[pos("10:00")]) - TICK))
e1 = E.iloc[2]
check("11:00 long: two patterns, span 6", e1.n_patterns == 2 and set(e1.patterns) == {"hammer", "five_lower_lows_higher_highs"}
      and approx(e1.stop, L[pos("09:45"):pos("11:00") + 1].min() - TICK))
e2 = E.iloc[1]
check("11:00 short: clv_extreme, own high + tick", e2.patterns == ["clv_extreme"] and approx(e2.stop, H[pos("11:00")] + TICK))
e3 = E.iloc[3]
check("span clamped to the segment start", approx(e3.stop, H[pos("18:00"):pos("18:15") + 1].max() + TICK))
with warnings.catch_warnings(record=True) as wl:
    warnings.simplefilter("always")
    tk = lb.infer_tick(b)
check("infer_tick: 0.25 on this tape, but warns (only 80 prices)", tk == 0.25 and lb.infer_tf(b) == 15
      and any("pass sym= or tick=" in str(w.message) for w in wl))
with warnings.catch_warnings(record=True) as wl:
    warnings.simplefilter("always")
    E_inf = lb.entry_events(b, P)
check("entry_events without sym/tick: same stops here (inferred 0.25) + a warning",
      np.allclose(E_inf.stop, E.stop) and len(wl) >= 1)
R1 = lb.random_events(b, 0.5, 7, sym="ES")
R2 = lb.random_events(b, 0.5, 7, sym="ES")
okm, _ = lb.eligible(b, 15)
check("random_events: reproducible, eligible bars only, ~frac of them",
      R1.equals(R2) and okm[R1.i].all() and len(R1) == round(0.5 * okm.sum()) and R1.i.is_unique)
check("random_events: stop = own low - tick / high + tick", np.allclose(
    R1.stop, np.where(R1.d > 0, L[R1.i] - TICK, H[R1.i] + TICK)) and set(R1.d) == {-1, 1})
lab = lb.label_entries("ES", 15, b, E)
check("labels run on generated events, risk > 0", len(lab) == 4 and (lab.risk_pts > 0).all())

# ============================================================================ 6. exit rows
p = Path([(T("09:00"), T("16:59"))])
# trade A (long, signal 09:45, entry 10:00 @100, stop 99): bars 10:00 H100.5 L99.5 C100.25; 10:15 O100.25 H101
# L99.75 C100.75; 10:30 O100.75 then stop at 10:37 (open 99.25, low 98.5) -> fill 98.75
p.set(f"{DAY} 10:00", 100, 100.5, 99.5, 100.25).level(f"{DAY} 10:01", f"{DAY} 10:14", 100.25)
p.set(f"{DAY} 10:15", 100.25, 101.0, 99.75, 100.5).level(f"{DAY} 10:16", f"{DAY} 10:29", 100.75)
p.level(f"{DAY} 10:30", f"{DAY} 10:36", 100.75).set(f"{DAY} 10:37", 99.25, 99.25, 98.5, 99.0)
p.level(f"{DAY} 10:38", f"{DAY} 12:59", 99.0)
# trade B (short, signal 12:45, entry 13:00 @ 99, stop 102): never stopped; max_bars 4 -> ends at close of 13:45 bar
p.set(f"{DAY} 13:00", 99, 99.5, 98.0, 98.5).level(f"{DAY} 13:01", f"{DAY} 13:14", 98.5)
p.level(f"{DAY} 13:15", f"{DAY} 13:29", 98.0).level(f"{DAY} 13:30", f"{DAY} 13:44", 97.5)
p.level(f"{DAY} 13:45", f"{DAY} 13:58", 97.0).set(f"{DAY} 13:59", 97.0, 97.0, 97.0, 96.5)
p.level(f"{DAY} 14:00", f"{DAY} 16:59", 96.5)
install(p); b = sg.bars("ES", 15)
Fx = pd.DataFrame({"f_pos": np.arange(len(b), dtype=np.float32), "f_two": 2.0}, index=b.index)
sig = ev(b, [(T("09:45"), 1, 99.0)])
# 2nd: entry 96.5 already past the stop 97; 3rd: entry 96.5 (15:15 open) exactly AT the stop 96.5 (risk 0)
rnd = ev(b, [(T("12:45"), -1, 102.0), (T("14:00"), 1, 97.0), (T("15:00"), 1, 96.5)])
X = lb.exit_rows("ES", 15, b, Fx, sig, max_bars=4, frac=1.0, seed=0, rand=rnd)
A, B = X[X.src == "signal"], X[X.src == "random"]
check("exit rows: A has rows for 10:00 and 10:15 only (stopped inside 10:30)", list(A.ts) == [T("10:00"), T("10:15")])
check("exit rows: B rows = entry bar .. time bar - 1 (13:00, 13:15, 13:30)", list(B.ts) == [T("13:00"), T("13:15"), T("13:30")])
check("exit rows: past-stop and at-stop (risk 0) trades create no rows", X.trade.nunique() == 2
      and np.isfinite(X[["open_R", "mfe_R", "mae_R", "dist_stop_R"]].to_numpy()).all())
# REGRESSION (review: ids restarted at 0 in every call, no market column -> pooled markets merged trades)
check("exit rows: market column and readable trade ids",
      (X.market == "ES").all() and list(A.trade.unique()) == ["ES:signal:2024-03-05T09:45:L"]
      and list(B.trade.unique()) == ["ES:random:2024-03-05T12:45:S"])
XN = lb.exit_rows("NQ", 15, b, Fx, sig, max_bars=4, frac=1.0, seed=0, rand=rnd)   # same tape, NQ spec
pool = pd.concat([X, XN], ignore_index=True)
w = 1.0 / pool.groupby("trade")["trade"].transform("size").to_numpy()            # = walkforward.exit_weights
check("exit rows pooled over ES + NQ: 4 distinct trades, each with total weight 1",
      not set(X.trade) & set(XN.trade) and pool.trade.nunique() == 4 and (XN.market == "NQ").all()
      and np.allclose(pd.Series(w).groupby(pool.trade).sum().to_numpy(), 1.0))
X5 = lb.exit_rows("ES", 15, b, Fx, sig, max_bars=4, frac=1.0, seed=5, rand=rnd)
check("exit rows: trade id depends on the event only (another seed, same trades -> same ids)",
      list(X5.trade) == list(X.trade))
check("exit rows: F row k attached", (X.f_pos.to_numpy() == X.k.to_numpy()).all() and (X.f_two == 2).all())
a0, a1 = A.iloc[0], A.iloc[1]
check("A state k=10:00: open_R .25, mfe .5, mae .5, held 1, dist_stop 1.25",
      approx(a0.open_R, 0.25) and approx(a0.mfe_R, 0.5) and approx(a0.mae_R, 0.5) and a0.bars_held == 1
      and approx(a0.dist_stop_R, 1.25))
check("A state k=10:15: open_R .75, mfe 1, mae .5 (running), held 2",
      approx(a1.open_R, 0.75) and approx(a1.mfe_R, 1.0) and approx(a1.mae_R, 0.5) and a1.bars_held == 2)
check("A labels: exit at O[k+1] vs baseline stop fill 98.75 (incl. extra tick)",
      approx(a0.exit_gain_usd, (100.25 - 98.75) * USD) and approx(a1.exit_gain_usd, (100.75 - 98.75) * USD)
      and a0.y_exit and a0.end_kind == "stop" and approx(a0.hold_pnl_usd, (98.75 - 100) * USD - COST))
check("A t_end = end of the stop minute; mins_to_1645 = 16:30 - 10:00 = 390",
      a0.t_end == T("10:38") and a0.mins_to_1645 == 390 and a1.mins_to_1645 == 375)
# B short: entry 99; bars 13:00 (H 99.5 L 98 C 98.5), 13:15 (C 98), 13:30 (C 97.5), 13:45 (O 97, C 96.5)
b0, b1, b2 = B.iloc[0], B.iloc[1], B.iloc[2]
check("B short state: open_R = (99-98.5)/3, mfe 1/3, mae 0.5/3", approx(b0.open_R, 0.5 / 3) and approx(b0.mfe_R, 1 / 3)
      and approx(b0.mae_R, 0.5 / 3) and approx(b0.dist_stop_R, (102 - 98.5) / 3) and b0.d == -1)
check("B short: running mfe at 13:30 = (99-97.5)/3", approx(b2.mfe_R, 1.5 / 3) and approx(b2.mae_R, 0.5 / 3))
check("B labels: hold to time exit at 96.5; exit now at O[k+1]",
      approx(b0.exit_gain_usd, -(98.0 - 96.5) * USD) and approx(b2.exit_gain_usd, -(97.0 - 96.5) * USD)
      and not b2.y_exit and b2.end_kind == "time" and b2.t_end == T("14:00") and approx(b2.hold_pnl_usd, 2.5 * USD - COST))
XD = lb.exit_rows("ES", 15, b, Fx, ev(b, [(T("09:45"), 1, 99.0)] * 4), max_bars=4, frac=0.5, rand=rnd.iloc[:0])
check("exit rows: random sample of entry events by frac; identical events get '#n' ids",
      list(XD.trade.unique()) == ["ES:signal:2024-03-05T09:45:L", "ES:signal:2024-03-05T09:45:L#1"])

# ============================================================================ 7. R-unit trade state is clipped
# REGRESSION (review: a 1-tick risk gave |open_R| in the hundreds): long, stop 99.75 = 1 tick under the entry 100;
# the 10:00 bar runs to H 104.5 / C 104 -> raw open_R 16, mfe_R 18, dist_stop_R 17 -> all clipped to R_CLIP[1] = 10
def bar15(p, hm, O, H, L, C):
    """make the 15-min bar starting at hm exactly O/H/L/C: minute 0 flat at O, minute 1 spans L..H and closes at C,
    minutes 2..14 flat at C."""
    t0 = T(hm)
    p.set(t0, O, O, O, O).set(t0 + lb._MIN, O, H, L, C)
    return p.level(t0 + 2 * lb._MIN, t0 + 14 * lb._MIN, C)


p = bar15(Path([(T("09:00"), T("16:59"))]), "10:00", 100, 104.5, 100, 104).level(f"{DAY} 10:15", f"{DAY} 16:59", 104)
install(p); b = sg.bars("ES", 15)
Fx = pd.DataFrame({"f_pos": np.arange(len(b), dtype=np.float32)}, index=b.index)
XC = lb.exit_rows("ES", 15, b, Fx, ev(b, [(T("09:45"), 1, 99.75)]), max_bars=3, frac=1.0, rand=ev(b, [])[:0])
c0 = XC.iloc[0]
check("R clip: R_CLIP = (-5, 10); open_R / mfe_R / dist_stop_R clipped to 10, mae_R 0, risk_pts stays 0.25",
      lb.R_CLIP == (-5.0, 10.0) and c0.ts == T("10:00") and c0.open_R == 10 and c0.mfe_R == 10
      and c0.dist_stop_R == 10 and c0.mae_R == 0 and c0.risk_pts == 0.25
      and (XC[["open_R", "mfe_R", "dist_stop_R"]].to_numpy() <= 10).all())
check("R clip: labels unaffected (exit at O[10:15] = 104 vs time exit at 104 -> gain 0)",
      approx(c0.exit_gain_usd, 0.0) and not c0.y_exit and approx(c0.hold_pnl_usd, 4 * USD - COST))

# ============================================================================ 8. breakout stops (REGRESSION)
# review: the breakouts used exits.SPAN = 3, which misses the mother / NR7 bar when the breakout comes 2-3 bars after
# the setup bar. Now the stop spans the pattern's actual extent (mother / NR7 bar .. breakout bar).
p = Path([(T("09:00"), T("16:59"))])
# A: mother 10:00 (L 97), inside 10:15, no close beyond 102 / 97 at 10:30 / 10:45, long breakout at 11:00 (3 after)
bar15(p, "10:00", 100, 102, 97, 100); bar15(p, "10:15", 100, 101, 99, 100.5)
bar15(p, "10:30", 100.5, 101.5, 99.5, 101); bar15(p, "10:45", 101, 101.75, 100, 101.5)
bar15(p, "11:00", 101.5, 103, 101, 102.5)
# B: a 104 high at 12:30 (2 bars before the mother 13:00); inside 13:15; short breakout at 13:30 (1 bar after)
bar15(p, "12:30", 100, 104, 100, 100); bar15(p, "13:00", 100, 101, 98, 100)
bar15(p, "13:15", 100, 100.5, 99, 100); bar15(p, "13:30", 100, 100, 97.5, 97.75)
# C: a 97 low at 14:00 (before the NR7 bar 14:15, L 99); no close beyond 100.5 / 99 at 14:30 / 14:45; long breakout
#    at 15:00 (3 bars after the NR7 bar)
bar15(p, "14:00", 100, 100, 97, 100); bar15(p, "14:15", 100, 100.5, 99, 100)
bar15(p, "14:30", 100, 100.25, 99.5, 100); bar15(p, "14:45", 100, 100.25, 99.5, 100)
bar15(p, "15:00", 100, 101, 99.75, 100.75)
# D: NR7 bar 15:45, long breakout at 16:00 (1 bar after; exact extent 2 < exits.SPAN 3); 98.5 low at 15:30 (j-2)
bar15(p, "15:30", 100, 100, 98.5, 100); bar15(p, "15:45", 100, 100.25, 99.75, 100)
bar15(p, "16:00", 100, 100.75, 99.75, 100.5)
install(p); b = sg.bars("ES", 15)
P = pd.DataFrame(0, index=b.index, columns=list(sg.PATTERN_RULES), dtype=np.int8)
P.loc[[T("10:15"), T("13:15")], "inside_bar"] = 1
P.loc[T("11:00"), "inside_bar_breakout"] = 1
P.loc[T("13:30"), "inside_bar_breakout"] = -1
P.loc[[T("14:15"), T("15:45")], "nr7"] = 1
P.loc[[T("15:00"), T("16:00")], "nr7_breakout"] = 1
pos = lambda hm: b.index.get_loc(T(hm))
S = lb.breakout_spans(b, P)
check("breakout_spans (exact extents): 11:00 = 5 (mother 10:00 .. 11:00), 13:30 = 3 (13:00 .. 13:30), "
      "nr7 15:00 = 4 (14:15 .. 15:00), nr7 16:00 = 2 (15:45 .. 16:00), 1 where nothing fires",
      S["inside_bar_breakout"][pos("11:00")] == 5 and S["inside_bar_breakout"][pos("13:30")] == 3
      and S["nr7_breakout"][pos("15:00")] == 4 and S["nr7_breakout"][pos("16:00")] == 2
      and S["inside_bar_breakout"][pos("12:00")] == 1)
E = lb.entry_events(b, P, sym="ES").set_index("t")
check("inside_bar_breakout 3 bars late: long stop = mother low 97 - tick (exits.SPAN 3 gave 99.5 - tick)",
      approx(E.loc[T("11:00"), "stop"], 96.75))
check("inside_bar_breakout 1 bar after: short stop = max H mother..breakout 101 + tick (not the 12:30 high 104)",
      approx(E.loc[T("13:30"), "stop"], 101.25) and E.loc[T("13:30"), "d"] == -1)
check("nr7_breakout 3 bars late: long stop = NR7 low 99 - tick (exits.SPAN 3 gave 99.5 - tick; not the 14:00 low)",
      approx(E.loc[T("15:00"), "stop"], 98.75))
check("nr7_breakout 1 bar after: span = max(2, exits.SPAN 3) -> 15:30 low 98.5 - tick (never tighter than SPEC)",
      approx(E.loc[T("16:00"), "stop"], 98.25))
# without the setup columns the largest possible extent is used (5 / 4 bars): never tighter than the textbook stop
E2 = lb.entry_events(b, P.drop(columns=["inside_bar", "nr7"]), sym="ES").set_index("t")
check("breakout fallback (no setup columns): spans 5 / 4 -> 96.75, 104.25, 98.75, 98.25",
      approx(E2.loc[T("11:00"), "stop"], 96.75) and approx(E2.loc[T("13:30"), "stop"], 104.25)
      and approx(E2.loc[T("15:00"), "stop"], 98.75) and approx(E2.loc[T("16:00"), "stop"], 98.25))
# the setup recovery agrees with the real signals.patterns on this tape
with warnings.catch_warnings():
    warnings.simplefilter("ignore", RuntimeWarning)                     # nr7's all-NaN lookback on a 32-bar tape
    Pr = sg.patterns(b, sg.context(b), tick=TICK)
Sr = lb.breakout_spans(b, Pr)
check("real signals.patterns: fires at 11:00 (+1) and 13:30 (-1) from the inside bars; spans 5 and 3",
      Pr.inside_bar_breakout.iloc[pos("11:00")] == 1 and Pr.inside_bar_breakout.iloc[pos("13:30")] == -1
      and Pr.inside_bar.iloc[pos("10:15")] == 1 and Pr.inside_bar.iloc[pos("13:15")] == 1
      and Sr["inside_bar_breakout"][pos("11:00")] == 5 and Sr["inside_bar_breakout"][pos("13:30")] == 3
      and set(np.unique(Sr["inside_bar_breakout"][Pr.inside_bar_breakout.to_numpy() != 0])) <= {3, 4, 5})

# ============================================================================ 9. tick from sym (REGRESSION)
# review: entry_events inferred the tick from b's prices; on a short slice on a coarse grid (all prices whole points)
# it inferred 1.0 and put the stop 4 ES ticks beyond the extreme. sym= / tick= now give the market's tick.
p = bar15(Path([(T("09:00"), T("16:59"))]), "10:00", 100, 101, 99, 100)
install(p); b = sg.bars("ES", 15)
P = pd.DataFrame(0, index=b.index, columns=list(sg.PATTERN_RULES), dtype=np.int8)
P.loc[T("10:00"), "clv_extreme"] = 1
with warnings.catch_warnings(record=True) as wl:
    warnings.simplefilter("always")
    s_inf = lb.entry_events(b, P).stop.iloc[0]
check("coarse grid: inferred tick 1.0 -> stop 98, with a warning", approx(s_inf, 98.0)
      and any("pass sym= or tick=" in str(w.message) for w in wl))
with warnings.catch_warnings():
    warnings.simplefilter("error")                                       # sym= / tick= never infer, never warn
    s_sym = lb.entry_events(b, P, sym="ES").stop.iloc[0]
    s_tk = lb.entry_events(b, P, tick=0.25).stop.iloc[0]
    Rs = lb.random_events(b, 1.0, 0, sym="ES")
check("sym='ES' / tick=0.25: stop = 99 - 0.25; random_events too", approx(s_sym, 98.75) and approx(s_tk, 98.75)
      and np.allclose(Rs.stop, np.where(Rs.d > 0, b.L.to_numpy()[Rs.i] - TICK, b.H.to_numpy()[Rs.i] + TICK)))
print("all label tests passed")
