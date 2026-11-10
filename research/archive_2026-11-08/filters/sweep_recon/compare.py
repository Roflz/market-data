import pandas as pd, numpy as np, os
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/'
vs=sorted(f[:-4] for f in os.listdir(B+'sweep_X/decisions'))
vy=sorted(f[:-4] for f in os.listdir(B+'sweep_Y/decisions'))
print(len(vs),len(vy),vs==vy)
tot=0
for v in vs:
    x=pd.read_csv(B+f'sweep_X/decisions/{v}.csv'); y=pd.read_csv(B+f'sweep_Y/decisions/{v}.csv')
    assert len(x)==len(y)==1731
    assert (x.date==y.date).all() and (x.side==y.side).all() and np.allclose(x.net_usd,y.net_usd)
    ds=(x.skip!=y.skip).sum(); de=(x.eligible!=y.eligible).sum()
    th=np.nanmax(np.abs(x.threshold-y.threshold)) if x.threshold.notna().any() else 0
    me=np.nanmax(np.abs(x.measure-y.measure_used)/np.abs(y.measure_used))
    tot+=ds+de
    print(v,'skipdiff',ds,'eligdiff',de,'thr maxabs %.3g'%th,'meas maxrel %.3g'%me, 'n',x.skip.sum())
print('total diffs',tot)
xv=pd.read_csv(B+'sweep_X/variants.csv').set_index('variant'); yv=pd.read_csv(B+'sweep_Y/sweep_variants.csv').set_index('variant')
pairs=[('removed_n','n_removed'),('removed_usd','removed_usd'),('kept_usd','kept_usd'),('welch_t_kept_minus_removed','welch_t_kept_minus_removed'),
('model_max_dd','model_mdd'),('model_worst_day','model_worst_day'),('book_max_dd','book_mdd'),('book_worst_day','book_worst_day'),('book_net','book_usd'),
('model_max_dd_2tick','model_mdd_2tick'),('model_worst_day_2tick','model_worst_day_2tick'),('book_max_dd_2tick','book_mdd_2tick'),('book_worst_day_2tick','book_worst_day_2tick'),('book_net_2tick','book_usd_2tick'),
('removed_usd_2tick','removed_usd_2tick'),('kept_usd_2tick','kept_usd_2tick'),('removed_usd_2010_2017','removed_usd_2010-2017'),('removed_usd_2018_2026','removed_usd_2018-2026'),
('removed_usd_2010-13','removed_usd_2010-13'),('removed_usd_2014-17','removed_usd_2014-17'),('removed_usd_2018-20','removed_usd_2018-20'),('removed_usd_2021-23','removed_usd_2021-23'),('removed_usd_2024-26','removed_usd_2024-26'),
('random_pctile','random_pct')]
for a,b in pairs:
    d=(xv[a]-yv.loc[xv.index,b]).abs()
    print(a, 'maxdiff %.4f'%d.max(), d.idxmax())
