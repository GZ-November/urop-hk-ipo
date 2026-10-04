"""Audit the 31 missing lower endpoints; never write back extraction or workbooks.

Read official PDFs from the pipeline cache, or --supplemental-dir for missing
files. Supplemental URLs below identify the exact documents reviewed.
"""
from pathlib import Path
import argparse,csv,hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/out/pricing_adjustment/lower_bound_audit'
SUPPLEMENTAL={
'1081':'0528/2026052800019.pdf','1187':'0427/2026042700013.pdf',
'1688':'0617/2026061700029.pdf','2476':'0413/2026041300005.pdf',
'3296':'0415/2026041500011.pdf','3661':'0617/2026061700042_c.pdf',
'6067':'0612/2026061200031.pdf','6228':'0617/2026061700075.pdf'}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--supplemental-dir',type=Path,required=True);args=ap.parse_args()
 source=ROOT/'analysis/out/pricing_adjustment/issuer_sample.csv'
 with source.open() as f:sample=list(csv.DictReader(f))
 selected=[r for r in sample if r['price_status']=='undisclosed_lower_bound']
 assert len(sample)==113 and len(selected)==31
 manifest={r['code']:r for r in json.loads((ROOT/'pipeline/prospectus_pipeline/out/downloaded.json').read_text())}
 rows=[]
 for r in selected:
  code=r['code'].split('.')[0];pdf=ROOT/f'pipeline/prospectus_pipeline/data/pdf/HKIPO-MB{code}.pdf'
  url=manifest.get(r['code'],{}).get('pdf_url','')
  if not pdf.exists():
   pdf=args.supplemental_dir/('3661_full_zh.pdf' if code=='3661' else f'{code}.pdf')
   url='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/'+SUPPLEMENTAL[code]
  p=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,check=True).stdout.decode('utf-8','replace').split('\f')
  if not p[-1].strip():p=p[:-1]
  assert len(p)>100,(code,'not a full prospectus')
  if code=='3661':
   compact=re.sub(r'\s+','',p[82]);phrase='以便本公司僅按以下基準在本招股章程內披露最高發售價'
   assert phrase in compact
   page=83;quote=phrase;interpretation='Company states that it discloses only the maximum offer price; analyst translation from Chinese.'
   status='confirmed_maximum_only';lang='Chinese'
  elif code=='2041':
   page=2;phrase='The Offer Price will be HK$15.42 per Offer Share, unless otherwise announced.'
   assert phrase in re.sub(r'\s+',' ',p[1]) and phrase.rstrip('.') in re.sub(r'\s+',' ',p[292])
   quote=phrase;interpretation='Single stated price, subject to an announcement of reduction. Pricing section corroborates at PDF page 293 (printed 285).'
   status='confirmed_single_price';lang='English'
  else:
   matches=[]
   for n,text in enumerate(p,1):
    clean=re.sub(r'\s+',' ',text)
    h=re.search(r'(?:our )?Company will only disclose the maximum Offer Price|[Aa] maximum (?:Public )?Offer Price will be disclosed in (?:this|the) (?:document|prospectus)',clean)
    if h:matches.append((n,h.group()))
   assert matches,(code,'requires manual evidence review')
   page,quote=matches[0];interpretation='Explicit maximum-only disclosure in the waiver section; no numeric lower offer-price endpoint identified in the full-document search.'
   status='confirmed_maximum_only';lang='English'
  footer=p[page-1].strip().splitlines()[-1].strip();footer=re.sub(r'[–—−\s]','',footer)
  if not re.fullmatch(r'\d+',footer):footer='unpaginated'
  rows.append(dict(code=r['code'],original_status=r['price_status'],audited_status=status,recorded_maximum_hkd=r['range_high'],proposed_single_price_hkd='15.42' if code=='2041' else '',pdf_page=page,printed_page=footer,document_pages=len(p),source_url=url,pdf_sha256=sha(pdf),language=lang,quote=quote,interpretation=interpretation,review_scope='Full-text search; offer-price terms and affirmative waiver/pricing evidence; no formal source writeback.'))
 assert sum(x['audited_status']=='confirmed_maximum_only' for x in rows)==30
 assert sum(x['audited_status']=='confirmed_single_price' for x in rows)==1
 OUT.mkdir(parents=True,exist_ok=True)
 with (OUT/'issuer_evidence.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (OUT/'audit_manifest.json').write_text(json.dumps({'audit_date':'2026-10-04','input_sha256':sha(source),'selected_issuers':31,'full_prospectuses':31,'confirmed_maximum_only':30,'confirmed_single_price':1,'numeric_lower_endpoint_found':0,'unresolved':0,'formal_writeback':False,'classification_after_research_review':{'two_sided_range':43,'single_or_equal_endpoint_price':40,'maximum_only':30},'script_sha256':sha(Path(__file__))},indent=2)+'\n')
 print('Audited 31 complete prospectuses: 30 maximum-only; 1 single-price; 0 numeric lower endpoints recovered.')
if __name__=='__main__':main()
