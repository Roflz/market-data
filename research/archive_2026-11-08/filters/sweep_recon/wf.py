import pandas as pd, numpy as np, os
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/'
V=sorted(f[:-4] for f in os.listdir(B+'sweep_Y/decisions'))
D={v:pd.read_csv(B+f'sweep_Y/decisions/{v}.csv',parse_dates=['date']) for v in V}
usd=D[V[0]].net_usd.to_numpy(); yr=D[V[0]].date.dt.year.to_numpy()
years=np.arange(2011,2027)
REM=pd.DataFrame({v:pd.Series(np.where(D[v].skip,usd,0)).groupby(yr).sum().reindex(years,fill_value=0) for v in V})
allY=pd.Series(usd).groupby(yr).sum()
def run(mode, tie_pick=None):
    tot=0;rows=[]
    for y in range(2013,2027):
        cum=-REM.loc[REM.index<y].sum(); b=cum.max(); lead=list(cum.index[cum==b])
        if len(lead)>1: pick=tie_pick(lead) if tie_pick else None
        elif mode=='none_if_le0' and b<=0: pick=None
        else: pick=lead[0]
        d=-(REM.loc[y,pick] if pick else 0); tot+=d; rows.append((y,pick,b,d))
    return tot,rows
t,rows=run('none_if_le0'); print('main',t); [print(r) for r in rows]
print('always pick best',run('always')[0])
for f,tag in [(lambda l:l[0],'tie->first'),(lambda l:l[-1],'tie->last')]:
    print(tag,run('none_if_le0',f)[0],run('always',f)[0])
print('X wf == Y wf:', np.allclose(pd.read_csv(B+'sweep_X/walk_forward.csv').wf_usd, pd.read_csv(B+'sweep_Y/walk_forward.csv').wf_usd))
pw=D['M1_q67_L250']; s=pw.skip.to_numpy(); e=pw.eligible.to_numpy(); pool=usd[e]; n=s.sum()
rng=np.random.default_rng(12345); tot=np.concatenate([pool[np.argpartition(rng.random((10000,len(pool))),n-1,axis=1)[:,:n]].sum(1) for _ in range(10)])
print('W pct100k',100*np.mean(tot<=usd[s].sum()), 'mean',tot.mean())
