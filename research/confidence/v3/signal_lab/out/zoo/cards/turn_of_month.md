# Impact card: turn_of_month

last trading day of a month and first 3 of the next [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.021 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.27).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.48 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.218 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.041 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.33).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.05 at recent bar sizes, 90% range up to $1.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.054 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.079 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.02).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.49 at recent bar sizes, 90% range up to $5.94); about 4.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.029 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.76).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.03 at recent bar sizes, 90% range up to $0.81); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.12 at recent bar sizes, 90% range up to $3.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.084 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.27).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.23 at recent bar sizes, 90% range up to $9.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.91).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.01 at recent bar sizes, 90% range up to $0.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.005 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.068 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.08 at recent bar sizes, 90% range up to $1.83); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.023 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.121 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.059).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.79 at recent bar sizes, 90% range up to $6.68); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.001 | -0.005 .. +0.003 | -0.0007 | 0.51 / 0.5 / 0.5 | 0.503 | 1 | 1 | 7/16 | -0.001 | -0.001 | False | -0.7 / -0.7 |  |
| MES | 5 | h2 | -0.002 | -0.010 .. +0.005 | -0.0009 | 0.56 / 0.54 / 0.54 | 0.539 |  |  | 7/16 | -0.003 | -0.002 |  | -0.9 / -0.6 |  |
| MES | 5 | h4 | -0.004 | -0.020 .. +0.011 | -0.0011 | 0.58 / 0.57 / 0.58 | 0.58 |  |  | 8/16 | -0.007 | -0.002 |  | -1.2 / -0.6 | 0.021 |
| MES | 5 | h8 | -0.009 | -0.041 .. +0.023 | -0.0016 | 0.59 / 0.57 / 0.59 | 0.589 |  |  | 9/16 | -0.013 | -0.005 |  | -1.7 / -0.5 |  |
| MES | 5 | h16 | -0.019 | -0.087 .. +0.048 | -0.0024 | 0.58 / 0.56 / 0.57 | 0.568 |  |  | 10/16 | -0.024 | -0.015 |  | -2.5 / -0.6 |  |
| MES | 5 | eod | -0.236 | -1.317 .. +0.844 | -0.0058 | 0.67 / 0.66 / 0.67 | 0.661 |  |  | 10/16 | -0.641 | +0.167 |  | -5.9 / -0.4 |  |
| MES | 15 | h1 * | -0.002 | -0.010 .. +0.005 | -0.0012 | 0.52 / 0.51 / 0.53 | 0.543 | 1 | 1 | 7/16 | -0.002 | -0.003 | False | -0.7 / -0.6 |  |
| MES | 15 | h2 | -0.004 | -0.019 .. +0.011 | -0.0014 | 0.58 / 0.57 / 0.58 | 0.582 |  |  | 9/16 | -0.004 | -0.004 |  | -0.9 / -0.5 |  |
| MES | 15 | h4 | -0.008 | -0.039 .. +0.022 | -0.0019 | 0.59 / 0.58 / 0.58 | 0.58 |  |  | 10/16 | -0.009 | -0.008 |  | -1.2 / -0.5 | 0.041 |
| MES | 15 | h8 | -0.017 | -0.080 .. +0.046 | -0.0027 | 0.59 / 0.58 / 0.58 | 0.568 |  |  | 9/16 | -0.016 | -0.018 |  | -1.7 / -0.5 |  |
| MES | 15 | h16 | -0.027 | -0.157 .. +0.103 | -0.0030 | 0.68 / 0.67 / 0.67 | 0.67 |  |  | 9/16 | -0.021 | -0.033 |  | -1.8 / -0.4 |  |
| MES | 15 | eod | -0.076 | -0.671 .. +0.520 | -0.0033 | 0.8 / 0.8 / 0.8 | 0.794 |  |  | 11/16 | -0.318 | +0.165 |  | -2.0 / -0.2 |  |
| MES | 60 | h1 | -0.003 | -0.017 .. +0.012 | -0.0014 | 0.7 / 0.7 / 0.71 | 0.709 |  |  | 9/16 | -0.006 | +0.000 |  | -0.4 / -0.4 |  |
| MES | 60 | h2 | -0.006 | -0.035 .. +0.023 | -0.0022 | 0.68 / 0.68 / 0.69 | 0.696 |  |  | 10/16 | -0.012 | -0.000 |  | -0.6 / -0.4 |  |
| MES | 60 | h4 | -0.012 | -0.070 .. +0.045 | -0.0031 | 0.68 / 0.67 / 0.68 | 0.689 |  |  | 8/16 | -0.021 | -0.003 |  | -0.9 / -0.4 | 0.079 |
| MES | 60 | h8 | -0.026 | -0.137 .. +0.085 | -0.0048 | 0.64 / 0.64 / 0.65 | 0.664 |  |  | 10/16 | -0.047 | -0.005 |  | -1.3 / -0.5 |  |
| MES | 60 | h16 * | -0.054 | -0.252 .. +0.144 | -0.0076 | 0.59 / 0.59 / 0.59 | 0.595 | 1 | 1 | 11/16 | -0.107 | -0.001 | False | -2.1 / -0.5 |  |
| MES | 60 | eod | -0.049 | -0.268 .. +0.171 | -0.0065 | 0.67 / 0.67 / 0.67 | 0.679 |  |  | 11/16 | -0.127 | +0.030 |  | -1.8 / -0.4 |  |
| MNQ | 5 | h1 * | -0.001 | -0.006 .. +0.003 | -0.0006 | 0.54 / 0.52 / 0.55 | 0.572 | 1 | 1 | 8/16 | -0.002 | -0.001 | False | -0.7 / -0.6 |  |
| MNQ | 5 | h2 | -0.002 | -0.011 .. +0.008 | -0.0004 | 0.74 / 0.73 / 0.74 | 0.754 |  |  | 8/16 | -0.004 | +0.001 |  | -0.5 / -0.3 |  |
| MNQ | 5 | h4 | -0.002 | -0.021 .. +0.017 | -0.0003 | 0.84 / 0.84 / 0.85 | 0.85 |  |  | 7/16 | -0.008 | +0.004 |  | -0.4 / -0.2 | 0.029 |
| MNQ | 5 | h8 | -0.005 | -0.045 .. +0.034 | -0.0006 | 0.8 / 0.8 / 0.81 | 0.812 |  |  | 7/16 | -0.016 | +0.005 |  | -0.8 / -0.3 |  |
| MNQ | 5 | h16 | -0.012 | -0.093 .. +0.070 | -0.0010 | 0.78 / 0.77 / 0.78 | 0.785 |  |  | 7/16 | -0.026 | +0.002 |  | -1.2 / -0.3 |  |
| MNQ | 5 | eod | -0.177 | -1.499 .. +1.145 | -0.0031 | 0.79 / 0.79 / 0.78 | 0.78 |  |  | 6/16 | -0.843 | +0.484 |  | -3.4 / -0.3 |  |
| MNQ | 15 | h1 * | -0.003 | -0.011 .. +0.005 | -0.0012 | 0.44 / 0.42 / 0.47 | 0.469 | 1 | 1 | 9/16 | -0.003 | -0.004 | False | -0.9 / -0.8 |  |
| MNQ | 15 | h2 | -0.004 | -0.021 .. +0.012 | -0.0010 | 0.61 / 0.6 / 0.62 | 0.606 |  |  | 8/16 | -0.006 | -0.002 |  | -0.7 / -0.5 |  |
| MNQ | 15 | h4 | -0.009 | -0.044 .. +0.025 | -0.0012 | 0.6 / 0.59 / 0.63 | 0.601 |  |  | 8/16 | -0.013 | -0.005 |  | -1.0 / -0.5 | 0.048 |
| MNQ | 15 | h8 | -0.020 | -0.091 .. +0.051 | -0.0021 | 0.57 / 0.56 / 0.56 | 0.556 |  |  | 8/16 | -0.026 | -0.015 |  | -1.6 / -0.6 |  |
| MNQ | 15 | h16 | -0.022 | -0.170 .. +0.127 | -0.0019 | 0.77 / 0.76 / 0.76 | 0.753 |  |  | 8/16 | -0.040 | -0.004 |  | -1.2 / -0.3 |  |
| MNQ | 15 | eod | +0.016 | -0.670 .. +0.703 | +0.0005 | 0.96 / 0.96 / 0.96 | 0.964 |  |  | 10/16 | -0.325 | +0.356 |  | +0.3 / +0.0 |  |
| MNQ | 60 | h1 * | -0.003 | -0.019 .. +0.012 | -0.0014 | 0.7 / 0.7 / 0.68 | 0.679 | 1 | 1 | 7/16 | -0.009 | +0.003 | False | -0.4 / -0.4 |  |
| MNQ | 60 | h2 | -0.005 | -0.036 .. +0.026 | -0.0017 | 0.75 / 0.74 / 0.73 | 0.72 |  |  | 7/16 | -0.016 | +0.006 |  | -0.5 / -0.3 |  |
| MNQ | 60 | h4 | -0.009 | -0.069 .. +0.052 | -0.0020 | 0.78 / 0.78 / 0.77 | 0.765 |  |  | 7/16 | -0.028 | +0.011 |  | -0.6 / -0.3 | 0.084 |
| MNQ | 60 | h8 | -0.017 | -0.133 .. +0.100 | -0.0028 | 0.78 / 0.78 / 0.77 | 0.768 |  |  | 7/16 | -0.057 | +0.024 |  | -0.8 / -0.3 |  |
| MNQ | 60 | h16 | -0.031 | -0.239 .. +0.178 | -0.0040 | 0.77 / 0.77 / 0.76 | 0.763 |  |  | 8/16 | -0.123 | +0.061 |  | -1.1 / -0.3 |  |
| MNQ | 60 | eod | -0.017 | -0.244 .. +0.210 | -0.0021 | 0.89 / 0.88 / 0.88 | 0.881 |  |  | 8/16 | -0.130 | +0.097 |  | -0.6 / -0.1 |  |
| MYM | 5 | h1 * | -0.001 | -0.007 .. +0.005 | -0.0005 | 0.72 / 0.71 / 0.73 | 0.738 | 1 | 1 | 6/8 | n/a | -0.001 | False | -0.4 / -0.4 |  |
| MYM | 5 | h2 | +0.000 | -0.014 .. +0.014 | +0.0001 | 0.97 / 0.97 / 0.97 | 0.97 |  |  | 4/8 | n/a | +0.000 |  | +0.1 / +0.0 |  |
| MYM | 5 | h4 | +0.003 | -0.028 .. +0.033 | +0.0004 | 0.86 / 0.86 / 0.87 | 0.893 |  |  | 4/8 | n/a | +0.003 |  | +0.4 / +0.2 | 0.045 |
| MYM | 5 | h8 | +0.003 | -0.056 .. +0.062 | +0.0003 | 0.93 / 0.93 / 0.93 | 0.954 |  |  | 4/8 | n/a | +0.003 |  | +0.3 / +0.1 |  |
| MYM | 5 | h16 | -0.010 | -0.119 .. +0.099 | -0.0009 | 0.86 / 0.86 / 0.87 | 0.87 |  |  | 5/8 | n/a | -0.010 |  | -0.8 / -0.2 |  |
| MYM | 5 | eod | -0.111 | -1.953 .. +1.732 | -0.0021 | 0.91 / 0.91 / 0.92 | 0.91 |  |  | 4/8 | n/a | -0.111 |  | -1.6 / -0.1 |  |
| MYM | 15 | h1 * | -0.005 | -0.015 .. +0.006 | -0.0018 | 0.38 / 0.38 / 0.45 | 0.43 | 1 | 1 | 4/8 | n/a | -0.005 | False | -0.9 / -0.9 |  |
| MYM | 15 | h2 | -0.006 | -0.028 .. +0.016 | -0.0013 | 0.6 / 0.6 / 0.61 | 0.606 |  |  | 4/8 | n/a | -0.006 |  | -0.7 / -0.5 |  |
| MYM | 15 | h4 | -0.012 | -0.057 .. +0.034 | -0.0016 | 0.61 / 0.62 / 0.63 | 0.645 |  |  | 4/8 | n/a | -0.012 |  | -0.9 / -0.5 | 0.068 |
| MYM | 15 | h8 | -0.026 | -0.120 .. +0.067 | -0.0028 | 0.58 / 0.59 / 0.59 | 0.603 |  |  | 4/8 | n/a | -0.026 |  | -1.5 / -0.6 |  |
| MYM | 15 | h16 | -0.050 | -0.256 .. +0.156 | -0.0037 | 0.63 / 0.64 / 0.65 | 0.668 |  |  | 4/8 | n/a | -0.050 |  | -2.0 / -0.5 |  |
| MYM | 15 | eod | +0.007 | -0.951 .. +0.965 | +0.0002 | 0.99 / 0.99 / 0.99 | 0.993 |  |  | 4/8 | n/a | +0.007 |  | +0.1 / +0.0 |  |
| MYM | 60 | h1 | -0.005 | -0.027 .. +0.016 | -0.0025 | 0.63 / 0.63 / 0.7 | 0.702 |  |  | 3/8 | n/a | -0.005 |  | -0.5 / -0.5 |  |
| MYM | 60 | h2 | -0.010 | -0.054 .. +0.033 | -0.0034 | 0.65 / 0.64 / 0.71 | 0.718 |  |  | 3/8 | n/a | -0.010 |  | -0.7 / -0.5 |  |
| MYM | 60 | h4 * | -0.023 | -0.108 .. +0.063 | -0.0055 | 0.61 / 0.6 / 0.67 | 0.695 | 1 | 1 | 3/8 | n/a | -0.023 | False | -1.1 / -0.5 | 0.121 |
| MYM | 60 | h8 | -0.038 | -0.207 .. +0.130 | -0.0067 | 0.66 / 0.65 / 0.71 | 0.72 |  |  | 4/8 | n/a | -0.038 |  | -1.3 / -0.4 |  |
| MYM | 60 | h16 | -0.071 | -0.379 .. +0.236 | -0.0096 | 0.65 / 0.65 / 0.67 | 0.701 |  |  | 3/8 | n/a | -0.071 |  | -1.8 / -0.5 |  |
| MYM | 60 | eod | -0.043 | -0.392 .. +0.306 | -0.0055 | 0.81 / 0.81 / 0.82 | 0.833 |  |  | 3/8 | n/a | -0.043 |  | -1.1 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.003 .. +0.002 | -0.1% | +0.001 | 0.6 |  | 9/16 |
| MES | 5 | h2 | +0.002 | -0.003 .. +0.007 | +0.3% | +0.001 | 0.5 |  | 10/16 |
| MES | 5 | h4 | +0.004 | -0.006 .. +0.013 | +0.4% | +0.003 | 0.46 |  | 10/16 |
| MES | 5 | h8 | +0.010 | -0.009 .. +0.028 | +0.7% | +0.006 | 0.31 |  | 10/16 |
| MES | 5 | h16 * | +0.037 | +0.002 .. +0.073 | +1.8% | +0.020 | 0.046 | 1 | 12/16 |
| MES | 5 | eod | +0.476 | -0.170 .. +1.122 | +4.8% | +0.635 | 0.16 |  | 10/16 |
| MES | 15 | h1 | +0.002 | -0.002 .. +0.007 | +0.4% | +0.000 | 0.31 |  | 9/16 |
| MES | 15 | h2 | +0.002 | -0.007 .. +0.010 | +0.2% | +0.000 | 0.73 |  | 9/16 |
| MES | 15 | h4 | +0.009 | -0.009 .. +0.026 | +0.8% | +0.002 | 0.35 |  | 11/16 |
| MES | 15 | h8 | +0.032 | -0.001 .. +0.066 | +2.1% | +0.011 | 0.069 |  | 11/16 |
| MES | 15 | h16 * | +0.067 | +0.000 .. +0.134 | +2.9% | +0.027 | 0.055 | 1 | 11/16 |
| MES | 15 | eod | +0.258 | -0.116 .. +0.631 | +4.7% | +0.323 | 0.2 |  | 12/16 |
| MES | 60 | h1 | +0.010 | -0.001 .. +0.020 | +1.9% | +0.013 | 0.071 |  | 12/16 |
| MES | 60 | h2 * | +0.026 | +0.009 .. +0.043 | +3.5% | +0.028 | 0.0034 | 0.519 | 14/16 |
| MES | 60 | h4 | +0.049 | +0.016 .. +0.082 | +4.6% | +0.054 | 0.0045 |  | 13/16 |
| MES | 60 | h8 | +0.086 | +0.026 .. +0.146 | +5.7% | +0.099 | 0.0063 |  | 13/16 |
| MES | 60 | h16 | +0.137 | +0.022 .. +0.252 | +6.7% | +0.195 | 0.02 |  | 14/16 |
| MES | 60 | eod | +0.142 | +0.008 .. +0.276 | +6.6% | +0.218 | 0.039 |  | 13/16 |
| MNQ | 5 | h1 * | -0.003 | -0.006 .. +0.000 | -0.5% | -0.003 | 0.13 | 1 | 11/16 |
| MNQ | 5 | h2 | -0.004 | -0.011 .. +0.003 | -0.5% | -0.007 | 0.34 |  | 10/16 |
| MNQ | 5 | h4 | -0.006 | -0.022 .. +0.009 | -0.6% | -0.014 | 0.49 |  | 10/16 |
| MNQ | 5 | h8 | -0.010 | -0.042 .. +0.021 | -0.6% | -0.027 | 0.57 |  | 10/16 |
| MNQ | 5 | h16 | -0.001 | -0.061 .. +0.060 | -0.0% | -0.045 | 0.98 |  | 8/16 |
| MNQ | 5 | eod | +0.241 | -0.587 .. +1.069 | +1.9% | +0.146 | 0.57 |  | 11/16 |
| MNQ | 15 | h1 | -0.001 | -0.007 .. +0.005 | -0.2% | -0.006 | 0.77 |  | 9/16 |
| MNQ | 15 | h2 | -0.005 | -0.019 .. +0.009 | -0.7% | -0.012 | 0.62 |  | 10/16 |
| MNQ | 15 | h4 | -0.010 | -0.042 .. +0.023 | -0.9% | -0.024 | 0.74 |  | 8/16 |
| MNQ | 15 | h8 | +0.004 | -0.051 .. +0.059 | +0.2% | -0.042 | 0.88 |  | 10/16 |
| MNQ | 15 | h16 * | +0.030 | -0.056 .. +0.116 | +1.2% | -0.062 | 0.53 | 1 | 11/16 |
| MNQ | 15 | eod | +0.116 | -0.336 .. +0.568 | +1.8% | +0.049 | 0.62 |  | 10/16 |
| MNQ | 60 | h1 | +0.007 | -0.004 .. +0.018 | +1.2% | +0.006 | 0.25 |  | 10/16 |
| MNQ | 60 | h2 | +0.019 | +0.000 .. +0.037 | +2.4% | +0.016 | 0.047 |  | 12/16 |
| MNQ | 60 | h4 | +0.035 | +0.000 .. +0.069 | +3.2% | +0.031 | 0.051 |  | 12/16 |
| MNQ | 60 | h8 * | +0.067 | +0.003 .. +0.131 | +4.2% | +0.056 | 0.044 | 1 | 12/16 |
| MNQ | 60 | h16 | +0.092 | -0.027 .. +0.210 | +4.2% | +0.121 | 0.14 |  | 12/16 |
| MNQ | 60 | eod | +0.092 | -0.043 .. +0.227 | +4.0% | +0.127 | 0.19 |  | 11/16 |
| MYM | 5 | h1 * | -0.004 | -0.009 .. +0.001 | -0.7% | -0.003 | 0.15 | 1 | 5/8 |
| MYM | 5 | h2 | -0.006 | -0.016 .. +0.005 | -0.7% | -0.010 | 0.41 |  | 5/8 |
| MYM | 5 | h4 | -0.013 | -0.036 .. +0.011 | -1.2% | -0.022 | 0.42 |  | 5/8 |
| MYM | 5 | h8 | -0.018 | -0.065 .. +0.028 | -1.2% | -0.045 | 0.55 |  | 3/8 |
| MYM | 5 | h16 | -0.003 | -0.079 .. +0.073 | -0.1% | -0.063 | 0.95 |  | 3/8 |
| MYM | 5 | eod | +0.651 | -0.483 .. +1.786 | +5.6% | +0.904 | 0.32 |  | 4/8 |
| MYM | 15 | h1 | +0.003 | -0.005 .. +0.011 | +0.5% | -0.002 | 0.61 |  | 6/8 |
| MYM | 15 | h2 | -0.004 | -0.022 .. +0.014 | -0.5% | -0.009 | 0.73 |  | 3/8 |
| MYM | 15 | h4 | -0.002 | -0.042 .. +0.039 | -0.2% | -0.020 | 0.96 |  | 3/8 |
| MYM | 15 | h8 | +0.020 | -0.052 .. +0.093 | +1.2% | -0.030 | 0.71 |  | 5/8 |
| MYM | 15 | h16 | +0.057 | -0.089 .. +0.203 | +2.3% | -0.030 | 0.56 |  | 5/8 |
| MYM | 15 | eod * | +0.379 | -0.247 .. +1.005 | +6.3% | +0.500 | 0.33 | 1 | 5/8 |
| MYM | 60 | h1 | +0.010 | -0.005 .. +0.026 | +2.0% | +0.014 | 0.2 |  | 5/8 |
| MYM | 60 | h2 | +0.033 | +0.006 .. +0.060 | +4.3% | +0.033 | 0.02 |  | 7/8 |
| MYM | 60 | h4 * | +0.070 | +0.017 .. +0.122 | +6.4% | +0.067 | 0.0099 | 1 | 7/8 |
| MYM | 60 | h8 | +0.134 | +0.036 .. +0.231 | +8.6% | +0.143 | 0.01 |  | 7/8 |
| MYM | 60 | h16 | +0.209 | +0.025 .. +0.393 | +9.8% | +0.276 | 0.037 |  | 7/8 |
| MYM | 60 | eod | +0.231 | +0.021 .. +0.440 | +10.4% | +0.327 | 0.041 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.22 pts | -0.76 .. +0.31 | 0.42 |
| MES | 15 | -0.25 pts | -1.16 .. +0.67 | 0.6 |
| MES | 60 | -0.17 pts | -2.09 .. +1.74 | 0.86 |
| MNQ | 5 | -0.24 pts | -0.76 .. +0.29 | 0.38 |
| MNQ | 15 | -0.37 pts | -1.28 .. +0.55 | 0.43 |
| MNQ | 60 | +0.46 pts | -1.46 .. +2.37 | 0.67 |
| MYM | 5 | -0.23 pts | -0.96 .. +0.50 | 0.54 |
| MYM | 15 | -0.27 pts | -1.42 .. +0.89 | 0.66 |
| MYM | 60 | -1.10 pts | -3.73 .. +1.53 | 0.41 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | short | 192995 | -0.000 | 0.321 | -0.01 | -3.51 | -3.50 | -3.52 | -3.51 |
| MES | 5 | h2 | event | short | 192995 | -0.003 | 0.321 | -0.04 | -3.54 | -3.51 | -3.56 | -3.52 |
| MES | 5 | h4 | event | short | 192995 | -0.006 | 0.321 | -0.09 | -3.59 | -3.53 | -3.65 | -3.54 |
| MES | 5 | h8 | event | short | 192995 | -0.014 | 0.321 | -0.19 | -3.69 | -3.57 | -3.81 | -3.58 |
| MES | 5 | h16 | event | short | 192995 | -0.030 | 0.321 | -0.40 | -3.90 | -3.65 | -4.14 | -3.64 |
| MES | 5 | eod | event | short | 192995 | -0.348 | 0.321 | -4.98 | -8.48 | -4.76 | -12.20 | -6.87 |
| MES | 15 | h1 | event | short | 63867 | -0.003 | 0.185 | -0.06 | -3.56 | -3.51 | -3.61 | -3.51 |
| MES | 15 | h2 | event | short | 63867 | -0.006 | 0.185 | -0.14 | -3.64 | -3.54 | -3.73 | -3.55 |
| MES | 15 | h4 | event | short | 63867 | -0.013 | 0.185 | -0.30 | -3.80 | -3.61 | -3.98 | -3.62 |
| MES | 15 | h8 | event | short | 63867 | -0.025 | 0.185 | -0.60 | -4.10 | -3.73 | -4.47 | -3.76 |
| MES | 15 | h16 | event | short | 63867 | -0.053 | 0.185 | -1.20 | -4.70 | -4.02 | -5.38 | -4.12 |
| MES | 15 | eod | event | short | 63867 | -0.203 | 0.185 | -4.97 | -8.47 | -4.76 | -12.18 | -7.15 |
| MES | 60 | h1 | event | short | 15720 | -0.006 | 0.092 | -0.29 | -3.79 | -3.62 | -3.96 | -3.62 |
| MES | 60 | h2 | event | short | 15720 | -0.012 | 0.092 | -0.62 | -4.12 | -3.75 | -4.48 | -3.72 |
| MES | 60 | h4 | event | short | 15720 | -0.025 | 0.092 | -1.22 | -4.72 | -4.08 | -5.37 | -3.87 |
| MES | 60 | h8 | event | short | 15720 | -0.044 | 0.092 | -2.32 | -5.82 | -4.57 | -7.08 | -4.16 |
| MES | 60 | h16 | event | short | 15720 | -0.060 | 0.092 | -4.03 | -7.53 | -4.87 | -10.21 | -4.93 |
| MES | 60 | eod | event | short | 15720 | -0.080 | 0.092 | -5.03 | -8.53 | -4.95 | -12.12 | -5.43 |
| MNQ | 5 | h1 | event | short | 192651 | -0.003 | 0.128 | -0.03 | -2.03 | -2.00 | -2.06 | -2.02 |
| MNQ | 5 | h2 | event | short | 192651 | -0.006 | 0.128 | -0.08 | -2.08 | -2.01 | -2.15 | -2.06 |
| MNQ | 5 | h4 | event | short | 192651 | -0.013 | 0.128 | -0.17 | -2.17 | -2.03 | -2.31 | -2.14 |
| MNQ | 5 | h8 | event | short | 192651 | -0.026 | 0.128 | -0.35 | -2.35 | -2.06 | -2.64 | -2.25 |
| MNQ | 5 | h16 | event | short | 192651 | -0.053 | 0.128 | -0.72 | -2.72 | -2.13 | -3.31 | -2.42 |
| MNQ | 5 | eod | event | short | 192651 | -0.628 | 0.128 | -9.45 | -11.45 | -2.78 | -20.09 | -10.49 |
| MNQ | 15 | h1 | event | short | 63836 | -0.005 | 0.073 | -0.12 | -2.12 | -2.02 | -2.22 | -2.01 |
| MNQ | 15 | h2 | event | short | 63836 | -0.010 | 0.073 | -0.26 | -2.26 | -2.05 | -2.47 | -2.10 |
| MNQ | 15 | h4 | event | short | 63836 | -0.018 | 0.073 | -0.54 | -2.54 | -2.10 | -2.97 | -2.22 |
| MNQ | 15 | h8 | event | short | 63836 | -0.035 | 0.073 | -1.08 | -3.08 | -2.19 | -3.97 | -2.42 |
| MNQ | 15 | h16 | event | short | 63836 | -0.071 | 0.073 | -2.13 | -4.13 | -2.41 | -5.84 | -3.38 |
| MNQ | 15 | eod | event | long | 63836 | +0.351 | 0.073 | +9.43 | +7.43 | -1.21 | +16.06 | +6.29 |
| MNQ | 60 | h1 | event | short | 15719 | -0.008 | 0.036 | -0.53 | -2.53 | -2.11 | -2.96 | -2.23 |
| MNQ | 60 | h2 | event | short | 15719 | -0.017 | 0.036 | -1.11 | -3.11 | -2.21 | -4.01 | -2.48 |
| MNQ | 60 | h4 | event | short | 15719 | -0.034 | 0.036 | -2.14 | -4.14 | -2.46 | -5.82 | -2.90 |
| MNQ | 60 | h8 | event | short | 15719 | -0.061 | 0.036 | -4.03 | -6.03 | -2.73 | -9.34 | -3.81 |
| MNQ | 60 | h16 | event | short | 15719 | -0.094 | 0.036 | -7.37 | -9.37 | -2.65 | -16.11 | -6.16 |
| MNQ | 60 | eod | event | short | 15719 | -0.125 | 0.036 | -9.39 | -11.39 | -2.96 | -19.86 | -7.44 |
| MYM | 5 | h1 | event | short | 96235 | +0.001 | 0.168 | -0.01 | -2.01 | +nan | -2.01 | -2.01 |
| MYM | 5 | h2 | event | long | 96235 | -0.002 | 0.168 | +0.02 | -1.98 | +nan | -1.98 | -1.97 |
| MYM | 5 | h4 | event | long | 96235 | -0.002 | 0.168 | +0.06 | -1.94 | +nan | -1.94 | -1.92 |
| MYM | 5 | h8 | event | long | 96235 | -0.004 | 0.168 | +0.13 | -1.87 | +nan | -1.87 | -1.86 |
| MYM | 5 | h16 | event | short | 96235 | +0.011 | 0.168 | -0.28 | -2.28 | +nan | -2.28 | -2.19 |
| MYM | 5 | eod | event | short | 96235 | -0.103 | 0.168 | -3.58 | -5.58 | +nan | -5.58 | -4.70 |
| MYM | 15 | h1 | event | short | 31835 | +0.002 | 0.095 | -0.03 | -2.03 | +nan | -2.03 | -2.02 |
| MYM | 15 | h2 | event | short | 31835 | +0.004 | 0.095 | -0.09 | -2.09 | +nan | -2.09 | -2.10 |
| MYM | 15 | h4 | event | short | 31835 | +0.008 | 0.095 | -0.21 | -2.21 | +nan | -2.21 | -2.23 |
| MYM | 15 | h8 | event | short | 31835 | +0.021 | 0.095 | -0.42 | -2.42 | +nan | -2.42 | -2.49 |
| MYM | 15 | h16 | event | short | 31835 | +0.053 | 0.095 | -0.72 | -2.72 | +nan | -2.72 | -3.05 |
| MYM | 15 | eod | event | long | 31835 | +0.064 | 0.095 | +3.54 | +1.54 | +nan | +1.54 | +1.91 |
| MYM | 60 | h1 | event | short | 7803 | -0.001 | 0.046 | -0.20 | -2.20 | +nan | -2.20 | -2.03 |
| MYM | 60 | h2 | event | short | 7803 | -0.002 | 0.046 | -0.42 | -2.42 | +nan | -2.42 | -2.07 |
| MYM | 60 | h4 | event | short | 7803 | -0.001 | 0.046 | -0.69 | -2.69 | +nan | -2.69 | -1.98 |
| MYM | 60 | h8 | event | short | 7803 | -0.002 | 0.046 | -1.17 | -3.17 | +nan | -3.17 | -1.97 |
| MYM | 60 | h16 | event | short | 7803 | +0.005 | 0.046 | -2.09 | -4.09 | +nan | -4.09 | -2.04 |
| MYM | 60 | eod | event | short | 7803 | -0.030 | 0.046 | -3.52 | -5.52 | +nan | -5.52 | -2.83 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.003 | -0.003 | -0.000 | +0.001 | +0.000 | +0.000 | -0.001 | -0.002 | -0.004 | -0.006 | -0.016 |
| MES | 15 | -0.014 | -0.006 | -0.002 | -0.001 | -0.000 | +0.000 | -0.001 | -0.003 | -0.006 | -0.014 | -0.025 |
| MES | 60 | -0.059 | -0.023 | -0.005 | -0.002 | +0.000 | +0.000 | -0.003 | -0.006 | -0.015 | -0.035 | -0.082 |
| MNQ | 5 | -0.004 | -0.005 | -0.001 | -0.000 | +0.000 | +0.000 | -0.000 | -0.000 | -0.000 | -0.002 | -0.010 |
| MNQ | 15 | -0.017 | -0.008 | -0.004 | -0.003 | -0.001 | +0.000 | -0.000 | -0.001 | -0.004 | -0.015 | -0.021 |
| MNQ | 60 | -0.041 | -0.019 | -0.003 | -0.001 | -0.000 | +0.000 | -0.003 | -0.005 | -0.014 | -0.034 | -0.088 |
| MYM | 5 | +0.006 | +0.001 | +0.001 | +0.000 | +0.000 | +0.000 | +0.002 | +0.003 | +0.006 | +0.007 | -0.010 |
| MYM | 15 | +0.012 | +0.005 | +0.003 | +0.001 | +0.000 | +0.000 | +0.001 | +0.000 | -0.005 | -0.022 | -0.058 |
| MYM | 60 | +0.071 | +0.050 | +0.019 | +0.003 | +0.001 | +0.000 | -0.003 | -0.006 | -0.025 | -0.083 | -0.176 |

## Calibration

- MES 5-min: 1036271 bars, 192995 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 63867 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 15720 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 192651 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 63836 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 15719 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 96235 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 31835 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 7803 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
