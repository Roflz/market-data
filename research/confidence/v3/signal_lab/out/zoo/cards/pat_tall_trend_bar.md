# Impact card: pat_tall_trend_bar

candle pattern tall_trend_bar in its textbook direction: range > 1.46 x avgR22 and body >= 0.5 x range; direction of the body (continuation) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.005 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.014 R20 or more 80% of the time).
- MES 5-min size: the market moves 13% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.067 R20, CONFIRMED, q=2.37e-150, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.22 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.233 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.013 R20 over the next 2 bars (30 min), p=0.36; we would catch an effect of 0.029 R20 or more 80% of the time).
- MES 15-min size: the market moves 11% MORE after the event than after matched bars over the next 2 bars (30 min) (+0.081 R20, CONFIRMED, q=1.45e-37, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.20 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.134 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.023 R20 over the next 1 bar (1 h), p=0.21; we would catch an effect of 0.052 R20 or more 80% of the time).
- MES 60-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.062 R20, CONFIRMED, q=2.01e-10, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.43 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.065 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.020 R20 over the next 4 bars (20 min), p=0.013; we would catch an effect of 0.016 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 15% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.078 R20, CONFIRMED, q=7.41e-119, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.48 at recent bar sizes, 90% range up to $0.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.017 R20 over the next 1 bar (15 min), p=0.029; we would catch an effect of 0.037 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 13% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.071 R20, CONFIRMED, q=2.41e-36, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.74 at recent bar sizes, 90% range up to $2.53); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: POSSIBLE direction effect +0.055 average bars (~$4.88 per micro at 2018-25 bar sizes) over the next 2 bars (2 h) (in the signal's direction), not confirmed (q=0.129, replicated in the other half=False, 12 of 16 years); best leg (event, with signal) grosses $+2.81 and nets $+0.81 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 60-min size: the market moves 10% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.075 R20, CONFIRMED, q=7.35e-08, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.88 at recent bar sizes, 90% range up to $8.31); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.094 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.034 R20 or more 80% of the time).
- MYM 5-min size: the market moves 15% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.079 R20, CONFIRMED, q=6.53e-65, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.33 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.181 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.025 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 15-min size: the market moves 14% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.076 R20, CONFIRMED, q=1.88e-20, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.11 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.102 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.031 R20 over the next 1 bar (1 h), p=0.26; we would catch an effect of 0.074 R20 or more 80% of the time).
- MYM 60-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.086 R20, CONFIRMED, q=1.16e-09, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.27 at recent bar sizes, 90% range up to $3.07); about 5.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.009 .. +0.003 | -0.0013 | 0.37 / 0.35 / 0.3 | 0.306 |  |  | 9/16 | -0.001 | -0.005 |  | -1.0 / -0.9 |  |
| MES | 5 | h2 * | -0.005 | -0.014 .. +0.003 | -0.0017 | 0.23 / 0.22 / 0.17 | 0.171 | 1 | 1 | 10/16 | -0.005 | -0.005 | False | -1.3 / -1.2 |  |
| MES | 5 | h4 | +0.000 | -0.011 .. +0.011 | +0.0000 | 0.98 / 0.98 / 0.95 | 0.948 |  |  | 8/16 | +0.003 | -0.002 |  | +0.0 / +0.0 | 0.014 |
| MES | 5 | h8 | -0.001 | -0.017 .. +0.015 | -0.0002 | 0.87 / 0.87 / 0.88 | 0.869 |  |  | 9/16 | -0.008 | +0.006 |  | -0.2 / -0.2 |  |
| MES | 5 | h16 | -0.001 | -0.024 .. +0.022 | -0.0001 | 0.94 / 0.94 / 0.95 | 0.944 |  |  | 6/16 | -0.017 | +0.015 |  | -0.1 / -0.1 |  |
| MES | 5 | eod | +0.022 | -0.082 .. +0.126 | +0.0005 | 0.68 / 0.68 / 0.66 | 0.664 |  |  | 9/16 | +0.017 | +0.028 |  | +0.5 / +0.4 |  |
| MES | 15 | h1 | +0.007 | -0.003 .. +0.016 | +0.0032 | 0.17 / 0.16 / 0.17 | 0.172 |  |  | 9/16 | -0.002 | +0.016 |  | +1.4 / +1.4 |  |
| MES | 15 | h2 * | +0.013 | -0.001 .. +0.027 | +0.0041 | 0.06 / 0.054 / 0.064 | 0.063 | 1 | 1 | 11/16 | -0.009 | +0.035 | False | +1.9 / +1.9 |  |
| MES | 15 | h4 | +0.018 | -0.002 .. +0.038 | +0.0038 | 0.076 / 0.069 / 0.085 | 0.0852 |  |  | 9/16 | -0.020 | +0.056 |  | +1.8 / +1.8 | 0.029 |
| MES | 15 | h8 | +0.023 | -0.004 .. +0.050 | +0.0035 | 0.092 / 0.081 / 0.099 | 0.0946 |  |  | 9/16 | -0.011 | +0.057 |  | +1.7 / +1.7 |  |
| MES | 15 | h16 | +0.023 | -0.015 .. +0.061 | +0.0024 | 0.23 / 0.22 / 0.23 | 0.238 |  |  | 8/16 | -0.018 | +0.064 |  | +1.2 / +1.2 |  |
| MES | 15 | eod | +0.061 | -0.022 .. +0.145 | +0.0025 | 0.15 / 0.16 / 0.21 | 0.216 |  |  | 10/16 | +0.014 | +0.109 |  | +1.5 / +1.4 |  |
| MES | 60 | h1 * | +0.023 | +0.005 .. +0.042 | +0.0113 | 0.013 / 0.022 / 0.018 | 0.0193 | 1 | 0.926 | 12/16 | +0.004 | +0.043 | False | +2.2 / +2.5 |  |
| MES | 60 | h2 | +0.031 | +0.006 .. +0.055 | +0.0103 | 0.015 / 0.026 / 0.025 | 0.0263 |  |  | 13/16 | +0.018 | +0.043 |  | +2.2 / +2.4 |  |
| MES | 60 | h4 | +0.034 | +0.001 .. +0.068 | +0.0082 | 0.046 / 0.059 / 0.066 | 0.0662 |  |  | 10/16 | +0.002 | +0.066 |  | +1.8 / +2.0 | 0.052 |
| MES | 60 | h8 | +0.024 | -0.018 .. +0.065 | +0.0041 | 0.26 / 0.29 / 0.31 | 0.31 |  |  | 9/16 | +0.013 | +0.035 |  | +1.0 / +1.1 |  |
| MES | 60 | h16 | +0.001 | -0.045 .. +0.047 | +0.0001 | 0.97 / 0.98 / 0.98 | 0.977 |  |  | 7/16 | -0.014 | +0.015 |  | +0.0 / +0.0 |  |
| MES | 60 | eod | +0.011 | -0.037 .. +0.060 | +0.0014 | 0.64 / 0.66 / 0.66 | 0.656 |  |  | 7/16 | -0.006 | +0.029 |  | +0.4 / +0.5 |  |
| MNQ | 5 | h1 | +0.008 | +0.002 .. +0.015 | +0.0034 | 0.011 / 0.0093 / 0.0057 | 0.00703 |  |  | 10/16 | +0.003 | +0.014 |  | +2.8 / +2.6 |  |
| MNQ | 5 | h2 | +0.009 | -0.000 .. +0.019 | +0.0023 | 0.058 / 0.042 / 0.036 | 0.0367 |  |  | 11/16 | -0.000 | +0.019 |  | +2.2 / +1.9 |  |
| MNQ | 5 | h4 * | +0.020 | +0.007 .. +0.032 | +0.0032 | 0.0021 / 0.0018 / 0.005 | 0.00599 | 0.343 | 0.426 | 11/16 | +0.015 | +0.024 | False | +3.3 / +3.1 | 0.016 |
| MNQ | 5 | h8 | +0.020 | +0.003 .. +0.037 | +0.0022 | 0.024 / 0.024 / 0.056 | 0.0581 |  |  | 9/16 | +0.013 | +0.027 |  | +2.4 / +2.2 |  |
| MNQ | 5 | h16 | +0.016 | -0.010 .. +0.043 | +0.0013 | 0.22 / 0.23 / 0.26 | 0.257 |  |  | 10/16 | +0.002 | +0.030 |  | +1.3 / +1.2 |  |
| MNQ | 5 | eod | +0.117 | -0.022 .. +0.256 | +0.0019 | 0.099 / 0.088 / 0.099 | 0.099 |  |  | 10/16 | +0.127 | +0.107 |  | +1.9 / +1.6 |  |
| MNQ | 15 | h1 * | +0.017 | +0.007 .. +0.028 | +0.0063 | 0.0012 / 0.0012 / 0.0045 | 0.00573 | 0.706 | 0.293 | 12/16 | +0.008 | +0.027 | False | +3.1 / +3.2 |  |
| MNQ | 15 | h2 | +0.024 | +0.009 .. +0.040 | +0.0053 | 0.0024 / 0.0013 / 0.015 | 0.0175 |  |  | 13/16 | +0.010 | +0.039 |  | +3.1 / +3.0 |  |
| MNQ | 15 | h4 | +0.025 | +0.003 .. +0.047 | +0.0032 | 0.025 / 0.024 / 0.15 | 0.137 |  |  | 14/16 | +0.009 | +0.041 |  | +2.2 / +2.2 | 0.037 |
| MNQ | 15 | h8 | +0.032 | -0.000 .. +0.064 | +0.0032 | 0.052 / 0.047 / 0.13 | 0.133 |  |  | 13/16 | +0.030 | +0.034 |  | +2.0 / +1.9 |  |
| MNQ | 15 | h16 | +0.024 | -0.019 .. +0.067 | +0.0019 | 0.28 / 0.28 / 0.4 | 0.41 |  |  | 9/16 | +0.000 | +0.047 |  | +1.1 / +1.1 |  |
| MNQ | 15 | eod | +0.065 | -0.038 .. +0.168 | +0.0019 | 0.21 / 0.2 / 0.36 | 0.359 |  |  | 13/16 | -0.001 | +0.131 |  | +1.3 / +1.2 |  |
| MNQ | 60 | h1 | +0.038 | +0.016 .. +0.060 | +0.0171 | 0.00077 / 0.0011 / 0.00064 | 0.00104 |  |  | 13/16 | +0.033 | +0.042 |  | +3.3 / +3.4 |  |
| MNQ | 60 | h2 * | +0.055 | +0.025 .. +0.085 | +0.0174 | 0.00033 / 0.00052 / 0.00024 | 0.000781 | 0.129 | 0.089 | 12/16 | +0.036 | +0.074 | False | +3.6 / +3.6 |  |
| MNQ | 60 | h4 | +0.054 | +0.017 .. +0.091 | +0.0121 | 0.0044 / 0.0058 / 0.007 | 0.00755 |  |  | 11/16 | +0.012 | +0.095 |  | +2.7 / +2.9 | 0.054 |
| MNQ | 60 | h8 | +0.053 | +0.008 .. +0.099 | +0.0087 | 0.02 / 0.029 / 0.03 | 0.0287 |  |  | 10/16 | +0.028 | +0.079 |  | +2.2 / +2.3 |  |
| MNQ | 60 | h16 | +0.037 | -0.014 .. +0.088 | +0.0046 | 0.16 / 0.17 / 0.17 | 0.171 |  |  | 10/16 | +0.008 | +0.066 |  | +1.4 / +1.4 |  |
| MNQ | 60 | eod | +0.042 | -0.012 .. +0.095 | +0.0050 | 0.13 / 0.14 / 0.13 | 0.127 |  |  | 10/16 | +0.007 | +0.076 |  | +1.5 / +1.5 |  |
| MYM | 5 | h1 | -0.000 | -0.008 .. +0.008 | -0.0001 | 0.96 / 0.96 / 0.92 | 0.924 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h2 | -0.002 | -0.014 .. +0.009 | -0.0006 | 0.68 / 0.68 / 0.83 | 0.827 |  |  | 5/8 | n/a | -0.002 |  | -0.4 / -0.4 |  |
| MYM | 5 | h4 | -0.003 | -0.019 .. +0.012 | -0.0005 | 0.67 / 0.67 / 0.86 | 0.851 |  |  | 4/8 | n/a | -0.003 |  | -0.4 / -0.4 | 0.034 |
| MYM | 5 | h8 | -0.009 | -0.035 .. +0.016 | -0.0009 | 0.46 / 0.43 / 0.6 | 0.602 |  |  | 6/8 | n/a | -0.009 |  | -0.8 / -0.7 |  |
| MYM | 5 | h16 | -0.005 | -0.039 .. +0.028 | -0.0004 | 0.76 / 0.76 / 0.83 | 0.832 |  |  | 5/8 | n/a | -0.005 |  | -0.3 / -0.3 |  |
| MYM | 5 | eod * | -0.094 | -0.259 .. +0.071 | -0.0016 | 0.26 / 0.29 / 0.32 | 0.316 | 1 | 1 | 5/8 | n/a | -0.094 | False | -1.1 / -1.1 |  |
| MYM | 15 | h1 | +0.001 | -0.013 .. +0.015 | +0.0003 | 0.92 / 0.92 / 0.94 | 0.951 |  |  | 5/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 15 | h2 | +0.007 | -0.016 .. +0.030 | +0.0015 | 0.55 / 0.53 / 0.66 | 0.62 |  |  | 6/8 | n/a | +0.007 |  | +0.7 / +0.6 |  |
| MYM | 15 | h4 * | +0.025 | -0.004 .. +0.054 | +0.0033 | 0.087 / 0.086 / 0.29 | 0.289 | 1 | 1 | 7/8 | n/a | +0.025 | False | +1.7 / +1.7 | 0.046 |
| MYM | 15 | h8 | +0.005 | -0.033 .. +0.043 | +0.0005 | 0.79 / 0.8 / 0.86 | 0.854 |  |  | 5/8 | n/a | +0.005 |  | +0.2 / +0.3 |  |
| MYM | 15 | h16 | +0.002 | -0.056 .. +0.060 | +0.0001 | 0.95 / 0.95 / 0.97 | 0.964 |  |  | 4/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 15 | eod | +0.028 | -0.101 .. +0.157 | +0.0008 | 0.67 / 0.67 / 0.78 | 0.791 |  |  | 6/8 | n/a | +0.028 |  | +0.4 / +0.4 |  |
| MYM | 60 | h1 * | +0.031 | +0.003 .. +0.059 | +0.0142 | 0.032 / 0.043 / 0.037 | 0.039 | 1 | 0.993 | 7/8 | n/a | +0.031 | False | +2.0 / +2.1 |  |
| MYM | 60 | h2 | +0.027 | -0.011 .. +0.064 | +0.0086 | 0.16 / 0.18 / 0.19 | 0.207 |  |  | 4/8 | n/a | +0.027 |  | +1.3 / +1.4 |  |
| MYM | 60 | h4 | +0.029 | -0.023 .. +0.081 | +0.0068 | 0.28 / 0.28 / 0.28 | 0.292 |  |  | 5/8 | n/a | +0.029 |  | +1.1 / +1.1 | 0.074 |
| MYM | 60 | h8 | +0.017 | -0.051 .. +0.085 | +0.0029 | 0.62 / 0.61 / 0.61 | 0.608 |  |  | 4/8 | n/a | +0.017 |  | +0.5 / +0.5 |  |
| MYM | 60 | h16 | -0.005 | -0.080 .. +0.070 | -0.0006 | 0.9 / 0.9 / 0.9 | 0.897 |  |  | 4/8 | n/a | -0.005 |  | -0.1 / -0.1 |  |
| MYM | 60 | eod | +0.003 | -0.076 .. +0.083 | +0.0004 | 0.93 / 0.93 / 0.92 | 0.926 |  |  | 4/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.067 | +0.062 .. +0.072 | +13.5% | +0.162 | 1.2e-153 | 2.37e-150 | 16/16 |
| MES | 5 | h2 | +0.083 | +0.077 .. +0.090 | +11.9% | +0.196 | 5.2e-131 |  | 16/16 |
| MES | 5 | h4 | +0.106 | +0.096 .. +0.115 | +10.6% | +0.240 | 7.1e-109 |  | 16/16 |
| MES | 5 | h8 | +0.132 | +0.117 .. +0.146 | +9.2% | +0.286 | 6.4e-69 |  | 16/16 |
| MES | 5 | h16 | +0.168 | +0.147 .. +0.190 | +8.0% | +0.346 | 1.6e-53 |  | 16/16 |
| MES | 5 | eod | +0.355 | +0.212 .. +0.499 | +3.6% | +0.626 | 1.2e-06 |  | 15/16 |
| MES | 15 | h1 | +0.059 | +0.050 .. +0.068 | +11.6% | +0.147 | 4.3e-38 |  | 16/16 |
| MES | 15 | h2 * | +0.081 | +0.069 .. +0.093 | +11.1% | +0.185 | 1.6e-40 | 1.45e-37 | 16/16 |
| MES | 15 | h4 | +0.105 | +0.087 .. +0.124 | +10.0% | +0.222 | 2.2e-29 |  | 16/16 |
| MES | 15 | h8 | +0.132 | +0.106 .. +0.159 | +8.6% | +0.251 | 5.9e-23 |  | 15/16 |
| MES | 15 | h16 | +0.146 | +0.106 .. +0.185 | +6.4% | +0.285 | 3.3e-13 |  | 14/16 |
| MES | 15 | eod | +0.124 | +0.005 .. +0.243 | +2.3% | +0.284 | 0.041 |  | 13/16 |
| MES | 60 | h1 * | +0.062 | +0.045 .. +0.079 | +12.1% | +0.152 | 5.3e-13 | 2.01e-10 | 13/16 |
| MES | 60 | h2 | +0.079 | +0.055 .. +0.102 | +10.6% | +0.181 | 2.3e-11 |  | 14/16 |
| MES | 60 | h4 | +0.099 | +0.064 .. +0.133 | +9.3% | +0.203 | 2.1e-08 |  | 12/16 |
| MES | 60 | h8 | +0.091 | +0.050 .. +0.131 | +6.0% | +0.215 | 1.9e-05 |  | 13/16 |
| MES | 60 | h16 | +0.075 | +0.031 .. +0.119 | +3.7% | +0.196 | 0.00093 |  | 13/16 |
| MES | 60 | eod | +0.073 | +0.027 .. +0.119 | +3.4% | +0.193 | 0.0017 |  | 13/16 |
| MNQ | 5 | h1 * | +0.078 | +0.071 .. +0.084 | +14.6% | +0.177 | 4.4e-122 | 7.41e-119 | 16/16 |
| MNQ | 5 | h2 | +0.097 | +0.087 .. +0.106 | +12.5% | +0.211 | 2.8e-89 |  | 16/16 |
| MNQ | 5 | h4 | +0.125 | +0.110 .. +0.140 | +11.3% | +0.260 | 4e-59 |  | 16/16 |
| MNQ | 5 | h8 | +0.160 | +0.132 .. +0.187 | +9.9% | +0.318 | 8.8e-30 |  | 15/16 |
| MNQ | 5 | h16 | +0.197 | +0.148 .. +0.246 | +8.2% | +0.388 | 2.4e-15 |  | 15/16 |
| MNQ | 5 | eod | +0.443 | +0.207 .. +0.678 | +3.5% | +0.779 | 0.00023 |  | 13/16 |
| MNQ | 15 | h1 * | +0.071 | +0.061 .. +0.080 | +13.2% | +0.151 | 2.8e-39 | 2.41e-36 | 16/16 |
| MNQ | 15 | h2 | +0.091 | +0.074 .. +0.107 | +11.7% | +0.186 | 1.2e-23 |  | 15/16 |
| MNQ | 15 | h4 | +0.110 | +0.078 .. +0.142 | +9.7% | +0.225 | 3e-11 |  | 15/16 |
| MNQ | 15 | h8 | +0.146 | +0.093 .. +0.198 | +8.7% | +0.262 | 6e-08 |  | 14/16 |
| MNQ | 15 | h16 | +0.162 | +0.102 .. +0.222 | +6.4% | +0.281 | 1.1e-07 |  | 15/16 |
| MNQ | 15 | eod | +0.139 | -0.060 .. +0.337 | +2.2% | +0.315 | 0.17 |  | 12/16 |
| MNQ | 60 | h1 | +0.052 | +0.034 .. +0.069 | +9.8% | +0.129 | 3.4e-09 |  | 15/16 |
| MNQ | 60 | h2 * | +0.075 | +0.052 .. +0.098 | +9.7% | +0.163 | 2.3e-10 | 7.35e-08 | 14/16 |
| MNQ | 60 | h4 | +0.091 | +0.061 .. +0.122 | +8.3% | +0.186 | 4.4e-09 |  | 14/16 |
| MNQ | 60 | h8 | +0.085 | +0.048 .. +0.122 | +5.4% | +0.204 | 1.2e-05 |  | 15/16 |
| MNQ | 60 | h16 | +0.089 | +0.045 .. +0.133 | +4.1% | +0.212 | 9.3e-05 |  | 14/16 |
| MNQ | 60 | eod | +0.090 | +0.046 .. +0.134 | +3.9% | +0.211 | 0.00011 |  | 13/16 |
| MYM | 5 | h1 * | +0.079 | +0.070 .. +0.088 | +14.9% | +0.176 | 5.3e-68 | 6.53e-65 | 8/8 |
| MYM | 5 | h2 | +0.098 | +0.086 .. +0.110 | +12.8% | +0.209 | 4.6e-55 |  | 8/8 |
| MYM | 5 | h4 | +0.115 | +0.092 .. +0.137 | +10.5% | +0.248 | 1e-23 |  | 8/8 |
| MYM | 5 | h8 | +0.147 | +0.108 .. +0.186 | +9.2% | +0.298 | 2e-13 |  | 7/8 |
| MYM | 5 | h16 | +0.185 | +0.129 .. +0.242 | +7.9% | +0.349 | 9.7e-11 |  | 7/8 |
| MYM | 5 | eod | +0.466 | +0.214 .. +0.718 | +4.0% | +0.908 | 0.00029 |  | 7/8 |
| MYM | 15 | h1 * | +0.076 | +0.062 .. +0.089 | +14.2% | +0.159 | 3.2e-23 | 1.88e-20 | 8/8 |
| MYM | 15 | h2 | +0.092 | +0.070 .. +0.113 | +12.0% | +0.190 | 2.1e-10 |  | 8/8 |
| MYM | 15 | h4 | +0.098 | +0.059 .. +0.137 | +8.8% | +0.210 | 8.5e-05 |  | 7/8 |
| MYM | 15 | h8 | +0.104 | +0.046 .. +0.163 | +6.3% | +0.226 | 0.001 |  | 7/8 |
| MYM | 15 | h16 | +0.100 | +0.000 .. +0.200 | +4.1% | +0.199 | 0.052 |  | 7/8 |
| MYM | 15 | eod | +0.136 | -0.103 .. +0.374 | +2.3% | +0.354 | 0.31 |  | 7/8 |
| MYM | 60 | h1 * | +0.086 | +0.062 .. +0.110 | +16.5% | +0.181 | 3.2e-12 | 1.16e-09 | 8/8 |
| MYM | 60 | h2 | +0.094 | +0.061 .. +0.126 | +12.4% | +0.209 | 5e-08 |  | 6/8 |
| MYM | 60 | h4 | +0.110 | +0.062 .. +0.158 | +10.2% | +0.226 | 6.6e-06 |  | 6/8 |
| MYM | 60 | h8 | +0.107 | +0.051 .. +0.164 | +6.9% | +0.240 | 0.00018 |  | 7/8 |
| MYM | 60 | h16 | +0.098 | +0.035 .. +0.161 | +4.6% | +0.224 | 0.0025 |  | 7/8 |
| MYM | 60 | eod | +0.092 | +0.026 .. +0.158 | +4.1% | +0.220 | 0.0066 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.08 pts | -0.23 .. +0.39 | 0.61 |
| MES | 15 | +0.34 pts | -0.12 .. +0.80 | 0.15 |
| MES | 60 | +1.30 pts | +0.51 .. +2.09 | 0.0027 |
| MNQ | 5 | +0.20 pts | -0.09 .. +0.50 | 0.18 |
| MNQ | 15 | +0.69 pts | +0.18 .. +1.21 | 0.0083 |
| MNQ | 60 | +1.92 pts | +1.07 .. +2.77 | 1.1e-05 |
| MYM | 5 | -0.19 pts | -0.56 .. +0.18 | 0.46 |
| MYM | 15 | +0.20 pts | -0.44 .. +0.83 | 0.56 |
| MYM | 60 | +1.35 pts | +0.14 .. +2.55 | 0.029 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 104432 | +0.014 | 0.324 | +0.15 | -3.35 | -3.41 | -3.29 | -3.47 |
| MES | 5 | h2 | event | against signal | 104432 | +0.021 | 0.324 | +0.24 | -3.26 | -3.35 | -3.17 | -3.43 |
| MES | 5 | h4 | event | with signal | 104432 | -0.016 | 0.324 | -0.17 | -3.67 | -3.58 | -3.75 | -3.49 |
| MES | 5 | h8 | event | against signal | 104432 | +0.017 | 0.324 | +0.14 | -3.36 | -3.36 | -3.37 | -3.53 |
| MES | 5 | h16 | event | against signal | 104432 | +0.019 | 0.324 | +0.08 | -3.42 | -3.33 | -3.49 | -3.60 |
| MES | 5 | eod | event | with signal | 104432 | +0.024 | 0.324 | +0.26 | -3.24 | -3.27 | -3.21 | -3.25 |
| MES | 15 | h1 | event | with signal | 39905 | -0.002 | 0.197 | +0.04 | -3.46 | -3.59 | -3.32 | -3.30 |
| MES | 15 | h2 | event | with signal | 39905 | +0.003 | 0.197 | +0.12 | -3.38 | -3.63 | -3.13 | -3.20 |
| MES | 15 | h4 | event | with signal | 39905 | +0.008 | 0.197 | +0.45 | -3.05 | -3.72 | -2.39 | -2.88 |
| MES | 15 | h8 | event | with signal | 39905 | +0.012 | 0.197 | +0.42 | -3.08 | -3.66 | -2.52 | -2.89 |
| MES | 15 | h16 | event | with signal | 39905 | +0.014 | 0.197 | +0.18 | -3.32 | -3.78 | -2.87 | -3.14 |
| MES | 15 | eod | event | with signal | 39905 | +0.081 | 0.197 | +1.24 | -2.26 | -3.18 | -1.35 | -2.57 |
| MES | 60 | h1 | event | with signal | 10133 | +0.023 | 0.096 | +0.86 | -2.64 | -3.30 | -2.01 | -2.62 |
| MES | 60 | h2 | event | with signal | 10133 | +0.029 | 0.096 | +1.00 | -2.50 | -2.95 | -2.05 | -2.38 |
| MES | 60 | h4 | event | with signal | 10133 | +0.030 | 0.096 | +1.22 | -2.28 | -3.47 | -1.12 | -2.08 |
| MES | 60 | h8 | event | with signal | 10133 | +0.017 | 0.096 | +0.88 | -2.62 | -3.03 | -2.23 | -2.31 |
| MES | 60 | h16 | event | with signal | 10133 | +0.004 | 0.096 | +0.95 | -2.55 | -3.15 | -1.97 | -2.57 |
| MES | 60 | eod | event | with signal | 10133 | +0.009 | 0.096 | +1.43 | -2.07 | -3.11 | -1.05 | -1.89 |
| MNQ | 5 | h1 | event | with signal | 117544 | +0.004 | 0.146 | +0.09 | -1.91 | -2.01 | -1.80 | -1.85 |
| MNQ | 5 | h2 | event | with signal | 117544 | +0.002 | 0.146 | +0.05 | -1.95 | -2.05 | -1.84 | -1.85 |
| MNQ | 5 | h4 | event | with signal | 117544 | +0.015 | 0.146 | +0.24 | -1.76 | -1.97 | -1.50 | -1.70 |
| MNQ | 5 | h8 | event | with signal | 117544 | +0.022 | 0.146 | +0.38 | -1.62 | -1.97 | -1.19 | -1.65 |
| MNQ | 5 | h16 | event | with signal | 117544 | +0.022 | 0.146 | +0.42 | -1.58 | -1.98 | -1.10 | -1.65 |
| MNQ | 5 | eod | event | with signal | 117544 | +0.152 | 0.146 | +1.51 | -0.49 | -1.62 | +0.87 | -0.94 |
| MNQ | 15 | h1 | event | with signal | 40940 | +0.013 | 0.081 | +0.47 | -1.53 | -1.91 | -1.10 | -1.42 |
| MNQ | 15 | h2 | event | with signal | 40940 | +0.022 | 0.081 | +0.59 | -1.41 | -1.86 | -0.91 | -1.35 |
| MNQ | 15 | h4 | event | with signal | 40940 | +0.024 | 0.081 | +0.80 | -1.20 | -1.84 | -0.50 | -1.18 |
| MNQ | 15 | h8 | event | with signal | 40940 | +0.036 | 0.081 | +0.89 | -1.11 | -1.77 | -0.39 | -1.19 |
| MNQ | 15 | h16 | event | with signal | 40940 | +0.027 | 0.081 | +1.02 | -0.98 | -1.94 | +0.08 | -1.01 |
| MNQ | 15 | eod | event | with signal | 40940 | +0.091 | 0.081 | +2.83 | +0.83 | -1.75 | +3.68 | +0.26 |
| MNQ | 60 | h1 | event | with signal | 10241 | +0.039 | 0.038 | +1.60 | -0.40 | -1.18 | +0.38 | -0.46 |
| MNQ | 60 | h2 | event | with signal | 10241 | +0.056 | 0.038 | +2.81 | +0.81 | -0.96 | +2.60 | +0.86 |
| MNQ | 60 | h4 | event | with signal | 10241 | +0.054 | 0.038 | +3.51 | +1.51 | -1.44 | +4.50 | +1.63 |
| MNQ | 60 | h8 | event | with signal | 10241 | +0.054 | 0.038 | +3.46 | +1.46 | -0.94 | +3.89 | +1.63 |
| MNQ | 60 | h16 | event | with signal | 10241 | +0.043 | 0.038 | +3.43 | +1.43 | -1.10 | +3.99 | +1.39 |
| MNQ | 60 | eod | event | with signal | 10241 | +0.044 | 0.038 | +4.14 | +2.14 | -1.20 | +5.53 | +2.32 |
| MYM | 5 | h1 | event | against signal | 57303 | +0.008 | 0.181 | +0.06 | -1.94 | +nan | -1.94 | -2.02 |
| MYM | 5 | h2 | event | against signal | 57303 | +0.011 | 0.181 | +0.12 | -1.88 | +nan | -1.88 | -1.98 |
| MYM | 5 | h4 | event | against signal | 57303 | +0.012 | 0.181 | +0.04 | -1.96 | +nan | -1.96 | -2.06 |
| MYM | 5 | h8 | event | against signal | 57303 | +0.017 | 0.181 | +0.12 | -1.88 | +nan | -1.88 | -1.96 |
| MYM | 5 | h16 | event | against signal | 57303 | +0.017 | 0.181 | +0.03 | -1.97 | +nan | -1.97 | -2.09 |
| MYM | 5 | eod | event | against signal | 57303 | +0.104 | 0.181 | +0.34 | -1.66 | +nan | -1.66 | -1.73 |
| MYM | 15 | h1 | event | with signal | 20441 | -0.005 | 0.102 | -0.06 | -2.06 | +nan | -2.06 | -1.96 |
| MYM | 15 | h2 | event | with signal | 20441 | +0.002 | 0.102 | +0.03 | -1.97 | +nan | -1.97 | -1.88 |
| MYM | 15 | h4 | event | with signal | 20441 | +0.024 | 0.102 | +0.59 | -1.41 | +nan | -1.41 | -1.38 |
| MYM | 15 | h8 | event | with signal | 20441 | +0.004 | 0.102 | +0.01 | -1.99 | +nan | -1.99 | -1.98 |
| MYM | 15 | h16 | event | with signal | 20441 | +0.007 | 0.102 | -0.29 | -2.29 | +nan | -2.29 | -2.38 |
| MYM | 15 | eod | event | with signal | 20441 | +0.038 | 0.102 | +0.23 | -1.77 | +nan | -1.77 | -1.95 |
| MYM | 60 | h1 | event | with signal | 5210 | +0.032 | 0.048 | +0.70 | -1.30 | +nan | -1.30 | -1.34 |
| MYM | 60 | h2 | event | with signal | 5210 | +0.023 | 0.048 | +0.41 | -1.59 | +nan | -1.59 | -1.40 |
| MYM | 60 | h4 | event | with signal | 5210 | +0.025 | 0.048 | +0.55 | -1.45 | +nan | -1.45 | -1.22 |
| MYM | 60 | h8 | event | with signal | 5210 | +0.014 | 0.048 | -0.09 | -2.09 | +nan | -2.09 | -1.84 |
| MYM | 60 | h16 | event | against signal | 5210 | -0.011 | 0.048 | -0.54 | -2.54 | +nan | -2.54 | -2.05 |
| MYM | 60 | eod | event | with signal | 5210 | +0.018 | 0.048 | +1.14 | -0.86 | +nan | -0.86 | -1.24 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.227 | -1.345 | -1.384 | -1.389 | -1.381 | +0.000 | -0.027 | -0.035 | -0.030 | -0.032 | -0.035 |
| MES | 15 | -1.230 | -1.362 | -1.423 | -1.425 | -1.428 | +0.000 | -0.006 | -0.001 | +0.002 | +0.003 | -0.006 |
| MES | 60 | -1.335 | -1.434 | -1.515 | -1.546 | -1.537 | +0.000 | +0.023 | +0.028 | +0.030 | -0.125 | -0.128 |
| MNQ | 5 | -1.317 | -1.445 | -1.485 | -1.488 | -1.472 | +0.000 | -0.009 | -0.011 | +0.002 | +0.008 | +0.007 |
| MNQ | 15 | -1.331 | -1.461 | -1.520 | -1.529 | -1.519 | +0.000 | +0.011 | +0.019 | +0.023 | +0.030 | +0.012 |
| MNQ | 60 | -1.377 | -1.515 | -1.585 | -1.635 | -1.629 | +0.000 | +0.039 | +0.054 | +0.053 | -0.091 | -0.084 |
| MYM | 5 | -1.279 | -1.409 | -1.460 | -1.464 | -1.454 | +0.000 | -0.013 | -0.018 | -0.021 | -0.029 | -0.030 |
| MYM | 15 | -1.285 | -1.414 | -1.489 | -1.503 | -1.497 | +0.000 | -0.006 | +0.001 | +0.022 | -0.001 | -0.002 |
| MYM | 60 | -1.335 | -1.487 | -1.572 | -1.621 | -1.607 | +0.000 | +0.033 | +0.033 | +0.039 | -0.069 | +0.098 |

## Calibration

- MES 5-min: 1036271 bars, 104432 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 39905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 10133 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 117544 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 40940 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 10241 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 57303 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 20441 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 5210 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41800 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
