"""HEAVY (raw 1-minute data; run under the shared flock). Hand-check 10 A2 trades (MNQ) and 2 ORB trades against the
RAW research_lib.bars_1m rows: overnight range, first 5-minute close beyond it (signal bar end), entry price, stop walk
on 5-minute clock buckets of the raw minutes, 16:45 / 16:00 exit, net $ per micro. The trend sign is recomputed with
an independent plain loop over the sessions table."""
import os, sys, warnings
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H, g2lib as G
import research_lib as rl
from handcheck_harness import raw_session, px_at
warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
tick, usd, cost = 0.25, 2.0, 2.0

tr = G.onbreak_trades("NQ")
rng = np.random.default_rng(7)
pick = list(rng.choice(np.flatnonzero(tr.exit_kind == "stop"), 5, replace=False)) + \
       list(rng.choice(np.flatnonzero(tr.exit_kind != "stop"), 5, replace=False))
S = H.sessions("NQ")
# independent trend recompute (plain loop)
I, ema, Iv, Ev = 1.0, None, {}, {}
for s, rc, ro in zip(S.index, S.ret_cc, S.ret_oc):
    Iv[s], Ev[s] = I, ema                      # values through the PREVIOUS session (known at this session's open)
    r = rc if rc == rc else (ro if ro == ro else 0.0)
    I = I * (1 + r)
    ema = I if ema is None else ema + (2 / 21) * (I - ema)
m = rl.bars_1m("NQ")
rows = []
for i in pick:
    t = tr.iloc[i]
    D = pd.Timestamp(t.session)
    r, body = raw_session(m, D)
    on = body[(body.index < D + pd.Timedelta(hours=9, minutes=30))]
    onh, onl = on.High.max(), on.Low.min()
    rth = body[(body.index >= D + pd.Timedelta(hours=9, minutes=30))]
    bk = rth.groupby(rth.index.floor("5min")).agg(O=("Open", "first"), Hh=("High", "max"), L=("Low", "min"), C=("Close", "last"))
    brk = bk[(bk.C > onh)] if t.d > 0 else bk[(bk.C < onl)]
    sig_start = brk.index[0]
    sig_end_off = int((sig_start + pd.Timedelta(minutes=5) - (D - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1))
    P = brk.C.iloc[0]
    Cp = S.loc[D, "prev_close_1600"] if S.loc[D, "prev_close_1600"] == S.loc[D, "prev_close_1600"] else S.loc[D, "prev_last_px"]
    trend = np.sign(Iv[D] * P / Cp - Ev[D])
    te = sig_start + pd.Timedelta(minutes=5)
    e = px_at(r, body, te, False)
    st = e - t.d * t.stop_pts
    w = body[(body.index >= te) & (body.index < D + pd.Timedelta(hours=16, minutes=45))]
    x, kind = px_at(r, body, D + pd.Timedelta(hours=16, minutes=45), True), "time"
    last_off = (body.index[-1] - (D - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1)
    if 1365 > last_off + 15:
        kind = "close"
    for _, g in w.groupby(w.index.floor("5min")):
        o, hi, lo = g.Open.iloc[0], g.High.max(), g.Low.min()
        if (t.d > 0 and lo <= st) or (t.d < 0 and hi >= st):
            x = min(o, st) - tick if t.d > 0 else max(o, st) + tick
            kind = "stop"
            break
    pnl = t.d * (x - e) * usd - cost
    rows.append(dict(session=D.date(), d=int(t.d), h_sig_end=int(t.sig_end), hand_sig_end=sig_end_off, hand_trend=int(trend),
                     h_entry=t.entry_px, hand_entry=e, h_P=t.P, hand_P=P, h_exit=t.exit_px, hand_exit=x, h_kind=t.exit_kind,
                     hand_kind=kind, h_pnl=round(t.pnl_usd, 6), hand_pnl=round(pnl, 6),
                     match=bool(sig_end_off == t.sig_end and trend == t.d and abs(e - t.entry_px) < 1e-9
                                and abs(pnl - t.pnl_usd) < 1e-6 and kind == t.exit_kind)))
# 2 ORB trades
to = G.orb_trades("NQ")
for i in rng.choice(len(to), 2, replace=False):
    t = to.iloc[i]
    D = pd.Timestamp(t.session)
    r, body = raw_session(m, D)
    b0 = body[(body.index >= D + pd.Timedelta(hours=9, minutes=30)) & (body.index < D + pd.Timedelta(hours=9, minutes=35))]
    side = int(np.sign(b0.Close.iloc[-1] - b0.Open.iloc[0]))
    e = px_at(r, body, D + pd.Timedelta(hours=9, minutes=35), False)
    st = b0.Low.min() if side > 0 else b0.High.max()
    tx = D + pd.Timedelta(hours=16)
    x, kind = px_at(r, body, tx, False), "time"
    w = body[(body.index >= D + pd.Timedelta(hours=9, minutes=35)) & (body.index < tx)]
    for _, g in w.groupby(w.index.floor("5min")):
        o, hi, lo = g.Open.iloc[0], g.High.max(), g.Low.min()
        if (side > 0 and lo <= st) or (side < 0 and hi >= st):
            x = min(o, st) - tick if side > 0 else max(o, st) + tick
            kind = "stop"
            break
    pnl = side * (x - e) * usd - cost
    rows.append(dict(session=D.date(), d=side, h_sig_end=935, hand_sig_end=935, hand_trend=0, h_entry=t.entry_px,
                     hand_entry=e, h_P=np.nan, hand_P=np.nan, h_exit=t.exit_px, hand_exit=x, h_kind=t.exit_kind,
                     hand_kind=kind, h_pnl=round(t.pnl_usd, 6), hand_pnl=round(pnl, 6),
                     match=bool(side == t.d and abs(e - t.entry_px) < 1e-9 and abs(pnl - t.pnl_usd) < 1e-6 and kind == t.exit_kind)))
del m
out = pd.DataFrame(rows)
out.to_csv(os.path.join(HERE, "handcheck_g2.csv"), index=False)
pd.set_option("display.width", 300)
print(out.to_string())
print(f"hand-check: {out.match.sum()} / {len(out)} trades match the raw 1-minute bars")
