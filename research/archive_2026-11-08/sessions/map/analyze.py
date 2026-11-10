"""
Volatility map of the Globex day for NQ and ES (5-minute clock slots, ET), plus event-time measurements in each
exchange's own local time (converted per date with zoneinfo), a DST natural experiment for foreign events, an 8:30 ET
release breakdown, Mountain-time (Denver and Arizona) views and a 1-minute zoom around 8:30 and 9:30 ET.
Inputs: slots5_{sym}.parquet and min1_{sym}.parquet from build.py; project calendars (read-only).
"""
import os
import sys

import numpy as np
import pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
ROOT = "/run/media/roflz/Disk 2/_/market_data"
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import calendar_days as cd  # noqa: E402

ET = "America/New_York"
ERAS = {"2010-2026": (2010, 2026), "2010-2017": (2010, 2017), "2018-2026": (2018, 2026)}
pd.set_option("display.width", 250, "display.max_columns", 40, "display.max_rows", 400)

CPI = cd.cpi_days()
FOMC = pd.read_csv("data/fomc_dates.csv")
FOMC = FOMC[FOMC.scheduled]
FOMC_T = dict(zip(pd.to_datetime(FOMC.date).dt.normalize(), FOMC.statement_time_et))


def hm_str(x):
    return f"{int(x) // 60 % 24:02d}:{int(x) % 60:02d}"


def load(sym):
    S = pd.read_parquet(f"{D}/slots5_{sym}.parquet")
    et = S.t.dt.tz_convert(ET)
    S["hm"] = (et.dt.hour * 60 + et.dt.minute).astype(int)
    S["summer"] = (et.dt.tz_localize(None) - S.t.dt.tz_localize(None)) == pd.Timedelta(hours=-4)  # US DST in force
    day = et.dt.tz_localize(None).dt.normalize()
    S["sess"] = day + pd.to_timedelta((S.hm >= 1080).astype(int), unit="D")
    sess = pd.read_pickle(f"data/daily_sessions_{sym}.pkl")
    cash = sess.index[sess.cash_day]
    S = S[S.sess.isin(cash)].copy()
    S["order"] = (S.hm - 1080) % 1440
    S["main"] = S.order < 1380                       # 18:00 .. 16:55 ET (current Globex day)
    S["abs"] = S.mv.abs()
    S["abs_pts"] = S["abs"] * S.px / 1e4
    S["yr"] = S.sess.dt.year
    # per-day normalisation: each slot's abs move / that day's mean abs move over its main slots
    dm = S[S.main].groupby("sess")["abs"].mean()
    S["abs_dn"] = S["abs"] / S.sess.map(dm)
    return S


def era(S, e):
    a, b = ERAS[e]
    return S[(S.yr >= a) & (S.yr <= b)]


def slot_table(S):
    g = S.groupby("hm")
    T = pd.DataFrame({
        "order": g.order.first(), "n_days": g.size(), "mean_abs_bp": g["abs"].mean(), "median_abs_bp": g["abs"].median(),
        "se_mean_abs_bp": g["abs"].std() / np.sqrt(g.size()), "p90_abs_bp": g["abs"].quantile(0.9),
        "mean_signed_bp": g.mv.mean(), "t_signed": g.mv.mean() / (g.mv.std() / np.sqrt(g.size())),
        "mean_abs_pts": g.abs_pts.mean(), "mean_vol": g.vol.mean(), "median_vol": g.vol.median(),
        "rel_daynorm": g.abs_dn.mean(), "ref_open_frac": g.ref_open.mean(),
    }).sort_values("order")
    main = T.order < 1380
    T["rel_to_day_avg"] = T.mean_abs_bp / T.mean_abs_bp[main].mean()
    T["vol_rel_to_day_avg"] = T.mean_vol / T.mean_vol[main].mean()
    T["day_avg_slot_bp"] = T.mean_abs_bp[main].mean()
    T["rank_in_day"] = T.mean_abs_bp.where(main).rank(ascending=False)
    return T


