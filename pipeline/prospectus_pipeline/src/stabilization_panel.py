#!/usr/bin/env python3
"""稳价行动、绿鞋超额配售与稳价结束“断崖效应”事件面板 (Price Stabilization & Greenshoe Event Panel).

依据香港《证券及期货（价格稳定）规则》（第 571W 章）第 9(2) 条法定披露要求：
  1. 结构化抽取稳价期起止日、稳价经理人、场内托单购买（价格区间、股数、金额）；
  2. 结构化抽取超额配售权（绿鞋）行使日期、行使股数、行使比例或失效未经行使事实；
  3. 构建托单支撑与稳价到期事件窗：
     - 稳价结束日前后 [-5, +5] 交易日累计超额收益与回撤（测试“托单断崖效应”）；
     - 稳价结束日至后 20 个交易日 [0, +20] 流动性衰减与跌幅；
  4. 输出 master 交付物：out/master/stabilization_events.csv。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import logging
import re
from pathlib import Path
from typing import Any, Optional

import openpyxl

logger = logging.getLogger("stabilization_panel")

ROOT = Path(__file__).resolve().parent.parent
sys_src = ROOT / "src"
import sys
if str(sys_src) not in sys.path:
    sys.path.insert(0, str(sys_src))

from market_fetcher import parse_bar_date

sys.path.insert(0, str(ROOT))
import master_contracts
from cohort import load_cfg
from market_observations import read_daily_market_panel

NUM = r"\d{1,3}(?:,\d{3})+|\d{4,}"
FLOAT_NUM = r"\d+(?:\.\d+)?"

# 稳价经理人：公告常见两种句式；均不命中时留空（不得以保荐人或默认券商代填）
RE_MANAGER = re.compile(r"(?:undertaken|borrowed)\s+by\s+([^,]+?),\s*(?:the\s+)?Stabili[sz](?:ing|ation)\s+Manager", re.I)
RE_MANAGER_AS = re.compile(
    r"In\s+connection\s+with\s+the\s+Global\s+Offering,\s+([^.;]{3,150}?)"
    r"(?:\s*\(or\s+(?:its|any)[^)]*\))?,?\s+as\s+(?:the\s+)?stabili[sz](?:ing|ation)\s+manager\b", re.I)
RE_NO_MANAGER = re.compile(r"No\s+stabili[sz](?:ing|ation)\s+manager\s+(?:will\s+be|has\s+been|was)\s+appointed", re.I)
# 从公告文本解析的字段；未命中者列入输出行的 missing_fields，便于审计
PARSED_FIELDS = (
    "stabilizing_manager", "stabilization_period_end", "stabilization_purchases_occurred",
    "over_allocation_shares", "over_allocation_pct", "stock_borrowing_arrangement",
    "option_exercise_date", "shares_issued_under_option", "exercise_pct_of_option",
    "expired_unexercised",
)
RE_NO_PURCHASE = re.compile(r"no\s+(?:purchase|sale)\s+(?:or\s+sale\s+)?of\s+any\s+(?:H\s+|Offer\s+)?Shares\s+on\s+the\s+market\s+for\s+the\s+purpose\s+of\s+price\s+stabilization", re.I)
RE_PURCHASE_RANGE = re.compile(rf"price\s+range\s+of\s+HK\$\s*({FLOAT_NUM})\s+to\s+HK\$\s*({FLOAT_NUM})", re.I)
RE_OVER_ALLOC = re.compile(rf"over-?allocations?\s+of\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:H\s+|Offer\s+)?Shares", re.I)
RE_OVER_PCT = re.compile(r"representing\s+(?:approximately\s+)?([\d.]+)\s*%\s+of\s+the\s+(?:total\s+number\s+of\s+)?(?:Offer\s+|H\s+)?Shares", re.I)
RE_BORROW = re.compile(r"(stock\s+borrowing\s+agreement|delayed\s+delivery)", re.I)
RE_EXERCISE_SHARES = re.compile(rf"(?:fully|partially)\s+exercised.*?in\s+respect\s+of\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+|Offer\s+)?Shares", re.I | re.S)
RE_EXERCISE_DATE = re.compile(r"(?:on|dated)\s+([A-Z][a-z]+day,\s+[A-Z][a-z]+\s+\d{1,2},\s+202\d)", re.I)
RE_END_STAB = re.compile(r"stabilization\s+period\s+in\s+connection\s+with\s+the\s+Global\s+Offering\s+ended\s+on\s+([A-Z][a-z]+day,\s+[A-Z][a-z]+\s+\d{1,2},\s+202\d)", re.I)


def parse_date_str(s: str) -> Optional[dt.date]:
    """解析如 Wednesday, January 28, 2026 的英文长日期。"""
    # 剔除星期
    s_clean = re.sub(r"^[A-Z][a-z]+day,\s*", "", s.strip())
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s_clean, fmt).date()
        except ValueError:
            pass
    return None


def normalize_ws(s: str) -> str:
    """折叠 PDF 抽取带来的换行与多余空白。"""
    return " ".join(s.split())


def extract_manager(text: str) -> Optional[str]:
    """从公告文本抽取稳价经理人名称；未披露或未命中返回 None。"""
    for pattern in (RE_MANAGER, RE_MANAGER_AS):
        m = pattern.search(text)
        if m:
            return normalize_ws(m.group(1))
    return None


class StabilizationPanelEngine:
    """稳价事件分析与断崖效应测算器。"""

    def __init__(self, cfg: dict | None = None) -> None:
        self.cfg = cfg or load_cfg()
        self.out_master = self.cfg["paths"]["out"] / "master"
        self.greenshoe_text_dir = self.cfg["paths"]["allot_out"] / "greenshoe" / "text"
        self.allot_text_dir = self.cfg["paths"]["allot_out"] / "text"
        self.greenshoe_index = self.cfg["paths"]["allot_out"] / "greenshoe.json"
        self.daily_panel_csv = self.out_master / "daily_market_panel.csv"
        self.out_master.mkdir(parents=True, exist_ok=True)
        self.daily_bars: dict[str, list[dict[str, Any]]] = {}
        self._load_daily_panel()

    def _load_daily_panel(self) -> None:
        """加载已生成的逐日行情大表以计算事件窗回报。"""
        self.daily_bars = read_daily_market_panel(self.daily_panel_csv)

    def parse_announcement(self, code: str, listing_date_str: str) -> dict[str, Any]:
        """解析公告文本并提取结构化字段。"""
        digits = "".join(ch for ch in code if ch.isdigit())
        g_file = self.greenshoe_text_dir / f"HKIPO-MB{digits}.jsonl"
        a_file = self.allot_text_dir / f"HKIPO-MB{digits}.jsonl"

        text_corpus = ""
        source_label = None
        if g_file.exists():
            source_label = "HKEXnews Section 9(2) Announcement (Ch 571W)"
            with g_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    p = json.loads(line)
                    text_corpus += " " + p.get("text", "")
        elif a_file.exists():
            source_label = "HKEXnews Allotment Results Announcement"
            with a_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    p = json.loads(line)
                    text_corpus += " " + p.get("text", "")
        has_text = bool(text_corpus.strip())
        lower = text_corpus.lower()

        # 以下各字段缺来源一律为 None：不以保荐人、法定期限推算或行业惯例值代填。
        # 稳价经理人
        manager = extract_manager(text_corpus)
        if manager:
            manager_status = "PARSED"
        elif not has_text:
            manager_status = "NO_SOURCE_TEXT"
        elif RE_NO_MANAGER.search(text_corpus):
            manager_status = "NOT_APPOINTED"
        else:
            manager_status = "NOT_FOUND"
        if manager_status in ("NO_SOURCE_TEXT", "NOT_FOUND"):
            logger.warning(f"{code}: stabilizing manager not parsed ({manager_status}); left blank")

        # 稳价结束日（只取公告明文；不按上市日 +30 天推算）
        end_match = RE_END_STAB.search(text_corpus)
        stab_end_date = parse_date_str(end_match.group(1)) if end_match else None

        # 是否有场内托单购买（公告未涉及时为未知，而非 False）
        no_purchase = bool(RE_NO_PURCHASE.search(text_corpus))
        if "no purchase" in lower or "stabilizing actions" in lower:
            purchases_occurred = not no_purchase
        else:
            purchases_occurred = None

        # 购买价格区间
        p_low, p_high = None, None
        range_match = RE_PURCHASE_RANGE.search(text_corpus)
        if range_match:
            p_low = float(range_match.group(1))
            p_high = float(range_match.group(2))

        # 超额配售股份数
        alloc_match = RE_OVER_ALLOC.search(text_corpus)
        alloc_shares = float(alloc_match.group(1).replace(",", "")) if alloc_match else None

        pct_match = RE_OVER_PCT.search(text_corpus)
        alloc_pct = float(pct_match.group(1)) if pct_match else None

        # 借股或延期交付安排
        borrow_match = RE_BORROW.search(text_corpus)
        borrow_str = "Delayed delivery arrangement / Stock borrowing" if borrow_match else None

        # 绿鞋行使情况
        ex_match = RE_EXERCISE_SHARES.search(text_corpus)
        ex_match_shares = float(ex_match.group(1).replace(",", "")) if ex_match else None
        ex_date_match = RE_EXERCISE_DATE.search(text_corpus)
        ex_date = parse_date_str(ex_date_match.group(1)) if ex_date_match else None

        if "full exercise" in lower or "fully exercised" in lower:
            ex_shares = alloc_shares or ex_match_shares
            ex_pct = 100.0
            expired = False
        elif "partial exercise" in lower or "partially exercised" in lower:
            ex_shares = ex_match_shares
            ex_pct = round((ex_shares / alloc_shares * 100.0), 2) if (ex_shares is not None and alloc_shares) else None
            expired = False
        elif "lapse" in lower or "not be exercised" in lower or "not exercised" in lower:
            ex_shares = 0.0
            ex_pct = 0.0
            expired = True
        else:
            # 公告未披露行使结果：未知
            ex_shares = None
            ex_pct = None
            expired = None

        # 截取证据引用
        quote_snip = ""
        if end_match:
            start_i = max(0, end_match.start() - 50)
            quote_snip = text_corpus[start_i:start_i + 250].replace("\n", " ").strip()
        elif "stabilization" in lower:
            idx = lower.find("stabilization")
            quote_snip = text_corpus[idx:idx + 250].replace("\n", " ").strip()

        rec = {
            "stock_code": code,
            "stabilizing_manager": manager,
            "stabilization_period_start": listing_date_str,
            "stabilization_period_end": str(stab_end_date) if stab_end_date else None,
            "stabilization_purchases_occurred": purchases_occurred,
            "purchase_price_low": p_low,
            "purchase_price_high": p_high,
            "aggregate_stabilization_shares": 0.0 if purchases_occurred is False else None,
            "over_allocation_shares": alloc_shares,
            "over_allocation_pct": alloc_pct,
            "stock_borrowing_arrangement": borrow_str,
            "option_exercise_date": str(ex_date) if ex_date else None,
            "shares_issued_under_option": ex_shares,
            "exercise_pct_of_option": ex_pct,
            "expired_unexercised": expired,
            "announcement_date": str(stab_end_date) if stab_end_date else None,
            "source_url": source_label,
            "evidence_quote": quote_snip[:200],
            "stabilizing_manager_status": manager_status,
        }
        rec["missing_fields"] = ";".join(k for k in PARSED_FIELDS if rec[k] is None)
        return rec

    def compute_event_windows(self, rec: dict[str, Any]) -> dict[str, Any]:
        """测算稳价期结束断崖效应（Cliff Effect）。"""
        code = rec["stock_code"]
        end_d_str = rec.get("stabilization_period_end")
        bars = self.daily_bars.get(code, [])
        if not end_d_str or not bars:
            rec["cliff_return_m5_p5"] = None
            rec["post_stab_return_p20"] = None
            rec["volume_decay_post_stab"] = None
            return rec

        end_d = parse_bar_date(end_d_str)
        # 寻找在 end_d 当日或最近的 bar 索引
        end_idx = None
        for i, b in enumerate(bars):
            if b["date"] >= end_d:
                end_idx = i
                break

        if end_idx is None:
            rec["cliff_return_m5_p5"] = None
            rec["post_stab_return_p20"] = None
            rec["volume_decay_post_stab"] = None
            return rec

        # [-5, +5] 窗口收益率
        idx_m5 = max(0, end_idx - 5)
        idx_p5 = min(len(bars) - 1, end_idx + 5)
        p_m5 = bars[idx_m5]["close"]
        p_p5 = bars[idx_p5]["close"]
        rec["cliff_return_m5_p5"] = round((p_p5 / p_m5) - 1.0, 6) if p_m5 > 0 else None

        # [0, +20] 稳价后 20 日表现
        idx_p20 = min(len(bars) - 1, end_idx + 20)
        p_0 = bars[end_idx]["close"]
        p_p20 = bars[idx_p20]["close"]
        rec["post_stab_return_p20"] = round((p_p20 / p_0) - 1.0, 6) if p_0 > 0 else None

        # 稳价期内日均成交额 vs 稳价后 20 日日均成交额
        pre_turnovers = [b["turnover"] for b in bars[:end_idx + 1] if b["turnover"] > 0]
        post_turnovers = [b["turnover"] for b in bars[end_idx + 1:idx_p20 + 1] if b["turnover"] > 0]
        avg_pre = sum(pre_turnovers) / len(pre_turnovers) if pre_turnovers else 0.0
        avg_post = sum(post_turnovers) / len(post_turnovers) if post_turnovers else 0.0
        rec["volume_decay_post_stab"] = round(avg_post / avg_pre, 6) if avg_pre > 0 else None

        return rec

    def run(self, issuers: list[dict[str, Any]]) -> Path:
        """全量解析并导出。"""
        out_records = []
        for iss in issuers:
            code = iss["stock_code"]
            l_date = iss.get("listing_date")
            rec = self.parse_announcement(code, l_date)
            rec = self.compute_event_windows(rec)
            out_records.append(rec)

        out_path = self.out_master / master_contracts.STABILIZATION_EVENTS
        if out_records:
            keys = list(out_records[0].keys())
            with out_path.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=keys)
                writer.writeheader()
                writer.writerows(out_records)

        logger.info(f"Stabilization events written to {out_path} ({len(out_records)} issuers)")
        return out_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build stabilization events for a configured IPO cohort")
    parser.add_argument("--workbook")
    parser.add_argument("--period-start")
    parser.add_argument("--period-end")
    args = parser.parse_args()
    cfg = load_cfg(args.workbook, args.period_start, args.period_end)
    from market_panel import load_issuers
    issuers = load_issuers(cfg=cfg)
    engine = StabilizationPanelEngine(cfg=cfg)
    out = engine.run(issuers)
    print(f"\nStabilization Panel Complete: {out}")
