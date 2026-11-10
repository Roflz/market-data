#!/usr/bin/env python3
"""
P1. Direct replication of the noise-band breakout (Zarattini, Aziz & Barbon, "Beat the Market").
Specification: literature_report.md section 7, "P1." (pre-registered; no parameter tuning).

Band      move(t,d) = |Close_d(t)/Open_d(09:30) - 1| (Close_d(t) = close of the bar ending at t);
          sigma(t) = mean of move(t,.) over the previous 14 full RTH sessions (half-days skipped);
          UB(t) = max(O_d, C_{d-1})*(1+sigma(t)), LB(t) = min(O_d, C_{d-1})*(1-sigma(t)), VM = 1.
          C_{d-1} = prior session's 15:59 bar close of the SAME contract (unadjusted prices).
Decisions 10:00, 10:30, ..., 15:30 (closes of the 09:59 ... 15:29 bars).
Entries   long if decision close > UB(t), short if < LB(t); fill next bar open, 1 tick adverse.
VWAP      RTH VWAP from the 09:30 bar, (H+L+C)/3 weighted by volume.
Exits     at each decision time: long exits if close < max(UB, VWAP); short exits if close > min(LB, VWAP);
          fill next bar open, 1 tick adverse. A break of the opposite band reverses (exit + new entry,
          each leg 1 tick, each round trip $1.00). Flat at the 15:59 bar close, 1 tick adverse.
Early     close days: no entries after 12:30; flat at the 12:59 bar close.
Variants  A = as published (exits only at decision times);
          B = A + resting exchange stop at the current trailing level (max(UB,VWAP) long, min(LB,VWAP) short),
              updated only at decision times, fills 1 tick beyond its price; re-entry allowed at the next
              decision time.
Sizing    (i) 1 micro; (ii) vol-targeted: floor(E*0.02/(sigma_d*P*M)), sigma_d = SD of last 14 within-contract
          daily close-to-close returns, leverage cap 4x, 0 => no trade. E = $100,000 (and --trader-equity).
Periods   (1) 2010-06..2024-04, (2) 2024-05..2024-09, (3) 2024-10..2026-11 primary, (3s) 2025-02..2026-11 strict.
Controls  random direction at the same decision times with identical exits (same entry/exit fills, coin-flip
          side; one fixed-seed realisation + 1000 replications); long/short legs; scrambled days (sigma(t) from
          14 randomly drawn earlier full sessions); constant vs vol-targeted size on the identical trade list.

Costs (fixed): MES $5/pt, MNQ $2/pt, tick 0.25; market/stop fills 1 tick adverse; $1.00 per round trip per micro.

Run:  cd <project> && PYTHONPATH=./pylib python3 lit_p1_noiseband.py [--trader-equity 25000]
"""
import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, 'data')
OUT_TRADES = os.path.join(BASE, 'lit_p1_noiseband_trades.csv')
OUT_SUMMARY = os.path.join(BASE, 'lit_p1_noiseband_summary.txt')

MARKETS = ['ES', 'NQ']
MULT = {'ES': 5.0, 'NQ': 2.0}          # MES / MNQ dollars per point
MICRO = {'ES': 'MES', 'NQ': 'MNQ'}
TICK = 0.25
COMM = 1.00                             # per round trip per micro
SLIP_TICKS = 1                          # per market/stop fill

RTH_START_MIN = 9 * 60 + 30             # 09:30 ET -> slot 0
N_SLOTS = 390                           # 09:30 .. 15:59 bars
DEC_SLOTS = list(range(30, 361, 30))    # decision at 10:00..15:30: uses close of slot k-1, fills at open of slot k
EARLY_LAST_DEC_SLOT = 180               # 12:30: no entries after 12:30 on early-close days
EARLY_FLAT_SLOT = 209                   # 12:59 bar close
FULL_FLAT_SLOT = 389                    # 15:59 bar close
HOLIDAY_LAST_SLOT_MAX = 219             # last RTH bar before 13:10 ET -> cash-market holiday (Globex-only session)
EARLY_LAST_SLOT_MAX = 329               # last RTH bar 13:10..14:59 -> early close (cash close 13:00)
ABNORMAL_GAP_MIN = 10                   # a run of >10 missing RTH minutes = abnormal gap -> excluded from trading
LOOKBACK = 14
VT_TARGET = 0.02
VT_LEV_CAP = 4.0
RESEARCH_EQUITY = 100_000.0
NW_LAGS = 5
N_RAND_REPS = 1000
SEED = 20261108

