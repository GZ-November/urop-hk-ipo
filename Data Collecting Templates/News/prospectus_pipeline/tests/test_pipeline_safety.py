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

from contracts import evidence_issues, is_company_level_statement, validate_record  # noqa: E402
from pdfprep import locate_sections  # noqa: E402
from state import authorized, save_record  # noqa: E402
from storage import official_files  # noqa: E402
from tools import search as tools_search  # noqa: E402
from cornerstone import assess  # noqa: E402


class PipelineSafetyTests(unittest.TestCase):
    def test_company_level_statement_detector(self):
        parent_headers = [
            "STATEMENTS OF FINANCIAL POSITION OF THE COMPANY\nAs at 31 December 2024",
            "STATEMENT OF FINANCIAL POSITION - THE COMPANY\nAs at 31 December",
            "STATEMENT OF FINANCIAL POSITION (THE COMPANY)",
            "COMPANY STATEMENTS OF FINANCIAL POSITION",
            "BALANCE SHEETS OF THE COMPANY",
            "COMPANY BALANCE SHEET",
            "STATEMENT OF FINANCIAL POSITION OF THE PARENT",
            "STATEMENT OF FINANCIAL POSITION\nNon-current assets: Investments in subsidiaries",
        ]
        for text in parent_headers:
            self.assertTrue(is_company_level_statement(text), f"Failed to detect parent statement in: {text!r}")

        group_headers = [
            "CONSOLIDATED STATEMENTS OF FINANCIAL POSITION\nAs at 31 December 2024",
            "SUMMARY OF CONSOLIDATED STATEMENTS OF FINANCIAL POSITION",
            "CONSOLIDATED BALANCE SHEETS",
            "CONSOLIDATED STATEMENTS OF PROFIT OR LOSS",
            "CONSOLIDATED STATEMENTS OF CASH FLOWS",
            "SHARE CAPITAL\nAuthorised and issued share capital",
        ]
        for text in group_headers:
            self.assertFalse(is_company_level_statement(text), f"False positive detected on group statement: {text!r}")

    def test_company_level_statement_rejected_by_evidence(self):
        schema = {"fields": [{"key": "col_Y", "kind": "number", "unit": "currency"}]}
        packet_content = (
            "# Header\n"
            "<<<PAGE 10>>>\n"
            "CONSOLIDATED STATEMENTS OF FINANCIAL POSITION\n"
            "Total assets 500,000,000\n"
            "<<<PAGE 11>>>\n"
            "STATEMENTS OF FINANCIAL POSITION OF THE COMPANY\n"
            "Total assets 100,000,000\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            pkt = Path(tmp) / "test_packet.md"
            pkt.write_text(packet_content, encoding="utf-8")

            # Citing parent company statement page 11 must be rejected
            rec_parent = {"code": "0001.HK", "fields": {
                "col_Y": {"value": 100000000, "page": 11, "quote": "Total assets 100,000,000", "confidence": "high"}
            }}
            issues = evidence_issues(rec_parent, pkt, schema)
            self.assertTrue(any("from company-level (parent) statement" in iss for iss in issues),
                            f"Expected parent statement rejection, got: {issues}")

            # Citing consolidated statement page 10 must pass
            rec_group = {"code": "0001.HK", "fields": {
                "col_Y": {"value": 500000000, "page": 10, "quote": "Total assets 500,000,000", "confidence": "high"}
            }}
            issues_group = evidence_issues(rec_group, pkt, schema)
            self.assertEqual(issues_group, [])

    def test_locate_sections_excludes_company_level_statement(self):
        mock_pages = [{"page": i, "text": f"Page {i}"} for i in range(1, 15)]
        mock_pages[0] = {"page": 1, "text": "COVER PAGE"}
        mock_pages[9] = {"page": 10, "text": "CONSOLIDATED STATEMENTS OF FINANCIAL POSITION\nAs at 31 Dec"}
        mock_pages[10] = {"page": 11, "text": "CONSOLIDATED STATEMENTS OF FINANCIAL POSITION (CONTINUED)\nEquity..."}
        mock_pages[11] = {"page": 12, "text": "STATEMENTS OF FINANCIAL POSITION OF THE COMPANY\nNon-current assets"}
        mock_pages[12] = {"page": 13, "text": "STATEMENTS OF FINANCIAL POSITION OF THE COMPANY (CONTINUED)"}
        mock_pages[13] = {"page": 14, "text": "NOTES TO THE FINANCIAL STATEMENTS"}
        cfg = {
            "extract": {"cover_pages": 1, "max_runs_per_anchor": 1},
            "paths": {"text": Path("/nonexistent")},
        }
        with patch("pdfprep._pages", return_value=mock_pages):
            loc = locate_sections(cfg, "0001.HK")
            fin_pages = loc.get("financials", [])
            self.assertIn(10, fin_pages)
            self.assertIn(11, fin_pages)
            self.assertNotIn(12, fin_pages)
            self.assertNotIn(13, fin_pages)

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
