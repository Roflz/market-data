import pandas as pd, numpy as np, sys
S='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
pairs={'A':('trades_A.csv','A_trades.csv'),'A1':('trades_A1-MES.csv','A1_trades.csv'),'A2':('trades_A2-VWAP.csv','A2_trades.csv'),
'B':('trades_B.csv','B_trades.csv'),'B-MES':('trades_B-MES.csv','B-MES_trades.csv'),'B1':('trades_B1.csv','B1_trades.csv'),
'C':('trades_C_reverse_leg.csv','C_reverse_leg_trades.csv'),'C1':('trades_C1-calm_reverse_leg.csv','C1_calm_reverse_leg_trades.csv'),'C2':('trades_C2-target_reverse_leg.csv','C2_target_reverse_leg_trades.csv')}
out=[]
for k,(fx,fy) in pairs.items():
    x=pd.read_csv(S+'s11_X/'+fx); y=pd.read_csv(S+'s11_Y/'+fy)
    key=['date','entry_time']
    m=x.merge(y,on=key,how='outer',suffixes=('_x','_y'),indicator=True)
    both=m[m._merge=='both']
    cols=['side','exit_time','entry','exit','net_usd']
    diff=np.zeros(len(both),bool)
    for c in cols:
        a,b=both[c+'_x'],both[c+'_y']
        if a.dtype.kind in 'fi': d=(a-b).abs()>1e-6
        else: d=a.astype(str)!=b.astype(str)
        diff|=d.values
    print(f"{k}: X={len(x)} Y={len(y)} matched={len(both)} identical={(~diff).sum()} differ={diff.sum()} Xonly={(m._merge=='left_only').sum()} Yonly={(m._merge=='right_only').sum()}  X$={x.net_usd.sum():.1f} Y$={y.net_usd.sum():.1f}")
    m.to_csv(f'/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/s11_recon/cmp_{k}.csv',index=False)
