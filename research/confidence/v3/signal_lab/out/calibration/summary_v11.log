# Signal lab v1.1: real-data self-test

Data: ES / NQ / YM continuous futures, 15-min and 60-min bars, cut before the locked holdout (2025-06-30 18:00 ET). YM starts 2018. Units: R20 = 'average bar' (mean high-low of the last 20 bars). $ = per ONE micro (MES $5/pt, MNQ $2/pt, MYM $0.5/pt). Round-trip cost = $1 + 1 tick each way (MES $3.50, MNQ $2.00, MYM $2.00).

v1.1 (after an adversarial review): (1) the look-ahead test now cuts the data at 40 of the metric's own signal bars plus 60 random bars (was 3 random bars) and a failed test makes every verdict INVALID; (2) tradability is judged in $ per trade against the real $ cost. An edge of e R20 on every trade earns e x MEAN R20 x $/pt, so the break-even edge is cost / mean R20. The old bar (mean of cost / R20) was 1.3-1.7x too high. $ per R20 below uses the MEAN R20 of the signal's trades in 2018-25 (v1 used the median of all bars).

## MES 15-min: PASSED (3877 sessions, 347273 bars)

- [x] null: decision p < 0.05 at most nominal (<= 5% + 2 sd)
- [x] null: each single-hold p method within 5% +- 2.6 sd
- [x] null: honest t spread at 16 bars 0.8-1.25
- [x] null: no random signal CONFIRMED or called REAL in the 200-metric batch
- [x] null: 20-metric batches with any q < 0.10 at most 10%
- [x] negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd
- [x] negative: no direction CONFIRMED
- [x] look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest + 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch
- [x] positive: range_ratio (last-bar range), time_of_day, news_830 detected
- [x] power: injected effect recovered (slope 0.85-1.15)
- [x] power: 80% detection reached within the tested range
- [x] classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%
- [x] classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%
- [x] classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%
- [x] classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building over 16 bars) called CONFIDENTLY NOTHING <= 10%
- [x] null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)
- (info) positive: reversal (direction, tiny) detected: True
- (info) positive: range4_ratio (extra, weaker by design) detected: True
- (info) negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd: True

**False positives (200 random signals):** decision p < 0.05 for 3.0% (direction) and 1.0% (size); 20-metric batches with any q < 0.10: 0% of 10; CONFIRMED direction: 0; CONFIRMED size: 0. Honest t spread at 16 bars 1.07 (naive bar-by-bar 2.69).
**Real signals moved to the wrong days (56):** direction p < 0.05 1.8% (by type {'other_market_days': 0.0, 'session_shift': 0.02857142857142857}), size p < 0.05 1.8% (by signal {'above_vwap': 0.0, 'back4_return': 0.0, 'bar_return': 0.0, 'big_bar_follow': 0.0, 'ema20_gap': 0.0, 'momentum14': 0.0, 'range_ratio': 0.125}); CONFIRMED direction 0, size 0.

**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a +0.55 R20 'edge'):**

| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | batch verdict |
|---|---|---|---|---|---|
| next_bar_direction (leaky) | sided | 90.8% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.55 R20) |
| whole_sample_zscore (leaky) | continuous | 99.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0.41, raw effect +0.01 R20) |
| centred_average (leaky) | continuous | 97.3% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.09 R20) |
| inside_bar_next_breakout (leaky) | sided | 4.8% | 5/5 | 7/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.77 R20) |
| big_bar_next_close_beyond (leaky) | sided | 2.0% | 5/5 | 8/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.26 R20) |
| big_bar_next_open_gap (leaky) | sided | 7.5% | 5/5 | 6/10 | INVALID (LOOK-AHEAD) (raw p 4.2e-08, raw effect -0.04 R20) |
| very_rare_next_bar_continues (leaky) | sided | 0.9% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 6.5e-206, raw effect +1.08 R20) |
| honest_ema20_gap (honest) | continuous | 99.6% | 0/5 |  | CONFIDENTLY NOTHING (raw p 1, raw effect -0.03 R20) |
| honest_inside_bar (honest) | sided | 8.8% | 0/5 |  | CONFIDENTLY NOTHING (raw p 1, raw effect +0.01 R20) |
| ema20_gap (textbook) | continuous | 99.6% | 0/2 |  |  |
| momentum14 (textbook) | continuous | 97.5% | 0/2 |  |  |
| above_vwap (textbook) | state | 55.3% | 0/2 |  |  |
| big_bar_follow (textbook) | sided | 7.4% | 0/2 |  |  |
| bar_return (textbook) | continuous | 90.4% | 0/2 |  |  |
| back4_return (textbook) | continuous | 90.9% | 0/2 |  |  |
| range_ratio (textbook) | continuous | 99.6% | 0/2 |  |  |

**Positive controls:**

| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | detected |
|---|---|---|---|---|---|---|---|
| range_ratio | rng_h1 | +0.234 | +0.220 .. +0.249 | +22% | 4e-227 | 16/16 | True |
| range4_ratio | rng_h4 | +0.313 | +0.241 .. +0.385 | +14% | 1.7e-17 | 15/16 | True |
| time_of_day | rng_h1 | +1.040 | +0.997 .. +1.083 | +98% | 0 | 9/9 | True |
| news_830 | rng_h1 | +3.576 | +3.004 .. +4.147 | +338% | 1.6e-34 | 16/16 | True |
| reversal | dir_h1 | -0.022 | -0.031 .. -0.012 | +nan% | 1.4e-05 | 15/16 | True |

U-shape, median bar range in points (2nd half of sessions) by bar start: {'03:00': 5.0, '08:15': 4.0, '08:30': 5.5, '09:30': 10.75, '12:00': 6.0, '15:45': 10.0, '20:00': 3.5}. Bar containing 8:30 ET: median 9.50 pts on NFP/CPI days (359) vs 3.00 on other days.

**Power (injected direction effect, full pipeline):**

| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |
|---|---|---|---|
| continuous | 0.01 | 50% | 0% |
| continuous | 0.02 | 100% | 75% |
| continuous | 0.03 | 100% | 100% |
| continuous | 0.05 | 100% | 100% |
| continuous | 0.08 | 100% | 100% |
| continuous | 0.12 | 100% | 100% |
| continuous | 0.20 | 100% | 100% |
| rare_events | 0.01 | 12% | 0% |
| rare_events | 0.02 | 12% | 0% |
| rare_events | 0.03 | 50% | 12% |
| rare_events | 0.05 | 100% | 25% |
| rare_events | 0.08 | 100% | 100% |
| rare_events | 0.12 | 100% | 100% |
| rare_events | 0.20 | 100% | 100% |

- continuous (136888 signal bars): MDE80 single 0.015 R20 ($0.21/micro/trade), as 1 of 100 0.022 R20 ($0.30); break-even per trade 0.129 R20 = $3.50 at the mean 2018-25 bar of these trades ($27.21 per R20) (a top-vs-bottom spread of 0.257 R20); injected effect recovered with slope 1.00.

