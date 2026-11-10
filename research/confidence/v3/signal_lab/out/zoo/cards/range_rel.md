# Impact card: range_rel

bar range / average range of the previous 20 bars [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (10 min), p=0.049; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 5-min size: the market moves 18% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.091 R20, CONFIRMED, q=2.07e-272, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.29 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.228 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: POSSIBLE direction effect -0.016 average bars (top-minus-bottom spread ~$0.43; ~$0.21 per trade when trading both ends, at 2018-25 bar sizes) over the next 1 bar (15 min) (top fifth vs bottom fifth of the metric), not confirmed (q=0.085, replicated in the other half=False, 10 of 16 years); best leg (bottom fifth, long) grosses $+0.09 and nets $-3.41 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: the market moves 20% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.103 R20, CONFIRMED, q=6.92e-98, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.83 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.128 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.010 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.066 R20 or more 80% of the time).
- MES 60-min size: the market moves 21% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.109 R20, CONFIRMED, q=2e-34, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.05 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.004 R20 over the next 1 bar (5 min), p=0.88; we would catch an effect of 0.022 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 19% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.102 R20, CONFIRMED, q=6.34e-103, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.05 at recent bar sizes, 90% range up to $0.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.016 R20 over the next 1 bar (15 min), p=0.13; we would catch an effect of 0.044 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 20% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.107 R20, CONFIRMED, q=1.27e-52, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.36 at recent bar sizes, 90% range up to $1.68); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.070 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 19% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.101 R20, CONFIRMED, q=2.76e-28, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.34 at recent bar sizes, 90% range up to $3.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.005 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MYM 5-min size: the market moves 18% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.097 R20, CONFIRMED, q=3.89e-44, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.03 at recent bar sizes, 90% range up to $0.99); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.566 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.061 R20 or more 80% of the time).
- MYM 15-min size: the market moves 20% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.107 R20, CONFIRMED, q=1.16e-18, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.77 at recent bar sizes, 90% range up to $1.99); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.019 R20 over the next 1 bar (1 h), p=0.99; we would catch an effect of 0.095 R20 or more 80% of the time).
- MYM 60-min size: the market moves 24% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.127 R20, CONFIRMED, q=1.1e-13, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.40 at recent bar sizes, 90% range up to $2.90); about 3.8x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.007 .. +0.002 | -0.0024 | 0.26 / 0.27 / 0.19 | 0.196 |  |  | 10/16 | +0.002 | -0.007 |  | -1.1 / -1.1 |  |
| MES | 5 | h2 * | -0.011 | -0.019 .. -0.003 | -0.0040 | 0.0074 / 0.0081 / 0.00067 | 0.000781 | 1 | 0.836 | 11/16 | -0.008 | -0.014 | False | -3.0 / -2.7 |  |
| MES | 5 | h4 | -0.011 | -0.028 .. +0.006 | -0.0019 | 0.22 / 0.22 / 0.014 | 0.0138 |  |  | 10/16 | -0.014 | -0.008 |  | -2.1 / -1.2 | 0.017 |
| MES | 5 | h8 | -0.010 | -0.043 .. +0.023 | -0.0002 | 0.54 / 0.53 / 0.15 | 0.145 |  |  | 10/16 | -0.020 | -0.001 |  | -1.4 / -0.6 |  |
| MES | 5 | h16 | -0.016 | -0.067 .. +0.035 | +0.0008 | 0.54 / 0.54 / 0.19 | 0.189 |  |  | 8/16 | -0.039 | +0.007 |  | -1.5 / -0.6 |  |
| MES | 5 | eod | +0.199 | -0.322 .. +0.720 | +0.0102 | 0.45 / 0.44 / 0.035 | 0.0344 |  |  | 6/16 | -0.057 | +0.453 |  | +3.8 / +0.7 |  |
| MES | 15 | h1 * | -0.016 | -0.024 .. -0.007 | -0.0096 | 0.00018 / 0.00047 / 1.3e-06 | 0.00026 | 0.085 | 0.068 | 10/16 | -0.015 | -0.016 | False | -3.4 / -3.7 |  |
| MES | 15 | h2 | -0.018 | -0.035 .. -0.002 | -0.0063 | 0.03 / 0.034 / 0.0004 | 0.000781 |  |  | 10/16 | -0.020 | -0.017 |  | -2.5 / -2.2 |  |
| MES | 15 | h4 | -0.017 | -0.048 .. +0.014 | -0.0036 | 0.28 / 0.27 / 0.05 | 0.0464 |  |  | 8/16 | -0.019 | -0.016 |  | -1.6 / -1.1 | 0.036 |
| MES | 15 | h8 | -0.014 | -0.071 .. +0.042 | -0.0010 | 0.62 / 0.61 / 0.31 | 0.309 |  |  | 9/16 | -0.045 | +0.016 |  | -1.0 / -0.5 |  |
| MES | 15 | h16 | +0.005 | -0.099 .. +0.109 | +0.0042 | 0.93 / 0.92 / 0.81 | 0.806 |  |  | 7/16 | -0.029 | +0.038 |  | +0.2 / +0.1 |  |
| MES | 15 | eod | +0.247 | -0.246 .. +0.740 | +0.0228 | 0.33 / 0.3 / 3.1e-07 | 0.00026 |  |  | 7/16 | -0.064 | +0.557 |  | +4.5 / +1.0 |  |
| MES | 60 | h1 * | -0.010 | -0.028 .. +0.008 | -0.0085 | 0.28 / 0.28 / 0.13 | 0.134 | 1 | 1 | 11/16 | -0.013 | -0.006 | False | -1.1 / -1.1 |  |
| MES | 60 | h2 | -0.010 | -0.040 .. +0.020 | -0.0077 | 0.52 / 0.52 / 0.33 | 0.327 |  |  | 11/16 | -0.015 | -0.005 |  | -0.8 / -0.6 |  |
| MES | 60 | h4 | -0.017 | -0.064 .. +0.030 | -0.0066 | 0.48 / 0.49 / 0.28 | 0.271 |  |  | 10/16 | -0.026 | -0.008 |  | -1.0 / -0.7 | 0.066 |
| MES | 60 | h8 | -0.014 | -0.083 .. +0.055 | -0.0052 | 0.68 / 0.69 / 0.55 | 0.562 |  |  | 10/16 | -0.028 | -0.000 |  | -0.6 / -0.4 |  |
| MES | 60 | h16 | +0.008 | -0.084 .. +0.099 | -0.0024 | 0.87 / 0.87 / 0.82 | 0.833 |  |  | 8/16 | +0.003 | +0.012 |  | +0.2 / +0.2 |  |
| MES | 60 | eod | -0.001 | -0.094 .. +0.092 | -0.0033 | 0.98 / 0.98 / 0.98 | 0.985 |  |  | 8/16 | -0.012 | +0.009 |  | -0.0 / -0.0 |  |
| MNQ | 5 | h1 * | -0.004 | -0.010 .. +0.001 | -0.0020 | 0.14 / 0.15 / 0.052 | 0.0534 | 1 | 1 | 10/16 | -0.003 | -0.005 | False | -1.2 / -1.5 |  |
| MNQ | 5 | h2 | -0.009 | -0.024 .. +0.005 | -0.0022 | 0.21 / 0.2 / 0.018 | 0.0167 |  |  | 10/16 | -0.018 | -0.001 |  | -1.6 / -1.3 |  |
| MNQ | 5 | h4 | -0.014 | -0.045 .. +0.018 | -0.0013 | 0.41 / 0.4 / 0.032 | 0.0313 |  |  | 13/16 | -0.038 | +0.011 |  | -1.5 / -0.8 | 0.022 |
| MNQ | 5 | h8 | -0.005 | -0.065 .. +0.055 | +0.0004 | 0.87 / 0.86 / 0.6 | 0.595 |  |  | 11/16 | -0.047 | +0.037 |  | -0.4 / -0.2 |  |
| MNQ | 5 | h16 | -0.010 | -0.100 .. +0.080 | +0.0006 | 0.83 / 0.83 / 0.58 | 0.582 |  |  | 9/16 | -0.064 | +0.044 |  | -0.5 / -0.2 |  |
| MNQ | 5 | eod | +0.229 | -0.463 .. +0.921 | +0.0066 | 0.52 / 0.5 / 0.0071 | 0.00547 |  |  | 4/16 | -0.272 | +0.726 |  | +2.9 / +0.6 |  |
| MNQ | 15 | h1 * | -0.016 | -0.029 .. -0.003 | -0.0111 | 0.016 / 0.022 / 9.4e-05 | 0.00026 | 1 | 0.968 | 13/16 | -0.014 | -0.019 | False | -2.3 / -2.4 |  |
| MNQ | 15 | h2 | -0.019 | -0.039 .. +0.000 | -0.0054 | 0.054 / 0.067 / 0.01 | 0.0112 |  |  | 12/16 | -0.023 | -0.015 |  | -1.5 / -1.9 |  |
| MNQ | 15 | h4 | -0.026 | -0.065 .. +0.014 | -0.0042 | 0.2 / 0.21 / 0.054 | 0.0531 |  |  | 9/16 | -0.034 | -0.018 |  | -1.2 / -1.3 | 0.044 |
| MNQ | 15 | h8 | -0.020 | -0.083 .. +0.043 | -0.0024 | 0.53 / 0.54 / 0.29 | 0.288 |  |  | 8/16 | -0.041 | +0.000 |  | -0.7 / -0.6 |  |
| MNQ | 15 | h16 | +0.053 | -0.088 .. +0.195 | +0.0107 | 0.46 / 0.46 / 0.037 | 0.0388 |  |  | 9/16 | +0.001 | +0.106 |  | +1.8 / +0.7 |  |
| MNQ | 15 | eod | +0.365 | -0.349 .. +1.079 | +0.0229 | 0.32 / 0.3 / 4.2e-08 | 0.00026 |  |  | 8/16 | -0.134 | +0.861 |  | +4.0 / +1.0 |  |
| MNQ | 60 | h1 * | -0.007 | -0.026 .. +0.011 | -0.0037 | 0.44 / 0.45 / 0.25 | 0.246 | 1 | 1 | 8/16 | -0.011 | -0.004 | False | -0.7 / -0.8 |  |
| MNQ | 60 | h2 | -0.001 | -0.033 .. +0.031 | -0.0018 | 0.94 / 0.94 / 0.9 | 0.902 |  |  | 9/16 | -0.016 | +0.014 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h4 | +0.005 | -0.047 .. +0.057 | -0.0013 | 0.86 / 0.86 / 0.75 | 0.757 |  |  | 5/16 | -0.014 | +0.023 |  | +0.3 / +0.2 | 0.070 |
| MNQ | 60 | h8 | +0.017 | -0.059 .. +0.093 | -0.0023 | 0.65 / 0.65 / 0.44 | 0.444 |  |  | 8/16 | -0.007 | +0.042 |  | +0.7 / +0.4 |  |
| MNQ | 60 | h16 | +0.021 | -0.076 .. +0.117 | +0.0007 | 0.68 / 0.66 / 0.55 | 0.553 |  |  | 8/16 | -0.028 | +0.069 |  | +0.6 / +0.4 |  |
| MNQ | 60 | eod | +0.024 | -0.074 .. +0.123 | +0.0015 | 0.63 / 0.62 / 0.51 | 0.503 |  |  | 7/16 | -0.028 | +0.076 |  | +0.7 / +0.5 |  |
| MYM | 5 | h1 * | -0.005 | -0.015 .. +0.006 | -0.0005 | 0.35 / 0.39 / 0.33 | 0.328 | 1 | 1 | 6/8 | n/a | -0.005 | False | -0.9 / -0.9 |  |
| MYM | 5 | h2 | -0.006 | -0.038 .. +0.026 | +0.0034 | 0.72 / 0.72 / 0.46 | 0.448 |  |  | 6/8 | n/a | -0.006 |  | -0.6 / -0.4 |  |
| MYM | 5 | h4 | +0.019 | -0.060 .. +0.097 | +0.0106 | 0.64 / 0.65 / 0.06 | 0.0585 |  |  | 2/8 | n/a | +0.019 |  | +1.2 / +0.5 | 0.045 |
| MYM | 5 | h8 | +0.050 | -0.094 .. +0.194 | +0.0144 | 0.5 / 0.51 / 0.0013 | 0.00211 |  |  | 3/8 | n/a | +0.050 |  | +2.3 / +0.7 |  |
| MYM | 5 | h16 | +0.076 | -0.114 .. +0.266 | +0.0159 | 0.43 / 0.45 / 0.00028 | 0.00105 |  |  | 4/8 | n/a | +0.076 |  | +2.9 / +0.8 |  |
| MYM | 5 | eod | +0.413 | -0.540 .. +1.366 | +0.0179 | 0.4 / 0.4 / 1.9e-07 | 0.000527 |  |  | 1/8 | n/a | +0.413 |  | +4.0 / +0.8 |  |
| MYM | 15 | h1 | -0.006 | -0.021 .. +0.008 | -0.0008 | 0.37 / 0.44 / 0.22 | 0.213 |  |  | 5/8 | n/a | -0.006 |  | -0.7 / -0.9 |  |
| MYM | 15 | h2 | +0.004 | -0.036 .. +0.045 | +0.0068 | 0.84 / 0.85 / 0.68 | 0.691 |  |  | 3/8 | n/a | +0.004 |  | +0.2 / +0.2 |  |
| MYM | 15 | h4 | +0.013 | -0.069 .. +0.096 | +0.0081 | 0.75 / 0.77 / 0.48 | 0.482 |  |  | 4/8 | n/a | +0.013 |  | +0.4 / +0.3 | 0.061 |
| MYM | 15 | h8 | +0.056 | -0.104 .. +0.217 | +0.0148 | 0.49 / 0.5 / 0.035 | 0.0358 |  |  | 5/8 | n/a | +0.056 |  | +1.5 / +0.7 |  |
| MYM | 15 | h16 | +0.198 | -0.185 .. +0.582 | +0.0338 | 0.31 / 0.32 / 1.6e-06 | 0.000527 |  |  | 4/8 | n/a | +0.198 |  | +3.8 / +1.0 |  |
| MYM | 15 | eod * | +0.566 | -0.462 .. +1.593 | +0.0401 | 0.28 / 0.29 / 4e-09 | 0.000527 | 1 | 1 | 4/8 | n/a | +0.566 | False | +4.5 / +1.1 |  |
| MYM | 60 | h1 * | -0.019 | -0.046 .. +0.008 | -0.0132 | 0.16 / 0.16 / 0.046 | 0.0448 | 1 | 1 | 6/8 | n/a | -0.019 | False | -1.4 / -1.4 |  |
| MYM | 60 | h2 | -0.015 | -0.060 .. +0.031 | -0.0062 | 0.53 / 0.52 / 0.31 | 0.311 |  |  | 6/8 | n/a | -0.015 |  | -0.8 / -0.6 |  |
| MYM | 60 | h4 | -0.002 | -0.074 .. +0.069 | -0.0002 | 0.95 / 0.96 / 0.94 | 0.947 |  |  | 5/8 | n/a | -0.002 |  | -0.1 / -0.1 | 0.095 |
| MYM | 60 | h8 | +0.023 | -0.080 .. +0.127 | +0.0035 | 0.66 / 0.67 / 0.46 | 0.453 |  |  | 3/8 | n/a | +0.023 |  | +0.7 / +0.4 |  |
| MYM | 60 | h16 | +0.021 | -0.114 .. +0.157 | -0.0009 | 0.76 / 0.75 / 0.64 | 0.638 |  |  | 4/8 | n/a | +0.021 |  | +0.5 / +0.3 |  |
| MYM | 60 | eod | +0.011 | -0.129 .. +0.151 | -0.0013 | 0.88 / 0.87 / 0.81 | 0.808 |  |  | 4/8 | n/a | +0.011 |  | +0.2 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.091 | +0.086 .. +0.097 | +18.3% | +0.214 | 6.4e-276 | 2.07e-272 | 16/16 |
| MES | 5 | h2 | +0.117 | +0.110 .. +0.124 | +16.7% | +0.267 | 3.5e-234 |  | 16/16 |
| MES | 5 | h4 | +0.146 | +0.132 .. +0.160 | +14.7% | +0.330 | 3e-94 |  | 16/16 |
| MES | 5 | h8 | +0.184 | +0.155 .. +0.213 | +12.8% | +0.398 | 7.3e-36 |  | 15/16 |
| MES | 5 | h16 | +0.225 | +0.177 .. +0.273 | +10.7% | +0.470 | 7.5e-20 |  | 15/16 |
| MES | 5 | eod | +0.474 | -0.031 .. +0.980 | +4.8% | +0.950 | 0.066 |  | 15/16 |
| MES | 15 | h1 * | +0.103 | +0.093 .. +0.112 | +20.1% | +0.235 | 4.9e-101 | 6.92e-98 | 16/16 |
| MES | 15 | h2 | +0.127 | +0.112 .. +0.143 | +17.5% | +0.285 | 1.3e-60 |  | 16/16 |
| MES | 15 | h4 | +0.150 | +0.115 .. +0.185 | +14.2% | +0.325 | 3.9e-17 |  | 15/16 |
| MES | 15 | h8 | +0.176 | +0.118 .. +0.234 | +11.4% | +0.341 | 2.7e-09 |  | 15/16 |
| MES | 15 | h16 | +0.201 | +0.101 .. +0.300 | +8.8% | +0.330 | 7.6e-05 |  | 15/16 |
| MES | 15 | eod | +0.025 | -0.437 .. +0.488 | +0.5% | +0.264 | 1 |  | 11/16 |
| MES | 60 | h1 * | +0.109 | +0.092 .. +0.125 | +21.2% | +0.243 | 2.3e-37 | 2e-34 | 15/16 |
| MES | 60 | h2 | +0.133 | +0.108 .. +0.158 | +18.0% | +0.297 | 8.3e-26 |  | 15/16 |
| MES | 60 | h4 | +0.156 | +0.118 .. +0.194 | +14.8% | +0.342 | 5.9e-16 |  | 14/16 |
| MES | 60 | h8 | +0.157 | +0.108 .. +0.207 | +10.4% | +0.371 | 1.1e-09 |  | 13/16 |
| MES | 60 | h16 | +0.128 | +0.069 .. +0.187 | +6.2% | +0.349 | 2e-05 |  | 14/16 |
| MES | 60 | eod | +0.117 | +0.055 .. +0.178 | +5.4% | +0.341 | 0.0002 |  | 14/16 |
| MNQ | 5 | h1 * | +0.102 | +0.093 .. +0.111 | +19.1% | +0.237 | 4.3e-106 | 6.34e-103 | 16/16 |
| MNQ | 5 | h2 | +0.122 | +0.102 .. +0.141 | +15.8% | +0.285 | 2.5e-33 |  | 15/16 |
| MNQ | 5 | h4 | +0.150 | +0.109 .. +0.191 | +13.5% | +0.337 | 9.6e-13 |  | 15/16 |
| MNQ | 5 | h8 | +0.177 | +0.086 .. +0.269 | +10.9% | +0.379 | 0.00015 |  | 15/16 |
| MNQ | 5 | h16 | +0.208 | +0.040 .. +0.377 | +8.7% | +0.408 | 0.015 |  | 15/16 |
| MNQ | 5 | eod | +0.336 | -0.603 .. +1.274 | +2.7% | +0.629 | 0.48 |  | 15/16 |
| MNQ | 15 | h1 * | +0.107 | +0.094 .. +0.120 | +20.0% | +0.231 | 1.2e-55 | 1.27e-52 | 15/16 |
| MNQ | 15 | h2 | +0.122 | +0.082 .. +0.161 | +15.7% | +0.266 | 2.1e-09 |  | 15/16 |
| MNQ | 15 | h4 | +0.120 | +0.015 .. +0.226 | +10.6% | +0.271 | 0.025 |  | 15/16 |
| MNQ | 15 | h8 | +0.125 | -0.053 .. +0.304 | +7.5% | +0.224 | 0.17 |  | 14/16 |
| MNQ | 15 | h16 | +0.149 | -0.040 .. +0.338 | +5.9% | +0.115 | 0.12 |  | 15/16 |
| MNQ | 15 | eod | -0.111 | -0.937 .. +0.715 | -1.7% | +0.027 | 0.79 |  | 3/16 |
| MNQ | 60 | h1 * | +0.101 | +0.084 .. +0.118 | +19.0% | +0.225 | 3.7e-31 | 2.76e-28 | 15/16 |
| MNQ | 60 | h2 | +0.125 | +0.100 .. +0.150 | +16.3% | +0.277 | 5.9e-23 |  | 16/16 |
| MNQ | 60 | h4 | +0.151 | +0.114 .. +0.188 | +13.6% | +0.320 | 1.1e-15 |  | 16/16 |
| MNQ | 60 | h8 | +0.155 | +0.104 .. +0.205 | +9.8% | +0.352 | 5.3e-09 |  | 13/16 |
| MNQ | 60 | h16 | +0.133 | +0.070 .. +0.195 | +6.0% | +0.357 | 4.4e-05 |  | 12/16 |
| MNQ | 60 | eod | +0.130 | +0.067 .. +0.192 | +5.6% | +0.355 | 7.2e-05 |  | 14/16 |
| MYM | 5 | h1 * | +0.097 | +0.084 .. +0.110 | +18.3% | +0.216 | 3.9e-47 | 3.89e-44 | 8/8 |
| MYM | 5 | h2 | +0.115 | +0.083 .. +0.147 | +15.1% | +0.254 | 1.5e-12 |  | 7/8 |
| MYM | 5 | h4 | +0.126 | +0.047 .. +0.204 | +11.4% | +0.288 | 0.0018 |  | 7/8 |
| MYM | 5 | h8 | +0.141 | -0.013 .. +0.295 | +8.9% | +0.306 | 0.073 |  | 7/8 |
| MYM | 5 | h16 | +0.162 | -0.054 .. +0.378 | +6.9% | +0.297 | 0.14 |  | 7/8 |
| MYM | 5 | eod | +0.377 | -0.604 .. +1.358 | +3.2% | +0.936 | 0.45 |  | 7/8 |
| MYM | 15 | h1 * | +0.107 | +0.085 .. +0.129 | +20.2% | +0.230 | 2e-21 | 1.16e-18 | 7/8 |
| MYM | 15 | h2 | +0.121 | +0.065 .. +0.177 | +15.8% | +0.257 | 2.2e-05 |  | 7/8 |
| MYM | 15 | h4 | +0.114 | -0.014 .. +0.242 | +10.2% | +0.241 | 0.08 |  | 7/8 |
| MYM | 15 | h8 | +0.103 | -0.105 .. +0.311 | +6.3% | +0.161 | 0.33 |  | 7/8 |
| MYM | 15 | h16 | +0.050 | -0.325 .. +0.425 | +2.0% | -0.010 | 0.8 |  | 6/8 |
| MYM | 15 | eod | -0.131 | -1.118 .. +0.855 | -2.2% | +0.052 | 0.8 |  | 2/8 |
| MYM | 60 | h1 * | +0.127 | +0.096 .. +0.157 | +24.2% | +0.267 | 2.5e-16 | 1.1e-13 | 7/8 |
| MYM | 60 | h2 | +0.155 | +0.113 .. +0.196 | +20.5% | +0.335 | 3.2e-13 |  | 6/8 |
| MYM | 60 | h4 | +0.185 | +0.126 .. +0.244 | +17.1% | +0.396 | 8.5e-10 |  | 6/8 |
| MYM | 60 | h8 | +0.203 | +0.129 .. +0.277 | +13.1% | +0.439 | 6.6e-08 |  | 7/8 |
| MYM | 60 | h16 | +0.194 | +0.099 .. +0.289 | +9.2% | +0.400 | 6e-05 |  | 8/8 |
| MYM | 60 | eod | +0.174 | +0.076 .. +0.272 | +7.8% | +0.389 | 0.00049 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.44 pts | -0.83 .. -0.05 | 0.026 |
| MES | 15 | -0.82 pts | -1.54 .. -0.10 | 0.026 |
| MES | 60 | -1.22 pts | -2.72 .. +0.27 | 0.12 |
| MNQ | 5 | -0.60 pts | -0.98 .. -0.22 | 0.0018 |
| MNQ | 15 | -0.72 pts | -1.41 .. -0.02 | 0.055 |
| MNQ | 60 | -1.04 pts | -2.62 .. +0.53 | 0.19 |
| MYM | 5 | -0.35 pts | -0.92 .. +0.23 | 0.24 |
| MYM | 15 | +0.09 pts | -1.02 .. +1.19 | 0.88 |
| MYM | 60 | -0.31 pts | -2.78 .. +2.16 | 0.81 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | short | 205944 | +0.001 | 0.340 | +0.03 | -3.47 | -3.52 | -3.41 | -3.46 |
| MES | 5 | h2 | bottom fifth | long | 207373 | +0.007 | 0.349 | +0.07 | -3.43 | -3.46 | -3.39 | -3.45 |
| MES | 5 | h4 | bottom fifth | long | 207373 | +0.010 | 0.349 | +0.13 | -3.37 | -3.41 | -3.32 | -3.40 |
| MES | 5 | h8 | bottom fifth | long | 207373 | +0.018 | 0.349 | +0.28 | -3.22 | -3.33 | -3.09 | -3.29 |
| MES | 5 | h16 | bottom fifth | long | 207373 | +0.035 | 0.349 | +0.44 | -3.06 | -3.14 | -2.97 | -3.21 |
| MES | 5 | eod | top fifth | long | 205944 | +0.590 | 0.340 | +4.24 | +0.74 | -0.32 | +1.77 | -0.73 |
| MES | 15 | h1 | bottom fifth | long | 68559 | +0.006 | 0.177 | +0.09 | -3.41 | -3.41 | -3.41 | -3.38 |
| MES | 15 | h2 | bottom fifth | long | 68559 | +0.007 | 0.177 | +0.18 | -3.32 | -3.33 | -3.31 | -3.29 |
| MES | 15 | h4 | bottom fifth | long | 68559 | +0.013 | 0.177 | +0.43 | -3.07 | -3.21 | -2.94 | -3.07 |
| MES | 15 | h8 | bottom fifth | long | 68559 | +0.024 | 0.177 | +0.67 | -2.83 | -2.91 | -2.74 | -2.86 |
| MES | 15 | h16 | top fifth | long | 68357 | +0.081 | 0.203 | +1.04 | -2.46 | -2.63 | -2.29 | -3.35 |
| MES | 15 | eod | top fifth | long | 68357 | +0.304 | 0.203 | +3.97 | +0.47 | -0.87 | +1.80 | -0.54 |
| MES | 60 | h1 | bottom fifth | long | 16671 | +0.008 | 0.088 | +0.16 | -3.34 | -3.30 | -3.38 | -3.39 |
| MES | 60 | h2 | bottom fifth | long | 16671 | +0.016 | 0.088 | +0.37 | -3.13 | -3.01 | -3.25 | -3.30 |
| MES | 60 | h4 | bottom fifth | long | 16671 | +0.031 | 0.088 | +0.88 | -2.62 | -2.59 | -2.65 | -3.15 |
| MES | 60 | h8 | bottom fifth | long | 16671 | +0.063 | 0.088 | +1.56 | -1.94 | -1.63 | -2.25 | -3.41 |
| MES | 60 | h16 | top fifth | long | 16666 | +0.091 | 0.099 | +3.62 | +0.12 | -1.36 | +1.58 | -1.44 |
| MES | 60 | eod | bottom fifth | long | 16671 | +0.168 | 0.088 | +4.19 | +0.69 | +0.74 | +0.65 | -4.05 |
| MNQ | 5 | h1 | bottom fifth | long | 207161 | +0.006 | 0.145 | +0.05 | -1.95 | -1.97 | -1.92 | -1.98 |
| MNQ | 5 | h2 | bottom fifth | long | 207161 | +0.007 | 0.145 | +0.09 | -1.91 | -1.93 | -1.88 | -1.95 |
| MNQ | 5 | h4 | bottom fifth | long | 207161 | +0.012 | 0.145 | +0.20 | -1.80 | -1.88 | -1.69 | -1.84 |
| MNQ | 5 | h8 | bottom fifth | long | 207161 | +0.019 | 0.145 | +0.43 | -1.57 | -1.79 | -1.26 | -1.66 |
| MNQ | 5 | h16 | bottom fifth | long | 207161 | +0.047 | 0.145 | +0.68 | -1.32 | -1.59 | -0.96 | -1.56 |
| MNQ | 5 | eod | top fifth | long | 206866 | +0.888 | 0.148 | +5.09 | +3.09 | +1.03 | +5.46 | +2.33 |
| MNQ | 15 | h1 | bottom fifth | long | 68433 | +0.015 | 0.074 | +0.17 | -1.83 | -1.90 | -1.76 | -1.89 |
| MNQ | 15 | h2 | bottom fifth | long | 68433 | +0.018 | 0.074 | +0.41 | -1.59 | -1.81 | -1.33 | -1.68 |
| MNQ | 15 | h4 | bottom fifth | long | 68433 | +0.027 | 0.074 | +0.69 | -1.31 | -1.68 | -0.88 | -1.52 |
| MNQ | 15 | h8 | bottom fifth | long | 68433 | +0.047 | 0.074 | +1.03 | -0.97 | -1.44 | -0.42 | -1.43 |
| MNQ | 15 | h16 | top fifth | long | 68391 | +0.095 | 0.084 | +1.45 | -0.55 | -1.21 | +0.17 | -1.23 |
| MNQ | 15 | eod | top fifth | long | 68391 | +0.435 | 0.084 | +5.35 | +3.35 | +0.88 | +6.05 | +2.91 |
| MNQ | 60 | h1 | bottom fifth | long | 16672 | +0.010 | 0.038 | +0.32 | -1.68 | -1.75 | -1.60 | -1.90 |
| MNQ | 60 | h2 | bottom fifth | long | 16672 | +0.019 | 0.038 | +0.68 | -1.32 | -1.48 | -1.12 | -1.70 |
| MNQ | 60 | h4 | top fifth | long | 16670 | +0.070 | 0.040 | +2.80 | +0.80 | -1.31 | +2.99 | -1.18 |
| MNQ | 60 | h8 | top fifth | long | 16670 | +0.117 | 0.040 | +3.99 | +1.99 | -0.34 | +4.44 | -0.88 |
| MNQ | 60 | h16 | top fifth | long | 16670 | +0.131 | 0.040 | +5.11 | +3.11 | +0.06 | +6.30 | +1.30 |
| MNQ | 60 | eod | top fifth | long | 16670 | +0.138 | 0.040 | +5.23 | +3.23 | +0.14 | +6.47 | +1.53 |
| MYM | 5 | h1 | bottom fifth | long | 103899 | +0.001 | 0.169 | +0.07 | -1.93 | +nan | -1.93 | -1.94 |
| MYM | 5 | h2 | bottom fifth | long | 103899 | -0.006 | 0.169 | +0.12 | -1.88 | +nan | -1.88 | -1.88 |
| MYM | 5 | h4 | top fifth | long | 103742 | -0.007 | 0.183 | -0.01 | -2.01 | +nan | -2.01 | -1.93 |
| MYM | 5 | h8 | top fifth | long | 103742 | +0.003 | 0.183 | +0.16 | -1.84 | +nan | -1.84 | -1.84 |
| MYM | 5 | h16 | top fifth | long | 103742 | +0.009 | 0.183 | +0.14 | -1.86 | +nan | -1.86 | -1.99 |
| MYM | 5 | eod | top fifth | long | 103742 | +0.301 | 0.183 | +3.43 | +1.43 | +nan | +1.43 | +0.42 |
| MYM | 15 | h1 | top fifth | short | 34279 | +0.005 | 0.105 | +0.13 | -1.87 | +nan | -1.87 | -1.90 |
| MYM | 15 | h2 | bottom fifth | short | 34283 | +0.013 | 0.092 | -0.11 | -2.11 | +nan | -2.11 | -2.16 |
| MYM | 15 | h4 | bottom fifth | short | 34283 | +0.037 | 0.092 | -0.17 | -2.17 | +nan | -2.17 | -2.33 |
| MYM | 15 | h8 | top fifth | long | 34279 | +0.000 | 0.105 | +0.13 | -1.87 | +nan | -1.87 | -2.00 |
| MYM | 15 | h16 | top fifth | long | 34279 | -0.004 | 0.105 | +0.27 | -1.73 | +nan | -1.73 | -1.14 |
| MYM | 15 | eod | top fifth | long | 34279 | +0.211 | 0.105 | +3.54 | +1.54 | +nan | +1.54 | +1.99 |
| MYM | 60 | h1 | top fifth | short | 8325 | +0.018 | 0.050 | +0.59 | -1.41 | +nan | -1.41 | -1.30 |
| MYM | 60 | h2 | top fifth | short | 8325 | +0.010 | 0.050 | +0.16 | -1.84 | +nan | -1.84 | -1.45 |
| MYM | 60 | h4 | top fifth | short | 8325 | -0.001 | 0.050 | -0.52 | -2.52 | +nan | -2.52 | -1.75 |
| MYM | 60 | h8 | top fifth | long | 8325 | +0.037 | 0.050 | +1.97 | -0.03 | +nan | -0.03 | -1.46 |
| MYM | 60 | h16 | top fifth | long | 8325 | +0.040 | 0.050 | +2.77 | +0.77 | +nan | +0.77 | -0.62 |
| MYM | 60 | eod | top fifth | long | 8325 | +0.043 | 0.050 | +2.95 | +0.95 | +nan | +0.95 | -0.60 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.324 | +0.289 | +0.182 | +0.086 | +0.026 | +0.000 | -0.000 | -0.009 | -0.007 | -0.007 | -0.008 |
| MES | 15 | +0.449 | +0.416 | +0.270 | +0.129 | +0.036 | +0.000 | -0.006 | -0.008 | -0.005 | +0.008 | +0.049 |
| MES | 60 | +1.230 | +0.611 | +0.365 | +0.215 | +0.074 | +0.000 | -0.007 | -0.004 | -0.018 | -0.033 | +0.116 |
| MNQ | 5 | +0.339 | +0.305 | +0.195 | +0.096 | +0.026 | +0.000 | +0.001 | -0.002 | -0.002 | +0.011 | +0.014 |
| MNQ | 15 | +0.423 | +0.398 | +0.268 | +0.129 | +0.031 | +0.000 | +0.003 | +0.002 | -0.000 | +0.015 | +0.115 |
| MNQ | 60 | +1.675 | +0.539 | +0.332 | +0.205 | +0.064 | +0.000 | -0.007 | +0.001 | +0.005 | +0.096 | +0.044 |
| MYM | 5 | +0.356 | +0.328 | +0.206 | +0.097 | +0.025 | +0.000 | +0.008 | +0.011 | +0.048 | +0.096 | +0.137 |
| MYM | 15 | +0.403 | +0.408 | +0.265 | +0.133 | +0.034 | +0.000 | +0.026 | +0.043 | +0.059 | +0.124 | +0.360 |
| MYM | 60 | +1.243 | +0.571 | +0.330 | +0.204 | +0.077 | +0.000 | -0.019 | -0.017 | -0.001 | +0.037 | +0.046 |

## Calibration

- MES 5-min: 1036209 bars, 205944 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342156 bars, 68357 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83351 bars, 16666 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034460 bars, 206866 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342000 bars, 68391 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83349 bars, 16670 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519008 bars, 103742 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171396 bars, 34279 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41624 bars, 8325 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
