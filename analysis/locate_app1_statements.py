import os, glob, pymupdf

deals = [
    "1_1672_HK", "1_1712_HK", "1_1743_HK", "1_1749_HK", "1_1821_HK",
    "1_2025_HK", "1_3738_HK", "1_6119_HK", "1_8447_HK",
    "1_8516_HK", "1_8645_HK", "1_9988_HK"
]

for d in deals:
    dpath = os.path.join("analysis/out/pilot_48_raw_docs", d)
    pdfs = glob.glob(os.path.join(dpath, "prospectus_full.pdf")) + glob.glob(os.path.join(dpath, "pros_sec_accountants*.pdf"))
    if not pdfs:
        continue
    pdf = pdfs[0]
    doc = pymupdf.open(pdf)
    print(f"\n{'='*70}\nDEAL: {d} ({os.path.basename(pdf)}, {len(doc)} pages)\n{'='*70}")
    
    # Search backwards or forward for Appendix I
    app1_pages = []
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        if ("APPENDIX I" in txt.upper() or "APPENDIX IA" in txt.upper()) and ("ACCOUNTANTS" in txt.upper() or "ACCOUNTANTS’ REPORT" in txt.upper()):
            app1_pages.append(pno)
            
    print(f"Appendix I pages count: {len(app1_pages)}, first page: {app1_pages[0]+1 if app1_pages else 'None'}")
    if app1_pages:
        # Check first 20 pages of Appendix I for the 3 primary financial statements
        for pno in app1_pages[:25]:
            txt = doc[pno].get_text()
            lines = [l.strip() for l in txt.split("\n") if l.strip()]
            header = " ".join(lines[:4]).upper()
            if any(k in header for k in ["STATEMENT OF PROFIT OR LOSS", "STATEMENT OF COMPREHENSIVE INCOME", "STATEMENTS OF PROFIT OR LOSS", "STATEMENTS OF COMPREHENSIVE INCOME"]):
                print(f"  >> Page {pno+1}: Income Statement Header:\n    {lines[:8]}")
            elif any(k in header for k in ["STATEMENT OF FINANCIAL POSITION", "STATEMENTS OF FINANCIAL POSITION", "BALANCE SHEET", "BALANCE SHEETS"]):
                print(f"  >> Page {pno+1}: Balance Sheet Header:\n    {lines[:8]}")
            elif any(k in header for k in ["STATEMENT OF CASH FLOWS", "STATEMENTS OF CASH FLOWS"]):
                print(f"  >> Page {pno+1}: Cash Flows Header:\n    {lines[:8]}")
    doc.close()
