import pandas as pd, numpy as np
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
for r in ['S3','S3-V1','S3-V2']:
    x=pd.read_csv(B+f's12_X/trades_{r}.csv'); y=pd.read_csv(B+f's12_Y/trades_{r}.csv')
    m=x.merge(y,on='date',suffixes=('_x','_y'))
    for c in ['placebo_net_bp','placebo_gross_bp']:
        d=~np.isclose(m[c+'_x'],m[c+'_y'],atol=1e-6)
        print(r,c,'diffs',d.sum(),'meanX',m[c+'_x'].mean(),'meanY',m[c+'_y'].mean())
    d=~np.isclose(m['placebo_net_bp_x'],m['placebo_net_bp_y'],atol=1e-6)
    print(m.loc[d,['date','placebo_net_bp_x','placebo_net_bp_y','placebo_gross_bp_x','placebo_gross_bp_y','n_NQ','n_ES','k_x']].head(8).to_string())
    print('outright', m.NQ_outright_lasthalf_bp_dir.mean(), m.nq_last30_bp_dir.mean(), m.ES_outright_lasthalf_bp_dir.mean(), m.es_last30_bp_dir.mean())
