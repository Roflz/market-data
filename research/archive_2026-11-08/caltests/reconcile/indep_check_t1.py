"""Independent check of the test-1 signal (Cal_t for t = T-4..T) and the primary P&L, written from scratch without the
back-adjustment cumsum: returns are chained multiplicatively within each contract (at a roll bar the old contract's
last close and the new contract's first open bridge the day). Compares with the reconciled event file."""
import numpy as np
import pandas as pd

PROJ = "/run/media/roflz/Disk 2/_/market_data"
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/caltests/reconcile"
ses = pd.read_pickle(f"{PROJ}/data/daily_sessions_ES.pkl")
cash = ses.index[ses.cash_day]
early = set(ses.index[ses.cash_day & ses.early_close])


def load(path):
    d = pd.read_csv(path, usecols=["ts_event", "Open", "Close", "instrument_id"])
    ts = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert("America/New_York")
    d.index = ts
    d = d[~d.index.duplicated()].sort_index().drop(columns="ts_event")
    return d


def price_at(d, targets):
    """value (close, inst, ts position) of the last bar with open <= target."""
    pos = d.index.searchsorted(pd.DatetimeIndex(targets), side="right") - 1
    return pos


def chain_ret(d, p0, p1):
    """Return from the close of bar p0 to the close of bar p1, chained multiplicatively within each contract."""
    inst, cl, op = d.instrument_id.values, d.Close.values, d.Open.values
    seg = inst[p0:p1 + 1]
    chg = np.where(seg[1:] != seg[:-1])[0] + 1 + p0          # roll bars
    g, ref = 1.0, cl[p0]
    for c in chg:
        g *= cl[c - 1] / ref                                  # old contract up to the bar before the roll
        ref = op[c]                                           # new contract from the roll bar's open
    return g * cl[p1] / ref - 1


es = load(f"{PROJ}/data/ES_fut_1m.csv")
zn = load(f"{PROJ}/data/ZN_fut_1h.csv")


def tgt(day, hh, mm):
    return pd.Timestamp(day).tz_localize("America/New_York") + pd.Timedelta(hours=hh, minutes=mm)


es_close = price_at(es, [tgt(x, 12, 59) if x in early else tgt(x, 15, 59) for x in cash])
es_pre = price_at(es, [tgt(x, 12, 54) if x in early else tgt(x, 15, 54) for x in cash])
zn_close = price_at(zn, [tgt(x, 12, 0) if x in early else tgt(x, 15, 0) for x in cash])
zn_pre = price_at(zn, [tgt(x, 11, 0) if x in early else tgt(x, 14, 0) for x in cash])
POS = {d: i for i, d in enumerate(cash)}
mp = pd.Series(cash.to_period("M"), index=cash)
T = mp.groupby(mp.values).apply(lambda s: s.index.max())
months = [m for m in T.index if pd.Period("2010-07", "M") <= m <= pd.Period("2026-10", "M")]
ref = pd.read_csv(f"{OUT}/events_1_primary.csv")
ref_cal = pd.read_csv(f"{OUT}/events_1_primary.csv").set_index("month")
rows = []
for m in months:
    iT, iP = POS[T[m]], POS[T[m - 1]]
    cals = []
    for t in range(iT - 4, iT + 1):
        gE = (1 + chain_ret(es, es_close[iP], es_close[t - 1])) * (1 + chain_ret(es, es_close[t - 1], es_pre[t])) \
            if t - 1 > iP else (1 + chain_ret(es, es_close[iP], es_pre[t]))
        gZ = (1 + chain_ret(zn, zn_close[iP], zn_close[t - 1])) * (1 + chain_ret(zn, zn_close[t - 1], zn_pre[t])) \
            if t - 1 > iP else (1 + chain_ret(zn, zn_close[iP], zn_pre[t]))
        cals.append(int(np.sign(gE - gZ)))
    pos = [-c for c in cals]
    cl = es.Close.values
    insts = es.instrument_id.values[[es_close[i] for i in range(iT - 4, iT + 2)]]
    assert len(set(insts)) == 1, m
    pts = sum(p * (cl[es_close[iT - 4 + j + 1]] - cl[es_close[iT - 4 + j]]) for j, p in enumerate(pos))
    seq = [0] + pos + [0]
    sides = sum(abs(seq[j + 1] - seq[j]) for j in range(6))
    rows.append(dict(month=str(m), cal4=cals[0], net=pts * 5 - sides * 1.75))
ind = pd.DataFrame(rows).set_index("month")
mrg = ind.join(ref_cal[["cal_T4", "net_usd"]])
print("months", len(mrg), "| Cal_T-4 agreement", (mrg.cal4 == mrg.cal_T4).mean(),
      "| net$ equal on", int((np.abs(mrg.net - mrg.net_usd) < 1e-6).sum()), "events")
diff = mrg[np.abs(mrg.net - mrg.net_usd) > 1e-6]
print(diff)
print("independent net mean", ind.net.mean(), "t", ind.net.mean() / (ind.net.std(ddof=1) / np.sqrt(len(ind))))
