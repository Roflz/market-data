"""No-look-ahead checks for G2 (PREREG 0.6).
1) H.lookahead_check(fn, sym, n_cuts=20, seed=0) for the A2 signal (NQ, ES, YM) and the ORB signal (NQ, ES):
   fn(S, B) returns every candidate signal; entries are given at the first 15-minute mark at/after the real
   5-minute entry time (the harness check works on marks), exit 16:45, stop_pts, side.
2) Truncation re-check of 20 random A2 trades and 20 random ORB trades cut EXACTLY at their 5-minute entry time
   (sessions table from H.truncate at the last mark <= entry; 5-minute bars kept only if closed by the entry time):
   the same signal (session, side, signal bar end, signal price, stop points) must be produced."""
import os, sys, warnings
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H, g2lib as G
warnings.simplefilter("ignore")
BO = G.fomc_blackout()


def ceil_mark(off):
    return np.minimum(np.ceil(np.asarray(off, float) / 15).astype(int), 91)


def fn_onbreak(S, B):
    c = G.onbreak_candidates(S, B[5], blackout=BO)
    return pd.DataFrame({"session": c["session"], "entry": ceil_mark(c["sig_end"]), "exit": 91, "d": c["side"].astype(int),
                         "stop_pts": c["stop_pts"].round(9)})


def orb_candidates(b):
    sess = pd.DatetimeIndex(b["session"])
    off = np.asarray((b.index - (sess - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1), np.int64)
    m = off == 930
    x = b[m]
    side = np.sign(x["C"] - x["O"]).astype(int)
    out = pd.DataFrame({"session": sess[m], "side": side.to_numpy(), "stop_px": np.where(side > 0, x["L"], x["H"])})
    return out[out.side != 0].reset_index(drop=True)


def fn_orb(S, B):
    c = orb_candidates(B[5])
    return pd.DataFrame({"session": c["session"], "entry": 63, "exit": 88, "d": c["side"], "stop_pts": c["stop_px"]})


rows = []
for sym in ("NQ", "ES", "YM"):
    r = H.lookahead_check(fn_onbreak, sym, n_cuts=20, seed=0, tfs=(5,), start="2012-01-01" if sym != "YM" else "2018-06-01")
    print(f"A2 signal {sym}: lookahead_check 20 cuts OK (entries compared {r.n_full.sum()})")
    rows.append(("A2-signal", sym, "lookahead_check n_cuts=20", bool(r.same.all())))
for sym in ("NQ", "ES"):
    r = H.lookahead_check(fn_orb, sym, n_cuts=20, seed=1, tfs=(5,))
    print(f"ORB signal {sym}: lookahead_check 20 cuts OK (entries compared {r.n_full.sum()})")
    rows.append(("ORB-signal", sym, "lookahead_check n_cuts=20", bool(r.same.all())))

# 2) targeted truncation at the exact entry time
rng = np.random.default_rng(20261109)
b5 = H.bars("NQ", 5)
tr = G.onbreak_trades("NQ")
ok = 0
for i in rng.choice(len(tr), 20, replace=False):
    t = tr.iloc[i]
    T = pd.Timestamp(t.t_entry)
    off = int((T - (t.session - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1))
    k = off // 15
    Sc, _ = H.truncate("NQ", t.session, k, tfs=(5,))
    bc = b5.loc[b5.index + pd.Timedelta(minutes=5) <= T]
    c = G.onbreak_candidates(Sc, bc, blackout=BO)
    c = c[(c.session == t.session) & (c.side == t.d)]
    same = len(c) == 1 and int(c.sig_end.iloc[0]) == int(t.sig_end) and abs(c.stop_pts.iloc[0] - t.stop_pts) < 1e-9 \
        and abs(c.P.iloc[0] - t.P) < 1e-9
    ok += same
    rows.append(("A2-trade", "NQ", f"{t.session.date()} {t.entry} d={t.d}", bool(same)))
print(f"A2 targeted truncation at the entry time: {ok}/20 reproduce the signal")
tro = G.orb_trades("NQ")
ok2 = 0
for i in rng.choice(len(tro), 20, replace=False):
    t = tro.iloc[i]
    T = pd.Timestamp(t.t_entry)
    bc = b5.loc[(b5.index + pd.Timedelta(minutes=5) <= T) & (b5.index >= T - pd.Timedelta(days=4))]
    c = orb_candidates(bc)
    c = c[c.session == t.session]
    same = len(c) == 1 and int(c.side.iloc[0]) == int(t.d) and abs(t.d * (t.entry_px - c.stop_px.iloc[0]) - t.stop_pts) < 1e-9
    ok2 += same
    rows.append(("ORB-trade", "NQ", f"{t.session.date()} {t.entry} d={t.d}", bool(same)))
print(f"ORB targeted truncation at the entry time: {ok2}/20 reproduce the signal")
out = pd.DataFrame(rows, columns=["check", "market", "case", "same"])
out.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lookahead_checks.csv"), index=False)
assert out.same.all(), out[~out.same]
print("NO-LOOK-AHEAD: all checks passed")
