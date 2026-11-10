"""Independent checks of the saved trades against the RAW 1-minute CSV rows (not the cached grid):
  1. every trade: entry = raw Open of the entry minute; same instrument_id on every raw bar entry..exit (no roll);
     entry/exit on the same date; exit logic consistent with raw bars (first stop touch / target trade-through /
     time exit at the raw Open);
  2. look-ahead: A signal recomputed from raw closes stamped before T; B statistic recomputed with every bar from
     the entry bar on removed (the arming and peak must be unchanged); C failure close from raw bar stamped <= f+4;
  3. a printed hand spot-check of 8 trades (raw bars around entry and exit)."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s11y_common as c  # noqa: E402
import rule_B as rb  # noqa: E402

P = lambda f: os.path.join(c.OUT, f)  # noqa: E731
TICK = c.TICK


def raw(sym):
    d = pd.read_csv(os.path.join(c.PROJ, "data", f"{sym}_fut_1m.csv"))
    ts = pd.DatetimeIndex(pd.to_datetime(d.ts_event, utc=True, format="ISO8601")).tz_convert("America/New_York")
    d.index = ts.tz_localize(None)
    return d.drop(columns="ts_event")


def bars(R, date, t0, t1):
    a = pd.Timestamp(f"{date.date()} {t0}")
    b = pd.Timestamp(f"{date.date()} {t1}")
    return R.loc[a:b]


def check_trade(R, r, cost, kind):
    """returns list of problems for one trade (dict-like row with date, entry_time, exit_time, dir, entry, exit,
    exit_reason, stop, target)."""
    probs = []
    d = int(r["dir"])
    b = bars(R, r["date"], r["entry_time"], r["exit_time"])
    if len(b) == 0 or b.index[0] != pd.Timestamp(f"{r['date'].date()} {r['entry_time']}"):
        return ["entry bar missing in raw"]
    if abs(b.Open.iloc[0] - r["entry"]) > 1e-9:
        probs.append(f"entry {r['entry']} != raw open {b.Open.iloc[0]}")
    if b.instrument_id.nunique() != 1:
        probs.append("instrument changes inside trade (roll)")
    stop, tgt = r["stop"], r.get("target", np.nan)
    tgt = np.nan if tgt is None else tgt
    held = b.iloc[:-1] if r["exit_reason"] in ("time60", "flat1500", "time15", "time") else b.iloc[:-1]
    # no stop touch / target trade-through on bars before the exit bar
    if len(held):
        st = (held.Low <= stop) if d > 0 else (held.High >= stop)
        if st.any():
            probs.append(f"stop touched earlier at {st.idxmax()}")
        if not np.isnan(tgt):
            tt = (held.High >= tgt + TICK) if d > 0 else (held.Low <= tgt - TICK)
            if tt.any():
                probs.append(f"target traded through earlier at {tt.idxmax()}")
    last = b.iloc[-1]
    xr = r["exit_reason"]
    if xr == "stop":
        touched = (last.Low <= stop) if d > 0 else (last.High >= stop)
        opened_beyond = (last.Open <= stop) if d > 0 else (last.Open >= stop)
        if not (touched or opened_beyond):
            probs.append("stop exit bar does not touch the stop")
        exp = last.Open if ((d > 0 and last.Open < stop) or (d < 0 and last.Open > stop)) else stop
        if b.index[-1] == b.index[0]:
            exp = stop if not ((d > 0 and last.Open < stop) or (d < 0 and last.Open > stop)) else last.Open
        if abs(exp - r["exit"]) > 1e-9:
            probs.append(f"stop fill {r['exit']} != expected {exp}")
    elif xr == "target":
        if abs(r["exit"] - tgt) > 1e-9:
            probs.append("target fill != target")
        tt = (last.High >= tgt + TICK) if d > 0 else (last.Low <= tgt - TICK)
        st = (last.Low <= stop) if d > 0 else (last.High >= stop)
        if not tt or st:
            probs.append("target bar inconsistent (no trade-through or stop also touched)")
    else:
        if abs(last.Open - r["exit"]) > 1e-9:
            probs.append(f"time exit {r['exit']} != raw open {last.Open}")
    gross = d * (r["exit"] - r["entry"])
    if abs(gross - r["gross_pts"]) > 1e-6 or abs(gross - cost - r["net_pts"]) > 1e-6:
        probs.append("pnl arithmetic")
    return probs


def check_file(R, f, sym, kind):
    T = pd.read_csv(P(f), parse_dates=["date"])
    if "dir" not in T:
        T["dir"] = np.where(T.side == "long", 1, -1)
    if "target" not in T:
        T["target"] = np.nan
    cost = c.SPEC[sym]["cost_pts"]
    bad = []
    for _, r in T.iterrows():
        p = check_trade(R, r, cost, kind)
        if p:
            bad.append((str(r.date.date()), r.entry_time, p))
    # entry and exit on the same date, flat by the rule's limit
    late = {"A": "15:00", "B": "14:45", "C": "14:00"}[kind]
    n_late = int((T.exit_time > late).sum())
    return len(T), bad, n_late


def lookahead_A(R, sym, f):
    """r60 / VWAP recomputed from raw bars stamped before T only."""
    T = pd.read_csv(P(f), parse_dates=["date"])
    worst = 0.0
    for _, r in T.sample(min(60, len(T)), random_state=1).iterrows():
        day = R.loc[pd.Timestamp(f"{r.date.date()} 08:00"):pd.Timestamp(f"{r.date.date()} 15:59")]
        Tts = pd.Timestamp(f"{r.date.date()} {r.entry_time}")
        before = day[day.index < Tts]
        P_T = before.Close.iloc[-1]
        worst = max(worst, abs(P_T - r.P_T))
        if "r60" in T and not np.isnan(r.get("r60", np.nan)):
            p60 = before[before.index < Tts - pd.Timedelta(minutes=60)].Close.iloc[-1]
            worst = max(worst, abs(np.log(P_T / p60) - r.r60) * 1e4)
        if "vwap" in T and not np.isnan(r.get("vwap", np.nan)):
            rth = before[before.index >= pd.Timestamp(f"{r.date.date()} 09:30")]
            tp = (rth.High + rth.Low + rth.Close) / 3
            vw = (tp * rth.Volume).sum() / rth.Volume.sum()
            worst = max(worst, abs(vw - r.vwap))
    return worst


def lookahead_B(sym, f):
    """Truncate each event day's closes at the bar before entry (t') and recompute arming and peak."""
    g = c.load_grid(sym)
    T = pd.read_csv(P(f), parse_dates=["date"])
    bad = 0
    for _, r in T.iterrows():
        i = int(r.di)
        e = int(r.entry_slot)
        cf = g["Cff"][i].copy()
        cf[e:] = np.nan                                     # bars stamped >= entry not yet known
        Tt = rb.burst_stat(cf)
        arm = next(t for t in range(rb.ARM_FIRST, rb.ARM_LAST + 1) if abs(Tt[t]) >= rb.CV)
        s = int(np.sign(Tt[arm]))
        tp = next(t2 for t2 in range(arm + 1, e) if s * Tt[t2] < s * Tt[t2 - 1])
        if c.hhmm(arm) != r.arm_time or tp + 1 != e or c.hhmm(tp - 1) != r.peak_time:
            bad += 1
    return len(T), bad


def lookahead_C(R):
    T = pd.read_csv(P("C_reverse_leg_trades.csv"), parse_dates=["date"])
    bad = 0
    for _, r in T.sample(100, random_state=2).iterrows():
        fb = pd.Timestamp(f"{r.date.date()} {r.fail_bar}")
        last = R.loc[:fb + pd.Timedelta(minutes=4)]
        cl = last.Close.iloc[-1]
        ok_close = abs(cl - r.fail_close) < 1e-9
        ok_side = (cl < r.mid) if r.orb_side > 0 else (cl > r.mid)
        ent = pd.Timestamp(f"{r.date.date()} {r.entry_time}")
        if not (ok_close and ok_side and ent >= fb + pd.Timedelta(minutes=5)):
            bad += 1
        # earlier 5-min closes (from 09:35) must not have been on the far side
        t = pd.Timestamp(f"{r.date.date()} 09:39")
        while t < fb + pd.Timedelta(minutes=4):
            c5 = R.loc[:t].Close.iloc[-1]
            if (r.orb_side > 0 and c5 < r.mid) or (r.orb_side < 0 and c5 > r.mid):
                bad += 1
                break
            t += pd.Timedelta(minutes=5)
    return bad


def spot(R, f, k, label):
    T = pd.read_csv(P(f), parse_dates=["date"])
    r = T.iloc[k]
    print(f"\n=== spot-check {label} #{k}: {r.date.date()} {r.side} entry {r.entry_time} @ {r.entry} exit "
          f"{r.exit_time} @ {r.exit} ({r.exit_reason}); stop {r.stop} target {r.get('target', None)} net {r.net_pts:+.2f} pts")
    e = pd.Timestamp(f"{r.date.date()} {r.entry_time}")
    x = pd.Timestamp(f"{r.date.date()} {r.exit_time}")
    sl = R.loc[e - pd.Timedelta(minutes=2):e + pd.Timedelta(minutes=1)]
    print(sl[["Open", "High", "Low", "Close", "instrument_id"]].to_string())
    print("  ...")
    sl = R.loc[x - pd.Timedelta(minutes=2):x]
    print(sl[["Open", "High", "Low", "Close", "instrument_id"]].to_string())
    seg = R.loc[e:x]
    print(f"  held-bars range: low {seg.Low.min()} high {seg.High.max()}; instruments {seg.instrument_id.unique().tolist()}")


def main():
    RN = raw("NQ")
    RE = raw("ES")
    out = {}
    for f, sym, kind in [("A_trades.csv", "NQ", "A"), ("A2_trades.csv", "NQ", "A"), ("A1_trades.csv", "ES", "A"),
                         ("A_C2_uncalm_trades.csv", "NQ", "A"), ("B_trades.csv", "NQ", "B"),
                         ("B-MES_trades.csv", "ES", "B"), ("C_reverse_leg_trades.csv", "NQ", "C"),
                         ("C2_target_reverse_leg_trades.csv", "NQ", "C")]:
        n, bad, late = check_file(RN if sym == "NQ" else RE, f, sym, kind)
        out[f] = dict(n=n, problems=len(bad), late_exits=late, examples=bad[:5])
        print(f, out[f])
    print("lookahead A max abs diff (pts or bp):", lookahead_A(RN, "NQ", "A_trades.csv"),
          lookahead_A(RN, "NQ", "A2_trades.csv"), lookahead_A(RE, "ES", "A1_trades.csv"))
    print("lookahead B (n, mismatches):", lookahead_B("NQ", "B_trades.csv"), lookahead_B("ES", "B-MES_trades.csv"))
    print("lookahead C mismatches (100 sampled):", lookahead_C(RN))
    for f, k, lab in [("A_trades.csv", 0, "A"), ("A_trades.csv", 500, "A"), ("A_trades.csv", 1200, "A"),
                      ("A2_trades.csv", 100, "A2"), ("B_trades.csv", 5, "B"), ("C_reverse_leg_trades.csv", 10, "C"),
                      ("C_reverse_leg_trades.csv", 900, "C"), ("C2_target_reverse_leg_trades.csv", 300, "C2")]:
        spot(RN, f, k, lab)


if __name__ == "__main__":
    main()
