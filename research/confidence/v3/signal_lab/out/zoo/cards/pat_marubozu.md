# Impact card: pat_marubozu

candle pattern marubozu in its textbook direction: body >= 0.9 x range AND body > avgB10; direction of the body [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.013 R20 over the next 4 bars (20 min), p=0.054; we would catch an effect of 0.015 R20 or more 80% of the time).
- MES 5-min size: the market moves 2% LESS after the event than after matched bars over the next 2 bars (10 min) (-0.015 R20, possible, q=0.0339, 9 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.31 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.278 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.016 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.14 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.136 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.086 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.100 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.11).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.83 at recent bar sizes, 90% range up to $7.33); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (5 min), p=0.63; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.027 R20, CONFIRMED, q=1.13e-14, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.74 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.082 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.032 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.042 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.11).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.46 at recent bar sizes, 90% range up to $2.68); about 5.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.108 R20 over the rest of the session (to 16:45), p=0.57; we would catch an effect of 0.108 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.59).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $10.27 at recent bar sizes, 90% range up to $14.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.014 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.028 R20 or more 80% of the time).
- MYM 5-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.031 R20, CONFIRMED, q=8.52e-09, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.199 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.022 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.062 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.17).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.25 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.103 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.054 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.150 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.16).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.36 at recent bar sizes, 90% range up to $8.01); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.000 | -0.005 .. +0.005 | +0.0001 | 0.96 / 0.96 / 0.92 | 0.921 |  |  | 9/16 | +0.001 | -0.001 |  | +0.1 / +0.1 |  |
| MES | 5 | h2 | +0.006 | -0.002 .. +0.013 | +0.0016 | 0.12 / 0.12 / 0.11 | 0.109 |  |  | 11/16 | +0.003 | +0.008 |  | +1.6 / +1.5 |  |
| MES | 5 | h4 * | +0.013 | +0.003 .. +0.023 | +0.0025 | 0.0089 / 0.0083 / 0.01 | 0.00912 | 1 | 0.885 | 11/16 | +0.008 | +0.018 | False | +2.7 / +2.6 | 0.015 |
| MES | 5 | h8 | +0.013 | -0.001 .. +0.027 | +0.0017 | 0.071 / 0.061 / 0.084 | 0.0862 |  |  | 12/16 | -0.000 | +0.026 |  | +1.8 / +1.8 |  |
| MES | 5 | h16 | +0.004 | -0.018 .. +0.026 | +0.0004 | 0.73 / 0.72 / 0.72 | 0.731 |  |  | 10/16 | +0.001 | +0.007 |  | +0.4 / +0.3 |  |
| MES | 5 | eod | +0.077 | -0.047 .. +0.201 | +0.0014 | 0.22 / 0.22 / 0.26 | 0.257 |  |  | 8/16 | +0.180 | -0.025 |  | +1.2 / +1.2 |  |
| MES | 15 | h1 | +0.005 | -0.008 .. +0.018 | +0.0013 | 0.44 / 0.43 / 0.44 | 0.435 |  |  | 8/16 | +0.017 | -0.007 |  | +0.8 / +0.8 |  |
| MES | 15 | h2 | +0.006 | -0.013 .. +0.026 | +0.0011 | 0.52 / 0.5 / 0.51 | 0.501 |  |  | 10/16 | +0.004 | +0.009 |  | +0.7 / +0.6 |  |
| MES | 15 | h4 * | +0.016 | -0.010 .. +0.042 | +0.0019 | 0.23 / 0.23 / 0.28 | 0.268 | 1 | 1 | 12/16 | -0.006 | +0.038 | False | +1.2 / +1.2 | 0.037 |
| MES | 15 | h8 | -0.005 | -0.043 .. +0.033 | -0.0004 | 0.78 / 0.79 / 0.8 | 0.796 |  |  | 10/16 | -0.040 | +0.029 |  | -0.3 / -0.3 |  |
| MES | 15 | h16 | -0.022 | -0.080 .. +0.035 | -0.0013 | 0.45 / 0.45 / 0.47 | 0.47 |  |  | 8/16 | -0.057 | +0.013 |  | -0.7 / -0.8 |  |
| MES | 15 | eod | +0.031 | -0.121 .. +0.183 | +0.0007 | 0.69 / 0.69 / 0.73 | 0.736 |  |  | 9/16 | +0.039 | +0.023 |  | +0.4 / +0.4 |  |
| MES | 60 | h1 | +0.008 | -0.030 .. +0.047 | +0.0017 | 0.67 / 0.68 / 0.65 | 0.655 |  |  | 8/16 | -0.001 | +0.018 |  | +0.4 / +0.4 |  |
| MES | 60 | h2 | +0.022 | -0.036 .. +0.081 | +0.0032 | 0.45 / 0.46 / 0.39 | 0.391 |  |  | 9/16 | -0.009 | +0.054 |  | +0.8 / +0.7 |  |
| MES | 60 | h4 | +0.043 | -0.033 .. +0.119 | +0.0044 | 0.26 / 0.26 / 0.23 | 0.227 |  |  | 12/16 | +0.027 | +0.060 |  | +1.1 / +1.1 | 0.100 |
| MES | 60 | h8 | +0.051 | -0.044 .. +0.145 | +0.0037 | 0.29 / 0.29 / 0.31 | 0.308 |  |  | 9/16 | +0.041 | +0.061 |  | +1.0 / +1.0 |  |
| MES | 60 | h16 | +0.051 | -0.066 .. +0.167 | +0.0029 | 0.39 / 0.4 / 0.42 | 0.426 |  |  | 8/16 | +0.015 | +0.086 |  | +0.8 / +0.9 |  |
| MES | 60 | eod * | +0.086 | -0.032 .. +0.203 | +0.0046 | 0.15 / 0.16 / 0.19 | 0.192 | 1 | 1 | 9/16 | +0.056 | +0.115 | False | +1.3 / +1.4 |  |
| MNQ | 5 | h1 * | +0.006 | -0.000 .. +0.013 | +0.0018 | 0.068 / 0.071 / 0.052 | 0.0508 | 1 | 1 | 11/16 | +0.011 | +0.002 | False | +1.9 / +1.8 |  |
| MNQ | 5 | h2 | +0.006 | -0.003 .. +0.016 | +0.0011 | 0.2 / 0.21 / 0.22 | 0.209 |  |  | 10/16 | +0.006 | +0.007 |  | +1.3 / +1.3 |  |
| MNQ | 5 | h4 | +0.009 | -0.005 .. +0.022 | +0.0010 | 0.22 / 0.22 / 0.28 | 0.262 |  |  | 11/16 | +0.004 | +0.013 |  | +1.3 / +1.2 | 0.019 |
| MNQ | 5 | h8 | +0.014 | -0.006 .. +0.033 | +0.0011 | 0.17 / 0.17 / 0.26 | 0.246 |  |  | 10/16 | +0.008 | +0.019 |  | +1.4 / +1.4 |  |
| MNQ | 5 | h16 | -0.020 | -0.050 .. +0.010 | -0.0011 | 0.19 / 0.18 / 0.24 | 0.237 |  |  | 10/16 | -0.045 | +0.005 |  | -1.3 / -1.3 |  |
| MNQ | 5 | eod | +0.040 | -0.156 .. +0.236 | +0.0005 | 0.69 / 0.69 / 0.68 | 0.669 |  |  | 8/16 | +0.032 | +0.048 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h1 | +0.002 | -0.012 .. +0.017 | +0.0004 | 0.76 / 0.76 / 0.8 | 0.752 |  |  | 9/16 | +0.002 | +0.003 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h2 | +0.017 | -0.003 .. +0.037 | +0.0020 | 0.094 / 0.092 / 0.22 | 0.175 |  |  | 11/16 | +0.019 | +0.015 |  | +1.6 / +1.7 |  |
| MNQ | 15 | h4 * | +0.032 | +0.001 .. +0.063 | +0.0022 | 0.046 / 0.05 / 0.19 | 0.171 | 1 | 0.999 | 12/16 | +0.033 | +0.031 | False | +2.1 / +2.0 | 0.042 |
| MNQ | 15 | h8 | +0.017 | -0.028 .. +0.062 | +0.0009 | 0.46 / 0.47 / 0.61 | 0.576 |  |  | 10/16 | +0.005 | +0.029 |  | +0.7 / +0.7 |  |
| MNQ | 15 | h16 | +0.018 | -0.049 .. +0.085 | +0.0008 | 0.59 / 0.61 / 0.66 | 0.648 |  |  | 12/16 | -0.011 | +0.048 |  | +0.5 / +0.5 |  |
| MNQ | 15 | eod | -0.026 | -0.195 .. +0.144 | -0.0004 | 0.76 / 0.77 / 0.83 | 0.82 |  |  | 9/16 | -0.122 | +0.070 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h1 | +0.024 | -0.016 .. +0.065 | +0.0048 | 0.24 / 0.26 / 0.21 | 0.211 |  |  | 9/16 | +0.048 | +0.001 |  | +1.2 / +1.2 |  |
| MNQ | 60 | h2 | +0.050 | -0.009 .. +0.108 | +0.0067 | 0.095 / 0.094 / 0.075 | 0.0727 |  |  | 8/16 | +0.068 | +0.032 |  | +1.7 / +1.7 |  |
| MNQ | 60 | h4 | +0.068 | -0.007 .. +0.144 | +0.0065 | 0.076 / 0.07 / 0.082 | 0.0847 |  |  | 11/16 | +0.098 | +0.039 |  | +1.8 / +1.8 | 0.108 |
| MNQ | 60 | h8 | +0.061 | -0.042 .. +0.164 | +0.0043 | 0.24 / 0.23 / 0.25 | 0.243 |  |  | 8/16 | +0.109 | +0.014 |  | +1.2 / +1.2 |  |
| MNQ | 60 | h16 | +0.101 | -0.028 .. +0.230 | +0.0055 | 0.12 / 0.11 / 0.12 | 0.12 |  |  | 11/16 | +0.118 | +0.084 |  | +1.5 / +1.5 |  |
| MNQ | 60 | eod * | +0.108 | -0.019 .. +0.234 | +0.0056 | 0.096 / 0.088 / 0.11 | 0.109 | 1 | 1 | 12/16 | +0.134 | +0.081 | False | +1.6 / +1.7 |  |
| MYM | 5 | h1 | -0.004 | -0.014 .. +0.007 | -0.0009 | 0.48 / 0.48 / 0.56 | 0.56 |  |  | 5/8 | n/a | -0.004 |  | -0.7 / -0.7 |  |
| MYM | 5 | h2 | -0.000 | -0.014 .. +0.013 | -0.0000 | 0.98 / 0.99 / 0.94 | 0.93 |  |  | 3/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h4 | +0.004 | -0.015 .. +0.022 | +0.0004 | 0.68 / 0.7 / 0.74 | 0.716 |  |  | 5/8 | n/a | +0.004 |  | +0.4 / +0.4 | 0.028 |
| MYM | 5 | h8 * | +0.014 | -0.014 .. +0.042 | +0.0009 | 0.32 / 0.33 / 0.48 | 0.459 | 1 | 1 | 4/8 | n/a | +0.014 | False | +1.0 / +1.0 |  |
| MYM | 5 | h16 | +0.002 | -0.038 .. +0.042 | +0.0001 | 0.92 / 0.92 / 0.91 | 0.897 |  |  | 3/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 5 | eod | -0.019 | -0.259 .. +0.222 | -0.0002 | 0.88 / 0.89 / 0.9 | 0.891 |  |  | 4/8 | n/a | -0.019 |  | -0.1 / -0.2 |  |
| MYM | 15 | h1 | -0.012 | -0.034 .. +0.009 | -0.0024 | 0.27 / 0.26 / 0.34 | 0.301 |  |  | 7/8 | n/a | -0.012 |  | -1.1 / -1.1 |  |
| MYM | 15 | h2 * | -0.022 | -0.054 .. +0.009 | -0.0025 | 0.17 / 0.15 / 0.32 | 0.254 | 1 | 1 | 7/8 | n/a | -0.022 | False | -1.4 / -1.4 |  |
| MYM | 15 | h4 | -0.004 | -0.047 .. +0.039 | -0.0003 | 0.85 / 0.84 / 0.91 | 0.885 |  |  | 4/8 | n/a | -0.004 |  | -0.2 / -0.2 | 0.062 |
| MYM | 15 | h8 | +0.000 | -0.059 .. +0.060 | +0.0000 | 0.99 / 0.99 / 0.99 | 0.992 |  |  | 2/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 15 | h16 | +0.019 | -0.071 .. +0.109 | +0.0007 | 0.67 / 0.67 / 0.79 | 0.758 |  |  | 3/8 | n/a | +0.019 |  | +0.4 / +0.4 |  |
| MYM | 15 | eod | +0.011 | -0.241 .. +0.263 | +0.0002 | 0.93 / 0.93 / 0.95 | 0.958 |  |  | 4/8 | n/a | +0.011 |  | +0.1 / +0.1 |  |
| MYM | 60 | h1 | +0.031 | -0.027 .. +0.090 | +0.0063 | 0.29 / 0.31 / 0.26 | 0.242 |  |  | 6/8 | n/a | +0.031 |  | +1.0 / +1.1 |  |
| MYM | 60 | h2 * | +0.054 | -0.032 .. +0.140 | +0.0076 | 0.22 / 0.23 / 0.17 | 0.158 | 1 | 1 | 7/8 | n/a | +0.054 | False | +1.3 / +1.2 |  |
| MYM | 60 | h4 | +0.068 | -0.044 .. +0.180 | +0.0069 | 0.23 / 0.23 / 0.21 | 0.209 |  |  | 5/8 | n/a | +0.068 |  | +1.2 / +1.2 | 0.150 |
| MYM | 60 | h8 | +0.066 | -0.066 .. +0.198 | +0.0049 | 0.32 / 0.35 / 0.37 | 0.357 |  |  | 5/8 | n/a | +0.066 |  | +0.9 / +1.0 |  |
| MYM | 60 | h16 | -0.010 | -0.168 .. +0.148 | -0.0005 | 0.9 / 0.91 / 0.91 | 0.904 |  |  | 5/8 | n/a | -0.010 |  | -0.1 / -0.1 |  |
| MYM | 60 | eod | +0.004 | -0.157 .. +0.166 | +0.0003 | 0.96 / 0.96 / 0.96 | 0.948 |  |  | 3/8 | n/a | +0.004 |  | +0.0 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.007 | -0.012 .. -0.001 | -1.3% | -0.009 | 0.013 |  | 9/16 |
| MES | 5 | h2 * | -0.015 | -0.023 .. -0.007 | -2.1% | -0.026 | 0.00017 | 0.0339 | 9/16 |
| MES | 5 | h4 | -0.021 | -0.033 .. -0.009 | -2.1% | -0.044 | 0.00066 |  | 8/16 |
| MES | 5 | h8 | -0.017 | -0.034 .. -0.001 | -1.2% | -0.054 | 0.25 |  | 9/16 |
| MES | 5 | h16 | -0.016 | -0.040 .. +0.008 | -0.8% | -0.052 | 0.9 |  | 5/16 |
| MES | 5 | eod | +0.049 | -0.212 .. +0.310 | +0.5% | +0.299 | 0.71 |  | 10/16 |
| MES | 15 | h1 | -0.001 | -0.010 .. +0.007 | -0.3% | +0.016 | 0.89 |  | 8/16 |
| MES | 15 | h2 | +0.005 | -0.009 .. +0.019 | +0.7% | +0.017 | 0.49 |  | 10/16 |
| MES | 15 | h4 | +0.004 | -0.016 .. +0.025 | +0.4% | +0.016 | 0.67 |  | 8/16 |
| MES | 15 | h8 | +0.019 | -0.010 .. +0.049 | +1.2% | +0.021 | 0.2 |  | 9/16 |
| MES | 15 | h16 * | +0.030 | -0.013 .. +0.074 | +1.3% | +0.042 | 0.17 | 1 | 10/16 |
| MES | 15 | eod | +0.042 | -0.126 .. +0.209 | +0.8% | +0.243 | 0.62 |  | 10/16 |
| MES | 60 | h1 | +0.017 | -0.011 .. +0.045 | +3.3% | +0.054 | 0.32 |  | 9/16 |
| MES | 60 | h2 | +0.047 | +0.005 .. +0.088 | +6.3% | +0.090 | 0.028 |  | 13/16 |
| MES | 60 | h4 * | +0.060 | +0.013 .. +0.108 | +5.7% | +0.109 | 0.018 | 1 | 14/16 |
| MES | 60 | h8 | +0.035 | -0.032 .. +0.102 | +2.3% | +0.097 | 0.3 |  | 13/16 |
| MES | 60 | h16 | +0.009 | -0.072 .. +0.091 | +0.5% | +0.068 | 0.82 |  | 9/16 |
| MES | 60 | eod | -0.009 | -0.093 .. +0.076 | -0.4% | +0.067 | 0.84 |  | 6/16 |
| MNQ | 5 | h1 * | +0.027 | +0.021 .. +0.032 | +5.0% | +0.032 | 2.4e-17 | 1.13e-14 | 16/16 |
| MNQ | 5 | h2 | +0.035 | +0.026 .. +0.044 | +4.5% | +0.047 | 1.1e-11 |  | 16/16 |
| MNQ | 5 | h4 | +0.052 | +0.036 .. +0.068 | +4.7% | +0.076 | 1.5e-10 |  | 15/16 |
| MNQ | 5 | h8 | +0.078 | +0.051 .. +0.106 | +4.8% | +0.123 | 1.9e-08 |  | 15/16 |
| MNQ | 5 | h16 | +0.141 | +0.091 .. +0.192 | +5.9% | +0.228 | 3.8e-08 |  | 15/16 |
| MNQ | 5 | eod | +1.065 | +0.590 .. +1.539 | +8.5% | +2.412 | 1.1e-05 |  | 13/16 |
| MNQ | 15 | h1 | +0.022 | +0.012 .. +0.032 | +4.2% | +0.040 | 0.059 |  | 14/16 |
| MNQ | 15 | h2 | +0.030 | +0.012 .. +0.047 | +3.8% | +0.042 | 0.059 |  | 13/16 |
| MNQ | 15 | h4 | +0.029 | -0.003 .. +0.061 | +2.6% | +0.059 | 0.29 |  | 13/16 |
| MNQ | 15 | h8 | +0.044 | -0.006 .. +0.095 | +2.6% | +0.096 | 0.085 |  | 12/16 |
| MNQ | 15 | h16 * | +0.079 | +0.013 .. +0.145 | +3.1% | +0.175 | 0.019 | 1 | 13/16 |
| MNQ | 15 | eod | +0.128 | -0.111 .. +0.367 | +2.0% | +0.441 | 0.29 |  | 9/16 |
| MNQ | 60 | h1 | +0.028 | -0.003 .. +0.059 | +5.3% | +0.054 | 0.13 |  | 10/16 |
| MNQ | 60 | h2 | +0.037 | -0.003 .. +0.077 | +4.9% | +0.064 | 0.11 |  | 10/16 |
| MNQ | 60 | h4 * | +0.041 | -0.007 .. +0.090 | +3.7% | +0.078 | 0.098 | 1 | 9/16 |
| MNQ | 60 | h8 | +0.029 | -0.039 .. +0.096 | +1.8% | +0.075 | 0.42 |  | 11/16 |
| MNQ | 60 | h16 | +0.029 | -0.057 .. +0.115 | +1.3% | +0.081 | 0.51 |  | 10/16 |
| MNQ | 60 | eod | +0.022 | -0.067 .. +0.112 | +1.0% | +0.072 | 0.63 |  | 11/16 |
| MYM | 5 | h1 * | +0.031 | +0.023 .. +0.040 | +5.9% | +0.062 | 2.5e-11 | 8.52e-09 | 8/8 |
| MYM | 5 | h2 | +0.031 | +0.019 .. +0.043 | +4.1% | +0.070 | 1.1e-06 |  | 7/8 |
| MYM | 5 | h4 | +0.032 | +0.010 .. +0.054 | +2.9% | +0.072 | 0.015 |  | 7/8 |
| MYM | 5 | h8 | +0.042 | +0.003 .. +0.080 | +2.6% | +0.087 | 0.038 |  | 7/8 |
| MYM | 5 | h16 | +0.075 | +0.020 .. +0.129 | +3.2% | +0.121 | 0.0096 |  | 7/8 |
| MYM | 5 | eod | +0.604 | +0.249 .. +0.958 | +5.2% | +1.144 | 0.00084 |  | 6/8 |
| MYM | 15 | h1 * | +0.029 | +0.013 .. +0.044 | +5.4% | +0.056 | 0.029 | 1 | 7/8 |
| MYM | 15 | h2 | +0.028 | +0.003 .. +0.054 | +3.7% | +0.053 | 0.11 |  | 7/8 |
| MYM | 15 | h4 | +0.018 | -0.023 .. +0.058 | +1.6% | +0.039 | 0.61 |  | 6/8 |
| MYM | 15 | h8 | +0.009 | -0.054 .. +0.071 | +0.5% | +0.029 | 0.83 |  | 5/8 |
| MYM | 15 | h16 | +0.062 | -0.037 .. +0.160 | +2.5% | +0.091 | 0.25 |  | 6/8 |
| MYM | 15 | eod | +0.043 | -0.234 .. +0.320 | +0.7% | +0.153 | 0.96 |  | 6/8 |
| MYM | 60 | h1 * | +0.052 | +0.006 .. +0.097 | +9.9% | +0.084 | 0.026 | 1 | 6/8 |
| MYM | 60 | h2 | +0.055 | -0.005 .. +0.114 | +7.2% | +0.132 | 0.073 |  | 6/8 |
| MYM | 60 | h4 | +0.072 | -0.002 .. +0.147 | +6.7% | +0.111 | 0.058 |  | 5/8 |
| MYM | 60 | h8 | +0.099 | -0.002 .. +0.199 | +6.4% | +0.148 | 0.054 |  | 7/8 |
| MYM | 60 | h16 | +0.090 | -0.023 .. +0.204 | +4.3% | +0.105 | 0.13 |  | 7/8 |
| MYM | 60 | eod | +0.052 | -0.068 .. +0.172 | +2.4% | +0.085 | 0.39 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.11 pts | -0.47 .. +0.25 | 0.68 |
| MES | 15 | +0.36 pts | -0.50 .. +1.22 | 0.47 |
| MES | 60 | +1.11 pts | -0.87 .. +3.09 | 0.39 |
| MNQ | 5 | -0.58 pts | -0.99 .. -0.17 | 0.0065 |
| MNQ | 15 | +0.19 pts | -0.65 .. +1.03 | 0.69 |
| MNQ | 60 | -0.98 pts | -3.00 .. +1.03 | 0.47 |
| MYM | 5 | -0.41 pts | -0.96 .. +0.14 | 0.25 |
| MYM | 15 | -0.88 pts | -2.02 .. +0.25 | 0.14 |
| MYM | 60 | +0.29 pts | -2.55 .. +3.14 | 0.84 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 79276 | -0.011 | 0.509 | -0.04 | -3.54 | -3.55 | -3.52 | -3.46 |
| MES | 5 | h2 | event | with signal | 79276 | -0.011 | 0.509 | -0.06 | -3.56 | -3.58 | -3.54 | -3.45 |
| MES | 5 | h4 | event | with signal | 79276 | -0.003 | 0.509 | +0.04 | -3.46 | -3.55 | -3.27 | -3.35 |
| MES | 5 | h8 | event | with signal | 79276 | -0.002 | 0.509 | +0.07 | -3.43 | -3.60 | -3.10 | -3.34 |
| MES | 5 | h16 | event | with signal | 79276 | -0.012 | 0.509 | -0.09 | -3.59 | -3.61 | -3.56 | -3.49 |
| MES | 5 | eod | event | with signal | 79276 | +0.085 | 0.509 | +0.59 | -2.91 | -3.00 | -2.73 | -3.08 |
| MES | 15 | h1 | event | with signal | 13176 | -0.003 | 0.224 | -0.03 | -3.53 | -3.43 | -3.67 | -3.41 |
| MES | 15 | h2 | event | with signal | 13176 | -0.003 | 0.224 | +0.18 | -3.32 | -3.41 | -3.19 | -3.17 |
| MES | 15 | h4 | event | with signal | 13176 | +0.007 | 0.224 | +0.55 | -2.95 | -3.46 | -2.28 | -2.82 |
| MES | 15 | h8 | event | against signal | 13176 | +0.016 | 0.224 | -0.27 | -3.77 | -3.24 | -4.48 | -3.92 |
| MES | 15 | h16 | event | against signal | 13176 | +0.033 | 0.224 | -0.00 | -3.50 | -3.14 | -3.99 | -3.65 |
| MES | 15 | eod | event | with signal | 13176 | +0.041 | 0.224 | +0.76 | -2.74 | -3.27 | -2.02 | -2.97 |
| MES | 60 | h1 | event | with signal | 1994 | +0.010 | 0.089 | -0.06 | -3.56 | -3.21 | -3.85 | -3.57 |
| MES | 60 | h2 | event | with signal | 1994 | +0.024 | 0.089 | +1.37 | -2.13 | -3.39 | -1.03 | -2.11 |
| MES | 60 | h4 | event | with signal | 1994 | +0.043 | 0.089 | +0.87 | -2.63 | -2.81 | -2.48 | -2.50 |
| MES | 60 | h8 | event | with signal | 1994 | +0.052 | 0.089 | +1.61 | -1.89 | -1.40 | -2.31 | -1.72 |
| MES | 60 | h16 | event | with signal | 1994 | +0.063 | 0.089 | +2.98 | -0.52 | -1.84 | +0.62 | -0.71 |
| MES | 60 | eod | event | with signal | 1994 | +0.095 | 0.089 | +4.46 | +0.96 | -1.13 | +2.77 | +0.93 |
| MNQ | 5 | h1 | event | with signal | 65023 | +0.002 | 0.221 | +0.04 | -1.96 | -2.01 | -1.83 | -1.92 |
| MNQ | 5 | h2 | event | with signal | 65023 | -0.001 | 0.221 | +0.00 | -2.00 | -2.01 | -1.96 | -1.93 |
| MNQ | 5 | h4 | event | with signal | 65023 | +0.005 | 0.221 | +0.09 | -1.91 | -2.01 | -1.66 | -1.88 |
| MNQ | 5 | h8 | event | with signal | 65023 | +0.017 | 0.221 | +0.03 | -1.97 | -2.03 | -1.82 | -2.01 |
| MNQ | 5 | h16 | event | against signal | 65023 | +0.012 | 0.221 | +0.36 | -1.64 | -1.85 | -1.08 | -1.57 |
| MNQ | 5 | eod | event | with signal | 65023 | +0.091 | 0.221 | +0.50 | -1.50 | -1.83 | -0.59 | -2.04 |
| MNQ | 15 | h1 | event | with signal | 12717 | -0.001 | 0.095 | +0.15 | -1.85 | -2.02 | -1.55 | -1.77 |
| MNQ | 15 | h2 | event | with signal | 12717 | +0.016 | 0.095 | +0.47 | -1.53 | -1.83 | -0.98 | -1.50 |
| MNQ | 15 | h4 | event | with signal | 12717 | +0.033 | 0.095 | +0.99 | -1.01 | -1.71 | +0.27 | -1.01 |
| MNQ | 15 | h8 | event | with signal | 12717 | +0.023 | 0.095 | +0.70 | -1.30 | -1.90 | -0.21 | -1.40 |
| MNQ | 15 | h16 | event | with signal | 12717 | +0.025 | 0.095 | +0.45 | -1.55 | -1.93 | -0.87 | -1.65 |
| MNQ | 15 | eod | event | against signal | 12717 | -0.020 | 0.095 | -0.66 | -2.66 | -1.75 | -4.30 | -1.96 |
| MNQ | 60 | h1 | event | with signal | 2088 | +0.026 | 0.038 | -0.94 | -2.94 | -1.30 | -4.97 | -3.02 |
| MNQ | 60 | h2 | event | with signal | 2088 | +0.051 | 0.038 | +1.63 | -0.37 | -1.10 | +0.53 | -0.39 |
| MNQ | 60 | h4 | event | with signal | 2088 | +0.070 | 0.038 | +0.35 | -1.65 | -1.10 | -2.33 | -1.59 |
| MNQ | 60 | h8 | event | with signal | 2088 | +0.066 | 0.038 | +3.14 | +1.14 | -0.00 | +2.56 | +1.19 |
| MNQ | 60 | h16 | event | with signal | 2088 | +0.117 | 0.038 | +5.92 | +3.92 | +0.05 | +8.75 | +3.63 |
| MNQ | 60 | eod | event | with signal | 2088 | +0.121 | 0.038 | +6.28 | +4.28 | +0.26 | +9.30 | +4.24 |
| MYM | 5 | h1 | event | against signal | 27100 | +0.011 | 0.199 | +0.05 | -1.95 | +nan | -1.95 | -2.03 |
| MYM | 5 | h2 | event | against signal | 27100 | +0.009 | 0.199 | +0.11 | -1.89 | +nan | -1.89 | -1.98 |
| MYM | 5 | h4 | event | with signal | 27100 | -0.005 | 0.199 | -0.01 | -2.01 | +nan | -2.01 | -1.92 |
| MYM | 5 | h8 | event | with signal | 27100 | +0.005 | 0.199 | +0.03 | -1.97 | +nan | -1.97 | -1.90 |
| MYM | 5 | h16 | event | with signal | 27100 | -0.012 | 0.199 | -0.08 | -2.08 | +nan | -2.08 | -1.95 |
| MYM | 5 | eod | event | against signal | 27100 | +0.042 | 0.199 | +0.11 | -1.89 | +nan | -1.89 | -2.05 |
| MYM | 15 | h1 | event | against signal | 6099 | +0.018 | 0.103 | +0.11 | -1.89 | +nan | -1.89 | -1.99 |
| MYM | 15 | h2 | event | against signal | 6099 | +0.027 | 0.103 | +0.02 | -1.98 | +nan | -1.98 | -2.07 |
| MYM | 15 | h4 | event | against signal | 6099 | +0.005 | 0.103 | -0.51 | -2.51 | +nan | -2.51 | -2.52 |
| MYM | 15 | h8 | event | with signal | 6099 | +0.000 | 0.103 | +0.34 | -1.66 | +nan | -1.66 | -1.66 |
| MYM | 15 | h16 | event | with signal | 6099 | +0.026 | 0.103 | +0.71 | -1.29 | +nan | -1.29 | -1.45 |
| MYM | 15 | eod | event | with signal | 6099 | +0.021 | 0.103 | +1.13 | -0.87 | +nan | -0.87 | -1.01 |
| MYM | 60 | h1 | event | with signal | 1068 | +0.033 | 0.046 | +1.16 | -0.84 | +nan | -0.84 | -0.91 |
| MYM | 60 | h2 | event | with signal | 1068 | +0.051 | 0.046 | +1.45 | -0.55 | +nan | -0.55 | -0.39 |
| MYM | 60 | h4 | event | with signal | 1068 | +0.063 | 0.046 | +0.37 | -1.63 | +nan | -1.63 | -1.37 |
| MYM | 60 | h8 | event | with signal | 1068 | +0.063 | 0.046 | +1.32 | -0.68 | +nan | -0.68 | -0.35 |
| MYM | 60 | h16 | event | against signal | 1068 | -0.003 | 0.046 | +0.65 | -1.35 | +nan | -1.35 | -1.07 |
| MYM | 60 | eod | event | with signal | 1068 | +0.017 | 0.046 | +1.11 | -0.89 | +nan | -0.89 | -1.05 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.656 | -0.722 | -0.761 | -0.806 | -0.878 | +0.000 | -0.115 | -0.115 | -0.108 | -0.107 | -0.120 |
| MES | 15 | -0.935 | -0.975 | -1.016 | -1.044 | -1.111 | +0.000 | -0.055 | -0.055 | -0.047 | -0.072 | -0.102 |
| MES | 60 | -1.825 | -1.408 | -1.367 | -1.392 | -1.408 | +0.000 | -0.004 | +0.000 | +0.006 | +0.011 | +0.084 |
| MNQ | 5 | -0.930 | -0.996 | -1.041 | -1.081 | -1.149 | +0.000 | -0.057 | -0.061 | -0.056 | -0.045 | -0.078 |
| MNQ | 15 | -1.082 | -1.129 | -1.181 | -1.208 | -1.270 | +0.000 | -0.023 | -0.006 | +0.009 | -0.004 | -0.009 |
| MNQ | 60 | -1.879 | -1.481 | -1.423 | -1.455 | -1.453 | +0.000 | +0.020 | +0.036 | +0.051 | -0.008 | +0.206 |
| MYM | 5 | -0.937 | -1.017 | -1.075 | -1.134 | -1.209 | +0.000 | -0.038 | -0.036 | -0.034 | -0.024 | -0.047 |
| MYM | 15 | -1.153 | -1.176 | -1.197 | -1.258 | -1.315 | +0.000 | -0.025 | -0.034 | -0.013 | -0.013 | +0.008 |
| MYM | 60 | -1.911 | -1.538 | -1.512 | -1.557 | -1.525 | +0.000 | +0.031 | +0.051 | +0.024 | -0.003 | -0.232 |

## Calibration

- MES 5-min: 1036271 bars, 79276 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 13176 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 1994 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 65023 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 12717 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 2088 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 27100 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 6099 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1068 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33012 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
