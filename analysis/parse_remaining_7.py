import os, glob, pymupdf, re

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

deals = ["1_2025_HK", "1_3738_HK", "1_6119_HK", "1_8447_HK", "1_8516_HK", "1_8645_HK", "1_9988_HK"]

with open("/tmp/batch1_fin_dump.txt") as f:
    fin_text = f.read()

for d in deals:
    print(f"\n{'='*70}\nDEAL: {d}\n{'='*70}")
    # Extract allotment info
    dpath = os.path.join("analysis/out/pilot_48_raw_docs", d)
    afiles = sorted(glob.glob(os.path.join(dpath, "allot_sec_2_*.pdf")) + glob.glob(os.path.join(dpath, "allot_sec_2_*.PDF")) + glob.glob(os.path.join(dpath, "allot_sec_1_*.pdf")))
    if afiles:
        adoc = pymupdf.open(afiles[0])
        atxt = "\n".join([adoc[p].get_text() for p in range(len(adoc))])
        adoc.close()
        print(">> ALLOTMENT:")
        for m in re.finditer(r"(Offer Price has been determined at|Offer Price is|Offer Price per Offer Share is)\s*(HK\$[\d\.]+)", atxt, re.I):
            print(" ", m.group(0))
            break
        for m in re.finditer(r"(A total of .*?valid applications.*?times|valid applications have been received.*?times|equivalent to approximately\s*[\d\.]+\s*times|representing approximately\s*[\d\.]+\s*times)", atxt, re.I):
            chunk = atxt[max(0, m.start()-20):min(len(atxt), m.end()+200)]
            print("  Subscription:", clean(chunk))
            break
        for m in re.finditer(r"(reallocation.*?effected|clawback.*?applied|reallocation procedure.*?applied|no reallocation|mandatory reallocation)", atxt, re.I):
            chunk = atxt[max(0, m.start()-20):min(len(atxt), m.end()+250)]
            print("  Clawback:", clean(chunk))
            break
        cs_m = list(re.finditer(r"cornerstone", atxt, re.I))
        if cs_m:
            print("  Cornerstone found:", len(cs_m), "mentions")
            for cm in cs_m[:1]:
                print("   ", clean(atxt[max(0, cm.start()-30):min(len(atxt), cm.end()+200)]))
        else:
            print("  Cornerstone: None")

    # Prospectus cover / share capital
    pfiles = sorted(glob.glob(os.path.join(dpath, "prospectus_full.pdf")) + glob.glob(os.path.join(dpath, "pros_sec_cover*.pdf")))
    if pfiles:
        pdoc = pymupdf.open(pfiles[0])
        ptxt = "\n".join([pdoc[p].get_text() for p in range(min(5, len(pdoc)))])
        print(">> PROSPECTUS COVER:")
        for line in ptxt.split("\n"):
            if any(k in line.lower() for k in ["number of offer shares", "offer price range", "not more than hk$", "not less than hk$", "maximum offer price", "over-allotment option"]):
                print(" ", clean(line))
        pdoc.close()

