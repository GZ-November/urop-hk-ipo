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

from contracts import is_company_level_statement


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
        if re.search(
            r"\b(Description of Shares|Shares to be issued|Unlisted Shares|"
            r"Class [AB] Ordinary|ISSUED SHARE CAPITAL|Issued Share Capital)\b",
            txt,
            re.I,
        ):
            score += 3
        if (
            re.search(r"\bTotal\s+[\d,]{6,}\b", txt)
            or re.search(r"\bTotal\b.{1,30}\b100(?:\.00)?%?\b", txt)
            or re.search(r"\b(?:Shares in total|Total issued Shares)\b[\s\S]{1,80}\b[\d,]{6,}\b", txt, re.I)
            or re.search(r"\b[\d,]{6,}\s+Total\b", txt, re.I)
        ):
            score += 4
        if score >= 6:
            candidate_pages.append((score, i))

    candidate_pages.sort(key=lambda x: (-x[0], x[1]))

    for _, page_idx in candidate_pages[:2]:
        page = doc[page_idx]
        lines = cluster_page_words_to_lines(page)
        table_rows = []
        in_table = False

        # 第 1 轮：标准行尾匹配（保持与历史单行股本表 100% 兼容）
        for lw in lines:
            line_str = " ".join(w[4] for w in lw).strip()
            line_str = re.sub(r"(?:\.\s*){2,}", " ", line_str).strip()
            if not in_table:
                if re.search(
                    r"\b(Description of Shares|Authorized share capital|Issued and to be issued|"
                    r"assuming the|immediately following|immediately after)\b",
                    line_str,
                    re.I,
                ):
                    in_table = True
                    continue
                if re.search(r"\b(Unlisted Shares|Class [AB] Ordinary|Ordinary Shares|Shares in issue)\b", line_str, re.I):
                    in_table = True

            if in_table:
                m = re.search(r"^(.*?)\s+([\d,]{6,})\s+(\d{1,3}(?:\.\d+)?%?)$", line_str)
                if m:
                    desc, shares, pct = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
                    if not re.match(r"^\([0-9ivx]+\)", desc, re.I):
                        table_rows.append([desc, shares, pct])
                        if desc.lower() == "total" or "total" in desc.lower():
                            break
                else:
                    m2 = re.search(r"^(.*?)\s+([\d,]{6,})(?:\s+Shares)?$", line_str, re.I)
                    if m2:
                        desc, num = m2.group(1).strip(), m2.group(2).strip()
                        if (
                            not desc.startswith(("RMB", "HK$", "US$"))
                            and not re.match(r"^\([0-9ivx]+\)", desc, re.I)
                        ):
                            table_rows.append([desc, num, "–"])
                            if desc.lower() == "total" or "total" in desc.lower():
                                break

        # 第 2 轮回退：若该页含名义价值列（US$/RMB）、股数在行首或描述跨多行，导致第 1 轮少于 2 行
        if len(table_rows) < 2:
            fallback_rows = []
            in_issued = False
            pending: list[str] = []
            for lw in lines:
                s_clean = re.sub(r"(?:\.\s*){2,}", " ", " ".join(w[4] for w in lw)).strip()
                if re.search(r"^(?:ASSUMPTIONS|RANKING|WVR STRUCTURE|OUR SHARES|GENERAL MANDATE|Notes?:)", s_clean, re.I):
                    if fallback_rows:
                        break
                    in_issued = False
                    pending = []
                    continue
                if re.search(r"(?:Authori[sz]ed [Ss]hare [Cc]apital|Before the Share Consolidation)", s_clean):
                    in_issued = False
                    pending = []
                    continue
                if re.search(
                    r"(?:Issued and to be issued|ISSUED SHARE CAPITAL|Issued Share Capital|"
                    r"immediately (?:following|after) (?:the )?completion|"
                    r"Assuming the Over-allotment Option is not exercised)",
                    s_clean,
                    re.I,
                ):
                    in_issued = True
                    pending = []
                    continue
                if re.search(r"^(?:Description of Shares|Number\s+Description|Aggregate nominal)", s_clean, re.I):
                    in_issued = True
                    pending = []
                    continue
                if not in_issued:
                    continue

                tokens = s_clean.split()
                share_num = None
                pct_val = "–"
                desc_tokens = []
                for tk in tokens:
                    tk_clean = tk.strip("(),;")
                    if (
                        share_num is None
                        and re.fullmatch(r"\d{1,3}(?:,\d{3})+", tk_clean)
                        and len(tk_clean) >= 6
                    ):
                        share_num = tk_clean
                    elif re.fullmatch(r"\d{1,3}(?:\.\d+)?%", tk_clean):
                        pct_val = tk_clean
                    elif re.match(r"^(?:US\$|RMB|HK\$|USD|HKD)\d", tk_clean, re.I):
                        continue
                    else:
                        desc_tokens.append(tk)
                desc_line = " ".join(desc_tokens).strip()
                if share_num:
                    full_desc = " ".join(pending + ([desc_line] if desc_line else [])).strip()
                    pending = []
                    if re.match(r"^\([0-9ivx]+\)", full_desc, re.I):
                        continue
                    fallback_rows.append([full_desc or "Shares", share_num, pct_val])
                    if re.search(r"\btotal\b", full_desc, re.I):
                        break
                elif desc_line and len(desc_line) < 75 and not re.match(r"^\([0-9ivx]+\)", desc_line, re.I):
                    pending.append(desc_line)
                    if len(pending) > 2:
                        pending = pending[-2:]
            if len(fallback_rows) >= 2:
                table_rows = fallback_rows

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
            # 捕获类似 "Underwriting commission: 2.5%" 或 "Listing expenses ... HK$ 45.2 million"，
            # 要求右侧值必须至少包含一个数字（防止匹配到散文词尾如 "s," 或 "fees,"）
            m = re.search(
                r"^(.*?commission.*?|.*?incentive fee.*?|.*?listing expenses.*?)\s*[:—–\-]?\s*"
                r"(\d+(?:\.\d+)?\s*%|(?:HK\$|RMB|US\$|USD|HKD)\s*[\d,]+(?:\.\d+)?\s*(?:million|thousand|’000|'000)?)",
                line_str,
                re.I,
            )
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
YEAR_TOKEN_RE = re.compile(r"^(?:FY|\d{1,2}M(?:FY)?)?(199\d|20\d\d)$", re.I)
UNIT_TOKEN_RE = re.compile(r"^(?:RMB|HK\$|US\$|USD|HKD|EUR|JPY|SGD)(?:[’']?000)?$", re.I)
PCT_TOKEN_RE = re.compile(r"^%$")
NUM_CELL_RE = re.compile(r"^(?:\(?[\d,]+(?:\.\d+)?%?\)?|[-–—]|nil)$", re.I)

