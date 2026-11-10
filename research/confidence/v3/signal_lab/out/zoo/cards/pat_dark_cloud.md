# Impact card: pat_dark_cloud

candle pattern dark_cloud in its textbook direction: mirror of piercing -> bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.013 R20 over the next 1 bar (5 min), p=0.61; we would catch an effect of 0.036 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.12).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.23 at recent bar sizes, 90% range up to $0.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.127 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.067 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.48 at recent bar sizes, 90% range up to $2.36); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.032 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.139 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.78 at recent bar sizes, 90% range up to $7.61); about 12.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.039 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.040 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.015 R20, possible, q=0.26, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.95 at recent bar sizes, 90% range up to $1.16); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.207 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.97 at recent bar sizes, 90% range up to $3.86); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.050 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.153 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.7).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.23 at recent bar sizes, 90% range up to $15.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: POSSIBLE direction effect +0.030 average bars (~$0.36 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.122, replicated in the other half=False, 8 of 8 years); best leg (event, with signal) grosses $+0.29 and nets $-1.71 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 5-min size: no measurable effect on how much price moves (best p=0.78).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.36 at recent bar sizes, 90% range up to $0.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.068 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.096 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.34 at recent bar sizes, 90% range up to $1.87); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.143 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.205 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.68).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.91 at recent bar sizes, 90% range up to $13.11); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.013 | -0.000 .. +0.027 | +0.0021 | 0.053 / 0.05 / 0.044 | 0.0448 | 1 | 1 | 10/16 | -0.010 | +0.036 | False | +1.9 / +1.9 |  |
| MES | 5 | h2 | +0.016 | -0.002 .. +0.033 | +0.0017 | 0.088 / 0.086 / 0.094 | 0.092 |  |  | 10/16 | -0.002 | +0.033 |  | +1.7 / +1.7 |  |
| MES | 5 | h4 | +0.008 | -0.017 .. +0.032 | +0.0006 | 0.53 / 0.53 / 0.54 | 0.536 |  |  | 11/16 | -0.013 | +0.029 |  | +0.6 / +0.6 | 0.036 |
| MES | 5 | h8 | +0.001 | -0.035 .. +0.038 | +0.0001 | 0.95 / 0.95 / 0.94 | 0.942 |  |  | 9/16 | -0.018 | +0.020 |  | +0.1 / +0.1 |  |
| MES | 5 | h16 | -0.022 | -0.077 .. +0.033 | -0.0008 | 0.43 / 0.45 / 0.43 | 0.426 |  |  | 10/16 | -0.017 | -0.027 |  | -0.8 / -0.8 |  |
| MES | 5 | eod | -0.168 | -0.616 .. +0.279 | -0.0012 | 0.46 / 0.48 / 0.22 | 0.227 |  |  | 13/16 | -0.080 | -0.256 |  | -1.4 / -0.7 |  |
| MES | 15 | h1 | +0.005 | -0.020 .. +0.030 | +0.0008 | 0.71 / 0.71 / 0.68 | 0.663 |  |  | 11/16 | +0.030 | -0.020 |  | +0.4 / +0.4 |  |
| MES | 15 | h2 | -0.001 | -0.037 .. +0.035 | -0.0001 | 0.95 / 0.94 / 0.94 | 0.94 |  |  | 6/16 | +0.018 | -0.020 |  | -0.1 / -0.1 |  |
| MES | 15 | h4 | +0.007 | -0.043 .. +0.058 | +0.0005 | 0.77 / 0.77 / 0.78 | 0.757 |  |  | 8/16 | +0.055 | -0.040 |  | +0.3 / +0.3 | 0.067 |
| MES | 15 | h8 | +0.026 | -0.046 .. +0.097 | +0.0013 | 0.48 / 0.48 / 0.47 | 0.465 |  |  | 10/16 | +0.108 | -0.056 |  | +0.8 / +0.7 |  |
| MES | 15 | h16 | -0.014 | -0.116 .. +0.087 | -0.0005 | 0.78 / 0.78 / 0.77 | 0.773 |  |  | 11/16 | +0.037 | -0.066 |  | -0.3 / -0.3 |  |
| MES | 15 | eod * | -0.127 | -0.422 .. +0.169 | -0.0017 | 0.4 / 0.41 / 0.3 | 0.302 | 1 | 1 | 11/16 | +0.038 | -0.290 | False | -1.2 / -0.8 |  |
| MES | 60 | h1 | +0.008 | -0.039 .. +0.054 | +0.0013 | 0.75 / 0.75 / 0.75 | 0.742 |  |  | 6/16 | -0.023 | +0.038 |  | +0.3 / +0.3 |  |
| MES | 60 | h2 | +0.010 | -0.058 .. +0.077 | +0.0012 | 0.78 / 0.78 / 0.77 | 0.774 |  |  | 10/16 | -0.027 | +0.046 |  | +0.3 / +0.3 |  |
| MES | 60 | h4 * | -0.032 | -0.126 .. +0.062 | -0.0027 | 0.5 / 0.52 / 0.5 | 0.505 | 1 | 1 | 9/16 | -0.044 | -0.020 | False | -0.7 / -0.7 | 0.139 |
| MES | 60 | h8 | -0.015 | -0.145 .. +0.115 | -0.0009 | 0.82 / 0.83 / 0.81 | 0.81 |  |  | 9/16 | -0.044 | +0.015 |  | -0.2 / -0.2 |  |
| MES | 60 | h16 | -0.039 | -0.192 .. +0.114 | -0.0018 | 0.62 / 0.62 / 0.59 | 0.591 |  |  | 11/16 | -0.071 | -0.007 |  | -0.5 / -0.5 |  |
| MES | 60 | eod | -0.022 | -0.177 .. +0.133 | -0.0010 | 0.78 / 0.79 / 0.77 | 0.763 |  |  | 11/16 | -0.056 | +0.012 |  | -0.3 / -0.3 |  |
| MNQ | 5 | h1 | +0.005 | -0.007 .. +0.016 | +0.0007 | 0.41 / 0.43 / 0.51 | 0.466 |  |  | 8/16 | -0.002 | +0.011 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h2 | +0.013 | -0.004 .. +0.031 | +0.0011 | 0.14 / 0.15 / 0.26 | 0.215 |  |  | 10/16 | -0.006 | +0.032 |  | +1.5 / +1.5 |  |
| MNQ | 5 | h4 | +0.014 | -0.010 .. +0.038 | +0.0008 | 0.26 / 0.26 / 0.44 | 0.374 |  |  | 12/16 | -0.004 | +0.031 |  | +1.1 / +1.1 | 0.040 |
| MNQ | 5 | h8 | +0.016 | -0.021 .. +0.053 | +0.0006 | 0.4 / 0.41 / 0.57 | 0.525 |  |  | 9/16 | +0.011 | +0.020 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h16 * | +0.039 | -0.018 .. +0.096 | +0.0010 | 0.18 / 0.19 / 0.31 | 0.305 | 1 | 1 | 12/16 | +0.021 | +0.056 | False | +1.4 / +1.3 |  |
| MNQ | 5 | eod | +0.055 | -0.419 .. +0.529 | +0.0003 | 0.82 / 0.83 / 0.73 | 0.736 |  |  | 9/16 | +0.027 | +0.083 |  | +0.4 / +0.2 |  |
| MNQ | 15 | h1 | +0.003 | -0.024 .. +0.030 | +0.0003 | 0.84 / 0.84 / 0.86 | 0.828 |  |  | 6/16 | -0.018 | +0.023 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h2 | +0.010 | -0.024 .. +0.044 | +0.0008 | 0.57 / 0.58 / 0.7 | 0.606 |  |  | 10/16 | +0.000 | +0.019 |  | +0.5 / +0.6 |  |
| MNQ | 15 | h4 | +0.030 | -0.020 .. +0.080 | +0.0014 | 0.24 / 0.23 / 0.46 | 0.338 |  |  | 10/16 | +0.041 | +0.018 |  | +1.2 / +1.2 | 0.076 |
| MNQ | 15 | h8 | +0.025 | -0.051 .. +0.101 | +0.0009 | 0.51 / 0.51 / 0.62 | 0.555 |  |  | 8/16 | +0.070 | -0.019 |  | +0.7 / +0.7 |  |
| MNQ | 15 | h16 | +0.032 | -0.085 .. +0.148 | +0.0009 | 0.59 / 0.58 / 0.62 | 0.609 |  |  | 10/16 | +0.111 | -0.048 |  | +0.6 / +0.5 |  |
| MNQ | 15 | eod * | -0.207 | -0.537 .. +0.123 | -0.0020 | 0.22 / 0.24 / 0.22 | 0.219 | 1 | 1 | 9/16 | +0.200 | -0.612 | False | -1.6 / -1.2 |  |
| MNQ | 60 | h1 | +0.010 | -0.043 .. +0.063 | +0.0015 | 0.72 / 0.71 / 0.72 | 0.719 |  |  | 8/16 | -0.006 | +0.025 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h2 | -0.008 | -0.085 .. +0.068 | -0.0009 | 0.83 / 0.83 / 0.82 | 0.82 |  |  | 11/16 | +0.016 | -0.032 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h4 | -0.000 | -0.117 .. +0.116 | -0.0000 | 1 / 1 / 0.99 | 0.995 |  |  | 8/16 | -0.030 | +0.029 |  | -0.0 / -0.0 | 0.153 |
| MNQ | 60 | h8 * | +0.050 | -0.102 .. +0.202 | +0.0028 | 0.52 / 0.52 / 0.47 | 0.459 | 1 | 1 | 10/16 | +0.090 | +0.011 | False | +0.7 / +0.6 |  |
| MNQ | 60 | h16 | +0.008 | -0.170 .. +0.185 | +0.0003 | 0.93 / 0.93 / 0.92 | 0.924 |  |  | 11/16 | +0.088 | -0.073 |  | +0.1 / +0.1 |  |
| MNQ | 60 | eod | +0.009 | -0.171 .. +0.189 | +0.0004 | 0.92 / 0.92 / 0.91 | 0.914 |  |  | 11/16 | +0.090 | -0.073 |  | +0.1 / +0.1 |  |
| MYM | 5 | h1 * | +0.030 | +0.014 .. +0.047 | +0.0040 | 0.00022 / 0.00019 / 0.0053 | 0.0184 | 0.122 | 0.078 | 8/8 | n/a | +0.030 | False | +3.6 / +3.7 |  |
| MYM | 5 | h2 | +0.025 | +0.001 .. +0.048 | +0.0020 | 0.04 / 0.044 / 0.19 | 0.129 |  |  | 6/8 | n/a | +0.025 |  | +1.9 / +2.1 |  |
| MYM | 5 | h4 | +0.043 | +0.009 .. +0.078 | +0.0021 | 0.014 / 0.015 / 0.14 | 0.125 |  |  | 7/8 | n/a | +0.043 |  | +2.3 / +2.5 | 0.053 |
| MYM | 5 | h8 | +0.033 | -0.020 .. +0.086 | +0.0011 | 0.23 / 0.24 / 0.44 | 0.391 |  |  | 5/8 | n/a | +0.033 |  | +1.2 / +1.2 |  |
| MYM | 5 | h16 | +0.007 | -0.081 .. +0.095 | +0.0002 | 0.87 / 0.87 / 0.91 | 0.899 |  |  | 4/8 | n/a | +0.007 |  | +0.2 / +0.2 |  |
| MYM | 5 | eod | -0.024 | -0.791 .. +0.743 | -0.0002 | 0.95 / 0.95 / 0.91 | 0.907 |  |  | 4/8 | n/a | -0.024 |  | -0.1 / -0.1 |  |
| MYM | 15 | h1 | -0.004 | -0.035 .. +0.028 | -0.0005 | 0.82 / 0.82 / 0.85 | 0.827 |  |  | 4/8 | n/a | -0.004 |  | -0.2 / -0.2 |  |
| MYM | 15 | h2 | +0.016 | -0.027 .. +0.059 | +0.0012 | 0.46 / 0.46 / 0.62 | 0.524 |  |  | 6/8 | n/a | +0.016 |  | +0.7 / +0.7 |  |
| MYM | 15 | h4 | -0.007 | -0.067 .. +0.053 | -0.0003 | 0.81 / 0.82 / 0.89 | 0.827 |  |  | 5/8 | n/a | -0.007 |  | -0.2 / -0.2 | 0.096 |
| MYM | 15 | h8 | +0.003 | -0.094 .. +0.100 | +0.0001 | 0.95 / 0.95 / 0.97 | 0.967 |  |  | 5/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |
| MYM | 15 | h16 * | -0.068 | -0.228 .. +0.092 | -0.0017 | 0.41 / 0.38 / 0.5 | 0.467 | 1 | 1 | 4/8 | n/a | -0.068 | False | -1.0 / -0.8 |  |
| MYM | 15 | eod | +0.014 | -0.438 .. +0.466 | +0.0001 | 0.95 / 0.95 / 0.96 | 0.956 |  |  | 5/8 | n/a | +0.014 |  | +0.1 / +0.1 |  |
| MYM | 60 | h1 | +0.050 | -0.030 .. +0.131 | +0.0080 | 0.22 / 0.24 / 0.15 | 0.144 |  |  | 5/8 | n/a | +0.050 |  | +1.2 / +1.2 |  |
| MYM | 60 | h2 | +0.077 | -0.038 .. +0.193 | +0.0087 | 0.19 / 0.2 / 0.11 | 0.105 |  |  | 7/8 | n/a | +0.077 |  | +1.3 / +1.3 |  |
| MYM | 60 | h4 | +0.017 | -0.146 .. +0.179 | +0.0013 | 0.84 / 0.84 / 0.81 | 0.796 |  |  | 4/8 | n/a | +0.017 |  | +0.2 / +0.2 | 0.205 |
| MYM | 60 | h8 * | +0.143 | -0.063 .. +0.350 | +0.0083 | 0.17 / 0.18 / 0.12 | 0.113 | 1 | 1 | 6/8 | n/a | +0.143 | False | +1.4 / +1.4 |  |
| MYM | 60 | h16 | +0.105 | -0.137 .. +0.347 | +0.0047 | 0.39 / 0.39 / 0.32 | 0.324 |  |  | 5/8 | n/a | +0.105 |  | +0.9 / +0.9 |  |
| MYM | 60 | eod | +0.105 | -0.139 .. +0.348 | +0.0044 | 0.4 / 0.4 / 0.34 | 0.335 |  |  | 4/8 | n/a | +0.105 |  | +0.9 / +0.8 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.006 | -0.003 .. +0.015 | +1.2% | -0.011 | 0.26 |  | 11/16 |
| MES | 5 | h2 | +0.003 | -0.010 .. +0.015 | +0.4% | -0.013 | 0.67 |  | 9/16 |
| MES | 5 | h4 | -0.003 | -0.021 .. +0.015 | -0.3% | -0.020 | 0.82 |  | 6/16 |
| MES | 5 | h8 | -0.018 | -0.043 .. +0.007 | -1.3% | -0.041 | 0.25 |  | 11/16 |
| MES | 5 | h16 * | -0.045 | -0.082 .. -0.007 | -2.1% | -0.074 | 0.02 | 1 | 10/16 |
| MES | 5 | eod | -0.076 | -0.291 .. +0.139 | -0.8% | -0.289 | 0.49 |  | 7/16 |
| MES | 15 | h1 | +0.002 | -0.016 .. +0.020 | +0.4% | -0.010 | 0.93 |  | 9/16 |
| MES | 15 | h2 | +0.009 | -0.015 .. +0.032 | +1.2% | -0.004 | 0.6 |  | 8/16 |
| MES | 15 | h4 | -0.012 | -0.043 .. +0.019 | -1.1% | -0.017 | 0.48 |  | 8/16 |
| MES | 15 | h8 * | -0.028 | -0.071 .. +0.015 | -1.8% | -0.049 | 0.21 | 1 | 9/16 |
| MES | 15 | h16 | -0.035 | -0.097 .. +0.027 | -1.5% | -0.039 | 0.27 |  | 8/16 |
| MES | 15 | eod | -0.099 | -0.273 .. +0.074 | -1.8% | -0.178 | 0.26 |  | 8/16 |
| MES | 60 | h1 | -0.005 | -0.033 .. +0.023 | -0.9% | -0.009 | 0.75 |  | 9/16 |
| MES | 60 | h2 * | +0.027 | -0.018 .. +0.071 | +3.6% | +0.009 | 0.46 | 1 | 11/16 |
| MES | 60 | h4 | -0.002 | -0.063 .. +0.059 | -0.2% | -0.047 | 0.96 |  | 9/16 |
| MES | 60 | h8 | -0.001 | -0.087 .. +0.086 | -0.0% | -0.039 | 0.99 |  | 8/16 |
| MES | 60 | h16 | -0.027 | -0.125 .. +0.070 | -1.3% | -0.062 | 0.58 |  | 9/16 |
| MES | 60 | eod | -0.025 | -0.119 .. +0.068 | -1.2% | -0.064 | 0.66 |  | 9/16 |
| MNQ | 5 | h1 * | -0.015 | -0.024 .. -0.007 | -2.9% | -0.033 | 0.0016 | 0.26 | 14/16 |
| MNQ | 5 | h2 | -0.014 | -0.026 .. -0.002 | -1.8% | -0.036 | 0.14 |  | 12/16 |
| MNQ | 5 | h4 | -0.029 | -0.049 .. -0.009 | -2.6% | -0.052 | 0.056 |  | 12/16 |
| MNQ | 5 | h8 | -0.053 | -0.088 .. -0.019 | -3.3% | -0.064 | 0.03 |  | 13/16 |
| MNQ | 5 | h16 | -0.066 | -0.120 .. -0.012 | -2.8% | -0.095 | 0.02 |  | 12/16 |
| MNQ | 5 | eod | -0.346 | -0.643 .. -0.049 | -2.8% | -0.703 | 0.022 |  | 11/16 |
| MNQ | 15 | h1 | -0.004 | -0.023 .. +0.015 | -0.7% | -0.009 | 0.7 |  | 11/16 |
| MNQ | 15 | h2 | -0.001 | -0.027 .. +0.025 | -0.1% | -0.014 | 0.98 |  | 9/16 |
| MNQ | 15 | h4 | -0.001 | -0.045 .. +0.042 | -0.1% | +0.000 | 0.95 |  | 8/16 |
| MNQ | 15 | h8 * | +0.019 | -0.044 .. +0.081 | +1.1% | +0.001 | 0.68 | 1 | 10/16 |
| MNQ | 15 | h16 | -0.007 | -0.084 .. +0.069 | -0.3% | -0.029 | 0.85 |  | 7/16 |
| MNQ | 15 | eod | +0.018 | -0.217 .. +0.253 | +0.3% | -0.023 | 0.99 |  | 10/16 |
| MNQ | 60 | h1 * | -0.027 | -0.060 .. +0.007 | -5.1% | +0.000 | 0.12 | 1 | 10/16 |
| MNQ | 60 | h2 | -0.018 | -0.067 .. +0.031 | -2.3% | -0.012 | 0.48 |  | 9/16 |
| MNQ | 60 | h4 | +0.004 | -0.077 .. +0.085 | +0.4% | -0.019 | 0.96 |  | 6/16 |
| MNQ | 60 | h8 | +0.003 | -0.094 .. +0.101 | +0.2% | +0.011 | 0.95 |  | 6/16 |
| MNQ | 60 | h16 | -0.001 | -0.110 .. +0.108 | -0.0% | +0.021 | 0.99 |  | 10/16 |
| MNQ | 60 | eod | -0.013 | -0.120 .. +0.094 | -0.6% | +0.009 | 0.99 |  | 10/16 |
| MYM | 5 | h1 * | -0.013 | -0.024 .. -0.002 | -2.5% | -0.034 | 0.13 | 1 | 8/8 |
| MYM | 5 | h2 | +0.002 | -0.017 .. +0.021 | +0.3% | -0.025 | 0.84 |  | 3/8 |
| MYM | 5 | h4 | -0.000 | -0.030 .. +0.030 | -0.0% | -0.021 | 0.98 |  | 3/8 |
| MYM | 5 | h8 | +0.000 | -0.048 .. +0.048 | +0.0% | -0.019 | 0.99 |  | 3/8 |
| MYM | 5 | h16 | +0.007 | -0.067 .. +0.080 | +0.3% | +0.001 | 0.91 |  | 4/8 |
| MYM | 5 | eod | -0.018 | -0.356 .. +0.319 | -0.2% | -0.107 | 0.99 |  | 3/8 |
| MYM | 15 | h1 * | -0.010 | -0.034 .. +0.013 | -1.9% | -0.021 | 0.39 | 1 | 6/8 |
| MYM | 15 | h2 | -0.007 | -0.045 .. +0.030 | -0.9% | -0.023 | 0.71 |  | 3/8 |
| MYM | 15 | h4 | -0.031 | -0.087 .. +0.025 | -2.8% | -0.013 | 0.41 |  | 5/8 |
| MYM | 15 | h8 | -0.019 | -0.089 .. +0.051 | -1.1% | -0.037 | 0.61 |  | 5/8 |
| MYM | 15 | h16 | -0.039 | -0.157 .. +0.080 | -1.6% | -0.023 | 0.52 |  | 3/8 |
| MYM | 15 | eod | -0.036 | -0.313 .. +0.241 | -0.6% | -0.004 | 0.8 |  | 4/8 |
| MYM | 60 | h1 | +0.024 | -0.032 .. +0.079 | +4.5% | +0.004 | 0.42 |  | 4/8 |
| MYM | 60 | h2 * | +0.067 | -0.015 .. +0.150 | +8.9% | +0.043 | 0.11 | 1 | 6/8 |
| MYM | 60 | h4 | +0.070 | -0.049 .. +0.190 | +6.5% | +0.078 | 0.26 |  | 5/8 |
| MYM | 60 | h8 | +0.070 | -0.072 .. +0.213 | +4.5% | +0.061 | 0.33 |  | 4/8 |
| MYM | 60 | h16 | +0.071 | -0.078 .. +0.220 | +3.4% | +0.053 | 0.35 |  | 5/8 |
| MYM | 60 | eod | +0.063 | -0.082 .. +0.209 | +2.8% | +0.045 | 0.4 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +1.16 pts | +0.39 .. +1.92 | 0.014 |
| MES | 15 | +1.05 pts | -0.21 .. +2.32 | 0.11 |
| MES | 60 | -0.84 pts | -3.34 .. +1.67 | 0.52 |
| MNQ | 5 | +0.76 pts | +0.01 .. +1.51 | 0.062 |
| MNQ | 15 | +0.12 pts | -1.13 .. +1.36 | 0.93 |
| MNQ | 60 | +1.08 pts | -1.43 .. +3.58 | 0.44 |
| MYM | 5 | +0.95 pts | -0.17 .. +2.07 | 0.098 |
| MYM | 15 | +0.62 pts | -1.23 .. +2.47 | 0.51 |
| MYM | 60 | +1.72 pts | -1.66 .. +5.11 | 0.34 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 12823 | +0.001 | 0.256 | +0.19 | -3.31 | -3.68 | -3.09 | -3.15 |
| MES | 5 | h2 | event | with signal | 12823 | -0.004 | 0.256 | +0.10 | -3.40 | -3.64 | -3.25 | -3.16 |
| MES | 5 | h4 | event | with signal | 12823 | -0.018 | 0.256 | -0.00 | -3.50 | -3.80 | -3.33 | -3.23 |
| MES | 5 | h8 | event | with signal | 12823 | -0.033 | 0.256 | -0.35 | -3.85 | -3.99 | -3.76 | -3.52 |
| MES | 5 | h16 | event | against signal | 12823 | +0.079 | 0.256 | +0.84 | -2.66 | -3.02 | -2.45 | -3.18 |
| MES | 5 | eod | event | against signal | 12823 | +0.590 | 0.256 | +6.01 | +2.51 | +0.46 | +3.71 | +1.55 |
| MES | 15 | h1 | event | with signal | 5151 | -0.008 | 0.172 | -0.29 | -3.79 | -3.39 | -4.10 | -3.58 |
| MES | 15 | h2 | event | against signal | 5151 | +0.020 | 0.172 | +0.46 | -3.04 | -3.41 | -2.76 | -3.34 |
| MES | 15 | h4 | event | with signal | 5151 | -0.021 | 0.172 | -0.47 | -3.97 | -3.30 | -4.47 | -3.57 |
| MES | 15 | h8 | event | with signal | 5151 | -0.024 | 0.172 | -0.68 | -4.18 | -2.93 | -5.13 | -3.56 |
| MES | 15 | h16 | event | against signal | 5151 | +0.107 | 0.172 | +1.82 | -1.68 | -2.52 | -1.04 | -2.65 |
| MES | 15 | eod | event | against signal | 5151 | +0.381 | 0.172 | +6.28 | +2.78 | +0.20 | +4.75 | +1.89 |
| MES | 60 | h1 | event | with signal | 1374 | -0.003 | 0.091 | +0.29 | -3.21 | -4.07 | -2.42 | -2.94 |
| MES | 60 | h2 | event | with signal | 1374 | -0.015 | 0.091 | +1.01 | -2.49 | -3.83 | -1.25 | -1.80 |
| MES | 60 | h4 | event | against signal | 1374 | +0.078 | 0.091 | +2.04 | -1.46 | -2.37 | -0.62 | -2.67 |
| MES | 60 | h8 | event | against signal | 1374 | +0.095 | 0.091 | +3.92 | +0.42 | -0.69 | +1.44 | -1.62 |
| MES | 60 | h16 | event | against signal | 1374 | +0.131 | 0.091 | +4.02 | +0.52 | +0.90 | +0.16 | -1.37 |
| MES | 60 | eod | event | against signal | 1374 | +0.122 | 0.091 | +3.83 | +0.33 | +0.94 | -0.23 | -1.76 |
| MNQ | 5 | h1 | event | with signal | 14960 | -0.004 | 0.125 | -0.06 | -2.06 | -2.07 | -2.06 | -1.97 |
| MNQ | 5 | h2 | event | with signal | 14960 | -0.004 | 0.125 | +0.03 | -1.97 | -2.12 | -1.85 | -1.80 |
| MNQ | 5 | h4 | event | with signal | 14960 | -0.009 | 0.125 | -0.10 | -2.10 | -2.20 | -2.02 | -1.95 |
| MNQ | 5 | h8 | event | with signal | 14960 | -0.018 | 0.125 | -0.31 | -2.31 | -2.16 | -2.44 | -2.17 |
| MNQ | 5 | h16 | event | with signal | 14960 | -0.028 | 0.125 | -0.11 | -2.11 | -2.34 | -1.92 | -1.76 |
| MNQ | 5 | eod | event | with signal | 14960 | -0.716 | 0.125 | -5.89 | -7.89 | -6.01 | -9.44 | -5.85 |
| MNQ | 15 | h1 | event | with signal | 5487 | -0.007 | 0.076 | +0.47 | -1.53 | -2.18 | -0.90 | -1.35 |
| MNQ | 15 | h2 | event | with signal | 5487 | -0.004 | 0.076 | +0.65 | -1.35 | -2.13 | -0.60 | -1.17 |
| MNQ | 15 | h4 | event | with signal | 5487 | +0.005 | 0.076 | +1.21 | -0.79 | -2.00 | +0.38 | -0.52 |
| MNQ | 15 | h8 | event | with signal | 5487 | -0.024 | 0.076 | +0.07 | -1.93 | -2.33 | -1.54 | -1.40 |
| MNQ | 15 | h16 | event | with signal | 5487 | -0.071 | 0.076 | -0.44 | -2.44 | -2.52 | -2.35 | -1.60 |
| MNQ | 15 | eod | event | against signal | 5487 | +0.588 | 0.076 | +8.27 | +6.27 | +0.70 | +11.71 | +5.28 |
| MNQ | 60 | h1 | event | with signal | 1298 | -0.002 | 0.039 | +0.55 | -1.45 | -2.27 | -0.66 | -1.20 |
| MNQ | 60 | h2 | event | against signal | 1298 | +0.035 | 0.039 | +1.54 | -0.46 | -2.33 | +1.37 | -1.18 |
| MNQ | 60 | h4 | event | against signal | 1298 | +0.052 | 0.039 | +0.80 | -1.20 | -0.83 | -1.55 | -2.66 |
| MNQ | 60 | h8 | event | with signal | 1298 | -0.039 | 0.039 | -2.30 | -4.30 | -3.18 | -5.39 | -1.84 |
| MNQ | 60 | h16 | event | with signal | 1298 | -0.107 | 0.039 | -7.03 | -9.03 | -4.01 | -13.94 | -6.54 |
| MNQ | 60 | eod | event | with signal | 1298 | -0.112 | 0.039 | -7.12 | -9.12 | -4.14 | -13.98 | -6.53 |
| MYM | 5 | h1 | event | with signal | 8129 | +0.023 | 0.169 | +0.29 | -1.71 | +nan | -1.71 | -1.62 |
| MYM | 5 | h2 | event | with signal | 8129 | +0.013 | 0.169 | +0.13 | -1.87 | +nan | -1.87 | -1.75 |
| MYM | 5 | h4 | event | with signal | 8129 | +0.026 | 0.169 | +0.15 | -1.85 | +nan | -1.85 | -1.67 |
| MYM | 5 | h8 | event | with signal | 8129 | +0.007 | 0.169 | -0.15 | -2.15 | +nan | -2.15 | -1.88 |
| MYM | 5 | h16 | event | with signal | 8129 | -0.037 | 0.169 | -0.57 | -2.57 | +nan | -2.57 | -2.08 |
| MYM | 5 | eod | event | against signal | 8129 | +0.410 | 0.169 | +5.05 | +3.05 | +nan | +3.05 | +0.62 |
| MYM | 15 | h1 | event | against signal | 2849 | +0.010 | 0.101 | -0.00 | -2.00 | +nan | -2.00 | -2.12 |
| MYM | 15 | h2 | event | with signal | 2849 | +0.006 | 0.101 | +0.31 | -1.69 | +nan | -1.69 | -1.51 |
| MYM | 15 | h4 | event | against signal | 2849 | +0.020 | 0.101 | -0.07 | -2.07 | +nan | -2.07 | -2.26 |
| MYM | 15 | h8 | event | with signal | 2849 | -0.021 | 0.101 | -0.21 | -2.21 | +nan | -2.21 | -1.82 |
| MYM | 15 | h16 | event | against signal | 2849 | +0.093 | 0.101 | +1.47 | -0.53 | +nan | -0.53 | -0.85 |
| MYM | 15 | eod | event | with signal | 2849 | -0.166 | 0.101 | -5.10 | -7.10 | +nan | -7.10 | -5.46 |
| MYM | 60 | h1 | event | with signal | 676 | +0.044 | 0.048 | +1.47 | -0.53 | +nan | -0.53 | -0.33 |
| MYM | 60 | h2 | event | with signal | 676 | +0.062 | 0.048 | +1.41 | -0.59 | +nan | -0.59 | -0.02 |
| MYM | 60 | h4 | event | with signal | 676 | -0.010 | 0.048 | -1.49 | -3.49 | +nan | -3.49 | -2.47 |
| MYM | 60 | h8 | event | with signal | 676 | +0.102 | 0.048 | +2.79 | +0.79 | +nan | +0.79 | +2.39 |
| MYM | 60 | h16 | event | with signal | 676 | +0.068 | 0.048 | +2.11 | +0.11 | +nan | +0.11 | +1.63 |
| MYM | 60 | eod | event | with signal | 676 | +0.062 | 0.048 | +2.95 | +0.95 | +nan | +0.95 | +2.84 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.100 | +0.145 | +0.203 | +0.247 | -0.639 | +0.000 | -0.012 | -0.014 | -0.022 | -0.023 | -0.043 |
| MES | 15 | +0.070 | +0.141 | +0.185 | +0.232 | -0.631 | +0.000 | -0.011 | -0.019 | -0.011 | +0.005 | -0.033 |
| MES | 60 | -0.118 | +0.024 | +0.149 | +0.205 | -0.626 | +0.000 | +0.006 | +0.001 | -0.056 | -0.071 | -0.128 |
| MNQ | 5 | +0.076 | +0.144 | +0.204 | +0.235 | -0.632 | +0.000 | -0.011 | -0.008 | -0.005 | +0.004 | +0.033 |
| MNQ | 15 | +0.027 | +0.104 | +0.179 | +0.230 | -0.639 | +0.000 | -0.006 | +0.002 | +0.021 | +0.016 | +0.005 |
| MNQ | 60 | +0.087 | +0.067 | +0.138 | +0.213 | -0.670 | +0.000 | +0.011 | -0.011 | +0.006 | +0.070 | -0.504 |
| MYM | 5 | +0.086 | +0.145 | +0.204 | +0.238 | -0.627 | +0.000 | +0.013 | +0.002 | +0.012 | -0.006 | -0.054 |
| MYM | 15 | +0.115 | +0.141 | +0.174 | +0.227 | -0.627 | +0.000 | -0.017 | -0.000 | -0.026 | -0.026 | -0.159 |
| MYM | 60 | -0.044 | +0.108 | +0.175 | +0.232 | -0.661 | +0.000 | +0.051 | +0.071 | -0.024 | +0.190 | -0.086 |

## Calibration

- MES 5-min: 1036271 bars, 12823 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 5151 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 1374 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 14960 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 5487 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 1298 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 8129 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 2849 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 676 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 47855 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
