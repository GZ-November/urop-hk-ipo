import datetime as dt
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "external" / "aftermarket.py"
SPEC = importlib.util.spec_from_file_location("aftermarket", MODULE_PATH)
aftermarket = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(aftermarket)


def make_bars(start: dt.date, days: int, base: float = 10.0) -> list[dict]:
    return [
        {
            "date": start + dt.timedelta(days=i),
            "open": base + i * 0.01,
            "close": base + i * 0.01,
            "high": base + i * 0.01,
            "low": base + i * 0.01,
            "volume": 1_000 + i,
            "turnover": 10_000 + i,
        }
        for i in range(days)
    ]


class AftermarketMaturityTests(unittest.TestCase):
    def company(self, listing_date: dt.date, unlock_date=None) -> dict:
        return {
            "listing_date": listing_date,
            "offer_price": 10.0,
            "day1_close": 10.0,
            "day1_turnover": 10_000.0,
            "unlock_date": unlock_date,
            "is_18a": False,
            "is_18c": False,
            "name": "Fixture issuer",
        }

    def test_calendar_month_arithmetic_clips_month_end(self):
        self.assertEqual(
            aftermarket.add_calendar_months(dt.date(2026, 8, 31), 6),
            dt.date(2027, 2, 28),
        )

    def test_immature_six_month_window_stays_missing(self):
        listing_date = dt.date(2026, 3, 31)
        bars = make_bars(listing_date, 120)
        result = aftermarket.calculate_metrics(self.company(listing_date), bars, bars, bars)

        self.assertTrue(result["observation_meta"]["one_month_matured"])
        self.assertFalse(result["observation_meta"]["six_month_matured"])
        self.assertEqual(result["observation_meta"]["six_month_target_date"], "2026-09-30")
        for col in range(148, 157):
            self.assertIsNone(result[col])

    def test_immature_one_month_window_stays_missing(self):
        listing_date = dt.date(2026, 9, 1)
        bars = make_bars(listing_date, 10)
        result = aftermarket.calculate_metrics(self.company(listing_date), bars, bars, bars)

        self.assertFalse(result["observation_meta"]["one_month_matured"])
        for col in range(140, 148):
            self.assertIsNone(result[col])

    def test_mature_six_month_window_uses_first_bar_on_or_after_target(self):
        listing_date = dt.date(2026, 1, 31)
        bars = make_bars(listing_date, 220)
        result = aftermarket.calculate_metrics(self.company(listing_date), bars, bars, bars)

        self.assertTrue(result["observation_meta"]["six_month_matured"])
        self.assertEqual(result["observation_meta"]["six_month_target_date"], "2026-07-31")
        self.assertEqual(result["observation_meta"]["six_month_actual_date"], "2026-07-31")
        self.assertIsNotNone(result[148])
        self.assertIsNotNone(result[149])

    def test_stale_trading_is_not_silently_labelled_active(self):
        listing_date = dt.date(2026, 1, 1)
        stock_bars = make_bars(listing_date, 40)
        benchmark_bars = make_bars(listing_date, 220)
        result = aftermarket.calculate_metrics(
            self.company(listing_date), stock_bars, benchmark_bars, benchmark_bars
        )
        self.assertEqual(result[139], "No recent trading (verify status)")

    def test_verified_status_override_wins(self):
        listing_date = dt.date(2026, 1, 1)
        stock_bars = make_bars(listing_date, 40)
        benchmark_bars = make_bars(listing_date, 220)
        company = self.company(listing_date)
        company["status_override"] = {
            "status": "Suspended",
            "source_url": "https://www.hkexnews.hk/example.pdf",
        }
        result = aftermarket.calculate_metrics(company, stock_bars, benchmark_bars, benchmark_bars)
        self.assertEqual(result[139], "Suspended")
        self.assertEqual(
            result["observation_meta"]["listing_status_source"],
            "https://www.hkexnews.hk/example.pdf",
        )


if __name__ == "__main__":
    unittest.main()
