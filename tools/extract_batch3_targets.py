#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path
import pymupdf

RAW_DOCS = Path("analysis/out/pilot_48_raw_docs")
COMPANIES = [
    ("3_0249_HK", "0249.HK", "Harbin Brewery Group Ltd"),
    ("3_0483_HK", "0483.HK", "Bauhaus International (Holdings) Ltd"),
    ("3_0587_HK", "0587.HK", "Hua Han Bio-Pharmaceutical Holdings Ltd"),
    ("3_0612_HK", "0612.HK", "China Investment Fund Co Ltd"),
    ("3_0700_HK", "0700.HK", "Tencent Holdings Ltd"),
    ("3_0939_HK", "0939.HK", "China Construction Bank Corporation"),
    ("3_0999_HK", "0999.HK", "I.T Limited"),
    ("3_1126_HK", "1126.HK", "Dream International Ltd"),
    ("3_2628_HK", "2628.HK", "China Life Insurance Company Ltd"),
    ("3_8077_HK", "8077.HK", "Infoserve Technology Corp"),
    ("3_8159_HK", "8159.HK", "Glory Mark Hi-Tech (Holdings) Ltd"),
    ("3_8160_HK", "8160.HK", "MediaNation Inc."),
]

def get_text_from_doc(doc_path):
    if doc_path.suffix == ".pdf":
        doc = pymupdf.open(doc_path)
        pages = []
        for pno in range(len(doc)):
            page = doc[pno]
            t = page.get_text()
            pages.append((pno + 1, t))
        return pages
    elif doc_path.suffix in [".htm", ".html"]:
        text = doc_path.read_text(errors="ignore")
        # remove tags
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return [(1, text)]
    elif doc_path.suffix == ".doc":
        out = subprocess.run(["strings", "-n", "4", str(doc_path)], capture_output=True, text=True)
        return [(1, out.stdout)]
    return []

def main():
    out_file = Path("/tmp/batch3_full_targets.txt")
    with open(out_file, "w", encoding="utf-8") as out:
        for folder_name, code, name in COMPANIES:
            folder = RAW_DOCS / folder_name
            out.write(f"\n{'='*80}\n")
            out.write(f"ISSUER: {code} | {name} | FOLDER: {folder_name}\n")
            out.write(f"{'='*80}\n\n")

            if not folder.exists():
                out.write(f"FOLDER NOT FOUND: {folder}\n")
                continue

            for f in sorted(folder.glob("*")):
                if f.name.startswith("."):
                    continue
                pages = get_text_from_doc(f)
                out.write(f"--- FILE: {f.name} (Total Pages/Sections: {len(pages)}) ---\n")
                for pno, text in pages:
                    # filter relevant pages or print summary
                    # For financial reports or accountants report or allotment, keep full text or targeted keywords
                    is_relevant = False
                    lower_t = text.lower()
                    keywords = [
                        "offer price", "maximum offer price", "valid applications", "clawback", 
                        "reallocation", "cornerstone", "corporate investor", "underwriting commission",
                        "listing expenses", "incorporated in", "principal place of business",
                        "headquarters", "founded", "commenced operations", "established",
                        "controlling shareholder", "turnover", "revenue", "net interest income",
                        "profit before tax", "profit for the year", "profit attributable to",
                        "total assets", "total equity", "net assets", "total liabilities",
                        "operating activities", "cash flows from operating activities"
                    ]
                    # If file is allotment announcement, keep all pages!
                    if "allot" in f.name.lower() or "notice" in f.name.lower():
                        is_relevant = True
                    elif any(k in lower_t for k in keywords):
                        is_relevant = True
                    
                    if is_relevant:
                        out.write(f"[PAGE {pno}]\n")
                        # write clean text
                        lines = [l.strip() for l in text.splitlines() if l.strip()]
                        out.write("\n".join(lines) + "\n\n")

    print(f"Extraction complete! Written to {out_file} ({out_file.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
