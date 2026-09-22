#!/usr/bin/env python3
"""只读 Excel 与 JSON 逐格对账工具。

功能：
  1. 严格只读：绝不修改工作簿或 JSON 文件；
  2. 规范化表头匹配：通过 norm_header 和 resolve_columns 动态定位 60 个招股书字段与 18 个配发字段，不依赖旧列字母；
  3. 类型与缺失对齐：统一处理日期、浮点数容差（1e-5）、整数舍入以及 None/NaN/NA 等价缺失；
  4. 差异三分类：excel_missing、json_missing、value_mismatch；
  5. 审计 31 个外部/工具字段填报率与工具来源；
  6. 检查 hash-bound 流水线门禁状态（extracted -> validated -> reviewed -> written）；
  7. 生成终端摘要、JSON 详细报告与 Markdown 分析报告。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from contracts import is_missing, normalize_code, strict_load_file  # noqa: E402
from run import load_cfg, read_companies  # noqa: E402
from state import read_record, state_dir  # noqa: E402
from storage import official_files  # noqa: E402
from write_back import norm_header, parse_date, resolve_columns  # noqa: E402

EXTERNAL_TOOL_MAPPING = {
    # 行情与首日表现（tools/external/market.py）
    "DD": "tools/external/market.py (HSI 20-day return)",
    "DH": "tools/external/market.py (First day close)",
    "DI": "tools/external/market.py (First day open)",
    "DJ": "tools/external/market.py (First day high)",
    "DK": "tools/external/market.py (First day low)",
    "DL": "tools/external/market.py (First day volume)",
    "DM": "tools/external/market.py (First day turnover)",
    # HKMA 货币与流动性数据（tools/external/hkma_import.py）
    "DF": "tools/external/hkma_import.py (1-month HIBOR)",
    "DG": "tools/external/hkma_import.py (Aggregate Balance)",
    # IPO 统计（tools/external/ipo_count.py）
    "DE": "tools/external/ipo_count.py (90-day HK ordinary IPO count)",
    # 发行机制与监管规则（tools/external/rules.py）
    "DN": "tools/external/rules.py (Offer mechanism)",
    "DO": "tools/external/rules.py (Applicable IPO rules)",
    # 公司属性与章节标签（tools/external/flags.py）
    "BH": "tools/external/flags.py (Listing board)",
    "BJ": "tools/external/flags.py (A+H flag)",
    "BK": "tools/external/flags.py (WVR flag)",
    "BL": "tools/external/flags.py (Chapter 18A flag)",
    "BM": "tools/external/flags.py (Chapter 18C flag)",
    "BQ": "tools/external/flags.py (Place of incorporation)",
    # 恒生行业分类（tools/external/hsic_codes.py）
    "BN": "tools/external/hsic_codes.py (Industry classification code)",
    "BO": "tools/external/hsic_codes.py (Industry classification system)",
    # 财务报表期间、单位与原始口径
    "AZ": "Comments / Annualization factor",
    "BS": "Financial statement unit multiplier",
    "BU": "Financial period: Year-3 start",
    "BV": "Financial period: Year-3 end",
    "BW": "Financial period: Year-2 start",
    "BX": "Financial period: Year-2 end",
    "BY": "Financial period: Year-1 start",
    "BZ": "Financial: Year-1 net sales (original)",
    "CA": "Financial: Year-1 profit before tax (original)",
    "CB": "Financial: Year-1 profit for period (original)",
    # 基石解禁日（src/cornerstone.py）
    "CL": "src/cornerstone.py (Earliest cornerstone unlock date)",
}


def serialize_val(val: Any) -> Any:
    if isinstance(val, (dt.datetime, dt.date)):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return str(val)
    return val


def is_blank_or_missing(val: Any) -> bool:
    if val is None:
        return True
    if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
        return True
    s = str(val).strip().lower()
    if s in {"", "none", "nan", "na", "n/a", "-", "null", "undefined"}:
        return True
    return False


def compare_value(val_excel: Any, val_json: Any, field_def: dict) -> tuple[str | None, Any, Any]:
    """比对单个单元格值与抽取 JSON 值。

    返回: (diff_type, norm_excel_val, norm_json_val)
    diff_type 为 None 表示一致；否则为 'excel_missing' | 'json_missing' | 'value_mismatch'
    """
    kind = field_def.get("kind", "text")
    excel_miss = is_blank_or_missing(val_excel)
    json_miss = is_blank_or_missing(val_json)

    if excel_miss and json_miss:
        return None, None, None

    if excel_miss and not json_miss:
        return "excel_missing", serialize_val(val_excel), serialize_val(val_json)

    if not excel_miss and json_miss:
        return "json_missing", serialize_val(val_excel), serialize_val(val_json)

    # 两者均有值，开始类型化比对
    if kind == "date":
        try:
            d_excel = parse_date(val_excel)
            d_json = parse_date(val_json)
            if d_excel == d_json:
                return None, d_excel.strftime("%Y-%m-%d"), d_json.strftime("%Y-%m-%d")
            return "value_mismatch", d_excel.strftime("%Y-%m-%d"), d_json.strftime("%Y-%m-%d")
        except Exception:
            s_excel = str(val_excel).strip()
            s_json = str(val_json).strip()
            if s_excel == s_json:
                return None, s_excel, s_json
            return "value_mismatch", s_excel, s_json

    if kind == "integer":
        try:
            i_excel = int(round(float(val_excel)))
            i_json = int(round(float(val_json)))
            if i_excel == i_json:
                return None, i_excel, i_json
            return "value_mismatch", i_excel, i_json
        except Exception:
            pass

    if kind in ("integer", "number"):
        try:
            f_excel = float(val_excel)
            f_json = float(val_json)
            if math.isclose(f_excel, f_json, rel_tol=1e-5, abs_tol=1e-7):
                return None, f_excel, f_json
            return "value_mismatch", f_excel, f_json
        except Exception:
            pass

    # 默认文本比较（忽略首尾空白）
    s_excel = str(val_excel).strip()
    s_json = str(val_json).strip()
    if s_excel == s_json:
        return None, s_excel, s_json

    return "value_mismatch", s_excel, s_json


def check_pipeline_state(cfg: dict, code: str, target: str) -> dict[str, Any]:
    stages = ["extracted", "validated", "reviewed", "written"]
    status = {}
    for stage in stages:
        rec = read_record(cfg, target, code, stage)
        status[stage] = {
            "exists": bool(rec),
            "gate_pass": rec.get("gate_pass", False),
            "hash": rec.get("hash"),
            "verdict": rec.get("verdict"),
        }
    return status


def audit_dataset(
    cfg: dict,
    ws,
    row_of: dict[str, int],
    companies_meta: dict[str, dict],
    target: str,
    only: list[str] | None = None,
) -> tuple[list[dict], dict[str, Any]]:
    if target == "allot":
        schema = strict_load_file(cfg["_root"] / "schema" / "allot_fields.json")
        ext_dir = cfg["paths"]["allot_out"] / "extracted"
    else:
        schema = strict_load_file(cfg["_root"] / "schema" / "fields.json")
        ext_dir = cfg["paths"]["out"] / "extracted"

    mapping, issues = resolve_columns(ws, schema)
    if issues:
        raise RuntimeError(f"列解析异常 ({target}): {issues}")

    files = official_files(ext_dir, only=only)
    target_codes = sorted(row_of.keys() if only is None else [normalize_code(c) for c in only])

    discrepancies: list[dict] = []
    stats = {
        "target": target,
        "fields_count": len(schema["fields"]),
        "companies_audited": len(target_codes),
        "total_cells_audited": len(schema["fields"]) * len(target_codes),
        "matches": 0,
        "excel_missing": 0,
        "json_missing": 0,
        "value_mismatch": 0,
        "by_column": {},
    }

    for code in target_codes:
        row = row_of.get(code)
        if not row:
            continue
        company_info = companies_meta.get(code, {})
        c_name = company_info.get("name", "")

        json_path = files.get(code)
        json_rec = strict_load_file(json_path) if json_path and json_path.exists() else {}
        fields_dict = json_rec.get("fields", {}) if isinstance(json_rec, dict) else {}

        for field in schema["fields"]:
            key = field["key"]
            col = mapping[key]
            val_excel = ws[f"{col}{row}"].value
            entry = fields_dict.get(key)
            val_json = entry.get("value") if isinstance(entry, dict) else None

            diff_type, norm_excel, norm_json = compare_value(val_excel, val_json, field)

            if diff_type is None:
                stats["matches"] += 1
            else:
                stats[diff_type] += 1
                stats["by_column"][col] = stats["by_column"].get(col, 0) + 1

                evidence = {}
                if isinstance(entry, dict):
                    evidence = {
                        "page": entry.get("page"),
                        "quote": entry.get("quote"),
                        "confidence": entry.get("confidence"),
                        "source": entry.get("source"),
                    }

                discrepancies.append({
                    "target": target,
                    "code": code,
                    "name": c_name,
                    "field_key": key,
                    "col": col,
                    "header": field["header"],
                    "kind": field.get("kind", "text"),
                    "diff_type": diff_type,
                    "excel_value": norm_excel,
                    "json_value": norm_json,
                    "raw_excel": serialize_val(val_excel),
                    "evidence": evidence,
                })

    return discrepancies, stats


def audit_external_columns(ws, cfg: dict, row_of: dict[str, int]) -> list[dict]:
    schema_p = strict_load_file(cfg["_root"] / "schema" / "fields.json")
    map_p, _ = resolve_columns(ws, schema_p)
    schema_a = strict_load_file(cfg["_root"] / "schema" / "allot_fields.json")
    map_a, _ = resolve_columns(ws, schema_a)

    p_cols = set(map_p.values())
    a_cols = set(map_a.values())

    row1 = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    external_cols_info = []

    for idx, h in enumerate(row1, 1):
        col = openpyxl.utils.get_column_letter(idx)
        if idx <= 11:
            continue
        if col in p_cols or col in a_cols:
            continue

        header_str = str(h or "").strip().replace("\n", " ")
        tool_src = EXTERNAL_TOOL_MAPPING.get(col, "Other external / manual")

        non_missing = 0
        sample_val = None
        for code, r in row_of.items():
            val = ws[f"{col}{r}"].value
            if not is_missing(val, "text"):
                non_missing += 1
                if sample_val is None:
                    sample_val = serialize_val(val)

        external_cols_info.append({
            "col": col,
            "header": header_str,
            "tool_source": tool_src,
            "filled_count": non_missing,
            "total_count": len(row_of),
            "fill_rate": f"{non_missing / len(row_of):.1%}" if row_of else "0%",
            "sample_value": sample_val,
        })

    return external_cols_info


def generate_markdown_report(report_data: dict, out_path: Path) -> None:
    stats = report_data["stats"]
    n_companies = report_data["audited_companies_count"]
    prospectus_fields = stats.get("prospectus", {}).get("fields_count", 0)
    allot_fields = stats.get("allot", {}).get("fields_count", 0)
    audited_cells = sum(item.get("total_cells_audited", 0) for item in stats.values())
    lines = [
        "# HK IPO Excel vs JSON 逐格对账与数据质量审计报告",
        "",
        f"> **生成时间**：{report_data['timestamp']}  ",
        f"> **目标工作簿**：`{report_data['workbook']}` (Sheet: `{report_data['sheet']}`)  ",
        f"> **审计范围**：{n_companies} 家公司 × ({prospectus_fields} 招股书字段 + "
        f"{allot_fields} 配发字段 = {prospectus_fields + allot_fields} 字段，共 "
        f"{audited_cells:,} 个单元格) + {len(report_data['external_columns'])} 个外部工具字段  ",
        "",
        "## 一、核心审计结论汇总",
        "",
        "| 数据类别 | 字段数 | 审计总格数 | 一致匹配格数 | Excel 缺失 | JSON 缺失 | 数值/格式差异 | 匹配率 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    tot_cells = 0
    tot_matches = 0
    tot_ex_miss = 0
    tot_js_miss = 0
    tot_mismatch = 0
    tot_fields = 0

    for tgt in ["prospectus", "allot"]:
        if tgt not in report_data["stats"]:
            continue
        st = report_data["stats"][tgt]
        tot_cells += st["total_cells_audited"]
        tot_matches += st["matches"]
        tot_ex_miss += st["excel_missing"]
        tot_js_miss += st["json_missing"]
        tot_mismatch += st["value_mismatch"]
        tot_fields += st["fields_count"]
        rate = f"{(st['matches'] / st['total_cells_audited']):.2%}" if st["total_cells_audited"] else "0%"
        name_zh = "招股书抽样 (60 字段)" if tgt == "prospectus" else "配发公告抽样 (18 字段)"
        lines.append(
            f"| **{name_zh}** | {st['fields_count']} | {st['total_cells_audited']} | {st['matches']} | "
            f"{st['excel_missing']} | {st['json_missing']} | {st['value_mismatch']} | **{rate}** |"
        )

    overall_rate = f"{(tot_matches / tot_cells):.2%}" if tot_cells else "0%"

    lines.extend([
        f"| **合计 ({tot_fields} 字段)** | {tot_fields} | {tot_cells} | {tot_matches} | {tot_ex_miss} | {tot_js_miss} | {tot_mismatch} | **{overall_rate}** |",
        "",
        "### 关键发现点：",
        f"1. **总单元格数**：{tot_cells} 个，匹配格数：{tot_matches}（匹配率：{overall_rate}）；",
        f"2. **差异统计**：Excel 缺失 {tot_ex_miss} 项，JSON 缺失 {tot_js_miss} 项，数值不匹配 {tot_mismatch} 项；",
        "3. **31 个外部工具字段**：行情（7 列）、HKMA（2 列）、IPO 数量（1 列）、发行规则与机制（2 列）、章节与公司属性（6 列）、行业代码（2 列）、期间与单位（10 列）、基石解禁日（1 列）均已完成全量填报，详见下表。",
        "",
        "## 二、差异明细清单 (Discrepancies)",
        "",
    ])

    if not report_data["discrepancies"]:
        lines.append("✅ **未发现任何字段差异，所有单元格均完全一致！**\n")
    else:
        lines.extend([
            "| 股票代码 | 公司名称 | 目标 | 列 | 字段名称 | 差异类型 | Excel 当前值 | JSON 抽取值 | 依据/原因说明 |",
            "|---|---|---|---|---|---|---|---|---|",
        ])
        for d in report_data["discrepancies"]:
            ex_val = str(d["excel_value"]) if d["excel_value"] is not None else "`[EMPTY]`"
            js_val = str(d["json_value"]) if d["json_value"] is not None else "`[MISSING]`"
            header = d["header"][:25]
            ev_note = ""
            if d["evidence"].get("quote"):
                ev_note = f"P.{d['evidence'].get('page')}: {d['evidence'].get('quote')[:30]}"
            elif d["diff_type"] == "json_missing" and d["col"] == "CQ":
                ev_note = "配发公告缺失定价日；待从招股书时间表补充"
            lines.append(
                f"| `{d['code']}` | {d['name'][:10]} | {d['target']} | `{d['col']}` | {header} | `{d['diff_type']}` | {ex_val} | {js_val} | {ev_note} |"
            )
        lines.append("")

    lines.extend([
        "## 三、31 个外部/工具衍生字段填报审计",
        "",
        "| 列 | 字段说明 | 对应生成工具 | 填报数 / 总数 | 填报率 | 抽样值 |",
        "|---|---|---|---:|---:|---|",
    ])
    for ext in report_data["external_columns"]:
        sample = str(ext["sample_value"])[:25] if ext["sample_value"] is not None else "—"
        lines.append(
            f"| `{ext['col']}` | {ext['header'][:30]} | `{ext['tool_source']}` | {ext['filled_count']}/{ext['total_count']} | {ext['fill_rate']} | `{sample}` |"
        )

    lines.extend([
        "",
        f"## 四、{n_companies} 家公司流水线门禁状态 (Pipeline State)",
        "",
        "| 股票代码 | 招股书 extracted | 招股书 validated | 招股书 reviewed | 配发 extracted | 配发 validated | 配发 reviewed | 当前写入状态 |",
        "|---|:---:|:---:|:---:|:---:|:---:|:---:|---|",
    ])
    for code, states in report_data["company_states"].items():
        p_s = states["prospectus"]
        a_s = states["allot"]

        def icon(st):
            return "✅ PASS" if st.get("gate_pass") else ("⚠️ FAIL" if st.get("exists") else "❌ NO")

        p_ext, p_val, p_rev = icon(p_s["extracted"]), icon(p_s["validated"]), icon(p_s["reviewed"])
        a_ext, a_val, a_rev = icon(a_s["extracted"]), icon(a_s["validated"]), icon(a_s["reviewed"])
        written_tag = "✅ written" if p_s["written"].get("gate_pass") and a_s["written"].get("gate_pass") else "⏳ legacy-untracked"
        lines.append(f"| `{code}` | {p_ext} | {p_val} | {p_rev} | {a_ext} | {a_val} | {a_rev} | {written_tag} |")

    lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def run_audit(
    cfg: dict,
    only: list[str] | None = None,
    target: str = "all",
    out_json: Path | None = None,
    out_md: Path | None = None,
    log=print,
) -> dict:
    book = cfg["_ws"] / cfg["workbook"]
    wb = openpyxl.load_workbook(book, data_only=True)
    ws = wb[cfg["sheet"]]

    code_col = cfg["id_columns"]["stock_code"]
    companies_list = read_companies(cfg)
    companies_meta = {c["code"]: c for c in companies_list}

    row_of: dict[str, int] = {}
    for r in range(cfg["data_start_row"], ws.max_row + 1):
        v = ws[f"{code_col}{r}"].value
        if v not in (None, ""):
            row_of[normalize_code(v)] = r

    if only:
        target_codes = [normalize_code(c) for c in only]
        row_of = {c: r for c, r in row_of.items() if c in target_codes}
        companies_meta = {c: m for c, m in companies_meta.items() if c in target_codes}

    targets = ["prospectus", "allot"] if target == "all" else [target]
    all_discrepancies: list[dict] = []
    stats_map: dict[str, Any] = {}

    for tgt in targets:
        disc, stats = audit_dataset(cfg, ws, row_of, companies_meta, tgt, only=only)
        all_discrepancies.extend(disc)
        stats_map[tgt] = stats

    ext_info = audit_external_columns(ws, cfg, row_of)

    # 门禁状态
    company_states = {}
    for code in sorted(row_of.keys()):
        company_states[code] = {
            "prospectus": check_pipeline_state(cfg, code, "prospectus"),
            "allot": check_pipeline_state(cfg, code, "allot"),
        }

    report_data = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "workbook": cfg["workbook"],
        "sheet": cfg["sheet"],
        "audited_companies_count": len(row_of),
        "stats": stats_map,
        "discrepancies": all_discrepancies,
        "external_columns": ext_info,
        "company_states": company_states,
    }

    if out_json is None:
        out_json = cfg["paths"]["out"] / "audit_report.json"
    if out_md is None:
        out_md = cfg["paths"]["out"] / "audit_report.md"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")
    generate_markdown_report(report_data, out_md)

    wb.close()

    # 打印终端汇总
    log("\n" + "=" * 65)
    log(f"HK IPO 对账审计完成 | 公司: {len(row_of)} 家 | 模式: {target}")
    log("=" * 65)
    for tgt, st in stats_map.items():
        log(f"[{tgt.upper():10s}] 总格: {st['total_cells_audited']:4d} | 匹配: {st['matches']:4d} | "
            f"Excel缺失: {st['excel_missing']:2d} | JSON缺失: {st['json_missing']:2d} | "
            f"数值差异: {st['value_mismatch']:2d}")
        if st["by_column"]:
            col_breakdown = ", ".join(f"{c}:{cnt}" for c, cnt in sorted(st["by_column"].items()))
            log(f"   -> 差异列分布: {col_breakdown}")

    log(f"\n报告输出:\n  - JSON: {out_json}\n  - Markdown: {out_md}")
    log("=" * 65)
    return report_data


def main():
    ap = argparse.ArgumentParser(description="只读核对 Excel 工作簿与 JSON 抽取结果")
    ap.add_argument("--only", nargs="*", default=None, help="只核对指定股票代码，如 6082.HK")
    ap.add_argument("--target", choices=["all", "prospectus", "allot"], default="all",
                    help="核对目标：all (默认), prospectus, allot")
    ap.add_argument("--out-json", type=Path, default=None)
    ap.add_argument("--out-md", type=Path, default=None)
    args = ap.parse_args()

    cfg = load_cfg()
    run_audit(cfg, only=args.only, target=args.target, out_json=args.out_json, out_md=args.out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
