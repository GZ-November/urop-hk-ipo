# Long-run and event-window performance

Reference code: `scripts/ipo_metrics.py` (`bhar_panel`, `skew_adjusted_t`,
`bootstrap_skew_adjusted_test`, `wealth_relative`, `calendar_time_portfolio`).

## Contents
1. Which method answers which question
2. BHAR construction
3. Benchmarks
4. Inference for BHAR
5. Calendar-time portfolios
6. Short windows: CAR around lockup expiry and other events
7. Hong Kong data issues
8. Reporting checklist

---

## 1. Which method answers which question

| Question | Method | Why |
|---|---|---|
| What did an investor holding an IPO for T months earn relative to an alternative? | BHAR (event time) | Matches the investor experience (Barber & Lyon 1997). |
| Is there a mispricing exploitable by a trading strategy? Are abnormal returns robust to cross-sectional dependence? | Calendar-time portfolio alpha | Portfolio variance absorbs cross-correlation (Fama 1998; Mitchell & Stafford 2000). |
| Short event (lockup expiry, index inclusion, stabilization end) | CAR over a few days | Model error is small over short windows (Kothari & Warner 2007). |

Report both BHAR and calendar-time results for long horizons: they weight
observations differently (event-by-event vs month-by-month, EW vs VW) and
Loughran & Ritter (2000) show calendar-time VW regressions have low power when
abnormal performance concentrates in hot-issue periods, while Mitchell &
Stafford (2000) show BHAR t-statistics ignoring dependence can be up to ~4× too
large. Agreement is persuasive; disagreement is informative and must be discussed.

## 2. BHAR construction

BHAR_i(T) = Π_{t=1..T}(1 + R_it) − Π_{t=1..T}(1 + R_bench,it)

- **Start date.** t = 1 begins after the first-day close; this excludes the
  initial return. If you compound from the offer price, call it "total return
  from offer" and do not compare with aftermarket BHARs.
- **Horizon.** Months are standard for 12/24/36/60-month studies; daily
  compounding for ≤ 6 months. Use trading days (21/63/126/252) or calendar
  months consistently, and state the convention.
- **Delisting / missing.** Include the delisting return; afterwards let the
  firm earn the benchmark (Lyon, Barber & Tsai 1999). Interior gaps from
  trading suspensions (common in HK) need explicit treatment: flag, compound
  across the gap using the resumption price, or exclude with a count.
- **Maturity.** An IPO whose horizon has not elapsed at the data cutoff is
  immature: exclude it from that horizon, report N per horizon.
- **Aggregation.** Report EW mean and median BHAR, VW mean (weights = market
  value at the start of the horizon), % positive, and the wealth relative
  WR = (1 + mean BHR_IPO)/(1 + mean BHR_bench) (Ritter 1991).

## 3. Benchmarks

Barber & Lyon (1997) identify three biases: new-listing bias (benchmarks hold
firms that list later), rebalancing bias (monthly-rebalanced indices compound
differently from buy-and-hold) and skewness bias (single-firm long-run returns
are right-skewed). Choices, best to weakest for BHAR:

1. **Matched control firm** by size then book-to-market (Barber & Lyon 1997):
   among seasoned firms (listed ≥ 3–5 years, not IPOs in the window) with market
   cap 70–130% of the IPO's, pick the closest B/M. Replace the match if it
   delists. Removes all three biases in random samples.
2. **Size/BM reference portfolio, buy-and-hold** (Lyon, Barber & Tsai 1999):
   compound each constituent from the event date and average, rather than
   compounding a rebalanced index.
3. **Market index** (HSCI total return, or Hang Seng index): simple and
   transparent; suffers rebalancing and new-listing bias; label as
   "market-adjusted", not "abnormal" in the strong sense.

Use total-return (dividend-adjusted) series on both sides. With few HK-listed
seasoned firms in some sectors, relax the size band and document it.

## 4. Inference for BHAR

- **Skewness-adjusted t** (Johnson 1978; LBT 1999):
  t_sa = √n (S + γS²/3 + γ/(6n)),  S = mean/sd,  γ = Σ(x − mean)³/(n·sd³).
- **Bootstrapped t_sa** (LBT 1999): 1,000 resamples of size n/4, centred on the
  sample mean; compare the sample t_sa with that distribution.
- **Cross-sectional dependence.** Overlapping horizons of IPOs listed in the
  same months are correlated; conventional and t_sa statistics overstate
  significance. Remedies: calendar-time portfolio; cluster by listing month in
  a regression of BHAR on a constant; or Jegadeesh & Karceski (2009) tests
  robust to heteroskedasticity and autocorrelation.
- **Non-parametric.** Wilcoxon signed-rank on BHARs and a sign test on
  % positive. Report medians; skewness makes means fragile.
- **Cross-sectional determinants of BHAR**: regress BHAR on characteristics with
  listing-month clustered or HC3 errors; winsorize BHAR only as a robustness step.

## 5. Calendar-time portfolios

Each month form a portfolio of all IPOs listed within the previous 12/36/60
months; regress its excess return on factors:

R_p,t − R_f,t = α + β(MKT − R_f)_t + s·SMB_t + h·HML_t [+ m·MOM_t, + RMW, CMA] + ε_t

- Report EW and VW α with Newey–West or White errors; require a minimum number
  of firms per month (e.g. ≥ 10) and report the average count.
- Hong Kong factors: Kenneth French's Data Library provides **Asia Pacific
  ex Japan** developed-market factors (includes HK) in USD; or construct local
  HK size/BM factors from all HK-listed stocks, excluding recent IPOs from the
  factor portfolios to avoid benchmark contamination (Loughran & Ritter 2000).
  State currency consistency (HKD returns vs USD factors; the HKD peg makes
  this minor but not zero).
- With a single year of IPOs the calendar-time sample is short; say explicitly
  when the method is under-powered rather than reporting it as a null result.

## 6. Short windows (CAR)

For lockup expirations, stabilization end, index inclusion or earnings
announcements after listing:

- Abnormal return AR_it = R_it − E[R_it]. Estimation windows before an IPO
  do not exist; use a market-adjusted model (β = 1) or estimate over a
  post-event window that excludes the event (e.g. days [+30, +150] for a +180
  lockup expiry), and state the choice.
- CAR(τ1, τ2) = Σ AR. Test with the cross-sectional t (Brown & Warner 1985),
  the Boehmer, Musumeci & Poulsen (1991) standardized test (robust to
  event-induced variance) and a rank/sign test.
- Thinly traded small-caps: use Dimson (1979) or Scholes–Williams betas if any
  beta is estimated; flag zero-volume days.

## 7. Hong Kong data issues

- Trading suspensions and long halts; resumption jumps belong in returns.
- Share consolidations/subdivisions and rights issues: use adjusted prices.
- Price floor effects near HK$0.01 tick sizes for penny stocks; minimum price
  filters (e.g. HK$0.10) must be pre-specified.
- H-share vs A-share benchmarks for A+H issuers; A-share market holidays differ.
- Delisting returns are rarely in vendor data: collect the last traded price
  and any liquidation/privatization consideration (privatization offers often
  carry premiums).

## 8. Reporting checklist

N per horizon (and immature/excluded counts) · benchmark definition and data
source · EW mean, median, VW mean, % positive, WR · conventional t, t_sa,
bootstrapped p · calendar-time α (EW, VW) with factor model and min-firm rule ·
delisting and suspension treatment · currency and total-return basis.
