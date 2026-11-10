"""Conservative contract rule: trade day D only when the data show that D's file contract was the 9:30-15:59 volume
leader on the prior NYSE day. Proxy: ratio = file-contract RTH volume / its median of the prior 20 days.
 - switch at D (new contract in file): tradable iff old contract's ratio on D-1 < 0.5 (old collapsed -> new led)
 - no switch, D within the 5 trading days before the next switch: tradable iff ratio(D-1) >= 0.5
 - all other days: tradable."""
import numpy as np, pandas as pd
R='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/s11_recon'
res={}
for sym in ['NQ','ES']:
    df=pd.read_csv(f'{R}/roll_proxy_{sym}.csv',index_col=0,parse_dates=True)
    n=len(df); sw=np.where(df.switch_today.values)[0]
    nxt=np.full(n,10**9)
    for i in range(n):
        j=sw[sw>i]
        if len(j): nxt[i]=j[0]-i
    pre=(nxt>=1)&(nxt<=5)
    tr=np.ones(n,bool)
    pr=df.prev_ratio.values
    tr[df.switch_today.values]=pr[df.switch_today.values]<0.5
    m=pre&~df.switch_today.values
    tr[m]=~(pr[m]<0.5)
    df['tradable_cons']=tr
    df.to_csv(f'{R}/roll_proxy_{sym}.csv')
    print(sym,'untradable days:',int((~tr).sum()),' of which switch days:',int((~tr&df.switch_today.values).sum()),' pre-switch days:',int((~tr&~df.switch_today.values).sum()))
