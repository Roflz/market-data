"""
Tests for research_lib.py. Run from the project folder:
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 test_research_lib.py
(also collectable by pytest). Builds the caches on first use (about 15 s), then runs in well under a minute.
  (a) live_trades() == chosen_models_trades.csv / chosen_models_skipped.csv, every column, exact floats
  (b) replay() with defaults reproduces every live (and skipped) trade exactly, and equals the slow reference path
  (c) stop caps reproduce the stop-cap study (scratchpad stopcap/stopcap.py):
        overnight_break  current $23,213.50, cap 0.20% $20,650, cap 0.10% $12,329 (within $1)
        opening_range    the study used the grid simulator (orb_grid.py) on the live dates: $20,022 / $15,950 /
                         $15,460. The grid skips the live rule's 2 trades on sessions with a 14-minute halt
                         (2020-03-09, 2020-03-18: lit_p5_orb 'abnormal' days, trade_ok False) which the live rule
                         trades through; on the other 3,507 trades replay matches the grid trade by trade. So the
                         grid references are tested on that set, and the live-rule replay (all 3,509 trades:
                         $19,438 / $15,886.50 / $15,427) against the live rule's own per-trade code.
      plus fast == engine/reference for stop multiples, fixed points / $, exit times and 2-tick slippage
  (d) keep_filter_report reproduces filter W's reconciled result (filters/W_recon/W_decisions_final.csv), and the
      random-skip / family-wise / walk-forward helpers reproduce filters/sweep_X (when those files exist)
  (e) a 10-value stop-cap sweep for both models (with the 2-tick re-simulation and book stats) runs in < 15 s
"""
import os
import time

import numpy as np
import pandas as pd

import research_lib as rl

SP = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad"
W_FILE = f"{SP}/filters/W_recon/W_decisions_final.csv"
SWEEP_X = f"{SP}/filters/sweep_X"
TIMINGS = {}


def _live(model, include_skipped=True):
    T = rl.live_trades(include_skipped)
    L = T[T.model == model]
    return L.sort_values("sig_bar" if model == "overnight_break" else "path_row").reset_index(drop=True)


def _same(a, b, cols=("date", "side", "exit", "usd", "R", "bp", "exit_time", "skip_rule")):
    assert len(a) == len(b), (len(a), len(b))
    for c in cols:
        x, y = a[c].to_numpy(), b[c].to_numpy()
        if x.dtype.kind == "f":
            assert np.array_equal(x, y, equal_nan=True), c
        else:
            assert (x == y).all(), c


def test_a_live_trades_equal_csv():
    T = rl.live_trades()
    rl._check_vs_csv(T)                                    # every CSV column, exact floats (raises otherwise)
    L = T[~T.skipped]
    got = L.groupby("model").usd.agg(["size", "sum"])
    assert got.loc["overnight_break"].tolist() == [1731, 23213.5]
    assert got.loc["opening_range"].tolist() == [3509, 19438.0]
    assert got.loc["expiry_fade"].tolist() == [197, 8005.5]
    b = rl.book()
    assert (b["net"], b["max_dd"], b["worst_day"]) == (50657.0, 7949.0, -758.0), b
    assert len(T[T.skipped]) == len(pd.read_csv(rl._p("chosen_models_skipped.csv")))
    # details are consistent: net points from the raw fills
    d = np.where(L.side == "long", 1, -1)
    assert np.allclose(d * (L.exit_px_raw - L.entry_px_raw) - 0.5, L.net_pts) and np.allclose(L.net_pts * 2, L.usd)
    assert (L.entry_time >= L.signal_time).all() and (L.exit_time >= L.entry_time).all()


def test_b_replay_defaults_exact():
    for m in rl.MODELS:
        L = _live(m)
        fast = rl.replay(m, include_skipped=True)
        _same(fast, L)
        _same(rl.replay(m, include_skipped=True, engine=True), fast)
        assert (rl.replay(m).usd.to_numpy() == L[~L.skipped].usd.to_numpy()).all()


