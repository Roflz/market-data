#!/usr/bin/env python3
"""
P2. Last-half-hour momentum signed by the prior-close-to-15:30 return
(Gao, Han, Li & Zhou [1]; Baltussen, Da, Lammers & Martens [2]; decay evidence [3]).
Specification: literature_report.md section 7, "P2." (pre-registered; no parameter tuning).

Signal    r_d = C(15:29 bar, day d) / C(prior session's 15:59 bar) - 1, both from the SAME contract (unadjusted).
          The contract traded on day d = instrument_id of its 09:30 bar. If the prior session's close bar belongs to
          another contract (first day after a roll; the new contract's prior close is not in the continuous file),
          the day is skipped and counted. If the prior session was an early-close day, its close anchor is the
          12:59 bar close (cash close 13:00; there is no 15:59 bar). The signal includes the overnight session.
Trade     side = sign(r_d) (r_d = 0 -> no trade). Entry at the 15:30 bar open, 1 tick adverse; exit at the 15:59
          bar close, 1 tick adverse. One trade per day per market per variant. Early-close days excluded.
Variants  (a) unconditional;
          (b) only when RV(09:30-09:59) = sqrt(sum of the 30 squared 1-min log returns, 09:30 open .. 09:59 close)
              is in the top tercile of its expanding distribution over all prior sessions (250-session burn-in);
          (c) only on scheduled FOMC statement days (data/fomc_dates.csv, scheduled == True) and CPI release days
              (data/cpi_dates.csv);
          (d) only when RSI(5) of daily closes known at the prior close (Wilder smoothing of within-contract daily
              close-to-close % returns; the roll-day return is unavailable and skipped) is in the bottom tercile of
              its expanding distribution over all prior sessions (250-session burn-in).
Eras      PRIMARY 2020-06-01 .. 2026-11-06; SEC1 2010-06-07 .. 2013-12-31; SEC2 2014-01-01 .. 2020-05-31.
Stats     day-level net $ per micro with Newey-West (5 lags) t on a calendar of all sessions of the era from the
          first day the variant's filter exists (no-trade days = 0). Holm over the 8 primary tests, BY over the 16
          secondary cells (two-sided normal p from the NW t on net $).
Controls  random direction at the same decision times with identical fills (one fixed-seed coin flip per
          market-day, shared by all variants; plus 1000 coin-flip and 1000 side-permutation replications);
          long and short legs against the always-long 15:30-16:00 drift on all eligible days.
Diagnostics (not used for selection): signal-size quintiles [3]; next-open reversal of the 15:30-16:00 move [74];
          per volatility tercile (common protocol: trailing 20-day RV of 5-min RTH returns, known at prior close);
          circuit-breaker days excluded by the abnormal-gap rule; unscheduled FOMC actions.

Costs (fixed): MES $5/pt, MNQ $2/pt, tick 0.25; each market fill 1 tick adverse; $1.00 per round trip per micro.

Run:  cd <project> && PYTHONPATH=./pylib python3 lit_p2_lasthalfhour.py
"""
import os
import time

import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data')
OUT_TRADES = os.path.join(BASE, 'lit_p2_lasthalfhour_trades.csv')
OUT_SUMMARY = os.path.join(BASE, 'lit_p2_lasthalfhour_summary.txt')

MARKETS = ['ES', 'NQ']
MULT = {'ES': 5.0, 'NQ': 2.0}          # MES / MNQ dollars per point
MICRO = {'ES': 'MES', 'NQ': 'MNQ'}
TICK = 0.25
COMM = 1.00                             # per round trip per micro
SLIP_TICKS = 1                          # per market fill
RT_COST = {m: 2 * SLIP_TICKS * TICK * MULT[m] + COMM for m in MARKETS}   # MES $3.50, MNQ $2.00

RTH_START_MIN = 9 * 60 + 30             # 09:30 ET -> slot 0
N_SLOTS = 390                           # 09:30 .. 15:59 bars
SIG_SLOT = 359                          # 15:29 bar close = "the price at 15:30"
ENTRY_SLOT = 360                        # 15:30 bar open
EXIT_SLOT = 389                         # 15:59 bar close
EARLY_CLOSE_SLOT = 209                  # 12:59 bar close = cash close on early-close days (prior-close anchor only)
RV_N = 30                               # 09:30 .. 09:59 bars
HOLIDAY_LAST_SLOT_MAX = 219             # last RTH bar before 13:10 -> cash-market holiday (Globex-only session)
EARLY_LAST_SLOT_MAX = 329               # last RTH bar 13:10..14:59 -> standard early close (cash close 13:00)
ABNORMAL_GAP_MIN = 10                   # a run of > 10 missing RTH minutes = abnormal gap -> excluded (section 5.6)
BURN_IN = 250
RSI_N = 5
NW_LAGS = 5
N_RAND_REPS = 1000
SEED = 20261108
N_TRIALS_DSR = 1042                     # ~1,000 earlier configurations + 26 primary + 16 secondary (preregistration)

VARIANTS = ['a', 'b', 'c', 'd']
VDESC = {'a': 'unconditional',
         'b': 'RV 09:30-09:59 top tercile',
         'c': 'FOMC statement / CPI days',
         'd': 'RSI(5) bottom tercile'}
ERAS = [('PRIMARY', '2020-06-01', '2026-11-30'),
        ('SEC1', '2010-06-01', '2013-12-31'),
        ('SEC2', '2014-01-01', '2020-05-31')]
PERIODS = ERAS + [('ALL', '2010-06-01', '2026-11-30')]
PERIOD_LABEL = {'PRIMARY': 'PRIMARY 2020-06 .. 2026-11', 'SEC1': 'SECONDARY 2010-06 .. 2013-12',
                'SEC2': 'SECONDARY 2014-01 .. 2020-05', 'ALL': 'ALL 2010-06 .. 2026-11 (information)'}


# ----------------------------------------------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------------------------------------------
def load_market(mkt, log):
    t0 = time.time()
    df = pd.read_csv(os.path.join(DATA, f'{mkt}_fut_1m.csv'))
    ts = pd.to_datetime(df['ts_event'], utc=True).dt.tz_convert('America/New_York')
    mins = (ts.dt.hour * 60 + ts.dt.minute).to_numpy()
    keep = (mins >= RTH_START_MIN) & (mins < RTH_START_MIN + N_SLOTS)
    df = df.loc[keep].reset_index(drop=True)
    ts = ts[keep].reset_index(drop=True)
    slot = mins[keep] - RTH_START_MIN
    day = ts.dt.tz_localize(None).dt.normalize().to_numpy()
    udays, didx = np.unique(day, return_inverse=True)
    nd = len(udays)
    O = np.full((nd, N_SLOTS), np.nan)
    C = O.copy()
    INST = np.full((nd, N_SLOTS), -1, dtype=np.int64)
    O[didx, slot] = df['Open'].to_numpy(float)
    C[didx, slot] = df['Close'].to_numpy(float)
    INST[didx, slot] = df['instrument_id'].to_numpy(np.int64)
    present = ~np.isnan(C)
    first_slot = np.argmax(present, axis=1)
    last_slot = N_SLOTS - 1 - np.argmax(present[:, ::-1], axis=1)
    max_gap = np.zeros(nd, dtype=int)
    for i in range(nd):
        p = np.flatnonzero(present[i])
        max_gap[i] = int(np.diff(p).max()) - 1 if len(p) > 1 else 0
    log.append(f'{mkt}: loaded {len(df):,} RTH bars (09:30-15:59) on {nd} dates in {time.time() - t0:.1f}s')
    return dict(dates=pd.to_datetime(udays), O=O, C=C, INST=INST, present=present,
                first_slot=first_slot, last_slot=last_slot, max_gap=max_gap)


