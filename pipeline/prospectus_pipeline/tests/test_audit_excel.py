import datetime as dt
import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from audit import (
    EXTERNAL_TOOL_MAPPING,
    compare_value,
    serialize_val,
)


class AuditExcelTests(unittest.TestCase):
    def test_missing_equivalence(self):
        field_text = {"kind": "text"}
        field_num = {"kind": "number"}
        field_date = {"kind": "date"}

        # Both missing in various shapes -> diff_type is None
        self.assertEqual(compare_value(None, None, field_text)[0], None)
        self.assertEqual(compare_value("", "NA", field_text)[0], None)
        self.assertEqual(compare_value("NaN", None, field_num)[0], None)
        self.assertEqual(compare_value(None, "NaN", field_num)[0], None)
        self.assertEqual(compare_value("NA", None, field_date)[0], None)
        self.assertEqual(compare_value("na", "nan", field_num)[0], None)

    def test_diff_classification(self):
        field_text = {"kind": "text"}
        field_num = {"kind": "number"}

        # excel_missing
        diff, ex, js = compare_value(None, "Tech Inc", field_text)
        self.assertEqual(diff, "excel_missing")
        self.assertEqual(js, "Tech Inc")

        # json_missing
        diff, ex, js = compare_value(123.45, "NaN", field_num)
        self.assertEqual(diff, "json_missing")
        self.assertEqual(ex, 123.45)

        # value_mismatch
        diff, ex, js = compare_value("USD", "HKD", field_text)
        self.assertEqual(diff, "value_mismatch")
        self.assertEqual(ex, "USD")
        self.assertEqual(js, "HKD")

    def test_date_normalization(self):
        field_date = {"kind": "date"}
        d = dt.date(2026, 1, 15)
        dt_val = dt.datetime(2026, 1, 15, 0, 0)

        # datetime vs string dd/mm/yy
        diff, ex, js = compare_value(dt_val, "15/01/26", field_date)
        self.assertIsNone(diff)
        self.assertEqual(ex, "2026-01-15")
        self.assertEqual(js, "2026-01-15")

        # string YYYY-MM-DD vs dd/mm/yyyy
        diff, ex, js = compare_value("2026-01-15", "15/01/2026", field_date)
        self.assertIsNone(diff)

        # true mismatch
        diff, ex, js = compare_value("2026-01-15", "2026-01-16", field_date)
        self.assertEqual(diff, "value_mismatch")

    def test_numeric_tolerance_and_integers(self):
        field_int = {"kind": "integer"}
        field_num = {"kind": "number"}

        # Integer rounding
        diff, ex, js = compare_value(1000, 1000.0, field_int)
        self.assertIsNone(diff)

        # Float small precision epsilon
        diff, ex, js = compare_value(0.15000000001, 0.15, field_num)
        self.assertIsNone(diff)

        # Float mismatch
        diff, ex, js = compare_value(0.15, 0.20, field_num)
        self.assertEqual(diff, "value_mismatch")

    def test_external_columns_coverage(self):
        # Verify 31 external tool columns are tracked
        self.assertEqual(len(EXTERNAL_TOOL_MAPPING), 31)
        expected_cols = {"DD", "DH", "DI", "DJ", "DK", "DL", "DM", "DF", "DG", "DE",
                         "DN", "DO", "BH", "BJ", "BK", "BL", "BM", "BQ", "BN", "BO",
                         "AZ", "BS", "BU", "BV", "BW", "BX", "BY", "BZ", "CA", "CB", "CL"}
        self.assertEqual(set(EXTERNAL_TOOL_MAPPING.keys()), expected_cols)


if __name__ == "__main__":
    unittest.main()
