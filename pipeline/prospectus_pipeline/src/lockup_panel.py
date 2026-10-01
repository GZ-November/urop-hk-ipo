#!/usr/bin/env python3
"""多重法定与契约解禁日程与事件窗影响面板 (Statutory & Contractual Lockup Panel).

基于香港主板制度现实与 Lowry, Michaely, & Volkova (2017) 股权限售与代理冲突框架：
  1. 梳理全量具有经济学实质的解禁时点（并非仅限于基石）：
     - 基石投资者 6 个月法定限售到期（Cornerstone 6M Statutory Expiry）；
     - 控股股东首阶段 6 个月绝对不得减持期满（Listing Rule 10.07(1)(a)）；
     - 控股股东次阶段 6 个月（累计12个月）不得放弃控制权期满（Listing Rule 10.07(1)(b)）；
     - 特专科技（Chapter 18C）资深独立投资者 12 个月锁定期；
     - 特专科技（Chapter 18C）控股股东 24 个月锁定期；
  2. 提取限售股数、占已发行股本比例、占自由流通盘（Free Float）比例；
  3. 构建解禁日前后三大微观结构事件窗：
     - [-20, +20] 交易日累计超额收益（CAR vs. HSI）与换手率异动；
     - [-5, +5] 交易日窗口高频价格吸收效率；
     - [0, +60] 交易日中长期筹码雪崩效应与实际冲击；
  4. 严格区分“解禁到期日”与“实际减持行为”，绝不预设解禁即等于必然抛售；
  5. 输出 master 交付物：out/master/lockup_events.csv。
"""
from __future__ import annotations

import argparse
import bisect
import csv
import datetime as dt
import logging
from pathlib import Path
from typing import Any, Optional


logger = logging.getLogger("lockup_panel")

ROOT = Path(__file__).resolve().parent.parent
sys_src = ROOT / "src"
import sys
if str(sys_src) not in sys.path:
    sys.path.insert(0, str(sys_src))

from as_of import resolve_as_of, truncate_bars
from market_fetcher import parse_bar_date
sys.path.insert(0, str(ROOT))
import master_contracts
from cohort import load_cfg
from market_observations import read_daily_market_panel
from date_windows import add_calendar_months  # noqa: F401 (compatibility re-export)


CONTRACTS_PATH = ROOT / "data" / "manual" / "lockup_contracts.json"

# Event categories derived from documents. No category receives a date unless a contract
# record states or formulaically implies it; there is no listing-date-plus-N-months default.
CATEGORY_ORDER = (
    "Cornerstone_Lockup",
    "Controlling_Shareholder_6M_Disposal",
    "Controlling_Shareholder_12M_Control",
)
CATEGORY_RULE_BASIS = {
    "Cornerstone_Lockup": "Cornerstone investment agreement lock-up (allotment announcement / prospectus)",
    "Controlling_Shareholder_6M_Disposal": "Listing Rule 10.07(1)(a) as undertaken in the prospectus",
    "Controlling_Shareholder_12M_Control": "Listing Rule 10.07(1)(b) as undertaken in the prospectus",
}


def load_lockup_contracts(path=None) -> dict[str, dict[str, Any]]:
    """Curated, evidence-bound lock-up records keyed by stock code ({} when the file is absent)."""
    import json
    path = Path(path) if path else CONTRACTS_PATH
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


