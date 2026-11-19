from pathlib import Path
import pymupdf

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
RAW_DOCS = ROOT / "analysis" / "out" / "pilot_48_raw_docs"

def search_pdf(pdf_path, keywords, max_matches=5):
    doc = pymupdf.open(pdf_path)
    res = []
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        tl = txt.lower()
        if all(k.lower() in tl for k in keywords):
            res.append((pno+1, txt))
            if len(res) >= max_matches:
                break
    doc.close()
    return res

print("=== 0968.HK Little Sheep ===")
# underwriting commission & listing expenses
p = RAW_DOCS / "2_0968_HK" / "pros_sec_underwriting_E122.pdf"
matches = search_pdf(p, ["commission"])
for pno, txt in matches:
    print(f"--- Underwriting Page {pno} ---")
    for line in txt.split("\n"):
        if any(w in line.lower() for w in ["commission", "expenses", "hk$", "%"]):
            print("  ", line)

# Corporate info / history
p = RAW_DOCS / "2_0968_HK" / "pros_sec_history_E112.pdf"
matches = search_pdf(p, ["commenced", "restaurant"])
for pno, txt in matches[:2]:
    print(f"--- History Page {pno} ---")
    print(txt[:800])

p = RAW_DOCS / "2_0968_HK" / "pros_sec_corporate_info_E110.pdf"
matches = search_pdf(p, ["registered office"])
for pno, txt in matches[:1]:
    print(f"--- Corp Info Page {pno} ---")
    print(txt[:800])

# Financial info: Year-1 table
p = RAW_DOCS / "2_0968_HK" / "pros_sec_financial_info_E120.pdf"
matches = search_pdf(p, ["turnover", "profit before tax", "total assets"])
if not matches:
    matches = search_pdf(p, ["turnover", "profit before tax"])
for pno, txt in matches[:2]:
    print(f"--- Fin Info Page {pno} ---")
    print(txt[:1200])

