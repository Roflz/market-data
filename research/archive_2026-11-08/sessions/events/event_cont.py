"""
Event continuation study: does the move in the first k minutes after a market event predict the next h minutes?
IMPULSE = log P(E+k) - log P(E);  FOLLOW = log P(min(E+k+h, stop)) - log P(E+k).
P(t) = Open of the bar opening at t; if no bar at t, Close of the last bar opened in [t-5, t-1]; else missing.
A window is skipped when it contains a contract change or a run of more than MAXGAP consecutive missing minutes.
stop = 17:00 ET, or the session's earlier halt/close: 16:15 ET while the 16:15-16:30 halt existed (until mid-2021),
13:15 ET on cash early-close days, 13:00 ET on Globex-only holiday sessions.
Run from the project dir: PYTHONPATH=./pylib python3 event_cont.py [maxgap]
"""
import sys
import numpy as np
import pandas as pd
from zoneinfo import ZoneInfo
from scipy.stats import norm

sys.path.insert(0, ".")
import calendar_days

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/sessions/events"
MAXGAP = int(sys.argv[1]) if len(sys.argv) > 1 else 5
KS, HS = (5, 15, 30), (30, 60, 120)
PRE = (15, 60)
NWLAG = 5
SPEC = {"NQ": dict(usd_pt=2.0, cost=2.00), "ES": dict(usd_pt=5.0, cost=3.50)}  # MNQ / MES
ET = ZoneInfo("America/New_York")
EPOCH = pd.Timestamp("1970-01-01", tz="UTC")
START, END = pd.Timestamp("2010-06-01"), pd.Timestamp("2026-11-08")

sess = pd.read_pickle("data/daily_sessions_NQ.pkl")
sess.index = pd.to_datetime(sess.index).normalize()
FOMC = pd.read_csv("data/fomc_dates.csv")
FOMC = FOMC[FOMC.scheduled].copy()
FOMC["date"] = pd.to_datetime(FOMC.date).dt.normalize()
CPI = calendar_days.cpi_days()


