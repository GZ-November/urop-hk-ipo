import pymupdf
from pathlib import Path

p_dir = Path("analysis/out/pilot_48_raw_docs/2_2722_HK")

# 1. Share capital
doc_cap = pymupdf.open(p_dir / "pros_sec_share_capital_E120.pdf")
print("=== 2722 SHARE CAPITAL ===")
for pno in range(len(doc_cap)):
    print(doc_cap[pno].get_text())
doc_cap.close()

# 2. Allotment
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== 2722 ALLOTMENT ===")
for pno in range(min(5, len(doc_allot))):
    txt = doc_allot[pno].get_text()
    if any(k in txt.lower() for k in ["valid application", "times", "clawback", "reallocat", "cornerstone"]):
        print(f"Allot P{pno+1}:")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["offer price", "valid application", "times", "clawback", "reallocat", "cornerstone", "pool a", "pool b", "final number"]):
                print("  ", line)
doc_allot.close()

# 3. Summary financial info
doc_sum = pymupdf.open(p_dir / "pros_sec_summary_E104.pdf")
print("=== 2722 SUMMARY FINANCIAL ===")
for pno in range(len(doc_sum)):
    txt = doc_sum[pno].get_text()
    if any(k in txt.lower() for k in ["turnover", "revenue", "profit for the year", "total assets"]):
        print(f"Summary P{pno+1}:")
        print(txt[:1500])
doc_sum.close()
