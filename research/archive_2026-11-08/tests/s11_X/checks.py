"""Independent sanity checks against the RAW 1-minute CSVs (not the cache):
 1. spot-check trades by hand-style minute loops (entry/exit price and time)
 2. no trade spans a roll (entry and exit bars carry the same instrument_id; A/B use the prior-day contract)
 3. no look-ahead (decision inputs come from bars that closed before the entry bar)"""
import math

import numpy as np
import pandas as pd

import s11common as sc

TICK = 0.25
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)


def raw(sym):
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"])
    ts = pd.DatetimeIndex(pd.to_datetime(d.ts_event, utc=True, format="ISO8601")).tz_convert("America/New_York")
    d["date"] = ts.strftime("%Y-%m-%d")
    d["hm"] = ts.strftime("%H:%M")
    d = d[(d.hm >= "08:00") & (d.hm <= "15:59")]
    return d.set_index(["date", "hm"]).sort_index()


def day(R, date):
    return R.loc[str(pd.Timestamp(date).date())]


def walk(x, entry_hm, exit_by_hm, dirn, stop, target=None):
    """minute loop: market entry at entry_hm open; stop (touch, gap at open), target (1-tick trade-through);
    time exit at the open of the first bar at/after exit_by_hm."""
    bars = x[x.index >= entry_hm]
    entry = bars.Open.iloc[0]
    for hm, b in bars.iterrows():
        if hm >= exit_by_hm:
            if (dirn > 0 and b.Open <= stop) or (dirn < 0 and b.Open >= stop):
                return entry, b.Open, hm, "stop"
            return entry, b.Open, hm, "time"
        s_hit = b.Low <= stop if dirn > 0 else b.High >= stop
        t_hit = target is not None and not math.isnan(target) and (b.High >= target + TICK if dirn > 0 else b.Low <= target - TICK)
        if s_hit:
            px = min(stop, b.Open) if dirn > 0 else max(stop, b.Open)
            return entry, px, hm, "stop"
        if t_hit:
            return entry, target, hm, "target"
    raise RuntimeError("no exit")


def snap(x, dirn, kind):
    if kind == "stop":
        return math.floor(x / TICK + 1e-9) * TICK if dirn > 0 else math.ceil(x / TICK - 1e-9) * TICK
    return math.ceil(x / TICK - 1e-9) * TICK if dirn > 0 else math.floor(x / TICK + 1e-9) * TICK


def prev_close(x, hm):
    """price at hm = close of the last bar strictly before hm (bar hm-1, forward-filled)."""
    return x[x.index < hm].Close.iloc[-1]


def hm_add(hm, k):
    h, m = map(int, hm.split(":"))
    t = h * 60 + m + k
    return f"{t // 60:02d}:{t % 60:02d}"


def check_A(R, tr, picks, kind="fade"):
    for i in picks:
        t = tr.iloc[i]
        x = day(R, t.date)
        T = t.decision
        P = prev_close(x, T)
        if kind == "fade":
            P60 = prev_close(x, hm_add(T, -60))
            dP = P - P60
            dirn = -np.sign(dP)
            tgt = snap(P - 0.5 * dP, dirn, "tgt")
            sd = abs(dP)
        else:
            rth = x[(x.index >= "09:30") & (x.index < T)]
            tp = (rth.High + rth.Low + rth.Close) / 3
            vw = (tp * rth.Volume).sum() / rth.Volume.sum()
            dev = P - vw
            dirn = -np.sign(dev)
            tgt = snap(vw, dirn, "tgt")
            sd = abs(dev)
        entry = x.loc[T].Open
        stop = snap(entry - dirn * sd, dirn, "stop")
        e, px, hm, why = walk(x, T, min(hm_add(T, 60), "15:00"), dirn, stop, tgt)
        ok = (abs(e - t.entry) < 1e-9 and abs(px - t.exit) < 1e-9 and hm == t.exit_time and why == t.exit_reason
              and dirn == (1 if t.side == "long" else -1) and abs(P - t.P_T) < 1e-9)
        say(f"  {kind} {t.date.date()} dec {T} P={P} side {t.side} entry {e} stop {stop} tgt {tgt} -> exit {px} at {hm} "
            f"({why}); csv: {t.entry}/{t.exit}/{t.exit_time}/{t.exit_reason}  {'OK' if ok else 'MISMATCH'}")
        assert ok


