"""
Live position sizing for the three chosen MNQ models (chosen_models.py): how many micros to trade per signal.

THE RULE (everything is known when the order is sent)
  Per trade:  contracts = floor(risk budget / (stop distance in NQ points x $2 + $2 cost)), at least 0, at most CAP.
              0 means one micro is already more risk than the budget: the trade is skipped.
    overnight_break  stop distance = 2 x ATR(5-min) at the signal bar (exits_engine R_pts; known at the signal close)
    opening_range    stop distance = 9:34 close + 1 tick - the candle's other end (longs; mirror for shorts), i.e. the
                     planned risk the model's own cost filter already uses at 9:35 (the real fill is the 9:35 open)
    expiry_fade      no stop in the model, so a NOTIONAL stop of K_EXP x ADR20 is used for sizing only, where
                     ADR20 = average 9:30-16:00 high-low of the prior 20 full sessions (known before the open).
                     K_EXP = average loss / ADR20 of the worst 10% of expiry-fade trades (the loss tail), so one
                     "notional risk" is about what a bad expiry day costs. Compared with a fixed 1 micro.
  Combined (days with more than one position; only the two breakout models can overlap, because on expiry Fridays
  only the expiry fade trades):
    open-risk cap    total open risk (contracts x risk per contract over open positions) <= OPEN_CAP x budget;
                     a later entry gets only what is left (the 9:35 opening_range entry goes first at a tie)
    daily loss limit realised loss today + open risk + the new trade's risk <= DAY_LIMIT x budget; once losses use
                     it up, no new trades that day
  Budgets: $50, $100, $200 per trade in 2026 dollars, two ways
    fixed   the same $ budget every year (what you would actually have done with a fixed budget since 2010)
    scaled  budget x (NQ price at entry / 2026 average NQ price): the past replayed at 2026 risk levels. One MNQ in
            2010 (NQ ~2,000) was about 1/12th of today's risk, so a fixed budget buys many more contracts back then.
Results are per scenario: contracts per trade by model, net $ per year, max drawdown, worst day, worst month,
return on an assumed account of ACCOUNT_X x budget (1% risk per trade), how often each rule binds, and how often
a trade was skipped because 1 micro was too much risk. Full period and 2019-2026 (real micros) reported separately.
No compounding: the budget is a fixed $ amount, so results for different windows can be read independently.

Input: the models are re-run (chosen_models.py functions, exits_engine, lit_p5_orb) to recover entry/exit times and
stop distances, and checked trade-for-trade against chosen_models_trades.csv. Cached as a pickle in OUT.
Usage:  PYTHONPATH=./pylib python3 position_sizing.py      (OUT defaults to the scratchpad folder below; env SIZING_OUT)
"""
import json
import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent
OUT = Path(os.environ.get("SIZING_OUT", "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/"
                                        "fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/next/sizing"))
CACHE = OUT / "sizing_trades_cache.pkl"
PPT, COST = 2.0, 2.0              # MNQ $ per NQ point, $ per round trip (1 tick each way + $1 commission)
BUDGETS = [50, 100, 200]
CAP = 10                          # most micros on any one trade
OPEN_CAP = 1.5                    # total open risk <= 1.5 x budget
DAY_LIMIT = 2.0                   # realised loss + open risk + new risk <= 2 x budget
ACCOUNT_X = 100                   # assumed account = 100 x budget (budget = 1% of the account)
TAIL_Q = 0.10                     # expiry fade: K = mean loss/ADR20 of the worst 10% of trades
MODELS = ["overnight_break", "opening_range", "expiry_fade"]
ORDER = {"opening_range": 0, "overnight_break": 1, "expiry_fade": 2}
L = []


def say(s=""):
    L.append(s)
    print(s, flush=True)


