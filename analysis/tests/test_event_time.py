"""Tests for the event-time aftermarket helpers."""
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS))
import aftermarket_event_time_2026 as et


def series(values, start="2026-01-05", freq="B"):
    return pd.Series(values, index=pd.date_range(start, periods=len(values), freq=freq), dtype=float)


class AlignmentTests(unittest.TestCase):
    def test_missing_benchmark_date_is_dropped_not_zero_filled(self):
        stock = series([10, 11, 12, 13])
        bench = stock.copy() * 0 + 100
        bench = bench.drop(stock.index[2])  # benchmark closed / missing on day 2
        frame = et.aligned_returns(stock, bench)
        self.assertTrue(np.isnan(frame["m"].iloc[2]))  # return into the missing day is unknown
        self.assertTrue(np.isnan(frame["m"].iloc[3]))  # and out of it: never a silent zero

    def test_event_day_zero_is_the_first_bar(self):
        frame = et.aligned_returns(series([10, 11, 12]), series([100, 100, 100]))
        self.assertEqual(frame["event_day"].tolist(), [0, 1, 2])


class BharTests(unittest.TestCase):
    def panel(self):
        rows = []
        for code, hot, path in [("A", 1.0, [10, 12, 15]), ("B", 0.0, [10, 10, 10])]:
            stock = series(path)
            bench = series([100, 110, 121])  # +10% per day
            frame = et.aligned_returns(stock, bench)
            frame["idx_HSI"], frame["m_HSI"] = frame["bench"], frame["m"]
            frame["code"], frame["hot"], frame["month"] = code, hot, "2026-01"
            rows.append(frame.rename_axis("date").reset_index())
        return pd.concat(rows, ignore_index=True)

    def test_bhar_is_stock_minus_benchmark_buy_and_hold(self):
        z = et.bhar(self.panel(), "HSI", 2)
        self.assertAlmostEqual(z.loc["A", "bhar"], 0.5 - 0.21)
        self.assertAlmostEqual(z.loc["B", "bhar"], 0.0 - 0.21)

    def test_calendar_portfolio_requires_minimum_issuers_and_holding_window(self):
        panel = self.panel()
        self.assertTrue(et.calendar_portfolio(panel, "HSI", None).empty)  # only two issuers per date
        many = pd.concat([panel.assign(code=panel["code"] + str(i)) for i in range(4)], ignore_index=True)
        port = et.calendar_portfolio(many, "HSI", None, hold=1)
        self.assertEqual(len(port), 1)  # only event day 1 is inside a one-day holding window
        self.assertEqual(int(port["n"].iloc[0]), 8)


class NeweyWestTests(unittest.TestCase):
    def test_alpha_detects_positive_mean_and_not_zero_mean(self):
        rng = np.random.default_rng(0)
        positive = pd.Series(rng.normal(0.01, 0.01, 300))
        self.assertLess(et.nw_alpha(positive)["p"], 0.001)
        self.assertGreater(et.nw_alpha(pd.Series(rng.normal(0, 0.01, 300)))["p"], 0.01)


if __name__ == "__main__":
    unittest.main()
