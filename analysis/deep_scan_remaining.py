import os, glob, re
import pymupdf

RAW_DOCS = "analysis/out/pilot_48_raw_docs"
deals = [
    "1_1712_HK", "1_1743_HK", "1_1749_HK", "1_2025_HK",
    "1_3738_HK", "1_6119_HK", "1_8447_HK", "1_8516_HK",
    "1_8645_HK", "1_9988_HK"
]

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

for deal in deals:
    dpath = os.path.join(RAW_DOCS, deal)
    print(f"\n{'='*70}\nSCANNING: {deal}\n{'='*70}")
    
    # Check prospectus files
    pfiles = sorted(glob.glob(os.path.join(dpath, "prospectus_full.pdf")) + glob.glob(os.path.join(dpath, "pros_sec_*.pdf")))
    
    # 1. Underwriting commission and listing expenses
    for pf in pfiles:
        doc = pymupdf.open(pf)
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if "COMMISSION" in txt.upper() and ("gross underwriting commission" in txt.lower() or "underwriting commission of" in txt.lower() or "commission equal to" in txt.lower()):
                for line in txt.split("\n"):
                    if any(k in line.lower() for k in ["commission", "%", "incentive"]):
                        print(f"[{os.path.basename(pf)} p{pno+1} Und Comm]: {clean(line)}")
                break
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if "LISTING EXPENSES" in txt.upper() and ("estimated listing expenses" in txt.lower() or "total listing expenses" in txt.lower() or "listing expenses relating to" in txt.lower()):
                for line in txt.split("\n"):
                    if any(k in line.lower() for k in ["million", "hk$", "rmb", "aud", "usd", "estimated to be", "aggregate to"]):
                        print(f"[{os.path.basename(pf)} p{pno+1} Listing Exp]: {clean(line)}")
                break
        doc.close()

    # 2. Corporate history & founding year & incorporation date
    for pf in pfiles:
        doc = pymupdf.open(pf)
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if ("HISTORY AND DEVELOPMENT" in txt.upper() or "HISTORY, DEVELOPMENT AND" in txt.upper() or "HISTORY, REORGANISATION" in txt.upper() or "OUR HISTORY" in txt.upper()) and len(txt) > 200:
                print(f"[{os.path.basename(pf)} p{pno+1} History snippet]:")
                lines = [clean(l) for l in txt.split("\n") if l.strip()]
                print("  " + "\n  ".join(lines[:12]))
                break
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if "CORPORATE INFORMATION" in txt.upper() and ("registered office" in txt.lower() or "headquarters" in txt.lower() or "principal place of business" in txt.lower()):
                print(f"[{os.path.basename(pf)} p{pno+1} Corp Info snippet]:")
                lines = [clean(l) for l in txt.split("\n") if l.strip()]
                print("  " + "\n  ".join(lines[:10]))
                break
        doc.close()
