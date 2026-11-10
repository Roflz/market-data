"""Vectorized bracket simulator on per-day 1-minute arrays (days x slots).
Fill rules (Section 11):
  entry      market at the open of the first bar at/after the decision slot (normally the decision bar itself)
  stop       stop-market, touch triggers (long: low <= stop), fill at the stop or at the bar open if it opened beyond
  target     limit, filled at the target only if a bar trades through it by >= 1 tick; stop wins a same-bar tie
  time exit  market at the open of the first bar at/after slot x; if that bar opens beyond the stop it is a stop
Checks run on bars from the entry bar to the bar before the time-exit bar.
"""
import numpy as np

TICK = 0.25
BIG = 10 ** 6


def simulate(O, H, L, Cff, NV, d, e, x, dirn, stop_dist=None, stop_abs=None, target=None, target_off=None):
    """d: day rows, e: decision/entry slot, x: time-exit slot (all int arrays, same length).
    dirn: +1/-1. stop: stop_abs (absolute price) or stop_dist (entry - dirn*dist, after the entry fill).
    target: absolute price (NaN = none), or target_off (entry + dirn*off). Returns dict of arrays."""
    n = len(d)
    ns = O.shape[1]
    d = np.asarray(d, int)
    e = np.asarray(e, int)
    x = np.asarray(x, int)
    dirn = np.asarray(dirn, float)
    ea = NV[d, np.minimum(e, ns - 1)]
    ok = ea < x
    eac = np.minimum(ea, ns - 1)
    entry = np.where(ok, O[d, eac], np.nan)
    if stop_abs is not None:
        stop = np.asarray(stop_abs, float)
    else:
        stop = entry - dirn * np.asarray(stop_dist, float)
    if target_off is not None:
        tgt = entry + dirn * np.asarray(target_off, float)
    elif target is not None:
        tgt = np.asarray(target, float)
    else:
        tgt = np.full(n, np.nan)
    # orders sit on ticks, never better than the formula: stops further from entry, targets further from entry
    stop = np.where(dirn > 0, np.floor(stop / TICK + 1e-9) * TICK, np.ceil(stop / TICK - 1e-9) * TICK)
    tgt = np.where(dirn > 0, np.ceil(tgt / TICK - 1e-9) * TICK, np.floor(tgt / TICK + 1e-9) * TICK)
    W = int(max(1, (x - np.minimum(ea, x)).max())) if n else 1
    idx = eac[:, None] + np.arange(W)[None, :]
    valid = (idx < x[:, None]) & ok[:, None]
    idc = np.minimum(idx, ns - 1)
    Hs, Ls, Os = H[d[:, None], idc], L[d[:, None], idc], O[d[:, None], idc]
    with np.errstate(invalid="ignore"):
        sh = np.where(dirn[:, None] > 0, Ls <= stop[:, None], Hs >= stop[:, None]) & valid
        th = np.where(dirn[:, None] > 0, Hs >= tgt[:, None] + TICK, Ls <= tgt[:, None] - TICK) & valid
    th &= ~np.isnan(tgt)[:, None]
    i_s = np.where(sh.any(1), sh.argmax(1), BIG)
    i_t = np.where(th.any(1), th.argmax(1), BIG)
    reason = np.full(n, "time", dtype=object)
    xs = np.full(n, -1)
    px = np.full(n, np.nan)
    at_open = np.zeros(n, bool)
    # target strictly first
    mt = (i_t < i_s) & ok
    xs[mt] = ea[mt] + i_t[mt]
    px[mt] = tgt[mt]
    reason[mt] = "target"
    o_t = Os[np.arange(n), np.minimum(i_t, W - 1)]
    at_open[mt] = np.where(dirn[mt] > 0, o_t[mt] >= tgt[mt] + TICK, o_t[mt] <= tgt[mt] - TICK)
    # stop
    ms = (i_s <= i_t) & (i_s < BIG) & ok
    xs[ms] = ea[ms] + i_s[ms]
    o_s = Os[np.arange(n), np.minimum(i_s, W - 1)]
    gap = np.where(dirn > 0, o_s < stop, o_s > stop) & ms
    px[ms] = np.where(gap[ms], o_s[ms], stop[ms])
    at_open[ms] = gap[ms]
    reason[ms] = "stop"
    # time exit
    mx = ok & ~mt & ~ms
    xa = NV[d, np.minimum(x, ns - 1)]
    has = xa < ns
    xo = O[d, np.minimum(xa, ns - 1)]
    # no bar at/after x inside the cache window: last known price (never happens for midday exits; logged)
    fb = mx & ~has
    xs[mx] = np.where(has[mx], xa[mx], x[mx])
    px[mx] = np.where(has[mx], xo[mx], Cff[d[mx], np.minimum(x[mx], ns - 1) - 1])
    at_open[mx] = True
    # time-exit bar opening beyond the stop -> counts as the stop (same price, the open)
    with np.errstate(invalid="ignore"):
        beyond = mx & has & np.where(dirn > 0, xo <= stop, xo >= stop)
    reason[mx] = "time"
    reason[beyond] = "stop"
    reason[~ok] = "no_entry"
    gross = dirn * (px - entry)
    return dict(ok=ok, entry_slot=np.where(ok, ea, -1), entry=entry, exit_slot=xs, exit=px, reason=reason,
                at_open=at_open, gross=gross, stop=stop, target=tgt, fallback=fb)


def finish(res, cost, usd, stress_ticks=2):
    """net points, $, bps and the stop-slippage stress (+stress_ticks ticks on stop fills)."""
    net = res["gross"] - cost
    stress = net - np.where(res["reason"] == "stop", stress_ticks * TICK, 0.0)
    res["net"] = net
    res["usd"] = net * usd
    res["bp"] = 1e4 * net / res["entry"]
    res["gross_bp"] = 1e4 * res["gross"] / res["entry"]
    res["stress_usd"] = stress * usd
    res["stress_bp"] = 1e4 * stress / res["entry"]
    return res


def coin_control(long_bp, short_bp, nrep=1000, seed=12345):
    """mean net bps per trade under fair-coin directions: returns the replication means."""
    rng = np.random.default_rng(seed)
    n = len(long_bp)
    flips = rng.random((nrep, n)) < 0.5
    vals = np.where(flips, long_bp[None, :], short_bp[None, :])
    return vals.mean(1)
