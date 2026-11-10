"""Tests for walkforward.py on synthetic data (no market data needed):
  folds + locked-holdout refusal, final-fold $/year (span to the data end), the holdout SESSION boundary
  (2025-06-30 18:00) for entries and exits, purge / embargo, sample weights, orientation (and a missing
  features.MIRROR raising), threshold and exit-policy helpers, scorecard points, a PLANTED signal (the model must find
  it with the right sign and make OOS $), PURE NOISE (no OOS edge), no look-ahead (later labels cannot change earlier
  folds), gbm + vote models, permutation test (incl. NaN scores), exits with logit / gbm / vote.
Run:
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_walkforward.py
"""
import math
import time
import warnings

import numpy as np
import pandas as pd

import walkforward as wf

warnings.filterwarnings("ignore", category=UserWarning)
SIGNED = ["f_sig", "f_noise", "pat_hammer", "pat_engulfing", "fam_reversal", "ema_stack"]
FEATS = ["f_sig", "f_noise", "f_level", "pat_hammer", "pat_engulfing", "fam_reversal", "ema_stack"]


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    assert cond, name


def make_events(beta=0.0, beta_pat=0.0, per_year=2500, markets=("ES", "NQ"), years=range(2010, 2027), seed=1):
    """Synthetic entry events. The outcome depends on the ORIENTED feature d*f_sig (beta) and on hammer firing
    in the trade direction (beta_pat). Win = +$27, loss = -$23 (after costs); with beta=beta_pat=0 the expected $ is
    ~0 for every subset (pure noise)."""
    rng = np.random.default_rng(seed)
    rows = []
    for y in years:
        for m in markets:
            day = rng.integers(0, 360, per_year)
            minute = rng.integers(9 * 60 + 30, 15 * 60 + 30, per_year)
            t = pd.Timestamp(y, 1, 1) + pd.to_timedelta(day, "D") + pd.to_timedelta(minute, "min")
            rows.append(pd.DataFrame({"t": t, "market": m}))
    ev = pd.concat(rows, ignore_index=True).sort_values("t", kind="stable").reset_index(drop=True)
    n = len(ev)
    ev["t_end"] = ev.t + pd.to_timedelta(rng.integers(15, 240, n), "min")
    ev["d"] = rng.choice([-1, 1], n)
    ev["f_sig"] = rng.normal(0, 1, n)
    ev["f_noise"] = rng.normal(0, 1, n)
    ev["f_level"] = rng.normal(5, 2, n)
    ev["pat_hammer"] = rng.choice([-1, 0, 1], n, p=[0.1, 0.8, 0.1])
    ev["pat_engulfing"] = rng.choice([-1, 0, 1], n, p=[0.1, 0.8, 0.1])
    ev["fam_reversal"] = np.clip(ev.pat_hammer + ev.pat_engulfing, -1, 1)
    ev["ema_stack"] = rng.choice([-1, 0, 1], n)
    z = -0.2 + beta * ev.d * ev.f_sig + beta_pat * (ev.d * ev.pat_hammer > 0)
    pr = 1 / (1 + np.exp(-z))
    win = rng.random(n) < pr
    if beta == 0 and beta_pat == 0:
        win = rng.random(n) < 23 / 50                  # break-even win rate: E[$] = 0
    ev["pnl_usd_1.5"] = np.where(win, 27.0, -23.0)
    ev["y_1.5"] = win.astype(int)
    ev["t_end_1.5"] = ev.t_end
    return ev


def make_exit_rows(beta=1.0, n_trades_per_year=600, years=range(2010, 2026), seed=3):
    """Synthetic exit rows: each trade is open for 2..20 15-min bars; exit_gain = $ of exiting now minus holding.
    Planted: exiting pays when the oriented f_sig is against the trade (gain = -beta*10*(d*f_sig) + noise - 1)."""
    rng = np.random.default_rng(seed)
    trades = []
    tid = 0
    for y in years:
        day = rng.integers(0, 360, n_trades_per_year)
        start = pd.Timestamp(y, 1, 1) + pd.to_timedelta(day, "D") + pd.Timedelta(hours=10)
        nr = rng.integers(2, 21, n_trades_per_year)
        tr = np.repeat(np.arange(tid, tid + n_trades_per_year), nr)
        k = np.concatenate([np.arange(v) for v in nr])
        t = np.repeat(start, nr) + pd.to_timedelta(15 * k, "min")
        d = np.repeat(rng.choice([-1, 1], n_trades_per_year), nr)
        tend = np.repeat(start + pd.to_timedelta(15 * nr, "min"), nr)
        hold = np.repeat(rng.normal(0, 20, n_trades_per_year), nr)
        sig = np.repeat(start, nr) - pd.Timedelta(minutes=15)          # labels.exit_rows: t = signal bar start
        trades.append(pd.DataFrame({"trade": tr, "k": k, "t": sig, "ts": t, "d": d, "t_end": tend,
                                    "hold_pnl_usd": hold}))
        tid += n_trades_per_year
    r = pd.concat(trades, ignore_index=True)
    n = len(r)
    r["market"] = "ES"
    r["f_sig"] = rng.normal(0, 1, n)
    r["f_noise"] = rng.normal(0, 1, n)
    r["open_R"] = rng.normal(0, 1, n)
    r["pat_engulfing"] = rng.choice([-1, 0, 1], n, p=[0.15, 0.7, 0.15])
    r["pat_hammer"] = rng.choice([-1, 0, 1], n, p=[0.05, 0.9, 0.05])
    r["exit_gain_usd"] = -beta * 10 * r.d * r.f_sig + rng.normal(0, 10, n) - 1.0
    r["y_exit"] = (r.exit_gain_usd > 0).astype(int)
    return r.sample(frac=1.0, random_state=seed).reset_index(drop=True)      # any row order must work


