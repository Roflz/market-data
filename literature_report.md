# Intraday MES/MNQ trading bot: what the verified literature says, and what to do next

This report is for the trader and the engineer. It uses the verified literature notes, plus a small number of sources added during review. Those are entries [73]-[85] in Section 8 and are marked "added in review, lightly verified". Numbers in square brackets point to Section 8, which gives the authors, year, URL and verification status for each source.

Treat the following with caution:
- claims from sources marked "partly verified" or "added in review";
- any number described as unverified.

Where a figure is our own arithmetic, extrapolation or recommendation rather than a result from a paper, the text says so.

**Conventions used throughout (our arithmetic and choices):**
- **Index levels.** ES is taken as 6,500 and NQ as 25,000 unless stated otherwise.
- **Contract specs.**
  - MES is $5 per point; one tick is 0.25 point ($1.25). One MES is about $32,500 notional.
  - MNQ is $2 per point; one tick is 0.25 point ($0.50). One MNQ is about $50,000 notional.
- **Round-trip costs:**

| Exit type | MES | MNQ |
|---|---|---|
| Market or stop exit (2 ticks plus $1.50) | $4.00 = 0.8 point ≈ 1.2 bp | $2.50 = 1.25 points ≈ 0.5 bp |
| Limit target exit (only the entry pays slippage) | $2.75 = 0.55 point | $2.00 = 1.0 point |
| Overnight fills (2 ticks per side) | $6.50 = 1.3 points ≈ 2.0 bp | $3.50 = 1.75 points ≈ 0.7 bp |

- **Volatility.** ES is taken as 16% annualized. NQ volatility in percentage terms is taken as about 1.35 times ES's.
- **Bar timestamps.** Databento 1-minute bars are stamped at the bar's open. "The price at 10:00" means the close of the 09:59 bar.
- **Sizing tests** use a stated research equity of $100,000, alongside the trader's actual account equity.

---

## 1. Bottom line

- **Generic indicator rules on the index's own bars do not predict direction mid-session after costs.**
  - Large searches over indicator rules find nothing that survives both a data-snooping correction and costs in modern data:

    | Search | Rules | Result |
    |---|---|---|
    | S&P 500 futures, 1984-96 [10] | 7,846 | Best Reality Check p = 0.908 |
    | 17 US futures markets [13] | 9,385 | The best S&P rule fell from 14.15%/yr in-sample to 1.49% out of sample |
    | 5-minute SPY data, 2002-03 [16] | 7,846 | None survive, even before costs (counts from a secondary source) |
    | DJIA, 1962-2011 [15] | – | The false-discovery-rate method finds no outperforming rules, even at zero cost |

  - **One published study of 15-minute market returns** reports an out-of-sample R² of about 0.07-0.10%. It uses 272 cross-sectional factor portfolios, not the index's own bars [39].
- **The intraday effects with credible evidence are tied to a clock time or an event.** They happen once a day and are driven by identifiable flows. Each is worth a few bp gross per trade, except FOMC days:
  - **Last 30 minutes.** The last 30 minutes before the 16:00 cash close follow the rest-of-day return. The effect shows up only when options dealers are short gamma [1][2]. The proposed mechanisms are:
    - dealer-gamma fragility [73];
    - leveraged-ETF rebalancing [74];
    - a 16-market out-of-sample study [75], which finds the effect stronger when liquidity is low and volatility high.

    All three are added in review, lightly verified.
  - **Overnight.** The 02:00-03:00 ET hour drifts upward after weak closes [4].
  - **FOMC.** The 24 hours before an FOMC statement drift upward, about 49 bp per event at 8 events a year [51].
  - **Early breakouts.** Breakouts in the first minutes after the open have practitioner-only evidence [7][22][25].
- **Several of those effects have weakened or disappeared since about 2014-2020:**
  - **Last half hour.** Rosa's 5-minute ES test finds the last-half-hour trade (signed by the overnight return) disappears out of sample in 2014-2020, except March-December 2020 [3].
  - **Overnight drift.** The authors' own 2026 update finds the 2-3 am window averaged about zero over 2021-2025 [4].
  - **Pre-FOMC drift.** It had essentially disappeared by 2016-2019 [54].
- **The breakout effects show long losing stretches, which is not the same as demonstrated decay.**
  - **Noise-band breakout [7]** (practitioner, in-sample). It lost money in 2016 (-12.8%) and 2017 (-6.9%), then made +61.1% in 2018, +37.2% in 2023 and +32.2% in 2024. Losses were concentrated in low-volatility years.
  - **5-minute opening-range breakout.** A practitioner replication was negative in 2015-17 in every market tested [25].
- **The horizon matters. Our 15-120 minute window is among the weakest in the evidence we have.**
  - **Order flow.** In modern data, order flow's predictive power lasts seconds to a few minutes [42][47][48]. In 1996 NYSE data it reached about 30 minutes, falling to about 5 minutes by 2002 [42].
    - Cont-Kukanov-Stoikov [41] is about how order-flow imbalance explains *contemporaneous* price changes. It is not evidence on prediction.
  - **Trend premia.** These show up at 1-12 month horizons, and in index futures they accrue overnight. This rests on monthly-horizon signals; applying it to intraday features is an extrapolation [5][71].
  - **Volatility.** What *is* forecastable at our horizon is volatility, not direction.
    - The HAR model forecasts next-day realized volatility with an out-of-sample R² of about 0.70 [67].
    - Intraday volatility follows a strong U-shape through the day [66].
- **Our results are consistent with the literature. Nothing in them looks like a bug.**
  - **Pre-cost edge.** Every strategy came out within about $1.50 per trade of zero before costs. Mesfin's independent MNQ study found the same: 11 of 14 signal families had gross edges of 0.07-1.5 points against 2 points of friction [8] (partly verified preprint).
  - **Out-of-sample correlation.** Our out-of-sample rank correlation of 0.00-0.04 would correspond to an R² of roughly 0-0.16% under the rough approximation R² ≈ IC². That is the same order of magnitude as the one 15-minute study [39]. The comparison is loose: our IC is a rank correlation on overlapping dollar bracket outcomes, not an R² on fixed-horizon returns.
  - **Per-state stop/target.** Choosing stop/target per market state made random entries profitable in-sample. That is the textbook result of selecting on noise [26][28]. It was amplified because the procedure picked the best bracket in each of 81 states and added the 81 winners together (Section 3.4).
  - **Scan survivors.** The 252 survivors were too many to be independent noise. But they came from one correlated "buy NQ after a drop" family and failed in 2016-2018 and 2026. That points to a regime-dependent common factor in 2019-2025, such as bull beta or buy-the-dip, rather than a persistent edge (Section 3.2).
  - **Classic setups.** Profit factors of 0.72-0.88 are consistent with the net losses and low Sharpe ratios in [13] and [20]. Those papers report returns and Sharpe ratios, not profit factors.
- **Costs are not unusual in bp terms. The edge per short trade is too small.**
  - Our micro costs are similar to or below many academic assumptions: about 1.2 bp round trip on MES and about 0.5 bp on MNQ, against 3 bp round trip in [20] and 1 bp per side in [18].
  - Costs dominate our results because the gross move captured in a 15-30 minute hold is a fraction of a point.
  - **For once-a-day structural trades** (Section 5.1, our arithmetic on historical gross effects):
    - **On MNQ,** cost is a small share of the historical edge, so the main question is whether the effect still exists.
    - **On MES,** cost takes about 35-47% of the historical last-half-hour and noise-band edges.
    - **The overnight drift** does not clear our overnight MES cost unconditionally.
    - These effects were concentrated in high-volatility years, so the pooled dollar figures overstate their value in calm years.
- **Stops control loss size; they do not create edge. The trader's directional skill is unproven.**
  - **Stops and expected return.** Under a random walk, a stop cannot raise expected return [63]. With costs, tight stops hurt [64].
  - **What stops do.** A stop reliably caps the loss tail, which is exactly the trader's documented failure.
    - Holding losers is close to universal among human traders [60][61].
    - It was nearly zero in one small study of algorithmic accounts [65].
  - **Base rates for skill.** Persistent day-trading skill is rare:
    - under 1% of Taiwanese day traders [57];
    - 3% net-profitable among persistent Brazilian mini-index day traders [59].

    The trader's directional skill should be tested with a forward log before the bot is built around it.
- **Recommended path:**
  - Stop broad mining.
  - Re-score past work with PBO, the deflated Sharpe ratio, a reality-check-style test (SPA) and a drift-preserving synthetic null.
  - Run a small set of pre-registered replications:
    - the noise-band breakout, whose post-publication window for futures starts in October 2024 (February 2025 to be strict);
    - the last-half-hour trade signed by the prior-close-to-15:30 return;
    - overnight and FOMC event trades;
    - the 5-minute opening-range breakout with a random-direction control.
  - Use volatility forecasts for sizing.
  - Treat forward paper trading as the only clean out-of-sample test.
  - Expect most of these to come out near zero after 2015. That would itself answer the question.

---

## 2. Signals with real evidence, and what is not supported

### 2.1 Ranked by strength of evidence and relevance to 1-minute OHLCV ES/NQ data

| Rank | Signal | Evidence base | Key numbers | Status after publication | Fit with our data |
|---|---|---|---|---|---|
| 1 | **Volatility and range forecasting (for sizing, brackets and no-trade filters; not direction)** | Peer-reviewed, consistent across decades [66][67][70]; HARQ refinement [81] (added in review); partly verified [38] | 5-minute S&P futures, 1986-89: the first ten autocorrelations of raw returns are 0.018 or smaller in absolute value. Absolute returns follow a strong U-shape: about 0.095% at the open, 0.055% at midday and 0.105% near the cash close [66]. HAR out-of-sample R² on S&P futures (1990-2007): 0.696 at 1 day, 0.698 at 1 week, 0.627 at 2 weeks [67]. A random forest predicts the sign of the *change* in volatility and higher moments over about a week with 0.54-0.61 accuracy [38]. | Stable property of the market | High: everything can be computed from 1-minute bars |
| 2 | **Last-half-hour momentum: the prior close to 15:30 return predicts 15:30-16:00** | Two peer-reviewed papers [1][2]; independent decay evidence [3]; out-of-sample evidence in 16 developed markets [75]; mechanisms [73][74] ([73]-[75] added in review) | SPY 1993-2013: the sign strategy earns 6.67%/yr, Sharpe 1.08, about 2.6 bp per trade [1]. Pooled equity futures (Baltussen et al.): slope 4.18 (t=7.29), out-of-sample R² 2.88%. ES out-of-sample R² 2.29%, NQ 3.76% (data to May 2020). Slope 6.63 when dealers are short gamma, 0.82 (t=1.03) when they are long [2]. | **Never tested by us. Baltussen's evidence ends in May 2020.** The version signed by the overnight return disappears in ES over 2014-2020 except Mar-Dec 2020 [3]. Our SPY test of the prior-close-to-10:00 version lost every year. | High: one trade a day. We lack dealer-gamma data (see [78] for a paid source). |
| 3 | **Overnight drift (02:00-03:00 ET) after weak closes, a dealer inventory premium** | Peer-reviewed (RFS) [4] | 1.48 bp/day (t=7.13), 1998-2020. After quoted-spread costs over 2004-2020, the plain version earns -0.59%/yr (Sharpe -0.54); the buy-the-dip version earns 4.04%/yr (Sharpe 1.10). Larger when VIX is high: about 2.6 bp at VIX 20 and 6.1 bp at VIX 30 for a one-SD more negative closing imbalance. | The authors' 2026 update: about zero in 2021-2025, with the same disappearance in NQ and YM [4] | Medium: needs overnight holding. The true closing-imbalance signal needs trades data; a return-based proxy is possible. |
| 4 | **FOMC and announcement-day effects** | Peer-reviewed [50][51][52][54]; partly verified [56] | Pre-FOMC drift: 49 bp in 2pm-to-2pm windows (1994-2011), Sharpe 1.14 [51]. FOMC cycle: holding only in even weeks gives Sharpe about 0.83 vs 0.42 (1994-2013, gross) [52]. Announcement days earn 11.4 bp of excess return vs 1.1 bp on other days (1958-2009, daily data) [50]. Post-SEP first hour: about 56 bp (17 events in 2012-2015, secondary source) [56]. | Pre-FOMC drift essentially gone in 2016-2019 [54]. The FOMC cycle has no out-of-sample test after 2016. | Medium: few events, so statistical power is low |
| 5 | **Breakout beyond a time-of-day "noise band", with a VWAP/band trailing exit** | Practitioner, in-sample, not independently replicated [7] | SPY 2007-2024: Sharpe 1.24 at 1x leverage, 1.33 with volatility targeting. 37% of trades win; returns are positively skewed. About $0.09 per share per trade; whether that is net of costs is not stated. The FAQ reports S&P futures Sharpe 1.32 and Nasdaq futures 1.23, costs not stated. | Long losing stretches in calm years: -12.8% (2016), -6.9% (2017), then +61.1% (2018), +37.2% (2023), +32.2% (2024). **The authors' Feb 2025 revision added a futures FAQ with data through Sep 2024, so for futures the window untouched by the authors starts Oct 2024 (Feb 2025 to be strict).** | High: the most precisely specified design, and directly testable |
| 6 | **Opening-range breakout using the first 1-5 minutes** | Weak: working paper [20], partly verified [21], practitioner [22][25] | S&P futures 1991-2010: net 0.3-3.0%/yr, mean/SD 0.09-0.18, below buy-and-hold [20]. QQQ 2016-2023: +0.13R per trade, no slippage modeled [22]. NQ CFDs 2015-2026: full sample +0.131R gross (t=2.9). In the cost-filtered sample (n = 2,638), +0.147R gross and +0.002R net at 2.5 points of cost. The first-candle direction beats a random-direction bracket by +0.124R (t=2.1) [25]. | Negative in 2015-17 in every market [25] | High: cheap to test |
| 7 | **Cross-sectional lead-lag (lagged returns of index constituents or factors)** | Peer-reviewed [39][48]; partly verified [40] | 15-minute market-return out-of-sample R² of 0.07-0.10%. Long/flat SPY strategy Sharpe 0.79 after half-spread costs; the long/short timing strategy is negative on QQQ, which has a wider spread [39]. Ensemble Sharpe 0.98 after costs (abstract only) [40]. At 1-minute horizons, cross-asset *lagged returns* do as well as cross-asset order-flow imbalance [48]. Most index price discovery happens in the E-mini, so ETFs should lag ES/NQ, not lead them [82] (added in review). | Predictability is concentrated in crises and fell after decimalization [40] | Medium-low: needs constituent data; edge is tiny relative to cost |
| 8 | **Short-lag reversal / contrarian trading** | Mixed [17][18][6][37] | FX: break-even costs of 1-3 bp, with apparent profits concentrated in thin hours [17]. 30-minute contrarian rules beat trend rules on S&P futures 1983-2007 (all models: 7.2% gross, 2.6% net per year); the 2004-07 sub-period was negative [18]. In stocks, sub-hour reversal is mostly bid-ask bounce [6]. | Decaying | Low-medium: consistent with our "buy after a drop" survivors, but those failed out of sample |

### 2.2 What the literature does not support

- **Plain indicator rules as entry signals after costs and snooping correction.** This covers MA/EMA crossovers, filters, channel breaks, RSI, momentum oscillators and OBV.
  - White: 3,654 indicator models reached 54.7% directional accuracy, but the Reality Check p-value was 0.204 [31].
  - Park & Irwin (S&P futures): the best of 9,385 rules lost about 90% of its in-sample return out of sample [13].
  - DJIA: the best rules selected by false discovery rate had in-sample Sharpe ratios of 3.4-5.3 and out-of-sample Sharpe ratios of -0.74 to +0.55. Fewer than 5% of selected rules were still selected the next month [15].
  - FX: filter and MA profits were gone by the early 1990s, consistent with the Adaptive Markets view [14].
  - Brock-Lakonishok-LeBaron's DJIA results (1897-1986, gross) were robust within that sample but did not hold after 1986 [9][10].