def expanding_tercile(x, burn=BURN_IN):
    """Tercile (1..3) of x[i] against all earlier non-NaN values x[j], j < i, once >= burn of them exist."""
    n = len(x)
    terc = np.full(n, np.nan)
    q1s = np.full(n, np.nan)
    q2s = np.full(n, np.nan)
    hist = []
    for i in range(n):
        v = x[i]
        if np.isnan(v):
            continue
        if len(hist) >= burn:
            q1, q2 = np.quantile(hist, [1 / 3, 2 / 3])
            terc[i] = 1 + int(v > q1) + int(v > q2)
            q1s[i], q2s[i] = q1, q2
        hist.append(v)
    return terc, q1s, q2s


def wilder_rsi(r, n=RSI_N):
    """Wilder RSI(n) of a return series; NaN returns (roll days) are skipped and the state carries forward."""
    out = np.full(len(r), np.nan)
    seed = []
    ag = al = np.nan
    for i, x in enumerate(r):
        if not np.isnan(x):
            g, l = max(x, 0.0), max(-x, 0.0)
            if len(seed) < n:
                seed.append((g, l))
                if len(seed) == n:
                    ag = np.mean([s[0] for s in seed])
                    al = np.mean([s[1] for s in seed])
            else:
                ag = (ag * (n - 1) + g) / n
                al = (al * (n - 1) + l) / n
        if not np.isnan(ag):
            out[i] = 50.0 if ag + al == 0 else (100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al))
    return out


def prepare(mkt, raw, log, fomc_sched, cpi_days, rng_side):
    dates_all = raw['dates']
    hol = raw['last_slot'] <= HOLIDAY_LAST_SLOT_MAX
    log.append(f'{mkt}: {int(hol.sum())} cash-market holiday dates (Globex-only session, last RTH bar before 13:10) '
               f'removed from the session calendar: ' + ', '.join(dates_all[hol].strftime('%Y-%m-%d')))
    keep = ~hol
    dates = dates_all[keep]
    O, C, INST, PRES = (raw[k][keep] for k in ('O', 'C', 'INST', 'present'))
    first_slot, last_slot, max_gap = (raw[k][keep] for k in ('first_slot', 'last_slot', 'max_gap'))
    n = len(dates)

    early = last_slot < EXIT_SLOT
    irregular = early & (last_slot > EARLY_LAST_SLOT_MAX)
    log.append(f'{mkt}: {n} RTH sessions; {int(early.sum())} early-close days (last RTH bar before 15:59) '
               f'excluded from trading: ' + ', '.join(dates[early].strftime('%Y-%m-%d')))
    if irregular.any():
        log.append(f'{mkt}: WARNING {int(irregular.sum())} of them end 15:00-15:58 (not a standard 13:15 close): '
                   + ', '.join(dates[irregular].strftime('%Y-%m-%d')))
    if (first_slot != 0).any():
        log.append(f'{mkt}: {int((first_slot != 0).sum())} sessions without a 09:30 bar: '
                   + ', '.join(dates[first_slot != 0].strftime('%Y-%m-%d')))

    # contract of the day = instrument at the 09:30 bar (first RTH bar if 09:30 is missing)
    rows = np.arange(n)
    inst0 = INST[rows, first_slot]
    multi = np.array([len(np.unique(INST[i, PRES[i]])) > 1 for i in range(n)])
    if multi.any():
        log.append(f'{mkt}: {int(multi.sum())} sessions with more than one instrument inside RTH (skipped): '
                   + ', '.join(dates[multi].strftime('%Y-%m-%d')))

    # session close anchor: 15:59 bar (full day), 12:59 bar (standard early close), last bar (irregular)
    close_slot = np.where(~early, EXIT_SLOT, np.where(irregular, last_slot, EARLY_CLOSE_SLOT))
    close_slot = np.minimum(close_slot, last_slot)
    Cff = pd.DataFrame(C).ffill(axis=1).to_numpy()
    sclose = Cff[rows, close_slot]
    close_inst = np.array([INST[i, np.flatnonzero(PRES[i, :close_slot[i] + 1])[-1]] for i in range(n)])
    prev_close = np.r_[np.nan, sclose[:-1]]
    prev_inst = np.r_[-1, close_inst[:-1]]
    prev_date = pd.DatetimeIndex([pd.NaT]).append(dates[:-1])
    prev_early = np.r_[False, early[:-1]]
    no_prior = np.zeros(n, dtype=bool)
    no_prior[0] = True
    roll_skip = (~no_prior) & (inst0 != prev_inst)

    # missing-minute handling: carry the last close forward (prices), as in section 5.6
    miss = ~PRES
    Off = O.copy()
    Off[miss] = Cff[miss]
    for slot, nm in [(SIG_SLOT, '15:29'), (ENTRY_SLOT, '15:30'), (EXIT_SLOT, '15:59')]:
        m = miss[:, slot] & ~early
        if m.any():
            log.append(f'{mkt}: {int(m.sum())} full sessions with no {nm} bar (last close carried forward): '
                       + ', '.join(dates[m].strftime('%Y-%m-%d')))
    p1529 = Cff[:, SIG_SLOT]
    e_ref = Off[:, ENTRY_SLOT]
    x_ref = Cff[:, EXIT_SLOT]
    sig = p1529 / prev_close - 1.0
    side = np.sign(sig)
    abnormal = max_gap > ABNORMAL_GAP_MIN

    # (b) RV 09:30-09:59 from 1-minute log returns: log(C0/O0), log(C_k/C_{k-1}), k = 1..29
    lr = np.concatenate([np.log(Cff[:, :1] / O[:, :1]), np.diff(np.log(Cff[:, :RV_N]), axis=1)], axis=1)
    rv30 = np.sqrt((lr ** 2).sum(1))           # NaN if the 09:30 bar is missing
    rv_terc, rv_q1, rv_q2 = expanding_tercile(rv30)

    # (d) RSI(5) of daily closes, within contract, known at the prior close
    r_daily = np.where((~no_prior) & (close_inst == prev_inst), sclose / prev_close - 1.0, np.nan)
    rsi_close = wilder_rsi(r_daily)
    rsi_prior = np.r_[np.nan, rsi_close[:-1]]
    rsi_terc, rsi_q1, rsi_q2 = expanding_tercile(rsi_prior)

    # common-protocol volatility regime: trailing 20-day RV of 5-min RTH log returns, known at the prior close
    grid = np.arange(4, N_SLOTS, 5)
    px = np.concatenate([O[:, :1], Cff[:, grid]], axis=1)
    lr5 = np.diff(np.log(px), axis=1)
    lr5[early[:, None] & (grid[None, :] > EARLY_CLOSE_SLOT)] = 0.0
    rv5 = np.nansum(lr5 ** 2, axis=1)
    vol20 = np.sqrt(252.0 * pd.Series(rv5).rolling(20).mean().shift(1).to_numpy())
    vol_terc, _, _ = expanding_tercile(vol20)

    # events
    fomc = dates.isin(fomc_sched)
    cpi = dates.isin(cpi_days)

    # next RTH session open (same contract) for the next-open reversal diagnostic
    next_open = np.r_[O[1:, 0], np.nan]
    next_inst = np.r_[inst0[1:], -1]
    next_open = np.where(next_inst == close_inst, next_open, np.nan)

    # eligibility (base = variant a), with exclusion accounting in order
    reasons = []
    excl = np.zeros(n, dtype=bool)
    for nm, m in [('no prior session in the file', no_prior),
                  ('early-close day', early),
                  ('first day after a roll (no same-contract prior close)', roll_skip),
                  ('abnormal RTH gap (> 10 missing minutes)', abnormal),
                  ('more than one contract inside RTH', multi),
                  ('missing price', ~np.isfinite(sig) | ~np.isfinite(e_ref) | ~np.isfinite(x_ref)),
                  ('zero signal return (no side)', side == 0)]:
        new = m & ~excl
        reasons.append((nm, int(new.sum()), dates[new]))
        excl |= m
    base = ~excl

    sess = pd.DataFrame({
        'date': dates, 'early': early, 'abnormal': abnormal, 'max_gap': max_gap, 'roll_skip': roll_skip,
        'no_prior': no_prior, 'multi': multi, 'inst': inst0, 'prev_date': prev_date, 'prev_close': prev_close,
        'prev_early': prev_early, 'p1529': p1529, 'sig': sig, 'side': side, 'e_ref': e_ref, 'x_ref': x_ref,
        'rv30': rv30, 'rv_terc': rv_terc, 'rv_q2': rv_q2, 'rsi_prior': rsi_prior, 'rsi_terc': rsi_terc,
        'rsi_q1': rsi_q1, 'vol20': vol20, 'vol_terc': vol_terc, 'fomc': fomc, 'cpi': cpi,
        'next_open': next_open, 'base': base,
        'rand_side': rng_side.choice([-1, 1], size=n)})
    sess['year'] = sess['date'].dt.year
    sess['elig_a'] = base
    sess['elig_b'] = base & (sess['rv_terc'] == 3)
    sess['elig_c'] = base & (fomc | cpi)
    sess['elig_d'] = base & (sess['rsi_terc'] == 1)
    # first session on which each variant's filter is defined (calendar start for the day-level t-stats)
    first = {'a': dates[1], 'c': dates[1],
             'b': dates[np.flatnonzero(~np.isnan(rv_terc))[0]],
             'd': dates[np.flatnonzero(~np.isnan(rsi_terc))[0]]}
    return sess, reasons, first


