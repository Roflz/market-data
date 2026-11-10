# Morning report: can the pullback process be automated to pass the Lucid eval fast?

All money is **net $ per micro contract per trade, after costs** ($1 commission + 1 tick slippage each way + 1 extra tick when a stop fills), unless a row says otherwise.
"Out of sample" means the model never saw that year while it was being trained.
The locked July 2025+ data was **not touched**. Everything below covers 2010 (MYM: 2018) to 2025-06-30.

---

## 1. The answer in 5 lines

1. **No setup clearly beats luck once costs are paid.** Your pullback rules as a group earn about $0 to +$1.6 per trade *before* costs. Costs are $2 (MNQ, MYM) and $3.50 (MES), so every version loses after costs.
2. The best learned version (call it **"B"**: 15-min bars, the model's top picks, hold until stopped or 16:45) earns **+$2.72 per trade** across the 3 markets. Almost all of that comes from **MNQ (+$6.52)**. MES is +$0.68 and MYM is -$0.59. Without its 10 best days it is only +$0.17.
3. **Passing fast:** B passes within 10 trading days in at most **5.5%** of start days (MNQ, 5 micros). Purely random trades at their best setting ($400 risk, quick 1.5R exit, more trades) reach **8-11%**. On speed alone, luck with big size is as good or better.
4. Against luck at the **same** number of trades and the same size, B does slightly better: about +1 to +2 points of "passed within 10 days" on MNQ, MYM and all 3 markets together, but not on MES. B was picked after seeing the results, so treat this as a hint, not proof.
5. **Adding a contract on pullbacks made results worse** in about 85-95% of the setups tested.

---

## 2. The luck baseline: what random trades achieve

"Luck" = random entries with no edge at all (random side, or always long), with the same stop rule, costs and exits, sized by fixed micros or fixed $ risk. 20 random draws for each setting.
"Within 10 days" = share of all possible start days on which the eval was passed within 10 trading days.
"p90" = what the luckiest 10% of random draws reached. A real setup should beat this, not just the average.

Best luck setting per market, start days 2013+ (MYM 2018+):

| market | consistency rule | eventually passes | passes within 5 days | within 10 days | within 20 days | p90 draw: passes / within 10 |
|---|---|---|---|---|---|---|
| MNQ | 40% | 27.8% | 2.9% | 10.2% | 18.8% | 52.5% / 11.7% |
| MNQ | 50% | 30.4% | 7.8% | 18.7% | 26.5% | 56.7% / 21.2% |
| MES | 40% | 20.6% | 2.6% | 7.9% | 13.9% | 32.6% / 8.9% |
| MES | 50% | 24.4% | 6.9% | 14.9% | 20.3% | 35.1% / 16.0% |
| MYM | 40% | 25.1% | 3.3% | 11.4% | 19.9% | 44.3% / 13.0% |
| MYM | 50% | 29.6% | 9.3% | 20.4% | 27.3% | 44.3% / 22.3% |

What luck teaches:
- The fastest random passes come from **big $ risk ($400 per trade) and a quick 1.5R target / 16-bar exit**. That is gambling on variance, not edge.
- At 1 micro, random trades take a median of 81-158 trading days to pass. At 5 micros, 22-42 days.
- Random trades lose money per trade: MNQ -$1.37, MES -$4.39, MYM -$2.17 (60-min, hold, both sides).
- **Being long MNQ at random** made +$2.51 per trade, but +$7.86 in 2021-25H1 against +$0.23 in 2010-20, and -$0.03 without the 10 best days. That is the Nasdaq uptrend, not skill. Any long MNQ result has to beat this.

Caution: one single random draw reached a 93% pass rate (MYM, 2022+ starts). Single good runs are easy to get by luck.

File: `v2/out/luck_bar.csv`, `v2/out/luck_table.csv`.

---

## 3. EMA 50 pullback: verdict

Tested: 60-min bars, a pullback that touches the EMA 50 in an uptrend (or the mirror for shorts), held until stopped or 16:45. It was compared with **"trend drift"**: taking a trade at a random bar in the same trend, same side, same year, same hour and similar stop size. "Edge" = setup minus that.
"Clustered t" = how sure we can be; about 2 or more would start to be convincing.

| market | side | trades/yr | $/trade | random trend trade | edge | clustered t | edge 2021-25H1 | $/trade without 10 best days |
|---|---|---|---|---|---|---|---|---|
| MNQ | long | 112 | +6.32 | +2.98 | +3.34 | 0.81 | -3.40 | -1.78 |
| MNQ | short | 81 | -8.81 | -7.65 | -1.16 | -0.21 | +3.54 | -18.15 |
| MES | long | 114 | -0.13 | -1.09 | +0.96 | 0.35 | -10.65 | -5.43 |
| MES | short | 84 | -4.04 | -7.08 | +3.04 | 0.70 | +7.54 | -13.51 |
| MYM | long | 110 | +2.56 | +0.84 | +1.72 | 0.44 | 0.00 | -5.01 |
| MYM | short | 91 | -8.38 | -5.24 | -3.14 | -0.58 | -7.45 | -19.57 |

**Verdict: no real edge.**
- **MNQ:** the long gain is mostly the trend itself (drift). Shorts lose.
- **MES and MYM:** noise.
- The MNQ evening-only longs (6 pm-2 am, +$23.69 per trade) look good but rest on 2020 and early 2025. The 5 best trades are 64% of the profit, and the same idea on 30-min bars loses.
- Out of 1,458 variations tried (timeframe, stop lookback, touch distance, exit, side, hours), **no variation was convincing in both halves of the data**. Fewer passed the significance bar than chance alone would give.
- It is also too rare to pass fast: at most 1.0% of start days pass within 10 days, against luck's 8-11%.

File: `v2/out/ema50_evidence.csv`, `v2/out/ema50_years.csv`.

---

## 4. Exits: which works best, and how many opposite signals to require

The "opposite evidence" exit closes the trade once **N** signs against it show up: a reversal candle, momentum turning, close past EMA 20, EMA 8 crossing EMA 20, a broken swing, the 60-min trend no longer agreeing, a 5-min trigger the other way. "1b" counts signs on the latest bar only; "2b" counts the latest 2 bars.

All of your rule signals together (no model), $/trade:

| market | timeframe | hold until stop / 16:45 | best opposite-evidence exit | avg bars held with that exit |
|---|---|---|---|---|
| MNQ | 60 min | -1.45 | N=3 (1 bar): -0.80 | 5 |
| MNQ | 15 min | **-0.37** | N=4 (1 bar): -0.43 | 13 |
| MNQ | 5 min | **-1.36** | N=3 (1 bar): -1.70 | 9 |
| MES | 60 min | -3.99 | N=3 (2 bars): **-3.05** | 4 |
| MES | 15 min | -3.63 | N=4 (2 bars): **-3.05** | 12 |
| MES | 5 min | -4.62 | N=1 (2 bars): -3.68 | 1 |
| MYM | 60 min | -3.51 | N=3 (1 bar): **-2.04** | 5 |
| MYM | 15 min | **-0.68** | N=4 (1 bar): -1.29 | 13 |
| MYM | 5 min | **-1.85** | N=2 (2 bars): -2.00 | 2 |

What this says:
- **Your instinct is right that exits need more evidence than entries.** With N = 1 or 2 the trade is out after 1-3 bars and just pays costs (about -$2 MNQ/MYM, -$3.7 MES).
- **Best count: N = 3 on 60-min bars, N = 4 on 15-min bars.**
- **But on 15-min and 5-min bars, plain "hold until stop or 16:45" beat every opposite-evidence exit on MNQ and MYM.** N = 3-4 only helps on 60-min bars and on MES.
- No exit turns the rule signals into a profit.
- Caveat, not yet tested: the count includes conditions that are often already true at entry (for example "60-min trend not agreeing" is already on for 24% of MNQ 15-min longs). A version that counts only *new* evidence after entry was not tested, and could give N = 1-2 a fairer chance.

File: `v2/out/v2_raw_exits.csv`.

---

## 5. Does the learned confidence score beat simple counting?

Five model types were tried, each trained only on past years and tested on the next year:
- **M0** = simple count of agreeing signals (your "more confirming signals = more confidence").
- **M1** = a points scorecard where each signal can only count in the direction you'd expect (with-trend signals can only add points; against-trend signals can only subtract).
- **M2** = a standard weighted score (logistic regression).
- **M3** = a decision-tree model forced to respect the expected direction of each signal.
- **M4** = the same tree model with no forcing (for reference only).

Results, out of sample 2013-2025H1, 3 markets pooled. "Edge vs drift" = beyond random trades in the same trend, side, hour and stop size.

| timeframe, exit | model | trades/yr | $/trade | edge vs drift (clustered t) | $/trade without 10 best days |
|---|---|---|---|---|---|
| 60 min, N=3 exit | M0 count | 2154 | -2.13 | -0.86 (-0.5) | -4.73 |
| 60 min, N=3 exit | M1 scorecard | 1427 | +0.05 | +1.00 (0.4) | -4.43 |
| 60 min, N=3 exit | M2 | 1622 | -1.50 | +0.18 (0.1) | -6.66 |
| 60 min, N=3 exit | **M3** | 1031 | **+3.04** | **+5.29 (1.74)** | -1.89 |
| 15 min, hold | M0 count | 2166 | -0.27 | +1.49 (0.79) | -4.08 |
| 15 min, hold | M1 scorecard | 6670 | -0.69 | +0.79 (0.42) | -4.15 |
| 15 min, hold | M2 | 3869 | +2.11 | +1.02 (0.65) | -0.59 |
| 15 min, hold | **M3 (= "B")** | 3774 | **+2.98** | +1.36 (0.83) | **+0.38** |

**Answer: yes, a little, but not enough to rely on.**
- The tree model (M3) beats simple counting (M0) at both timeframes. Simple counting does not help at 60 min.
- But much of what the models learn is mechanical: **skip trades where costs are big compared with the stop, prefer wider stops, and lean long.** Once these are matched away, what is left is about +$1 to +$5 per trade with a clustered t of at most about 1.7-2.0. That is about what the best of 77 tries would give by chance.
- The 60-min M3 "winner" collapses when trained on only the last 5 years (-$0.16 per trade), and its 10 best days carry 161% of its total profit.
- The 15-min M3 (B) is the most consistent: positive in 10 of 13 years and in all 3 markets.
- Note: these stage figures average overlapping trades. With one position per market at a time (section 6), the 60-min M3 drops from +$3.04 to -$1.17 per trade; B stays positive (+$2.72).

### The points table (M1 scorecard)

"Points": in the 15-min table, **+20 points doubles the odds the trade wins**. Middle value over the 13 yearly models. First number = 15-min hold; second = 60-min with the N=3 exit.

| signal | 15 min | 60 min |
|---|---|---|
| price on the right side of VWAP | +7.0 | +1.5 |
| 60-min trend agrees | +3.0 | 0 |
| 5-min trend agrees | +2.5 | +1.4 |
| 15-min trend agrees | 0 | +2.7 |
| reversal candle at the pullback low/high | +1.3 | 0 |
| 5-min trigger in the trade's direction | +1.2 | +2.3 |
| 15-min momentum rising | +1.1 | +0.3 |
| 60-min momentum rising | 0 | +1.9 |
| 60-min swing structure agrees | +0.8 | +1.1 |
| pullback momentum divergence | +0.4 | 0 |
| candle-pattern majority | about 0 | 0 |
| 2 or more rules firing together | 0 | 0 |
| room to the 60-min swing | 0 | 0 |
| **against:** 60-min trend against | -3.3 | 0 |
| **against:** entry right at high/low of day | -3.3 | -1.5 |
| **against:** 15-min structure against | -1.2 | -1.5 |
| **against:** 60-min structure against | 0 | -3.7 |
| **cost compared with stop size** | -71 per 1.0 (about -4 at a typical 0.06) | -67 per 1.0 |

What the points say in plain words: **VWAP side, higher-timeframe trend, not entering right at the high or low of the day, and not trading a tight stop where costs eat the trade** carry the weight. **Candle patterns and "several rules at once" carry about zero.**

File: `v2/out/models_summary.csv`, `v2/out/models_points.csv`.

---

## 6. Eval pass odds and days-to-pass, compared with luck, with and without adds

Each candidate was run through the full eval simulation: one position per market at a time, max 20 micros, $600 daily loss limit, $1,000 trailing drawdown, starting the eval on every possible day. "Matched luck" = random trades from the same pool with the same side, year, time of day and stop size, run through the exact same procedure.

Candidates:
- **A** = 60-min, M3, N=3 exit.
- **B** = 15-min, M3, hold.
- **C** = 60-min, M3 (other target), N=3 exit.

Fastest sizing for each, start days 2013+, 40% consistency, **no adds**:

| candidate | market | size | eventually passes | median days to pass | within 5 days | **within 10 days** | busts | matched luck within 10: average (p90) |
|---|---|---|---|---|---|---|---|---|
| A | MNQ | 5 micros | 24.2% | 31 | 0.3% | 2.1% | 75.3% | 1.8% (2.2%) |
| A | all 3 | 5 micros | 25.5% | 30 | 0.3% | 2.3% | 73.9% | 1.5% (1.9%) |
| **B** | **MNQ** | **5 micros** | 30.1% | 21 | 1.2% | **5.5%** | 69.5% | 3.6% (4.2%) |
| B | MES | 5 micros | 23.8% | 36 | 0.9% | 3.1% | 75.6% | 2.8% (3.6%) |
| B | MYM | $400 risk | 15.1% | 14 | 0.9% | 4.7% | 83.7% | 3.0% (3.6%) |
| B | all 3 | $400 risk | 21.6% | 22 | 0.9% | 4.3% | 78.0% | 3.0% (3.5%) |
| C | MNQ | 5 micros | 32.1% | 35 | 0.4% | 2.1% | 67.1% | 1.7% (2.2%) |
| C | all 3 | 5 micros | 26.8% | 30 | 0.6% | 3.1% | 72.3% | 1.9% (2.5%) |

For comparison: the **best luck of all** (high trade count, $400 risk, quick 1.5R exit) passes within 10 days **7.9-11.4%** of the time.

Best case found anywhere: **B on MNQ, 5 micros, start days 2022+, 50% consistency: 22.7% pass within 10 days** (matched luck 14.4% average, 16.4% p90), 41.7% pass overall, median 10 days. MNQ in 2022+ is the strongest drift period, so this is the most flattering slice.

**Slow but likely (1 micro, no adds):** B on MNQ eventually passes **67%** of the time, but the median is **171 trading days** (matched luck: 28% average, 35% p90). On MES 43% / 267 days; on MYM 34% / 161 days.

### With adds (your "add on the pullback, move the first stop to net breakeven" rule)

| candidate / market / size | no adds: passes / within 10 days | add same size | add 1 micro |
|---|---|---|---|
| B MNQ 5 micros | 30.1% / 5.5% | 20.7% / 1.7% | 25.0% / 2.0% |
| B MES 5 micros | 23.8% / 3.1% | 10.0% / 0.7% | 7.2% / 0.3% |
| B MYM $400 risk | 15.1% / 4.7% | 10.8% / 1.2% | 11.9% / 1.5% |
| B all 3, $400 risk | 21.6% / 4.3% | 19.1% / 2.8% | 17.6% / 2.1% |
| A all 3, 5 micros | 25.5% / 2.3% | 25.1% / 2.2% | 22.6% / 1.4% |
| C all 3, 5 micros | 26.8% / 3.1% | 26.3% / 2.8% | 24.1% / 2.9% |
| **average over all 84 settings** | **24.2% / 1.49%** | 18.9% / 0.77% | 18.4% / 0.69% |

Why adds hurt:
- Most add signals are refused because the first trade is not yet far enough in profit to move its stop to breakeven (only 7-20% of attempts are taken at 1 micro).
- When an add does happen, the earlier stop is pulled close to price, so the whole position is often stopped out at about breakeven after paying extra costs.
- Only one reading of your add rule was tested (stops moved so the whole position nets $0 if all stops hit). Other versions, for example adding only after a new swing forms, were not tested.

**Busts dominate**: 66-92% of starts fail in the fastest settings. At fixed 5 micros there are many days with raw losses beyond -$600 (the simulation then caps the day at -$600). The worst raw day for all 3 markets together was -$10,233 (2025-04-07).

File: `v2/out/evalc_table.csv`, `v2/out/evalc_pnl.csv`.

### B in $ per trade, 1 micro, one position per market

| market | all | 2018+ | 2022+ | 2010-20 | 2021-25H1 | without 10 best days | without 2025H1 |
|---|---|---|---|---|---|---|---|
| MNQ | +6.52 | +9.40 | +12.57 | +3.50 | +9.81 | +3.27 | +5.80 |
| MES | +0.68 | +1.20 | -0.96 | +1.87 | -0.33 | -1.80 | +1.11 |
| MYM | -0.59 | -0.59 | -4.98 | +6.15 | -3.68 | -2.81 | -1.03 |
| all 3 | +2.72 | +3.52 | +2.46 | +3.45 | +2.13 | +0.17 | +2.47 |

B (all 3 markets) by year, 2013 to 2025H1: -2.6, 0.5, 1.1, -3.0, 0.5, 7.9, 3.1, 8.3, 1.2, 1.4, -2.0, 8.3, 8.3.
Against matched luck, B's all-3 edge is about +$3 per trade, and it stays about +$2.4-2.7 without the 10 best days (the luck draws lose their own best days too). But B was chosen after looking at all results, and MNQ (the uptrending market) carries it.

### Chart gallery: B's out-of-sample trades

15-min charts in your NinjaTrader-like style. Yellow ring = signal bar; yellow line = entry; red dashed = stop; magenta X = exit. Trades were chosen at random (seed 7), 1 micro, no adds. Every entry was checked to equal the open of the bar after the signal.

12 random trades (4 per market):
- [MNQ 2024-09-25 long, +$77.50](out/gallery/random_MNQ_20240925_1415_long.png)
- [MNQ 2021-10-12 short, +$26.50](out/gallery/random_MNQ_20211012_1600_short.png)
- [MNQ 2024-01-26 short, +$14.50](out/gallery/random_MNQ_20240126_1600_short.png)
- [MNQ 2022-03-16 long, +$134.00](out/gallery/random_MNQ_20220316_1545_long.png)
- [MES 2013-04-17 short, -$22.69](out/gallery/random_MES_20130417_1145_short.png)
- [MES 2018-10-29 short, +$111.50](out/gallery/random_MES_20181029_1400_short.png)
- [MES 2024-05-15 long, +$35.25](out/gallery/random_MES_20240515_1245_long.png)
- [MES 2023-11-14 long, +$176.50](out/gallery/random_MES_20231114_0830_long.png)
- [MYM 2020-08-31 short, -$27.00](out/gallery/random_MYM_20200831_1100_short.png)
- [MYM 2020-11-20 short, +$55.50](out/gallery/random_MYM_20201120_1430_short.png)
- [MYM 2023-09-15 short, +$83.50](out/gallery/random_MYM_20230915_1000_short.png)
- [MYM 2021-02-14 long, +$40.50](out/gallery/random_MYM_20210214_2000_long.png)

6 losing trades (2 per market):
- [MNQ 2014-03-03 short, -$24.50](out/gallery/loser_MNQ_20140303_1100_short.png)
- [MNQ 2016-08-31 short, -$25.50](out/gallery/loser_MNQ_20160831_1200_short.png)
- [MES 2015-10-23 long, -$8.50](out/gallery/loser_MES_20151023_1330_long.png)
- [MES 2023-02-28 short, -$57.25](out/gallery/loser_MES_20230228_1130_short.png)
- [MYM 2021-09-27 long, -$28.17](out/gallery/loser_MYM_20210927_1145_long.png)
- [MYM 2021-11-29 short, -$34.60](out/gallery/loser_MYM_20211129_1100_short.png)

Note: 10 of the 12 random trades won. B's real win rate is not that high (the average is only +$2.72 per trade), so this sample happens to be friendlier than usual. Don't judge B by the gallery. List with prices: `v2/out/gallery/gallery.csv`. Rebuild: `v2/gallery.py`.

---

## 7. What did NOT work

| idea | result |
|---|---|
| EMA 50 pullback (60 min) | no edge in any market; MNQ long = trend drift; too rare to pass fast |
| All your rule signals together, no model | +$0 to +$1.6 before costs, loses after costs everywhere |
| 5-min bars | hopeless after costs (best -$1.36 per trade, model +$0.47 with ~0 edge) |
| Short trades | lose in every market and every test |
| Opposite-evidence exit with N = 1-2 | out in 1-3 bars, pays costs |
| Simple signal count (M0) as confidence | does not help at 60 min; marginal at 15 min |
| Candle patterns as confirmation | about zero weight in the scorecard |
| "More rules firing at once" | zero weight |
| Adding on pullbacks with stop to net breakeven | lowers pass odds in about 85-95% of settings |
| Model trained to beat drift directly | about $0 edge at 15 min, small (+$1.5-2.2, t below 1) at 60 min |
| 60-min "winner" (A) | collapses with one position per market (-$1.17) and with 5-year training (-$0.16) |
| MNQ evening longs | rest on 2020 and 2025H1; fails on 30-min bars |

---

## 8. Recommended next steps and decisions for you

**Recommended next steps**
1. **Do not trade any of this live yet.** Nothing here is strong enough.
2. If you want to keep going with B, the honest next test is a **paper-forward run** (new data as it arrives), not more digging in the old data. Over 4,000 configurations have already been tried and logged; more tries on the same data mostly find luck.
3. Test the one exit idea that wasn't tested: **count only evidence that appears after entry** (a "new" momentum turn, a "new" EMA cross), with N = 1-3.
4. Test other versions of your add rule (for example add only after a new higher low forms, stop under that low).
5. Speed of passing is driven mainly by **size and variance**, not edge. If the goal is passing quickly, the sizing plan matters more than the entry signal, and fast passes also mean many busts (66-92% in the fastest settings).

**Decisions you need to make**
1. **Final exam on the locked July 2025+ data?** It can only be used once. My suggestion: **not yet.** Use it only when one fully fixed candidate (rules, model, sizing, exit) is ready. If you want to know whether B holds up, B (MNQ only, no adds, 5 micros or $400 risk) is the only reasonable choice.
2. **MNQ only, or all 3 markets?** B's gains are almost all MNQ, which is also the market with the strongest upward drift. MES and MYM add little.
3. **Do you accept a long bias?** Shorts lost everywhere. A long-only version would be simpler, but it is closer to "just being long Nasdaq".
4. **Speed versus survival:** 5 micros or $400 risk passes faster but busts 70-84% of the time. 1 micro passes B on MNQ 67% of the time, but takes a median of 171 trading days.

---

## Things to keep in mind (fine print)

- **Daily loss limit**: the simulation checks the $600 limit only on closed trades and only stops new trades. Lucid may also count open losses intraday, so real results could be a bit worse, especially at fixed 5 micros.
- **Trailing drawdown** is checked only at the end of each day; an intraday check would bust somewhat more often.
- **Old dollars**: before about 2018 a fixed number of micros risked far fewer dollars, so fixed-micro results across years are not like-for-like. $-risk sizing is the fair comparison.
- **On 60-min bars** the "hold" exit ends at 16:00 (the last full bar before 16:45).
- **Multiple tries**: 4,160 v2 configurations are logged in `out/trials.csv` (luck 96, EMA 50 1,458, raw dataset 2,277, models 77, eval candidates 252). With that many, a few "good" results are expected by chance.
- A bug in the old code let 2010-2015 trades run past 16:45. The v2 work fixes it (`v2/lucid.py`). The old files in `out/` still contain those late exits.
- Unit tests: all v2 test files pass except one stale test in `v2/test_models.py` (a test fixture missing two columns added later; the reported numbers were reproduced independently).
- All numbers here come from the stage output files listed under each section. Every stage was re-checked by an independent reviewer: trades re-walked from the raw 1-minute data matched to the cent, and there is no look-ahead and no use of the locked data. The gallery's entry prices were checked against the bar opens; its charts were not hand-checked bar by bar.
