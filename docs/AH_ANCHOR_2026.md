# A+H issuers: A-share reference prices and the offer discount · 2026-09-30

Collector: `pipeline/prospectus_pipeline/tools/external/ah_reference.py`. Analysis: `analysis/ah_anchor_2026.py` (outputs in `analysis/out/ah_anchor/`).
Data written: `pipeline/exports/HKIPO-2026-AH-reference.csv` (anchors and discounts per issuer) and caches under `pipeline/prospectus_pipeline/data/market/ah_reference/` (raw A-share bars, CNY/HKD, CSI 300, symbol map).

## What was collected

- **A-share symbol for all 34 A+H issuers**, found through Tencent's search endpoint by requiring the same short name as the H listing (STAR-market symbols and status suffixes such as "U" handled). One issuer (2768.HK, A short name differs) is a documented manual override. No symbol was guessed.
- **Raw A-share closes**, CNY/HKD (Yahoo daily close) and CSI 300 for the whole sample period. The reference price is the A-share close on the last A trading day on or before the H subscription closing date, converted to HKD; a pre-pricing anchor is also stored where a pricing date exists. A missing bar or exchange rate leaves the anchor missing. Unit tests cover the anchor rules.
- **Sanity check:** all discounts are negative and between -12.8% and -61.8%; one issuer (6067.HK, -61.8%) is flagged outside a +/-60% plausibility band and dropped in a robustness run.

## Results (N = 34, exploratory)

- **Discount size.** H shares are offered at a mean 38.2% (median 39.2%) below the converted A-share close, in every one of the 34 cases. The discount narrows to 32.8% at the day-1 close (paired t p = 0.029) and then stays about 30% for at least 60 trading days: the H share does not converge to the A share within the window (mean change in the gap from day 0 to day 60 = +1.6 pp, Wilcoxon p = 0.22). Measured against its own A share, the H share earns +1.5% to +5.5% on average over 5 to 40 days, not significant.
- **The discount follows the A-share tape, not the H-share market.** A 10-point rise in the A share's 20-day return before the offer makes the offer 3.7 points cheaper relative to the A price (p < 0.001; wild cluster p = 0.027): the H offer price does not fully follow a recent A-share run-up. Larger offers have smaller discounts (+5.8 points per unit of ln size, p = 0.001). The April-June window has no effect on the discount (p = 0.62).
- **Discount and first-day return.** A deeper offer discount goes with a higher first-day return (rank correlation -0.33, p = 0.059; regression coefficient about -0.05 per +10 points of offer premium, p = 0.07 with the window, and -0.105, p = 0.009, wild cluster p = 0.012, when ln size is added). Dropping the implausible anchor gives -0.055, p = 0.10. So the pricing anchor carries information the size-and-window models miss, but the evidence is directional with 34 issuers.
- **A-share reaction to the H issue.** Relative to the CSI 300 and to the same stock's neighbouring days (placebo-calibrated), A shares fall around the H listing: CAR [-5,+5] = -6.0% (Wilcoxon p = 0.009, placebo p < 0.001), [0,+5] = -4.0%, [-1,+1] = -2.7%; around the subscription close [0,+5] = -3.8% (Wilcoxon p = 0.046, placebo p = 0.004). No pre-event drift ([-5,-1] about 0 at the subscription close). The A-share benchmark is the index, not a sector match, so read the placebo comparison as the relevant one.

Multiplicity (`ah_anchor.md`): the A-share momentum coefficient and the A-share reaction on listing day pass BH at 10%; the discount-vs-IR link does not on its own.

Limits: 34 issuers; the closing-date anchor is used because pricing dates are missing for several issuers; CNY/HKD is a daily close; raw A-share prices are not adjusted for dividends in the window.

## The other two items

- **Daily margin-financing (孖展) data: not collectable here.** No public, machine-readable history of daily margin totals was found (AAStocks shows only current snapshots on its IPO page, and the other pages found are guides or brokers' promotions). Nothing is estimated. Instead there is an ingestion path: put a file at `pipeline/exports/HKIPO-2026-margin-daily.csv` using `pipeline/templates/HKIPO-2026-margin-daily.template.csv`, and `analysis/margin_financing_2026.py` validates it (issuers in sample, dates inside each subscription period, cumulative totals never falling) and relates the margin path to IR. Without the file it writes a note and exits. Sources are the brokers' daily margin tables; each row should record where its figure came from.
- **Q2 lockup windows: calendar-gated.** The first Q2 six-month windows mature from mid-October 2026. `make refresh-2026` refreshes the cohort bars and aftermarket columns, clears any immature window statistics, re-exports, refreshes A-share references, rebuilds the master and reruns every analysis. The lockup event study reads the cached daily bars directly, so Q2 issuers enter it as their unlock dates pass; the expansion writer is not needed (and cannot be used without clearing curated Q2 cells).
