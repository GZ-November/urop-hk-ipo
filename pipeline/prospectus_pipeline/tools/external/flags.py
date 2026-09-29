#!/usr/bin/env python3
"""从已有产物确定性推导 7 个空列（不花 token）。

推导来源：
  BH Listing board            ← col_AS（上市途径）是否含 Main Board / GEM
  BJ A+H issuer flag          ← col_AS 是否肯定表明已有 A 股上市（A+H / other listed shares / A Shares …，见 is_a_plus_h）；
                                col_AS 未提及时回退扫招股书全文中发行人自述
                                "Our A Shares are listed on the Shanghai Stock Exchange"（见 a_share_listing_statement）
  BK WVR flag                 ← col_AS 是否肯定援引 "Chapter 8A"（忽略否定式表述）
  BL Chapter 18A flag         ← col_AS 是否肯定援引 "Chapter 18A"（忽略否定式表述）
  BM Chapter 18C flag         ← col_AS 是否肯定援引 "Chapter 18C"（忽略否定式表述）
  BQ Place of incorporation   ← 招股书前几页 "incorporated in ..."
  CL Earliest cornerstone unlock date ← 上市日 + 6 个月（港交所规则；
                                无基石者填 NA，依据配发抽取 col_CK == 0
                                或 cornerstone_absence.json verdict absent/none）

只赋值，不改 font/fill/number_format。写前备份。
证据落到 out/derived_flags.json 供审计（按代码合并，--only 不会抹掉其他公司的记录）。
--dry-run 只打印推导值与工作簿现值的差异，不写工作簿也不写证据。
"""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from contracts import normalize_code  # noqa: E402
from run import load_cfg  # noqa: E402

HEADERS = {
    "BH": "Listing board",
    "BJ": "A+H issuer flag",
    "BK": "WVR flag",
    "BL": "Chapter 18A flag",
    "BM": "Chapter 18C flag",
    "BQ": "Place of incorporation",
    "CL": "Earliest cornerstone unlock date (dd/mm/yy)",
}
LOCKUP_MONTHS = 6


def norm(s) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip().lower()


def add_months(d: dt.date, months: int) -> dt.date:
    """月末安全加月：2026-08-31 + 6 → 2027-02-28。"""
    y, m = divmod(d.month - 1 + months, 12)
    y, m = d.year + y, m + 1
    import calendar
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def cell_str(v) -> str:
    """工作簿单元格值 → 与推导值同口径的字符串（日期取 ISO，整数去 .0）。"""
    if v is None:
        return ""
    if isinstance(v, dt.datetime):
        v = v.date()
    if isinstance(v, dt.date):
        return v.isoformat()
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def digits(code: str) -> str:
    return "".join(c for c in str(code) if c.isdigit())


NEGATION_BEFORE = re.compile(
    r"\b(?:not|no|neither|nor|without|except|other\s+than|rather\s+than)\b\s*"
    r"(?:[^.,;()]{0,40}\s+)?$",
    re.I,
)
NEGATION_AFTER = re.compile(
    r"^\s*(?:[^.,;()]{0,20}\s+)?(?:does\s+not|do\s+not|is\s+not|are\s+not|not)\b",
    re.I,
)


def cites_chapter(text: str, label: str) -> bool:
    """判断上市途径文本是否「肯定地」依据某一章上市。

    招股书抽取文本里大量出现否定式澄清，例如
      "Main Board standard listing (not Chapter 18C / 18A)"
      "H share listing; no Chapter 18C basis disclosed"
    单纯子串匹配会把这类表述误判为肯定，造成 18A/18C 标记假阳性
    （2025Q2 cohort 的 2605.HK、9678.HK 即因此被误标为 18C）。
    这里同时检查命中位置前后的否定词，命中否定式则跳过该处提及。
    """
    return _affirmed(text, re.compile(rf"Chapter\s+{label}", re.I))


