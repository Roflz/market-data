"""v3/exp_evalmath/luck2.py - 'structured luck' bar on REAL pre-holdout trades: v2 luck-pool trades (NOT demeaned:
real costs, real drift), side random or always long, sized by $ risk or fixed micros, up to n trades a day in time
order, a trade only if its stop fits in the $600 daily room, optional stop for the day once green. Accounts start on
random sessions of the window and run on the following real sessions (to 2025-06-30). Light (small parquet files)."""
import os
import numpy as np
import pandas as pd
from evalmath import sim, metrics, DLL, V2OUT
H, P = 60, 8000
rng = np.random.default_rng(7)
rows = []
for mkt in ("ES", "NQ", "YM"):
    for tf in (15, 60):
        d = pd.read_parquet(os.path.join(V2OUT, f"luck_pool_{mkt}_{tf}.parquet"),
                            columns=["session", "t_entry", "d", "pnl_old", "pnl_hold", "risk_usd"])
        d = d[d.session >= "2013-01-01"].sort_values(["session", "t_entry", "d"])
        assert d.session.max() <= pd.Timestamp("2025-06-30")
        sess = np.sort(d.session.unique())
        si = np.searchsorted(sess, d.session.to_numpy())
        S_ = len(sess)
        slot = d.groupby([si, d.d.to_numpy()]).cumcount().to_numpy()      # bar order within the session, per side
        side = (d.d.to_numpy() > 0).astype(int)
        for ex in ("pnl_old", "pnl_hold"):
            M = np.full((S_, 8, 2), np.nan)
            RK = np.full((S_, 8, 2), np.nan)
            ok = slot < 8
            M[si[ok], slot[ok], side[ok]] = d[ex].to_numpy()[ok]
            RK[si[ok], slot[ok], side[ok]] = d.risk_usd.to_numpy()[ok]
            for win, lo in (("2013+", "2013-01-01"), ("2018+", "2018-01-01"), ("2022+", "2022-01-01")):
                s0 = np.searchsorted(sess, np.datetime64(lo))
                starts = rng.integers(s0, S_ - H, P)
                idx = starts[:, None] + np.arange(H)[None, :]
                for mode in ("random", "long"):
                    sd_ = rng.integers(0, 2, (P, H, 8)) if mode == "random" else np.ones((P, H, 8), int)
                    Mi = np.take_along_axis(M[idx], sd_[..., None], 3)[..., 0]
                    Ri = np.take_along_axis(RK[idx], sd_[..., None], 3)[..., 0]
                    for n in (2, 3):
                        pick = np.sort(np.argsort(rng.random((P, H, 8)), axis=2)[:, :, :n], axis=2)
                        T = np.take_along_axis(Mi, pick, 2)
                        TR = np.take_along_axis(Ri, pick, 2)
                        valid = np.isfinite(T) & np.isfinite(TR) & (TR > 0)
                        T, TR = np.where(valid, T, 0), np.where(valid, TR, np.inf)
                        for size in (("B", 250), ("B", 400), ("k", 3), ("k", 5)):
                            for pst in ("none", "green"):
                                cum = np.zeros((P, H))
                                for j in range(n):
                                    want = np.floor(size[1] / TR[:, :, j]) if size[0] == "B" else np.where(valid[:, :, j], size[1], 0)
                                    fit = np.floor((cum + DLL) / (TR[:, :, j] + 8.0))
                                    m = np.clip(np.minimum(want, fit), 0, 20)
                                    if pst == "green":
                                        m = np.where(cum > 0, 0, m)
                                    cum = np.maximum(cum + m * T[:, :, j], -DLL)
                                for cons in (0.4, 0.5):
                                    o, dd = sim(cum, cons)
                                    rows.append(dict(market=mkt, tf=tf, exit=ex, window=win, side=mode, n=n,
                                                     size=f"{size[0]}{size[1]}", pstop=pst, cons=cons,
                                                     day_mean=cum[:, :20].mean(), **metrics(o, dd, H)))
        print(mkt, tf, "done", flush=True)
df = pd.DataFrame(rows)
df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "table_luck2.csv"), index=False)
