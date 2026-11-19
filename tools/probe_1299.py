from pathlib import Path
import pymupdf

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1299_HK")

# 1. Allotment
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== 1299 ALLOTMENT (len={}) ===".format(len(doc_allot)))
for pno in range(min(5, len(doc_allot))):
    txt = doc_allot[pno].get_text()
    print(f"--- Allot Page {pno+1} ---")
    print(txt[:1000])
doc_allot.close()

# 2. Summary
doc_sum = pymupdf.open(p_dir / "pros_sec_summary_E106.pdf")
print("=== 1299 SUMMARY (len={}) ===".format(len(doc_sum)))
for pno in range(min(10, len(doc_sum))):
    txt = doc_sum[pno].get_text()
    if "offer statistics" in txt.lower() or "offer shares" in txt.lower():
        print(f"--- Summary Page {pno+1} ---")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["offer price", "hk$", "shares", "selling shareholder"]):
                print("  ", line)
doc_sum.close()

# 3. Share Capital
doc_cap = pymupdf.open(p_dir / "pros_sec_share_capital_E124.pdf")
print("=== 1299 SHARE CAPITAL ===")
for pno in range(len(doc_cap)):
    print(doc_cap[pno].get_text())
doc_cap.close()

# 4. Underwriting
doc_uw = pymupdf.open(p_dir / "pros_sec_underwriting_E128.pdf")
print("=== 1299 UNDERWRITING ===")
for pno in range(len(doc_uw)):
    txt = doc_uw[pno].get_text()
    if "commission" in txt.lower():
        print(f"--- UW Page {pno+1} ---")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["commission", "%", "expenses", "hk$"]):
                print("  ", line)
doc_uw.close()

# 5. Corporate Info & History
doc_corp = pymupdf.open(p_dir / "pros_sec_corporate_info_E113.pdf")
print("=== 1299 CORP INFO ===")
print(doc_corp[0].get_text()[:1000])
doc_corp.close()

doc_hist = pymupdf.open(p_dir / "pros_sec_history_E117.pdf")
print("=== 1299 HISTORY ===")
print(doc_hist[0].get_text()[:1000])
doc_hist.close()

