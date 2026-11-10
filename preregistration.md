# Pre-registration: literature enhancements (written 2026-11-08, before any of these runs)

Base strategy ("BASE"): MNQ overnight-level break + daily trend. Signal at 5-min closes 9:35-15:00 ET when price first
closes beyond the overnight high (daily trend up) or low (trend down) within the last 5 minutes. Entry next bar open
+1 tick; initial stop 2 x ATR(5m), snapped to the tick grid; hold until stopped or the 5 PM ET close. Max 3 trades per
session, one position at a time. Costs: 1 tick slippage per side on market/stop fills, $1.50 commission per round trip.
Results are reported in R (initial risk) and in $ per micro, per year, MNQ and MES separately, gross and net.

## Common acceptance gates (fixed now)
- Net mean positive in >= 2/3 of calendar years with >= 20 trades (2-year blocks for event strategies).
- Beats random entries with identical exits (same direction mix and time of day where stated).
- Mean gross edge >= 1.5 x round-trip cost.
- Single pre-registered replication: report exact day-level t; t >= 2 = "promising, forward test"; searched results need t >= 3.
- Deflated Sharpe uses the effective number of trials in the ledger below plus all earlier work (~1,000 configurations).
- An enhancement to BASE counts only if it improves BASE out of sample (walk-forward) in total AND in most years AND does
  not reduce 2026.

## Step 1. Is BASE real? (no variants: these are checks, not strategies)
1a. Sign-flipped synthetic markets (generator G2 from the report): each real 1-min NQ bar is reflected around its open
    with probability 1/2; bars chained so each open = previous synthetic close; volume unchanged.
    Two drift settings: zero drift, and each calendar year's mean 1-min return added back. 100 replications each.
    Statistic: BASE total net R 2011-2026. Empirical p = (1 + #null >= real) / (1 + 100).
1b. Execution delay: enter 1 and 2 bars (5 / 10 min) later than BASE. Reported, no selection.

## Step 2. Volatility module (4 variants, logged as 4 trials)
Forecast = HAR model of daily realized variance (sum of squared 5-min log returns over the full session), fitted on
an expanding window of prior days only, predicting today's realized volatility. Terciles from expanding history after
a 250-day burn-in.
  V1 skip trades when today's forecast is in the top tercile
  V2 trade only when the forecast is in the bottom tercile
  V3 size = constant dollar risk per trade (report $ at a fixed $100 risk per trade instead of 1 contract)
  V4 V3 x (median forecast / today's forecast), capped at 0.5x-2x (volatility targeting)

## Step 3. ML filter on BASE ("meta-labeling", 2 variants)
Walk-forward by year (fit on years < Y-2, choose threshold on Y-2..Y-1, refit on < Y, test Y), gradient-boosted
classifier of P(trade R > 0) from the 88 entry-time measures of the futures pipeline + the HAR forecast.
  M1 skip trades below the probability threshold (threshold grid: none, 20th, 35th, 50th percentile of training predictions)
  M2 size = 0.5x / 1x / 1.5x by prediction tercile (training-period cut-offs)
Control: identical pipeline with labels shuffled between trades.

## Step 4. FOMC handling (official calendar; 2 variants)
  F1 no new entries from 13:30 to 14:15 ET on scheduled FOMC statement days (replaces the size-of-bar detector)
  F2 trade only in even FOMC-cycle weeks (Cieslak et al.: week 0 = days -1..3, week 1 = 4..8, ...)

## Step 5. Literature replications (specifications exactly as in literature_report.md section 7)
  P1 noise-band breakout, variants A (as published) and B (+ resting stop at the trailing level); 1 contract and
     vol-targeted; ES and NQ; primary period Oct 2024 - Nov 2026, also 2010-2024.
  P2 last-half-hour momentum (prior close to 15:30 signal), variants a-d; ES and NQ; primary era Jun 2020 - Nov 2026;
     Holm adjustment over the 8 primary tests.
  P5 opening-range breakout on the first 5-minute range, with a random-direction control; ES and NQ.

## Trial ledger (this round)
Step 1: 0 strategy trials (checks). Step 2: 4. Step 3: 2 (+ threshold grid inside walk-forward). Step 4: 2.
P1: 2 variants x 2 sizings x 2 markets = 8. P2: 4 x 2 = 8 primary (+16 secondary). P5: 2.
Total new trials this round: about 26 primary (+16 secondary), added to ~1,000 earlier configurations.
