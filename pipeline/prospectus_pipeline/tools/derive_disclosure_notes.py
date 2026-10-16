#!/usr/bin/env python3
"""派生「披露附注」10 列（Continuation of the template's disclosure-notes block）.

模板里以下 10 列此前一直 0/60，代码本归类为 "Reserved / Unmatured"，
但它们**并非无法获得**，而是可以从已抽取的 70 个字段确定性派生：

| 列 | 含义 | 派生方式 |
|---|---|---|
| BC  | Comments (nearest sales & profit adjustment factor - original data duration in year) | year-1 覆盖月数 / 12 |
| CG  | Financial statement unit multiplier | 由「披露值 vs 存储值」推断（'000 -> 1000） |
| CI/CJ | Year-3 financial period start / end | year-2 之前的完整财年 |
| CK/CL | Year-2 financial period start / end | year-1 之前的完整财年 |
| CM  | Year-1 financial period start | year-1（可为存根）期初 |
| CN  | Year-1 net sales (original, pre-annualization) | 年化值 × BC |
| CO  | Year-1 profit before tax (original) | 年化值 × BC |
| CP  | Year-1 profit for period (original) | 年化值 × BC |

口径全部以 2026Q1 权威成品（HKIPO-MB2026Q1.xlsx，38/38 已填）反解并逐行验证：

- `BC` 分布 0.5 / 0.6667 / 0.75 / 0.8333 对应 year-1 期末 06-30 / 08-31 / 09-30 / 10-31；
- **年化值 ÷ 原值恒等于 1/BC**（38 行全部成立，例如 BC=0.5 时比值精确为 2.0000）；
- `CM` 恒为期初（2025-01-01），`CI/CJ`、`CK/CL` 为 year-3 / year-2 的整年区间；
- `CG` 37 家为 1000、1 家为 1000000。

year-1 的月数不能只凭 col_AT 的月日推断（6 月 30 日既可能是 6M 存根，也可能是 6 月结账的
完整财年）。月数取自 src/periods.py：优先用页级全文判定的 Track Record Period（须与 col_AT
同一期末），否则用抽取 JSON 中年化值与引文原值之比（col_AH/AK/AN）；两者冲突或都缺失时
跳过该公司并列明原因，绝不猜测。

用法：
    python tools/derive_disclosure_notes.py [--book ../HKIPO-MB2026Q2.xlsx] [--only 6656.HK ...]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import timedelta
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from periods import parse_date, payload_months, period_ending, resolve  # noqa: E402
from workbook_transaction import workbook_transaction  # noqa: E402
from write_back import resolve_columns  # noqa: E402
from run import load_cfg  # noqa: E402

# 派生只读取这 4 个抽取字段；GEM 模板合法删除了主板专列，不能要求全部表头。
SOURCE_FIELDS = ("col_AT", "col_AH", "col_AK", "col_AN")

# 派生列（模板表头 -> 列名就地解析，不依赖历史字母键）
TARGETS = {
    "BC": "Comments (nearest sales& profit adjustment factor",
    "CG": "Financial statement unit multiplier",
    "CI": "Year-3 financial period start",
    "CJ": "Year-3 financial period end",
    "CK": "Year-2 financial period start",
    "CL": "Year-2 financial period end",
    "CM": "Year-1 financial period start",
    "CN": "Year-1 net sales (original, pre-annualization)",
    "CO": "Year-1 profit before tax (original)",
    "CP": "Year-1 profit for period (original)",
}

def year1_periods(code: str, fields: dict, text_dir: Path) -> tuple[dict | None, str]:
    """Return {"year1", "year2", "year3"} Periods for one issuer, or (None, reason)."""
    end = parse_date((fields.get("col_AT") or {}).get("value"))
    if end is None:
        return None, "无有效 year-1 期末日（col_AT）"
    implied = payload_months(fields)
    text_file = text_dir / f"HKIPO-MB{''.join(ch for ch in code if ch.isdigit())}.jsonl"
    if text_file.exists():
        pages = [json.loads(line) for line in text_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        tr = resolve(pages)
        if tr.status == "ok":
            if tr.year1.end != end:
                return None, (f"col_AT={end} 与 Track Record 判定的 year-1 期末 {tr.year1.end} 不一致"
                              "（期间锚定错误，先修抽取）")
            if implied is not None and implied != tr.year1.months:
                return None, (f"年化值/引文原值隐含 {implied} 个月，但 Track Record 判定 year-1 为 "
                              f"{tr.year1.months} 个月（年化错误）")
            return {"year1": tr.year1, "year2": tr.year2, "year3": tr.year3}, "track_record"
    if implied is None:
        return None, "无法确定 year-1 期间长度（无页级全文判定，且年化值无法与引文原值对上）"
    year1 = period_ending(end, implied)
    year2 = period_ending(year1.start - timedelta(days=1), 12)
    year3 = period_ending(year2.start - timedelta(days=1), 12)
    return {"year1": year1, "year2": year2, "year3": year3}, "payload_annualisation"


def infer_multiplier(rec: dict, key: str, value=None) -> int | None:
    """由「存储值 ÷ 引文中的数字」推断财报单位乘数。

    ``value`` overrides the stored value: annualised fields must be compared at their
    original-period size, or a stub's comparative-period number can match a wrong unit.
    """
    entry = (rec.get("fields") or {}).get(key) or {}
    quote = entry.get("quote") or ""
    value = entry.get("value") if value is None else value
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not value:
        return None
    nums = []
    for tok in re.findall(r"\d[\d,\.]*", str(quote)):
        t = tok.replace(",", "").rstrip(".")
        try:
            f = float(t)
        except ValueError:
            continue
        if f:
            nums.append(f)
    if not nums:
        return None
    # Stored values are the quoted figure times the unit, so the ratio is exact up to
    # rounding. A loose tolerance lets an unrelated number in the quote (a comparative
    # period, a year, a note number) match a wrong unit, so require 0.1% and rank by
    # relative error.
    best = None
    for n in nums:
        r = abs(value) / n
        for cand in (1, 10, 100, 1000, 10000, 100000, 1000000):
            err = abs(r - cand) / cand
            if err < 0.001 and (best is None or err < best[0]):
                best = (err, cand)
    return best[1] if best else None


def main() -> int:
    ap = argparse.ArgumentParser(description="派生模板的 10 个披露附注列")
    ap.add_argument("--book", default=None, help="目标工作簿（默认取 config）")
    ap.add_argument("--config", default=None, help="配置路径 (cohort.yaml)")
    ap.add_argument("--only", nargs="*", default=None, help="只处理指定代码")
    args = ap.parse_args()

    # If --book is specified and no --config, check if cohort.yaml exists in same folder
    config_path = args.config
    if not config_path and args.book:
        candidate = Path(args.book).resolve().with_name("cohort.yaml")
        if candidate.is_file():
            config_path = str(candidate)

    cfg = load_cfg(workbook_override=args.book, config_path=config_path)
    book = Path(cfg.get("_workbook_path") or cfg["workbook"])
    schema = json.loads((ROOT / "schema" / "fields.json").read_text(encoding="utf-8"))
    schema = {**schema, "fields": [f for f in schema["fields"] if f["key"] in SOURCE_FIELDS]}

    wb = openpyxl.load_workbook(book, data_only=False)
    ws = wb[cfg["sheet"]]
    mapping, missing = resolve_columns(ws, schema)
    if missing:
        print(f"错误: 字段未全部解析: {missing}")
        return 1

    # 表头 -> 列字母（派生列）
    header_to_letter: dict[str, str] = {}
    for i in range(1, ws.max_column + 1):
        h = ws.cell(1, i).value
        if h:
            header_to_letter[str(h).strip().lower()] = openpyxl.utils.get_column_letter(i)

    derived: dict[str, str] = {}
    for key, header in TARGETS.items():
        want = header.strip().lower()
        letter = header_to_letter.get(want)
        if not letter:  # 允许前缀匹配（模板里 BC 表头带长尾注释）
            hits = [v for h, v in header_to_letter.items() if h.startswith(want)]
            letter = hits[0] if len(hits) == 1 else None
        if not letter:
            print(f"错误: 找不到表头「{header}」对应的列")
            return 1
        derived[key] = letter

    # 行号（模板 B 列 = Stock Code；A 列是文件序号，不是代码）
    code_col = None
    for i in range(1, 6):
        if str(ws.cell(1, i).value or "").strip().lower().startswith("stock code"):
            code_col = i
            break
    if code_col is None:
        print("错误: 找不到 Stock Code 列")
        return 1
    row_of: dict[str, int] = {}
    for r in range(2, ws.max_row + 1):
        code = ws.cell(r, code_col).value
        if code:
            row_of[str(code).strip()] = r
    wb.close()

    ext_dir = Path(cfg["paths"]["out"]) / "extracted"
    only = {c.strip() for c in args.only} if args.only else None

    plans: list[tuple[str, int, dict[str, object], str]] = []
    skipped: list[str] = []
    for path in sorted(ext_dir.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        code = str(rec.get("code") or "").strip()
        if not code or code not in row_of:
            continue
        if only and code not in only:
            continue

        fields = rec.get("fields") or {}
        periods, basis = year1_periods(code, fields, Path(cfg["paths"]["text"]))
        if periods is None:
            skipped.append(f"{code}: {basis}")
            continue
        year1, year2, year3 = periods["year1"], periods["year2"], periods["year3"]
        factor = year1.months / 12

        def annualized(key: str):
            entry = fields.get(key) or {}
            v = entry.get("value")
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return None if math.isnan(v) or math.isinf(v) else v
            if isinstance(v, str):
                try:
                    f = float(v.replace(",", ""))
                except ValueError:
                    return None
                return None if math.isnan(f) or math.isinf(f) else f
            return None

        sales, pbt, prof = annualized("col_AH"), annualized("col_AK"), annualized("col_AN")

        values: dict[str, object] = {
            "BC": round(factor, 6),
            "CK": year2.start,
            "CL": year2.end,
            "CM": year1.start,
        }
        if year3 is not None:
            values["CI"], values["CJ"] = year3.start, year3.end
        if sales is not None:
            values["CN"] = round(sales * factor)
        if pbt is not None:
            values["CO"] = round(pbt * factor)
        if prof is not None:
            values["CP"] = round(prof * factor)

        # Sales and profit usually quote the Accountants' Report, whose unit is the one this
        # column records; match them at their original-period size, because for a 6M stub the
        # annualised figure divided by a comparative-period number can mimic a wrong unit
        # (2675.HK). Balance-sheet totals, which are never annualised, are the fallback.
        mult = ((infer_multiplier(rec, "col_AH", sales * factor) if sales else None)
                or (infer_multiplier(rec, "col_AN", prof * factor) if prof else None)
                or infer_multiplier(rec, "col_Y") or infer_multiplier(rec, "col_X")
                or infer_multiplier(rec, "col_W"))
        if mult:
            values["CG"] = mult

        plans.append((code, row_of[code], values, f"{year1.label}, {basis}"))

    if not plans:
        print("没有可派生的公司。")
        for s in skipped:
            print("  跳过:", s)
        return 1

    written = 0
    with workbook_transaction(book, operation="derive-disclosure-notes") as twb:
        tws = twb[cfg["sheet"]]
        for code, row, values, basis in plans:
            for key, val in values.items():
                tws[f"{derived[key]}{row}"].value = val
            written += 1
            print(f"  {code:9s} 行 {row:3d} 派生 {len(values):2d} 列（{basis}）")

    print(f"\n派生完成：{written} 家 -> {book}")
    for s in skipped:
        print("  跳过:", s)
    if skipped:
        print("  ⚠️ 跳过的公司其工作簿原有派生值未改动，须按上述原因修正抽取或人工核对。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
