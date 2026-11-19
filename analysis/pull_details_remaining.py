import pymupdf, re

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

def search_pdf(pdf_path, terms):
    doc = pymupdf.open(pdf_path)
    res = {}
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        for term in terms:
            if term.lower() in txt.lower():
                if term not in res:
                    res[term] = []
                res[term].append((pno+1, txt))
    doc.close()
    return res

# 1. 6119.HK
print("=== 6119.HK Details ===")
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_6119_HK/prospectus_full.pdf")
for p in range(len(doc)):
    t = doc[p].get_text()
    if "SHARE CAPITAL" in t and ("Issued and to be issued" in t or "Shares in issue" in t):
        print("Share capital p", p+1, ":\n", clean(t[:500]))
        break
for p in range(215, 235):
    t = doc[p].get_text()
    if "estimated listing expenses" in t.lower() or "total listing expenses" in t.lower():
        print("Listing expenses p", p+1, ":\n", clean(t[:500]))
        break
for p in range(len(doc)):
    t = doc[p].get_text()
    if "underwriting commission of" in t.lower() and "%" in t:
        print("Und commission p", p+1, ":\n", clean(t[:400]))
        break
for p in range(len(doc)):
    t = doc[p].get_text()
    if "incorporated in the Cayman Islands" in t:
        print("Incorporation p", p+1, ":\n", clean(t[:300]))
        break
for p in range(80, 105):
    t = doc[p].get_text()
    if "commenced" in t.lower() or "founded" in t.lower() or "history" in t.lower():
        if "our history" in t.lower():
            print("History p", p+1, ":\n", clean(t[:500]))
            break
doc.close()

# Allotment 6119.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_6119_HK/allot_sec_2_E102.PDF")
txt = "\n".join([doc[p].get_text() for p in range(len(doc))])
print("6119 Allotment:\n", clean(txt[:1000]))
doc.close()

