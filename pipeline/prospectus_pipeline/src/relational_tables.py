#!/usr/bin/env python3
"""机构投资者与承销辛迪加实体级关系数据库生成引擎 (Relational Investor & Syndicate Tables).

依据实证金融文献 (Gompers 1996, Megginson-Weiss 1991, Corwin-Schultz 2005):
  1. 将非结构化文本拆解为规范的实体关系表：
     - 投资者关系表 (investor_relational.csv)：
       涵盖基石投资者 (Cornerstone)、Pre-IPO VC/PE 机构、国家队/地方国资 (State/Gov)、
       企业战投 (CVC)、跨界基金 (Crossover Fund, 兼具 Pre-IPO 与基石双重身份)；
       记录标准化统一机构 ID (investor_id)、母集团归属、配售股数、解禁日期、董事会席位。
     - 承销辛迪加关系表 (underwriter_relational.csv)：
       涵盖独家/联席保荐人 (Sponsor)、整体协调人 (OC)、全球协调人 (GC)、账簿管理人 (Bookrunner)、
       稳价经理人 (Stabilizing Manager)；
       记录机构统一代号、佣金费率分成、酌情奖励费 (Discretionary Incentive Fee) 与商业银行关联性。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import logging
import math
import re
from pathlib import Path
from typing import Any, Optional

import openpyxl

logger = logging.getLogger("relational_tables")

ROOT = Path(__file__).resolve().parent.parent
sys_src = ROOT / "src"
import sys
if str(sys_src) not in sys.path:
    sys.path.insert(0, str(sys_src))

from market_fetcher import parse_bar_date
sys.path.insert(0, str(ROOT))
import master_contracts
from cohort import load_cfg


def clean_str(s: Any) -> str:
    return str(s or "").strip()


def normalize_ws(s: str) -> str:
    """折叠 PDF 抽取带来的换行与多余空白。"""
    return " ".join(str(s or "").split())


# 上游曾写入的占位符（非真实机构名），读入时视为缺失
PLACEHOLDER_MARKERS = ("sponsor-oc",)


def commission_pct(raw: Any) -> Optional[float]:
    """招股书佣金率 (schema unit=decimal，如 0.015) → 百分点 (1.5)。

    输出列名为 *_pct，下游 expansion_mapping 再 /100 写成 Excel 百分比；
    缺失、非数值或不在 [0, 1] 的值返回 None（不猜测单位，也不以行业惯例代填）。
    """
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(v) or not 0.0 <= v <= 1.0:
        return None
    return round(v * 100.0, 6)


def split_sponsors(raw: Any) -> list[str]:
    """按 / 或 ; 拆分保荐人名单；换行只是 PDF 折行，不是分隔符。"""
    names = (normalize_ws(s) for s in re.split(r"[/;]+", str(raw or "")))
    return [n for n in names if len(n) > 3]


def slugify(name: str) -> str:
    """生成紧凑的实体标识符。"""
    clean = re.sub(r"[^A-Za-z0-9]+", "_", name.strip().upper()).strip("_")
    return clean[:30] if clean else "ENTITY_UNKNOWN"


class RelationalTableEngine:
    """机构投资者与承销辛迪加关系生成引擎。"""

    def __init__(self, cfg: dict | None = None) -> None:
        self.cfg = cfg or load_cfg()
        self.out_master = self.cfg["paths"]["out"] / "master"
        self.extracted_dir = self.cfg["paths"]["out"] / "extracted"
        self.allot_extracted_dir = self.cfg["paths"]["allot_out"] / "extracted"
        self.stabilization_csv = self.out_master / "stabilization_events.csv"
        self.issuer_master_csv = self.out_master / "issuer_master.csv"
        self.out_master.mkdir(parents=True, exist_ok=True)
        self.stabilizing_managers: dict[str, str] = {}
        self.issuer_sponsors: dict[str, str] = {}
        self._load_stabilization_data()
        self._load_issuer_sponsors()

    def _load_stabilization_data(self) -> None:
        if not self.stabilization_csv.exists():
            return
        with self.stabilization_csv.open("r", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for r in reader:
                mgr = normalize_ws(r.get("stabilizing_manager"))
                if any(m in mgr.lower() for m in PLACEHOLDER_MARKERS):
                    logger.warning(f"{r['stock_code']}: ignoring placeholder stabilizing manager {mgr!r}")
                    mgr = ""
                self.stabilizing_managers[r["stock_code"]] = mgr

    def _load_issuer_sponsors(self) -> None:
        """保荐人名单取自 issuer_master.csv（HKEX New Listing Report 的 Sponsor 栏）。

        load_issuers() 不带 sponsors 键；缺此来源时该发行人不产生保荐人行。
        """
        if not self.issuer_master_csv.exists():
            return
        with self.issuer_master_csv.open("r", encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                if r.get("sponsors"):
                    self.issuer_sponsors[r["stock_code"]] = r["sponsors"]

    def process_investors(self, issuers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """构建标准化机构投资者关系表。"""
        investor_records: list[dict[str, Any]] = []

        for iss in issuers:
            code = iss["stock_code"]
            digits = "".join(ch for ch in code if ch.isdigit())
            l_date = iss.get("listing_date")
            p_json_path = self.extracted_dir / f"HKIPO-MB{digits}.json"
            
            cs_names_raw = ""
            pre_ipo_raw = ""
            vc_backed = 0
            pe_backed = 0
            gov_backed = 0
            has_board_seat = 0

            if p_json_path.exists():
                try:
                    p_data = json.loads(p_json_path.read_text(encoding="utf-8"))
                    fields = p_data.get("fields", {})
                    cs_names_raw = clean_str(fields.get("col_CJ", {}).get("value"))
                    pre_ipo_raw = clean_str(fields.get("col_pre_ipo_investors", {}).get("value"))
                    vc_backed = int(fields.get("col_vc_backed", {}).get("value") or 0)
                    pe_backed = int(fields.get("col_pe_backed", {}).get("value") or 0)
                    gov_backed = int(fields.get("col_gov_backed", {}).get("value") or 0)
                    has_board_seat = int(fields.get("col_vc_board_seat", {}).get("value") or 0)
                except Exception:
                    pass

            # 1. 解析基石投资者 (Cornerstone)
            if cs_names_raw and cs_names_raw.lower() not in ("none", "nan", "0", ""):
                # 分割基石名称（常见分隔符为分号、换行、逗号）
                cs_list = [n.strip() for n in re.split(r"[;\n,、]+", cs_names_raw) if len(n.strip()) > 2]
                for cs in cs_list:
                    # 识别是否国资/地方政府引导基金
                    is_gov = bool(re.search(r"(guoxin|state|fund|asset|municipal|sasac|investment|capital|国资|产业|政府)", cs, re.I))
                    is_cross = bool(re.search(r"(crossover|hillhouse|boyu|matrix|qiming|sequoia)", cs, re.I))
                    ent_id = f"INV_{slugify(cs)}"
                    investor_records.append({
                        "stock_code": code,
                        "company_name": iss.get("company_name", ""),
                        "investor_id": ent_id,
                        "standardized_name": cs,
                        "disclosed_name": cs,
                        "investor_category": "Cornerstone",
                        "ultimate_parent": cs.split()[0] if cs else "",
                        "state_owned_flag": is_gov,
                        "pre_ipo_flag": is_cross,
                        "cornerstone_flag": True,
                        "crossover_flag": is_cross,
                        "shares_allocated": None,
                        "allocation_value_hkd": None,
                        "pct_of_base_offer": None,
                        "investment_round": "IPO Cornerstone",
                        "lockup_expiry_date": str(parse_bar_date(l_date) + dt.timedelta(days=183)) if l_date else None,
                        "board_seat_flag": False,
                        "source_evidence": "Prospectus Cornerstone Chapter / Col CJ"
                    })

            # 2. 解析 Pre-IPO 机构投资者
            if pre_ipo_raw and pre_ipo_raw.lower() not in ("none", "nan", "0", ""):
                pre_list = [n.strip() for n in re.split(r"[;\n,、]+", pre_ipo_raw) if len(n.strip()) > 2]
                for pre_inv in pre_list:
                    cat = "Pre-IPO VC" if vc_backed else ("Pre-IPO PE" if pe_backed else "Pre-IPO Strategic")
                    is_gov = bool(gov_backed) or bool(re.search(r"(state|guoxin|sasac|capital|fund|国投|深创投)", pre_inv, re.I))
                    ent_id = f"INV_{slugify(pre_inv)}"
                    investor_records.append({
                        "stock_code": code,
                        "company_name": iss.get("company_name", ""),
                        "investor_id": ent_id,
                        "standardized_name": pre_inv,
                        "disclosed_name": pre_inv,
                        "investor_category": cat,
                        "ultimate_parent": pre_inv.split()[0] if pre_inv else "",
                        "state_owned_flag": is_gov,
                        "pre_ipo_flag": True,
                        "cornerstone_flag": False,
                        "crossover_flag": False,
                        "shares_allocated": None,
                        "allocation_value_hkd": None,
                        "pct_of_base_offer": None,
                        "investment_round": "Pre-IPO Series",
                        "lockup_expiry_date": str(parse_bar_date(l_date) + dt.timedelta(days=183)) if l_date else None,
                        "board_seat_flag": bool(has_board_seat),
                        "source_evidence": "Prospectus History Chapter / Pre-IPO Disclosure"
                    })

        return investor_records

    def process_syndicate(self, issuers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """构建承销辛迪加投行中介机构关系表。"""
        syndicate_records: list[dict[str, Any]] = []

        # 商业银行系投行名单（用于检验 Idea 10 信贷关系认证假说）
        COMMERCIAL_BANKS = (
            "cicc", "boc", "boci", "ccb", "icbc", "abc", "spdb", "cmb", "hsbc",
            "standard chartered", "citigroup", "jpmorgan", "mizuho", "ping an"
        )

        for iss in issuers:
            code = iss["stock_code"]
            digits = "".join(ch for ch in code if ch.isdigit())
            sponsors_raw = iss.get("sponsors") or self.issuer_sponsors.get(code, "")
            stab_mgr = self.stabilizing_managers.get(code, "")

            # 读取招股书佣金费率（百分点）；无抽取值则为 None
            comm_hk = None
            comm_int = None
            p_json_path = self.extracted_dir / f"HKIPO-MB{digits}.json"
            if p_json_path.exists():
                try:
                    p_data = json.loads(p_json_path.read_text(encoding="utf-8"))
                    fields = p_data.get("fields", {})
                    c_hk_val = fields.get("col_AO", {}).get("value")
                    c_int_val = fields.get("col_AP", {}).get("value")
                    comm_hk = commission_pct(c_hk_val)
                    comm_int = commission_pct(c_int_val)
                    for key, raw, val in (("col_AO", c_hk_val, comm_hk), ("col_AP", c_int_val, comm_int)):
                        if raw not in (None, "") and val is None:
                            logger.warning(f"{code}: {key}={raw!r} is not a decimal rate in [0, 1]; left blank")
                except Exception:
                    pass

            # 酌情奖励费：招股书尚无对应抽取字段，不得以行业惯例 (0.5%-1.5%) 代填
            incentive = None

            def total_fee(base: Optional[float]) -> Optional[float]:
                if base is None or incentive is None:
                    return None
                return round(base + incentive, 6)

            # 拆分联席保荐人名单
            sponsors = split_sponsors(sponsors_raw)
            for idx, sp in enumerate(sponsors):
                is_sole = (len(sponsors) == 1)
                role = "Sole Sponsor" if is_sole else "Joint Sponsor"
                is_bank = any(b in sp.lower() for b in COMMERCIAL_BANKS)
                ent_id = f"IB_{slugify(sp)}"

                syndicate_records.append({
                    "stock_code": code,
                    "company_name": iss.get("company_name", ""),
                    "intermediary_id": ent_id,
                    "intermediary_name": sp,
                    "syndicate_role": role,
                    "role_rank": 1,
                    "base_commission_pct": comm_hk,
                    "discretionary_incentive_fee_pct": incentive,
                    "total_fee_rate_pct": total_fee(comm_hk),
                    "commercial_bank_affiliate": is_bank,
                    "is_stabilizing_manager": (sp.lower() in stab_mgr.lower() if stab_mgr else False),
                    "source_evidence": "HKEX New Listing Report Sponsor Field / Prospectus Underwriting"
                })

            # 若有单独的稳价经理人且未在保荐人中列出
            if stab_mgr and not any(stab_mgr.lower() in s.lower() for s in sponsors):
                is_bank = any(b in stab_mgr.lower() for b in COMMERCIAL_BANKS)
                ent_id = f"IB_{slugify(stab_mgr)}"
                syndicate_records.append({
                    "stock_code": code,
                    "company_name": iss.get("company_name", ""),
                    "intermediary_id": ent_id,
                    "intermediary_name": stab_mgr,
                    "syndicate_role": "Stabilizing Manager",
                    "role_rank": 2,
                    "base_commission_pct": comm_int,
                    "discretionary_incentive_fee_pct": incentive,
                    "total_fee_rate_pct": total_fee(comm_int),
                    "commercial_bank_affiliate": is_bank,
                    "is_stabilizing_manager": True,
                    "source_evidence": "HKEX Section 9(2) Price Stabilizing Announcement"
                })

        return syndicate_records

    def run(self, issuers: list[dict[str, Any]]) -> tuple[Path, Path]:
        """生成并导出两张实体关系表。"""
        # 1. 投资者表
        inv_recs = self.process_investors(issuers)
        inv_path = self.out_master / master_contracts.INVESTOR_RELATIONAL
        if inv_recs:
            keys = list(inv_recs[0].keys())
            with inv_path.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=keys)
                writer.writeheader()
                writer.writerows(inv_recs)

        # 2. 承销辛迪加表
        syn_recs = self.process_syndicate(issuers)
        syn_path = self.out_master / master_contracts.UNDERWRITER_RELATIONAL
        if syn_recs:
            keys = list(syn_recs[0].keys())
            with syn_path.open("w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.DictWriter(fh, fieldnames=keys)
                writer.writeheader()
                writer.writerows(syn_recs)

        logger.info(f"Relational tables written: {len(inv_recs)} investor records, {len(syn_recs)} syndicate records")
        return inv_path, syn_path


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build relational tables for a configured IPO cohort")
    parser.add_argument("--workbook")
    parser.add_argument("--period-start")
    parser.add_argument("--period-end")
    args = parser.parse_args()
    cfg = load_cfg(args.workbook, args.period_start, args.period_end)
    from market_panel import load_issuers
    issuers = load_issuers(cfg=cfg)
    engine = RelationalTableEngine(cfg=cfg)
    i_out, s_out = engine.run(issuers)
    print(f"\n=======================================================")
    print(f"Relational Tables Generation Complete")
    print(f"=======================================================")
    print(f"Investor Relational Table    : {i_out}")
    print(f"Underwriter Relational Table : {s_out}")
