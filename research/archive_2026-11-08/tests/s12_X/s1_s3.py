"""Section 12, rules S1 (calm-day residual fade), S3 (big-day close-flow continuation) and variants. Builder X.
Vectorized: days x 390-minute arrays (9:30..15:59 bars, index m = minutes after 9:30)."""
import json, os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load
from common import *
import calendar_days as cd

o = load.get()
dsN = pd.read_pickle("data/daily_sessions_NQ.pkl")
dsE = pd.read_pickle("data/daily_sessions_ES.pkl")
days = o["NQ"]["days"]
assert (days == o["ES"]["days"]).all() and (dsN.index == days).all() and (dsE.index == days).all()
N = len(days)

# ---------- arrays ----------
def prep(sym):
    A = o[sym]
    O = A["Open"]; C = A["Close"]; inst = A["inst"]
    Cf = pd.DataFrame(C).ffill(axis=1).to_numpy()            # last traded close up to minute m
    Ob = pd.DataFrame(O).bfill(axis=1).to_numpy()            # next available open from minute m on
    ex = ~np.isnan(C)
    return dict(O=O, C=C, Cf=Cf, Ob=Ob, ex=ex, inst=inst)

NQ, ES = prep("NQ"), prep("ES")
cash = dsN.cash_day.to_numpy() & dsE.cash_day.to_numpy()
early = dsN.early_close.to_numpy() | dsE.early_close.to_numpy()
full = cash & ~early

# prior close: previous cash session's 15:59 close (12:59 if early close), its instrument
prev_idx = np.full(N, -1)
last = -1
for i in range(N):
    prev_idx[i] = last
    if cash[i]:
        last = i
def prior_close(L, ds):
    pc = np.full(N, np.nan); pinst = np.full(N, -2)
    j = prev_idx
    ok = j >= 0
    slot = np.where(ds.early_close.to_numpy()[j], 209, 389)
    pc[ok] = L["C"][j[ok], slot[ok]]
    pinst[ok] = L["inst"][j[ok], slot[ok]]
    return pc, pinst
NQ["pc"], NQ["pinst"] = prior_close(NQ, dsN)
ES["pc"], ES["pinst"] = prior_close(ES, dsE)
same_contract = (NQ["inst"][:, 0] == NQ["pinst"]) & (ES["inst"][:, 0] == ES["pinst"])
one_inst_day = np.array([len(set(NQ["inst"][i][NQ["inst"][i] >= 0])) == 1 and len(set(ES["inst"][i][ES["inst"][i] >= 0])) == 1
                         for i in range(N)])

def maxgap(ex):
    out = np.zeros(N, int)
    for i in range(N):
        t = np.where(ex[i])[0]
        if len(t) == 0:
            out[i] = 999; continue
        out[i] = max(np.diff(t).max() if len(t) > 1 else 0, t[0] + 1, 390 - t[-1])
    return out
gap_ok = (maxgap(NQ["ex"]) <= 10) & (maxgap(ES["ex"]) <= 10)
bars_ok = NQ["ex"][:, [0, 299, 389]].all(1) & ES["ex"][:, [0, 299, 389]].all(1)
bars_ok_v1 = bars_ok & ES["ex"][:, 359] & NQ["ex"][:, 359]

fomc = cd.fomc_days(); cpi = cd.cpi_days()
is_fomc = days.isin(list(fomc)); is_cpi = days.isin(list(cpi))
expiry = cd.expiry_fridays(days[cash])
is_exp = days.isin(list(expiry))

# ---------- hedge beta: 5-min log returns on 9:30-16:00 grid, prior 60 full cash sessions ----------
F = np.where(full & one_inst_day & NQ["ex"][:, 0] & ES["ex"][:, 0])[0]      # pool of full cash sessions
def grid_ret(L, rows):
    P = L["Cf"][rows][:, 4::5]                     # P(9:35)..P(16:00) = close of bars 9:34, ..., 15:59
    P0 = L["O"][rows, 0][:, None]
    lp = np.log(np.concatenate([P0, P], 1))
    return np.diff(lp, axis=1)                    # 78 returns
