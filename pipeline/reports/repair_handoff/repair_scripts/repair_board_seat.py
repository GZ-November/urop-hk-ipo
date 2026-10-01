#!/usr/bin/env python3
"""Apply reviewer-approved col_vc_board_seat values to the formal Q2 extraction records.

Only values that an independent reviewer approved with verbatim, page-checked evidence are written.
Issuers the reviewer left unresolved keep the missing value ("NaN"); this script never writes 0
because a disclosure was not found. Edits are targeted text replacements so the rest of each
record keeps its original bytes and formatting. Run from the repository root.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REVIEWS = ROOT / "pipeline/reports/repair_handoff/board_seat/reviews"
EXTRACTED = ROOT / "pipeline/prospectus_pipeline/out/extracted"
TEXT = ROOT / "pipeline/prospectus_pipeline/data/text"
CONFIDENCE = {"6872": "high", "1779": "medium", "3310": "medium", "1956": "medium", "6871": "medium",
              "1392": "medium", "2493": "medium", "6915": "low", "0901": "medium"}
# Index of the reviewer-approved passage stored in the single-quote record field (default 0).
# 0901: the sponsor sentence that investors hold the same rights as public shareholders is the decisive passage.
PREFERRED = {"0901": 1}
ENTRY = re.compile(r'"col_vc_board_seat"(\s*):(\s*)\{[^{}]*\}')


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def page_text(code, page):
    with (TEXT / f"HKIPO-MB{code}.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if row["page"] == page:
                return norm(row["text"])
    raise KeyError((code, page))


def main():
    summary = {}
    for review_file in sorted(REVIEWS.glob("[0-9][0-9][0-9][0-9].json")):
        review = json.loads(review_file.read_text(encoding="utf-8"))
        code = review_file.stem
        value = review["approved_value"]
        if value is None:
            summary[code] = "unresolved: record keeps NaN"
            continue
        evidence = review["approved_evidence"]
        first = PREFERRED.get(code, 0)
        ordered = evidence[first:first + 1] + evidence[:first] + evidence[first + 1:]
        chosen = next((e for e in ordered if norm(e["quote"]) in page_text(code, e["pdf_page"])), None)
        if chosen is None:
            raise SystemExit(f"{code}: no reviewer quote verifies against the cached page text")
        entry = {"value": value, "page": chosen["pdf_page"], "quote": norm(chosen["quote"]),
                 "confidence": CONFIDENCE[code]}
        path = EXTRACTED / f"HKIPO-MB{code}.json"
        text = path.read_text(encoding="utf-8")
        match = ENTRY.search(text)
        if not match:
            raise SystemExit(f"{code}: col_vc_board_seat entry not found")
        if "\n" in match.group(0):
            base = len(text[:match.start()].rsplit("\n", 1)[-1])
            inner = " " * (base + 2)
            body = ",\n".join(f'{inner}"{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in entry.items())
            new = f'"col_vc_board_seat": {{\n{body}\n{" " * base}}}'
        else:
            new = '"col_vc_board_seat": ' + json.dumps(entry, ensure_ascii=False)
            if match.group(1) == "" and match.group(2) == "":
                new = new.replace('": {', '":{', 1).replace(", ", ",")  # keep the compact style
        path.write_text(text[:match.start()] + new + text[match.end():], encoding="utf-8")
        json.loads(path.read_text(encoding="utf-8"))
        summary[code] = f"value {value} (p.{entry['page']})"
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