PERIODS = [
    ('P1_2010-06_2024-04', '2010-06-01', '2024-04-30'),
    ('P2_2024-05_2024-09', '2024-05-01', '2024-09-30'),
    ('P3_PRIMARY_2024-10_2026-11', '2024-10-01', '2026-11-30'),
    ('P3s_STRICT_2025-02_2026-11', '2025-02-01', '2026-11-30'),
    ('ALL_2010-06_2026-11', '2010-06-01', '2026-11-30'),
]


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
    H = O.copy(); L = O.copy(); C = O.copy(); V = np.zeros((nd, N_SLOTS))
    INST = np.full((nd, N_SLOTS), -1, dtype=np.int64)
    O[didx, slot] = df['Open'].to_numpy(float)
    H[didx, slot] = df['High'].to_numpy(float)
    L[didx, slot] = df['Low'].to_numpy(float)
    C[didx, slot] = df['Close'].to_numpy(float)
    V[didx, slot] = df['Volume'].to_numpy(float)
    INST[didx, slot] = df['instrument_id'].to_numpy(np.int64)
    present = ~np.isnan(C)

    first_slot = np.argmax(present, axis=1)
    last_slot = N_SLOTS - 1 - np.argmax(present[:, ::-1], axis=1)
    max_gap = np.zeros(nd, dtype=int)
    multi_inst = np.zeros(nd, dtype=bool)
    for i in range(nd):
        p = np.flatnonzero(present[i])
        upto = p[p <= min(last_slot[i], FULL_FLAT_SLOT)]
        max_gap[i] = int(np.diff(upto).max()) - 1 if len(upto) > 1 else 0
        multi_inst[i] = len(np.unique(INST[i, p])) > 1
    inst_day = INST[np.arange(nd), first_slot]

    # carry the last close forward through missing minutes (zero volume)
    Cff = pd.DataFrame(C).ffill(axis=1).to_numpy()
    miss = ~present
    O[miss] = Cff[miss]; H[miss] = Cff[miss]; L[miss] = Cff[miss]; C = Cff
    V[miss] = 0.0

    info = pd.DataFrame({'date': pd.to_datetime(udays), 'first_slot': first_slot, 'last_slot': last_slot,
                         'max_gap': max_gap, 'multi_inst': multi_inst, 'inst': inst_day,
                         'n_bars': present.sum(1)})
    info['holiday'] = info['last_slot'] <= HOLIDAY_LAST_SLOT_MAX
    info['early'] = (~info['holiday']) & (info['last_slot'] <= EARLY_LAST_SLOT_MAX)
    log.append(f'{mkt}: loaded {len(df):,} RTH bars on {nd} dates in {time.time() - t0:.1f}s')
    return dict(info=info, O=O, H=H, L=L, C=C, V=V)


def prepare_sessions(mkt, raw, log, rng_scr):
    info = raw['info']
    keep = ~info['holiday'].to_numpy()
    hol = info.loc[~keep, 'date'].dt.strftime('%Y-%m-%d').tolist()
    log.append(f'{mkt}: {len(hol)} cash-market holiday dates (Globex-only, last RTH bar before 13:10) removed '
               f'from the session calendar: {", ".join(hol)}')
    info = info.loc[keep].reset_index(drop=True)
    O, H, L, C, V = (raw[k][keep] for k in ('O', 'H', 'L', 'C', 'V'))
    n = len(info)
    early = info['early'].to_numpy()
    full = ~early
    if info['multi_inst'].any():
        log.append(f'{mkt}: WARNING {int(info.multi_inst.sum())} sessions with >1 instrument inside RTH')
    if (info['first_slot'] != 0).any():
        log.append(f'{mkt}: WARNING {int((info.first_slot != 0).sum())} sessions without a 09:30 bar')
    log.append(f'{mkt}: {n} sessions, {int(early.sum())} early-close: '
               + ', '.join(info.loc[early, 'date'].dt.strftime('%Y-%m-%d')))

    # session close: 15:59 bar (full) / 12:59 bar (early close: cash close 13:00)
    sclose = np.where(early, C[:, EARLY_FLAT_SLOT], C[:, FULL_FLAT_SLOT])
    inst = info['inst'].to_numpy()
    cprev = np.r_[np.nan, sclose[:-1]]
    same_prev = np.r_[False, inst[1:] == inst[:-1]]
    open0 = O[:, 0]

    # move(t,d) at the 12 decision times from full sessions; sigma(t) = mean over previous 14 full sessions
    dec = np.array(DEC_SLOTS)
    move = np.abs(C[:, dec - 1] / open0[:, None] - 1.0)
    full_idx = np.flatnonzero(full)
    sigma = np.full((n, len(dec)), np.nan)
    sigma_scr = np.full((n, len(dec)), np.nan)
    for i in range(n):
        nb = np.searchsorted(full_idx, i)          # full sessions strictly before i
        if nb >= LOOKBACK:
            sigma[i] = move[full_idx[nb - LOOKBACK:nb]].mean(0)
            pick = rng_scr.choice(nb, size=LOOKBACK, replace=False)
            sigma_scr[i] = move[full_idx[pick]].mean(0)

    # VWAP through each bar
    tp = (H + L + C) / 3.0
    cv = np.cumsum(V, axis=1)
    vwap = np.cumsum(tp * V, axis=1) / np.where(cv > 0, cv, np.nan)
    vwap = pd.DataFrame(vwap).bfill(axis=1).to_numpy()   # only matters if the 09:30 bar had zero volume

    # within-contract daily close-to-close returns and sigma_d (SD of last 14)
    r = np.where(same_prev, sclose / cprev - 1.0, np.nan)
    ridx = np.flatnonzero(~np.isnan(r))
    sigma_d = np.full(n, np.nan)
    for i in range(n):
        nb = np.searchsorted(ridx, i)              # returns of sessions strictly before i
        if nb >= LOOKBACK:
            sigma_d[i] = np.std(r[ridx[nb - LOOKBACK:nb]], ddof=1)

    # volatility regime: trailing 20-day realised vol from 5-minute RTH log returns (known at the prior close),
    # tercile cut-offs from an expanding window of all prior days after a 250-day burn-in
    grid = np.arange(4, N_SLOTS, 5)
    px = np.concatenate([open0[:, None], C[:, grid]], axis=1)
    lr = np.diff(np.log(px), axis=1)
    lr[early[:, None] & (grid[None, :] > EARLY_FLAT_SLOT)] = 0.0
    rv = (lr ** 2).sum(1)
    var20 = pd.Series(rv).rolling(20).mean().shift(1).to_numpy()
    vol20 = np.sqrt(252.0 * var20)
    terc = np.full(n, np.nan)
    hist = []
    for i in range(n):
        v = vol20[i]
        if np.isnan(v):
            continue
        if len(hist) >= 250:
            q1, q2 = np.quantile(hist, [1 / 3, 2 / 3])
            terc[i] = 1 + int(v > q1) + int(v > q2)
        hist.append(v)

    # 1-minute drift per calendar year (bp/minute), for the drift-only benchmark of the long/short legs
    lr1 = np.concatenate([np.log(C[:, :1] / O[:, :1]), np.diff(np.log(C), axis=1)], axis=1)
    mask = np.ones_like(lr1, dtype=bool)
    mask[early, EARLY_FLAT_SLOT + 1:] = False
    yrs = info['date'].dt.year.to_numpy()
    drift = {}
    for y in np.unique(yrs):
        sel = (yrs == y)
        drift[int(y)] = 1e4 * lr1[sel][mask[sel]].mean()

    abnormal = info['max_gap'].to_numpy() > ABNORMAL_GAP_MIN
    sess = info.assign(early=early, sclose=sclose, cprev=cprev, same_prev=same_prev, open0=open0,
                       sigma_d=sigma_d, vol20=vol20, terc=terc, abnormal=abnormal)
    return dict(sess=sess, O=O, H=H, L=L, C=C, vwap=vwap, sigma=sigma, sigma_scr=sigma_scr, drift=drift)


