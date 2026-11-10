"""
Step 2 of the pre-registration: volatility forecast (HAR) for sizing and a regime filter on BASE.

Forecast: log-HAR on daily realized variance (sum of squared 5-min log returns over the full Globex session):
  log RV_d = b0 + b1 log RV_{d-1} + b2 log mean(RV_{d-5..d-1}) + b3 log mean(RV_{d-22..d-1})
refit every session on all PRIOR sessions only (expanding window, 250-session burn-in). Terciles of the forecast use
the expanding history of forecasts up to the previous session.
Variants (pre-registered):
  V1 skip sessions whose forecast is in the top tercile
  V2 trade only sessions whose forecast is in the bottom tercile
  V3 constant dollar risk: every trade risks $100 (P&L = net R x $100)
  V4 volatility targeting: risk = $100 x clip(median past forecast / today's forecast, 0.5, 2)
Usage:  PYTHONPATH=./pylib python3 vol_module.py
"""
import warnings

import numpy as np
import pandas as pd

import exits_compare as ec
import exits_engine as ee

warnings.filterwarnings("ignore")
SETUP, K0, BURN = "Overnight break + daily trend", 2.0, 250


def har_forecast(sym):
    b = pd.read_pickle(f"data/x5_{sym}.pkl")
    lr = np.log(b.Close).diff()
    same = b.sess.eq(b.sess.shift())
    rv = (lr.where(same) ** 2).groupby(b.sess).sum()
    rv = rv[rv > 0]
    x = np.log(rv)
    w = np.log(rv.rolling(5).mean())
    m = np.log(rv.rolling(22).mean())
    X = pd.concat([x, w, m], axis=1).shift(1)            # information through the previous session
    X.columns = ["d", "w", "mo"]
    y = x
    fc = pd.Series(np.nan, index=rv.index)
    A = np.column_stack([np.ones(len(X)), X.to_numpy()])
    yy = y.to_numpy()
    for i in range(BURN, len(X)):
        rows = slice(22, i)                               # fit on sessions before i only
        Ai, yi = A[rows], yy[rows]
        ok = np.isfinite(Ai).all(1) & np.isfinite(yi)
        if ok.sum() < 100 or not np.isfinite(A[i]).all():
            continue
        beta, *_ = np.linalg.lstsq(Ai[ok], yi[ok], rcond=None)
        fc.iloc[i] = np.exp(A[i] @ beta)                  # forecast of today's realized variance
    f = pd.DataFrame({"rv": rv, "fc": fc})
    f["fc_vol"] = np.sqrt(f.fc)
    hist = f.fc_vol.shift(1)
    f["q33"] = hist.expanding(BURN // 2).quantile(1 / 3)
    f["q67"] = hist.expanding(BURN // 2).quantile(2 / 3)
    f["med"] = hist.expanding(BURN // 2).median()
    f["tercile"] = np.where(f.fc_vol <= f.q33, 0, np.where(f.fc_vol <= f.q67, 1, 2))
    f.loc[f.fc_vol.isna() | f.q33.isna(), "tercile"] = -1
    valid = f.dropna(subset=["fc"])
    corr = np.corrcoef(np.log(valid.fc), np.log(valid.rv))[0, 1]
    return f, corr


def run_set(sym, keep_day=None):
    D, sp = ec.G[sym], ee.SPEC[sym]
    sigs = ec.G[("sets", sym)][SETUP]
    if keep_day is not None:
        sigs = [(i, d) for i, d in sigs if keep_day(D.sess[i])]
    t = ee.run(D, sigs, "hold", k0=K0)
    bb = t.bar.to_numpy()
    t["R"] = (t.pts - sp["comm"] / sp["usd"]) / (K0 * D.atr5[bb])
    t["usd"] = t.pts * sp["usd"] - sp["comm"]
    t["year"], t["sess"] = D.year[bb], D.sess[bb]
    return t


def summarize(t, risk=None):
    r = t.R if risk is None else t.R * risk / 100.0
    yr = r.groupby(t.year).sum()
    daily = r.groupby(t.sess).sum()
    tstat = daily.mean() / (daily.std() / np.sqrt(len(daily)))
    return dict(trades=len(t), total_R=r.sum(), R_per_trade=r.mean(), t=tstat, years_up=f"{int((yr > 0).sum())}/{len(yr)}",
                R_2026=float(yr.get(2026, 0.0)), usd_at_100_risk=100 * r.sum())


def main():
    ec.init()
    pd.set_option("display.width", 220)
    for sym in ("NQ", "ES"):
        f, corr = har_forecast(sym)
        print(f"\n######## {ee.SPEC[sym]['micro']} ########")
        print(f"HAR forecast vs realized log-variance correlation (out of sample, expanding refit): {corr:.2f}")
        terc = f.tercile.to_dict()
        base = run_set(sym)
        base["terc"] = base.sess.map(terc)
        print("BASE by today's forecast tercile (R per trade): " + ", ".join(
            f"{n}: {g.R.mean():+.3f} (n={len(g)})" for n, g in base.groupby("terc")))
        rows = {"BASE": summarize(base)}
        v1 = run_set(sym, lambda s: terc.get(s, -1) != 2)
        v2 = run_set(sym, lambda s: terc.get(s, -1) == 0)
        rows["V1 skip top tercile"] = summarize(v1)
        rows["V2 bottom tercile only"] = summarize(v2)
        rows["V3 constant $100 risk"] = summarize(base, risk=np.full(len(base), 100.0))
        fc = base.sess.map(f.fc_vol.to_dict())
        med = base.sess.map(f.med.to_dict())
        risk4 = 100 * np.clip((med / fc).fillna(1.0), 0.5, 2.0)
        rows["V4 vol-targeted risk"] = summarize(base, risk=risk4.to_numpy())
        res = pd.DataFrame(rows).T
        print(res.round(3).to_string())
        yrs = pd.DataFrame({"BASE": base.groupby("year").R.sum(), "V1": v1.groupby("year").R.sum(),
                            "V2": v2.groupby("year").R.sum(),
                            "V4": (base.R * risk4 / 100).groupby(base.year).sum()}).round(1)
        print("Net R by year:\n" + yrs.T.to_string())
        res.to_csv(f"vol_module_{sym}.csv")


if __name__ == "__main__":
    main()