def _affirmed(text: str, pattern: re.Pattern) -> bool:
    """pattern 在 text 中至少有一处命中不处于否定语境（前后 NEGATION_* 均不触发）。"""
    for m in pattern.finditer(text):
        before = text[max(0, m.start() - 60): m.start()]
        after = text[m.end(): m.end() + 40]
        if NEGATION_BEFORE.search(before) or NEGATION_AFTER.match(after):
            continue
        if re.search(r"[非无未不]\s*$", before):
            continue
        return True
    return False


# 上市途径文本里 A+H 发行人的几种写法（2025–2026 cohort 实测）：
#   "A+H dual listing ..." / "Chapter 19A PRC issuer (A+H)"
#   "Chapter 19A of the Listing Rules (PRC issuer with other listed shares)"
#   "PRC issuer with A Shares listed on the Shenzhen Stock Exchange"
#   "PRC joint stock company already listed on the SZSE main board"
# 仅写 "Chapter 19A PRC issuer" / "H Share issuer" 的不算——19A 同样适用于
# 只发 H 股、无 A 股的中国发行人。
A_PLUS_H_PATTERNS = [
    re.compile(r"\bA\s*\+\s*H\b"),
    re.compile(r"\bother\s+listed\s+shares\b", re.I),
    re.compile(r"(?<![\w.])A[-\s]?[Ss]hares?\b"),       # "A Shares"/"A-share"；大写 A 避开冠词 "a share"
    re.compile(r"A\s*股"),
    re.compile(r"\blisted\s+on\s+(?:the\s+)?(?:ChiNext|STAR\s+Market|SSE|SZSE|BSE|"
               r"(?:Shanghai|Shenzhen|Beijing)\s+Stock\s+Exchange)\b", re.I),
]


def is_a_plus_h(text: str) -> bool:
    """上市途径文本是否肯定地表明发行人已有 A 股上市（A+H）。

    旧规则只认字面量 "A+H"，漏掉了 2026Q2/Q3 抽取统一写成的
    "PRC issuer with other listed shares"（2476.HK、3308.HK 等 12 家）
    以及 "with A Shares listed on the Shenzhen Stock Exchange"（1081.HK）。
    """
    return any(_affirmed(text, p) for p in A_PLUS_H_PATTERNS)


# 招股书全文里发行人自述 A 股已上市的肯定句（2025–2026 cohort 实测）：
#   "Our A Shares are listed and traded on the Shanghai Stock Exchange"（1276、3288 …）
#   "our A Shares became listed on the Shenzhen Stock Exchange"（2865）
#   "our Company's A Shares have been listed on the main board of Shanghai Stock Exchange"（3296）
#   "The A Shares of our Company have been listed on the Shanghai Stock Exchange STAR Market"（2493）
# 主语限定为 our / our Company's / our Group's / the Company's / the A Shares of our Company：
# H 股发行人提到控股股东、可比公司的 A 股时主语是别的公司，不会命中；
# "Class A Shares"（同股不同权）、"Series A Shares"（融资轮次）因 A 前不是 our 也不会命中。
_A_SHARE_EXCHANGE = (
    r"(?:(?:main\s+board|STAR\s+Market|ChiNext(?:\s+Market)?)\s+of\s+(?:the\s+)?)?"
    r"(?:(?:Shanghai|Shenzhen|Beijing)\s+Stock\s+Exchange|SSE|SZSE|BSE)\b"
)
A_SHARE_LISTING_STATEMENT = re.compile(
    r"(?:\b(?:[Oo]ur|[Tt]he\s+Company['’]s|[Oo]ur\s+(?:Company|Group)['’]s)\s+A[\s-][Ss]hares?"
    r"|\b[Tt]he\s+A[\s-][Ss]hares\s+of\s+(?:our|the)\s+Company)"
    r"\s+(?:are|were|is|was|have\s+been|has\s+been|had\s+been|became)"
    r"\s+(?:currently\s+|already\s+|also\s+)?(?:listed|traded)(?:\s+and\s+(?:listed|traded))?"
    r"\s+on\s+(?:the\s+)?" + _A_SHARE_EXCHANGE
)
# 条件/假设语境（"if our A Shares are listed on …"、"after our A Shares are listed …"）
# 出现在拟 A 股上市的 H 股发行人里，不是已上市的陈述。
HYPOTHETICAL_BEFORE = re.compile(
    r"\b(?:if|once|after|upon|until|unless|before|whether|should|assuming|provided\s+that|in\s+the\s+event)\b"
    r"\s*(?:[^.,;()]{0,40}\s+)?$",
    re.I,
)


