"""原生结构化表格解析引擎 (Table Parser Engine)。

利用 PyMuPDF / 空间几何拓扑算法，对招股书开放式无框表格（Borderless Tables）
进行行向 Y 轴聚类与列向 X 轴空间投影视网膜对齐，输出干净的 Markdown 表格与结构化 JSON。

支持 4 大核心表格抽取：
1. 股本结构表 (Share Capital Table)
2. 基石配售表 (Cornerstone Investors Table)
3. 承销佣金与上市费用表 (Underwriting & Expenses Table)
4. 合并财务三大表摘要 (Financial Summary Tables)
"""
from __future__ import annotations

import itertools
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF


@dataclass
class ParsedTable:
    name: str
    page: int
    title: str
    headers: list[str]
    rows: list[list[str]]
    markdown: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def format_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    """生成标准 Markdown 表格字符串。"""
    if not headers and not rows:
        return ""
    if not headers and rows:
        headers = [f"Col {i+1}" for i in range(len(rows[0]))]

    # 清洗换行与管道符
    clean_headers = [re.sub(r"\s+", " ", h).replace("|", "&#124;").strip() for h in headers]
    clean_rows = [
        [re.sub(r"\s+", " ", str(c)).replace("|", "&#124;").strip() for c in row]
        for row in rows
    ]

    # 补齐列数
    max_cols = max(len(clean_headers), max((len(r) for r in clean_rows), default=0))
    while len(clean_headers) < max_cols:
        clean_headers.append(f"Col {len(clean_headers)+1}")
    padded_rows = []
    for r in clean_rows:
        pr = list(r)
        while len(pr) < max_cols:
            pr.append("")
        padded_rows.append(pr[:max_cols])

    col_widths = [len(clean_headers[i]) for i in range(max_cols)]
    for r in padded_rows:
        for i, c in enumerate(r):
            col_widths[i] = max(col_widths[i], len(c))
    col_widths = [max(w, 3) for w in col_widths]

    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(clean_headers)) + " |"
    sep_line = "| " + " | ".join("-" * col_widths[i] for i in range(max_cols)) + " |"
    body_lines = [
        "| " + " | ".join(r[i].ljust(col_widths[i]) for i in range(max_cols)) + " |"
        for r in padded_rows
    ]
    return "\n".join([header_line, sep_line] + body_lines)


def cluster_page_words_to_lines(page: fitz.Page, y_tol: float = 3.5) -> list[list[tuple]]:
    """按 Y 轴空间公差将 words 聚类为逻辑行。
    word 元组格式: (x0, y0, x1, y1, word_text, block_no, line_no, word_no)
    """
    words = page.get_text("words")
    if not words:
        return []
    sorted_words = sorted(words, key=lambda w: (round(w[1] / y_tol) * y_tol, w[0]))
    lines = []
    for _, g in itertools.groupby(sorted_words, key=lambda w: round(w[1] / y_tol) * y_tol):
        lines.append(list(g))
    return lines


# ----------------------------------------------------------------
# 1. 股本结构表 (Share Capital Table)
# ----------------------------------------------------------------
def extract_share_capital_table(doc: fitz.Document) -> list[ParsedTable]:
    results: list[ParsedTable] = []
    candidate_pages = []

    for i in range(doc.page_count):
        txt = doc[i].get_text()
        score = 0
        if "SHARE CAPITAL" in txt.upper():
            score += 3
        if re.search(r"\b(Description of Shares|Shares to be issued|Unlisted Shares|Class [AB] Ordinary)\b", txt, re.I):
            score += 3
        if re.search(r"\bTotal\s+[\d,]{6,}\b", txt) or re.search(r"\bTotal\b.{1,20}\b100(?:\.00)?%?\b", txt):
            score += 4
        if score >= 6:
            candidate_pages.append((score, i))

    candidate_pages.sort(key=lambda x: x[0], reverse=True)

    for _, page_idx in candidate_pages[:2]:
        page = doc[page_idx]
        lines = cluster_page_words_to_lines(page)
        table_rows = []
        in_table = False

        for lw in lines:
            line_str = " ".join(w[4] for w in lw).strip()
            if not in_table:
                if re.search(r"\b(Description of Shares|Authorized share capital|Issued and to be issued|assuming the|immediately following)\b", line_str, re.I):
                    in_table = True
                    continue
                if re.search(r"\b(Unlisted Shares|Class [AB] Ordinary|Ordinary Shares|Shares in issue)\b", line_str, re.I):
                    in_table = True

            if in_table:
                # 尝试解析多列: Description + Shares + Percentage / Value
                m = re.search(r"^(.*?)\s+([\d,]{6,})\s+(\d{1,3}(?:\.\d+)?%?)$", line_str)
                if m:
                    desc, shares, pct = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
                    table_rows.append([desc, shares, pct])
                    if desc.lower() == "total" or "total" in desc.lower():
                        break
                else:
                    # 两列情况: Description + Number
                    m2 = re.search(r"^(.*?)\s+([\d,]{6,})$", line_str)
                    if m2:
                        desc, num = m2.group(1).strip(), m2.group(2).strip()
                        if not desc.startswith("RMB") and not desc.startswith("HK$") and not desc.startswith("US$"):
                            table_rows.append([desc, num, "–"])
                            if desc.lower() == "total" or "total" in desc.lower():
                                break

        if table_rows:
            headers = ["Description of Shares", "Number of Shares", "Approximate Percentage (%)"]
            md = format_markdown_table(headers, table_rows)
            results.append(ParsedTable(
                name="share_capital",
                page=page_idx + 1,
                title="股份结构与发售比例表 (Share Capital Table)",
                headers=headers,
                rows=table_rows,
                markdown=md,
                metadata={"total_rows": len(table_rows)},
            ))

    return results


