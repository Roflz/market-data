# Impact card: ema_stack

EMA 8/20/50 stack: +1 = 8>20>50 (up), -1 = 8<20<50 (down), 0 mixed; up stack vs down stack [controls: 15-min slot, weekday, year (trend state / volatility NOT controlled: they are the metric)]

Kind: state. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.333 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.019 R20 or more 80% of the time).
- MES 5-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.025 R20, CONFIRMED, q=1.2e-67, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.20 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.221 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.056 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MES 15-min size: the market moves 6% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.029 R20, CONFIRMED, q=2.06e-25, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.69 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.126 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.001 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.068 R20 or more 80% of the time).
- MES 60-min size: the market moves 6% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.033 R20, CONFIRMED, q=9.45e-11, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.34 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.064 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.611 R20 over the rest of the session (to 16:45), p=0.57; we would catch an effect of 0.023 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.025 R20, CONFIRMED, q=2.58e-25, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.95 at recent bar sizes, 90% range up to $0.57); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.050 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 6% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.032 R20, CONFIRMED, q=8.16e-09, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.16 at recent bar sizes, 90% range up to $1.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.074 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 6% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.032 R20, CONFIRMED, q=3.85e-10, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.20 at recent bar sizes, 90% range up to $4.16); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.055 R20 over the next 8 bars (40 min), p=0.72; we would catch an effect of 0.035 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.024 R20, CONFIRMED, q=9.88e-09, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.66 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.168 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MYM 15-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.024 R20, CONFIRMED, q=0.000106, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.90 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.095 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.069 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.101 R20 or more 80% of the time).
- MYM 60-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.028 R20, CONFIRMED, q=0.0102, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.46 at recent bar sizes, 90% range up to $3.09); about 3.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.004 .. +0.001 | -0.0010 | 0.32 / 0.32 / 0.36 | 0.368 |  |  | 8/16 | -0.003 | +0.000 |  | -0.9 / -1.0 |  |
| MES | 5 | h2 | -0.001 | -0.006 .. +0.005 | -0.0003 | 0.84 / 0.84 / 0.86 | 0.857 |  |  | 7/16 | -0.008 | +0.007 |  | -0.2 / -0.2 |  |
| MES | 5 | h4 | +0.001 | -0.011 .. +0.013 | +0.0001 | 0.88 / 0.88 / 0.88 | 0.877 |  |  | 8/16 | -0.019 | +0.021 |  | +0.3 / +0.2 | 0.019 |
| MES | 5 | h8 | +0.000 | -0.023 .. +0.024 | -0.0001 | 0.99 / 0.99 / 0.99 | 0.986 |  |  | 8/16 | -0.039 | +0.039 |  | +0.0 / +0.0 |  |
| MES | 5 | h16 | -0.005 | -0.050 .. +0.040 | -0.0008 | 0.83 / 0.83 / 0.83 | 0.842 |  |  | 10/16 | -0.066 | +0.056 |  | -0.7 / -0.2 |  |
| MES | 5 | eod * | +0.333 | -0.179 .. +0.846 | +0.0088 | 0.2 / 0.19 / 0.13 | 0.127 | 1 | 1 | 7/16 | +0.245 | +0.421 | False | +9.4 / +1.3 |  |
| MES | 15 | h1 | -0.001 | -0.007 .. +0.005 | -0.0005 | 0.7 / 0.69 / 0.69 | 0.681 |  |  | 8/16 | -0.005 | +0.002 |  | -0.4 / -0.4 |  |
| MES | 15 | h2 | +0.000 | -0.011 .. +0.011 | +0.0003 | 0.97 / 0.97 / 0.98 | 0.976 |  |  | 9/16 | -0.013 | +0.013 |  | +0.0 / +0.0 |  |
| MES | 15 | h4 | +0.003 | -0.019 .. +0.025 | +0.0009 | 0.8 / 0.8 / 0.82 | 0.822 |  |  | 8/16 | -0.024 | +0.030 |  | +0.4 / +0.2 | 0.035 |
| MES | 15 | h8 | +0.012 | -0.032 .. +0.057 | +0.0021 | 0.59 / 0.59 / 0.61 | 0.609 |  |  | 9/16 | -0.050 | +0.074 |  | +1.2 / +0.5 |  |
| MES | 15 | h16 * | +0.056 | -0.038 .. +0.150 | +0.0070 | 0.24 / 0.23 / 0.24 | 0.241 | 1 | 1 | 10/16 | -0.074 | +0.186 | False | +4.0 / +1.2 |  |
| MES | 15 | eod | +0.204 | -0.191 .. +0.598 | +0.0096 | 0.31 / 0.3 / 0.29 | 0.291 |  |  | 8/16 | +0.055 | +0.352 |  | +5.8 / +1.0 |  |
| MES | 60 | h1 * | -0.001 | -0.014 .. +0.011 | -0.0001 | 0.82 / 0.82 / 0.84 | 0.828 | 1 | 1 | 9/16 | -0.010 | +0.007 | False | -0.2 / -0.2 |  |
| MES | 60 | h2 | -0.001 | -0.025 .. +0.023 | +0.0004 | 0.93 / 0.93 / 0.94 | 0.937 |  |  | 7/16 | -0.016 | +0.013 |  | -0.1 / -0.1 |  |
| MES | 60 | h4 | -0.002 | -0.049 .. +0.046 | -0.0000 | 0.94 / 0.94 / 0.95 | 0.951 |  |  | 8/16 | -0.020 | +0.016 |  | -0.2 / -0.1 | 0.068 |
| MES | 60 | h8 | +0.000 | -0.090 .. +0.090 | +0.0005 | 0.99 / 0.99 / 0.99 | 0.985 |  |  | 8/16 | -0.014 | +0.014 |  | +0.0 / +0.0 |  |
| MES | 60 | h16 | +0.010 | -0.147 .. +0.168 | +0.0020 | 0.9 / 0.9 / 0.89 | 0.892 |  |  | 8/16 | +0.000 | +0.020 |  | +0.4 / +0.1 |  |
| MES | 60 | eod | +0.002 | -0.172 .. +0.176 | +0.0009 | 0.98 / 0.98 / 0.97 | 0.972 |  |  | 10/16 | +0.000 | +0.004 |  | +0.1 / +0.0 |  |
| MNQ | 5 | h1 | +0.002 | -0.002 .. +0.006 | +0.0010 | 0.28 / 0.28 / 0.33 | 0.327 |  |  | 9/16 | -0.003 | +0.007 |  | +0.9 / +1.1 |  |
| MNQ | 5 | h2 | +0.006 | -0.003 .. +0.014 | +0.0019 | 0.17 / 0.17 / 0.18 | 0.177 |  |  | 9/16 | -0.008 | +0.019 |  | +1.6 / +1.4 |  |
| MNQ | 5 | h4 | +0.013 | -0.005 .. +0.030 | +0.0026 | 0.16 / 0.16 / 0.15 | 0.152 |  |  | 9/16 | -0.014 | +0.039 |  | +2.2 / +1.4 | 0.023 |
| MNQ | 5 | h8 | +0.018 | -0.012 .. +0.049 | +0.0027 | 0.24 / 0.23 / 0.28 | 0.288 |  |  | 9/16 | -0.018 | +0.054 |  | +2.2 / +1.2 |  |
| MNQ | 5 | h16 | +0.029 | -0.028 .. +0.087 | +0.0030 | 0.32 / 0.31 / 0.37 | 0.363 |  |  | 10/16 | -0.014 | +0.072 |  | +2.6 / +1.0 |  |
| MNQ | 5 | eod * | +0.611 | -0.107 .. +1.329 | +0.0120 | 0.095 / 0.083 / 0.033 | 0.0289 | 1 | 1 | 10/16 | +0.539 | +0.682 | False | +12.1 / +1.7 |  |
| MNQ | 15 | h1 | -0.002 | -0.011 .. +0.007 | -0.0007 | 0.65 / 0.65 / 0.61 | 0.615 |  |  | 7/16 | -0.005 | +0.001 |  | -0.5 / -0.4 |  |
| MNQ | 15 | h2 | -0.003 | -0.019 .. +0.012 | -0.0004 | 0.68 / 0.68 / 0.71 | 0.717 |  |  | 5/16 | -0.010 | +0.004 |  | -0.5 / -0.4 |  |
| MNQ | 15 | h4 | -0.004 | -0.033 .. +0.025 | -0.0001 | 0.77 / 0.77 / 0.81 | 0.825 |  |  | 6/16 | -0.022 | +0.013 |  | -0.5 / -0.3 | 0.044 |
| MNQ | 15 | h8 | +0.005 | -0.043 .. +0.052 | +0.0013 | 0.85 / 0.85 / 0.88 | 0.881 |  |  | 10/16 | -0.053 | +0.062 |  | +0.4 / +0.2 |  |
| MNQ | 15 | h16 * | +0.050 | -0.041 .. +0.142 | +0.0056 | 0.28 / 0.3 / 0.38 | 0.378 | 1 | 1 | 11/16 | -0.064 | +0.164 | False | +3.5 / +1.1 |  |
| MNQ | 15 | eod | +0.168 | -0.229 .. +0.565 | +0.0066 | 0.41 / 0.41 / 0.48 | 0.496 |  |  | 9/16 | +0.213 | +0.123 |  | +4.5 / +0.8 |  |
| MNQ | 60 | h1 * | +0.004 | -0.008 .. +0.017 | +0.0033 | 0.5 / 0.5 / 0.53 | 0.533 | 1 | 1 | 8/16 | -0.004 | +0.013 | False | +0.7 / +0.7 |  |
| MNQ | 60 | h2 | +0.006 | -0.019 .. +0.031 | +0.0039 | 0.63 / 0.63 / 0.65 | 0.657 |  |  | 8/16 | -0.006 | +0.018 |  | +0.6 / +0.5 |  |
| MNQ | 60 | h4 | +0.010 | -0.039 .. +0.058 | +0.0044 | 0.7 / 0.7 / 0.72 | 0.714 |  |  | 8/16 | -0.000 | +0.019 |  | +0.7 / +0.4 | 0.074 |
| MNQ | 60 | h8 | +0.003 | -0.088 .. +0.094 | +0.0023 | 0.95 / 0.95 / 0.94 | 0.947 |  |  | 7/16 | +0.010 | -0.004 |  | +0.2 / +0.1 |  |
| MNQ | 60 | h16 | -0.003 | -0.163 .. +0.156 | +0.0011 | 0.97 / 0.97 / 0.98 | 0.982 |  |  | 7/16 | +0.028 | -0.035 |  | -0.1 / -0.0 |  |
| MNQ | 60 | eod | +0.000 | -0.175 .. +0.176 | +0.0017 | 1 / 1 / 0.98 | 0.987 |  |  | 10/16 | +0.053 | -0.053 |  | +0.0 / +0.0 |  |
| MYM | 5 | h1 | +0.001 | -0.004 .. +0.006 | +0.0003 | 0.75 / 0.76 / 0.77 | 0.762 |  |  | 3/8 | n/a | +0.001 |  | +0.3 / +0.3 |  |
| MYM | 5 | h2 | +0.010 | -0.007 .. +0.026 | +0.0025 | 0.26 / 0.25 / 0.14 | 0.149 |  |  | 3/8 | n/a | +0.010 |  | +1.7 / +1.1 |  |
| MYM | 5 | h4 | +0.028 | -0.012 .. +0.069 | +0.0046 | 0.17 / 0.16 / 0.043 | 0.0437 |  |  | 2/8 | n/a | +0.028 |  | +3.0 / +1.4 | 0.035 |
| MYM | 5 | h8 * | +0.055 | -0.014 .. +0.124 | +0.0063 | 0.12 / 0.12 / 0.029 | 0.0279 | 1 | 1 | 5/8 | n/a | +0.055 | False | +4.2 / +1.6 |  |
| MYM | 5 | h16 | +0.079 | -0.033 .. +0.191 | +0.0072 | 0.17 / 0.17 / 0.083 | 0.089 |  |  | 4/8 | n/a | +0.079 |  | +4.8 / +1.4 |  |
| MYM | 5 | eod | +0.322 | -0.626 .. +1.269 | +0.0065 | 0.51 / 0.51 / 0.39 | 0.399 |  |  | 3/8 | n/a | +0.322 |  | +4.8 / +0.7 |  |
| MYM | 15 | h1 * | +0.005 | -0.005 .. +0.014 | +0.0024 | 0.33 / 0.34 / 0.35 | 0.355 | 1 | 1 | 4/8 | n/a | +0.005 | False | +0.9 / +1.0 |  |
| MYM | 15 | h2 | +0.008 | -0.008 .. +0.024 | +0.0025 | 0.32 / 0.34 / 0.49 | 0.517 |  |  | 3/8 | n/a | +0.008 |  | +1.1 / +1.0 |  |
| MYM | 15 | h4 | +0.012 | -0.019 .. +0.043 | +0.0023 | 0.44 / 0.47 / 0.63 | 0.644 |  |  | 3/8 | n/a | +0.012 |  | +1.2 / +0.8 | 0.076 |
| MYM | 15 | h8 | +0.032 | -0.029 .. +0.093 | +0.0039 | 0.31 / 0.33 / 0.48 | 0.484 |  |  | 3/8 | n/a | +0.032 |  | +2.3 / +1.0 |  |
| MYM | 15 | h16 | +0.050 | -0.075 .. +0.174 | +0.0047 | 0.44 / 0.44 / 0.55 | 0.547 |  |  | 4/8 | n/a | +0.050 |  | +2.5 / +0.8 |  |
| MYM | 15 | eod | +0.133 | -0.402 .. +0.667 | +0.0054 | 0.63 / 0.62 / 0.66 | 0.68 |  |  | 4/8 | n/a | +0.133 |  | +2.7 / +0.5 |  |
| MYM | 60 | h1 | +0.004 | -0.014 .. +0.021 | +0.0025 | 0.68 / 0.69 / 0.68 | 0.684 |  |  | 4/8 | n/a | +0.004 |  | +0.4 / +0.4 |  |
| MYM | 60 | h2 | +0.010 | -0.025 .. +0.045 | +0.0046 | 0.57 / 0.57 / 0.58 | 0.579 |  |  | 4/8 | n/a | +0.010 |  | +0.8 / +0.6 |  |
| MYM | 60 | h4 | +0.019 | -0.050 .. +0.087 | +0.0063 | 0.6 / 0.6 / 0.59 | 0.591 |  |  | 4/8 | n/a | +0.019 |  | +1.0 / +0.5 | 0.101 |
| MYM | 60 | h8 | +0.033 | -0.101 .. +0.168 | +0.0076 | 0.63 / 0.62 / 0.61 | 0.604 |  |  | 4/8 | n/a | +0.033 |  | +1.3 / +0.5 |  |
| MYM | 60 | h16 * | +0.069 | -0.159 .. +0.298 | +0.0115 | 0.55 / 0.54 / 0.55 | 0.552 | 1 | 1 | 4/8 | n/a | +0.069 | False | +2.1 / +0.6 |  |
| MYM | 60 | eod | +0.062 | -0.190 .. +0.313 | +0.0100 | 0.63 / 0.62 / 0.63 | 0.63 |  |  | 5/8 | n/a | +0.062 |  | +1.8 / +0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.025 | -0.028 .. -0.023 | -5.1% | -0.035 | 9.5e-71 | 1.2e-67 | 16/16 |
| MES | 5 | h2 | -0.036 | -0.041 .. -0.031 | -5.1% | -0.053 | 7.7e-41 |  | 15/16 |
| MES | 5 | h4 | -0.046 | -0.056 .. -0.035 | -4.6% | -0.073 | 4.3e-18 |  | 15/16 |
| MES | 5 | h8 | -0.052 | -0.070 .. -0.034 | -3.6% | -0.087 | 3.2e-08 |  | 15/16 |
| MES | 5 | h16 | -0.042 | -0.074 .. -0.010 | -2.0% | -0.075 | 0.011 |  | 13/16 |
| MES | 5 | eod | +0.407 | +0.030 .. +0.785 | +4.1% | +0.710 | 0.084 |  | 10/16 |
| MES | 15 | h1 * | -0.029 | -0.034 .. -0.024 | -5.7% | -0.045 | 3e-28 | 2.06e-25 | 16/16 |
| MES | 15 | h2 | -0.039 | -0.051 .. -0.026 | -5.3% | -0.067 | 1.1e-09 |  | 15/16 |
| MES | 15 | h4 | -0.044 | -0.069 .. -0.018 | -4.1% | -0.087 | 0.00096 |  | 14/16 |
| MES | 15 | h8 | -0.042 | -0.083 .. -0.000 | -2.7% | -0.108 | 0.049 |  | 11/16 |
| MES | 15 | h16 | -0.026 | -0.097 .. +0.044 | -1.2% | -0.107 | 0.46 |  | 9/16 |
| MES | 15 | eod | +0.154 | -0.129 .. +0.438 | +2.8% | +0.319 | 0.42 |  | 10/16 |
| MES | 60 | h1 * | -0.033 | -0.041 .. -0.025 | -6.5% | -0.057 | 2.4e-13 | 9.45e-11 | 16/16 |
| MES | 60 | h2 | -0.045 | -0.060 .. -0.031 | -6.1% | -0.073 | 1.1e-09 |  | 16/16 |
| MES | 60 | h4 | -0.055 | -0.083 .. -0.028 | -5.2% | -0.081 | 8.7e-05 |  | 14/16 |
| MES | 60 | h8 | -0.059 | -0.112 .. -0.006 | -3.9% | -0.079 | 0.029 |  | 11/16 |
| MES | 60 | h16 | -0.082 | -0.181 .. +0.018 | -4.0% | -0.078 | 0.11 |  | 9/16 |
| MES | 60 | eod | -0.094 | -0.207 .. +0.019 | -4.3% | -0.084 | 0.1 |  | 10/16 |
| MNQ | 5 | h1 * | -0.025 | -0.030 .. -0.021 | -4.7% | -0.034 | 3.8e-28 | 2.58e-25 | 15/16 |
| MNQ | 5 | h2 | -0.036 | -0.046 .. -0.025 | -4.7% | -0.049 | 3.7e-11 |  | 15/16 |
| MNQ | 5 | h4 | -0.046 | -0.067 .. -0.024 | -4.1% | -0.068 | 3.3e-05 |  | 15/16 |
| MNQ | 5 | h8 | -0.049 | -0.088 .. -0.010 | -3.0% | -0.080 | 0.014 |  | 14/16 |
| MNQ | 5 | h16 | -0.027 | -0.090 .. +0.035 | -1.1% | -0.072 | 0.39 |  | 8/16 |
| MNQ | 5 | eod | +0.591 | +0.011 .. +1.170 | +4.7% | +1.054 | 0.046 |  | 13/16 |
| MNQ | 15 | h1 * | -0.032 | -0.041 .. -0.023 | -6.0% | -0.049 | 2.4e-11 | 8.16e-09 | 15/16 |
| MNQ | 15 | h2 | -0.039 | -0.053 .. -0.024 | -5.0% | -0.062 | 1.8e-07 |  | 15/16 |
| MNQ | 15 | h4 | -0.044 | -0.068 .. -0.020 | -3.9% | -0.069 | 0.01 |  | 14/16 |
| MNQ | 15 | h8 | -0.032 | -0.064 .. +0.001 | -1.9% | -0.061 | 0.26 |  | 13/16 |
| MNQ | 15 | h16 | -0.004 | -0.061 .. +0.053 | -0.2% | -0.020 | 1 |  | 9/16 |
| MNQ | 15 | eod | +0.365 | +0.107 .. +0.623 | +5.8% | +0.547 | 0.033 |  | 12/16 |
| MNQ | 60 | h1 * | -0.032 | -0.041 .. -0.024 | -6.1% | -0.047 | 1e-12 | 3.85e-10 | 15/16 |
| MNQ | 60 | h2 | -0.042 | -0.057 .. -0.026 | -5.4% | -0.060 | 2.4e-07 |  | 15/16 |
| MNQ | 60 | h4 | -0.046 | -0.074 .. -0.018 | -4.2% | -0.063 | 0.0013 |  | 13/16 |
| MNQ | 60 | h8 | -0.028 | -0.080 .. +0.024 | -1.8% | -0.044 | 0.31 |  | 10/16 |
| MNQ | 60 | h16 | +0.005 | -0.092 .. +0.101 | +0.2% | -0.002 | 0.98 |  | 9/16 |
| MNQ | 60 | eod | +0.015 | -0.095 .. +0.125 | +0.6% | +0.001 | 0.85 |  | 9/16 |
| MYM | 5 | h1 * | -0.024 | -0.031 .. -0.017 | -4.5% | -0.038 | 2.9e-11 | 9.88e-09 | 8/8 |
| MYM | 5 | h2 | -0.038 | -0.055 .. -0.020 | -4.9% | -0.057 | 1.8e-05 |  | 8/8 |
| MYM | 5 | h4 | -0.056 | -0.096 .. -0.016 | -5.1% | -0.084 | 0.0062 |  | 7/8 |
| MYM | 5 | h8 | -0.075 | -0.145 .. -0.004 | -4.7% | -0.121 | 0.04 |  | 7/8 |
| MYM | 5 | h16 | -0.073 | -0.180 .. +0.035 | -3.1% | -0.155 | 0.2 |  | 6/8 |
| MYM | 5 | eod | +0.664 | -0.044 .. +1.372 | +5.7% | +1.201 | 0.071 |  | 7/8 |
| MYM | 15 | h1 * | -0.024 | -0.033 .. -0.015 | -4.5% | -0.041 | 4.2e-07 | 0.000106 | 7/8 |
| MYM | 15 | h2 | -0.028 | -0.043 .. -0.014 | -3.7% | -0.052 | 0.0029 |  | 7/8 |
| MYM | 15 | h4 | -0.028 | -0.051 .. -0.005 | -2.5% | -0.056 | 0.17 |  | 5/8 |
| MYM | 15 | h8 | -0.002 | -0.044 .. +0.039 | -0.1% | -0.032 | 0.97 |  | 4/8 |
| MYM | 15 | h16 | +0.048 | -0.032 .. +0.129 | +2.0% | +0.070 | 0.5 |  | 7/8 |
| MYM | 15 | eod | +0.467 | +0.115 .. +0.819 | +7.8% | +0.883 | 0.081 |  | 7/8 |
| MYM | 60 | h1 * | -0.028 | -0.041 .. -0.016 | -5.4% | -0.047 | 4.8e-05 | 0.0102 | 8/8 |
| MYM | 60 | h2 | -0.028 | -0.050 .. -0.006 | -3.7% | -0.054 | 0.028 |  | 6/8 |
| MYM | 60 | h4 | -0.031 | -0.073 .. +0.010 | -2.9% | -0.047 | 0.19 |  | 5/8 |
| MYM | 60 | h8 | -0.011 | -0.086 .. +0.063 | -0.7% | -0.022 | 0.87 |  | 4/8 |
| MYM | 60 | h16 | +0.005 | -0.135 .. +0.146 | +0.3% | +0.013 | 0.94 |  | 5/8 |
| MYM | 60 | eod | -0.001 | -0.161 .. +0.159 | -0.1% | +0.011 | 0.99 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -1.17 pts | -1.59 .. -0.76 | 4e-08 |
| MES | 15 | -0.86 pts | -1.58 .. -0.14 | 0.019 |
| MES | 60 | +0.51 pts | -1.10 .. +2.12 | 0.55 |
| MNQ | 5 | -0.86 pts | -1.29 .. -0.43 | 0.0001 |
| MNQ | 15 | -0.21 pts | -0.96 .. +0.55 | 0.75 |
| MNQ | 60 | +0.67 pts | -0.94 .. +2.29 | 0.41 |
| MYM | 5 | -0.15 pts | -0.67 .. +0.37 | 0.6 |
| MYM | 15 | +0.23 pts | -0.78 .. +1.24 | 0.66 |
| MYM | 60 | +1.57 pts | -0.60 .. +3.75 | 0.17 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom level | long | 356770 | +0.002 | 0.292 | +0.02 | -3.48 | -3.49 | -3.47 | -3.48 |
| MES | 5 | h2 | bottom level | long | 356770 | +0.004 | 0.292 | +0.04 | -3.46 | -3.47 | -3.45 | -3.48 |
| MES | 5 | h4 | top level | long | 440805 | +0.009 | 0.351 | +0.14 | -3.36 | -3.44 | -3.29 | -3.42 |
| MES | 5 | h8 | top level | long | 440805 | +0.020 | 0.351 | +0.29 | -3.21 | -3.38 | -3.06 | -3.34 |
| MES | 5 | h16 | bottom level | long | 356770 | +0.046 | 0.292 | +0.39 | -3.11 | -3.08 | -3.13 | -3.41 |
| MES | 5 | eod | top level | long | 440805 | +0.656 | 0.351 | +4.67 | +1.17 | +0.36 | +1.96 | -0.62 |
| MES | 15 | h1 | bottom level | long | 112471 | +0.006 | 0.161 | +0.10 | -3.40 | -3.43 | -3.36 | -3.46 |
| MES | 15 | h2 | top level | long | 150132 | +0.011 | 0.208 | +0.15 | -3.35 | -3.42 | -3.28 | -3.46 |
| MES | 15 | h4 | top level | long | 150132 | +0.023 | 0.208 | +0.32 | -3.18 | -3.34 | -3.03 | -3.39 |
| MES | 15 | h8 | top level | long | 150132 | +0.041 | 0.208 | +0.58 | -2.92 | -3.16 | -2.68 | -3.31 |
| MES | 15 | h16 | top level | long | 150132 | +0.101 | 0.208 | +1.45 | -2.05 | -2.67 | -1.45 | -2.68 |
| MES | 15 | eod | top level | long | 150132 | +0.362 | 0.208 | +4.13 | +0.63 | +0.11 | +1.14 | -0.76 |
| MES | 60 | h1 | bottom level | long | 25214 | +0.010 | 0.077 | +0.54 | -2.96 | -3.14 | -2.79 | -3.16 |
| MES | 60 | h2 | bottom level | long | 25214 | +0.019 | 0.077 | +1.08 | -2.42 | -2.86 | -1.99 | -2.86 |
| MES | 60 | h4 | bottom level | long | 25214 | +0.034 | 0.077 | +2.08 | -1.42 | -2.53 | -0.34 | -2.37 |
| MES | 60 | h8 | top level | long | 39070 | +0.074 | 0.110 | +2.23 | -1.27 | -2.07 | -0.46 | -2.97 |
| MES | 60 | h16 | top level | long | 39070 | +0.123 | 0.110 | +3.57 | +0.07 | -1.03 | +1.18 | -2.69 |
| MES | 60 | eod | top level | long | 39070 | +0.137 | 0.110 | +3.75 | +0.25 | -0.75 | +1.27 | -3.00 |
| MNQ | 5 | h1 | top level | long | 443945 | +0.005 | 0.142 | +0.06 | -1.94 | -1.98 | -1.90 | -1.96 |
| MNQ | 5 | h2 | top level | long | 443945 | +0.011 | 0.142 | +0.13 | -1.87 | -1.95 | -1.79 | -1.90 |
| MNQ | 5 | h4 | top level | long | 443945 | +0.022 | 0.142 | +0.24 | -1.76 | -1.89 | -1.63 | -1.80 |
| MNQ | 5 | h8 | top level | long | 443945 | +0.044 | 0.142 | +0.48 | -1.52 | -1.79 | -1.25 | -1.63 |
| MNQ | 5 | h16 | top level | long | 443945 | +0.087 | 0.142 | +0.99 | -1.01 | -1.58 | -0.45 | -1.28 |
| MNQ | 5 | eod | top level | long | 443945 | +1.031 | 0.142 | +6.34 | +4.34 | +1.42 | +7.22 | +2.63 |
| MNQ | 15 | h1 | bottom level | long | 110913 | +0.009 | 0.063 | +0.10 | -1.90 | -1.90 | -1.89 | -2.03 |
| MNQ | 15 | h2 | bottom level | long | 110913 | +0.017 | 0.063 | +0.20 | -1.80 | -1.80 | -1.79 | -1.97 |
| MNQ | 15 | h4 | bottom level | long | 110913 | +0.030 | 0.063 | +0.32 | -1.68 | -1.62 | -1.73 | -2.01 |
| MNQ | 15 | h8 | top level | long | 152565 | +0.058 | 0.082 | +1.17 | -0.83 | -1.65 | -0.01 | -1.52 |
| MNQ | 15 | h16 | top level | long | 152565 | +0.128 | 0.082 | +2.73 | +0.73 | -1.20 | +2.68 | -0.09 |
| MNQ | 15 | eod | top level | long | 152565 | +0.479 | 0.082 | +4.54 | +2.54 | +0.95 | +4.13 | +1.08 |
| MNQ | 60 | h1 | top level | long | 39202 | +0.017 | 0.044 | +0.52 | -1.48 | -1.74 | -1.20 | -1.84 |
| MNQ | 60 | h2 | top level | long | 39202 | +0.033 | 0.044 | +0.98 | -1.02 | -1.52 | -0.51 | -1.76 |
| MNQ | 60 | h4 | top level | long | 39202 | +0.061 | 0.044 | +1.80 | -0.20 | -1.10 | +0.74 | -1.63 |
| MNQ | 60 | h8 | top level | long | 39202 | +0.098 | 0.044 | +2.29 | +0.29 | -0.23 | +0.84 | -2.33 |
| MNQ | 60 | h16 | bottom level | long | 25032 | +0.118 | 0.030 | +9.56 | +7.56 | +1.28 | +13.37 | +4.02 |
| MNQ | 60 | eod | top level | long | 39202 | +0.175 | 0.044 | +3.42 | +1.42 | +1.12 | +1.73 | -3.66 |
| MYM | 5 | h1 | top level | long | 218091 | -0.001 | 0.182 | +0.00 | -2.00 | +nan | -2.00 | -1.99 |
| MYM | 5 | h2 | top level | long | 218091 | -0.000 | 0.182 | +0.02 | -1.98 | +nan | -1.98 | -1.95 |
| MYM | 5 | h4 | top level | long | 218091 | +0.002 | 0.182 | +0.06 | -1.94 | +nan | -1.94 | -1.86 |
| MYM | 5 | h8 | top level | long | 218091 | +0.005 | 0.182 | +0.14 | -1.86 | +nan | -1.86 | -1.74 |
| MYM | 5 | h16 | top level | long | 218091 | +0.021 | 0.182 | +0.26 | -1.74 | +nan | -1.74 | -1.66 |
| MYM | 5 | eod | top level | long | 218091 | +0.311 | 0.182 | +3.73 | +1.73 | +nan | +1.73 | +1.25 |
| MYM | 15 | h1 | top level | long | 73191 | +0.004 | 0.105 | +0.02 | -1.98 | +nan | -1.98 | -2.00 |
| MYM | 15 | h2 | top level | long | 73191 | +0.008 | 0.105 | +0.07 | -1.93 | +nan | -1.93 | -1.92 |
| MYM | 15 | h4 | top level | long | 73191 | +0.012 | 0.105 | +0.16 | -1.84 | +nan | -1.84 | -1.81 |
| MYM | 15 | h8 | top level | long | 73191 | +0.017 | 0.105 | +0.33 | -1.67 | +nan | -1.67 | -1.58 |
| MYM | 15 | h16 | top level | long | 73191 | +0.034 | 0.105 | +0.99 | -1.01 | +nan | -1.01 | -0.55 |
| MYM | 15 | eod | top level | long | 73191 | +0.215 | 0.105 | +3.25 | +1.25 | +nan | +1.25 | +1.68 |
| MYM | 60 | h1 | top level | long | 18209 | +0.008 | 0.053 | +0.23 | -1.77 | +nan | -1.77 | -1.89 |
| MYM | 60 | h2 | top level | long | 18209 | +0.017 | 0.053 | +0.48 | -1.52 | +nan | -1.52 | -1.76 |
| MYM | 60 | h4 | top level | long | 18209 | +0.034 | 0.053 | +1.08 | -0.92 | +nan | -0.92 | -1.38 |
| MYM | 60 | h8 | top level | long | 18209 | +0.052 | 0.053 | +1.83 | -0.17 | +nan | -0.17 | -1.01 |
| MYM | 60 | h16 | top level | long | 18209 | +0.090 | 0.053 | +3.49 | +1.49 | +nan | +1.49 | +0.13 |
| MYM | 60 | eod | top level | long | 18209 | +0.105 | 0.053 | +3.84 | +1.84 | +nan | +1.84 | -0.03 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.000 | -0.002 | +0.002 | +0.002 | +0.001 | +0.000 | -0.002 | -0.002 | -0.003 | -0.007 | -0.008 |
| MES | 15 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 |
| MES | 60 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 |
| MNQ | 5 | -0.004 | -0.002 | -0.001 | +0.000 | +0.002 | +0.000 | -0.001 | +0.001 | -0.000 | -0.002 | -0.009 |
| MNQ | 15 | -0.000 | -0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 |
| MNQ | 60 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 |
| MYM | 5 | -0.000 | -0.001 | -0.000 | +0.000 | -0.000 | +0.000 | +0.001 | +0.001 | +0.002 | +0.001 | +0.005 |
| MYM | 15 | -0.000 | -0.000 | -0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | -0.000 | +0.000 | +0.000 |
| MYM | 60 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +0.000 | -0.000 | -0.000 | -0.000 | -0.000 | +0.000 |

## Calibration

- MES 5-min: 1034349 bars, 440805 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 340296 bars, 150132 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81614 bars, 39070 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1032600 bars, 443945 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340140 bars, 152565 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81612 bars, 39202 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518078 bars, 218091 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170466 bars, 73191 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40755 bars, 18209 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