# ------------------------------------------------------------------------------------------- folds / holdout
def test_folds_and_holdout():
    f = wf.make_folds()
    check("folds: 2013..2024 + 2025H1 (13 folds)", [x.name for x in f] == [str(y) for y in range(2013, 2025)]
          + ["2025H1"])
    check("folds: last test ends at the holdout's first bar (2025-06-30 18:00 = session 2025-07-01)",
          f[-1].test_end == wf.HOLDOUT_SESSION_START == pd.Timestamp("2025-06-30 18:00")
          and wf.session_label([wf.HOLDOUT_SESSION_START])[0] == wf.HOLDOUT_START
          and f[-1].test_start == pd.Timestamp("2025-01-01"))
    check("folds: expanding (train_end = test_start)", all(x.train_end == x.test_start for x in f))
    try:
        wf.make_folds(test_years=(2025,), h1_2025=False)
        ok = False
    except wf.HoldoutError:
        ok = True
    check("holdout: a full-2025 test year is refused", ok)
    ff = wf.make_folds(final=True)
    check("holdout: final=True adds the 2025H2+ fold", ff[-1].name == "2025H2+" and ff[-1].test_start ==
          wf.HOLDOUT_SESSION_START and ff[-2].test_end == ff[-1].test_start)
    ev = make_events(beta=0.6, per_year=600)
    try:
        wf.walk_forward(ev, FEATS, signed=SIGNED, folds=[ff[-1]], baselines=False)
        ok = False
    except wf.HoldoutError:
        ok = True
    check("holdout: walk_forward refuses a holdout fold without final=True", ok)
    # holdout labels are never read: garbage / NaN in the holdout leaves every result unchanged
    r1 = wf.walk_forward(ev, FEATS, signed=SIGNED, folds=f[-3:], n_random=20)
    ev2 = ev.copy()
    h = ev2.t >= wf.HOLDOUT_SESSION_START
    ev2.loc[h, "y_1.5"] = 1 - ev2.loc[h, "y_1.5"]
    ev2.loc[h, "pnl_usd_1.5"] = 1e6
    ev2.loc[h, "f_sig"] = np.nan
    r2 = wf.walk_forward(ev2, FEATS, signed=SIGNED, folds=f[-3:], n_random=20)
    check("holdout: changing holdout rows changes nothing", np.array_equal(r1.oos.p.to_numpy(), r2.oos.p.to_numpy())
          and r1.folds.threshold.tolist() == r2.folds.threshold.tolist()
          and r1.pooled.total_usd == r2.pooled.total_usd)
    check("holdout: no OOS row in the holdout", (ev.loc[r1.oos.index, "t"] < wf.HOLDOUT_SESSION_START).all())
    r3 = wf.walk_forward(ev, FEATS, signed=SIGNED, final=True, folds=ff[-2:], n_random=20)
    check("holdout: final=True evaluates 2025H2+", "2025H2+" in r3.folds.fold.tolist())


def test_final_fold_years():
    """REGRESSION (review, major): the open-ended final fold used to divide $ by the years to FAR_FUTURE (74.5 y),
    so its $/year (and the pooled $/year) were ~50x too small. $/year must divide by the span the data covers."""
    ff = wf.make_folds(final=True)
    fh = ff[-1]
    check("final fold: calendar years undefined (NaN), span measured to the data end",
          fh.open_ended and np.isnan(fh.years)
          and np.isclose(fh.span_years(pd.Timestamp("2026-07-01")), (pd.Timestamp("2026-07-01")
                                                                      - wf.HOLDOUT_SESSION_START) / wf.YEAR))
    check("closed folds: span = calendar length (whole year 365/365.25; data_end later changes nothing)",
          np.isclose(ff[0].years, 365 / 365.25) and ff[0].span_years(pd.Timestamp("2030-01-01")) == ff[0].years)
    try:
        fh.span_years()
        ok = False
    except ValueError:
        ok = True
    check("final fold: span_years without data_end refuses (never measured to FAR_FUTURE)", ok)
    ev = make_events(beta=0.6, beta_pat=0.8, per_year=600)
    last = ev.t.max()                                          # 2026-12-26 (synthetic data end)
    span = (wf.session_label([last])[0] + pd.Timedelta(days=1) - wf.HOLDOUT_SESSION_START) / wf.YEAR
    r = wf.walk_forward(ev, FEATS, signed=SIGNED, final=True, folds=ff[-2:], n_random=20)
    F = r.folds.set_index("fold")
    h = F.loc["2025H2+"]
    print(f"     final fold: years {h.years:.3f} (data span {span:.3f}), total ${h.total_usd:.0f}, "
          f"$/year {h.usd_per_year:.0f}; pooled years {r.pooled.years:.3f}, $/year {r.pooled.usd_per_year:.0f}")
    check(f"final fold: years = data span after the holdout start ({h.years:.3f} ~ 1.49, not 74.5)",
          np.isclose(h.years, span) and 1.4 < h.years < 1.6)
    check("final fold: usd_per_year and all_usd_per_year = total / actual span",
          np.isclose(h.usd_per_year, h.total_usd / span) and np.isclose(h.all_usd_per_year, h.all_total / span))
    check("2025H1 fold: span = 2025-01-01 .. 2025-06-30 18:00",
          np.isclose(F.loc["2025H1", "years"], 180.75 / 365.25))
    P = r.pooled
    check("pooled: years = sum of fold spans, $/year = pooled total / years",
          np.isclose(P.years, F.years.sum()) and P.years < 2.1
          and np.isclose(P.usd_per_year, P.total_usd / P.years)
          and np.isclose(P.all_usd_per_year, F.all_total.sum() / P.years))
    r2 = wf.walk_forward(ev, FEATS, signed=SIGNED, final=True, folds=ff[-1:], n_random=20,
                         data_end=pd.Timestamp("2027-07-01"))
    check("data_end= overrides the span (2025-06-30 18:00 .. 2027-07-01 = 2.0 y)",
          np.isclose(r2.folds.years.iloc[0], (pd.Timestamp("2027-07-01") - wf.HOLDOUT_SESSION_START) / wf.YEAR))
    # exits: learned $ gain per year of the final fold uses the same span
    rows = make_exit_rows(beta=1.0, years=range(2018, 2027), n_trades_per_year=300)
    feats = ["f_sig", "f_noise", "open_R"]
    re = wf.walk_forward(rows, feats, kind="exit", label="y_exit", pnl="exit_gain_usd", t_end="t_end",
                         signed=["f_sig", "f_noise"], final=True, folds=ff[-1:], n_random=20, mirror={})
    e = re.folds.iloc[0]
    span_e = (wf.session_label([rows.t.max()])[0] + pd.Timedelta(days=1) - wf.HOLDOUT_SESSION_START) / wf.YEAR
    check(f"final exit fold: learned_gain_per_year = learned_total / span ({e.years:.3f} y)",
          np.isclose(e.years, span_e) and np.isclose(e.learned_gain_per_year, e.learned_total / span_e)
          and np.isclose(re.pooled.learned_gain_per_year, e.learned_total / span_e))