def build_trades(mkt, sess, v):
    s = sess.loc[sess[f'elig_{v}']].copy()
    M = MULT[mkt]
    side = s['side'].to_numpy()
    e_ref = s['e_ref'].to_numpy()
    x_ref = s['x_ref'].to_numpy()
    raw = x_ref - e_ref
    t = pd.DataFrame({'date': s['date'].to_numpy(), 'market': mkt, 'variant': v})
    t['era'] = np.select([(t['date'] >= pd.Timestamp(a)) & (t['date'] <= pd.Timestamp(b)) for _, a, b in ERAS],
                         [e for e, _, _ in ERAS], default='')
    t['side'] = np.where(side > 0, 'long', 'short')
    t['side_n'] = side
    t['entry_time'] = t['date'] + pd.Timedelta(hours=15, minutes=30)
    t['entry_price'] = e_ref + side * TICK * SLIP_TICKS
    t['exit_time'] = t['date'] + pd.Timedelta(hours=16)        # close of the 15:59 bar
    t['exit_price'] = x_ref - side * TICK * SLIP_TICKS
    t['gross_points'] = side * raw
    t['gross_usd'] = t['gross_points'] * M
    t['gross_bp'] = 1e4 * side * (x_ref / e_ref - 1.0)
    t['net_points'] = side * (t['exit_price'].to_numpy() - t['entry_price'].to_numpy())
    t['net_usd'] = t['net_points'] * M - COMM
    t['net_bp'] = 1e4 * t['net_usd'] / (e_ref * M)
    t['win'] = t['net_usd'] > 0
    t['entry_ref_price'] = e_ref
    t['exit_ref_price'] = x_ref
    t['contract_id'] = s['inst'].to_numpy()
    t['prior_close_date'] = s['prev_date'].to_numpy()
    t['prior_close'] = s['prev_close'].to_numpy()
    t['prior_close_is_1259'] = s['prev_early'].to_numpy()
    t['price_1530'] = s['p1529'].to_numpy()
    t['signal_bp'] = 1e4 * s['sig'].to_numpy()
    t['rv30_bp'] = 1e4 * s['rv30'].to_numpy()
    t['rv30_tercile'] = s['rv_terc'].to_numpy()
    t['rsi5_prior_close'] = s['rsi_prior'].to_numpy()
    t['rsi5_tercile'] = s['rsi_terc'].to_numpy()
    t['vol20_tercile'] = s['vol_terc'].to_numpy()
    t['fomc_day'] = s['fomc'].to_numpy()
    t['cpi_day'] = s['cpi'].to_numpy()
    rs = s['rand_side'].to_numpy()
    t['rand_side'] = np.where(rs > 0, 'long', 'short')
    t['rand_side_n'] = rs
    t['rand_gross_points'] = rs * raw
    t['rand_gross_usd'] = t['rand_gross_points'] * M
    t['rand_gross_bp'] = 1e4 * rs * (x_ref / e_ref - 1.0)
    t['rand_net_usd'] = (rs * raw - 2 * TICK * SLIP_TICKS) * M - COMM
    t['rand_net_bp'] = 1e4 * t['rand_net_usd'] / (e_ref * M)
    t['raw_move_points'] = raw
    t['move_bp'] = 1e4 * (x_ref / e_ref - 1.0)
    nopen = s['next_open'].to_numpy()
    t['next_open'] = nopen
    t['next_open_side_bp'] = 1e4 * side * (nopen / x_ref - 1.0)
    t['next_open_ret_bp'] = 1e4 * (nopen / x_ref - 1.0)
    t['year'] = t['date'].dt.year
    for c in t.columns:
        if t[c].dtype == float:
            t[c] = t[c] + 0.0                                    # turn -0.0 into 0.0
    return t


# ----------------------------------------------------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------------------------------------------------
def nw_t(x, lags=NW_LAGS):
    x = np.asarray(x, float)
    T = len(x)
    if T < 3:
        return np.nan
    e = x - x.mean()
    lrv = e @ e / T
    for l in range(1, lags + 1):
        lrv += 2.0 * (1.0 - l / (lags + 1.0)) * (e[l:] @ e[:-l]) / T
    se = np.sqrt(lrv / T) if lrv > 0 else 0.0
    return x.mean() / se if se > 0 else np.nan


