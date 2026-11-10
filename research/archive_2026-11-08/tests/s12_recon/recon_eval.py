"""Reconciled Section 12 evaluation. Base = per-trade lists on which X and Y agree (prices, sides, bars, bp identical);
correction = integer sizing on exact relative-error ties (smallest n wins). Recomputes all criteria and diagnostics."""
import pandas as pd, numpy as np, math, json
from scipy import stats
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
R=B+'s12_recon/'
DATA_END=pd.Timestamp('2026-11-06')

def size_exact(k):
    rels=[]
    for n in range(1,11):
        x=n*k; r=math.floor(x+0.5); rel=abs(r-x)/x
        if rel<=0.05+1e-12: return n,max(1,r)
        rels.append(rel)
    mn=min(rels); n=next(i+1 for i,v in enumerate(rels) if v<=mn+1e-9)
    return n,max(1,math.floor(n*k+0.5))

corrections=[]
def fix_sizes(df,rule,nc,ec,datecol):
    df=df.copy()
    for i,k in df.k.items():
        n,e=size_exact(k)
        if n!=df.at[i,nc] or e!=df.at[i,ec]:
            assert abs(e/n - df.at[i,ec]/df.at[i,nc])<1e-12, 'ratio changes -> bp would change'
            f=n/df.at[i,nc]
            old=df.at[i,'net_usd']
            for c in ['gross_usd','cost_usd','net_usd','net_usd_flipdir','placebo_net_usd','NQ_notional_usd','lead_notional_usd','gross_long_usd']:
                if c in df: df.at[i,c]=df.at[i,c]*f
            corrections.append(dict(rule=rule,date=df.at[i,datecol],k=k,X=(int(df.at[i,nc]),int(df.at[i,ec])),correct=(n,e),net_usd_old=old,net_usd_new=df.at[i,'net_usd']))
            df.at[i,nc]=n; df.at[i,ec]=e
    return df

def tstat(x): x=np.asarray(x,float); return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
def nw_t(x,L):
    x=np.asarray(x,float); n=len(x); u=x-x.mean(); g0=(u*u).sum()/n; s=g0
    for l in range(1,L+1): s+=2*(1-l/(L+1))*(u[l:]*u[:-l]).sum()/n
    return x.mean()/np.sqrt(s/n)
def pval(x): t=tstat(x); return 2*stats.t.sf(abs(t),len(x)-1)
def block(y): return '2026' if y>=2026 else f'{y - (y%2)}-{str(y - (y%2)+1)[2:]}'

def common(df,dates,netbp,grossbp,costbp,usd,minblk=10):
    y=dates.dt.year
    o=dict(n=len(df),mean_net_bp=netbp.mean(),mean_gross_bp=grossbp.mean(),mean_cost_bp=costbp.mean(),
           net_usd_per_trade=usd.mean(),total_usd=usd.sum(),t=tstat(netbp),gross_t=tstat(grossbp))
    blk=pd.DataFrame({'b':y.map(block),'v':netbp.values,'u':usd.values}).groupby('b').agg(n=('v','size'),mean_net_bp=('v','mean'),usd=('u','sum'))
    blk['counted']=blk.n>=minblk
    o['blocks']=blk.round(3).to_dict('index')
    c=blk[blk.counted]; o['blocks_pos']=int((c.mean_net_bp>0).sum()); o['blocks_counted']=int(len(c))
    o['by_year']=pd.DataFrame({'y':y.values,'net':netbp.values,'gross':grossbp.values,'u':usd.values}).groupby('y').agg(n=('net','size'),net_bp=('net','mean'),gross_bp=('gross','mean'),usd=('u','sum')).round(3).to_dict('index')
    pre=dates<'2020-06-01'
    o['era_pre_Jun2020']=dict(n=int(pre.sum()),net_bp=netbp[pre].mean(),gross_bp=grossbp[pre].mean(),cost_bp=costbp[pre].mean())
    o['era_post_Jun2020']=dict(n=int((~pre).sum()),net_bp=netbp[~pre].mean(),gross_bp=grossbp[~pre].mean(),cost_bp=costbp[~pre].mean())
    c26=costbp[y==2026].mean(); n26=grossbp-c26
    o['costs_at_2026']=dict(cost_bp_2026=c26,mean_net_bp=n26.mean(),t=tstat(n26),post_Jun2020_mean=n26[~pre].mean())
    return o

