# v3 PRE-REGISTRATION (frozen 2026-11-09, before any v3 hypothesis test was run)

Written 12:23-12:45 MST, 2026-11-09. Inputs: the v3 literature sweep, the methods protocol
(`v3/stats_protocol.py`), the internal-evidence re-cut (`v3/exp_internal/`), the eval-math study
(`v3/exp_evalmath/`, `v3/out/evalmath_summary.txt`) and the shared harness (`v3/harness.py`).
Machine-readable copies with sha256 and UTC time: `v3/out/prereg/<id>.json` (written by
`stats_protocol.prereg_record`, which refuses to overwrite). The hash of this file is in
`v3/out/prereg/PREREG.md.sha256`. **Any change to a rule below gets a NEW id and counts as a new trial.**

Plain-words summary: we test 5 frozen trading rules plus 1 frozen combination of them (the
"confirmatory family"). Each must beat a matched control (the same trade, same side, same clock
times, but on random days of the same year) after costs, survive a multiple-testing correction, and
pass robustness checks. Everything else (variants, other markets, filters, new ideas) is "secondary"
or "exploratory": reported, but it cannot be called proven in this round unless it clears the much
stricter mined-idea bar.

**Honest caveat, stated before testing:** A1-A4 were already measured on this data by earlier runs
(the archive and the internal re-cut). This round re-measures them with frozen rules, a new harness
and stronger controls; it is a gate, not a fresh discovery. Their final confirmation can only come from
forward paper trading (the locked holdout was already viewed for these rules). A5 and P0 are new.

---------------------------------------------------------------------------------------------------

## 0. Common protocol (applies to every hypothesis below)

### 0.1 Data and window
- Only `v3/data/*.parquet` through `harness.py` (cut before the locked holdout, which starts
  2025-06-30 18:00 ET). Never load raw 1-minute data for these tests; never read any file or number
  dated after 2025-06-30 (including old summaries with 2026 columns).
- Calendar: `H.calendar(("NQ","ES"))` restricted to sessions ≤ 2025-06-27 = 3,876 Globex sessions
  2010-06-07 .. 2025-06-27 (session = 18:00 previous evening to 16:45, labelled by its close date). The last
  harness session (2025-06-30, pre-holdout) is dropped because `sp.robust_report` asserts every session is
  < 2025-06-30; dropping it everywhere keeps all columns on one calendar. YM (MYM) exists from 2018 only; on earlier
  sessions MYM columns are 0 / not counted.
- Windows reported: every calendar year, 2010-17, 2018-25H1, 2018+, 2022+, full; "H1" = through 2025-06-27.
- No trade may be open during 16:45-18:00. Latest exit mark is 16:45 (= the 16:44 bar close).

### 0.2 Costs and units
- Per micro per trade: $1 commission + 1 tick slippage each way, +1 extra tick on stop fills
  (exactly `harness.SPEC` / `time_trades`: MES $3.50, MNQ $2.00, MYM $2.00 per round trip without a stop).
- **U1 (primary unit):** net $ per 1 micro at the historical price (harness `pnl_usd`).
- **U2 (price-normalised, pre-registered secondary unit):** for each trade,
  `U2 = gross_return × P_ref × $/pt − cost_usd` where gross_return = d × (exit_px − entry_px)/entry_px
  and P_ref = mean 16:00 price in 2025-01-02..2025-06-30: **NQ 20,789.6; ES 5,843.2; YM 42,516.3**.
  Reason: costs per trade are fixed in $ but were 3-10× larger in % terms in 2010-17 (NQ 2,000-6,000), so
  U2 answers "what would this trade make per micro at today's price and today's cost".
- Daily series: one row per calendar session, sum of all trades of that session (several markets summed
  for basket hypotheses), 0 on no-trade sessions.