- rare_events (3781 signal bars): MDE80 single 0.041 R20 ($1.10/micro/trade), as 1 of 100 0.071 R20 ($1.90); break-even per trade 0.130 R20 = $3.50 at the mean 2018-25 bar of these trades ($26.98 per R20); injected effect recovered with slope 1.00.
- analytic cross-check, rare_events: smallest se at dir_h1; MDE80 single 0.043 R20 ($1.17/micro/trade), as 1 of 100 0.065 R20 ($1.80).
- analytic cross-check, continuous: smallest se at dir_h1; MDE80 single 0.015 R20 ($0.20/micro/trade), as 1 of 100 0.023 R20 ($0.31).

**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. placebo), 200 random signals:** p < 0.05 for 3.0%; CONFIRMED 1, called REAL 1 (REAL & TRADABLE 0); size CONFIRMED 1. (Same signals judged without the placebo gate: called REAL 1.)

**How trustworthy are the four-way classes? (100 runs per case, rare +-1 events about once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known multiple of the $3.50 round trip; full pipeline incl. placebo for the planted-edge cases; the two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are single metrics judged without the placebo gate)**

| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |
|---|---|---|---|---|
| 200 random signals (no edge) | 0% | 0% | 60% | 39% |
| no edge (rare events) | 0% | 1% | 46% | 53% |
| edge = cost (the boundary) | 6% | 93% | 0% | 1% |
| edge = 2x cost | 100% | 0% | 0% | 0% |
| 1.5x cost on long trades, builds over 8 bars: long side tested alone | 30% | 28% | 0% | 42% |
| same, both sides pooled (true pooled edge 0.75x cost) | 4% | 21% | 13% | 62% |
| 1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars) | 27% | 31% | 1% | 41% |

For a signal firing about once per session with no edge, the lab can rule out per-trade edges bigger than about $2.65 per micro (median 90% range at holds of 1-8 bars, at recent bar sizes); break-even is 0.129 R20 = $3.50.

**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** ema20_gap: CONFIDENTLY NOTHING (best dir -0.030 R20 at dir_h16, p=1, per-trade edge now $0.44, 90% range up to $0.86 at 1-8 bars, look-ahead passed), size CONFIRMED -9% at abs_h1; momentum14: CONFIDENTLY NOTHING (best dir +0.004 R20 at dir_h1, p=1, per-trade edge now $0.07, 90% range up to $0.94 at 1-8 bars, look-ahead passed), size CONFIRMED -9% at abs_h1; above_vwap: CONFIDENTLY NOTHING (best dir +0.132 R20 at dir_eod, p=1, per-trade edge now $1.80, 90% range up to $0.40 at 1-8 bars, look-ahead passed), size CONFIRMED -4% at abs_h1; big_bar_follow: CONFIDENTLY NOTHING (best dir +0.020 R20 at dir_h4, p=1, per-trade edge now $0.50, 90% range up to $1.36 at 1-8 bars, look-ahead passed), size CONFIRMED +24% at abs_h1; bar_return: CONFIDENTLY NOTHING (best dir -0.005 R20 at dir_h1, p=1, per-trade edge now $0.07, 90% range up to $0.47 at 1-8 bars, look-ahead passed), size CONFIRMED -4% at abs_h1; back4_return: CONFIDENTLY NOTHING (best dir +0.042 R20 at dir_eod, p=1, per-trade edge now $0.56, 90% range up to $0.67 at 1-8 bars, look-ahead passed), size CONFIRMED -10% at abs_h1; range_ratio: REAL BUT TOO SMALL (best dir -0.015 R20 at dir_h1, p=0.0041, per-trade edge now $0.21, 90% range up to $0.83 at 1-8 bars, look-ahead passed), size CONFIRMED +20% at abs_h1

## MES 60-min: PASSED (3877 sessions, 88467 bars)

- [x] null: decision p < 0.05 at most nominal (<= 5% + 2 sd)
- [x] null: each single-hold p method within 5% +- 2.6 sd
- [x] null: honest t spread at 16 bars 0.8-1.25
- [x] null: no random signal CONFIRMED or called REAL in the 200-metric batch
- [x] null: 20-metric batches with any q < 0.10 at most 10%
- [x] negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd
- [x] negative: no direction CONFIRMED
- [x] look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest + 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch
- [x] positive: range_ratio (last-bar range), time_of_day, news_830 detected
- [x] power: injected effect recovered (slope 0.85-1.15)
- [x] power: 80% detection reached within the tested range
- [x] classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%
- [x] classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%
- [x] classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%
- [x] classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building over 16 bars) called CONFIDENTLY NOTHING <= 10%
- [x] null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)
- (info) positive: reversal (direction, tiny) detected: False
- (info) positive: range4_ratio (extra, weaker by design) detected: True
- (info) negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd: True

**False positives (200 random signals):** decision p < 0.05 for 1.0% (direction) and 1.0% (size); 20-metric batches with any q < 0.10: 0% of 10; CONFIRMED direction: 0; CONFIRMED size: 0. Honest t spread at 16 bars 1.02 (naive bar-by-bar 2.57).
**Real signals moved to the wrong days (56):** direction p < 0.05 0.0% (by type {'other_market_days': 0.0, 'session_shift': 0.0}), size p < 0.05 0.0% (by signal {'above_vwap': 0.0, 'back4_return': 0.0, 'bar_return': 0.0, 'big_bar_follow': 0.0, 'ema20_gap': 0.0, 'momentum14': 0.0, 'range_ratio': 0.0}); CONFIRMED direction 0, size 0.

**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a +0.54 R20 'edge'):**

| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | batch verdict |
|---|---|---|---|---|---|
| next_bar_direction (leaky) | sided | 95.3% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.54 R20) |
| whole_sample_zscore (leaky) | continuous | 98.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0.27, raw effect +0.02 R20) |
| centred_average (leaky) | continuous | 98.7% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.16 R20) |
| inside_bar_next_breakout (leaky) | sided | 6.3% | 5/5 | 7/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.70 R20) |
| big_bar_next_close_beyond (leaky) | sided | 2.9% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 3.9e-240, raw effect +1.24 R20) |
| big_bar_next_open_gap (leaky) | sided | 9.1% | 5/5 | 7/10 | INVALID (LOOK-AHEAD) (raw p 0.98, raw effect -0.02 R20) |
| very_rare_next_bar_continues (leaky) | sided | 1.2% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 4.8e-95, raw effect +1.08 R20) |
| honest_ema20_gap (honest) | continuous | 98.6% | 0/5 |  | CONFIDENTLY NOTHING (raw p 1, raw effect +0.02 R20) |
| honest_inside_bar (honest) | sided | 11.9% | 0/5 |  | CONFIDENTLY NOTHING (raw p 1, raw effect -0.02 R20) |
| ema20_gap (textbook) | continuous | 98.6% | 0/2 |  |  |
| momentum14 (textbook) | continuous | 98.1% | 0/2 |  |  |
| above_vwap (textbook) | state | 55.4% | 0/2 |  |  |
| big_bar_follow (textbook) | sided | 9.6% | 0/2 |  |  |
| bar_return (textbook) | continuous | 94.1% | 0/2 |  |  |
| back4_return (textbook) | continuous | 79.7% | 0/2 |  |  |
| range_ratio (textbook) | continuous | 98.6% | 0/2 |  |  |

**Positive controls:**

| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | detected |
|---|---|---|---|---|---|---|---|
| range_ratio | rng_h1 | +0.246 | +0.219 .. +0.272 | +23% | 8.1e-75 | 16/16 | True |
| range4_ratio | rng_h4 | +0.295 | +0.232 .. +0.359 | +14% | 4.4e-20 | 13/16 | True |
| time_of_day | rng_h1 | +1.263 | +1.223 .. +1.304 | +119% | 0 | 9/9 | True |
| news_830 | rng_h1 | +1.673 | +1.376 .. +1.970 | +158% | 2.5e-28 | 16/16 | True |
| reversal | dir_h1 | +0.015 | -0.004 .. +0.034 | +nan% | 0.2 | 9/16 | False |

U-shape, median bar range in points (2nd half of sessions) by bar start: {'03:00': 8.75, '08:00': 9.25, '09:00': 15.5, '12:00': 11.75, '15:00': 15.0, '20:00': 6.5}. Bar containing 8:30 ET: median 11.50 pts on NFP/CPI days (359) vs 5.25 on other days.

**Power (injected direction effect, full pipeline):**

| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |
|---|---|---|---|
| continuous | 0.01 | 0% | 0% |
| continuous | 0.02 | 25% | 0% |
| continuous | 0.03 | 62% | 0% |
| continuous | 0.05 | 100% | 75% |
| continuous | 0.08 | 100% | 100% |
| continuous | 0.12 | 100% | 100% |
| continuous | 0.20 | 100% | 100% |
| rare_events | 0.01 | 0% | 0% |
| rare_events | 0.02 | 0% | 0% |
| rare_events | 0.03 | 38% | 0% |
| rare_events | 0.05 | 75% | 0% |
| rare_events | 0.08 | 100% | 75% |
| rare_events | 0.12 | 100% | 100% |
| rare_events | 0.20 | 100% | 100% |

- continuous (33366 signal bars): MDE80 single 0.038 R20 ($1.05/micro/trade), as 1 of 100 0.055 R20 ($1.52); break-even per trade 0.063 R20 = $3.50 at the mean 2018-25 bar of these trades ($55.27 per R20) (a top-vs-bottom spread of 0.127 R20); injected effect recovered with slope 1.00.

- rare_events (3628 signal bars): MDE80 single 0.055 R20 ($3.02/micro/trade), as 1 of 100 0.087 R20 ($4.76); break-even per trade 0.064 R20 = $3.50 at the mean 2018-25 bar of these trades ($54.89 per R20); injected effect recovered with slope 1.00.
- analytic cross-check, rare_events: smallest se at dir_h1; MDE80 single 0.046 R20 ($2.55/micro/trade), as 1 of 100 0.071 R20 ($3.90).
- analytic cross-check, continuous: smallest se at dir_h1; MDE80 single 0.031 R20 ($0.85/micro/trade), as 1 of 100 0.047 R20 ($1.31).

**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. placebo), 200 random signals:** p < 0.05 for 1.0%; CONFIRMED 0, called REAL 0 (REAL & TRADABLE 0); size CONFIRMED 1. (Same signals judged without the placebo gate: called REAL 0.)

**How trustworthy are the four-way classes? (100 runs per case, rare +-1 events about once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known multiple of the $3.50 round trip; full pipeline incl. placebo for the planted-edge cases; the two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are single metrics judged without the placebo gate)**

| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |
|---|---|---|---|---|
| 200 random signals (no edge) | 0% | 0% | 12% | 88% |
| no edge (rare events) | 0% | 0% | 3% | 97% |
| edge = cost (the boundary) | 5% | 83% | 0% | 12% |
| edge = 2x cost | 95% | 5% | 0% | 0% |
| 1.5x cost on long trades, builds over 8 bars: long side tested alone | 2% | 2% | 0% | 96% |
| same, both sides pooled (true pooled edge 0.75x cost) | 1% | 5% | 1% | 93% |
| 1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars) | 7% | 5% | 0% | 88% |

For a signal firing about once per session with no edge, the lab can rule out per-trade edges bigger than about $4.76 per micro (median 90% range at holds of 1-8 bars, at recent bar sizes); break-even is 0.063 R20 = $3.50.

**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** ema20_gap: CONFIDENTLY NOTHING (best dir +0.018 R20 at dir_h4, p=1, per-trade edge now $0.52, 90% range up to $2.62 at 1-8 bars, look-ahead passed), size CONFIRMED -13% at abs_h1; momentum14: INCONCLUSIVE (best dir +0.017 R20 at dir_h1, p=0.14, per-trade edge now $0.59, 90% range up to $4.58 at 1-8 bars, look-ahead passed), size CONFIRMED -9% at abs_h1; above_vwap: CONFIDENTLY NOTHING (best dir +0.032 R20 at dir_h8, p=1, per-trade edge now $0.88, 90% range up to $2.28 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; big_bar_follow: CONFIDENTLY NOTHING (best dir +0.031 R20 at dir_h2, p=0.47, per-trade edge now $1.62, 90% range up to $3.50 at 1-8 bars, look-ahead passed), size CONFIRMED +23% at abs_h1; bar_return: CONFIDENTLY NOTHING (best dir +0.025 R20 at dir_h2, p=0.77, per-trade edge now $0.67, 90% range up to $1.76 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; back4_return: CONFIDENTLY NOTHING (best dir +0.017 R20 at dir_eod, p=1, per-trade edge now $0.47, 90% range up to $2.35 at 1-8 bars, look-ahead passed), size CONFIRMED -15% at abs_h1; range_ratio: CONFIDENTLY NOTHING (best dir -0.008 R20 at dir_h1, p=1, per-trade edge now $0.23, 90% range up to $1.85 at 1-8 bars, look-ahead passed), size CONFIRMED +21% at abs_h1

## MNQ 15-min: PASSED (3877 sessions, 347117 bars)

- [x] null: decision p < 0.05 at most nominal (<= 5% + 2 sd)
- [x] null: each single-hold p method within 5% +- 2.6 sd
- [x] null: honest t spread at 16 bars 0.8-1.25
- [x] null: no random signal CONFIRMED or called REAL in the 200-metric batch
- [x] null: 20-metric batches with any q < 0.10 at most 10%
- [x] negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd
- [x] negative: no direction CONFIRMED
- [x] look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest + 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch
- [x] positive: range_ratio (last-bar range), time_of_day, news_830 detected
- [x] power: injected effect recovered (slope 0.85-1.15)
- [x] power: 80% detection reached within the tested range
- [x] classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%
- [x] classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%
- [x] classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%
- [x] classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building over 16 bars) called CONFIDENTLY NOTHING <= 10%
- [x] null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)
- (info) positive: reversal (direction, tiny) detected: False
- (info) positive: range4_ratio (extra, weaker by design) detected: False
- (info) negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd: True

**False positives (200 random signals):** decision p < 0.05 for 2.5% (direction) and 0.0% (size); 20-metric batches with any q < 0.10: 0% of 10; CONFIRMED direction: 0; CONFIRMED size: 0. Honest t spread at 16 bars 1.08 (naive bar-by-bar 2.74).
**Real signals moved to the wrong days (56):** direction p < 0.05 0.0% (by type {'other_market_days': 0.0, 'session_shift': 0.0}), size p < 0.05 1.8% (by signal {'above_vwap': 0.0, 'back4_return': 0.0, 'bar_return': 0.0, 'big_bar_follow': 0.125, 'ema20_gap': 0.0, 'momentum14': 0.0, 'range_ratio': 0.0}); CONFIRMED direction 0, size 0.