models=pd.read_csv('/run/media/roflz/Disk 2/_/market_data/chosen_models_trades.csv',parse_dates=['date'])
def corr_models(dates,usd,alldays):
    s=pd.Series(usd.values,index=pd.DatetimeIndex(dates)).groupby(level=0).sum()
    out={}
    for m,g in models.groupby('model'):
        mp=g.groupby('date').usd.sum()
        a=s.reindex(alldays,fill_value=0); b=mp.reindex(alldays,fill_value=0)
        ov=s.index.intersection(mp.index); lost=mp[mp<0].index.intersection(s.index)
        out[m]=dict(corr_zero_filled=round(float(np.corrcoef(a,b)[0,1]),4),corr_overlap=round(float(np.corrcoef(s[ov],mp[ov])[0,1]),4) if len(ov)>2 else None,
                    n_overlap=len(ov),spec_mean_usd_on_model_loss_days=round(float(s[lost].mean()),2) if len(lost) else None,n_loss_days=len(lost))
    return out

res={}; series={}
rng_seed=12345
# ---------- S1 / S3 family ----------
start={'S1':'2010-12-06','S1-V1':'2010-12-06','S1-V2':'2010-12-06'}
for r in ['S1','S1-V1','S1-V2','S3','S3-V1','S3-V2','S1-C2']:
    df=pd.read_csv(B+f's12_X/trades_{r}.csv',parse_dates=['date'])
    df=fix_sizes(df,r,'n_NQ','n_ES','date')
    df.to_csv(R+f'trades_{r}.csv',index=False)
    o=common(df,df.date,df.net_bp,df.gross_bp,df.cost_bp,df.net_usd)
    o['t_nw5']=nw_t(df.net_bp,5); o['p_two_sided']=pval(df.net_bp)
    st=pd.Timestamp(start.get(r,df.date.min())); o['trades_per_year']=len(df)/((DATA_END-st).days/365.25); o['sample_start']=str(st.date())
    rng=np.random.default_rng(rng_seed)
    sg=rng.choice([-1.0,1.0],size=(1000,len(df)))
    coin=(sg*df.gross_bp.values-df.cost_bp.values).mean(1)
    o['C1_p95']=float(np.percentile(coin,95)); o['C1_mean']=float(coin.mean())
    if r.startswith('S1'):
        za=df.z_entry.abs()
        o['by_z']={lab:dict(n=int(m.sum()),net_bp=df.net_bp[m].mean(),gross_bp=df.gross_bp[m].mean()) for lab,m in [('1-1.5',(za>=1)&(za<1.5)),('1.5-2',(za>=1.5)&(za<2)),('>=2',za>=2)]}
        o['stop_exits']=int((df.exit_reason!='close').sum())
        ef=df.expiry_friday.astype(bool); o['expiry_fridays']=dict(n=int(ef.sum()),net_bp=df.net_bp[ef].mean(),usd=df.net_usd[ef].sum())
        sl=stats.linregress(df.es_ret_entry_to_close_bp,df.net_bp); o['C3_beta_net']=sl.slope
        o['C3_beta_gross']=stats.linregress(df.es_ret_entry_to_close_bp,df.gross_bp).slope
    if r.startswith('S3'):
        o['C2_placebo_net_bp_X_15:30sizes']=df.placebo_net_bp.mean()
        y=pd.read_csv(B+f's12_Y/trades_{r}.csv'); o['C2_placebo_net_bp_Y_14:30sizes']=y.placebo_net_bp.mean()
        o['C2_placebo_used']=max(o['C2_placebo_net_bp_X_15:30sizes'],o['C2_placebo_net_bp_Y_14:30sizes'])
        rn=df.R_NQ.abs()*100; rmin=np.minimum(df.R_NQ.abs(),df.R_ES.abs())*100
        o['by_R_NQ']={lab:dict(n=int(m.sum()),net_bp=df.net_bp[m].mean(),gross_bp=df.gross_bp[m].mean()) for lab,m in [('1-1.5',(rn<1.5)),('1.5-2',(rn>=1.5)&(rn<2)),('2-3',(rn>=2)&(rn<3)),('>=3',rn>=3)]}
        o['by_R_min']={lab:dict(n=int(m.sum()),net_bp=df.net_bp[m].mean(),gross_bp=df.gross_bp[m].mean()) for lab,m in [('<1.5',(rmin<1.5)),('1.5-2',(rmin>=1.5)&(rmin<2)),('2-3',(rmin>=2)&(rmin<3)),('>=3',rmin>=3)]}
        o['by_vix_tercile']={int(k):dict(n=int(len(g)),net_bp=g.net_bp.mean(),gross_bp=g.gross_bp.mean()) for k,g in df.groupby('vix_tercile')}
        for c in ['fomc','cpi']:
            m=df[c].astype(bool); o[c]=dict(n=int(m.sum()),net_bp=df.net_bp[m].mean())
        o['outright_last30_dir_bp']=dict(NQ=df.NQ_outright_lasthalf_bp_dir.mean(),NQ_t=tstat(df.NQ_outright_lasthalf_bp_dir),ES=df.ES_outright_lasthalf_bp_dir.mean(),ES_t=tstat(df.ES_outright_lasthalf_bp_dir))
    alldays=pd.bdate_range(df.date.min(),DATA_END)
    o['model_corr']=corr_models(df.date,df.net_usd,alldays)
    res[r]=o; series[r]=df.net_bp.values
