# Impact card: vol_spike_follow

volume > 2x slot average, traded in the bar's colour [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.023 R20 over the next 16 bars (80 min), p=0.66; we would catch an effect of 0.015 R20 or more 80% of the time).
- MES 5-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.078 R20, CONFIRMED, q=2.78e-166, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.57 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.159 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.022 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.029 R20 or more 80% of the time).
- MES 15-min size: the market moves 18% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.094 R20, CONFIRMED, q=2.66e-96, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.57 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.092 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.031 R20 over the next 2 bars (2 h), p=0.55; we would catch an effect of 0.066 R20 or more 80% of the time).
- MES 60-min size: the market moves 24% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.123 R20, CONFIRMED, q=2.13e-28, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.31 at recent bar sizes, 90% range up to $7.28); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (5 min), p=0.53; we would catch an effect of 0.016 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 15% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.078 R20, CONFIRMED, q=1.57e-168, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.50 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.061 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.034 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.088 R20, CONFIRMED, q=1.19e-55, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.38 at recent bar sizes, 90% range up to $3.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.040 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.064 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 22% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.117 R20, CONFIRMED, q=7.23e-26, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.64 at recent bar sizes, 90% range up to $8.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.011 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.024 R20 or more 80% of the time).
- MYM 5-min size: the market moves 16% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.083 R20, CONFIRMED, q=3.08e-88, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.35 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.122 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.022 R20 over the next 2 bars (30 min), p=0.99; we would catch an effect of 0.047 R20 or more 80% of the time).
- MYM 15-min size: the market moves 18% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.098 R20, CONFIRMED, q=8.82e-45, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.52 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.069 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.035 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.095 R20 or more 80% of the time).
- MYM 60-min size: the market moves 25% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.129 R20, CONFIRMED, q=7.78e-16, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.04 at recent bar sizes, 90% range up to $6.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.004 | -0.002 .. +0.009 | +0.0015 | 0.17 / 0.18 / 0.12 | 0.122 |  |  | 10/16 | +0.005 | +0.002 |  | +1.3 / +1.4 |  |
| MES | 5 | h2 | -0.003 | -0.010 .. +0.004 | -0.0010 | 0.36 / 0.37 / 0.38 | 0.377 |  |  | 8/16 | -0.006 | -0.000 |  | -0.9 / -0.9 |  |
| MES | 5 | h4 | -0.008 | -0.018 .. +0.001 | -0.0017 | 0.092 / 0.1 / 0.12 | 0.117 |  |  | 11/16 | -0.011 | -0.006 |  | -1.7 / -1.7 | 0.015 |
| MES | 5 | h8 | -0.014 | -0.027 .. -0.002 | -0.0020 | 0.027 / 0.038 / 0.071 | 0.0719 |  |  | 12/16 | -0.025 | -0.004 |  | -2.1 / -2.2 |  |
| MES | 5 | h16 * | -0.023 | -0.042 .. -0.003 | -0.0022 | 0.026 / 0.029 / 0.056 | 0.0578 | 1 | 0.992 | 12/16 | -0.051 | +0.005 | False | -2.3 / -2.2 |  |
| MES | 5 | eod | -0.018 | -0.132 .. +0.096 | -0.0004 | 0.76 / 0.76 / 0.78 | 0.782 |  |  | 9/16 | +0.001 | -0.037 |  | -0.4 / -0.3 |  |
| MES | 15 | h1 | +0.003 | -0.006 .. +0.011 | +0.0009 | 0.58 / 0.6 / 0.59 | 0.587 |  |  | 7/16 | -0.007 | +0.012 |  | +0.5 / +0.6 |  |
| MES | 15 | h2 | -0.001 | -0.013 .. +0.012 | -0.0002 | 0.92 / 0.92 / 0.92 | 0.922 |  |  | 8/16 | -0.017 | +0.015 |  | -0.1 / -0.1 |  |
| MES | 15 | h4 | -0.007 | -0.026 .. +0.012 | -0.0012 | 0.48 / 0.49 / 0.54 | 0.532 |  |  | 9/16 | -0.035 | +0.021 |  | -0.7 / -0.7 | 0.029 |
| MES | 15 | h8 | -0.018 | -0.046 .. +0.011 | -0.0021 | 0.23 / 0.22 / 0.28 | 0.272 |  |  | 9/16 | -0.048 | +0.013 |  | -1.3 / -1.2 |  |
| MES | 15 | h16 * | -0.022 | -0.065 .. +0.021 | -0.0018 | 0.31 / 0.29 / 0.37 | 0.362 | 1 | 1 | 9/16 | -0.044 | -0.001 | False | -1.1 / -1.0 |  |
| MES | 15 | eod | -0.013 | -0.121 .. +0.095 | -0.0005 | 0.82 / 0.81 / 0.85 | 0.842 |  |  | 8/16 | -0.014 | -0.012 |  | -0.3 / -0.2 |  |
| MES | 60 | h1 | +0.016 | -0.010 .. +0.042 | +0.0052 | 0.22 / 0.21 / 0.11 | 0.115 |  |  | 7/16 | +0.013 | +0.020 |  | +1.3 / +1.2 |  |
| MES | 60 | h2 * | +0.031 | -0.005 .. +0.066 | +0.0069 | 0.092 / 0.079 / 0.05 | 0.0498 | 1 | 1 | 8/16 | +0.015 | +0.046 | False | +1.7 / +1.7 |  |
| MES | 60 | h4 | +0.025 | -0.028 .. +0.078 | +0.0040 | 0.36 / 0.34 / 0.27 | 0.275 |  |  | 12/16 | +0.028 | +0.022 |  | +1.0 / +0.9 | 0.066 |
| MES | 60 | h8 | +0.040 | -0.028 .. +0.109 | +0.0046 | 0.25 / 0.23 / 0.21 | 0.213 |  |  | 11/16 | +0.049 | +0.031 |  | +1.3 / +1.2 |  |
| MES | 60 | h16 | +0.051 | -0.044 .. +0.145 | +0.0045 | 0.29 / 0.28 / 0.26 | 0.258 |  |  | 8/16 | +0.099 | +0.002 |  | +1.2 / +1.1 |  |
| MES | 60 | eod | +0.041 | -0.061 .. +0.142 | +0.0034 | 0.43 / 0.42 / 0.39 | 0.391 |  |  | 9/16 | +0.094 | -0.013 |  | +0.9 / +0.8 |  |
| MNQ | 5 | h1 * | +0.005 | -0.001 .. +0.010 | +0.0016 | 0.089 / 0.086 / 0.092 | 0.0956 | 1 | 1 | 11/16 | +0.004 | +0.006 | False | +1.7 / +1.7 |  |
| MNQ | 5 | h2 | +0.001 | -0.006 .. +0.009 | +0.0003 | 0.72 / 0.72 / 0.74 | 0.737 |  |  | 11/16 | -0.003 | +0.006 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h4 | +0.006 | -0.005 .. +0.017 | +0.0009 | 0.26 / 0.26 / 0.38 | 0.359 |  |  | 10/16 | +0.010 | +0.003 |  | +1.2 / +1.1 | 0.016 |
| MNQ | 5 | h8 | +0.003 | -0.012 .. +0.018 | +0.0003 | 0.71 / 0.71 / 0.79 | 0.779 |  |  | 6/16 | +0.006 | -0.000 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h16 | -0.021 | -0.043 .. +0.002 | -0.0015 | 0.07 / 0.072 / 0.21 | 0.205 |  |  | 12/16 | -0.031 | -0.010 |  | -1.9 / -1.8 |  |
| MNQ | 5 | eod | -0.048 | -0.187 .. +0.091 | -0.0007 | 0.5 / 0.5 / 0.59 | 0.597 |  |  | 10/16 | -0.079 | -0.017 |  | -0.8 / -0.7 |  |
| MNQ | 15 | h1 * | +0.007 | -0.003 .. +0.016 | +0.0019 | 0.16 / 0.18 / 0.27 | 0.216 | 1 | 0.996 | 10/16 | -0.004 | +0.017 | False | +1.3 / +1.4 |  |
| MNQ | 15 | h2 | -0.001 | -0.015 .. +0.013 | -0.0003 | 0.84 / 0.84 / 0.89 | 0.86 |  |  | 7/16 | -0.016 | +0.013 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h4 | -0.021 | -0.041 .. -0.002 | -0.0022 | 0.032 / 0.04 / 0.24 | 0.197 |  |  | 9/16 | -0.040 | -0.002 |  | -2.1 / -2.1 | 0.034 |
| MNQ | 15 | h8 | -0.032 | -0.062 .. -0.001 | -0.0025 | 0.042 / 0.046 / 0.17 | 0.156 |  |  | 9/16 | -0.057 | -0.007 |  | -2.1 / -2.0 |  |
| MNQ | 15 | h16 | -0.038 | -0.086 .. +0.011 | -0.0024 | 0.13 / 0.12 / 0.22 | 0.209 |  |  | 8/16 | -0.080 | +0.005 |  | -1.7 / -1.5 |  |
| MNQ | 15 | eod | +0.014 | -0.106 .. +0.135 | +0.0003 | 0.81 / 0.82 / 0.88 | 0.872 |  |  | 10/16 | +0.047 | -0.018 |  | +0.3 / +0.2 |  |
| MNQ | 60 | h1 | +0.001 | -0.025 .. +0.026 | +0.0001 | 0.97 / 0.97 / 0.96 | 0.96 |  |  | 7/16 | +0.001 | +0.001 |  | +0.0 / +0.0 |  |
| MNQ | 60 | h2 | -0.005 | -0.040 .. +0.030 | -0.0011 | 0.78 / 0.78 / 0.76 | 0.765 |  |  | 11/16 | -0.007 | -0.003 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h4 | +0.004 | -0.048 .. +0.055 | +0.0005 | 0.88 / 0.88 / 0.87 | 0.871 |  |  | 8/16 | -0.008 | +0.015 |  | +0.2 / +0.1 | 0.064 |
| MNQ | 60 | h8 | +0.013 | -0.057 .. +0.082 | +0.0013 | 0.72 / 0.71 / 0.7 | 0.709 |  |  | 10/16 | +0.019 | +0.006 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h16 | +0.035 | -0.058 .. +0.129 | +0.0029 | 0.46 / 0.45 / 0.45 | 0.454 |  |  | 9/16 | +0.097 | -0.026 |  | +0.8 / +0.7 |  |
| MNQ | 60 | eod * | +0.040 | -0.063 .. +0.142 | +0.0031 | 0.45 / 0.44 / 0.43 | 0.429 | 1 | 1 | 8/16 | +0.103 | -0.024 | False | +0.8 / +0.8 |  |
| MYM | 5 | h1 | +0.001 | -0.007 .. +0.009 | +0.0002 | 0.85 / 0.85 / 0.82 | 0.807 |  |  | 4/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 5 | h2 | -0.003 | -0.014 .. +0.009 | -0.0005 | 0.65 / 0.66 / 0.76 | 0.732 |  |  | 4/8 | n/a | -0.003 |  | -0.5 / -0.4 |  |
| MYM | 5 | h4 | -0.006 | -0.020 .. +0.009 | -0.0007 | 0.45 / 0.44 / 0.7 | 0.651 |  |  | 5/8 | n/a | -0.006 |  | -0.7 / -0.8 | 0.024 |
| MYM | 5 | h8 | -0.002 | -0.023 .. +0.020 | -0.0002 | 0.88 / 0.88 / 0.93 | 0.924 |  |  | 3/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 5 | h16 * | +0.011 | -0.020 .. +0.042 | +0.0007 | 0.5 / 0.51 / 0.65 | 0.633 | 1 | 1 | 4/8 | n/a | +0.011 | False | +0.7 / +0.7 |  |
| MYM | 5 | eod | -0.004 | -0.179 .. +0.172 | +0.0001 | 0.97 / 0.97 / 0.97 | 0.972 |  |  | 5/8 | n/a | -0.004 |  | -0.1 / -0.0 |  |
| MYM | 15 | h1 | +0.010 | -0.005 .. +0.024 | +0.0028 | 0.19 / 0.19 / 0.22 | 0.212 |  |  | 4/8 | n/a | +0.010 |  | +1.3 / +1.3 |  |
| MYM | 15 | h2 * | +0.022 | +0.001 .. +0.043 | +0.0036 | 0.037 / 0.03 / 0.13 | 0.127 | 1 | 0.949 | 5/8 | n/a | +0.022 | False | +2.2 / +2.1 |  |
| MYM | 15 | h4 | +0.031 | +0.006 .. +0.056 | +0.0030 | 0.017 / 0.026 / 0.26 | 0.211 |  |  | 7/8 | n/a | +0.031 |  | +2.1 / +2.4 | 0.047 |
| MYM | 15 | h8 | +0.019 | -0.018 .. +0.057 | +0.0015 | 0.31 / 0.32 / 0.59 | 0.506 |  |  | 5/8 | n/a | +0.019 |  | +0.9 / +1.0 |  |
| MYM | 15 | h16 | +0.006 | -0.054 .. +0.065 | +0.0003 | 0.85 / 0.85 / 0.92 | 0.899 |  |  | 5/8 | n/a | +0.006 |  | +0.2 / +0.2 |  |
| MYM | 15 | eod | -0.052 | -0.206 .. +0.103 | -0.0011 | 0.51 / 0.52 / 0.69 | 0.66 |  |  | 3/8 | n/a | -0.052 |  | -0.7 / -0.7 |  |
| MYM | 60 | h1 | +0.023 | -0.015 .. +0.060 | +0.0067 | 0.24 / 0.22 / 0.16 | 0.156 |  |  | 6/8 | n/a | +0.023 |  | +1.2 / +1.2 |  |
| MYM | 60 | h2 * | +0.035 | -0.018 .. +0.088 | +0.0074 | 0.2 / 0.2 / 0.14 | 0.136 | 1 | 1 | 6/8 | n/a | +0.035 | False | +1.3 / +1.3 |  |
| MYM | 60 | h4 | +0.000 | -0.072 .. +0.073 | +0.0000 | 0.99 / 0.99 / 1 | 0.996 |  |  | 3/8 | n/a | +0.000 |  | +0.0 / +0.0 | 0.095 |
| MYM | 60 | h8 | +0.007 | -0.099 .. +0.113 | +0.0009 | 0.89 / 0.89 / 0.88 | 0.878 |  |  | 4/8 | n/a | +0.007 |  | +0.1 / +0.1 |  |
| MYM | 60 | h16 | +0.003 | -0.158 .. +0.165 | +0.0004 | 0.97 / 0.97 / 0.96 | 0.956 |  |  | 4/8 | n/a | +0.003 |  | +0.1 / +0.0 |  |
| MYM | 60 | eod | +0.016 | -0.155 .. +0.188 | +0.0014 | 0.85 / 0.85 / 0.8 | 0.8 |  |  | 4/8 | n/a | +0.016 |  | +0.2 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.078 | +0.072 .. +0.083 | +15.6% | +0.164 | 1.3e-169 | 2.78e-166 | 16/16 |
| MES | 5 | h2 | +0.089 | +0.081 .. +0.096 | +12.6% | +0.189 | 7.9e-119 |  | 16/16 |
| MES | 5 | h4 | +0.091 | +0.080 .. +0.103 | +9.1% | +0.207 | 4e-57 |  | 16/16 |
| MES | 5 | h8 | +0.086 | +0.068 .. +0.104 | +6.0% | +0.197 | 6.9e-21 |  | 16/16 |
| MES | 5 | h16 | +0.051 | +0.023 .. +0.079 | +2.4% | +0.128 | 0.00039 |  | 14/16 |
| MES | 5 | eod | -0.571 | -0.892 .. -0.249 | -5.7% | -1.134 | 0.011 |  | 12/16 |
| MES | 15 | h1 * | +0.094 | +0.086 .. +0.103 | +18.5% | +0.208 | 1.9e-99 | 2.66e-96 | 16/16 |
| MES | 15 | h2 | +0.107 | +0.094 .. +0.121 | +14.7% | +0.249 | 1.7e-52 |  | 16/16 |
| MES | 15 | h4 | +0.117 | +0.097 .. +0.138 | +11.2% | +0.272 | 2.5e-29 |  | 16/16 |
| MES | 15 | h8 | +0.134 | +0.100 .. +0.169 | +8.7% | +0.270 | 5.3e-14 |  | 16/16 |
| MES | 15 | h16 | +0.135 | +0.077 .. +0.194 | +5.9% | +0.259 | 5.9e-06 |  | 15/16 |
| MES | 15 | eod | +0.069 | -0.148 .. +0.287 | +1.3% | +0.014 | 0.53 |  | 10/16 |
| MES | 60 | h1 * | +0.123 | +0.102 .. +0.144 | +24.0% | +0.268 | 2.9e-31 | 2.13e-28 | 16/16 |
| MES | 60 | h2 | +0.148 | +0.116 .. +0.181 | +20.1% | +0.313 | 1.9e-18 |  | 16/16 |
| MES | 60 | h4 | +0.193 | +0.141 .. +0.246 | +18.2% | +0.352 | 6.9e-13 |  | 16/16 |
| MES | 60 | h8 | +0.203 | +0.139 .. +0.266 | +13.4% | +0.374 | 4.4e-10 |  | 16/16 |
| MES | 60 | h16 | +0.244 | +0.135 .. +0.352 | +11.8% | +0.411 | 1.1e-05 |  | 14/16 |
| MES | 60 | eod | +0.245 | +0.118 .. +0.372 | +11.3% | +0.431 | 0.00016 |  | 13/16 |
| MNQ | 5 | h1 * | +0.078 | +0.072 .. +0.083 | +14.5% | +0.171 | 7.2e-172 | 1.57e-168 | 16/16 |
| MNQ | 5 | h2 | +0.087 | +0.079 .. +0.096 | +11.4% | +0.190 | 3.8e-93 |  | 16/16 |
| MNQ | 5 | h4 | +0.085 | +0.071 .. +0.100 | +7.7% | +0.193 | 2e-30 |  | 16/16 |
| MNQ | 5 | h8 | +0.067 | +0.040 .. +0.094 | +4.1% | +0.162 | 1.3e-06 |  | 15/16 |
| MNQ | 5 | h16 | +0.008 | -0.042 .. +0.057 | +0.3% | +0.051 | 0.77 |  | 10/16 |
| MNQ | 5 | eod | -1.150 | -1.552 .. -0.747 | -9.1% | -2.191 | 5.4e-05 |  | 13/16 |
| MNQ | 15 | h1 * | +0.088 | +0.079 .. +0.097 | +16.5% | +0.200 | 1e-58 | 1.19e-55 | 16/16 |
| MNQ | 15 | h2 | +0.105 | +0.089 .. +0.122 | +13.6% | +0.240 | 1.6e-31 |  | 16/16 |
| MNQ | 15 | h4 | +0.111 | +0.077 .. +0.144 | +9.8% | +0.255 | 2.5e-10 |  | 15/16 |
| MNQ | 15 | h8 | +0.120 | +0.067 .. +0.174 | +7.2% | +0.255 | 5.6e-05 |  | 14/16 |
| MNQ | 15 | h16 | +0.070 | +0.001 .. +0.138 | +2.8% | +0.207 | 0.083 |  | 12/16 |
| MNQ | 15 | eod | -0.137 | -0.419 .. +0.145 | -2.2% | -0.313 | 0.61 |  | 10/16 |
| MNQ | 60 | h1 * | +0.117 | +0.096 .. +0.138 | +22.1% | +0.251 | 1e-28 | 7.23e-26 | 16/16 |
| MNQ | 60 | h2 | +0.134 | +0.103 .. +0.165 | +17.5% | +0.292 | 6.1e-17 |  | 15/16 |
| MNQ | 60 | h4 | +0.176 | +0.126 .. +0.226 | +15.9% | +0.327 | 5.4e-12 |  | 15/16 |
| MNQ | 60 | h8 | +0.195 | +0.136 .. +0.254 | +12.3% | +0.347 | 4.3e-09 |  | 16/16 |
| MNQ | 60 | h16 | +0.220 | +0.115 .. +0.325 | +10.0% | +0.353 | 6.7e-05 |  | 14/16 |
| MNQ | 60 | eod | +0.224 | +0.100 .. +0.348 | +9.7% | +0.368 | 0.00041 |  | 15/16 |
| MYM | 5 | h1 * | +0.083 | +0.075 .. +0.091 | +15.6% | +0.176 | 2.3e-91 | 3.08e-88 | 8/8 |
| MYM | 5 | h2 | +0.090 | +0.077 .. +0.103 | +11.8% | +0.188 | 9.6e-43 |  | 8/8 |
| MYM | 5 | h4 | +0.085 | +0.061 .. +0.110 | +7.8% | +0.186 | 6.5e-12 |  | 8/8 |
| MYM | 5 | h8 | +0.079 | +0.036 .. +0.122 | +5.0% | +0.159 | 0.017 |  | 7/8 |
| MYM | 5 | h16 | +0.032 | -0.030 .. +0.095 | +1.4% | +0.059 | 0.56 |  | 6/8 |
| MYM | 5 | eod | -0.952 | -1.441 .. -0.462 | -8.1% | -2.161 | 0.0071 |  | 7/8 |
| MYM | 15 | h1 * | +0.098 | +0.085 .. +0.111 | +18.4% | +0.214 | 8.6e-48 | 8.82e-45 | 8/8 |
| MYM | 15 | h2 | +0.117 | +0.094 .. +0.140 | +15.3% | +0.255 | 3.3e-19 |  | 8/8 |
| MYM | 15 | h4 | +0.138 | +0.099 .. +0.176 | +12.3% | +0.283 | 1.7e-05 |  | 8/8 |
| MYM | 15 | h8 | +0.153 | +0.092 .. +0.214 | +9.3% | +0.302 | 0.043 |  | 7/8 |
| MYM | 15 | h16 | +0.111 | +0.002 .. +0.221 | +4.5% | +0.238 | 0.33 |  | 7/8 |
| MYM | 15 | eod | +0.165 | -0.192 .. +0.521 | +2.7% | +0.017 | 0.63 |  | 5/8 |
| MYM | 60 | h1 * | +0.129 | +0.100 .. +0.157 | +24.6% | +0.273 | 1.5e-18 | 7.78e-16 | 8/8 |
| MYM | 60 | h2 | +0.174 | +0.131 .. +0.217 | +23.0% | +0.344 | 4.6e-14 |  | 8/8 |
| MYM | 60 | h4 | +0.212 | +0.150 .. +0.273 | +19.6% | +0.387 | 1.4e-09 |  | 8/8 |
| MYM | 60 | h8 | +0.269 | +0.169 .. +0.370 | +17.4% | +0.422 | 1.4e-06 |  | 8/8 |
| MYM | 60 | h16 | +0.380 | +0.206 .. +0.555 | +18.0% | +0.490 | 4.1e-05 |  | 7/8 |
| MYM | 60 | eod | +0.382 | +0.180 .. +0.583 | +17.2% | +0.529 | 0.00034 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.31 pts | -0.60 .. -0.01 | 0.14 |
| MES | 15 | -0.39 pts | -0.95 .. +0.16 | 0.32 |
| MES | 60 | +0.78 pts | -0.61 .. +2.17 | 0.35 |
| MNQ | 5 | -0.21 pts | -0.51 .. +0.10 | 0.27 |
| MNQ | 15 | -0.28 pts | -0.91 .. +0.35 | 0.51 |
| MNQ | 60 | -0.42 pts | -1.88 .. +1.04 | 0.58 |
| MYM | 5 | -0.34 pts | -0.78 .. +0.10 | 0.16 |
| MYM | 15 | +0.07 pts | -0.74 .. +0.88 | 0.87 |
| MYM | 60 | -1.13 pts | -2.97 .. +0.71 | 0.23 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 86981 | -0.008 | 0.241 | -0.17 | -3.67 | -3.59 | -3.76 | -3.51 |
| MES | 5 | h2 | event | against signal | 86981 | +0.019 | 0.241 | +0.38 | -3.12 | -3.28 | -2.95 | -3.36 |
| MES | 5 | h4 | event | against signal | 86981 | +0.025 | 0.241 | +0.38 | -3.12 | -3.27 | -2.96 | -3.36 |
| MES | 5 | h8 | event | against signal | 86981 | +0.029 | 0.241 | +0.38 | -3.12 | -3.22 | -3.02 | -3.34 |
| MES | 5 | h16 | event | against signal | 86981 | +0.040 | 0.241 | +0.38 | -3.12 | -3.07 | -3.17 | -3.37 |
| MES | 5 | eod | event | against signal | 86981 | +0.003 | 0.241 | +0.69 | -2.81 | -3.32 | -2.26 | -2.75 |
| MES | 15 | h1 | event | with signal | 24987 | -0.006 | 0.139 | -0.10 | -3.60 | -3.65 | -3.54 | -3.38 |
| MES | 15 | h2 | event | against signal | 24987 | +0.011 | 0.139 | +0.15 | -3.35 | -3.21 | -3.50 | -3.61 |
| MES | 15 | h4 | event | against signal | 24987 | +0.018 | 0.139 | +0.09 | -3.41 | -3.17 | -3.66 | -3.67 |
| MES | 15 | h8 | event | against signal | 24987 | +0.030 | 0.139 | +0.15 | -3.35 | -3.30 | -3.40 | -3.65 |
| MES | 15 | h16 | event | against signal | 24987 | +0.037 | 0.139 | +0.39 | -3.11 | -3.28 | -2.93 | -3.43 |
| MES | 15 | eod | event | against signal | 24987 | +0.008 | 0.139 | +0.93 | -2.57 | -3.76 | -1.32 | -2.34 |
| MES | 60 | h1 | event | with signal | 4871 | +0.014 | 0.069 | +0.47 | -3.03 | -2.97 | -3.08 | -2.96 |
| MES | 60 | h2 | event | with signal | 4871 | +0.025 | 0.069 | +1.13 | -2.37 | -2.98 | -1.74 | -2.12 |
| MES | 60 | h4 | event | with signal | 4871 | +0.015 | 0.069 | -0.33 | -3.83 | -3.22 | -4.46 | -3.45 |
| MES | 60 | h8 | event | with signal | 4871 | +0.024 | 0.069 | -0.72 | -4.22 | -2.55 | -5.93 | -3.61 |
| MES | 60 | h16 | event | with signal | 4871 | +0.042 | 0.069 | -1.91 | -5.41 | -1.72 | -9.18 | -5.23 |
| MES | 60 | eod | event | with signal | 4871 | +0.026 | 0.069 | -3.82 | -7.32 | -2.84 | -11.89 | -6.85 |
| MNQ | 5 | h1 | event | with signal | 91716 | +0.000 | 0.111 | -0.10 | -2.10 | -2.06 | -2.15 | -2.02 |
| MNQ | 5 | h2 | event | with signal | 91716 | -0.006 | 0.111 | -0.21 | -2.21 | -2.14 | -2.29 | -2.06 |
| MNQ | 5 | h4 | event | with signal | 91716 | +0.002 | 0.111 | -0.12 | -2.12 | -2.07 | -2.19 | -2.04 |
| MNQ | 5 | h8 | event | with signal | 91716 | +0.006 | 0.111 | -0.10 | -2.10 | -2.00 | -2.24 | -2.14 |
| MNQ | 5 | h16 | event | against signal | 91716 | +0.015 | 0.111 | +0.24 | -1.76 | -1.93 | -1.54 | -1.66 |
| MNQ | 5 | eod | event | against signal | 91716 | -0.004 | 0.111 | +0.61 | -1.39 | -1.94 | -0.70 | -0.85 |
| MNQ | 15 | h1 | event | with signal | 25768 | +0.003 | 0.064 | +0.24 | -1.76 | -2.10 | -1.31 | -1.63 |
| MNQ | 15 | h2 | event | against signal | 25768 | +0.004 | 0.064 | -0.02 | -2.02 | -1.80 | -2.29 | -2.09 |
| MNQ | 15 | h4 | event | against signal | 25768 | +0.022 | 0.064 | +0.21 | -1.79 | -1.88 | -1.66 | -1.81 |
| MNQ | 15 | h8 | event | against signal | 25768 | +0.029 | 0.064 | +0.52 | -1.48 | -1.91 | -0.93 | -1.40 |
| MNQ | 15 | h16 | event | against signal | 25768 | +0.038 | 0.064 | +0.51 | -1.49 | -1.70 | -1.22 | -1.50 |
| MNQ | 15 | eod | event | with signal | 25768 | +0.026 | 0.064 | -1.39 | -3.39 | -1.95 | -5.26 | -3.86 |
| MNQ | 60 | h1 | event | with signal | 4916 | -0.000 | 0.031 | -0.46 | -2.46 | -1.51 | -3.71 | -2.47 |
| MNQ | 60 | h2 | event | against signal | 4916 | +0.009 | 0.031 | +0.11 | -1.89 | -2.52 | -1.06 | -2.13 |
| MNQ | 60 | h4 | event | with signal | 4916 | -0.004 | 0.031 | -0.52 | -2.52 | -1.88 | -3.38 | -2.11 |
| MNQ | 60 | h8 | event | with signal | 4916 | -0.000 | 0.031 | -0.50 | -2.50 | -0.78 | -4.78 | -1.89 |
| MNQ | 60 | h16 | event | with signal | 4916 | +0.024 | 0.031 | -2.51 | -4.51 | +0.03 | -10.51 | -4.01 |
| MNQ | 60 | eod | event | with signal | 4916 | +0.022 | 0.031 | -3.06 | -5.06 | -0.43 | -11.18 | -4.12 |
| MYM | 5 | h1 | event | with signal | 43782 | -0.007 | 0.122 | -0.12 | -2.12 | +nan | -2.12 | -2.00 |
| MYM | 5 | h2 | event | against signal | 43782 | +0.011 | 0.122 | +0.30 | -1.70 | +nan | -1.70 | -1.85 |
| MYM | 5 | h4 | event | against signal | 43782 | +0.014 | 0.122 | +0.23 | -1.77 | +nan | -1.77 | -1.92 |
| MYM | 5 | h8 | event | against signal | 43782 | +0.009 | 0.122 | +0.08 | -1.92 | +nan | -1.92 | -2.05 |
| MYM | 5 | h16 | event | with signal | 43782 | -0.000 | 0.122 | -0.07 | -2.07 | +nan | -2.07 | -1.88 |
| MYM | 5 | eod | event | against signal | 43782 | +0.023 | 0.122 | +0.06 | -1.94 | +nan | -1.94 | -2.21 |
| MYM | 15 | h1 | event | with signal | 12539 | +0.005 | 0.069 | +0.08 | -1.92 | +nan | -1.92 | -1.79 |
| MYM | 15 | h2 | event | with signal | 12539 | +0.017 | 0.069 | +0.39 | -1.61 | +nan | -1.61 | -1.47 |
| MYM | 15 | h4 | event | with signal | 12539 | +0.028 | 0.069 | +0.68 | -1.32 | +nan | -1.32 | -1.24 |
| MYM | 15 | h8 | event | with signal | 12539 | +0.017 | 0.069 | +0.35 | -1.65 | +nan | -1.65 | -1.57 |
| MYM | 15 | h16 | event | with signal | 12539 | +0.005 | 0.069 | +0.17 | -1.83 | +nan | -1.83 | -1.77 |
| MYM | 15 | eod | event | against signal | 12539 | +0.064 | 0.069 | +0.87 | -1.13 | +nan | -1.13 | -1.63 |
| MYM | 60 | h1 | event | with signal | 2413 | +0.023 | 0.034 | +0.38 | -1.62 | +nan | -1.62 | -1.63 |
| MYM | 60 | h2 | event | with signal | 2413 | +0.028 | 0.034 | +1.00 | -1.00 | +nan | -1.00 | -0.59 |
| MYM | 60 | h4 | event | with signal | 2413 | -0.009 | 0.034 | -1.46 | -3.46 | +nan | -3.46 | -2.90 |
| MYM | 60 | h8 | event | with signal | 2413 | -0.004 | 0.034 | -2.63 | -4.63 | +nan | -4.63 | -3.94 |
| MYM | 60 | h16 | event | with signal | 2413 | +0.008 | 0.034 | -1.61 | -3.61 | +nan | -3.61 | -3.83 |
| MYM | 60 | eod | event | with signal | 2413 | +0.017 | 0.034 | -2.45 | -4.45 | +nan | -4.45 | -4.45 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.035 | -1.104 | -1.075 | -0.996 | -0.861 | +0.000 | -0.017 | -0.029 | -0.035 | -0.040 | -0.051 |
| MES | 15 | -1.115 | -1.188 | -1.135 | -1.028 | -0.874 | +0.000 | -0.008 | -0.013 | -0.020 | -0.039 | -0.061 |
| MES | 60 | -1.672 | -1.377 | -1.189 | -1.101 | -0.925 | +0.000 | +0.016 | +0.028 | -0.006 | -0.012 | +0.011 |
| MNQ | 5 | -1.089 | -1.161 | -1.131 | -1.042 | -0.898 | +0.000 | -0.006 | -0.013 | -0.006 | -0.003 | -0.025 |
| MNQ | 15 | -1.134 | -1.201 | -1.151 | -1.040 | -0.875 | +0.000 | +0.002 | -0.005 | -0.024 | -0.035 | -0.053 |
| MNQ | 60 | -1.605 | -1.308 | -1.105 | -1.047 | -0.886 | +0.000 | +0.001 | -0.008 | -0.013 | -0.015 | -0.004 |
| MYM | 5 | -0.985 | -1.060 | -1.047 | -0.972 | -0.852 | +0.000 | -0.009 | -0.014 | -0.019 | -0.016 | -0.010 |
| MYM | 15 | -1.028 | -1.105 | -1.090 | -0.997 | -0.867 | +0.000 | +0.005 | +0.017 | +0.028 | +0.006 | -0.017 |
| MYM | 60 | -1.433 | -1.257 | -1.127 | -1.086 | -0.931 | +0.000 | +0.023 | +0.031 | -0.054 | -0.058 | +0.021 |

## Calibration

- MES 5-min: 1033593 bars, 86981 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341360 bars, 24987 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83231 bars, 4871 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1031845 bars, 91716 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341205 bars, 25768 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83229 bars, 4916 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 516339 bars, 43782 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170547 bars, 12539 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41455 bars, 2413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