**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a +0.55 R20 'edge'):**

| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | batch verdict |
|---|---|---|---|---|---|
| next_bar_direction (leaky) | sided | 96.1% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.55 R20) |
| whole_sample_zscore (leaky) | continuous | 99.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0.049, raw effect +0.02 R20) |
| centred_average (leaky) | continuous | 98.8% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 2.1e-215, raw effect +1.08 R20) |
| inside_bar_next_breakout (leaky) | sided | 6.9% | 5/5 | 8/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.75 R20) |
| big_bar_next_close_beyond (leaky) | sided | 2.6% | 5/5 | 8/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.35 R20) |
| big_bar_next_open_gap (leaky) | sided | 11.3% | 5/5 | 7/10 | INVALID (LOOK-AHEAD) (raw p 1, raw effect +0.02 R20) |
| very_rare_next_bar_continues (leaky) | sided | 1.3% | 5/5 | 8/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.17 R20) |
| honest_ema20_gap (honest) | continuous | 99.6% | 0/5 |  | INCONCLUSIVE (raw p 0.57, raw effect +0.01 R20) |
| honest_inside_bar (honest) | sided | 12.3% | 0/5 |  | CONFIDENTLY NOTHING (raw p 0.91, raw effect +0.01 R20) |
| ema20_gap (textbook) | continuous | 99.6% | 0/2 |  |  |
| momentum14 (textbook) | continuous | 98.8% | 0/2 |  |  |
| above_vwap (textbook) | state | 55.6% | 0/2 |  |  |
| big_bar_follow (textbook) | sided | 8.6% | 0/2 |  |  |
| bar_return (textbook) | continuous | 95.6% | 0/2 |  |  |
| back4_return (textbook) | continuous | 93.4% | 0/2 |  |  |
| range_ratio (textbook) | continuous | 99.6% | 0/2 |  |  |

**Positive controls:**

| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | detected |
|---|---|---|---|---|---|---|---|
| range_ratio | rng_h1 | +0.232 | +0.200 .. +0.263 | +22% | 6.1e-48 | 15/16 | True |
| range4_ratio | rng_h4 | +0.233 | +0.037 .. +0.428 | +10% | 0.02 | 15/16 | False |
| time_of_day | rng_h1 | +1.142 | +1.074 .. +1.209 | +107% | 1.8e-242 | 9/9 | True |
| news_830 | rng_h1 | +3.602 | +3.013 .. +4.190 | +335% | 3.9e-33 | 16/16 | True |
| reversal | dir_h1 | -0.005 | -0.015 .. +0.004 | +nan% | 0.34 | 10/16 | False |

U-shape, median bar range in points (2nd half of sessions) by bar start: {'03:00': 20.0, '08:15': 16.25, '08:30': 22.0, '09:30': 58.0, '12:00': 27.25, '15:45': 36.5, '20:00': 14.5}. Bar containing 8:30 ET: median 23.75 pts on NFP/CPI days (359) vs 8.00 on other days.

**Power (injected direction effect, full pipeline):**

| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |
|---|---|---|---|
| continuous | 0.01 | 12% | 0% |
| continuous | 0.02 | 88% | 0% |
| continuous | 0.03 | 100% | 88% |
| continuous | 0.05 | 100% | 100% |
| continuous | 0.08 | 100% | 100% |
| continuous | 0.12 | 100% | 100% |
| continuous | 0.20 | 100% | 100% |
| rare_events | 0.01 | 0% | 0% |
| rare_events | 0.02 | 12% | 0% |
| rare_events | 0.03 | 25% | 0% |
| rare_events | 0.05 | 38% | 25% |
| rare_events | 0.08 | 100% | 38% |
| rare_events | 0.12 | 100% | 88% |
| rare_events | 0.20 | 100% | 100% |

- continuous (136826 signal bars): MDE80 single 0.019 R20 ($0.42/micro/trade), as 1 of 100 0.029 R20 ($0.65); break-even per trade 0.045 R20 = $2.00 at the mean 2018-25 bar of these trades ($44.88 per R20) (a top-vs-bottom spread of 0.089 R20); injected effect recovered with slope 1.00.

- rare_events (3782 signal bars): MDE80 single 0.069 R20 ($3.09/micro/trade), as 1 of 100 0.113 R20 ($5.07); break-even per trade 0.045 R20 = $2.00 at the mean 2018-25 bar of these trades ($44.89 per R20); injected effect recovered with slope 1.00.
- analytic cross-check, rare_events: smallest se at dir_h1; MDE80 single 0.046 R20 ($2.03/micro/trade), as 1 of 100 0.070 R20 ($3.12).
- analytic cross-check, continuous: smallest se at dir_h1; MDE80 single 0.016 R20 ($0.36/micro/trade), as 1 of 100 0.024 R20 ($0.54).

**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. placebo), 200 random signals:** p < 0.05 for 2.5%; CONFIRMED 1, called REAL 1 (REAL & TRADABLE 0); size CONFIRMED 0. (Same signals judged without the placebo gate: called REAL 2.)

**How trustworthy are the four-way classes? (100 runs per case, rare +-1 events about once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known multiple of the $2.00 round trip; full pipeline incl. placebo for the planted-edge cases; the two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are single metrics judged without the placebo gate)**

| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |
|---|---|---|---|---|
| 200 random signals (no edge) | 0% | 1% | 3% | 96% |
| no edge (rare events) | 0% | 0% | 0% | 100% |
| edge = cost (the boundary) | 6% | 28% | 0% | 66% |
| edge = 2x cost | 74% | 23% | 0% | 3% |
| 1.5x cost on long trades, builds over 8 bars: long side tested alone | 0% | 1% | 0% | 99% |
| same, both sides pooled (true pooled edge 0.75x cost) | 0% | 0% | 0% | 100% |
| 1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars) | 0% | 0% | 0% | 100% |

For a signal firing about once per session with no edge, the lab can rule out per-trade edges bigger than about $4.70 per micro (median 90% range at holds of 1-8 bars, at recent bar sizes); break-even is 0.045 R20 = $2.00.

