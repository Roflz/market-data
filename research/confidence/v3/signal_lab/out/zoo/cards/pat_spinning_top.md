# Impact card: pat_spinning_top

candle pattern spinning_top (no direction): body <= 0.3 x range AND both shadows >= body AND range >= 0.5 x avgR10 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.009 R20 over the next 2 bars (10 min), p=0.023; we would catch an effect of 0.014 R20 or more 80% of the time).
- MES 5-min size: the market moves 2% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.013 R20, CONFIRMED, q=4.26e-05, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.14 at recent bar sizes, 90% range up to $0.49); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.015 R20 over the next 2 bars (30 min), p=0.091; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.041).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.11 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.130 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.077 R20 over the next 16 bars (16 h), p=0.028; we would catch an effect of 0.046 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.13).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.47 at recent bar sizes, 90% range up to $4.70); about 3.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.007 R20 over the next 2 bars (10 min), p=0.36; we would catch an effect of 0.017 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.54).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.15 at recent bar sizes, 90% range up to $0.91); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.29 at recent bar sizes, 90% range up to $1.39); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.028 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.050 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.023 R20, possible, q=0.132, 12 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.05 at recent bar sizes, 90% range up to $7.11); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.007 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.026 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.33).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.07 at recent bar sizes, 90% range up to $0.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.024 R20 over the next 2 bars (30 min), p=0.22; we would catch an effect of 0.056 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.40 at recent bar sizes, 90% range up to $1.62); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.023 R20 over the next 1 bar (1 h), p=0.36; we would catch an effect of 0.068 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.35).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.79 at recent bar sizes, 90% range up to $4.42); about 24.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.004 | -0.001 .. +0.008 | +0.0016 | 0.13 / 0.12 / 0.12 | 0.118 |  |  | 10/16 | +0.000 | +0.007 |  | +1.5 / +1.5 |  |
| MES | 5 | h2 * | +0.009 | +0.003 .. +0.016 | +0.0029 | 0.0028 / 0.0038 / 0.0042 | 0.00313 | 0.572 | 0.536 | 11/16 | +0.001 | +0.017 | False | +2.9 / +3.0 |  |
| MES | 5 | h4 | +0.009 | -0.001 .. +0.019 | +0.0020 | 0.067 / 0.078 / 0.067 | 0.0659 |  |  | 11/16 | +0.002 | +0.016 |  | +2.0 / +1.8 | 0.014 |
| MES | 5 | h8 | +0.006 | -0.010 .. +0.022 | +0.0009 | 0.46 / 0.47 / 0.42 | 0.426 |  |  | 8/16 | -0.007 | +0.019 |  | +0.9 / +0.7 |  |
| MES | 5 | h16 | +0.021 | -0.005 .. +0.047 | +0.0021 | 0.12 / 0.11 / 0.052 | 0.0552 |  |  | 8/16 | -0.002 | +0.043 |  | +2.2 / +1.6 |  |
| MES | 5 | eod | +0.031 | -0.209 .. +0.270 | +0.0006 | 0.8 / 0.81 / 0.74 | 0.748 |  |  | 8/16 | -0.021 | +0.082 |  | +0.7 / +0.3 |  |
| MES | 15 | h1 | +0.005 | -0.002 .. +0.012 | +0.0023 | 0.18 / 0.2 / 0.22 | 0.219 |  |  | 8/16 | +0.002 | +0.008 |  | +1.3 / +1.3 |  |
| MES | 15 | h2 * | +0.015 | +0.004 .. +0.025 | +0.0046 | 0.0089 / 0.0078 / 0.013 | 0.0167 | 1 | 0.869 | 13/16 | +0.009 | +0.020 | False | +2.7 / +2.6 |  |
| MES | 15 | h4 | +0.009 | -0.008 .. +0.026 | +0.0019 | 0.29 / 0.29 / 0.3 | 0.295 |  |  | 8/16 | -0.002 | +0.020 |  | +1.1 / +1.1 | 0.023 |
| MES | 15 | h8 | +0.019 | -0.003 .. +0.041 | +0.0029 | 0.088 / 0.095 / 0.11 | 0.114 |  |  | 12/16 | +0.000 | +0.038 |  | +1.7 / +1.7 |  |
| MES | 15 | h16 | +0.031 | -0.006 .. +0.069 | +0.0032 | 0.1 / 0.12 / 0.077 | 0.0815 |  |  | 8/16 | +0.024 | +0.038 |  | +1.9 / +1.6 |  |
| MES | 15 | eod | +0.029 | -0.122 .. +0.180 | +0.0012 | 0.71 / 0.71 / 0.55 | 0.551 |  |  | 7/16 | -0.093 | +0.150 |  | +0.7 / +0.4 |  |
| MES | 60 | h1 | +0.004 | -0.011 .. +0.020 | +0.0021 | 0.59 / 0.58 / 0.59 | 0.592 |  |  | 9/16 | +0.004 | +0.005 |  | +0.5 / +0.5 |  |
| MES | 60 | h2 | +0.008 | -0.013 .. +0.030 | +0.0028 | 0.45 / 0.46 / 0.46 | 0.465 |  |  | 11/16 | +0.003 | +0.014 |  | +0.7 / +0.8 |  |
| MES | 60 | h4 | +0.009 | -0.022 .. +0.040 | +0.0021 | 0.58 / 0.58 / 0.57 | 0.565 |  |  | 11/16 | +0.014 | +0.004 |  | +0.6 / +0.6 | 0.046 |
| MES | 60 | h8 | +0.043 | -0.001 .. +0.088 | +0.0075 | 0.054 / 0.06 / 0.045 | 0.0445 |  |  | 13/16 | +0.068 | +0.019 |  | +2.0 / +1.9 |  |
| MES | 60 | h16 * | +0.077 | +0.025 .. +0.130 | +0.0103 | 0.0039 / 0.0046 / 0.0032 | 0.00417 | 0.683 | 0.615 | 14/16 | +0.094 | +0.061 | False | +2.9 / +2.9 |  |
| MES | 60 | eod | +0.066 | +0.012 .. +0.121 | +0.0084 | 0.017 / 0.018 / 0.014 | 0.0156 |  |  | 14/16 | +0.079 | +0.053 |  | +2.5 / +2.4 |  |
| MNQ | 5 | h1 | +0.003 | -0.002 .. +0.007 | +0.0010 | 0.21 / 0.22 / 0.34 | 0.334 |  |  | 10/16 | -0.001 | +0.006 |  | +1.2 / +1.2 |  |
| MNQ | 5 | h2 * | +0.007 | +0.000 .. +0.013 | +0.0017 | 0.036 / 0.037 / 0.098 | 0.0979 | 1 | 0.999 | 9/16 | +0.001 | +0.013 | False | +2.1 / +2.1 |  |
| MNQ | 5 | h4 | +0.010 | -0.002 .. +0.023 | +0.0017 | 0.11 / 0.094 / 0.11 | 0.11 |  |  | 7/16 | -0.008 | +0.028 |  | +2.1 / +1.6 | 0.017 |
| MNQ | 5 | h8 | +0.016 | -0.005 .. +0.037 | +0.0018 | 0.14 / 0.12 / 0.094 | 0.092 |  |  | 8/16 | -0.007 | +0.039 |  | +2.3 / +1.5 |  |
| MNQ | 5 | h16 | +0.024 | -0.008 .. +0.056 | +0.0019 | 0.14 / 0.13 / 0.075 | 0.0735 |  |  | 8/16 | +0.000 | +0.048 |  | +2.4 / +1.5 |  |
| MNQ | 5 | eod | +0.130 | -0.181 .. +0.441 | +0.0021 | 0.41 / 0.41 / 0.15 | 0.162 |  |  | 10/16 | -0.093 | +0.350 |  | +2.6 / +0.8 |  |
| MNQ | 15 | h1 | +0.001 | -0.007 .. +0.008 | +0.0002 | 0.89 / 0.89 / 0.91 | 0.924 |  |  | 10/16 | -0.003 | +0.004 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h2 * | +0.008 | -0.003 .. +0.019 | +0.0018 | 0.16 / 0.15 / 0.33 | 0.325 | 1 | 1 | 10/16 | +0.003 | +0.013 | False | +1.3 / +1.4 |  |
| MNQ | 15 | h4 | +0.001 | -0.017 .. +0.019 | +0.0001 | 0.92 / 0.92 / 0.95 | 0.94 |  |  | 8/16 | -0.007 | +0.009 |  | +0.1 / +0.1 | 0.030 |
| MNQ | 15 | h8 | +0.000 | -0.025 .. +0.026 | +0.0000 | 0.98 / 0.98 / 0.99 | 0.985 |  |  | 9/16 | -0.013 | +0.014 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h16 | +0.001 | -0.050 .. +0.052 | +0.0001 | 0.96 / 0.96 / 0.96 | 0.954 |  |  | 7/16 | -0.053 | +0.055 |  | +0.1 / +0.0 |  |
| MNQ | 15 | eod | +0.062 | -0.148 .. +0.271 | +0.0018 | 0.56 / 0.54 / 0.34 | 0.345 |  |  | 7/16 | -0.212 | +0.334 |  | +1.3 / +0.6 |  |
| MNQ | 60 | h1 | +0.008 | -0.011 .. +0.026 | +0.0034 | 0.42 / 0.4 / 0.37 | 0.379 |  |  | 8/16 | +0.017 | -0.002 |  | +0.8 / +0.8 |  |
| MNQ | 60 | h2 | +0.001 | -0.025 .. +0.027 | +0.0003 | 0.95 / 0.95 / 0.95 | 0.944 |  |  | 8/16 | +0.021 | -0.020 |  | +0.1 / +0.1 |  |
| MNQ | 60 | h4 | +0.012 | -0.025 .. +0.050 | +0.0027 | 0.53 / 0.52 / 0.48 | 0.487 |  |  | 9/16 | +0.009 | +0.015 |  | +0.7 / +0.6 | 0.050 |
| MNQ | 60 | h8 * | +0.028 | -0.024 .. +0.079 | +0.0045 | 0.29 / 0.3 / 0.24 | 0.243 | 1 | 1 | 10/16 | +0.024 | +0.031 | False | +1.1 / +1.1 |  |
| MNQ | 60 | h16 | +0.030 | -0.030 .. +0.090 | +0.0037 | 0.33 / 0.33 / 0.29 | 0.289 |  |  | 9/16 | +0.034 | +0.026 |  | +1.0 / +1.0 |  |
| MNQ | 60 | eod | +0.029 | -0.031 .. +0.088 | +0.0034 | 0.34 / 0.35 / 0.32 | 0.319 |  |  | 10/16 | +0.028 | +0.029 |  | +1.0 / +0.9 |  |
| MYM | 5 | h1 | +0.003 | -0.003 .. +0.010 | +0.0012 | 0.34 / 0.33 / 0.41 | 0.399 |  |  | 5/8 | n/a | +0.003 |  | +1.0 / +1.0 |  |
| MYM | 5 | h2 * | +0.007 | -0.004 .. +0.018 | +0.0016 | 0.22 / 0.23 / 0.25 | 0.241 | 1 | 1 | 4/8 | n/a | +0.007 | False | +1.5 / +1.2 |  |
| MYM | 5 | h4 | +0.013 | -0.010 .. +0.035 | +0.0019 | 0.26 / 0.27 / 0.21 | 0.212 |  |  | 3/8 | n/a | +0.013 |  | +1.9 / +1.1 | 0.026 |
| MYM | 5 | h8 | +0.017 | -0.022 .. +0.056 | +0.0019 | 0.38 / 0.39 / 0.21 | 0.221 |  |  | 3/8 | n/a | +0.017 |  | +1.8 / +0.9 |  |
| MYM | 5 | h16 | +0.017 | -0.038 .. +0.072 | +0.0015 | 0.54 / 0.55 / 0.32 | 0.332 |  |  | 3/8 | n/a | +0.017 |  | +1.2 / +0.6 |  |
| MYM | 5 | eod | +0.029 | -0.285 .. +0.343 | +0.0006 | 0.86 / 0.86 / 0.76 | 0.757 |  |  | 4/8 | n/a | +0.029 |  | +0.4 / +0.2 |  |
| MYM | 15 | h1 | +0.006 | -0.005 .. +0.017 | +0.0025 | 0.27 / 0.25 / 0.33 | 0.332 |  |  | 6/8 | n/a | +0.006 |  | +1.1 / +1.1 |  |
| MYM | 15 | h2 * | +0.024 | +0.008 .. +0.040 | +0.0053 | 0.0037 / 0.0054 / 0.04 | 0.0369 | 1 | 0.573 | 7/8 | n/a | +0.024 | False | +2.8 / +2.9 |  |
| MYM | 15 | h4 | +0.019 | -0.008 .. +0.046 | +0.0025 | 0.17 / 0.2 / 0.33 | 0.337 |  |  | 5/8 | n/a | +0.019 |  | +1.5 / +1.4 | 0.056 |
| MYM | 15 | h8 | +0.029 | -0.019 .. +0.078 | +0.0030 | 0.24 / 0.24 / 0.22 | 0.233 |  |  | 5/8 | n/a | +0.029 |  | +1.6 / +1.2 |  |
| MYM | 15 | h16 | +0.020 | -0.084 .. +0.124 | +0.0015 | 0.7 / 0.7 / 0.56 | 0.575 |  |  | 3/8 | n/a | +0.020 |  | +0.8 / +0.4 |  |
| MYM | 15 | eod | +0.073 | -0.203 .. +0.348 | +0.0022 | 0.6 / 0.61 / 0.38 | 0.384 |  |  | 4/8 | n/a | +0.073 |  | +1.1 / +0.5 |  |
| MYM | 60 | h1 * | +0.023 | -0.001 .. +0.047 | +0.0105 | 0.058 / 0.059 / 0.055 | 0.0564 | 1 | 0.998 | 6/8 | n/a | +0.023 | False | +1.9 / +1.9 |  |
| MYM | 60 | h2 | +0.022 | -0.011 .. +0.056 | +0.0071 | 0.19 / 0.19 / 0.21 | 0.199 |  |  | 6/8 | n/a | +0.022 |  | +1.3 / +1.3 |  |
| MYM | 60 | h4 | -0.014 | -0.064 .. +0.036 | -0.0033 | 0.58 / 0.58 / 0.57 | 0.563 |  |  | 4/8 | n/a | -0.014 |  | -0.6 / -0.6 | 0.068 |
| MYM | 60 | h8 | -0.015 | -0.084 .. +0.054 | -0.0025 | 0.68 / 0.67 / 0.66 | 0.663 |  |  | 3/8 | n/a | -0.015 |  | -0.4 / -0.4 |  |
| MYM | 60 | h16 | -0.036 | -0.112 .. +0.039 | -0.0046 | 0.34 / 0.35 / 0.36 | 0.357 |  |  | 4/8 | n/a | -0.036 |  | -0.9 / -0.9 |  |
| MYM | 60 | eod | -0.028 | -0.106 .. +0.050 | -0.0034 | 0.48 / 0.48 / 0.5 | 0.506 |  |  | 4/8 | n/a | -0.028 |  | -0.7 / -0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.009 | +0.006 .. +0.012 | +1.8% | +0.009 | 4.9e-05 |  | 13/16 |
| MES | 5 | h2 * | +0.013 | +0.008 .. +0.018 | +1.9% | +0.018 | 1.6e-07 | 4.26e-05 | 14/16 |
| MES | 5 | h4 | +0.015 | +0.007 .. +0.022 | +1.5% | +0.025 | 0.0012 |  | 13/16 |
| MES | 5 | h8 | +0.008 | -0.004 .. +0.021 | +0.6% | +0.024 | 0.76 |  | 10/16 |
| MES | 5 | h16 | +0.003 | -0.017 .. +0.024 | +0.2% | +0.021 | 0.74 |  | 9/16 |
| MES | 5 | eod | -0.083 | -0.276 .. +0.111 | -0.8% | -0.219 | 0.4 |  | 6/16 |
| MES | 15 | h1 * | +0.009 | +0.004 .. +0.014 | +1.8% | +0.015 | 0.0068 | 0.952 | 13/16 |
| MES | 15 | h2 | +0.010 | +0.003 .. +0.018 | +1.4% | +0.019 | 0.067 |  | 13/16 |
| MES | 15 | h4 | +0.009 | -0.005 .. +0.023 | +0.9% | +0.023 | 0.37 |  | 11/16 |
| MES | 15 | h8 | +0.003 | -0.016 .. +0.022 | +0.2% | +0.020 | 0.96 |  | 9/16 |
| MES | 15 | h16 | +0.002 | -0.029 .. +0.033 | +0.1% | +0.008 | 0.89 |  | 10/16 |
| MES | 15 | eod | -0.041 | -0.169 .. +0.086 | -0.8% | -0.057 | 0.52 |  | 7/16 |
| MES | 60 | h1 * | +0.016 | +0.005 .. +0.027 | +3.1% | +0.018 | 0.022 | 1 | 10/16 |
| MES | 60 | h2 | +0.016 | -0.001 .. +0.032 | +2.1% | +0.020 | 0.061 |  | 10/16 |
| MES | 60 | h4 | +0.012 | -0.010 .. +0.034 | +1.1% | +0.025 | 0.32 |  | 9/16 |
| MES | 60 | h8 | +0.011 | -0.017 .. +0.039 | +0.7% | +0.029 | 0.78 |  | 8/16 |
| MES | 60 | h16 | -0.003 | -0.039 .. +0.033 | -0.2% | +0.008 | 0.86 |  | 9/16 |
| MES | 60 | eod | +0.000 | -0.036 .. +0.037 | +0.0% | +0.005 | 0.98 |  | 8/16 |
| MNQ | 5 | h1 | -0.000 | -0.004 .. +0.003 | -0.0% | +0.003 | 0.97 |  | 7/16 |
| MNQ | 5 | h2 | -0.004 | -0.011 .. +0.002 | -0.5% | +0.003 | 0.31 |  | 8/16 |
| MNQ | 5 | h4 | -0.005 | -0.017 .. +0.007 | -0.5% | -0.001 | 0.59 |  | 9/16 |
| MNQ | 5 | h8 | -0.018 | -0.043 .. +0.007 | -1.1% | -0.018 | 0.16 |  | 8/16 |
| MNQ | 5 | h16 * | -0.038 | -0.082 .. +0.006 | -1.6% | -0.056 | 0.09 | 1 | 10/16 |
| MNQ | 5 | eod | -0.245 | -0.552 .. +0.062 | -2.0% | -0.568 | 0.12 |  | 8/16 |
| MNQ | 15 | h1 | +0.006 | -0.000 .. +0.012 | +1.1% | +0.009 | 0.36 |  | 11/16 |
| MNQ | 15 | h2 | +0.004 | -0.008 .. +0.017 | +0.6% | +0.008 | 0.74 |  | 11/16 |
| MNQ | 15 | h4 | +0.000 | -0.028 .. +0.029 | +0.0% | +0.002 | 1 |  | 11/16 |
| MNQ | 15 | h8 | -0.006 | -0.050 .. +0.039 | -0.3% | -0.008 | 0.8 |  | 7/16 |
| MNQ | 15 | h16 * | -0.030 | -0.081 .. +0.020 | -1.2% | -0.042 | 0.24 | 1 | 9/16 |
| MNQ | 15 | eod | -0.106 | -0.320 .. +0.109 | -1.7% | -0.148 | 0.33 |  | 8/16 |
| MNQ | 60 | h1 * | +0.023 | +0.010 .. +0.036 | +4.3% | +0.023 | 0.00075 | 0.132 | 12/16 |
| MNQ | 60 | h2 | +0.020 | +0.001 .. +0.038 | +2.6% | +0.027 | 0.044 |  | 9/16 |
| MNQ | 60 | h4 | +0.015 | -0.012 .. +0.041 | +1.3% | +0.033 | 0.3 |  | 8/16 |
| MNQ | 60 | h8 | +0.007 | -0.030 .. +0.045 | +0.5% | +0.020 | 0.82 |  | 9/16 |
| MNQ | 60 | h16 | -0.006 | -0.046 .. +0.035 | -0.3% | +0.005 | 0.78 |  | 8/16 |
| MNQ | 60 | eod | -0.009 | -0.049 .. +0.031 | -0.4% | +0.006 | 0.67 |  | 8/16 |
| MYM | 5 | h1 * | -0.005 | -0.010 .. -0.000 | -0.9% | -0.010 | 0.055 | 1 | 5/8 |
| MYM | 5 | h2 | -0.002 | -0.012 .. +0.008 | -0.3% | -0.006 | 0.66 |  | 3/8 |
| MYM | 5 | h4 | -0.004 | -0.024 .. +0.017 | -0.3% | -0.004 | 0.74 |  | 3/8 |
| MYM | 5 | h8 | -0.008 | -0.046 .. +0.031 | -0.5% | -0.006 | 0.69 |  | 1/8 |
| MYM | 5 | h16 | -0.024 | -0.075 .. +0.028 | -1.0% | -0.018 | 0.38 |  | 3/8 |
| MYM | 5 | eod | -0.184 | -0.460 .. +0.092 | -1.6% | -0.314 | 0.19 |  | 4/8 |
| MYM | 15 | h1 | +0.001 | -0.007 .. +0.009 | +0.3% | +0.005 | 0.95 |  | 5/8 |
| MYM | 15 | h2 | -0.000 | -0.016 .. +0.016 | -0.0% | +0.006 | 1 |  | 3/8 |
| MYM | 15 | h4 | -0.003 | -0.037 .. +0.030 | -0.3% | +0.003 | 0.85 |  | 4/8 |
| MYM | 15 | h8 * | -0.007 | -0.060 .. +0.047 | -0.4% | -0.004 | 0.81 | 1 | 3/8 |
| MYM | 15 | h16 | -0.009 | -0.103 .. +0.085 | -0.4% | -0.004 | 0.85 |  | 3/8 |
| MYM | 15 | eod | -0.012 | -0.262 .. +0.237 | -0.2% | -0.037 | 0.94 |  | 1/8 |
| MYM | 60 | h1 | +0.009 | -0.008 .. +0.025 | +1.7% | +0.016 | 0.71 |  | 4/8 |
| MYM | 60 | h2 | +0.016 | -0.008 .. +0.040 | +2.1% | +0.027 | 0.55 |  | 5/8 |
| MYM | 60 | h4 * | +0.046 | +0.012 .. +0.079 | +4.2% | +0.062 | 0.058 | 1 | 6/8 |
| MYM | 60 | h8 | +0.046 | -0.001 .. +0.092 | +2.9% | +0.082 | 0.21 |  | 5/8 |
| MYM | 60 | h16 | +0.051 | -0.003 .. +0.105 | +2.4% | +0.077 | 0.1 |  | 7/8 |
| MYM | 60 | eod | +0.052 | -0.001 .. +0.104 | +2.3% | +0.076 | 0.079 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.25 pts | -0.06 .. +0.57 | 0.11 |
| MES | 15 | +0.06 pts | -0.45 .. +0.57 | 0.83 |
| MES | 60 | +0.10 pts | -0.78 .. +0.99 | 0.95 |
| MNQ | 5 | +0.20 pts | -0.08 .. +0.47 | 0.16 |
| MNQ | 15 | +0.13 pts | -0.31 .. +0.58 | 0.55 |
| MNQ | 60 | +0.11 pts | -0.75 .. +0.97 | 0.8 |
| MYM | 5 | +0.26 pts | -0.15 .. +0.67 | 0.22 |
| MYM | 15 | +0.01 pts | -0.61 .. +0.62 | 0.98 |
| MYM | 60 | +0.15 pts | -1.19 .. +1.49 | 0.94 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 119087 | +0.004 | 0.250 | +0.10 | -3.40 | -3.48 | -3.36 | -3.40 |
| MES | 5 | h2 | event | long | 119087 | +0.012 | 0.250 | +0.22 | -3.28 | -3.44 | -3.18 | -3.29 |
| MES | 5 | h4 | event | long | 119087 | +0.017 | 0.250 | +0.28 | -3.22 | -3.39 | -3.13 | -3.27 |
| MES | 5 | h8 | event | long | 119087 | +0.024 | 0.250 | +0.35 | -3.15 | -3.38 | -3.02 | -3.27 |
| MES | 5 | h16 | event | long | 119087 | +0.058 | 0.250 | +0.73 | -2.77 | -3.16 | -2.55 | -3.08 |
| MES | 5 | eod | event | long | 119087 | +0.380 | 0.250 | +4.85 | +1.35 | -0.33 | +2.28 | +0.80 |
| MES | 15 | h1 | event | long | 52347 | +0.009 | 0.177 | +0.15 | -3.35 | -3.43 | -3.29 | -3.42 |
| MES | 15 | h2 | event | long | 52347 | +0.022 | 0.177 | +0.30 | -3.20 | -3.31 | -3.12 | -3.32 |
| MES | 15 | h4 | event | long | 52347 | +0.028 | 0.177 | +0.41 | -3.09 | -3.29 | -2.93 | -3.31 |
| MES | 15 | h8 | event | long | 52347 | +0.058 | 0.177 | +0.95 | -2.55 | -2.98 | -2.21 | -2.98 |
| MES | 15 | h16 | event | long | 52347 | +0.107 | 0.177 | +1.58 | -1.92 | -2.28 | -1.62 | -2.61 |
| MES | 15 | eod | event | long | 52347 | +0.287 | 0.177 | +4.61 | +1.11 | -0.68 | +2.53 | -0.02 |
| MES | 60 | h1 | event | long | 13261 | +0.014 | 0.097 | +0.38 | -3.12 | -3.12 | -3.13 | -3.35 |
| MES | 60 | h2 | event | long | 13261 | +0.029 | 0.097 | +1.05 | -2.45 | -2.83 | -2.08 | -2.93 |
| MES | 60 | h4 | event | long | 13261 | +0.050 | 0.097 | +1.53 | -1.97 | -2.18 | -1.75 | -2.93 |
| MES | 60 | h8 | event | long | 13261 | +0.112 | 0.097 | +3.62 | +0.12 | -0.58 | +0.83 | -1.62 |
| MES | 60 | h16 | event | long | 13261 | +0.173 | 0.097 | +5.72 | +2.22 | +0.25 | +4.22 | -0.17 |
| MES | 60 | eod | event | long | 13261 | +0.172 | 0.097 | +5.41 | +1.91 | +0.22 | +3.61 | -0.70 |
| MNQ | 5 | h1 | event | long | 153422 | +0.005 | 0.109 | +0.09 | -1.91 | -1.99 | -1.86 | -1.92 |
| MNQ | 5 | h2 | event | long | 153422 | +0.012 | 0.109 | +0.21 | -1.79 | -1.94 | -1.71 | -1.81 |
| MNQ | 5 | h4 | event | long | 153422 | +0.022 | 0.109 | +0.37 | -1.63 | -1.85 | -1.49 | -1.65 |
| MNQ | 5 | h8 | event | long | 153422 | +0.041 | 0.109 | +0.66 | -1.34 | -1.75 | -1.09 | -1.44 |
| MNQ | 5 | h16 | event | long | 153422 | +0.077 | 0.109 | +1.08 | -0.92 | -1.50 | -0.58 | -1.24 |
| MNQ | 5 | eod | event | long | 153422 | +0.732 | 0.109 | +7.81 | +5.81 | +1.45 | +8.40 | +5.54 |
| MNQ | 15 | h1 | event | long | 56991 | +0.007 | 0.071 | +0.23 | -1.77 | -1.95 | -1.63 | -1.89 |
| MNQ | 15 | h2 | event | long | 56991 | +0.019 | 0.071 | +0.36 | -1.64 | -1.83 | -1.49 | -1.80 |
| MNQ | 15 | h4 | event | long | 56991 | +0.026 | 0.071 | +0.47 | -1.53 | -1.72 | -1.38 | -1.85 |
| MNQ | 15 | h8 | event | long | 56991 | +0.052 | 0.071 | +1.19 | -0.81 | -1.51 | -0.26 | -1.49 |
| MNQ | 15 | h16 | event | long | 56991 | +0.095 | 0.071 | +2.06 | +0.06 | -1.14 | +0.99 | -0.67 |
| MNQ | 15 | eod | event | long | 56991 | +0.404 | 0.071 | +7.98 | +5.98 | +0.74 | +10.07 | +5.43 |
| MNQ | 60 | h1 | event | long | 12904 | +0.018 | 0.037 | +0.70 | -1.30 | -1.51 | -1.10 | -1.61 |
| MNQ | 60 | h2 | event | long | 12904 | +0.024 | 0.037 | +0.92 | -1.08 | -1.23 | -0.94 | -1.72 |
| MNQ | 60 | h4 | event | long | 12904 | +0.056 | 0.037 | +2.62 | +0.62 | -0.90 | +2.00 | -0.70 |
| MNQ | 60 | h8 | event | long | 12904 | +0.108 | 0.037 | +4.78 | +2.78 | +0.11 | +5.22 | +0.37 |
| MNQ | 60 | h16 | event | long | 12904 | +0.153 | 0.037 | +6.98 | +4.98 | +1.05 | +8.57 | +1.75 |
| MNQ | 60 | eod | event | long | 12904 | +0.160 | 0.037 | +7.07 | +5.07 | +1.13 | +8.68 | +1.73 |
| MYM | 5 | h1 | event | long | 82288 | +0.003 | 0.162 | +0.08 | -1.92 | +nan | -1.92 | -1.92 |
| MYM | 5 | h2 | event | long | 82288 | +0.006 | 0.162 | +0.15 | -1.85 | +nan | -1.85 | -1.85 |
| MYM | 5 | h4 | event | long | 82288 | +0.013 | 0.162 | +0.29 | -1.71 | +nan | -1.71 | -1.73 |
| MYM | 5 | h8 | event | long | 82288 | +0.022 | 0.162 | +0.38 | -1.62 | +nan | -1.62 | -1.70 |
| MYM | 5 | h16 | event | long | 82288 | +0.033 | 0.162 | +0.67 | -1.33 | +nan | -1.33 | -1.57 |
| MYM | 5 | eod | event | long | 82288 | +0.305 | 0.162 | +4.43 | +2.43 | +nan | +2.43 | +1.00 |
| MYM | 15 | h1 | event | long | 29479 | +0.007 | 0.098 | +0.17 | -1.83 | +nan | -1.83 | -1.84 |
| MYM | 15 | h2 | event | long | 29479 | +0.023 | 0.098 | +0.46 | -1.54 | +nan | -1.54 | -1.58 |
| MYM | 15 | h4 | event | long | 29479 | +0.024 | 0.098 | +0.63 | -1.37 | +nan | -1.37 | -1.48 |
| MYM | 15 | h8 | event | long | 29479 | +0.041 | 0.098 | +1.06 | -0.94 | +nan | -0.94 | -1.14 |
| MYM | 15 | h16 | event | long | 29479 | +0.037 | 0.098 | +1.31 | -0.69 | +nan | -0.69 | -0.86 |
| MYM | 15 | eod | event | long | 29479 | +0.208 | 0.098 | +4.13 | +2.13 | +nan | +2.13 | +1.23 |
| MYM | 60 | h1 | event | long | 6621 | +0.025 | 0.049 | +0.80 | -1.20 | +nan | -1.20 | -1.36 |
| MYM | 60 | h2 | event | long | 6621 | +0.027 | 0.049 | +1.13 | -0.87 | +nan | -0.87 | -1.15 |
| MYM | 60 | h4 | event | short | 6621 | -0.004 | 0.049 | -0.83 | -2.83 | +nan | -2.83 | -2.31 |
| MYM | 60 | h8 | event | short | 6621 | -0.015 | 0.049 | -2.29 | -4.29 | +nan | -4.29 | -3.39 |
| MYM | 60 | h16 | event | short | 6621 | -0.010 | 0.049 | -2.62 | -4.62 | +nan | -4.62 | -3.21 |
| MYM | 60 | eod | event | short | 6621 | -0.022 | 0.049 | -2.99 | -4.99 | +nan | -4.99 | -3.31 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.009 | +0.018 | +0.018 | +0.011 | +0.000 | +0.000 | +0.004 | +0.008 | +0.008 | +0.003 | +0.015 |
| MES | 15 | +0.009 | +0.027 | +0.015 | +0.011 | +0.004 | +0.000 | +0.005 | +0.013 | +0.007 | +0.016 | +0.032 |
| MES | 60 | -0.021 | +0.003 | +0.007 | +0.009 | +0.009 | +0.000 | +0.005 | +0.009 | +0.014 | +0.061 | +0.126 |
| MNQ | 5 | +0.013 | +0.020 | +0.017 | +0.011 | +0.005 | +0.000 | +0.003 | +0.007 | +0.009 | +0.013 | +0.018 |
| MNQ | 15 | +0.014 | +0.026 | +0.023 | +0.017 | +0.008 | +0.000 | +0.002 | +0.010 | +0.003 | -0.000 | +0.004 |
| MNQ | 60 | +0.025 | +0.021 | +0.016 | +0.014 | +0.015 | +0.000 | +0.007 | -0.000 | +0.015 | +0.038 | +0.047 |
| MYM | 5 | -0.003 | +0.009 | +0.008 | +0.003 | -0.001 | +0.000 | +0.006 | +0.012 | +0.022 | +0.033 | +0.041 |
| MYM | 15 | +0.010 | +0.021 | +0.006 | +0.008 | +0.002 | +0.000 | +0.010 | +0.028 | +0.031 | +0.051 | +0.071 |
| MYM | 60 | -0.011 | -0.004 | +0.006 | +0.007 | +0.006 | +0.000 | +0.020 | +0.019 | -0.015 | +0.001 | -0.072 |

## Calibration

- MES 5-min: 1036271 bars, 119087 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 52347 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 13261 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 153422 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 56991 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 12904 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 82288 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 29479 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 6621 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33347 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
