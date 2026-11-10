# v3 research report: is there a statistically significant edge?

Run of 2026-11-09 (12:06-14:55 MST). Data: 1-minute futures bars turned into v3 session files, sessions 2010-06-07 .. 2025-06-27 (3,876 sessions; MYM from 2018). The locked holdout (2025-06-30 18:00 ET onward) was never loaded. All money figures are **net $ per 1 micro after costs** ($1 commission + 1 tick each way, +1 tick on stop fills), unless a line says "per day".

## The answer

1. **Yes, by the standard we fixed before testing, there is a statistically significant edge.** Five rules and one fixed mix of them were frozen at 12:35 (PREREG.md, sha256 c9aef662...2460). After the multiple-testing correction (Holm), three rules and the fixed mix pass every pre-registered test:
   - **A1**: noise-band intraday momentum on MNQ.
   - **A3**: short on options-expiry Fridays, MES + MNQ + MYM.
   - **A4**: fading the 08:30 CPI/jobs-report move on MNQ.
   - **P0**: the pre-fixed mix of all five rules.

   A2 (overnight-range break) is PROMISING. It fails the extra check for having been picked from an earlier search (deflated Sharpe 0.814, needs 0.95), so it is not proven. A5 (daily reversal) has no edge.
2. **How strong.** The three survivors combined (P1, 1 micro per trade) make **+$10.20 per trade, about $10.75 per day** (t 4.7, bootstrap p 0.0002, annual Sharpe 1.16). They beat matched random-day copies of the same trades by $13.24 per day (p 0.0002). **All of it comes from 2018 on:**
   - 2010-17: +$0.24 per day (t 0.28).
   - 2018-25H1: +$21.30 per day (t 4.9).
   - 2022+: +$27.00 per day.
3. **Which markets.**
   - **MNQ** carries almost everything.
   - **MES** has a real edge only in A3 (+$16.26 per trade, about 12 days a year). The A1, A2 and A4 rules pick better-than-random moments on MES too, but the edge does not survive MES's $3.50 round-trip cost: +$1.53, +$0.59 and +$0.69 per trade.
   - **MYM**: nothing usable.
4. **How fast it could pass the Lucid eval: it does not pass fast.**
   - Passing within 10 trading days never reaches the luck bar.
     - 40% consistency rule: best 3.5% (3.8% from 2022) against a luck bar of 10.8%.
     - 50% rule: best 8.6% (11.9% from 2022) against a luck bar of 20.4%.
   - Its strength is the *eventual* pass rate and fewer busts. At about $150 of virtual risk per trade (about 3 micros), for start days from 2018 on under the 40% rule:
     - It passes 79.5% of start days, against 21% for the zero-edge copies.
     - It busts 7.7% of the time, against 69%.
     - The median pass takes 114 trading days.
   - Fast passes still come only from size and variance, and size raises the bust rate. That gets worse when the $600 daily limit is enforced intraday, as a real account would do (section 7).
5. **Next step: paper-trade P1 (A1 + A3 + A4) forward from 2026-11-10.** Use the pre-set O'Brien-Fleming stopping bounds (z 4.05 / 2.86 / 2.34 / 2.02).
   - The one-shot holdout check `final_exam.py` is ready and **not run**. It needs your approval.
   - It is worth running as a sanity check, but it cannot confirm the edge. Over about 340 holdout sessions the expected t is only about 1.9, and earlier archive runs already looked at those months for these rules.

## 1. How the tests worked

- **Primary statistic.** For each session, take net P&L minus the matched control C1. C1 is the same trade, same side and same clock times, placed on 999 random sessions of the same year. That removes plain drift and most of the cost. Significance comes from a stationary bootstrap over days, using the worst p over block lengths 1/5/10/20.
- **Confirmatory family** (A1-A5 + P0, K = 6): Holm at alpha 0.03. A claim also needs:
  - raw net p <= 0.05;
  - all robustness gates: both halves, years, without the 10 best days, winsorised, matched-control rank, gross >= 1.5x cost, beats plain and hour drift;
  - for A2 and A4, a deflated-Sharpe check, because they came out of earlier searches.
