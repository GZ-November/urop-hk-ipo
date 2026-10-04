"""Complete Topic 1 on a frozen sample, with audited disclosure classifications.

All resampling is exact sign enumeration, not investment simulation. No formal
source-field writes. See specifications/pricing_topic1_completion.md.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from scipy.optimize import linprog
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from shared.inference import wild_cluster_p

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis/out/pricing_adjustment'
OUT=BASE/'topic1'
STAGES=['log_close','log_opening','log_intraday','log_mair_subscription']
DESIGNS={'revision_only':['revision'],'quarter_controls':['revision','q2','q3'],
         'launch_size_and_ah':['revision','log_planned_proceeds','ah_true'],
         'subscription_market_and_size':['revision','log_subscription_market','log_planned_proceeds']}

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def xmatrix(d,terms):
 x=sm.add_constant(d[terms],has_constant='add').to_numpy(float)
 if np.linalg.matrix_rank(x)!=x.shape[1]:raise ValueError('Rank deficient design')
 return x

def cv3(y,x,g):
 """CV3 about full-sample coefficients; confirm with block-residual sandwich."""
 b=np.linalg.lstsq(x,y,rcond=None)[0];u=y-x@b;ids=np.unique(g);bread=np.linalg.inv(x.T@x)
 deletions=[];meat=np.zeros((x.shape[1],x.shape[1]))
 for c in ids:
  mask=g==c;xc=x[mask];remaining=x[~mask]
  if np.linalg.matrix_rank(remaining)!=x.shape[1]:raise ValueError('Singular deleted cluster')
  bc=np.linalg.lstsq(remaining,y[~mask],rcond=None)[0];deletions.append(bc)
  adjusted=np.linalg.solve(np.eye(mask.sum())-xc@bread@xc.T,u[mask]);score=xc.T@adjusted
  meat+=np.outer(score,score)
 diff=np.array(deletions)-b;scale=(len(ids)-1)/len(ids)
 v=scale*diff.T@diff;direct=scale*bread@meat@bread
 assert np.allclose(v,direct,rtol=1e-8,atol=1e-10)
 return b,v,np.array(deletions),float(np.max(np.abs(v-direct)))

def fit_row(d,outcome,terms,focus,label):
 x=xmatrix(d,terms);y=d[outcome].to_numpy();g=d.month.to_numpy();j=1+terms.index(focus)
 model=sm.OLS(y,x).fit(cov_type='HC3',use_t=True);b,v,deleted,gap=cv3(y,x,g);se=np.sqrt(v[j,j]);df=len(np.unique(g))-1
 return dict(model=label,outcome=outcome,term=focus,n=len(d),clusters=df+1,k=x.shape[1],coefficient=b[j],hc3_se=model.bse[j],hc3_p=model.pvalues[j],cv3_se=se,cv3_t_p=2*stats.t.sf(abs(b[j]/se),df),cv3_ci_low=b[j]-stats.t.ppf(.975,df)*se,cv3_ci_high=b[j]+stats.t.ppf(.975,df)*se,wcr_p=wild_cluster_p(y,x,g,j),adjusted_r2=model.rsquared_adj,cv3_block_check_gap=gap)

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 source=BASE/'issuer_sample.csv';evidence=BASE/'lower_bound_audit/issuer_evidence.csv'
 s=pd.read_csv(source);audit=pd.read_csv(evidence)
 assert len(s)==113 and s.code.nunique()==113 and len(audit)==31
 s=s.merge(audit[['code','audited_status']],on='code',how='left',validate='one_to_one')
 s['disclosure_class']=s.audited_status.fillna(s.price_status).replace({'equal_endpoints':'recorded_equal_endpoints','two_sided_range':'two_sided_range'})
 assert s.disclosure_class.value_counts().to_dict()=={'two_sided_range':43,'recorded_equal_endpoints':39,'confirmed_maximum_only':30,'confirmed_single_price':1}
 s['ceiling_revision']=s.offer_price/s.range_high-1
 d=s[s.disclosure_class.eq('two_sided_range')].copy().reset_index(drop=True)
 assert len(d)==43 and d[STAGES+list(set(sum(DESIGNS.values(),[])))].notna().all().all()
 assert np.allclose(d.revision,d.range_width*(d.range_position-.5))
 assert np.allclose(d.log_close,d.log_opening+d.log_intraday)
 s.to_csv(OUT/'audited_issuer_panel.csv',index=False)
 groups=[]
 for key,g in s.groupby('disclosure_class'):
  groups.append(dict(group=key,n=len(g),ah_n=int(g.ah_true.sum()),mean_close=g.close.mean(),median_close=g.close.median(),mean_open=g.opening.mean(),median_open=g.opening.median(),mean_intraday=g.intraday.mean(),mean_log_close=g.log_close.mean(),mean_log_open=g.log_opening.mean(),mean_log_intraday=g.log_intraday.mean(),positive_close=(g.close>0).mean(),at_ceiling=int(np.isclose(g.ceiling_revision,0).sum())))
 pd.DataFrame(groups).to_csv(OUT/'disclosure_groups.csv',index=False)
 desc=[]
 for col in ['revision','range_position','range_width','close','opening','intraday','mair_subscription','log_planned_proceeds','log_subscription_market']:
  a=d[col];desc.append(dict(variable=col,n=len(a),mean=a.mean(),sd=a.std(),p25=a.quantile(.25),median=a.median(),p75=a.quantile(.75),minimum=a.min(),maximum=a.max()))
 pd.DataFrame(desc).to_csv(OUT/'range_descriptives.csv',index=False)
 main_results=[];loo=[];cluster_rows=[]
 for design,terms in DESIGNS.items():
  x=xmatrix(d,terms);g=d.month.to_numpy();ids=np.unique(g)
  controls=np.delete(x,1,axis=1);vr=x[:,1]-controls@np.linalg.lstsq(controls,x[:,1],rcond=None)[0]
  for c in ids:
   mask=g==c;cluster_rows.append(dict(model=design,month=c,n=int(mask.sum()),information_share=(vr[mask]**2).sum()/(vr**2).sum(),sum_leverage=np.trace(x[mask]@np.linalg.inv(x.T@x)@x[mask].T)))
  for outcome in STAGES:
   main_results.append(fit_row(d,outcome,terms,'revision',design))
   b,v,deleted,_=cv3(d[outcome].to_numpy(),x,g)
   for i,c in enumerate(ids):loo.append(dict(model=design,outcome=outcome,deleted_month=c,retained_n=int((g!=c).sum()),coefficient=deleted[i,1],change=deleted[i,1]-b[1]))
 main=pd.DataFrame(main_results)
 # Retain the historical seven-outcome family, rather than quietly replacing it.
 historical=pd.read_csv(BASE/'range_regressions.csv');primary=historical[historical.model.eq('quarter_controls')]
 assert len(primary)==7
 # Primary family labels are assigned from the exact prior p-value family below.
 family=next(c for c in primary.columns if 'holm' in c.lower() and 'wild' in c.lower())
 main['historical_seven_outcome_holm_wcr_p']=main.outcome.map(primary.set_index('outcome')[family])
 primary_family=pd.DataFrame([fit_row(d,o,['revision','q2','q3'],'revision','quarter_controls') for o in primary.outcome])
 primary_family['holm_cv3_7_tests']=multipletests(primary_family.cv3_t_p,method='holm')[1]
 primary_family['holm_wcr_7_tests']=multipletests(primary_family.wcr_p,method='holm')[1]
 assert np.allclose(primary_family.set_index('outcome').holm_wcr_7_tests.reindex(primary.outcome),primary[family])
 primary_family.to_csv(OUT/'primary_family_inference.csv',index=False)
 main['historical_seven_outcome_holm_cv3_p']=main.outcome.map(primary_family.set_index('outcome').holm_cv3_7_tests)
 for _,r in main[main.model.eq('quarter_controls')].iterrows():assert np.isclose(r.coefficient,primary.set_index('outcome').loc[r.outcome,'coefficient'])
 main.to_csv(OUT/'stage_inference.csv',index=False);pd.DataFrame(loo).to_csv(OUT/'leave_one_month_out.csv',index=False);pd.DataFrame(cluster_rows).to_csv(OUT/'cluster_information.csv',index=False)
 # Conditional on width, price position and fractional revision are different designs.
 d['centered_position']=d.range_position-.5
 geometry=[]
 for outcome in STAGES:
  for label,terms,focus in [('revision_and_width',['revision','range_width','q2','q3'],'revision'),('position_and_width',['centered_position','range_width','q2','q3'],'centered_position')]:
   geometry.append(fit_row(d,outcome,terms,focus,label))
 geometry=pd.DataFrame(geometry);geometry['holm_wcr_8_tests']=multipletests(geometry.wcr_p,method='holm')[1];geometry.to_csv(OUT/'range_geometry.csv',index=False)
 # Exploratory continuous hinge. Difference is reparameterized for null-imposed WCR.
 d['revision_positive']=d.revision.clip(lower=0);d['revision_negative']=d.revision.clip(upper=0)
 asym=[]
 for outcome in STAGES:
  terms=['revision_positive','revision_negative','q2','q3']
  for focus in terms[:2]:asym.append(fit_row(d,outcome,terms,focus,'asymmetric_revision'))
  asym.append(fit_row(d,outcome,['revision','revision_positive','q2','q3'],'revision_positive','positive_minus_negative_slope'))
 asym=pd.DataFrame(asym);asym['holm_wcr_12_tests']=multipletests(asym.wcr_p,method='holm')[1];asym.to_csv(OUT/'asymmetry.csv',index=False)
 public=[fit_row(d,'revision',['log_subscription_market','q2','q3'],'log_subscription_market','market_window_and_revision')]
 for outcome in STAGES:public.append(fit_row(d,outcome,['revision','log_subscription_market','q2','q3'],'log_subscription_market','market_window_and_return'))
 pd.DataFrame(public).to_csv(OUT/'public_market_associations.csv',index=False)
 # Overlap is reported, rather than asserting disclosure format is an intervention.
 ah=[]
 for (route,key),g in s.groupby(['ah_true','disclosure_class']):
  ah.append(dict(ah=int(route),group=key,n=len(g),mean_close=g.close.mean(),median_close=g.close.median(),mean_open=g.opening.mean(),mean_intraday=g.intraday.mean()))
 pd.DataFrame(ah).to_csv(OUT/'route_disclosure_overlap.csv',index=False)
 cap=s[s.disclosure_class.eq('confirmed_maximum_only')].copy();cap['at_ceiling']=np.isclose(cap.ceiling_revision,0)
 cap.to_csv(OUT/'maximum_only_panel.csv',index=False)
 cg=[]
 for key,g in cap.groupby('at_ceiling'):cg.append(dict(at_ceiling=bool(key),n=len(g),mean_ceiling_revision=g.ceiling_revision.mean(),mean_close=g.close.mean(),median_close=g.close.median(),mean_open=g.opening.mean(),median_open=g.opening.median(),mean_intraday=g.intraday.mean(),ah_n=int(g.ah_true.sum())))
 pd.DataFrame(cg).to_csv(OUT/'ceiling_groups.csv',index=False)
 # Sharp point-slope sensitivity bounds on a fixed design; not confidence intervals.
 dates=pd.read_csv(BASE/'steps/step02_date_provenance.csv');d=d.merge(dates[['code','final_price_publication_hkt']],on='code',validate='one_to_one')
 hsi_path=ROOT/'pipeline/prospectus_pipeline/data/market/first_day_returns/hsi_bars.json'
 hsi=pd.DataFrame(json.loads(hsi_path.read_text()));hsi['date']=pd.to_datetime(hsi.date);hsi=hsi.sort_values('date')
 anchors=[];bounds=[];x=xmatrix(d,['revision','q2','q3']);weights=np.linalg.pinv(x)[1]
 for window,startcol in [('subscription_to_publication','subscription_close_date'),('prospectus_to_publication','prospectus_date')]:
  low=[];high=[]
  for i,r in d.iterrows():
   start=pd.Timestamp(r[startcol]);end=pd.Timestamp(r.final_price_publication_hkt).normalize();assert start<=end
   earlier=hsi[hsi.date<=start];assert len(earlier)>0
   candidates=hsi[(hsi.date>=earlier.iloc[-1].date)&(hsi.date<=end)]
   values=r.log_close-np.log(r['First-day HSI listing close'])+np.log(candidates.close.to_numpy())
   assert len(values)>0
   lo=float(values.min());hi=float(values.max());low.append(lo);high.append(hi)
   anchors.append(dict(code=r.code,window=window,start=str(start.date()),end=str(end.date()),candidate_trading_days=len(values),minimum_log_adjusted_return=lo,maximum_log_adjusted_return=hi,minimum_adjusted_return=np.expm1(lo),maximum_adjusted_return=np.expm1(hi),coefficient_weight=weights[i]))
  low=np.array(low);high=np.array(high)
  lower=np.where(weights>=0,weights*low,weights*high).sum();upper=np.where(weights>=0,weights*high,weights*low).sum()
  bl=list(zip(low,high));l=linprog(weights,bounds=bl,method='highs');u=linprog(-weights,bounds=bl,method='highs');assert l.success and u.success
  assert np.isclose(lower,l.fun) and np.isclose(upper,-u.fun)
  bounds.append(dict(window=window,n=43,coefficient_min=lower,coefficient_max=upper,mean_adjusted_return_min=np.expm1(low).mean(),mean_adjusted_return_max=np.expm1(high).mean(),lp_bound_check_error=max(abs(lower-l.fun),abs(upper+u.fun)),interpretation='Sharp conditional point-slope bounds over assumed independent issuer anchor sets; not actual dates, confidence intervals, or significance tests.'))
 pd.DataFrame(anchors).to_csv(OUT/'anchor_sensitivity_panel.csv',index=False);pd.DataFrame(bounds).to_csv(OUT/'anchor_slope_bounds.csv',index=False)
 stages=[]
 for key,g in d.groupby(d.revision.gt(0)):
  stages.append(dict(above_midpoint=bool(key),n=len(g),mean_revision=g.revision.mean(),mean_log_revision=g.log_revision.mean(),mean_log_close=g.log_close.mean(),mean_log_open=g.log_opening.mean(),mean_log_intraday=g.log_intraday.mean(),mean_close=g.close.mean(),median_close=g.close.median(),mean_open=g.opening.mean(),median_open=g.opening.median()))
 pd.DataFrame(stages).to_csv(OUT/'revision_stage_groups.csv',index=False)
 # Same-design OLS accounting and independent checks are substantive validation.
 a=main[main.model.eq('quarter_controls')].set_index('outcome');assert np.isclose(a.loc['log_close','coefficient'],a.loc['log_opening','coefficient']+a.loc['log_intraday','coefficient'])
 ll=pd.DataFrame(loo).query("model=='quarter_controls'").pivot(index='deleted_month',columns='outcome',values='coefficient');assert np.allclose(ll.log_close,ll.log_opening+ll.log_intraday)
 paths=[source,evidence,hsi_path,BASE/'steps/step02_date_provenance.csv',BASE/'range_regressions.csv',Path(__file__),ROOT/'analysis/specifications/pricing_topic1_completion.md']
 manifest={'prepared_on':'2026-10-04','cutoff':'2026-09-30','topic':1,'status':'current_sample_analysis_complete; causal mechanisms and actual dates not identified','n_total':113,'n_primary':43,'clusters':9,'classification_counts':s.disclosure_class.value_counts().to_dict(),'estimation':'HC3; CV3 full-estimate centering with t(G-1); exact restricted Rademacher cluster-t (512 signs)','multiplicity':'Historical seven-outcome Holm family retained; exploratory asymmetry has a separate 12-test Holm family','random_resampling':False,'formal_source_writeback':False,'checks':{'cv3_block_sandwich':True,'fixed_sample':True,'stage_coefficient_addition':True,'range_geometry':True,'linear_programming_anchor_bounds':True,'historical_main_coefficients':True},'versions':{'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'statsmodels':statsmodels.__version__},'input_sha256':{str(p.relative_to(ROOT)):digest(p) for p in paths}}
 (OUT/'run_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(main[main.model.eq('quarter_controls')].to_string(index=False));print(pd.DataFrame(bounds).to_string(index=False));print(pd.DataFrame(cg).to_string(index=False))
if __name__=='__main__':main()
