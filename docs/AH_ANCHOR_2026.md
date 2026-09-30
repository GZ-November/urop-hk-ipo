# A+H reference prices and source review · 2026-09-30

The collector now covers **41 A+H issuers in the stored master**: seven 2025 listings and 34 in 2026, all with subscription-close A-share/FX anchors. This is coverage of the stored panel, not certification of exchange-wide listing completeness. The 2026 analysis keeps its 34-issuer scope. Cross-year collection does not increase that study's N.

`pipeline/exports/HKIPO-MASTER-AH-reference.csv` stores cross-year anchors; `HKIPO-2026-AH-reference.csv` is the study input. `--all --as-of 2026-09-30` extends old caches, rather than reusing a 2026-only FX history. Anchors record A price date, FX date and observation cutoff. Failed or empty refreshes preserve existing caches. The refresh target rebuilds the master before collecting reference prices.

First-day OHLC was corrected for 26 of 106 stored 2026 issuers; using adjusted prices with original offer prices had even reversed the return sign for some split stocks. The A+H mean first-day return is now 10.9%. See the correction ledger in the integration review.

The daily H/A premium now divides **raw H prices by raw A prices × FX**. Previously the H aftermarket cache could be adjusted for subsequent splits while A prices remained raw. The collector stores raw H bars separately. Buy-and-hold price returns still exclude dividend reinvestment and may be affected by corporate actions; they are not total returns.

## Updated exploratory results

Mean offer discount remains **38.2%**, versus **30.7%** at the first-day close. These anchors have different dates, so the change also includes A-share and FX moves. Discount versus IR has Spearman rho −0.30, p = 0.084; this is an association.

At day 60, **25 of 34 issuers** have matched observations. Within those 25, the mean raw-price gap is −28.7% at both day 0 and day 60; mean change is about zero (paired t p = 0.996; Wilcoxon p = 0.075). This does **not establish absence of convergence**. The fixed-endpoint-cohort path and horizon coverage are exported alongside the issuer/date premium panel. Interior cross-market holidays are not filled.

For A-share reactions, the original CSI 300 subtraction is retained alongside an alpha/beta market model estimated separately before each event on A trading bars [−120,−21], requiring 60 valid pairs. At H listing, market-model mean CAR [−5,+5] is **−7.6%** (N = 34, Wilcoxon p ≈ 0.001; placebo p ≈ 0.004), versus −6.0% for simple index subtraction. The market model is a sensitivity check, not a sector control or causal identification. Raw prices, overlapping event dates and few clusters remain limitations.

Generated tables: `analysis/out/ah_anchor/ah_anchor.md`; underlying outputs include `premium_panel.csv`, `horizon_coverage.csv`, `balanced_path_60.csv`, and event-specific market-model parameter files.

## Margin financing and lockups

The earlier claim that historical margin data cannot be collected was too broad. Dated news broker surveys provide **69 sourced observations for 23 of 106 stored 2026 issuers**, with nine closing-day snapshots. Coverage is sparse, broker membership is unspecified, and source dates are distinct from final official retail-subscription outcomes. See [source review](AGY_INTEGRATION_2026-09-30.md).

Q2 six-month lockup windows remain calendar-gated. This work did not fabricate post-unlock returns or move the observation cutoff beyond 2026-09-30. `make refresh-2026` can be run once event windows mature.
