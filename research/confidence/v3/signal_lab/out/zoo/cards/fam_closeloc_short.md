# Impact card: fam_closeloc_short

bearish closeloc patterns only (short side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=0.11; we would catch an effect of 0.012 R20 or more 80% of the time).
- MES 5-min size: the market moves 1% LESS after the event than after matched bars over the next 2 bars (10 min) (-0.007 R20, possible, q=0.128, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.34 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.211 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (15 min), p=0.038; we would catch an effect of 0.021 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.010 R20, CONFIRMED, q=0.0114, 10 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.88 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.125 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.040 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.041 R20 or more 80% of the time).
- MES 60-min size: the market moves 4% LESS after the event than after matched bars over the next 2 bars (2 h) (-0.032 R20, CONFIRMED, q=1.84e-05, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.29 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.006 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.013 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.81).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.15 at recent bar sizes, 90% range up to $0.55); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.006 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.026 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 2% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.010 R20, possible, q=0.124, 12 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.26 at recent bar sizes, 90% range up to $1.13); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.009 R20 over the next 1 bar (1 h), p=0.63; we would catch an effect of 0.043 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.022 R20, CONFIRMED, q=0.000658, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.79 at recent bar sizes, 90% range up to $5.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.028 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: POSSIBLE direction effect +0.012 average bars (~$0.24 per micro at 2018-25 bar sizes) over the next 1 bar (15 min) (in the signal's direction), not confirmed (q=0.238, replicated in the other half=False, 7 of 8 years); best leg (event, with signal) grosses $+0.22 and nets $-1.78 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 15-min size: no measurable effect on how much price moves (best p=0.057).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $1.01); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.061 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.048).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.14 at recent bar sizes, 90% range up to $3.29); about 5.8x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.004 | +0.001 .. +0.007 | +0.0033 | 0.019 / 0.012 / 0.0051 | 0.00495 | 1 | 0.974 | 12/16 | +0.005 | +0.003 | False | +2.6 / +2.3 |  |
| MES | 5 | h2 | +0.005 | +0.001 .. +0.009 | +0.0028 | 0.027 / 0.026 / 0.018 | 0.0182 |  |  | 13/16 | +0.006 | +0.004 |  | +2.3 / +2.2 |  |
| MES | 5 | h4 | -0.000 | -0.007 .. +0.007 | -0.0001 | 0.93 / 0.94 / 0.94 | 0.933 |  |  | 8/16 | +0.002 | -0.003 |  | -0.1 / -0.1 | 0.012 |
| MES | 5 | h8 | -0.005 | -0.017 .. +0.007 | -0.0014 | 0.4 / 0.43 / 0.28 | 0.284 |  |  | 11/16 | +0.001 | -0.011 |  | -1.2 / -0.8 |  |
| MES | 5 | h16 | -0.008 | -0.030 .. +0.014 | -0.0016 | 0.47 / 0.5 / 0.24 | 0.233 |  |  | 8/16 | +0.001 | -0.017 |  | -1.3 / -0.7 |  |
| MES | 5 | eod | +0.018 | -0.359 .. +0.394 | +0.0007 | 0.93 / 0.93 / 0.65 | 0.664 |  |  | 11/16 | +0.064 | -0.028 |  | +0.6 / +0.1 |  |
| MES | 15 | h1 * | +0.007 | +0.002 .. +0.011 | +0.0057 | 0.0063 / 0.0052 / 0.0048 | 0.00313 | 0.893 | 0.784 | 11/16 | +0.004 | +0.010 | False | +2.6 / +2.7 |  |
| MES | 15 | h2 | +0.004 | -0.004 .. +0.011 | +0.0021 | 0.36 / 0.37 / 0.31 | 0.318 |  |  | 10/16 | +0.004 | +0.003 |  | +1.0 / +0.9 |  |
| MES | 15 | h4 | -0.001 | -0.014 .. +0.013 | -0.0003 | 0.92 / 0.92 / 0.91 | 0.905 |  |  | 10/16 | +0.002 | -0.004 |  | -0.1 / -0.1 | 0.021 |
| MES | 15 | h8 | +0.000 | -0.024 .. +0.024 | +0.0000 | 0.99 / 0.99 / 0.98 | 0.981 |  |  | 7/16 | +0.012 | -0.012 |  | +0.0 / +0.0 |  |
| MES | 15 | h16 | +0.003 | -0.045 .. +0.051 | +0.0005 | 0.92 / 0.92 / 0.82 | 0.798 |  |  | 11/16 | +0.030 | -0.025 |  | +0.2 / +0.1 |  |
| MES | 15 | eod | +0.052 | -0.152 .. +0.256 | +0.0038 | 0.62 / 0.63 / 0.12 | 0.115 |  |  | 12/16 | +0.115 | -0.010 |  | +1.8 / +0.5 |  |
| MES | 60 | h1 | +0.004 | -0.006 .. +0.014 | +0.0036 | 0.42 / 0.42 / 0.39 | 0.397 |  |  | 9/16 | +0.009 | -0.001 |  | +0.8 / +0.8 |  |
| MES | 60 | h2 | +0.001 | -0.014 .. +0.016 | +0.0006 | 0.9 / 0.9 / 0.89 | 0.895 |  |  | 7/16 | +0.003 | -0.001 |  | +0.1 / +0.1 |  |
| MES | 60 | h4 | +0.007 | -0.018 .. +0.032 | +0.0031 | 0.59 / 0.59 / 0.48 | 0.481 |  |  | 8/16 | +0.015 | -0.001 |  | +0.7 / +0.5 | 0.041 |
| MES | 60 | h8 | +0.005 | -0.038 .. +0.047 | +0.0015 | 0.83 / 0.83 / 0.73 | 0.723 |  |  | 8/16 | +0.010 | -0.000 |  | +0.3 / +0.2 |  |
| MES | 60 | h16 | +0.034 | -0.036 .. +0.105 | +0.0085 | 0.34 / 0.36 / 0.057 | 0.056 |  |  | 13/16 | +0.029 | +0.040 |  | +1.9 / +1.0 |  |
| MES | 60 | eod * | +0.040 | -0.037 .. +0.118 | +0.0095 | 0.31 / 0.33 / 0.035 | 0.0341 | 1 | 1 | 11/16 | +0.031 | +0.049 | False | +2.1 / +1.0 |  |
| MNQ | 5 | h1 | +0.002 | -0.002 .. +0.005 | +0.0012 | 0.31 / 0.29 / 0.28 | 0.279 |  |  | 9/16 | +0.004 | -0.000 |  | +1.1 / +1.0 |  |
| MNQ | 5 | h2 | -0.001 | -0.006 .. +0.004 | -0.0003 | 0.81 / 0.81 / 0.81 | 0.809 |  |  | 8/16 | +0.006 | -0.007 |  | -0.3 / -0.2 |  |
| MNQ | 5 | h4 * | -0.006 | -0.013 .. +0.002 | -0.0017 | 0.15 / 0.16 / 0.15 | 0.157 | 1 | 1 | 9/16 | +0.003 | -0.014 | False | -1.8 / -1.4 | 0.013 |
| MNQ | 5 | h8 | -0.009 | -0.023 .. +0.004 | -0.0019 | 0.19 / 0.21 / 0.13 | 0.128 |  |  | 10/16 | +0.007 | -0.025 |  | -2.0 / -1.3 |  |
| MNQ | 5 | h16 | -0.012 | -0.037 .. +0.013 | -0.0017 | 0.35 / 0.38 / 0.15 | 0.155 |  |  | 10/16 | +0.007 | -0.031 |  | -1.7 / -0.9 |  |
| MNQ | 5 | eod | -0.019 | -0.452 .. +0.414 | -0.0006 | 0.93 / 0.93 / 0.71 | 0.706 |  |  | 8/16 | +0.152 | -0.188 |  | -0.5 / -0.1 |  |
| MNQ | 15 | h1 | -0.001 | -0.005 .. +0.004 | -0.0004 | 0.78 / 0.8 / 0.83 | 0.833 |  |  | 9/16 | +0.002 | -0.004 |  | -0.2 / -0.3 |  |
| MNQ | 15 | h2 | -0.004 | -0.011 .. +0.004 | -0.0015 | 0.35 / 0.38 / 0.48 | 0.483 |  |  | 10/16 | +0.004 | -0.011 |  | -0.9 / -0.9 |  |
| MNQ | 15 | h4 * | -0.006 | -0.019 .. +0.008 | -0.0014 | 0.42 / 0.45 / 0.52 | 0.514 | 1 | 1 | 9/16 | +0.005 | -0.016 | False | -1.0 / -0.8 | 0.026 |
| MNQ | 15 | h8 | -0.002 | -0.027 .. +0.023 | -0.0004 | 0.87 / 0.88 / 0.86 | 0.873 |  |  | 8/16 | +0.012 | -0.016 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h16 | -0.007 | -0.057 .. +0.042 | -0.0011 | 0.77 / 0.78 / 0.6 | 0.599 |  |  | 7/16 | +0.026 | -0.041 |  | -0.6 / -0.3 |  |
| MNQ | 15 | eod | +0.006 | -0.217 .. +0.229 | +0.0003 | 0.96 / 0.96 / 0.89 | 0.89 |  |  | 10/16 | +0.139 | -0.127 |  | +0.2 / +0.1 |  |
| MNQ | 60 | h1 * | -0.009 | -0.019 .. +0.001 | -0.0074 | 0.093 / 0.11 / 0.077 | 0.0813 | 1 | 1 | 10/16 | -0.007 | -0.011 | False | -1.6 / -1.7 |  |
| MNQ | 60 | h2 | -0.014 | -0.030 .. +0.002 | -0.0081 | 0.092 / 0.11 / 0.056 | 0.0581 |  |  | 10/16 | -0.008 | -0.020 |  | -1.8 / -1.7 |  |
| MNQ | 60 | h4 | -0.013 | -0.041 .. +0.014 | -0.0057 | 0.34 / 0.35 / 0.2 | 0.2 |  |  | 10/16 | -0.003 | -0.024 |  | -1.2 / -1.0 | 0.043 |
| MNQ | 60 | h8 | -0.020 | -0.066 .. +0.025 | -0.0062 | 0.39 / 0.4 / 0.16 | 0.162 |  |  | 10/16 | +0.000 | -0.041 |  | -1.3 / -0.9 |  |
| MNQ | 60 | h16 | -0.013 | -0.088 .. +0.062 | -0.0029 | 0.74 / 0.75 / 0.52 | 0.524 |  |  | 8/16 | +0.002 | -0.027 |  | -0.6 / -0.3 |  |
| MNQ | 60 | eod | -0.009 | -0.091 .. +0.072 | -0.0021 | 0.82 / 0.83 / 0.65 | 0.658 |  |  | 7/16 | +0.008 | -0.026 |  | -0.5 / -0.2 |  |
| MYM | 5 | h1 * | +0.003 | -0.001 .. +0.008 | +0.0022 | 0.18 / 0.16 / 0.2 | 0.205 | 1 | 1 | 5/8 | n/a | +0.003 | False | +1.5 / +1.3 |  |
| MYM | 5 | h2 | +0.003 | -0.003 .. +0.010 | +0.0014 | 0.35 / 0.34 / 0.47 | 0.483 |  |  | 5/8 | n/a | +0.003 |  | +1.1 / +0.9 |  |
| MYM | 5 | h4 | +0.001 | -0.010 .. +0.013 | +0.0004 | 0.81 / 0.81 / 0.9 | 0.908 |  |  | 5/8 | n/a | +0.001 |  | +0.3 / +0.2 | 0.028 |
| MYM | 5 | h8 | -0.005 | -0.027 .. +0.017 | -0.0009 | 0.67 / 0.65 / 0.55 | 0.551 |  |  | 3/8 | n/a | -0.005 |  | -0.8 / -0.4 |  |
| MYM | 5 | h16 | -0.006 | -0.046 .. +0.034 | -0.0009 | 0.78 / 0.78 / 0.58 | 0.581 |  |  | 3/8 | n/a | -0.006 |  | -0.6 / -0.3 |  |
| MYM | 5 | eod | -0.038 | -0.736 .. +0.660 | -0.0013 | 0.91 / 0.91 / 0.48 | 0.483 |  |  | 2/8 | n/a | -0.038 |  | -0.8 / -0.1 |  |
| MYM | 15 | h1 * | +0.012 | +0.005 .. +0.019 | +0.0083 | 0.0011 / 0.0014 / 0.0036 | 0.00527 | 0.238 | 0.269 | 7/8 | n/a | +0.012 | False | +3.2 / +3.3 |  |
| MYM | 15 | h2 | +0.008 | -0.004 .. +0.019 | +0.0031 | 0.19 / 0.2 / 0.27 | 0.266 |  |  | 5/8 | n/a | +0.008 |  | +1.5 / +1.3 |  |
| MYM | 15 | h4 | +0.004 | -0.017 .. +0.024 | +0.0009 | 0.73 / 0.74 / 0.77 | 0.785 |  |  | 5/8 | n/a | +0.004 |  | +0.5 / +0.3 | 0.042 |
| MYM | 15 | h8 | +0.000 | -0.038 .. +0.038 | +0.0001 | 0.99 / 0.99 / 0.98 | 0.985 |  |  | 6/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 15 | h16 | -0.012 | -0.090 .. +0.066 | -0.0016 | 0.76 / 0.75 / 0.57 | 0.567 |  |  | 3/8 | n/a | -0.012 |  | -0.7 / -0.3 |  |
| MYM | 15 | eod | -0.012 | -0.360 .. +0.337 | -0.0006 | 0.95 / 0.95 / 0.83 | 0.835 |  |  | 2/8 | n/a | -0.012 |  | -0.3 / -0.1 |  |
| MYM | 60 | h1 * | +0.003 | -0.012 .. +0.018 | +0.0029 | 0.66 / 0.66 / 0.62 | 0.609 | 1 | 1 | 5/8 | n/a | +0.003 | False | +0.4 / +0.4 |  |
| MYM | 60 | h2 | +0.001 | -0.022 .. +0.024 | +0.0008 | 0.91 / 0.91 / 0.9 | 0.9 |  |  | 3/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 60 | h4 | +0.002 | -0.035 .. +0.040 | +0.0010 | 0.9 / 0.91 / 0.87 | 0.87 |  |  | 2/8 | n/a | +0.002 |  | +0.2 / +0.1 | 0.061 |
| MYM | 60 | h8 | +0.000 | -0.064 .. +0.065 | +0.0000 | 1 / 1 / 0.99 | 0.992 |  |  | 3/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 60 | h16 | +0.015 | -0.094 .. +0.124 | +0.0035 | 0.79 / 0.8 / 0.57 | 0.557 |  |  | 5/8 | n/a | +0.015 |  | +0.5 / +0.3 |  |
| MYM | 60 | eod | +0.025 | -0.093 .. +0.142 | +0.0056 | 0.68 / 0.69 / 0.36 | 0.349 |  |  | 5/8 | n/a | +0.025 |  | +0.9 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.006 .. +0.000 | -0.5% | -0.000 | 0.073 |  | 10/16 |
| MES | 5 | h2 * | -0.007 | -0.011 .. -0.003 | -1.0% | -0.008 | 0.00072 | 0.128 | 12/16 |
| MES | 5 | h4 | -0.009 | -0.015 .. -0.003 | -0.9% | -0.015 | 0.0056 |  | 11/16 |
| MES | 5 | h8 | -0.015 | -0.026 .. -0.005 | -1.1% | -0.030 | 0.0048 |  | 10/16 |
| MES | 5 | h16 | -0.025 | -0.041 .. -0.009 | -1.2% | -0.049 | 0.0017 |  | 11/16 |
| MES | 5 | eod | -0.098 | -0.250 .. +0.054 | -1.0% | -0.226 | 0.21 |  | 9/16 |
| MES | 15 | h1 * | -0.010 | -0.014 .. -0.005 | -1.9% | -0.015 | 5.4e-05 | 0.0114 | 10/16 |
| MES | 15 | h2 | -0.010 | -0.018 .. -0.003 | -1.4% | -0.021 | 0.0052 |  | 10/16 |
| MES | 15 | h4 | -0.014 | -0.026 .. -0.001 | -1.3% | -0.027 | 0.038 |  | 10/16 |
| MES | 15 | h8 | -0.012 | -0.032 .. +0.008 | -0.8% | -0.032 | 0.23 |  | 9/16 |
| MES | 15 | h16 | -0.009 | -0.038 .. +0.020 | -0.4% | -0.048 | 0.55 |  | 6/16 |
| MES | 15 | eod | -0.038 | -0.171 .. +0.095 | -0.7% | -0.104 | 0.58 |  | 6/16 |
| MES | 60 | h1 | -0.023 | -0.032 .. -0.014 | -4.5% | -0.036 | 2.4e-07 |  | 12/16 |
| MES | 60 | h2 * | -0.032 | -0.043 .. -0.020 | -4.3% | -0.048 | 6.8e-08 | 1.84e-05 | 15/16 |
| MES | 60 | h4 | -0.034 | -0.049 .. -0.018 | -3.2% | -0.059 | 0.00014 |  | 12/16 |
| MES | 60 | h8 | -0.033 | -0.054 .. -0.012 | -2.2% | -0.065 | 0.0034 |  | 13/16 |
| MES | 60 | h16 | -0.023 | -0.051 .. +0.005 | -1.1% | -0.056 | 0.13 |  | 11/16 |
| MES | 60 | eod | -0.024 | -0.052 .. +0.004 | -1.1% | -0.055 | 0.17 |  | 12/16 |
| MNQ | 5 | h1 | -0.001 | -0.004 .. +0.003 | -0.1% | +0.006 | 0.77 |  | 8/16 |
| MNQ | 5 | h2 * | -0.005 | -0.011 .. +0.001 | -0.6% | -0.003 | 0.14 | 1 | 6/16 |
| MNQ | 5 | h4 | -0.008 | -0.020 .. +0.005 | -0.7% | -0.010 | 0.22 |  | 7/16 |
| MNQ | 5 | h8 | -0.015 | -0.041 .. +0.010 | -0.9% | -0.027 | 0.24 |  | 9/16 |
| MNQ | 5 | h16 | -0.022 | -0.068 .. +0.024 | -0.9% | -0.049 | 0.36 |  | 8/16 |
| MNQ | 5 | eod | -0.143 | -0.405 .. +0.119 | -1.1% | -0.378 | 0.29 |  | 9/16 |
| MNQ | 15 | h1 * | -0.010 | -0.016 .. -0.005 | -1.9% | -0.018 | 0.0007 | 0.124 | 12/16 |
| MNQ | 15 | h2 | -0.017 | -0.030 .. -0.004 | -2.2% | -0.028 | 0.012 |  | 11/16 |
| MNQ | 15 | h4 | -0.020 | -0.052 .. +0.011 | -1.8% | -0.037 | 0.21 |  | 9/16 |
| MNQ | 15 | h8 | -0.020 | -0.069 .. +0.029 | -1.2% | -0.057 | 0.42 |  | 9/16 |
| MNQ | 15 | h16 | -0.013 | -0.066 .. +0.040 | -0.5% | -0.078 | 0.64 |  | 6/16 |
| MNQ | 15 | eod | -0.075 | -0.303 .. +0.154 | -1.2% | -0.152 | 0.52 |  | 8/16 |
| MNQ | 60 | h1 * | -0.022 | -0.031 .. -0.013 | -4.1% | -0.041 | 2.7e-06 | 0.000658 | 14/16 |
| MNQ | 60 | h2 | -0.026 | -0.038 .. -0.014 | -3.4% | -0.050 | 3.5e-05 |  | 14/16 |
| MNQ | 60 | h4 | -0.018 | -0.035 .. -0.001 | -1.6% | -0.055 | 0.076 |  | 11/16 |
| MNQ | 60 | h8 | -0.021 | -0.043 .. +0.000 | -1.3% | -0.062 | 0.11 |  | 8/16 |
| MNQ | 60 | h16 | -0.024 | -0.053 .. +0.005 | -1.1% | -0.060 | 0.17 |  | 11/16 |
| MNQ | 60 | eod | -0.031 | -0.061 .. -0.001 | -1.4% | -0.065 | 0.084 |  | 11/16 |
| MYM | 5 | h1 | -0.002 | -0.007 .. +0.002 | -0.4% | +0.001 | 0.34 |  | 4/8 |
| MYM | 5 | h2 * | -0.006 | -0.016 .. +0.005 | -0.7% | -0.008 | 0.28 | 1 | 4/8 |
| MYM | 5 | h4 | -0.013 | -0.036 .. +0.010 | -1.1% | -0.020 | 0.28 |  | 4/8 |
| MYM | 5 | h8 | -0.013 | -0.056 .. +0.030 | -0.8% | -0.031 | 0.56 |  | 2/8 |
| MYM | 5 | h16 | -0.024 | -0.084 .. +0.036 | -1.0% | -0.054 | 0.43 |  | 4/8 |
| MYM | 5 | eod | -0.138 | -0.419 .. +0.144 | -1.2% | -0.212 | 0.35 |  | 5/8 |
| MYM | 15 | h1 * | -0.012 | -0.020 .. -0.005 | -2.3% | -0.018 | 0.0094 | 1 | 8/8 |
| MYM | 15 | h2 | -0.015 | -0.032 .. +0.002 | -1.9% | -0.029 | 0.09 |  | 6/8 |
| MYM | 15 | h4 | -0.018 | -0.055 .. +0.018 | -1.6% | -0.041 | 0.33 |  | 5/8 |
| MYM | 15 | h8 | -0.030 | -0.086 .. +0.027 | -1.8% | -0.075 | 0.3 |  | 5/8 |
| MYM | 15 | h16 | -0.042 | -0.143 .. +0.058 | -1.7% | -0.112 | 0.42 |  | 6/8 |
| MYM | 15 | eod | -0.106 | -0.377 .. +0.165 | -1.8% | -0.151 | 0.46 |  | 4/8 |
| MYM | 60 | h1 | -0.012 | -0.024 .. +0.001 | -2.2% | -0.024 | 0.069 |  | 6/8 |
| MYM | 60 | h2 * | -0.023 | -0.040 .. -0.006 | -3.1% | -0.041 | 0.008 | 1 | 6/8 |
| MYM | 60 | h4 | -0.029 | -0.055 .. -0.003 | -2.7% | -0.054 | 0.029 |  | 7/8 |
| MYM | 60 | h8 | -0.023 | -0.057 .. +0.010 | -1.5% | -0.063 | 0.16 |  | 5/8 |
| MYM | 60 | h16 | -0.020 | -0.059 .. +0.019 | -1.0% | -0.065 | 0.31 |  | 6/8 |
| MYM | 60 | eod | -0.019 | -0.060 .. +0.021 | -0.9% | -0.063 | 0.35 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.28 pts | +0.03 .. +0.53 | 0.026 |
| MES | 15 | +0.29 pts | -0.13 .. +0.71 | 0.18 |
| MES | 60 | -0.09 pts | -0.90 .. +0.72 | 0.85 |
| MNQ | 5 | +0.13 pts | -0.11 .. +0.38 | 0.29 |
| MNQ | 15 | -0.02 pts | -0.41 .. +0.36 | 0.9 |
| MNQ | 60 | -0.26 pts | -1.07 .. +0.55 | 0.54 |
| MYM | 5 | +0.16 pts | -0.19 .. +0.50 | 0.38 |
| MYM | 15 | +0.41 pts | -0.18 .. +1.01 | 0.18 |
| MYM | 60 | -0.38 pts | -1.40 .. +0.63 | 0.5 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 218974 | +0.012 | 0.286 | +0.12 | -3.38 | -3.41 | -3.35 | -3.50 |
| MES | 5 | h2 | event | with signal | 218974 | +0.015 | 0.286 | +0.18 | -3.32 | -3.38 | -3.27 | -3.48 |
| MES | 5 | h4 | event | against signal | 218974 | -0.005 | 0.286 | -0.03 | -3.53 | -3.54 | -3.52 | -3.40 |
| MES | 5 | h8 | event | against signal | 218974 | +0.013 | 0.286 | +0.13 | -3.37 | -3.41 | -3.33 | -3.32 |
| MES | 5 | h16 | event | against signal | 218974 | +0.037 | 0.286 | +0.43 | -3.07 | -3.21 | -2.96 | -3.16 |
| MES | 5 | eod | event | with signal | 218974 | -0.460 | 0.286 | -4.42 | -7.92 | -6.71 | -8.84 | -6.93 |
| MES | 15 | h1 | event | with signal | 80663 | +0.010 | 0.173 | +0.16 | -3.34 | -3.43 | -3.27 | -3.44 |
| MES | 15 | h2 | event | with signal | 80663 | +0.003 | 0.173 | -0.02 | -3.52 | -3.49 | -3.53 | -3.60 |
| MES | 15 | h4 | event | against signal | 80663 | +0.011 | 0.173 | +0.29 | -3.21 | -3.33 | -3.11 | -3.21 |
| MES | 15 | h8 | event | with signal | 80663 | -0.029 | 0.173 | -0.60 | -4.10 | -3.88 | -4.28 | -3.95 |
| MES | 15 | h16 | event | with signal | 80663 | -0.062 | 0.173 | -1.23 | -4.73 | -4.31 | -5.06 | -4.35 |
| MES | 15 | eod | event | with signal | 80663 | -0.218 | 0.173 | -3.68 | -7.18 | -6.39 | -7.82 | -5.79 |
| MES | 60 | h1 | event | with signal | 21407 | -0.005 | 0.091 | -0.25 | -3.75 | -3.59 | -3.88 | -3.56 |
| MES | 60 | h2 | event | with signal | 21407 | -0.015 | 0.091 | -0.46 | -3.96 | -3.94 | -3.99 | -3.61 |
| MES | 60 | h4 | event | with signal | 21407 | -0.026 | 0.091 | -0.89 | -4.39 | -4.23 | -4.53 | -3.62 |
| MES | 60 | h8 | event | with signal | 21407 | -0.058 | 0.091 | -2.09 | -5.59 | -5.37 | -5.78 | -4.11 |
| MES | 60 | h16 | event | with signal | 21407 | -0.074 | 0.091 | -2.54 | -6.04 | -6.20 | -5.90 | -3.32 |
| MES | 60 | eod | event | with signal | 21407 | -0.079 | 0.091 | -2.43 | -5.93 | -6.29 | -5.60 | -2.86 |
| MNQ | 5 | h1 | event | with signal | 248688 | +0.002 | 0.123 | +0.05 | -1.95 | -1.97 | -1.94 | -2.01 |
| MNQ | 5 | h2 | event | against signal | 248688 | +0.001 | 0.123 | -0.01 | -2.01 | -2.04 | -1.99 | -1.91 |
| MNQ | 5 | h4 | event | against signal | 248688 | +0.017 | 0.123 | +0.19 | -1.81 | -1.95 | -1.68 | -1.76 |
| MNQ | 5 | h8 | event | against signal | 248688 | +0.042 | 0.123 | +0.41 | -1.59 | -1.84 | -1.36 | -1.70 |
| MNQ | 5 | h16 | event | against signal | 248688 | +0.079 | 0.123 | +0.84 | -1.16 | -1.61 | -0.75 | -1.51 |
| MNQ | 5 | eod | event | against signal | 248688 | +0.755 | 0.123 | +5.84 | +3.84 | +1.09 | +6.38 | +3.46 |
| MNQ | 15 | h1 | event | against signal | 86607 | +0.004 | 0.072 | +0.06 | -1.94 | -1.98 | -1.90 | -1.96 |
| MNQ | 15 | h2 | event | against signal | 86607 | +0.015 | 0.072 | +0.29 | -1.71 | -1.91 | -1.51 | -1.82 |
| MNQ | 15 | h4 | event | against signal | 86607 | +0.031 | 0.072 | +0.52 | -1.48 | -1.73 | -1.23 | -1.78 |
| MNQ | 15 | h8 | event | against signal | 86607 | +0.057 | 0.072 | +1.05 | -0.95 | -1.47 | -0.44 | -1.70 |
| MNQ | 15 | h16 | event | against signal | 86607 | +0.101 | 0.072 | +1.78 | -0.22 | -1.05 | +0.60 | -0.96 |
| MNQ | 15 | eod | event | with signal | 86607 | -0.362 | 0.072 | -4.67 | -6.67 | -4.70 | -8.61 | -5.54 |
| MNQ | 60 | h1 | event | against signal | 21937 | +0.021 | 0.036 | +0.90 | -1.10 | -1.61 | -0.60 | -1.45 |
| MNQ | 60 | h2 | event | against signal | 21937 | +0.035 | 0.036 | +1.42 | -0.58 | -1.34 | +0.16 | -1.13 |
| MNQ | 60 | h4 | event | against signal | 21937 | +0.054 | 0.036 | +2.17 | +0.17 | -0.95 | +1.26 | -0.89 |
| MNQ | 60 | h8 | event | against signal | 21937 | +0.094 | 0.036 | +4.34 | +2.34 | +0.04 | +4.59 | +0.41 |
| MNQ | 60 | h16 | event | against signal | 21937 | +0.136 | 0.036 | +5.43 | +3.43 | +1.07 | +5.74 | +0.25 |
| MNQ | 60 | eod | event | against signal | 21937 | +0.148 | 0.036 | +5.71 | +3.71 | +1.21 | +6.16 | +0.04 |
| MYM | 5 | h1 | event | with signal | 133068 | +0.010 | 0.170 | +0.09 | -1.91 | +nan | -1.91 | -1.99 |
| MYM | 5 | h2 | event | with signal | 133068 | +0.012 | 0.170 | +0.13 | -1.87 | +nan | -1.87 | -1.97 |
| MYM | 5 | h4 | event | with signal | 133068 | +0.011 | 0.170 | +0.05 | -1.95 | +nan | -1.95 | -2.06 |
| MYM | 5 | h8 | event | against signal | 133068 | -0.005 | 0.170 | +0.02 | -1.98 | +nan | -1.98 | -1.90 |
| MYM | 5 | h16 | event | against signal | 133068 | -0.002 | 0.170 | +0.17 | -1.83 | +nan | -1.83 | -1.80 |
| MYM | 5 | eod | event | against signal | 133068 | +0.257 | 0.170 | +3.67 | +1.67 | +nan | +1.67 | +0.94 |
| MYM | 15 | h1 | event | with signal | 43705 | +0.015 | 0.095 | +0.22 | -1.78 | +nan | -1.78 | -1.87 |
| MYM | 15 | h2 | event | with signal | 43705 | +0.010 | 0.095 | +0.07 | -1.93 | +nan | -1.93 | -2.02 |
| MYM | 15 | h4 | event | with signal | 43705 | +0.002 | 0.095 | -0.16 | -2.16 | +nan | -2.16 | -2.19 |
| MYM | 15 | h8 | event | with signal | 43705 | -0.001 | 0.095 | -0.35 | -2.35 | +nan | -2.35 | -2.41 |
| MYM | 15 | h16 | event | against signal | 43705 | +0.013 | 0.095 | +0.88 | -1.12 | +nan | -1.12 | -1.01 |
| MYM | 15 | eod | event | against signal | 43705 | +0.107 | 0.095 | +3.22 | +1.22 | +nan | +1.22 | +1.10 |
| MYM | 60 | h1 | event | with signal | 10809 | -0.001 | 0.047 | -0.11 | -2.11 | +nan | -2.11 | -1.96 |
| MYM | 60 | h2 | event | with signal | 10809 | -0.002 | 0.047 | -0.26 | -2.26 | +nan | -2.26 | -2.20 |
| MYM | 60 | h4 | event | with signal | 10809 | -0.007 | 0.047 | -0.70 | -2.70 | +nan | -2.70 | -2.44 |
| MYM | 60 | h8 | event | with signal | 10809 | -0.020 | 0.047 | -1.72 | -3.72 | +nan | -3.72 | -3.08 |
| MYM | 60 | h16 | event | with signal | 10809 | -0.034 | 0.047 | -2.78 | -4.78 | +nan | -4.78 | -2.95 |
| MYM | 60 | eod | event | with signal | 10809 | -0.034 | 0.047 | -2.80 | -4.80 | +nan | -4.80 | -2.46 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.594 | +0.698 | +0.762 | +0.710 | +0.664 | +0.000 | +0.052 | +0.058 | +0.053 | +0.049 | +0.052 |
| MES | 15 | +0.588 | +0.632 | +0.686 | +0.662 | +0.646 | +0.000 | +0.030 | +0.028 | +0.025 | +0.031 | +0.033 |
| MES | 60 | +0.946 | +0.788 | +0.720 | +0.640 | +0.620 | +0.000 | +0.009 | +0.010 | +0.026 | +0.060 | +0.098 |
| MNQ | 5 | +0.589 | +0.678 | +0.738 | +0.701 | +0.674 | +0.000 | +0.026 | +0.027 | +0.018 | +0.007 | +0.001 |
| MNQ | 15 | +0.591 | +0.630 | +0.680 | +0.659 | +0.646 | +0.000 | +0.008 | +0.003 | -0.002 | -0.001 | -0.008 |
| MNQ | 60 | +1.023 | +0.841 | +0.749 | +0.660 | +0.632 | +0.000 | -0.008 | -0.009 | -0.002 | +0.017 | +0.029 |
| MYM | 5 | +0.543 | +0.625 | +0.681 | +0.660 | +0.648 | +0.000 | +0.019 | +0.020 | +0.017 | +0.008 | +0.009 |
| MYM | 15 | +0.568 | +0.606 | +0.662 | +0.644 | +0.638 | +0.000 | +0.016 | +0.011 | +0.002 | -0.007 | -0.043 |
| MYM | 60 | +0.968 | +0.811 | +0.743 | +0.664 | +0.637 | +0.000 | +0.003 | +0.004 | +0.011 | +0.023 | +0.050 |

## Calibration

- MES 5-min: 1036271 bars, 218974 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 80663 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 21407 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 248688 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 86607 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 21937 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 133068 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 43705 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 10809 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45454 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
