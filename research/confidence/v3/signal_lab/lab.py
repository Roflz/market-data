"""
v3/signal_lab/lab.py - SIGNAL LAB v1: how much does ONE metric move price, measured so the answer can be trusted.

QUESTION ANSWERED
  "When this metric says X at a bar's close, what does price do next, beyond what it would have done anyway at that
  time of day / weekday / volatility / trend / last-bar-direction / year?"  Answer = an IMPACT CARD (markdown + csv):
  direction effect + 95% CI, size effect + CI, false-discovery q-value, year-by-year stability, replication in the other
  half of the data, placebo and power calibration, $ per micro after costs, and a one-line plain verdict.

INPUT  (one metric)
  signal: float array / Series aligned to the bar index (bar START time), value KNOWN AT THAT BAR'S CLOSE (NaN = no value).
  kind:   'continuous' (any number; also ordered 'state' with <= 5 levels -> top level vs bottom level),
          'event'      (0/1; optional side=+1/-1 per bar -> effect measured in the trade's direction),
          'sided'      (+1 / -1 / 0 = long event / short event / nothing).
  A callable fn(bars) -> Series (or (Series, side)) is run through lookahead_check() (truncation test) by evaluate_many.

TARGETS (Panel; entry = NEXT bar's open, never crossing the 16:45-18:00 break: horizons are truncated at the session's
  last bar, 16:40-16:45 on 5-min bars)
  dir_h{1,2,4,8,16}, dir_eod : signed forward return (exit = close of bar i+h, or the session's last close) / R20
  abs_*                       : |forward return| / R20                       (SIZE)
  rng_*                       : (max high - min low over bars i+1..i+h) / R20 (SIZE)
  path                        : 1 if +1 R20 is touched before -1 R20 within 16 bars, 0 if -1 first, 0.5 if both in
                                the same bar or neither (stored minus 0.5; effect = change in probability)
  R20 ("average bar") = mean(H - L) of the 20 bars up to and including the decision bar (same contract), floor 2 ticks.
  $ per micro = R20 move x R20 in points x $/point; round-trip cost = harness.SPEC cost ($1 + 1 tick each way).

ISOLATING THE METRIC'S OWN IMPACT  (regression with fixed effects = "matched controls" done additively)
  Every target is residualised on additive fixed effects: 15-min time-of-day slot of the decision bar's close, day of
  week, volatility decile (R20 / its 100-bar median), EMA8/20/50 trend state, sign of the decision bar (C - O), and
  calendar year (removes the plain drift of each slot / regime / year, e.g. "NQ went up"). The metric's rank-score is
  residualised on the same effects for the IC (Frisch-Waugh). The contrast "top fifth minus bottom fifth" (continuous)
  or "event minus non-event" (event) or "event in its side" (sided) is computed on the residualised targets.

INFERENCE  (targets never cross a session, so ALL dependence from overlapping horizons is inside a session)
  Per-session sums A_d, N_d -> effect = sum A / sum N. Reported:
   - se_boot: stationary block bootstrap OVER SESSIONS (Politis-Romano, mean block 10 sessions) -> p_boot (normal tail)
   - se_nw:   Newey-West on the per-session influence series (lag = NW rule, >= 1 session) -> p_nw
   - t_bar_nw (lag = horizon in bars) and t_iid (naive, inflated by overlap) only as diagnostics
   - PLACEBO: the signal grid (session x time-of-day) is circularly shifted by every whole number of sessions in
     [20, T-20] (keeps the signal's own clustering and time-of-day pattern, breaks its timing vs prices; computed for all
     shifts at once with FFT cross-correlation) -> p_placebo_emp (rank) and p_placebo (z vs the placebo spread)
   - p (final, per target) = max(p_boot, p_nw, p_placebo)  (conservative)
   - POWER: a known effect `delta` (R20) is injected into a copy of the target aligned to placebo-shifted copies of the
     signal (n_power shifts) -> detection rate at 0.05 and MDE80 = the effect we would detect 80% of the time.
  Per metric: p_dir = min(1, 6 x min_h p) (Bonferroni over the 6 horizons), p_size the same over abs_*.
  Batch (evaluate_many): Benjamini-Yekutieli q-values over every (metric, market, tf, direction|size) p (valid under
  any dependence); Romano-Wolf step-down (two-sided max-|t|, same session bootstrap) per panel over metric x horizon;
  HALVES: discovery in 2010-17 (BY q < 0.10 among all metrics) must be confirmed in 2018-25H1 (same sign, one-sided
  p < 0.05 at the same horizon), and the other way round.
  Verdict 'CONFIRMED' = q < 0.05 AND replicated (either way) AND placebo rank p < 0.05 AND >= 60% of years same sign.

USAGE
    import lab as L
    P = L.Panel(H.bars("ES", 15), "ES", 15)                     # ~1 s (15-min), ~10 s (5-min)
    b = P.bars
    r = L.evaluate(P, (b.C - b.ema20) / b.atr14, "continuous", name="dist_ema20")
    print(r["table"]); print(L.verdict_lines(r))
    sig = {"dist_ema20": dict(fn=lambda b: (b.C - b.ema20) / b.atr14, kind="continuous", desc="...")}
    batch, res = L.evaluate_many(sig, markets=("ES", "NQ", "YM"), tfs=(5, 15, 60), log_tag="mybatch")
        # writes out/batch_summary.csv + out/cards/<metric>.md/.csv, logs every metric x market x tf to trials.csv
        # 5-min panels need ~2.5 GB: run batches that include tf 5 under the shared heavy flock
  Speed (measured): per metric ~0.3 s (60-min), ~1.5 s (15-min), ~3 s (5-min) per market -> 100 metrics x 3 markets
  x 3 timeframes ~ 25 minutes. Panel build: 1 s / 3 s / 6-9 s.
  Controls can be changed per batch: panel_kw=dict(fe=("slot", "dow", "vol", "trend", "year")) drops the
  last-bar-sign control (which otherwise absorbs most of the known next-bar reversal: see calibrate_real.py).
  python3 v3/signal_lab/test_lab.py          synthetic proof (planted effects, null calibration, overlap, look-ahead)
  python3 v3/signal_lab/calibrate_real.py    real-data null calibration + positive controls (ES 15-min)
  python3 v3/signal_lab/lab.py smoke [5,15,60] [ES,NQ,YM] [nolog]   (4 textbook metrics; example cards in out/smoke)

V1 UPGRADES (2026-11-09, from the methods research; proven on real data by calibrate_lab.py)
  - MAIN PLACEBO = SESSION RE-PAIRING: each session's signal is paired with the prices of a random other session of
    the same calendar year and weekday (n_repair=100 draws). p_repair (z vs the re-pairing spread) replaces the
    circular-shift placebo in the final p = max(p_boot, p_nw, p_repair); verdicts use its rank p (p_repair_emp). The
    circular shift is still reported. A signal that is (nearly) the same every session (pure time of day) cannot be
    judged by re-pairing: the placebo is then marked not applicable (NaN) and left out.
  - FOUR-WAY DIRECTION VERDICT (batch column dir_class, card 'BOTTOM LINE'), an equivalence test of the per-trade
    edge in $ per micro against the real $ round-trip cost (v1.1; see V1.1 FIXES and _dir_class):
      REAL & TRADABLE     CONFIRMED and, in 2018-25H1, the $ edge per trade's lower 80% bound beats the cost
      REAL BUT TOO SMALL  CONFIRMED but not clearly above cost (filter / sizing use only)
      CONFIDENTLY NOTHING not confirmed, at every hold of 1-8 bars the 90% CI of the $ edge lies inside +-cost, and
                          the 16-bar / to-16:45 best estimates are below cost
      INCONCLUSIVE        otherwise (data_needed_x = how many times more data would settle it)
  - REPLICATION for markets without both chronological halves (YM, 2018+) uses interleaved halves (odd / even
    calendar quarters); batch column rep_split says which split was used.
  - Panel.injected(add): power by injection into REAL prices through the full pipeline (Brown-Warner).
  - Cards print the real-data self-test status for each market x timeframe (out/calibration/self_test_status.json,
    written by calibrate_lab.py summary): PASSED / FAILED / UNCALIBRATED.

V1.1 FIXES (2026-11-09, after an adversarial review)
  - LOOK-AHEAD: lookahead_check cuts the data at 40 of the metric's OWN signal rows (events / non-default levels / top
    and bottom fifth) plus 60 random rows (was: 3 random rows). A leak in a rare yes/no event only changes the value on
    event bars, which 3 random cuts almost never hit (an inside bar labelled with its next bar's breakout passed and
    was called REAL & TRADABLE). A FAILED check now overrides every verdict to INVALID (batch column `lookahead`,
    dir_class 'INVALID (LOOK-AHEAD)'); metrics given as numbers are 'UNCHECKED' and a REAL class on them carries
    ' (look-ahead UNCHECKED)'. evaluate() also accepts a function and checks it.
  - TRADABILITY IN $: the four-way verdict compares the per-trade edge in $ per micro (each trade's excess move x its
    own R20 x $/pt, session bootstrap) with the real $ round trip. The old rule compared the R20 edge with the MEAN of
    cost/R20, which overstates the break-even 1.3-1.7x (Jensen) and labelled edges clearing costs by $1-2 'too small'.
    Break-even in R20 = cost / mean R20 of the signal's trades. CONFIDENTLY NOTHING now also requires the 16-bar and
    to-16:45 best estimates to be below cost (an edge building over 16 bars was called 'nothing'). $ per R20 uses
    the MEAN R20 of the signal's trades (was the median of all bars: mixed units on the cards).

CAVEATS (v0, still true in v1)
  Quintile cut points are full-sample (fine for measuring association; a live rule must use past-only cut points).
  Fixed effects are additive (no slot x trend interactions) and estimated in-sample. Event-study paths have no CI.
"""
import math
import os
import sys
import time

import numpy as np
import pandas as pd
import scipy.sparse as sps
from scipy.stats import norm, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
try:
    import harness as H
    SPEC = H.SPEC
except Exception:                                                   # standalone use (tests)
    H = None
    SPEC = {"ES": dict(usd=5.0, tick=0.25, micro="MES"), "NQ": dict(usd=2.0, tick=0.25, micro="MNQ"),
            "YM": dict(usd=0.5, tick=1.0, micro="MYM")}
    for _s in SPEC.values():
        _s["cost"] = 2 * _s["tick"] * _s["usd"] + 1.0
MICRO = {"ES": "MES", "NQ": "MNQ", "YM": "MYM"}

HORIZONS = (1, 2, 4, 8, 16, 0)                                      # 0 = to the session's last bar (16:45)
HN = {h: ("eod" if h == 0 else f"h{h}") for h in HORIZONS}
DIR = [f"dir_{HN[h]}" for h in HORIZONS]
ABS = [f"abs_{HN[h]}" for h in HORIZONS]
RNG = [f"rng_{HN[h]}" for h in HORIZONS]
TARGETS = DIR + ABS + RNG + ["path"]
COL = {c: j for j, c in enumerate(TARGETS)}
PLACEBO_COLS = DIR + ABS + RNG + ["path"]
SIZE_COLS = set(ABS + RNG)
PATH_H = 16
ES_K = 16
SESSION_MIN = 1365                                                  # 18:00 -> 16:45
MIN_SHIFT = 20
ERAS = {"2010-17": (2010, 2017), "2018-25H1": (2018, 2025)}
FE_DEFAULT = ("slot", "dow", "vol", "trend", "prev", "year")
NOTHING_HOLDS = ("dir_h1", "dir_h2", "dir_h4", "dir_h8")              # holds a CONFIDENTLY NOTHING verdict covers


