"""Section 12, rule S2 (monthly NQ-ES beta-neutral spread momentum) + V1 (1-month) + V2 (RTY-ES). Builder X."""
import os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load
from common import *

o = load.get()
dsN = pd.read_pickle("data/daily_sessions_NQ.pkl")
dsE = pd.read_pickle("data/daily_sessions_ES.pkl")
days = o["NQ"]["days"]; N = len(days)
cash = dsN.cash_day.to_numpy() & dsE.cash_day.to_numpy()
early = dsN.early_close.to_numpy() | dsE.early_close.to_numpy()

def prep(sym):
    A = o[sym]
    Cf = pd.DataFrame(A["Close"]).ffill(axis=1).to_numpy()
    Ob = pd.DataFrame(A["Open"]).bfill(axis=1).to_numpy()
    inst = A["inst"]
    sess_inst = np.array([np.unique(r[r >= 0])[0] if (r >= 0).any() else -1 for r in inst])
    multi = np.array([len(np.unique(r[r >= 0])) > 1 for r in inst])
    return dict(Cf=Cf, Ob=Ob, inst=inst, sinst=sess_inst, multi=multi)
NQ, ES = prep("NQ"), prep("ES")
assert not NQ["multi"][cash].any() and not ES["multi"][cash].any()
close_slot = np.where(early, 209, 389)

