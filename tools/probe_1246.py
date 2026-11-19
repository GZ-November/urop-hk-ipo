from pathlib import Path
import pymupdf

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1246_HK")

# 1. Allotment
doc_allot = pymupdf.open(p_dir / "allot_sec_2_E102.PDF")
print("=== 1246 ALLOTMENT (len={}) ===".format(len(doc_allot)))
for pno in range(min(4, len(doc_allot))):
    print(f"--- Allot Page {pno+1} ---")
    print(doc_allot[pno].get_text()[:1200])
doc_allot.close()

# 2. Prospectus
doc_pros = pymupdf.open(p_dir / "prospectus_full.pdf")
print("=== 1246 PROSPECTUS (len={}) ===".format(len(doc_pros)))

# Search underwriting commission and listing expenses
for pno in range(len(doc_pros)):
    txt = doc_pros[pno].get_text()
    if "underwriting commission" in txt.lower():
        print(f"--- Underwriting Commission Page {pno+1} ---")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["commission", "%", "expenses", "hk$"]):
                print("  ", line)
        break

# Search history & corporate info
for pno in range(min(120, len(doc_pros))):
    txt = doc_pros[pno].get_text()
    if "corporate information" in txt.lower() and "registered office" in txt.lower():
        print(f"--- Corp Info Page {pno+1} ---")
        print(txt[:1000])
        break

for pno in range(min(120, len(doc_pros))):
    txt = doc_pros[pno].get_text()
    if "history and development" in txt.lower() or "history and corporate structure" in txt.lower():
        print(f"--- History Page {pno+1} ---")
        print(txt[:1000])
        break

# Search share capital
for pno in range(min(180, len(doc_pros))):
    txt = doc_pros[pno].get_text()
    if "share capital" in txt.lower() and "issued and to be issued" in txt.lower():
        print(f"--- Share Capital Page {pno+1} ---")
        print(txt[:1000])
        break

# Search financial summary / income statement
for pno in range(min(80, len(doc_pros))):
    txt = doc_pros[pno].get_text()
    if "summary financial information" in txt.lower() or ("selected" in txt.lower() and "income statement" in txt.lower()):
        print(f"--- Summary Fin Info Page {pno+1} ---")
        print(txt[:1500])
        break

doc_pros.close()
