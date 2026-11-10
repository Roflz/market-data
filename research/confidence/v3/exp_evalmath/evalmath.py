"""
v3/exp_evalmath/evalmath.py - EVAL MATH: what a daily P&L stream must look like to pass LucidFlex 25K fast and often.
SYNTHETIC P&L only (no market data, light compute) + one realistic check that resamples the v2 luck pools (random
no-edge trades already costed, per micro) with an injected edge.

Rules (prop_sim.Rules defaults): start 25,000, target +1,250, $1,000 trailing the highest END-OF-DAY balance, locks
at +100 once a close exceeds +1,100, consistency 40% / 50% (best day <= c x profit to pass), $600 daily loss limit
(day P&L floored at -600, the soft limit prop_sim/eval_sim use). Each synthetic account = its own independent path of
H trading days (no overlapping starts). sim() reproduces prop_sim.run_starts_loop exactly (checked in check()).
Option intraday=True: the account also fails if the running REALIZED P&L inside a day touches the threshold
(Lucid's EOD drawdown is updated at the close but - at most firms - enforced in real time).

Sections (tables -> v3/exp_evalmath/*.csv, summary -> v3/out/evalmath_summary.txt):
  A  Gaussian daily P&L grid: daily Sharpe S x daily sd -> pass odds; best sd per S; luck bar comparison
  B  skew at trade level (win rate / payoff at the same mean & sd), with and without a daily profit stop,
     EOD vs intraday drawdown check; plus daily-level skew
  C  autocorrelation / regimes / sparse (event-day) edges
  D  combining K uncorrelated (or rho-correlated) weak streams
  E  sizing rules for one edge (trade level, vol clustering): fixed micros, fixed $ risk, vol targeting, cushion
     scaling, target-remaining, daily profit stop
  F  realistic check: v2 luck-pool trades (MES / MNQ / MYM, random side, demeaned) + edge $/trade/micro
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 \
      OMP_NUM_THREADS=3 python3 v3/exp_evalmath/evalmath.py
"""
import os
import sys
import time

import numpy as np
import pandas as pd

import prop_sim as ps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT3 = os.path.join(os.path.dirname(HERE), "out")
V2OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "v2", "out")
TARGET, MLL, LOCK_AT, TRIG, DLL = 1250.0, 1000.0, 100.0, 1100.0, 600.0
P_DEF, H_DEF = 20000, 60
LUCK10 = (8.0, 11.0)                                 # luck bar: best no-edge config passes within 10 days 8-11% (c=0.4)


# ------------------------------------------------------------------------------------------------ core simulator
def sim(V, cons=0.40, low=None):
    """V (P, H): day P&L (already floored at -DLL). low (P, H): the day's lowest running realized P&L (<= 0), or
    None (EOD check only). Returns out (1 pass, -1 fail, 0 open) and days (day of the outcome, H if open)."""
    P, H = V.shape
    bal, hi, best = np.zeros(P), np.zeros(P), np.zeros(P)
    locked = np.zeros(P, bool)
    out = np.zeros(P, np.int8)
    days = np.full(P, H, np.int64)
    alive = np.ones(P, bool)
    for k in range(H):
        x = V[:, k]
        thr = np.where(locked, LOCK_AT, hi - MLL)
        f_intra = (bal + low[:, k] <= thr) if low is not None else np.zeros(P, bool)
        bal = bal + x
        best = np.maximum(best, x)
        hi = np.maximum(hi, bal)
        locked = locked | (hi > TRIG)
        fail = f_intra | (bal <= np.where(locked, LOCK_AT, hi - MLL))
        ok = (bal >= TARGET) & ~fail
        if cons is not None:
            ok &= best <= cons * bal
        nf, np_ = alive & fail, alive & ok
        out[nf], out[np_] = -1, 1
        days[nf | np_] = k + 1
        alive &= ~(fail | ok)
        if not alive.any():
            break
    return out, days