def tstat_day(x, upto_hm):
    """naive loop computation of T_t at bar upto_hm for one day (closes from 08:00, missing minute -> r=0)."""
    mins = [hm_add("08:00", k) for k in range(0, 480)]
    c = x.Close.reindex(mins).ffill()
    r = np.r_[0.0, np.diff(np.log(c.to_numpy()))]
    r = np.nan_to_num(r)
    t = mins.index(upto_hm)
    D = sum(math.exp(-j / 5) * r[t - j] for j in range(30))
    V = sum(math.exp(-j / 25) * r[t - j] ** 2 for j in range(120)) / sum(math.exp(-j / 25) for j in range(120))
    return D / math.sqrt(V * sum(math.exp(-2 * j / 5) for j in range(30)))


def check_B(R, tr, picks):
    for i in picks:
        t = tr.iloc[i]
        x = day(R, t.date)
        # first arming bar in 10:29..14:29
        arm = None
        for k in range(sc.slot(1029), sc.slot(1429) + 1):
            hm = sc.slot_time(k)
            v = tstat_day(x, hm)
            if abs(v) >= 4.0:
                arm, s = hm, np.sign(v)
                break
        hm, prev = arm, s * tstat_day(x, arm)
        while True:
            hm = hm_add(hm, 1)
            cur = s * tstat_day(x, hm)
            if cur < prev:
                break
            prev = cur
        peak = hm_add(hm, -1)
        ent_hm = hm_add(hm, 1)
        c = x.Close.reindex([hm_add("08:00", k) for k in range(480)]).ffill()
        M = abs(c[peak] - c[hm_add(peak, -5)])
        dirn = -s
        entry = x.loc[ent_hm].Open
        stop = entry - dirn * M
        e, px, xh, why = walk(x, ent_hm, hm_add(ent_hm, 15), dirn, stop)
        ok = arm == t.arm_time and peak == t.peak_time and abs(e - t.entry) < 1e-9 and abs(px - t.exit) < 1e-9 and xh == t.exit_time and why == t.exit_reason
        say(f"  B {t.date.date()} arm {arm} peak {peak} entry {ent_hm} @{e} M={M} stop {stop} -> {px} at {xh} ({why}); "
            f"csv arm {t.arm_time} peak {t.peak_time} {t.entry}/{t.exit}/{t.exit_time}  {'OK' if ok else 'MISMATCH'}")
        assert ok


def check_C(R, rv, b0, picks):
    for i in picks:
        t = rv.iloc[i]
        x = day(R, t.date)
        rth = x[x.index >= "09:30"]
        orh, orl = rth.loc["09:30":"09:34"].High.max(), rth.loc["09:30":"09:34"].Low.min()
        mid = (orh + orl) / 2
        d = 1 if t.orb_side == "long" else -1
        o = b0[b0.date == t.date].iloc[0]
        fail = None
        for k in range(0, 85, 5):
            f = hm_add("09:35", k)
            cl = rth[rth.index <= hm_add(f, 4)].Close.iloc[-1]
            if d * (cl - mid) < 0:
                fail = f
                break
        act = hm_add(fail, 5)
        seg = rth.loc["09:35":hm_add(fail, 4)]
        stop = seg.High.max() + 0.5 if d > 0 else seg.Low.min() - 0.5
        tgt = None
        e, px, xh, why = walk(x, act, "14:00", -d, stop, tgt)
        # ORB was not stopped up to the failure bar's end
        orb_stop = orl if d > 0 else orh
        not_stopped = (seg.Low > orb_stop).all() if d > 0 else (seg.High < orb_stop).all()
        ok = fail == t.failure_bar and abs(e - t.entry) < 1e-9 and abs(px - t.exit) < 1e-9 and xh == t.exit_time and not_stopped
        say(f"  C {t.date.date()} ORB {t.orb_side} OR {orl}-{orh} mid {mid} fail bar {fail} rev entry {act}@{e} stop {stop} -> {px} at {xh} ({why}); "
            f"csv {t.failure_bar} {t.entry}/{t.exit}/{t.exit_time}/{t.exit_reason}  {'OK' if ok else 'MISMATCH'}")
        assert ok