- **Everything else** (50 secondary columns, 24 pre-registered exploratory columns, 18 post-hoc extras) had to clear a much stricter bar inside its idea family: Romano-Wolf StepM <= 0.004, t >= 3 and deflated Sharpe >= 0.95.
- **No look-ahead.** Truncation tests passed in every group. Hand checks against raw 1-minute bars matched in every group. Independent skeptic re-implementations rebuilt A1, A2, A3 and A4 trade-for-trade.

## 2. Confirmatory results (Tier A)

"p before" = bootstrap p of the timing edge d (net minus C1); "p after" = Holm-adjusted. Halves and 2022+ are $ per trade (historical prices); "w/o top 10" = $ per trade with the 10 best days removed.

| id | rule in plain words | $/trade | trades/yr | p before -> after | raw net p | 2010-17 / 2018-25H1 | 2022+ | w/o top 10 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| A1 | MNQ: every half hour 10:00-15:30, go with a move that breaks the day's "noise band" (open +/- average move of the last 14 days); exit when price drops back below the band or VWAP, reverse if it breaks the other band; flat at 16:00 | **+7.75** | 213 | 0.0002 -> **0.0012** | 0.0006 | -0.20 / +15.70 | +21.81 | +4.77 | **SIGNIFICANT** |
| A2 | MNQ: first 5-min close outside the overnight range in the direction of the 20-day trend, stop 2x ATR, exit 16:45 | +8.50 | 153 | 0.0070 -> 0.021 | 0.0054 | -0.39 / +17.75 | +22.57 | +4.52 | PROMISING (fails the pre-set deflated-Sharpe check: 0.814 < 0.95) |
| A3 | Options-expiry Friday (3rd Friday): short 1 MES + 1 MNQ + 1 MYM at 09:30, cover 16:00 | **+26.34** | 29 (about 12 days) | 0.0108 -> **0.0216** | 0.024 | +4.64 / +40.98 | +30.42 | +1.82 | **SIGNIFICANT** (fragile) |
| A4 | CPI / jobs-report days, MNQ: at 08:45 take the side opposite to the 08:30-08:45 move, exit 09:45 | **+12.24** | 23 | 0.0012 -> **0.0048** | 0.0064 | -0.22 / +24.70 | +42.44 | +3.86 | **SIGNIFICANT** |
| A5 | Every session, MES/MNQ/MYM: side opposite to the weighted last 4 daily moves, hold 18:00-16:45 | -0.61 | 617 | 0.071 -> 0.071 | 0.585 | -1.99 / +0.30 | +2.35 | -4.36 | NOT SIGNIFICANT (7 of 9 gates fail) |
| P0 | Pre-fixed mix of A1-A5, weights 1/sd(2010-17): A4 0.54, A3 0.17, A2 0.14, A1 0.13, A5 0.03 | +$2.62 per day | - | 0.0002 -> **0.0012** | 0.0004 | -$0.10 / +$5.36 per day | +$7.35 per day | +$1.80 per day | **SIGNIFICANT** |

- **Holm step by step.** A1 0.0002 <= 0.005, P0 0.0002 <= 0.006, A4 0.0012 <= 0.0075, A2 0.0070 <= 0.010, A3 0.0108 <= 0.015, A5 0.0708 > 0.03.
- **Robustness of that decision.** The decision holds for 8 of 8 bootstrap seeds: A2's p ranges 0.0048-0.0070 and A3's 0.0078-0.0108.
- **Other family tests.** Romano-Wolf StepM on the same 6 columns rejects the same five, with no StepM-only case. Hansen SPA_c p is 0.0002.
- **Timing edge in $ per trade** (net minus the random-day copy): A1 +$9.72, A2 +$7.67, A3 +$31.46, A4 +$14.72, A5 +$4.68.
- **Against "just be long at those hours":**
  - A1: plain drift -$0.38, hour drift -$1.61.
  - A3: plain drift -$31.55 (long at the same times), hour drift -$0.63.
  - A4: plain drift +$2.34, hour drift -$1.74.
  - All three beat both.
- **Correlation.** The survivors are nearly independent day to day: daily net correlation A1-A3 0.05, A1-A4 -0.01, A3-A4 0.00. A1-A2 is 0.38.

