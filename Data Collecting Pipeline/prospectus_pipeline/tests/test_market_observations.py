import csv
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from market_observations import read_daily_market_panel


class MarketObservationTests(unittest.TestCase):
    def test_groups_and_sorts_daily_bars_and_normalizes_empty_returns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "daily_market_panel.csv"
            with path.open("w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(
                    stream,
                    fieldnames=["stock_code", "trade_date", "close", "turnover", "daily_return"],
                )
                writer.writeheader()
                writer.writerows([
                    {"stock_code": "1234.HK", "trade_date": "2026-01-05", "close": "12", "turnover": "120", "daily_return": "0.2"},
                    {"stock_code": "5678.HK", "trade_date": "2026-01-03", "close": "20", "turnover": "200", "daily_return": ""},
                    {"stock_code": "1234.HK", "trade_date": "2026-01-02", "close": "10", "turnover": "100", "daily_return": ""},
                ])

            daily = read_daily_market_panel(path)

        self.assertEqual(list(daily), ["1234.HK", "5678.HK"])
        self.assertEqual([bar["date"] for bar in daily["1234.HK"]], [date(2026, 1, 2), date(2026, 1, 5)])
        self.assertEqual(daily["1234.HK"][0]["daily_return"], 0.0)
        self.assertEqual(daily["5678.HK"][0]["close"], 20.0)

    def test_missing_panel_returns_empty_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(read_daily_market_panel(Path(tmp) / "missing.csv"), {})


if __name__ == "__main__":
    unittest.main()
