import pandas as pd, numpy as np, os, json
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/'
P='/run/media/roflz/Disk 2/_/market_data/'
cm=pd.read_csv(P+'chosen_models_trades.csv',parse_dates=['date'])
ob=cm[cm.model=='overnight_break'].reset_index(drop=True); other=cm[cm.model!='overnight_break']
V=sorted(f[:-4] for f in os.listdir(B+'sweep_X/decisions'))
D={v:pd.read_csv(B+f'sweep_X/decisions/{v}.csv',parse_dates=['date']) for v in V}
x0=D[V[0]]
assert len(ob)==1731 and (ob.date==x0.date).all() and (ob.side==x0.side).all() and np.allclose(ob.usd,x0.net_usd)
usd=ob.usd.to_numpy(); yr=ob.date.dt.year.to_numpy(); N=len(usd)
S={v:D[v].skip.to_numpy().astype(bool) for v in V}; E={v:D[v].eligible.to_numpy().astype(bool) for v in V}

# --- independent recompute of W (M1 q67 L250) and M3 from stored inputs + project cash-day calendar
ds=pd.read_pickle(P+'data/daily_sessions_NQ.pkl')
cash=pd.DatetimeIndex(sorted(pd.to_datetime(ds.index[ds.cash_day.astype(bool)])))
cash=cash[cash>=pd.Timestamp('2011-01-01')]
pos=cash.get_indexer(ob.date); assert (pos>=0).all()
m1=(D['M1_q67_L250'].R_pts/D['M1_q67_L250'].raw_signal_close).to_numpy()
def lookback(meas,q,L):
    sk=np.zeros(N,bool); el=np.zeros(N,bool)
    for k in range(N):
        if pos[k] < L: continue
        el[k]=True
        w=(pos>=pos[k]-L)&(pos<pos[k])
        sk[k]= meas[k] > np.percentile(meas[w],q)
    return sk,el
for q,L in [(67,250),(90,500),(50,125)]:
    sk,el=lookback(m1,q,L); v=f'M1_q{q}_L{L}'
    print('recompute',v,'elig',el.sum(),'skip',sk.sum(),'skipdiff',(sk!=S[v]).sum(),'eligdiff',(el!=E[v]).sum())
m4=D['M4_q50_L250'].atr5_signal/D['M4_q50_L250'].atr_med60
sk,el=lookback(m4.to_numpy(),50,250); print('recompute M4_q50_L250 skipdiff',(sk!=S['M4_q50_L250']).sum())
r=D['M3_X250'].R_pts.to_numpy()
for X in [75,100,150,200,250,300]:
    print('M3',X,'skipdiff',((r*2+2>X)!=S[f'M3_X{X}']).sum())

# --- metrics from project CSV
def ddw(dates,u):
    d=pd.Series(u).groupby(pd.Series(dates)).sum().sort_index(); eq=np.r_[0,d.cumsum().to_numpy()]
    return (np.maximum.accumulate(eq)-eq).max(), d.min()
rows=[]
for v in V:
    s=S[v]; k=~s
    mdd,mw=ddw(ob.date[k].to_numpy(),usd[k]); bdd,bw=ddw(np.r_[ob.date[k],other.date],np.r_[usd[k],other.usd])
    rows.append(dict(variant=v,n=int(s.sum()),rem=usd[s].sum(),r1017=usd[s&(yr<=2017)].sum(),r1826=usd[s&(yr>=2018)].sum(),
       r2426=usd[s&(yr>=2024)].sum(),mdd=mdd,mw=mw,bdd=bdd,bw=bw,book=np.r_[usd[k],other.usd].sum()))
R=pd.DataFrame(rows).set_index('variant')
xv=pd.read_csv(B+'sweep_X/variants.csv').set_index('variant')
for a,b in [('rem','removed_usd'),('mdd','model_max_dd'),('mw','model_worst_day'),('bdd','book_max_dd'),('bw','book_worst_day'),('book','book_net')]:
    print('metric',a,'maxdiff vs X',(R[a]-xv.loc[R.index,b]).abs().max())
print('base',usd.sum(),ddw(ob.date,usd),ddw(np.r_[ob.date,other.date],np.r_[usd,other.usd]))

# --- precise single-variant random percentiles (100k draws)
rng=np.random.default_rng(12345); NB=100000
pct={}
for v in V:
    n=int(S[v].sum()); pool=usd[E[v]]
    tot=np.empty(NB)
    for c in range(0,NB,10000):
        K=rng.random((10000,len(pool))); idx=np.argpartition(K,n-1,axis=1)[:,:n]; tot[c:c+10000]=pool[idx].sum(1)
    pct[v]=100*np.mean(tot<=R.loc[v,'rem'])
R['pct100k']=pd.Series(pct)

# --- family-wise, three nulls
best=R.rem.min(); bestv=R.rem.idxmin()
def fw_from(mins): return 100*np.mean(mins<=best), np.median(mins), np.percentile(mins,5)
out={}
# (1) permutation: one relabelling of $ per draw, stratified so every eligible pool maps to itself; actual masks kept
el_lvls=[np.ones(N,bool),E['M1_q50_L125'],E['M1_q50_L250'],E['M1_q50_L500']]
strata=[]
for i in range(4):
    m=el_lvls[i]&~(el_lvls[i+1] if i<3 else np.zeros(N,bool)); strata.append(np.flatnonzero(m))
print('strata sizes',[len(s) for s in strata])
M=np.column_stack([S[v] for v in V]).astype(float)
for NDR,tag in [(1000,'perm1k'),(20000,'perm20k')]:
    rng=np.random.default_rng(12345); mins=np.empty(NDR)
    for j in range(NDR):
        u=usd.copy()
        for st in strata: u[st]=usd[rng.permutation(st)]
        mins[j]=(u@M).min()
    out[tag]=fw_from(mins)
# (1b) unstratified within-pool: each variant random subset, joint dependence = actual masks via global permutation of eligible core only
# (2) comonotone keys (X), (3) independent (Y), each 20k draws
for tag in ['common','indep']:
    rng=np.random.default_rng(12345); NDR=20000; mins=np.full(NDR,np.inf)
    if tag=='common':
        for c in range(0,NDR,2000):
            U=rng.random((2000,N))
            for v in V:
                n=int(S[v].sum()); cols=np.flatnonzero(E[v]); idx=np.argpartition(U[:,cols],n-1,axis=1)[:,:n]
                mins[c:c+2000]=np.minimum(mins[c:c+2000],usd[cols][idx].sum(1))
    else:
        for v in V:
            n=int(S[v].sum()); cols=np.flatnonzero(E[v])
            for c in range(0,NDR,2000):
                U=rng.random((2000,len(cols))); idx=np.argpartition(U,n-1,axis=1)[:,:n]
                mins[c:c+2000]=np.minimum(mins[c:c+2000],usd[cols][idx].sum(1))
    out[tag+'20k']=fw_from(mins)
print('FW best',bestv,best); 
for k,vv in out.items(): print('FW',k,'pctile %.1f median %.1f p5 %.1f'%vv)
# M3-only sub-family and M3_X250 permutation p-value from same perm
R.round(2).to_csv(B+'sweep_recon/recon_variants.csv')
print(R[['n','rem','r1017','r1826','pct100k']].assign(px=xv.random_pctile).sort_values('rem').head(12).round(1).to_string())
print('min pct100k',R.pct100k.min(), R.pct100k.idxmin(), 'n<=5:',(R.pct100k<=5).sum())
json.dump({k:list(map(float,vv)) for k,vv in out.items()},open(B+'sweep_recon/familywise.json','w'),indent=1)
