from pathlib import Path
import pymupdf

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
RAW_DOCS = ROOT / "analysis" / "out" / "pilot_48_raw_docs"
full_issuers = ["2_1246_HK", "2_1989_HK", "2_2289_HK", "2_8267_HK", "2_8348_HK"]

for code in full_issuers:
    p = RAW_DOCS / code / "prospectus_full.pdf"
    doc = pymupdf.open(p)
    print(f"\n{'='*70}\n{code}: TOC SEARCH\n{'='*70}")
    for pno in range(2, min(10, len(doc))):
        txt = doc[pno].get_text()
        if "summary" in txt.lower() and "corporate information" in txt.lower():
            print(f"--- Page {pno+1} ---")
            print(txt[:1500])
    doc.close()