METRIC_PATTERNS = re.compile(
    r"^(Revenue|Total\s+revenue|Net\s+revenues?|Turnover|"
    r"Gross\s+profit(?:\s*/\s*\(loss\))?|"
    r"(?:Operating\s+)?(?:profit|loss)(?:\s*/\s*\((?:loss|profit)\))?\s+before\s+(?:income\s+)?tax(?:ation)?|"
    r"(?:Net\s+)?(?:profit|loss)\s+before\s+(?:income\s+)?tax(?:ation)?(?:\s+and\s+.*)?|"
    r"(?:Profit|Loss)(?:\s*/\s*\((?:loss|profit)\))?\s+(?:and\s+total\s+comprehensive\s+(?:income|loss)\s+)?for\s+the\s+(?:year|period)(?:/period)?s?|"
    r"Net\s+(?:profit|loss)(?:\s+for\s+the\s+(?:year|period)s?)?|"
    r"Total\s+assets|Total\s+current\s+assets|Total\s+non-current\s+assets|"
    r"Total\s+liabilities|Total\s+current\s+liabilities|Total\s+non-current\s+liabilities|"
    r"Total\s+equity(?:\s*/\s*\(deficit\))?|Total\s+deficits?|"
    r"Net\s+assets(?:\s*/\s*\((?:liabilities|deficits?)\))?|Net\s+current\s+assets(?:\s*/\s*\(liabilities\))?|"
    r"Cash\s+and\s+cash\s+equivalents(?:\s+at\s+end\s+of\s+(?:year|period)s?)?|"
    r"Net\s+cash\s+(?:generated\s+from|from|used\s+in)\s+operating\s+activities|"
    r"Research\s+and\s+development\s+(?:expenses|costs))\b",
    re.I,
)


