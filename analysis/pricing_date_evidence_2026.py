"""Topic 1, step 1: source candidates only; never certifies actual dates automatically.

Manual expected-date checks: 0100 prospectus p2 and 0664 prospectus p2.
Original source records and the current report are not changed.
"""
from pathlib import Path
import pandas as pd,json,re,hashlib,subprocess
root=Path(__file__).resolve().parents[1];out=root/'analysis/out/pricing_adjustment/steps'
out.mkdir(parents=True,exist_ok=True)
f=pd.read_csv(root/'analysis/out/pricing_adjustment/issuer_sample.csv');f=f[f.price_status.eq('two_sided_range')].copy()
index=json.loads((root/'pipeline/prospectus_pipeline/out/allot/downloaded.json').read_text());index={r['code']:r for r in index}
rows=[]
for _,r in f.iterrows():
 code=r.code.split('.')[0];path=root/f'pipeline/prospectus_pipeline/data/allot/text/HKIPO-MB{code}.jsonl'
 pages=[json.loads(s) for s in path.read_text().splitlines()]
 hits=[]
 for page in pages:
  text=re.sub(r'\s+',' ',page['text'])
  for h in re.finditer(r'price determination|pricing agreement|offer price (?:was|has been) determined|定價日|定價協議',text,re.I):
   hits.append({'page':page['page'],'quote':text[max(0,h.start()-100):h.end()+260]})
 pdf=root/f'pipeline/prospectus_pipeline/data/pdf/HKIPO-MB{code}.pdf'
 snippets=[]
 if pdf.exists():
  p=subprocess.run(['pdftotext','-f','1','-l','15','-layout',str(pdf),'-'],capture_output=True,text=True,check=True)
  for pg,text in enumerate(p.stdout.split('\f'),start=1):
   text=re.sub(r'\s+',' ',text)
   for h in list(re.finditer(r'price determination|定價日',text,re.I))[:2]:
    snippets.append({'pdf_page':pg,'quote':text[max(0,h.start()-80):h.end()+300]})
 pub=index.get(r.code,{})
 rows.append({'code':r.code,'revision':r.revision,'pricing_group':r.pricing_group,
 'recorded_pricing_proxy':r['Pricing date'],'actual_pricing_date':None,'actual_date_status':'not_verified',
 'allotment_publication_hkt':pub.get('datetime'),'final_price_announcement_url':pub.get('pdf_url'),
 'date_candidate_count':len(hits),'allotment_date_candidates':json.dumps(hits,ensure_ascii=False),
 'prospectus_first15_pages_candidates':json.dumps(snippets,ensure_ascii=False),
 'allotment_source':str(path.relative_to(root)),'allotment_text_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'prospectus_available_locally':pdf.exists(),
 'prospectus_first_pages_checked':15 if pdf.exists() else 0,
 'prospectus_pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None,
 'proxy_semantic_review':'confirmed_expected_in_prospectus' if r.code in ['0100.HK','0664.HK'] else 'not_reviewed',
 'scope':'Candidate search only; no-hit does not establish absence of an actual date; publication is not determination.'})
a=pd.DataFrame(rows);a.to_csv(out/'step01_pricing_date_evidence.csv',index=False)
f['revision_direction']=f.revision.gt(0).map({True:'Above midpoint',False:'Below midpoint'})
g=f.groupby('revision_direction').agg(n=('code','size'),mean_revision=('revision','mean'),mean_close=('close','mean'),mean_open=('opening','mean'),median_close=('close','median'))
g.to_csv(out/'step01_revision_groups.csv')
print(g.to_string());print('Candidate count:',a.date_candidate_count.sum());print('Allotment publication coverage:',a.allotment_publication_hkt.notna().sum())
for code in ['0068.HK','0100.HK','0664.HK']:
 row=a[a.code==code].iloc[0];print(code,row.prospectus_first15_pages_candidates[:1000])
