# Impact card: fam_reversal_short

bearish reversal patterns only (short side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (5 min), p=0.05; we would catch an effect of 0.013 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.013 R20, CONFIRMED, q=8.33e-16, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.18 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.237 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.132 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.027 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.011 R20, possible, q=0.241, 13 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.45 at recent bar sizes, 90% range up to $0.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.024 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.056 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.35).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.28 at recent bar sizes, 90% range up to $4.73); about 3.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.018 R20 over the next 8 bars (40 min), p=0.32; we would catch an effect of 0.017 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.014 R20, CONFIRMED, q=1.15e-08, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.44 at recent bar sizes, 90% range up to $0.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.236 R20 over the rest of the session (to 16:45), p=0.54; we would catch an effect of 0.040 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.2).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $10.08 at recent bar sizes, 90% range up to $2.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.025 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.058 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.18).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.21 at recent bar sizes, 90% range up to $6.09); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (5 min), p=0.23; we would catch an effect of 0.040 R20 or more 80% of the time).
- MYM 5-min size: the market moves 3% LESS after the event than after matched bars over the next 2 bars (10 min) (-0.020 R20, CONFIRMED, q=0.0477, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.10 at recent bar sizes, 90% range up to $0.27); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.082 R20 over the next 16 bars (4 h), p=0.44; we would catch an effect of 0.044 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.16).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.64 at recent bar sizes, 90% range up to $1.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.059 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.083 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.43 at recent bar sizes, 90% range up to $5.84); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.005 | +0.001 .. +0.009 | +0.0028 | 0.0062 / 0.007 / 0.0064 | 0.00729 | 1 | 0.793 | 12/16 | -0.000 | +0.010 | False | +2.6 / +2.7 |  |
| MES | 5 | h2 | +0.005 | +0.000 .. +0.011 | +0.0021 | 0.042 / 0.042 / 0.034 | 0.0365 |  |  | 12/16 | +0.003 | +0.008 |  | +2.0 / +2.0 |  |
| MES | 5 | h4 | +0.003 | -0.005 .. +0.010 | +0.0008 | 0.46 / 0.47 / 0.44 | 0.438 |  |  | 10/16 | +0.003 | +0.003 |  | +0.7 / +0.7 | 0.013 |
| MES | 5 | h8 | +0.001 | -0.012 .. +0.014 | +0.0002 | 0.87 / 0.88 / 0.84 | 0.836 |  |  | 8/16 | +0.004 | -0.002 |  | +0.2 / +0.2 |  |
| MES | 5 | h16 | +0.012 | -0.014 .. +0.037 | +0.0015 | 0.36 / 0.38 / 0.14 | 0.143 |  |  | 10/16 | +0.020 | +0.004 |  | +1.4 / +0.9 |  |
| MES | 5 | eod | -0.173 | -0.577 .. +0.232 | -0.0044 | 0.4 / 0.42 / 0.0012 | 0.000781 |  |  | 14/16 | -0.173 | -0.172 |  | -3.9 / -0.8 |  |
| MES | 15 | h1 | +0.002 | -0.006 .. +0.010 | +0.0010 | 0.62 / 0.63 / 0.61 | 0.6 |  |  | 10/16 | +0.004 | -0.000 |  | +0.5 / +0.5 |  |
| MES | 15 | h2 | +0.005 | -0.006 .. +0.017 | +0.0017 | 0.38 / 0.39 / 0.36 | 0.357 |  |  | 11/16 | +0.001 | +0.010 |  | +0.9 / +0.9 |  |
| MES | 15 | h4 | +0.004 | -0.013 .. +0.021 | +0.0009 | 0.66 / 0.66 / 0.63 | 0.632 |  |  | 8/16 | +0.005 | +0.003 |  | +0.5 / +0.4 | 0.027 |
| MES | 15 | h8 | +0.000 | -0.031 .. +0.031 | -0.0000 | 1 / 1 / 0.99 | 0.991 |  |  | 8/16 | +0.018 | -0.018 |  | +0.0 / +0.0 |  |
| MES | 15 | h16 | -0.029 | -0.084 .. +0.027 | -0.0031 | 0.32 / 0.32 / 0.081 | 0.0761 |  |  | 10/16 | +0.010 | -0.067 |  | -1.6 / -1.0 |  |
| MES | 15 | eod * | -0.132 | -0.363 .. +0.099 | -0.0055 | 0.26 / 0.27 / 0.0033 | 0.00365 | 1 | 1 | 12/16 | -0.085 | -0.179 | False | -3.0 / -1.1 |  |
| MES | 60 | h1 | +0.003 | -0.014 .. +0.020 | +0.0013 | 0.76 / 0.75 / 0.74 | 0.74 |  |  | 6/16 | +0.000 | +0.005 |  | +0.3 / +0.3 |  |
| MES | 60 | h2 | -0.010 | -0.037 .. +0.017 | -0.0032 | 0.48 / 0.48 / 0.38 | 0.372 |  |  | 8/16 | -0.013 | -0.006 |  | -0.8 / -0.7 |  |
| MES | 60 | h4 * | -0.024 | -0.062 .. +0.015 | -0.0056 | 0.22 / 0.22 / 0.12 | 0.123 | 1 | 1 | 13/16 | -0.030 | -0.018 | False | -1.4 / -1.2 | 0.056 |
| MES | 60 | h8 | -0.034 | -0.098 .. +0.030 | -0.0059 | 0.29 / 0.29 / 0.12 | 0.114 |  |  | 9/16 | -0.031 | -0.038 |  | -1.4 / -1.1 |  |
| MES | 60 | h16 | -0.039 | -0.129 .. +0.051 | -0.0051 | 0.4 / 0.4 / 0.16 | 0.157 |  |  | 12/16 | -0.042 | -0.036 |  | -1.3 / -0.8 |  |
| MES | 60 | eod | -0.030 | -0.124 .. +0.063 | -0.0038 | 0.52 / 0.53 / 0.29 | 0.3 |  |  | 11/16 | -0.033 | -0.028 |  | -1.0 / -0.6 |  |
| MNQ | 5 | h1 | +0.003 | -0.002 .. +0.008 | +0.0012 | 0.25 / 0.24 / 0.27 | 0.269 |  |  | 11/16 | +0.001 | +0.004 |  | +1.2 / +1.1 |  |
| MNQ | 5 | h2 | -0.003 | -0.010 .. +0.004 | -0.0007 | 0.43 / 0.43 / 0.5 | 0.5 |  |  | 9/16 | -0.005 | -0.001 |  | -0.8 / -0.8 |  |
| MNQ | 5 | h4 | -0.009 | -0.020 .. +0.001 | -0.0016 | 0.079 / 0.076 / 0.13 | 0.121 |  |  | 10/16 | -0.006 | -0.013 |  | -1.9 / -1.8 | 0.017 |
| MNQ | 5 | h8 * | -0.018 | -0.036 .. +0.000 | -0.0021 | 0.053 / 0.052 / 0.043 | 0.0448 | 1 | 1 | 11/16 | -0.015 | -0.020 | False | -2.5 / -1.9 |  |
| MNQ | 5 | h16 | -0.018 | -0.050 .. +0.014 | -0.0015 | 0.26 / 0.27 / 0.15 | 0.156 |  |  | 9/16 | -0.011 | -0.025 |  | -1.7 / -1.1 |  |
| MNQ | 5 | eod | -0.123 | -0.622 .. +0.376 | -0.0021 | 0.63 / 0.65 / 0.062 | 0.0594 |  |  | 11/16 | -0.104 | -0.141 |  | -2.0 / -0.5 |  |
| MNQ | 15 | h1 | +0.003 | -0.006 .. +0.012 | +0.0009 | 0.57 / 0.57 / 0.62 | 0.602 |  |  | 9/16 | -0.003 | +0.008 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h2 | +0.010 | -0.004 .. +0.024 | +0.0023 | 0.14 / 0.14 / 0.21 | 0.204 |  |  | 12/16 | +0.007 | +0.014 |  | +1.6 / +1.5 |  |
| MNQ | 15 | h4 | +0.013 | -0.007 .. +0.034 | +0.0017 | 0.19 / 0.19 / 0.33 | 0.32 |  |  | 10/16 | +0.016 | +0.010 |  | +1.4 / +1.3 | 0.040 |
| MNQ | 15 | h8 | +0.018 | -0.017 .. +0.053 | +0.0018 | 0.31 / 0.31 / 0.3 | 0.3 |  |  | 10/16 | +0.042 | -0.005 |  | +1.3 / +1.0 |  |
| MNQ | 15 | h16 | -0.006 | -0.070 .. +0.058 | -0.0005 | 0.86 / 0.86 / 0.78 | 0.79 |  |  | 7/16 | +0.047 | -0.058 |  | -0.3 / -0.2 |  |
| MNQ | 15 | eod * | -0.236 | -0.500 .. +0.029 | -0.0067 | 0.081 / 0.089 / 0.00017 | 0.00026 | 1 | 1 | 12/16 | -0.146 | -0.324 | False | -4.6 / -1.7 |  |
| MNQ | 60 | h1 | +0.003 | -0.015 .. +0.021 | +0.0013 | 0.76 / 0.76 / 0.75 | 0.754 |  |  | 8/16 | +0.001 | +0.005 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h2 | -0.003 | -0.031 .. +0.026 | -0.0008 | 0.85 / 0.85 / 0.82 | 0.825 |  |  | 8/16 | -0.003 | -0.002 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h4 | +0.002 | -0.040 .. +0.045 | +0.0006 | 0.91 / 0.91 / 0.89 | 0.882 |  |  | 8/16 | -0.008 | +0.013 |  | +0.1 / +0.1 | 0.058 |
| MNQ | 60 | h8 | -0.012 | -0.079 .. +0.055 | -0.0020 | 0.72 / 0.71 / 0.59 | 0.592 |  |  | 9/16 | -0.043 | +0.019 |  | -0.5 / -0.4 |  |
| MNQ | 60 | h16 * | -0.025 | -0.118 .. +0.068 | -0.0031 | 0.6 / 0.61 / 0.4 | 0.401 | 1 | 1 | 10/16 | -0.037 | -0.013 | False | -0.8 / -0.5 |  |
| MNQ | 60 | eod | -0.023 | -0.122 .. +0.075 | -0.0027 | 0.64 / 0.65 / 0.45 | 0.452 |  |  | 10/16 | -0.037 | -0.009 |  | -0.7 / -0.5 |  |
| MYM | 5 | h1 * | +0.009 | +0.002 .. +0.015 | +0.0032 | 0.011 / 0.012 / 0.031 | 0.0306 | 1 | 0.888 | 6/8 | n/a | +0.009 | False | +2.6 / +2.5 |  |
| MYM | 5 | h2 | +0.009 | -0.000 .. +0.018 | +0.0020 | 0.06 / 0.063 / 0.15 | 0.14 |  |  | 7/8 | n/a | +0.009 |  | +1.9 / +1.9 |  |
| MYM | 5 | h4 | +0.001 | -0.014 .. +0.016 | +0.0001 | 0.92 / 0.92 / 0.93 | 0.933 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.1 | 0.040 |
| MYM | 5 | h8 | -0.002 | -0.028 .. +0.024 | -0.0002 | 0.88 / 0.88 / 0.88 | 0.887 |  |  | 4/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 5 | h16 | -0.019 | -0.067 .. +0.029 | -0.0015 | 0.44 / 0.44 / 0.31 | 0.324 |  |  | 5/8 | n/a | -0.019 |  | -1.3 / -0.8 |  |
| MYM | 5 | eod | -0.222 | -0.953 .. +0.510 | -0.0039 | 0.55 / 0.55 / 0.011 | 0.0116 |  |  | 6/8 | n/a | -0.222 |  | -2.7 / -0.6 |  |
| MYM | 15 | h1 | -0.004 | -0.017 .. +0.009 | -0.0016 | 0.52 / 0.52 / 0.54 | 0.534 |  |  | 4/8 | n/a | -0.004 |  | -0.7 / -0.6 |  |
| MYM | 15 | h2 | -0.007 | -0.027 .. +0.012 | -0.0016 | 0.46 / 0.45 / 0.53 | 0.518 |  |  | 5/8 | n/a | -0.007 |  | -0.8 / -0.7 |  |
| MYM | 15 | h4 | -0.012 | -0.042 .. +0.018 | -0.0016 | 0.42 / 0.41 / 0.54 | 0.526 |  |  | 4/8 | n/a | -0.012 |  | -1.0 / -0.8 | 0.044 |
| MYM | 15 | h8 | -0.025 | -0.076 .. +0.025 | -0.0025 | 0.33 / 0.32 / 0.33 | 0.328 |  |  | 5/8 | n/a | -0.025 |  | -1.4 / -1.0 |  |
| MYM | 15 | h16 * | -0.082 | -0.171 .. +0.008 | -0.0057 | 0.074 / 0.067 / 0.026 | 0.0184 | 1 | 1 | 6/8 | n/a | -0.082 | False | -3.0 / -1.8 |  |
| MYM | 15 | eod | -0.157 | -0.548 .. +0.235 | -0.0046 | 0.43 / 0.42 / 0.077 | 0.0732 |  |  | 5/8 | n/a | -0.157 |  | -2.3 / -0.8 |  |
| MYM | 60 | h1 | +0.013 | -0.013 .. +0.038 | +0.0056 | 0.34 / 0.35 / 0.3 | 0.293 |  |  | 5/8 | n/a | +0.013 |  | +0.9 / +0.9 |  |
| MYM | 60 | h2 | +0.007 | -0.032 .. +0.047 | +0.0023 | 0.72 / 0.72 / 0.67 | 0.676 |  |  | 4/8 | n/a | +0.007 |  | +0.4 / +0.4 |  |
| MYM | 60 | h4 | +0.020 | -0.040 .. +0.079 | +0.0044 | 0.52 / 0.51 / 0.4 | 0.399 |  |  | 4/8 | n/a | +0.020 |  | +0.7 / +0.6 | 0.083 |
| MYM | 60 | h8 * | +0.059 | -0.039 .. +0.157 | +0.0097 | 0.24 / 0.23 / 0.068 | 0.068 | 1 | 1 | 5/8 | n/a | +0.059 | False | +1.6 / +1.2 |  |
| MYM | 60 | h16 | +0.051 | -0.082 .. +0.184 | +0.0064 | 0.45 / 0.45 / 0.21 | 0.212 |  |  | 7/8 | n/a | +0.051 |  | +1.1 / +0.8 |  |
| MYM | 60 | eod | +0.037 | -0.102 .. +0.175 | +0.0044 | 0.6 / 0.6 / 0.38 | 0.379 |  |  | 6/8 | n/a | +0.037 |  | +0.8 / +0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.013 | -0.016 .. -0.010 | -2.7% | -0.026 | 1.7e-18 | 8.33e-16 | 15/16 |
| MES | 5 | h2 | -0.015 | -0.019 .. -0.011 | -2.1% | -0.035 | 4.1e-12 |  | 14/16 |
| MES | 5 | h4 | -0.021 | -0.027 .. -0.014 | -2.1% | -0.045 | 2.1e-10 |  | 13/16 |
| MES | 5 | h8 | -0.023 | -0.033 .. -0.013 | -1.6% | -0.057 | 7.9e-06 |  | 14/16 |
| MES | 5 | h16 | -0.031 | -0.048 .. -0.015 | -1.5% | -0.077 | 0.00019 |  | 16/16 |
| MES | 5 | eod | -0.195 | -0.331 .. -0.059 | -2.0% | -0.306 | 0.0051 |  | 11/16 |
| MES | 15 | h1 * | -0.011 | -0.017 .. -0.005 | -2.1% | -0.021 | 0.0014 | 0.241 | 13/16 |
| MES | 15 | h2 | -0.008 | -0.018 .. +0.002 | -1.1% | -0.023 | 0.099 |  | 11/16 |
| MES | 15 | h4 | -0.011 | -0.026 .. +0.003 | -1.1% | -0.036 | 0.11 |  | 9/16 |
| MES | 15 | h8 | -0.018 | -0.039 .. +0.003 | -1.2% | -0.059 | 0.088 |  | 11/16 |
| MES | 15 | h16 | -0.019 | -0.052 .. +0.013 | -0.8% | -0.073 | 0.24 |  | 10/16 |
| MES | 15 | eod | -0.078 | -0.200 .. +0.044 | -1.4% | -0.132 | 0.21 |  | 10/16 |
| MES | 60 | h1 | -0.002 | -0.014 .. +0.011 | -0.3% | -0.004 | 0.79 |  | 9/16 |
| MES | 60 | h2 | +0.001 | -0.016 .. +0.018 | +0.1% | -0.007 | 0.92 |  | 9/16 |
| MES | 60 | h4 | -0.015 | -0.039 .. +0.008 | -1.4% | -0.020 | 0.2 |  | 10/16 |
| MES | 60 | h8 * | -0.031 | -0.063 .. +0.001 | -2.1% | -0.034 | 0.059 | 1 | 9/16 |
| MES | 60 | h16 | -0.031 | -0.068 .. +0.007 | -1.5% | -0.041 | 0.13 |  | 11/16 |
| MES | 60 | eod | -0.031 | -0.070 .. +0.008 | -1.4% | -0.039 | 0.14 |  | 10/16 |
| MNQ | 5 | h1 * | -0.014 | -0.018 .. -0.010 | -2.7% | -0.026 | 3.4e-11 | 1.15e-08 | 14/16 |
| MNQ | 5 | h2 | -0.016 | -0.023 .. -0.009 | -2.1% | -0.032 | 5.7e-06 |  | 14/16 |
| MNQ | 5 | h4 | -0.025 | -0.037 .. -0.012 | -2.2% | -0.048 | 0.00011 |  | 15/16 |
| MNQ | 5 | h8 | -0.036 | -0.060 .. -0.011 | -2.2% | -0.072 | 0.004 |  | 13/16 |
| MNQ | 5 | h16 | -0.054 | -0.097 .. -0.011 | -2.2% | -0.120 | 0.014 |  | 12/16 |
| MNQ | 5 | eod | -0.266 | -0.482 .. -0.050 | -2.1% | -0.466 | 0.016 |  | 12/16 |
| MNQ | 15 | h1 * | -0.009 | -0.016 .. -0.002 | -1.6% | -0.020 | 0.033 | 1 | 12/16 |
| MNQ | 15 | h2 | -0.012 | -0.026 .. +0.002 | -1.5% | -0.029 | 0.16 |  | 11/16 |
| MNQ | 15 | h4 | -0.027 | -0.056 .. +0.002 | -2.4% | -0.045 | 0.12 |  | 11/16 |
| MNQ | 15 | h8 | -0.031 | -0.075 .. +0.013 | -1.8% | -0.085 | 0.17 |  | 10/16 |
| MNQ | 15 | h16 | -0.025 | -0.076 .. +0.026 | -1.0% | -0.136 | 0.37 |  | 8/16 |
| MNQ | 15 | eod | -0.083 | -0.285 .. +0.118 | -1.3% | -0.189 | 0.42 |  | 6/16 |
| MNQ | 60 | h1 | +0.003 | -0.009 .. +0.015 | +0.5% | +0.006 | 0.8 |  | 10/16 |
| MNQ | 60 | h2 | -0.004 | -0.021 .. +0.013 | -0.5% | -0.008 | 0.66 |  | 9/16 |
| MNQ | 60 | h4 | -0.005 | -0.031 .. +0.021 | -0.5% | -0.003 | 0.69 |  | 8/16 |
| MNQ | 60 | h8 * | -0.038 | -0.071 .. -0.004 | -2.4% | -0.022 | 0.03 | 1 | 12/16 |
| MNQ | 60 | h16 | -0.030 | -0.070 .. +0.010 | -1.4% | -0.023 | 0.15 |  | 11/16 |
| MNQ | 60 | eod | -0.033 | -0.073 .. +0.007 | -1.4% | -0.025 | 0.12 |  | 11/16 |
| MYM | 5 | h1 | -0.013 | -0.019 .. -0.007 | -2.4% | -0.025 | 0.00055 |  | 8/8 |
| MYM | 5 | h2 * | -0.020 | -0.031 .. -0.010 | -2.7% | -0.037 | 0.00025 | 0.0477 | 7/8 |
| MYM | 5 | h4 | -0.028 | -0.049 .. -0.008 | -2.6% | -0.057 | 0.0063 |  | 7/8 |
| MYM | 5 | h8 | -0.042 | -0.078 .. -0.005 | -2.6% | -0.084 | 0.029 |  | 6/8 |
| MYM | 5 | h16 | -0.063 | -0.114 .. -0.011 | -2.7% | -0.129 | 0.018 |  | 7/8 |
| MYM | 5 | eod | -0.170 | -0.422 .. +0.082 | -1.5% | -0.319 | 0.19 |  | 4/8 |
| MYM | 15 | h1 | -0.010 | -0.021 .. +0.000 | -2.0% | -0.022 | 0.079 |  | 6/8 |
| MYM | 15 | h2 * | -0.023 | -0.042 .. -0.005 | -3.0% | -0.041 | 0.026 | 1 | 5/8 |
| MYM | 15 | h4 | -0.027 | -0.062 .. +0.007 | -2.5% | -0.056 | 0.13 |  | 5/8 |
| MYM | 15 | h8 | -0.042 | -0.094 .. +0.009 | -2.6% | -0.109 | 0.11 |  | 5/8 |
| MYM | 15 | h16 | -0.078 | -0.164 .. +0.008 | -3.2% | -0.177 | 0.084 |  | 7/8 |
| MYM | 15 | eod | -0.144 | -0.389 .. +0.101 | -2.4% | -0.209 | 0.25 |  | 5/8 |
| MYM | 60 | h1 | -0.004 | -0.022 .. +0.014 | -0.7% | -0.011 | 0.67 |  | 4/8 |
| MYM | 60 | h2 | +0.001 | -0.027 .. +0.029 | +0.1% | -0.014 | 0.96 |  | 5/8 |
| MYM | 60 | h4 | -0.000 | -0.037 .. +0.037 | -0.0% | -0.008 | 0.99 |  | 4/8 |
| MYM | 60 | h8 | -0.006 | -0.056 .. +0.045 | -0.4% | -0.010 | 0.83 |  | 5/8 |
| MYM | 60 | h16 | -0.013 | -0.072 .. +0.045 | -0.6% | -0.016 | 0.66 |  | 5/8 |
| MYM | 60 | eod * | -0.014 | -0.073 .. +0.045 | -0.6% | -0.022 | 0.64 | 1 | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.47 pts | +0.18 .. +0.77 | 0.0021 |
| MES | 15 | +0.35 pts | -0.22 .. +0.91 | 0.23 |
| MES | 60 | +0.29 pts | -0.84 .. +1.42 | 0.66 |
| MNQ | 5 | +0.36 pts | +0.03 .. +0.69 | 0.031 |
| MNQ | 15 | +0.42 pts | -0.11 .. +0.95 | 0.12 |
| MNQ | 60 | +0.20 pts | -0.87 .. +1.27 | 0.74 |
| MYM | 5 | +1.04 pts | +0.58 .. +1.50 | 8.8e-06 |
| MYM | 15 | +0.17 pts | -0.63 .. +0.98 | 0.68 |
| MYM | 60 | +0.62 pts | -0.96 .. +2.20 | 0.45 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 132780 | -0.004 | 0.371 | +0.03 | -3.47 | -3.53 | -3.40 | -3.39 |
| MES | 5 | h2 | event | with signal | 132780 | -0.010 | 0.371 | -0.06 | -3.56 | -3.56 | -3.57 | -3.43 |
| MES | 5 | h4 | event | with signal | 132780 | -0.018 | 0.371 | -0.13 | -3.63 | -3.59 | -3.68 | -3.47 |
| MES | 5 | h8 | event | with signal | 132780 | -0.031 | 0.371 | -0.26 | -3.76 | -3.67 | -3.87 | -3.54 |
| MES | 5 | h16 | event | with signal | 132780 | -0.046 | 0.371 | -0.34 | -3.84 | -3.75 | -3.95 | -3.48 |
| MES | 5 | eod | event | against signal | 132780 | +0.808 | 0.371 | +5.02 | +1.52 | +0.30 | +3.04 | -0.56 |
| MES | 15 | h1 | event | with signal | 39102 | -0.010 | 0.203 | -0.15 | -3.65 | -3.61 | -3.69 | -3.48 |
| MES | 15 | h2 | event | with signal | 39102 | -0.013 | 0.203 | -0.16 | -3.66 | -3.68 | -3.63 | -3.42 |
| MES | 15 | h4 | event | with signal | 39102 | -0.026 | 0.203 | -0.33 | -3.83 | -3.82 | -3.83 | -3.50 |
| MES | 15 | h8 | event | with signal | 39102 | -0.052 | 0.203 | -0.76 | -4.26 | -3.94 | -4.61 | -3.73 |
| MES | 15 | h16 | event | against signal | 39102 | +0.124 | 0.203 | +1.75 | -1.75 | -2.45 | -0.99 | -2.61 |
| MES | 15 | eod | event | against signal | 39102 | +0.426 | 0.203 | +5.24 | +1.74 | +0.33 | +3.26 | +0.16 |
| MES | 60 | h1 | event | with signal | 9002 | -0.007 | 0.096 | -0.31 | -3.81 | -3.66 | -3.96 | -3.60 |
| MES | 60 | h2 | event | against signal | 9002 | +0.032 | 0.096 | +0.84 | -2.66 | -3.01 | -2.31 | -3.23 |
| MES | 60 | h4 | event | against signal | 9002 | +0.068 | 0.096 | +2.11 | -1.39 | -1.98 | -0.81 | -2.52 |
| MES | 60 | h8 | event | against signal | 9002 | +0.114 | 0.096 | +3.43 | -0.07 | -1.20 | +1.05 | -2.06 |
| MES | 60 | h16 | event | against signal | 9002 | +0.149 | 0.096 | +4.33 | +0.83 | -0.17 | +1.81 | -1.69 |
| MES | 60 | eod | event | against signal | 9002 | +0.152 | 0.096 | +4.27 | +0.77 | -0.08 | +1.62 | -2.08 |
| MNQ | 5 | h1 | event | with signal | 117169 | -0.005 | 0.140 | -0.02 | -2.02 | -2.02 | -2.02 | -1.94 |
| MNQ | 5 | h2 | event | against signal | 117169 | +0.017 | 0.140 | +0.13 | -1.87 | -1.94 | -1.80 | -1.99 |
| MNQ | 5 | h4 | event | against signal | 117169 | +0.028 | 0.140 | +0.26 | -1.74 | -1.91 | -1.56 | -1.85 |
| MNQ | 5 | h8 | event | against signal | 117169 | +0.047 | 0.140 | +0.35 | -1.65 | -1.84 | -1.45 | -1.76 |
| MNQ | 5 | h16 | event | against signal | 117169 | +0.079 | 0.140 | +0.47 | -1.53 | -1.69 | -1.35 | -1.80 |
| MNQ | 5 | eod | event | against signal | 117169 | +0.962 | 0.140 | +6.47 | +4.47 | +1.20 | +7.97 | +2.64 |
| MNQ | 15 | h1 | event | with signal | 37900 | -0.008 | 0.079 | +0.09 | -1.91 | -2.10 | -1.72 | -1.74 |
| MNQ | 15 | h2 | event | with signal | 37900 | -0.004 | 0.079 | +0.15 | -1.85 | -2.14 | -1.56 | -1.68 |
| MNQ | 15 | h4 | event | with signal | 37900 | -0.012 | 0.079 | -0.01 | -2.01 | -2.26 | -1.75 | -1.72 |
| MNQ | 15 | h8 | event | with signal | 37900 | -0.031 | 0.079 | -0.89 | -2.89 | -2.38 | -3.41 | -2.35 |
| MNQ | 15 | h16 | event | against signal | 37900 | +0.098 | 0.079 | +2.33 | +0.33 | -1.21 | +1.91 | -0.48 |
| MNQ | 15 | eod | event | against signal | 37900 | +0.574 | 0.079 | +8.32 | +6.32 | +1.35 | +11.39 | +5.20 |
| MNQ | 60 | h1 | event | with signal | 9260 | -0.008 | 0.039 | -0.56 | -2.56 | -2.26 | -2.88 | -2.34 |
| MNQ | 60 | h2 | event | against signal | 9260 | +0.027 | 0.039 | +1.24 | -0.76 | -1.53 | +0.08 | -1.41 |
| MNQ | 60 | h4 | event | with signal | 9260 | -0.046 | 0.039 | -1.71 | -3.71 | -3.09 | -4.39 | -2.36 |
| MNQ | 60 | h8 | event | against signal | 9260 | +0.098 | 0.039 | +3.23 | +1.23 | +0.15 | +2.39 | -1.08 |
| MNQ | 60 | h16 | event | against signal | 9260 | +0.149 | 0.039 | +5.07 | +3.07 | +0.54 | +5.79 | +0.20 |
| MNQ | 60 | eod | event | against signal | 9260 | +0.163 | 0.039 | +5.02 | +3.02 | +0.93 | +5.29 | -0.32 |
| MYM | 5 | h1 | event | with signal | 56644 | +0.004 | 0.175 | +0.08 | -1.92 | +nan | -1.92 | -1.86 |
| MYM | 5 | h2 | event | with signal | 56644 | +0.004 | 0.175 | +0.01 | -1.99 | +nan | -1.99 | -1.91 |
| MYM | 5 | h4 | event | with signal | 56644 | -0.002 | 0.175 | -0.05 | -2.05 | +nan | -2.05 | -1.96 |
| MYM | 5 | h8 | event | against signal | 56644 | +0.003 | 0.175 | +0.15 | -1.85 | +nan | -1.85 | -1.99 |
| MYM | 5 | h16 | event | against signal | 56644 | +0.029 | 0.175 | +0.30 | -1.70 | +nan | -1.70 | -2.01 |
| MYM | 5 | eod | event | against signal | 56644 | +0.466 | 0.175 | +4.72 | +2.72 | +nan | +2.72 | +1.28 |
| MYM | 15 | h1 | event | against signal | 18686 | +0.011 | 0.100 | +0.16 | -1.84 | +nan | -1.84 | -1.95 |
| MYM | 15 | h2 | event | against signal | 18686 | +0.013 | 0.100 | +0.10 | -1.90 | +nan | -1.90 | -2.00 |
| MYM | 15 | h4 | event | against signal | 18686 | +0.016 | 0.100 | +0.11 | -1.89 | +nan | -1.89 | -1.96 |
| MYM | 15 | h8 | event | against signal | 18686 | +0.030 | 0.100 | +0.55 | -1.45 | +nan | -1.45 | -1.55 |
| MYM | 15 | h16 | event | against signal | 18686 | +0.064 | 0.100 | +1.57 | -0.43 | +nan | -0.43 | -0.15 |
| MYM | 15 | eod | event | against signal | 18686 | +0.223 | 0.100 | +4.87 | +2.87 | +nan | +2.87 | +2.90 |
| MYM | 60 | h1 | event | with signal | 4487 | +0.007 | 0.048 | +0.04 | -1.96 | +nan | -1.96 | -1.80 |
| MYM | 60 | h2 | event | with signal | 4487 | -0.008 | 0.048 | -0.72 | -2.72 | +nan | -2.72 | -2.18 |
| MYM | 60 | h4 | event | with signal | 4487 | -0.007 | 0.048 | -0.37 | -2.37 | +nan | -2.37 | -1.43 |
| MYM | 60 | h8 | event | with signal | 4487 | +0.013 | 0.048 | +0.37 | -1.63 | +nan | -1.63 | -0.01 |
| MYM | 60 | h16 | event | with signal | 4487 | -0.008 | 0.048 | -1.56 | -3.56 | +nan | -3.56 | -1.48 |
| MYM | 60 | eod | event | with signal | 4487 | -0.031 | 0.048 | -2.09 | -4.09 | +nan | -4.09 | -1.56 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.124 | +0.155 | +0.060 | -0.071 | -0.474 | +0.000 | -0.043 | -0.046 | -0.048 | -0.049 | -0.038 |
| MES | 15 | +0.128 | +0.163 | +0.055 | -0.089 | -0.533 | +0.000 | -0.020 | -0.018 | -0.021 | -0.026 | -0.063 |
| MES | 60 | +0.024 | +0.053 | -0.019 | -0.148 | -0.568 | +0.000 | +0.000 | -0.015 | -0.037 | -0.056 | +0.040 |
| MNQ | 5 | +0.209 | +0.258 | +0.141 | -0.032 | -0.505 | +0.000 | -0.017 | -0.024 | -0.028 | -0.030 | -0.027 |
| MNQ | 15 | +0.169 | +0.204 | +0.097 | -0.066 | -0.537 | +0.000 | -0.009 | +0.001 | +0.007 | +0.015 | -0.017 |
| MNQ | 60 | +0.024 | +0.072 | -0.011 | -0.144 | -0.566 | +0.000 | +0.003 | -0.008 | +0.001 | -0.038 | -0.031 |
| MYM | 5 | +0.219 | +0.259 | +0.140 | -0.036 | -0.524 | +0.000 | -0.005 | -0.006 | -0.013 | -0.014 | -0.034 |
| MYM | 15 | +0.193 | +0.225 | +0.106 | -0.062 | -0.538 | +0.000 | -0.015 | -0.019 | -0.023 | -0.037 | -0.103 |
| MYM | 60 | +0.103 | +0.149 | +0.041 | -0.104 | -0.550 | +0.000 | +0.012 | +0.003 | +0.002 | +0.046 | +0.022 |

## Calibration

- MES 5-min: 1036271 bars, 132780 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 39102 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 9002 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 117169 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 37900 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 9260 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 56644 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 18686 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 4487 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33551 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
