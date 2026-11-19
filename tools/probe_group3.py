from pathlib import Path
import pymupdf

ROOT = Path("analysis/out/pilot_48_raw_docs")

group3 = [
    ("2722.HK", "2_2722_HK"),
    ("8267.HK", "2_8267_HK"),
    ("8325.HK", "2_8325_HK"),
    ("8348.HK", "2_8348_HK")
]

for code, dname in group3:
    print(f"\n{'='*70}\nPROBING {code} ({dname})\n{'='*70}")
    p = ROOT / dname
    files = sorted(list(p.glob("*.pdf")) + list(p.glob("*.PDF")), key=lambda x: x.name)
    
    # 1. Allotment
    allot_files = [f for f in files if "allot" in f.name.lower()]
    for af in allot_files:
        doc = pymupdf.open(af)
        for pno in range(min(5, len(doc))):
            txt = doc[pno].get_text()
            if any(k in txt.lower() for k in ["valid application", "times", "clawback", "reallocat", "cornerstone", "offer price", "placing price"]):
                print(f"--- ALLOT {af.name} P{pno+1} ---")
                for line in txt.split("\n"):
                    if any(k in line.lower() for k in ["valid application", "times", "clawback", "reallocat", "cornerstone", "determined", "placing price"]):
                        print("  ", line)
        doc.close()

    # 2. Underwriting & Listing expenses
    pros_files = [f for f in files if "allot" not in f.name.lower()]
    for pf in pros_files:
        doc = pymupdf.open(pf)
        for pno in range(len(doc)):
            txt = doc[pno].get_text()
            if "underwriting commission" in txt.lower() or ("commission" in txt.lower() and "listing expenses" in txt.lower()):
                print(f"--- UW {pf.name} P{pno+1} ---")
                for line in txt.split("\n"):
                    if any(k in line.lower() for k in ["commission", "%", "expenses", "hk$"]):
                        print("  ", line)
                break
        doc.close()

