import pandas as pd, numpy as np, sys
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
out=[]
for r in ['S1','S1-V1','S1-V2','S3','S3-V1','S3-V2']:
    x=pd.read_csv(B+f's12_X/trades_{r}.csv'); y=pd.read_csv(B+f's12_Y/trades_{r}.csv')
    x=x.rename(columns={'n_NQ':'nN','n_ES':'nE','NQ_entry':'eN','NQ_exit':'xN','ES_entry':'eE','ES_exit':'xE'})
    y=y.rename(columns={'n_nq':'nN','n_es':'nE'})
    m=x.merge(y,on='date',how='outer',suffixes=('_x','_y'),indicator=True)
    both=m[m._merge=='both']
    print(r,'X',len(x),'Y',len(y),'both',len(both),'onlyX',(m._merge=='left_only').sum(),'onlyY',(m._merge=='right_only').sum())
    cols=['side','entry_time','nN','nE','eN','xN','eE','xE','exit_reason']
    for c in cols:
        a=both[c+'_x']; b=both[c+'_y']
        if a.dtype.kind=='f' or b.dtype.kind=='f': d=~np.isclose(a.astype(float),b.astype(float))
        else: d=a.astype(str)!=b.astype(str)
        if d.sum(): print('  diff',c,d.sum(), both.loc[d,['date',c+'_x',c+'_y']].head(5).to_string())
    d=~np.isclose(both.net_usd_x,both.net_usd_y,atol=0.01)
    print('  net_usd diffs',d.sum(),'sum X',x.net_usd.sum(),'sum Y',y.net_usd.sum())
    if d.sum(): print(both.loc[d,['date','net_usd_x','net_usd_y','exit_time_x','exit_time_y','xN_x','xN_y','xE_x','xE_y','nN_x','nN_y','nE_x','nE_y']].head(10).to_string())
    db=~np.isclose(both.net_bp_x,both.net_bp_y,atol=1e-6); print('  net_bp diffs',db.sum())
