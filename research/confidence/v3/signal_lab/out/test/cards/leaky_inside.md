# Impact card: leaky_inside

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: INVALID - the metric FAILED the look-ahead test (its value at 2017-04-24 14:30:00 changes when the bars after it are removed), so it uses information from after the bar's close. Every number on this card measures that peek, not the metric. Fix the metric and re-run.
- MES 15-min BOTTOM LINE (direction): INVALID (LOOK-AHEAD) - see above. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.841 | +0.807 .. +0.875 | +0.2417 | 0 / 0 / 0 | 0.00276 | 0 | 0 | 2/2 | +0.848 | +0.829 | True | +40.3 / +48.4 |  |
| MES | 15 | h2 | +0.835 | +0.787 .. +0.884 | +0.1693 | 1.1e-251 / 1e-277 / 7.9e-223 | 0.00276 |  |  | 2/2 | +0.832 | +0.842 |  | +30.2 / +33.9 |  |
| MES | 15 | h4 | +0.844 | +0.775 .. +0.913 | +0.1208 | 9.8e-127 / 2e-128 / 1.9e-117 | 0.00276 |  |  | 2/2 | +0.826 | +0.878 |  | +21.8 / +23.9 | 0.103 |
| MES | 15 | h8 | +0.863 | +0.765 .. +0.961 | +0.0877 | 2.5e-67 / 2.3e-62 / 1.8e-62 | 0.00276 |  |  | 2/2 | +0.872 | +0.846 |  | +16.0 / +17.3 |  |
| MES | 15 | h16 | +0.839 | +0.696 .. +0.982 | +0.0612 | 1.5e-30 / 1.7e-30 / 5.8e-32 | 0.00276 |  |  | 2/2 | +0.837 | +0.841 |  | +11.2 / +11.5 |  |
| MES | 15 | eod | +0.911 | +0.687 .. +1.136 | +0.0374 | 1.7e-15 / 6.8e-14 / 2.8e-13 | 0.00276 |  |  | 2/2 | +0.860 | +1.007 |  | +7.0 / +8.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.170 | +0.147 .. +0.193 | +25.1% | +0.106 | 2.5e-47 | 6.13e-46 | 2/2 |
| MES | 15 | h2 | +0.084 | +0.054 .. +0.114 | +8.7% | +0.081 | 1.5e-06 |  | 2/2 |
| MES | 15 | h4 | +0.086 | +0.042 .. +0.129 | +6.3% | +0.082 | 0.0002 |  | 2/2 |
| MES | 15 | h8 | +0.091 | +0.029 .. +0.153 | +4.8% | +0.072 | 0.0039 |  | 2/2 |
| MES | 15 | h16 | +0.100 | +0.022 .. +0.178 | +3.8% | +0.071 | 0.013 |  | 2/2 |
| MES | 15 | eod | +0.024 | -0.116 .. +0.163 | +0.5% | -0.010 | 0.98 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +32.84 pts | +31.02 .. +34.66 | 4.6e-191 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | with signal | 2150 | +0.844 | 0.594 | +4.93 | +1.43 | +1.39 | +1.50 | +1.41 |
| MES | 15 | h2 | event | with signal | 2150 | +0.840 | 0.594 | +4.89 | +1.39 | +1.30 | +1.55 | +1.36 |
| MES | 15 | h4 | event | with signal | 2150 | +0.852 | 0.594 | +4.94 | +1.44 | +1.28 | +1.77 | +1.40 |
| MES | 15 | h8 | event | with signal | 2150 | +0.868 | 0.594 | +5.03 | +1.53 | +1.55 | +1.50 | +1.50 |
| MES | 15 | h16 | event | with signal | 2150 | +0.848 | 0.594 | +4.93 | +1.43 | +1.44 | +1.42 | +1.38 |
| MES | 15 | eod | event | with signal | 2150 | +0.942 | 0.594 | +5.48 | +1.98 | +1.78 | +2.37 | +1.81 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.048 | -0.072 | -0.068 | -0.040 | -0.122 | +0.000 | +0.838 | +0.832 | +0.836 | +0.859 | +0.831 |

## Calibration

- MES 15-min: 35981 bars, 2150 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: FAILED at 2017-04-24 14:30:00 (43 of 100 cuts changed earlier values) -> all verdicts INVALID.

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