- **Intraday momentum continuation from bar technicals.**
  - In 22 equity-index futures, time-series momentum earns its returns overnight. The intraday component is about zero (raw -0.29%/month) with a skew of -2.77 [5]. Caveat: those signals are monthly, so applying the result to 60-minute EMA/MACD features is an extrapolation.
  - The documented trend premium is a 1-12 month effect [71].
- **15, 30 and 60-minute opening-range and initial-balance breakouts.**
  - In stocks with a relative-volume filter, Sharpe falls from 2.81 for a 5-minute range to 0.21 (30-minute) and 0.40 (60-minute) [23].
  - For E-minis, Tsai et al.'s abstract says only that the best probe time was "short" for US markets [21]. Everything more specific is unverified:
    - the reported best lengths (1 minute for S&P and Nasdaq, 4 minutes for the Dow);
    - the per-market numbers;
    - the chart reading that 30-90 minute ranges are near zero.
- **The same clock-time interval yesterday as a direction feature.**
  - That effect is cross-sectional in stocks [6].
  - At the index level, the prior day's last-half-hour return carries a *negative* coefficient (-6.81) for today's last half hour. Other intervals were not tested [2].
- **Order-flow proxies built from bars for direction,** such as the tick rule on bars, bulk volume classification (BVC) and VPIN.
  - BVC on 1-minute bars misclassifies 23.2% of contracts. The tick rule on 60-second bars misclassifies 38.7% [44].
  - VPIN does not indicate direction [43]. Once volume and realized volatility are controlled for, it adds nothing to volatility forecasts, and VIX is far stronger [44].
- **Deep learning on the order book at retail latency.** The horizons are seconds and the predictable move is a tick or less [45][46][47].
- **Choosing stops and targets per market state as a source of edge.** See Section 3.4 and [63][69]. If brackets must vary with state, derive them from a fitted price process rather than a backtested grid [79][80] (added in review).

### 2.3 Where the evidence is thin or conflicting

- **Little peer-reviewed work tests intraday rules on ES/NQ after 2015 with retail micro costs.** The two closest studies are:
  - Mesfin: an independent preprint, partly verified, MNQ 2021-2025 [8];
  - an MQL5 replication: a practitioner blog read through a fetch-tool summary [25].

  Both agree with our nulls, but neither is strong evidence.
- **Whether intraday returns show momentum or reversal depends on the clock and the regime.**
  - Momentum: the last half hour [1][2][75], the noise-band breakout [7], and the 1-5 minute opening-range breakout [22][25].
  - Reversal: short lags [17][6], overnight after sell-offs [4], and 30-minute contrarian rules [18].
  - Proposed mechanisms (added in review, lightly verified):
    - Dealer gamma combined with illiquidity predicts intraday momentum when gamma is negative and reversal when it is positive [73].
    - Behind the last-half-hour effect, leveraged-ETF rebalancing pushes toward momentum, while options delta-hedging can push toward reversal; the pressure reverts at the next open [74].
  - A reasonable reading is that these are flow- and time-specific effects, not a general property of intraday returns.
- **Volatility management.**
  - Moreira-Muir: about +25% Sharpe in-sample [68].
  - Cederburg et al.: real-time versions are worse in 72 of 103 strategies [69].
  - Harvey et al.: the reductions in volatility-of-volatility and left-tail risk are robust; Sharpe gains appear only for risk assets [70].
- **Rolling vs expanding training windows.**
  - Pooled, longer history wins in [45], but that was next-tick prediction with billions of events.
  - The decay evidence argues for weighting recent data [14][36].
  - Liu & Stentoft use a 10-month rolling window (secondary source only) [40].
  - Test both, and count both as trials.
- **The dealer-gamma channel after 2022 (0DTE options).** The evidence conflicts; both sources below are secondary only and need verification before use:
  - Dim, Eraker & Vilkov: according to secondary summaries, higher 0DTE gamma goes with *lower* intraday volatility [76].
  - Brogaard, Han & Won: according to news coverage, a one-SD rise in 0DTE volume is associated with about 14% *higher* S&P daily volatility [77].

  Treat whether the gamma channel still works in 2022-2026 as open.
- **Institutional rebalancing flows** (added in review, abstract and press coverage only). Predictable calendar and threshold rebalancing creates price pressure that can be front-run [84]. This fits the structural-flow thesis and could be tested on ES as a daily-hold sleeve (P10).
- **Many headline positives are practitioner or in-sample work.**
  - The Zarattini group's papers [7][22][23] have commercial ties and no hold-out period.
  - Tsai et al. picked the best of about 390 range lengths with no snooping correction [21].
  - Wu et al. mention no transaction costs [24].
- **Several key numbers come from working-paper versions.** For example, the announcement-drift paper's working-paper version reports 7 of 21 announcements with drift and a drift share of about 49%. The published version reports 9 of 20 and about 40% [53].

---

## 3. Why our results look the way they do

### 3.1 Gross edge is about zero at our holding periods

- **Pre-cost edge vs cost.**
  - Our hand-written rules were within about $1.50 per trade of zero before costs, against $2.75-4.00 of cost on MES.
  - Mesfin found the same on MNQ: gross edges of 0.07-1.5 points against 2 points of friction. Their friction ($4 per MNQ round trip) is about 1.6 times ours [8].
- **Positive before costs, negative after.** Krauss et al.'s ensemble had an after-cost Sharpe of -0.88 in 2010-2015 while staying positive before costs [36].
- **Cheaper execution does not rescue out-of-sample failure.** In Park & Irwin, halving costs from $100 to $50 did not fix it. The binding problem is gross-edge decay and snooping, not the cost model [13].
- **Our boosted models have not been shown to be informative.**
  - The top 1% of predicted trades beat the average trade by $6-18, but no significance test was run.
  - The outcomes are dollar results of 6/12-ATR brackets. High-volatility states produce larger dollar outcomes in both directions, so the top-ranked trades may simply be the high-volatility trades.
  - Lo-Mamaysky-Wang distinguish a signal that is informative (it shifts the distribution) from one that is profitable [11]. Before calling ours informative in that sense, do two things (P0i):
    - normalize each outcome by volatility at entry;
    - compare the top-ranked trades with random entries in the same state and time of day.

### 3.2 The search is very large

Our research history is one large search universe:
- hand-written rules;
- 43,457 scan conditions (× 4 horizons = 173,828 if those are counted separately);
- 81 states × 48 stop/target pairs = 3,888 combinations;
- boosted-tree setups: 32-88 features × 8-16 stop/target pairs × thresholds × rolling or expanding windows × ES/NQ × 1-minute or 5-minute bars;
- the classic setups.

How much "profit" pure noise produces from a search this size:
- **Expected best Sharpe ratio under the null** [27][28]:

  E[max] ≈ √V[SR]·((1-γ)Φ⁻¹(1-1/N) + γΦ⁻¹(1-1/(N·e))), with γ = 0.5772.

  These are our calculations from the papers' formulas, assuming independent trials:
  - For N = 43,457 trials this is about 4.21 standard errors. Annualized, that is about 1.88 on 5 discovery years, or about 1.04 on all 16.4 years.
  - For N = 3,888 it is about 3.62 standard errors. That is not the right model for our per-state bracket procedure, which summed 81 per-state maxima (Section 3.4).
- **Minimum backtest length.** With 5 years of data, no more than about 45 independent configurations can be tried before an in-sample Sharpe of 1 is expected from noise alone [28].
- **Chance baseline for the scan** (our arithmetic):
  - **One stage.** If discovery used a p<0.01 screen, about 435 of 43,457 independent null conditions would pass by chance. Marshall et al. make the same single-stage point: about 78 expected false passes out of 7,846 at p<0.01 [16].
  - **Two stages.** Our survivors also had to pass validation (2024-2025). Under independent nulls, the expected two-stage count is about 435 × the validation pass rate. At a pass rate of about 0.025-0.05 (for example, p<0.05 with the same sign), that is roughly 10-20, not 435.
  - **Correlation.** Correlated conditions leave this expected count unchanged but make it much more variable, because correlated conditions pass or fail together.
  - **Reading.** The 252 survivors exceed an independent-noise baseline by an order of magnitude. They came almost entirely from one correlated family ("buy NQ after a sharp drop") and then failed in 2016-2018 and 2026. The better reading is a real but regime-dependent common factor in 2019-2025, such as bull beta or buy-the-dip. It is not pure noise, and it is not a persistent edge.
  - **Few independent findings.** The 252 survivors amount to very few independent findings.
  - **Right baseline.** The right baseline is the survivor count the same pipeline produces on a *drift-preserving* synthetic null (Section 7, P0d).
- **Significance hurdles.**
  - Bonferroni at 5% two-sided over 43,457 tests needs t ≈ 4.9 (our calculation).
  - Harvey-Liu-Zhu recommend t > 3.0 for a new factor even with a theoretical motivation, and higher for brute-force scans [30].

### 3.3 Overlapping labels shrink the real sample

- **How many labels overlap.** A 2-hour outcome evaluated every 5 minutes overlaps about 24 other labels. Evaluated every 1 minute, it overlaps about 120 [34].
  - At about 19,600 RTH 5-minute decisions a year, that leaves roughly 800 independent observations a year (our arithmetic).
  - That is consistent with an in-sample rank correlation of 0.18 against about 0.02 out of sample.
- **Naive t-statistics on overlapping labels are inflated.**
  - For roughly uncorrelated returns the inflation can approach √24 ≈ 5 times. The √24 figure is the researcher's approximation.
  - The true factor depends on the autocorrelation structure. Compute it with HAC errors or day-level aggregation rather than assuming it [30].
- **The most robust direction effects in index futures are once-a-day observations with R² of about 2-3%** [2]. A signal like that cannot be seen in a bar-level rank correlation over overlapping 2-hour labels.
  - Shorter-horizon predictability does appear in the literature:
    - a 15-minute effect from factor portfolios [39];
    - order flow at 5-30 minutes in 1996-2002 [42];
    - short-lag reversal [17].
  - It is smaller, needs data we lack, or has decayed.

### 3.4 Choosing brackets cannot create edge

- **Under a driftless martingale, no stop/target/time-exit rule changes expected gross P&L.** This is the optional stopping theorem, a standard result rather than one from the papers. Costs then make the expected P&L negative.
  - For a pure bracket on a continuous driftless path, the probability of hitting the target first is s/(s+t), where s and t are the stop and target distances. With a time barrier, 1-tick price steps, a 1-tick trade-through requirement and drift, the realized hit rate will differ from s/(s+t) even with no edge. P0(e) therefore tests mean P&L, not hit rates.
  - In 2019-2023, random *long* entries also collected bull-market drift, so per-state bracket selection could lean on beta.
- **Stops change only the distribution of outcomes, not the mean**, unless losses continue (momentum) or the stop detects a regime with a negative mean. Kaminski-Lo derive this with transaction costs set to zero [63].
- **How selection produced our +$21.5k in-sample result from random entries** (our arithmetic):
  - The procedure picked the best of 48 brackets in each of 81 states and added the 81 winners. The inflation is therefore the sum of 81 per-state maxima, not the best of 3,888 trials.
  - The expected maximum of 48 independent null brackets is about 2.2 standard errors of that state's mean P&L. It is somewhat less in practice, because the 48 brackets are correlated.
  - Suppose the 81 states had equal trade counts and independent P&L. Then the combined in-sample total would be inflated by roughly 2.2 × √81 ≈ 20 standard errors of the combined P&L. That alone can produce a large positive total from random entries.
  - Random long entries also collected the 2019-2023 drift on top of that.
  - P0(d) measures both effects directly on null data.
- **The principled alternative to a backtested grid.** Derive brackets from a fitted price process [79][80] (added in review, lightly verified). These methods imply no bracket adds value when the fitted process has no drift or mean reversion, which is the point.
- **Overfit configurations can lose money out of sample, not just break even.** Bailey et al. show that when returns have memory, in-sample and out-of-sample performance become negatively related [28].
- **Cederburg et al. found the same failure in volatility-managed portfolios:** conditioning parameters that are unstable over time destroy real-time performance [69].

### 3.5 Regime change and decay

- **Edges decay, the most-studied ones first** [14]. Specific examples are in [3][4][54][36][18], with long losing stretches in [7][25].
- **Our failures fit a decaying, regime-dependent edge.** The scan survivors failed in 2016-2018 and 2026, and ES and NQ disagreed.
- **The "buy NQ after a sharp drop" survivors have three candidate explanations.** They are ranked here by fit with the facts:
  1. **Bull-market beta plus short-term reversal** (best fit). Fischer-Krauss's LSTM rediscovered this pattern [37]. It fits a long-only, NQ-concentrated family that worked in 2019-2025. Its 2016-2018 failure would need a weaker reversal payoff in those years, which can be tested.
  2. **The FOMC-cycle "Fed put" in even weeks** [52]. This is partly verified: the authors' follow-up supports it, but it was not checked in the published text.
  3. **A liquidity or inventory premium realized overnight** [4] (worst fit). The scan used RTH-only SPY/QQQ data, so it had no overnight leg. The survivors also passed validation in 2024-2025, when [4] reports the drift was about zero. They failed in 2016-2018, when the drift was still strong. That timing is the opposite of what this explanation predicts.
- **Which explanation applies can be tested** (Section 7, P0h).

### 3.6 Our holdouts are already contaminated

- **2016-2018, 2024-2025 and 2026 have all been looked at.**
- **There is no true out-of-sample test on data the researcher has already seen** [29].
- **The gold standard is a long post-sample period untouched during design** [10].
- **What remains clean:**
  - **Forward paper trading** from now on.
  - **Exact literature replications run without tuning,** over the period after each paper's sample ended. That period is out of sample relative to the authors' choices, though not relative to everything we have looked at.
- **The noise-band window** [7]:
  - The SPY sample ends in April 2024.
  - The authors' February 2025 revision added a futures FAQ with data through September 2024, plus post-publication monthly returns.
  - For futures, the window untouched by the authors therefore starts in October 2024, or February 2025 to be strict.
  - We have used 2024-2025 as a validation period for other work, though never for this strategy.

### 3.7 Tools to measure overfitting

