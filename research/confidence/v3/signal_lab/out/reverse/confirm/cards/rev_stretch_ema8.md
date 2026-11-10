# Impact card: rev_stretch_ema8

distance of close from EMA8 in average bars; far above -> next hour down

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.068 R20 or more 80% of the time).
- MES 15-min size: the market moves 12% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.064 R20, CONFIRMED, q=3.03e-17, 7 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.24 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.127 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +0.014 R20 over the next 1 bar (15 min), p=0.24; we would catch an effect of 0.097 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.059 R20, CONFIRMED, q=1.06e-14, 7 of 8 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.31 at recent bar sizes, 90% range up to $1.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best -0.038 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MYM 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.055 R20, CONFIRMED, q=8.06e-16, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.11 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.096 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.003 | -0.011 .. +0.016 | +0.0015 | 0.68 / 0.68 / 0.68 | 0.685 |  |  | 5/8 | n/a | +0.003 |  | +0.4 / +0.4 |  |
| MES | 15 | h2 * | +0.008 | -0.015 .. +0.030 | +0.0038 | 0.51 / 0.52 / 0.54 | 0.527 | 1 | 1 | 5/8 | n/a | +0.008 | False | +0.7 / +0.7 |  |
| MES | 15 | h4 | +0.004 | -0.035 .. +0.042 | +0.0047 | 0.86 / 0.86 / 0.87 | 0.865 |  |  | 4/8 | n/a | +0.004 |  | +0.3 / +0.2 | 0.068 |
| MES | 15 | h8 | -0.006 | -0.074 .. +0.062 | +0.0011 | 0.86 / 0.86 / 0.86 | 0.866 |  |  | 4/8 | n/a | -0.006 |  | -0.3 / -0.2 |  |
| MES | 15 | h16 | -0.007 | -0.108 .. +0.094 | +0.0036 | 0.89 / 0.9 / 0.91 | 0.906 |  |  | 4/8 | n/a | -0.007 |  | -0.2 / -0.1 |  |
| MES | 15 | eod | -0.038 | -0.313 .. +0.237 | +0.0037 | 0.79 / 0.8 / 0.82 | 0.817 |  |  | 4/8 | n/a | -0.038 |  | -0.6 / -0.3 |  |
| MNQ | 15 | h1 * | +0.014 | +0.002 .. +0.026 | +0.0085 | 0.026 / 0.032 / 0.047 | 0.0358 | 1 | 0.415 | 6/8 | n/a | +0.014 | False | +2.0 / +2.2 |  |
| MNQ | 15 | h2 | +0.024 | +0.004 .. +0.044 | +0.0087 | 0.02 / 0.027 / 0.058 | 0.0527 |  |  | 7/8 | n/a | +0.024 |  | +2.5 / +2.3 |  |
| MNQ | 15 | h4 | +0.028 | -0.010 .. +0.066 | +0.0057 | 0.15 / 0.16 / 0.19 | 0.188 |  |  | 5/8 | n/a | +0.028 |  | +2.0 / +1.4 | 0.097 |
| MNQ | 15 | h8 | +0.018 | -0.052 .. +0.087 | +0.0011 | 0.62 / 0.62 / 0.61 | 0.6 |  |  | 4/8 | n/a | +0.018 |  | +0.9 / +0.5 |  |
| MNQ | 15 | h16 | +0.001 | -0.101 .. +0.104 | +0.0012 | 0.98 / 0.98 / 0.98 | 0.986 |  |  | 5/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MNQ | 15 | eod | +0.147 | -0.138 .. +0.431 | +0.0075 | 0.31 / 0.34 / 0.35 | 0.362 |  |  | 5/8 | n/a | +0.147 |  | +2.1 / +1.0 |  |
| MYM | 15 | h1 | -0.001 | -0.014 .. +0.012 | -0.0013 | 0.86 / 0.86 / 0.86 | 0.869 |  |  | 3/8 | n/a | -0.001 |  | -0.2 / -0.2 |  |
| MYM | 15 | h2 | +0.002 | -0.021 .. +0.025 | +0.0001 | 0.85 / 0.85 / 0.86 | 0.875 |  |  | 4/8 | n/a | +0.002 |  | +0.2 / +0.2 |  |
| MYM | 15 | h4 | +0.002 | -0.036 .. +0.040 | +0.0004 | 0.91 / 0.91 / 0.91 | 0.899 |  |  | 3/8 | n/a | +0.002 |  | +0.2 / +0.1 | 0.078 |
| MYM | 15 | h8 | -0.024 | -0.091 .. +0.042 | -0.0030 | 0.47 / 0.51 / 0.46 | 0.481 |  |  | 5/8 | n/a | -0.024 |  | -1.2 / -0.7 |  |
| MYM | 15 | h16 * | -0.038 | -0.142 .. +0.065 | -0.0018 | 0.47 / 0.5 / 0.51 | 0.521 | 1 | 1 | 6/8 | n/a | -0.038 | False | -1.3 / -0.7 |  |
| MYM | 15 | eod | +0.067 | -0.247 .. +0.380 | +0.0026 | 0.68 / 0.69 / 0.69 | 0.711 |  |  | 4/8 | n/a | +0.067 |  | +0.9 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.064 | -0.078 .. -0.050 | -12.4% | -0.126 | 1.1e-19 | 3.03e-17 | 7/8 |
| MES | 15 | h2 | -0.080 | -0.101 .. -0.059 | -10.7% | -0.157 | 2.2e-13 |  | 7/8 |
| MES | 15 | h4 | -0.081 | -0.112 .. -0.050 | -7.5% | -0.173 | 2.7e-07 |  | 7/8 |
| MES | 15 | h8 | -0.092 | -0.140 .. -0.044 | -5.8% | -0.181 | 0.00021 |  | 7/8 |
| MES | 15 | h16 | -0.089 | -0.172 .. -0.006 | -3.8% | -0.159 | 0.035 |  | 7/8 |
| MES | 15 | eod | -0.078 | -0.258 .. +0.102 | -1.3% | -0.162 | 0.46 |  | 5/8 |
| MNQ | 15 | h1 * | -0.059 | -0.073 .. -0.045 | -11.3% | -0.111 | 7e-17 | 1.06e-14 | 7/8 |
| MNQ | 15 | h2 | -0.071 | -0.092 .. -0.050 | -9.4% | -0.141 | 8.3e-11 |  | 7/8 |
| MNQ | 15 | h4 | -0.064 | -0.097 .. -0.032 | -5.8% | -0.155 | 0.00012 |  | 6/8 |
| MNQ | 15 | h8 | -0.061 | -0.111 .. -0.011 | -3.8% | -0.153 | 0.017 |  | 7/8 |
| MNQ | 15 | h16 | -0.068 | -0.153 .. +0.018 | -2.8% | -0.129 | 0.12 |  | 5/8 |
| MNQ | 15 | eod | -0.116 | -0.304 .. +0.072 | -1.9% | -0.126 | 0.28 |  | 5/8 |
| MYM | 15 | h1 * | -0.055 | -0.068 .. -0.043 | -10.5% | -0.107 | 4.3e-18 | 8.06e-16 | 8/8 |
| MYM | 15 | h2 | -0.071 | -0.090 .. -0.052 | -9.3% | -0.136 | 2.9e-13 |  | 7/8 |
| MYM | 15 | h4 | -0.083 | -0.112 .. -0.053 | -7.5% | -0.158 | 6.6e-08 |  | 7/8 |
| MYM | 15 | h8 | -0.093 | -0.143 .. -0.042 | -5.7% | -0.171 | 0.0003 |  | 7/8 |
| MYM | 15 | h16 | -0.125 | -0.209 .. -0.042 | -5.2% | -0.196 | 0.0032 |  | 7/8 |
| MYM | 15 | eod | -0.173 | -0.408 .. +0.063 | -2.9% | -0.303 | 0.16 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +0.32 pts | -0.57 .. +1.20 | 0.6 |
| MNQ | 15 | +1.36 pts | +0.48 .. +2.23 | 0.019 |
| MYM | 15 | -0.02 pts | -0.90 .. +0.86 | 0.99 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top fifth | long | 34301 | -0.000 | 0.132 | +0.01 | -3.49 | +nan | -3.49 | -3.47 |
| MES | 15 | h2 | top fifth | long | 34301 | +0.006 | 0.132 | +0.16 | -3.34 | +nan | -3.34 | -3.46 |
| MES | 15 | h4 | top fifth | long | 34301 | +0.008 | 0.132 | +0.20 | -3.30 | +nan | -3.30 | -3.66 |
| MES | 15 | h8 | bottom fifth | long | 34301 | -0.004 | 0.122 | +0.32 | -3.18 | +nan | -3.18 | -3.11 |
| MES | 15 | h16 | bottom fifth | long | 34301 | -0.011 | 0.122 | +1.08 | -2.42 | +nan | -2.42 | -1.57 |
| MES | 15 | eod | bottom fifth | long | 34301 | +0.002 | 0.122 | +2.44 | -1.06 | +nan | -1.06 | +2.04 |
| MNQ | 15 | h1 | top fifth | long | 34299 | +0.012 | 0.046 | +0.28 | -1.72 | +nan | -1.72 | -1.88 |
| MNQ | 15 | h2 | top fifth | long | 34299 | +0.026 | 0.046 | +0.73 | -1.27 | +nan | -1.27 | -1.64 |
| MNQ | 15 | h4 | top fifth | long | 34299 | +0.034 | 0.046 | +1.04 | -0.96 | +nan | -0.96 | -1.82 |
| MNQ | 15 | h8 | top fifth | long | 34299 | +0.060 | 0.046 | +1.78 | -0.22 | +nan | -0.22 | -2.30 |
| MNQ | 15 | h16 | top fifth | long | 34299 | +0.093 | 0.046 | +2.69 | +0.69 | +nan | +0.69 | -2.49 |
| MNQ | 15 | eod | top fifth | long | 34299 | +0.318 | 0.046 | +8.87 | +6.87 | +nan | +6.87 | +1.04 |
| MYM | 15 | h1 | top fifth | short | 34281 | +0.004 | 0.098 | +0.10 | -1.90 | +nan | -1.90 | -1.93 |
| MYM | 15 | h2 | bottom fifth | short | 34281 | +0.007 | 0.094 | +0.00 | -2.00 | +nan | -2.00 | -2.02 |
| MYM | 15 | h4 | bottom fifth | short | 34281 | +0.013 | 0.094 | +0.06 | -1.94 | +nan | -1.94 | -2.01 |
| MYM | 15 | h8 | bottom fifth | long | 34281 | +0.002 | 0.094 | +0.44 | -1.56 | +nan | -1.56 | -1.32 |
| MYM | 15 | h16 | bottom fifth | long | 34281 | +0.006 | 0.094 | +1.15 | -0.85 | +nan | -0.85 | +0.00 |
| MYM | 15 | eod | top fifth | long | 34281 | +0.149 | 0.098 | +3.44 | +1.44 | +nan | +1.44 | +1.33 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -3.100 | -3.432 | -2.889 | -1.935 | -1.134 | +0.000 | -0.011 | -0.007 | -0.011 | -0.023 | -0.037 |
| MNQ | 15 | -3.175 | -3.496 | -2.920 | -1.945 | -1.132 | +0.000 | +0.007 | +0.022 | +0.029 | +0.025 | -0.007 |
| MYM | 15 | -3.158 | -3.514 | -2.955 | -1.990 | -1.166 | +0.000 | -0.010 | -0.005 | +0.002 | -0.025 | -0.045 |

## Calibration

- MES 15-min: 171502 bars, 34301 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171495 bars, 34299 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171402 bars, 34281 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