# ------------------------------------------------------------------------------------------------------------------
# 1. rebuild the trades with entry/exit times and the stop distance known at entry
# ------------------------------------------------------------------------------------------------------------------
def build():
    os.chdir(ROOT)
    import calendar_days as cd
    import chosen_models as cm
    import exits_compare as ec
    import exits_engine as ee
    import lit_p5_orb as p5

    ds = cm.sessions()
    cash_days = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash_days)
    rows = []

    # overnight_break: identical call to chosen_models.overnight_break, keeping bar indices and R_pts
    b = pd.read_pickle("data/x5_NQ.pkl")
    D = ee.Day(b[b.index.year >= ec.FIRST_YEAR])
    del b
    D.pos = pd.Index(D.idx)
    ec.G["NQ"] = D
    sets = ec.entry_sets("NQ")
    t = ee.run(D, sets["Overnight break + daily trend"], "hold", k0=2.0)
    del sets
    bar = t.bar.to_numpy()
    date = pd.to_datetime(D.sess[bar])
    adj = (ds.close_adj - ds.close_raw).reindex(date).to_numpy()
    net_pts = t.pts.to_numpy() - 1.0 / PPT
    ent_t = pd.DatetimeIndex(D.idx[bar + 1]).tz_localize(None)
    ext_t = pd.DatetimeIndex(D.idx[bar + t.hold_bars.to_numpy()]).tz_localize(None) + pd.Timedelta(minutes=5)
    on = pd.DataFrame({"model": "overnight_break", "date": date, "side": np.where(t.dir > 0, "long", "short"),
                       "exit": t.exit.to_numpy(), "entry_time": ent_t, "exit_time": ext_t,
                       "usd": net_pts * PPT, "stop_pts": t.R_pts.to_numpy(), "price": D.Close[bar] - adj})
    on = on[on.date.isin(cash_days) & ~on.date.isin(expiry)]
    rows.append(on)
    del D, t
    ec.G.clear()

    # opening_range and expiry_fade: same loop as chosen_models, also recording the planned stop and times
    dates, g, inst = p5.load_market("NQ")
    sess, Cff, _ = p5.build_sessions("NQ", dates, g, inst)
    sess = sess[sess.date.isin(cash_days)]
    O, H, Lo = g["Open"], g["High"], g["Low"]
    K, ppt, min_R = cm.K, p5.MARKETS["NQ"]["ppt"], p5.MARKETS["NQ"]["min_R"]
    orb = []
    for r in sess.itertuples(index=False):
        i = r.di
        if r.date in expiry or np.isnan(O[i, 0]) or np.isnan(O[i, K]):
            continue
        oc, cc = O[i, 0], Cff[i, K - 1]
        if cc == oc:
            continue
        d = 1 if cc > oc else -1
        stop = np.nanmin(Lo[i, :K]) if d > 0 else np.nanmax(H[i, :K])
        R_sig = d * (cc + d * p5.TICK - stop)
        if R_sig < min_R:
            continue
        ref, fill = O[i, K], O[i, K] + d * p5.TICK
        s_x = r.exit_slot
        if d * (fill - stop) <= 0:
            xs, xfill, why = K, ref - d * p5.TICK, "stop"
        else:
            xs, _, xfill, why = p5.run_trade(H[i], Lo[i], O[i], Cff[i, s_x], K, s_x, d, stop, None, True)
        net = d * (xfill - fill) - p5.COMM / ppt
        base = pd.Timestamp(r.date) + pd.Timedelta(minutes=570)
        orb.append(dict(model="opening_range", date=r.date, side="long" if d > 0 else "short", exit=why,
                        entry_time=base + pd.Timedelta(minutes=K), exit_time=base + pd.Timedelta(minutes=int(xs) + 1),
                        usd=net * ppt, stop_pts=R_sig, price=ref))
    rows.append(pd.DataFrame(orb))

    # ADR20: mean 9:30-close high-low of the prior 20 full sessions (valid-session order, today excluded)
    ncol = np.arange(p5.NSLOT)[None, :]
    di = sess.di.to_numpy()
    inr = ncol <= sess.exit_slot.to_numpy()[:, None]
    rng = np.nanmax(np.where(inr, H[di], np.nan), axis=1) - np.nanmin(np.where(inr, Lo[di], np.nan), axis=1)
    adr = p5.prior_mean(rng, (sess.full & ~sess.abnormal).to_numpy(), 20)
    adr = pd.Series(adr, index=pd.to_datetime(sess.date.to_numpy()))
    ex = []
    for r in sess[sess.date.isin(expiry)].itertuples(index=False):
        ent, ext = O[r.di, 0], Cff[r.di, min(p5.FULL_EXIT_SLOT, r.exit_slot)]
        if np.isnan(ent) or np.isnan(ext):
            continue
        net = (ent - p5.TICK) - (ext + p5.TICK) - p5.COMM / ppt
        base = pd.Timestamp(r.date) + pd.Timedelta(minutes=570)
        ex.append(dict(model="expiry_fade", date=r.date, side="short", exit="close", entry_time=base,
                       exit_time=base + pd.Timedelta(minutes=int(min(p5.FULL_EXIT_SLOT, r.exit_slot)) + 1),
                       usd=net * ppt, stop_pts=np.nan, price=ent))
    rows.append(pd.DataFrame(ex))
    del g, Cff
    T = pd.concat(rows, ignore_index=True)
    T["date"] = pd.to_datetime(T.date)
    T["adr20"] = adr.reindex(T.date).to_numpy()

    # same skip rules as chosen_models
    after_drop, fed = cm.skip_days()
    brk = T.model.isin(["overnight_break", "opening_range"])
    drop = (brk & T.date.isin(after_drop)) | ((T.model == "opening_range") & T.date.isin(fed))
    T = T[~drop].reset_index(drop=True)
    T["ord"] = T.model.map(ORDER)
    T = T.sort_values(["date", "entry_time", "ord"]).reset_index(drop=True)
    p26 = float(ds.close_raw[(ds.index.year == 2026) & ds.cash_day].mean())
    return T, p26


