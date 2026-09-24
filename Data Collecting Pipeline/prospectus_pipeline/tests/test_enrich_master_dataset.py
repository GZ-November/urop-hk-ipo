import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from tools.enrich_master_dataset import ACADEMIC_FIELDS, academic_header_issues  # noqa: E402


class AcademicHeaderValidationTests(unittest.TestCase):
    def test_all_academic_fields_can_live_in_any_workbook_width(self):
        headers = ["existing field"] * 205 + [field["header"] for field in ACADEMIC_FIELDS]
        self.assertEqual(academic_header_issues(headers), [])

    def test_missing_or_duplicated_academic_header_fails_closed(self):
        headers = [field["header"] for field in ACADEMIC_FIELDS]
        headers.remove(ACADEMIC_FIELDS[0]["header"])
        headers.append(ACADEMIC_FIELDS[1]["header"])
        issues = academic_header_issues(headers)
        self.assertEqual(len(issues), 2)
        self.assertIn(ACADEMIC_FIELDS[0]["key"], issues[0])
        self.assertIn(ACADEMIC_FIELDS[1]["key"], issues[1])


if __name__ == "__main__":
    unittest.main()