# ----------------------------------------------------------------
# 2. 基石投资者名单表 (Cornerstone Investors Table)
# ----------------------------------------------------------------
def extract_cornerstone_table(doc: fitz.Document) -> list[ParsedTable]:
    results: list[ParsedTable] = []
    candidate_pages = []

    for i in range(doc.page_count):
        txt = doc[i].get_text()
        if "CORNERSTONE INVESTOR" in txt.upper() or "CORNERSTONE PLACING" in txt.upper():
            if re.search(r"\bTotal\b", txt) and re.search(r"\b\d{1,3}(?:,\d{3}){2,}\b", txt):
                candidate_pages.append(i)

    for page_idx in candidate_pages[:3]:
        page = doc[page_idx]
        lines = cluster_page_words_to_lines(page)
        table_rows = []

        for lw in lines:
            line_str = " ".join(w[4] for w in lw).strip()
            # 匹配基石行格式: 机构名 + 金额 + 股数 + 比例...
            # 例: Fullgoal Fund 8.0 3,662,600 1.48% 0.16% ...
            m = re.search(r"^([A-Za-z0-9\u4e00-\u9fff\s\(\)\.,&'-]+?)\s+([\d\.]+)\s+([\d,]{5,})\s+(\d{1,2}\.\d{1,2}%?)(.*)$", line_str)
            if m:
                inv = m.group(1).strip()
                amt = m.group(2).strip()
                shares = m.group(3).strip()
                pct = m.group(4).strip()
                if not inv.upper().startswith("NOTE") and not inv.upper().startswith("ASSUMING"):
                    table_rows.append([inv, amt, shares, pct])
            elif re.search(r"^Total\s+([\d\.]+)\s+([\d,]{5,})\s+(\d{1,2}\.\d{1,2}%?)", line_str, re.I):
                tm = re.search(r"^Total\s+([\d\.]+)\s+([\d,]{5,})\s+(\d{1,2}\.\d{1,2}%?)", line_str, re.I)
                table_rows.append(["Total", tm.group(1), tm.group(2), tm.group(3)])

        if table_rows:
            headers = ["Cornerstone Investor", "Investment Amount (M)", "Number of Offer Shares", "Approximate % of Offer Shares"]
            md = format_markdown_table(headers, table_rows)
            results.append(ParsedTable(
                name="cornerstone",
                page=page_idx + 1,
                title="基石投资者配售名单与认购规模表 (Cornerstone Investors Table)",
                headers=headers,
                rows=table_rows,
                markdown=md,
                metadata={"investor_count": len([r for r in table_rows if r[0].lower() != "total"])},
            ))

    return results


