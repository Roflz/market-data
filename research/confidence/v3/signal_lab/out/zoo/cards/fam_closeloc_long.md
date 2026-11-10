# Impact card: fam_closeloc_long

bullish closeloc patterns only (long side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: POSSIBLE direction effect +0.006 average bars (~$0.10 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.227, replicated in the other half=False, 14 of 16 years); best leg (event, with signal) grosses $+0.21 and nets $-3.29 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.010 R20, CONFIRMED, q=5.7e-09, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.10 at recent bar sizes, 90% range up to $0.29); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (15 min), p=0.03; we would catch an effect of 0.022 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.012 R20, CONFIRMED, q=0.000819, 11 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.25 at recent bar sizes, 90% range up to $0.96); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.026 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.043 R20 or more 80% of the time).
- MES 60-min size: the market moves 3% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.023 R20, possible, q=0.151, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.63 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.062 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=0.38; we would catch an effect of 0.016 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.013 R20, CONFIRMED, q=2.49e-08, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.09 at recent bar sizes, 90% range up to $0.56); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (15 min), p=0.32; we would catch an effect of 0.031 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.012 R20, CONFIRMED, q=0.0168, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.29 at recent bar sizes, 90% range up to $1.52); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.036 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.52).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.34 at recent bar sizes, 90% range up to $5.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.030 R20 or more 80% of the time).
- MYM 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.010 R20, CONFIRMED, q=0.0279, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.040 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.055).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.07 at recent bar sizes, 90% range up to $1.38); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.066 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.17).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.51 at recent bar sizes, 90% range up to $3.33); about 3.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.006 | +0.003 .. +0.010 | +0.0048 | 0.00052 / 0.00049 / 4.4e-05 | 0.000521 | 0.227 | 0.166 | 14/16 | +0.007 | +0.005 | False | +3.7 / +3.5 |  |
| MES | 5 | h2 | +0.005 | -0.001 .. +0.011 | +0.0027 | 0.08 / 0.076 / 0.03 | 0.0292 |  |  | 11/16 | +0.008 | +0.002 |  | +2.1 / +1.7 |  |
| MES | 5 | h4 | -0.001 | -0.009 .. +0.008 | -0.0002 | 0.9 / 0.9 / 0.83 | 0.823 |  |  | 11/16 | -0.004 | +0.002 |  | -0.2 / -0.1 | 0.012 |
| MES | 5 | h8 | -0.004 | -0.019 .. +0.010 | -0.0011 | 0.56 / 0.58 / 0.36 | 0.357 |  |  | 8/16 | -0.002 | -0.007 |  | -0.9 / -0.6 |  |
| MES | 5 | h16 | +0.003 | -0.025 .. +0.031 | +0.0005 | 0.83 / 0.84 / 0.7 | 0.697 |  |  | 6/16 | +0.010 | -0.004 |  | +0.4 / +0.2 |  |
| MES | 5 | eod | +0.060 | -0.329 .. +0.449 | +0.0021 | 0.76 / 0.77 / 0.22 | 0.21 |  |  | 7/16 | -0.003 | +0.123 |  | +1.8 / +0.3 |  |
| MES | 15 | h1 * | +0.009 | +0.003 .. +0.015 | +0.0068 | 0.0047 / 0.0051 / 0.00066 | 0.00026 | 0.739 | 0.706 | 13/16 | +0.013 | +0.005 | False | +3.0 / +2.8 |  |
| MES | 15 | h2 | +0.001 | -0.009 .. +0.011 | +0.0004 | 0.88 / 0.88 / 0.84 | 0.834 |  |  | 8/16 | +0.003 | -0.001 |  | +0.2 / +0.2 |  |
| MES | 15 | h4 | +0.000 | -0.016 .. +0.017 | +0.0001 | 0.96 / 0.96 / 0.95 | 0.945 |  |  | 9/16 | +0.000 | +0.001 |  | +0.1 / +0.0 | 0.022 |
| MES | 15 | h8 | +0.002 | -0.029 .. +0.033 | +0.0005 | 0.9 / 0.89 / 0.82 | 0.822 |  |  | 10/16 | +0.000 | +0.004 |  | +0.2 / +0.1 |  |
| MES | 15 | h16 | +0.000 | -0.054 .. +0.055 | +0.0001 | 0.99 / 0.99 / 0.98 | 0.979 |  |  | 6/16 | +0.008 | -0.007 |  | +0.0 / +0.0 |  |
| MES | 15 | eod | +0.011 | -0.209 .. +0.232 | +0.0007 | 0.92 / 0.92 / 0.76 | 0.759 |  |  | 5/16 | -0.000 | +0.022 |  | +0.4 / +0.1 |  |
| MES | 60 | h1 | +0.001 | -0.012 .. +0.014 | +0.0008 | 0.86 / 0.86 / 0.83 | 0.843 |  |  | 8/16 | +0.006 | -0.004 |  | +0.2 / +0.2 |  |
| MES | 60 | h2 | -0.003 | -0.023 .. +0.018 | -0.0015 | 0.78 / 0.78 / 0.72 | 0.706 |  |  | 6/16 | +0.003 | -0.009 |  | -0.3 / -0.3 |  |
| MES | 60 | h4 | +0.000 | -0.032 .. +0.033 | +0.0001 | 0.99 / 0.99 / 0.99 | 0.99 |  |  | 10/16 | +0.012 | -0.012 |  | +0.0 / +0.0 | 0.043 |
| MES | 60 | h8 | +0.002 | -0.051 .. +0.054 | +0.0005 | 0.95 / 0.95 / 0.92 | 0.92 |  |  | 10/16 | +0.026 | -0.023 |  | +0.1 / +0.1 |  |
| MES | 60 | h16 | -0.011 | -0.095 .. +0.073 | -0.0023 | 0.8 / 0.8 / 0.61 | 0.604 |  |  | 10/16 | +0.017 | -0.039 |  | -0.5 / -0.3 |  |
| MES | 60 | eod * | -0.026 | -0.117 .. +0.066 | -0.0050 | 0.58 / 0.6 / 0.26 | 0.269 | 1 | 1 | 10/16 | -0.001 | -0.050 | False | -1.1 / -0.5 |  |
| MNQ | 5 | h1 * | +0.003 | -0.000 .. +0.007 | +0.0024 | 0.064 / 0.06 / 0.046 | 0.049 | 1 | 1 | 11/16 | +0.006 | +0.001 | False | +2.1 / +1.9 |  |
| MNQ | 5 | h2 | +0.001 | -0.005 .. +0.006 | +0.0003 | 0.81 / 0.82 / 0.84 | 0.852 |  |  | 8/16 | +0.005 | -0.003 |  | +0.3 / +0.2 |  |
| MNQ | 5 | h4 | -0.005 | -0.014 .. +0.004 | -0.0015 | 0.25 / 0.27 / 0.21 | 0.215 |  |  | 12/16 | -0.006 | -0.005 |  | -1.5 / -1.2 | 0.016 |
| MNQ | 5 | h8 | -0.008 | -0.023 .. +0.008 | -0.0014 | 0.35 / 0.37 / 0.23 | 0.233 |  |  | 12/16 | -0.011 | -0.004 |  | -1.5 / -0.9 |  |
| MNQ | 5 | h16 | +0.002 | -0.029 .. +0.032 | +0.0002 | 0.91 / 0.91 / 0.85 | 0.855 |  |  | 7/16 | -0.009 | +0.012 |  | +0.2 / +0.1 |  |
| MNQ | 5 | eod | +0.040 | -0.415 .. +0.496 | +0.0011 | 0.86 / 0.87 / 0.44 | 0.439 |  |  | 7/16 | -0.046 | +0.126 |  | +1.0 / +0.2 |  |
| MNQ | 15 | h1 * | +0.006 | +0.000 .. +0.012 | +0.0037 | 0.04 / 0.053 / 0.066 | 0.068 | 1 | 0.999 | 12/16 | +0.012 | +0.000 | False | +2.0 / +2.1 |  |
| MNQ | 15 | h2 | -0.002 | -0.012 .. +0.008 | -0.0008 | 0.66 / 0.67 / 0.69 | 0.694 |  |  | 11/16 | -0.001 | -0.004 |  | -0.5 / -0.4 |  |
| MNQ | 15 | h4 | -0.004 | -0.021 .. +0.013 | -0.0009 | 0.63 / 0.63 / 0.66 | 0.663 |  |  | 8/16 | -0.010 | +0.001 |  | -0.7 / -0.5 | 0.031 |
| MNQ | 15 | h8 | -0.007 | -0.037 .. +0.023 | -0.0011 | 0.65 / 0.65 / 0.57 | 0.571 |  |  | 8/16 | -0.006 | -0.008 |  | -0.7 / -0.5 |  |
| MNQ | 15 | h16 | +0.000 | -0.055 .. +0.055 | +0.0000 | 1 / 1 / 1 | 0.996 |  |  | 6/16 | +0.008 | -0.008 |  | +0.0 / +0.0 |  |
| MNQ | 15 | eod | -0.007 | -0.254 .. +0.239 | -0.0003 | 0.95 / 0.95 / 0.87 | 0.873 |  |  | 13/16 | -0.060 | +0.045 |  | -0.2 / -0.1 |  |
| MNQ | 60 | h1 | -0.004 | -0.017 .. +0.010 | -0.0025 | 0.61 / 0.6 / 0.54 | 0.533 |  |  | 9/16 | +0.002 | -0.009 |  | -0.5 / -0.5 |  |
| MNQ | 60 | h2 | -0.005 | -0.025 .. +0.015 | -0.0024 | 0.63 / 0.64 / 0.56 | 0.564 |  |  | 9/16 | -0.001 | -0.009 |  | -0.5 / -0.5 |  |
| MNQ | 60 | h4 | -0.005 | -0.037 .. +0.027 | -0.0017 | 0.77 / 0.77 / 0.7 | 0.696 |  |  | 8/16 | +0.010 | -0.020 |  | -0.4 / -0.3 | 0.046 |
| MNQ | 60 | h8 | -0.015 | -0.070 .. +0.041 | -0.0036 | 0.61 / 0.61 / 0.4 | 0.406 |  |  | 9/16 | -0.010 | -0.019 |  | -0.8 / -0.5 |  |
| MNQ | 60 | h16 | -0.029 | -0.119 .. +0.061 | -0.0055 | 0.53 / 0.54 / 0.21 | 0.203 |  |  | 10/16 | -0.023 | -0.034 |  | -1.2 / -0.6 |  |
| MNQ | 60 | eod * | -0.036 | -0.133 .. +0.062 | -0.0065 | 0.47 / 0.49 / 0.14 | 0.134 | 1 | 1 | 10/16 | -0.024 | -0.047 | False | -1.5 / -0.7 |  |
| MYM | 5 | h1 * | +0.003 | -0.002 .. +0.008 | +0.0023 | 0.18 / 0.16 / 0.21 | 0.212 | 1 | 1 | 6/8 | n/a | +0.003 | False | +1.5 / +1.3 |  |
| MYM | 5 | h2 | +0.003 | -0.006 .. +0.012 | +0.0013 | 0.5 / 0.46 / 0.52 | 0.542 |  |  | 3/8 | n/a | +0.003 |  | +0.9 / +0.7 |  |
| MYM | 5 | h4 | +0.005 | -0.009 .. +0.020 | +0.0014 | 0.47 / 0.42 / 0.42 | 0.42 |  |  | 4/8 | n/a | +0.005 |  | +1.2 / +0.7 | 0.030 |
| MYM | 5 | h8 | +0.003 | -0.022 .. +0.027 | +0.0005 | 0.82 / 0.82 / 0.8 | 0.792 |  |  | 3/8 | n/a | +0.003 |  | +0.4 / +0.2 |  |
| MYM | 5 | h16 | +0.009 | -0.035 .. +0.053 | +0.0013 | 0.69 / 0.69 / 0.46 | 0.466 |  |  | 4/8 | n/a | +0.009 |  | +0.9 / +0.4 |  |
| MYM | 5 | eod | +0.092 | -0.619 .. +0.803 | +0.0030 | 0.8 / 0.8 / 0.11 | 0.114 |  |  | 5/8 | n/a | +0.092 |  | +1.7 / +0.3 |  |
| MYM | 15 | h1 * | +0.003 | -0.006 .. +0.012 | +0.0020 | 0.49 / 0.48 / 0.48 | 0.488 | 1 | 1 | 4/8 | n/a | +0.003 | False | +0.7 / +0.7 |  |
| MYM | 15 | h2 | +0.001 | -0.013 .. +0.016 | +0.0005 | 0.86 / 0.85 / 0.87 | 0.872 |  |  | 3/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 15 | h4 | +0.003 | -0.021 .. +0.027 | +0.0007 | 0.79 / 0.79 / 0.8 | 0.82 |  |  | 5/8 | n/a | +0.003 |  | +0.4 / +0.3 | 0.040 |
| MYM | 15 | h8 | +0.005 | -0.039 .. +0.050 | +0.0009 | 0.81 / 0.81 / 0.76 | 0.751 |  |  | 4/8 | n/a | +0.005 |  | +0.4 / +0.2 |  |
| MYM | 15 | h16 | +0.009 | -0.077 .. +0.094 | +0.0010 | 0.84 / 0.84 / 0.71 | 0.718 |  |  | 2/8 | n/a | +0.009 |  | +0.5 / +0.2 |  |
| MYM | 15 | eod | +0.053 | -0.312 .. +0.418 | +0.0026 | 0.78 / 0.77 / 0.37 | 0.37 |  |  | 3/8 | n/a | +0.053 |  | +1.1 / +0.3 |  |
| MYM | 60 | h1 * | -0.012 | -0.031 .. +0.007 | -0.0085 | 0.22 / 0.22 / 0.15 | 0.148 | 1 | 1 | 6/8 | n/a | -0.012 | False | -1.3 / -1.2 |  |
| MYM | 60 | h2 | -0.017 | -0.046 .. +0.012 | -0.0084 | 0.26 / 0.27 / 0.15 | 0.152 |  |  | 5/8 | n/a | -0.017 |  | -1.3 / -1.1 |  |
| MYM | 60 | h4 | -0.006 | -0.052 .. +0.040 | -0.0020 | 0.81 / 0.81 / 0.73 | 0.732 |  |  | 3/8 | n/a | -0.006 |  | -0.3 / -0.2 | 0.066 |
| MYM | 60 | h8 | +0.006 | -0.073 .. +0.086 | +0.0017 | 0.87 / 0.87 / 0.79 | 0.787 |  |  | 4/8 | n/a | +0.006 |  | +0.3 / +0.2 |  |
| MYM | 60 | h16 | -0.008 | -0.133 .. +0.118 | -0.0015 | 0.9 / 0.91 / 0.81 | 0.809 |  |  | 3/8 | n/a | -0.008 |  | -0.2 / -0.1 |  |
| MYM | 60 | eod | -0.021 | -0.156 .. +0.113 | -0.0040 | 0.76 / 0.77 / 0.51 | 0.504 |  |  | 4/8 | n/a | -0.021 |  | -0.6 / -0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.010 | +0.007 .. +0.013 | +2.0% | +0.025 | 1.6e-11 | 5.7e-09 | 13/16 |
| MES | 5 | h2 | +0.010 | +0.006 .. +0.015 | +1.5% | +0.024 | 2.7e-06 |  | 11/16 |
| MES | 5 | h4 | +0.009 | +0.002 .. +0.016 | +0.9% | +0.022 | 0.0078 |  | 10/16 |
| MES | 5 | h8 | +0.010 | -0.001 .. +0.021 | +0.7% | +0.019 | 0.074 |  | 11/16 |
| MES | 5 | h16 | +0.008 | -0.008 .. +0.024 | +0.4% | +0.010 | 0.32 |  | 10/16 |
| MES | 5 | eod | -0.061 | -0.206 .. +0.083 | -0.6% | -0.155 | 0.41 |  | 6/16 |
| MES | 15 | h1 * | +0.012 | +0.007 .. +0.017 | +2.3% | +0.023 | 3.4e-06 | 0.000819 | 11/16 |
| MES | 15 | h2 | +0.017 | +0.009 .. +0.024 | +2.3% | +0.030 | 1.7e-05 |  | 14/16 |
| MES | 15 | h4 | +0.018 | +0.005 .. +0.032 | +1.7% | +0.031 | 0.0062 |  | 13/16 |
| MES | 15 | h8 | +0.017 | -0.003 .. +0.037 | +1.1% | +0.022 | 0.087 |  | 13/16 |
| MES | 15 | h16 | +0.015 | -0.016 .. +0.046 | +0.7% | +0.008 | 0.33 |  | 12/16 |
| MES | 15 | eod | -0.008 | -0.136 .. +0.121 | -0.1% | -0.024 | 0.91 |  | 5/16 |
| MES | 60 | h1 | +0.014 | +0.004 .. +0.024 | +2.8% | +0.033 | 0.0061 |  | 10/16 |
| MES | 60 | h2 * | +0.023 | +0.010 .. +0.036 | +3.1% | +0.042 | 0.00087 | 0.151 | 15/16 |
| MES | 60 | h4 | +0.027 | +0.009 .. +0.045 | +2.6% | +0.052 | 0.007 |  | 12/16 |
| MES | 60 | h8 | +0.021 | -0.003 .. +0.045 | +1.4% | +0.050 | 0.12 |  | 10/16 |
| MES | 60 | h16 | +0.013 | -0.016 .. +0.043 | +0.7% | +0.040 | 0.37 |  | 11/16 |
| MES | 60 | eod | +0.017 | -0.015 .. +0.049 | +0.8% | +0.040 | 0.3 |  | 11/16 |
| MNQ | 5 | h1 * | +0.013 | +0.009 .. +0.017 | +2.4% | +0.030 | 7.6e-11 | 2.49e-08 | 15/16 |
| MNQ | 5 | h2 | +0.013 | +0.006 .. +0.020 | +1.6% | +0.029 | 0.0003 |  | 11/16 |
| MNQ | 5 | h4 | +0.009 | -0.004 .. +0.023 | +0.9% | +0.026 | 0.16 |  | 11/16 |
| MNQ | 5 | h8 | +0.011 | -0.015 .. +0.038 | +0.7% | +0.026 | 0.4 |  | 12/16 |
| MNQ | 5 | h16 | +0.013 | -0.034 .. +0.061 | +0.6% | +0.014 | 0.58 |  | 12/16 |
| MNQ | 5 | eod | -0.049 | -0.296 .. +0.199 | -0.4% | -0.248 | 0.7 |  | 5/16 |
| MNQ | 15 | h1 * | +0.012 | +0.006 .. +0.018 | +2.2% | +0.022 | 8.1e-05 | 0.0168 | 14/16 |
| MNQ | 15 | h2 | +0.010 | -0.004 .. +0.023 | +1.3% | +0.021 | 0.15 |  | 13/16 |
| MNQ | 15 | h4 | +0.013 | -0.018 .. +0.044 | +1.1% | +0.019 | 0.42 |  | 13/16 |
| MNQ | 15 | h8 | +0.012 | -0.036 .. +0.060 | +0.7% | +0.009 | 0.63 |  | 13/16 |
| MNQ | 15 | h16 | +0.020 | -0.031 .. +0.072 | +0.8% | -0.004 | 0.44 |  | 13/16 |
| MNQ | 15 | eod | -0.002 | -0.219 .. +0.216 | -0.0% | -0.028 | 0.99 |  | 5/16 |
| MNQ | 60 | h1 | +0.002 | -0.008 .. +0.012 | +0.3% | +0.019 | 0.71 |  | 8/16 |
| MNQ | 60 | h2 * | +0.013 | -0.002 .. +0.027 | +1.6% | +0.024 | 0.086 | 1 | 12/16 |
| MNQ | 60 | h4 | +0.001 | -0.018 .. +0.020 | +0.1% | +0.026 | 0.94 |  | 8/16 |
| MNQ | 60 | h8 | -0.000 | -0.025 .. +0.024 | -0.0% | +0.024 | 0.98 |  | 9/16 |
| MNQ | 60 | h16 | -0.002 | -0.036 .. +0.031 | -0.1% | +0.031 | 0.89 |  | 9/16 |
| MNQ | 60 | eod | -0.004 | -0.038 .. +0.031 | -0.2% | +0.027 | 0.85 |  | 9/16 |
| MYM | 5 | h1 * | +0.010 | +0.005 .. +0.016 | +1.9% | +0.024 | 0.00014 | 0.0279 | 7/8 |
| MYM | 5 | h2 | +0.008 | -0.002 .. +0.018 | +1.1% | +0.020 | 0.12 |  | 7/8 |
| MYM | 5 | h4 | +0.006 | -0.017 .. +0.029 | +0.6% | +0.014 | 0.58 |  | 6/8 |
| MYM | 5 | h8 | -0.002 | -0.045 .. +0.041 | -0.2% | -0.003 | 0.91 |  | 2/8 |
| MYM | 5 | h16 | -0.004 | -0.062 .. +0.054 | -0.2% | -0.025 | 0.9 |  | 3/8 |
| MYM | 5 | eod | -0.092 | -0.355 .. +0.171 | -0.8% | -0.136 | 0.49 |  | 2/8 |
| MYM | 15 | h1 * | +0.012 | +0.004 .. +0.020 | +2.3% | +0.021 | 0.0092 | 1 | 6/8 |
| MYM | 15 | h2 | +0.010 | -0.008 .. +0.028 | +1.3% | +0.017 | 0.48 |  | 6/8 |
| MYM | 15 | h4 | +0.011 | -0.026 .. +0.048 | +1.0% | +0.011 | 0.64 |  | 6/8 |
| MYM | 15 | h8 | -0.001 | -0.057 .. +0.056 | -0.0% | -0.016 | 0.98 |  | 2/8 |
| MYM | 15 | h16 | -0.010 | -0.112 .. +0.093 | -0.4% | -0.047 | 0.85 |  | 2/8 |
| MYM | 15 | eod | -0.088 | -0.351 .. +0.175 | -1.5% | -0.097 | 0.52 |  | 3/8 |
| MYM | 60 | h1 | +0.018 | +0.004 .. +0.032 | +3.4% | +0.035 | 0.061 |  | 7/8 |
| MYM | 60 | h2 * | +0.022 | +0.003 .. +0.041 | +2.9% | +0.049 | 0.028 | 1 | 6/8 |
| MYM | 60 | h4 | +0.016 | -0.010 .. +0.042 | +1.5% | +0.047 | 0.29 |  | 5/8 |
| MYM | 60 | h8 | +0.026 | -0.010 .. +0.063 | +1.7% | +0.057 | 0.22 |  | 6/8 |
| MYM | 60 | h16 | +0.034 | -0.009 .. +0.077 | +1.6% | +0.068 | 0.23 |  | 6/8 |
| MYM | 60 | eod | +0.028 | -0.019 .. +0.075 | +1.3% | +0.059 | 0.31 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.34 pts | +0.05 .. +0.64 | 0.024 |
| MES | 15 | +0.62 pts | +0.12 .. +1.12 | 0.015 |
| MES | 60 | +0.29 pts | -0.66 .. +1.25 | 0.55 |
| MNQ | 5 | +0.25 pts | -0.01 .. +0.51 | 0.067 |
| MNQ | 15 | +0.17 pts | -0.24 .. +0.59 | 0.44 |
| MNQ | 60 | -0.24 pts | -1.14 .. +0.66 | 0.59 |
| MYM | 5 | +0.06 pts | -0.33 .. +0.46 | 0.89 |
| MYM | 15 | +0.51 pts | -0.10 .. +1.12 | 0.1 |
| MYM | 60 | -0.18 pts | -1.48 .. +1.12 | 0.8 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 199795 | +0.018 | 0.287 | +0.21 | -3.29 | -3.36 | -3.24 | -3.42 |
| MES | 5 | h2 | event | with signal | 199795 | +0.024 | 0.287 | +0.27 | -3.23 | -3.29 | -3.18 | -3.43 |
| MES | 5 | h4 | event | against signal | 199795 | -0.024 | 0.287 | -0.28 | -3.78 | -3.66 | -3.87 | -3.55 |
| MES | 5 | h8 | event | against signal | 199795 | -0.030 | 0.287 | -0.30 | -3.80 | -3.74 | -3.85 | -3.52 |
| MES | 5 | h16 | event | with signal | 199795 | +0.062 | 0.287 | +0.59 | -2.91 | -3.00 | -2.84 | -3.36 |
| MES | 5 | eod | event | with signal | 199795 | +0.550 | 0.287 | +5.15 | +1.65 | -0.08 | +3.01 | +0.70 |
| MES | 15 | h1 | event | with signal | 68984 | +0.021 | 0.175 | +0.38 | -3.12 | -3.24 | -3.01 | -3.33 |
| MES | 15 | h2 | event | with signal | 68984 | +0.019 | 0.175 | +0.36 | -3.14 | -3.31 | -3.00 | -3.42 |
| MES | 15 | h4 | event | with signal | 68984 | +0.028 | 0.175 | +0.50 | -3.00 | -3.20 | -2.82 | -3.36 |
| MES | 15 | h8 | event | with signal | 68984 | +0.051 | 0.175 | +0.91 | -2.59 | -2.99 | -2.25 | -3.13 |
| MES | 15 | h16 | event | with signal | 68984 | +0.087 | 0.175 | +1.57 | -1.93 | -2.41 | -1.52 | -2.70 |
| MES | 15 | eod | event | with signal | 68984 | +0.270 | 0.175 | +4.48 | +0.98 | -0.15 | +1.96 | +0.14 |
| MES | 60 | h1 | event | with signal | 16462 | +0.010 | 0.092 | +0.45 | -3.05 | -3.19 | -2.90 | -3.24 |
| MES | 60 | h2 | event | against signal | 16462 | -0.017 | 0.092 | -0.64 | -4.14 | -4.02 | -4.26 | -3.64 |
| MES | 60 | h4 | event | with signal | 16462 | +0.041 | 0.092 | +1.29 | -2.21 | -2.20 | -2.23 | -3.27 |
| MES | 60 | h8 | event | with signal | 16462 | +0.077 | 0.092 | +1.95 | -1.55 | -1.22 | -1.88 | -3.48 |
| MES | 60 | h16 | event | against signal | 16462 | -0.095 | 0.092 | -2.31 | -5.81 | -6.45 | -5.17 | -3.31 |
| MES | 60 | eod | event | against signal | 16462 | -0.102 | 0.092 | -2.16 | -5.66 | -6.64 | -4.66 | -2.47 |
| MNQ | 5 | h1 | event | with signal | 226577 | +0.012 | 0.127 | +0.15 | -1.85 | -1.92 | -1.79 | -1.94 |
| MNQ | 5 | h2 | event | with signal | 226577 | +0.016 | 0.127 | +0.20 | -1.80 | -1.87 | -1.74 | -1.94 |
| MNQ | 5 | h4 | event | against signal | 226577 | -0.016 | 0.127 | -0.15 | -2.15 | -2.11 | -2.20 | -2.05 |
| MNQ | 5 | h8 | event | against signal | 226577 | -0.024 | 0.127 | -0.20 | -2.20 | -2.17 | -2.24 | -2.13 |
| MNQ | 5 | h16 | event | with signal | 226577 | +0.063 | 0.127 | +0.59 | -1.41 | -1.67 | -1.15 | -1.62 |
| MNQ | 5 | eod | event | with signal | 226577 | +0.787 | 0.127 | +6.41 | +4.41 | +1.36 | +7.39 | +4.46 |
| MNQ | 15 | h1 | event | with signal | 73121 | +0.017 | 0.074 | +0.26 | -1.74 | -1.83 | -1.65 | -1.95 |
| MNQ | 15 | h2 | event | against signal | 73121 | -0.013 | 0.074 | -0.17 | -2.17 | -2.13 | -2.21 | -1.98 |
| MNQ | 15 | h4 | event | against signal | 73121 | -0.021 | 0.074 | -0.38 | -2.38 | -2.16 | -2.62 | -2.09 |
| MNQ | 15 | h8 | event | against signal | 73121 | -0.040 | 0.074 | -0.58 | -2.58 | -2.34 | -2.84 | -2.10 |
| MNQ | 15 | h16 | event | with signal | 73121 | +0.094 | 0.074 | +1.25 | -0.75 | -1.10 | -0.38 | -1.35 |
| MNQ | 15 | eod | event | against signal | 73121 | -0.346 | 0.074 | -4.45 | -6.45 | -5.02 | -7.97 | -6.47 |
| MNQ | 60 | h1 | event | against signal | 16509 | -0.006 | 0.037 | -0.15 | -2.15 | -2.11 | -2.20 | -1.95 |
| MNQ | 60 | h2 | event | against signal | 16509 | -0.017 | 0.037 | -0.47 | -2.47 | -2.40 | -2.56 | -1.87 |
| MNQ | 60 | h4 | event | against signal | 16509 | -0.039 | 0.037 | -0.67 | -2.67 | -3.22 | -2.05 | -1.42 |
| MNQ | 60 | h8 | event | against signal | 16509 | -0.065 | 0.037 | -1.29 | -3.29 | -3.41 | -3.16 | -1.12 |
| MNQ | 60 | h16 | event | against signal | 16509 | -0.091 | 0.037 | -1.26 | -3.26 | -4.12 | -2.32 | -0.54 |
| MNQ | 60 | eod | event | against signal | 16509 | -0.107 | 0.037 | -1.05 | -3.05 | -4.58 | -1.35 | +0.54 |
| MYM | 5 | h1 | event | with signal | 125292 | +0.010 | 0.170 | +0.13 | -1.87 | +nan | -1.87 | -1.95 |
| MYM | 5 | h2 | event | with signal | 125292 | +0.011 | 0.170 | +0.17 | -1.83 | +nan | -1.83 | -1.92 |
| MYM | 5 | h4 | event | with signal | 125292 | +0.013 | 0.170 | +0.19 | -1.81 | +nan | -1.81 | -1.91 |
| MYM | 5 | h8 | event | with signal | 125292 | +0.012 | 0.170 | +0.22 | -1.78 | +nan | -1.78 | -1.91 |
| MYM | 5 | h16 | event | with signal | 125292 | +0.027 | 0.170 | +0.44 | -1.56 | +nan | -1.56 | -1.83 |
| MYM | 5 | eod | event | with signal | 125292 | +0.360 | 0.170 | +4.35 | +2.35 | +nan | +2.35 | +1.04 |
| MYM | 15 | h1 | event | with signal | 38515 | +0.010 | 0.096 | +0.23 | -1.77 | +nan | -1.77 | -1.90 |
| MYM | 15 | h2 | event | with signal | 38515 | +0.008 | 0.096 | +0.27 | -1.73 | +nan | -1.73 | -1.84 |
| MYM | 15 | h4 | event | with signal | 38515 | +0.009 | 0.096 | +0.33 | -1.67 | +nan | -1.67 | -1.74 |
| MYM | 15 | h8 | event | with signal | 38515 | +0.012 | 0.096 | +0.72 | -1.28 | +nan | -1.28 | -1.34 |
| MYM | 15 | h16 | event | with signal | 38515 | +0.005 | 0.096 | +1.25 | -0.75 | +nan | -0.75 | -0.56 |
| MYM | 15 | eod | event | with signal | 38515 | +0.154 | 0.096 | +4.07 | +2.07 | +nan | +2.07 | +1.82 |
| MYM | 60 | h1 | event | against signal | 8396 | +0.009 | 0.047 | -0.08 | -2.08 | +nan | -2.08 | -1.95 |
| MYM | 60 | h2 | event | against signal | 8396 | +0.005 | 0.047 | -0.38 | -2.38 | +nan | -2.38 | -1.90 |
| MYM | 60 | h4 | event | against signal | 8396 | -0.015 | 0.047 | -1.18 | -3.18 | +nan | -3.18 | -2.31 |
| MYM | 60 | h8 | event | with signal | 8396 | +0.040 | 0.047 | +1.90 | -0.10 | +nan | -0.10 | -1.52 |
| MYM | 60 | h16 | event | against signal | 8396 | -0.027 | 0.047 | -1.73 | -3.73 | +nan | -3.73 | -2.16 |
| MYM | 60 | eod | event | against signal | 8396 | -0.026 | 0.047 | -1.32 | -3.32 | +nan | -3.32 | -1.07 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.631 | +0.734 | +0.792 | +0.743 | +0.698 | +0.000 | +0.057 | +0.060 | +0.055 | +0.049 | +0.059 |
| MES | 15 | +0.606 | +0.668 | +0.713 | +0.706 | +0.700 | +0.000 | +0.036 | +0.029 | +0.030 | +0.034 | +0.037 |
| MES | 60 | +1.082 | +0.841 | +0.778 | +0.727 | +0.709 | +0.000 | +0.006 | +0.008 | +0.019 | +0.048 | +0.024 |
| MNQ | 5 | +0.620 | +0.706 | +0.761 | +0.733 | +0.708 | +0.000 | +0.028 | +0.029 | +0.021 | +0.013 | +0.024 |
| MNQ | 15 | +0.622 | +0.668 | +0.707 | +0.705 | +0.703 | +0.000 | +0.020 | +0.012 | +0.009 | +0.004 | +0.030 |
| MNQ | 60 | +1.141 | +0.870 | +0.796 | +0.743 | +0.730 | +0.000 | -0.002 | +0.002 | +0.004 | +0.006 | -0.016 |
| MYM | 5 | +0.554 | +0.635 | +0.690 | +0.677 | +0.670 | +0.000 | +0.024 | +0.027 | +0.034 | +0.035 | +0.049 |
| MYM | 15 | +0.599 | +0.653 | +0.694 | +0.680 | +0.681 | +0.000 | +0.017 | +0.016 | +0.018 | +0.025 | +0.037 |
| MYM | 60 | +1.124 | +0.886 | +0.813 | +0.756 | +0.730 | +0.000 | -0.012 | -0.013 | +0.003 | +0.033 | +0.012 |

## Calibration

- MES 5-min: 1036271 bars, 199795 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68984 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16462 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 226577 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 73121 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16509 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 125292 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 38515 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8396 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31779 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
