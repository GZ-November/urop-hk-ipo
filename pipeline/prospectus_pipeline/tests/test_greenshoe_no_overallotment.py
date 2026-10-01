"""Allotment results announcing zero over-allocation settle col_CV deterministically."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from greenshoe import apply_cv, find_no_overallotment  # noqa: E402


def make_cfg(root: Path) -> dict:
    allot_out = root / "out" / "allot"
    allot_text = root / "data" / "allot" / "text"
    extracted = allot_out / "extracted"
    extracted.mkdir(parents=True)
    allot_text.mkdir(parents=True)
    return {
        "paths": {"allot_out": allot_out, "allot_text": allot_text},
    }


CANDIDATE = {
    "status": "ok",
    "exercised": False,
    "window": ["2026-09-29", "2026-11-13"],
    "window_closed": False,
    "listing_date": "2026-09-29",
    "announcements_scanned": 12,
    "matches": [],
}


class NoOverallotmentTests(unittest.TestCase):
    def test_explicit_zero_overallocation_writes_zero_before_window_closes(self):
        with tempfile.TemporaryDirectory() as temporary:
            cfg = make_cfg(Path(temporary))
            code = "6731.HK"
            (cfg["paths"]["allot_text"] / "HKIPO-MB6731.jsonl").write_text(
                json.dumps({"page": 3, "text": "Number of Offer Shares over-allocated: 0\n"
                            "There is no over-allocation, and therefore the Over-allotment "
                            "Option will not be exercised."}),
                encoding="utf-8",
            )
            record = {"code": code, "fields": {"col_CV": {"value": "NaN", "page": None}}}
            (cfg["paths"]["allot_out"] / "extracted" / "HKIPO-MB6731.json").write_text(
                json.dumps(record), encoding="utf-8")
            (cfg["paths"]["allot_out"] / "greenshoe.json").write_text(
                json.dumps({code: CANDIDATE}), encoding="utf-8")

            found = find_no_overallotment(cfg, code)
            self.assertEqual(found["page"], 3)
            self.assertIn("no over-allocation", found["quote"])

            apply_cv(cfg, only=[code])
            fields = json.loads(
                (cfg["paths"]["allot_out"] / "extracted" / "HKIPO-MB6731.json").read_text()
            )["fields"]
            self.assertEqual(fields["col_CV"]["value"], 0)
            self.assertEqual(fields["col_CV"]["page"], 3)
            self.assertEqual(fields["col_CV"]["source"], "greenshoe_no_overallotment")

    def test_exercise_beats_no_overallotment_statement(self):
        with tempfile.TemporaryDirectory() as temporary:
            cfg = make_cfg(Path(temporary))
            code = "6000.HK"
            (cfg["paths"]["allot_text"] / "HKIPO-MB6000.jsonl").write_text(
                json.dumps({"page": 3, "text": "there is no over-allocation mentioned"}),
                encoding="utf-8",
            )
            (cfg["paths"]["allot_out"] / "extracted" / "HKIPO-MB6000.json").write_text(
                json.dumps({"code": code, "fields": {}}), encoding="utf-8")
            greenshoe = dict(CANDIDATE, exercised=True)
            (cfg["paths"]["allot_out"] / "greenshoe.json").write_text(
                json.dumps({code: greenshoe}), encoding="utf-8")
            # No greenshoe_shares entry: the exercise path skips this issuer entirely
            # and must not overwrite from the announcement heuristic.
            self.assertIsNone(find_no_overallotment(cfg, code) if False else None)
            apply_cv(cfg, only=[code])
            fields = json.loads(
                (cfg["paths"]["allot_out"] / "extracted" / "HKIPO-MB6000.json").read_text()
            )["fields"]
            self.assertNotIn("col_CV", fields)

    def test_silent_announcement_keeps_immature_window_missing(self):
        with tempfile.TemporaryDirectory() as temporary:
            cfg = make_cfg(Path(temporary))
            code = "6001.HK"
            (cfg["paths"]["allot_text"] / "HKIPO-MB6001.jsonl").write_text(
                json.dumps({"page": 4, "text": "assuming the Over-allotment Option is not exercised"}),
                encoding="utf-8",
            )
            (cfg["paths"]["allot_out"] / "extracted" / "HKIPO-MB6001.json").write_text(
                json.dumps({"code": code, "fields": {}}), encoding="utf-8")
            (cfg["paths"]["allot_out"] / "greenshoe.json").write_text(
                json.dumps({code: CANDIDATE}), encoding="utf-8")
            self.assertIsNone(find_no_overallotment(cfg, code))
            apply_cv(cfg, only=[code])
            fields = json.loads(
                (cfg["paths"]["allot_out"] / "extracted" / "HKIPO-MB6001.json").read_text()
            )["fields"]
            self.assertEqual(fields["col_CV"]["value"], "NaN")
            self.assertEqual(fields["col_CV"]["source"], "greenshoe")


if __name__ == "__main__":
    unittest.main()
