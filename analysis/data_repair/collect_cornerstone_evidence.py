#!/usr/bin/env python3
"""Collect prospectus evidence on whether an IPO had cornerstone investors."""
import csv, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz
sys.path.insert(0, str(Path(__file__).parent))
from download_historical_financial_sections import fetch, links

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "analysis/out/historical_financial_sources"
OUT = ROOT / "analysis/out/subscription_cornerstone_repair"
CS = re.compile(r"corner\s*stone", re.I)


def pdf_evidence(paths):
    pages = hits = toc = 0
    for p in paths:
        with fitz.open(p) as d:
            pages += d.page_count
            for i, pg in enumerate(d):
                t = pg.get_text()
                n = len(CS.findall(t))
                hits += n
                if n and i < 14 and re.search(r"contents", t[:1500], re.I) and re.search(r"corner\s*stone[^\n]{0,40}(?:\.{3,}|\s\d{2,3}\s*$)", t, re.I | re.M):
                    toc = 1
    return pages, hits, toc


def one(r):
    d = SRC / r["batch"] / r["key"]
    rec = {"key": r["key"], "format": r["format"], "url": r["url"], "source": "", "sections": 0, "section_hit": 0, "pdf_pages": 0, "pdf_hits": 0, "toc_hit": 0, "label": ""}
    try:
        if r["url"].lower().endswith((".htm", ".html")):
            ls = links(fetch(r["url"]).decode("utf8", "ignore"), r["url"])
            time.sleep(0.15)
            hit = [t for _, t in ls if CS.search(t)]
            rec.update(source="index", sections=len(ls), section_hit=int(bool(hit)), label="; ".join(hit)[:120])
        whole = sorted(list(d.glob("full.pdf")) + list(d.glob("part_*.pdf")))
        if whole and rec["sections"] < 8:
            pg, h, toc = pdf_evidence(whole)
            rec.update(source="pdf", pdf_pages=pg, pdf_hits=h, toc_hit=toc)
    except Exception as e:
        rec["source"] = "error:" + str(e)[:60]
    return rec


def main():
    rows = [r for r in csv.DictReader(open(SRC / "status.csv")) if r["url"]]
    seen = {}
    for r in rows:
        seen[r["key"]] = r
    with ThreadPoolExecutor(5) as ex, open(OUT / "cornerstone_evidence.jsonl", "w") as f:
        for i, rec in enumerate(ex.map(one, seen.values())):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(len(seen))


if __name__ == "__main__":
    main()
