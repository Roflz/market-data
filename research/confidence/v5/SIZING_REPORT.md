# Sizing by forecast move size (volatility): does it help pass the Lucid 25K eval?

Run of 2026-11-09. Rules tested: A1 (MNQ noise-band momentum), A3 (OPEX Friday short, MES+MNQ+MYM), A4 (CPI/NFP 08:30 fade, MNQ), together as portfolio "P1", and A1 alone.
Data: 2018-01-01 to 2025-06-27 (2,088 trades). The locked holdout (2025-06-30 and later) was not touched.
Lucid rules simulated: +$1,250 target, $1,000 end-of-day trailing drawdown locking at $25,100, $600 daily loss limit, 40% consistency (50% also checked), at most 20 micros.

Labels used below:
- **[source]**: backed by a published paper (author and year in brackets; full list at the end).
- **[ours]**: our own assumption or inference, with no published backing.

---

## 1. The answer

**No. Sizing from a volatility forecast did not beat fixed sizing on pass odds, and it did not cut busts. Keep fixed sizing.**

- **Pass odds.** No sizing policy raised them reliably. At 1 to 3 micros, volatility targeting (VT) *lowered* pass odds and *raised* busts:
  - 1 micro: 73.2% pass becomes 63.4%; bust 19.8% becomes 32.6%.
  - 3 micros: 55.5% becomes 47.3% (difference -8.2 points, 95% CI -15.7 to -1.1); bust 40.0% becomes 49.1% (+9.1 points, CI +1.5 to +17.0).
- **Speed.** VT passed more start days within 20 trading days, by about +3 points (3 micros: 13.2% becomes 16.3%; 5 micros: 13.5% becomes 16.8%). It also cut median days to pass by about 5 to 8.
- **Is the speed gain more than luck?** Not proven.
  - On zero-edge random-day "twins" (same rules, random days), VT gained only about 0.2 to 1 point, so part of the real gain is not explained by chance.
  - But after correcting for the 20 tests that were run (Holm 1979), no test came close to significance: the smallest adjusted p was 0.43.
  - Treat the speed gain as **a lead, not a finding**.
- **Speed costs bust risk.** VT's speed comes from taking larger effective size. Theory predicts exactly this: when you have an edge, bigger bets reach the target faster but less often (Dubins & Savage 1965; Browne 1997).

