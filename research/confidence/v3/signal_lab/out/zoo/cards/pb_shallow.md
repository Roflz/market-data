# Impact card: pb_shallow

pullback setups with depth < 38.2% [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.125 R20 over the next 16 bars (80 min), p=0.027; we would catch an effect of 0.056 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.37).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.27 at recent bar sizes, 90% range up to $2.37); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.111 R20 over the next 16 bars (4 h), p=0.82; we would catch an effect of 0.087 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.51).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.21 at recent bar sizes, 90% range up to $3.64); about 1.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.061 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.170 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.3).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.36 at recent bar sizes, 90% range up to $8.34); about 52.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.016 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.052 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.088).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.44 at recent bar sizes, 90% range up to $1.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.029 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.080 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.23).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.36 at recent bar sizes, 90% range up to $3.87); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.051 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.175 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.11).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.68 at recent bar sizes, 90% range up to $17.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.018 R20 over the next 1 bar (5 min), p=0.64; we would catch an effect of 0.072 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.12).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $1.24); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.083 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.111 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.84 at recent bar sizes, 90% range up to $4.20); about 219.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.060 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.253 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.57 at recent bar sizes, 90% range up to $14.37); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.023 .. +0.016 | -0.0003 | 0.73 / 0.73 / 0.74 | 0.748 |  |  | 9/16 | -0.014 | +0.007 |  | -0.3 / -0.3 |  |
| MES | 5 | h2 | +0.008 | -0.019 .. +0.036 | +0.0005 | 0.55 / 0.54 / 0.57 | 0.565 |  |  | 6/16 | -0.021 | +0.038 |  | +0.6 / +0.6 |  |
| MES | 5 | h4 | +0.031 | -0.009 .. +0.070 | +0.0013 | 0.13 / 0.12 / 0.16 | 0.156 |  |  | 9/16 | -0.000 | +0.061 |  | +1.6 / +1.5 | 0.056 |
| MES | 5 | h8 | +0.084 | +0.028 .. +0.140 | +0.0024 | 0.0031 / 0.0031 / 0.0066 | 0.00808 |  |  | 11/16 | +0.004 | +0.165 |  | +2.9 / +3.0 |  |
| MES | 5 | h16 * | +0.125 | +0.039 .. +0.212 | +0.0025 | 0.0045 / 0.0043 / 0.0077 | 0.0099 | 0.672 | 0.566 | 12/16 | -0.009 | +0.259 | False | +2.9 / +2.8 |  |
| MES | 5 | eod | +0.578 | +0.118 .. +1.039 | +0.0023 | 0.014 / 0.014 / 0.025 | 0.026 |  |  | 13/16 | +0.306 | +0.849 |  | +2.6 / +2.5 |  |
| MES | 15 | h1 | -0.006 | -0.033 .. +0.022 | -0.0005 | 0.67 / 0.68 / 0.7 | 0.685 |  |  | 10/16 | +0.017 | -0.029 |  | -0.4 / -0.4 |  |
| MES | 15 | h2 | +0.004 | -0.037 .. +0.044 | +0.0003 | 0.87 / 0.86 / 0.88 | 0.872 |  |  | 9/16 | +0.019 | -0.011 |  | +0.2 / +0.2 |  |
| MES | 15 | h4 | -0.015 | -0.079 .. +0.049 | -0.0006 | 0.66 / 0.65 / 0.67 | 0.652 |  |  | 8/16 | -0.022 | -0.007 |  | -0.5 / -0.4 | 0.087 |
| MES | 15 | h8 | +0.051 | -0.035 .. +0.137 | +0.0016 | 0.25 / 0.26 / 0.32 | 0.301 |  |  | 9/16 | +0.035 | +0.066 |  | +1.1 / +1.2 |  |
| MES | 15 | h16 * | +0.111 | -0.015 .. +0.236 | +0.0024 | 0.083 / 0.088 / 0.13 | 0.127 | 1 | 1 | 10/16 | +0.087 | +0.135 | False | +1.7 / +1.7 |  |
| MES | 15 | eod | +0.012 | -0.416 .. +0.440 | +0.0001 | 0.96 / 0.96 / 0.95 | 0.957 |  |  | 8/16 | +0.215 | -0.191 |  | +0.1 / +0.1 |  |
| MES | 60 | h1 | -0.001 | -0.057 .. +0.054 | -0.0002 | 0.96 / 0.96 / 0.96 | 0.96 |  |  | 10/16 | -0.012 | +0.009 |  | -0.1 / -0.1 |  |
| MES | 60 | h2 | -0.005 | -0.079 .. +0.070 | -0.0003 | 0.9 / 0.9 / 0.92 | 0.919 |  |  | 8/16 | -0.058 | +0.048 |  | -0.1 / -0.1 |  |
| MES | 60 | h4 | -0.000 | -0.126 .. +0.125 | +0.0002 | 1 / 1 / 1 | 0.998 |  |  | 6/16 | -0.025 | +0.024 |  | -0.0 / -0.0 | 0.170 |
| MES | 60 | h8 | +0.019 | -0.135 .. +0.174 | +0.0010 | 0.81 / 0.81 / 0.83 | 0.823 |  |  | 8/16 | -0.040 | +0.078 |  | +0.2 / +0.2 |  |
| MES | 60 | h16 * | +0.061 | -0.158 .. +0.279 | +0.0020 | 0.59 / 0.6 / 0.62 | 0.632 | 1 | 1 | 10/16 | -0.059 | +0.180 | False | +0.5 / +0.5 |  |
| MES | 60 | eod | +0.061 | -0.163 .. +0.286 | +0.0019 | 0.59 / 0.6 / 0.63 | 0.633 |  |  | 9/16 | -0.072 | +0.195 |  | +0.5 / +0.5 |  |
| MNQ | 5 | h1 | +0.006 | -0.012 .. +0.023 | +0.0005 | 0.52 / 0.51 / 0.59 | 0.539 |  |  | 11/16 | +0.007 | +0.005 |  | +0.7 / +0.6 |  |
| MNQ | 5 | h2 * | +0.016 | -0.010 .. +0.041 | +0.0008 | 0.23 / 0.21 / 0.37 | 0.263 | 1 | 1 | 11/16 | +0.001 | +0.030 | False | +1.2 / +1.2 |  |
| MNQ | 5 | h4 | -0.002 | -0.037 .. +0.033 | -0.0001 | 0.91 / 0.9 / 0.94 | 0.914 |  |  | 8/16 | -0.031 | +0.026 |  | -0.1 / -0.1 | 0.052 |
| MNQ | 5 | h8 | +0.018 | -0.032 .. +0.068 | +0.0004 | 0.49 / 0.5 / 0.63 | 0.565 |  |  | 8/16 | -0.031 | +0.066 |  | +0.7 / +0.7 |  |
| MNQ | 5 | h16 | +0.034 | -0.039 .. +0.107 | +0.0005 | 0.36 / 0.38 / 0.54 | 0.487 |  |  | 9/16 | -0.031 | +0.098 |  | +0.9 / +0.9 |  |
| MNQ | 5 | eod | +0.042 | -0.441 .. +0.525 | +0.0001 | 0.86 / 0.87 / 0.89 | 0.891 |  |  | 7/16 | +0.198 | -0.112 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h1 | +0.003 | -0.022 .. +0.028 | +0.0003 | 0.81 / 0.81 / 0.84 | 0.832 |  |  | 8/16 | +0.022 | -0.016 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h2 | +0.001 | -0.036 .. +0.037 | +0.0001 | 0.96 / 0.96 / 0.97 | 0.963 |  |  | 8/16 | +0.030 | -0.028 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h4 | -0.007 | -0.059 .. +0.045 | -0.0002 | 0.79 / 0.79 / 0.88 | 0.804 |  |  | 9/16 | +0.025 | -0.039 |  | -0.3 / -0.3 | 0.080 |
| MNQ | 15 | h8 | +0.017 | -0.059 .. +0.094 | +0.0004 | 0.66 / 0.67 / 0.79 | 0.723 |  |  | 7/16 | -0.012 | +0.047 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h16 * | +0.029 | -0.097 .. +0.156 | +0.0005 | 0.65 / 0.65 / 0.7 | 0.686 | 1 | 1 | 9/16 | +0.024 | +0.035 | False | +0.5 / +0.5 |  |
| MNQ | 15 | eod | -0.022 | -0.424 .. +0.381 | -0.0001 | 0.92 / 0.92 / 0.94 | 0.936 |  |  | 9/16 | +0.228 | -0.269 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h1 | -0.004 | -0.054 .. +0.046 | -0.0003 | 0.88 / 0.88 / 0.88 | 0.881 |  |  | 8/16 | -0.016 | +0.008 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h2 | +0.003 | -0.075 .. +0.082 | +0.0003 | 0.93 / 0.93 / 0.94 | 0.936 |  |  | 6/16 | +0.007 | -0.000 |  | +0.1 / +0.1 |  |
| MNQ | 60 | h4 | -0.015 | -0.130 .. +0.100 | -0.0007 | 0.8 / 0.8 / 0.82 | 0.811 |  |  | 10/16 | -0.038 | +0.008 |  | -0.3 / -0.3 | 0.175 |
| MNQ | 60 | h8 * | -0.051 | -0.219 .. +0.117 | -0.0019 | 0.55 / 0.55 / 0.57 | 0.572 | 1 | 1 | 10/16 | -0.059 | -0.043 | False | -0.6 / -0.6 |  |
| MNQ | 60 | h16 | -0.064 | -0.304 .. +0.175 | -0.0019 | 0.6 / 0.59 / 0.61 | 0.611 |  |  | 10/16 | -0.072 | -0.057 |  | -0.5 / -0.5 |  |
| MNQ | 60 | eod | -0.048 | -0.292 .. +0.196 | -0.0013 | 0.7 / 0.69 / 0.71 | 0.712 |  |  | 9/16 | -0.039 | -0.057 |  | -0.4 / -0.4 |  |
| MYM | 5 | h1 * | +0.018 | -0.003 .. +0.040 | +0.0015 | 0.088 / 0.098 / 0.18 | 0.151 | 1 | 1 | 6/8 | n/a | +0.018 | False | +1.6 / +1.7 |  |
| MYM | 5 | h2 | +0.007 | -0.025 .. +0.039 | +0.0004 | 0.66 / 0.66 / 0.77 | 0.695 |  |  | 5/8 | n/a | +0.007 |  | +0.4 / +0.4 |  |
| MYM | 5 | h4 | +0.005 | -0.038 .. +0.048 | +0.0002 | 0.82 / 0.83 / 0.88 | 0.821 |  |  | 5/8 | n/a | +0.005 |  | +0.2 / +0.2 | 0.072 |
| MYM | 5 | h8 | +0.037 | -0.026 .. +0.100 | +0.0008 | 0.25 / 0.28 / 0.54 | 0.397 |  |  | 6/8 | n/a | +0.037 |  | +1.1 / +1.2 |  |
| MYM | 5 | h16 | +0.039 | -0.070 .. +0.147 | +0.0007 | 0.48 / 0.49 / 0.6 | 0.544 |  |  | 6/8 | n/a | +0.039 |  | +0.7 / +0.7 |  |
| MYM | 5 | eod | -0.250 | -0.931 .. +0.431 | -0.0009 | 0.47 / 0.47 / 0.54 | 0.531 |  |  | 5/8 | n/a | -0.250 |  | -0.8 / -0.7 |  |
| MYM | 15 | h1 | -0.015 | -0.047 .. +0.018 | -0.0012 | 0.38 / 0.4 / 0.54 | 0.49 |  |  | 5/8 | n/a | -0.015 |  | -0.8 / -0.9 |  |
| MYM | 15 | h2 | +0.022 | -0.028 .. +0.071 | +0.0011 | 0.4 / 0.4 / 0.61 | 0.482 |  |  | 4/8 | n/a | +0.022 |  | +0.8 / +0.8 |  |
| MYM | 15 | h4 | +0.043 | -0.030 .. +0.117 | +0.0013 | 0.24 / 0.26 / 0.58 | 0.339 |  |  | 5/8 | n/a | +0.043 |  | +1.1 / +1.2 | 0.111 |
| MYM | 15 | h8 * | +0.083 | -0.044 .. +0.209 | +0.0019 | 0.2 / 0.19 / 0.34 | 0.226 | 1 | 1 | 4/8 | n/a | +0.083 | False | +1.4 / +1.3 |  |
| MYM | 15 | h16 | +0.069 | -0.111 .. +0.249 | +0.0011 | 0.45 / 0.43 / 0.6 | 0.506 |  |  | 3/8 | n/a | +0.069 |  | +0.8 / +0.8 |  |
| MYM | 15 | eod | +0.025 | -0.552 .. +0.601 | +0.0001 | 0.93 / 0.93 / 0.94 | 0.928 |  |  | 4/8 | n/a | +0.025 |  | +0.1 / +0.1 |  |
| MYM | 60 | h1 * | +0.060 | -0.010 .. +0.130 | +0.0066 | 0.094 / 0.089 / 0.15 | 0.153 | 1 | 1 | 4/8 | n/a | +0.060 | False | +1.8 / +1.7 |  |
| MYM | 60 | h2 | +0.067 | -0.046 .. +0.181 | +0.0054 | 0.24 / 0.24 / 0.3 | 0.296 |  |  | 5/8 | n/a | +0.067 |  | +1.2 / +1.2 |  |
| MYM | 60 | h4 | +0.064 | -0.108 .. +0.236 | +0.0037 | 0.47 / 0.46 / 0.47 | 0.474 |  |  | 4/8 | n/a | +0.064 |  | +0.8 / +0.7 | 0.253 |
| MYM | 60 | h8 | +0.128 | -0.120 .. +0.376 | +0.0053 | 0.31 / 0.31 / 0.32 | 0.313 |  |  | 4/8 | n/a | +0.128 |  | +1.0 / +1.0 |  |
| MYM | 60 | h16 | +0.132 | -0.215 .. +0.478 | +0.0042 | 0.46 / 0.45 / 0.46 | 0.456 |  |  | 3/8 | n/a | +0.132 |  | +0.8 / +0.7 |  |
| MYM | 60 | eod | +0.154 | -0.204 .. +0.512 | +0.0047 | 0.4 / 0.39 / 0.41 | 0.395 |  |  | 4/8 | n/a | +0.154 |  | +0.9 / +0.8 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | -0.010 .. +0.016 | +0.5% | -0.021 | 0.75 |  | 8/16 |
| MES | 5 | h2 | +0.001 | -0.020 .. +0.022 | +0.2% | -0.033 | 0.92 |  | 6/16 |
| MES | 5 | h4 | -0.017 | -0.043 .. +0.010 | -1.7% | -0.062 | 0.48 |  | 11/16 |
| MES | 5 | h8 | -0.033 | -0.073 .. +0.006 | -2.3% | -0.085 | 0.34 |  | 12/16 |
| MES | 5 | h16 | -0.059 | -0.114 .. -0.004 | -2.8% | -0.125 | 0.11 |  | 11/16 |
| MES | 5 | eod * | -0.330 | -0.638 .. -0.021 | -3.3% | -0.806 | 0.062 | 1 | 12/16 |
| MES | 15 | h1 | -0.014 | -0.032 .. +0.004 | -2.8% | -0.047 | 0.26 |  | 11/16 |
| MES | 15 | h2 | -0.022 | -0.049 .. +0.005 | -3.0% | -0.054 | 0.39 |  | 10/16 |
| MES | 15 | h4 | -0.009 | -0.051 .. +0.034 | -0.8% | -0.065 | 0.82 |  | 7/16 |
| MES | 15 | h8 | -0.019 | -0.077 .. +0.039 | -1.2% | -0.094 | 0.76 |  | 10/16 |
| MES | 15 | h16 * | -0.097 | -0.181 .. -0.013 | -4.2% | -0.191 | 0.085 | 1 | 11/16 |
| MES | 15 | eod | +0.120 | -0.119 .. +0.359 | +2.2% | -0.037 | 0.34 |  | 11/16 |
| MES | 60 | h1 | -0.006 | -0.041 .. +0.028 | -1.2% | -0.009 | 0.99 |  | 10/16 |
| MES | 60 | h2 * | -0.053 | -0.104 .. -0.002 | -7.2% | -0.017 | 0.051 | 1 | 11/16 |
| MES | 60 | h4 | -0.054 | -0.132 .. +0.024 | -5.1% | -0.009 | 0.28 |  | 12/16 |
| MES | 60 | h8 | -0.058 | -0.161 .. +0.045 | -3.9% | -0.018 | 0.32 |  | 12/16 |
| MES | 60 | h16 | -0.089 | -0.232 .. +0.054 | -4.3% | -0.025 | 0.23 |  | 10/16 |
| MES | 60 | eod | -0.065 | -0.206 .. +0.075 | -3.0% | -0.022 | 0.38 |  | 9/16 |
| MNQ | 5 | h1 | -0.007 | -0.018 .. +0.005 | -1.3% | -0.035 | 0.33 |  | 11/16 |
| MNQ | 5 | h2 | -0.007 | -0.026 .. +0.011 | -1.0% | -0.041 | 0.59 |  | 7/16 |
| MNQ | 5 | h4 | -0.029 | -0.054 .. -0.005 | -2.7% | -0.072 | 0.37 |  | 11/16 |
| MNQ | 5 | h8 | -0.066 | -0.106 .. -0.026 | -4.1% | -0.115 | 0.088 |  | 11/16 |
| MNQ | 5 | h16 | -0.113 | -0.178 .. -0.047 | -4.7% | -0.205 | 0.026 |  | 12/16 |
| MNQ | 5 | eod * | -0.533 | -0.903 .. -0.164 | -4.2% | -1.283 | 0.015 | 1 | 12/16 |
| MNQ | 15 | h1 | -0.021 | -0.041 .. -0.001 | -3.9% | -0.044 | 0.038 |  | 11/16 |
| MNQ | 15 | h2 * | -0.034 | -0.060 .. -0.008 | -4.3% | -0.069 | 0.038 | 1 | 13/16 |
| MNQ | 15 | h4 | -0.064 | -0.103 .. -0.024 | -5.6% | -0.113 | 0.063 |  | 14/16 |
| MNQ | 15 | h8 | -0.077 | -0.136 .. -0.017 | -4.6% | -0.163 | 0.28 |  | 11/16 |
| MNQ | 15 | h16 | -0.059 | -0.148 .. +0.029 | -2.4% | -0.181 | 0.33 |  | 10/16 |
| MNQ | 15 | eod | +0.018 | -0.262 .. +0.297 | +0.3% | -0.279 | 0.95 |  | 8/16 |
| MNQ | 60 | h1 | -0.007 | -0.044 .. +0.029 | -1.4% | -0.018 | 0.71 |  | 9/16 |
| MNQ | 60 | h2 | -0.044 | -0.093 .. +0.006 | -5.7% | -0.059 | 0.097 |  | 12/16 |
| MNQ | 60 | h4 * | -0.099 | -0.182 .. -0.017 | -9.0% | -0.103 | 0.019 | 1 | 11/16 |
| MNQ | 60 | h8 | -0.100 | -0.208 .. +0.008 | -6.3% | -0.121 | 0.074 |  | 11/16 |
| MNQ | 60 | h16 | -0.055 | -0.199 .. +0.088 | -2.5% | -0.034 | 0.47 |  | 9/16 |
| MNQ | 60 | eod | -0.068 | -0.213 .. +0.077 | -3.0% | -0.058 | 0.37 |  | 10/16 |
| MYM | 5 | h1 | -0.016 | -0.031 .. -0.001 | -3.0% | -0.038 | 0.13 |  | 5/8 |
| MYM | 5 | h2 | -0.027 | -0.050 .. -0.003 | -3.5% | -0.063 | 0.089 |  | 7/8 |
| MYM | 5 | h4 | -0.044 | -0.077 .. -0.011 | -4.0% | -0.108 | 0.087 |  | 7/8 |
| MYM | 5 | h8 | -0.070 | -0.121 .. -0.019 | -4.4% | -0.166 | 0.23 |  | 7/8 |
| MYM | 5 | h16 | -0.099 | -0.177 .. -0.021 | -4.2% | -0.215 | 0.14 |  | 7/8 |
| MYM | 5 | eod * | -0.807 | -1.238 .. -0.376 | -6.9% | -1.506 | 0.02 | 1 | 8/8 |
| MYM | 15 | h1 * | -0.022 | -0.047 .. +0.003 | -4.2% | -0.058 | 0.29 | 1 | 6/8 |
| MYM | 15 | h2 | -0.033 | -0.072 .. +0.007 | -4.3% | -0.073 | 0.6 |  | 5/8 |
| MYM | 15 | h4 | -0.048 | -0.112 .. +0.017 | -4.3% | -0.103 | 0.76 |  | 6/8 |
| MYM | 15 | h8 | -0.032 | -0.126 .. +0.061 | -2.0% | -0.141 | 0.93 |  | 3/8 |
| MYM | 15 | h16 | -0.140 | -0.276 .. -0.003 | -5.7% | -0.246 | 0.36 |  | 6/8 |
| MYM | 15 | eod | +0.005 | -0.358 .. +0.368 | +0.1% | -0.370 | 0.98 |  | 5/8 |
| MYM | 60 | h1 * | -0.034 | -0.076 .. +0.009 | -6.4% | -0.056 | 0.21 | 1 | 6/8 |
| MYM | 60 | h2 | -0.013 | -0.087 .. +0.062 | -1.7% | -0.042 | 0.95 |  | 4/8 |
| MYM | 60 | h4 | -0.033 | -0.139 .. +0.073 | -3.1% | -0.013 | 0.92 |  | 4/8 |
| MYM | 60 | h8 | -0.043 | -0.211 .. +0.124 | -2.8% | -0.040 | 0.61 |  | 5/8 |
| MYM | 60 | h16 | -0.078 | -0.275 .. +0.120 | -3.7% | -0.116 | 0.56 |  | 5/8 |
| MYM | 60 | eod | -0.076 | -0.274 .. +0.122 | -3.4% | -0.154 | 0.55 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +1.42 pts | -0.02 .. +2.85 | 0.063 |
| MES | 15 | -1.11 pts | -3.30 .. +1.08 | 0.37 |
| MES | 60 | +1.07 pts | -2.74 .. +4.88 | 0.68 |
| MNQ | 5 | -0.10 pts | -1.36 .. +1.15 | 0.98 |
| MNQ | 15 | -0.14 pts | -2.12 .. +1.83 | 0.89 |
| MNQ | 60 | -0.76 pts | -4.14 .. +2.62 | 0.66 |
| MYM | 5 | +0.52 pts | -1.02 .. +2.05 | 0.61 |
| MYM | 15 | +0.51 pts | -1.99 .. +3.02 | 0.7 |
| MYM | 60 | +3.19 pts | -2.27 .. +8.65 | 0.25 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 4101 | +0.004 | 0.256 | -0.08 | -3.58 | -3.47 | -3.65 | -3.58 |
| MES | 5 | h2 | event | with signal | 4101 | +0.009 | 0.256 | +0.27 | -3.23 | -3.55 | -3.01 | -3.24 |
| MES | 5 | h4 | event | with signal | 4101 | +0.034 | 0.256 | +0.47 | -3.03 | -3.43 | -2.75 | -3.08 |
| MES | 5 | h8 | event | with signal | 4101 | +0.091 | 0.256 | +1.19 | -2.31 | -3.38 | -1.59 | -2.40 |
| MES | 5 | h16 | event | with signal | 4101 | +0.137 | 0.256 | +1.64 | -1.86 | -3.64 | -0.65 | -1.98 |
| MES | 5 | eod | event | with signal | 4101 | +0.853 | 0.256 | +6.44 | +2.94 | -1.87 | +6.19 | -0.04 |
| MES | 15 | h1 | event | against signal | 1897 | +0.005 | 0.167 | +0.13 | -3.37 | -3.84 | -3.00 | -3.37 |
| MES | 15 | h2 | event | with signal | 1897 | +0.006 | 0.167 | +0.08 | -3.42 | -3.07 | -3.69 | -3.45 |
| MES | 15 | h4 | event | against signal | 1897 | +0.007 | 0.167 | +0.12 | -3.38 | -3.38 | -3.38 | -3.26 |
| MES | 15 | h8 | event | with signal | 1897 | +0.066 | 0.167 | +1.63 | -1.87 | -2.70 | -1.22 | -2.13 |
| MES | 15 | h16 | event | with signal | 1897 | +0.155 | 0.167 | +3.05 | -0.45 | -1.75 | +0.56 | -1.21 |
| MES | 15 | eod | event | with signal | 1897 | +0.162 | 0.167 | +0.41 | -3.09 | -1.20 | -4.55 | -5.45 |
| MES | 60 | h1 | event | against signal | 649 | -0.002 | 0.089 | +0.62 | -2.88 | -3.60 | -2.31 | -2.82 |
| MES | 60 | h2 | event | against signal | 649 | -0.002 | 0.089 | -0.45 | -3.95 | -2.74 | -4.92 | -3.82 |
| MES | 60 | h4 | event | against signal | 649 | -0.013 | 0.089 | +2.55 | -0.95 | -4.15 | +1.61 | -0.75 |
| MES | 60 | h8 | event | with signal | 649 | +0.049 | 0.089 | -0.13 | -3.63 | -4.12 | -3.24 | -4.20 |
| MES | 60 | h16 | event | with signal | 649 | +0.116 | 0.089 | +4.06 | +0.56 | -4.25 | +4.42 | -0.56 |
| MES | 60 | eod | event | with signal | 649 | +0.118 | 0.089 | +3.96 | +0.46 | -4.97 | +4.82 | -0.60 |
| MNQ | 5 | h1 | event | with signal | 5963 | +0.008 | 0.108 | -0.00 | -2.00 | -1.93 | -2.06 | -2.03 |
| MNQ | 5 | h2 | event | with signal | 5963 | +0.020 | 0.108 | +0.35 | -1.65 | -1.87 | -1.49 | -1.73 |
| MNQ | 5 | h4 | event | against signal | 5963 | -0.008 | 0.108 | -0.34 | -2.34 | -2.13 | -2.49 | -2.18 |
| MNQ | 5 | h8 | event | with signal | 5963 | +0.035 | 0.108 | +0.72 | -1.28 | -1.86 | -0.85 | -1.53 |
| MNQ | 5 | h16 | event | with signal | 5963 | +0.066 | 0.108 | +0.98 | -1.02 | -1.95 | -0.33 | -1.43 |
| MNQ | 5 | eod | event | with signal | 5963 | +0.498 | 0.108 | +3.90 | +1.90 | -0.94 | +4.02 | -4.56 |
| MNQ | 15 | h1 | event | with signal | 2411 | +0.005 | 0.067 | -0.32 | -2.32 | -1.75 | -2.79 | -2.33 |
| MNQ | 15 | h2 | event | with signal | 2411 | +0.004 | 0.067 | -0.59 | -2.59 | -1.58 | -3.40 | -2.57 |
| MNQ | 15 | h4 | event | against signal | 2411 | +0.002 | 0.067 | +1.10 | -0.90 | -2.32 | +0.26 | -0.89 |
| MNQ | 15 | h8 | event | with signal | 2411 | +0.038 | 0.067 | +1.41 | -0.59 | -1.78 | +0.39 | -0.87 |
| MNQ | 15 | h16 | event | with signal | 2411 | +0.083 | 0.067 | +3.93 | +1.93 | -1.19 | +4.47 | +1.03 |
| MNQ | 15 | eod | event | against signal | 2411 | -0.186 | 0.067 | +3.43 | +1.43 | -2.13 | +4.34 | +4.63 |
| MNQ | 60 | h1 | event | against signal | 759 | -0.006 | 0.034 | -0.25 | -2.25 | -1.99 | -2.47 | -1.87 |
| MNQ | 60 | h2 | event | with signal | 759 | +0.021 | 0.034 | -0.83 | -2.83 | -1.73 | -3.72 | -3.52 |
| MNQ | 60 | h4 | event | against signal | 759 | -0.017 | 0.034 | +2.45 | +0.45 | -2.74 | +3.08 | +1.65 |
| MNQ | 60 | h8 | event | against signal | 759 | -0.005 | 0.034 | +4.37 | +2.37 | -2.04 | +6.00 | +4.28 |
| MNQ | 60 | h16 | event | against signal | 759 | -0.029 | 0.034 | +4.87 | +2.87 | -3.01 | +7.73 | +5.75 |
| MNQ | 60 | eod | event | against signal | 759 | -0.056 | 0.034 | +3.17 | +1.17 | -3.96 | +5.40 | +4.35 |
| MYM | 5 | h1 | event | with signal | 3019 | +0.019 | 0.151 | +0.08 | -1.92 | +nan | -1.92 | -1.93 |
| MYM | 5 | h2 | event | with signal | 3019 | +0.011 | 0.151 | +0.03 | -1.97 | +nan | -1.97 | -2.03 |
| MYM | 5 | h4 | event | with signal | 3019 | +0.016 | 0.151 | -0.24 | -2.24 | +nan | -2.24 | -2.44 |
| MYM | 5 | h8 | event | with signal | 3019 | +0.056 | 0.151 | -0.04 | -2.04 | +nan | -2.04 | -2.41 |
| MYM | 5 | h16 | event | with signal | 3019 | +0.070 | 0.151 | -0.20 | -2.20 | +nan | -2.20 | -2.77 |
| MYM | 5 | eod | event | against signal | 3019 | +0.070 | 0.151 | +2.43 | +0.43 | +nan | +0.43 | +2.59 |
| MYM | 15 | h1 | event | against signal | 1189 | +0.011 | 0.090 | +0.02 | -1.98 | +nan | -1.98 | -1.91 |
| MYM | 15 | h2 | event | with signal | 1189 | +0.027 | 0.090 | +0.75 | -1.25 | +nan | -1.25 | -1.39 |
| MYM | 15 | h4 | event | with signal | 1189 | +0.050 | 0.090 | +0.63 | -1.37 | +nan | -1.37 | -1.57 |
| MYM | 15 | h8 | event | with signal | 1189 | +0.100 | 0.090 | +2.32 | +0.32 | +nan | +0.32 | -0.23 |
| MYM | 15 | h16 | event | with signal | 1189 | +0.093 | 0.090 | +2.37 | +0.37 | +nan | +0.37 | -0.50 |
| MYM | 15 | eod | event | with signal | 1189 | +0.091 | 0.090 | +0.46 | -1.54 | +nan | -1.54 | -3.11 |
| MYM | 60 | h1 | event | with signal | 337 | +0.064 | 0.047 | +1.82 | -0.18 | +nan | -0.18 | -0.26 |
| MYM | 60 | h2 | event | with signal | 337 | +0.074 | 0.047 | +2.66 | +0.66 | +nan | +0.66 | +0.54 |
| MYM | 60 | h4 | event | with signal | 337 | +0.079 | 0.047 | -0.31 | -2.31 | +nan | -2.31 | -2.68 |
| MYM | 60 | h8 | event | with signal | 337 | +0.154 | 0.047 | +2.14 | +0.14 | +nan | +0.14 | -0.47 |
| MYM | 60 | h16 | event | with signal | 337 | +0.174 | 0.047 | +4.50 | +2.50 | +nan | +2.50 | +1.79 |
| MYM | 60 | eod | event | with signal | 337 | +0.197 | 0.047 | +5.56 | +3.56 | +nan | +3.56 | +3.01 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.160 | +0.765 | -0.141 | -0.077 | -0.008 | +0.000 | -0.004 | +0.007 | +0.030 | +0.088 | +0.139 |
| MES | 15 | -0.289 | +0.727 | -0.121 | -0.066 | -0.004 | +0.000 | +0.003 | +0.011 | -0.006 | +0.064 | +0.123 |
| MES | 60 | +1.348 | +0.889 | -0.026 | -0.041 | +0.017 | +0.000 | -0.000 | -0.006 | -0.002 | -0.001 | +0.151 |
| MNQ | 5 | -0.356 | +0.836 | -0.089 | -0.061 | -0.007 | +0.000 | +0.006 | +0.017 | +0.001 | +0.020 | +0.033 |
| MNQ | 15 | -0.438 | +0.756 | -0.101 | -0.078 | -0.016 | +0.000 | +0.004 | -0.001 | -0.012 | -0.003 | +0.015 |
| MNQ | 60 | +1.377 | +0.801 | -0.038 | -0.041 | -0.019 | +0.000 | +0.004 | +0.011 | +0.014 | -0.019 | +0.104 |
| MYM | 5 | -0.401 | +0.823 | -0.103 | -0.067 | -0.010 | +0.000 | +0.017 | +0.006 | +0.006 | +0.036 | +0.049 |
| MYM | 15 | -0.553 | +0.736 | -0.084 | -0.051 | -0.011 | +0.000 | -0.013 | +0.020 | +0.039 | +0.097 | +0.053 |
| MYM | 60 | +1.171 | +0.752 | -0.059 | -0.035 | -0.020 | +0.000 | +0.056 | +0.058 | +0.049 | +0.078 | +0.068 |

## Calibration

- MES 5-min: 1036271 bars, 4101 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1897 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 649 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 5963 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 2411 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 759 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 3019 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 1189 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 337 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
