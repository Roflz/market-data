# Impact card: nfp_day

US jobs report (NFP) session (computed BLS schedule) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (5 min), p=0.28; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.92).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.11 at recent bar sizes, 90% range up to $1.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.011 R20 over the next 1 bar (15 min), p=0.68; we would catch an effect of 0.071 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.15).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.32 at recent bar sizes, 90% range up to $5.27); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.020 R20 over the next 1 bar (1 h), p=0.94; we would catch an effect of 0.142 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.01).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.09 at recent bar sizes, 90% range up to $16.91); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (5 min), p=0.8; we would catch an effect of 0.044 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.81).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.16 at recent bar sizes, 90% range up to $2.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.452 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.079 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.15).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $21.37 at recent bar sizes, 90% range up to $7.75); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.167 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.154 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.074).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $15.36 at recent bar sizes, 90% range up to $26.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.083 R20 over the next 8 bars (40 min), p=0.62; we would catch an effect of 0.064 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.99 at recent bar sizes, 90% range up to $2.02); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.263 R20 over the next 16 bars (4 h), p=0.98; we would catch an effect of 0.108 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.83).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.58 at recent bar sizes, 90% range up to $5.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.048 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.205 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.15).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.00 at recent bar sizes, 90% range up to $16.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.007 | +0.000 .. +0.014 | +0.0023 | 0.046 / 0.039 / 0.045 | 0.0464 | 1 | 0.999 | 11/16 | +0.007 | +0.007 | False | +1.9 / +2.0 |  |
| MES | 5 | h2 | +0.013 | -0.001 .. +0.027 | +0.0029 | 0.067 / 0.059 / 0.062 | 0.0649 |  |  | 10/16 | +0.011 | +0.014 |  | +2.5 / +1.8 |  |
| MES | 5 | h4 | +0.025 | -0.003 .. +0.054 | +0.0039 | 0.082 / 0.075 / 0.076 | 0.0802 |  |  | 10/16 | +0.020 | +0.031 |  | +3.5 / +1.7 | 0.038 |
| MES | 5 | h8 | +0.051 | -0.008 .. +0.110 | +0.0054 | 0.093 / 0.085 / 0.084 | 0.0849 |  |  | 10/16 | +0.034 | +0.067 |  | +4.8 / +1.7 |  |
| MES | 5 | h16 | +0.105 | -0.018 .. +0.227 | +0.0078 | 0.094 / 0.086 / 0.083 | 0.0818 |  |  | 10/16 | +0.055 | +0.154 |  | +6.8 / +1.7 |  |
| MES | 5 | eod | +1.347 | -0.600 .. +3.295 | +0.0199 | 0.18 / 0.16 / 0.21 | 0.201 |  |  | 11/16 | +0.389 | +2.301 |  | +17.9 / +1.4 |  |
| MES | 15 | h1 * | +0.011 | -0.003 .. +0.025 | +0.0034 | 0.11 / 0.099 / 0.11 | 0.108 | 1 | 1 | 10/16 | +0.007 | +0.015 | False | +1.6 / +1.6 |  |
| MES | 15 | h2 | +0.021 | -0.006 .. +0.048 | +0.0042 | 0.13 / 0.12 / 0.13 | 0.125 |  |  | 10/16 | +0.009 | +0.032 |  | +2.2 / +1.5 |  |
| MES | 15 | h4 | +0.041 | -0.014 .. +0.097 | +0.0056 | 0.15 / 0.13 / 0.14 | 0.144 |  |  | 10/16 | +0.013 | +0.070 |  | +2.9 / +1.5 | 0.071 |
| MES | 15 | h8 | +0.084 | -0.032 .. +0.199 | +0.0081 | 0.15 / 0.14 / 0.14 | 0.147 |  |  | 10/16 | +0.010 | +0.157 |  | +4.1 / +1.4 |  |
| MES | 15 | h16 | +0.167 | -0.076 .. +0.410 | +0.0112 | 0.18 / 0.16 / 0.17 | 0.166 |  |  | 10/16 | -0.006 | +0.340 |  | +5.5 / +1.4 |  |
| MES | 15 | eod | +0.719 | -0.376 .. +1.813 | +0.0186 | 0.2 / 0.18 / 0.23 | 0.223 |  |  | 11/16 | +0.160 | +1.274 |  | +9.9 / +1.3 |  |
| MES | 60 | h1 * | +0.020 | -0.008 .. +0.047 | +0.0060 | 0.16 / 0.15 / 0.16 | 0.158 | 1 | 1 | 10/16 | +0.007 | +0.032 | False | +1.4 / +1.4 |  |
| MES | 60 | h2 | +0.039 | -0.016 .. +0.093 | +0.0082 | 0.16 / 0.15 / 0.17 | 0.165 |  |  | 10/16 | +0.010 | +0.067 |  | +2.0 / +1.4 |  |
| MES | 60 | h4 | +0.072 | -0.034 .. +0.178 | +0.0109 | 0.18 / 0.17 / 0.19 | 0.189 |  |  | 10/16 | +0.021 | +0.123 |  | +2.6 / +1.3 | 0.142 |
| MES | 60 | h8 | +0.128 | -0.076 .. +0.332 | +0.0140 | 0.22 / 0.21 / 0.23 | 0.228 |  |  | 10/16 | +0.049 | +0.207 |  | +3.5 / +1.2 |  |
| MES | 60 | h16 | +0.215 | -0.144 .. +0.575 | +0.0181 | 0.24 / 0.23 / 0.26 | 0.261 |  |  | 11/16 | +0.077 | +0.353 |  | +4.5 / +1.2 |  |
| MES | 60 | eod | +0.222 | -0.164 .. +0.608 | +0.0178 | 0.26 / 0.25 / 0.3 | 0.309 |  |  | 11/16 | +0.102 | +0.343 |  | +4.6 / +1.1 |  |
| MNQ | 5 | h1 * | +0.006 | -0.002 .. +0.014 | +0.0015 | 0.13 / 0.12 / 0.17 | 0.159 | 1 | 1 | 9/16 | +0.008 | +0.004 | False | +1.5 / +1.5 |  |
| MNQ | 5 | h2 | +0.012 | -0.004 .. +0.028 | +0.0019 | 0.13 / 0.12 / 0.19 | 0.179 |  |  | 10/16 | +0.014 | +0.010 |  | +2.1 / +1.5 |  |
| MNQ | 5 | h4 | +0.024 | -0.009 .. +0.057 | +0.0026 | 0.15 / 0.14 / 0.21 | 0.19 |  |  | 10/16 | +0.025 | +0.023 |  | +2.9 / +1.4 | 0.044 |
| MNQ | 5 | h8 | +0.046 | -0.023 .. +0.115 | +0.0033 | 0.19 / 0.17 / 0.25 | 0.218 |  |  | 10/16 | +0.042 | +0.051 |  | +3.7 / +1.3 |  |
| MNQ | 5 | h16 | +0.084 | -0.060 .. +0.229 | +0.0043 | 0.25 / 0.24 / 0.3 | 0.276 |  |  | 10/16 | +0.056 | +0.112 |  | +4.6 / +1.1 |  |
| MNQ | 5 | eod | +0.888 | -1.777 .. +3.554 | +0.0095 | 0.51 / 0.5 / 0.5 | 0.52 |  |  | 9/16 | -0.628 | +2.393 |  | +8.4 / +0.7 |  |
| MNQ | 15 | h1 | +0.005 | -0.011 .. +0.021 | +0.0012 | 0.52 / 0.5 / 0.57 | 0.508 |  |  | 9/16 | +0.001 | +0.009 |  | +0.7 / +0.6 |  |
| MNQ | 15 | h2 | +0.011 | -0.021 .. +0.042 | +0.0015 | 0.51 / 0.49 / 0.59 | 0.525 |  |  | 10/16 | -0.001 | +0.022 |  | +1.0 / +0.7 |  |
| MNQ | 15 | h4 | +0.021 | -0.046 .. +0.087 | +0.0017 | 0.54 / 0.51 / 0.62 | 0.54 |  |  | 10/16 | -0.009 | +0.051 |  | +1.3 / +0.6 | 0.079 |
| MNQ | 15 | h8 | +0.043 | -0.097 .. +0.183 | +0.0027 | 0.55 / 0.52 / 0.58 | 0.535 |  |  | 9/16 | -0.035 | +0.120 |  | +1.8 / +0.6 |  |
| MNQ | 15 | h16 | +0.089 | -0.206 .. +0.385 | +0.0046 | 0.55 / 0.53 / 0.54 | 0.522 |  |  | 8/16 | -0.101 | +0.279 |  | +2.5 / +0.6 |  |
| MNQ | 15 | eod * | +0.452 | -0.891 .. +1.795 | +0.0081 | 0.51 / 0.49 / 0.54 | 0.522 | 1 | 1 | 9/16 | -0.372 | +1.271 | False | +5.0 / +0.7 |  |
| MNQ | 60 | h1 | +0.010 | -0.020 .. +0.040 | +0.0030 | 0.49 / 0.48 / 0.48 | 0.484 |  |  | 9/16 | -0.003 | +0.024 |  | +0.7 / +0.7 |  |
| MNQ | 60 | h2 | +0.023 | -0.037 .. +0.083 | +0.0046 | 0.45 / 0.43 / 0.44 | 0.443 |  |  | 9/16 | -0.008 | +0.054 |  | +1.1 / +0.8 |  |
| MNQ | 60 | h4 | +0.047 | -0.070 .. +0.165 | +0.0067 | 0.43 / 0.41 / 0.42 | 0.432 |  |  | 9/16 | -0.011 | +0.105 |  | +1.6 / +0.8 | 0.154 |
| MNQ | 60 | h8 | +0.090 | -0.134 .. +0.314 | +0.0093 | 0.43 / 0.41 / 0.43 | 0.436 |  |  | 9/16 | -0.006 | +0.187 |  | +2.3 / +0.8 |  |
| MNQ | 60 | h16 * | +0.167 | -0.230 .. +0.564 | +0.0131 | 0.41 / 0.39 / 0.42 | 0.422 | 1 | 1 | 9/16 | -0.028 | +0.362 | False | +3.2 / +0.8 |  |
| MNQ | 60 | eod | +0.175 | -0.247 .. +0.598 | +0.0132 | 0.42 / 0.4 / 0.44 | 0.442 |  |  | 9/16 | -0.003 | +0.354 |  | +3.3 / +0.8 |  |
| MYM | 5 | h1 | +0.009 | -0.003 .. +0.020 | +0.0021 | 0.14 / 0.14 / 0.16 | 0.159 |  |  | 6/8 | n/a | +0.009 |  | +1.6 / +1.5 |  |
| MYM | 5 | h2 | +0.018 | -0.006 .. +0.041 | +0.0026 | 0.14 / 0.14 / 0.19 | 0.177 |  |  | 5/8 | n/a | +0.018 |  | +2.2 / +1.5 |  |
| MYM | 5 | h4 | +0.037 | -0.011 .. +0.086 | +0.0034 | 0.13 / 0.13 / 0.2 | 0.184 |  |  | 6/8 | n/a | +0.037 |  | +3.2 / +1.5 | 0.064 |
| MYM | 5 | h8 * | +0.083 | -0.017 .. +0.182 | +0.0054 | 0.1 / 0.1 / 0.15 | 0.134 | 1 | 1 | 6/8 | n/a | +0.083 | False | +4.9 / +1.6 |  |
| MYM | 5 | h16 | +0.165 | -0.037 .. +0.366 | +0.0084 | 0.11 / 0.1 / 0.13 | 0.126 |  |  | 6/8 | n/a | +0.165 |  | +6.7 / +1.6 |  |
| MYM | 5 | eod | +1.846 | -1.434 .. +5.126 | +0.0210 | 0.27 / 0.27 / 0.28 | 0.27 |  |  | 5/8 | n/a | +1.846 |  | +13.9 / +1.1 |  |
| MYM | 15 | h1 | +0.013 | -0.007 .. +0.033 | +0.0032 | 0.21 / 0.2 / 0.24 | 0.222 |  |  | 5/8 | n/a | +0.013 |  | +1.3 / +1.3 |  |
| MYM | 15 | h2 | +0.027 | -0.014 .. +0.069 | +0.0038 | 0.19 / 0.19 / 0.28 | 0.236 |  |  | 5/8 | n/a | +0.027 |  | +1.9 / +1.3 |  |
| MYM | 15 | h4 | +0.057 | -0.028 .. +0.141 | +0.0047 | 0.19 / 0.18 / 0.3 | 0.232 |  |  | 5/8 | n/a | +0.057 |  | +2.7 / +1.3 | 0.108 |
| MYM | 15 | h8 | +0.123 | -0.051 .. +0.297 | +0.0078 | 0.16 / 0.16 / 0.22 | 0.191 |  |  | 5/8 | n/a | +0.123 |  | +4.1 / +1.4 |  |
| MYM | 15 | h16 * | +0.263 | -0.107 .. +0.634 | +0.0119 | 0.16 / 0.16 / 0.21 | 0.182 | 1 | 1 | 5/8 | n/a | +0.263 | False | +5.8 / +1.4 |  |
| MYM | 15 | eod | +0.947 | -0.709 .. +2.602 | +0.0177 | 0.26 / 0.26 / 0.31 | 0.287 |  |  | 5/8 | n/a | +0.947 |  | +8.3 / +1.1 |  |
| MYM | 60 | h1 | +0.022 | -0.017 .. +0.062 | +0.0065 | 0.27 / 0.26 / 0.27 | 0.272 |  |  | 4/8 | n/a | +0.022 |  | +1.1 / +1.1 |  |
| MYM | 60 | h2 * | +0.048 | -0.031 .. +0.127 | +0.0097 | 0.24 / 0.23 / 0.24 | 0.254 | 1 | 1 | 4/8 | n/a | +0.048 | False | +1.7 / +1.2 |  |
| MYM | 60 | h4 | +0.084 | -0.070 .. +0.239 | +0.0123 | 0.28 / 0.28 / 0.29 | 0.301 |  |  | 4/8 | n/a | +0.084 |  | +2.2 / +1.1 | 0.205 |
| MYM | 60 | h8 | +0.127 | -0.171 .. +0.426 | +0.0135 | 0.4 / 0.4 / 0.41 | 0.41 |  |  | 4/8 | n/a | +0.127 |  | +2.4 / +0.8 |  |
| MYM | 60 | h16 | +0.207 | -0.317 .. +0.731 | +0.0168 | 0.44 / 0.44 / 0.44 | 0.441 |  |  | 4/8 | n/a | +0.207 |  | +3.0 / +0.8 |  |
| MYM | 60 | eod | +0.199 | -0.367 .. +0.766 | +0.0154 | 0.49 / 0.49 / 0.51 | 0.512 |  |  | 5/8 | n/a | +0.199 |  | +2.8 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.004 .. +0.005 | +0.1% | +0.005 | 0.82 |  | 8/16 |
| MES | 5 | h2 | -0.002 | -0.011 .. +0.006 | -0.4% | +0.008 | 0.55 |  | 10/16 |
| MES | 5 | h4 | -0.002 | -0.018 .. +0.014 | -0.2% | +0.019 | 0.77 |  | 9/16 |
| MES | 5 | h8 | +0.006 | -0.027 .. +0.040 | +0.4% | +0.044 | 0.75 |  | 8/16 |
| MES | 5 | h16 | +0.030 | -0.035 .. +0.095 | +1.4% | +0.106 | 0.37 |  | 8/16 |
| MES | 5 | eod * | +0.835 | -0.236 .. +1.907 | +8.4% | +2.414 | 0.15 | 1 | 10/16 |
| MES | 15 | h1 | +0.007 | -0.001 .. +0.016 | +1.4% | +0.023 | 0.092 |  | 12/16 |
| MES | 15 | h2 | +0.015 | -0.001 .. +0.031 | +2.1% | +0.042 | 0.061 |  | 11/16 |
| MES | 15 | h4 | +0.031 | -0.002 .. +0.063 | +2.9% | +0.080 | 0.065 |  | 11/16 |
| MES | 15 | h8 | +0.059 | -0.003 .. +0.120 | +3.8% | +0.152 | 0.062 |  | 11/16 |
| MES | 15 | h16 * | +0.140 | +0.018 .. +0.263 | +6.1% | +0.335 | 0.025 | 1 | 12/16 |
| MES | 15 | eod | +0.553 | -0.068 .. +1.174 | +10.1% | +1.555 | 0.095 |  | 11/16 |
| MES | 60 | h1 * | +0.035 | +0.013 .. +0.057 | +6.8% | +0.053 | 0.0017 | 0.277 | 14/16 |
| MES | 60 | h2 | +0.039 | +0.004 .. +0.073 | +5.3% | +0.081 | 0.027 |  | 12/16 |
| MES | 60 | h4 | +0.065 | +0.006 .. +0.125 | +6.2% | +0.139 | 0.031 |  | 11/16 |
| MES | 60 | h8 | +0.107 | +0.003 .. +0.212 | +7.1% | +0.255 | 0.049 |  | 10/16 |
| MES | 60 | h16 | +0.192 | +0.002 .. +0.383 | +9.3% | +0.464 | 0.057 |  | 10/16 |
| MES | 60 | eod | +0.136 | -0.075 .. +0.347 | +6.3% | +0.443 | 0.25 |  | 9/16 |
| MNQ | 5 | h1 | +0.002 | -0.002 .. +0.007 | +0.4% | +0.006 | 0.36 |  | 13/16 |
| MNQ | 5 | h2 | +0.004 | -0.005 .. +0.014 | +0.5% | +0.012 | 0.47 |  | 10/16 |
| MNQ | 5 | h4 | +0.005 | -0.015 .. +0.025 | +0.5% | +0.024 | 0.67 |  | 9/16 |
| MNQ | 5 | h8 | +0.018 | -0.027 .. +0.063 | +1.1% | +0.052 | 0.47 |  | 8/16 |
| MNQ | 5 | h16 | +0.033 | -0.057 .. +0.123 | +1.4% | +0.123 | 0.47 |  | 11/16 |
| MNQ | 5 | eod * | +1.268 | -0.393 .. +2.929 | +10.1% | +3.169 | 0.13 | 1 | 10/16 |
| MNQ | 15 | h1 | +0.010 | +0.000 .. +0.020 | +1.9% | +0.023 | 0.044 |  | 11/16 |
| MNQ | 15 | h2 * | +0.024 | +0.003 .. +0.045 | +3.1% | +0.046 | 0.026 | 1 | 13/16 |
| MNQ | 15 | h4 | +0.038 | -0.009 .. +0.084 | +3.3% | +0.088 | 0.12 |  | 13/16 |
| MNQ | 15 | h8 | +0.055 | -0.033 .. +0.143 | +3.3% | +0.162 | 0.22 |  | 10/16 |
| MNQ | 15 | h16 | +0.137 | -0.036 .. +0.309 | +5.4% | +0.348 | 0.12 |  | 10/16 |
| MNQ | 15 | eod | +0.672 | -0.177 .. +1.522 | +10.6% | +1.702 | 0.12 |  | 10/16 |
| MNQ | 60 | h1 * | +0.028 | +0.006 .. +0.049 | +5.2% | +0.051 | 0.012 | 1 | 13/16 |
| MNQ | 60 | h2 | +0.026 | -0.009 .. +0.062 | +3.4% | +0.075 | 0.15 |  | 11/16 |
| MNQ | 60 | h4 | +0.052 | -0.013 .. +0.117 | +4.7% | +0.126 | 0.12 |  | 12/16 |
| MNQ | 60 | h8 | +0.102 | -0.018 .. +0.222 | +6.4% | +0.233 | 0.098 |  | 10/16 |
| MNQ | 60 | h16 | +0.209 | -0.014 .. +0.432 | +9.5% | +0.431 | 0.068 |  | 10/16 |
| MNQ | 60 | eod | +0.166 | -0.075 .. +0.408 | +7.2% | +0.414 | 0.18 |  | 9/16 |
| MYM | 5 | h1 * | +0.005 | -0.002 .. +0.011 | +0.9% | +0.004 | 0.17 | 1 | 5/8 |
| MYM | 5 | h2 | +0.005 | -0.009 .. +0.019 | +0.6% | +0.008 | 0.51 |  | 6/8 |
| MYM | 5 | h4 | +0.008 | -0.020 .. +0.037 | +0.8% | +0.014 | 0.58 |  | 4/8 |
| MYM | 5 | h8 | +0.018 | -0.041 .. +0.077 | +1.1% | +0.025 | 0.56 |  | 6/8 |
| MYM | 5 | h16 | +0.052 | -0.053 .. +0.157 | +2.2% | +0.076 | 0.33 |  | 5/8 |
| MYM | 5 | eod | +0.852 | -1.221 .. +2.925 | +7.3% | +2.221 | 0.42 |  | 4/8 |
| MYM | 15 | h1 * | +0.010 | -0.003 .. +0.022 | +1.8% | +0.016 | 0.14 | 1 | 6/8 |
| MYM | 15 | h2 | +0.017 | -0.006 .. +0.041 | +2.2% | +0.030 | 0.16 |  | 6/8 |
| MYM | 15 | h4 | +0.034 | -0.015 .. +0.082 | +3.0% | +0.057 | 0.18 |  | 6/8 |
| MYM | 15 | h8 | +0.060 | -0.030 .. +0.151 | +3.7% | +0.113 | 0.19 |  | 6/8 |
| MYM | 15 | h16 | +0.098 | -0.091 .. +0.288 | +4.0% | +0.259 | 0.31 |  | 5/8 |
| MYM | 15 | eod | +0.421 | -0.624 .. +1.466 | +7.0% | +1.231 | 0.43 |  | 4/8 |
| MYM | 60 | h1 * | +0.031 | +0.004 .. +0.058 | +5.9% | +0.041 | 0.024 | 1 | 6/8 |
| MYM | 60 | h2 | +0.031 | -0.015 .. +0.077 | +4.1% | +0.060 | 0.19 |  | 5/8 |
| MYM | 60 | h4 | +0.035 | -0.050 .. +0.120 | +3.3% | +0.100 | 0.42 |  | 4/8 |
| MYM | 60 | h8 | +0.054 | -0.109 .. +0.217 | +3.5% | +0.184 | 0.52 |  | 4/8 |
| MYM | 60 | h16 | +0.114 | -0.197 .. +0.426 | +5.4% | +0.363 | 0.47 |  | 4/8 |
| MYM | 60 | eod | +0.086 | -0.258 .. +0.431 | +3.9% | +0.351 | 0.62 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.21 pts | -0.74 .. +1.16 | 0.67 |
| MES | 15 | +1.06 pts | -0.57 .. +2.69 | 0.2 |
| MES | 60 | +2.99 pts | -0.40 .. +6.37 | 0.084 |
| MNQ | 5 | +0.31 pts | -0.69 .. +1.32 | 0.54 |
| MNQ | 15 | +1.26 pts | -0.37 .. +2.90 | 0.13 |
| MNQ | 60 | +3.42 pts | +0.02 .. +6.82 | 0.049 |
| MYM | 5 | +0.06 pts | -1.29 .. +1.41 | 0.93 |
| MYM | 15 | -0.40 pts | -2.68 .. +1.88 | 0.82 |
| MYM | 60 | +2.85 pts | -2.23 .. +7.93 | 0.27 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 48014 | +0.008 | 0.302 | +0.00 | -3.50 | -3.48 | -3.52 | -3.50 |
| MES | 5 | h2 | event | long | 48014 | +0.017 | 0.302 | +0.01 | -3.49 | -3.46 | -3.52 | -3.50 |
| MES | 5 | h4 | event | long | 48014 | +0.035 | 0.302 | +0.03 | -3.47 | -3.41 | -3.54 | -3.51 |
| MES | 5 | h8 | event | long | 48014 | +0.069 | 0.302 | +0.06 | -3.44 | -3.32 | -3.56 | -3.53 |
| MES | 5 | h16 | event | long | 48014 | +0.144 | 0.302 | +0.17 | -3.33 | -3.14 | -3.52 | -3.56 |
| MES | 5 | eod | event | long | 48014 | +2.100 | 0.302 | +3.16 | -0.34 | +1.10 | -1.75 | -4.65 |
| MES | 15 | h1 | event | long | 15892 | +0.015 | 0.175 | +0.02 | -3.48 | -3.43 | -3.54 | -3.53 |
| MES | 15 | h2 | event | long | 15892 | +0.029 | 0.175 | +0.05 | -3.45 | -3.36 | -3.55 | -3.53 |
| MES | 15 | h4 | event | long | 15892 | +0.057 | 0.175 | +0.11 | -3.39 | -3.23 | -3.56 | -3.50 |
| MES | 15 | h8 | event | long | 15892 | +0.115 | 0.175 | +0.38 | -3.12 | -2.95 | -3.29 | -3.34 |
| MES | 15 | h16 | event | long | 15892 | +0.234 | 0.175 | +0.77 | -2.73 | -2.46 | -3.00 | -3.20 |
| MES | 15 | eod | event | long | 15892 | +1.101 | 0.175 | +3.18 | -0.32 | +1.09 | -1.71 | -4.18 |
| MES | 60 | h1 | event | long | 3921 | +0.027 | 0.090 | +0.16 | -3.34 | -3.21 | -3.48 | -3.54 |
| MES | 60 | h2 | event | long | 3921 | +0.056 | 0.090 | +0.48 | -3.02 | -2.96 | -3.09 | -3.51 |
| MES | 60 | h4 | event | long | 3921 | +0.109 | 0.090 | +0.79 | -2.71 | -2.43 | -2.99 | -3.80 |
| MES | 60 | h8 | event | long | 3921 | +0.204 | 0.090 | +1.20 | -2.30 | -1.28 | -3.32 | -4.57 |
| MES | 60 | h16 | event | long | 3921 | +0.349 | 0.090 | +2.49 | -1.01 | +0.10 | -2.13 | -5.06 |
| MES | 60 | eod | event | long | 3921 | +0.382 | 0.090 | +3.14 | -0.36 | +1.08 | -1.80 | -5.37 |
| MNQ | 5 | h1 | event | long | 47888 | +0.007 | 0.120 | -0.06 | -2.06 | -1.98 | -2.14 | -2.03 |
| MNQ | 5 | h2 | event | long | 47888 | +0.015 | 0.120 | -0.10 | -2.10 | -1.97 | -2.24 | -2.04 |
| MNQ | 5 | h4 | event | long | 47888 | +0.030 | 0.120 | -0.20 | -2.20 | -1.93 | -2.47 | -2.05 |
| MNQ | 5 | h8 | event | long | 47888 | +0.053 | 0.120 | -0.40 | -2.40 | -1.87 | -2.91 | -2.08 |
| MNQ | 5 | h16 | event | long | 47888 | +0.101 | 0.120 | -0.72 | -2.72 | -1.75 | -3.68 | -2.23 |
| MNQ | 5 | eod | event | long | 47888 | +1.096 | 0.120 | -7.05 | -9.05 | +0.25 | -18.20 | -0.30 |
| MNQ | 15 | h1 | event | long | 15883 | +0.008 | 0.068 | -0.16 | -2.16 | -1.94 | -2.38 | -2.13 |
| MNQ | 15 | h2 | event | long | 15883 | +0.015 | 0.068 | -0.31 | -2.31 | -1.89 | -2.71 | -2.20 |
| MNQ | 15 | h4 | event | long | 15883 | +0.027 | 0.068 | -0.57 | -2.57 | -1.80 | -3.33 | -2.31 |
| MNQ | 15 | h8 | event | long | 15883 | +0.053 | 0.068 | -0.92 | -2.92 | -1.63 | -4.21 | -2.31 |
| MNQ | 15 | h16 | event | long | 15883 | +0.099 | 0.068 | -1.84 | -3.84 | -1.37 | -6.27 | -2.17 |
| MNQ | 15 | eod | event | long | 15883 | +0.523 | 0.068 | -7.09 | -9.09 | +0.12 | -18.20 | -2.00 |
| MNQ | 60 | h1 | event | long | 3920 | +0.014 | 0.035 | -0.52 | -2.52 | -1.80 | -3.25 | -2.35 |
| MNQ | 60 | h2 | event | long | 3920 | +0.030 | 0.035 | -0.80 | -2.80 | -1.64 | -3.95 | -2.55 |
| MNQ | 60 | h4 | event | long | 3920 | +0.060 | 0.035 | -1.87 | -3.87 | -1.37 | -6.37 | -3.47 |
| MNQ | 60 | h8 | event | long | 3920 | +0.113 | 0.035 | -4.19 | -6.19 | -0.85 | -11.52 | -5.37 |
| MNQ | 60 | h16 | event | long | 3920 | +0.203 | 0.035 | -6.39 | -8.39 | -0.59 | -16.18 | -6.52 |
| MNQ | 60 | eod | event | long | 3920 | +0.224 | 0.035 | -6.94 | -8.94 | +0.12 | -17.99 | -7.37 |
| MYM | 5 | h1 | event | long | 24139 | +0.009 | 0.158 | +0.02 | -1.98 | +nan | -1.98 | -1.99 |
| MYM | 5 | h2 | event | long | 24139 | +0.020 | 0.158 | +0.05 | -1.95 | +nan | -1.95 | -1.98 |
| MYM | 5 | h4 | event | long | 24139 | +0.042 | 0.158 | +0.11 | -1.89 | +nan | -1.89 | -1.97 |
| MYM | 5 | h8 | event | long | 24139 | +0.089 | 0.158 | +0.22 | -1.78 | +nan | -1.78 | -1.94 |
| MYM | 5 | h16 | event | long | 24139 | +0.197 | 0.158 | +0.53 | -1.47 | +nan | -1.47 | -2.06 |
| MYM | 5 | eod | event | long | 24139 | +3.078 | 0.158 | +8.64 | +6.64 | +nan | +6.64 | -8.08 |
| MYM | 15 | h1 | event | long | 7989 | +0.019 | 0.090 | +0.08 | -1.92 | +nan | -1.92 | -2.03 |
| MYM | 15 | h2 | event | long | 7989 | +0.038 | 0.090 | +0.17 | -1.83 | +nan | -1.83 | -2.06 |
| MYM | 15 | h4 | event | long | 7989 | +0.077 | 0.090 | +0.37 | -1.63 | +nan | -1.63 | -2.11 |
| MYM | 15 | h8 | event | long | 7989 | +0.167 | 0.090 | +1.02 | -0.98 | +nan | -0.98 | -2.07 |
| MYM | 15 | h16 | event | long | 7989 | +0.358 | 0.090 | +2.14 | +0.14 | +nan | +0.14 | -2.39 |
| MYM | 15 | eod | event | long | 7989 | +1.555 | 0.090 | +8.69 | +6.69 | +nan | +6.69 | -6.22 |
| MYM | 60 | h1 | event | long | 1962 | +0.036 | 0.046 | +0.41 | -1.59 | +nan | -1.59 | -2.18 |
| MYM | 60 | h2 | event | long | 1962 | +0.076 | 0.046 | +1.15 | -0.85 | +nan | -0.85 | -2.14 |
| MYM | 60 | h4 | event | long | 1962 | +0.142 | 0.046 | +2.17 | +0.17 | +nan | +0.17 | -2.48 |
| MYM | 60 | h8 | event | long | 1962 | +0.239 | 0.046 | +3.60 | +1.60 | +nan | +1.60 | -3.39 |
| MYM | 60 | h16 | event | long | 1962 | +0.403 | 0.046 | +7.33 | +5.33 | +nan | +5.33 | -3.30 |
| MYM | 60 | eod | event | long | 1962 | +0.428 | 0.046 | +8.49 | +6.49 | +nan | +6.49 | -3.65 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.022 | +0.009 | +0.001 | -0.002 | -0.002 | +0.000 | +0.006 | +0.012 | +0.024 | +0.049 | +0.105 |
| MES | 15 | -0.016 | -0.007 | -0.007 | -0.008 | -0.006 | +0.000 | +0.010 | +0.020 | +0.039 | +0.089 | +0.214 |
| MES | 60 | -0.215 | -0.117 | -0.057 | -0.030 | -0.018 | +0.000 | +0.017 | +0.041 | +0.081 | +0.172 | +0.313 |
| MNQ | 5 | -0.007 | -0.006 | -0.004 | -0.003 | -0.002 | +0.000 | +0.004 | +0.009 | +0.016 | +0.027 | +0.058 |
| MNQ | 15 | -0.040 | -0.017 | -0.007 | -0.005 | -0.003 | +0.000 | +0.003 | +0.005 | +0.011 | +0.039 | +0.108 |
| MNQ | 60 | -0.118 | -0.043 | -0.020 | -0.009 | -0.006 | +0.000 | +0.002 | +0.010 | +0.029 | +0.071 | +0.151 |
| MYM | 5 | -0.042 | -0.019 | -0.012 | -0.009 | -0.005 | +0.000 | +0.011 | +0.024 | +0.049 | +0.103 | +0.208 |
| MYM | 15 | -0.150 | -0.085 | -0.043 | -0.024 | -0.013 | +0.000 | +0.021 | +0.040 | +0.081 | +0.177 | +0.410 |
| MYM | 60 | -0.474 | -0.238 | -0.133 | -0.070 | -0.035 | +0.000 | +0.033 | +0.076 | +0.139 | +0.243 | +0.378 |

## Calibration

- MES 5-min: 1036271 bars, 48014 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 15892 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3921 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 47888 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 15883 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 3920 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 24139 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 7989 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1962 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
