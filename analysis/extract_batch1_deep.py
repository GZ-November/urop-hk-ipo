import os, glob, re
import pymupdf

RAW_DOCS_DIR = "analysis/out/pilot_48_raw_docs"
deals = [
    "1_1672_HK", "1_1712_HK", "1_1743_HK", "1_1749_HK",
    "1_1821_HK", "1_2025_HK", "1_3738_HK", "1_6119_HK",
    "1_8447_HK", "1_8516_HK", "1_8645_HK", "1_9988_HK"
]

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

results = {}

for deal in deals:
    dpath = os.path.join(RAW_DOCS_DIR, deal)
    print(f"\n{'='*80}\nDEAL: {deal}\n{'='*80}")
    
    # Check all files
    pfiles = sorted(glob.glob(os.path.join(dpath, "prospectus_full.pdf")) + glob.glob(os.path.join(dpath, "pros_sec_*.pdf")))
    
    print(f"Prospectus files for {deal}: {[os.path.basename(f) for f in pfiles]}")
    
    for pf in pfiles:
        pf_name = os.path.basename(pf)
        doc = pymupdf.open(pf)
        
        # Look for share capital table
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if "SHARE CAPITAL" in txt.upper() and ("issued and to be issued" in txt.lower() or "shares to be issued" in txt.lower() or "capitalisation issue" in txt.lower()):
                print(f"[{pf_name} Page {pno+1} - SHARE CAPITAL]:")
                lines = [l.strip() for l in txt.split("\n") if l.strip()]
                print("\n".join(lines[:25]))
                print("-" * 50)
                break
                
        # Look for Offer price range on cover
        if "prospectus_full" in pf_name or "cover" in pf_name or "summary" in pf_name:
            for pno in range(min(5, len(doc))):
                txt = doc[pno].get_text()
                if "OFFER PRICE" in txt.upper() or "PRICE RANGE" in txt.upper() or "MAXIMUM OFFER PRICE" in txt.upper():
                    for line in txt.split("\n"):
                        if any(k in line.lower() for k in ["maximum offer price", "not more than hk$", "not less than hk$", "hk$", "offer price range", "indicative offer price"]):
                            print(f"[{pf_name} Page {pno+1} - Price]: {clean(line)}")

        doc.close()

