"""
DST natural experiment, two views (per-day-normalised abs 5-min moves: 1.00 = that day's average slot):
 1) event-relative profiles: mean normalised move at -30..+30 min around a foreign event, separately for each ET
    clock time the event falls on (e.g. London open at 03:00 ET most days, 04:00 ET in the 2-3 US/UK DST-mismatch weeks).
    If the spike sits at offset 0 in both groups, the event (not the US clock) drives it.
 2) clock test: for fixed ET slots, normal days vs Europe-shifted days (US on DST, Europe not) and US summer vs winter
    (Asia shifts by 1h in ET).
"""
import os
import sys

import numpy as np
import pandas as pd

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import analyze as A  # noqa: E402  (chdir to project root, read-only)

EV = [
    ("London open 08:00 UK / Xetra 09:00 CET", "Europe/London", "08:00"),
    ("Eurex/European 08:00 CET (UK data 07:00 UK)", "Europe/Berlin", "08:00"),
    ("European 10:00 CET data (Ifo, euro-area)", "Europe/Berlin", "10:00"),
    ("UK midday 12:00 UK (BoE decision time)", "Europe/London", "12:00"),
    ("London close 16:30 UK / Xetra 17:30 CET", "Europe/London", "16:30"),
    ("Tokyo open 09:00 JST", "Asia/Tokyo", "09:00"),
    ("Shanghai/HK open 09:30", "Asia/Shanghai", "09:30"),
    ("Tokyo lunch end 12:30 JST", "Asia/Tokyo", "12:30"),
    ("Tokyo close 15:00 JST", "Asia/Tokyo", "15:00"),
]
OFFS = list(range(-30, 35, 5))


def main():
    prof, clock = [], []
    for sym in ("NQ", "ES"):
        S_all = A.load(sym)
        uk_off = S_all.t.dt.tz_convert("Europe/London")
        uk_minus_et = ((uk_off.dt.tz_localize(None) - S_all.t.dt.tz_convert(A.ET).dt.tz_localize(None))
                       / pd.Timedelta(hours=1)).round().astype(int)
        S_all["eu_shift"] = uk_minus_et.ne(5)          # True in the US-DST/Europe-standard mismatch weeks
        for e in A.ERAS:
            S = A.era(S_all, e)
            Sidx = S.set_index("t")
            for name, tz, lt in EV:
                E = A.event_instants(sorted(S.sess.unique()), tz, lt, None, 0)
                E = E.join(Sidx[["hm", "sess"]], on="t", rsuffix="_s").dropna(subset=["hm"])
                E = E[E.sess == E.sess_s]
                for hm, grp in E.groupby("hm"):
                    if len(grp) < 15:
                        continue
                    row = dict(symbol=sym, era=e, event=name, event_et=A.hm_str(hm), n_days=len(grp))
                    for o in OFFS:
                        x = Sidx["abs_dn"].reindex(grp.t + pd.Timedelta(minutes=o))
                        row[f"{o:+d}"] = x.mean()
                    prof.append(row)
            # clock test
            for hm in [120, 180, 240, 270, 300, 360, 420, 480, 510, 690, 750]:
                at = S[S.hm == hm]
                a, b = at[~at.eu_shift], at[at.eu_shift]
                clock.append(dict(symbol=sym, era=e, test="normal = usual weeks, shifted = US/EU DST-mismatch weeks (European events 1h later in ET)",
                                  slot_et=A.hm_str(hm), n_normal=len(a), n_shifted=len(b),
                                  normal_daynorm=a.abs_dn.mean(), shifted_daynorm=b.abs_dn.mean(),
                                  normal_bp=a["abs"].mean(), shifted_bp=b["abs"].mean()))
            for hm in [1140, 1200, 1230, 1260, 1290, 1320, 1350, 1380, 1410, 60, 120]:
                at = S[S.hm == hm]
                a, b = at[~at.summer], at[at.summer]
                clock.append(dict(symbol=sym, era=e, test="normal = US winter (EST), shifted = US summer (EDT): Asian events 1h later in ET in summer",
                                  slot_et=A.hm_str(hm), n_normal=len(a), n_shifted=len(b),
                                  normal_daynorm=a.abs_dn.mean(), shifted_daynorm=b.abs_dn.mean(),
                                  normal_bp=a["abs"].mean(), shifted_bp=b["abs"].mean()))
        print(sym, "done", flush=True)
    P = pd.DataFrame(prof)
    P.to_csv(f"{D}/vol_map_event_profiles_daynorm.csv", index=False, float_format="%.3f")
    C = pd.DataFrame(clock)
    C.to_csv(f"{D}/vol_map_clock_vs_event_test.csv", index=False, float_format="%.3f")
    pd.set_option("display.width", 250, "display.max_columns", 40, "display.max_rows", 400, "display.max_colwidth", 44)
    print(P[(P.symbol == "NQ")].round(2).to_string(index=False))
    print(C[(C.symbol == "NQ")].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