def test_c_stop_caps():
    ref_on = {None: 23213.5, 0.002: 20650, 0.001: 12329}
    for cap, ref in ref_on.items():
        r = rl.replay("overnight_break", stop_cap_frac=cap)
        assert abs(r.usd.sum() - ref) <= 1, (cap, r.usd.sum())
        _same(r, rl.replay("overnight_break", stop_cap_frac=cap, engine=True))
    # opening range: grid-study references on the grid's trade set, and the live rule on all trades
    sess = rl.rth()["sess"].set_index("date")
    ref_grid = {None: 20022, 0.002: 15950, 0.001: 15460}
    ref_live = {None: 19438.0, 0.002: 15886.5, 0.001: 15427.0}
    for cap in ref_grid:
        r = rl.replay("opening_range", stop_cap_frac=cap)
        on_grid = r.date.map(sess.trade_ok).to_numpy()
        assert (~on_grid).sum() == 2 and set(r.date[~on_grid].dt.strftime("%Y-%m-%d")) == {"2020-03-09", "2020-03-18"}
        assert abs(r.usd[on_grid].sum() - ref_grid[cap]) <= 1, (cap, r.usd[on_grid].sum())
        assert r.usd.sum() == ref_live[cap], (cap, r.usd.sum())
        _same(r, rl.replay("opening_range", stop_cap_frac=cap, engine=True))


def test_c2_fast_equals_engine_other_settings():
    cases = [dict(stop_mult=0.5), dict(stop_mult=1.5), dict(stop_pts=25), dict(stop_usd=60), dict(exit_time="12:00"),
             dict(exit_time="15:30", stop_cap_frac=0.003), dict(slippage_ticks=2), dict(stop="mult:0.75")]
    n_diff = 0
    for kw in cases:
        a = rl.replay("overnight_break", include_skipped=True, **kw)
        b = rl.replay("overnight_break", include_skipped=True, engine=True, **kw)
        _same(a, b)
        n_diff += len(a) != len(_live("overnight_break"))
    assert n_diff > 0                     # some settings do change which same-day re-entries happen
    for m in ("opening_range", "expiry_fade"):
        for kw in cases + [dict(stop_cap_frac=0.004), dict(exit_time="10:30", stop_pts=8)]:
            _same(rl.replay(m, include_skipped=True, **kw), rl.replay(m, include_skipped=True, engine=True, **kw))
    # 2 ticks per fill on a close-to-close trade = exactly $1 less
    e1, e2 = rl.replay("expiry_fade"), rl.replay("expiry_fade", slippage_ticks=2)
    assert np.allclose(e1.usd - e2.usd, 1.0)


