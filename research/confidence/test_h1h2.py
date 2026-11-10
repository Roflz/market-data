"""Hand-made checks for h1h2.detect and label_stop_entries."""
import numpy as np
import pandas as pd
import h1h2

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)

HL = [(10, 9), (11, 10), (12, 11), (11, 10), (10, 9), (11, 10), (13, 12), (14, 13), (13, 12), (12, 11), (13, 12),
      (15, 14), (16, 15), (15, 14), (14, 13), (15, 14), (14.5, 13.5), (15.5, 14.5), (17, 16), (18, 17)]
def frame(hl):
    H = np.array([h for h, l in hl], float); L = np.array([l for h, l in hl], float)
    idx = pd.date_range("2024-03-05 09:30", periods=len(hl), freq="5min")
    b = pd.DataFrame(dict(O=(H + L) / 2, H=H, L=L, C=(H + L) / 2, seg=1, run=1, inst=1, sess=idx.normalize()),
                     index=idx)
    ctx = pd.DataFrame(dict(ema8=3.0, ema20=2.0, ema50=1.0), index=idx)        # stacked up throughout
    return b, ctx
b, ctx = frame(HL)
ev = h1h2.detect(b, ctx, tick=0.25, tf=5, k=2)
L_ = ev[ev.d > 0]
check("long orders at bars 13, 14, 16", L_.i.tolist() == [13, 14, 16])
check("attempt numbers 1, 1, 2 (H1 fails at bar 15, next order is an H2)", L_.attempt.tolist() == [1, 1, 2])
check("triggers = signal bar high + 1 tick", L_.trigger.tolist() == [15.25, 14.25, 14.75])
check("stops = pullback low so far - 1 tick", L_.stop.tolist() == [13.75, 12.75, 12.75])
check("signal-bar stops", L_.stop_sig.tolist() == [13.75, 12.75, 13.25])
check("no short orders in an uptrend", (ev.d < 0).sum() == 0)
# pullback that breaks the last higher low (the confirmed higher low at bar 16 is 11, from bar 9): no order at/after bar 16
HL2 = list(HL); HL2[16] = (14.5, 10.5)
b2, c2 = frame(HL2)
ev2 = h1h2.detect(b2, c2, tick=0.25, tf=5, k=2)
check("broken higher low stops new orders", ev2[ev2.d > 0].i.max() < 16)
# EMAs not stacked -> no orders
c3 = ctx.copy(); c3["ema8"] = 0.0
check("no trend (EMAs not stacked) -> no orders", len(h1h2.detect(b, c3, tick=0.25, tf=5, k=2)) == 0)
# mirror: the same path upside down gives short orders with mirrored prices
b4 = b.copy(); b4["H"], b4["L"] = -b.L, -b.H; b4["O"], b4["C"] = -b.O, -b.C
c4 = pd.DataFrame(dict(ema8=-3.0, ema20=-2.0, ema50=-1.0), index=b.index)
ev4 = h1h2.detect(b4, c4, tick=0.25, tf=5, k=2)
check("mirror: short orders at the same bars", ev4[ev4.d < 0].i.tolist() == [13, 14, 16])
check("mirror: short triggers = low - 1 tick", ev4[ev4.d < 0].trigger.tolist() == [-15.25, -14.25, -14.75])
check("mirror: short stops = pullback high + 1 tick", ev4[ev4.d < 0].stop.tolist() == [-13.75, -12.75, -12.75])
print("ALL PASS" if ok else "SOME FAILED")

# ---- stop-order fills on the 1-minute path (5-minute bars)
import labels as lb
idx1 = pd.date_range("2024-03-05 09:30", periods=20, freq="1min")
m1 = pd.DataFrame(dict(O=100.0, H=100.5, L=99.75, C=100.0, inst=1, sess=idx1.normalize()), index=idx1)
m1.loc[idx1[6], ["O", "H"]] = [100.25, 101.5]            # bar 1 (09:35-09:39), 2nd minute trades through 101
bq = pd.DataFrame(dict(O=100.0, H=101.5, L=99.75, C=100.0, seg=1, run=1, inst=1, sess=idx1[0].normalize()),
                  index=pd.date_range("2024-03-05 09:30", periods=4, freq="5min"))
evq = pd.DataFrame(dict(i=[0, 0, 1], t=bq.index[[0, 0, 1]], d=[1, -1, 1], attempt=1, trigger=[101.0, 98.0, 100.25],
                        stop=[99.0, 102.0, 99.0], stop_sig=[99.0, 102.0, 99.0]))
lab = h1h2.label_stop_entries("NQ", 5, bq, evq, m1=m1, max_bars=2)
check("untriggered short order is dropped", (lab.d < 0).sum() == 0)
r0 = lab[(lab.i == 0)].iloc[0]
check("long fills on the first minute reaching the trigger, at the trigger + 1 tick slippage", r0.entry == 101.25 and
      r0.t_entry == idx1[6])
m1g = m1.copy(); m1g.loc[idx1[10], ["O", "H"]] = [100.75, 100.9]   # bar 2 opens above the 100.25 trigger
labg = h1h2.label_stop_entries("NQ", 5, bq, evq, m1=m1g, max_bars=2)
rg = labg[labg.i == 1].iloc[0]
check("gap through the trigger fills at the minute's open + 1 tick slippage", rg.entry == 101.0 and rg.t_entry == idx1[10])
print("ALL PASS" if ok else "SOME FAILED")
