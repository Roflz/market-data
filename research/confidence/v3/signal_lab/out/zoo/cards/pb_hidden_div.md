# Impact card: pb_hidden_div

pullback setups with hidden Momentum(14) divergence (higher low in price, lower momentum) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.336 R20 over the rest of the session (to 16:45), p=0.47; we would catch an effect of 0.048 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.13).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $6.08 at recent bar sizes, 90% range up to $1.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.027 R20 over the next 2 bars (30 min), p=0.97; we would catch an effect of 0.085 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.059).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.81 at recent bar sizes, 90% range up to $3.54); about 1.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.076 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.164 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.065).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.15 at recent bar sizes, 90% range up to $10.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.025 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.017).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.68 at recent bar sizes, 90% range up to $1.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.021 R20 over the next 1 bar (15 min), p=0.63; we would catch an effect of 0.076 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.97 at recent bar sizes, 90% range up to $4.37); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.041 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.180 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.69 at recent bar sizes, 90% range up to $15.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.033 R20 over the next 2 bars (10 min), p=0.18; we would catch an effect of 0.058 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.099).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.41 at recent bar sizes, 90% range up to $1.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.087 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.103 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.51).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.88 at recent bar sizes, 90% range up to $3.97); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.062 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.238 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.26).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.58 at recent bar sizes, 90% range up to $10.90); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.004 | -0.019 .. +0.011 | -0.0004 | 0.62 / 0.62 / 0.67 | 0.672 |  |  | 7/16 | -0.008 | +0.000 |  | -0.5 / -0.5 |  |
| MES | 5 | h2 | -0.018 | -0.038 .. +0.002 | -0.0014 | 0.085 / 0.099 / 0.16 | 0.157 |  |  | 10/16 | -0.012 | -0.024 |  | -1.6 / -1.7 |  |
| MES | 5 | h4 | -0.002 | -0.036 .. +0.032 | -0.0001 | 0.91 / 0.91 / 0.92 | 0.92 |  |  | 8/16 | -0.008 | +0.004 |  | -0.1 / -0.1 | 0.048 |
| MES | 5 | h8 | +0.009 | -0.044 .. +0.063 | +0.0003 | 0.73 / 0.73 / 0.72 | 0.721 |  |  | 8/16 | -0.024 | +0.042 |  | +0.4 / +0.3 |  |
| MES | 5 | h16 | +0.052 | -0.023 .. +0.128 | +0.0013 | 0.17 / 0.15 / 0.16 | 0.151 |  |  | 9/16 | +0.010 | +0.095 |  | +1.4 / +1.4 |  |
| MES | 5 | eod * | +0.336 | -0.038 .. +0.710 | +0.0017 | 0.079 / 0.065 / 0.08 | 0.0755 | 1 | 1 | 10/16 | +0.368 | +0.303 | False | +2.0 / +1.8 |  |
| MES | 15 | h1 | -0.009 | -0.035 .. +0.016 | -0.0010 | 0.49 / 0.49 / 0.55 | 0.538 |  |  | 10/16 | +0.001 | -0.019 |  | -0.6 / -0.7 |  |
| MES | 15 | h2 * | -0.027 | -0.066 .. +0.011 | -0.0021 | 0.16 / 0.15 / 0.23 | 0.216 | 1 | 1 | 12/16 | -0.014 | -0.040 | False | -1.4 / -1.4 |  |
| MES | 15 | h4 | -0.003 | -0.057 .. +0.050 | -0.0002 | 0.91 / 0.91 / 0.93 | 0.918 |  |  | 9/16 | +0.007 | -0.014 |  | -0.1 / -0.1 | 0.085 |
| MES | 15 | h8 | -0.047 | -0.134 .. +0.040 | -0.0017 | 0.29 / 0.28 / 0.32 | 0.313 |  |  | 11/16 | +0.005 | -0.098 |  | -1.1 / -1.1 |  |
| MES | 15 | h16 | +0.081 | -0.036 .. +0.198 | +0.0020 | 0.18 / 0.19 / 0.23 | 0.233 |  |  | 10/16 | +0.060 | +0.101 |  | +1.3 / +1.4 |  |
| MES | 15 | eod | +0.094 | -0.224 .. +0.412 | +0.0009 | 0.56 / 0.55 / 0.62 | 0.61 |  |  | 5/16 | -0.064 | +0.250 |  | +0.6 / +0.6 |  |
| MES | 60 | h1 | -0.015 | -0.071 .. +0.040 | -0.0018 | 0.59 / 0.56 / 0.61 | 0.609 |  |  | 9/16 | -0.037 | +0.006 |  | -0.6 / -0.5 |  |
| MES | 60 | h2 | -0.024 | -0.104 .. +0.056 | -0.0019 | 0.56 / 0.54 / 0.59 | 0.597 |  |  | 8/16 | -0.019 | -0.029 |  | -0.6 / -0.6 |  |
| MES | 60 | h4 | -0.059 | -0.171 .. +0.054 | -0.0033 | 0.31 / 0.29 / 0.34 | 0.345 |  |  | 9/16 | +0.024 | -0.141 |  | -1.0 / -1.0 | 0.164 |
| MES | 60 | h8 * | -0.076 | -0.220 .. +0.068 | -0.0031 | 0.3 / 0.3 / 0.35 | 0.346 | 1 | 1 | 10/16 | -0.024 | -0.128 | False | -1.0 / -1.0 |  |
| MES | 60 | h16 | +0.006 | -0.182 .. +0.194 | +0.0002 | 0.95 / 0.95 / 0.95 | 0.955 |  |  | 6/16 | +0.045 | -0.034 |  | +0.1 / +0.1 |  |
| MES | 60 | eod | +0.062 | -0.140 .. +0.264 | +0.0019 | 0.55 / 0.54 / 0.59 | 0.586 |  |  | 9/16 | +0.112 | +0.012 |  | +0.6 / +0.6 |  |
| MNQ | 5 | h1 | -0.008 | -0.022 .. +0.006 | -0.0008 | 0.28 / 0.28 / 0.39 | 0.336 |  |  | 8/16 | -0.005 | -0.010 |  | -1.1 / -1.1 |  |
| MNQ | 5 | h2 | -0.009 | -0.029 .. +0.012 | -0.0006 | 0.41 / 0.41 / 0.55 | 0.448 |  |  | 9/16 | +0.002 | -0.019 |  | -0.8 / -0.8 |  |
| MNQ | 5 | h4 * | -0.025 | -0.054 .. +0.004 | -0.0011 | 0.09 / 0.11 / 0.25 | 0.181 | 1 | 1 | 12/16 | -0.018 | -0.032 | False | -1.6 / -1.7 | 0.046 |
| MNQ | 5 | h8 | -0.018 | -0.061 .. +0.025 | -0.0005 | 0.4 / 0.43 / 0.58 | 0.522 |  |  | 10/16 | +0.002 | -0.038 |  | -0.8 / -0.8 |  |
| MNQ | 5 | h16 | +0.031 | -0.035 .. +0.096 | +0.0006 | 0.36 / 0.38 / 0.51 | 0.494 |  |  | 10/16 | +0.007 | +0.054 |  | +0.9 / +0.9 |  |
| MNQ | 5 | eod | -0.038 | -0.453 .. +0.378 | -0.0002 | 0.86 / 0.85 / 0.87 | 0.877 |  |  | 6/16 | +0.034 | -0.110 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h1 * | -0.021 | -0.047 .. +0.004 | -0.0021 | 0.11 / 0.1 / 0.2 | 0.12 | 1 | 1 | 10/16 | -0.019 | -0.024 | False | -1.6 / -1.6 |  |
| MNQ | 15 | h2 | -0.032 | -0.069 .. +0.005 | -0.0019 | 0.089 / 0.085 / 0.24 | 0.125 |  |  | 10/16 | -0.016 | -0.048 |  | -1.7 / -1.7 |  |
| MNQ | 15 | h4 | -0.005 | -0.057 .. +0.047 | -0.0002 | 0.85 / 0.85 / 0.92 | 0.875 |  |  | 8/16 | -0.008 | -0.002 |  | -0.2 / -0.2 | 0.076 |
| MNQ | 15 | h8 | -0.031 | -0.108 .. +0.046 | -0.0008 | 0.43 / 0.43 / 0.61 | 0.528 |  |  | 8/16 | -0.076 | +0.013 |  | -0.8 / -0.8 |  |
| MNQ | 15 | h16 | +0.005 | -0.113 .. +0.122 | +0.0001 | 0.94 / 0.94 / 0.95 | 0.952 |  |  | 8/16 | -0.109 | +0.117 |  | +0.1 / +0.1 |  |
| MNQ | 15 | eod | +0.121 | -0.249 .. +0.492 | +0.0009 | 0.52 / 0.53 / 0.62 | 0.583 |  |  | 11/16 | +0.062 | +0.180 |  | +0.7 / +0.6 |  |
| MNQ | 60 | h1 | -0.001 | -0.058 .. +0.057 | -0.0001 | 0.99 / 0.99 / 0.99 | 0.993 |  |  | 7/16 | +0.019 | -0.020 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h2 | +0.012 | -0.077 .. +0.100 | +0.0008 | 0.79 / 0.79 / 0.79 | 0.796 |  |  | 9/16 | +0.061 | -0.038 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h4 | -0.026 | -0.144 .. +0.092 | -0.0015 | 0.66 / 0.66 / 0.69 | 0.692 |  |  | 9/16 | +0.077 | -0.130 |  | -0.4 / -0.4 | 0.180 |
| MNQ | 60 | h8 * | -0.041 | -0.193 .. +0.111 | -0.0016 | 0.6 / 0.59 / 0.63 | 0.642 | 1 | 1 | 10/16 | +0.037 | -0.119 | False | -0.5 / -0.5 |  |
| MNQ | 60 | h16 | -0.047 | -0.261 .. +0.168 | -0.0015 | 0.67 / 0.67 / 0.68 | 0.687 |  |  | 9/16 | +0.031 | -0.124 |  | -0.4 / -0.4 |  |
| MNQ | 60 | eod | -0.022 | -0.252 .. +0.207 | -0.0007 | 0.85 / 0.85 / 0.86 | 0.862 |  |  | 8/16 | +0.091 | -0.136 |  | -0.2 / -0.2 |  |
| MYM | 5 | h1 | -0.006 | -0.023 .. +0.012 | -0.0006 | 0.52 / 0.52 / 0.66 | 0.603 |  |  | 5/8 | n/a | -0.006 |  | -0.6 / -0.6 |  |
| MYM | 5 | h2 * | -0.033 | -0.058 .. -0.007 | -0.0020 | 0.013 / 0.013 / 0.14 | 0.0885 | 1 | 0.677 | 6/8 | n/a | -0.033 | False | -2.3 / -2.5 |  |
| MYM | 5 | h4 | -0.051 | -0.087 .. -0.015 | -0.0020 | 0.0052 / 0.0066 / 0.14 | 0.103 |  |  | 7/8 | n/a | -0.051 |  | -2.5 / -2.8 | 0.058 |
| MYM | 5 | h8 | -0.041 | -0.094 .. +0.013 | -0.0011 | 0.13 / 0.16 / 0.41 | 0.316 |  |  | 6/8 | n/a | -0.041 |  | -1.3 / -1.5 |  |
| MYM | 5 | h16 | -0.025 | -0.109 .. +0.059 | -0.0005 | 0.56 / 0.57 / 0.69 | 0.659 |  |  | 4/8 | n/a | -0.025 |  | -0.6 / -0.6 |  |
| MYM | 5 | eod | -0.174 | -0.694 .. +0.346 | -0.0008 | 0.51 / 0.52 / 0.56 | 0.547 |  |  | 5/8 | n/a | -0.174 |  | -0.7 / -0.7 |  |
| MYM | 15 | h1 | -0.006 | -0.039 .. +0.027 | -0.0006 | 0.71 / 0.72 / 0.79 | 0.755 |  |  | 4/8 | n/a | -0.006 |  | -0.4 / -0.4 |  |
| MYM | 15 | h2 | -0.014 | -0.062 .. +0.033 | -0.0008 | 0.55 / 0.56 / 0.73 | 0.621 |  |  | 5/8 | n/a | -0.014 |  | -0.6 / -0.6 |  |
| MYM | 15 | h4 | -0.006 | -0.076 .. +0.064 | -0.0002 | 0.86 / 0.86 / 0.93 | 0.875 |  |  | 3/8 | n/a | -0.006 |  | -0.2 / -0.2 | 0.103 |
| MYM | 15 | h8 * | -0.087 | -0.202 .. +0.028 | -0.0023 | 0.14 / 0.12 / 0.31 | 0.181 | 1 | 1 | 7/8 | n/a | -0.087 | False | -1.6 / -1.5 |  |
| MYM | 15 | h16 | +0.041 | -0.124 .. +0.206 | +0.0008 | 0.63 / 0.63 / 0.72 | 0.665 |  |  | 5/8 | n/a | +0.041 |  | +0.5 / +0.5 |  |
| MYM | 15 | eod | -0.093 | -0.519 .. +0.332 | -0.0007 | 0.67 / 0.66 / 0.77 | 0.752 |  |  | 2/8 | n/a | -0.093 |  | -0.5 / -0.4 |  |
| MYM | 60 | h1 | +0.017 | -0.067 .. +0.102 | +0.0020 | 0.69 / 0.69 / 0.71 | 0.708 |  |  | 3/8 | n/a | +0.017 |  | +0.4 / +0.4 |  |
| MYM | 60 | h2 | +0.010 | -0.105 .. +0.124 | +0.0008 | 0.86 / 0.87 / 0.88 | 0.88 |  |  | 4/8 | n/a | +0.010 |  | +0.2 / +0.2 |  |
| MYM | 60 | h4 * | +0.062 | -0.079 .. +0.203 | +0.0036 | 0.39 / 0.41 / 0.47 | 0.476 | 1 | 1 | 5/8 | n/a | +0.062 | False | +0.9 / +0.9 | 0.238 |
| MYM | 60 | h8 | +0.090 | -0.113 .. +0.292 | +0.0038 | 0.38 / 0.39 / 0.43 | 0.45 |  |  | 5/8 | n/a | +0.090 |  | +0.9 / +0.9 |  |
| MYM | 60 | h16 | +0.066 | -0.214 .. +0.345 | +0.0022 | 0.65 / 0.65 / 0.67 | 0.669 |  |  | 4/8 | n/a | +0.066 |  | +0.4 / +0.5 |  |
| MYM | 60 | eod | +0.101 | -0.211 .. +0.413 | +0.0031 | 0.53 / 0.53 / 0.54 | 0.544 |  |  | 4/8 | n/a | +0.101 |  | +0.6 / +0.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.012 | -0.023 .. -0.001 | -2.4% | -0.030 | 0.13 |  | 11/16 |
| MES | 5 | h2 | -0.006 | -0.020 .. +0.008 | -0.9% | -0.034 | 0.71 |  | 10/16 |
| MES | 5 | h4 | -0.001 | -0.023 .. +0.021 | -0.1% | -0.029 | 0.95 |  | 6/16 |
| MES | 5 | h8 | -0.009 | -0.042 .. +0.025 | -0.6% | -0.036 | 0.81 |  | 6/16 |
| MES | 5 | h16 | -0.025 | -0.075 .. +0.026 | -1.2% | -0.061 | 0.51 |  | 8/16 |
| MES | 5 | eod * | -0.312 | -0.577 .. -0.046 | -3.1% | -0.560 | 0.021 | 1 | 9/16 |
| MES | 15 | h1 | -0.013 | -0.032 .. +0.006 | -2.6% | -0.034 | 0.2 |  | 9/16 |
| MES | 15 | h2 | -0.026 | -0.051 .. -0.001 | -3.6% | -0.051 | 0.12 |  | 13/16 |
| MES | 15 | h4 | -0.051 | -0.089 .. -0.013 | -4.9% | -0.078 | 0.035 |  | 12/16 |
| MES | 15 | h8 | -0.035 | -0.093 .. +0.022 | -2.3% | -0.077 | 0.44 |  | 10/16 |
| MES | 15 | h16 | -0.012 | -0.091 .. +0.067 | -0.5% | -0.099 | 0.82 |  | 10/16 |
| MES | 15 | eod * | -0.298 | -0.486 .. -0.109 | -5.4% | -0.419 | 0.0099 | 1 | 11/16 |
| MES | 60 | h1 | -0.029 | -0.065 .. +0.007 | -5.6% | -0.030 | 0.26 |  | 12/16 |
| MES | 60 | h2 | -0.021 | -0.071 .. +0.030 | -2.8% | -0.032 | 0.43 |  | 11/16 |
| MES | 60 | h4 | -0.033 | -0.111 .. +0.044 | -3.2% | -0.022 | 0.4 |  | 12/16 |
| MES | 60 | h8 | -0.090 | -0.187 .. +0.006 | -6.0% | -0.050 | 0.096 |  | 10/16 |
| MES | 60 | h16 * | -0.181 | -0.290 .. -0.072 | -8.8% | -0.124 | 0.011 | 1 | 11/16 |
| MES | 60 | eod | -0.121 | -0.240 .. -0.002 | -5.6% | -0.107 | 0.087 |  | 10/16 |
| MNQ | 5 | h1 | -0.011 | -0.021 .. -0.001 | -2.1% | -0.030 | 0.12 |  | 12/16 |
| MNQ | 5 | h2 | -0.013 | -0.027 .. +0.002 | -1.7% | -0.036 | 0.19 |  | 10/16 |
| MNQ | 5 | h4 | -0.004 | -0.029 .. +0.021 | -0.3% | -0.040 | 0.93 |  | 9/16 |
| MNQ | 5 | h8 | -0.017 | -0.056 .. +0.022 | -1.1% | -0.051 | 0.55 |  | 10/16 |
| MNQ | 5 | h16 | -0.029 | -0.090 .. +0.032 | -1.2% | -0.098 | 0.44 |  | 9/16 |
| MNQ | 5 | eod * | -0.480 | -0.793 .. -0.166 | -3.8% | -0.806 | 0.0028 | 0.435 | 12/16 |
| MNQ | 15 | h1 | -0.012 | -0.029 .. +0.005 | -2.2% | -0.037 | 0.39 |  | 11/16 |
| MNQ | 15 | h2 | -0.012 | -0.039 .. +0.015 | -1.6% | -0.052 | 0.67 |  | 10/16 |
| MNQ | 15 | h4 | -0.046 | -0.086 .. -0.007 | -4.1% | -0.082 | 0.33 |  | 10/16 |
| MNQ | 15 | h8 | -0.044 | -0.100 .. +0.012 | -2.6% | -0.125 | 0.4 |  | 11/16 |
| MNQ | 15 | h16 * | -0.080 | -0.162 .. +0.002 | -3.2% | -0.205 | 0.23 | 1 | 10/16 |
| MNQ | 15 | eod | -0.192 | -0.461 .. +0.077 | -3.0% | -0.454 | 0.33 |  | 11/16 |
| MNQ | 60 | h1 | +0.008 | -0.031 .. +0.047 | +1.4% | +0.001 | 0.71 |  | 10/16 |
| MNQ | 60 | h2 | -0.018 | -0.083 .. +0.047 | -2.3% | +0.018 | 0.59 |  | 9/16 |
| MNQ | 60 | h4 * | -0.043 | -0.125 .. +0.040 | -3.9% | -0.037 | 0.32 | 1 | 11/16 |
| MNQ | 60 | h8 | -0.056 | -0.148 .. +0.036 | -3.5% | -0.041 | 0.37 |  | 10/16 |
| MNQ | 60 | h16 | -0.051 | -0.183 .. +0.080 | -2.3% | -0.056 | 0.44 |  | 9/16 |
| MNQ | 60 | eod | -0.024 | -0.160 .. +0.112 | -1.0% | -0.056 | 0.74 |  | 9/16 |
| MYM | 5 | h1 | -0.017 | -0.030 .. -0.004 | -3.2% | -0.041 | 0.019 |  | 6/8 |
| MYM | 5 | h2 | -0.029 | -0.052 .. -0.006 | -3.8% | -0.057 | 0.019 |  | 6/8 |
| MYM | 5 | h4 | -0.026 | -0.059 .. +0.006 | -2.4% | -0.071 | 0.54 |  | 4/8 |
| MYM | 5 | h8 | -0.023 | -0.072 .. +0.025 | -1.5% | -0.080 | 0.73 |  | 6/8 |
| MYM | 5 | h16 | -0.025 | -0.103 .. +0.054 | -1.1% | -0.108 | 0.67 |  | 4/8 |
| MYM | 5 | eod * | -0.559 | -0.920 .. -0.198 | -4.8% | -1.024 | 0.016 | 1 | 7/8 |
| MYM | 15 | h1 | -0.020 | -0.041 .. +0.001 | -3.7% | -0.040 | 0.29 |  | 5/8 |
| MYM | 15 | h2 | -0.035 | -0.068 .. -0.001 | -4.6% | -0.060 | 0.27 |  | 7/8 |
| MYM | 15 | h4 | -0.082 | -0.133 .. -0.031 | -7.4% | -0.111 | 0.28 |  | 7/8 |
| MYM | 15 | h8 | -0.061 | -0.141 .. +0.019 | -3.7% | -0.133 | 0.39 |  | 6/8 |
| MYM | 15 | h16 | +0.006 | -0.127 .. +0.138 | +0.2% | -0.153 | 0.96 |  | 5/8 |
| MYM | 15 | eod * | -0.420 | -0.730 .. -0.109 | -7.0% | -0.597 | 0.086 | 1 | 7/8 |
| MYM | 60 | h1 | -0.022 | -0.080 .. +0.035 | -4.2% | -0.027 | 0.48 |  | 6/8 |
| MYM | 60 | h2 | -0.057 | -0.129 .. +0.015 | -7.6% | -0.023 | 0.16 |  | 5/8 |
| MYM | 60 | h4 * | -0.119 | -0.206 .. -0.032 | -11.0% | -0.070 | 0.044 | 1 | 6/8 |
| MYM | 60 | h8 | -0.098 | -0.221 .. +0.025 | -6.3% | -0.080 | 0.13 |  | 5/8 |
| MYM | 60 | h16 | -0.091 | -0.274 .. +0.092 | -4.3% | -0.064 | 0.37 |  | 6/8 |
| MYM | 60 | eod | -0.049 | -0.246 .. +0.148 | -2.2% | -0.019 | 0.63 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.62 pts | -1.71 .. +0.48 | 0.37 |
| MES | 15 | -0.19 pts | -2.23 .. +1.84 | 0.85 |
| MES | 60 | -0.07 pts | -3.44 .. +3.30 | 0.97 |
| MNQ | 5 | -0.99 pts | -1.98 .. +0.00 | 0.066 |
| MNQ | 15 | -1.72 pts | -3.32 .. -0.12 | 0.036 |
| MNQ | 60 | -1.08 pts | -4.43 .. +2.28 | 0.65 |
| MYM | 5 | -0.98 pts | -2.24 .. +0.27 | 0.14 |
| MYM | 15 | -0.78 pts | -3.11 .. +1.55 | 0.51 |
| MYM | 60 | +1.08 pts | -3.55 .. +5.72 | 0.79 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 6602 | +0.005 | 0.251 | -0.02 | -3.52 | -3.43 | -3.58 | -3.54 |
| MES | 5 | h2 | event | against signal | 6602 | +0.019 | 0.251 | +0.16 | -3.34 | -3.44 | -3.27 | -3.35 |
| MES | 5 | h4 | event | against signal | 6602 | +0.002 | 0.251 | +0.07 | -3.43 | -3.43 | -3.44 | -3.43 |
| MES | 5 | h8 | event | with signal | 6602 | +0.011 | 0.251 | +0.29 | -3.21 | -3.62 | -2.95 | -3.22 |
| MES | 5 | h16 | event | with signal | 6602 | +0.055 | 0.251 | +0.78 | -2.72 | -3.60 | -2.18 | -2.74 |
| MES | 5 | eod | event | with signal | 6602 | +0.474 | 0.251 | +1.06 | -2.44 | -1.00 | -3.33 | -4.19 |
| MES | 15 | h1 | event | against signal | 2543 | +0.008 | 0.162 | +0.34 | -3.16 | -3.52 | -2.89 | -3.16 |
| MES | 15 | h2 | event | against signal | 2543 | +0.026 | 0.162 | +0.63 | -2.87 | -3.62 | -2.32 | -2.85 |
| MES | 15 | h4 | event | against signal | 2543 | -0.001 | 0.162 | +0.05 | -3.45 | -3.77 | -3.22 | -3.39 |
| MES | 15 | h8 | event | against signal | 2543 | +0.038 | 0.162 | +0.91 | -2.59 | -3.48 | -1.93 | -2.46 |
| MES | 15 | h16 | event | with signal | 2543 | +0.107 | 0.162 | +1.92 | -1.58 | -3.08 | -0.46 | -2.02 |
| MES | 15 | eod | event | with signal | 2543 | +0.189 | 0.162 | +0.31 | -3.19 | -2.95 | -3.37 | -4.78 |
| MES | 60 | h1 | event | against signal | 681 | +0.013 | 0.092 | -0.22 | -3.72 | -2.92 | -4.43 | -3.65 |
| MES | 60 | h2 | event | against signal | 681 | +0.018 | 0.092 | -0.51 | -4.01 | -3.41 | -4.55 | -3.85 |
| MES | 60 | h4 | event | against signal | 681 | +0.046 | 0.092 | +1.72 | -1.78 | -4.08 | +0.27 | -1.49 |
| MES | 60 | h8 | event | against signal | 681 | +0.053 | 0.092 | +1.84 | -1.66 | -3.46 | -0.06 | -1.21 |
| MES | 60 | h16 | event | with signal | 681 | +0.039 | 0.092 | +2.19 | -1.31 | -3.37 | +0.52 | -2.00 |
| MES | 60 | eod | event | with signal | 681 | +0.096 | 0.092 | +4.33 | +0.83 | -1.69 | +3.09 | +0.22 |
| MNQ | 5 | h1 | event | against signal | 9291 | +0.007 | 0.108 | +0.19 | -1.81 | -1.95 | -1.72 | -1.80 |
| MNQ | 5 | h2 | event | against signal | 9291 | +0.007 | 0.108 | +0.44 | -1.56 | -2.02 | -1.25 | -1.51 |
| MNQ | 5 | h4 | event | against signal | 9291 | +0.020 | 0.108 | +0.40 | -1.60 | -1.90 | -1.41 | -1.50 |
| MNQ | 5 | h8 | event | against signal | 9291 | +0.010 | 0.108 | +0.70 | -1.30 | -2.12 | -0.76 | -1.14 |
| MNQ | 5 | h16 | event | with signal | 9291 | +0.047 | 0.108 | +0.45 | -1.55 | -1.79 | -1.40 | -1.79 |
| MNQ | 5 | eod | event | against signal | 9291 | -0.241 | 0.108 | -0.85 | -2.85 | -1.55 | -3.71 | +2.31 |
| MNQ | 15 | h1 | event | against signal | 3129 | +0.021 | 0.068 | +0.10 | -1.90 | -1.89 | -1.91 | -1.92 |
| MNQ | 15 | h2 | event | against signal | 3129 | +0.031 | 0.068 | +0.78 | -1.22 | -1.75 | -0.81 | -1.24 |
| MNQ | 15 | h4 | event | against signal | 3129 | +0.001 | 0.068 | +0.20 | -1.80 | -1.69 | -1.88 | -1.76 |
| MNQ | 15 | h8 | event | against signal | 3129 | +0.018 | 0.068 | +0.27 | -1.73 | -0.81 | -2.44 | -1.57 |
| MNQ | 15 | h16 | event | with signal | 3129 | +0.039 | 0.068 | +2.62 | +0.62 | -2.81 | +3.28 | -0.04 |
| MNQ | 15 | eod | event | with signal | 3129 | +0.244 | 0.068 | +0.11 | -1.89 | -2.23 | -1.63 | -4.27 |
| MNQ | 60 | h1 | event | against signal | 721 | -0.006 | 0.036 | +2.04 | +0.04 | -1.98 | +1.96 | +0.22 |
| MNQ | 60 | h2 | event | with signal | 721 | +0.024 | 0.036 | -1.66 | -3.66 | -2.40 | -4.84 | -4.03 |
| MNQ | 60 | h4 | event | against signal | 721 | +0.002 | 0.036 | +4.69 | +2.69 | -1.55 | +6.70 | +3.41 |
| MNQ | 60 | h8 | event | against signal | 721 | +0.002 | 0.036 | +3.36 | +1.36 | -1.04 | +3.64 | +2.49 |
| MNQ | 60 | h16 | event | against signal | 721 | -0.016 | 0.036 | -0.45 | -2.45 | -2.84 | -2.08 | -0.39 |
| MNQ | 60 | eod | event | against signal | 721 | -0.052 | 0.036 | -1.94 | -3.94 | -4.32 | -3.58 | -1.49 |
| MYM | 5 | h1 | event | against signal | 5220 | +0.006 | 0.157 | +0.14 | -1.86 | +nan | -1.86 | -1.87 |
| MYM | 5 | h2 | event | against signal | 5220 | +0.031 | 0.157 | +0.55 | -1.45 | +nan | -1.45 | -1.42 |
| MYM | 5 | h4 | event | against signal | 5220 | +0.045 | 0.157 | +1.15 | -0.85 | +nan | -0.85 | -0.74 |
| MYM | 5 | h8 | event | against signal | 5220 | +0.030 | 0.157 | +0.83 | -1.17 | +nan | -1.17 | -0.96 |
| MYM | 5 | h16 | event | against signal | 5220 | +0.007 | 0.157 | +0.66 | -1.34 | +nan | -1.34 | -1.03 |
| MYM | 5 | eod | event | against signal | 5220 | +0.072 | 0.157 | +1.90 | -0.10 | +nan | -0.10 | +1.28 |
| MYM | 15 | h1 | event | against signal | 1681 | +0.004 | 0.093 | +0.71 | -1.29 | +nan | -1.29 | -1.26 |
| MYM | 15 | h2 | event | against signal | 1681 | +0.013 | 0.093 | +0.93 | -1.07 | +nan | -1.07 | -1.03 |
| MYM | 15 | h4 | event | against signal | 1681 | +0.003 | 0.093 | +0.54 | -1.46 | +nan | -1.46 | -1.38 |
| MYM | 15 | h8 | event | against signal | 1681 | +0.082 | 0.093 | +1.26 | -0.74 | +nan | -0.74 | -0.59 |
| MYM | 15 | h16 | event | with signal | 1681 | +0.038 | 0.093 | +1.11 | -0.89 | +nan | -0.89 | -0.90 |
| MYM | 15 | eod | event | against signal | 1681 | +0.087 | 0.093 | +1.41 | -0.59 | +nan | -0.59 | -1.23 |
| MYM | 60 | h1 | event | with signal | 349 | +0.019 | 0.048 | +0.85 | -1.15 | +nan | -1.15 | -1.21 |
| MYM | 60 | h2 | event | with signal | 349 | +0.011 | 0.048 | -0.47 | -2.47 | +nan | -2.47 | -2.43 |
| MYM | 60 | h4 | event | with signal | 349 | +0.064 | 0.048 | +0.89 | -1.11 | +nan | -1.11 | -1.04 |
| MYM | 60 | h8 | event | with signal | 349 | +0.095 | 0.048 | +1.32 | -0.68 | +nan | -0.68 | -0.49 |
| MYM | 60 | h16 | event | with signal | 349 | +0.076 | 0.048 | +0.48 | -1.52 | +nan | -1.52 | -1.30 |
| MYM | 60 | eod | event | with signal | 349 | +0.110 | 0.048 | +1.80 | -0.20 | +nan | -0.20 | +0.20 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +1.206 | +0.891 | -0.287 | -0.192 | -0.058 | +0.000 | -0.003 | -0.018 | -0.003 | +0.007 | +0.050 |
| MES | 15 | +1.242 | +0.956 | -0.251 | -0.164 | -0.032 | +0.000 | -0.005 | -0.026 | +0.002 | -0.057 | +0.117 |
| MES | 60 | +1.667 | +1.069 | -0.185 | -0.115 | -0.025 | +0.000 | -0.011 | -0.015 | -0.047 | -0.068 | +0.207 |
| MNQ | 5 | +1.260 | +1.012 | -0.238 | -0.162 | -0.037 | +0.000 | -0.010 | -0.011 | -0.026 | -0.019 | +0.026 |
| MNQ | 15 | +1.255 | +1.017 | -0.182 | -0.144 | -0.032 | +0.000 | -0.021 | -0.035 | -0.009 | -0.036 | +0.006 |
| MNQ | 60 | +1.849 | +1.139 | -0.211 | -0.127 | -0.035 | +0.000 | +0.004 | +0.018 | +0.018 | -0.041 | +0.045 |
| MYM | 5 | +1.229 | +1.018 | -0.253 | -0.166 | -0.041 | +0.000 | -0.007 | -0.035 | -0.055 | -0.048 | -0.038 |
| MYM | 15 | +1.175 | +1.007 | -0.223 | -0.121 | -0.003 | +0.000 | -0.005 | -0.015 | -0.009 | -0.116 | -0.010 |
| MYM | 60 | +1.500 | +1.144 | -0.191 | -0.090 | -0.039 | +0.000 | +0.015 | +0.013 | +0.108 | +0.175 | +0.162 |

## Calibration

- MES 5-min: 1036271 bars, 6602 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 2543 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 681 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 9291 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 3129 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 721 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 5220 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 1681 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 349 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