def check(T):
    """Trade-for-trade match against chosen_models_trades.csv (model, date, side, usd)."""
    C = pd.read_csv(ROOT / "chosen_models_trades.csv", parse_dates=["date"])
    key = ["model", "date", "side"]
    a = T.assign(n=T.groupby(key).cumcount()).sort_values(key)
    c = C.assign(n=C.groupby(key).cumcount())
    m = a.merge(c, on=key + ["n"], how="outer", suffixes=("", "_csv"), indicator=True)
    both = m[m._merge == "both"]
    bad = (both.usd - both.usd_csv).abs() > 1e-6
    # R in the CSV = net pts / risk from the fill; ours is the risk known before the fill (9:34 close for the ORB)
    rp = both.usd / PPT / both.R
    return dict(n_rebuilt=len(T), n_csv=len(C), only_rebuilt=int((m._merge == "left_only").sum()),
                only_csv=int((m._merge == "right_only").sum()), usd_mismatch=int(bad.sum()),
                on_stop_vs_csv_R_max_diff=float((rp - both.stop_pts)[both.model == "overnight_break"].abs().max()),
                orb_stop_vs_fill_risk_median_abs_diff=float((rp - both.stop_pts)[both.model == "opening_range"]
                                                            .abs().median()))


# ------------------------------------------------------------------------------------------------------------------
# 2. sizing simulation
# ------------------------------------------------------------------------------------------------------------------
def expiry_k(T, before=None):
    e = T[(T.model == "expiry_fade") & T.adr20.notna()]
    if before is not None:
        e = e[e.date < before]
    loss = np.maximum(0.0, -e.usd / PPT) / e.adr20          # loss in ADR20 units (0 for winners)
    n = max(1, int(np.ceil(TAIL_Q * len(loss))))
    return float(np.sort(loss.to_numpy())[::-1][:n].mean()), e


