# Impact card: big_bar_follow

bar range > 2x its 20-bar average; side = bar colour

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 60-min: no measurable direction effect (best +0.031 R20 over the next 2 bars (2 h), p=0.47; we would catch an effect of 0.058 R20 or more 80% of the time).
- MES 60-min size: the market moves 23% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.120 R20, CONFIRMED, q=1.34e-29, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.49 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.068 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.042 R20 over the next 1 bar (1 h), p=0.17; we would catch an effect of 0.079 R20 or more 80% of the time).
- MYM 60-min size: the market moves 25% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.132 R20, CONFIRMED, q=4.12e-15, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.62 at recent bar sizes, 90% range up to $3.76); about 10.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | +0.023 | -0.000 .. +0.046 | +0.0099 | 0.055 / 0.073 / 0.053 | 0.0537 |  |  | 11/16 | +0.011 | +0.034 |  | +1.7 / +1.9 |  |
| MES | 60 | h2 * | +0.031 | +0.001 .. +0.062 | +0.0096 | 0.046 / 0.065 / 0.044 | 0.0471 | 1 | 0.235 | 11/16 | +0.025 | +0.038 | False | +1.8 / +2.0 |  |
| MES | 60 | h4 | +0.023 | -0.019 .. +0.065 | +0.0050 | 0.28 / 0.31 / 0.27 | 0.269 |  |  | 10/16 | +0.002 | +0.044 |  | +1.0 / +1.1 | 0.058 |
| MES | 60 | h8 | +0.022 | -0.031 .. +0.074 | +0.0034 | 0.42 / 0.44 / 0.39 | 0.395 |  |  | 10/16 | +0.026 | +0.017 |  | +0.8 / +0.8 |  |
| MES | 60 | h16 | +0.001 | -0.054 .. +0.056 | +0.0002 | 0.97 / 0.97 / 0.96 | 0.964 |  |  | 7/16 | +0.013 | -0.010 |  | +0.0 / +0.0 |  |
| MES | 60 | eod | +0.013 | -0.044 .. +0.071 | +0.0016 | 0.64 / 0.66 / 0.62 | 0.61 |  |  | 10/16 | +0.024 | +0.003 |  | +0.5 / +0.5 |  |
| MYM | 60 | h1 * | +0.042 | +0.005 .. +0.078 | +0.0182 | 0.026 / 0.029 / 0.015 | 0.0137 | 0.75 | 0.143 | 7/8 | n/a | +0.042 | False | +2.2 / +2.2 |  |
| MYM | 60 | h2 | +0.027 | -0.020 .. +0.073 | +0.0082 | 0.27 / 0.28 / 0.25 | 0.251 |  |  | 5/8 | n/a | +0.027 |  | +1.1 / +1.1 |  |
| MYM | 60 | h4 | +0.021 | -0.038 .. +0.080 | +0.0047 | 0.48 / 0.5 / 0.49 | 0.484 |  |  | 5/8 | n/a | +0.021 |  | +0.7 / +0.7 | 0.079 |
| MYM | 60 | h8 | +0.031 | -0.046 .. +0.108 | +0.0051 | 0.43 / 0.44 / 0.4 | 0.414 |  |  | 6/8 | n/a | +0.031 |  | +0.8 / +0.8 |  |
| MYM | 60 | h16 | +0.015 | -0.066 .. +0.096 | +0.0019 | 0.72 / 0.73 / 0.7 | 0.708 |  |  | 5/8 | n/a | +0.015 |  | +0.4 / +0.4 |  |
| MYM | 60 | eod | +0.018 | -0.066 .. +0.102 | +0.0022 | 0.67 / 0.68 / 0.64 | 0.646 |  |  | 5/8 | n/a | +0.018 |  | +0.4 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 * | +0.120 | +0.100 .. +0.140 | +23.4% | +0.268 | 1e-31 | 1.34e-29 | 14/16 |
| MES | 60 | h2 | +0.145 | +0.117 .. +0.173 | +19.6% | +0.319 | 2.3e-24 |  | 16/16 |
| MES | 60 | h4 | +0.160 | +0.121 .. +0.199 | +15.1% | +0.348 | 5.4e-15 |  | 14/16 |
| MES | 60 | h8 | +0.145 | +0.101 .. +0.189 | +9.6% | +0.345 | 1.5e-09 |  | 13/16 |
| MES | 60 | h16 | +0.126 | +0.081 .. +0.172 | +6.1% | +0.324 | 2.5e-07 |  | 15/16 |
| MES | 60 | eod | +0.125 | +0.077 .. +0.172 | +5.8% | +0.317 | 7.8e-07 |  | 15/16 |
| MYM | 60 | h1 * | +0.132 | +0.101 .. +0.163 | +25.2% | +0.268 | 9.5e-17 | 4.12e-15 | 8/8 |
| MYM | 60 | h2 | +0.151 | +0.108 .. +0.194 | +20.0% | +0.307 | 6.8e-12 |  | 7/8 |
| MYM | 60 | h4 | +0.143 | +0.092 .. +0.195 | +13.3% | +0.325 | 6.9e-08 |  | 6/8 |
| MYM | 60 | h8 | +0.152 | +0.088 .. +0.217 | +9.8% | +0.333 | 1.1e-05 |  | 8/8 |
| MYM | 60 | h16 | +0.138 | +0.067 .. +0.208 | +6.5% | +0.290 | 0.00017 |  | 8/8 |
| MYM | 60 | eod | +0.138 | +0.065 .. +0.212 | +6.2% | +0.288 | 0.00029 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 60 | +1.51 pts | +0.59 .. +2.44 | 0.0017 |
| MYM | 60 | +1.59 pts | +0.34 .. +2.84 | 0.018 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | event | with signal | 8409 | +0.021 | 0.099 | +0.52 | -2.98 | -3.09 | -2.88 | -2.95 |
| MES | 60 | h2 | event | with signal | 8409 | +0.026 | 0.099 | +0.63 | -2.87 | -2.78 | -2.94 | -2.70 |
| MES | 60 | h4 | event | with signal | 8409 | +0.013 | 0.099 | -0.02 | -3.52 | -3.48 | -3.55 | -3.23 |
| MES | 60 | h8 | event | with signal | 8409 | +0.007 | 0.099 | +0.16 | -3.34 | -3.08 | -3.60 | -2.92 |
| MES | 60 | h16 | event | with signal | 8409 | -0.004 | 0.099 | -0.50 | -4.00 | -3.26 | -4.70 | -3.90 |
| MES | 60 | eod | event | with signal | 8409 | +0.003 | 0.099 | -0.06 | -3.56 | -3.08 | -4.02 | -3.27 |
| MYM | 60 | h1 | event | with signal | 4610 | +0.042 | 0.052 | +0.91 | -1.09 | +nan | -1.09 | -1.10 |
| MYM | 60 | h2 | event | with signal | 4610 | +0.022 | 0.052 | +0.24 | -1.76 | +nan | -1.76 | -1.56 |
| MYM | 60 | h4 | event | with signal | 4610 | +0.016 | 0.052 | -0.34 | -2.34 | +nan | -2.34 | -2.06 |
| MYM | 60 | h8 | event | with signal | 4610 | +0.024 | 0.052 | +0.14 | -1.86 | +nan | -1.86 | -1.49 |
| MYM | 60 | h16 | event | with signal | 4610 | +0.027 | 0.052 | +0.13 | -1.87 | +nan | -1.87 | -2.12 |
| MYM | 60 | eod | event | with signal | 4610 | +0.029 | 0.052 | +0.31 | -1.69 | +nan | -1.69 | -1.83 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | -1.312 | -1.385 | -1.465 | -1.499 | -1.476 | +0.000 | +0.024 | +0.029 | +0.005 | -0.058 | -0.146 |
| MYM | 60 | -1.277 | -1.380 | -1.471 | -1.521 | -1.512 | +0.000 | +0.044 | +0.030 | +0.008 | +0.077 | +0.248 |

## Calibration

- MES 60-min: 83351 bars, 8409 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41624 bars, 4610 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