### 0.3 Controls
- **C1 (primary matched control, every hypothesis):** each real trade re-placed on a random session of the
  same calendar year with the SAME entry mark, exit mark, side and stop/target distance in points:
  `H.random_time_trades(sym, entries, n_rep=R, keep_session=False, keep_marks=True, keep_side=True)`
  with a pass-through trade id `tid`. **R = 999** draws, run in chunks of ≤ 100 reps (seed = 1000·k + chunk,
  k = hypothesis number; A1 → 1, ..., A5 → 5) to keep memory < 2 GB. Draws whose session has no price at the
  mark are dropped; c_i = mean over the remaining draws of trade i. (Random sessions may include event days;
  this makes the control slightly harder to beat when events are good, i.e. conservative.)
  Custom-walker hypotheses (A2) build the same control with their own walker (same 5-minute entry clock time,
  same side, same stop distance in points, random session of the same year).
- **Primary statistic:** `d_t = Σ_{trades i in session t} (net_i − c_i)` in U1, on the full calendar.
  Because C1 has the same side and hours, d removes drift and (mostly) costs; therefore the claim also
  requires the raw net test (0.4, intersection rule).
- **Reported controls (all hypotheses):** C2 random side, same sessions and marks (direction skill);
  plain drift = long at the same sessions and marks (`H.drift_trades`); hour drift = long at the same marks
  on random same-year sessions (`H.hour_drift_trades`, n_rep = 100); `H.standard_report` with n_rep = 100.
  Event hypotheses also report C3 = the same rule applied on all non-event sessions (same weekday for A3).

### 0.4 Statistics
- Bootstrap: `sp.conservative_p(sp.boot_pvalue_mean, x, B=5000)` = the LARGEST one-sided stationary-bootstrap
  p over mean block lengths {1, 5, 10, 20} sessions; base seed 20261109. Also report the Newey-West t
  (`sp.hac_t`) and the harness `H.stats` table.
- p_d = conservative p of mean(d_t) > 0. p_net = conservative p of mean(raw U1 daily net) > 0.
- **Confirmatory family (Tier A), K = 6: A1, A2, A3, A4, A5, P0.** Decision = **Holm at α_A = 0.03**
  (sorted thresholds 0.005, 0.006, 0.0075, 0.010, 0.015, 0.030) applied to p_d.
  Romano-Wolf StepM (`sp.stepm` on the 6-column d matrix, mean block 10, B = 5000) and Hansen SPA_c are
  reported; a hypothesis rejected by StepM but not by Holm is labelled PROMISING, not SIGNIFICANT.
- **Intersection rule:** a Tier A claim needs Holm rejection on p_d AND p_net ≤ 0.05 AND all gates in 0.5.
- **Tier B (every secondary and exploratory column):** StepM within its family at 0.02/5 = 0.004, AND
  Newey-West t ≥ 3, AND DSR ≥ 0.95 with N_eff = Li-Ji effective count of that family's v3 columns + earlier
  trials (F3 momentum ≥ 45, F2 events ≥ 45, F1 drift/daily ≥ 15; F4 is closed, ≥ 300). Round alpha budget:
  0.03 (Tier A) + 0.02 (Tier B) = 0.05 one-sided familywise.
- Selection-history gate (pre-registered because these two came out of earlier searches):
  **A2 needs DSR(d) ≥ 0.95 with N_eff = 30; A4 needs DSR(d) ≥ 0.95 with N_eff = 9** (`sp.dsr`).

### 0.5 Robustness gates (all must hold for SIGNIFICANT; `sp.robust_report` + checks below)
1. d mean > 0 in 2010-17 AND in 2018-25H1 (U1).
2. Raw net mean > 0 in both halves in U2; raw net mean (U1) > 0 in 2018-25H1 AND in 2022+.
3. ≥ 60% of calendar years with raw net (U2) > 0 (event hypotheses A3, A4: 2-year blocks 2010-11 ... 2024-25H1).
4. Raw net (U1) > 0 with the 10 best sessions set to 0.
5. Winsorised raw net mean (U1, clip non-zero days at the 1st/99th percentile) > 0.
6. Matched-control rank p ≤ 0.05: `sp.mc_rank_p(real mean daily net, the 999 C1 strategy means)`.
7. Gross mean per trade in 2018-25H1 (U1) ≥ 1.5 × mean cost per trade.
8. Raw net mean > mean of plain drift AND > mean of hour drift at the same marks (beats "just be long then").
9. Markets: MNQ-primary hypotheses (A1, A2, A4): MES and MYM reported (no requirement). Basket hypotheses
   (A3, A5): U1 net > 0 in ≥ 2 of the 3 markets (MYM judged on 2018+).
