# Impact card: pat_inside_bar_breakout

candle pattern inside_bar_breakout in its textbook direction: first close beyond the mother bar's high/low within 3 bars after an inside bar [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.022 R20 over the next 4 bars (20 min), p=0.023; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.14).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.64 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.190 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.019 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.41 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.120 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.014 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.063 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.2).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.38 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.061 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.018 R20 over the next 4 bars (20 min), p=0.16; we would catch an effect of 0.018 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.24).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.98 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.077 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.037 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.038 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.61 at recent bar sizes, 90% range up to $2.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.038 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.062 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.46 at recent bar sizes, 90% range up to $7.95); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.94).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.39 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.162 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.009 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.050 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.16 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.095 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.026 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.084 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.10 at recent bar sizes, 90% range up to $3.34); about 3.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.010 | -0.017 .. -0.003 | -0.0029 | 0.0051 / 0.0037 / 0.0062 | 0.00625 |  |  | 14/16 | -0.010 | -0.010 |  | -2.9 / -2.8 |  |
| MES | 5 | h2 | -0.015 | -0.025 .. -0.005 | -0.0030 | 0.0035 / 0.0034 / 0.0043 | 0.00573 |  |  | 13/16 | -0.018 | -0.012 |  | -3.0 / -2.9 |  |
| MES | 5 | h4 * | -0.022 | -0.036 .. -0.009 | -0.0031 | 0.0015 / 0.00089 / 0.0033 | 0.00313 | 0.591 | 0.335 | 14/16 | -0.028 | -0.016 | False | -3.2 / -3.2 | 0.020 |
| MES | 5 | h8 | -0.019 | -0.038 .. -0.000 | -0.0018 | 0.047 / 0.048 / 0.084 | 0.081 |  |  | 12/16 | -0.034 | -0.004 |  | -1.9 / -2.0 |  |
| MES | 5 | h16 | -0.021 | -0.049 .. +0.006 | -0.0014 | 0.13 / 0.13 / 0.16 | 0.164 |  |  | 13/16 | -0.041 | -0.002 |  | -1.5 / -1.5 |  |
| MES | 5 | eod | -0.016 | -0.140 .. +0.107 | -0.0002 | 0.79 / 0.79 / 0.81 | 0.806 |  |  | 8/16 | -0.020 | -0.013 |  | -0.2 / -0.3 |  |
| MES | 15 | h1 | -0.000 | -0.012 .. +0.011 | +0.0000 | 0.99 / 0.99 / 0.98 | 0.984 |  |  | 8/16 | +0.003 | -0.004 |  | -0.0 / -0.0 |  |
| MES | 15 | h2 | +0.000 | -0.016 .. +0.016 | +0.0001 | 0.98 / 0.98 / 0.99 | 0.985 |  |  | 8/16 | +0.002 | -0.001 |  | +0.0 / +0.0 |  |
| MES | 15 | h4 | -0.009 | -0.032 .. +0.014 | -0.0013 | 0.44 / 0.45 / 0.5 | 0.496 |  |  | 10/16 | -0.016 | -0.002 |  | -0.8 / -0.8 | 0.038 |
| MES | 15 | h8 * | -0.019 | -0.054 .. +0.015 | -0.0019 | 0.27 / 0.27 / 0.3 | 0.298 | 1 | 1 | 8/16 | -0.018 | -0.021 | False | -1.1 / -1.1 |  |
| MES | 15 | h16 | -0.012 | -0.059 .. +0.035 | -0.0008 | 0.63 / 0.63 / 0.66 | 0.663 |  |  | 8/16 | -0.050 | +0.027 |  | -0.5 / -0.5 |  |
| MES | 15 | eod | +0.022 | -0.092 .. +0.135 | +0.0006 | 0.71 / 0.71 / 0.73 | 0.728 |  |  | 8/16 | +0.019 | +0.025 |  | +0.4 / +0.4 |  |
| MES | 60 | h1 * | -0.014 | -0.035 .. +0.007 | -0.0048 | 0.18 / 0.18 / 0.22 | 0.214 | 1 | 1 | 11/16 | -0.004 | -0.025 | False | -1.3 / -1.3 |  |
| MES | 60 | h2 | -0.002 | -0.031 .. +0.028 | -0.0003 | 0.91 / 0.92 / 0.92 | 0.916 |  |  | 11/16 | +0.018 | -0.021 |  | -0.1 / -0.1 |  |
| MES | 60 | h4 | +0.021 | -0.019 .. +0.061 | +0.0037 | 0.29 / 0.32 / 0.35 | 0.353 |  |  | 9/16 | +0.048 | -0.005 |  | +1.0 / +1.0 | 0.063 |
| MES | 60 | h8 | +0.012 | -0.044 .. +0.067 | +0.0015 | 0.68 / 0.69 / 0.71 | 0.71 |  |  | 9/16 | +0.053 | -0.030 |  | +0.4 / +0.4 |  |
| MES | 60 | h16 | +0.033 | -0.033 .. +0.100 | +0.0032 | 0.33 / 0.33 / 0.4 | 0.401 |  |  | 10/16 | +0.051 | +0.016 |  | +0.9 / +1.0 |  |
| MES | 60 | eod | +0.032 | -0.037 .. +0.101 | +0.0029 | 0.37 / 0.38 / 0.43 | 0.433 |  |  | 9/16 | +0.055 | +0.009 |  | +0.8 / +0.9 |  |
| MNQ | 5 | h1 | -0.008 | -0.013 .. -0.002 | -0.0024 | 0.0075 / 0.0073 / 0.027 | 0.0326 |  |  | 12/16 | -0.001 | -0.014 |  | -2.7 / -2.7 |  |
| MNQ | 5 | h2 | -0.011 | -0.019 .. -0.003 | -0.0022 | 0.0056 / 0.0056 / 0.043 | 0.0474 |  |  | 10/16 | -0.004 | -0.018 |  | -2.7 / -2.8 |  |
| MNQ | 5 | h4 * | -0.018 | -0.029 .. -0.006 | -0.0022 | 0.0032 / 0.0032 / 0.034 | 0.0372 | 1 | 0.55 | 13/16 | -0.006 | -0.029 | False | -3.0 / -2.9 | 0.018 |
| MNQ | 5 | h8 | -0.022 | -0.040 .. -0.005 | -0.0019 | 0.011 / 0.011 / 0.068 | 0.0701 |  |  | 12/16 | -0.018 | -0.027 |  | -2.6 / -2.5 |  |
| MNQ | 5 | h16 | -0.027 | -0.053 .. -0.002 | -0.0016 | 0.036 / 0.039 / 0.12 | 0.12 |  |  | 12/16 | -0.005 | -0.049 |  | -2.1 / -2.1 |  |
| MNQ | 5 | eod | -0.051 | -0.176 .. +0.075 | -0.0006 | 0.43 / 0.44 / 0.52 | 0.53 |  |  | 11/16 | -0.045 | -0.057 |  | -0.7 / -0.8 |  |
| MNQ | 15 | h1 | +0.003 | -0.008 .. +0.013 | +0.0007 | 0.63 / 0.61 / 0.69 | 0.66 |  |  | 9/16 | -0.001 | +0.006 |  | +0.5 / +0.5 |  |
| MNQ | 15 | h2 | +0.000 | -0.014 .. +0.015 | +0.0000 | 0.99 / 0.99 / 0.99 | 0.993 |  |  | 8/16 | -0.008 | +0.008 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h4 | -0.016 | -0.037 .. +0.005 | -0.0016 | 0.14 / 0.14 / 0.39 | 0.364 |  |  | 11/16 | -0.008 | -0.023 |  | -1.5 / -1.5 | 0.038 |
| MNQ | 15 | h8 | -0.020 | -0.052 .. +0.011 | -0.0016 | 0.21 / 0.2 / 0.4 | 0.383 |  |  | 9/16 | -0.006 | -0.034 |  | -1.3 / -1.3 |  |
| MNQ | 15 | h16 * | -0.037 | -0.082 .. +0.009 | -0.0023 | 0.12 / 0.12 / 0.22 | 0.211 | 1 | 1 | 13/16 | -0.017 | -0.056 | False | -1.6 / -1.6 |  |
| MNQ | 15 | eod | +0.027 | -0.080 .. +0.135 | +0.0006 | 0.62 / 0.62 / 0.73 | 0.737 |  |  | 8/16 | +0.064 | -0.009 |  | +0.5 / +0.5 |  |
| MNQ | 60 | h1 | +0.014 | -0.006 .. +0.035 | +0.0051 | 0.18 / 0.19 / 0.2 | 0.206 |  |  | 10/16 | +0.002 | +0.027 |  | +1.3 / +1.4 |  |
| MNQ | 60 | h2 | +0.009 | -0.022 .. +0.039 | +0.0022 | 0.58 / 0.59 / 0.59 | 0.597 |  |  | 10/16 | -0.005 | +0.022 |  | +0.5 / +0.5 |  |
| MNQ | 60 | h4 | -0.016 | -0.059 .. +0.028 | -0.0027 | 0.48 / 0.47 / 0.48 | 0.484 |  |  | 11/16 | -0.030 | -0.001 |  | -0.7 / -0.7 | 0.062 |
| MNQ | 60 | h8 * | -0.038 | -0.095 .. +0.019 | -0.0049 | 0.19 / 0.2 / 0.21 | 0.221 | 1 | 1 | 8/16 | -0.057 | -0.019 | False | -1.3 / -1.3 |  |
| MNQ | 60 | h16 | +0.004 | -0.070 .. +0.078 | +0.0004 | 0.92 / 0.91 / 0.92 | 0.913 |  |  | 7/16 | +0.004 | +0.004 |  | +0.1 / +0.1 |  |
| MNQ | 60 | eod | -0.005 | -0.080 .. +0.070 | -0.0004 | 0.9 / 0.9 / 0.9 | 0.899 |  |  | 9/16 | -0.012 | +0.002 |  | -0.1 / -0.1 |  |
| MYM | 5 | h1 | -0.001 | -0.009 .. +0.006 | -0.0004 | 0.7 / 0.72 / 0.84 | 0.817 |  |  | 4/8 | n/a | -0.001 |  | -0.3 / -0.4 |  |
| MYM | 5 | h2 * | -0.011 | -0.020 .. -0.001 | -0.0019 | 0.026 / 0.04 / 0.23 | 0.217 | 1 | 0.992 | 5/8 | n/a | -0.011 | False | -1.9 / -2.2 |  |
| MYM | 5 | h4 | -0.011 | -0.025 .. +0.002 | -0.0013 | 0.099 / 0.12 / 0.42 | 0.4 |  |  | 7/8 | n/a | -0.011 |  | -1.4 / -1.7 | 0.039 |
| MYM | 5 | h8 | -0.009 | -0.028 .. +0.011 | -0.0007 | 0.38 / 0.41 / 0.66 | 0.636 |  |  | 6/8 | n/a | -0.009 |  | -0.7 / -0.9 |  |
| MYM | 5 | h16 | -0.014 | -0.043 .. +0.015 | -0.0009 | 0.35 / 0.36 / 0.55 | 0.537 |  |  | 4/8 | n/a | -0.014 |  | -0.8 / -0.9 |  |
| MYM | 5 | eod | -0.001 | -0.181 .. +0.178 | -0.0000 | 0.99 / 0.99 / 0.98 | 0.983 |  |  | 5/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |
| MYM | 15 | h1 * | -0.009 | -0.023 .. +0.004 | -0.0029 | 0.16 / 0.18 / 0.31 | 0.309 | 1 | 1 | 5/8 | n/a | -0.009 | False | -1.4 / -1.4 |  |
| MYM | 15 | h2 | -0.007 | -0.028 .. +0.014 | -0.0012 | 0.52 / 0.53 / 0.66 | 0.644 |  |  | 5/8 | n/a | -0.007 |  | -0.7 / -0.6 |  |
| MYM | 15 | h4 | -0.030 | -0.060 .. +0.001 | -0.0031 | 0.058 / 0.049 / 0.24 | 0.223 |  |  | 6/8 | n/a | -0.030 |  | -2.1 / -1.9 | 0.050 |
| MYM | 15 | h8 | -0.018 | -0.059 .. +0.023 | -0.0014 | 0.39 / 0.4 / 0.56 | 0.54 |  |  | 6/8 | n/a | -0.018 |  | -0.9 / -0.9 |  |
| MYM | 15 | h16 | -0.026 | -0.084 .. +0.032 | -0.0015 | 0.37 / 0.4 / 0.56 | 0.54 |  |  | 5/8 | n/a | -0.026 |  | -0.8 / -0.9 |  |
| MYM | 15 | eod | -0.006 | -0.153 .. +0.142 | -0.0001 | 0.94 / 0.94 / 0.96 | 0.95 |  |  | 4/8 | n/a | -0.006 |  | -0.1 / -0.1 |  |
| MYM | 60 | h1 | +0.018 | -0.011 .. +0.047 | +0.0066 | 0.23 / 0.23 / 0.24 | 0.229 |  |  | 6/8 | n/a | +0.018 |  | +1.2 / +1.2 |  |
| MYM | 60 | h2 * | +0.026 | -0.016 .. +0.068 | +0.0065 | 0.23 / 0.23 / 0.24 | 0.238 | 1 | 1 | 5/8 | n/a | +0.026 | False | +1.2 / +1.2 |  |
| MYM | 60 | h4 | +0.021 | -0.036 .. +0.077 | +0.0038 | 0.48 / 0.48 / 0.49 | 0.486 |  |  | 4/8 | n/a | +0.021 |  | +0.7 / +0.7 | 0.084 |
| MYM | 60 | h8 | +0.010 | -0.072 .. +0.091 | +0.0013 | 0.82 / 0.81 / 0.82 | 0.827 |  |  | 4/8 | n/a | +0.010 |  | +0.3 / +0.2 |  |
| MYM | 60 | h16 | +0.022 | -0.072 .. +0.117 | +0.0023 | 0.64 / 0.66 / 0.67 | 0.665 |  |  | 3/8 | n/a | +0.022 |  | +0.5 / +0.5 |  |
| MYM | 60 | eod | +0.009 | -0.088 .. +0.106 | +0.0009 | 0.86 / 0.86 / 0.88 | 0.868 |  |  | 3/8 | n/a | +0.009 |  | +0.2 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.000 | -0.005 .. +0.005 | -0.0% | +0.020 | 0.99 |  | 9/16 |
| MES | 5 | h2 | +0.001 | -0.006 .. +0.008 | +0.1% | +0.019 | 0.83 |  | 9/16 |
| MES | 5 | h4 | +0.002 | -0.008 .. +0.011 | +0.2% | +0.011 | 0.93 |  | 8/16 |
| MES | 5 | h8 | +0.003 | -0.012 .. +0.018 | +0.2% | +0.008 | 0.99 |  | 9/16 |
| MES | 5 | h16 | +0.007 | -0.016 .. +0.029 | +0.3% | -0.005 | 0.97 |  | 9/16 |
| MES | 5 | eod * | -0.228 | -0.423 .. -0.032 | -2.3% | -0.489 | 0.023 | 1 | 9/16 |
| MES | 15 | h1 | +0.003 | -0.005 .. +0.011 | +0.6% | +0.008 | 0.73 |  | 8/16 |
| MES | 15 | h2 * | +0.007 | -0.005 .. +0.019 | +1.0% | +0.012 | 0.53 | 1 | 9/16 |
| MES | 15 | h4 | +0.005 | -0.013 .. +0.023 | +0.5% | +0.012 | 0.77 |  | 10/16 |
| MES | 15 | h8 | -0.007 | -0.033 .. +0.019 | -0.4% | -0.001 | 0.61 |  | 9/16 |
| MES | 15 | h16 | +0.006 | -0.034 .. +0.047 | +0.3% | -0.008 | 0.76 |  | 8/16 |
| MES | 15 | eod | -0.033 | -0.160 .. +0.095 | -0.6% | -0.102 | 0.62 |  | 6/16 |
| MES | 60 | h1 | -0.002 | -0.017 .. +0.013 | -0.4% | -0.004 | 0.96 |  | 7/16 |
| MES | 60 | h2 | +0.009 | -0.013 .. +0.031 | +1.2% | +0.003 | 0.44 |  | 6/16 |
| MES | 60 | h4 | -0.008 | -0.038 .. +0.022 | -0.8% | -0.009 | 0.84 |  | 7/16 |
| MES | 60 | h8 | -0.014 | -0.047 .. +0.018 | -1.0% | -0.006 | 0.42 |  | 12/16 |
| MES | 60 | h16 * | -0.047 | -0.090 .. -0.004 | -2.3% | -0.059 | 0.033 | 1 | 13/16 |
| MES | 60 | eod | -0.043 | -0.087 .. +0.001 | -2.0% | -0.064 | 0.056 |  | 12/16 |
| MNQ | 5 | h1 * | +0.008 | +0.003 .. +0.012 | +1.4% | +0.025 | 0.039 | 1 | 12/16 |
| MNQ | 5 | h2 | +0.006 | -0.001 .. +0.013 | +0.7% | +0.022 | 0.39 |  | 11/16 |
| MNQ | 5 | h4 | +0.004 | -0.008 .. +0.016 | +0.4% | +0.014 | 0.83 |  | 12/16 |
| MNQ | 5 | h8 | -0.002 | -0.025 .. +0.022 | -0.1% | +0.004 | 0.88 |  | 4/16 |
| MNQ | 5 | h16 | -0.007 | -0.050 .. +0.037 | -0.3% | -0.011 | 0.77 |  | 4/16 |
| MNQ | 5 | eod | -0.219 | -0.465 .. +0.027 | -1.7% | -0.492 | 0.081 |  | 11/16 |
| MNQ | 15 | h1 | +0.001 | -0.006 .. +0.009 | +0.3% | +0.010 | 0.71 |  | 8/16 |
| MNQ | 15 | h2 | +0.004 | -0.010 .. +0.018 | +0.5% | +0.011 | 0.8 |  | 12/16 |
| MNQ | 15 | h4 | +0.006 | -0.024 .. +0.036 | +0.5% | +0.005 | 0.89 |  | 12/16 |
| MNQ | 15 | h8 | +0.001 | -0.044 .. +0.046 | +0.1% | -0.014 | 0.97 |  | 10/16 |
| MNQ | 15 | h16 | -0.018 | -0.069 .. +0.033 | -0.7% | -0.051 | 0.54 |  | 7/16 |
| MNQ | 15 | eod * | -0.101 | -0.300 .. +0.099 | -1.6% | -0.174 | 0.32 | 1 | 8/16 |
| MNQ | 60 | h1 | +0.008 | -0.007 .. +0.023 | +1.6% | +0.021 | 0.33 |  | 10/16 |
| MNQ | 60 | h2 | +0.006 | -0.014 .. +0.025 | +0.7% | +0.026 | 0.58 |  | 10/16 |
| MNQ | 60 | h4 * | +0.019 | -0.011 .. +0.049 | +1.7% | +0.035 | 0.21 | 1 | 11/16 |
| MNQ | 60 | h8 | +0.025 | -0.012 .. +0.062 | +1.6% | +0.051 | 0.26 |  | 9/16 |
| MNQ | 60 | h16 | +0.022 | -0.023 .. +0.066 | +1.0% | +0.028 | 0.52 |  | 9/16 |
| MNQ | 60 | eod | +0.021 | -0.025 .. +0.068 | +0.9% | +0.030 | 0.48 |  | 9/16 |
| MYM | 5 | h1 | +0.009 | +0.003 .. +0.016 | +1.7% | +0.030 | 0.2 |  | 7/8 |
| MYM | 5 | h2 | +0.005 | -0.006 .. +0.015 | +0.6% | +0.021 | 0.97 |  | 5/8 |
| MYM | 5 | h4 | +0.003 | -0.018 .. +0.024 | +0.3% | +0.013 | 0.76 |  | 5/8 |
| MYM | 5 | h8 | +0.004 | -0.033 .. +0.041 | +0.3% | +0.011 | 0.83 |  | 6/8 |
| MYM | 5 | h16 | +0.008 | -0.045 .. +0.061 | +0.3% | +0.012 | 0.98 |  | 6/8 |
| MYM | 5 | eod * | -0.197 | -0.470 .. +0.076 | -1.7% | -0.343 | 0.16 | 1 | 4/8 |
| MYM | 15 | h1 | +0.003 | -0.008 .. +0.014 | +0.6% | -0.000 | 0.56 |  | 4/8 |
| MYM | 15 | h2 | -0.001 | -0.018 .. +0.016 | -0.1% | -0.003 | 0.91 |  | 5/8 |
| MYM | 15 | h4 * | -0.011 | -0.045 .. +0.022 | -1.0% | -0.013 | 0.5 | 1 | 5/8 |
| MYM | 15 | h8 | -0.012 | -0.062 .. +0.037 | -0.8% | -0.024 | 0.64 |  | 3/8 |
| MYM | 15 | h16 | -0.007 | -0.094 .. +0.080 | -0.3% | -0.019 | 0.88 |  | 3/8 |
| MYM | 15 | eod | +0.040 | -0.196 .. +0.276 | +0.7% | -0.029 | 0.75 |  | 7/8 |
| MYM | 60 | h1 | +0.011 | -0.009 .. +0.031 | +2.1% | +0.018 | 0.36 |  | 6/8 |
| MYM | 60 | h2 | -0.011 | -0.038 .. +0.016 | -1.5% | +0.010 | 0.46 |  | 5/8 |
| MYM | 60 | h4 | -0.002 | -0.039 .. +0.035 | -0.2% | +0.007 | 0.92 |  | 5/8 |
| MYM | 60 | h8 | -0.041 | -0.090 .. +0.009 | -2.6% | -0.017 | 0.25 |  | 4/8 |
| MYM | 60 | h16 * | -0.050 | -0.110 .. +0.011 | -2.3% | -0.055 | 0.2 | 1 | 5/8 |
| MYM | 60 | eod | -0.050 | -0.112 .. +0.012 | -2.2% | -0.052 | 0.24 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.78 pts | -1.25 .. -0.31 | 0.0011 |
| MES | 15 | +0.01 pts | -0.70 .. +0.72 | 0.98 |
| MES | 60 | -0.81 pts | -1.98 .. +0.37 | 0.18 |
| MNQ | 5 | -0.75 pts | -1.13 .. -0.38 | 6.8e-05 |
| MNQ | 15 | -0.14 pts | -0.70 .. +0.42 | 0.69 |
| MNQ | 60 | +0.32 pts | -0.78 .. +1.41 | 0.61 |
| MYM | 5 | -0.46 pts | -0.88 .. -0.05 | 0.047 |
| MYM | 15 | -0.86 pts | -1.77 .. +0.06 | 0.066 |
| MYM | 60 | +0.05 pts | -1.44 .. +1.54 | 0.99 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 43796 | +0.021 | 0.235 | +0.28 | -3.22 | -3.32 | -3.17 | -3.39 |
| MES | 5 | h2 | event | against signal | 43796 | +0.031 | 0.235 | +0.46 | -3.04 | -3.17 | -2.97 | -3.28 |
| MES | 5 | h4 | event | against signal | 43796 | +0.038 | 0.235 | +0.60 | -2.90 | -3.05 | -2.83 | -3.14 |
| MES | 5 | h8 | event | against signal | 43796 | +0.033 | 0.235 | +0.54 | -2.96 | -3.03 | -2.93 | -3.18 |
| MES | 5 | h16 | event | against signal | 43796 | +0.037 | 0.235 | +0.57 | -2.93 | -2.89 | -2.94 | -3.16 |
| MES | 5 | eod | event | against signal | 43796 | -0.004 | 0.235 | +0.84 | -2.66 | -2.95 | -2.52 | -2.46 |
| MES | 15 | h1 | event | against signal | 18742 | +0.008 | 0.158 | +0.10 | -3.40 | -3.44 | -3.37 | -3.59 |
| MES | 15 | h2 | event | with signal | 18742 | -0.009 | 0.158 | -0.11 | -3.61 | -3.55 | -3.65 | -3.40 |
| MES | 15 | h4 | event | against signal | 18742 | +0.017 | 0.158 | +0.08 | -3.42 | -3.28 | -3.51 | -3.62 |
| MES | 15 | h8 | event | against signal | 18742 | +0.027 | 0.158 | +0.19 | -3.31 | -3.21 | -3.38 | -3.51 |
| MES | 15 | h16 | event | against signal | 18742 | +0.017 | 0.158 | -0.03 | -3.53 | -2.89 | -3.96 | -3.70 |
| MES | 15 | eod | event | with signal | 18742 | +0.057 | 0.158 | +0.43 | -3.07 | -2.85 | -3.23 | -3.71 |
| MES | 60 | h1 | event | against signal | 5405 | +0.014 | 0.086 | +0.51 | -2.99 | -3.45 | -2.60 | -2.98 |
| MES | 60 | h2 | event | against signal | 5405 | +0.002 | 0.086 | -0.04 | -3.54 | -3.95 | -3.19 | -3.58 |
| MES | 60 | h4 | event | with signal | 5405 | +0.021 | 0.086 | +0.16 | -3.34 | -2.58 | -3.98 | -3.27 |
| MES | 60 | h8 | event | with signal | 5405 | +0.013 | 0.086 | -0.11 | -3.61 | -1.91 | -5.07 | -3.55 |
| MES | 60 | h16 | event | with signal | 5405 | +0.050 | 0.086 | +1.47 | -2.03 | -1.67 | -2.34 | -2.54 |
| MES | 60 | eod | event | with signal | 5405 | +0.045 | 0.086 | +1.03 | -2.47 | -1.72 | -3.11 | -2.82 |
| MNQ | 5 | h1 | event | against signal | 74071 | +0.012 | 0.114 | +0.28 | -1.72 | -1.92 | -1.59 | -1.80 |
| MNQ | 5 | h2 | event | against signal | 74071 | +0.019 | 0.114 | +0.43 | -1.57 | -1.89 | -1.35 | -1.71 |
| MNQ | 5 | h4 | event | against signal | 74071 | +0.022 | 0.114 | +0.62 | -1.38 | -1.85 | -1.07 | -1.46 |
| MNQ | 5 | h8 | event | against signal | 74071 | +0.019 | 0.114 | +0.64 | -1.36 | -1.81 | -1.04 | -1.31 |
| MNQ | 5 | h16 | event | against signal | 74071 | +0.020 | 0.114 | +0.65 | -1.35 | -1.94 | -0.95 | -1.24 |
| MNQ | 5 | eod | event | against signal | 74071 | +0.002 | 0.114 | +0.91 | -1.09 | -2.00 | -0.46 | -0.52 |
| MNQ | 15 | h1 | event | with signal | 26589 | -0.001 | 0.070 | -0.05 | -2.05 | -1.98 | -2.10 | -1.95 |
| MNQ | 15 | h2 | event | with signal | 26589 | -0.001 | 0.070 | +0.00 | -2.00 | -2.01 | -1.98 | -1.95 |
| MNQ | 15 | h4 | event | against signal | 26589 | +0.013 | 0.070 | +0.47 | -1.53 | -2.05 | -1.12 | -1.49 |
| MNQ | 15 | h8 | event | against signal | 26589 | +0.012 | 0.070 | +0.72 | -1.28 | -2.12 | -0.62 | -1.10 |
| MNQ | 15 | h16 | event | against signal | 26589 | +0.029 | 0.070 | +1.60 | -0.40 | -1.96 | +0.83 | -0.29 |
| MNQ | 15 | eod | event | with signal | 26589 | +0.071 | 0.070 | -1.51 | -3.51 | -1.20 | -5.31 | -4.24 |
| MNQ | 60 | h1 | event | with signal | 6719 | +0.017 | 0.036 | +1.14 | -0.86 | -1.61 | -0.18 | -0.94 |
| MNQ | 60 | h2 | event | with signal | 6719 | +0.010 | 0.036 | +0.68 | -1.32 | -1.63 | -1.04 | -1.31 |
| MNQ | 60 | h4 | event | against signal | 6719 | +0.014 | 0.036 | +0.63 | -1.37 | -1.97 | -0.83 | -1.42 |
| MNQ | 60 | h8 | event | against signal | 6719 | +0.033 | 0.036 | +1.35 | -0.65 | -1.73 | +0.33 | -0.64 |
| MNQ | 60 | h16 | event | with signal | 6719 | +0.020 | 0.036 | +1.00 | -1.00 | -1.19 | -0.82 | -1.49 |
| MNQ | 60 | eod | event | against signal | 6719 | -0.008 | 0.036 | -0.47 | -2.47 | -2.39 | -2.55 | -2.17 |
| MYM | 5 | h1 | event | against signal | 39320 | +0.009 | 0.162 | +0.08 | -1.92 | +nan | -1.92 | -2.02 |
| MYM | 5 | h2 | event | against signal | 39320 | +0.020 | 0.162 | +0.18 | -1.82 | +nan | -1.82 | -1.93 |
| MYM | 5 | h4 | event | against signal | 39320 | +0.020 | 0.162 | +0.26 | -1.74 | +nan | -1.74 | -1.85 |
| MYM | 5 | h8 | event | against signal | 39320 | +0.017 | 0.162 | +0.27 | -1.73 | +nan | -1.73 | -1.82 |
| MYM | 5 | h16 | event | against signal | 39320 | +0.026 | 0.162 | +0.31 | -1.69 | +nan | -1.69 | -1.83 |
| MYM | 5 | eod | event | against signal | 39320 | +0.019 | 0.162 | +0.65 | -1.35 | +nan | -1.35 | -1.63 |
| MYM | 15 | h1 | event | against signal | 13741 | +0.015 | 0.095 | +0.19 | -1.81 | +nan | -1.81 | -1.91 |
| MYM | 15 | h2 | event | against signal | 13741 | +0.012 | 0.095 | +0.10 | -1.90 | +nan | -1.90 | -2.00 |
| MYM | 15 | h4 | event | against signal | 13741 | +0.031 | 0.095 | +0.25 | -1.75 | +nan | -1.75 | -1.79 |
| MYM | 15 | h8 | event | against signal | 13741 | +0.020 | 0.095 | +0.04 | -1.96 | +nan | -1.96 | -2.00 |
| MYM | 15 | h16 | event | against signal | 13741 | +0.023 | 0.095 | +0.23 | -1.77 | +nan | -1.77 | -1.71 |
| MYM | 15 | eod | event | against signal | 13741 | -0.000 | 0.095 | -0.55 | -2.55 | +nan | -2.55 | -2.57 |
| MYM | 60 | h1 | event | with signal | 3354 | +0.019 | 0.047 | +0.62 | -1.38 | +nan | -1.38 | -1.41 |
| MYM | 60 | h2 | event | with signal | 3354 | +0.022 | 0.047 | +0.64 | -1.36 | +nan | -1.36 | -1.15 |
| MYM | 60 | h4 | event | with signal | 3354 | +0.017 | 0.047 | +0.02 | -1.98 | +nan | -1.98 | -1.70 |
| MYM | 60 | h8 | event | with signal | 3354 | +0.006 | 0.047 | -0.28 | -2.28 | +nan | -2.28 | -1.97 |
| MYM | 60 | h16 | event | with signal | 3354 | +0.037 | 0.047 | +0.55 | -1.45 | +nan | -1.45 | -1.77 |
| MYM | 60 | eod | event | with signal | 3354 | +0.023 | 0.047 | -0.11 | -2.11 | +nan | -2.11 | -2.40 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.898 | -1.032 | -1.111 | -1.060 | -0.889 | +0.000 | -0.035 | -0.045 | -0.053 | -0.050 | -0.055 |
| MES | 15 | -0.924 | -1.009 | -1.086 | -1.044 | -0.885 | +0.000 | -0.013 | -0.014 | -0.026 | -0.043 | -0.048 |
| MES | 60 | -1.239 | -1.092 | -1.033 | -0.982 | -0.844 | +0.000 | -0.016 | -0.004 | +0.007 | -0.087 | +0.040 |
| MNQ | 5 | -0.862 | -0.989 | -1.072 | -1.034 | -0.885 | +0.000 | -0.022 | -0.029 | -0.033 | -0.031 | -0.035 |
| MNQ | 15 | -0.916 | -0.988 | -1.057 | -1.012 | -0.873 | +0.000 | -0.004 | -0.005 | -0.020 | -0.027 | -0.054 |
| MNQ | 60 | -1.269 | -1.066 | -0.976 | -0.924 | -0.809 | +0.000 | +0.015 | +0.006 | -0.039 | -0.103 | +0.108 |
| MYM | 5 | -0.868 | -0.979 | -1.063 | -1.013 | -0.862 | +0.000 | -0.014 | -0.025 | -0.028 | -0.024 | -0.033 |
| MYM | 15 | -0.881 | -0.974 | -1.030 | -1.002 | -0.854 | +0.000 | -0.015 | -0.013 | -0.029 | -0.021 | -0.033 |
| MYM | 60 | -1.240 | -1.119 | -0.995 | -0.949 | -0.817 | +0.000 | +0.019 | +0.021 | -0.003 | -0.035 | +0.147 |

## Calibration

- MES 5-min: 1036271 bars, 43796 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 18742 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 5405 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 74071 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 26589 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 6719 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 39320 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 13741 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 3354 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 30095 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
