# Impact card: honest_inside

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.040 R20 over the next 1 bar (15 min), p=0.11; we would catch an effect of 0.076 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.56).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.89 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.590 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.040 | -0.073 .. -0.007 | -0.0138 | 0.018 / 0.0086 / 0.012 | 0.0138 | 0.295 | 0.095 | 2/2 | -0.010 | -0.096 | False | -2.6 / -2.4 |  |
| MES | 15 | h2 | -0.033 | -0.075 .. +0.009 | -0.0080 | 0.12 / 0.11 / 0.13 | 0.116 |  |  | 2/2 | -0.007 | -0.080 |  | -1.5 / -1.5 |  |
| MES | 15 | h4 | -0.054 | -0.114 .. +0.007 | -0.0092 | 0.081 / 0.086 / 0.081 | 0.0801 |  |  | 2/2 | -0.033 | -0.091 |  | -1.7 / -1.7 | 0.076 |
| MES | 15 | h8 | -0.068 | -0.154 .. +0.018 | -0.0083 | 0.12 / 0.15 / 0.11 | 0.122 |  |  | 2/2 | -0.057 | -0.088 |  | -1.5 / -1.5 |  |
| MES | 15 | h16 | -0.117 | -0.229 .. -0.006 | -0.0103 | 0.039 / 0.05 / 0.054 | 0.0359 |  |  | 2/2 | -0.126 | -0.101 |  | -1.9 / -2.1 |  |
| MES | 15 | eod | +0.010 | -0.154 .. +0.174 | +0.0005 | 0.91 / 0.92 / 0.93 | 0.925 |  |  | 1/2 | +0.023 | -0.015 |  | +0.1 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.004 | -0.023 .. +0.015 | -0.6% | -0.006 | 0.68 |  | 1/2 |
| MES | 15 | h2 | -0.014 | -0.039 .. +0.011 | -1.4% | -0.013 | 0.34 |  | 2/2 |
| MES | 15 | h4 | +0.014 | -0.019 .. +0.047 | +1.0% | +0.008 | 0.53 |  | 1/2 |
| MES | 15 | h8 | +0.032 | -0.021 .. +0.085 | +1.7% | +0.018 | 0.31 |  | 2/2 |
| MES | 15 | h16 * | +0.063 | -0.002 .. +0.127 | +2.4% | +0.037 | 0.093 | 1 | 2/2 |
| MES | 15 | eod | +0.011 | -0.111 .. +0.133 | +0.2% | +0.001 | 0.97 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -1.38 pts | -3.07 .. +0.32 | 0.14 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | against signal | 3021 | +0.037 | 0.593 | +0.22 | -3.28 | -3.47 | -2.91 | -3.26 |
| MES | 15 | h2 | event | against signal | 3021 | +0.028 | 0.593 | +0.18 | -3.32 | -3.49 | -2.99 | -3.29 |
| MES | 15 | h4 | event | against signal | 3021 | +0.045 | 0.593 | +0.29 | -3.21 | -3.38 | -2.88 | -3.16 |
| MES | 15 | h8 | event | against signal | 3021 | +0.060 | 0.593 | +0.40 | -3.10 | -3.20 | -2.91 | -3.06 |
| MES | 15 | h16 | event | against signal | 3021 | +0.104 | 0.593 | +0.66 | -2.84 | -2.85 | -2.83 | -2.76 |
| MES | 15 | eod | event | with signal | 3021 | +0.019 | 0.593 | +0.08 | -3.42 | -3.26 | -3.71 | -3.48 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.005 | -0.130 | -0.076 | -0.115 | -0.318 | +0.000 | -0.037 | -0.028 | -0.034 | -0.053 | -0.120 |

## Calibration

- MES 15-min: 35981 bars, 3021 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36400 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
