# Offering Economics: Exploratory Analysis Design

Written on 1 October 2026 before running the new models below. Existing facts and earlier project results have already been examined; this is an exploratory specification record, not a preregistration.

## Sample and scope

Use the 113 unique Hong Kong Main Board ordinary IPOs listed in 2026 on or before 30 September, selected from the current master by actual listing date. Do not refresh sources or incorporate first-day or aftermarket outcomes. Separate missing classifications from observed zeros. Each nested model family uses the complete-case sample of its largest specification. Preserve issuer-level exclusion logs and input hashes.

## Literature and questions

The [literature review](IPO_LITERATURE_METHODS_2026.md) explains what can be transferred from original IPO research. The models below are our adaptations:

1. **Issuance cost scaling.** Following the cost questions in [Lee et al. (1996)](https://site.warrington.ufl.edu/ritter/files/2016/01/The-Costs-of-Raising-Capital-1996.pdf), model log absolute disclosed listing expenses against log base proceeds. Test a proceeds elasticity of one: a slope below one is consistent with lower proportional costs for larger deals. It is not a causal production-function estimate.
2. **Disclosed underwriting fees.** Motivated by [Chen and Ritter (2000)](https://people.bath.ac.uk/mnsrf/Teaching%202011/IB/Literature/L3-spread/Chen-Ritter.pdf), examine the HK tranche commission rate and its conditional size gradient. Do not label this the full US-style gross spread. Do not add it to potentially overlapping listing expenses.
3. **Cornerstone allocation.** Motivated by [McGuinness (2014)](https://www.sciencedirect.com/science/article/pii/S0927538X14000213), model the observed cornerstone share of final base shares. Use OLS for transparent comparisons and small-cluster tests, and a fractional-logit conditional mean model for bounded predictions. [Papke and Wooldridge](https://www.nber.org/papers/t0147) permit endpoint shares without arbitrary log-odds corrections. This studies allocation composition, not certification or a causal effect of changing offering size.
4. **Retail participation and denominators.** Model log applicant counts, rather than only oversubscription. Add final cornerstone share as an association check. Decompose a separately constructed applied/initial-public share multiple into applicant participation, nominal application intensity and the public-tranche denominator. [Cornelli and Goldreich (2001)](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00407) motivate distinguishing demand from allocation, but their institutional bid-level estimand cannot be replicated here.
5. **Backing composition and overlap.** Before attempting the type of matched comparison used by [Megginson and Weiss (1991)](https://business.lehigh.edu/sites/default/files/2019-08/8%20megginson_weiss_1991_jf.pdf), report VC/PE group imbalance and within-route/coarse-industry counts. No propensity matching, treatment effect or certification claim is planned: the non-backed group is small and sector/route support may be absent.

## Specifications and timing

Define base proceeds as final offer price × final global offering shares before overallotment. Expenses are disclosed HKD amounts. Latest-period losses use observed profits; ratios are not pooled across currencies. The coarse industry groups are technology (semiconductors, software/AI, hardware/robotics), health (biotech/pharma, medical devices/services), and other industries. This classification is fixed before the new estimates.

For cost, commission and cornerstone outcomes, report:

- M1: log base proceeds only.
- M2: M1 + log firm age + independent A+H flag + latest-period loss flag.
- M3: M2 + technology and health indicators + Q2 and Q3 listing indicators.

For applicants, use the same M1–M3 and M4 = M3 + final cornerstone share. Cornerstone shares, offering size, route and listing timing are selected and can be jointly determined with expected demand. Final cornerstone allocation is not established as predetermined retail information. The M4 comparison is not a mediation analysis.

For demand decomposition, use the same M3 design and same issuer set for every component:

\[
\log\left(\frac{\text{valid applied shares}}{\text{initial public shares}}\right)
=\log(\text{applicants})
+\log\left(\frac{\text{valid applied shares}\times\text{offer price}}{\text{applicants}}\right)
-\log(\text{initial public shares}\times\text{offer price}).
\]

The regression coefficient identity follows from OLS linearity on a shared design, not from independent behavioral mechanisms. Compare the constructed multiple to the reported multiple and log discrepancies; never silently overwrite reported demand.

## Inference, robustness and reporting

OLS: HC3 and listing-month CR1 covariance, explicit cluster counts, and the project's exact restricted Rademacher wild-cluster bootstrap. For expense elasticity, test beta=1 by shifting the outcome by the log-proceeds regressor before applying the zero-null bootstrap. Enumerating 2^G sign patterns does not make finite-cluster inference exact in its statistical validity; it only removes simulation error.

The five fully adjusted OLS focal tests form one exploratory family: expense-size elasticity=1, commission-size slope=0, cornerstone-size slope=0, applicant-size slope=0 (M3), and applicant-cornerstone slope=0 (M4). Report separate Holm corrections for HC3 and wild-cluster p-values. Earlier explored tests and supplementary specifications are outside this narrow family; correction does not remove the broader search history.

Fractional logit uses binomial quasi-likelihood and HC0 sandwich covariance. Supplement with 1,000 listing-month pairs-bootstrap draws for the standardized doubling-size share difference. Refit the model on each draw, evaluate predictions on the original model sample, and log rank/convergence failures. Nine months make nonlinear asymptotic p-values and percentile intervals fragile; there is no valid automatic transfer of the linear restricted bootstrap to GLM.

Robustness: remove the largest three deals, remove the highest-Cook-distance observation, and perform leave-one-listing-month-out slope checks. These describe influence and temporal stability. Report all attempted specifications, N, rank, residual degrees of freedom, leverage, VIF, coefficients, standard errors, sample records and nonlinear bootstrap diagnostics. Do not select a specification based on significance. Do not implement policy DiD/RD with an all-post-reform sample or IV without an exclusion argument.
