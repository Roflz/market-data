# Pre-registration: rebalancing-pressure signal, traded the way the forecast says (MNQ)

Written 2026-11-08 before any new P&L was computed. Only results already reported in
`scratchpad/caltests2/` (A, B, reconcile, nq runs of test 12) were looked at.

## 1. What the signal is (unchanged from test 12)

Test 12 is a DAILY threshold-rebalancing signal, not a month-end calendar rule (month-end calendar
rebalancing was test 1 / test 13). For every NYSE trading day t (cash_day sessions of
`data/daily_sessions_ES.pkl`):

- rES_t = (close_adj_t - close_adj_{t-1}) / close_raw_{t-1}, ES daily session close (15:59 bar close = 16:00 price;
  12:59 bar close on early-close days).
- rZN_t = same for ZN, using the close of the last hourly ZN bar that opens at or before 15:00 ET on day t
  (normally the 15:00 bar = 16:00 price), back-adjusted additively at instrument changes.
- 26 hypothetical 60/40 ES/ZN portfolios with rebalancing thresholds d = 0.0%, 0.1%, ..., 2.5%. Each starts at
  w = 60% on 2010-06-07. Each day: w_pre = w(1+rES)/(w(1+rES) + (1-w)(1+rZN)); dev = w_pre - 0.60;
  the portfolio resets to w = 0.60 if |dev| >= d, else w = w_pre.
- s_t = mean of the 26 devs (in weight units; 0.005 = 0.5 pp).

Positive s = stocks have outrun bonds since the funds last rebalanced, so rebalancers must SELL stocks;
negative s = they must BUY.

The ES-built signal is kept (it is the test-12 definition and the pension story is about the S&P 500). It forecast
the next day's NQ close-to-close return with slope -31 bp per 1 pp of signal, Newey-West t = -2.83 (A and B runs),
intercept +16 bp. The t = -2.94 figure in the brief is the "nq" run, where the signal was built from NQ instead of
ES (the markets were swapped); that version is reported below as report-only and cannot rescue the result.

## 2. Why the simple rule failed (from reported numbers only)

Simple rule: hold -sign(s_t) from close t to close t+1 whenever |s_t| >= 0.5%.
MES: 1,600 days, gross $4.49/day t = 1.01, net t = 0.72, 5/9 blocks, post-Mar-2023 negative.
MNQ (nq run): net 3.19 bp/day, t = 0.75, 4/9 blocks, 2023-2025 all negative.

1. It was a short-bias rule in a bull market. The signal's mean is +0.28 pp (stocks usually outrun bonds), so
   1,380 of 1,600 days were SHORT. The forecast has intercept +13 to +16 bp; the predicted next-day return at
   s = +0.5 pp is about zero. So most short days were days on which the forecast itself expected roughly
   nothing, and they paid the equity drift.
2. A fixed 0.5 pp threshold is not "extreme": it is hit on 39% of days, and in calm bull years the signal sits
   above it for months.
3. The profit came from crises: on MES 2020 alone made $5,554 of the $5,110 total; on MNQ 2018-2022 made all
   of it. The forecast slope after March 2023 is weak (NW t -0.4 to -0.9).
4. Costs were not the problem (about 1 bp per day of turnover).
5. Minor: it entered at the same 16:00 close used to compute the signal (not executable).

What the forecast actually says: the next day is relatively WORSE after a high signal and relatively BETTER
after a low signal, compared with the usual day. So the new rules (a) judge "high/low" relative to the recent
past (trailing 252 trading days), which removes the bull-market level bias, (b) trade only the extremes, (c)
enter after the signal is known.

## 3. Common mechanics (all rules)

- Decision time 16:05 ET on each NYSE trading day t that is not an early-close day. The signal s_t uses only
  bars that closed by 16:00 (ES 15:59 bar, ZN 15:00 hourly bar). Early-close days: no decision; any position
  is closed there and stays flat until the next normal decision.
- Reference distribution: the 252 previous signal values s_{t-252} .. s_{t-1} (today excluded). No decision
  until 252 prior values exist (first decision about June 2011).
  - pct_t = fraction of those 252 values that are <= s_t.
  - z_t = (s_t - mean of those 252) / (sample sd of those 252).
