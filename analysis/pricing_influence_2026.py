"""Topic 1, step 3: exact influence audit for the seven missing pricing proxies.

All exclusions are diagnostic. Full 43-IPO results remain the main estimates.
No source writeback, imputation, selection strategy or causal claim.
"""
from pathlib import Path
from itertools import combinations
from math import factorial
import hashlib
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/out/pricing_adjustment/steps'
OUTCOMES=['log_close','log_opening','log_intraday']


def fit(rows,outcome):
    x=sm.add_constant(rows[['revision','q2','q3']],has_constant='add')
    assert np.linalg.matrix_rank(x)==x.shape[1]
    return sm.OLS(rows[outcome],x).fit()


def shapley_values(values,codes):
    """Exact average marginal coefficient change over every deletion order."""
    n=len(codes);result={}
    for code in codes:
        others=[x for x in codes if x!=code]
        total=0.
        for k in range(n):
            weight=factorial(k)*factorial(n-k-1)/factorial(n)
            for subset in combinations(others,k):
                key=frozenset(subset)
                total+=weight*(values[key|{code}]-values[key])
        result[code]=total
    assert np.isclose(sum(result.values()),values[frozenset(codes)]-values[frozenset()],atol=1e-10)
    return result


def main():
    input_path=ROOT/'analysis/out/pricing_adjustment/issuer_sample.csv'
    d=pd.read_csv(input_path);d=d[d.price_status.eq('two_sided_range')].copy()
    missing=sorted(d.loc[d['Pricing date'].isna(),'code']);assert len(d)==43 and len(missing)==7
    d['pricing_proxy_missing']=d.code.isin(missing)
    # Fixed specification; diagnostics for every issuer and every price stage.
    influence=[];fwl=[]
    controls=sm.add_constant(d[['q2','q3']],has_constant='add')
    xr=sm.OLS(d.revision,controls).fit().resid
    sxx=float(xr@xr)
    for outcome in OUTCOMES:
        model=fit(d,outcome);inf=model.get_influence()
        yr=sm.OLS(d[outcome],controls).fit().resid
        per=xr*yr/sxx
        assert np.isclose(per.sum(),model.params['revision'])
        for k,(_,r) in enumerate(d.iterrows()):
            influence.append({'code':r.code,'outcome':outcome,'pricing_proxy_missing':r.pricing_proxy_missing,
                              'leverage':inf.hat_matrix_diag[k],'cooks_distance':inf.cooks_distance[0][k],
                              'studentized_external_residual':inf.resid_studentized_external[k],
                              'revision_dfbeta':inf.dfbetas[k,1],
                              'coefficient_after_single_deletion':fit(d[d.code.ne(r.code)],outcome).params['revision']})
            fwl.append({'code':r.code,'outcome':outcome,'pricing_proxy_missing':r.pricing_proxy_missing,
                        'residualized_revision':xr.iloc[k],'residualized_outcome':yr.iloc[k],
                        'full_sample_slope_contribution':per.iloc[k]})
    subsets=[];values={key:{} for key in OUTCOMES}
    for k in range(8):
        for subset in combinations(missing,k):
            retained=d[~d.code.isin(subset)]
            results={outcome:fit(retained,outcome).params['revision'] for outcome in OUTCOMES}
            assert np.isclose(results['log_close'],results['log_opening']+results['log_intraday'])
            for outcome,beta in results.items():
                values[outcome][frozenset(subset)]=beta
                subsets.append({'excluded_codes':';'.join(subset),'excluded_n':len(subset),
                                'retained_n':len(retained),'outcome':outcome,'revision_coefficient':beta})
    contributions=[]
    for outcome in OUTCOMES:
        for code,val in shapley_values(values[outcome],missing).items():
            contributions.append({'code':code,'outcome':outcome,'shapley_deletion_effect':val})
    effects=pd.DataFrame(contributions).pivot(index='code',columns='outcome',values='shapley_deletion_effect')
    assert np.allclose(effects.log_close,effects.log_opening+effects.log_intraday)
    summary=[]
    prominent=['2672.HK','3231.HK']
    for label,exclude in [('All range offers',[]),('Remove all seven missing proxies',missing),
                          ('Remove 2672 only',['2672.HK']),('Remove 3231 only',['3231.HK']),
                          ('Remove 2672 and 3231',prominent),
                          ('Remove other five missing proxies',[c for c in missing if c not in prominent])]:
        retained=d[~d.code.isin(exclude)]
        for outcome in OUTCOMES:
            model=fit(retained,outcome);robust=model.get_robustcov_results(cov_type='HC3',use_t=True)
            summary.append({'sample':label,'outcome':outcome,'n':len(retained),
                            'coefficient':model.params['revision'],'hc3_se':robust.bse[1],
                            'hc3_t_p':robust.pvalues[1],'mean_raw_close':retained.close.mean()})
    groups=d.groupby('pricing_proxy_missing').agg(n=('code','size'),mean_revision=('revision','mean'),
         mean_close=('close','mean'),median_close=('close','median'),mean_opening=('opening','mean'),
         mean_log_close=('log_close','mean'),mean_log_opening=('log_opening','mean'),mean_log_intraday=('log_intraday','mean'))
    quarters=pd.crosstab(d.pricing_proxy_missing,d.quarter)
    d[d.pricing_proxy_missing][['code','quarter','revision','close','opening','intraday','log_close','log_opening','log_intraday']].to_csv(OUT/'step03_seven_issuer_profiles.csv',index=False)
    for name,frame in [('influence',pd.DataFrame(influence)),('fwl_contributions',pd.DataFrame(fwl)),
                       ('all_deletion_subsets',pd.DataFrame(subsets)),('shapley_contributions',pd.DataFrame(contributions)),
                       ('diagnostic_models',pd.DataFrame(summary)),('availability_groups',groups.reset_index()),
                       ('availability_quarters',quarters.reset_index())]:
        frame.to_csv(OUT/('step03_'+name+'.csv'),index=False)
    checks=[];source_paths=[]
    for code in prominent:
        row=d[d.code.eq(code)].iloc[0]
        market=ROOT/('pipeline/prospectus_pipeline/data/market/hk'+code.split('.')[0].zfill(5)+'.json')
        bars=json.loads(market.read_text());bar=next(b for b in bars if b['date']==row.listing_date)
        assert bar.get('price_basis')=='raw_as_traded'
        assert np.isclose(bar['open'],row['First trading day opening price (HK$)'])
        assert np.isclose(bar['close'],row.first_day_close)
        extraction=ROOT/('pipeline/prospectus_pipeline/out/extracted/HKIPO-MB'+code.split('.')[0]+'.json')
        fields=json.loads(extraction.read_text())['fields']
        assert np.isclose(fields['col_T']['value'],row.range_high)
        assert np.isclose(fields['col_U']['value'],row.range_low)
        allot=ROOT/('pipeline/prospectus_pipeline/data/allot/text/HKIPO-MB'+code.split('.')[0]+'.jsonl')
        pages=[json.loads(line) for line in allot.read_text().splitlines()]
        page=next(p for p in pages if p['page']==2)
        text=' '.join(page['text'].split())
        assert 'Final Offer Price' in text and str(f'{row.offer_price:.2f}') in text
        checks.append({'code':code,'offer_price':row.offer_price,'range_low':row.range_low,'range_high':row.range_high,
                       'raw_open':bar['open'],'raw_close':bar['close'],'listing_date':bar['date'],
                       'market_source_url':bar.get('source_url'),'allotment_pdf_page':2,
                       'basis':'Final offer price checked in stored allotment text; raw market prices match cache; endpoints match stored extraction, not a new full semantic certification.'})
        source_paths.extend([market,extraction,allot])
    pd.DataFrame(checks).to_csv(OUT/'step03_two_issuer_price_checks.csv',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    data=pd.DataFrame(fwl);data=data[data.outcome.eq('log_close')]
    fig,ax=plt.subplots(figsize=(7.2,4.7),layout='constrained')
    for missing_flag,color,label in [(False,'#2463a5','Pricing proxy available (36)'),(True,'#c75d14','Pricing proxy missing (7)')]:
        g=data[data.pricing_proxy_missing.eq(missing_flag)]
        ax.scatter(100*g.residualized_revision,g.residualized_outcome,s=42,c=color,label=label,edgecolors='white',linewidths=.5)
    x=np.linspace(data.residualized_revision.min(),data.residualized_revision.max(),100)
    ax.plot(100*x,fit(d,'log_close').params['revision']*x,color='#444444',linewidth=1,label='Full-sample slope')
    for code in prominent:
        row=data[data.code.eq(code)].iloc[0]
        ax.annotate(code,(100*row.residualized_revision,row.residualized_outcome),xytext=(5,6),textcoords='offset points',fontsize=9)
    ax.axhline(0,color='#cccccc',linewidth=.7);ax.axvline(0,color='#cccccc',linewidth=.7)
    ax.set_xlabel('Revision after quarter adjustment (percentage points)')
    ax.set_ylabel('Log offer-to-close return after quarter adjustment')
    ax.set_title('Topic 1: missing-date sample restriction and price outcomes',fontsize=11)
    ax.legend(fontsize=8);ax.spines[['top','right']].set_visible(False)
    fig.savefig(OUT/'step03_partial_relationship.png',dpi=180)
    fig.savefig(OUT/'step03_partial_relationship.svg')
    plt.close(fig)
    manifest={'prepared_on':'2026-10-04','topic':1,'step':3,'n':43,'missing_proxy_codes':missing,
              'deterministic_subsets':128,'outcomes':OUTCOMES,
              'specification':'Intercept, revision, Q2 and Q3; same specification within each diagnostic sample.',
              'scope':'Exact influence and deletion accounting, not causal effects or a strategy; no deletion replaces full-sample result.',
              'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [input_path,Path(__file__),*source_paths]}}
    (OUT/'step03_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(pd.DataFrame(summary).to_string(index=False))
    print('\nExact deletion contributions:');print(effects.sort_values('log_close',ascending=False).to_string())
    print('\nAvailability groups:');print(groups.to_string());print(quarters.to_string())


if __name__=='__main__':
    main()
