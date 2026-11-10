"""Walker == H.time_trades on 50 mark-aligned trades (with stops), plus 20 without stops and 16:00 exits."""
import numpy as np, pandas as pd, warnings, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H, g2lib as G
warnings.simplefilter("ignore")
rng = np.random.default_rng(20261109)
rows = []
for sym, n in (("NQ", 50), ("ES", 15), ("YM", 10)):
    S, b, M, A, PX, last_t, _ = G.data(sym)
    pool = np.flatnonzero((S.index <= G.LAST_SESSION) & (S.index >= "2011-01-01"))
    si = rng.choice(pool, n, replace=False)
    ke = rng.integers(63, 81, n)                       # 09:45 .. 14:00 marks
    kx = np.where(rng.random(n) < 0.7, 91, 88)
    d = rng.choice([-1, 1], n)
    bi = M[si, 3 * ke]
    atr = np.where(bi >= 0, A["atr"][np.maximum(bi, 0)], np.nan)
    sp = np.round(rng.choice([1.5, 2.0, 3.0], n) * atr / H.SPEC[sym]["tick"]) * H.SPEC[sym]["tick"]
    sp[rng.random(n) < 0.2] = np.nan
    ent = pd.DataFrame({"session": S.index[si], "entry": ke, "exit": kx, "d": d, "stop_pts": sp})
    h = H.time_trades(sym, ent)
    w = G.walk(sym, si, 3 * ke, kx, d, sp)
    f = G.to_frame(sym, si, 3 * ke, kx, d, sp, w)[w["ok"]].reset_index(drop=True)
    assert len(f) == len(h), (len(f), len(h))
    for c in ("entry_px", "exit_px", "pnl_usd"):
        eq = np.allclose(f[c].to_numpy(), h[c].to_numpy(), equal_nan=True, atol=1e-9)
        rows.append((sym, c, eq))
    rows.append((sym, "exit_kind", bool((f.exit_kind.to_numpy() == h.exit_kind.to_numpy()).all())))
    rows.append((sym, "t_exit", bool((pd.DatetimeIndex(f.t_exit) == pd.DatetimeIndex(h.t_exit)).all())))
    print(sym, len(f), "trades;", "stops", (h.exit_kind == "stop").sum(), "close", (h.exit_kind == "close").sum())
r = pd.DataFrame(rows, columns=["market", "field", "identical"])
print(r.to_string())
assert r.identical.all(), "walker != time_trades"
print("CONSISTENCY OK: walker == H.time_trades on all mark-aligned test trades")
