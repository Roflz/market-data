# Impact card: big_bar_follow

bar range > 2x previous 20-bar average, traded in the bar's colour [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.140 R20 over the rest of the session (to 16:45), p=0.49; we would catch an effect of 0.022 R20 or more 80% of the time).
- MES 5-min size: the market moves 28% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.139 R20, CONFIRMED, q=2.83e-130, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.54 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.238 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.020 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MES 15-min size: the market moves 24% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.123 R20, CONFIRMED, q=1.19e-53, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.36 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.139 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.031 R20 over the next 2 bars (2 h), p=0.47; we would catch an effect of 0.058 R20 or more 80% of the time).
- MES 60-min size: the market moves 23% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.120 R20, CONFIRMED, q=7.69e-29, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.49 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.068 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.023 R20 over the next 4 bars (20 min), p=0.14; we would catch an effect of 0.024 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 26% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.138 R20, CONFIRMED, q=3.47e-144, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.55 at recent bar sizes, 90% range up to $1.25); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.019 R20 over the next 2 bars (30 min), p=0.45; we would catch an effect of 0.050 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 23% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.122 R20, CONFIRMED, q=2.76e-78, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.80 at recent bar sizes, 90% range up to $1.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.052 R20 over the next 4 bars (4 h), p=0.11; we would catch an effect of 0.059 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 20% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.103 R20, CONFIRMED, q=1.36e-21, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.38 at recent bar sizes, 90% range up to $7.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.172 R20 over the rest of the session (to 16:45), p=0.98; we would catch an effect of 0.051 R20 or more 80% of the time).
- MYM 5-min size: the market moves 23% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.172 R20, CONFIRMED, q=2.97e-82, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.58 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.188 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.042 R20 over the next 4 bars (1 h), p=0.44; we would catch an effect of 0.066 R20 or more 80% of the time).
- MYM 15-min size: the market moves 22% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.119 R20, CONFIRMED, q=4.3e-30, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.86 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.108 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.042 R20 over the next 1 bar (1 h), p=0.17; we would catch an effect of 0.079 R20 or more 80% of the time).
- MYM 60-min size: the market moves 25% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.132 R20, CONFIRMED, q=4.24e-14, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.62 at recent bar sizes, 90% range up to $3.76); about 10.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | -0.007 .. +0.013 | +0.0009 | 0.58 / 0.58 / 0.46 | 0.473 |  |  | 6/16 | +0.005 | +0.001 |  | +0.6 / +0.6 |  |
| MES | 5 | h2 | +0.006 | -0.008 .. +0.019 | +0.0013 | 0.39 / 0.39 / 0.29 | 0.295 |  |  | 8/16 | +0.002 | +0.010 |  | +0.8 / +0.9 |  |
| MES | 5 | h4 | +0.012 | -0.007 .. +0.030 | +0.0017 | 0.23 / 0.23 / 0.15 | 0.147 |  |  | 12/16 | +0.005 | +0.019 |  | +1.3 / +1.2 | 0.022 |
| MES | 5 | h8 | +0.015 | -0.012 .. +0.041 | +0.0015 | 0.28 / 0.28 / 0.22 | 0.221 |  |  | 10/16 | -0.008 | +0.037 |  | +1.2 / +1.1 |  |
| MES | 5 | h16 | +0.003 | -0.035 .. +0.040 | +0.0002 | 0.89 / 0.89 / 0.87 | 0.868 |  |  | 5/16 | -0.057 | +0.062 |  | +0.1 / +0.1 |  |
| MES | 5 | eod * | +0.140 | -0.018 .. +0.298 | +0.0020 | 0.082 / 0.08 / 0.08 | 0.0748 | 1 | 1 | 11/16 | -0.004 | +0.283 | False | +2.0 / +1.7 |  |
| MES | 15 | h1 | +0.009 | -0.007 .. +0.026 | +0.0034 | 0.28 / 0.26 / 0.2 | 0.199 |  |  | 9/16 | -0.001 | +0.019 |  | +1.1 / +1.1 |  |
| MES | 15 | h2 | +0.013 | -0.010 .. +0.036 | +0.0031 | 0.27 / 0.26 / 0.2 | 0.204 |  |  | 9/16 | -0.009 | +0.034 |  | +1.2 / +1.1 |  |
| MES | 15 | h4 * | +0.020 | -0.011 .. +0.051 | +0.0033 | 0.2 / 0.19 / 0.17 | 0.172 | 1 | 1 | 8/16 | -0.012 | +0.052 | False | +1.4 / +1.3 | 0.039 |
| MES | 15 | h8 | +0.014 | -0.028 .. +0.056 | +0.0016 | 0.52 / 0.5 / 0.48 | 0.485 |  |  | 8/16 | -0.004 | +0.032 |  | +0.7 / +0.6 |  |
| MES | 15 | h16 | -0.005 | -0.055 .. +0.044 | -0.0005 | 0.83 / 0.83 / 0.83 | 0.827 |  |  | 10/16 | -0.051 | +0.040 |  | -0.2 / -0.2 |  |
| MES | 15 | eod | +0.028 | -0.071 .. +0.127 | +0.0008 | 0.58 / 0.59 / 0.65 | 0.666 |  |  | 8/16 | -0.020 | +0.076 |  | +0.5 / +0.6 |  |
| MES | 60 | h1 | +0.023 | -0.000 .. +0.046 | +0.0099 | 0.055 / 0.073 / 0.053 | 0.0537 |  |  | 11/16 | +0.011 | +0.034 |  | +1.7 / +1.9 |  |
| MES | 60 | h2 * | +0.031 | +0.001 .. +0.062 | +0.0096 | 0.046 / 0.065 / 0.044 | 0.0471 | 1 | 0.998 | 11/16 | +0.025 | +0.038 | False | +1.8 / +2.0 |  |
| MES | 60 | h4 | +0.023 | -0.019 .. +0.065 | +0.0050 | 0.28 / 0.31 / 0.27 | 0.269 |  |  | 10/16 | +0.002 | +0.044 |  | +1.0 / +1.1 | 0.058 |
| MES | 60 | h8 | +0.022 | -0.031 .. +0.074 | +0.0034 | 0.42 / 0.44 / 0.39 | 0.395 |  |  | 10/16 | +0.026 | +0.017 |  | +0.8 / +0.8 |  |
| MES | 60 | h16 | +0.001 | -0.054 .. +0.056 | +0.0002 | 0.97 / 0.97 / 0.96 | 0.964 |  |  | 7/16 | +0.013 | -0.010 |  | +0.0 / +0.0 |  |
| MES | 60 | eod | +0.013 | -0.044 .. +0.071 | +0.0016 | 0.64 / 0.66 / 0.62 | 0.61 |  |  | 10/16 | +0.024 | +0.003 |  | +0.5 / +0.5 |  |
| MNQ | 5 | h1 | +0.008 | -0.002 .. +0.018 | +0.0023 | 0.11 / 0.11 / 0.11 | 0.109 |  |  | 11/16 | +0.005 | +0.011 |  | +1.6 / +1.6 |  |
| MNQ | 5 | h2 | +0.007 | -0.008 .. +0.021 | +0.0012 | 0.37 / 0.35 / 0.28 | 0.271 |  |  | 11/16 | -0.003 | +0.016 |  | +1.0 / +0.9 |  |
| MNQ | 5 | h4 * | +0.023 | +0.003 .. +0.043 | +0.0027 | 0.023 / 0.021 / 0.017 | 0.0203 | 1 | 0.99 | 13/16 | +0.010 | +0.035 | False | +2.5 / +2.3 | 0.024 |
| MNQ | 5 | h8 | +0.030 | +0.003 .. +0.056 | +0.0024 | 0.028 / 0.027 / 0.036 | 0.0375 |  |  | 11/16 | +0.018 | +0.042 |  | +2.3 / +2.2 |  |
| MNQ | 5 | h16 | +0.019 | -0.019 .. +0.058 | +0.0011 | 0.32 / 0.32 / 0.35 | 0.357 |  |  | 11/16 | -0.004 | +0.043 |  | +1.1 / +1.0 |  |
| MNQ | 5 | eod | +0.176 | -0.013 .. +0.365 | +0.0021 | 0.068 / 0.067 / 0.08 | 0.0797 |  |  | 12/16 | +0.131 | +0.221 |  | +2.1 / +1.8 |  |
| MNQ | 15 | h1 | +0.012 | -0.004 .. +0.027 | +0.0035 | 0.14 / 0.13 / 0.13 | 0.128 |  |  | 10/16 | -0.005 | +0.028 |  | +1.5 / +1.5 |  |
| MNQ | 15 | h2 * | +0.019 | -0.002 .. +0.040 | +0.0035 | 0.075 / 0.066 / 0.11 | 0.109 | 1 | 1 | 11/16 | -0.002 | +0.040 | False | +1.8 / +1.8 |  |
| MNQ | 15 | h4 | +0.018 | -0.010 .. +0.047 | +0.0020 | 0.21 / 0.21 / 0.4 | 0.398 |  |  | 11/16 | -0.006 | +0.042 |  | +1.2 / +1.3 | 0.050 |
| MNQ | 15 | h8 | -0.004 | -0.044 .. +0.036 | -0.0003 | 0.86 / 0.86 / 0.89 | 0.887 |  |  | 9/16 | -0.010 | +0.003 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h16 | -0.018 | -0.069 .. +0.034 | -0.0012 | 0.5 / 0.51 / 0.6 | 0.579 |  |  | 11/16 | -0.044 | +0.009 |  | -0.7 / -0.7 |  |
| MNQ | 15 | eod | +0.056 | -0.064 .. +0.177 | +0.0013 | 0.36 / 0.34 / 0.5 | 0.491 |  |  | 11/16 | +0.029 | +0.083 |  | +1.0 / +0.9 |  |
| MNQ | 60 | h1 | +0.027 | +0.002 .. +0.051 | +0.0119 | 0.034 / 0.042 / 0.036 | 0.0396 |  |  | 13/16 | +0.014 | +0.039 |  | +2.0 / +2.1 |  |
| MNQ | 60 | h2 | +0.031 | -0.003 .. +0.065 | +0.0096 | 0.075 / 0.081 / 0.058 | 0.063 |  |  | 11/16 | +0.019 | +0.043 |  | +1.7 / +1.8 |  |
| MNQ | 60 | h4 * | +0.052 | +0.009 .. +0.096 | +0.0115 | 0.018 / 0.019 / 0.014 | 0.0135 | 1 | 0.956 | 12/16 | +0.015 | +0.089 | False | +2.3 / +2.4 | 0.059 |
| MNQ | 60 | h8 | +0.049 | -0.001 .. +0.100 | +0.0080 | 0.057 / 0.06 / 0.055 | 0.0529 |  |  | 11/16 | +0.032 | +0.067 |  | +1.8 / +1.9 |  |
| MNQ | 60 | h16 | +0.039 | -0.014 .. +0.092 | +0.0048 | 0.15 / 0.16 / 0.14 | 0.149 |  |  | 11/16 | +0.023 | +0.054 |  | +1.4 / +1.4 |  |
| MNQ | 60 | eod | +0.049 | -0.007 .. +0.105 | +0.0057 | 0.089 / 0.09 / 0.07 | 0.0667 |  |  | 11/16 | +0.029 | +0.068 |  | +1.7 / +1.7 |  |
| MYM | 5 | h1 | -0.004 | -0.017 .. +0.009 | -0.0011 | 0.54 / 0.53 / 0.78 | 0.843 |  |  | 5/8 | n/a | -0.004 |  | -0.6 / -0.6 |  |
| MYM | 5 | h2 | -0.006 | -0.023 .. +0.011 | -0.0010 | 0.51 / 0.51 / 0.61 | 0.592 |  |  | 5/8 | n/a | -0.006 |  | -0.6 / -0.7 |  |
| MYM | 5 | h4 | -0.006 | -0.031 .. +0.019 | -0.0006 | 0.62 / 0.62 / 0.83 | 0.812 |  |  | 4/8 | n/a | -0.006 |  | -0.5 / -0.5 | 0.051 |
| MYM | 5 | h8 | -0.023 | -0.061 .. +0.015 | -0.0016 | 0.23 / 0.22 / 0.37 | 0.345 |  |  | 6/8 | n/a | -0.023 |  | -1.3 / -1.2 |  |
| MYM | 5 | h16 | -0.020 | -0.070 .. +0.029 | -0.0012 | 0.42 / 0.43 / 0.5 | 0.483 |  |  | 6/8 | n/a | -0.020 |  | -0.8 / -0.8 |  |
| MYM | 5 | eod * | +0.172 | -0.059 .. +0.402 | +0.0021 | 0.14 / 0.16 / 0.21 | 0.213 | 1 | 1 | 6/8 | n/a | +0.172 | False | +1.5 / +1.5 |  |
| MYM | 15 | h1 | +0.013 | -0.008 .. +0.034 | +0.0041 | 0.22 / 0.22 / 0.33 | 0.341 |  |  | 5/8 | n/a | +0.013 |  | +1.2 / +1.2 |  |
| MYM | 15 | h2 | +0.020 | -0.011 .. +0.051 | +0.0035 | 0.2 / 0.2 / 0.34 | 0.326 |  |  | 5/8 | n/a | +0.020 |  | +1.4 / +1.3 |  |
| MYM | 15 | h4 * | +0.042 | +0.002 .. +0.081 | +0.0043 | 0.038 / 0.049 / 0.2 | 0.197 | 1 | 0.997 | 7/8 | n/a | +0.042 | False | +2.1 / +2.1 | 0.066 |
| MYM | 15 | h8 | +0.028 | -0.024 .. +0.080 | +0.0022 | 0.29 / 0.31 / 0.41 | 0.416 |  |  | 6/8 | n/a | +0.028 |  | +1.0 / +1.1 |  |
| MYM | 15 | h16 | +0.006 | -0.064 .. +0.076 | +0.0004 | 0.86 / 0.87 / 0.92 | 0.921 |  |  | 4/8 | n/a | +0.006 |  | +0.2 / +0.2 |  |
| MYM | 15 | eod | +0.075 | -0.082 .. +0.232 | +0.0018 | 0.35 / 0.36 / 0.56 | 0.548 |  |  | 6/8 | n/a | +0.075 |  | +0.9 / +0.9 |  |
| MYM | 60 | h1 * | +0.042 | +0.005 .. +0.078 | +0.0182 | 0.026 / 0.029 / 0.015 | 0.0137 | 1 | 0.985 | 7/8 | n/a | +0.042 | False | +2.2 / +2.2 |  |
| MYM | 60 | h2 | +0.027 | -0.020 .. +0.073 | +0.0082 | 0.27 / 0.28 / 0.25 | 0.251 |  |  | 5/8 | n/a | +0.027 |  | +1.1 / +1.1 |  |
| MYM | 60 | h4 | +0.021 | -0.038 .. +0.080 | +0.0047 | 0.48 / 0.5 / 0.49 | 0.484 |  |  | 5/8 | n/a | +0.021 |  | +0.7 / +0.7 | 0.079 |
| MYM | 60 | h8 | +0.031 | -0.046 .. +0.108 | +0.0051 | 0.43 / 0.44 / 0.4 | 0.414 |  |  | 6/8 | n/a | +0.031 |  | +0.8 / +0.8 |  |
| MYM | 60 | h16 | +0.015 | -0.066 .. +0.096 | +0.0019 | 0.72 / 0.73 / 0.7 | 0.708 |  |  | 5/8 | n/a | +0.015 |  | +0.4 / +0.4 |  |
| MYM | 60 | eod | +0.018 | -0.066 .. +0.102 | +0.0022 | 0.67 / 0.68 / 0.64 | 0.646 |  |  | 5/8 | n/a | +0.018 |  | +0.4 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.139 | +0.128 .. +0.150 | +27.8% | +0.306 | 1.6e-133 | 2.83e-130 | 16/16 |
| MES | 5 | h2 | +0.170 | +0.155 .. +0.185 | +24.1% | +0.374 | 2.1e-108 |  | 16/16 |
| MES | 5 | h4 | +0.198 | +0.180 .. +0.216 | +19.9% | +0.449 | 4.4e-105 |  | 16/16 |
| MES | 5 | h8 | +0.244 | +0.221 .. +0.267 | +17.0% | +0.528 | 1.4e-94 |  | 16/16 |
| MES | 5 | h16 | +0.281 | +0.248 .. +0.315 | +13.4% | +0.592 | 1.1e-60 |  | 16/16 |
| MES | 5 | eod | +0.502 | +0.360 .. +0.644 | +5.0% | +0.906 | 3.8e-12 |  | 15/16 |
| MES | 15 | h1 * | +0.123 | +0.107 .. +0.138 | +24.0% | +0.268 | 1.1e-56 | 1.19e-53 | 16/16 |
| MES | 15 | h2 | +0.150 | +0.131 .. +0.169 | +20.5% | +0.329 | 9e-54 |  | 16/16 |
| MES | 15 | h4 | +0.179 | +0.153 .. +0.205 | +17.0% | +0.382 | 6.8e-42 |  | 16/16 |
| MES | 15 | h8 | +0.201 | +0.163 .. +0.238 | +13.0% | +0.420 | 2e-25 |  | 16/16 |
| MES | 15 | h16 | +0.247 | +0.195 .. +0.299 | +10.8% | +0.485 | 7.2e-21 |  | 16/16 |
| MES | 15 | eod | +0.231 | +0.107 .. +0.355 | +4.2% | +0.498 | 0.00027 |  | 14/16 |
| MES | 60 | h1 * | +0.120 | +0.100 .. +0.140 | +23.4% | +0.268 | 1e-31 | 7.69e-29 | 14/16 |
| MES | 60 | h2 | +0.145 | +0.117 .. +0.173 | +19.6% | +0.319 | 2.3e-24 |  | 16/16 |
| MES | 60 | h4 | +0.160 | +0.121 .. +0.199 | +15.1% | +0.348 | 5.4e-15 |  | 14/16 |
| MES | 60 | h8 | +0.145 | +0.101 .. +0.189 | +9.6% | +0.345 | 1.5e-09 |  | 13/16 |
| MES | 60 | h16 | +0.126 | +0.081 .. +0.172 | +6.1% | +0.324 | 2.5e-07 |  | 15/16 |
| MES | 60 | eod | +0.125 | +0.077 .. +0.172 | +5.8% | +0.317 | 7.8e-07 |  | 15/16 |
| MNQ | 5 | h1 * | +0.138 | +0.128 .. +0.149 | +25.8% | +0.292 | 1.8e-147 | 3.47e-144 | 16/16 |
| MNQ | 5 | h2 | +0.166 | +0.152 .. +0.181 | +21.6% | +0.357 | 2.9e-110 |  | 16/16 |
| MNQ | 5 | h4 | +0.207 | +0.186 .. +0.227 | +18.7% | +0.441 | 6.5e-87 |  | 16/16 |
| MNQ | 5 | h8 | +0.252 | +0.222 .. +0.283 | +15.6% | +0.531 | 1.8e-59 |  | 16/16 |
| MNQ | 5 | h16 | +0.304 | +0.249 .. +0.359 | +12.7% | +0.637 | 3.2e-27 |  | 15/16 |
| MNQ | 5 | eod | +0.745 | +0.511 .. +0.980 | +5.9% | +1.458 | 4.9e-10 |  | 13/16 |
| MNQ | 15 | h1 * | +0.122 | +0.110 .. +0.135 | +22.9% | +0.245 | 2.2e-81 | 2.76e-78 | 16/16 |
| MNQ | 15 | h2 | +0.149 | +0.130 .. +0.168 | +19.3% | +0.305 | 2.5e-54 |  | 16/16 |
| MNQ | 15 | h4 | +0.174 | +0.138 .. +0.211 | +15.4% | +0.358 | 7.1e-21 |  | 15/16 |
| MNQ | 15 | h8 | +0.204 | +0.149 .. +0.260 | +12.2% | +0.401 | 5e-13 |  | 14/16 |
| MNQ | 15 | h16 | +0.217 | +0.150 .. +0.284 | +8.6% | +0.425 | 2.1e-10 |  | 15/16 |
| MNQ | 15 | eod | +0.221 | +0.035 .. +0.408 | +3.5% | +0.495 | 0.02 |  | 15/16 |
| MNQ | 60 | h1 * | +0.103 | +0.083 .. +0.123 | +19.5% | +0.232 | 2.2e-24 | 1.36e-21 | 15/16 |
| MNQ | 60 | h2 | +0.125 | +0.097 .. +0.153 | +16.3% | +0.278 | 2.6e-18 |  | 14/16 |
| MNQ | 60 | h4 | +0.137 | +0.100 .. +0.175 | +12.4% | +0.298 | 1.6e-12 |  | 15/16 |
| MNQ | 60 | h8 | +0.131 | +0.085 .. +0.177 | +8.2% | +0.303 | 1.5e-07 |  | 14/16 |
| MNQ | 60 | h16 | +0.132 | +0.085 .. +0.178 | +6.0% | +0.303 | 1.1e-07 |  | 16/16 |
| MNQ | 60 | eod | +0.135 | +0.089 .. +0.181 | +5.9% | +0.305 | 5.1e-08 |  | 16/16 |
| MYM | 5 | h1 | +0.139 | +0.125 .. +0.153 | +26.1% | +0.297 | 2e-82 |  | 8/8 |
| MYM | 5 | h2 * | +0.172 | +0.154 .. +0.189 | +22.5% | +0.361 | 2.3e-85 | 2.97e-82 | 8/8 |
| MYM | 5 | h4 | +0.195 | +0.172 .. +0.219 | +17.8% | +0.422 | 5.8e-37 |  | 8/8 |
| MYM | 5 | h8 | +0.248 | +0.209 .. +0.287 | +15.6% | +0.495 | 2.9e-35 |  | 8/8 |
| MYM | 5 | h16 | +0.284 | +0.227 .. +0.341 | +12.2% | +0.554 | 1.1e-22 |  | 8/8 |
| MYM | 5 | eod | +0.503 | +0.267 .. +0.740 | +4.3% | +1.076 | 3.6e-05 |  | 7/8 |
| MYM | 15 | h1 * | +0.119 | +0.099 .. +0.138 | +22.3% | +0.249 | 5.4e-33 | 4.3e-30 | 8/8 |
| MYM | 15 | h2 | +0.149 | +0.123 .. +0.175 | +19.5% | +0.301 | 5.6e-30 |  | 8/8 |
| MYM | 15 | h4 | +0.161 | +0.119 .. +0.203 | +14.5% | +0.328 | 5.2e-14 |  | 8/8 |
| MYM | 15 | h8 | +0.182 | +0.120 .. +0.243 | +11.1% | +0.352 | 1.8e-08 |  | 7/8 |
| MYM | 15 | h16 | +0.175 | +0.074 .. +0.275 | +7.1% | +0.314 | 0.00075 |  | 7/8 |
| MYM | 15 | eod | +0.231 | -0.005 .. +0.467 | +3.8% | +0.477 | 0.065 |  | 7/8 |
| MYM | 60 | h1 * | +0.132 | +0.101 .. +0.163 | +25.2% | +0.268 | 9.5e-17 | 4.24e-14 | 8/8 |
| MYM | 60 | h2 | +0.151 | +0.108 .. +0.194 | +20.0% | +0.307 | 6.8e-12 |  | 7/8 |
| MYM | 60 | h4 | +0.143 | +0.092 .. +0.195 | +13.3% | +0.325 | 6.9e-08 |  | 6/8 |
| MYM | 60 | h8 | +0.152 | +0.088 .. +0.217 | +9.8% | +0.333 | 1.1e-05 |  | 8/8 |
| MYM | 60 | h16 | +0.138 | +0.067 .. +0.208 | +6.5% | +0.290 | 0.00017 |  | 8/8 |
| MYM | 60 | eod | +0.138 | +0.065 .. +0.212 | +6.2% | +0.288 | 0.00029 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.66 pts | +0.20 .. +1.13 | 0.0048 |
| MES | 15 | +0.36 pts | -0.21 .. +0.94 | 0.22 |
| MES | 60 | +1.51 pts | +0.59 .. +2.44 | 0.0017 |
| MNQ | 5 | +0.36 pts | -0.01 .. +0.74 | 0.058 |
| MNQ | 15 | +0.70 pts | +0.17 .. +1.23 | 0.012 |
| MNQ | 60 | +1.29 pts | +0.42 .. +2.17 | 0.0051 |
| MYM | 5 | -0.14 pts | -0.66 .. +0.38 | 0.82 |
| MYM | 15 | +0.53 pts | -0.29 .. +1.35 | 0.21 |
| MYM | 60 | +1.59 pts | +0.34 .. +2.84 | 0.018 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 50521 | -0.008 | 0.328 | -0.16 | -3.66 | -3.54 | -3.76 | -3.54 |
| MES | 5 | h2 | event | with signal | 50521 | -0.010 | 0.328 | -0.25 | -3.75 | -3.62 | -3.86 | -3.57 |
| MES | 5 | h4 | event | with signal | 50521 | -0.005 | 0.328 | -0.08 | -3.58 | -3.57 | -3.58 | -3.40 |
| MES | 5 | h8 | event | with signal | 50521 | -0.001 | 0.328 | +0.03 | -3.47 | -3.66 | -3.31 | -3.30 |
| MES | 5 | h16 | event | with signal | 50521 | -0.017 | 0.328 | +0.09 | -3.41 | -3.91 | -3.00 | -3.22 |
| MES | 5 | eod | event | with signal | 50521 | +0.140 | 0.328 | +1.17 | -2.33 | -3.51 | -1.35 | -2.33 |
| MES | 15 | h1 | event | with signal | 25694 | +0.001 | 0.202 | +0.15 | -3.35 | -3.61 | -3.11 | -3.20 |
| MES | 15 | h2 | event | with signal | 25694 | +0.003 | 0.202 | +0.20 | -3.30 | -3.70 | -2.92 | -3.12 |
| MES | 15 | h4 | event | with signal | 25694 | +0.010 | 0.202 | +0.62 | -2.88 | -3.62 | -2.19 | -2.70 |
| MES | 15 | h8 | event | with signal | 25694 | +0.001 | 0.202 | +0.28 | -3.22 | -3.52 | -2.94 | -2.99 |
| MES | 15 | h16 | event | against signal | 25694 | +0.018 | 0.202 | -0.13 | -3.63 | -3.19 | -4.05 | -3.87 |
| MES | 15 | eod | event | with signal | 25694 | +0.037 | 0.202 | +0.73 | -2.77 | -3.42 | -2.17 | -2.91 |
| MES | 60 | h1 | event | with signal | 8409 | +0.021 | 0.099 | +0.52 | -2.98 | -3.09 | -2.88 | -2.95 |
| MES | 60 | h2 | event | with signal | 8409 | +0.026 | 0.099 | +0.63 | -2.87 | -2.78 | -2.94 | -2.70 |
| MES | 60 | h4 | event | with signal | 8409 | +0.013 | 0.099 | -0.02 | -3.52 | -3.48 | -3.55 | -3.23 |
| MES | 60 | h8 | event | with signal | 8409 | +0.007 | 0.099 | +0.16 | -3.34 | -3.08 | -3.60 | -2.92 |
| MES | 60 | h16 | event | with signal | 8409 | -0.004 | 0.099 | -0.50 | -4.00 | -3.26 | -4.70 | -3.90 |
| MES | 60 | eod | event | with signal | 8409 | +0.003 | 0.099 | -0.06 | -3.56 | -3.08 | -4.02 | -3.27 |
| MNQ | 5 | h1 | event | with signal | 65261 | +0.003 | 0.156 | +0.04 | -1.96 | -1.99 | -1.92 | -1.90 |
| MNQ | 5 | h2 | event | with signal | 65261 | -0.001 | 0.156 | -0.08 | -2.08 | -2.04 | -2.13 | -1.98 |
| MNQ | 5 | h4 | event | with signal | 65261 | +0.019 | 0.156 | +0.24 | -1.76 | -1.94 | -1.53 | -1.71 |
| MNQ | 5 | h8 | event | with signal | 65261 | +0.033 | 0.156 | +0.45 | -1.55 | -1.93 | -1.07 | -1.58 |
| MNQ | 5 | h16 | event | with signal | 65261 | +0.026 | 0.156 | +0.43 | -1.57 | -2.01 | -1.02 | -1.64 |
| MNQ | 5 | eod | event | with signal | 65261 | +0.221 | 0.156 | +2.78 | +0.78 | -1.61 | +3.82 | +0.37 |
| MNQ | 15 | h1 | event | with signal | 29756 | +0.008 | 0.086 | +0.57 | -1.43 | -2.00 | -0.79 | -1.34 |
| MNQ | 15 | h2 | event | with signal | 29756 | +0.017 | 0.086 | +0.71 | -1.29 | -2.03 | -0.44 | -1.22 |
| MNQ | 15 | h4 | event | with signal | 29756 | +0.018 | 0.086 | +0.98 | -1.02 | -2.03 | +0.14 | -1.00 |
| MNQ | 15 | h8 | event | against signal | 29756 | +0.001 | 0.086 | -0.52 | -2.52 | -2.05 | -3.06 | -2.46 |
| MNQ | 15 | h16 | event | against signal | 29756 | +0.017 | 0.086 | -0.70 | -2.70 | -1.89 | -3.63 | -2.71 |
| MNQ | 15 | eod | event | with signal | 29756 | +0.075 | 0.086 | +2.67 | +0.67 | -1.72 | +3.42 | +0.28 |
| MNQ | 60 | h1 | event | with signal | 9903 | +0.027 | 0.041 | +1.53 | -0.47 | -1.56 | +0.68 | -0.47 |
| MNQ | 60 | h2 | event | with signal | 9903 | +0.028 | 0.041 | +1.51 | -0.49 | -1.45 | +0.53 | -0.31 |
| MNQ | 60 | h4 | event | with signal | 9903 | +0.046 | 0.041 | +2.59 | +0.59 | -1.73 | +3.06 | +0.93 |
| MNQ | 60 | h8 | event | with signal | 9903 | +0.042 | 0.041 | +2.74 | +0.74 | -1.37 | +2.98 | +1.19 |
| MNQ | 60 | h16 | event | with signal | 9903 | +0.037 | 0.041 | +2.27 | +0.27 | -1.41 | +2.07 | +0.49 |
| MNQ | 60 | eod | event | with signal | 9903 | +0.043 | 0.041 | +2.90 | +0.90 | -1.38 | +3.32 | +1.30 |
| MYM | 5 | h1 | event | against signal | 30549 | +0.011 | 0.188 | +0.15 | -1.85 | +nan | -1.85 | -1.93 |
| MYM | 5 | h2 | event | against signal | 30549 | +0.014 | 0.188 | +0.19 | -1.81 | +nan | -1.81 | -1.89 |
| MYM | 5 | h4 | event | against signal | 30549 | +0.014 | 0.188 | +0.10 | -1.90 | +nan | -1.90 | -1.98 |
| MYM | 5 | h8 | event | against signal | 30549 | +0.028 | 0.188 | +0.20 | -1.80 | +nan | -1.80 | -1.85 |
| MYM | 5 | h16 | event | against signal | 30549 | +0.029 | 0.188 | +0.23 | -1.77 | +nan | -1.77 | -1.86 |
| MYM | 5 | eod | event | with signal | 30549 | +0.172 | 0.188 | +0.49 | -1.51 | +nan | -1.51 | -1.61 |
| MYM | 15 | h1 | event | with signal | 14135 | +0.008 | 0.108 | +0.28 | -1.72 | +nan | -1.72 | -1.62 |
| MYM | 15 | h2 | event | with signal | 14135 | +0.014 | 0.108 | +0.30 | -1.70 | +nan | -1.70 | -1.59 |
| MYM | 15 | h4 | event | with signal | 14135 | +0.040 | 0.108 | +1.12 | -0.88 | +nan | -0.88 | -0.84 |
| MYM | 15 | h8 | event | with signal | 14135 | +0.027 | 0.108 | +0.81 | -1.19 | +nan | -1.19 | -1.16 |
| MYM | 15 | h16 | event | with signal | 14135 | +0.011 | 0.108 | +0.53 | -1.47 | +nan | -1.47 | -1.53 |
| MYM | 15 | eod | event | with signal | 14135 | +0.082 | 0.108 | +1.59 | -0.41 | +nan | -0.41 | -0.48 |
| MYM | 60 | h1 | event | with signal | 4610 | +0.042 | 0.052 | +0.91 | -1.09 | +nan | -1.09 | -1.10 |
| MYM | 60 | h2 | event | with signal | 4610 | +0.022 | 0.052 | +0.24 | -1.76 | +nan | -1.76 | -1.56 |
| MYM | 60 | h4 | event | with signal | 4610 | +0.016 | 0.052 | -0.34 | -2.34 | +nan | -2.34 | -2.06 |
| MYM | 60 | h8 | event | with signal | 4610 | +0.024 | 0.052 | +0.14 | -1.86 | +nan | -1.86 | -1.49 |
| MYM | 60 | h16 | event | with signal | 4610 | +0.027 | 0.052 | +0.13 | -1.87 | +nan | -1.87 | -2.12 |
| MYM | 60 | eod | event | with signal | 4610 | +0.029 | 0.052 | +0.31 | -1.69 | +nan | -1.69 | -1.83 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.468 | -1.604 | -1.632 | -1.597 | -1.542 | +0.000 | -0.013 | -0.015 | -0.010 | -0.008 | -0.019 |
| MES | 15 | -1.323 | -1.446 | -1.521 | -1.509 | -1.472 | +0.000 | +0.002 | +0.004 | +0.011 | -0.004 | -0.032 |
| MES | 60 | -1.312 | -1.385 | -1.465 | -1.499 | -1.476 | +0.000 | +0.024 | +0.029 | +0.005 | -0.058 | -0.146 |
| MNQ | 5 | -1.507 | -1.658 | -1.685 | -1.660 | -1.598 | +0.000 | -0.006 | -0.010 | +0.008 | +0.020 | +0.016 |
| MNQ | 15 | -1.361 | -1.488 | -1.562 | -1.549 | -1.518 | +0.000 | +0.006 | +0.014 | +0.019 | -0.006 | -0.033 |
| MNQ | 60 | -1.320 | -1.381 | -1.450 | -1.486 | -1.482 | +0.000 | +0.028 | +0.028 | +0.052 | -0.131 | -0.071 |
| MYM | 5 | -1.481 | -1.629 | -1.666 | -1.637 | -1.588 | +0.000 | -0.014 | -0.018 | -0.023 | -0.041 | -0.043 |
| MYM | 15 | -1.348 | -1.464 | -1.534 | -1.541 | -1.514 | +0.000 | +0.005 | +0.012 | +0.038 | +0.020 | -0.001 |
| MYM | 60 | -1.277 | -1.380 | -1.471 | -1.521 | -1.512 | +0.000 | +0.044 | +0.030 | +0.008 | +0.077 | +0.248 |

## Calibration

- MES 5-min: 1036209 bars, 50521 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342156 bars, 25694 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83351 bars, 8409 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034460 bars, 65261 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342000 bars, 29756 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83349 bars, 9903 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519008 bars, 30549 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171396 bars, 14135 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41624 bars, 4610 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
