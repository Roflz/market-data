# Impact card: pat_nr7_breakout

candle pattern nr7_breakout in its textbook direction: first close beyond an NR7 bar's high/low within 3 bars [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.012 R20 over the next 2 bars (10 min), p=0.014; we would catch an effect of 0.015 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS after the event than after matched bars over the next 2 bars (10 min) (-0.018 R20, CONFIRMED, q=3.76e-07, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.33 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.190 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.046 R20 over the next 8 bars (2 h), p=0.031; we would catch an effect of 0.026 R20 or more 80% of the time).
- MES 15-min size: the market moves 6% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.029 R20, CONFIRMED, q=1.62e-11, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.97 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.118 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.035 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.082 R20 or more 80% of the time).
- MES 60-min size: the market moves 10% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.050 R20, CONFIRMED, q=0.0262, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.98 at recent bar sizes, 90% range up to $6.22); about 11.9x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.009 R20 over the next 2 bars (10 min), p=0.29; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.013 R20, CONFIRMED, q=1.37e-07, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.42 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.072 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (15 min), p=0.091; we would catch an effect of 0.026 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.022 R20, CONFIRMED, q=0.000383, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.56 at recent bar sizes, 90% range up to $2.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.079 R20 over the next 8 bars (8 h), p=0.42; we would catch an effect of 0.087 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.035).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.03 at recent bar sizes, 90% range up to $13.41); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (5 min), p=0.71; we would catch an effect of 0.021 R20 or more 80% of the time).
- MYM 5-min size: the market moves 3% LESS after the event than after matched bars over the next 2 bars (10 min) (-0.021 R20, CONFIRMED, q=0.0207, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.38 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.155 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.066).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.24 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.092 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.035 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.109 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.014).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.49 at recent bar sizes, 90% range up to $5.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.008 | -0.013 .. -0.003 | -0.0031 | 0.00076 / 0.00063 / 0.0021 | 0.00182 |  |  | 12/16 | -0.003 | -0.012 |  | -3.3 / -3.4 |  |
| MES | 5 | h2 * | -0.012 | -0.019 .. -0.006 | -0.0034 | 0.00023 / 0.00016 / 0.0012 | 0.0013 | 0.371 | 0.09 | 12/16 | -0.010 | -0.014 | False | -3.6 / -3.7 |  |
| MES | 5 | h4 | -0.010 | -0.019 .. -0.001 | -0.0019 | 0.024 / 0.027 / 0.071 | 0.0706 |  |  | 11/16 | -0.010 | -0.011 |  | -2.1 / -2.2 | 0.015 |
| MES | 5 | h8 | -0.004 | -0.017 .. +0.009 | -0.0005 | 0.55 / 0.55 / 0.61 | 0.604 |  |  | 8/16 | -0.012 | +0.004 |  | -0.6 / -0.6 |  |
| MES | 5 | h16 | +0.003 | -0.017 .. +0.023 | +0.0003 | 0.77 / 0.78 / 0.79 | 0.789 |  |  | 10/16 | -0.007 | +0.012 |  | +0.3 / +0.3 |  |
| MES | 5 | eod | +0.024 | -0.072 .. +0.119 | +0.0004 | 0.63 / 0.63 / 0.66 | 0.659 |  |  | 11/16 | -0.040 | +0.087 |  | +0.5 / +0.5 |  |
| MES | 15 | h1 | -0.008 | -0.016 .. -0.000 | -0.0031 | 0.047 / 0.043 / 0.059 | 0.0664 |  |  | 13/16 | -0.007 | -0.009 |  | -2.1 / -2.0 |  |
| MES | 15 | h2 | -0.018 | -0.030 .. -0.006 | -0.0045 | 0.0034 / 0.0026 / 0.0074 | 0.00651 |  |  | 14/16 | -0.021 | -0.014 |  | -3.1 / -2.9 |  |
| MES | 15 | h4 | -0.024 | -0.041 .. -0.007 | -0.0041 | 0.0061 / 0.005 / 0.015 | 0.0151 |  |  | 12/16 | -0.023 | -0.025 |  | -2.9 / -2.7 | 0.026 |
| MES | 15 | h8 * | -0.046 | -0.070 .. -0.021 | -0.0055 | 0.00032 / 0.00028 / 0.0018 | 0.00339 | 0.755 | 0.105 | 15/16 | -0.044 | -0.047 | False | -3.6 / -3.6 |  |
| MES | 15 | h16 | -0.026 | -0.064 .. +0.011 | -0.0022 | 0.17 / 0.19 / 0.23 | 0.232 |  |  | 11/16 | -0.047 | -0.006 |  | -1.3 / -1.4 |  |
| MES | 15 | eod | -0.041 | -0.134 .. +0.053 | -0.0013 | 0.4 / 0.4 / 0.45 | 0.469 |  |  | 12/16 | -0.016 | -0.065 |  | -0.8 / -0.8 |  |
| MES | 60 | h1 | +0.013 | -0.016 .. +0.042 | +0.0032 | 0.38 / 0.36 / 0.43 | 0.436 |  |  | 8/16 | +0.015 | +0.011 |  | +0.9 / +0.9 |  |
| MES | 60 | h2 | +0.002 | -0.042 .. +0.047 | +0.0005 | 0.91 / 0.91 / 0.91 | 0.914 |  |  | 7/16 | -0.000 | +0.005 |  | +0.1 / +0.1 |  |
| MES | 60 | h4 * | -0.035 | -0.089 .. +0.019 | -0.0042 | 0.21 / 0.21 / 0.24 | 0.241 | 1 | 1 | 10/16 | -0.040 | -0.029 | False | -1.3 / -1.3 | 0.082 |
| MES | 60 | h8 | -0.042 | -0.122 .. +0.038 | -0.0038 | 0.3 / 0.3 / 0.32 | 0.316 |  |  | 8/16 | -0.018 | -0.067 |  | -1.1 / -1.0 |  |
| MES | 60 | h16 | -0.030 | -0.128 .. +0.068 | -0.0020 | 0.55 / 0.55 / 0.56 | 0.565 |  |  | 9/16 | -0.033 | -0.028 |  | -0.6 / -0.6 |  |
| MES | 60 | eod | -0.026 | -0.124 .. +0.072 | -0.0017 | 0.6 / 0.6 / 0.61 | 0.614 |  |  | 9/16 | -0.030 | -0.023 |  | -0.5 / -0.5 |  |
| MNQ | 5 | h1 | -0.006 | -0.010 .. -0.001 | -0.0021 | 0.017 / 0.015 / 0.042 | 0.0445 |  |  | 10/16 | +0.002 | -0.013 |  | -2.5 / -2.4 |  |
| MNQ | 5 | h2 * | -0.009 | -0.016 .. -0.003 | -0.0022 | 0.0057 / 0.0051 / 0.044 | 0.0474 | 1 | 0.725 | 11/16 | -0.002 | -0.016 | False | -3.0 / -2.8 |  |
| MNQ | 5 | h4 | -0.005 | -0.014 .. +0.005 | -0.0007 | 0.33 / 0.34 / 0.53 | 0.517 |  |  | 10/16 | -0.002 | -0.008 |  | -1.0 / -1.0 | 0.019 |
| MNQ | 5 | h8 | +0.001 | -0.012 .. +0.014 | +0.0001 | 0.86 / 0.87 / 0.89 | 0.89 |  |  | 9/16 | -0.001 | +0.004 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h16 | +0.011 | -0.009 .. +0.031 | +0.0008 | 0.29 / 0.31 / 0.43 | 0.431 |  |  | 10/16 | +0.005 | +0.017 |  | +1.1 / +1.1 |  |
| MNQ | 5 | eod | +0.022 | -0.090 .. +0.134 | +0.0003 | 0.7 / 0.69 / 0.74 | 0.74 |  |  | 6/16 | +0.002 | +0.042 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h1 * | -0.012 | -0.019 .. -0.005 | -0.0038 | 0.00094 / 0.001 / 0.014 | 0.0258 | 1 | 0.209 | 14/16 | -0.011 | -0.013 | False | -3.1 / -3.3 |  |
| MNQ | 15 | h2 | -0.018 | -0.028 .. -0.008 | -0.0035 | 0.0007 / 0.00067 / 0.023 | 0.032 |  |  | 13/16 | -0.020 | -0.016 |  | -3.3 / -3.4 |  |
| MNQ | 15 | h4 | -0.022 | -0.037 .. -0.006 | -0.0025 | 0.0063 / 0.0065 / 0.12 | 0.121 |  |  | 14/16 | -0.024 | -0.020 |  | -2.7 / -2.7 | 0.026 |
| MNQ | 15 | h8 | -0.026 | -0.051 .. -0.002 | -0.0023 | 0.033 / 0.031 / 0.2 | 0.201 |  |  | 11/16 | -0.036 | -0.017 |  | -2.1 / -2.1 |  |
| MNQ | 15 | h16 | -0.043 | -0.082 .. -0.005 | -0.0031 | 0.027 / 0.028 / 0.07 | 0.0695 |  |  | 11/16 | -0.071 | -0.016 |  | -2.2 / -2.2 |  |
| MNQ | 15 | eod | +0.012 | -0.088 .. +0.113 | +0.0003 | 0.81 / 0.81 / 0.86 | 0.856 |  |  | 8/16 | -0.012 | +0.036 |  | +0.2 / +0.2 |  |
| MNQ | 60 | h1 | +0.024 | -0.007 .. +0.055 | +0.0057 | 0.12 / 0.12 / 0.14 | 0.147 |  |  | 11/16 | +0.004 | +0.045 |  | +1.5 / +1.5 |  |
| MNQ | 60 | h2 | +0.017 | -0.027 .. +0.061 | +0.0028 | 0.45 / 0.45 / 0.48 | 0.471 |  |  | 8/16 | +0.012 | +0.022 |  | +0.8 / +0.8 |  |
| MNQ | 60 | h4 | -0.035 | -0.091 .. +0.020 | -0.0041 | 0.21 / 0.22 / 0.26 | 0.254 |  |  | 9/16 | -0.009 | -0.061 |  | -1.2 / -1.2 | 0.087 |
| MNQ | 60 | h8 * | -0.079 | -0.164 .. +0.006 | -0.0067 | 0.069 / 0.07 / 0.081 | 0.0836 | 1 | 1 | 10/16 | -0.043 | -0.115 | False | -1.8 / -1.8 |  |
| MNQ | 60 | h16 | -0.080 | -0.187 .. +0.026 | -0.0052 | 0.14 / 0.13 / 0.16 | 0.161 |  |  | 9/16 | -0.079 | -0.082 |  | -1.5 / -1.5 |  |
| MNQ | 60 | eod | -0.077 | -0.184 .. +0.030 | -0.0048 | 0.16 / 0.15 / 0.17 | 0.177 |  |  | 9/16 | -0.077 | -0.078 |  | -1.4 / -1.4 |  |
| MYM | 5 | h1 * | -0.007 | -0.013 .. -0.000 | -0.0024 | 0.037 / 0.035 / 0.13 | 0.128 | 1 | 0.996 | 5/8 | n/a | -0.007 | False | -2.2 / -2.1 |  |
| MYM | 5 | h2 | -0.010 | -0.019 .. -0.001 | -0.0021 | 0.029 / 0.024 / 0.18 | 0.177 |  |  | 5/8 | n/a | -0.010 |  | -2.3 / -2.2 |  |
| MYM | 5 | h4 | -0.011 | -0.024 .. +0.002 | -0.0015 | 0.092 / 0.081 / 0.33 | 0.31 |  |  | 5/8 | n/a | -0.011 |  | -1.8 / -1.7 | 0.021 |
| MYM | 5 | h8 | -0.013 | -0.032 .. +0.006 | -0.0012 | 0.19 / 0.19 / 0.42 | 0.412 |  |  | 6/8 | n/a | -0.013 |  | -1.4 / -1.3 |  |
| MYM | 5 | h16 | -0.005 | -0.030 .. +0.020 | -0.0004 | 0.67 / 0.68 / 0.8 | 0.807 |  |  | 6/8 | n/a | -0.005 |  | -0.4 / -0.4 |  |
| MYM | 5 | eod | +0.061 | -0.085 .. +0.207 | +0.0010 | 0.41 / 0.41 / 0.46 | 0.474 |  |  | 5/8 | n/a | +0.061 |  | +0.8 / +0.8 |  |
| MYM | 15 | h1 * | -0.008 | -0.019 .. +0.003 | -0.0027 | 0.17 / 0.15 / 0.22 | 0.206 | 1 | 1 | 5/8 | n/a | -0.008 | False | -1.5 / -1.4 |  |
| MYM | 15 | h2 | -0.012 | -0.029 .. +0.006 | -0.0023 | 0.19 / 0.17 / 0.31 | 0.273 |  |  | 4/8 | n/a | -0.012 |  | -1.5 / -1.3 |  |
| MYM | 15 | h4 | -0.018 | -0.041 .. +0.005 | -0.0021 | 0.12 / 0.11 / 0.37 | 0.33 |  |  | 5/8 | n/a | -0.018 |  | -1.6 / -1.6 | 0.039 |
| MYM | 15 | h8 | -0.030 | -0.061 .. +0.002 | -0.0027 | 0.065 / 0.075 / 0.34 | 0.333 |  |  | 6/8 | n/a | -0.030 |  | -1.7 / -1.8 |  |
| MYM | 15 | h16 | -0.023 | -0.071 .. +0.025 | -0.0015 | 0.34 / 0.36 / 0.53 | 0.526 |  |  | 5/8 | n/a | -0.023 |  | -0.9 / -1.0 |  |
| MYM | 15 | eod | -0.079 | -0.211 .. +0.054 | -0.0021 | 0.24 / 0.23 / 0.39 | 0.387 |  |  | 6/8 | n/a | -0.079 |  | -1.2 / -1.2 |  |
| MYM | 60 | h1 | -0.010 | -0.049 .. +0.028 | -0.0027 | 0.6 / 0.59 / 0.63 | 0.643 |  |  | 6/8 | n/a | -0.010 |  | -0.6 / -0.5 |  |
| MYM | 60 | h2 | -0.004 | -0.057 .. +0.048 | -0.0008 | 0.87 / 0.87 / 0.89 | 0.876 |  |  | 4/8 | n/a | -0.004 |  | -0.2 / -0.2 |  |
| MYM | 60 | h4 * | +0.035 | -0.036 .. +0.106 | +0.0046 | 0.33 / 0.33 / 0.35 | 0.356 | 1 | 1 | 4/8 | n/a | +0.035 | False | +1.0 / +1.0 | 0.109 |
| MYM | 60 | h8 | +0.003 | -0.100 .. +0.106 | +0.0003 | 0.95 / 0.96 / 0.96 | 0.953 |  |  | 4/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |
| MYM | 60 | h16 | +0.009 | -0.115 .. +0.134 | +0.0007 | 0.88 / 0.89 / 0.89 | 0.888 |  |  | 5/8 | n/a | +0.009 |  | +0.1 / +0.1 |  |
| MYM | 60 | eod | +0.011 | -0.114 .. +0.135 | +0.0007 | 0.87 / 0.87 / 0.88 | 0.875 |  |  | 5/8 | n/a | +0.011 |  | +0.2 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.010 | -0.014 .. -0.007 | -2.1% | -0.028 | 6.7e-08 |  | 15/16 |
| MES | 5 | h2 * | -0.018 | -0.024 .. -0.012 | -2.5% | -0.044 | 1.2e-09 | 3.76e-07 | 14/16 |
| MES | 5 | h4 | -0.024 | -0.032 .. -0.015 | -2.4% | -0.062 | 1.1e-08 |  | 14/16 |
| MES | 5 | h8 | -0.035 | -0.048 .. -0.022 | -2.4% | -0.079 | 2e-07 |  | 12/16 |
| MES | 5 | h16 | -0.040 | -0.058 .. -0.022 | -1.9% | -0.093 | 1.9e-05 |  | 9/16 |
| MES | 5 | eod | -0.190 | -0.346 .. -0.034 | -1.9% | -0.421 | 0.017 |  | 10/16 |
| MES | 15 | h1 * | -0.029 | -0.035 .. -0.024 | -5.7% | -0.056 | 4e-14 | 1.62e-11 | 16/16 |
| MES | 15 | h2 | -0.036 | -0.045 .. -0.027 | -5.0% | -0.072 | 3e-10 |  | 16/16 |
| MES | 15 | h4 | -0.039 | -0.054 .. -0.025 | -3.7% | -0.081 | 6.5e-06 |  | 14/16 |
| MES | 15 | h8 | -0.051 | -0.071 .. -0.032 | -3.3% | -0.102 | 1.3e-06 |  | 14/16 |
| MES | 15 | h16 | -0.060 | -0.091 .. -0.028 | -2.6% | -0.131 | 0.00022 |  | 13/16 |
| MES | 15 | eod | -0.083 | -0.201 .. +0.035 | -1.5% | -0.218 | 0.17 |  | 8/16 |
| MES | 60 | h1 * | -0.050 | -0.070 .. -0.029 | -9.7% | -0.089 | 0.00013 | 0.0262 | 13/16 |
| MES | 60 | h2 | -0.041 | -0.073 .. -0.010 | -5.6% | -0.103 | 0.015 |  | 12/16 |
| MES | 60 | h4 | -0.028 | -0.066 .. +0.010 | -2.6% | -0.106 | 0.51 |  | 11/16 |
| MES | 60 | h8 | -0.029 | -0.080 .. +0.022 | -1.9% | -0.113 | 0.31 |  | 10/16 |
| MES | 60 | h16 | -0.026 | -0.089 .. +0.036 | -1.3% | -0.087 | 0.41 |  | 10/16 |
| MES | 60 | eod | -0.025 | -0.090 .. +0.040 | -1.2% | -0.083 | 0.45 |  | 9/16 |
| MNQ | 5 | h1 * | -0.013 | -0.017 .. -0.010 | -2.5% | -0.031 | 4.4e-10 | 1.37e-07 | 15/16 |
| MNQ | 5 | h2 | -0.022 | -0.028 .. -0.016 | -2.9% | -0.050 | 4.5e-09 |  | 16/16 |
| MNQ | 5 | h4 | -0.030 | -0.042 .. -0.019 | -2.8% | -0.073 | 1.1e-06 |  | 16/16 |
| MNQ | 5 | h8 | -0.045 | -0.068 .. -0.021 | -2.8% | -0.092 | 0.0002 |  | 16/16 |
| MNQ | 5 | h16 | -0.054 | -0.096 .. -0.013 | -2.3% | -0.120 | 0.01 |  | 14/16 |
| MNQ | 5 | eod | -0.236 | -0.476 .. +0.004 | -1.9% | -0.510 | 0.054 |  | 13/16 |
| MNQ | 15 | h1 * | -0.022 | -0.028 .. -0.016 | -4.2% | -0.048 | 1.6e-06 | 0.000383 | 16/16 |
| MNQ | 15 | h2 | -0.028 | -0.040 .. -0.016 | -3.6% | -0.061 | 0.00071 |  | 15/16 |
| MNQ | 15 | h4 | -0.034 | -0.061 .. -0.007 | -3.0% | -0.077 | 0.038 |  | 14/16 |
| MNQ | 15 | h8 | -0.031 | -0.072 .. +0.010 | -1.8% | -0.086 | 0.14 |  | 10/16 |
| MNQ | 15 | h16 | -0.035 | -0.084 .. +0.013 | -1.4% | -0.118 | 0.15 |  | 12/16 |
| MNQ | 15 | eod | -0.092 | -0.287 .. +0.102 | -1.5% | -0.212 | 0.35 |  | 10/16 |
| MNQ | 60 | h1 * | -0.031 | -0.052 .. -0.010 | -5.9% | -0.078 | 0.0058 | 0.824 | 14/16 |
| MNQ | 60 | h2 | -0.033 | -0.063 .. -0.003 | -4.3% | -0.095 | 0.12 |  | 12/16 |
| MNQ | 60 | h4 | -0.041 | -0.082 .. +0.000 | -3.7% | -0.108 | 0.19 |  | 10/16 |
| MNQ | 60 | h8 | +0.003 | -0.055 .. +0.062 | +0.2% | -0.091 | 0.92 |  | 10/16 |
| MNQ | 60 | h16 | -0.035 | -0.102 .. +0.032 | -1.6% | -0.089 | 0.4 |  | 11/16 |
| MNQ | 60 | eod | -0.035 | -0.101 .. +0.032 | -1.5% | -0.085 | 0.39 |  | 10/16 |
| MYM | 5 | h1 | -0.010 | -0.016 .. -0.005 | -1.9% | -0.023 | 0.0004 |  | 8/8 |
| MYM | 5 | h2 * | -0.021 | -0.031 .. -0.012 | -2.8% | -0.043 | 0.0001 | 0.0207 | 8/8 |
| MYM | 5 | h4 | -0.029 | -0.050 .. -0.008 | -2.6% | -0.066 | 0.0065 |  | 8/8 |
| MYM | 5 | h8 | -0.046 | -0.084 .. -0.008 | -2.9% | -0.088 | 0.017 |  | 7/8 |
| MYM | 5 | h16 | -0.058 | -0.111 .. -0.005 | -2.5% | -0.121 | 0.032 |  | 7/8 |
| MYM | 5 | eod | -0.225 | -0.468 .. +0.018 | -1.9% | -0.523 | 0.07 |  | 5/8 |
| MYM | 15 | h1 * | -0.018 | -0.027 .. -0.009 | -3.4% | -0.042 | 0.011 | 1 | 7/8 |
| MYM | 15 | h2 | -0.021 | -0.036 .. -0.005 | -2.7% | -0.051 | 0.099 |  | 8/8 |
| MYM | 15 | h4 | -0.022 | -0.053 .. +0.009 | -2.0% | -0.056 | 0.29 |  | 6/8 |
| MYM | 15 | h8 | -0.030 | -0.079 .. +0.018 | -1.8% | -0.077 | 0.24 |  | 5/8 |
| MYM | 15 | h16 | -0.030 | -0.119 .. +0.058 | -1.2% | -0.066 | 0.51 |  | 4/8 |
| MYM | 15 | eod | -0.035 | -0.265 .. +0.195 | -0.6% | -0.128 | 0.77 |  | 3/8 |
| MYM | 60 | h1 | -0.047 | -0.071 .. -0.024 | -9.1% | -0.081 | 0.0027 |  | 7/8 |
| MYM | 60 | h2 * | -0.063 | -0.099 .. -0.026 | -8.3% | -0.103 | 0.0023 | 0.371 | 7/8 |
| MYM | 60 | h4 | -0.052 | -0.099 .. -0.006 | -4.8% | -0.114 | 0.11 |  | 7/8 |
| MYM | 60 | h8 | -0.087 | -0.151 .. -0.024 | -5.6% | -0.153 | 0.024 |  | 7/8 |
| MYM | 60 | h16 | -0.092 | -0.167 .. -0.017 | -4.3% | -0.137 | 0.016 |  | 7/8 |
| MYM | 60 | eod | -0.086 | -0.163 .. -0.010 | -3.9% | -0.129 | 0.027 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.26 pts | -0.60 .. +0.08 | 0.32 |
| MES | 15 | -0.88 pts | -1.48 .. -0.28 | 0.0079 |
| MES | 60 | -0.56 pts | -2.26 .. +1.14 | 0.68 |
| MNQ | 5 | -0.39 pts | -0.70 .. -0.08 | 0.025 |
| MNQ | 15 | -0.59 pts | -1.08 .. -0.09 | 0.067 |
| MNQ | 60 | +0.46 pts | -1.20 .. +2.13 | 0.68 |
| MYM | 5 | -0.46 pts | -0.87 .. -0.05 | 0.044 |
| MYM | 15 | -0.63 pts | -1.32 .. +0.06 | 0.16 |
| MYM | 60 | -0.55 pts | -2.42 .. +1.32 | 0.58 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 76203 | +0.019 | 0.250 | +0.25 | -3.25 | -3.37 | -3.18 | -3.41 |
| MES | 5 | h2 | event | against signal | 76203 | +0.028 | 0.250 | +0.38 | -3.12 | -3.26 | -3.03 | -3.34 |
| MES | 5 | h4 | event | against signal | 76203 | +0.026 | 0.250 | +0.34 | -3.16 | -3.26 | -3.10 | -3.39 |
| MES | 5 | h8 | event | against signal | 76203 | +0.018 | 0.250 | +0.31 | -3.19 | -3.24 | -3.16 | -3.39 |
| MES | 5 | h16 | event | with signal | 76203 | -0.012 | 0.250 | -0.13 | -3.63 | -3.60 | -3.65 | -3.42 |
| MES | 5 | eod | event | with signal | 76203 | +0.028 | 0.250 | +0.54 | -2.96 | -3.56 | -2.57 | -2.94 |
| MES | 15 | h1 | event | against signal | 26710 | +0.016 | 0.160 | +0.35 | -3.15 | -3.34 | -3.02 | -3.34 |
| MES | 15 | h2 | event | against signal | 26710 | +0.027 | 0.160 | +0.54 | -2.96 | -3.17 | -2.81 | -3.17 |
| MES | 15 | h4 | event | against signal | 26710 | +0.032 | 0.160 | +0.57 | -2.93 | -3.17 | -2.75 | -3.13 |
| MES | 15 | h8 | event | against signal | 26710 | +0.055 | 0.160 | +0.99 | -2.51 | -3.04 | -2.11 | -2.72 |
| MES | 15 | h16 | event | against signal | 26710 | +0.036 | 0.160 | +0.48 | -3.02 | -3.11 | -2.96 | -3.24 |
| MES | 15 | eod | event | against signal | 26710 | +0.023 | 0.160 | +0.89 | -2.61 | -3.85 | -1.70 | -2.28 |
| MES | 60 | h1 | event | with signal | 2893 | +0.014 | 0.085 | -0.07 | -3.57 | -2.83 | -4.13 | -3.60 |
| MES | 60 | h2 | event | with signal | 2893 | +0.003 | 0.085 | -0.16 | -3.66 | -2.89 | -4.24 | -3.62 |
| MES | 60 | h4 | event | against signal | 2893 | +0.035 | 0.085 | +1.97 | -1.53 | -2.93 | -0.47 | -1.59 |
| MES | 60 | h8 | event | against signal | 2893 | +0.042 | 0.085 | +1.13 | -2.37 | -3.91 | -1.21 | -2.56 |
| MES | 60 | h16 | event | against signal | 2893 | +0.017 | 0.085 | -0.15 | -3.65 | -3.81 | -3.54 | -3.34 |
| MES | 60 | eod | event | against signal | 2893 | +0.017 | 0.085 | -0.15 | -3.65 | -3.81 | -3.54 | -3.51 |
| MNQ | 5 | h1 | event | against signal | 104840 | +0.010 | 0.110 | +0.26 | -1.74 | -1.95 | -1.59 | -1.83 |
| MNQ | 5 | h2 | event | against signal | 104840 | +0.017 | 0.110 | +0.43 | -1.57 | -1.90 | -1.32 | -1.71 |
| MNQ | 5 | h4 | event | against signal | 104840 | +0.009 | 0.110 | +0.31 | -1.69 | -1.90 | -1.52 | -1.77 |
| MNQ | 5 | h8 | event | with signal | 104840 | +0.003 | 0.110 | -0.11 | -2.11 | -2.08 | -2.13 | -2.14 |
| MNQ | 5 | h16 | event | with signal | 104840 | +0.017 | 0.110 | +0.17 | -1.83 | -2.00 | -1.70 | -1.92 |
| MNQ | 5 | eod | event | with signal | 104840 | +0.042 | 0.110 | +0.55 | -1.45 | -1.85 | -1.15 | -1.61 |
| MNQ | 15 | h1 | event | against signal | 32900 | +0.015 | 0.066 | +0.43 | -1.57 | -1.89 | -1.30 | -1.67 |
| MNQ | 15 | h2 | event | against signal | 32900 | +0.019 | 0.066 | +0.50 | -1.50 | -1.83 | -1.24 | -1.55 |
| MNQ | 15 | h4 | event | against signal | 32900 | +0.020 | 0.066 | +0.27 | -1.73 | -1.89 | -1.60 | -1.72 |
| MNQ | 15 | h8 | event | against signal | 32900 | +0.020 | 0.066 | +0.51 | -1.49 | -1.89 | -1.16 | -1.32 |
| MNQ | 15 | h16 | event | against signal | 32900 | +0.038 | 0.066 | +0.71 | -1.29 | -1.60 | -1.03 | -1.20 |
| MNQ | 15 | eod | event | with signal | 32900 | +0.043 | 0.066 | -0.27 | -2.27 | -1.88 | -2.59 | -3.04 |
| MNQ | 60 | h1 | event | with signal | 3051 | +0.026 | 0.035 | +1.94 | -0.06 | -1.65 | +1.19 | -0.14 |
| MNQ | 60 | h2 | event | with signal | 3051 | +0.018 | 0.035 | +1.18 | -0.82 | -1.60 | -0.21 | -0.77 |
| MNQ | 60 | h4 | event | against signal | 3051 | +0.035 | 0.035 | +2.41 | +0.41 | -1.95 | +2.26 | +0.31 |
| MNQ | 60 | h8 | event | against signal | 3051 | +0.079 | 0.035 | +3.36 | +1.36 | -1.66 | +3.73 | +1.19 |
| MNQ | 60 | h16 | event | against signal | 3051 | +0.072 | 0.035 | +0.82 | -1.18 | -1.34 | -1.05 | -0.93 |
| MNQ | 60 | eod | event | against signal | 3051 | +0.072 | 0.035 | +0.82 | -1.18 | -1.34 | -1.05 | -1.12 |
| MYM | 5 | h1 | event | against signal | 55149 | +0.014 | 0.155 | +0.18 | -1.82 | +nan | -1.82 | -1.91 |
| MYM | 5 | h2 | event | against signal | 55149 | +0.019 | 0.155 | +0.23 | -1.77 | +nan | -1.77 | -1.88 |
| MYM | 5 | h4 | event | against signal | 55149 | +0.020 | 0.155 | +0.22 | -1.78 | +nan | -1.78 | -1.89 |
| MYM | 5 | h8 | event | against signal | 55149 | +0.021 | 0.155 | +0.29 | -1.71 | +nan | -1.71 | -1.82 |
| MYM | 5 | h16 | event | against signal | 55149 | +0.019 | 0.155 | +0.25 | -1.75 | +nan | -1.75 | -1.91 |
| MYM | 5 | eod | event | with signal | 55149 | +0.043 | 0.155 | +0.73 | -1.27 | +nan | -1.27 | -1.03 |
| MYM | 15 | h1 | event | against signal | 17234 | +0.013 | 0.092 | +0.21 | -1.79 | +nan | -1.79 | -1.89 |
| MYM | 15 | h2 | event | against signal | 17234 | +0.016 | 0.092 | +0.33 | -1.67 | +nan | -1.67 | -1.76 |
| MYM | 15 | h4 | event | against signal | 17234 | +0.019 | 0.092 | +0.23 | -1.77 | +nan | -1.77 | -1.80 |
| MYM | 15 | h8 | event | against signal | 17234 | +0.032 | 0.092 | +0.49 | -1.51 | +nan | -1.51 | -1.55 |
| MYM | 15 | h16 | event | against signal | 17234 | +0.018 | 0.092 | +0.16 | -1.84 | +nan | -1.84 | -1.71 |
| MYM | 15 | eod | event | against signal | 17234 | +0.061 | 0.092 | +1.31 | -0.69 | +nan | -0.69 | -0.37 |
| MYM | 60 | h1 | event | against signal | 1799 | +0.008 | 0.047 | -0.03 | -2.03 | +nan | -2.03 | -1.95 |
| MYM | 60 | h2 | event | against signal | 1799 | +0.006 | 0.047 | -0.26 | -2.26 | +nan | -2.26 | -2.39 |
| MYM | 60 | h4 | event | with signal | 1799 | +0.033 | 0.047 | +1.04 | -0.96 | +nan | -0.96 | -0.80 |
| MYM | 60 | h8 | event | with signal | 1799 | +0.001 | 0.047 | +1.90 | -0.10 | +nan | -0.10 | +0.07 |
| MYM | 60 | h16 | event | with signal | 1799 | +0.025 | 0.047 | +3.37 | +1.37 | +nan | +1.37 | +0.78 |
| MYM | 60 | eod | event | with signal | 1799 | +0.025 | 0.047 | +3.37 | +1.37 | +nan | +1.37 | +0.83 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.583 | -0.652 | -0.714 | -0.736 | -0.683 | +0.000 | -0.036 | -0.046 | -0.045 | -0.037 | -0.031 |
| MES | 15 | -0.568 | -0.620 | -0.687 | -0.709 | -0.648 | +0.000 | -0.022 | -0.034 | -0.040 | -0.060 | -0.039 |
| MES | 60 | -0.802 | -0.700 | -0.659 | -0.687 | -0.651 | +0.000 | +0.012 | -0.003 | -0.066 | -0.098 | +nan |
| MNQ | 5 | -0.561 | -0.633 | -0.698 | -0.721 | -0.672 | +0.000 | -0.020 | -0.027 | -0.020 | -0.007 | +0.008 |
| MNQ | 15 | -0.526 | -0.593 | -0.663 | -0.689 | -0.633 | +0.000 | -0.018 | -0.022 | -0.023 | -0.025 | -0.054 |
| MNQ | 60 | -0.815 | -0.702 | -0.660 | -0.670 | -0.638 | +0.000 | +0.025 | +0.025 | -0.067 | -0.158 | +nan |
| MYM | 5 | -0.556 | -0.627 | -0.686 | -0.709 | -0.658 | +0.000 | -0.020 | -0.025 | -0.028 | -0.029 | -0.026 |
| MYM | 15 | -0.560 | -0.602 | -0.651 | -0.677 | -0.620 | +0.000 | -0.013 | -0.018 | -0.020 | -0.031 | -0.026 |
| MYM | 60 | -0.940 | -0.746 | -0.667 | -0.684 | -0.663 | +0.000 | -0.010 | -0.002 | +0.046 | -0.046 | +nan |

## Calibration

- MES 5-min: 1036271 bars, 76203 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 26710 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 2893 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 104840 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 32900 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 3051 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 55149 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 17234 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1799 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38308 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