# ---------------------------------------------------------------- events
EVENTS = [  # name, tz, local time ('fomc' = per-day statement time), day filter, offset_days (event date = sess + off)
    ("Globex reopen 18:00 ET", ET, "18:00", None, -1),
    ("Tokyo cash open 09:00 JST", "Asia/Tokyo", "09:00", None, 0),
    ("Shanghai/Hong Kong open 09:30 CST/HKT", "Asia/Shanghai", "09:30", None, 0),
    ("Tokyo lunch end 12:30 JST", "Asia/Tokyo", "12:30", None, 0),
    ("Eurex futures open 08:00 CET (extra)", "Europe/Berlin", "08:00", None, 0),
    ("Frankfurt Xetra open 09:00 CET (= London open 08:00 UK)", "Europe/Berlin", "09:00", None, 0),
    ("London open 08:00 UK", "Europe/London", "08:00", None, 0),
    ("Treasury/CME pit-era open 08:20 ET", ET, "08:20", None, 0),
    ("US data 08:30 ET (all days)", ET, "08:30", None, 0),
    ("US data 08:30 ET (CPI days)", ET, "08:30", "cpi", 0),
    ("US data 08:30 ET (non-CPI days)", ET, "08:30", "noncpi", 0),
    ("US cash open 09:30 ET", ET, "09:30", None, 0),
    ("US 10:00 ET data", ET, "10:00", None, 0),
    ("London close 16:30 UK", "Europe/London", "16:30", None, 0),
    ("Frankfurt close 17:30 CET", "Europe/Berlin", "17:30", None, 0),
    ("US cash close 16:00 ET (16:00 slot)", ET, "16:00", None, 0),
    ("US cash close: last cash 5 min 15:55 ET", ET, "15:55", None, 0),
    ("FOMC statement (scheduled days)", ET, "fomc", "fomc", 0),
    ("FOMC days, 14:00 ET slot regardless of time", ET, "14:00", "fomc", 0),
    ("Non-FOMC days, 14:00 ET slot", ET, "14:00", "nonfomc", 0),
]


def event_instants(sessions, tz, local, filt, off):
    rows = []
    for s in sessions:
        if filt == "cpi" and s not in CPI:
            continue
        if filt == "noncpi" and s in CPI:
            continue
        if filt == "fomc" and s not in FOMC_T:
            continue
        if filt == "nonfomc" and s in FOMC_T:
            continue
        lt = FOMC_T[s] if local == "fomc" else local
        dloc = s + pd.Timedelta(days=off)
        ts = pd.Timestamp(f"{dloc:%Y-%m-%d} {lt}").tz_localize(tz)
        rows.append((s, ts.tz_convert("UTC")))
    return pd.DataFrame(rows, columns=["sess", "t"])


def event_stats(S, Sidx, T_era, name, tz, local, filt, off):
    sessions = S.sess.unique()
    E = event_instants(sorted(sessions), tz, local, filt, off)
    E = E.join(Sidx[["abs", "vol", "hm", "sess"]].rename(columns={"sess": "sess_s"}), on="t")
    E = E[E.sess == E.sess_s].dropna(subset=["abs"])
    if not len(E):
        return None, None
    pre = []
    for k in range(1, 7):  # the six slots before (-30..-5 min)
        x = Sidx["abs"].reindex(E.t - pd.Timedelta(minutes=5 * k))
        pre.append(x.to_numpy())
    pre = np.nanmean(np.vstack(pre), axis=0)
    prev1 = Sidx["abs"].reindex(E.t - pd.Timedelta(minutes=5)).to_numpy()
    nxt1 = Sidx["abs"].reindex(E.t + pd.Timedelta(minutes=5)).to_numpy()
    if name.startswith("Globex reopen"):          # the slots before the reopen are the closed hour: no comparison
        pre = np.full(len(E), np.nan)
        prev1 = np.full(len(E), np.nan)
    day_avg = T_era.day_avg_slot_bp.iloc[0]
    et_times = E.hm.map(hm_str).value_counts()
    r = dict(event=name, local_tz=tz, local_time=local, n_days=len(E),
             et_times="; ".join(f"{k} ET x{v}" for k, v in et_times.items()),
             mean_abs_bp=E["abs"].mean(), median_abs_bp=E["abs"].median(),
             se=E["abs"].std() / np.sqrt(len(E)), mean_vol=E.vol.mean(),
             rel_to_day_avg=E["abs"].mean() / day_avg,
             prev_slot_bp=np.nanmean(prev1), next_slot_bp=np.nanmean(nxt1),
             ratio_vs_prev_slot=E["abs"].mean() / np.nanmean(prev1),
             ratio_vs_prior_30min=E["abs"].mean() / np.nanmean(pre))
    # DST natural experiment: at each ET clock time X the event occupies, event days vs other days
    ctrl = []
    if len(et_times) > 1 or filt in ("cpi", "fomc"):
        for hm, n in E.hm.value_counts().items():
            if n < 15:
                continue
            evd = set(E.sess[E.hm == hm])
            at = S[S.hm == hm]
            ev = at[at.sess.isin(evd)]
            ot = at[~at.sess.isin(evd)]
            if filt == "fomc":   # control = non-FOMC days only
                ot = ot[~ot.sess.isin(FOMC_T.keys())]
            ctrl.append(dict(event=name, slot_et=hm_str(hm), n_event_days=len(ev), n_other_days=len(ot),
                             event_days_bp=ev["abs"].mean(), other_days_bp=ot["abs"].mean(),
                             ratio=ev["abs"].mean() / ot["abs"].mean(),
                             event_days_daynorm=ev.abs_dn.mean(), other_days_daynorm=ot.abs_dn.mean(),
                             ratio_daynorm=ev.abs_dn.mean() / ot.abs_dn.mean(),
                             event_vol=ev.vol.mean(), other_vol=ot.vol.mean()))
    return r, ctrl


