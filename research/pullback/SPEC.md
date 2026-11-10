# PRE-REGISTERED SPECIFICATION: Trend-pullback process (EMA 8/20/50 + Momentum + swing support) and Analog sub-test

Version 1.0, frozen 2026-11-08, before any result is computed. All 121 selectable variants, the selection rules, the
controls and the pass/fail criteria are fixed below. Nothing may be added, dropped or retuned after results are seen.
If a bug is fixed, the fix is logged with a date and every number is recomputed. Every variant is reported,
including the losers.

Prior expectation, from the research: the trend filter has weak support; EMA alignment, Momentum(14), intraday
pullback entries and "today repeats yesterday" have little support or contrary support (STW 1999: best of 7,846
rules p = 0.908 on S&P futures; Baltussen 2021: yesterday's last half-hour predicts today's NEGATIVELY). The
default expectation is therefore NO EDGE after costs. The test is designed so that luck from choosing among many
variants cannot pass as edge.

---------------------------------------------------------------------------------------------------------------
## 0. Run environment

    cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib:. python3 <script>

- The project is read-only. Code and outputs go under `research/pullback/` (builders and reconciler only).
  Scratch work goes under `/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/pullback/<name>/`.
- No paid APIs. Never download data.
- All arithmetic is float64. Prices are compared exactly; they sit on the tick grid. Every inequality below is strict
  unless written ≤ or ≥.

---------------------------------------------------------------------------------------------------------------
## 1. Data

| Market traded | File | Sample | $/point | Tick | Cost per round trip per contract |
|---|---|---|---|---|---|
| MES | data/ES_fut_1m.csv | 2010-06-06 to 2026-11-06 | 5.00 | 0.25 ($1.25) | 2 x 1.25 + 1.00 = **$3.50** |
| MNQ | data/NQ_fut_1m.csv | 2010-06-06 to 2026-11-06 | 2.00 | 0.25 ($0.50) | 2 x 0.50 + 1.00 = **$2.00** |
| MYM | data/YM_fut_1m.csv | 2018-01-01 to 2026-11-06 | 0.50 | 1.0 ($0.50) | 2 x 0.50 + 1.00 = **$2.00** |

Columns: `ts_event, Open, High, Low, Close, Volume, instrument_id`. `ts_event` is the bar's OPEN time. The file
stores it with a UTC offset (e.g. `-04:00`).

1.1 Loading. Parse `ts_event` as a timezone-aware instant and convert it to America/New_York (ET). Drop
duplicate timestamps (keep the first) and sort. `research_lib.bars_1m(sym)` does exactly this and may be used. It
also adds `sess` and `tmin` (below).

1.2 Session date: `sess = date(ET timestamp + 6 hours)`. A session runs from 18:00 ET on the previous day to 17:00
ET. Calendar (per market): every session date that has at least one bar with ET open time in [09:30, 16:00).
Daily P&L series are indexed on this calendar; days without trades are 0.

1.3 Contract series: a maximal run of consecutive 1-minute bars with the same `instrument_id`. If the id flips
back, a new series starts. All indicators are computed per contract series and run continuously across sessions,
nights and weekends inside the series. They reset at every new series. Raw prices are used; nothing is back-adjusted.

1.4 Segment: a maximal run of consecutive bars in one contract series where every step
`ts[i] - ts[i-1] ≤ 5 minutes`. A position never spans two segments. It is closed at the Close of the last bar of
its segment (exit reason `segment_end`). Using that knowledge is an accepted data-structure convention.

1.5 Last prices, used for "today's $" rescaling: ES 7404.0, NQ 27107.5, YM 51390.0. These are the Closes of the
2026-11-06 16:59 bars.

---------------------------------------------------------------------------------------------------------------
## 2. Signal bars (timeframes TF ∈ {5, 15, 60} minutes)

2.1 Bucket. For a 1-minute bar with tz-aware ET open time `ts`:
`bucket_start = ts - ((ts.hour*60 + ts.minute) mod TF) minutes`. The arithmetic is done on the tz-aware instant,
so the repeated 01:00 hour on the DST fall-back day forms two separate buckets. Signal bar key =
(contract series, bucket_start). Signal OHLC = first Open, max High, min Low, last Close of the 1-minute bars
present. Missing minutes are allowed. `close_time = bucket_start + TF`.

