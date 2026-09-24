#!/usr/bin/env python3
"""逐日交易、微观结构与多跨期学术收益面板生成引擎 (Event-Level Market & Liquidity Panel).

功能：
  1. 为香港主板新股从挂牌首日 (Day 1) 起拉取逐日完整 K 线 (OHLCV, Turnover)；
  2. 自动抓取对标市场基准：恒生指数 (^HSI / hkHSI) 与恒生科技指数 (^HSTECH / hkHSTECH)；
  3. 计算逐日微观结构指标：
     - 日度收益率 (Daily Return)；
     - Amihud (2002) 非流动性指标：(|Return| / Turnover) * 1e6；
     - 零成交量标识 (Zero-volume indicator)；
     - 20日滚动波动率 (20-day rolling return volatility)；
     - 上市以来最大回撤 (Maximum drawdown)；
  4. 构建多重学术跨期事件窗口 (Day 1, Day 5, Day 20, 1M, 3M, 6M, 12M, 24M, 36M)：
     - 买入持有收益率 (BHR from Day-1 close)；
     - 一级发售价格累计回报率 (Total return from offer price)；
     - 同期恒指收益与恒科收益；
     - 财富相对比 (Wealth Relatives: WR = (1 + R_stock) / (1 + R_bench))；
     - 区间日均成交额与流动性衰减率 (Liquidity decay ratio)；
  5. 严格成熟度防前视审查 (Maturity Guard)：
     - 绝不以最新价格替代未成熟观测；
     - 未到期窗口严格置为空值，并标注 IMMATURE_WINDOW。
"""
from __future__ import annotations

import csv
import argparse
import datetime as dt
import json
import logging
import math
import statistics
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
sys_src = ROOT / "src"
import sys
if str(sys_src) not in sys.path:
    sys.path.insert(0, str(sys_src))

from market_fetcher import get_market_fetcher, parse_bar_date

logger = logging.getLogger("market_panel")
sys.path.insert(0, str(ROOT))
from cohort import load_cfg, read_companies, _read_workbook_issuers

# 标准跨期交易日对应关系（约数与日历月标准）
HORIZONS = [
    ("Day_1", 1, "首日挂牌交易"),
    ("Day_5", 5, "上市首周(T+5交易日)"),
    ("Day_20", 20, "上市首月(T+20交易日/稳价期基准)"),
    ("Month_1", 21, "满1个日历月"),
    ("Month_3", 63, "满3个日历月(季度)"),
    ("Month_6", 126, "满6个日历月(基石法定解禁点)"),
    ("Month_12", 252, "满1周年(首个年报期/控股股东解禁)"),
    ("Month_24", 504, "满2周年"),
    ("Month_36", 756, "满3周年(经典长期表现检验)"),
]


def load_issuers(
    workbook_path: Path | str | None = None,
    use_master_cache: bool = True,
    cfg: dict | None = None,
    *,
    focus_2026q1_only: bool | None = None,
) -> list[dict[str, Any]]:
    """Read issuers from the selected cohort, with compatibility for direct workbook callers."""
    cfg = cfg or load_cfg()
    if workbook_path is not None:
        cfg = {**cfg, "workbook": str(workbook_path), "workbook_path": Path(workbook_path)}

    if workbook_path is not None or "dataset" not in cfg:
        selected = _read_workbook_issuers(cfg)
        if not any(company.get("offer_price") is not None for company in selected):
            import openpyxl
            book_path = Path(cfg.get("workbook_path") or cfg["workbook"])
            if not book_path.is_absolute():
                book_path = Path(cfg.get("_ws", ROOT.parent)) / book_path
            workbook = openpyxl.load_workbook(book_path, read_only=True, data_only=True)
            try:
                worksheet = workbook[cfg["sheet"]]
                headers = {
                    " ".join(str(worksheet.cell(1, col).value or "").split()).strip().lower(): col
                    for col in range(1, worksheet.max_column + 1)
                }
                offer_col = headers.get("ipo subscription price (hk$)")
                if offer_col:
                    for company in selected:
                        company["offer_price"] = worksheet.cell(
                            company["row"], offer_col
                        ).value
            finally:
                workbook.close()
    else:
        selected = read_companies(cfg)
    issuers = []
    for company in selected:
        code = company["code"]
        if not code:
            continue
        c_str = str(code).strip()
        if not c_str.endswith(".HK"):
            digits = "".join(ch for ch in c_str if ch.isdigit())
            c_str = f"{int(digits):04d}.HK"
        offer_p = company.get("offer_price")
        try:
            offer_price = (
                float(str(offer_p).replace(",", "").strip())
                if offer_p not in (None, "")
                else None
            )
        except (TypeError, ValueError):
            offer_price = None
        issuers.append({
            "stock_code": c_str,
            "company_name": company["name"],
            "prospectus_date": company["prospectus_date"].isoformat() if company["prospectus_date"] else None,
            "listing_date": company["listing_date"].isoformat() if company["listing_date"] else None,
            "offer_price_hkd": offer_price,
            "row_idx": company["row"]
        })
    return issuers


