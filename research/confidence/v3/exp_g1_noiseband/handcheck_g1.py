"""
G1 hand check - HEAVY (raw 1-minute NQ data; run under the shared flock).

10 random A1 trades (v3/out/trades/A1.parquet) are re-derived from the RAW research_lib.bars_1m rows with no g1lib /
v3 bar code: entry and exit prices (open of the 1-minute bar at the mark, else the last close before it), and the
signal at every decision time of the trade: C(t) = close of the last 1-minute bar before t, O_d = 09:30 open,
C_{d-1} = previous session's last close before 16:00 (same contract; else its last price), sigma(t) = mean |C(t)/O - 1|
over the previous 14 full sessions (last bar at/after 16:00), UB/LB, RTH VWAP from 5-minute buckets of raw minutes.
Checks: entry px, exit px, entry condition (long: C > UB; short: C < LB), hold conditions at intermediate decisions
and the exit condition at the exit decision (long exits if C < max(UB, VWAP) - or C < LB; short mirror).
Output: v3/exp_g1_noiseband/handcheck_10.csv
"""
import os

import numpy as np
import pandas as pd

import harness as H
import research_lib as rl

HERE = os.path.dirname(os.path.abspath(__file__))
NY = "America/New_York"
DEC = ["1000", "1030", "1100", "1130", "1200", "1230", "1300", "1330", "1400", "1430", "1500", "1530"]


def main():
    tr = pd.read_parquet(os.path.join(H.HERE, "out", "trades", "A1.parquet"))
    rng = np.random.default_rng(20261109)
    pick = tr.iloc[np.sort(rng.choice(len(tr), 10, replace=False))]
    m = rl.bars_1m("NQ")
    m = m.loc[m.index < pd.Timestamp("2025-06-30 18:00").tz_localize(NY)]        # holdout never loaded further
    m = m.set_axis(m.index.tz_localize(None))
    tmin = m.index.hour * 60 + m.index.minute
    m = m.loc[~((tmin >= 16 * 60 + 45) & (tmin < 18 * 60))]
    # per session: kept contract = contract of the session's last row; per-session info table
    m = m.assign(sess=(m.index + pd.Timedelta(hours=6)).normalize())
    last_inst = m.groupby("sess").instrument_id.transform("last")
    m = m.loc[m.instrument_id == last_inst]
    info = m.groupby("sess").agg(last_ts=("Close", lambda s: s.index[-1]), inst=("instrument_id", "last"))
    info["last_off"] = (info.last_ts - (info.index - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1)
    info["early"] = info.last_off < 1320

    def sess_rows(D):
        return m.loc[(m.index >= D - pd.Timedelta(hours=6)) & (m.index < D + pd.Timedelta(hours=16, minutes=45))]

    def C_at(r, D, hhmm):
        t = D + pd.Timedelta(hours=int(hhmm[:2]), minutes=int(hhmm[2:]))
        x = r.loc[r.index < t]
        return float(x.Close.iloc[-1]) if len(x) else np.nan

    def px_at(r, D, hhmm):
        t = D + pd.Timedelta(hours=int(hhmm[:2]), minutes=int(hhmm[2:]))
        if t in r.index:
            return float(r.loc[t, "Open"])
        if t > r.index[-1]:
            return float(r.Close.iloc[-1])                     # market closed: last price
        return float(r.Close[r.index < t].iloc[-1])

    def open930(r, D):
        t = D + pd.Timedelta(hours=9, minutes=30)
        if t in r.index:
            return float(r.loc[t, "Open"])
        x = r.loc[r.index < t]
        return float(x.Close.iloc[-1]) if len(x) and r.index[-1] >= t else np.nan

    def vwap(r, D, hhmm):
        t = D + pd.Timedelta(hours=int(hhmm[:2]), minutes=int(hhmm[2:]))
        x = r.loc[(r.index >= D + pd.Timedelta(hours=9, minutes=30)) & (r.index < t)]
        if not len(x):
            return np.nan
        g = x.groupby(x.index.floor("5min")).agg(H=("High", "max"), L=("Low", "min"), C=("Close", "last"),
                                                 V=("Volume", "sum"))
        return float(((g.H + g.L + g.C) / 3 * g.V).sum() / g.V.sum())

    sessions = info.index
    rows = []
    for _, t in pick.iterrows():
        D = pd.Timestamp(t.session)
        r = sess_rows(D)
        i = sessions.get_loc(D)
        prevD = sessions[i - 1]
        rp = sess_rows(prevD)
        if info.inst.iloc[i - 1] == info.inst.iloc[i]:
            x = rp.loc[rp.index < prevD + pd.Timedelta(hours=16)]
            cprev = float(x.Close.iloc[-1])
        else:
            cprev = np.nan
        O = open930(r, D)
        # previous 14 full sessions with a complete set of decision closes
        full = []
        k = i - 1
        while len(full) < 14 and k >= 0:
            Dk = sessions[k]
            if not info.early.iloc[k]:
                rk = sess_rows(Dk)
                Ok = open930(rk, Dk)
                mv = [abs(C_at(rk, Dk, h) / Ok - 1) for h in DEC]
                if np.isfinite(Ok) and np.all(np.isfinite(mv)):
                    full.append(mv)
            k -= 1
        sig = np.mean(np.array(full), axis=0)
        early = bool(info.early.iloc[i])
        dec = [h for h in DEC if (not early or h <= "1230")]
        ke, kx = t.entry, t.exit
        e_px = px_at(r, D, ke)
        x_px = px_at(r, D, kx)
        ok_cond = True
        notes = []
        for h in [h for h in dec if ke <= h <= kx]:
            j = DEC.index(h)
            c = C_at(r, D, h)
            ub = max(O, cprev) * (1 + sig[j]); lb = min(O, cprev) * (1 - sig[j]); vw = vwap(r, D, h)
            if h == ke:
                cond = (c > ub) if t.d > 0 else (c < lb)
                notes.append(f"enter {h}: C={c:.2f} UB={ub:.2f} LB={lb:.2f} {'ok' if cond else 'FAIL'}")
            elif h == kx:
                cond = (c < max(ub, vw)) if t.d > 0 else (c > min(lb, vw))
                notes.append(f"exit {h}: C={c:.2f} trail={'%.2f' % (max(ub, vw) if t.d > 0 else min(lb, vw))} "
                             f"{'ok' if cond else 'FAIL'}")
            else:
                cond = (c >= max(ub, vw)) if t.d > 0 else (c <= min(lb, vw))
                if not cond:
                    notes.append(f"hold {h} FAIL C={c:.2f}")
            ok_cond &= bool(cond)
        rows.append(dict(session=D.date(), d=int(t.d), entry=ke, exit=kx, entry_px_v3=t.entry_px, entry_px_raw=e_px,
                         exit_px_v3=t.exit_px, exit_px_raw=x_px,
                         pnl_v3=t.pnl_usd, pnl_raw=t.d * (x_px - e_px) * 2.0 - 2.0,
                         px_match=bool(abs(e_px - t.entry_px) < 1e-9 and abs(x_px - t.exit_px) < 1e-9),
                         signal_match=ok_cond, early=early, notes=" | ".join(notes)))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "handcheck_10.csv"), index=False)
    pd.set_option("display.width", 250)
    print(out.drop(columns=["notes"]).to_string())
    for n_ in out.notes:
        print(n_)
    print("ALL PRICES MATCH:", out.px_match.all(), " ALL SIGNALS MATCH:", out.signal_match.all())


if __name__ == "__main__":
    main()
