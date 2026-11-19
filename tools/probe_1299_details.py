import pymupdf
from pathlib import Path

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1299_HK")

# 1. Incorporation date and jurisdiction
doc_corp = pymupdf.open(p_dir / "pros_sec_corporate_info_E113.pdf")
print("=== CORP INFO ===")
for pno in range(len(doc_corp)):
    txt = doc_corp[pno].get_text()
    if "registered office" in txt.lower():
        print(f"Page {pno+1}:")
        print(txt[:1000])
doc_corp.close()

doc_hist = pymupdf.open(p_dir / "pros_sec_history_E117.pdf")
print("=== HISTORY (incorporation of Company) ===")
for pno in range(len(doc_hist)):
    txt = doc_hist[pno].get_text()
    if "company was incorporated" in txt.lower() or "incorporated in" in txt.lower():
        print(f"Page {pno+1}:")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["incorporated", "registered", "company was"]):
                print("  ", line)
doc_hist.close()

# 2. Base shares and capital structure
doc_cap = pymupdf.open(p_dir / "pros_sec_share_capital_E124.pdf")
print("=== SHARE CAPITAL (full) ===")
for pno in range(len(doc_cap)):
    print(f"Page {pno+1}:")
    print(doc_cap[pno].get_text())
doc_cap.close()

# 3. Allotment: clawback, final shares, cornerstone
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== ALLOTMENT (clawback & final shares & cornerstone) ===")
for pno in range(3, min(9, len(doc_allot))):
    txt = doc_allot[pno].get_text()
    for w in ["reallocation", "clawback", "cornerstone", "final number", "pool a", "pool b"]:
        if w in txt.lower():
            print(f"Allot P{pno+1} ({w}):")
            for line in txt.split("\n"):
                if any(k in line.lower() for k in ["clawback", "reallocat", "final number", "cornerstone", "offer shares comprised"]):
                    print("  ", line)
doc_allot.close()

# 4. Financial tables in Summary
doc_sum = pymupdf.open(p_dir / "pros_sec_summary_E106.pdf")
print("=== FINANCIAL TABLES IN SUMMARY ===")
for pno in range(len(doc_sum)):
    txt = doc_sum[pno].get_text()
    if "summary historical financial" in txt.lower() or ("income statement" in txt.lower() and "revenue" in txt.lower()):
        print(f"Summary P{pno+1}:")
        print(txt[:1500])
doc_sum.close()
