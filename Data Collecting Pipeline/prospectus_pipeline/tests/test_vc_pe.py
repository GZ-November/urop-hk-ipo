import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from tools import generate_vc_pe_report, vc_pe_enricher  # noqa: E402


def valid_fields():
    values = {
        "col_vc_backed": 1,
        "col_pe_backed": 0,
        "col_cvc_backed": 0,
        "col_gov_backed": 0,
        "col_top_tier_vc": 1,
        "col_pre_ipo_investors": "Example Capital",
        "col_vc_pe_stake": 0.25,
        "col_vc_board_seat": 1,
        "col_earliest_round": "Series A",
        "col_holding_duration": 3.5,
    }
    return {key: {"value": value, "page": 12, "quote": "The company received an investment.",
                  "confidence": "high"} for key, value in values.items()}


class VcPeAuditTests(unittest.TestCase):
    def audit_one(self, record):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "HKIPO-MB0001.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            packets, texts = root / "packets", root / "text"
            packets.mkdir()
            texts.mkdir()
            (packets / "HKIPO-MB0001.md").write_text(
                "<<<PAGE 12>>>\nThe company received an investment.", encoding="utf-8")
            (texts / "HKIPO-MB0001.jsonl").write_text(
                json.dumps({"page": 12, "text": "The company received an investment."}) + "\n",
                encoding="utf-8")
            cfg = {"paths": {"out": root, "packets": packets, "text": texts}}
            with patch.object(vc_pe_enricher, "read_companies",
                              return_value=[{"code": "0001.HK", "name": "Issuer"}]), \
                 patch.object(vc_pe_enricher, "official_files", return_value={"0001.HK": path}):
                return vc_pe_enricher.audit(cfg)

    def test_valid_record_is_accepted(self):
        result = self.audit_one({"code": "0001.HK", "fields": valid_fields()})[0]
        self.assertEqual(result["present"], 10)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["issues"], {})

    def test_bad_value_and_page_are_reported(self):
        fields = valid_fields()
        fields["col_vc_backed"]["value"] = 2
        fields["col_vc_backed"]["page"] = "12"
        result = self.audit_one({"code": "0001.HK", "fields": fields})[0]
        self.assertIn("expected binary 0/1", result["issues"]["col_vc_backed"])
        self.assertIn("missing prospectus page", result["issues"]["col_vc_backed"])

    def test_extraction_identity_must_match_workbook_code(self):
        result = self.audit_one({"code": "0002.HK", "fields": valid_fields()})[0]
        self.assertIn("_record", result["issues"])

    def test_quote_must_match_the_cited_page(self):
        fields = valid_fields()
        fields["col_vc_backed"]["quote"] = "A fabricated quotation with no supporting source."
        result = self.audit_one({"code": "0001.HK", "fields": fields})[0]
        self.assertIn("col_vc_backed", result["issues"])
        self.assertTrue(result["issues"]["col_vc_backed"])


class VcPeReportTests(unittest.TestCase):
    def test_missing_flags_are_excluded_from_report_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            book_path = directory / "HKIPO-MB2026Q2.xlsx"
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "NLR"
            headers = ["Stock code", "Name", *generate_vc_pe_report.FIELD_KEYS]
            ws.append(headers)
            ws.append(["0001.HK", "Issuer A", 1, 1, "NaN", 0, 0, 1, "Fund A", 0.25, 1,
                       "Series A", 2.5])
            ws.append(["0002.HK", "Issuer B", 0, "NaN", 0, 0, 0, 0, "NA", "NaN", 0,
                       "NA", "NaN"])
            wb.save(book_path)
            wb.close()
            out = directory / "out"
            out.mkdir()
            cfg = {
                "workbook": book_path.name,
                "workbook_path": book_path,
                "sheet": "NLR",
                "data_start_row": 2,
                "id_columns": {"stock_code": "A", "name": "B"},
                "dataset": {"id": "HKIPO-MB2026Q2", "cohort": "2026 Q2"},
                "paths": {"out": out},
            }
            with patch.object(generate_vc_pe_report, "load_cfg", return_value=cfg), \
                 patch.object(sys, "argv", ["generate_vc_pe_report.py"]):
                self.assertEqual(generate_vc_pe_report.main(), 0)
            report = (out / "HKIPO-MB2026Q2_VC_PE_Research_Report.md").read_text(encoding="utf-8")
            self.assertIn("2026 Q2", report)
            self.assertIn("`col_vc_backed` | 1 / 1 | 1 | 100.0%", report)
            self.assertIn("`col_pe_backed` | 0 / 1 | 1 | 0.0%", report)


if __name__ == "__main__":
    unittest.main()
