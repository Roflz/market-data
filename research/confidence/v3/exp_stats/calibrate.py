"""Calibrate the v3 significance protocol on existing (pre-holdout) daily P&L series. Light: reads small v2 files.
Output: v3/out/stats_calibration_series.csv, stats_calibration_tables.txt"""
import math, sys
import numpy as np, pandas as pd
sys.path.insert(0, "v3")
import stats_protocol as sp

HOLD = pd.Timestamp("2025-06-30")
O = "v3/out/"
rows, lines = [], []

def P(*a):
    s = " ".join(str(x) for x in a); print(s); lines.append(s)

# common session calendar from the luck pools (every session with bars), pre-holdout
cal = {}
pools = {}
for m in ["NQ", "ES", "YM"]:
    d = pd.read_parquet(f"v2/out/luck_pool_{m}_60.parquet", columns=["d", "pnl_hold", "session", "hour", "t_exit_hold"])
    d = d[d.session < HOLD]
    assert d.t_exit_hold.max() < HOLD + pd.Timedelta(hours=17), "holdout leak"
    pools[m] = d
    cal[m] = np.sort(d.session.unique())
sess_all = np.sort(pools["NQ"].session.unique())

def daily(df, col, sessions):
    s = df.groupby("session")[col].sum()
    return s.reindex(sessions, fill_value=0.0).to_numpy(float)

def describe(name, x):
    x = np.asarray(x, float)
    T = len(x)
    t, se, se_iid = sp.hac_t(x)
    acf = [np.corrcoef(x[:-k], x[k:])[0, 1] for k in (1, 2, 5, 10)]
    ax = np.abs(x - x.mean())
    acfa = [np.corrcoef(ax[:-k], ax[k:])[0, 1] for k in (1, 5, 20)]
    b_sb, _ = sp.politis_white_block(x)
    b_abs, _ = sp.politis_white_block(ax)
    r = dict(series=name, T=T, mean=x.mean(), sd=x.std(ddof=1), sr_ann=x.mean() / x.std(ddof=1) * math.sqrt(252),
             t_iid=x.mean() / se_iid, t_hac=t, vif=(se / se_iid) ** 2, acf1=acf[0], acf2=acf[1], acf5=acf[2],
             acf10=acf[3], absacf1=acfa[0], absacf5=acfa[1], absacf20=acfa[2], pw_block=b_sb, pw_block_abs=b_abs)
    for L in (1, 5, 10, 20, 60):
        r[f"z_boot_L{L}"] = sp.boot_pvalue_mean(x, L, 4000, seed=11)["z_boot"]
    skew, kurt = sp.moments(x)
    r.update(skew=skew, kurt=kurt)
    rows.append(r)

# 1) random LONG trades, 60-min, held to 16:45 (= plain drift): mean per session of the random long trades
for m in ["NQ", "ES", "YM"]:
    d = pools[m]
    lo = d[d.d == 1]
    s = lo.groupby("session").pnl_hold.mean().reindex(sess_all).fillna(0.0).to_numpy()
    sel = sess_all >= (np.datetime64("2018-01-01") if m == "YM" else sess_all[0])
    describe(f"random_long_60_hold_{m}", s[sel])
    # random both sides, one trade per session (first random 18:00-02:00 entry) for per-trade sd
    P(f"{m}: per-trade sd of random 60-min hold trades: all {d.pnl_hold.std():.1f}, 2018+ "
      f"{d[d.session >= '2018-01-01'].pnl_hold.std():.1f}, 2022+ {d[d.session >= '2022-01-01'].pnl_hold.std():.1f}; "
      f"mean long {lo.pnl_hold.mean():+.2f}, short {d[d.d == -1].pnl_hold.mean():+.2f}")

