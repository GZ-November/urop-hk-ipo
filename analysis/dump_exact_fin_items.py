import pymupdf

def dump_page_lines(doc, pno, start=0, count=60):
    lines = doc[pno-1].get_text().split("\n")
    for i, l in enumerate(lines[start:start+count], start):
        if l.strip():
            print(f"{i}: {l.strip()}")

# 1. 3738.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_3738_HK/prospectus_full.pdf")
print("=== 3738.HK Income Statement (p260) ===")
dump_page_lines(doc, 260, 0, 70)
print("=== 3738.HK Balance Sheet (p261) ===")
dump_page_lines(doc, 261, 0, 80)
print("=== 3738.HK Cash Flows (p264) ===")
dump_page_lines(doc, 264, 0, 50)
doc.close()

# 2. 6119.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_6119_HK/prospectus_full.pdf")
print("\n=== 6119.HK Income Statement (p291) ===")
dump_page_lines(doc, 291, 0, 60)
print("=== 6119.HK Balance Sheet (p292) ===")
dump_page_lines(doc, 292, 0, 70)
print("=== 6119.HK Cash Flows (p296) ===")
dump_page_lines(doc, 296, 0, 50)
doc.close()

# 3. 8447.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_8447_HK/pros_sec_accountants_report_E129.pdf")
print("\n=== 8447.HK Income Statement (p5) ===")
dump_page_lines(doc, 5, 0, 50)
print("=== 8447.HK Balance Sheet (p6) ===")
dump_page_lines(doc, 6, 0, 60)
print("=== 8447.HK Cash Flows (p8) ===")
dump_page_lines(doc, 8, 0, 50)
doc.close()

# 4. 8516.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_8516_HK/prospectus_full.pdf")
print("\n=== 8516.HK Income Statement (p306) ===")
dump_page_lines(doc, 306, 0, 50)
print("=== 8516.HK Balance Sheet (p307) ===")
dump_page_lines(doc, 307, 0, 60)
print("=== 8516.HK Cash Flows (p308) ===")
dump_page_lines(doc, 308, 0, 50)
doc.close()

# 5. 8645.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_8645_HK/prospectus_full.pdf")
print("\n=== 8645.HK Income Statement (p332) ===")
dump_page_lines(doc, 332, 0, 60)
print("=== 8645.HK Balance Sheet (p333) ===")
dump_page_lines(doc, 333, 0, 70)
print("=== 8645.HK Cash Flows (p336) ===")
dump_page_lines(doc, 336, 0, 50)
doc.close()

# 6. 9988.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_9988_HK/pros_sec_accountants_report_2019111500075.pdf")
print("\n=== 9988.HK Income Statement (p5) ===")
dump_page_lines(doc, 5, 0, 60)
print("=== 9988.HK Balance Sheet (p7) ===")
dump_page_lines(doc, 7, 0, 60)
print("=== 9988.HK Balance Sheet Continued (p8) ===")
dump_page_lines(doc, 8, 0, 60)
print("=== 9988.HK Cash Flows (p16) ===")
dump_page_lines(doc, 16, 0, 50)
doc.close()