def test_holdout_boundary():
    """REGRESSION (review, minor): the holdout starts with the 2025-07-01 Globex SESSION, i.e. at 2025-06-30 18:00.
    With final=False, events on the evening of 2025-06-30, labels whose path runs past 18:00 and exit trades with
    bars there must be dropped (they used to stay in the 2025H1 test with holdout prices in them)."""
    HS = wf.HOLDOUT_SESSION_START
    ev = make_events(beta=0.6, beta_pat=0.8, per_year=600)
    ev = ev[ev.t < "2025-06-01"].copy()
    T = pd.Timestamp
    add = pd.DataFrame({
        "t": [T("2025-06-30 22:00")] * 4 + [T("2025-06-30 16:30"), T("2025-06-30 10:00"), T("2025-06-30 11:00")],
        "t_end_1.5": [T("2025-07-01 02:00")] * 2 + [T("2025-06-30 23:00")] * 2 + [T("2025-06-30 18:01"),
                                                                                 T("2025-06-30 11:00"),
                                                                                 T("2025-06-30 16:45")],
        "d": [1, -1, 1, -1, 1, 1, -1], "market": ["ES", "NQ", "ES", "NQ", "ES", "ES", "NQ"]},
        index=10 ** 7 + np.arange(7))
    for c in ["f_sig", "f_noise", "f_level", "pat_hammer", "pat_engulfing", "fam_reversal", "ema_stack"]:
        add[c] = ev[c].iloc[:7].to_numpy()
    add["t_end"] = add["t_end_1.5"]
    add["pnl_usd_1.5"] = [27.0, -23.0, 27.0, -23.0, 27.0, 27.0, -23.0]
    add["y_1.5"] = (add["pnl_usd_1.5"] > 0).astype(int)
    ev = pd.concat([ev, add])
    bad, ctrl = add.index[:5], add.index[5:]
    m = wf.before_holdout(ev, "entry", t_end="t_end_1.5")
    check("before_holdout: evening-of-06-30 events and labels ending after 18:00 are holdout; the day is not",
          not m[ev.index.isin(bad)].any() and m[ev.index.isin(ctrl)].all() and m[~ev.index.isin(add.index)].all())
    f = wf.make_folds()[-1:]
    r1 = wf.walk_forward(ev, FEATS, signed=SIGNED, folds=f, n_random=20)
    check("boundary: no 2025H1 OOS row is a holdout-session event; the 2025-06-30 day-session controls are in",
          not r1.oos.index.isin(bad).any() and r1.oos.index.isin(ctrl).sum() == 2)
    ev2 = ev.copy()
    ev2.loc[bad, "pnl_usd_1.5"] = 1e5
    ev2.loc[bad, "y_1.5"] = 1 - ev2.loc[bad, "y_1.5"]
    ev2.loc[bad, "f_sig"] = 50.0
    r2 = wf.walk_forward(ev2, FEATS, signed=SIGNED, folds=f, n_random=20)
    check("boundary: changing holdout-session outcomes/features changes nothing in 2025H1 (final=False)",
          np.array_equal(r1.oos.p.to_numpy(), r2.oos.p.to_numpy()) and r1.folds.all_total.iloc[0] ==
          r2.folds.all_total.iloc[0] and r1.folds.total_usd.iloc[0] == r2.folds.total_usd.iloc[0]
          and r1.folds.threshold.iloc[0] == r2.folds.threshold.iloc[0])
    # also through the default fold (a custom fold ending at calendar 2025-07-01 is accepted; the data guard drops)
    r1c = wf.walk_forward(ev2, FEATS, signed=SIGNED, folds=[wf.Fold("H1cal", T("2025-01-01"), wf.HOLDOUT_START,
                                                                     T("2025-01-01"))], n_random=20)
    check("boundary: a calendar fold ending 2025-07-01 still sees no holdout-session row",
          not r1c.oos.index.isin(bad).any() and r1c.folds.all_total.iloc[0] == r1.folds.all_total.iloc[0])
    # final=True: the evening events are evaluated in the HOLDOUT fold, not in 2025H1
    ff = wf.make_folds(final=True)[-2:]
    r3 = wf.walk_forward(ev, FEATS, signed=SIGNED, final=True, folds=ff, n_random=20)
    o3 = r3.oos
    check("boundary, final=True: 06-30 evening events belong to 2025H2+, day-session controls to 2025H1",
          (o3.loc[o3.index.isin(add.index[:4]), "fold"] == "2025H2+").all() and o3.index.isin(add.index[:4]).sum() == 4
          and (o3.loc[o3.index.isin(ctrl), "fold"] == "2025H1").all())
    # EXITS: a trade signalled 23:30 (bars in the holdout) and one whose bars run past 18:00 are dropped whole
    rows = make_exit_rows(beta=1.0, years=range(2018, 2026), n_trades_per_year=300)
    rows = rows[rows.t < "2025-06-01"]
    feats = ["f_sig", "f_noise", "open_R", "pat_engulfing", "pat_hammer"]

    def trade(tid, t, n, t_end):
        ts = t + pd.Timedelta(minutes=15) + pd.to_timedelta(15 * np.arange(n), "min")
        return pd.DataFrame({"trade": tid, "k": range(n), "t": t, "ts": ts, "d": 1, "t_end": t_end,
                             "hold_pnl_usd": 5.0, "market": "ES", "f_sig": -1.0, "f_noise": 0.0, "open_R": 0.0,
                             "pat_engulfing": 0, "pat_hammer": 0, "exit_gain_usd": 1.0, "y_exit": 1})
    x = pd.concat([trade(10 ** 6, T("2025-06-30 23:30"), 6, T("2025-07-01 01:30")),     # holdout session
                   trade(10 ** 6 + 1, T("2025-06-30 16:00"), 10, T("2025-06-30 18:45")),  # bars run past 18:00
                   trade(10 ** 6 + 2, T("2025-06-30 10:00"), 6, T("2025-06-30 11:45"))],  # control, kept
                  ignore_index=True)
    allr = pd.concat([rows, x], ignore_index=True)
    me = wf.before_holdout(allr, "exit")
    check("before_holdout (exits): holdout trades dropped whole, the day trade kept",
          not me[allr.trade.isin([10 ** 6, 10 ** 6 + 1]).to_numpy()].any() and me[(allr.trade == 10 ** 6 + 2)
                                                                                  .to_numpy()].all())
    kw = dict(kind="exit", label="y_exit", pnl="exit_gain_usd", t_end="t_end", classic=["engulfing"], n_random=20,
              signed=["f_sig", "f_noise", "pat_engulfing", "pat_hammer"], folds=f)
    re1 = wf.walk_forward(allr, feats, **kw)
    check("boundary (exits): no 2025H1 OOS row from a holdout trade or a bar at/after 18:00; control trade in",
          not re1.oos.trade.isin([10 ** 6, 10 ** 6 + 1]).any() and (re1.oos.trade == 10 ** 6 + 2).sum() == 6
          and (allr.loc[re1.oos.index, "ts"] < HS).all())
    allr2 = allr.copy()
    hb = allr2.trade.isin([10 ** 6, 10 ** 6 + 1])
    allr2.loc[hb, "exit_gain_usd"] = 1e5
    allr2.loc[hb, "hold_pnl_usd"] = -1e5
    re2 = wf.walk_forward(allr2, feats, **kw)
    check("boundary (exits): changing holdout trades changes nothing in 2025H1",
          np.array_equal(re1.oos.p.to_numpy(), re2.oos.p.to_numpy())
          and re1.folds.learned_total.iloc[0] == re2.folds.learned_total.iloc[0]
          and re1.folds.hold_total.iloc[0] == re2.folds.hold_total.iloc[0])


