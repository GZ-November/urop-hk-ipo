import pymupdf

def get_text_range(doc, start, end):
    return "\n".join([f"--- Page {p+1} ---\n" + doc[p].get_text() for p in range(start-1, min(end, len(doc)))])

# 1. 1712.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_1712_HK/prospectus_full.pdf")
print("=== 1712.HK Income (p395), BS (p397), CF (p399) ===")
print(get_text_range(doc, 395, 399))
doc.close()

# 2. 1743.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_1743_HK/prospectus_full.pdf")
print("=== 1743.HK Income (p292), BS (p294), CF (p298) ===")
print(get_text_range(doc, 292, 299))
doc.close()

# 3. 1749.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_1749_HK/prospectus_full.pdf")
print("=== 1749.HK Income (p381), BS (p382), CF (p385) ===")
print(get_text_range(doc, 381, 385))
doc.close()

# 4. 2025.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_2025_HK/prospectus_full.pdf")
print("=== 2025.HK Income (p340), BS (p342), CF (p345) ===")
print(get_text_range(doc, 339, 346))
doc.close()

# 5. 3738.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_3738_HK/prospectus_full.pdf")
print("=== 3738.HK Income (p259), BS (p261), CF (p264) ===")
print(get_text_range(doc, 258, 265))
doc.close()

# 6. 6119.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_6119_HK/prospectus_full.pdf")
print("=== 6119.HK Income (p290), BS (p292), CF (p296) ===")
print(get_text_range(doc, 290, 297))
doc.close()

# 7. 8447.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_8447_HK/pros_sec_accountants_report_E129.pdf")
print("=== 8447.HK Income (p5), BS (p6), CF (p8) ===")
print(get_text_range(doc, 5, 8))
doc.close()

# 8. 8516.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_8516_HK/prospectus_full.pdf")
print("=== 8516.HK Income (p306), BS (p307), CF (p308) ===")
print(get_text_range(doc, 306, 309))
doc.close()

# 9. 8645.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_8645_HK/prospectus_full.pdf")
print("=== 8645.HK Income (p331), BS (p333), CF (p336) ===")
print(get_text_range(doc, 331, 337))
doc.close()

# 10. 9988.HK
doc = pymupdf.open("analysis/out/pilot_48_raw_docs/1_9988_HK/pros_sec_accountants_report_2019111500075.pdf")
print("=== 9988.HK Income (p5), BS (p7), CF (p16) ===")
print(get_text_range(doc, 5, 9))
print(get_text_range(doc, 16, 17))
doc.close()