def metrics(out, days, H=None):
    H = H or int(days.max())
    r = {}
    for N in (5, 10, 20, 40, 60):
        if N <= H:
            r[f"pass{N}"] = 100 * ((out == 1) & (days <= N)).mean()
    for N in (10, 20, 60):
        if N <= H:
            r[f"bust{N}"] = 100 * ((out == -1) & (days <= N)).mean()
    done = (out != 0).sum()
    r["pass_rate"] = 100 * (out == 1).sum() / done if done else np.nan    # passes / finished (prop_sim def)
    r["open_end"] = 100 * (out == 0).mean()
    dp = days[out == 1]
    r["med_days_pass"] = float(np.median(dp)) if len(dp) else np.nan
    return r


def floor_dll(V):
    return np.maximum(V, -DLL)


def bm_days(mu, sd, Z, U):
    """Day P&L as Brownian motion inside the day (final X = mu + sd Z) with a HARD daily stop at -600: the day's low
    is the minimum of a Brownian bridge from 0 to X (exact draw: (X - sqrt(X^2 - 2 sd^2 ln U)) / 2); if it reaches
    -600 the day ends at -600. Unlike flooring the final P&L at -600 (which adds a phantom +$12/day at sd 400 and
    +$50/day at sd 600 for a zero-edge stream), this keeps a zero-edge stream at zero mean. Returns (V, low)."""
    X = mu + sd * Z
    low = (X - np.sqrt(X * X - 2 * sd * sd * np.log(U))) / 2
    hit = low <= -DLL
    return np.where(hit, -DLL, X), np.maximum(low, -DLL)


def check(rng):
    """sim() == prop_sim.run_starts_loop on independent paths (each path = its own series, start at 0)."""
    bad = 0
    for cons in (0.4, 0.5, None):
        V = floor_dll(rng.normal(30, 350, (400, 60)))
        o, d = sim(V, cons)
        for i in range(len(V)):
            o2, d2 = ps.run_starts_loop(V[i], [0], ps.Rules(consistency=cons))
            if o2[0] != o[i] or (o2[0] != 0 and d2[0] != d[i]):
                bad += 1
    return bad


# ------------------------------------------------------------------------------------------------ trade-level engine
def trade_days(R, risk, n, policy, rng, cons=0.40, H=H_DEF, pstop=None, intraday=False, vol=None, room=False):
    """Trade-level paths. R (P, H, n): each trade's result in R (net of costs) per micro, risk (P, H, n): $ risk per
    micro (stop distance). policy(state) -> micros (P,) for each trade; state has bal, hi, locked, cum (day realized),
    risk, k (day), j (trade), vol_est. Daily loss limit: no new trade once cum <= -600, the crossing trade is cut to
    -600 (soft limit). pstop: no new trade once cum >= pstop. Returns out, days, day P&L (P, H), micros used."""
    P = R.shape[0]
    bal, hi, best = np.zeros(P), np.zeros(P), np.zeros(P)
    locked = np.zeros(P, bool)
    out = np.zeros(P, np.int8)
    days = np.full(P, H, np.int64)
    alive = np.ones(P, bool)
    Vd = np.zeros((P, H))
    mic_sum, mic_n = 0.0, 0
    hist = np.zeros((P, H))                                    # per-micro day P&L history (for vol targeting)
    for k in range(H):
        cum = np.zeros(P)
        low = np.zeros(P)
        permicro = np.zeros(P)
        thr = np.where(locked, LOCK_AT, hi - MLL)
        for j in range(n):
            can = alive & (cum > -DLL)
            if pstop is not None:
                can &= cum < pstop
            st = dict(bal=bal, hi=hi, locked=locked, cum=cum, risk=risk[:, k, j], k=k, j=j, thr=thr,
                      hist=hist[:, :k])
            m = np.clip(np.floor(policy(st)), 0, 20)
            if room:                                           # never risk past the daily loss limit
                m = np.minimum(m, np.floor((cum + DLL) / risk[:, k, j] + 1e-9))
            m = np.where(can, m, 0)
            pnl = m * risk[:, k, j] * R[:, k, j]
            cum = np.maximum(cum + pnl, -DLL)
            low = np.minimum(low, cum)
            permicro += np.where(m > 0, risk[:, k, j] * R[:, k, j], 0)
            mic_sum += m[m > 0].sum()
            mic_n += (m > 0).sum()
        hist[:, k] = permicro
        x = cum
        Vd[:, k] = x
        f_intra = (bal + low <= thr) if intraday else np.zeros(P, bool)
        bal = bal + x
        best = np.maximum(best, x)
        hi = np.maximum(hi, bal)
        locked = locked | (hi > TRIG)
        fail = f_intra | (bal <= np.where(locked, LOCK_AT, hi - MLL))
        ok = (bal >= TARGET) & ~fail
        if cons is not None:
            ok &= best <= cons * bal
        nf, np_ = alive & fail, alive & ok
        out[nf], out[np_] = -1, 1
        days[nf | np_] = k + 1
        alive &= ~(fail | ok)
        if not alive.any():
            break
    return out, days, Vd, (mic_sum / mic_n if mic_n else 0.0)


