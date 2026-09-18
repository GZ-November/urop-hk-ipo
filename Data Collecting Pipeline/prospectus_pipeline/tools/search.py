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
TEXT_DIR = ROOT / "data" / "text"

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


MONTHS = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,
          "august":8,"september":9,"october":10,"november":11,"december":12}
MON = "|".join(m.capitalize() for m in MONTHS)
# 中期：支持 "nine months ended 30 September 2025" 与 "... September 30, 2025"
STUB_A = re.compile(r"(nine|six|three)\s+months\s+ended\s+(\d{1,2})\s+(" + MON + r")\s+(20\d\d)", re.I)
STUB_B = re.compile(r"(nine|six|three)\s+months\s+ended\s+(" + MON + r")\s+(\d{1,2}),?\s+(20\d\d)", re.I)
YEAR_A = re.compile(r"year\s+ended\s+(\d{1,2})\s+(" + MON + r")\s+(20\d\d)", re.I)
YEAR_B = re.compile(r"year\s+ended\s+(" + MON + r")\s+(\d{1,2}),?\s+(20\d\d)", re.I)
YEAR_C = re.compile(r"years?\s+ended\s+December\s+31,?\s+(20\d\d),\s*(20\d\d)\s+and\s+(20\d\d)", re.I)
YEAR_D = re.compile(r"years?\s+ended\s+31\s+December\s+(20\d\d),\s*(20\d\d)\s+and\s+(20\d\d)", re.I)
MAX_YEAR = 2026


def detect_periods(pages: list[dict]) -> dict:
    """确定性判定 Track Record Period。

    代理看到现成的三年表就直接填 2022/2023/2024，漏掉中期（如 9M2025），
    会让 year-1 的 19 个财务字段全错。所以在这里算死。
    只扫前 500 页 + 后 500 页（摘要表与会计师报告），避免把前瞻年份当历史。
    """
    stubs: dict[tuple[int, int], str] = {}
    stub_days: dict[tuple[int, int], int] = {}
    years: set[int] = set()
    body = pages[:500] + pages[-500:]
    # 只在真正的报表页里认中期：表头口径才作数，
    # 后续事项/季度比较里的偶然提法不算。
    STMT = re.compile(r"CONSOLIDATED STATEMENTS? OF (?:PROFIT OR LOSS|COMPREHENSIVE|"
                      r"FINANCIAL POSITION|CASH FLOWS?)|ACCOUNTANTS. REPORT|"
                      r"SUMMARY OF HISTORICAL FINANCIAL INFORMATION|"
                      r"SUMMARY OF CONSOLIDATED STATEMENTS", re.I)
    stmt_pages = [p for p in body if STMT.search(p["text"])]
    scan = stmt_pages or body
    for p in scan:
        t = p["text"]
        for m in STUB_A.finditer(t):
            w, day, mon, yr = m.group(1).lower(), int(m.group(2)), m.group(3), int(m.group(4))
            stubs[(yr, MONTHS[mon.lower()])] = f"{ {'nine':9,'six':6,'three':3}[w] }M{yr}"
            stub_days[(yr, MONTHS[mon.lower()])] = day
        for m in STUB_B.finditer(t):
            w, mon, day, yr = m.group(1).lower(), m.group(2), int(m.group(3)), int(m.group(4))
            stubs[(yr, MONTHS[mon.lower()])] = f"{ {'nine':9,'six':6,'three':3}[w] }M{yr}"
            stub_days[(yr, MONTHS[mon.lower()])] = day
        for rx, gi in ((YEAR_A, 3), (YEAR_B, 3)):
            for m in rx.finditer(t):
                yr = int(m.group(gi))
                if yr <= MAX_YEAR:
                    years.add(yr)
        for rx in (YEAR_C, YEAR_D):
            for m in rx.finditer(t):
                for g in m.groups():
                    if int(g) <= MAX_YEAR:
                        years.add(int(g))
    stubs = {k: v for k, v in stubs.items() if k[0] <= MAX_YEAR}
    # 统计每个中期的出现次数：Track Record 的中期会在每个表头反复出现，
    # 后续事项/季度比较里的偶然提法只出现一两次。
    freq: dict[tuple[int, int], int] = {}
    for p in scan:
        t = p["text"]
        for rx in (STUB_A, STUB_B):
            for m in rx.finditer(t):
                g = m.groups()
                if rx is STUB_A:
                    mon, yr = g[2], int(g[3])
                else:
                    mon, yr = g[1], int(g[3])
                key = (yr, MONTHS[mon.lower()])
                if yr <= MAX_YEAR:
                    freq[key] = freq.get(key, 0) + 1
    return {"stubs": sorted((y, mo, lab) for (y, mo), lab in stubs.items()),
            "years": sorted(years), "freq": freq, "stub_days": stub_days}


def cmd_periods(args):
    """打印期间判定结果（确定性）。"""
    pages = load(args.code)
    d = detect_periods(pages)
    stubs, years = d["stubs"], d["years"]
    if not stubs and not years:
        print("（未能判定期间，请用 search \"months ended\"）")
        return
    print("# 招股书出现的中期与年度")
    print(f"  中期: {[f'{l}@{m:02d}' for y, m, l in stubs] or '无'}")
    print(f"  年度: {years or '无'}")
    if stubs:
        freq = d.get("freq") or {}
        # Track Record Period 应取报表覆盖的最新中期。频次只用于显示诊断，
        # 不能让重复出现较多的旧比较期覆盖更新期间。
        sy, sm, label = max(stubs, key=lambda x: (x[0], x[1]))
        day = d.get("stub_days", {}).get((sy, sm))
        if freq:
            print("  （各中期出现次数：" +
                  ", ".join(f"{lab}@{mo:02d}x{freq.get((y, mo), 0)}" for y, mo, lab in stubs) + "）")
        n = int("".join(c for c in label if c.isdigit()))
        months = int(label.split("M")[0])
        factor = 12 / months
        print(f"\n# 判定：year-1 = {label}（期末 {sm:02d}/{sy}）；"
              f"year-2 = FY{sy-1}；year-3 = FY{sy-2}")
        if day is None:
            print("  col_AT = 无法确定具体日；必须回报表页核对，不能写月/年占位值")
        else:
            print(f"  col_AT = {day:02d}/{sm:02d}/{str(sy)[2:]}")
        print(f"  年化：销售/税前/净利 ×{factor:.4g}（{months} 个月 -> 12 个月）；"
              f"AU/AW/AX/AY/AV 一律不年化")
    else:
        ly = max(y for y in years if y <= MAX_YEAR)
        print(f"\n# 判定：均为完整年度 -> year-1 = FY{ly}；year-2 = FY{ly-1}；year-3 = FY{ly-2}")
        print(f"  col_AT = 31/12/{str(ly)[2:]}")
        print("  不年化（均为全年）")


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
    return TEXT_DIR / f"HKIPO-MB{int(digits):04d}.jsonl"


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