# ----------------------------------------------------------------------------------------------------------------
# Strategy simulation (one day)
# ----------------------------------------------------------------------------------------------------------------
def first_stop_hit(side, stop, Od, Hd, Ld, a, b):
    """first bar in [a, b] (inclusive) that touches the resting stop; returns (slot, reference price) or None."""
    if b < a:
        return None
    if side > 0:
        hit = np.flatnonzero(Ld[a:b + 1] <= stop)
        if len(hit) == 0:
            return None
        j = a + int(hit[0])
        return j, min(Od[j], stop)
    hit = np.flatnonzero(Hd[a:b + 1] >= stop)
    if len(hit) == 0:
        return None
    j = a + int(hit[0])
    return j, max(Od[j], stop)


def sim_day(Od, Hd, Ld, Cd, vwd, ub, lb, early, variant):
    trades = []
    pos = 0
    cur = None
    stop = None
    seg = 0
    ndec = DEC_SLOTS.index(EARLY_LAST_DEC_SLOT) + 1 if early else len(DEC_SLOTS)
    last = EARLY_FLAT_SLOT if early else FULL_FLAT_SLOT

    def close(x_slot, x_ref, reason):
        cur.update(x_slot=x_slot, x_ref=x_ref, reason=reason)
        trades.append(cur)

    for j in range(ndec):
        k = DEC_SLOTS[j]
        if variant == 'B' and pos != 0:
            h = first_stop_hit(pos, stop, Od, Hd, Ld, seg, k - 1)
            if h is not None:
                close(h[0], h[1], 'stop')
                pos, cur, stop = 0, None, None
        c, vw, u, l = Cd[k - 1], vwd[k - 1], ub[j], lb[j]
        new = pos
        if pos == 1:
            if c < l:
                new = -1
            elif c < max(u, vw):
                new = 0
        elif pos == -1:
            if c > u:
                new = 1
            elif c > min(l, vw):
                new = 0
        else:
            if c > u:
                new = 1
            elif c < l:
                new = -1
        if pos != 0 and new != pos:
            close(k, Od[k], 'reverse' if new != 0 else 'trail')
            pos, cur = 0, None
        if new != 0 and pos == 0:
            pos = new
            cur = dict(side=new, e_slot=k, e_ref=Od[k], dec_close=c, dec_vwap=vw, ub=u, lb=l,
                       wrong_vwap=bool((new > 0 and c < vw) or (new < 0 and c > vw)))
        if pos != 0:
            # exchange stops must sit on the tick grid: a sell stop at the highest tick <= the level (triggers once
            # price trades below the level), a buy stop at the lowest tick >= the level
            stop = (np.floor(max(u, vw) / TICK + 1e-9) * TICK if pos > 0
                    else np.ceil(min(l, vw) / TICK - 1e-9) * TICK)
            seg = k
    if pos != 0 and variant == 'B':
        h = first_stop_hit(pos, stop, Od, Hd, Ld, seg, last)
        if h is not None:
            close(h[0], h[1], 'stop')
            pos, cur = 0, None
    if pos != 0:
        close(last + 1, Cd[last], 'eod')      # x_slot = last+1 marks "close of bar `last`"
    return trades


def run_strategy(mkt, P, variant, sigma_key, log, label):
    s = P['sess']
    sig = P[sigma_key]
    n = len(s)
    rows = []
    cnt = dict(no_sigma=0, roll_skip=0, abnormal=0, traded_days=0)
    for i in range(n):
        if np.isnan(sig[i]).any():
            cnt['no_sigma'] += 1
            continue
        if not s.same_prev.iat[i]:
            cnt['roll_skip'] += 1
            continue
        if s.abnormal.iat[i]:
            cnt['abnormal'] += 1
            continue
        cnt['traded_days'] += 1
        o0, cp = s.open0.iat[i], s.cprev.iat[i]
        ub = max(o0, cp) * (1.0 + sig[i])
        lb = min(o0, cp) * (1.0 - sig[i])
        tr = sim_day(P['O'][i], P['H'][i], P['L'][i], P['C'][i], P['vwap'][i], ub, lb, bool(s.early.iat[i]), variant)
        for t in tr:
            t['si'] = i
        rows.extend(tr)
    df = pd.DataFrame(rows)
    df['variant'] = label
    df['market'] = mkt
    return df, cnt


