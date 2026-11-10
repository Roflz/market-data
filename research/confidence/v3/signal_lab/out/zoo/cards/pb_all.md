# Impact card: pb_all

pullback detector (pullbacks.detect, 5-bar legs): every setup in its trend direction at the event bar [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.027 R20 over the next 8 bars (40 min), p=0.43; we would catch an effect of 0.030 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.05).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.96 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.190 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.059 R20 over the next 16 bars (4 h), p=0.76; we would catch an effect of 0.050 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.093).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.01 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.114 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.084 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.093 R20 or more 80% of the time).
- MES 60-min size: the market moves 6% LESS after the event than after matched bars over the next 16 bars (16 h) (-0.128 R20, possible, q=0.0506, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.77 at recent bar sizes, 90% range up to $6.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.013 R20 over the next 2 bars (10 min), p=0.88; we would catch an effect of 0.029 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.02).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.35 at recent bar sizes, 90% range up to $1.14); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.017 R20 over the next 1 bar (15 min), p=0.39; we would catch an effect of 0.046 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.011).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.81 at recent bar sizes, 90% range up to $2.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.066 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.098 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.041).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.21 at recent bar sizes, 90% range up to $8.86); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.016 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.596 R20, CONFIRMED, q=0.00318, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.20 at recent bar sizes, 90% range up to $0.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.016 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.065 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.12).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.37 at recent bar sizes, 90% range up to $3.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.041 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.128 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.82 at recent bar sizes, 90% range up to $5.98); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.013 .. +0.006 | -0.0006 | 0.49 / 0.5 / 0.53 | 0.53 |  |  | 9/16 | -0.006 | -0.001 |  | -0.7 / -0.7 |  |
| MES | 5 | h2 | -0.007 | -0.020 .. +0.005 | -0.0009 | 0.25 / 0.27 / 0.34 | 0.324 |  |  | 9/16 | -0.010 | -0.005 |  | -1.0 / -1.2 |  |
| MES | 5 | h4 | +0.009 | -0.010 .. +0.029 | +0.0008 | 0.35 / 0.36 / 0.4 | 0.404 |  |  | 9/16 | -0.007 | +0.026 |  | +0.9 / +0.9 | 0.030 |
| MES | 5 | h8 * | +0.027 | -0.002 .. +0.057 | +0.0016 | 0.068 / 0.072 / 0.09 | 0.0899 | 1 | 1 | 10/16 | -0.017 | +0.071 | False | +1.8 / +1.8 |  |
| MES | 5 | h16 | +0.017 | -0.025 .. +0.060 | +0.0007 | 0.43 / 0.42 / 0.46 | 0.463 |  |  | 7/16 | -0.013 | +0.047 |  | +0.8 / +0.8 |  |
| MES | 5 | eod | +0.008 | -0.240 .. +0.256 | +0.0000 | 0.95 / 0.95 / 0.96 | 0.956 |  |  | 8/16 | +0.116 | -0.100 |  | +0.1 / +0.1 |  |
| MES | 15 | h1 | -0.012 | -0.027 .. +0.003 | -0.0023 | 0.12 / 0.13 / 0.17 | 0.177 |  |  | 11/16 | -0.004 | -0.020 |  | -1.5 / -1.6 |  |
| MES | 15 | h2 | -0.013 | -0.036 .. +0.009 | -0.0017 | 0.24 / 0.24 / 0.31 | 0.314 |  |  | 9/16 | +0.000 | -0.027 |  | -1.1 / -1.2 |  |
| MES | 15 | h4 | -0.025 | -0.058 .. +0.008 | -0.0021 | 0.14 / 0.14 / 0.2 | 0.203 |  |  | 10/16 | -0.002 | -0.048 |  | -1.5 / -1.5 | 0.050 |
| MES | 15 | h8 | -0.025 | -0.073 .. +0.024 | -0.0015 | 0.32 / 0.32 / 0.38 | 0.369 |  |  | 10/16 | +0.010 | -0.059 |  | -1.0 / -1.0 |  |
| MES | 15 | h16 * | +0.059 | -0.008 .. +0.127 | +0.0025 | 0.085 / 0.087 / 0.15 | 0.15 | 1 | 1 | 10/16 | +0.027 | +0.092 | False | +1.6 / +1.7 |  |
| MES | 15 | eod | +0.004 | -0.196 .. +0.203 | +0.0001 | 0.97 / 0.97 / 0.97 | 0.972 |  |  | 6/16 | -0.026 | +0.033 |  | +0.0 / +0.0 |  |
| MES | 60 | h1 | +0.001 | -0.029 .. +0.032 | +0.0003 | 0.94 / 0.94 / 0.94 | 0.935 |  |  | 8/16 | +0.002 | +0.001 |  | +0.1 / +0.1 |  |
| MES | 60 | h2 | -0.015 | -0.057 .. +0.028 | -0.0020 | 0.49 / 0.49 / 0.54 | 0.543 |  |  | 8/16 | -0.011 | -0.019 |  | -0.7 / -0.7 |  |
| MES | 60 | h4 | -0.001 | -0.062 .. +0.060 | +0.0000 | 0.98 / 0.98 / 0.98 | 0.98 |  |  | 7/16 | +0.011 | -0.013 |  | -0.0 / -0.0 | 0.093 |
| MES | 60 | h8 | +0.046 | -0.031 .. +0.123 | +0.0034 | 0.24 / 0.26 / 0.32 | 0.321 |  |  | 11/16 | +0.061 | +0.031 |  | +1.1 / +1.2 |  |
| MES | 60 | h16 | +0.063 | -0.045 .. +0.170 | +0.0035 | 0.25 / 0.27 / 0.34 | 0.341 |  |  | 11/16 | +0.066 | +0.059 |  | +1.1 / +1.1 |  |
| MES | 60 | eod * | +0.084 | -0.040 .. +0.207 | +0.0045 | 0.18 / 0.19 / 0.23 | 0.234 | 1 | 1 | 11/16 | +0.066 | +0.101 | False | +1.3 / +1.3 |  |
| MNQ | 5 | h1 | -0.002 | -0.010 .. +0.006 | -0.0005 | 0.56 / 0.57 / 0.66 | 0.646 |  |  | 6/16 | -0.002 | -0.003 |  | -0.6 / -0.6 |  |
| MNQ | 5 | h2 * | -0.013 | -0.025 .. -0.001 | -0.0015 | 0.037 / 0.04 / 0.15 | 0.133 | 1 | 0.999 | 9/16 | -0.010 | -0.016 | False | -2.1 / -2.1 |  |
| MNQ | 5 | h4 | -0.018 | -0.036 .. -0.000 | -0.0013 | 0.049 / 0.056 / 0.2 | 0.169 |  |  | 12/16 | -0.016 | -0.019 |  | -1.9 / -2.0 | 0.029 |
| MNQ | 5 | h8 | -0.009 | -0.034 .. +0.016 | -0.0005 | 0.49 / 0.5 / 0.66 | 0.629 |  |  | 8/16 | -0.003 | -0.015 |  | -0.7 / -0.7 |  |
| MNQ | 5 | h16 | +0.008 | -0.035 .. +0.050 | +0.0003 | 0.72 / 0.73 / 0.78 | 0.778 |  |  | 9/16 | -0.003 | +0.018 |  | +0.4 / +0.4 |  |
| MNQ | 5 | eod | -0.060 | -0.339 .. +0.219 | -0.0005 | 0.67 / 0.68 / 0.72 | 0.724 |  |  | 10/16 | -0.041 | -0.079 |  | -0.6 / -0.4 |  |
| MNQ | 15 | h1 * | -0.017 | -0.030 .. -0.004 | -0.0028 | 0.013 / 0.018 / 0.081 | 0.0583 | 1 | 0.932 | 12/16 | -0.003 | -0.031 | False | -2.2 / -2.5 |  |
| MNQ | 15 | h2 | -0.024 | -0.044 .. -0.003 | -0.0023 | 0.022 / 0.026 / 0.14 | 0.103 |  |  | 10/16 | +0.003 | -0.050 |  | -2.2 / -2.3 |  |
| MNQ | 15 | h4 | -0.019 | -0.049 .. +0.012 | -0.0011 | 0.23 / 0.25 / 0.51 | 0.388 |  |  | 10/16 | -0.012 | -0.025 |  | -1.2 / -1.2 | 0.046 |
| MNQ | 15 | h8 | -0.013 | -0.059 .. +0.034 | -0.0006 | 0.59 / 0.6 / 0.74 | 0.717 |  |  | 9/16 | -0.029 | +0.004 |  | -0.5 / -0.5 |  |
| MNQ | 15 | h16 | +0.019 | -0.053 .. +0.092 | +0.0007 | 0.6 / 0.6 / 0.68 | 0.666 |  |  | 8/16 | -0.005 | +0.044 |  | +0.5 / +0.5 |  |
| MNQ | 15 | eod | -0.036 | -0.274 .. +0.203 | -0.0004 | 0.77 / 0.77 / 0.82 | 0.825 |  |  | 9/16 | +0.047 | -0.118 |  | -0.4 / -0.3 |  |
| MNQ | 60 | h1 | +0.010 | -0.019 .. +0.039 | +0.0020 | 0.51 / 0.52 / 0.55 | 0.562 |  |  | 9/16 | +0.014 | +0.005 |  | +0.7 / +0.7 |  |
| MNQ | 60 | h2 | +0.021 | -0.026 .. +0.067 | +0.0028 | 0.38 / 0.37 / 0.4 | 0.402 |  |  | 8/16 | +0.048 | -0.007 |  | +0.9 / +0.9 |  |
| MNQ | 60 | h4 | +0.012 | -0.057 .. +0.082 | +0.0013 | 0.73 / 0.72 / 0.73 | 0.728 |  |  | 10/16 | +0.029 | -0.004 |  | +0.4 / +0.3 | 0.098 |
| MNQ | 60 | h8 | +0.013 | -0.076 .. +0.102 | +0.0010 | 0.78 / 0.77 / 0.78 | 0.79 |  |  | 10/16 | +0.028 | -0.002 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h16 | +0.014 | -0.117 .. +0.145 | +0.0008 | 0.84 / 0.83 / 0.83 | 0.821 |  |  | 10/16 | +0.030 | -0.002 |  | +0.2 / +0.2 |  |
| MNQ | 60 | eod * | +0.066 | -0.070 .. +0.203 | +0.0035 | 0.34 / 0.33 / 0.35 | 0.353 | 1 | 1 | 11/16 | +0.106 | +0.026 | False | +1.0 / +1.0 |  |
| MYM | 5 | h1 | -0.000 | -0.011 .. +0.011 | +0.0000 | 0.99 / 0.99 / 1 | 0.998 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h2 * | -0.016 | -0.030 .. -0.001 | -0.0016 | 0.032 / 0.046 / 0.24 | 0.18 | 1 | 0.998 | 7/8 | n/a | -0.016 | False | -1.9 / -2.1 |  |
| MYM | 5 | h4 | -0.017 | -0.038 .. +0.003 | -0.0011 | 0.096 / 0.14 / 0.4 | 0.32 |  |  | 6/8 | n/a | -0.017 |  | -1.4 / -1.7 | 0.037 |
| MYM | 5 | h8 | -0.001 | -0.035 .. +0.032 | -0.0000 | 0.94 / 0.94 / 0.98 | 0.968 |  |  | 4/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 5 | h16 | -0.001 | -0.055 .. +0.052 | -0.0000 | 0.96 / 0.96 / 0.97 | 0.967 |  |  | 5/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |
| MYM | 5 | eod | -0.043 | -0.411 .. +0.324 | -0.0003 | 0.82 / 0.83 / 0.85 | 0.855 |  |  | 5/8 | n/a | -0.043 |  | -0.3 / -0.2 |  |
| MYM | 15 | h1 * | -0.016 | -0.034 .. +0.001 | -0.0028 | 0.066 / 0.074 / 0.22 | 0.174 | 1 | 1 | 6/8 | n/a | -0.016 | False | -1.6 / -1.8 |  |
| MYM | 15 | h2 | -0.011 | -0.037 .. +0.014 | -0.0011 | 0.39 / 0.4 / 0.65 | 0.542 |  |  | 5/8 | n/a | -0.011 |  | -0.8 / -0.9 |  |
| MYM | 15 | h4 | -0.020 | -0.061 .. +0.021 | -0.0012 | 0.34 / 0.33 / 0.65 | 0.502 |  |  | 4/8 | n/a | -0.020 |  | -0.9 / -1.0 | 0.065 |
| MYM | 15 | h8 | -0.053 | -0.127 .. +0.021 | -0.0024 | 0.16 / 0.13 / 0.35 | 0.263 |  |  | 5/8 | n/a | -0.053 |  | -1.6 / -1.4 |  |
| MYM | 15 | h16 | -0.021 | -0.122 .. +0.079 | -0.0007 | 0.68 / 0.68 / 0.77 | 0.766 |  |  | 6/8 | n/a | -0.021 |  | -0.4 / -0.4 |  |
| MYM | 15 | eod | -0.127 | -0.431 .. +0.177 | -0.0017 | 0.41 / 0.39 / 0.53 | 0.53 |  |  | 5/8 | n/a | -0.127 |  | -1.1 / -0.8 |  |
| MYM | 60 | h1 | +0.005 | -0.037 .. +0.047 | +0.0010 | 0.82 / 0.82 / 0.83 | 0.822 |  |  | 3/8 | n/a | +0.005 |  | +0.2 / +0.2 |  |
| MYM | 60 | h2 | -0.004 | -0.066 .. +0.057 | -0.0006 | 0.89 / 0.89 / 0.9 | 0.905 |  |  | 4/8 | n/a | -0.004 |  | -0.1 / -0.1 |  |
| MYM | 60 | h4 | +0.013 | -0.065 .. +0.091 | +0.0014 | 0.74 / 0.75 / 0.78 | 0.781 |  |  | 4/8 | n/a | +0.013 |  | +0.3 / +0.3 | 0.128 |
| MYM | 60 | h8 * | +0.041 | -0.069 .. +0.152 | +0.0031 | 0.46 / 0.47 / 0.52 | 0.528 | 1 | 1 | 3/8 | n/a | +0.041 | False | +0.7 / +0.7 |  |
| MYM | 60 | h16 | +0.023 | -0.148 .. +0.193 | +0.0013 | 0.79 / 0.79 / 0.8 | 0.807 |  |  | 4/8 | n/a | +0.023 |  | +0.3 / +0.3 |  |
| MYM | 60 | eod | +0.050 | -0.135 .. +0.234 | +0.0027 | 0.6 / 0.59 / 0.61 | 0.615 |  |  | 4/8 | n/a | +0.050 |  | +0.5 / +0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.005 | -0.012 .. +0.002 | -0.9% | -0.022 | 0.26 |  | 6/16 |
| MES | 5 | h2 | -0.002 | -0.012 .. +0.007 | -0.3% | -0.027 | 0.82 |  | 7/16 |
| MES | 5 | h4 | +0.001 | -0.014 .. +0.015 | +0.1% | -0.033 | 0.93 |  | 9/16 |
| MES | 5 | h8 | -0.016 | -0.036 .. +0.005 | -1.1% | -0.048 | 0.19 |  | 10/16 |
| MES | 5 | h16 | -0.038 | -0.069 .. -0.008 | -1.8% | -0.081 | 0.014 |  | 10/16 |
| MES | 5 | eod * | -0.273 | -0.476 .. -0.070 | -2.7% | -0.561 | 0.0083 | 1 | 9/16 |
| MES | 15 | h1 | -0.005 | -0.015 .. +0.006 | -0.9% | -0.027 | 0.57 |  | 9/16 |
| MES | 15 | h2 | -0.012 | -0.028 .. +0.003 | -1.7% | -0.032 | 0.35 |  | 11/16 |
| MES | 15 | h4 | -0.021 | -0.042 .. -0.001 | -2.0% | -0.055 | 0.27 |  | 12/16 |
| MES | 15 | h8 | -0.009 | -0.042 .. +0.025 | -0.6% | -0.070 | 0.72 |  | 9/16 |
| MES | 15 | h16 | -0.046 | -0.090 .. -0.001 | -2.0% | -0.126 | 0.1 |  | 12/16 |
| MES | 15 | eod * | -0.160 | -0.287 .. -0.033 | -2.9% | -0.281 | 0.015 | 1 | 11/16 |
| MES | 60 | h1 | -0.010 | -0.031 .. +0.011 | -2.0% | -0.021 | 0.68 |  | 9/16 |
| MES | 60 | h2 | -0.031 | -0.060 .. -0.002 | -4.2% | -0.042 | 0.11 |  | 13/16 |
| MES | 60 | h4 | -0.045 | -0.089 .. -0.001 | -4.3% | -0.038 | 0.08 |  | 10/16 |
| MES | 60 | h8 | -0.064 | -0.115 .. -0.014 | -4.3% | -0.063 | 0.059 |  | 13/16 |
| MES | 60 | h16 * | -0.128 | -0.189 .. -0.067 | -6.2% | -0.104 | 0.00027 | 0.0506 | 13/16 |
| MES | 60 | eod | -0.072 | -0.135 .. -0.009 | -3.3% | -0.087 | 0.046 |  | 13/16 |
| MNQ | 5 | h1 | -0.012 | -0.018 .. -0.005 | -2.2% | -0.032 | 0.013 |  | 11/16 |
| MNQ | 5 | h2 | -0.016 | -0.026 .. -0.007 | -2.1% | -0.041 | 0.022 |  | 12/16 |
| MNQ | 5 | h4 | -0.019 | -0.035 .. -0.003 | -1.7% | -0.054 | 0.21 |  | 12/16 |
| MNQ | 5 | h8 | -0.039 | -0.065 .. -0.014 | -2.4% | -0.081 | 0.039 |  | 13/16 |
| MNQ | 5 | h16 | -0.044 | -0.089 .. +0.002 | -1.8% | -0.119 | 0.061 |  | 11/16 |
| MNQ | 5 | eod * | -0.388 | -0.647 .. -0.129 | -3.1% | -0.825 | 0.0033 | 0.508 | 12/16 |
| MNQ | 15 | h1 * | -0.020 | -0.030 .. -0.009 | -3.7% | -0.041 | 0.0018 | 0.291 | 11/16 |
| MNQ | 15 | h2 | -0.023 | -0.040 .. -0.005 | -2.9% | -0.056 | 0.14 |  | 13/16 |
| MNQ | 15 | h4 | -0.037 | -0.068 .. -0.006 | -3.3% | -0.083 | 0.16 |  | 15/16 |
| MNQ | 15 | h8 | -0.050 | -0.094 .. -0.006 | -3.0% | -0.137 | 0.14 |  | 11/16 |
| MNQ | 15 | h16 | -0.062 | -0.122 .. -0.002 | -2.4% | -0.203 | 0.043 |  | 10/16 |
| MNQ | 15 | eod | -0.122 | -0.330 .. +0.086 | -1.9% | -0.311 | 0.25 |  | 8/16 |
| MNQ | 60 | h1 | -0.019 | -0.040 .. +0.002 | -3.5% | -0.030 | 0.079 |  | 11/16 |
| MNQ | 60 | h2 * | -0.042 | -0.073 .. -0.012 | -5.5% | -0.048 | 0.0069 | 0.959 | 14/16 |
| MNQ | 60 | h4 | -0.046 | -0.091 .. -0.001 | -4.2% | -0.064 | 0.056 |  | 11/16 |
| MNQ | 60 | h8 | -0.067 | -0.122 .. -0.012 | -4.2% | -0.089 | 0.049 |  | 12/16 |
| MNQ | 60 | h16 | -0.043 | -0.113 .. +0.027 | -2.0% | -0.054 | 0.27 |  | 7/16 |
| MNQ | 60 | eod | -0.051 | -0.122 .. +0.019 | -2.2% | -0.073 | 0.24 |  | 10/16 |
| MYM | 5 | h1 | -0.013 | -0.021 .. -0.005 | -2.5% | -0.036 | 0.016 |  | 8/8 |
| MYM | 5 | h2 | -0.024 | -0.037 .. -0.011 | -3.1% | -0.048 | 0.025 |  | 8/8 |
| MYM | 5 | h4 | -0.031 | -0.052 .. -0.011 | -2.9% | -0.070 | 0.1 |  | 7/8 |
| MYM | 5 | h8 | -0.037 | -0.074 .. -0.001 | -2.3% | -0.104 | 0.18 |  | 7/8 |
| MYM | 5 | h16 | -0.058 | -0.111 .. -0.004 | -2.5% | -0.154 | 0.072 |  | 7/8 |
| MYM | 5 | eod * | -0.596 | -0.863 .. -0.330 | -5.1% | -0.987 | 1.4e-05 | 0.00318 | 8/8 |
| MYM | 15 | h1 | -0.022 | -0.035 .. -0.008 | -4.1% | -0.048 | 0.12 |  | 6/8 |
| MYM | 15 | h2 | -0.030 | -0.051 .. -0.008 | -3.9% | -0.066 | 0.25 |  | 6/8 |
| MYM | 15 | h4 | -0.051 | -0.088 .. -0.014 | -4.6% | -0.099 | 0.34 |  | 7/8 |
| MYM | 15 | h8 | -0.039 | -0.099 .. +0.020 | -2.4% | -0.128 | 0.48 |  | 5/8 |
| MYM | 15 | h16 | -0.050 | -0.148 .. +0.049 | -2.0% | -0.165 | 0.36 |  | 4/8 |
| MYM | 15 | eod * | -0.288 | -0.532 .. -0.044 | -4.8% | -0.402 | 0.021 | 1 | 7/8 |
| MYM | 60 | h1 | -0.002 | -0.030 .. +0.026 | -0.4% | -0.032 | 0.89 |  | 6/8 |
| MYM | 60 | h2 | -0.015 | -0.054 .. +0.024 | -2.0% | -0.038 | 0.86 |  | 5/8 |
| MYM | 60 | h4 | -0.041 | -0.094 .. +0.011 | -3.8% | -0.046 | 0.48 |  | 6/8 |
| MYM | 60 | h8 | -0.031 | -0.104 .. +0.042 | -2.0% | -0.061 | 0.62 |  | 6/8 |
| MYM | 60 | h16 * | -0.090 | -0.184 .. +0.004 | -4.2% | -0.096 | 0.22 | 1 | 6/8 |
| MYM | 60 | eod | -0.053 | -0.152 .. +0.047 | -2.4% | -0.080 | 0.49 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.39 pts | -0.27 .. +1.05 | 0.26 |
| MES | 15 | +0.51 pts | -0.61 .. +1.63 | 0.38 |
| MES | 60 | +0.12 pts | -2.01 .. +2.25 | 0.91 |
| MNQ | 5 | -0.47 pts | -1.06 .. +0.12 | 0.18 |
| MNQ | 15 | -1.09 pts | -2.07 .. -0.11 | 0.088 |
| MNQ | 60 | +0.17 pts | -1.88 .. +2.21 | 0.87 |
| MYM | 5 | -0.34 pts | -1.06 .. +0.39 | 0.38 |
| MYM | 15 | -0.71 pts | -1.98 .. +0.56 | 0.39 |
| MYM | 60 | +0.17 pts | -2.52 .. +2.86 | 0.9 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 17425 | +0.004 | 0.246 | -0.00 | -3.50 | -3.43 | -3.55 | -3.51 |
| MES | 5 | h2 | event | against signal | 17425 | +0.008 | 0.246 | +0.07 | -3.43 | -3.45 | -3.42 | -3.43 |
| MES | 5 | h4 | event | with signal | 17425 | +0.010 | 0.246 | +0.16 | -3.34 | -3.59 | -3.17 | -3.35 |
| MES | 5 | h8 | event | with signal | 17425 | +0.029 | 0.246 | +0.36 | -3.14 | -3.62 | -2.85 | -3.17 |
| MES | 5 | h16 | event | with signal | 17425 | +0.020 | 0.246 | +0.28 | -3.22 | -3.79 | -2.87 | -3.24 |
| MES | 5 | eod | event | with signal | 17425 | +0.176 | 0.246 | -0.63 | -4.13 | -2.92 | -4.88 | -6.37 |
| MES | 15 | h1 | event | against signal | 7129 | +0.012 | 0.156 | +0.28 | -3.22 | -3.47 | -3.03 | -3.24 |
| MES | 15 | h2 | event | against signal | 7129 | +0.013 | 0.156 | +0.42 | -3.08 | -3.62 | -2.67 | -3.08 |
| MES | 15 | h4 | event | against signal | 7129 | +0.022 | 0.156 | +0.85 | -2.65 | -3.47 | -2.03 | -2.60 |
| MES | 15 | h8 | event | against signal | 7129 | +0.017 | 0.156 | +0.79 | -2.71 | -3.59 | -2.04 | -2.56 |
| MES | 15 | h16 | event | with signal | 7129 | +0.088 | 0.156 | +1.46 | -2.04 | -3.00 | -1.32 | -2.58 |
| MES | 15 | eod | event | with signal | 7129 | +0.104 | 0.156 | -0.26 | -3.76 | -2.89 | -4.41 | -5.69 |
| MES | 60 | h1 | event | with signal | 2042 | +0.003 | 0.089 | +0.01 | -3.49 | -3.17 | -3.77 | -3.51 |
| MES | 60 | h2 | event | against signal | 2042 | +0.010 | 0.089 | +0.54 | -2.96 | -3.43 | -2.54 | -2.87 |
| MES | 60 | h4 | event | against signal | 2042 | -0.007 | 0.089 | +1.08 | -2.42 | -3.89 | -1.08 | -2.27 |
| MES | 60 | h8 | event | with signal | 2042 | +0.063 | 0.089 | +0.11 | -3.39 | -2.01 | -4.65 | -3.68 |
| MES | 60 | h16 | event | with signal | 2042 | +0.094 | 0.089 | +0.84 | -2.66 | -1.72 | -3.52 | -3.28 |
| MES | 60 | eod | event | with signal | 2042 | +0.115 | 0.089 | +2.10 | -1.40 | -1.52 | -1.30 | -1.87 |
| MNQ | 5 | h1 | event | against signal | 25843 | +0.001 | 0.107 | +0.07 | -1.93 | -1.96 | -1.90 | -1.91 |
| MNQ | 5 | h2 | event | against signal | 25843 | +0.010 | 0.107 | +0.27 | -1.73 | -1.93 | -1.60 | -1.68 |
| MNQ | 5 | h4 | event | against signal | 25843 | +0.012 | 0.107 | +0.17 | -1.83 | -1.93 | -1.76 | -1.71 |
| MNQ | 5 | h8 | event | against signal | 25843 | -0.002 | 0.107 | +0.47 | -1.53 | -2.03 | -1.20 | -1.35 |
| MNQ | 5 | h16 | event | with signal | 25843 | +0.026 | 0.107 | +0.08 | -1.92 | -2.02 | -1.84 | -2.19 |
| MNQ | 5 | eod | event | against signal | 25843 | -0.258 | 0.107 | -1.08 | -3.08 | -1.82 | -3.92 | +2.33 |
| MNQ | 15 | h1 | event | against signal | 8854 | +0.017 | 0.064 | +0.59 | -1.41 | -1.90 | -1.02 | -1.44 |
| MNQ | 15 | h2 | event | against signal | 8854 | +0.023 | 0.064 | +1.09 | -0.91 | -1.95 | -0.11 | -0.96 |
| MNQ | 15 | h4 | event | against signal | 8854 | +0.016 | 0.064 | +1.17 | -0.83 | -1.70 | -0.16 | -0.84 |
| MNQ | 15 | h8 | event | against signal | 8854 | +0.001 | 0.064 | +0.05 | -1.95 | -1.62 | -2.21 | -1.78 |
| MNQ | 15 | h16 | event | with signal | 8854 | +0.054 | 0.064 | +2.05 | +0.05 | -1.97 | +1.62 | -0.73 |
| MNQ | 15 | eod | event | against signal | 8854 | -0.089 | 0.064 | +2.43 | +0.43 | -1.73 | +2.11 | +3.28 |
| MNQ | 60 | h1 | event | with signal | 2180 | +0.016 | 0.035 | +0.06 | -1.94 | -1.69 | -2.17 | -2.14 |
| MNQ | 60 | h2 | event | with signal | 2180 | +0.031 | 0.035 | -1.09 | -3.09 | -1.67 | -4.38 | -3.46 |
| MNQ | 60 | h4 | event | with signal | 2180 | +0.033 | 0.035 | -1.70 | -3.70 | -1.70 | -5.50 | -4.39 |
| MNQ | 60 | h8 | event | with signal | 2180 | +0.047 | 0.035 | -2.17 | -4.17 | -1.69 | -6.40 | -5.20 |
| MNQ | 60 | h16 | event | with signal | 2180 | +0.070 | 0.035 | -1.77 | -3.77 | -0.51 | -6.71 | -5.54 |
| MNQ | 60 | eod | event | with signal | 2180 | +0.130 | 0.035 | +0.53 | -1.47 | +1.05 | -3.75 | -3.36 |
| MYM | 5 | h1 | event | against signal | 14047 | +0.000 | 0.155 | +0.07 | -1.93 | +nan | -1.93 | -1.93 |
| MYM | 5 | h2 | event | against signal | 14047 | +0.013 | 0.155 | +0.22 | -1.78 | +nan | -1.78 | -1.74 |
| MYM | 5 | h4 | event | against signal | 14047 | +0.008 | 0.155 | +0.28 | -1.72 | +nan | -1.72 | -1.57 |
| MYM | 5 | h8 | event | against signal | 14047 | -0.015 | 0.155 | +0.16 | -1.84 | +nan | -1.84 | -1.56 |
| MYM | 5 | h16 | event | against signal | 14047 | -0.024 | 0.155 | +0.19 | -1.81 | +nan | -1.81 | -1.41 |
| MYM | 5 | eod | event | against signal | 14047 | -0.095 | 0.155 | +0.28 | -1.72 | +nan | -1.72 | +0.02 |
| MYM | 15 | h1 | event | against signal | 4683 | +0.015 | 0.089 | +0.49 | -1.51 | +nan | -1.51 | -1.47 |
| MYM | 15 | h2 | event | against signal | 4683 | +0.009 | 0.089 | +0.55 | -1.45 | +nan | -1.45 | -1.38 |
| MYM | 15 | h4 | event | against signal | 4683 | +0.015 | 0.089 | +0.86 | -1.14 | +nan | -1.14 | -0.99 |
| MYM | 15 | h8 | event | against signal | 4683 | +0.041 | 0.089 | +1.43 | -0.57 | +nan | -0.57 | -0.20 |
| MYM | 15 | h16 | event | against signal | 4683 | +0.005 | 0.089 | +0.48 | -1.52 | +nan | -1.52 | -0.97 |
| MYM | 15 | eod | event | against signal | 4683 | +0.072 | 0.089 | +2.91 | +0.91 | +nan | +0.91 | +1.96 |
| MYM | 60 | h1 | event | with signal | 1097 | +0.007 | 0.046 | -0.07 | -2.07 | +nan | -2.07 | -2.16 |
| MYM | 60 | h2 | event | against signal | 1097 | +0.000 | 0.046 | +0.57 | -1.43 | +nan | -1.43 | -1.30 |
| MYM | 60 | h4 | event | with signal | 1097 | +0.021 | 0.046 | -1.11 | -3.11 | +nan | -3.11 | -3.36 |
| MYM | 60 | h8 | event | with signal | 1097 | +0.056 | 0.046 | -0.41 | -2.41 | +nan | -2.41 | -2.84 |
| MYM | 60 | h16 | event | with signal | 1097 | +0.046 | 0.046 | -1.53 | -3.53 | +nan | -3.53 | -4.17 |
| MYM | 60 | eod | event | with signal | 1097 | +0.071 | 0.046 | -1.09 | -3.09 | +nan | -3.09 | -3.48 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.515 | +0.885 | -0.227 | -0.141 | -0.032 | +0.000 | -0.003 | -0.008 | +0.009 | +0.027 | +0.011 |
| MES | 15 | +0.496 | +0.946 | -0.190 | -0.115 | -0.024 | +0.000 | -0.009 | -0.011 | -0.023 | -0.025 | +0.076 |
| MES | 60 | +1.191 | +1.021 | -0.100 | -0.073 | +0.003 | +0.000 | +0.004 | -0.009 | +0.004 | +0.075 | +0.100 |
| MNQ | 5 | +0.492 | +1.002 | -0.167 | -0.113 | -0.020 | +0.000 | -0.003 | -0.014 | -0.018 | -0.008 | +0.006 |
| MNQ | 15 | +0.452 | +0.984 | -0.156 | -0.110 | -0.025 | +0.000 | -0.016 | -0.024 | -0.021 | -0.013 | +0.037 |
| MNQ | 60 | +1.415 | +1.034 | -0.099 | -0.071 | -0.014 | +0.000 | +0.013 | +0.024 | +0.019 | +0.020 | +0.094 |
| MYM | 5 | +0.491 | +0.999 | -0.193 | -0.120 | -0.022 | +0.000 | -0.002 | -0.019 | -0.020 | -0.006 | -0.007 |
| MYM | 15 | +0.456 | +0.983 | -0.160 | -0.094 | -0.017 | +0.000 | -0.015 | -0.011 | -0.020 | -0.058 | -0.042 |
| MYM | 60 | +1.230 | +1.043 | -0.107 | -0.040 | +0.006 | +0.000 | +0.001 | -0.008 | +0.025 | +0.070 | -0.060 |

## Calibration

- MES 5-min: 1036271 bars, 17425 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 7129 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 2042 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 25843 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 8854 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 2180 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 14047 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 4683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1097 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