y = grid_ret(NQ, F); x = grid_ret(ES, F)
assert y.shape[1] == 78
Sx, Sy, Sxx, Sxy = x.sum(1), y.sum(1), (x * x).sum(1), (x * y).sum(1)
def roll60(a):
    c = np.concatenate([[0.0], np.cumsum(a)])
    r = np.full(len(a), np.nan)
    r[60:] = c[60:len(a)] - c[0:len(a) - 60]
    return r                                     # r[p] = sum of a[p-60..p-1]
n5 = 78 * 60
RSx, RSy, RSxx, RSxy = roll60(Sx), roll60(Sy), roll60(Sxx), roll60(Sxy)
bF = (n5 * RSxy - RSx * RSy) / (n5 * RSxx - RSx ** 2)
b = np.full(N, np.nan); b[F] = bF                   # defined only on pool days with 60 prior pool days
posF = np.full(N, -1); posF[F] = np.arange(len(F))

# ---------- residuals ----------
def resid(L1, L2, m_close):
    return np.log(L1["Cf"][:, m_close] / L1["O"][:, 0]) - b * np.log(L2["Cf"][:, m_close] / L2["O"][:, 0])
e1430 = resid(NQ, ES, 299)       # P(14:30) = close of 14:29 bar
e1530 = resid(NQ, ES, 359)
def prior60_std(e):
    """std (ddof=1) of e over the prior 60 pool days, each with its own b; NaN unless all 60 defined."""
    eF = e[F]
    out = np.full(N, np.nan)
    s = pd.Series(eF).rolling(60, min_periods=60).std(ddof=1).shift(1).to_numpy()
    out[F] = s
    return out
s1430 = prior60_std(e1430); s1530 = prior60_std(e1530)
z1430 = e1430 / s1430; z1530 = e1530 / s1530

# eligibility (S1 conditions 1-5, (5) literal: >= 60 prior full cash sessions => b defined)
roll_ok = same_contract
elig = full & roll_ok & bars_ok & gap_ok & ~is_fomc & ~is_cpi & np.isfinite(b)
# overnight residual and its std over prior 60 eligible sessions
zo_raw = np.log(NQ["O"][:, 0] / NQ["pc"]) - b * np.log(ES["O"][:, 0] / ES["pc"])
Ei = np.where(elig)[0]
sd_zo = np.full(N, np.nan)
sd_zo[Ei] = pd.Series(zo_raw[Ei]).rolling(60, min_periods=60).std(ddof=1).shift(1).to_numpy()
zo = zo_raw / sd_zo

# F3 VIX regime
vix = pd.read_csv("data/yahoo_daily/VIX_index.csv", parse_dates=["Date"]).set_index("Date").Close.dropna()
vmed = vix.rolling(252, min_periods=252).median()
pos = vix.index.searchsorted(days, side="left") - 1          # last VIX date strictly before today
vprev = np.where(pos >= 0, vix.to_numpy()[np.maximum(pos, 0)], np.nan)
vmedprev = np.where(pos >= 0, vmed.to_numpy()[np.maximum(pos, 0)], np.nan)
vix_date = np.where(pos >= 0, vix.index.to_numpy()[np.maximum(pos, 0)], np.datetime64("NaT"))
F3 = vprev < vmedprev

es_day1430 = np.log(ES["Cf"][:, 299] / ES["pc"])
es_day1530 = np.log(ES["Cf"][:, 359] / ES["pc"])
F4 = np.abs(zo) < 2
computable = elig & np.isfinite(z1430) & np.isfinite(zo)
computable_v1 = elig & bars_ok_v1 & np.isfinite(z1530) & np.isfinite(zo)