def p_two(t):
    return 2.0 * stats.norm.sf(abs(t)) if np.isfinite(t) else np.nan


def holm(p):
    p = np.asarray(p, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (m - k) * p[i]))
        adj[i] = run
    return adj


def by_adjust(p):
    p = np.asarray(p, float)
    m = len(p)
    c = np.sum(1.0 / np.arange(1, m + 1))
    order = np.argsort(p)[::-1]
    adj = np.empty(m)
    run = 1.0
    for k, i in enumerate(order):
        rank = m - k
        run = min(run, min(1.0, p[i] * m * c / rank))
        adj[i] = run
    return adj


def dsr(x, n_trials=N_TRIALS_DSR):
    """Deflated Sharpe ratio (Bailey & Lopez de Prado) of a daily series; null SR variance approximated by 1/T."""
    x = np.asarray(x, float)
    T = len(x)
    sd = x.std(ddof=1)
    if T < 10 or sd == 0:
        return np.nan
    sr = x.mean() / sd
    g3 = stats.skew(x)
    g4 = stats.kurtosis(x, fisher=False)
    em = 0.5772156649
    sr0 = np.sqrt(1.0 / T) * ((1 - em) * stats.norm.ppf(1 - 1.0 / n_trials)
                              + em * stats.norm.ppf(1 - 1.0 / (n_trials * np.e)))
    den = 1 - g3 * sr + (g4 - 1) / 4.0 * sr ** 2
    return stats.norm.cdf((sr - sr0) * np.sqrt(T - 1) / np.sqrt(den)) if den > 0 else np.nan


def day_series(tr, col, cal):
    return tr.groupby('date')[col].sum().reindex(cal, fill_value=0.0).to_numpy()


def sharpe(x):
    sd = np.std(x, ddof=1)
    return np.sqrt(252) * np.mean(x) / sd if sd > 0 else np.nan


def years_positive(tr, col, two_year=False):
    key = ((tr['year'] - 2010) // 2) if two_year else tr['year']
    g = tr.groupby(key)[col].agg(['count', 'mean'])
    g = g[g['count'] >= 20]
    return int((g['mean'] > 0).sum()), len(g)


def stats_block(tr, cal, rand=False, two_year=False):
    """Per-trade and day-level statistics; rand=True uses the random-direction control columns."""
    pre = 'rand_' if rand else ''
    col = pre + 'net_usd'
    n = len(tr)
    out = dict(trades=n, days=len(cal))
    if n == 0:
        return out
    d = day_series(tr, col, cal)
    yp, yn = years_positive(tr, col, two_year)
    out.update(win=tr[col].gt(0).mean(), gross_pts=tr[pre + 'gross_points'].mean(),
               gross_usd=tr[pre + 'gross_usd'].mean(), gross_bp=tr[pre + 'gross_bp'].mean(),
               net_usd=tr[col].mean(), net_bp=tr[pre + 'net_bp'].mean(),
               tot_gross=tr[pre + 'gross_usd'].sum(), tot_net=tr[col].sum(), t_nw=nw_t(d), sharpe=sharpe(d),
               yrs=f'{yp}/{yn}', yp=yp, yn=yn, dseries=d)
    return out


HDR = (f'{"":<30} {"trades":>6} {"win%":>5} {"g pts":>7} {"g bp":>6} {"g $/tr":>7} {"net$/tr":>8} '
       f'{"net bp":>7} {"gross $":>9} {"net $ tot":>9} {"t(NW5)":>6} {"Shrp":>6} {"yrs+":>5}')


def fmt_row(lab, s, extra=''):
    if s.get('trades', 0) == 0:
        return f'{lab:<30} {0:>6}  no trades'
    nb = f'{s["net_bp"]:>7.2f}'
    return (f'{lab:<30} {s["trades"]:>6} {100 * s["win"]:>5.1f} {s["gross_pts"]:>7.2f} {s["gross_bp"]:>6.2f} '
            f'{s["gross_usd"]:>7.2f} {s["net_usd"]:>8.2f} {nb} {s["tot_gross"]:>9.0f} {s["tot_net"]:>9.0f} '
            f'{s["t_nw"]:>6.2f} {s["sharpe"]:>6.2f} {s["yrs"]:>5}{extra}')


def rand_reps(tr, rng):
    """1000 coin-flip and 1000 side-permutation replications on the identical fills; total net $."""
    if len(tr) == 0:
        return None
    mult = tr['market'].map(MULT).to_numpy()
    gross_usd_raw = tr['raw_move_points'].to_numpy() * mult
    cost = (2 * TICK * SLIP_TICKS * mult + COMM).sum()
    S = rng.choice(np.array([-1, 1], dtype=np.int8), size=(N_RAND_REPS, len(tr)))
    coin = S @ gross_usd_raw - cost
    side = tr['side_n'].to_numpy()
    perm = np.array([rng.permutation(side) @ gross_usd_raw for _ in range(N_RAND_REPS)]) - cost
    strat = tr['net_usd'].sum()
    return dict(strat=strat, coin_mean=coin.mean(), coin_p5=np.percentile(coin, 5), coin_p95=np.percentile(coin, 95),
                coin_p=(1 + np.sum(coin >= strat)) / (1 + N_RAND_REPS),
                perm_mean=perm.mean(), perm_p5=np.percentile(perm, 5), perm_p95=np.percentile(perm, 95),
                perm_p=(1 + np.sum(perm >= strat)) / (1 + N_RAND_REPS))


def period_mask(dates, a, b):
    return (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))