## 3. Per market, MES first ($ per micro per trade, full window)

| rule | MES | MNQ | MYM (2018+) | comment |
|---|---|---|---|---|
| A1 noise band | +1.53 (timing edge t 4.95, but raw net p 0.088; about $0 without the 10 best days; -$0.97 with +1 tick) | **+7.75** | -0.17 (killed) | MES loses to its $3.50 cost |
| A2 overnight break | +0.59 (net t 0.40) | +8.50 | +0.42 | NQ only |
| A3 expiry short | **+16.26** (2010-17 +2.38, 2018-25H1 +30.29, 2022+ +18.38) | +44.74 | +9.63 (2022+ -11.13) | positive in 3 of 3 markets |
| A4 release fade | +0.69 (net p 0.39) | +12.24 | -5.26 (killed) | NQ only |
| A5 daily reversal | -0.43 | +1.12 | -4.43 | no edge |

## 4. Secondary and exploratory columns (Tier B), corrected across each whole family

StepM was re-run across all of a family's secondary and exploratory columns, including post-hoc extras; neighbours were left out because they are stability checks. Deflated Sharpe used N_eff = family floor + Li-Ji effective count:

| family | columns | N_eff | t needed |
|---|---|---|---|
| F3 momentum | 32 | 65 | about 4.0 |
| F2 events | 38 | 68 | about 4.0 |
| F1 daily | 22 | 32 | about 3.7 |

| column | what it is | $/trade | t (timing edge) | StepM p | deflated Sharpe | label |
|---|---|---|---|---|---|---|
| S1.5 | A1, skip days after an ES drop of 2% or more | +8.28 | 6.45 | 0.0002 | 1.00 | passes Tier B (A1 variant) |
| S1.6 | A1, exit 16:45 | +7.99 | 5.05 | 0.0002 | 0.997 | passes Tier B (about A1) |
| S1.3 | A1 rule on MES + MNQ + MYM | +3.61 | 4.99 | 0.0002 | 0.994 | passes on d; raw net t only 2.91 (diluted A1) |
| S1.4 | A1 only in mid/high-volatility regimes | +12.18 | 4.81 | 0.0006 | 0.992 | passes Tier B (A1 subset) |
| S1.1 | A1 rule on MES | +1.53 | 4.95 | 0.0002 | 0.988 | timing edge passes; **not tradeable** (net p 0.088) |
| S2.3 / S2.4 | A2 with ES-drop skip / without expiry Fridays | +9.90 / +8.46 | 3.41 / 3.09 | 0.014 / 0.025 | 0.88 / 0.73 | PROMISING |
| S4.3 | A4 on big first moves only | +21.80 | 3.16 | 0.035 | 0.85 | PROMISING |
| E4.1 | A4 signal read on the 08:44 close (execution check) | +12.55 | 3.29 | 0.025 | 0.83 | PROMISING (A4 is not a same-price artifact) |
| all others (83) | see out/synthesis/tierB.csv | | <= 2.81 | >= 0.075 | <= 0.68 | 46 not significant, 37 killed |

The Tier B passes are all versions of A1 that share most of its trades, so they are **one finding, not five**.

## 5. What failed (killed or no edge after costs)

- **A5 daily index reversal**, and every reversal secondary (RSI(2), the 1-day reversal, big-move reversal). The short side loses in a rising market, and the whole stream does about $6.50 per trade worse than simply being long.
- **Overnight dip buying (2-3am).** About $0 after costs, and dead since 2021.
- **Expiry-day overnight run-up and turn-of-month overnight long.** After the Labor-Day fix: t 1.65.
- **FOMC reversal**, the announcement-day premium (that is just drift), and the CPI-only half of A4 (t 1.81).
- **5-minute opening-range breakout** on MNQ (+$2.62, t 1.2) and on MES (-$3.42).
- **Every G6 deductive idea:**
  - Asian-range break at the European open: -$5.21.
  - Same-slot repeat: -$3.74; slot returns actually reverse.
  - Calm-market midday fade: -$2.04.
  - Gap-fill bracket: -$1.74, despite a 50-60% win rate.
  - Post-sell-off rebound: +$48 per trade, but it is almost all 2020 and 9 April 2025, and -$7,248 without its 10 best days.
