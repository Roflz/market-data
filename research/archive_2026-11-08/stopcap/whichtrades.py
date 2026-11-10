"""Capped-stop test (pre-registered in the review doc, section 6.2 'Capped stops'). Run from the project folder."""
import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import calendar_days as cd, chosen_models as cm, exits_compare as ec, exits_engine as ee, lit_p5_orb as p5
S = '/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad'
CAPS = {"current": None, "0.20%": 0.0020, "0.10%": 0.0010}
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
        out[name] = (date[keep], (net / t.R_pts.to_numpy())[keep], (net * 2.0)[keep], t.bar.to_numpy()[keep], t.exit.to_numpy()[keep], t.R_pts.to_numpy()[keep])
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
        out[name] = (pd.to_datetime(E2.date), Rm[:, c], Um[:, c], np.arange(len(E2)), np.where(Rm[:, c] <= -0.95, 'stop', 'close'), E2.R0.to_numpy())
    return out

for model, fn in (('overnight break', overnight), ('opening range', opening)):
    res = fn(1)
    cur = pd.DataFrame({'date': res['current'][0], 'usd': res['current'][2], 'id': res['current'][3], 'exit': res['current'][4], 'risk_pts': res['current'][5]}).set_index('id')
    print(f"\n######## {model}, current stop, 1 micro, 1 tick (all trades)")
    cur['width'] = pd.qcut(cur.risk_pts / cur.groupby(cur.date.dt.year).risk_pts.transform('median'), 3, labels=['narrow third', 'middle third', 'wide third'])
    g = cur.groupby('width', observed=True)
    print(pd.DataFrame({'trades': g.size(), 'stopped': g.apply(lambda x: (x.exit == 'stop').mean()).round(2),
                        'stop losses $': g.apply(lambda x: x.usd[x.exit == 'stop'].sum()).round(0),
                        'held-to-close $': g.apply(lambda x: x.usd[x.exit != 'stop'].sum()).round(0),
                        'net $': g.usd.sum().round(0)}).to_string())
    for cap in ('0.20%', '0.10%'):
        cp = pd.DataFrame({'usd': res[cap][2], 'id': res[cap][3], 'exit': res[cap][4]}).set_index('id')
        j = cur.join(cp, rsuffix='_cap', how='inner')
        changed = j[(j.exit_cap == 'stop') & (j.exit != 'stop')]          # cap stops it, current stop does not
        win = changed.usd > 0
        print(f"  cap {cap}: {len(changed)} trades the cap stops out that the current stop holds. Under the current stop, "
              f"{win.mean():.0%} of them ended as winners (+${changed.usd[win].sum():,.0f}) and {1 - win.mean():.0%} as losers "
              f"(${changed.usd[~win].sum():,.0f}); under the cap these same trades made ${changed.usd_cap.sum():,.0f}.")
        both = j[(j.exit == 'stop') & (j.exit_cap == 'stop')]
        print(f"           trades stopped by both: current ${both.usd.sum():,.0f} vs cap ${both.usd_cap.sum():,.0f} (the cap's smaller losses)")
