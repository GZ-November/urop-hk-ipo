# Academic extensions on the 2026 sample · 2026-09-30

> Numerical results below predate the September 30 raw first-day price correction and are retained as a historical write-up. Use regenerated `analysis/out/academic/` tables and [the integration review](AGY_INTEGRATION_2026-09-30.md) for current estimates.

Script: `analysis/academic_extensions_2026.py` (about 20 seconds); outputs in `analysis/out/academic/`. Sample: 106 Main Board ordinary IPOs listed 2026-01-02 to 2026-09-09. Exploratory throughout.
It complements `EXTENDED_ANALYSIS_2026.md` (regime, mechanism, tails, aftermarket) with five designs from the IPO literature.

## Results

**1. Money left on the table (Loughran & Ritter 2002).**
- Issuers left **HK$83.0bn** on the table (HK$93.7bn of gains on deals that closed above the offer, HK$10.7bn of losses on the rest) against **HK$4.8bn** of disclosed underwriting commissions: 17.3 times the fees in aggregate, 8.8 times for the median deal, and above the fee on 65% of deals. In the April-June window the multiple is 34.8 (other listings 8.2).
- Who holds the gain follows who holds the shares: cornerstone investors hold 39.0% of the base offer and capture 40.6% of net money left; other placees 50.1% and 46.9%; retail 10.9% and 12.5%. The split is almost the same in and out of the hot window, so the pricing outcome is decided by allocation policy (cornerstone plus placing share), not by retail demand.
- A retail application earns little in expectation: assuming proportional allocation, the median expected gain is HK$0.7 per HK$10,000 applied outside the hot window and HK$2.6 inside it (median allocation ratio 0.23% and 0.06%). Averaged over everyone who applied, the retail gain per applicant is a median HK$76 (other) and HK$401 (April-June).

**2. Underwriting commission (Chen & Ritter 2000).** No single rate dominates (3.0% is the mode at 30% of deals; 2.5% 12%; 2.0% 8%), unlike the U.S. 7% gross-spread cluster. Scale economies are strong and robust: -0.47 percentage points per unit of ln offer size (HC3 p < 0.001, wild cluster p = 0.004), and A+H issuers pay 0.68 points less (p = 0.003, wild 0.020); R-squared 0.61. The raw correlation of fee rate with IR (+0.21, p = 0.03) is a size effect: with size, window and A+H controlled the coefficient on log(1 + IR) is -0.10 points (p = 0.45), so commissions are not set higher in deals that turn out more underpriced.

**3. Supply events around the lockup expiry and the end of stabilization** (HSI-adjusted, daily bars, placebo dates drawn from each issuer's neighbouring trading days; t-statistic-based so event-induced variance does not bias the test).
- **Stabilization end** (about 20 trading days after listing, N = 99): mean CAR [-5,+5] = +4.1% (plain t = 1.87, Wilcoxon p = 0.059, placebo p = 0.004). The pre-window [-5,-1] is also positive (+2.8%, placebo p = 0.029). Relative to the issuer's own neighbouring days the window is unusually strong, which fits price support lasting to the end of the period, and the effect is present among issuers without recorded stabilizing purchases (N = 86, placebo p = 0.005), so it is not simply the purchases. The 13 issuers with purchases show nothing (placebo p = 0.87).
- **Six-month lockup expiry** (N = 26 to 31, January-March listings only): mean CAR [-5,+5] = -5.9% and [-5,-1] = -3.9%, both marginal (placebo p = 0.147 and 0.116; HSTECH-adjusted 0.088 and 0.032), with a visible drop on the event day. Turnover rises about 15% relative to the pre-event baseline (median log ratio 0.14; placebo p = 0.004), consistent with selling into expiry.
- The placebo p-values are much smaller than the plain tests because placebo statistics are centred below zero (returns drift down and turnover decays as a listing ages). Read them as "unusual for the same weeks of a new listing's life", not as significance against zero.

**4. Partial adjustment inside the filing range (Hanley 1993).** Among the 41 range deals, offer-price revision (relative to the range midpoint) has the predicted positive relation with first-day return (rank correlation 0.19; regression coefficient 1.5 to 1.7 log points per 100 pp of revision) but it is not significant (p about 0.22 to 0.26). The 65 fixed-price deals cannot speak to this; the sample is too small to confirm or reject partial adjustment.

**5. Sponsor effects.** First-named sponsors (9 sponsors with at least 3 deals, 80 deals) do not explain first-day returns: the intraclass correlation is about zero before and after controlling for the listing window, A+H and size (permutation p = 0.58 and 0.76). Sponsor differences in mean IR reflect when their deals listed. Low power; not evidence of no effect.

Benjamini-Hochberg over this module's 7 tests (`multiplicity.md`): fee scale economies, stabilization-end CAR and the lockup turnover shock have q < 0.05; the rest do not.

## Data problems found while doing this

| Column | Problem | Effect |
|---|---|---|
| `Lead sponsor name` | Reads "CICC" for 92 of 106 issuers even when CICC is not among the sponsors (e.g., sponsors listed only as China Securities International or Yue Xiu). | Unusable. The first-named sponsor in `Sponsor(s)` is used instead. |
| `Total underwriting fee rate (%)` and `Underwriting base commission rate (%)` | The total equals 3.5% for 68 issuers and 1.00x% for the other 38, regardless of the disclosed commission (0.3% to 5.0%); the base rate looks 100 times too small. | Unusable; the disclosed HK and international commission columns are used. |
| `Underwriting discretionary incentive fee rate (%)` | Constant 1.00% for all 106 issuers (known). | Discretionary fees are not measured; the fee totals above are lower bounds. |

## What this suggests for the write-up

1. The strongest publishable descriptive facts are the size of money left relative to fees, who holds it (cornerstone and placing allocation, not retail), and the strong scale economies in commissions with an A+H discount.
2. The supply-event results (stabilization end, lockup expiry) are the most novel and most fragile: the stabilization-end result rests on a placebo calibration and should be reproduced on Q4 listings; the lockup result needs Q2 listings, whose 6-month windows begin to mature in mid-October.
3. Retail returns are a small number of Hong Kong dollars per application in expectation; the headline figures are the 0.06% to 0.23% allocation ratios.
4. Data still to collect: A-share closes before pricing for the 34 A+H issuers (turns the A+H discount into a measurable pricing anchor) and daily margin-financing data for the hot window. Neither is in the repository, and neither was estimated here.

Limits: 9 listing months, sample ends 2026-09-09, first-named sponsor is a proxy, expected retail gains assume proportional allocation, and all fee totals exclude discretionary fees.
