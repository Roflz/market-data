# Impact card: pat_inside_bar

candle pattern inside_bar (no direction): high < previous high AND low > previous low [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.014 R20 over the next 8 bars (40 min), p=0.43; we would catch an effect of 0.015 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.320 R20, possible, q=0.057, 11 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $0.51); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.016 R20 over the next 2 bars (30 min), p=0.15; we would catch an effect of 0.026 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.009 R20, possible, q=0.217, 13 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.42 at recent bar sizes, 90% range up to $1.16); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.049 R20 over the rest of the session (to 16:45), p=0.78; we would catch an effect of 0.047 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.88).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.48 at recent bar sizes, 90% range up to $3.70); about 1.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.013 R20 over the next 4 bars (20 min), p=0.25; we would catch an effect of 0.017 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS after the event than after matched bars over the next 8 bars (40 min) (-0.048 R20, CONFIRMED, q=0.00748, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.30 at recent bar sizes, 90% range up to $0.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.008 R20 over the next 1 bar (15 min), p=0.8; we would catch an effect of 0.028 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% LESS after the event than after matched bars over the next 16 bars (4 h) (-0.079 R20, possible, q=0.243, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.31 at recent bar sizes, 90% range up to $1.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.018 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.46 at recent bar sizes, 90% range up to $5.41); about 54.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.027 R20 over the next 4 bars (20 min), p=0.099; we would catch an effect of 0.023 R20 or more 80% of the time).
- MYM 5-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.020 R20, CONFIRMED, q=0.011, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.29 at recent bar sizes, 90% range up to $0.66); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.094 R20 over the next 16 bars (4 h), p=0.4; we would catch an effect of 0.040 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.13).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.75 at recent bar sizes, 90% range up to $1.58); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.062 R20 over the rest of the session (to 16:45), p=0.78; we would catch an effect of 0.063 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.52).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.32 at recent bar sizes, 90% range up to $4.52); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.004 | -0.009 .. +0.001 | -0.0014 | 0.14 / 0.13 / 0.13 | 0.138 |  |  | 12/16 | -0.007 | -0.001 |  | -1.5 / -1.5 |  |
| MES | 5 | h2 | +0.001 | -0.006 .. +0.008 | +0.0003 | 0.75 / 0.74 / 0.8 | 0.793 |  |  | 9/16 | -0.003 | +0.005 |  | +0.3 / +0.3 |  |
| MES | 5 | h4 | +0.006 | -0.004 .. +0.016 | +0.0011 | 0.22 / 0.22 / 0.29 | 0.278 |  |  | 11/16 | -0.003 | +0.016 |  | +1.2 / +1.2 | 0.015 |
| MES | 5 | h8 * | +0.014 | -0.000 .. +0.029 | +0.0017 | 0.055 / 0.056 / 0.067 | 0.0669 | 1 | 1 | 11/16 | -0.004 | +0.033 | False | +1.9 / +1.9 |  |
| MES | 5 | h16 | +0.012 | -0.011 .. +0.035 | +0.0010 | 0.3 / 0.29 / 0.32 | 0.323 |  |  | 9/16 | -0.006 | +0.031 |  | +1.1 / +1.0 |  |
| MES | 5 | eod | +0.074 | -0.121 .. +0.269 | +0.0012 | 0.46 / 0.46 / 0.34 | 0.345 |  |  | 10/16 | +0.015 | +0.133 |  | +1.4 / +0.7 |  |
| MES | 15 | h1 | +0.008 | +0.000 .. +0.016 | +0.0031 | 0.048 / 0.054 / 0.063 | 0.0636 |  |  | 12/16 | +0.009 | +0.008 |  | +1.9 / +2.0 |  |
| MES | 15 | h2 * | +0.016 | +0.004 .. +0.027 | +0.0040 | 0.0061 / 0.0058 / 0.014 | 0.0133 | 1 | 0.777 | 15/16 | +0.009 | +0.023 | False | +2.6 / +2.7 |  |
| MES | 15 | h4 | +0.015 | -0.002 .. +0.032 | +0.0026 | 0.079 / 0.081 / 0.12 | 0.121 |  |  | 11/16 | +0.010 | +0.020 |  | +1.7 / +1.8 | 0.026 |
| MES | 15 | h8 | +0.011 | -0.015 .. +0.037 | +0.0013 | 0.41 / 0.4 / 0.42 | 0.418 |  |  | 8/16 | -0.007 | +0.029 |  | +0.8 / +0.8 |  |
| MES | 15 | h16 | +0.014 | -0.028 .. +0.055 | +0.0011 | 0.53 / 0.51 / 0.49 | 0.501 |  |  | 9/16 | -0.004 | +0.031 |  | +0.7 / +0.6 |  |
| MES | 15 | eod | +0.103 | -0.047 .. +0.253 | +0.0033 | 0.18 / 0.17 / 0.052 | 0.0531 |  |  | 9/16 | +0.007 | +0.199 |  | +2.2 / +1.4 |  |
| MES | 60 | h1 | +0.012 | -0.004 .. +0.028 | +0.0049 | 0.14 / 0.13 / 0.13 | 0.134 |  |  | 10/16 | +0.007 | +0.017 |  | +1.5 / +1.5 |  |
| MES | 60 | h2 | +0.013 | -0.012 .. +0.037 | +0.0036 | 0.3 / 0.29 / 0.27 | 0.272 |  |  | 9/16 | -0.000 | +0.026 |  | +1.1 / +1.0 |  |
| MES | 60 | h4 | +0.011 | -0.024 .. +0.046 | +0.0022 | 0.54 / 0.53 / 0.51 | 0.516 |  |  | 8/16 | -0.008 | +0.030 |  | +0.6 / +0.6 | 0.047 |
| MES | 60 | h8 | +0.005 | -0.040 .. +0.050 | +0.0008 | 0.82 / 0.82 / 0.81 | 0.805 |  |  | 9/16 | -0.012 | +0.023 |  | +0.2 / +0.2 |  |
| MES | 60 | h16 | +0.040 | -0.020 .. +0.100 | +0.0045 | 0.19 / 0.18 / 0.17 | 0.174 |  |  | 12/16 | +0.027 | +0.053 |  | +1.3 / +1.3 |  |
| MES | 60 | eod * | +0.049 | -0.014 .. +0.111 | +0.0052 | 0.13 / 0.11 / 0.11 | 0.111 | 1 | 1 | 11/16 | +0.032 | +0.065 | False | +1.5 / +1.5 |  |
| MNQ | 5 | h1 | +0.001 | -0.004 .. +0.005 | +0.0003 | 0.7 / 0.7 / 0.74 | 0.743 |  |  | 10/16 | -0.002 | +0.004 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h2 | +0.004 | -0.003 .. +0.012 | +0.0010 | 0.24 / 0.23 / 0.29 | 0.286 |  |  | 9/16 | +0.003 | +0.006 |  | +1.3 / +1.2 |  |
| MNQ | 5 | h4 * | +0.013 | +0.001 .. +0.025 | +0.0019 | 0.028 / 0.028 / 0.044 | 0.0422 | 1 | 0.997 | 11/16 | +0.008 | +0.018 | False | +2.6 / +2.2 | 0.017 |
| MNQ | 5 | h8 | +0.017 | -0.002 .. +0.036 | +0.0016 | 0.086 / 0.084 / 0.077 | 0.0792 |  |  | 10/16 | +0.013 | +0.020 |  | +2.2 / +1.7 |  |
| MNQ | 5 | h16 | -0.000 | -0.029 .. +0.029 | -0.0000 | 1 / 1 / 0.97 | 0.971 |  |  | 11/16 | -0.005 | +0.005 |  | -0.0 / -0.0 |  |
| MNQ | 5 | eod | +0.030 | -0.208 .. +0.268 | +0.0005 | 0.8 / 0.8 / 0.73 | 0.735 |  |  | 8/16 | -0.131 | +0.190 |  | +0.5 / +0.2 |  |
| MNQ | 15 | h1 * | +0.008 | +0.000 .. +0.016 | +0.0027 | 0.047 / 0.048 / 0.12 | 0.117 | 1 | 0.999 | 10/16 | +0.006 | +0.010 | False | +1.9 / +2.0 |  |
| MNQ | 15 | h2 | +0.009 | -0.002 .. +0.021 | +0.0019 | 0.1 / 0.097 / 0.26 | 0.247 |  |  | 11/16 | +0.009 | +0.009 |  | +1.5 / +1.6 |  |
| MNQ | 15 | h4 | +0.016 | -0.002 .. +0.033 | +0.0018 | 0.082 / 0.08 / 0.25 | 0.249 |  |  | 11/16 | +0.010 | +0.021 |  | +1.6 / +1.7 | 0.028 |
| MNQ | 15 | h8 | +0.016 | -0.009 .. +0.042 | +0.0015 | 0.21 / 0.21 / 0.35 | 0.342 |  |  | 11/16 | +0.006 | +0.026 |  | +1.2 / +1.3 |  |
| MNQ | 15 | h16 | +0.018 | -0.029 .. +0.065 | +0.0013 | 0.45 / 0.45 / 0.41 | 0.413 |  |  | 8/16 | -0.001 | +0.037 |  | +0.9 / +0.8 |  |
| MNQ | 15 | eod | +0.130 | -0.062 .. +0.322 | +0.0033 | 0.19 / 0.17 / 0.044 | 0.044 |  |  | 8/16 | +0.083 | +0.177 |  | +2.5 / +1.3 |  |
| MNQ | 60 | h1 | -0.002 | -0.017 .. +0.013 | -0.0009 | 0.79 / 0.78 / 0.79 | 0.79 |  |  | 9/16 | -0.003 | -0.001 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h2 | -0.005 | -0.026 .. +0.016 | -0.0014 | 0.65 / 0.65 / 0.65 | 0.653 |  |  | 7/16 | -0.017 | +0.007 |  | -0.4 / -0.5 |  |
| MNQ | 60 | h4 | -0.011 | -0.041 .. +0.019 | -0.0022 | 0.49 / 0.48 / 0.49 | 0.493 |  |  | 10/16 | -0.017 | -0.004 |  | -0.6 / -0.7 | 0.044 |
| MNQ | 60 | h8 * | -0.018 | -0.057 .. +0.021 | -0.0028 | 0.36 / 0.35 / 0.37 | 0.375 | 1 | 1 | 10/16 | -0.026 | -0.011 | False | -0.8 / -0.9 |  |
| MNQ | 60 | h16 | -0.008 | -0.061 .. +0.044 | -0.0010 | 0.75 / 0.76 / 0.76 | 0.763 |  |  | 8/16 | -0.005 | -0.012 |  | -0.3 / -0.3 |  |
| MNQ | 60 | eod | -0.006 | -0.061 .. +0.049 | -0.0007 | 0.82 / 0.82 / 0.83 | 0.836 |  |  | 9/16 | -0.009 | -0.004 |  | -0.2 / -0.2 |  |
| MYM | 5 | h1 | +0.007 | +0.001 .. +0.014 | +0.0025 | 0.02 / 0.021 / 0.05 | 0.0495 |  |  | 7/8 | n/a | +0.007 |  | +2.3 / +2.3 |  |
| MYM | 5 | h2 | +0.011 | -0.001 .. +0.023 | +0.0022 | 0.064 / 0.056 / 0.1 | 0.0933 |  |  | 5/8 | n/a | +0.011 |  | +2.3 / +1.9 |  |
| MYM | 5 | h4 * | +0.027 | +0.006 .. +0.048 | +0.0034 | 0.013 / 0.012 / 0.011 | 0.0137 | 1 | 0.914 | 7/8 | n/a | +0.027 | False | +3.7 / +2.5 | 0.023 |
| MYM | 5 | h8 | +0.037 | -0.000 .. +0.074 | +0.0033 | 0.051 / 0.05 / 0.016 | 0.019 |  |  | 5/8 | n/a | +0.037 |  | +3.5 / +1.9 |  |
| MYM | 5 | h16 | +0.026 | -0.024 .. +0.076 | +0.0018 | 0.31 / 0.31 / 0.19 | 0.185 |  |  | 5/8 | n/a | +0.026 |  | +1.7 / +1.0 |  |
| MYM | 5 | eod | +0.196 | -0.092 .. +0.485 | +0.0031 | 0.18 / 0.17 / 0.039 | 0.0364 |  |  | 5/8 | n/a | +0.196 |  | +2.5 / +1.3 |  |
| MYM | 15 | h1 | +0.010 | -0.001 .. +0.020 | +0.0034 | 0.077 / 0.071 / 0.13 | 0.129 |  |  | 6/8 | n/a | +0.010 |  | +1.7 / +1.8 |  |
| MYM | 15 | h2 | +0.017 | -0.000 .. +0.034 | +0.0034 | 0.054 / 0.053 / 0.12 | 0.124 |  |  | 6/8 | n/a | +0.017 |  | +2.0 / +1.9 |  |
| MYM | 15 | h4 | +0.026 | -0.002 .. +0.054 | +0.0031 | 0.071 / 0.072 / 0.17 | 0.165 |  |  | 5/8 | n/a | +0.026 |  | +2.0 / +1.8 | 0.040 |
| MYM | 15 | h8 | +0.036 | -0.011 .. +0.083 | +0.0034 | 0.13 / 0.13 / 0.15 | 0.149 |  |  | 6/8 | n/a | +0.036 |  | +2.0 / +1.5 |  |
| MYM | 15 | h16 * | +0.094 | -0.006 .. +0.195 | +0.0062 | 0.066 / 0.065 / 0.0068 | 0.0105 | 1 | 0.999 | 6/8 | n/a | +0.094 | False | +3.5 / +1.8 |  |
| MYM | 15 | eod | +0.185 | -0.080 .. +0.450 | +0.0050 | 0.17 / 0.18 / 0.034 | 0.0332 |  |  | 6/8 | n/a | +0.185 |  | +2.7 / +1.4 |  |
| MYM | 60 | h1 | +0.005 | -0.015 .. +0.025 | +0.0020 | 0.65 / 0.65 / 0.67 | 0.658 |  |  | 4/8 | n/a | +0.005 |  | +0.4 / +0.5 |  |
| MYM | 60 | h2 | +0.008 | -0.022 .. +0.039 | +0.0025 | 0.59 / 0.59 / 0.59 | 0.573 |  |  | 5/8 | n/a | +0.008 |  | +0.5 / +0.5 |  |
| MYM | 60 | h4 | +0.033 | -0.010 .. +0.076 | +0.0070 | 0.13 / 0.13 / 0.13 | 0.124 |  |  | 5/8 | n/a | +0.033 |  | +1.4 / +1.5 | 0.063 |
| MYM | 60 | h8 | +0.014 | -0.047 .. +0.075 | +0.0022 | 0.65 / 0.64 / 0.64 | 0.631 |  |  | 3/8 | n/a | +0.014 |  | +0.5 / +0.5 |  |
| MYM | 60 | h16 | +0.057 | -0.021 .. +0.134 | +0.0067 | 0.15 / 0.15 / 0.15 | 0.151 |  |  | 6/8 | n/a | +0.057 |  | +1.4 / +1.4 |  |
| MYM | 60 | eod * | +0.062 | -0.018 .. +0.142 | +0.0070 | 0.13 / 0.13 / 0.14 | 0.139 | 1 | 1 | 6/8 | n/a | +0.062 | False | +1.4 / +1.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | -0.001 .. +0.006 | +0.5% | -0.006 | 0.15 |  | 11/16 |
| MES | 5 | h2 | +0.003 | -0.003 .. +0.008 | +0.4% | +0.000 | 0.34 |  | 10/16 |
| MES | 5 | h4 | +0.001 | -0.007 .. +0.009 | +0.1% | +0.001 | 0.82 |  | 8/16 |
| MES | 5 | h8 | -0.013 | -0.025 .. -0.002 | -0.9% | -0.016 | 0.053 |  | 11/16 |
| MES | 5 | h16 | -0.024 | -0.043 .. -0.005 | -1.1% | -0.047 | 0.012 |  | 11/16 |
| MES | 5 | eod * | -0.320 | -0.493 .. -0.146 | -3.2% | -0.660 | 0.0003 | 0.057 | 11/16 |
| MES | 15 | h1 * | +0.009 | +0.004 .. +0.015 | +1.8% | +0.003 | 0.0013 | 0.217 | 13/16 |
| MES | 15 | h2 | +0.003 | -0.005 .. +0.012 | +0.5% | -0.001 | 0.44 |  | 9/16 |
| MES | 15 | h4 | -0.008 | -0.021 .. +0.004 | -0.8% | -0.012 | 0.3 |  | 10/16 |
| MES | 15 | h8 | -0.010 | -0.029 .. +0.010 | -0.6% | -0.027 | 0.33 |  | 7/16 |
| MES | 15 | h16 | -0.030 | -0.059 .. -0.000 | -1.3% | -0.068 | 0.049 |  | 11/16 |
| MES | 15 | eod | -0.117 | -0.239 .. +0.006 | -2.1% | -0.247 | 0.062 |  | 12/16 |
| MES | 60 | h1 | +0.003 | -0.007 .. +0.014 | +0.7% | -0.005 | 0.53 |  | 10/16 |
| MES | 60 | h2 | -0.001 | -0.015 .. +0.014 | -0.1% | -0.010 | 0.94 |  | 5/16 |
| MES | 60 | h4 | -0.005 | -0.027 .. +0.017 | -0.4% | -0.011 | 0.9 |  | 8/16 |
| MES | 60 | h8 | +0.013 | -0.014 .. +0.040 | +0.8% | -0.014 | 0.37 |  | 9/16 |
| MES | 60 | h16 | -0.025 | -0.059 .. +0.009 | -1.2% | -0.054 | 0.17 |  | 9/16 |
| MES | 60 | eod * | -0.027 | -0.064 .. +0.009 | -1.3% | -0.061 | 0.15 | 1 | 9/16 |
| MNQ | 5 | h1 | -0.009 | -0.012 .. -0.006 | -1.7% | -0.021 | 0.046 |  | 13/16 |
| MNQ | 5 | h2 | -0.012 | -0.018 .. -0.006 | -1.6% | -0.024 | 0.048 |  | 14/16 |
| MNQ | 5 | h4 | -0.024 | -0.035 .. -0.014 | -2.2% | -0.041 | 0.0039 |  | 15/16 |
| MNQ | 5 | h8 * | -0.048 | -0.071 .. -0.025 | -3.0% | -0.077 | 3.4e-05 | 0.00748 | 16/16 |
| MNQ | 5 | h16 | -0.079 | -0.121 .. -0.036 | -3.3% | -0.145 | 0.00028 |  | 15/16 |
| MNQ | 5 | eod | -0.513 | -0.767 .. -0.260 | -4.1% | -1.165 | 7.3e-05 |  | 14/16 |
| MNQ | 15 | h1 | +0.000 | -0.006 .. +0.006 | +0.1% | -0.009 | 0.93 |  | 7/16 |
| MNQ | 15 | h2 | -0.012 | -0.025 .. +0.000 | -1.6% | -0.022 | 0.13 |  | 11/16 |
| MNQ | 15 | h4 | -0.027 | -0.054 .. -0.000 | -2.4% | -0.044 | 0.049 |  | 14/16 |
| MNQ | 15 | h8 | -0.047 | -0.090 .. -0.004 | -2.8% | -0.089 | 0.032 |  | 13/16 |
| MNQ | 15 | h16 * | -0.079 | -0.127 .. -0.030 | -3.1% | -0.177 | 0.0015 | 0.243 | 16/16 |
| MNQ | 15 | eod | -0.226 | -0.431 .. -0.022 | -3.6% | -0.430 | 0.03 |  | 13/16 |
| MNQ | 60 | h1 | -0.004 | -0.015 .. +0.006 | -0.8% | -0.017 | 0.39 |  | 10/16 |
| MNQ | 60 | h2 | -0.008 | -0.023 .. +0.007 | -1.0% | -0.020 | 0.31 |  | 7/16 |
| MNQ | 60 | h4 | -0.009 | -0.031 .. +0.012 | -0.8% | -0.015 | 0.4 |  | 12/16 |
| MNQ | 60 | h8 * | -0.020 | -0.048 .. +0.008 | -1.3% | -0.014 | 0.18 | 1 | 12/16 |
| MNQ | 60 | h16 | -0.002 | -0.038 .. +0.033 | -0.1% | -0.020 | 0.9 |  | 10/16 |
| MNQ | 60 | eod | -0.003 | -0.040 .. +0.034 | -0.1% | -0.018 | 0.88 |  | 9/16 |
| MYM | 5 | h1 * | -0.020 | -0.025 .. -0.015 | -3.7% | -0.036 | 5.2e-05 | 0.011 | 8/8 |
| MYM | 5 | h2 | -0.023 | -0.033 .. -0.014 | -3.1% | -0.040 | 0.003 |  | 8/8 |
| MYM | 5 | h4 | -0.030 | -0.049 .. -0.011 | -2.7% | -0.061 | 0.013 |  | 7/8 |
| MYM | 5 | h8 | -0.047 | -0.084 .. -0.010 | -3.0% | -0.090 | 0.014 |  | 7/8 |
| MYM | 5 | h16 | -0.068 | -0.122 .. -0.015 | -2.9% | -0.154 | 0.012 |  | 6/8 |
| MYM | 5 | eod | -0.514 | -0.784 .. -0.243 | -4.4% | -0.882 | 0.0002 |  | 8/8 |
| MYM | 15 | h1 | -0.006 | -0.013 .. +0.002 | -1.1% | -0.019 | 0.41 |  | 6/8 |
| MYM | 15 | h2 | -0.014 | -0.028 .. +0.001 | -1.8% | -0.029 | 0.18 |  | 5/8 |
| MYM | 15 | h4 | -0.040 | -0.070 .. -0.011 | -3.6% | -0.069 | 0.028 |  | 7/8 |
| MYM | 15 | h8 * | -0.058 | -0.105 .. -0.010 | -3.5% | -0.130 | 0.021 | 1 | 7/8 |
| MYM | 15 | h16 | -0.080 | -0.168 .. +0.009 | -3.2% | -0.187 | 0.084 |  | 7/8 |
| MYM | 15 | eod | -0.180 | -0.418 .. +0.058 | -3.0% | -0.327 | 0.15 |  | 7/8 |
| MYM | 60 | h1 * | -0.013 | -0.028 .. +0.001 | -2.5% | -0.023 | 0.087 | 1 | 6/8 |
| MYM | 60 | h2 | -0.014 | -0.035 .. +0.007 | -1.9% | -0.027 | 0.36 |  | 5/8 |
| MYM | 60 | h4 | +0.004 | -0.027 .. +0.035 | +0.4% | -0.023 | 0.79 |  | 5/8 |
| MYM | 60 | h8 | -0.025 | -0.063 .. +0.013 | -1.6% | -0.045 | 0.25 |  | 5/8 |
| MYM | 60 | h16 | -0.037 | -0.087 .. +0.013 | -1.7% | -0.082 | 0.37 |  | 5/8 |
| MYM | 60 | eod | -0.032 | -0.086 .. +0.022 | -1.4% | -0.077 | 0.55 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.18 pts | -0.15 .. +0.52 | 0.29 |
| MES | 15 | +0.50 pts | -0.03 .. +1.03 | 0.08 |
| MES | 60 | +0.54 pts | -0.50 .. +1.59 | 0.31 |
| MNQ | 5 | -0.10 pts | -0.38 .. +0.17 | 0.47 |
| MNQ | 15 | +0.31 pts | -0.14 .. +0.76 | 0.22 |
| MNQ | 60 | -0.05 pts | -0.91 .. +0.80 | 1 |
| MYM | 5 | +0.38 pts | -0.02 .. +0.78 | 0.075 |
| MYM | 15 | +0.26 pts | -0.35 .. +0.88 | 0.42 |
| MYM | 60 | +0.38 pts | -1.11 .. +1.86 | 0.62 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | short | 76818 | +0.002 | 0.254 | -0.03 | -3.53 | -3.46 | -3.57 | -3.52 |
| MES | 5 | h2 | event | long | 76818 | +0.005 | 0.254 | +0.10 | -3.40 | -3.48 | -3.36 | -3.42 |
| MES | 5 | h4 | event | long | 76818 | +0.013 | 0.254 | +0.18 | -3.32 | -3.46 | -3.23 | -3.35 |
| MES | 5 | h8 | event | long | 76818 | +0.029 | 0.254 | +0.37 | -3.13 | -3.33 | -3.01 | -3.21 |
| MES | 5 | h16 | event | long | 76818 | +0.044 | 0.254 | +0.59 | -2.91 | -3.17 | -2.75 | -3.10 |
| MES | 5 | eod | event | long | 76818 | +0.428 | 0.254 | +5.43 | +1.93 | +0.04 | +3.04 | +1.87 |
| MES | 15 | h1 | event | long | 31884 | +0.010 | 0.162 | +0.15 | -3.35 | -3.37 | -3.34 | -3.38 |
| MES | 15 | h2 | event | long | 31884 | +0.021 | 0.162 | +0.31 | -3.19 | -3.29 | -3.12 | -3.24 |
| MES | 15 | h4 | event | long | 31884 | +0.028 | 0.162 | +0.45 | -3.05 | -3.10 | -3.02 | -3.17 |
| MES | 15 | h8 | event | long | 31884 | +0.040 | 0.162 | +0.78 | -2.72 | -2.88 | -2.61 | -2.94 |
| MES | 15 | h16 | event | long | 31884 | +0.072 | 0.162 | +1.33 | -2.17 | -2.43 | -1.98 | -2.55 |
| MES | 15 | eod | event | long | 31884 | +0.304 | 0.162 | +5.22 | +1.72 | -0.16 | +3.06 | +1.17 |
| MES | 60 | h1 | event | long | 8841 | +0.019 | 0.088 | +0.76 | -2.74 | -3.20 | -2.32 | -2.90 |
| MES | 60 | h2 | event | long | 8841 | +0.029 | 0.088 | +1.46 | -2.04 | -3.17 | -1.02 | -2.43 |
| MES | 60 | h4 | event | long | 8841 | +0.043 | 0.088 | +2.24 | -1.26 | -2.94 | +0.27 | -2.03 |
| MES | 60 | h8 | event | long | 8841 | +0.070 | 0.088 | +3.18 | -0.32 | -2.21 | +1.39 | -1.98 |
| MES | 60 | h16 | event | long | 8841 | +0.141 | 0.088 | +5.85 | +2.35 | -0.83 | +5.24 | -0.34 |
| MES | 60 | eod | event | long | 8841 | +0.163 | 0.088 | +6.41 | +2.91 | -0.37 | +5.88 | -0.31 |
| MNQ | 5 | h1 | event | long | 116147 | +0.005 | 0.115 | +0.10 | -1.90 | -1.98 | -1.85 | -1.93 |
| MNQ | 5 | h2 | event | long | 116147 | +0.010 | 0.115 | +0.09 | -1.91 | -1.94 | -1.89 | -1.92 |
| MNQ | 5 | h4 | event | long | 116147 | +0.024 | 0.115 | +0.25 | -1.75 | -1.84 | -1.69 | -1.77 |
| MNQ | 5 | h8 | event | long | 116147 | +0.039 | 0.115 | +0.30 | -1.70 | -1.68 | -1.72 | -1.77 |
| MNQ | 5 | h16 | event | short | 116147 | -0.052 | 0.115 | -0.43 | -2.43 | -2.41 | -2.45 | -2.18 |
| MNQ | 5 | eod | event | long | 116147 | +0.674 | 0.115 | +6.78 | +4.78 | +1.29 | +7.19 | +4.47 |
| MNQ | 15 | h1 | event | long | 42508 | +0.014 | 0.069 | +0.27 | -1.73 | -1.88 | -1.61 | -1.84 |
| MNQ | 15 | h2 | event | long | 42508 | +0.019 | 0.069 | +0.40 | -1.60 | -1.78 | -1.46 | -1.75 |
| MNQ | 15 | h4 | event | long | 42508 | +0.036 | 0.069 | +0.72 | -1.28 | -1.60 | -1.04 | -1.56 |
| MNQ | 15 | h8 | event | long | 42508 | +0.058 | 0.069 | +1.29 | -0.71 | -1.40 | -0.16 | -1.26 |
| MNQ | 15 | h16 | event | long | 42508 | +0.091 | 0.069 | +2.08 | +0.08 | -0.99 | +0.92 | -0.52 |
| MNQ | 15 | eod | event | long | 42508 | +0.406 | 0.069 | +7.27 | +5.27 | +1.89 | +7.93 | +4.45 |
| MNQ | 60 | h1 | event | short | 10800 | -0.010 | 0.036 | -0.43 | -2.43 | -2.15 | -2.69 | -2.11 |
| MNQ | 60 | h2 | event | short | 10800 | -0.019 | 0.036 | -1.46 | -3.46 | -2.19 | -4.62 | -2.81 |
| MNQ | 60 | h4 | event | short | 10800 | -0.033 | 0.036 | -2.24 | -4.24 | -2.70 | -5.66 | -3.07 |
| MNQ | 60 | h8 | event | short | 10800 | -0.059 | 0.036 | -3.66 | -5.66 | -3.18 | -7.94 | -3.50 |
| MNQ | 60 | h16 | event | short | 10800 | -0.119 | 0.036 | -5.29 | -7.29 | -4.43 | -9.92 | -3.69 |
| MNQ | 60 | eod | event | short | 10800 | -0.143 | 0.036 | -6.08 | -8.08 | -4.93 | -10.97 | -3.61 |
| MYM | 5 | h1 | event | long | 61881 | +0.006 | 0.163 | +0.07 | -1.93 | +nan | -1.93 | -1.93 |
| MYM | 5 | h2 | event | long | 61881 | +0.007 | 0.163 | +0.07 | -1.93 | +nan | -1.93 | -1.91 |
| MYM | 5 | h4 | event | long | 61881 | +0.015 | 0.163 | +0.16 | -1.84 | +nan | -1.84 | -1.79 |
| MYM | 5 | h8 | event | long | 61881 | +0.019 | 0.163 | +0.20 | -1.80 | +nan | -1.80 | -1.73 |
| MYM | 5 | h16 | event | long | 61881 | +0.012 | 0.163 | +0.27 | -1.73 | +nan | -1.73 | -1.73 |
| MYM | 5 | eod | event | long | 61881 | +0.314 | 0.163 | +4.19 | +2.19 | +nan | +2.19 | +1.93 |
| MYM | 15 | h1 | event | long | 22291 | +0.009 | 0.094 | +0.21 | -1.79 | +nan | -1.79 | -1.79 |
| MYM | 15 | h2 | event | long | 22291 | +0.015 | 0.094 | +0.35 | -1.65 | +nan | -1.65 | -1.64 |
| MYM | 15 | h4 | event | long | 22291 | +0.020 | 0.094 | +0.43 | -1.57 | +nan | -1.57 | -1.49 |
| MYM | 15 | h8 | event | long | 22291 | +0.021 | 0.094 | +0.59 | -1.41 | +nan | -1.41 | -1.16 |
| MYM | 15 | h16 | event | long | 22291 | +0.047 | 0.094 | +1.21 | -0.79 | +nan | -0.79 | -0.08 |
| MYM | 15 | eod | event | long | 22291 | +0.164 | 0.094 | +4.62 | +2.62 | +nan | +2.62 | +3.77 |
| MYM | 60 | h1 | event | long | 5418 | +0.010 | 0.047 | +0.69 | -1.31 | +nan | -1.31 | -1.50 |
| MYM | 60 | h2 | event | long | 5418 | +0.017 | 0.047 | +1.49 | -0.51 | +nan | -0.51 | -0.82 |
| MYM | 60 | h4 | event | long | 5418 | +0.043 | 0.047 | +2.88 | +0.88 | +nan | +0.88 | +0.39 |
| MYM | 60 | h8 | event | long | 5418 | +0.040 | 0.047 | +2.85 | +0.85 | +nan | +0.85 | -0.17 |
| MYM | 60 | h16 | event | long | 5418 | +0.091 | 0.047 | +6.26 | +4.26 | +nan | +4.26 | +2.59 |
| MYM | 60 | eod | event | long | 5418 | +0.109 | 0.047 | +7.00 | +5.00 | +nan | +5.00 | +2.65 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.018 | -0.007 | -0.003 | +0.001 | -0.004 | +0.000 | -0.004 | +0.000 | +0.003 | +0.010 | +0.002 |
| MES | 15 | -0.021 | -0.008 | -0.002 | +0.004 | -0.009 | +0.000 | +0.008 | +0.014 | +0.012 | +0.007 | +0.006 |
| MES | 60 | +0.048 | -0.004 | +0.019 | +0.020 | -0.015 | +0.000 | +0.010 | +0.010 | +0.006 | +0.001 | +0.108 |
| MNQ | 5 | -0.007 | -0.002 | +0.000 | +0.006 | +0.000 | +0.000 | +0.001 | +0.003 | +0.010 | +0.010 | -0.009 |
| MNQ | 15 | -0.004 | -0.002 | +0.007 | +0.010 | -0.004 | +0.000 | +0.008 | +0.009 | +0.014 | +0.012 | +0.004 |
| MNQ | 60 | +0.116 | +0.036 | +0.034 | +0.032 | -0.007 | +0.000 | -0.001 | -0.004 | -0.008 | -0.026 | +0.018 |
| MYM | 5 | -0.015 | -0.009 | -0.009 | -0.004 | -0.006 | +0.000 | +0.008 | +0.011 | +0.022 | +0.030 | +0.019 |
| MYM | 15 | -0.029 | -0.015 | -0.002 | +0.005 | -0.013 | +0.000 | +0.011 | +0.015 | +0.024 | +0.028 | +0.079 |
| MYM | 60 | -0.017 | -0.013 | +0.016 | +0.025 | -0.020 | +0.000 | +0.003 | +0.007 | +0.038 | +0.008 | +0.056 |

## Calibration

- MES 5-min: 1036271 bars, 76818 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 31884 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 8841 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 116147 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 42508 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 10800 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 61881 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 22291 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 5418 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33926 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
