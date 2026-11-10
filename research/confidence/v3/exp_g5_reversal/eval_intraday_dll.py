"""EXPLORATORY eval-realism check (descriptive, not a new rule; logged). The v2 eval judge uses END-OF-DAY P&L floored
at -$600, so a 23-hour hold that is down -$900 at 03:00 and closes +$200 counts as +$200. In a real Lucid account the
$600 daily loss limit would have flattened it at about -$600. Here each session's open P&L path is rebuilt from the
5-minute bars (worst price of every bar, all markets of the basket summed per bar, costs included), and a day whose
path touches -$600 at the chosen size is booked at -$600. Then the same eval_daily is run. (Still optimistic about the
trailing drawdown, which is only checked at the close; still slightly pessimistic about the basket, because the bar
extremes of different markets need not coincide.) Light (v3 5-minute bars)."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness as H   # noqa: E402
import eval_sim as es  # noqa: E402
import g5             # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def worst_path(tr):
    """per session: (worst open P&L over the day for 1 micro of every trade, EOD P&L) - trades must be one per market
    per session."""
    parts = []
    for m in tr.market.unique():
        t = tr[tr.market == m]
        assert not t.session.duplicated().any()
        b = H.bars(m, 5)[["session", "H", "L"]].reset_index()
        b = b[b.session.isin(t.session)]
        x = b.merge(t[["session", "t_entry", "t_exit", "d", "entry_px", "cost_usd"]], on="session")
        x = x[(x.ts >= x.t_entry) & (x.ts < x.t_exit)]
        usd = H.SPEC[m]["usd"]
        worst = np.where(x.d > 0, x.L - x.entry_px, x.entry_px - x.H) * usd - x.cost_usd
        parts.append(pd.DataFrame({"session": x.session.to_numpy(), "ts": x.ts.to_numpy(), "w": worst}))
    P = pd.concat(parts).groupby(["session", "ts"]).w.sum()
    return P.groupby(level=0).min()


def run(name, tr, sizes=(1, 3, 5)):
    wp = worst_path(tr).reindex(g5.CAL).fillna(0.0)
    eod = tr.groupby(pd.DatetimeIndex(tr.session)).pnl_usd.sum().reindex(g5.CAL, fill_value=0.0)
    rows = []
    for k in sizes:
        d_eod = (k * eod).clip(lower=-600)
        hit = (k * wp) <= -600
        d_int = d_eod.where(~hit, -600.0)
        for lab, dly in (("EOD floor (v2 judge)", d_eod), ("intraday $600 stop", d_int)):
            e = es.eval_daily(dly, (0.40, 0.50))
            e.insert(0, "model", lab); e.insert(0, "micros_per_market", k); e.insert(0, "stream", name)
            e["dll_hit_days_pct"] = 100 * hit.mean()
            rows.append(e)
    return pd.concat(rows, ignore_index=True)


def main():
    A5 = pd.read_parquet(os.path.join(H.HERE, "out", "trades", "A5.parquet"))
    drift = pd.concat([H.drift_trades(m, g5.entries_for(g5.sig_A5, m)) for m in g5.MK_ORDER], ignore_index=True)
    drift = drift[pd.DatetimeIndex(drift.session) <= g5.CAL[-1]]
    s51 = pd.read_parquet(os.path.join(H.HERE, "out", "trades", "S5.1_MNQ.parquet"))
    out = pd.concat([run("A5 basket", A5), run("long-drift basket 18:00-16:45", drift), run("S5.1 MNQ", s51)],
                    ignore_index=True)
    keep = ["stream", "micros_per_market", "model", "consistency", "window", "pass_pct", "fail_pct", "within_10",
            "within_20", "dll_hit_days_pct"]
    out = out[keep]
    out.to_csv(os.path.join(H.HERE, "exp_G5", "eval_intraday_dll_EXPLORATORY.csv"), index=False)
    H.log("G5_evalrealism_EXPLORATORY", "MES+MNQ+MYM", "eval with intraday $600 stop on 5-min worst path",
          trades=A5, params=dict(sizes=[1, 3, 5]), note="exploratory eval-model check, not a new rule")
    pd.set_option("display.width", 250)
    print(out[(out.consistency == 0.4) & (out.window == "2018+")].round(1).to_string())


if __name__ == "__main__":
    main()