- **Labels:** SIGNIFICANT = Holm + intersection + all gates → forward paper test, eligible for the eval
  portfolio. PROMISING = Newey-West t of d ≥ 2 and ≤ 2 failed gates (Holm not passed counts as one), or StepM-only → forward paper test only, never trade.
  NOT SIGNIFICANT otherwise. **Kill criterion (every hypothesis):** mean d ≤ 0, or U1 net ≤ 0 in 2018-25H1
  → dropped, no rescue by tuning.

### 0.6 No-look-ahead check (mandatory)
- Every signal is written as `fn(S, B) -> entries` using only `S` (sessions table) and `B` ({tf: bars}),
  and passed through `H.lookahead_check(fn, sym, n_cuts=20, seed=0)`. Current-session columns
  (high, low, rv, volume, ret_*, close_1600, last_px) are forbidden; use `prev_*` columns, mark prices at
  or before the decision mark, and bars that END at or before the decision time (bar start + tf ≤ decision).
- Custom walkers (A2, X-ideas with stops) additionally re-run their entry/exit on `H.truncate` data cut at
  the entry time for 20 random trades and must reproduce the same signal.

### 0.7 Standard outputs (so the synthesis step can combine without re-running)
For each hypothesis or secondary column `<hid>` (ids below):
- `v3/out/daily/<hid>.csv`: session, net_U1, net_U2, gross_U1, ctrl_C1, d, n_trades, and per-market net_U1
  columns (net_ES, net_NQ, net_YM) — full calendar, zeros on no-trade sessions.
- `v3/out/trades/<hid>.parquet`: the trade table from `time_trades` (or the custom walker, same columns).
- `v3/out/results/<hid>.json`: p_d, p_net, NW t of d and net, mean d/net by window, by year, halves, w/o 10
  best, winsorised, mc_rank_p, gross/cost, drift and hour-drift comparisons, DSR where required, label.
- Every column (primary, secondary, neighbour, exploratory) is logged once with
  `H.log("<hid>", scope, model, trades=..., baseline=C1 trades, params=..., note="prereg sha256 <hash>")`
  → `out/trials.csv` module `v3-<hid>`.
- Report in plain words: $ per micro after costs, MES first, then MNQ, MYM.

### 0.8 Eval relevance (reported, never used as significance)
For each Tier A hypothesis: `H.eval(trades, sizing=[("fixed",1),("fixed",3),("fixed",5)])` and the same eval on
200 C1 realisations (zero-timing-edge twin: same side, hours and sizes) → pass within 10 / 20 days and
eventual pass rate, rank p vs the twin. A difference counts only if rank p ≤ 0.05 and > 3 points per 10%.
Also report the eval-math target check (v3/out/evalmath_summary.txt): daily Sharpe of the stream (mean/sd of
daily net, target ≥ 0.15 for a clear fast-pass gain), share of sessions with ≥ 1 trade (target ≥ 80%), win rate
(target ≥ 45%), net $ per micro per trade vs the +0.10R guide (MNQ ≈ $10, MES ≈ $6 for hour-scale trades), and
the share of profit left without the 10 best days.

---------------------------------------------------------------------------------------------------

## 1. Confirmatory hypotheses (Tier A; one primary test each)

### A1 — Noise-band intraday momentum, MNQ (family F3) — group G1
- Source: Zarattini, Aziz & Barbon "Beat the Market" (2024/25); local `lit_p1_noiseband.py` variant A.
- Reason: intraday moves beyond the normal daily noise continue (dealer short-gamma hedging, leveraged-ETF
  rebalancing). Expected sign +; planning size $5-8 per MNQ trade (local re-cut +$7.66, day t 3.73).
