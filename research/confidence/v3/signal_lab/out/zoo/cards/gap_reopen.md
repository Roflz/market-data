# Impact card: gap_reopen

18:00 reopen gap vs prior session close, in average daily ranges (ADR20) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (5 min), p=0.15; we would catch an effect of 0.026 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=1).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.064 R20 over the next 8 bars (2 h), p=0.38; we would catch an effect of 0.049 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.97 at recent bar sizes, 90% range up to $1.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.114 R20 over the next 8 bars (8 h), p=0.4; we would catch an effect of 0.096 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.53 at recent bar sizes, 90% range up to $6.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (5 min), p=0.076; we would catch an effect of 0.032 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=1).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.10 at recent bar sizes, 90% range up to $1.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (15 min), p=0.21; we would catch an effect of 0.068 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $3.55); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.019 R20 over the next 1 bar (1 h), p=0.26; we would catch an effect of 0.104 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.96 at recent bar sizes, 90% range up to $12.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.200 R20 over the next 16 bars (80 min), p=0.49; we would catch an effect of 0.053 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.27 at recent bar sizes, 90% range up to $1.57); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.356 R20 over the next 16 bars (4 h), p=0.36; we would catch an effect of 0.074 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.02 at recent bar sizes, 90% range up to $3.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.108 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.139 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.56).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.51 at recent bar sizes, 90% range up to $5.91); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.005 | +0.001 .. +0.009 | +0.0021 | 0.026 / 0.026 / 0.029 | 0.0287 | 1 | 0.992 | 11/16 | +0.004 | +0.006 | False | +2.2 / +2.2 |  |
| MES | 5 | h2 | +0.009 | +0.001 .. +0.018 | +0.0029 | 0.029 / 0.029 / 0.036 | 0.0357 |  |  | 11/16 | +0.007 | +0.012 |  | +2.9 / +2.2 |  |
| MES | 5 | h4 | +0.019 | +0.002 .. +0.036 | +0.0042 | 0.03 / 0.029 / 0.041 | 0.0393 |  |  | 11/16 | +0.012 | +0.026 |  | +4.1 / +2.2 | 0.026 |
| MES | 5 | h8 | +0.039 | +0.004 .. +0.074 | +0.0060 | 0.03 / 0.029 / 0.042 | 0.0419 |  |  | 11/16 | +0.021 | +0.056 |  | +5.8 / +2.2 |  |
| MES | 5 | h16 | +0.079 | +0.006 .. +0.152 | +0.0086 | 0.035 / 0.034 / 0.043 | 0.0404 |  |  | 10/16 | +0.038 | +0.119 |  | +8.2 / +2.1 |  |
| MES | 5 | eod | +1.156 | +0.020 .. +2.291 | +0.0214 | 0.046 / 0.044 / 0.077 | 0.0748 |  |  | 12/16 | +0.970 | +1.339 |  | +25.4 / +2.0 |  |
| MES | 15 | h1 | +0.006 | -0.003 .. +0.014 | +0.0016 | 0.19 / 0.2 / 0.19 | 0.198 |  |  | 9/16 | +0.004 | +0.007 |  | +1.3 / +1.3 |  |
| MES | 15 | h2 | +0.014 | -0.002 .. +0.030 | +0.0034 | 0.093 / 0.097 / 0.11 | 0.11 |  |  | 10/16 | +0.008 | +0.019 |  | +2.2 / +1.7 |  |
| MES | 15 | h4 | +0.030 | -0.002 .. +0.063 | +0.0054 | 0.067 / 0.068 / 0.085 | 0.0849 |  |  | 10/16 | +0.015 | +0.045 |  | +3.5 / +1.8 | 0.049 |
| MES | 15 | h8 * | +0.064 | -0.003 .. +0.130 | +0.0077 | 0.063 / 0.062 / 0.074 | 0.0742 | 1 | 0.998 | 10/16 | +0.030 | +0.097 | False | +5.0 / +1.9 |  |
| MES | 15 | h16 | +0.131 | -0.009 .. +0.271 | +0.0105 | 0.067 / 0.064 / 0.076 | 0.0784 |  |  | 10/16 | +0.062 | +0.199 |  | +7.2 / +1.8 |  |
| MES | 15 | eod | +0.653 | +0.030 .. +1.277 | +0.0217 | 0.04 / 0.038 / 0.08 | 0.0808 |  |  | 12/16 | +0.558 | +0.747 |  | +15.2 / +2.1 |  |
| MES | 60 | h1 | +0.013 | -0.003 .. +0.030 | +0.0043 | 0.11 / 0.1 / 0.13 | 0.129 |  |  | 11/16 | +0.010 | +0.017 |  | +1.6 / +1.6 |  |
| MES | 60 | h2 | +0.026 | -0.006 .. +0.059 | +0.0059 | 0.11 / 0.11 / 0.14 | 0.137 |  |  | 11/16 | +0.020 | +0.033 |  | +2.2 / +1.6 |  |
| MES | 60 | h4 | +0.053 | -0.010 .. +0.117 | +0.0083 | 0.1 / 0.098 / 0.12 | 0.125 |  |  | 12/16 | +0.039 | +0.067 |  | +3.2 / +1.6 | 0.096 |
| MES | 60 | h8 * | +0.114 | -0.008 .. +0.236 | +0.0132 | 0.067 / 0.066 / 0.089 | 0.0886 | 1 | 1 | 11/16 | +0.096 | +0.132 | False | +5.1 / +1.8 |  |
| MES | 60 | h16 | +0.200 | -0.015 .. +0.415 | +0.0172 | 0.069 / 0.067 / 0.097 | 0.0985 |  |  | 12/16 | +0.190 | +0.210 |  | +6.8 / +1.8 |  |
| MES | 60 | eod | +0.224 | -0.013 .. +0.461 | +0.0189 | 0.064 / 0.065 / 0.098 | 0.0977 |  |  | 12/16 | +0.220 | +0.228 |  | +7.3 / +1.8 |  |
| MNQ | 5 | h1 * | +0.007 | +0.001 .. +0.012 | +0.0024 | 0.013 / 0.0098 / 0.0088 | 0.00703 | 1 | 0.823 | 12/16 | +0.003 | +0.011 | False | +2.5 / +2.5 |  |
| MNQ | 5 | h2 | +0.016 | +0.003 .. +0.028 | +0.0034 | 0.016 / 0.012 / 0.0092 | 0.00677 |  |  | 11/16 | +0.006 | +0.025 |  | +3.4 / +2.4 |  |
| MNQ | 5 | h4 | +0.032 | +0.007 .. +0.057 | +0.0043 | 0.013 / 0.0093 / 0.014 | 0.0141 |  |  | 11/16 | +0.012 | +0.051 |  | +4.7 / +2.5 | 0.032 |
| MNQ | 5 | h8 | +0.062 | +0.016 .. +0.107 | +0.0052 | 0.0081 / 0.0062 / 0.019 | 0.0169 |  |  | 11/16 | +0.026 | +0.096 |  | +6.8 / +2.6 |  |
| MNQ | 5 | h16 | +0.118 | +0.032 .. +0.205 | +0.0065 | 0.0075 / 0.0066 / 0.023 | 0.0193 |  |  | 11/16 | +0.064 | +0.172 |  | +9.8 / +2.7 |  |
| MNQ | 5 | eod | +1.684 | +0.243 .. +3.124 | +0.0215 | 0.022 / 0.024 / 0.047 | 0.0521 |  |  | 14/16 | +1.743 | +1.625 |  | +27.7 / +2.3 |  |
| MNQ | 15 | h1 * | +0.009 | +0.001 .. +0.018 | +0.0029 | 0.035 / 0.034 / 0.04 | 0.0427 | 1 | 0.996 | 11/16 | +0.005 | +0.014 | False | +2.1 / +2.1 |  |
| MNQ | 15 | h2 | +0.020 | +0.002 .. +0.037 | +0.0031 | 0.026 / 0.027 / 0.065 | 0.068 |  |  | 11/16 | +0.009 | +0.030 |  | +3.1 / +2.2 |  |
| MNQ | 15 | h4 | +0.041 | +0.005 .. +0.076 | +0.0036 | 0.025 / 0.027 / 0.095 | 0.101 |  |  | 11/16 | +0.019 | +0.062 |  | +4.4 / +2.2 | 0.068 |
| MNQ | 15 | h8 | +0.079 | +0.006 .. +0.152 | +0.0055 | 0.035 / 0.038 / 0.085 | 0.087 |  |  | 13/16 | +0.036 | +0.121 |  | +5.8 / +2.1 |  |
| MNQ | 15 | h16 | +0.147 | -0.006 .. +0.299 | +0.0073 | 0.06 / 0.064 / 0.12 | 0.122 |  |  | 13/16 | +0.052 | +0.240 |  | +7.3 / +1.9 |  |
| MNQ | 15 | eod | +0.780 | +0.071 .. +1.488 | +0.0159 | 0.031 / 0.034 / 0.099 | 0.103 |  |  | 14/16 | +0.758 | +0.801 |  | +15.5 / +2.2 |  |
| MNQ | 60 | h1 * | +0.019 | +0.002 .. +0.035 | +0.0061 | 0.029 / 0.031 / 0.048 | 0.05 | 1 | 0.99 | 13/16 | +0.014 | +0.023 | False | +2.1 / +2.2 |  |
| MNQ | 60 | h2 | +0.038 | +0.004 .. +0.071 | +0.0084 | 0.029 / 0.031 / 0.048 | 0.0487 |  |  | 14/16 | +0.031 | +0.044 |  | +2.9 / +2.2 |  |
| MNQ | 60 | h4 | +0.071 | +0.005 .. +0.137 | +0.0111 | 0.036 / 0.039 / 0.059 | 0.0602 |  |  | 13/16 | +0.061 | +0.081 |  | +4.0 / +2.1 | 0.104 |
| MNQ | 60 | h8 | +0.133 | +0.007 .. +0.258 | +0.0151 | 0.038 / 0.043 / 0.065 | 0.0706 |  |  | 12/16 | +0.125 | +0.140 |  | +5.5 / +2.1 |  |
| MNQ | 60 | h16 | +0.230 | +0.006 .. +0.454 | +0.0200 | 0.045 / 0.05 / 0.076 | 0.0808 |  |  | 12/16 | +0.262 | +0.198 |  | +7.3 / +2.0 |  |
| MNQ | 60 | eod | +0.255 | +0.007 .. +0.502 | +0.0213 | 0.044 / 0.05 / 0.077 | 0.0821 |  |  | 11/16 | +0.313 | +0.197 |  | +7.7 / +2.0 |  |
| MYM | 5 | h1 | +0.009 | -0.003 .. +0.021 | +0.0033 | 0.13 / 0.15 / 0.026 | 0.029 |  |  | 6/8 | n/a | +0.009 |  | +1.9 / +1.5 |  |
| MYM | 5 | h2 | +0.026 | -0.007 .. +0.060 | +0.0057 | 0.13 / 0.14 / 0.0069 | 0.0126 |  |  | 6/8 | n/a | +0.026 |  | +2.8 / +1.5 |  |
| MYM | 5 | h4 | +0.063 | -0.016 .. +0.142 | +0.0083 | 0.12 / 0.13 / 0.0041 | 0.00843 |  |  | 7/8 | n/a | +0.063 |  | +3.9 / +1.6 | 0.053 |
| MYM | 5 | h8 | +0.121 | -0.025 .. +0.267 | +0.0111 | 0.1 / 0.12 / 0.0041 | 0.00843 |  |  | 7/8 | n/a | +0.121 |  | +5.5 / +1.6 |  |
| MYM | 5 | h16 * | +0.200 | -0.016 .. +0.417 | +0.0143 | 0.069 / 0.082 / 0.0096 | 0.0148 | 1 | 1 | 7/8 | n/a | +0.200 | False | +7.6 / +1.8 |  |
| MYM | 5 | eod | +1.635 | -0.446 .. +3.716 | +0.0211 | 0.12 / 0.12 / 0.16 | 0.156 |  |  | 5/8 | n/a | +1.635 |  | +17.1 / +1.5 |  |
| MYM | 15 | h1 | +0.014 | -0.000 .. +0.028 | +0.0051 | 0.053 / 0.062 / 0.038 | 0.0411 |  |  | 7/8 | n/a | +0.014 |  | +1.9 / +1.9 |  |
| MYM | 15 | h2 | +0.042 | -0.003 .. +0.087 | +0.0082 | 0.066 / 0.078 / 0.014 | 0.0158 |  |  | 7/8 | n/a | +0.042 |  | +2.6 / +1.8 |  |
| MYM | 15 | h4 | +0.092 | -0.006 .. +0.189 | +0.0102 | 0.067 / 0.08 / 0.015 | 0.0148 |  |  | 7/8 | n/a | +0.092 |  | +3.1 / +1.8 | 0.074 |
| MYM | 15 | h8 | +0.171 | -0.003 .. +0.345 | +0.0141 | 0.054 / 0.065 / 0.017 | 0.0195 |  |  | 7/8 | n/a | +0.171 |  | +4.4 / +1.9 |  |
| MYM | 15 | h16 * | +0.356 | -0.001 .. +0.712 | +0.0207 | 0.05 / 0.061 / 0.017 | 0.0174 | 1 | 0.999 | 7/8 | n/a | +0.356 | False | +7.2 / +2.0 |  |
| MYM | 15 | eod | +1.074 | -0.309 .. +2.457 | +0.0230 | 0.13 / 0.13 / 0.1 | 0.107 |  |  | 5/8 | n/a | +1.074 |  | +8.7 / +1.5 |  |
| MYM | 60 | h1 | +0.013 | -0.009 .. +0.036 | +0.0040 | 0.24 / 0.25 / 0.32 | 0.325 |  |  | 4/8 | n/a | +0.013 |  | +1.1 / +1.2 |  |
| MYM | 60 | h2 | +0.026 | -0.019 .. +0.071 | +0.0054 | 0.26 / 0.27 / 0.34 | 0.344 |  |  | 4/8 | n/a | +0.026 |  | +1.5 / +1.1 |  |
| MYM | 60 | h4 | +0.054 | -0.034 .. +0.143 | +0.0082 | 0.23 / 0.24 / 0.31 | 0.32 |  |  | 4/8 | n/a | +0.054 |  | +2.2 / +1.2 | 0.139 |
| MYM | 60 | h8 * | +0.108 | -0.066 .. +0.282 | +0.0128 | 0.22 / 0.23 / 0.29 | 0.302 | 1 | 1 | 5/8 | n/a | +0.108 | False | +3.3 / +1.2 |  |
| MYM | 60 | h16 | +0.172 | -0.140 .. +0.484 | +0.0144 | 0.28 / 0.27 / 0.35 | 0.357 |  |  | 5/8 | n/a | +0.172 |  | +4.0 / +1.1 |  |
| MYM | 60 | eod | +0.160 | -0.190 .. +0.511 | +0.0128 | 0.37 / 0.36 / 0.43 | 0.437 |  |  | 5/8 | n/a | +0.160 |  | +3.6 / +0.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.000 | -0.003 .. +0.003 | -0.0% | +0.001 | 0.95 |  | 7/16 |
| MES | 5 | h2 * | -0.004 | -0.010 .. +0.002 | -0.6% | -0.003 | 0.28 | 1 | 8/16 |
| MES | 5 | h4 | -0.006 | -0.017 .. +0.006 | -0.6% | -0.008 | 0.56 |  | 8/16 |
| MES | 5 | h8 | -0.008 | -0.029 .. +0.014 | -0.5% | -0.016 | 0.69 |  | 10/16 |
| MES | 5 | h16 | +0.014 | -0.025 .. +0.054 | +0.7% | -0.016 | 0.49 |  | 7/16 |
| MES | 5 | eod | -0.084 | -0.801 .. +0.633 | -0.8% | +0.214 | 0.99 |  | 7/16 |
| MES | 15 | h1 | -0.003 | -0.009 .. +0.003 | -0.6% | -0.006 | 0.39 |  | 8/16 |
| MES | 15 | h2 | -0.006 | -0.018 .. +0.006 | -0.8% | -0.012 | 0.5 |  | 9/16 |
| MES | 15 | h4 | -0.001 | -0.022 .. +0.019 | -0.1% | -0.019 | 0.91 |  | 7/16 |
| MES | 15 | h8 | +0.011 | -0.028 .. +0.051 | +0.7% | -0.023 | 0.59 |  | 9/16 |
| MES | 15 | h16 * | +0.043 | -0.031 .. +0.117 | +1.9% | -0.030 | 0.27 | 1 | 10/16 |
| MES | 15 | eod | -0.138 | -0.538 .. +0.261 | -2.5% | -0.066 | 0.77 |  | 8/16 |
| MES | 60 | h1 | -0.001 | -0.013 .. +0.011 | -0.2% | -0.012 | 0.94 |  | 7/16 |
| MES | 60 | h2 | +0.008 | -0.012 .. +0.028 | +1.0% | -0.007 | 0.46 |  | 8/16 |
| MES | 60 | h4 * | +0.023 | -0.014 .. +0.060 | +2.2% | +0.001 | 0.24 | 1 | 10/16 |
| MES | 60 | h8 | +0.023 | -0.044 .. +0.091 | +1.6% | +0.005 | 0.5 |  | 8/16 |
| MES | 60 | h16 | -0.012 | -0.138 .. +0.113 | -0.6% | -0.004 | 0.95 |  | 7/16 |
| MES | 60 | eod | -0.030 | -0.172 .. +0.111 | -1.4% | -0.018 | 0.79 |  | 8/16 |
| MNQ | 5 | h1 | -0.001 | -0.006 .. +0.003 | -0.3% | -0.000 | 0.66 |  | 8/16 |
| MNQ | 5 | h2 * | -0.005 | -0.017 .. +0.007 | -0.7% | -0.005 | 0.53 | 1 | 7/16 |
| MNQ | 5 | h4 | -0.009 | -0.033 .. +0.014 | -0.8% | -0.015 | 0.62 |  | 7/16 |
| MNQ | 5 | h8 | -0.017 | -0.055 .. +0.021 | -1.0% | -0.039 | 0.67 |  | 10/16 |
| MNQ | 5 | h16 | +0.005 | -0.047 .. +0.057 | +0.2% | -0.060 | 0.87 |  | 11/16 |
| MNQ | 5 | eod | -0.048 | -0.968 .. +0.872 | -0.4% | +0.214 | 0.97 |  | 6/16 |
| MNQ | 15 | h1 | -0.001 | -0.006 .. +0.005 | -0.1% | -0.001 | 0.91 |  | 7/16 |
| MNQ | 15 | h2 | -0.002 | -0.013 .. +0.009 | -0.2% | -0.005 | 0.94 |  | 8/16 |
| MNQ | 15 | h4 | +0.006 | -0.014 .. +0.027 | +0.6% | -0.011 | 0.66 |  | 12/16 |
| MNQ | 15 | h8 | +0.017 | -0.023 .. +0.057 | +1.0% | -0.012 | 0.57 |  | 11/16 |
| MNQ | 15 | h16 * | +0.064 | -0.018 .. +0.147 | +2.6% | +0.004 | 0.27 | 1 | 11/16 |
| MNQ | 15 | eod | -0.126 | -0.574 .. +0.323 | -2.0% | -0.005 | 0.86 |  | 9/16 |
| MNQ | 60 | h1 | +0.002 | -0.010 .. +0.014 | +0.4% | -0.007 | 0.76 |  | 7/16 |
| MNQ | 60 | h2 | +0.004 | -0.017 .. +0.025 | +0.5% | -0.002 | 0.72 |  | 8/16 |
| MNQ | 60 | h4 * | +0.017 | -0.022 .. +0.055 | +1.5% | +0.006 | 0.41 | 1 | 9/16 |
| MNQ | 60 | h8 | +0.007 | -0.064 .. +0.078 | +0.4% | +0.006 | 0.85 |  | 7/16 |
| MNQ | 60 | h16 | -0.031 | -0.164 .. +0.101 | -1.4% | -0.011 | 0.81 |  | 8/16 |
| MNQ | 60 | eod | -0.052 | -0.203 .. +0.099 | -2.3% | -0.015 | 0.66 |  | 10/16 |
| MYM | 5 | h1 | -0.002 | -0.014 .. +0.010 | -0.4% | -0.003 | 0.75 |  | 3/8 |
| MYM | 5 | h2 | -0.018 | -0.052 .. +0.016 | -2.3% | -0.020 | 0.31 |  | 5/8 |
| MYM | 5 | h4 | -0.042 | -0.122 .. +0.038 | -3.8% | -0.058 | 0.31 |  | 3/8 |
| MYM | 5 | h8 * | -0.080 | -0.231 .. +0.070 | -5.1% | -0.130 | 0.3 | 1 | 3/8 |
| MYM | 5 | h16 | -0.081 | -0.290 .. +0.128 | -3.5% | -0.218 | 0.45 |  | 4/8 |
| MYM | 5 | eod | -0.282 | -1.775 .. +1.211 | -2.4% | -0.275 | 0.74 |  | 5/8 |
| MYM | 15 | h1 | -0.005 | -0.018 .. +0.008 | -1.0% | -0.012 | 0.48 |  | 5/8 |
| MYM | 15 | h2 * | -0.027 | -0.073 .. +0.019 | -3.6% | -0.045 | 0.25 | 1 | 5/8 |
| MYM | 15 | h4 | -0.060 | -0.173 .. +0.053 | -5.4% | -0.110 | 0.33 |  | 5/8 |
| MYM | 15 | h8 | -0.083 | -0.274 .. +0.109 | -5.1% | -0.238 | 0.46 |  | 5/8 |
| MYM | 15 | h16 | -0.064 | -0.384 .. +0.255 | -2.6% | -0.422 | 0.82 |  | 5/8 |
| MYM | 15 | eod | -0.519 | -1.658 .. +0.619 | -8.7% | -0.641 | 0.41 |  | 5/8 |
| MYM | 60 | h1 | +0.011 | -0.006 .. +0.027 | +2.0% | +0.005 | 0.21 |  | 4/8 |
| MYM | 60 | h2 | +0.022 | -0.007 .. +0.050 | +2.9% | +0.013 | 0.14 |  | 4/8 |
| MYM | 60 | h4 * | +0.048 | -0.001 .. +0.097 | +4.5% | +0.032 | 0.093 | 1 | 5/8 |
| MYM | 60 | h8 | +0.069 | -0.022 .. +0.161 | +4.5% | +0.067 | 0.24 |  | 4/8 |
| MYM | 60 | h16 | +0.045 | -0.125 .. +0.216 | +2.1% | +0.077 | 0.76 |  | 3/8 |
| MYM | 60 | eod | +0.028 | -0.163 .. +0.220 | +1.3% | +0.070 | 0.9 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.58 pts | -0.06 .. +1.22 | 0.078 |
| MES | 15 | +0.41 pts | -0.60 .. +1.43 | 0.43 |
| MES | 60 | +2.49 pts | +0.26 .. +4.73 | 0.034 |
| MNQ | 5 | +0.72 pts | +0.14 .. +1.31 | 0.016 |
| MNQ | 15 | +0.64 pts | -0.45 .. +1.72 | 0.25 |
| MNQ | 60 | +1.81 pts | -0.57 .. +4.19 | 0.14 |
| MYM | 5 | +0.70 pts | -0.14 .. +1.54 | 0.12 |
| MYM | 15 | +0.21 pts | -1.11 .. +1.54 | 0.76 |
| MYM | 60 | +1.12 pts | -2.04 .. +4.28 | 0.5 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | long | 203480 | +0.004 | 0.294 | +0.04 | -3.46 | -3.48 | -3.44 | -3.46 |
| MES | 5 | h2 | top fifth | long | 203480 | +0.008 | 0.294 | +0.09 | -3.41 | -3.45 | -3.37 | -3.42 |
| MES | 5 | h4 | top fifth | long | 203480 | +0.017 | 0.294 | +0.20 | -3.30 | -3.39 | -3.22 | -3.34 |
| MES | 5 | h8 | top fifth | long | 203480 | +0.035 | 0.294 | +0.41 | -3.09 | -3.27 | -2.93 | -3.20 |
| MES | 5 | h16 | top fifth | long | 203480 | +0.072 | 0.294 | +0.83 | -2.67 | -3.02 | -2.34 | -2.94 |
| MES | 5 | eod | top fifth | long | 203480 | +0.933 | 0.294 | +10.51 | +7.01 | +2.98 | +10.85 | +5.55 |
| MES | 15 | h1 | top fifth | long | 67346 | +0.006 | 0.168 | +0.13 | -3.37 | -3.43 | -3.31 | -3.42 |
| MES | 15 | h2 | top fifth | long | 67346 | +0.014 | 0.168 | +0.29 | -3.21 | -3.33 | -3.09 | -3.30 |
| MES | 15 | h4 | top fifth | long | 67346 | +0.029 | 0.168 | +0.60 | -2.90 | -3.15 | -2.65 | -3.07 |
| MES | 15 | h8 | top fifth | long | 67346 | +0.059 | 0.168 | +1.26 | -2.24 | -2.76 | -1.74 | -2.58 |
| MES | 15 | h16 | top fifth | long | 67346 | +0.118 | 0.168 | +2.73 | -0.77 | -1.96 | +0.36 | -1.33 |
| MES | 15 | eod | top fifth | long | 67346 | +0.505 | 0.168 | +10.48 | +6.98 | +2.97 | +10.79 | +6.08 |
| MES | 60 | h1 | top fifth | long | 16594 | +0.012 | 0.082 | +0.61 | -2.89 | -3.13 | -2.67 | -3.08 |
| MES | 60 | h2 | top fifth | long | 16594 | +0.024 | 0.082 | +1.30 | -2.20 | -2.75 | -1.68 | -2.64 |
| MES | 60 | h4 | top fifth | long | 16594 | +0.050 | 0.082 | +2.79 | -0.71 | -1.95 | +0.48 | -1.69 |
| MES | 60 | h8 | top fifth | long | 16594 | +0.105 | 0.082 | +5.68 | +2.18 | -0.01 | +4.28 | +0.30 |
| MES | 60 | h16 | top fifth | long | 16594 | +0.173 | 0.082 | +9.42 | +5.92 | +2.32 | +9.36 | +2.88 |
| MES | 60 | eod | top fifth | long | 16594 | +0.198 | 0.082 | +10.38 | +6.88 | +2.91 | +10.68 | +3.29 |
| MNQ | 5 | h1 | top fifth | long | 203162 | +0.006 | 0.115 | +0.06 | -1.94 | -1.98 | -1.92 | -1.96 |
| MNQ | 5 | h2 | top fifth | long | 203162 | +0.013 | 0.115 | +0.12 | -1.88 | -1.94 | -1.81 | -1.88 |
| MNQ | 5 | h4 | top fifth | long | 203162 | +0.027 | 0.115 | +0.26 | -1.74 | -1.88 | -1.61 | -1.74 |
| MNQ | 5 | h8 | top fifth | long | 203162 | +0.055 | 0.115 | +0.53 | -1.47 | -1.76 | -1.20 | -1.52 |
| MNQ | 5 | h16 | top fifth | long | 203162 | +0.111 | 0.115 | +1.10 | -0.90 | -1.50 | -0.35 | -1.18 |
| MNQ | 5 | eod | top fifth | long | 203162 | +1.167 | 0.115 | +10.32 | +8.32 | +4.70 | +11.64 | +9.09 |
| MNQ | 15 | h1 | top fifth | long | 67395 | +0.010 | 0.065 | +0.17 | -1.83 | -1.91 | -1.75 | -1.96 |
| MNQ | 15 | h2 | top fifth | long | 67395 | +0.020 | 0.065 | +0.38 | -1.62 | -1.82 | -1.44 | -1.78 |
| MNQ | 15 | h4 | top fifth | long | 67395 | +0.040 | 0.065 | +0.79 | -1.21 | -1.62 | -0.82 | -1.51 |
| MNQ | 15 | h8 | top fifth | long | 67395 | +0.078 | 0.065 | +1.66 | -0.34 | -1.23 | +0.48 | -1.02 |
| MNQ | 15 | h16 | top fifth | long | 67395 | +0.146 | 0.065 | +3.35 | +1.35 | -0.43 | +2.98 | +0.68 |
| MNQ | 15 | eod | top fifth | long | 67395 | +0.533 | 0.065 | +10.28 | +8.28 | +4.69 | +11.60 | +9.17 |
| MNQ | 60 | h1 | top fifth | long | 16608 | +0.015 | 0.032 | +0.81 | -1.19 | -1.61 | -0.79 | -1.45 |
| MNQ | 60 | h2 | top fifth | long | 16608 | +0.030 | 0.032 | +1.69 | -0.31 | -1.21 | +0.52 | -0.85 |
| MNQ | 60 | h4 | top fifth | long | 16608 | +0.058 | 0.032 | +3.39 | +1.39 | -0.41 | +3.06 | +0.29 |
| MNQ | 60 | h8 | top fifth | long | 16608 | +0.113 | 0.032 | +6.53 | +4.53 | +1.34 | +7.49 | +2.50 |
| MNQ | 60 | h16 | top fifth | long | 16608 | +0.183 | 0.032 | +9.69 | +7.69 | +3.82 | +11.28 | +4.87 |
| MNQ | 60 | eod | top fifth | long | 16608 | +0.214 | 0.032 | +10.18 | +8.18 | +4.66 | +11.45 | +4.66 |
| MYM | 5 | h1 | top fifth | long | 101620 | +0.002 | 0.160 | +0.04 | -1.96 | +nan | -1.96 | -1.96 |
| MYM | 5 | h2 | top fifth | long | 101620 | +0.006 | 0.160 | +0.09 | -1.91 | +nan | -1.91 | -1.90 |
| MYM | 5 | h4 | top fifth | long | 101620 | +0.015 | 0.160 | +0.20 | -1.80 | +nan | -1.80 | -1.77 |
| MYM | 5 | h8 | top fifth | long | 101620 | +0.035 | 0.160 | +0.42 | -1.58 | +nan | -1.58 | -1.57 |
| MYM | 5 | h16 | top fifth | long | 101620 | +0.075 | 0.160 | +0.84 | -1.16 | +nan | -1.16 | -1.28 |
| MYM | 5 | eod | top fifth | long | 101620 | +1.244 | 0.160 | +10.60 | +8.60 | +nan | +8.60 | +6.11 |
| MYM | 15 | h1 | top fifth | long | 33634 | +0.007 | 0.090 | +0.14 | -1.86 | +nan | -1.86 | -1.89 |
| MYM | 15 | h2 | top fifth | long | 33634 | +0.015 | 0.090 | +0.30 | -1.70 | +nan | -1.70 | -1.67 |
| MYM | 15 | h4 | top fifth | long | 33634 | +0.031 | 0.090 | +0.63 | -1.37 | +nan | -1.37 | -1.30 |
| MYM | 15 | h8 | top fifth | long | 33634 | +0.061 | 0.090 | +1.23 | -0.77 | +nan | -0.77 | -0.64 |
| MYM | 15 | h16 | top fifth | long | 33634 | +0.126 | 0.090 | +2.73 | +0.73 | +nan | +0.73 | +1.20 |
| MYM | 15 | eod | top fifth | long | 33634 | +0.596 | 0.090 | +10.57 | +8.57 | +nan | +8.57 | +8.44 |
| MYM | 60 | h1 | top fifth | long | 8262 | +0.011 | 0.043 | +0.62 | -1.38 | +nan | -1.38 | -1.60 |
| MYM | 60 | h2 | top fifth | long | 8262 | +0.022 | 0.043 | +1.26 | -0.74 | +nan | -0.74 | -1.21 |
| MYM | 60 | h4 | top fifth | long | 8262 | +0.047 | 0.043 | +2.85 | +0.85 | +nan | +0.85 | -0.14 |
| MYM | 60 | h8 | top fifth | long | 8262 | +0.095 | 0.043 | +5.75 | +3.75 | +nan | +3.75 | +1.94 |
| MYM | 60 | h16 | top fifth | long | 8262 | +0.168 | 0.043 | +9.72 | +7.72 | +nan | +7.72 | +4.65 |
| MYM | 60 | eod | top fifth | long | 8262 | +0.195 | 0.043 | +10.63 | +8.63 | +nan | +8.63 | +4.73 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.139 | +0.074 | +0.028 | +0.008 | +0.002 | +0.000 | +0.004 | +0.008 | +0.017 | +0.035 | +0.070 |
| MES | 15 | +0.209 | +0.119 | +0.048 | +0.015 | +0.004 | +0.000 | +0.008 | +0.015 | +0.030 | +0.060 | +0.128 |
| MES | 60 | +0.047 | +0.029 | +0.018 | +0.006 | -0.000 | +0.000 | +0.012 | +0.023 | +0.046 | +0.114 | +0.205 |
| MNQ | 5 | +0.159 | +0.083 | +0.031 | +0.010 | +0.003 | +0.000 | +0.007 | +0.014 | +0.028 | +0.055 | +0.102 |
| MNQ | 15 | +0.218 | +0.119 | +0.046 | +0.015 | +0.004 | +0.000 | +0.010 | +0.019 | +0.037 | +0.070 | +0.130 |
| MNQ | 60 | +0.075 | +0.055 | +0.021 | +0.001 | -0.004 | +0.000 | +0.016 | +0.034 | +0.062 | +0.126 | +0.216 |
| MYM | 5 | +0.133 | +0.071 | +0.026 | +0.006 | -0.000 | +0.000 | +0.017 | +0.034 | +0.070 | +0.130 | +0.219 |
| MYM | 15 | +0.152 | +0.093 | +0.030 | +0.004 | -0.004 | +0.000 | +0.030 | +0.057 | +0.109 | +0.200 | +0.446 |
| MYM | 60 | -0.105 | -0.061 | -0.015 | -0.003 | -0.005 | +0.000 | +0.014 | +0.027 | +0.062 | +0.177 | +0.323 |

## Calibration

- MES 5-min: 1018598 bars, 203480 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 337156 bars, 67346 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83051 bars, 16594 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1016931 bars, 203162 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 337005 bars, 67395 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83049 bars, 16608 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 508256 bars, 101620 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 168240 bars, 33634 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41312 bars, 8262 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