- **Every rule on MYM**, and every rule on MES except A3.

## 6. Portfolios

**P0** (the pre-fixed mix, in the Holm family): SIGNIFICANT.

| P0 measure | value |
|---|---|
| weighted net per day | +$2.62 (t 4.67) |
| timing edge per day | +$3.34 (t 5.99) |
| today's-price units per day, 2010-17 / 2018-25H1 | +$2.71 / +$9.79 |
| historical $ per day, 2010-17 | **-$0.10** |
| positive years in today's-price units | 15 of 16 |
| net per day without the 10 best days | +$1.80 |

Its weights are dominated by A4 (0.54), because A4 trades rarely and so has a small daily sd.

**P1** (the eval portfolio, fixed rule: the Tier A rules labelled SIGNIFICANT, so A1 + A3 + A4). Its components were chosen from the results, so the p-values below are descriptive. The confirmatory evidence is the Holm family above.

| P1 at 1 micro per trade (A3 = 1 per market) | value |
|---|---|
| trades | 4,086 (MES 181, MNQ 3,815, MYM 90); trades on 63% of sessions |
| net per trade / per day | **+$10.20 / +$10.75** (t 4.71, p 0.0002) |
| timing edge per day | +$13.24 (t 5.73, p 0.0002) |
| 2010-17 / 2018-25H1 / 2022+ per day | +$0.24 (t 0.28) / **+$21.30** (t 4.93) / +$27.00 (t 3.44) |
| today's-price units per day, 2010-17 / 2018-25H1 | +$11.66 / +$37.69 |
| without the 10 best days | +$6.48 per day (t 3.66); the 10 best days are 39.7% of profit; without the 20 best, t 2.61 |
| years positive | 13 of 16 (2010, 2013, 2016 negative); 2018-2025H1 every year positive |
| daily Sharpe | 0.073 overall, 0.104 since 2018 (eval-math target for fast passing: >= 0.15) |
| sized at $250 virtual risk (about 5.1 micros) | +$18.51 per day (t 4.22); 2010-17 +$2.65 (t 0.45), 2018-25H1 +$34.41 |

P1 net by calendar year at 1 micro ($ total):

| 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025H1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| -329 | +286 | +486 | -460 | +471 | +641 | -668 | +43 | +5,343 | +392 | +6,296 | +4,854 | +6,928 | +6,147 | +5,308 | +5,943 |

## 7. Eval odds (LucidFlex 25K, start on every trading day)

The real P1 is compared with 200 zero-timing-edge twins: the same trades and sizes, moved to random sessions of the same year. The luck bar is the best no-edge result from v2 (NQ). Start days are from 2018 on. Pass and bust rates are the % of start days. The "intraday" columns re-score the same streams with the $600 daily limit hit by the running 5-minute P&L, as a real account would, instead of the v2 judge's closing-P&L floor.

**40% consistency rule**

| sizing | pass (real vs twins) | within 10 days (real vs twins; luck 10.8) | within 20 days | bust (real vs twins) | median days to pass | intraday: pass / within 10 / bust |
|---|---|---|---|---|---|---|
| $150 virtual risk (about 3.4 micros) | **79.5 vs 21.2** (p 0.005) | 0.3 vs 0.1 | 3.4 vs 0.8 | **7.7 vs 69.5** | 114 | 77.4 / 0.3 / 9.8 |
| $250 risk (about 5.1 micros) | 55.6 vs 22.6 | 1.5 vs 0.7 (p 0.06) | 8.6 vs 3.4 | 35.9 vs 73.9 | 55 | 46.8 / 1.4 / 44.7 |
| $400 risk (about 8.2 micros) | 50.2 vs 25.6 | 2.0 vs 1.8 | 10.6 vs 6.8 | 42.7 vs 71.4 | 37 | n/a |
| 1 micro fixed | 73.2 vs 21.3 | 0.6 vs 0.3 | 5.3 vs 1.9 | 19.8 vs 75.7 | 73 | 70.9 / 0.6 / 22.2 |
| 3 micros fixed | 55.5 vs 26.9 | 3.5 vs 2.2 | 13.2 vs 7.4 | 40.0 vs 71.3 | 39 | **33.4 / 2.4 / 63.6** |

