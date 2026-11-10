# Impact card: fam_breakout_short

bearish breakout patterns only (short side) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.013 R20 over the next 2 bars (10 min), p=0.01; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.044).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $0.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.019 R20 over the next 4 bars (1 h), p=0.57; we would catch an effect of 0.032 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.47).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.55 at recent bar sizes, 90% range up to $1.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.055 R20 over the next 8 bars (8 h), p=0.77; we would catch an effect of 0.062 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.07 at recent bar sizes, 90% range up to $6.40); about 60.3x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.009 R20 over the next 2 bars (10 min), p=0.37; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.45).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.23 at recent bar sizes, 90% range up to $0.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (30 min), p=0.63; we would catch an effect of 0.037 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.11).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.50 at recent bar sizes, 90% range up to $2.58); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.064 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.99 at recent bar sizes, 90% range up to $7.54); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.012 R20 over the next 2 bars (10 min), p=0.55; we would catch an effect of 0.030 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.44 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.161 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.013 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.050 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.52).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.27 at recent bar sizes, 90% range up to $1.37); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.021 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.087 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.29).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.89 at recent bar sizes, 90% range up to $4.06); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.009 | -0.015 .. -0.003 | -0.0036 | 0.0024 / 0.0016 / 0.0013 | 0.0026 |  |  | 13/16 | -0.008 | -0.010 |  | -3.2 / -3.0 |  |
| MES | 5 | h2 * | -0.013 | -0.022 .. -0.005 | -0.0036 | 0.0017 / 0.0012 / 0.00077 | 0.000781 | 0.279 | 0.378 | 12/16 | -0.015 | -0.011 | False | -3.3 / -3.1 |  |
| MES | 5 | h4 | -0.016 | -0.027 .. -0.004 | -0.0029 | 0.011 / 0.0095 / 0.0049 | 0.00443 |  |  | 12/16 | -0.017 | -0.014 |  | -2.8 / -2.5 | 0.017 |
| MES | 5 | h8 | -0.011 | -0.030 .. +0.008 | -0.0014 | 0.24 / 0.24 / 0.17 | 0.166 |  |  | 11/16 | -0.013 | -0.009 |  | -1.4 / -1.2 |  |
| MES | 5 | h16 | -0.010 | -0.042 .. +0.022 | -0.0009 | 0.54 / 0.55 / 0.39 | 0.381 |  |  | 10/16 | -0.009 | -0.011 |  | -0.9 / -0.6 |  |
| MES | 5 | eod | -0.001 | -0.395 .. +0.393 | -0.0000 | 1 / 1 / 0.99 | 0.987 |  |  | 6/16 | +0.031 | -0.033 |  | -0.0 / -0.0 |  |
| MES | 15 | h1 | -0.004 | -0.013 .. +0.006 | -0.0015 | 0.46 / 0.48 / 0.45 | 0.446 |  |  | 9/16 | -0.004 | -0.003 |  | -0.7 / -0.7 |  |
| MES | 15 | h2 | -0.006 | -0.020 .. +0.009 | -0.0015 | 0.45 / 0.46 / 0.42 | 0.426 |  |  | 8/16 | -0.012 | +0.001 |  | -0.8 / -0.7 |  |
| MES | 15 | h4 * | -0.019 | -0.041 .. +0.003 | -0.0035 | 0.091 / 0.094 / 0.058 | 0.0581 | 1 | 1 | 13/16 | -0.029 | -0.008 | False | -2.0 / -1.7 | 0.032 |
| MES | 15 | h8 | -0.023 | -0.060 .. +0.015 | -0.0030 | 0.23 / 0.22 / 0.1 | 0.102 |  |  | 10/16 | -0.044 | -0.002 |  | -1.6 / -1.2 |  |
| MES | 15 | h16 | -0.029 | -0.095 .. +0.037 | -0.0026 | 0.39 / 0.39 / 0.14 | 0.138 |  |  | 10/16 | -0.055 | -0.003 |  | -1.4 / -0.9 |  |
| MES | 15 | eod | -0.012 | -0.245 .. +0.221 | -0.0004 | 0.92 / 0.92 / 0.81 | 0.803 |  |  | 6/16 | +0.093 | -0.117 |  | -0.3 / -0.1 |  |
| MES | 60 | h1 | -0.007 | -0.027 .. +0.014 | -0.0028 | 0.51 / 0.51 / 0.5 | 0.511 |  |  | 8/16 | -0.011 | -0.003 |  | -0.6 / -0.7 |  |
| MES | 60 | h2 | -0.005 | -0.036 .. +0.026 | -0.0014 | 0.75 / 0.75 / 0.72 | 0.716 |  |  | 9/16 | +0.012 | -0.022 |  | -0.3 / -0.3 |  |
| MES | 60 | h4 | -0.013 | -0.055 .. +0.030 | -0.0025 | 0.56 / 0.57 / 0.49 | 0.489 |  |  | 10/16 | -0.000 | -0.025 |  | -0.6 / -0.6 | 0.062 |
| MES | 60 | h8 * | -0.055 | -0.122 .. +0.013 | -0.0080 | 0.11 / 0.13 / 0.032 | 0.0388 | 1 | 1 | 13/16 | -0.017 | -0.092 | False | -1.9 / -1.6 |  |
| MES | 60 | h16 | -0.061 | -0.154 .. +0.033 | -0.0068 | 0.2 / 0.22 / 0.061 | 0.0641 |  |  | 12/16 | -0.018 | -0.104 |  | -1.7 / -1.3 |  |
| MES | 60 | eod | -0.054 | -0.152 .. +0.043 | -0.0057 | 0.28 / 0.29 / 0.1 | 0.103 |  |  | 12/16 | +0.000 | -0.109 |  | -1.5 / -1.1 |  |
| MNQ | 5 | h1 | -0.005 | -0.011 .. -0.000 | -0.0022 | 0.039 / 0.038 / 0.063 | 0.0597 |  |  | 10/16 | -0.002 | -0.009 |  | -2.2 / -2.1 |  |
| MNQ | 5 | h2 * | -0.009 | -0.016 .. -0.001 | -0.0021 | 0.026 / 0.028 / 0.062 | 0.0623 | 1 | 0.997 | 10/16 | -0.004 | -0.013 | False | -2.4 / -2.2 |  |
| MNQ | 5 | h4 | -0.009 | -0.020 .. +0.002 | -0.0015 | 0.1 / 0.11 / 0.17 | 0.165 |  |  | 11/16 | -0.003 | -0.015 |  | -1.8 / -1.6 | 0.019 |
| MNQ | 5 | h8 | -0.004 | -0.022 .. +0.015 | -0.0004 | 0.69 / 0.69 / 0.75 | 0.74 |  |  | 7/16 | -0.004 | -0.004 |  | -0.5 / -0.4 |  |
| MNQ | 5 | h16 | +0.007 | -0.027 .. +0.041 | +0.0005 | 0.68 / 0.68 / 0.54 | 0.531 |  |  | 11/16 | +0.025 | -0.011 |  | +0.6 / +0.4 |  |
| MNQ | 5 | eod | +0.080 | -0.384 .. +0.544 | +0.0013 | 0.74 / 0.74 / 0.22 | 0.224 |  |  | 13/16 | +0.254 | -0.092 |  | +1.4 / +0.3 |  |
| MNQ | 15 | h1 | -0.008 | -0.017 .. +0.001 | -0.0028 | 0.087 / 0.082 / 0.13 | 0.132 |  |  | 12/16 | -0.012 | -0.004 |  | -1.7 / -1.7 |  |
| MNQ | 15 | h2 * | -0.011 | -0.024 .. +0.002 | -0.0024 | 0.1 / 0.1 / 0.19 | 0.178 | 1 | 0.999 | 11/16 | -0.019 | -0.003 | False | -1.7 / -1.6 |  |
| MNQ | 15 | h4 | -0.021 | -0.042 .. +0.000 | -0.0027 | 0.054 / 0.057 / 0.16 | 0.155 |  |  | 11/16 | -0.017 | -0.025 |  | -2.2 / -1.9 | 0.037 |
| MNQ | 15 | h8 | -0.027 | -0.062 .. +0.009 | -0.0026 | 0.15 / 0.15 / 0.15 | 0.151 |  |  | 13/16 | -0.023 | -0.030 |  | -1.9 / -1.4 |  |
| MNQ | 15 | h16 | -0.036 | -0.101 .. +0.029 | -0.0029 | 0.28 / 0.28 / 0.1 | 0.0974 |  |  | 10/16 | -0.016 | -0.057 |  | -1.8 / -1.1 |  |
| MNQ | 15 | eod | +0.044 | -0.212 .. +0.301 | +0.0012 | 0.74 / 0.74 / 0.48 | 0.487 |  |  | 10/16 | +0.161 | -0.073 |  | +0.9 / +0.3 |  |
| MNQ | 60 | h1 | -0.006 | -0.028 .. +0.016 | -0.0025 | 0.58 / 0.59 / 0.55 | 0.548 |  |  | 11/16 | -0.014 | +0.002 |  | -0.5 / -0.5 |  |
| MNQ | 60 | h2 * | -0.011 | -0.043 .. +0.021 | -0.0032 | 0.51 / 0.52 / 0.43 | 0.435 | 1 | 1 | 11/16 | -0.001 | -0.021 | False | -0.7 / -0.7 |  |
| MNQ | 60 | h4 | -0.013 | -0.058 .. +0.032 | -0.0026 | 0.57 / 0.58 / 0.48 | 0.473 |  |  | 11/16 | +0.004 | -0.030 |  | -0.6 / -0.6 | 0.064 |
| MNQ | 60 | h8 | -0.021 | -0.092 .. +0.050 | -0.0031 | 0.56 / 0.58 / 0.42 | 0.424 |  |  | 10/16 | -0.007 | -0.035 |  | -0.7 / -0.6 |  |
| MNQ | 60 | h16 | -0.031 | -0.136 .. +0.075 | -0.0035 | 0.57 / 0.57 / 0.36 | 0.359 |  |  | 12/16 | -0.015 | -0.046 |  | -0.9 / -0.6 |  |
| MNQ | 60 | eod | -0.029 | -0.137 .. +0.078 | -0.0032 | 0.59 / 0.61 / 0.39 | 0.397 |  |  | 11/16 | -0.012 | -0.047 |  | -0.8 / -0.5 |  |
| MYM | 5 | h1 | -0.007 | -0.014 .. +0.000 | -0.0026 | 0.065 / 0.066 / 0.11 | 0.107 |  |  | 6/8 | n/a | -0.007 |  | -1.9 / -1.8 |  |
| MYM | 5 | h2 * | -0.012 | -0.023 .. -0.002 | -0.0028 | 0.025 / 0.02 / 0.063 | 0.0569 | 1 | 0.989 | 6/8 | n/a | -0.012 | False | -2.5 / -2.2 |  |
| MYM | 5 | h4 | -0.017 | -0.033 .. -0.002 | -0.0025 | 0.029 / 0.028 / 0.084 | 0.0722 |  |  | 5/8 | n/a | -0.017 |  | -2.5 / -2.2 | 0.030 |
| MYM | 5 | h8 | -0.014 | -0.040 .. +0.012 | -0.0014 | 0.3 / 0.3 / 0.31 | 0.31 |  |  | 5/8 | n/a | -0.014 |  | -1.4 / -1.0 |  |
| MYM | 5 | h16 | -0.008 | -0.055 .. +0.039 | -0.0006 | 0.74 / 0.74 / 0.63 | 0.632 |  |  | 3/8 | n/a | -0.008 |  | -0.5 / -0.3 |  |
| MYM | 5 | eod | +0.107 | -0.540 .. +0.754 | +0.0019 | 0.75 / 0.75 / 0.2 | 0.204 |  |  | 6/8 | n/a | +0.107 |  | +1.4 / +0.3 |  |
| MYM | 15 | h1 | -0.006 | -0.018 .. +0.006 | -0.0022 | 0.35 / 0.36 / 0.43 | 0.409 |  |  | 4/8 | n/a | -0.006 |  | -0.9 / -0.9 |  |
| MYM | 15 | h2 | +0.002 | -0.016 .. +0.020 | +0.0005 | 0.82 / 0.82 / 0.87 | 0.858 |  |  | 5/8 | n/a | +0.002 |  | +0.2 / +0.2 |  |
| MYM | 15 | h4 * | -0.013 | -0.042 .. +0.016 | -0.0017 | 0.39 / 0.39 / 0.52 | 0.525 | 1 | 1 | 4/8 | n/a | -0.013 | False | -1.0 / -0.9 | 0.050 |
| MYM | 15 | h8 | -0.012 | -0.062 .. +0.038 | -0.0012 | 0.64 / 0.63 / 0.63 | 0.617 |  |  | 4/8 | n/a | -0.012 |  | -0.7 / -0.5 |  |
| MYM | 15 | h16 | -0.009 | -0.103 .. +0.085 | -0.0007 | 0.85 / 0.84 / 0.79 | 0.787 |  |  | 4/8 | n/a | -0.009 |  | -0.3 / -0.2 |  |
| MYM | 15 | eod | +0.002 | -0.353 .. +0.356 | +0.0000 | 0.99 / 0.99 / 0.98 | 0.988 |  |  | 3/8 | n/a | +0.002 |  | +0.0 / +0.0 |  |
| MYM | 60 | h1 * | +0.021 | -0.008 .. +0.050 | +0.0092 | 0.16 / 0.17 / 0.13 | 0.121 | 1 | 1 | 5/8 | n/a | +0.021 | False | +1.4 / +1.4 |  |
| MYM | 60 | h2 | -0.000 | -0.041 .. +0.041 | -0.0000 | 1 / 1 / 1 | 0.997 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 60 | h4 | +0.007 | -0.053 .. +0.068 | +0.0016 | 0.81 / 0.81 / 0.76 | 0.755 |  |  | 6/8 | n/a | +0.007 |  | +0.3 / +0.2 | 0.087 |
| MYM | 60 | h8 | +0.012 | -0.088 .. +0.113 | +0.0020 | 0.81 / 0.81 / 0.71 | 0.721 |  |  | 5/8 | n/a | +0.012 |  | +0.3 / +0.2 |  |
| MYM | 60 | h16 | -0.022 | -0.160 .. +0.116 | -0.0026 | 0.76 / 0.76 / 0.6 | 0.61 |  |  | 4/8 | n/a | -0.022 |  | -0.5 / -0.3 |  |
| MYM | 60 | eod | -0.016 | -0.159 .. +0.126 | -0.0019 | 0.82 / 0.83 / 0.7 | 0.705 |  |  | 3/8 | n/a | -0.016 |  | -0.3 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.007 | +0.002 .. +0.012 | +1.4% | +0.018 | 0.0074 | 1 | 12/16 |
| MES | 5 | h2 | +0.008 | +0.002 .. +0.014 | +1.2% | +0.017 | 0.0077 |  | 13/16 |
| MES | 5 | h4 | +0.009 | +0.001 .. +0.017 | +0.9% | +0.015 | 0.13 |  | 10/16 |
| MES | 5 | h8 | +0.008 | -0.005 .. +0.021 | +0.5% | +0.017 | 0.44 |  | 12/16 |
| MES | 5 | h16 | +0.012 | -0.006 .. +0.031 | +0.6% | +0.011 | 0.47 |  | 12/16 |
| MES | 5 | eod | -0.096 | -0.260 .. +0.068 | -1.0% | -0.229 | 0.25 |  | 7/16 |
| MES | 15 | h1 * | +0.007 | -0.000 .. +0.013 | +1.3% | +0.013 | 0.079 | 1 | 11/16 |
| MES | 15 | h2 | +0.010 | -0.001 .. +0.020 | +1.3% | +0.014 | 0.18 |  | 8/16 |
| MES | 15 | h4 | +0.004 | -0.012 .. +0.019 | +0.4% | +0.011 | 0.76 |  | 11/16 |
| MES | 15 | h8 | -0.006 | -0.028 .. +0.016 | -0.4% | -0.004 | 0.61 |  | 9/16 |
| MES | 15 | h16 | +0.004 | -0.033 .. +0.041 | +0.2% | -0.011 | 0.99 |  | 9/16 |
| MES | 15 | eod | +0.017 | -0.109 .. +0.144 | +0.3% | -0.054 | 0.8 |  | 11/16 |
| MES | 60 | h1 | +0.007 | -0.008 .. +0.022 | +1.4% | +0.024 | 0.34 |  | 8/16 |
| MES | 60 | h2 | +0.003 | -0.017 .. +0.024 | +0.4% | +0.026 | 0.76 |  | 11/16 |
| MES | 60 | h4 | +0.004 | -0.024 .. +0.032 | +0.4% | +0.024 | 0.79 |  | 9/16 |
| MES | 60 | h8 | +0.014 | -0.022 .. +0.050 | +0.9% | +0.053 | 0.46 |  | 10/16 |
| MES | 60 | h16 | -0.024 | -0.068 .. +0.019 | -1.2% | +0.017 | 0.35 |  | 9/16 |
| MES | 60 | eod * | -0.027 | -0.072 .. +0.018 | -1.2% | +0.013 | 0.32 | 1 | 10/16 |
| MNQ | 5 | h1 * | +0.006 | +0.002 .. +0.010 | +1.1% | +0.015 | 0.074 | 1 | 12/16 |
| MNQ | 5 | h2 | +0.006 | -0.001 .. +0.013 | +0.8% | +0.012 | 0.15 |  | 9/16 |
| MNQ | 5 | h4 | +0.006 | -0.007 .. +0.018 | +0.5% | +0.005 | 0.66 |  | 10/16 |
| MNQ | 5 | h8 | +0.005 | -0.019 .. +0.029 | +0.3% | +0.001 | 0.92 |  | 11/16 |
| MNQ | 5 | h16 | +0.005 | -0.038 .. +0.048 | +0.2% | -0.006 | 1 |  | 10/16 |
| MNQ | 5 | eod | -0.082 | -0.323 .. +0.158 | -0.7% | -0.277 | 0.5 |  | 6/16 |
| MNQ | 15 | h1 * | +0.010 | +0.002 .. +0.017 | +1.8% | +0.011 | 0.019 | 1 | 11/16 |
| MNQ | 15 | h2 | +0.011 | -0.003 .. +0.026 | +1.5% | +0.013 | 0.19 |  | 13/16 |
| MNQ | 15 | h4 | +0.009 | -0.020 .. +0.039 | +0.8% | +0.009 | 0.59 |  | 11/16 |
| MNQ | 15 | h8 | +0.007 | -0.036 .. +0.051 | +0.4% | -0.002 | 0.74 |  | 10/16 |
| MNQ | 15 | h16 | +0.004 | -0.044 .. +0.053 | +0.2% | -0.027 | 0.86 |  | 12/16 |
| MNQ | 15 | eod | -0.003 | -0.195 .. +0.190 | -0.0% | -0.050 | 0.98 |  | 4/16 |
| MNQ | 60 | h1 | +0.011 | -0.005 .. +0.026 | +2.0% | +0.032 | 0.19 |  | 13/16 |
| MNQ | 60 | h2 | +0.013 | -0.009 .. +0.035 | +1.7% | +0.038 | 0.25 |  | 10/16 |
| MNQ | 60 | h4 | +0.009 | -0.019 .. +0.037 | +0.8% | +0.039 | 0.53 |  | 10/16 |
| MNQ | 60 | h8 * | +0.027 | -0.010 .. +0.064 | +1.7% | +0.053 | 0.19 | 1 | 9/16 |
| MNQ | 60 | h16 | +0.021 | -0.022 .. +0.065 | +1.0% | +0.039 | 0.35 |  | 11/16 |
| MNQ | 60 | eod | +0.018 | -0.027 .. +0.063 | +0.8% | +0.040 | 0.45 |  | 14/16 |
| MYM | 5 | h1 * | +0.009 | +0.003 .. +0.015 | +1.7% | +0.021 | 0.34 | 1 | 7/8 |
| MYM | 5 | h2 | +0.004 | -0.006 .. +0.015 | +0.6% | +0.013 | 0.82 |  | 5/8 |
| MYM | 5 | h4 | +0.001 | -0.020 .. +0.023 | +0.1% | +0.008 | 0.91 |  | 5/8 |
| MYM | 5 | h8 | +0.002 | -0.036 .. +0.040 | +0.1% | +0.006 | 0.93 |  | 6/8 |
| MYM | 5 | h16 | -0.008 | -0.061 .. +0.046 | -0.3% | -0.012 | 0.78 |  | 1/8 |
| MYM | 5 | eod | -0.055 | -0.307 .. +0.196 | -0.5% | -0.211 | 0.67 |  | 4/8 |
| MYM | 15 | h1 * | +0.012 | +0.001 .. +0.023 | +2.3% | +0.012 | 0.086 | 1 | 6/8 |
| MYM | 15 | h2 | +0.010 | -0.009 .. +0.028 | +1.3% | +0.013 | 0.68 |  | 6/8 |
| MYM | 15 | h4 | +0.011 | -0.025 .. +0.046 | +0.9% | +0.010 | 0.98 |  | 6/8 |
| MYM | 15 | h8 | -0.006 | -0.059 .. +0.048 | -0.3% | -0.006 | 0.84 |  | 4/8 |
| MYM | 15 | h16 | +0.005 | -0.089 .. +0.100 | +0.2% | -0.009 | 0.96 |  | 5/8 |
| MYM | 15 | eod | +0.015 | -0.224 .. +0.255 | +0.3% | -0.008 | 0.91 |  | 7/8 |
| MYM | 60 | h1 * | +0.020 | +0.000 .. +0.041 | +3.9% | +0.034 | 0.049 | 1 | 6/8 |
| MYM | 60 | h2 | -0.002 | -0.030 .. +0.026 | -0.2% | +0.023 | 0.9 |  | 4/8 |
| MYM | 60 | h4 | +0.019 | -0.018 .. +0.057 | +1.8% | +0.040 | 0.3 |  | 6/8 |
| MYM | 60 | h8 | +0.017 | -0.036 .. +0.070 | +1.1% | +0.049 | 0.53 |  | 4/8 |
| MYM | 60 | h16 | -0.005 | -0.070 .. +0.061 | -0.2% | +0.028 | 0.94 |  | 6/8 |
| MYM | 60 | eod | -0.010 | -0.075 .. +0.055 | -0.5% | +0.022 | 0.91 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.29 pts | -0.68 .. +0.11 | 0.16 |
| MES | 15 | -0.36 pts | -1.02 .. +0.29 | 0.28 |
| MES | 60 | -0.53 pts | -1.72 .. +0.67 | 0.39 |
| MNQ | 5 | -0.31 pts | -0.64 .. +0.02 | 0.071 |
| MNQ | 15 | -0.22 pts | -0.81 .. +0.36 | 0.45 |
| MNQ | 60 | +0.10 pts | -1.11 .. +1.30 | 0.97 |
| MYM | 5 | -0.60 pts | -1.11 .. -0.09 | 0.02 |
| MYM | 15 | -0.56 pts | -1.37 .. +0.26 | 0.18 |
| MYM | 60 | -0.46 pts | -2.06 .. +1.14 | 0.57 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 70780 | +0.021 | 0.251 | +0.24 | -3.26 | -3.33 | -3.22 | -3.41 |
| MES | 5 | h2 | event | against signal | 70780 | +0.033 | 0.251 | +0.39 | -3.11 | -3.19 | -3.07 | -3.35 |
| MES | 5 | h4 | event | against signal | 70780 | +0.041 | 0.251 | +0.47 | -3.03 | -3.11 | -2.99 | -3.30 |
| MES | 5 | h8 | event | against signal | 70780 | +0.045 | 0.251 | +0.54 | -2.96 | -3.02 | -2.93 | -3.28 |
| MES | 5 | h16 | event | against signal | 70780 | +0.066 | 0.251 | +0.71 | -2.79 | -2.83 | -2.76 | -3.27 |
| MES | 5 | eod | event | against signal | 70780 | +0.410 | 0.251 | +4.99 | +1.49 | +0.09 | +2.34 | +1.24 |
| MES | 15 | h1 | event | against signal | 27575 | +0.018 | 0.162 | +0.27 | -3.23 | -3.31 | -3.17 | -3.51 |
| MES | 15 | h2 | event | against signal | 27575 | +0.026 | 0.162 | +0.43 | -3.07 | -3.18 | -2.98 | -3.41 |
| MES | 15 | h4 | event | against signal | 27575 | +0.050 | 0.162 | +0.66 | -2.84 | -2.85 | -2.82 | -3.30 |
| MES | 15 | h8 | event | against signal | 27575 | +0.076 | 0.162 | +1.12 | -2.38 | -2.42 | -2.35 | -3.08 |
| MES | 15 | h16 | event | against signal | 27575 | +0.118 | 0.162 | +1.86 | -1.64 | -1.83 | -1.51 | -2.57 |
| MES | 15 | eod | event | against signal | 27575 | +0.253 | 0.162 | +4.82 | +1.32 | -0.74 | +2.77 | +0.72 |
| MES | 60 | h1 | event | against signal | 6556 | +0.014 | 0.088 | +0.68 | -2.82 | -3.24 | -2.48 | -2.95 |
| MES | 60 | h2 | event | against signal | 6556 | +0.025 | 0.088 | +1.42 | -2.08 | -3.51 | -0.92 | -2.58 |
| MES | 60 | h4 | event | against signal | 6556 | +0.057 | 0.088 | +2.81 | -0.69 | -2.77 | +1.00 | -1.91 |
| MES | 60 | h8 | event | against signal | 6556 | +0.130 | 0.088 | +5.18 | +1.68 | -1.66 | +4.39 | -0.34 |
| MES | 60 | h16 | event | against signal | 6556 | +0.162 | 0.088 | +6.04 | +2.54 | -1.25 | +5.63 | -0.00 |
| MES | 60 | eod | event | against signal | 6556 | +0.168 | 0.088 | +6.17 | +2.67 | -1.23 | +5.84 | -0.24 |
| MNQ | 5 | h1 | event | against signal | 101657 | +0.013 | 0.112 | +0.20 | -1.80 | -1.92 | -1.70 | -1.90 |
| MNQ | 5 | h2 | event | against signal | 101657 | +0.024 | 0.112 | +0.40 | -1.60 | -1.84 | -1.43 | -1.76 |
| MNQ | 5 | h4 | event | against signal | 101657 | +0.029 | 0.112 | +0.45 | -1.55 | -1.78 | -1.37 | -1.66 |
| MNQ | 5 | h8 | event | against signal | 101657 | +0.033 | 0.112 | +0.41 | -1.59 | -1.67 | -1.54 | -1.67 |
| MNQ | 5 | h16 | event | with signal | 101657 | -0.051 | 0.112 | -0.60 | -2.60 | -2.38 | -2.76 | -2.38 |
| MNQ | 5 | eod | event | with signal | 101657 | -0.607 | 0.112 | -5.56 | -7.56 | -4.86 | -9.54 | -7.84 |
| MNQ | 15 | h1 | event | against signal | 35084 | +0.019 | 0.069 | +0.37 | -1.63 | -1.87 | -1.43 | -1.87 |
| MNQ | 15 | h2 | event | against signal | 35084 | +0.026 | 0.069 | +0.44 | -1.56 | -1.70 | -1.44 | -1.78 |
| MNQ | 15 | h4 | event | against signal | 35084 | +0.048 | 0.069 | +0.89 | -1.11 | -1.64 | -0.68 | -1.49 |
| MNQ | 15 | h8 | event | against signal | 35084 | +0.076 | 0.069 | +1.67 | -0.33 | -1.30 | +0.46 | -0.95 |
| MNQ | 15 | h16 | event | against signal | 35084 | +0.132 | 0.069 | +3.04 | +1.04 | -0.69 | +2.44 | +0.22 |
| MNQ | 15 | eod | event | with signal | 35084 | -0.295 | 0.069 | -5.99 | -7.99 | -4.68 | -10.68 | -7.79 |
| MNQ | 60 | h1 | event | against signal | 7520 | +0.012 | 0.036 | +0.06 | -1.94 | -1.89 | -1.99 | -2.01 |
| MNQ | 60 | h2 | event | against signal | 7520 | +0.031 | 0.036 | +1.34 | -0.66 | -1.84 | +0.42 | -1.18 |
| MNQ | 60 | h4 | event | against signal | 7520 | +0.057 | 0.036 | +3.33 | +1.33 | -1.52 | +3.95 | +0.04 |
| MNQ | 60 | h8 | event | against signal | 7520 | +0.104 | 0.036 | +3.80 | +1.80 | -0.62 | +4.03 | -0.61 |
| MNQ | 60 | h16 | event | against signal | 7520 | +0.157 | 0.036 | +5.08 | +3.08 | -0.03 | +5.93 | -0.25 |
| MNQ | 60 | eod | event | against signal | 7520 | +0.169 | 0.036 | +5.37 | +3.37 | +0.24 | +6.23 | -0.36 |
| MYM | 5 | h1 | event | against signal | 54054 | +0.014 | 0.161 | +0.12 | -1.88 | +nan | -1.88 | -1.97 |
| MYM | 5 | h2 | event | against signal | 54054 | +0.022 | 0.161 | +0.21 | -1.79 | +nan | -1.79 | -1.91 |
| MYM | 5 | h4 | event | against signal | 54054 | +0.030 | 0.161 | +0.26 | -1.74 | +nan | -1.74 | -1.88 |
| MYM | 5 | h8 | event | against signal | 54054 | +0.030 | 0.161 | +0.35 | -1.65 | +nan | -1.65 | -1.84 |
| MYM | 5 | h16 | event | against signal | 54054 | +0.039 | 0.161 | +0.53 | -1.47 | +nan | -1.47 | -1.86 |
| MYM | 5 | eod | event | with signal | 54054 | -0.193 | 0.161 | -3.46 | -5.46 | +nan | -5.46 | -3.80 |
| MYM | 15 | h1 | event | against signal | 18384 | +0.014 | 0.095 | +0.27 | -1.73 | +nan | -1.73 | -1.88 |
| MYM | 15 | h2 | event | with signal | 18384 | -0.005 | 0.095 | -0.19 | -2.19 | +nan | -2.19 | -2.10 |
| MYM | 15 | h4 | event | against signal | 18384 | +0.024 | 0.095 | +0.52 | -1.48 | +nan | -1.48 | -1.62 |
| MYM | 15 | h8 | event | against signal | 18384 | +0.030 | 0.095 | +0.75 | -1.25 | +nan | -1.25 | -1.46 |
| MYM | 15 | h16 | event | against signal | 18384 | +0.032 | 0.095 | +1.05 | -0.95 | +nan | -0.95 | -1.16 |
| MYM | 15 | eod | event | with signal | 18384 | -0.148 | 0.095 | -3.77 | -5.77 | +nan | -5.77 | -4.79 |
| MYM | 60 | h1 | event | with signal | 3995 | +0.021 | 0.048 | +0.50 | -1.50 | +nan | -1.50 | -1.54 |
| MYM | 60 | h2 | event | against signal | 3995 | +0.009 | 0.048 | +0.98 | -1.02 | +nan | -1.02 | -1.38 |
| MYM | 60 | h4 | event | with signal | 3995 | -0.014 | 0.048 | -1.82 | -3.82 | +nan | -3.82 | -2.97 |
| MYM | 60 | h8 | event | with signal | 3995 | -0.022 | 0.048 | -2.09 | -4.09 | +nan | -4.09 | -2.73 |
| MYM | 60 | h16 | event | against signal | 3995 | +0.058 | 0.048 | +4.02 | +2.02 | +nan | +2.02 | +0.52 |
| MYM | 60 | eod | event | against signal | 3995 | +0.060 | 0.048 | +4.02 | +2.02 | +nan | +2.02 | +0.13 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.590 | -0.647 | -0.724 | -0.757 | -0.742 | +0.000 | -0.035 | -0.044 | -0.047 | -0.040 | -0.037 |
| MES | 15 | -0.609 | -0.636 | -0.709 | -0.748 | -0.739 | +0.000 | -0.018 | -0.021 | -0.034 | -0.040 | -0.063 |
| MES | 60 | -0.880 | -0.699 | -0.715 | -0.728 | -0.767 | +0.000 | -0.007 | -0.007 | -0.033 | -0.126 | -0.085 |
| MNQ | 5 | -0.582 | -0.638 | -0.707 | -0.746 | -0.733 | +0.000 | -0.020 | -0.027 | -0.026 | -0.014 | +0.001 |
| MNQ | 15 | -0.602 | -0.644 | -0.701 | -0.731 | -0.729 | +0.000 | -0.017 | -0.021 | -0.029 | -0.033 | -0.062 |
| MNQ | 60 | -1.001 | -0.763 | -0.729 | -0.727 | -0.758 | +0.000 | -0.004 | -0.012 | -0.028 | -0.067 | +0.086 |
| MYM | 5 | -0.577 | -0.628 | -0.694 | -0.724 | -0.715 | +0.000 | -0.022 | -0.032 | -0.045 | -0.048 | -0.052 |
| MYM | 15 | -0.593 | -0.613 | -0.663 | -0.711 | -0.710 | +0.000 | -0.019 | -0.015 | -0.030 | -0.040 | -0.076 |
| MYM | 60 | -0.893 | -0.721 | -0.684 | -0.698 | -0.734 | +0.000 | +0.021 | -0.001 | -0.017 | -0.059 | -0.086 |

## Calibration

- MES 5-min: 1036271 bars, 70780 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 27575 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 6556 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 101657 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 35084 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 7520 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 54054 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 18384 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 3995 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39387 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
