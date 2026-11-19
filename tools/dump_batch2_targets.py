from pathlib import Path
import pymupdf

ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
RAW_DOCS = ROOT / "analysis" / "out" / "pilot_48_raw_docs"
OUT_FILE = Path("/tmp/batch2_full_targets.txt")

issuers = [
    "2_0968_HK", "2_1246_HK", "2_1288_HK", "2_1299_HK", "2_1318_HK", "2_1333_HK",
    "2_1989_HK", "2_2289_HK", "2_2722_HK", "2_8267_HK", "2_8325_HK", "2_8348_HK"
]

out = []

def extract_pages(pdf_path, predicate, max_pages=10):
    matched = []
    doc = pymupdf.open(pdf_path)
    for pno in range(len(doc)):
        text = doc[pno].get_text()
        if predicate(text):
            matched.append((pno + 1, text))
            if len(matched) >= max_pages:
                break
    doc.close()
    return matched

for code in issuers:
    out.append(f"\n{'='*80}\nISSUER: {code}\n{'='*80}\n")
    p = RAW_DOCS / code
    files = sorted(list(p.glob("*.pdf")) + list(p.glob("*.PDF")), key=lambda x: x.name)

    # 1. Allotment Announcement
    allot_files = [f for f in files if "allot" in f.name.lower()]
    for af in allot_files:
        doc = pymupdf.open(af)
        for pno in range(min(5, len(doc))):
            txt = doc[pno].get_text()
            if any(k in txt.lower() for k in ["valid application", "offer price", "clawback", "reallocation", "basis of allotment", "net proceeds", "cornerstone"]):
                out.append(f"--- ALLOT DOC: {af.name} Page {pno+1} ---")
                out.append(txt)
        doc.close()

    # 2. Prospectus: Cover & Share Capital & Underwriting & Corporate Info & History
    pros_files = [f for f in files if "allot" not in f.name.lower()]
    for pf in pros_files:
        doc = pymupdf.open(pf)
        name_lower = pf.name.lower()
        
        # Cover / Offering Structure
        if any(k in name_lower for k in ["cover", "offering_structure", "share_capital", "summary"]):
            for pno in range(min(15, len(doc))):
                txt = doc[pno].get_text()
                if any(k in txt.lower() for k in ["number of offer shares", "offer price", "over-allotment option", "share capital", "issued shares"]):
                    out.append(f"--- PROS OFFER/CAPITAL: {pf.name} Page {pno+1} ---")
                    out.append(txt)

        # Corporate info / History
        if any(k in name_lower for k in ["corporate_info", "history", "controlling"]):
            for pno in range(min(15, len(doc))):
                txt = doc[pno].get_text()
                if any(k in txt.lower() for k in ["incorporated", "headquarters", "principal place", "controlling shareholder", "commenced", "established", "founded"]):
                    out.append(f"--- PROS CORP/HIST: {pf.name} Page {pno+1} ---")
                    out.append(txt)

        # Underwriting / Commission
        if "underwriting" in name_lower:
            for pno in range(min(10, len(doc))):
                txt = doc[pno].get_text()
                if any(k in txt.lower() for k in ["commission", "listing expenses"]):
                    out.append(f"--- PROS UNDERWRITING: {pf.name} Page {pno+1} ---")
                    out.append(txt)

        # Financial info / Accountants report
        if any(k in name_lower for k in ["financial_info", "accountants_report"]):
            for pno in range(len(doc)):
                txt = doc[pno].get_text()
                # Check for income statement / balance sheet / cash flows
                has_rev = any(k in txt.lower() for k in ["revenue", "turnover", "net interest income"])
                has_prof = any(k in txt.lower() for k in ["profit before tax", "profit for the year", "profit for the period"])
                has_bal = any(k in txt.lower() for k in ["total assets", "total equity", "net assets"])
                has_cf = any(k in txt.lower() for k in ["operating activities", "cash flows from operating"])
                
                if (has_rev and has_prof) or has_bal or has_cf:
                    out.append(f"--- PROS FINANCIAL: {pf.name} Page {pno+1} ---")
                    out.append(txt)

        # For single prospectus_full.pdf
        if "prospectus_full.pdf" in name_lower:
            # We search targeted pages
            for pno in range(len(doc)):
                txt = doc[pno].get_text()
                tl = txt.lower()
                # cover
                if pno < 10 and ("number of offer shares" in tl or "offer price" in tl):
                    out.append(f"--- FULL PROS COVER Page {pno+1} ---")
                    out.append(txt)
                # corporate info
                if "corporate information" in tl and ("registered office" in tl or "principal place" in tl):
                    out.append(f"--- FULL PROS CORP INFO Page {pno+1} ---")
                    out.append(txt)
                # history
                if "history" in tl and ("commenced" in tl or "established" in tl or "founded" in tl) and pno < 120:
                    out.append(f"--- FULL PROS HISTORY Page {pno+1} ---")
                    out.append(txt)
                # share capital
                if "share capital" in tl and "issued and to be issued" in tl:
                    out.append(f"--- FULL PROS SHARE CAPITAL Page {pno+1} ---")
                    out.append(txt)
                # underwriting commission
                if "underwriting commission" in tl and ("expenses" in tl or "percent" in tl or "%" in tl):
                    out.append(f"--- FULL PROS UNDERWRITING Page {pno+1} ---")
                    out.append(txt)
                # financial tables: income statement
                if (("combined income statement" in tl or "consolidated income statement" in tl or "combined statements of comprehensive income" in tl or "consolidated statements of profit or loss" in tl) and ("revenue" in tl or "turnover" in tl) and ("profit before tax" in tl or "profit for the year" in tl)):
                    out.append(f"--- FULL PROS FINANCIAL INC STMT Page {pno+1} ---")
                    out.append(txt)
                # balance sheet
                if (("combined balance sheet" in tl or "consolidated balance sheet" in tl or "combined statements of financial position" in tl or "consolidated statements of financial position" in tl) and "total assets" in tl and ("total equity" in tl or "net assets" in tl)):
                    out.append(f"--- FULL PROS FINANCIAL BAL SHEET Page {pno+1} ---")
                    out.append(txt)
                # cash flows
                if (("combined cash flow statement" in tl or "consolidated cash flow statement" in tl or "combined statements of cash flows" in tl or "consolidated statements of cash flows" in tl) and ("net cash flows from operating activities" in tl or "net cash generated from operating activities" in tl or "net cash from operating activities" in tl or "cash generated from operations" in tl)):
                    out.append(f"--- FULL PROS FINANCIAL CASH FLOW Page {pno+1} ---")
                    out.append(txt)

        doc.close()

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print(f"Dumped targets to {OUT_FILE}, total characters: {len(out)}, size: {OUT_FILE.stat().st_size / 1024:.1f} KB")
