import pymupdf
from pathlib import Path

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1989_HK")

# 1. Allotment
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== 1989 ALLOTMENT ===")
for pno in range(min(5, len(doc_allot))):
    txt = doc_allot[pno].get_text()
    if any(k in txt.lower() for k in ["valid application", "times", "clawback", "reallocat", "cornerstone"]):
        print(f"Allot P{pno+1}:")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["offer price", "valid application", "times", "clawback", "reallocat", "cornerstone", "pool a", "pool b"]):
                print("  ", line)
doc_allot.close()

# 2. Prospectus cover and TOC
doc_pros = pymupdf.open(p_dir / "prospectus_full.pdf")
print("=== 1989 PROSPECTUS COVER ===")
print(doc_pros[1].get_text()[:1500])

for pno in range(len(doc_pros)):
    txt = doc_pros[pno].get_text()
    if "underwriting commission" in txt.lower():
        print(f"UW P{pno+1}:")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["commission", "%", "expenses", "hk$"]):
                print("  ", line)
        break

doc_pros.close()