# ---------- S2 family ----------
for r in ['S2','S2-V1','S2-V2']:
    seg=pd.read_csv(B+f's12_X/trades_{r}_segments.csv')
    seg=fix_sizes(seg,r,'n_lead','n_ES','entry_date'); seg.to_csv(R+f'trades_{r}_segments.csv',index=False)
    mo=pd.read_csv(B+f's12_X/trades_{r}.csv')
    agg=seg.groupby('hold_month').agg(gross_usd=('gross_usd','sum'),cost_usd=('cost_usd','sum'),net_usd=('net_usd','sum'))
    mo=mo.drop(columns=['gross_usd','cost_usd','net_usd']).merge(agg,left_on='hold_month',right_index=True)
    mo.to_csv(R+f'trades_{r}.csv',index=False)
    d=pd.to_datetime(mo.hold_month+'-01')
    o=common(mo,d,mo.net_bp,mo.gross_bp,mo.cost_bp,mo.net_usd)
    o['t_nw3']=nw_t(mo.net_bp,3); o['p_two_sided']=pval(mo.net_bp); o['trades_per_year']=12.0
    post16=d>='2016-01-01'; o['post_2016']=dict(n=int(post16.sum()),net_bp=mo.net_bp[post16].mean())
    gl=mo.gross_long_bp.values; cost=mo.cost_bp.values; dd=mo.d.values; N=len(mo)
    sh=[(np.roll(dd,k)*gl-cost).mean() for k in range(12,N-12+1)]
    o['C1_offsets']=len(sh); o['C1_p95']=float(np.percentile(sh,95))
    o['C2_static_long']=float((gl-cost).mean())
    run=(dd!=np.r_[np.nan,dd[:-1]]).cumsum(); g=pd.Series(mo.net_bp.values).groupby(run).sum()
    best=g.idxmax(); o['best_regime']=dict(start=mo.hold_month[run==best].iloc[0],end=mo.hold_month[run==best].iloc[-1],months=int((run==best).sum()),sum_bp=g.max())
    o['ex_best_regime_mean']=float(mo.net_bp.values[run!=best].mean())
    o['sign_changes']=int((np.diff(dd)!=0).sum()); o['long_share']=float((dd>0).mean())
    res[r]=o; series[r]=mo.net_bp.values