- Market: **MNQ (pre-specified)**. MES and MYM run as secondaries.
- Rules (frozen; 5-minute v3 bars; unadjusted same-contract prices):
  - O_d = `rth_open` (09:30 mark). C_{d-1} = `prev_close_1600`; if that is missing because the prior session
    closed early, use `prev_last_px` (its last price, as the reference's 12:59 close). Sessions where both are
    missing (first session after a roll) or with fewer than 14 earlier full RTH sessions are skipped.
  - Early-close sessions = sessions whose exchange schedule ends before 16:00 (identified once from `last_t`
    < 1320 OUTSIDE the signal function and passed in as a fixed calendar list, because the exchange holiday
    schedule is known in advance; never used as a price signal).
  - Decision times t = 10:00, 10:30, ..., 15:30 (12 times). Decision price C_d(t) = close of the 5-minute bar
    ending at t (bar start t − 5 min). Fill = the mark price at t (`px_HHMM`), as in the reference (decide on the
    bar close, fill at the next open).
  - move(t, d) = |C_d(t)/O_d − 1|; sigma(t) = mean of move(t, ·) over the previous 14 FULL RTH sessions
    (early-close sessions excluded from the average).
  - UB(t) = max(O_d, C_{d-1})·(1 + sigma(t)); LB(t) = min(O_d, C_{d-1})·(1 − sigma(t)).
  - VWAP(t) = RTH VWAP from the 09:30 bar to t: Σ((H+L+C)/3 · V) / Σ V over 5-minute bars ending ≤ t.
  - At each decision time, in order: flat → long if C > UB, short if C < LB. Long → short (reverse) if C < LB,
    else flat if C < max(UB, VWAP). Short → long (reverse) if C > UB, else flat if C > min(LB, VWAP).
    No re-entry at the same decision time after an exit to flat. One position at a time, 1 micro, no stop.
  - Exit at the 16:00 mark (15:59 bar close). Early-close sessions: no entries after 12:30, exit 13:00 mark.
  - Each entry→exit span is one trade for `H.time_trades` (entry and exit at marks; no stop).
- Primary test: p_d (d vs C1) for MNQ, in the Holm family.

### A2 — Overnight-range break with the 20-day trend, MNQ (F3) — group G2
- Source: archive `setup_rule.overnight_break` / `chosen_models.py` model 1 (MNQ +$11.26/trade, t 3.28 pre-holdout;
  selected from a large earlier scan → DSR gate N_eff = 30).
- Reason: the first break of the overnight range in the direction of the daily trend starts an intraday trend
  (same momentum mechanism as A1). Expected sign +; planning $6-10 per MNQ trade.
- Market: **MNQ (pre-specified)**. MES and MYM as secondaries.
- Rules (frozen, 5-minute version of the 1-minute original):
  - on_high/on_low = `on_high`/`on_low` of the session (18:00-09:29, known at 09:30).
  - Trend: index I chained from within-contract daily returns (ret_cc; ret_oc on sessions where ret_cc is
    missing; 0 if both missing), EMA20 = exponential mean (span 20, adjust=False) of I through session d−1.
    At a decision, trend = sign(I_{d−1} · P/C_{d−1} − EMA20_{d−1}), P = the signal bar's close, C_{d−1} as in
    A1 (prev_close_1600, else prev_last_px after an early close); no trade on roll sessions (both missing).
  - Long: the FIRST 5-minute bar of the session (bars starting 09:30 or later) whose close > on_high, if that
    bar ends between 09:35 and 15:00 inclusive and trend > 0; enter at the next 5-minute bar open.
    Short: mirror with the first close < on_low and trend < 0. Each side at most once per session; one
    position at a time (a signal that arrives while in a position is ignored).
  - FOMC blackout (as the original): no entry whose signal bar ends from 30 min before to 15 min after the
    scheduled statement time (`../../data/fomc_dates.csv`, scheduled only).
  - Stop = 2 × ATR14 of 5-minute bars at the signal bar (`atr14`), from the entry fill; walked on 5-minute bars
    with the harness convention (stop checked from the entry bar's high/low; fill at the stop or the bar open if
    it opened through it; +1 extra tick). No target. Exit at the 16:45 mark (16:44 close) if not stopped.
  - The walker must match `H.time_trades` exactly on entries placed at 15-minute marks (consistency test, 50 trades).
- Primary test: p_d (vs C1 built with the walker) for MNQ, in the Holm family; plus DSR(N_eff 30) gate.

### A3 — Monthly options-expiry Friday short (third-Friday price spike reversal), basket (F2) — group G3
- Source: Baltussen, Terstegge & Whelan "The Derivative Payoff Bias" (2024); local expiry_fade.
- Reason: option-hedging flows push index futures up into the 09:30 settlement print, then the move reverts
  during the day. Expected sign +; planning size ≈ half published (≈ 12 bp ≈ $25-35 per micro at today's prices).
- Market: **basket = 1 MES + 1 MNQ + 1 MYM** (MYM from 2018), summed per session.
- Rules: sessions with `opex == 1` (third Friday or the prior trading day if that Friday is a holiday).
  Short at the 09:30 mark, cover at the 16:00 mark (15:59 close). No stop. One trade per market per event.
- Primary test: p_d (basket d vs basket C1), Holm family. Reported C3: the same short on non-expiry Fridays.

### A4 — 08:30 CPI / jobs-report fade, MNQ (F2) — group G4
- Source: archive section 13 (CPI best of 30 event tests in sample; NFP pre-registered and passed) →
  DSR gate N_eff = 9.
- Reason: the first algorithmic reaction to a headline number overshoots and partly reverses within the hour.
  Expected sign +; planning $10 per MNQ trade (pre-holdout +$13.31, t 2.93).
- Market: **MNQ (pre-specified)**. MES, MYM as secondaries.
- Rules: sessions with `nfp == 1` or `cpi == 1` (one trade if both). m = px_0845 − px_0830. If m > 0 short,
  if m < 0 long, m = 0 no trade. Enter at the 08:45 mark, exit at the 09:45 mark, no stop. Skip roll
  sessions and sessions where age_0830, age_0845 or age_0945 > 5 minutes (stale prices).
- Primary test: p_d (vs C1), Holm family; plus DSR(N_eff 9) gate. Reported C3: the same fade on all
  non-release sessions.

### A5 — Daily index reversal (negative day-to-day autocorrelation), basket (F1) — group G5
- Source: Baltussen, van Bekkum & Da (JFE 2019): index futures/ETF daily returns negatively autocorrelated
  since 1999; S&P strategy Sharpe ≈ 0.67 gross to 2016.
- Reason: index arbitrage/ETF flows and liquidity provision make yesterday's index move partly revert.
  Expected sign +; planning size half published (≈ 2 bp/day gross; LOW POWER: expected t ≈ 1-2;
  included because it is the main untested peer-reviewed daily effect and would be an every-day stream).
- Market: **basket = 1 MES + 1 MNQ + 1 MYM**, each on its own signal.
- Rules: at the 18:00 mark of every session, S = 4·r1 + 3·r2 + 2·r3 + 1·r4 with r_k = `ret_cc` of the k-th
  previous session of the same market (r1 = prev_ret_cc; missing → 0). Side = −sign(S) (S = 0 → no trade).
  Enter at the 18:00 mark, exit at the 16:45 mark, no stop. Sessions without an 18:00 price (roll sessions,
  late opens) are skipped.
- Primary test: p_d (basket d vs basket C1), Holm family. Long and short legs reported separately.

### P0 — Pre-specified equal-risk portfolio of A1-A5 (all five, survivors or not) — synthesis step
- Reason: weak, mostly uncorrelated streams combine (Sharpe adds as √K when correlations are low); the
  component list and weights are fixed now, so there is no selection.
- Weights: w_k = 1 / sd_k, sd_k = standard deviation of component k's raw daily net (U1, zeros included) over
  sessions 2010-06-07..2017-12-31; normalised to Σ w = 1. P0_d = Σ w_k d_k; P0_net = Σ w_k net_k.
- Primary test: p_d of P0 (one series; correlations handled by the common bootstrap), in the Holm family.
  Gates 1-8 apply (gate 9 not applicable). Also `sp.portfolio_test` reported.


## 1b. Why these five (selection logic, written before testing)
- Power check first (methods): a rule is Tier A only if its planning effect (local estimate shrunk 25% for
  internal results, half the published size for literature-only effects) gives an expected t ≥ 2 on
  2010-2025H1 — A1 (≈2.8), A2 (≈2.5), A3 (≈2.0), A4 (≈2.2). A5 fails this (≈1-2) but is kept as the one
  untested peer-reviewed every-day stream; FOMC reversal, announcement-day premium, turn-of-month and
  overnight buy-the-dip fail it and are Tier B secondaries (≈1.0 each).
- Eval-math fit (v3/out/evalmath_summary.txt): fast passes need an every-day stream with daily Sharpe ≥ 0.15
  or ≥ +0.10R per trade; event rules (≈12-24 trades/yr) cannot pass alone and only help as layers. So the
  family holds three daily streams (A1 ≈ 0.9 trades/day, A2 ≈ 0.4/day, A5 1/day per market) and two event
  layers (A3, A4); P0 tests the pre-fixed combination, because uncorrelated weak streams add up (√K).
- Economic mechanism + published or earlier pre-registered evidence for each; ideas that already failed
  locally or decayed after publication are excluded (section 6).
- MES first-class: MES is inside both basket hypotheses (A3, A5) and is the first secondary of every
  MNQ-primary group. The MNQ primaries are pre-specified because every earlier positive result was NQ-only;
  choosing MES there would test a rule on the market where it is already known to be weak.

---------------------------------------------------------------------------------------------------

## 2. Pre-registered secondaries (Tier B, NOT in the confirmatory family) and robustness neighbours

Neighbours (marked N) are stability checks, not tests: reported as "same sign as the primary: yes/no".
Secondaries (marked S) are logged trials judged at the Tier B bar.

**G1 (A1 noise band):** S1.1 MES; S1.2 MYM; S1.3 3-market basket; S1.4 MNQ only when the trailing 20-session
RTH realised vol (mean of prev_rv_rth over the 20 previous sessions) is in the middle or top tercile of its
expanding history; S1.5 MNQ skipping sessions after an ES daily drop ≤ −2% (ES prev_ret_cc ≤ −0.02);
S1.6 MNQ exit at 16:45 instead of 16:00. Long and short legs reported (decomposition, not trials).
N: lookback 10 and 20; decisions only on the hour (10:00 ... 15:00); +1 extra tick cost.

**G2 (A2 overnight break):** S2.1 MES; S2.2 MYM; S2.3 MNQ with the ES-drop skip (R1, as S1.5); S2.4 MNQ
skipping monthly-expiry Fridays; S2.5 5-minute opening-range breakout MNQ (direction of the 09:30-09:34 bar,
enter 09:35 open, stop at the bar's other end, exit 16:00); S2.6 the same on MES.
N: stop 1.5× and 3× ATR; break bar ending up to 15:30; trend = sign of the 5-session return; exit 16:00.

**G3 (A3 expiry short):** S3.1 cover at 12:00 (paper: reversion done by noon); S3.2 leg 1 = long 18:00 → 09:30
of the expiry session (overnight run-up into the settlement print); S3.3 the paper's round trip (S3.2 + A3);
S3.4 monthly non-quarterly only / S3.5 quarterly only (split of A3, reported); S3.6 quarterly-expiry last-hour
short 15:00 → 16:00, MES first, then MNQ, MYM; S3.7 turn-of-month overnight leg: long 18:00 → 09:30 on the
session that closes on the first trading day of each month (basket).
N: A3 entry at 09:45; cover at 15:00; MES alone, MNQ alone, MYM alone (reported per market anyway).

**G4 (A4 release fade):** S4.1 NFP only; S4.2 CPI only; S4.3 big-move days only (|m| in bp above the median of
all EARLIER events, expanding); S4.4 MES; S4.5 MYM; S4.6 disaster stop at 2·|m| from entry; S4.7 archive NFP
rule: at 09:30 trade against the 08:30 → 09:30 move, exit 16:00 (MNQ); S4.8 FOMC announcement reversal
(Baglioni & Ribeiro 2022, adapted to marks): on scheduled FOMC days, entry mark = statement time − 15 min
(13:45 for 14:00, 14:00 for 14:15, 12:15 for 12:30), signal = price at that mark / price at the same mark of
the previous session − 1, side = −sign(signal), exit 16:00, +1 extra tick on the exit, basket;
S4.9 announcement-day premium (Savor-Wilson): long 18:00 → 16:45 on FOMC, NFP and CPI sessions, MES first,
then MNQ, MYM (low power, ≈ 470 events).
N: A4 exit 09:30 and 10:00; entry 09:00 (signal 08:30-09:00).

**G5 (A5 daily reversal):** S5.1 prior day only, side = −sign(r1); S5.2 only when |r1| > 1 × sd of the 20
previous ret_cc; S5.3 Connors RSI(2) long-only: RSI(2) of daily 16:00 closes (chained index as in A2) < 10 and
index > its 200-session simple mean at the prior close → long 18:00 → 16:45, repeat each session until RSI(2)
> 70 at a prior close; S5.4 mirror short (RSI(2) > 90 and index < 200-session mean, until RSI(2) < 30);
S5.5 overnight buy-the-dip (Boyarchenko-Larsen-Whelan): long 02:00 → 03:00 only when the PREVIOUS session's
15:15 → 16:00 return (its px_1600/px_1515 − 1) < 0; S5.6 same condition, long 02:00 → 09:30. All per market,
MES first. Reported benchmark (not a trial): long 18:00 → 09:30 every session.
N for A5: lags weighted 5,4,3,2,1 (5 lags); equal weights 1,1,1,1; overnight part only (exit 09:30);
day part only (entry 09:30, exit 16:00).

---------------------------------------------------------------------------------------------------

## 3. Exploratory group (G6) — deductive ideas, clearly EXPLORATORY, not in the confirmatory family

These are new, logic-based ideas aimed at the eval target (many trades, high win rate, MES-friendly). They
are Tier B at best: nothing here can be called proven this round; a column that clears StepM 0.004 + t ≥ 3 +
DSR becomes a candidate for the NEXT round's pre-registration and forward test. All per market (MES first,
MNQ, MYM), 1 micro, C1 controls as in 0.3 (R = 200 is enough here), no-look-ahead check mandatory.

- **X1 Post-sell-off rebound** (liquidity provision after forced selling; internal evidence that breakouts lose
  on these days). Condition: ES prev_ret_cc ≤ −0.02 (known at 18:00). X1a: long 09:30 → 16:00. X1b: at 10:00
  take the side opposite to the 09:30 → 10:00 move (px_1000 vs px_0930), exit 16:00.
- **X2 Opening-gap fade bracket** (overnight inventory unwinds at the cash open; built for a high win rate).
  gap = px_0930 / prev_close_1600 − 1. If 0.15% < |gap| < 0.50%: enter at 09:30 against the gap, target =
  prev_close_1600 (gap filled), stop = |gap| in points beyond the entry, time exit 11:00. (`time_trades` with
  stop_pts and target_pts; stop-and-target-same-bar → stop first.)
- **X3 Asian-range break at the European open** (European participants trade on news since the US close).
  Range = high/low of the 15-minute bars 18:00-01:45. From 02:00 to 04:45, the first 15-minute bar close beyond
  the range → enter at the next mark in the break direction, stop at the range midpoint, exit at the 09:30 mark.
- **X4 Same-slot persistence, index level** (Heston-Korajczyk-Sadka; low prior). For each 30-minute slot of
  the RTH day (09:30 ... 15:30), signal = mean slot return over the previous 20 completed sessions; trade only
  the ONE slot per session with the largest |signal| / (its 20-session sd), in the signal's direction,
  entry/exit at the slot's marks.
- **X5 Calm-regime midday fade** (dealers long gamma in calm markets pin prices). Only when prev_rv_rth is in the
  lowest tercile of its trailing 250-session distribution: at 12:00, side = −sign(px_1200 − px_0930) if
  |px_1200/px_0930 − 1| > 0.5 × the mean |09:30→12:00 move| of the previous 20 sessions; exit 15:30.

---------------------------------------------------------------------------------------------------

## 4. Groups (exactly 6; one experimenter each, ~55 minutes, shared harness)

| Group | Experiment dir | Contents | In the confirmatory family | Rough runtime |
|---|---|---|---|---|
| G1 Noise-band momentum (F3) | `v3/exp_g1_noiseband/` | A1 + S1.1-S1.6 + neighbours + eval | A1 | ~55 min (20 code, 15 runs incl. 999 C1 reps, 20 report) |
| G2 Overnight-range break (F3) | `v3/exp_g2_onbreak/` | A2 (custom 5-min walker + consistency test) + S2.1-S2.6 + neighbours | A2 | ~55 min (walker is the long pole) |
| G3 Expiry-day flows (F2) | `v3/exp_g3_expiry/` | A3 + S3.1-S3.7 + neighbours + C3 | A3 | ~40 min |
| G4 Macro releases & FOMC (F2) | `v3/exp_g4_releases/` | A4 + S4.1-S4.9 + neighbours + C3 | A4 | ~50 min |
| G5 Daily reversal & overnight (F1) | `v3/exp_g5_reversal/` | A5 + S5.1-S5.6 + neighbours + benchmark | A5 | ~45 min |
| G6 EXPLORATORY deductive (F1/F2/F3, Tier B) | `v3/exp_g6_explore/` | X1-X5 | none | ~55 min |

All light (v3/data only, ≤ 3 threads, no flock needed); if anything needs > 2 GB or 1-minute data it must use
the shared flock. Each group writes the standard outputs (0.7) and logs every column.

## 5. Synthesis step (after the groups; ~15 min; fixed now)
1. Collect p_d of A1-A5, build P0 from `v3/out/daily/A*.csv` with the 2010-17 weights, compute its p_d.
2. Holm at 0.03 over {A1..A5, P0}; StepM and SPA_c on the 6-column d matrix (mean block 10, B = 5000).
3. Apply the intersection rule and gates; label each SIGNIFICANT / PROMISING / NOT SIGNIFICANT.
4. Tier B: per family, StepM over all its secondary + exploratory columns at 0.004, t ≥ 3, DSR.
5. **Eval portfolio P1 (fixed rule):** components = all Tier A hypotheses labelled SIGNIFICANT (if none, the
   PROMISING ones, explicitly labelled "not proven"). Each trade gets a virtual risk_usd = the sd of that
   component's per-micro net $ over its previous 100 trades (known before entry; first 100 trades skipped).
   Sizing `("risk", 150)`, `("risk", 250)` and `("risk", 400)` in `H.eval` (cap 20 micros, $600 daily limit, 40% and 50% rules),
   compared with the same sizing on 200 C1 realisations of the same components (zero-timing-edge twin).
   Report pass within 10 / 20 days, eventual pass rate, bust rate, rank p vs the twin. Eval results are
   descriptive; they never upgrade a label.
6. Forward test plan for SIGNIFICANT / PROMISING rules: paper log from 2026-11-10, O'Brien-Fleming looks at
   z = 4.05, 2.86, 2.34, 2.02 (one-sided 2.5%), frozen rules as above.

## 6. What is deliberately NOT tested (reasons in the research inputs)
Candle patterns, EMA pullbacks, BOS/CHoCH, H1/H2, learned confidence models (family F4 closed); last-half-hour
momentum; midday fade (unconditional); NQ-ES spread fade; month-end 60/40 rebalancing fade; pre-FOMC drift;
opex-week and pre-holiday effects; weekend/Monday effects; Lou-Polk-Skouras quarterly timing. Volatility-managed
sizing is treated only as an eval tool (it changes variance, not the mean).