**Recommended sizing rule:** trade a **fixed number of micros, chosen by how much bust risk you accept**. For the best pass odds, use **1 micro fixed, or fixed $150 risk per trade** (sizing that targets a fixed $ risk per trade, with risk measured as the SD of the previous 100 trades, inherited from v3) **[source: Dubins & Savage 1965; Browne 1997, "timid play" maximizes the chance of reaching a target before ruin when the edge is positive. Applying it to Lucid's rulebook is [ours]]**.

---

## 2. Important caveat: the $600 daily limit (found by the skeptic)

The simulator (inherited from v2 `eval_sim`) applies the daily limit by **capping each day's closing P&L at -$600** and stopping new trades once realized losses reach -$600. In real trading, an open position can lose more than that before it closes. The cap therefore erases losses:

| Size | FIXED 3 | VT 3 | FIXED 5 | VT 5 | FIXED 10 | VT 10 |
|---|---|---|---|---|---|---|
| Days whose raw loss was worse than -$600 | 97 | 106 | 199 | 226 | 403 | 416 |
| Erased loss as a share of net P&L | 36% | 33% | 64% | 61% | 108% | 97% |

The raw worst days were -$3,946 to -$11,950. **All pass and bust figures at 2 or more micros in this report are optimistic upper bounds.**

The skeptic re-ran FIXED pass % under three other ways the limit might be enforced. The four values in each cell below are: intraday close / intraday bar-extreme / realized-only with no cap / no limit. The official figure is in brackets.

| Size | Pass % under the other limit models | Official |
|---|---|---|
| FIXED 1 | 70.9 / 70.9 / 72.7 / 72.7 | [73.2] |
| FIXED 3 | 36.6 / 33.4 / 44.3 / 45.5 | [55.5] |
| FIXED 5 | 28.7 / 24.4 / 32.7 / 34.2 | [46.3] |
| FIXED 10 | 24.2 / 18.4 / 23.5 / 28.6 | [51.1] |
| Fixed $150 risk | 77.6 / 77.4 / 79.4 / 79.4 | [79.5] |

- The official table shows 10 micros passing more often than 5. That is **caused by the cap**, not real.
- The two low-size recommendations (1 micro, and fixed $150 risk) hold under every model.

**Action for you:** check Lucid's current rules page.
- Does your LucidFlex 25K have a daily loss limit at all? Third-party pages disagree: some say there is none, others say it is optional.
- If it does, is it checked on realized plus open P&L, and does it close open positions?

Lucid's own help article returned 404, so we could not verify this ourselves.

---

## 3. Comparison table (P1, 40% consistency, every start day from 2018, 1,935 starts, official sim)

"Within 20" means the share of start days that passed within 20 trading days.

| Policy (source) | Size | Pass % | Bust % | Median days to pass | Within 20 % |
|---|---|---|---|---|---|
| FIXED (control) | 1 | 73.2 | 19.8 | 73 | 5.3 |
| VT, volatility targeting (Harvey et al. 2018; Barroso & Santa-Clara 2015; Zarattini et al. 2024) | 1 | 63.4 | 32.6 | 53 | 6.2 |
| FIXED | 3 | 55.5 | 40.0 | 39 | 13.2 |
| VT | 3 | 47.3 | 49.1 | 31 | 16.3 |
| CVT, conditional VT (Bongaerts, Kang & van Dijk 2020) | 3 | 47.6 | 48.4 | 33 | 14.3 |
| CVT down-only [ours, variant of Bongaerts et al.] | 3 | 54.3 | 41.3 | 39 | 13.4 |
| IV, inverse variance (Moreira & Muir 2017) | 3 | 43.9 | 52.3 | 31 | 14.7 |
| EV, edge over variance, Kelly shape (MacLean, Thorp & Ziemba 2010) | 3 | 48.8 | 47.8 | 53 | 8.8 |
| FIXED | 5 | 46.3 | 50.8 | 34 | 13.5 |
| VT | 5 | 48.8 | 49.0 | 28 | 16.8 |
| FIXED | 10 | 51.1 | 47.4 | 30 | 16.9 |
| VT | 10 | 52.0 | 46.5 | 25 | 19.4 |
| Fixed $ risk, $150 (v3 baseline) | about 1.3 avg | **79.5** | **7.6** | 114 | 3.4 |

The pre-registered tests below compare each policy with FIXED at the same size (difference D = policy - FIXED, in percentage points, with 95% CI). The p-values are Holm-corrected across all 20 tests.

| Test | D | 95% CI | Holm p | Twin p |
|---|---|---|---|---|
| VT within-20, 3 micros | +3.13 | +0.63 to +6.15 | 0.43 | 0.020 |
| VT within-20, 5 micros | +3.29 | +0.57 to +6.64 | 0.53 | 0.040 |
| VT pass %, 3 micros | -8.2 | -15.7 to -1.1 | n.s. | |
| VT pass %, 5 micros | +2.5 | -2.2 to +7.4 | n.s. | |
| VT bust %, 3 micros | +9.1 | +1.5 to +17.0 | fails the bust guard | |
| VT bust %, 5 micros | -1.8 | -7.0 to +3.3 | n.s. | |

The other policies did no better:
- CVT: pass -7.9 points at 3 micros.
- CVT down-only: about neutral.
- IV: pass -11.6 points at 3 micros and -28 at 1 micro.
- EV: clearly slower (within-20 -4.4 and -4.2).

**Decision (pre-registered in `v5/PLAN.md`, hash unchanged): no policy beats fixed sizing.**

---

## 4. $ per micro and the speed-versus-bust trade-off across sizes

These figures are for P1, FIXED, from 2018 on, official sim. Average profit was **about $21 per trading day per micro** (FIXED 1: $20.73/day, daily SD $187). A1 alone made **+$7.75 per trade per micro**, net of costs, on about 213 trades a year.

| Fixed micros | Pass % | Bust % | Median days | Within 20 % | Avg $/day | Daily SD $ |
|---|---|---|---|---|---|---|
| 1 | 73.2 | 19.8 | 73 | 5.3 | 20.7 | 187 |
| 2 | 55.8 | 37.7 | 45 | 11.1 | 45.9 | 359 |
| 3 | 55.5 | 40.0 | 39 | 13.2 | 76.8 | 520 |
| 4 | 47.3 | 49.7 | 33 | 13.4 | 109.4 | 682 |
| 5 | 46.3 | 50.8 | 34 | 13.5 | 145.1 | 839 |
| 6 | 49.6 | 48.9 | 34 | 14.5 | 179.6 | 953 |
| 8 | 50.1 | 48.3 | 33 | 16.2 | 248.8 | 1,172 |
| 10 | 51.1 | 47.4 | 30 | 16.9 | 319.5 | 1,393 |

How to read this table:
- Going from 1 to about 4 micros cuts median days to pass from 73 to 33, but bust risk rises from 20% to about 50%.
- Above 4 micros, the table shows no further gain in pass odds, and the apparent flattening comes from the -$600 cap (section 2).
- Under a stricter enforcement of the limit, pass odds keep falling as size grows (for example, FIXED 10 passes only 18 to 29%).

Fixed $ risk across levels shows the same pattern:

| Fixed $ risk | Pass % | Bust % | Median days |
|---|---|---|---|
| $150 | 79.5 | 7.6 | 114 |
| $250 | 55.6 | 35.9 | 55 |
| $400 | 50.2 | 42.7 | 37 |
| $600 | 41.6 | 52.8 | 31 |

Start days from 2022 on (901 starts) are harder than the full period:
- FIXED 1: 46.7% pass, 38.3% bust.
- FIXED 3: 44.5% pass, 45.8% bust.
- Fixed $150 risk: 72.5% pass, 0% bust; the remaining starts were still open, not passed or busted.
- VT was worse than FIXED on pass at every size from 1 to 6 in this window (for example, 3 micros: 35.8% vs 44.5%).

---

## 5. What the skeptic found

A separate reviewer recomputed the headline with independent code. Its numbers match the output files exactly, the Holm-corrected p-values reproduce (smallest 0.4298), and the decision stands. In addition:

1. **The daily-limit cap is generous (blocking for the numbers, not for the decision).** See section 2.
2. **VT's speed gain is robust only at small size.**
   - P1 at 3 micros: +2.6 to +3.6 points within 20 days under every limit model.
   - A1 alone at 50% consistency, 2 to 3 micros: +5.4 to +7.3 points, p ≤ 0.006 under every model.
   - At 5 to 10 micros the gain disappears with intraday liquidation (-0.8 to +0.05 points).
3. **The speed gain was found in selected cells only.**
   - Only 6 of 16 P1 cells had a bootstrap p below 0.05, and 4 of 16 a twin p below 0.05.
   - No P1 cell starting in 2022 did.
   - At 6 to 10 micros, CVT, CVT down-only and IV showed the same speed gain, so it is not specific to VT.
4. **The equal-bust comparison was too kind to VT.**
   - The bust-matched fixed size for VT 5 is FIXED 6 (49.6% pass), not FIXED 4.
   - FIXED 10 beat VT 5 on pass, bust and within-20 alike (official sim).
5. **Integrity checks passed:**
   - The plan was frozen first (17:03:26, before any code or output); its hash is unchanged.
   - Hand-checked forecasts use only data before entry (7 trades, match to 1e-12).
   - Bootstrap p is stable across block lengths 20 to 250.
   - Twins were built correctly.
   - Risk matching held for VT (0.98 to 1.01) but not for CVT, CVT down-only, IV or EV (0.84 to 0.95), as disclosed.
   - One-position-per-market was not enforced: 76 overlapping MNQ trade pairs. P&L is additive, so this does not matter.
6. **No re-test on the same data.** A follow-up test on the same 2018-2025H1 data, chosen after seeing these results, would not be confirmatory (Gelman & Loken 2014). Any confirmation needs unseen data: the holdout, or forward/paper trading.

---

## 6. Why it did not work, in plain words

- **The forecast is good, but it predicts move size, not profit.**
  - Move size per trade is forecastable: rank correlation 0.7 to 0.85 with realized window volatility (models: Corsi 2009; Andersen, Bollerslev & Diebold 2007; Andersen & Bollerslev 1997).
  - But it correlates only 0.3 to 0.45 with a single trade's actual move. One trade is a noisy draw (Andersen & Bollerslev 1998).
  - Volatility sizing mostly evens out dollar risk. It does not add profit.
- **A1 makes more money when volatility is high.**
  - In 2018-2021, mean $ per trade rose from $3.9 to $20.0 across the forecast quintiles, and $ per unit of risk rose from 0.54 to 1.52.
  - Zarattini et al. (2024) report the same for SPY momentum: its Sharpe ratio rises with VIX.
  - Volatility targeting shrinks exactly those trades. (The linear fit was flat, t = -0.19, so this evidence is mixed.)
- **The published evidence is modest.**
  - Volatility targeting reliably cuts tail risk, but gains in Sharpe ratio are small and mostly limited to equities (Harvey et al. 2018).
  - The stronger inverse-variance claim mostly fails in real time (Cederburg et al. 2020; Liu, Tang & Zhou 2019).
  - None of these papers study per-trade intraday sizing under prop-firm rules **[ours: the transfer to Lucid is untested by any source]**.
- **Theory says the only way to raise both pass odds and speed** is to move size toward trades with a higher edge-to-variance ratio (Browne 1997). That requires predicting edge, and the v4 study found direction unpredictable. EV, the policy built on this idea, lost.

---

## 7. Our own assumptions (not from any source)

- The forecast was chosen by its 2018-2021 rank correlation with realized window SD.
  - A1 uses v4 sigma×rv_60 (0.799).
  - A3 uses HAR-log×share (0.829).
  - A4 uses sigma×rv_240 (0.747).
  - The v4 features are our own.
- Policies stayed at base size until 20 prior trades (50 for EV).
- Volatility history starts in 2018 (Bongaerts et al. used 10 or more years).
- CVT leverage cap Lmax = 2; the down-only CVT variant; a linear edge estimate for EV.
- Risk matching in return-volatility units per rule and market.
- Bootstrap block lengths of 20 and 60 days.
- The fixed $ risk baseline uses the SD of the previous 100 trades (from v3).
- The $600 cap model is inherited from v2; see section 2.
- Cushion-proportional sizing (Grossman & Zhou 1993) was declared in the plan but not run.

---

## 8. References

Entries marked "(from memory)" were not re-verified this session.

- Andersen, T.G. & Bollerslev, T. (1997). Intraday periodicity and volatility persistence in financial markets. *Journal of Empirical Finance* 4, 115-158. (from memory)
- Andersen, T.G. & Bollerslev, T. (1998). Answering the skeptics: Yes, standard volatility models do provide accurate forecasts. *International Economic Review* 39(4), 885-905.
- Andersen, T.G., Bollerslev, T. & Diebold, F.X. (2007). Roughing it up: Including jump components in the measurement, modeling and forecasting of return volatility. *Review of Economics and Statistics* 89(4), 701-720.
- Andersen, T.G., Bollerslev, T., Diebold, F.X. & Labys, P. (2003). Modeling and forecasting realized volatility. *Econometrica* 71(2), 579-625.
- Barroso, P. & Santa-Clara, P. (2015). Momentum has its moments. *Journal of Financial Economics* 116(1), 111-120. (from memory)
- Bongaerts, D., Kang, X. & van Dijk, M. (2020). Conditional volatility targeting. *Financial Analysts Journal* 76(4), 54-71.
- Browne, S. (1997). Survival and growth with a liability: Optimal portfolio strategies in continuous time. *Mathematics of Operations Research* 22(2), 468-493.
- Browne, S. (1999). Reaching goals by a deadline: Digital options and continuous-time active portfolio management. *Advances in Applied Probability* 31(2), 551-577.
- Cederburg, S., O'Doherty, M., Wang, F. & Yan, X. (2020). On the performance of volatility-managed portfolios. *Journal of Financial Economics* 138(1), 95-117.
- Corsi, F. (2009). A simple approximate long-memory model of realized volatility. *Journal of Financial Econometrics* 7(2), 174-196.
- Dubins, L. & Savage, L. (1965). *How to Gamble If You Must*. McGraw-Hill. (from memory)
- Gelman, A. & Loken, E. (2014). The statistical crisis in science (the garden of forking paths). *American Scientist* 102(6), 460-465. (from memory)
- Grossman, S. & Zhou, Z. (1993). Optimal investment strategies for controlling drawdowns. *Mathematical Finance* 3(3), 241-276.
- Harvey, C., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M. & Van Hemert, O. (2018). The impact of volatility targeting. *Journal of Portfolio Management* 45(1), 14-33.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2), 65-70. (from memory)
- Liu, F., Tang, X. & Zhou, G. (2019). Volatility-managed portfolio: Does it really work? *Journal of Portfolio Management* 46(1), 38-51.
- MacLean, L., Thorp, E. & Ziemba, W. (2010). Long-term capital growth: the good and bad properties of the Kelly and fractional Kelly capital growth criteria. *Quantitative Finance* 10(7), 681-687.
- Moreira, A. & Muir, T. (2017). Volatility-managed portfolios. *Journal of Finance* 72(4), 1611-1644.
- Politis, D. & Romano, J. (1994). The stationary bootstrap. *Journal of the American Statistical Association* 89(428), 1303-1313. (from memory)
- Zarattini, C., Aziz, A. & Barbon, A. (2024). Beat the market: An effective intraday momentum strategy for S&P500 ETF (SPY). Swiss Finance Institute Research Paper 24-97. Working paper, not peer-reviewed.

Lucid daily-limit mechanics: the Lucid help center article "Daily loss limit" returned 404 and could not be verified. Third-party pages (tradetanto.com, proptradingvibes.com and others) are not authoritative and contradict each other.

Files:
- Plan: `v5/PLAN.md`
- Code: `v5/sizing.py`, `v5/vol.py`
- Outputs: `v5/out/sizing_real.csv`, `sizing_tests.csv`, `sizing_twins.csv`, `sizing_summary.txt`, `vol_corr.csv`
- Trials log: `out/trials.csv` (modules v5-vol and v5-sizing)