def roll_check(R, tr, name, need_prev_contract):
    """entry and exit bars of each trade carry the same instrument id, equal to the prior trading day's contract."""
    days = sorted(set(R.index.get_level_values(0)))
    inst_day = R.xs("09:30", level=1).instrument_id
    bad = 0
    for t in tr.itertuples():
        dk = str(t.date.date())
        ie = R.loc[(dk, t.entry_time)].instrument_id
        ix = R.loc[(dk, t.exit_time)].instrument_id if (dk, t.exit_time) in R.index else ie
        prev = inst_day[inst_day.index < dk].iloc[-1] if need_prev_contract else ie
        bad += int(ie != ix or ie != prev)
    say(f"  roll check {name}: {len(tr)} trades, violations {bad}")
    assert bad == 0


def main():
    rng = np.random.default_rng(sc.SEED)
    RN = raw("NQ")
    RE = raw("ES")
    rd = lambda n: pd.read_csv(f"{sc.OUT}/trades_{n}.csv", parse_dates=["date"])
    A, A1, A2, B, BM, B1 = rd("A"), rd("A1-MES"), rd("A2-VWAP"), rd("B"), rd("B-MES"), rd("B1")
    C = rd("C_reverse_leg")
    C2 = rd("C2-target_reverse_leg")
    b0 = rd("C_B0_orb")
    say("SPOT CHECKS (raw CSV, minute loops)")
    pickA = list(rng.choice(len(A), 4, replace=False)) + [int(A.exit_reason.eq("stop").idxmax()), int(A.exit_reason.eq("target").idxmax())]
    check_A(RN, A, pickA)
    check_A(RE, A1, list(rng.choice(len(A1), 2, replace=False)))
    check_A(RN, A2, list(rng.choice(len(A2), 2, replace=False)), kind="vwap")
    check_B(RN, B, list(rng.choice(len(B), 3, replace=False)))
    check_B(RE, BM, list(rng.choice(len(BM), 2, replace=False)))
    check_C(RN, C, b0, list(rng.choice(len(C), 4, replace=False)) + [int(C.exit_reason.eq("stop").idxmax())])
    say("ROLL CHECKS")
    for n, t, r, prevc in [("A", A, RN, True), ("A1-MES", A1, RE, True), ("A2-VWAP", A2, RN, True), ("B", B, RN, True),
                           ("B-MES", BM, RE, True), ("B1", B1, RN, True), ("C reverse", C, RN, False),
                           ("C2 reverse", C2, RN, False)]:
        roll_check(r, t, n, prevc)
    say("LOOK-AHEAD CHECKS")
    # A: entry at/after the decision bar; inputs = closes of bars before it; one position: next entry only after exit
    for n, t in [("A", A), ("A1-MES", A1), ("A2-VWAP", A2)]:
        assert (t.entry_slot >= t.dec_slot).all()
        bad = 0
        for _, g in t.groupby("date"):
            g = g.sort_values("entry_slot")
            prev_x, prev_open = g.exit_slot.shift(), g.at_open.shift()
            ok = (g.entry_slot > prev_x) | ((g.entry_slot == prev_x) & (prev_open == True)) | prev_x.isna()
            bad += int((~ok).sum())
        assert (t.exit_slot <= sc.slot(1500)).all()
        say(f"  {n}: entries at/after decision bar, no overlapping positions (violations {bad}), all flat by 15:00")
        assert bad == 0
    for n, t in [("B", B), ("B-MES", BM), ("B1", B1)]:
        ps = t.peak_time.map(lambda h: sc.slot(int(h.replace(":", ""))))
        ar = t.arm_time.map(lambda h: sc.slot(int(h.replace(":", ""))))
        assert ((t.entry_slot >= ps + 2) & (ps >= ar)).all() and (t.entry_slot <= sc.slot(1430)).all()
        say(f"  {n}: entry bar >= peak+2 (peak confirmed by the close of bar peak+1), entry <= 14:30, exit <= 14:45: "
            f"{bool((t.exit_slot <= sc.slot(1445)).all())}")
    fb = C.failure_bar.map(lambda h: int(h[:2]) * 60 + int(h[3:]))
    en = C.entry_time.map(lambda h: int(h[:2]) * 60 + int(h[3:]))
    assert (en >= fb + 5).all()
    say("  C: reverse entry at/after the bar following the failure 5-min bar's close (all)")
    with open(f"{sc.OUT}/checks_output.txt", "w") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
