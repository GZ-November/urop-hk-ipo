# agy integration and source review · 2026-09-30

> Historical snapshot: the sample sizes, checks and repair status below describe the stage recorded here. The current population is 113 issuers after PR #23/#25; see [current research plan](../../RESEARCH_PLAN_2026.md) for coverage and remaining work. Historical audit counts do not certify the expanded sample.

Inspected agy's local DeepCoder work and its investigator/search results in the Antigravity transcripts, plus uncommitted changes in the primary checkout. Their original working files remain untouched there. The integration branch incorporates the useful collector and analysis work, corrects its data/interpretation contracts, and regenerates outputs.

## Accepted and corrected

- Cross-year A+H collection: expanded from 34 to 41 stored issuers. The seven 2025 rows initially had no FX anchors because the cached FX series began in November 2025. Extending cache coverage produced 41/41 subscription-close anchors. The statistical study stays 2026-only.
- Fee regressions use one complete-case control sample rather than estimating different regressor samples.
- Idea 13's full-sample retail-demand, applicants, HIBOR, price-range and flipping regressions are retained. Nested specifications now use common samples, all reported HC3 tests enter the BH family, and singular/unit-leverage designs are not estimated. These proxies cannot identify individual leverage or causal herding.
- A+H raw H/A price comparison, fixed endpoint cohort and pre-event market-model sensitivity are implemented; outputs and coverage are exported.

## First-day price-basis correction

Fresh raw H-share collection exposed a wider defect: first-day OHLC in the master had been taken from Tencent's forward-adjusted series and compared with the original IPO offer price. **26 of 106** first-day closes changed when reconstructed from Tencent's static yearly HK files. For example, 2768.HK's close changes from 26.747 to 40.16 and IR from −25.7% to +11.6%; 3296.HK changes from 61.876 to 88.00 and IR from −20.4% to +13.3%. The full before/after ledger is `first_day_price_corrections.csv`.

The market provider now has an explicit raw mode. It reads `https://data.gtimg.cn/flashdata/hk/daily/YY/hkNNNNN.js`, records the source and price basis, and does not fall back to a split-adjusted Yahoo quote for as-traded OHLC. Static files do not provide turnover, so the existing separately collected amount is retained. Incomplete first-day collections stop before workbook writeback. Adjusted aftermarket baselines are aligned even for dividend adjustments below 1%, when the first bar is on the listing date. All three 2026 workbooks, academic derived fields, aftermarket fields, exports, master and analysis outputs are regenerated.

## Candidate margin observations

`pipeline/reports/margin_review/agy_candidates_UNVERIFIED.csv` preserves all **42 candidate rows / 20 issuers** from agy. These do not enter the analysis. Source labels such as “HK01 / AAStocks broker survey” had no article URL, timestamp or survey definition.

A concrete discrepancy: the candidate records 2768.HK's HK$110.76bn on **2026-01-27**. [The dated article](https://www.guandian.cn/article/20260129/540627.html) reports that amount for **2026-01-29**. The final candidate's 2252 multiple also resembles the official retail subscription outcome; it has not been established as a margin observation. No candidate is deemed verified merely because its date falls within the subscription window.

Reconstructed source ledger: `pipeline/prospectus_pipeline/data/margin/reported_snapshots.json`. Export: **69 rows / 23 stored 2026 issuers**, including **nine closing-day snapshots**. Six observations outside the stored sample are retained in the ledger and logged in `source_exclusions.json`, rather than silently incorporated. This is partial coverage of 106 issuers.

Sources include dated Zhitong broker-survey reports syndicated through [HSTong (April 20)](https://www.hstong.com/news/hk/detail/26042019160019985), [April 21](https://hk.investing.com/news/stock-market-news/article-1417308), [June 30](https://hk.investing.com/news/stock-market-news/article-1532406), [July 6](https://hk.investing.com/news/stock-market-news/article-1539561), and [September 1](https://hk.investing.com/news/stock-market-news/article-1637419). Every source and observed amount is recorded in the ledger; the exporter converts HKD 100 million to HKD without filling missing dates.

The harmonized margin multiple is reported margin amount / (initial public-offer shares × maximum offer price). Source “oversubscription” terminology is inconsistent about subtraction of one and coverage, so it is not copied into this standardized ratio. Final allotment/retail demand is a separate variable. Declining snapshots are permitted; they may reflect cancellations or changing survey coverage. Duplicate issuer/date observations require reconciliation. Missing/nonfinite amounts, absent links, changed denominators and invalid windows are rejected. Endpoint growth requires a named constant survey scope and positive initial observation, but unnamed broker membership still prevents treating it as a complete market path.

## What the evidence supports

The sourced panel's latest-observed margin multiple versus first-day return has rho **0.38**, p **0.076**. The size/window-adjusted coefficient has HC3 p **0.611**. Closing-day sensitivity has N = 9; its hot-window control creates a unit-leverage observation, so HC3 inference is withheld. The earlier “exponential crowding” claim is removed. Sparse endpoint growth does not measure acceleration or establish information cascades.

The full 106-issuer proxy models show strong simple correlations, but the subscription coefficient loses significance after applicants, size, HIBOR and listing-window controls. This work therefore improves the evidence, without claiming the proposed mechanism is confirmed.

## Verification and remaining coverage

`make check-code`: 287 pipeline tests (two real-PDF tests skipped because PDFs are absent in this worktree), 42 analysis tests, lint and registry consistency passed after the raw first-day correction. `make analysis` regenerated all 2026 analysis outputs successfully.

Workbook/JSON audits for 2026 Q1/Q2/Q3: respectively 2,660/3,136/1,610 prospectus cells matched, and 684/810/414 allotment cells matched. Q2 has **14 missing JSON cells in BL** and no numeric mismatches; Q1/Q3 have no audited missing cells. These are storage reconciliations against existing extractions, not a fresh semantic review of every original prospectus. The prior extraction import commit is preserved; source completeness is not declared on the basis of these audit counts.

Q2 lockup horizons remain immature at the September 30 cutoff. There is no synthetic future data or automatic recurring job in this change. `make refresh-2026` refreshes data and analyses when run later.
