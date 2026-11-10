# Impact card: swing_break

first close above the last swing high (long) / below the last swing low (short) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.024 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.019 R20 or more 80% of the time).
- MES 5-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.041 R20, CONFIRMED, q=3.2e-40, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.36 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.221 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.028 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 15-min size: the market moves 9% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.044 R20, CONFIRMED, q=1.86e-13, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.72 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.130 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.009 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.074 R20 or more 80% of the time).
- MES 60-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.062 R20, CONFIRMED, q=2.17e-06, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.50 at recent bar sizes, 90% range up to $3.70); about 1.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: POSSIBLE direction effect +0.012 average bars (~$0.30 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.169, replicated in the other half=False, 14 of 16 years); best leg (event, with signal) grosses $+0.10 and nets $-1.90 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.044 R20, CONFIRMED, q=2.3e-48, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.30 at recent bar sizes, 90% range up to $0.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.013 R20 over the next 1 bar (15 min), p=0.54; we would catch an effect of 0.052 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 10% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.053 R20, CONFIRMED, q=1.98e-21, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.57 at recent bar sizes, 90% range up to $2.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.035 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.077 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 12% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.092 R20, CONFIRMED, q=2.24e-08, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.03 at recent bar sizes, 90% range up to $8.30); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.014 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MYM 5-min size: the market moves 7% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.053 R20, CONFIRMED, q=4.37e-14, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.16 at recent bar sizes, 90% range up to $0.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.015 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.057 R20 or more 80% of the time).
- MYM 15-min size: the market moves 13% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.068 R20, CONFIRMED, q=3.93e-05, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.48 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.100 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.089 R20 over the next 4 bars (4 h), p=0.11; we would catch an effect of 0.101 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.19).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.70 at recent bar sizes, 90% range up to $8.29); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.009 .. +0.005 | -0.0007 | 0.56 / 0.58 / 0.55 | 0.553 |  |  | 6/16 | +0.002 | -0.006 |  | -0.6 / -0.6 |  |
| MES | 5 | h2 | -0.000 | -0.009 .. +0.009 | -0.0000 | 0.98 / 0.98 / 0.98 | 0.983 |  |  | 5/16 | +0.003 | -0.004 |  | -0.0 / -0.0 |  |
| MES | 5 | h4 | +0.003 | -0.010 .. +0.017 | +0.0005 | 0.64 / 0.64 / 0.64 | 0.641 |  |  | 11/16 | +0.009 | -0.002 |  | +0.5 / +0.5 | 0.019 |
| MES | 5 | h8 | -0.001 | -0.021 .. +0.020 | -0.0001 | 0.96 / 0.96 / 0.98 | 0.975 |  |  | 6/16 | -0.010 | +0.009 |  | -0.1 / -0.0 |  |
| MES | 5 | h16 * | -0.024 | -0.055 .. +0.008 | -0.0018 | 0.15 / 0.14 / 0.16 | 0.158 | 1 | 1 | 11/16 | -0.031 | -0.016 | False | -1.7 / -1.4 |  |
| MES | 5 | eod | -0.032 | -0.189 .. +0.125 | -0.0005 | 0.69 / 0.7 / 0.73 | 0.732 |  |  | 9/16 | -0.057 | -0.008 |  | -0.5 / -0.4 |  |
| MES | 15 | h1 | +0.004 | -0.008 .. +0.015 | +0.0011 | 0.54 / 0.57 / 0.58 | 0.57 |  |  | 7/16 | -0.006 | +0.013 |  | +0.6 / +0.6 |  |
| MES | 15 | h2 | +0.007 | -0.011 .. +0.025 | +0.0015 | 0.46 / 0.46 / 0.47 | 0.47 |  |  | 10/16 | -0.017 | +0.031 |  | +0.7 / +0.7 |  |
| MES | 15 | h4 | -0.006 | -0.033 .. +0.022 | -0.0009 | 0.68 / 0.68 / 0.68 | 0.676 |  |  | 7/16 | -0.026 | +0.015 |  | -0.4 / -0.4 | 0.038 |
| MES | 15 | h8 * | -0.028 | -0.071 .. +0.014 | -0.0029 | 0.19 / 0.18 / 0.18 | 0.182 | 1 | 1 | 10/16 | -0.053 | -0.004 | False | -1.4 / -1.3 |  |
| MES | 15 | h16 | -0.016 | -0.076 .. +0.044 | -0.0010 | 0.61 / 0.6 / 0.61 | 0.609 |  |  | 8/16 | -0.073 | +0.041 |  | -0.6 / -0.5 |  |
| MES | 15 | eod | +0.079 | -0.069 .. +0.226 | +0.0022 | 0.3 / 0.29 / 0.34 | 0.347 |  |  | 9/16 | +0.064 | +0.093 |  | +1.4 / +1.0 |  |
| MES | 60 | h1 | +0.007 | -0.019 .. +0.033 | +0.0023 | 0.6 / 0.63 / 0.6 | 0.603 |  |  | 8/16 | +0.004 | +0.010 |  | +0.5 / +0.5 |  |
| MES | 60 | h2 * | +0.009 | -0.027 .. +0.045 | +0.0022 | 0.61 / 0.62 / 0.62 | 0.621 | 1 | 1 | 9/16 | +0.034 | -0.016 | False | +0.5 / +0.5 |  |
| MES | 60 | h4 | -0.004 | -0.052 .. +0.044 | -0.0007 | 0.87 / 0.88 / 0.88 | 0.89 |  |  | 10/16 | +0.024 | -0.032 |  | -0.2 / -0.2 | 0.074 |
| MES | 60 | h8 | -0.009 | -0.077 .. +0.060 | -0.0011 | 0.8 / 0.81 / 0.81 | 0.821 |  |  | 7/16 | +0.013 | -0.030 |  | -0.3 / -0.2 |  |
| MES | 60 | h16 | -0.001 | -0.086 .. +0.083 | -0.0003 | 0.98 / 0.98 / 0.98 | 0.981 |  |  | 7/16 | +0.023 | -0.025 |  | -0.0 / -0.0 |  |
| MES | 60 | eod | -0.001 | -0.087 .. +0.085 | -0.0003 | 0.99 / 0.99 / 0.99 | 0.988 |  |  | 6/16 | +0.044 | -0.045 |  | -0.0 / -0.0 |  |
| MNQ | 5 | h1 * | +0.012 | +0.005 .. +0.019 | +0.0034 | 0.00093 / 0.00098 / 0.0034 | 0.00469 | 0.169 | 0.234 | 14/16 | +0.011 | +0.012 | False | +3.2 / +3.3 |  |
| MNQ | 5 | h2 | +0.012 | +0.002 .. +0.022 | +0.0021 | 0.024 / 0.025 / 0.048 | 0.0518 |  |  | 13/16 | +0.009 | +0.015 |  | +2.3 / +2.3 |  |
| MNQ | 5 | h4 | +0.013 | -0.001 .. +0.028 | +0.0015 | 0.068 / 0.067 / 0.16 | 0.15 |  |  | 11/16 | +0.014 | +0.012 |  | +1.8 / +1.8 | 0.023 |
| MNQ | 5 | h8 | +0.004 | -0.017 .. +0.026 | +0.0003 | 0.71 / 0.71 / 0.77 | 0.756 |  |  | 8/16 | +0.010 | -0.002 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h16 | -0.015 | -0.049 .. +0.018 | -0.0009 | 0.37 / 0.37 / 0.51 | 0.507 |  |  | 10/16 | -0.017 | -0.014 |  | -1.0 / -0.9 |  |
| MNQ | 5 | eod | -0.066 | -0.261 .. +0.128 | -0.0008 | 0.51 / 0.52 / 0.56 | 0.548 |  |  | 9/16 | -0.188 | +0.055 |  | -0.8 / -0.7 |  |
| MNQ | 15 | h1 * | +0.013 | -0.002 .. +0.028 | +0.0039 | 0.09 / 0.077 / 0.04 | 0.049 | 1 | 1 | 12/16 | +0.004 | +0.022 | False | +1.9 / +1.7 |  |
| MNQ | 15 | h2 | +0.018 | -0.003 .. +0.038 | +0.0029 | 0.091 / 0.084 / 0.11 | 0.11 |  |  | 12/16 | +0.009 | +0.026 |  | +1.8 / +1.7 |  |
| MNQ | 15 | h4 | +0.003 | -0.024 .. +0.031 | +0.0001 | 0.82 / 0.82 / 0.87 | 0.87 |  |  | 10/16 | -0.006 | +0.013 |  | +0.2 / +0.2 | 0.052 |
| MNQ | 15 | h8 | -0.012 | -0.056 .. +0.031 | -0.0011 | 0.59 / 0.58 / 0.67 | 0.652 |  |  | 9/16 | -0.041 | +0.017 |  | -0.6 / -0.5 |  |
| MNQ | 15 | h16 | -0.040 | -0.105 .. +0.024 | -0.0024 | 0.22 / 0.21 / 0.3 | 0.293 |  |  | 9/16 | -0.109 | +0.027 |  | -1.4 / -1.2 |  |
| MNQ | 15 | eod | +0.051 | -0.104 .. +0.205 | +0.0009 | 0.52 / 0.52 / 0.64 | 0.628 |  |  | 10/16 | -0.013 | +0.114 |  | +0.8 / +0.6 |  |
| MNQ | 60 | h1 | +0.010 | -0.019 .. +0.039 | +0.0030 | 0.52 / 0.53 / 0.51 | 0.506 |  |  | 8/16 | -0.014 | +0.033 |  | +0.6 / +0.6 |  |
| MNQ | 60 | h2 | -0.007 | -0.046 .. +0.033 | -0.0015 | 0.74 / 0.75 / 0.74 | 0.743 |  |  | 8/16 | -0.017 | +0.003 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h4 * | -0.035 | -0.090 .. +0.021 | -0.0055 | 0.22 / 0.23 / 0.21 | 0.208 | 1 | 1 | 12/16 | -0.056 | -0.013 | False | -1.2 / -1.2 | 0.077 |
| MNQ | 60 | h8 | -0.034 | -0.105 .. +0.038 | -0.0040 | 0.36 / 0.36 / 0.38 | 0.365 |  |  | 10/16 | -0.042 | -0.026 |  | -0.9 / -0.9 |  |
| MNQ | 60 | h16 | -0.006 | -0.096 .. +0.084 | -0.0007 | 0.89 / 0.89 / 0.89 | 0.89 |  |  | 9/16 | -0.007 | -0.005 |  | -0.1 / -0.1 |  |
| MNQ | 60 | eod | -0.003 | -0.096 .. +0.091 | -0.0004 | 0.96 / 0.96 / 0.96 | 0.954 |  |  | 10/16 | +0.014 | -0.020 |  | -0.1 / -0.1 |  |
| MYM | 5 | h1 * | +0.014 | -0.007 .. +0.035 | +0.0039 | 0.19 / 0.19 / 0.03 | 0.04 | 1 | 1 | 5/8 | n/a | +0.014 | False | +1.3 / +1.3 |  |
| MYM | 5 | h2 | +0.005 | -0.010 .. +0.020 | +0.0007 | 0.55 / 0.54 / 0.57 | 0.538 |  |  | 5/8 | n/a | +0.005 |  | +0.6 / +0.6 |  |
| MYM | 5 | h4 | +0.010 | -0.016 .. +0.036 | +0.0010 | 0.44 / 0.44 / 0.52 | 0.491 |  |  | 5/8 | n/a | +0.010 |  | +0.8 / +0.8 | 0.035 |
| MYM | 5 | h8 | -0.012 | -0.043 .. +0.019 | -0.0009 | 0.46 / 0.44 / 0.63 | 0.617 |  |  | 5/8 | n/a | -0.012 |  | -0.8 / -0.7 |  |
| MYM | 5 | h16 | -0.039 | -0.081 .. +0.004 | -0.0022 | 0.078 / 0.083 / 0.2 | 0.199 |  |  | 7/8 | n/a | -0.039 |  | -1.8 / -1.8 |  |
| MYM | 5 | eod | -0.197 | -0.429 .. +0.035 | -0.0025 | 0.096 / 0.13 / 0.17 | 0.176 |  |  | 5/8 | n/a | -0.197 |  | -1.8 / -1.7 |  |
| MYM | 15 | h1 * | +0.015 | -0.017 .. +0.046 | +0.0043 | 0.36 / 0.35 / 0.17 | 0.163 | 1 | 1 | 5/8 | n/a | +0.015 | False | +1.0 / +0.9 |  |
| MYM | 15 | h2 | +0.008 | -0.024 .. +0.040 | +0.0012 | 0.62 / 0.61 / 0.68 | 0.653 |  |  | 6/8 | n/a | +0.008 |  | +0.5 / +0.5 |  |
| MYM | 15 | h4 | -0.001 | -0.041 .. +0.040 | -0.0002 | 0.98 / 0.98 / 0.98 | 0.983 |  |  | 5/8 | n/a | -0.001 |  | -0.0 / -0.0 | 0.057 |
| MYM | 15 | h8 | -0.022 | -0.081 .. +0.037 | -0.0016 | 0.47 / 0.49 / 0.59 | 0.579 |  |  | 6/8 | n/a | -0.022 |  | -0.7 / -0.7 |  |
| MYM | 15 | h16 | -0.012 | -0.093 .. +0.070 | -0.0005 | 0.78 / 0.78 / 0.85 | 0.832 |  |  | 5/8 | n/a | -0.012 |  | -0.3 / -0.3 |  |
| MYM | 15 | eod | +0.053 | -0.175 .. +0.280 | +0.0011 | 0.65 / 0.66 / 0.73 | 0.75 |  |  | 5/8 | n/a | +0.053 |  | +0.5 / +0.5 |  |
| MYM | 60 | h1 | -0.019 | -0.056 .. +0.017 | -0.0063 | 0.3 / 0.33 / 0.3 | 0.306 |  |  | 6/8 | n/a | -0.019 |  | -1.0 / -1.0 |  |
| MYM | 60 | h2 | -0.026 | -0.077 .. +0.025 | -0.0059 | 0.32 / 0.35 / 0.33 | 0.332 |  |  | 5/8 | n/a | -0.026 |  | -1.0 / -1.0 |  |
| MYM | 60 | h4 * | -0.089 | -0.162 .. -0.017 | -0.0148 | 0.015 / 0.019 / 0.017 | 0.0174 | 1 | 0.93 | 6/8 | n/a | -0.089 | False | -2.5 / -2.4 | 0.101 |
| MYM | 60 | h8 | -0.115 | -0.215 .. -0.016 | -0.0140 | 0.023 / 0.027 / 0.026 | 0.0263 |  |  | 5/8 | n/a | -0.115 |  | -2.5 / -2.3 |  |
| MYM | 60 | h16 | -0.127 | -0.259 .. +0.004 | -0.0119 | 0.058 / 0.055 / 0.042 | 0.0448 |  |  | 5/8 | n/a | -0.127 |  | -2.3 / -1.9 |  |
| MYM | 60 | eod | -0.143 | -0.283 .. -0.003 | -0.0127 | 0.045 / 0.039 / 0.027 | 0.0311 |  |  | 5/8 | n/a | -0.143 |  | -2.6 / -2.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.041 | +0.035 .. +0.047 | +8.2% | +0.100 | 3.5e-43 | 3.2e-40 | 16/16 |
| MES | 5 | h2 | +0.042 | +0.035 .. +0.049 | +6.0% | +0.108 | 7e-30 |  | 16/16 |
| MES | 5 | h4 | +0.051 | +0.042 .. +0.060 | +5.1% | +0.113 | 8.6e-22 |  | 16/16 |
| MES | 5 | h8 | +0.057 | +0.042 .. +0.073 | +4.0% | +0.124 | 1.5e-12 |  | 16/16 |
| MES | 5 | h16 | +0.065 | +0.045 .. +0.085 | +3.1% | +0.141 | 1.1e-08 |  | 16/16 |
| MES | 5 | eod | +0.155 | +0.012 .. +0.299 | +1.6% | +0.279 | 0.059 |  | 12/16 |
| MES | 15 | h1 * | +0.044 | +0.035 .. +0.054 | +8.7% | +0.113 | 4.3e-16 | 1.86e-13 | 15/16 |
| MES | 15 | h2 | +0.056 | +0.044 .. +0.069 | +7.7% | +0.133 | 4.5e-14 |  | 15/16 |
| MES | 15 | h4 | +0.075 | +0.056 .. +0.093 | +7.1% | +0.152 | 2.5e-11 |  | 15/16 |
| MES | 15 | h8 | +0.083 | +0.059 .. +0.107 | +5.4% | +0.174 | 1.5e-06 |  | 13/16 |
| MES | 15 | h16 | +0.086 | +0.049 .. +0.123 | +3.8% | +0.177 | 2.1e-05 |  | 13/16 |
| MES | 15 | eod | +0.047 | -0.072 .. +0.166 | +0.9% | +0.179 | 0.45 |  | 11/16 |
| MES | 60 | h1 * | +0.062 | +0.043 .. +0.082 | +12.2% | +0.106 | 7.5e-09 | 2.17e-06 | 14/16 |
| MES | 60 | h2 | +0.063 | +0.038 .. +0.088 | +8.5% | +0.121 | 5.2e-06 |  | 14/16 |
| MES | 60 | h4 | +0.050 | +0.018 .. +0.083 | +4.7% | +0.125 | 0.018 |  | 11/16 |
| MES | 60 | h8 | +0.067 | +0.025 .. +0.108 | +4.4% | +0.134 | 0.0058 |  | 15/16 |
| MES | 60 | h16 | +0.070 | +0.021 .. +0.118 | +3.4% | +0.127 | 0.0052 |  | 13/16 |
| MES | 60 | eod | +0.051 | +0.000 .. +0.102 | +2.4% | +0.117 | 0.049 |  | 13/16 |
| MNQ | 5 | h1 * | +0.044 | +0.039 .. +0.050 | +8.3% | +0.107 | 2.2e-51 | 2.3e-48 | 16/16 |
| MNQ | 5 | h2 | +0.050 | +0.042 .. +0.059 | +6.5% | +0.115 | 1.5e-30 |  | 15/16 |
| MNQ | 5 | h4 | +0.065 | +0.051 .. +0.079 | +5.9% | +0.133 | 1.3e-09 |  | 15/16 |
| MNQ | 5 | h8 | +0.073 | +0.048 .. +0.098 | +4.5% | +0.143 | 6e-09 |  | 15/16 |
| MNQ | 5 | h16 | +0.084 | +0.043 .. +0.126 | +3.5% | +0.156 | 6.7e-05 |  | 14/16 |
| MNQ | 5 | eod | +0.099 | -0.129 .. +0.326 | +0.8% | +0.321 | 0.4 |  | 12/16 |
| MNQ | 15 | h1 * | +0.053 | +0.043 .. +0.064 | +10.0% | +0.107 | 3.2e-24 | 1.98e-21 | 16/16 |
| MNQ | 15 | h2 | +0.050 | +0.036 .. +0.065 | +6.5% | +0.112 | 8.7e-08 |  | 15/16 |
| MNQ | 15 | h4 | +0.075 | +0.051 .. +0.098 | +6.6% | +0.128 | 5.5e-06 |  | 15/16 |
| MNQ | 15 | h8 | +0.089 | +0.051 .. +0.127 | +5.3% | +0.136 | 1.1e-05 |  | 13/16 |
| MNQ | 15 | h16 | +0.101 | +0.056 .. +0.146 | +4.0% | +0.139 | 0.0011 |  | 15/16 |
| MNQ | 15 | eod | +0.034 | -0.139 .. +0.207 | +0.5% | +0.126 | 0.74 |  | 11/16 |
| MNQ | 60 | h1 | +0.049 | +0.027 .. +0.070 | +9.2% | +0.086 | 8.4e-06 |  | 14/16 |
| MNQ | 60 | h2 * | +0.092 | +0.065 .. +0.119 | +12.1% | +0.132 | 6.8e-11 | 2.24e-08 | 15/16 |
| MNQ | 60 | h4 | +0.104 | +0.068 .. +0.140 | +9.4% | +0.166 | 4.8e-08 |  | 13/16 |
| MNQ | 60 | h8 | +0.104 | +0.059 .. +0.149 | +6.6% | +0.169 | 7.5e-06 |  | 13/16 |
| MNQ | 60 | h16 | +0.096 | +0.044 .. +0.149 | +4.4% | +0.174 | 0.00036 |  | 14/16 |
| MNQ | 60 | eod | +0.091 | +0.039 .. +0.144 | +4.0% | +0.174 | 0.00078 |  | 15/16 |
| MYM | 5 | h1 | +0.058 | +0.041 .. +0.076 | +10.9% | +0.122 | 3e-10 |  | 8/8 |
| MYM | 5 | h2 * | +0.053 | +0.041 .. +0.066 | +7.0% | +0.133 | 9.8e-17 | 4.37e-14 | 8/8 |
| MYM | 5 | h4 | +0.069 | +0.053 .. +0.086 | +6.3% | +0.142 | 1.2e-08 |  | 8/8 |
| MYM | 5 | h8 | +0.073 | +0.034 .. +0.112 | +4.6% | +0.160 | 0.00022 |  | 7/8 |
| MYM | 5 | h16 | +0.096 | +0.044 .. +0.147 | +4.1% | +0.184 | 0.00027 |  | 6/8 |
| MYM | 5 | eod | +0.327 | +0.080 .. +0.574 | +2.8% | +0.569 | 0.0095 |  | 7/8 |
| MYM | 15 | h1 * | +0.068 | +0.043 .. +0.092 | +12.8% | +0.156 | 1.5e-07 | 3.93e-05 | 8/8 |
| MYM | 15 | h2 | +0.080 | +0.061 .. +0.100 | +10.5% | +0.171 | 1.3e-06 |  | 8/8 |
| MYM | 15 | h4 | +0.075 | +0.051 .. +0.100 | +6.8% | +0.175 | 0.001 |  | 8/8 |
| MYM | 15 | h8 | +0.084 | +0.046 .. +0.121 | +5.1% | +0.218 | 0.0079 |  | 8/8 |
| MYM | 15 | h16 | +0.069 | -0.010 .. +0.149 | +2.8% | +0.210 | 0.19 |  | 7/8 |
| MYM | 15 | eod | +0.074 | -0.096 .. +0.244 | +1.2% | +0.216 | 0.41 |  | 6/8 |
| MYM | 60 | h1 * | +0.040 | +0.013 .. +0.068 | +7.7% | +0.112 | 0.032 | 1 | 5/8 |
| MYM | 60 | h2 | +0.024 | -0.010 .. +0.058 | +3.2% | +0.108 | 0.59 |  | 5/8 |
| MYM | 60 | h4 | +0.020 | -0.030 .. +0.071 | +1.9% | +0.113 | 0.83 |  | 4/8 |
| MYM | 60 | h8 | +0.041 | -0.023 .. +0.105 | +2.6% | +0.121 | 0.43 |  | 6/8 |
| MYM | 60 | h16 | +0.062 | -0.005 .. +0.130 | +2.9% | +0.103 | 0.13 |  | 6/8 |
| MYM | 60 | eod | +0.050 | -0.022 .. +0.121 | +2.2% | +0.097 | 0.23 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.02 pts | -0.40 .. +0.45 | 0.93 |
| MES | 15 | +0.39 pts | -0.31 .. +1.08 | 0.3 |
| MES | 60 | +0.36 pts | -0.91 .. +1.63 | 0.92 |
| MNQ | 5 | +0.35 pts | -0.05 .. +0.76 | 0.088 |
| MNQ | 15 | +0.10 pts | -0.62 .. +0.82 | 0.78 |
| MNQ | 60 | -1.36 pts | -2.78 .. +0.05 | 0.059 |
| MYM | 5 | -0.26 pts | -0.87 .. +0.35 | 0.4 |
| MYM | 15 | -0.16 pts | -1.08 .. +0.75 | 0.74 |
| MYM | 60 | -1.02 pts | -2.66 .. +0.62 | 0.25 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 55843 | +0.013 | 0.309 | +0.17 | -3.33 | -3.45 | -3.22 | -3.45 |
| MES | 5 | h2 | event | against signal | 55843 | +0.016 | 0.309 | +0.19 | -3.31 | -3.44 | -3.20 | -3.49 |
| MES | 5 | h4 | event | with signal | 55843 | -0.012 | 0.309 | -0.05 | -3.55 | -3.45 | -3.64 | -3.38 |
| MES | 5 | h8 | event | against signal | 55843 | +0.013 | 0.309 | +0.02 | -3.48 | -3.45 | -3.51 | -3.64 |
| MES | 5 | h16 | event | against signal | 55843 | +0.038 | 0.309 | +0.26 | -3.24 | -3.42 | -3.08 | -3.42 |
| MES | 5 | eod | event | against signal | 55843 | -0.085 | 0.309 | -0.02 | -3.52 | -3.70 | -3.36 | -2.37 |
| MES | 15 | h1 | event | with signal | 19849 | -0.004 | 0.186 | +0.17 | -3.33 | -3.51 | -3.17 | -3.17 |
| MES | 15 | h2 | event | with signal | 19849 | -0.002 | 0.186 | +0.28 | -3.22 | -3.56 | -2.91 | -3.04 |
| MES | 15 | h4 | event | against signal | 19849 | +0.013 | 0.186 | -0.27 | -3.77 | -3.45 | -4.07 | -3.93 |
| MES | 15 | h8 | event | against signal | 19849 | +0.034 | 0.186 | +0.33 | -3.17 | -3.43 | -2.93 | -3.30 |
| MES | 15 | h16 | event | against signal | 19849 | +0.007 | 0.186 | -0.12 | -3.62 | -3.53 | -3.70 | -3.51 |
| MES | 15 | eod | event | with signal | 19849 | +0.167 | 0.186 | +0.94 | -2.56 | -2.00 | -3.06 | -3.94 |
| MES | 60 | h1 | event | with signal | 5018 | +0.008 | 0.094 | +0.63 | -2.87 | -3.49 | -2.29 | -2.88 |
| MES | 60 | h2 | event | with signal | 5018 | +0.010 | 0.094 | -0.04 | -3.54 | -3.01 | -4.03 | -3.52 |
| MES | 60 | h4 | event | against signal | 5018 | +0.003 | 0.094 | +1.01 | -2.49 | -3.45 | -1.59 | -2.55 |
| MES | 60 | h8 | event | against signal | 5018 | +0.005 | 0.094 | +0.99 | -2.51 | -3.42 | -1.66 | -2.58 |
| MES | 60 | h16 | event | against signal | 5018 | -0.019 | 0.094 | +0.01 | -3.49 | -3.96 | -3.04 | -3.08 |
| MES | 60 | eod | event | against signal | 5018 | -0.014 | 0.094 | +0.40 | -3.10 | -4.20 | -2.07 | -2.94 |
| MNQ | 5 | h1 | event | with signal | 61834 | +0.008 | 0.129 | +0.10 | -1.90 | -1.93 | -1.86 | -1.83 |
| MNQ | 5 | h2 | event | with signal | 61834 | +0.006 | 0.129 | +0.02 | -1.98 | -1.95 | -2.00 | -1.88 |
| MNQ | 5 | h4 | event | with signal | 61834 | +0.013 | 0.129 | +0.08 | -1.92 | -1.86 | -1.97 | -1.90 |
| MNQ | 5 | h8 | event | with signal | 61834 | +0.014 | 0.129 | -0.21 | -2.21 | -1.88 | -2.51 | -2.32 |
| MNQ | 5 | h16 | event | against signal | 61834 | -0.003 | 0.129 | +0.32 | -1.68 | -2.08 | -1.30 | -1.45 |
| MNQ | 5 | eod | event | against signal | 61834 | -0.146 | 0.129 | -0.25 | -2.25 | -1.92 | -2.57 | +0.64 |
| MNQ | 15 | h1 | event | with signal | 21184 | +0.010 | 0.075 | +0.33 | -1.67 | -1.95 | -1.40 | -1.56 |
| MNQ | 15 | h2 | event | with signal | 21184 | +0.017 | 0.075 | +0.19 | -1.81 | -1.93 | -1.69 | -1.74 |
| MNQ | 15 | h4 | event | with signal | 21184 | +0.005 | 0.075 | -0.02 | -2.02 | -2.02 | -2.02 | -2.00 |
| MNQ | 15 | h8 | event | against signal | 21184 | +0.001 | 0.075 | +0.19 | -1.81 | -1.83 | -1.80 | -1.63 |
| MNQ | 15 | h16 | event | against signal | 21184 | +0.016 | 0.075 | -0.21 | -2.21 | -1.65 | -2.75 | -1.79 |
| MNQ | 15 | eod | event | with signal | 21184 | +0.159 | 0.075 | +1.93 | -0.07 | -1.63 | +1.40 | -1.92 |
| MNQ | 60 | h1 | event | with signal | 5294 | +0.014 | 0.038 | +1.72 | -0.28 | -2.10 | +1.46 | -0.43 |
| MNQ | 60 | h2 | event | against signal | 5294 | +0.002 | 0.038 | -0.31 | -2.31 | -1.88 | -2.73 | -2.22 |
| MNQ | 60 | h4 | event | against signal | 5294 | +0.027 | 0.038 | +0.68 | -1.32 | -1.01 | -1.61 | -1.22 |
| MNQ | 60 | h8 | event | against signal | 5294 | +0.023 | 0.038 | +0.51 | -1.49 | -1.43 | -1.54 | -1.42 |
| MNQ | 60 | h16 | event | against signal | 5294 | -0.012 | 0.038 | -0.26 | -2.26 | -1.86 | -2.63 | -1.99 |
| MNQ | 60 | eod | event | against signal | 5294 | -0.013 | 0.038 | +0.03 | -1.97 | -1.94 | -1.99 | -1.90 |
| MYM | 5 | h1 | event | with signal | 31657 | +0.007 | 0.175 | +0.06 | -1.94 | +nan | -1.94 | -1.86 |
| MYM | 5 | h2 | event | with signal | 31657 | -0.001 | 0.175 | +0.05 | -1.95 | +nan | -1.95 | -1.89 |
| MYM | 5 | h4 | event | with signal | 31657 | +0.009 | 0.175 | +0.19 | -1.81 | +nan | -1.81 | -1.80 |
| MYM | 5 | h8 | event | against signal | 31657 | +0.006 | 0.175 | -0.07 | -2.07 | +nan | -2.07 | -1.98 |
| MYM | 5 | h16 | event | against signal | 31657 | +0.030 | 0.175 | +0.04 | -1.96 | +nan | -1.96 | -1.83 |
| MYM | 5 | eod | event | against signal | 31657 | +0.125 | 0.175 | +0.65 | -1.35 | +nan | -1.35 | -0.51 |
| MYM | 15 | h1 | event | with signal | 10825 | +0.010 | 0.100 | -0.01 | -2.01 | +nan | -2.01 | -1.93 |
| MYM | 15 | h2 | event | with signal | 10825 | +0.006 | 0.100 | +0.07 | -1.93 | +nan | -1.93 | -1.89 |
| MYM | 15 | h4 | event | against signal | 10825 | -0.002 | 0.100 | -0.23 | -2.23 | +nan | -2.23 | -2.19 |
| MYM | 15 | h8 | event | against signal | 10825 | +0.014 | 0.100 | +0.26 | -1.74 | +nan | -1.74 | -1.58 |
| MYM | 15 | h16 | event | against signal | 10825 | -0.009 | 0.100 | +0.15 | -1.85 | +nan | -1.85 | -1.46 |
| MYM | 15 | eod | event | with signal | 10825 | +0.102 | 0.100 | -0.77 | -2.77 | +nan | -2.77 | -3.40 |
| MYM | 60 | h1 | event | against signal | 2744 | +0.017 | 0.048 | +0.37 | -1.63 | +nan | -1.63 | -1.58 |
| MYM | 60 | h2 | event | against signal | 2744 | +0.026 | 0.048 | +1.14 | -0.86 | +nan | -0.86 | -0.98 |
| MYM | 60 | h4 | event | against signal | 2744 | +0.087 | 0.048 | +3.88 | +1.88 | +nan | +1.88 | +1.79 |
| MYM | 60 | h8 | event | against signal | 2744 | +0.109 | 0.048 | +5.11 | +3.11 | +nan | +3.11 | +3.08 |
| MYM | 60 | h16 | event | against signal | 2744 | +0.094 | 0.048 | +4.12 | +2.12 | +nan | +2.12 | +3.06 |
| MYM | 60 | eod | event | against signal | 2744 | +0.112 | 0.048 | +4.63 | +2.63 | +nan | +2.63 | +3.40 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.050 | -1.224 | -1.198 | -1.073 | -1.000 | +0.000 | -0.031 | -0.034 | -0.032 | -0.037 | -0.063 |
| MES | 15 | -1.135 | -1.293 | -1.297 | -1.172 | -1.074 | +0.000 | -0.006 | -0.005 | -0.021 | -0.051 | -0.050 |
| MES | 60 | -1.277 | -1.412 | -1.431 | -1.311 | -1.182 | +0.000 | +0.004 | -0.003 | -0.033 | -0.064 | -0.049 |
| MNQ | 5 | -1.197 | -1.371 | -1.341 | -1.202 | -1.089 | +0.000 | -0.005 | -0.008 | -0.005 | -0.008 | -0.025 |
| MNQ | 15 | -1.195 | -1.355 | -1.365 | -1.247 | -1.145 | +0.000 | +0.004 | +0.009 | -0.002 | -0.019 | -0.063 |
| MNQ | 60 | -1.264 | -1.407 | -1.461 | -1.370 | -1.253 | +0.000 | +0.009 | -0.012 | -0.048 | -0.092 | +0.050 |
| MYM | 5 | -1.199 | -1.371 | -1.342 | -1.191 | -1.072 | +0.000 | +0.006 | -0.004 | -0.001 | -0.021 | -0.049 |
| MYM | 15 | -1.207 | -1.365 | -1.356 | -1.244 | -1.138 | +0.000 | +0.025 | +0.020 | +0.016 | -0.005 | +0.002 |
| MYM | 60 | -1.376 | -1.442 | -1.472 | -1.334 | -1.215 | +0.000 | -0.016 | -0.026 | -0.109 | -0.165 | -0.069 |

## Calibration

- MES 5-min: 1033927 bars, 55843 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341202 bars, 19849 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 82974 bars, 5018 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1033835 bars, 61834 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341355 bars, 21184 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83036 bars, 5294 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518694 bars, 31657 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171064 bars, 10825 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41548 bars, 2744 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