class LockupPanelEngine:
    """法定与契约解禁事件面板引擎：日期只来自带证据的合同记录。"""

    def __init__(self, cfg: dict | None = None, as_of: Any = None, contracts: dict | None = None) -> None:
        self.cfg = cfg or load_cfg()
        self.as_of = resolve_as_of(as_of)
        self.contracts = load_lockup_contracts() if contracts is None else contracts
        self.out_master = self.cfg["paths"]["out"] / "master"
        self.daily_panel_csv = self.out_master / "daily_market_panel.csv"
        self.market_cache = self.cfg["paths"]["data"] / "market" / "daily_bars"
        self.out_master.mkdir(parents=True, exist_ok=True)
        self.daily_bars: dict[str, list[dict[str, Any]]] = {}
        self.hsi_map: dict[dt.date, float] = {}
        self._load_market_data()

    def _load_market_data(self) -> None:
        """加载已生成的个股及恒指日线数据，并按观察截止日截断。"""
        bars = read_daily_market_panel(self.daily_panel_csv)
        self.daily_bars = {code: truncate_bars(rows, self.as_of) for code, rows in bars.items()}
        hsi_cache = self.market_cache / "HSI_bars.json"
        if hsi_cache.exists():
            import json
            for b in json.loads(hsi_cache.read_text(encoding="utf-8")):
                day = parse_bar_date(b["date"])
                if day <= self.as_of:
                    self.hsi_map[day] = float(b["close"])

    def calculate_event_window_metrics(
        self,
        code: str,
        unlock_date: dt.date,
    ) -> tuple[Optional[float], Optional[float], Optional[float], Optional[float], str]:
        """计算解禁事件窗 [-20, +20], [-5, +5], [0, +60] 的 CAR 与成交量冲击比（含端点）。"""
        return self.window_metrics_detail(code, unlock_date)[:5]

    def window_metrics_detail(self, code: str, unlock_date: dt.date):
        """Window metrics plus a finer reason: (car20, car5, car60, vol_shock, status, detail).

        Windows need an actual stock bar and benchmark quote on every exchange-calendar day
        (the HSI calendar) from the preceding close to the endpoint. A suspension or cache gap
        yields missing data, never a shifted window, and bars after the cutoff never count.
        """
        import math
        as_of = getattr(self, "as_of", None) or resolve_as_of()
        bars = [b for b in self.daily_bars.get(code, []) if b["date"] <= as_of]
        if not bars:
            return None, None, None, None, "NO_TRADING_DATA", "no_bars_through_cutoff"
        if unlock_date > as_of:
            return None, None, None, None, "IMMATURE_WINDOW", "future_event_after_cutoff"

        calendar = sorted(day for day in self.hsi_map if day <= as_of)
        u_idx = None
        for i, b in enumerate(bars):
            if b["date"] >= unlock_date:
                u_idx = i
                break
        if u_idx is None:
            return None, None, None, None, "POST_UNLOCK_TRADING_MISSING", "no_stock_bar_on_or_after_event"
        # The first stock bar must be the first exchange trading day on/after the event date.
        if bisect.bisect_left(calendar, bars[u_idx]["date"]) - bisect.bisect_left(calendar, unlock_date) > 0:
            return None, None, None, None, "POST_UNLOCK_TRADING_MISSING", "stock_not_trading_on_event_day"

        reasons: dict[str, str] = {}

        def contiguous(start: int, end: int) -> bool:
            # A gap exists when the market traded on a day strictly between two consecutive stock bars.
            for i in range(start - 1, end):
                a, b = bars[i]["date"], bars[i + 1]["date"]
                if bisect.bisect_left(calendar, b) - bisect.bisect_right(calendar, a) > 0:
                    return False
            return True

        def car(start: int, end: int, label: str) -> Optional[float]:
            # CAR [a,b] 包含 a 与 b 两日收益，a 日基准收益需 a-1 的收盘价。
            if start < 1:
                reasons["INCOMPLETE_WINDOW"] = "insufficient_pre_event_history"
                return None
            if end >= len(bars):
                reasons["INCOMPLETE_WINDOW"] = "future_endpoint_after_cutoff" if (
                    not calendar or bars[-1]["date"] >= calendar[-1]) else "stock_bars_end_before_endpoint"
                return None
            if not contiguous(start, end):
                reasons["MISSING_RETURN_DATA"] = "stock_bar_gap_vs_exchange_calendar"
                return None
            total = 0.0
            for i in range(start, end + 1):
                r_stock = bars[i].get("daily_return")
                if r_stock is None or not math.isfinite(r_stock):
                    reasons["MISSING_RETURN_DATA"] = "missing_or_nonfinite_stock_return"
                    return None
                curr = self.hsi_map.get(bars[i]["date"])
                prev = self.hsi_map.get(bars[i - 1]["date"])
                if (curr is None or prev is None or not math.isfinite(curr)
                        or not math.isfinite(prev) or curr <= 0 or prev <= 0):
                    reasons["MISSING_BENCHMARK_DATA"] = "missing_or_invalid_benchmark_close"
                    return None
                total += r_stock - (curr / prev - 1.0)
            return round(total, 6)

        car_20 = car(u_idx - 20, u_idx + 20, "[-20,+20]")
        car_5 = car(u_idx - 5, u_idx + 5, "[-5,+5]")
        car_60 = car(u_idx, u_idx + 60, "[0,+60]")

        # 完整 [-20,-1] 与 [0,+20] 窗口；真实零成交额保留在均值分母中。
        vol_shock = None
        if u_idx >= 20 and u_idx + 20 < len(bars) and contiguous(u_idx - 20, u_idx + 20):
            pre_to = [b["turnover"] for b in bars[u_idx - 20:u_idx]]
            post_to = [b["turnover"] for b in bars[u_idx:u_idx + 21]]
            if all(t is not None and math.isfinite(t) and t >= 0 for t in pre_to + post_to):
                avg_pre = sum(pre_to) / len(pre_to)
                avg_post = sum(post_to) / len(post_to)
                vol_shock = round(avg_post / avg_pre, 4) if avg_pre > 0 else None
        if vol_shock is None:
            reasons.setdefault("INCOMPLETE_WINDOW", "incomplete_turnover_window")
        status = next((r for r in ("MISSING_BENCHMARK_DATA", "MISSING_RETURN_DATA", "INCOMPLETE_WINDOW")
                       if r in reasons), "MATURED")
        detail = reasons.get(status, "complete_windows") if status != "MATURED" else "complete_windows"
        return car_20, car_5, car_60, vol_shock, status, detail

    def process_issuer_lockups(self, issuer: dict[str, Any]) -> list[dict[str, Any]]:
        """Build one row per evidenced lock-up event; flag missing contractual evidence explicitly."""
        code = issuer["stock_code"]
        l_date_str = issuer.get("listing_date")
        if not l_date_str:
            return []
        contract = self.contracts.get(code) or {}
        by_category: dict[str, list[dict[str, Any]]] = {}
        for ev in contract.get("events", []):
            by_category.setdefault(ev["category"], []).append(ev)

        rows: list[dict[str, Any]] = []
        categories = list(CATEGORY_ORDER) + [c for c in by_category if c not in CATEGORY_ORDER]
        for category in categories:
            events = by_category.get(category) or [None]
            for ev in events:
                base = {
                    "stock_code": code,
                    "company_name": issuer.get("company_name", ""),
                    "lockup_category": category,
                    "as_of": self.as_of.isoformat(),
                }
                if ev is None or not ev.get("first_free_day"):
                    rows.append({**base,
                                 "lockup_target_entity": (ev or {}).get("holder", ""),
                                 "expiry_date": "", "last_restricted_day": "",
                                 "statutory_rule_basis": CATEGORY_RULE_BASIS.get(category, ""),
                                 "evidence_status": "no_contract_evidence" if ev is None else ev.get("review", "unreviewed"),
                                 "locked_pct_approx": None, "locked_shares": None,
                                 "car_m20_p20": None, "car_m5_p5": None, "car_0_p60": None,
                                 "volume_shock_ratio": None,
                                 "window_status": "MISSING_CONTRACTUAL_EVIDENCE",
                                 "window_detail": "no_dated_contract_record"})
                    continue
                first_free = dt.date.fromisoformat(ev["first_free_day"])
                car20, car5, car60, vol, status, detail = self.window_metrics_detail(code, first_free)
                rows.append({**base,
                             "lockup_target_entity": ev.get("holder", ""),
                             "expiry_date": str(first_free),
                             "last_restricted_day": ev.get("last_restricted_day", ""),
                             "statutory_rule_basis": CATEGORY_RULE_BASIS.get(category, ev.get("term", "")),
                             "evidence_status": ev.get("review", "unreviewed"),
                             "locked_pct_approx": ev.get("pct_issued_shares"),
                             "locked_shares": ev.get("shares_restricted"),
                             "car_m20_p20": car20, "car_m5_p5": car5, "car_0_p60": car60,
                             "volume_shock_ratio": vol,
                             "window_status": status, "window_detail": detail})
        return rows

    def run(self, issuers: list[dict[str, Any]]) -> Path:
        """全量解析并导出。"""
        all_events = []
        for iss in issuers:
            events = self.process_issuer_lockups(iss)
            all_events.extend(events)

        out_path = self.out_master / master_contracts.LOCKUP_EVENTS
        if all_events:
            keys = list(dict.fromkeys(k for row in all_events for k in row))
            with out_path.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=keys)
                writer.writeheader()
                writer.writerows(all_events)

        logger.info(f"Lockup events written to {out_path} ({len(all_events)} events across {len(issuers)} issuers)")
        return out_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build lockup events for a configured IPO cohort")
    parser.add_argument("--workbook")
    parser.add_argument("--period-start")
    parser.add_argument("--period-end")
    parser.add_argument("--as-of", default=None, help="观察截止日 YYYY-MM-DD（默认 PIPELINE_AS_OF 或今日）")
    args = parser.parse_args()
    cfg = load_cfg(args.workbook, args.period_start, args.period_end)
    from market_panel import load_issuers
    issuers = load_issuers(cfg=cfg)
    engine = LockupPanelEngine(cfg=cfg, as_of=args.as_of)
    out = engine.run(issuers)
    print(f"\nLockup Panel Complete: {out}")
