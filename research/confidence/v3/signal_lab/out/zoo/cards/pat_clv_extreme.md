# Impact card: pat_clv_extreme

candle pattern clv_extreme in its textbook direction: range >= 4 ticks; close in the bottom 20% of the range -> bullish, top 20% -> bearish (reversal) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: POSSIBLE direction effect +0.006 average bars (~$0.10 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.0204, replicated in the other half=False, 13 of 16 years); best leg (event, with signal) grosses $+0.18 and nets $-3.32 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.010 R20, CONFIRMED, q=7.39e-09, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.18 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.204 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: POSSIBLE direction effect +0.009 average bars (~$0.24 per micro at 2018-25 bar sizes) over the next 1 bar (15 min) (in the signal's direction), not confirmed (q=0.00631, replicated in the other half=False, 13 of 16 years); best leg (event, with signal) grosses $+0.28 and nets $-3.22 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: no measurable effect on how much price moves (best p=0.17).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.33 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.125 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.020 R20 over the next 16 bars (16 h), p=0.92; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.21 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=0.074; we would catch an effect of 0.008 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.008 R20, CONFIRMED, q=0.00168, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.27 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.077 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.017 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.52 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.043 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (2 h), p=0.46; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.11).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.02 at recent bar sizes, 90% range up to $3.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=0.49; we would catch an effect of 0.011 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.27).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.12 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.170 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (15 min), p=0.12; we would catch an effect of 0.024 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.38 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.096 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.004 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.034 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.50 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.047 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.006 | +0.003 .. +0.009 | +0.0056 | 9.9e-05 / 2.1e-05 / 8.4e-06 | 0.00026 | 0.0204 | 0.045 | 13/16 | +0.007 | +0.005 | False | +4.6 / +3.9 |  |
| MES | 5 | h2 | +0.007 | +0.003 .. +0.011 | +0.0046 | 0.00093 / 0.00037 / 0.00024 | 0.000521 |  |  | 12/16 | +0.010 | +0.004 |  | +3.8 / +3.3 |  |
| MES | 5 | h4 | +0.001 | -0.004 .. +0.006 | +0.0005 | 0.64 / 0.63 / 0.68 | 0.678 |  |  | 10/16 | +0.002 | +0.001 |  | +0.5 / +0.5 | 0.008 |
| MES | 5 | h8 | -0.003 | -0.010 .. +0.004 | -0.0010 | 0.36 / 0.36 / 0.38 | 0.386 |  |  | 9/16 | +0.001 | -0.007 |  | -0.9 / -0.9 |  |
| MES | 5 | h16 | -0.002 | -0.011 .. +0.008 | -0.0003 | 0.76 / 0.76 / 0.77 | 0.777 |  |  | 9/16 | +0.006 | -0.009 |  | -0.3 / -0.3 |  |
| MES | 5 | eod | +0.014 | -0.034 .. +0.061 | +0.0006 | 0.57 / 0.58 / 0.56 | 0.544 |  |  | 9/16 | -0.005 | +0.032 |  | +0.6 / +0.6 |  |
| MES | 15 | h1 * | +0.009 | +0.005 .. +0.013 | +0.0088 | 2.9e-05 / 2.6e-05 / 6e-05 | 0.00026 | 0.00631 | 0.011 | 13/16 | +0.008 | +0.009 | False | +4.1 / +4.2 |  |
| MES | 15 | h2 | +0.002 | -0.004 .. +0.008 | +0.0016 | 0.43 / 0.42 / 0.45 | 0.457 |  |  | 10/16 | +0.003 | +0.002 |  | +0.8 / +0.8 |  |
| MES | 15 | h4 | +0.001 | -0.008 .. +0.009 | +0.0003 | 0.86 / 0.86 / 0.86 | 0.862 |  |  | 8/16 | +0.003 | -0.002 |  | +0.2 / +0.2 | 0.013 |
| MES | 15 | h8 | +0.001 | -0.011 .. +0.012 | +0.0002 | 0.93 / 0.92 / 0.93 | 0.928 |  |  | 7/16 | +0.005 | -0.004 |  | +0.1 / +0.1 |  |
| MES | 15 | h16 | -0.002 | -0.019 .. +0.015 | -0.0004 | 0.85 / 0.85 / 0.86 | 0.86 |  |  | 9/16 | +0.012 | -0.015 |  | -0.2 / -0.2 |  |
| MES | 15 | eod | +0.026 | -0.015 .. +0.068 | +0.0023 | 0.21 / 0.22 / 0.25 | 0.254 |  |  | 10/16 | +0.061 | -0.008 |  | +1.2 / +1.3 |  |
| MES | 60 | h1 | +0.003 | -0.005 .. +0.010 | +0.0030 | 0.48 / 0.5 / 0.5 | 0.497 |  |  | 12/16 | +0.007 | -0.002 |  | +0.7 / +0.7 |  |
| MES | 60 | h2 | +0.001 | -0.010 .. +0.012 | +0.0010 | 0.8 / 0.81 / 0.81 | 0.804 |  |  | 9/16 | +0.004 | -0.002 |  | +0.2 / +0.2 |  |
| MES | 60 | h4 | +0.006 | -0.009 .. +0.021 | +0.0032 | 0.44 / 0.43 / 0.46 | 0.458 |  |  | 9/16 | +0.015 | -0.003 |  | +0.7 / +0.8 | 0.023 |
| MES | 60 | h8 | +0.005 | -0.015 .. +0.025 | +0.0019 | 0.62 / 0.63 / 0.66 | 0.659 |  |  | 8/16 | +0.017 | -0.007 |  | +0.4 / +0.5 |  |
| MES | 60 | h16 * | +0.020 | -0.006 .. +0.045 | +0.0058 | 0.13 / 0.13 / 0.17 | 0.176 | 1 | 1 | 10/16 | +0.026 | +0.013 | False | +1.3 / +1.5 |  |
| MES | 60 | eod | +0.016 | -0.011 .. +0.043 | +0.0046 | 0.24 / 0.23 / 0.28 | 0.279 |  |  | 9/16 | +0.020 | +0.013 |  | +1.1 / +1.2 |  |
| MNQ | 5 | h1 * | +0.004 | +0.001 .. +0.007 | +0.0034 | 0.0069 / 0.0049 / 0.0087 | 0.00781 | 1 | 0.79 | 11/16 | +0.007 | +0.001 | False | +3.1 / +2.7 |  |
| MNQ | 5 | h2 | +0.002 | -0.002 .. +0.005 | +0.0009 | 0.41 / 0.41 / 0.51 | 0.511 |  |  | 10/16 | +0.007 | -0.004 |  | +0.9 / +0.8 |  |
| MNQ | 5 | h4 | -0.003 | -0.007 .. +0.002 | -0.0010 | 0.26 / 0.29 / 0.43 | 0.43 |  |  | 9/16 | +0.003 | -0.008 |  | -1.1 / -1.1 | 0.008 |
| MNQ | 5 | h8 | -0.005 | -0.012 .. +0.002 | -0.0012 | 0.16 / 0.17 / 0.32 | 0.324 |  |  | 12/16 | +0.002 | -0.012 |  | -1.3 / -1.4 |  |
| MNQ | 5 | h16 | -0.001 | -0.011 .. +0.009 | -0.0002 | 0.8 / 0.8 / 0.84 | 0.843 |  |  | 8/16 | +0.005 | -0.007 |  | -0.2 / -0.3 |  |
| MNQ | 5 | eod | -0.016 | -0.070 .. +0.038 | -0.0006 | 0.57 / 0.56 / 0.6 | 0.61 |  |  | 11/16 | +0.022 | -0.054 |  | -0.6 / -0.6 |  |
| MNQ | 15 | h1 * | +0.003 | -0.001 .. +0.007 | +0.0027 | 0.098 / 0.12 / 0.23 | 0.237 | 1 | 1 | 11/16 | +0.008 | -0.001 | False | +1.5 / +1.7 |  |
| MNQ | 15 | h2 | -0.003 | -0.008 .. +0.003 | -0.0015 | 0.29 / 0.3 / 0.51 | 0.52 |  |  | 9/16 | +0.003 | -0.009 |  | -1.0 / -1.1 |  |
| MNQ | 15 | h4 | -0.003 | -0.012 .. +0.005 | -0.0010 | 0.45 / 0.45 / 0.66 | 0.66 |  |  | 10/16 | +0.002 | -0.008 |  | -0.7 / -0.8 | 0.017 |
| MNQ | 15 | h8 | -0.001 | -0.013 .. +0.012 | -0.0002 | 0.88 / 0.88 / 0.92 | 0.932 |  |  | 9/16 | +0.009 | -0.011 |  | -0.1 / -0.1 |  |
| MNQ | 15 | h16 | -0.002 | -0.020 .. +0.015 | -0.0004 | 0.81 / 0.81 / 0.85 | 0.837 |  |  | 10/16 | +0.020 | -0.024 |  | -0.2 / -0.2 |  |
| MNQ | 15 | eod | -0.002 | -0.047 .. +0.042 | -0.0001 | 0.92 / 0.93 / 0.95 | 0.949 |  |  | 7/16 | +0.062 | -0.066 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h1 | -0.007 | -0.015 .. +0.002 | -0.0069 | 0.11 / 0.11 / 0.13 | 0.127 |  |  | 9/16 | -0.004 | -0.010 |  | -1.6 / -1.6 |  |
| MNQ | 60 | h2 * | -0.011 | -0.023 .. +0.000 | -0.0078 | 0.06 / 0.071 / 0.08 | 0.0844 | 1 | 1 | 10/16 | -0.008 | -0.014 | False | -1.8 / -1.9 |  |
| MNQ | 60 | h4 | -0.008 | -0.024 .. +0.008 | -0.0041 | 0.32 / 0.31 / 0.36 | 0.36 |  |  | 10/16 | +0.001 | -0.018 |  | -0.9 / -1.0 | 0.025 |
| MNQ | 60 | h8 | -0.017 | -0.040 .. +0.005 | -0.0062 | 0.14 / 0.13 / 0.16 | 0.163 |  |  | 10/16 | -0.006 | -0.028 |  | -1.4 / -1.5 |  |
| MNQ | 60 | h16 | -0.015 | -0.043 .. +0.014 | -0.0041 | 0.31 / 0.31 / 0.35 | 0.354 |  |  | 7/16 | -0.003 | -0.026 |  | -0.9 / -1.0 |  |
| MNQ | 60 | eod | -0.016 | -0.046 .. +0.014 | -0.0042 | 0.3 / 0.29 / 0.34 | 0.345 |  |  | 10/16 | +0.001 | -0.033 |  | -1.0 / -1.0 |  |
| MYM | 5 | h1 * | +0.004 | -0.000 .. +0.007 | +0.0032 | 0.06 / 0.038 / 0.098 | 0.103 | 1 | 1 | 5/8 | n/a | +0.004 | False | +2.2 / +1.9 |  |
| MYM | 5 | h2 | +0.004 | -0.001 .. +0.009 | +0.0023 | 0.11 / 0.08 / 0.25 | 0.239 |  |  | 5/8 | n/a | +0.004 |  | +1.9 / +1.6 |  |
| MYM | 5 | h4 | +0.005 | -0.001 .. +0.011 | +0.0017 | 0.12 / 0.12 / 0.38 | 0.369 |  |  | 5/8 | n/a | +0.005 |  | +1.6 / +1.5 | 0.011 |
| MYM | 5 | h8 | +0.002 | -0.007 .. +0.012 | +0.0005 | 0.68 / 0.66 / 0.83 | 0.822 |  |  | 3/8 | n/a | +0.002 |  | +0.4 / +0.4 |  |
| MYM | 5 | h16 | +0.006 | -0.007 .. +0.019 | +0.0011 | 0.38 / 0.39 / 0.55 | 0.564 |  |  | 6/8 | n/a | +0.006 |  | +0.8 / +0.9 |  |
| MYM | 5 | eod | +0.021 | -0.042 .. +0.085 | +0.0009 | 0.51 / 0.53 / 0.61 | 0.595 |  |  | 6/8 | n/a | +0.021 |  | +0.6 / +0.7 |  |
| MYM | 15 | h1 * | +0.009 | +0.003 .. +0.015 | +0.0077 | 0.0037 / 0.0036 / 0.016 | 0.0179 | 1 | 0.567 | 7/8 | n/a | +0.009 | False | +3.0 / +2.9 |  |
| MYM | 15 | h2 | +0.006 | -0.003 .. +0.014 | +0.0028 | 0.19 / 0.18 / 0.36 | 0.372 |  |  | 6/8 | n/a | +0.006 |  | +1.4 / +1.3 |  |
| MYM | 15 | h4 | +0.004 | -0.008 .. +0.016 | +0.0012 | 0.52 / 0.5 / 0.7 | 0.675 |  |  | 4/8 | n/a | +0.004 |  | +0.7 / +0.6 | 0.024 |
| MYM | 15 | h8 | +0.004 | -0.012 .. +0.020 | +0.0008 | 0.66 / 0.66 / 0.78 | 0.77 |  |  | 5/8 | n/a | +0.004 |  | +0.4 / +0.4 |  |
| MYM | 15 | h16 | -0.002 | -0.026 .. +0.021 | -0.0004 | 0.85 / 0.85 / 0.89 | 0.887 |  |  | 3/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 15 | eod | +0.014 | -0.050 .. +0.078 | +0.0009 | 0.67 / 0.67 / 0.75 | 0.761 |  |  | 5/8 | n/a | +0.014 |  | +0.4 / +0.4 |  |
| MYM | 60 | h1 * | -0.004 | -0.017 .. +0.009 | -0.0044 | 0.52 / 0.52 / 0.5 | 0.492 | 1 | 1 | 6/8 | n/a | -0.004 | False | -0.7 / -0.6 |  |
| MYM | 60 | h2 | -0.005 | -0.022 .. +0.012 | -0.0036 | 0.55 / 0.55 / 0.56 | 0.547 |  |  | 4/8 | n/a | -0.005 |  | -0.6 / -0.6 |  |
| MYM | 60 | h4 | -0.001 | -0.023 .. +0.021 | -0.0005 | 0.94 / 0.94 / 0.94 | 0.943 |  |  | 3/8 | n/a | -0.001 |  | -0.1 / -0.1 | 0.034 |
| MYM | 60 | h8 | +0.002 | -0.027 .. +0.032 | +0.0009 | 0.87 / 0.87 / 0.89 | 0.878 |  |  | 5/8 | n/a | +0.002 |  | +0.1 / +0.2 |  |
| MYM | 60 | h16 | +0.004 | -0.034 .. +0.043 | +0.0012 | 0.82 / 0.83 / 0.83 | 0.833 |  |  | 3/8 | n/a | +0.004 |  | +0.2 / +0.2 |  |
| MYM | 60 | eod | +0.004 | -0.036 .. +0.044 | +0.0011 | 0.84 / 0.85 / 0.85 | 0.84 |  |  | 4/8 | n/a | +0.004 |  | +0.2 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.010 | +0.007 .. +0.013 | +2.0% | +0.028 | 2.1e-11 | 7.39e-09 | 13/16 |
| MES | 5 | h2 | +0.012 | +0.008 .. +0.017 | +1.7% | +0.029 | 1.7e-07 |  | 14/16 |
| MES | 5 | h4 | +0.017 | +0.009 .. +0.024 | +1.7% | +0.034 | 1e-05 |  | 14/16 |
| MES | 5 | h8 | +0.015 | +0.002 .. +0.029 | +1.1% | +0.032 | 0.021 |  | 12/16 |
| MES | 5 | h16 | +0.009 | -0.011 .. +0.029 | +0.4% | +0.020 | 0.77 |  | 12/16 |
| MES | 5 | eod | -0.097 | -0.336 .. +0.141 | -1.0% | -0.330 | 0.42 |  | 7/16 |
| MES | 15 | h1 | +0.004 | -0.000 .. +0.008 | +0.7% | +0.010 | 0.075 |  | 11/16 |
| MES | 15 | h2 * | +0.008 | +0.001 .. +0.015 | +1.1% | +0.013 | 0.028 | 1 | 12/16 |
| MES | 15 | h4 | +0.008 | -0.006 .. +0.022 | +0.7% | +0.012 | 0.28 |  | 11/16 |
| MES | 15 | h8 | +0.009 | -0.013 .. +0.031 | +0.6% | +0.003 | 0.43 |  | 11/16 |
| MES | 15 | h16 | +0.004 | -0.031 .. +0.039 | +0.2% | -0.023 | 0.82 |  | 11/16 |
| MES | 15 | eod | -0.042 | -0.212 .. +0.128 | -0.8% | -0.123 | 0.63 |  | 7/16 |
| MES | 60 | h1 | -0.002 | -0.010 .. +0.005 | -0.5% | +0.005 | 0.54 |  | 9/16 |
| MES | 60 | h2 | -0.002 | -0.012 .. +0.008 | -0.2% | +0.005 | 0.72 |  | 8/16 |
| MES | 60 | h4 | -0.002 | -0.016 .. +0.012 | -0.2% | +0.005 | 0.79 |  | 11/16 |
| MES | 60 | h8 * | -0.007 | -0.025 .. +0.011 | -0.5% | -0.002 | 0.44 | 1 | 9/16 |
| MES | 60 | h16 | -0.002 | -0.027 .. +0.022 | -0.1% | +0.001 | 0.85 |  | 8/16 |
| MES | 60 | eod | -0.002 | -0.027 .. +0.023 | -0.1% | +0.000 | 0.95 |  | 7/16 |
| MNQ | 5 | h1 * | +0.008 | +0.005 .. +0.012 | +1.6% | +0.031 | 7.2e-06 | 0.00168 | 15/16 |
| MNQ | 5 | h2 | +0.005 | -0.002 .. +0.012 | +0.7% | +0.023 | 0.15 |  | 12/16 |
| MNQ | 5 | h4 | -0.000 | -0.016 .. +0.015 | -0.0% | +0.012 | 1 |  | 4/16 |
| MNQ | 5 | h8 | -0.006 | -0.038 .. +0.026 | -0.4% | -0.004 | 0.69 |  | 4/16 |
| MNQ | 5 | h16 | -0.016 | -0.074 .. +0.042 | -0.7% | -0.037 | 0.59 |  | 5/16 |
| MNQ | 5 | eod | -0.335 | -0.701 .. +0.030 | -2.7% | -0.936 | 0.072 |  | 7/16 |
| MNQ | 15 | h1 * | +0.002 | -0.004 .. +0.008 | +0.3% | +0.006 | 0.6 | 1 | 10/16 |
| MNQ | 15 | h2 | -0.001 | -0.018 .. +0.015 | -0.2% | +0.000 | 0.86 |  | 5/16 |
| MNQ | 15 | h4 | +0.001 | -0.040 .. +0.042 | +0.1% | -0.003 | 0.97 |  | 14/16 |
| MNQ | 15 | h8 | -0.003 | -0.066 .. +0.060 | -0.2% | -0.023 | 0.93 |  | 2/16 |
| MNQ | 15 | h16 | +0.005 | -0.062 .. +0.073 | +0.2% | -0.049 | 0.88 |  | 13/16 |
| MNQ | 15 | eod | -0.068 | -0.364 .. +0.228 | -1.1% | -0.164 | 0.65 |  | 7/16 |
| MNQ | 60 | h1 * | -0.010 | -0.017 .. -0.002 | -1.9% | -0.008 | 0.018 | 1 | 12/16 |
| MNQ | 60 | h2 | -0.008 | -0.018 .. +0.003 | -1.0% | -0.012 | 0.23 |  | 9/16 |
| MNQ | 60 | h4 | -0.006 | -0.023 .. +0.010 | -0.6% | -0.011 | 0.66 |  | 7/16 |
| MNQ | 60 | h8 | -0.012 | -0.033 .. +0.008 | -0.8% | -0.018 | 0.36 |  | 8/16 |
| MNQ | 60 | h16 | -0.016 | -0.043 .. +0.011 | -0.7% | -0.015 | 0.38 |  | 11/16 |
| MNQ | 60 | eod | -0.023 | -0.052 .. +0.005 | -1.0% | -0.022 | 0.24 |  | 11/16 |
| MYM | 5 | h1 * | +0.006 | +0.000 .. +0.012 | +1.1% | +0.019 | 0.045 | 1 | 6/8 |
| MYM | 5 | h2 | +0.002 | -0.011 .. +0.015 | +0.3% | +0.009 | 0.74 |  | 6/8 |
| MYM | 5 | h4 | -0.002 | -0.032 .. +0.029 | -0.1% | -0.001 | 0.92 |  | 1/8 |
| MYM | 5 | h8 | -0.009 | -0.068 .. +0.049 | -0.6% | -0.021 | 0.76 |  | 2/8 |
| MYM | 5 | h16 | -0.022 | -0.102 .. +0.058 | -0.9% | -0.054 | 0.6 |  | 3/8 |
| MYM | 5 | eod | -0.241 | -0.611 .. +0.130 | -2.1% | -0.375 | 0.2 |  | 5/8 |
| MYM | 15 | h1 | -0.001 | -0.010 .. +0.008 | -0.2% | +0.001 | 0.79 |  | 2/8 |
| MYM | 15 | h2 | -0.005 | -0.026 .. +0.017 | -0.6% | -0.010 | 0.68 |  | 2/8 |
| MYM | 15 | h4 | -0.005 | -0.053 .. +0.044 | -0.4% | -0.021 | 0.85 |  | 2/8 |
| MYM | 15 | h8 | -0.021 | -0.096 .. +0.054 | -1.3% | -0.060 | 0.59 |  | 3/8 |
| MYM | 15 | h16 | -0.032 | -0.168 .. +0.104 | -1.3% | -0.103 | 0.65 |  | 2/8 |
| MYM | 15 | eod * | -0.116 | -0.474 .. +0.242 | -1.9% | -0.150 | 0.54 | 1 | 3/8 |
| MYM | 60 | h1 | +0.005 | -0.006 .. +0.016 | +0.9% | +0.010 | 0.6 |  | 4/8 |
| MYM | 60 | h2 | -0.001 | -0.016 .. +0.013 | -0.2% | +0.008 | 0.9 |  | 4/8 |
| MYM | 60 | h4 * | -0.011 | -0.032 .. +0.010 | -1.0% | -0.001 | 0.3 | 1 | 6/8 |
| MYM | 60 | h8 | +0.002 | -0.028 .. +0.031 | +0.1% | -0.000 | 0.94 |  | 4/8 |
| MYM | 60 | h16 | +0.008 | -0.027 .. +0.043 | +0.4% | +0.008 | 0.88 |  | 3/8 |
| MYM | 60 | eod | +0.003 | -0.034 .. +0.040 | +0.1% | +0.002 | 0.99 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.11 pts | -0.08 .. +0.29 | 0.55 |
| MES | 15 | +0.43 pts | +0.18 .. +0.67 | 0.0023 |
| MES | 60 | +0.14 pts | -0.32 .. +0.60 | 0.56 |
| MNQ | 5 | +0.17 pts | +0.01 .. +0.33 | 0.067 |
| MNQ | 15 | +0.07 pts | -0.16 .. +0.29 | 0.61 |
| MNQ | 60 | -0.17 pts | -0.65 .. +0.31 | 0.6 |
| MYM | 5 | +0.14 pts | -0.10 .. +0.37 | 0.3 |
| MYM | 15 | +0.54 pts | +0.24 .. +0.83 | 0.0011 |
| MYM | 60 | -0.22 pts | -0.80 .. +0.37 | 0.5 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 326099 | +0.016 | 0.253 | +0.18 | -3.32 | -3.35 | -3.30 | -3.46 |
| MES | 5 | h2 | event | with signal | 326099 | +0.022 | 0.253 | +0.27 | -3.23 | -3.28 | -3.20 | -3.44 |
| MES | 5 | h4 | event | with signal | 326099 | +0.016 | 0.253 | +0.18 | -3.32 | -3.37 | -3.29 | -3.53 |
| MES | 5 | h8 | event | against signal | 326099 | -0.010 | 0.253 | -0.11 | -3.61 | -3.59 | -3.62 | -3.42 |
| MES | 5 | h16 | event | against signal | 326099 | -0.012 | 0.253 | -0.10 | -3.60 | -3.63 | -3.58 | -3.39 |
| MES | 5 | eod | event | with signal | 326099 | +0.010 | 0.253 | +0.14 | -3.36 | -3.59 | -3.23 | -3.38 |
| MES | 15 | h1 | event | with signal | 134380 | +0.016 | 0.170 | +0.28 | -3.22 | -3.33 | -3.13 | -3.38 |
| MES | 15 | h2 | event | with signal | 134380 | +0.011 | 0.170 | +0.17 | -3.33 | -3.41 | -3.27 | -3.51 |
| MES | 15 | h4 | event | with signal | 134380 | +0.008 | 0.170 | +0.09 | -3.41 | -3.43 | -3.39 | -3.58 |
| MES | 15 | h8 | event | with signal | 134380 | +0.008 | 0.170 | +0.12 | -3.38 | -3.45 | -3.32 | -3.56 |
| MES | 15 | h16 | event | against signal | 134380 | -0.006 | 0.170 | -0.10 | -3.60 | -3.58 | -3.61 | -3.41 |
| MES | 15 | eod | event | with signal | 134380 | +0.007 | 0.170 | -0.03 | -3.53 | -3.38 | -3.64 | -3.24 |
| MES | 60 | h1 | event | with signal | 35509 | +0.002 | 0.091 | +0.06 | -3.44 | -3.43 | -3.46 | -3.43 |
| MES | 60 | h2 | event | with signal | 35509 | +0.001 | 0.091 | +0.05 | -3.45 | -3.50 | -3.40 | -3.48 |
| MES | 60 | h4 | event | with signal | 35509 | +0.006 | 0.091 | +0.13 | -3.37 | -3.26 | -3.48 | -3.43 |
| MES | 60 | h8 | event | with signal | 35509 | +0.004 | 0.091 | -0.34 | -3.84 | -3.52 | -4.13 | -3.88 |
| MES | 60 | h16 | event | with signal | 35509 | +0.007 | 0.091 | -0.44 | -3.94 | -3.62 | -4.23 | -3.56 |
| MES | 60 | eod | event | with signal | 35509 | +0.006 | 0.091 | -0.44 | -3.94 | -3.57 | -4.29 | -3.67 |
| MNQ | 5 | h1 | event | with signal | 417071 | +0.008 | 0.120 | +0.11 | -1.89 | -1.93 | -1.86 | -1.97 |
| MNQ | 5 | h2 | event | with signal | 417071 | +0.009 | 0.120 | +0.12 | -1.88 | -1.91 | -1.85 | -2.00 |
| MNQ | 5 | h4 | event | against signal | 417071 | -0.002 | 0.120 | +0.00 | -2.00 | -2.03 | -1.97 | -1.92 |
| MNQ | 5 | h8 | event | against signal | 417071 | +0.007 | 0.120 | +0.07 | -1.93 | -2.01 | -1.86 | -1.95 |
| MNQ | 5 | h16 | event | against signal | 417071 | +0.006 | 0.120 | +0.11 | -1.89 | -1.98 | -1.81 | -1.96 |
| MNQ | 5 | eod | event | against signal | 417071 | +0.031 | 0.120 | +0.10 | -1.90 | -2.01 | -1.82 | -2.02 |
| MNQ | 15 | h1 | event | with signal | 147240 | +0.006 | 0.073 | +0.09 | -1.91 | -1.92 | -1.90 | -1.99 |
| MNQ | 15 | h2 | event | against signal | 147240 | +0.002 | 0.073 | +0.11 | -1.89 | -2.03 | -1.75 | -1.86 |
| MNQ | 15 | h4 | event | against signal | 147240 | +0.005 | 0.073 | +0.11 | -1.89 | -1.97 | -1.82 | -1.92 |
| MNQ | 15 | h8 | event | against signal | 147240 | +0.008 | 0.073 | +0.26 | -1.74 | -1.94 | -1.55 | -1.92 |
| MNQ | 15 | h16 | event | against signal | 147240 | +0.008 | 0.073 | +0.35 | -1.65 | -1.99 | -1.31 | -1.74 |
| MNQ | 15 | eod | event | against signal | 147240 | +0.033 | 0.073 | +0.75 | -1.25 | -2.13 | -0.36 | -1.76 |
| MNQ | 60 | h1 | event | against signal | 35885 | +0.009 | 0.037 | +0.42 | -1.58 | -1.84 | -1.30 | -1.67 |
| MNQ | 60 | h2 | event | against signal | 35885 | +0.013 | 0.037 | +0.59 | -1.41 | -1.78 | -1.03 | -1.44 |
| MNQ | 60 | h4 | event | against signal | 35885 | +0.011 | 0.037 | +0.75 | -1.25 | -1.98 | -0.50 | -1.27 |
| MNQ | 60 | h8 | event | against signal | 35885 | +0.023 | 0.037 | +1.77 | -0.23 | -1.51 | +1.08 | -0.33 |
| MNQ | 60 | h16 | event | against signal | 35885 | +0.031 | 0.037 | +2.26 | +0.26 | -1.37 | +1.95 | -0.27 |
| MNQ | 60 | eod | event | against signal | 35885 | +0.031 | 0.037 | +2.56 | +0.56 | -1.52 | +2.71 | +0.12 |
| MYM | 5 | h1 | event | with signal | 238479 | +0.010 | 0.170 | +0.12 | -1.88 | +nan | -1.88 | -1.97 |
| MYM | 5 | h2 | event | with signal | 238479 | +0.013 | 0.170 | +0.17 | -1.83 | +nan | -1.83 | -1.93 |
| MYM | 5 | h4 | event | with signal | 238479 | +0.014 | 0.170 | +0.14 | -1.86 | +nan | -1.86 | -1.97 |
| MYM | 5 | h8 | event | with signal | 238479 | +0.012 | 0.170 | +0.14 | -1.86 | +nan | -1.86 | -1.97 |
| MYM | 5 | h16 | event | with signal | 238479 | +0.020 | 0.170 | +0.19 | -1.81 | +nan | -1.81 | -1.98 |
| MYM | 5 | eod | event | with signal | 238479 | +0.042 | 0.170 | +0.26 | -1.74 | +nan | -1.74 | -2.05 |
| MYM | 15 | h1 | event | with signal | 76620 | +0.014 | 0.096 | +0.25 | -1.75 | +nan | -1.75 | -1.86 |
| MYM | 15 | h2 | event | with signal | 76620 | +0.010 | 0.096 | +0.19 | -1.81 | +nan | -1.81 | -1.91 |
| MYM | 15 | h4 | event | with signal | 76620 | +0.006 | 0.096 | +0.08 | -1.92 | +nan | -1.92 | -1.97 |
| MYM | 15 | h8 | event | with signal | 76620 | +0.006 | 0.096 | +0.19 | -1.81 | +nan | -1.81 | -1.88 |
| MYM | 15 | h16 | event | against signal | 76620 | +0.004 | 0.096 | -0.18 | -2.18 | +nan | -2.18 | -2.19 |
| MYM | 15 | eod | event | with signal | 76620 | +0.012 | 0.096 | +0.20 | -1.80 | +nan | -1.80 | -1.87 |
| MYM | 60 | h1 | event | against signal | 17906 | +0.005 | 0.047 | +0.06 | -1.94 | +nan | -1.94 | -1.96 |
| MYM | 60 | h2 | event | against signal | 17906 | +0.001 | 0.047 | -0.09 | -2.09 | +nan | -2.09 | -1.90 |
| MYM | 60 | h4 | event | against signal | 17906 | -0.004 | 0.047 | -0.10 | -2.10 | +nan | -2.10 | -1.84 |
| MYM | 60 | h8 | event | with signal | 17906 | +0.007 | 0.047 | -0.15 | -2.15 | +nan | -2.15 | -2.46 |
| MYM | 60 | h16 | event | with signal | 17906 | -0.006 | 0.047 | -0.78 | -2.78 | +nan | -2.78 | -2.49 |
| MYM | 60 | eod | event | with signal | 17906 | -0.006 | 0.047 | -0.94 | -2.94 | +nan | -2.94 | -2.66 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.537 | +0.597 | +0.652 | +0.702 | +0.744 | +0.000 | +0.038 | +0.043 | +0.038 | +0.032 | +0.046 |
| MES | 15 | +0.534 | +0.564 | +0.610 | +0.661 | +0.706 | +0.000 | +0.031 | +0.026 | +0.026 | +0.028 | +0.027 |
| MES | 60 | +0.862 | +0.717 | +0.664 | +0.661 | +0.683 | +0.000 | +0.008 | +0.012 | +0.024 | +0.053 | +0.071 |
| MNQ | 5 | +0.523 | +0.574 | +0.626 | +0.676 | +0.723 | +0.000 | +0.022 | +0.024 | +0.017 | +0.010 | +0.007 |
| MNQ | 15 | +0.539 | +0.563 | +0.605 | +0.655 | +0.699 | +0.000 | +0.015 | +0.007 | +0.005 | +0.004 | +0.010 |
| MNQ | 60 | +0.889 | +0.742 | +0.676 | +0.676 | +0.700 | +0.000 | -0.006 | -0.006 | +0.000 | +0.011 | +0.023 |
| MYM | 5 | +0.490 | +0.544 | +0.595 | +0.640 | +0.683 | +0.000 | +0.023 | +0.025 | +0.027 | +0.023 | +0.032 |
| MYM | 15 | +0.518 | +0.544 | +0.589 | +0.634 | +0.680 | +0.000 | +0.018 | +0.015 | +0.010 | +0.009 | -0.006 |
| MYM | 60 | +0.889 | +0.740 | +0.679 | +0.680 | +0.702 | +0.000 | -0.005 | -0.002 | +0.005 | +0.024 | +0.034 |

## Calibration

- MES 5-min: 1036271 bars, 326099 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 134380 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 35509 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 417071 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 147240 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 35885 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 238479 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 76620 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 17906 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32709 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