# 2) candidate B (15-min M3, hold) out-of-sample trades, and B minus its drift control
b = pd.read_parquet("v2/out/oos_M3_cls_hold_15m_exp.parquet")
b = b[b.session < HOLD]
assert b.t_exit.max() < HOLD + pd.Timedelta(hours=17)
sB = sess_all[sess_all >= np.datetime64("2013-01-01")]
b["edge"] = b.pnl_usd - b.drift_usd
for mk, g in [("all3", b), ("MNQ", b[b.micro == "MNQ"]), ("MES", b[b.micro == "MES"])]:
    describe(f"B_{mk}_daily", daily(g, "pnl_usd", sB))
    describe(f"B_{mk}_minus_drift_daily", daily(g, "edge", sB))
    P(f"B {mk}: trades {len(g)}, per-trade sd {g.pnl_usd.std():.1f}, mean {g.pnl_usd.mean():+.2f}, "
      f"edge vs drift {g.edge.mean():+.2f} (sd {g.edge.std():.1f})")

# 3) cross-market correlation of the drift series (markets are not independent confirmations)
X = np.column_stack([pools[m][pools[m].d == 1].groupby("session").pnl_hold.mean().reindex(sess_all).fillna(0) for m in ["NQ", "ES", "YM"]])
sel = sess_all >= np.datetime64("2018-01-01")
C = np.corrcoef(X[sel].T)
P("daily corr random-long NQ/ES/YM 2018+:\n", np.round(C, 2), " effective N (rho-bar, Li-Ji):", np.round(sp.effective_n(C), 2))

df = pd.DataFrame(rows)
df.to_csv(O + "stats_calibration_series.csv", index=False)
pd.set_option("display.width", 250)
P(df[["series", "T", "mean", "sd", "sr_ann", "t_iid", "t_hac", "vif", "acf1", "acf5", "absacf1", "absacf20",
      "pw_block", "pw_block_abs", "z_boot_L1", "z_boot_L10", "z_boot_L60", "kurt"]].round(3).to_string(index=False))

# 4) planning tables
P("\nSessions needed (years at 252/yr) for t >= bar; vif 1")
for sr in (0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
    a = [sp.days_needed(sr, tb, pw) for tb, pw in ((2, .5), (2, .8), (3, .5), (3, .8))]
    P(f"  SR_ann {sr:4.2f}: t2@50% {a[0]:7.0f} ({a[0]/252:4.1f}y) t2@80% {a[1]:7.0f} ({a[1]/252:4.1f}y) "
      f"t3@50% {a[2]:7.0f} ({a[2]/252:4.1f}y) t3@80% {a[3]:7.0f} ({a[3]/252:4.1f}y)")
P("\nt-bar implied by DSR>=0.95 (null var) and by one-sided Bonferroni 5%, by effective trials N")
for N in (1, 3, 10, 30, 100, 300, 1000, 4300, 43457):
    P(f"  N {N:6d}: DSR bar t >= {sp.dsr_t_bar(N):.2f}; Bonferroni t >= {sp.bonferroni_t(N):.2f}; E[max z] {sp.expected_max_sr(N,1):.2f}")
hold_days = int(np.busday_count("2025-07-01", "2026-11-07")) - 12
P(f"\nLocked holdout ~{hold_days} sessions: SR_ann detectable at one-sided 5% with 50% power "
  f"{1.645/math.sqrt(hold_days)*math.sqrt(252):.2f}, 80% power {(1.645+0.8416)/math.sqrt(hold_days)*math.sqrt(252):.2f}; "
  f"t>=3 at 50%: {3/math.sqrt(hold_days)*math.sqrt(252):.2f}")
P("\nTrades needed (t>=3, 50% / 80% power) for per-trade edge e with sd s:")
for e, s in ((2, 60), (3, 60), (5, 60), (3, 100), (5, 100), (10, 100), (20, 150), (37, 150)):
    P(f"  edge ${e} sd ${s}: {sp.trades_needed(e, s, 3, .5):8.0f} / {sp.trades_needed(e, s, 3, .8):8.0f}")
open(O + "stats_calibration_tables.txt", "w").write("\n".join(lines) + "\n")
