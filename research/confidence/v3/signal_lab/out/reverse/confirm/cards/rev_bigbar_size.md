# Impact card: rev_bigbar_size

last bar's range / average bar; big bar -> bigger move next hour

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (15 min), p=0.5; we would catch an effect of 0.053 R20 or more 80% of the time).
- MES 15-min size: the market moves 22% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.116 R20, CONFIRMED, q=8.1e-51, 8 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.06 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.128 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best -0.032 R20 over the next 4 bars (1 h), p=0.82; we would catch an effect of 0.064 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 21% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.110 R20, CONFIRMED, q=4.6e-56, 8 of 8 years same sign).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.67 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.044 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.183 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.062 R20 or more 80% of the time).
- MYM 15-min size: the market moves 22% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.115 R20, CONFIRMED, q=1.18e-37, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.75 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.098 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.012 | -0.026 .. +0.001 | -0.0055 | 0.065 / 0.084 / 0.0075 | 0.00685 | 1 | 0.783 | 4/8 | n/a | -0.012 | False | -1.8 / -1.8 |  |
| MES | 15 | h2 | -0.016 | -0.039 .. +0.006 | -0.0043 | 0.15 / 0.18 / 0.026 | 0.0258 |  |  | 5/8 | n/a | -0.016 |  | -1.6 / -1.4 |  |
| MES | 15 | h4 | -0.024 | -0.063 .. +0.014 | -0.0044 | 0.22 / 0.23 / 0.037 | 0.0443 |  |  | 4/8 | n/a | -0.024 |  | -1.8 / -1.2 | 0.053 |
| MES | 15 | h8 | -0.007 | -0.075 .. +0.061 | +0.0009 | 0.84 / 0.84 / 0.71 | 0.705 |  |  | 4/8 | n/a | -0.007 |  | -0.4 / -0.2 |  |
| MES | 15 | h16 | -0.017 | -0.112 .. +0.077 | -0.0013 | 0.72 / 0.73 / 0.55 | 0.537 |  |  | 4/8 | n/a | -0.017 |  | -0.7 / -0.4 |  |
| MES | 15 | eod | +0.102 | -0.136 .. +0.339 | +0.0107 | 0.4 / 0.41 / 0.12 | 0.117 |  |  | 5/8 | n/a | +0.102 |  | +1.5 / +0.8 |  |
| MNQ | 15 | h1 | -0.010 | -0.022 .. +0.003 | -0.0066 | 0.13 / 0.16 / 0.039 | 0.04 |  |  | 5/8 | n/a | -0.010 |  | -1.4 / -1.5 |  |
| MNQ | 15 | h2 | -0.015 | -0.037 .. +0.007 | -0.0030 | 0.19 / 0.21 / 0.045 | 0.0448 |  |  | 5/8 | n/a | -0.015 |  | -1.4 / -1.3 |  |
| MNQ | 15 | h4 * | -0.032 | -0.072 .. +0.009 | -0.0021 | 0.12 / 0.14 / 0.0073 | 0.0058 | 1 | 0.937 | 6/8 | n/a | -0.032 | False | -1.9 / -1.5 | 0.064 |
| MNQ | 15 | h8 | -0.007 | -0.078 .. +0.065 | +0.0047 | 0.86 / 0.86 / 0.71 | 0.703 |  |  | 4/8 | n/a | -0.007 |  | -0.3 / -0.2 |  |
| MNQ | 15 | h16 | +0.005 | -0.094 .. +0.104 | -0.0028 | 0.93 / 0.93 / 0.86 | 0.865 |  |  | 3/8 | n/a | +0.005 |  | +0.2 / +0.1 |  |
| MNQ | 15 | eod | +0.023 | -0.151 .. +0.196 | +0.0073 | 0.8 / 0.81 / 0.74 | 0.747 |  |  | 3/8 | n/a | +0.023 |  | +0.3 / +0.3 |  |
| MYM | 15 | h1 | -0.004 | -0.017 .. +0.009 | -0.0011 | 0.57 / 0.61 / 0.41 | 0.403 |  |  | 4/8 | n/a | -0.004 |  | -0.5 / -0.6 |  |
| MYM | 15 | h2 | -0.007 | -0.030 .. +0.017 | -0.0017 | 0.58 / 0.6 / 0.4 | 0.403 |  |  | 4/8 | n/a | -0.007 |  | -0.6 / -0.6 |  |
| MYM | 15 | h4 | -0.019 | -0.059 .. +0.021 | -0.0011 | 0.36 / 0.38 / 0.11 | 0.101 |  |  | 5/8 | n/a | -0.019 |  | -1.3 / -0.9 | 0.062 |
| MYM | 15 | h8 | -0.014 | -0.085 .. +0.058 | -0.0004 | 0.71 / 0.71 / 0.45 | 0.454 |  |  | 4/8 | n/a | -0.014 |  | -0.7 / -0.4 |  |
| MYM | 15 | h16 | +0.010 | -0.091 .. +0.111 | -0.0017 | 0.84 / 0.84 / 0.71 | 0.719 |  |  | 5/8 | n/a | +0.010 |  | +0.4 / +0.2 |  |
| MYM | 15 | eod * | +0.183 | -0.109 .. +0.475 | +0.0129 | 0.22 / 0.22 / 0.012 | 0.01 | 1 | 0.979 | 4/8 | n/a | +0.183 | False | +2.2 / +1.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.116 | +0.101 .. +0.131 | +22.4% | +0.250 | 9.6e-54 | 8.1e-51 | 8/8 |
| MES | 15 | h2 | +0.145 | +0.127 .. +0.164 | +19.5% | +0.308 | 8.3e-53 |  | 8/8 |
| MES | 15 | h4 | +0.176 | +0.145 .. +0.206 | +16.3% | +0.358 | 2e-29 |  | 8/8 |
| MES | 15 | h8 | +0.205 | +0.156 .. +0.254 | +13.0% | +0.401 | 1.9e-16 |  | 7/8 |
| MES | 15 | h16 | +0.267 | +0.188 .. +0.346 | +11.3% | +0.467 | 3.3e-11 |  | 7/8 |
| MES | 15 | eod | +0.299 | +0.088 .. +0.510 | +5.2% | +0.681 | 0.0054 |  | 6/8 |
| MNQ | 15 | h1 * | +0.110 | +0.097 .. +0.123 | +21.1% | +0.228 | 2.7e-59 | 4.6e-56 | 8/8 |
| MNQ | 15 | h2 | +0.139 | +0.120 .. +0.158 | +18.4% | +0.282 | 3.1e-46 |  | 8/8 |
| MNQ | 15 | h4 | +0.163 | +0.132 .. +0.194 | +14.8% | +0.331 | 5.5e-25 |  | 8/8 |
| MNQ | 15 | h8 | +0.199 | +0.150 .. +0.247 | +12.2% | +0.398 | 1.5e-15 |  | 7/8 |
| MNQ | 15 | h16 | +0.239 | +0.169 .. +0.309 | +9.8% | +0.460 | 2.2e-11 |  | 7/8 |
| MNQ | 15 | eod | +0.403 | +0.262 .. +0.544 | +6.5% | +0.678 | 2.6e-08 |  | 8/8 |
| MYM | 15 | h1 * | +0.115 | +0.098 .. +0.132 | +21.7% | +0.249 | 2.8e-40 | 1.18e-37 | 8/8 |
| MYM | 15 | h2 | +0.145 | +0.121 .. +0.170 | +19.1% | +0.307 | 1.8e-30 |  | 8/8 |
| MYM | 15 | h4 | +0.176 | +0.136 .. +0.215 | +16.0% | +0.363 | 3.3e-18 |  | 7/8 |
| MYM | 15 | h8 | +0.205 | +0.147 .. +0.263 | +12.7% | +0.428 | 3.8e-12 |  | 7/8 |
| MYM | 15 | h16 | +0.233 | +0.155 .. +0.312 | +9.6% | +0.450 | 5.4e-09 |  | 6/8 |
| MYM | 15 | eod | +0.261 | +0.005 .. +0.517 | +4.4% | +0.663 | 0.046 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.39 pts | -1.40 .. +0.62 | 0.45 |
| MNQ | 15 | -0.57 pts | -1.53 .. +0.39 | 0.25 |
| MYM | 15 | +0.18 pts | -0.88 .. +1.25 | 0.99 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top fifth | short | 34301 | +0.002 | 0.139 | +0.13 | -3.37 | +nan | -3.37 | -3.21 |
| MES | 15 | h2 | bottom fifth | long | 34318 | +0.004 | 0.119 | +0.18 | -3.32 | +nan | -3.32 | -3.28 |
| MES | 15 | h4 | bottom fifth | long | 34318 | +0.011 | 0.119 | +0.59 | -2.91 | +nan | -2.91 | -2.91 |
| MES | 15 | h8 | bottom fifth | long | 34318 | +0.012 | 0.119 | +0.80 | -2.70 | +nan | -2.70 | -2.75 |
| MES | 15 | h16 | bottom fifth | long | 34318 | +0.039 | 0.119 | +1.77 | -1.73 | +nan | -1.73 | -2.25 |
| MES | 15 | eod | top fifth | long | 34301 | +0.253 | 0.139 | +5.05 | +1.55 | +nan | +1.55 | +1.17 |
| MNQ | 15 | h1 | bottom fifth | long | 34301 | +0.005 | 0.041 | +0.18 | -1.82 | +nan | -1.82 | -1.89 |
| MNQ | 15 | h2 | bottom fifth | long | 34301 | +0.010 | 0.041 | +0.53 | -1.47 | +nan | -1.47 | -1.62 |
| MNQ | 15 | h4 | bottom fifth | long | 34301 | +0.013 | 0.041 | +1.01 | -0.99 | +nan | -0.99 | -1.23 |
| MNQ | 15 | h8 | bottom fifth | long | 34301 | +0.017 | 0.041 | +1.30 | -0.70 | +nan | -0.70 | -1.34 |
| MNQ | 15 | h16 | top fifth | long | 34299 | +0.052 | 0.048 | +2.12 | +0.12 | +nan | +0.12 | -0.35 |
| MNQ | 15 | eod | top fifth | long | 34299 | +0.297 | 0.048 | +7.88 | +5.88 | +nan | +5.88 | +3.51 |
| MYM | 15 | h1 | top fifth | short | 34280 | +0.004 | 0.106 | +0.09 | -1.91 | +nan | -1.91 | -1.94 |
| MYM | 15 | h2 | top fifth | short | 34280 | +0.009 | 0.106 | +0.13 | -1.87 | +nan | -1.87 | -1.96 |
| MYM | 15 | h4 | bottom fifth | long | 34282 | -0.002 | 0.091 | +0.21 | -1.79 | +nan | -1.79 | -1.62 |
| MYM | 15 | h8 | bottom fifth | long | 34282 | -0.006 | 0.091 | +0.11 | -1.89 | +nan | -1.89 | -1.58 |
| MYM | 15 | h16 | top fifth | long | 34280 | -0.001 | 0.106 | +0.32 | -1.68 | +nan | -1.68 | -1.10 |
| MYM | 15 | eod | top fifth | long | 34280 | +0.227 | 0.106 | +3.66 | +1.66 | +nan | +1.66 | +2.10 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.520 | +0.520 | +0.347 | +0.179 | +0.056 | +0.000 | -0.003 | -0.006 | -0.015 | +0.015 | +0.034 |
| MNQ | 15 | +0.475 | +0.490 | +0.343 | +0.182 | +0.053 | +0.000 | +0.003 | +0.002 | -0.011 | +0.022 | +0.073 |
| MYM | 15 | +0.410 | +0.425 | +0.277 | +0.141 | +0.041 | +0.000 | +0.010 | +0.012 | +0.005 | +0.027 | +0.110 |

## Calibration

- MES 15-min: 171502 bars, 34301 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171495 bars, 34299 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171402 bars, 34280 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
