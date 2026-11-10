import pandas as pd, numpy as np
B='/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests/'
x=pd.read_csv(B+'s12_X/trades_S1-C2.csv'); y=pd.read_csv(B+'s12_Y/trades_S1-C2.csv')
m=x.merge(y,on='date',how='outer',indicator=True,suffixes=('_x','_y'))
print(len(x),len(y),m._merge.value_counts().to_dict())
b=m[m._merge=='both']
print('net_bp diffs',(~np.isclose(b.net_bp_x,b.net_bp_y)).sum(),'X mean net',x.net_bp.mean(),'gross',x.gross_bp.mean(),'Y',y.net_bp.mean(),y.gross_bp.mean())
print(m[m._merge!='both'][['date','_merge']].head(20))