# RTY hourly -> per-session arrays (10:00 open (or next available RTH hourly bar), 15:00 close (12:00 on early close), inst)
r = pd.read_csv("data/RTY_fut_1h.csv")
ts = pd.to_datetime(r.ts_event, utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
r["date"] = ts.dt.normalize(); r["h"] = ts.dt.hour
rth = r[(r.h >= 10) & (r.h <= 15)]
RTY = {"open10": np.full(N, np.nan), "open10_h": np.full(N, -1), "inst": np.full(N, -1, dtype=np.int64),
       "close15": np.full(N, np.nan), "close12": np.full(N, np.nan), "close_h": {}}
di = days.get_indexer(rth.date)
first = rth.assign(di=di)[di >= 0].sort_values(["di", "h"]).groupby("di").head(1)
RTY["open10"][first.di] = first.Open; RTY["open10_h"][first.di] = first.h; RTY["inst"][first.di] = first.instrument_id
for hh, key in ((15, "close15"), (12, "close12")):
    x = rth[rth.h == hh]; j = days.get_indexer(x.date); RTY[key][j[j >= 0]] = x.Close.to_numpy()[j >= 0]
RTY["closeX"] = np.where(early, RTY["close12"], RTY["close15"])
RTY["Cf"] = None

# ---------- signals from Yahoo cash indexes ----------
def yclose(name):
    s = pd.read_csv(f"data/yahoo_daily/{name}.csv", parse_dates=["Date"]).set_index("Date").Close.dropna()
    return s[~s.index.duplicated()]
SPX = yclose("SP500_index"); NDX = yclose("NASDAQ100_index"); RUT = yclose("RUSSELL2000_index")

def monthly_signal(LEAD, BASE):
    df = pd.concat([LEAD.rename("L"), BASE.rename("B")], axis=1, join="inner").dropna()
    lr = np.log(df).diff()
    # rolling OLS slope over 250 daily returns ending each day
    cov = lr.L.rolling(250, min_periods=250).cov(lr.B)
    var = lr.B.rolling(250, min_periods=250).var()
    beta = cov / var
    ym = df.index.to_period("M")
    me = df.groupby(ym).tail(1)                 # month-end closes (last trading day in data for that month)
    me_beta = beta.loc[me.index]
    M = pd.DataFrame({"date": me.index, "L": me.L.values, "B": me.B.values, "b": me_beta.values}, index=me.index.to_period("M"))
    M["R"] = np.log(M.L / M.L.shift()) - M.b.shift() * np.log(M.B / M.B.shift())
    M["S12"] = M.R.rolling(12, min_periods=12).sum()
    # live-use vol scaling (reported only): trailing 60-session sd of daily beta-hedged spread returns
    spread_d = lr.L - beta.shift() * lr.B
    vol60 = spread_d.rolling(60, min_periods=60).std() * np.sqrt(252)
    M["vol60_ann"] = vol60.loc[me.index].values
    M["scale_live"] = np.minimum(2.0, 0.08 / M.vol60_ann)
    return M

M_ndx = monthly_signal(NDX, SPX)
M_rut = monthly_signal(RUT, SPX)
# last month-end must be a complete month: drop the current (partial) month of the data end
for M in (M_ndx, M_rut):
    if M.index[-1] == pd.Period("2026-11", "M"):
        M.drop(M.index[-1], inplace=True)

# ---------- execution ----------
cash_idx = np.where(cash)[0]
cash_days = days[cash_idx]
first_cash_of_month = pd.Series(cash_idx, index=cash_days).groupby(cash_days.to_period("M")).first()

def run(M, sigcol, lead="NQ", first_hold="2010-07", last_hold="2026-10"):
    """Returns per-segment frame and per-month frame (direction from M[sigcol] at month m -> hold month m+1)."""
    segs = []
    months = pd.period_range(first_hold, last_hold, freq="M")
    mult = 2.0 if lead == "NQ" else 5.0
    cost_lead = 2.0
    for h in months:
        m = h - 1
        if m not in M.index or h not in first_cash_of_month.index or (h + 1) not in first_cash_of_month.index:
            continue
        sig = M.loc[m, sigcol]
        if not np.isfinite(sig):
            continue
        d = int(np.sign(sig)); bm = M.loc[m, "b"]
        E = first_cash_of_month[h]; X = first_cash_of_month[h + 1]
        if lead == "RTY" and not np.isfinite(RTY["open10"][E]):
            continue                                   # no RTY data at the entry session (before 2017-07-10)
        sess = cash_idx[(cash_idx >= E) & (cash_idx <= X)]
        linst = NQ["sinst"] if lead == "NQ" else RTY["inst"]
        def entry_px(i):
            if lead == "NQ":
                return NQ["Ob"][i, 30], ES["Ob"][i, 30], "10:00"
            hh = RTY["open10_h"][i]
            return RTY["open10"][i], ES["Ob"][i, (hh - 9) * 60 - 30], f"{hh:02d}:00"
        def exit_close(i):
            if lead == "NQ":
                return NQ["Cf"][i, close_slot[i]], ES["Cf"][i, close_slot[i]]
            return RTY["closeX"][i], ES["Cf"][i, close_slot[i]]
        start = E
        while start is not None:
            heldL, heldE = linst[start], ES["sinst"][start]
            Le, Ee, et = entry_px(start)
            k = bm * mult * Le / (5 * Ee)
            nL, nE = size_legs(np.array([k]))
            nL, nE = int(nL[0]), int(nE[0])
            rest = sess[sess > start]
            rolled = [s for s in rest if linst[s] != heldL or ES["sinst"][s] != heldE]
            if not rolled:                                   # normal monthly exit at X 10:00
                Lx, Ex, xt = entry_px(X); xd = X; reason = "month_end"
                nxt = None
            else:
                s_r = rolled[0]
                prev = rest[rest < s_r]
                xd = prev[-1] if len(prev) else start
                Lx, Ex = exit_close(xd); xt = "13:00" if early[xd] else "16:00"; reason = "roll"
                # reopen at first session on which both legs are in new contracts, if before X
                cand = [s for s in sess[sess >= s_r] if linst[s] != heldL and ES["sinst"][s] != heldE and s < X]
                nxt = cand[0] if cand else None
            gL = d * (Lx - Le); gE = -d * (Ex - Ee)
            gross_long = nL * mult * (Lx - Le) - nE * 5 * (Ex - Ee)
            gross = d * gross_long
            cost = nL * cost_lead + nE * 3.5
            notl = nL * mult * Le
            segs.append(dict(hold_month=str(h), date=days[start], entry_date=days[start], entry_time=et,
                             exit_date=days[xd], exit_time=xt, side="long_lead_short_ES" if d > 0 else "short_lead_long_ES",
                             d=d, signal=sig, b=bm, k=k, n_lead=nL, n_ES=nE,
                             lead_entry=Le, ES_entry=Ee, lead_exit=Lx, ES_exit=Ex,
                             lead_entry_fill=Le + d * (0.25 if lead == "NQ" else 0.1), ES_entry_fill=Ee - d * 0.25,
                             lead_exit_fill=Lx - d * (0.25 if lead == "NQ" else 0.1), ES_exit_fill=Ex + d * 0.25,
                             exit_reason=reason, lead_gross_pts=gL, ES_gross_pts=gE,
                             gross_usd=gross, gross_long_usd=gross_long, cost_usd=cost, net_usd=gross - cost,
                             gross_bp=1e4 * gross / notl, gross_long_bp=1e4 * gross_long / notl, cost_bp=1e4 * cost / notl,
                             net_bp=1e4 * (gross - cost) / notl, lead_notional_usd=notl,
                             lead_inst_entry=heldL, ES_inst_entry=heldE, lead_inst_exit=linst[xd], ES_inst_exit=ES["sinst"][xd]))
            start = nxt
    S = pd.DataFrame(segs)
    S["net_pts_lead_equiv"] = S.net_usd / (mult * S.n_lead)
    Mo = S.groupby("hold_month").agg(date=("entry_date", "first"), d=("d", "first"), signal=("signal", "first"),
                                     n_segments=("d", "size"), gross_usd=("gross_usd", "sum"), cost_usd=("cost_usd", "sum"),
                                     net_usd=("net_usd", "sum"), gross_bp=("gross_bp", "sum"), gross_long_bp=("gross_long_bp", "sum"),
                                     cost_bp=("cost_bp", "sum"), net_bp=("net_bp", "sum")).reset_index()
    return S, Mo

out = {}
for nm, M, col, lead, fh in (("S2", M_ndx, "S12", "NQ", "2010-07"), ("S2-V1", M_ndx, "R", "NQ", "2010-07"),
                             ("S2-V2", M_rut, "S12", "RTY", "2017-07")):
    S, Mo = run(M, col, lead, fh)
    S.to_csv(os.path.join(HERE, f"trades_{nm}_segments.csv"), index=False)
    Mo.to_csv(os.path.join(HERE, f"trades_{nm}.csv"), index=False)
    out[nm] = (S, Mo)
    print(nm, len(Mo), "months", len(S), "segments", round(Mo.net_bp.mean(), 2), round(tstat(Mo.net_bp), 2), Mo.date.min().date(), Mo.date.max().date())

# index-only diagnostics (gross, cash indexes): month m+1 spread return signed by signal at m
def index_diag(M, col, start, end):
    R_next = M.R.shift(-1)          # R_{m+1} = ln(L) - b_m ln(B)
    d = np.sign(M[col])
    x = (d * R_next * 1e4)
    sel = (M.index + 1 >= pd.Period(start, "M")) & (M.index + 1 <= pd.Period(end, "M"))
    x = x[sel].dropna()
    return {"months": int(len(x)), "mean_gross_bp": float(x.mean()), "t": float(tstat(x)),
            "sign_changes": int((np.sign(M[col][sel]).diff().fillna(0) != 0).sum())}
diag = {
    "S2_1990_2009": index_diag(M_ndx, "S12", "1990-01", "2009-12"),
    "S2-V1_1990_2009": index_diag(M_ndx, "R", "1990-01", "2009-12"),
    "S2-V2_1990_2009": index_diag(M_rut, "S12", "1990-01", "2009-12"),
    "S2-V2_index_proxy_2010-07_2017-06": index_diag(M_rut, "S12", "2010-07", "2017-06"),
    "S2_index_2010-07_2026-10": index_diag(M_ndx, "S12", "2010-07", "2026-10"),
}
live = {"S2_latest_month": str(M_ndx.index[-1]), "S2_vol60_ann": float(M_ndx.vol60_ann.iloc[-1]),
        "S2_scale_live": float(M_ndx.scale_live.iloc[-1]),
        "S2_scale_live_mean_2010_2026": float(M_ndx.scale_live[M_ndx.index >= pd.Period("2010-06", "M")].mean())}
pd.to_pickle(dict(out=out, diag=diag, live=live, M_ndx=M_ndx, M_rut=M_rut), os.path.join(HERE, "s2_state.pkl"))
print(diag); print(live)