# ============================================================================================ small stats helpers
def nw_lags(T):
    return max(int(math.floor(4 * (T / 100.0) ** (2.0 / 9.0))), 1)


def stationary_indices(T, mean_block, B, seed=0):
    """(B, T) day indices of the stationary bootstrap (Politis-Romano), circular wrap (= stats_protocol)."""
    rng = np.random.default_rng(seed)
    p = 1.0 / max(float(mean_block), 1.0)
    new = rng.random((B, T)) < p
    new[:, 0] = True
    pos = np.broadcast_to(np.arange(T), (B, T))
    last = np.maximum.accumulate(np.where(new, pos, 0), axis=1)
    first = np.take_along_axis(rng.integers(0, T, (B, T)), last, axis=1)
    return ((first + pos - last) % T).astype(np.int64)


def boot_counts(T, mean_block=10.0, B=1000, seed=0):
    """(B, T) float matrix: how often each session is drawn in each bootstrap replicate (sum stats = counts @ x)."""
    idx = stationary_indices(T, mean_block, B, seed)
    flat = (np.arange(B)[:, None] * T + idx).ravel()
    return np.bincount(flat, minlength=B * T).reshape(B, T).astype(np.float64)


def _lrv(u, L):
    """Bartlett long-run variance (per observation) of a demeaned series u with L lags."""
    n = len(u)
    if n < 2:
        return np.nan
    if L <= 40:
        s = u @ u / n
        for k in range(1, min(L, n - 1) + 1):
            s += 2 * (1 - k / (L + 1)) * (u[:-k] @ u[k:]) / n
        return s
    nf = 1 << int(math.ceil(math.log2(2 * n)))
    f = np.fft.rfft(u, nf)
    ac = np.fft.irfft(f * np.conj(f), nf)[: L + 1] / n
    k = np.arange(1, L + 1)
    return ac[0] + 2 * np.sum((1 - k / (L + 1)) * ac[1:])


def nw_ratio(A, N, L):
    """effect = sum(A)/sum(N) per column; Newey-West se from the per-session influence A_d - e N_d (lag L)."""
    A = np.asarray(A, np.float64)
    A = A[:, None] if A.ndim == 1 else A
    tot = N.sum()
    e = A.sum(0) / tot
    z = A - N[:, None] * e
    T = len(N)
    se = np.array([math.sqrt(max(_lrv(z[:, j] - z[:, j].mean(), L), 0) * T) / tot for j in range(A.shape[1])])
    return e, se


def bh(p, dependent=True):
    """Benjamini-Hochberg q-values; dependent=True = Benjamini-Yekutieli (valid under any dependence)."""
    p = np.asarray(p, np.float64)
    out = np.full(len(p), np.nan)
    ok = np.isfinite(p)
    K = int(ok.sum())
    if K == 0:
        return out
    c = np.sum(1.0 / np.arange(1, K + 1)) if dependent else 1.0
    pv = p[ok]
    o = np.argsort(pv)
    raw = pv[o] * K * c / np.arange(1, K + 1)
    adj = np.minimum(1, np.minimum.accumulate(raw[::-1])[::-1])
    q = np.empty(K)
    q[o] = adj
    out[ok] = q
    return out


def romano_wolf_2s(e, eb):
    """Two-sided Romano-Wolf step-down p-values: e (K,), eb (B, K) bootstrap draws on the SAME resamples."""
    e = np.asarray(e, float)
    se = eb.std(0, ddof=1)
    se[~(se > 0)] = np.nan
    t = np.abs(e / se)
    tb = np.abs((eb - e) / se)
    K = len(e)
    p = np.full(K, np.nan)
    good = np.flatnonzero(np.isfinite(t))
    order = good[np.argsort(-t[good])]
    prev = 0.0
    for r, j in enumerate(order):
        mx = np.nanmax(tb[:, order[r:]], axis=1)
        pj = max(prev, float(np.mean(mx >= t[j])))
        p[j] = pj
        prev = pj
    return p


def _p2(z):
    return 2 * norm.sf(np.abs(z))


def _xc(FA, FB, T):
    """circular cross-correlation summed over grid columns: out[k] = sum_{d,s} A[d,s] B[(d+k)%T,s]."""
    return np.fft.irfft((np.conj(FA) * FB).sum(axis=1), n=T)


