import sys, pandas as pd
sys.argv = ["paper_log.py", "--since", "2026-09-01", "--out", sys.argv[1]]
import paper_log as pl
orig = pl.coverage
def fake():
    c = orig(); c["ctx"] = pd.Timestamp("2026-11-04"); c["cpi"] = pd.Timestamp("2026-10-01"); return c
pl.coverage = fake
pl.main()
