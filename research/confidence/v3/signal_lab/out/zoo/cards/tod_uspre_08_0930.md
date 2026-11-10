# Impact card: tod_uspre_08_0930

bar closes in the uspre_08_0930 block (ET) vs all other bars [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.056 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.067 R20 or more 80% of the time).
- MES 5-min size: the market moves 23% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.112 R20, CONFIRMED, q=3.09e-152, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.90 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.240 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.195 R20 over the rest of the session (to 16:45), p=0.054; we would catch an effect of 0.114 R20 or more 80% of the time).
- MES 15-min size: the market moves 52% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.265 R20, CONFIRMED, q=1.57e-193, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.27 at recent bar sizes, 90% range up to $3.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.053 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.102 R20 or more 80% of the time).
- MES 60-min size: the market moves 97% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.717 R20, CONFIRMED, q=1.75e-254, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.51 at recent bar sizes, 90% range up to $6.88); about 19.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.041 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.098 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 103% MORE after the event than after matched bars over the next 16 bars (80 min) (+2.481 R20, CONFIRMED, q=2.08e-160, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.90 at recent bar sizes, 90% range up to $3.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.123 R20 over the rest of the session (to 16:45), p=0.56; we would catch an effect of 0.149 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 91% MORE after the event than after matched bars over the next 16 bars (4 h) (+2.302 R20, CONFIRMED, q=1.09e-215, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.32 at recent bar sizes, 90% range up to $8.18); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.067 R20 over the rest of the session (to 16:45), p=0.04; we would catch an effect of 0.114 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 74% MORE after the event than after matched bars over the next 8 bars (8 h) (+1.165 R20, CONFIRMED, q=1.35e-274, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.07 at recent bar sizes, 90% range up to $10.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.138 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.314 R20 or more 80% of the time).
- MYM 5-min size: the market moves 98% MORE after the event than after matched bars over the next 16 bars (80 min) (+2.286 R20, CONFIRMED, q=6.19e-87, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.39 at recent bar sizes, 90% range up to $4.62); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.240 R20 over the rest of the session (to 16:45), p=0.17; we would catch an effect of 0.211 R20 or more 80% of the time).
- MYM 15-min size: the market moves 118% MORE after the event than after matched bars over the next 8 bars (2 h) (+1.934 R20, CONFIRMED, q=6.83e-134, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.00 at recent bar sizes, 90% range up to $3.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.062 R20 over the next 16 bars (16 h), p=0.56; we would catch an effect of 0.156 R20 or more 80% of the time).
- MYM 60-min size: the market moves 68% MORE after the event than after matched bars over the next 8 bars (8 h) (+1.046 R20, CONFIRMED, q=2.22e-144, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.22 at recent bar sizes, 90% range up to $7.49); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.002 | -0.006 .. +0.009 | +0.0006 | 0.68 / 0.67 / 0.92 | nan |  |  | 8/16 | +0.001 | +0.002 |  | +0.4 / +0.4 |  |
| MES | 5 | h2 | -0.006 | -0.025 .. +0.013 | -0.0015 | 0.54 / 0.53 / 0.95 | nan |  |  | 8/16 | -0.001 | -0.011 |  | -0.9 / -0.6 |  |
| MES | 5 | h4 | -0.026 | -0.072 .. +0.020 | -0.0044 | 0.28 / 0.27 / 0.87 | nan |  |  | 9/16 | -0.014 | -0.037 |  | -2.3 / -1.1 | 0.067 |
| MES | 5 | h8 * | -0.056 | -0.149 .. +0.036 | -0.0066 | 0.23 / 0.23 / 0.77 | nan | 1 | 1 | 10/16 | -0.036 | -0.077 | False | -3.4 / -1.2 |  |
| MES | 5 | h16 | -0.041 | -0.176 .. +0.093 | -0.0034 | 0.55 / 0.55 / 0.86 | nan |  |  | 10/16 | -0.031 | -0.051 |  | -1.9 / -0.6 |  |
| MES | 5 | eod | -0.019 | -0.191 .. +0.153 | -0.0003 | 0.83 / 0.83 / 0.81 | nan |  |  | 10/16 | -0.066 | +0.028 |  | -0.4 / -0.2 |  |
| MES | 15 | h1 | +0.001 | -0.013 .. +0.016 | +0.0004 | 0.86 / 0.87 / 0.92 | nan |  |  | 9/16 | -0.008 | +0.011 |  | +0.2 / +0.2 |  |
| MES | 15 | h2 | -0.011 | -0.046 .. +0.024 | -0.0024 | 0.55 / 0.55 / 0.99 | nan |  |  | 9/16 | -0.022 | +0.000 |  | -0.7 / -0.6 |  |
| MES | 15 | h4 | -0.029 | -0.108 .. +0.049 | -0.0044 | 0.46 / 0.46 / 0.96 | nan |  |  | 10/16 | -0.023 | -0.036 |  | -1.2 / -0.7 | 0.114 |
| MES | 15 | h8 | -0.027 | -0.146 .. +0.091 | -0.0029 | 0.65 / 0.66 / 0.99 | nan |  |  | 10/16 | -0.011 | -0.043 |  | -0.8 / -0.4 |  |
| MES | 15 | h16 | -0.001 | -0.163 .. +0.162 | -0.0000 | 1 / 1 / 0.98 | nan |  |  | 7/16 | +0.054 | -0.055 |  | -0.0 / -0.0 |  |
| MES | 15 | eod * | -0.195 | -0.341 .. -0.049 | -0.0055 | 0.009 / 0.0079 / 0.94 | nan | 1 | 0.871 | 12/16 | -0.123 | -0.267 | False | -3.2 / -2.6 |  |
| MES | 60 | h1 | +0.010 | -0.031 .. +0.050 | +0.0026 | 0.64 / 0.64 / 0.98 | nan |  |  | 7/16 | -0.019 | +0.038 |  | +0.5 / +0.5 |  |
| MES | 60 | h2 | -0.025 | -0.082 .. +0.032 | -0.0047 | 0.39 / 0.39 / 0.99 | nan |  |  | 11/16 | -0.030 | -0.019 |  | -0.8 / -0.9 |  |
| MES | 60 | h4 | +0.029 | -0.042 .. +0.099 | +0.0039 | 0.42 / 0.43 / 0.98 | nan |  |  | 7/16 | +0.030 | +0.028 |  | +0.7 / +0.8 | 0.102 |
| MES | 60 | h8 * | +0.053 | -0.018 .. +0.125 | +0.0052 | 0.14 / 0.17 / 1 | nan | 1 | 1 | 11/16 | +0.061 | +0.045 | False | +1.0 / +1.5 |  |
| MES | 60 | h16 | +0.011 | -0.037 .. +0.058 | +0.0008 | 0.66 / 0.68 / 0.93 | nan |  |  | 11/16 | +0.007 | +0.014 |  | +0.2 / +0.4 |  |
| MES | 60 | eod | -0.007 | -0.049 .. +0.036 | -0.0005 | 0.76 / 0.76 / 0.9 | nan |  |  | 7/16 | -0.014 | +0.000 |  | -0.1 / -0.3 |  |
| MNQ | 5 | h1 | -0.003 | -0.015 .. +0.008 | -0.0010 | 0.56 / 0.59 / 0.97 | nan |  |  | 9/16 | -0.003 | -0.004 |  | -0.5 / -0.6 |  |
| MNQ | 5 | h2 | -0.026 | -0.070 .. +0.019 | -0.0046 | 0.26 / 0.25 / 0.94 | nan |  |  | 9/16 | -0.005 | -0.047 |  | -1.7 / -1.1 |  |
| MNQ | 5 | h4 * | -0.041 | -0.109 .. +0.027 | -0.0048 | 0.24 / 0.23 / 0.96 | nan | 1 | 1 | 8/16 | -0.015 | -0.067 | False | -2.0 / -1.2 | 0.098 |
| MNQ | 5 | h8 | -0.055 | -0.149 .. +0.040 | -0.0043 | 0.26 / 0.27 / 0.95 | nan |  |  | 11/16 | -0.044 | -0.065 |  | -2.0 / -1.1 |  |
| MNQ | 5 | h16 | -0.048 | -0.211 .. +0.115 | -0.0027 | 0.56 / 0.58 / 0.98 | nan |  |  | 8/16 | -0.082 | -0.015 |  | -1.5 / -0.6 |  |
| MNQ | 5 | eod | -0.031 | -0.303 .. +0.242 | -0.0004 | 0.83 / 0.83 / 0.8 | nan |  |  | 9/16 | -0.349 | +0.285 |  | -0.4 / -0.2 |  |
| MNQ | 15 | h1 | +0.013 | -0.019 .. +0.044 | +0.0033 | 0.42 / 0.44 / 0.93 | nan |  |  | 9/16 | -0.000 | +0.026 |  | +0.7 / +0.8 |  |
| MNQ | 15 | h2 | -0.005 | -0.055 .. +0.044 | -0.0008 | 0.83 / 0.84 / 0.97 | nan |  |  | 8/16 | -0.013 | +0.003 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h4 | +0.011 | -0.093 .. +0.114 | +0.0010 | 0.84 / 0.85 / 0.95 | nan |  |  | 8/16 | -0.030 | +0.051 |  | +0.2 / +0.2 | 0.149 |
| MNQ | 15 | h8 | +0.062 | -0.136 .. +0.259 | +0.0043 | 0.54 / 0.53 / 0.91 | nan |  |  | 8/16 | -0.040 | +0.162 |  | +1.3 / +0.6 |  |
| MNQ | 15 | h16 | +0.032 | -0.133 .. +0.196 | +0.0018 | 0.71 / 0.71 / 0.95 | nan |  |  | 9/16 | +0.018 | +0.045 |  | +0.7 / +0.4 |  |
| MNQ | 15 | eod * | -0.123 | -0.268 .. +0.021 | -0.0024 | 0.094 / 0.089 / 1 | nan | 1 | 1 | 10/16 | -0.260 | +0.012 | False | -1.4 / -1.7 |  |
| MNQ | 60 | h1 | +0.005 | -0.042 .. +0.053 | +0.0014 | 0.82 / 0.83 / 0.99 | nan |  |  | 6/16 | -0.015 | +0.026 |  | +0.2 / +0.2 |  |
| MNQ | 60 | h2 | -0.049 | -0.116 .. +0.018 | -0.0087 | 0.15 / 0.16 / 0.98 | nan |  |  | 10/16 | -0.055 | -0.043 |  | -1.2 / -1.4 |  |
| MNQ | 60 | h4 | -0.001 | -0.080 .. +0.077 | -0.0002 | 0.98 / 0.98 / 0.99 | nan |  |  | 9/16 | -0.006 | +0.004 |  | -0.0 / -0.0 | 0.114 |
| MNQ | 60 | h8 | +0.036 | -0.045 .. +0.116 | +0.0033 | 0.39 / 0.41 / 1 | nan |  |  | 10/16 | +0.034 | +0.037 |  | +0.6 / +0.9 |  |
| MNQ | 60 | h16 | -0.041 | -0.093 .. +0.011 | -0.0029 | 0.12 / 0.13 / 0.93 | nan |  |  | 10/16 | -0.058 | -0.025 |  | -0.7 / -1.6 |  |
| MNQ | 60 | eod * | -0.067 | -0.114 .. -0.020 | -0.0045 | 0.0049 / 0.0066 / 0.9 | nan | 0.932 | 0.676 | 13/16 | -0.089 | -0.045 | False | -1.1 / -2.8 |  |
| MYM | 5 | h1 | -0.004 | -0.023 .. +0.014 | -0.0012 | 0.64 / 0.67 / 0.95 | nan |  |  | 5/8 | n/a | -0.004 |  | -0.4 / -0.5 |  |
| MYM | 5 | h2 | -0.057 | -0.152 .. +0.038 | -0.0091 | 0.24 / 0.25 / 0.87 | nan |  |  | 3/8 | n/a | -0.057 |  | -2.2 / -1.2 |  |
| MYM | 5 | h4 * | -0.138 | -0.355 .. +0.079 | -0.0137 | 0.21 / 0.22 / 0.83 | nan | 1 | 1 | 4/8 | n/a | -0.138 | False | -3.2 / -1.2 | 0.314 |
| MYM | 5 | h8 | -0.182 | -0.472 .. +0.109 | -0.0129 | 0.22 / 0.24 / 0.87 | nan |  |  | 4/8 | n/a | -0.182 |  | -3.7 / -1.2 |  |
| MYM | 5 | h16 | -0.100 | -0.354 .. +0.155 | -0.0055 | 0.44 / 0.47 / 0.99 | nan |  |  | 3/8 | n/a | -0.100 |  | -2.4 / -0.8 |  |
| MYM | 5 | eod | -0.164 | -0.538 .. +0.211 | -0.0020 | 0.39 / 0.39 / 0.9 | nan |  |  | 5/8 | n/a | -0.164 |  | -1.6 / -0.9 |  |
| MYM | 15 | h1 | +0.012 | -0.023 .. +0.047 | +0.0032 | 0.5 / 0.54 / 0.93 | nan |  |  | 6/8 | n/a | +0.012 |  | +0.6 / +0.7 |  |
| MYM | 15 | h2 | -0.032 | -0.132 .. +0.067 | -0.0048 | 0.53 / 0.55 / 0.99 | nan |  |  | 3/8 | n/a | -0.032 |  | -0.7 / -0.6 |  |
| MYM | 15 | h4 | -0.050 | -0.195 .. +0.096 | -0.0044 | 0.51 / 0.53 / 0.96 | nan |  |  | 3/8 | n/a | -0.050 |  | -0.7 / -0.7 | 0.211 |
| MYM | 15 | h8 | -0.035 | -0.209 .. +0.139 | -0.0024 | 0.69 / 0.7 / 0.89 | nan |  |  | 4/8 | n/a | -0.035 |  | -0.7 / -0.4 |  |
| MYM | 15 | h16 | -0.162 | -0.463 .. +0.139 | -0.0079 | 0.29 / 0.3 / 0.9 | nan |  |  | 4/8 | n/a | -0.162 |  | -2.0 / -1.1 |  |
| MYM | 15 | eod * | -0.240 | -0.454 .. -0.026 | -0.0049 | 0.028 / 0.026 / 0.96 | nan | 1 | 0.994 | 5/8 | n/a | -0.240 | False | -2.0 / -2.2 |  |
| MYM | 60 | h1 | +0.036 | -0.031 .. +0.104 | +0.0094 | 0.29 / 0.29 / 0.97 | nan |  |  | 5/8 | n/a | +0.036 |  | +1.0 / +1.1 |  |
| MYM | 60 | h2 | -0.014 | -0.105 .. +0.077 | -0.0025 | 0.76 / 0.76 / 1 | nan |  |  | 3/8 | n/a | -0.014 |  | -0.3 / -0.3 |  |
| MYM | 60 | h4 | +0.028 | -0.080 .. +0.135 | +0.0036 | 0.62 / 0.61 / 0.98 | nan |  |  | 5/8 | n/a | +0.028 |  | +0.4 / +0.5 | 0.156 |
| MYM | 60 | h8 | +0.062 | -0.046 .. +0.169 | +0.0058 | 0.26 / 0.27 / 0.98 | nan |  |  | 6/8 | n/a | +0.062 |  | +0.8 / +1.1 |  |
| MYM | 60 | h16 * | +0.062 | -0.009 .. +0.133 | +0.0045 | 0.085 / 0.093 / 0.99 | nan | 1 | 1 | 6/8 | n/a | +0.062 | False | +0.8 / +1.7 |  |
| MYM | 60 | eod | +0.054 | -0.011 .. +0.119 | +0.0037 | 0.1 / 0.11 / 1 | nan |  |  | 6/8 | n/a | +0.054 |  | +0.7 / +1.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.112 | +0.104 .. +0.121 | +22.5% | +0.237 | 1.5e-155 | 3.09e-152 | 16/16 |
| MES | 5 | h2 | +0.218 | +0.198 .. +0.238 | +31.1% | +0.438 | 8.1e-101 |  | 16/16 |
| MES | 5 | h4 | +0.437 | +0.390 .. +0.483 | +43.8% | +0.868 | 4.4e-75 |  | 16/16 |
| MES | 5 | h8 | +0.858 | +0.762 .. +0.953 | +59.6% | +1.694 | 1.7e-69 |  | 16/16 |
| MES | 5 | h16 | +1.623 | +1.502 .. +1.745 | +77.4% | +3.281 | 4.2e-151 |  | 16/16 |
| MES | 5 | eod | +0.748 | +0.531 .. +0.966 | +7.5% | +1.323 | 1.6e-11 |  | 13/16 |
| MES | 15 | h1 * | +0.265 | +0.247 .. +0.282 | +51.9% | +0.540 | 6.6e-197 | 1.57e-193 | 16/16 |
| MES | 15 | h2 | +0.513 | +0.466 .. +0.560 | +70.3% | +1.020 | 1.8e-101 |  | 16/16 |
| MES | 15 | h4 | +0.918 | +0.820 .. +1.017 | +87.2% | +1.845 | 3e-75 |  | 16/16 |
| MES | 15 | h8 | +1.559 | +1.434 .. +1.685 | +101.4% | +3.166 | 7.8e-131 |  | 16/16 |
| MES | 15 | h16 | +1.649 | +1.518 .. +1.781 | +72.2% | +3.360 | 4.7e-133 |  | 16/16 |
| MES | 15 | eod | -0.099 | -0.241 .. +0.042 | -1.8% | -0.329 | 0.17 |  | 12/16 |
| MES | 60 | h1 | +0.456 | +0.426 .. +0.486 | +88.9% | +0.930 | 2.6e-191 |  | 16/16 |
| MES | 60 | h2 * | +0.717 | +0.676 .. +0.758 | +97.2% | +1.420 | 5.9e-258 | 1.75e-254 | 16/16 |
| MES | 60 | h4 | +0.771 | +0.721 .. +0.822 | +72.9% | +1.541 | 6.2e-197 |  | 16/16 |
| MES | 60 | h8 | +0.962 | +0.905 .. +1.020 | +63.8% | +1.789 | 3e-237 |  | 16/16 |
| MES | 60 | h16 | +0.436 | +0.393 .. +0.480 | +21.2% | +0.742 | 9.8e-85 |  | 16/16 |
| MES | 60 | eod | +0.339 | +0.298 .. +0.380 | +15.7% | +0.562 | 1.5e-59 |  | 16/16 |
| MNQ | 5 | h1 | +0.146 | +0.130 .. +0.163 | +27.4% | +0.305 | 8.8e-66 |  | 16/16 |
| MNQ | 5 | h2 | +0.301 | +0.241 .. +0.361 | +39.1% | +0.592 | 6.9e-23 |  | 16/16 |
| MNQ | 5 | h4 | +0.604 | +0.508 .. +0.701 | +54.5% | +1.203 | 1.7e-34 |  | 16/16 |
| MNQ | 5 | h8 | +1.233 | +1.073 .. +1.392 | +76.1% | +2.435 | 7.6e-52 |  | 16/16 |
| MNQ | 5 | h16 * | +2.481 | +2.303 .. +2.660 | +103.4% | +4.959 | 1e-163 | 2.08e-160 | 16/16 |
| MNQ | 5 | eod | +1.059 | +0.746 .. +1.373 | +8.4% | +1.932 | 3.3e-11 |  | 12/16 |
| MNQ | 15 | h1 | +0.371 | +0.336 .. +0.405 | +69.4% | +0.731 | 3.6e-97 |  | 16/16 |
| MNQ | 15 | h2 | +0.736 | +0.625 .. +0.848 | +95.1% | +1.433 | 1.5e-38 |  | 16/16 |
| MNQ | 15 | h4 | +1.374 | +1.185 .. +1.563 | +121.2% | +2.686 | 3.6e-46 |  | 16/16 |
| MNQ | 15 | h8 | +2.284 | +2.123 .. +2.445 | +136.2% | +4.531 | 2.5e-169 |  | 16/16 |
| MNQ | 15 | h16 * | +2.302 | +2.159 .. +2.445 | +91.1% | +4.665 | 4.3e-219 | 1.09e-215 | 16/16 |
| MNQ | 15 | eod | -0.042 | -0.183 .. +0.099 | -0.7% | -0.260 | 0.56 |  | 11/16 |
| MNQ | 60 | h1 | +0.679 | +0.638 .. +0.721 | +128.5% | +1.342 | 1.9e-227 |  | 16/16 |
| MNQ | 60 | h2 | +0.994 | +0.937 .. +1.051 | +129.7% | +1.911 | 4.4e-253 |  | 16/16 |
| MNQ | 60 | h4 | +1.041 | +0.976 .. +1.106 | +94.2% | +2.021 | 2.1e-217 |  | 16/16 |
| MNQ | 60 | h8 * | +1.165 | +1.101 .. +1.229 | +73.5% | +2.156 | 4.1e-278 | 1.35e-274 | 16/16 |
| MNQ | 60 | h16 | +0.616 | +0.565 .. +0.666 | +28.1% | +1.053 | 9.4e-127 |  | 16/16 |
| MNQ | 60 | eod | +0.525 | +0.477 .. +0.573 | +22.8% | +0.884 | 1.9e-101 |  | 16/16 |
| MYM | 5 | h1 | +0.174 | +0.148 .. +0.201 | +32.7% | +0.333 | 2.1e-37 |  | 8/8 |
| MYM | 5 | h2 | +0.363 | +0.262 .. +0.464 | +47.7% | +0.663 | 2e-12 |  | 8/8 |
| MYM | 5 | h4 | +0.709 | +0.488 .. +0.931 | +64.7% | +1.360 | 3.5e-10 |  | 8/8 |
| MYM | 5 | h8 | +1.319 | +1.003 .. +1.636 | +82.9% | +2.571 | 5.9e-16 |  | 8/8 |
| MYM | 5 | h16 * | +2.286 | +2.065 .. +2.507 | +97.9% | +4.662 | 4.7e-90 | 6.19e-87 | 8/8 |
| MYM | 5 | eod | +1.280 | +0.767 .. +1.793 | +10.9% | +2.292 | 9.9e-07 |  | 6/8 |
| MYM | 15 | h1 | +0.367 | +0.322 .. +0.412 | +69.1% | +0.714 | 1.3e-57 |  | 8/8 |
| MYM | 15 | h2 | +0.736 | +0.580 .. +0.892 | +96.1% | +1.422 | 2.6e-20 |  | 8/8 |
| MYM | 15 | h4 | +1.273 | +1.045 .. +1.501 | +114.3% | +2.552 | 6.7e-28 |  | 8/8 |
| MYM | 15 | h8 * | +1.934 | +1.782 .. +2.086 | +117.9% | +3.982 | 3.7e-137 | 6.83e-134 | 8/8 |
| MYM | 15 | h16 | +2.036 | +1.796 .. +2.276 | +82.7% | +4.172 | 3.4e-61 |  | 8/8 |
| MYM | 15 | eod | -0.059 | -0.263 .. +0.145 | -1.0% | -0.235 | 0.57 |  | 5/8 |
| MYM | 60 | h1 | +0.603 | +0.543 .. +0.663 | +115.1% | +1.233 | 2.7e-87 |  | 8/8 |
| MYM | 60 | h2 | +0.826 | +0.759 .. +0.893 | +109.3% | +1.635 | 1.7e-128 |  | 8/8 |
| MYM | 60 | h4 | +0.883 | +0.808 .. +0.958 | +81.7% | +1.759 | 3.9e-118 |  | 8/8 |
| MYM | 60 | h8 * | +1.046 | +0.971 .. +1.121 | +67.6% | +1.934 | 1.1e-147 | 2.22e-144 | 8/8 |
| MYM | 60 | h16 | +0.492 | +0.437 .. +0.548 | +23.2% | +0.842 | 1.9e-58 |  | 8/8 |
| MYM | 60 | eod | +0.395 | +0.342 .. +0.449 | +17.8% | +0.669 | 1.4e-42 |  | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.80 pts | -1.48 .. -0.11 | 0.022 |
| MES | 15 | -1.37 pts | -2.27 .. -0.47 | 0.004 |
| MES | 60 | -1.14 pts | -2.71 .. +0.44 | 0.16 |
| MNQ | 5 | -1.10 pts | -1.76 .. -0.44 | 0.0011 |
| MNQ | 15 | -1.41 pts | -2.33 .. -0.50 | 0.0028 |
| MNQ | 60 | -1.84 pts | -3.36 .. -0.32 | 0.017 |
| MYM | 5 | -0.96 pts | -2.02 .. +0.11 | 0.077 |
| MYM | 15 | -0.94 pts | -2.37 .. +0.50 | 0.2 |
| MYM | 60 | -0.11 pts | -2.19 .. +1.97 | 0.92 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 69744 | +0.004 | 0.347 | +0.05 | -3.45 | -3.48 | -3.42 | -3.46 |
| MES | 5 | h2 | event | short | 69744 | +0.000 | 0.347 | -0.09 | -3.59 | -3.53 | -3.65 | -3.56 |
| MES | 5 | h4 | event | short | 69744 | +0.012 | 0.347 | -0.08 | -3.58 | -3.52 | -3.64 | -3.52 |
| MES | 5 | h8 | event | short | 69744 | +0.028 | 0.347 | -0.13 | -3.63 | -3.48 | -3.78 | -3.49 |
| MES | 5 | h16 | event | short | 69744 | -0.011 | 0.347 | -0.54 | -4.04 | -3.69 | -4.39 | -3.76 |
| MES | 5 | eod | event | short | 69744 | -0.332 | 0.347 | -3.66 | -7.16 | -6.18 | -8.13 | -6.54 |
| MES | 15 | h1 | event | long | 23249 | +0.005 | 0.215 | +0.06 | -3.44 | -3.51 | -3.36 | -3.47 |
| MES | 15 | h2 | event | short | 23249 | +0.002 | 0.215 | -0.21 | -3.71 | -3.44 | -3.98 | -3.63 |
| MES | 15 | h4 | event | short | 23249 | +0.010 | 0.215 | -0.37 | -3.87 | -3.50 | -4.24 | -3.70 |
| MES | 15 | h8 | event | short | 23249 | -0.011 | 0.215 | -0.70 | -4.20 | -3.84 | -4.57 | -3.87 |
| MES | 15 | h16 | event | short | 23249 | -0.074 | 0.215 | -1.82 | -5.32 | -4.71 | -5.92 | -4.73 |
| MES | 15 | eod | event | short | 23249 | -0.140 | 0.215 | -3.56 | -7.06 | -6.13 | -8.00 | -4.71 |
| MES | 60 | h1 | event | long | 3815 | +0.021 | 0.105 | +0.74 | -2.76 | -3.41 | -2.10 | -2.98 |
| MES | 60 | h2 | event | short | 3815 | +0.001 | 0.105 | -0.04 | -3.54 | -3.71 | -3.36 | -3.07 |
| MES | 60 | h4 | event | long | 3815 | +0.074 | 0.105 | +2.23 | -1.27 | -1.92 | -0.63 | -2.29 |
| MES | 60 | h8 | event | long | 3815 | +0.133 | 0.105 | +3.77 | +0.27 | -0.86 | +1.39 | -1.58 |
| MES | 60 | h16 | event | long | 3815 | +0.133 | 0.105 | +3.77 | +0.27 | -0.86 | +1.39 | -2.45 |
| MES | 60 | eod | event | short | 3815 | -0.133 | 0.105 | -3.77 | -7.27 | -6.14 | -8.39 | -4.06 |
| MNQ | 5 | h1 | event | short | 69727 | -0.000 | 0.144 | -0.01 | -2.01 | -2.02 | -2.00 | -1.99 |
| MNQ | 5 | h2 | event | short | 69727 | +0.017 | 0.144 | -0.05 | -2.05 | -2.05 | -2.04 | -2.03 |
| MNQ | 5 | h4 | event | short | 69727 | +0.024 | 0.144 | -0.04 | -2.04 | -2.09 | -1.99 | -2.00 |
| MNQ | 5 | h8 | event | short | 69727 | +0.023 | 0.144 | -0.04 | -2.04 | -2.06 | -2.03 | -1.98 |
| MNQ | 5 | h16 | event | short | 69727 | -0.008 | 0.144 | -0.26 | -2.26 | -2.04 | -2.48 | -2.13 |
| MNQ | 5 | eod | event | short | 69727 | -0.464 | 0.144 | -4.89 | -6.89 | -4.24 | -9.56 | -7.51 |
| MNQ | 15 | h1 | event | long | 23243 | +0.017 | 0.089 | +0.03 | -1.97 | -1.92 | -2.02 | -2.04 |
| MNQ | 15 | h2 | event | short | 23243 | -0.004 | 0.089 | -0.18 | -2.18 | -2.06 | -2.30 | -2.09 |
| MNQ | 15 | h4 | event | long | 23243 | +0.028 | 0.089 | +0.24 | -1.76 | -2.02 | -1.49 | -1.92 |
| MNQ | 15 | h8 | event | long | 23243 | +0.091 | 0.089 | +0.39 | -1.61 | -1.92 | -1.29 | -1.90 |
| MNQ | 15 | h16 | event | long | 23243 | +0.100 | 0.089 | +1.77 | -0.23 | -1.20 | +0.74 | -0.56 |
| MNQ | 15 | eod | event | short | 23243 | -0.275 | 0.089 | -4.95 | -6.95 | -4.21 | -9.68 | -4.04 |
| MNQ | 60 | h1 | event | long | 3814 | +0.022 | 0.042 | +0.81 | -1.19 | -2.13 | -0.25 | -1.63 |
| MNQ | 60 | h2 | event | short | 3814 | +0.014 | 0.042 | +1.31 | -0.69 | -1.71 | +0.33 | +0.19 |
| MNQ | 60 | h4 | event | short | 3814 | -0.062 | 0.042 | -1.71 | -3.71 | -2.85 | -4.58 | -1.96 |
| MNQ | 60 | h8 | event | long | 3814 | +0.149 | 0.042 | +4.50 | +2.50 | +0.03 | +4.98 | -0.78 |
| MNQ | 60 | h16 | event | short | 3814 | -0.149 | 0.042 | -4.50 | -6.50 | -4.03 | -8.98 | -1.20 |
| MNQ | 60 | eod | event | short | 3814 | -0.149 | 0.042 | -4.50 | -6.50 | -4.03 | -8.98 | -0.32 |
| MYM | 5 | h1 | event | short | 34788 | +0.002 | 0.186 | -0.08 | -2.08 | +nan | -2.08 | -2.07 |
| MYM | 5 | h2 | event | short | 34788 | +0.048 | 0.186 | -0.11 | -2.11 | +nan | -2.11 | -2.08 |
| MYM | 5 | h4 | event | short | 34788 | +0.117 | 0.186 | -0.07 | -2.07 | +nan | -2.07 | -2.02 |
| MYM | 5 | h8 | event | short | 34788 | +0.145 | 0.186 | -0.18 | -2.18 | +nan | -2.18 | -2.06 |
| MYM | 5 | h16 | event | short | 34788 | +0.050 | 0.186 | -0.45 | -2.45 | +nan | -2.45 | -2.20 |
| MYM | 5 | eod | event | short | 34788 | -0.057 | 0.186 | -3.61 | -5.61 | +nan | -5.61 | -4.92 |
| MYM | 15 | h1 | event | long | 11601 | +0.014 | 0.112 | +0.08 | -1.92 | +nan | -1.92 | -1.96 |
| MYM | 15 | h2 | event | short | 11601 | +0.023 | 0.112 | -0.28 | -2.28 | +nan | -2.28 | -2.21 |
| MYM | 15 | h4 | event | short | 11601 | +0.034 | 0.112 | -0.37 | -2.37 | +nan | -2.37 | -2.25 |
| MYM | 15 | h8 | event | short | 11601 | +0.017 | 0.112 | -0.47 | -2.47 | +nan | -2.47 | -2.39 |
| MYM | 15 | h16 | event | short | 11601 | +0.118 | 0.112 | -1.45 | -3.45 | +nan | -3.45 | -3.36 |
| MYM | 15 | eod | event | short | 11601 | +0.079 | 0.112 | -3.53 | -5.53 | +nan | -5.53 | -4.79 |
| MYM | 60 | h1 | event | long | 1905 | +0.040 | 0.053 | +0.88 | -1.12 | +nan | -1.12 | -1.22 |
| MYM | 60 | h2 | event | short | 1905 | +0.007 | 0.053 | +0.27 | -1.73 | +nan | -1.73 | -1.59 |
| MYM | 60 | h4 | event | long | 1905 | +0.035 | 0.053 | +1.76 | -0.24 | +nan | -0.24 | -0.42 |
| MYM | 60 | h8 | event | long | 1905 | +0.075 | 0.053 | +3.35 | +1.35 | +nan | +1.35 | +0.94 |
| MYM | 60 | h16 | event | long | 1905 | +0.075 | 0.053 | +3.35 | +1.35 | +nan | +1.35 | +0.89 |
| MYM | 60 | eod | event | long | 1905 | +0.075 | 0.053 | +3.35 | +1.35 | +nan | +1.35 | +0.52 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.001 | +0.000 | -0.001 | -0.001 | +0.001 | +0.000 | +0.004 | +0.006 | +0.002 | +0.002 | +0.005 |
| MES | 15 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | -0.000 | +0.000 | +0.000 |
| MES | 60 | +nan | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +nan |
| MNQ | 5 | +0.001 | +0.001 | +0.001 | +0.001 | +0.003 | +0.000 | +0.005 | +0.006 | +0.006 | +0.005 | +0.002 |
| MNQ | 15 | -0.000 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 |
| MNQ | 60 | +nan | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | +nan |
| MYM | 5 | -0.000 | -0.001 | -0.002 | +0.000 | +0.001 | +0.000 | +0.010 | +0.010 | +0.007 | +0.006 | +0.009 |
| MYM | 15 | -0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 |
| MYM | 60 | +nan | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +nan |

## Calibration

- MES 5-min: 1036271 bars, 69744 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 23249 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3815 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 69727 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 23243 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 3814 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 34788 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 11601 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.051); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
