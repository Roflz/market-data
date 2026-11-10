import numpy as np, pandas as pd, sys
R='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/s11_recon'
out={}
for sym in ['NQ','ES']:
    c=pd.read_pickle(f'{R}/xmod/cache_{sym}.pkl')
    days,g,info=c['days'],c['g'],c['info']
    V=np.nansum(g['Volume'][:,90:],1)   # 9:30-15:59
    inst=info.inst.to_numpy()
    s=pd.Series(V,index=days)
    med=s.rolling(20,min_periods=10).median().shift(1)
    ratio=(s/med)
    df=pd.DataFrame({'inst':inst,'V':V,'ratio':ratio.values},index=days)
    df['switch_today']=np.r_[False,inst[1:]!=inst[:-1]]
    # day D: prior-day leader likely NOT the file contract of D-1 if D-1 volume collapsed and no switch at D
    prevratio=np.r_[np.nan,df.ratio.values[:-1]]
    df['prev_ratio']=prevratio
    df['skip_proxy']=(~df.switch_today)&(df.prev_ratio<0.5)
    # pre-switch days stats
    sw=np.where(df.switch_today)[0]
    rows=[]
    for i in sw:
        rows.append(dict(switch=str(days[i].date()),dow=days[i].day_name()[:3],r_m1=round(df.ratio.iloc[i-1],2),r_m2=round(df.ratio.iloc[i-2],2),r_m3=round(df.ratio.iloc[i-3],2)))
    rr=pd.DataFrame(rows)
    print(sym,'switches',len(sw),' D-1 ratio<0.5:',(rr.r_m1<0.5).sum(),' D-2 ratio<0.5:',(rr.r_m2<0.5).sum(),' D-3<0.5:',(rr.r_m3<0.5).sum())
    print(rr[(rr.r_m1>=0.5)].to_string())
    print('skip_proxy days (no switch at D, D-1 file-contract RTH vol < 50% of its 20d median):',int(df.skip_proxy.sum()))
    print(df[df.skip_proxy].index.strftime('%Y-%m-%d').tolist())
    df.to_csv(f'{R}/roll_proxy_{sym}.csv')