# ============================================================================================ panel
class Panel:
    """One market x timeframe: forward targets, controls, residualised targets, session bootstrap, placebo FFTs.
    bars: v3 bars frame (index = bar start; O H L C seg session [run trend]) or synthetic_bars() output."""

    def __init__(self, bars, sym, tf, n_boot=1000, block=10.0, seed=0, fe=FE_DEFAULT, fe_iter=6, spec=None):
        t0 = time.time()
        b = bars.sort_index()
        self.bars, self.sym, self.tf = b, sym, int(tf)
        s_ = dict(spec or SPEC[sym])
        self.tick, self.usd, self.cost_usd = float(s_["tick"]), float(s_["usd"]), float(s_["cost"])
        self.cost_pts = self.cost_usd / self.usd
        n = self.n = len(b)
        O, Hh, L, C = (b[c].to_numpy(np.float64) for c in ("O", "H", "L", "C"))
        self.C = C
        seg = b["seg"].to_numpy()
        run = b["run"].to_numpy() if "run" in b.columns else np.zeros(n, np.int64)
        sess = pd.DatetimeIndex(b["session"]).normalize()
        code, uni = pd.factorize(sess, sort=True)
        self.sess_code = code.astype(np.int64)
        self.sessions = pd.DatetimeIndex(uni)
        T = self.T = len(uni)
        idx = np.arange(n)
        last = np.r_[seg[1:] != seg[:-1], True]
        ends = np.flatnonzero(last)
        self.seg_end = seg_end = ends[np.searchsorted(ends, idx)]
        first = np.r_[True, seg[1:] != seg[:-1]]
        self.seg_start = np.maximum.accumulate(np.where(first, idx, 0))
        # R20
        rs = np.r_[True, run[1:] != run[:-1]]
        run_start = np.maximum.accumulate(np.where(rs, idx, 0))
        cs = np.r_[0.0, np.cumsum(Hh - L)]
        r20 = (cs[idx + 1] - cs[np.maximum(idx - 19, 0)]) / 20.0
        r20[idx - run_start < 19] = np.nan
        self.r20 = r20 = np.maximum(r20, 2 * self.tick)
        ok = (idx < seg_end) & np.isfinite(r20)
        self.ok = ok
        nx = np.minimum(idx + 1, n - 1)
        entry = O[nx]
        Y = np.full((n, len(TARGETS)), np.nan)
        hi = np.full(n, -np.inf)
        lo = np.full(n, np.inf)
        for k in range(1, max(HORIZONS) + 1):
            j = np.minimum(idx + k, seg_end)
            hi = np.maximum(hi, Hh[j])
            lo = np.minimum(lo, L[j])
            if k in HORIZONS:
                d = C[j] - entry
                Y[:, COL[f"dir_h{k}"]] = d / r20
                Y[:, COL[f"abs_h{k}"]] = np.abs(d) / r20
                Y[:, COL[f"rng_h{k}"]] = (hi - lo) / r20
        rH = pd.Series(Hh[::-1]).groupby(seg[::-1]).cummax().to_numpy()[::-1]
        rL = pd.Series(L[::-1]).groupby(seg[::-1]).cummin().to_numpy()[::-1]
        d = C[seg_end] - entry
        Y[:, COL["dir_eod"]] = d / r20
        Y[:, COL["abs_eod"]] = np.abs(d) / r20
        Y[:, COL["rng_eod"]] = (rH[nx] - rL[nx]) / r20
        up, dn = entry + r20, entry - r20
        path = np.full(n, 0.5)
        res = np.zeros(n, bool)
        for k in range(1, PATH_H + 1):
            j = np.minimum(idx + k, seg_end)
            hu, hd = Hh[j] >= up, L[j] <= dn
            new = ~res & (hu | hd)
            path[new & hu & ~hd] = 1.0
            path[new & hd & ~hu] = 0.0
            res |= new
        Y[:, COL["path"]] = path - 0.5
        Y[~ok] = np.nan
        self.Y = Y
        self.Y0 = np.nan_to_num(Y)                                     # NaN -> 0 (rows outside `ok`)
        # controls
        ts = b.index
        mins = ((ts.hour * 60 + ts.minute).to_numpy() - 18 * 60) % 1440
        self.pos = (mins // self.tf).astype(np.int64)
        self.P = int(math.ceil(SESSION_MIN / self.tf))
        slot = np.minimum((mins + self.tf) // 15, 91)
        dow = self.sessions.day_of_week.to_numpy()[code]
        self.year_s = self.sessions.year.to_numpy()
        year = self.year_s[code]
        trend = (b["trend"].to_numpy() + 1) if "trend" in b.columns else np.ones(n, np.int64)
        prev = (np.sign(C - O) + 1).astype(np.int64)
        med = pd.Series(r20).rolling(100, min_periods=50).median().to_numpy()
        vr = r20 / med
        qs = np.nanquantile(vr, np.linspace(0.1, 0.9, 9))
        vol = np.where(np.isfinite(vr), np.searchsorted(qs, vr), 10)
        codes = dict(slot=slot, dow=dow, vol=vol, trend=trend, prev=prev, year=year)
        self.groups = []
        for name in fe:
            g = pd.factorize(codes[name])[0]
            self.groups.append(sps.csr_matrix((np.ones(n), (idx, g)), shape=(n, g.max() + 1)))
        self.fe_iter = fe_iter
        self.cell = pd.factorize(slot * 3 + trend)[0]                 # event-study control cell
        self.Yr = self.resid(self.Y, ok)
        self.Smat = sps.csr_matrix((np.ones(n), (idx, self.sess_code)), shape=(n, T))
        yrs = np.unique(self.year_s)
        self.years = yrs
        self.Ymat = sps.csr_matrix((np.ones(T), (np.arange(T), np.searchsorted(yrs, self.year_s))),
                                   shape=(T, len(yrs)))
        self.n_boot = n_boot
        self.counts = boot_counts(T, block, n_boot, seed)
        self.nw_L = nw_lags(T)
        self.flat = self.sess_code * self.P + self.pos
        if len(np.unique(self.flat)) != n:
            raise ValueError("two bars share a (session, time-of-day) slot")
        self._fft = None
        self._es = None
        self._rep = None
        self._perms = {}
        self.shifts = np.arange(MIN_SHIFT, T - MIN_SHIFT + 1) if T > 3 * MIN_SHIFT else np.arange(1, T)
        # interleaved halves (alternate calendar quarters): a second replication split that YM (2018+ only) can use
        qn = self.sessions.year.to_numpy() * 4 + (self.sessions.month.to_numpy() - 1) // 3
        self.qodd_s = (qn % 2 == 1)
        self.build_s = time.time() - t0

    # ---------------------------------------------------------------- v1 additions
    def repair_perms(self, n, seed=0):
        """(n, T) session re-pairings: each session's signal is paired with the prices of a random OTHER session of
        the same calendar year and weekday (main placebo, v1; valid where circular shifts can fail - Harris 2020)."""
        key = (n, seed)
        if key not in self._perms:
            rng = np.random.default_rng(seed + 12345)
            grp = self.year_s * 10 + self.sessions.day_of_week.to_numpy()
            base = np.argsort(grp, kind="stable")
            out = np.empty((n, self.T), np.int64)
            for b in range(n):
                out[b, base] = np.lexsort((rng.random(self.T), grp))
            self._perms[key] = out
        return self._perms[key]

    def rep_cache(self):
        if self._rep is None:
            okf = self.ok.astype(np.float64)
            G = np.zeros((self.T * self.P, len(PLACEBO_COLS)))
            G[self.flat] = self.Yr[:, [COL[c] for c in PLACEBO_COLS]] * okf[:, None]
            isz = np.array([c in SIZE_COLS for c in PLACEBO_COLS])
            OK = np.zeros(self.T * self.P)
            OK[self.flat] = okf
            self._rep = dict(isz=isz, Gd=np.ascontiguousarray(G[:, ~isz]), Gs=np.ascontiguousarray(G[:, isz]),
                             G2=G * G, OK=OK)
        return self._rep

    def injected(self, add, cols=None):
        """Copy of this panel with `add` (n,) R20 added to the direction targets (power by injection into REAL data,
        Brown-Warner style). Residualisation is linear, so Yr gains resid(add) and the full pipeline re-runs."""
        import copy
        cols = [COL[c] for c in (cols or DIR)]
        Q = copy.copy(self)
        a = np.where(self.ok, np.nan_to_num(np.asarray(add, np.float64)), 0.0)
        Q.Y = self.Y.copy()
        Q.Y[:, cols] += a[:, None]
        Q.Y0 = np.nan_to_num(Q.Y)
        Q.Yr = self.Yr.copy()
        Q.Yr[:, cols] += self.resid(a, self.ok)[:, None]
        Q._fft, Q._rep, Q._es = None, None, None
        return Q

    # ---------------------------------------------------------------- helpers
    def resid(self, Y, mask, n_iter=None):
        """Residualise columns of Y on the additive fixed effects over rows `mask` (0 elsewhere)."""
        Y = np.asarray(Y, np.float64)
        one = Y.ndim == 1
        R = Y.reshape(len(Y), -1).copy()
        m = mask.astype(np.float64)
        R[~mask] = 0.0
        R[~np.isfinite(R)] = 0.0
        cnts = [np.maximum(G.T @ m, 1.0) for G in self.groups]
        for _ in range(n_iter or self.fe_iter):
            for G, c in zip(self.groups, cnts):
                mu = (G.T @ R) / c[:, None]
                R -= (G @ mu) * m[:, None]
        return R.ravel() if one else R

    def grid(self, v):
        g = np.zeros(self.T * self.P)
        g[self.flat] = v
        return g.reshape(self.T, self.P)

    def fft_cache(self):
        if self._fft is None:
            okf = self.ok.astype(np.float64)
            FY, FY2 = {}, {}
            for c in PLACEBO_COLS:
                y = self.Yr[:, COL[c]] * okf
                FY[c] = np.fft.rfft(self.grid(y), axis=0)
                FY2[c] = np.fft.rfft(self.grid(y * y), axis=0)
            self._fft = (FY, FY2, np.fft.rfft(self.grid(okf), axis=0))
        return self._fft

    def es_cellmeans(self):
        if self._es is None:
            n = self.n
            K = np.arange(-ES_K, ES_K + 1)
            out = np.zeros((self.cell.max() + 1, len(K)))
            idx = np.arange(n)
            for a, k in enumerate(K):
                j = idx + k
                inside = (j >= self.seg_start) & (j <= self.seg_end) & self.ok
                jj = np.clip(j, 0, n - 1)
                Pk = np.where(inside, (self.C[jj] - self.C) / self.r20, 0.0)
                s = np.bincount(self.cell, weights=Pk, minlength=out.shape[0])
                c = np.bincount(self.cell, weights=inside.astype(float), minlength=out.shape[0])
                out[:, a] = s / np.maximum(c, 1)
            self._es = out
        return self._es

    def es_paths(self, rows):
        K = np.arange(-ES_K, ES_K + 1)
        j = rows[:, None] + K[None, :]
        inside = (j >= self.seg_start[rows][:, None]) & (j <= self.seg_end[rows][:, None])
        jj = np.clip(j, 0, self.n - 1)
        Pm = (self.C[jj] - self.C[rows][:, None]) / self.r20[rows][:, None]
        Pm = Pm - self.es_cellmeans()[self.cell[rows]]
        Pm[~inside] = np.nan
        return Pm

    def hold_label(self, col):
        h = col.split("_")[-1]
        if h == "eod":
            return "to 16:45"
        k = int(h[1:])
        m = k * self.tf
        return f"{k} bar{'s' if k > 1 else ''} ({m} min)" if (m < 60 or m % 60) else \
            f"{k} bar{'s' if k > 1 else ''} ({m // 60} h)"


def repair_placebo(P, wd, ws, m, n_perm=100, seed=0, batch=20):
    """Normalised statistic (same as the circular placebo) for the real pairing (row 0) and n_perm session re-pairings
    within (year, weekday). Returns (n_perm + 1, len(PLACEBO_COLS))."""
    c = P.rep_cache()
    isz = c["isz"]
    allp = np.vstack([np.arange(P.T)[None], P.repair_perms(n_perm, seed)])
    Wd, Ws, M = P.grid(wd), P.grid(ws), P.grid(m)
    same = np.array_equal(wd, ws)
    out = np.empty((len(allp), len(PLACEBO_COLS)))
    w0, ww = Wd.ravel(), max(float(Wd.ravel() @ Wd.ravel()), 1e-300)
    sim = []
    for i0 in range(0, len(allp), batch):
        pp = allp[i0:i0 + batch]
        b = len(pp)
        Y2m = M[pp].reshape(b, -1) @ c["G2"]
        Wp = Wd[pp].reshape(b, -1)
        sim.append((Wp @ w0) / ww)
        d1 = (Wp * Wp) @ c["OK"]
        out[i0:i0 + b, ~isz] = (Wp @ c["Gd"]) / np.sqrt(np.maximum(d1[:, None] * Y2m[:, ~isz], 1e-300))
        if not same:
            Wp = Ws[pp].reshape(b, -1)
            d1 = (Wp * Wp) @ c["OK"]
        out[i0:i0 + b, isz] = (Wp @ c["Gs"]) / np.sqrt(np.maximum(d1[:, None] * Y2m[:, isz], 1e-300))
    repair_placebo.similarity = float(np.mean(np.concatenate(sim)[1:]))   # overlap of re-paired vs real signal
    return out


def _align(P, s):
    if s is None:
        return None
    if isinstance(s, pd.Series):
        return s.reindex(P.bars.index).to_numpy(np.float64)
    a = np.asarray(s, np.float64)
    if len(a) != P.n:
        raise ValueError("signal length != number of bars")
    return a


# ============================================================================================ one metric
def evaluate(P, signal, kind="continuous", side=None, name="metric", n_q=5, placebo=True, power=True, delta=0.05,
             power_col="dir_h4", n_power=40, event_study=True, ic=True, seed=0, desc="", repair=True, n_repair=100,
             check_lookahead=True, la_kw=None):
    """Impact of ONE metric on one Panel. Returns a dict (see module doc); r['table'] has one row per target.
    repair=True runs the session re-pairing placebo (n_repair draws) and includes it in the final p.
    signal may be a function fn(bars) -> Series | (Series, side): it is then truncation-tested for look-ahead
    (r['lookahead']); numbers (array / Series) cannot be tested and are marked UNCHECKED."""
    la = None
    if callable(signal):
        if check_lookahead:
            la = lookahead_check(signal, P.bars, **(la_kw or {}))
        out = signal(P.bars)
        signal, side = (out if isinstance(out, tuple) else (out, side))
    with np.errstate(invalid="ignore", divide="ignore"):
        r = _evaluate(P, signal, kind, side, name, n_q, placebo, power, delta, power_col, n_power, event_study, ic,
                      seed, desc, repair, n_repair)
    r["lookahead"] = la
    return r


def _evaluate(P, signal, kind, side, name, n_q, placebo, power, delta, power_col, n_power, event_study, ic, seed,
              desc, repair=True, n_repair=100):
    t0 = time.time()
    n, T = P.n, P.T
    x = _align(P, signal)
    valid = P.ok & np.isfinite(x)
    m = valid.astype(np.float64)
    if valid.sum() < 50:
        raise ValueError(f"{name}: fewer than 50 usable bars")
    xv = np.nan_to_num(x)
    legs = []
    if kind in ("continuous", "state"):
        vals = x[valid]
        lev = np.unique(vals)
        if len(lev) <= n_q:
            top, bot = valid & (xv == lev[-1]), valid & (xv == lev[0])
        else:
            q = np.quantile(vals, [1.0 / n_q, 1 - 1.0 / n_q])
            top, bot = valid & (xv > q[1]), valid & (xv <= q[0])
            if top.sum() == 0:
                top = valid & (xv >= q[1])
        pt, pb = top.sum() / valid.sum(), bot.sum() / valid.sum()
        wd = top / pt - bot / pb
        ws = wd
        inj = 0.5 * top - 0.5 * bot
        legs = [("top fifth" if len(lev) > n_q else "top level", top, 1.0), ("bottom fifth" if len(lev) > n_q
                                                                            else "bottom level", bot, -1.0)]
        tlegs = [(top, 1.0, 0.5), (bot, -1.0, 0.5)]                   # trades: long top, short bottom (half spread)
    elif kind in ("event", "sided"):
        if kind == "sided":
            sd = np.sign(xv)
            ev = valid & (sd != 0)
        else:
            ev = valid & (xv != 0)
            sd = None
            if side is not None:
                sd = np.sign(np.nan_to_num(_align(P, side)))
                ev &= sd != 0
        non = valid & ~ev
        pe = ev.sum() / valid.sum()
        if ev.sum() < 10:
            raise ValueError(f"{name}: fewer than 10 events")
        ws = ev / pe - non / (1 - pe) if non.any() else np.zeros(n)     # no non-events -> no size contrast
        if sd is None:
            wd, inj = ws, ev.astype(float)
            legs = [("event", ev, 1.0)]
            tlegs = [(ev, 1.0, 1.0)]                                   # trades: every event, one direction
        else:
            wd, inj = sd * ev / pe, sd * ev
            legs = [("event", ev, sd)]
            tlegs = [(ev, sd, 1.0)]                                    # trades: every event in its own side
        top, bot = ev, non
    else:
        raise ValueError(f"unknown kind {kind}")
    wd = np.where(valid, wd, 0.0)
    ws = np.where(valid, ws, 0.0)
    Wcol = np.array([c not in SIZE_COLS for c in TARGETS])            # True -> direction weights
    Nd = P.Smat.T @ m
    A = np.empty((T, len(TARGETS)))
    A[:, Wcol] = P.Smat.T @ (P.Yr[:, Wcol] * wd[:, None])
    A[:, ~Wcol] = P.Smat.T @ (P.Yr[:, ~Wcol] * ws[:, None])
    tot = Nd.sum()
    e = A.sum(0) / tot
    eb = (P.counts @ A) / (P.counts @ Nd)[:, None]
    se_b = eb.std(0, ddof=1)
    _, se_nw = nw_ratio(A, Nd, P.nw_L)
    tab = pd.DataFrame(index=TARGETS)
    tab["effect"] = e
    tab["se_boot"] = se_b
    tab["ci_lo"] = e - 1.96 * se_b
    tab["ci_hi"] = e + 1.96 * se_b
    tab["p_boot"] = _p2(e / se_b)
    tab["se_nw"] = se_nw
    tab["p_nw"] = _p2(e / se_nw)
    # comparison-group raw level (for "% more movement")
    base = bot if kind in ("continuous", "state") else (valid & ~top)
    tab["raw_top"] = (top.astype(float) @ P.Y0) / top.sum() if top.any() else np.nan
    tab["raw_base"] = (base.astype(float) @ P.Y0) / base.sum() if base.any() else np.nan
    allmean = (m @ P.Y0) / m.sum()
    tab["pct_vs_avg"] = np.where([c in SIZE_COLS for c in TARGETS], 100 * e / allmean, np.nan)
    # bar-level diagnostics for direction columns
    tib, tbn = [], []
    for c in TARGETS:
        if c in DIR:
            j = COL[c]
            w = wd
            u = w * P.Yr[:, j] - e[j] * m
            h = c.split("_")[1]
            L = P.P if h == "eod" else int(h[1:])
            tib.append(e[j] / (math.sqrt(u @ u) / tot))
            tbn.append(e[j] / (math.sqrt(max(_lrv(u, L), 0) * n) / tot))
        else:
            tib.append(np.nan)
            tbn.append(np.nan)
    tab["t_iid_bar"] = tib
    tab["t_nw_bar"] = tbn
    # IC (partial rank correlation)
    if ic:
        xr = np.zeros(n)
        rk = (rankdata(x[valid]) - 0.5) / valid.sum()
        xr[valid] = norm.ppf(rk)
        xr = P.resid(xr, valid)
        Yv = P.Yr if valid.sum() == P.ok.sum() else P.Yr * m[:, None]   # Yr is already 0 outside `ok`
        Aic = P.Smat.T @ (Yv * xr[:, None])
        Bx = P.Smat.T @ (xr * xr)
        By = P.Smat.T @ (Yv * Yv)
        icv = Aic.sum(0) / np.sqrt(Bx.sum() * By.sum(0))
        icb = (P.counts @ Aic) / np.sqrt((P.counts @ Bx)[:, None] * (P.counts @ By))
        tab["ic"] = icv
        tab["ic_se"] = icb.std(0, ddof=1)
    # placebo
    if placebo:
        FY, FY2, Fok = P.fft_cache()
        Wd_g, Ws_g, M_g = P.grid(wd), P.grid(ws), P.grid(m)
        F = {k: np.fft.rfft(v, axis=0) for k, v in (("d", Wd_g), ("d2", Wd_g ** 2), ("s", Ws_g), ("s2", Ws_g ** 2),
                                                    ("m", M_g))}
        pz, pe_, zz = [], [], []
        for c in TARGETS:
            if c not in FY:
                pz.append(np.nan); pe_.append(np.nan); zz.append(np.nan)
                continue
            a, a2 = ("s", "s2") if c in SIZE_COLS else ("d", "d2")
            num = _xc(F[a], FY[c], T)
            den = np.sqrt(np.maximum(_xc(F[a2], Fok, T) * _xc(F["m"], FY2[c], T), 1e-300))
            st = num / den
            null = st[P.shifts]
            mu, sd_ = null.mean(), null.std(ddof=1)
            z = (st[0] - mu) / sd_
            zz.append(z)
            pz.append(_p2(z))
            pe_.append((1 + np.sum(np.abs(null - mu) >= abs(st[0] - mu))) / (1 + len(null)))
        tab["z_placebo"] = zz
        tab["p_placebo"] = pz
        tab["p_placebo_emp"] = pe_
    placebo_ok = True
    if repair:                                                         # v1 main placebo: session re-pairing
        st = repair_placebo(P, wd, ws, m, n_repair, seed)
        # a signal that is (nearly) the same every session (pure time-of-day) cannot be judged by moving it to other
        # sessions: the placebo is then marked not applicable and left out of the final p
        placebo_ok = repair_placebo.similarity < 0.9
        null = st[1:]
        mu, sd_ = null.mean(0), null.std(0, ddof=1)
        zr = (st[0] - mu) / sd_
        rep = pd.DataFrame(dict(z_repair=zr, p_repair=_p2(zr),
                                p_repair_emp=(1 + np.sum(np.abs(null - mu) >= np.abs(st[0] - mu), axis=0)) /
                                (1 + len(null))), index=PLACEBO_COLS)
        tab = tab.join(rep)
    # final p: the most conservative of session bootstrap, Newey-West on sessions and the main placebo
    pcols = ["p_boot", "p_nw"] + ((["p_repair"] if repair else (["p_placebo"] if placebo else [])) if placebo_ok
                                  else [])
    if not placebo_ok:
        for c in ("p_repair_emp", "p_placebo_emp"):
            if c in tab:
                tab[c] = np.nan
    tab["p"] = tab[pcols].max(axis=1)
    tab["ci90_lo"] = e - 1.6449 * se_b
    tab["ci90_hi"] = e + 1.6449 * se_b
    # stability: by year, eras
    Ay = P.Ymat.T @ A
    Ny = P.Ymat.T @ Nd
    with np.errstate(invalid="ignore", divide="ignore"):
        ey = Ay / Ny[:, None]
    have = Ny > 0
    same = (np.sign(ey[have]) == np.sign(e)[None, :])
    tab["years_same"] = same.sum(0)
    tab["years_n"] = int(have.sum())
    by_year = pd.DataFrame(ey[have], index=P.years[have], columns=TARGETS)
    for era, (y0, y1) in ERAS.items():
        sel = (P.year_s >= y0) & (P.year_s <= y1)
        if sel.sum() > 20 and Nd[sel].sum() > 0:
            ee, ss = nw_ratio(A[sel], Nd[sel], P.nw_L)
            tab[f"effect_{era}"] = ee
            tab[f"z_{era}"] = ee / ss
        else:
            tab[f"effect_{era}"] = np.nan
            tab[f"z_{era}"] = np.nan
    for half, sel in (("Qodd", P.qodd_s), ("Qeven", ~P.qodd_s)):       # interleaved halves (alternate quarters)
        if sel.sum() > 20 and Nd[sel].sum() > 0:
            ee, ss = nw_ratio(A[sel], Nd[sel], P.nw_L)
            tab[f"effect_{half}"], tab[f"z_{half}"] = ee, ee / ss
        else:
            tab[f"effect_{half}"], tab[f"z_{half}"] = np.nan, np.nan
    # economics (direction columns): best leg per horizon
    econ = []
    era_of = P.year_s[P.sess_code]
    trade_rows = np.zeros(n, bool)
    for mk_, _, _ in tlegs:
        trade_rows |= mk_
    usd_per_r20 = {}         # $ per micro of a 1-R20 move, by era: MEAN R20 of the signal's trades (an edge of e R20 on
    for era, (y0, y1) in ERAS.items():                                 # every trade earns e x mean(R20) x $/pt)
        s_ = trade_rows & (era_of >= y0) & (era_of <= y1)
        usd_per_r20[era] = float(np.mean(P.r20[s_]) * P.usd) if s_.any() else np.nan
    for c in DIR:
        j = COL[c]
        sg = np.sign(e[j]) or 1.0
        best = None
        for lname, lmask, lsign in legs:
            rows = np.flatnonzero(lmask)
            if len(rows) == 0:
                continue
            dirn = (lsign[rows] if isinstance(lsign, np.ndarray) else lsign) * sg
            r20 = P.r20[rows]
            g = dirn * P.Y[rows, j]
            ex = dirn * P.Yr[rows, j]
            row = dict(target=c, hold=P.hold_label(c), leg=lname, trade=("with signal" if sg > 0 else "against signal")
                       if kind == "sided" else ("long" if (np.mean(dirn) > 0) else "short"),
                       n=len(rows), gross_r20=g.mean(), excess_r20=ex.mean(), cost_r20=P.cost_pts / np.mean(r20),
                       gross_usd=np.mean(g * r20 * P.usd), excess_usd=np.mean(ex * r20 * P.usd))
            row["net_usd"] = row["gross_usd"] - P.cost_usd
            row["net_excess_usd"] = row["excess_usd"] - P.cost_usd
            for era, (y0, y1) in ERAS.items():
                s_ = (era_of[rows] >= y0) & (era_of[rows] <= y1)
                row[f"net_usd_{era}"] = np.mean(g[s_] * r20[s_] * P.usd) - P.cost_usd if s_.any() else np.nan
            econ.append(row)
            best = row if best is None or row["net_usd"] > best["net_usd"] else best
    econ = pd.DataFrame(econ)
    # event study
    es = None
    if event_study:
        rng_ = np.random.default_rng(seed)

        def _mean_path(mask, sgn=None, cap=200000):
            rows = np.flatnonzero(mask)
            if len(rows) > cap:
                keep = np.sort(rng_.choice(len(rows), cap, replace=False))
                rows = rows[keep]
            Pm = P.es_paths(rows)
            if sgn is not None:
                Pm = Pm * sgn[rows][:, None]
            return np.nanmean(Pm, axis=0)

        K = np.arange(-ES_K, ES_K + 1)
        if kind in ("continuous", "state"):
            es = pd.Series(_mean_path(top) - _mean_path(bot), index=K)
        elif legs[0][2] is not None and isinstance(legs[0][2], np.ndarray):
            es = pd.Series(_mean_path(top, legs[0][2]), index=K)
        else:
            es = pd.Series(_mean_path(top), index=K)
    # power: inject delta into a copy of the target, aligned with placebo-shifted copies of the signal
    pw = None
    if power and power_col in COL:
        j = COL[power_col]
        okg = P.grid(P.ok.astype(float))
        Yg = P.grid(P.Yr[:, j] * P.ok)
        Wg = P.grid(wd if power_col not in SIZE_COLS else ws)
        Ig, Mg = P.grid(np.where(valid, inj, 0.0)), P.grid(m)
        rng_ = np.random.default_rng(seed + 1)
        ks = rng_.choice(P.shifts, size=min(n_power, len(P.shifts)), replace=False)
        det, ses, bias = [], [], []
        for k in ks:
            Wk, Ik, Mk = (np.roll(v, k, axis=0) for v in (Wg, Ig, Mg))
            Mk = Mk * okg
            A0 = (Wk * Yg).sum(1)
            A1 = A0 + delta * (Wk * Ik * okg).sum(1)
            Nk = Mk.sum(1)
            e0, e1 = A0.sum() / Nk.sum(), A1.sum() / Nk.sum()
            eb1 = (P.counts @ A1) / (P.counts @ Nk)
            s1 = eb1.std(ddof=1)
            ses.append(s1)
            det.append(e1 / s1 > 1.96 if delta > 0 else e1 / s1 < -1.96)
            bias.append(e1 - e0)
        pw = dict(col=power_col, delta=delta, n=len(ks), detect_rate=float(np.mean(det)),
                  mde80=float((1.96 + 0.8416) * np.median(ses)), injected_recovered=float(np.mean(bias)))
    # ---- four-way verdict inputs (v1.1): the PER-TRADE edge in $ per micro, judged against the real $ round-trip cost.
    # Trades (tlegs): continuous/state = long the top fifth/level and short the bottom (edge = half the spread); sided
    # (or event with side) = every event in its side; plain event = every event in one direction. Edge = excess over
    # matched bars (residualised target). Three versions per hold, each with a session-bootstrap se (max with the
    # Newey-West se on sessions):
    #   trade_usd      $ per trade, each trade's R20 edge x ITS OWN R20 x $/pt, full sample
    #   trade_usd_B    the same in 2018-25H1 only (the recent half: what tradability is judged on)
    #   trade_usd_rec  per-trade R20 edge (full sample, most precise) x mean R20 of the signal's trades at recent bar
    #                  sizes (the larger of 2018-25H1 and full sample) x $/pt  = the edge restated at today's bar sizes
    # The break-even edge in R20 is cost / mean R20 (NOT mean of cost / R20, which overstates it 1.3-1.7x).
    four = _trade_edges(P, tlegs, trade_rows, era_of, tab)
    pdir = tab.loc[DIR, "p"]
    psz = tab.loc[ABS, "p"]
    r = dict(name=name, desc=desc, kind=kind, sym=P.sym, tf=P.tf, n_valid=int(valid.sum()), n_top=int(top.sum()),
             n_bot=int(bot.sum()), share_top=float(top.sum() / valid.sum()), table=tab, econ=econ, event_path=es,
             power=pw, by_year=by_year, best_dir=_best(pdir), p_dir=float(min(1.0, len(DIR) * pdir.min())),
             best_size=_best(psz), p_size=float(min(1.0, len(ABS) * psz.min())),
             p_path=float(tab.loc["path", "p"]), usd_per_r20=usd_per_r20, A_dir=A[:, [COL[c] for c in DIR]].copy(),
             eb_dir=eb[:, [COL[c] for c in DIR]].copy(), Nd=Nd, seconds=time.time() - t0, **four)
    return r


def _leg_edge(P, tlegs, wt, sel=None):
    """Per-trade edge over the direction holds: sum_k c_k x (sum over leg-k trades of side x Yr x wt) / n_k.
    sel (T,) bool restricts to those sessions. Returns (est (6,), se (6,)) with se = max(session stationary bootstrap,
    Newey-West on the per-session influence)."""
    dcols = [COL[c] for c in DIR]
    T = P.T
    est = np.zeros(len(dcols))
    boot = np.zeros((P.n_boot, len(dcols)))
    infl = np.zeros((T, len(dcols)))
    cnt = P.counts if sel is None else P.counts * sel[None, :]
    for mask, sgn, c in tlegs:
        s = np.where(mask, np.asarray(sgn, np.float64) * wt, 0.0)        # NaN weights outside the trades -> 0
        Ak = P.Smat.T @ (P.Yr[:, dcols] * s[:, None])
        Nk = P.Smat.T @ mask.astype(np.float64)
        if sel is not None:
            Ak, Nk = Ak * sel[:, None], Nk * sel
        tot = Nk.sum()
        if tot <= 0:
            return np.full(len(dcols), np.nan), np.full(len(dcols), np.nan)
        ek = Ak.sum(0) / tot
        est += c * ek
        boot += c * (cnt @ Ak) / np.maximum(cnt @ Nk, 1e-12)[:, None]
        infl += c * (Ak - Nk[:, None] * ek) / tot
    rows = np.arange(T) if sel is None else np.flatnonzero(sel)
    se_nw = np.array([math.sqrt(max(_lrv(infl[rows, j] - infl[rows, j].mean(), P.nw_L), 0) * len(rows))
                      for j in range(len(dcols))])
    return est, np.maximum(boot.std(0, ddof=1), se_nw)


def _trade_edges(P, tlegs, trade_rows, era_of, tab):
    """Four-way verdict inputs in $ per micro per trade (see the comment in _evaluate). Adds per-hold columns to tab
    and returns the per-metric dict merged into the result."""
    y0, y1 = ERAS["2018-25H1"]
    selB = (P.year_s >= y0) & (P.year_s <= y1)
    rowsB = trade_rows & (era_of >= y0) & (era_of <= y1)
    w_usd = P.r20 * P.usd
    e_r, s_r = _leg_edge(P, tlegs, np.ones(P.n))
    e_u, s_u = _leg_edge(P, tlegs, w_usd)
    e_b, s_b = _leg_edge(P, tlegs, w_usd, selB) if rowsB.any() else (np.full(len(DIR), np.nan),) * 2
    usd_all = float(np.mean(w_usd[trade_rows])) if trade_rows.any() else np.nan
    usd_B = float(np.mean(w_usd[rowsB])) if rowsB.any() else np.nan
    usd_rec = float(np.nanmax([usd_all, usd_B]))                        # $ per R20 at recent (larger) bar sizes
    cost = P.cost_usd
    z90 = 1.6449
    rec_lo, rec_hi = usd_rec * (e_r - z90 * s_r), usd_rec * (e_r + z90 * s_r)
    dir_lo, dir_hi = e_u - z90 * s_u, e_u + z90 * s_u
    ci_max = np.maximum(np.maximum(np.abs(rec_lo), np.abs(rec_hi)), np.maximum(np.abs(dir_lo), np.abs(dir_hi)))
    point = np.maximum(np.abs(usd_rec * e_r), np.abs(e_u))
    inside = ci_max < cost
    nh = np.array([c in NOTHING_HOLDS for c in DIR])                  # CI test: holds of 1-8 bars
    long_ok = point[~nh] < cost                                        # 16-bar / to-16:45: best estimate below cost
    # how many times more data would put the 1-8 bar CIs inside the cost (binding version and hold)
    need = []
    for est, se in ((usd_rec * e_r, usd_rec * s_r), (e_u, s_u)):
        gap = cost - np.abs(est)
        need.append(np.where(gap > 0, (z90 * se / np.maximum(gap, 1e-12)) ** 2, np.inf))
    need = np.maximum(need[0], need[1])
    for k, v in (("trade_edge_r20", e_r), ("trade_edge_r20_se", s_r), ("trade_usd", e_u), ("trade_usd_se", s_u),
                 ("trade_usd_B", e_b), ("trade_usd_B_se", s_b), ("trade_usd_rec", usd_rec * e_r),
                 ("trade_usd_rec_lo90", rec_lo), ("trade_usd_rec_hi90", rec_hi), ("edge_usd_ci90_max", ci_max)):
        tab[k] = np.nan
        tab.loc[DIR, k] = v
    tab["edge_ci90_max"] = np.nan                                      # same, in R20 at recent bar sizes
    tab.loc[DIR, "edge_ci90_max"] = ci_max / usd_rec
    be = cost / usd_rec
    return dict(cost_usd=cost, usd_per_r20_trades=usd_all, usd_per_r20_trades_B=usd_B, usd_per_r20_recent=usd_rec,
                breakeven_r20=be, cost_r20=be, cost_margin=be,
                cost_r20_B=cost / usd_B if np.isfinite(usd_B) else np.nan,
                dir_inside_cost=bool(inside[nh].all() and long_ok.all()), long_holds_below_cost=bool(long_ok.all()),
                n_holds_inside=int(inside.sum()), holds_inside=[c for c, i in zip(DIR, inside) if i],
                edge_usd_ci90_max_h1_8=float(ci_max[nh].max()),
                data_needed_x=float(need[nh].max()) if long_ok.all() else np.inf)


def _best(p):
    return p.idxmin() if p.notna().any() else p.index[0]


# ============================================================================================ look-ahead check
def _as_xs(out):
    if isinstance(out, tuple):
        return [np.asarray(o, np.float64) for o in out]
    return [np.asarray(out, np.float64)]


def _signal_rows(xs, n_q=5):
    """Rows where the metric 'says something': for an output with <= n_q distinct values (event / sided / state) every
    row that differs from its most common value; otherwise the top and bottom fifth. A leak in a yes/no event changes
    the value ONLY on these rows, so the truncation test must cut exactly there."""
    rows = []
    for a in xs:
        fin = np.isfinite(a)
        v = a[fin]
        if not len(v):
            continue
        lev, cnt = np.unique(v, return_counts=True)
        if len(lev) <= n_q:
            rows.append(np.flatnonzero(fin & (a != lev[np.argmax(cnt)])))
        else:
            q = np.quantile(v, [1.0 / n_q, 1 - 1.0 / n_q])
            rows.append(np.flatnonzero(fin & ((a <= q[0]) | (a > q[1]))))
    return np.unique(np.concatenate(rows)) if rows else np.zeros(0, np.int64)


def lookahead_check(fn, bars, n_target=40, n_random=60, seed=0, lo=0.2, budget_s=120.0, n_cuts=None):
    """TRUNCATION TEST for peeking at the future. fn(bars) values at rows <= a cut row c must be identical when fn only
    sees bars.iloc[:c+1] (= what was known at bar c's close).
    Cuts (v1.1): n_target rows drawn from the metric's OWN signal rows (event / non-default level / top or bottom
    fifth, see _signal_rows) - a leak in a rare yes/no metric changes the value only there - plus n_random uniform
    rows (leaks that create events where the full data has none, whole-sample statistics, centred windows).
    If one full call times (n_target + n_random) would exceed budget_s, the test runs on the most recent bars only
    (a property of fn, valid on any contiguous stretch; at least 20,000 bars).
    A crash of fn on a truncated frame counts as a failure (the metric cannot be shown to be causal).
    Returns dict(ok, status 'passed'|'FAILED', n_cuts, n_target, n_random, n_bad, n_bad_target, n_bad_random,
    first_bad, n_rows, n_signal_rows)."""
    if n_cuts is not None:                                             # old signature: n_cuts random cuts only
        n_random, n_target = int(n_cuts), 0
    rng = np.random.default_rng(seed)
    t0 = time.time()
    full = _as_xs(fn(bars))
    t_one = time.time() - t0
    n = len(bars)
    if t_one * (n_target + n_random) > budget_s and n > 20000:
        keep = max(20000, int(n * budget_s / (t_one * (n_target + n_random))))
        bars = bars.iloc[n - keep:]
        n = len(bars)
        full = _as_xs(fn(bars))
    lo_i, hi_i = int(lo * n), n - 2                                    # leave at least one future bar after the cut
    sig = _signal_rows(full)
    sig = sig[(sig >= lo_i) & (sig <= hi_i)]
    tgt = np.sort(rng.choice(sig, min(n_target, len(sig)), replace=False)) if len(sig) else np.zeros(0, np.int64)
    rnd = np.sort(rng.integers(lo_i, hi_i + 1, n_random)) if n_random else np.zeros(0, np.int64)
    cuts = [(int(c), "target") for c in tgt] + [(int(c), "random") for c in rnd]
    bad = {"target": 0, "random": 0}
    first_bad, bad_rows = None, []
    for c, src in cuts:
        try:
            cut = _as_xs(fn(bars.iloc[: c + 1]))
        except Exception as err:                                       # noqa: BLE001 - any crash = cannot verify
            bad[src] += 1
            first_bad = first_bad or f"{bars.index[c]} (fn crashed on truncated data: {type(err).__name__})"
            continue
        for a, b in zip(full, cut):
            if len(b) != c + 1 or not np.allclose(a[: c + 1], b, rtol=1e-7, atol=1e-9, equal_nan=True):
                bad[src] += 1
                diff = ~np.isclose(a[: c + 1], b[: c + 1] if len(b) > c else np.r_[b, [np.nan] * (c + 1 - len(b))],
                                   rtol=1e-7, atol=1e-9, equal_nan=True)
                where = str(bars.index[int(np.flatnonzero(diff)[0])]) if diff.any() else "length"
                bad_rows.append(where)
                first_bad = first_bad or where
                break
    nb = bad["target"] + bad["random"]
    return dict(ok=nb == 0, status="passed" if nb == 0 else "FAILED", n_cuts=len(cuts), n_target=len(tgt),
                n_random=len(rnd), n_bad=nb, n_bad_target=bad["target"], n_bad_random=bad["random"],
                first_bad=first_bad, bad_rows=bad_rows[:5], n_rows=n, n_signal_rows=int(len(sig)),
                seconds=round(time.time() - t0, 2))


def lookahead_status(la):
    """'passed' / 'FAILED' / 'UNCHECKED' (metric given as numbers, not as a function the lab can re-run)."""
    if not la:
        return "UNCHECKED"
    return "passed" if la.get("ok") else "FAILED"


# ============================================================================================ batch
def evaluate_many(signals, panels=None, markets=("ES", "NQ", "YM"), tfs=(15,), check_lookahead=True, la_kw=None,
                  out_dir=None, write=True, verbose=True, q_disc=0.10, n_power=20, log_tag=None, panel_kw=None,
                  **kw):
    """signals: {name: dict(fn=callable(bars) -> Series | (Series, side), kind=..., desc=...)} or {name: (array, kind)}
    when `panels` is given. panels: optional {(sym, tf): Panel}; otherwise panels are built one at a time from
    harness.bars. Returns (batch DataFrame one row per metric x market x tf, list of result dicts).
    Look-ahead: every callable metric is truncation-tested once (on the first panel; la_kw -> lookahead_check). A
    FAILED test overrides every verdict to INVALID; a metric given as numbers is marked UNCHECKED on its card."""
    results, checked = [], {}
    keys = list(panels.keys()) if panels else [(s, tf) for s in markets for tf in tfs]
    for sym, tf in keys:
        t0 = time.time()
        P = panels[(sym, tf)] if panels else Panel(H.bars(sym, tf), sym, tf, **(panel_kw or {}))
        if verbose:
            print(f"[lab] panel {sym} {tf}m: {P.n} bars, {P.T} sessions, built in {P.build_s:.1f}s", flush=True)
        for name, spec in signals.items():
            if isinstance(spec, dict):
                fn, kind = spec["fn"], spec.get("kind", "continuous")
                out = fn(P.bars) if callable(fn) else fn
                if check_lookahead and callable(fn) and name not in checked:    # a property of fn: once per metric
                    checked[name] = lookahead_check(fn, P.bars, **(la_kw or {}))
                    if verbose and not checked[name]["ok"]:
                        print(f"[lab]   {name}: LOOK-AHEAD FAILED at {checked[name]['first_bad']} -> verdicts INVALID")
                la = checked.get(name)
                desc = spec.get("desc", "")
            else:
                out, kind = spec[0], spec[1]
                la, desc = None, ""
            x, side = (out if isinstance(out, tuple) else (out, None))
            try:
                r = evaluate(P, x, kind, side=side, name=name, desc=desc, n_power=n_power, **kw)
            except ValueError as err:
                if verbose:
                    print(f"[lab]   {name}: skipped ({err})")
                continue
            r["lookahead"] = la
            results.append(r)
        if verbose:
            print(f"[lab] panel {sym} {tf}m done: {len(signals)} metrics in {time.time() - t0:.1f}s", flush=True)
        if not panels:
            del P
    batch = batch_table(results, q_disc=q_disc)
    if write:
        write_outputs(batch, results, out_dir or OUT)
    if log_tag:
        log_trials(batch, log_tag)
    return batch, results


def log_trials(batch, tag):
    """Append one row per (metric, market, tf) to out/trials.csv (run_pipeline.log_trial, module 'v3-lab-<tag>'):
    every metric looked at counts toward the data-snooping tally."""
    import json
    import run_pipeline as rp
    for _, r in batch.iterrows():
        rp.log_trial(module=f"v3-lab-{tag}", scope=MICRO.get(r.market, r.market), model=f"signal_lab {r.metric}",
                     target=f"{r.best_dir}|{r.best_size}", oos_rows=int(r.n),
                     parameters=json.dumps(dict(tf=int(r.tf), kind=r.kind, dir_effect_r20=round(float(r.dir_effect), 5),
                                                p_dir=float(r.p_dir), q_dir=float(r.q_dir),
                                                size_pct=round(float(r.size_pct), 2), q_size=float(r.q_size))),
                     note=f"signal lab v1.1: dir={r.dir_verdict} class={r.get('dir_class', '')} size={r.size_verdict} "
                          f"lookahead={r.get('lookahead', 'UNCHECKED')}")


def batch_table(results, q_disc=0.10):
    rows = []
    for r in results:
        t = r["table"]
        bd, bs = r["best_dir"], r["best_size"]
        rows.append(dict(metric=r["name"], kind=r["kind"], market=r["sym"], tf=r["tf"], n=r["n_valid"],
                         n_top=r["n_top"], best_dir=bd, dir_effect=t.at[bd, "effect"], dir_lo=t.at[bd, "ci_lo"],
                         dir_hi=t.at[bd, "ci_hi"], dir_ic=t.at[bd, "ic"] if "ic" in t else np.nan, p_dir=r["p_dir"],
                         dir_placebo_emp=t.at[bd, "p_placebo_emp"] if "p_placebo_emp" in t else np.nan,
                         dir_years_same=int(t.at[bd, "years_same"]), years_n=int(t.at[bd, "years_n"]),
                         dir_eff_A=t.at[bd, "effect_2010-17"], dir_z_A=t.at[bd, "z_2010-17"],
                         dir_eff_B=t.at[bd, "effect_2018-25H1"], dir_z_B=t.at[bd, "z_2018-25H1"],
                         best_size=bs, size_effect=t.at[bs, "effect"], size_lo=t.at[bs, "ci_lo"],
                         size_hi=t.at[bs, "ci_hi"], size_pct=t.at[bs, "pct_vs_avg"], p_size=r["p_size"],
                         size_years_same=int(t.at[bs, "years_same"]),
                         size_placebo_emp=t.at[bs, "p_placebo_emp"] if "p_placebo_emp" in t else np.nan,
                         path_effect=t.at["path", "effect"],
                         p_path=r["p_path"], mde80=(r["power"] or {}).get("mde80", np.nan),
                         power_rate=(r["power"] or {}).get("detect_rate", np.nan),
                         lookahead_ok=(r.get("lookahead") or {}).get("ok", np.nan)))
    B = pd.DataFrame(rows)
    if B.empty:
        return B
    q = bh(np.r_[B.p_dir.to_numpy(), B.p_size.to_numpy()], dependent=True)
    B["q_dir"], B["q_size"] = q[: len(B)], q[len(B):]
    # Romano-Wolf per panel over metric x direction horizon
    B["rw_dir"] = np.nan
    for (sym, tf), g in B.groupby(["market", "tf"]):
        ii = list(g.index)
        e = np.concatenate([results[i]["table"].loc[DIR, "effect"].to_numpy() for i in ii])
        eb = np.concatenate([results[i]["eb_dir"] for i in ii], axis=1)
        prw = romano_wolf_2s(e, eb).reshape(len(ii), len(DIR))
        B.loc[ii, "rw_dir"] = np.nanmin(prw, axis=1)
    # halves: discovery in one half, confirmation in the other (both ways). Chronological halves (2010-17 /
    # 2018-25H1) when the metric has data in both; otherwise (YM: 2018+ only) interleaved halves (odd / even quarters)
    chrono_ok = np.array([np.isfinite(r["table"].loc[DIR, "z_2010-17"].to_numpy()).any() and
                          np.isfinite(r["table"].loc[DIR, "z_2018-25H1"].to_numpy()).any() for r in results])
    B["rep_split"] = np.where(chrono_ok, "chronological", "interleaved quarters")
    rep_any = np.zeros(len(B), bool)
    for halves, use in ((list(ERAS), chrono_ok), (["Qodd", "Qeven"], ~chrono_ok)):
        ph = {}
        for era in halves:
            pz = np.array([np.nanmin(_p2(r["table"].loc[DIR, f"z_{era}"].to_numpy())) * len(DIR)
                           if np.isfinite(r["table"].loc[DIR, f"z_{era}"].to_numpy()).any() else np.nan for r in results])
            ph[era] = np.where(use, np.minimum(pz, 1), np.nan)
        for a, b_ in ((halves[0], halves[1]), (halves[1], halves[0])):
            qa = bh(ph[a], dependent=True)
            conf = []
            for i, r in enumerate(results):
                t = r["table"].loc[DIR]
                za = t[f"z_{a}"].to_numpy()
                if not use[i] or not np.isfinite(qa[i]) or qa[i] >= q_disc or not np.isfinite(za).any():
                    conf.append(False)
                    continue
                j = int(np.nanargmax(np.abs(za)))
                zb = t[f"z_{b_}"].to_numpy()[j]
                conf.append(bool(np.isfinite(zb) and np.sign(zb) == np.sign(za[j]) and norm.sf(abs(zb)) < 0.05))
            B[f"q_{a}"] = qa
            B[f"rep_{a[:5]}to{b_[:5]}"] = conf
            rep_any |= np.array(conf, bool)
    B["replicated"] = rep_any
    # economics of the recent half (2018-25H1) at the best hold, in $ per micro per trade (v1.1): the per-trade edge
    # (each trade's excess R20 move x its own R20 x $/pt, session bootstrap) and its lower 80% bound vs the real cost
    eB_, lo80 = [], []
    for i, r in enumerate(results):
        t = r["table"]
        bd = r["best_dir"]
        sg = np.sign(t.at[bd, "effect"]) or 1.0
        eB = t.at[bd, "trade_usd_B"] if "trade_usd_B" in t else np.nan
        seB = t.at[bd, "trade_usd_B_se"] if "trade_usd_B_se" in t else np.nan
        eB_.append(sg * eB)
        lo80.append(sg * eB - 1.2816 * seB)
    B["edge_usd_B"] = eB_
    B["edge_usd_B_lo80"] = lo80
    B["edge_usd_rec"] = [abs(r["table"].at[r["best_dir"], "trade_usd_rec"]) if "trade_usd_rec" in r["table"] else
                         np.nan for r in results]
    B["cost_usd"] = [r.get("cost_usd", np.nan) for r in results]
    B["breakeven_r20"] = [r.get("breakeven_r20", np.nan) for r in results]
    B["cost_r20"] = B["breakeven_r20"]
    B["edge_usd_ci90_max_h1_8"] = [r.get("edge_usd_ci90_max_h1_8", np.nan) for r in results]
    B["dir_inside_cost"] = [r.get("dir_inside_cost", False) for r in results]
    B["data_needed_x"] = [r.get("data_needed_x", np.nan) for r in results]
    B["dir_placebo_repair_emp"] = [r["table"].at[r["best_dir"], "p_repair_emp"] if "p_repair_emp" in r["table"]
                                   else np.nan for r in results]
    B["size_placebo_repair_emp"] = [r["table"].at[r["best_size"], "p_repair_emp"] if "p_repair_emp" in r["table"]
                                    else np.nan for r in results]
    B["lookahead"] = [lookahead_status(r.get("lookahead")) for r in results]
    B["dir_verdict"] = [_dir_status(row) for _, row in B.iterrows()]
    B["size_verdict"] = [_size_status(row) for _, row in B.iterrows()]
    B["dir_class"] = [_dir_class(row) for _, row in B.iterrows()]
    # a FAILED look-ahead test overrides everything: the numbers describe the future, not the metric
    bad = B.lookahead.eq("FAILED")
    B.loc[bad, ["dir_verdict", "size_verdict"]] = "INVALID"
    B.loc[bad, "dir_class"] = INVALID_CLASS
    return B


INVALID_CLASS = "INVALID (LOOK-AHEAD)"
UNCHECKED_TAG = " (look-ahead UNCHECKED)"


def _dir_class(row):
    """FOUR-WAY direction verdict (v1.1): the per-trade edge in $ per micro against the real $ round-trip cost.
    REAL & TRADABLE   CONFIRMED and, in 2018-25H1, the lower 80% bound of the $ edge per trade (each trade's excess
                       move x its own bar size, session bootstrap) is above the round-trip cost
    REAL BUT TOO SMALL CONFIRMED, but not clearly above cost (usable as a filter / for sizing only)
    CONFIDENTLY NOTHING not confirmed; at every hold of 1, 2, 4 and 8 bars the 90% range of the $ edge per trade sits
                       inside +-cost (both as measured in $ and restated at recent bar sizes), and at the 16-bar and
                       to-16:45 holds the best estimate is below the cost
    INCONCLUSIVE       anything else (data_needed_x = how many times more data would settle it)
    A REAL class on a metric the lab could not truncation-test (given as numbers) carries ' (look-ahead UNCHECKED)'."""
    if row.dir_verdict == "CONFIRMED":
        tr = np.isfinite(row.edge_usd_B_lo80) and np.isfinite(row.cost_usd) and row.edge_usd_B_lo80 > row.cost_usd
        cls = "REAL & TRADABLE" if tr else "REAL BUT TOO SMALL"
        return cls + (UNCHECKED_TAG if row.get("lookahead", "UNCHECKED") == "UNCHECKED" else "")
    if row.dir_inside_cost:
        return "CONFIDENTLY NOTHING"
    return "INCONCLUSIVE"


def _size_status(row):
    share = row.size_years_same / max(row.years_n, 1)
    pl = row.size_placebo_repair_emp if np.isfinite(row.size_placebo_repair_emp) else (
        row.size_placebo_emp if np.isfinite(row.size_placebo_emp) else 0.0)
    if row.q_size < 0.05 and pl < 0.05 and share >= 0.6:
        return "CONFIRMED"
    if row.q_size < 0.10 or row.p_size < 0.01:
        return "possible"
    return "none"


def _dir_status(row):
    share = row.dir_years_same / max(row.years_n, 1)
    pl = row.dir_placebo_repair_emp if np.isfinite(row.dir_placebo_repair_emp) else (
        row.dir_placebo_emp if np.isfinite(row.dir_placebo_emp) else 0.0)
    if row.q_dir < 0.05 and row.replicated and pl < 0.05 and share >= 0.6:
        return "CONFIRMED"
    if row.q_dir < 0.10 or row.p_dir < 0.01:
        return "possible"
    return "none"


# ============================================================================================ impact card
def _f(x, d=3):
    return "n/a" if x is None or not np.isfinite(x) else f"{x:+.{d}f}"


def _g(x, fmt=".3g"):
    return "" if x is None or not np.isfinite(x) else format(x, fmt)


def verdict_lines(r, brow=None):
    """Plain one-liners for one result (one market x tf)."""
    t = r["table"]
    sym, tf = r["sym"], r["tf"]
    mk = f"{MICRO.get(sym, sym)} {tf}-min"
    single = brow is None
    if single:                                   # one metric alone: a batch of one (q = p, halves test included)
        brow = batch_table([r]).iloc[0]
    bd = r["best_dir"]
    e = t.at[bd, "effect"]
    hold = _hold(bd, tf)
    who = {"continuous": "top fifth vs bottom fifth of the metric", "state": "top level vs bottom level",
           "event": "after the event vs matched non-events", "sided": "in the signal's direction"}[r["kind"]]
    status = brow["dir_verdict"]
    qtxt = f"q={brow['q_dir']:.3g}" + (" (single metric, q = p)" if single else "")
    ys = f"{int(t.at[bd, 'years_same'])} of {int(t.at[bd, 'years_n'])} years"
    econ = r["econ"]
    eb = econ[econ.target == bd].sort_values("net_usd", ascending=False).head(1)
    money = ""
    if len(eb):
        x = eb.iloc[0]
        money = (f"; best leg ({x['leg']}, {x['trade']}) grosses ${x['gross_usd']:+.2f} and nets ${x['net_usd']:+.2f} "
                 f"per micro per trade after ${r_cost(sym):.2f} costs")
        tradable = (x["net_usd"] > 0 and np.nan_to_num(x.get("net_usd_2010-17"), nan=-1) > 0
                    and np.nan_to_num(x.get("net_usd_2018-25H1"), nan=-1) > 0 and status == "CONFIRMED")
        money += " -> tradable on its own" if tradable else " -> not tradable on its own"
    upr = r.get("usd_per_r20", {}).get("2018-25H1", np.nan)
    usd_txt = f" (~${abs(e) * upr:.2f} per micro at 2018-25 bar sizes)" if np.isfinite(upr) else ""
    if r["kind"] in ("continuous", "state") and np.isfinite(upr):
        usd_txt = (f" (top-minus-bottom spread ~${abs(e) * upr:.2f}; ~${abs(e) * upr / 2:.2f} per trade when trading "
                   "both ends, at 2018-25 bar sizes)")
    up = "up" if e > 0 else "down"
    if r["kind"] == "sided":
        up = "in the signal's favour" if e > 0 else "AGAINST the signal"
    if status == "CONFIRMED":
        dline = (f"{mk}: moves price {up} {abs(e):.3f} average bars{usd_txt} over {hold} ({who}), same sign in {ys}, "
                 f"{qtxt}{money}.")
    elif status == "possible":
        dline = (f"{mk}: POSSIBLE direction effect {e:+.3f} average bars{usd_txt} over {hold} ({who}), not confirmed "
                 f"({qtxt}, replicated in the other half={bool(brow['replicated'])}, {ys}){money}.")
    else:
        mde = (r["power"] or {}).get("mde80", np.nan)
        dline = (f"{mk}: no measurable direction effect (best {e:+.3f} R20 over {hold}, p={r['p_dir']:.2g}"
                 + (f"; we would catch an effect of {mde:.3f} R20 or more 80% of the time" if np.isfinite(mde) else "")
                 + ").")
    bs = r["best_size"]
    es_, pct = t.at[bs, "effect"], t.at[bs, "pct_vs_avg"]
    sstat = brow["size_verdict"]
    if sstat in ("CONFIRMED", "possible"):
        swho = {"continuous": "in the metric's top fifth than in its bottom fifth",
                "state": "at the top level than at the bottom level"}.get(r["kind"], "after the event than after matched bars")
        sline = (f"{mk} size: the market moves {abs(pct):.0f}% {'MORE' if es_ > 0 else 'LESS'} {swho} "
                 f"over {_hold(bs, tf)} ({es_:+.3f} R20, {sstat}, "
                 f"q={brow['q_size']:.3g},"
                 f" {int(t.at[bs, 'years_same'])} of {int(t.at[bs, 'years_n'])} years same sign).")
    else:
        sline = f"{mk} size: no measurable effect on how much price moves (best p={r['p_size']:.2g})."
    la = r.get("lookahead")
    las = lookahead_status(la)
    if status == "INVALID":
        bad = (la or {}).get("first_bad")
        msg = (f"{mk}: INVALID - the metric FAILED the look-ahead test (its value at {bad} changes when the bars after "
               "it are removed), so it uses information from after the bar's close. Every number on this card "
               "measures that peek, not the metric. Fix the metric and re-run.")
        return [msg, f"{mk} BOTTOM LINE (direction): {INVALID_CLASS} - see above. {calib_status(sym, tf)}"]
    out = [dline, sline]
    cls = brow.get("dir_class") if hasattr(brow, "get") else None
    if cls:
        cost = r.get("cost_usd", r_cost(sym))
        be = r.get("breakeven_r20", np.nan)
        bd_ = r["best_dir"]
        eB, lo80 = brow.get("edge_usd_B", np.nan), brow.get("edge_usd_B_lo80", np.nan)
        e_rec = t.at[bd_, "trade_usd_rec"] if "trade_usd_rec" in t else np.nan
        edge_max = r.get("edge_usd_ci90_max_h1_8", np.nan)
        dn = r.get("data_needed_x", np.nan)
        dn_txt = (f"about {dn:.1f}x more data would settle it" if np.isfinite(dn) else
                  "the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short "
                  "holds alone will not settle it")
        base = cls.replace(UNCHECKED_TAG, "")
        expl = {"REAL & TRADABLE": f"the effect is confirmed and, in 2018-25H1, its per-trade edge is ${eB:+.2f} per "
                                   f"micro with a pessimistic (lower 80%) value of ${lo80:+.2f}, above the "
                                   f"${cost:.2f} round trip",
                "REAL BUT TOO SMALL": f"the effect is confirmed but its 2018-25H1 per-trade edge (${eB:+.2f}, "
                                      f"pessimistic ${lo80:+.2f}) does not clearly beat the ${cost:.2f} round trip: "
                                      "use it as a filter or for sizing only",
                "CONFIDENTLY NOTHING": f"at every hold of 1-8 bars the 90% range of the per-trade edge is at most "
                                       f"${math.floor(edge_max * 100) / 100:.2f} per micro (at recent bar sizes), "
                                       f"inside the ${cost:.2f} "
                                       f"round trip (break-even {be:.3f} R20), and longer holds are below it too: "
                                       "whatever the true effect is, it cannot pay for the trade",
                "INCONCLUSIVE": f"not confirmed, but the data cannot rule out a per-trade edge as big as the ${cost:.2f} "
                                f"round trip (best hold now ${abs(e_rec):.2f} at recent bar sizes, 90% range up to "
                                f"${edge_max:.2f}); {dn_txt}"}
        warn = ""
        if las == "UNCHECKED":
            warn = (" WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for "
                    "peeking at the future; pass it as a function fn(bars) to get it checked.")
        out.append(f"{mk} BOTTOM LINE (direction): {cls} - {expl[base]}.{warn} {calib_status(sym, tf)}")
    return out


CALIB_FILE = os.path.join(OUT, "calibration", "self_test_status.json")


def calib_status(sym, tf):
    """One line from the real-data self-test (calibrate_lab.py): PASSED / FAILED / UNCALIBRATED for this panel."""
    try:
        import json
        with open(CALIB_FILE) as f:
            st = json.load(f).get(f"{sym} {int(tf)}")
    except Exception:
        st = None
    if not st:
        return "Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py)."
    return (f"Lab self-test for this market/timeframe: {'PASSED' if st.get('passed') else 'FAILED'} "
            f"({st.get('date', '?')}; false-positive rate {st.get('fpr_dir', float('nan')):.1%} at p<0.05, "
            f"80%-detectable effect {st.get('mde80_rare', float('nan')):.3f} R20 for ~1 event/session).")


def r_cost(sym):
    return SPEC[sym]["cost"]


def _la_text(la):
    s = lookahead_status(la)
    if s == "UNCHECKED":
        return "UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it)"
    if s == "FAILED":
        return (f"FAILED at {la.get('first_bad')} ({la.get('n_bad')} of {la.get('n_cuts')} cuts changed earlier "
                "values) -> all verdicts INVALID")
    return (f"passed ({la.get('n_cuts')} cuts, {la.get('n_target')} of them on the metric's own signal bars, over "
            f"{la.get('n_rows')} bars; the check tests the metric's code, so a batch runs it once, on its first "
            "market / timeframe)")


def _hold(col, tf):
    h = col.split("_")[-1]
    if h == "eod":
        return "the rest of the session (to 16:45)"
    k = int(h[1:])
    m = k * tf
    return f"the next {k} bar{'s' if k > 1 else ''} ({m} min)" if (m < 60 or m % 60) else \
        f"the next {k} bar{'s' if k > 1 else ''} ({m // 60} h)"


_ORDER = {"ES": 0, "NQ": 1, "YM": 2}


def render_card(name, results, batch):
    """Markdown impact card for one metric over all its (market, tf) results."""
    rs = sorted([r for r in results if r["name"] == name], key=lambda r: (_ORDER.get(r["sym"], 9), r["tf"]))
    if not rs:
        return ""
    bsub = batch[batch.metric == name].set_index(["market", "tf"])
    L = [f"# Impact card: {name}", ""]
    if rs[0]["desc"]:
        L += [rs[0]["desc"], ""]
    L += [f"Kind: {rs[0]['kind']}. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. "
          "Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, "
          "last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is "
          "a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. "
          "Data 2010 - 2025-06-30 (locked holdout untouched).", "", "## Verdict", ""]
    for r in rs:
        br = bsub.loc[(r["sym"], r["tf"])] if (r["sym"], r["tf"]) in bsub.index else None
        for line in verdict_lines(r, br):
            L.append(f"- {line}")
    L += ["", "## Direction (does price go further up or down than usual?)", "",
          "| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | "
          "years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        t = r["table"]
        br = bsub.loc[(r["sym"], r["tf"])] if (r["sym"], r["tf"]) in bsub.index else None
        for c in DIR:
            star = " *" if c == r["best_dir"] else ""
            L.append(f"| {MICRO.get(r['sym'], r['sym'])} | {r['tf']} | {c.split('_')[1]}{star} | {_f(t.at[c, 'effect'])} | "
                     f"{_f(t.at[c, 'ci_lo'])} .. {_f(t.at[c, 'ci_hi'])} | {_f(t.at[c, 'ic'] if 'ic' in t else np.nan, 4)} | "
                     f"{t.at[c, 'p_boot']:.2g} / {t.at[c, 'p_nw']:.2g} / {t.at[c, 'p_placebo'] if 'p_placebo' in t else np.nan:.2g} | "
                     f"{t.at[c, 'p_placebo_emp'] if 'p_placebo_emp' in t else np.nan:.3g} | "
                     f"{_g(br['q_dir'] if (br is not None and star) else np.nan)} | "
                     f"{_g(br['rw_dir'] if (br is not None and star) else np.nan)} | "
                     f"{int(t.at[c, 'years_same'])}/{int(t.at[c, 'years_n'])} | {_f(t.at[c, 'effect_2010-17'])} | "
                     f"{_f(t.at[c, 'effect_2018-25H1'])} | {bool(br['replicated']) if (br is not None and star) else ''} | "
                     f"{t.at[c, 't_iid_bar']:+.1f} / {t.at[c, 'effect'] / t.at[c, 'se_boot']:+.1f} | "
                     f"{_g((r['power'] or {}).get('mde80', np.nan) if c == (r['power'] or {}).get('col') else np.nan, '.3f')} |")
    L += ["", "## Size (does price move MORE, either way?)", "",
          "| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        t = r["table"]
        br = bsub.loc[(r["sym"], r["tf"])] if (r["sym"], r["tf"]) in bsub.index else None
        for ca, cr in zip(ABS, RNG):
            star = " *" if ca == r["best_size"] else ""
            L.append(f"| {MICRO.get(r['sym'], r['sym'])} | {r['tf']} | {ca.split('_')[1]}{star} | {_f(t.at[ca, 'effect'])} | "
                     f"{_f(t.at[ca, 'ci_lo'])} .. {_f(t.at[ca, 'ci_hi'])} | {t.at[ca, 'pct_vs_avg']:+.1f}% | "
                     f"{_f(t.at[cr, 'effect'])} | {t.at[ca, 'p']:.2g} | "
                     f"{_g(br['q_size'] if (br is not None and star) else np.nan)} | "
                     f"{int(t.at[ca, 'years_same'])}/{int(t.at[ca, 'years_n'])} |")
    L += ["", "## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)", "",
          "| market | tf | change in probability | 95% CI | p |", "|---|---|---|---|---|"]
    for r in rs:
        t = r["table"]
        L.append(f"| {MICRO.get(r['sym'], r['sym'])} | {r['tf']} | {100 * t.at['path', 'effect']:+.2f} pts | "
                 f"{100 * t.at['path', 'ci_lo']:+.2f} .. {100 * t.at['path', 'ci_hi']:+.2f} | {t.at['path', 'p']:.2g} |")
    L += ["", "## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)", "",
          f"| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | "
          "net $ 2018-25H1 | signal-only $ net |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        ec = r["econ"]
        if ec is None or ec.empty:
            continue
        for c in DIR:
            x = ec[ec.target == c].sort_values("net_usd", ascending=False).head(1)
            if not len(x):
                continue
            x = x.iloc[0]
            L.append(f"| {MICRO.get(r['sym'], r['sym'])} | {r['tf']} | {c.split('_')[1]} | {x['leg']} | {x['trade']} | "
                     f"{int(x['n'])} | {x['gross_r20']:+.3f} | {x['cost_r20']:.3f} | {x['gross_usd']:+.2f} | "
                     f"{x['net_usd']:+.2f} | {x['net_usd_2010-17']:+.2f} | {x['net_usd_2018-25H1']:+.2f} | "
                     f"{x['net_excess_usd']:+.2f} |")
    L += ["", "## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)", ""]
    ks = [-16, -8, -4, -2, -1, 0, 1, 2, 4, 8, 16]
    L += ["| market | tf | " + " | ".join(f"{k:+d}" for k in ks) + " |", "|---|---|" + "---|" * len(ks)]
    for r in rs:
        es = r["event_path"]
        if es is None:
            continue
        L.append(f"| {MICRO.get(r['sym'], r['sym'])} | {r['tf']} | " + " | ".join(f"{es.get(k, np.nan):+.3f}" for k in ks) + " |")
    L += ["", "## Calibration", ""]
    for r in rs:
        pw, la = r["power"] or {}, r.get("lookahead") or {}
        L.append(f"- {MICRO.get(r['sym'], r['sym'])} {r['tf']}-min: {r['n_valid']} bars, {r['n_top']} in the signal group; "
                 f"power: a true {pw.get('delta', np.nan):.3f} R20 effect at {pw.get('col', '')} is detected "
                 f"{100 * pw.get('detect_rate', np.nan):.0f}% of the time (recovered {pw.get('injected_recovered', np.nan):.3f}); "
                 f"look-ahead truncation check: {_la_text(r.get('lookahead'))}.")
    L += ["", "How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's "
          "favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = "
          "Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in "
          "one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping "
          "returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.", ""]
    return "\n".join(L)


def write_outputs(batch, results, out_dir):
    os.makedirs(os.path.join(out_dir, "cards"), exist_ok=True)
    batch.to_csv(os.path.join(out_dir, "batch_summary.csv"), index=False)
    for name in batch.metric.unique():
        md = render_card(name, results, batch)
        safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in name)
        with open(os.path.join(out_dir, "cards", f"{safe}.md"), "w") as f:
            f.write(md)
        rows = []
        for r in results:
            if r["name"] != name:
                continue
            t = r["table"].copy()
            t.insert(0, "target", t.index)
            t.insert(0, "tf", r["tf"])
            t.insert(0, "market", r["sym"])
            rows.append(t)
        pd.concat(rows).to_csv(os.path.join(out_dir, "cards", f"{safe}.csv"), index=False)


# ============================================================================================ synthetic data
def synthetic_bars(n_sessions=400, tf=15, seed=0, start="2017-01-02", sub=6, vol_cluster=0.0, u_shape=0.0,
                   extra_ret=None, vol_mult=None, base_vol=1.0):
    """Synthetic bars with the v3 bar columns (one contract, 18:00-16:45 sessions). Each bar = `sub` Gaussian steps.
    extra_ret (n,) is added to each bar's return (spread over its steps); vol_mult (n,) scales a bar's steps.
    vol_cluster in [0, 1): AR(1) persistence of log session volatility; u_shape: intraday volatility smile."""
    P = int(math.ceil(SESSION_MIN / tf))
    days = pd.bdate_range(start, periods=n_sessions)
    n = n_sessions * P
    rng = np.random.default_rng(seed)
    lv = np.zeros(n_sessions)
    eps = rng.standard_normal(n_sessions)
    for t in range(1, n_sessions):
        lv[t] = vol_cluster * lv[t - 1] + math.sqrt(1 - vol_cluster ** 2) * 0.4 * eps[t] if vol_cluster > 0 else 0.0
    pos = np.tile(np.arange(P), n_sessions)
    s_i = np.repeat(np.arange(n_sessions), P)
    sig = base_vol * np.exp(lv)[s_i] * (1 + u_shape * np.cos(2 * np.pi * pos / P))
    steps = rng.standard_normal((n, sub)) * (sig / math.sqrt(sub))[:, None]
    if vol_mult is not None:
        steps *= np.asarray(vol_mult, float)[:, None]
    if extra_ret is not None:
        steps += (np.asarray(extra_ret, float) / sub)[:, None]
    cp = np.cumsum(steps, axis=1)
    ret = cp[:, -1]
    C = 1000.0 + np.cumsum(ret)
    O = C - ret
    Hh = O + np.maximum(cp.max(1), 0)
    Lw = O + np.minimum(cp.min(1), 0)
    ts = (days[s_i] - pd.Timedelta(hours=6)) + pd.to_timedelta(pos * tf, unit="m")
    b = pd.DataFrame(dict(O=O, H=Hh, L=Lw, C=C, V=1.0), index=pd.DatetimeIndex(ts, name="ts"))
    b["sess"] = days[s_i]
    b["inst"] = 1
    b["seg"] = s_i + 1
    b["run"] = 1
    b["session"] = days[s_i]
    tp = (b.H + b.L + b.C) / 3
    b["vwap"] = tp.groupby(s_i).cumsum().to_numpy() / (pos + 1)
    for s in (8, 20, 50):
        b[f"ema{s}"] = b.C.ewm(span=s, adjust=False).mean()
    b["mom14"] = 100 * b.C / b.C.shift(14)
    b["atr14"] = (b.H - b.L).rolling(14).mean()
    b["trend"] = np.select([(b.ema8 > b.ema20) & (b.ema20 > b.ema50), (b.ema8 < b.ema20) & (b.ema20 < b.ema50)],
                           [1, -1], 0).astype(np.int8)
    return b


# ============================================================================================ smoke run on real data
def _smoke(tfs=(15,), markets=("ES",), log=True):
    def ema_gap(b):
        return (b.C - b.ema20) / b.atr14

    def mom(b):
        return b.mom14 - 100.0

    def above_vwap(b):
        return (b.C > b.vwap).astype(float).where(b.vwap.notna())

    def big_bar(b):
        r = (b.H - b.L)
        avg = r.groupby(b.run).transform(lambda s: s.rolling(20, min_periods=20).mean().shift(1))
        return pd.Series(np.where(r > 2 * avg, np.sign(b.C - b.O), 0.0), index=b.index).where(avg.notna())

    sig = {"ema20_gap": dict(fn=ema_gap, kind="continuous", desc="(close - EMA20) / ATR14"),
           "momentum14": dict(fn=mom, kind="continuous", desc="Momentum(14) - 100"),
           "above_vwap": dict(fn=above_vwap, kind="state", desc="close above session VWAP (1) or below (0)"),
           "big_bar_follow": dict(fn=big_bar, kind="sided", desc="bar range > 2x its 20-bar average; side = bar colour")}
    t0 = time.time()
    batch, res = evaluate_many(sig, markets=markets, tfs=tfs, out_dir=os.path.join(OUT, "smoke"),
                               log_tag="smoke" if log else None)
    print(batch[["metric", "market", "tf", "best_dir", "dir_effect", "p_dir", "q_dir", "dir_verdict", "best_size",
                 "size_pct", "q_size", "size_verdict"]].to_string())
    for r in res:
        print(f"{r['name']} {r['sym']} {r['tf']}: {r['seconds']:.1f}s")
    print(f"total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "smoke":
        tfs = tuple(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 else (15,)
        mk = tuple(sys.argv[3].split(",")) if len(sys.argv) > 3 else ("ES",)
        _smoke(tfs, mk, log="nolog" not in sys.argv)
