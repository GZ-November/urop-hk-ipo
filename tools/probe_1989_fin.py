import pymupdf
from pathlib import Path

p_dir = Path("analysis/out/pilot_48_raw_docs/2_1989_HK")
doc = pymupdf.open(p_dir / "prospectus_full.pdf")

# 1. Share capital
for pno in range(180, 240):
    txt = doc[pno].get_text()
    if "share capital" in txt.lower() and "issued and to be issued" in txt.lower():
        print(f"Share Cap P{pno+1}:")
        print(txt[:1000])
        break

# 2. UW commission
for pno in range(350, 420):
    txt = doc[pno].get_text()
    if "commission and expenses" in txt.lower() or "underwriting commission" in txt.lower():
        print(f"UW Commission P{pno+1}:")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["commission", "%", "expenses", "hk$"]):
                print("  ", line)
        break

# 3. Fin info: income statement & balance sheet & cash flow
for pno in range(250, 320):
    txt = doc[pno].get_text()
    if "combined statements of comprehensive income" in txt.lower() or "combined income statement" in txt.lower():
        print(f"Income stmt P{pno+1}:")
        print(txt[:1500])
        break

for pno in range(250, 320):
    txt = doc[pno].get_text()
    if "combined statements of financial position" in txt.lower() or "combined balance sheet" in txt.lower():
        print(f"Balance sheet P{pno+1}:")
        print(txt[:1500])
        break

for pno in range(250, 320):
    txt = doc[pno].get_text()
    if "combined statements of cash flows" in txt.lower():
        print(f"Cash flows P{pno+1}:")
        print(txt[:1500])
        break

doc.close()
