"""
Tests for prop_sim.py. Run from the project folder:
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib:. python3 test_prop_sim.py
(also collectable by pytest). Runs in about 10-20 s.
  (a) the vectorized simulator == the loop (run_starts_loop) on real and random series under varied rules
      (consistency 40% / 50% / none, daily loss limit, other targets and max losses), outcome and days of EVERY start
  (b) == the research scripts' own loops: passrate() of research/eval_short_trades.py (its definitions are executed
      exactly as research/eval_tight_stops.py does; nothing is written) and evaluate() of
      research/prop_lucid_flex_dd.py (pulled out of the file with ast), on several series
  (c) evaluate() reproduces EVERY row of research/eval_tight_stops_results.csv, eval_short_trades_results.csv and
      eval_tight_stops_2tick.csv (pass rates, eras, median days, worst day, max drawdown, net and trades per year...)
  (d) the presets equal their reference rows ('Current live models' against the reference code's own row())
  (e) sweeps of 8-10 values finish in well under a few seconds (timings printed), cold and warm cache
"""
import ast
import os
import time

import numpy as np
import pandas as pd

import prop_sim as ps

HERE = os.path.dirname(os.path.abspath(__file__))
TIMINGS = {}
_REF = {}


def _ref():
    """research/eval_short_trades.py's definitions (today, onb, onem, daily, passrate, row, cal), executed the way
    research/eval_tight_stops.py does it: everything before the part that computes and writes the results."""
    if not _REF:
        import research_lib as rl
        src = open(os.path.join(HERE, "research", "eval_short_trades.py")).read()
        ns = {"np": np, "pd": pd, "rl": rl}
        exec(src.split("rows, exp = [], onem")[0].split("import research_lib as rl")[1], ns)
        _REF.update(ns)
        # evaluate() of prop_lucid_flex_dd.py (that script reads a backfill file at import, so only the function and
        # its constants are taken from it)
        tree = ast.parse(open(os.path.join(HERE, "research", "prop_lucid_flex_dd.py")).read())
        keep = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name == "evaluate") or
                (isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "START" or
                                                   isinstance(t, ast.Tuple) and any(getattr(e, "id", None) == "START"
                                                                                    for e in t.elts)
                                                   for t in n.targets))]
        ns2 = {"np": np, "pd": pd}
        exec(compile(ast.Module(body=keep, type_ignores=[]), "prop_lucid_flex_dd.py", "exec"), ns2)
        _REF["evaluate_dd"] = ns2["evaluate"]
    return _REF


def _series(p, start="2018-01-01"):
    dates, v, _ = ps.daily_series(p)
    s = pd.Series(v, index=dates)
    return s[s.index >= start]


def _test_series():
    plan = ps.PRESETS["Eval plan: ONB 9:xx entries, cap 0.15%"][0]
    out = {"live": _series(ps.Params()), "plan": _series(plan), "onb+exp": _series(ps.Params(orb_on=False)),
           "orb hold": _series(ps.Params(onb_on=False, exp_on=False)),
           "plan actual $": _series(ps.replace(plan, money="actual")),
           "onb 3 micros exit 12": _series(ps.Params(orb_on=False, exp_on=False, onb_micros=3, onb_exit=720)),
           "all since 2011": _series(ps.Params(), start="2011-01-01")}
    rng = np.random.default_rng(7)
    idx = out["live"].index
    for mu, sd in ((10, 150), (25, 300), (-5, 120), (3, 60)):
        out[f"random {mu}/{sd}"] = pd.Series(np.round(rng.normal(mu, sd, len(idx)), 2), index=idx)
    out["ties"] = pd.Series(rng.choice([-500.0, -250.0, 0.0, 250.0, 500.0, 1250.0], len(idx)), index=idx)
    return out


RULES = [ps.Rules(), ps.Rules(consistency=0.5), ps.Rules(consistency=None), ps.Rules(dll=600.0),
         ps.Rules(target=2000.0, max_loss=1500.0), ps.Rules(dll=300.0, consistency=0.3, target=1000.0)]


