import pymupdf
from pathlib import Path

def inspect_0249():
    print("=== 0249.HK ===")
    raw = Path("analysis/out/pilot_48_raw_docs/3_0249_HK")
    # check offering structure
    doc = pymupdf.open(raw / "pros_sec_offering_structure_F108.pdf")
    for i in range(len(doc)):
        t = doc[i].get_text()
        if "offer price" in t.lower() or "new shares" in t.lower():
            print(f"Structure p{i+1}:", t[:400].replace("\n", " "))
    # check corporate info
    doc = pymupdf.open(raw / "pros_sec_corporate_info_F110.pdf")
    for i in range(len(doc)):
        print(f"CorpInfo p{i+1}:", doc[i].get_text()[:400].replace("\n", " "))
    # check summary / history
    doc = pymupdf.open(raw / "pros_sec_summary_F104.pdf")
    for i in range(len(doc)):
        t = doc[i].get_text()
        if "founded" in t.lower() or "established" in t.lower() or "history" in t.lower() or "brewery" in t.lower():
            print(f"Summary p{i+1}:", t[:400].replace("\n", " "))
    # check underwriting
    doc = pymupdf.open(raw / "pros_sec_underwriting_F122.pdf")
    for i in range(len(doc)):
        t = doc[i].get_text()
        if "commission" in t.lower():
            print(f"Underwriting p{i+1}:", t[:400].replace("\n", " "))
    # check accountants report
    doc = pymupdf.open(raw / "pros_sec_accountants_report_F125.pdf")
    for i in range(min(15, len(doc))):
        t = doc[i].get_text()
        if "turnover" in t.lower() or "profit before" in t.lower() or "balance sheet" in t.lower():
            print(f"AcctReport p{i+1}:", t[:600].replace("\n", " "))

if __name__ == "__main__":
    inspect_0249()