def simulate(T, budget, scaled, p26, k_exp, exp_mode="vol", open_cap=None, day_limit=None, cap=CAP):
    """Returns per-trade frame with contracts and $ result, and bind flags. No state carries across days."""
    b = budget * (T.price.to_numpy() / p26 if scaled else np.ones(len(T)))
    stop = np.where(T.model == "expiry_fade", k_exp * T.adr20.to_numpy(), T.stop_pts.to_numpy())
    rpc = stop * PPT + COST
    n0 = np.floor(b / rpc)
    n0 = np.where(np.isnan(n0), 0, n0)
    is_exp = (T.model == "expiry_fade").to_numpy()
    no_adr = is_exp & np.isnan(stop)
    if exp_mode == "fixed1":
        n0 = np.where(is_exp, 1, n0)
    else:
        n0 = np.where(no_adr, 1, n0)                           # first 20 sessions of data: 1 micro
        rpc = np.where(no_adr, np.nan, rpc)
    too_big = (n0 == 0)
    at_cap = n0 > cap
    n0 = np.minimum(n0, cap)
    n = n0.copy()
    bind_open = np.zeros(len(T), bool)
    bind_day = np.zeros(len(T), bool)
    if open_cap is not None or day_limit is not None:
        dates = T.date.to_numpy()
        et, xt = T.entry_time.to_numpy(), T.exit_time.to_numpy()
        usd = T.usd.to_numpy()
        starts = np.flatnonzero(np.r_[True, dates[1:] != dates[:-1]])
        ends = np.r_[starts[1:], len(T)]
        for s, e in zip(starts, ends):
            if e - s == 1:
                continue
            for j in range(s + 1, e):
                if n[j] == 0 or np.isnan(rpc[j]):
                    continue
                prev = np.arange(s, j)
                open_ = prev[(xt[prev] > et[j]) & (n[prev] > 0)]
                closed = prev[(xt[prev] <= et[j]) & (n[prev] > 0)]
                open_risk = float(np.nansum(n[open_] * rpc[open_]))
                want = n[j]
                if open_cap is not None:
                    a = max(0.0, np.floor((open_cap * b[j] - open_risk) / rpc[j]))
                    if a < want:
                        bind_open[j] = True
                        want = a
                if day_limit is not None:
                    realised = float((n[closed] * usd[closed]).sum())
                    used = max(0.0, -realised) + open_risk
                    a = max(0.0, np.floor((day_limit * b[j] - used) / rpc[j]))
                    if a < want:
                        bind_day[j] = True
                        want = a
                n[j] = want
    out = T[["model", "date", "side", "exit", "entry_time", "exit_time", "price", "stop_pts", "adr20"]].copy()
    out["budget"] = b
    out["risk_per_micro"] = rpc
    out["usd_1micro"] = T.usd.to_numpy()
    out["contracts"] = n.astype(int)
    out["net_usd"] = n * T.usd.to_numpy()
    out["skip_1micro_too_big"] = too_big
    out["cap_binds"] = at_cap
    out["open_cap_binds"] = bind_open
    out["day_limit_binds"] = bind_day
    return out


def metrics(S, budget, lo=None, hi=None):
    if lo is not None:
        S = S[S.date >= lo]
    if hi is not None:
        S = S[S.date <= hi]
    d = S.groupby("date").net_usd.sum()
    cum = d.cumsum()
    dd = float((np.maximum.accumulate(np.r_[0.0, cum.to_numpy()])[1:] - cum.to_numpy()).max())
    mo = d.groupby(d.index.to_period("M")).sum()
    yrs = (S.date.max() - S.date.min()).days / 365.25
    acct = ACCOUNT_X * budget
    per = {}
    for m in MODELS:
        g = S[S.model == m]
        tk = g[g.contracts > 0]
        per[m] = dict(trades=len(g), taken=len(tk),
                      contracts_median=float(tk.contracts.median()) if len(tk) else 0.0,
                      contracts_min=int(tk.contracts.min()) if len(tk) else 0,
                      contracts_max=int(tk.contracts.max()) if len(tk) else 0,
                      skipped_1micro_too_big_pct=100 * float(g.skip_1micro_too_big.mean()) if len(g) else 0.0,
                      at_cap_pct=100 * float(g.cap_binds.mean()) if len(g) else 0.0,
                      net_usd=float(g.net_usd.sum()))
    return dict(years=yrs, net_usd=float(d.sum()), net_per_year=float(d.sum() / yrs), max_dd=dd,
                worst_day=float(d.min()), worst_day_date=str(d.idxmin().date()),
                worst_month=float(mo.min()), worst_month_id=str(mo.idxmin()),
                ret_pct=100 * float(d.sum()) / acct, ret_pct_per_year=100 * float(d.sum()) / acct / yrs,
                dd_pct=100 * dd / acct, dd_budgets=dd / budget, net_per_budget=float(d.sum()) / budget,
                skipped_1micro_pct=100 * float(S.skip_1micro_too_big.mean()),
                open_cap_binds=int(S.open_cap_binds.sum()), day_limit_binds=int(S.day_limit_binds.sum()),
                days_2plus_trades=int((S.groupby("date").size() >= 2).sum()), per_model=per)


