# Impact card: ema20_pullback_long

up-stack EMA8>20>50, bar touches EMA20 and closes above EMA8 -> long

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.011 R20 over the next 1 bar (15 min), p=0.95; we would catch an effect of 0.053 R20 or more 80% of the time).
- MES 15-min size: the market moves 8% MORE after the event than after matched bars over the next 2 bars (30 min) (+0.060 R20, CONFIRMED, q=1.58e-08, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.26 at recent bar sizes, 90% range up to $1.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.023 R20 over the next 1 bar (1 h), p=0.93; we would catch an effect of 0.101 R20 or more 80% of the time).
- MES 60-min size: the market moves 11% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.054 R20, CONFIRMED, q=0.00123, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.01 at recent bar sizes, 90% range up to $5.70); about 4.7x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best -0.021 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.081 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.34).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.82 at recent bar sizes, 90% range up to $2.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.033 R20 over the next 1 bar (1 h), p=0.44; we would catch an effect of 0.114 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.42).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.52 at recent bar sizes, 90% range up to $8.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best -0.009 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.104 R20 or more 80% of the time).
- MYM 15-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.043 R20, CONFIRMED, q=0.00261, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.17 at recent bar sizes, 90% range up to $2.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.023 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.159 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.41).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.83 at recent bar sizes, 90% range up to $5.32); about 13.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.011 | -0.026 .. +0.003 | -0.0032 | 0.13 / 0.12 / 0.12 | 0.119 | 1 | 0.588 | 10/16 | -0.012 | -0.010 | False | -1.5 / -1.5 |  |
| MES | 15 | h2 | +0.003 | -0.019 .. +0.026 | +0.0006 | 0.77 / 0.77 / 0.77 | 0.777 |  |  | 10/16 | -0.014 | +0.021 |  | +0.3 / +0.3 |  |
| MES | 15 | h4 | +0.013 | -0.024 .. +0.050 | +0.0017 | 0.49 / 0.48 / 0.48 | 0.471 |  |  | 9/16 | -0.026 | +0.051 |  | +0.9 / +0.7 | 0.053 |
| MES | 15 | h8 | +0.013 | -0.050 .. +0.075 | +0.0012 | 0.69 / 0.69 / 0.66 | 0.659 |  |  | 7/16 | -0.057 | +0.082 |  | +0.6 / +0.4 |  |
| MES | 15 | h16 | +0.019 | -0.078 .. +0.117 | +0.0012 | 0.7 / 0.69 / 0.66 | 0.668 |  |  | 7/16 | -0.102 | +0.140 |  | +0.6 / +0.4 |  |
| MES | 15 | eod | +0.184 | -0.133 .. +0.501 | +0.0045 | 0.26 / 0.28 / 0.18 | 0.175 |  |  | 11/16 | -0.093 | +0.459 |  | +2.6 / +1.1 |  |
| MES | 60 | h1 * | -0.023 | -0.054 .. +0.008 | -0.0064 | 0.15 / 0.16 / 0.13 | 0.127 | 1 | 0.602 | 9/16 | -0.035 | -0.011 | False | -1.4 / -1.4 |  |
| MES | 60 | h2 | -0.016 | -0.061 .. +0.028 | -0.0031 | 0.48 / 0.5 / 0.47 | 0.471 |  |  | 8/16 | -0.015 | -0.017 |  | -0.7 / -0.7 |  |
| MES | 60 | h4 | -0.030 | -0.103 .. +0.044 | -0.0041 | 0.43 / 0.44 / 0.38 | 0.377 |  |  | 8/16 | -0.040 | -0.019 |  | -1.0 / -0.8 | 0.101 |
| MES | 60 | h8 | +0.036 | -0.072 .. +0.145 | +0.0039 | 0.51 / 0.52 / 0.46 | 0.459 |  |  | 9/16 | +0.080 | -0.008 |  | +0.9 / +0.7 |  |
| MES | 60 | h16 | +0.036 | -0.095 .. +0.166 | +0.0027 | 0.59 / 0.62 / 0.57 | 0.574 |  |  | 9/16 | +0.062 | +0.010 |  | +0.8 / +0.5 |  |
| MES | 60 | eod | +0.028 | -0.108 .. +0.164 | +0.0020 | 0.69 / 0.7 / 0.67 | 0.672 |  |  | 7/16 | +0.062 | -0.006 |  | +0.6 / +0.4 |  |
| MNQ | 15 | h1 | -0.008 | -0.025 .. +0.009 | -0.0017 | 0.35 / 0.34 / 0.4 | 0.334 |  |  | 9/16 | -0.025 | +0.008 |  | -1.0 / -0.9 |  |
| MNQ | 15 | h2 | -0.012 | -0.038 .. +0.014 | -0.0015 | 0.36 / 0.35 / 0.46 | 0.383 |  |  | 9/16 | -0.032 | +0.008 |  | -1.0 / -0.9 |  |
| MNQ | 15 | h4 * | -0.021 | -0.062 .. +0.020 | -0.0015 | 0.31 / 0.32 / 0.46 | 0.399 | 1 | 0.917 | 10/16 | -0.054 | +0.011 | False | -1.2 / -1.0 | 0.081 |
| MNQ | 15 | h8 | +0.001 | -0.068 .. +0.070 | +0.0002 | 0.98 / 0.98 / 0.98 | 0.978 |  |  | 6/16 | -0.066 | +0.068 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h16 | +0.021 | -0.098 .. +0.140 | +0.0010 | 0.73 / 0.73 / 0.71 | 0.687 |  |  | 8/16 | -0.068 | +0.109 |  | +0.6 / +0.3 |  |
| MNQ | 15 | eod | +0.135 | -0.273 .. +0.542 | +0.0022 | 0.52 / 0.53 / 0.46 | 0.441 |  |  | 7/16 | -0.037 | +0.305 |  | +1.5 / +0.6 |  |
| MNQ | 60 | h1 * | -0.033 | -0.069 .. +0.003 | -0.0086 | 0.073 / 0.065 / 0.055 | 0.0586 | 1 | 0.356 | 10/16 | -0.046 | -0.020 | False | -1.8 / -1.8 |  |
| MNQ | 60 | h2 | -0.012 | -0.064 .. +0.040 | -0.0019 | 0.65 / 0.65 / 0.64 | 0.654 |  |  | 11/16 | -0.045 | +0.022 |  | -0.5 / -0.4 |  |
| MNQ | 60 | h4 | -0.007 | -0.087 .. +0.072 | -0.0007 | 0.86 / 0.86 / 0.85 | 0.853 |  |  | 11/16 | -0.089 | +0.074 |  | -0.2 / -0.2 | 0.114 |
| MNQ | 60 | h8 | -0.012 | -0.132 .. +0.108 | -0.0011 | 0.84 / 0.84 / 0.83 | 0.828 |  |  | 10/16 | -0.122 | +0.097 |  | -0.3 / -0.2 |  |
| MNQ | 60 | h16 | -0.007 | -0.157 .. +0.143 | -0.0005 | 0.93 / 0.93 / 0.92 | 0.918 |  |  | 7/16 | -0.103 | +0.089 |  | -0.1 / -0.1 |  |
| MNQ | 60 | eod | +0.006 | -0.145 .. +0.158 | +0.0005 | 0.93 / 0.93 / 0.92 | 0.923 |  |  | 8/16 | -0.082 | +0.095 |  | +0.1 / +0.1 |  |
| MYM | 15 | h1 * | -0.009 | -0.032 .. +0.014 | -0.0021 | 0.45 / 0.46 / 0.5 | 0.493 | 1 | 0.805 | 4/8 | n/a | -0.009 | False | -0.7 / -0.8 |  |
| MYM | 15 | h2 | -0.010 | -0.048 .. +0.028 | -0.0012 | 0.61 / 0.61 / 0.69 | 0.645 |  |  | 4/8 | n/a | -0.010 |  | -0.6 / -0.5 |  |
| MYM | 15 | h4 | +0.038 | -0.025 .. +0.100 | +0.0029 | 0.24 / 0.23 / 0.38 | 0.321 |  |  | 6/8 | n/a | +0.038 |  | +1.5 / +1.2 | 0.104 |
| MYM | 15 | h8 | +0.034 | -0.069 .. +0.137 | +0.0018 | 0.52 / 0.51 / 0.55 | 0.513 |  |  | 5/8 | n/a | +0.034 |  | +1.0 / +0.6 |  |
| MYM | 15 | h16 | +0.023 | -0.150 .. +0.195 | +0.0008 | 0.8 / 0.8 / 0.8 | 0.8 |  |  | 5/8 | n/a | +0.023 |  | +0.4 / +0.3 |  |
| MYM | 15 | eod | +0.193 | -0.375 .. +0.761 | +0.0032 | 0.5 / 0.51 / 0.44 | 0.427 |  |  | 6/8 | n/a | +0.193 |  | +1.6 / +0.7 |  |
| MYM | 60 | h1 | -0.010 | -0.061 .. +0.041 | -0.0026 | 0.7 / 0.7 / 0.68 | 0.69 |  |  | 5/8 | n/a | -0.010 |  | -0.4 / -0.4 |  |
| MYM | 60 | h2 * | -0.023 | -0.106 .. +0.060 | -0.0041 | 0.59 / 0.58 / 0.53 | 0.533 | 1 | 0.974 | 4/8 | n/a | -0.023 | False | -0.6 / -0.5 |  |
| MYM | 60 | h4 | -0.029 | -0.141 .. +0.082 | -0.0038 | 0.61 / 0.61 / 0.6 | 0.6 |  |  | 4/8 | n/a | -0.029 |  | -0.6 / -0.5 | 0.159 |
| MYM | 60 | h8 | +0.001 | -0.163 .. +0.165 | -0.0000 | 0.99 / 0.99 / 0.97 | 0.977 |  |  | 4/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 60 | h16 | -0.018 | -0.217 .. +0.182 | -0.0014 | 0.86 / 0.86 / 0.87 | 0.878 |  |  | 4/8 | n/a | -0.018 |  | -0.2 / -0.2 |  |
| MYM | 60 | eod | -0.018 | -0.226 .. +0.189 | -0.0013 | 0.86 / 0.86 / 0.87 | 0.863 |  |  | 4/8 | n/a | -0.018 |  | -0.3 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.035 | +0.025 .. +0.046 | +6.9% | +0.067 | 1.2e-08 |  | 14/16 |
| MES | 15 | h2 * | +0.060 | +0.044 .. +0.075 | +8.2% | +0.096 | 2.9e-11 | 1.58e-08 | 15/16 |
| MES | 15 | h4 | +0.073 | +0.049 .. +0.097 | +6.9% | +0.121 | 1.5e-08 |  | 13/16 |
| MES | 15 | h8 | +0.096 | +0.060 .. +0.133 | +6.3% | +0.147 | 8.2e-07 |  | 13/16 |
| MES | 15 | h16 | +0.076 | +0.019 .. +0.134 | +3.4% | +0.170 | 0.021 |  | 12/16 |
| MES | 15 | eod | +0.012 | -0.184 .. +0.208 | +0.2% | +0.188 | 0.91 |  | 9/16 |
| MES | 60 | h1 * | +0.054 | +0.033 .. +0.076 | +10.6% | +0.093 | 4.5e-06 | 0.00123 | 14/16 |
| MES | 60 | h2 | +0.050 | +0.017 .. +0.083 | +6.8% | +0.122 | 0.0093 |  | 13/16 |
| MES | 60 | h4 | +0.077 | +0.030 .. +0.125 | +7.3% | +0.157 | 0.0015 |  | 14/16 |
| MES | 60 | h8 | +0.077 | +0.011 .. +0.143 | +5.1% | +0.181 | 0.023 |  | 11/16 |
| MES | 60 | h16 | +0.058 | -0.019 .. +0.136 | +2.8% | +0.172 | 0.16 |  | 9/16 |
| MES | 60 | eod | +0.063 | -0.017 .. +0.142 | +2.9% | +0.182 | 0.14 |  | 8/16 |
| MNQ | 15 | h1 | +0.028 | +0.016 .. +0.040 | +5.2% | +0.057 | 0.1 |  | 11/16 |
| MNQ | 15 | h2 | +0.039 | +0.021 .. +0.057 | +5.1% | +0.078 | 0.068 |  | 13/16 |
| MNQ | 15 | h4 | +0.051 | +0.017 .. +0.085 | +4.5% | +0.098 | 0.069 |  | 12/16 |
| MNQ | 15 | h8 * | +0.077 | +0.027 .. +0.127 | +4.6% | +0.129 | 0.057 | 1 | 14/16 |
| MNQ | 15 | h16 | +0.051 | -0.022 .. +0.123 | +2.0% | +0.134 | 0.3 |  | 12/16 |
| MNQ | 15 | eod | +0.060 | -0.201 .. +0.322 | +1.0% | +0.266 | 0.65 |  | 10/16 |
| MNQ | 60 | h1 | +0.021 | -0.004 .. +0.046 | +3.9% | +0.064 | 0.18 |  | 11/16 |
| MNQ | 60 | h2 | +0.036 | +0.002 .. +0.070 | +4.7% | +0.097 | 0.13 |  | 10/16 |
| MNQ | 60 | h4 * | +0.056 | +0.002 .. +0.109 | +5.0% | +0.116 | 0.07 | 1 | 12/16 |
| MNQ | 60 | h8 | +0.063 | -0.012 .. +0.137 | +3.9% | +0.162 | 0.16 |  | 11/16 |
| MNQ | 60 | h16 | +0.078 | -0.009 .. +0.164 | +3.5% | +0.184 | 0.14 |  | 13/16 |
| MNQ | 60 | eod | +0.061 | -0.026 .. +0.148 | +2.6% | +0.178 | 0.25 |  | 11/16 |
| MYM | 15 | h1 * | +0.043 | +0.026 .. +0.059 | +8.1% | +0.075 | 1.4e-05 | 0.00261 | 7/8 |
| MYM | 15 | h2 | +0.063 | +0.038 .. +0.088 | +8.2% | +0.100 | 0.023 |  | 8/8 |
| MYM | 15 | h4 | +0.089 | +0.045 .. +0.133 | +8.0% | +0.132 | 0.047 |  | 6/8 |
| MYM | 15 | h8 | +0.138 | +0.071 .. +0.205 | +8.4% | +0.198 | 0.042 |  | 7/8 |
| MYM | 15 | h16 | +0.116 | +0.004 .. +0.229 | +4.8% | +0.210 | 0.22 |  | 7/8 |
| MYM | 15 | eod | +0.097 | -0.256 .. +0.450 | +1.6% | +0.227 | 0.73 |  | 5/8 |
| MYM | 60 | h1 * | +0.037 | -0.001 .. +0.075 | +7.1% | +0.074 | 0.068 | 1 | 4/8 |
| MYM | 60 | h2 | +0.041 | -0.023 .. +0.106 | +5.5% | +0.105 | 0.2 |  | 4/8 |
| MYM | 60 | h4 | +0.075 | -0.016 .. +0.167 | +6.9% | +0.138 | 0.11 |  | 4/8 |
| MYM | 60 | h8 | +0.079 | -0.029 .. +0.187 | +5.1% | +0.140 | 0.17 |  | 5/8 |
| MYM | 60 | h16 | -0.003 | -0.126 .. +0.120 | -0.1% | +0.077 | 0.96 |  | 4/8 |
| MYM | 60 | eod | -0.002 | -0.125 .. +0.120 | -0.1% | +0.085 | 0.97 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.48 pts | -1.44 .. +0.47 | 0.34 |
| MES | 60 | -0.88 pts | -2.70 .. +0.93 | 0.35 |
| MNQ | 15 | -0.01 pts | -1.03 .. +1.01 | 0.98 |
| MNQ | 60 | -0.83 pts | -2.59 .. +0.94 | 0.36 |
| MYM | 15 | -0.38 pts | -1.69 .. +0.92 | 0.58 |
| MYM | 60 | -0.60 pts | -3.56 .. +2.37 | 0.74 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | against signal | 14647 | +0.009 | 0.227 | +0.09 | -3.41 | -3.48 | -3.34 | -3.42 |
| MES | 15 | h2 | event | with signal | 14647 | +0.011 | 0.227 | +0.23 | -3.27 | -3.47 | -3.05 | -3.30 |
| MES | 15 | h4 | event | with signal | 14647 | +0.033 | 0.227 | +0.79 | -2.71 | -3.39 | -1.97 | -2.85 |
| MES | 15 | h8 | event | with signal | 14647 | +0.055 | 0.227 | +1.15 | -2.35 | -3.58 | -1.03 | -2.68 |
| MES | 15 | h16 | event | with signal | 14647 | +0.126 | 0.227 | +2.35 | -1.15 | -3.32 | +1.19 | -2.08 |
| MES | 15 | eod | event | with signal | 14647 | +0.562 | 0.227 | +6.63 | +3.13 | -0.52 | +7.06 | +0.70 |
| MES | 60 | h1 | event | against signal | 3590 | +0.011 | 0.119 | +0.24 | -3.26 | -3.17 | -3.35 | -3.00 |
| MES | 60 | h2 | event | against signal | 3590 | -0.010 | 0.119 | -0.02 | -3.52 | -3.58 | -3.46 | -2.97 |
| MES | 60 | h4 | event | against signal | 3590 | -0.017 | 0.119 | -0.70 | -4.20 | -3.37 | -5.14 | -3.24 |
| MES | 60 | h8 | event | with signal | 3590 | +0.116 | 0.119 | +2.08 | -1.42 | -1.24 | -1.61 | -3.00 |
| MES | 60 | h16 | event | with signal | 3590 | +0.155 | 0.119 | +3.66 | +0.16 | -0.04 | +0.39 | -2.10 |
| MES | 60 | eod | event | with signal | 3590 | +0.149 | 0.119 | +3.10 | -0.40 | +0.11 | -0.96 | -2.64 |
| MNQ | 15 | h1 | event | against signal | 13758 | +0.001 | 0.087 | -0.22 | -2.22 | -1.88 | -2.56 | -2.17 |
| MNQ | 15 | h2 | event | against signal | 13758 | -0.002 | 0.087 | -0.23 | -2.23 | -1.84 | -2.62 | -2.10 |
| MNQ | 15 | h4 | event | against signal | 13758 | -0.013 | 0.087 | -0.61 | -2.61 | -1.89 | -3.34 | -2.20 |
| MNQ | 15 | h8 | event | with signal | 13758 | +0.071 | 0.087 | +1.98 | -0.02 | -2.24 | +2.23 | -0.95 |
| MNQ | 15 | h16 | event | with signal | 13758 | +0.154 | 0.087 | +4.16 | +2.16 | -1.82 | +6.22 | +0.58 |
| MNQ | 15 | eod | event | with signal | 13758 | +0.620 | 0.087 | +7.83 | +5.83 | -0.20 | +11.98 | +2.02 |
| MNQ | 60 | h1 | event | against signal | 3431 | +0.017 | 0.045 | +1.00 | -1.00 | -1.49 | -0.47 | -0.52 |
| MNQ | 60 | h2 | event | against signal | 3431 | -0.023 | 0.045 | -0.63 | -2.63 | -1.60 | -3.71 | -1.54 |
| MNQ | 60 | h4 | event | against signal | 3431 | -0.058 | 0.045 | -3.40 | -5.40 | -1.37 | -9.68 | -3.40 |
| MNQ | 60 | h8 | event | against signal | 3431 | -0.091 | 0.045 | -4.22 | -6.22 | -1.62 | -11.10 | -3.36 |
| MNQ | 60 | h16 | event | against signal | 3431 | -0.130 | 0.045 | -3.73 | -5.73 | -2.63 | -9.01 | -2.66 |
| MNQ | 60 | eod | event | with signal | 3431 | +0.148 | 0.045 | +4.05 | +2.05 | -1.00 | +5.28 | -0.95 |
| MYM | 15 | h1 | event | against signal | 6542 | +0.010 | 0.109 | +0.29 | -1.71 | +nan | -1.71 | -1.74 |
| MYM | 15 | h2 | event | against signal | 6542 | +0.010 | 0.109 | +0.51 | -1.49 | +nan | -1.49 | -1.48 |
| MYM | 15 | h4 | event | with signal | 6542 | +0.049 | 0.109 | +0.89 | -1.11 | +nan | -1.11 | -1.33 |
| MYM | 15 | h8 | event | with signal | 6542 | +0.054 | 0.109 | +0.91 | -1.09 | +nan | -1.09 | -1.47 |
| MYM | 15 | h16 | event | with signal | 6542 | +0.050 | 0.109 | +1.40 | -0.60 | +nan | -0.60 | -1.24 |
| MYM | 15 | eod | event | with signal | 6542 | +0.404 | 0.109 | +4.04 | +2.04 | +nan | +2.04 | -0.08 |
| MYM | 60 | h1 | event | against signal | 1568 | +0.003 | 0.056 | -0.22 | -2.22 | +nan | -2.22 | -1.99 |
| MYM | 60 | h2 | event | against signal | 1568 | +0.009 | 0.056 | -0.43 | -2.43 | +nan | -2.43 | -1.97 |
| MYM | 60 | h4 | event | against signal | 1568 | -0.002 | 0.056 | -0.89 | -2.89 | +nan | -2.89 | -1.80 |
| MYM | 60 | h8 | event | with signal | 1568 | +0.050 | 0.056 | +2.16 | +0.16 | +nan | +0.16 | -1.55 |
| MYM | 60 | h16 | event | against signal | 1568 | -0.070 | 0.056 | -3.33 | -5.33 | +nan | -5.33 | -2.18 |
| MYM | 60 | eod | event | against signal | 1568 | -0.074 | 0.056 | -3.26 | -5.26 | +nan | -5.26 | -1.90 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.907 | +0.407 | -0.049 | -0.372 | -0.541 | +0.000 | -0.029 | -0.016 | -0.009 | -0.009 | +0.009 |
| MES | 60 | +1.084 | +0.407 | -0.054 | -0.365 | -0.572 | +0.000 | -0.025 | -0.023 | -0.040 | +0.017 | -0.044 |
| MNQ | 15 | +0.998 | +0.455 | -0.040 | -0.386 | -0.583 | +0.000 | -0.017 | -0.020 | -0.022 | +0.005 | +0.011 |
| MNQ | 60 | +1.140 | +0.421 | -0.038 | -0.383 | -0.619 | +0.000 | -0.038 | -0.024 | -0.022 | -0.072 | -0.235 |
| MYM | 15 | +0.976 | +0.460 | -0.048 | -0.394 | -0.584 | +0.000 | -0.018 | -0.020 | +0.036 | +0.045 | +0.054 |
| MYM | 60 | +1.092 | +0.398 | -0.064 | -0.400 | -0.631 | +0.000 | -0.008 | -0.020 | -0.041 | -0.007 | -0.139 |

## Calibration

- MES 15-min: 340296 bars, 14647 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81614 bars, 3590 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340140 bars, 13758 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81612 bars, 3431 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170466 bars, 6542 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40755 bars, 1568 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 347273 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