# ---------------------------------------------------------------- 8:30 breakdown
def release_flags(sym):
    M = pd.read_parquet(f"{D}/min1_{sym}.parquet")
    et = M.t.dt.tz_convert(ET)
    M["hm"] = et.dt.hour * 60 + et.dt.minute
    M["day"] = et.dt.tz_localize(None).dt.normalize()
    M["abs"] = M.mv.abs()
    v = M.pivot_table(index="day", columns="hm", values="vol", aggfunc="sum")
    base = v.loc[:, 501:509].median(axis=1)           # 8:21-8:29 median 1-min volume
    spike = v.get(510) / base                          # 8:30 bar volume / pre-release baseline
    return M, spike


def main():
    out_slots, out_ev, out_ctrl, out_830, out_mt, out_zoom = [], [], [], [], [], []
    for sym in ("NQ", "ES"):
        S_all = load(sym)
        M, spike = release_flags(sym)
        for e in ERAS:
            S = era(S_all, e)
            T = slot_table(S)
            T.insert(0, "symbol", sym)
            T.insert(1, "era", e)
            T.insert(2, "slot_et", [hm_str(x) for x in T.index])
            T.insert(3, "slot_mountain_denver", [hm_str(x - 120) for x in T.index])
            T.insert(4, "slot_arizona_mst_when_us_dst", [hm_str(x - 180) for x in T.index])
            T["in_current_globex_day"] = T.order < 1380
            out_slots.append(T.reset_index(drop=True))
            Sidx = S.set_index("t")
            for ev in EVENTS:
                r, c = event_stats(S, Sidx, T, *ev)
                if r is None:
                    continue
                r.update(symbol=sym, era=e)
                out_ev.append(r)
                for x in c or []:
                    x.update(symbol=sym, era=e)
                    out_ctrl.append(x)
            # ---- 8:30 slot by day type
            at = S[S.hm == 510].copy()
            at["spike"] = at.sess.map(spike)
            dow = at.sess.dt.dayofweek
            first_fri = (dow == 4) & (at.sess.dt.day <= 7)
            types = {
                "CPI days": at.sess.isin(CPI),
                "First Friday (NFP proxy), non-CPI": first_fri & ~at.sess.isin(CPI),
                "Thursday (jobless claims), non-CPI": (dow == 3) & ~at.sess.isin(CPI),
                "Mon/Tue/Wed non-CPI": dow.isin([0, 1, 2]) & ~at.sess.isin(CPI),
                "Other Fridays non-CPI": (dow == 4) & ~first_fri & ~at.sess.isin(CPI),
                "Detected 8:30 release (8:30 1-min volume >= 4x 8:21-8:29 median), non-CPI":
                    (at.spike >= 4) & ~at.sess.isin(CPI),
                "No detected release (spike < 2), non-CPI": (at.spike < 2) & ~at.sess.isin(CPI),
                "All days": pd.Series(True, index=at.index),
            }
            day_avg = T.day_avg_slot_bp.iloc[0]
            for k, msk in types.items():
                x = at[msk]
                sl = S[S.sess.isin(set(x.sess))]
                prior = sl[(sl.hm >= 480) & (sl.hm < 510)]["abs"].mean()   # 8:00-8:25 same days
                out_830.append(dict(symbol=sym, era=e, day_type=k, n_days=len(x),
                                    mean_abs_830_bp=x["abs"].mean(), median_abs_830_bp=x["abs"].median(),
                                    p90_abs_830_bp=x["abs"].quantile(0.9),
                                    rel_to_day_avg=x["abs"].mean() / day_avg,
                                    same_days_800_825_bp=prior, ratio_vs_800_825=x["abs"].mean() / prior,
                                    mean_abs_pts=x.abs_pts.mean(), mean_vol=x.vol.mean(),
                                    same_days_0930_bp=sl[sl.hm == 570]["abs"].mean()))
            # ---- Mountain local-clock views (Denver: MST/MDT, always ET-2; Arizona: MST all year)
            for tzname, label in (("America/Denver", "Denver (MST/MDT)"), ("America/Phoenix", "Arizona (MST, no DST)")):
                loc = S.t.dt.tz_convert(tzname)
                lhm = loc.dt.hour * 60 + loc.dt.minute
                sel = (lhm >= 240) & (lhm < 600)
                g = S[sel].groupby([S.summer[sel], lhm[sel]])
                tab = pd.DataFrame({"n": g.size(), "mean_abs_bp": g["abs"].mean(), "rel_daynorm": g.abs_dn.mean(),
                                    "mean_vol": g.vol.mean(), "et_slot": g.hm.first()}).reset_index()
                tab.columns = ["us_dst", "local_hm", "n", "mean_abs_bp", "rel_daynorm", "mean_vol", "et_hm"]
                tab["rel_to_day_avg"] = tab.mean_abs_bp / day_avg
                tab.insert(0, "symbol", sym)
                tab.insert(1, "era", e)
                tab.insert(2, "local_zone", label)
                tab["season"] = np.where(tab.us_dst, "US summer time (Mar-Nov)", "US winter time (Nov-Mar)")
                tab["local_time"] = tab.local_hm.map(hm_str)
                tab["et_time"] = tab.et_hm.map(hm_str)
                out_mt.append(tab.drop(columns=["local_hm", "et_hm", "us_dst"]))
            # ---- 1-minute zoom (07:50-10:10 ET)
            a, b = ERAS[e]
            Me = M[(M.day.dt.year >= a) & (M.day.dt.year <= b) & M.day.isin(set(S.sess))]
            Me = Me[(Me.hm >= 470) & (Me.hm <= 610)]
            sp = Me.day.map(spike)
            cls = np.select([Me.day.isin(CPI), sp >= 4, sp < 2], ["CPI day", "detected release non-CPI", "no release"],
                            "ambiguous")
            z = Me.assign(cls=cls).groupby(["cls", "hm"]).agg(n=("abs", "size"), mean_abs_bp=("abs", "mean"),
                                                             mean_vol=("vol", "mean")).reset_index()
            z2 = Me.groupby("hm").agg(n=("abs", "size"), mean_abs_bp=("abs", "mean"), mean_vol=("vol", "mean"))
            z2 = z2.reset_index().assign(cls="all days")
            z = pd.concat([z, z2])
            z["time_et"] = z.hm.map(hm_str)
            z["time_denver"] = (z.hm - 120).map(hm_str)
            z.insert(0, "symbol", sym)
            z.insert(1, "era", e)
            out_zoom.append(z.drop(columns="hm"))
        print(sym, "done", flush=True)

    slots = pd.concat(out_slots)
    slots.drop(columns=["order"]).to_csv(f"{D}/vol_map_5min_slots.csv", index=False, float_format="%.4f")
    ev = pd.DataFrame(out_ev)
    ev = ev[["symbol", "era"] + [c for c in ev.columns if c not in ("symbol", "era")]]
    ev.to_csv(f"{D}/vol_map_events.csv", index=False, float_format="%.4f")
    ctrl = pd.DataFrame(out_ctrl)
    ctrl = ctrl[["symbol", "era"] + [c for c in ctrl.columns if c not in ("symbol", "era")]]
    ctrl.to_csv(f"{D}/vol_map_events_dst_control.csv", index=False, float_format="%.4f")
    pd.DataFrame(out_830).to_csv(f"{D}/vol_map_0830_by_daytype.csv", index=False, float_format="%.4f")
    pd.concat(out_mt).to_csv(f"{D}/vol_map_mountain_local_clock.csv", index=False, float_format="%.4f")
    pd.concat(out_zoom).to_csv(f"{D}/vol_map_1min_zoom_0750_1010.csv", index=False, float_format="%.4f")
    print("written")


if __name__ == "__main__":
    main()
