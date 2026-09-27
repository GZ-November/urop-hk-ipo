import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from expansion_mapping import EXPANSION_COLUMNS, ExpansionValueMapper


class ExpansionMappingTests(unittest.TestCase):
    def test_catalog_covers_all_41_expansion_columns(self):
        self.assertEqual(len(EXPANSION_COLUMNS), 41)
        self.assertEqual([column[0] for column in EXPANSION_COLUMNS], list(range(162, 203)))
        mapper = ExpansionValueMapper(Path("unused"))
        for column, _, expected_format, _ in EXPANSION_COLUMNS:
            self.assertEqual(mapper.value_for("missing.HK", column)[1], expected_format)

    def test_mapper_resolves_values_from_master_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_master = Path(tmp)
            with (out_master / "horizon_summary.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=["stock_code", "horizon", "bhr_from_day1", "wr_hsi"])
                writer.writeheader()
                writer.writerow({"stock_code": "1234.HK", "horizon": "Day_5", "bhr_from_day1": "0.125", "wr_hsi": "1.2"})
            with (out_master / "stabilization_events.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=["stock_code", "stabilizing_manager", "stabilization_period_end"])
                writer.writeheader()
                writer.writerow({"stock_code": "1234.HK", "stabilizing_manager": "Example Sponsor", "stabilization_period_end": "2026-02-01"})

            mapper = ExpansionValueMapper(out_master)
            mapper.load_sources()

        self.assertEqual(mapper.value_for("1234.HK", 162), ("Example Sponsor", "@"))
        self.assertEqual(mapper.value_for("1234.HK", 173), (0.125, "0.00%"))
        self.assertEqual(mapper.value_for("1234.HK", 174), (1.2, "0.000"))
        self.assertEqual(mapper.value_for("missing.HK", 173), (None, "0.00%"))


if __name__ == "__main__":
    unittest.main()