def test_a_vectorized_equals_loop():
    t = time.time()
    n = 0
    for name, s in _test_series().items():
        for r in RULES:
            v = np.maximum(s.to_numpy(), -r.dll) if r.dll is not None else s.to_numpy()
            starts = np.arange(len(v))
            a = ps.run_starts(v, starts, r)
            b = ps.run_starts_loop(v, starts, r)
            assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1]), (name, r)
            n += 1
    TIMINGS["a_cases"] = n
    TIMINGS["a_seconds"] = time.time() - t


def _rates_ref(r):
    done = r[r.out != "open"]
    rate = lambda a, b: (done.loc[a:b].out == "pass").mean()
    return ((done.out == "pass").mean(), rate("2018", "2021"), rate("2022", "2026"),
            done[done.out == "pass"].days.median())


def test_b_equals_research_loops():
    R = _ref()
    for name, s in list(_test_series().items()):
        if name == "all since 2011":
            continue
        ref = R["passrate"](s)                                  # (pass_all, 2018-21, 2022-26, median days)
        got = ps.simulate(s, ps.Rules())
        mine = (got["pass_rate"], got["eras"]["2018-21"]["pass_rate"], got["eras"]["2022-26"]["pass_rate"],
                got["days_pass"][1])
        assert all((a == b) or (np.isnan(a) and np.isnan(b)) for a, b in zip(ref, mine)), (name, ref, mine)
        for cons in (0.40, 0.50):                               # prop_lucid_flex_dd.evaluate: every start
            e = R["evaluate_dd"](s, cons=cons)
            o = ps.simulate(s, ps.Rules(consistency=cons))["outcomes"]
            assert (e.out.to_numpy() == o.out.to_numpy()).all() and (e.days.to_numpy() == o.days.to_numpy()).all(), \
                (name, cons)
            assert _rates_ref(e)[0] == ps.simulate(s, ps.Rules(consistency=cons))["pass_rate"]


# ------------------------------------------------------------------------------------------- reference CSV rows
def _onb(stop, hold, **kw):
    p = dict(orb_on=False, exp_on=True if kw.get("exp") else False, onb_micros=1)
    p.update({"onb_stop_mult": stop.get("stop_mult", 1.0), "onb_cap_pct": stop.get("cap")})
    p.update(hold)
    return ps.Params(**p)


def _orb(stop, exit_min):
    return ps.Params(onb_on=False, exp_on=False, orb_stop_mult=stop.get("stop_mult", 1.0),
                     orb_cap_pct=stop.get("cap"), orb_exit=exit_min)


def tight_stop_params():
    stops = {"2 ATR (now)": {}, "1.5 ATR": {"stop_mult": 0.75}, "1 ATR": {"stop_mult": 0.5},
             "cap 0.20%": {"cap": 0.20}, "cap 0.15%": {"cap": 0.15}, "cap 0.10%": {"cap": 0.10}}
    holds = {"hold to 16:45": {}, "exit 10:30": {"onb_exit": 630}, "9:xx entries only": {"onb_latest_entry": 595}}
    out = []
    for hname, h in holds.items():
        for sname, s in stops.items():
            out.append((f"ONB {hname}, stop {sname}", _onb(s, h)))
            out.append(("  + expiry", _onb(s, h, exp=True)))
    for sname, s in {"1 candle (now)": {}, "0.75 candle": {"stop_mult": 0.75}, "0.5 candle": {"stop_mult": 0.5},
                     "cap 0.10%": {"cap": 0.10}}.items():
        for t in (None, 630):
            out.append((f"ORB {'hold' if t is None else 'exit 10:30'}, stop {sname}", _orb(s, t)))
    return out


def short_trade_params():
    out = []
    for t in (None, 630, 660, 720, 780, 840, 900):
        lab = "close (16:45)" if t is None else ps.hhmm(t)
        h = {} if t is None else {"onb_exit": t}
        out.append((f"ONB exit {lab}", _onb({}, h)))
        out.append((f"ONB exit {lab} + expiry", _onb({}, h, exp=True)))
    out.append(("ONB 9:xx entries only, close", _onb({}, {"onb_latest_entry": 595})))
    out.append(("ONB 9:xx entries only + expiry", _onb({}, {"onb_latest_entry": 595}, exp=True)))
    for t in (600, 630, 660, 720, 780, 840, 900, None):
        out.append((f"ORB exit {'close (15:59)' if t is None else ps.hhmm(t)}", _orb({}, t)))
    out.append(("expiry fade alone", ps.Params(onb_on=False, orb_on=False)))
    return out


