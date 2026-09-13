import unittest
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

from codebook import build_codebook, export_clean_csv, export_all


class CodebookTests(unittest.TestCase):
    def test_build_codebook_full_coverage(self):
        variables, summary = build_codebook()
        self.assertEqual(summary["sample_size"], 38)
        self.assertEqual(summary["variable_count"], 120)
        self.assertEqual(summary["tiers"]["green_hkex"], 11)
        self.assertEqual(summary["tiers"]["blue_prospectus"], 60)
        self.assertEqual(summary["tiers"]["darkblue_external"], 49)
        self.assertEqual(len(variables), 120)

    def test_clean_csv_export(self):
        variables, summary = build_codebook()
        csv_path = export_clean_csv(variables)
        self.assertTrue(csv_path.exists())

        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = list(csv.reader(f))
            self.assertEqual(len(reader), 39)  # 1 header row + 38 data rows
            self.assertEqual(len(reader[0]), 120)
            self.assertEqual(reader[0][1], "Stock Code")
            # Stock codes should all end with .HK
            stock_codes = [row[1] for row in reader[1:]]
            self.assertEqual(len(stock_codes), 38)
            self.assertTrue(all(code.endswith(".HK") for code in stock_codes))

    def test_export_all_artifacts(self):
        res = export_all()
        self.assertEqual(res["variable_count"], 120)
        self.assertEqual(res["sample_size"], 38)
        self.assertTrue(Path(res["csv_path"]).exists())
        self.assertTrue(Path(res["md_path"]).exists())
        self.assertTrue(Path(res["json_path"]).exists())

        md_content = Path(res["md_path"]).read_text(encoding="utf-8")
        self.assertIn("120 维全量变量字典详细清单", md_content)
        self.assertIn("38 家", md_content)
        self.assertIn("淺綠" if "淺綠" in md_content else "浅绿", md_content)


if __name__ == "__main__":
    unittest.main()
