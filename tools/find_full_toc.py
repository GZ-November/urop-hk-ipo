from pathlib import Path
import pymupdf

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
RAW_DOCS = ROOT / "analysis" / "out" / "pilot_48_raw_docs"

full_issuers = ["2_1246_HK", "2_1989_HK", "2_2289_HK", "2_8267_HK", "2_8348_HK"]

for code in full_issuers:
    p = RAW_DOCS / code / "prospectus_full.pdf"
    doc = pymupdf.open(p)
    print(f"\n{'='*70}\n{code}: {p.name} ({len(doc)} pages)\n{'='*70}")
    # scan first 25 pages for CONTENTS or TABLE OF CONTENTS
    toc_found = False
    for pno in range(min(25, len(doc))):
        txt = doc[pno].get_text()
        if "contents" in txt.lower() or "table of contents" in txt.lower():
            print(f"--- TOC found on Page {pno+1} ---")
            print(txt)
            toc_found = True
            break
    if not toc_found:
        print("TOC not found in first 25 pages")
    doc.close()
