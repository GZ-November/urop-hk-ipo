"""Reproducible retail outcome distributions and descriptive allocation economics.

Observed 2026 cohort only. Lottery simulations condition on observed closing prices;
fees are explicitly scenarios, not historical account observations.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import retail_allocation_profit_2026 as baseline
import subscription_heat_2026 as demand
from research_inputs import C, ROOT
from shared.allocation_review import reviewed_tiers
from shared.retail_report import render_retail_report

OUT = ROOT / 'analysis/out/retail_distribution'
SEED = 20261003
SIMULATIONS = 100000


def outcome_metrics(frame, fee=0.0, borrowed_fraction=0.0, annual_rate=0.0, days=2):
    """Two disclosed states, including guarantees; amounts in security units."""
    required = ['applicants', 'ballot_winners', 'guaranteed_shares', 'ballot_extra_shares',
                'applied_shares', 'p0', 'p1']
    if not np.isfinite(frame[required].to_numpy(float)).all():
        raise ValueError('Nonfinite lottery inputs')
    if (frame.applicants <= 0).any() or (frame.applied_shares <= 0).any() or (frame.p0 <= 0).any():
        raise ValueError('Positive applicant count, applied units and offer price required')
    p = frame.ballot_winners / frame.applicants
    if not p.between(0, 1).all() or (frame[['guaranteed_shares', 'ballot_extra_shares']] < 0).any().any():
        raise ValueError('Invalid outcome counts')
    if ((frame.guaranteed_shares + frame.ballot_extra_shares) > frame.applied_shares).any():
        raise ValueError('Allocation outcome exceeds applied units')
    if fee < 0 or not 0 <= borrowed_fraction < 1 or annual_rate < 0 or days < 0:
        raise ValueError('Invalid fee/financing scenario')
    d = frame.copy()
    delta = d.p1 - d.p0
    capital = d.applied_shares * d.p0
    cost = fee + capital * borrowed_fraction * annual_rate * days / 365
    d['prob_extra'] = p
    d['net_low'] = d.guaranteed_shares * delta - cost
    d['net_high'] = (d.guaranteed_shares + d.ballot_extra_shares) * delta - cost
    d['expected_net'] = (1-p) * d.net_low + p * d.net_high
    d['variance_net'] = p * (1-p) * (d.net_high-d.net_low)**2
    d['p_loss'] = (1-p) * (d.net_low < 0) + p * (d.net_high < 0)
    d['p_zero_net'] = (1-p) * (d.net_low == 0) + p * (d.net_high == 0)
    d['p_profit'] = (1-p) * (d.net_low > 0) + p * (d.net_high > 0)
    d['p_no_shares'] = (1-p) * (d.guaranteed_shares == 0) + p * ((d.guaranteed_shares + d.ballot_extra_shares) == 0)
    d['application_capital'] = capital
    d['expected_application_return'] = d.expected_net / capital
    d['fee_break_even_hkd'] = (1-p) * d.guaranteed_shares * delta + p * (d.guaranteed_shares+d.ballot_extra_shares) * delta
    return d


def simulate_portfolio(states, draws=SIMULATIONS, seed=SEED):
    """Independent ballots across IPOs, conditioned on observed price outcomes."""
    rng = np.random.default_rng(seed)
    values = []
    for start in range(0, draws, 5000):
        count = min(5000, draws-start)
        wins = rng.random((count, len(states))) < states.prob_extra.to_numpy()
        values.append(states.net_low.sum() + wins @ (states.net_high-states.net_low).to_numpy())
    return np.concatenate(values)


def decomposition(frame):
    """Population covariance with denominator N; purely descriptive identity."""
    z = frame[['alloc_rate', 'ir']].replace([np.inf, -np.inf], np.nan).dropna()
    a, r = z.alloc_rate, z.ir
    return {'n': len(z), 'mean_allocation': a.mean(), 'mean_ir': r.mean(),
            'product_of_means': a.mean()*r.mean(), 'mean_product': (a*r).mean(),
            'covariance': ((a-a.mean())*(r-r.mean())).mean()}


def cluster_mean_interval(frame, value, draws=2000, seed=SEED):
    z = frame[['month', value]].replace([np.inf, -np.inf], np.nan).dropna()
    groups = [part[value].to_numpy() for _, part in z.groupby('month', observed=True)]
    if len(groups) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    samples = [np.concatenate([groups[k] for k in rng.integers(0, len(groups), len(groups))]).mean() for _ in range(draws)]
    return tuple(np.quantile(samples, [.025, .975]))


def build_tier_frame(panel, tiers):
    data = panel.reset_index()[['Stock Code', 'listing_date', 'cohort', 'month', 'ir', 'sub_x',
                              'base_proceeds', 'ah_true', C['offer'], 'First trading day closing price (HK$)']]
    data = data.rename(columns={'Stock Code':'code', C['offer']:'p0', 'First trading day closing price (HK$)':'p1'})
    data['month'] = data.month.astype(str)
    data['size_group'] = pd.qcut(data.base_proceeds,3,labels=['small','mid','large'])
    frame = tiers.merge(data, on='code', validate='many_to_one')
    frame['alloc_rate'] = frame.expected_shares / frame.applied_shares
    return frame


def select_tiers(tiers, choices):
    z = choices[['code', 'applied_shares']].merge(tiers, on=['code', 'applied_shares'], validate='one_to_one')
    if len(z) != len(choices):
        raise ValueError('Selected application tier missing')
    return z


def a_robustness():
    d = demand.load_data()
    r = demand.prepare_regression(d)
    rows = []
    for label, subset in [('all', r), ('exclude_top3_ir', r.drop(r.y.nlargest(3).index)), ('non_ah', r[r.ah.eq(0)])]:
        z = subset[['y','lsub','lproc','ah','lage','corner','q2','q3','month']].replace([np.inf,-np.inf],np.nan).dropna()
        xs = ['lsub','lproc','lage','corner','q2','q3'] + (['ah'] if label != 'non_ah' else [])
        X = demand.sm.add_constant(z[xs], has_constant='add')
        if np.linalg.matrix_rank(X) != X.shape[1]:
            raise ValueError('Rank-deficient robustness design')
        fit = demand.sm.OLS(z.y, X).fit(cov_type='HC3')
        rows.append({'sample':label,'n':len(z),'g':z.month.nunique(),'b_lsub':fit.params.lsub,
                     'hc3_se':fit.bse.lsub,'hc3_p':fit.pvalues.lsub,
                     'ci_lower':fit.conf_int().loc['lsub',0], 'ci_upper':fit.conf_int().loc['lsub',1],
                     'wild_p':demand.wild_cluster_p(z.y.to_numpy(),X.to_numpy(),z.month.to_numpy(),list(X.columns).index('lsub'))})
    pd.DataFrame(rows).to_csv(OUT/'a_influence_regressions.csv',index=False)
    summary = []
    for dimension in ['cohort','ah_true','size_tercile']:
        for name, subset in d.groupby(dimension, observed=True):
            for heat, part in subset.groupby('demand_tercile',observed=True):
                summary.append({'dimension':dimension,'group':str(name),'demand':str(heat),'n':len(part),
                                'mean_ir':part.ir.mean(),'median_ir':part.ir.median(),'break_rate':part.is_break.mean()})
    pd.DataFrame(summary).to_csv(OUT/'a_subgroup_stability.csv',index=False)
    columns = ['Day-5 BHR from Day-1 close (%)','Day-20 BHR from Day-1 close (%)',
               'Day-5 wealth relative vs HSI','Day-20 wealth relative vs HSI']
    mature = d.replace([np.inf,-np.inf],np.nan).dropna(subset=columns).copy()
    mature['market_relative_day5'] = mature[columns[2]]-1
    mature['market_relative_day20'] = mature[columns[3]]-1
    mature['month'] = mature.month.astype(str)
    out = []
    for label, part in [('all',mature), *[(str(k),g) for k,g in mature.groupby('demand_tercile',observed=True)]]:
        for day, raw, adjusted in [(5,columns[0],'market_relative_day5'),(20,columns[1],'market_relative_day20')]:
            low, high = cluster_mean_interval(part,adjusted)
            out.append({'group':label,'day':day,'n':len(part),'g':part.month.nunique(),
                        'mean_bhr':part[raw].mean(),'median_bhr':part[raw].median(),
                        'mean_market_relative':part[adjusted].mean(),'median_market_relative':part[adjusted].median(),
                        'mean_ci_lower':low,'mean_ci_upper':high})
    pd.DataFrame(out).to_csv(OUT/'a_matched_aftermarket.csv',index=False)
    mature[['Stock Code','month','demand_tercile',*columns]].to_csv(OUT/'a_matched_sample.csv',index=False)
    return pd.DataFrame(rows),pd.DataFrame(out)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    panel, one, ten, budgets = baseline.load_strategies_data()
    tiers = build_tier_frame(panel,reviewed_tiers(ROOT))
    min_tiers = select_tiers(tiers,one)
    strict = min_tiers[min_tiers.code.isin(one.loc[one.is_exact_lot.eq(1),'code'])].copy()
    strategies = {'strict_one_lot':strict,'one_lot_or_minimum':min_tiers,
                  'one_lot_or_minimum_ex3355':min_tiers[min_tiers.code.ne('3355.HK')],
                  'ten_lot':select_tiers(tiers,ten)}
    for budget, group in budgets.groupby('budget'):
        strategies[f'budget_{int(budget)}'] = select_tiers(tiers,group[group.can_afford.eq(1)])
    portfolio_rows, state_frames, sensitivity = [], [], []
    for name, subset in strategies.items():
        # For budgets, skipped IPOs carry no fee or outcome, while N states counts participants.
        for fee in [0,28,88,100]:
            states = outcome_metrics(subset,fee)
            states['strategy'] = name; states['fee_hkd'] = fee
            state_frames.append(states)
            sims = simulate_portfolio(states)
            portfolio_rows.append({'strategy':name,'fee_hkd':fee,'n':len(states),
                'expected_total_net_hkd':states.expected_net.sum(),
                'mean_expected_net_hkd':states.expected_net.mean(),
                'std_total_net_hkd':np.sqrt(states.variance_net.sum()),
                'median_simulated_net_hkd':np.median(sims),'p_total_loss':(sims<0).mean(),
                'p05_net_hkd':np.quantile(sims,.05),'p95_net_hkd':np.quantile(sims,.95),
                'mean_applicant_loss_probability':states.p_loss.mean(),
                'share_negative_expected_net':states.expected_net.lt(0).mean(),
                'mean_application_return':states.expected_application_return.mean(),
                'gross_fee_break_even_mean':states.fee_break_even_hkd.mean()})
            if name=='one_lot_or_minimum' and fee==88:
                main_sims = sims
        for drop in [0,1,3]:
            z = outcome_metrics(subset,88).sort_values('fee_break_even_hkd',ascending=False).iloc[drop:]
            sensitivity.append({'strategy':name,'drop_highest_gross':drop,'n':len(z),
                                'mean_expected_net_hkd':z.expected_net.mean(),'total_expected_net_hkd':z.expected_net.sum()})
    portfolios = pd.DataFrame(portfolio_rows)
    portfolios.to_csv(OUT/'portfolio_distributions.csv',index=False)
    pd.concat(state_frames,ignore_index=True).to_csv(OUT/'applicant_outcomes.csv',index=False)
    pd.DataFrame(sensitivity).to_csv(OUT/'profit_concentration_sensitivity.csv',index=False)
    pd.DataFrame({'net_hkd':main_sims}).to_csv(OUT/'conditional_portfolio_draws_fee88.csv',index=False)
    dec_rows = []
    for strategy in ['strict_one_lot','one_lot_or_minimum','ten_lot']:
        z = strategies[strategy].copy()
        dec_rows.append({'strategy':strategy,'dimension':'all','group':'all',**decomposition(z)})
        for col in ['cohort','ah_true','size_group']:
            for group, part in z.groupby(col,observed=True):
                dec_rows.append({'strategy':strategy,'dimension':col,'group':str(group),**decomposition(part)})
    dec = pd.DataFrame(dec_rows)
    dec.to_csv(OUT/'allocation_return_decomposition.csv',index=False)
    bootstrap_rows = []
    for name in ['strict_one_lot', 'one_lot_or_minimum']:
        s = outcome_metrics(strategies[name], 88)
        lower, upper = cluster_mean_interval(s, 'expected_net')
        bootstrap_rows.append({'strategy': name, 'n': len(s), 'g': s.month.nunique(),
                               'mean_expected_net': s.expected_net.mean(),
                               'month_bootstrap_lower': lower, 'month_bootstrap_upper': upper})
    pd.DataFrame(bootstrap_rows).to_csv(OUT/'month_bootstrap_mean_net.csv', index=False)
    # Preserve untouched source page separately from the inserted guarantee wording.
    raw_pages = [json.loads(line) for line in (ROOT/'pipeline/prospectus_pipeline/data/allot/text/HKIPO-MB3355.jsonl').read_text().splitlines()]
    provenance = {'code': '3355.HK', 'method': 'guarantee inferred from printed rounded percentages and pool totals',
                  'new_independent_semantic_review': False,
                  'existing_review': 'pipeline/reports/data_gap_collection/allocation_review.json',
                  'original_pages': [page for page in raw_pages if page['page'] in (15,16)],
                  'derived_rows': tiers[tiers.code.eq('3355.HK') & tiers.pool.eq('B')][['applied_shares','guaranteed_shares','ballot_winners','applicants','ballot_extra_shares','printed_allocation_pct','rule_original']].to_dict('records')}
    (OUT/'3355_original_and_derived.json').write_text(json.dumps(provenance,indent=2)+'\n')
    frontier = []
    for name in ['strict_one_lot','one_lot_or_minimum','ten_lot','budget_10000','budget_50000','budget_100000']:
        subset = strategies[name]
        for fee in np.arange(0,201,5):
            s = outcome_metrics(subset,float(fee))
            frontier.append({'strategy':name,'fee_hkd':fee,'n':len(s),'mean_net_hkd':s.expected_net.mean(),
                             'median_net_hkd':s.expected_net.median(),'mean_p_loss':s.p_loss.mean(),
                             'negative_expected_share':s.expected_net.lt(0).mean()})
    fee_curve = pd.DataFrame(frontier)
    fee_curve.to_csv(OUT/'fee_frontier.csv',index=False)
    # Full size schedules are descriptive; do not choose tiers using observed returns.
    schedule = outcome_metrics(tiers,88)
    schedule.to_csv(OUT/'application_size_schedule_fee88.csv',index=False)
    finance = []
    for name in ['strict_one_lot','ten_lot']:
        for fee in [0,88,100]:
            for days in [2,5]:
                for rate in [.03,.06,.10]:
                    s = outcome_metrics(strategies[name],fee,.9,rate,days)
                    finance.append({'strategy':name,'fee_hkd':fee,'days_assumed':days,'annual_rate_assumed':rate,
                                    'borrowed_fraction':.9,'mean_expected_net_hkd':s.expected_net.mean(),
                                    'negative_expected_share':s.expected_net.lt(0).mean(),
                                    'mean_applicant_loss_probability':s.p_loss.mean()})
    pd.DataFrame(finance).to_csv(OUT/'financing_sensitivity.csv',index=False)
    a_reg,a_after=a_robustness()
    sources = {'checked_on':'2026-10-03','historical_cohort_charges_verified':False,
               'sources':[{'url':'https://www.futuhk.com/en/support/topic2_418from_platform%3D1%26%26lang%3Dzh-hk',
                           'current_schedule':'ordinary cash/Futu financing subscription handling 0; bank financing handling 100 HKD',
                           'scope':'handling fee only; interest and promotions may differ'},
                          {'url':'https://www.hsbc.com.hk/zh-hk/help/faq/investments/',
                           'current_schedule':'branch/IPO hotline application 100 HKD', 'scope':'channel-specific current quote'}],
               'fees_28_and_88':'unsourced hypothetical sensitivity values',
               'excluded_costs':['allotted-share subscription brokerage/levies','sale brokerage/levies','opportunity cost'],
               'financing':'90% borrowing, 2/5 days, 3/6/10 percent are assumptions; FINI does not determine account loan duration'}
    (OUT/'fee_sources.json').write_text(json.dumps(sources,indent=2)+'\n')
    fig, axes = plt.subplots(1,3,figsize=(13,4))
    axes[0].hist(main_sims,bins=80,color='#406b87');axes[0].axvline(0,color='black');axes[0].set_xlabel('Total net HKD, fee 88');axes[0].set_title('Conditional independent ballots')
    for name in ['strict_one_lot','ten_lot']:
        z=fee_curve[fee_curve.strategy.eq(name)]
        axes[1].plot(z.fee_hkd,z.mean_net_hkd,label=name)
    axes[1].axhline(0,color='black');axes[1].set_xlabel('Handling fee HKD');axes[1].set_ylabel('Mean expected net HKD');axes[1].legend()
    z=dec[(dec.strategy=='one_lot_or_minimum')&(dec.dimension=='all')].iloc[0]
    axes[2].bar(['Product of means','Covariance','Mean product'],100*np.array([z.product_of_means,z.covariance,z.mean_product]),color=['#406b87','#bc693d','#406b87'])
    axes[2].axhline(0,color='black');axes[2].set_ylabel('Percentage points');axes[2].tick_params(axis='x',labelrotation=20)
    fig.tight_layout();fig.savefig(OUT/'retail_profit_distribution.png',dpi=180);plt.close(fig)
    inputs=[baseline.TIERS_PATH,baseline.LOTS_PATH,ROOT/'pipeline/exports/HKIPO-MB-MASTER_clean.csv',
            baseline.TIERS_PATH.parent/'allocation_review.json',baseline.TIERS_PATH.parent/'allocation_tiers_candidates.csv',
            baseline.TIERS_PATH.parent/'allocation_coverage.csv',ROOT/'pipeline/registry/HKIPO_Variable_Registry.yaml',
            Path(__file__),Path(baseline.__file__),Path(demand.__file__),ROOT/'analysis/shared/allocation_review.py',ROOT/'analysis/shared/retail_report.py']
    manifest={'as_of':'2026-09-30','seed':SEED,'simulations':SIMULATIONS,'lottery_assumption':'independent across IPOs; observed prices fixed',
              'market_resampling':'2000 listing-month bootstrap draws, descriptive; few unequal clusters',
              'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
              'versions':{'numpy':np.__version__,'pandas':pd.__version__,'statsmodels':__import__('statsmodels').__version__},
              'outputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.csv')}}
    report = render_retail_report(portfolios, pd.DataFrame(sensitivity), dec,
                                  pd.DataFrame(bootstrap_rows), a_reg, a_after)
    (OUT/'research.md').write_text(report)
    canonical = ROOT/'docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md'
    canonical.parent.mkdir(parents=True, exist_ok=True)
    canonical.write_text(render_retail_report(portfolios, pd.DataFrame(sensitivity), dec,
                         pd.DataFrame(bootstrap_rows), a_reg, a_after,
                         results_prefix='../../analysis/out/retail_distribution', repo_prefix='../..'))
    manifest['outputs'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name != 'run_manifest.json'}
    manifest['outputs']['docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md'] = hashlib.sha256((ROOT/'docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md').read_bytes()).hexdigest()
    (OUT/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(portfolios[portfolios.strategy.isin(['strict_one_lot','one_lot_or_minimum'])].to_string(index=False))
    print('Research written:',OUT)


if __name__=='__main__':
    main()