| Tool | Question it answers | Input | Decision rule | Source |
|---|---|---|---|---|
| Trial ledger | How many configurations were tried? | Every configuration ever run, including failures, with its daily net P&L on a common calendar (construction rules in P0a) | Required input for everything below | [26][27][29] |
| Effective number of trials | How many *independent* trials? | Average pairwise correlation ρ̄ of the daily P&L series, M trials | N̂ = ρ̄ + (1-ρ̄)·M | [27] |
| Expected max Sharpe / minimum backtest length | How high would noise alone push the best result? | N̂, cross-trial variance of SR, years of data | A candidate must clearly exceed this | [27][28] |
| Deflated Sharpe ratio (DSR) | Is the selected Sharpe significant given the search and non-normal returns? | Daily SR, skew, raw kurtosis, T, N̂, V[SR] | DSR = Φ[(ŜR-SR₀)√(T-1)/√(1-γ₃ŜR+((γ₄-1)/4)ŜR²)]; require ≥ 0.95 | [27] |
| PBO via CSCV | Does the in-sample winner tend to fall below the out-of-sample median? | T×N matrix of daily P&L; S = 16 blocks (about one per year) gives C(16,8) = 12,870 splits | Reject a family if PBO > 0.05 (the threshold is our choice). Also report the in-sample/out-of-sample degradation slope and the probability of an out-of-sample loss. Never optimize on PBO. Applies only to families with two or more variants selected on in-sample data. | [26] |
| White's Reality Check | Does the best model beat the benchmark? | Daily P&L differences vs a benchmark; stationary bootstrap | Loses power when many poor variants are included | [31] |
| Hansen's SPA (preferred) | Same question, studentized and robust to junk variants | As above; report SPA_l, SPA_c, SPA_u | p ≤ 0.05 on SPA_c | [32] |
| Romano-Wolf StepM | *Which* configurations beat the benchmark, with familywise error control? | Studentized, block bootstrap, at least 1,000 resamples | Test several block lengths | [33] |
| Holm / BHY haircuts | Multiple-testing-adjusted p-values and a haircut Sharpe | p-values of all trials (HAC t-statistics on daily P&L) | t ≥ 3; the haircut is nonlinear | [29][30] |
| False discovery rate (FDR+) and persistence | What share of selected rules are false? Do the selections persist? | Bootstrap p-values; overlap of selected sets between windows (the Jaccard measure is the researcher's suggestion) | Near-zero persistence means the selection is noise | [15] |
| Model-based bootstrap (synthetic null) | How much "profit" does the *whole pipeline* find in data with no signal? | Synthetic ES/NQ paths with zero drift and with drift preserved (generators in P0d) | Real results must beat the distribution of the best null result | [9] |
| Pre-registration checklist | Was the research process itself sound? | Written protocol before data are touched | Every experiment in Section 7 follows it | [83] (added in review) |

**Bootstrap settings and benchmarks:**
- **Bootstrap.** Use a stationary or circular block bootstrap on **daily** P&L.
  - The notes conflict on White's setting. One note says White used q = 0.5 on S&P daily data. The White verifier note says the paper's illustration used q = 0.1. Check the paper before relying on either value.
  - Hansen used q = 0.25.
  - A 5-20 day mean block is the researcher's suggestion [31][32][33].
- **Software.** Python's `arch` package implements SPA, StepM and MCS (as noted in the implications for [10]).
- **Benchmarks that separate entry skill from beta and from exit design:**
  - (a) zero;
  - (b) random entries with the same exits and the same long/short mix;
  - (c) long-only random entries, or exposure matched to NQ beta [31].

### 3.8 Applying the tools to our five experiments

| Our experiment | Trials to log | Test | What the literature predicts |
|---|---|---|---|
| (1) Hand-written rules | Every parameter set tried | SPA vs zero and vs random entries with the same exits; DSR | Not significant [10][16] |
| (2) 43,457-condition scan | 43,457 × 4 horizons = 173,828 columns | FDR+ / BHY; survivor count on a drift-preserving synthetic null; persistence across windows | Few independent discoveries. Survivors reflect a common, regime-dependent 2019-2025 factor, not persistent edges [15][16]. |
| (3) Per-state stop/target (81 × 48) | 3,888 per entry type, selected as 81 per-state maxima | CSCV with the per-state selection procedure (P0b); null-pipeline comparison (P0d) | PBO far above 0.5 and a negative degradation slope [26] |
| (4) Boosted trees | Features × pairs × thresholds × windows × instruments × bar size | Walk-forward out-of-sample daily P&L as the matrix columns; PBO across setups; SPA vs random entries with the same exits; StepM separately for ES/NQ and for 2010-2018 vs 2019-2026; volatility-normalized informativeness test (P0i) | High PBO; not significant [32][33] |
| (5) Classic setups on ES (profit factor 0.72-0.88) | All variants | SPA (the losing variants would weaken a plain Reality Check) | Not significant [13][32] |

---

## 4. Methodology fixes for the ML pipeline

1. **Make fewer, sparser decisions.** Decide at fixed clock times (for example :00/:30, as in [7]) or on volatility-scaled CUSUM events [34], not on every 1-minute bar. This reduces label overlap and the number of trades that pay costs.
2. **Weight samples by uniqueness.** For each label, average 1/c_t over its life, where c_t is the number of labels alive at bar t. Pass the result as `sample_weight`, or use the sequential bootstrap [34].
3. **Purge and embargo every train/test boundary.**
   - Drop training labels whose outcome window overlaps the test block.
   - Embargo about 1% of T after each test block.
   - Replace the single yearly walk-forward path with combinatorial purged cross-validation (CPCV): 16 yearly groups with k = 2 give 120 splits and 15 backtest paths [34].
   - Purge at least the full label horizon, 2 hours for our current labels. This is our recommendation, motivated by [34][38].
4. **Remove hidden leakage.**
   - **Early stopping.** sklearn's `HistGradientBoostingRegressor/Classifier` turns on early stopping automatically above 10,000 samples. By default it uses a random (shuffled) validation split, and with overlapping labels that split leaks. Set `early_stopping=False`, or supply a purged, time-ordered validation block [34].
   - **Nest the threshold tuning** [34]:
     - fit on years up to k-1;
     - predict year k and tune the threshold on it;
     - refit, then test on year k+1.

     At present the threshold is tuned on a year the model was trained on.
5. **Labels.**
   - **Fix the barriers in advance.** Our stop/target dollar outcomes already are triple-barrier labels [34]. Fix 1-3 barrier pairs in advance, in units of forecast volatility, rather than per state. If state-dependent brackets are wanted, derive them from a fitted process [79][80], not a grid.
   - **Add time-exit and trailing-exit labels.** The evidence that fixed targets cut off the rare large days that pay for breakouts is suggestive but weak:
     - In [22], an end-of-day exit beat 1-10R targets, but only in one in-sample heatmap on TQQQ, with ATR-based stops and no slippage. The paper's own headline rule used a 10R target.
     - Take-profit rules lowered performance relative to a stop alone in [24] (no costs mentioned).
     - Winners lasted several times longer than losers in [18].
   - **Express outcomes in units of volatility at entry** [71].
   - **Handle releases.** Cut labels at the next scheduled release (our recommendation, motivated by the release-minute evidence in [49][51]). Remove jump intervals from training targets, or model them separately [39].
6. **Model choice.**
   - **Use shallow, regularized trees.**
     - In Gu-Kelly-Xiu, trees average fewer than 6 leaves and neural nets peak at 3 layers [35].
     - In sklearn terms: `max_leaf_nodes` 4-8, depth 2-3, `min_samples_leaf` in the hundreds or thousands, and a nonzero `l2_regularization`.
   - **Run a linear baseline.** Fit an elastic-net / LASSO baseline on the same features [35][39]. If the boosted model does not beat it under purged CV, its "nonlinearity" is fitting noise.
   - **Use a diverse ensemble** (random forest, shallow boosted trees, elastic net) [36].
   - **Pool ES and NQ** with instrument-agnostic, normalized features [45][71].
7. **Features.**
   - **Add:**
     - normalization by time-of-day volatility [66][6];
     - the noise-band quantities: move from the open divided by σ at that clock time, whether price is beyond the band, distance to VWAP, prior-day NR4/NR7 [7];
     - daily features, all computed from the 16:00 RTH close: prior close to 10:00, 15:00-15:30, and prior close to 15:30 [1][2];
     - a ladder of lagged returns plus the overnight gap. The 1-120 minute range is our recommendation, motivated by the lagged-return features in [36];
     - an event calendar with exact timestamps (Section 5.5);
     - cross-asset lags: NQ ↔ ES and SPY/QQQ/IWM/DIA [48][40]. Most price discovery happens in the E-mini [82], so expect the ETFs to lag ES/NQ, not lead them;
     - bar-based liquidity measures (Amihud, Roll, Kyle's lambda) [38]. Treat bar-derived signing and VPIN with suspicion [44].
   - **Make features stationary.** In Kolm et al., the stationarity of inputs mattered more than the model architecture [47]. Compute percentage-based features from unadjusted per-contract prices (Section 5.6).
   - **Drop:** same-clock-time-yesterday direction features [6][2] and raw EMA levels.
8. **Feature importance.** Use out-of-sample permutation importance (MDA) on purged test folds, not in-sample gain or MDI. Features with strong in-sample explanatory power can have little predictive power [38][34].
9. **Meta-labeling.** Code the trader's EMA 8/20/50 plus Momentum(14) rule as the primary model that picks the side. A secondary classifier then decides take/skip and size [34].
   - It can only filter, so it cannot rescue a primary rule that is about zero before costs.
   - Judge it on after-cost P&L, not accuracy.
10. **Distill the model.** Reduce the top-1% trades to a depth-2 surrogate tree or a simple rule. Then test that rule and its mirror image directly. A long-only edge with no short-side counterpart is probably beta [37].
11. **Metrics.**
    - Report out-of-sample R² against a *zero* forecast at 1/5/15/30/60/120 minutes, which gives the "alpha term structure" [47][35].
    - Test informativeness before profitability, using volatility-normalized outcomes against matched random entries (P0i) [11].
    - Compare buy-signal and sell-signal returns against the unconditional mean [9].
    - Report gross bp per trade first, plus the break-even cost in ticks [15][17].
    - Break results down by year and by regime [16][3].
12. **Train with costs.** Tune thresholds with 1.5-2 times the modeled costs, then evaluate out of sample at 1 times. This is our recommendation, motivated by the cost sensitivity in [17][13].
13. **Test execution delay.** Fill one or two bars late. If the edge flips sign, it was a microstructure artifact [10][8].

---

## 5. Costs, execution and event days

### 5.1 Literature effect sizes against our costs

Our round-trip costs are about 1.2 bp on MES and about 0.5 bp on MNQ, and about 2.0 bp and 0.7 bp for overnight fills.

How to read the table:
- All conversions to points, dollars and cost shares are our arithmetic and assume the bp effect transfers unchanged to futures at today's index levels.
- "Gross" is the pooled historical figure.
- Most of these effects were concentrated in crisis or high-VIX years, so the pooled figure overstates expected value in calm years. Where the notes give conditional numbers, they are shown.

| Effect | Gross per trade in the literature (pooled) | ≈ ES points / $ per MES | Cost as share of gross: MES / MNQ | Conditional evidence in the notes | Status |
|---|---|---|---|---|---|
| Last half hour, signed by prior close to 10:00 [1] | about 2.6 bp | 1.7 points / $8.5 | 47% / about 19% | Stronger on high-volatility days (no split figures in the notes) | Decayed [3]; our SPY test negative |
| Last half hour, signed by prior close to 15:30 [2] | about 2.7 bp | 1.75 points / $8.8 | 46% / about 19% | Slope 6.63 when dealers are short gamma vs 0.82 (not significant) when long | Never tested by us; evidence ends May 2020 |
| Overnight 2-3 am drift [4] | 1.48 bp/day | 1.0 point / $4.8 | **135%** (overnight cost $6.50) / about 47% if NQ's drift equals ES's in bp (not reported) | Per one-SD more negative closing imbalance: about 2.6 bp at VIX 20 (1.7 points / $8.5) and 6.1 bp at VIX 30 (4.0 points / $19.8) | Plain version negative after costs in 2004-2020; about 0 in 2021-25 |
| Noise-band breakout [7] | about 3.6 bp ($0.09/share at an SPY price of about $247; gross or net not stated) | 2.3 points / $11.7 | about 35% before reversal costs / about 14% | By year: +61.1% (2018), +37.2% (2023), +32.2% (2024) vs -12.8% (2016), -6.9% (2017) | Futures post-publication window from Oct 2024 (Feb 2025 strict) |
| Pre-FOMC drift [51] | 49 bp per event (8 a year) | 32 points / $159 | about 2.5% / about 1% | About +31 bp per one-SD higher VIX | About 0 in 2016-19 [54] |
| HFT trading of releases in ES [55] | about 2 bp per event, summed across all traders | n/a | n/a | — | Out of reach at retail speed |
| Common OHLCV signal families on 5-minute MNQ [8] | 0.07-1.5 MNQ points | n/a | Mostly above 100% of gross (our cost 1.0-1.25 points) | — | Mostly below cost |

Conclusions:
- **On paper, against historical gross effects:**
  - **Pre-FOMC drift** clears our costs easily.
  - **The last-half-hour and noise-band trades** clear comfortably on MNQ, where cost is about 15-20% of the edge. On MES they clear only marginally, with cost taking about 35-47% of the edge.
  - **The overnight drift** does not clear on MES unconditionally. Cost is about 135% of the edge, and the plain version was already negative after costs in 2004-2020 [4]. Only the conditional versions (weak close, high VIX) can clear.
- **What binds for each trade:**
  - For FOMC trades, and for the last-half-hour trade on MNQ, the main question is whether the effect still exists.
  - For MES, and for any overnight trade, cost binds as well.
- **Report each effect by volatility regime.** The pooled dollar figures overstate what to expect in calm years. Every experiment in Section 7 reports results per volatility tercile.
- **Short-hold scalps cannot clear costs:** at 15-30 minute horizons the gross edge is a fraction of a point.

### 5.2 Break-even correlation by horizon (our arithmetic; applies only to a sign trade held to a fixed horizon)

- **Formula.** Suppose a forecast has Pearson correlation ρ with the forward return over horizon h. Take the forecast's sign and hold to h with no stop and no target. With normal returns, the expected gross profit is about 0.8·ρ·σ_h per trade, where σ_h is the standard deviation of the h-horizon return.
- **Volatility assumptions:**
  - **ES.** At 16% annualized and ES 6,500, daily σ is about 65.5 points. If all daily variance fell in the 390 RTH minutes, σ would be about 18 points over 30 minutes and about 36 points over 2 hours.
    - Overnight variance is not zero, so true RTH figures are somewhat lower.
    - Midday is lower still because of the U-shape.
    - The volatility note's figure of 47 points for 2 hours corresponds to about 3.5 hours under these assumptions.
  - **NQ.** At about 1.35 times ES's volatility and NQ 25,000, daily σ is about 340 points: about 94 points over 30 minutes and about 189 over 2 hours.
- **Break-even ρ.** Cost is taken midway between a target exit and a stop exit: about 0.65 point on MES and about 1.1 points on MNQ.

| Instrument | 30 minutes | 2 hours |
|---|---|---|
| MES | about 0.045 | about 0.022 |
| MNQ | about 0.015 | about 0.007 |

- **This arithmetic does not explain our ML results, and we no longer claim it does.**
  - By the table, an out-of-sample ρ of 0.02-0.04 would be clearly profitable on MNQ. Yet the MNQ results were the worse ones (2026 MNQ -$9,740 with one setup).
  - The formula does not apply to our IC. Our 0.00-0.04 is a rank correlation between predicted and realized *dollar bracket outcomes*, with stops, targets and overlapping labels. It is not the Pearson correlation of a forecast with a fixed-horizon return.
  - The table is a target for a correctly measured directional ρ: sign of prediction vs forward return at a fixed horizon, on non-overlapping decisions, clustered by day (P0j).
- **What still holds.**
  - Cost per trade is a fixed number of points, so a larger σ per trade (longer holds, wider brackets) and fewer trades lower the cost share.
  - That is consistent with the models' preference for wide 6/12-ATR brackets. The preference may also reflect selection of high-volatility states (Section 3.1).

**Cost as a share of stop distance** (our arithmetic).

As a guide, keep cost at or below 10-15% of stop distance unless measured edge clearly exceeds it. This threshold is our recommendation, motivated by the cost results for tight stops in [64].

| Instrument | Stop distance | Stop in $ | Cost share at full round-trip cost |
|---|---|---|---|
| MES | 2 points | $10 | 40% |
| MES | 4 points | $20 | 20% |
| MES | 8 points | $40 | 10% |
| MES | 16 points | $80 | 5% |
| MNQ | 8 points | $16 | 16% |
| MNQ | 16 points | $32 | 8% |
| MNQ | 32 points | $64 | 4% |

### 5.3 Execution modeling

- **Fill timing.** Enter at the next bar after the signal, and test sensitivity to 1-2 minute delays.
  - Mesfin's positive control flipped sign with a one-bar delay [8].
  - In [10], a one-day delay cut the best rule's return from 17.2% to 7.8%; the 7.8% rule remained significant.
- **Intrabar ordering.** When a stop and the entry or target fall inside the same 1-minute bar, assume the worst case (from the implications for [21]).
- **Passive limit orders.** Standard microstructure reasoning (adverse selection; not a finding of the papers cited here) says that the passive orders that fill are disproportionately those the market moves through.
  - Simulating passive entries credibly needs queue position.
  - With bar data, assume a fill only when price trades through. That is our current rule for targets.
- **Thin hours** (overnight, lunch, around the 17:00 ET halt). Cost those fills at 2 or more ticks, or exclude them. Apparent intraday edges often sit in thin hours [17].
- **The 16:00 close.** Exit just before 16:00 at market and pay the spread on both legs. Futures traders cannot use the closing auction [1], and the 16:00-16:15 futures segment has no predictability [2].
- **Buying data.** Three options, with costs to weigh against each other:
  - **Trades data,** about $157/yr. This is a project figure, not taken from the papers.
  - **Databento's TBBO schema** [85] (added in review, lightly verified). It gives each trade with the prevailing top of book and a side field: A = sell aggressor, B = buy aggressor, N = none. Implied CME trades may show N. That allows trade signing plus quote-based checks without full MBP-1 data. Its price relative to the $157/yr figure is not verified.
  - **Dealer-gamma history.** Baltussen et al. used SqueezeMetrics GEX. SqueezeMetrics sells DIX/GEX history from 2011; a third-party listing quotes about $720/month, unverified [78]. This would replace the crude 5-day-RSI proxy in P2(d). It is worth buying only if P2's cheaper variants show signs of life.
- **What trades or TBBO data would be worth buying for.** Only three specific tests (Section 7, P9):
  - the closing signed-volume imbalance behind the overnight drift [4];
  - order flow in the 30 minutes before the 10:00 releases [53];
  - a falsification test of signed volume at our horizons [42][48].
- **Limits of trades data.**
  - Trade imbalance explains about half as much of *contemporaneous* price changes as quote-based order-flow imbalance: R² of 32% vs 65% over the same 10-second interval [41]. Full order-flow imbalance needs top-of-book quotes.
  - Sign each trade individually, never at bar level [44].

### 5.4 Order-flow evidence by horizon (why trades data is unlikely to fix 15-120 minute direction)

- **NYSE stocks.** Lagged imbalance predicted returns for up to 30 minutes in 1996 and only up to 5 minutes in 2002. The adjusted R² at 5 minutes in 2002 was 0.28% [42].
- **Full-depth order-flow imbalance aggregated to 1 minute** has a negative out-of-sample R² for the next minute: -0.37% for a stock's own imbalance, and -0.36% for an autoregression on its own returns [48].
- **Deep order-flow models** predict over about 2 average price changes, which is seconds [47].

### 5.5 Event days

- **Release minutes.**
  - The significant response sits almost entirely in the first 5-minute bar after the release [49].
  - **Reaction speed.** Prices react within about 0.1 second (working paper) or 5 ms (published abstract) [55].
  - **Fast-trading profits.** Profits from fast trading in ES were about 2 bp per event and fell every year from 2011 to 2014 [55].
  - A one-SD payrolls surprise moved ES about 0.42% in 5 minutes, against a typical 5-minute SD of 0.12% (2008-2014, working-paper figures) [53].
  - **Conclusion:** do not trade releases. Treat them as risk:
    - stops gap, so 1-tick slippage fails;
    - ATR measured just before the release is too low.
- **Informed drift before releases.**
  - The working paper finds strong drift in 7 of 21 market-moving announcements. It starts about 30 minutes early and is worth about 44-49% of the total move, mostly for the 10:00 releases. The published version reports 9 of 20 and about 40% [53].
  - This drift cannot be traded without knowing the surprise in advance.
  - Treat 9:30-10:00 before ISM, Conference Board confidence and home-sales releases as a separate regime. Flag or block entries from about 9:55 to 10:05.
- **The direction of the response depends on the regime.** Good real-economy news lowered stock prices in the 1998-2001 expansion and raised them in the 2001-02 contraction [49]. Do not hard-code "good data means up".
- **Daily priors:**
  - Announcement days earn 11.4 bp vs 1.1 bp [50]. Part of this sits in the overnight gap for 8:30 releases.
  - Pre-FOMC drift [51], which has decayed [54].
  - FOMC-cycle weeks [52].
  - Unscheduled Fed actions averaged -89.2 bp (15 days, 2001-2009) [50]. Keep hard daily loss limits.
- **Calendar.** Build it with exact timestamps:
  - 8:30 ET: payrolls, CPI, PPI, retail sales, GDP, jobless claims.
  - 9:15: industrial production.
  - 10:00: ISM, Conference Board confidence, existing, pending and new home sales, University of Michigan sentiment.
  - **FOMC statement times** (per the verifier's note on [51]; confirm each meeting from the data):
    - about 14:15 until March 2011;
    - about 12:30 on press-conference days from April 2011 to 2012. Other meetings in that period presumably stayed near 14:15;
    - 14:00 from 2013.
    - The 14:30 press-conference time is background knowledge, not verified against the papers.
  - Every FOMC meeting has had a press conference since 2019 (stated in the notes on [56]).
- **Model rules for event days:**
  - Add features for minutes until and since each release.
  - Truncate label outcomes at the next release, or block entries from about 5 minutes before to 5-15 minutes after it. This is our recommendation, motivated by [49][51].
  - For stops that cross a release minute, model the fill from that minute's actual range, not as 1 tick.
- **Statistical power** (our arithmetic).
  - There have been about 85 FOMC meetings since 2016.
  - With a per-event SD of about 1.2% [51], only drifts above roughly 25-30 bp are detectable.
  - Use event-level bootstraps, and placebo calendars shifted ±1 week.

### 5.6 Futures data engineering (added in review)

Our ES/NQ series are back-adjusted at rolls. That is fine for point-based P&L within one trade. It breaks percentage-based measures, prior-close anchors and session-dependent rules. Every experiment in Section 7 follows these rules.

- **Two price layers.**
  - **Keep the raw contract data.** Keep the unadjusted per-contract bars, the contract code for each bar, and the roll calendar used to build the continuous series.
  - **Compute percentage measures within one contract.** Both ends of each return must come from the same contract. Chain those returns where a continuous series is needed. This covers:
    - the noise-band σ(t) = |Close/Open − 1|;
    - bp returns;
    - daily and intraday realized volatility and the HAR inputs;
    - RSI;
    - Amihud;
    - daily close-to-close σ.
  - **Continuous levels.** Where a continuous level series is needed (for example multi-day EMAs), use ratio (multiplicative) back-adjustment, not additive.
    - Additive adjustment shifts every earlier price by a fixed number of points.
    - In early years (ES near 1,100 in 2010), percentages computed from it are distorted.
- **Roll days.**
  - "The contract traded that day" follows the same roll calendar as the continuous series.
  - Prior-close anchors come from that same contract's prior-day 15:59 bar, never from the expiring contract. This covers C_{d−1} in P1, the P2 signal and the P3 close.
  - Lookbacks that span a roll (the 14-day σ(t), 14-day daily σ, 20-day realized volatility, HAR's 22-day component) use per-day quantities, each computed within that day's contract.
  - A daily return on a roll day uses the new contract's own prior close.
- **Session structure.** Build a session calendar from the bars themselves (first and last bar, and missing minutes, for each date). Flag:
  - the daily 17:00-18:00 ET halt and the Sunday 18:00 ET open;
  - the 16:15-16:30 ET halt that existed until 2021. Take its exact end date from the data: it is the date when the 16:15-16:29 bars stop being missing;
  - holiday closures and early-close days. The cash close is 13:00 ET; take the futures close time from the data;
  - RTH days with abnormal gaps. Exclude them and log each exclusion.
- **Timestamps.**
  - Bars are stamped at their open, in UTC. Convert with a time-zone database.
  - "The price at 10:00" is the close of the 09:59 bar. A "next-bar open" fill at 10:00 is the open of the 10:00 bar.
  - Minutes with no trades produce no bar. Carry the last close forward for price levels, with zero volume.
- **DST-mismatch weeks (for P3).**
  - US daylight time runs from the second Sunday of March to the first Sunday of November. UK summer time runs from the last Sunday of March to the last Sunday of October.
  - Between those dates London is 4 hours ahead of New York instead of 5.
  - Examples: in 2025, March 9-29 and October 26 to November 1. In 2026, March 8-28 and October 25-31.
  - Generate the full 2010-2026 list from these rules and store it with the code.
- **VIX.** The project data has no VIX.
  - **Source.** Cboe publishes daily VIX history on its website (not checked in this review). Intraday VIX would need another vendor.
  - **No look-ahead.** Use only values known at decision time:
    - for decisions before 16:15 ET, the prior trading day's close;
    - for overnight decisions, the same day's close.
  - **Fallback.** Where VIX is unavailable, use the realized-volatility tercile defined in the common protocol.
- **SPY/QQQ data.**
  - Most S&P 500 and Nasdaq-100 price discovery occurs in the E-mini [82] (added in review). Expect ETF bars to lag ES/NQ slightly.
  - Scaling them to futures points is fine for 5-minute moves (correlation 0.996 in our check). Do not expect ETF lead-lag features to lead the futures.

---

## 6. Risk, stops, sizing and the human side

### 6.1 Base rates for day-trading skill

- **Taiwan, 1992-2006** [57]:
  - Fewer than 1% of day traders predictably earn positive abnormal returns after fees.
  - The top 500 traders earned 61.3 bp/day before fees and 37.9 bp/day after.
- **Same data, learning study** [58]:
  - 74% of day-trading volume comes from traders with a history of losses.
  - 97% of traders are likely to lose in future day trading.
  - A draft reports that experienced losing traders had a 95.3% chance of day trading again within 12 months.
- **Brazilian mini-index futures, the closest analogue to MES/MNQ** [59]:
  - Of 19,646 people who started in 2013-2015, 1,551 persisted beyond 300 days. Only 11% of those were positive gross, and 3.0% positive net.
  - The best trader's daily Sharpe was about 0.12, which needs about 270 days to reach t = 2 (researcher's calculation).
  - This study is a working paper, partly verified.
- **What this means for the trader's belief that they predict direction well.**
  - It is a hypothesis with a low prior. Test it before building the bot around it (Section 7, P7).
  - Biased learning, where wins count as skill and losses as bad luck, is the documented pattern [58]. Use a timestamped log, not recall.

### 6.2 Holding losers (the disposition effect)

- **Retail investors** realize gains about 1.5 times as readily as losses: PGR 0.148 vs PLR 0.098, confirmed via a secondary source [60].
  - The finding that sold winners then outperformed held losers is confirmed. The 3.41% figure over the following year was not re-verified in this pass.
  - Shefrin & Statman's framework (prospect theory, mental accounting, regret aversion, self-control) points to pre-commitment as the remedy [60].
- **Professional floor traders** in futures also hold losers longer. Relative discipline predicted later success, though their sample showed no measurable direct cost of holding losers [61] (abstract only).
- **CBOT T-bond locals with morning losses** were about 16% more likely to take above-average afternoon risk. The prices they set reversed within about ten minutes [62].
- **Human vs algorithmic day traders in Copenhagen** [65]. This is one small working-paper study, partly verified: reportedly 31 algorithmic and 34 human accounts in Danish equities.
  - Humans showed a substantial disposition effect; the algorithmic accounts showed nearly none.
  - Disposition hurt performance (qualitative result only).
  - The specific figures (a 12-point vs 1-point spread, 8-hour P&L) are unverified.
- **Actions:**
  - From the trader's historical fills, compute:
    - PGR and PLR;
    - average loser holding time divided by average winner holding time;
    - average loss divided by average win;
    - the largest loss as a multiple of the median loss.
  - Replay the historical trades with the bot's proposed stop. The bot's value is the loss tail it removes, minus the losers it cuts that would have come back [60][61].

### 6.3 When stop-losses help

- **Theory** [63]. Under a random walk, a stop cannot raise expected return, and it lowers expected return when the strategy has positive drift. A stop adds value only with momentum (losses continue) or a detectable bad regime.
  - The analysis sets transaction costs to zero.
  - Its empirical gains (50-100 bp/month while stopped out, in monthly equities vs bonds 1950-2004) depend on bonds rallying during equity sell-offs. A single-instrument intraday bot has no such alternative asset; its alternative is being flat.
- **Individual US stocks, daily data, 1964-2014** [64]:
  - Tight stops underperform buy-and-hold, mainly because of costs.
  - Wide 10-day stops roughly match buy-and-hold on a risk-adjusted basis by cutting downside volatility. They raise skewness and cut maximum drawdown.
  - Delayed (next-day) execution helps tight stops, because short-horizon moves reverse.
- **Breakout setups.**
  - **Taiwan index futures [24]** (no transaction costs mentioned):
    - Adding a stop to the GA-optimized opening-range breakout raised Sharpe from 1.865 to 2.495 (GA_Sharpe), or from 1.810 to 2.302 (GA_Ret), and reduced drawdown.
    - The often-quoted 1.47 → 2.50 compares the un-optimized benchmark with the optimized stop version, so it mixes the effect of optimization with the effect of the stop.
    - Take-profit rules lowered performance relative to a stop alone.
  - **TQQQ [22].** In one in-sample heatmap (ATR-based stops, no slippage), holding to the close beat 1-10R targets. The paper's own headline rule used a 10R target. This is weak evidence either way.
  - **Noise band [7].** The strategy cuts losers mechanically: 37% of trades win, with positive skew.
- **Implications:**
  - **The stop is a risk control.** Set it wide enough that cost is a small share of the stop distance (Section 5.2).
  - **Exits for breakouts.** For breakout-type entries, test trailing or time exits against fixed targets as pre-registered variants. Do not assume either wins.
  - **Measure each signal's "stopping premium":** expected P&L with the bracket, minus expected P&L with a time exit only, after costs.
  - **Check for continuation.** Estimate ES/NQ autocorrelation conditional on a trade being k ATR against the position. Without continuation, a tight stop costs expected value [63].
  - **Holding cap.** A 30-minute holding cap would cut off the right tail that pays for breakout strategies; the literature's candidates mostly hold to the close [7][22]. This is our inference.

### 6.4 Sizing

- **Contracts per trade** = floor(dollar risk budget / (stop distance in points × $ per point)).
- **Set the stop from a forecast of σ over the holding period,** not from a lagging 14-bar ATR.
  - Combine a HAR daily forecast [67][81] with the intraday profile [66].
  - A 14-bar ATR at 9:31 is built from quiet pre-open bars. At 12:30 it still carries the open's volatility.
- **What volatility targeting does.** It reliably reduces volatility-of-volatility and tail risk [70]. Sharpe gains are fragile out of sample [69].
- **Test the mechanism on our own trades** [68]:
  - Bucket trades by forecast σ at entry.
  - If mean P&L stays flat while variance rises with σ, sizing by 1/σ helps.
  - If mean P&L rises in proportion to σ (common for breakouts), it does not.
- **Volatility scaling multiplies an edge; it cannot create one.**
- **Account size decides whether sizing can vary at all** (our arithmetic).
  - One MES is about $32,500 notional and one MNQ about $50,000.
  - With a 2% daily volatility target and daily σ near 1%, leverage is about 2×. A $25k-50k account then holds 1-3 MES, and rounding makes constant and volatility-targeted sizing nearly identical.
  - **In every sizing test:** state the equity used, and report how often the contract count actually changes.
  - P1 and P6 use a $100,000 research equity (about 6 MES or 4 MNQ at 2× leverage) alongside the trader's actual equity.
- **Practical details:**
  - Prefer 1/σ over 1/σ² for lower turnover.
  - Cap leverage.
  - Simulate rounding to whole micro contracts.
  - Cost is fixed per contract. Low-volatility periods therefore mean more contracts and a larger cost share [70].

### 6.5 Operating rules for a trader who refused to cut losses

- **Stops:**
  - A resting exchange stop on every trade that cannot be widened by hand.
  - Log every manual override.
  - Monitor the bot's own realized-gain vs realized-loss rates to catch overrides creeping in [60][65].
- **Loss limits:**
  - A fixed daily loss cap (for example 3R), after which the bot stops for the day.
  - No increase in size or frequency after losses [62].
  - The daily cap mainly changes variance, not the mean.
- **Kill switches.** Pre-commit to them and write them down before going live.
  - Use a CUSUM or SPRT on per-trade or daily net P&L. This is our recommendation, motivated by the decay evidence in [14] and the skill base rates in [57].
  - Losing traders keep trading at about 95% rates [58], so the switch has to be decided in advance.
- **Promotion:** promote a strategy only on forward paper or small-size results.

---

## 7. Prioritized experiments

### Common protocol (applies to every experiment)

- **Pre-register before running.** Use the Arnott-Harvey-Markowitz checklist [83] as the template. Write down:
  - the specification;
  - the full list of variants (each counts as a trial);
  - the metrics;
  - the acceptance rule.

  Log every run in the trial ledger.
- **Data:**
  - Databento ES/NQ 1-minute bars, June 2010 to Nov 2026, including the overnight session, engineered as in Section 5.6.
  - Compute intraday levels (open, prior 16:00 close, VWAP, ranges) and all percentage measures from the contract actually traded that day, using unadjusted prices.
  - RTH is 09:30-16:00 ET.
  - SPY/QQQ/IWM/DIA 2016-2026 data is used for cross-checks and lead-lag features.
- **Volatility regimes** (defined ex ante):
  - **Variable.** The prior day's Cboe VIX close. Where VIX is unavailable, use trailing 20-day realized volatility from 5-minute RTH returns. Both are known at the prior close.
  - **Cutoffs.** Tercile cutoffs come from an expanding window of all prior days, after a 250-trading-day burn-in (June 2010 to about June 2011, used only to set cutoffs).
- **Report:**
  - gross points and bp per trade first;
  - then net under our cost model: 1 tick per side on market and stop fills, a 1-tick trade-through for targets, $1.50 per round trip, and 2 ticks per side for overnight fills;
  - results per year, per volatility tercile, and for ES and NQ separately and pooled;
  - long and short legs separately, against the unconditional drift.
- **Statistics:**
  - day-level P&L with HAC t-statistics;
  - SPA against zero and against a random-entry control with the same exits;
  - DSR using the effective number of trials from the ledger;
  - PBO only for families with two or more variants selected on in-sample data. PBO is not defined for a single pre-registered replication.
- **Acceptance gates** (our recommendations, combining [8][26][27][30]):
  - **Searched strategies:** day-level net t ≥ 3 for anything selected from a search.
  - **Single replications:** for a single pre-registered literature replication, report the exact t, and treat 2-3 as "promising, needs a forward test".
  - **Sign consistency:** net mean P&L positive in at least two-thirds of out-of-sample calendar years with 20 or more trades. For event strategies with fewer trades, use 2-year blocks.
  - **PBO ≤ 0.05,** where PBO applies.
  - **DSR ≥ 0.95.**
  - **Gross edge vs cost:** mean gross edge at least 1.5 times cost. This is our recommendation, motivated by the gross-vs-friction gap in [8].
  - **Beats the random-entry control.**
  - **Then forward paper trading.**

### P0. Re-score past work and calibrate the pipeline on null data (cheapest and most decisive)

- **Hypothesis.** Experiments (2)-(4) are fully explained by search size, label overlap, and a regime-dependent common factor (bull beta or buy-the-dip). On this view there is no persistent entry edge.

- **(a) Ledger and P&L columns.**
  - **One column per configuration.** A configuration is: signal or condition, side, horizon or bracket, instrument, bar size and data source; for ML setups, also the feature set, threshold and training window.
  - **Within a column, one position at a time.**
    - A signal that fires while a position is open is ignored.
    - No netting of opposing signals, and no pyramiding.
    - Entry is at the next bar's open plus 1 tick; exits follow the configuration's rule under our cost model.
  - **Daily P&L.** Daily P&L is the sum of net P&L of trades that exit that day, on a common calendar of all trading days. Days with no trade count as 0.
  - **Scan columns.** One column per (condition, horizon), with the side fixed by the sign of the condition's discovery-period mean. That gives 43,457 × 4 = 173,828 columns, rebuilt on the original Alpaca data (SPY/QQQ RTH, scaled to futures points), 2016-2026.
  - **Per-state bracket columns.**
    - Random entries are generated once with a fixed seed and shared by every column.
    - Each of the 81 × 48 = 3,888 columns trades those entries only in its own state, with its own bracket.
    - Add the 48 uniform-bracket columns, each applying one bracket in all states.
    - Rebuild on the original data and period, and again on Databento NQ 2010-2026.
  - **Boosted-tree columns.** One column per setup, built from walk-forward out-of-sample predictions only.
  - **Configurations that cannot be regenerated.**
    - List them with whatever summary survived. They still count in M.
    - Compute DSR twice: once with M = the regenerated columns, and once with M = every configuration ever tried, using ρ̄ estimated from the regenerated ones.
    - Decide on the more conservative of the two.

- **(b) CSCV-PBO** [26]:
  - **Scan.** Use S = 10 equal blocks of trading days on 2016-2026, giving C(10,5) = 252 splits.
  - **Databento-based grids.** Use S = 16, giving 12,870 splits.
  - **Boosted trees.** Use S = the number of whole out-of-sample years, rounded down to an even number. For example, 14 years gives 3,432 splits.
  - **Per-state procedure.**
    - In each split, choose the best of 48 brackets in each state on the in-sample half, and sum the 81 selected columns into a composite.
    - The reference set is the 48 uniform-bracket columns plus 1,000 composites with random per-state bracket assignments.
    - PBO is the share of splits in which the composite's out-of-sample Sharpe ranks below the reference set's median.

- **(c) Benchmark tests.** Run SPA (lower, consistent and upper versions) and StepM against the random-entry-same-exits benchmark. Compute DSR for the best configuration [27][32][33].

- **(d) Synthetic null.** Two generators, each run under two drift settings:
  - **Generators:**
    - **G1 (parametric).** 1-minute log return = drift + s(minute of day) × GARCH(1,1) with Student-t innovations.
      - s(·) is the empirical median absolute return by minute of day, with a separate profile for overnight minutes.
      - The GARCH is fitted by maximum likelihood to deseasonalized returns over the full sample, per instrument. A full-sample fit leaks no direction.
      - Bar highs and lows are scaled from the real bar at the same position.
    - **G2 (sign-randomized real bars).** Flip a fair coin for each real 1-minute bar, and reflect the bar around its open when the coin says so.
      - Reflected bar: C' = O − (C − O), H' = O + (O − L), L' = O − (H − O).
      - Bars are chained so that each open equals the previous synthetic close. Volume is unchanged.
      - This keeps the exact volatility, the U-shape, volume and clustering, and destroys any directional predictability.
  - **Drift settings:**
    - zero drift (demeaned);
    - drift preserved: each calendar year's mean 1-minute return, added back as a constant within that year. This is the drift-preserving null that can reproduce bull-beta survivors.
  - **Replications:**
    - **Scan and per-state bracket pipelines:** 200 per generator and drift setting.
    - **Boosted-tree pipeline:**
      - Time one full walk-forward run first.
      - Pre-register at least 20 replications per generator and drift setting.
      - If one run takes more than an hour, run only the single setup with the best real out-of-sample result, not the whole grid.
  - **Statistics compared with the real results:**
    - (i) survivor count after discovery plus validation;
    - (ii) best in-sample net P&L;
    - (iii) in-sample P&L of the per-state composite;
    - (iv) out-of-sample rank correlation of the boosted models, pooled and by year;
    - (v) the top-1% trade minus the average trade.
  - **Empirical p-value** = (1 + number of null runs ≥ real) / (1 + R), where R is the number of replications.

- **(e) Bracket diagnostics on random entries:**
  - **Primary test.** Compare mean gross P&L of random entries under each bracket with the drift-only expectation for the same trades. The drift-only expectation is side × μ × realized holding time, where μ is that year's mean 1-minute return. Test the difference with day-clustered errors.
  - **Secondary (report only).** Among trades that hit a barrier before the time limit, compare the target-first share with s/(s + t + 1 tick). The extra tick reflects the trade-through rule; discreteness will cause small deviations.
  - **Stopping premium.** Compute it as defined in Section 6.3.

- **(f) Execution delay.** Delay the boosted model's top trades by 1-2 bars [10][8].

- **(g) Hour-of-day table.**
  - Mean return per clock hour (ET) for ES and NQ over 2010-2026, from per-contract returns.
  - Split into 2010-15, 2016-20 and 2021-26.
  - Apply a BY correction over 24 hours × 2 instruments × 3 eras [5][4].

- **(h) The "buy after a drop" family:**
  - **Family definition.**
    - The family is every long-side survivor whose condition includes the bottom quintile of any trailing-return feature.
    - If the scan includes other "drop" measures (distance below VWAP or below an EMA), decide whether to include their bottom quintiles before looking at results.
    - Write the cell IDs into the ledger before testing.
  - **Data:**
    - (1) the original QQQ RTH data at the original horizons;
    - (2) Databento NQ 2010-2026, with entries only during RTH and the same horizons, plus a separately measured overnight leg (held from 16:00 to the next 09:30).
  - **Tests.** Each is a trial, run on both data sources: 5 × 2 = 10 tests, Holm-adjusted.
    - even vs odd FOMC-cycle week [52];
    - trend across VIX terciles;
    - RTH vs overnight leg [4];
    - the mirrored short [37];
    - comparison with random long entries at the same times of day in the same years (the beta benchmark).
  - **What each explanation predicts** (ranked as in Section 3.5):
    - **Bull beta plus reversal:** little edge over the random-long benchmark, and a losing mirrored short.
    - **FOMC cycle:** P&L concentrated in even weeks.
    - **Overnight premium:** P&L in the overnight leg, and in 2010-2020 only.

- **(i) Volatility-normalized informativeness test of the boosted models:**
  - **Normalize.** Divide each trade's gross outcome by forecast σ at entry, in points.
  - **Match.** Compare the top-1% predicted trades with random entries matched on state (the 81 states), 30-minute time-of-day bucket and side. Use day-clustered errors.
  - **Report.** Also report the top 1%'s mean σ at entry against the average trade's.

- **(j) Directional correlation.** For each boosted setup:
  - compute the Pearson correlation between the predicted long-minus-short dollar value and the forward return at 30 and 120 minutes, measured from the decision bar's close;
  - use non-overlapping decisions (one per 30 or 120 minutes) and day-clustered errors;
  - compare the result with the break-even ρ in Section 5.2 by instrument.

- **What the literature predicts:**
  - PBO far above 0.5 and a negative degradation slope for the bracket grid.
  - SPA p > 0.1 for the boosted models.
  - The drift-preserving null produces in-sample "profits" and survivor counts close to the real ones. The zero-drift null produces fewer.
  - The top-1% advantage shrinks after volatility normalization.
  - The survivors concentrate in high-volatility periods and 2020-type years, with little edge over random long entries.

### P1. Direct replication of the noise-band breakout [7]

- **Hypothesis.** Breakouts beyond a time-of-day-normalized band, managed with a VWAP/band trailing exit, have positive expectancy in ES/NQ after our costs, including after publication.
- **Specification** (exactly as published, no tuning; all prices from that day's contract, unadjusted):
  - **Band:**
    - For each RTH minute t, move(t, d) = |Close_d(t)/Open_d(09:30) − 1|.
      - Close_d(t) is the close of the bar ending at t; for t = 10:00 that is the 09:59 bar.
      - Open_d(09:30) is the open of the 09:30 bar.
    - σ(t) is the mean of move(t, ·) over the previous 14 full RTH sessions. Half-days are skipped.
    - UB(t) = max(O_d, C_{d−1})·(1 + σ(t)) and LB(t) = min(O_d, C_{d−1})·(1 − σ(t)), with VM = 1.
    - C_{d−1} is the prior session's 15:59 bar close of the same contract. On roll days it is the new contract's own prior-day close.
  - **Decision times:** 10:00, 10:30, …, 15:30. These are the closes of the 09:59, 10:29, …, 15:29 bars.
  - **Entries:**
    - Go long if the decision close is above UB(t), short if below LB(t).
    - Fill at the next bar's open, 1 tick adverse.
  - **VWAP:** RTH VWAP from the 09:30 bar, using each bar's (H+L+C)/3 weighted by volume (our stated choice).
  - **Exits:**
    - At each decision time, exit a long if the close is below max(UB, VWAP), and exit a short if the close is above min(LB, VWAP). Fill at the next bar's open, 1 tick adverse.
    - A break of the opposite band reverses the position. A reversal is an exit plus a new entry: each leg pays 1 tick, and each completed round trip pays the $1.50 commission.
    - Go flat at the 15:59 bar close, 1 tick adverse.
  - **Early-close days.** No entries after 12:30; flat at the 12:59 bar close.
  - **Two pre-registered variants:**
    - (A) as published, with exits checked only at the half-hour;
    - (B) A plus a resting exchange stop at the current trailing level, updated only at decision times.
      - The stop fills 1 tick beyond its price.
      - Re-entry is allowed at the next decision time if the entry conditions hold.
      - This meets the trader's requirement of a stop on every trade.
  - **Sizing:**
    - (i) 1 contract;
    - (ii) volatility-targeted: contracts = floor(E × 0.02 / (σ_d × P × M)), where:
      - E is equity, P the price at entry and M the dollars per point;
      - σ_d is the SD of the last 14 daily close-to-close returns computed within contract;
      - leverage is capped at 4×;
      - a result of 0 means no trade (report how often that happens).

      Run with E = $100,000 and with the trader's actual equity. Report the distribution of contract counts, and the share of trades whose count differs from the median.
  - **Periods:**
    - (1) June 2010 to April 2024: the paper's SPY era, run on futures;
    - (2) May-September 2024: after the SPY sample, but inside the authors' futures FAQ data;
    - (3) **October 2024 to November 2026 (primary)**, untouched by the authors for futures. Report February 2025 to November 2026 as the strict version.

    We have looked at 2024-2025 market data in other work, but never with this strategy.
- **Controls:**
  - random direction at the same decision times, with identical exit logic;
  - long and short legs separately;
  - scrambled days;
  - constant vs volatility-targeted size on the identical trade list.
- **Expected effect size:**
  - **SPY 2007-2024:** about 1.8 trades a day, Sharpe 1.24 at 1×, 37% of trades winning.
  - **Per trade:** about 3.6 bp, or about 2.3 ES points ($11.7 per MES) if gross.
    - MES cost would take about a third of that before reversal costs.
    - On MNQ, cost would be about 14%.
  - **Futures results reported in the paper's FAQ:** S&P Sharpe 1.32, Nasdaq 1.23, costs not stated.
  - **Losing stretches:** -12.8% in 2016 and -6.9% in 2017, followed by +61.1% in 2018, +37.2% in 2023 and +32.2% in 2024 (2024 mostly in-sample through April). January 2025 was -1.2%.
  - **Power** (our arithmetic). Even if the published Sharpe of about 1.24 held exactly, the roughly 2 years of period (3) give t ≈ 1.75. A pass there can only be "promising", and must be confirmed by forward paper trading.
  - **Prior:**
    - positive in high-volatility years, and weak or negative in calm years;
    - plausibly a smaller edge after publication.

    This is practitioner, in-sample evidence, so treat it as a hypothesis.

### P2. Last-half-hour momentum signed by the prior-close-to-15:30 return [2][1][3]

- **Hypothesis.** The sign of the return from the prior 16:00 RTH close to 15:30 predicts the 15:30-16:00 return, mainly on high-volatility or stress days.
- **Specification:**
  - **Signal.** The return from the prior day's 15:59 bar close to today's 15:29 bar close, both from the same contract.
    - On roll days, use the new contract's prior-day close.
    - The signal uses futures prices, so it includes the overnight session.
  - **Entry.** At the 15:30 bar open, 1 tick adverse.
  - **Exit.** At the 15:59 bar close, 1 tick adverse. MES/MNQ trade through 16:00, so this price is fillable.
  - **Early-close days** are excluded.
  - **Pre-registered variants (4):**
    - (a) unconditional;
    - (b) only when realized volatility over 09:30-09:59 (from 1-minute returns) is in the top tercile of its expanding distribution, after a 250-day burn-in [1][75];
    - (c) only on FOMC statement days and CPI release days, from the event calendar [1];
    - (d) only when the 5-day RSI of daily closes (computed within contract) is in its bottom tercile.
      - This is the crude dealer-gamma proxy used in [7]; we have no data on dealer gamma itself [2].
      - GEX history [78] would allow a direct test of the gamma mechanism [73], but costs far more than the trades data.
  - **Diagnostics only** (not used for selection):
    - the effect of a signal-size threshold [3];
    - the next-open reversal of the 15:30-16:00 move [74].
  - Do not re-test the prior-close-to-10:00 signal; it already failed.
- **Evaluation:**
  - **Primary era:** June 2020 to November 2026, which is after both Baltussen's and Rosa's samples.
  - **Secondary eras:** June 2010 to 2013, and 2014 to May 2020.
  - **Multiple testing:**
    - The 8 primary tests (4 variants × 2 instruments, primary era) are Holm-adjusted at 5% familywise.
    - The other 16 cells (2 secondary eras × 4 variants × 2 instruments) are reported with BY-adjusted p-values.
    - All 24 go in the ledger.
  - Report gross bp first, then net.
  - **Power** (our arithmetic):
    - The primary era has about 1,600 days. That gives t ≈ 6 for the historical ES R² of 2.29%, t ≈ 4.0 for R² = 1%, and t ≈ 2.0 for R² = 0.25%.
    - A null result therefore rules out the historical effect size, but not a much smaller one.
- **Expected effect size:**
  - **Historically:** about 2.6-2.7 bp gross. That is about 1.7 ES points ($8.5 per MES) and about 6.7 NQ points ($13.5 per MNQ).
  - **Out-of-sample R²:** ES 2.29% to 2020.
  - **Gamma dependence:** the effect is absent when dealers are long gamma [2]. Whether 0DTE options changed this after 2022 is contested [76][77].
  - **Prior:** about zero unconditionally after 2014 [3]; the conditional variants positive only in stress years.

### P3. Overnight drift after weak closes [4]

- **Hypothesis.** ES/NQ rise during the European-open hour after sell-off closes, more so when volatility is high. Our "buy after a drop" survivors are unlikely to be this premium (Section 3.5), but P0(h) checks that separately.
- **Specification:**
  - **Proxy for the closing imbalance.** The return from the close of the 15:14 bar to the close of the 16:14 bar, in the same contract. The 16:14 bar is the last bar before the pre-2021 16:15 halt, so the same bars work in every year.
    - A weak close is the bottom tercile of an expanding window, after a 250-day burn-in.
    - If the signal day is an early-close day, there is no signal.
  - **Window.** Go long from 07:00 to 08:00 London time:
    - normally the 02:00 bar open to the 02:59 bar close, ET;
    - in the DST-mismatch weeks listed in Section 5.6, the 03:00 bar open to the 03:59 bar close.

    Report the fixed 02:00-03:00 ET clock version as a diagnostic.
  - **Weekends and holidays.**
    - A Friday signal trades Monday's window, inside the session that opens Sunday at 18:00. Report Mondays separately.
    - Skip the trade if the next session is a holiday or shortened session that does not include the window.
  - **Pre-registered variants:**
    - (a) unconditional;
    - (b) weak close;
    - (c) weak close and the signal day's VIX close above 20, or the realized-volatility top tercile if VIX is unavailable;
    - (d) a wider 1:30-3:30 ET window, shifted like the main window in mismatch weeks.
  - **Costs:** 2 ticks per side, plus commission.
- **Go/no-go, stated in advance** (our arithmetic):
  - **MES.** The overnight cost (about $6.50) exceeds the historical unconditional edge (about $4.8). Variant (a) therefore cannot pass on MES. Only (b)-(d) can.
  - **MNQ.** The cost is about 0.7 bp, so (a) could clear on paper if NQ's historical drift matched ES's 1.48 bp. The notes do not report NQ's figure.
- **Evaluation:** per year; 2010-2020 vs 2021-2026; MNQ vs MES.
- **Expected effect size:**
  - **Unconditional:** 1.48 bp/day, about $4.8 per MES. The plain version was already negative after quoted spreads in 2004-2020.
  - **Buy-the-dip version:** after-cost Sharpe of 1.10 (2004-2020).
  - **Conditional:** about 2.6-6.1 bp at VIX 20-30.
  - **2021-2025:** about zero, according to the authors.
  - **Prior:** positive in 2010-2020, about zero afterward.
  - This would be a bot sleeve running outside the trader's normal hours.

### P4. FOMC event trades [51][54][52][56][50]

- **Events.**
  - **Source.** The scheduled FOMC meetings from June 2010 to November 2026, taken from the Federal Reserve's FOMC calendars.
  - **Exclusions.** Unscheduled meetings and intermeeting actions (for example March 3 and March 15, 2020) are excluded and reported separately, as description only.
  - **Statement time T:**
    - 14:15 until March 2011;
    - April 2011 to December 2012: 12:30 on press-conference meetings, about 14:15 otherwise;
    - 14:00 from 2013.

    Confirm each meeting's time from the data (the largest 1-minute move within ±30 minutes of the scheduled time).
- **Specification:**
  - **(a) Pre-FOMC drift.** Long from T minus 24 hours 15 minutes to T minus 15 minutes. For example:
    - 14:00 statements: 13:45 the prior day to 13:45 on FOMC day;
    - 12:30 statements: 12:15 to 12:15.

    Entry is at the open of the first bar; exit at the close of the bar that ends at T−15.

    The RTH-only variant runs from the 09:30 bar open on FOMC day to T−15.
  - **(b) Post-SEP first hour.**
    - **Window.** Long from the open of the bar at T+1 minute to the close of the bar that ends at T+60.
    - **Meetings.** SEP meetings are those the Fed's calendar marks as having a Summary of Economic Projections. Do not use a month rule; the SEP months differed in 2011-2012. Compare with non-SEP meetings.
    - **Stop.** A catastrophic stop at 3 × the forecast σ over 60 minutes, using the event-day profile from P6.
    - **Press conference.** The press conference falls inside this window; report it as part of the result.
  - **(c) FOMC-cycle gate.**
    - Label every trading day by cycle week relative to the statement day (day 0): week 0 = days −1 to 3, week 1 = days 4-8, week 2 = days 9-13, and so on.
    - Report the P&L of buy-and-hold RTH, and of every P1/P2/P5 strategy, by even weeks (0, 2, 4, 6) vs odd weeks. Show the even-week result both with and without week 0, since week 0 contains the pre-FOMC drift.
  - **(d) Placebos.** The same clock windows on dates shifted ±5 trading days.
  - **One pre-registered conditional.** The Cboe VIX close two trading days before the meeting is above its expanding median.
  - **Trials:** (a), (a) RTH-only, (a) conditional, (b) SEP, (b) non-SEP, and (c) for each strategy gated. All are logged.
- **Evaluation:** event-level bootstrap (10,000 resamples), June 2010 to 2015 vs 2016-2026.
- **Expected effect size:**
  - **Pre-FOMC drift:** 49 bp in 1994-2011, indistinguishable from other days in 2016-2019 [54], and about +31 bp per one-SD higher VIX [51].
  - **Post-SEP:** about 56 bp (17 events, partly verified) [56].
  - **Cycle:** even-week days earn about 10-13.6 bp more than odd-week days [52].
  - **Power:** since 2016, only drifts of 25-30 bp or more are detectable.
  - **Prior:** small or zero, except possibly in high-uncertainty years such as 2020 and 2022.

### P5. Opening-range breakout using the first 1-5 minutes [22][25][23][21][20]

- **Step 1, before any P&L is computed.** Compute the empirical distribution of R (the opening candle or range height, in points) by year and instrument. This uses no outcomes, so it does not contaminate the test. It converts R-multiples into dollars:

  expected net $ per trade ≈ gross R-multiple × mean R (points) × $ per point − cost in $.

  This assumes the gross R-multiple does not depend on R's size.
  - **Sanity check (our arithmetic).** In the MQL5 cost-filtered sample, 2.5 points of cost equalled 0.145R (gross 0.147R minus net 0.002R). That implies an average R of about 17 NQ CFD points, pooled over 2015-2026 price levels.
  - **At today's levels.** R is likely larger at today's NQ level. If so, cost is a smaller share of R and the dollar edge per trade is larger.
- **Two rule families, kept separate:**
  - **Family A (Zarattini-Aziz first-candle direction).** For a first k-minute candle (09:30 to 09:30+k):
    - Direction = sign(close − open). A doji means close = open exactly, and gives no trade. A looser doji definition (|C−O| ≤ 10% of the range) is reported as a diagnostic only.
    - Enter at market at the open of the bar at 09:30+k, 1 tick adverse.
    - Place a resting stop at the candle's opposite extreme, filled 1 tick adverse. R = |entry − stop|.
    - Target 10R as a limit with a 1-tick trade-through. Otherwise exit at the 15:59 bar close, 1 tick adverse.
  - **Family B (Tsai-style timely ORB, TORB).** The range is the high and low of the first k minutes. From 09:30+k, place one-cancels-other orders: a buy-stop at the range high + 1 tick and a sell-stop at the range low − 1 tick.
    - The orders are active until 11:00 ET. This window is our choice; Tsai's exact window is unverified.
    - The first fill enters, 1 tick beyond the stop price.
    - The stop goes at the opposite range extreme. The target and the close exit are the same as in Family A.
- **Trials.** The grid is {A, B} × k ∈ {1, 3, 5}, giving 6 trials, plus one exit variant:
  - **Primary:** A5, the published rule.
  - **Secondary:** B1 and B3, the closest match to [21], whose best probe times are unverified.
  - **Reported and counted:** A1, A3 and B5.
  - **Exit variant (counted):** A5 with a time exit only (no 10R target). The evidence on targets vs end-of-day exits is weak (Section 6.3).
- **Cost filter.** Skip trades where R is less than 2 times the round-trip cost in points: 1.6 points on MES, 2.5 points on MNQ [25].
- **Conditioners,** reported but not used for selection:
  - relative volume: first-k-minute volume divided by its 14-day average for the same window [23];
  - prior-day NR4/NR7, and VIX at the prior close [7];
  - gap divided by ATR.
- **Controls:** a random-direction bracket, and the average of both directions [25].
- **Expected effect size:**
  - **NQ CFDs [25].** Full sample +0.131R gross (t = 2.9). Cost-filtered sample (n = 2,638): +0.147R gross and +0.002R net at 2.5 points of cost.
  - **For MNQ.** Our cost of about 1.25 points is half of 2.5. With the same R distribution, cost would be about 0.07R, leaving roughly +0.05-0.08R net. That is a rough linear extrapolation; treat it as a hypothesis.
    - Convert to dollars with the Step 1 formula on our own R distribution before judging it.
    - For illustration only (an assumed mean R, not measured): at a mean R of 40 NQ points, +0.05-0.08R is about $4.00-6.40 per MNQ trade.
  - **For MES.** The replication's SPX cost (0.8 point) equals ours, and SPX was -0.081R net, so expect about zero or negative.
  - **History.** Negative in 2015-17 everywhere [25]. S&P futures opening-range breakouts earned a mean/SD of 0.09-0.18 net [20].

### P6. Volatility-forecasting module and sizing overlay [67][66][70][68][69][81]

- **Specification:**
  - **Daily target.** RTH realized variance (RV) from 5-minute log returns over 09:30-16:00, computed within contract.
  - **Overnight variance.** Overnight RV is the sum of squared 5-minute returns from 16:00 to 09:30, excluding halts. It enters as a separate HAR regressor. A 24-hour RV target is reported as a secondary.
  - **Models.** All are re-estimated daily on a rolling 1,000-day window:
    - **primary:** HAR on RV (daily, 5-day and 22-day components plus the overnight regressor);
    - **secondary:** log-HAR, and HARQ [81] (added in review).
  - **Forecast loss.**
    - QLIKE is the primary loss for daily RV.
    - MSE on log RV and Mincer-Zarnowitz R² are reported for comparison with [67].
  - **Intraday target.** RV from 1-minute log returns over the next 60 and 120 minutes, at each decision time.
    - Forecast = the HAR daily forecast × the share of daily variance that the intraday profile assigns to those minutes. The profile is normalized to sum to 1 over RTH.
    - The per-minute profile comes from the trailing 60 sessions. A separate profile is used for event days.
  - **No-trade filter.** Skip a trade when round-trip cost in points divided by the forecast σ over the planned holding period exceeds 0.05. This is our recommendation.
    - Example: at ES 6,500 with σ over 30 minutes of about 18 points, MES cost of 0.8 point gives 0.044. The filter therefore binds mostly in quiet hours.
    - Thresholds of 0.03 and 0.10 are reported as diagnostics, not selected.
  - **On P1/P5 trades:**
    - compare constant vs volatility-targeted size on identical trade lists, using a paired day-level bootstrap, at $100,000 and at the trader's actual equity. Report how often the contract count changes;
    - set bracket widths in σ units, fixed ex ante.
- **Expected effect size:**
  - daily out-of-sample R² of about 0.6-0.7 (S&P futures 1990-2007) [67];
  - lower volatility-of-volatility and a thinner left tail [70];
  - a small, uncertain Sharpe change: 53 wins out of 103 strategies in [69], and 0.40 to 0.48-0.51 for US equities in [70];
  - no improvement in the mean for strategies with zero edge;
  - little measurable difference at small account sizes, because of contract rounding.

### P7. Forward test of the trader's directional skill (start now; runs in calendar time) [57][58][59][12]

- **Specification:**
  - **Logging.** The trader records each discretionary call (timestamp, instrument, side) *before* entry, via a button in the bot.
    - **During the test, the bot only logs; it places no orders.** If the trader insists on trading during the test, those trades go through the bot at 1 MES with the standard bracket.
    - The test always scores the logged call, never the bracketed fill.
    - Bot trading on the trader's calls (meta-labeling, Section 4.9) starts only after a pass.
  - **Spacing.** Calls on the same instrument less than 15 minutes after the previous scored call are logged but excluded from the primary test. Only one open call per instrument is allowed at a time.
  - **Primary metric (one, pre-registered).**
    - Mean signed 30-minute forward return after that instrument's round-trip cost, in units of the forecast 30-minute σ at the call (from P6).
    - The return is measured from the open of the next bar to the close of the bar 30 minutes later.
    - The test uses day-clustered standard errors.
  - **Secondary (reported, not used for the decision):**
    - sign accuracy;
    - signed returns at 5, 15 and 60 minutes;
    - gross versions of all metrics.
  - **Nulls:** random sides at the same timestamps, and the EMA/Momentum rule's call at the same timestamps.
- **Sample size, pre-registered** (our arithmetic; normal returns, so E|r| ≈ 0.8σ):
  - **Gross.** A 55% hit rate corresponds to a mean signed return of about 0.08σ. That needs about 625 independent calls for t ≈ 2 gross.
  - **After cost on MNQ** (cost ≈ 0.012σ at 30 minutes): about 865 calls.
  - **After cost on MES** (cost ≈ 0.04σ): about 2,000-3,000 calls.
  - **Day clustering.** Multiply by the design effect 1 + (m − 1)·ICC, where m is calls per day and ICC is the within-day correlation. For example, 3 calls a day with ICC 0.1 adds 20%.
  - **Secondary metric.** For sign accuracy alone: about 400 calls to detect 55% and about 1,100 to detect 53%, before clustering.
  - **Instrument.** Calls on MNQ need far fewer observations, so prefer MNQ calls.
  - **Analysis plan.**
    - One pre-registered analysis at the target count.
    - One interim look at 300 calls, for futility only: stop if the primary metric is negative by more than one standard error.
- **Expected.** The base rate of persistent skill is about 1-3%.
  - A pass would justify meta-labeling the trader's own calls (Section 4.9).
  - A fail means the bot should not rely on discretionary direction.

### P8. ML pipeline rebuild with meta-labeling and cross-asset features [34][35][36][38][39][40][48]

As originally scoped, this would be a new search. It therefore gets a fixed trial budget of 12 configurations and one pre-registered primary configuration. All 12 are logged. DSR is computed with N including experiment (4)'s ledger, because the features overlap.

- **Primary configuration:**
  - **Decisions.** At 10:00, 10:30, …, 15:00 ET (11 a day) on ES and NQ, pooled with normalized features. All Section 4 fixes apply.
  - **Side rule.** The trader's rule, codified as follows; confirm it with the trader before freezing it:
    - long if EMA8 > EMA20 > EMA50 on 1-minute closes and Momentum(14) = close − close 14 bars ago > 0;
    - short if the reverse holds;
    - otherwise no trade.
  - **Label.** Triple barrier: stop at 1.0 σ_60, target at 1.5 σ_60, time limit 60 minutes, using P6's forecast σ. The outcome is in σ units, net of cost.
  - **Model.** `HistGradientBoostingClassifier` with:
    - `max_leaf_nodes=6`, `max_depth=3`, `min_samples_leaf=500`;
    - `l2_regularization=1.0`, `learning_rate=0.05`, `max_iter=300`;
    - `early_stopping=False`.
  - **Take/skip rule (no tuned threshold).** Take the trade when the predicted probability of hitting the target first exceeds the bracket's break-even probability, (s + c)/(s + t), where c is cost in σ units. Time exits make this approximate.
  - **Features.** Fixed in advance; no optional blocks:
    - noise-band and time-of-day-normalized features;
    - daily prior-close-to-10:00 and prior-close-to-15:30 returns;
    - the event calendar;
    - cross-asset lags (ES ↔ NQ, SPY/QQQ/IWM/DIA; expect the ETFs to lag [82]);
    - Amihud, Roll and Kyle's lambda from bars.

    Constituent-level features are excluded from this budget. They would be a separately pre-registered test, and only if the primary configuration passes.
  - **Validation.** CPCV with 16 groups and k = 2, a 60-minute purge and a 1-day embargo. Report the alpha term structure (out-of-sample R² against a zero forecast, by horizon).
- **Secondaries (11).** They complete a grid of 2 decision frequencies (30 or 15 minutes) × 2 brackets × 3 models:
  - **Brackets:** the primary bracket, or stop 1σ_120 / target 2σ_120 / 120-minute limit.
  - **Models:** the primary boosted model, an elastic-net logistic model, or an ensemble of random forest, boosted model and elastic net.
- **Acceptance.** Decided on the primary configuration only, under the common protocol. Secondaries are reported with DSR.
- **Expected:**
  - an out-of-sample R² of at most about 0.1% at 15 minutes [39], which is a correlation of about 0.03;
  - after-cost value likely zero or negative on MES;
  - cross-asset gains small and concentrated in crises [40];
  - meta-labeling can only filter trades.

### P9. (Conditional on buying data) ES/NQ trades or TBBO data [42][41][48][4][53][44][85]

- **Specification:**
  - **Data.** Buy the most recent 1-2 years (for example December 2024 to November 2026).
    - Prefer the TBBO schema if its price is close to the trades schema's. It carries a per-trade side field and the prevailing quote [85].
    - Check the trades schema's documentation for an equivalent side field before buying.
  - **Signing.**
    - Sign each trade with the side field: B = buy aggressor, A = sell aggressor.
    - Trades marked N (for example implied trades) are signed with the tick rule on individual trades. Report their share separately.
  - **Signed volume.** Build 1-minute signed volume.
  - **Three pre-registered tests:**
    - (i) Incremental out-of-sample R² of lagged signed volume beyond lagged returns and volume, at 1, 5, 15, 30, 60 and 120 minutes.
      - Expanding-window estimation with monthly refits, after a 6-month initial window.
      - Non-overlapping targets at each horizon.
      - Clark-West test for nested models, with HAC errors.
    - (ii) The closing signed-volume imbalance (15:15-16:15) as the P3 signal.
    - (iii) Signed volume over 09:30-09:59 vs the 10:00-10:05 return, on ISM, Conference Board and home-sales days.
  - **Continuation rule.** Continue only if, at the same horizon (15 or 30 minutes), the one-sided Clark-West p-value is below 0.025 in each of the four instrument-years (2 instruments × 2 years). The 0.025 level is a Bonferroni correction over the two horizons.
- **Expected.** Predictive content only within minutes:
  - NYSE 2002: adjusted R² of 0.28% at 5 minutes [42];
  - negative out-of-sample R² for the next minute at 1-minute aggregation [48];
  - trade imbalance explains about half as much of *contemporaneous* price changes as quote-based order-flow imbalance [41].

  This is a falsification test, not an alpha source.

### P10. (Added in review; low priority) Institutional rebalancing flows [84]

- **Status.** Read so far at abstract and press-coverage level only. Before pre-registering, take the exact signal and holding window from the full paper:
  - the calendar month-end and threshold-rebalancing triggers;
  - the stock-bond relative-performance measure.
- **Specification:**
  - a daily-hold sleeve on ES/MES, with at most 4 variants, all logged;
  - costs at 2 ticks per side when the hold spans the overnight session;
  - evaluation per year and per volatility tercile, under the common protocol.
- **Prior:** unknown. It fits the structural-flow thesis. Like the other published flow effects, it may have weakened once publicized.

### Suggested order

1. **P0 and P7 first,** in parallel. P0 is cheap and guards everything else; P7 needs calendar time.
2. **P1 and P2:** the precisely specified replications with clean or informative windows.
3. **P6:** needed for risk control whatever happens.
4. **P5.**
5. **P3 and P4.**
6. **P8.**
7. **P9.**
8. **P10.**

---

## 8. References

**Status labels:**
- "Verified" is the verifier's status: yes, or partly (only abstract, secondary or working-paper evidence was checked). Read depth is also noted.
- Entries [73]-[85] were "added in review, lightly verified". They were supplied during review and checked at most at abstract or listing level.
- Published versions may differ from the working papers that were read.

**A. Intraday momentum and where returns accrue**
1. Gao, L., Han, Y., Li, S.Z., Zhou, G. (2018). Market intraday momentum. *Journal of Financial Economics* 129(2):394-414. https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414 (Dec 2015 working-paper full text: https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf). Verified: yes; working-paper full text.
2. Baltussen, G., Da, Z., Lammers, S., Martens, M. (2021). Hedging demand and market intraday momentum. *JFE* 142(1):377-403. https://academicweb.nd.edu/~zda/intramom.pdf. Verified: partly. Costs are discussed only qualitatively. Correction: currency futures are not significant in 2000-2020. Data end in May 2020.
3. Rosa, C. (2022). Understanding intraday momentum strategies. *Journal of Futures Markets* 42(12):2218-2234. https://econpapers.repec.org/RePEc:wly:jfutmk:v:42:y:2022:i:12:p:2218-2234 (excerpt: https://law-journals-books.vlex.com/vid/understanding-intraday-momentum-strategies-1049461706). Verified: yes, at abstract-plus-excerpt depth. No numbers available; cost treatment unknown.
4. Boyarchenko, N., Larsen, L.C., Whelan, P. (2023). The overnight drift. *Review of Financial Studies* 36(9):3502-3547; plus "The Disappearing Overnight Drift," Liberty Street Economics, July 2026. https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf ; https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/. Verified: yes (staff-report version).
5. Lou, D., Polk, C., Skouras, S. (2019). A tug of war: Overnight versus intraday expected returns. *JFE* 134(1):192-213. https://personal.lse.ac.uk/polk/research/TugOfWar.pdf. Verified: yes. Applying it to intraday features is an extrapolation.
6. Heston, S.L., Korajczyk, R.A., Sadka, R. (2010). Intraday patterns in the cross-section of stock returns. *Journal of Finance* 65(4):1369-1407. https://arxiv.org/abs/1005.3535. Verified: yes.
7. Zarattini, C., Aziz, A., Barbon, A. (2024, rev. Feb 2025). Beat the Market: An effective intraday momentum strategy for S&P500 ETF (SPY). Swiss Finance Institute RP 24-97 / SSRN 4824172. https://alexandria.unisg.ch/server/api/core/bitstreams/a99aba00-f967-49b3-aceb-f544dc386e0b/content (also https://concretumgroup.com/wp-content/uploads/2026/02/Beat-the-Market.pdf). Verified: yes. Practitioner, in-sample, not peer-reviewed. The Feb 2025 revision's futures FAQ uses data through Sep 2024.
8. Mesfin, M. (2026). Structural limits of OHLCV-based intraday momentum signals in MNQ futures. arXiv 2605.04004. https://arxiv.org/abs/2605.04004. Verified: partly. Single-author preprint. Its implication that only 60-75 minute holds cleared friction is overstated.

**B. Technical analysis and its decay**
9. Brock, W., Lakonishok, J., LeBaron, B. (1992). Simple technical trading rules and the stochastic properties of stock returns. *Journal of Finance* 47(5):1731-1764. https://econpapers.repec.org/RePEc:bla:jfinan:v:47:y:1992:i:5:p:1731-64. Verified: partly (abstract; numbers via Park & Irwin).
10. Sullivan, R., Timmermann, A., White, H. (1999). Data-snooping, technical trading rule performance, and the bootstrap. *Journal of Finance* 54(5):1647-1691. https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Sullivan_Timmermann_White.pdf. Verified: yes.
11. Lo, A.W., Mamaysky, H., Wang, J. (2000). Foundations of technical analysis. *Journal of Finance* 55(4):1705-1765. https://www.nber.org/papers/w7613. Verified: yes (NBER version).
12. Park, C.-H., Irwin, S.H. (2007). What do we know about the profitability of technical analysis? *Journal of Economic Surveys* 21(4):786-826. https://ideas.repec.org/a/bla/jecsur/v21y2007i4p786-826.html. Verified: yes (abstract plus the 2004 working paper).
13. Park, C.-H., Irwin, S.H. (2010). A reality check on technical trading rule profits in the U.S. futures markets. *Journal of Futures Markets* 30(7):633-659. https://ageconsearch.umn.edu/record/19039/files/cp05pa01.pdf. Verified: yes (2005 conference version). Reports returns, not profit factors.
14. Neely, C.J., Weller, P.A., Ulrich, J.M. (2009). The adaptive markets hypothesis: Evidence from the foreign exchange market. *JFQA* 44(2):467-488. https://files.stlouisfed.org/files/htdocs/wp/2006/2006-046.pdf. Verified: yes.
15. Bajgrowicz, P., Scaillet, O. (2012). Technical trading revisited: False discoveries, persistence tests, and transaction costs. *JFE* 106(3):473-491. https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Bajgrowicz_Scaillet.pdf. Verified: yes.
16. Marshall, B.R., Cahan, R.H., Cahan, J.M. (2008). Does intraday technical analysis in the U.S. equity market have value? *Journal of Empirical Finance* 15(2):199-210. https://ideas.repec.org/a/eee/empfin/v15y2008i2p199-210.html. Verified: yes for the headline. Counts come from a secondary summary.
17. Neely, C.J., Weller, P.A. (2003). Intraday technical trading in the foreign exchange market. *Journal of International Money and Finance* 22(2):223-237. https://files.stlouisfed.org/files/htdocs/wp/1999/99-016.pdf. Verified: yes.
18. Schulmeister, S. (2009). Profitability of technical stock trading: Has it moved from daily to intraday data? *Review of Financial Economics* 18(4):190-201. https://econpapers.repec.org/RePEc:eee:revfin:v:18:y:2009:i:4:p:190-201. Verified: yes (WIFO working paper). Internal inconsistency in the trend-following figure (4.8% vs 6.8%).

**C. Breakout strategies**
19. Holmberg, U., Lönnbark, C., Lundström, C. (2013). Assessing the profitability of intraday opening range breakout strategies. *Finance Research Letters* 10(1):27-33. https://ideas.repec.org/a/eee/finlet/v10y2013i1p27-33.html. Verified: partly; table numbers unverifiable.
20. Lundström, C. (2013/2017; IFTA Journal 2019). Day trading returns across volatility states. https://www.diva-portal.org/smash/get/diva2:732318/FULLTEXT02.pdf. Verified: yes (working paper). The IFTA page range is uncertain. Reports returns and mean/SD, not profit factors.
21. Tsai, Y.-C., et al. (2019). Assessing the profitability of timely opening range breakout on index futures markets. *IEEE Access* 7:32061-32071. https://doi.org/10.1109/ACCESS.2019.2899177. Verified: partly. The abstract says the best probe time was "short" for US markets; the specific best lengths and per-market numbers are unverified.
22. Zarattini, C., Aziz, A. (2023, rev. 2025). Can day trading really be profitable? SSRN 4416622. https://concretumgroup.com/wp-content/uploads/2026/02/Can-Day-Trading-Really-Be-Profitable.pdf. Verified: yes. Practitioner; no slippage modeled. The end-of-day-exit comparison is a single in-sample TQQQ heatmap; the headline rule uses a 10R target.
23. Zarattini, C., Barbon, A., Aziz, A. (2024). A profitable day trading strategy for the U.S. equity market. SFI RP 24-98. https://ideas.repec.org/p/chf/rpseri/rp2498.html. Verified: yes. Practitioner co-authors; slippage not modeled.
24. Wu, M.-E., Syu, J.-H., Lin, J.C.-W., Ho, J.-M. (2021). Evolutionary ORB-based model with protective closing strategies. *Knowledge-Based Systems* 216:106769. https://doi.org/10.1016/j.knosys.2021.106769. Verified: yes. No transaction costs mentioned. Stop effect: Sharpe 1.865 → 2.495 (GA_Sharpe), 1.810 → 2.302 (GA_Ret); 1.473 is the un-optimized benchmark.
25. Krueger, T.-p. (2026). The opening-range breakout paper, replicated on five indices: gross reproduced, net zero. MQL5 blog. https://www.mql5.com/en/blogs/post/776235. Verified: yes, via a fetch-tool summary. Practitioner; not peer-reviewed.

**D. Backtest overfitting and multiple testing**
26. Bailey, D.H., Borwein, J.M., López de Prado, M., Zhu, Q.J. (2017). The probability of backtest overfitting. *Journal of Computational Finance* 20(4):39-69. https://escholarship.org/content/qt4w1110bb/qt4w1110bb.pdf. Verified: yes. Internal inconsistencies: 12,780 vs 12,870 splits, and 0.04% vs 4%.
27. Bailey, D.H., López de Prado, M. (2014). The deflated Sharpe ratio. *Journal of Portfolio Management* 40(5):94-107. https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf. Verified: yes.
28. Bailey, D.H., Borwein, J.M., López de Prado, M., Zhu, Q.J. (2014). Pseudo-mathematics and financial charlatanism. *Notices of the AMS* 61(5):458-471. https://carmamaths.org/jon/backtest.pdf. Verified: yes.
29. Harvey, C.R., Liu, Y. (2015). Backtesting. *Journal of Portfolio Management* 42(1):13-28. https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF. Verified: yes.
30. Harvey, C.R., Liu, Y., Zhu, H. (2016). … and the cross-section of expected returns. *RFS* 29(1):5-68. https://www.nber.org/papers/w20592. Verified: yes (NBER version).
31. White, H. (2000). A reality check for data snooping. *Econometrica* 68(5):1097-1126. https://users.ssc.wisc.edu/~bhansen/718/White2000.pdf. Verified: yes. The notes conflict on the bootstrap parameter: q = 0.5 in one note, q = 0.1 per the White verifier. Check the paper.
32. Hansen, P.R. (2005). A test for superior predictive ability. *Journal of Business & Economic Statistics* 23(4):365-380. https://cdr.lib.unc.edu/concern/articles/hd76s214m. Verified: yes (with corrections to the description of the application).
33. Romano, J.P., Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica* 73(4):1237-1282. https://econ-papers.upf.edu/papers/712.pdf. Verified: yes (2003 working paper).

**E. ML methodology for financial time series**
34. López de Prado, M. (2018). The 10 reasons most machine learning funds fail. *Journal of Portfolio Management* 44(6). https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf. Verified: yes. Practitioner essay; condensed from the book.
35. Gu, S., Kelly, B., Xiu, D. (2020). Empirical asset pricing via machine learning. *RFS* 33(5):2223-2273. https://www.nber.org/papers/w25398. Verified: yes (end page corrected to 2273). Monthly cross-sectional stock returns; not comparable with intraday index R².
36. Krauss, C., Do, X.A., Huck, N. (2017). Deep neural networks, gradient-boosted trees, random forests: Statistical arbitrage on the S&P 500. *European Journal of Operational Research* 259(2):689-702. https://www.iwf.rw.fau.de/files/2016/03/03-2016.pdf. Verified: yes.
37. Fischer, T., Krauss, C. (2018). Deep learning with LSTM networks for financial market predictions. *EJOR* 270(2):654-669. https://iwf.rw.fau.de/files/2015/12/11-2017.pdf. Verified: yes.
38. Easley, D., López de Prado, M., O'Hara, M., Zhang, Z. (2021). Microstructure in the machine age. *RFS* 34(7):3316-3363. https://conference.nber.org/conf_papers/f117415.pdf. Verified: partly. Correction: Corwin-Schultz is used for a target, not as a feature.
39. Aleti, S., Bollerslev, T., Siggaard, M. (2025). Intraday market return predictability culled from the factor zoo. *Management Science* 71(9):7731-7751. https://dukespace.lib.duke.edu/server/api/core/bitstreams/db48671f-3684-4569-ada1-4a4ffb8ed258/content. Verified: yes (dissertation chapter).
40. Huddleston, D., Liu, F., Stentoft, L. (2023). Intraday market predictability: A machine learning approach. *Journal of Financial Econometrics* 21(2):485-527. https://ideas.repec.org/a/oup/jfinec/v21y2023i2p485-527..html. Verified: partly (abstract only).

**F. Order flow and microstructure**
41. Cont, R., Kukanov, A., Stoikov, S. (2014). The price impact of order book events. *Journal of Financial Econometrics* 12(1):47-88. https://arxiv.org/abs/1011.6402. Verified: yes. Contemporaneous price impact; not a prediction study.
42. Chordia, T., Roll, R., Subrahmanyam, A. (2005). Evidence on the speed of convergence to market efficiency. *JFE* 76(2):271-292. https://escholarship.org/uc/item/8wb6140g. Verified: yes (working paper).
43. Easley, D., López de Prado, M., O'Hara, M. (2012). Flow toxicity and liquidity in a high-frequency world. *RFS* 25(5):1457-1493. https://papers.ssrn.com/abstract=1695596 (full text: https://www.stern.nyu.edu/sites/default/files/assets/documents/con_035928.pdf). Verified: yes. The authors have a financial interest in VPIN.
44. Andersen, T.G., Bondarenko, O. (2014). VPIN and the flash crash. *Journal of Financial Markets* 17:1-46; companion paper in *Review of Finance* 19(1):1-54 (2015). https://repec.econ.au.dk/repec/creates/rp/11/rp11_50.pdf ; https://repec.econ.au.dk/repec/creates/rp/13/rp13_43.pdf. Verified: partly. Correction: on 1-second bars the tick rule beats bulk volume classification.
45. Sirignano, J., Cont, R. (2019). Universal features of price formation in financial markets. *Quantitative Finance* 19(9):1449-1459. https://arxiv.org/abs/1803.06917. Verified: yes.
46. Zhang, Z., Zohren, S., Roberts, S. (2019). DeepLOB. *IEEE Transactions on Signal Processing* 67(11):3001-3012. https://arxiv.org/abs/1808.03668. Verified: yes.
47. Kolm, P.N., Turiel, J., Westray, N. (2023). Deep order flow imbalance. *Mathematical Finance* 33(4):1044-1081. https://papers.ssrn.com/abstract=3900141 (slides: https://www.northinfo.com/Documents/1087.pdf). Verified: partly; values read from plots.
48. Cont, R., Cucuringu, M., Zhang, C. (2023). Cross-impact of order flow imbalance in equity markets. *Quantitative Finance* 23(10):1373-1393. https://arxiv.org/abs/2112.13213. Verified: yes.

**G. Macro announcements and FOMC**
49. Andersen, T.G., Bollerslev, T., Diebold, F.X., Vega, C. (2007). Real-time price discovery in global stock, bond and foreign exchange markets. *Journal of International Economics* 73(2):251-277. https://repec.econ.au.dk/repec/creates/rp/07/rp07_20.pdf. Verified: yes.
50. Savor, P., Wilson, M. (2013). How much do investors care about macroeconomic risk? *JFQA* 48(2):343-375. https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Draft20111128p_edited.pdf. Verified: yes.
51. Lucca, D.O., Moench, E. (2015). The pre-FOMC announcement drift. *Journal of Finance* 70(1):329-371. https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf. Verified: yes.
52. Cieslak, A., Morse, A., Vissing-Jorgensen, A. (2019). Stock returns over the FOMC cycle. *Journal of Finance* 74(5):2201-2248. http://www.stern.nyu.edu/sites/default/files/assets/documents/cycle_paper_cieslak_morse_vissingjorgensen.pdf. Verified: yes (2015 draft). The "Fed put" share is not checked in the published text.
53. Kurov, A., Sancetta, A., Strasser, G., Wolfe, M.H. (2019). Price drift before U.S. macroeconomic news. *JFQA* 54(1):449-479. https://ecb.europa.eu/pub/pdf/scpwps/ecbwp1901.lv.pdf. Verified: partly. Working-paper numbers differ from the published ones (9 of 20, about 40%).
54. Kurov, A., Wolfe, M.H., Gilbert, T. (2021). The disappearing pre-FOMC announcement drift. *Finance Research Letters* 40:101781. https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html. Verified: yes (text without tables).
55. Chordia, T., Green, T.C., Kottimukkalur, B. (2018). Rent seeking by low-latency traders. *RFS* 31(12):4650-4687. https://www.unsw.edu.au/content/dam/pdfs/business/banking-finance/events/news-events/2021-10-busines-banking-finance-news-events-Low-Latency-Trading-on-Macroeconomic-Announcements.pdf. Verified: yes (working paper).
56. Gu, C., Kurov, A., Wolfe, M.H. (2018). Relief rallies after FOMC announcements as a resolution of uncertainty. *Journal of Empirical Finance* 49:1-18. https://ideas.repec.org/a/eee/empfin/v49y2018icp1-18.html. Verified: partly; the 56 bp and Sharpe 2.10 figures come from a secondary source.

**H. Trader behavior and stop-losses**
57. Barber, B.M., Lee, Y.-T., Liu, Y.-J., Odean, T. (2014). The cross-section of speculator skill: Evidence from day trading. *Journal of Financial Markets* 18:1-24. https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html. Verified: partly (abstract numbers confirmed).
58. Barber, B.M., Lee, Y.-T., Liu, Y.-J., Odean, T., Zhang, K. (2020). Learning, fast or slow. *Review of Asset Pricing Studies* 10(1):61-93. https://ideas.repec.org/a/oup/rasset/v10y2020i1p61-93..html. Verified: partly.
59. Chague, F., De-Losso, R., Giovannetti, B. (2019/2020). Day trading for a living? Working paper (FGV EESP TD 525; SSRN 3423101). https://ideas.repec.org/p/fgv/eesptd/525.html. Verified: partly; not peer-reviewed.
60. Odean, T. (1998). Are investors reluctant to realize their losses? *Journal of Finance* 53(5):1775-1798; with Shefrin, H., Statman, M. (1985), *Journal of Finance* 40(3):777-790. https://doi.org/10.1111/0022-1082.00072. Verified: partly.
61. Locke, P.R., Mann, S.C. (2005). Professional trader discipline and trade disposition. *JFE* 76(2):401-444. https://doi.org/10.1016/j.jfineco.2004.01.004. Verified: partly (abstract).
62. Coval, J.D., Shumway, T. (2005). Do behavioral biases affect prices? *Journal of Finance* 60(1):1-34. https://ideas.repec.org/a/bla/jfinan/v60y2005i1p1-34.html. Verified: partly. The 16% figure is confirmed; the other numbers are unverified.
63. Kaminski, K.M., Lo, A.W. (2014). When do stop-loss rules stop losses? *Journal of Financial Markets* 18:234-254. https://dspace.mit.edu/handle/1721.1/114876. Verified: partly (2008 working paper in full; transaction costs set to zero).
64. Lo, A.W., Remorov, A. (2017). Stop-loss strategies with serial correlation, regime switching, and transaction costs. *Journal of Financial Markets* 34:1-15. https://doi.org/10.1016/j.finmar.2017.02.003. Verified: yes (abstract plus summary depth).
65. Liaudinskas, K. (2019/2022). Human vs. machine: Disposition effect among algorithmic and human day traders. Barcelona GSE WP 1133; Norges Bank WP 6/2022. https://bse.eu/research/working-papers/human-vs-machine-disposition-effect-among-algorithmic-and-human-day-traders. Verified: partly (qualitative results only). A small sample of accounts in Danish equities.

**I. Volatility and regimes**
66. Andersen, T.G., Bollerslev, T. (1997). Intraday periodicity and volatility persistence in financial markets. *Journal of Empirical Finance* 4(2-3):115-158. https://public.econ.duke.edu/~boller/Published_Papers/joef_97.pdf. Verified: yes. Corrections: the 1987 crash period was excluded; the 0.31 absolute-return autocorrelation is for DM-$, not the S&P.
67. Corsi, F. (2009). A simple approximate long-memory model of realized volatility. *Journal of Financial Econometrics* 7(2):174-196. https://statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/Corsi2009JFinEtrics_LMmodelRealizedVola.pdf. Verified: yes. The ARFIMA benchmark uses a full-sample d.
68. Moreira, A., Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance* 72(4):1611-1644. https://amoreira2.github.io/alan-moreira.github.io/VolPortfolios_published.pdf. Verified: yes.
69. Cederburg, S., O'Doherty, M.S., Wang, F., Yan, X.S. (2020). On the performance of volatility-managed portfolios. *JFE* 138(1):95-117. https://www.lehigh.edu/~xuy219/research/COWY.pdf. Verified: yes.
70. Harvey, C.R., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M., Van Hemert, O. (2018). The impact of volatility targeting. *Journal of Portfolio Management* 45(1):14-33. https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf. Verified: yes (tables garbled in extraction).
71. Moskowitz, T.J., Ooi, Y.H., Pedersen, L.H. (2012). Time series momentum. *JFE* 104(2):228-250. https://fairmodel.econ.yale.edu/ec439/jpde.pdf. Verified: yes.
72. Ang, A., Timmermann, A. (2012). Regime changes and financial markets. *Annual Review of Financial Economics* 4:313-337. https://www.nber.org/papers/w17182. Verified: yes (NBER version; invited review).

**J. Added in review, lightly verified**
73. Barbon, A., Buraschi, A. (2020). Gamma fragility. Working paper. https://abarbon.com/papers/gamma-fragility (also https://www.alexandria.unisg.ch/261487). Added in review, lightly verified (abstract level). Aggregate dealer gamma imbalance combined with illiquidity predicts intraday momentum (negative gamma) vs reversal (positive gamma).
74. Barbon, A., Beckmeyer, H., Buraschi, A., Moerke, M. (2022). Liquidity provision to leveraged ETFs and equity options rebalancing flows: Evidence from end-of-day stock prices. SFI RP 22-40; earlier title "The role of leveraged ETFs and option market imbalances on end-of-day price dynamics", SSRN 3925725. https://papers.ssrn.com/abstract=3925725. Added in review, lightly verified. Separates the leveraged-ETF momentum channel from the options delta-hedging channel (which can produce reversal) behind the last-half-hour effect; the pressure reverts at the next open.
75. Li, Sakkas & Urquhart (2022). Intraday time series momentum: Global evidence and links to market characteristics. *Journal of Financial Markets* 57:100619. https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html. Added in review, lightly verified. 16 developed markets, in and out of sample. The effect is stronger when liquidity is low, volatility high, and information arrives discretely.
76. Dim, C., Eraker, B., Vilkov, G. (2024). 0DTE options, dealer gamma and intraday volatility. SSRN 4692190. https://papers.ssrn.com/abstract=4692190. Added in review; secondary summaries only (higher 0DTE gamma goes with lower intraday volatility). The paper was not accessed; verify before use.
77. Brogaard, J., Han, J., Won, P.Y. 0DTE options volume and S&P 500 volatility. Working paper, known only through news coverage: https://www.bnnbloomberg.ca/zero-day-options-are-reordering-the-way-the-stock-market-behaves-1.1921930. Added in review; secondary only (a one-SD rise in 0DTE volume is associated with about 14% higher S&P daily volatility). Verify before use.
78. SqueezeMetrics (Prior Analytics LLC). DIX/GEX history from 2011; data-provider listing: https://nexusfi.com/d/data-providers/squeezemetrics-prior-analytics-llc. Added in review, lightly verified. The price (about $720/month) comes from a third-party listing and is unverified.
79. Carr, P., López de Prado, M. (2014). Determining optimal trading rules without backtesting. arXiv 1408.1159. https://arxiv.org/abs/1408.1159. Added in review, lightly verified.
80. Lipton, A., López de Prado, M. (2020). Closed-form optimal profit-take and stop-loss levels for mean-reverting (Ornstein-Uhlenbeck) trading strategies. arXiv 2003.10502. https://arxiv.org/abs/2003.10502. Added in review, lightly verified.
81. Bollerslev, T., Patton, A.J., Quaedvlieg, R. (2016). Exploiting the errors: A simple approach for improved volatility forecasting. *Journal of Econometrics* 192(1):1-18. https://econpapers.repec.org/RePEc:eee:econom:v:192:y:2016:i:1:p:1-18 (open working paper: https://cris.maastrichtuniversity.nl/ws/files/12579554/1600566.pdf). Added in review, lightly verified. HARQ model; tested on S&P 500 data 1997-2013.
82. Hasbrouck, J. (2003). Intraday price formation in U.S. equity index markets. *Journal of Finance* 58(6):2375-2400. https://ideas.repec.org/a/bla/jfinan/v58y2003i6p2375-2400.html. Added in review, lightly verified. Most S&P 500 and Nasdaq-100 price discovery occurs in the E-mini.
83. Arnott, R., Harvey, C.R., Markowitz, H. (2019). A backtesting protocol in the era of machine learning. *Journal of Financial Data Science* 1(1):64-74. https://papers.ssrn.com/abstract=3275654. Added in review, lightly verified.
84. Harvey, C.R., Mazzoleni, M., Melone, A. (2025). The unintended consequences of rebalancing. NBER Working Paper 33554. https://www.nber.org/papers/w33554. Added in review, lightly verified (abstract and press coverage only).
85. Databento. TBBO schema documentation. https://databento.com/docs/schemas-and-data-formats/tbbo. Added in review, lightly verified. Each trade comes with the prevailing top of book and a side field (A = sell aggressor, B = buy aggressor, N = none; implied CME trades may show N). Pricing relative to the ~$157/yr trades figure is not verified.

**Secondary mentions in the notes (not reviewed as entries; use with caution)**
- Engle & Sokalska (2012), *Journal of Financial Econometrics* 10(1):54-83, intraday volatility components: abstract-level pointer only.
- Briola, Bartolucci & Aste (2025), *Quantitative Finance* 25(7), arXiv 2403.09267: checked by the verifier of [46].
- Garrison, Jain & Paddrik (2019), OFR WP 19-04: exists. The "spillovers fade within about a second" figure is unverified.
- Baron, Brogaard & Kirilenko (2014), CFTC working paper, https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_riskandreturn0414.pdf: cited in the order-flow summary; not separately verified.
- Takahashi (2025), arXiv 2508.06788, E-mini one-second structural VAR: not verified.
- Liu & Stentoft (2023) working paper: secondary summary only, https://www.cxoadvisory.com/calendar-effects/robustness-and-exploitability-of-intraday-stock-return-prediction/.
- Kurov, Sancetta & Wolfe, "Drift Begone!" (2022 draft): exists; journal unconfirmed.
- Cieslak & Vissing-Jorgensen, "The Economics of the Fed Put" (RFS 2021): draft cited by the verifier of [52].
- Ernst, Gilbert & Hrdlicka: abstract and listing only.
- Bessembinder & Chan (1998): numbers only via Park & Irwin [12].