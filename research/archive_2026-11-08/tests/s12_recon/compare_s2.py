import pandas as pd, numpy as np
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
for r in ['S2','S2-V1','S2-V2']:
    xm=pd.read_csv(B+f's12_X/trades_{r}.csv'); ym=pd.read_csv(B+f's12_Y/months_{r}.csv')
    m=xm.merge(ym,left_on='hold_month',right_on='month',suffixes=('_x','_y'))
    print(r,len(xm),len(ym),len(m),'d diff',(m.d_x!=m.d_y).sum(),'net_usd diff',(~np.isclose(m.net_usd_x,m.net_usd_y)).sum(),'net_bp diff',(~np.isclose(m.net_bp_x,m.net_bp_y)).sum(), 'seg diff',(m.n_segments!=m.segments).sum())
    xs=pd.read_csv(B+f's12_X/trades_{r}_segments.csv'); ys=pd.read_csv(B+f's12_Y/trades_{r}.csv')
    print('  segs',len(xs),len(ys))
    xs=xs.reset_index(drop=True); ys=ys.reset_index(drop=True)
    for a,b in [('entry_date','date'),('exit_date','exit_date'),('exit_time','exit_time'),('entry_time','entry_time'),('n_lead','n_a'),('n_ES','n_es'),('lead_entry','entry'),('lead_exit','exit'),('ES_entry','es_entry'),('ES_exit','es_exit'),('net_usd','net_usd')]:
        A=xs[a]; Bc=ys[b]
        d=(~np.isclose(A.astype(float),Bc.astype(float))) if A.dtype.kind in 'fi' else (A.astype(str)!=Bc.astype(str))
        if d.sum(): print('   diff',a,d.sum(), pd.concat([xs.loc[d,['hold_month',a]],ys.loc[d,[b]]],axis=1).head(4).to_string())
