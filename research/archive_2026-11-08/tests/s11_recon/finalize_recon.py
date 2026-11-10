import json, numpy as np, pandas as pd, sys
R='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/s11_recon'
sys.path.insert(0,R+'/xmod')
import s11common as sc
out={}
for k,f,s in [('A','trades_A.csv','NQ'),('A1-MES','trades_A1-MES.csv','ES'),('A2-VWAP','trades_A2-VWAP.csv','NQ')]:
    t=pd.read_csv(f'{R}/xmod/{f}',parse_dates=['date'])
    p=pd.read_csv(f'{R}/roll_proxy_{s}.csv',index_col=0,parse_dates=True)
    for lab,tt in [('reconciled',t),('sens_rollproxy_skip',t[p.tradable_cons.reindex(t.date).values])]:
        d=tt.groupby('date').net_bp.sum()
        h=sc.headline(tt,'2010-07-26')
        out[f'{k}|{lab}']=dict(trades=len(tt),total_usd=round(tt.net_usd.sum(),2),usd_per_trade=round(tt.net_usd.mean(),3),
            net_bp=round(tt.net_bp.mean(),3),gross_bp=round(tt.gross_bp.mean(),3),t_nw5=round(sc.nw_t(d.values),3),t_iid=round(sc.iid_t(d.values),3),
            post2025=round(tt[tt.date>='2025-01-01'].net_usd.sum(),2),blocks_pos=h['blocks_positive'],tpy=round(h['trades_per_year'],2))
for k,v in out.items(): print(k,v)
json.dump(out,open(f'{R}/recon_A_headlines.json','w'),indent=1)
