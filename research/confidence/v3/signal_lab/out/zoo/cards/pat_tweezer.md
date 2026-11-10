# Impact card: pat_tweezer

candle pattern tweezer in its textbook direction: lows within 0.05 x avgR10, bar1 down, bar2 up, close1 < EMA10 -> bullish bottom; highs mirror -> bearish top [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (10 min), p=0.12; we would catch an effect of 0.014 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.016 R20, CONFIRMED, q=1.71e-15, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.27 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.246 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.012 R20 over the next 2 bars (30 min), p=0.37; we would catch an effect of 0.027 R20 or more 80% of the time).
- MES 15-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.020 R20, CONFIRMED, q=1.8e-05, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.14 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.127 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.044 R20 over the next 4 bars (4 h), p=0.35; we would catch an effect of 0.059 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.03).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.52 at recent bar sizes, 90% range up to $4.70); about 4.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.157 R20 over the rest of the session (to 16:45), p=0.37; we would catch an effect of 0.018 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.018 R20, CONFIRMED, q=1.69e-09, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.31 at recent bar sizes, 90% range up to $0.61); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.033 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.020 R20, CONFIRMED, q=2.18e-05, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.57 at recent bar sizes, 90% range up to $1.49); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.053 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.060 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.24).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.94 at recent bar sizes, 90% range up to $7.15); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.027 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.027 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.033).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.63 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.160 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.098 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.033).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.17 at recent bar sizes, 90% range up to $1.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.024 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.082 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.064).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.08 at recent bar sizes, 90% range up to $5.30); about 30.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.006 | +0.001 .. +0.011 | +0.0024 | 0.021 / 0.015 / 0.017 | 0.0148 |  |  | 10/16 | +0.005 | +0.007 |  | +2.5 / +2.3 |  |
| MES | 5 | h2 * | +0.008 | +0.001 .. +0.014 | +0.0022 | 0.019 / 0.017 / 0.023 | 0.0198 | 1 | 0.977 | 12/16 | +0.010 | +0.006 | False | +2.3 / +2.3 |  |
| MES | 5 | h4 | +0.007 | -0.001 .. +0.015 | +0.0014 | 0.083 / 0.1 / 0.14 | 0.147 |  |  | 9/16 | +0.006 | +0.009 |  | +1.5 / +1.7 | 0.014 |
| MES | 5 | h8 | +0.009 | -0.003 .. +0.021 | +0.0012 | 0.15 / 0.16 / 0.21 | 0.207 |  |  | 10/16 | +0.010 | +0.008 |  | +1.3 / +1.4 |  |
| MES | 5 | h16 | +0.005 | -0.014 .. +0.024 | +0.0005 | 0.6 / 0.59 / 0.61 | 0.613 |  |  | 9/16 | +0.005 | +0.005 |  | +0.5 / +0.5 |  |
| MES | 5 | eod | +0.059 | -0.040 .. +0.159 | +0.0011 | 0.24 / 0.25 / 0.26 | 0.266 |  |  | 9/16 | -0.004 | +0.122 |  | +1.1 / +1.2 |  |
| MES | 15 | h1 | +0.003 | -0.007 .. +0.012 | +0.0010 | 0.57 / 0.56 / 0.58 | 0.578 |  |  | 9/16 | +0.001 | +0.005 |  | +0.6 / +0.6 |  |
| MES | 15 | h2 * | +0.012 | +0.000 .. +0.024 | +0.0029 | 0.045 / 0.051 / 0.087 | 0.0828 | 1 | 1 | 11/16 | +0.002 | +0.022 | False | +1.9 / +2.0 |  |
| MES | 15 | h4 | +0.013 | -0.004 .. +0.030 | +0.0021 | 0.13 / 0.13 / 0.2 | 0.203 |  |  | 12/16 | -0.004 | +0.030 |  | +1.4 / +1.5 | 0.027 |
| MES | 15 | h8 | +0.018 | -0.010 .. +0.046 | +0.0020 | 0.21 / 0.2 / 0.23 | 0.228 |  |  | 9/16 | +0.013 | +0.023 |  | +1.3 / +1.3 |  |
| MES | 15 | h16 | +0.017 | -0.022 .. +0.056 | +0.0014 | 0.39 / 0.39 / 0.44 | 0.443 |  |  | 9/16 | +0.006 | +0.028 |  | +0.8 / +0.9 |  |
| MES | 15 | eod | -0.030 | -0.136 .. +0.077 | -0.0009 | 0.59 / 0.58 / 0.64 | 0.642 |  |  | 9/16 | -0.167 | +0.107 |  | -0.5 / -0.5 |  |
| MES | 60 | h1 | -0.003 | -0.023 .. +0.016 | -0.0011 | 0.73 / 0.73 / 0.75 | 0.75 |  |  | 9/16 | -0.015 | +0.008 |  | -0.3 / -0.3 |  |
| MES | 60 | h2 | -0.020 | -0.051 .. +0.010 | -0.0044 | 0.19 / 0.18 / 0.18 | 0.178 |  |  | 9/16 | -0.030 | -0.010 |  | -1.4 / -1.3 |  |
| MES | 60 | h4 * | -0.044 | -0.085 .. -0.003 | -0.0069 | 0.035 / 0.027 / 0.037 | 0.0357 | 1 | 0.997 | 12/16 | -0.066 | -0.022 | False | -2.2 / -2.1 | 0.059 |
| MES | 60 | h8 | -0.035 | -0.092 .. +0.022 | -0.0038 | 0.23 / 0.22 / 0.26 | 0.264 |  |  | 10/16 | -0.035 | -0.035 |  | -1.2 / -1.2 |  |
| MES | 60 | h16 | -0.005 | -0.088 .. +0.078 | -0.0003 | 0.91 / 0.9 / 0.91 | 0.913 |  |  | 9/16 | +0.001 | -0.010 |  | -0.1 / -0.1 |  |
| MES | 60 | eod | +0.007 | -0.081 .. +0.096 | +0.0008 | 0.87 / 0.86 / 0.87 | 0.879 |  |  | 8/16 | +0.013 | +0.002 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h1 | +0.002 | -0.004 .. +0.007 | +0.0005 | 0.5 / 0.52 / 0.6 | 0.593 |  |  | 9/16 | +0.002 | +0.001 |  | +0.6 / +0.7 |  |
| MNQ | 5 | h2 | -0.001 | -0.009 .. +0.006 | -0.0002 | 0.72 / 0.73 / 0.8 | 0.785 |  |  | 9/16 | +0.000 | -0.003 |  | -0.3 / -0.4 |  |
| MNQ | 5 | h4 | -0.005 | -0.018 .. +0.007 | -0.0006 | 0.4 / 0.4 / 0.55 | 0.529 |  |  | 9/16 | -0.005 | -0.006 |  | -0.8 / -0.8 | 0.018 |
| MNQ | 5 | h8 | -0.007 | -0.025 .. +0.011 | -0.0006 | 0.43 / 0.43 / 0.58 | 0.564 |  |  | 10/16 | -0.008 | -0.006 |  | -0.8 / -0.8 |  |
| MNQ | 5 | h16 | +0.001 | -0.025 .. +0.027 | +0.0001 | 0.95 / 0.95 / 0.97 | 0.965 |  |  | 6/16 | -0.004 | +0.006 |  | +0.1 / +0.1 |  |
| MNQ | 5 | eod * | +0.157 | -0.007 .. +0.322 | +0.0018 | 0.061 / 0.055 / 0.083 | 0.0808 | 1 | 1 | 12/16 | +0.199 | +0.116 | False | +1.9 / +1.9 |  |
| MNQ | 15 | h1 | -0.007 | -0.017 .. +0.004 | -0.0016 | 0.23 / 0.23 / 0.34 | 0.278 |  |  | 8/16 | +0.000 | -0.013 |  | -1.3 / -1.2 |  |
| MNQ | 15 | h2 | -0.007 | -0.022 .. +0.008 | -0.0011 | 0.37 / 0.36 / 0.54 | 0.474 |  |  | 8/16 | -0.007 | -0.007 |  | -0.9 / -0.9 |  |
| MNQ | 15 | h4 | -0.009 | -0.030 .. +0.013 | -0.0008 | 0.43 / 0.43 / 0.65 | 0.583 |  |  | 9/16 | -0.005 | -0.013 |  | -0.8 / -0.8 | 0.039 |
| MNQ | 15 | h8 | -0.005 | -0.037 .. +0.028 | -0.0003 | 0.78 / 0.78 / 0.86 | 0.853 |  |  | 6/16 | -0.004 | -0.005 |  | -0.3 / -0.3 |  |
| MNQ | 15 | h16 * | -0.033 | -0.085 .. +0.018 | -0.0018 | 0.21 / 0.2 / 0.29 | 0.293 | 1 | 1 | 10/16 | -0.005 | -0.062 | False | -1.3 / -1.3 |  |
| MNQ | 15 | eod | -0.069 | -0.206 .. +0.067 | -0.0013 | 0.32 / 0.33 / 0.46 | 0.453 |  |  | 10/16 | -0.139 | -0.000 |  | -1.0 / -1.0 |  |
| MNQ | 60 | h1 | -0.006 | -0.027 .. +0.014 | -0.0018 | 0.54 / 0.55 / 0.55 | 0.542 |  |  | 9/16 | +0.014 | -0.027 |  | -0.6 / -0.6 |  |
| MNQ | 60 | h2 | -0.003 | -0.032 .. +0.026 | -0.0004 | 0.85 / 0.85 / 0.86 | 0.865 |  |  | 9/16 | +0.029 | -0.035 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h4 | -0.019 | -0.062 .. +0.025 | -0.0026 | 0.4 / 0.39 / 0.39 | 0.389 |  |  | 11/16 | +0.006 | -0.044 |  | -0.9 / -0.8 | 0.060 |
| MNQ | 60 | h8 | -0.026 | -0.086 .. +0.034 | -0.0027 | 0.39 / 0.38 / 0.4 | 0.412 |  |  | 11/16 | -0.045 | -0.007 |  | -0.9 / -0.9 |  |
| MNQ | 60 | h16 * | -0.053 | -0.133 .. +0.027 | -0.0042 | 0.2 / 0.2 / 0.25 | 0.249 | 1 | 1 | 10/16 | -0.071 | -0.035 | False | -1.2 / -1.3 |  |
| MNQ | 60 | eod | -0.039 | -0.122 .. +0.045 | -0.0029 | 0.37 / 0.38 / 0.42 | 0.431 |  |  | 11/16 | -0.049 | -0.028 |  | -0.8 / -0.9 |  |
| MYM | 5 | h1 | +0.004 | -0.005 .. +0.014 | +0.0011 | 0.34 / 0.34 / 0.41 | 0.39 |  |  | 6/8 | n/a | +0.004 |  | +1.0 / +1.0 |  |
| MYM | 5 | h2 | +0.008 | -0.005 .. +0.021 | +0.0012 | 0.21 / 0.21 / 0.41 | 0.355 |  |  | 5/8 | n/a | +0.008 |  | +1.2 / +1.2 |  |
| MYM | 5 | h4 | +0.017 | -0.002 .. +0.036 | +0.0016 | 0.072 / 0.073 / 0.26 | 0.225 |  |  | 6/8 | n/a | +0.017 |  | +1.8 / +1.8 | 0.027 |
| MYM | 5 | h8 * | +0.027 | -0.001 .. +0.055 | +0.0018 | 0.054 / 0.046 / 0.22 | 0.2 | 1 | 1 | 5/8 | n/a | +0.027 | False | +2.0 / +1.9 |  |
| MYM | 5 | h16 | +0.021 | -0.018 .. +0.059 | +0.0011 | 0.29 / 0.31 / 0.46 | 0.44 |  |  | 5/8 | n/a | +0.021 |  | +1.0 / +1.1 |  |
| MYM | 5 | eod | +0.105 | -0.107 .. +0.317 | +0.0012 | 0.33 / 0.34 / 0.41 | 0.423 |  |  | 6/8 | n/a | +0.105 |  | +0.9 / +1.0 |  |
| MYM | 15 | h1 | -0.008 | -0.023 .. +0.007 | -0.0020 | 0.29 / 0.3 / 0.39 | 0.363 |  |  | 5/8 | n/a | -0.008 |  | -1.0 / -1.1 |  |
| MYM | 15 | h2 | -0.006 | -0.027 .. +0.015 | -0.0009 | 0.57 / 0.58 / 0.71 | 0.657 |  |  | 4/8 | n/a | -0.006 |  | -0.6 / -0.6 |  |
| MYM | 15 | h4 | +0.010 | -0.020 .. +0.039 | +0.0008 | 0.52 / 0.55 / 0.73 | 0.649 |  |  | 5/8 | n/a | +0.010 |  | +0.6 / +0.6 | 0.046 |
| MYM | 15 | h8 | +0.012 | -0.031 .. +0.054 | +0.0007 | 0.6 / 0.61 / 0.77 | 0.727 |  |  | 5/8 | n/a | +0.012 |  | +0.5 / +0.5 |  |
| MYM | 15 | h16 | -0.013 | -0.081 .. +0.054 | -0.0006 | 0.7 / 0.7 / 0.8 | 0.792 |  |  | 5/8 | n/a | -0.013 |  | -0.4 / -0.4 |  |
| MYM | 15 | eod * | -0.098 | -0.258 .. +0.061 | -0.0018 | 0.23 / 0.24 / 0.44 | 0.432 | 1 | 1 | 6/8 | n/a | -0.098 | False | -1.1 / -1.2 |  |
| MYM | 60 | h1 | -0.016 | -0.043 .. +0.011 | -0.0049 | 0.26 / 0.25 / 0.28 | 0.283 |  |  | 6/8 | n/a | -0.016 |  | -1.1 / -1.1 |  |
| MYM | 60 | h2 * | -0.024 | -0.062 .. +0.013 | -0.0053 | 0.21 / 0.21 / 0.24 | 0.242 | 1 | 1 | 6/8 | n/a | -0.024 | False | -1.2 / -1.3 |  |
| MYM | 60 | h4 | -0.022 | -0.075 .. +0.032 | -0.0033 | 0.43 / 0.43 / 0.47 | 0.471 |  |  | 3/8 | n/a | -0.022 |  | -0.8 / -0.8 | 0.082 |
| MYM | 60 | h8 | +0.001 | -0.077 .. +0.078 | +0.0001 | 0.98 / 0.98 / 0.99 | 0.985 |  |  | 4/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 60 | h16 | -0.010 | -0.118 .. +0.097 | -0.0009 | 0.85 / 0.85 / 0.86 | 0.853 |  |  | 6/8 | n/a | -0.010 |  | -0.2 / -0.2 |  |
| MYM | 60 | eod | -0.017 | -0.127 .. +0.093 | -0.0014 | 0.76 / 0.77 / 0.79 | 0.786 |  |  | 4/8 | n/a | -0.017 |  | -0.3 / -0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.016 | -0.020 .. -0.013 | -3.3% | -0.038 | 3.5e-18 | 1.71e-15 | 16/16 |
| MES | 5 | h2 | -0.017 | -0.021 .. -0.012 | -2.3% | -0.041 | 3.3e-09 |  | 15/16 |
| MES | 5 | h4 | -0.019 | -0.026 .. -0.011 | -1.9% | -0.044 | 1.9e-06 |  | 14/16 |
| MES | 5 | h8 | -0.020 | -0.031 .. -0.008 | -1.4% | -0.047 | 0.0021 |  | 14/16 |
| MES | 5 | h16 | -0.020 | -0.038 .. -0.003 | -1.0% | -0.041 | 0.036 |  | 12/16 |
| MES | 5 | eod | +0.106 | -0.040 .. +0.252 | +1.1% | +0.271 | 0.15 |  | 12/16 |
| MES | 15 | h1 * | -0.020 | -0.026 .. -0.014 | -3.9% | -0.041 | 6.6e-08 | 1.8e-05 | 15/16 |
| MES | 15 | h2 | -0.019 | -0.028 .. -0.009 | -2.6% | -0.050 | 0.0015 |  | 14/16 |
| MES | 15 | h4 | -0.024 | -0.039 .. -0.009 | -2.3% | -0.053 | 0.015 |  | 13/16 |
| MES | 15 | h8 | -0.022 | -0.045 .. +0.001 | -1.5% | -0.050 | 0.17 |  | 13/16 |
| MES | 15 | h16 | -0.030 | -0.065 .. +0.005 | -1.3% | -0.037 | 0.18 |  | 12/16 |
| MES | 15 | eod | +0.027 | -0.109 .. +0.162 | +0.5% | +0.038 | 0.7 |  | 10/16 |
| MES | 60 | h1 * | -0.022 | -0.037 .. -0.007 | -4.2% | -0.048 | 0.005 | 0.73 | 12/16 |
| MES | 60 | h2 | -0.029 | -0.050 .. -0.009 | -4.0% | -0.058 | 0.0098 |  | 15/16 |
| MES | 60 | h4 | -0.042 | -0.070 .. -0.013 | -3.9% | -0.069 | 0.018 |  | 13/16 |
| MES | 60 | h8 | -0.059 | -0.096 .. -0.023 | -3.9% | -0.096 | 0.012 |  | 13/16 |
| MES | 60 | h16 | -0.066 | -0.121 .. -0.012 | -3.2% | -0.097 | 0.041 |  | 11/16 |
| MES | 60 | eod | -0.062 | -0.120 .. -0.004 | -2.9% | -0.100 | 0.05 |  | 9/16 |
| MNQ | 5 | h1 * | -0.018 | -0.022 .. -0.013 | -3.3% | -0.045 | 4.7e-12 | 1.69e-09 | 16/16 |
| MNQ | 5 | h2 | -0.017 | -0.024 .. -0.010 | -2.2% | -0.044 | 0.00022 |  | 15/16 |
| MNQ | 5 | h4 | -0.017 | -0.030 .. -0.004 | -1.5% | -0.045 | 0.021 |  | 14/16 |
| MNQ | 5 | h8 | -0.020 | -0.045 .. +0.004 | -1.3% | -0.045 | 0.1 |  | 10/16 |
| MNQ | 5 | h16 | +0.003 | -0.041 .. +0.048 | +0.1% | -0.015 | 0.88 |  | 9/16 |
| MNQ | 5 | eod | +0.025 | -0.212 .. +0.261 | +0.2% | +0.321 | 0.95 |  | 9/16 |
| MNQ | 15 | h1 * | -0.020 | -0.027 .. -0.013 | -3.8% | -0.044 | 8e-08 | 2.18e-05 | 16/16 |
| MNQ | 15 | h2 | -0.015 | -0.029 .. -0.001 | -1.9% | -0.048 | 0.13 |  | 9/16 |
| MNQ | 15 | h4 | -0.017 | -0.044 .. +0.011 | -1.5% | -0.047 | 0.32 |  | 10/16 |
| MNQ | 15 | h8 | -0.021 | -0.065 .. +0.023 | -1.3% | -0.057 | 0.39 |  | 6/16 |
| MNQ | 15 | h16 | -0.035 | -0.091 .. +0.021 | -1.4% | -0.074 | 0.33 |  | 8/16 |
| MNQ | 15 | eod | -0.002 | -0.209 .. +0.206 | -0.0% | +0.028 | 0.99 |  | 8/16 |
| MNQ | 60 | h1 | -0.008 | -0.023 .. +0.008 | -1.5% | -0.035 | 0.59 |  | 8/16 |
| MNQ | 60 | h2 | -0.019 | -0.039 .. +0.002 | -2.4% | -0.054 | 0.24 |  | 12/16 |
| MNQ | 60 | h4 | -0.031 | -0.060 .. -0.003 | -2.8% | -0.065 | 0.062 |  | 12/16 |
| MNQ | 60 | h8 * | -0.049 | -0.092 .. -0.007 | -3.1% | -0.109 | 0.04 | 1 | 11/16 |
| MNQ | 60 | h16 | -0.051 | -0.109 .. +0.007 | -2.3% | -0.096 | 0.11 |  | 12/16 |
| MNQ | 60 | eod | -0.062 | -0.124 .. -0.001 | -2.7% | -0.103 | 0.055 |  | 11/16 |
| MYM | 5 | h1 * | -0.012 | -0.020 .. -0.005 | -2.3% | -0.033 | 0.0054 | 0.783 | 7/8 |
| MYM | 5 | h2 | -0.014 | -0.027 .. -0.001 | -1.9% | -0.039 | 0.082 |  | 6/8 |
| MYM | 5 | h4 | -0.011 | -0.034 .. +0.011 | -1.0% | -0.041 | 0.35 |  | 3/8 |
| MYM | 5 | h8 | -0.019 | -0.057 .. +0.019 | -1.2% | -0.055 | 0.41 |  | 3/8 |
| MYM | 5 | h16 | -0.027 | -0.083 .. +0.029 | -1.1% | -0.062 | 0.35 |  | 4/8 |
| MYM | 5 | eod | +0.134 | -0.143 .. +0.412 | +1.1% | +0.240 | 0.34 |  | 6/8 |
| MYM | 15 | h1 * | -0.019 | -0.030 .. -0.007 | -3.6% | -0.035 | 0.0055 | 0.797 | 8/8 |
| MYM | 15 | h2 | -0.029 | -0.047 .. -0.011 | -3.8% | -0.048 | 0.069 |  | 7/8 |
| MYM | 15 | h4 | -0.016 | -0.052 .. +0.019 | -1.5% | -0.038 | 0.49 |  | 4/8 |
| MYM | 15 | h8 | -0.049 | -0.103 .. +0.005 | -3.0% | -0.082 | 0.12 |  | 5/8 |
| MYM | 15 | h16 | -0.027 | -0.121 .. +0.068 | -1.1% | -0.068 | 0.58 |  | 6/8 |
| MYM | 15 | eod | -0.043 | -0.290 .. +0.205 | -0.7% | -0.151 | 0.74 |  | 3/8 |
| MYM | 60 | h1 | -0.023 | -0.043 .. -0.003 | -4.4% | -0.052 | 0.086 |  | 6/8 |
| MYM | 60 | h2 | -0.031 | -0.058 .. -0.004 | -4.1% | -0.077 | 0.11 |  | 5/8 |
| MYM | 60 | h4 * | -0.061 | -0.094 .. -0.029 | -5.7% | -0.102 | 0.011 | 1 | 7/8 |
| MYM | 60 | h8 | -0.061 | -0.112 .. -0.011 | -4.0% | -0.127 | 0.077 |  | 7/8 |
| MYM | 60 | h16 | -0.093 | -0.169 .. -0.016 | -4.4% | -0.112 | 0.028 |  | 6/8 |
| MYM | 60 | eod | -0.102 | -0.181 .. -0.024 | -4.6% | -0.116 | 0.015 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.67 pts | +0.34 .. +0.99 | 6.4e-05 |
| MES | 15 | +0.45 pts | -0.14 .. +1.05 | 0.13 |
| MES | 60 | -0.52 pts | -1.94 .. +0.90 | 0.52 |
| MNQ | 5 | +0.59 pts | +0.20 .. +0.99 | 0.0034 |
| MNQ | 15 | -0.38 pts | -1.04 .. +0.27 | 0.3 |
| MNQ | 60 | -0.43 pts | -1.70 .. +0.84 | 0.53 |
| MYM | 5 | +0.92 pts | +0.34 .. +1.50 | 0.0029 |
| MYM | 15 | -0.10 pts | -1.09 .. +0.89 | 0.85 |
| MYM | 60 | -1.50 pts | -3.45 .. +0.46 | 0.14 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 85829 | -0.006 | 0.392 | -0.02 | -3.52 | -3.53 | -3.50 | -3.42 |
| MES | 5 | h2 | event | with signal | 85829 | -0.009 | 0.392 | -0.07 | -3.57 | -3.56 | -3.59 | -3.42 |
| MES | 5 | h4 | event | with signal | 85829 | -0.010 | 0.392 | -0.07 | -3.57 | -3.57 | -3.56 | -3.41 |
| MES | 5 | h8 | event | with signal | 85829 | -0.008 | 0.392 | -0.00 | -3.50 | -3.59 | -3.39 | -3.36 |
| MES | 5 | h16 | event | with signal | 85829 | -0.014 | 0.392 | +0.03 | -3.47 | -3.64 | -3.23 | -3.30 |
| MES | 5 | eod | event | with signal | 85829 | -0.030 | 0.392 | +0.38 | -3.12 | -3.86 | -2.10 | -2.29 |
| MES | 15 | h1 | event | with signal | 23830 | -0.006 | 0.208 | -0.08 | -3.58 | -3.54 | -3.64 | -3.45 |
| MES | 15 | h2 | event | with signal | 23830 | +0.002 | 0.208 | +0.06 | -3.44 | -3.53 | -3.32 | -3.28 |
| MES | 15 | h4 | event | with signal | 23830 | +0.001 | 0.208 | +0.08 | -3.42 | -3.61 | -3.19 | -3.24 |
| MES | 15 | h8 | event | with signal | 23830 | +0.001 | 0.208 | -0.08 | -3.58 | -3.53 | -3.65 | -3.32 |
| MES | 15 | h16 | event | with signal | 23830 | -0.013 | 0.208 | -0.07 | -3.57 | -3.73 | -3.36 | -3.11 |
| MES | 15 | eod | event | against signal | 23830 | +0.088 | 0.208 | -0.02 | -3.52 | -1.98 | -5.51 | -4.40 |
| MES | 60 | h1 | event | against signal | 4630 | +0.005 | 0.091 | +0.01 | -3.49 | -3.41 | -3.57 | -3.52 |
| MES | 60 | h2 | event | against signal | 4630 | +0.025 | 0.091 | +0.36 | -3.14 | -3.25 | -3.04 | -3.29 |
| MES | 60 | h4 | event | against signal | 4630 | +0.055 | 0.091 | +1.73 | -1.77 | -2.45 | -1.13 | -2.09 |
| MES | 60 | h8 | event | against signal | 4630 | +0.054 | 0.091 | +2.30 | -1.20 | -2.75 | +0.26 | -1.81 |
| MES | 60 | h16 | event | against signal | 4630 | +0.025 | 0.091 | +1.64 | -1.86 | -3.57 | -0.22 | -2.40 |
| MES | 60 | eod | event | with signal | 4630 | -0.017 | 0.091 | -1.86 | -5.36 | -3.33 | -7.30 | -4.65 |
| MNQ | 5 | h1 | event | with signal | 60231 | -0.004 | 0.131 | -0.05 | -2.05 | -2.01 | -2.09 | -1.97 |
| MNQ | 5 | h2 | event | against signal | 60231 | +0.011 | 0.131 | +0.13 | -1.87 | -1.95 | -1.78 | -2.02 |
| MNQ | 5 | h4 | event | against signal | 60231 | +0.014 | 0.131 | +0.10 | -1.90 | -1.94 | -1.85 | -2.02 |
| MNQ | 5 | h8 | event | against signal | 60231 | +0.011 | 0.131 | -0.02 | -2.02 | -2.00 | -2.05 | -2.05 |
| MNQ | 5 | h16 | event | with signal | 60231 | -0.006 | 0.131 | +0.02 | -1.98 | -2.06 | -1.89 | -1.92 |
| MNQ | 5 | eod | event | with signal | 60231 | +0.009 | 0.131 | -0.18 | -2.18 | -1.88 | -2.52 | -0.26 |
| MNQ | 15 | h1 | event | against signal | 19536 | +0.010 | 0.071 | +0.28 | -1.72 | -1.94 | -1.50 | -1.81 |
| MNQ | 15 | h2 | event | against signal | 19536 | +0.010 | 0.071 | +0.22 | -1.78 | -1.88 | -1.69 | -1.82 |
| MNQ | 15 | h4 | event | against signal | 19536 | +0.011 | 0.071 | +0.40 | -1.60 | -1.79 | -1.40 | -1.60 |
| MNQ | 15 | h8 | event | against signal | 19536 | +0.007 | 0.071 | +0.48 | -1.52 | -1.48 | -1.55 | -1.50 |
| MNQ | 15 | h16 | event | against signal | 19536 | +0.055 | 0.071 | +2.22 | +0.22 | -1.22 | +1.62 | -0.16 |
| MNQ | 15 | eod | event | against signal | 19536 | +0.138 | 0.071 | +0.50 | -1.50 | -0.51 | -2.46 | -2.41 |
| MNQ | 60 | h1 | event | against signal | 4667 | +0.008 | 0.037 | +0.89 | -1.11 | -2.21 | +0.06 | -1.18 |
| MNQ | 60 | h2 | event | against signal | 4667 | +0.009 | 0.037 | +1.34 | -0.66 | -2.47 | +1.25 | -0.93 |
| MNQ | 60 | h4 | event | against signal | 4667 | +0.031 | 0.037 | +2.57 | +0.57 | -1.76 | +3.02 | +0.05 |
| MNQ | 60 | h8 | event | against signal | 4667 | +0.043 | 0.037 | +1.37 | -0.63 | -0.90 | -0.35 | -1.29 |
| MNQ | 60 | h16 | event | against signal | 4667 | +0.070 | 0.037 | +2.56 | +0.56 | -0.78 | +1.97 | +0.08 |
| MNQ | 60 | eod | event | against signal | 4667 | +0.063 | 0.037 | +2.45 | +0.45 | -0.89 | +1.86 | -0.38 |
| MYM | 5 | h1 | event | with signal | 26918 | -0.003 | 0.160 | -0.05 | -2.05 | +nan | -2.05 | -1.95 |
| MYM | 5 | h2 | event | with signal | 26918 | -0.004 | 0.160 | -0.06 | -2.06 | +nan | -2.06 | -1.91 |
| MYM | 5 | h4 | event | with signal | 26918 | +0.001 | 0.160 | +0.00 | -2.00 | +nan | -2.00 | -1.78 |
| MYM | 5 | h8 | event | with signal | 26918 | +0.006 | 0.160 | +0.02 | -1.98 | +nan | -1.98 | -1.69 |
| MYM | 5 | h16 | event | with signal | 26918 | -0.011 | 0.160 | +0.02 | -1.98 | +nan | -1.98 | -1.56 |
| MYM | 5 | eod | event | with signal | 26918 | +0.006 | 0.160 | +0.27 | -1.73 | +nan | -1.73 | -0.60 |
| MYM | 15 | h1 | event | against signal | 9324 | +0.014 | 0.090 | +0.11 | -1.89 | +nan | -1.89 | -2.02 |
| MYM | 15 | h2 | event | against signal | 9324 | +0.013 | 0.090 | +0.06 | -1.94 | +nan | -1.94 | -2.10 |
| MYM | 15 | h4 | event | with signal | 9324 | +0.003 | 0.090 | +0.43 | -1.57 | +nan | -1.57 | -1.44 |
| MYM | 15 | h8 | event | with signal | 9324 | +0.000 | 0.090 | +0.26 | -1.74 | +nan | -1.74 | -1.49 |
| MYM | 15 | h16 | event | against signal | 9324 | +0.030 | 0.090 | +0.29 | -1.71 | +nan | -1.71 | -2.05 |
| MYM | 15 | eod | event | against signal | 9324 | +0.147 | 0.090 | +2.44 | +0.44 | +nan | +0.44 | -0.34 |
| MYM | 60 | h1 | event | against signal | 2379 | +0.017 | 0.045 | +0.26 | -1.74 | +nan | -1.74 | -1.73 |
| MYM | 60 | h2 | event | against signal | 2379 | +0.033 | 0.045 | +0.71 | -1.29 | +nan | -1.29 | -1.61 |
| MYM | 60 | h4 | event | against signal | 2379 | +0.036 | 0.045 | +0.24 | -1.76 | +nan | -1.76 | -2.25 |
| MYM | 60 | h8 | event | with signal | 2379 | -0.023 | 0.045 | +0.47 | -1.53 | +nan | -1.53 | -0.73 |
| MYM | 60 | h16 | event | against signal | 2379 | +0.032 | 0.045 | +0.71 | -1.29 | +nan | -1.29 | -1.90 |
| MYM | 60 | eod | event | against signal | 2379 | +0.043 | 0.045 | +1.44 | -0.56 | +nan | -0.56 | -1.33 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.270 | +0.327 | +0.183 | +0.013 | -0.610 | +0.000 | -0.034 | -0.038 | -0.039 | -0.036 | -0.043 |
| MES | 15 | +0.302 | +0.340 | +0.186 | +0.021 | -0.561 | +0.000 | -0.015 | -0.007 | -0.005 | -0.003 | -0.009 |
| MES | 60 | +0.373 | +0.280 | +0.166 | -0.009 | -0.490 | +0.000 | -0.003 | -0.025 | -0.053 | -0.034 | +0.118 |
| MNQ | 5 | +0.376 | +0.454 | +0.263 | +0.057 | -0.580 | +0.000 | -0.013 | -0.020 | -0.021 | -0.017 | -0.009 |
| MNQ | 15 | +0.391 | +0.402 | +0.223 | +0.044 | -0.529 | +0.000 | -0.013 | -0.011 | -0.010 | -0.004 | -0.030 |
| MNQ | 60 | +0.454 | +0.356 | +0.177 | +0.019 | -0.446 | +0.000 | -0.005 | -0.001 | -0.015 | -0.033 | -0.053 |
| MYM | 5 | +0.371 | +0.429 | +0.253 | +0.055 | -0.556 | +0.000 | -0.008 | -0.007 | +0.000 | +0.009 | -0.008 |
| MYM | 15 | +0.375 | +0.407 | +0.232 | +0.047 | -0.524 | +0.000 | -0.013 | -0.012 | +0.005 | +0.002 | -0.021 |
| MYM | 60 | +0.401 | +0.356 | +0.150 | +0.008 | -0.465 | +0.000 | -0.014 | -0.026 | -0.041 | -0.069 | -0.048 |

## Calibration

- MES 5-min: 1036271 bars, 85829 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 23830 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 4630 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 60231 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 19536 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 4667 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 26918 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 9324 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 2379 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 44425 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
