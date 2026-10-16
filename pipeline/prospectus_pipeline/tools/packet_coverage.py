#!/usr/bin/env python3
"""Check that the deduplicated packet layout keeps every page the stored payloads cite.

For each stored payload the script rebuilds the page selection from the page-level text, compares it
with the pages of the previous per-group layout (and with an existing packet file when --old-packets
is given), and reports packet size before and after. Exit status 1 when a page that was in the old
packet, or that a payload cites and the old layout carried, is missing from the new packet.

  python3 tools/packet_coverage.py --config config_2026q1.yaml --text-dir data/text \
      --payloads out/extracted [--old-packets data/packets] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import yaml  # noqa: E402
import pdfprep  # noqa: E402

PAGE_MARK = re.compile(r"<<<PAGE\s+(\d+)>>>")


def old_layout_chars(page_text: dict[int, str], kept: dict[str, list[int]]) -> int:
    """Size of the per-group layout: every group repeats the pages it shares with others."""
    return sum(len(pdfprep.render_pages(page_text, pgs)) for pgs in kept.values())


def measure(cfg: dict, payload: Path, old_packets: Path | None) -> dict:
    record = json.loads(payload.read_text(encoding="utf-8"))
    code = record["code"]
    loc = pdfprep.locate_sections(cfg, code)
    kept, _ = pdfprep.select_pages(cfg, code, loc)
    page_text = {p["page"]: p["text"] for p in pdfprep._pages(cfg, code)}
    new_pages = {pg for pgs in kept.values() for pg in pgs}
    old_pages = new_pages
    if old_packets is not None:
        old_file = old_packets / f"{pdfprep._safe_name(code)}.md"
        if old_file.exists():
            old_pages = {int(x) for x in PAGE_MARK.findall(old_file.read_text(encoding="utf-8"))}
    cited = {k: e["page"] for k, e in record.get("fields", {}).items()
             if isinstance(e, dict) and isinstance(e.get("page"), int)}
    return {
        "code": code,
        "old_chars": old_layout_chars(page_text, kept),
        "new_chars": len(pdfprep.render_pages(page_text, sorted(new_pages))),
        "cited": len(cited),
        "cited_in_old": sum(1 for p in cited.values() if p in old_pages),
        "cited_in_new": sum(1 for p in cited.values() if p in new_pages),
        "lost_pages": sorted(old_pages - new_pages),
        "lost_cites": sorted(k for k, p in cited.items() if p in old_pages and p not in new_pages),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, help="cohort YAML (its extract: section sets the caps)")
    ap.add_argument("--text-dir", required=True, type=Path, help="page-level text jsonl directory")
    ap.add_argument("--payloads", required=True, type=Path, help="directory of stored extraction payloads")
    ap.add_argument("--old-packets", type=Path, help="existing packet directory to compare page sets with")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)
    # Older cohort configs omit some extract keys (cover_pages); take them from config.yaml.
    base = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8")).get("extract", {})
    cohort = yaml.safe_load(Path(args.config).read_text(encoding="utf-8")).get("extract", {})
    cfg = {"extract": {**base, **cohort}, "paths": {"text": args.text_dir}}
    rows = []
    for payload in sorted(args.payloads.glob("*.json")):
        if args.limit and len(rows) >= args.limit:
            break
        code = json.loads(payload.read_text(encoding="utf-8")).get("code", "")
        if not (args.text_dir / f"{pdfprep._safe_name(code)}.jsonl").exists():
            continue
        rows.append(measure(cfg, payload, args.old_packets))
    if not rows:
        print("no payloads with page text found")
        return 1
    old = sum(r["old_chars"] for r in rows)
    new = sum(r["new_chars"] for r in rows)
    bad = [r for r in rows if r["lost_pages"] or r["lost_cites"]]
    print(f"issuers {len(rows)}  mean old {old // len(rows):,} chars  mean new {new // len(rows):,} chars  "
          f"({100 * (1 - new / old):.1f}% smaller)")
    print(f"cited pages carried: old {sum(r['cited_in_old'] for r in rows)}  new {sum(r['cited_in_new'] for r in rows)}"
          f"  of {sum(r['cited'] for r in rows)} cited")
    for r in bad:
        print(f"LOST {r['code']}: pages {r['lost_pages'][:10]} cites {r['lost_cites'][:10]}")
    print("OK: no page that the old packet carried is missing" if not bad else f"FAIL: {len(bad)} issuer(s) lost pages")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
