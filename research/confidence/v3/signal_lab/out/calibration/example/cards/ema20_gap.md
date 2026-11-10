# Impact card: ema20_gap

(close - EMA20) / ATR14

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 60-min: no measurable direction effect (best +0.018 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.083 R20 or more 80% of the time).
- MES 60-min size: the market moves 13% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.068 R20, CONFIRMED, q=7.17e-16, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.62 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.016 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.122 R20 or more 80% of the time).
- MYM 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.051 R20, CONFIRMED, q=0.000912, 6 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.34 at recent bar sizes, 90% range up to $4.17); about 36.7x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | +0.006 | -0.011 .. +0.022 | +0.0074 | 0.5 / 0.49 / 0.53 | 0.522 |  |  | 7/16 | -0.015 | +0.026 |  | +0.7 / +0.7 |  |
| MES | 60 | h2 | +0.009 | -0.020 .. +0.038 | +0.0060 | 0.55 / 0.55 / 0.59 | 0.593 |  |  | 6/16 | -0.025 | +0.042 |  | +0.7 / +0.6 |  |
| MES | 60 | h4 * | +0.018 | -0.035 .. +0.072 | +0.0067 | 0.5 / 0.5 / 0.55 | 0.552 | 1 | 0.909 | 8/16 | -0.040 | +0.077 | False | +1.1 / +0.7 | 0.083 |
| MES | 60 | h8 | +0.013 | -0.082 .. +0.109 | +0.0022 | 0.79 / 0.79 / 0.8 | 0.8 |  |  | 8/16 | -0.072 | +0.099 |  | +0.6 / +0.3 |  |
| MES | 60 | h16 | -0.028 | -0.186 .. +0.129 | -0.0046 | 0.72 / 0.72 / 0.75 | 0.756 |  |  | 8/16 | -0.154 | +0.097 |  | -0.9 / -0.4 |  |
| MES | 60 | eod | -0.052 | -0.224 .. +0.120 | -0.0062 | 0.56 / 0.56 / 0.6 | 0.61 |  |  | 10/16 | -0.154 | +0.050 |  | -1.6 / -0.6 |  |
| MYM | 60 | h1 * | +0.016 | -0.007 .. +0.039 | +0.0069 | 0.18 / 0.2 / 0.23 | 0.24 | 1 | 0.608 | 5/8 | n/a | +0.016 | False | +1.2 / +1.4 |  |
| MYM | 60 | h2 | +0.019 | -0.025 .. +0.063 | +0.0051 | 0.4 / 0.41 / 0.44 | 0.457 |  |  | 6/8 | n/a | +0.019 |  | +1.0 / +0.8 |  |
| MYM | 60 | h4 | +0.035 | -0.045 .. +0.116 | +0.0078 | 0.39 / 0.4 / 0.42 | 0.419 |  |  | 6/8 | n/a | +0.035 |  | +1.4 / +0.9 | 0.122 |
| MYM | 60 | h8 | +0.073 | -0.073 .. +0.219 | +0.0112 | 0.32 / 0.31 / 0.32 | 0.332 |  |  | 5/8 | n/a | +0.073 |  | +2.1 / +1.0 |  |
| MYM | 60 | h16 | +0.077 | -0.165 .. +0.320 | +0.0099 | 0.53 / 0.52 / 0.54 | 0.526 |  |  | 5/8 | n/a | +0.077 |  | +1.7 / +0.6 |  |
| MYM | 60 | eod | +0.072 | -0.197 .. +0.340 | +0.0095 | 0.6 / 0.59 / 0.6 | 0.595 |  |  | 3/8 | n/a | +0.072 |  | +1.5 / +0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 * | -0.068 | -0.084 .. -0.053 | -13.3% | -0.141 | 1.1e-17 | 7.17e-16 | 14/16 |
| MES | 60 | h2 | -0.081 | -0.105 .. -0.058 | -11.0% | -0.182 | 1.2e-11 |  | 13/16 |
| MES | 60 | h4 | -0.109 | -0.145 .. -0.073 | -10.3% | -0.225 | 3.3e-09 |  | 13/16 |
| MES | 60 | h8 | -0.141 | -0.200 .. -0.082 | -9.3% | -0.280 | 2.6e-06 |  | 14/16 |
| MES | 60 | h16 | -0.153 | -0.252 .. -0.054 | -7.4% | -0.322 | 0.0024 |  | 13/16 |
| MES | 60 | eod | -0.149 | -0.266 .. -0.032 | -6.9% | -0.328 | 0.013 |  | 13/16 |
| MYM | 60 | h1 * | -0.051 | -0.075 .. -0.027 | -9.8% | -0.119 | 2.8e-05 | 0.000912 | 6/8 |
| MYM | 60 | h2 | -0.062 | -0.100 .. -0.025 | -8.2% | -0.148 | 0.0011 |  | 7/8 |
| MYM | 60 | h4 | -0.098 | -0.157 .. -0.040 | -9.1% | -0.190 | 0.00097 |  | 7/8 |
| MYM | 60 | h8 | -0.101 | -0.198 .. -0.004 | -6.5% | -0.216 | 0.041 |  | 6/8 |
| MYM | 60 | h16 | -0.104 | -0.263 .. +0.055 | -4.9% | -0.244 | 0.2 |  | 4/8 |
| MYM | 60 | eod | -0.104 | -0.285 .. +0.078 | -4.7% | -0.256 | 0.28 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 60 | +0.87 pts | -0.98 .. +2.72 | 0.44 |
| MYM | 60 | +1.52 pts | -0.98 .. +4.02 | 0.36 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | top fifth | long | 16670 | +0.013 | 0.101 | +0.42 | -3.08 | -3.29 | -2.89 | -3.27 |
| MES | 60 | h2 | top fifth | long | 16670 | +0.023 | 0.101 | +0.69 | -2.81 | -3.05 | -2.59 | -3.22 |
| MES | 60 | h4 | top fifth | long | 16670 | +0.042 | 0.101 | +1.27 | -2.23 | -2.72 | -1.78 | -3.02 |
| MES | 60 | h8 | top fifth | long | 16670 | +0.064 | 0.101 | +2.18 | -1.32 | -1.86 | -0.83 | -2.83 |
| MES | 60 | h16 | bottom fifth | long | 16671 | +0.075 | 0.082 | +2.18 | -1.32 | -0.33 | -2.26 | -3.72 |
| MES | 60 | eod | bottom fifth | long | 16671 | +0.105 | 0.082 | +4.03 | +0.53 | +0.08 | +0.96 | -2.75 |
| MYM | 60 | h1 | top fifth | long | 8325 | +0.014 | 0.051 | +0.27 | -1.73 | +nan | -1.73 | -1.95 |
| MYM | 60 | h2 | top fifth | long | 8325 | +0.025 | 0.051 | +0.54 | -1.46 | +nan | -1.46 | -1.88 |
| MYM | 60 | h4 | top fifth | long | 8325 | +0.048 | 0.051 | +1.03 | -0.97 | +nan | -0.97 | -1.89 |
| MYM | 60 | h8 | top fifth | long | 8325 | +0.107 | 0.051 | +2.82 | +0.82 | +nan | +0.82 | -0.75 |
| MYM | 60 | h16 | top fifth | long | 8325 | +0.138 | 0.051 | +3.64 | +1.64 | +nan | +1.64 | -1.32 |
| MYM | 60 | eod | top fifth | long | 8325 | +0.154 | 0.051 | +3.95 | +1.95 | +nan | +1.95 | -1.56 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | -4.079 | -3.284 | -2.252 | -1.371 | -0.770 | +0.000 | +0.003 | +0.003 | -0.002 | -0.028 | -0.102 |
| MYM | 60 | -4.180 | -3.387 | -2.329 | -1.423 | -0.800 | +0.000 | +0.017 | +0.015 | +0.031 | +0.069 | +0.031 |

## Calibration

- MES 60-min: 83351 bars, 16670 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41624 bars, 8325 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