**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** ema20_gap: INCONCLUSIVE (best dir +0.009 R20 at dir_h1, p=0.57, per-trade edge now $0.22, 90% range up to $1.54 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; momentum14: INCONCLUSIVE (best dir +0.007 R20 at dir_h1, p=1, per-trade edge now $0.22, 90% range up to $1.49 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; above_vwap: INCONCLUSIVE (best dir +0.263 R20 at dir_eod, p=1, per-trade edge now $5.87, 90% range up to $0.85 at 1-8 bars, look-ahead passed), size CONFIRMED -4% at abs_h1; big_bar_follow: INCONCLUSIVE (best dir +0.019 R20 at dir_h2, p=0.44, per-trade edge now $0.80, 90% range up to $1.76 at 1-8 bars, look-ahead passed), size CONFIRMED +23% at abs_h1; bar_return: CONFIDENTLY NOTHING (best dir +0.063 R20 at dir_eod, p=1, per-trade edge now $1.37, 90% range up to $0.84 at 1-8 bars, look-ahead passed), size CONFIRMED -4% at abs_h1; back4_return: CONFIDENTLY NOTHING (best dir +0.005 R20 at dir_h1, p=1, per-trade edge now $0.12, 90% range up to $1.01 at 1-8 bars, look-ahead passed), size CONFIRMED -10% at abs_h1; range_ratio: INCONCLUSIVE (best dir -0.018 R20 at dir_h1, p=0.069, per-trade edge now $0.40, 90% range up to $1.74 at 1-8 bars, look-ahead passed), size CONFIRMED +20% at abs_h1

## MNQ 60-min: PASSED (3877 sessions, 88465 bars)

- [x] null: decision p < 0.05 at most nominal (<= 5% + 2 sd)
- [x] null: each single-hold p method within 5% +- 2.6 sd
- [x] null: honest t spread at 16 bars 0.8-1.25
- [x] null: no random signal CONFIRMED or called REAL in the 200-metric batch
- [x] null: 20-metric batches with any q < 0.10 at most 10%
- [x] negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd
- [x] negative: no direction CONFIRMED
- [x] look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest + 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch
- [x] positive: range_ratio (last-bar range), time_of_day, news_830 detected
- [x] power: injected effect recovered (slope 0.85-1.15)
- [x] power: 80% detection reached within the tested range
- [x] classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%
- [x] classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%
- [x] classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%
- [x] classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building over 16 bars) called CONFIDENTLY NOTHING <= 10%
- [x] null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)
- (info) positive: reversal (direction, tiny) detected: False
- (info) positive: range4_ratio (extra, weaker by design) detected: True
- (info) negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd: True

**False positives (200 random signals):** decision p < 0.05 for 3.0% (direction) and 1.0% (size); 20-metric batches with any q < 0.10: 0% of 10; CONFIRMED direction: 0; CONFIRMED size: 0. Honest t spread at 16 bars 1.09 (naive bar-by-bar 2.78).
**Real signals moved to the wrong days (56):** direction p < 0.05 1.8% (by type {'other_market_days': 0.0, 'session_shift': 0.02857142857142857}), size p < 0.05 1.8% (by signal {'above_vwap': 0.0, 'back4_return': 0.0, 'bar_return': 0.125, 'big_bar_follow': 0.0, 'ema20_gap': 0.0, 'momentum14': 0.0, 'range_ratio': 0.0}); CONFIRMED direction 0, size 0.

**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a +0.54 R20 'edge'):**

| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | batch verdict |
|---|---|---|---|---|---|
| next_bar_direction (leaky) | sided | 98.0% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.54 R20) |
| whole_sample_zscore (leaky) | continuous | 98.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0.3, raw effect +0.02 R20) |
| centred_average (leaky) | continuous | 99.4% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 6.7e-256, raw effect +1.14 R20) |
| inside_bar_next_breakout (leaky) | sided | 7.8% | 5/5 | 7/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.68 R20) |
| big_bar_next_close_beyond (leaky) | sided | 3.6% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.34 R20) |
| big_bar_next_open_gap (leaky) | sided | 12.8% | 5/5 | 6/10 | INVALID (LOOK-AHEAD) (raw p 1, raw effect +0.02 R20) |
| very_rare_next_bar_continues (leaky) | sided | 1.7% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 5.5e-122, raw effect +1.19 R20) |
| honest_ema20_gap (honest) | continuous | 98.6% | 0/5 |  | INCONCLUSIVE (raw p 1, raw effect +0.01 R20) |
| honest_inside_bar (honest) | sided | 14.6% | 0/5 |  | INCONCLUSIVE (raw p 1, raw effect -0.02 R20) |
| ema20_gap (textbook) | continuous | 98.6% | 0/2 |  |  |
| momentum14 (textbook) | continuous | 98.7% | 0/2 |  |  |
| above_vwap (textbook) | state | 55.7% | 0/2 |  |  |
| big_bar_follow (textbook) | sided | 11.4% | 0/2 |  |  |
| bar_return (textbook) | continuous | 96.7% | 0/2 |  |  |
| back4_return (textbook) | continuous | 80.7% | 0/2 |  |  |
| range_ratio (textbook) | continuous | 98.6% | 0/2 |  |  |

**Positive controls:**

| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | detected |
|---|---|---|---|---|---|---|---|
| range_ratio | rng_h1 | +0.227 | +0.200 .. +0.254 | +21% | 1.3e-62 | 16/16 | True |
| range4_ratio | rng_h4 | +0.270 | +0.214 .. +0.326 | +12% | 2.9e-21 | 14/16 | True |
| time_of_day | rng_h1 | +1.386 | +1.343 .. +1.428 | +130% | 0 | 9/9 | True |
| news_830 | rng_h1 | +1.605 | +1.311 .. +1.899 | +149% | 1.2e-26 | 16/16 | True |
| reversal | dir_h1 | +0.019 | -0.001 .. +0.040 | +nan% | 0.09 | 11/16 | False |

U-shape, median bar range in points (2nd half of sessions) by bar start: {'03:00': 36.0, '08:00': 39.5, '09:00': 80.25, '12:00': 51.5, '15:00': 58.0, '20:00': 26.0}. Bar containing 8:30 ET: median 27.50 pts on NFP/CPI days (359) vs 14.50 on other days.

**Power (injected direction effect, full pipeline):**

| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |
|---|---|---|---|
| continuous | 0.01 | 0% | 0% |
| continuous | 0.02 | 12% | 0% |
| continuous | 0.03 | 75% | 0% |
| continuous | 0.05 | 100% | 75% |
| continuous | 0.08 | 100% | 100% |
| continuous | 0.12 | 100% | 100% |
| continuous | 0.20 | 100% | 100% |
| rare_events | 0.01 | 0% | 0% |
| rare_events | 0.02 | 12% | 0% |
| rare_events | 0.03 | 25% | 0% |
| rare_events | 0.05 | 88% | 12% |
| rare_events | 0.08 | 100% | 100% |
| rare_events | 0.12 | 100% | 100% |
| rare_events | 0.20 | 100% | 100% |

- continuous (33365 signal bars): MDE80 single 0.033 R20 ($1.53/micro/trade), as 1 of 100 0.055 R20 ($2.53); break-even per trade 0.022 R20 = $2.00 at the mean 2018-25 bar of these trades ($91.96 per R20) (a top-vs-bottom spread of 0.043 R20); injected effect recovered with slope 1.00.

- rare_events (3622 signal bars): MDE80 single 0.047 R20 ($4.28/micro/trade), as 1 of 100 0.072 R20 ($6.53); break-even per trade 0.022 R20 = $2.00 at the mean 2018-25 bar of these trades ($90.95 per R20); injected effect recovered with slope 1.00.
- analytic cross-check, rare_events: smallest se at dir_h1; MDE80 single 0.048 R20 ($4.43/micro/trade), as 1 of 100 0.074 R20 ($6.79).
- analytic cross-check, continuous: smallest se at dir_h1; MDE80 single 0.032 R20 ($1.48/micro/trade), as 1 of 100 0.050 R20 ($2.27).

**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. placebo), 200 random signals:** p < 0.05 for 3.0%; CONFIRMED 2, called REAL 2 (REAL & TRADABLE 0); size CONFIRMED 0. (Same signals judged without the placebo gate: called REAL 2.)

