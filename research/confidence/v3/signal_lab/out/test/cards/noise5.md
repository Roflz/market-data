# Impact card: noise5

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.049 R20 over the next 2 bars (30 min), p=0.13; we would catch an effect of 0.076 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.11).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.586 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.024 | -0.003 .. +0.050 | +0.0079 | 0.079 / 0.074 / 0.084 | 0.0912 |  |  | 2/2 | +0.024 | +0.023 |  | +1.7 / +1.8 |  |
| MES | 15 | h2 * | +0.049 | +0.007 .. +0.091 | +0.0158 | 0.022 / 0.014 / 0.016 | 0.0249 | 1 | 0.495 | 2/2 | +0.065 | +0.018 | False | +2.4 / +2.3 |  |
| MES | 15 | h4 | +0.049 | -0.004 .. +0.103 | +0.0119 | 0.068 / 0.092 / 0.08 | 0.0912 |  |  | 1/2 | +0.080 | -0.007 |  | +1.7 / +1.8 | 0.076 |
| MES | 15 | h8 | +0.054 | -0.031 .. +0.138 | +0.0087 | 0.21 / 0.19 / 0.19 | 0.221 |  |  | 1/2 | +0.111 | -0.053 |  | +1.3 / +1.2 |  |
| MES | 15 | h16 | +0.040 | -0.089 .. +0.169 | +0.0024 | 0.54 / 0.51 / 0.47 | 0.472 |  |  | 1/2 | +0.117 | -0.103 |  | +0.7 / +0.6 |  |
| MES | 15 | eod | +0.109 | -0.133 .. +0.350 | +0.0020 | 0.38 / 0.31 / 0.27 | 0.262 |  |  | 2/2 | +0.101 | +0.124 |  | +1.1 / +0.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.007 | -0.010 .. +0.024 | +1.0% | +0.007 | 0.57 |  | 2/2 |
| MES | 15 | h2 | -0.001 | -0.028 .. +0.027 | -0.1% | +0.003 | 0.96 |  | 1/2 |
| MES | 15 | h4 * | +0.047 | +0.009 .. +0.085 | +3.5% | +0.028 | 0.018 | 1 | 2/2 |
| MES | 15 | h8 | +0.010 | -0.027 .. +0.047 | +0.5% | +0.031 | 0.8 |  | 2/2 |
| MES | 15 | h16 | +0.002 | -0.062 .. +0.065 | +0.1% | +0.008 | 0.99 |  | 1/2 |
| MES | 15 | eod | +0.048 | -0.055 .. +0.151 | +1.1% | +0.003 | 0.6 |  | 2/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +1.35 pts | -0.51 .. +3.21 | 0.15 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | short | 7197 | +0.019 | 0.589 | +0.11 | -3.39 | -3.44 | -3.31 | -3.41 |
| MES | 15 | h2 | bottom fifth | short | 7197 | +0.042 | 0.589 | +0.24 | -3.26 | -3.30 | -3.17 | -3.29 |
| MES | 15 | h4 | bottom fifth | short | 7197 | +0.059 | 0.589 | +0.34 | -3.16 | -3.21 | -3.05 | -3.22 |
| MES | 15 | h8 | bottom fifth | short | 7197 | +0.088 | 0.589 | +0.50 | -3.00 | -3.03 | -2.94 | -3.13 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.101 | 0.589 | +0.56 | -2.94 | -3.09 | -2.64 | -3.25 |
| MES | 15 | eod | bottom fifth | short | 7197 | +0.383 | 0.589 | +2.25 | -1.25 | -2.27 | +0.70 | -2.94 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.078 | +0.089 | +0.056 | +0.034 | +0.006 | +0.000 | +0.023 | +0.050 | +0.046 | +0.059 | +0.039 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
