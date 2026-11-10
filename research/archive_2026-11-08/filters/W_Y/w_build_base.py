"""
Builder Y, Filter W, step 1: rebuild the live overnight_break trades exactly as chosen_models.overnight_break does,
keeping per trade the inputs Filter W needs (signal bar, R_pts, raw entry reference price), then apply the
cash-day / expiry / R1 skip rules as chosen_models.main does, and check against chosen_models_trades.csv.
Output (in this dir): base_overnight_break.pkl
Read-only use of the project: only imports and reads.
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

import calendar_days as cd
import chosen_models as cm
import exits_compare as ec
import exits_engine as ee

warnings.filterwarnings("ignore")
OUT = os.path.dirname(os.path.abspath(__file__))
SYM = "NQ"


def build_D():
    """Same as exits_compare.init(), but NQ only (saves memory; ES is never used by the overnight_break model)."""
    b = pd.read_pickle(f"data/x5_{SYM}.pkl")
    D = ee.Day(b[b.index.year >= ec.FIRST_YEAR])
    D.pos = pd.Index(D.idx)
    ec.G[SYM] = D
    ec.G[("sets", SYM)] = ec.entry_sets(SYM)
    return D


def main():
    ds = cm.sessions()
    cash_days = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash_days)
    D = build_D()
    sp = ee.SPEC[SYM]
    t = ee.run(D, ec.G[("sets", SYM)]["Overnight break + daily trend"], "hold", k0=2.0)
    b = t.bar.to_numpy()
    date = pd.to_datetime(D.sess[b])
    adj = (ds.close_adj - ds.close_raw).reindex(date).to_numpy()
    net_pts = t.pts - sp["comm"] / sp["usd"]
    out = pd.DataFrame({
        "model": "overnight_break", "date": date, "side": np.where(t.dir > 0, "long", "short"),
        "exit": t.exit.to_numpy(), "usd": (net_pts * sp["usd"]).to_numpy(), "R": (net_pts / t.R_pts).to_numpy(),
        "bp": 1e4 * net_pts.to_numpy() / (D.Close[b] - adj),
        # Filter W inputs and audit fields
        "bar": b, "signal_bar_time": D.idx[b], "entry_time": D.idx[b + 1],
        "R_pts": t.R_pts.to_numpy(), "atr5_signal": D.atr5[b], "signal_close_adj": D.Close[b], "sess_adj": adj,
        "raw_ref_price": D.Close[b] - adj,                       # the raw price chosen_models uses for bp
        "entry_fill_adj": D.Open[b + 1] + t.dir.to_numpy() * ee.SLIP,
        "gross_pts": t.pts.to_numpy(), "net_pts": net_pts.to_numpy(), "hold_bars": t.hold_bars.to_numpy(),
    })
    out["entry_fill_raw"] = out.entry_fill_adj - adj
    out["exit_time"] = D.idx[b + t.hold_bars.to_numpy()]         # exit bar = entry bar + hold_bars - 1, stamped open
    out = out[out.date.isin(cash_days) & ~out.date.isin(expiry)]
    after_drop, _ = cm.skip_days()
    out = out[~out.date.isin(after_drop)].reset_index(drop=True)

    ref = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    ref = ref[ref.model == "overnight_break"].reset_index(drop=True)
    print(f"rebuilt {len(out)} trades ${out.usd.sum():,.2f} | csv {len(ref)} trades ${ref.usd.sum():,.2f}")
    same = (len(out) == len(ref)
            and (out.date.values == ref.date.values).all() and (out.side.values == ref.side.values).all()
            and np.allclose(out.usd.values, ref.usd.values) and np.allclose(out.bp.values, ref.bp.values)
            and np.allclose(out.R.values, ref.R.values) and (out.exit.values == ref.exit.values).all())
    print("row-by-row identical to chosen_models_trades.csv:", same)
    if not same:
        sys.exit(1)
    out.to_pickle(os.path.join(OUT, "base_overnight_break.pkl"))
    # the trading calendar and the model's data start, for the 250-trading-day window
    pd.to_pickle({"cash_days": cash_days, "model_first_sess": pd.Timestamp(D.sess[0]),
                  "model_last_sess": pd.Timestamp(D.sess[-1])}, os.path.join(OUT, "calendar.pkl"))
    print("model data sessions", D.sess[0], "->", D.sess[-1])


if __name__ == "__main__":
    main()
