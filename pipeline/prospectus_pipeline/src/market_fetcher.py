"""高容灾多源证券市场数据抓取引擎 (Resilient Multi-Provider Market Data Fetcher)

架构说明：
  1. 默认主数据源：腾讯证券高频日 K 线 (TencentProvider)
     - 包含交易所官方高精度日成交额（Turnover）与前复权 K 线序列。
  2. 容灾备用源：雅虎财经官方 REST 接口 (YahooFinanceProvider)
     - 当腾讯接口发生超时、网络阻断、IP 限流、字段变更或空响应时，自动无缝降级切换至 Yahoo Finance (v8 chart API)。
     - 自动映射恒指 (^HSI) 与恒生科技指数 (HSTECH.HK) 以及港股四位股票代码 (如 6082.HK)。
     - 采用双端冗余 (query2.finance.yahoo.com 优先，query1 备用) 及抗封禁请求头。
  3. 观察清单与数据血统 (Observation Provenance)：
     - 精确记录数据源提供方 (provider: tencent | yahoo)、抓取时间戳与 fallback 降级历史。
     - 备用源成交额使用标准金融代理指标（典型均价 × 成交量）估算，并在元数据中明确标注。
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import math
import time
import urllib.parse
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("market_fetcher")

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

HK_TZ = dt.timezone(dt.timedelta(hours=8))


def parse_bar_date(v: Any) -> dt.date:
    """统一转换各种格式的日期对象为 dt.date。"""
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v)[:10].strip()
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


class MarketDataProvider(ABC):
    """市场数据源抽象基类。"""

    name: str

    @abstractmethod
    def normalize_symbol(self, code_or_symbol: str) -> str:
        """规范化标的代码。"""
        pass

    @abstractmethod
    def fetch_bars(
        self,
        symbol_or_code: str,
        from_date: dt.date | str,
        to_date: dt.date | str,
        n_bars: int = 350,
        timeout: int = 25,
    ) -> list[dict[str, Any]]:
        """拉取指定标的之规范化日 K 线序列。

        每条 K 线必须包含：
          - date: dt.date
          - open: float
          - close: float
          - high: float
          - low: float
          - volume: float (股)
          - turnover: Optional[float] (港元，若无则为 None)
          - turnover_estimated: bool
        """
        pass


class TencentProvider(MarketDataProvider):
    """腾讯证券日 K 线提供商 (Primary Provider)。"""

    name = "tencent"

    def __init__(self, user_agent: str = DEFAULT_UA) -> None:
        self.user_agent = user_agent

    def normalize_symbol(self, code_or_symbol: str) -> str:
        s = str(code_or_symbol).strip().upper()
        if s in ("HSI", "^HSI", "HKHSI", "%5EHSI"):
            return "hkHSI"
        if s in ("HSTECH", "^HSTECH", "HSTECH.HK", "HKHSTECH", "%5EHSTECH"):
            return "hkHSTECH"
        digits = "".join(ch for ch in s if ch.isdigit())
        if digits:
            return f"hk{int(digits):05d}"
        return code_or_symbol

    def fetch_bars(
        self,
        symbol_or_code: str,
        from_date: dt.date | str,
        to_date: dt.date | str,
        n_bars: int = 350,
        timeout: int = 25,
    ) -> list[dict[str, Any]]:
        sym = self.normalize_symbol(symbol_or_code)
        frm_str = str(from_date)[:10]
        to_str = str(to_date)[:10]
        url = (
            "https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
            f"?param={sym},day,{frm_str},{to_str},{n_bars},qfq"
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "*/*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        if payload.get("code") != 0:
            raise RuntimeError(
                f"Tencent API error code={payload.get('code')}: {payload.get('msg')}"
            )

        data = (payload.get("data") or {}).get(sym) or {}
        rows = data.get("qfqday") or data.get("day") or []
        if not rows:
            raise RuntimeError(
                f"Tencent returned empty bars for {sym} ({frm_str} ~ {to_str})"
            )

        bars = []
        for row in rows:
            turnover = None
            if len(row) > 8 and row[8] not in (None, "", "{}", {}):
                try:
                    turnover = float(row[8]) * 10_000.0  # 腾讯第 9 列单位为万元
                except (TypeError, ValueError):
                    turnover = None
            bars.append({
                "date": parse_bar_date(row[0]),
                "open": float(row[1]),
                "close": float(row[2]),
                "high": float(row[3]),
                "low": float(row[4]),
                "volume": float(row[5]),
                "turnover": turnover,
                "turnover_estimated": False,
            })
        bars.sort(key=lambda x: x["date"])
        return bars


class YahooFinanceProvider(MarketDataProvider):
    """雅虎财经 REST API 提供商 (Disaster Recovery Fallback Provider)。"""

    name = "yahoo"

    def __init__(self, user_agent: str = DEFAULT_UA) -> None:
        self.user_agent = user_agent
        self.endpoints = [
            "https://query2.finance.yahoo.com",
            "https://query1.finance.yahoo.com",
        ]

    def normalize_symbol(self, code_or_symbol: str) -> str:
        s = str(code_or_symbol).strip().upper()
        if s in ("HSI", "^HSI", "HKHSI", "%5EHSI"):
            return "%5EHSI"  # URL-encoded ^HSI
        if s in ("HSTECH", "^HSTECH", "HSTECH.HK", "HKHSTECH", "%5EHSTECH"):
            return "HSTECH.HK"
        digits = "".join(ch for ch in s if ch.isdigit())
        if digits:
            return f"{int(digits):04d}.HK"
        return code_or_symbol

    def fetch_bars(
        self,
        symbol_or_code: str,
        from_date: dt.date | str,
        to_date: dt.date | str,
        n_bars: int = 350,
        timeout: int = 25,
    ) -> list[dict[str, Any]]:
        sym = self.normalize_symbol(symbol_or_code)
        d_from = parse_bar_date(from_date)
        d_to = parse_bar_date(to_date)

        # 港股时区 UTC+8 转换为 unix timestamp
        p1 = int(dt.datetime(d_from.year, d_from.month, d_from.day, 0, 0, 0, tzinfo=HK_TZ).timestamp())
        p2 = int(dt.datetime(d_to.year, d_to.month, d_to.day, 23, 59, 59, tzinfo=HK_TZ).timestamp()) + 86400

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }

        last_error = None
        payload = None
        for base in self.endpoints:
            url = f"{base}/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d"
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                    if payload:
                        break
            except urllib.error.HTTPError as he:
                err_msg = f"{base} HTTP {he.code}"
                try:
                    err_body = he.read().decode("utf-8")
                    err_json = json.loads(err_body)
                    chart_err = (err_json.get("chart") or {}).get("error")
                    if chart_err:
                        err_msg += f": {chart_err.get('description', chart_err)}"
                except Exception:
                    pass
                last_error = RuntimeError(err_msg)
            except Exception as exc:
                last_error = exc

        if payload is None:
            raise RuntimeError(f"Yahoo Finance failed for {sym}: {last_error}")

        res_list = (payload.get("chart") or {}).get("result") or []
        if not res_list:
            err = (payload.get("chart") or {}).get("error")
            raise RuntimeError(f"Yahoo Finance API error for {sym}: {err}")

        res = res_list[0]
        timestamps = res.get("timestamp") or []
        quote = ((res.get("indicators") or {}).get("quote") or [{}])[0]
        opens = quote.get("open") or []
        closes = quote.get("close") or []
        highs = quote.get("high") or []
        lows = quote.get("low") or []
        volumes = quote.get("volume") or []

        if not timestamps:
            raise RuntimeError(
                f"Yahoo Finance returned 0 historical bars for {sym} ({d_from} ~ {d_to})"
            )

        bars = []
        for i, ts in enumerate(timestamps):
            o = opens[i] if i < len(opens) else None
            c = closes[i] if i < len(closes) else None
            h = highs[i] if i < len(highs) else None
            l = lows[i] if i < len(lows) else None
            v = volumes[i] if i < len(volumes) else 0.0

            # 过滤节假日、未开市或未成交空行
            if c is None or o is None:
                continue

            bar_date = dt.datetime.fromtimestamp(ts, tz=HK_TZ).date()
            vol_float = float(v or 0.0)
            # 雅虎接口不直接提供逐笔成交额，用典范均价 (High+Low+Close)/3 * Volume 近似成交额
            turnover_est = (
                vol_float * ((float(h or c) + float(l or c) + float(c)) / 3.0)
                if vol_float > 0
                else 0.0
            )

            bars.append({
                "date": bar_date,
                "open": float(o),
                "close": float(c),
                "high": float(h if h is not None else max(o, c)),
                "low": float(l if l is not None else min(o, c)),
                "volume": vol_float,
                "turnover": turnover_est,
                "turnover_estimated": True,
            })

        if not bars:
            raise RuntimeError(f"No valid trading bars parsed from Yahoo Finance for {sym}")

        bars.sort(key=lambda x: x["date"])
        return bars


class ResilientMarketFetcher:
    """高可用弹性市场行情抓取调度引擎。"""

    def __init__(
        self,
        providers: list[MarketDataProvider] | None = None,
        retries_per_provider: int = 3,
        backoff_sec: float = 0.5,
    ) -> None:
        self.providers = providers or [TencentProvider(), YahooFinanceProvider()]
        self.retries_per_provider = retries_per_provider
        self.backoff_sec = backoff_sec

    def fetch_bars_resilient(
        self,
        symbol_or_code: str,
        from_date: dt.date | str,
        to_date: dt.date | str,
        n_bars: int = 350,
        preferred_provider: str | None = None,
    ) -> tuple[list[dict[str, Any]], str, list[str]]:
        """按优先级尝试各数据源，实现自动故障转移。

        返回: (bars, successful_provider_name, error_history)
        """
        active_providers = self.providers[:]
        if preferred_provider and preferred_provider.lower() != "auto":
            pref = preferred_provider.lower().strip()
            active_providers.sort(key=lambda p: 0 if p.name.lower() == pref else 1)

        errors: list[str] = []
        for provider in active_providers:
            for attempt in range(1, self.retries_per_provider + 1):
                try:
                    bars = provider.fetch_bars(
                        symbol_or_code, from_date, to_date, n_bars=n_bars
                    )
                    if bars:
                        if errors:
                            logger.info(
                                f"Failover succeeded: {symbol_or_code} fetched via {provider.name} "
                                f"after previous errors: {errors}"
                            )
                        return bars, provider.name, errors
                except Exception as exc:  # noqa: BLE001
                    msg = f"[{provider.name}] attempt {attempt}/{self.retries_per_provider} failed for {symbol_or_code}: {exc}"
                    errors.append(msg)
                    logger.warning(msg)
                    if attempt < self.retries_per_provider:
                        time.sleep(self.backoff_sec * attempt)

        raise RuntimeError(
            f"All market data providers failed for {symbol_or_code} ({from_date} ~ {to_date}). "
            f"Errors: {'; '.join(errors)}"
        )


_DEFAULT_FETCHER: ResilientMarketFetcher | None = None


def get_market_fetcher() -> ResilientMarketFetcher:
    """获取全局默认弹性市场行情调度器单例。"""
    global _DEFAULT_FETCHER
    if _DEFAULT_FETCHER is None:
        _DEFAULT_FETCHER = ResilientMarketFetcher()
    return _DEFAULT_FETCHER