def _page_text_path(code: str, text_dir: Path | None) -> Path:
    return (text_dir or ROOT / "data" / "text") / f"HKIPO-MB{digits(code)}.jsonl"


def a_share_listing_statement(code: str, text_dir: Path | None = None) -> dict | None:
    """在招股书全文里找发行人自述「A 股已在上交所/深交所/北交所上市」的肯定句。

    上市途径抽取（col_AS）对不少 A+H 发行人只写 "Main Board" 或
    "Main Board (Chapter 19A PRC issuer)"，is_a_plus_h 无从判断；这里作确定性兜底。
    命中返回 {"page", "quote", "hits"}（首个命中所在页、上下文引文、命中总数），
    否则返回 None；缺页级文本时返回 {"missing_text": True}。
    否定（"… are not listed"）因动词后直接接 listed/traded 本就不会命中；
    否定词与条件语境（NEGATION_BEFORE / HYPOTHETICAL_BEFORE）前置时跳过该处。
    """
    f = _page_text_path(code, text_dir)
    if not f.exists():
        return {"missing_text": True}
    first, hits = None, 0
    with f.open(encoding="utf-8") as stream:
        for line in stream:
            page = json.loads(line)
            flat = " ".join(str(page.get("text") or "").split())
            for m in A_SHARE_LISTING_STATEMENT.finditer(flat):
                before = flat[max(0, m.start() - 60): m.start()]
                if NEGATION_BEFORE.search(before) or HYPOTHETICAL_BEFORE.search(before):
                    continue
                hits += 1
                if first is None:
                    first = {"page": page.get("page"),
                             "quote": flat[max(0, m.start() - 40): m.end() + 60]}
    if first is None:
        return None
    return {**first, "hits": hits}


def place_of_incorporation(code: str, text_dir: Path | None = None) -> tuple[str, str]:
    """扫前若干页判断注册地；返回 (值, 证据)。"""
    f = _page_text_path(code, text_dir)
    if not f.exists():
        return "NA", "缺页级文本"
    head = ""
    for i, line in enumerate(f.open(encoding="utf-8")):
        if i >= 6:
            break
        head += json.loads(line)["text"] + "\n"
    flat = " ".join(head.split())
    # 封面措辞不统一：incorporated / established / organised / formed / registered 都见过
    VERB = r"(?:incorporated|established|organi[sz]ed|formed|registered|constituted)"
    pats = [
        (rf"{VERB}\s+in\s+the\s+People.{{0,3}}s\s+Republic\s+of\s+China", "PRC"),
        (rf"{VERB}\s+in\s+(?:the\s+)?Cayman\s+Islands", "Cayman Islands"),
        (rf"{VERB}\s+in\s+(?:the\s+)?Bermuda", "Bermuda"),
        (rf"{VERB}\s+in\s+the\s+British\s+Virgin\s+Islands", "British Virgin Islands"),
        (rf"{VERB}\s+in\s+Hong\s+Kong", "Hong Kong"),
        # 兜底：直接看 "People's Republic of China with limited liability"
        (r"People.{0,3}s\s+Republic\s+of\s+China\s+with\s+limited\s+liability", "PRC"),
    ]
    for pat, val in pats:
        m = re.search(pat, flat, re.I)
        if m:
            return val, flat[max(0, m.start() - 60):m.end() + 60]
    return "NA", "前 6 页未见注册地表述"


import argparse
from workbook_transaction import workbook_transaction