# ---------- generic two-leg simulation ----------
def simulate(rows, dir_nq, m_entry, m_size, stop=None, m_exit_close=389, name=""):
    """rows: day indices; dir_nq: +1 long NQ/short ES, -1 short NQ/long ES. Entry at open of bar m_entry,
    sizing on P = close of bar m_size. stop = (z_entry, s, ) -> disaster stop on closes m_entry..388.
    Exit: close of m_exit_close or next-bar open after stop."""
    rows = np.asarray(rows, int); d = np.asarray(dir_nq, int)
    bb = b[rows]
    Pn = NQ["Cf"][rows, m_size]; Pe = ES["Cf"][rows, m_size]
    k = bb * (2 * Pn) / (5 * Pe)
    nN, nE = size_legs(k)
    En = NQ["Ob"][rows, m_entry]; Ee = ES["Ob"][rows, m_entry]
    exit_m = np.full(len(rows), m_exit_close); reason = np.array(["close"] * len(rows), dtype=object)
    Xn = NQ["Cf"][rows, m_exit_close].copy(); Xe = ES["Cf"][rows, m_exit_close].copy()
    if stop is not None:
        z0, s = stop
        ms = np.arange(m_entry, 389)                                       # closes 14:30..15:58 (or 15:30..15:58)
        zt = (np.log(NQ["Cf"][rows][:, ms] / NQ["O"][rows, 0][:, None])
              - bb[:, None] * np.log(ES["Cf"][rows][:, ms] / ES["O"][rows, 0][:, None])) / s[:, None]
        hit = (np.sign(zt) == np.sign(z0)[:, None]) & (np.abs(zt) >= (np.abs(z0) + 2.0)[:, None])
        anyh = hit.any(1)
        first = ms[hit.argmax(1)]
        for j in np.where(anyh)[0]:
            m = first[j] + 1
            exit_m[j] = m; reason[j] = "stop"
            Xn[j] = NQ["Ob"][rows[j], m]; Xe[j] = ES["Ob"][rows[j], m]
    gN = d * (Xn - En); gE = -d * (Xe - Ee)
    gross = nN * 2 * gN + nE * 5 * gE
    cost = nN * 2.0 + nE * 3.5
    net = gross - cost
    notl = nN * 2 * En
    tmin = lambda m: [f"{(570 + int(x)) // 60:02d}:{(570 + int(x)) % 60:02d}" for x in m]
    df = pd.DataFrame({
        "date": days[rows], "entry_time": tmin(np.full(len(rows), m_entry)),
        "exit_time": [t if r == "stop" else ("16:00" if m_exit_close == 389 else tmin([m_exit_close + 1])[0])
                      for t, r in zip(tmin(exit_m), reason)],
        "exit_bar": tmin(exit_m),
        "side": np.where(d > 0, "long_NQ_short_ES", "short_NQ_long_ES"),
        "n_NQ": nN, "n_ES": nE, "k": k, "beta": bb,
        "NQ_entry": En, "ES_entry": Ee, "NQ_exit": Xn, "ES_exit": Xe,
        "NQ_entry_fill": En + d * 0.25, "ES_entry_fill": Ee - d * 0.25,
        "NQ_exit_fill": Xn - d * 0.25, "ES_exit_fill": Xe + d * 0.25,
        "exit_reason": reason,
        "NQ_gross_pts": gN, "ES_gross_pts": gE,
        "gross_usd": gross, "cost_usd": cost, "net_usd": net,
        "net_pts_NQ_equiv": net / (2 * nN),
        "gross_bp": 1e4 * gross / notl, "cost_bp": 1e4 * cost / notl, "net_bp": 1e4 * net / notl,
        "NQ_notional_usd": notl,
        "NQ_inst": NQ["inst"][rows, m_entry], "ES_inst": ES["inst"][rows, m_entry],
        "NQ_inst_exit": NQ["inst"][rows, np.minimum(exit_m, 389)], "ES_inst_exit": ES["inst"][rows, np.minimum(exit_m, 389)],
        "fomc": is_fomc[rows], "cpi": is_cpi[rows], "expiry_friday": is_exp[rows],
    })
    df["net_usd_flipdir"] = -gross - cost
    return df

# ---------- S1 primary and variants ----------
def s1_rows(z, es_day, require_f3=True, ok=None, zgate=True):
    base = ok & (np.abs(es_day) < 0.0075) & F4
    if require_f3:
        base &= F3
    if zgate:
        return base & (np.abs(z) >= 1.0)
    return base & (np.abs(z) < 1.0) & (z != 0)