# ---------- Holm across 9 ----------
fam=['S1','S1-V1','S1-V2','S2','S2-V1','S2-V2','S3','S3-V1','S3-V2']
p=np.array([res[r]['p_two_sided'] for r in fam]); order=np.argsort(p); adj=np.empty(9); run=0
for i,j in enumerate(order): run=max(run,min(1,(9-i)*p[j])); adj[j]=run
for r,a in zip(fam,adj): res[r]['holm_p']=float(a)
# ---------- criteria ----------
def crit(r):
    o=res[r]; prim='-' not in r; C=[]
    if prim: C.append(('a: t>=2 full sample', f"t={o['t']:.2f}", o['t']>=2))
    else: C.append(('a(variant): t>=3 or Holm p<0.05, mean>0', f"t={o['t']:.2f}, Holm p={o['holm_p']:.2g}", (o['t']>=3 or o['holm_p']<0.05) and o['mean_net_bp']>0))
    if r.startswith('S2'):
        if prim: C[0]=('a: t>=2 plain and NW3', f"t={o['t']:.3f}, NW3 {o['t_nw3']:.3f}", o['t']>=2 and o['t_nw3']>=2)
        C.append(('b: mean net>0 Jan2016-Nov2026', f"{o['post_2016']['net_bp']:.3f} bp (n={o['post_2016']['n']})", o['post_2016']['net_bp']>0))
        C.append(('c: >=2/3 counted blocks positive', f"{o['blocks_pos']}/{o['blocks_counted']}", o['blocks_pos']>=2/3*o['blocks_counted']))
        C.append(('d1: > C1 circular-shift p95', f"{o['mean_net_bp']:.3f} vs {o['C1_p95']:.3f}", o['mean_net_bp']>o['C1_p95']))
        C.append(('d2: > C2 static long-spread', f"{o['mean_net_bp']:.3f} vs {o['C2_static_long']:.3f}", o['mean_net_bp']>o['C2_static_long']))
        C.append(('e: >0 after dropping best regime', f"{o['ex_best_regime_mean']:.3f}", o['ex_best_regime_mean']>0))
    else:
        e=o['era_post_Jun2020']
        C.append(('b: mean net>0 Jun2020-Nov2026', f"{e['net_bp']:.3f} bp (n={e['n']})", e['net_bp']>0))
        C.append(('c: >=2/3 counted blocks positive', f"{o['blocks_pos']}/{o['blocks_counted']}", o['blocks_pos']>=2/3*o['blocks_counted']))
        C.append(('d: > C1 coin p95', f"{o['mean_net_bp']:.3f} vs {o['C1_p95']:.3f}", o['mean_net_bp']>o['C1_p95']))
        if r.startswith('S3'): C.append(('e: > C2 placebo 14:30-15:00 (higher of two sizings)', f"{o['mean_net_bp']:.3f} vs {o['C2_placebo_used']:.3f}", o['mean_net_bp']>o['C2_placebo_used']))
        C.append(('gross>=1.5x cost', f"{o['mean_gross_bp']:.3f} vs {1.5*o['mean_cost_bp']:.3f}", o['mean_gross_bp']>=1.5*o['mean_cost_bp']))
    o['criteria']=[dict(name=a,value=b,pass_=bool(c)) for a,b,c in C]; o['verdict']='pass' if all(c for _,_,c in C) else 'fail'
for r in fam+['S1-C2']:
    if r!='S1-C2': crit(r)
res['corrections']=corrections
json.dump(res,open(R+'recon_summary.json','w'),indent=1,default=lambda x: x.item() if hasattr(x,'item') else str(x))
for r in fam:
    o=res[r]; print(f"{r}: n={o['n']} net {o['mean_net_bp']:.3f}bp gross {o['mean_gross_bp']:.3f} cost {o['mean_cost_bp']:.3f} $/tr {o['net_usd_per_trade']:.2f} tot {o['total_usd']:.2f} t {o['t']:.3f} tpy {o['trades_per_year']:.2f} holm {o['holm_p']:.3g} -> {o['verdict']}")
    for c in o['criteria']: print('   ',c['name'],'|',c['value'],'|',c['pass_'])
for c in corrections: print(c)
print('S1-C2',res['S1-C2']['n'],res['S1-C2']['mean_net_bp'],res['S1-C2']['mean_gross_bp'])
