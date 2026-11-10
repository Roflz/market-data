# Impact card: cpi_day

CPI release session (data/cpi_dates.csv) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +1.219 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.027).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $19.20 at recent bar sizes, 90% range up to $0.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.660 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.072 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.054).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $18.14 at recent bar sizes, 90% range up to $3.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.096 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.146 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.15).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $5.15 at recent bar sizes, 90% range up to $15.11); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +1.990 R20 over the rest of the session (to 16:45), p=0.9; we would catch an effect of 0.044 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.34).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $51.86 at recent bar sizes, 90% range up to $2.04); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.210 R20 over the next 16 bars (4 h), p=0.69; we would catch an effect of 0.082 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $9.57 at recent bar sizes, 90% range up to $8.34); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.167 R20 over the next 8 bars (8 h), p=0.92; we would catch an effect of 0.155 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.38).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $14.98 at recent bar sizes, 90% range up to $32.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.016 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.064 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.17).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.18 at recent bar sizes, 90% range up to $1.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.191 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.112 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.086).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.98 at recent bar sizes, 90% range up to $4.54); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.094 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.216 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.15).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.87 at recent bar sizes, 90% range up to $15.57); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.006 .. +0.009 | +0.0004 | 0.71 / 0.7 / 0.69 | 0.683 |  |  | 9/16 | -0.003 | +0.005 |  | +0.4 / +0.4 |  |
| MES | 5 | h2 | +0.002 | -0.013 .. +0.016 | +0.0004 | 0.81 / 0.81 / 0.8 | 0.797 |  |  | 9/16 | -0.007 | +0.010 |  | +0.3 / +0.2 |  |
| MES | 5 | h4 | +0.003 | -0.027 .. +0.033 | +0.0004 | 0.84 / 0.84 / 0.83 | 0.83 |  |  | 9/16 | -0.014 | +0.020 |  | +0.4 / +0.2 | 0.039 |
| MES | 5 | h8 | +0.006 | -0.055 .. +0.068 | +0.0006 | 0.84 / 0.84 / 0.82 | 0.819 |  |  | 9/16 | -0.030 | +0.043 |  | +0.5 / +0.2 |  |
| MES | 5 | h16 | +0.019 | -0.109 .. +0.147 | +0.0013 | 0.77 / 0.76 / 0.74 | 0.748 |  |  | 10/16 | -0.055 | +0.093 |  | +1.1 / +0.3 |  |
| MES | 5 | eod * | +1.219 | -1.026 .. +3.463 | +0.0163 | 0.29 / 0.29 / 0.22 | 0.211 | 1 | 1 | 9/16 | +0.189 | +2.242 | False | +13.7 / +1.1 |  |
| MES | 15 | h1 | +0.003 | -0.011 .. +0.017 | +0.0009 | 0.65 / 0.65 / 0.63 | 0.629 |  |  | 10/16 | -0.004 | +0.010 |  | +0.4 / +0.4 |  |
| MES | 15 | h2 | +0.007 | -0.020 .. +0.035 | +0.0013 | 0.6 / 0.59 / 0.57 | 0.568 |  |  | 10/16 | -0.007 | +0.022 |  | +0.7 / +0.5 |  |
| MES | 15 | h4 | +0.017 | -0.039 .. +0.072 | +0.0021 | 0.55 / 0.55 / 0.53 | 0.513 |  |  | 10/16 | -0.014 | +0.048 |  | +1.1 / +0.6 | 0.072 |
| MES | 15 | h8 | +0.045 | -0.068 .. +0.159 | +0.0039 | 0.44 / 0.43 / 0.4 | 0.392 |  |  | 10/16 | -0.023 | +0.113 |  | +2.1 / +0.8 |  |
| MES | 15 | h16 | +0.127 | -0.114 .. +0.368 | +0.0077 | 0.3 / 0.3 / 0.26 | 0.256 |  |  | 9/16 | -0.024 | +0.277 |  | +4.1 / +1.0 |  |
| MES | 15 | eod * | +0.660 | -0.540 .. +1.861 | +0.0154 | 0.28 / 0.28 / 0.24 | 0.231 | 1 | 1 | 9/16 | +0.089 | +1.229 | False | +8.1 / +1.1 |  |
| MES | 60 | h1 | +0.009 | -0.019 .. +0.037 | +0.0025 | 0.54 / 0.53 / 0.5 | 0.483 |  |  | 10/16 | -0.006 | +0.024 |  | +0.6 / +0.6 |  |
| MES | 60 | h2 | +0.020 | -0.036 .. +0.076 | +0.0038 | 0.49 / 0.49 / 0.46 | 0.45 |  |  | 11/16 | -0.009 | +0.048 |  | +0.9 / +0.7 |  |
| MES | 60 | h4 | +0.045 | -0.064 .. +0.155 | +0.0062 | 0.42 / 0.42 / 0.39 | 0.372 |  |  | 10/16 | -0.010 | +0.100 |  | +1.6 / +0.8 | 0.146 |
| MES | 60 | h8 * | +0.096 | -0.118 .. +0.310 | +0.0095 | 0.38 / 0.38 / 0.34 | 0.332 | 1 | 1 | 11/16 | -0.019 | +0.211 | False | +2.5 / +0.9 |  |
| MES | 60 | h16 | +0.166 | -0.220 .. +0.552 | +0.0126 | 0.4 / 0.4 / 0.36 | 0.349 |  |  | 9/16 | -0.010 | +0.343 |  | +3.2 / +0.8 |  |
| MES | 60 | eod | +0.185 | -0.235 .. +0.605 | +0.0134 | 0.39 / 0.39 / 0.36 | 0.356 |  |  | 10/16 | +0.017 | +0.353 |  | +3.5 / +0.9 |  |
| MNQ | 5 | h1 | +0.003 | -0.005 .. +0.011 | +0.0007 | 0.44 / 0.44 / 0.47 | 0.452 |  |  | 10/16 | -0.001 | +0.008 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h2 | +0.005 | -0.011 .. +0.021 | +0.0007 | 0.54 / 0.54 / 0.58 | 0.563 |  |  | 10/16 | -0.006 | +0.016 |  | +0.8 / +0.6 |  |
| MNQ | 5 | h4 | +0.009 | -0.023 .. +0.041 | +0.0009 | 0.58 / 0.58 / 0.63 | 0.606 |  |  | 10/16 | -0.016 | +0.034 |  | +1.1 / +0.6 | 0.044 |
| MNQ | 5 | h8 | +0.021 | -0.046 .. +0.088 | +0.0014 | 0.54 / 0.54 / 0.6 | 0.566 |  |  | 10/16 | -0.031 | +0.072 |  | +1.6 / +0.6 |  |
| MNQ | 5 | h16 | +0.051 | -0.088 .. +0.191 | +0.0024 | 0.47 / 0.47 / 0.52 | 0.499 |  |  | 10/16 | -0.055 | +0.157 |  | +2.7 / +0.7 |  |
| MNQ | 5 | eod * | +1.990 | -0.718 .. +4.697 | +0.0193 | 0.15 / 0.15 / 0.11 | 0.11 | 1 | 1 | 10/16 | +0.744 | +3.225 | False | +18.4 / +1.4 |  |
| MNQ | 15 | h1 | +0.007 | -0.007 .. +0.022 | +0.0015 | 0.32 / 0.31 / 0.39 | 0.324 |  |  | 10/16 | +0.001 | +0.013 |  | +1.0 / +1.0 |  |
| MNQ | 15 | h2 | +0.016 | -0.013 .. +0.044 | +0.0020 | 0.29 / 0.28 / 0.4 | 0.331 |  |  | 10/16 | +0.000 | +0.031 |  | +1.4 / +1.1 |  |
| MNQ | 15 | h4 | +0.033 | -0.025 .. +0.091 | +0.0025 | 0.27 / 0.27 / 0.41 | 0.328 |  |  | 10/16 | +0.000 | +0.066 |  | +2.0 / +1.1 | 0.082 |
| MNQ | 15 | h8 | +0.078 | -0.043 .. +0.200 | +0.0045 | 0.2 / 0.2 / 0.28 | 0.245 |  |  | 10/16 | +0.011 | +0.145 |  | +3.4 / +1.3 |  |
| MNQ | 15 | h16 * | +0.210 | -0.051 .. +0.470 | +0.0098 | 0.11 / 0.12 / 0.12 | 0.117 | 1 | 1 | 10/16 | +0.060 | +0.359 | False | +6.1 / +1.6 |  |
| MNQ | 15 | eod | +1.011 | -0.357 .. +2.379 | +0.0164 | 0.15 / 0.15 / 0.15 | 0.135 |  |  | 10/16 | +0.281 | +1.737 |  | +10.8 / +1.4 |  |
| MNQ | 60 | h1 | +0.020 | -0.010 .. +0.050 | +0.0051 | 0.2 / 0.2 / 0.16 | 0.16 |  |  | 11/16 | +0.003 | +0.037 |  | +1.3 / +1.3 |  |
| MNQ | 60 | h2 | +0.040 | -0.020 .. +0.101 | +0.0073 | 0.19 / 0.19 / 0.15 | 0.155 |  |  | 11/16 | +0.007 | +0.074 |  | +1.8 / +1.3 |  |
| MNQ | 60 | h4 | +0.084 | -0.034 .. +0.202 | +0.0107 | 0.16 / 0.16 / 0.13 | 0.132 |  |  | 11/16 | +0.019 | +0.149 |  | +2.8 / +1.4 | 0.155 |
| MNQ | 60 | h8 * | +0.167 | -0.063 .. +0.397 | +0.0155 | 0.15 / 0.15 / 0.12 | 0.118 | 1 | 1 | 11/16 | +0.036 | +0.299 | False | +4.0 / +1.4 |  |
| MNQ | 60 | h16 | +0.299 | -0.116 .. +0.713 | +0.0212 | 0.16 / 0.16 / 0.12 | 0.126 |  |  | 10/16 | +0.086 | +0.512 |  | +5.5 / +1.4 |  |
| MNQ | 60 | eod | +0.309 | -0.143 .. +0.761 | +0.0210 | 0.18 / 0.18 / 0.15 | 0.155 |  |  | 10/16 | +0.085 | +0.533 |  | +5.4 / +1.3 |  |
| MYM | 5 | h1 | +0.003 | -0.008 .. +0.014 | +0.0006 | 0.61 / 0.6 / 0.64 | 0.638 |  |  | 4/8 | n/a | +0.003 |  | +0.5 / +0.5 |  |
| MYM | 5 | h2 | +0.007 | -0.016 .. +0.029 | +0.0009 | 0.55 / 0.55 / 0.6 | 0.606 |  |  | 4/8 | n/a | +0.007 |  | +0.8 / +0.6 |  |
| MYM | 5 | h4 * | +0.016 | -0.032 .. +0.063 | +0.0013 | 0.52 / 0.52 / 0.59 | 0.578 | 1 | 1 | 4/8 | n/a | +0.016 | False | +1.2 / +0.6 | 0.064 |
| MYM | 5 | h8 | +0.030 | -0.070 .. +0.129 | +0.0018 | 0.56 / 0.56 / 0.6 | 0.584 |  |  | 4/8 | n/a | +0.030 |  | +1.5 / +0.6 |  |
| MYM | 5 | h16 | +0.049 | -0.157 .. +0.254 | +0.0023 | 0.64 / 0.65 / 0.65 | 0.644 |  |  | 4/8 | n/a | +0.049 |  | +1.7 / +0.5 |  |
| MYM | 5 | eod | +0.931 | -2.926 .. +4.788 | +0.0096 | 0.64 / 0.65 / 0.59 | 0.577 |  |  | 4/8 | n/a | +0.931 |  | +5.6 / +0.5 |  |
| MYM | 15 | h1 | +0.004 | -0.016 .. +0.024 | +0.0008 | 0.71 / 0.72 / 0.73 | 0.71 |  |  | 4/8 | n/a | +0.004 |  | +0.3 / +0.4 |  |
| MYM | 15 | h2 | +0.012 | -0.029 .. +0.053 | +0.0015 | 0.57 / 0.58 / 0.64 | 0.592 |  |  | 4/8 | n/a | +0.012 |  | +0.7 / +0.6 |  |
| MYM | 15 | h4 | +0.027 | -0.057 .. +0.112 | +0.0021 | 0.52 / 0.53 / 0.61 | 0.557 |  |  | 4/8 | n/a | +0.027 |  | +1.1 / +0.6 | 0.112 |
| MYM | 15 | h8 | +0.062 | -0.111 .. +0.236 | +0.0036 | 0.48 / 0.5 / 0.53 | 0.482 |  |  | 4/8 | n/a | +0.062 |  | +1.8 / +0.7 |  |
| MYM | 15 | h16 * | +0.191 | -0.180 .. +0.561 | +0.0078 | 0.31 / 0.33 / 0.37 | 0.335 | 1 | 1 | 5/8 | n/a | +0.191 | False | +3.6 / +1.0 |  |
| MYM | 15 | eod | +0.480 | -1.430 .. +2.390 | +0.0081 | 0.62 / 0.63 / 0.6 | 0.59 |  |  | 4/8 | n/a | +0.480 |  | +3.4 / +0.5 |  |
| MYM | 60 | h1 | +0.009 | -0.032 .. +0.051 | +0.0024 | 0.66 / 0.67 / 0.66 | 0.657 |  |  | 4/8 | n/a | +0.009 |  | +0.4 / +0.4 |  |
| MYM | 60 | h2 | +0.015 | -0.066 .. +0.097 | +0.0028 | 0.71 / 0.72 / 0.71 | 0.714 |  |  | 4/8 | n/a | +0.015 |  | +0.5 / +0.4 |  |
| MYM | 60 | h4 | +0.038 | -0.123 .. +0.198 | +0.0050 | 0.65 / 0.65 / 0.65 | 0.641 |  |  | 4/8 | n/a | +0.038 |  | +0.9 / +0.5 | 0.216 |
| MYM | 60 | h8 * | +0.094 | -0.225 .. +0.412 | +0.0090 | 0.56 / 0.57 / 0.55 | 0.55 | 1 | 1 | 4/8 | n/a | +0.094 | False | +1.5 / +0.6 |  |
| MYM | 60 | h16 | +0.128 | -0.453 .. +0.709 | +0.0093 | 0.67 / 0.67 / 0.64 | 0.629 |  |  | 4/8 | n/a | +0.128 |  | +1.6 / +0.4 |  |
| MYM | 60 | eod | +0.138 | -0.497 .. +0.772 | +0.0096 | 0.67 / 0.67 / 0.66 | 0.659 |  |  | 5/8 | n/a | +0.138 |  | +1.7 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | -0.002 .. +0.008 | +0.6% | +0.007 | 0.21 |  | 10/16 |
| MES | 5 | h2 | +0.012 | +0.002 .. +0.021 | +1.7% | +0.017 | 0.021 |  | 10/16 |
| MES | 5 | h4 * | +0.028 | +0.009 .. +0.047 | +2.8% | +0.040 | 0.0045 | 0.672 | 10/16 |
| MES | 5 | h8 | +0.057 | +0.017 .. +0.096 | +3.9% | +0.086 | 0.0057 |  | 9/16 |
| MES | 5 | h16 | +0.089 | +0.007 .. +0.170 | +4.2% | +0.166 | 0.033 |  | 8/16 |
| MES | 5 | eod | +1.231 | -0.264 .. +2.725 | +12.3% | +2.542 | 0.11 |  | 8/16 |
| MES | 15 | h1 * | +0.012 | +0.003 .. +0.021 | +2.4% | +0.013 | 0.009 | 1 | 10/16 |
| MES | 15 | h2 | +0.022 | +0.004 .. +0.039 | +3.0% | +0.029 | 0.018 |  | 9/16 |
| MES | 15 | h4 | +0.037 | +0.001 .. +0.073 | +3.5% | +0.058 | 0.043 |  | 7/16 |
| MES | 15 | h8 | +0.051 | -0.020 .. +0.121 | +3.3% | +0.105 | 0.16 |  | 7/16 |
| MES | 15 | h16 | +0.053 | -0.092 .. +0.199 | +2.3% | +0.233 | 0.47 |  | 7/16 |
| MES | 15 | eod | +0.599 | -0.189 .. +1.387 | +10.9% | +1.221 | 0.14 |  | 8/16 |
| MES | 60 | h1 * | +0.023 | +0.003 .. +0.043 | +4.5% | +0.042 | 0.025 | 1 | 8/16 |
| MES | 60 | h2 | +0.026 | -0.011 .. +0.062 | +3.5% | +0.065 | 0.17 |  | 6/16 |
| MES | 60 | h4 | +0.016 | -0.050 .. +0.081 | +1.5% | +0.107 | 0.64 |  | 6/16 |
| MES | 60 | h8 | +0.039 | -0.087 .. +0.166 | +2.6% | +0.200 | 0.54 |  | 7/16 |
| MES | 60 | h16 | +0.129 | -0.104 .. +0.362 | +6.3% | +0.359 | 0.28 |  | 8/16 |
| MES | 60 | eod | +0.121 | -0.133 .. +0.375 | +5.6% | +0.330 | 0.37 |  | 6/16 |
| MNQ | 5 | h1 | +0.002 | -0.003 .. +0.008 | +0.5% | +0.005 | 0.48 |  | 9/16 |
| MNQ | 5 | h2 | +0.010 | -0.001 .. +0.021 | +1.2% | +0.015 | 0.099 |  | 10/16 |
| MNQ | 5 | h4 * | +0.021 | -0.001 .. +0.042 | +1.9% | +0.032 | 0.057 | 1 | 10/16 |
| MNQ | 5 | h8 | +0.042 | -0.004 .. +0.089 | +2.6% | +0.063 | 0.075 |  | 9/16 |
| MNQ | 5 | h16 | +0.062 | -0.034 .. +0.157 | +2.6% | +0.112 | 0.27 |  | 9/16 |
| MNQ | 5 | eod | +1.255 | -0.566 .. +3.077 | +10.0% | +2.007 | 0.21 |  | 9/16 |
| MNQ | 15 | h1 | +0.007 | -0.002 .. +0.016 | +1.3% | +0.010 | 0.43 |  | 9/16 |
| MNQ | 15 | h2 | +0.014 | -0.006 .. +0.035 | +1.9% | +0.019 | 0.32 |  | 6/16 |
| MNQ | 15 | h4 | +0.023 | -0.023 .. +0.068 | +2.0% | +0.035 | 0.5 |  | 9/16 |
| MNQ | 15 | h8 | +0.026 | -0.059 .. +0.112 | +1.6% | +0.054 | 0.66 |  | 8/16 |
| MNQ | 15 | h16 | +0.031 | -0.133 .. +0.196 | +1.2% | +0.139 | 0.71 |  | 7/16 |
| MNQ | 15 | eod * | +0.616 | -0.319 .. +1.552 | +9.7% | +0.971 | 0.21 | 1 | 9/16 |
| MNQ | 60 | h1 * | +0.020 | -0.001 .. +0.041 | +3.7% | +0.038 | 0.063 | 1 | 8/16 |
| MNQ | 60 | h2 | +0.024 | -0.014 .. +0.063 | +3.2% | +0.059 | 0.21 |  | 7/16 |
| MNQ | 60 | h4 | +0.019 | -0.052 .. +0.090 | +1.7% | +0.093 | 0.66 |  | 6/16 |
| MNQ | 60 | h8 | +0.052 | -0.087 .. +0.190 | +3.3% | +0.169 | 0.53 |  | 8/16 |
| MNQ | 60 | h16 | +0.147 | -0.110 .. +0.405 | +6.7% | +0.299 | 0.31 |  | 7/16 |
| MNQ | 60 | eod | +0.139 | -0.144 .. +0.422 | +6.0% | +0.273 | 0.44 |  | 8/16 |
| MYM | 5 | h1 | +0.006 | -0.002 .. +0.014 | +1.2% | +0.010 | 0.14 |  | 6/8 |
| MYM | 5 | h2 | +0.018 | +0.001 .. +0.036 | +2.4% | +0.029 | 0.043 |  | 5/8 |
| MYM | 5 | h4 * | +0.041 | +0.005 .. +0.077 | +3.8% | +0.064 | 0.029 | 1 | 7/8 |
| MYM | 5 | h8 | +0.086 | +0.009 .. +0.162 | +5.4% | +0.136 | 0.033 |  | 7/8 |
| MYM | 5 | h16 | +0.149 | +0.001 .. +0.298 | +6.4% | +0.279 | 0.052 |  | 5/8 |
| MYM | 5 | eod | +1.813 | -0.944 .. +4.571 | +15.5% | +4.884 | 0.21 |  | 4/8 |
| MYM | 15 | h1 * | +0.020 | +0.004 .. +0.036 | +3.8% | +0.024 | 0.014 | 1 | 6/8 |
| MYM | 15 | h2 | +0.036 | +0.005 .. +0.068 | +4.8% | +0.049 | 0.025 |  | 5/8 |
| MYM | 15 | h4 | +0.064 | -0.001 .. +0.128 | +5.7% | +0.096 | 0.061 |  | 5/8 |
| MYM | 15 | h8 | +0.112 | -0.014 .. +0.237 | +6.8% | +0.179 | 0.083 |  | 5/8 |
| MYM | 15 | h16 | +0.165 | -0.094 .. +0.424 | +6.7% | +0.421 | 0.21 |  | 4/8 |
| MYM | 15 | eod | +0.725 | -0.602 .. +2.052 | +12.0% | +2.082 | 0.31 |  | 4/8 |
| MYM | 60 | h1 * | +0.038 | +0.005 .. +0.071 | +7.3% | +0.079 | 0.025 | 1 | 4/8 |
| MYM | 60 | h2 | +0.065 | +0.004 .. +0.126 | +8.6% | +0.126 | 0.036 |  | 4/8 |
| MYM | 60 | h4 | +0.061 | -0.045 .. +0.168 | +5.7% | +0.202 | 0.26 |  | 3/8 |
| MYM | 60 | h8 | +0.116 | -0.089 .. +0.321 | +7.5% | +0.372 | 0.29 |  | 3/8 |
| MYM | 60 | h16 | +0.184 | -0.189 .. +0.557 | +8.7% | +0.626 | 0.39 |  | 3/8 |
| MYM | 60 | eod | +0.148 | -0.261 .. +0.556 | +6.6% | +0.577 | 0.57 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.11 pts | -0.76 .. +0.98 | 0.8 |
| MES | 15 | -0.44 pts | -2.01 .. +1.12 | 0.76 |
| MES | 60 | +1.52 pts | -1.61 .. +4.65 | 0.36 |
| MNQ | 5 | +0.56 pts | -0.32 .. +1.44 | 0.21 |
| MNQ | 15 | -0.13 pts | -1.77 .. +1.50 | 0.96 |
| MNQ | 60 | +1.64 pts | -1.61 .. +4.89 | 0.33 |
| MYM | 5 | -0.17 pts | -1.31 .. +0.98 | 0.9 |
| MYM | 15 | -0.08 pts | -2.33 .. +2.17 | 0.94 |
| MYM | 60 | +1.41 pts | -3.12 .. +5.94 | 0.55 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 48220 | +0.003 | 0.315 | +0.01 | -3.49 | -3.48 | -3.50 | -3.49 |
| MES | 5 | h2 | event | long | 48220 | +0.006 | 0.315 | +0.03 | -3.47 | -3.46 | -3.47 | -3.47 |
| MES | 5 | h4 | event | long | 48220 | +0.012 | 0.315 | +0.08 | -3.42 | -3.41 | -3.43 | -3.45 |
| MES | 5 | h8 | event | long | 48220 | +0.027 | 0.315 | +0.16 | -3.34 | -3.33 | -3.34 | -3.42 |
| MES | 5 | h16 | event | long | 48220 | +0.061 | 0.315 | +0.33 | -3.17 | -3.16 | -3.18 | -3.38 |
| MES | 5 | eod | event | long | 48220 | +1.652 | 0.315 | +5.92 | +2.42 | +2.52 | +2.32 | +2.09 |
| MES | 15 | h1 | event | long | 15947 | +0.007 | 0.182 | +0.04 | -3.46 | -3.46 | -3.47 | -3.51 |
| MES | 15 | h2 | event | long | 15947 | +0.016 | 0.182 | +0.10 | -3.40 | -3.39 | -3.40 | -3.49 |
| MES | 15 | h4 | event | long | 15947 | +0.036 | 0.182 | +0.22 | -3.28 | -3.27 | -3.29 | -3.45 |
| MES | 15 | h8 | event | long | 15947 | +0.082 | 0.182 | +0.48 | -3.02 | -2.99 | -3.05 | -3.33 |
| MES | 15 | h16 | event | long | 15947 | +0.193 | 0.182 | +1.25 | -2.25 | -2.36 | -2.13 | -2.74 |
| MES | 15 | eod | event | long | 15947 | +0.896 | 0.182 | +5.96 | +2.46 | +2.52 | +2.40 | +1.77 |
| MES | 60 | h1 | event | long | 3917 | +0.016 | 0.093 | +0.21 | -3.29 | -3.27 | -3.31 | -3.44 |
| MES | 60 | h2 | event | long | 3917 | +0.034 | 0.093 | +0.47 | -3.03 | -2.98 | -3.08 | -3.36 |
| MES | 60 | h4 | event | long | 3917 | +0.075 | 0.093 | +1.30 | -2.20 | -2.33 | -2.06 | -2.92 |
| MES | 60 | h8 | event | long | 3917 | +0.154 | 0.093 | +3.24 | -0.26 | -0.95 | +0.44 | -1.65 |
| MES | 60 | h16 | event | long | 3917 | +0.255 | 0.093 | +5.17 | +1.67 | +1.33 | +2.02 | -0.33 |
| MES | 60 | eod | event | long | 3917 | +0.287 | 0.093 | +5.81 | +2.31 | +2.61 | +2.00 | -0.03 |
| MNQ | 5 | h1 | event | long | 48143 | +0.007 | 0.125 | +0.09 | -1.91 | -1.96 | -1.86 | -1.92 |
| MNQ | 5 | h2 | event | long | 48143 | +0.013 | 0.125 | +0.18 | -1.82 | -1.92 | -1.71 | -1.83 |
| MNQ | 5 | h4 | event | long | 48143 | +0.025 | 0.125 | +0.36 | -1.64 | -1.85 | -1.42 | -1.65 |
| MNQ | 5 | h8 | event | long | 48143 | +0.053 | 0.125 | +0.73 | -1.27 | -1.71 | -0.83 | -1.38 |
| MNQ | 5 | h16 | event | long | 48143 | +0.113 | 0.125 | +1.43 | -0.57 | -1.43 | +0.28 | -0.88 |
| MNQ | 5 | eod | event | long | 48143 | +2.597 | 0.125 | +18.76 | +16.76 | +5.97 | +27.57 | +17.14 |
| MNQ | 15 | h1 | event | long | 15943 | +0.015 | 0.071 | +0.26 | -1.74 | -1.89 | -1.59 | -1.90 |
| MNQ | 15 | h2 | event | long | 15943 | +0.030 | 0.071 | +0.53 | -1.47 | -1.78 | -1.15 | -1.71 |
| MNQ | 15 | h4 | event | long | 15943 | +0.061 | 0.071 | +1.05 | -0.95 | -1.58 | -0.31 | -1.44 |
| MNQ | 15 | h8 | event | long | 15943 | +0.132 | 0.071 | +2.10 | +0.10 | -1.14 | +1.34 | -0.85 |
| MNQ | 15 | h16 | event | long | 15943 | +0.292 | 0.071 | +4.52 | +2.52 | -0.23 | +5.29 | +1.55 |
| MNQ | 15 | eod | event | long | 15943 | +1.306 | 0.071 | +18.77 | +16.77 | +5.95 | +27.66 | +16.17 |
| MNQ | 60 | h1 | event | long | 3917 | +0.028 | 0.036 | +1.00 | -1.00 | -1.57 | -0.42 | -1.22 |
| MNQ | 60 | h2 | event | long | 3917 | +0.055 | 0.036 | +2.03 | +0.03 | -1.13 | +1.22 | -0.41 |
| MNQ | 60 | h4 | event | long | 3917 | +0.113 | 0.036 | +4.55 | +2.55 | -0.21 | +5.37 | +1.65 |
| MNQ | 60 | h8 | event | long | 3917 | +0.221 | 0.036 | +9.84 | +7.84 | +1.77 | +14.05 | +6.29 |
| MNQ | 60 | h16 | event | long | 3917 | +0.378 | 0.036 | +16.82 | +14.82 | +5.06 | +24.79 | +13.03 |
| MNQ | 60 | eod | event | long | 3917 | +0.405 | 0.036 | +18.29 | +16.29 | +5.96 | +26.84 | +13.96 |
| MYM | 5 | h1 | event | long | 24042 | +0.002 | 0.162 | -0.06 | -2.06 | +nan | -2.06 | -2.05 |
| MYM | 5 | h2 | event | long | 24042 | +0.004 | 0.162 | -0.10 | -2.10 | +nan | -2.10 | -2.06 |
| MYM | 5 | h4 | event | long | 24042 | +0.009 | 0.162 | -0.18 | -2.18 | +nan | -2.18 | -2.11 |
| MYM | 5 | h8 | event | long | 24042 | +0.018 | 0.162 | -0.36 | -2.36 | +nan | -2.36 | -2.29 |
| MYM | 5 | h16 | event | long | 24042 | +0.034 | 0.162 | -0.70 | -2.70 | +nan | -2.70 | -2.69 |
| MYM | 5 | eod | event | long | 24042 | +0.720 | 0.162 | -6.93 | -8.93 | +nan | -8.93 | -5.74 |
| MYM | 15 | h1 | event | long | 7945 | +0.005 | 0.091 | -0.15 | -2.15 | +nan | -2.15 | -2.16 |
| MYM | 15 | h2 | event | long | 7945 | +0.011 | 0.091 | -0.28 | -2.28 | +nan | -2.28 | -2.25 |
| MYM | 15 | h4 | event | long | 7945 | +0.025 | 0.091 | -0.54 | -2.54 | +nan | -2.54 | -2.51 |
| MYM | 15 | h8 | event | long | 7945 | +0.050 | 0.091 | -1.11 | -3.11 | +nan | -3.11 | -2.92 |
| MYM | 15 | h16 | event | long | 7945 | +0.128 | 0.091 | -1.99 | -3.99 | +nan | -3.99 | -2.99 |
| MYM | 15 | eod | event | long | 7945 | +0.367 | 0.091 | -6.84 | -8.84 | +nan | -8.84 | -5.62 |
| MYM | 60 | h1 | event | long | 1937 | +0.009 | 0.046 | -0.54 | -2.54 | +nan | -2.54 | -2.54 |
| MYM | 60 | h2 | event | long | 1937 | +0.014 | 0.046 | -1.12 | -3.12 | +nan | -3.12 | -3.13 |
| MYM | 60 | h4 | event | long | 1937 | +0.034 | 0.046 | -1.91 | -3.91 | +nan | -3.91 | -3.90 |
| MYM | 60 | h8 | event | long | 1937 | +0.083 | 0.046 | -2.97 | -4.97 | +nan | -4.97 | -4.78 |
| MYM | 60 | h16 | event | long | 1937 | +0.107 | 0.046 | -6.48 | -8.48 | +nan | -8.48 | -8.22 |
| MYM | 60 | eod | event | long | 1937 | +0.113 | 0.046 | -6.86 | -8.86 | +nan | -8.86 | -8.58 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.006 | -0.009 | -0.005 | -0.003 | -0.001 | +0.000 | +0.001 | +0.001 | +0.002 | +0.003 | +0.011 |
| MES | 15 | +0.013 | +0.000 | -0.007 | -0.006 | -0.004 | +0.000 | +0.004 | +0.008 | +0.016 | +0.040 | +0.129 |
| MES | 60 | -0.018 | -0.053 | -0.014 | -0.005 | -0.003 | +0.000 | +0.007 | +0.014 | +0.034 | +0.100 | +0.139 |
| MNQ | 5 | +0.002 | -0.003 | -0.003 | -0.002 | -0.001 | +0.000 | +0.003 | +0.005 | +0.010 | +0.021 | +0.052 |
| MNQ | 15 | +0.027 | +0.006 | -0.008 | -0.008 | -0.006 | +0.000 | +0.009 | +0.019 | +0.039 | +0.089 | +0.249 |
| MNQ | 60 | -0.131 | -0.116 | -0.047 | -0.021 | -0.011 | +0.000 | +0.016 | +0.033 | +0.078 | +0.201 | +0.332 |
| MYM | 5 | -0.011 | -0.015 | -0.008 | -0.004 | -0.002 | +0.000 | +0.004 | +0.007 | +0.015 | +0.025 | +0.036 |
| MYM | 15 | +0.014 | -0.005 | -0.013 | -0.009 | -0.005 | +0.000 | +0.008 | +0.015 | +0.030 | +0.058 | +0.184 |
| MYM | 60 | +0.137 | -0.007 | +0.020 | +0.009 | +0.002 | +0.000 | +0.005 | +0.004 | +0.022 | +0.115 | +0.155 |

## Calibration

- MES 5-min: 1036271 bars, 48220 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 15947 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3917 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 48143 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 15943 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 3917 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 24042 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 7945 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1937 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
