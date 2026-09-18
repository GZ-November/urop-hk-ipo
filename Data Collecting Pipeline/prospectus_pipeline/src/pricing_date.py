"""确定性派生配发字段 col_CQ (定价日，Pricing date)。

口径定义与业务规则：
  1. 固定发售价机制（Fixed Price Offering）：
     当招股书中最高发售价 (col_T) == 最低发售价 (col_U) 时，发行价在招股书刊载时已最终确定，
     无簿记建档定价日环节，业务上定价日不适用，确定性派生为 'NA'。
  2. 区间询价发售机制（Price Range Offering）：
     当最高发售价 (col_T) != 最低发售价 (col_U) 时，从招股书「Expected Timetable（预期时间表）」
     中确定性提取 Expected Price Determination Date，挂载真实页码与原文引文，source 标注为 'prospectus'。
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

from contracts import normalize_code, strict_load_file
from storage import atomic_json, official_files

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_PATTERN = re.compile(
    rf"(?:on\s+or\s+(?:about|before)\s+)?(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?,?\s*"
    rf"(\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}|(?:{MONTHS})\s+\d{{1,2}},?\s+\d{{4}}|\d{{1,2}}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{{4}})",
    re.IGNORECASE,
)


def _parse_date_str(s: str) -> dt.date | None:
    s = " ".join(s.replace(",", " ").split())
    for fmt in ("%d %B %Y", "%B %d %Y", "%d %b %Y", "%b %d %Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def extract_pricing_date(cfg: dict, code: str) -> dict[str, Any]:
    code = normalize_code(code)
    digits = "".join(c for c in code if c.isdigit())

    # 1. 读取招股书提取结果检查发售定价机制 (col_T vs col_U)
    p_file = cfg["paths"]["out"] / "extracted" / f"HKIPO-MB{digits}.json"
    if not p_file.exists():
        return {"value": "NA", "page": None, "quote": "", "source": "prospectus", "confidence": "low"}

    prec = strict_load_file(p_file)
    pfields = prec.get("fields", {})
    t_entry = pfields.get("col_T", {})
    u_entry = pfields.get("col_U", {})
    t_val = t_entry.get("value")
    u_val = u_entry.get("value")

    # 若为固定发售价（col_T == col_U）
    if t_val is not None and u_val is not None:
        try:
            if float(t_val) == float(u_val):
                return {
                    "value": "NA",
                    "page": t_entry.get("page") or 1,
                    "quote": f"Offer Price is fixed at HK${float(t_val):.2f}; no bookbuilding price determination date",
                    "source": "allotment",
                    "confidence": "high",
                }
        except (ValueError, TypeError):
            pass

    # 2. 从招股书前 25 页检索 Expected Timetable
    text_file = cfg["paths"]["text"] / f"HKIPO-MB{digits}.jsonl"
    if text_file.exists():
        for line in text_file.open(encoding="utf-8"):
            p = json.loads(line)
            if p["page"] > 25:
                continue
            txt = p["text"]
            if any(k in txt for k in ["Price Determination Date", "price determination date", "Offer Price is expected to be determined"]):
                lines = txt.split("\n")
                for i, l in enumerate(lines):
                    if any(k in l for k in ["Price Determination", "price determination", "Offer Price is expected to be determined"]):
                        # 拼接下两行防止时间表跨行折叠
                        next_lines = " ".join(lines[i+1:i+3]) if i + 1 < len(lines) else ""
                        chunk = l + " " + next_lines
                        m = DATE_PATTERN.search(chunk)
                        if m:
                            d = _parse_date_str(m.group(1))
                            if d:
                                return {
                                    "value": d.strftime("%d/%m/%y"),
                                    "page": p["page"],
                                    "quote": chunk.strip()[:150],
                                    "source": "prospectus",
                                    "confidence": "high",
                                }

    # 未检出默认回退
    return {"value": "NA", "page": None, "quote": "", "source": "allotment", "confidence": "low"}


def apply_cq(cfg: dict, only: list[str] | None = None, log=print) -> int:
    """确定性写入或补全配发 JSON 中的 col_CQ 字段。"""
    ext = cfg["paths"]["allot_out"] / "extracted"
    count = 0
    for code, fp in official_files(ext, only=only).items():
        rec = strict_load_file(fp)
        fields = rec.setdefault("fields", {})

        current_entry = fields.get("col_CQ")
        # 如果已有非空合法日期，不盲目覆盖；若为 missing 则补齐
        current_val = current_entry.get("value") if isinstance(current_entry, dict) else None
        if current_val not in (None, "", "NaN", "NA", "nan", "na"):
            continue

        cq_data = extract_pricing_date(cfg, code)
        fields["col_CQ"] = cq_data
        atomic_json(fp, rec)
        count += 1
        log(f"  col_CQ派生 [{code}]: {cq_data['value']} (P.{cq_data['page']})")

    return count
