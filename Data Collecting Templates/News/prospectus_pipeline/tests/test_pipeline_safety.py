import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from contracts import validate_record  # noqa: E402
from state import authorized, save_record  # noqa: E402
from storage import official_files  # noqa: E402
from tools import search as tools_search  # noqa: E402
from cornerstone import assess  # noqa: E402


class PipelineSafetyTests(unittest.TestCase):
    def test_fake_derived_source_cannot_bypass_evidence(self):
        schema = {"fields": [{"key": "col_AR", "kind": "text", "unit": "text"}]}
        record = {"code": "0001.HK", "fields": {"col_AR": {
            "value": "invented", "page": None, "quote": "invented",
            "confidence": "high", "source": "da_formula"}}}
        errors = validate_record(record, schema, "0001.HK", "prospectus", {})
        self.assertTrue(any("derived source" in error for error in errors))
        self.assertTrue(any("requires page" in error for error in errors))

    def test_decimal_schema_has_default_zero_to_one_range(self):
        schema = {"fields": [{"key": "col_AY", "kind": "number", "unit": "decimal"}]}
        record = {"code": "0001.HK", "fields": {"col_AY": {
            "value": 1.5, "page": 1, "quote": "one hundred and fifty percent",
            "confidence": "high"}}}
        errors = validate_record(record, schema, "0001.HK")
        self.assertTrue(any("outside schema range" in error for error in errors))

    def test_periods_keeps_full_date(self):
        page = {"page": 1, "text": ("CONSOLIDATED STATEMENT OF CASH FLOWS\n"
                                    "nine months ended 30 September 2025")}
        with patch.object(tools_search, "load", return_value=[page]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                tools_search.cmd_periods(type("Args", (), {"code": "0001.HK"})())
        self.assertIn("col_AT = 30/09/25", output.getvalue())

    def test_backup_json_is_not_an_official_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "HKIPO-MB0001.json").write_text("{}")
            (directory / "HKIPO-MB0001.backup-before-fix-20260913.json").write_text("{}")
            self.assertEqual(list(official_files(directory)), ["0001.HK"])

    def test_stale_hash_cannot_be_authorized(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {"_root": Path(tmp)}
            current = {"code": "0001.HK", "target": "prospectus", "hash": "new",
                       "status": "pass", "errors": []}
            for stage in ("extracted", "validated", "reviewed"):
                save_record(cfg, "prospectus", "0001.HK", stage,
                            {**current, "hash": "old", "gate_pass": True})
            with self.assertRaises(ValueError):
                authorized(cfg, "0001.HK", "prospectus", current)

    def test_incidental_announcement_mention_is_not_presence(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            prospectus, allot = base / "prospectus", base / "allot"
            prospectus.mkdir()
            allot.mkdir()
            name = "HKIPO-MB0001.jsonl"
            (prospectus / name).write_text(
                json.dumps({"page": 1, "text": "No relevant section"}) + "\n")
            (allot / name).write_text(json.dumps({
                "page": 1,
                "text": "A connected client may participate as a placee or cornerstone investor."
            }) + "\n")
            result = assess({"paths": {"text": prospectus, "allot_text": allot}}, "0001.HK")
            self.assertEqual(result["verdict"], "absent")
            self.assertTrue(result["evidence_complete"])


if __name__ == "__main__":
    unittest.main()
