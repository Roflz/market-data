# Impact card: fam_continuation

any continuation pattern, textbook direction (both sides) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.045 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.011 R20 or more 80% of the time).
- MES 5-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.033 R20, CONFIRMED, q=2.65e-57, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.19 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.246 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.016 R20 over the next 4 bars (1 h), p=0.45; we would catch an effect of 0.025 R20 or more 80% of the time).
- MES 15-min size: the market moves 8% MORE after the event than after matched bars over the next 2 bars (30 min) (+0.060 R20, CONFIRMED, q=8.05e-30, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.08 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.134 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.027 R20 over the next 2 bars (2 h), p=0.35; we would catch an effect of 0.048 R20 or more 80% of the time).
- MES 60-min size: the market moves 10% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.052 R20, CONFIRMED, q=9.7e-09, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.49 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.065 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (5 min), p=0.023; we would catch an effect of 0.014 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 10% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.056 R20, CONFIRMED, q=4.65e-108, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.18 at recent bar sizes, 90% range up to $0.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.020 R20 over the next 2 bars (30 min), p=0.089; we would catch an effect of 0.032 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 11% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.056 R20, CONFIRMED, q=1.69e-29, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.88 at recent bar sizes, 90% range up to $2.18); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: POSSIBLE direction effect +0.051 average bars (~$4.54 per micro at 2018-25 bar sizes) over the next 2 bars (2 h) (in the signal's direction), not confirmed (q=0.101, replicated in the other half=False, 12 of 16 years); best leg (event, with signal) grosses $+2.55 and nets $+0.55 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 60-min size: the market moves 7% MORE after the event than after matched bars over the next 4 bars (4 h) (+0.081 R20, CONFIRMED, q=2.41e-06, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.54 at recent bar sizes, 90% range up to $8.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.085 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.027 R20 or more 80% of the time).
- MYM 5-min size: the market moves 11% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.060 R20, CONFIRMED, q=1.06e-55, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.25 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.185 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.017 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.043 R20 or more 80% of the time).
- MYM 15-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.062 R20, CONFIRMED, q=2.12e-15, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.95 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.102 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.029 R20 over the next 1 bar (1 h), p=0.22; we would catch an effect of 0.068 R20 or more 80% of the time).
- MYM 60-min size: the market moves 15% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.081 R20, CONFIRMED, q=7.43e-10, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.19 at recent bar sizes, 90% range up to $3.04); about 5.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.006 .. +0.003 | -0.0012 | 0.42 / 0.39 / 0.36 | 0.359 |  |  | 10/16 | +0.000 | -0.004 |  | -0.9 / -0.8 |  |
| MES | 5 | h2 | -0.001 | -0.007 .. +0.005 | -0.0005 | 0.71 / 0.7 / 0.72 | 0.713 |  |  | 9/16 | -0.001 | -0.001 |  | -0.4 / -0.4 |  |
| MES | 5 | h4 | +0.003 | -0.004 .. +0.011 | +0.0010 | 0.37 / 0.38 / 0.36 | 0.37 |  |  | 8/16 | +0.005 | +0.002 |  | +0.9 / +0.9 | 0.011 |
| MES | 5 | h8 | +0.002 | -0.009 .. +0.014 | +0.0005 | 0.67 / 0.67 / 0.66 | 0.656 |  |  | 8/16 | -0.004 | +0.009 |  | +0.4 / +0.4 |  |
| MES | 5 | h16 | -0.001 | -0.017 .. +0.016 | -0.0001 | 0.95 / 0.95 / 0.96 | 0.962 |  |  | 7/16 | -0.007 | +0.006 |  | -0.1 / -0.1 |  |
| MES | 5 | eod * | +0.045 | -0.035 .. +0.126 | +0.0013 | 0.27 / 0.27 / 0.28 | 0.295 | 1 | 1 | 11/16 | +0.093 | -0.002 | False | +1.1 / +1.1 |  |
| MES | 15 | h1 | +0.005 | -0.003 .. +0.013 | +0.0029 | 0.21 / 0.2 / 0.2 | 0.198 |  |  | 10/16 | -0.000 | +0.011 |  | +1.3 / +1.3 |  |
| MES | 15 | h2 | +0.009 | -0.002 .. +0.021 | +0.0034 | 0.11 / 0.1 / 0.12 | 0.117 |  |  | 10/16 | -0.008 | +0.027 |  | +1.6 / +1.6 |  |
| MES | 15 | h4 * | +0.016 | -0.002 .. +0.033 | +0.0038 | 0.075 / 0.068 / 0.076 | 0.0787 | 1 | 1 | 10/16 | -0.018 | +0.049 | False | +1.9 / +1.8 | 0.025 |
| MES | 15 | h8 | +0.017 | -0.006 .. +0.041 | +0.0030 | 0.15 / 0.14 / 0.16 | 0.157 |  |  | 10/16 | -0.015 | +0.050 |  | +1.5 / +1.4 |  |
| MES | 15 | h16 | +0.015 | -0.019 .. +0.049 | +0.0018 | 0.38 / 0.37 / 0.37 | 0.371 |  |  | 9/16 | -0.025 | +0.055 |  | +0.9 / +0.9 |  |
| MES | 15 | eod | +0.056 | -0.022 .. +0.134 | +0.0026 | 0.16 / 0.17 / 0.2 | 0.207 |  |  | 10/16 | +0.031 | +0.081 |  | +1.5 / +1.4 |  |
| MES | 60 | h1 | +0.019 | +0.002 .. +0.036 | +0.0100 | 0.024 / 0.035 / 0.032 | 0.0307 |  |  | 12/16 | -0.001 | +0.040 |  | +2.1 / +2.2 |  |
| MES | 60 | h2 * | +0.027 | +0.004 .. +0.049 | +0.0096 | 0.021 / 0.033 / 0.034 | 0.0339 | 1 | 0.98 | 11/16 | +0.011 | +0.042 | False | +2.1 / +2.3 |  |
| MES | 60 | h4 | +0.034 | +0.003 .. +0.064 | +0.0087 | 0.03 / 0.038 / 0.048 | 0.0498 |  |  | 10/16 | +0.004 | +0.064 |  | +1.9 / +2.2 | 0.048 |
| MES | 60 | h8 | +0.031 | -0.008 .. +0.069 | +0.0058 | 0.12 / 0.14 / 0.17 | 0.165 |  |  | 10/16 | +0.016 | +0.045 |  | +1.4 / +1.6 |  |
| MES | 60 | h16 | +0.013 | -0.030 .. +0.057 | +0.0019 | 0.55 / 0.58 / 0.6 | 0.597 |  |  | 7/16 | -0.010 | +0.037 |  | +0.5 / +0.6 |  |
| MES | 60 | eod | +0.026 | -0.020 .. +0.073 | +0.0035 | 0.27 / 0.3 / 0.31 | 0.307 |  |  | 8/16 | +0.002 | +0.050 |  | +1.0 / +1.1 |  |
| MNQ | 5 | h1 * | +0.007 | +0.002 .. +0.013 | +0.0037 | 0.0038 / 0.003 / 0.0016 | 0.00182 | 0.582 | 0.6 | 10/16 | +0.006 | +0.009 | False | +3.2 / +2.9 |  |
| MNQ | 5 | h2 | +0.008 | +0.000 .. +0.015 | +0.0024 | 0.043 / 0.03 / 0.031 | 0.0362 |  |  | 11/16 | +0.001 | +0.014 |  | +2.3 / +2.0 |  |
| MNQ | 5 | h4 | +0.014 | +0.005 .. +0.024 | +0.0029 | 0.0043 / 0.004 / 0.0098 | 0.00834 |  |  | 12/16 | +0.010 | +0.018 |  | +3.1 / +2.9 | 0.014 |
| MNQ | 5 | h8 | +0.018 | +0.004 .. +0.031 | +0.0024 | 0.01 / 0.011 / 0.034 | 0.0323 |  |  | 11/16 | +0.013 | +0.023 |  | +2.6 / +2.6 |  |
| MNQ | 5 | h16 | +0.010 | -0.011 .. +0.031 | +0.0010 | 0.34 / 0.34 / 0.39 | 0.383 |  |  | 9/16 | -0.003 | +0.023 |  | +1.0 / +1.0 |  |
| MNQ | 5 | eod | +0.115 | -0.010 .. +0.241 | +0.0023 | 0.071 / 0.061 / 0.056 | 0.0516 |  |  | 12/16 | +0.113 | +0.118 |  | +2.1 / +1.8 |  |
| MNQ | 15 | h1 | +0.013 | +0.004 .. +0.022 | +0.0053 | 0.0044 / 0.0052 / 0.016 | 0.0185 |  |  | 11/16 | +0.005 | +0.020 |  | +2.7 / +2.8 |  |
| MNQ | 15 | h2 * | +0.020 | +0.007 .. +0.034 | +0.0050 | 0.0031 / 0.0018 / 0.02 | 0.0245 | 1 | 0.54 | 13/16 | +0.008 | +0.033 | False | +3.0 / +3.0 |  |
| MNQ | 15 | h4 | +0.023 | +0.004 .. +0.042 | +0.0034 | 0.017 / 0.016 / 0.11 | 0.112 |  |  | 14/16 | +0.008 | +0.038 |  | +2.4 / +2.4 | 0.032 |
| MNQ | 15 | h8 | +0.027 | -0.001 .. +0.055 | +0.0030 | 0.06 / 0.053 / 0.16 | 0.154 |  |  | 11/16 | +0.016 | +0.038 |  | +2.0 / +1.9 |  |
| MNQ | 15 | h16 | +0.024 | -0.014 .. +0.062 | +0.0022 | 0.22 / 0.22 / 0.33 | 0.331 |  |  | 9/16 | -0.008 | +0.056 |  | +1.2 / +1.2 |  |
| MNQ | 15 | eod | +0.053 | -0.045 .. +0.150 | +0.0017 | 0.29 / 0.28 / 0.41 | 0.407 |  |  | 11/16 | -0.020 | +0.124 |  | +1.2 / +1.1 |  |
| MNQ | 60 | h1 | +0.032 | +0.012 .. +0.052 | +0.0157 | 0.0015 / 0.0023 / 0.0013 | 0.00182 |  |  | 13/16 | +0.031 | +0.034 |  | +3.1 / +3.2 |  |
| MNQ | 60 | h2 * | +0.051 | +0.024 .. +0.078 | +0.0173 | 0.00021 / 0.00037 / 0.00021 | 0.00026 | 0.101 | 0.054 | 12/16 | +0.037 | +0.065 | False | +3.6 / +3.7 |  |
| MNQ | 60 | h4 | +0.055 | +0.021 .. +0.089 | +0.0132 | 0.0016 / 0.0018 / 0.003 | 0.00208 |  |  | 11/16 | +0.022 | +0.088 |  | +3.0 / +3.2 | 0.051 |
| MNQ | 60 | h8 | +0.054 | +0.012 .. +0.097 | +0.0095 | 0.012 / 0.015 / 0.02 | 0.0201 |  |  | 11/16 | +0.038 | +0.071 |  | +2.4 / +2.5 |  |
| MNQ | 60 | h16 | +0.045 | -0.004 .. +0.094 | +0.0060 | 0.074 / 0.077 / 0.082 | 0.0821 |  |  | 10/16 | +0.022 | +0.068 |  | +1.8 / +1.8 |  |
| MNQ | 60 | eod | +0.048 | -0.003 .. +0.099 | +0.0062 | 0.065 / 0.066 / 0.069 | 0.0709 |  |  | 10/16 | +0.022 | +0.074 |  | +1.9 / +1.8 |  |
| MYM | 5 | h1 | -0.001 | -0.008 .. +0.005 | -0.0005 | 0.73 / 0.73 / 0.88 | 0.885 |  |  | 4/8 | n/a | -0.001 |  | -0.4 / -0.4 |  |
| MYM | 5 | h2 | -0.003 | -0.012 .. +0.006 | -0.0008 | 0.53 / 0.56 / 0.73 | 0.711 |  |  | 5/8 | n/a | -0.003 |  | -0.6 / -0.6 |  |
| MYM | 5 | h4 | -0.003 | -0.016 .. +0.010 | -0.0005 | 0.62 / 0.63 / 0.82 | 0.811 |  |  | 3/8 | n/a | -0.003 |  | -0.5 / -0.5 | 0.027 |
| MYM | 5 | h8 | -0.007 | -0.027 .. +0.014 | -0.0008 | 0.51 / 0.49 / 0.67 | 0.679 |  |  | 6/8 | n/a | -0.007 |  | -0.7 / -0.7 |  |
| MYM | 5 | h16 | -0.008 | -0.035 .. +0.019 | -0.0008 | 0.54 / 0.55 / 0.67 | 0.676 |  |  | 6/8 | n/a | -0.008 |  | -0.6 / -0.6 |  |
| MYM | 5 | eod * | -0.085 | -0.227 .. +0.058 | -0.0017 | 0.24 / 0.27 / 0.29 | 0.294 | 1 | 1 | 7/8 | n/a | -0.085 | False | -1.1 / -1.2 |  |
| MYM | 15 | h1 | -0.000 | -0.013 .. +0.012 | -0.0002 | 0.94 / 0.94 / 0.95 | 0.957 |  |  | 4/8 | n/a | -0.000 |  | -0.1 / -0.1 |  |
| MYM | 15 | h2 | +0.003 | -0.017 .. +0.024 | +0.0008 | 0.74 / 0.73 / 0.81 | 0.791 |  |  | 5/8 | n/a | +0.003 |  | +0.4 / +0.3 |  |
| MYM | 15 | h4 * | +0.017 | -0.009 .. +0.043 | +0.0024 | 0.2 / 0.19 / 0.42 | 0.408 | 1 | 1 | 7/8 | n/a | +0.017 | False | +1.3 / +1.3 | 0.043 |
| MYM | 15 | h8 | +0.002 | -0.032 .. +0.036 | +0.0002 | 0.91 / 0.91 / 0.94 | 0.941 |  |  | 5/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 15 | h16 | +0.007 | -0.042 .. +0.057 | +0.0006 | 0.77 / 0.77 / 0.85 | 0.858 |  |  | 4/8 | n/a | +0.007 |  | +0.3 / +0.3 |  |
| MYM | 15 | eod | +0.016 | -0.106 .. +0.138 | +0.0005 | 0.79 / 0.79 / 0.86 | 0.865 |  |  | 5/8 | n/a | +0.016 |  | +0.3 / +0.3 |  |
| MYM | 60 | h1 * | +0.029 | +0.004 .. +0.054 | +0.0143 | 0.024 / 0.036 / 0.031 | 0.0342 | 1 | 0.98 | 7/8 | n/a | +0.029 | False | +2.0 / +2.3 |  |
| MYM | 60 | h2 | +0.027 | -0.007 .. +0.061 | +0.0093 | 0.13 / 0.15 / 0.16 | 0.159 |  |  | 4/8 | n/a | +0.027 |  | +1.4 / +1.5 |  |
| MYM | 60 | h4 | +0.031 | -0.018 .. +0.079 | +0.0077 | 0.21 / 0.22 / 0.22 | 0.233 |  |  | 5/8 | n/a | +0.031 |  | +1.2 / +1.2 | 0.068 |
| MYM | 60 | h8 | +0.021 | -0.041 .. +0.083 | +0.0038 | 0.5 / 0.5 / 0.51 | 0.503 |  |  | 4/8 | n/a | +0.021 |  | +0.7 / +0.7 |  |
| MYM | 60 | h16 | -0.012 | -0.080 .. +0.057 | -0.0016 | 0.74 / 0.75 / 0.75 | 0.735 |  |  | 4/8 | n/a | -0.012 |  | -0.3 / -0.3 |  |
| MYM | 60 | eod | -0.007 | -0.079 .. +0.066 | -0.0009 | 0.86 / 0.86 / 0.86 | 0.856 |  |  | 4/8 | n/a | -0.007 |  | -0.2 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.033 | +0.029 .. +0.037 | +6.6% | +0.084 | 2.3e-60 | 2.65e-57 | 16/16 |
| MES | 5 | h2 | +0.038 | +0.033 .. +0.044 | +5.5% | +0.094 | 9.9e-44 |  | 15/16 |
| MES | 5 | h4 | +0.046 | +0.039 .. +0.054 | +4.6% | +0.110 | 1.7e-32 |  | 14/16 |
| MES | 5 | h8 | +0.061 | +0.049 .. +0.073 | +4.2% | +0.128 | 6.6e-25 |  | 14/16 |
| MES | 5 | h16 | +0.083 | +0.065 .. +0.100 | +3.9% | +0.163 | 5.4e-20 |  | 14/16 |
| MES | 5 | eod | +0.204 | +0.048 .. +0.361 | +2.0% | +0.484 | 0.011 |  | 13/16 |
| MES | 15 | h1 | +0.043 | +0.036 .. +0.050 | +8.4% | +0.112 | 1.2e-30 |  | 15/16 |
| MES | 15 | h2 * | +0.060 | +0.051 .. +0.070 | +8.3% | +0.141 | 1e-32 | 8.05e-30 | 16/16 |
| MES | 15 | h4 | +0.079 | +0.063 .. +0.095 | +7.5% | +0.168 | 5.6e-23 |  | 16/16 |
| MES | 15 | h8 | +0.101 | +0.078 .. +0.124 | +6.6% | +0.188 | 4.1e-18 |  | 15/16 |
| MES | 15 | h16 | +0.113 | +0.078 .. +0.148 | +4.9% | +0.220 | 3.8e-10 |  | 14/16 |
| MES | 15 | eod | +0.086 | -0.036 .. +0.207 | +1.6% | +0.265 | 0.17 |  | 12/16 |
| MES | 60 | h1 * | +0.052 | +0.037 .. +0.067 | +10.1% | +0.134 | 2.8e-11 | 9.7e-09 | 13/16 |
| MES | 60 | h2 | +0.071 | +0.050 .. +0.091 | +9.6% | +0.161 | 2.9e-11 |  | 14/16 |
| MES | 60 | h4 | +0.088 | +0.059 .. +0.118 | +8.4% | +0.182 | 6.7e-09 |  | 12/16 |
| MES | 60 | h8 | +0.083 | +0.047 .. +0.120 | +5.5% | +0.190 | 1.2e-05 |  | 15/16 |
| MES | 60 | h16 | +0.066 | +0.026 .. +0.107 | +3.2% | +0.166 | 0.0016 |  | 13/16 |
| MES | 60 | eod | +0.062 | +0.020 .. +0.104 | +2.9% | +0.166 | 0.0037 |  | 13/16 |
| MNQ | 5 | h1 * | +0.056 | +0.051 .. +0.060 | +10.4% | +0.118 | 3.1e-111 | 4.65e-108 | 16/16 |
| MNQ | 5 | h2 | +0.071 | +0.063 .. +0.079 | +9.2% | +0.145 | 7.3e-73 |  | 16/16 |
| MNQ | 5 | h4 | +0.094 | +0.080 .. +0.108 | +8.5% | +0.185 | 4.4e-39 |  | 15/16 |
| MNQ | 5 | h8 | +0.127 | +0.100 .. +0.154 | +7.8% | +0.240 | 6.3e-20 |  | 15/16 |
| MNQ | 5 | h16 | +0.174 | +0.125 .. +0.224 | +7.3% | +0.321 | 5.4e-12 |  | 15/16 |
| MNQ | 5 | eod | +0.675 | +0.372 .. +0.978 | +5.4% | +1.441 | 1.3e-05 |  | 14/16 |
| MNQ | 15 | h1 * | +0.056 | +0.048 .. +0.065 | +10.6% | +0.121 | 2.2e-32 | 1.69e-29 | 16/16 |
| MNQ | 15 | h2 | +0.074 | +0.058 .. +0.089 | +9.5% | +0.150 | 7.4e-21 |  | 15/16 |
| MNQ | 15 | h4 | +0.092 | +0.061 .. +0.122 | +8.1% | +0.183 | 5.8e-09 |  | 15/16 |
| MNQ | 15 | h8 | +0.120 | +0.070 .. +0.171 | +7.2% | +0.218 | 3.1e-06 |  | 14/16 |
| MNQ | 15 | h16 | +0.144 | +0.086 .. +0.203 | +5.7% | +0.252 | 1.4e-06 |  | 15/16 |
| MNQ | 15 | eod | +0.140 | -0.067 .. +0.346 | +2.2% | +0.351 | 0.18 |  | 11/16 |
| MNQ | 60 | h1 | +0.043 | +0.028 .. +0.059 | +8.2% | +0.111 | 3.4e-08 |  | 15/16 |
| MNQ | 60 | h2 | +0.065 | +0.044 .. +0.085 | +8.4% | +0.141 | 1.4e-08 |  | 14/16 |
| MNQ | 60 | h4 * | +0.081 | +0.054 .. +0.109 | +7.4% | +0.163 | 8.5e-09 | 2.41e-06 | 14/16 |
| MNQ | 60 | h8 | +0.074 | +0.041 .. +0.107 | +4.7% | +0.178 | 3.3e-05 |  | 15/16 |
| MNQ | 60 | h16 | +0.079 | +0.038 .. +0.120 | +3.6% | +0.184 | 0.00022 |  | 13/16 |
| MNQ | 60 | eod | +0.077 | +0.037 .. +0.117 | +3.3% | +0.181 | 0.00032 |  | 13/16 |
| MYM | 5 | h1 * | +0.060 | +0.053 .. +0.068 | +11.3% | +0.132 | 9.2e-59 | 1.06e-55 | 8/8 |
| MYM | 5 | h2 | +0.073 | +0.062 .. +0.083 | +9.6% | +0.156 | 3.1e-41 |  | 8/8 |
| MYM | 5 | h4 | +0.085 | +0.064 .. +0.107 | +7.8% | +0.182 | 3.6e-15 |  | 7/8 |
| MYM | 5 | h8 | +0.109 | +0.070 .. +0.148 | +6.8% | +0.221 | 5.2e-08 |  | 7/8 |
| MYM | 5 | h16 | +0.139 | +0.084 .. +0.195 | +6.0% | +0.263 | 8.4e-07 |  | 7/8 |
| MYM | 5 | eod | +0.500 | +0.226 .. +0.773 | +4.3% | +0.960 | 0.00035 |  | 7/8 |
| MYM | 15 | h1 * | +0.062 | +0.051 .. +0.073 | +11.7% | +0.130 | 4.4e-18 | 2.12e-15 | 8/8 |
| MYM | 15 | h2 | +0.073 | +0.053 .. +0.093 | +9.5% | +0.153 | 1.1e-08 |  | 7/8 |
| MYM | 15 | h4 | +0.077 | +0.040 .. +0.114 | +6.9% | +0.166 | 0.00031 |  | 7/8 |
| MYM | 15 | h8 | +0.078 | +0.021 .. +0.135 | +4.8% | +0.172 | 0.0078 |  | 6/8 |
| MYM | 15 | h16 | +0.085 | -0.014 .. +0.185 | +3.5% | +0.164 | 0.097 |  | 7/8 |
| MYM | 15 | eod | +0.118 | -0.127 .. +0.363 | +2.0% | +0.327 | 0.36 |  | 6/8 |
| MYM | 60 | h1 * | +0.081 | +0.058 .. +0.103 | +15.4% | +0.165 | 2.1e-12 | 7.43e-10 | 8/8 |
| MYM | 60 | h2 | +0.088 | +0.059 .. +0.118 | +11.7% | +0.195 | 9.9e-08 |  | 6/8 |
| MYM | 60 | h4 | +0.098 | +0.056 .. +0.140 | +9.1% | +0.204 | 4.8e-06 |  | 6/8 |
| MYM | 60 | h8 | +0.102 | +0.052 .. +0.151 | +6.6% | +0.226 | 6.2e-05 |  | 7/8 |
| MYM | 60 | h16 | +0.095 | +0.037 .. +0.153 | +4.5% | +0.206 | 0.0013 |  | 7/8 |
| MYM | 60 | eod | +0.079 | +0.018 .. +0.140 | +3.5% | +0.198 | 0.011 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.03 pts | -0.28 .. +0.22 | 0.99 |
| MES | 15 | +0.30 pts | -0.13 .. +0.73 | 0.17 |
| MES | 60 | +1.22 pts | +0.44 .. +2.00 | 0.0031 |
| MNQ | 5 | -0.08 pts | -0.34 .. +0.19 | 0.82 |
| MNQ | 15 | +0.52 pts | +0.05 .. +0.99 | 0.031 |
| MNQ | 60 | +1.58 pts | +0.77 .. +2.40 | 0.00015 |
| MYM | 5 | -0.25 pts | -0.57 .. +0.08 | 0.27 |
| MYM | 15 | -0.01 pts | -0.59 .. +0.57 | 0.98 |
| MYM | 60 | +1.10 pts | -0.04 .. +2.24 | 0.058 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 174490 | +0.013 | 0.388 | +0.11 | -3.39 | -3.43 | -3.34 | -3.49 |
| MES | 5 | h2 | event | against signal | 174490 | +0.017 | 0.388 | +0.16 | -3.34 | -3.39 | -3.27 | -3.48 |
| MES | 5 | h4 | event | with signal | 174490 | -0.013 | 0.388 | -0.10 | -3.60 | -3.57 | -3.64 | -3.45 |
| MES | 5 | h8 | event | with signal | 174490 | -0.013 | 0.388 | -0.05 | -3.55 | -3.60 | -3.50 | -3.42 |
| MES | 5 | h16 | event | against signal | 174490 | +0.017 | 0.388 | +0.08 | -3.42 | -3.39 | -3.46 | -3.57 |
| MES | 5 | eod | event | with signal | 174490 | +0.049 | 0.388 | +0.39 | -3.11 | -3.12 | -3.11 | -3.16 |
| MES | 15 | h1 | event | with signal | 50225 | -0.003 | 0.203 | +0.01 | -3.49 | -3.57 | -3.40 | -3.34 |
| MES | 15 | h2 | event | with signal | 50225 | -0.000 | 0.203 | +0.09 | -3.41 | -3.60 | -3.21 | -3.24 |
| MES | 15 | h4 | event | with signal | 50225 | +0.006 | 0.203 | +0.43 | -3.07 | -3.64 | -2.45 | -2.90 |
| MES | 15 | h8 | event | with signal | 50225 | +0.007 | 0.203 | +0.45 | -3.05 | -3.64 | -2.41 | -2.86 |
| MES | 15 | h16 | event | with signal | 50225 | +0.006 | 0.203 | +0.19 | -3.31 | -3.74 | -2.85 | -3.14 |
| MES | 15 | eod | event | with signal | 50225 | +0.075 | 0.203 | +1.18 | -2.32 | -3.07 | -1.50 | -2.62 |
| MES | 60 | h1 | event | with signal | 11450 | +0.020 | 0.095 | +0.76 | -2.74 | -3.38 | -2.12 | -2.72 |
| MES | 60 | h2 | event | with signal | 11450 | +0.025 | 0.095 | +0.99 | -2.51 | -3.08 | -1.96 | -2.41 |
| MES | 60 | h4 | event | with signal | 11450 | +0.031 | 0.095 | +1.12 | -2.38 | -3.39 | -1.40 | -2.20 |
| MES | 60 | h8 | event | with signal | 11450 | +0.026 | 0.095 | +1.26 | -2.24 | -2.80 | -1.69 | -1.97 |
| MES | 60 | h16 | event | with signal | 11450 | +0.019 | 0.095 | +1.58 | -1.92 | -3.01 | -0.86 | -2.01 |
| MES | 60 | eod | event | with signal | 11450 | +0.027 | 0.095 | +2.07 | -1.43 | -2.92 | +0.01 | -1.34 |
| MNQ | 5 | h1 | event | with signal | 167788 | +0.003 | 0.165 | +0.06 | -1.94 | -2.01 | -1.83 | -1.88 |
| MNQ | 5 | h2 | event | with signal | 167788 | +0.000 | 0.165 | +0.04 | -1.96 | -2.04 | -1.84 | -1.87 |
| MNQ | 5 | h4 | event | with signal | 167788 | +0.010 | 0.165 | +0.17 | -1.83 | -1.99 | -1.58 | -1.78 |
| MNQ | 5 | h8 | event | with signal | 167788 | +0.021 | 0.165 | +0.28 | -1.72 | -1.99 | -1.31 | -1.75 |
| MNQ | 5 | h16 | event | with signal | 167788 | +0.017 | 0.165 | +0.21 | -1.79 | -2.01 | -1.45 | -1.86 |
| MNQ | 5 | eod | event | with signal | 167788 | +0.157 | 0.165 | +1.33 | -0.67 | -1.64 | +0.79 | -1.13 |
| MNQ | 15 | h1 | event | with signal | 49876 | +0.009 | 0.084 | +0.35 | -1.65 | -1.96 | -1.27 | -1.55 |
| MNQ | 15 | h2 | event | with signal | 49876 | +0.018 | 0.084 | +0.48 | -1.52 | -1.89 | -1.07 | -1.47 |
| MNQ | 15 | h4 | event | with signal | 49876 | +0.023 | 0.084 | +0.74 | -1.26 | -1.87 | -0.51 | -1.24 |
| MNQ | 15 | h8 | event | with signal | 49876 | +0.032 | 0.084 | +0.89 | -1.11 | -1.87 | -0.18 | -1.20 |
| MNQ | 15 | h16 | event | with signal | 49876 | +0.028 | 0.084 | +0.92 | -1.08 | -1.99 | +0.03 | -1.13 |
| MNQ | 15 | eod | event | with signal | 49876 | +0.084 | 0.084 | +2.39 | +0.39 | -1.90 | +3.20 | -0.23 |
| MNQ | 60 | h1 | event | with signal | 11577 | +0.034 | 0.038 | +1.28 | -0.72 | -1.27 | -0.14 | -0.79 |
| MNQ | 60 | h2 | event | with signal | 11577 | +0.052 | 0.038 | +2.55 | +0.55 | -1.06 | +2.24 | +0.58 |
| MNQ | 60 | h4 | event | with signal | 11577 | +0.056 | 0.038 | +3.12 | +1.12 | -1.38 | +3.75 | +1.20 |
| MNQ | 60 | h8 | event | with signal | 11577 | +0.056 | 0.038 | +3.51 | +1.51 | -0.81 | +3.95 | +1.59 |
| MNQ | 60 | h16 | event | with signal | 11577 | +0.054 | 0.038 | +3.96 | +1.96 | -0.95 | +5.01 | +1.76 |
| MNQ | 60 | eod | event | with signal | 11577 | +0.054 | 0.038 | +4.38 | +2.38 | -1.02 | +5.95 | +2.39 |
| MYM | 5 | h1 | event | against signal | 77510 | +0.009 | 0.185 | +0.06 | -1.94 | +nan | -1.94 | -2.02 |
| MYM | 5 | h2 | event | against signal | 77510 | +0.012 | 0.185 | +0.13 | -1.87 | +nan | -1.87 | -1.97 |
| MYM | 5 | h4 | event | against signal | 77510 | +0.012 | 0.185 | +0.06 | -1.94 | +nan | -1.94 | -2.04 |
| MYM | 5 | h8 | event | against signal | 77510 | +0.015 | 0.185 | +0.12 | -1.88 | +nan | -1.88 | -1.96 |
| MYM | 5 | h16 | event | against signal | 77510 | +0.021 | 0.185 | +0.10 | -1.90 | +nan | -1.90 | -2.02 |
| MYM | 5 | eod | event | against signal | 77510 | +0.101 | 0.185 | +0.36 | -1.64 | +nan | -1.64 | -1.75 |
| MYM | 15 | h1 | event | against signal | 24592 | +0.006 | 0.102 | +0.04 | -1.96 | +nan | -1.96 | -2.07 |
| MYM | 15 | h2 | event | with signal | 24592 | -0.001 | 0.102 | +0.05 | -1.95 | +nan | -1.95 | -1.86 |
| MYM | 15 | h4 | event | with signal | 24592 | +0.015 | 0.102 | +0.51 | -1.49 | +nan | -1.49 | -1.47 |
| MYM | 15 | h8 | event | with signal | 24592 | +0.001 | 0.102 | +0.07 | -1.93 | +nan | -1.93 | -1.92 |
| MYM | 15 | h16 | event | with signal | 24592 | +0.012 | 0.102 | -0.04 | -2.04 | +nan | -2.04 | -2.14 |
| MYM | 15 | eod | event | with signal | 24592 | +0.027 | 0.102 | +0.61 | -1.39 | +nan | -1.39 | -1.56 |
| MYM | 60 | h1 | event | with signal | 5852 | +0.030 | 0.048 | +0.72 | -1.28 | +nan | -1.28 | -1.32 |
| MYM | 60 | h2 | event | with signal | 5852 | +0.023 | 0.048 | +0.53 | -1.47 | +nan | -1.47 | -1.28 |
| MYM | 60 | h4 | event | with signal | 5852 | +0.026 | 0.048 | +0.55 | -1.45 | +nan | -1.45 | -1.21 |
| MYM | 60 | h8 | event | with signal | 5852 | +0.017 | 0.048 | +0.17 | -1.83 | +nan | -1.83 | -1.57 |
| MYM | 60 | h16 | event | against signal | 5852 | -0.003 | 0.048 | -0.17 | -2.17 | +nan | -2.17 | -1.73 |
| MYM | 60 | eod | event | against signal | 5852 | -0.006 | 0.048 | -0.67 | -2.67 | +nan | -2.67 | -2.34 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.951 | -1.040 | -1.080 | -1.092 | -1.105 | +0.000 | -0.065 | -0.069 | -0.066 | -0.067 | -0.073 |
| MES | 15 | -1.129 | -1.233 | -1.287 | -1.288 | -1.293 | +0.000 | -0.019 | -0.016 | -0.011 | -0.014 | -0.025 |
| MES | 60 | -1.333 | -1.391 | -1.450 | -1.469 | -1.457 | +0.000 | +0.018 | +0.022 | +0.027 | -0.068 | -0.026 |
| MNQ | 5 | -1.133 | -1.233 | -1.275 | -1.282 | -1.282 | +0.000 | -0.024 | -0.027 | -0.018 | -0.009 | -0.014 |
| MNQ | 15 | -1.236 | -1.340 | -1.393 | -1.401 | -1.397 | +0.000 | +0.002 | +0.011 | +0.018 | +0.021 | +0.011 |
| MNQ | 60 | -1.378 | -1.465 | -1.511 | -1.550 | -1.537 | +0.000 | +0.033 | +0.048 | +0.052 | -0.058 | +0.046 |
| MYM | 5 | -1.129 | -1.240 | -1.292 | -1.302 | -1.305 | +0.000 | -0.020 | -0.023 | -0.026 | -0.031 | -0.039 |
| MYM | 15 | -1.207 | -1.313 | -1.377 | -1.391 | -1.389 | +0.000 | -0.008 | -0.004 | +0.013 | -0.006 | +0.005 |
| MYM | 60 | -1.338 | -1.437 | -1.504 | -1.544 | -1.527 | +0.000 | +0.031 | +0.031 | +0.038 | -0.036 | -0.035 |

## Calibration

- MES 5-min: 1036271 bars, 174490 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 50225 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 11450 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 167788 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 49876 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 11577 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 77510 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 24592 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 5852 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39936 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