# ------------------------------------------------------------------------------------------- purge / embargo
def test_purge_embargo():
    T = pd.to_datetime
    t = T(["2012-12-30 10:00", "2012-12-30 22:00", "2012-12-31 10:00", "2012-06-01 10:00", "2013-02-01 10:00",
           "2014-01-01 10:00", "2014-01-02 10:00", "2014-01-03 10:00", "2014-06-01 10:00"])
    te = T(["2012-12-30 12:00", "2012-12-31 00:00", "2012-12-31 11:00", "2013-01-02 10:00", "2013-02-01 12:00",
            "2014-01-01 12:00", "2014-01-02 12:00", "2014-01-03 12:00", "2014-06-01 12:00"])
    ts, tend = pd.Timestamp("2013-01-01"), pd.Timestamp("2014-01-01")
    m = wf.train_mask(t, te, ts, tend)
    check("purge: label ending <= test start - 1 day kept (incl. exactly at the boundary)", m[0] and m[1])
    check("purge: label ending after test start - 1 day dropped", not m[2])
    check("purge: an old event whose label runs into the test window dropped", not m[3])
    check("purge: test-window and later events never train (expanding)", not m[4:].any())
    m2 = wf.train_mask(t, te, ts, tend, train_end=pd.Timestamp("2020-01-01"), embargo_sessions=1)
    check("embargo: the rest of the test's last session (Jan 1) is embargoed", not m2[5])
    check("embargo: the first session after the test is embargoed", not m2[6])
    check("embargo: later sessions train when allowed", m2[7] and m2[8])
    m3 = wf.train_mask(t, te, ts, tend, train_end=pd.Timestamp("2020-01-01"), embargo_sessions=2)
    check("embargo: 2 sessions", not m3[7] and m3[8])
    # REGRESSION (review): with fewer later sessions in the data than embargo_sessions, the embargo used to switch
    # off (every later session trainable); it must embargo all the later sessions there are.
    t1 = T(["2012-06-01 10:00", "2013-05-01 10:00", "2014-01-02 10:00"])
    te1 = T(["2012-06-01 12:00", "2013-05-01 12:00", "2014-01-02 12:00"])
    me = [wf.train_mask(t1, te1, ts, tend, train_end=pd.Timestamp("2020-01-01"), embargo_sessions=k)[2]
          for k in (0, 1, 2, 3)]
    check("embargo: only one later session in the data -> embargoed for embargo_sessions 1, 2, 3 (0 = off)",
          me == [True, False, False, False])
    # inside walk_forward: no training row of fold 2013 has a label end after 2012-12-31
    ev = make_events(beta=0.6, per_year=400)
    ev.loc[ev.index[:50], "t_end_1.5"] = pd.Timestamp("2013-03-01")      # a few long-running labels from 2010
    tr = wf.train_mask(ev.t, ev["t_end_1.5"], ts, tend)
    check("purge: long-running 2010 labels dropped from fold 2013", not tr[:50].any() and tr[50:].sum() > 1000)


# ------------------------------------------------------------------------------------------- weights
def test_weights():
    T = pd.to_datetime
    ev = pd.DataFrame({"t": T(["2020-01-02 10:00"] * 3 + ["2020-01-03 10:00", "2020-01-04 10:00",
                                                         "2020-01-04 10:05"]),
                       "t_end": T(["2020-01-02 11:00"] * 3 + ["2020-01-03 11:00", "2020-01-04 10:10",
                                                             "2020-01-04 10:15"]),
                       "d": [1, 1, 1, 1, 1, 1], "market": ["ES"] * 6})
    w = wf.sample_weights(ev)
    check("uniqueness: 3 identical windows get 1/3 each", np.allclose(w[:3], 1 / 3))
    check("uniqueness: a lone window gets 1", np.isclose(w[3], 1.0))
    # [10:00,10:10] and [10:05,10:15] overlap half: 5 min alone + 5 min shared -> (5*1 + 5*0.5)/10 = 0.75
    check("uniqueness: half-overlapping windows get 0.75", np.allclose(w[4:], 0.75))
    ev2 = pd.DataFrame({"t": T(["2020-01-02 10:00"] * 3 + ["2020-01-02 10:00"]),
                        "t_end": T(["2020-01-02 11:00"] * 4),
                        "d": [1, 1, 1, -1], "market": ["ES", "NQ", "YM", "ES"]})
    w2 = wf.sample_weights(ev2)
    # per market: ES has 2 overlapping events (1/2 each), NQ/YM 1 each; cross-market (t, d=+1) -> 3 markets
    check("cross-market: same bar & direction in 3 markets divided by 3", np.allclose(w2, [0.5 / 3, 1 / 3, 1 / 3,
                                                                                         0.5]))
    check("cross-market off: only uniqueness", np.allclose(wf.sample_weights(ev2, cross_market=False),
                                                           [0.5, 1, 1, 0.5]))
    ev3 = pd.DataFrame({"t": T(["2020-01-02 10:00", "2020-01-02 10:00"]),
                        "t_end": T(["2020-01-02 10:00", "2020-01-02 10:00"]), "d": [1, 1], "market": ["ES", "ES"]})
    check("uniqueness: zero-length windows use counts", np.allclose(wf.sample_weights(ev3, cross_market=False),
                                                                    0.5))
    rows = pd.DataFrame({"trade": [7, 7, 7, 9, 9, 4]})
    we = wf.exit_weights(rows)
    check("exit weights: each trade's rows sum to 1", np.allclose(pd.Series(we).groupby(rows.trade).sum(), 1.0)
          and np.allclose(we, [1 / 3] * 3 + [0.5, 0.5, 1]))
    # timestamp resolutions must not matter (pandas 3 may store us/s)
    ev4 = ev.copy()
    ev4["t_end"] = pd.DatetimeIndex(ev4.t_end).as_unit("s")
    ev4["t"] = pd.DatetimeIndex(ev4.t).as_unit("us")
    check("weights: mixed timestamp units give the same weights", np.allclose(wf.sample_weights(ev4), w))


