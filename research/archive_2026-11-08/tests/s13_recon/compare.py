import pandas as pd, numpy as np, sys
S=sys.argv[1]; X=S+"/s13_X/"; Y=S+"/s13_Y/trades/"
pairs=[]
for inst in ["MNQ","MES"]:
  for xs,ys in [("NFP","NFP"),("CPI","CPI"),("CPI_or_NFP_once","CPIorNFP")]:
    for xv,yv in [("primary_time","strict_time"),("disaster_stop","strict_stop2x"),("literal_open845_time","time"),("literal_open845_stop","stop2x")]:
      pairs.append((f"{X}L1_{xv}_{inst}_{xs}.csv",f"{Y}L1-{ys}-2010-2026-{inst}-{yv}.csv",f"{inst} {ys} {yv}"))
rows=[]
for xf,yf,lab in pairs:
  a=pd.read_csv(xf); b=pd.read_csv(yf)
  a["date"]=a.date.astype(str); b["date"]=b.date.astype(str)
  a["exit_reason"]=a.exit_reason.map(lambda s:"stop" if "stop" in s else "time"); b["exit_reason"]=b.exit_reason.map(lambda s:"stop" if "stop" in s else "time")
  m=a.merge(b,on="date",how="outer",suffixes=("_x","_y"),indicator=True)
  both=m[m._merge=="both"]
  cols=["side","entry_time","exit_time","entry","exit","exit_reason","net_usd"]
  diff=np.zeros(len(both),bool)
  for c in cols:
    if not pd.api.types.is_numeric_dtype(both[c+"_x"]): diff|= (both[c+"_x"]!=both[c+"_y"]).to_numpy()
    else: diff|= ~np.isclose(both[c+"_x"],both[c+"_y"],atol=1e-6)
  for era,(lo,hi) in {"2018-26":("2018-01-01","2026-12-31"),"all":("2000","2100")}.items():
    ax=a[(a.date>=lo)&(a.date<=hi)]; by=b[(b.date>=lo)&(b.date<=hi)]
    rows.append(dict(set=lab,era=era,nX=len(ax),nY=len(by),totX=ax.net_usd.sum(),totY=by.net_usd.sum()))
  print(f"{lab:32s} X={len(a)} Y={len(b)} onlyX={list(m.date[m._merge=='left_only'])} onlyY={list(m.date[m._merge=='right_only'])} matched={len(both)} fielddiffs={diff.sum()}")
  if diff.sum(): print(both[diff][["date"]+[c+s for c in cols for s in ("_x","_y")]].to_string())
print(pd.DataFrame(rows).to_string())