**How trustworthy are the four-way classes? (100 runs per case, rare +-1 events about once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known multiple of the $2.00 round trip; full pipeline incl. placebo for the planted-edge cases; the two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are single metrics judged without the placebo gate)**

| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |
|---|---|---|---|---|
| 200 random signals (no edge) | 0% | 1% | 0% | 99% |
| no edge (rare events) | 0% | 0% | 0% | 100% |
| edge = cost (the boundary) | 3% | 2% | 0% | 95% |
| edge = 2x cost | 33% | 10% | 0% | 57% |
| 1.5x cost on long trades, builds over 8 bars: long side tested alone | 0% | 0% | 0% | 100% |
| same, both sides pooled (true pooled edge 0.75x cost) | 1% | 1% | 0% | 98% |
| 1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars) | 2% | 0% | 0% | 98% |

For a signal firing about once per session with no edge, the lab can rule out per-trade edges bigger than about $8.15 per micro (median 90% range at holds of 1-8 bars, at recent bar sizes); break-even is 0.022 R20 = $2.00.

**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** ema20_gap: INCONCLUSIVE (best dir +0.007 R20 at dir_h1, p=1, per-trade edge now $0.32, 90% range up to $4.17 at 1-8 bars, look-ahead passed), size CONFIRMED -11% at abs_h1; momentum14: REAL BUT TOO SMALL (best dir +0.024 R20 at dir_h1, p=0.029, per-trade edge now $1.30, 90% range up to $7.40 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; above_vwap: INCONCLUSIVE (best dir +0.056 R20 at dir_h16, p=1, per-trade edge now $2.55, 90% range up to $3.73 at 1-8 bars, look-ahead passed), size CONFIRMED -7% at abs_h1; big_bar_follow: INCONCLUSIVE (best dir +0.052 R20 at dir_h4, p=0.11, per-trade edge now $4.38, 90% range up to $7.77 at 1-8 bars, look-ahead passed), size CONFIRMED +20% at abs_h1; bar_return: INCONCLUSIVE (best dir +0.031 R20 at dir_h2, p=0.31, per-trade edge now $1.38, 90% range up to $3.82 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; back4_return: INCONCLUSIVE (best dir +0.021 R20 at dir_h4, p=1, per-trade edge now $0.94, 90% range up to $4.26 at 1-8 bars, look-ahead passed), size CONFIRMED -13% at abs_h1; range_ratio: INCONCLUSIVE (best dir -0.006 R20 at dir_h1, p=1, per-trade edge now $0.28, 90% range up to $3.73 at 1-8 bars, look-ahead passed), size CONFIRMED +19% at abs_h1

## MYM 15-min: PASSED (1936 sessions, 173952 bars)

- [x] null: decision p < 0.05 at most nominal (<= 5% + 2 sd)
- [x] null: each single-hold p method within 5% +- 2.6 sd
- [x] null: honest t spread at 16 bars 0.8-1.25
- [x] null: no random signal CONFIRMED or called REAL in the 200-metric batch
- [x] null: 20-metric batches with any q < 0.10 at most 10%
- [x] negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd
- [x] negative: no direction CONFIRMED
- [x] look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest + 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch
- [x] positive: range_ratio (last-bar range), time_of_day, news_830 detected
- [x] power: injected effect recovered (slope 0.85-1.15)
- [x] power: 80% detection reached within the tested range
- [x] classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%
- [x] classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%
- [x] classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%
- [x] classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building over 16 bars) called CONFIDENTLY NOTHING <= 10%
- [x] null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)
- (info) positive: reversal (direction, tiny) detected: False
- (info) positive: range4_ratio (extra, weaker by design) detected: False
- (info) negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd: True

**False positives (200 random signals):** decision p < 0.05 for 1.0% (direction) and 0.5% (size); 20-metric batches with any q < 0.10: 0% of 10; CONFIRMED direction: 0; CONFIRMED size: 0. Honest t spread at 16 bars 1.07 (naive bar-by-bar 2.57).
**Real signals moved to the wrong days (56):** direction p < 0.05 1.8% (by type {'other_market_days': 0.047619047619047616, 'session_shift': 0.0}), size p < 0.05 0.0% (by signal {'above_vwap': 0.0, 'back4_return': 0.0, 'bar_return': 0.0, 'big_bar_follow': 0.0, 'ema20_gap': 0.0, 'momentum14': 0.0, 'range_ratio': 0.0}); CONFIRMED direction 0, size 0.

**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a +0.54 R20 'edge'):**

| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | batch verdict |
|---|---|---|---|---|---|
| next_bar_direction (leaky) | sided | 97.2% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.54 R20) |
| whole_sample_zscore (leaky) | continuous | 99.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 1, raw effect -0.05 R20) |
| centred_average (leaky) | continuous | 99.2% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.18 R20) |
| inside_bar_next_breakout (leaky) | sided | 7.1% | 5/5 | 7/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.74 R20) |
| big_bar_next_close_beyond (leaky) | sided | 2.4% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 3.5e-228, raw effect +1.28 R20) |
| big_bar_next_open_gap (leaky) | sided | 11.8% | 5/5 | 6/10 | INVALID (LOOK-AHEAD) (raw p 1, raw effect +0.01 R20) |
| very_rare_next_bar_continues (leaky) | sided | 1.2% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 2.9e-103, raw effect +1.14 R20) |
| honest_ema20_gap (honest) | continuous | 99.6% | 0/5 |  | CONFIDENTLY NOTHING (raw p 1, raw effect -0.03 R20) |
| honest_inside_bar (honest) | sided | 12.8% | 0/5 |  | CONFIDENTLY NOTHING (raw p 1, raw effect +0.01 R20) |
| ema20_gap (textbook) | continuous | 99.6% | 0/2 |  |  |
| momentum14 (textbook) | continuous | 99.1% | 0/2 |  |  |
| above_vwap (textbook) | state | 54.5% | 0/2 |  |  |
| big_bar_follow (textbook) | sided | 8.1% | 0/2 |  |  |
| bar_return (textbook) | continuous | 96.9% | 0/2 |  |  |
| back4_return (textbook) | continuous | 94.0% | 0/2 |  |  |
| range_ratio (textbook) | continuous | 99.6% | 0/2 |  |  |

**Positive controls:**

| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | detected |
|---|---|---|---|---|---|---|---|
| range_ratio | rng_h1 | +0.230 | +0.188 .. +0.271 | +21% | 4.3e-27 | 7/8 | True |
| range4_ratio | rng_h4 | +0.214 | -0.031 .. +0.459 | +9% | 0.087 | 7/8 | False |
| time_of_day | rng_h1 | +1.331 | +1.288 .. +1.375 | +123% | 0 | 5/5 | True |
| news_830 | rng_h1 | +4.156 | +3.242 .. +5.070 | +389% | 5e-19 | 8/8 | True |
| reversal | dir_h1 | -0.018 | -0.032 .. -0.004 | +nan% | 0.034 | 7/8 | False |

U-shape, median bar range in points (2nd half of sessions) by bar start: {'03:00': 41.0, '08:15': 32.0, '08:30': 50.5, '09:30': 124.0, '12:00': 56.0, '15:45': 83.0, '20:00': 25.0}. Bar containing 8:30 ET: median 146.00 pts on NFP/CPI days (179) vs 37.00 on other days.

