import pandas as pd, numpy as np
R="/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/next/rebal/"
def ts(x): x=np.asarray(x); return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
for f in ['trades_A_MNQ.csv','trades_P_MNQ.csv','trades_A_MES.csv']:
    t=pd.read_csv(R+f,parse_dates=['date'])
    ex=t[t.date.dt.year!=2020]
    eq=t.net_usd.cumsum(); dd=(eq-eq.cummax()).min()
    top=t.net_usd.sort_values(ascending=False)
    print(f, 'n',len(t),'ex-2020 total',round(ex.net_usd.sum()),'t',round(ts(ex.net_usd),2),
          '| ex-Feb-Apr2020', round(t[~((t.date>='2020-02-01')&(t.date<'2020-05-01'))].net_usd.sum()),
          '| top10 trades sum',round(top.head(10).sum()),'| worst trade', round(t.net_usd.min()),'| maxDD',round(dd),
          '| bp t', round(ts(t.net_bp),2), '| ex-2020 bp t', round(ts(ex.net_bp),2), '| bp t 2023+', round(ts(t[t.date>='2023'].net_bp),2))
    print(t.groupby('max_contracts').net_usd.agg(['count','sum','mean']).round(1).to_string())
    print('median trade', t.net_usd.median(), 'win rate', (t.net_usd>0).mean().round(3))
