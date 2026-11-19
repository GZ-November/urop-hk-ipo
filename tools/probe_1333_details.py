import pymupdf
from pathlib import Path

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1333_HK")

# 1. Share capital
doc_cap = pymupdf.open(p_dir / "pros_sec_share_capital_e119.pdf")
print("=== 1333 SHARE CAPITAL ===")
for pno in range(len(doc_cap)):
    print(doc_cap[pno].get_text())
doc_cap.close()

# 2. Summary financial info
doc_sum = pymupdf.open(p_dir / "pros_sec_summary_e105.pdf")
print("=== 1333 SUMMARY FINANCIAL ===")
for pno in range(len(doc_sum)):
    txt = doc_sum[pno].get_text()
    if any(k in txt.lower() for k in ["turnover", "revenue", "profit for the year", "total assets"]):
        print(f"Summary P{pno+1}:")
        print(txt[:1500])
doc_sum.close()

# 3. Allotment under-subscription details
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== 1333 ALLOTMENT DETAILS ===")
for pno in range(len(doc_allot)):
    txt = doc_allot[pno].get_text()
    if "reallocation" in txt.lower() or "under-subscription" in txt.lower():
        print(f"Allot P{pno+1}:")
        print(txt[:1200])
doc_allot.close()
