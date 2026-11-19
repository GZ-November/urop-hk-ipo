import os, glob
import pymupdf

RAW_DOCS_DIR = "analysis/out/pilot_48_raw_docs"
deals = [
    "1_1712_HK", "1_1743_HK", "1_1749_HK", "1_1821_HK",
    "1_2025_HK", "1_3738_HK", "1_6119_HK", "1_8447_HK",
    "1_8516_HK", "1_8645_HK", "1_9988_HK"
]

for deal in deals:
    dpath = os.path.join(RAW_DOCS_DIR, deal)
    print(f"\n{'='*80}\nDEAL: {deal}\n{'='*80}")
    
    # Financial statements
    # Search for statement of profit or loss
    pfiles = sorted(glob.glob(os.path.join(dpath, "prospectus_full.pdf")) + glob.glob(os.path.join(dpath, "pros_sec_accountants*.pdf")) + glob.glob(os.path.join(dpath, "pros_sec_financial*.pdf")))
    
    for pf in pfiles:
        doc = pymupdf.open(pf)
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if any(h in txt.upper() for h in ["CONSOLIDATED STATEMENTS OF PROFIT OR LOSS", "CONSOLIDATED STATEMENT OF PROFIT OR LOSS", "CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME", "CONSOLIDATED STATEMENT OF COMPREHENSIVE INCOME"]):
                if any(k in txt.lower() for k in ["revenue", "turnover"]) and any(k in txt.lower() for k in ["profit before", "profit for the"]):
                    print(f"[{os.path.basename(pf)} Page {pno+1} - PROFIT OR LOSS]:")
                    for line in txt.split("\n")[:40]:
                        print(" ", line)
                    print("-" * 50)
                    break
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if any(h in txt.upper() for h in ["CONSOLIDATED STATEMENTS OF FINANCIAL POSITION", "CONSOLIDATED STATEMENT OF FINANCIAL POSITION", "CONSOLIDATED BALANCE SHEET"]):
                if any(k in txt.lower() for k in ["total assets", "net assets", "total equity"]):
                    print(f"[{os.path.basename(pf)} Page {pno+1} - FINANCIAL POSITION]:")
                    for line in txt.split("\n")[:40]:
                        print(" ", line)
                    print("-" * 50)
                    break
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if any(h in txt.upper() for h in ["CONSOLIDATED STATEMENTS OF CASH FLOWS", "CONSOLIDATED STATEMENT OF CASH FLOWS"]):
                if any(k in txt.lower() for k in ["cash flows from operating activities", "operating activities", "cash generated from operations"]):
                    print(f"[{os.path.basename(pf)} Page {pno+1} - CASH FLOWS]:")
                    for line in txt.split("\n")[:30]:
                        print(" ", line)
                    print("-" * 50)
                    break
        doc.close()