- Position p_t (MNQ contracts, sign = side) is held from the open of the NQ 1-min bar stamped 16:05 ET on day t
  to the open of the bar stamped 16:05 ET on the next NYSE trading day (13:05 if that day closes early).
  If the exact bar is missing, use the first bar opening within the next 15 minutes (10 on early-close days);
  if none, that holding segment is flat. If the next decision gives the same position, the position is simply
  kept (no trade, no cost).
- Rolls: a segment is flat if the NQ instrument_id changes anywhere between its entry bar and its exit bar
  (raw prices, never across contracts).
- Costs: MNQ $1.00 per contract per side ($2.00 round trip = 1 NQ point). A change from p to p' costs
  $1.00 x |p' - p| (a flip -1 -> +1 costs $2.00). Stress test at 2 ticks per side ($1.50 per side).
- A "trade" = a maximal run of consecutive segments with the same nonzero sign (size may vary inside the run
  for variant A). Trade net $ = sum of segment P&L - all side costs inside the run, including its entry and exit.
  Trades are dated by entry date.
- Sample: decisions 2011-06 (end of burn-in) to 2026-11-05 (last segment ends 2026-11-06, data end).
- bp per trade = 1e4 x net points / raw entry price.

## 4. Rules

PRIMARY P - "extreme-decile reversal, next day":
  pct_t <= 0.10 -> long 1 MNQ;  pct_t >= 0.90 -> short 1 MNQ;  otherwise flat.

VARIANT A - "scaled by signal size":
  p_t = -sign(z_t) x min(3, floor(|z_t|)), i.e. 0 if |z| < 1, 1 contract for 1 <= |z| < 2, 2 for 2-3, 3 for >= 3,
  long when z is negative, short when positive.

VARIANT B - "buy side only":
  pct_t <= 0.10 -> long 1 MNQ; otherwise flat. (Tests whether the effect is all in rebalancers' BUYING after
  stocks lag bonds.)

Three trials in total. No other thresholds, windows, holding times or filters will be tried.

## 5. Controls (fixed seed 12345, 1,000 replications)

- Random direction: same trades (same entry/exit segments, same sizes, same costs), each trade's side set by
  an independent fair coin. Statistic: total net $.
- Shuffled-date placebo: the rule's whole segment-position path is circularly shifted by a random offset of
  252..(M-252) segments (M = number of segments), positions landing on flat-forced segments (rolls, early
  closes, missing bars) are set to 0, costs recomputed. Statistic: total net $. This keeps the same mix of
  long/short days and holding lengths but breaks the link to the signal, so it measures how much of the P&L
  is just market drift.

## 6. Pass criteria (MNQ; evaluated and reported one by one)

PRIMARY passes only if ALL hold:
  C1  trade-level t of net $ >= 2.0 over the full sample (2011-06 .. 2026-11)
  C2  net total > 0 for trades entered 2018-01-01 .. end
  C3  net total > 0 for trades entered 2023-01-01 .. end
  C4  net total > 0 in at least 6 of 8 two-year blocks: 2010-11, 2012-13, 2014-15, 2016-17, 2018-19, 2020-21,
      2022-23, 2024-26 (2026 joins the last block; 2010-11 contains only Jun-Dec 2011 because of the burn-in)
  C5  total net $ above the 95th percentile of the random-direction control
VARIANTS A and B: the same, but C1 needs t >= 2.4.

Extra check, NOT part of the official pass list (reported as a warning label): total net $ above the 95th
percentile of the shuffled-date placebo ("beats drift"). A rule that passes C1-C5 but fails this is labelled
"passes on paper, but not distinguishable from drift".

## 7. Report-only (cannot change any verdict)

- MES: the same positions on ES 1-min prices, $1.75 per side ($3.50 round trip).
- 2-tick cost stress; day-level t; long and short legs separately; by year.
- The NQ-built signal (the "nq" run's t = -2.94 version) run through rule P.
- Correlation of daily P&L with the three live MNQ models (chosen_models_trades.csv).
