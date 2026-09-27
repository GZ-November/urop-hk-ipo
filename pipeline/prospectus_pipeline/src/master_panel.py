#!/usr/bin/env python3
"""跨 cohort 分析准备面板：变量注册表 + Master 合并 + 漂移报告。

功能：
  1. `build_registry`：解析各季度 Markdown Codebook 中的 202 维变量定义，
     合成单一机器可读变量注册表（YAML，纳入版本控制）；
     跨 cohort 定义冲突逐条记录，以最新 cohort 口径为准。
  2. `build_master`：把各季度 `_clean.csv` 合并成单张 master 面板
     （首列新增 cohort 标识），并生成漂移报告：
     - 表头跨 cohort 对齐（顺序敏感）；
     - 表头 vs 注册表校验；
     - cohort 内与跨 cohort 重复股票代码；
     - 上市日期与 cohort 季度一致性（警告级）；
     - 逐变量填报率（跨 cohort 对比）。

约定：
  - 只依赖标准库 + pyyaml，与 codebook.py 的导出保持一致（UTF-8 with BOM）；
  - master/漂移报告写入工作簿所在目录（WS），与 `_clean.csv` 同级，均为本地产物；
  - 注册表 YAML 为版本控制文件，是列名/类型/层级的单一事实来源。
"""
from __future__ import annotations

import csv
import datetime as dt
import math
import re
from pathlib import Path
from typing import Any

import yaml

from paths import (  # noqa: E402
    CODEBOOKS as CODEBOOKS_SUBDIR, EXPORTS as EXPORTS_SUBDIR, MASTER_STEM,
    REGISTRY_NAME, REPORTS as REPORTS_SUBDIR,
    codebook_md_path, drift_report_path, exports_dir, exclusions_path, master_csv_path,
    registry_path as layout_registry_path,
)

COHORT_CSV_RE = re.compile(r"^HKIPO-MB(\d{4}Q[1-4])_clean\.csv$")

LAYER_MAP = {
    "浅绿": "official_hkex",
    "浅蓝": "prospectus",
    "深蓝": "allotment_external",
}

MISSING_TOKENS = {"", "nan", "na", "n/a", "#n/a", "none", "null"}

# Codebook 法定恒等式（招股书股数口径）：
#   L = N + Q  （总股数 = 资本化发行 + 新股）
#   L = O + M  （总股数 = 资本化发行 + 全球发售股数）
#   M = Q + P  （全球发售 = 新股 + 老股出售）
IDENTITY_CHECKS = [
    ("L = N + Q", "Total (without option)",
     ["Number of offer shares under the capitalization Issue", "New shares"]),
    ("L = O + M", "Total (without option)",
     ["Number of offer shares under Capitalization Rest", "Global Offering (without option)"]),
    ("M = Q + P", "Global Offering (without option)",
     ["New shares", "Sale Shares"]),
]
IDENTITY_TOLERANCE = 1.0  # 股数为整数口径，允许 ±1 舍入

# 免汇率派生变量（分母子同币种，比率单位无关；财务列为原币种 × 单位乘数）
DERIVED_SPECS = [
    ("leverage_y1", ["total liability in year-1", "total assets in year-1"]),
    ("roa_y1", ["Profit for the year in year-1", "total assets in year-1"]),
    ("sales_growth_y1", ["Net sales in year-1", "Net sales in year-2"]),
    ("log_proceeds_hkd", ["Total (without option)"]),
    ("public_offer_fraction", ["Public Offer shares", "New shares"]),
]

VAR_ROW_RE = re.compile(r"^\|\s*\*\*([A-Z]{1,3})\*\*\s*\|")


# --------------------------------------------------------------------------- #
# 基础工具
# --------------------------------------------------------------------------- #

def slugify(header: str) -> str:
    """原始表头 -> 稳定的 snake_case 分析变量名。"""
    s = header.strip().lower()
    s = s.replace("(1=yes; 0=no)", "").replace("(dd/mm/yy)", "")
    s = s.replace("%", " pct ").replace("#", " no ")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "var"


