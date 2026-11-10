# Impact card: above_vwap

close above session VWAP (1) vs below (0) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: state. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (5 min), p=0.4; we would catch an effect of 0.015 R20 or more 80% of the time).
- MES 5-min size: the market moves 1% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.006 R20, CONFIRMED, q=0.003, 11 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.16 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.225 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.132 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.028 R20 or more 80% of the time).
- MES 15-min size: the market moves 4% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.021 R20, CONFIRMED, q=1.64e-13, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.40 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.129 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.032 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MES 60-min size: the market moves 8% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.039 R20, CONFIRMED, q=2.43e-17, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.27 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.013 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 1% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.007 R20, CONFIRMED, q=0.0391, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.35 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.078 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.263 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 4% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.023 R20, CONFIRMED, q=5.67e-08, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.87 at recent bar sizes, 90% range up to $0.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.056 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.050 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 7% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.036 R20, CONFIRMED, q=5.55e-12, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.55 at recent bar sizes, 90% range up to $3.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.029 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.059).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.34 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.171 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.062 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.060 R20 or more 80% of the time).
- MYM 15-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.025 R20, CONFIRMED, q=0.000189, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.84 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.097 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.015 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.070 R20 or more 80% of the time).
- MYM 60-min size: the market moves 6% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.032 R20, CONFIRMED, q=0.000292, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.32 at recent bar sizes, 90% range up to $2.15); about 1.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.003 | -0.005 .. +0.000 | -0.0025 | 0.053 / 0.067 / 0.083 | 0.0813 | 1 | 1 | 12/16 | -0.004 | -0.001 | False | -1.8 / -1.9 |  |
| MES | 5 | h2 | -0.002 | -0.007 .. +0.002 | -0.0017 | 0.33 / 0.35 / 0.4 | 0.387 |  |  | 12/16 | -0.008 | +0.004 |  | -1.2 / -1.0 |  |
| MES | 5 | h4 | -0.001 | -0.010 .. +0.009 | -0.0004 | 0.88 / 0.88 / 0.89 | 0.898 |  |  | 9/16 | -0.014 | +0.013 |  | -0.2 / -0.2 | 0.015 |
| MES | 5 | h8 | -0.004 | -0.022 .. +0.014 | -0.0013 | 0.67 / 0.69 / 0.71 | 0.714 |  |  | 9/16 | -0.034 | +0.026 |  | -0.9 / -0.4 |  |
| MES | 5 | h16 | -0.003 | -0.039 .. +0.033 | -0.0007 | 0.86 / 0.87 / 0.87 | 0.869 |  |  | 9/16 | -0.043 | +0.037 |  | -0.5 / -0.2 |  |
| MES | 5 | eod | +0.071 | -0.386 .. +0.528 | +0.0031 | 0.76 / 0.76 / 0.74 | 0.747 |  |  | 6/16 | +0.073 | +0.069 |  | +2.2 / +0.3 |  |
| MES | 15 | h1 | -0.000 | -0.005 .. +0.005 | -0.0000 | 0.98 / 0.98 / 0.97 | 0.973 |  |  | 10/16 | -0.005 | +0.005 |  | -0.0 / -0.0 |  |
| MES | 15 | h2 | +0.000 | -0.008 .. +0.009 | +0.0002 | 0.92 / 0.93 / 0.94 | 0.944 |  |  | 7/16 | -0.013 | +0.014 |  | +0.1 / +0.1 |  |
| MES | 15 | h4 | +0.001 | -0.016 .. +0.019 | +0.0005 | 0.88 / 0.88 / 0.9 | 0.898 |  |  | 7/16 | -0.018 | +0.020 |  | +0.2 / +0.2 | 0.028 |
| MES | 15 | h8 | -0.001 | -0.034 .. +0.033 | -0.0002 | 0.97 / 0.97 / 0.97 | 0.968 |  |  | 9/16 | -0.036 | +0.034 |  | -0.1 / -0.0 |  |
| MES | 15 | h16 | +0.030 | -0.037 .. +0.097 | +0.0052 | 0.38 / 0.39 / 0.39 | 0.383 |  |  | 8/16 | -0.054 | +0.113 |  | +2.4 / +0.9 |  |
| MES | 15 | eod * | +0.132 | -0.181 .. +0.445 | +0.0089 | 0.41 / 0.39 / 0.29 | 0.288 | 1 | 1 | 7/16 | +0.041 | +0.223 | False | +4.2 / +0.8 |  |
| MES | 60 | h1 | -0.001 | -0.011 .. +0.009 | -0.0008 | 0.82 / 0.83 / 0.83 | 0.823 |  |  | 9/16 | -0.010 | +0.008 |  | -0.2 / -0.2 |  |
| MES | 60 | h2 | -0.004 | -0.021 .. +0.014 | -0.0019 | 0.68 / 0.69 / 0.7 | 0.708 |  |  | 8/16 | -0.019 | +0.012 |  | -0.5 / -0.4 |  |
| MES | 60 | h4 | +0.013 | -0.015 .. +0.042 | +0.0049 | 0.35 / 0.37 / 0.42 | 0.42 |  |  | 8/16 | -0.016 | +0.042 |  | +1.2 / +0.9 | 0.046 |
| MES | 60 | h8 * | +0.032 | -0.018 .. +0.082 | +0.0085 | 0.21 / 0.21 / 0.24 | 0.235 | 1 | 1 | 8/16 | +0.003 | +0.061 | False | +2.1 / +1.3 |  |
| MES | 60 | h16 | +0.038 | -0.037 .. +0.113 | +0.0077 | 0.32 / 0.31 / 0.34 | 0.343 |  |  | 9/16 | +0.028 | +0.047 |  | +1.9 / +1.0 |  |
| MES | 60 | eod | +0.038 | -0.041 .. +0.117 | +0.0074 | 0.34 / 0.33 / 0.36 | 0.358 |  |  | 9/16 | +0.034 | +0.043 |  | +1.9 / +1.0 |  |
| MNQ | 5 | h1 | -0.001 | -0.004 .. +0.003 | -0.0005 | 0.71 / 0.72 / 0.75 | 0.746 |  |  | 6/16 | -0.005 | +0.004 |  | -0.3 / -0.4 |  |
| MNQ | 5 | h2 | -0.001 | -0.008 .. +0.006 | -0.0004 | 0.84 / 0.85 / 0.86 | 0.862 |  |  | 9/16 | -0.013 | +0.011 |  | -0.2 / -0.2 |  |
| MNQ | 5 | h4 | -0.000 | -0.015 .. +0.014 | -0.0001 | 0.97 / 0.97 / 0.98 | 0.977 |  |  | 8/16 | -0.024 | +0.023 |  | -0.1 / -0.0 | 0.019 |
| MNQ | 5 | h8 | -0.007 | -0.031 .. +0.017 | -0.0015 | 0.57 / 0.58 / 0.64 | 0.642 |  |  | 9/16 | -0.047 | +0.033 |  | -1.0 / -0.6 |  |
| MNQ | 5 | h16 * | -0.013 | -0.058 .. +0.033 | -0.0020 | 0.58 / 0.59 / 0.64 | 0.65 | 1 | 1 | 8/16 | -0.067 | +0.041 | False | -1.4 / -0.5 |  |
| MNQ | 5 | eod | +0.119 | -0.505 .. +0.742 | +0.0038 | 0.71 / 0.7 / 0.67 | 0.666 |  |  | 7/16 | -0.175 | +0.410 |  | +2.7 / +0.4 |  |
| MNQ | 15 | h1 | -0.001 | -0.008 .. +0.006 | -0.0006 | 0.79 / 0.79 / 0.77 | 0.786 |  |  | 9/16 | -0.009 | +0.007 |  | -0.3 / -0.3 |  |
| MNQ | 15 | h2 | +0.000 | -0.011 .. +0.012 | +0.0001 | 0.95 / 0.95 / 0.96 | 0.965 |  |  | 8/16 | -0.014 | +0.015 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h4 | -0.001 | -0.023 .. +0.021 | -0.0002 | 0.93 / 0.93 / 0.94 | 0.943 |  |  | 8/16 | -0.022 | +0.020 |  | -0.1 / -0.1 | 0.037 |
| MNQ | 15 | h8 | -0.002 | -0.042 .. +0.037 | -0.0003 | 0.92 / 0.92 / 0.94 | 0.939 |  |  | 9/16 | -0.046 | +0.042 |  | -0.2 / -0.1 |  |
| MNQ | 15 | h16 | +0.007 | -0.072 .. +0.087 | +0.0010 | 0.86 / 0.86 / 0.86 | 0.868 |  |  | 9/16 | -0.108 | +0.122 |  | +0.5 / +0.2 |  |
| MNQ | 15 | eod * | +0.263 | -0.157 .. +0.682 | +0.0123 | 0.22 / 0.2 / 0.11 | 0.107 | 1 | 1 | 9/16 | +0.035 | +0.489 | False | +5.5 / +1.2 |  |
| MNQ | 60 | h1 | -0.002 | -0.013 .. +0.008 | -0.0017 | 0.66 / 0.67 / 0.67 | 0.678 |  |  | 7/16 | -0.016 | +0.011 |  | -0.4 / -0.4 |  |
| MNQ | 60 | h2 | -0.003 | -0.021 .. +0.016 | -0.0013 | 0.78 / 0.78 / 0.79 | 0.792 |  |  | 6/16 | -0.028 | +0.022 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h4 | +0.001 | -0.030 .. +0.033 | +0.0005 | 0.93 / 0.93 / 0.94 | 0.942 |  |  | 9/16 | -0.041 | +0.044 |  | +0.1 / +0.1 | 0.050 |
| MNQ | 60 | h8 | +0.016 | -0.037 .. +0.069 | +0.0040 | 0.55 / 0.55 / 0.58 | 0.593 |  |  | 8/16 | -0.045 | +0.077 |  | +1.0 / +0.6 |  |
| MNQ | 60 | h16 * | +0.056 | -0.023 .. +0.135 | +0.0105 | 0.17 / 0.16 / 0.19 | 0.193 | 1 | 1 | 9/16 | +0.011 | +0.101 | False | +2.7 / +1.4 |  |
| MNQ | 60 | eod | +0.047 | -0.036 .. +0.131 | +0.0085 | 0.27 / 0.26 / 0.29 | 0.288 |  |  | 8/16 | +0.014 | +0.081 |  | +2.2 / +1.1 |  |
| MYM | 5 | h1 * | -0.002 | -0.007 .. +0.002 | -0.0017 | 0.33 / 0.34 / 0.4 | 0.414 | 1 | 1 | 5/8 | n/a | -0.002 | False | -0.9 / -1.0 |  |
| MYM | 5 | h2 | -0.000 | -0.014 .. +0.013 | -0.0000 | 0.98 / 0.98 / 0.99 | 0.991 |  |  | 5/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h4 | +0.001 | -0.031 .. +0.034 | +0.0005 | 0.94 / 0.94 / 0.91 | 0.921 |  |  | 2/8 | n/a | +0.001 |  | +0.2 / +0.1 | 0.029 |
| MYM | 5 | h8 | -0.002 | -0.057 .. +0.052 | -0.0003 | 0.93 / 0.93 / 0.92 | 0.932 |  |  | 6/8 | n/a | -0.002 |  | -0.2 / -0.1 |  |
| MYM | 5 | h16 | -0.012 | -0.100 .. +0.077 | -0.0016 | 0.8 / 0.8 / 0.76 | 0.764 |  |  | 5/8 | n/a | -0.012 |  | -0.9 / -0.3 |  |
| MYM | 5 | eod | -0.178 | -1.008 .. +0.652 | -0.0061 | 0.67 / 0.67 / 0.62 | 0.619 |  |  | 6/8 | n/a | -0.178 |  | -3.1 / -0.4 |  |
| MYM | 15 | h1 | +0.000 | -0.007 .. +0.008 | +0.0003 | 0.9 / 0.91 / 0.92 | 0.924 |  |  | 2/8 | n/a | +0.000 |  | +0.1 / +0.1 |  |
| MYM | 15 | h2 | +0.004 | -0.015 .. +0.024 | +0.0016 | 0.67 / 0.67 / 0.69 | 0.707 |  |  | 2/8 | n/a | +0.004 |  | +0.5 / +0.4 |  |
| MYM | 15 | h4 | +0.009 | -0.031 .. +0.049 | +0.0020 | 0.66 / 0.67 / 0.67 | 0.695 |  |  | 4/8 | n/a | +0.009 |  | +0.6 / +0.4 | 0.060 |
| MYM | 15 | h8 | +0.014 | -0.065 .. +0.092 | +0.0023 | 0.73 / 0.74 / 0.7 | 0.738 |  |  | 4/8 | n/a | +0.014 |  | +0.7 / +0.3 |  |
| MYM | 15 | h16 * | +0.062 | -0.129 .. +0.254 | +0.0075 | 0.52 / 0.53 / 0.35 | 0.361 | 1 | 1 | 4/8 | n/a | +0.062 | False | +2.3 / +0.6 |  |
| MYM | 15 | eod | +0.116 | -0.465 .. +0.698 | +0.0058 | 0.7 / 0.7 / 0.58 | 0.591 |  |  | 2/8 | n/a | +0.116 |  | +1.8 / +0.4 |  |
| MYM | 60 | h1 | +0.002 | -0.012 .. +0.016 | +0.0013 | 0.8 / 0.81 / 0.82 | 0.822 |  |  | 4/8 | n/a | +0.002 |  | +0.2 / +0.3 |  |
| MYM | 60 | h2 | +0.006 | -0.018 .. +0.031 | +0.0030 | 0.62 / 0.64 / 0.67 | 0.662 |  |  | 4/8 | n/a | +0.006 |  | +0.5 / +0.5 |  |
| MYM | 60 | h4 * | +0.015 | -0.029 .. +0.059 | +0.0053 | 0.5 / 0.51 / 0.54 | 0.54 | 1 | 1 | 5/8 | n/a | +0.015 | False | +0.9 / +0.7 | 0.070 |
| MYM | 60 | h8 | +0.007 | -0.069 .. +0.083 | +0.0019 | 0.85 / 0.85 / 0.85 | 0.85 |  |  | 4/8 | n/a | +0.007 |  | +0.3 / +0.2 |  |
| MYM | 60 | h16 | -0.006 | -0.116 .. +0.103 | -0.0013 | 0.91 / 0.91 / 0.91 | 0.9 |  |  | 5/8 | n/a | -0.006 |  | -0.2 / -0.1 |  |
| MYM | 60 | eod | -0.003 | -0.120 .. +0.113 | -0.0006 | 0.95 / 0.95 / 0.95 | 0.949 |  |  | 5/8 | n/a | -0.003 |  | -0.1 / -0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.006 | -0.009 .. -0.003 | -1.2% | -0.009 | 1.3e-05 | 0.003 | 11/16 |
| MES | 5 | h2 | -0.006 | -0.011 .. -0.002 | -0.9% | -0.012 | 0.0065 |  | 10/16 |
| MES | 5 | h4 | -0.004 | -0.013 .. +0.004 | -0.4% | -0.012 | 0.31 |  | 8/16 |
| MES | 5 | h8 | -0.003 | -0.018 .. +0.012 | -0.2% | -0.010 | 0.71 |  | 7/16 |
| MES | 5 | h16 | -0.001 | -0.026 .. +0.025 | -0.0% | +0.001 | 0.97 |  | 7/16 |
| MES | 5 | eod | +0.089 | -0.224 .. +0.403 | +0.9% | +0.070 | 0.82 |  | 11/16 |
| MES | 15 | h1 * | -0.021 | -0.026 .. -0.016 | -4.1% | -0.045 | 3.8e-16 | 1.64e-13 | 14/16 |
| MES | 15 | h2 | -0.025 | -0.034 .. -0.015 | -3.4% | -0.056 | 6.4e-07 |  | 14/16 |
| MES | 15 | h4 | -0.032 | -0.050 .. -0.013 | -3.0% | -0.066 | 0.00071 |  | 13/16 |
| MES | 15 | h8 | -0.032 | -0.063 .. -0.001 | -2.1% | -0.069 | 0.04 |  | 8/16 |
| MES | 15 | h16 | -0.037 | -0.090 .. +0.017 | -1.6% | -0.085 | 0.18 |  | 9/16 |
| MES | 15 | eod | -0.037 | -0.278 .. +0.204 | -0.7% | -0.150 | 0.76 |  | 6/16 |
| MES | 60 | h1 * | -0.039 | -0.047 .. -0.031 | -7.6% | -0.079 | 4.6e-20 | 2.43e-17 | 15/16 |
| MES | 60 | h2 | -0.043 | -0.055 .. -0.030 | -5.8% | -0.096 | 2.1e-10 |  | 15/16 |
| MES | 60 | h4 | -0.058 | -0.079 .. -0.037 | -5.5% | -0.119 | 1.3e-07 |  | 14/16 |
| MES | 60 | h8 | -0.069 | -0.102 .. -0.036 | -4.6% | -0.143 | 3.7e-05 |  | 13/16 |
| MES | 60 | h16 | -0.055 | -0.100 .. -0.009 | -2.7% | -0.139 | 0.018 |  | 11/16 |
| MES | 60 | eod | -0.046 | -0.095 .. +0.004 | -2.1% | -0.134 | 0.072 |  | 9/16 |
| MNQ | 5 | h1 * | -0.007 | -0.011 .. -0.003 | -1.3% | -0.011 | 0.0002 | 0.0391 | 13/16 |
| MNQ | 5 | h2 | -0.011 | -0.019 .. -0.002 | -1.4% | -0.016 | 0.013 |  | 11/16 |
| MNQ | 5 | h4 | -0.012 | -0.029 .. +0.005 | -1.1% | -0.021 | 0.15 |  | 10/16 |
| MNQ | 5 | h8 | -0.013 | -0.043 .. +0.018 | -0.8% | -0.026 | 0.41 |  | 7/16 |
| MNQ | 5 | h16 | -0.014 | -0.064 .. +0.036 | -0.6% | -0.024 | 0.58 |  | 6/16 |
| MNQ | 5 | eod | +0.146 | -0.330 .. +0.621 | +1.2% | +0.109 | 0.8 |  | 10/16 |
| MNQ | 15 | h1 * | -0.023 | -0.030 .. -0.016 | -4.4% | -0.046 | 1.8e-10 | 5.67e-08 | 14/16 |
| MNQ | 15 | h2 | -0.031 | -0.049 .. -0.014 | -4.0% | -0.066 | 0.00042 |  | 13/16 |
| MNQ | 15 | h4 | -0.043 | -0.085 .. -0.001 | -3.8% | -0.090 | 0.046 |  | 12/16 |
| MNQ | 15 | h8 | -0.053 | -0.126 .. +0.020 | -3.2% | -0.126 | 0.15 |  | 10/16 |
| MNQ | 15 | h16 | -0.051 | -0.136 .. +0.034 | -2.0% | -0.174 | 0.24 |  | 7/16 |
| MNQ | 15 | eod | -0.128 | -0.527 .. +0.271 | -2.0% | -0.227 | 0.53 |  | 7/16 |
| MNQ | 60 | h1 * | -0.036 | -0.044 .. -0.027 | -6.7% | -0.076 | 1.4e-14 | 5.55e-12 | 14/16 |
| MNQ | 60 | h2 | -0.039 | -0.052 .. -0.026 | -5.1% | -0.089 | 1.1e-08 |  | 14/16 |
| MNQ | 60 | h4 | -0.051 | -0.072 .. -0.030 | -4.6% | -0.108 | 4e-06 |  | 15/16 |
| MNQ | 60 | h8 | -0.064 | -0.097 .. -0.030 | -4.0% | -0.128 | 0.00037 |  | 13/16 |
| MNQ | 60 | h16 | -0.042 | -0.093 .. +0.009 | -1.9% | -0.120 | 0.11 |  | 12/16 |
| MNQ | 60 | eod | -0.042 | -0.097 .. +0.013 | -1.8% | -0.119 | 0.13 |  | 12/16 |
| MYM | 5 | h1 * | -0.007 | -0.013 .. -0.002 | -1.4% | -0.011 | 0.0098 | 1 | 5/8 |
| MYM | 5 | h2 | -0.010 | -0.023 .. +0.003 | -1.3% | -0.017 | 0.13 |  | 5/8 |
| MYM | 5 | h4 | -0.014 | -0.045 .. +0.017 | -1.3% | -0.025 | 0.37 |  | 4/8 |
| MYM | 5 | h8 | -0.013 | -0.067 .. +0.041 | -0.8% | -0.029 | 0.63 |  | 3/8 |
| MYM | 5 | h16 | -0.009 | -0.092 .. +0.074 | -0.4% | -0.026 | 0.83 |  | 3/8 |
| MYM | 5 | eod | -0.082 | -0.637 .. +0.472 | -0.7% | -0.057 | 0.79 |  | 3/8 |
| MYM | 15 | h1 * | -0.025 | -0.035 .. -0.015 | -4.7% | -0.049 | 7.6e-07 | 0.000189 | 8/8 |
| MYM | 15 | h2 | -0.039 | -0.064 .. -0.014 | -5.1% | -0.075 | 0.0026 |  | 7/8 |
| MYM | 15 | h4 | -0.056 | -0.112 .. -0.000 | -5.0% | -0.111 | 0.054 |  | 5/8 |
| MYM | 15 | h8 | -0.083 | -0.173 .. +0.007 | -5.1% | -0.179 | 0.082 |  | 5/8 |
| MYM | 15 | h16 | -0.153 | -0.320 .. +0.013 | -6.2% | -0.292 | 0.082 |  | 6/8 |
| MYM | 15 | eod | -0.298 | -0.772 .. +0.177 | -4.9% | -0.505 | 0.24 |  | 7/8 |
| MYM | 60 | h1 * | -0.032 | -0.045 .. -0.019 | -6.1% | -0.068 | 1.2e-06 | 0.000292 | 7/8 |
| MYM | 60 | h2 | -0.038 | -0.058 .. -0.018 | -5.1% | -0.088 | 0.00021 |  | 7/8 |
| MYM | 60 | h4 | -0.061 | -0.093 .. -0.029 | -5.6% | -0.112 | 0.00018 |  | 7/8 |
| MYM | 60 | h8 | -0.073 | -0.122 .. -0.023 | -4.7% | -0.142 | 0.0043 |  | 6/8 |
| MYM | 60 | h16 | -0.062 | -0.127 .. +0.003 | -2.9% | -0.149 | 0.071 |  | 7/8 |
| MYM | 60 | eod | -0.055 | -0.123 .. +0.014 | -2.5% | -0.146 | 0.13 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.31 pts | -0.67 .. +0.05 | 0.091 |
| MES | 15 | -0.51 pts | -1.08 .. +0.06 | 0.08 |
| MES | 60 | -0.38 pts | -1.37 .. +0.61 | 0.47 |
| MNQ | 5 | -0.27 pts | -0.63 .. +0.08 | 0.15 |
| MNQ | 15 | -0.78 pts | -1.38 .. -0.17 | 0.012 |
| MNQ | 60 | -0.60 pts | -1.59 .. +0.39 | 0.25 |
| MYM | 5 | -0.37 pts | -0.86 .. +0.11 | 0.13 |
| MYM | 15 | -0.35 pts | -1.09 .. +0.40 | 0.38 |
| MYM | 60 | +0.31 pts | -1.08 .. +1.69 | 0.84 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom level | long | 463999 | +0.005 | 0.306 | +0.04 | -3.46 | -3.47 | -3.45 | -3.49 |
| MES | 5 | h2 | bottom level | long | 463999 | +0.008 | 0.306 | +0.05 | -3.45 | -3.45 | -3.44 | -3.48 |
| MES | 5 | h4 | bottom level | long | 463999 | +0.012 | 0.306 | +0.08 | -3.42 | -3.42 | -3.43 | -3.48 |
| MES | 5 | h8 | bottom level | long | 463999 | +0.025 | 0.306 | +0.15 | -3.35 | -3.30 | -3.39 | -3.46 |
| MES | 5 | h16 | bottom level | long | 463999 | +0.050 | 0.306 | +0.36 | -3.14 | -3.16 | -3.12 | -3.41 |
| MES | 5 | eod | top level | long | 572272 | +0.676 | 0.348 | +5.43 | +1.93 | +0.51 | +3.32 | -0.67 |
| MES | 15 | h1 | bottom level | long | 153107 | +0.007 | 0.182 | +0.05 | -3.45 | -3.44 | -3.46 | -3.54 |
| MES | 15 | h2 | top level | long | 189111 | +0.008 | 0.195 | +0.19 | -3.31 | -3.42 | -3.21 | -3.36 |
| MES | 15 | h4 | top level | long | 189111 | +0.020 | 0.195 | +0.41 | -3.09 | -3.27 | -2.91 | -3.24 |
| MES | 15 | h8 | bottom level | long | 153107 | +0.040 | 0.182 | +0.52 | -2.98 | -3.01 | -2.95 | -3.28 |
| MES | 15 | h16 | top level | long | 189111 | +0.100 | 0.195 | +1.73 | -1.77 | -2.48 | -1.09 | -2.53 |
| MES | 15 | eod | top level | long | 189111 | +0.378 | 0.195 | +5.55 | +2.05 | +0.44 | +3.63 | -0.18 |
| MES | 60 | h1 | bottom level | long | 37306 | +0.009 | 0.094 | +0.15 | -3.35 | -3.26 | -3.44 | -3.53 |
| MES | 60 | h2 | bottom level | long | 37306 | +0.021 | 0.094 | +0.52 | -2.98 | -2.97 | -2.99 | -3.42 |
| MES | 60 | h4 | top level | long | 46107 | +0.041 | 0.094 | +1.80 | -1.70 | -2.60 | -0.83 | -2.49 |
| MES | 60 | h8 | top level | long | 46107 | +0.081 | 0.094 | +3.61 | +0.11 | -1.38 | +1.56 | -1.46 |
| MES | 60 | h16 | top level | long | 46107 | +0.129 | 0.094 | +5.57 | +2.07 | +0.16 | +3.94 | -0.68 |
| MES | 60 | eod | top level | long | 46107 | +0.143 | 0.094 | +5.98 | +2.48 | +0.40 | +4.50 | -0.70 |
| MNQ | 5 | h1 | bottom level | long | 459925 | +0.004 | 0.121 | +0.02 | -1.98 | -1.98 | -1.98 | -1.99 |
| MNQ | 5 | h2 | bottom level | long | 459925 | +0.007 | 0.121 | +0.04 | -1.96 | -1.95 | -1.97 | -1.95 |
| MNQ | 5 | h4 | bottom level | long | 459925 | +0.011 | 0.121 | +0.06 | -1.94 | -1.92 | -1.97 | -1.90 |
| MNQ | 5 | h8 | bottom level | long | 459925 | +0.027 | 0.121 | +0.14 | -1.86 | -1.82 | -1.89 | -1.82 |
| MNQ | 5 | h16 | bottom level | long | 459925 | +0.058 | 0.121 | +0.30 | -1.70 | -1.67 | -1.73 | -1.78 |
| MNQ | 5 | eod | top level | long | 574597 | +1.009 | 0.141 | +8.00 | +6.00 | +1.37 | +10.58 | +2.17 |
| MNQ | 15 | h1 | bottom level | long | 152021 | +0.009 | 0.071 | +0.05 | -1.95 | -1.91 | -1.99 | -2.11 |
| MNQ | 15 | h2 | top level | long | 190041 | +0.013 | 0.078 | +0.32 | -1.68 | -1.90 | -1.46 | -1.79 |
| MNQ | 15 | h4 | bottom level | long | 152021 | +0.026 | 0.071 | +0.25 | -1.75 | -1.72 | -1.77 | -2.07 |
| MNQ | 15 | h8 | bottom level | long | 152021 | +0.049 | 0.071 | +0.40 | -1.60 | -1.45 | -1.75 | -2.14 |
| MNQ | 15 | h16 | top level | long | 190041 | +0.106 | 0.078 | +2.62 | +0.62 | -1.15 | +2.38 | -0.37 |
| MNQ | 15 | eod | top level | long | 190041 | +0.505 | 0.078 | +7.80 | +5.80 | +1.31 | +10.26 | +3.60 |
| MNQ | 60 | h1 | bottom level | long | 37039 | +0.011 | 0.036 | +0.22 | -1.78 | -1.70 | -1.87 | -2.01 |
| MNQ | 60 | h2 | bottom level | long | 37039 | +0.023 | 0.036 | +0.35 | -1.65 | -1.39 | -1.90 | -2.22 |
| MNQ | 60 | h4 | top level | long | 46372 | +0.043 | 0.037 | +2.56 | +0.56 | -1.24 | +2.36 | -0.56 |
| MNQ | 60 | h8 | top level | long | 46372 | +0.084 | 0.037 | +4.93 | +2.93 | -0.41 | +6.28 | +0.88 |
| MNQ | 60 | h16 | top level | long | 46372 | +0.152 | 0.037 | +7.40 | +5.40 | +1.01 | +9.79 | +2.10 |
| MNQ | 60 | eod | top level | long | 46372 | +0.167 | 0.037 | +7.66 | +5.66 | +1.29 | +10.03 | +1.67 |
| MYM | 5 | h1 | bottom level | long | 236477 | +0.001 | 0.160 | +0.04 | -1.96 | +nan | -1.96 | -1.96 |
| MYM | 5 | h2 | bottom level | long | 236477 | -0.004 | 0.160 | +0.06 | -1.94 | +nan | -1.94 | -1.90 |
| MYM | 5 | h4 | top level | long | 282562 | +0.002 | 0.181 | +0.09 | -1.91 | +nan | -1.91 | -1.98 |
| MYM | 5 | h8 | bottom level | long | 236477 | -0.023 | 0.160 | +0.15 | -1.85 | +nan | -1.85 | -1.58 |
| MYM | 5 | h16 | bottom level | long | 236477 | -0.023 | 0.160 | +0.39 | -1.61 | +nan | -1.61 | -1.34 |
| MYM | 5 | eod | bottom level | long | 236477 | +0.184 | 0.160 | +3.50 | +1.50 | +nan | +1.50 | +2.12 |
| MYM | 15 | h1 | top level | long | 93429 | +0.002 | 0.100 | +0.06 | -1.94 | +nan | -1.94 | -1.96 |
| MYM | 15 | h2 | top level | long | 93429 | +0.004 | 0.100 | +0.11 | -1.89 | +nan | -1.89 | -1.90 |
| MYM | 15 | h4 | top level | long | 93429 | +0.007 | 0.100 | +0.24 | -1.76 | +nan | -1.76 | -1.79 |
| MYM | 15 | h8 | top level | long | 93429 | +0.012 | 0.100 | +0.47 | -1.53 | +nan | -1.53 | -1.61 |
| MYM | 15 | h16 | top level | long | 93429 | +0.024 | 0.100 | +1.06 | -0.94 | +nan | -0.94 | -0.86 |
| MYM | 15 | eod | top level | long | 93429 | +0.145 | 0.100 | +4.18 | +2.18 | +nan | +2.18 | +1.92 |
| MYM | 60 | h1 | top level | long | 22759 | +0.005 | 0.047 | +0.32 | -1.68 | +nan | -1.68 | -1.81 |
| MYM | 60 | h2 | top level | long | 22759 | +0.010 | 0.047 | +0.58 | -1.42 | +nan | -1.42 | -1.60 |
| MYM | 60 | h4 | top level | long | 22759 | +0.021 | 0.047 | +1.32 | -0.68 | +nan | -0.68 | -1.12 |
| MYM | 60 | h8 | top level | long | 22759 | +0.031 | 0.047 | +2.50 | +0.50 | +nan | +0.50 | -0.38 |
| MYM | 60 | h16 | bottom level | long | 18896 | +0.028 | 0.047 | +2.06 | +0.06 | +nan | +0.06 | -1.14 |
| MYM | 60 | eod | bottom level | long | 18896 | +0.039 | 0.047 | +2.29 | +0.29 | +nan | +0.29 | -1.58 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.407 | -0.470 | -0.416 | -0.297 | -0.186 | +0.000 | -0.012 | -0.009 | -0.008 | -0.017 | -0.036 |
| MES | 15 | -1.458 | -1.286 | -0.942 | -0.601 | -0.349 | +0.000 | -0.008 | -0.009 | -0.012 | -0.021 | -0.002 |
| MES | 60 | -2.468 | -2.148 | -1.669 | -1.114 | -0.672 | +0.000 | -0.005 | -0.013 | -0.008 | -0.011 | +0.009 |
| MNQ | 5 | -0.463 | -0.519 | -0.461 | -0.324 | -0.198 | +0.000 | -0.001 | -0.005 | -0.007 | -0.013 | -0.017 |
| MNQ | 15 | -1.562 | -1.352 | -0.987 | -0.631 | -0.366 | +0.000 | -0.000 | +0.002 | +0.002 | +0.001 | +0.000 |
| MNQ | 60 | -2.644 | -2.223 | -1.711 | -1.133 | -0.681 | +0.000 | -0.003 | -0.009 | -0.018 | -0.018 | +0.081 |
| MYM | 5 | -0.348 | -0.436 | -0.413 | -0.295 | -0.180 | +0.000 | -0.003 | -0.001 | -0.004 | -0.020 | -0.026 |
| MYM | 15 | -1.409 | -1.239 | -0.914 | -0.582 | -0.336 | +0.000 | +0.005 | +0.008 | +0.015 | +0.018 | +0.073 |
| MYM | 60 | -2.627 | -2.238 | -1.695 | -1.105 | -0.659 | +0.000 | +0.003 | +0.001 | +0.002 | -0.021 | -0.031 |

## Calibration

- MES 5-min: 1036271 bars, 572272 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 189111 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 46107 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 574597 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 190041 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 46372 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 282562 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 93429 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 22759 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