def two_tick_params():
    names = {"ONB 9:xx, 2 ATR (now)": _onb({}, {"onb_latest_entry": 595}),
             "ONB 9:xx, cap 0.20%": _onb({"cap": 0.20}, {"onb_latest_entry": 595}),
             "ONB 9:xx, cap 0.15%": _onb({"cap": 0.15}, {"onb_latest_entry": 595}),
             "ONB 9:xx, cap 0.10%": _onb({"cap": 0.10}, {"onb_latest_entry": 595}),
             "ONB exit 10:30, cap 0.15%": _onb({"cap": 0.15}, {"onb_exit": 630}),
             "ONB exit 10:30, cap 0.10%": _onb({"cap": 0.10}, {"onb_exit": 630}),
             "ONB hold, cap 0.15%": _onb({"cap": 0.15}, {}),
             "ORB exit 10:30, cap 0.10%": _orb({"cap": 0.10}, 630), "ORB hold, cap 0.10%": _orb({"cap": 0.10}, None)}
    return names


COLS = {"pass_all": "pass_rate", "pass_18_21": ("eras", "2018-21"), "pass_22_26": ("eras", "2022-26"),
        "days": "days_pass", "worst_day": "worst_day", "max_dd": "max_dd", "net_yr": "net_yr",
        "trades_yr": "trades_yr", "day_mean": "day_mean", "day_sd": "day_sd", "edge_per_var": "edge_per_var"}


def _get(res, key):
    if isinstance(key, tuple):
        return res[key[0]][key[1]]["pass_rate"]
    if key == "days_pass":
        return res["days_pass"][1]
    return res[key]


def _compare(ref_row, res, tag):
    worst = {}
    for col, key in COLS.items():
        a, b = float(ref_row[col]), float(_get(res, key))
        tol = 1e-9 * max(1.0, abs(a))
        assert (np.isnan(a) and np.isnan(b)) or abs(a - b) <= tol, (tag, col, a, b)
        worst[col] = abs(a - b) if np.isfinite(a) else 0.0
    return worst


def _check_csv(path, plist, key=None):
    ref = pd.read_csv(path)
    rows = list(ref.itertuples(index=False))
    assert len(rows) == len(plist), (path, len(rows), len(plist))
    diff = {}
    for r, (name, p) in zip(rows, plist):
        assert r.variant == name, (r.variant, name)
        w = _compare(r._asdict(), ps.evaluate(p, ps.Rules(), outcomes=False), f"{os.path.basename(path)}: {name}")
        for k, v in w.items():
            diff[k] = max(diff.get(k, 0.0), v)
    return len(rows), diff


def test_c_reference_csvs():
    t = time.time()
    n1, d1 = _check_csv(os.path.join(HERE, "research", "eval_tight_stops_results.csv"), tight_stop_params())
    n2, d2 = _check_csv(os.path.join(HERE, "research", "eval_short_trades_results.csv"), short_trade_params())
    ref = pd.read_csv(os.path.join(HERE, "research", "eval_tight_stops_2tick.csv"))
    names = two_tick_params()
    d3 = {}
    for r in ref.itertuples(index=False):
        p = ps.replace(names[r.variant], slippage_ticks=int(r.slip))
        for k, v in _compare(r._asdict(), ps.evaluate(p, ps.Rules(), outcomes=False), f"2tick {r.slip} {r.variant}").items():
            d3[k] = max(d3.get(k, 0.0), v)
    TIMINGS["c_rows"] = n1 + n2 + len(ref)
    TIMINGS["c_seconds"] = time.time() - t
    TIMINGS["c_max_abs_diff_pass_points"] = 100 * max(d1["pass_all"], d2["pass_all"], d3["pass_all"])
    TIMINGS["c_max_abs_diff_net_yr"] = max(d1["net_yr"], d2["net_yr"], d3["net_yr"])