def test_d_filter_W():
    if not os.path.exists(W_FILE):
        print("  (skipped: W reconciliation file not found)")
        return
    W = pd.read_csv(W_FILE, parse_dates=["date"])
    on = rl.live_trades(include_skipped=False)
    on = on[on.model == "overnight_break"].reset_index(drop=True)
    assert (W.date.values == on.date.values).all() and np.array_equal(W.usd.values, on.usd.values)
    keep = (W.decision == "keep").to_numpy()
    r = rl.keep_filter_report(on, keep)
    assert r["removed_n"] == 522 and r["removed_usd"] == 6444.5 and r["kept_usd"] == 16769.0
    assert round(r["welch_t"], 3) == 0.150
    assert r["model_before"]["max_dd"] == 3749.0 and r["model_after"]["max_dd"] == 1306.0
    assert r["model_before"]["worst_day"] == -415.5 and r["model_after"]["worst_day"] == -223.0
    assert r["book_before"]["max_dd"] == 7949.0 and r["book_after"]["max_dd"] == 4903.0
    assert r["book_after"]["net"] == 44212.5 and r["book_after"]["worst_day"] == -729.5
    rp = r["removed_by_period"]
    assert (rp["2010-17"], rp["2018-26"], rp["2024-26"], rp["2023-26"]) == (233.5, 6211.0, -849.5, -1400.5)
    assert not r["pass_a_removed_lose"] and not r["pass_b_t"] and r["pass_c_risk"] and not r["PASS"]
    t2 = r["two_tick"]
    assert t2["removed_usd"] == 5922.5 and t2["model_after"]["max_dd"] == 1590.5
    assert t2["book_before"]["net"] == 45220.0 and t2["book_after"]["max_dd"] == 5103.0
    rs = rl.random_skip_control(on, ~keep, eligible=W.eligible.to_numpy())
    assert abs(rs["pctile"] - 39.8) < 1e-9, rs["pctile"]
    rl.print_report(r, "filter W (reconciled)")

    if os.path.exists(f"{SWEEP_X}/decisions.pkl"):
        P = pd.read_pickle(f"{SWEEP_X}/decisions.pkl")
        fw = rl.familywise(P["dec"], on, eligible=P["elig"])
        assert fw["best_variant"] == "M3_X250" and fw["best_removed_usd"] == -1377.0 and abs(fw["fw_pctile"] - 8.7) < 1e-9
        G = rl.removed_by_year(on, P["dec"])
        Wt, s = rl.walk_forward(G)
        assert abs(s["total_gain"] - (-3318.5)) < 1e-9 and s["years_no_filter"] == 2 and not s["beats_no_filter"]
        ref = pd.read_csv(f"{SWEEP_X}/walk_forward.csv")
        assert (Wt.chosen.values == ref.chosen.values).all()


def test_f_loaders():
    b = rl.bars_1m()
    assert str(b.index.tz) == "America/New_York" and b.index.is_monotonic_increasing
    assert {"Open", "High", "Low", "Close", "Volume", "instrument_id", "sess", "tmin"} <= set(b.columns)
    M = rl.rth()
    assert M["g"]["Open"].dtype == np.float64 and M["g"]["Open"].shape[1] == 390 and len(M["sess"]) > 4000
    D, sigs = rl.engine()
    assert len(sigs) == len(rl.trade_paths("overnight_break")["n"])
    assert rl.daily_sessions().cash_day.sum() > 4000 and "spx_ret_1d_prev" in rl.market_context()
    p = rl.trade_paths("opening_range")
    assert p["sO"].dtype == np.float32 and p["sO"].shape[1] == 385


def test_e_sweep_timing():
    caps = [None, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.004, 0.005, 0.006]
    rl._MEM.clear()                                       # include loading the cache from disk
    t0 = time.time()
    a = rl.sweep("overnight_break", "stop_cap_frac", caps)
    t1 = time.time()
    b = rl.sweep("opening_range", "stop_cap_frac", caps)
    t2 = time.time()
    TIMINGS.update(sweep_overnight_break=t1 - t0, sweep_opening_range=t2 - t1, sweep_both=t2 - t0)
    assert a.net.iloc[0] == 23213.5 and abs(a.set_index("value").net[0.002] - 20650) <= 1
    assert b.net.iloc[0] == 19438.0
    assert t2 - t0 < 15, t2 - t0
    pd.set_option("display.width", 250, "display.max_columns", 30)
    for name, x in (("overnight_break", a), ("opening_range", b)):
        print(f"stop-cap sweep, {name} (value = cap as share of price; NaN = live stop)")
        print(x.round(1).assign(value=x.value).to_string(index=False))


if __name__ == "__main__":
    t0 = time.time()
    TIMINGS["cache_build_or_load"] = sum(rl.build_all().values())
    for name, fn in sorted((k, v) for k, v in globals().items() if k.startswith("test_")):
        t = time.time()
        fn()
        print(f"PASS {name}  ({time.time() - t:.1f}s)")
    print("timings (s):", {k: round(v, 2) for k, v in TIMINGS.items()}, f"total {time.time() - t0:.1f}s")