def main() -> int:
    ap = argparse.ArgumentParser(description="Derive statutory flags")
    ap.add_argument("--config", help="Cohort config (otherwise PIPELINE_CONFIG)")
    ap.add_argument("--dry-run", action="store_true", help="Do not mutate workbook")
    ap.add_argument("--book", help="Path to workbook")
    ap.add_argument("--only", nargs="*", default=None, help="Filter by stock code(s)")
    args = ap.parse_args()
    cfg = load_cfg(config_path=args.config)

    book = Path(args.book) if args.book else cfg["_workbook_path"]
    dry = args.dry_run

    # 基石「确认无」的公司
    ca_path = cfg["paths"]["allot_out"] / "cornerstone_absence.json"
    no_cornerstone = set()
    if ca_path.exists():
        for code, rec in json.loads(ca_path.read_text(encoding="utf-8")).items():
            # cornerstone.py 现写 "absent"；"none" 是旧版记录的同义标签
            if rec.get("verdict") in ("absent", "none"):
                no_cornerstone.add(normalize_code(code))
    # The allotment extraction is the authoritative final allocation. Some
    # cohorts have no separate cornerstone_absence.json at all.
    for path in (cfg["paths"]["allot_out"] / "extracted").glob("HKIPO-MB*.json"):
        rec = json.loads(path.read_text(encoding="utf-8"))
        allocation = (rec.get("fields", {}).get("col_CK") or {}).get("value")
        if isinstance(allocation, (int, float)) and not isinstance(allocation, bool) and allocation == 0:
            no_cornerstone.add(normalize_code(rec["code"]))

    wb_read = openpyxl.load_workbook(book, data_only=True)
    ws_read = wb_read[cfg["sheet"]]
    col_of = {}
    for c in range(1, ws_read.max_column + 1):
        v = ws_read.cell(1, c).value
        if v in (None, ""):
            continue
        for key, h in HEADERS.items():
            if norm(v) == norm(h):
                col_of[key] = c
    missing = [k for k in HEADERS if k not in col_of]
    if missing:
        wb_read.close()
        raise SystemExit(f"工作簿找不到列：{missing}")

    # 行号 + 上市日
    row_of, listing, current = {}, {}, {}
    ci_code = openpyxl.utils.column_index_from_string(cfg["id_columns"]["stock_code"])
    ci_list = openpyxl.utils.column_index_from_string(cfg["id_columns"]["listing_date"])
    selected = {normalize_code(x) for x in args.only} if args.only else None
    for r in range(cfg["data_start_row"], ws_read.max_row + 1):
        code = ws_read.cell(r, ci_code).value
        if code in (None, ""):
            continue
        norm_c = normalize_code(str(code).strip())
        if selected is not None and norm_c not in selected:
            continue
        row_of[norm_c] = r
        ld = ws_read.cell(r, ci_list).value
        if isinstance(ld, dt.datetime):
            ld = ld.date()
        listing[norm_c] = ld if isinstance(ld, dt.date) else None
        current[norm_c] = {k: cell_str(ws_read.cell(r, c).value) for k, c in col_of.items()}
    wb_read.close()
    if not row_of:
        raise SystemExit("没有匹配的公司；检查 --config、--book 和 --only 参数")
    if selected is not None and selected != set(row_of):
        raise SystemExit(f"--only 中有代码未匹配工作簿：{sorted(selected - set(row_of))}")

    audit, n, no_text = {}, 0, []
    print(f"{'code':9s} {'board':10s} {'A+H':4s} {'WVR':4s} {'18A':4s} {'18C':4s} "
          f"{'注册地':14s} 基石解禁")
    for code, r in sorted(row_of.items()):
        jf = cfg["paths"]["out"] / "extracted" / f"HKIPO-MB{digits(code)}.json"
        if not jf.exists():
            raise SystemExit(f"{code}: 缺抽取 JSON：{jf}")
        asv = str(json.loads(jf.read_text(encoding="utf-8"))["fields"]["col_AS"]["value"])
        board = "GEM" if re.search(r"\bGEM\b", asv, re.I) else "Main Board"
        if is_a_plus_h(asv):
            a_plus_h, ah_ev = 1, {"source": "col_AS"}
        else:
            stmt = a_share_listing_statement(code, cfg["paths"]["text"])
            if stmt is None:
                a_plus_h, ah_ev = 0, {"source": "none", "note": "col_AS 与招股书全文均未见 A 股已上市表述"}
            elif stmt.get("missing_text"):
                a_plus_h, ah_ev = 0, {"source": "none", "note": "缺页级文本，未能扫描招股书"}
                no_text.append(code)
            else:
                a_plus_h, ah_ev = 1, {"source": "prospectus", **stmt}
        wvr = 1 if cites_chapter(asv, "8A") else 0
        c18a = 1 if cites_chapter(asv, "18A") else 0
        c18c = 1 if cites_chapter(asv, "18C") else 0
        inc, inc_ev = place_of_incorporation(code, cfg["paths"]["text"])
        ld = listing.get(code)
        if code in no_cornerstone:
            unlock, unlock_note = "NA", "确认无基石，无解禁日"
        elif ld:
            unlock = add_months(ld, LOCKUP_MONTHS)
            unlock_note = f"上市日 {ld} + {LOCKUP_MONTHS} 个月"
        else:
            unlock, unlock_note = "NA", "缺上市日"
        vals = {"BH": board, "BJ": a_plus_h, "BK": wvr, "BL": c18a, "BM": c18c,
                "BQ": inc, "CL": unlock}
        audit[code] = {"values": {k: str(v) for k, v in vals.items()},
                       "evidence": {"col_AS": asv, "a_plus_h": ah_ev,
                                    "incorporation": inc_ev, "unlock": unlock_note}}
        n += 1
        ah_mark = "*" if ah_ev["source"] == "prospectus" else " "
        print(f"{code:9s} {board:10s} {a_plus_h:<3d}{ah_mark} {wvr:4d} {c18a:4d} {c18c:4d} "
              f"{inc:14s} {str(unlock)}")
    print(f"\n推导 {n} 家（A+H 列 * = 由招股书全文兜底判定）")
    if no_text:
        print(f"⚠️ 缺页级文本（BJ 兜底与 BQ 无从判断）：{', '.join(no_text)}")

    changes = [(code, k, current[code][k], rec["values"][k])
               for code, rec in sorted(audit.items()) for k in HEADERS
               if current[code][k] != rec["values"][k]]
    print(f"与工作簿现值不同 {len(changes)} 处" + ("：" if changes else ""))
    for code, k, old, new in changes:
        print(f"  {code:9s} {k} {HEADERS[k]}: {old!r} -> {new!r}")

    if dry:
        print("--dry-run：未写回工作簿，未写证据")
        return 0

    # 按代码合并：--only 只覆盖选中公司的证据，保留其他公司（及共用 out/ 的其他 cohort）的记录
    outj = cfg["paths"]["out"] / "derived_flags.json"
    merged = json.loads(outj.read_text(encoding="utf-8")) if outj.exists() else {}
    merged.update(audit)
    outj.write_text(json.dumps(merged, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    print(f"证据 -> {outj}")

    with workbook_transaction(book, operation="flags") as wb:
        ws = wb[cfg["sheet"]]
        for code, rec in audit.items():
            r = row_of[code]
            for k in ["BH", "BJ", "BK", "BL", "BM", "BQ"]:
                v = rec["values"][k]
                ws.cell(r, col_of[k]).value = int(v) if v.lstrip("-").isdigit() else v
            u = rec["values"]["CL"]
            if u == "NA":
                ws.cell(r, col_of["CL"]).value = "NA"
            else:
                y, m, d = (int(x) for x in u.split("-"))
                ws.cell(r, col_of["CL"]).value = dt.date(y, m, d)

    print(f"已写回 7 列（{len(audit)} 家） -> {book.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
