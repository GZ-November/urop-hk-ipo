import pymupdf
from pathlib import Path

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1318_HK")

# 1. Corp info & history
doc_corp = pymupdf.open(p_dir / "pros_sec_corporate_info_E112.pdf")
print("=== 1318 CORP INFO ===")
print(doc_corp[0].get_text()[:1000])
doc_corp.close()

# 2. Share capital
doc_cap = pymupdf.open(p_dir / "pros_sec_share_capital_E120.pdf")
print("=== 1318 SHARE CAPITAL ===")
for pno in range(len(doc_cap)):
    print(doc_cap[pno].get_text())
doc_cap.close()

# 3. Summary financial info
doc_sum = pymupdf.open(p_dir / "pros_sec_summary_E105.pdf")
print("=== 1318 SUMMARY FINANCIAL ===")
for pno in range(len(doc_sum)):
    txt = doc_sum[pno].get_text()
    if any(k in txt.lower() for k in ["turnover", "revenue", "profit for the year", "total assets"]):
        print(f"Summary P{pno+1}:")
        print(txt[:1500])
doc_sum.close()