res = {}
S1_cond = s1_rows(z1430, es_day1430, True, computable)              # F1-F4 met (used for S3 precedence)
specs = {
    "S1": dict(rows=S1_cond, z=z1430, s=s1430, m=300, ms=299),
    "S1-V1": dict(rows=s1_rows(z1530, es_day1530, True, computable_v1), z=z1530, s=s1530, m=360, ms=359),
    "S1-V2": dict(rows=s1_rows(z1430, es_day1430, False, computable), z=z1430, s=s1430, m=300, ms=299),
    "S1-C2": dict(rows=s1_rows(z1430, es_day1430, True, computable, zgate=False), z=z1430, s=s1430, m=300, ms=299),
}
trades = {}
for nm, sp in specs.items():
    r = np.where(sp["rows"])[0]
    zz = sp["z"][r]
    t = simulate(r, -np.sign(zz).astype(int), sp["m"], sp["ms"], stop=(zz, sp["s"][r]))
    t.insert(3, "z_entry", zz)
    t["s"] = sp["s"][r]; t["b"] = b[r]; t["zo"] = zo[r]; t["es_day_ret"] = (es_day1430 if sp["m"] == 300 else es_day1530)[r]
    t["vix_prev"] = vprev[r]; t["vix_med252"] = vmedprev[r]; t["vix_date"] = vix_date[r]
    t["es_ret_entry_to_close_bp"] = 1e4 * np.log(ES["Cf"][r, 389] / ES["O"][r, sp["m"]])
    trades[nm] = t

# ---------- S3 ----------
elig3 = full & roll_ok & NQ["ex"][:, 359] & ES["ex"][:, 359] & NQ["ex"][:, 389] & ES["ex"][:, 389] & np.isfinite(b)
RN = np.log(NQ["Cf"][:, 359] / NQ["pc"]); RE = np.log(ES["Cf"][:, 359] / ES["pc"])
prec = S1_cond.copy()          # S1 F1-F4 met at 14:30 on an S1-eligible day
g3 = {
    "S3": elig3 & ~prec & (np.abs(RN) >= 0.01) & (np.abs(RE) >= 0.01) & (np.sign(RN) == np.sign(RE)),
    "S3-V1": elig3 & ~prec & (np.abs(RN) >= 0.015) & (np.abs(RE) >= 0.015) & (np.sign(RN) == np.sign(RE)),
    "S3-V2": elig3 & ~prec & (np.abs(RN) >= 0.01) & (np.sign(RN) == np.sign(RE)) & (RE != 0),
}
vix_terc = pd.read_pickle("data/market_context.pkl").vix_tercile.reindex(days).to_numpy()
for nm, mask in g3.items():
    r = np.where(mask)[0]
    d = np.sign(RN[r]).astype(int)
    t = simulate(r, d, 360, 359)
    t["R_NQ"] = RN[r]; t["R_ES"] = RE[r]; t["b"] = b[r]; t["vix_tercile"] = vix_terc[r]
    t["NQ_outright_lasthalf_bp_dir"] = 1e4 * d * np.log(NQ["Cf"][r, 389] / NQ["O"][r, 360])
    t["ES_outright_lasthalf_bp_dir"] = 1e4 * d * np.log(ES["Cf"][r, 389] / ES["O"][r, 360])
    pl = simulate(r, d, 300, 359, m_exit_close=329)       # C2 placebo 14:30 -> 15:00, same sizes (15:30 prices)
    t["placebo_net_bp"] = pl.net_bp.to_numpy(); t["placebo_gross_bp"] = pl.gross_bp.to_numpy()
    t["placebo_net_usd"] = pl.net_usd.to_numpy()
    trades[nm] = t

# ---------- persist ----------
for nm, t in trades.items():
    t.to_csv(os.path.join(HERE, f"trades_{nm}.csv"), index=False)

pd.to_pickle(dict(trades=trades, days=days, b=b, z1430=z1430, s1430=s1430, zo=zo, F3=F3, elig=elig,
                  computable=computable, RN=RN, RE=RE, prec=prec, elig3=elig3), os.path.join(HERE, "s1s3_state.pkl"))
for nm, t in trades.items():
    print(nm, len(t), round(t.net_bp.mean(), 3), round(tstat(t.net_bp), 2), t.date.min().date() if len(t) else None)
print("pool F days", len(F), "first b day", days[np.where(np.isfinite(b))[0][0]].date(),
      "first computable", days[np.where(computable)[0][0]].date())
print("eligible", elig.sum(), "computable", computable.sum())