class MarketPanelEngine:
    """逐日市场与微观结构面板构建器。"""

    def __init__(self, today: Optional[dt.date] = None, cfg: dict | None = None) -> None:
        self.cfg = cfg or load_cfg()
        self.out_master = self.cfg["paths"]["out"] / "master"
        self.cache_dir = self.cfg["paths"]["data"] / "market" / "daily_bars"
        self.fetcher = get_market_fetcher()
        self.today = today or dt.date.today()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.out_master.mkdir(parents=True, exist_ok=True)
        self.benchmarks: dict[str, list[dict[str, Any]]] = {}

    def fetch_benchmark_bars(self, symbol: str, from_date: dt.date) -> list[dict[str, Any]]:
        """拉取并缓存基准指数日度序列。"""
        if symbol in self.benchmarks:
            return self.benchmarks[symbol]
        cache_file = self.cache_dir / f"{symbol.replace('^', '')}_bars.json"
        if cache_file.exists():
            try:
                bars = json.loads(cache_file.read_text(encoding="utf-8"))
                for b in bars:
                    b["date"] = parse_bar_date(b["date"])
                self.benchmarks[symbol] = bars
                return bars
            except Exception:
                pass

        bars, prov, errs = self.fetcher.fetch_bars_resilient(symbol, from_date, self.today, n_bars=1200)
        # 序列化缓存
        ser = []
        for b in bars:
            rec = dict(b)
            rec["date"] = str(b["date"])
            ser.append(rec)
        cache_file.write_text(json.dumps(ser, indent=2), encoding="utf-8")
        self.benchmarks[symbol] = bars
        return bars

    def fetch_issuer_bars(self, stock_code: str, listing_date: dt.date) -> list[dict[str, Any]]:
        """拉取并缓存个股日度序列。"""
        cache_file = self.cache_dir / f"{stock_code}_bars.json"
        if cache_file.exists():
            try:
                bars = json.loads(cache_file.read_text(encoding="utf-8"))
                for b in bars:
                    b["date"] = parse_bar_date(b["date"])
                return bars
            except Exception:
                pass

        bars, prov, errs = self.fetcher.fetch_bars_resilient(stock_code, listing_date, self.today, n_bars=850)
        ser = []
        for b in bars:
            rec = dict(b)
            rec["date"] = str(b["date"])
            ser.append(rec)
        cache_file.write_text(json.dumps(ser, indent=2), encoding="utf-8")
        return bars

    def process_issuer(
        self,
        issuer: dict[str, Any],
        hsi_bars: list[dict[str, Any]],
        hstech_bars: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """处理单家公司的逐日面板与跨期汇总。"""
        code = issuer["stock_code"]
        l_date_str = issuer.get("listing_date")
        if not l_date_str:
            return [], []
        l_date = parse_bar_date(l_date_str)
        offer_p = issuer.get("offer_price_hkd")

        bars = self.fetch_issuer_bars(code, l_date)
        if not bars:
            logger.warning(f"No trading bars for {code}")
            return [], []

        # 确保按日期升序排列
        bars = sorted(bars, key=lambda x: x["date"])
        # 仅保留 listing_date 当日及以后的 bars
        bars = [b for b in bars if b["date"] >= l_date]
        if not bars:
            return [], []

        # 构建基准快速索引 (date -> close)
        hsi_map = {b["date"]: b["close"] for b in hsi_bars}
        hstech_map = {b["date"]: b["close"] for b in hstech_bars}

        # 逐日计算衍生指标
        daily_records: list[dict[str, Any]] = []
        cum_max_price = 0.0
        returns_history: list[float] = []

        for idx, bar in enumerate(bars):
            event_day = idx + 1
            close = bar["close"]
            prev_close = bars[idx - 1]["close"] if idx > 0 else offer_p or close
            ret = (close - prev_close) / prev_close if prev_close else 0.0
            returns_history.append(ret)

            # Amihud Illiquidity = (|Return| / Turnover) * 1e6
            turnover = bar.get("turnover") or 0.0
            illiq = (abs(ret) / turnover * 1e6) if turnover > 0 else None

            # 最大回撤
            cum_max_price = max(cum_max_price, bar.get("high") or close)
            dd = (cum_max_price - close) / cum_max_price if cum_max_price > 0 else 0.0

            # 20日滚动波动率
            vol_20 = None
            if len(returns_history) >= 5:
                window = returns_history[-20:]
                vol_20 = statistics.stdev(window) if len(window) > 1 else 0.0

            daily_records.append({
                "stock_code": code,
                "trade_date": str(bar["date"]),
                "event_day": event_day,
                "open": bar["open"],
                "high": bar["high"],
                "low": bar["low"],
                "close": close,
                "adj_close": close,
                "volume": bar["volume"],
                "turnover": turnover,
                "daily_return": round(ret, 6),
                "amihud_illiq": round(illiq, 6) if illiq is not None else None,
                "zero_volume_flag": (bar["volume"] == 0),
                "volatility_20d": round(vol_20, 6) if vol_20 is not None else None,
                "max_drawdown": round(dd, 6),
                "data_source": "tencent" if not bar.get("turnover_estimated") else "yahoo"
            })

        # 计算多跨期学术表现 (Horizons)
        day1_close = bars[0]["close"]
        day1_turnover = bars[0].get("turnover") or 0.0
        hsi_base = hsi_map.get(bars[0]["date"])
        hstech_base = hstech_map.get(bars[0]["date"])

        horizon_records: list[dict[str, Any]] = []

        for h_name, req_days, desc in HORIZONS:
            # 判断是否成熟
            matured = len(bars) >= req_days
            rec: dict[str, Any] = {
                "stock_code": code,
                "horizon": h_name,
                "horizon_desc": desc,
                "target_trading_days": req_days,
                "matured": matured,
                "target_date": str(l_date + dt.timedelta(days=int(req_days * 1.5))),  # 日历估算
            }

            if not matured:
                rec["actual_date"] = None
                rec["close_price"] = None
                rec["bhr_from_day1"] = None
                rec["total_return_from_offer"] = None
                rec["hsi_return"] = None
                rec["hstech_return"] = None
                rec["wr_hsi"] = None
                rec["wr_hstech"] = None
                rec["avg_daily_turnover"] = None
                rec["amihud_mean"] = None
                rec["liquidity_decay_ratio"] = None
                rec["missing_reason"] = "IMMATURE_WINDOW"
                horizon_records.append(rec)
                continue

            target_bar = bars[req_days - 1]
            rec["actual_date"] = str(target_bar["date"])
            p_end = target_bar["close"]
            rec["close_price"] = round(p_end, 4)

            # BHR = (P_T / P_Day1) - 1
            bhr = (p_end / day1_close) - 1.0 if day1_close > 0 else None
            rec["bhr_from_day1"] = round(bhr, 6) if bhr is not None else None

            # Total Return from Offer Price = (P_T / P_Offer) - 1
            tot_ret = ((p_end / offer_p) - 1.0) if offer_p and offer_p > 0 else None
            rec["total_return_from_offer"] = round(tot_ret, 6) if tot_ret is not None else None

            # 基准收益与财富相对比 (WR)
            hsi_end = hsi_map.get(target_bar["date"])
            r_hsi = ((hsi_end / hsi_base) - 1.0) if (hsi_base and hsi_end) else None
            rec["hsi_return"] = round(r_hsi, 6) if r_hsi is not None else None

            hstech_end = hstech_map.get(target_bar["date"])
            r_hstech = ((hstech_end / hstech_base) - 1.0) if (hstech_base and hstech_end) else None
            rec["hstech_return"] = round(r_hstech, 6) if r_hstech is not None else None

            # WR = (1 + R_firm) / (1 + R_bench)
            if bhr is not None and r_hsi is not None and (1.0 + r_hsi) != 0:
                rec["wr_hsi"] = round((1.0 + bhr) / (1.0 + r_hsi), 4)
            else:
                rec["wr_hsi"] = None

            if bhr is not None and r_hstech is not None and (1.0 + r_hstech) != 0:
                rec["wr_hstech"] = round((1.0 + bhr) / (1.0 + r_hstech), 4)
            else:
                rec["wr_hstech"] = None

            # 区间均成交额与 Amihud
            window_bars = bars[:req_days]
            to_vals = [b.get("turnover") or 0.0 for b in window_bars]
            avg_to = sum(to_vals) / len(to_vals) if to_vals else 0.0
            rec["avg_daily_turnover"] = round(avg_to, 2)

            # 区间平均 Amihud Illiquidity
            illiq_list = []
            for w_i, wb_item in enumerate(window_bars):
                p_c = wb_item["close"]
                p_prev = window_bars[w_i - 1]["close"] if w_i > 0 else offer_p or p_c
                w_to = wb_item.get("turnover") or 0.0
                if p_prev and w_to > 0:
                    illiq_list.append(abs(p_c - p_prev) / p_prev / w_to * 1e6)
            rec["amihud_mean"] = round(sum(illiq_list) / len(illiq_list), 6) if illiq_list else None

            # 流动性衰减率 (相对首日)
            rec["liquidity_decay_ratio"] = round(avg_to / day1_turnover, 6) if day1_turnover > 0 else None
            rec["missing_reason"] = None

            horizon_records.append(rec)

        return daily_records, horizon_records

    def run(self, issuers: list[dict[str, Any]]) -> tuple[Path, Path]:
        """批量执行全量面板构建。"""
        logger.info(f"Processing market panel for {len(issuers)} issuers...")
        # 预先拉取基准指数
        min_date = min((parse_bar_date(i["listing_date"]) for i in issuers if i.get("listing_date")), default=dt.date(2021, 1, 1))
        hsi_bars = self.fetch_benchmark_bars("^HSI", min_date)
        hstech_bars = self.fetch_benchmark_bars("^HSTECH", min_date)

        all_daily: list[dict[str, Any]] = []
        all_horizons: list[dict[str, Any]] = []

        for i in issuers:
            d_recs, h_recs = self.process_issuer(i, hsi_bars, hstech_bars)
            all_daily.extend(d_recs)
            all_horizons.extend(h_recs)

        # 导出逐日交易大表 (daily_market_panel.csv)
        daily_csv = self.out_master / "daily_market_panel.csv"
        if all_daily:
            d_keys = list(all_daily[0].keys())
            with daily_csv.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=d_keys)
                writer.writeheader()
                writer.writerows(all_daily)

        # 导出学术跨期表现汇总表 (horizon_summary.csv)
        horizon_csv = self.out_master / "horizon_summary.csv"
        h_keys = [
            "stock_code", "horizon", "horizon_desc", "target_trading_days", "matured",
            "target_date", "actual_date", "close_price", "bhr_from_day1", "total_return_from_offer",
            "hsi_return", "hstech_return", "wr_hsi", "wr_hstech", "avg_daily_turnover",
            "amihud_mean", "liquidity_decay_ratio", "missing_reason"
        ]
        if all_horizons:
            with horizon_csv.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=h_keys, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(all_horizons)

        logger.info(f"Market panel built: {len(all_daily)} daily bars, {len(all_horizons)} horizon records")
        return daily_csv, horizon_csv


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build the market panel for a configured IPO cohort")
    parser.add_argument("--workbook")
    parser.add_argument("--period-start")
    parser.add_argument("--period-end")
    args = parser.parse_args()
    cfg = load_cfg(args.workbook, args.period_start, args.period_end)
    engine = MarketPanelEngine(cfg=cfg)
    issuers = load_issuers(cfg=cfg)
    d_out, h_out = engine.run(issuers)
    print(f"\n=======================================================")
    print(f"Market & Microstructure Panel Construction Complete")
    print(f"=======================================================")
    print(f"Daily Market Panel : {d_out}")
    print(f"Horizon Summary    : {h_out}")
