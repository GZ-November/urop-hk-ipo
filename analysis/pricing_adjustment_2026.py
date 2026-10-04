"""Explore price adjustment and strictly timed retail information in 2026.

No source-field writeback, investment simulation, or causal identification.
Reuses research_helpers.ipo_metrics and shared.inference from this repository.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

from research_inputs import ROOT, MASTER, load_panel, select_2026
from research_helpers.ipo_metrics import price_revision
from shared.inference import wild_cluster_p

OUT = ROOT / 'analysis/out/pricing_adjustment'
FROZEN = ROOT / 'analysis/out/retail_mechanisms/return_stages/issuer_sample.csv'
MARGIN = ROOT / 'pipeline/exports/HKIPO-2026-margin-daily.csv'
HSI = ROOT / 'pipeline/prospectus_pipeline/data/market/first_day_returns/hsi_bars.json'
RANGE_OUTCOMES = ['log_close', 'log_opening', 'log_intraday', 'allocation_rate',
                  'application_return', 'log_mair_subscription', 'close']
MODELS = {
    'revision_only': ['revision'],
    'quarter_controls': ['revision', 'q2', 'q3'],
    'launch_size_and_ah': ['revision', 'log_planned_proceeds', 'ah_true'],
    'subscription_market_and_size': ['revision', 'log_subscription_market', 'log_planned_proceeds'],
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def classify_prices(low, high):
    status = pd.Series('invalid_or_missing', index=low.index)
    valid = low.gt(0) & high.gt(0)
    status.loc[valid & high.gt(low)] = 'two_sided_range'
    status.loc[valid & high.eq(low)] = 'equal_endpoints'
    status.loc[low.isna() & high.gt(0)] = 'undisclosed_lower_bound'
    return status


def build_sample():
    master = select_2026(load_panel()).copy()
    frozen = pd.read_csv(FROZEN)
    assert len(master) == len(frozen) == 113
    assert set(master['Stock Code']) == set(frozen.code)
    wanted = ['Stock Code', 'Minimum Offer Price', 'Maximum Offer Price',
              'Global Offering (without option)', 'Pricing position in filing range',
              'Filing price revision (%)', 'Pricing date', 'Date of Prospectus (dd/mm/yy)',
              'Subscription opening date', 'Subscription closing date',
              'HSI return over 20 trading days before prospectus (%)']
    current = master[wanted].rename(columns={'Subscription closing date': 'current_subscription_close'})
    d = frozen.merge(current, left_on='code', right_on='Stock Code', validate='one_to_one')
    check = master.set_index('Stock Code').reindex(d.code)
    for frozen_col, master_col in [('offer_price', 'IPO Subscription Price (HK$)'),
                                  ('first_day_close', 'First trading day closing price (HK$)')]:
        assert np.allclose(d[frozen_col], check[master_col], rtol=0, atol=1e-10)
    d['range_low'] = d['Minimum Offer Price']
    d['range_high'] = d['Maximum Offer Price']
    d['price_status'] = classify_prices(d.range_low, d.range_high)
    assert not d.price_status.eq('invalid_or_missing').any()
    metrics = price_revision(d.offer_price, d.range_low, d.range_high)
    eligible = d.price_status.eq('two_sided_range')
    d['midpoint'] = ((d.range_low + d.range_high) / 2).where(eligible)
    d['revision'] = metrics.pr_mid.where(eligible)
    d['range_position'] = metrics.range_pos
    d['range_width'] = ((d.range_high - d.range_low)/d.midpoint).where(eligible)
    d['log_revision'] = np.log1p(d.revision)
    d['log_midpoint_close'] = np.log(d.first_day_close/d.midpoint)
    d['pricing_group'] = np.select([
        eligible & np.isclose(d.offer_price, d.range_low),
        eligible & np.isclose(d.offer_price, d.range_high), eligible],
        ['At low', 'At high', 'Inside range'], default='No two-sided range')
    assert np.allclose(d.loc[eligible, 'revision'], d.loc[eligible, 'Filing price revision (%)'], atol=1e-6)
    d['q2'] = d.quarter.eq('2026Q2').astype(float)
    d['q3'] = d.quarter.eq('2026Q3').astype(float)
    d['prospectus_date'] = pd.to_datetime(d['Date of Prospectus (dd/mm/yy)'])
    d['subscription_close_date'] = pd.to_datetime(d['Subscription closing date'])
    assert d.subscription_close_date.eq(pd.to_datetime(d.current_subscription_close)).all()
    d['listing_date'] = pd.to_datetime(d.listing_date)
    d['month'] = d.listing_date.dt.to_period('M').astype(str)
    d['planned_offer_units'] = d['Global Offering (without option)']
    # Launch measure: filed global quantity times midpoint, or published ceiling.
    reference = d.midpoint.fillna(d.range_high)
    d['planned_proceeds'] = d.planned_offer_units*reference
    d['log_planned_proceeds'] = np.log(d.planned_proceeds/1e9)
    bars = pd.DataFrame(json.loads(HSI.read_text())).sort_values('date')
    bars['date'] = pd.to_datetime(bars.date)
    def index_at_or_before(day):
        history = bars[bars.date.le(day)]
        if history.empty:
            raise ValueError('Missing HSI endpoint')
        return history.iloc[-1]['close']
    d['hsi_prospectus_close'] = d.prospectus_date.map(index_at_or_before)
    d['hsi_subscription_close'] = d.subscription_close_date.map(index_at_or_before)
    assert np.allclose(d.hsi_subscription_close,
                       d['First-day HSI subscription-close index close'], atol=.05, rtol=0)
    d['log_subscription_market'] = np.log(d.hsi_subscription_close/d.hsi_prospectus_close)
    # Full requested principal at the published maximum; brokerage/levies excluded.
    d['ceiling_principal_return'] = d.application_return*d.offer_price/d.range_high
    assert d.offer_price.le(d.range_high+1e-8).all()
    assert np.allclose(d.log_close, d.log_opening+d.log_intraday, atol=1e-12)
    assert np.allclose(d.loc[eligible, 'log_midpoint_close'],
                       d.loc[eligible, 'log_revision']+d.loc[eligible, 'log_close'], atol=1e-12)
    return d


def source_audit(d):
    downloads = json.loads((ROOT/'pipeline/prospectus_pipeline/out/downloaded.json').read_text())
    urls = {str(x['code']).split('.')[0].zfill(4): x.get('pdf_url', '') for x in downloads}
    records, paths = [], []
    for _, row in d.iterrows():
        code = row.code.split('.')[0]
        path = ROOT/f'pipeline/prospectus_pipeline/out/extracted/HKIPO-MB{code}.json'
        fields = json.loads(path.read_text())['fields']
        paths.append(path)
        for name, key in [('range_high', 'col_T'), ('range_low', 'col_U'),
                          ('planned_offer_units', 'col_M')]:
            f = fields.get(key, {})
            value = pd.to_numeric(pd.Series([f.get('value')]), errors='coerce').iloc[0]
            expected = row[name]
            missing = pd.isna(value) and pd.isna(expected)
            match = missing or np.isclose(value, expected, rtol=1e-10, atol=1e-8)
            if not match:
                raise ValueError(f'{row.code}: {name} disagrees with extraction')
            records.append({'code': row.code, 'field': name, 'value': expected,
                            'status': 'both_missing_not_verified' if missing else 'extracted_value_matches_master',
                            'page': f.get('page'), 'quote': f.get('quote', ''),
                            'source_url': urls.get(code, ''), 'extraction_sha256': digest(path)})
    pd.DataFrame(records).to_csv(OUT/'source_audit.csv', index=False)
    return paths


def estimate(d, outcome, xs, focus):
    columns = [outcome, 'month', *xs]
    if d[columns].isna().any().any():
        raise ValueError('Specify a common complete sample before estimation')
    x = sm.add_constant(d[xs], has_constant='add')
    if np.linalg.matrix_rank(x) != x.shape[1]:
        raise ValueError('Rank-deficient design')
    fit = sm.OLS(d[outcome], x).fit()
    robust = fit.get_robustcov_results(cov_type='HC3')
    j = list(x.columns).index(focus)
    return fit, {
        'outcome': outcome, 'focus': focus, 'coefficient': fit.params[focus],
        'hc3_se': robust.bse[j], 'hc3_p': robust.pvalues[j],
        'wild_cluster_p': wild_cluster_p(d[outcome].to_numpy(), x.to_numpy(), d.month.to_numpy(), j),
        'n': len(d), 'month_clusters': d.month.nunique(), 'adjusted_r2': fit.rsquared_adj,
        'max_leverage': fit.get_influence().hat_matrix_diag.max(),
    }


def descriptive(d):
    rows = []
    for grouping in ['price_status', 'pricing_group']:
        for group, g in d.groupby(grouping):
            rows.append({'grouping': grouping, 'group': group, 'n': len(g),
                         'mean_close': g['close'].mean(), 'median_close': g['close'].median(),
                         'mean_opening': g.opening.mean(), 'mean_intraday': g.intraday.mean(),
                         'mean_allocation': g.allocation_rate.mean(),
                         'mean_application_return': g.application_return.mean(),
                         'median_application_return': g.application_return.median(),
                         'mean_ceiling_principal_return': g.ceiling_principal_return.mean()})
    result = pd.DataFrame(rows)
    result.to_csv(OUT/'group_statistics.csv', index=False)
    return result


def range_analysis(d):
    z = d[d.price_status.eq('two_sided_range')].copy()
    assert len(z) == 43
    assert z[RANGE_OUTCOMES+['revision', 'log_planned_proceeds', 'ah_true']].notna().all().all()
    results, coefs = [], []
    for name, xs in MODELS.items():
        for outcome in RANGE_OUTCOMES:
            fit, result = estimate(z, outcome, xs, 'revision')
            result['model'] = name
            results.append(result)
            for term in fit.params.index:
                coefs.append({'model': name, 'outcome': outcome, 'term': term,
                              'coefficient': fit.params[term]})
    table = pd.DataFrame(results)
    primary = table.model.eq('quarter_controls')
    table.loc[primary, 'holm_hc3_p'] = multipletests(table.loc[primary, 'hc3_p'], method='holm')[1]
    table.loc[primary, 'holm_wild_p'] = multipletests(table.loc[primary, 'wild_cluster_p'], method='holm')[1]
    table.to_csv(OUT/'range_regressions.csv', index=False)
    pd.DataFrame(coefs).to_csv(OUT/'range_coefficients.csv', index=False)
    # Deterministic exclusions keep all outcomes and controls identical within a run.
    sensitivities = []
    masks = {'full': pd.Series(True, index=z.index),
             'without_top_three_close_returns': ~z.index.isin(z.nlargest(3, 'close').index),
             'without_top_three_application_returns': ~z.index.isin(z.nlargest(3, 'application_return').index)}
    for q in sorted(z.quarter.unique()):
        masks[f'without_{q}'] = z.quarter.ne(q)
    for name, mask in masks.items():
        t = z.loc[mask]
        xs = ['revision']+[c for c in ['q2', 'q3'] if t[c].nunique()>1]
        # Avoid a constant and both quarter dummies when Q1 has been removed.
        if t.quarter.nunique()==2 and t.q2.nunique()>1 and t.q3.nunique()>1:
            xs.remove('q3')
        for outcome in RANGE_OUTCOMES:
            _, result = estimate(t, outcome, xs, 'revision')
            result['exclusion'] = name
            sensitivities.append(result)
    for code in z.code:
        t = z[z.code.ne(code)]
        for outcome in ['log_close', 'log_intraday', 'application_return']:
            x = sm.add_constant(t[['revision','q2','q3']])
            fit = sm.OLS(t[outcome], x).fit()
            sensitivities.append({'outcome': outcome, 'coefficient': fit.params.revision,
                                  'n': len(t), 'exclusion': f'leave_out_{code}'})
    pd.DataFrame(sensitivities).to_csv(OUT/'range_sensitivity.csv', index=False)
    identity = []
    for y in ['log_close', 'log_opening', 'log_intraday', 'log_midpoint_close']:
        fit, result = estimate(z, y, ['log_revision', 'q2', 'q3'], 'log_revision')
        identity.append(result)
    identity = pd.DataFrame(identity)
    b = identity.set_index('outcome').coefficient
    assert np.isclose(b.log_close, b.log_opening+b.log_intraday)
    assert np.isclose(b.log_midpoint_close, 1+b.log_close)
    identity.to_csv(OUT/'midpoint_identity.csv', index=False)
    return table


def margin_sample(d, raw):
    raw = raw.copy()
    raw['published_day'] = pd.to_datetime(raw.published_date)
    raw['closing_day'] = pd.to_datetime(raw.subscription_close_date)
    # A date strictly before closing day is safe without a within-day timestamp.
    eligible = raw.available_before_deadline.eq('yes_published_before_closing_day')
    eligible &= raw.published_day.lt(raw.closing_day)
    raw['included_for_timed_analysis'] = eligible
    raw.to_csv(OUT/'margin_timing_audit.csv', index=False)
    latest = raw[eligible].sort_values(['stock_code','published_day','date']).groupby('stock_code').tail(1)
    t = d.merge(latest[['stock_code', 'margin_multiple', 'published_date', 'source', 'scope_class']],
                left_on='code', right_on='stock_code', validate='one_to_one')
    assert len(t) == 25 and t.margin_multiple.gt(0).all()
    t['log_margin'] = np.log(t.margin_multiple)
    t.to_csv(OUT/'margin_sample.csv', index=False)
    results = []
    for name, xs in [('margin_only', ['log_margin']),
                     ('margin_and_launch_size', ['log_margin','log_planned_proceeds'])]:
        for outcome in ['log_close','allocation_rate','ceiling_principal_return']:
            _, result = estimate(t, outcome, xs, 'log_margin')
            result['model'] = name
            results.append(result)
    result = pd.DataFrame(results)
    adjusted = result.model.eq('margin_and_launch_size')
    result.loc[adjusted, 'holm_hc3_p'] = multipletests(result.loc[adjusted, 'hc3_p'], method='holm')[1]
    result.loc[adjusted, 'holm_wild_p'] = multipletests(result.loc[adjusted, 'wild_cluster_p'], method='holm')[1]
    result.to_csv(OUT/'margin_regressions.csv', index=False)
    d['margin_covered'] = d.code.isin(t.code)
    coverage = d.groupby('month').agg(issuers=('code','size'), covered=('margin_covered','sum'))
    coverage.to_csv(OUT/'margin_coverage.csv')
    return result


def rolling_assessment(d, minimum_training=40):
    """Retrospective temporal exercise; all current data were previously explored.

    Train only on deals whose first-day close precedes the target prospectus date.
    This enforces time order, but it is not a new untouched holdout or a strategy.
    """
    rows = []
    for _, target in d.sort_values(['prospectus_date','code']).iterrows():
        train = d[d.listing_date.lt(target.prospectus_date)]
        if len(train) < minimum_training:
            continue
        features = ['log_planned_proceeds','ah_true']
        x = sm.add_constant(train[features], has_constant='add')
        fit = sm.OLS(train.ceiling_principal_return, x).fit()
        xt = np.array([1.,target.log_planned_proceeds,target.ah_true])
        rows.append({'code': target.code, 'cutoff': target.prospectus_date.date(),
                     'training_n': len(train), 'latest_training_listing': train.listing_date.max().date(),
                     'training_codes': ';'.join(sorted(train.code)),
                     'actual': target.ceiling_principal_return,
                     'expanding_mean': train.ceiling_principal_return.mean(),
                     'launch_size_and_ah': float(xt@fit.params.to_numpy())})
    predictions = pd.DataFrame(rows)
    predictions.to_csv(OUT/'rolling_predictions.csv', index=False)
    assert pd.to_datetime(predictions.latest_training_listing).lt(pd.to_datetime(predictions.cutoff)).all()
    y = predictions.actual
    baseline_sse = ((y-predictions.expanding_mean)**2).sum()
    summary = []
    for model in ['expanding_mean','launch_size_and_ah']:
        error = y-predictions[model]
        summary.append({'model': model, 'n':len(y), 'mae':error.abs().mean(),
                        'rmse': np.sqrt((error**2).mean()),
                        'relative_mse_gain': 1-(error**2).sum()/baseline_sse,
                        'mean_prediction': predictions[model].mean(), 'mean_actual':y.mean()})
    summary = pd.DataFrame(summary)
    summary.to_csv(OUT/'rolling_summary.csv', index=False)
    return summary


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d = build_sample()
    paths = source_audit(d)
    descriptive(d)
    range_results = range_analysis(d)
    margin_results = margin_sample(d, pd.read_csv(MARGIN))
    rolling = rolling_assessment(d)
    d.to_csv(OUT/'issuer_sample.csv', index=False)
    paths += [MASTER,FROZEN,MARGIN,HSI,ROOT/'pipeline/registry/HKIPO_Variable_Registry.yaml',
              ROOT/'pipeline/prospectus_pipeline/out/downloaded.json',Path(__file__),
              ROOT/'analysis/pricing_adjustment_report.py',
              ROOT/'analysis/specifications/pricing_adjustment.md']
    manifest = {'prepared_on':'2026-10-04','cutoff':'2026-09-30','n':len(d),
                'price_status_counts':d.price_status.value_counts().to_dict(),
                'input_sha256':{str(p.relative_to(ROOT)):digest(p) for p in paths},
                'inference':'HC3 with t reference; restricted wild cluster-t, exact Rademacher signs; Holm families',
                'scope':'Exploratory associations and retrospective temporal assessment. No causal or untouched-holdout claim.',
                'versions':{'pandas':pd.__version__,'numpy':np.__version__,'statsmodels':sm.__version__ if hasattr(sm,'__version__') else __import__('statsmodels').__version__}}
    (OUT/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Completed Topic 1 has a dedicated builder; preserve the open editor source.
    print('Report generation: run analysis/pricing_topic1_report.py for Topic 1.')
    print('Price status:',manifest['price_status_counts'])
    print(range_results[range_results.model.eq('quarter_controls')].to_string(index=False))
    print(margin_results[margin_results.model.eq('margin_and_launch_size')].to_string(index=False))
    print(rolling.to_string(index=False))


if __name__=='__main__':
    main()