# ------------------------------------------------------------------------------------------- helpers
def test_orientation_and_helpers():
    X = pd.DataFrame({"a": [1.0, 1.0, -1.0], "b": [2.0, 2.0, 2.0]})
    o = wf.orient(X, np.array([1, -1, -1]), ["a"])
    check("orient: signed x d, unsigned untouched", o.a.tolist() == [1, -1, 1] and o.b.tolist() == [2, 2, 2]
          and X.a.tolist() == [1, 1, -1])
    Xm = pd.DataFrame({"dist_swhi_5": [-2.0, -2.0], "dist_swlo_5": [3.0, 3.0], "brk_5": [1.0, 1.0]})
    om = wf.orient(Xm, np.array([1, -1]), ["dist_swhi_5", "dist_swlo_5", "brk_5"], {"dist_swhi_5": "dist_swlo_5"})
    check("orient: mirror pairs swap for shorts", om.dist_swhi_5.tolist() == [-2, -3] and
          om.dist_swlo_5.tolist() == [3, 2] and om.brk_5.tolist() == [1, -1])
    try:
        import features as fe
        rng = np.random.default_rng(0)
        cols = [c for c in fe.COLUMNS("ES")]
        Fr = pd.DataFrame(rng.normal(size=(50, len(cols))).astype(np.float32), columns=cols)
        dd = rng.choice([-1, 1], 50)
        same = np.allclose(wf.orient(Fr, dd, fe.SIGNED, fe.MIRROR).to_numpy(), fe.orient(Fr, dd).to_numpy())
        check("orient: identical to features.orient on all feature columns", same and wf.default_mirror() == fe.MIRROR)
        # REGRESSION (review): default_mirror() used to return {} silently when features.MIRROR was missing, so
        # walk_forward(mirror='auto') stopped swapping the swing-distance pair for shorts without a word.
        saved = fe.MIRROR
        del fe.MIRROR
        try:
            try:
                wf.default_mirror()
                raised = False
            except AttributeError:
                raised = True
            ev = make_events(beta=0.0, per_year=50, markets=("ES",), years=range(2010, 2014))
            try:
                wf.walk_forward(ev, FEATS, signed=SIGNED, folds=wf.make_folds()[:1], baselines=False)
                raised_wf = False
            except AttributeError:
                raised_wf = True
            r0 = wf.walk_forward(ev, FEATS, signed=SIGNED, folds=wf.make_folds()[:1], baselines=False, mirror={},
                                 min_inner=20)
        finally:
            fe.MIRROR = saved
        check("default_mirror: a missing features.MIRROR raises (default_mirror and walk_forward(mirror='auto')); "
              "mirror={} runs", raised and raised_wf and isinstance(r0, wf.WalkForwardResult))
    except ImportError:
        print("SKIP features.py not importable")
    p = np.array([0.9, 0.8, 0.7, 0.6]); pnl = np.array([10.0, -5.0, 8.0, -20.0])
    thr, info = wf.select_threshold(p, pnl, min_keep=0.25)
    check("threshold: best mean $ (top 1 -> 10 $)", thr == 0.9 and info["mean_usd"] == 10)
    thr, info = wf.select_threshold(p, pnl, min_keep=0.5)
    check("threshold: >= 50% kept -> top 3 (4.33 $)", thr == 0.7 and np.isclose(info["mean_usd"], 13 / 3))
    thr, info = wf.select_threshold(np.array([0.5, 0.5, 0.4]), np.array([-1.0, 3.0, -9.0]), min_keep=0.3)
    check("threshold: ties in p are kept together", thr == 0.5 and info["keep_share"] == 2 / 3)
    thr, info = wf.select_threshold(np.array([0.5, 0.4]), np.array([-1.0, 3.0]), min_keep=0.05)
    check("threshold: keep-all gives thr 0", thr == 0.0 and info["keep_share"] == 1.0)
    codes = np.array([0, 0, 0, 1, 1]); gain = np.array([1.0, 2.0, 3.0, 5.0, -1.0])
    pe = np.array([0.1, 0.6, 0.9, 0.2, 0.3])
    g, ex = wf.policy_gain(pe >= 0.5, gain, wf.group_starts(codes))
    check("exit policy: first bar with p >= thr; untouched trade held", g.tolist() == [2.0, 0.0]
          and ex.tolist() == [True, False])
    thr, info = wf.select_exit_threshold(pe, gain, codes, min_keep=0.5)
    check("exit threshold: best mean gain per trade", info["mean_usd"] == 3.5 and thr == 0.2)  # A exits row 1 (+2), B row 3 (+5)
    opp = np.array([False, False, True, False, True])
    ev = wf.evaluate_exit_policies(pe, 0.5, gain, codes, opp, hold_usd=np.array([10.0, -4.0]), n_random=50)
    check("exit eval: learned / opp / hold numbers", ev["learned_gain"] == 1.0 and ev["opp_gain"] == 1.0
          and ev["hold_gain"] == 0 and ev["learned_net"] == 4.0 and ev["hold_net"] == 3.0)
    # random-time exits use the learned offsets: learned exits trade 0 at offset 1 with share 0.5
    check("exit eval: random exits within the 5-95% band", ev["random_p5"] <= ev["random_gain"] <= ev["random_p95"])
    check("points: ln2/20 -> 1, ln2 -> 20, -ln2/10 -> -2", wf.points([math.log(2) / 20, math.log(2),
                                                                     -math.log(2) / 10]).tolist() == [1, 20, -2])
    rt = wf.random_skip(np.arange(10.0), 3, 100, np.random.default_rng(0))
    check("random skip: totals of 3 distinct rows", rt.min() >= 3 and rt.max() <= 24 and len(rt) == 100)
    check("top_n: highest scores", sorted(wf.top_n(np.array([1, 5, 3, 5]), 2).tolist()) == [1, 3])


# ------------------------------------------------------------------------------------------- planted / noise
def test_planted_signal():
    ev = make_events(beta=0.6, beta_pat=0.8)
    t0 = time.time()
    r = wf.walk_forward(ev, FEATS, signed=SIGNED, model="logit")
    print(f"     logit walk-forward on {len(ev)} events: {time.time() - t0:.1f} s, folds {len(r.folds)}")
    P = r.pooled
    print(r.folds[["fold", "C", "threshold", "auc", "n_kept", "pnl_per_trade", "all_pnl_per_trade",
                   "vote_topN_pnl_per_trade", "random_p95", "best_pattern"]].round(3).to_string(index=False))
    check("planted: 13 folds evaluated", len(r.folds) == 13)
    check(f"planted: pooled OOS AUC clearly > 0.5 ({P.auc:.3f})", P.auc > 0.62)
    check(f"planted: OOS $/trade {P.pnl_per_trade:.2f} beats all events {P.all_pnl_per_trade:.2f}",
          P.pnl_per_trade > P.all_pnl_per_trade + 3)
    check("planted: beats the random-skip 95% at the same trade count", P.pnl_per_trade > P.random_p95)
    check("planted: beats vote top-N", P.pnl_per_trade > P.vote_topN_pnl_per_trade)
    check(f"planted: ~5% or more kept every fold (min {r.folds.keep_share.min():.3f} >= 0.04; the 5% floor is set "
          "on the validation years)", (r.folds.keep_share >= 0.04).all())
    wt = wf.weight_table(r.coefs)
    s = wt.set_index("feature")
    check("planted: f_sig weight positive in every fold", s.loc["f_sig", "sign_stability"] == 1
          and s.loc["f_sig", "coef_raw_median"] > 0)
    check("planted: f_sig is the largest standardized weight", wt.feature.iloc[0] in ("f_sig", "(intercept)")
          and wt[wt.feature != "(intercept)"].feature.iloc[0] == "f_sig")
    check("planted: pat_hammer positive", s.loc["pat_hammer", "coef_raw_median"] > 0.2)
    check("planted: noise weights small", abs(s.loc["f_noise", "coef_std_median"]) < 0.05
          and abs(s.loc["f_level", "coef_std_median"]) < 0.05)
    sc = wf.scorecard(wt, SIGNED)
    pts = sc.set_index("feature").points
    exp = 0.6 / wf.POINT                                       # 17.3 points per unit of d*f_sig
    print(sc.head(5).to_string(index=False))
    check(f"scorecard: f_sig points {pts['f_sig']} ~ {exp:.1f}", abs(pts["f_sig"] - exp) <= 4)
    check("scorecard: hammer points positive with words", pts["pat_hammer"] > 0 and
          "pointing with the trade" in sc.set_index("feature").loc["pat_hammer", "words"])
    check("planted: best single pattern = hammer in most folds", (r.folds.best_pattern == "pat_hammer").mean() >= 0.8)
    check("calibration: 10 bins, mean p tracks the rate", len(r.calibration) == 10 and
          np.corrcoef(r.calibration.p_mean, r.calibration.y_rate)[0, 1] > 0.95)
    # without orientation the signal is invisible: the planted effect is in d*f_sig, not f_sig
    r_no = wf.walk_forward(ev, FEATS, signed=["pat_hammer", "pat_engulfing", "fam_reversal", "ema_stack"],
                           model="logit", baselines=False, folds=wf.make_folds()[:4])
    check("orientation matters: f_sig without x d has ~no weight",
          abs(wf.weight_table(r_no.coefs).set_index("feature").loc["f_sig", "coef_std_median"]) < 0.05)
    return r


