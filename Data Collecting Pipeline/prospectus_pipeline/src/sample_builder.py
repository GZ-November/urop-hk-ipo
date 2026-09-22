#!/usr/bin/env python3
"""香港主板多年度新股全景样本构建引擎 (Multi-Year HK IPO Master Sample Builder).

功能：
  1. 解析 HKEX 官方 New Listing Report (NLR2021 到 NLR2026_Eng.xlsx)；
  2. 严格遵循实证金融文献 (Lowry, Michaely, & Volkova 2017) 与港交所上市规则：
     - 明确记录每一家候选上市公司的纳入/剔除法定原因 (inclusion_status, exclusion_reason)；
     - 剔除 GEM 转主板 (Chapter 9A, 无一级市场公开发行)；
     - 剔除 SPAC 发售与 De-SPAC 并购上市 (Chapter 18B)；
     - 剔除 介绍上市 (Listing by Introduction, 无募集资金)；
     - 准确标记 Chapter 18A (未盈利生物科技), Chapter 18C (特专科技), Chapter 8A (WVR 同股不同权), Chapter 19A (H股 / A+H 两地上市)；
     - 划分 FINI 数字化结算前 (Pre-FINI) 与结算后 (Post-FINI, 2023年11月22日生效) 监管制度窗口。
  3. 输出标准样本构建清单 (sample_construction.csv) 与主板新股 Master 基础信息表 (issuer_master.csv / json)。
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import logging
from pathlib import Path
from typing import Any, Optional

import openpyxl

logger = logging.getLogger("sample_builder")

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT.parent / "sources"
OUT_MASTER = ROOT / "out" / "master"

# FINI 官方上线实施日：2023 年 11 月 22 日
FINI_CUTOFF_DATE = dt.date(2023, 11, 22)
# 2025 年定价与发售机制改革分界点
REFORM_2025_DATE = dt.date(2025, 1, 1)


def parse_date(v: Any) -> Optional[dt.date]:
    """安全解析日期对象。"""
    if v is None:
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(s[:10], fmt).date()
        except ValueError:
            pass
    return None


def clean_code(raw: Any) -> str:
    """标准化 4/5 位港股代码为 0000.HK 格式。"""
    digits = "".join(ch for ch in str(raw or "") if ch.isdigit())
    if not digits:
        return str(raw or "").strip()
    return f"{int(digits):04d}.HK"


def to_float(v: Any) -> Optional[float]:
    """安全转换为浮点数。"""
    if v is None:
        return None
    s = str(v).replace(",", "").replace("$", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def load_nlr_candidates(filepath: Path, cohort_year: int) -> list[dict[str, Any]]:
    """解析单个年度的官方 NLR 工作簿。"""
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return []

    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    # 定位包含 "stock code" 的表头行
    hdr_idx = None
    for idx, r in enumerate(rows[:12]):
        vals = [str(x or "").lower() for x in r[:8]]
        if any("stock code" in v for v in vals):
            hdr_idx = idx
            break

    if hdr_idx is None:
        logger.error(f"Cannot find header row in {filepath}")
        return []

    candidates: list[dict[str, Any]] = []
    curr: Optional[dict[str, Any]] = None

    for r in rows[hdr_idx + 1:]:
        file_no = r[0] if len(r) > 0 else None
        code_raw = r[1] if len(r) > 1 else None
        name_raw = r[2] if len(r) > 2 else None
        p_date = r[3] if len(r) > 3 else None
        l_date = r[4] if len(r) > 4 else None
        sponsor = r[5] if len(r) > 5 else ""
        accountant = r[6] if len(r) > 6 else ""
        valuer = r[7] if len(r) > 7 else ""
        funds = r[8] if len(r) > 8 else None
        price = r[9] if len(r) > 9 else None
        fund_type = str(r[10] if len(r) > 10 else "").strip().lower()

        if code_raw not in (None, "", '"') and str(code_raw).strip() != '"':
            if curr:
                candidates.append(curr)
            norm_code = clean_code(code_raw)
            curr = {
                "file_no": file_no,
                "raw_code": str(code_raw).strip(),
                "stock_code": norm_code,
                "company_name": str(name_raw or "").strip(),
                "prospectus_date": parse_date(p_date),
                "listing_date": parse_date(l_date),
                "cohort_year": cohort_year,
                "sponsors": str(sponsor or "").strip(),
                "auditor": str(accountant or "").strip(),
                "valuer": str(valuer or "").strip() if str(valuer or "").strip() not in ("N/A", "NA", "") else None,
                "funds_raised_public_hkd": to_float(funds),
                "funds_raised_int_hkd": None,
                "offer_price_hkd": to_float(price),
                "raw_price_str": str(price or "").strip(),
                "raw_funds_str": str(funds or "").strip(),
            }
        elif curr and (fund_type == "(b)" or str(code_raw or "").strip() == '"'):
            curr["funds_raised_int_hkd"] = to_float(funds)
            if curr["offer_price_hkd"] is None:
                curr["offer_price_hkd"] = to_float(price)

    if curr:
        candidates.append(curr)

    return candidates


def audit_candidate(cand: dict[str, Any]) -> dict[str, Any]:
    """对单个候选上市实体进行排他性法定口径与学术实证筛选。"""
    name = cand["company_name"]
    name_l = name.lower()
    raw_price = cand["raw_price_str"].lower()
    raw_funds = cand["raw_funds_str"].lower()
    code = cand["stock_code"]

    f_pub = cand["funds_raised_public_hkd"] or 0.0
    f_int = cand["funds_raised_int_hkd"] or 0.0
    tot_funds = f_pub + f_int
    cand["funds_raised_total_hkd"] = tot_funds if tot_funds > 0 else None

    # 1. 甄别 GEM 转主板 (Chapter 9A)
    if "transfer" in name_l or "transfer" in raw_price or "transfer" in raw_funds or "gem" in raw_price:
        cand["inclusion_status"] = "EXCLUDED"
        cand["exclusion_reason"] = "Transfer of listing from GEM to Main Board under Chapter 9A (No IPO capital raising)"
        cand["security_type"] = "GEM Transfer"
        cand["listing_route"] = "Transfer from GEM"
        cand["data_completion_status"] = "EXCLUDED_NON_IPO"
        return cand

    # 2. 甄别 SPAC 与 De-SPAC 并购 (Chapter 18B)
    if "spac" in name_l or "spac" in raw_price or code.startswith("78"):
        cand["inclusion_status"] = "EXCLUDED"
        cand["exclusion_reason"] = "Special Purpose Acquisition Company (SPAC) offering or De-SPAC business combination under Chapter 18B"
        cand["security_type"] = "SPAC"
        cand["listing_route"] = "De-SPAC" if "de-spac" in name_l or "de-spac" in raw_price else "SPAC"
        cand["data_completion_status"] = "EXCLUDED_NON_IPO"
        return cand

    # 3. 甄别介绍上市 (Listing by Introduction - 无公开发行募资)
    if "introduction" in name_l or "introduction" in raw_price or "introduction" in raw_funds or (cand["offer_price_hkd"] is None and tot_funds == 0):
        cand["inclusion_status"] = "EXCLUDED"
        cand["exclusion_reason"] = "Listing by Introduction without primary or secondary public capital raising"
        cand["security_type"] = "Ordinary Shares"
        cand["listing_route"] = "Introduction"
        cand["data_completion_status"] = "EXCLUDED_NON_IPO"
        return cand

    # 4. 纳入：合格主板 IPO (Ordinary Main Board IPO with primary/secondary capital raising)
    cand["inclusion_status"] = "INCLUDED"
    cand["exclusion_reason"] = None
    cand["data_completion_status"] = "COMPLETE"

    # 细化分类特征 (Listing Chapters & Security Types)
    is_18a = False
    is_18c = False
    is_wvr = False
    is_ah = False

    # Chapter 18A: 生物科技标记 (- B)
    if any(tag in name for tag in ("- B", " - B", "-B")):
        is_18a = True

    # Chapter 18C: 特专科技公司
    if any(tag in name for tag in ("- P", " - P", "-P")):
        is_18c = True

    # Chapter 8A: WVR 同股不同权 (- W)
    if any(tag in name for tag in ("- W", " - W", "-W")):
        is_wvr = True

    # Chapter 19A: H 股 / A+H 两地发行
    if "h share" in name_l or "h-share" in name_l:
        is_ah = True
        sec_type = "H Shares"
    elif is_wvr:
        sec_type = "WVR Shares"
    else:
        sec_type = "Ordinary Shares"

    cand["security_type"] = sec_type
    cand["is_18a"] = is_18a
    cand["is_18c"] = is_18c
    cand["is_wvr"] = is_wvr
    cand["is_ah"] = is_ah

    # 确定上市监管通道
    if is_18c:
        route = "Chapter 18C (Specialist Tech)"
    elif is_18a:
        route = "Chapter 18A (Biotech)"
    elif is_ah:
        route = "Chapter 19A (A+H)"
    elif is_wvr:
        route = "Chapter 8A (WVR)"
    else:
        route = "Main Board Conventional"
    cand["listing_route"] = route

    # 制度分期
    l_date = cand["listing_date"]
    if l_date:
        cand["fini_regime"] = "POST_FINI" if l_date >= FINI_CUTOFF_DATE else "PRE_FINI"
        cand["pricing_reform_regime"] = "POST_2025_REFORM" if l_date >= REFORM_2025_DATE else "PRE_2025_REFORM"
    else:
        cand["fini_regime"] = "POST_FINI"
        cand["pricing_reform_regime"] = "POST_2025_REFORM"

    cand["prospectus_source"] = "HKEXnews (Official Prospectus)"
    cand["allotment_source"] = "HKEXnews (Allotment Results Announcement)"

    # 提取首位独家/联席保荐人
    sp_raw = cand.get("sponsors", "")
    lead_sp = sp_raw.split("/")[0].split("\n")[0].strip() if sp_raw else ""
    cand["lead_sponsor"] = lead_sp

    return cand


def build_master_sample(start_year: int = 2021, end_year: int = 2026) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """批量构建跨年度香港主板全样本。"""
    OUT_MASTER.mkdir(parents=True, exist_ok=True)
    all_candidates: list[dict[str, Any]] = []

    for y in range(start_year, end_year + 1):
        fn = f"NLR{y}_Eng.xlsx"
        fp = SOURCES_DIR / fn
        cands = load_nlr_candidates(fp, y)
        logger.info(f"Loaded {len(cands)} candidates from {fn}")
        for c in cands:
            audited = audit_candidate(c)
            all_candidates.append(audited)

    # 拆分有效样本与筛选清单
    included_sample = [c for c in all_candidates if c["inclusion_status"] == "INCLUDED"]
    excluded_sample = [c for c in all_candidates if c["inclusion_status"] == "EXCLUDED"]

    # 1. 导出样本构建全景清单 (sample_construction.csv)
    sc_fields = [
        "stock_code", "company_name", "cohort_year", "listing_date", "prospectus_date",
        "security_type", "listing_route", "inclusion_status", "exclusion_reason",
        "funds_raised_total_hkd", "offer_price_hkd", "prospectus_source", "allotment_source", "data_completion_status"
    ]
    sc_path = OUT_MASTER / "sample_construction.csv"
    with sc_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=sc_fields, extrasaction="ignore")
        writer.writeheader()
        for c in all_candidates:
            row = dict(c)
            row["listing_date"] = str(c["listing_date"]) if c.get("listing_date") else ""
            row["prospectus_date"] = str(c["prospectus_date"]) if c.get("prospectus_date") else ""
            writer.writerow(row)

    # 2. 导出主板新股 Master 基础信息表 (issuer_master.csv)
    im_fields = [
        "stock_code", "company_name", "cohort_year", "listing_date", "prospectus_date",
        "security_type", "listing_route", "fini_regime", "pricing_reform_regime",
        "is_ah", "is_wvr", "is_18a", "is_18c", "lead_sponsor", "sponsors", "auditor", "valuer",
        "offer_price_hkd", "funds_raised_public_hkd", "funds_raised_int_hkd", "funds_raised_total_hkd"
    ]
    im_path = OUT_MASTER / "issuer_master.csv"
    with im_path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=im_fields, extrasaction="ignore")
        writer.writeheader()
        for c in included_sample:
            row = dict(c)
            row["listing_date"] = str(c["listing_date"]) if c.get("listing_date") else ""
            row["prospectus_date"] = str(c["prospectus_date"]) if c.get("prospectus_date") else ""
            writer.writerow(row)

    # 3. 导出结构化 JSON 缓存供下游流水线无缝消费
    im_json_path = OUT_MASTER / "issuer_master.json"
    serializable = []
    for c in included_sample:
        rec = dict(c)
        rec["listing_date"] = str(c["listing_date"]) if c.get("listing_date") else None
        rec["prospectus_date"] = str(c["prospectus_date"]) if c.get("prospectus_date") else None
        serializable.append(rec)
    im_json_path.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")

    return all_candidates, included_sample


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    all_cands, inc_sample = build_master_sample(2021, 2026)
    print(f"\n=======================================================")
    print(f"HK IPO Master Sample Construction Complete (2021-2026)")
    print(f"=======================================================")
    print(f"Total Candidate Filings Screened : {len(all_cands)}")
    print(f"Included Ordinary IPO Issuers    : {len(inc_sample)}")
    print(f"Excluded Filings (GEM/SPAC/Intro): {len(all_cands) - len(inc_sample)}")
    print(f"Outputs written to: {OUT_MASTER}")
