"""
Replication of skip rules R1 / R2 on MES versions of the two breakout models.
Run from the project dir:
  cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this>
Writes only to the scratchpad dir given in OUT.
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, ".")
import calendar_days as cd
import exits_compare as ec
import exits_engine as ee

OUT = Path("/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/skiprules/replication")
PERIODS = [("2010-2015", 2010, 2015), ("2016-2020", 2016, 2020), ("2021-2026", 2021, 2026)]


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


def stats_line(T, cond, label):
    """T: trades with date, usd; cond: boolean array same length."""
    c, o = T.usd[cond], T.usd[~cond]
    return dict(set=label, n=len(c), usd_per_trade=c.mean() if len(c) else np.nan,
                win_pct=100 * (c > 0).mean() if len(c) else np.nan, total=c.sum(),
                n_other=len(o), other_usd=o.mean(), other_win_pct=100 * (o > 0).mean(), t_welch=welch(c, o))


def fmt(d):
    return (f"{d['set']:34s} n={d['n']:4d}  ${d['usd_per_trade']:8.2f}/tr  win {d['win_pct']:5.1f}%  tot ${d['total']:9.0f} | "
            f"other n={d['n_other']:5d} ${d['other_usd']:7.2f}/tr win {d['other_win_pct']:5.1f}%  | t {d['t_welch']:6.2f}")


# ---------------------------------------------------------------- context
ctx = pd.read_pickle("data/market_context.pkl")
ctx.index = pd.to_datetime(ctx.index).normalize()
spx_prev = ctx["spx_ret_1d_prev"]
fomc = cd.fomc_days()

# ---------------------------------------------------------------- MNQ (as traded)
C = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
nq_ob = C[C.model == "overnight_break"][["date", "side", "usd", "bp"]].reset_index(drop=True)
nq_or = C[C.model == "opening_range"][["date", "side", "usd", "bp"]].reset_index(drop=True)

# ---------------------------------------------------------------- MES overnight_break
ds_es = pd.read_pickle("data/daily_sessions_ES.pkl")
ds_es.index = pd.to_datetime(ds_es.index).normalize()
cash_es = ds_es.index[ds_es.cash_day]
exp_es = cd.expiry_fridays(cash_es)

ec.init()
D = ec.G["ES"]
sp = ee.SPEC["ES"]
t = ee.run(D, ec.G[("sets", "ES")]["Overnight break + daily trend"], "hold", k0=2.0)
b = t.bar.to_numpy()
date = pd.to_datetime(D.sess[b]).normalize()
adj = (ds_es.close_adj - ds_es.close_raw).reindex(date).to_numpy()
net_pts = t.pts.to_numpy() - sp["comm"] / sp["usd"]
es_ob = pd.DataFrame({"date": date, "side": np.where(t.dir > 0, "long", "short"),
                      "usd": t.pts.to_numpy() * sp["usd"] - sp["comm"], "bp": 1e4 * net_pts / (D.Close[b] - adj)})
n0 = len(es_ob)
es_ob = es_ob[es_ob.date.isin(cash_es) & ~es_ob.date.isin(exp_es)].reset_index(drop=True)
print(f"MES overnight_break: {n0} raw trades -> {len(es_ob)} after cash-day / expiry-Friday filter, "
      f"{es_ob.date.min():%Y-%m-%d}..{es_ob.date.max():%Y-%m-%d}")

# ---------------------------------------------------------------- MES opening_range (A5T, CSV)
P = pd.read_csv("lit_p5_orb_trades.csv", parse_dates=["date"])
es_or = P[(P.variant == "A5T") & (P.kind == "strategy") & (P.market == "ES")][["date", "side", "net_usd", "net_bp"]]
es_or = es_or.rename(columns={"net_usd": "usd", "net_bp": "bp"})
n0 = len(es_or)
es_or = es_or[~es_or.date.isin(exp_es)].reset_index(drop=True)
print(f"MES opening_range (A5T csv): {n0} -> {len(es_or)} after expiry-Friday filter; "
      f"non-cash days left: {(~es_or.date.isin(cash_es)).sum()}")
# NQ A5T from the same CSV (to see how the CSV construction compares with the as-traded MNQ model)
ds_nq = pd.read_pickle("data/daily_sessions_NQ.pkl")
ds_nq.index = pd.to_datetime(ds_nq.index).normalize()
exp_nq = cd.expiry_fridays(ds_nq.index[ds_nq.cash_day])
nq_or_csv = P[(P.variant == "A5T") & (P.kind == "strategy") & (P.market == "NQ")][["date", "side", "net_usd", "net_bp"]]
nq_or_csv = nq_or_csv.rename(columns={"net_usd": "usd", "net_bp": "bp"})
nq_or_csv = nq_or_csv[~nq_or_csv.date.isin(exp_nq)].reset_index(drop=True)

# ---------------------------------------------------------------- MES opening_range, chosen_models construction (cross-check)
try:
    import chosen_models as cm
    import lit_p5_orb as p5
    cm.SYM = "ES"
    dates, g, inst = p5.load_market("ES")
    sess, Cff, _ = p5.build_sessions("ES", dates, g, inst)
    sess = sess[sess.date.isin(cash_es)]
    es_or_cm = cm.opening_range(exp_es, sess, g, Cff)[["date", "side", "usd", "bp"]]
    es_or_cm["date"] = pd.to_datetime(es_or_cm.date).dt.normalize()
    print(f"MES opening_range (chosen_models construction): {len(es_or_cm)} trades")
except Exception as e:  # noqa
    print("chosen_models-style ES opening_range failed:", repr(e))
    es_or_cm = None

SETS = {
    "MNQ overnight_break (as traded)": nq_ob,
    "MES overnight_break": es_ob,
    "MNQ opening_range (as traded)": nq_or,
    "MNQ opening_range (A5T csv)": nq_or_csv,
    "MES opening_range (A5T csv)": es_or,
}
if es_or_cm is not None:
    SETS["MES opening_range (chosen_models)"] = es_or_cm

for k, T in SETS.items():
    T["spx_prev"] = spx_prev.reindex(T.date).to_numpy()
    T["r1"] = T.spx_prev <= -2
    T["r2"] = T.date.isin(fomc)
    T["year"] = T.date.dt.year
    miss = T.spx_prev.isna().sum()
    if miss:
        print(f"  {k}: {miss} trades without spx_ret_1d_prev")

rows = []
for rule, col in (("R1 (SPX prev day <= -2%)", "r1"), ("R2 (scheduled FOMC day)", "r2")):
    print(f"\n=================== {rule} ===================")
    for k, T in SETS.items():
        d = stats_line(T, T[col].to_numpy(), k)
        d.update(rule=col, period="all")
        rows.append(d)
        print(fmt(d))
        for pname, y0, y1 in PERIODS:
            m = (T.year >= y0) & (T.year <= y1)
            Ts = T[m].reset_index(drop=True)
            if len(Ts) == 0:
                continue
            ds_ = stats_line(Ts, Ts[col].to_numpy(), f"   {pname}")
            ds_.update(rule=col, period=pname, set_full=k)
            rows.append({**ds_, "set": k})
            print(fmt(ds_))
pd.DataFrame(rows).to_csv(OUT / "replication_stats.csv", index=False)


# ---------------------------------------------------------------- overlap / correlation on condition days
def overlap(A, B, col, la, lb):
    a = A.groupby("date").agg(usd_a=("usd", "sum"), bp_a=("bp", "sum"), side_a=("side", "first"), c=(col, "first"))
    bb = B.groupby("date").agg(usd_b=("usd", "sum"), bp_b=("bp", "sum"), side_b=("side", "first"), c=(col, "first"))
    ca, cb = a[a.c], bb[bb.c]
    both = ca.join(cb.drop(columns="c"), how="inner")
    only_a = ca.index.difference(cb.index)
    only_b = cb.index.difference(ca.index)
    print(f"\n--- {la} vs {lb} on {col} days ---")
    print(f"  condition days traded: {la} {len(ca)}, {lb} {len(cb)}, both {len(both)}, only {la} {len(only_a)}, "
          f"only {lb} {len(only_b)}")
    if len(both) > 2:
        r_usd = np.corrcoef(both.usd_a, both.usd_b)[0, 1]
        r_bp = np.corrcoef(both.bp_a, both.bp_b)[0, 1]
        same = (both.side_a == both.side_b).mean() * 100
        signag = (np.sign(both.usd_a) == np.sign(both.usd_b)).mean() * 100
        print(f"  on shared days: corr($) {r_usd:.2f}, corr(bp) {r_bp:.2f}, same side {same:.0f}%, same win/loss sign {signag:.0f}%")
        print(f"  shared days: {la} ${both.usd_a.mean():.2f}/day ({both.bp_a.mean():.1f} bp), "
              f"{lb} ${both.usd_b.mean():.2f}/day ({both.bp_b.mean():.1f} bp)")
    # full-sample daily correlation for reference
    allj = a.join(bb.drop(columns="c"), how="inner")
    print(f"  all shared trading days ({len(allj)}): corr($) {np.corrcoef(allj.usd_a, allj.usd_b)[0, 1]:.2f}, "
          f"same side {(allj.side_a == allj.side_b).mean() * 100:.0f}%")
    # the part of the MES evidence not shared with MNQ
    if len(only_b):
        x = cb.loc[only_b]
        print(f"  {lb} condition days with no {la} trade: n={len(x)}, ${x.usd_b.mean():.2f}/day, "
              f"win {(x.usd_b > 0).mean() * 100:.0f}%")
    # combined test: per-day average of the two versions in bp (each version's bp, averaged where both trade)
    res = {}
    for nm, aa in (("a", a), ("b", bb)):
        res[nm] = aa
    comb = pd.concat([a[["bp_a", "c"]].rename(columns={"bp_a": "bp"}), bb[["bp_b", "c"]].rename(columns={"bp_b": "bp"})])
    comb = comb.groupby(level=0).agg(bp=("bp", "mean"), c=("c", "first"))
    ta = welch(a.bp_a[a.c], a.bp_a[~a.c])
    tb = welch(bb.bp_b[bb.c], bb.bp_b[~bb.c])
    tc = welch(comb.bp[comb.c], comb.bp[~comb.c])
    print(f"  Welch t in bp per day: {la} {ta:.2f}, {lb} {tb:.2f}, average of both versions per day {tc:.2f} "
          f"(n cond days {int(comb.c.sum())})")
    # residual: MES condition-day bp after removing the part explained by MNQ (regression on all shared days)
    if len(both) > 2:
        beta = np.polyfit(allj.bp_a, allj.bp_b, 1)
        resid_all = allj.bp_b - np.polyval(beta, allj.bp_a)
        rc = resid_all[allj.c]
        ro = resid_all[~allj.c]
        print(f"  MES-on-MNQ regression (all shared days) slope {beta[0]:.2f}; MES residual on condition days "
              f"{rc.mean():.1f} bp vs {ro.mean():.1f} bp other, Welch t {welch(rc, ro):.2f}")


print("\n=================== overlap with the MNQ versions ===================")
overlap(nq_ob, es_ob, "r1", "MNQ_ob", "MES_ob")
overlap(nq_or, es_or, "r1", "MNQ_or", "MES_or")
overlap(nq_or, es_or, "r2", "MNQ_or", "MES_or")
overlap(nq_ob, es_ob, "r2", "MNQ_ob", "MES_ob")
if es_or_cm is not None:
    overlap(nq_or, es_or_cm, "r1", "MNQ_or", "MES_or_cm")
    overlap(nq_or, es_or_cm, "r2", "MNQ_or", "MES_or_cm")

# ---------------------------------------------------------------- R1 threshold sensitivity on MES (descriptive)
print("\n=================== MES R1 threshold sensitivity (spx_ret_1d_prev <= x) ===================")
for k in ("MES overnight_break", "MES opening_range (A5T csv)", "MNQ overnight_break (as traded)", "MNQ opening_range (as traded)"):
    T = SETS[k]
    s = []
    for x in (-1.0, -1.5, -2.0, -2.5, -3.0):
        m = (T.spx_prev <= x).to_numpy()
        s.append(f"<= {x:4.1f}: n={m.sum():3d} ${T.usd[m].mean():7.2f} t {welch(T.usd[m], T.usd[~m]):5.2f}")
    print(f"{k:34s} " + " | ".join(s))
# also: up-day mirror (SPX prev >= +2) for symmetry
print("\nmirror: SPX prev day >= +2%")
for k in ("MES overnight_break", "MES opening_range (A5T csv)", "MNQ overnight_break (as traded)", "MNQ opening_range (as traded)"):
    T = SETS[k]
    m = (T.spx_prev >= 2).to_numpy()
    print(f"  {k:34s} n={m.sum():3d} ${T.usd[m].mean():7.2f} win {100 * (T.usd[m] > 0).mean():4.1f}% t {welch(T.usd[m], T.usd[~m]):5.2f}")

for k, T in SETS.items():
    T.to_csv(OUT / f"trades_{k.split(' (')[0].replace(' ', '_')}_{'cm' if 'chosen' in k else ('csv' if 'csv' in k else 'x')}.csv", index=False)