def test_pure_noise():
    ev = make_events(beta=0.0, beta_pat=0.0, seed=7)
    r = wf.walk_forward(ev, FEATS, signed=SIGNED, model="logit")
    P = r.pooled
    se = 25.0 / math.sqrt(max(P.n_kept, 1))
    print(f"     noise: AUC {P.auc:.3f}, kept {P.n_kept:.0f} ({P.keep_share:.2f}), $/trade {P.pnl_per_trade:.2f}, "
          f"all {P.all_pnl_per_trade:.2f}, random 5-95% [{P.random_p5:.2f}, {P.random_p95:.2f}]")
    check(f"noise: pooled AUC ~0.5 ({P.auc:.3f})", abs(P.auc - 0.5) < 0.02)
    check("noise: no OOS edge (within 3 SE of 0)", abs(P.pnl_per_trade) < 3 * se)
    check("noise: inside a widened random-skip band", P.random_p5 - se <= P.pnl_per_trade <= P.random_p95 + se)
    wt = wf.weight_table(r.coefs)
    check("noise: all standardized weights small", wt[wt.feature != "(intercept)"].coef_std_median.abs().max() < 0.05)
    return r


def test_no_lookahead():
    ev = make_events(beta=0.6, beta_pat=0.8, per_year=800)
    folds = wf.make_folds()
    r1 = wf.walk_forward(ev, FEATS, signed=SIGNED, folds=folds, n_random=20)
    ev2 = ev.copy()
    late = ev2.t >= pd.Timestamp("2018-01-01")
    rng = np.random.default_rng(5)
    ev2.loc[late, "y_1.5"] = rng.integers(0, 2, late.sum())
    ev2.loc[late, "pnl_usd_1.5"] = rng.normal(0, 100, late.sum())
    ev2.loc[late, "f_sig"] = rng.normal(0, 5, late.sum())
    r2 = wf.walk_forward(ev2, FEATS, signed=SIGNED, folds=folds, n_random=20)
    early = r1.folds.fold.isin([str(y) for y in range(2013, 2018)])
    o1 = r1.oos[r1.oos.fold.isin([str(y) for y in range(2013, 2018)])]
    o2 = r2.oos[r2.oos.fold.isin([str(y) for y in range(2013, 2018)])]
    check("no look-ahead: 2018+ labels/features don't change folds 2013-2017 (p, thr, C, $)",
          np.array_equal(o1.p.to_numpy(), o2.p.to_numpy())
          and r1.folds[early].threshold.tolist() == r2.folds[early].threshold.tolist()
          and r1.folds[early].C.tolist() == r2.folds[early].C.tolist()
          and r1.folds[early].total_usd.tolist() == r2.folds[early].total_usd.tolist())
    check("no look-ahead: but later folds do change", not np.array_equal(
        r1.oos[~r1.oos.fold.isin(o1.fold.unique())].p.to_numpy(), r2.oos[~r2.oos.fold.isin(o1.fold.unique())].p.to_numpy()))
    # fold k's training rows all end >= 1 day before its test start
    for f in folds:
        m = wf.train_mask(ev.t, ev["t_end_1.5"], f.test_start, f.test_end, f.train_end)
        assert (ev["t_end_1.5"][m] <= f.test_start - pd.Timedelta(days=1)).all()
    check("no look-ahead: every fold's training labels end >= 1 day before its test", True)


def test_gbm_and_vote():
    ev = make_events(beta=0.6, beta_pat=0.8, per_year=1500)
    gp = dict(wf.GBM_PARAMS, min_samples_leaf=100, max_iter=150)
    t0 = time.time()
    rg = wf.walk_forward(ev, FEATS, signed=SIGNED, model="gbm", gbm_params=gp, n_random=50)
    print(f"     gbm walk-forward on {len(ev)} events: {time.time() - t0:.1f} s")
    check(f"gbm: finds the planted signal (AUC {rg.pooled.auc:.3f}, $/trade {rg.pooled.pnl_per_trade:.2f} vs all "
          f"{rg.pooled.all_pnl_per_trade:.2f})", rg.pooled.auc > 0.6 and
          rg.pooled.pnl_per_trade > rg.pooled.all_pnl_per_trade + 2)
    check("gbm: isotonic-calibrated (top bin rate within 0.08 of mean p)",
          abs(rg.calibration.p_mean.iloc[-1] - rg.calibration.y_rate.iloc[-1]) < 0.08)
    # vote: the planted signal is NOT in the vote columns -> vote has ~no edge; with hammer in the vote it has some
    rv = wf.walk_forward(ev, FEATS, signed=SIGNED, model="vote", n_random=50)
    check(f"vote: AUC {rv.pooled.auc:.3f} only from fam_reversal (hammer)", 0.49 < rv.pooled.auc < 0.58)
    check("vote: vote top-N baseline equals the vote model's own picks in $ roughly",
          abs(rv.pooled.pnl_per_trade - rv.pooled.vote_topN_pnl_per_trade) < 3)