# ----------------------------------------------------------------
# 3. 承销佣金与上市费用表 (Underwriting Table)
# ----------------------------------------------------------------
def extract_underwriting_table(doc: fitz.Document) -> list[ParsedTable]:
    results: list[ParsedTable] = []
    candidate_pages = []

    for i in range(doc.page_count):
        txt = doc[i].get_text()
        if "UNDERWRITING COMMISSION" in txt.upper() or "LISTING EXPENSES" in txt.upper():
            if re.search(r"\b(commission|incentive fee|HK\$|RMB)\b", txt, re.I):
                candidate_pages.append(i)

    for page_idx in candidate_pages[:2]:
        page = doc[page_idx]
        lines = cluster_page_words_to_lines(page)
        table_rows = []

        for lw in lines:
            line_str = " ".join(w[4] for w in lw).strip()
            # 捕获类似 "Underwriting commission: 2.5%" 或 "Listing expenses ... HK$ 45.2 million"
            m = re.search(r"^(.*?commission.*?|.*?incentive fee.*?|.*?listing expenses.*?)\s*[:—–\-]?\s*([0-9\.]+\s*%|[A-Za-z\$]+\s*[\d,\.]+\s*(?:million|thousand)?)", line_str, re.I)
            if m:
                table_rows.append([m.group(1).strip(), m.group(2).strip()])

        if table_rows:
            headers = ["Item Description", "Rate / Amount Disclosed"]
            md = format_markdown_table(headers, table_rows)
            results.append(ParsedTable(
                name="underwriting",
                page=page_idx + 1,
                title="承销佣金率与上市费用构成表 (Underwriting & Expenses Table)",
                headers=headers,
                rows=table_rows,
                markdown=md,
                metadata={"items_count": len(table_rows)},
            ))

    return results


# ----------------------------------------------------------------
# 4. 合并财务三大表摘要 (Financial Summary Tables)
# ----------------------------------------------------------------
def extract_financial_summary_tables(doc: fitz.Document) -> list[ParsedTable]:
    results: list[ParsedTable] = []
    candidate_pages = []

    FIN_KEYWORDS = [
        "CONSOLIDATED STATEMENTS OF FINANCIAL POSITION",
        "CONSOLIDATED STATEMENTS OF PROFIT OR LOSS",
        "SUMMARY OF HISTORICAL FINANCIAL INFORMATION",
    ]

    for i in range(min(500, doc.page_count)):
        txt = doc[i].get_text()
        if any(k in txt.upper() for k in FIN_KEYWORDS):
            if "Revenue" in txt or "Total assets" in txt or "Total equity" in txt:
                candidate_pages.append(i)

    for page_idx in candidate_pages[:3]:
        page = doc[page_idx]
        lines = cluster_page_words_to_lines(page)
        table_rows = []

        for lw in lines:
            line_str = " ".join(w[4] for w in lw).strip()
            # 捕获财务核心行：名称 + 3~4个数字列
            m = re.search(r"^(Revenue|Gross profit|Profit for the (?:year|period)|Total assets|Total equity|Total liabilities|Net cash (?:used in|from) operating activities)\s+([\d,\.\(\)\s\-–—]+)$", line_str, re.I)
            if m:
                item_name = m.group(1).strip()
                nums = re.findall(r"[\d,\.]+|(?:\([\d,\.]+\))|[-–—]", m.group(2))
                if len(nums) >= 2:
                    table_rows.append([item_name] + nums[:4])

        if table_rows:
            headers = ["Financial Metric", "Year-3", "Year-2", "Year-1"]
            md = format_markdown_table(headers, table_rows)
            results.append(ParsedTable(
                name="financials",
                page=page_idx + 1,
                title="合并财务报表核心指标表 (Consolidated Financial Summary Table)",
                headers=headers,
                rows=table_rows,
                markdown=md,
                metadata={"metrics_count": len(table_rows)},
            ))

    return results


def extract_all_tables_for_pdf(pdf_path: Path, output_dir: Path | None = None) -> dict[str, list[dict[str, Any]]]:
    """对单份 PDF 执行全局结构化表格抽取与持久化。"""
    if not pdf_path.exists():
        return {}

    doc = fitz.open(pdf_path)
    extracted: dict[str, list[ParsedTable]] = {
        "share_capital": extract_share_capital_table(doc),
        "cornerstone": extract_cornerstone_table(doc),
        "underwriting": extract_underwriting_table(doc),
        "financials": extract_financial_summary_tables(doc),
    }
    doc.close()

    payload = {}
    for name, tables in extracted.items():
        payload[name] = [t.to_dict() for t in tables]

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        # 写 JSON
        json_file = output_dir / "tables.json"
        json_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        # 写按表格划分的 Markdown
        for name, tables in extracted.items():
            if tables:
                md_file = output_dir / f"{name}.md"
                content = []
                for t in tables:
                    content.append(f"## {t.title} (Page {t.page})\n\n{t.markdown}\n")
                md_file.write_text("\n".join(content), encoding="utf-8")

    return payload
