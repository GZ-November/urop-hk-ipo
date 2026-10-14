#!/usr/bin/env python3
"""给抽取代理用的招股书全文检索工具。

招股书披露位置并不模板化：同一个字段在不同公司可能出现在 MD&A、附注、业务章节或
重大合同章节。因此 packet 只是起点，代理需要用本工具在**页级全文**里自己检索。

用法（CODE 形如 6082.HK 或 HKIPO-MB6082）：
  outline  CODE                     列出每页页首标题，快速定位章节
  search   CODE PATTERN [--context N] [--max M] [--ignore-case]
                                    正则检索，返回命中页 + 上下文行
  pages    CODE RANGE               按页导出原文，RANGE 如 413-415 或 413,420,488
  info     CODE                     该公司的页数与文件路径

输出为 UTF-8 文本，带 <<<PAGE n>>> 标记，便于引用页码。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "tools" else Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

# 每个字段的定位锚点。bundle 命令一次把全部字段的候选原文吐出来，
# 目的是把「十几次 search 往返」压成「一次调用」，从而砍掉大量轮数与 token。
FIELD_ANCHORS: dict[str, list[str]] = {
    "col_L": [r"OUR SHARE CAPITAL", r"STATISTICS OF THE GLOBAL OFFERING",
              r"Number of issued Shares upon Listing", r"total number of issued Shares"],
    "col_M": [r"OUR SHARE CAPITAL", r"STATISTICS OF THE GLOBAL OFFERING",
              r"Number of Offer Shares (?:in|under) the Global Offering",
              r"Global Offering of"],
    "col_N": [r"H Shares to be converted from Unlisted Shares",
              r"H Shares converted from Unlisted Shares",
              r"Shares to be issued pursuant to the Capitalisation Issue",
              r"OUR SHARE CAPITAL"],
    "col_O": [r"H Shares to be converted from Unlisted Shares",
              r"H Shares converted from Unlisted Shares",
              r"Shares to be issued pursuant to the Capitalisation Issue",
              r"OUR SHARE CAPITAL"],
    "col_P": [r"Sale Shares", r"selling shareholder", r"Sale Shares being offered"],
    "col_Q": [r"New Shares", r"H Shares to be issued pursuant to the Global Offering",
              r"new Shares.{0,40}Global Offering"],
    "col_R": [r"Placing Shares", r"International Offering of", r"International Offer Shares"],
    "col_S": [r"Public Offer Shares", r"Hong Kong Public Offering of",
              r"Hong Kong Offer Shares"],
    "col_T": [r"Maximum (?:Offer Price|of the Offer Price range)", r"Highest Offer Price",
              r"maximum.{0,20}HK\$"],
    "col_U": [r"Minimum (?:Offer Price|of the Offer Price range)", r"Lowest Offer Price",
              r"minimum.{0,20}HK\$"],
    "col_V": [r"RMB['\u2019]?000", r"currency.{0,30}financial information",
              r"presented in RMB", r"denominated in RMB"],
    "col_W": [r"Total assets", r"TOTAL ASSETS", r"total assets"],
    "col_Z": [r"Total equity", r"TOTAL EQUITY", r"total equity"],
    "col_AC": [r"Total liabilities", r"TOTAL LIABILITIES", r"total liabilities"],
    "col_AF": [r"Revenue\b", r"Total revenue", r"Net sales"],
    "col_AI": [r"Profit before tax", r"PROFIT BEFORE TAX", r"Loss before tax"],
    "col_AL": [r"Profit for the year", r"PROFIT FOR THE YEAR", r"Loss for the year"],
    "col_AO": [r"underwriting commission", r"Underwriting Commissions and (?:Listing )?Expenses",
               r"Underwriting Commission"],
    "col_AQ": [r"Over-?allotment Option", r"Over-allotment Shares"],
    "col_AR": [r"^BUSINESS", r"OVERVIEW", r"we are (?:a|the)", r"our principal business"],
    "col_AS": [r"Chapter 18C", r"Chapter 8A", r"Chapter 18A", r"Chapter 18B",
               r"Specialist Technology", r"Biotech", r"GEM", r"basis of listing"],
    "col_AT": [r"30 June 20\d\d", r"30 September 20\d\d", r"31 December 20\d\d",
               r"Track Record Period"],
    "col_AU": [r"Net cash (?:used in|from|generated from) operating activities",
               r"OPERATING ACTIVITIES", r"net cash flows? (?:used in|from) operating"],
    "col_AV": [r"Cash and cash equivalents at the end of",
               r"cash and cash equivalents at the end"],
    "col_AW": [r"[Rr]esearch and development (?:expense|cost|expenditure)",
               r"R&D (?:expense|expenditure)"],
    "col_AX": [r"[Dd]evelopment cost", r"capitalised development", r"Additions",
               r"INTANGIBLE ASSETS"],
    "col_AY": [r"[Ff]ive largest customers", r"[Tt]op five customers",
               r"largest customer"],
    "col_DP": [r"股份有限公司", r"有限公司"],
    "col_CJ": [r"Cornerstone Investor", r"Cornerstone Placing",
               r"CORNERSTONE INVESTORS"],
    # ---- 扩展 18 列 ----
    "col_BA": [r"Pre-IPO Investment", r"Pre-IPO Investors", r"Pre-IPO Investments"],
    "col_BB": [r"Controlling Shareholders?", r"Substantial Shareholders?",
               r"ultimate beneficial owner"],
    "col_BC": [r"Controlling Shareholders?", r"Substantial Shareholders?",
               r"interest in our Shares"],
    "col_BD": [r"Controlling Shareholders?", r"voting rights", r"Substantial Shareholders?"],
    "col_BE": [r"INDEBTEDNESS", r"Interest-bearing", r"Borrowings", r"bank borrowings"],
    "col_BF": [r"commerciali[sz]", r"mass production", r"in the process of"],
    "col_BG": [r"USE OF PROCEEDS", r"repay(?:ment)? of (?:bank )?borrowings",
               r"FUTURE PLANS AND USE OF PROCEEDS"],
    "col_BI": [r"Share class", r"H Shares", r"Class A Ordinary Shares"],
    "col_BP": [
        r"(?:(?:our|the)\s+Company|predecessor\s+of\s+our\s+Company)\s+was\s+(?:incorporated|established)[\s\S]{0,120}on\s+(?:\d{1,2}\s+[A-Za-z]+|[A-Za-z]+\s+\d{1,2},?)\s+(?:19|20)\d\d",
        r"(?:was )?(?:incorporated|established)\s+(?:under the laws of|in the PRC as|in|as)[\s\S]{0,120}on\s+(?:\d{1,2}\s+[A-Za-z]+|[A-Za-z]+\s+\d{1,2},?)\s+(?:19|20)\d\d",
        r"1\.\s*\n?\s*Incorporation",
        r"Early History and Establishment",
        r"[Ii]ncorporated on\s+(?:\d{1,2}\s+[A-Za-z]+|[A-Za-z]+\s+\d{1,2},?)\s+(?:19|20)\d\d",
        r"[Ee]stablished on\s+(?:\d{1,2}\s+[A-Za-z]+|[A-Za-z]+\s+\d{1,2},?)\s+(?:19|20)\d\d",
    ],
    "col_BR": [r"principal place of business", r"registered office", r"[Hh]ead office"],
    "col_BT": [r"IFRS Accounting Standards", r"HKFRS", r"Accounting Standards",
               r"accounting policies"],
    "col_CC": [r"EXPECTED TIMETABLE", r"Hong Kong Public Offering commences",
               r"commencement of the Hong Kong Public Offering"],
    "col_CD": [r"EXPECTED TIMETABLE", r"applications? (?:close|closing)",
               r"closing of the Hong Kong Public Offering"],
    "col_CE": [r"H Shares to be issued pursuant to the Global Offering",
               r"Number of H Shares"],
    "col_CF": [r"Gross profit", r"GROSS PROFIT"],
    "col_CG": [r"capital expenditure", r"Capital expenditure",
               r"purchase of property, plant and equipment"],
    "col_CH": [r"unqualified", r"in our opinion", r"ACCOUNTANTS. REPORT"],
    "col_CI": [r"listing expenses", r"Listing Expenses",
               r"UNDERWRITING COMMISSIONS AND LISTING EXPENSES"],
}


_DOT = re.compile(r"\.\s*\.\s*\.")


def _is_definitions(text: str) -> bool:
    """Check if page text is part of DEFINITIONS / GLOSSARY section."""
    if not text:
        return False
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return False
    edge = lines[:5] + lines[-5:]
    for ln in edge:
        cleaned = re.sub(r"[^A-Za-z\u4e00-\u9fff]", "", ln).upper()
        if cleaned in {"DEFINITIONS", "DEFINITIONSANDGLOSSARY", "GLOSSARY", "释义", "釋義"}:
            return True
    return False


def _like_toc(text: str) -> bool:
    """目录页有大量点号引导行；真内容页没有。bundle 要跳过目录页，
    否则 'SUBSTANTIAL SHAREHOLDERS' 这类锚点永远命中目录。"""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return True
    dotted = sum(1 for ln in lines if _DOT.search(ln))
    return dotted >= 6 and dotted / len(lines) > 0.25


def _bundle_field(pages: list[dict], patterns: list[str], per_field: int = 3,
                  ctx: int = 3, field_key: str | None = None) -> list[str]:
    blocks: list[str] = []
    for pat in patterns:
        try:
            rx = re.compile(pat, re.I)
        except re.error:
            continue
        for p in pages:
            if _like_toc(p["text"]):
                continue
            if field_key == "col_BP" and _is_definitions(p["text"]):
                continue
            lines = p["text"].splitlines()
            hit = next((i for i, ln in enumerate(lines) if rx.search(ln)), None)
            if hit is None:
                continue
            lo, hi = max(0, hit - ctx), min(len(lines), hit + ctx + 1)
            snippet = " / ".join(s.strip() for s in lines[lo:hi] if s.strip())[:400]
            blocks.append(f"p{p['page']}: {snippet}")
            break
        if len(blocks) >= per_field:
            break
    return blocks


def cmd_periods(args):
    """打印期间判定结果（确定性，见 src/periods.py 的数据集口径）。"""
    from periods import resolve
    pages = load(args.code)
    tr = resolve(pages)
    print("# 招股书出现的中期与年度（来源：" + (tr.source or "无") + "）")
    print("  中期: " + (", ".join(f"{months}M@{end:%Y-%m-%d}x{n}" for end, months, n in tr.stubs) or "无"))
    print("  年度: " + (", ".join(f"FY@{end:%Y-%m-%d}" for end in tr.annual_ends) or "无"))
    if tr.status != "ok":
        print(f"\n# 无法判定：{tr.reason}；请核对 Track Record Period 定义与报表页，不得用减法推期间")
        return
    y1, y2, y3 = tr.year1, tr.year2, tr.year3
    year3 = f"FY{y3.end.year}" if y3 else "无（Track Record 不足两个完整年度，year-3 记缺失）"
    if y1.months < 12:
        print(f"\n# 判定：year-1 = {y1.months}M{y1.end.year}（{y1.start:%d/%m/%Y}–{y1.end:%d/%m/%Y}）；"
              f"year-2 = FY{y2.end.year}；year-3 = {year3}")
        print(f"  col_AT = {y1.end:%d/%m/%y}（资产负债表字段同样取该存根期末）")
        print(f"  年化：销售/税前/净利 ×{12 / y1.months:.4g}（{y1.months} 个月 -> 12 个月）；"
              f"AU/AW/AX/AY/AV/CF/CG 一律不年化")
    else:
        print(f"\n# 判定：均为完整年度 -> year-1 = FY{y1.end.year}；year-2 = FY{y2.end.year}；year-3 = {year3}")
        print(f"  col_AT = {y1.end:%d/%m/%y}")
        print("  不年化（均为全年）")
    print(f"  year-2 = {y2.start:%d/%m/%Y}–{y2.end:%d/%m/%Y}" +
          (f"；year-3 = {y3.start:%d/%m/%Y}–{y3.end:%d/%m/%Y}" if y3 else ""))


def _sharecap_score(text: str) -> int:
    """给页打股本表的分。真表一定同时有『描述行 + 大数字 + Total』。"""
    score = 0
    if re.search(r"converted from Unlisted Shares", text, re.I):
        score += 5
    if re.search(r"to be issued pursuant to the (?:Capitalisation|Capitalization) Issue", text, re.I):
        score += 5
    if re.search(r"H Shares (?:to be )?(?:issued|converted)[^\n]{0,60}Global Offering", text, re.I):
        score += 3
    if re.search(r"Shares to be issued under the Global Offering", text, re.I):
        score += 3
    if re.search(r"Number of issued Shares upon Listing", text, re.I):
        score += 3
    if re.search(r"Number of Shares", text, re.I):
        score += 2
    if re.search(r"\nTotal\s+[\d,]{6,}", text):
        score += 4
    if re.search(r"Approximate %|enlarged issued share", text, re.I):
        score += 3
    if re.search(r"\b\d{1,3}(?:,\d{3}){2,}\b", text):
        score += 2
    # W 股（同股不同权）结构表用这套措辞
    if re.search(r"Issued and to be issued, fully paid", text, re.I):
        score += 6
    if re.search(r"Class [AB] Ordinary Shares", text):
        score += 3
    if re.search(r"nominal value of US\$", text, re.I):
        score += 2
    # 港股标准结构表的三件套措辞
    if re.search(r"(?:UPON COMPLETION OF|immediately following the completion of) "
                 r"the Global Offering", text, re.I):
        score += 3
    if re.search(r"App(?:roximate|roximately)\s*(?:%|percentage)\s*of\s*"
                 r"(?:the\s*)?issued\s*share\s*capital", text, re.I):
        score += 3
    if re.search(r"\nTotal\b", text) and re.search(r"100(?:\.\d+)?\s*%", text):
        score += 2
    if re.search(r"AUTHORIZED AND ISSUED SHARE CAPITAL", text, re.I):
        score += 3
    # 汇总表的标准表头（区分「股本汇总表」与「股东明细表」）
    if re.search(r"Description of Shares", text, re.I):
        score += 4
    if re.search(r"Approximate percentage of (?:total )?share capital", text, re.I):
        score += 4
    if re.search(r"enlarged issued share\s*capital", text, re.I):
        score += 3
    return score


def cmd_sharecap(args):
    """把股本结构表所在页整页打印出来。

    L/M/N/O/P/Q/R/S 全部依赖这张表，必须一次给全——上一版就是靠「搜到哪算哪」
    把 N 填成了历史沿革里的数字。按证据打分，只给最像的 2 页。
    """
    pages = load(args.code)
    DOT = re.compile(r"\.\s*\.\s*\.")
    def is_toc(text: str) -> bool:
        """目录页有大量点号引导行；真表格只有 1–2 行。按密度判断，别误杀表格。"""
        lines = [ln for ln in text.splitlines() if ln.strip()]
        if not lines:
            return True
        dotted = sum(1 for ln in lines if DOT.search(ln))
        return dotted >= 6 and dotted / len(lines) > 0.25
    def table_likeness(text: str) -> int:
        """表格页有大量「纯数字/纯百分比」短行；散文页没有。
        不加这道闸门，光凭措辞会把提到该词的风险因素/责任段误判成股本表。"""
        n = 0
        for ln in text.splitlines():
            t = ln.strip().replace(". . .", "").strip()
            if not t or len(t) > 40:
                continue
            if re.fullmatch(r"[\d,]+(?:\.\d+)?%?", t):
                n += 1
            elif re.fullmatch(r"[-–—]", t):
                n += 1
        return n

    scored = []
    for p in pages:
        if is_toc(p["text"]):
            continue
        if table_likeness(p["text"]) < 5:
            continue
        sc = _sharecap_score(p["text"])
        if sc >= 7:
            scored.append((sc, p["page"], p["text"]))
    scored.sort(key=lambda x: (-x[0], x[1]))
    if not scored:
        print("（没找到股本结构表页，请用 search OUR SHARE CAPITAL）")
        return
    top = scored[:2]
    print(f"# 股本结构表页（按可信度排序）：{[(s, pg) for s, pg, _ in top]}")
    for sc, pg, txt in top:
        print(f"\n<<<PAGE {pg}>>>\n{txt}")


def cmd_bundle(args):
    """一次输出全部字段的候选原文（替代十几次 search 往返）。"""
    pages = load(args.code)
    fields = [f for f in args.fields.split(",") if f]
    total = 0
    for key in fields:
        pats = FIELD_ANCHORS.get(key) or [key.replace("col_", "")]
        blocks = _bundle_field(pages, pats, per_field=args.per_field, ctx=args.context, field_key=key)
        if not blocks:
            print(f"\n### {key}\n（锚点无命中，需要自己 search）")
            continue
        out = "\n".join(f"  - {b}" for b in blocks)
        print(f"\n### {key}\n{out}")
        total += len(out)
        if total > args.max_chars:
            print(f"\n（已达 --max-chars {args.max_chars} 上限，其余字段请用 search）")
            break


def cmd_table(args):
    """打印预解析结构化表格 (Markdown 格式)。"""
    digits = "".join(c for c in str(args.code) if c.isdigit())
    safe_name = f"HKIPO-MB{int(digits):04d}" if digits else args.code
    tables_dir = ROOT / "data" / "tables" / safe_name

    alias = {
        "sharecap": "share_capital",
        "shares": "share_capital",
        "cornerstone": "cornerstone",
        "cj": "cornerstone",
        "underwriting": "underwriting",
        "commissions": "underwriting",
        "financials": "financials",
        "fin": "financials",
    }

    if not tables_dir.exists():
        sys.exit(f"未找到预解析表格目录：{tables_dir}（请先运行 run.py prepare）")

    want = (args.name or "").lower().strip()
    if want in alias:
        want = alias[want]

    if not want:
        md_files = sorted(tables_dir.glob("*.md"))
        if not md_files:
            print(f"[{args.code}] 暂无可用的结构化表格")
            return
        print(f"# {args.code} 可用的结构化表格：")
        for f in md_files:
            print(f"  - {f.stem}")
        return

    target_file = tables_dir / f"{want}.md"
    if not target_file.exists():
        candidates = [f.stem for f in tables_dir.glob("*.md")]
        sys.exit(f"未找到表格 '{want}'。可用表格: {candidates}")

    print(target_file.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="招股书全文检索工具")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("info"); p.add_argument("code"); p.set_defaults(fn=cmd_info)
    p = sub.add_parser("outline"); p.add_argument("code"); p.set_defaults(fn=cmd_outline)
    p = sub.add_parser("search")
    p.add_argument("code"); p.add_argument("pattern")
    p.add_argument("--context", type=int, default=3)
    p.add_argument("--max", type=int, default=8)
    p.add_argument("--ignore-case", action="store_true", default=True)
    p.set_defaults(fn=cmd_search)
    p = sub.add_parser("pages"); p.add_argument("code"); p.add_argument("range")
    p.set_defaults(fn=cmd_pages)
    p = sub.add_parser("periods"); p.add_argument("code"); p.set_defaults(fn=cmd_periods)
    p = sub.add_parser("sharecap"); p.add_argument("code"); p.set_defaults(fn=cmd_sharecap)
    p = sub.add_parser("table")
    p.add_argument("code")
    p.add_argument("name", nargs="?", default="")
    p.set_defaults(fn=cmd_table)
    p = sub.add_parser("bundle")
    p.add_argument("code")
    p.add_argument("--fields", default=",".join(FIELD_ANCHORS))
    p.add_argument("--per-field", type=int, default=3)
    p.add_argument("--context", type=int, default=3)
    p.add_argument("--max-chars", type=int, default=60000)
    p.set_defaults(fn=cmd_bundle)

    args = ap.parse_args()
    args.fn(args)
    return 0


def text_path(code: str) -> Path:
    digits = "".join(c for c in str(code) if c.isdigit())
    from run import load_cfg
    return load_cfg()["paths"]["text"] / f"HKIPO-MB{int(digits):04d}.jsonl"


def load(code: str) -> list[dict]:
    p = text_path(code)
    if not p.exists():
        sys.exit(f"找不到文本文件：{p}（先运行 run.py prepare）")
    return [json.loads(line) for line in p.open(encoding="utf-8")]


def cmd_info(args):
    pages = load(args.code)
    print(f"file: {text_path(args.code)}")
    print(f"pages: {len(pages)}")
    print(f"chars: {sum(len(p['text']) for p in pages)}")


def cmd_outline(args):
    pages = load(args.code)
    for p in pages:
        heads = []
        for line in p["text"].splitlines():
            s = " ".join(line.split())
            if not s or re.fullmatch(r"[\s\-–—\d|.]+", s):
                continue
            heads.append(s[:88])
            if len(heads) >= 2:
                break
        if heads:
            print(f"p{p['page']:>4} | " + " || ".join(heads))


def cmd_search(args):
    pages = load(args.code)
    flags = re.IGNORECASE if args.ignore_case else 0
    try:
        rx = re.compile(args.pattern, flags)
    except re.error as exc:
        sys.exit(f"正则无效：{exc}")
    hits = 0
    for p in pages:
        lines = p["text"].splitlines()
        matched = [i for i, line in enumerate(lines) if rx.search(line)]
        if not matched:
            continue
        hits += 1
        print(f"\n<<<PAGE {p['page']}>>>  （{len(matched)} 处命中）")
        shown: set[int] = set()
        for i in matched:
            for j in range(max(0, i - args.context), min(len(lines), i + args.context + 1)):
                shown.add(j)
        last = -2
        for j in sorted(shown):
            if j != last + 1:
                print("   ...")
            print("   " + lines[j].strip())
            last = j
        if hits >= args.max:
            print(f"\n（已达到 --max {args.max} 页上限，可能还有更多命中）")
            break
    if not hits:
        print("（无命中）")


def cmd_pages(args):
    pages = {p["page"]: p["text"] for p in load(args.code)}
    wanted: list[int] = []
    for part in args.range.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            wanted.extend(range(int(a), int(b) + 1))
        elif part:
            wanted.append(int(part))
    for pg in wanted:
        if pg in pages:
            print(f"\n<<<PAGE {pg}>>>\n{pages[pg]}")
        else:
            print(f"\n<<<PAGE {pg}>>> （不存在）")


if __name__ == "__main__":
    raise SystemExit(main())

if __name__ == "__main__":
    raise SystemExit(main())
