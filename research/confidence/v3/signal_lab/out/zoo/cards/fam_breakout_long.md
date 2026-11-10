# Impact card: fam_breakout_long

bullish breakout patterns only (long side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.010 R20 over the next 2 bars (10 min), p=0.063; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.15).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.17 at recent bar sizes, 90% range up to $0.38); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.038 R20 over the next 8 bars (2 h), p=0.11; we would catch an effect of 0.030 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.068).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.88 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.121 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.036 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.061 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.34).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.01 at recent bar sizes, 90% range up to $4.75); about 3.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.004 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.018 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.085).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.12 at recent bar sizes, 90% range up to $0.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.009 R20 over the next 1 bar (15 min), p=0.26; we would catch an effect of 0.034 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.15).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.42 at recent bar sizes, 90% range up to $2.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.057 R20 over the next 8 bars (8 h), p=0.47; we would catch an effect of 0.061 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.12 at recent bar sizes, 90% range up to $9.91); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.002 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.036 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.82).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.02 at recent bar sizes, 90% range up to $0.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.05 at recent bar sizes, 90% range up to $1.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.022 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.082 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.95 at recent bar sizes, 90% range up to $4.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.006 | -0.011 .. -0.001 | -0.0024 | 0.026 / 0.025 / 0.016 | 0.019 |  |  | 14/16 | -0.005 | -0.007 |  | -2.2 / -2.2 |  |
| MES | 5 | h2 * | -0.010 | -0.017 .. -0.002 | -0.0027 | 0.0092 / 0.01 / 0.011 | 0.0128 | 1 | 0.89 | 14/16 | -0.015 | -0.005 | False | -2.6 / -2.6 |  |
| MES | 5 | h4 | -0.008 | -0.019 .. +0.003 | -0.0016 | 0.15 / 0.14 / 0.15 | 0.145 |  |  | 12/16 | -0.018 | +0.002 |  | -1.5 / -1.5 | 0.017 |
| MES | 5 | h8 | -0.006 | -0.024 .. +0.011 | -0.0008 | 0.48 / 0.49 / 0.39 | 0.383 |  |  | 9/16 | -0.024 | +0.011 |  | -0.8 / -0.7 |  |
| MES | 5 | h16 | +0.004 | -0.024 .. +0.032 | +0.0004 | 0.77 / 0.78 / 0.71 | 0.713 |  |  | 8/16 | -0.020 | +0.028 |  | +0.4 / +0.3 |  |
| MES | 5 | eod | +0.024 | -0.354 .. +0.402 | +0.0004 | 0.9 / 0.9 / 0.73 | 0.723 |  |  | 7/16 | -0.117 | +0.165 |  | +0.5 / +0.1 |  |
| MES | 15 | h1 | -0.007 | -0.015 .. +0.002 | -0.0029 | 0.12 / 0.12 / 0.12 | 0.117 |  |  | 10/16 | -0.007 | -0.007 |  | -1.5 / -1.6 |  |
| MES | 15 | h2 | -0.016 | -0.028 .. -0.003 | -0.0044 | 0.014 / 0.015 / 0.018 | 0.0203 |  |  | 11/16 | -0.027 | -0.004 |  | -2.5 / -2.5 |  |
| MES | 15 | h4 | -0.019 | -0.038 .. -0.000 | -0.0037 | 0.047 / 0.05 / 0.041 | 0.0417 |  |  | 11/16 | -0.038 | -0.001 |  | -2.1 / -2.0 | 0.030 |
| MES | 15 | h8 * | -0.038 | -0.070 .. -0.007 | -0.0052 | 0.015 / 0.018 / 0.0035 | 0.00365 | 1 | 0.939 | 15/16 | -0.063 | -0.014 | False | -2.9 / -2.4 |  |
| MES | 15 | h16 | -0.036 | -0.094 .. +0.023 | -0.0034 | 0.23 / 0.23 / 0.057 | 0.0563 |  |  | 13/16 | -0.083 | +0.011 |  | -1.8 / -1.2 |  |
| MES | 15 | eod | -0.020 | -0.243 .. +0.203 | -0.0007 | 0.86 / 0.86 / 0.67 | 0.665 |  |  | 12/16 | -0.095 | +0.054 |  | -0.4 / -0.2 |  |
| MES | 60 | h1 | -0.007 | -0.026 .. +0.012 | -0.0031 | 0.45 / 0.45 / 0.46 | 0.454 |  |  | 7/16 | +0.009 | -0.024 |  | -0.7 / -0.8 |  |
| MES | 60 | h2 | -0.008 | -0.035 .. +0.020 | -0.0023 | 0.59 / 0.59 / 0.56 | 0.561 |  |  | 10/16 | -0.005 | -0.010 |  | -0.5 / -0.5 |  |
| MES | 60 | h4 | -0.021 | -0.059 .. +0.017 | -0.0045 | 0.27 / 0.27 / 0.22 | 0.213 |  |  | 8/16 | -0.005 | -0.038 |  | -1.1 / -1.1 | 0.061 |
| MES | 60 | h8 * | -0.036 | -0.092 .. +0.021 | -0.0055 | 0.21 / 0.23 / 0.14 | 0.132 | 1 | 1 | 10/16 | +0.000 | -0.072 | False | -1.4 / -1.2 |  |
| MES | 60 | h16 | -0.007 | -0.090 .. +0.075 | -0.0009 | 0.86 / 0.86 / 0.81 | 0.814 |  |  | 7/16 | +0.015 | -0.030 |  | -0.2 / -0.2 |  |
| MES | 60 | eod | -0.005 | -0.091 .. +0.081 | -0.0005 | 0.91 / 0.91 / 0.87 | 0.873 |  |  | 7/16 | +0.017 | -0.027 |  | -0.2 / -0.1 |  |
| MNQ | 5 | h1 | -0.002 | -0.006 .. +0.003 | -0.0006 | 0.51 / 0.53 / 0.54 | 0.53 |  |  | 7/16 | +0.006 | -0.009 |  | -0.6 / -0.7 |  |
| MNQ | 5 | h2 * | -0.004 | -0.011 .. +0.002 | -0.0011 | 0.17 / 0.2 / 0.26 | 0.255 | 1 | 1 | 10/16 | -0.001 | -0.008 | False | -1.3 / -1.4 |  |
| MNQ | 5 | h4 | -0.005 | -0.016 .. +0.005 | -0.0009 | 0.3 / 0.31 / 0.41 | 0.419 |  |  | 10/16 | -0.005 | -0.006 |  | -1.1 / -1.0 | 0.018 |
| MNQ | 5 | h8 | -0.009 | -0.025 .. +0.008 | -0.0010 | 0.3 / 0.3 / 0.32 | 0.325 |  |  | 13/16 | -0.016 | -0.001 |  | -1.2 / -1.0 |  |
| MNQ | 5 | h16 | -0.006 | -0.035 .. +0.022 | -0.0005 | 0.66 / 0.67 / 0.57 | 0.573 |  |  | 9/16 | -0.013 | +0.000 |  | -0.6 / -0.4 |  |
| MNQ | 5 | eod | -0.029 | -0.472 .. +0.414 | -0.0005 | 0.9 / 0.9 / 0.66 | 0.662 |  |  | 11/16 | -0.217 | +0.158 |  | -0.5 / -0.1 |  |
| MNQ | 15 | h1 * | -0.009 | -0.017 .. -0.002 | -0.0035 | 0.017 / 0.016 / 0.053 | 0.0542 | 1 | 0.957 | 13/16 | -0.011 | -0.008 | False | -2.2 / -2.4 |  |
| MNQ | 15 | h2 | -0.013 | -0.024 .. -0.001 | -0.0029 | 0.029 / 0.026 / 0.1 | 0.104 |  |  | 11/16 | -0.026 | +0.000 |  | -2.1 / -2.2 |  |
| MNQ | 15 | h4 | -0.023 | -0.041 .. -0.004 | -0.0030 | 0.015 / 0.015 / 0.095 | 0.0946 |  |  | 13/16 | -0.036 | -0.010 |  | -2.6 / -2.4 | 0.034 |
| MNQ | 15 | h8 | -0.033 | -0.064 .. -0.002 | -0.0034 | 0.035 / 0.036 / 0.064 | 0.0703 |  |  | 13/16 | -0.049 | -0.017 |  | -2.6 / -2.1 |  |
| MNQ | 15 | h16 | -0.030 | -0.086 .. +0.026 | -0.0025 | 0.29 / 0.31 / 0.16 | 0.152 |  |  | 12/16 | -0.075 | +0.014 |  | -1.6 / -1.1 |  |
| MNQ | 15 | eod | -0.004 | -0.238 .. +0.231 | -0.0001 | 0.98 / 0.98 / 0.95 | 0.954 |  |  | 12/16 | -0.138 | +0.130 |  | -0.1 / -0.0 |  |
| MNQ | 60 | h1 | +0.001 | -0.019 .. +0.021 | +0.0004 | 0.92 / 0.92 / 0.92 | 0.922 |  |  | 7/16 | +0.002 | -0.000 |  | +0.1 / +0.1 |  |
| MNQ | 60 | h2 | -0.007 | -0.037 .. +0.022 | -0.0022 | 0.62 / 0.62 / 0.57 | 0.569 |  |  | 10/16 | -0.018 | +0.003 |  | -0.5 / -0.5 |  |
| MNQ | 60 | h4 | -0.024 | -0.064 .. +0.016 | -0.0051 | 0.25 / 0.24 / 0.17 | 0.173 |  |  | 11/16 | -0.028 | -0.020 |  | -1.2 / -1.2 | 0.061 |
| MNQ | 60 | h8 * | -0.057 | -0.119 .. +0.006 | -0.0088 | 0.076 / 0.078 / 0.018 | 0.0159 | 1 | 1 | 11/16 | -0.062 | -0.051 | False | -2.1 / -1.8 |  |
| MNQ | 60 | h16 | -0.047 | -0.140 .. +0.045 | -0.0057 | 0.32 / 0.32 / 0.12 | 0.12 |  |  | 11/16 | -0.031 | -0.063 |  | -1.4 / -1.0 |  |
| MNQ | 60 | eod | -0.053 | -0.149 .. +0.043 | -0.0060 | 0.28 / 0.29 / 0.088 | 0.0862 |  |  | 10/16 | -0.037 | -0.069 |  | -1.6 / -1.1 |  |
| MYM | 5 | h1 * | +0.002 | -0.005 .. +0.008 | +0.0006 | 0.64 / 0.64 / 0.6 | 0.61 | 1 | 1 | 5/8 | n/a | +0.002 | False | +0.5 / +0.5 |  |
| MYM | 5 | h2 | +0.001 | -0.008 .. +0.010 | +0.0003 | 0.77 / 0.78 / 0.77 | 0.772 |  |  | 5/8 | n/a | +0.001 |  | +0.3 / +0.3 |  |
| MYM | 5 | h4 | +0.001 | -0.013 .. +0.016 | +0.0002 | 0.84 / 0.84 / 0.75 | 0.773 |  |  | 3/8 | n/a | +0.001 |  | +0.2 / +0.2 | 0.036 |
| MYM | 5 | h8 | +0.001 | -0.024 .. +0.026 | +0.0001 | 0.94 / 0.94 / 0.86 | 0.865 |  |  | 3/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 5 | h16 | +0.010 | -0.033 .. +0.053 | +0.0008 | 0.63 / 0.64 / 0.52 | 0.523 |  |  | 2/8 | n/a | +0.010 |  | +0.7 / +0.5 |  |
| MYM | 5 | eod | +0.100 | -0.521 .. +0.721 | +0.0018 | 0.75 / 0.76 / 0.21 | 0.218 |  |  | 5/8 | n/a | +0.100 |  | +1.3 / +0.3 |  |
| MYM | 15 | h1 * | -0.002 | -0.013 .. +0.009 | -0.0009 | 0.7 / 0.7 / 0.75 | 0.73 | 1 | 1 | 3/8 | n/a | -0.002 | False | -0.4 / -0.4 |  |
| MYM | 15 | h2 | -0.004 | -0.021 .. +0.014 | -0.0009 | 0.67 / 0.67 / 0.75 | 0.754 |  |  | 5/8 | n/a | -0.004 |  | -0.5 / -0.4 |  |
| MYM | 15 | h4 | -0.004 | -0.030 .. +0.023 | -0.0005 | 0.79 / 0.79 / 0.86 | 0.858 |  |  | 4/8 | n/a | -0.004 |  | -0.3 / -0.3 | 0.046 |
| MYM | 15 | h8 | -0.007 | -0.053 .. +0.039 | -0.0007 | 0.77 / 0.77 / 0.79 | 0.796 |  |  | 5/8 | n/a | -0.007 |  | -0.4 / -0.3 |  |
| MYM | 15 | h16 | +0.014 | -0.077 .. +0.105 | +0.0010 | 0.77 / 0.76 / 0.69 | 0.704 |  |  | 3/8 | n/a | +0.014 |  | +0.5 / +0.3 |  |
| MYM | 15 | eod | -0.010 | -0.374 .. +0.354 | -0.0003 | 0.96 / 0.96 / 0.9 | 0.901 |  |  | 5/8 | n/a | -0.010 |  | -0.2 / -0.1 |  |
| MYM | 60 | h1 | +0.005 | -0.020 .. +0.030 | +0.0023 | 0.69 / 0.7 / 0.69 | 0.694 |  |  | 5/8 | n/a | +0.005 |  | +0.4 / +0.4 |  |
| MYM | 60 | h2 * | +0.022 | -0.017 .. +0.062 | +0.0070 | 0.27 / 0.28 / 0.2 | 0.197 | 1 | 1 | 7/8 | n/a | +0.022 | False | +1.2 / +1.1 |  |
| MYM | 60 | h4 | +0.029 | -0.029 .. +0.087 | +0.0064 | 0.33 / 0.33 / 0.22 | 0.222 |  |  | 7/8 | n/a | +0.029 |  | +1.1 / +1.0 | 0.082 |
| MYM | 60 | h8 | +0.006 | -0.089 .. +0.100 | +0.0009 | 0.91 / 0.91 / 0.86 | 0.879 |  |  | 4/8 | n/a | +0.006 |  | +0.2 / +0.1 |  |
| MYM | 60 | h16 | +0.002 | -0.129 .. +0.133 | +0.0003 | 0.98 / 0.98 / 0.97 | 0.967 |  |  | 4/8 | n/a | +0.002 |  | +0.0 / +0.0 |  |
| MYM | 60 | eod | -0.011 | -0.146 .. +0.124 | -0.0013 | 0.87 / 0.88 / 0.78 | 0.789 |  |  | 4/8 | n/a | -0.011 |  | -0.2 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.005 .. +0.004 | -0.2% | -0.004 | 0.72 |  | 6/16 |
| MES | 5 | h2 | -0.005 | -0.011 .. +0.001 | -0.7% | -0.014 | 0.087 |  | 11/16 |
| MES | 5 | h4 | -0.006 | -0.015 .. +0.002 | -0.6% | -0.023 | 0.12 |  | 10/16 |
| MES | 5 | h8 * | -0.015 | -0.027 .. -0.002 | -1.0% | -0.038 | 0.025 | 1 | 9/16 |
| MES | 5 | h16 | -0.022 | -0.042 .. -0.001 | -1.0% | -0.058 | 0.036 |  | 9/16 |
| MES | 5 | eod | -0.175 | -0.339 .. -0.011 | -1.8% | -0.382 | 0.037 |  | 10/16 |
| MES | 15 | h1 * | -0.009 | -0.015 .. -0.002 | -1.7% | -0.015 | 0.011 | 1 | 9/16 |
| MES | 15 | h2 | -0.011 | -0.021 .. -0.001 | -1.5% | -0.023 | 0.028 |  | 12/16 |
| MES | 15 | h4 | -0.013 | -0.028 .. +0.003 | -1.2% | -0.028 | 0.1 |  | 9/16 |
| MES | 15 | h8 | -0.010 | -0.031 .. +0.012 | -0.6% | -0.036 | 0.39 |  | 10/16 |
| MES | 15 | h16 | -0.015 | -0.050 .. +0.019 | -0.7% | -0.058 | 0.39 |  | 8/16 |
| MES | 15 | eod | -0.089 | -0.212 .. +0.033 | -1.6% | -0.178 | 0.15 |  | 9/16 |
| MES | 60 | h1 | +0.004 | -0.010 .. +0.019 | +0.8% | -0.008 | 0.56 |  | 9/16 |
| MES | 60 | h2 | -0.001 | -0.021 .. +0.019 | -0.2% | -0.018 | 0.92 |  | 9/16 |
| MES | 60 | h4 | -0.002 | -0.029 .. +0.026 | -0.1% | -0.030 | 0.97 |  | 8/16 |
| MES | 60 | h8 | -0.020 | -0.054 .. +0.014 | -1.3% | -0.039 | 0.31 |  | 8/16 |
| MES | 60 | h16 | -0.038 | -0.077 .. +0.002 | -1.8% | -0.059 | 0.073 |  | 10/16 |
| MES | 60 | eod * | -0.041 | -0.083 .. -0.000 | -1.9% | -0.067 | 0.056 | 1 | 10/16 |
| MNQ | 5 | h1 | -0.003 | -0.007 .. +0.001 | -0.5% | -0.003 | 0.18 |  | 9/16 |
| MNQ | 5 | h2 | -0.008 | -0.015 .. -0.001 | -1.0% | -0.016 | 0.029 |  | 9/16 |
| MNQ | 5 | h4 | -0.011 | -0.023 .. +0.001 | -1.0% | -0.027 | 0.072 |  | 9/16 |
| MNQ | 5 | h8 * | -0.030 | -0.054 .. -0.006 | -1.8% | -0.046 | 0.014 | 1 | 10/16 |
| MNQ | 5 | h16 | -0.040 | -0.082 .. +0.003 | -1.7% | -0.079 | 0.067 |  | 10/16 |
| MNQ | 5 | eod | -0.157 | -0.401 .. +0.086 | -1.3% | -0.400 | 0.21 |  | 10/16 |
| MNQ | 15 | h1 * | -0.008 | -0.015 .. -0.001 | -1.5% | -0.012 | 0.026 | 1 | 10/16 |
| MNQ | 15 | h2 | -0.005 | -0.018 .. +0.008 | -0.6% | -0.017 | 0.45 |  | 7/16 |
| MNQ | 15 | h4 | -0.012 | -0.039 .. +0.016 | -1.0% | -0.029 | 0.4 |  | 7/16 |
| MNQ | 15 | h8 | -0.014 | -0.056 .. +0.028 | -0.8% | -0.046 | 0.52 |  | 7/16 |
| MNQ | 15 | h16 | -0.016 | -0.064 .. +0.032 | -0.6% | -0.073 | 0.51 |  | 9/16 |
| MNQ | 15 | eod | -0.094 | -0.293 .. +0.105 | -1.5% | -0.177 | 0.35 |  | 7/16 |
| MNQ | 60 | h1 | +0.003 | -0.011 .. +0.018 | +0.6% | -0.001 | 0.69 |  | 9/16 |
| MNQ | 60 | h2 | +0.013 | -0.007 .. +0.033 | +1.7% | +0.008 | 0.26 |  | 11/16 |
| MNQ | 60 | h4 * | +0.019 | -0.008 .. +0.045 | +1.7% | +0.003 | 0.23 | 1 | 11/16 |
| MNQ | 60 | h8 | +0.010 | -0.022 .. +0.042 | +0.6% | -0.004 | 0.64 |  | 10/16 |
| MNQ | 60 | h16 | -0.008 | -0.048 .. +0.032 | -0.4% | -0.021 | 0.71 |  | 8/16 |
| MNQ | 60 | eod | -0.011 | -0.053 .. +0.031 | -0.5% | -0.022 | 0.61 |  | 10/16 |
| MYM | 5 | h1 | +0.000 | -0.005 .. +0.005 | +0.0% | +0.001 | 0.98 |  | 5/8 |
| MYM | 5 | h2 | -0.005 | -0.015 .. +0.004 | -0.7% | -0.011 | 0.27 |  | 4/8 |
| MYM | 5 | h4 | -0.007 | -0.028 .. +0.013 | -0.7% | -0.021 | 0.48 |  | 3/8 |
| MYM | 5 | h8 | -0.020 | -0.060 .. +0.019 | -1.3% | -0.041 | 0.31 |  | 4/8 |
| MYM | 5 | h16 | -0.017 | -0.070 .. +0.037 | -0.7% | -0.050 | 0.54 |  | 2/8 |
| MYM | 5 | eod * | -0.203 | -0.470 .. +0.064 | -1.7% | -0.387 | 0.14 | 1 | 4/8 |
| MYM | 15 | h1 * | -0.007 | -0.017 .. +0.002 | -1.4% | -0.016 | 0.23 | 1 | 4/8 |
| MYM | 15 | h2 | -0.011 | -0.027 .. +0.006 | -1.4% | -0.022 | 0.32 |  | 5/8 |
| MYM | 15 | h4 | -0.018 | -0.050 .. +0.014 | -1.6% | -0.032 | 0.3 |  | 5/8 |
| MYM | 15 | h8 | -0.014 | -0.063 .. +0.035 | -0.9% | -0.046 | 0.59 |  | 2/8 |
| MYM | 15 | h16 | -0.010 | -0.098 .. +0.078 | -0.4% | -0.049 | 0.82 |  | 2/8 |
| MYM | 15 | eod | +0.017 | -0.219 .. +0.253 | +0.3% | -0.069 | 0.89 |  | 7/8 |
| MYM | 60 | h1 * | +0.008 | -0.010 .. +0.026 | +1.6% | +0.002 | 0.58 | 1 | 5/8 |
| MYM | 60 | h2 | -0.003 | -0.030 .. +0.024 | -0.4% | -0.006 | 0.82 |  | 5/8 |
| MYM | 60 | h4 | +0.004 | -0.031 .. +0.039 | +0.3% | -0.016 | 0.85 |  | 4/8 |
| MYM | 60 | h8 | +0.006 | -0.041 .. +0.053 | +0.4% | -0.009 | 0.81 |  | 4/8 |
| MYM | 60 | h16 | -0.011 | -0.066 .. +0.043 | -0.5% | -0.029 | 0.69 |  | 4/8 |
| MYM | 60 | eod | -0.011 | -0.068 .. +0.046 | -0.5% | -0.031 | 0.71 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.48 pts | -0.87 .. -0.09 | 0.016 |
| MES | 15 | -0.53 pts | -1.13 .. +0.06 | 0.081 |
| MES | 60 | -0.61 pts | -1.66 .. +0.45 | 0.28 |
| MNQ | 5 | -0.38 pts | -0.71 .. -0.06 | 0.021 |
| MNQ | 15 | -0.59 pts | -1.12 .. -0.06 | 0.03 |
| MNQ | 60 | -0.02 pts | -1.14 .. +1.10 | 0.97 |
| MYM | 5 | +0.00 pts | -0.44 .. +0.44 | 0.99 |
| MYM | 15 | -0.28 pts | -1.02 .. +0.45 | 0.5 |
| MYM | 60 | +0.77 pts | -0.79 .. +2.33 | 0.34 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 73513 | +0.016 | 0.251 | +0.21 | -3.29 | -3.37 | -3.24 | -3.44 |
| MES | 5 | h2 | event | against signal | 73513 | +0.022 | 0.251 | +0.29 | -3.21 | -3.27 | -3.17 | -3.43 |
| MES | 5 | h4 | event | against signal | 73513 | +0.016 | 0.251 | +0.24 | -3.26 | -3.28 | -3.26 | -3.45 |
| MES | 5 | h8 | event | against signal | 73513 | +0.002 | 0.251 | +0.08 | -3.42 | -3.37 | -3.45 | -3.52 |
| MES | 5 | h16 | event | with signal | 73513 | +0.029 | 0.251 | +0.39 | -3.11 | -3.32 | -2.98 | -3.15 |
| MES | 5 | eod | event | with signal | 73513 | +0.424 | 0.251 | +5.09 | +1.59 | -0.82 | +3.02 | +1.39 |
| MES | 15 | h1 | event | against signal | 29804 | +0.009 | 0.163 | +0.21 | -3.29 | -3.36 | -3.24 | -3.38 |
| MES | 15 | h2 | event | against signal | 29804 | +0.015 | 0.163 | +0.27 | -3.23 | -3.16 | -3.28 | -3.31 |
| MES | 15 | h4 | event | against signal | 29804 | +0.007 | 0.163 | -0.12 | -3.62 | -3.25 | -3.89 | -3.58 |
| MES | 15 | h8 | event | against signal | 29804 | +0.007 | 0.163 | -0.35 | -3.85 | -3.32 | -4.23 | -3.62 |
| MES | 15 | h16 | event | against signal | 29804 | -0.029 | 0.163 | -1.22 | -4.72 | -3.80 | -5.37 | -4.28 |
| MES | 15 | eod | event | against signal | 29804 | -0.238 | 0.163 | -4.56 | -8.06 | -6.33 | -9.28 | -6.92 |
| MES | 60 | h1 | event | against signal | 7267 | +0.000 | 0.088 | +0.29 | -3.21 | -3.86 | -2.66 | -3.08 |
| MES | 60 | h2 | event | against signal | 7267 | -0.007 | 0.088 | -0.21 | -3.71 | -3.89 | -3.57 | -3.41 |
| MES | 60 | h4 | event | against signal | 7267 | -0.014 | 0.088 | +0.09 | -3.41 | -4.24 | -2.71 | -2.55 |
| MES | 60 | h8 | event | against signal | 7267 | -0.026 | 0.088 | -0.96 | -4.46 | -5.22 | -3.83 | -3.02 |
| MES | 60 | h16 | event | against signal | 7267 | -0.102 | 0.088 | -4.01 | -7.51 | -6.36 | -8.47 | -4.68 |
| MES | 60 | eod | event | against signal | 7267 | -0.107 | 0.088 | -4.04 | -7.54 | -6.58 | -8.34 | -4.69 |
| MNQ | 5 | h1 | event | against signal | 106019 | +0.003 | 0.113 | +0.17 | -1.83 | -2.00 | -1.70 | -1.90 |
| MNQ | 5 | h2 | event | against signal | 106019 | +0.005 | 0.113 | +0.23 | -1.77 | -2.00 | -1.61 | -1.89 |
| MNQ | 5 | h4 | event | against signal | 106019 | -0.005 | 0.113 | +0.20 | -1.80 | -2.02 | -1.65 | -1.87 |
| MNQ | 5 | h8 | event | against signal | 106019 | -0.023 | 0.113 | +0.01 | -1.99 | -2.10 | -1.91 | -1.87 |
| MNQ | 5 | h16 | event | against signal | 106019 | -0.060 | 0.113 | -0.52 | -2.52 | -2.39 | -2.62 | -2.15 |
| MNQ | 5 | eod | event | against signal | 106019 | -0.667 | 0.113 | -6.08 | -8.08 | -5.07 | -10.28 | -8.05 |
| MNQ | 15 | h1 | event | against signal | 37558 | +0.005 | 0.069 | +0.12 | -1.88 | -1.93 | -1.84 | -1.85 |
| MNQ | 15 | h2 | event | against signal | 37558 | +0.002 | 0.069 | -0.06 | -2.06 | -1.90 | -2.20 | -1.96 |
| MNQ | 15 | h4 | event | against signal | 37558 | -0.006 | 0.069 | -0.48 | -2.48 | -2.02 | -2.86 | -2.10 |
| MNQ | 15 | h8 | event | against signal | 37558 | -0.025 | 0.069 | -1.01 | -3.01 | -2.25 | -3.64 | -2.15 |
| MNQ | 15 | h16 | event | against signal | 37558 | -0.067 | 0.069 | -1.67 | -3.67 | -2.62 | -4.52 | -2.83 |
| MNQ | 15 | eod | event | against signal | 37558 | -0.365 | 0.069 | -5.86 | -7.86 | -4.80 | -10.35 | -6.73 |
| MNQ | 60 | h1 | event | with signal | 8313 | +0.009 | 0.036 | +0.21 | -1.79 | -1.51 | -2.05 | -1.94 |
| MNQ | 60 | h2 | event | against signal | 8313 | -0.009 | 0.036 | -0.10 | -2.10 | -2.45 | -1.78 | -1.79 |
| MNQ | 60 | h4 | event | against signal | 8313 | -0.013 | 0.036 | +0.12 | -1.88 | -2.72 | -1.09 | -1.04 |
| MNQ | 60 | h8 | event | against signal | 8313 | -0.016 | 0.036 | +0.02 | -1.98 | -2.79 | -1.21 | -0.17 |
| MNQ | 60 | h16 | event | against signal | 8313 | -0.079 | 0.036 | -0.81 | -2.81 | -4.34 | -1.36 | +0.54 |
| MNQ | 60 | eod | event | against signal | 8313 | -0.080 | 0.036 | -0.25 | -2.25 | -4.42 | -0.21 | +1.06 |
| MYM | 5 | h1 | event | with signal | 56058 | -0.006 | 0.160 | -0.05 | -2.05 | +nan | -2.05 | -1.96 |
| MYM | 5 | h2 | event | with signal | 56058 | -0.007 | 0.160 | -0.03 | -2.03 | +nan | -2.03 | -1.92 |
| MYM | 5 | h4 | event | with signal | 56058 | -0.006 | 0.160 | +0.03 | -1.97 | +nan | -1.97 | -1.88 |
| MYM | 5 | h8 | event | with signal | 56058 | -0.002 | 0.160 | +0.14 | -1.86 | +nan | -1.86 | -1.83 |
| MYM | 5 | h16 | event | with signal | 56058 | +0.012 | 0.160 | +0.37 | -1.63 | +nan | -1.63 | -1.67 |
| MYM | 5 | eod | event | with signal | 56058 | +0.347 | 0.160 | +4.47 | +2.47 | +nan | +2.47 | +1.44 |
| MYM | 15 | h1 | event | against signal | 19669 | +0.005 | 0.095 | +0.01 | -1.99 | +nan | -1.99 | -2.07 |
| MYM | 15 | h2 | event | against signal | 19669 | +0.007 | 0.095 | +0.08 | -1.92 | +nan | -1.92 | -2.03 |
| MYM | 15 | h4 | event | against signal | 19669 | -0.003 | 0.095 | -0.38 | -2.38 | +nan | -2.38 | -2.33 |
| MYM | 15 | h8 | event | against signal | 19669 | -0.006 | 0.095 | -0.47 | -2.47 | +nan | -2.47 | -2.35 |
| MYM | 15 | h16 | event | with signal | 19669 | +0.041 | 0.095 | +1.36 | -0.64 | +nan | -0.64 | -0.97 |
| MYM | 15 | eod | event | against signal | 19669 | -0.146 | 0.095 | -3.69 | -5.69 | +nan | -5.69 | -4.57 |
| MYM | 60 | h1 | event | with signal | 4218 | +0.008 | 0.047 | +0.45 | -1.55 | +nan | -1.55 | -1.60 |
| MYM | 60 | h2 | event | with signal | 4218 | +0.024 | 0.047 | +1.23 | -0.77 | +nan | -0.77 | -0.74 |
| MYM | 60 | h4 | event | with signal | 4218 | +0.039 | 0.047 | +1.43 | -0.57 | +nan | -0.57 | -0.84 |
| MYM | 60 | h8 | event | with signal | 4218 | +0.027 | 0.047 | +2.15 | +0.15 | +nan | +0.15 | -0.47 |
| MYM | 60 | h16 | event | with signal | 4218 | +0.059 | 0.047 | +4.30 | +2.30 | +nan | +2.30 | +0.21 |
| MYM | 60 | eod | event | against signal | 4218 | -0.051 | 0.047 | -3.94 | -5.94 | +nan | -5.94 | -3.57 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.632 | -0.720 | -0.761 | -0.741 | -0.720 | +0.000 | -0.031 | -0.040 | -0.039 | -0.038 | -0.031 |
| MES | 15 | -0.647 | -0.723 | -0.757 | -0.727 | -0.709 | +0.000 | -0.018 | -0.029 | -0.035 | -0.059 | -0.063 |
| MES | 60 | -0.913 | -0.788 | -0.733 | -0.664 | -0.684 | +0.000 | -0.008 | -0.015 | -0.039 | -0.073 | +0.103 |
| MNQ | 5 | -0.599 | -0.688 | -0.736 | -0.724 | -0.711 | +0.000 | -0.015 | -0.021 | -0.019 | -0.016 | -0.008 |
| MNQ | 15 | -0.631 | -0.696 | -0.736 | -0.711 | -0.699 | +0.000 | -0.012 | -0.013 | -0.022 | -0.031 | -0.031 |
| MNQ | 60 | -0.908 | -0.759 | -0.697 | -0.632 | -0.663 | +0.000 | +0.001 | -0.013 | -0.044 | -0.115 | +0.034 |
| MYM | 5 | -0.605 | -0.684 | -0.727 | -0.710 | -0.701 | +0.000 | -0.008 | -0.008 | -0.004 | +0.003 | +0.014 |
| MYM | 15 | -0.634 | -0.683 | -0.707 | -0.693 | -0.685 | +0.000 | -0.002 | +0.000 | +0.009 | +0.015 | +0.081 |
| MYM | 60 | -0.915 | -0.783 | -0.716 | -0.662 | -0.680 | +0.000 | +0.007 | +0.023 | +0.027 | -0.023 | +0.160 |

## Calibration

- MES 5-min: 1036271 bars, 73513 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 29804 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 7267 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 106019 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 37558 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 8313 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 56058 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 19669 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 4218 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 37094 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