**Power (injected direction effect, full pipeline):**

| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |
|---|---|---|---|
| continuous | 0.01 | 0% | 0% |
| continuous | 0.02 | 50% | 0% |
| continuous | 0.03 | 88% | 25% |
| continuous | 0.05 | 100% | 88% |
| continuous | 0.08 | 100% | 100% |
| continuous | 0.12 | 100% | 100% |
| continuous | 0.20 | 100% | 100% |
| rare_events | 0.01 | 0% | 0% |
| rare_events | 0.02 | 0% | 0% |
| rare_events | 0.03 | 0% | 0% |
| rare_events | 0.05 | 25% | 0% |
| rare_events | 0.08 | 88% | 25% |
| rare_events | 0.12 | 100% | 88% |
| rare_events | 0.20 | 100% | 100% |

- continuous (68572 signal bars): MDE80 single 0.028 R20 ($0.29/micro/trade), as 1 of 100 0.047 R20 ($0.49); break-even per trade 0.097 R20 = $2.00 at the mean 2018-25 bar of these trades ($20.68 per R20) (a top-vs-bottom spread of 0.193 R20); injected effect recovered with slope 1.00.

- rare_events (1897 signal bars): MDE80 single 0.076 R20 ($1.56/micro/trade), as 1 of 100 0.114 R20 ($2.36); break-even per trade 0.097 R20 = $2.00 at the mean 2018-25 bar of these trades ($20.68 per R20); injected effect recovered with slope 1.00.
- analytic cross-check, rare_events: smallest se at dir_h1; MDE80 single 0.062 R20 ($1.27/micro/trade), as 1 of 100 0.095 R20 ($1.95).
- analytic cross-check, continuous: smallest se at dir_h1; MDE80 single 0.024 R20 ($0.25/micro/trade), as 1 of 100 0.037 R20 ($0.38).

**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. placebo), 200 random signals:** p < 0.05 for 1.0%; CONFIRMED 0, called REAL 0 (REAL & TRADABLE 0); size CONFIRMED 0. (Same signals judged without the placebo gate: called REAL 0.)

**How trustworthy are the four-way classes? (100 runs per case, rare +-1 events about once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known multiple of the $2.00 round trip; full pipeline incl. placebo for the planted-edge cases; the two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are single metrics judged without the placebo gate)**

| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |
|---|---|---|---|---|
| 200 random signals (no edge) | 0% | 0% | 14% | 86% |
| no edge (rare events) | 0% | 0% | 0% | 100% |
| edge = cost (the boundary) | 8% | 80% | 0% | 12% |
| edge = 2x cost | 100% | 0% | 0% | 0% |
| 1.5x cost on long trades, builds over 8 bars: long side tested alone | 5% | 1% | 0% | 94% |
| same, both sides pooled (true pooled edge 0.75x cost) | 0% | 1% | 0% | 99% |
| 1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars) | 2% | 0% | 0% | 98% |

For a signal firing about once per session with no edge, the lab can rule out per-trade edges bigger than about $3.37 per micro (median 90% range at holds of 1-8 bars, at recent bar sizes); break-even is 0.097 R20 = $2.00.

**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** ema20_gap: CONFIDENTLY NOTHING (best dir -0.026 R20 at dir_h16, p=1, per-trade edge now $0.30, 90% range up to $1.33 at 1-8 bars, look-ahead passed), size CONFIRMED -10% at abs_h1; momentum14: CONFIDENTLY NOTHING (best dir -0.043 R20 at dir_h8, p=1, per-trade edge now $0.62, 90% range up to $1.69 at 1-8 bars, look-ahead passed), size CONFIRMED -8% at abs_h1; above_vwap: CONFIDENTLY NOTHING (best dir +0.062 R20 at dir_h16, p=1, per-trade edge now $0.64, 90% range up to $0.84 at 1-8 bars, look-ahead passed), size CONFIRMED -5% at abs_h1; big_bar_follow: CONFIDENTLY NOTHING (best dir +0.042 R20 at dir_h4, p=0.44, per-trade edge now $0.77, 90% range up to $1.87 at 1-8 bars, look-ahead passed), size CONFIRMED +22% at abs_h1; bar_return: CONFIDENTLY NOTHING (best dir -0.011 R20 at dir_h2, p=1, per-trade edge now $0.11, 90% range up to $0.36 at 1-8 bars, look-ahead passed), size possible -4% at abs_h1; back4_return: CONFIDENTLY NOTHING (best dir +0.010 R20 at dir_h1, p=1, per-trade edge now $0.10, 90% range up to $0.84 at 1-8 bars, look-ahead passed), size CONFIRMED -10% at abs_h1; range_ratio: INCONCLUSIVE (best dir +0.594 R20 at dir_eod, p=1, per-trade edge now $6.07, 90% range up to $2.00 at 1-8 bars, look-ahead passed), size CONFIRMED +20% at abs_h1

## MYM 60-min: PASSED (1936 sessions, 44179 bars)

- [x] null: decision p < 0.05 at most nominal (<= 5% + 2 sd)
- [x] null: each single-hold p method within 5% +- 2.6 sd
- [x] null: honest t spread at 16 bars 0.8-1.25
- [x] null: no random signal CONFIRMED or called REAL in the 200-metric batch
- [x] null: 20-metric batches with any q < 0.10 at most 10%
- [x] negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd
- [x] negative: no direction CONFIRMED
- [x] look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest + 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch
- [x] positive: range_ratio (last-bar range), time_of_day, news_830 detected
- [x] power: injected effect recovered (slope 0.85-1.15)
- [x] power: 80% detection reached within the tested range
- [x] classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%
- [x] classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%
- [x] classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%
- [x] classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building over 16 bars) called CONFIDENTLY NOTHING <= 10%
- [x] null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)
- (info) positive: reversal (direction, tiny) detected: False
- (info) positive: range4_ratio (extra, weaker by design) detected: True
- (info) negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd: True

**False positives (200 random signals):** decision p < 0.05 for 3.0% (direction) and 3.0% (size); 20-metric batches with any q < 0.10: 0% of 10; CONFIRMED direction: 0; CONFIRMED size: 0. Honest t spread at 16 bars 1.01 (naive bar-by-bar 2.40).
**Real signals moved to the wrong days (56):** direction p < 0.05 0.0% (by type {'other_market_days': 0.0, 'session_shift': 0.0}), size p < 0.05 1.8% (by signal {'above_vwap': 0.0, 'back4_return': 0.0, 'bar_return': 0.125, 'big_bar_follow': 0.0, 'ema20_gap': 0.0, 'momentum14': 0.0, 'range_ratio': 0.0}); CONFIRMED direction 0, size 0.

**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a +0.53 R20 'edge'):**

| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | batch verdict |
|---|---|---|---|---|---|
| next_bar_direction (leaky) | sided | 98.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.53 R20) |
| whole_sample_zscore (leaky) | continuous | 98.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 1, raw effect +0.01 R20) |
| centred_average (leaky) | continuous | 99.6% | 5/5 | 0/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +1.28 R20) |
| inside_bar_next_breakout (leaky) | sided | 8.1% | 5/5 | 9/10 | INVALID (LOOK-AHEAD) (raw p 0, raw effect +0.68 R20) |
| big_bar_next_close_beyond (leaky) | sided | 3.2% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 2.9e-88, raw effect +1.33 R20) |
| big_bar_next_open_gap (leaky) | sided | 13.5% | 5/5 | 2/10 | INVALID (LOOK-AHEAD) (raw p 1, raw effect +0.03 R20) |
| very_rare_next_bar_continues (leaky) | sided | 1.5% | 5/5 | 10/10 | INVALID (LOOK-AHEAD) (raw p 8.7e-54, raw effect +1.07 R20) |
| honest_ema20_gap (honest) | continuous | 98.6% | 0/5 |  | INCONCLUSIVE (raw p 1, raw effect +0.02 R20) |
| honest_inside_bar (honest) | sided | 14.9% | 0/5 |  | INCONCLUSIVE (raw p 1, raw effect +0.05 R20) |
| ema20_gap (textbook) | continuous | 98.6% | 0/2 |  |  |
| momentum14 (textbook) | continuous | 98.8% | 0/2 |  |  |
| above_vwap (textbook) | state | 54.7% | 0/2 |  |  |
| big_bar_follow (textbook) | sided | 10.5% | 0/2 |  |  |
| bar_return (textbook) | continuous | 97.4% | 0/2 |  |  |
| back4_return (textbook) | continuous | 80.9% | 0/2 |  |  |
| range_ratio (textbook) | continuous | 98.6% | 0/2 |  |  |

**Positive controls:**

| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | detected |
|---|---|---|---|---|---|---|---|
| range_ratio | rng_h1 | +0.269 | +0.219 .. +0.318 | +25% | 1e-26 | 8/8 | True |
| range4_ratio | rng_h4 | +0.358 | +0.259 .. +0.458 | +16% | 1.5e-12 | 6/8 | True |
| time_of_day | rng_h1 | +1.546 | +1.479 .. +1.612 | +143% | 0 | 5/5 | True |
| news_830 | rng_h1 | +1.822 | +1.357 .. +2.287 | +171% | 1.6e-14 | 8/8 | True |
| reversal | dir_h1 | +0.010 | -0.018 .. +0.038 | +nan% | 0.62 | 5/8 | False |

U-shape, median bar range in points (2nd half of sessions) by bar start: {'03:00': 71.0, '08:00': 84.0, '09:00': 169.0, '12:00': 110.5, '15:00': 131.0, '20:00': 44.5}. Bar containing 8:30 ET: median 173.00 pts on NFP/CPI days (179) vs 68.00 on other days.

**Power (injected direction effect, full pipeline):**

| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |
|---|---|---|---|
| continuous | 0.01 | 0% | 0% |
| continuous | 0.02 | 12% | 0% |
| continuous | 0.03 | 12% | 0% |
| continuous | 0.05 | 100% | 12% |
| continuous | 0.08 | 100% | 100% |
| continuous | 0.12 | 100% | 100% |
| continuous | 0.20 | 100% | 100% |
| rare_events | 0.01 | 12% | 0% |
| rare_events | 0.02 | 12% | 0% |
| rare_events | 0.03 | 12% | 0% |
| rare_events | 0.05 | 50% | 12% |
| rare_events | 0.08 | 100% | 25% |
| rare_events | 0.12 | 100% | 100% |
| rare_events | 0.20 | 100% | 100% |

- continuous (16662 signal bars): MDE80 single 0.044 R20 ($0.94/micro/trade), as 1 of 100 0.072 R20 ($1.52); break-even per trade 0.047 R20 = $2.00 at the mean 2018-25 bar of these trades ($42.43 per R20) (a top-vs-bottom spread of 0.094 R20); injected effect recovered with slope 0.99.

- rare_events (1823 signal bars): MDE80 single 0.066 R20 ($2.82/micro/trade), as 1 of 100 0.108 R20 ($4.58); break-even per trade 0.047 R20 = $2.00 at the mean 2018-25 bar of these trades ($42.50 per R20); injected effect recovered with slope 1.00.
- analytic cross-check, rare_events: smallest se at dir_h1; MDE80 single 0.066 R20 ($2.78/micro/trade), as 1 of 100 0.101 R20 ($4.25).
- analytic cross-check, continuous: smallest se at dir_h1; MDE80 single 0.044 R20 ($0.93/micro/trade), as 1 of 100 0.067 R20 ($1.43).

**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. placebo), 200 random signals:** p < 0.05 for 3.0%; CONFIRMED 0, called REAL 0 (REAL & TRADABLE 0); size CONFIRMED 1. (Same signals judged without the placebo gate: called REAL 0.)

**How trustworthy are the four-way classes? (100 runs per case, rare +-1 events about once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known multiple of the $2.00 round trip; full pipeline incl. placebo for the planted-edge cases; the two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are single metrics judged without the placebo gate)**

| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |
|---|---|---|---|---|
| 200 random signals (no edge) | 0% | 0% | 0% | 100% |
| no edge (rare events) | 0% | 0% | 0% | 100% |
| edge = cost (the boundary) | 12% | 11% | 0% | 77% |
| edge = 2x cost | 85% | 7% | 0% | 8% |
| 1.5x cost on long trades, builds over 8 bars: long side tested alone | 2% | 0% | 0% | 98% |
| same, both sides pooled (true pooled edge 0.75x cost) | 0% | 1% | 0% | 99% |
| 1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars) | 0% | 0% | 0% | 100% |

For a signal firing about once per session with no edge, the lab can rule out per-trade edges bigger than about $5.53 per micro (median 90% range at holds of 1-8 bars, at recent bar sizes); break-even is 0.047 R20 = $2.00.

**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** ema20_gap: INCONCLUSIVE (best dir +0.016 R20 at dir_h1, p=1, per-trade edge now $0.34, 90% range up to $4.17 at 1-8 bars, look-ahead passed), size CONFIRMED -10% at abs_h1; momentum14: INCONCLUSIVE (best dir +0.044 R20 at dir_h4, p=1, per-trade edge now $1.17, 90% range up to $4.78 at 1-8 bars, look-ahead passed), size CONFIRMED -10% at abs_h1; above_vwap: INCONCLUSIVE (best dir +0.015 R20 at dir_h4, p=1, per-trade edge now $0.32, 90% range up to $2.15 at 1-8 bars, look-ahead passed), size CONFIRMED -6% at abs_h1; big_bar_follow: INCONCLUSIVE (best dir +0.042 R20 at dir_h1, p=0.17, per-trade edge now $1.62, 90% range up to $3.76 at 1-8 bars, look-ahead passed), size CONFIRMED +25% at abs_h1; bar_return: CONFIDENTLY NOTHING (best dir -0.033 R20 at dir_eod, p=1, per-trade edge now $0.68, 90% range up to $1.39 at 1-8 bars, look-ahead passed), size CONFIRMED -7% at abs_h1; back4_return: INCONCLUSIVE (best dir +0.010 R20 at dir_h1, p=1, per-trade edge now $0.21, 90% range up to $2.56 at 1-8 bars, look-ahead passed), size CONFIRMED -15% at abs_h1; range_ratio: INCONCLUSIVE (best dir -0.012 R20 at dir_h1, p=1, per-trade edge now $0.26, 90% range up to $3.12 at 1-8 bars, look-ahead passed), size CONFIRMED +24% at abs_h1

