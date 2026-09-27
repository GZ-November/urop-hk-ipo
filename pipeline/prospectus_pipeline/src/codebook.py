#!/usr/bin/env python3
"""HK IPO 学术研究级变量字典（Codebook）与纯净 CSV 导出引擎。

功能：
  1. 完整解析当前配置的工作簿（变量数与样本量按工作簿动态识别）；
  2. 自动识别三色数据层级：
     - 浅绿（A–K，11 列）：香港交易所新上市报告官方基础信息；
     - 浅蓝（L–AY, DP, CJ, BA–CI，60 列）：招股书全量披露指标；
     - 深蓝（CK, CM–DC，18 列）：配发结果公告与确定性派生指标；
     - 深蓝（DD–DO, DF, DG，31 列）：外部工具行情、HIBOR、总结余与监管分类。
  3. 变量类型智能推断（Numeric / Date / Boolean / Categorical / Text）；
  4. 计算样本统计量（有效样本量、填报率、均值、中位数、标准差、分位数、极值范围、分类频数）；
  5. 导出：
     - cohort-specific clean CSV (UTF-8 with BOM, compatible with Stata, Python pandas, and Excel);
     - cohort-specific Markdown codebook;
     - cohort-specific machine-readable JSON codebook.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import statistics
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from variable_catalog import (  # noqa: E402
    ACADEMIC_VARS, EXTERNAL_VARS, EXTRA_HEADER_VARS, HKEX_GREEN_VARS, lookup_tables,
)
from cohort import cohort_artifact_stem  # noqa: E402
from run import load_cfg  # noqa: E402

# 浅绿 A–K 官方定义
def parse_numeric(v: Any) -> float | None:
    if v in (None, "", "NA", "NaN"):
        return None
    try:
        val = float(v)
        return None if (math.isnan(val) or math.isinf(val)) else val
    except (ValueError, TypeError):
        return None


def parse_date_str(v: Any) -> str | None:
    if v in (None, "", "NA", "NaN"):
        return None
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    s = str(v).strip()
    return s if s else None


def clean_header_name(s: str) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip()


from workbook_reader import norm_header  # noqa: E402


def classify_column(
    col_letter: str,
    raw_header: str,
    col_vals: list[Any],
    n_companies: int,
    declared: str | None,
) -> dict[str, Any]:
    """纯函数 seam：单列 -> (dtype, 统计量)。不含 openpyxl / 文件 I/O。

    declared 为注册表声明的完整 dtype（如 "numeric"）；列全空且存在声明时
    直接采用声明类型（Reserved / Unmatured 列不再依赖推断，避免跨季漂移）。
    """
    import statistics
    from collections import Counter

    clean_header = clean_header_name(raw_header)
    valid_vals = [v for v in col_vals if v not in (None, "", "NA", "NaN")]
    valid_n = len(valid_vals)
    missing_n = n_companies - valid_n
    fill_rate = (valid_n / n_companies) * 100.0

    # 推断数据类型与统计量
    # 1. 检查是否为日期
    is_date = any(isinstance(v, (dt.date, dt.datetime)) for v in valid_vals) or "Date" in clean_header
    # 2. 检查是否为布尔 (0/1)
    is_bool = all(v in (0, 1, "0", "1", True, False) for v in valid_vals) and (
        col_letter in ("BJ", "BK", "BL", "BM", "CR") or "flag" in clean_header.lower() or "0/1" in clean_header or "occurred" in clean_header.lower()
    )
    # 3. 检查是否为纯数值
    numeric_vals = [parse_numeric(v) for v in col_vals]
    valid_nums = [v for v in numeric_vals if v is not None]
    is_numeric = (len(valid_nums) == valid_n and valid_n > 0) and not is_date and not is_bool

    dtype = "string"
    stats: dict[str, Any] = {
        "valid_n": valid_n,
        "missing_n": missing_n,
        "fill_rate_pct": round(fill_rate, 2),
    }

    if valid_n == 0 and declared:
        dtype = declared
        stats["summary_display"] = "全部缺失（Reserved / Unmatured；类型取自注册表声明）"
    elif is_bool:
        dtype = "boolean (0/1)"
        bool_ints = [int(v) for v in valid_vals]
        ones = sum(1 for v in bool_ints if v == 1)
        zeros = sum(1 for v in bool_ints if v == 0)
        stats.update({
            "true_count": ones,
            "false_count": zeros,
            "true_pct": round(ones / valid_n * 100.0, 1) if valid_n else 0.0,
            "summary_display": f"1 (是): {ones} 家 ({ones/valid_n*100:.1f}%), 0 (否): {zeros} 家" if valid_n else "全部缺失"
        })
    elif is_numeric:
        dtype = "numeric"
        avg = statistics.mean(valid_nums)
        med = statistics.median(valid_nums)
        std_dev = statistics.stdev(valid_nums) if len(valid_nums) > 1 else 0.0
        min_v = min(valid_nums)
        max_v = max(valid_nums)
        sorted_nums = sorted(valid_nums)
        q25 = sorted_nums[int(len(sorted_nums) * 0.25)]
        q75 = sorted_nums[int(len(sorted_nums) * 0.75)]
        stats.update({
            "mean": avg,
            "std": std_dev,
            "median": med,
            "min": min_v,
            "q25": q25,
            "q75": q75,
            "max": max_v,
            "summary_display": f"均值 {avg:,.2f} | 中位数 {med:,.2f} | 区间 [{min_v:,.2f}, {max_v:,.2f}]"
        })
    elif is_date:
        dtype = "date (YYYY-MM-DD)"
        date_strs = sorted([parse_date_str(v) for v in valid_vals if parse_date_str(v)])
        min_d = date_strs[0] if date_strs else "N/A"
        max_d = date_strs[-1] if date_strs else "N/A"
        stats.update({
            "min_date": min_d,
            "max_date": max_d,
            "summary_display": f"区间: {min_d} ~ {max_d}" if date_strs else "无有效日期"
        })
    else:
        dtype = "string / categorical"
        counts = Counter(str(v).strip() for v in valid_vals)
        top3 = counts.most_common(3)
        top_str = ", ".join(f"'{k}': {cnt}" for k, cnt in top3)
        stats.update({
            "unique_count": len(counts),
            "top_categories": dict(counts.most_common(5)),
            "summary_display": f"共 {len(counts)} 种取值 ({top_str})" if valid_n else "全部缺失"
        })

    return {
        "dtype": dtype, "stats": stats, "valid_vals": valid_vals,
        "valid_n": valid_n, "missing_n": missing_n, "fill_rate": fill_rate,
        "is_numeric": is_numeric, "is_date": is_date,
    }


def build_codebook(cfg: dict | None = None) -> tuple[list[dict], dict]:
    """完整扫描工作簿生成全量变量字典与样本统计量。"""
    if cfg is None:
        cfg = load_cfg()
    if "workbook_path" in cfg:
        book_path = Path(cfg["workbook_path"])
    elif Path(cfg["workbook"]).is_absolute():
        book_path = Path(cfg["workbook"])
    else:
        book_path = WS / cfg["workbook"]
    wb = openpyxl.load_workbook(book_path, data_only=True)
    ws = wb[cfg["sheet"]]

    # 加载招股书 schema 与配发 schema
    p_schema_by_header = {}
    p_schema_path = ROOT / "schema" / "fields.json"
    if p_schema_path.exists():
        p_data = json.loads(p_schema_path.read_text(encoding="utf-8"))
        p_schema_by_header = {norm_header(f["header"]): f for f in p_data.get("fields", [])}

    a_schema_by_header = {}
    a_schema_path = ROOT / "schema" / "allot_fields.json"
    if a_schema_path.exists():
        a_data = json.loads(a_schema_path.read_text(encoding="utf-8"))
        a_schema_by_header = {norm_header(f["header"]): f for f in a_data.get("fields", [])}

    green_by_header, ext_by_header, academic_by_header, extra_by_header = lookup_tables()

    # 变量注册表声明的类型（declarations from HKIPO_Variable_Registry.yaml）：
    # 全空列（Reserved / Unmatured）不再靠推断，避免跨季度 numeric/string 翻转
    declared_by_header: dict[str, str] = {}
    try:
        from master_panel import REGISTRY_NAME, load_registry
        from paths import registry_path as layout_registry_path
        registry_path = layout_registry_path(WS)
        if registry_path.is_file():
            declared_by_header = {
                v["header"]: (v.get("declared_dtype") or v.get("dtype") or "")
                for v in load_registry(registry_path)["variables"]
            }
    except Exception:
        declared_by_header = {}
    declared_dtype_full = {
        "numeric": "numeric",
        "boolean": "boolean (0/1)",
        "date": "date (YYYY-MM-DD)",
        "string": "string / categorical",
    }

    start_row = cfg["data_start_row"]
    max_col = ws.max_column

    # 动态确定实际公司样本数量
    valid_rows = []
    for r in range(start_row, ws.max_row + 1):
        c_val = ws.cell(r, 2).value
        if c_val is not None and str(c_val).strip():
            valid_rows.append(r)
    n_companies = len(valid_rows)
    if n_companies == 0:
        n_companies = max(1, ws.max_row - start_row + 1)
        valid_rows = list(range(start_row, start_row + n_companies))

    variables = []
    matrix = []

    # 提取所有数据行
    for r in valid_rows:
        row_vals = [ws.cell(r, c).value for c in range(1, max_col + 1)]
        matrix.append(row_vals)

    wb.close()

    # 逐列解析
    for c in range(1, max_col + 1):
        col_letter = get_column_letter(c)
        raw_header = str(ws.cell(1, c).value or "").strip()
        clean_header = clean_header_name(raw_header)
        norm_h = norm_header(raw_header)
        col_vals = [matrix[r_idx][c - 1] for r_idx in range(n_companies)]

        # 确定三色来源与分组
        tier = "深蓝 (配发及外部数据)"
        source_desc = "外部数据源 / 配发公告 / 港交所衍生工具"
        group_name = "external"
        chinese_desc = clean_header

        if norm_h in academic_by_header:
            item = academic_by_header[norm_h]
            clean_header, chinese_desc, _, tier, group_name = item
            source_desc = f"实证金融模型衍生指标（Group: {group_name}，Lowry et al. 2017 规范）"
        elif norm_h in green_by_header:
            tier = "浅绿 (港交所官方报告)"
            item = green_by_header[norm_h]
            clean_header, chinese_desc, _ = item
            source_desc = "香港交易所 (HKEX) 新上市报告 (New Listing Report) 官方表格"
            group_name = "hkex_nlr"
        elif norm_h in p_schema_by_header:
            tier = "浅蓝 (招股书全量披露)"
            meta = p_schema_by_header[norm_h]
            source_desc = f"招股书法定披露章节（Group: {meta.get('group', 'prospectus')}）"
            group_name = meta.get("group", "prospectus")
            chinese_desc = meta.get("description", meta.get("hint", clean_header))
        elif norm_h in a_schema_by_header:
            tier = "深蓝 (配发结果与确定性派生)"
            meta = a_schema_by_header[norm_h]
            source_desc = f"配发结果公告 (Allotment Results) / 确定性派生"
            group_name = meta.get("group", "allotment")
            chinese_desc = meta.get("description", clean_header)
        elif norm_h in ext_by_header:
            item = ext_by_header[norm_h]
            clean_header, chinese_desc, _ = item
            source_desc = "外部市场数据 (Hang Seng / HKMA / 港交所规则)"
            group_name = "external_tools"
        elif norm_h in extra_by_header:
            clean_header, chinese_desc, tier, group_name, source_desc = extra_by_header[norm_h]
        else:
            raise ValueError(
                f"未登记的工作簿表头：{col_letter}={raw_header!r}。"
                "请按稳定表头在 schema 或 EXTRA_HEADER_VARS 中登记；禁止按列字母猜测变量定义。"
            )

        profile = classify_column(
            col_letter, raw_header, col_vals, n_companies,
            declared_dtype_full.get(declared_by_header.get(raw_header, "")))
        dtype = profile["dtype"]
        stats = profile["stats"]
        valid_n = profile["valid_n"]
        fill_rate = profile["fill_rate"]
        is_numeric = profile["is_numeric"]
        valid_vals = profile["valid_vals"]

        h_low = clean_header.lower()
        if "1-month" in h_low:
            timing = "Post-IPO T+20 trading days"
        elif "day-5" in h_low or "day-20" in h_low or "3-month" in h_low:
            timing = "Aftermarket event horizon window"
        elif "stabilization" in h_low or "over-allocation" in h_low or "over-allotment" in h_low:
            timing = "Post-IPO 30-day stabilization window"
        elif "lockup" in h_low or "unlock" in h_low:
            timing = "Post-IPO lockup expiration events"
        elif "6-month" in h_low or "(first 6m)" in h_low or "6m mean" in h_low:
            timing = "Post-IPO 6 calendar months (cornerstone unlock / 6M microstructure)"
        elif "1-year" in h_low or "3-year" in h_low or "reserved" in h_low:
            timing = "Long-run post-IPO (Reserved / Unmatured)"
        elif "first trading day" in h_low or "first-day" in h_low or "money left" in h_low:
            timing = "Listing Day 1 secondary market"
        elif "before prospectus" in h_low:
            timing = "Ex-ante pre-prospectus window"
        elif group_name == "allotment" or "final" in h_low or "subscription ratio" in h_low:
            timing = "Allotment results announcement"
        elif "financial" in group_name or "year-" in h_low:
            timing = "Track record period financial disclosure"
        elif group_name == "syndicate" or "sponsor" in h_low or "underwriting" in h_low:
            timing = "Prospectus syndicate structure"
        elif group_name == "investor_network":
            timing = "Prospectus / allotment institutional network"
        elif group_name == "regulatory_regime" or "regime" in h_low:
            timing = "Listing date regulatory regime"
        else:
            timing = "Ex-ante prospectus disclosure"

        if "[reserved]" in h_low or valid_n == 0:
            coverage = "Reserved / Unmatured"
            missing_pol = "Unmatured window (blank in CSV, None in memory)"
        elif fill_rate == 100.0:
            coverage = "Complete (100%)"
            missing_pol = "No missing observations"
        elif is_numeric:
            coverage = "Adequate" if fill_rate >= 50.0 else "Sparse"
            missing_pol = "NaN in Excel, empty in econometric CSV"
        else:
            coverage = "Adequate" if fill_rate >= 50.0 else "Sparse"
            missing_pol = "NA in Excel, empty in econometric CSV"

        variables.append({
            "col_idx": c,
            "col_letter": col_letter,
            "header": clean_header,
            "chinese_desc": chinese_desc,
            "tier": tier,
            "group": group_name,
            "data_type": dtype,
            "timing_convention": timing,
            "missing_policy": missing_pol,
            "coverage_status": coverage,
            "source": source_desc,
            "stats": stats,
            "values": col_vals,
        })


    cohort_str = cfg.get("dataset", {}).get("cohort", "IPO cohort") if cfg else "IPO cohort"
    summary = {
        "dataset_name": f"HK IPO Main Board {cohort_str} Full Dataset",
        "cohort": cohort_str,
        "workbook_name": book_path.name,
        "sheet": cfg.get("sheet", "NLR") if cfg else "NLR",
        "sample_size": n_companies,
        "variable_count": len(variables),
        "tiers": {
            "green_hkex": sum(1 for v in variables if "浅绿" in v["tier"]),
            "blue_prospectus": sum(1 for v in variables if "浅蓝" in v["tier"]),
            "darkblue_external": sum(1 for v in variables if "深蓝" in v["tier"]),
        },
        "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return variables, summary


def export_clean_csv(variables: list[dict], out_path: Path | None = None) -> Path:
    """导出格式规整、无编码歧义的 UTF-8-BOM CSV 文件。"""
    if out_path is None:
        out_path = ROOT / "out" / "HKIPO_clean.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_rows = variables[0]["stats"]["valid_n"] + variables[0]["stats"]["missing_n"]
    headers = [v["header"] for v in variables]

    with open(out_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for r_idx in range(n_rows):
            row_vals = []
            for v in variables:
                val = v["values"][r_idx]
                if val in (None, "", "NA", "NaN"):
                    row_vals.append("")
                elif isinstance(val, (dt.date, dt.datetime)):
                    row_vals.append(val.strftime("%Y-%m-%d"))
                elif isinstance(val, float):
                    if math.isnan(val) or math.isinf(val):
                        row_vals.append("")
                    else:
                        row_vals.append(f"{int(val)}" if val.is_integer() else f"{val:.6g}")
                else:
                    row_vals.append(str(val).strip())
            writer.writerow(row_vals)

    return out_path


def generate_codebook_markdown(variables: list[dict], summary: dict, out_path: Path | None = None) -> Path:
    """生成详尽的学术计量级数据变量代码本（Markdown 格式）。"""
    cohort = summary.get("cohort", "IPO cohort")
    wb_name = summary.get("workbook_name", "workbook.xlsx")
    clean_csv_name = f"{cohort_artifact_stem(cohort, Path(wb_name).stem)}_clean.csv"
    sheet_name = summary.get("sheet", "NLR")
    if out_path is None:
        tag = cohort.replace(" ", "")
        out_path = ROOT / "out" / f"HKIPO_{tag}_Codebook.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# 香港主板 {cohort} IPO 学术研究数据变量代码本 (Data Codebook)",
        f"\n- **样本规模 (N)**：{summary['sample_size']} 家香港联交所主板新上市公司",
        f"- **变量总数 (K)**：{summary['variable_count']} 维完整跨学科指标",
        f"- **数据层级划分**：浅绿官方基础 ({summary['tiers']['green_hkex']} 列) + 浅蓝招股书披露 ({summary['tiers']['blue_prospectus']} 列) + 深蓝配发及外部衍生 ({summary['tiers']['darkblue_external']} 列)",
        f"- **生成时间**：{summary['generated_at']} | **数据基准**：`{wb_name}` (Sheet: {sheet_name})",
        "\n---",
        "\n## 一、变量层级与来源体系导览",
        "\n| 数据层级 | 覆盖范围 | 列数 | 核心特征与学术用途 |",
        "|---|---|---|---|",
        f"| **浅绿 (HKEX 官方来源)** | 列 A–K | {summary['tiers']['green_hkex']} 列 | 港交所新上市报告官方确证指标：上市编号、代码、保荐人、会计师、公开发售及国际发售募资额、最终定价。 |",
        f"| **浅蓝 (招股书全量来源)** | 招股书法定披露与Pre-IPO结构 | {summary['tiers']['blue_prospectus']} 列 | 发行人招股书披露：资本结构、发售价区间、Pre-IPO VC/PE 投资背景与治理席位、近三年财务与业务指标。 |",
        f"| **深蓝 (配发及外部数据)** | 配发公告与外部市场数据 | {summary['tiers']['darkblue_external']} 列 | 发行结果与市场宏观：基石投资者最终获配及禁售期、回拨机制、超购倍数、自由流通量、首日二级市场表现、恒指收益率、HIBOR、总结余、监管分类。 |",
        "\n---",
        f"\n## 二、{summary['variable_count']} 维全量变量字典详细清单 (Codebook)",
        "\n| 列 | 变量英文名 (Variable Header) | 中文口径释义 | 数据层级 | 数据类型 | 时点约定 | 样本状态 (填报率) | 描述性统计 / 分布特征 |",
        "|---|---|---|---|---|---|---|---|"
    ]

    for v in variables:
        col = f"**{v['col_letter']}**"
        h = f"`{v['header']}`"
        desc = v["chinese_desc"].replace("|", "/")
        tier_short = v["tier"].split("(")[0].strip()
        dtype = v["data_type"].split()[0]
        fill = f"{v['stats']['valid_n']}/{summary['sample_size']} ({v['stats']['fill_rate_pct']}%)"
        cov = v.get("coverage_status", "")
        cov_disp = f"{cov} ({fill})" if cov != "Complete (100%)" else "100% 完备"
        timing_disp = v.get("timing_convention", "-")
        summary_disp = " ".join(v["stats"].get("summary_display", "-").split()).replace("|", "/")
        lines.append(f"| {col} | {h} | {desc} | {tier_short} | `{dtype}` | {timing_disp} | {cov_disp} | {summary_disp} |")


    lines.extend([
        "\n---",
        "\n## 三、计量软件导入指引 (Stata / Python)",
        f"\n配套清洗数据文件：`out/{clean_csv_name}`（编码：UTF-8 with BOM）。",
        "\n### 1. Stata",
        "```stata",
        '* 导入纯净版 CSV 数据',
        f'import delimited "out/{clean_csv_name}", clear bindquote(strict) varnames(1)',
        'describe',
        'summarize',
        '```',
        "\n### 2. Python (pandas)",
        "```python",
        'import pandas as pd',
        f'df = pd.read_csv("out/{clean_csv_name}")',
        'print(df.info())',
        'print(df.describe())',
        '```',
        "\n---\n*本数据代码本由 HK IPO Prospectus Pipeline 自动化分析引擎生成。*"
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def generate_codebook_json(variables: list[dict], summary: dict, out_path: Path | None = None) -> Path:
    """导出结构化 JSON 格式代码本供 Agent 或 API 调用。"""
    if out_path is None:
        out_path = ROOT / "out" / "HKIPO_Codebook.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "summary": summary,
        "variables": [{k: v for k, v in item.items() if k != "values"} for item in variables]
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out_path


def export_all(cfg: dict | None = None, out_dir: Path | str | None = None) -> dict:
    """一键执行代码本构建、CSV 导出与 JSON 生成。"""
    if cfg is None:
        cfg = load_cfg()
    variables, summary = build_codebook(cfg)
    cohort = summary.get("cohort", "IPO cohort")
    tag = cohort.replace(" ", "")
    dataset_id = cfg.get("dataset", {}).get("id", Path(cfg["workbook"]).stem) if cfg else "HKIPO"

    csv_name = f"{cohort_artifact_stem(cohort, dataset_id)}_clean.csv"
    md_name = f"HKIPO_{tag}_Codebook.md"
    json_name = f"HKIPO_{tag}_Codebook.json"

    if out_dir is not None:
        od = Path(out_dir)
        od.mkdir(parents=True, exist_ok=True)
        csv_path = export_clean_csv(variables, out_path=od / csv_name)
        md_path = generate_codebook_markdown(variables, summary, out_path=od / md_name)
        json_path = generate_codebook_json(variables, summary, out_path=od / json_name)
    else:
        out_root = cfg["paths"]["out"] if (cfg and "paths" in cfg and "out" in cfg["paths"]) else ROOT / "out"
        out_root.mkdir(parents=True, exist_ok=True)
        csv_path = export_clean_csv(variables, out_path=out_root / csv_name)
        md_path = generate_codebook_markdown(variables, summary, out_path=out_root / md_name)
        json_path = generate_codebook_json(variables, summary, out_path=out_root / json_name)

    # 发布到规范工件目录（仅默认流水线运行；测试的 out_dir 隔离不受影响）
    if out_dir is None:
        from paths import codebooks_dir as layout_codebooks_dir, exports_dir as layout_exports_dir
        codebooks_dir = layout_codebooks_dir(WS)
        exports_dir = layout_exports_dir(WS)
        codebooks_dir.mkdir(parents=True, exist_ok=True)
        exports_dir.mkdir(parents=True, exist_ok=True)
        (codebooks_dir / md_name).write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")
        shutil.copyfile(csv_path, exports_dir / csv_name)
        print("已发布: codebooks/" + md_name + " | exports/" + csv_name)

    print("\n" + "=" * 70)
    print("HK IPO 学术代码本与科研 CSV 导出完成")
    print("=" * 70)
    print(f"样本规模: {summary['sample_size']} 家公司 | 已解析表头: {summary['variable_count']} 列（非空值覆盖请查看 audit）")
    print(f"数据层级: 浅绿 (HKEX) {summary['tiers']['green_hkex']} 列 | 浅蓝 (招股书) {summary['tiers']['blue_prospectus']} 列 | 深蓝 (外部/配发) {summary['tiers']['darkblue_external']} 列")
    print("-" * 70)
    print("产出成果文件:")
    print(f"  - 计量分析纯净 CSV:  {csv_path}")
    print(f"  - 学术数据代码本 MD: {md_path}")
    print(f"  - 结构化变量元数据:  {json_path}")
    print("=" * 70 + "\n")

    return {
        "csv_path": str(csv_path),
        "md_path": str(md_path),
        "json_path": str(json_path),
        "variable_count": summary["variable_count"],
        "sample_size": summary["sample_size"]
    }


def main():
    export_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
