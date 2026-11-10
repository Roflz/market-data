# Impact card: pat_bar_80_20

candle pattern bar_80_20 in its textbook direction: range >= 4 ticks; opens in the top 20% and closes in the bottom 20% -> bullish (fade), mirror bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=0.21; we would catch an effect of 0.011 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.014 R20, CONFIRMED, q=1.28e-11, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.32 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.209 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.008 R20 over the next 2 bars (30 min), p=0.44; we would catch an effect of 0.019 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.08).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.72 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.126 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.030 R20 over the next 8 bars (8 h), p=0.47; we would catch an effect of 0.036 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.19 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.014 R20 over the next 8 bars (40 min), p=0.33; we would catch an effect of 0.013 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.016 R20, CONFIRMED, q=1.64e-12, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.59 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.076 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.016 R20 over the next 2 bars (30 min), p=0.16; we would catch an effect of 0.027 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.019).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.45 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.043 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.026 R20 over the next 2 bars (2 h), p=0.07; we would catch an effect of 0.039 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.083).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.44 at recent bar sizes, 90% range up to $5.31); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.011 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.017 R20 or more 80% of the time).
- MYM 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.014 R20, CONFIRMED, q=7.07e-05, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.26 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.173 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.010 R20 over the next 1 bar (15 min), p=0.44; we would catch an effect of 0.028 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.39).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.73 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.096 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.023 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.054 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.047).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.97 at recent bar sizes, 90% range up to $2.54); about 1.9x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.004 | +0.000 .. +0.008 | +0.0026 | 0.033 / 0.026 / 0.025 | 0.0292 | 1 | 0.997 | 13/16 | +0.007 | +0.002 | False | +2.3 / +2.1 |  |
| MES | 5 | h2 | +0.002 | -0.004 .. +0.008 | +0.0008 | 0.54 / 0.52 / 0.54 | 0.536 |  |  | 8/16 | +0.006 | -0.003 |  | +0.7 / +0.6 |  |
| MES | 5 | h4 | -0.005 | -0.012 .. +0.002 | -0.0014 | 0.18 / 0.19 / 0.2 | 0.2 |  |  | 12/16 | -0.002 | -0.008 |  | -1.3 / -1.4 | 0.011 |
| MES | 5 | h8 | -0.010 | -0.020 .. -0.000 | -0.0019 | 0.047 / 0.062 / 0.072 | 0.0758 |  |  | 13/16 | +0.001 | -0.021 |  | -1.9 / -2.0 |  |
| MES | 5 | h16 | +0.001 | -0.013 .. +0.015 | +0.0001 | 0.9 / 0.9 / 0.92 | 0.921 |  |  | 9/16 | +0.012 | -0.010 |  | +0.1 / +0.1 |  |
| MES | 5 | eod | +0.008 | -0.054 .. +0.071 | +0.0002 | 0.79 / 0.79 / 0.8 | 0.806 |  |  | 8/16 | -0.021 | +0.038 |  | +0.2 / +0.3 |  |
| MES | 15 | h1 | +0.002 | -0.004 .. +0.008 | +0.0011 | 0.56 / 0.56 / 0.56 | 0.57 |  |  | 10/16 | +0.006 | -0.002 |  | +0.6 / +0.6 |  |
| MES | 15 | h2 * | -0.008 | -0.017 .. +0.001 | -0.0033 | 0.072 / 0.069 / 0.091 | 0.0906 | 1 | 1 | 11/16 | -0.003 | -0.014 | False | -1.8 / -1.8 |  |
| MES | 15 | h4 | -0.010 | -0.024 .. +0.003 | -0.0027 | 0.14 / 0.12 / 0.16 | 0.155 |  |  | 10/16 | -0.004 | -0.016 |  | -1.6 / -1.5 | 0.019 |
| MES | 15 | h8 | -0.011 | -0.029 .. +0.008 | -0.0020 | 0.25 / 0.23 / 0.29 | 0.287 |  |  | 8/16 | -0.002 | -0.020 |  | -1.1 / -1.2 |  |
| MES | 15 | h16 | -0.008 | -0.033 .. +0.016 | -0.0011 | 0.51 / 0.51 / 0.56 | 0.568 |  |  | 10/16 | +0.011 | -0.028 |  | -0.6 / -0.7 |  |
| MES | 15 | eod | -0.007 | -0.068 .. +0.053 | -0.0004 | 0.81 / 0.81 / 0.84 | 0.835 |  |  | 8/16 | +0.009 | -0.024 |  | -0.2 / -0.2 |  |
| MES | 60 | h1 | -0.004 | -0.017 .. +0.009 | -0.0023 | 0.57 / 0.58 / 0.56 | 0.546 |  |  | 9/16 | +0.003 | -0.011 |  | -0.6 / -0.6 |  |
| MES | 60 | h2 | -0.012 | -0.030 .. +0.007 | -0.0049 | 0.22 / 0.22 / 0.21 | 0.207 |  |  | 10/16 | -0.012 | -0.011 |  | -1.3 / -1.2 |  |
| MES | 60 | h4 | -0.022 | -0.048 .. +0.003 | -0.0066 | 0.09 / 0.091 / 0.082 | 0.0815 |  |  | 12/16 | -0.019 | -0.025 |  | -1.7 / -1.7 | 0.036 |
| MES | 60 | h8 * | -0.030 | -0.062 .. +0.003 | -0.0065 | 0.071 / 0.077 / 0.096 | 0.0992 | 1 | 1 | 12/16 | -0.028 | -0.031 | False | -1.7 / -1.8 |  |
| MES | 60 | h16 | -0.014 | -0.054 .. +0.027 | -0.0023 | 0.51 / 0.51 / 0.55 | 0.563 |  |  | 10/16 | -0.003 | -0.025 |  | -0.6 / -0.7 |  |
| MES | 60 | eod | -0.020 | -0.062 .. +0.023 | -0.0032 | 0.37 / 0.37 / 0.41 | 0.414 |  |  | 8/16 | -0.017 | -0.022 |  | -0.8 / -0.9 |  |
| MNQ | 5 | h1 | -0.000 | -0.004 .. +0.004 | -0.0001 | 0.95 / 0.95 / 0.91 | 0.899 |  |  | 8/16 | +0.006 | -0.007 |  | -0.1 / -0.1 |  |
| MNQ | 5 | h2 | -0.004 | -0.009 .. +0.002 | -0.0013 | 0.18 / 0.17 / 0.24 | 0.235 |  |  | 10/16 | +0.006 | -0.014 |  | -1.5 / -1.3 |  |
| MNQ | 5 | h4 | -0.008 | -0.015 .. -0.000 | -0.0017 | 0.04 / 0.044 / 0.12 | 0.123 |  |  | 10/16 | +0.002 | -0.018 |  | -2.1 / -2.1 | 0.013 |
| MNQ | 5 | h8 * | -0.014 | -0.024 .. -0.004 | -0.0021 | 0.0055 / 0.0065 / 0.057 | 0.0578 | 1 | 0.725 | 10/16 | +0.001 | -0.029 | False | -2.6 / -2.8 |  |
| MNQ | 5 | h16 | -0.002 | -0.016 .. +0.013 | -0.0002 | 0.81 / 0.82 / 0.85 | 0.843 |  |  | 9/16 | +0.014 | -0.017 |  | -0.2 / -0.2 |  |
| MNQ | 5 | eod | +0.057 | -0.017 .. +0.130 | +0.0012 | 0.13 / 0.15 / 0.21 | 0.215 |  |  | 11/16 | +0.052 | +0.062 |  | +1.3 / +1.5 |  |
| MNQ | 15 | h1 | -0.006 | -0.012 .. +0.001 | -0.0028 | 0.075 / 0.079 / 0.15 | 0.149 |  |  | 11/16 | -0.003 | -0.009 |  | -1.8 / -1.8 |  |
| MNQ | 15 | h2 * | -0.016 | -0.025 .. -0.007 | -0.0045 | 0.00076 / 0.00069 / 0.016 | 0.019 | 1 | 0.226 | 13/16 | -0.011 | -0.021 | False | -3.3 / -3.4 |  |
| MNQ | 15 | h4 | -0.017 | -0.030 .. -0.004 | -0.0029 | 0.0089 / 0.012 / 0.13 | 0.136 |  |  | 11/16 | -0.013 | -0.022 |  | -2.5 / -2.6 | 0.027 |
| MNQ | 15 | h8 | -0.015 | -0.034 .. +0.005 | -0.0019 | 0.15 / 0.15 / 0.33 | 0.326 |  |  | 7/16 | +0.005 | -0.034 |  | -1.4 / -1.4 |  |
| MNQ | 15 | h16 | -0.007 | -0.034 .. +0.021 | -0.0007 | 0.64 / 0.65 / 0.72 | 0.713 |  |  | 8/16 | +0.028 | -0.041 |  | -0.4 / -0.5 |  |
| MNQ | 15 | eod | +0.010 | -0.058 .. +0.078 | +0.0003 | 0.77 / 0.77 / 0.84 | 0.837 |  |  | 8/16 | +0.070 | -0.050 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h1 | -0.018 | -0.032 .. -0.004 | -0.0103 | 0.013 / 0.014 / 0.01 | 0.0104 |  |  | 9/16 | -0.016 | -0.020 |  | -2.7 / -2.5 |  |
| MNQ | 60 | h2 * | -0.026 | -0.046 .. -0.006 | -0.0104 | 0.0098 / 0.012 / 0.0082 | 0.0086 | 1 | 0.859 | 9/16 | -0.022 | -0.031 | False | -2.7 / -2.6 |  |
| MNQ | 60 | h4 | -0.021 | -0.047 .. +0.006 | -0.0058 | 0.12 / 0.12 / 0.14 | 0.146 |  |  | 9/16 | -0.003 | -0.039 |  | -1.5 / -1.5 | 0.039 |
| MNQ | 60 | h8 | -0.027 | -0.063 .. +0.009 | -0.0056 | 0.14 / 0.13 / 0.16 | 0.151 |  |  | 9/16 | -0.007 | -0.048 |  | -1.5 / -1.5 |  |
| MNQ | 60 | h16 | -0.025 | -0.070 .. +0.020 | -0.0039 | 0.28 / 0.27 / 0.31 | 0.316 |  |  | 7/16 | +0.016 | -0.065 |  | -1.0 / -1.1 |  |
| MNQ | 60 | eod | -0.028 | -0.075 .. +0.018 | -0.0042 | 0.23 / 0.23 / 0.28 | 0.279 |  |  | 7/16 | +0.013 | -0.069 |  | -1.1 / -1.2 |  |
| MYM | 5 | h1 | +0.004 | -0.001 .. +0.008 | +0.0019 | 0.14 / 0.14 / 0.28 | 0.286 |  |  | 6/8 | n/a | +0.004 |  | +1.5 / +1.5 |  |
| MYM | 5 | h2 | +0.002 | -0.004 .. +0.009 | +0.0008 | 0.48 / 0.49 / 0.7 | 0.679 |  |  | 4/8 | n/a | +0.002 |  | +0.7 / +0.7 |  |
| MYM | 5 | h4 | +0.001 | -0.009 .. +0.011 | +0.0001 | 0.9 / 0.9 / 0.99 | 0.993 |  |  | 3/8 | n/a | +0.001 |  | +0.1 / +0.1 | 0.017 |
| MYM | 5 | h8 * | -0.011 | -0.025 .. +0.004 | -0.0015 | 0.15 / 0.14 / 0.3 | 0.305 | 1 | 1 | 7/8 | n/a | -0.011 | False | -1.5 / -1.4 |  |
| MYM | 5 | h16 | +0.003 | -0.016 .. +0.023 | +0.0004 | 0.73 / 0.74 / 0.84 | 0.836 |  |  | 5/8 | n/a | +0.003 |  | +0.3 / +0.3 |  |
| MYM | 5 | eod | +0.045 | -0.049 .. +0.140 | +0.0011 | 0.35 / 0.38 / 0.45 | 0.449 |  |  | 5/8 | n/a | +0.045 |  | +0.8 / +0.9 |  |
| MYM | 15 | h1 * | +0.010 | +0.001 .. +0.019 | +0.0051 | 0.026 / 0.026 / 0.063 | 0.069 | 1 | 0.993 | 8/8 | n/a | +0.010 | False | +2.3 / +2.2 |  |
| MYM | 15 | h2 | +0.008 | -0.006 .. +0.022 | +0.0022 | 0.28 / 0.24 / 0.42 | 0.405 |  |  | 5/8 | n/a | +0.008 |  | +1.2 / +1.1 |  |
| MYM | 15 | h4 | +0.010 | -0.009 .. +0.029 | +0.0016 | 0.31 / 0.29 / 0.54 | 0.536 |  |  | 5/8 | n/a | +0.010 |  | +1.0 / +1.0 | 0.028 |
| MYM | 15 | h8 | +0.015 | -0.009 .. +0.039 | +0.0019 | 0.22 / 0.21 / 0.46 | 0.463 |  |  | 6/8 | n/a | +0.015 |  | +1.1 / +1.2 |  |
| MYM | 15 | h16 | +0.018 | -0.016 .. +0.052 | +0.0017 | 0.29 / 0.32 / 0.53 | 0.531 |  |  | 5/8 | n/a | +0.018 |  | +0.9 / +1.1 |  |
| MYM | 15 | eod | +0.065 | -0.037 .. +0.166 | +0.0025 | 0.21 / 0.2 / 0.35 | 0.355 |  |  | 5/8 | n/a | +0.065 |  | +1.3 / +1.3 |  |
| MYM | 60 | h1 | -0.003 | -0.021 .. +0.014 | -0.0021 | 0.7 / 0.72 / 0.73 | 0.731 |  |  | 4/8 | n/a | -0.003 |  | -0.4 / -0.4 |  |
| MYM | 60 | h2 | -0.008 | -0.035 .. +0.019 | -0.0033 | 0.56 / 0.58 / 0.56 | 0.549 |  |  | 4/8 | n/a | -0.008 |  | -0.6 / -0.6 |  |
| MYM | 60 | h4 * | -0.023 | -0.058 .. +0.013 | -0.0065 | 0.21 / 0.23 / 0.23 | 0.229 | 1 | 1 | 5/8 | n/a | -0.023 | False | -1.2 / -1.2 | 0.054 |
| MYM | 60 | h8 | -0.005 | -0.053 .. +0.043 | -0.0011 | 0.83 / 0.83 / 0.84 | 0.839 |  |  | 4/8 | n/a | -0.005 |  | -0.2 / -0.2 |  |
| MYM | 60 | h16 | +0.001 | -0.063 .. +0.065 | +0.0001 | 0.98 / 0.98 / 0.98 | 0.975 |  |  | 3/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 60 | eod | -0.004 | -0.069 .. +0.061 | -0.0007 | 0.91 / 0.91 / 0.91 | 0.912 |  |  | 5/8 | n/a | -0.004 |  | -0.1 / -0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.014 | +0.010 .. +0.017 | +2.8% | +0.041 | 3.2e-14 | 1.28e-11 | 14/16 |
| MES | 5 | h2 | +0.015 | +0.010 .. +0.020 | +2.2% | +0.041 | 1.7e-09 |  | 13/16 |
| MES | 5 | h4 | +0.020 | +0.013 .. +0.027 | +2.0% | +0.045 | 5.3e-08 |  | 14/16 |
| MES | 5 | h8 | +0.023 | +0.011 .. +0.036 | +1.6% | +0.046 | 0.00025 |  | 15/16 |
| MES | 5 | h16 | +0.024 | +0.005 .. +0.042 | +1.1% | +0.048 | 0.012 |  | 12/16 |
| MES | 5 | eod | +0.015 | -0.173 .. +0.204 | +0.2% | -0.116 | 0.87 |  | 9/16 |
| MES | 15 | h1 | +0.006 | +0.001 .. +0.011 | +1.1% | +0.020 | 0.025 |  | 12/16 |
| MES | 15 | h2 | +0.010 | +0.002 .. +0.018 | +1.3% | +0.024 | 0.014 |  | 13/16 |
| MES | 15 | h4 * | +0.016 | +0.003 .. +0.028 | +1.5% | +0.026 | 0.013 | 1 | 12/16 |
| MES | 15 | h8 | +0.020 | +0.001 .. +0.038 | +1.3% | +0.024 | 0.041 |  | 11/16 |
| MES | 15 | h16 | +0.013 | -0.017 .. +0.042 | +0.6% | +0.015 | 0.39 |  | 12/16 |
| MES | 15 | eod | +0.001 | -0.129 .. +0.130 | +0.0% | -0.012 | 0.99 |  | 9/16 |
| MES | 60 | h1 | +0.002 | -0.008 .. +0.012 | +0.4% | +0.019 | 0.98 |  | 8/16 |
| MES | 60 | h2 | +0.003 | -0.010 .. +0.015 | +0.4% | +0.023 | 0.97 |  | 7/16 |
| MES | 60 | h4 * | +0.007 | -0.011 .. +0.024 | +0.6% | +0.023 | 0.45 | 1 | 10/16 |
| MES | 60 | h8 | +0.000 | -0.023 .. +0.024 | +0.0% | +0.010 | 0.98 |  | 10/16 |
| MES | 60 | h16 | -0.005 | -0.037 .. +0.027 | -0.2% | -0.002 | 0.86 |  | 6/16 |
| MES | 60 | eod | -0.006 | -0.038 .. +0.026 | -0.3% | -0.004 | 0.93 |  | 7/16 |
| MNQ | 5 | h1 * | +0.016 | +0.013 .. +0.020 | +3.1% | +0.045 | 3.9e-15 | 1.64e-12 | 14/16 |
| MNQ | 5 | h2 | +0.015 | +0.008 .. +0.021 | +1.9% | +0.039 | 2e-05 |  | 13/16 |
| MNQ | 5 | h4 | +0.013 | +0.001 .. +0.025 | +1.2% | +0.036 | 0.035 |  | 13/16 |
| MNQ | 5 | h8 | +0.017 | -0.008 .. +0.042 | +1.0% | +0.037 | 0.18 |  | 13/16 |
| MNQ | 5 | h16 | +0.034 | -0.011 .. +0.079 | +1.4% | +0.047 | 0.14 |  | 15/16 |
| MNQ | 5 | eod | -0.133 | -0.396 .. +0.130 | -1.1% | -0.466 | 0.32 |  | 7/16 |
| MNQ | 15 | h1 * | +0.010 | +0.004 .. +0.016 | +1.9% | +0.026 | 0.0031 | 0.481 | 13/16 |
| MNQ | 15 | h2 | +0.013 | -0.000 .. +0.026 | +1.7% | +0.027 | 0.058 |  | 12/16 |
| MNQ | 15 | h4 | +0.026 | -0.003 .. +0.055 | +2.3% | +0.041 | 0.08 |  | 15/16 |
| MNQ | 15 | h8 | +0.033 | -0.013 .. +0.079 | +2.0% | +0.050 | 0.16 |  | 13/16 |
| MNQ | 15 | h16 | +0.032 | -0.021 .. +0.084 | +1.3% | +0.058 | 0.23 |  | 13/16 |
| MNQ | 15 | eod | +0.033 | -0.184 .. +0.251 | +0.5% | +0.059 | 0.77 |  | 13/16 |
| MNQ | 60 | h1 | +0.004 | -0.006 .. +0.014 | +0.7% | +0.017 | 0.48 |  | 9/16 |
| MNQ | 60 | h2 * | +0.017 | +0.003 .. +0.030 | +2.2% | +0.025 | 0.014 | 1 | 12/16 |
| MNQ | 60 | h4 | +0.020 | +0.001 .. +0.040 | +1.9% | +0.035 | 0.043 |  | 11/16 |
| MNQ | 60 | h8 | +0.015 | -0.011 .. +0.040 | +0.9% | +0.021 | 0.3 |  | 11/16 |
| MNQ | 60 | h16 | +0.022 | -0.013 .. +0.057 | +1.0% | +0.025 | 0.23 |  | 10/16 |
| MNQ | 60 | eod | +0.016 | -0.020 .. +0.052 | +0.7% | +0.028 | 0.39 |  | 10/16 |
| MYM | 5 | h1 * | +0.014 | +0.009 .. +0.019 | +2.6% | +0.034 | 2.8e-07 | 7.07e-05 | 7/8 |
| MYM | 5 | h2 | +0.014 | +0.004 .. +0.024 | +1.8% | +0.032 | 0.0043 |  | 7/8 |
| MYM | 5 | h4 | +0.014 | -0.008 .. +0.036 | +1.2% | +0.028 | 0.22 |  | 7/8 |
| MYM | 5 | h8 | +0.013 | -0.029 .. +0.054 | +0.8% | +0.025 | 0.56 |  | 6/8 |
| MYM | 5 | h16 | +0.026 | -0.031 .. +0.082 | +1.1% | +0.036 | 0.38 |  | 6/8 |
| MYM | 5 | eod | +0.020 | -0.249 .. +0.289 | +0.2% | +0.047 | 1 |  | 7/8 |
| MYM | 15 | h1 * | +0.010 | +0.002 .. +0.017 | +1.8% | +0.022 | 0.065 | 1 | 6/8 |
| MYM | 15 | h2 | +0.008 | -0.009 .. +0.026 | +1.1% | +0.020 | 0.6 |  | 6/8 |
| MYM | 15 | h4 | +0.018 | -0.017 .. +0.052 | +1.6% | +0.023 | 0.47 |  | 7/8 |
| MYM | 15 | h8 | +0.004 | -0.050 .. +0.059 | +0.3% | +0.012 | 0.92 |  | 6/8 |
| MYM | 15 | h16 | +0.014 | -0.082 .. +0.110 | +0.6% | +0.022 | 0.78 |  | 4/8 |
| MYM | 15 | eod | -0.026 | -0.278 .. +0.226 | -0.4% | -0.002 | 0.84 |  | 3/8 |
| MYM | 60 | h1 | +0.015 | +0.001 .. +0.030 | +2.9% | +0.030 | 0.044 |  | 6/8 |
| MYM | 60 | h2 * | +0.026 | +0.007 .. +0.046 | +3.5% | +0.053 | 0.0078 | 1 | 6/8 |
| MYM | 60 | h4 | +0.019 | -0.009 .. +0.047 | +1.8% | +0.039 | 0.18 |  | 5/8 |
| MYM | 60 | h8 | +0.017 | -0.017 .. +0.051 | +1.1% | +0.034 | 0.34 |  | 6/8 |
| MYM | 60 | h16 | +0.036 | -0.008 .. +0.081 | +1.7% | +0.040 | 0.24 |  | 7/8 |
| MYM | 60 | eod | +0.014 | -0.033 .. +0.061 | +0.6% | +0.017 | 0.66 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.18 pts | -0.44 .. +0.08 | 0.19 |
| MES | 15 | -0.10 pts | -0.48 .. +0.29 | 0.62 |
| MES | 60 | -0.39 pts | -1.12 .. +0.34 | 0.37 |
| MNQ | 5 | +0.07 pts | -0.16 .. +0.31 | 0.81 |
| MNQ | 15 | -0.23 pts | -0.59 .. +0.13 | 0.31 |
| MNQ | 60 | -0.62 pts | -1.29 .. +0.06 | 0.091 |
| MYM | 5 | +0.01 pts | -0.31 .. +0.33 | 0.95 |
| MYM | 15 | +0.65 pts | +0.14 .. +1.15 | 0.012 |
| MYM | 60 | -0.33 pts | -1.34 .. +0.68 | 0.53 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 149878 | +0.016 | 0.262 | +0.17 | -3.33 | -3.35 | -3.31 | -3.48 |
| MES | 5 | h2 | event | with signal | 149878 | +0.018 | 0.262 | +0.25 | -3.25 | -3.30 | -3.23 | -3.47 |
| MES | 5 | h4 | event | against signal | 149878 | -0.011 | 0.262 | -0.14 | -3.64 | -3.62 | -3.66 | -3.43 |
| MES | 5 | h8 | event | against signal | 149878 | -0.004 | 0.262 | -0.05 | -3.55 | -3.64 | -3.49 | -3.36 |
| MES | 5 | h16 | event | with signal | 149878 | +0.016 | 0.262 | +0.17 | -3.33 | -3.28 | -3.36 | -3.54 |
| MES | 5 | eod | event | with signal | 149878 | -0.000 | 0.262 | +0.01 | -3.49 | -3.85 | -3.28 | -3.37 |
| MES | 15 | h1 | event | with signal | 58147 | +0.010 | 0.173 | +0.13 | -3.37 | -3.36 | -3.37 | -3.53 |
| MES | 15 | h2 | event | against signal | 58147 | -0.001 | 0.173 | +0.04 | -3.46 | -3.55 | -3.39 | -3.27 |
| MES | 15 | h4 | event | against signal | 58147 | +0.002 | 0.173 | +0.12 | -3.38 | -3.53 | -3.27 | -3.20 |
| MES | 15 | h8 | event | against signal | 58147 | +0.002 | 0.173 | +0.05 | -3.45 | -3.52 | -3.39 | -3.26 |
| MES | 15 | h16 | event | against signal | 58147 | +0.000 | 0.173 | -0.01 | -3.51 | -3.62 | -3.42 | -3.33 |
| MES | 15 | eod | event | against signal | 58147 | +0.031 | 0.173 | +0.33 | -3.17 | -3.22 | -3.13 | -3.64 |
| MES | 60 | h1 | event | against signal | 14709 | +0.004 | 0.091 | +0.12 | -3.38 | -3.41 | -3.36 | -3.39 |
| MES | 60 | h2 | event | against signal | 14709 | +0.011 | 0.091 | +0.26 | -3.24 | -3.16 | -3.30 | -3.18 |
| MES | 60 | h4 | event | against signal | 14709 | +0.021 | 0.091 | +0.22 | -3.28 | -3.20 | -3.35 | -3.19 |
| MES | 60 | h8 | event | against signal | 14709 | +0.030 | 0.091 | +1.16 | -2.34 | -2.78 | -1.93 | -2.25 |
| MES | 60 | h16 | event | against signal | 14709 | +0.026 | 0.091 | +1.25 | -2.25 | -2.95 | -1.59 | -2.62 |
| MES | 60 | eod | event | against signal | 14709 | +0.029 | 0.091 | +1.22 | -2.28 | -2.84 | -1.76 | -2.53 |
| MNQ | 5 | h1 | event | against signal | 187167 | -0.004 | 0.126 | -0.02 | -2.02 | -2.06 | -1.99 | -1.95 |
| MNQ | 5 | h2 | event | against signal | 187167 | -0.004 | 0.126 | -0.06 | -2.06 | -2.07 | -2.06 | -1.94 |
| MNQ | 5 | h4 | event | against signal | 187167 | +0.003 | 0.126 | +0.06 | -1.94 | -2.03 | -1.86 | -1.87 |
| MNQ | 5 | h8 | event | against signal | 187167 | +0.017 | 0.126 | +0.11 | -1.89 | -2.02 | -1.77 | -1.93 |
| MNQ | 5 | h16 | event | against signal | 187167 | +0.008 | 0.126 | -0.02 | -2.02 | -2.02 | -2.01 | -2.12 |
| MNQ | 5 | eod | event | with signal | 187167 | +0.024 | 0.126 | +0.21 | -1.79 | -2.01 | -1.57 | -1.31 |
| MNQ | 15 | h1 | event | against signal | 63002 | +0.003 | 0.075 | +0.02 | -1.98 | -2.01 | -1.95 | -1.89 |
| MNQ | 15 | h2 | event | against signal | 63002 | +0.015 | 0.075 | +0.29 | -1.71 | -1.92 | -1.49 | -1.67 |
| MNQ | 15 | h4 | event | against signal | 63002 | +0.018 | 0.075 | +0.29 | -1.71 | -1.87 | -1.55 | -1.73 |
| MNQ | 15 | h8 | event | against signal | 63002 | +0.022 | 0.075 | +0.63 | -1.37 | -1.89 | -0.80 | -1.54 |
| MNQ | 15 | h16 | event | against signal | 63002 | +0.013 | 0.075 | +0.54 | -1.46 | -2.00 | -0.87 | -1.58 |
| MNQ | 15 | eod | event | with signal | 63002 | -0.026 | 0.075 | -0.93 | -2.93 | -1.83 | -4.12 | -2.15 |
| MNQ | 60 | h1 | event | against signal | 14987 | +0.020 | 0.037 | +0.84 | -1.16 | -1.56 | -0.74 | -1.23 |
| MNQ | 60 | h2 | event | against signal | 14987 | +0.028 | 0.037 | +1.29 | -0.71 | -1.44 | +0.06 | -0.69 |
| MNQ | 60 | h4 | event | against signal | 14987 | +0.022 | 0.037 | +1.09 | -0.91 | -1.87 | +0.10 | -0.84 |
| MNQ | 60 | h8 | event | against signal | 14987 | +0.032 | 0.037 | +2.48 | +0.48 | -1.33 | +2.39 | +0.50 |
| MNQ | 60 | h16 | event | against signal | 14987 | +0.042 | 0.037 | +4.24 | +2.24 | -1.71 | +6.40 | +1.81 |
| MNQ | 60 | eod | event | against signal | 14987 | +0.044 | 0.037 | +4.37 | +2.37 | -1.79 | +6.75 | +2.04 |
| MYM | 5 | h1 | event | with signal | 105993 | +0.011 | 0.173 | +0.09 | -1.91 | +nan | -1.91 | -2.00 |
| MYM | 5 | h2 | event | with signal | 105993 | +0.012 | 0.173 | +0.15 | -1.85 | +nan | -1.85 | -1.95 |
| MYM | 5 | h4 | event | with signal | 105993 | +0.010 | 0.173 | +0.06 | -1.94 | +nan | -1.94 | -2.05 |
| MYM | 5 | h8 | event | against signal | 105993 | +0.001 | 0.173 | +0.03 | -1.97 | +nan | -1.97 | -1.87 |
| MYM | 5 | h16 | event | with signal | 105993 | +0.017 | 0.173 | +0.12 | -1.88 | +nan | -1.88 | -2.03 |
| MYM | 5 | eod | event | with signal | 105993 | +0.058 | 0.173 | +0.27 | -1.73 | +nan | -1.73 | -1.89 |
| MYM | 15 | h1 | event | with signal | 32307 | +0.016 | 0.096 | +0.24 | -1.76 | +nan | -1.76 | -1.87 |
| MYM | 15 | h2 | event | with signal | 32307 | +0.013 | 0.096 | +0.21 | -1.79 | +nan | -1.79 | -1.89 |
| MYM | 15 | h4 | event | with signal | 32307 | +0.011 | 0.096 | +0.13 | -1.87 | +nan | -1.87 | -1.91 |
| MYM | 15 | h8 | event | with signal | 32307 | +0.017 | 0.096 | +0.36 | -1.64 | +nan | -1.64 | -1.68 |
| MYM | 15 | h16 | event | with signal | 32307 | +0.014 | 0.096 | +0.49 | -1.51 | +nan | -1.51 | -1.42 |
| MYM | 15 | eod | event | with signal | 32307 | +0.057 | 0.096 | +0.75 | -1.25 | +nan | -1.25 | -1.13 |
| MYM | 60 | h1 | event | against signal | 7416 | +0.005 | 0.047 | -0.27 | -2.27 | +nan | -2.27 | -2.31 |
| MYM | 60 | h2 | event | against signal | 7416 | +0.004 | 0.047 | -0.21 | -2.21 | +nan | -2.21 | -2.02 |
| MYM | 60 | h4 | event | against signal | 7416 | +0.018 | 0.047 | +0.17 | -1.83 | +nan | -1.83 | -1.59 |
| MYM | 60 | h8 | event | against signal | 7416 | +0.001 | 0.047 | +0.36 | -1.64 | +nan | -1.64 | -1.41 |
| MYM | 60 | h16 | event | with signal | 7416 | -0.011 | 0.047 | -0.83 | -2.83 | +nan | -2.83 | -2.36 |
| MYM | 60 | eod | event | against signal | 7416 | +0.016 | 0.047 | +1.02 | -0.98 | +nan | -0.98 | -1.43 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.839 | +0.918 | +0.969 | +1.015 | +1.070 | +0.000 | +0.036 | +0.039 | +0.033 | +0.027 | +0.042 |
| MES | 15 | +0.855 | +0.902 | +0.949 | +0.986 | +1.042 | +0.000 | +0.023 | +0.014 | +0.014 | +0.015 | +0.022 |
| MES | 60 | +1.362 | +1.130 | +1.034 | +1.029 | +1.040 | +0.000 | +0.001 | -0.003 | -0.005 | +0.029 | +0.061 |
| MNQ | 5 | +0.850 | +0.927 | +0.979 | +1.027 | +1.080 | +0.000 | +0.021 | +0.020 | +0.014 | +0.001 | +0.013 |
| MNQ | 15 | +0.886 | +0.927 | +0.967 | +1.004 | +1.054 | +0.000 | +0.005 | -0.006 | -0.010 | -0.012 | +0.005 |
| MNQ | 60 | +1.417 | +1.181 | +1.061 | +1.053 | +1.060 | +0.000 | -0.017 | -0.021 | -0.011 | +0.015 | +0.032 |
| MYM | 5 | +0.782 | +0.856 | +0.917 | +0.966 | +1.023 | +0.000 | +0.023 | +0.024 | +0.023 | +0.012 | +0.030 |
| MYM | 15 | +0.841 | +0.886 | +0.938 | +0.982 | +1.033 | +0.000 | +0.019 | +0.016 | +0.014 | +0.020 | +0.013 |
| MYM | 60 | +1.320 | +1.158 | +1.070 | +1.083 | +1.082 | +0.000 | -0.005 | -0.007 | -0.015 | +0.031 | +0.001 |

## Calibration

- MES 5-min: 1036271 bars, 149878 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 58147 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 14709 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 187167 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 63002 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 14987 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 105993 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 32307 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 7416 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39249 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