2.2 Decisions are made at `close_time` using only signal bars with index ≤ t and 1-minute bars with open time
< close_time.

2.3 Entry bar = the first 1-minute bar with open time ≥ close_time. It must be in the same segment as the last
1-minute bar of signal bar t. Otherwise the order is cancelled.

2.4 Warm-up. Signal bar t (0-based index within its contract series) is usable only if t ≥ 149. On 60-minute bars
this blocks roughly the first week after each roll. That cost is accepted.

---------------------------------------------------------------------------------------------------------------
## 3. Indicators (per contract series, on signal bars)

- EMA(n): `E_0 = C_0`, `E_t = a*C_t + (1-a)*E_{t-1}`, with `a = 2/(n+1)`. This equals pandas `ewm(span=n, adjust=False)`.
  n ∈ {8, 20, 50}.
- ATR(14), Wilder: `TR_0 = H_0 - L_0`, `TR_t = max(H_t-L_t, |H_t-C_{t-1}|, |L_t-C_{t-1}|)`,
  `ATR_0 = TR_0`, `ATR_t = ATR_{t-1} + (TR_t - ATR_{t-1})/14`. This equals `ewm(alpha=1/14, adjust=False)` on TR.
- Momentum: `MOM_t = 100 * C_t / C_{t-n}`, n ∈ {10, 14, 20}.
- Trend state:
  - **T1** (default). LONG if EMA8 > EMA20 > EMA50. SHORT if EMA8 < EMA20 < EMA50. Otherwise NONE.
  - **T2**. T1 plus a slope condition: LONG also needs EMA50_t > EMA50_{t-5}; SHORT also needs EMA50_t < EMA50_{t-5}.
- Swing pivots, k ∈ {2, 3, 5}. Bar i is a swing low if `L_i < min(L_{i-k..i-1})` and `L_i ≤ min(L_{i+1..i+k})`.
  The mirror rule with highs defines a swing high. All 2k+1 bars must be in the same contract series. The pivot is
  CONFIRMED at the close of bar i+k and may be used only by decisions at bars t ≥ i+k.
  - "Most recent confirmed swing low at t" is the one with the largest i such that i+k ≤ t and i ≥ t-200.
    If none exists, there is no swing.
- Buffer: `buf_t = max(2 ticks, b * ATR_t)`, with b = 0.25 by default.
- Tick rounding: long stops round DOWN to the tick grid (floor) and short stops round UP (ceil). Long targets round
  UP and short targets round DOWN. All rounding is to the market's tick.

---------------------------------------------------------------------------------------------------------------
## 4. The rule (written for LONGS; shorts are the exact mirror: highs↔lows, >↔<, LONG↔SHORT, up↔down)

4.1 Support level S_t at bar t (variant dimension SUP):
- **swing** (default): the most recent confirmed swing low at t.
- **daylow**: the minimum Low of the session's 1-minute bars with open time < bucket_start of t. At least 60 such
  bars are required; otherwise S does not exist.
- **ema20**: EMA20_t.

4.2 Touch bar j (long). All of these must hold:
- trend state at j is LONG;
- S_j exists and `C_j > S_j`;
- `L_j ≤ S_j + d*ATR_j`, with d = 0.5 by default;
- `L_j > S_j - buf_j`.

4.3 Trigger at decision bar t. The position must be flat at the close of t; an exit earlier inside bar t counts as
flat. Let j be the LARGEST index in {t, t-1, t-2, t-3} that is a long touch bar. Enter long if ALL of these hold:
- trend state at t is LONG;
- `C_t > S_j`;
- `min(L_j..L_t) > S_j - buf_j`;
- the trigger condition holds:
  - **E1 momentum turn** (default): `MOM_t > MOM_{t-1}` and `MOM_{t-1} ≤ MOM_{t-2}`.
  - **E2 EMA8 reclaim**: `C_t > EMA8_t` and `C_{t-1} ≤ EMA8_{t-1}`.

  Indices t-3 to t must all be usable (t-3 ≥ 149) and in the same contract series.