def two_point(p, m, s):
    """Win W with prob p, lose L with 1-p, mean m and sd s."""
    D = s / np.sqrt(p * (1 - p))
    return m + (1 - p) * D, p * D - m                       # W, L


# ------------------------------------------------------------------------------------------------ sections
def section_A(rng, P=P_DEF, H=120):
    """Gaussian days with a hard intraday -600 stop (bm_days). EOD drawdown check, and intraday check (intra=1)."""
    rows = []
    Z = rng.standard_normal((P, H))
    U = rng.random((P, H))
    for S in (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5):
        for sd in (100, 150, 200, 250, 300, 350, 400, 500, 600, 800, 1000):
            V, low = bm_days(S * sd, sd, Z, U)
            for cons in (0.4, 0.5):
                for intra in (0, 1):
                    o, d = sim(V, cons, low if intra else None)
                    rows.append(dict(S=S, sd=sd, mean=S * sd, cons=cons, intra=intra, mean_after_dll=V.mean(),
                                     sd_after_dll=V.std(), **metrics(o, d, H)))
    return pd.DataFrame(rows)


def section_B(rng, sd_day, P=P_DEF, H=H_DEF):
    """Same per-trade mean & sd, different win rate (skew). n trades/day; daily sd ~ sd_day."""
    rows = []
    for S in (0.0, 0.1, 0.2):
        for n in (1, 2, 4):
            s = sd_day / np.sqrt(n)
            m = S * sd_day / n
            U = rng.random((P, H, n))
            for p in (0.15, 0.3, 0.5, 0.7, 0.85):
                W, L = two_point(p, m, s)
                R = np.where(U < p, W, -L)                    # $ per trade (risk = 1, micros = 1)
                one = np.ones_like(R)
                skew = ((1 - 2 * p) / np.sqrt(p * (1 - p)))
                for pstop in (None, 300, 500):
                    for intra in (False, True):
                        for cons in (0.4, 0.5):
                            o, d, Vd, _ = trade_days(R, one, n, lambda st: np.ones_like(st["bal"]), rng, cons, H,
                                                     pstop, intra)
                            rows.append(dict(S=S, n=n, win_rate=p, win=W, loss=L, trade_skew=skew,
                                             pstop=pstop or 0, intraday=intra, cons=cons,
                                             day_mean=Vd.mean(), day_sd=Vd.std(),
                                             day_skew=float(pd.Series(Vd[:, :20].ravel()).skew()),
                                             **metrics(o, d, H)))
    return pd.DataFrame(rows)


def section_B2(rng, sd_day, P=P_DEF, H=H_DEF):
    """Daily-level skew: two-point daily P&L at the same mean/sd (before the -600 floor)."""
    rows = []
    U = rng.random((P, H))
    for S in (0.0, 0.1, 0.2):
        for p in (0.15, 0.3, 0.5, 0.7, 0.85):
            W, L = two_point(p, S * sd_day, sd_day)
            V = floor_dll(np.where(U < p, W, -L))
            for cons in (0.4, 0.5):
                o, d = sim(V, cons)
                rows.append(dict(S=S, win_rate=p, win=W, loss=L, cons=cons, mean_after_dll=V.mean(),
                                 **metrics(o, d, H)))
    return pd.DataFrame(rows)


