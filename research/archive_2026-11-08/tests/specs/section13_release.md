# Section 13: release-day leads (L1, L2)

Pre-registered before any P&L of L1-on-jobs-days or L2 was seen. Implement EXACTLY as written; ambiguities: most conservative reading, write it down.

Context: the time-of-day study found the 8:30 ET slot spikes only on release days; a CPI-day fade (8:30-8:45 move faded 8:45-9:45) made +$10.66/MNQ trade 2010-2026 on 194 CPI days (in-sample, best of 30 pre-specified tests, not significant). Jobs-report (NFP) days have NOT been examined and are the honest test.

## Major 8:30 release fade (CPI found in-sample; jobs report kept as the untouched test)

### rule
Days: CPI release days, and Bureau of Labor Statistics jobs-report (NFP) days taken from the official release calendar; if only the first-Friday proxy is available, use it. Measure the NQ move from the 8:30:00 ET bar open to the 8:45:00 ET bar open (6:30-6:45 AM Denver, MST in winter and MDT in summer, always 2 h behind ET; Arizona MST: 6:30-6:45 Nov-Mar, 5:30-5:45 Mar-Nov). If that move is nonzero, enter 1 MNQ at the 8:45 ET bar open in the OPPOSITE direction. Exit at the 9:45 ET bar open (7:45 Denver; Arizona 7:45 Nov-Mar, 6:45 Mar-Nov). Primary test: time exit only. Also report, without changing the primary result, a disaster stop at 2x the 8:30-8:45 move beyond entry, fixed now, untested. Costs: $2.00 round trip per MNQ (1 tick slippage each way + $1 commission); mirror on MES at $3.50. Skip the day if a contract roll or a gap of more than 5 minutes falls inside 8:30-9:45. Pass criterion, fixed now: NFP days 2018-2026 (not yet examined separately) show mean net > 0 with t > 2 on MNQ and the same sign on MES; then a forward test on new CPI and NFP days.

### why
It was the largest per-trade result among the 30 pre-specified k15/h60 tests, and the parameters were not chosen by search. It acts at exactly the moment the trader calls 'crazy' (6:30 AM Mountain). There is a plausible mechanism: an overshoot on the first algorithmic reaction to a headline number, partly corrected once the details are digested.

### evidence
NQ CPI k15/h60 fade: +$10.66/MNQ trade over 2010-26 (n=194; iid t 1.69; regression slope t -0.90). 2018-26: +$20.95, median +$21, hit rate 56%, t 1.83, worst trade -$318. Every year 2021-2026 is positive on NQ, and 2022-2026 on ES. Weaknesses: the 5 best trades are 65% of NQ profit; ES nets only +$2.11 (+$6.21 in 2018-26), and the 5 best trades exceed its entire total; 2010-2017 is flat to negative. On the multiple-testing standard it is NOT significant. Treat it as a lead with low statistical power, about 24 events a year.

### trades_per_year
24

### overlap_with_existing
Mostly separate: it trades 8:45-9:45 ET, before the existing strategies act. It overlaps 9:35-9:45 with the 9:35 first-5-minute ORB and the overnight-range breakout on about 24 days a year, so check combined exposure. It is unrelated to the options-expiry Friday short, except on rare CPI/NFP days that are also expiry Fridays.

## Release-day filter for the existing overnight-range breakout (diagnostic, adds no trades)

### rule
Using the existing MNQ overnight-range breakout (range 18:00-9:30 ET = 16:00-7:30 Denver MST/MDT; entries 9:35-15:00 ET = 7:35-13:00 Denver, Arizona 6:35-12:00 Mar-Nov; held to 17:00 ET = 15:00 Denver), pre-register a comparison of per-trade net P&L ($2.00 round trip per MNQ, existing stops unchanged) on major 8:30 release days (CPI and official NFP dates) against all other days. The candidate rule is 'skip the breakout on CPI/NFP days'. Adopt it only if release-day trades are worse with a two-sided p < 0.05 in BOTH 2010-17 and 2018-26. If release days turn out better, record that and do not add size without a separate test.

### why
On release days the overnight range is largely made by the 6:30 AM Mountain data spike, so a breakout of that range means something different from a breakout of a quiet overnight range. The test needs only the existing trade log and adds no new trades, so it costs almost nothing in multiple testing.

### evidence
Mechanism only, with no P&L tested yet. On CPI days the NQ overnight high or low (close-based) is set during 8:30-9:29 ET on 64% of days vs 42% on other days. The CPI 8:30 slot is about 10x normal volatility in 2018-26; first-Friday days are about 6x.

### trades_per_year
24

### overlap_with_existing
It is a filter on an existing strategy and affects about 24 of its trading days a year. The same test could also be applied to the 9:35 ORB.

## Clarifications fixed now (before testing)
- L1 is judged ONLY on jobs-report (NFP) days 2018-01-01 to the latest data: pass = MNQ mean net $ per trade > 0 with t > 2 (plain t of per-trade net $) AND the MES mean net with the same sign. Also REPORT (not judged): NFP 2010-2017, CPI days in both eras (in-sample, for reference), days that are both CPI and NFP counted once, the disaster-stop version, gross vs net, best-5-trades share, by year.
- NFP dates: use the official BLS Employment Situation release dates if you can obtain them (e.g. the BLS 'Employment Situation' archived news release list, https://www.bls.gov/bls/news-release/empsit.htm, via WebFetch). If that fails, use the proxy: the first Friday of the month, EXCEPT when that Friday is a NYSE holiday or the 1st/2nd of the month and the BLS customarily moved it - in proxy mode just use the first Friday that is an NYSE trading day and SAY that the proxy was used. Save the date list you used as nfp_dates.csv in your dir and report its source.
- L2 uses the existing trades in chosen_models_trades.csv (overnight_break rows; also report opening_range rows as a diagnostic). Release day = CPI day (calendar_days.cpi_days()) or NFP day (your list). Compare per-trade net $ on release days vs all other days with a Welch t-test, separately for 2010-2017 and 2018-2026. Adopt-skip condition: release-day trades worse with two-sided p < 0.05 in BOTH eras. Also report R per trade and bp per trade.