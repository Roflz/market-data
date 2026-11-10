"""Average price path after each entry, in the trade's direction (gross bp, before costs).
If the path never rises above costs at any horizon, no exit rule can make the entry profitable."""
import numpy as np, pandas as pd
S = '/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests'
d = pd.read_csv('data/NQ_fut_1m.csv', usecols=['ts_event', 'Open', 'Close', 'instrument_id'])
t = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert('America/New_York')
d['day'] = t.dt.tz_localize(None).dt.normalize(); d['m'] = t.dt.hour * 60 + t.dt.minute
d = d[(d.m >= 8 * 60 + 30) & (d.m <= 16 * 60)]
G = {k: (g.m.to_numpy(), g.Open.to_numpy(), g.Close.to_numpy(), g.instrument_id.to_numpy()) for k, g in d.groupby('day')}
H = [5, 10, 15, 30, 45, 60, 90, 120, 180]

def paths(tr, label):
    out = []
    for r in tr.itertuples(index=False):
        day = pd.Timestamp(r.date); hh, mm = map(int, r.entry_time.split(':')); m0 = hh * 60 + mm
        if day not in G: continue
        m, o, c, inst = G[day]
        i = np.searchsorted(m, m0)
        if i >= len(m) or m[i] != m0: continue
        sgn = 1 if r.side == 'long' else -1
        row = []
        for h in H:
            j = np.searchsorted(m, m0 + h - 1)            # close of the bar ending at entry + h minutes
            ok = j < len(m) and m[j] == m0 + h - 1 and inst[j] == inst[i]
            row.append(1e4 * sgn * (c[j] / o[i] - 1) if ok else np.nan)
        out.append(row)
    a = np.array(out, float)
    mu = np.nanmean(a, 0); se = np.nanstd(a, 0) / np.sqrt(np.sum(~np.isnan(a), 0))
    print(f'{label:38s} n={len(a):5d}  ' + '  '.join(f'{h:>3d}m {x:+5.1f}' for h, x in zip(H, mu)))
    print(f'{"":38s}           ' + '  '.join(f'   t {x / s:+5.1f}' for x, s in zip(mu, se)))

def load(f, side='side_x'):
    x = pd.read_csv(f); return x.assign(side=x[side] if side in x else x.side)
cost_bp = lambda px: 1e4 * 1.0 / px
print('cost of one MNQ round trip ~ 1 NQ point = 5 bp at NQ 2,000 (2010), 1.4 bp at 7,000 (2018), 0.4 bp at 25,000 (2025)\n')
paths(load(f'{S}/s11_recon/cmp_A.csv'), 'A calm-day midday fade (MNQ)')
paths(load(f'{S}/s11_recon/cmp_C.csv'), 'C reverse after failed opening range')
paths(load(f'{S}/s11_recon/cmp_B.csv'), 'B explosive-move fade')
l1 = pd.read_csv(f'{S}/l1b/L1b_MNQ_nfp_exit945.csv').assign(entry_time='08:45')
paths(l1, 'L1 jobs-report fade (from 8:45)')
paths(l1.assign(side=np.where(l1.side == 'long', 'short', 'long')), 'L1 opposite side (check)')