**50% consistency rule**

| sizing | pass (real vs twins) | within 10 days (real vs twins; luck 20.4) | within 20 days | bust | median days to pass |
|---|---|---|---|---|---|
| $150 risk | 79.7 vs 24.1 | 0.6 vs 0.3 | 5.2 vs 1.4 | 7.7 | 99 |
| $400 risk | 51.8 vs 30.1 | 5.7 vs 4.6 | 20.8 vs 12.8 | 42.0 | 25 |
| 3 micros | 57.5 vs 31.1 | **8.6 vs 5.5** (p 0.02) | 23.0 vs 13.8 | 39.4 | 26 |
| 3 micros, 2022+ starts | 48.1 vs 34.3 | 11.9 vs 7.7 (luck 19.4) | 28.0 vs 18.4 | 45.3 | 18 |

**Reading it:**
- **The edge is real for the eval, but it is a slow edge.** It roughly triples the eventual pass rate and cuts the bust rate by about 60 points at small size. It never makes a fast pass likely.
- **Zero-edge streams can do better on speed.** The eval-math study found that zero-edge random trades with day management (fixed $ risk, stop for the day once green) pass within 10 days 18-22% of the time under the 40% rule. P1's best is 3.5%.
- **Bigger size buys speed with busts, and the closing-P&L judge hides part of the cost.** At 3 micros fixed, 7.4% of traded days touch -$600 intraday, and 101 of those days closed above -$600. Enforcing the limit intraday cuts the pass rate from 58.6% to 33.4% and raises busts to 63.6% (v2-style closing judge vs intraday, same code). At $150 risk the intraday limit barely matters (77.4% pass, 9.8% bust).
- **As a target spec,** P1 trades on 63% of sessions (target 80%) with a daily Sharpe of 0.073 (target 0.15). Its win rate is mixed: A1 37%, A3 56%, A4 52%.

## 8. Honest caveats

- **Not a fresh discovery.** A1-A4 were measured on this data by earlier runs, and the archive runs of 2026-11-08 also looked at the post-2025-06-30 data for them. This round is a frozen re-test with stronger controls. Only forward paper trading can confirm it.
- **Regime dependence.**
  - In historical dollars, every survivor was flat in 2010-17: A1 -$0.20, A3 +$4.64, A4 -$0.22 per trade; P0 -$0.10 per day.
  - They pass the "both halves" gate only through the pre-registered today's-price unit and the timing-edge statistic.
  - Even in % terms A1's gross edge was about 3x smaller then (2.4 vs 7.3 basis points per trade).
  - A4 is a 2021-24 effect: without those years p is 0.14.
- **Concentration.**
  - P1's 10 best days are 40% of its profit. On 2025-04-09 (tariff-pause day) P1 netted +$3,024, 7.3% of its 15-year total; one A1 trade that day made +$3,628.50.
  - A3's 10 best of 181 expiry days are 93% of its profit, and only 52% of expiry days are positive.
  - A4's 10 best days are 68.5%.
- **Fragile pieces.**
  - A3 passes Holm only because A2 (p 0.0070) clears its 0.010 step. That held for 8 of 8 bootstrap seeds, but the margin is thin.
  - A4 passes its selection-history check (deflated Sharpe 0.971 at N_eff 9) but would fail at any N_eff above about 14.
  - A4's profit comes from 09:30-09:45: exiting at 09:30 gives about $0.
- **Execution.**
  - A1 assumes a fill at the open of the minute after the 5-minute decision bar. Filling 5 minutes late cuts it to +$5.50 per trade (MES to +$0.37).
  - A3 and A1 have no stop.
  - A1 and A3 can hold opposite MNQ positions on the same expiry Friday. The P&L adds up correctly, but a real account would net them.
- **Eval model.**
  - The v2 judge floors each day at -$600 on closing P&L. The re-score above shows this is optimistic at 3 or more micros.
  - The luck bar was computed with that same lenient judge, so comparing it with the intraday numbers is conservative for P1.
