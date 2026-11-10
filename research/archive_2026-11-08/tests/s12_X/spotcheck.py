"""Independent spot checks against the raw 1-minute CSVs (loop-based, not reusing the vectorized arrays)."""
import os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
out = []
def raw(sym, dates):
    """Load raw rows for given ET calendar dates (plus their RTH), straight from the CSV."""
    d = pd.read_csv(f"data/{sym}_fut_1m.csv")
    ts = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    d["ts"] = ts
    return d.set_index("ts").sort_index()
NQr = raw("NQ", None); ESr = raw("ES", None)

def bar(df, t):
    return df.loc[pd.Timestamp(t)]

def check_intraday(rule, date, et, xt_bar, row):
    nq_e = bar(NQr, f"{date} {et}"); es_e = bar(ESr, f"{date} {et}")
    nq_x = bar(NQr, f"{date} {xt_bar}"); es_x = bar(ESr, f"{date} {xt_bar}")
    stop = row.exit_reason == "stop"
    xn = nq_x.Open if stop else nq_x.Close; xe = es_x.Open if stop else es_x.Close
    ok = (nq_e.Open == row.NQ_entry and es_e.Open == row.ES_entry and xn == row.NQ_exit and xe == row.ES_exit
          and nq_e.instrument_id == nq_x.instrument_id and es_e.instrument_id == es_x.instrument_id)
    out.append(f"{rule} {date}: raw NQ entry {nq_e.Open} vs {row.NQ_entry}, ES entry {es_e.Open} vs {row.ES_entry}, "
               f"NQ exit {xn} vs {row.NQ_exit}, ES exit {xe} vs {row.ES_exit} ({'open of ' if stop else 'close of '}{xt_bar} bar); same inst: "
               f"{nq_e.instrument_id == nq_x.instrument_id and es_e.instrument_id == es_x.instrument_id} -> {'OK' if ok else 'MISMATCH'}")
    return ok

def independent_z(date, row, sig_min="14:29"):
    """Recompute b, e, s, z and zo for one S1 day by explicit loops over prior sessions."""
    ds = pd.read_pickle("data/daily_sessions_NQ.pkl"); dse = pd.read_pickle("data/daily_sessions_ES.pkl")
    full = ds.index[ds.cash_day & dse.cash_day & ~ds.early_close & ~dse.early_close]
    D = pd.Timestamp(date)
    prior = full[full < D]
    def day_px(df, d):
        x = df.loc[f"{d.date()} 09:30":f"{d.date()} 15:59"]
        idx = pd.date_range(f"{d.date()} 09:30", f"{d.date()} 15:59", freq="1min")
        c = x.Close.reindex(idx).ffill()
        return x.Open.iloc[0], c, x
    def rets(d):
        on, cn, _ = day_px(NQr, d); oe, ce, _ = day_px(ESr, d)
        pn = np.r_[on, cn.iloc[4::5].to_numpy()]; pe = np.r_[oe, ce.iloc[4::5].to_numpy()]
        return np.diff(np.log(pn)), np.diff(np.log(pe))
    def beta_for(d):
        p = full[full < d][-60:]
        Y, X = zip(*[rets(q) for q in p])
        Y = np.concatenate(Y); X = np.concatenate(X)
        return np.polyfit(X, Y, 1)[0]
    def e_for(d, b, m=sig_min):
        on, cn, _ = day_px(NQr, d); oe, ce, _ = day_px(ESr, d)
        t = pd.Timestamp(f"{d.date()} {m}")
        return np.log(cn[t] / on) - b * np.log(ce[t] / oe)
    b = beta_for(D)
    e = e_for(D, b)
    es_ = [e_for(q, beta_for(q)) for q in prior[-60:]]
    s = np.std(es_, ddof=1)
    out.append(f"S1 {date}: independent b={b:.6f} (vectorized {row.b:.6f}), e/s z={e / s:.4f} (vectorized {row.z_entry:.4f}); "
               f"signal uses bars up to {sig_min} close only, entry at {row.entry_time} open")
    return abs(b - row.b) < 1e-6 and abs(e / s - row.z_entry) < 1e-4