def test_gbm_constant_and_empty_columns():
    """Regression (run_pipeline, pooled ES+NQ+YM): a feature with NO finite value in a fold's training rows (x_YM_*
    before YM's data starts in 2018) crashed scikit-learn 1.9's HistGradientBoosting binning. GBMModel now fits on
    the informative columns only (>= 2 distinct finite values), and a constant column (mkt_YM = 0 then) is dropped
    too; the predictions equal those of a fit without the two columns."""
    ev = make_events(beta=0.6, beta_pat=0.8, per_year=800)
    ev["f_empty"] = np.where(ev.t >= pd.Timestamp("2016-01-01"), 1.0, np.nan)    # all-NaN in the 2013-15 training rows
    ev["f_const"] = 0.0
    gp = dict(wf.GBM_PARAMS, min_samples_leaf=100, max_iter=40)
    folds = wf.make_folds()[:2]
    r = wf.walk_forward(ev, FEATS + ["f_empty", "f_const"], signed=SIGNED, model="gbm", gbm_params=gp, folds=folds,
                        baselines=False)
    r0 = wf.walk_forward(ev, FEATS, signed=SIGNED, model="gbm", gbm_params=gp, folds=folds, baselines=False)
    check("gbm: an all-NaN and a constant training column no longer crash (2 folds evaluated)", len(r.folds) == 2)
    check("gbm: those columns are ignored (identical OOS p to a fit without them)",
          np.allclose(r.oos.p.to_numpy(), r0.oos.p.to_numpy()))
    X = np.array([[np.nan, 1.0, 2.0, np.nan], [np.nan, 1.0, 3.0, 5.0], [np.nan, 1.0, 2.0, np.nan]], np.float32)
    check("informative_columns: all-NaN, constant and single-value+NaN columns dropped",
          wf.informative_columns(X).tolist() == [2])
    check("informative_columns: rows with weight 0 do not count",
          wf.informative_columns(X, w=np.array([1.0, 0.0, 1.0])).tolist() == [])


def test_permutation():
    ev = make_events(beta=0.6, beta_pat=0.8, per_year=600, markets=("ES",))
    folds = wf.make_folds()[:6]
    n_perm = 9
    p_min = 1 / (n_perm + 1)                                   # the strongest p-value n_perm shuffles can give
    t0 = time.time()
    pt = wf.permutation_test(ev, FEATS, n_perm=n_perm, seed=1, signed=SIGNED, folds=folds, C_grid=(0.01, 0.1, 1.0))
    print(f"     permutation (planted, {n_perm} shuffles): real {pt['real']:.0f}, perm {np.round(pt['perm'])}, "
          f"p {pt['p_value']:.3f}, {time.time() - t0:.1f} s")
    check("permutation: planted real $ beats every shuffle (p = 1/(n+1))", pt["real"] > pt["perm"].max()
          and np.isclose(pt["p_value"], p_min) and pt["n_valid"] == n_perm)
    evn = make_events(beta=0.0, per_year=600, markets=("ES",), seed=11)
    pn = wf.permutation_test(evn, FEATS, n_perm=n_perm, seed=1, signed=SIGNED, folds=folds, C_grid=(0.01, 0.1, 1.0))
    print(f"     permutation (noise): real {pn['real']:.0f}, perm {np.round(pn['perm'])}, p {pn['p_value']:.3f}")
    # the same assertion FAILS on the planted result above (its p is p_min), so it is not vacuous
    check(f"permutation: noise is not significant (p {pn['p_value']:.2f} > {p_min:.2f}; planted p "
          f"{pt['p_value']:.2f} is not)", pn["p_value"] > p_min and not pt["p_value"] > p_min)
    # REGRESSION (review): a degenerate run (every fold skipped -> real score NaN) used to get the strongest p-value
    evd = make_events(beta=0.0, per_year=300, markets=("ES",), years=range(2012, 2016))
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        pd_ = wf.permutation_test(evd, FEATS, n_perm=5, seed=1, signed=SIGNED, folds=wf.make_folds()[:2],
                                  C_grid=(0.1,))
    check("permutation: NaN real score (all folds skipped) -> p_value NaN with a warning, not 1/(n+1)",
          np.isnan(pd_["real"]) and np.isnan(pd_["p_value"]) and pd_["n_valid"] == 0
          and any(issubclass(w.category, RuntimeWarning) and "p_value is NaN" in str(w.message) for w in wl))
    # NaN SHUFFLE scores count as ">= real" (conservative): real 100, every shuffle NaN -> p = 1
    real = wf.walk_forward(ev, FEATS, signed=SIGNED, folds=folds, C_grid=(0.1,), baselines=False)
    orig = wf.walk_forward

    def nan_run(*a, **k):
        res = orig(*a, **k)
        res.pooled = res.pooled.copy()
        res.pooled["total_usd"] = np.nan
        return res
    wf.walk_forward = nan_run
    try:
        pnan = wf.permutation_test(ev, FEATS, n_perm=3, real=real, signed=SIGNED, folds=folds[:2], C_grid=(0.1,))
    finally:
        wf.walk_forward = orig
    check("permutation: NaN shuffles count against the real model (p = 1, n_valid 0, perm_mean NaN)",
          pnan["p_value"] == 1.0 and pnan["n_valid"] == 0 and np.isnan(pnan["perm_mean"])
          and np.isfinite(pnan["real"]))


def test_exits():
    rows = make_exit_rows(beta=1.0)
    feats = ["f_sig", "f_noise", "open_R", "pat_engulfing", "pat_hammer"]
    signed = ["f_sig", "f_noise", "pat_engulfing", "pat_hammer"]
    t0 = time.time()
    r = wf.walk_forward(rows, feats, kind="exit", model="logit", label="y_exit", pnl="exit_gain_usd",
                        t_end="t_end", signed=signed, trade="trade", classic=["engulfing"])
    print(f"     exit walk-forward on {len(rows)} rows / {rows.trade.nunique()} trades: {time.time() - t0:.1f} s")
    P = r.pooled
    print(r.folds[["fold", "threshold", "auc", "n_trades", "learned_exit_share", "learned_gain", "opp_gain",
                   "random_gain", "random_p95"]].round(3).to_string(index=False))
    check(f"exit planted: AUC {P.auc:.3f} > 0.7", P.auc > 0.7)
    check(f"exit planted: learned exit gains vs hold ({P.learned_gain:.2f} $/trade)", P.learned_gain > 3)
    check("exit planted: beats opposite-pattern exit and random-time exits",
          P.learned_gain > P.opp_gain and P.learned_gain > P.random_p95)
    check("exit: net $ = hold + gain (hold_pnl_usd picked up automatically)",
          np.isclose(P.learned_net, P.hold_net + P.learned_gain))
    o = r.oos.join(rows[["trade", "ts"]], rsuffix="_r")
    check("exit: rows of each trade evaluated in bar order", (o.groupby("trade", sort=False).ts.apply(
        lambda s: s.is_monotonic_increasing)).all())
    wt = wf.weight_table(r.coefs).set_index("feature")
    check("exit planted: f_sig weight NEGATIVE (with-the-trade evidence -> don't exit), stable",
          wt.loc["f_sig", "coef_raw_median"] < 0 and wt.loc["f_sig", "sign_stability"] == 1)
    sc = wf.scorecard(wf.weight_table(r.coefs), signed, kind="exit")
    check("exit scorecard note", "exiting now" in sc.attrs["note"])
    # noise exits: learned exit should not beat hold materially
    rn = wf.walk_forward(make_exit_rows(beta=0.0, seed=9), feats, kind="exit", model="logit", label="y_exit",
                         pnl="exit_gain_usd", t_end="t_end", signed=signed, trade="trade", classic=["engulfing"])
    print(f"     exit noise: AUC {rn.pooled.auc:.3f}, learned gain {rn.pooled.learned_gain:.2f}, "
          f"opp {rn.pooled.opp_gain:.2f}, random [{rn.pooled.random_p5:.2f}, {rn.pooled.random_p95:.2f}]")
    check("exit noise: AUC ~0.5 and no gain vs hold", abs(rn.pooled.auc - 0.5) < 0.03 and rn.pooled.learned_gain < 1.0)
    return r