- **P1 p-values are descriptive.** P1's components were chosen from the results; the confirmatory test is the Holm family, where P0 and the three rules pass.
- **Bookkeeping choices by the groups (disclosed):**
  - G3 fixed a Labor-Day bug in S3.7, which moved it from PROMISING to not significant.
  - Some groups ran StepM only within their own group. This synthesis redid it across whole families, which only makes the bar stricter.
  - Tier B labels here count StepM, t and deflated Sharpe as three separate failures (stats_protocol.round_verdict). Counted as one failure, S3.1, S4.1, S4.6, N4.2 and N4.3 would also be PROMISING.

## 9. Recommended next step

1. **Forward paper test of P1 (A1 + A3 + A4, rules exactly as in PREREG.md section 1) from 2026-11-10.** Use the O'Brien-Fleming looks (z 4.05 / 2.86 / 2.34 / 2.02).
   - At the 2018+ daily Sharpe of about 0.10, reaching z 2.02 takes about 380 trading days on average, and about 760 for 80% power.
   - Plan on 1.5-3 years. An early stop needs a very large result.
   - Trade at $150 virtual risk per trade (or 1 MNQ / 1 MES per leg), not larger.
2. **Final exam on the locked holdout: optional sanity check, and only with your approval.**
   - **What it does.** v3/final_exam.py is prepared and not run. It rebuilds the data including 2025-06-30 onward into v3/data_exam/, regenerates A1, A3 and A4 with the same code, and first checks that the rebuilt in-sample trades equal the saved ones.
   - **Frozen rule.** PASSED if P1's timing edge has p <= 0.05 and net > 0. NOT CONFIRMED if net > 0 without significance. FAILED if net <= 0. The spec is in out/prereg/v3round1_FINAL_EXAM.json, together with the script's sha256.
   - **Dress rehearsal.** A self-test on in-sample data (2024-07-01..2025-06-27, the strongest year) reproduced all 3,278 + 452 + 356 trades exactly. On that year, P1's timing edge came out at p 0.048, so even a great year only just passes.
   - **Is it warranted?** Yes, but only as a cheap tripwire. A FAILED result would be a real warning, while NOT CONFIRMED is the likely outcome even if the edge is real (expected t about 1.9). It cannot replace the forward test, because these months were already viewed for these rules.
   - To run it after approving, from research/confidence: V3_FINAL_EXAM_APPROVED=YES_SPEND_THE_HOLDOUT python3 v3/final_exam.py --run --approved-by "<name, date>", with the usual PYTHONPATH. It takes the heavy lock itself.
3. **Do not chase speed with these rules.** If fast passes are the goal, pre-register a test of P1 inside the eval-math day rules (fixed $ risk, stop for the day once green, 2-3 trades a day) against zero-edge twins that use the same day rules. That is the only way the edge could add to the 18-22% that day management gives on its own.
4. **Treat as dead and do not retest:**
   - A5 daily reversal and all RSI(2)/reversal variants;
   - overnight dip buying;
   - FOMC reversal and the announcement-day premium;
   - expiry overnight run-up and turn-of-month;
   - the opening-range breakout;
   - X2-X5;
   - every MYM rule, and every MES version except A3.

## 10. Files

- Synthesis code:
  - v3/exp_synth/synth_stats.py: Holm, StepM, SPA, P0, labels, Tier B.
  - v3/exp_synth/synth_p1.py: P1 stats and eval against 200 twins.
  - v3/exp_synth/synth_dll.py: intraday $600 re-score.
- Results in v3/out/synthesis/:
  - tierA.csv, tierB.csv, synth_stats.json;
  - P1_stats.json, P1_eval_vs_twins.csv, P1_eval_intraday_dll_EXPLORATORY.csv;
  - holm_seed_sensitivity.json.
- P0 standard outputs: v3/out/daily/P0.csv, v3/out/results/P0.json.
- Final exam:
  - v3/final_exam.py (not run);
  - frozen spec v3/out/prereg/v3round1_FINAL_EXAM.json;
  - self-test output in v3/out/final_exam/selftest/ (in-sample only).
- Trials logged in out/trials.csv: v3-P0, v3-P1, v3-P1-risk250, v3-SYNTH-tierB, v3-P1-evalrealism.
- Per-group details: the G1-G6 experiment folders and v3/out/results/<id>.json.