def test_d_presets():
    tight = pd.read_csv(os.path.join(HERE, "research", "eval_tight_stops_results.csv"))
    short = pd.read_csv(os.path.join(HERE, "research", "eval_short_trades_results.csv"))
    plan = ps.evaluate(*ps.PRESETS["Eval plan: ONB 9:xx entries, cap 0.15%"])
    _compare(tight[tight.variant == "ONB 9:xx entries only, stop cap 0.15%"].iloc[0], plan, "preset plan")
    onbx = ps.evaluate(*ps.PRESETS["ONB + expiry fade"])
    _compare(short[short.variant == "ONB exit close (16:45) + expiry"].iloc[0], onbx, "preset ONB + expiry")
    # all three live models: the reference code's own row() on its own daily() of the three replays
    R = _ref()
    o = R["onb"](None)
    o = o[pd.to_datetime(o.date) >= "2018-01-01"]
    orb = R["onem"]("opening_range")
    orb = orb[pd.to_datetime(orb.date) >= "2018-01-01"]
    exp = R["onem"]("expiry_fade")
    exp = exp[pd.to_datetime(exp.date) >= "2018-01-01"]
    row = R["row"]("live", R["daily"](o, orb, exp), len(o) + len(orb) + len(exp))
    live = ps.evaluate(*ps.PRESETS["Current live models"])
    _compare(row, live, "preset live (3 models)")
    TIMINGS["d_live_pass"] = live["pass_rate"]


def test_e_dll_and_windows():
    p = ps.Params()
    dates, v, _ = ps.daily_series(p)
    s = pd.Series(v, index=dates)
    a = ps.simulate(s, ps.Rules(dll=600.0))
    b = ps.simulate(s.clip(lower=-600.0), ps.Rules())
    assert a["pass_rate"] == b["pass_rate"] and a["days_pass"] == b["days_pass"]
    # a custom window's rates are the same starts' outcomes as in the full run
    full = ps.simulate(s, ps.Rules(), start_from="2011-01-01")["outcomes"]
    win = ps.simulate(s, ps.Rules(), start_from="2024-01-01", start_to="2025-06-30")
    sub = full.loc["2024-01-01":"2025-06-30"]
    done = sub[sub.out != "open"]
    assert win["pass_rate"] == (done.out == "pass").mean()
    assert win["n_starts"] == len(sub)
    # era rows are the era's starts whatever the window
    assert win["eras"]["2018-21"]["n_starts"] == ((dates >= "2018-01-01") & (dates <= "2021-12-31")).sum()


def test_f_sweep_timing():
    plan = ps.PRESETS["Eval plan: ONB 9:xx entries, cap 0.15%"][0]
    live = ps.Params()
    ps._replay.cache_clear()
    ps.model_daily.cache_clear()
    worst = 0.0
    for tag, p in (("cold", plan), ("warm", plan), ("live", live)):
        tt = time.time()
        for key in ps.SWEEPABLE:
            vals = ps.SPECS[key]["sweep"]
            assert 5 <= len(vals) <= 12, key
            t = time.time()
            df = ps.sweep(p, ps.Rules(), key, vals)
            dt = time.time() - t
            worst = max(worst, dt)
            TIMINGS[f"f_{tag}_{key}"] = dt
            assert len(df) == len(vals) and df.pass_rate.notna().all(), key
        TIMINGS[f"f_{tag}_all_{len(ps.SWEEPABLE)}_sweeps"] = time.time() - tt
    TIMINGS["f_slowest_single_sweep"] = worst
    assert worst < 3.0, worst


if __name__ == "__main__":
    t0 = time.time()
    for name, fn in sorted((k, v) for k, v in globals().items() if k.startswith("test_")):
        t = time.time()
        fn()
        print(f"PASS {name}  ({time.time() - t:.1f}s)")
    keys = [k for k in TIMINGS if not k.startswith("f_") or "all" in k or "slowest" in k]
    print("results:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in TIMINGS.items() if k in keys})
    print("sweep seconds (cold cache, eval plan):",
          {k[7:]: round(v, 3) for k, v in TIMINGS.items() if k.startswith("f_cold_") and "all" not in k})
    print(f"total {time.time() - t0:.1f}s")
