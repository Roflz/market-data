"""Capped-stop test (pre-registered in the review doc, section 6.2 'Capped stops'). Run from the project folder."""
import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import calendar_days as cd, chosen_models as cm, exits_compare as ec, exits_engine as ee, lit_p5_orb as p5
S = '/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad'
CAPS = {"current": None, **{f"{c*100:.2f}%": c for c in (0.0010, 0.0015, 0.0020, 0.0025, 0.0030, 0.0040, 0.0050)}}
ds = cm.sessions(); cash = ds.index[ds.cash_day]; expiry = cd.expiry_fridays(cash)
after_drop, fed = cm.skip_days()
live = pd.read_csv('chosen_models_trades.csv', parse_dates=['date'])
orb_days = set(live[live.model == 'opening_range'].date)

def daily(dates, R):
    return pd.Series(R, index=pd.DatetimeIndex(dates)).groupby(level=0).sum()

def overnight(slip_ticks):
    ee.SLIP = slip_ticks * 0.25
    ec.init(); D = ec.G['NQ']; sigs = ec.G[('sets', 'NQ')]['Overnight break + daily trend']
    adj = (ds.close_adj - ds.close_raw)
    out = {}
    for name, cap in CAPS.items():
        extra = None
        if cap is not None:
            extra = {}
            for i, d in sigs:
                raw = D.Close[i] - adj.get(pd.Timestamp(D.sess[i]), 0.0)
                extra[i] = {"R_pts": min(2.0 * D.atr5[i], cap * raw)}
        t = ee.run(D, sigs, "hold", k0=2.0, extra=extra)
        date = pd.to_datetime(D.sess[t.bar.to_numpy()])
        keep = date.isin(cash) & ~date.isin(expiry) & ~date.isin(after_drop)
        net = t.pts.to_numpy() - ee.SPEC['NQ']['comm'] / ee.SPEC['NQ']['usd'] - (slip_ticks - 1) * 0 # comm only; slip in prices
        out[name] = (date[keep], (net / t.R_pts.to_numpy())[keep], (net * 2.0)[keep])
    return out

def opening(slip_ticks):
    sys.argv = ['x', str(slip_ticks), 'NQ']
    ns = {}; exec(open(f'{S}/orb_grid.py').read().split('for sym in ONLY:')[0], ns)
    mk = p5.MARKETS['NQ']; dates, g, inst = p5.load_market('NQ'); sess, Cff, _ = p5.build_sessions('NQ', dates, g, inst)
    E0 = ns['entries']('A', 5, sess, g, Cff, mk['min_R'])
    E0 = E0[pd.to_datetime(E0.date).isin(orb_days)].reset_index(drop=True)
    c = ns['COMBOS'].index((None, 'none')); out = {}
    for name, cap in CAPS.items():
        E = E0.copy()
        if cap is not None: E['R0'] = np.minimum(E.R0, cap * E.fill)
        E2, Rm, Um = ns['simulate'](E, g, Cff, 1.0, 'A', 0.0, mk['ppt'])
        out[name] = (pd.to_datetime(E2.date), Rm[:, c], Um[:, c])
    return out

ERAS = [('2010-13', '2010', '2013'), ('2014-17', '2014', '2017'), ('2018-20', '2018', '2020'), ('2021-23', '2021', '2023'), ('2024-26', '2024', '2026')]
rows = []
for model, fn in (('overnight break', overnight), ('opening range', opening)):
    for slip in (1, 2):
        res = fn(slip)
        print(f"\n{model}, {slip} tick(s) per fill: net $ at 1 micro by period (stopped-out share in brackets)")
        print(f"  {'stop':9s} " + " ".join(f"{e[0]:>9s}" for e in ERAS) + f" {'total':>9s} {'2018-26':>9s}")
        for name, (dts, R, U) in res.items():
            u = pd.Series(U, index=pd.DatetimeIndex(dts))
            vals = [u[a:b].sum() for _, a, b in ERAS]
            print(f"  {name:9s} " + " ".join(f"{v:+9,.0f}" for v in vals) + f" {u.sum():+9,.0f} {u['2018':].sum():+9,.0f}")
            y = u.groupby(u.index.year).sum()
            for yr, v in y.items(): rows.append(dict(model=model, slip=slip, stop=name, year=yr, usd=v))
pd.DataFrame(rows).pivot_table(index=['model', 'slip', 'stop'], columns='year', values='usd').round(0).to_csv(f'{S}/cap_usd_by_year.csv')
print(f"\nper-year table saved: {S}/cap_usd_by_year.csv")