def column_letter(idx0: int) -> str:
    """0 基列索引 -> 电子表格列字母（0 -> A）。"""
    letters = ""
    idx0 += 1
    while idx0:
        idx0, rem = divmod(idx0 - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def parse_date(value: Any) -> dt.date | None:
    """兼容导出 CSV 中的日期写法：YYYY-MM-DD、dd/mm/yy、dd/mm/yyyy。"""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.split(" ")[0]
    for fmt in ("%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def quarter_bounds(tag: str) -> tuple[dt.date, dt.date]:
    """cohort 标签（如 2026Q3）-> 该季度自然日起止。"""
    year, quarter = int(tag[:4]), int(tag[-1])
    start_month = 3 * (quarter - 1) + 1
    start = dt.date(year, start_month, 1)
    end_month = start_month + 3
    end = dt.date(year, end_month, 1) - dt.timedelta(days=1) if end_month <= 12 else dt.date(year, 12, 31)
    return start, end


def discover_cohort_csvs(ws: Path) -> list[tuple[str, Path]]:
    """exports/ 目录下的 cohort clean CSV，按 cohort 标签升序。"""
    found = []
    for path in exports_dir(ws).glob("HKIPO-MB*_clean.csv"):
        m = COHORT_CSV_RE.match(path.name)
        if m:
            found.append((m.group(1), path))
    return sorted(found)


def read_cohort_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        headers = next(reader)
        rows = [row for row in reader]
    return headers, rows


def _cell_missing(value: Any) -> bool:
    return str(value).strip().lower() in MISSING_TOKENS


def _num(value: Any) -> float | None:
    """CSV 单元格 -> float；缺失或不可解析返回 None。"""
    text = str(value).strip().replace(",", "")
    if text.lower() in MISSING_TOKENS:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def check_identities(
    headers: list[str], rows: list[list[str]], tag: str
) -> tuple[list[dict[str, str]], list[str]]:
    """按行校验股数恒等式；返回 (违规明细, 因缺列而跳过的恒等式名)。"""
    idx = {h: i for i, h in enumerate(headers)}
    violations: list[dict[str, str]] = []
    skipped: list[str] = []
    for name, lhs, rhs_parts in IDENTITY_CHECKS:
        involved = [lhs] + rhs_parts
        if any(h not in idx for h in involved):
            skipped.append(name)
            continue
        for row_no, row in enumerate(rows, start=2):  # 含表头的 CSV 行号
            values = [
                _num(row[idx[h]]) if idx[h] < len(row) else None for h in involved
            ]
            if any(v is None for v in values):
                continue
            lhs_v, rhs_v = values[0], sum(values[1:])
            if abs(lhs_v - rhs_v) > IDENTITY_TOLERANCE:
                code = row[idx["Stock Code"]] if "Stock Code" in idx and idx["Stock Code"] < len(row) else "?"
                violations.append({
                    "identity": name,
                    "cohort": tag,
                    "code": code,
                    "row": str(row_no),
                    "detail": f"{lhs}={lhs_v:,.0f} vs {' + '.join(rhs_parts)}={rhs_v:,.0f}",
                })
    return violations, skipped


def compute_derived_columns(
    headers: list[str], rows: list[list[str]]
) -> tuple[list[str], list[list[str]], list[str]]:
    """计算免汇率派生比率列；返回 (新列名, 新列值矩阵, 缺源跳过的列名)。

    只保留源表头齐全的派生列；比率分母为 0 或任一输入缺失时填 NaN。
    """
    idx = {h: i for i, h in enumerate(headers)}
    added: list[str] = []
    skipped: list[str] = []
    columns: list[list[str]] = []
    for name, sources in DERIVED_SPECS:
        if any(h not in idx for h in sources):
            skipped.append(name)
            continue
        added.append(name)
        values: list[str] = []
        if len(sources) == 1:
            for row in rows:
                v = _num(row[idx[sources[0]]]) if idx[sources[0]] < len(row) else None
                values.append("NaN" if v is None or v <= 0 else f"{math.log(v):.6f}")
        else:
            for row in rows:
                nums = [_num(row[idx[h]]) if idx[h] < len(row) else None for h in sources]
                if any(v is None for v in nums) or nums[1] == 0:
                    values.append("NaN")
                elif name == "sales_growth_y1":
                    values.append(f"{nums[0] / nums[1] - 1:.6f}")
                else:
                    values.append(f"{nums[0] / nums[1]:.6f}")
        columns.append(values)
    return added, columns, skipped


# --------------------------------------------------------------------------- #
# 变量注册表
# --------------------------------------------------------------------------- #

def parse_codebook_variables(md_path: Path) -> dict[str, dict[str, str]]:
    """从单个 Markdown Codebook 解析变量定义：letter -> 定义字段。"""
    variables: dict[str, dict[str, str]] = {}
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = VAR_ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.split("|")]
        # ['', '**A**', '`header`', 中文释义, 层级, '`type`', 时点约定, 填报状态, 统计, '']
        if len(cells) < 8:
            continue
        letter = m.group(1)
        if letter in variables:
            raise ValueError(f"{md_path.name}: 列 {letter} 在变量表中出现多次")
        variables[letter] = {
            "header": cells[2].strip("`").strip(),
            "description_zh": cells[3],
            "layer_raw": cells[4],
            "dtype": cells[5].strip("`").strip(),
            "timing": cells[6],
            "coverage_raw": cells[7],
        }
    return variables


def _coverage_pct(coverage_cell: str) -> float:
    """填报状态单元格 -> 覆盖率（%）："100% 完备" -> 100，"Sparse (2/23 (8.7%))" -> 8.7。"""
    pcts = [float(m) for m in re.findall(r"(\d+(?:\.\d+)?)\s*%", coverage_cell or "")]
    return max(pcts) if pcts else 0.0


def _layer_en(layer_raw: str) -> str:
    for key, value in LAYER_MAP.items():
        if key in layer_raw:
            return value
    return "unclassified"


def _unit_for(header: str, dtype: str) -> str | None:
    if "(1=yes; 0=no)" in header:
        return "binary"
    if "(HK$)" in header:
        return "HKD"
    if "(%)" in header:
        return "percent"
    if "(years)" in header:
        return "years"
    if "(shares)" in header:
        return "shares"
    if dtype == "date":
        return "date"
    if re.search(r"in year-[123]", header) or header.startswith(
        ("Cash and cash equivalents", "Operating cash flow", "R&D", "Development costs", "Top 5 customers")
    ):
        # 财务报表科目：原币种 × Financial statement unit multiplier（逐行见工作簿）
        return "reporting_currency_raw"
    return None


def build_registry(
    ws: Path,
    out_path: Path | None = None,
    codebook_names: list[str] | None = None,
) -> dict[str, Any]:
    """合并各季度 Codebook 变量定义，生成注册表 YAML。

    冲突处理：同列名/类型/层级在 cohort 间不一致时，以文件名排序最新的
    Codebook 为准，并把冲突逐条写入 meta.conflicts。
    """
    names = codebook_names or sorted((Path(ws) / CODEBOOKS_SUBDIR).glob("HKIPO_*_Codebook.md"))
    if not names:
        raise FileNotFoundError(f"{ws} 下未找到任何 HKIPO_*_Codebook.md")
    paths = [Path(n) if isinstance(n, str) else n for n in names]

    per_book = {p.name: parse_codebook_variables(p) for p in paths}
    latest_book = max(per_book)  # 文件名含 cohort 标签，字典序即时间序
    latest = per_book[latest_book]

    conflicts: list[dict[str]] = []
    variables: list[dict[str, Any]] = []
    used_slugs: set[str] = set()
    for letter in sorted(latest, key=lambda x: (len(x), x)):
        definition = latest[letter]
        # 声明类型：取自数据覆盖率最高的季度 Codebook（避免被空列的推断翻转）；
        # 覆盖率并列时取最新季度
        declared_dtype = None
        declared_from = None
        best_coverage = -1.0
        for book in sorted(per_book):
            table = per_book[book]
            if letter not in table:
                continue
            coverage = _coverage_pct(table[letter].get("coverage_raw", ""))
            if coverage >= best_coverage:
                best_coverage = coverage
                declared_dtype = table[letter]["dtype"]
                declared_from = book
        for book, table in per_book.items():
            if book == latest_book or letter not in table:
                continue
            for field in ("header", "dtype", "timing"):
                if table[letter][field] != definition[field]:
                    conflicts.append({
                        "letter": letter,
                        "field": field,
                        "latest": definition[field],
                        "cohort_book": book,
                        "value": table[letter][field],
                    })
        slug = slugify(definition["header"])
        while slug in used_slugs:
            slug += "_x"
        used_slugs.add(slug)
        variables.append({
            "letter": letter,
            "header": definition["header"],
            "slug": slug,
            "dtype": definition["dtype"],
            "declared_dtype": declared_dtype,
            "declared_from": declared_from,
            "layer": _layer_en(definition["layer_raw"]),
            "timing": definition["timing"],
            "unit": _unit_for(definition["header"], definition["dtype"]),
            "description_zh": definition["description_zh"],
        })

    conflict_summary: dict[str, dict[str, list[str]]] = {}
    for c in conflicts:
        transition = f"{c['value']} -> {c['latest']}"
        letters = conflict_summary.setdefault(c["field"], {}).setdefault(transition, [])
        if c["letter"] not in letters:
            letters.append(c["letter"])

    registry = {
        "meta": {
            "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
            "generated_from": [p.name for p in paths],
            "authoritative_codebook": latest_book,
            "variables_per_codebook": {book: len(table) for book, table in per_book.items()},
            "variable_count": len(variables),
            "conflict_count": len(conflicts),
            "conflict_summary": conflict_summary,
            "conflicts": conflicts,
            "note": "变量定义单一事实来源；季度 Codebook 由工作簿导出，口径以本注册表对齐。",
        },
        "variables": variables,
    }
    if out_path is not None:
        out_path.write_text(
            yaml.safe_dump(registry, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    return registry


def load_registry(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "variables" not in data:
        raise ValueError(f"注册表格式无效：{path}")
    return data


# --------------------------------------------------------------------------- #
# Master 合并与漂移报告
# --------------------------------------------------------------------------- #

def _check_headers(base: list[str], other: list[str]) -> dict[str, Any]:
    extra = [h for h in other if h not in base]
    missing = [h for h in base if h not in other]
    order_same = other == base
    return {"order_same": order_same, "extra": extra, "missing": missing}


def build_master(
    ws: Path,
    registry_path: Path | None = None,
    out_dir: Path | None = None,
    master_stem: str = MASTER_STEM,
    derive: bool = False,
) -> dict[str, Any]:
    """合并全部 cohort clean CSV 为 master 面板，并生成漂移报告。

    返回 summary dict；表头漂移 / 注册表不一致 / 重复代码记为 hard error。
    """
    cohorts = discover_cohort_csvs(ws)
    if not cohorts:
        raise FileNotFoundError(f"{ws} 下未找到任何 HKIPO-MB*_clean.csv")

    tables: dict[str, tuple[list[str], list[list[str]]]] = {}
    for tag, path in cohorts:
        tables[tag] = read_cohort_csv(path)
    tags = [tag for tag, _ in cohorts]
    base_tag, base_headers = tags[0], tables[tags[0]][0]

    header_issues = {
        tag: _check_headers(base_headers, tables[tag][0]) for tag in tags[1:]
    }
    headers_aligned = all(issue["order_same"] and not issue["extra"] and not issue["missing"]
                          for issue in header_issues.values())

    # 注册表校验
    registry_notes: list[str] = []
    registry_ok: bool | None = None
    registry = None
    if registry_path and Path(registry_path).exists():
        registry = load_registry(registry_path)
        reg_vars = registry["variables"]
        expected_headers = [v["header"] for v in reg_vars]
        if expected_headers == base_headers:
            registry_ok = True
        else:
            registry_ok = False
            if len(expected_headers) != len(base_headers):
                registry_notes.append(
                    f"列数不一致：注册表 {len(expected_headers)} vs CSV {len(base_headers)}")
            for i, (want, got) in enumerate(zip(expected_headers, base_headers)):
                if want != got:
                    registry_notes.append(
                        f"第 {i + 1} 列（{column_letter(i)}）：注册表 `{want}` vs CSV `{got}`")
            if len(expected_headers) > len(base_headers):
                for v in reg_vars[len(base_headers):]:
                    registry_notes.append(f"注册表多出列 {v['letter']} `{v['header']}`")
            elif len(base_headers) > len(expected_headers):
                for i in range(len(expected_headers), len(base_headers)):
                    registry_notes.append(f"CSV 多出列 `{base_headers[i]}`")

    # 每个 cohort 的行级检查
    per_cohort: dict[str, dict[str, Any]] = {}
    duplicate_codes: dict[str, list[str]] = {}
    date_violations: dict[str, list[str]] = {}
    fill_rates: dict[str, dict[str, float]] = {}
    seen_codes: dict[str, set[str]] = {}
    cross_cohort_dupes: set[str] = set()

    for tag in tags:
        headers, rows = tables[tag]
        code_idx = headers.index("Stock Code") if "Stock Code" in headers else None
        codes = [row[code_idx] if code_idx is not None and code_idx < len(row) else ""
                 for row in rows]
        dups = sorted({c for c in codes if codes.count(c) > 1})
        if dups:
            duplicate_codes[tag] = dups
        for code in codes:
            if not _cell_missing(code):
                seen_codes.setdefault(code, set()).add(tag)
        cross_cohort_dupes = {c for c, ts in seen_codes.items() if len(ts) > 1}

        q_start, q_end = quarter_bounds(tag)
        listing_idx = headers.index("Date of Listing (dd/mm/yy)") if "Date of Listing (dd/mm/yy)" in headers else None
        violations = []
        if listing_idx is not None:
            for row in rows:
                listing = parse_date(row[listing_idx]) if listing_idx < len(row) else None
                if listing and not (q_start <= listing <= q_end):
                    violations.append(
                        f"{row[headers.index('Stock Code')] if 'Stock Code' in headers else '?'} "
                        f"上市日 {listing} 不在 {tag}（{q_start}~{q_end}）内")
        date_violations[tag] = violations

        fill: dict[str, float] = {}
        for i, header in enumerate(headers):
            filled = sum(1 for row in rows if i < len(row) and not _cell_missing(row[i]))
            fill[header] = round(100.0 * filled / len(rows), 1) if rows else 0.0
        fill_rates[tag] = fill

        per_cohort[tag] = {
            "rows": len(rows),
            "duplicate_codes": dups,
            "date_violations": violations,
        }

    # 恒等式校验（面板级监控，警告级）
    identity_violations: list[dict[str, str]] = []
    identities_skipped: list[str] = []
    for tag in tags:
        violations, skipped = check_identities(tables[tag][0], tables[tag][1], tag)
        identity_violations.extend(violations)
        for name in skipped:
            if name not in identities_skipped:
                identities_skipped.append(name)

    # 免汇率派生比率列（可选）
    derived_columns: list[str] = []
    derived_skipped: list[str] = []
    derived_values: dict[str, list[list[str]]] = {}
    if derive:
        for tag in tags:
            added, cols, skipped = compute_derived_columns(tables[tag][0], tables[tag][1])
            derived_values[tag] = cols
            if not derived_columns:
                derived_columns, derived_skipped = added, skipped

    # 填报率跨 cohort 对比：只保留任一 cohort < 100% 的列
    low_fill = {}
    for header in base_headers:
        rates = {tag: fill_rates[tag].get(header) for tag in tags}
        present = [r for r in rates.values() if r is not None]
        if present and min(present) < 100.0:
            low_fill[header] = rates

    # 填报率环比：最近两个 cohort 的变化（|Δ| ≥ 10pp，抓新季度抽取质量下滑）
    fill_rate_deltas: dict[str, dict[str, float]] = {}
    if len(tags) >= 2:
        prev_tag, last_tag = tags[-2], tags[-1]
        for header in base_headers:
            prev_rate = fill_rates[prev_tag].get(header)
            last_rate = fill_rates[last_tag].get(header)
            if prev_rate is None or last_rate is None:
                continue
            delta = round(last_rate - prev_rate, 1)
            if abs(delta) >= 10.0:
                fill_rate_deltas[header] = {
                    "prev_cohort": prev_tag, "last_cohort": last_tag,
                    "from": prev_rate, "to": last_rate, "delta": delta,
                }

    # 布尔列空值：注册表 dtype=boolean 的列按约定必须填 0/1，不得留空
    boolean_fill_gaps: dict[str, dict[str, float]] = {}
    if registry is not None:
        bool_headers = [v["header"] for v in registry["variables"] if v.get("dtype") == "boolean"]
        for header in bool_headers:
            rates = {tag: fill_rates[tag][header] for tag in tags if header in fill_rates[tag]}
            if rates and min(rates.values()) < 100.0:
                boolean_fill_gaps[header] = rates

    hard_errors = bool(
        (not headers_aligned) or duplicate_codes or cross_cohort_dupes
        or (registry_ok is False)
    )

    # 写 master CSV（cohort 与跨 cohort 重复标记作为前两列）
    master_path = Path(out_dir) / f"{master_stem}_clean.csv" if out_dir else master_csv_path(ws, master_stem)
    master_path.parent.mkdir(parents=True, exist_ok=True)
    code_idx = base_headers.index("Stock Code") if "Stock Code" in base_headers else None
    with master_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["cohort", "cross_cohort_duplicate"] + base_headers + derived_columns)
        for tag in tags:
            cols = derived_values.get(tag, [])
            for i, row in enumerate(tables[tag][1]):
                code = row[code_idx] if code_idx is not None and code_idx < len(row) else ""
                flag = 1 if code in cross_cohort_dupes else 0
                extra = [c[i] for c in cols]
                writer.writerow([tag, flag] + row + extra)

    total_rows = sum(per_cohort[tag]["rows"] for tag in tags)
    summary = {
        "cohorts": per_cohort,
        "cohort_order": tags,
        "total_rows": total_rows,
        "variable_count": len(base_headers),
        "headers_aligned": headers_aligned,
        "header_issues": header_issues,
        "registry_ok": registry_ok,
        "registry_notes": registry_notes,
        "duplicate_codes": duplicate_codes,
        "cross_cohort_duplicate_codes": sorted(cross_cohort_dupes),
        "cross_cohort_duplicate_details": {
            code: sorted(seen_codes[code]) for code in sorted(cross_cohort_dupes)
        },
        "date_violations": date_violations,
        "identity_violations": identity_violations,
        "identities_skipped": identities_skipped,
        "derived_columns": derived_columns,
        "derived_skipped": derived_skipped,
        "low_fill_columns": low_fill,
        "fill_rate_deltas": fill_rate_deltas,
        "boolean_fill_gaps": boolean_fill_gaps,
        "hard_errors": hard_errors,
        "master_csv": str(master_path),
    }

    report_path = Path(out_dir) / f"{master_stem}_Drift_Report.md" if out_dir else drift_report_path(ws, master_stem)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    _write_report(report_path, summary, registry is not None)
    summary["drift_report"] = str(report_path)
    return summary


def _write_report(path: Path, s: dict[str, Any], has_registry: bool) -> None:
    lines: list[str] = []
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"# Master 面板漂移报告 ({s['cohort_order'][0]} ~ {s['cohort_order'][-1]})")
    lines.append("")
    lines.append(f"- **生成时间**：{now} | **cohort 数**：{len(s['cohort_order'])} | "
                 f"**样本合计**：{s['total_rows']} 家 | **变量数**：{s['variable_count']}")
    lines.append(f"- **复现命令**：`python3 run.py master`")
    lines.append(f"- **Master 数据**：`{Path(s['master_csv']).name}`（cohort 列已前置，本地产物不入库）")
    if s.get("derived_columns"):
        lines.append(f"- **派生比率列**：{', '.join(s['derived_columns'])}（免汇率，`--derive` 生成）")
    lines.append("")

    status = "✅ 通过" if s["headers_aligned"] else "❌ 漂移"
    lines.append(f"## 1. 表头跨 cohort 对齐：{status}")
    lines.append("")
    if s["headers_aligned"]:
        lines.append(f"全部 {len(s['cohort_order'])} 个 cohort 的 {s['variable_count']} 列表头完全一致（顺序敏感）。")
    else:
        for tag, issue in s["header_issues"].items():
            lines.append(f"- **{tag}**：order_same={issue['order_same']}，"
                         f"多出 {issue['extra']}，缺失 {issue['missing']}")
    lines.append("")

    if has_registry:
        ok = s["registry_ok"]
        lines.append(f"## 2. 注册表校验（HKIPO_Variable_Registry.yaml）：{'✅ 一致' if ok else '❌ 不一致'}")
        lines.append("")
        if not ok:
            lines.extend(f"- {note}" for note in s["registry_notes"])
        else:
            lines.append("CSV 表头与注册表逐列一致（列名 + 顺序）。")
        lines.append("")
    else:
        lines.append("## 2. 注册表校验：⚠️ 未找到注册表文件")
        lines.append("")
        lines.append("先运行 `python3 run.py registry` 生成注册表，再重跑 master。")
        lines.append("")

    lines.append("## 3. 样本与重复检查")
    lines.append("")
    lines.append("| cohort | 样本数 | cohort 内重复代码 |")
    lines.append("|---|---|---|")
    for tag in s["cohort_order"]:
        dups = s["duplicate_codes"].get(tag) or []
        lines.append(f"| {tag} | {s['cohorts'][tag]['rows']} | {', '.join(dups) if dups else '无'} |")
    lines.append("")
    if s["cross_cohort_duplicate_codes"]:
        lines.append(f"**❌ 跨 cohort 重复股票代码 {len(s['cross_cohort_duplicate_codes'])} 只**"
                     f"（同一发行人被多个工作簿收录，合并分析时须去重，master 中 "
                     f"`cross_cohort_duplicate` 列已标记）：")
        lines.append("")
        for code in s["cross_cohort_duplicate_codes"]:
            cohorts = "、".join(s["cross_cohort_duplicate_details"][code])
            lines.append(f"- {code}：{cohorts}")
    else:
        lines.append("✅ 无跨 cohort 重复股票代码。")
    lines.append("")

    lines.append("## 4. 上市日期与 cohort 季度一致性（警告级）")
    lines.append("")
    total_violations = sum(len(v) for v in s["date_violations"].values())
    if total_violations == 0:
        lines.append("全部样本的上市日期落在所属 cohort 的自然季度内。")
    else:
        for tag, violations in s["date_violations"].items():
            if violations:
                lines.append(f"**{tag}**（{len(violations)} 条）：")
                lines.append("")
                lines.extend(f"- {v}" for v in violations)
    lines.append("")

    lines.append("## 5. 填报率监控（任一 cohort < 100% 的列）")
    lines.append("")
    if not s["low_fill_columns"]:
        lines.append("全部变量在全部 cohort 填报率均为 100%。")
    else:
        tags = s["cohort_order"]
        header_row = "| 变量 | " + " | ".join(tags) + " |"
        lines.append(header_row)
        lines.append("|---" * (len(tags) + 1) + "|")
        for header, rates in s["low_fill_columns"].items():
            cells = " | ".join(
                f"{rates[tag]:.1f}%" if rates.get(tag) is not None else "—" for tag in tags)
            lines.append(f"| `{header}` | {cells} |")
    lines.append("")

    lines.append("### 5.1 填报率环比（最近两个 cohort，|Δ| ≥ 10pp）")
    lines.append("")
    if not s["fill_rate_deltas"]:
        lines.append("最近两个 cohort 之间没有 ≥10pp 的填报率变化。")
    else:
        lines.append("| 变量 | 上一 cohort | 最新 cohort | 变化 |")
        lines.append("|---|---|---|---|")
        for header, d in s["fill_rate_deltas"].items():
            sign = "+" if d["delta"] > 0 else ""
            lines.append(f"| `{header}` | {d['from']:.1f}% | {d['to']:.1f}% | {sign}{d['delta']:.1f}pp |")
    lines.append("")

    lines.append("### 5.2 布尔列空值警告（约定：0/1 不得留空）")
    lines.append("")
    if not s["boolean_fill_gaps"]:
        lines.append("全部布尔列在所有 cohort 均为 0/1 填报，无空值。")
    else:
        tags = s["cohort_order"]
        lines.append("| 布尔列 | " + " | ".join(tags) + " |")
        lines.append("|---" * (len(tags) + 1) + "|")
        for header, rates in s["boolean_fill_gaps"].items():
            cells = " | ".join(f"{rates[tag]:.1f}%" if tag in rates else "—" for tag in tags)
            lines.append(f"| `{header}` | {cells} |")
        lines.append("")
        lines.append("处置：确认「确无」后补 0（或按手册填 NA），重跑 export 与 master。")
    lines.append("")

    lines.append("## 6. 股数恒等式校验（警告级，容差 ±1 股）")
    lines.append("")
    if s["identities_skipped"]:
        lines.append(f"⚠️ 因面板缺列跳过：{', '.join(s['identities_skipped'])}")
    violations = s["identity_violations"]
    if not violations:
        lines.append("✅ 全部可评估样本满足恒等式 L = N + Q、L = O + M、M = Q + P。")
    else:
        by_identity: dict[str, int] = {}
        for v in violations:
            by_identity[v["identity"]] = by_identity.get(v["identity"], 0) + 1
        for name in ("L = N + Q", "L = O + M", "M = Q + P"):
            lines.append(f"- {name}：违规 {by_identity.get(name, 0)} 行")
        lines.append("")
        for v in violations[:30]:
            lines.append(f"- `{v['cohort']}` 第 {v['row']} 行 {v['code']}：{v['detail']}")
        if len(violations) > 30:
            lines.append(f"- ...其余 {len(violations) - 30} 条从略")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
