# Impact card: x_ema8_20

EMA8 crosses EMA20: up cross long, down cross short [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.047 R20 over the rest of the session (to 16:45), p=0.049; we would catch an effect of 0.016 R20 or more 80% of the time).
- MES 5-min size: the market moves 2% MORE after the event than after matched bars over the next 8 bars (40 min) (+0.035 R20, CONFIRMED, q=0.00086, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.26 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.233 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.028 R20 over the next 4 bars (1 h), p=0.17; we would catch an effect of 0.033 R20 or more 80% of the time).
- MES 15-min size: the market moves 4% MORE after the event than after matched bars over the next 16 bars (4 h) (+0.090 R20, possible, q=0.0613, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.28 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.132 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.045 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.067 R20 or more 80% of the time).
- MES 60-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.036 R20, CONFIRMED, q=0.0379, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.53 at recent bar sizes, 90% range up to $4.64); about 3.3x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.096 R20 over the rest of the session (to 16:45), p=0.032; we would catch an effect of 0.020 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.021).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.39 at recent bar sizes, 90% range up to $0.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.024 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.041 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.030 R20, CONFIRMED, q=0.00931, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.94 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.046 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.081 R20 over the rest of the session (to 16:45), p=0.095; we would catch an effect of 0.075 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.044 R20, CONFIRMED, q=0.0392, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.46 at recent bar sizes, 90% range up to $10.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.020 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.027 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.1).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.179 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.055 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.056 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.58).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.33 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.099 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.043 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.104 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.012).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.78 at recent bar sizes, 90% range up to $4.21); about 124.6x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.005 | -0.012 .. +0.002 | -0.0015 | 0.18 / 0.18 / 0.14 | 0.147 |  |  | 11/16 | -0.006 | -0.004 |  | -1.4 / -1.3 |  |
| MES | 5 | h2 | -0.003 | -0.012 .. +0.006 | -0.0006 | 0.55 / 0.54 / 0.54 | 0.546 |  |  | 10/16 | +0.001 | -0.006 |  | -0.6 / -0.6 |  |
| MES | 5 | h4 | +0.005 | -0.005 .. +0.016 | +0.0008 | 0.29 / 0.32 / 0.36 | 0.351 |  |  | 11/16 | +0.010 | +0.001 |  | +0.8 / +1.1 | 0.016 |
| MES | 5 | h8 | +0.006 | -0.007 .. +0.020 | +0.0006 | 0.38 / 0.38 / 0.45 | 0.442 |  |  | 8/16 | +0.005 | +0.008 |  | +0.6 / +0.9 |  |
| MES | 5 | h16 | +0.005 | -0.012 .. +0.022 | +0.0004 | 0.54 / 0.56 / 0.6 | 0.596 |  |  | 9/16 | -0.010 | +0.021 |  | +0.4 / +0.6 |  |
| MES | 5 | eod * | -0.047 | -0.080 .. -0.015 | -0.0007 | 0.0047 / 0.0055 / 0.012 | 0.0135 | 1 | 0.703 | 12/16 | -0.075 | -0.020 | False | -0.7 / -2.8 |  |
| MES | 15 | h1 | +0.013 | +0.000 .. +0.025 | +0.0038 | 0.043 / 0.05 / 0.06 | 0.0597 |  |  | 12/16 | +0.006 | +0.020 |  | +2.0 / +2.0 |  |
| MES | 15 | h2 | +0.012 | -0.004 .. +0.028 | +0.0024 | 0.13 / 0.14 / 0.2 | 0.201 |  |  | 8/16 | -0.005 | +0.030 |  | +1.4 / +1.5 |  |
| MES | 15 | h4 * | +0.028 | +0.005 .. +0.052 | +0.0037 | 0.017 / 0.015 / 0.036 | 0.0388 | 1 | 0.967 | 11/16 | +0.013 | +0.044 | False | +2.2 / +2.4 | 0.033 |
| MES | 15 | h8 | -0.005 | -0.034 .. +0.025 | -0.0004 | 0.76 / 0.76 / 0.78 | 0.788 |  |  | 7/16 | -0.021 | +0.012 |  | -0.2 / -0.3 |  |
| MES | 15 | h16 | -0.014 | -0.050 .. +0.022 | -0.0009 | 0.45 / 0.46 / 0.48 | 0.483 |  |  | 9/16 | -0.046 | +0.018 |  | -0.5 / -0.8 |  |
| MES | 15 | eod | -0.028 | -0.073 .. +0.018 | -0.0007 | 0.24 / 0.26 / 0.35 | 0.356 |  |  | 8/16 | -0.074 | +0.018 |  | -0.4 / -1.2 |  |
| MES | 60 | h1 | +0.003 | -0.025 .. +0.030 | +0.0008 | 0.84 / 0.84 / 0.84 | 0.847 |  |  | 8/16 | -0.016 | +0.022 |  | +0.2 / +0.2 |  |
| MES | 60 | h2 | +0.030 | -0.007 .. +0.066 | +0.0059 | 0.11 / 0.12 / 0.12 | 0.119 |  |  | 13/16 | +0.012 | +0.047 |  | +1.5 / +1.6 |  |
| MES | 60 | h4 | +0.031 | -0.014 .. +0.076 | +0.0044 | 0.18 / 0.19 / 0.21 | 0.215 |  |  | 9/16 | -0.025 | +0.087 |  | +1.1 / +1.4 | 0.067 |
| MES | 60 | h8 | +0.037 | -0.016 .. +0.091 | +0.0038 | 0.17 / 0.17 / 0.22 | 0.219 |  |  | 8/16 | -0.028 | +0.103 |  | +1.0 / +1.4 |  |
| MES | 60 | h16 | +0.036 | -0.020 .. +0.091 | +0.0028 | 0.21 / 0.23 / 0.27 | 0.277 |  |  | 8/16 | -0.004 | +0.076 |  | +0.8 / +1.3 |  |
| MES | 60 | eod * | +0.045 | -0.012 .. +0.103 | +0.0034 | 0.12 / 0.13 / 0.17 | 0.164 | 1 | 1 | 10/16 | -0.009 | +0.100 | False | +1.0 / +1.6 |  |
| MNQ | 5 | h1 | -0.002 | -0.010 .. +0.006 | -0.0005 | 0.59 / 0.57 / 0.63 | 0.627 |  |  | 8/16 | -0.014 | +0.010 |  | -0.6 / -0.5 |  |
| MNQ | 5 | h2 | -0.002 | -0.012 .. +0.009 | -0.0003 | 0.73 / 0.72 / 0.78 | 0.76 |  |  | 10/16 | -0.017 | +0.013 |  | -0.4 / -0.3 |  |
| MNQ | 5 | h4 | +0.001 | -0.013 .. +0.015 | +0.0001 | 0.88 / 0.88 / 0.91 | 0.901 |  |  | 9/16 | -0.021 | +0.023 |  | +0.1 / +0.1 | 0.020 |
| MNQ | 5 | h8 | -0.005 | -0.022 .. +0.012 | -0.0003 | 0.59 / 0.59 / 0.7 | 0.695 |  |  | 8/16 | -0.039 | +0.030 |  | -0.4 / -0.5 |  |
| MNQ | 5 | h16 | -0.005 | -0.025 .. +0.016 | -0.0002 | 0.67 / 0.67 / 0.79 | 0.796 |  |  | 10/16 | -0.031 | +0.022 |  | -0.3 / -0.4 |  |
| MNQ | 5 | eod * | -0.096 | -0.145 .. -0.047 | -0.0010 | 0.00012 / 6e-05 / 0.0099 | 0.0099 | 0.777 | 0.059 | 13/16 | -0.168 | -0.025 | False | -1.0 / -3.8 |  |
| MNQ | 15 | h1 | +0.005 | -0.009 .. +0.019 | +0.0011 | 0.52 / 0.51 / 0.6 | 0.558 |  |  | 10/16 | -0.015 | +0.024 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h2 | -0.009 | -0.029 .. +0.011 | -0.0012 | 0.36 / 0.34 / 0.5 | 0.44 |  |  | 9/16 | -0.028 | +0.009 |  | -0.9 / -0.9 |  |
| MNQ | 15 | h4 | -0.001 | -0.027 .. +0.024 | -0.0001 | 0.91 / 0.91 / 0.95 | 0.943 |  |  | 8/16 | -0.002 | -0.001 |  | -0.1 / -0.1 | 0.041 |
| MNQ | 15 | h8 | -0.016 | -0.048 .. +0.015 | -0.0010 | 0.31 / 0.34 / 0.54 | 0.525 |  |  | 10/16 | -0.026 | -0.007 |  | -0.7 / -1.0 |  |
| MNQ | 15 | h16 * | -0.024 | -0.063 .. +0.015 | -0.0012 | 0.23 / 0.25 / 0.42 | 0.416 | 1 | 1 | 11/16 | -0.058 | +0.011 | False | -0.7 / -1.2 |  |
| MNQ | 15 | eod | -0.031 | -0.090 .. +0.029 | -0.0005 | 0.31 / 0.32 / 0.61 | 0.611 |  |  | 10/16 | -0.096 | +0.034 |  | -0.4 / -1.0 |  |
| MNQ | 60 | h1 | +0.018 | -0.015 .. +0.051 | +0.0048 | 0.28 / 0.27 / 0.24 | 0.234 |  |  | 10/16 | -0.008 | +0.045 |  | +1.1 / +1.1 |  |
| MNQ | 60 | h2 | +0.022 | -0.019 .. +0.063 | +0.0041 | 0.29 / 0.29 / 0.29 | 0.283 |  |  | 10/16 | -0.024 | +0.068 |  | +1.0 / +1.1 |  |
| MNQ | 60 | h4 | +0.045 | -0.003 .. +0.094 | +0.0059 | 0.067 / 0.074 / 0.09 | 0.0852 |  |  | 10/16 | -0.011 | +0.102 |  | +1.5 / +1.8 | 0.075 |
| MNQ | 60 | h8 | +0.059 | -0.000 .. +0.119 | +0.0056 | 0.051 / 0.05 / 0.067 | 0.0641 |  |  | 9/16 | -0.046 | +0.165 |  | +1.5 / +1.9 |  |
| MNQ | 60 | h16 | +0.065 | +0.001 .. +0.128 | +0.0047 | 0.045 / 0.042 / 0.064 | 0.0667 |  |  | 10/16 | +0.003 | +0.127 |  | +1.4 / +2.0 |  |
| MNQ | 60 | eod * | +0.081 | +0.018 .. +0.145 | +0.0057 | 0.012 / 0.011 / 0.02 | 0.0177 | 1 | 0.897 | 12/16 | +0.024 | +0.139 | False | +1.7 / +2.5 |  |
| MYM | 5 | h1 | +0.001 | -0.009 .. +0.010 | +0.0002 | 0.87 / 0.87 / 0.87 | 0.852 |  |  | 5/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 5 | h2 | -0.002 | -0.015 .. +0.010 | -0.0004 | 0.69 / 0.71 / 0.86 | 0.849 |  |  | 5/8 | n/a | -0.002 |  | -0.3 / -0.4 |  |
| MYM | 5 | h4 | -0.014 | -0.032 .. +0.004 | -0.0013 | 0.12 / 0.12 / 0.42 | 0.375 |  |  | 5/8 | n/a | -0.014 |  | -1.3 / -1.6 | 0.027 |
| MYM | 5 | h8 | -0.011 | -0.036 .. +0.014 | -0.0008 | 0.39 / 0.37 / 0.6 | 0.587 |  |  | 2/8 | n/a | -0.011 |  | -0.7 / -0.9 |  |
| MYM | 5 | h16 * | -0.020 | -0.048 .. +0.009 | -0.0011 | 0.17 / 0.16 / 0.4 | 0.404 | 1 | 1 | 3/8 | n/a | -0.020 | False | -0.9 / -1.4 |  |
| MYM | 5 | eod | -0.036 | -0.096 .. +0.023 | -0.0004 | 0.23 / 0.24 / 0.49 | 0.495 |  |  | 5/8 | n/a | -0.036 |  | -0.3 / -1.2 |  |
| MYM | 15 | h1 | +0.005 | -0.013 .. +0.023 | +0.0011 | 0.58 / 0.61 / 0.69 | 0.674 |  |  | 3/8 | n/a | +0.005 |  | +0.5 / +0.5 |  |
| MYM | 15 | h2 | +0.011 | -0.016 .. +0.038 | +0.0014 | 0.42 / 0.43 / 0.59 | 0.535 |  |  | 4/8 | n/a | +0.011 |  | +0.8 / +0.8 |  |
| MYM | 15 | h4 | -0.003 | -0.036 .. +0.030 | -0.0002 | 0.86 / 0.86 / 0.93 | 0.917 |  |  | 3/8 | n/a | -0.003 |  | -0.1 / -0.2 | 0.056 |
| MYM | 15 | h8 | -0.010 | -0.054 .. +0.034 | -0.0006 | 0.65 / 0.67 / 0.78 | 0.746 |  |  | 5/8 | n/a | -0.010 |  | -0.4 / -0.5 |  |
| MYM | 15 | h16 | -0.007 | -0.063 .. +0.049 | -0.0003 | 0.8 / 0.8 / 0.88 | 0.868 |  |  | 5/8 | n/a | -0.007 |  | -0.2 / -0.3 |  |
| MYM | 15 | eod * | -0.055 | -0.130 .. +0.020 | -0.0010 | 0.15 / 0.14 / 0.53 | 0.507 | 1 | 1 | 6/8 | n/a | -0.055 | False | -0.5 / -1.4 |  |
| MYM | 60 | h1 | +0.010 | -0.032 .. +0.051 | +0.0027 | 0.66 / 0.67 / 0.66 | 0.661 |  |  | 5/8 | n/a | +0.010 |  | +0.4 / +0.4 |  |
| MYM | 60 | h2 | +0.011 | -0.044 .. +0.065 | +0.0021 | 0.71 / 0.72 / 0.71 | 0.724 |  |  | 5/8 | n/a | +0.011 |  | +0.3 / +0.4 |  |
| MYM | 60 | h4 * | +0.043 | -0.025 .. +0.111 | +0.0059 | 0.22 / 0.22 / 0.24 | 0.249 | 1 | 1 | 5/8 | n/a | +0.043 | False | +1.0 / +1.2 | 0.104 |
| MYM | 60 | h8 | -0.015 | -0.093 .. +0.063 | -0.0015 | 0.7 / 0.71 / 0.73 | 0.728 |  |  | 4/8 | n/a | -0.015 |  | -0.3 / -0.4 |  |
| MYM | 60 | h16 | -0.021 | -0.106 .. +0.063 | -0.0016 | 0.62 / 0.64 / 0.65 | 0.644 |  |  | 5/8 | n/a | -0.021 |  | -0.3 / -0.5 |  |
| MYM | 60 | eod | -0.025 | -0.110 .. +0.060 | -0.0018 | 0.56 / 0.58 / 0.59 | 0.58 |  |  | 4/8 | n/a | -0.025 |  | -0.4 / -0.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.005 | +0.001 .. +0.010 | +1.0% | +0.026 | 0.03 |  | 12/16 |
| MES | 5 | h2 | +0.005 | -0.001 .. +0.012 | +0.7% | +0.027 | 0.14 |  | 9/16 |
| MES | 5 | h4 | +0.017 | +0.008 .. +0.026 | +1.7% | +0.039 | 0.0015 |  | 12/16 |
| MES | 5 | h8 * | +0.035 | +0.020 .. +0.050 | +2.5% | +0.052 | 3.6e-06 | 0.00086 | 13/16 |
| MES | 5 | h16 | +0.049 | +0.027 .. +0.071 | +2.3% | +0.072 | 1.3e-05 |  | 14/16 |
| MES | 5 | eod | +0.026 | -0.120 .. +0.172 | +0.3% | +0.128 | 0.73 |  | 9/16 |
| MES | 15 | h1 | +0.021 | +0.014 .. +0.029 | +4.2% | +0.050 | 0.0014 |  | 15/16 |
| MES | 15 | h2 | +0.016 | +0.004 .. +0.028 | +2.2% | +0.055 | 0.1 |  | 13/16 |
| MES | 15 | h4 | +0.034 | +0.015 .. +0.052 | +3.2% | +0.066 | 0.022 |  | 13/16 |
| MES | 15 | h8 | +0.047 | +0.018 .. +0.075 | +3.0% | +0.085 | 0.011 |  | 10/16 |
| MES | 15 | h16 * | +0.090 | +0.047 .. +0.134 | +4.0% | +0.109 | 0.00033 | 0.0613 | 15/16 |
| MES | 15 | eod | +0.079 | -0.055 .. +0.213 | +1.4% | +0.109 | 0.25 |  | 10/16 |
| MES | 60 | h1 * | +0.036 | +0.018 .. +0.054 | +7.0% | +0.063 | 0.0002 | 0.0379 | 16/16 |
| MES | 60 | h2 | +0.037 | +0.009 .. +0.064 | +4.9% | +0.085 | 0.012 |  | 12/16 |
| MES | 60 | h4 | +0.065 | +0.025 .. +0.105 | +6.2% | +0.104 | 0.0015 |  | 12/16 |
| MES | 60 | h8 | +0.047 | -0.003 .. +0.097 | +3.1% | +0.097 | 0.13 |  | 7/16 |
| MES | 60 | h16 | +0.047 | -0.014 .. +0.108 | +2.3% | +0.091 | 0.18 |  | 10/16 |
| MES | 60 | eod | +0.045 | -0.019 .. +0.109 | +2.1% | +0.090 | 0.17 |  | 11/16 |
| MNQ | 5 | h1 * | +0.011 | +0.006 .. +0.017 | +2.1% | +0.035 | 0.0035 | 0.538 | 13/16 |
| MNQ | 5 | h2 | +0.015 | +0.007 .. +0.023 | +2.0% | +0.039 | 0.035 |  | 15/16 |
| MNQ | 5 | h4 | +0.027 | +0.015 .. +0.040 | +2.5% | +0.057 | 0.015 |  | 15/16 |
| MNQ | 5 | h8 | +0.039 | +0.015 .. +0.062 | +2.4% | +0.067 | 0.01 |  | 15/16 |
| MNQ | 5 | h16 | +0.056 | +0.015 .. +0.098 | +2.4% | +0.090 | 0.0081 |  | 14/16 |
| MNQ | 5 | eod | +0.132 | -0.108 .. +0.373 | +1.1% | +0.341 | 0.28 |  | 11/16 |
| MNQ | 15 | h1 * | +0.030 | +0.020 .. +0.041 | +5.6% | +0.060 | 4.3e-05 | 0.00931 | 13/16 |
| MNQ | 15 | h2 | +0.031 | +0.016 .. +0.046 | +4.0% | +0.065 | 0.033 |  | 12/16 |
| MNQ | 15 | h4 | +0.011 | -0.018 .. +0.041 | +1.0% | +0.043 | 0.66 |  | 8/16 |
| MNQ | 15 | h8 | -0.010 | -0.058 .. +0.038 | -0.6% | -0.006 | 0.68 |  | 6/16 |
| MNQ | 15 | h16 | +0.022 | -0.037 .. +0.080 | +0.9% | -0.069 | 0.77 |  | 12/16 |
| MNQ | 15 | eod | -0.100 | -0.308 .. +0.109 | -1.6% | -0.122 | 0.36 |  | 9/16 |
| MNQ | 60 | h1 * | +0.044 | +0.021 .. +0.067 | +8.2% | +0.058 | 0.0002 | 0.0392 | 14/16 |
| MNQ | 60 | h2 | +0.036 | +0.005 .. +0.067 | +4.7% | +0.063 | 0.022 |  | 14/16 |
| MNQ | 60 | h4 | +0.025 | -0.019 .. +0.068 | +2.2% | +0.064 | 0.27 |  | 10/16 |
| MNQ | 60 | h8 | +0.024 | -0.025 .. +0.072 | +1.5% | +0.069 | 0.37 |  | 10/16 |
| MNQ | 60 | h16 | +0.020 | -0.042 .. +0.083 | +0.9% | +0.076 | 0.54 |  | 9/16 |
| MNQ | 60 | eod | +0.017 | -0.046 .. +0.081 | +0.7% | +0.072 | 0.61 |  | 10/16 |
| MYM | 5 | h1 * | +0.012 | +0.005 .. +0.019 | +2.2% | +0.033 | 0.017 | 1 | 6/8 |
| MYM | 5 | h2 | +0.017 | +0.004 .. +0.030 | +2.3% | +0.042 | 0.059 |  | 7/8 |
| MYM | 5 | h4 | +0.032 | +0.010 .. +0.054 | +2.9% | +0.053 | 0.041 |  | 7/8 |
| MYM | 5 | h8 | +0.045 | +0.005 .. +0.085 | +2.9% | +0.070 | 0.026 |  | 7/8 |
| MYM | 5 | h16 | +0.067 | +0.010 .. +0.123 | +2.9% | +0.090 | 0.02 |  | 7/8 |
| MYM | 5 | eod | +0.041 | -0.220 .. +0.302 | +0.3% | +0.121 | 0.76 |  | 5/8 |
| MYM | 15 | h1 | +0.017 | +0.003 .. +0.031 | +3.1% | +0.037 | 0.24 |  | 5/8 |
| MYM | 15 | h2 | +0.013 | -0.010 .. +0.037 | +1.7% | +0.035 | 0.73 |  | 6/8 |
| MYM | 15 | h4 | +0.007 | -0.033 .. +0.047 | +0.6% | +0.012 | 0.82 |  | 7/8 |
| MYM | 15 | h8 | -0.002 | -0.060 .. +0.057 | -0.1% | -0.044 | 0.96 |  | 2/8 |
| MYM | 15 | h16 | -0.076 | -0.167 .. +0.015 | -3.1% | -0.165 | 0.13 |  | 6/8 |
| MYM | 15 | eod * | -0.229 | -0.499 .. +0.041 | -3.8% | -0.354 | 0.097 | 1 | 5/8 |
| MYM | 60 | h1 | +0.040 | +0.012 .. +0.068 | +7.7% | +0.069 | 0.011 |  | 8/8 |
| MYM | 60 | h2 * | +0.065 | +0.030 .. +0.100 | +8.6% | +0.099 | 0.002 | 0.329 | 8/8 |
| MYM | 60 | h4 | +0.046 | -0.012 .. +0.103 | +4.2% | +0.083 | 0.16 |  | 6/8 |
| MYM | 60 | h8 | +0.039 | -0.030 .. +0.108 | +2.5% | +0.108 | 0.39 |  | 6/8 |
| MYM | 60 | h16 | +0.031 | -0.056 .. +0.118 | +1.5% | +0.105 | 0.5 |  | 4/8 |
| MYM | 60 | eod | +0.027 | -0.069 .. +0.123 | +1.2% | +0.098 | 0.59 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.11 pts | -0.50 .. +0.29 | 0.89 |
| MES | 15 | +0.67 pts | -0.03 .. +1.38 | 0.068 |
| MES | 60 | +1.40 pts | +0.08 .. +2.71 | 0.091 |
| MNQ | 5 | -0.21 pts | -0.61 .. +0.20 | 0.34 |
| MNQ | 15 | -0.01 pts | -0.75 .. +0.74 | 0.98 |
| MNQ | 60 | +0.39 pts | -1.04 .. +1.82 | 0.59 |
| MYM | 5 | -0.28 pts | -0.81 .. +0.25 | 0.38 |
| MYM | 15 | +0.25 pts | -0.72 .. +1.22 | 0.63 |
| MYM | 60 | +0.71 pts | -1.20 .. +2.61 | 0.82 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 52672 | +0.013 | 0.345 | +0.08 | -3.42 | -3.45 | -3.37 | -3.50 |
| MES | 5 | h2 | event | against signal | 52672 | +0.014 | 0.345 | +0.10 | -3.40 | -3.46 | -3.33 | -3.51 |
| MES | 5 | h4 | event | with signal | 52672 | -0.006 | 0.345 | -0.08 | -3.58 | -3.47 | -3.69 | -3.47 |
| MES | 5 | h8 | event | with signal | 52672 | -0.005 | 0.345 | -0.01 | -3.51 | -3.51 | -3.52 | -3.40 |
| MES | 5 | h16 | event | with signal | 52672 | -0.009 | 0.345 | +0.06 | -3.44 | -3.53 | -3.34 | -3.30 |
| MES | 5 | eod | event | against signal | 52672 | +0.016 | 0.345 | -0.21 | -3.71 | -3.53 | -3.89 | -3.28 |
| MES | 15 | h1 | event | with signal | 16788 | +0.006 | 0.196 | +0.23 | -3.27 | -3.43 | -3.11 | -3.14 |
| MES | 15 | h2 | event | with signal | 16788 | +0.004 | 0.196 | +0.14 | -3.36 | -3.45 | -3.27 | -3.21 |
| MES | 15 | h4 | event | with signal | 16788 | +0.020 | 0.196 | +0.58 | -2.92 | -3.26 | -2.57 | -2.77 |
| MES | 15 | h8 | event | against signal | 16788 | +0.015 | 0.196 | -0.06 | -3.56 | -3.43 | -3.70 | -3.71 |
| MES | 15 | h16 | event | against signal | 16788 | +0.017 | 0.196 | -0.01 | -3.51 | -3.30 | -3.74 | -3.54 |
| MES | 15 | eod | event | against signal | 16788 | -0.008 | 0.196 | -0.54 | -4.04 | -3.50 | -4.60 | -3.29 |
| MES | 60 | h1 | event | with signal | 3878 | +0.001 | 0.094 | +0.19 | -3.31 | -3.71 | -2.89 | -3.20 |
| MES | 60 | h2 | event | with signal | 3878 | +0.025 | 0.094 | +0.91 | -2.59 | -3.14 | -2.02 | -2.40 |
| MES | 60 | h4 | event | with signal | 3878 | +0.022 | 0.094 | +1.10 | -2.40 | -4.06 | -0.69 | -2.11 |
| MES | 60 | h8 | event | with signal | 3878 | +0.023 | 0.094 | +0.69 | -2.81 | -4.18 | -1.41 | -2.41 |
| MES | 60 | h16 | event | with signal | 3878 | +0.025 | 0.094 | +1.23 | -2.27 | -3.57 | -0.93 | -2.12 |
| MES | 60 | eod | event | with signal | 3878 | +0.027 | 0.094 | +1.83 | -1.67 | -3.74 | +0.47 | -1.27 |
| MNQ | 5 | h1 | event | against signal | 51837 | +0.005 | 0.138 | -0.04 | -2.04 | -1.92 | -2.17 | -2.09 |
| MNQ | 5 | h2 | event | against signal | 51837 | +0.006 | 0.138 | -0.03 | -2.03 | -1.88 | -2.18 | -2.10 |
| MNQ | 5 | h4 | event | with signal | 51837 | -0.000 | 0.138 | +0.20 | -1.80 | -2.06 | -1.54 | -1.77 |
| MNQ | 5 | h8 | event | against signal | 51837 | +0.001 | 0.138 | -0.22 | -2.22 | -1.88 | -2.57 | -2.18 |
| MNQ | 5 | h16 | event | against signal | 51837 | -0.005 | 0.138 | -0.24 | -2.24 | -1.96 | -2.52 | -2.14 |
| MNQ | 5 | eod | event | against signal | 51837 | +0.010 | 0.138 | -0.71 | -2.71 | -2.08 | -3.36 | -1.43 |
| MNQ | 15 | h1 | event | with signal | 16548 | +0.001 | 0.078 | +0.34 | -1.66 | -2.10 | -1.21 | -1.57 |
| MNQ | 15 | h2 | event | against signal | 16548 | +0.012 | 0.078 | +0.15 | -1.85 | -1.82 | -1.89 | -1.92 |
| MNQ | 15 | h4 | event | against signal | 16548 | +0.003 | 0.078 | +0.21 | -1.79 | -2.01 | -1.57 | -1.85 |
| MNQ | 15 | h8 | event | against signal | 16548 | +0.016 | 0.078 | +0.28 | -1.72 | -1.85 | -1.59 | -1.72 |
| MNQ | 15 | h16 | event | against signal | 16548 | +0.015 | 0.078 | +0.19 | -1.81 | -1.70 | -1.92 | -1.66 |
| MNQ | 15 | eod | event | against signal | 16548 | -0.015 | 0.078 | -1.38 | -3.38 | -1.99 | -4.80 | -2.54 |
| MNQ | 60 | h1 | event | with signal | 3814 | +0.017 | 0.037 | +2.38 | +0.38 | -1.87 | +2.74 | +0.46 |
| MNQ | 60 | h2 | event | with signal | 3814 | +0.018 | 0.037 | +1.83 | -0.17 | -2.22 | +1.99 | +0.13 |
| MNQ | 60 | h4 | event | with signal | 3814 | +0.038 | 0.037 | +3.65 | +1.65 | -2.03 | +5.53 | +2.16 |
| MNQ | 60 | h8 | event | with signal | 3814 | +0.043 | 0.037 | +5.82 | +3.82 | -2.41 | +10.38 | +4.79 |
| MNQ | 60 | h16 | event | with signal | 3814 | +0.036 | 0.037 | +5.09 | +3.09 | -2.13 | +8.58 | +4.70 |
| MNQ | 60 | eod | event | with signal | 3814 | +0.045 | 0.037 | +6.17 | +4.17 | -1.93 | +10.59 | +6.13 |
| MYM | 5 | h1 | event | with signal | 26008 | -0.004 | 0.179 | -0.01 | -2.01 | +nan | -2.01 | -1.96 |
| MYM | 5 | h2 | event | against signal | 26008 | +0.006 | 0.179 | +0.13 | -1.87 | +nan | -1.87 | -1.91 |
| MYM | 5 | h4 | event | against signal | 26008 | +0.014 | 0.179 | +0.13 | -1.87 | +nan | -1.87 | -1.86 |
| MYM | 5 | h8 | event | against signal | 26008 | +0.006 | 0.179 | +0.06 | -1.94 | +nan | -1.94 | -1.85 |
| MYM | 5 | h16 | event | against signal | 26008 | +0.012 | 0.179 | -0.03 | -2.03 | +nan | -2.03 | -1.91 |
| MYM | 5 | eod | event | against signal | 26008 | -0.003 | 0.179 | -0.21 | -2.21 | +nan | -2.21 | -1.62 |
| MYM | 15 | h1 | event | with signal | 8370 | +0.002 | 0.099 | -0.19 | -2.19 | +nan | -2.19 | -2.13 |
| MYM | 15 | h2 | event | with signal | 8370 | +0.010 | 0.099 | -0.12 | -2.12 | +nan | -2.12 | -2.08 |
| MYM | 15 | h4 | event | against signal | 8370 | +0.001 | 0.099 | +0.05 | -1.95 | +nan | -1.95 | -1.95 |
| MYM | 15 | h8 | event | against signal | 8370 | +0.004 | 0.099 | +0.46 | -1.54 | +nan | -1.54 | -1.46 |
| MYM | 15 | h16 | event | against signal | 8370 | -0.015 | 0.099 | -0.03 | -2.03 | +nan | -2.03 | -1.81 |
| MYM | 15 | eod | event | against signal | 8370 | +0.018 | 0.099 | -0.08 | -2.08 | +nan | -2.08 | -1.88 |
| MYM | 60 | h1 | event | with signal | 1964 | +0.009 | 0.048 | +0.71 | -1.29 | +nan | -1.29 | -1.24 |
| MYM | 60 | h2 | event | with signal | 1964 | +0.010 | 0.048 | +0.41 | -1.59 | +nan | -1.59 | -1.49 |
| MYM | 60 | h4 | event | with signal | 1964 | +0.045 | 0.048 | +1.44 | -0.56 | +nan | -0.56 | -0.53 |
| MYM | 60 | h8 | event | against signal | 1964 | +0.011 | 0.048 | +0.73 | -1.27 | +nan | -1.27 | -1.15 |
| MYM | 60 | h16 | event | against signal | 1964 | -0.008 | 0.048 | -0.07 | -2.07 | +nan | -2.07 | -0.99 |
| MYM | 60 | eod | event | against signal | 1964 | -0.004 | 0.048 | -0.71 | -2.71 | +nan | -2.71 | -1.66 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.225 | -1.029 | -1.190 | -0.946 | -0.616 | +0.000 | -0.031 | -0.032 | -0.025 | -0.025 | -0.025 |
| MES | 15 | -0.290 | -1.073 | -1.271 | -1.024 | -0.661 | +0.000 | -0.001 | -0.002 | +0.014 | -0.024 | -0.044 |
| MES | 60 | -0.794 | -1.260 | -1.401 | -1.142 | -0.756 | +0.000 | -0.001 | +0.023 | +0.016 | -0.023 | -0.045 |
| MNQ | 5 | -0.257 | -1.134 | -1.314 | -1.046 | -0.676 | +0.000 | -0.016 | -0.017 | -0.013 | -0.014 | -0.008 |
| MNQ | 15 | -0.321 | -1.133 | -1.354 | -1.109 | -0.729 | +0.000 | -0.004 | -0.017 | -0.007 | -0.026 | -0.048 |
| MNQ | 60 | -0.872 | -1.308 | -1.468 | -1.222 | -0.803 | +0.000 | +0.014 | +0.007 | +0.021 | -0.039 | +0.023 |
| MYM | 5 | -0.228 | -1.116 | -1.291 | -1.014 | -0.659 | +0.000 | -0.010 | -0.014 | -0.026 | -0.021 | -0.029 |
| MYM | 15 | -0.308 | -1.110 | -1.321 | -1.072 | -0.703 | +0.000 | -0.001 | +0.005 | -0.005 | -0.004 | +0.005 |
| MYM | 60 | -0.874 | -1.286 | -1.445 | -1.195 | -0.812 | +0.000 | +0.009 | +0.010 | +0.028 | -0.091 | +0.037 |

## Calibration

- MES 5-min: 1036147 bars, 52672 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342094 bars, 16788 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83335 bars, 3878 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034398 bars, 51837 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341938 bars, 16548 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83333 bars, 3814 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518977 bars, 26008 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171365 bars, 8370 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41615 bars, 1964 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