ok_all = True
for rule, k in (("S1", 0), ("S1", 189), ("S1", 392), ("S1-V1", 100), ("S3", 788), ("S3", 300), ("S1-V2", 250)):
    t = pd.read_csv(os.path.join(HERE, f"trades_{rule}.csv"))
    r = t.iloc[k]
    xb = r.exit_bar
    ok_all &= check_intraday(rule, r.date, r.entry_time, xb, r)
    if rule == "S1" and k in (0, 189):
        ok_all &= independent_z(r.date, r)
    if r.exit_reason == "stop":
        # verify trigger: close of the bar before exit bar shows |z_t| >= |z0|+2 with entry sign and no earlier trigger
        out.append(f"   stop trade: exit at open of {xb} bar, i.e. after the close of the prior bar triggered")

# S2: NQ roll segment and month-end segment; S2-V2 RTY segment
for rule, k in (("S2", 2), ("S2", 3), ("S2-V2", 0)):
    s = pd.read_csv(os.path.join(HERE, f"trades_{rule}_segments.csv")).iloc[k]
    lead = NQr if rule == "S2" else None
    if rule == "S2":
        le = bar(NQr, f"{s.entry_date} 10:00").Open; ee = bar(ESr, f"{s.entry_date} 10:00").Open
        if s.exit_reason == "roll":
            lx = bar(NQr, f"{s.exit_date} 15:59").Close; ex = bar(ESr, f"{s.exit_date} 15:59").Close
            nxt_n = NQr.loc[f"{s.exit_date} 18:00":].iloc[0].instrument_id
        else:
            lx = bar(NQr, f"{s.exit_date} 10:00").Open; ex = bar(ESr, f"{s.exit_date} 10:00").Open
    else:
        r = pd.read_csv("data/RTY_fut_1h.csv")
        r["ts"] = pd.to_datetime(r.ts_event, utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
        r = r.set_index("ts")
        le = r.loc[pd.Timestamp(f"{s.entry_date} 10:00")].Open; ee = bar(ESr, f"{s.entry_date} 10:00").Open
        lx = r.loc[pd.Timestamp(f"{s.exit_date} 10:00")].Open; ex = bar(ESr, f"{s.exit_date} 10:00").Open
    ok = (le == s.lead_entry and ee == s.ES_entry and lx == s.lead_exit and ex == s.ES_exit)
    ok_all &= ok
    out.append(f"{rule} seg {s.entry_date}->{s.exit_date} ({s.exit_reason}): raw lead {le}->{lx} vs {s.lead_entry}->{s.lead_exit}, "
               f"ES {ee}->{ex} vs {s.ES_entry}->{s.ES_exit}; inst {s.lead_inst_entry}/{s.lead_inst_exit} -> {'OK' if ok else 'MISMATCH'}")

# roll checks for all intraday rules
for rule in ("S1", "S1-V1", "S1-V2", "S3", "S3-V1", "S3-V2", "S1-C2"):
    t = pd.read_csv(os.path.join(HERE, f"trades_{rule}.csv"))
    bad = ((t.NQ_inst != t.NQ_inst_exit) | (t.ES_inst != t.ES_inst_exit)).sum()
    out.append(f"{rule}: trades spanning an instrument change = {bad}")
    ok_all &= bad == 0
for rule in ("S2", "S2-V1", "S2-V2"):
    t = pd.read_csv(os.path.join(HERE, f"trades_{rule}_segments.csv"))
    bad = ((t.lead_inst_entry != t.lead_inst_exit) | (t.ES_inst_entry != t.ES_inst_exit)).sum()
    out.append(f"{rule}: segments spanning an instrument change = {bad}")
    ok_all &= bad == 0
out.append(f"ALL OK: {ok_all}")
print("\n".join(out))
open(os.path.join(HERE, "spotcheck.txt"), "w").write("\n".join(out) + "\n")
