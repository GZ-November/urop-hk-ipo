"""Lockup event metrics require complete windows and observed benchmark returns."""
import datetime as dt
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from lockup_panel import LockupPanelEngine  # noqa: E402

CODE = "1234.HK"
FIRST_DATE = dt.date(2025, 1, 1)


def make_engine(count: int = 86) -> LockupPanelEngine:
    """Build an in-memory engine with flat HSI and one-percent stock returns."""
    engine = object.__new__(LockupPanelEngine)
    bars = [{"date": FIRST_DATE + dt.timedelta(days=i), "daily_return": 0.01,
             "turnover": 100} for i in range(count)]
    engine.daily_bars = {CODE: bars}
    engine.hsi_map = {bar["date"]: 100 for bar in bars}
    return engine


def metrics(engine: LockupPanelEngine, unlock_index: int = 25) -> tuple:
    return engine.calculate_event_window_metrics(CODE, FIRST_DATE + dt.timedelta(days=unlock_index))


class LockupWindowCoverageTests(unittest.TestCase):
    def test_full_windows_have_expected_car_and_matured_status(self):
        car20, car5, car60, volume, status = metrics(make_engine())
        self.assertAlmostEqual(car20, 0.41)
        self.assertAlmostEqual(car5, 0.11)
        self.assertAlmostEqual(car60, 0.61)
        self.assertEqual(volume, 1.0)
        self.assertEqual(status, "MATURED")

    def test_exact_plus60_boundary_is_incomplete_without_index_error(self):
        car20, car5, car60, volume, status = metrics(make_engine(85))
        self.assertAlmostEqual(car20, 0.41)
        self.assertAlmostEqual(car5, 0.11)
        self.assertIsNone(car60)
        self.assertEqual(volume, 1.0)
        self.assertEqual(status, "INCOMPLETE_WINDOW")

    def test_tiny_trading_history_cannot_stand_in_for_named_windows(self):
        self.assertEqual(metrics(make_engine(8), unlock_index=3),
                         (None, None, None, None, "INCOMPLETE_WINDOW"))

    def test_independent_short_window_survives_missing_long_window_endpoints(self):
        car20, car5, car60, volume, status = metrics(make_engine(15), unlock_index=6)
        self.assertIsNone(car20)
        self.assertAlmostEqual(car5, 0.11)
        self.assertIsNone(car60)
        self.assertIsNone(volume)
        self.assertEqual(status, "INCOMPLETE_WINDOW")

    def test_car_start_at_first_bar_requires_prior_price_history(self):
        car20, car5, car60, volume, status = metrics(make_engine(66), unlock_index=5)
        self.assertIsNone(car20)
        self.assertIsNone(car5)
        self.assertAlmostEqual(car60, 0.61)
        self.assertIsNone(volume)
        self.assertEqual(status, "INCOMPLETE_WINDOW")

    def test_true_zero_turnover_is_kept_in_pre_unlock_average(self):
        engine = make_engine()
        engine.daily_bars[CODE][5]["turnover"] = 0
        *_, volume, status = metrics(engine)
        self.assertAlmostEqual(volume, round(100 / 95, 4))
        self.assertEqual(status, "MATURED")

    def test_true_zero_post_unlock_turnover_gives_zero_shock(self):
        engine = make_engine()
        for bar in engine.daily_bars[CODE][25:46]:
            bar["turnover"] = 0
        *_, volume, status = metrics(engine)
        self.assertEqual(volume, 0)
        self.assertEqual(status, "MATURED")

    def test_no_trading_data_keeps_existing_status(self):
        self.assertEqual(metrics(make_engine(0)), (None, None, None, None, "NO_TRADING_DATA"))

    def test_future_unlock_keeps_existing_immature_status(self):
        engine = make_engine()
        future = dt.date.today() + dt.timedelta(days=1)
        self.assertEqual(engine.calculate_event_window_metrics(CODE, future),
                         (None, None, None, None, "IMMATURE_WINDOW"))

    def test_no_post_unlock_bar_keeps_existing_status(self):
        self.assertEqual(metrics(make_engine(10)),
                         (None, None, None, None, "POST_UNLOCK_TRADING_MISSING"))


class LockupWindowEvidenceTests(unittest.TestCase):
    def test_left_endpoint_stock_return_is_required_for_each_inclusive_window(self):
        expected = {5: (None, 0.11, 0.61), 20: (None, None, 0.61), 25: (None, None, None)}
        for index, expected_cars in expected.items():
            with self.subTest(left_endpoint=index):
                engine = make_engine()
                engine.daily_bars[CODE][index]["daily_return"] = None
                car20, car5, car60, volume, status = metrics(engine)
                for actual, wanted in zip((car20, car5, car60), expected_cars):
                    if wanted is None:
                        self.assertIsNone(actual)
                    else:
                        self.assertAlmostEqual(actual, wanted)
                self.assertEqual(volume, 1.0)
                self.assertEqual(status, "MISSING_RETURN_DATA")

    def test_missing_previous_benchmark_quote_only_blanks_affected_window(self):
        engine = make_engine()
        del engine.hsi_map[FIRST_DATE + dt.timedelta(days=4)]
        car20, car5, car60, volume, status = metrics(engine)
        self.assertIsNone(car20)
        self.assertAlmostEqual(car5, 0.11)
        self.assertAlmostEqual(car60, 0.61)
        self.assertEqual(volume, 1.0)
        self.assertEqual(status, "MISSING_BENCHMARK_DATA")

    def test_missing_current_benchmark_quote_blanks_all_affected_cars(self):
        engine = make_engine()
        del engine.hsi_map[FIRST_DATE + dt.timedelta(days=25)]
        car20, car5, car60, volume, status = metrics(engine)
        self.assertEqual((car20, car5, car60), (None, None, None))
        self.assertEqual(volume, 1.0)
        self.assertEqual(status, "MISSING_BENCHMARK_DATA")

    def test_invalid_benchmark_quotes_never_become_zero_benchmark_returns(self):
        for quote in (None, 0, float("nan"), float("inf")):
            with self.subTest(quote=quote):
                engine = make_engine()
                engine.hsi_map[FIRST_DATE + dt.timedelta(days=25)] = quote
                car20, car5, car60, volume, status = metrics(engine)
                self.assertEqual((car20, car5, car60), (None, None, None))
                self.assertEqual(volume, 1.0)
                self.assertEqual(status, "MISSING_BENCHMARK_DATA")

    def test_missing_or_nonfinite_stock_returns_only_blank_affected_windows(self):
        for value in (None, float("nan"), float("inf"), "missing-key"):
            with self.subTest(value=value):
                engine = make_engine()
                bar = engine.daily_bars[CODE][21]
                if value == "missing-key":
                    del bar["daily_return"]
                else:
                    bar["daily_return"] = value
                car20, car5, car60, volume, status = metrics(engine)
                self.assertEqual((car20, car5), (None, None))
                self.assertAlmostEqual(car60, 0.61)
                self.assertEqual(volume, 1.0)
                self.assertEqual(status, "MISSING_RETURN_DATA")


if __name__ == "__main__":
    unittest.main()
