import importlib.util
import unittest
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("blank_stats", ROOT / "tools" / "blank_immature_window_stats.py")
blank_stats = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(blank_stats)


class ImmatureWindowStatsTests(unittest.TestCase):
    def sheet(self, rows):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append([blank_stats.MATURITY_HEADER, *blank_stats.STAT_HEADERS])
        for row in rows:
            ws.append(row)
        return ws

    def test_only_rows_without_a_six_month_return_are_selected(self):
        ws = self.sheet([[0.2, 1, 2, 3, 4], [None, 1, 2, None, 4], [None, None, None, None, None]])
        cells = blank_stats.immature_cells(ws)
        self.assertEqual(cells, [(3, 2), (3, 3), (3, 5)])  # mature row 2 and the empty row 4 are untouched

    def test_missing_headers_fail_closed(self):
        wb = openpyxl.Workbook()
        wb.active.append(["something else"])
        with self.assertRaises(ValueError):
            blank_stats.immature_cells(wb.active)


if __name__ == "__main__":
    unittest.main()