# ------------------------------------------------------------------------------------------------------------------
# 3. report
# ------------------------------------------------------------------------------------------------------------------
def line_block(title, res, budgets):
    say(title)
    say(f"  {'budget':>7} {'net $/yr':>9} {'total $':>9} {'max DD $':>9} {'DD/bgt':>6} {'worst day':>17} "
        f"{'worst month':>17} {'ret %':>6} {'ret %/yr':>8} {'DD %':>6} {'skip1%':>6}")
    for B in budgets:
        m = res[B]
        say(f"  ${B:>6} {m['net_per_year']:>9,.0f} {m['net_usd']:>9,.0f} {m['max_dd']:>9,.0f} {m['dd_budgets']:>6.0f} "
            f"{m['worst_day']:>7,.0f} {m['worst_day_date']:>9} {m['worst_month']:>8,.0f} {m['worst_month_id']:>8} "
            f"{m['ret_pct']:>6.0f} {m['ret_pct_per_year']:>8.1f} {m['dd_pct']:>6.1f} {m['skipped_1micro_pct']:>6.1f}")
    say("  contracts per taken trade, median [min-max]; % of signals skipped because 1 micro > budget; % capped")
    for m_ in MODELS:
        s = "   ".join(f"${B}: {res[B]['per_model'][m_]['contracts_median']:>4.1f} "
                       f"[{res[B]['per_model'][m_]['contracts_min']}-{res[B]['per_model'][m_]['contracts_max']}] "
                       f"skip {res[B]['per_model'][m_]['skipped_1micro_too_big_pct']:4.1f}% "
                       f"cap {res[B]['per_model'][m_]['at_cap_pct']:4.1f}%" for B in budgets)
        say(f"    {m_:16s} {s}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if CACHE.exists():
        T, p26 = pd.read_pickle(CACHE)
    else:
        T, p26 = build()
        pd.to_pickle((T, p26), CACHE)
    chk = check(T)
    k_exp, E = expiry_k(T)
    k_pre, _ = expiry_k(T, before=pd.Timestamp("2019-01-01"))
    loss_adr = np.maximum(0.0, -E.usd / PPT) / E.adr20
    say("POSITION SIZING - three live MNQ models (1 micro = $2/NQ point, $2 round-trip cost)")
    say(f"Rebuilt {chk['n_rebuilt']} trades vs {chk['n_csv']} in chosen_models_trades.csv: only-rebuilt "
        f"{chk['only_rebuilt']}, only-csv {chk['only_csv']}, $ mismatches {chk['usd_mismatch']}")
    say(f"  overnight_break stop = R_pts used by the CSV's R (max diff {chk['on_stop_vs_csv_R_max_diff']:.2g} pts); "
        f"opening_range sizing stop (9:34 close) differs from the fill-based risk by a median "
        f"{chk['orb_stop_vs_fill_risk_median_abs_diff']:.2f} pts")
    say(f"2026 average NQ price used for 'scaled' budgets: {p26:,.0f}")
    say()
    say("Stop distances known at entry (NQ points), median by era:")
    for m in ["overnight_break", "opening_range"]:
        g = T[T.model == m]
        say("  " + f"{m:16s} " + "  ".join(f"{y}: {g[g.date.dt.year == y].stop_pts.median():5.1f}"
                                            for y in (2011, 2014, 2018, 2020, 2022, 2024, 2026)))
    g = T[T.model == "expiry_fade"]
    say("  " + f"{'expiry ADR20':16s} " + "  ".join(f"{y}: {g[g.date.dt.year == y].adr20.median():5.1f}"
                                                    for y in (2011, 2014, 2018, 2020, 2022, 2024, 2026)))
    say()
    say(f"EXPIRY FADE notional stop: K = {k_exp:.2f} x ADR20 (mean loss of the worst {TAIL_Q:.0%} of "
        f"{len(E)} expiry trades, in ADR20 units; using only pre-2019 trades K = {k_pre:.2f})")
    say(f"  share of expiry trades losing more than K x ADR20: {100 * (loss_adr > k_exp).mean():.1f}%; "
        f"worst loss = {loss_adr.max():.2f} x ADR20; median loss of losers = {loss_adr[loss_adr > 0].median():.2f} x ADR20")
    say()

    scen = {}
    sized = {}
    for scaled in (False, True):
        for combo in ("plain", "combined"):
            for B in BUDGETS:
                kw = dict(open_cap=OPEN_CAP, day_limit=DAY_LIMIT) if combo == "combined" else {}
                S = simulate(T, B, scaled, p26, k_exp, **kw)
                tag = f"{'scaled' if scaled else 'fixed'}_{combo}_{B}"
                sized[tag] = S
                scen[tag] = {"full": metrics(S, B), "2019_2026": metrics(S, B, lo=pd.Timestamp("2019-01-01")),
                             "2010_2018": metrics(S, B, hi=pd.Timestamp("2018-12-31")),
                             "2026": metrics(S, B, lo=pd.Timestamp("2026-01-01"))}
    # expiry: vol-sized vs fixed 1 micro (2019-2026 and full, fixed budgets, plain)
    exp_cmp = {}
    for B in BUDGETS:
        for mode in ("vol", "fixed1"):
            S = simulate(T, B, False, p26, k_exp, exp_mode=mode)
            S = S[S.model == "expiry_fade"]
            for lab, lo in (("full", None), ("2019_2026", pd.Timestamp("2019-01-01"))):
                s = S if lo is None else S[S.date >= lo]
                exp_cmp[f"{mode}_{B}_{lab}"] = dict(
                    n=len(s), contracts_median=float(s.contracts.median()), net=float(s.net_usd.sum()),
                    worst=float(s.net_usd.min()), worst_vs_budget=float(s.net_usd.min() / B),
                    sd=float(s.net_usd.std()), mean_over_sd=float(s.net_usd.mean() / s.net_usd.std()))

    sections = [("2019-2026 (real micros)", "2019_2026"), ("2026 so far (today's prices)", "2026"),
                ("FULL 2010-2026", "full"), ("2010-2018 only", "2010_2018")]
    say("=" * 118)
    say(f"RESULTS. Cap {CAP} micros/trade. 'combined' adds open-risk cap {OPEN_CAP} x budget and daily loss limit "
        f"{DAY_LIMIT} x budget. Return % on an assumed account of {ACCOUNT_X} x budget.")
    say("skip1% = share of all signals skipped because one micro was already more risk than the budget.")
    say("=" * 118)
    for lab, key in sections:
        for scaled in ("fixed", "scaled"):
            if key == "2019_2026" and scaled == "scaled":
                note = " (2019 NQ ~7,000 = 1/4 of 2026, so early budgets shrink to 1/4)"
            else:
                note = ""
            for combo in ("combined", "plain"):
                res = {B: scen[f"{scaled}_{combo}_{B}"][key] for B in BUDGETS}
                line_block(f"\n{lab} | {scaled} budget | {combo} rules{note}", res, BUDGETS)
                if combo == "combined":
                    say("  combined rules bound on: " + "   ".join(
                        f"${B}: open-cap {res[B]['open_cap_binds']} trades, day-limit {res[B]['day_limit_binds']} "
                        f"trades (of {res[B]['days_2plus_trades']} days with 2+ trades)" for B in BUDGETS))
    say()
    say("Skipped signals (1 micro > budget), fixed budget, % of that model's signals by year:")
    say(f"  {'year':>4} " + " ".join(f"{m[:8]}${B:<4}" for m in ['overnight_break', 'opening_range'] for B in BUDGETS))
    for y in range(2010, 2027):
        cells = []
        for m in ["overnight_break", "opening_range"]:
            for B in BUDGETS:
                S = sized[f"fixed_plain_{B}"]
                g = S[(S.model == m) & (S.date.dt.year == y)]
                cells.append(f"{100 * g.skip_1micro_too_big.mean():>12.0f}" if len(g) else f"{'-':>12}")
        say(f"  {y:>4} " + " ".join(cells))
    say()
    say("Expiry fade sizing compared (fixed budget, no combined rules needed: nothing else trades on expiry days):")
    for B in BUDGETS:
        for lab in ("2019_2026", "full"):
            v, f = exp_cmp[f"vol_{B}_{lab}"], exp_cmp[f"fixed1_{B}_{lab}"]
            say(f"  ${B:<4} {lab:9s} vol-sized: median {v['contracts_median']:.0f} micros, net ${v['net']:,.0f}, "
                f"worst ${v['worst']:,.0f} ({v['worst_vs_budget']:.1f}x budget)  |  fixed 1 micro: net "
                f"${f['net']:,.0f}, worst ${f['worst']:,.0f} ({f['worst_vs_budget']:.1f}x budget)")

    say()
    say("Baseline for comparison: always exactly 1 micro on every signal (no budget, as chosen_models_trades.csv):")
    S1 = simulate(T, 1e9, False, p26, k_exp, cap=1)
    S1["skip_1micro_too_big"] = False
    for lab, lo, hi in (("2019-2026", "2019-01-01", None), ("2026", "2026-01-01", None), ("full", None, None)):
        m = metrics(S1, 200, lo=pd.Timestamp(lo) if lo else None)
        say(f"  {lab:9s} net ${m['net_per_year']:,.0f}/yr, total ${m['net_usd']:,.0f}, max DD ${m['max_dd']:,.0f}, "
            f"worst day ${m['worst_day']:,.0f} ({m['worst_day_date']}), worst month ${m['worst_month']:,.0f} "
            f"({m['worst_month_id']})")
    say()
    say("What 1 micro risks at the 2026 median stop (the smallest budget that trades it at all):")
    T26 = T[T.date.dt.year == 2026]
    for m in ["overnight_break", "opening_range"]:
        q = T26[T26.model == m].stop_pts * PPT + COST
        say(f"  {m:16s} median ${q.median():,.0f}  (25-75%: ${q.quantile(.25):,.0f}-${q.quantile(.75):,.0f})")
    q = k_exp * T26[T26.model == "expiry_fade"].adr20 * PPT + COST
    say(f"  {'expiry_fade':16s} median ${q.median():,.0f}  (notional {k_exp:.2f} x ADR20)")
    say()
    say("Are the skipped (big-stop) signals better or worse than the ones taken? 2019-2026, fixed budget, "
        "1-micro results, R = net $ / (stop pts x $2 + $2):")
    for B in BUDGETS:
        S = sized[f"fixed_plain_{B}"]
        S = S[(S.date >= pd.Timestamp("2019-01-01")) & (S.model != "expiry_fade")]
        r = S.usd_1micro / S.risk_per_micro
        parts = []
        for m in ["overnight_break", "opening_range"]:
            k = S.model == m
            sk, tk = k & S.skip_1micro_too_big, k & ~S.skip_1micro_too_big
            parts.append(f"{m}: skipped {sk.sum()} avg {r[sk].mean():+.2f}R (${S.usd_1micro[sk].sum():+,.0f} at 1 micro) | "
                         f"taken {tk.sum()} avg {r[tk].mean():+.2f}R")
        say(f"  ${B:<4} " + "   ".join(parts))

    # save
    for tag in ("fixed_combined_50", "fixed_combined_100", "fixed_combined_200", "scaled_combined_100",
                "fixed_plain_100"):
        sized[tag].to_csv(OUT / f"sized_trades_{tag}.csv", index=False)
    rows = []
    for tag, d in scen.items():
        for per, m in d.items():
            r = {"scenario": tag, "period": per, **{k: v for k, v in m.items() if k != "per_model"}}
            for mm, pm in m["per_model"].items():
                for k, v in pm.items():
                    r[f"{mm}_{k}"] = v
            rows.append(r)
    pd.DataFrame(rows).to_csv(OUT / "sizing_scenarios.csv", index=False)
    json.dump(dict(check=chk, p26=p26, k_exp=k_exp, k_exp_pre2019=k_pre, cap=CAP, open_cap=OPEN_CAP,
                   day_limit=DAY_LIMIT, account_x=ACCOUNT_X, scenarios=scen, expiry_compare=exp_cmp),
              open(OUT / "sizing_summary.json", "w"), indent=1, default=str)
    (OUT / "sizing_summary.txt").write_text("\n".join(L) + "\n")
    print(f"\nsaved to {OUT}")


if __name__ == "__main__":
    main()
