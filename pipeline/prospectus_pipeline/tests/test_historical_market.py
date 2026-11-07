"""Historical HK IPO compatibility tests (Group C: Market Data & Pre-HSTECH)."""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

MODULE_PATH = ROOT / "tools" / "external" / "aftermarket.py"
SPEC = importlib.util.spec_from_file_location("aftermarket", MODULE_PATH)
aftermarket = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(aftermarket)

from market_fetcher import TencentProvider
from market_panel import MarketEngine, MarketPanelEngine


def make_bars(start: dt.date, days: int, base: float = 10.0) -> list[dict]:
    return [
        {
            "date": start + dt.timedelta(days=i),
            "open": base + i * 0.01,
            "close": base + i * 0.01,
            "high": base + i * 0.01,
            "low": base + i * 0.01,
            "volume": 1_000 + i,
            "turnover": 10_000.0 + i,
        }
        for i in range(days)
    ]


class HistoricalMarketTests(unittest.TestCase):
    def test_pre_2015_ipo_with_empty_hstech_bars(self) -> None:
        """When hstech_bars is empty (pre-2015 IPO), compute_metrics succeeds without error."""
        listing_date = dt.date(2005, 7, 13)
        company = {
            "listing_date": listing_date,
            "offer_price": 10.0,
            "day1_close": 10.0,
            "day1_turnover": 10_000.0,
            "unlock_date": None,
            "is_18a": False,
            "is_18c": False,
            "name": "Historical 2005 Issuer",
        }
        stock_bars = make_bars(listing_date, 200, base=10.0)
        hsi_bars = make_bars(listing_date, 200, base=15000.0)
        hstech_bars: list[dict] = []

        result = aftermarket.compute_metrics(company, stock_bars, hsi_bars, hstech_bars)

        self.assertNotIn("error", result)
        self.assertIsNotNone(result.get("adj_ret_1m_hsi"))
        self.assertIsNotNone(result.get("wr_hsi_1m"))
        self.assertIsNone(result.get("hstech_ret_1m"))
        self.assertIsNone(result.get("wr_hstech_1m"))

    def test_tencent_fetch_bars_multi_window_chunking(self) -> None:
        """When (d_to - d_from).days > 750, fetch_bars queries contiguous 730-day windows."""
        tp = TencentProvider()
        d_from = "2020-01-01"
        d_to = "2023-01-01"

        def fake_urlopen(req, timeout=25):
            url = req.full_url
            mock_resp = MagicMock()
            if "2020-01-01" in url:
                payload = {
                    "code": 0,
                    "msg": "",
                    "data": {
                        "hk00700": {
                            "qfqday": [
                                ["2020-01-02", "380", "382", "385", "378", "1000", {}, None, "38"],
                                ["2021-12-31", "450", "453", "455", "448", "2000", {}, None, "90"],
                            ]
                        }
                    },
                }
            else:
                payload = {
                    "code": 0,
                    "msg": "",
                    "data": {
                        "hk00700": {
                            "qfqday": [
                                ["2021-12-31", "450", "453", "455", "448", "2000", {}, None, "90"],
                                ["2022-01-03", "455", "458", "460", "452", "1500", {}, None, "68"],
                            ]
                        }
                    },
                }
            mock_resp.read.return_value = json.dumps(payload).encode("utf-8")
            cm = MagicMock()
            cm.__enter__.return_value = mock_resp
            return cm

        with patch("urllib.request.urlopen", side_effect=fake_urlopen) as mock_open:
            bars = tp.fetch_bars("0700", d_from, d_to)
            self.assertEqual(mock_open.call_count, 2)
            # Verify deduplication: 2021-12-31 present in both responses appears only once
            dates = [b["date"] for b in bars]
            self.assertEqual(len(dates), 3)
            self.assertEqual(
                dates,
                [dt.date(2020, 1, 2), dt.date(2021, 12, 31), dt.date(2022, 1, 3)],
            )

    def test_tencent_fetch_raw_bars_404_fallback(self) -> None:
        """When static js returns HTTP 404, fetch_raw_bars falls back to unadjusted fqkline."""
        tp = TencentProvider()

        def fake_urlopen(req, timeout=25):
            url = req.full_url
            if "flashdata/hk/daily" in url:
                raise urllib.error.HTTPError(
                    url=url, code=404, msg="Not Found", hdrs={}, fp=None
                )
            mock_resp = MagicMock()
            payload = {
                "code": 0,
                "msg": "",
                "data": {
                    "hk00001": {
                        "day": [
                            ["2000-01-04", "100", "105", "106", "99", "50000"]
                        ]
                    }
                },
            }
            mock_resp.read.return_value = json.dumps(payload).encode("utf-8")
            cm = MagicMock()
            cm.__enter__.return_value = mock_resp
            return cm

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            bars = tp.fetch_bars("0001", "2000-01-01", "2000-01-10", adjusted=False)
            self.assertEqual(len(bars), 1)
            self.assertEqual(bars[0]["date"], dt.date(2000, 1, 4))
            self.assertEqual(bars[0]["close"], 105.0)
            self.assertEqual(bars[0]["price_basis"], "raw_as_traded")

    def test_market_engine_alias_and_horizon_bounds(self) -> None:
        """MarketEngine is an alias for MarketPanelEngine with bounded benchmark fetch."""
        import tempfile

        self.assertIs(MarketEngine, MarketPanelEngine)
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg = {
                "paths": {
                    "out": Path(tmp_dir) / "out",
                    "data": Path(tmp_dir) / "data",
                }
            }
            engine = MarketEngine(cfg=cfg)
            mock_fetcher = MagicMock()
            mock_fetcher.fetch_bars.return_value = [
                {"date": dt.date(2005, 1, 3), "close": 14000.0}
            ]
            engine.fetcher = mock_fetcher

            engine.fetch_benchmark_bars(
                "^HSI", dt.date(2005, 1, 1), max_date=dt.date(2008, 2, 15)
            )
            mock_fetcher.fetch_bars.assert_called_once_with(
                "^HSI", "2005-01-01", "2008-02-15", n_bars=1200
            )


if __name__ == "__main__":
    unittest.main()