def test_exit_gbm_vote_permutation():
    """kind='exit' with model='gbm' and model='vote', and the exit permutation test (review: untested before)."""
    rows = make_exit_rows(beta=1.0, n_trades_per_year=400)
    feats = ["f_sig", "f_noise", "open_R", "pat_engulfing", "pat_hammer"]
    kw = dict(kind="exit", label="y_exit", pnl="exit_gain_usd", t_end="t_end", trade="trade", classic=["engulfing"],
              signed=["f_sig", "f_noise", "pat_engulfing", "pat_hammer"], n_random=50)
    t0 = time.time()
    rg = wf.walk_forward(rows, feats, model="gbm", gbm_params=dict(wf.GBM_PARAMS, min_samples_leaf=100, max_iter=60),
                         **kw)
    P = rg.pooled
    print(f"     exit gbm: {time.time() - t0:.1f} s, folds {len(rg.folds)}, AUC {P.auc:.3f}, gain {P.learned_gain:.2f}"
          f" $/trade (share {P.learned_exit_share:.2f}), opp {P.opp_gain:.2f}, random p95 {P.random_p95:.2f}")
    check("exit gbm: all 13 folds, finds the planted exit signal and beats opp / random-time exits",
          len(rg.folds) == 13 and P.auc > 0.75 and P.learned_gain > 3 and P.learned_gain > P.opp_gain
          and P.learned_gain > P.random_p95 and np.isclose(P.learned_net, P.hold_net + P.learned_gain))
    check("exit gbm: no logit coefficients, isotonic p in [0, 1]", rg.coefs.empty and rg.oos.p.between(0, 1).all())
    # vote on the oriented f_sig: for exits the vote is NEGATED (evidence against the trade = reason to exit)
    rv = wf.walk_forward(rows, feats, model="vote", vote_cols=["f_sig"], **kw)
    o = rv.oos.join(rows[["d", "f_sig"]], rsuffix="_r")
    check("exit vote: vote column = -(d * f_sig), positively related to y_exit",
          np.allclose(o.vote, -(o.d_r * o.f_sig), atol=1e-5) and np.corrcoef(o.vote, o.y)[0, 1] > 0.3)
    check(f"exit vote: AUC {rv.pooled.auc:.3f} > 0.75 and gain {rv.pooled.learned_gain:.2f} > 3 $/trade",
          rv.pooled.auc > 0.75 and rv.pooled.learned_gain > 3)
    rv0 = wf.walk_forward(rows, feats, model="vote", **kw)         # no vote columns in feats -> constant p
    check("exit vote without vote columns: runs, constant p per fold (fold AUC 0.5)",
          len(rv0.folds) == 13 and np.allclose(rv0.folds.auc, 0.5)
          and (rv0.oos.groupby("fold").p.nunique() == 1).all())
    pt = wf.permutation_test(rows, feats, n_perm=3, seed=2, folds=wf.make_folds()[:4], C_grid=(0.1,),
                             **dict(kw, n_random=20))
    print(f"     exit permutation: real {pt['real']:.2f}, perm {np.round(pt['perm'], 2)}, p {pt['p_value']:.2f}")
    check("exit permutation: planted real gain beats every shuffle", pt["real"] > pt["perm"].max()
          and np.isclose(pt["p_value"], 1 / 4))


def test_rolling_window_and_decay():
    """Rolling window: each fold trains only on the last N calendar years. Time decay: older rows weigh less.
    On a signal whose sign FLIPS in 2018 both must adapt faster than the expanding window."""
    ev = make_events(beta=0.8, per_year=1500)
    late = ev.t >= pd.Timestamp("2018-01-01")
    ev.loc[late, "f_sig"] = -ev.loc[late, "f_sig"]                  # same outcomes, the feature's meaning flips
    kw = dict(signed=SIGNED, model="logit", baselines=False)
    r3 = wf.walk_forward(ev, FEATS, train_years=3, **kw)
    yrs = pd.DatetimeIndex(ev.t).year
    for row in r3.folds.itertuples():
        y0 = pd.Timestamp(row.test_start).year
        n_max = int(((yrs >= y0 - 3) & (yrs < y0)).sum())
        if not (0 < row.n_train <= n_max and row.n_train > 0.9 * n_max):
            check(f"rolling 3: fold {row.fold} trains on the 3 years before it ({row.n_train} vs {n_max})", False)
    check("rolling 3: every fold trains on (only) the 3 calendar years before its test", True)
    r_exp = wf.walk_forward(ev, FEATS, **kw)
    r_dec = wf.walk_forward(ev, FEATS, decay_half_life=1.0, **kw)
    def after(r):
        f = r.folds[pd.to_datetime(r.folds.test_start) >= pd.Timestamp("2020-01-01")]
        return float((f.pnl_per_trade * f.n_kept).sum() / f.n_kept.sum())
    a_exp, a_3, a_dec = after(r_exp), after(r3), after(r_dec)
    print(f"     2020+ $/trade after the 2018 flip: expanding {a_exp:.2f}  rolling-3 {a_3:.2f}  decay-1y {a_dec:.2f}")
    check("rolling 3 adapts to the flip faster than expanding", a_3 > a_exp + 1)
    check("decay (1-year half-life) adapts to the flip faster than expanding", a_dec > a_exp + 1)
    r_none = wf.walk_forward(ev, FEATS, decay_half_life=None, train_years=None, folds=wf.make_folds()[:3], **kw)
    r_def = wf.walk_forward(ev, FEATS, folds=wf.make_folds()[:3], **kw)
    check("defaults unchanged (expanding, no decay)", np.allclose(r_none.folds.threshold, r_def.folds.threshold))


if __name__ == "__main__":
    T0 = time.time()
    for fn in [test_folds_and_holdout, test_final_fold_years, test_holdout_boundary, test_purge_embargo,
               test_weights, test_orientation_and_helpers, test_planted_signal, test_pure_noise, test_no_lookahead,
               test_gbm_and_vote, test_gbm_constant_and_empty_columns, test_permutation, test_exits, test_exit_gbm_vote_permutation,
               test_rolling_window_and_decay]:
        t = time.time()
        print(f"--- {fn.__name__}")
        fn()
        print(f"    ({time.time() - t:.1f} s)")
    print(f"ALL PASS ({time.time() - T0:.1f} s)")
