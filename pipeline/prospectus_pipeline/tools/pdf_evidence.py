#!/usr/bin/env python3
"""Locate passages in an original disclosure PDF and record their evidence coordinates.

Reports the file SHA-256, the 1-based PDF page and the printed page number so an
independent reviewer can find the same passage. Text search only locates
candidates; it never assigns a field value.

    python tools/pdf_evidence.py dump  FILE.pdf OUT_DIR
    python tools/pdf_evidence.py grep  FILE.pdf "regex" [--context 300] [--max 20]
    python tools/pdf_evidence.py page  FILE.pdf PDF_PAGE
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

_PRINTED = re.compile(r"^\s*(?:[-–—]\s*)?(\d{1,4}|[ivxlcdm]{1,8})(?:\s*[-–—])?\s*$", re.I)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def printed_page(text):
    """Printed folio: a lone number/roman numeral among the first or last lines of the page."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in list(reversed(lines[-3:])) + lines[:2]:
        match = _PRINTED.match(ln)
        if match:
            return match.group(1)
    return ""


def page_texts(path):
    import pymupdf
    with pymupdf.open(str(path)) as doc:
        return [page.get_text("text") for page in doc]


def find(pages, pattern, context=300, limit=20):
    rx = re.compile(pattern, re.I)
    hits = []
    for idx, text in enumerate(pages, start=1):
        flat = re.sub(r"\s+", " ", text)
        for match in rx.finditer(flat):
            lo, hi = max(0, match.start() - context), min(len(flat), match.end() + context)
            hits.append({"pdf_page": idx, "printed_page": printed_page(text),
                         "snippet": flat[lo:hi]})
            if len(hits) >= limit:
                return hits
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    dump = sub.add_parser("dump")
    dump.add_argument("pdf")
    dump.add_argument("out")
    grep = sub.add_parser("grep")
    grep.add_argument("pdf")
    grep.add_argument("pattern")
    grep.add_argument("--context", type=int, default=300)
    grep.add_argument("--max", type=int, default=20)
    page = sub.add_parser("page")
    page.add_argument("pdf")
    page.add_argument("number", type=int)
    args = ap.parse_args(argv)

    pages = page_texts(args.pdf)
    if args.cmd == "dump":
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        index = [f"sha256\t{sha256_file(args.pdf)}", f"pdf_pages\t{len(pages)}", "pdf_page\tprinted_page"]
        for idx, text in enumerate(pages, start=1):
            (out / f"p{idx:03d}.txt").write_text(text, encoding="utf-8")
            index.append(f"{idx}\t{printed_page(text)}")
        (out / "INDEX.tsv").write_text("\n".join(index) + "\n", encoding="utf-8")
        print(f"{args.pdf}: {len(pages)} pages -> {out}")
    elif args.cmd == "grep":
        print(f"sha256 {sha256_file(args.pdf)} pages {len(pages)}")
        for hit in find(pages, args.pattern, args.context, args.max):
            print(f"[pdf p.{hit['pdf_page']} / printed {hit['printed_page'] or '?'}] {hit['snippet']}\n")
    else:
        text = pages[args.number - 1]
        print(f"[pdf p.{args.number} / printed {printed_page(text) or '?'}]\n{text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