4.4 Order: buy 1 contract at the Open of the entry bar (2.3) = price `E`.

4.5 Initial stop:
- **SB** (structural, default): `stop = floor_tick(S_j - buf_j)`.
- **FA** (fixed ATR): `stop = floor_tick(E - 1.5*ATR_t)`.

Skip the trade if `E ≤ stop + 1 tick` or `E - stop > 3*ATR_t`. Let `R = E - stop`.

4.6 Entry time window (on the entry bar's ET open time):
- **ALL** (default): any time except [16:30, 18:00).
- **RTH**: [09:30, 15:45).
- **EXCL**: as ALL, but also no entries in [08:25, 08:35) or [09:25, 09:40).

Signal bars are always built from all hours.

4.7 Forced flat:
- ALL and EXCL: exit at the Close of the last 1-minute bar of the session with open time < 16:45 (reason
  `flat_1645`). This also guarantees flat before weekends and holidays.
- RTH: exit at the Close of the last bar with open time < 16:00 (`flat_rth`).

Segment ends also force an exit (1.4). An entry whose entry bar is itself a forced-exit bar is cancelled.
Positions therefore never cross sessions: entry session = exit session = the trade's P&L date.

4.8 Exit rule (dimension EXIT). Every exit rule also keeps the initial stop, the time stop, the reversal rule (4.9)
and the forced flats.
- **X1 prior swing high** (default): target = the most recent confirmed swing high at t whose level is > E.
  Search back to i ≥ t-200. If there is none, target = E + 2R. The target is a resting limit order.
- **X2 2R**: target = E + 2R.
- **X3 EMA20 trail**: no target. At each signal close after entry, if `C < EMA20`, exit at the next 1-minute Open
  (reason `signal_trail`).
- **X4 trend flip**: no target. At each signal close after entry, if the trend state is not LONG, exit at the next
  Open (`signal_flip`).
- Time stop (all variants): exit at the next Open after the close of signal bar t_entry + 32, where t_entry is the
  decision bar (reason `time`).
- Signal exits are first checked at the close of the first signal bar that contains the entry bar.

4.9 Reversal (dimension REV). At each signal close while long, a "reversal" means `MOM_t < 100` AND `C_t < ` the
most recent confirmed swing low at t.
- **R1** (default): exit at the next Open (`reversal`).
- **R0**: ignore reversals.
- **R2**: exit and at the same Open go SHORT 1 contract. The touch condition is not required. Stop = ceil_tick(the
  most recent confirmed swing high at t + buf_t). Skip the short if there is no swing, if `E ≥ stop - 1 tick`, or if
  `stop - E > 3*ATR_t`. The short is managed with the variant's exit rule mirrored. R2 applies to every position,
  so a reversal short can itself reverse.

4.10 1-minute processing order (for every 1-minute bar, while a position or order exists):
1. At the Open, execute exits scheduled at the previous signal close, then scheduled entries, reversals and adds.
2. Gap check on every open contract, including ones just entered. Long: if `Open ≤ stop`, fill at Open (`stop`).
   If `Open ≥ target`, fill at Open (`target`).
3. Long: if `Low ≤ stop`, fill at stop (`stop`). Otherwise, if `High ≥ target`, fill at target (`target`). If both
   are touched in the same bar, the STOP wins.
4. If this bar is a forced-flat or segment-end bar, exit what remains at Close.

Signal-based exits are decided only at signal closes. After an exit, the next entry may come from any later
decision. No new non-reversal entry may execute at the same Open as a scheduled exit. One position per market at a
time, plus at most one add (4.11).

4.11 Add-on (dimension ADD; never on reversal positions):
- **A0** (default): no add.
- **Ab** and **Ac**: while long exactly 1 contract from entry E1 with support S1 (= S_{j1}), at a later decision bar
  t2 with no exit scheduled, a full new long setup (4.2-4.5) with touch bar j2 > t_entry triggers an add if
  `S2 > S1` and `min(L_{j2..t2}) > S1`. Buy 1 more contract at the next Open, price E2.
  - **Ab**: contract 2 has its own stop `floor_tick(S2 - buf_{j2})` and its own X1/X2 target computed from E2 at t2.
    Contract 1 keeps its stop and target.
  - **Ac**: breakeven price `P_be = ceil_tick((E1+E2)/2 + cost_rt/USD_PT)` (MES: +0.70, so +0.75 after rounding).
    If `P_be ≥ E2`, the add is REFUSED and no contract is bought. Otherwise both contracts' stops become
    `max(P_be, stop1)`. Contract 2 gets its own target as in Ab.
  - In both cases, signal, reversal, time and flat exits close both contracts. The time stop counts from the first
    entry. The two contracts are recorded as separate legs.

Max position 2 contracts. The Lucid limit of 20 micros never binds.

4.12 P&L per leg:
- As traded: `usd = dir*(exit-entry)*USD_PT - cost_rt`.
- Today's $ (eval only): `usd_today = dir*(exit-entry)/entry * P_last * USD_PT - cost_rt`.

Daily P&L is the sum by session date.

---------------------------------------------------------------------------------------------------------------
## 5. Variants (121 selectable; listed exactly)

Default settings: TF15, T1, MOM14, k3, SUP swing, d 0.5, E1, SB with b 0.25, X1, R1, A0, window ALL.

**PRIMARY = S040** (the trader's stated process). It is judged on its own, with no selection.

**Core grid S001-S081**: TF {5, 15, 60} x n {10, 14, 20} x k {2, 3, 5} x EXIT {X1, X2, X3}. All other settings are
the defaults. The ID is `1 + 27*iTF + 9*in + 3*ik + iX`, with every index 0-based in the order listed. Examples:
S001 = TF5/n10/k2/X1, S040 = TF15/n14/k3/X1, S081 = TF60/n20/k5/X3.

**Block B**: one change from S040 each.

| ID | Change | ID | Change |
|---|---|---|---|
| S082 | trend T2 | S090 | stop FA (1.5 ATR) |
| S083 | SUP daylow | S091 | EXIT X4 |
| S084 | SUP ema20 | S092 | REV R0 |
| S085 | d 0.25 | S093 | REV R2 |
| S086 | d 1.0 | S094 | ADD Ab |
| S087 | trigger E2 | S095 | ADD Ac |
| S088 | b 0.5 | S096 | window RTH |
| S089 | b 1.0 | S097 | window EXCL |

**Block C**: S098 RTH+Ab, S099 RTH+Ac, S100 EXCL+Ab, S101 EXCL+Ac.

Strategy family = S001-S101 (101 variants). **Analog family = A01-A20** (section 9, 20 variants). Total 121.
Every variant is run on ES, NQ and YM.

**Neighbour runs** are diagnostic only and never selectable. For a strategy variant v, the neighbours are v with
exactly one of these moved one step, inside each list's bounds: TF (5, 15, 60), n (10, 14, 20), k (2, 3, 5), d
(0.25, 0.5, 1.0), b (0.25, 0.5, 1.0; only when the stop is SB). That gives up to 10 neighbours. For an analog
variant, the neighbours are: the other T, the other H, L one step along (1, 20, 60) with K fixed, and the other K
when L ≥ 20.

---------------------------------------------------------------------------------------------------------------
## 6. Metrics (each market alone, and the portfolio)

Ranges by session date:
- 2010-17: 2010-06-07 to 2017-12-31
- 2018-21: 2018-01-01 to 2021-12-31
- 2022-26: 2022-01-01 to 2026-11-06
- 2023-26: 2023-01-01 to 2026-11-06
- Full
- Halves: split at the market's median calendar session

For YM, only 2018 onward exists.

For every range, report these as traded:
- net $; $ per trade; trades per year (trades / (sessions/252)); win rate; average win; average loss;
- max drawdown (peak-to-trough of cumulative daily $); worst day;
- daily Sharpe = mean/sd(ddof=1) x √252 over ALL calendar sessions in the range, zeros included;
- t = mean/sd x √(n_days);
- splits: long vs short; by entry hour bucket (18-24, 0-8, 8-9:30, 9:30-11, 11-14, 14-16:30);
- by volatility tercile. The regime of a session is the tercile of the previous session's (High-Low)/Close (whole
  session), ranked within the trailing 252 sessions.

Size is 1 contract for A0 variants and up to 2 for add variants.

Portfolio = MES + MNQ + MYM at 1 micro each: the sum of daily $ over the union of the calendars.

---------------------------------------------------------------------------------------------------------------
## 7. Protocol

7.1 Selection score = daily Sharpe (6) in the selection window. A variant needs at least 30 trades in the window
to be eligible. Ties go to the lower ID. Strategy and analog families are selected separately.

7.2 In-sample optimisation, per market and per family. Choose the best variant on:
(a) the full sample;
(b) 2018-01-01 to 2026-11-06;
(c) 2022-01-01 to 2026-11-06.

Report each chosen variant's metrics in ALL ranges. **Every such number is labelled IN-SAMPLE.**

7.3 Rolling walk-forward (the realistic estimate). For each year Y from 2013 to 2026 (YM: from 2021), choose the
best variant (7.1) on sessions from Y-3-01-01 to Y-1-12-31. Then take that variant's trades whose session falls in
year Y. Stitch the years together. Do this per market and per family. Walk-forward portfolio = the sum of the three
markets' walk-forward daily series. Report the yearly picks, the per-year $, and the metrics for 2013-26, 2018-21,
2022-26 and 2023-26.

7.4 Stability. For each in-sample pick (7.2a, 7.2b), compute the neighbour runs over the same window. The pick is
STABLE if all neighbours have net > 0 AND the median neighbour Sharpe ≥ 0.5 x the pick's Sharpe. With no
neighbours, the pick counts as not stable. Also report the share of walk-forward yearly picks that are stable on
their own selection window.

7.5 Random-entry control (1,000 draws, `rng = numpy.random.default_rng(12345)`, re-created fresh for each series
tested). For each real leg i, in chronological order (entry time, then leg number):
- holding h_i = the number of 1-minute bars from the entry bar to the exit bar, inclusive;
- direction dir_i = the leg's direction.

Eligible entry bars E_i are bars j that meet all of these:
- the session date is in the same calendar year as the real leg;
- the open time is inside the variant's entry window;
- bars j to j+h_i-1 lie in one segment and one session, and all open before the forced-flat time (16:45, or 16:00
  for RTH).

E_i is sorted by time. For each draw d = 0..999, and for each leg in order: `u = rng.integers(0, len(E_i))`.
Random leg P&L = `dir_i*(C[j+h_i-1] - O[j])*USD_PT - cost_rt`, where j = E_i[u]. If E_i is empty, that leg is
dropped from every draw and the drop count is reported.

Statistics: net $ and daily Sharpe over the series' range. Percentile = the share of draws strictly below the real
value. The control is applied to S040, to every in-sample pick, and to every walk-forward series (the walk-forward
legs keep each year's variant's window).

7.6 Family-wise check. For every variant v in a family, and every draw d (7.5, each with its own fresh
default_rng(12345)), compute Sharpe_{v,d} over the window. Let `M_d = max_v Sharpe_{v,d}`. Then
`p_FW = (1 + #{d : M_d ≥ max_v Sharpe_v,real}) / 1001`. Report it for the full, 2018-26 and 2022-26 windows. Do
this for the strategy family (101), the analog family (20) and both together (121).

7.7 Cross-market check. Run each market's in-sample picks (7.2a, 7.2b) on the other two markets unchanged. Report
the same metrics and whether net > 0 over 2018-01-01 to 2026-11-06.

---------------------------------------------------------------------------------------------------------------
## 8. LucidFlex 25K evaluation

Use the root `prop_sim.py`:
`prop_sim.simulate(daily_today, prop_sim.Rules(), start_from="2018-01-01")`.

Rules():
- start $25,000;
- target $1,250;
- $1,000 maximum loss trailing the highest end-of-day balance, locking at $25,100 once a close exceeds $26,100;
- best day ≤ 40% of profit;
- no daily loss limit.

These are the same pass rules as `research/eval_short_trades.py` (passrate). Inputs are the daily usd_today series
(4.12).

Report the pass rate, the fail rate, the median days to pass (with the 25th and 75th percentiles), the eras 2018-21
and 2022-26, and the open share. Report this for:
- S040;
- each in-sample pick;
- the walk-forward series (headline);
- the portfolio.

Run each at 1, 2, 3 and 5 contracts: multiply each leg's usd_today by that number. Costs scale with it, because
cost_rt is included per contract.

Sensitivities: `Rules(consistency=0.50)` and `Rules(dll=600)`.

Compare against the existing plans over the same start window:
- "ONB 9:xx entries, cap 0.15%": 80%, 133 days;
- current models: 58%, 47 days.

---------------------------------------------------------------------------------------------------------------
## 9. Analog ("today repeats a past day") sub-test, A01-A20

Boundaries for session s: B_0 = 18:00 ET on the evening before s, and `B_m = B_0 + 15m minutes`.
- P(B_0) = the Open of the first bar with open time in [18:00, 18:05).
- P(B_m), for m ≥ 1, = the Close of the last bar with open time in [B_m - 5 min, B_m).

A session is "usable to X" if every P(B_m) with B_m ≤ X exists and all those bars share one instrument_id.

Shape: `x_s = [ln(P(B_m)/P(B_0)) for m = 1..M]`, where B_M = T.

Decision time T ∈ {10:00, 13:00}, horizon H ∈ {60, 120} minutes, and (L, K) ∈ {(1,1), (20,1), (20,5), (60,1),
(60,5)}. ID = `1 + 10*iT + 5*iH + iLK`. **The analog primary is A06** (T 10:00, H 120, L 1, K 1 = "today repeats
yesterday").

Procedure:
- Today must be usable to T.
- The pool is the L most recent earlier sessions that are usable to T+H.
- Rank the pool by the Pearson correlation of x_today with x_cand; ties go to the more recent session. Take the
  top K.
- Forecast `f = mean of ln(P(T+H)/P(T))` over those K sessions. Trade `sign(f)`; if f = 0, no trade.
- Enter at the Open of the first bar with open time ≥ T. It must be in the same segment as the bar that gave P(T),
  with open time < T+5.
- Exit at the Close of the last bar with open time < T+H (`time`), or earlier at a segment end. There is no stop.
  Size is 1 contract, at the market's own costs.

Not selectable benchmark: the sign of `ln(P(T)/P(B_0))`, i.e. momentum since 18:00, traded the same way.

Report the same metrics, halves, controls (7.5 with window [09:30, 16:00-H)), walk-forward (analog family),
family-wise test and eval as the strategy.

---------------------------------------------------------------------------------------------------------------
## 10. Decision criteria (fixed now)

A family on a market is WORTH PAPER/EVAL TRADING only if ALL of these hold:
1. The walk-forward series has net > 0 after costs, with t ≥ 2 on daily P&L (2013-26; YM 2021-26).
2. The walk-forward net is > 0 in 2022-26 AND in 2023-26.
3. The walk-forward net $ is above the 95th percentile of its random-entry control (7.5).
4. The in-sample picks 7.2a and 7.2b are both STABLE (7.4).
5. Pick 7.2a has net > 0 for 2018-26 on at least 2 of the 3 markets (7.7).

S040 is reported against criteria 1-3 on its own, as a fixed rule with no walk-forward selection. The portfolio is
judged on criteria 1-3 using the walk-forward portfolio. p_FW is reported alongside as context. In-sample numbers
never satisfy any criterion.

For the evaluation use case, the walk-forward pass rate and median days to pass are set against 80%/133 days and
58%/47 days. A plan that fails criteria 1-3 is not recommended for evaluations, whatever its in-sample pass rate.

---------------------------------------------------------------------------------------------------------------
## 11. Outputs (for reconciliation)

`research/pullback/trades_<MKT>_<ID>.csv` has these columns:

    market, variant, leg, dir, session, entry_ts, entry_px, exit_ts, exit_px, exit_reason, contracts, usd, usd_today

Exit reasons:

    stop, target, signal_trail, signal_flip, reversal, time, flat_1645, flat_rth, segment_end

Plus a summary of every table above.

Reconciliation: two independent builds must produce identical trade files for S040, S093, S095 and A06 on ES. If
any line differs, the cause is traced to a clause of this spec, and the clause is clarified in a dated note before
any other result is used.

(Saved at /tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/pullback/SPEC.md)
