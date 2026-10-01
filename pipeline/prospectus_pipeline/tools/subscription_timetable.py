#!/usr/bin/env python3
"""Extract each issuer's application-list open/close wording from its prospectus page text.

The exchange timetable is stated in the prospectus: lists open at a stated time on the last day and
close at 12:00 noon on that day ("... noon on the last day for submitting applications, when the
application lists close"). A time is recorded only when the wording was found; otherwise it stays
unknown. Output: data/manual/subscription_timetables.json (evidence page + verbatim snippet).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = ROOT / "data" / "text"
OUT = ROOT / "data" / "manual" / "subscription_timetables.json"
OPEN = re.compile(r"Application lists?(?: of the Hong Kong Public Offering)? open ?(?:\(\w+ ?\d?\))?[ .]*"
                  r"(\d{1,2}: ?\d{2} ?[ap]\.m\.) on ([A-Za-z]+day,? [^.]{6,30}?\d{4})", re.I)
CLOSE = re.compile(r"noon on the last day for submitting applications, when the application lists close", re.I)


def extract(code: str):
    digits = code.split(".")[0]
    path = TEXT / f"HKIPO-MB{digits}.jsonl"
    if not path.exists():
        return {"status": "no_local_text"}
    opened = closed = None
    for line in path.open(encoding="utf-8"):
        page = json.loads(line)
        if page["page"] > 40:
            break
        flat = re.sub(r"\s+", " ", page["text"])
        if opened is None and (m := OPEN.search(flat)):
            opened = {"page": page["page"], "open_time_hkt": m.group(1).replace(": ", ":").replace(" ", " "),
                      "open_day_wording": m.group(2).strip(), "snippet": flat[m.start():m.end()][:200]}
        if closed is None and (m := CLOSE.search(flat)):
            closed = {"page": page["page"], "snippet": flat[max(0, m.start() - 40):m.end()][:200]}
        if opened and closed:
            break
    return {"status": "found" if opened and closed else "partial",
            "application_lists_open": opened,
            "close_time_hkt": "12:00" if closed else None, "close_evidence": closed}


def main(argv):
    import csv
    master = ROOT.parent / "exports" / "HKIPO-MB-MASTER_clean.csv"
    with master.open(encoding="utf-8-sig") as fh:
        codes = [r["Stock Code"] for r in csv.DictReader(fh) if r["Date of Listing (dd/mm/yy)"].startswith("2026")]
    result = {code: extract(code) for code in codes}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    found = sum(1 for v in result.values() if v["status"] == "found")
    print(f"timetables: {found}/{len(result)} with both open and 12:00 noon close wording -> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1:])
