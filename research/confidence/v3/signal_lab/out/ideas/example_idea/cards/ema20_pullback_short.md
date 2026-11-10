# Impact card: ema20_pullback_short

down-stack EMA8<20<50, bar touches EMA20 and closes below EMA8 -> short

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.299 R20 over the rest of the session (to 16:45), p=0.58; we would catch an effect of 0.059 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.43).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $8.91 at recent bar sizes, 90% range up to $2.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.046 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.123 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.06 at recent bar sizes, 90% range up to $9.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best -0.021 R20 over the next 1 bar (15 min), p=0.28; we would catch an effect of 0.072 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.026 R20, CONFIRMED, q=0.022, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.07 at recent bar sizes, 90% range up to $3.91); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.084 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.144 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.65).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $9.02 at recent bar sizes, 90% range up to $22.46); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best -0.027 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.095 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.58 at recent bar sizes, 90% range up to $2.95); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.085 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.177 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.92 at recent bar sizes, 90% range up to $15.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.011 | -0.026 .. +0.005 | -0.0026 | 0.18 / 0.19 / 0.2 | 0.199 |  |  | 11/16 | -0.010 | -0.011 |  | -1.3 / -1.3 |  |
| MES | 15 | h2 | +0.001 | -0.024 .. +0.026 | +0.0001 | 0.94 / 0.94 / 0.95 | 0.938 |  |  | 8/16 | +0.007 | -0.005 |  | +0.1 / +0.1 |  |
| MES | 15 | h4 | -0.018 | -0.059 .. +0.022 | -0.0021 | 0.38 / 0.39 / 0.39 | 0.385 |  |  | 9/16 | -0.028 | -0.009 |  | -1.1 / -0.9 | 0.059 |
| MES | 15 | h8 | -0.035 | -0.102 .. +0.032 | -0.0028 | 0.3 / 0.31 / 0.28 | 0.274 |  |  | 11/16 | -0.062 | -0.009 |  | -1.5 / -1.0 |  |
| MES | 15 | h16 | -0.023 | -0.133 .. +0.087 | -0.0012 | 0.68 / 0.7 / 0.66 | 0.654 |  |  | 9/16 | -0.063 | +0.017 |  | -0.7 / -0.4 |  |
| MES | 15 | eod * | -0.299 | -0.651 .. +0.054 | -0.0063 | 0.097 / 0.087 / 0.056 | 0.0586 | 1 | 0.505 | 14/16 | -0.104 | -0.492 | False | -3.8 / -1.7 |  |
| MES | 60 | h1 | +0.001 | -0.036 .. +0.039 | +0.0002 | 0.94 / 0.94 / 0.94 | 0.937 |  |  | 10/16 | +0.001 | +0.002 |  | +0.1 / +0.1 |  |
| MES | 60 | h2 | -0.011 | -0.071 .. +0.048 | -0.0020 | 0.71 / 0.71 / 0.7 | 0.699 |  |  | 8/16 | -0.003 | -0.019 |  | -0.4 / -0.4 |  |
| MES | 60 | h4 | -0.001 | -0.091 .. +0.088 | -0.0003 | 0.98 / 0.98 / 0.98 | 0.985 |  |  | 9/16 | +0.017 | -0.019 |  | -0.0 / -0.0 | 0.123 |
| MES | 60 | h8 | -0.010 | -0.149 .. +0.129 | -0.0011 | 0.89 / 0.89 / 0.88 | 0.88 |  |  | 9/16 | +0.051 | -0.071 |  | -0.2 / -0.1 |  |
| MES | 60 | h16 * | -0.046 | -0.231 .. +0.138 | -0.0032 | 0.62 / 0.62 / 0.57 | 0.573 | 1 | 0.98 | 9/16 | +0.089 | -0.182 | False | -0.8 / -0.5 |  |
| MES | 60 | eod | -0.027 | -0.220 .. +0.167 | -0.0018 | 0.79 / 0.78 / 0.75 | 0.749 |  |  | 9/16 | +0.108 | -0.161 |  | -0.4 / -0.3 |  |
| MNQ | 15 | h1 * | -0.021 | -0.042 .. -0.000 | -0.0038 | 0.046 / 0.042 / 0.064 | 0.055 | 1 | 0.299 | 12/16 | -0.032 | -0.011 | False | -2.1 / -2.0 |  |
| MNQ | 15 | h2 | -0.008 | -0.038 .. +0.023 | -0.0008 | 0.63 / 0.62 / 0.7 | 0.632 |  |  | 8/16 | -0.023 | +0.008 |  | -0.5 / -0.5 |  |
| MNQ | 15 | h4 | -0.006 | -0.055 .. +0.043 | -0.0005 | 0.81 / 0.81 / 0.86 | 0.823 |  |  | 9/16 | -0.031 | +0.019 |  | -0.3 / -0.2 | 0.072 |
| MNQ | 15 | h8 | -0.009 | -0.090 .. +0.073 | -0.0005 | 0.84 / 0.83 / 0.85 | 0.831 |  |  | 8/16 | -0.088 | +0.070 |  | -0.3 / -0.2 |  |
| MNQ | 15 | h16 | +0.025 | -0.115 .. +0.165 | +0.0011 | 0.73 / 0.72 / 0.71 | 0.695 |  |  | 9/16 | -0.062 | +0.112 |  | +0.6 / +0.4 |  |
| MNQ | 15 | eod | +0.004 | -0.385 .. +0.392 | +0.0000 | 0.99 / 0.99 / 0.98 | 0.984 |  |  | 7/16 | +0.241 | -0.232 |  | +0.0 / +0.0 |  |
| MNQ | 60 | h1 | -0.016 | -0.064 .. +0.032 | -0.0035 | 0.52 / 0.51 / 0.47 | 0.484 |  |  | 10/16 | -0.055 | +0.023 |  | -0.7 / -0.7 |  |
| MNQ | 60 | h2 | -0.008 | -0.077 .. +0.062 | -0.0013 | 0.82 / 0.82 / 0.81 | 0.812 |  |  | 7/16 | -0.036 | +0.020 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h4 | -0.033 | -0.131 .. +0.065 | -0.0036 | 0.51 / 0.52 / 0.51 | 0.505 |  |  | 10/16 | -0.055 | -0.011 |  | -0.8 / -0.7 | 0.144 |
| MNQ | 60 | h8 * | -0.084 | -0.227 .. +0.060 | -0.0066 | 0.25 / 0.27 / 0.25 | 0.247 | 1 | 0.788 | 11/16 | -0.106 | -0.062 | False | -1.5 / -1.1 |  |
| MNQ | 60 | h16 | -0.054 | -0.233 .. +0.124 | -0.0035 | 0.55 / 0.56 / 0.54 | 0.536 |  |  | 9/16 | -0.082 | -0.026 |  | -0.9 / -0.6 |  |
| MNQ | 60 | eod | -0.028 | -0.212 .. +0.156 | -0.0018 | 0.77 / 0.77 / 0.76 | 0.759 |  |  | 8/16 | -0.055 | -0.001 |  | -0.4 / -0.3 |  |
| MYM | 15 | h1 | -0.018 | -0.042 .. +0.005 | -0.0041 | 0.13 / 0.14 / 0.21 | 0.195 |  |  | 7/8 | n/a | -0.018 |  | -1.4 / -1.5 |  |
| MYM | 15 | h2 * | -0.027 | -0.064 .. +0.010 | -0.0032 | 0.16 / 0.17 / 0.32 | 0.262 | 1 | 0.601 | 6/8 | n/a | -0.027 | False | -1.5 / -1.4 |  |
| MYM | 15 | h4 | -0.020 | -0.080 .. +0.040 | -0.0014 | 0.52 / 0.53 / 0.66 | 0.632 |  |  | 4/8 | n/a | -0.020 |  | -0.8 / -0.6 | 0.095 |
| MYM | 15 | h8 | -0.035 | -0.127 .. +0.057 | -0.0017 | 0.46 / 0.48 / 0.57 | 0.526 |  |  | 4/8 | n/a | -0.035 |  | -1.0 / -0.7 |  |
| MYM | 15 | h16 | -0.041 | -0.205 .. +0.124 | -0.0014 | 0.63 / 0.63 / 0.69 | 0.659 |  |  | 6/8 | n/a | -0.041 |  | -0.8 / -0.5 |  |
| MYM | 15 | eod | -0.210 | -0.740 .. +0.320 | -0.0032 | 0.44 / 0.45 / 0.46 | 0.436 |  |  | 5/8 | n/a | -0.210 |  | -1.7 / -0.8 |  |
| MYM | 60 | h1 | +0.007 | -0.054 .. +0.068 | +0.0017 | 0.82 / 0.81 / 0.79 | 0.777 |  |  | 3/8 | n/a | +0.007 |  | +0.2 / +0.2 |  |
| MYM | 60 | h2 | -0.018 | -0.108 .. +0.073 | -0.0028 | 0.7 / 0.69 / 0.68 | 0.678 |  |  | 5/8 | n/a | -0.018 |  | -0.4 / -0.4 |  |
| MYM | 60 | h4 * | -0.085 | -0.219 .. +0.050 | -0.0097 | 0.22 / 0.2 / 0.16 | 0.15 | 1 | 0.721 | 4/8 | n/a | -0.085 | False | -1.6 / -1.2 | 0.177 |
| MYM | 60 | h8 | -0.112 | -0.323 .. +0.099 | -0.0092 | 0.3 / 0.29 / 0.21 | 0.218 |  |  | 6/8 | n/a | -0.112 |  | -1.5 / -1.0 |  |
| MYM | 60 | h16 | -0.159 | -0.414 .. +0.096 | -0.0101 | 0.22 / 0.22 / 0.15 | 0.151 |  |  | 6/8 | n/a | -0.159 |  | -1.9 / -1.2 |  |
| MYM | 60 | eod | -0.132 | -0.390 .. +0.127 | -0.0081 | 0.32 / 0.32 / 0.26 | 0.252 |  |  | 6/8 | n/a | -0.132 |  | -1.6 / -1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.014 | +0.003 .. +0.024 | +2.7% | +0.009 | 0.072 | 1 | 12/16 |
| MES | 15 | h2 | +0.018 | +0.002 .. +0.033 | +2.4% | +0.004 | 0.13 |  | 10/16 |
| MES | 15 | h4 | +0.015 | -0.010 .. +0.039 | +1.4% | -0.012 | 0.44 |  | 11/16 |
| MES | 15 | h8 | +0.006 | -0.034 .. +0.045 | +0.4% | -0.042 | 0.91 |  | 9/16 |
| MES | 15 | h16 | +0.004 | -0.061 .. +0.069 | +0.2% | -0.064 | 0.91 |  | 7/16 |
| MES | 15 | eod | -0.103 | -0.304 .. +0.098 | -1.9% | -0.031 | 0.33 |  | 8/16 |
| MES | 60 | h1 * | +0.026 | +0.002 .. +0.050 | +5.1% | +0.036 | 0.18 | 1 | 11/16 |
| MES | 60 | h2 | +0.022 | -0.016 .. +0.059 | +2.9% | +0.038 | 0.5 |  | 11/16 |
| MES | 60 | h4 | +0.019 | -0.035 .. +0.073 | +1.8% | +0.041 | 0.71 |  | 9/16 |
| MES | 60 | h8 | +0.031 | -0.054 .. +0.116 | +2.1% | +0.037 | 0.72 |  | 7/16 |
| MES | 60 | h16 | +0.005 | -0.100 .. +0.110 | +0.2% | -0.000 | 0.98 |  | 9/16 |
| MES | 60 | eod | +0.003 | -0.105 .. +0.111 | +0.1% | +0.001 | 1 |  | 7/16 |
| MNQ | 15 | h1 * | +0.026 | +0.012 .. +0.039 | +4.8% | +0.023 | 0.00016 | 0.022 | 14/16 |
| MNQ | 15 | h2 | +0.027 | +0.006 .. +0.047 | +3.4% | +0.022 | 0.078 |  | 11/16 |
| MNQ | 15 | h4 | +0.015 | -0.021 .. +0.051 | +1.3% | +0.011 | 0.68 |  | 12/16 |
| MNQ | 15 | h8 | +0.036 | -0.022 .. +0.095 | +2.2% | +0.029 | 0.43 |  | 13/16 |
| MNQ | 15 | h16 | +0.057 | -0.031 .. +0.145 | +2.3% | +0.052 | 0.5 |  | 13/16 |
| MNQ | 15 | eod | +0.005 | -0.272 .. +0.283 | +0.1% | +0.074 | 0.97 |  | 9/16 |
| MNQ | 60 | h1 * | +0.025 | -0.005 .. +0.055 | +4.7% | +0.038 | 0.11 | 1 | 10/16 |
| MNQ | 60 | h2 | +0.038 | -0.006 .. +0.082 | +4.9% | +0.048 | 0.13 |  | 11/16 |
| MNQ | 60 | h4 | +0.021 | -0.041 .. +0.083 | +1.9% | +0.034 | 0.63 |  | 9/16 |
| MNQ | 60 | h8 | -0.007 | -0.098 .. +0.085 | -0.4% | +0.008 | 0.89 |  | 10/16 |
| MNQ | 60 | h16 | +0.010 | -0.095 .. +0.114 | +0.4% | -0.006 | 0.87 |  | 8/16 |
| MNQ | 60 | eod | +0.003 | -0.101 .. +0.108 | +0.1% | -0.007 | 0.95 |  | 8/16 |
| MYM | 15 | h1 | +0.005 | -0.013 .. +0.023 | +1.0% | +0.011 | 0.78 |  | 3/8 |
| MYM | 15 | h2 | +0.002 | -0.025 .. +0.030 | +0.3% | +0.006 | 0.88 |  | 3/8 |
| MYM | 15 | h4 | -0.004 | -0.050 .. +0.042 | -0.4% | -0.009 | 0.87 |  | 3/8 |
| MYM | 15 | h8 * | -0.035 | -0.101 .. +0.031 | -2.1% | -0.049 | 0.3 | 1 | 4/8 |
| MYM | 15 | h16 | -0.042 | -0.153 .. +0.069 | -1.7% | -0.081 | 0.46 |  | 4/8 |
| MYM | 15 | eod | -0.072 | -0.420 .. +0.275 | -1.2% | -0.018 | 0.74 |  | 4/8 |
| MYM | 60 | h1 * | +0.030 | -0.007 .. +0.068 | +5.7% | +0.046 | 0.3 | 1 | 6/8 |
| MYM | 60 | h2 | +0.026 | -0.025 .. +0.077 | +3.5% | +0.068 | 0.67 |  | 4/8 |
| MYM | 60 | h4 | +0.004 | -0.069 .. +0.077 | +0.4% | +0.036 | 0.91 |  | 5/8 |
| MYM | 60 | h8 | +0.053 | -0.066 .. +0.172 | +3.4% | +0.082 | 0.61 |  | 5/8 |
| MYM | 60 | h16 | +0.033 | -0.107 .. +0.174 | +1.6% | +0.080 | 0.93 |  | 3/8 |
| MYM | 60 | eod | +0.012 | -0.127 .. +0.151 | +0.5% | +0.053 | 0.87 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +0.38 pts | -0.80 .. +1.57 | 0.53 |
| MES | 60 | +0.23 pts | -2.00 .. +2.47 | 0.84 |
| MNQ | 15 | -0.17 pts | -1.31 .. +0.97 | 0.77 |
| MNQ | 60 | -1.77 pts | -4.07 .. +0.52 | 0.16 |
| MYM | 15 | +0.18 pts | -1.42 .. +1.77 | 0.83 |
| MYM | 60 | -0.21 pts | -2.91 .. +2.48 | 0.88 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | against signal | 10972 | +0.026 | 0.179 | +0.41 | -3.09 | -3.26 | -2.91 | -3.35 |
| MES | 15 | h2 | event | with signal | 10972 | -0.020 | 0.179 | -0.40 | -3.90 | -3.59 | -4.24 | -3.58 |
| MES | 15 | h4 | event | against signal | 10972 | +0.050 | 0.179 | +0.80 | -2.70 | -2.97 | -2.42 | -3.13 |
| MES | 15 | h8 | event | against signal | 10972 | +0.080 | 0.179 | +1.27 | -2.23 | -2.49 | -1.96 | -2.70 |
| MES | 15 | h16 | event | against signal | 10972 | +0.087 | 0.179 | +1.38 | -2.12 | -2.25 | -1.98 | -2.44 |
| MES | 15 | eod | event | against signal | 10972 | +0.438 | 0.179 | +7.08 | +3.58 | -1.24 | +8.76 | +5.19 |
| MES | 60 | h1 | event | with signal | 2342 | -0.011 | 0.081 | -1.08 | -4.58 | -3.65 | -5.61 | -4.23 |
| MES | 60 | h2 | event | against signal | 2342 | +0.038 | 0.081 | +2.96 | -0.54 | -2.79 | +1.93 | -1.33 |
| MES | 60 | h4 | event | against signal | 2342 | +0.048 | 0.081 | +4.03 | +0.53 | -2.71 | +4.08 | -0.81 |
| MES | 60 | h8 | event | against signal | 2342 | +0.085 | 0.081 | +6.33 | +2.83 | -2.48 | +8.64 | +0.89 |
| MES | 60 | h16 | event | against signal | 2342 | +0.128 | 0.081 | +8.51 | +5.01 | -3.52 | +14.35 | +3.64 |
| MES | 60 | eod | event | against signal | 2342 | +0.125 | 0.081 | +8.42 | +4.92 | -3.45 | +14.08 | +3.06 |
| MNQ | 15 | h1 | event | against signal | 9914 | +0.034 | 0.065 | +0.96 | -1.04 | -1.66 | -0.46 | -1.35 |
| MNQ | 15 | h2 | event | against signal | 9914 | +0.026 | 0.065 | +1.05 | -0.95 | -1.57 | -0.37 | -1.28 |
| MNQ | 15 | h4 | event | against signal | 9914 | +0.040 | 0.065 | +1.05 | -0.95 | -1.54 | -0.40 | -1.55 |
| MNQ | 15 | h8 | event | against signal | 9914 | +0.060 | 0.065 | +0.54 | -1.46 | -0.84 | -2.04 | -2.16 |
| MNQ | 15 | h16 | event | with signal | 9914 | -0.045 | 0.065 | -0.26 | -2.26 | -3.28 | -1.30 | -2.23 |
| MNQ | 15 | eod | event | with signal | 9914 | -0.237 | 0.065 | -5.78 | -7.78 | -3.71 | -11.59 | -11.20 |
| MNQ | 60 | h1 | event | against signal | 2182 | +0.023 | 0.031 | +0.38 | -1.62 | -0.83 | -2.36 | -1.76 |
| MNQ | 60 | h2 | event | against signal | 2182 | +0.033 | 0.031 | +1.42 | -0.58 | -0.31 | -0.84 | -1.48 |
| MNQ | 60 | h4 | event | against signal | 2182 | +0.081 | 0.031 | +3.88 | +1.88 | +0.54 | +3.16 | +0.09 |
| MNQ | 60 | h8 | event | against signal | 2182 | +0.173 | 0.031 | +7.95 | +5.95 | +2.50 | +9.22 | +2.88 |
| MNQ | 60 | h16 | event | against signal | 2182 | +0.168 | 0.031 | +7.41 | +5.41 | +2.88 | +7.80 | +2.86 |
| MNQ | 60 | eod | event | against signal | 2182 | +0.149 | 0.031 | +6.23 | +4.23 | +2.40 | +5.97 | +1.61 |
| MYM | 15 | h1 | event | against signal | 5383 | +0.022 | 0.092 | +0.49 | -1.51 | +nan | -1.51 | -1.56 |
| MYM | 15 | h2 | event | against signal | 5383 | +0.029 | 0.092 | +0.79 | -1.21 | +nan | -1.21 | -1.23 |
| MYM | 15 | h4 | event | against signal | 5383 | +0.028 | 0.092 | +0.73 | -1.27 | +nan | -1.27 | -1.41 |
| MYM | 15 | h8 | event | against signal | 5383 | +0.035 | 0.092 | +1.15 | -0.85 | +nan | -0.85 | -0.77 |
| MYM | 15 | h16 | event | against signal | 5383 | +0.029 | 0.092 | +1.04 | -0.96 | +nan | -0.96 | -0.56 |
| MYM | 15 | eod | event | against signal | 5383 | +0.304 | 0.092 | +6.29 | +4.29 | +nan | +4.29 | +3.97 |
| MYM | 60 | h1 | event | with signal | 1249 | +0.005 | 0.043 | +0.22 | -1.78 | +nan | -1.78 | -1.65 |
| MYM | 60 | h2 | event | against signal | 1249 | +0.028 | 0.043 | +2.33 | +0.33 | +nan | +0.33 | -0.20 |
| MYM | 60 | h4 | event | against signal | 1249 | +0.105 | 0.043 | +6.48 | +4.48 | +nan | +4.48 | +3.43 |
| MYM | 60 | h8 | event | against signal | 1249 | +0.141 | 0.043 | +9.29 | +7.29 | +nan | +7.29 | +5.87 |
| MYM | 60 | h16 | event | against signal | 1249 | +0.171 | 0.043 | +11.63 | +9.63 | +nan | +9.63 | +8.68 |
| MYM | 60 | eod | event | against signal | 1249 | +0.157 | 0.043 | +11.09 | +9.09 | +nan | +9.09 | +7.39 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.888 | +0.427 | -0.077 | -0.404 | -0.578 | +0.000 | -0.034 | -0.024 | -0.048 | -0.069 | -0.074 |
| MES | 60 | +0.915 | +0.313 | -0.135 | -0.458 | -0.663 | +0.000 | -0.000 | -0.015 | -0.010 | -0.051 | +0.113 |
| MNQ | 15 | +0.947 | +0.470 | -0.049 | -0.426 | -0.622 | +0.000 | -0.042 | -0.028 | -0.022 | -0.025 | -0.007 |
| MNQ | 60 | +0.993 | +0.325 | -0.163 | -0.512 | -0.732 | +0.000 | -0.017 | -0.018 | -0.041 | -0.128 | +0.086 |
| MYM | 15 | +0.952 | +0.452 | -0.059 | -0.415 | -0.606 | +0.000 | -0.045 | -0.051 | -0.043 | -0.067 | -0.054 |
| MYM | 60 | +0.905 | +0.357 | -0.127 | -0.492 | -0.702 | +0.000 | +0.014 | -0.000 | -0.070 | +0.004 | -0.299 |

## Calibration

- MES 15-min: 340296 bars, 10972 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81614 bars, 2342 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340140 bars, 9914 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81612 bars, 2182 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170466 bars, 5383 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40755 bars, 1249 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
