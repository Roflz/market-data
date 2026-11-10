import pandas as pd, numpy as np, math
from fractions import Fraction
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
def size_exact(k):
    # exact-tie-aware: relative errors equal up to 1e-9 are ties -> smallest n
    rels=[]
    for n in range(1,11):
        x=n*k; r=math.floor(x+0.5); rel=abs(r-x)/x
        if rel<=0.05+1e-12: return n,max(1,r),False
        rels.append(rel)
    mn=min(rels); n=next(i+1 for i,v in enumerate(rels) if v<=mn+1e-9)
    return n,max(1,math.floor(n*k+0.5)),True
for r,f,nc,ec in [(r,f'trades_{r}.csv','n_NQ','n_ES') for r in ['S1','S1-V1','S1-V2','S1-C2','S3','S3-V1','S3-V2']]+[(r,f'trades_{r}_segments.csv','n_lead','n_ES') for r in ['S2','S2-V1','S2-V2']]:
    x=pd.read_csv(B+'s12_X/'+f)
    res=[size_exact(k) for k in x.k]
    n=np.array([a for a,b,c in res]); e=np.array([b for a,b,c in res]); t=np.array([c for a,b,c in res])
    bad=(n!=x[nc].values)|(e!=x[ec].values)
    near=np.array([min(abs(abs(math.floor(m*k+0.5)-m*k)/(m*k)-0.05) for m in range(1,11)) for k in x.k])
    print(r,len(x),'noqualify',t.sum(),'X wrong',bad.sum(), x.loc[bad,['date' if 'date' in x else 'hold_month','k',nc,ec]].assign(n_ok=n[bad],e_ok=e[bad]).to_string() if bad.sum() else '', 'min dist to 5% boundary',near.min())