def section_C(rng, sd_day, P=P_DEF, H=H_DEF):
    rows = []
    e = rng.standard_normal((P, H))
    U = rng.random((P, H))
    for S in (0.0, 0.1, 0.2):
        for phi in (-0.3, 0.0, 0.2, 0.4, 0.6):
            z = np.zeros((P, H))
            z[:, 0] = e[:, 0]
            for k in range(1, H):
                z[:, k] = phi * z[:, k - 1] + np.sqrt(1 - phi ** 2) * e[:, k]
            V, low = bm_days(S * sd_day, sd_day, z, U)
            for cons in (0.4, 0.5):
                o, d = sim(V, cons)
                rows.append(dict(kind="AR1", S=S, param=phi, cons=cons, **metrics(o, d, H)))
        # edge regimes: the mean switches between 2S and 0 in runs (average run length `run` days), same average edge
        for run in (5, 20, 60):
            on = np.zeros((P, H), bool)
            on[:, 0] = rng.random(P) < 0.5
            flip = rng.random((P, H)) < 1.0 / run
            for k in range(1, H):
                on[:, k] = on[:, k - 1] ^ flip[:, k]
            V, low = bm_days(np.where(on, 2 * S * sd_day, 0.0), sd_day, e, U)
            for cons in (0.4, 0.5):
                o, d = sim(V, cons)
                rows.append(dict(kind="regime_on_off", S=S, param=run, cons=cons, **metrics(o, d, H)))
    # sparse edges: trade only on a share f of days (event days), per-active-day Sharpe Sa, active-day sd = sd_day
    for Sa in (0.2, 0.4, 0.8):
        for f in (1.0, 0.5, 0.25, 0.05):
            act = rng.random((P, H)) < f
            V, low = bm_days(Sa * sd_day, sd_day, e, U)
            V = np.where(act, V, 0.0)
            for cons in (0.4, 0.5):
                o, d = sim(V, cons)
                rows.append(dict(kind="sparse", S=Sa, param=f, cons=cons, **metrics(o, d, H)))
    # sparse edge + filler: the event days at sd_day, plus no-edge filler trading on the other days at sd 150 / 300
    for Sa in (0.4, 0.8):
        for fill_sd in (150, 300):
            act = rng.random((P, H)) < 0.05
            V1, _ = bm_days(Sa * sd_day, sd_day, e, U)
            V0, _ = bm_days(0.0, fill_sd, e, U)
            V = np.where(act, V1, V0)
            for cons in (0.4, 0.5):
                o, d = sim(V, cons)
                rows.append(dict(kind=f"sparse5%+filler_sd{fill_sd}", S=Sa, param=0.05, cons=cons,
                                 **metrics(o, d, H)))
    return pd.DataFrame(rows)


def section_D(rng, sd_day, P=P_DEF, H=H_DEF):
    rows = []
    Z = rng.standard_normal((P, H))
    U = rng.random((P, H))
    for s0 in (0.03, 0.05, 0.08, 0.1):
        for rho in (0.0, 0.3):
            for K in (1, 2, 4, 8, 16):
                Sc = s0 * K / np.sqrt(K + K * (K - 1) * rho)       # combined Sharpe
                # (i) each stream at a fixed size (sd_day / 2 each) -> combined sd grows; (ii) rescaled to sd_day
                for mode in ("fixed_each", "rescaled"):
                    sd = sd_day / 2 * np.sqrt(K + K * (K - 1) * rho) if mode == "fixed_each" else sd_day
                    sd = min(sd, 2000)
                    V, low = bm_days(Sc * sd, sd, Z, U)
                    for cons in (0.4, 0.5):
                        o, d = sim(V, cons)
                        rows.append(dict(s_each=s0, rho=rho, K=K, S_comb=Sc, mode=mode, sd=sd, cons=cons,
                                         **metrics(o, d, H)))
    return pd.DataFrame(rows)


