"""English presentation for the retail study, separate from numerical estimation."""
from __future__ import annotations

from shared.reporting import to_markdown

STRATEGIES = {
    'strict_one_lot': 'Strict one-lot',
    'one_lot_or_minimum': 'One-lot / minimum tier',
    'one_lot_or_minimum_ex3355': 'One-lot / minimum, excluding 3355',
    'ten_lot': 'Ten-lot',
    'budget_10000': 'HK$10,000 principal budget',
    'budget_50000': 'HK$50,000 principal budget',
    'budget_100000': 'HK$100,000 principal budget',
}


def table(frame):
    """Use the repository serializer; presentation never changes stored numbers."""
    return to_markdown(frame.set_index(frame.columns[0]), str(frame.columns[0]))


def money(values):
    return values.map(lambda value: f'{value:,.2f}')


def percent(values):
    return values.map(lambda value: f'{100*value:.2f}%')


def render_retail_report(portfolios, sensitivity, decomposition, bootstrap, regressions,
                         aftermarket, results_prefix='.', repo_prefix='../../..'):
    strict = portfolios[(portfolios.strategy=='strict_one_lot') & (portfolios.fee_hkd==88)].iloc[0]
    minimum = portfolios[(portfolios.strategy=='one_lot_or_minimum') & (portfolios.fee_hkd==88)].iloc[0]
    summary = portfolios[portfolios.strategy.isin(['strict_one_lot','one_lot_or_minimum'])][[
        'strategy','fee_hkd','n','mean_expected_net_hkd','median_simulated_net_hkd','p_total_loss']].copy()
    summary.strategy = summary.strategy.map(STRATEGIES)
    for col in ['mean_expected_net_hkd','median_simulated_net_hkd']: summary[col]=money(summary[col])
    summary.p_total_loss = percent(summary.p_total_loss)
    summary=summary.rename(columns={'strategy':'Strategy','fee_hkd':'Fee (HK$)','n':'IPOs',
        'mean_expected_net_hkd':'Mean expected profit per IPO (HK$)',
        'median_simulated_net_hkd':'Median total portfolio profit (HK$)', 'p_total_loss':'Portfolio loss probability'})
    sampling=bootstrap.copy();sampling.strategy=sampling.strategy.map(STRATEGIES)
    for col in ['mean_expected_net','month_bootstrap_lower','month_bootstrap_upper']: sampling[col]=money(sampling[col])
    sampling=sampling.rename(columns={'strategy':'Strategy','n':'IPOs','g':'Months','mean_expected_net':'Mean (HK$)',
        'month_bootstrap_lower':'95% lower (HK$)','month_bootstrap_upper':'95% upper (HK$)'})
    influence=sensitivity[sensitivity.strategy.isin(['strict_one_lot','one_lot_or_minimum'])][[
        'strategy','drop_highest_gross','n','mean_expected_net_hkd']].copy()
    influence.strategy=influence.strategy.map(STRATEGIES);influence.mean_expected_net_hkd=money(influence.mean_expected_net_hkd)
    influence=influence.rename(columns={'strategy':'Strategy','drop_highest_gross':'Highest-profit IPOs removed','n':'Remaining IPOs','mean_expected_net_hkd':'Mean expected profit (HK$)'})
    dec=decomposition[decomposition.strategy.isin(['strict_one_lot','one_lot_or_minimum'])][[
        'strategy','dimension','group','n','product_of_means','covariance','mean_product']].copy()
    dec.strategy=dec.strategy.map(STRATEGIES)
    for col in ['product_of_means','covariance','mean_product']:dec[col]=percent(dec[col])
    dec=dec.rename(columns={'strategy':'Strategy','dimension':'Grouping','group':'Group','n':'IPOs',
        'product_of_means':'Product of means','covariance':'Covariance contribution (pp)','mean_product':'Mean capital return'})
    # Covariance is a contribution in percentage points, not a percentage growth rate.
    dec['Covariance contribution (pp)']=dec['Covariance contribution (pp)'].str.removesuffix('%')
    reg=regressions.copy()
    for col in ['b_lsub','hc3_se','hc3_p','ci_lower','ci_upper','wild_p']:reg[col]=reg[col].map(lambda v:f'{v:.4f}')
    reg=reg.rename(columns={'sample':'Sample','n':'IPOs','g':'Months','b_lsub':'Demand coefficient',
        'hc3_se':'HC3 SE','hc3_p':'HC3 p','ci_lower':'95% lower','ci_upper':'95% upper','wild_p':'Wild-cluster p'})
    after=aftermarket[['group','day','n','g','median_bhr','mean_market_relative','median_market_relative','mean_ci_lower','mean_ci_upper']].copy()
    for col in ['median_bhr','mean_market_relative','median_market_relative','mean_ci_lower','mean_ci_upper']:after[col]=percent(after[col])
    after=after.rename(columns={'group':'Demand group','day':'Trading days','n':'IPOs','g':'Months',
        'median_bhr':'Median raw BHR','mean_market_relative':'Mean market-relative return',
        'median_market_relative':'Median market-relative return','mean_ci_lower':'Mean: 95% lower','mean_ci_upper':'Mean: 95% upper'})
    return f'''# Retail IPO Applications in Hong Kong: Allocation, Fees and Profit Distributions

Updated 3 October 2026. Observation cutoff: 30 September 2026.

## Research scope and principal finding

The population comprises 113 ordinary Hong Kong Main Board IPOs listed from 2 January to 30 September 2026. Headline first-day returns describe gains on allocated securities; they do not describe gains on the full application principal.

At an assumed HK$88 handling fee per IPO, the strict one-lot strategy has a mean expected profit of **HK${strict['mean_expected_net_hkd']:.2f} per application** and total expected profit of **HK${strict['expected_total_net_hkd']:,.2f}**. Its simulated total profit has a median of **HK${strict['median_simulated_net_hkd']:,.0f}**, with a **{100*strict['p_total_loss']:.1f}%** probability of a portfolio loss. For the 113-IPO one-lot/minimum-tier strategy, the corresponding mean is HK${minimum['mean_expected_net_hkd']:.2f} and loss probability is {100*minimum['p_total_loss']:.1f}%.

These are expectations and conditional lottery scenarios using observed first-day closing prices. They are not actual account performance, forecasts or causal policy estimates.

## 1. Sample construction: why strict one-lot coverage is 112

The current board-lot record for **2649.HK (ALSCO)** states 200 securities per trading lot. Its disclosed/extracted allocation schedule starts at 500 securities and has no 200-security application tier. The strict one-lot sample therefore contains 112 IPOs; the full-coverage sample uses the 500-security minimum tier for 2649. The unusual 200/500 difference remains a source follow-up item, rather than an assumption that a 500-security application is one trading lot.

Additional specifications cover ten lots, fixed principal budgets, and the minimum-tier sample excluding 3355.HK. For 3355, the published text and the inferred guarantee quantities remain distinguishable in the [provenance appendix]({results_prefix}/3355_original_and_derived.json). Excluding 3355 is a sensitivity check, not a new independent semantic review.

The frozen tier relation contains 4,582 rows across 113 issuers. The read-time gate verifies the existing independent review's candidate and coverage hashes, source-text hashes, and agreement between candidate and clean economic fields. Arithmetic reconciliation does not itself authorize a semantic review. Re-extraction produces candidates only; changed candidates require a new independent review before use.

## 2. Single applications and repeated participation

For each application, the model uses its guaranteed quantity, additional ballot quantity and disclosed ballot probability. It computes positive, zero and negative net-profit probabilities separately. Portfolio simulations use 100,000 draws, seed 20261003, and independent ballots across IPOs.

{table(summary)}

The table distinguishes **mean expected profit per IPO** from **median simulated total portfolio profit**. The complete [portfolio table]({results_prefix}/portfolio_distributions.csv) also reports the expected total, standard deviation, 5th/95th percentiles, negative-expectation share and applicant-level loss probability. These two loss measures have different denominators.

Prices remain fixed at their observed values. The simulation does not capture future market uncertainty, correlation across market returns, overlapping funding requirements or account-specific financing. Fixed budgets constrain subscription principal; handling fees are paid separately. IPOs that cannot be afforded are skipped without a fee. No annualized return is reported.

### Sampling sensitivity, distinct from ballot risk

The following intervals resample listing-month groups 2,000 times. Only nine unequal months are available; these are descriptive sensitivity intervals, not a guarantee of inference under arbitrary market dependence.

{table(sampling)}

## 3. Dependence on a small number of winners

At the HK$88 fee assumption:

{table(influence)}

Removing the largest observed gains is an influence diagnostic. It is not an implementable rule for choosing IPOs before returns become known. [All strategy sensitivities]({results_prefix}/profit_concentration_sensitivity.csv) include fixed-budget and ten-lot applications.

## 4. Allocation and initial returns: a descriptive decomposition

Let a be the expected allocated quantity divided by applied quantity and r the first-day return. With equal IPO weights:

`E[a*r] = E[a]*E[r] + Cov(a, r)`

The covariance uses denominator N. A negative contribution describes the combination of small allocations in high-return IPOs and larger allocations in weaker IPOs. The product of means is an algebraic comparison, not an identified policy counterfactual or proof of investor information types in Rock's model.

{table(dec)}

[All decompositions]({results_prefix}/allocation_return_decomposition.csv) also include the ten-lot strategy. Size groups use the same population cutoffs across strategies. Returns in source CSVs are decimal-scale values; the presentation above converts them to percentages or percentage points.

## 5. Fees, application size and financing

The [fee frontier]({results_prefix}/fee_frontier.csv) covers handling fees from HK$0 to HK$200. The [application-size schedule]({results_prefix}/application_size_schedule_fee88.csv) shows every disclosed tier at an assumed HK$88 fee. No tier is selected using its subsequently observed return.

Current channel examples are documented in [Futu's fee schedule](https://www.futuhk.com/en/support/topic2_418from_platform%3D1%26%26lang%3Dzh-hk) and [HSBC's channel FAQ](https://www.hsbc.com.hk/zh-hk/help/faq/investments/), checked on 3 October 2026. Some ordinary subscription channels charge no handling fee; selected bank-financing or branch channels quote HK$100. These current quotes do not establish actual fees paid throughout the research cohort. HK$28 and HK$88 remain hypothetical sensitivity values. See the [fee-source record]({results_prefix}/fee_sources.json).

The [financing sensitivity]({results_prefix}/financing_sensitivity.csv) assumes 90% borrowing, 3%/6%/10% annual interest and two/five funded days. These are scenario parameters; FINI settlement does not determine an individual account's loan duration.

All reported net profits subtract only the specified handling and financing costs. Subscription brokerage/levies on allotted securities, sale costs and opportunity cost are excluded. They are therefore partial-cost outcomes rather than complete net investment returns.

## 6. Subscription demand as supporting evidence

The demand regression below controls for offer size, firm age, cornerstone share, quarters and, where applicable, A+H status. It compares the full sample, exclusion of the three largest first-day returns, and non-A+H issuers. Final demand is endogenous and observed after pricing; coefficients are associations.

{table(reg)}

The aftermarket analysis uses **100 IPOs** with valid raw returns and HSI wealth relatives at both five and twenty trading days. Market-relative return is `(1+BHR)/(1+HSI)-1`, or wealth relative minus one. It differs from an additive abnormal-return measure.

{table(after)}

Mean intervals resample listing months. The high-demand group's negative twenty-day mean has an interval spanning zero; these data do not establish a general reversal. All group results are reported together. Final demand terciles are retrospective labels, not a pre-subscription prediction strategy.

## 7. Files and reproducibility

![Conditional portfolio profits, fee sensitivity and allocation-return decomposition]({results_prefix}/retail_profit_distribution.png)

- [Subscription demand baseline]({repo_prefix}/analysis/out/subscription_heat/subscription_heat.md)
- [Retail allocation baseline]({repo_prefix}/analysis/out/retail_profit/retail_profit.md)
- [Independent A+H price-anchor study]({repo_prefix}/analysis/out/ah_anchor/ah_anchor.md)
- [Input/output hashes and package versions]({results_prefix}/run_manifest.json)
- [Economic tests and review-gate tests]({repo_prefix}/analysis/tests/test_retail_distribution.py)

From the project root:

```bash
python run.py analysis --study demand --study allocation_profit --study retail_distribution
python tools/build_empirical_report.py
make check-code
make workspace-check
```

The A+H topic remains separate. This round does not add a causal design or resolve its external-price anomaly. The preceding narrative is preserved as a historical snapshot in [the archive]({repo_prefix}/docs/archive/README.md).
'''
