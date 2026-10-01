# IPO literature and methods for the September 2026 offering-facts sample

Prepared on 1 October 2026. Target population: the project's 113 Hong Kong Main Board IPOs listed from January through 30 September 2026. This note develops offering and company analyses; first-day returns, aftermarket prices, trading and event outcomes are outside its scope.

This is a literature-informed exploratory methods review, not a preregistration or a replication claim. Historical studies motivate questions and variable choices; they do not establish a Hong Kong rule, a universal fee benchmark or causality in this sample. Proposed specifications below are our adaptations, distinguished from the authors' findings. Estimates belong in the generated analysis report, not in this note.

## 1. What previous research contributes

Eight IPO publications were consulted: seven original empirical papers and one survey. Two additional original methods sources inform fractional responses and clustered inference. Access was uneven: where only publisher abstracts were available, the note does not infer unobserved sample sizes or regression details.

| Publication and evidence inspected | Question, sample, data and method | Transfer to this project; limits |
| --- | --- | --- |
| Lowry, Michaely and Volkova (2017), *Initial Public Offerings: A Synthesis of the Literature and Directions for Future Research*. University repository abstract and bibliographic record. | Literature synthesis covering the IPO process, intermediaries and the decision to list. It is a survey, without one common estimation sample or estimand. It motivates studying issuance costs and intermediary choices alongside returns. [University source](https://hub.hku.hk/handle/10722/326143). | Organize separate questions about costs, investor composition and demand. The survey supplies conceptual scope, not an identification strategy for our cross-section. |
| Lee, Lochhead, Ritter and Zhao (1996), *The Costs of Raising Capital*. Author-university PDF's indexed abstract and introduction; publisher abstract. | US corporate debt and equity issues, 1990–1994; compares underwriting spreads and other direct expenses by security class and proceeds. The authors characterize the study as descriptive and report economies of scale. [Author PDF](https://site.warrington.ufl.edu/ritter/files/2016/01/The-Costs-of-Raising-Capital-1996.pdf), [publisher](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1475-6803.1996.tb00584.x). | Separate expense categories and examine scale gradients. Our total listing expense can already include commissions; never add a commission proxy to it without checking accounting scope. Their historical US averages are not HK benchmarks. |
| Chen and Ritter (2000), *The Seven Percent Solution*. Full university-hosted paper; sample section and fee tables inspected. | 3,203 US firm-commitment IPOs, 1985–1998, SDC; domestic proceeds at least US$20 million, excluding selected security types. Proceeds exclude overallotment and are inflation-adjusted. The paper examines spread distributions, time trends and offer-size patterns, including concentrated 7% fees among moderate-sized US offerings. [Full paper](https://people.bath.ac.uk/mnsrf/Teaching%202011/IB/Literature/L3-spread/Chen-Ritter.pdf). | Report disclosed rate frequencies and size gradients separately. Use base proceeds excluding overallotment. Do not assume Hong Kong fees should equal 7%, or equate a Hong Kong tranche commission with a full US gross spread. |
| Torstila (2003), *The Clustering of IPO Gross Spreads: International Evidence*. Publisher abstract. | International comparison of spread clustering and abnormal spreads. The abstract finds clustering in several markets and explains that clustering need not imply collusion. Exact country coverage, sample counts and specifications were not verified from accessible full text. [Publisher](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/clustering-of-ipo-gross-spreads-international-evidence/37755479B2A322916AF76D5ACAE93D6B). | Fee bunching is a useful fact. Concentration at a rate cannot establish market power, tacit collusion or excess profits without further economic evidence. |
| Cornelli and Goldreich (2001), *Bookbuilding and Strategic Allocation*. Publisher abstract. | Books for 39 international equity issues; investor-level bid information and allocation comparisons. Informative bids, repeat participation and certain other bidder characteristics are associated with preferential allocation. [Publisher](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00407). | Distinguish investor demand from the issuer's allocation choices. Aggregate applicant counts and tranche totals cannot replicate investor-level information-revelation tests; individual institutional bids and discretionary allocations are missing. |
| Megginson and Weiss (1991), *Venture Capitalist Certification in Initial Public Offerings*. Full university-hosted paper; sample and gross-spread regression tables inspected. | 320 VC-backed and 320 non-VC-backed US IPOs, January 1983–September 1987, matched on industry and offering size using IDD and prospectus information. Comparisons and spread regressions include backing, log offering amount, underwriter market share and age. Matched samples still differ in mean offering size. [Full paper](https://business.lehigh.edu/sites/default/files/2019-08/8%20megginson_weiss_1991_jf.pdf). | Backing indicators can be related to fees after controlling for scale and composition. First diagnose overlap and residual imbalance. Our combined VC/PE category is broader than their VC measure, and matching does not establish random assignment. |
| McGuinness (2014), *IPO firm value and its connection with cornerstone and wider signalling effects*. Publisher-indexed abstract and author profile abstract. | Hong Kong IPO cornerstone agreements; separates presence, size, investor count and lockup, relating these to valuation multiples and other outcomes. Exact sample dates/counts and detailed estimators were not verified from accessible full text. [Publisher article](https://www.sciencedirect.com/science/article/pii/S0927538X14000213), [publisher author record](https://www.sciencedirect.com/author/7003488617/paul-b-mcguinness). | Separate cornerstone dimensions rather than treating all agreements alike. Our cornerstone-share and retail-applicant models are new descriptive adaptations, not replications of the valuation tests. Investor counts need source repair before use. |
| Pagano, Panetta and Zingales (1998), *Why Do Companies Go Public? An Empirical Analysis*. Publisher abstract. | Italian private-firm database; compares ex ante and ex post IPO-firm characteristics with private firms to examine listing selection and subsequent financing outcomes. The abstract associates listing likelihood with firm size and industry valuation. Detailed sample counts and estimators were not verified here. [Publisher](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.25448). | Our issuer characteristics describe firms that completed IPOs. They cannot estimate the probability of going public, or prove why firms list, without private-company controls, eligible non-listing firms and unsuccessful applicants. |

## 2. The estimands we can study now

The current data support conditional associations among completed IPOs. They do not support the causal effect of appointing a sponsor, securing a cornerstone, obtaining VC backing or choosing a listing route. Issuer quality, anticipated demand and bargaining strength can influence several of these variables together.

### A. Do absolute listing expenses increase less than proportionally with offering size?

Let \(E_i\) be disclosed absolute listing expenses in HKD and \(P_i\) be offer price times final base-offer shares, excluding overallotment. Estimate:

\[
\log E_i=\alpha+\beta\log P_i+X_i'\gamma+\tau_{q(i)}+\varepsilon_i.
\]

The principal estimand is a conditional expense elasticity. Test \(H_0:\beta=1\), rather than testing only whether \(\beta=0\). A slope below one is consistent with a declining expense burden as deals grow. For the fitted relationship, doubling proceeds changes expenses by a factor \(2^\beta\), and the expense/proceeds ratio by \(2^{\beta-1}\).

This avoids putting a variable containing \(P_i\) in its denominator on the left and \(P_i\) on the right. An expense/proceeds scatter remains useful descriptive context. The log model is our adaptation of the cost and scale questions in Lee et al. and Chen–Ritter, not their exact estimator. Check estimated versus final expense timing, one-off restructuring items, currency, positive amounts, influential large deals and whether fees are included. Cross-sectional elasticity alone cannot identify a production cost function or prove cost savings from enlarging the same issuer's offering.

Start with log proceeds alone; then add a small set of age, A+H and loss-status controls and quarter indicators. Coarse industry controls belong in a separately labelled sensitivity model if degrees of freedom and support permit. Fix the complete-case sample across nested columns.

### B. Which issuer and offer characteristics correlate with disclosed commission rates?

Estimate an OLS model in percentage-point units:

\[
u_i=\alpha+\beta\log P_i+X_i'\gamma+\tau_{q(i)}+\varepsilon_i.
\]

Here \(u_i\) is the original disclosed Hong Kong underwriting commission, not an inferred all-in spread. A doubling of proceeds corresponds to \(\beta\log 2\) percentage points in the fitted rate. Display its exact frequency distribution and rounding conventions; a strongly bunched rate may offer little independent variation.

Analyze an international-tranche rate separately where supported. Discretionary incentive maxima are not observed payments. Do not use derived total-fee fields flagged in the fact inventory or construct an all-in spread from incompatible tranche disclosures. Backing comparisons should use known classifications, keep unknown values missing and show how adding scale controls changes the association. This follows the historical distinction between rate clustering and fee determinants, without treating their findings as causal evidence here.

### C. Which firms receive a larger cornerstone share?

For cornerstone share \(c_i\in[0,1]\), estimate a fractional logit conditional mean:

\[
E[c_i\mid X_i]=\Lambda(\alpha+X_i'\gamma+\tau_{q(i)}+\eta_{s(i)}),
\qquad \Lambda(z)=\frac{\exp z}{1+\exp z}.
\]

The fractional-response quasi-likelihood accommodates observed zeros and ones without ad hoc log-odds transformations. It does not require interpreting shares as binomial counts of independent shares. This estimator comes from [Papke and Wooldridge's original methods paper](https://www.nber.org/papers/t0147), published in 1996 after a 1993 working paper.

Report average marginal effects or average predicted-share contrasts in percentage points; logit coefficients are not percentage-point effects. Start with scale, age and A+H plus quarter, then use coarse industry sensitivity if supported. Keep shares bounded and un-winsorized. Compare OLS as a functional-form sensitivity, inspect predictions and convergence, and show a model including zeros alongside a participation/positive-share decomposition only if its sub-samples are adequate.

The denominator must be final base-offer shares, not total company shares. Final cornerstone shares can combine a pre-subscription monetary commitment with final price and offer scale; timing and units must be disclosed. A guaranteed allocation is different from an institutional order-book bid. Restrict presence to documented zeros versus positive shares; undisclosed information is missing.

### D. Is cornerstone participation associated with broader retail demand?

Use retail applicant count \(A_i\), not aftermarket returns:

\[
\log A_i=\alpha+\theta c_i+\beta\log P_i+X_i'\gamma+\tau_{q(i)}+\eta_{s(i)}+\varepsilon_i.
\]

If all eligible counts are positive, use \(\log A_i\); if genuine zeros occur, disclose a \(\log(1+A_i)\) sensitivity and a count conditional-mean model. For the positive-count log specification, a 10-percentage-point share increase corresponds to \(100[\exp(0.1\theta)-1]\)% in the fitted count relationship. This is a log-scale association, not automatically a change in the arithmetic mean count.

For a count-model sensitivity, Poisson pseudo-maximum likelihood can model \(E[A_i\mid X_i]=\exp(X_i'\beta)\); robust uncertainty is needed and equality of mean and variance should not be assumed. Oversubscription is a separate outcome: its denominator is retail shares offered, creating a mechanical supply component. Applicant counts offer a different breadth measure, but their sum across deals is not a count of unique investors.

Cornerstone and retail demand can both reflect expected issuer attractiveness and marketing. Final allocations can depend on price and offer size. Prefer an ex ante commitment measure, initial offer size and initial retail tranche if those are validated; treat final-share models as jointly determined associations. Do not control for final clawback or final retail share in the primary demand model and then call the remaining coefficient a direct causal effect. Running the cornerstone model first does not establish mediation or the mechanism of certification.

### E. Does backing composition permit meaningful adjusted comparisons?

Before a backing coefficient is emphasized, tabulate known VC/PE versus no-VC/PE counts by route, coarse industry and quarter. Compare log proceeds, age, loss status, customer concentration and available pre-IPO holdings; show standardized mean differences, missingness and ranges. Diagnose whether a few non-backed issuers carry nearly all of the comparison.

VC, PE, corporate VC and government backing overlap; do not turn overlapping indicators into mutually exclusive groups without a documented rule. A+H status and an exclusive route classification are also different variables. If support is poor, report composition differences and restricted-support sensitivities. Do not force propensity-score matching or weighting merely to obtain a treatment coefficient; weights can become unstable and matching cannot remove unobserved selection. The practical lesson from Megginson–Weiss is to examine comparability, not to assume that its historical matched sample guarantees comparability here.

## 3. Inference, timing and reporting

The 113 firms are one issuer-level cross-section spanning at most nine listing-month clusters. Complete-case regressions may contain fewer firms or months. Quarter fixed effects absorb broad period shifts; they do not eliminate arbitrary dependence among IPOs in the same month. Conventional cluster-robust standard errors with few clusters can over-reject and produce narrow intervals. [Cameron and Miller (2015), author-university paper](https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf).

For small OLS models, report HC3 intervals as inference conditional on independent issuer errors, alongside restricted wild cluster bootstrap tests for the main slopes and the expense elasticity restriction where implemented. Record actual cluster count, cluster sizes, bootstrap weights, seed, draws and failures. With nine clusters, a bootstrap is a sensitivity analysis with limited information, not a guarantee. For nonlinear models, robust sandwich or case-bootstrap intervals do not automatically address shared month shocks; acknowledge that limitation and show leave-one-month-out coefficient stability. Never label independent-case bootstrap intervals as month-cluster inference.

Use one coherent test family for the principal questions, show unadjusted and Holm-adjusted p-values, and emphasize magnitudes and confidence intervals. List every fitted specification and sensitivity, including failed convergence. Since facts have already been examined, the exercise is exploratory; a retrospectively written methods note is not preregistration.

Required table notes: sample cutoff; outcome units; variable timing; expense/proceeds scope; complete-case N; quarter/industry controls; uncertainty estimator; clusters; missingness and exclusions. Graphs should reveal support and influential observations, not just fitted lines. Preserve non-positive accounting facts as separate indicators where logs are inappropriate; unknown backing is not a zero and negative equity is not a valid denominator for a conventional leverage ratio.

The current sample contains no historical policy pre-period or private-company comparison population. Thus a 2026-only before/after story cannot identify the effect of an earlier regime reform, and these data cannot answer the listing-choice question in Pagano et al. Broadening to withdrawn applications, eligible private firms, historical cohorts, documented ex ante cornerstone commitments or institutional bid books would change what can be identified. Current results should remain conditional associations among the 113 completed listings through 30 September 2026.

## 4. Immediate analysis sequence

1. Preserve the 113-issuer snapshot and audit the exact cost, commission, cornerstone and application definitions.
2. Estimate the absolute expense elasticity and disclosed commission-rate gradients; inspect bunching and large-offer influence.
3. Estimate cornerstone fractional logit and its marginal effects; then fit retail-demand associations with scale and period controls.
4. Publish backing overlap diagnostics before substantive backing comparisons.
5. Report fixed-sample nested models, coarse-sector sensitivities, influential-observation and leave-one-month-out checks, uncertainty limitations and the full exploratory specification inventory.

The [offering-facts report](../analysis/out/offer_facts/facts.md) provides the source-field coverage and cautions that govern these adaptations. None of the proposed models requires first-day or aftermarket performance.