# ----------------------------------------------------------------------------------------------------------------
# P&L, statistics
# ----------------------------------------------------------------------------------------------------------------
def slot_time(dates, slots):
    return dates + pd.to_timedelta(RTH_START_MIN + slots, unit='m')


def enrich(df, P, mkt, rng, equity_list):
    s = P['sess']
    M = MULT[mkt]
    si = df['si'].to_numpy()
    df['date'] = s['date'].to_numpy()[si]
    df['early_close_day'] = s['early'].to_numpy()[si]
    side = df['side'].to_numpy()
    e_ref = df['e_ref'].to_numpy(); x_ref = df['x_ref'].to_numpy()
    df['entry_time'] = slot_time(df['date'], df['e_slot'])
    df['exit_time'] = slot_time(df['date'], df['x_slot'])    # open fills: bar start; stop: bar start; eod: bar end
    df['hold_min'] = df['x_slot'] - df['e_slot']
    df['entry_price'] = e_ref + side * TICK * SLIP_TICKS
    df['exit_price'] = x_ref - side * TICK * SLIP_TICKS
    df['gross_points'] = side * (x_ref - e_ref)
    df['gross_usd'] = df['gross_points'] * M
    df['gross_bp'] = 1e4 * side * (x_ref / e_ref - 1.0)
    df['net_points'] = side * (df['exit_price'] - df['entry_price'])
    df['net_usd'] = df['net_points'] * M - COMM
    df['net_bp'] = 1e4 * df['net_usd'] / (e_ref * M)
    df['win'] = df['net_usd'] > 0
    df['year'] = df['date'].dt.year
    df['vol_tercile'] = s['terc'].to_numpy()[si]
    df['sigma_d'] = s['sigma_d'].to_numpy()[si]
    df['drift_bp'] = side * np.array([P['drift'][y] for y in df['year']]) * df['hold_min'].to_numpy()
    # random-direction control: same entry/exit fills, coin-flip side
    rs = rng.choice([-1, 1], size=len(df))
    df['rand_side'] = rs
    df['rand_gross_points'] = rs * (x_ref - e_ref)
    df['rand_net_usd'] = (df['rand_gross_points'] - 2 * TICK * SLIP_TICKS) * M - COMM
    # volatility-targeted size on the identical trade list
    for E in equity_list:
        tag = f'{int(E)}'
        nraw = np.floor(E * VT_TARGET / (df['sigma_d'].to_numpy() * e_ref * M))
        cap = np.floor(VT_LEV_CAP * E / (e_ref * M))
        nct = np.minimum(nraw, cap)
        df[f'vt{tag}_contracts'] = nct
        df[f'vt{tag}_capped'] = nraw > cap
        df[f'vt{tag}_net_usd'] = np.where(np.isnan(nct), np.nan, nct * df['net_usd'].to_numpy())
        df[f'vt{tag}_gross_usd'] = np.where(np.isnan(nct), np.nan, nct * df['gross_usd'].to_numpy())
    return df


def nw_t(x, lags=NW_LAGS):
    x = np.asarray(x, float)
    T = len(x)
    if T < 3:
        return np.nan
    e = x - x.mean()
    lrv = e @ e / T
    for l in range(1, lags + 1):
        lrv += 2.0 * (1.0 - l / (lags + 1.0)) * (e[l:] @ e[:-l]) / T
    se = np.sqrt(lrv / T)
    return x.mean() / se if se > 0 else np.nan


def daily_series(tr, col, cal):
    d = tr.groupby('date')[col].sum()
    return d.reindex(cal, fill_value=0.0).to_numpy()


def sharpe(x):
    sd = np.std(x, ddof=1)
    return np.sqrt(252) * np.mean(x) / sd if sd > 0 else np.nan


def period_mask(dates, a, b):
    return (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))


def stats_block(tr, cal, col='net_usd', gcol='gross_usd'):
    n = len(tr)
    if n == 0:
        return dict(trades=0)
    d = daily_series(tr, col, cal)
    out = dict(trades=n, days=len(cal), tpd=n / max(len(cal), 1), win=tr['win'].mean() if 'win' in tr else np.nan,
               gross_pts=tr['gross_points'].mean(), gross_usd=tr[gcol].mean(), gross_bp=tr['gross_bp'].mean(),
               net_usd=tr[col].mean(), net_bp=tr['net_bp'].mean(), tot_net=tr[col].sum(),
               t_nw=nw_t(d), sharpe=sharpe(d))
    yr = tr.groupby('year')[col].agg(['count', 'mean'])
    yr = yr[yr['count'] >= 20]
    out['yrs_pos'] = f'{int((yr["mean"] > 0).sum())}/{len(yr)}'
    return out


def fmt_row(lab, s, extra=''):
    if s.get('trades', 0) == 0:
        return f'{lab:<34} no trades'
    return (f'{lab:<34} {s["trades"]:>6} {s["tpd"]:>5.2f} {100 * s["win"]:>5.1f} {s["gross_pts"]:>8.2f} '
            f'{s["gross_usd"]:>8.2f} {s["gross_bp"]:>7.2f} {s["net_usd"]:>8.2f} {s["net_bp"]:>7.2f} '
            f'{s["tot_net"]:>10.0f} {s["t_nw"]:>6.2f} {s["sharpe"]:>6.2f} {s["yrs_pos"]:>6}{extra}')