def to_min(local_naive, tz):
    """naive local timestamps (DatetimeIndex) in zone tz -> UTC minutes since epoch."""
    ts = pd.DatetimeIndex(local_naive).tz_localize(tz, nonexistent="raise", ambiguous="raise")
    return ((ts.tz_convert("UTC") - EPOCH) // pd.Timedelta(minutes=1)).astype(np.int64).to_numpy()


def weekdays():
    d = pd.date_range(START, END, freq="D")
    return d[d.day_of_week < 5]


def local_event(hhmm, tz):
    h, m = map(int, hhmm.split(":"))
    d = weekdays()
    return to_min(d + pd.Timedelta(hours=h, minutes=m), tz)


def et_event_on_sessions(hhmm, days):
    h, m = map(int, hhmm.split(":"))
    return to_min(pd.DatetimeIndex(days) + pd.Timedelta(hours=h, minutes=m), "America/New_York")


cash = sess.index[sess.cash_day]
allsess = sess.index
cpi_cash = cash[cash.isin(list(CPI))]
noncpi_cash = cash[~cash.isin(list(CPI))]
fomc_ok = FOMC[FOMC.date.isin(cash)]
fomc_min = np.concatenate([et_event_on_sessions(t, fomc_ok.date[fomc_ok.statement_time_et == t])
                           for t in fomc_ok.statement_time_et.unique()])

# name, minutes array, which sessions are allowed ("cash" or "any"), Mountain-time note filled later
EVENTS = [
    ("Globex reopen 18:00 ET", et_event_on_sessions("18:00", allsess - pd.Timedelta(days=1)), "any"),
    ("Tokyo open 09:00 JST", local_event("09:00", "Asia/Tokyo"), "any"),
    ("Tokyo lunch end 12:30 JST", local_event("12:30", "Asia/Tokyo"), "any"),
    ("Shanghai/HK open 09:30 CST/HKT", local_event("09:30", "Asia/Shanghai"), "any"),
    ("London open 08:00 UK = Xetra open 09:00 CET", local_event("08:00", "Europe/London"), "any"),
    ("US 06:00 Arizona MST (08:00 EST / 09:00 EDT)", local_event("06:00", "America/Phoenix"), "cash"),
    ("US 08:00 ET (06:00 Denver MST/MDT)", et_event_on_sessions("08:00", cash), "cash"),
    ("Treasury pit open 08:20 ET", et_event_on_sessions("08:20", cash), "cash"),
    ("US data 08:30 ET - CPI days", et_event_on_sessions("08:30", cpi_cash), "cash"),
    ("US data 08:30 ET - non-CPI weekdays", et_event_on_sessions("08:30", noncpi_cash), "cash"),
    ("US cash open 09:30 ET", et_event_on_sessions("09:30", cash), "cash"),
    ("US data 10:00 ET", et_event_on_sessions("10:00", cash), "cash"),
    ("London close 16:30 UK = Xetra close 17:30 CET", local_event("16:30", "Europe/London"), "any"),
    ("Fed statement (scheduled FOMC, 14:00 ET; 14:15/12:30 in 2010-12)", fomc_min, "cash"),
    ("US cash close 16:00 ET", et_event_on_sessions("16:00", cash), "cash"),
]
# sanity: London 08:00 and Berlin 09:00 are the same instant on every date (EU DST rules); same for the closes
assert (local_event("08:00", "Europe/London") == local_event("09:00", "Europe/Berlin")).all()
assert (local_event("16:30", "Europe/London") == local_event("17:30", "Europe/Berlin")).all()


def nw_t(y, x=None, lag=NWLAG):
    """Newey-West (Bartlett) t of the slope of y on x (or of the mean of y when x is None)."""
    y = np.asarray(y, float)
    n = len(y)
    if n < 20:
        return np.nan, np.nan
    X = np.column_stack([np.ones(n)] if x is None else [np.ones(n), np.asarray(x, float)])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    g = X * e[:, None]
    S = g.T @ g
    for L in range(1, lag + 1):
        G = g[L:].T @ g[:-L]
        S += (1 - L / (lag + 1)) * (G + G.T)
    V = XtX_inv @ S @ XtX_inv
    j = X.shape[1] - 1
    return b[j], b[j] / np.sqrt(V[j, j])


def build_grid(sym):
    d = pd.read_parquet(f"{OUT}/{sym}_1m.parquet")
    m = d.m.to_numpy()
    m0 = m.min() - 10
    n = m.max() - m0 + 200
    pos = m - m0
    has = np.zeros(n, bool); has[pos] = True
    op = np.full(n, np.nan); op[pos] = d.Open.to_numpy()
    cl = np.full(n, np.nan); cl[pos] = d.Close.to_numpy()
    last = np.where(has, np.arange(n), -10**9)
    last = np.maximum.accumulate(last)
    miss_run = np.arange(n) - last
    bad = miss_run > MAXGAP
    cumbad = np.cumsum(bad)
    inst = d.instrument_id.to_numpy()
    rflag = np.zeros(n, np.int64)
    rflag[pos[1:]] = (inst[1:] != inst[:-1])
    cumroll = np.cumsum(rflag)
    return dict(m0=m0, n=n, has=has, op=op, cl=cl, last=last, cumbad=cumbad, cumroll=cumroll)


def price(G, t):
    """vectorised P(t) for grid indices t, plus the index of the bar the price came from."""
    t = np.asarray(t)
    p = np.where(G["has"][t], G["op"][t], np.nan)
    j = G["last"][t - 1]
    stale_ok = (~G["has"][t]) & (t - j <= MAXGAP) & (j >= 0)
    p = np.where(stale_ok, G["cl"][np.clip(j, 0, None)], p)
    src = np.where(G["has"][t], t, j)
    return p, src


def window_ok(G, src_a, b):
    """no contract change and no long gap between the price source of a and minute b."""
    return (G["cumbad"][b] - G["cumbad"][src_a] == 0) & (G["cumroll"][b] - G["cumroll"][src_a] == 0)


def session_info(Emin):
    """session date ((ET + 6h).date), and stop minute (UTC epoch minutes) for each event minute."""
    et = pd.to_datetime(Emin * 60, unit="s", utc=True).tz_convert(ET)
    sd = (et + pd.Timedelta(hours=6)).tz_localize(None).normalize()
    return pd.DatetimeIndex(sd), et


def stop_minutes(G, sd):
    """per session date: 17:00 ET, or 16:15 if the 16:15-16:30 halt existed that day, 13:15 on early close,
    13:00 on Globex-only holiday sessions."""
    u = pd.DatetimeIndex(sd.unique())
    s1700 = to_min(u + pd.Timedelta(hours=17), "America/New_York")
    s1615 = to_min(u + pd.Timedelta(hours=16, minutes=15), "America/New_York")
    s1315 = to_min(u + pd.Timedelta(hours=13, minutes=15), "America/New_York")
    s1300 = to_min(u + pd.Timedelta(hours=13), "America/New_York")
    # halt present = no bars in 16:16..16:29
    halt = np.ones(len(u), bool)
    for dm in range(1, 15):
        halt &= ~G["has"][np.clip(s1615 + dm - G["m0"], 0, G["n"] - 1)]
    stop = np.where(halt, s1615, s1700)
    info = sess.reindex(u)
    stop = np.where(info.early_close.fillna(False).to_numpy(bool), s1315, stop)
    stop = np.where(info.cash_holiday.fillna(False).to_numpy(bool), s1300, stop)
    return pd.Series(stop, index=u).reindex(sd).to_numpy()


def run_market(sym, events=None):
    events = EVENTS if events is None else events
    G = build_grid(sym)
    usd_pt, cost = SPEC[sym]["usd_pt"], SPEC[sym]["cost"]
    rows, perday = [], []
    for name, Emin, req in events:
        Emin = np.unique(Emin)
        sd, et = session_info(Emin)
        keep = sd.isin(sess.index[sess.cash_day]) if req == "cash" else sd.isin(sess.index)
        Emin, sd, et = Emin[keep], sd[keep], et[keep]
        stop = stop_minutes(G, sd)
        t_E = Emin - G["m0"]
        inr = (t_E > 10) & (t_E < G["n"] - 400)
        Emin, sd, et, stop, t_E = Emin[inr], sd[inr], et[inr], stop[inr], t_E[inr]
        if name.startswith("Globex reopen"):
            # use the first bar in [18:00, 18:00+MAXGAP) as the reopen price
            t_first = t_E.copy()
            for dm in range(MAXGAP - 1, -1, -1):
                hit = G["has"][t_E + dm]
                t_first = np.where(hit, t_E + dm, t_first)
            pE = np.where(G["has"][t_first], G["op"][t_first], np.nan)
            srcE = t_first
        else:
            pE, srcE = price(G, t_E)
        stop_t = stop - G["m0"]
        ettimes = pd.Series(et.strftime("%H:%M")).value_counts()
        dentimes = pd.Series(et.tz_convert("America/Denver").strftime("%H:%M")).value_counts()
        phxtimes = pd.Series(et.tz_convert("America/Phoenix").strftime("%H:%M")).value_counts()
        # baseline: same-length window one hour earlier, for the "how wild is it" ratio
        pB0, srcB0 = price(G, t_E - 60)
        for k in KS:
            pB1, _ = price(G, t_E - 60 + k)
            okB = np.isfinite(pB0) & np.isfinite(pB1) & window_ok(G, srcB0, t_E - 60 + k)
            pK, srcK = price(G, t_E + k)
            okI = np.isfinite(pE) & np.isfinite(pK) & window_ok(G, srcE, t_E + k) & (t_E + k < stop_t)
            imp = np.log(pK) - np.log(pE)
            for h in HS:
                tend = np.minimum(t_E + k + h, stop_t)
                pX, _ = price(G, tend)
                ok = okI & np.isfinite(pX) & window_ok(G, srcE, tend) & (tend > t_E + k)
                fol = np.log(pX) - np.log(pK)
                x, y = imp[ok], fol[ok]
                yrs = et.year[ok]
                n = int(ok.sum())
                b, t = nw_t(y, x)
                e1, l1 = yrs <= 2017, yrs >= 2018
                b1, t1 = nw_t(y[e1], x[e1])
                b2, t2 = nw_t(y[l1], x[l1])
                # winsorised impulse (1/99 pct) as an outlier check
                lo, hi = np.nanpercentile(x, [1, 99]) if n else (np.nan, np.nan)
                bw, tw = nw_t(y, np.clip(x, lo, hi))
                sgn = np.sign(x)
                pts = (pX[ok] - pK[ok])
                traded = sgn != 0
                gross_follow = sgn * pts * usd_pt
                net_follow = gross_follow[traded] - cost
                net_fade = -gross_follow[traded] - cost
                _, t_follow = nw_t(gross_follow[traded])
                trunc = float(np.mean(tend[ok] < t_E[ok] + k + h)) if n else np.nan
                mi = okI & okB
                ratio = np.nan if name.startswith("Globex reopen") else np.mean(np.abs(np.log(pK[mi]) - np.log(pE[mi]))) / np.mean(np.abs(np.log(pB1[mi]) - np.log(pB0[mi]))) if mi.sum() else np.nan
                recent = okI & (et.year >= 2024)
                abs_pts_recent = float(np.mean(np.abs(pK[recent] - pE[recent]))) if recent.sum() else np.nan
                rows.append(dict(
                    event=name, market=sym, k=k, h=h, n_days=n,
                    n_2010_2017=int(e1.sum()), n_2018_2026=int(l1.sum()),
                    first=str(sd[ok].min().date()) if n else "", last=str(sd[ok].max().date()) if n else "",
                    slope=b, t_nw=t, slope_2010_2017=b1, t_2010_2017=t1, slope_2018_2026=b2, t_2018_2026=t2,
                    slope_wins=bw, t_nw_wins=tw,
                    corr=float(np.corrcoef(x, y)[0, 1]) if n > 2 else np.nan,
                    hit_rate_follow=float(np.mean(np.sign(y[traded]) == sgn[traded])) if n else np.nan,
                    follow_gross_usd=float(gross_follow[traded].mean()) if n else np.nan,
                    follow_net_usd=float(net_follow.mean()) if n else np.nan,
                    fade_net_usd=float(net_fade.mean()) if n else np.nan,
                    t_follow_gross_nw=t_follow,
                    follow_net_usd_2010_2017=float(net_follow[e1[traded]].mean()) if e1.sum() else np.nan,
                    follow_net_usd_2018_2026=float(net_follow[l1[traded]].mean()) if l1.sum() else np.nan,
                    frac_follow_truncated=trunc,
                    abs_impulse_ratio_vs_hour_before=ratio, abs_impulse_pts_2024_26=abs_pts_recent,
                    et_times=";".join(f"{a}({c})" for a, c in ettimes.items()),
                    denver_times=";".join(f"{a}({c})" for a, c in dentimes.items()),
                    arizona_times=";".join(f"{a}({c})" for a, c in phxtimes.items()),
                ))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    res = pd.concat([run_market(s) for s in ("NQ", "ES")], ignore_index=True)
    res.to_csv(f"{OUT}/event_continuation_all_gap{MAXGAP}.csv", index=False)
    print(len(res), "rows")