def _is_year_header_line(lw: list[tuple]) -> list[tuple]:
    """检测是否为纯年份表头行（左侧无散文叙述，右侧含 >=2 个年份词）。"""
    left_words = [
        w[4] for w in lw
        if w[0] < 140 and not re.match(r"^(?:Notes?|Item)$", w[4], re.I)
    ]
    if left_words:
        return []
    right_words = [w for w in lw if w[0] >= 140]
    year_words = [w for w in right_words if YEAR_TOKEN_RE.match(w[4].strip("(),*"))]
    if len(year_words) >= 2 and len(year_words) >= len(right_words) - 1:
        return year_words
    return []


def _build_subtable_columns(
    lines: list[list[tuple]],
    year_line_idx: int,
    year_words: list[tuple],
) -> tuple[list[dict[str, Any]], list[float]]:
    """根据年份行的 X 轴坐标及上下相邻行重构真实表头（含完整年/Stub期间、未审计标记、币种单位）。"""
    year_groups = []
    for w in year_words:
        year_groups.append({
            "year": w[4].strip("(),*"),
            "xc": (w[0] + w[2]) / 2.0,
            "x0": w[0],
            "x1": w[2],
            "prefix": [],
            "audit": [],
        })

    # 向上检查 1-2 行：提取期间前缀（如 Year ended Dec 31 vs Four months ended Apr 30）
    for hl in lines[max(0, year_line_idx - 2):year_line_idx]:
        if any(w[0] < 140 for w in hl):
            continue
        hw = [w for w in hl if w[0] >= 140]
        if not hw:
            continue
        segs = [[hw[0]]]
        for w in hw[1:]:
            if w[0] - segs[-1][-1][2] > 18:
                segs.append([w])
            else:
                segs[-1].append(w)

        if len(segs) == 1:
            seg = segs[0]
            seg_text = " ".join(w[4] for w in seg)
            seg_x0 = seg[0][0]
            if seg_x0 > year_groups[0]["xc"] + 45:
                for g in year_groups:
                    if g["xc"] >= seg_x0 - 35:
                        g["prefix"].append(seg_text)
            else:
                for g in year_groups:
                    g["prefix"].append(seg_text)
        elif len(segs) >= 2:
            right_seg = segs[-1]
            right_text = " ".join(w[4] for w in right_seg)
            right_x0 = right_seg[0][0]
            right_groups = [g for g in year_groups if g["xc"] >= right_x0 - 40]
            if not right_groups:
                right_groups = [year_groups[-1]]
            # 若存在对比期（如 2022, 2023, 2024, 2024, 2025），最后两列属于右侧 Stub 期间
            if len(year_groups) >= 4 and year_groups[-2]["year"] == year_groups[-3]["year"]:
                right_groups = year_groups[-2:]
            elif len(year_groups) >= 4 and any(
                p in right_text.lower() or any(p in x.lower() for x in year_groups[-1]["prefix"])
                for p in ("as of", "as at")
            ):
                right_groups = [year_groups[-1]]
            for g in right_groups:
                g["prefix"].append(right_text)
            left_text = " ".join(w[4] for w in segs[0])
            for g in year_groups:
                if g not in right_groups:
                    g["prefix"].append(left_text)

    # 向下检查 1-3 行：提取 (unaudited)、全局量级单位与分列币种/百分比列坐标
    shared_scale = ""
    per_col_units: list[tuple] = []
    pct_xs: list[float] = []

    for hl in lines[year_line_idx + 1:min(len(lines), year_line_idx + 4)]:
        if any(w[0] < 140 for w in hl):
            break
        line_str = " ".join(w[4] for w in hl).strip()
        if re.search(r"unaudited", line_str, re.I):
            for w in hl:
                if "unaudited" in w[4].lower():
                    w_xc = (w[0] + w[2]) / 2.0
                    best = min(year_groups, key=lambda g: abs(g["xc"] - w_xc))
                    if abs(best["xc"] - w_xc) < 45 and "unaudited" not in best["audit"]:
                        best["audit"].append("unaudited")
        elif (
            re.search(r"\b(in\s+thousands|in\s+millions|million|thousand)\b", line_str, re.I)
            and not UNIT_TOKEN_RE.match(hl[0][4].strip("()"))
        ):
            m_sc = re.search(
                r"\(?((?:RMB|HK\$|US\$|USD|HKD)?\s*(?:in\s+)?(?:millions?|thousands?|’000|'000))",
                line_str,
                re.I,
            )
            if m_sc:
                shared_scale = m_sc.group(1).strip()
        else:
            u_tokens = [w for w in hl if w[0] >= 140 and UNIT_TOKEN_RE.match(w[4].strip("()"))]
            p_tokens = [w for w in hl if w[0] >= 140 and PCT_TOKEN_RE.match(w[4].strip())]
            for pw in p_tokens:
                px = (pw[0] + pw[2]) / 2.0
                if all(abs(px - existing) > 5 for existing in pct_xs):
                    pct_xs.append(px)
            if len(u_tokens) >= len(year_groups):
                per_col_units = u_tokens

    value_cols: list[dict[str, Any]] = []
    if per_col_units:
        for uw in per_col_units:
            u_xc = (uw[0] + uw[2]) / 2.0
            u_text = uw[4].strip("()")
            yg = min(year_groups, key=lambda g: abs(g["xc"] - u_xc))
            p = " ".join(yg["prefix"]).strip(" ,")
            p = re.sub(r"\bFor the\s+", "", p, flags=re.I)
            label = f"{p} {yg['year']}".strip() if p else yg["year"]
            if yg["audit"]:
                label += " (unaudited)"
            unit_label = (
                f"{u_text} {shared_scale}".strip()
                if shared_scale and shared_scale.lower() not in u_text.lower()
                else u_text
            )
            label += f" [{unit_label}]"
            value_cols.append({"xc": u_xc, "header": label})
    else:
        for yg in year_groups:
            p = " ".join(yg["prefix"]).strip(" ,")
            p = re.sub(r"\bFor the\s+", "", p, flags=re.I)
            label = f"{p} {yg['year']}".strip() if p else yg["year"]
            if yg["audit"]:
                label += " (unaudited)"
            if shared_scale:
                label += f" [{shared_scale}]"
            value_cols.append({"xc": yg["xc"], "header": label})

    return value_cols, pct_xs


