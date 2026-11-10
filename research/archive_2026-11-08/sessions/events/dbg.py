import sys
sys.path.insert(0, "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/sessions/events")
import numpy as np, pandas as pd
import event_cont as ec
out = {}
for gap in (5, 15):
    ec.MAXGAP = gap
    G = ec.build_grid("NQ")
    cash = ec.sess.index[ec.sess.cash_day]
    E = ec.et_event_on_sessions("09:30", cash) - G["m0"]
    pE, sE = ec.price(G, E); pK, _ = ec.price(G, E + 5); pX, _ = ec.price(G, E + 125)
    ok = np.isfinite(pE) & np.isfinite(pK) & np.isfinite(pX) & ec.window_ok(G, sE, E + 125)
    out[gap] = pd.DataFrame({"x": np.log(pK / pE), "y": np.log(pX / pK), "ok": ok}, index=cash)
a, b = out[5], out[15]
extra = b.index[b.ok & ~a.ok]
print(b.loc[extra].assign(xbp=lambda d: d.x * 1e4, ybp=lambda d: d.y * 1e4).round(1))
d = a[a.ok]
for lab, s in [("all", d), ("ex 2020-02..04", d[~((d.index >= "2020-02-20") & (d.index <= "2020-04-30"))])]:
    print(lab, ec.nw_t(s.y, s.x))
# influence: top 10 contributions
d = d.assign(c=(d.x - d.x.mean()) * (d.y - d.y.mean()))
print(d.sort_values("c").tail(8).assign(xbp=lambda q: q.x * 1e4, ybp=lambda q: q.y * 1e4)[["xbp", "ybp"]].round(0))
