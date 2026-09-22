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

from contracts import (  # noqa: E402
    evidence_issues, is_company_level_statement, is_definitions_page, validate_record
)
from pdfprep import locate_sections  # noqa: E402
from state import CONTRACT_VERSION, authorized, save_record  # noqa: E402
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

    def test_old_contract_cannot_be_authorized(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {"_root": Path(tmp)}
            current = {"code": "0001.HK", "target": "prospectus", "hash": "same",
                       "status": "pass", "errors": []}
            for stage in ("extracted", "validated", "reviewed"):
                save_record(cfg, "prospectus", "0001.HK", stage,
                            {**current, "gate_pass": True})
                path = Path(tmp) / ".pipeline_state" / "prospectus" / stage / "0001.HK.json"
                record = json.loads(path.read_text())
                record["contract_version"] = "obsolete-contract"
                path.write_text(json.dumps(record), encoding="utf-8")
            self.assertNotEqual(CONTRACT_VERSION, "obsolete-contract")
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

    def test_definitions_page_detector(self):
        definitions_texts = [
            "“Company”\nOur company...\nDEFINITIONS\n– 17 –",
            "DEFINITIONS AND GLOSSARY\n“Listing Rules”\nthe Rules Governing...",
            "释义\n“本公司”\n指红星冷链...",
        ]
        for txt in definitions_texts:
            self.assertTrue(is_definitions_page(txt), f"Expected True for definitions text: {txt!r}")

        normal_texts = [
            "HISTORY, DEVELOPMENT AND CORPORATE STRUCTURE\nOur history can be traced back to 2006",
            "STATUTORY AND GENERAL INFORMATION\n1. Incorporation\nThe predecessor of our Company was incorporated...",
            "ACCOUNTANTS' REPORT\n1. CORPORATE INFORMATION\nHongxing Coldchain was incorporated...",
        ]
        for txt in normal_texts:
            self.assertFalse(is_definitions_page(txt), f"Expected False for normal text: {txt!r}")

    def test_definitions_page_rejected_for_col_BP(self):
        schema = {"fields": [{"key": "col_BP", "kind": "date", "unit": "date"}]}
        packet_content = (
            "# Test Packet\n"
            "<<<PAGE 26>>>\n"
            "“Company”\npredecessor was established on August 30, 2006\nDEFINITIONS\n– 17 –\n"
            "<<<PAGE 346>>>\n"
            "STATUTORY AND GENERAL INFORMATION\n"
            "1. Incorporation\n"
            "predecessor was incorporated under the laws of the PRC on October 16, 2006\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            pkt = Path(tmp) / "test_packet.md"
            pkt.write_text(packet_content, encoding="utf-8")

            # Citing definitions page 26 must be rejected
            rec_def = {"code": "0001.HK", "fields": {
                "col_BP": {"value": "30/08/06", "page": 26, "quote": "predecessor was established on August 30, 2006", "confidence": "medium"}
            }}
            issues = evidence_issues(rec_def, pkt, schema)
            self.assertTrue(any("from DEFINITIONS section" in iss for iss in issues),
                            f"Expected definitions rejection, got: {issues}")

            # Citing statutory page 346 must pass
            rec_stat = {"code": "0001.HK", "fields": {
                "col_BP": {"value": "16/10/06", "page": 346, "quote": "predecessor was incorporated under the laws of the PRC on October 16, 2006", "confidence": "high"}
            }}
            issues_stat = evidence_issues(rec_stat, pkt, schema)
            self.assertEqual(issues_stat, [])

    def test_gross_margin_ceiling_rejects_full_year_gp_in_stub(self):
        from validate import check_firm
        schema = {"fields": []}
        # col_AH annualized = 236,096,000, 6M unannualized = 118,048,000
        # If col_CF is 123,379,000 (full year), gross margin is 104.5% -> MUST REJECT
        rec_err = {
            "code": "1641.HK",
            "fields": {
                "col_AT": {"value": "30/06/2025"},
                "col_AH": {"value": 236096000},
                "col_CF": {"value": 123379000},
                "col_V": {"value": "RMB"},
            }
        }
        issues = check_firm(rec_err, schema)
        self.assertTrue(any("毛利率超限/期间错位" in iss["check"] for iss in issues),
                        f"Expected gross margin ceiling rejection, got: {issues}")

        # Correct 6M gross profit = 62,861,000 (margin 53.3%) -> MUST PASS
        rec_ok = {
            "code": "1641.HK",
            "fields": {
                "col_AT": {"value": "30/06/2025"},
                "col_AH": {"value": 236096000},
                "col_CF": {"value": 62861000},
                "col_V": {"value": "RMB"},
            }
        }
        issues_ok = [i for i in check_firm(rec_ok, schema) if "毛利" in i["check"]]
        self.assertEqual(issues_ok, [])

    def test_monetary_scale_guard_rejects_unscaled_thousands(self):
        from validate import check_firm
        schema = {"fields": []}
        # Issuer with > 50M assets, values entered in thousands without x1000
        rec_unscaled = {
            "code": "2726.HK",
            "fields": {
                "col_AT": {"value": "30/09/25"},
                "col_V": {"value": "RMB"},
                "col_Y": {"value": 4366624000},
                "col_AH": {"value": 713417333},
                "col_CF": {"value": 137081},
                "col_CG": {"value": 69800},
                "col_BE": {"value": 65025},
            }
        }
        issues = check_firm(rec_unscaled, schema)
        checks = [i["check"] for i in issues]
        self.assertTrue(any("金额单位未折算 (毛利)" in c or "毛利数值数量级异常" in c for c in checks))
        self.assertTrue(any("金额单位未折算 (资本开支)" in c for c in checks))
        self.assertTrue(any("金额单位未折算 (有息负债)" in c for c in checks))

        # Properly scaled values -> MUST PASS
        rec_scaled = {
            "code": "2726.HK",
            "fields": {
                "col_AT": {"value": "30/09/25"},
                "col_V": {"value": "RMB"},
                "col_Y": {"value": 4366624000},
                "col_AH": {"value": 713417333},
                "col_CF": {"value": 137081000},
                "col_CG": {"value": 69806000},
                "col_BE": {"value": 769604000},
            }
        }
        scale_issues = [i for i in check_firm(rec_scaled, schema) if "折算" in i["check"] or "毛利" in i["check"]]
        self.assertEqual(scale_issues, [])


if __name__ == "__main__":
    unittest.main()