def _extract_rows_for_subtable(
    lines: list[list[tuple]],
    start_idx: int,
    end_idx: int,
    value_cols: list[dict[str, Any]],
    pct_xs: list[float],
) -> list[list[str]]:
    """按数值列的真实 X 坐标聚类对齐每一行，过滤百分比附列与附注行号，不截断任何期间列。"""
    rows: list[list[str]] = []
    pending_desc: list[str] = []
    min_val_x = min(c["xc"] for c in value_cols) - 45

    for idx in range(start_idx, end_idx):
        lw = lines[idx]
        left_w = [w for w in lw if w[0] < min_val_x and not re.match(r"^\.+$", w[4])]
        right_w = [w for w in lw if w[0] >= min_val_x and NUM_CELL_RE.match(w[4].strip())]

        left_str = " ".join(w[4] for w in left_w).strip(" .")
        # 剔除行末附注标记如 "(1)" 或会计师报告 Note 编号如 "23"
        left_str = re.sub(r"(?:\s*\(\d+\)|\s+\d{1,2})\s*$", "", left_str).strip(" .")

        if left_str and not right_w:
            if (
                len(left_str) < 48
                and not left_str.endswith(".")
                and not re.search(r"\b(we|our|increased|decreased|table|following)\b", left_str, re.I)
            ):
                pending_desc.append(left_str)
                if len(pending_desc) > 2:
                    pending_desc = pending_desc[-2:]
            else:
                pending_desc = []
            continue

        if right_w:
            full_desc = " ".join(pending_desc + ([left_str] if left_str else [])).strip(" .")
            pending_desc = []
            if not full_desc or not METRIC_PATTERNS.search(full_desc):
                continue

            row_vals = ["–"] * len(value_cols)
            for nw in right_w:
                n_xc = (nw[0] + nw[2]) / 2.0
                best_col_i = min(range(len(value_cols)), key=lambda ci: abs(value_cols[ci]["xc"] - n_xc))
                dist_col = abs(value_cols[best_col_i]["xc"] - n_xc)
                dist_pct = min((abs(px - n_xc) for px in pct_xs), default=999.0)
                if dist_pct < dist_col and dist_pct < 20:
                    continue
                if dist_col < 38:
                    row_vals[best_col_i] = nw[4].strip()

            if sum(1 for v in row_vals if v != "–") >= 2:
                rows.append([full_desc] + row_vals)

    return rows


