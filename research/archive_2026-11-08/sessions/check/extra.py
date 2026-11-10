"""Points sizes near 6 AM Mountain (2024-26), CPI-fade 2018-26 stats, overnight-range share set by 8:30-9:29 on CPI days."""
import sys, os
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from events import event, cpi, cash, MULT, COST, G_
from grid import pclose

for name, t0, days in (("08:00 ET", 480, None), ("08:30 ET non-CPI", 510, "noncpi"), ("08:30 ET CPI", 510, cpi),
                       ("09:30 ET", 570, None), ("10:00 ET", 600, None)):
    if days == "noncpi":
        d = event("NQ", t0, 15, 0)
        d = d[~d.sess.isin(cpi)]
    else:
        d = event("NQ", t0, 15, 0, days=days)
    d = d[d.yr >= 2024]
    print(f"NQ |15-min move| 2024-26 {name}: {np.abs(d.p1 - d.p0).mean():.1f} pts (n={len(d)})")

for sym in ("NQ", "ES"):
    d = event(sym, 510, 15, 60, days=cpi)
    d = d[(d.imp != 0) & (d.yr >= 2018)]
    f = -np.sign(d.imp) * d.fol_pts * MULT[sym] - COST[sym]
    print(f"{sym} CPI fade 2018-26: n={len(f)} mean {f.mean():+.2f} t {f.mean() / (f.std() / np.sqrt(len(f))):.2f} "
          f"median {f.median():+.2f} hit {np.mean(f > 0):.2f}; impulse median |pts| {np.abs(d.p1 - d.p0).median():.1f}; "
          f"worst trade {f.min():.0f}")

# overnight range (18:00 prior evening to 09:29) : share of days where the high or low is made 08:30-09:29
G = G_("NQ")
H = G["C"]  # use closes as proxy for high/low (no High/Low loaded)
sess, em = G["sess"], G["et_min"]
mask = ((em >= 18 * 60) | (em < 9 * 60 + 30)) & ~np.isnan(H)
idx = np.flatnonzero(mask)
df = pd.DataFrame({"sess": sess[idx], "em": em[idx], "c": H[idx]})
df = df[df.sess.isin(cash)]
g = df.groupby("sess")
hi_t = df.loc[g.c.idxmax(), ["sess", "em"]].set_index("sess").em
lo_t = df.loc[g.c.idxmin(), ["sess", "em"]].set_index("sess").em
late = ((hi_t >= 510) & (hi_t < 570)) | ((lo_t >= 510) & (lo_t < 570))
isc = pd.Index(late.index).isin(list(cpi))
print(f"NQ overnight extreme (close-based) set 08:30-09:29 ET: CPI days {late[isc].mean():.2f}, other days {late[~isc].mean():.2f}")
