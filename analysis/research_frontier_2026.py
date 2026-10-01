"""Exploratory retail allocation economics, cornerstone sensitivity and coverage.

Design: docs/RESEARCH_DESIGN_2026.md. No causal treatment or preregistration claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

import academic_extensions_2026 as academic
import module_b_underpricing_regression as mb
import research_inputs
from research_inputs import prepare_extended, C as C, ROOT as ROOT, load_panel as load_panel, select_2026 as select_2026
from module_a_stylized_facts import (
    to_markdown,
)
from research_helpers.ipo_metrics import initial_returns
from research_helpers.regtable import regression_table

OUT = ROOT / 'analysis/out/research_frontier'
SEED = 20260930


def allocation_metrics(frame: pd.DataFrame) -> dict:
    """Separate offer-return, allocated-capital and application-capital denominators."""
    z = frame[['ir', 'allocation']].replace([np.inf, -np.inf], np.nan).dropna()
    z = z[(z.allocation > 0) & (z.allocation <= 1)]
    if z.empty:
        return {'n': 0, 'mean_ir': np.nan, 'allocation_weighted_ir': np.nan, 'application_return': np.nan}
    return {'n': len(z), 'mean_ir': z.ir.mean(),
            'allocation_weighted_ir': np.average(z.ir, weights=z.allocation),
            'application_return': (z.ir * z.allocation).mean()}


def point_sensitivity(fit, focus: str) -> dict:
    """Cinelli-Hazlett point-estimate sensitivity; classical OLS scale, no CI claim."""
    t2 = float(fit.tvalues[focus]) ** 2
    df = float(fit.df_resid)
    f2 = t2 / df
    rv = (np.sqrt(f2 * f2 + 4 * f2) - f2) / 2
    return {'partial_r2_y_d_given_x': t2 / (t2 + df), 'rv_to_zero_equal_strength': rv}


def ovb_magnitude(fit, focus: str, r2_yz: float, r2_dz: float) -> float:
    """Absolute coefficient bias from partial R² with residual outcome/treatment."""
    if not (0 <= r2_yz <= 1 and 0 <= r2_dz < 1):
        raise ValueError('partial R2 parameters outside their domain')
    return float(fit.bse[focus] * np.sqrt(fit.df_resid * r2_yz * r2_dz / (1 - r2_dz)))


def retail_analysis(sample: pd.DataFrame) -> str:
    prices = initial_returns(sample[C['offer']], sample['First trading day closing price (HK$)'])
    frame = pd.DataFrame({'code': sample['Stock Code'], 'month': sample.listing_date.dt.to_period('M').astype(str),
                          'ir': prices.ir, 'allocation': sample['Final public offer shares'] / sample['Public valid applied shares']})
    valid = np.isfinite(frame[['ir', 'allocation']]).all(axis=1) & frame.allocation.gt(0) & frame.allocation.le(1)
    frame['included'] = valid
    frame['exclusion_reason'] = np.where(valid, '', 'missing/nonfinite input or allocation outside (0,1]')
    frame.to_csv(OUT / 'retail_sample.csv', index=False)
    z = frame[valid].copy()
    if z.empty:
        raise ValueError("No valid allocation observations at this cutoff")
    summary = allocation_metrics(z)
    rng = np.random.default_rng(SEED)
    groups = [g for _, g in z.groupby('month')]
    draws = []
    for _ in range(2000):
        resampled = pd.concat([groups[k] for k in rng.integers(0, len(groups), len(groups))])
        draws.append(allocation_metrics(resampled))
    intervals = pd.DataFrame(draws).quantile([.025, .975])
    scenarios = []
    for fee in (0, 28, 88):
        for fraction in (0, .9):
            for rate in ((0,) if fraction == 0 else (0, .03, .06, .10)):
                cost = fee + 10000 * fraction * rate * 2 / 365
                gain = 10000 * z.allocation * z.ir - cost
                scenarios.append({'fee_hkd': fee, 'borrowed_fraction': fraction, 'annual_rate': rate,
                                  'days': 2, 'mean_net_gain_hkd': gain.mean(), 'median_net_gain_hkd': gain.median(),
                                  'share_negative': gain.lt(0).mean()})
    pd.DataFrame(scenarios).to_csv(OUT / 'retail_cost_scenarios.csv', index=False)
    rows = []
    for key in ('mean_ir', 'allocation_weighted_ir', 'application_return'):
        rows.append({'Measure': key, 'Estimate': summary[key], 'Cluster-bootstrap lower': intervals.loc[.025, key],
                     'Cluster-bootstrap upper': intervals.loc[.975, key]})
    table = pd.DataFrame(rows).set_index('Measure')
    table.to_csv(OUT / 'retail_summary.csv')
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.4))
    labels = ['Offer capital: equal-deal IR', 'Allocated capital: weighted IR', 'Application capital: return']
    for ax, key, label in zip(axes, table.index, labels):
        point = summary[key] * 100
        low, high = intervals.loc[.025, key] * 100, intervals.loc[.975, key] * 100
        ax.bar([0], [point], width=.5, color='#406b87')
        ax.errorbar([0], [point], yerr=[[point-low], [high-point]], fmt='none', color='black', capsize=5)
        ax.axhline(0, color='grey', lw=.7)
        ax.set_xticks([]); ax.set_ylabel('Return (%)'); ax.set_title(label, fontsize=9)
        ax.text(.05, .93, f'{point:.3f}%', transform=ax.transAxes, va='top')
    fig.suptitle(f'Different denominators and scales; N={len(z)}, month-cluster bootstrap intervals', fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / 'retail_denominators.png', dpi=200)
    plt.close(fig)
    return f'''## 零售申请资金与配售资金的收益

共同有效样本 N={summary['n']}，上市月份 G={len(groups)}；2,000 次按上市月重抽样，seed={SEED}。少月份区间仅作描述，不能消除市场冲击或信息类型选择。

{to_markdown(table.apply(lambda col: col.map(lambda value: f'{100 * value:.3f}%')), 'Measure')}

表中收益以百分比显示，CSV保留小数。申请 HK$10,000 的平均毛收益为 HK${10000 * summary['application_return']:.2f}。这是发行人层面平均配售率下的等额申请情景，不能当作一手中奖概率或实际账户收益。融资情景详见 retail_cost_scenarios.csv；费率、借款比例及2天占款是情景参数，未从真实借贷记录估计。未补入股票交易、申购交易费或机会成本；不能称完整净投资回报。
'''


def cornerstone_analysis(sample: pd.DataFrame) -> str:
    frame = prepare_extended(sample)
    frame['corner'] = frame.code.map(sample.set_index('Stock Code')[C['corner']])
    allocation = sample.set_index('Stock Code')['Final public offer shares'] / sample.set_index('Stock Code')['Public valid applied shares']
    # Quarantine allocation unit anomalies from new focal regressions too.
    frame = frame[~frame.code.isin(allocation[allocation > 1].index)].copy()
    control = ['corner', 'lproc', 'lage', 'ah', 'vc', 'hot']
    z = frame.replace([np.inf, -np.inf], np.nan).dropna(subset=['y', 'month', *control, 'lsub']).copy()
    z[['code', 'month', 'y', *control, 'lsub']].to_csv(OUT / 'cornerstone_sample.csv', index=False)
    models, results, scenarios = [], [], []
    for name, xs in [('Ex-ante controls', control), ('+ final demand (endogenous)', [*control, 'lsub'])]:
        x = sm.add_constant(z[xs].astype(float), has_constant='add')
        if np.linalg.matrix_rank(x) < x.shape[1] or len(x) <= x.shape[1]:
            raise ValueError('Rank/df failure in cornerstone design')
        leverage = np.einsum('ij,ji->i', x, np.linalg.pinv(x))
        if leverage.max() >= 1 - 1e-9:
            raise ValueError('Unit leverage; HC3 is undefined')
        ordinary = sm.OLS(z.y, x).fit()
        robust = sm.OLS(z.y, x).fit(cov_type='HC3')
        clustered = ordinary.get_robustcov_results(cov_type='cluster', groups=z.month, use_correction=True, use_t=True)
        assert list(robust.model.data.row_labels) == list(z.index)
        j = list(x.columns).index('corner')
        wild = mb.wild_cluster_p(z.y.to_numpy(float), x.to_numpy(), z.month.to_numpy(), j)
        results.append({'Specification': name, 'n': len(z), 'g': z.month.nunique(), 'b': robust.params['corner'],
                        'hc3_se': robust.bse['corner'], 'hc3_p': robust.pvalues['corner'],
                        'cr1_p': clustered.pvalues[j], 'restricted_wild_p': wild,
                        'max_leverage': leverage.max(), **point_sensitivity(ordinary, 'corner')})
        for r2 in (.01, .05, .10):
            bias = ovb_magnitude(ordinary, 'corner', r2, r2)
            scenarios.append({'specification': name, 'r2_yz': r2, 'r2_dz': r2, 'bias_magnitude': bias,
                              'b_toward_zero': ordinary.params['corner'] - np.sign(ordinary.params['corner']) * bias})
        models.append(robust)
    result = pd.DataFrame(results).set_index('Specification')
    result['holm_hc3_p'] = multipletests(result.hc3_p, method='holm')[1]
    result.to_csv(OUT / 'cornerstone_sensitivity.csv')
    pd.DataFrame(scenarios).to_csv(OUT / 'ovb_scenarios.csv', index=False)
    (OUT / 'cornerstone_regressions.tex').write_text(regression_table(
        models, keep=control + ['lsub'], stars=False, depvar='log(1+IR)',
        extra_rows={'Listing-month clusters': [str(z.month.nunique())] * 2},
        notes='HC3 standard errors. Observational associations; common sample. Wild-cluster p-values and point-estimate sensitivity are reported separately.'))
    display = result[['n', 'g', 'b', 'hc3_se', 'hc3_p', 'restricted_wild_p', 'rv_to_zero_equal_strength']].copy()
    for col in display:
        display[col] = display[col].map((lambda value: str(int(value))) if col in ('n', 'g') else (lambda value: f'{value:.3f}'))
    return f'''## 基石份额：关联、少聚类推断与遗漏变量

{to_markdown(display, 'Specification')}

两个规格共用同一发行人样本。焦点变化0.10对应 log(1+IR) 变化0.10×b，exp(0.10×b)-1是价格比(1+IR)的比例变化，不是 IR 百分点。wild 检验沿用已验证的 restricted bootstrap-t，枚举 G 个上市月的全部 Rademacher 符号组合；HC3 的两个焦点检验独立作为 Holm family，聚类 p 不混用于星号。

RV/partial-R² 是点估计对未观测混杂的代数诊断，使用普通 OLS 的残差尺度，不是聚类显著性或因果置信区间。最终需求和基石份额均内生；加入需求可能条件化于通道或碰撞点。任意一个显著结果都不能修复识别。
'''


def event_readiness(sample: pd.DataFrame, as_of: str) -> None:
    cutoff = pd.Timestamp(as_of)
    frames, _ = academic.load_event_frame(sample, as_of)
    d = academic.build_frame(sample).set_index('code')
    rows = []
    for _, issuer in sample.iterrows():
        code = issuer['Stock Code']; event = d.loc[code, 'lockup_date']; frame = frames.get(code)
        status = 'missing_event_date'
        actual = pd.NaT
        if pd.notna(event):
            if event > cutoff:
                status = 'immature_event'
            elif frame is None:
                status = 'missing_market_data'
            else:
                idx = academic.event_index(frame, event)
                if idx is None:
                    status = 'post_event_data_missing'
                elif idx < 6 or idx + 5 >= len(frame):
                    status = 'incomplete_window'
                else:
                    actual = frame.index[idx]
                    status = 'complete' if np.isfinite(academic.window_car(frame, idx, -5, 5, 'ex_hsi')) else 'missing_return_or_benchmark'
        target = issuer.listing_date + pd.DateOffset(months=6)
        horizon = 'immature_calendar_horizon' if target > cutoff else 'mature_but_market_endpoint_missing'
        if target <= cutoff and frame is not None and (frame.index >= target).any():
            horizon = 'observed_calendar_endpoint'
        rows.append({'code': code, 'listing_date': issuer.listing_date, 'cohort': issuer.cohort,
                     'event_date_workbook': event, 'event_trade_date': actual, 'event_status': status,
                     'event_date_provenance': 'workbook date; contract not independently reverified in this run',
                     'six_month_target': target, 'six_month_status': horizon,
                     'cached_last_date': frame.index[-1] if frame is not None else pd.NaT, 'as_of': as_of})
    pd.DataFrame(rows).to_csv(OUT / 'event_readiness.csv', index=False)
    cross = pd.crosstab([d.r18c, d.fixed], d.mech, dropna=False)
    cross.to_csv(OUT / 'mechanism_support.csv')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of', default='2026-09-30')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    sample = select_2026(load_panel())
    sample = sample[sample.listing_date <= pd.Timestamp(args.as_of)].copy()
    if sample.empty:
        raise ValueError("No 2026 listings observed at the requested cutoff")
    report = '# 2026 研究前沿：探索性实证\n\n设计见 docs/RESEARCH_DESIGN_2026.md；不作因果或预注册声明。\n\n'
    report += retail_analysis(sample) + cornerstone_analysis(sample)
    event_readiness(sample, args.as_of)
    report += '\n事件与六日历月窗口覆盖见 event_readiness.csv；机制共同支持见 mechanism_support.csv。缺证据和未成熟分别保留，不填估计。\n'
    (OUT / 'research.md').write_text(report)
    market_inputs = [academic.et.BARS / name for name in ('hsi_bars.json', 'hstech_bars.json')]
    market_inputs += [academic.et.BARS / f"hk{code.split('.')[0].zfill(5)}.json" for code in sample['Stock Code']]
    manifest = {'as_of': args.as_of, 'seed': SEED, 'sample_n': len(sample),
                'event_market_inputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in market_inputs if p.exists()},
                'missing_event_market_inputs': [str(p.relative_to(ROOT)) for p in market_inputs if not p.exists()],
                'versions': {'numpy': np.__version__, 'pandas': pd.__version__, 'statsmodels': sm.__version__ if hasattr(sm, '__version__') else __import__('statsmodels').__version__},
                'inputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT / 'pipeline/exports/HKIPO-MB-MASTER_clean.csv', ROOT / 'docs/RESEARCH_DESIGN_2026.md',
                                     ROOT / 'pipeline/reports/margin_review/market_source_manifest.json',
                                     Path(__file__).resolve(), Path(academic.__file__).resolve(),
                                     Path(research_inputs.__file__).resolve())},
                'skill_helpers': json.loads((Path(__file__).parent / 'research_helpers/PROVENANCE.json').read_text())}
    (OUT / 'run_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('Research frontier written:', OUT)


if __name__ == '__main__':
    main()
