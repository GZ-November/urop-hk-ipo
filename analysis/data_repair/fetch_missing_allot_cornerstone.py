#!/usr/bin/env python3
"""Fetch full HKEX allotment announcement PDFs/sections for confirmed-CS IPOs lacking full cornerstone details."""
from __future__ import annotations

import glob
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from download_historical_financial_sections import fetch, links

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "analysis/out/subscription_cornerstone_repair"
PDF_DIR = OUT_DIR / "allot_pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)
CS_PAT = re.compile(r"corner\s*stone|corporate\s+investor", re.I)
SKIP_LINK = re.compile(r"identification\s+doc|passport|hksar|identity\s+card|ccass|white\s+form|yellow\s+form|pink\s+form|blue\s+form|green\s+form", re.I)


def get_source_url(key: str) -> str:
    fs = glob.glob(str(ROOT / f"analysis/out/batch*_*_packets/{key}.md"))
    if not fs:
        return ""
    txt = Path(fs[0]).read_text(errors="ignore")
    sec2 = txt.split("## Section 2")[1].split("## Section 3")[0] if "## Section 2" in txt else ""
    m = re.search(r"\*\*Source URL\*\*:\s*(\S+)", sec2)
    return m.group(1) if m else ""


def scan_pdf_bytes(pdf_path: Path, data: bytes | None = None) -> tuple[int, list[int], str]:
    if data is not None and not pdf_path.exists():
        pdf_path.write_bytes(data)
    with fitz.open(pdf_path) as doc:
        snippets = []
        cs_pages = []
        for idx, pg in enumerate(doc):
            t = pg.get_text("text")
            if CS_PAT.search(t):
                cs_pages.append(idx + 1)
                snippets.append(f"=== PAGE {idx + 1} ===\n{t}")
                if idx + 1 < doc.page_count and len(snippets) <= 6:
                    nt = doc[idx + 1].get_text("text")
                    if not CS_PAT.search(nt):
                        snippets.append(f"=== PAGE {idx + 2} (CONT) ===\n{nt}")
        return doc.page_count, cs_pages, "\n".join(snippets)


def process_one(row: dict) -> dict:
    key = row["key"]
    url = get_source_url(key)
    rec = {"key": key, "url": url, "pages": 0, "cs_pages": [], "text": "", "err": ""}
    if not url:
        rec["err"] = "no_url"
        return rec
    try:
        if url.lower().endswith((".htm", ".html")):
            html = fetch(url).decode("utf8", "ignore")
            ls = links(html, url)
            # Filter out identification-number lists; prioritize Summary / Cornerstone / Result / Despatch / Cover
            cand_links = [(u, lbl) for u, lbl in ls if u.lower().endswith(".pdf") and not SKIP_LINK.search(lbl)]
            if not cand_links:
                cand_links = [(u, lbl) for u, lbl in ls[:5] if u.lower().endswith(".pdf")]
            # Put Summary / Cornerstone / Placing first
            cand_links.sort(key=lambda x: (0 if re.search(r"summary|corner|placing|result", x[1], re.I) else 1))
            all_snips = []
            for idx, (u, lbl) in enumerate(cand_links[:6]):
                p = PDF_DIR / f"{key}_part{idx+1}.pdf"
                if not p.exists():
                    data = fetch(u)
                    time.sleep(0.08)
                    if not data.startswith(b"%PDF"):
                        continue
                    p.write_bytes(data)
                pgs, cp, txt = scan_pdf_bytes(p)
                rec["pages"] += pgs
                if cp:
                    rec["cs_pages"].extend(cp)
                    all_snips.append(f"[{lbl}]\n{txt}")
            rec["text"] = "\n".join(all_snips)[:20000]
        else:
            p = PDF_DIR / f"{key}.pdf"
            if not p.exists():
                data = fetch(url)
                time.sleep(0.08)
                if not data.startswith(b"%PDF"):
                    rec["err"] = "not_pdf"
                    return rec
                p.write_bytes(data)
            pgs, cp, txt = scan_pdf_bytes(p)
            rec["pages"] = pgs
            rec["cs_pages"] = cp
            rec["text"] = txt[:20000]
    except Exception as e:
        rec["err"] = str(e)[:120]
    return rec


def main():
    df = pd.read_csv(OUT_DIR / "parsed_cornerstone_pct.csv")
    need = df[df["status"].isin(["no_cs_in_sec2", "unparsed", "explicit_pct_only", "out_of_range"])].to_dict("records")
    print(f"Fetching full allotment PDFs/sections for {len(need)} issuers...")
    with ThreadPoolExecutor(6) as ex, open(OUT_DIR / "allot_extra_sec2.jsonl", "w") as f:
        ok_cs = 0
        for rec in ex.map(process_one, need):
            if rec["cs_pages"]:
                ok_cs += 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Done. Found cornerstone pages in {ok_cs} / {len(need)} allotment announcements.")


if __name__ == "__main__":
    main()
