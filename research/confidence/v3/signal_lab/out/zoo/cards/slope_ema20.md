# Impact card: slope_ema20

5-bar change of EMA20 in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.025 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 5-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.029 R20, CONFIRMED, q=7.59e-26, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.41 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.213 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.158 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MES 15-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.035 R20, CONFIRMED, q=3.66e-13, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.71 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.123 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.018 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.087 R20 or more 80% of the time).
- MES 60-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.044 R20, CONFIRMED, q=1.86e-07, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.62 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.062 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=0.8; we would catch an effect of 0.032 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.027 R20, CONFIRMED, q=2.6e-21, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.06 at recent bar sizes, 90% range up to $0.62); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.364 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.053 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.030 R20, CONFIRMED, q=0.0012, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.44 at recent bar sizes, 90% range up to $1.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.011 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.092 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.038 R20, CONFIRMED, q=3.35e-05, 13 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.52 at recent bar sizes, 90% range up to $4.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.069 R20 over the next 16 bars (80 min), p=0.72; we would catch an effect of 0.045 R20 or more 80% of the time).
- MYM 5-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.033 R20, CONFIRMED, q=5.54e-07, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.56 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.164 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.581 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MYM 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.041 R20, CONFIRMED, q=0.021, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.25 at recent bar sizes, 90% range up to $1.99); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.079 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.125 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.69 at recent bar sizes, 90% range up to $4.44); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.007 .. +0.001 | -0.0012 | 0.2 / 0.19 / 0.23 | 0.234 |  |  | 11/16 | -0.006 | +0.001 |  | -1.2 / -1.3 |  |
| MES | 5 | h2 | -0.005 | -0.014 .. +0.003 | -0.0020 | 0.19 / 0.17 / 0.22 | 0.229 |  |  | 10/16 | -0.015 | +0.004 |  | -1.7 / -1.3 |  |
| MES | 5 | h4 | -0.011 | -0.027 .. +0.005 | -0.0031 | 0.17 / 0.15 / 0.21 | 0.209 |  |  | 12/16 | -0.035 | +0.013 |  | -2.4 / -1.4 | 0.024 |
| MES | 5 | h8 * | -0.025 | -0.056 .. +0.007 | -0.0057 | 0.12 / 0.1 / 0.14 | 0.138 | 1 | 1 | 12/16 | -0.068 | +0.019 | False | -3.7 / -1.5 |  |
| MES | 5 | h16 | -0.036 | -0.094 .. +0.021 | -0.0049 | 0.22 / 0.18 / 0.22 | 0.215 |  |  | 12/16 | -0.096 | +0.023 |  | -3.8 / -1.2 |  |
| MES | 5 | eod | -0.042 | -0.408 .. +0.323 | -0.0023 | 0.82 / 0.82 / 0.83 | 0.833 |  |  | 11/16 | -0.083 | -0.002 |  | -0.9 / -0.2 |  |
| MES | 15 | h1 | -0.003 | -0.012 .. +0.007 | -0.0026 | 0.6 / 0.58 / 0.55 | 0.548 |  |  | 10/16 | -0.005 | -0.000 |  | -0.6 / -0.5 |  |
| MES | 15 | h2 | -0.005 | -0.020 .. +0.011 | -0.0022 | 0.53 / 0.52 / 0.55 | 0.543 |  |  | 11/16 | -0.014 | +0.004 |  | -0.8 / -0.6 |  |
| MES | 15 | h4 | -0.009 | -0.040 .. +0.023 | -0.0032 | 0.59 / 0.58 / 0.59 | 0.593 |  |  | 9/16 | -0.026 | +0.008 |  | -0.9 / -0.5 | 0.045 |
| MES | 15 | h8 | -0.001 | -0.053 .. +0.051 | -0.0030 | 0.97 / 0.97 / 0.98 | 0.976 |  |  | 7/16 | -0.036 | +0.034 |  | -0.1 / -0.0 |  |
| MES | 15 | h16 | -0.006 | -0.098 .. +0.087 | -0.0008 | 0.9 / 0.91 / 0.92 | 0.921 |  |  | 7/16 | -0.093 | +0.081 |  | -0.3 / -0.1 |  |
| MES | 15 | eod * | +0.158 | -0.311 .. +0.627 | +0.0119 | 0.51 / 0.49 / 0.42 | 0.426 | 1 | 1 | 6/16 | -0.051 | +0.366 | False | +3.1 / +0.7 |  |
| MES | 60 | h1 | +0.005 | -0.011 .. +0.020 | +0.0050 | 0.55 / 0.56 / 0.59 | 0.589 |  |  | 8/16 | -0.011 | +0.020 |  | +0.6 / +0.6 |  |
| MES | 60 | h2 | +0.004 | -0.027 .. +0.034 | +0.0043 | 0.81 / 0.81 / 0.82 | 0.824 |  |  | 7/16 | -0.025 | +0.032 |  | +0.3 / +0.2 |  |
| MES | 60 | h4 * | +0.018 | -0.039 .. +0.075 | +0.0052 | 0.53 / 0.54 / 0.57 | 0.563 | 1 | 1 | 10/16 | -0.023 | +0.059 | False | +1.1 / +0.6 | 0.087 |
| MES | 60 | h8 | +0.007 | -0.096 .. +0.110 | +0.0007 | 0.89 / 0.89 / 0.9 | 0.896 |  |  | 7/16 | -0.074 | +0.089 |  | +0.3 / +0.1 |  |
| MES | 60 | h16 | -0.032 | -0.207 .. +0.142 | -0.0045 | 0.72 / 0.71 / 0.74 | 0.744 |  |  | 8/16 | -0.153 | +0.088 |  | -1.1 / -0.4 |  |
| MES | 60 | eod | -0.064 | -0.257 .. +0.128 | -0.0075 | 0.51 / 0.51 / 0.55 | 0.549 |  |  | 9/16 | -0.168 | +0.039 |  | -2.0 / -0.7 |  |
| MNQ | 5 | h1 * | +0.004 | -0.000 .. +0.009 | +0.0039 | 0.054 / 0.062 / 0.12 | 0.125 | 1 | 1 | 10/16 | -0.001 | +0.010 | False | +1.6 / +1.9 |  |
| MNQ | 5 | h2 | +0.004 | -0.006 .. +0.013 | +0.0015 | 0.45 / 0.45 / 0.56 | 0.546 |  |  | 8/16 | -0.009 | +0.016 |  | +0.9 / +0.7 |  |
| MNQ | 5 | h4 | +0.003 | -0.016 .. +0.022 | +0.0009 | 0.75 / 0.75 / 0.8 | 0.791 |  |  | 8/16 | -0.019 | +0.025 |  | +0.6 / +0.3 | 0.032 |
| MNQ | 5 | h8 | -0.013 | -0.053 .. +0.027 | -0.0028 | 0.53 / 0.52 / 0.57 | 0.572 |  |  | 9/16 | -0.045 | +0.020 |  | -1.6 / -0.6 |  |
| MNQ | 5 | h16 | -0.031 | -0.121 .. +0.059 | -0.0033 | 0.5 / 0.47 / 0.43 | 0.416 |  |  | 10/16 | -0.070 | +0.007 |  | -2.5 / -0.7 |  |
| MNQ | 5 | eod | -0.092 | -0.716 .. +0.532 | +0.0014 | 0.77 / 0.77 / 0.74 | 0.749 |  |  | 10/16 | -0.390 | +0.204 |  | -1.3 / -0.3 |  |
| MNQ | 15 | h1 | +0.000 | -0.015 .. +0.016 | -0.0028 | 0.95 / 0.95 / 0.93 | 0.936 |  |  | 9/16 | +0.003 | -0.002 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h2 | +0.008 | -0.014 .. +0.030 | -0.0031 | 0.49 / 0.49 / 0.52 | 0.526 |  |  | 9/16 | +0.002 | +0.013 |  | +0.6 / +0.7 |  |
| MNQ | 15 | h4 | +0.013 | -0.031 .. +0.056 | -0.0059 | 0.56 / 0.57 / 0.59 | 0.582 |  |  | 11/16 | +0.004 | +0.022 |  | +0.6 / +0.6 | 0.053 |
| MNQ | 15 | h8 | +0.002 | -0.069 .. +0.074 | -0.0072 | 0.95 / 0.95 / 0.96 | 0.956 |  |  | 9/16 | -0.017 | +0.021 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h16 | +0.034 | -0.108 .. +0.175 | +0.0053 | 0.64 / 0.64 / 0.63 | 0.611 |  |  | 9/16 | -0.095 | +0.161 |  | +1.1 / +0.5 |  |
| MNQ | 15 | eod * | +0.364 | -0.457 .. +1.185 | +0.0255 | 0.39 / 0.38 / 0.15 | 0.151 | 1 | 1 | 8/16 | +0.077 | +0.649 | False | +4.0 / +0.9 |  |
| MNQ | 60 | h1 * | +0.011 | -0.005 .. +0.027 | +0.0050 | 0.16 / 0.17 / 0.22 | 0.22 | 1 | 1 | 10/16 | +0.003 | +0.020 | False | +1.3 / +1.4 |  |
| MNQ | 60 | h2 | +0.018 | -0.013 .. +0.048 | +0.0051 | 0.26 / 0.29 / 0.33 | 0.326 |  |  | 11/16 | +0.007 | +0.028 |  | +1.4 / +1.1 |  |
| MNQ | 60 | h4 | +0.024 | -0.034 .. +0.081 | +0.0046 | 0.42 / 0.44 / 0.47 | 0.488 |  |  | 11/16 | -0.001 | +0.048 |  | +1.3 / +0.8 | 0.092 |
| MNQ | 60 | h8 | +0.019 | -0.081 .. +0.120 | +0.0018 | 0.71 / 0.72 / 0.74 | 0.738 |  |  | 9/16 | -0.014 | +0.053 |  | +0.8 / +0.4 |  |
| MNQ | 60 | h16 | -0.027 | -0.204 .. +0.150 | -0.0055 | 0.77 / 0.78 / 0.8 | 0.801 |  |  | 8/16 | -0.043 | -0.010 |  | -0.8 / -0.3 |  |
| MNQ | 60 | eod | -0.082 | -0.277 .. +0.114 | -0.0118 | 0.41 / 0.43 / 0.48 | 0.477 |  |  | 10/16 | -0.069 | -0.094 |  | -2.4 / -0.8 |  |
| MYM | 5 | h1 | -0.006 | -0.014 .. +0.001 | +0.0002 | 0.092 / 0.08 / 0.13 | 0.131 |  |  | 4/8 | n/a | -0.006 |  | -1.3 / -1.7 |  |
| MYM | 5 | h2 | -0.013 | -0.026 .. +0.001 | -0.0032 | 0.069 / 0.055 / 0.17 | 0.17 |  |  | 6/8 | n/a | -0.013 |  | -2.0 / -1.8 |  |
| MYM | 5 | h4 | -0.016 | -0.044 .. +0.011 | -0.0027 | 0.24 / 0.22 / 0.38 | 0.374 |  |  | 6/8 | n/a | -0.016 |  | -1.6 / -1.2 | 0.045 |
| MYM | 5 | h8 | -0.044 | -0.091 .. +0.002 | -0.0070 | 0.062 / 0.06 / 0.15 | 0.153 |  |  | 7/8 | n/a | -0.044 |  | -3.2 / -1.9 |  |
| MYM | 5 | h16 * | -0.069 | -0.153 .. +0.014 | -0.0079 | 0.1 / 0.11 / 0.19 | 0.199 | 1 | 1 | 6/8 | n/a | -0.069 | False | -4.1 / -1.6 |  |
| MYM | 5 | eod | +0.104 | -0.825 .. +1.033 | +0.0092 | 0.83 / 0.83 / 0.77 | 0.783 |  |  | 3/8 | n/a | +0.104 |  | +1.1 / +0.2 |  |
| MYM | 15 | h1 | -0.001 | -0.014 .. +0.011 | -0.0022 | 0.82 / 0.84 / 0.85 | 0.849 |  |  | 4/8 | n/a | -0.001 |  | -0.2 / -0.2 |  |
| MYM | 15 | h2 | +0.009 | -0.028 .. +0.046 | +0.0027 | 0.63 / 0.65 / 0.59 | 0.592 |  |  | 4/8 | n/a | +0.009 |  | +0.5 / +0.5 |  |
| MYM | 15 | h4 | +0.026 | -0.054 .. +0.105 | +0.0035 | 0.53 / 0.55 / 0.42 | 0.423 |  |  | 4/8 | n/a | +0.026 |  | +0.8 / +0.6 | 0.078 |
| MYM | 15 | h8 | +0.049 | -0.106 .. +0.204 | +0.0115 | 0.53 / 0.55 / 0.41 | 0.425 |  |  | 4/8 | n/a | +0.049 |  | +1.3 / +0.6 |  |
| MYM | 15 | h16 | +0.161 | -0.235 .. +0.556 | +0.0354 | 0.43 / 0.44 / 0.13 | 0.125 |  |  | 3/8 | n/a | +0.161 |  | +3.0 / +0.8 |  |
| MYM | 15 | eod * | +0.581 | -0.602 .. +1.763 | +0.0422 | 0.34 / 0.34 / 0.077 | 0.0669 | 1 | 1 | 4/8 | n/a | +0.581 | False | +4.7 / +1.0 |  |
| MYM | 60 | h1 | +0.001 | -0.023 .. +0.026 | +0.0075 | 0.92 / 0.92 / 0.92 | 0.919 |  |  | 6/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 60 | h2 | +0.001 | -0.047 .. +0.049 | +0.0085 | 0.96 / 0.96 / 0.96 | 0.959 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.0 |  |
| MYM | 60 | h4 | +0.020 | -0.066 .. +0.107 | +0.0114 | 0.64 / 0.64 / 0.65 | 0.648 |  |  | 5/8 | n/a | +0.020 |  | +0.8 / +0.5 | 0.125 |
| MYM | 60 | h8 * | +0.079 | -0.075 .. +0.232 | +0.0155 | 0.32 / 0.3 / 0.32 | 0.329 | 1 | 1 | 6/8 | n/a | +0.079 | False | +2.4 / +1.0 |  |
| MYM | 60 | h16 | +0.107 | -0.151 .. +0.365 | +0.0145 | 0.42 / 0.4 / 0.43 | 0.421 |  |  | 5/8 | n/a | +0.107 |  | +2.4 / +0.8 |  |
| MYM | 60 | eod | +0.106 | -0.183 .. +0.395 | +0.0145 | 0.47 / 0.45 / 0.48 | 0.48 |  |  | 3/8 | n/a | +0.106 |  | +2.3 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.029 | -0.034 .. -0.024 | -5.8% | -0.054 | 1.1e-28 | 7.59e-26 | 15/16 |
| MES | 5 | h2 | -0.037 | -0.045 .. -0.029 | -5.3% | -0.074 | 1.8e-20 |  | 13/16 |
| MES | 5 | h4 | -0.050 | -0.063 .. -0.036 | -5.0% | -0.101 | 3.1e-13 |  | 13/16 |
| MES | 5 | h8 | -0.059 | -0.082 .. -0.036 | -4.1% | -0.125 | 2.8e-07 |  | 13/16 |
| MES | 5 | h16 | -0.077 | -0.113 .. -0.040 | -3.7% | -0.141 | 3.7e-05 |  | 14/16 |
| MES | 5 | eod | -0.146 | -0.390 .. +0.098 | -1.5% | -0.314 | 0.24 |  | 11/16 |
| MES | 15 | h1 * | -0.035 | -0.043 .. -0.026 | -6.8% | -0.071 | 8.6e-16 | 3.66e-13 | 14/16 |
| MES | 15 | h2 | -0.046 | -0.061 .. -0.031 | -6.3% | -0.092 | 2e-09 |  | 13/16 |
| MES | 15 | h4 | -0.054 | -0.079 .. -0.029 | -5.1% | -0.117 | 2.8e-05 |  | 12/16 |
| MES | 15 | h8 | -0.065 | -0.107 .. -0.024 | -4.3% | -0.141 | 0.0019 |  | 10/16 |
| MES | 15 | h16 | -0.073 | -0.140 .. -0.006 | -3.2% | -0.173 | 0.034 |  | 9/16 |
| MES | 15 | eod | -0.124 | -0.489 .. +0.240 | -2.3% | -0.296 | 0.5 |  | 9/16 |
| MES | 60 | h1 * | -0.044 | -0.057 .. -0.030 | -8.5% | -0.099 | 6e-10 | 1.86e-07 | 13/16 |
| MES | 60 | h2 | -0.059 | -0.081 .. -0.037 | -8.0% | -0.129 | 1.3e-07 |  | 13/16 |
| MES | 60 | h4 | -0.087 | -0.125 .. -0.050 | -8.2% | -0.171 | 5.8e-06 |  | 13/16 |
| MES | 60 | h8 | -0.110 | -0.171 .. -0.049 | -7.3% | -0.221 | 0.00044 |  | 14/16 |
| MES | 60 | h16 | -0.123 | -0.233 .. -0.012 | -6.0% | -0.260 | 0.029 |  | 12/16 |
| MES | 60 | eod | -0.115 | -0.245 .. +0.016 | -5.3% | -0.261 | 0.084 |  | 11/16 |
| MNQ | 5 | h1 * | -0.027 | -0.032 .. -0.022 | -5.1% | -0.051 | 4.3e-24 | 2.6e-21 | 14/16 |
| MNQ | 5 | h2 | -0.032 | -0.040 .. -0.024 | -4.2% | -0.069 | 4e-11 |  | 14/16 |
| MNQ | 5 | h4 | -0.042 | -0.056 .. -0.028 | -3.8% | -0.089 | 1.5e-06 |  | 14/16 |
| MNQ | 5 | h8 | -0.044 | -0.071 .. -0.018 | -2.7% | -0.102 | 0.0042 |  | 13/16 |
| MNQ | 5 | h16 | -0.049 | -0.092 .. -0.006 | -2.1% | -0.097 | 0.078 |  | 13/16 |
| MNQ | 5 | eod | -0.331 | -0.806 .. +0.145 | -2.6% | -0.469 | 0.18 |  | 10/16 |
| MNQ | 15 | h1 * | -0.030 | -0.042 .. -0.017 | -5.6% | -0.065 | 5.1e-06 | 0.0012 | 14/16 |
| MNQ | 15 | h2 | -0.048 | -0.082 .. -0.014 | -6.2% | -0.102 | 0.0053 |  | 13/16 |
| MNQ | 15 | h4 | -0.070 | -0.159 .. +0.018 | -6.2% | -0.163 | 0.12 |  | 11/16 |
| MNQ | 15 | h8 | -0.097 | -0.252 .. +0.059 | -5.8% | -0.266 | 0.22 |  | 9/16 |
| MNQ | 15 | h16 | -0.094 | -0.269 .. +0.080 | -3.7% | -0.416 | 0.29 |  | 8/16 |
| MNQ | 15 | eod | -0.412 | -1.259 .. +0.435 | -6.5% | -0.630 | 0.34 |  | 10/16 |
| MNQ | 60 | h1 * | -0.038 | -0.052 .. -0.024 | -7.1% | -0.088 | 1.3e-07 | 3.35e-05 | 13/16 |
| MNQ | 60 | h2 | -0.050 | -0.073 .. -0.028 | -6.6% | -0.115 | 9.9e-06 |  | 13/16 |
| MNQ | 60 | h4 | -0.071 | -0.109 .. -0.034 | -6.5% | -0.152 | 0.0002 |  | 13/16 |
| MNQ | 60 | h8 | -0.120 | -0.183 .. -0.058 | -7.6% | -0.226 | 0.00016 |  | 13/16 |
| MNQ | 60 | h16 | -0.168 | -0.275 .. -0.060 | -7.6% | -0.338 | 0.0027 |  | 11/16 |
| MNQ | 60 | eod | -0.153 | -0.276 .. -0.030 | -6.6% | -0.338 | 0.018 |  | 11/16 |
| MYM | 5 | h1 * | -0.033 | -0.044 .. -0.023 | -6.3% | -0.060 | 1.9e-09 | 5.54e-07 | 7/8 |
| MYM | 5 | h2 | -0.039 | -0.053 .. -0.025 | -5.1% | -0.081 | 2.7e-08 |  | 7/8 |
| MYM | 5 | h4 | -0.053 | -0.079 .. -0.026 | -4.8% | -0.107 | 0.00012 |  | 7/8 |
| MYM | 5 | h8 | -0.055 | -0.094 .. -0.015 | -3.4% | -0.126 | 0.01 |  | 7/8 |
| MYM | 5 | h16 | -0.047 | -0.108 .. +0.014 | -2.0% | -0.121 | 0.21 |  | 5/8 |
| MYM | 5 | eod | -0.426 | -1.146 .. +0.293 | -3.6% | -0.744 | 0.25 |  | 5/8 |
| MYM | 15 | h1 * | -0.041 | -0.062 .. -0.020 | -7.8% | -0.087 | 0.0001 | 0.021 | 8/8 |
| MYM | 15 | h2 | -0.073 | -0.130 .. -0.016 | -9.6% | -0.144 | 0.012 |  | 7/8 |
| MYM | 15 | h4 | -0.121 | -0.248 .. +0.007 | -10.8% | -0.242 | 0.07 |  | 7/8 |
| MYM | 15 | h8 | -0.194 | -0.399 .. +0.012 | -11.8% | -0.429 | 0.072 |  | 6/8 |
| MYM | 15 | h16 | -0.292 | -0.672 .. +0.088 | -11.9% | -0.677 | 0.14 |  | 6/8 |
| MYM | 15 | eod | -0.532 | -1.594 .. +0.531 | -8.8% | -0.941 | 0.33 |  | 4/8 |
| MYM | 60 | h1 * | -0.025 | -0.046 .. -0.005 | -4.8% | -0.074 | 0.017 | 1 | 6/8 |
| MYM | 60 | h2 | -0.027 | -0.061 .. +0.007 | -3.6% | -0.096 | 0.11 |  | 6/8 |
| MYM | 60 | h4 | -0.052 | -0.107 .. +0.004 | -4.8% | -0.134 | 0.066 |  | 6/8 |
| MYM | 60 | h8 | -0.056 | -0.150 .. +0.038 | -3.6% | -0.143 | 0.25 |  | 5/8 |
| MYM | 60 | h16 | -0.068 | -0.230 .. +0.094 | -3.2% | -0.165 | 0.47 |  | 4/8 |
| MYM | 60 | eod | -0.078 | -0.269 .. +0.112 | -3.5% | -0.180 | 0.5 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.77 pts | -1.29 .. -0.25 | 0.01 |
| MES | 15 | -0.48 pts | -1.38 .. +0.42 | 0.31 |
| MES | 60 | +0.73 pts | -1.26 .. +2.73 | 0.49 |
| MNQ | 5 | -0.57 pts | -1.14 .. -0.00 | 0.049 |
| MNQ | 15 | -0.09 pts | -1.04 .. +0.85 | 0.85 |
| MNQ | 60 | +1.45 pts | -0.48 .. +3.38 | 0.15 |
| MYM | 5 | -0.37 pts | -1.04 .. +0.30 | 0.32 |
| MYM | 15 | +0.09 pts | -1.09 .. +1.27 | 0.94 |
| MYM | 60 | +0.85 pts | -1.89 .. +3.59 | 0.69 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207180 | +0.002 | 0.282 | +0.03 | -3.47 | -3.48 | -3.47 | -3.48 |
| MES | 5 | h2 | bottom fifth | long | 207180 | +0.004 | 0.282 | +0.02 | -3.48 | -3.46 | -3.50 | -3.49 |
| MES | 5 | h4 | bottom fifth | long | 207180 | +0.007 | 0.282 | +0.02 | -3.48 | -3.40 | -3.56 | -3.50 |
| MES | 5 | h8 | bottom fifth | long | 207180 | +0.013 | 0.282 | +0.06 | -3.44 | -3.28 | -3.59 | -3.51 |
| MES | 5 | h16 | bottom fifth | long | 207180 | +0.034 | 0.282 | +0.31 | -3.19 | -3.07 | -3.30 | -3.42 |
| MES | 5 | eod | bottom fifth | long | 207180 | +0.180 | 0.282 | +2.30 | -1.20 | -0.90 | -1.47 | -0.01 |
| MES | 15 | h1 | bottom fifth | long | 68370 | +0.005 | 0.162 | +0.07 | -3.43 | -3.46 | -3.40 | -3.50 |
| MES | 15 | h2 | bottom fifth | long | 68370 | +0.010 | 0.162 | +0.19 | -3.31 | -3.38 | -3.24 | -3.41 |
| MES | 15 | h4 | bottom fifth | long | 68370 | +0.022 | 0.162 | +0.37 | -3.13 | -3.20 | -3.06 | -3.28 |
| MES | 15 | h8 | bottom fifth | long | 68370 | +0.024 | 0.162 | +0.50 | -3.00 | -2.96 | -3.02 | -3.15 |
| MES | 15 | h16 | bottom fifth | long | 68370 | +0.037 | 0.162 | +0.88 | -2.62 | -2.40 | -2.83 | -2.54 |
| MES | 15 | eod | top fifth | long | 68369 | +0.238 | 0.195 | +2.80 | -0.70 | -0.01 | -1.31 | -3.66 |
| MES | 60 | h1 | top fifth | long | 16621 | +0.010 | 0.103 | +0.24 | -3.26 | -3.23 | -3.28 | -3.46 |
| MES | 60 | h2 | top fifth | long | 16621 | +0.021 | 0.103 | +0.55 | -2.95 | -3.00 | -2.90 | -3.39 |
| MES | 60 | h4 | top fifth | long | 16621 | +0.042 | 0.103 | +1.32 | -2.18 | -2.49 | -1.90 | -3.05 |
| MES | 60 | h8 | top fifth | long | 16621 | +0.058 | 0.103 | +2.34 | -1.16 | -2.14 | -0.27 | -2.78 |
| MES | 60 | h16 | bottom fifth | long | 16621 | +0.069 | 0.080 | +2.99 | -0.51 | -0.26 | -0.75 | -2.95 |
| MES | 60 | eod | bottom fifth | long | 16621 | +0.108 | 0.080 | +5.30 | +1.80 | +0.32 | +3.20 | -1.58 |
| MNQ | 5 | h1 | top fifth | long | 206830 | +0.005 | 0.140 | +0.06 | -1.94 | -1.99 | -1.88 | -1.97 |
| MNQ | 5 | h2 | top fifth | long | 206830 | +0.010 | 0.140 | +0.13 | -1.87 | -1.97 | -1.76 | -1.92 |
| MNQ | 5 | h4 | top fifth | long | 206830 | +0.018 | 0.140 | +0.22 | -1.78 | -1.93 | -1.61 | -1.89 |
| MNQ | 5 | h8 | bottom fifth | long | 206830 | +0.023 | 0.119 | +0.20 | -1.80 | -1.89 | -1.71 | -1.74 |
| MNQ | 5 | h16 | bottom fifth | long | 206830 | +0.065 | 0.119 | +0.40 | -1.60 | -1.67 | -1.53 | -1.68 |
| MNQ | 5 | eod | bottom fifth | long | 206830 | +0.334 | 0.119 | +2.21 | +0.21 | +1.13 | -0.79 | +5.64 |
| MNQ | 15 | h1 | top fifth | long | 68338 | +0.009 | 0.082 | +0.11 | -1.89 | -1.90 | -1.88 | -1.97 |
| MNQ | 15 | h2 | top fifth | long | 68338 | +0.018 | 0.082 | +0.32 | -1.68 | -1.77 | -1.59 | -1.82 |
| MNQ | 15 | h4 | top fifth | long | 68338 | +0.031 | 0.082 | +0.61 | -1.39 | -1.55 | -1.22 | -1.70 |
| MNQ | 15 | h8 | top fifth | long | 68338 | +0.043 | 0.082 | +0.65 | -1.35 | -1.29 | -1.42 | -2.05 |
| MNQ | 15 | h16 | top fifth | long | 68338 | +0.094 | 0.082 | +1.80 | -0.20 | -0.81 | +0.42 | -1.67 |
| MNQ | 15 | eod | top fifth | long | 68338 | +0.387 | 0.082 | +2.76 | +0.76 | +1.45 | +0.06 | -3.59 |
| MNQ | 60 | h1 | top fifth | long | 16620 | +0.020 | 0.042 | +0.75 | -1.25 | -1.57 | -0.94 | -1.80 |
| MNQ | 60 | h2 | top fifth | long | 16620 | +0.037 | 0.042 | +1.43 | -0.57 | -1.26 | +0.11 | -1.61 |
| MNQ | 60 | h4 | top fifth | long | 16620 | +0.070 | 0.042 | +2.75 | +0.75 | -0.85 | +2.34 | -1.12 |
| MNQ | 60 | h8 | top fifth | long | 16620 | +0.094 | 0.042 | +3.64 | +1.64 | -0.74 | +4.01 | -1.09 |
| MNQ | 60 | h16 | bottom fifth | long | 16620 | +0.101 | 0.031 | +6.11 | +4.11 | +1.25 | +6.78 | +1.43 |
| MNQ | 60 | eod | bottom fifth | long | 16620 | +0.147 | 0.031 | +9.98 | +7.98 | +1.86 | +13.67 | +4.24 |
| MYM | 5 | h1 | bottom fifth | long | 103771 | -0.000 | 0.155 | +0.03 | -1.97 | +nan | -1.97 | -1.95 |
| MYM | 5 | h2 | top fifth | short | 103771 | +0.009 | 0.175 | +0.03 | -1.97 | +nan | -1.97 | -1.95 |
| MYM | 5 | h4 | top fifth | short | 103771 | +0.012 | 0.175 | -0.02 | -2.02 | +nan | -2.02 | -1.93 |
| MYM | 5 | h8 | top fifth | short | 103771 | +0.030 | 0.175 | +0.06 | -1.94 | +nan | -1.94 | -1.71 |
| MYM | 5 | h16 | bottom fifth | long | 103771 | -0.029 | 0.155 | +0.10 | -1.90 | +nan | -1.90 | -1.41 |
| MYM | 5 | eod | top fifth | long | 103771 | +0.195 | 0.175 | +3.26 | +1.26 | +nan | +1.26 | -1.03 |
| MYM | 15 | h1 | bottom fifth | long | 34249 | -0.003 | 0.085 | +0.04 | -1.96 | +nan | -1.96 | -1.91 |
| MYM | 15 | h2 | top fifth | long | 34248 | +0.002 | 0.102 | -0.07 | -2.07 | +nan | -2.07 | -2.20 |
| MYM | 15 | h4 | top fifth | long | 34248 | +0.004 | 0.102 | -0.11 | -2.11 | +nan | -2.11 | -2.33 |
| MYM | 15 | h8 | top fifth | long | 34248 | +0.006 | 0.102 | -0.23 | -2.23 | +nan | -2.23 | -2.53 |
| MYM | 15 | h16 | top fifth | long | 34248 | +0.016 | 0.102 | +0.03 | -1.97 | +nan | -1.97 | -2.55 |
| MYM | 15 | eod | top fifth | long | 34248 | +0.171 | 0.102 | +3.35 | +1.35 | +nan | +1.35 | -0.66 |
| MYM | 60 | h1 | top fifth | long | 8300 | +0.015 | 0.052 | +0.23 | -1.77 | +nan | -1.77 | -2.01 |
| MYM | 60 | h2 | top fifth | long | 8300 | +0.027 | 0.052 | +0.34 | -1.66 | +nan | -1.66 | -2.18 |
| MYM | 60 | h4 | top fifth | long | 8300 | +0.066 | 0.052 | +1.72 | -0.28 | +nan | -0.28 | -1.39 |
| MYM | 60 | h8 | top fifth | long | 8300 | +0.129 | 0.052 | +3.62 | +1.62 | +nan | +1.62 | -0.09 |
| MYM | 60 | h16 | top fifth | long | 8300 | +0.171 | 0.052 | +4.67 | +2.67 | +nan | +2.67 | -0.22 |
| MYM | 60 | eod | top fifth | long | 8300 | +0.193 | 0.052 | +5.14 | +3.14 | +nan | +3.14 | -0.42 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -2.843 | -2.114 | -0.839 | -0.252 | -0.083 | +0.000 | -0.006 | -0.009 | -0.015 | -0.030 | -0.043 |
| MES | 15 | -2.921 | -2.147 | -0.878 | -0.268 | -0.089 | +0.000 | -0.004 | -0.007 | -0.012 | -0.004 | -0.019 |
| MES | 60 | -3.483 | -2.486 | -1.034 | -0.320 | -0.110 | +0.000 | +0.004 | +0.001 | +0.015 | +0.014 | -0.065 |
| MNQ | 5 | -3.155 | -2.332 | -0.938 | -0.288 | -0.099 | +0.000 | +0.002 | -0.001 | -0.001 | -0.018 | -0.039 |
| MNQ | 15 | -3.137 | -2.263 | -0.936 | -0.296 | -0.101 | +0.000 | +0.006 | +0.013 | +0.018 | +0.009 | +0.038 |
| MNQ | 60 | -3.732 | -2.630 | -1.105 | -0.351 | -0.119 | +0.000 | +0.010 | +0.015 | +0.017 | +0.008 | -0.019 |
| MYM | 5 | -3.051 | -2.280 | -0.916 | -0.277 | -0.092 | +0.000 | -0.006 | -0.013 | -0.017 | -0.043 | -0.074 |
| MYM | 15 | -3.027 | -2.244 | -0.934 | -0.296 | -0.102 | +0.000 | +0.015 | +0.027 | +0.049 | +0.078 | +0.219 |
| MYM | 60 | -3.529 | -2.610 | -1.099 | -0.337 | -0.113 | +0.000 | +0.000 | -0.005 | +0.020 | +0.067 | +0.021 |

## Calibration

- MES 5-min: 1035899 bars, 207180 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341846 bars, 68369 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83102 bars, 16621 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034150 bars, 206830 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341690 bars, 68338 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83100 bars, 16620 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518853 bars, 103771 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171241 bars, 34248 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41499 bars, 8300 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