def section_E(rng, P=P_DEF, H=H_DEF, n=2, ER=0.10):
    """One edge (ER = expected R per trade net, 1.5R target / 1R stop two-point), n trades/day, vol clustering:
    per-day vol multiplier v (log-AR(1), phi 0.95, sd of log 0.35 long run); stop distance (risk $/micro) = 50 x v
    (MES-like: a 10-pt stop = $50); the edge in R is the same in every regime (so $ edge scales with vol)."""
    b = 1.5
    p = (ER + 1) / (b + 1)
    U = rng.random((P, H, n))
    R = np.where(U < p, b, -1.0)
    lv = np.zeros((P, H))
    lv[:, 0] = rng.normal(0, 0.35, P)
    for k in range(1, H):
        lv[:, k] = 0.95 * lv[:, k - 1] + np.sqrt(1 - 0.95 ** 2) * rng.normal(0, 0.35, P)
    v = np.exp(lv)
    risk = np.repeat((50 * v * np.exp(rng.normal(0, 0.25, (P, H))))[:, :, None], n, 2)   # per-trade stop jitter
    rows = []

    def run(name, par, pol, pstop=None, cons=0.4, intra=False):
        o, d, Vd, mm = trade_days(R, risk, n, pol, rng, cons, H, pstop, intra, room=True)
        rows.append(dict(policy=name, param=par, pstop=pstop or 0, cons=cons, intraday=intra, micros_avg=mm,
                         day_mean=Vd.mean(), day_sd=Vd.std(), **metrics(o, d, H)))

    for cons in (0.4, 0.5):
        for k in (1, 2, 3, 4, 6, 8, 10):
            run("fixed_micros", k, lambda st, k=k: np.full_like(st["bal"], k), cons=cons)
        for B in (100, 150, 200, 250, 300, 400):
            run("fixed_risk", B, lambda st, B=B: B / st["risk"], cons=cons)
        for tgt in (150, 200, 300, 400):             # vol targeting: micros = target day sd / trailing 10-day sd
            def vt(st, tgt=tgt):
                h = st["hist"][:, -10:]
                if h.shape[1] < 3:
                    return tgt / (st["risk"] * 1.2 * np.sqrt(n))   # warm-up: stop-based estimate
                sd = h.std(1) + 1e-9
                return tgt / sd
            run("vol_target", tgt, vt, cons=cons)
        for f in (0.15, 0.25, 0.35, 0.5):            # cushion scaling: risk = f x (balance - threshold)
            run("cushion", f, lambda st, f=f: f * (st["bal"] + st["cum"] - st["thr"]) / st["risk"], cons=cons)
        for g in (3, 5, 8):                          # target-remaining: risk = (remaining to target) / g, >= $100
            run("target_remaining", g,
                lambda st, g=g: np.maximum((TARGET - st["bal"] - st["cum"]) / g, 100) / st["risk"], cons=cons)
        for B in (200, 250, 300):                    # gains -> bigger: risk B, x1.5 after balance > +500
            run("scale_up_after_500", B,
                lambda st, B=B: np.where(st["bal"] > 500, 1.5 * B, B) / st["risk"], cons=cons)
            run("scale_down_after_500", B,
                lambda st, B=B: np.where(st["bal"] > 500, 0.6 * B, B) / st["risk"], cons=cons)
        for B in (200, 300, 400):
            for pstop in (250, 400, 500):
                run("fixed_risk+profit_stop", B, lambda st, B=B: B / st["risk"], pstop=pstop, cons=cons)
    # intraday drawdown enforcement for a few
    for B in (150, 250, 400):
        run("fixed_risk", B, lambda st, B=B: B / st["risk"], intra=True)
    df = pd.DataFrame(rows)
    df["ER"], df["n"] = ER, n
    return df


