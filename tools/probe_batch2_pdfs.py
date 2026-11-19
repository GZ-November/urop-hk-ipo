from pathlib import Path
import pymupdf

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
RAW_DOCS = ROOT / "analysis" / "out" / "pilot_48_raw_docs"

issuers = [
    "2_0968_HK", "2_1246_HK", "2_1288_HK", "2_1299_HK", "2_1318_HK", "2_1333_HK",
    "2_1989_HK", "2_2289_HK", "2_2722_HK", "2_8267_HK", "2_8325_HK", "2_8348_HK"
]

print(f"Checking {len(issuers)} issuers in {RAW_DOCS}...")
for code in issuers:
    p = RAW_DOCS / code
    if not p.exists():
        print(f"MISSING: {code}")
        continue
    files = list(p.glob("*.pdf")) + list(p.glob("*.PDF"))
    print(f"=== {code} ({len(files)} pdfs) ===")
    for f in sorted(files, key=lambda x: x.name):
        doc = pymupdf.open(f)
        print(f"  {f.name}: {len(doc)} pages")
        doc.close()