HDR = (f'{"":<34} {"trades":>6} {"t/day":>5} {"win%":>5} {"g pts":>8} {"g $/tr":>8} {"g bp":>7} '
       f'{"net$/tr":>8} {"net bp":>7} {"net $ tot":>10} {"t(NW5)":>6} {"Shrp":>6} {"yrs+":>6}')


# ----------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trader-equity', type=float, default=None,
                    help="trader's actual account equity for the vol-targeted sizing run (not supplied by default)")
    args = ap.parse_args()
    equity_list = [RESEARCH_EQUITY] + ([args.trader_equity] if args.trader_equity else [])

    t_start = time.time()
    log = []
    rng_scr = np.random.default_rng(SEED + 1)
    rng_rand = np.random.default_rng(SEED)
    all_trades = []
    cals = {}
    counts = {}
    halt_days = {}
    for mkt in MARKETS:
        raw = load_market(mkt, log)
        P = prepare_sessions(mkt, raw, log, rng_scr)
        del raw
        s = P['sess']
        roll = s.loc[~s.same_prev, 'date'].dt.strftime('%Y-%m-%d').tolist()[1:]   # [0] = first day of the data
        log.append(f'{mkt}: {len(roll)} sessions whose prior session is a different contract (first day after a '
                   f'roll; no same-contract C_(d-1) in the continuous file) -> skipped (plus the first data day, '
                   f'which has no prior session): {", ".join(roll)}')
        ab = s.loc[s.abnormal, ['date', 'max_gap']]
        log.append(f'{mkt}: {len(ab)} RTH days with an abnormal gap (> {ABNORMAL_GAP_MIN} missing minutes) excluded '
                   f'from trading: ' + ', '.join(f'{d:%Y-%m-%d} ({g} min)' for d, g in ab.itertuples(index=False)))
        halt_days[mkt] = set(ab['date'])
        first_trade_session = s.index[~np.isnan(P['sigma']).any(1)][0]
        cals[mkt] = s['date'].iloc[first_trade_session:].reset_index(drop=True)
        for variant, skey, label in [('A', 'sigma', 'A'), ('B', 'sigma', 'B'),
                                     ('A', 'sigma_scr', 'A_scrambled'), ('B', 'sigma_scr', 'B_scrambled')]:
            df, cnt = run_strategy(mkt, P, variant, skey, log, label)
            counts[(mkt, label)] = cnt
            df = enrich(df, P, mkt, rng_rand, equity_list)
            all_trades.append(df)
        # sensitivity: the abnormal-gap (circuit-breaker halt) days, simulated anyway, reported separately
        Pab = dict(P)
        sess2 = s.copy(); sess2['abnormal'] = False
        Pab['sess'] = sess2
        for variant in ['A', 'B']:
            df, _ = run_strategy(mkt, Pab, variant, 'sigma', log, variant)
            df = df[df['si'].isin(np.flatnonzero(s.abnormal.to_numpy()))]
            if len(df):
                df = enrich(df, Pab, mkt, np.random.default_rng(0), equity_list)
                halt_days[(mkt, variant)] = df
        log.append(f'{mkt}: done ({time.time() - t_start:.0f}s elapsed)')
        del P, Pab

    tr = pd.concat(all_trades, ignore_index=True)
    tr['period'] = np.select(
        [period_mask(tr['date'], '2010-06-01', '2024-04-30'), period_mask(tr['date'], '2024-05-01', '2024-09-30'),
         period_mask(tr['date'], '2024-10-01', '2026-11-30')], ['P1', 'P2', 'P3'], default='')
    tr['strict_P3s'] = period_mask(tr['date'], '2025-02-01', '2026-11-30')
    tr['side_str'] = np.where(tr['side'] > 0, 'long', 'short')
    tr['rand_side_str'] = np.where(tr['rand_side'] > 0, 'long', 'short')

    # ---- trades CSV ----
    vtcols = [c for c in tr.columns if c.startswith('vt')]
    out_cols = ['date', 'market', 'variant', 'period', 'strict_P3s', 'side_str', 'entry_time', 'entry_price',
                'exit_time', 'exit_price', 'reason', 'hold_min', 'gross_points', 'gross_usd', 'gross_bp',
                'net_points', 'net_usd', 'net_bp', 'e_ref', 'x_ref', 'dec_close', 'dec_vwap', 'ub', 'lb',
                'wrong_vwap', 'early_close_day', 'vol_tercile', 'sigma_d', 'drift_bp', 'rand_side_str',
                'rand_gross_points', 'rand_net_usd'] + vtcols
    csv = tr[out_cols].rename(columns={'side_str': 'side', 'rand_side_str': 'rand_side', 'e_ref': 'entry_ref_price',
                                       'x_ref': 'exit_ref_price', 'reason': 'exit_reason'})
    csv['date'] = csv['date'].dt.strftime('%Y-%m-%d')
    csv['entry_time'] = csv['entry_time'].dt.strftime('%Y-%m-%d %H:%M')
    csv['exit_time'] = csv['exit_time'].dt.strftime('%Y-%m-%d %H:%M')
    csv.to_csv(OUT_TRADES, index=False, float_format='%.10g')

    # ---- summary ----
    L = []
    w = L.append
    w('P1 NOISE-BAND BREAKOUT REPLICATION (Zarattini, Aziz & Barbon) -- literature_report.md section 7, P1')
    w(f'Generated by lit_p1_noiseband.py on {pd.Timestamp.now():%Y-%m-%d %H:%M}; runtime {time.time() - t_start:.0f}s')
    w('Data: Databento CME 1-min bars, continuous front contract by volume, unadjusted; RTH 09:30-16:00 ET.')
    w('Costs per micro: entry and exit each 1 tick adverse (market, stop and 15:59-close fills), $1.00 per round trip.')
    w('  MES round trip = 2 ticks x $1.25 + $1.00 = $3.50; MNQ = 2 ticks x $0.50 + $1.00 = $2.00.')
    w('Gross = from reference prices (next-bar open / stop price / 15:59 close) with no slippage or commission.')
    w('bp = 1e4 x P&L / entry reference price notional.  t(NW5) = day-level mean net $ / Newey-West(5 lags) SE on a')
    w('common calendar of all sessions in the period from the first day sigma(t) exists (no-trade days = 0).')
    w('Shrp = annualised daily Sharpe of net $ (1 micro).  yrs+ = calendar years (within the period) with >= 20')
    w('trades and positive mean net $ / such years.')
    w('')
    w('=' * 120)
    w('DATA / SESSION LOG')
    w('=' * 120)
    for line in log:
        w(line)
    for (mkt, lab), c in counts.items():
        w(f'{mkt} {lab:<12} sessions without 14 prior full sessions: {c["no_sigma"]}, roll days skipped after that: '
          f'{c["roll_skip"]}, abnormal-gap days excluded: {c["abnormal"]}, days simulated: {c["traded_days"]}')
    w('')

    main_variants = ['A', 'B']
    rand_reps = {}
    for mkt in MARKETS:
        cal_all = cals[mkt]
        w('=' * 120)
        w(f'{mkt} ({MICRO[mkt]}, ${MULT[mkt]:.0f}/pt) -- 1 micro per trade')
        w('=' * 120)
        for pname, a, b in PERIODS:
            cal = cal_all[period_mask(cal_all, a, b)]
            w('')
            w(f'--- {pname}  ({len(cal)} sessions) ---')
            w(HDR)
            for v in main_variants + ['A_scrambled', 'B_scrambled']:
                t = tr[(tr.market == mkt) & (tr.variant == v) & period_mask(tr['date'], a, b)]
                st = stats_block(t, cal)
                w(fmt_row(f'{v}', st))
                if v in main_variants and len(t):
                    for leg, sgn in [('long', 1), ('short', -1)]:
                        tl = t[t.side == sgn]
                        stl = stats_block(tl, cal)
                        w(fmt_row(f'  {v} {leg} leg', stl,
                                  f'  drift-only exp. {tl["drift_bp"].mean():+.2f} bp/tr' if len(tl) else ''))
                    # random-direction control
                    tr_r = t.assign(net_usd=t['rand_net_usd'], gross_points=t['rand_gross_points'],
                                    gross_usd=t['rand_gross_points'] * MULT[mkt],
                                    gross_bp=1e4 * t['rand_gross_points'] / t['e_ref'],
                                    net_bp=1e4 * t['rand_net_usd'] / (t['e_ref'] * MULT[mkt]),
                                    win=t['rand_net_usd'] > 0)
                    w(fmt_row(f'  {v} random-direction ctrl', stats_block(tr_r, cal)))
                    mv = (t['x_ref'] - t['e_ref']).to_numpy()
                    rr = np.random.default_rng(SEED + 7)
                    signs = rr.choice([-1.0, 1.0], size=(N_RAND_REPS, len(mv)))
                    tot = (signs @ mv) * MULT[mkt] - len(mv) * (2 * TICK * SLIP_TICKS * MULT[mkt] + COMM)
                    real = t['net_usd'].sum()
                    p = (1 + int((tot >= real).sum())) / (1 + N_RAND_REPS)
                    rand_reps[(mkt, v, pname)] = (tot.mean(), np.percentile(tot, 5), np.percentile(tot, 95), p)
                    w(f'  {v} random-direction, {N_RAND_REPS} reps: total net mean {tot.mean():,.0f} '
                      f'[5%..95%: {np.percentile(tot, 5):,.0f} .. {np.percentile(tot, 95):,.0f}]; strategy '
                      f'{real:,.0f}; empirical p (rand >= strategy) = {p:.4f}')
            # vol tercile
            w('  by volatility tercile (trailing 20-day 5-min RTH realised vol, expanding cut-offs after 250-day burn-in)')
            for v in main_variants:
                t = tr[(tr.market == mkt) & (tr.variant == v) & period_mask(tr['date'], a, b)]
                for q in [1, 2, 3]:
                    tq = t[t.vol_tercile == q]
                    st = stats_block(tq, cal)  # day-level t on the full calendar (other days = 0)
                    w(fmt_row(f'  {v} tercile {q} ({["low", "mid", "high"][q - 1]})', st))
                tn = t[t.vol_tercile.isna()]
                if len(tn):
                    w(f'  {v} burn-in (no tercile): {len(tn)} trades, net $/tr {tn.net_usd.mean():.2f}')
        # per-year table
        w('')
        w(f'--- {mkt} per calendar year (1 micro) ---')
        w(f'{"year":<6}{"var":<4} {"trades":>6} {"win%":>5} {"g $/tr":>8} {"g bp":>7} {"net$/tr":>8} {"net bp":>7} '
          f'{"net $ tot":>10} {"t(NW5)":>7} {"long n":>6} {"long $":>8} {"short n":>7} {"short $":>8} '
          f'{"rand $":>8} {"VT100k $":>10}')
        for y in sorted(tr['year'].unique()):
            caly = cal_all[cal_all.dt.year == y]
            for v in main_variants:
                t = tr[(tr.market == mkt) & (tr.variant == v) & (tr.year == y)]
                if len(t) == 0:
                    continue
                d = daily_series(t, 'net_usd', caly)
                lg = t[t.side > 0]; sh = t[t.side < 0]
                w(f'{y:<6}{v:<4} {len(t):>6} {100 * t.win.mean():>5.1f} {t.gross_usd.mean():>8.2f} '
                  f'{t.gross_bp.mean():>7.2f} {t.net_usd.mean():>8.2f} {t.net_bp.mean():>7.2f} {t.net_usd.sum():>10.0f} '
                  f'{nw_t(d):>7.2f} {len(lg):>6} {lg.net_usd.sum():>8.0f} {len(sh):>7} {sh.net_usd.sum():>8.0f} '
                  f'{t.rand_net_usd.sum():>8.0f} {t["vt100000_net_usd"].sum():>10.0f}')
        # exit reasons and diagnostics
        w('')
        w(f'--- {mkt} diagnostics (all periods) ---')
        for v in main_variants:
            t = tr[(tr.market == mkt) & (tr.variant == v)]
            rc = t['reason'].value_counts().to_dict()
            w(f'{v}: exit reasons {rc}; entries whose decision close was beyond the band but on the wrong side of '
              f'VWAP: {int(t.wrong_vwap.sum())} ({100 * t.wrong_vwap.mean():.1f}%); mean hold {t.hold_min.mean():.0f} min; '
              f'early-close-day trades {int(t.early_close_day.sum())}')
            wv = t[t.wrong_vwap]
            w(f'{v}: those wrong-side-of-VWAP entries: net $ total {wv.net_usd.sum():,.0f}, net $/tr '
              f'{wv.net_usd.mean():.2f} (they are taken because the spec enters on close > UB / < LB alone)')
            if v == 'B':
                imm = t[(t.reason == 'stop') & (t.x_slot == t.e_slot)]
                w(f'B: stopped out on the entry bar itself: {len(imm)} trades ({100 * len(imm) / len(t):.1f}%), '
                  f'of which {int(imm.wrong_vwap.sum())} had the entry close on the wrong side of VWAP')
        w('')

    # pooled ES + NQ
    w('=' * 120)
    w('POOLED ES + NQ (1 MES + 1 MNQ; day-level P&L summed across markets)')
    w('=' * 120)
    calp = pd.Series(sorted(set(cals['ES']) | set(cals['NQ'])))
    w(f'{"period":<30}{"var":<4} {"trades":>6} {"net $ tot":>10} {"net$/day":>9} {"t(NW5)":>7} {"Shrp":>6} '
      f'{"rand $ tot":>10}')
    for pname, a, b in PERIODS:
        cal = calp[period_mask(calp, a, b)]
        for v in main_variants:
            t = tr[(tr.variant == v) & period_mask(tr['date'], a, b)]
            d = daily_series(t, 'net_usd', cal)
            w(f'{pname:<30}{v:<4} {len(t):>6} {t.net_usd.sum():>10.0f} {d.mean():>9.2f} {nw_t(d):>7.2f} '
              f'{sharpe(d):>6.2f} {t.rand_net_usd.sum():>10.0f}')
    w('')

    # vol-targeted sizing
    for E in equity_list:
        tag = f'{int(E)}'
        w('=' * 120)
        w(f'VOLATILITY-TARGETED SIZING, E = ${E:,.0f} (fixed, not compounded): contracts = floor(E*0.02/(sigma_d*P*M)),')
        w('sigma_d = SD of the last 14 within-contract daily close-to-close returns, leverage cap 4x; same trade list.')
        w('=' * 120)
        for mkt in MARKETS:
            for pname, a, b in PERIODS:
                cal = cals[mkt][period_mask(cals[mkt], a, b)]
                for v in main_variants:
                    t = tr[(tr.market == mkt) & (tr.variant == v) & period_mask(tr['date'], a, b)]
                    if len(t) == 0:
                        continue
                    nct = t[f'vt{tag}_contracts']
                    valid = nct.notna()
                    tv = t[valid]
                    n0 = int((tv[f'vt{tag}_contracts'] == 0).sum())
                    traded = tv[tv[f'vt{tag}_contracts'] > 0]
                    med = np.median(tv[f'vt{tag}_contracts']) if len(tv) else np.nan
                    d1 = daily_series(t, 'net_usd', cal)
                    dv = daily_series(tv, f'vt{tag}_net_usd', cal)
                    # paired moving-block bootstrap (10-day blocks) of the Sharpe difference
                    rr = np.random.default_rng(SEED + 11)
                    T = len(d1); bl = 10; nb = int(np.ceil(T / bl))
                    diffs = []
                    for _ in range(500):
                        st_ = rr.integers(0, max(T - bl, 1), size=nb)
                        idx = (st_[:, None] + np.arange(bl)[None, :]).ravel()[:T]
                        diffs.append(sharpe(dv[idx]) - sharpe(d1[idx]))
                    diffs = np.array(diffs)
                    pct = np.percentile(tv[f'vt{tag}_contracts'], [5, 25, 50, 75, 95]) if len(tv) else []
                    w(f'{mkt} {pname:<28} {v}: trades {len(t)}, no sigma_d {int((~valid).sum())}, size 0 -> no trade '
                      f'{n0} ({100 * n0 / max(len(tv), 1):.1f}%), cap binding {int(tv[f"vt{tag}_capped"].sum())}; '
                      f'contracts p5/25/50/75/95 = {"/".join(f"{x:.0f}" for x in pct)}, share != median '
                      f'{100 * (tv[f"vt{tag}_contracts"] != med).mean():.1f}%')
                    w(f'    net $ total {tv[f"vt{tag}_net_usd"].sum():,.0f} (gross {tv[f"vt{tag}_gross_usd"].sum():,.0f}), '
                      f'net $/trade {traded[f"vt{tag}_net_usd"].mean():.2f}, return on E {100 * tv[f"vt{tag}_net_usd"].sum() / E:.1f}%, '
                      f't(NW5) {nw_t(dv):.2f}, Sharpe VT {sharpe(dv):.2f} vs 1-contract {sharpe(d1):.2f}; '
                      f'Sharpe diff boot 95% CI [{np.nanpercentile(diffs, 2.5):.2f}, {np.nanpercentile(diffs, 97.5):.2f}]')
            w('')
        w('Per calendar year, VT net $ (A / B):')
        for mkt in MARKETS:
            for v in main_variants:
                t = tr[(tr.market == mkt) & (tr.variant == v)]
                yy = t.groupby('year')[f'vt{tag}_net_usd'].sum()
                w(f'  {mkt} {v}: ' + ', '.join(f'{y}: {x:,.0f}' for y, x in yy.items()))
        w('')

    # sensitivity: abnormal-gap days
    w('=' * 120)
    w('SENSITIVITY: abnormal-gap days (March 2020 market-wide circuit-breaker halts) excluded above; their trades:')
    for mkt in MARKETS:
        for v in main_variants:
            df = halt_days.get((mkt, v))
            if df is None:
                w(f'  {mkt} {v}: no trades')
                continue
            w(f'  {mkt} {v}: {len(df)} trades, net $ {df.net_usd.sum():,.0f} (1 micro): '
              + '; '.join(f'{r.date:%Y-%m-%d} {"L" if r.side > 0 else "S"} {r.net_usd:,.0f}' for r in df.itertuples()))
    w('')
    w('HEADLINE (1 micro; primary = P3)')
    for mkt in MARKETS:
        for v in main_variants:
            for pname, a, b in PERIODS:
                cal = cals[mkt][period_mask(cals[mkt], a, b)]
                t = tr[(tr.market == mkt) & (tr.variant == v) & period_mask(tr['date'], a, b)]
                st = stats_block(t, cal)
                rm = rand_reps[(mkt, v, pname)]
                w(f'  {mkt} {v} {pname:<28} trades {st["trades"]:>5}  gross $ {t.gross_usd.sum():>9,.0f}  net $ '
                  f'{st["tot_net"]:>9,.0f}  net $/tr {st["net_usd"]:>6.2f}  t {st["t_nw"]:>5.2f}  yrs+ {st["yrs_pos"]:>5}  '
                  f'rand net $ (realisation) {t.rand_net_usd.sum():>9,.0f}  rand mean {rm[0]:>9,.0f}  p {rm[3]:.3f}')
    w('')
    w('ACCEPTANCE GATES (section 7 common protocol; 1 micro, net):  single pre-registered replication -> report exact t,')
    w('2-3 = "promising, needs a forward test"; sign consistency = net mean > 0 in >= 2/3 of years with >= 20 trades;')
    w('gross edge >= 1.5 x round-trip cost; beats the random-direction control (empirical p < 0.05).  DSR/SPA not computed.')
    for pname, a, b in PERIODS:
        for mkt in MARKETS:
            rt_cost = 2 * TICK * SLIP_TICKS * MULT[mkt] + COMM
            for v in main_variants:
                cal = cals[mkt][period_mask(cals[mkt], a, b)]
                t = tr[(tr.market == mkt) & (tr.variant == v) & period_mask(tr['date'], a, b)]
                st = stats_block(t, cal)
                yp, yn = (int(x) for x in st['yrs_pos'].split('/'))
                ratio = t.gross_usd.mean() / rt_cost
                p = rand_reps[(mkt, v, pname)][3]
                w(f'  {pname:<28} {mkt} {v}: t {st["t_nw"]:5.2f} | years {yp}/{yn} '
                  f'{"PASS" if yn and yp >= 2 * yn / 3 else "fail"} | gross/cost {ratio:5.2f} '
                  f'{"PASS" if ratio >= 1.5 else "fail"} | random-control p {p:.3f} {"PASS" if p < 0.05 else "fail"}')
    w('')
    w('Note on trade counts: the paper reports ~1.8 trades/day for SPY; variant A here makes ~0.9 round trips/day,')
    w('i.e. ~1.8 position changes/day, so the paper most likely counts entries and exits separately (not verified).')
    with open(OUT_SUMMARY, 'w') as f:
        f.write('\n'.join(L) + '\n')
    print("\n".join(L[-80:]))
    print(f'wrote {OUT_TRADES} ({len(csv)} rows) and {OUT_SUMMARY}; {time.time() - t_start:.0f}s')


if __name__ == '__main__':
    main()
