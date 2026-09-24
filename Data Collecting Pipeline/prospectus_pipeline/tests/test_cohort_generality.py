import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from market_panel import load_issuers  # noqa: E402


class ConfiguredCohortTests(unittest.TestCase):
    def test_market_issuer_loader_uses_configured_columns_and_data_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "cohort.xlsx"
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Listings"
            ws.append(["unused", "unused", "Ticker", "Issuer", "Prospectus", "Listing", "IPO Subscription Price (HK$)"])
            ws.append([None] * 7)  # data starts after a cohort-specific note row
            ws.append([None, None, "6656", "Issuer A", dt.date(2026, 5, 1),
                       dt.date(2026, 6, 1), 42.5])
            wb.save(book)
            wb.close()

            cfg = {
                "workbook": book.name,
                "_ws": Path(tmp),
                "sheet": "Listings",
                "data_start_row": 3,
                "id_columns": {
                    "stock_code": "C", "name": "D", "prospectus_date": "E", "listing_date": "F"
                },
            }
            issuers = load_issuers(book, use_master_cache=False, cfg=cfg)

        self.assertEqual(len(issuers), 1)
        self.assertEqual(issuers[0]["stock_code"], "6656.HK")
        self.assertEqual(issuers[0]["company_name"], "Issuer A")
        self.assertEqual(issuers[0]["row_idx"], 3)
        self.assertEqual(issuers[0]["offer_price_hkd"], 42.5)


if __name__ == "__main__":
    unittest.main()
