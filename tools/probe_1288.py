from pathlib import Path
import pymupdf

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1288_HK")

# 1. Allotment
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== 1288 ALLOTMENT (len={}) ===".format(len(doc_allot)))
for pno in range(min(5, len(doc_allot))):
    print(f"--- Allot Page {pno+1} ---")
    print(doc_allot[pno].get_text()[:1200])
doc_allot.close()

# 2. Cover / summary offering structure
doc_cover = pymupdf.open(p_dir / "pros_sec_cover_E101.pdf")
print("=== 1288 COVER ===")
print(doc_cover[0].get_text()[:1500])
doc_cover.close()

# 3. Share capital
doc_cap = pymupdf.open(p_dir / "pros_sec_share_capital_E124.pdf")
print("=== 1288 SHARE CAPITAL ===")
print(doc_cap[0].get_text()[:1500])
doc_cap.close()

# 4. Underwriting
doc_uw = pymupdf.open(p_dir / "pros_sec_underwriting_E127.pdf")
print("=== 1288 UNDERWRITING ===")
for pno in range(len(doc_uw)):
    txt = doc_uw[pno].get_text()
    if "commission" in txt.lower():
        print(f"--- UW Page {pno+1} ---")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["commission", "%", "expenses", "hk$"]):
                print("  ", line)
doc_uw.close()

# 5. History / corporate info
doc_hist = pymupdf.open(p_dir / "pros_sec_history_E114.pdf")
print("=== 1288 HISTORY ===")
print(doc_hist[0].get_text()[:1500])
doc_hist.close()

doc_corp = pymupdf.open(p_dir / "pros_sec_corporate_info_E110.pdf")
print("=== 1288 CORP INFO ===")
print(doc_corp[0].get_text()[:1500])
doc_corp.close()

