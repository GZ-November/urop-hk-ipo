# Extended 2026 analysis, data fixes and hold-out plan · 2026-09-30

Sample: 106 Main Board ordinary IPOs listed 2026-01-02 to 2026-09-09. Everything below is exploratory.
Scripts: `analysis/extended_analysis_2026.py` (outputs in `analysis/out/extended/`) and `analysis/aftermarket_event_time_2026.py` (`analysis/out/event_time/`).

## 1. Data problems found and fixed

| # | Finding | Status |
|---|---|---|
| 1 | **9903.HK 1M/6M BHR mixed price bases.** Bars are split-adjusted (3-for-1 after listing; first bar 52.27 vs raw day-1 close 156.80) but the master divided adjusted 1M/6M closes by the raw close: 1M showed -63.1% (correct +10.7%), 6M +19.0% (correct +257.1%). | **Fixed.** `aftermarket.py` now puts day-1 close and offer price on the bars' basis when they differ by more than 1% (`price_basis_scale` recorded per issuer; small dividend adjustments are left alone). Regression tests added. 2026Q1 workbook, exports and master regenerated for this issuer only. Table 2: 6-month mean 33.4% -> 41.0% (Wilcoxon p 0.116 -> 0.209), 1-month mean 5.3% -> 6.1%. |
| 2 | **"First 6M" Amihud, volatility, drawdown and zero-volume columns filled for all 106 issuers** although only 31 have a matured 6-month window (Q2/Q3 values came from about a week of bars). | **Fixed.** New `tools/blank_immature_window_stats.py` clears exactly those four columns where an issuer's own 6-month BHR is empty: 28 cells in Q1 (7 issuers), 180 in Q2, 92 in Q3, with workbook snapshots. The expansion writer could not do it: it regenerates from Q1-only event tables and would have cleared about 1,480 curated Q2 cells. Values return automatically as windows mature and the expansion is rerun. |
| 3 | "1-month" is the T+20 trading day, identical to "Day 20" (Table 2's two rows are now identical). | Documented; extended tables use Day 20 only. |
| 4 | Columns labelled "(%)" store fractions (0.53 = 53%). | Open: rename or document in the codebook. |
| 5 | Offer mechanism missing for 3 issuers (2290, 2335, 2697); pricing date filled for 59 of 106; controller type is bilingual free text. | Open: fill from prospectuses. |

Side effects reverted: the `--only` re-run overwrote the shared aftermarket run manifest and refreshed cached bars; those files were restored to their committed state. `make check-code` passes (flake8 installed for this).

## 2. Results (extended analysis)

**Regime.** The Apr-Jun window's ordinary p (0.0004) overstates the evidence because it was found in these data. A permutation scan over all contiguous windows gives a search-corrected p = **0.081**. Month explains about 13% of variance in log(1 + IR) (permutation p = 0.011). Consecutive listings are not serially correlated, prior-30-day IPO returns do not predict IR, and crowding does not move IR (retail oversubscription is about 5% lower per overlapping offering, marginal).

**Mechanism A vs B cannot be a main hypothesis.** 17 of 17 18C issuers use Mechanism A; only 6 of 86 others do. The route- and window-adjusted coefficient is -0.15 log points (s.e. 0.18, minimum detectable effect about 0.49).

**Tails.** 27% of deals break issue and 25% more than double. PPML on 1 + IR: A+H multiplier 0.72 (p = 0.007), Apr-Jun 1.51 (p = 0.014). Apr-Jun raises the odds of IR > 100% about fivefold (p = 0.004); VC/PE-backed issuers are much less likely to break issue (odds ratio 0.22, p = 0.011). The cornerstone-at-the-90th-percentile pattern does **not** survive a bootstrap (p = 0.29).

**Prediction.** Out of sample the M3 baseline (R-squared 0.16 leave-one-month-out) does no better than the window dummy alone; prior-IPO returns add nothing.

**Aftermarket, corrected reading.** The first pass (Mann-Whitney on 1-month and 3-month BHR) suggested that April-June listings fall much further after day 1. The daily-bar study qualifies this:

- Event time, each IPO as independent: BHAR vs HSI at 60 trading days is -19.1% (hot, N = 45) vs +40.0% (other, N = 38); Mann-Whitney p < 0.001. With exact wild cluster inference over 9 listing months the day-60 p is 0.031 and the day-20 p is 0.109.
- Calendar time, each date counted once: the April-June portfolio's excess return is -19 bp/day (Newey-West p = 0.50, not different from zero), the other listings' is +37 bp/day (p = 0.039), and the difference is not significant (p = 0.27).
- So the data support "January-March listings did well after day 1" more than "April-June listings collapsed", and cannot separate either from the market path of each window. Drop hot-window aftermarket reversal from the list of confirmatory claims.

## 3. Hold-out plan: Q4 2026 and later listings

Decide now, test once on listings dated 2026-10-01 or later (the analysis scope stays 2026 listings, so Q4 2026 listings are part of the same year and are the natural hold-out; anything listed in 2027 belongs to a later study). Do not re-tune these on Q4 data.

| Claim | Test | Fixed before seeing Q4 |
|---|---|---|
| H1. A+H issuers have lower first-day returns | OLS on log(1 + IR) with the M3 controls; A+H coefficient < 0 | One-sided 5%, HC3; direction only |
| H2. VC/PE-backed issuers are less likely to break issue | Logit or Fisher on IR < 0 | One-sided 5% |
| H3. First-day returns differ by listing window (level shift) | Compare the mean log(1 + IR) of Q4 listings with the Jul-Sep mean | Two-sided, 5% |
| H4. Mechanism A vs B | Not tested separately; report as part of route/18C | none |

Power warning: Q4 will contain far fewer than 106 IPOs, so H1-H3 can only fail to reject or give directional support. That is expected; the purpose is to avoid re-using the same 106 observations for new tests.

## 4. Status of the other next steps

| Step | Status |
|---|---|
| Fix data items 1-2, re-export | Done (above). |
| Event-time aftermarket study from daily bars | Done (`analysis/out/event_time/`). |
| Hold-out claims | Written above; awaiting Q4 listings. |
| A-share pre-pricing close for the 34 A+H issuers | **Done** (`docs/AH_ANCHOR_2026.md`): collected programmatically for all 34, no estimates. |
| Daily margin-financing (孖展) data for the hot window | **Not collectable**: no public machine-readable history was found. Ingestion path and validator added (`analysis/margin_financing_2026.py`); needs a data file. |
| 6-month windows and cornerstone unlocks for Q2 listings | **Time-gated** until mid-October 2026; `make refresh-2026` reruns everything, and the lockup event study picks Q2 issuers up from the cached bars. |
| Retire Mechanism A vs B as a stand-alone line | Recommended (section 2). |

Limits: 9 listing months (few clusters), the sample ends 2026-09-09, endogenous retail and cornerstone choices, and a hot window that remains data-informed.
