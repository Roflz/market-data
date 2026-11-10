# Impact card: prior_sess_ret

prior session's open-to-close return in ADR20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -1.125 R20 over the rest of the session (to 16:45), p=0.85; we would catch an effect of 0.027 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 2 bars (10 min) (-0.031 R20, CONFIRMED, q=3.46e-20, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $9.86 at recent bar sizes, 90% range up to $0.56); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.758 R20 over the rest of the session (to 16:45), p=0.43; we would catch an effect of 0.051 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.11).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $11.61 at recent bar sizes, 90% range up to $1.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.241 R20 over the rest of the session (to 16:45), p=0.94; we would catch an effect of 0.095 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.23).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $7.49 at recent bar sizes, 90% range up to $6.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -1.112 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 2 bars (10 min) (-0.020 R20, CONFIRMED, q=0.00603, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $15.75 at recent bar sizes, 90% range up to $0.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.844 R20 over the rest of the session (to 16:45), p=0.77; we would catch an effect of 0.072 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.93).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $20.91 at recent bar sizes, 90% range up to $2.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.026 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.103 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.59).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.32 at recent bar sizes, 90% range up to $10.01); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.051 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.02 at recent bar sizes, 90% range up to $0.54); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.233 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.73 at recent bar sizes, 90% range up to $1.99); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.140 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.24).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.15 at recent bar sizes, 90% range up to $6.17); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.006 .. +0.002 | -0.0007 | 0.36 / 0.34 / 0.37 | 0.376 |  |  | 11/16 | -0.004 | +0.000 |  | -0.9 / -0.9 |  |
| MES | 5 | h2 | -0.005 | -0.013 .. +0.004 | -0.0015 | 0.28 / 0.27 / 0.3 | 0.299 |  |  | 10/16 | -0.010 | +0.000 |  | -1.4 / -1.1 |  |
| MES | 5 | h4 | -0.011 | -0.029 .. +0.007 | -0.0024 | 0.24 / 0.23 / 0.26 | 0.261 |  |  | 10/16 | -0.021 | -0.000 |  | -2.1 / -1.2 | 0.027 |
| MES | 5 | h8 | -0.022 | -0.058 .. +0.015 | -0.0033 | 0.25 / 0.24 / 0.27 | 0.271 |  |  | 10/16 | -0.044 | +0.000 |  | -2.9 / -1.2 |  |
| MES | 5 | h16 | -0.036 | -0.112 .. +0.039 | -0.0035 | 0.35 / 0.34 / 0.36 | 0.365 |  |  | 9/16 | -0.086 | +0.012 |  | -3.5 / -0.9 |  |
| MES | 5 | eod * | -1.125 | -2.388 .. +0.138 | -0.0143 | 0.081 / 0.076 / 0.094 | 0.093 | 1 | 1 | 11/16 | -1.582 | -0.673 | False | -21.9 / -1.7 |  |
| MES | 15 | h1 | -0.005 | -0.013 .. +0.003 | -0.0016 | 0.21 / 0.21 / 0.23 | 0.234 |  |  | 10/16 | -0.009 | -0.002 |  | -1.2 / -1.3 |  |
| MES | 15 | h2 | -0.012 | -0.030 .. +0.005 | -0.0035 | 0.16 / 0.16 / 0.16 | 0.159 |  |  | 10/16 | -0.019 | -0.006 |  | -1.8 / -1.4 |  |
| MES | 15 | h4 | -0.024 | -0.060 .. +0.012 | -0.0047 | 0.19 / 0.18 / 0.18 | 0.185 |  |  | 10/16 | -0.039 | -0.009 |  | -2.3 / -1.3 | 0.051 |
| MES | 15 | h8 | -0.047 | -0.118 .. +0.024 | -0.0057 | 0.19 / 0.18 / 0.2 | 0.205 |  |  | 10/16 | -0.083 | -0.012 |  | -3.3 / -1.3 |  |
| MES | 15 | h16 | -0.114 | -0.262 .. +0.035 | -0.0093 | 0.13 / 0.13 / 0.14 | 0.138 |  |  | 10/16 | -0.182 | -0.046 |  | -5.7 / -1.5 |  |
| MES | 15 | eod * | -0.758 | -1.525 .. +0.009 | -0.0222 | 0.053 / 0.049 / 0.049 | 0.0511 | 1 | 1 | 11/16 | -0.949 | -0.569 | False | -13.7 / -1.9 |  |
| MES | 60 | h1 | -0.014 | -0.031 .. +0.003 | -0.0045 | 0.098 / 0.091 / 0.12 | 0.119 |  |  | 12/16 | -0.024 | -0.004 |  | -1.7 / -1.7 |  |
| MES | 60 | h2 | -0.030 | -0.064 .. +0.003 | -0.0068 | 0.073 / 0.068 / 0.092 | 0.0917 |  |  | 12/16 | -0.052 | -0.009 |  | -2.6 / -1.8 |  |
| MES | 60 | h4 | -0.054 | -0.120 .. +0.011 | -0.0072 | 0.1 / 0.098 / 0.13 | 0.125 |  |  | 12/16 | -0.095 | -0.014 |  | -3.3 / -1.6 | 0.095 |
| MES | 60 | h8 | -0.113 | -0.239 .. +0.014 | -0.0103 | 0.081 / 0.075 / 0.1 | 0.104 |  |  | 11/16 | -0.188 | -0.038 |  | -4.9 / -1.7 |  |
| MES | 60 | h16 | -0.210 | -0.437 .. +0.016 | -0.0139 | 0.068 / 0.065 / 0.088 | 0.0933 |  |  | 12/16 | -0.343 | -0.078 |  | -7.0 / -1.8 |  |
| MES | 60 | eod * | -0.241 | -0.496 .. +0.015 | -0.0149 | 0.065 / 0.063 / 0.083 | 0.087 | 1 | 1 | 12/16 | -0.368 | -0.114 | False | -7.6 / -1.8 |  |
| MNQ | 5 | h1 | +0.003 | -0.002 .. +0.007 | +0.0005 | 0.3 / 0.3 / 0.32 | 0.33 |  |  | 10/16 | +0.002 | +0.003 |  | +0.9 / +1.0 |  |
| MNQ | 5 | h2 | +0.004 | -0.007 .. +0.015 | -0.0001 | 0.49 / 0.5 / 0.51 | 0.518 |  |  | 10/16 | +0.003 | +0.005 |  | +0.7 / +0.7 |  |
| MNQ | 5 | h4 | +0.003 | -0.019 .. +0.026 | -0.0009 | 0.77 / 0.77 / 0.78 | 0.796 |  |  | 8/16 | +0.004 | +0.003 |  | +0.4 / +0.3 | 0.035 |
| MNQ | 5 | h8 | +0.001 | -0.042 .. +0.045 | -0.0015 | 0.96 / 0.96 / 0.96 | 0.963 |  |  | 8/16 | +0.006 | -0.003 |  | +0.1 / +0.0 |  |
| MNQ | 5 | h16 | +0.009 | -0.075 .. +0.092 | -0.0010 | 0.84 / 0.84 / 0.86 | 0.865 |  |  | 8/16 | +0.015 | +0.002 |  | +0.5 / +0.2 |  |
| MNQ | 5 | eod * | -1.112 | -2.789 .. +0.566 | -0.0230 | 0.19 / 0.18 / 0.19 | 0.181 | 1 | 1 | 10/16 | -0.915 | -1.305 | False | -14.9 / -1.3 |  |
| MNQ | 15 | h1 | +0.001 | -0.008 .. +0.009 | -0.0000 | 0.84 / 0.84 / 0.84 | 0.842 |  |  | 9/16 | -0.000 | +0.002 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h2 | -0.006 | -0.026 .. +0.014 | -0.0029 | 0.56 / 0.56 / 0.58 | 0.58 |  |  | 7/16 | -0.000 | -0.012 |  | -0.6 / -0.6 |  |
| MNQ | 15 | h4 | -0.017 | -0.064 .. +0.030 | -0.0040 | 0.47 / 0.47 / 0.48 | 0.473 |  |  | 7/16 | -0.003 | -0.031 |  | -0.9 / -0.7 | 0.072 |
| MNQ | 15 | h8 | -0.039 | -0.127 .. +0.049 | -0.0061 | 0.38 / 0.38 / 0.39 | 0.391 |  |  | 7/16 | -0.018 | -0.060 |  | -1.6 / -0.9 |  |
| MNQ | 15 | h16 | -0.118 | -0.317 .. +0.080 | -0.0132 | 0.24 / 0.24 / 0.21 | 0.208 |  |  | 8/16 | -0.064 | -0.172 |  | -4.0 / -1.2 |  |
| MNQ | 15 | eod * | -0.844 | -1.930 .. +0.242 | -0.0308 | 0.13 / 0.11 / 0.075 | 0.0766 | 1 | 1 | 9/16 | -0.543 | -1.141 | False | -9.3 / -1.5 |  |
| MNQ | 60 | h1 | -0.013 | -0.030 .. +0.004 | -0.0080 | 0.14 / 0.13 / 0.17 | 0.174 |  |  | 11/16 | -0.015 | -0.011 |  | -1.5 / -1.5 |  |
| MNQ | 60 | h2 * | -0.026 | -0.061 .. +0.008 | -0.0112 | 0.14 / 0.13 / 0.17 | 0.172 | 1 | 1 | 11/16 | -0.030 | -0.023 | False | -2.1 / -1.5 |  |
| MNQ | 60 | h4 | -0.050 | -0.118 .. +0.019 | -0.0147 | 0.16 / 0.15 / 0.19 | 0.188 |  |  | 11/16 | -0.055 | -0.045 |  | -2.8 / -1.4 | 0.103 |
| MNQ | 60 | h8 | -0.089 | -0.221 .. +0.042 | -0.0194 | 0.18 / 0.17 / 0.22 | 0.219 |  |  | 10/16 | -0.093 | -0.085 |  | -3.7 / -1.3 |  |
| MNQ | 60 | h16 | -0.166 | -0.404 .. +0.072 | -0.0268 | 0.17 / 0.16 / 0.21 | 0.203 |  |  | 11/16 | -0.176 | -0.156 |  | -5.3 / -1.4 |  |
| MNQ | 60 | eod | -0.199 | -0.467 .. +0.069 | -0.0302 | 0.15 / 0.13 / 0.17 | 0.174 |  |  | 11/16 | -0.197 | -0.200 |  | -6.1 / -1.5 |  |
| MYM | 5 | h1 * | +0.003 | -0.004 .. +0.010 | +0.0011 | 0.4 / 0.4 / 0.46 | 0.466 | 1 | 1 | 5/8 | n/a | +0.003 | False | +0.6 / +0.8 |  |
| MYM | 5 | h2 | +0.005 | -0.009 .. +0.020 | +0.0013 | 0.49 / 0.5 / 0.58 | 0.582 |  |  | 5/8 | n/a | +0.005 |  | +0.6 / +0.7 |  |
| MYM | 5 | h4 | +0.007 | -0.025 .. +0.040 | +0.0011 | 0.66 / 0.67 / 0.72 | 0.72 |  |  | 5/8 | n/a | +0.007 |  | +0.5 / +0.4 | 0.051 |
| MYM | 5 | h8 | +0.014 | -0.053 .. +0.081 | +0.0011 | 0.69 / 0.7 / 0.73 | 0.729 |  |  | 5/8 | n/a | +0.014 |  | +0.7 / +0.4 |  |
| MYM | 5 | h16 | +0.018 | -0.125 .. +0.160 | +0.0004 | 0.81 / 0.81 / 0.8 | 0.793 |  |  | 6/8 | n/a | +0.018 |  | +0.7 / +0.2 |  |
| MYM | 5 | eod | +0.306 | -1.782 .. +2.395 | +0.0096 | 0.77 / 0.78 / 0.76 | 0.766 |  |  | 5/8 | n/a | +0.306 |  | +3.1 / +0.3 |  |
| MYM | 15 | h1 | +0.002 | -0.011 .. +0.014 | +0.0006 | 0.81 / 0.81 / 0.8 | 0.799 |  |  | 4/8 | n/a | +0.002 |  | +0.2 / +0.2 |  |
| MYM | 15 | h2 | -0.007 | -0.050 .. +0.036 | -0.0031 | 0.75 / 0.76 / 0.69 | 0.71 |  |  | 3/8 | n/a | -0.007 |  | -0.5 / -0.3 |  |
| MYM | 15 | h4 | -0.016 | -0.111 .. +0.079 | -0.0045 | 0.74 / 0.75 / 0.68 | 0.693 |  |  | 3/8 | n/a | -0.016 |  | -0.5 / -0.3 | 0.076 |
| MYM | 15 | h8 | -0.024 | -0.191 .. +0.144 | -0.0056 | 0.78 / 0.79 / 0.74 | 0.753 |  |  | 3/8 | n/a | -0.024 |  | -0.6 / -0.3 |  |
| MYM | 15 | h16 | -0.050 | -0.404 .. +0.303 | -0.0093 | 0.78 / 0.79 / 0.73 | 0.756 |  |  | 3/8 | n/a | -0.050 |  | -1.0 / -0.3 |  |
| MYM | 15 | eod * | -0.233 | -1.624 .. +1.158 | -0.0069 | 0.74 / 0.75 / 0.71 | 0.73 | 1 | 1 | 3/8 | n/a | -0.233 | False | -1.9 / -0.3 |  |
| MYM | 60 | h1 * | +0.006 | -0.017 .. +0.029 | +0.0050 | 0.61 / 0.61 / 0.62 | 0.626 | 1 | 1 | 5/8 | n/a | +0.006 | False | +0.5 / +0.5 |  |
| MYM | 60 | h2 | +0.008 | -0.038 .. +0.054 | +0.0062 | 0.74 / 0.74 / 0.74 | 0.749 |  |  | 5/8 | n/a | +0.008 |  | +0.5 / +0.3 |  |
| MYM | 60 | h4 | +0.017 | -0.073 .. +0.108 | +0.0094 | 0.71 / 0.71 / 0.72 | 0.724 |  |  | 6/8 | n/a | +0.017 |  | +0.7 / +0.4 | 0.140 |
| MYM | 60 | h8 | +0.035 | -0.139 .. +0.209 | +0.0136 | 0.69 / 0.7 / 0.71 | 0.717 |  |  | 6/8 | n/a | +0.035 |  | +1.1 / +0.4 |  |
| MYM | 60 | h16 | +0.054 | -0.257 .. +0.365 | +0.0197 | 0.73 / 0.74 / 0.74 | 0.752 |  |  | 6/8 | n/a | +0.054 |  | +1.2 / +0.3 |  |
| MYM | 60 | eod | +0.046 | -0.303 .. +0.396 | +0.0223 | 0.79 / 0.8 / 0.8 | 0.802 |  |  | 5/8 | n/a | +0.046 |  | +1.0 / +0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.015 | -0.018 .. -0.012 | -3.0% | +0.001 | 1.1e-18 |  | 16/16 |
| MES | 5 | h2 * | -0.031 | -0.037 .. -0.025 | -4.4% | -0.015 | 5.9e-23 | 3.46e-20 | 16/16 |
| MES | 5 | h4 | -0.052 | -0.063 .. -0.041 | -5.2% | -0.042 | 6.7e-18 |  | 15/16 |
| MES | 5 | h8 | -0.078 | -0.100 .. -0.055 | -5.4% | -0.085 | 1.5e-09 |  | 13/16 |
| MES | 5 | h16 | -0.108 | -0.153 .. -0.064 | -5.2% | -0.146 | 6.7e-06 |  | 13/16 |
| MES | 5 | eod | +0.030 | -0.812 .. +0.873 | +0.3% | -0.035 | 0.94 |  | 7/16 |
| MES | 15 | h1 * | -0.007 | -0.013 .. -0.001 | -1.5% | +0.016 | 0.018 | 1 | 13/16 |
| MES | 15 | h2 | -0.016 | -0.028 .. -0.005 | -2.3% | +0.009 | 0.018 |  | 13/16 |
| MES | 15 | h4 | -0.024 | -0.050 .. +0.002 | -2.3% | -0.004 | 0.12 |  | 12/16 |
| MES | 15 | h8 | -0.040 | -0.088 .. +0.009 | -2.6% | -0.023 | 0.14 |  | 11/16 |
| MES | 15 | h16 | -0.060 | -0.154 .. +0.033 | -2.6% | -0.063 | 0.24 |  | 11/16 |
| MES | 15 | eod | -0.030 | -0.588 .. +0.528 | -0.5% | -0.076 | 0.92 |  | 11/16 |
| MES | 60 | h1 * | +0.013 | +0.001 .. +0.025 | +2.5% | +0.030 | 0.038 | 1 | 11/16 |
| MES | 60 | h2 | +0.013 | -0.010 .. +0.036 | +1.7% | +0.030 | 0.28 |  | 10/16 |
| MES | 60 | h4 | +0.011 | -0.032 .. +0.054 | +1.0% | +0.021 | 0.62 |  | 10/16 |
| MES | 60 | h8 | -0.005 | -0.083 .. +0.073 | -0.3% | -0.003 | 0.96 |  | 7/16 |
| MES | 60 | h16 | -0.006 | -0.149 .. +0.137 | -0.3% | -0.047 | 0.96 |  | 9/16 |
| MES | 60 | eod | -0.002 | -0.168 .. +0.165 | -0.1% | -0.057 | 1 |  | 9/16 |
| MNQ | 5 | h1 | -0.008 | -0.012 .. -0.004 | -1.5% | +0.005 | 9.8e-05 |  | 16/16 |
| MNQ | 5 | h2 * | -0.020 | -0.029 .. -0.011 | -2.6% | +0.000 | 2.7e-05 | 0.00603 | 15/16 |
| MNQ | 5 | h4 | -0.038 | -0.056 .. -0.021 | -3.5% | -0.016 | 0.00011 |  | 14/16 |
| MNQ | 5 | h8 | -0.062 | -0.094 .. -0.030 | -3.8% | -0.054 | 0.0027 |  | 14/16 |
| MNQ | 5 | h16 | -0.119 | -0.175 .. -0.062 | -5.0% | -0.125 | 0.0017 |  | 13/16 |
| MNQ | 5 | eod | -0.180 | -1.242 .. +0.882 | -1.4% | -0.870 | 0.86 |  | 7/16 |
| MNQ | 15 | h1 * | -0.005 | -0.011 .. +0.002 | -0.9% | +0.024 | 0.15 | 1 | 13/16 |
| MNQ | 15 | h2 | -0.010 | -0.026 .. +0.006 | -1.3% | +0.023 | 0.23 |  | 11/16 |
| MNQ | 15 | h4 | -0.019 | -0.073 .. +0.035 | -1.7% | +0.018 | 0.49 |  | 12/16 |
| MNQ | 15 | h8 | -0.048 | -0.151 .. +0.055 | -2.9% | +0.002 | 0.36 |  | 13/16 |
| MNQ | 15 | h16 | -0.108 | -0.262 .. +0.045 | -4.3% | -0.030 | 0.17 |  | 13/16 |
| MNQ | 15 | eod | -0.099 | -0.926 .. +0.728 | -1.6% | -0.432 | 0.99 |  | 10/16 |
| MNQ | 60 | h1 | +0.005 | -0.009 .. +0.018 | +0.9% | +0.025 | 0.74 |  | 7/16 |
| MNQ | 60 | h2 | -0.008 | -0.031 .. +0.016 | -1.0% | +0.015 | 0.52 |  | 10/16 |
| MNQ | 60 | h4 | -0.025 | -0.069 .. +0.018 | -2.3% | -0.015 | 0.28 |  | 10/16 |
| MNQ | 60 | h8 * | -0.075 | -0.152 .. +0.002 | -4.7% | -0.085 | 0.098 | 1 | 12/16 |
| MNQ | 60 | h16 | -0.122 | -0.263 .. +0.019 | -5.6% | -0.215 | 0.14 |  | 9/16 |
| MNQ | 60 | eod | -0.114 | -0.276 .. +0.048 | -5.0% | -0.228 | 0.24 |  | 8/16 |
| MYM | 5 | h1 | -0.001 | -0.006 .. +0.004 | -0.1% | +0.011 | 0.87 |  | 4/8 |
| MYM | 5 | h2 | -0.006 | -0.017 .. +0.005 | -0.8% | +0.016 | 0.7 |  | 5/8 |
| MYM | 5 | h4 | -0.004 | -0.030 .. +0.021 | -0.4% | +0.018 | 0.89 |  | 4/8 |
| MYM | 5 | h8 | +0.006 | -0.046 .. +0.057 | +0.3% | +0.029 | 0.84 |  | 5/8 |
| MYM | 5 | h16 | +0.049 | -0.061 .. +0.160 | +2.1% | +0.112 | 0.39 |  | 4/8 |
| MYM | 5 | eod * | +0.720 | -0.775 .. +2.215 | +6.2% | +1.793 | 0.35 | 1 | 5/8 |
| MYM | 15 | h1 | +0.002 | -0.008 .. +0.011 | +0.4% | +0.027 | 0.7 |  | 4/8 |
| MYM | 15 | h2 | +0.015 | -0.023 .. +0.052 | +1.9% | +0.045 | 0.45 |  | 3/8 |
| MYM | 15 | h4 * | +0.043 | -0.057 .. +0.144 | +3.9% | +0.087 | 0.41 | 1 | 3/8 |
| MYM | 15 | h8 | +0.062 | -0.112 .. +0.237 | +3.8% | +0.169 | 0.49 |  | 4/8 |
| MYM | 15 | h16 | +0.095 | -0.216 .. +0.406 | +3.9% | +0.326 | 0.56 |  | 5/8 |
| MYM | 15 | eod | +0.299 | -0.851 .. +1.450 | +5.0% | +0.609 | 0.62 |  | 4/8 |
| MYM | 60 | h1 * | +0.020 | +0.001 .. +0.038 | +3.8% | +0.029 | 0.04 | 1 | 5/8 |
| MYM | 60 | h2 | +0.021 | -0.012 .. +0.054 | +2.7% | +0.038 | 0.22 |  | 5/8 |
| MYM | 60 | h4 | +0.022 | -0.037 .. +0.081 | +2.0% | +0.044 | 0.46 |  | 5/8 |
| MYM | 60 | h8 | -0.008 | -0.117 .. +0.102 | -0.5% | +0.044 | 0.89 |  | 3/8 |
| MYM | 60 | h16 | -0.051 | -0.258 .. +0.157 | -2.4% | +0.008 | 0.93 |  | 3/8 |
| MYM | 60 | eod | -0.052 | -0.291 .. +0.188 | -2.3% | +0.001 | 0.95 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.43 pts | -1.05 .. +0.19 | 0.28 |
| MES | 15 | -0.15 pts | -1.25 .. +0.95 | 0.9 |
| MES | 60 | -0.43 pts | -2.78 .. +1.91 | 0.91 |
| MNQ | 5 | +0.14 pts | -0.46 .. +0.75 | 0.64 |
| MNQ | 15 | +0.77 pts | -0.33 .. +1.87 | 0.17 |
| MNQ | 60 | +0.32 pts | -2.00 .. +2.64 | 0.79 |
| MYM | 5 | +0.56 pts | -0.27 .. +1.40 | 0.19 |
| MYM | 15 | +0.07 pts | -1.45 .. +1.58 | 0.93 |
| MYM | 60 | +0.41 pts | -2.74 .. +3.56 | 0.83 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 203756 | +0.003 | 0.247 | +0.07 | -3.43 | -3.47 | -3.39 | -3.43 |
| MES | 5 | h2 | bottom fifth | long | 203756 | +0.008 | 0.247 | +0.15 | -3.35 | -3.43 | -3.28 | -3.36 |
| MES | 5 | h4 | bottom fifth | long | 203756 | +0.016 | 0.247 | +0.31 | -3.19 | -3.34 | -3.06 | -3.24 |
| MES | 5 | h8 | bottom fifth | long | 203756 | +0.033 | 0.247 | +0.60 | -2.90 | -3.17 | -2.66 | -3.01 |
| MES | 5 | h16 | bottom fifth | long | 203756 | +0.064 | 0.247 | +1.17 | -2.33 | -2.84 | -1.88 | -2.61 |
| MES | 5 | eod | bottom fifth | long | 203756 | +0.994 | 0.247 | +11.24 | +7.74 | +2.29 | +12.52 | +6.95 |
| MES | 15 | h1 | bottom fifth | long | 67443 | +0.008 | 0.140 | +0.22 | -3.28 | -3.40 | -3.17 | -3.32 |
| MES | 15 | h2 | bottom fifth | long | 67443 | +0.015 | 0.140 | +0.45 | -3.05 | -3.27 | -2.86 | -3.12 |
| MES | 15 | h4 | bottom fifth | long | 67443 | +0.029 | 0.140 | +0.88 | -2.62 | -3.01 | -2.28 | -2.75 |
| MES | 15 | h8 | bottom fifth | long | 67443 | +0.058 | 0.140 | +1.72 | -1.78 | -2.54 | -1.12 | -2.05 |
| MES | 15 | h16 | bottom fifth | long | 67443 | +0.115 | 0.140 | +3.18 | -0.32 | -1.80 | +0.98 | -0.61 |
| MES | 15 | eod | bottom fifth | long | 67443 | +0.512 | 0.140 | +11.32 | +7.82 | +2.29 | +12.65 | +7.79 |
| MES | 60 | h1 | bottom fifth | long | 16630 | +0.016 | 0.071 | +0.85 | -2.65 | -3.04 | -2.31 | -2.84 |
| MES | 60 | h2 | bottom fifth | long | 16630 | +0.031 | 0.071 | +1.68 | -1.82 | -2.59 | -1.13 | -2.24 |
| MES | 60 | h4 | bottom fifth | long | 16630 | +0.059 | 0.071 | +3.15 | -0.35 | -1.87 | +0.99 | -1.30 |
| MES | 60 | h8 | bottom fifth | long | 16630 | +0.113 | 0.071 | +5.81 | +2.31 | -0.39 | +4.69 | +0.48 |
| MES | 60 | h16 | bottom fifth | long | 16630 | +0.191 | 0.071 | +9.62 | +6.12 | +1.72 | +10.01 | +3.28 |
| MES | 60 | eod | bottom fifth | long | 16630 | +0.220 | 0.071 | +11.00 | +7.50 | +2.11 | +12.26 | +3.92 |
| MNQ | 5 | h1 | top fifth | long | 203168 | +0.003 | 0.136 | -0.01 | -2.01 | -2.00 | -2.03 | -2.03 |
| MNQ | 5 | h2 | top fifth | long | 203168 | +0.003 | 0.136 | -0.02 | -2.02 | -1.99 | -2.05 | -2.04 |
| MNQ | 5 | h4 | top fifth | long | 203168 | +0.003 | 0.136 | -0.05 | -2.05 | -1.99 | -2.10 | -2.07 |
| MNQ | 5 | h8 | top fifth | long | 203168 | +0.003 | 0.136 | -0.08 | -2.08 | -1.98 | -2.18 | -2.18 |
| MNQ | 5 | h16 | top fifth | long | 203168 | +0.013 | 0.136 | -0.15 | -2.15 | -1.96 | -2.31 | -2.43 |
| MNQ | 5 | eod | bottom fifth | long | 203567 | +0.521 | 0.096 | +15.17 | +13.17 | -0.13 | +24.07 | +15.64 |
| MNQ | 15 | h1 | top fifth | long | 67332 | +0.005 | 0.079 | -0.04 | -2.04 | -1.99 | -2.08 | -2.16 |
| MNQ | 15 | h2 | bottom fifth | long | 67406 | +0.003 | 0.055 | +0.57 | -1.43 | -1.91 | -1.05 | -1.57 |
| MNQ | 15 | h4 | bottom fifth | long | 67406 | +0.007 | 0.055 | +1.12 | -0.88 | -1.81 | -0.11 | -1.14 |
| MNQ | 15 | h8 | bottom fifth | long | 67406 | +0.022 | 0.055 | +2.23 | +0.23 | -1.65 | +1.76 | -0.32 |
| MNQ | 15 | h16 | bottom fifth | long | 67406 | +0.057 | 0.055 | +4.26 | +2.26 | -1.41 | +5.26 | +2.15 |
| MNQ | 15 | eod | bottom fifth | long | 67406 | +0.283 | 0.055 | +15.35 | +13.35 | -0.10 | +24.38 | +15.83 |
| MNQ | 60 | h1 | bottom fifth | long | 16627 | +0.008 | 0.027 | +1.10 | -0.90 | -1.82 | -0.15 | -1.06 |
| MNQ | 60 | h2 | bottom fifth | long | 16627 | +0.015 | 0.027 | +2.21 | +0.21 | -1.66 | +1.75 | -0.20 |
| MNQ | 60 | h4 | bottom fifth | long | 16627 | +0.029 | 0.027 | +4.23 | +2.23 | -1.42 | +5.23 | +1.35 |
| MNQ | 60 | h8 | bottom fifth | long | 16627 | +0.055 | 0.027 | +8.03 | +6.03 | -0.87 | +11.71 | +4.26 |
| MNQ | 60 | h16 | bottom fifth | long | 16627 | +0.091 | 0.027 | +13.42 | +11.42 | -0.05 | +20.88 | +9.10 |
| MNQ | 60 | eod | bottom fifth | long | 16627 | +0.103 | 0.027 | +14.88 | +12.88 | -0.11 | +23.60 | +9.89 |
| MYM | 5 | h1 | top fifth | long | 101531 | +0.001 | 0.173 | -0.01 | -2.01 | +nan | -2.01 | -2.00 |
| MYM | 5 | h2 | top fifth | long | 101531 | +0.001 | 0.173 | -0.00 | -2.00 | +nan | -2.00 | -1.97 |
| MYM | 5 | h4 | top fifth | long | 101531 | -0.003 | 0.173 | +0.00 | -2.00 | +nan | -2.00 | -1.93 |
| MYM | 5 | h8 | top fifth | long | 101531 | -0.005 | 0.173 | +0.02 | -1.98 | +nan | -1.98 | -1.91 |
| MYM | 5 | h16 | top fifth | long | 101531 | +0.005 | 0.173 | +0.06 | -1.94 | +nan | -1.94 | -1.94 |
| MYM | 5 | eod | top fifth | long | 101531 | +0.116 | 0.173 | -1.13 | -3.13 | +nan | -3.13 | -3.21 |
| MYM | 15 | h1 | top fifth | long | 33622 | +0.003 | 0.098 | +0.01 | -1.99 | +nan | -1.99 | -2.01 |
| MYM | 15 | h2 | bottom fifth | long | 33660 | +0.001 | 0.076 | +0.33 | -1.67 | +nan | -1.67 | -1.62 |
| MYM | 15 | h4 | bottom fifth | long | 33660 | +0.001 | 0.076 | +0.62 | -1.38 | +nan | -1.38 | -1.28 |
| MYM | 15 | h8 | bottom fifth | long | 33660 | -0.000 | 0.076 | +1.17 | -0.83 | +nan | -0.83 | -0.61 |
| MYM | 15 | h16 | bottom fifth | long | 33660 | -0.010 | 0.076 | +2.08 | +0.08 | +nan | +0.08 | +0.69 |
| MYM | 15 | eod | bottom fifth | long | 33660 | -0.046 | 0.076 | +7.54 | +5.54 | +nan | +5.54 | +6.28 |
| MYM | 60 | h1 | top fifth | long | 8261 | +0.010 | 0.047 | +0.04 | -1.96 | +nan | -1.96 | -2.12 |
| MYM | 60 | h2 | top fifth | long | 8261 | +0.018 | 0.047 | +0.02 | -1.98 | +nan | -1.98 | -2.38 |
| MYM | 60 | h4 | top fifth | long | 8261 | +0.030 | 0.047 | +0.05 | -1.95 | +nan | -1.95 | -2.75 |
| MYM | 60 | h8 | top fifth | long | 8261 | +0.048 | 0.047 | -0.18 | -2.18 | +nan | -2.18 | -3.54 |
| MYM | 60 | h16 | top fifth | long | 8261 | +0.078 | 0.047 | -1.37 | -3.37 | +nan | -3.37 | -5.99 |
| MYM | 60 | eod | top fifth | long | 8261 | +0.072 | 0.047 | -2.34 | -4.34 | +nan | -4.34 | -7.59 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.141 | +0.071 | +0.030 | +0.012 | +0.005 | +0.000 | -0.001 | -0.003 | -0.008 | -0.015 | -0.023 |
| MES | 15 | +0.911 | +0.477 | +0.202 | +0.079 | +0.030 | +0.000 | -0.004 | -0.008 | -0.015 | -0.032 | -0.089 |
| MES | 60 | +2.379 | +1.256 | +0.573 | +0.233 | +0.093 | +0.000 | -0.012 | -0.025 | -0.042 | -0.074 | -0.189 |
| MNQ | 5 | +0.167 | +0.083 | +0.033 | +0.013 | +0.005 | +0.000 | +0.001 | +0.001 | +0.002 | +0.000 | +0.013 |
| MNQ | 15 | +0.968 | +0.510 | +0.221 | +0.088 | +0.036 | +0.000 | -0.008 | -0.014 | -0.023 | -0.038 | -0.110 |
| MNQ | 60 | +2.570 | +1.341 | +0.621 | +0.249 | +0.100 | +0.000 | -0.010 | -0.020 | -0.036 | -0.055 | -0.083 |
| MYM | 5 | +0.112 | +0.058 | +0.025 | +0.009 | +0.004 | +0.000 | -0.001 | +0.002 | +0.004 | +0.013 | +0.019 |
| MYM | 15 | +0.855 | +0.460 | +0.198 | +0.080 | +0.034 | +0.000 | -0.013 | -0.024 | -0.036 | -0.047 | -0.086 |
| MYM | 60 | +2.269 | +1.201 | +0.544 | +0.218 | +0.086 | +0.000 | +0.004 | +0.007 | +0.026 | +0.053 | +0.055 |

## Calibration

- MES 5-min: 1018598 bars, 203506 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 337156 bars, 67369 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83051 bars, 16596 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1016931 bars, 203168 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 337005 bars, 67332 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83049 bars, 16595 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 508256 bars, 101531 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 168240 bars, 33622 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41312 bars, 8261 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
