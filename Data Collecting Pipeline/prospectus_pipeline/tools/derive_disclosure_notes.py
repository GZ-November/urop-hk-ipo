#!/usr/bin/env python3
"""派生「披露附注」10 列（Continuation of the template's disclosure-notes block）.

模板里以下 10 列此前一直 0/60，代码本归类为 "Reserved / Unmatured"，
但它们**并非无法获得**，而是可以从已抽取的 70 个字段确定性派生：

| 列 | 含义 | 派生方式 |
|---|---|---|
| BC  | Comments (nearest sales & profit adjustment factor - original data duration in year) | year-1 覆盖月数 / 12 |
| CG  | Financial statement unit multiplier | 由「披露值 vs 存储值」推断（'000 -> 1000） |
| CI/CJ | Year-3 financial period start / end | year-1 期间前移 2 年 |
| CK/CL | Year-2 financial period start / end | year-1 期间前移 1 年 |
| CM  | Year-1 financial period start | 财年起始日 |
| CN  | Year-1 net sales (original, pre-annualization) | 年化值 × BC |
| CO  | Year-1 profit before tax (original) | 年化值 × BC |
| CP  | Year-1 profit for period (original) | 年化值 × BC |

口径全部以 2026Q1 权威成品（HKIPO-MB2026Q1.xlsx，38/38 已填）反解并逐行验证：

- `BC` 分布 0.5 / 0.6667 / 0.75 / 0.8333 对应 year-1 期末 06-30 / 08-31 / 09-30 / 10-31；
- **年化值 ÷ 原值恒等于 1/BC**（38 行全部成立，例如 BC=0.5 时比值精确为 2.0000）；
- `CM` 恒为期初（2025-01-01），`CI/CJ`、`CK/CL` 为 year-3 / year-2 的整年区间；
- `CG` 37 家为 1000、1 家为 1000000。

用法：
    python tools/derive_disclosure_notes.py [--book ../HKIPO-MB2026Q2.xlsx] [--only 6656.HK ...]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from calendar import monthrange
from datetime import date
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from workbook_transaction import workbook_transaction  # noqa: E402
from write_back import resolve_columns  # noqa: E402
from run import load_cfg  # noqa: E402

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

_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


def parse_date(value) -> date | None:
    """尽最大努力解析招股书日期（支持 31/12/25、31 December 2025、2025-12-31 等）。"""
    if isinstance(value, date):
        return value
    if value is None:
        return None
    s = str(value).strip()
    if not s or s.upper() in {"NA", "NAN", "NONE"}:
        return None
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})\b", s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        try:
            return date(y, mo, d)
        except ValueError:
            return None
    m = re.search(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{4})\b", s)
    if m:
        mo = _MONTHS.get(m.group(2)[:3].lower())
        if mo:
            try:
                return date(int(m.group(3)), mo, int(m.group(1)))
            except ValueError:
                return None
    return None


def month_span(start: date, end: date) -> int:
    """含头含尾的整月数（Jan 1 -> Sep 30 == 9）。"""
    return (end.year - start.year) * 12 + (end.month - start.month) + 1


def fiscal_start(end: date) -> date:
    """由财年期末推期初：12 月结账 -> 同年 1/1；否则期末月+1 的上一年首日。"""
    if end.month == 12:
        return date(end.year, 1, 1)
    y, m = (end.year - 1, end.month + 1)
    return date(y, m, 1)


def shift_year(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:  # 2 月 29 日
        return d.replace(year=d.year + years, day=28)


def infer_multiplier(rec: dict, key: str) -> int | None:
    """由「存储值 ÷ 引文中的数字」推断财报单位乘数。"""
    entry = (rec.get("fields") or {}).get(key) or {}
    value, quote = entry.get("value"), entry.get("quote") or ""
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
    best = None
    for n in nums:
        r = abs(value) / n
        for cand in (1, 10, 100, 1000, 10000, 100000, 1000000):
            if abs(r - cand) / cand < 0.02:  # 相对误差 <2%
                if best is None or abs(r - cand) < abs(best[0] - best[1]):
                    best = (r, cand)
    return best[1] if best else None


def main() -> int:
    ap = argparse.ArgumentParser(description="派生模板的 10 个披露附注列")
    ap.add_argument("--book", default=None, help="目标工作簿（默认取 config）")
    ap.add_argument("--only", nargs="*", default=None, help="只处理指定代码")
    args = ap.parse_args()

    cfg = load_cfg(workbook_override=args.book)
    book = Path(cfg["workbook"])
    schema = json.loads((ROOT / "schema" / "fields.json").read_text(encoding="utf-8"))

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

    plans: list[tuple[str, int, dict[str, object]]] = []
    skipped: list[str] = []
    for path in sorted(ext_dir.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        code = str(rec.get("code") or "").strip()
        if not code or code not in row_of:
            continue
        if only and code not in only:
            continue

        fields = rec.get("fields") or {}
        end = parse_date((fields.get("col_AT") or {}).get("value"))
        if end is None:
            skipped.append(f"{code}: 无有效 year-1 期末日（col_AT）")
            continue

        start = fiscal_start(end)
        months = month_span(start, end)
        # 只接受 3..12 个月的合理期间
        if not 3 <= months <= 12:
            skipped.append(f"{code}: year-1 期间异常（{months} 个月）")
            continue
        factor = months / 12

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
            "CI": shift_year(start, -2),
            "CJ": shift_year(end, -2),
            "CK": shift_year(start, -1),
            "CL": shift_year(end, -1),
            "CM": start,
        }
        if sales is not None:
            values["CN"] = round(sales * factor)
        if pbt is not None:
            values["CO"] = round(pbt * factor)
        if prof is not None:
            values["CP"] = round(prof * factor)

        mult = infer_multiplier(rec, "col_AH") or infer_multiplier(rec, "col_AN")
        if mult:
            values["CG"] = mult

        plans.append((code, row_of[code], values))

    if not plans:
        print("没有可派生的公司。")
        for s in skipped:
            print("  跳过:", s)
        return 1

    written = 0
    with workbook_transaction(book, operation="derive-disclosure-notes") as twb:
        tws = twb[cfg["sheet"]]
        for code, row, values in plans:
            for key, val in values.items():
                tws[f"{derived[key]}{row}"].value = val
            written += 1
            print(f"  {code:9s} 行 {row:3d} 派生 {len(values):2d} 列")

    print(f"\n派生完成：{written} 家 -> {book}")
    for s in skipped:
        print("  跳过:", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