def extract_financial_summary_tables(doc: fitz.Document) -> list[ParsedTable]:
    results: list[ParsedTable] = []
    candidate_pages = []

    FIN_KEYWORDS = [
        "CONSOLIDATED STATEMENTS OF FINANCIAL POSITION",
        "CONSOLIDATED STATEMENTS OF PROFIT OR LOSS",
        "SUMMARY OF HISTORICAL FINANCIAL INFORMATION",
        "SUMMARY CONSOLIDATED STATEMENTS",
        "COMBINED STATEMENTS OF",
        "CONSOLIDATED PROFIT AND LOSS",
        "COMBINED PROFIT AND LOSS",
        "CONSOLIDATED INCOME STATEMENT",
        "COMBINED INCOME STATEMENT",
        "CONSOLIDATED BALANCE SHEET",
        "COMBINED BALANCE SHEET",
        "SUMMARY OF COMBINED",
    ]

    for i in range(min(500, doc.page_count)):
        txt = doc[i].get_text()
        if is_company_level_statement(txt):
            continue
        if any(k in txt.upper() for k in FIN_KEYWORDS):
            if any(
                m in txt
                for m in (
                    "Revenue",
                    "Net revenues",
                    "Turnover",
                    "Total assets",
                    "Total equity",
                    "Net assets",
                )
            ):
                candidate_pages.append(i)

    for page_idx in candidate_pages[:4]:
        page = doc[page_idx]
        lines = cluster_page_words_to_lines(page)
        year_idxs = [i for i, lw in enumerate(lines) if _is_year_header_line(lw)]

        if year_idxs:
            for k, y_idx in enumerate(year_idxs):
                next_y_idx = year_idxs[k + 1] - 2 if k + 1 < len(year_idxs) else len(lines)
                yw = _is_year_header_line(lines[y_idx])
                vcols, pct_xs = _build_subtable_columns(lines, y_idx, yw)
                table_rows = _extract_rows_for_subtable(lines, y_idx + 1, next_y_idx, vcols, pct_xs)
                if table_rows:
                    headers = ["Financial Metric"] + [c["header"] for c in vcols]
                    md = format_markdown_table(headers, table_rows)
                    results.append(ParsedTable(
                        name="financials",
                        page=page_idx + 1,
                        title="合并财务报表核心指标表 (Consolidated Financial Summary Table)",
                        headers=headers,
                        rows=table_rows,
                        markdown=md,
                        metadata={
                            "metrics_count": len(table_rows),
                            "columns_count": len(vcols),
                        },
                    ))
            continue

        # 兜底分支：若页面未检出标准年份行，保留全部数字列而不截断为 4 列
        table_rows = []
        for lw in lines:
            line_str = " ".join(w[4] for w in lw).strip()
            m = re.search(
                r"^(Revenue|Net revenues?|Gross profit|Profit for the (?:year|period)|"
                r"Total assets|Total equity|Total liabilities|"
                r"Net cash (?:generated from|from|used in) operating activities)\s+([\d,\.\(\)\s\-–—]+)$",
                line_str,
                re.I,
            )
            if m:
                item_name = m.group(1).strip()
                nums = re.findall(r"[\d,\.]+|(?:\([\d,\.]+\))|[-–—]", m.group(2))
                if len(nums) >= 2:
                    table_rows.append([item_name] + nums)

        if table_rows:
            max_num_cols = max(len(r) - 1 for r in table_rows)
            headers = ["Financial Metric"] + [f"Period {c + 1}" for c in range(max_num_cols)]
            md = format_markdown_table(headers, table_rows)
            results.append(ParsedTable(
                name="financials",
                page=page_idx + 1,
                title="合并财务报表核心指标表 (Consolidated Financial Summary Table)",
                headers=headers,
                rows=table_rows,
                markdown=md,
                metadata={"metrics_count": len(table_rows), "columns_count": max_num_cols},
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