# ----------------------------------------------------------------------------------------------------------------
def main():
    t_start = time.time()
    log = []
    fomc_df = pd.read_csv(os.path.join(DATA, 'fomc_dates.csv'))
    fomc_df['date'] = pd.to_datetime(fomc_df['date'])
    sched = fomc_df['scheduled'].astype(str).str.lower() == 'true'
    fomc_sched = pd.DatetimeIndex(fomc_df.loc[sched, 'date'])
    fomc_unsched = fomc_df.loc[~sched].copy()
    cpi_days = pd.DatetimeIndex(pd.to_datetime(pd.read_csv(os.path.join(DATA, 'cpi_dates.csv'))['date']))
    log.append(f'Event calendar: {len(fomc_sched)} scheduled FOMC statement dates '
               f'({fomc_sched.min():%Y-%m-%d} .. {fomc_sched.max():%Y-%m-%d}); {len(fomc_unsched)} unscheduled '
               f'actions NOT used by variant (c): ' + ', '.join(
                   f'{d:%Y-%m-%d} {tm}' for d, tm in zip(fomc_unsched['date'], fomc_unsched['statement_time_et'])))
    log.append(f'Event calendar: {len(cpi_days)} CPI release dates ({cpi_days.min():%Y-%m-%d} .. '
               f'{cpi_days.max():%Y-%m-%d}).')

    rng_side = np.random.default_rng(SEED)
    all_tr = []
    sessions = {}
    firsts = {}
    for mkt in MARKETS:
        raw = load_market(mkt, log)
        sess, reasons, first = prepare(mkt, raw, log, fomc_sched, cpi_days, rng_side)
        del raw
        sessions[mkt] = sess
        firsts[mkt] = first
        for nm, cnt, ds in reasons:
            lst = ', '.join(ds.strftime('%Y-%m-%d')) if 0 < cnt <= 120 and nm != 'early-close day' else ''
            log.append(f'{mkt}: excluded -- {nm}: {cnt} sessions' + (f': {lst}' if lst else ''))
        log.append(f'{mkt}: base-eligible sessions (variant a): {int(sess.base.sum())} of {len(sess)}; '
                   f'prior-close anchor taken from a 12:59 bar (prior session was an early close) on '
                   f'{int((sess.base & sess.prev_early).sum())} of them')
        b0 = sess.loc[~sess.rv_terc.isna(), 'date'].iloc[0]
        d0 = sess.loc[~sess.rsi_terc.isna(), 'date'].iloc[0]
        log.append(f'{mkt}: variant (b) RV tercile available from {b0:%Y-%m-%d}; variant (d) RSI tercile from '
                   f'{d0:%Y-%m-%d} (250-session burn-in); latest cut-offs: RV top-tercile threshold '
                   f'{1e4 * sess.rv_q2.dropna().iloc[-1]:.1f} bp, RSI bottom-tercile threshold '
                   f'{sess.rsi_q1.dropna().iloc[-1]:.1f}')
        # event-day accounting
        for ev, mask in [('FOMC (scheduled)', sess.fomc), ('CPI', sess.cpi)]:
            ev_dates = fomc_sched if ev.startswith('FOMC') else cpi_days
            inrange = ev_dates[(ev_dates >= sess.date.iloc[0]) & (ev_dates <= sess.date.iloc[-1])]
            in_cal = int(mask.sum())
            lost = sess.loc[mask & ~sess.base]
            why = []
            for _, r in lost.iterrows():
                w_ = ('early' if r.early else 'roll' if r.roll_skip else 'abnormal-gap' if r.abnormal
                      else 'multi-contract' if r.multi else 'other')
                why.append(f'{r.date:%Y-%m-%d} ({w_})')
            log.append(f'{mkt}: {ev}: {len(inrange)} dates within the data, {in_cal} are RTH sessions, '
                       f'{in_cal - len(lost)} tradable; not tradable: ' + (', '.join(why) if why else 'none'))
        for v in VARIANTS:
            all_tr.append(build_trades(mkt, sess, v))
        log.append(f'{mkt}: done ({time.time() - t_start:.0f}s elapsed)')

    tr = pd.concat(all_tr, ignore_index=True)

    # ---- trades CSV ----
    cols = ['date', 'market', 'variant', 'era', 'side', 'entry_time', 'entry_price', 'exit_time', 'exit_price',
            'gross_points', 'gross_usd', 'gross_bp', 'net_points', 'net_usd', 'net_bp', 'win', 'entry_ref_price',
            'exit_ref_price', 'contract_id', 'prior_close_date', 'prior_close', 'prior_close_is_1259', 'price_1530',
            'signal_bp', 'rv30_bp', 'rv30_tercile', 'rsi5_prior_close', 'rsi5_tercile', 'vol20_tercile',
            'fomc_day', 'cpi_day', 'rand_side', 'rand_gross_points', 'rand_net_usd', 'next_open',
            'next_open_side_bp']
    csv = tr[cols].copy()
    csv['date'] = csv['date'].dt.strftime('%Y-%m-%d')
    csv['prior_close_date'] = pd.to_datetime(csv['prior_close_date']).dt.strftime('%Y-%m-%d')
    csv['entry_time'] = csv['entry_time'].dt.strftime('%Y-%m-%d %H:%M')
    csv['exit_time'] = csv['exit_time'].dt.strftime('%Y-%m-%d %H:%M')
    csv.to_csv(OUT_TRADES, index=False, float_format='%.6g')

    # ---- calendars ----
    def calendar(mkt, v, a, b):
        d = sessions[mkt]['date']
        d = d[period_mask(d, a, b) & (d >= firsts[mkt][v])]
        return pd.DatetimeIndex(d)

    def pooled_cal(v, a, b):
        return calendar('ES', v, a, b).union(calendar('NQ', v, a, b))

    rng_reps = np.random.default_rng(SEED + 7)

    L = []
    w = L.append
    bar = '=' * 132
    w('P2 LAST-HALF-HOUR MOMENTUM, SIGNED BY THE PRIOR-CLOSE-TO-15:30 RETURN -- literature_report.md section 7, P2')
    w(f'Generated by lit_p2_lasthalfhour.py on {pd.Timestamp.now():%Y-%m-%d %H:%M}')
    w('Data: Databento CME 1-min bars, continuous front contract by volume, unadjusted prices; RTH 09:30-16:00 ET.')
    w('Trade: side = sign(C 15:29 / prior-session C 15:59 - 1), same contract; buy/sell the 15:30 bar open, exit the')
    w('       15:59 bar close; one micro per trade (MES $5/pt, MNQ $2/pt).')
    w('Costs per micro: entry and exit each 1 tick adverse (market fills), $1.00 commission per round trip.')
    w(f'  MES round trip = 2 x $1.25 + $1.00 = ${RT_COST["ES"]:.2f}; MNQ = 2 x $0.50 + $1.00 = ${RT_COST["NQ"]:.2f}.')
    w('Gross = 15:30 open to 15:59 close with no slippage or commission.  bp = 1e4 x P&L / entry notional.')
    w('win% = share of trades with net $ > 0.  t(NW5) = mean day-level net $ / Newey-West (5 lags) SE on the calendar')
    w('of all RTH sessions in the period from the first day the variant filter exists (no-trade days count as 0).')
    w('Shrp = annualised Sharpe of that daily series.  yrs+ = calendar years in the period with >= 20 trades and')
    w('positive mean net $ / such years (variant c: 2-year blocks 2010-11, 2012-13, ... with >= 20 trades).')
    w('Random ctrl = same days, same fills, coin-flip side (one fixed-seed draw per market-day shared by all variants).')
    w('')
    w(bar)
    w('DATA / SESSION LOG')
    w(bar)
    for line in log:
        w(line)

    # ---------------- primary table + multiple testing ----------------
    cells = []
    for era, a, b in ERAS:
        for mkt in MARKETS:
            for v in VARIANTS:
                t = tr[(tr.market == mkt) & (tr.variant == v) & (tr.era == era)]
                cal = calendar(mkt, v, a, b)
                s = stats_block(t, cal, two_year=(v == 'c'))
                sr = stats_block(t, cal, rand=True, two_year=(v == 'c'))
                cells.append(dict(era=era, mkt=mkt, v=v, s=s, sr=sr, t=t, cal=cal))
    prim = [c for c in cells if c['era'] == 'PRIMARY']
    sec = [c for c in cells if c['era'] != 'PRIMARY']
    for grp, fn in [(prim, holm), (sec, by_adjust)]:
        p = np.array([p_two(c['s'].get('t_nw', np.nan)) if c['s']['trades'] else 1.0 for c in grp])
        p = np.where(np.isfinite(p), p, 1.0)
        adj = fn(p)
        for c, pi, ai in zip(grp, p, adj):
            c['p'] = pi
            c['p_adj'] = ai
            pg = p_two(nw_t(day_series(c['t'], 'gross_usd', c['cal']))) if c['s']['trades'] else np.nan
            c['t_gross'] = nw_t(day_series(c['t'], 'gross_usd', c['cal'])) if c['s']['trades'] else np.nan
            c['p_gross'] = pg

    w('')
    w(bar)
    w('HEADLINE: 24 PRE-REGISTERED CELLS (1 micro per trade). Gross first, then net.')
    w('  PRIMARY (8 tests): p_adj = Holm, 5% familywise.  SECONDARY (16 cells): p_adj = Benjamini-Yekutieli.')
    w('  p = two-sided normal p of the day-level NW(5) t on net $.  t gross = same on gross $.')
    w(bar)
    w(f'{"era":<8} {"mkt":<4} {"var":<3} {"trades":>6} {"win%":>5} {"g bp":>6} {"g $/tr":>7} {"t gross":>7} '
      f'{"net bp":>7} {"net$/tr":>8} {"net $ tot":>9} {"t(NW5)":>6} {"p":>7} {"p_adj":>7} {"yrs+":>5} '
      f'{"rand net$":>9} {"rand t":>6}')
    for c in cells:
        s, sr = c['s'], c['sr']
        if s['trades'] == 0:
            w(f'{c["era"]:<8} {c["mkt"]:<4} {c["v"]:<3} no trades')
            continue
        w(f'{c["era"]:<8} {c["mkt"]:<4} {c["v"]:<3} {s["trades"]:>6} {100 * s["win"]:>5.1f} {s["gross_bp"]:>6.2f} '
          f'{s["gross_usd"]:>7.2f} {c["t_gross"]:>7.2f} {s["net_bp"]:>7.2f} {s["net_usd"]:>8.2f} '
          f'{s["tot_net"]:>9.0f} {s["t_nw"]:>6.2f} {c["p"]:>7.4f} {c["p_adj"]:>7.4f} {s["yrs"]:>5} '
          f'{sr["tot_net"]:>9.0f} {sr["t_nw"]:>6.2f}')

    w('')
    w('KEY NUMBERS (computed):')
    pos = [c for c in prim if c['s']['trades'] and c['s']['net_usd'] > 0]
    best = max((c for c in prim if c['s']['trades']), key=lambda c: c['s']['t_nw'])
    w(f'  PRIMARY: {len(pos)} of 8 cells have positive mean net $; best net t = {best["s"]["t_nw"]:.2f} '
      f'({best["mkt"]} {best["v"]}); Holm-significant POSITIVE cells: '
      + (', '.join(f'{c["mkt"]} {c["v"]}' for c in prim if c['p_adj'] <= 0.05 and c['s']['t_nw'] > 0) or 'none'))
    neg = [c for c in prim if c['p_adj'] <= 0.05 and c['s']['t_nw'] < 0]
    for c in neg:
        w(f'  PRIMARY {c["mkt"]} {c["v"]}: net t {c["s"]["t_nw"]:.2f} (Holm p {c["p_adj"]:.4f}) is significantly '
          f'NEGATIVE; its gross t is {c["t_gross"]:.2f} (gross {c["s"]["gross_bp"]:+.2f} bp/tr), so the loss is the '
          f'round-trip cost (${RT_COST[c["mkt"]]:.2f}/tr), not a reversed signal.')
    w('  SECONDARY: BY-significant cells (p_adj <= 0.05): '
      + (', '.join(f'{c["era"]} {c["mkt"]} {c["v"]} (net t {c["s"]["t_nw"]:+.2f}, gross t {c["t_gross"]:+.2f}, '
                   f'gross {c["s"]["gross_bp"]:+.2f} bp/tr)' for c in sec if c['p_adj'] <= 0.05) or 'none'))
    w('  (a negative net t with a non-negative gross t means the round-trip cost, not the signal, drives the loss)')
    for mkt in MARKETS:
        ss = sessions[mkt]
        w(f'  {mkt}: days skipped as first day after a roll (no same-contract prior close in the continuous file): '
          f'{int(ss.roll_skip.sum())} total; by era ' + ', '.join(
              f'{e} {int((ss.roll_skip & period_mask(ss.date, a, b)).sum())}' for e, a, b in ERAS)
          + f'; early-close days excluded: {int(ss.early.sum())}; abnormal-gap days excluded: '
          f'{int((ss.abnormal & ~ss.roll_skip & ~ss.early).sum())}')

    # ---------------- acceptance gates (primary) ----------------
    w('')
    w(bar)
    w('ACCEPTANCE GATES, PRIMARY ERA (literature_report.md section 7 common protocol; preregistration.md)')
    w('  t: single pre-registered replication -> exact t reported; 2-3 = "promising, needs a forward test".')
    w('  yrs+ >= 2/3 of years (variant c: 2-year blocks) with >= 20 trades; gross $/tr >= 1.5 x round-trip cost;')
    w('  beats random: empirical p (1000 coin-flip reps, same fills) <= 0.05; DSR >= 0.95 '
      f'(N = {N_TRIALS_DSR} trials, null SR variance 1/T); Holm(+) = Holm p_adj <= 0.05 with t > 0.')
    w(bar)
    w(f'{"mkt":<4} {"var":<3} {"t(NW5)":>7} {"Holm p":>7} {"yrs+":>6} {"g$/tr":>7} {"1.5xcost":>8} '
      f'{"rand p":>7} {"DSR":>6}  verdict')
    gate_rows = {}
    for c in prim:
        s = c['s']
        if s['trades'] == 0:
            continue
        rr = rand_reps(c['t'], rng_reps)
        c['rr'] = rr
        dval = dsr(s['dseries'])
        g_t = s['t_nw'] >= 2
        g_y = s['yn'] > 0 and s['yp'] >= 2 / 3 * s['yn']
        g_c = s['gross_usd'] >= 1.5 * RT_COST[c['mkt']]
        g_r = rr['coin_p'] <= 0.05
        g_d = dval >= 0.95
        g_h = (c['p_adj'] <= 0.05) and s['t_nw'] > 0
        gates = [('t>=2', g_t), ('Holm(+)', g_h), ('years', g_y), ('gross>=1.5c', g_c),
                 ('beats random', g_r), ('DSR', g_d)]
        verdict = 'PASS all' if all(g for _, g in gates) else 'fails: ' + ', '.join(nm for nm, g in gates if not g)
        if c['p_adj'] <= 0.05 and s['t_nw'] < 0:
            verdict += '  [significantly NEGATIVE net after Holm]'
        gate_rows[(c['mkt'], c['v'])] = dict(dsr=dval, rand_p=rr['coin_p'])
        w(f'{c["mkt"]:<4} {c["v"]:<3} {s["t_nw"]:>7.2f} {c["p_adj"]:>7.4f} {s["yrs"]:>6} {s["gross_usd"]:>7.2f} '
          f'{1.5 * RT_COST[c["mkt"]]:>8.2f} {rr["coin_p"]:>7.3f} {dval:>6.3f}  {verdict}')

    # ---------------- detailed per market / period ----------------
    def detail_section(mkt_label, tsel_fn, cal_fn, mkts):
        w('')
        w(bar)
        w(f'{mkt_label} -- 1 micro per trade')
        w(bar)
        for per, a, b in PERIODS:
            w('')
            w(f'--- {PERIOD_LABEL[per]} ---')
            w(HDR)
            for v in VARIANTS:
                t = tsel_fn(v, a, b)
                cal = cal_fn(v, a, b)
                s = stats_block(t, cal, two_year=(v == 'c'))
                w(fmt_row(f'({v}) {VDESC[v]}', s))
                if s['trades'] == 0:
                    continue
                # unconditional drift: always-long 15:30 open -> 15:59 close on all base-eligible days in period
                dr = []
                for m in mkts:
                    ss = sessions[m]
                    sel = ss.base & period_mask(ss.date, a, b)
                    dr.append(1e4 * (ss.loc[sel, 'x_ref'] / ss.loc[sel, 'e_ref'] - 1.0))
                drift = pd.concat(dr).mean()
                for sd_, nm in [('long', 'long leg'), ('short', 'short leg')]:
                    tl = t[t.side == sd_]
                    sl = stats_block(tl, cal, two_year=(v == 'c'))
                    exp = drift if sd_ == 'long' else -drift
                    w(fmt_row(f'    {nm}', sl, f'  drift-only exp. {exp:+.2f} bp/tr'))
                sr = stats_block(t, cal, rand=True, two_year=(v == 'c'))
                w(fmt_row('    random-direction ctrl', sr))
                rr = rand_reps(t, rng_reps)
                w(f'    random reps ({N_RAND_REPS}): coin-flip total net mean {rr["coin_mean"]:,.0f} '
                  f'[5%..95% {rr["coin_p5"]:,.0f} .. {rr["coin_p95"]:,.0f}], p(rand >= strat) = {rr["coin_p"]:.3f}; '
                  f'side-permutation (same long/short mix) mean {rr["perm_mean"]:,.0f} '
                  f'[{rr["perm_p5"]:,.0f} .. {rr["perm_p95"]:,.0f}], p = {rr["perm_p"]:.3f}')
                w(f'    always-long 15:30-16:00 on all {sum(len(x) for x in dr)} eligible session-markets: '
                  f'{drift:+.2f} bp gross per day; long share of trades {100 * (t.side == "long").mean():.1f}%')

    for mkt in MARKETS:
        detail_section(f'{mkt} ({MICRO[mkt]}, ${MULT[mkt]:.0f}/pt)',
                       lambda v, a, b, m=mkt: tr[(tr.market == m) & (tr.variant == v) & period_mask(tr.date, a, b)],
                       lambda v, a, b, m=mkt: calendar(m, v, a, b), [mkt])
    detail_section('POOLED ES + NQ (1 MES + 1 MNQ; day P&L summed; bp averaged over trades)',
                   lambda v, a, b: tr[(tr.variant == v) & period_mask(tr.date, a, b)],
                   pooled_cal, MARKETS)

    # ---------------- per calendar year ----------------
    w('')
    w(bar)
    w('PER CALENDAR YEAR (all eras; 1 micro per trade)')
    w('  rand = fixed-seed random-direction control on the same days and fills; L/S = long / short legs;')
    w('  drift = always-long 15:30-16:00 gross bp on all base-eligible days of that year.')
    w(bar)
    for mkt in MARKETS:
        ss = sessions[mkt]
        drift_y = (1e4 * (ss.x_ref / ss.e_ref - 1.0))[ss.base].groupby(ss.year[ss.base]).mean()
        for v in VARIANTS:
            t = tr[(tr.market == mkt) & (tr.variant == v)]
            w('')
            w(f'{mkt} ({v}) {VDESC[v]}')
            w(f'{"year":<6} {"trades":>6} {"win%":>5} {"g bp":>6} {"g $/tr":>7} {"g $ tot":>8} {"net$/tr":>8} '
              f'{"net bp":>7} {"net $ tot":>9} {"L n":>4} {"L net$":>8} {"S n":>4} {"S net$":>8} {"rand $":>8} '
              f'{"drift":>6}')
            for y, g in t.groupby('year'):
                gl, gs = g[g.side == 'long'], g[g.side == 'short']
                w(f'{y:<6} {len(g):>6} {100 * g.win.mean():>5.1f} {g.gross_bp.mean():>6.2f} {g.gross_usd.mean():>7.2f} '
                  f'{g.gross_usd.sum():>8.0f} {g.net_usd.mean():>8.2f} {g.net_bp.mean():>7.2f} {g.net_usd.sum():>9.0f} '
                  f'{len(gl):>4} {gl.net_usd.sum():>8.0f} {len(gs):>4} {gs.net_usd.sum():>8.0f} '
                  f'{g.rand_net_usd.sum():>8.0f} {drift_y.get(y, np.nan):>6.2f}')
            if v == 'c':
                w('  2-year blocks:')
                for blk, g in t.groupby((t.year - 2010) // 2):
                    y0 = 2010 + 2 * blk
                    w(f'  {y0}-{(y0 + 1) % 100:02d} {len(g):>5} trades, net $/tr {g.net_usd.mean():>7.2f}, '
                      f'net $ tot {g.net_usd.sum():>7.0f}, gross bp {g.gross_bp.mean():>6.2f}')

    # ---------------- volatility tercile breakdown ----------------
    w('')
    w(bar)
    w('BY VOLATILITY REGIME (common protocol; VIX unavailable -> trailing 20-day realised vol of 5-min RTH returns,')
    w('known at the prior close; expanding tercile cut-offs after a 250-session burn-in). Breakdown only.')
    w(bar)
    for per in ['PRIMARY', 'ALL']:
        a, b = [(x[1], x[2]) for x in PERIODS if x[0] == per][0]
        w('')
        w(f'--- {PERIOD_LABEL[per]} ---')
        w(HDR)
        for mkt in MARKETS:
            for v in VARIANTS:
                t = tr[(tr.market == mkt) & (tr.variant == v) & period_mask(tr.date, a, b)]
                ss = sessions[mkt]
                for k in [1, 2, 3]:
                    tk = t[t.vol20_tercile == k]
                    calk = pd.DatetimeIndex(ss.loc[(ss.vol_terc == k) & period_mask(ss.date, a, b)
                                                   & (ss.date >= firsts[mkt][v]), 'date'])
                    w(fmt_row(f'{mkt} ({v}) vol tercile {k}', stats_block(tk, calk, two_year=(v == 'c'))))
                nb = int(t.vol20_tercile.isna().sum())
                if nb:
                    w(f'{mkt} ({v}) burn-in (no tercile): {nb} trades, net $/tr {t[t.vol20_tercile.isna()].net_usd.mean():.2f}')

    # ---------------- diagnostics ----------------
    w('')
    w(bar)
    w('DIAGNOSTICS (not used for selection)')
    w(bar)
    w('')
    w('1) Signal size [3]: variant (a) by quintile of |prior close -> 15:30 return| (cut-offs from the trades in the')
    w('   period itself; descriptive only). t = per-trade NW(5) t of net $.')
    for per in ['PRIMARY', 'SEC1', 'SEC2', 'ALL']:
        a, b = [(x[1], x[2]) for x in PERIODS if x[0] == per][0]
        w(f'   --- {PERIOD_LABEL[per]} ---')
        w(f'   {"mkt":<4} {"q":<2} {"|sig| bp range":<18} {"trades":>6} {"win%":>5} {"g bp":>6} {"g $/tr":>7} '
          f'{"net$/tr":>8} {"t":>6}')
        for mkt in MARKETS:
            t = tr[(tr.market == mkt) & (tr.variant == 'a') & period_mask(tr.date, a, b)].copy()
            if len(t) < 50:
                continue
            t['absig'] = t.signal_bp.abs()
            t['q'] = pd.qcut(t.absig, 5, labels=False) + 1
            for q, g in t.groupby('q'):
                w(f'   {mkt:<4} {q:<2} {g.absig.min():>7.1f} .. {g.absig.max():>7.1f} {len(g):>6} '
                  f'{100 * g.win.mean():>5.1f} {g.gross_bp.mean():>6.2f} {g.gross_usd.mean():>7.2f} '
                  f'{g.net_usd.mean():>8.2f} {nw_t(g.net_usd.to_numpy()):>6.2f}')
    w('')
    w('2) Next-open reversal of the 15:30-16:00 move [74] (variant (a) days; next RTH 09:30 open of the same contract).')
    w('   side x (next open / 15:59 close - 1): + = the position kept going overnight, - = it reversed.')
    w('   beta = OLS slope of the 16:00 -> next-open return on the 15:30 -> 16:00 return (HC0 t);')
    w('   share reversed = -mean(sign(move) x next-open ret) / mean(|move|).')
    w(f'   {"period":<10} {"mkt":<4} {"n":>5} {"side x next-open bp":>20} {"t":>6} {"beta":>7} {"t":>6} '
      f'{"share reversed":>15}')
    for per in ['PRIMARY', 'SEC1', 'SEC2', 'ALL']:
        a, b = [(x[1], x[2]) for x in PERIODS if x[0] == per][0]
        for mkt in MARKETS:
            t = tr[(tr.market == mkt) & (tr.variant == 'a') & period_mask(tr.date, a, b)]
            t = t[np.isfinite(t.next_open_ret_bp)]
            if len(t) < 20:
                continue
            xs = t.move_bp.to_numpy()
            ys = t.next_open_ret_bp.to_numpy()
            X = np.c_[np.ones_like(xs), xs]
            beta, *_ = np.linalg.lstsq(X, ys, rcond=None)
            res = ys - X @ beta
            XtXi = np.linalg.inv(X.T @ X)
            cov = XtXi @ (X.T * res ** 2) @ X @ XtXi
            tb = beta[1] / np.sqrt(cov[1, 1])
            share = -np.mean(np.sign(xs) * ys) / np.mean(np.abs(xs))
            w(f'   {per:<10} {mkt:<4} {len(t):>5} {t.next_open_side_bp.mean():>20.2f} '
              f'{nw_t(t.next_open_side_bp.to_numpy()):>6.2f} {beta[1]:>7.3f} {tb:>6.2f} {100 * share:>14.1f}%')
    w('')
    w('3) Days excluded by the abnormal-gap rule (section 5.6: > 10 consecutive missing RTH minutes, i.e. the March')
    w('   2020 circuit-breaker halts). What variant (a) would have done on them (information only, not in any total):')
    for mkt in MARKETS:
        ss = sessions[mkt]
        ab = ss[ss.abnormal]
        for _, r in ab.iterrows():
            ok = (not r.early) and (not r.roll_skip) and np.isfinite(r.sig) and r.side != 0
            if ok:
                g = r.side * (r.x_ref - r.e_ref)
                net = (g - 2 * TICK) * MULT[mkt] - COMM
                w(f'   {mkt} {r.date:%Y-%m-%d} gap {r.max_gap} min: signal {1e4 * r.sig:+.0f} bp -> '
                  f'{"long" if r.side > 0 else "short"}, gross {g:+.2f} pts, net ${net:+.2f}; '
                  f'RV tercile {r.rv_terc:.0f}, RSI tercile {r.rsi_terc:.0f}, FOMC {r.fomc}, CPI {r.cpi}')
            else:
                w(f'   {mkt} {r.date:%Y-%m-%d} gap {r.max_gap} min: also '
                  + ('a roll day' if r.roll_skip else 'early close' if r.early else 'no signal'))
    w('')
    w('4) Unscheduled FOMC actions (not part of variant (c)); variant (a) trade on that date if any (information only):')
    for _, r in fomc_unsched.iterrows():
        parts = []
        for mkt in MARKETS:
            t = tr[(tr.market == mkt) & (tr.variant == 'a') & (tr.date == r['date'])]
            parts.append(f'{mkt} ' + (f'{t.side.iloc[0]} net ${t.net_usd.iloc[0]:+.2f}' if len(t) else 'no trade'))
        w(f'   {r["date"]:%Y-%m-%d} {r["statement_time_et"]}: ' + '; '.join(parts))
    w('')
    w('5) Variant (c) split by event type, all eras (descriptive).')
    for mkt in MARKETS:
        t = tr[(tr.market == mkt) & (tr.variant == 'c')]
        for nm, m in [('FOMC only', t.fomc_day & ~t.cpi_day), ('CPI only', t.cpi_day & ~t.fomc_day),
                      ('both', t.fomc_day & t.cpi_day)]:
            g = t[m]
            if len(g):
                w(f'   {mkt} {nm:<10} {len(g):>4} trades, gross bp {g.gross_bp.mean():>6.2f}, net $/tr '
                  f'{g.net_usd.mean():>7.2f}, net $ tot {g.net_usd.sum():>7.0f}, win {100 * g.win.mean():.1f}%')

    w('')
    w(f'Runtime {time.time() - t_start:.0f}s. Trades CSV: {os.path.basename(OUT_TRADES)} ({len(tr)} rows).')
    with open(OUT_SUMMARY, 'w') as f:
        f.write('\n'.join(L) + '\n')

    # machine-readable headline for the caller
    rows = []
    for c in cells:
        s, sr = c['s'], c['sr']
        rows.append(dict(market=c['mkt'], variant=c['v'], period=c['era'], trades=s['trades'],
                         gross_usd=round(float(s.get('tot_gross', 0.0)), 2),
                         net_usd=round(float(s.get('tot_net', 0.0)), 2),
                         net_per_trade_usd=round(float(s.get('net_usd', np.nan)), 3),
                         t_stat=round(float(s.get('t_nw', np.nan)), 3), p_adj=round(float(c['p_adj']), 4),
                         random_control_net_usd=round(float(sr.get('tot_net', np.nan)), 2),
                         years_positive=s.get('yrs', '')))
    print(pd.DataFrame(rows).to_string(index=False))
    print(f'done in {time.time() - t_start:.0f}s')


if __name__ == '__main__':
    main()