def section_F(rng, P=10000, H=H_DEF):
    """v2 luck pools (60-min bars, '1.5R target, 16 bars' exit = pnl_old, already net of costs, per micro):
    random side, demeaned (so zero edge), + edge e $/trade/micro; n trades per session from that session's bars;
    k micros; consecutive real sessions from a random start in 2018-01 .. 2025-06 (vol regimes kept)."""
    rows = []
    for mkt in ("ES", "NQ", "YM"):
        f = os.path.join(V2OUT, f"luck_pool_{mkt}_60.parquet")
        d = pd.read_parquet(f, columns=["session", "t_entry", "d", "pnl_old", "risk_usd"])
        d = d[d.session >= "2018-01-01"]
        assert d.session.max() <= pd.Timestamp("2025-06-30")
        mu = d.pnl_old.mean()
        sess = np.sort(d.session.unique())
        si = np.searchsorted(sess, d.session.to_numpy())
        # matrix sessions x 16 slots (8 bars x 2 sides)
        S_ = len(sess)
        M = np.full((S_, 16), np.nan)
        RK = np.full((S_, 16), np.nan)
        slot = d.groupby(si).cumcount().to_numpy()
        ok = slot < 16
        M[si[ok], slot[ok]] = d.pnl_old.to_numpy()[ok] - mu
        RK[si[ok], slot[ok]] = d.risk_usd.to_numpy()[ok]
        sd_trade = np.nanstd(M)
        starts = rng.integers(0, S_ - H, P)
        idx = starts[:, None] + np.arange(H)[None, :]
        for n in (1, 2, 4):
            pick = np.argsort(rng.random((P, H, 16)), axis=2)[:, :, :n]
            T = np.take_along_axis(M[idx], pick, axis=2)
            TR = np.take_along_axis(RK[idx], pick, axis=2)
            T = np.nan_to_num(T)
            for e in (0, 2, 5, 10, 20):
                for k in (1, 2, 3, 5, 8, 12):
                    if k * n > 20:
                        continue
                    V = floor_dll(k * (T + e * (TR > 0)).sum(2))
                    for cons in (0.4, 0.5):
                        o, dd = sim(V, cons)
                        rows.append(dict(market=mkt, n=n, edge_usd=e, micros=k, cons=cons, sd_trade=sd_trade,
                                         day_mean=V.mean(), day_sd=V.std(), S_day=V.mean() / V.std(),
                                         **metrics(o, dd, H)))
            # fixed $ risk version (micros = floor(B / risk)), edge in $ per micro
            for e in (0, 5, 10):
                for B in (100, 200, 300, 400):
                    m = np.clip(np.floor(B / np.where(TR > 0, TR, np.inf)), 0, 20 // n)
                    V = floor_dll((m * (T + e)).sum(2))
                    for cons in (0.4, 0.5):
                        o, dd = sim(V, cons)
                        rows.append(dict(market=mkt, n=n, edge_usd=e, micros=-B, cons=cons, sd_trade=sd_trade,
                                         day_mean=V.mean(), day_sd=V.std(), S_day=V.mean() / V.std(),
                                         **metrics(o, dd, H)))
    return pd.DataFrame(rows)


def day_engine(R, B, nmax, pstop, lstop, cons, H):
    """Fast trade-level engine for section G: every trade risks exactly $B (1R stop) and pays R x B (two-point, net
    of costs); at most nmax trades a day; a trade is only taken if its full stop fits in the daily room
    (cum - B >= -600); stop for the day once cum >= pstop (None = never) or cum <= -lstop (None = never)."""
    P = R.shape[0]
    V = np.zeros((P, H))
    for j in range(nmax):
        can = (V - B >= -DLL - 1e-9)
        if pstop is not None:
            can &= V < pstop
        if lstop is not None:
            can &= V > -lstop
        V = V + np.where(can, B * R[:, :, j], 0.0)
    o, d = sim(V, cons)
    return o, d, V


def section_G(rng, P=10000, H=H_DEF):
    """Day management x edge: 1R = $B stop, target b R (win prob p = (1 + ER) / (1 + b)), up to nmax trades/day,
    daily room rule, profit stop (None / after the first win / +$500) and loss stop (None / after one loss)."""
    rows = []
    U = rng.random((P, H, 4))
    for ER in (0.0, 0.05, 0.1, 0.2):
        for b in (1.0, 1.5, 2.0, 3.0):
            p = (1 + ER) / (1 + b)
            R = np.where(U < p, b, -1.0)
            for B in (100, 150, 200, 250, 300, 400):
                for nmax in (1, 2, 3, 4):
                    for pname, pst in (("none", None), ("first_win", 0.01), ("500", 500.0)):
                        if nmax == 1 and pname != "none":
                            continue
                        for lname, lst in (("none", None), ("one_loss", 0.01)):
                            if nmax == 1 and lname != "none":
                                continue
                            V = None
                            for cons in (0.4, 0.5):
                                o, d, V = day_engine(R, B, nmax, pst, lst, cons, H)
                                v = V[:, :20]
                                rows.append(dict(ER=ER, b=b, win_rate=p, B=B, nmax=nmax, pstop=pname, lstop=lname,
                                                 cons=cons, day_mean=v.mean(), day_sd=v.std(),
                                                 day_max=v.max(), S_day=v.mean() / v.std() if v.std() else np.nan,
                                                 **metrics(o, d, H)))
    return pd.DataFrame(rows)


def section_F2(rng, P=10000, H=H_DEF):
    """v2 luck pools, done sequentially: trades of a session in time order, k micros (or $B risk), random side,
    demeaned per market (zero edge) + edge e $/micro/trade; a trade is only taken if its stop ($ risk x micros +
    $8 cost allowance) fits in the daily room; optional stop for the day after the first winning trade.
    Pool: 15-min bars, exit '1.5R target, 16 bars' (pnl_old), 2018-01 .. 2025-06-30 (pre-holdout)."""
    rows = []
    for mkt in ("ES", "NQ", "YM"):
        d = pd.read_parquet(os.path.join(V2OUT, f"luck_pool_{mkt}_15.parquet"),
                            columns=["session", "t_entry", "d", "pnl_old", "risk_usd"])
        d = d[d.session >= "2018-01-01"].sort_values(["session", "t_entry", "d"])
        assert d.session.max() <= pd.Timestamp("2025-06-30")
        mu = d.pnl_old.mean()
        sess = np.sort(d.session.unique())
        si = np.searchsorted(sess, d.session.to_numpy())
        S_ = len(sess)
        M = np.full((S_, 16), np.nan)
        RK = np.full((S_, 16), np.nan)
        slot = d.groupby(si).cumcount().to_numpy()
        ok = slot < 16
        M[si[ok], slot[ok]] = d.pnl_old.to_numpy()[ok] - mu
        RK[si[ok], slot[ok]] = d.risk_usd.to_numpy()[ok]
        starts = rng.integers(0, S_ - H, P)
        idx = starts[:, None] + np.arange(H)[None, :]
        Mi, RKi = M[idx], RK[idx]
        for n in (1, 2, 3):
            pick = np.sort(np.argsort(rng.random((P, H, 16)), axis=2)[:, :, :n], axis=2)    # time order kept
            T = np.nan_to_num(np.take_along_axis(Mi, pick, axis=2))
            TR = np.nan_to_num(np.take_along_axis(RKi, pick, axis=2))
            for e in (0, 2, 5, 10, 20):
                for size in (("k", 1), ("k", 2), ("k", 3), ("k", 5), ("k", 8), ("B", 150), ("B", 250), ("B", 400)):
                    for pst in (None, "first_win"):
                        cum = np.zeros((P, H))
                        for j in range(n):
                            r = TR[:, :, j]
                            want = np.full_like(r, size[1]) if size[0] == "k" else \
                                np.floor(size[1] / np.where(r > 0, r, np.inf))
                            fit = np.floor((cum + DLL) / (r + 8.0))
                            m = np.clip(np.minimum(want, fit), 0, 20)
                            if pst is not None:
                                m = np.where(cum > 0, 0, m)
                            cum = np.maximum(cum + m * (T[:, :, j] + e), -DLL)
                        for cons in (0.4, 0.5):
                            o, dd = sim(cum, cons)
                            v = cum[:, :20]
                            rows.append(dict(market=mkt, n=n, edge_usd=e, size=f"{size[0]}{size[1]}",
                                             pstop=pst or "none", cons=cons, day_mean=v.mean(), day_sd=v.std(),
                                             S_day=v.mean() / v.std(), **metrics(o, dd, H)))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    rng = np.random.default_rng(20261109)
    secs = sys.argv[1:] or list("ABCDEF")
    if "check" in secs:
        print("mismatches vs prop_sim.run_starts_loop:", check(rng))
        return
    SD_DAY = float(os.environ.get("SD_DAY", 300))
    for s in secs:
        t = time.time()
        df = dict(A=lambda: section_A(rng), B=lambda: section_B(rng, SD_DAY), B2=lambda: section_B2(rng, SD_DAY),
                  C=lambda: section_C(rng, SD_DAY), D=lambda: section_D(rng, SD_DAY), E=lambda: section_E(rng),
                  E05=lambda: section_E(rng, ER=0.05), E20=lambda: section_E(rng, ER=0.20),
                  F=lambda: section_F(rng), G=lambda: section_G(rng),
                  F2=lambda: section_F2(rng))[s]()
        df.to_csv(os.path.join(HERE, f"table_{s}.csv"), index=False)
        print(f"section {s}: {len(df)} rows, {time.time() - t:.1f}s", flush=True)
    print(f"total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
