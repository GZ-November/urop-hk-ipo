"""Market horizons use calendar anniversaries and respect the observation date."""
import datetime as dt
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
from market_panel import MarketPanelEngine


def bar(date, close=10.0, turnover=100.0):
    if isinstance(date, str):
        date = dt.date.fromisoformat(date)
    return {"date": date, "open": close, "high": close, "low": close,
            "close": close, "volume": 100, "turnover": turnover}


def process(listing_date, today, bars):
    engine = object.__new__(MarketPanelEngine)
    engine.today = dt.date.fromisoformat(today)
    engine.fetch_issuer_bars = lambda stock_code, from_date: list(bars)
    issuer = {"stock_code": "00001.HK", "listing_date": listing_date,
              "offer_price_hkd": 10.0}
    daily, horizons = engine.process_issuer(issuer, bars, bars)
    return daily, {record["horizon"]: record for record in horizons}


class CalendarMarketHorizonTests(unittest.TestCase):
    def test_one_month_clamps_january_31_and_uses_first_observed_day_after_target(self):
        bars = [bar("2026-01-31", 10), bar("2026-02-27", 11),
                bar("2026-03-02", 12), bar("2026-03-03", 15)]
        _, horizons = process("2026-01-31", "2026-03-03", bars)
        month = horizons["Month_1"]
        self.assertTrue(month["matured"])
        self.assertEqual(month["target_date"], "2026-02-28")
        self.assertEqual(month["actual_date"], "2026-03-02")
        self.assertEqual(month["close_price"], 12)
        self.assertAlmostEqual(month["bhr_from_day1"], 0.2)

    def test_calendar_anniversaries_have_precise_target_dates(self):
        expected = {"Month_1": "2024-09-30", "Month_3": "2024-11-30",
                    "Month_6": "2025-02-28", "Month_12": "2025-08-31",
                    "Month_24": "2026-08-31", "Month_36": "2027-08-31"}
        bars = [bar("2024-08-31"), *[bar(date, 12) for date in expected.values()]]
        _, horizons = process("2024-08-31", "2027-08-31", bars)
        for name, target in expected.items():
            with self.subTest(horizon=name):
                self.assertEqual(horizons[name]["target_date"], target)
                self.assertEqual(horizons[name]["actual_date"], target)
                self.assertTrue(horizons[name]["matured"])

    def test_126_bars_before_six_calendar_months_do_not_mature_six_month_horizon(self):
        start = dt.date(2026, 1, 1)
        bars = [bar(start + dt.timedelta(days=day)) for day in range(126)]
        _, horizons = process("2026-01-01", "2026-05-06", bars)
        six_months = horizons["Month_6"]
        self.assertFalse(six_months["matured"])
        self.assertEqual(six_months["target_date"], "2026-07-01")
        self.assertIsNone(six_months["actual_date"])
        self.assertIsNone(six_months["bhr_from_day1"])
        self.assertIsNone(six_months["avg_daily_turnover"])

    def test_fewer_than_126_observations_can_mature_six_calendar_months(self):
        bars = [bar("2026-01-01", 10), bar("2026-06-30", 11),
                bar("2026-07-01", 13)]
        _, horizons = process("2026-01-01", "2026-07-01", bars)
        six_months = horizons["Month_6"]
        self.assertTrue(six_months["matured"])
        self.assertEqual(six_months["actual_date"], "2026-07-01")
        self.assertAlmostEqual(six_months["bhr_from_day1"], 0.3)

    def test_turnover_window_ends_at_actual_calendar_endpoint(self):
        bars = [bar("2026-01-31", turnover=100), bar("2026-02-27", turnover=200),
                bar("2026-03-02", turnover=300), bar("2026-03-03", turnover=100_000)]
        _, horizons = process("2026-01-31", "2026-03-03", bars)
        month = horizons["Month_1"]
        self.assertEqual(month["actual_date"], "2026-03-02")
        self.assertEqual(month["avg_daily_turnover"], 200.0)
        self.assertEqual(month["liquidity_decay_ratio"], 2.0)

    def test_cached_future_bars_do_not_enter_daily_panel_or_mature_horizons(self):
        bars = [bar("2025-12-31"), bar("2026-01-01"), bar("2026-06-30", 11),
                bar("2026-07-01", 99)]
        daily, horizons = process("2026-01-01", "2026-06-30", bars)
        self.assertEqual([row["trade_date"] for row in daily], ["2026-01-01", "2026-06-30"])
        self.assertFalse(horizons["Month_6"]["matured"])
        self.assertIsNone(horizons["Month_6"]["close_price"])

    def test_day_five_still_uses_fifth_observation(self):
        dates = ["2026-01-02", "2026-01-05", "2026-01-06", "2026-01-07",
                 "2026-01-08", "2026-01-09"]
        bars = [bar(date, 10 + index) for index, date in enumerate(dates)]
        _, horizons = process("2026-01-02", "2026-01-09", list(reversed(bars)))
        day_five = horizons["Day_5"]
        self.assertTrue(day_five["matured"])
        self.assertEqual(day_five["actual_date"], "2026-01-08")
        self.assertEqual(day_five["close_price"], 14)
        self.assertAlmostEqual(day_five["bhr_from_day1"], 0.4)


if __name__ == "__main__":
    unittest.main()
