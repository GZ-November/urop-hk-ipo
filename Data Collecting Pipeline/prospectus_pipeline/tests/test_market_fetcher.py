"""市场数据高可用多源抓取引擎单元测试 (Resilient Market Data Fetcher Tests)

验证：
  1. 腾讯与雅虎符号规范化映射 (HSI, HSTECH, 港股代码);
  2. 主数据源正常响应与数据规范化验证;
  3. 主数据源故障时自动向备用数据源 (Yahoo Finance) 故障转移与血统日志记录;
  4. 全源故障时的 Fail-Closed 防伪造断言;
  5. 偏好数据源指定与动态重排逻辑;
  6. 典型均价代理成交额估算逻辑。
"""
from __future__ import annotations

import datetime as dt
import json
import unittest
from unittest.mock import MagicMock, patch

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from market_fetcher import (
    MarketDataProvider,
    ResilientMarketFetcher,
    TencentProvider,
    YahooFinanceProvider,
    get_market_fetcher,
    parse_bar_date,
)


class MockProvider(MarketDataProvider):
    def __init__(self, name: str, should_fail: bool = False, bars: list[dict] | None = None) -> None:
        self.name = name
        self.should_fail = should_fail
        self.call_count = 0
        self.bars = bars or [
            {
                "date": dt.date(2026, 1, 2),
                "open": 35.0,
                "close": 36.0,
                "high": 37.0,
                "low": 34.0,
                "volume": 100_000.0,
                "turnover": 3_600_000.0,
                "turnover_estimated": False,
            }
        ]

    def normalize_symbol(self, code_or_symbol: str) -> str:
        return f"{self.name}:{code_or_symbol}"

    def fetch_bars(
        self,
        symbol_or_code: str,
        from_date: dt.date | str,
        to_date: dt.date | str,
        n_bars: int = 350,
        timeout: int = 25,
    ) -> list[dict]:
        self.call_count += 1
        if self.should_fail:
            raise ConnectionResetError(f"Mock network drop from {self.name}")
        return self.bars


class MarketFetcherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tp = TencentProvider()
        self.yp = YahooFinanceProvider()

    def test_tencent_symbol_normalization(self) -> None:
        self.assertEqual(self.tp.normalize_symbol("HSI"), "hkHSI")
        self.assertEqual(self.tp.normalize_symbol("^HSI"), "hkHSI")
        self.assertEqual(self.tp.normalize_symbol("%5EHSI"), "hkHSI")
        self.assertEqual(self.tp.normalize_symbol("hkHSI"), "hkHSI")

        self.assertEqual(self.tp.normalize_symbol("HSTECH"), "hkHSTECH")
        self.assertEqual(self.tp.normalize_symbol("^HSTECH"), "hkHSTECH")
        self.assertEqual(self.tp.normalize_symbol("HSTECH.HK"), "hkHSTECH")

        self.assertEqual(self.tp.normalize_symbol("6082"), "hk06082")
        self.assertEqual(self.tp.normalize_symbol("06082"), "hk06082")
        self.assertEqual(self.tp.normalize_symbol("6082.HK"), "hk06082")
        self.assertEqual(self.tp.normalize_symbol("0700"), "hk00700")

    def test_yahoo_symbol_normalization(self) -> None:
        self.assertEqual(self.yp.normalize_symbol("HSI"), "%5EHSI")
        self.assertEqual(self.yp.normalize_symbol("^HSI"), "%5EHSI")
        self.assertEqual(self.yp.normalize_symbol("hkHSI"), "%5EHSI")

        self.assertEqual(self.yp.normalize_symbol("HSTECH"), "HSTECH.HK")
        self.assertEqual(self.yp.normalize_symbol("hkHSTECH"), "HSTECH.HK")

        self.assertEqual(self.yp.normalize_symbol("6082"), "6082.HK")
        self.assertEqual(self.yp.normalize_symbol("06082"), "6082.HK")
        self.assertEqual(self.yp.normalize_symbol("6082.HK"), "6082.HK")
        self.assertEqual(self.yp.normalize_symbol("0700"), "0700.HK")
        self.assertEqual(self.yp.normalize_symbol("100"), "0100.HK")

    def test_parse_bar_date_formats(self) -> None:
        d = dt.date(2026, 3, 15)
        self.assertEqual(parse_bar_date(d), d)
        self.assertEqual(parse_bar_date(dt.datetime(2026, 3, 15, 12, 0, 0)), d)
        self.assertEqual(parse_bar_date("2026-03-15"), d)
        self.assertEqual(parse_bar_date("2026-03-15 09:30:00"), d)

    def test_resilient_fetcher_primary_success(self) -> None:
        p1 = MockProvider("primary", should_fail=False)
        p2 = MockProvider("fallback", should_fail=False)
        fetcher = ResilientMarketFetcher(providers=[p1, p2], retries_per_provider=2, backoff_sec=0.01)

        bars, prov, errs = fetcher.fetch_bars_resilient("6082", "2026-01-01", "2026-01-10")
        self.assertEqual(prov, "primary")
        self.assertEqual(len(bars), 1)
        self.assertEqual(errs, [])
        self.assertEqual(p1.call_count, 1)
        self.assertEqual(p2.call_count, 0)

    def test_resilient_fetcher_automatic_failover(self) -> None:
        p1 = MockProvider("primary", should_fail=True)
        p2 = MockProvider("fallback", should_fail=False)
        fetcher = ResilientMarketFetcher(providers=[p1, p2], retries_per_provider=2, backoff_sec=0.01)

        bars, prov, errs = fetcher.fetch_bars_resilient("6082", "2026-01-01", "2026-01-10")
        self.assertEqual(prov, "fallback")
        self.assertEqual(len(bars), 1)
        self.assertEqual(len(errs), 2)  # 2 retries on primary
        self.assertIn("[primary] attempt 1/2 failed", errs[0])
        self.assertIn("[primary] attempt 2/2 failed", errs[1])
        self.assertEqual(p1.call_count, 2)
        self.assertEqual(p2.call_count, 1)

    def test_resilient_fetcher_all_fail_closed(self) -> None:
        p1 = MockProvider("primary", should_fail=True)
        p2 = MockProvider("fallback", should_fail=True)
        fetcher = ResilientMarketFetcher(providers=[p1, p2], retries_per_provider=1, backoff_sec=0.01)

        with self.assertRaises(RuntimeError) as ctx:
            fetcher.fetch_bars_resilient("6082", "2026-01-01", "2026-01-10")
        self.assertIn("All market data providers failed", str(ctx.exception))
        self.assertIn("primary", str(ctx.exception))
        self.assertIn("fallback", str(ctx.exception))

    def test_resilient_fetcher_preferred_provider(self) -> None:
        p1 = MockProvider("primary", should_fail=False)
        p2 = MockProvider("fallback", should_fail=False)
        fetcher = ResilientMarketFetcher(providers=[p1, p2], retries_per_provider=1, backoff_sec=0.01)

        bars, prov, errs = fetcher.fetch_bars_resilient(
            "6082", "2026-01-01", "2026-01-10", preferred_provider="fallback"
        )
        self.assertEqual(prov, "fallback")
        self.assertEqual(p2.call_count, 1)
        self.assertEqual(p1.call_count, 0)

    def test_tencent_payload_parsing(self) -> None:
        fake_response = {
            "code": 0,
            "msg": "",
            "data": {
                "hk06082": {
                    "day": [
                        ["2026-01-02", "35.70", "34.46", "36.20", "33.80", "150709945", {}, None, "552127.56"]
                    ]
                }
            }
        }
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_resp = MagicMock()
            mock_resp.read.return_value = json.dumps(fake_response).encode("utf-8")
            mock_urlopen.return_value.__enter__.return_value = mock_resp

            bars = self.tp.fetch_bars("6082", "2026-01-02", "2026-01-02")
            self.assertEqual(len(bars), 1)
            b = bars[0]
            self.assertEqual(b["date"], dt.date(2026, 1, 2))
            self.assertAlmostEqual(b["open"], 35.70)
            self.assertAlmostEqual(b["close"], 34.46)
            self.assertAlmostEqual(b["high"], 36.20)
            self.assertAlmostEqual(b["low"], 33.80)
            self.assertEqual(b["volume"], 150709945.0)
            self.assertAlmostEqual(b["turnover"], 5521275600.0, delta=1.0)
            self.assertFalse(b["turnover_estimated"])

    def test_yahoo_chart_payload_parsing_and_typical_price(self) -> None:
        fake_response = {
            "chart": {
                "result": [
                    {
                        "meta": {"currency": "HKD", "symbol": "6082.HK"},
                        "timestamp": [1767317400],  # 2026-01-02 01:30 UTC
                        "indicators": {
                            "quote": [
                                {
                                    "open": [35.70],
                                    "close": [34.46],
                                    "high": [36.20],
                                    "low": [33.80],
                                    "volume": [10000.0],
                                }
                            ]
                        }
                    }
                ],
                "error": None
            }
        }
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_resp = MagicMock()
            mock_resp.read.return_value = json.dumps(fake_response).encode("utf-8")
            mock_urlopen.return_value.__enter__.return_value = mock_resp

            bars = self.yp.fetch_bars("6082", "2026-01-02", "2026-01-02")
            self.assertEqual(len(bars), 1)
            b = bars[0]
            self.assertEqual(b["date"], dt.date(2026, 1, 2))
            self.assertAlmostEqual(b["open"], 35.70)
            self.assertAlmostEqual(b["close"], 34.46)
            self.assertEqual(b["volume"], 10000.0)
            # typical price = (36.20 + 33.80 + 34.46) / 3 = 34.82
            # turnover = 10000 * 34.82 = 348200.0
            expected_turnover = 10000.0 * ((36.20 + 33.80 + 34.46) / 3.0)
            self.assertAlmostEqual(b["turnover"], expected_turnover)
            self.assertTrue(b["turnover_estimated"])


if __name__ == "__main__":
    unittest.main()
