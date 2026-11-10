# Impact card: pat_engulfing

candle pattern engulfing in its textbook direction: bar2 body engulfs bar1 body (opposite colours, at least one side strictly), body2 > avgB10, bar1 against the EMA10 trend; bullish after a down bar below EMA10, bearish mirror [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (5 min), p=0.56; we would catch an effect of 0.016 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.053).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.31 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.216 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.031 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.056).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.79 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.132 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.061 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.42).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.32 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.066 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.015 R20 over the next 4 bars (20 min), p=0.47; we would catch an effect of 0.020 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.039).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.91 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.081 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.052 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.053 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.16 at recent bar sizes, 90% range up to $1.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.023 R20 over the next 1 bar (1 h), p=0.51; we would catch an effect of 0.071 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.97 at recent bar sizes, 90% range up to $6.26); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.043 R20 over the next 8 bars (40 min), p=0.072; we would catch an effect of 0.033 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.74 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.173 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.044 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.049 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.18 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.103 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.086 R20 over the next 16 bars (16 h), p=0.71; we would catch an effect of 0.096 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.42 at recent bar sizes, 90% range up to $5.61); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.005 | -0.001 .. +0.010 | +0.0018 | 0.088 / 0.094 / 0.089 | 0.093 | 1 | 1 | 11/16 | +0.002 | +0.008 | False | +1.7 / +1.7 |  |
| MES | 5 | h2 | +0.004 | -0.004 .. +0.012 | +0.0011 | 0.29 / 0.28 / 0.31 | 0.307 |  |  | 11/16 | +0.001 | +0.008 |  | +1.0 / +1.1 |  |
| MES | 5 | h4 | +0.006 | -0.005 .. +0.017 | +0.0010 | 0.3 / 0.29 / 0.3 | 0.296 |  |  | 9/16 | +0.007 | +0.005 |  | +1.0 / +1.0 | 0.016 |
| MES | 5 | h8 | +0.006 | -0.009 .. +0.022 | +0.0007 | 0.43 / 0.42 / 0.46 | 0.461 |  |  | 10/16 | +0.011 | +0.002 |  | +0.8 / +0.8 |  |
| MES | 5 | h16 | +0.019 | -0.005 .. +0.043 | +0.0016 | 0.13 / 0.12 / 0.12 | 0.122 |  |  | 13/16 | +0.012 | +0.025 |  | +1.5 / +1.5 |  |
| MES | 5 | eod | +0.016 | -0.088 .. +0.120 | +0.0003 | 0.76 / 0.77 / 0.78 | 0.785 |  |  | 9/16 | +0.062 | -0.030 |  | +0.3 / +0.3 |  |
| MES | 15 | h1 * | +0.006 | -0.004 .. +0.017 | +0.0022 | 0.25 / 0.25 / 0.27 | 0.272 | 1 | 1 | 8/16 | -0.000 | +0.013 | False | +1.2 / +1.2 |  |
| MES | 15 | h2 | +0.005 | -0.008 .. +0.018 | +0.0012 | 0.46 / 0.47 / 0.55 | 0.546 |  |  | 7/16 | -0.006 | +0.016 |  | +0.7 / +0.7 |  |
| MES | 15 | h4 | +0.004 | -0.016 .. +0.024 | +0.0006 | 0.71 / 0.69 / 0.75 | 0.748 |  |  | 8/16 | -0.005 | +0.013 |  | +0.4 / +0.4 | 0.031 |
| MES | 15 | h8 | +0.002 | -0.025 .. +0.030 | +0.0003 | 0.87 / 0.87 / 0.9 | 0.9 |  |  | 8/16 | -0.015 | +0.019 |  | +0.1 / +0.2 |  |
| MES | 15 | h16 | +0.002 | -0.036 .. +0.041 | +0.0002 | 0.9 / 0.9 / 0.91 | 0.918 |  |  | 8/16 | +0.002 | +0.003 |  | +0.1 / +0.1 |  |
| MES | 15 | eod | -0.007 | -0.101 .. +0.087 | -0.0002 | 0.89 / 0.89 / 0.9 | 0.903 |  |  | 10/16 | -0.003 | -0.011 |  | -0.1 / -0.1 |  |
| MES | 60 | h1 * | +0.005 | -0.016 .. +0.026 | +0.0018 | 0.65 / 0.67 / 0.67 | 0.666 | 1 | 1 | 8/16 | +0.006 | +0.004 | False | +0.4 / +0.4 |  |
| MES | 60 | h2 | +0.008 | -0.023 .. +0.038 | +0.0019 | 0.63 / 0.63 / 0.63 | 0.625 |  |  | 9/16 | +0.019 | -0.004 |  | +0.5 / +0.5 |  |
| MES | 60 | h4 | -0.001 | -0.046 .. +0.043 | -0.0002 | 0.95 / 0.95 / 0.95 | 0.948 |  |  | 6/16 | +0.002 | -0.005 |  | -0.1 / -0.1 | 0.061 |
| MES | 60 | h8 | +0.013 | -0.045 .. +0.072 | +0.0018 | 0.65 / 0.65 / 0.64 | 0.638 |  |  | 10/16 | +0.028 | -0.001 |  | +0.4 / +0.4 |  |
| MES | 60 | h16 | -0.002 | -0.067 .. +0.063 | -0.0002 | 0.95 / 0.95 / 0.95 | 0.948 |  |  | 8/16 | +0.014 | -0.018 |  | -0.1 / -0.1 |  |
| MES | 60 | eod | +0.002 | -0.064 .. +0.068 | +0.0002 | 0.95 / 0.95 / 0.95 | 0.954 |  |  | 8/16 | +0.015 | -0.011 |  | +0.1 / +0.1 |  |
| MNQ | 5 | h1 | +0.001 | -0.005 .. +0.008 | +0.0004 | 0.67 / 0.66 / 0.73 | 0.72 |  |  | 8/16 | +0.001 | +0.002 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h2 | -0.004 | -0.013 .. +0.005 | -0.0007 | 0.39 / 0.39 / 0.53 | 0.524 |  |  | 8/16 | -0.006 | -0.002 |  | -0.8 / -0.9 |  |
| MNQ | 5 | h4 * | -0.015 | -0.027 .. -0.002 | -0.0017 | 0.025 / 0.025 / 0.11 | 0.11 | 1 | 0.922 | 10/16 | -0.012 | -0.017 | False | -2.2 / -2.2 | 0.020 |
| MNQ | 5 | h8 | -0.022 | -0.040 .. -0.005 | -0.0018 | 0.012 / 0.012 / 0.088 | 0.0914 |  |  | 11/16 | -0.026 | -0.019 |  | -2.3 / -2.5 |  |
| MNQ | 5 | h16 | -0.024 | -0.050 .. +0.002 | -0.0014 | 0.071 / 0.069 / 0.19 | 0.18 |  |  | 9/16 | -0.041 | -0.007 |  | -1.7 / -1.8 |  |
| MNQ | 5 | eod | +0.006 | -0.123 .. +0.134 | +0.0001 | 0.93 / 0.93 / 0.94 | 0.947 |  |  | 9/16 | -0.015 | +0.026 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h1 | -0.001 | -0.014 .. +0.012 | -0.0002 | 0.93 / 0.93 / 0.93 | 0.923 |  |  | 8/16 | -0.007 | +0.005 |  | -0.1 / -0.1 |  |
| MNQ | 15 | h2 | +0.004 | -0.014 .. +0.022 | +0.0006 | 0.68 / 0.67 / 0.76 | 0.738 |  |  | 9/16 | -0.004 | +0.012 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h4 | +0.001 | -0.024 .. +0.026 | +0.0001 | 0.94 / 0.94 / 0.97 | 0.957 |  |  | 6/16 | -0.005 | +0.007 |  | +0.1 / +0.1 | 0.053 |
| MNQ | 15 | h8 | +0.012 | -0.023 .. +0.047 | +0.0009 | 0.5 / 0.5 / 0.65 | 0.64 |  |  | 9/16 | +0.017 | +0.006 |  | +0.6 / +0.7 |  |
| MNQ | 15 | h16 | +0.016 | -0.031 .. +0.063 | +0.0010 | 0.5 / 0.5 / 0.6 | 0.594 |  |  | 8/16 | +0.024 | +0.008 |  | +0.6 / +0.7 |  |
| MNQ | 15 | eod * | -0.052 | -0.173 .. +0.070 | -0.0010 | 0.41 / 0.4 / 0.53 | 0.531 | 1 | 1 | 10/16 | -0.033 | -0.070 | False | -0.8 / -0.8 |  |
| MNQ | 60 | h1 * | +0.023 | -0.003 .. +0.049 | +0.0074 | 0.083 / 0.086 / 0.095 | 0.0948 | 1 | 1 | 9/16 | +0.024 | +0.023 | False | +1.7 / +1.7 |  |
| MNQ | 60 | h2 | +0.028 | -0.009 .. +0.066 | +0.0063 | 0.14 / 0.13 / 0.13 | 0.125 |  |  | 9/16 | +0.030 | +0.027 |  | +1.5 / +1.5 |  |
| MNQ | 60 | h4 | +0.027 | -0.021 .. +0.074 | +0.0043 | 0.27 / 0.27 / 0.29 | 0.286 |  |  | 10/16 | +0.052 | +0.002 |  | +1.0 / +1.1 | 0.071 |
| MNQ | 60 | h8 | +0.022 | -0.039 .. +0.082 | +0.0025 | 0.49 / 0.49 / 0.52 | 0.52 |  |  | 9/16 | +0.051 | -0.007 |  | +0.6 / +0.7 |  |
| MNQ | 60 | h16 | +0.021 | -0.049 .. +0.092 | +0.0019 | 0.55 / 0.56 / 0.57 | 0.577 |  |  | 9/16 | +0.052 | -0.009 |  | +0.5 / +0.6 |  |
| MNQ | 60 | eod | +0.021 | -0.049 .. +0.091 | +0.0018 | 0.56 / 0.57 / 0.59 | 0.603 |  |  | 10/16 | +0.044 | -0.003 |  | +0.5 / +0.6 |  |
| MYM | 5 | h1 | +0.005 | -0.003 .. +0.014 | +0.0015 | 0.23 / 0.21 / 0.37 | 0.335 |  |  | 5/8 | n/a | +0.005 |  | +1.2 / +1.2 |  |
| MYM | 5 | h2 | +0.006 | -0.006 .. +0.019 | +0.0010 | 0.33 / 0.31 / 0.43 | 0.387 |  |  | 5/8 | n/a | +0.006 |  | +1.0 / +1.0 |  |
| MYM | 5 | h4 | +0.019 | +0.001 .. +0.037 | +0.0019 | 0.043 / 0.035 / 0.21 | 0.2 |  |  | 6/8 | n/a | +0.019 |  | +2.1 / +2.0 | 0.033 |
| MYM | 5 | h8 * | +0.043 | +0.017 .. +0.069 | +0.0032 | 0.0011 / 0.00039 / 0.027 | 0.0248 | 1 | 0.263 | 7/8 | n/a | +0.043 | False | +3.3 / +3.3 |  |
| MYM | 5 | h16 | +0.056 | +0.020 .. +0.092 | +0.0032 | 0.0024 / 0.0012 / 0.023 | 0.0211 |  |  | 7/8 | n/a | +0.056 |  | +2.9 / +3.0 |  |
| MYM | 5 | eod | +0.037 | -0.162 .. +0.236 | +0.0005 | 0.72 / 0.71 / 0.73 | 0.724 |  |  | 4/8 | n/a | +0.037 |  | +0.4 / +0.4 |  |
| MYM | 15 | h1 | +0.004 | -0.013 .. +0.022 | +0.0012 | 0.63 / 0.62 / 0.68 | 0.652 |  |  | 3/8 | n/a | +0.004 |  | +0.5 / +0.5 |  |
| MYM | 15 | h2 | -0.002 | -0.026 .. +0.022 | -0.0003 | 0.87 / 0.87 / 0.91 | 0.885 |  |  | 5/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 15 | h4 | -0.003 | -0.035 .. +0.029 | -0.0003 | 0.86 / 0.86 / 0.92 | 0.887 |  |  | 5/8 | n/a | -0.003 |  | -0.2 / -0.2 | 0.049 |
| MYM | 15 | h8 | +0.019 | -0.029 .. +0.067 | +0.0014 | 0.43 / 0.42 / 0.59 | 0.558 |  |  | 5/8 | n/a | +0.019 |  | +0.8 / +0.8 |  |
| MYM | 15 | h16 * | +0.044 | -0.022 .. +0.110 | +0.0023 | 0.19 / 0.18 / 0.38 | 0.389 | 1 | 1 | 6/8 | n/a | +0.044 | False | +1.2 / +1.3 |  |
| MYM | 15 | eod | +0.090 | -0.050 .. +0.230 | +0.0019 | 0.21 / 0.23 / 0.45 | 0.439 |  |  | 6/8 | n/a | +0.090 |  | +1.0 / +1.3 |  |
| MYM | 60 | h1 | +0.011 | -0.022 .. +0.044 | +0.0036 | 0.5 / 0.51 / 0.55 | 0.557 |  |  | 5/8 | n/a | +0.011 |  | +0.6 / +0.7 |  |
| MYM | 60 | h2 | +0.011 | -0.037 .. +0.060 | +0.0027 | 0.65 / 0.65 / 0.66 | 0.668 |  |  | 4/8 | n/a | +0.011 |  | +0.4 / +0.5 |  |
| MYM | 60 | h4 | +0.051 | -0.015 .. +0.118 | +0.0084 | 0.13 / 0.13 / 0.13 | 0.139 |  |  | 5/8 | n/a | +0.051 |  | +1.5 / +1.5 | 0.096 |
| MYM | 60 | h8 | +0.051 | -0.040 .. +0.143 | +0.0060 | 0.27 / 0.25 / 0.26 | 0.262 |  |  | 5/8 | n/a | +0.051 |  | +1.0 / +1.1 |  |
| MYM | 60 | h16 * | +0.086 | -0.016 .. +0.188 | +0.0077 | 0.098 / 0.081 / 0.098 | 0.0969 | 1 | 1 | 5/8 | n/a | +0.086 | False | +1.5 / +1.7 |  |
| MYM | 60 | eod | +0.083 | -0.019 .. +0.185 | +0.0072 | 0.11 / 0.093 / 0.11 | 0.103 |  |  | 5/8 | n/a | +0.083 |  | +1.4 / +1.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.006 | -0.010 .. -0.001 | -1.1% | -0.004 | 0.0089 | 1 | 13/16 |
| MES | 5 | h2 | +0.002 | -0.004 .. +0.007 | +0.2% | +0.001 | 0.78 |  | 13/16 |
| MES | 5 | h4 | +0.002 | -0.007 .. +0.011 | +0.2% | +0.002 | 0.97 |  | 11/16 |
| MES | 5 | h8 | +0.008 | -0.005 .. +0.022 | +0.6% | +0.013 | 0.33 |  | 12/16 |
| MES | 5 | h16 | +0.015 | -0.006 .. +0.036 | +0.7% | +0.020 | 0.19 |  | 13/16 |
| MES | 5 | eod | -0.000 | -0.143 .. +0.143 | -0.0% | -0.002 | 1 |  | 8/16 |
| MES | 15 | h1 * | -0.010 | -0.017 .. -0.002 | -1.9% | -0.002 | 0.0094 | 1 | 11/16 |
| MES | 15 | h2 | -0.008 | -0.018 .. +0.003 | -1.1% | -0.001 | 0.15 |  | 10/16 |
| MES | 15 | h4 | -0.001 | -0.016 .. +0.014 | -0.1% | -0.002 | 0.88 |  | 8/16 |
| MES | 15 | h8 | +0.020 | -0.003 .. +0.043 | +1.3% | +0.005 | 0.15 |  | 11/16 |
| MES | 15 | h16 | +0.009 | -0.026 .. +0.044 | +0.4% | +0.009 | 0.65 |  | 12/16 |
| MES | 15 | eod | +0.012 | -0.109 .. +0.134 | +0.2% | +0.016 | 0.84 |  | 12/16 |
| MES | 60 | h1 * | +0.016 | -0.001 .. +0.033 | +3.1% | +0.049 | 0.07 | 1 | 10/16 |
| MES | 60 | h2 | +0.015 | -0.007 .. +0.037 | +2.0% | +0.048 | 0.32 |  | 9/16 |
| MES | 60 | h4 | +0.011 | -0.020 .. +0.041 | +1.0% | +0.053 | 0.81 |  | 11/16 |
| MES | 60 | h8 | +0.006 | -0.032 .. +0.044 | +0.4% | +0.062 | 0.79 |  | 8/16 |
| MES | 60 | h16 | -0.000 | -0.044 .. +0.044 | -0.0% | +0.068 | 1 |  | 9/16 |
| MES | 60 | eod | +0.006 | -0.038 .. +0.049 | +0.3% | +0.080 | 0.85 |  | 7/16 |
| MNQ | 5 | h1 * | -0.008 | -0.013 .. -0.004 | -1.6% | -0.005 | 0.0066 | 0.927 | 9/16 |
| MNQ | 5 | h2 | -0.008 | -0.016 .. +0.000 | -1.0% | -0.006 | 0.11 |  | 10/16 |
| MNQ | 5 | h4 | -0.001 | -0.015 .. +0.012 | -0.1% | -0.002 | 0.87 |  | 9/16 |
| MNQ | 5 | h8 | -0.002 | -0.027 .. +0.023 | -0.1% | +0.001 | 0.9 |  | 6/16 |
| MNQ | 5 | h16 | +0.005 | -0.039 .. +0.049 | +0.2% | +0.014 | 1 |  | 12/16 |
| MNQ | 5 | eod | -0.009 | -0.235 .. +0.218 | -0.1% | -0.048 | 0.94 |  | 5/16 |
| MNQ | 15 | h1 | +0.001 | -0.009 .. +0.010 | +0.1% | +0.013 | 0.9 |  | 9/16 |
| MNQ | 15 | h2 | +0.006 | -0.010 .. +0.022 | +0.8% | +0.020 | 0.91 |  | 11/16 |
| MNQ | 15 | h4 * | +0.011 | -0.019 .. +0.041 | +1.0% | +0.021 | 0.46 | 1 | 10/16 |
| MNQ | 15 | h8 | +0.010 | -0.036 .. +0.056 | +0.6% | +0.010 | 0.66 |  | 11/16 |
| MNQ | 15 | h16 | +0.013 | -0.040 .. +0.066 | +0.5% | +0.015 | 0.65 |  | 11/16 |
| MNQ | 15 | eod | +0.066 | -0.128 .. +0.260 | +1.0% | +0.108 | 0.51 |  | 11/16 |
| MNQ | 60 | h1 | +0.013 | -0.005 .. +0.031 | +2.5% | +0.048 | 0.2 |  | 10/16 |
| MNQ | 60 | h2 | +0.016 | -0.007 .. +0.040 | +2.2% | +0.049 | 0.24 |  | 12/16 |
| MNQ | 60 | h4 | +0.004 | -0.028 .. +0.036 | +0.3% | +0.050 | 0.95 |  | 9/16 |
| MNQ | 60 | h8 | -0.022 | -0.069 .. +0.025 | -1.4% | +0.038 | 0.36 |  | 11/16 |
| MNQ | 60 | h16 | -0.037 | -0.093 .. +0.020 | -1.7% | +0.023 | 0.2 |  | 10/16 |
| MNQ | 60 | eod * | -0.039 | -0.095 .. +0.017 | -1.7% | +0.023 | 0.17 | 1 | 9/16 |
| MYM | 5 | h1 | -0.004 | -0.011 .. +0.004 | -0.7% | -0.002 | 0.38 |  | 5/8 |
| MYM | 5 | h2 | -0.007 | -0.019 .. +0.006 | -0.9% | -0.006 | 0.47 |  | 4/8 |
| MYM | 5 | h4 | -0.011 | -0.032 .. +0.011 | -1.0% | -0.007 | 0.38 |  | 4/8 |
| MYM | 5 | h8 | +0.004 | -0.033 .. +0.042 | +0.3% | +0.012 | 0.82 |  | 6/8 |
| MYM | 5 | h16 | +0.014 | -0.039 .. +0.068 | +0.6% | +0.011 | 0.67 |  | 6/8 |
| MYM | 5 | eod * | +0.134 | -0.125 .. +0.393 | +1.1% | +0.110 | 0.31 | 1 | 6/8 |
| MYM | 15 | h1 | +0.001 | -0.012 .. +0.013 | +0.1% | -0.000 | 0.92 |  | 4/8 |
| MYM | 15 | h2 * | -0.015 | -0.034 .. +0.004 | -2.0% | -0.010 | 0.29 | 1 | 6/8 |
| MYM | 15 | h4 | -0.008 | -0.045 .. +0.029 | -0.7% | -0.013 | 0.67 |  | 4/8 |
| MYM | 15 | h8 | +0.004 | -0.050 .. +0.058 | +0.2% | -0.017 | 0.95 |  | 6/8 |
| MYM | 15 | h16 | -0.005 | -0.095 .. +0.086 | -0.2% | -0.025 | 0.92 |  | 3/8 |
| MYM | 15 | eod | +0.046 | -0.192 .. +0.284 | +0.8% | +0.060 | 1 |  | 6/8 |
| MYM | 60 | h1 | +0.014 | -0.010 .. +0.037 | +2.6% | +0.042 | 0.46 |  | 5/8 |
| MYM | 60 | h2 * | +0.026 | -0.004 .. +0.057 | +3.5% | +0.056 | 0.3 | 1 | 5/8 |
| MYM | 60 | h4 | +0.014 | -0.027 .. +0.055 | +1.3% | +0.041 | 0.9 |  | 3/8 |
| MYM | 60 | h8 | +0.045 | -0.023 .. +0.112 | +2.9% | +0.086 | 0.41 |  | 4/8 |
| MYM | 60 | h16 | +0.023 | -0.053 .. +0.099 | +1.1% | +0.090 | 0.76 |  | 4/8 |
| MYM | 60 | eod | +0.024 | -0.050 .. +0.098 | +1.1% | +0.097 | 0.68 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.72 pts | +0.35 .. +1.09 | 0.00012 |
| MES | 15 | +0.39 pts | -0.18 .. +0.96 | 0.18 |
| MES | 60 | +0.48 pts | -0.68 .. +1.64 | 0.57 |
| MNQ | 5 | -0.10 pts | -0.48 .. +0.27 | 0.73 |
| MNQ | 15 | +0.55 pts | -0.05 .. +1.15 | 0.084 |
| MNQ | 60 | +0.78 pts | -0.37 .. +1.93 | 0.2 |
| MYM | 5 | +1.00 pts | +0.49 .. +1.51 | 0.00012 |
| MYM | 15 | +0.21 pts | -0.66 .. +1.08 | 0.64 |
| MYM | 60 | +0.68 pts | -1.17 .. +2.54 | 0.47 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 65857 | -0.006 | 0.292 | +0.00 | -3.50 | -3.52 | -3.48 | -3.36 |
| MES | 5 | h2 | event | with signal | 65857 | -0.012 | 0.292 | -0.09 | -3.59 | -3.58 | -3.60 | -3.40 |
| MES | 5 | h4 | event | with signal | 65857 | -0.011 | 0.292 | -0.07 | -3.57 | -3.53 | -3.60 | -3.37 |
| MES | 5 | h8 | event | with signal | 65857 | -0.010 | 0.292 | -0.10 | -3.60 | -3.52 | -3.66 | -3.41 |
| MES | 5 | h16 | event | with signal | 65857 | +0.002 | 0.292 | +0.12 | -3.38 | -3.52 | -3.28 | -3.19 |
| MES | 5 | eod | event | with signal | 65857 | -0.053 | 0.292 | -0.62 | -4.12 | -3.30 | -4.74 | -3.29 |
| MES | 15 | h1 | event | with signal | 24471 | -0.002 | 0.186 | +0.10 | -3.40 | -3.64 | -3.20 | -3.25 |
| MES | 15 | h2 | event | with signal | 24471 | -0.005 | 0.186 | -0.07 | -3.57 | -3.71 | -3.45 | -3.38 |
| MES | 15 | h4 | event | with signal | 24471 | -0.007 | 0.186 | +0.03 | -3.47 | -3.76 | -3.21 | -3.27 |
| MES | 15 | h8 | event | with signal | 24471 | -0.012 | 0.186 | -0.01 | -3.51 | -3.81 | -3.24 | -3.25 |
| MES | 15 | h16 | event | with signal | 24471 | -0.021 | 0.186 | -0.30 | -3.80 | -3.64 | -3.94 | -3.36 |
| MES | 15 | eod | event | against signal | 24471 | +0.040 | 0.186 | +0.86 | -2.64 | -3.01 | -2.32 | -3.37 |
| MES | 60 | h1 | event | with signal | 6047 | +0.004 | 0.097 | +0.08 | -3.42 | -3.13 | -3.71 | -3.41 |
| MES | 60 | h2 | event | with signal | 6047 | +0.004 | 0.097 | +0.21 | -3.29 | -2.76 | -3.82 | -3.17 |
| MES | 60 | h4 | event | against signal | 6047 | +0.009 | 0.097 | +0.35 | -3.15 | -3.47 | -2.83 | -3.37 |
| MES | 60 | h8 | event | with signal | 6047 | +0.003 | 0.097 | +0.33 | -3.17 | -2.95 | -3.39 | -2.83 |
| MES | 60 | h16 | event | against signal | 6047 | +0.006 | 0.097 | -0.18 | -3.68 | -4.13 | -3.24 | -3.71 |
| MES | 60 | eod | event | with signal | 6047 | -0.005 | 0.097 | +0.47 | -3.03 | -2.84 | -3.22 | -2.88 |
| MNQ | 5 | h1 | event | with signal | 64162 | -0.004 | 0.132 | +0.02 | -1.98 | -2.00 | -1.96 | -1.90 |
| MNQ | 5 | h2 | event | against signal | 64162 | +0.013 | 0.132 | +0.17 | -1.83 | -1.95 | -1.72 | -1.97 |
| MNQ | 5 | h4 | event | against signal | 64162 | +0.022 | 0.132 | +0.31 | -1.69 | -1.93 | -1.46 | -1.80 |
| MNQ | 5 | h8 | event | against signal | 64162 | +0.025 | 0.132 | +0.39 | -1.61 | -1.83 | -1.39 | -1.64 |
| MNQ | 5 | h16 | event | against signal | 64162 | +0.028 | 0.132 | +0.43 | -1.57 | -1.76 | -1.38 | -1.59 |
| MNQ | 5 | eod | event | with signal | 64162 | -0.112 | 0.132 | -0.78 | -2.78 | -2.31 | -3.24 | -1.11 |
| MNQ | 15 | h1 | event | against signal | 22466 | +0.004 | 0.081 | -0.26 | -2.26 | -1.89 | -2.65 | -2.33 |
| MNQ | 15 | h2 | event | with signal | 22466 | +0.002 | 0.081 | +0.15 | -1.85 | -2.15 | -1.53 | -1.80 |
| MNQ | 15 | h4 | event | with signal | 22466 | -0.000 | 0.081 | +0.15 | -1.85 | -2.16 | -1.53 | -1.86 |
| MNQ | 15 | h8 | event | with signal | 22466 | +0.013 | 0.081 | +0.28 | -1.72 | -2.06 | -1.38 | -1.79 |
| MNQ | 15 | h16 | event | with signal | 22466 | +0.002 | 0.081 | +0.11 | -1.89 | -1.99 | -1.77 | -1.60 |
| MNQ | 15 | eod | event | against signal | 22466 | +0.093 | 0.081 | +1.18 | -0.82 | -1.53 | -0.08 | -1.71 |
| MNQ | 60 | h1 | event | with signal | 5450 | +0.022 | 0.041 | +0.33 | -1.67 | -1.44 | -1.93 | -1.64 |
| MNQ | 60 | h2 | event | with signal | 5450 | +0.024 | 0.041 | +0.47 | -1.53 | -1.28 | -1.82 | -1.36 |
| MNQ | 60 | h4 | event | with signal | 5450 | +0.017 | 0.041 | -0.36 | -2.36 | -0.94 | -3.98 | -1.99 |
| MNQ | 60 | h8 | event | with signal | 5450 | +0.008 | 0.041 | -0.48 | -2.48 | -0.79 | -4.39 | -2.05 |
| MNQ | 60 | h16 | event | with signal | 5450 | +0.012 | 0.041 | +0.38 | -1.62 | -0.50 | -2.89 | -1.57 |
| MNQ | 60 | eod | event | with signal | 5450 | +0.006 | 0.041 | +0.48 | -1.52 | -0.72 | -2.42 | -1.30 |
| MYM | 5 | h1 | event | with signal | 33364 | -0.002 | 0.173 | +0.03 | -1.97 | +nan | -1.97 | -1.88 |
| MYM | 5 | h2 | event | with signal | 33364 | -0.005 | 0.173 | -0.07 | -2.07 | +nan | -2.07 | -1.93 |
| MYM | 5 | h4 | event | with signal | 33364 | +0.003 | 0.173 | +0.08 | -1.92 | +nan | -1.92 | -1.74 |
| MYM | 5 | h8 | event | with signal | 33364 | +0.023 | 0.173 | +0.25 | -1.75 | +nan | -1.75 | -1.50 |
| MYM | 5 | h16 | event | with signal | 33364 | +0.025 | 0.173 | +0.43 | -1.57 | +nan | -1.57 | -1.19 |
| MYM | 5 | eod | event | with signal | 33364 | -0.057 | 0.173 | +0.13 | -1.87 | +nan | -1.87 | -0.79 |
| MYM | 15 | h1 | event | with signal | 11411 | -0.002 | 0.103 | +0.06 | -1.94 | +nan | -1.94 | -1.82 |
| MYM | 15 | h2 | event | against signal | 11411 | +0.009 | 0.103 | +0.21 | -1.79 | +nan | -1.79 | -1.93 |
| MYM | 15 | h4 | event | against signal | 11411 | +0.009 | 0.103 | +0.17 | -1.83 | +nan | -1.83 | -1.94 |
| MYM | 15 | h8 | event | with signal | 11411 | +0.009 | 0.103 | +0.28 | -1.72 | +nan | -1.72 | -1.51 |
| MYM | 15 | h16 | event | with signal | 11411 | +0.031 | 0.103 | +0.43 | -1.57 | +nan | -1.57 | -1.34 |
| MYM | 15 | eod | event | with signal | 11411 | +0.057 | 0.103 | +0.83 | -1.17 | +nan | -1.17 | -0.69 |
| MYM | 60 | h1 | event | with signal | 2657 | +0.009 | 0.050 | +0.57 | -1.43 | +nan | -1.43 | -1.37 |
| MYM | 60 | h2 | event | with signal | 2657 | +0.002 | 0.050 | +0.58 | -1.42 | +nan | -1.42 | -1.07 |
| MYM | 60 | h4 | event | with signal | 2657 | +0.036 | 0.050 | +1.52 | -0.48 | +nan | -0.48 | +0.00 |
| MYM | 60 | h8 | event | with signal | 2657 | +0.029 | 0.050 | +1.68 | -0.32 | +nan | -0.32 | +0.38 |
| MYM | 60 | h16 | event | with signal | 2657 | +0.067 | 0.050 | +3.07 | +1.07 | +nan | +1.07 | +1.45 |
| MYM | 60 | eod | event | with signal | 2657 | +0.061 | 0.050 | +2.93 | +0.93 | +nan | +0.93 | +1.37 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.051 | -0.057 | -0.288 | -0.548 | -0.947 | +0.000 | -0.031 | -0.036 | -0.034 | -0.032 | -0.021 |
| MES | 15 | -0.101 | -0.096 | -0.322 | -0.576 | -0.966 | +0.000 | -0.011 | -0.013 | -0.015 | -0.018 | -0.025 |
| MES | 60 | -0.234 | -0.197 | -0.396 | -0.652 | -1.042 | +0.000 | +0.004 | +0.005 | -0.022 | -0.042 | +0.044 |
| MNQ | 5 | -0.033 | -0.034 | -0.283 | -0.566 | -0.961 | +0.000 | -0.016 | -0.025 | -0.033 | -0.035 | -0.037 |
| MNQ | 15 | -0.099 | -0.101 | -0.336 | -0.609 | -0.994 | +0.000 | -0.007 | -0.002 | -0.001 | +0.011 | +0.009 |
| MNQ | 60 | -0.212 | -0.193 | -0.400 | -0.688 | -1.082 | +0.000 | +0.025 | +0.025 | +0.017 | -0.060 | +0.182 |
| MYM | 5 | -0.026 | -0.024 | -0.270 | -0.559 | -0.944 | +0.000 | -0.010 | -0.011 | -0.001 | +0.021 | +0.031 |
| MYM | 15 | -0.088 | -0.099 | -0.335 | -0.598 | -0.977 | +0.000 | -0.001 | -0.007 | -0.008 | +0.018 | +0.047 |
| MYM | 60 | -0.081 | -0.147 | -0.379 | -0.684 | -1.059 | +0.000 | +0.011 | +0.003 | +0.031 | -0.014 | +0.130 |

## Calibration

- MES 5-min: 1036271 bars, 65857 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 24471 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 6047 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 64162 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 22466 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 5450 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 33364 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 11411 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 2657 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39631 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
