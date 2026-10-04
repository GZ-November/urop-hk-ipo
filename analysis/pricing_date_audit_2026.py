"""Topic 1 step 2: audit date provenance and compare explicitly labelled anchors.

No actual pricing date is inferred from an expected date or publication time.
Source searches generate candidates for review, never pipeline approvals.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/out/pricing_adjustment/steps'
PATTERN=re.compile(r'price determination|pricing agreement|price (?:was|has been) (?:determined|fixed|agreed)|定價|定价|釐定',re.I)


def candidates(pages, code, kind, source):
    hits=[]
    for number,text in pages:
        clean=re.sub(r'\s+',' ',text)
        for hit in PATTERN.finditer(clean):
            quote=clean[max(0,hit.start()-100):hit.end()+300]
            hits.append({'code':code,'document_kind':kind,'source':str(source.relative_to(ROOT)),
                         'pdf_page':number,'candidate_quote':quote,'status':'unreviewed_candidate'})
    return hits


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    f=pd.read_csv(ROOT/'analysis/out/pricing_adjustment/issuer_sample.csv')
    f=f[f.price_status.eq('two_sided_range')].copy()
    indexes=json.loads((ROOT/'pipeline/prospectus_pipeline/out/allot/downloaded.json').read_text())
    indexes={r['code']:r for r in indexes}
    ledger=[];hits=[];inputs={}
    for _,r in f.iterrows():
        code=r.code.split('.')[0]
        packet=ROOT/f'pipeline/prospectus_pipeline/data/allot/packets/HKIPO-MB{code}.md'
        text=packet.read_text()
        timestamp=re.search(r'\*\*(\d{2}/\d{2}/\d{4} \d{2}:\d{2})\*\*',text)
        url=re.search(r'https://[^\s]+\.pdf',text)
        assert timestamp and url,r.code
        ts=pd.to_datetime(timestamp[1],format='%d/%m/%Y %H:%M')
        source=ROOT/f'pipeline/prospectus_pipeline/data/allot/text/HKIPO-MB{code}.jsonl'
        pages=[json.loads(line) for line in source.read_text().splitlines()]
        hits+=candidates([(p['page'],p['text']) for p in pages],r.code,'allotment',source)
        prospectus=ROOT/f'pipeline/prospectus_pipeline/data/pdf/HKIPO-MB{code}.pdf'
        full_prospectus=False
        replacement_chars=0
        if prospectus.exists():
            result=subprocess.run(['pdftotext','-layout',str(prospectus),'-'],capture_output=True,text=True,encoding='utf-8',errors='replace',check=True)
            replacement_chars=result.stdout.count('\ufffd')
            hits+=candidates(list(enumerate(result.stdout.split('\f'),1)),r.code,'prospectus',prospectus)
            full_prospectus=True
            inputs[str(prospectus.relative_to(ROOT))]=hashlib.sha256(prospectus.read_bytes()).hexdigest()
        greenshoe=ROOT/f'pipeline/prospectus_pipeline/data/allot/greenshoe/text/HKIPO-MB{code}.jsonl'
        if greenshoe.exists():
            pages=[json.loads(line) for line in greenshoe.read_text().splitlines()]
            hits+=candidates([(p['page'],p['text']) for p in pages],r.code,'greenshoe',greenshoe)
            inputs[str(greenshoe.relative_to(ROOT))]=hashlib.sha256(greenshoe.read_bytes()).hexdigest()
        for path in [packet,source]:inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        old=indexes.get(r.code,{}).get('datetime')
        if old:assert old==timestamp[1],r.code
        ledger.append({'code':r.code,'recorded_pricing_proxy':r['Pricing date'],
                       'actual_pricing_date':None,'actual_date_status':'not_verified',
                       'final_price_publication_hkt':ts.isoformat(),
                       'publication_metadata_source':str(packet.relative_to(ROOT)),
                       'announcement_url':url[0], 'recovered_from_older_packet':not bool(old),
                       'full_local_prospectus_searched':full_prospectus,
                       'prospectus_text_replacement_characters':replacement_chars,
                       'publication_day_upper_bound_only':ts.date().isoformat(),
                       'upper_bound_basis':'Announcement reports final price; release date is not agreement date.'})
    dates=pd.DataFrame(ledger)
    dates.to_csv(OUT/'step02_date_provenance.csv',index=False)
    pd.DataFrame(hits).to_csv(OUT/'step02_date_candidates.csv',index=False)
    bars=pd.DataFrame(json.loads((ROOT/'pipeline/prospectus_pipeline/data/market/first_day_returns/hsi_bars.json').read_text()))
    bars.date=pd.to_datetime(bars.date);bars=bars.sort_values('date').set_index('date')
    def level(date):
        available=bars.loc[bars.index<=pd.Timestamp(date)]
        assert len(available)>0
        return available.iloc[-1]['close'],available.index[-1].date().isoformat()
    f=f.merge(dates[['code','final_price_publication_hkt']],on='code',validate='one_to_one')
    rows=[]
    for _,r in f.iterrows():
        end,end_day=level(r.listing_date)
        anchors={'subscription_close':r.subscription_close_date,
                 'recorded_expected_pricing_proxy':r['Pricing date'],
                 'final_price_publication_day':str(r.final_price_publication_hkt)[:10]}
        for kind,date in anchors.items():
            if pd.isna(date):continue
            start,start_day=level(date)
            market=end/start-1
            rows.append({'code':r.code,'anchor_kind':kind,'anchor_date':str(date)[:10],
                         'index_start_trading_date':start_day,'index_end_trading_date':end_day,
                         'index_start':start,'index_end':end,'market_return':market,
                         'raw_close_return':r.close,'adjusted_close_return':(1+r.close)/(1+market)-1,
                         'adjusted_log_close':np.log1p(r.close)-np.log1p(market)})
    panel=pd.DataFrame(rows)
    common=set(f.loc[f['Pricing date'].notna(),'code'])
    assert len(common)==36
    assert all(set(panel.loc[panel.anchor_kind.eq(k),'code'])>=common for k in panel.anchor_kind.unique())
    summary=[]
    for label, codes in [('All range offers',set(f.code)),('Common proxy-available sample',common)]:
        raw=f[f.code.isin(codes)].copy()
        x=sm.add_constant(raw[['revision','q2','q3']],has_constant='add')
        fit=sm.OLS(np.log1p(raw.close),x).fit(cov_type='HC3',use_t=True)
        summary.append({'sample':label,'anchor_kind':'unadjusted_close','n':len(raw),
                        'mean_raw_close':raw.close.mean(),'mean_adjusted_close':raw.close.mean(),
                        'revision_log_return_coefficient':fit.params['revision'],
                        'revision_hc3_se':fit.bse['revision'],'revision_hc3_p':fit.pvalues['revision']})
        subset=panel[panel.code.isin(codes)].merge(f[['code','revision','q2','q3']],on='code',validate='many_to_one')
        for kind,g in subset.groupby('anchor_kind'):
            if len(g)!=len(codes):continue
            x=sm.add_constant(g[['revision','q2','q3']],has_constant='add')
            fit=sm.OLS(g.adjusted_log_close,x).fit(cov_type='HC3',use_t=True)
            summary.append({'sample':label,'anchor_kind':kind,'n':len(g),'mean_raw_close':g.raw_close_return.mean(),
                            'mean_adjusted_close':g.adjusted_close_return.mean(),
                            'revision_log_return_coefficient':fit.params['revision'],
                            'revision_hc3_se':fit.bse['revision'],'revision_hc3_p':fit.pvalues['revision']})
    f[~f.code.isin(common)][['code','revision','close','opening','listing_date']].to_csv(OUT/'step02_missing_proxy_issuers.csv',index=False)
    panel.to_csv(OUT/'step02_market_anchor_panel.csv',index=False)
    pd.DataFrame(summary).to_csv(OUT/'step02_matched_anchor_comparison.csv',index=False)
    for path in [Path(__file__),ROOT/'analysis/out/pricing_adjustment/issuer_sample.csv',ROOT/'pipeline/prospectus_pipeline/data/market/first_day_returns/hsi_bars.json']:
        inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    manifest={'prepared_on':'2026-10-04','topic':1,'step':2,'n_range':43,'announcement_metadata':43,
              'recovered_packet_metadata':int(dates.recovered_from_older_packet.sum()),
              'full_local_prospectuses':int(dates.full_local_prospectus_searched.sum()),
              'newly_verified_actual_dates':0,'matched_anchor_n':36,
              'scope':'Exploratory anchor sensitivity, not an actual-pricing-window test. Candidate snippets need semantic review.',
              'source_sha256':inputs}
    (OUT/'step02_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(pd.DataFrame(summary).to_string(index=False))
    print('Candidate rows:',len(hits),'Recovered metadata:',manifest['recovered_packet_metadata'])


if __name__=='__main__':
    main()
