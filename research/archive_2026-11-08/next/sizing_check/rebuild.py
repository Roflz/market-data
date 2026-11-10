"""Independent per-trade rebuild from raw 1-min data: entry/stop/exit for every trade in chosen_models_trades.csv.
ON entry times are taken from the builder's CSV and then VERIFIED by reproducing each trade's 1-micro $ from raw bars."""
import os, sys, numpy as np, pandas as pd
W = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, W)
from load_raw import load1, load5
SZ = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/next/sizing"
TICK = 0.25
os.chdir("/run/media/roflz/Disk 2/_/market_data")
C = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
B = pd.read_csv(f"{SZ}/sized_trades_fixed_plain_100.csv", parse_dates=["date", "entry_time", "exit_time"])
assert len(B) == len(C)

def snap_stop(x, d):
    return np.floor(x / TICK + 1e-9) * TICK if d > 0 else np.ceil(x / TICK - 1e-9) * TICK

# ---------------- overnight_break ----------------
b = load5()
bi = b.index
O5, H5, L5, C5, A5 = (b[c].to_numpy() for c in ("Open", "High", "Low", "Close", "atr"))
sess5 = b.sess.to_numpy(); inst5 = b.inst.to_numpy()
last = np.r_[sess5[1:] != sess5[:-1], True]
ends = np.flatnonzero(last); day_end = ends[np.searchsorted(ends, np.arange(len(b)))]
d1 = load1()
on_rows = []
Bon = B[B.model == "overnight_break"]
for r in Bon.itertuples():
    d = 1 if r.side == "long" else -1
    e = bi.get_loc(r.entry_time); i = e - 1
    R = 2.0 * A5[i]                                  # ATR(14) of 5-min bars ending with the signal bar (closed at entry)
    R_next = 2.0 * A5[e]                             # look-ahead variant: ATR including the entry bar
    entry = O5[e] + d * TICK
    stop = snap_stop(entry - d * R, d)
    end = day_end[e]
    for t in range(e, end + 1):
        if (L5[t] <= stop) if d > 0 else (H5[t] >= stop):
            fill = (min(stop, O5[t]) if d > 0 else max(stop, O5[t])) - d * TICK; why = "stop"; break
        if t == end:
            fill = C5[t] - d * TICK; why = "close"; break
    usd = ((fill - entry) * d - 0.5) * 2.0
    # signal sanity: signal-bar close beyond the overnight (18:00-9:30) extreme, raw prices of the same session
    s = pd.Timestamp(sess5[e]); on = d1.loc[s - pd.Timedelta(hours=6): s + pd.Timedelta(hours=9, minutes=29)]
    on = on[on.instrument_id == inst5[e]]
    sig_close_raw = d1.Close.asof(bi[i] + pd.Timedelta(minutes=4))
    beyond = (sig_close_raw > on.High.max()) if d > 0 else (sig_close_raw < on.Low.min())
    on_rows.append(dict(idx=r.Index, sig_bar=bi[i], entry_px=entry, stop_px=stop, stop_pts=R, stop_pts_lookahead=R_next,
                        exit_time2=bi[t] + pd.Timedelta(minutes=5), why2=why, usd2=usd,
                        price2=sig_close_raw, beyond_on=bool(beyond), inst_same=inst5[i] == inst5[e]))
ON = pd.DataFrame(on_rows).set_index("idx")
del b

# ---------------- RTH grid for opening_range and expiry_fade ----------------
tm = d1.index.hour * 60 + d1.index.minute
m = (tm >= 570) & (tm < 960)
r1 = d1[m]
dates = r1.index.normalize()
udates, di = np.unique(dates, return_inverse=True)
slot = (tm[m] - 570).to_numpy()
nd = len(udates)
G = {}
for c in ("Open", "High", "Low", "Close"):
    a = np.full((nd, 390), np.nan); a[di, slot] = r1[c].to_numpy(); G[c] = a
