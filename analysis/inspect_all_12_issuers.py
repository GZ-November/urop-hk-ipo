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

for deal in deals:
    dpath = os.path.join(RAW_DOCS_DIR, deal)
    print(f"\n{'='*80}\nDEAL: {deal}\n{'='*80}")
    
    # 1. Allotment doc
    allot_files = sorted(glob.glob(os.path.join(dpath, "allot_sec_2_*.pdf")) + glob.glob(os.path.join(dpath, "allot_sec_2_*.PDF")))
    if not allot_files:
        allot_files = sorted(glob.glob(os.path.join(dpath, "allot_sec_1_*.pdf")) + glob.glob(os.path.join(dpath, "allot_sec_1_*.PDF")))
    
    if allot_files:
        adoc = pymupdf.open(allot_files[0])
        atext = ""
        for p in range(len(adoc)):
            atext += f"\n--- Page {p+1} ---\n" + adoc[p].get_text()
        
        print(">> ALLOTMENT HIGHLIGHTS:")
        # Offer price
        m_op = re.search(r"Offer Price (has been determined at|per Offer Share|is)\s*(HK\$[\d\.]+)", atext, re.I)
        if m_op:
            print("  Offer Price:", m_op.group(0))
        
        # Subscription multiple / applications
        for m in re.finditer(r"(valid applications.*?times|applications.*?received.*?times|subscription.*?\b\d+\.\d+\s*times|approximately\s*\d+(\.\d+)?\s*times)", atext, re.I):
            start = max(0, m.start() - 50)
            end = min(len(atext), m.end() + 150)
            print("  Subscription:", clean(atext[start:end]))
            break
            
        # Reallocation / clawback
        for m in re.finditer(r"(reallocation.*?effected|clawback.*?applied|reallocation.*?exercised|mandatory reallocation)", atext, re.I):
            start = max(0, m.start() - 50)
            end = min(len(atext), m.end() + 200)
            print("  Reallocation:", clean(atext[start:end]))
            break

        # Cornerstone
        cs_matches = list(re.finditer(r"cornerstone", atext, re.I))
        if cs_matches:
            for cm in cs_matches[:2]:
                start = max(0, cm.start() - 50)
                end = min(len(atext), cm.end() + 200)
                print("  Cornerstone snippet:", clean(atext[start:end]))
        else:
            print("  Cornerstone: None mentioned in announcement body")
        adoc.close()

print("\nDone inspect allotment.")
