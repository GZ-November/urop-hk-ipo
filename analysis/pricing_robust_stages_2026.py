"""Topic 1, step 4: fixed-sample OLS, median and Huber price-stage checks.

Robust estimators are sensitivity checks, not selected replacement main results.
No imputation, random resampling, source writeback or final report generation.
"""
from pathlib import Path
import hashlib
import json
import warnings
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import linprog
import statsmodels
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/out/pricing_adjustment/steps'
DESIGNS={
    'revision_only':['revision'],
    'quarter_controls':['revision','q2','q3'],
    'launch_size_and_ah':['revision','log_planned_proceeds','ah_true'],
    'subscription_market_and_size':['revision','log_subscription_market','log_planned_proceeds'],
}
OUTCOMES=['log_close','log_opening','log_intraday','log_mair_subscription']


def median_lp_objective(y,x):
    """Independent exact linear-programming check of median absolute loss."""
    n,p=x.shape
    cost=np.r_[np.zeros(p),np.full(2*n,.5)]
    result=linprog(cost,A_eq=np.c_[x,np.eye(n),-np.eye(n)],b_eq=y,
                   bounds=[(None,None)]*p+[(0,None)]*(2*n),method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.fun)


def main():
    path=ROOT/'analysis/out/pricing_adjustment/issuer_sample.csv'
    d=pd.read_csv(path);d=d[d.price_status.eq('two_sided_range')].copy()
    assert len(d)==43 and d.code.nunique()==43
    assert d[OUTCOMES+list(set(sum(DESIGNS.values(),[])))].notna().all().all()
    estimates=[];coefficients=[];weights=[];checks=[]
    for design,columns in DESIGNS.items():
        x=sm.add_constant(d[columns],has_constant='add')
        assert np.linalg.matrix_rank(x)==x.shape[1]
        for outcome in OUTCOMES:
            y=d[outcome]
            for estimator in ['OLS_HC3','Median','Huber']:
                with warnings.catch_warnings(record=True) as captured:
                    warnings.simplefilter('always')
                    if estimator=='OLS_HC3':
                        model=sm.OLS(y,x).fit(cov_type='HC3',use_t=True)
                        se_method='HC3 t reference';iterations=0
                    elif estimator=='Median':
                        model=sm.QuantReg(y,x).fit(q=.5,vcov='robust',kernel='epa',bandwidth='hsheather',
                                                 max_iter=10000,p_tol=1e-9)
                        se_method='QuantReg robust asymptotic sparsity estimate; not cluster robust'
                        iterations=model.iterations
                        optimal=median_lp_objective(y.to_numpy(),x.to_numpy())
                        loss=.5*np.abs(model.resid).sum()
                        checks.append({'design':design,'outcome':outcome,'median_loss':loss,
                                       'independent_lp_loss':optimal,'loss_gap':loss-optimal})
                        if not np.isclose(loss,optimal,rtol=1e-6,atol=1e-6):
                            raise ValueError('Median fit fails independent objective check')
                    else:
                        model=sm.RLM(y,x,M=sm.robust.norms.HuberT(t=1.345)).fit(scale_est='mad',cov='H1',
                                                                                            maxiter=200,tol=1e-9)
                        se_method='RLM H1 asymptotic covariance; not HC3 or cluster robust'
                        iterations=model.fit_history['iteration']
                        if iterations>=200:
                            raise ValueError('Huber fit did not finish within iteration limit')
                        for code,weight,resid in zip(d.code,model.weights,model.resid):
                            weights.append({'code':code,'design':design,'outcome':outcome,
                                            'huber_weight':weight,'huber_residual':resid})
                messages='; '.join(str(w.message) for w in captured)
                if 'IterationLimit' in messages or 'Convergence cycle' in messages:
                    raise ValueError(messages)
                estimates.append({'design':design,'outcome':outcome,'estimator':estimator,'n':len(d),
                                  'revision_coefficient':model.params['revision'],
                                  'se':model.bse['revision'],'se_method':se_method,
                                  'ols_hc3_t_p':model.pvalues['revision'] if estimator=='OLS_HC3' else np.nan,
                                  'iterations':iterations,'warning':messages,
                                  'interpretation':'Exploratory sensitivity; median and Huber target different functionals from conditional mean.'})
                for term in x.columns:
                    coefficients.append({'design':design,'outcome':outcome,'estimator':estimator,
                                         'term':term,'coefficient':model.params[term]})
    e=pd.DataFrame(estimates)
    # Only linear OLS stage coefficients have exact additive identities.
    ols=e[e.estimator.eq('OLS_HC3')].pivot(index='design',columns='outcome',values='revision_coefficient')
    assert np.allclose(ols.log_close,ols.log_opening+ols.log_intraday)
    previous=pd.read_csv(ROOT/'analysis/out/pricing_adjustment/range_regressions.csv')
    comparison=e[e.estimator.eq('OLS_HC3')].merge(previous,left_on=['design','outcome'],right_on=['model','outcome'],validate='one_to_one')
    assert np.allclose(comparison.revision_coefficient,comparison.coefficient)
    for name,frame in [('estimates',e),('coefficients',pd.DataFrame(coefficients)),
                       ('huber_weights',pd.DataFrame(weights)),('median_objective_checks',pd.DataFrame(checks))]:
        frame.to_csv(OUT/('step04_'+name+'.csv'),index=False)
    missing=d['Pricing date'].isna()
    availability=d[['code']].assign(pricing_proxy_missing=missing)
    ws=pd.DataFrame(weights).merge(availability,on='code',validate='many_to_one')
    ws.groupby(['design','outcome','pricing_proxy_missing']).agg(n=('code','size'),mean_weight=('huber_weight','mean'),
             min_weight=('huber_weight','min'),downweighted=('huber_weight',lambda w:int((w<.999999).sum()))).reset_index().to_csv(OUT/'step04_weight_groups.csv',index=False)
    manifest={'prepared_on':'2026-10-04','topic':1,'step':4,'n':43,'designs':DESIGNS,'outcomes':OUTCOMES,
              'estimators':['OLS HC3 with t reference','Median q=0.5','Huber t=1.345, MAD scale, H1 covariance'],
              'models':len(e),'scope':'Post-exploration sensitivity checks. Different estimands; no new robust/cluster significance claim.',
              'validation':'Independent median LP objectives; OLS matches prior estimates; OLS stage identities; all fits retain 43 firms.',
              'versions':{'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'statsmodels':statsmodels.__version__},
              'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [path,Path(__file__),ROOT/'analysis/out/pricing_adjustment/range_regressions.csv']}}
    (OUT/'step04_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(e[e.design.eq('quarter_controls')][['outcome','estimator','revision_coefficient','se','ols_hc3_t_p','iterations']].to_string(index=False))
    print('\nAll declared designs:')
    print(e.pivot(index=['design','outcome'],columns='estimator',values='revision_coefficient').to_string())


if __name__=='__main__':
    main()