ib = np.full((nd, 390), -1, np.int64); ib[di, slot] = r1.instrument_id.to_numpy()
inst0 = ib[:, 0]
foreign = (ib >= 0) & (ib != inst0[:, None])
for c in G: G[c][foreign] = np.nan
O, H, Lo, Cl = G["Open"], G["High"], G["Low"], G["Close"]
present = ~np.isnan(Cl)
lastslot = 389 - np.argmax(present[:, ::-1], axis=1)
Cff = pd.DataFrame(Cl.T).ffill().to_numpy().T
dpos = {pd.Timestamp(x): k for k, x in enumerate(udates)}
del d1, r1

orb = []
for r in B[B.model == "opening_range"].itertuples():
    i = dpos[r.date]; d = 1 if r.side == "long" else -1
    oc, cc = O[i, 0], Cff[i, 4]
    assert (cc > oc) == (d > 0)
    stop = np.nanmin(Lo[i, :5]) if d > 0 else np.nanmax(H[i, :5])
    Rsig = d * (cc + d * TICK - stop)
    fill = O[i, 5] + d * TICK
    xs_end = 389 if lastslot[i] == 389 else 209
    if d * (fill - stop) <= 0:
        xs, xf = 5, O[i, 5] - d * TICK
    else:
        xs, xf = xs_end, Cff[i, xs_end] - d * TICK
        for s in range(5, xs_end + 1):
            if (Lo[i, s] <= stop) if d > 0 else (H[i, s] >= stop):
                o = O[i, s]; ref = stop
                if s > 5 and not np.isnan(o) and ((d > 0 and o < stop) or (d < 0 and o > stop)): ref = o
                xs, xf = s, ref - d * TICK; break
    usd = (d * (xf - fill) - 0.5) * 2
    base = r.date + pd.Timedelta(minutes=570)
    orb.append(dict(idx=r.Index, entry_px=fill, stop_px=stop, stop_pts=Rsig, usd2=usd, price2=O[i, 5],
                    exit_time2=base + pd.Timedelta(minutes=xs + 1), oc=oc, cc934=cc))
ORB = pd.DataFrame(orb).set_index("idx")

# expiry: ADR20 = mean RTH range of the prior 20 FULL sessions (independent definition, today excluded)
maxgap = np.array([np.diff(np.flatnonzero(p)).max() if p.sum() > 1 else 0 for p in present])
holiday = lastslot <= 215
full = (lastslot == 389) & ~holiday & (maxgap < 6) & present[:, 0]
xslot = np.where(lastslot == 389, 389, 209)
inr = np.arange(390)[None, :] <= xslot[:, None]
rng = np.nanmax(np.where(inr, H, np.nan), axis=1) - np.nanmin(np.where(inr, Lo, np.nan), axis=1)
valid = np.flatnonzero(~holiday)
adr = {}; adr_incl = {}
fullpos = [k for k in valid if full[k]]
fp = np.array(fullpos)
for r in B[B.model == "expiry_fade"].itertuples():
    i = dpos[r.date]
    prior = fp[fp < i]
    adr[r.Index] = rng[prior[-20:]].mean() if len(prior) >= 20 else np.nan
    incl = fp[fp <= i]
    adr_incl[r.Index] = rng[incl[-20:]].mean() if len(incl) >= 20 else np.nan
EX = pd.DataFrame({"adr20_2": pd.Series(adr), "adr20_incl_today": pd.Series(adr_incl)})
EX["price2"] = [O[dpos[d], 0] for d in B.loc[EX.index, "date"]]
EX["usd2"] = [((O[dpos[d], 0] - TICK) - (Cff[dpos[d], min(389, 389 if lastslot[dpos[d]] == 389 else 209)] + TICK) - 0.5) * 2
              for d in B.loc[EX.index, "date"]]

X = B.join(pd.concat([ON, ORB, EX]), rsuffix="_ind")
X["stop_ind"] = X.stop_pts_ind
X["usd_csv"] = C.usd.to_numpy()        # same order? verify below
X.to_pickle(f"{W}/rebuild.pkl")
# p26 independent: mean 2026 session close (17:00 Globex close, raw) on cash days
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
print("p26 from daily_sessions close_raw (cash days 2026):", ds.close_raw[(ds.index.year == 2026) & ds.cash_day].mean())
print("p26 from my RTH 15:59 closes 2026:", np.nanmean([Cff[k, 389] for k in valid if pd.Timestamp(udates[k]).year == 2026 and full[k]]))
