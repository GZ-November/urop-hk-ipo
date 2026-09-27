"""AI 抽取结果的唯一、严格、可审计 JSON 契约。"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

MISSING_NUMERIC = "NaN"
MISSING_TEXT = "NA"
CONFIDENCES = {"high", "medium", "low"}
FIELD_ENTRY_KEYS = {"value", "page", "quote", "confidence"}
COVERAGE_MIN = 0.90      # 引文至少 90% 的词要能在该页找到连续原文
LONGEST_SPAN_MIN = 0.75  # 且最长的那一段连续原文要占引文 ≥75%（防"两处真话拼一句"）


def normalize_code(value: Any) -> str:
    s = str(value or "").strip().upper().replace(" ", "")
    digits = "".join(c for c in s if c.isdigit())
    return f"{int(digits):04d}.HK" if digits else s


def _no_duplicate_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_constant(value):
    raise ValueError(f"non-standard JSON constant: {value}")


def strict_loads(raw: str, source: str = "JSON") -> Any:
    if raw.startswith("\ufeff"):
        raise ValueError(f"{source}: UTF-8 BOM is not allowed")
    stripped = raw.strip()
    if stripped.startswith("```") or stripped.endswith("```"):
        raise ValueError(f"{source}: Markdown code fence is not allowed")
    return json.loads(
        raw,
        object_pairs_hook=_no_duplicate_pairs,
        parse_constant=_reject_constant,
    )


def strict_load_file(path: Path) -> Any:
    raw = path.read_text(encoding="utf-8")
    return strict_loads(raw, str(path))


def is_missing(value: Any, kind: str) -> bool:
    return value == (MISSING_TEXT if kind in {"text", "date"} else MISSING_NUMERIC)


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _valid_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return bool(re.fullmatch(r"(?:\d{2}/\d{2}/\d{2,4}|\d{4}-\d{2}-\d{2})", value.strip()))


def _valid_value(value: Any, field: dict) -> bool:
    kind = field.get("kind", "text")
    if is_missing(value, kind):
        return True
    if kind == "integer":
        return finite_number(value) and float(value).is_integer() and float(value) >= 0
    if kind == "number":
        return finite_number(value)
    if kind == "date":
        return _valid_date(value)
    return isinstance(value, str) and bool(value.strip())


def validate_record(record: Any, schema: dict, expected_code: str | None = None,
                    target: str = "prospectus", context: dict | None = None) -> list[str]:
    issues: list[str] = []
    if not isinstance(record, dict):
        return ["top-level JSON must be an object"]
    if set(record) != {"code", "fields"}:
        issues.append(f"top-level keys must be exactly code/fields, got {sorted(record)}")
    code = normalize_code(record.get("code"))
    if expected_code and code != normalize_code(expected_code):
        issues.append(f"code mismatch: {record.get('code')!r} != {expected_code!r}")
    fields = record.get("fields")
    if not isinstance(fields, dict):
        return issues + ["fields must be an object"]
    expected = {f["key"] for f in schema["fields"]}
    missing_keys = expected - set(fields)
    extra_keys = set(fields) - expected
    if missing_keys:
        issues.append("missing field keys: " + ", ".join(sorted(missing_keys)))
    if extra_keys:
        issues.append("unknown field keys: " + ", ".join(sorted(extra_keys)))
    by_key = {f["key"]: f for f in schema["fields"]}
    for key, entry in fields.items():
        if key not in by_key:
            continue
        if not isinstance(entry, dict):
            issues.append(f"{key}: entry must be object")
            continue
        # source/note 为流水线确定性回填（目前只有 col_CV 的绿鞋核实）留的可选元数据，
        # 必填仍是 value/page/quote/confidence。
        extra = set(entry) - FIELD_ENTRY_KEYS - {"source", "note"}
        if not FIELD_ENTRY_KEYS <= set(entry) or extra:
            issues.append(f"{key}: entry keys must be value/page/quote/confidence"
                          f"（可选 source/note），实得 {sorted(entry)}")
            continue
        value = entry["value"]
        field = by_key[key]
        if not _valid_value(value, field):
            issues.append(f"{key}: invalid {field.get('kind')} value {value!r}")
        page = entry["page"]
        if page is not None and (not isinstance(page, int) or isinstance(page, bool) or page <= 0):
            issues.append(f"{key}: page must be positive integer or null")
        quote = entry["quote"]
        if not isinstance(quote, str) or len(quote) > 200:
            issues.append(f"{key}: quote must be string <=200 chars")
        confidence = entry["confidence"]
        if confidence not in CONFIDENCES:
            issues.append(f"{key}: invalid confidence {confidence!r}")
        if not is_missing(value, field.get("kind", "text")):
            # 绿鞋检索结论（无行使公告 / 公告已失效）的证据是 greenshoe.json 里的检索记录
            # 本身，不存在对应的「页」，由 validate.check_allot 做确定性核对。
            searched = derived_allowed(record, key, target, context)
            if page is None and not searched:
                issues.append(f"{key}: non-missing value requires page")
            if not quote.strip():
                issues.append(f"{key}: non-missing value requires quote")
    issues.extend(source_issues(record, target, context))
    issues.extend(range_issues(record, schema))
    return issues


def _page_text(packet_text: str, page: int) -> str:
    m = re.search(rf"<<<PAGE\s+{page}>>>\s*(.*?)(?=\n<<<PAGE\s+\d+>>>|\Z)", packet_text, re.S)
    return m.group(1) if m else ""


def _words(s: str) -> list[str]:
    return [w.lower() for w in re.findall(r"[A-Za-z0-9]{2,}|[\u4e00-\u9fff]", str(s))]


def _span_stats(quote: str, page_text: str, min_span: int = 4) -> tuple[float, float]:
    """返回 (总覆盖率, 最长单段占比)。

    只看总覆盖率不够：把**页面上两处真话拼成一句**也能拿到高分。
    因此还要求「最长的那一段连续原文」占引文的比例达标 —— 真照抄应当是**一整段**。
    """
    q, p = _words(quote), _words(page_text)
    if not q:
        return 1.0, 1.0
    pos: dict[str, list[int]] = {}
    for i, w in enumerate(p):
        pos.setdefault(w, []).append(i)
    covered = [False] * len(q)
    longest = 0
    i = 0
    while i < len(q):
        best = 0
        for start in pos.get(q[i], []):
            L = 0
            while i + L < len(q) and start + L < len(p) and q[i + L] == p[start + L]:
                L += 1
            if L > best:
                best = L
        if best >= min_span:
            for k in range(i, i + best):
                covered[k] = True
            longest = max(longest, best)
            i += best
        else:
            i += 1
    return sum(covered) / len(q), longest / len(q)


def _verbatim_coverage(quote: str, page_text: str, min_span: int = 4) -> float:
    """引文被该页连续原文覆盖的词比例（保留此函数供外部调用）。"""
    return _span_stats(quote, page_text, min_span)[0]



def _has_verbatim_span(quote: str, page_text: str, min_words: int = 6) -> bool:
    """兼容旧调用：总覆盖率**且**最长单段占比都达标，才算真照抄。"""
    if len(_words(quote)) < min_words:
        p = _words(page_text)
        return bool(_words(quote)) and all(w in p for w in _words(quote))
    total, longest = _span_stats(quote, page_text)
    return total >= COVERAGE_MIN and longest >= LONGEST_SPAN_MIN


COMPANY_LEVEL_TITLE_PATTERN = re.compile(
    r"(?:STATEMENTS?\s+OF\s+FINANCIAL\s+POSITION\s+(?:OF\s+THE\s+COMPANY|[-–—]\s*THE\s+COMPANY|\(THE\s+COMPANY\))|"
    r"COMPANY\s+STATEMENTS?\s+OF\s+FINANCIAL\s+POSITION|"
    r"BALANCE\s+SHEETS?\s+OF\s+THE\s+COMPANY|"
    r"BALANCE\s+SHEET\s+OF\s+THE\s+COMPANY|"
    r"COMPANY\s+BALANCE\s+SHEETS?|"
    r"STATEMENT\s+OF\s+FINANCIAL\s+POSITION\s+OF\s+THE\s+PARENT)",
    re.IGNORECASE,
)

CONSOLIDATED_FINANCIAL_FIELDS = {
    # 3-year Balance sheet (Assets, Equity, Liabilities)
    "col_W", "col_X", "col_Y",
    "col_Z", "col_AA", "col_AB",
    "col_AC", "col_AD", "col_AE",
    # 3-year Income statement (Sales, PBT, Profit for year)
    "col_AF", "col_AG", "col_AH",
    "col_AI", "col_AJ", "col_AK",
    "col_AL", "col_AM", "col_AN",
    # Cash flow & Indebtedness
    "col_AU", "col_AV", "col_AW", "col_AX", "col_BE",
    # Financial metrics & Meta
    "col_V", "col_BT", "col_CF", "col_CG", "col_CH",
}


def is_company_level_statement(text: str) -> bool:
    """Detect whether page text contains a company-level (parent-only) balance sheet.

    In HK IPO prospectuses (Accountants' Report, Appendix I), parent-only balance sheets
    typically appear immediately after consolidated group balance sheets. They must never
    be cited for Group financial metrics.
    """
    if not text:
        return False
    lines = [line.strip() for line in text.splitlines() if line.strip()][:15]
    header = " ".join(lines).upper()
    if COMPANY_LEVEL_TITLE_PATTERN.search(header):
        return True
    if ("STATEMENT OF FINANCIAL POSITION" in header or "BALANCE SHEET" in header) and "CONSOLIDATED" not in header:
        if "INVESTMENTS IN SUBSIDIARIES" in text.upper() or "INVESTMENT IN SUBSIDIARIES" in text.upper():
            return True
    return False


def is_definitions_page(text: str) -> bool:
    """Detect whether page belongs to the Definitions / Glossary section.

    In HK IPO prospectuses, the Definitions section contains simplified, informal
    or predecessor terms with draft placeholders that frequently conflict with
    statutory company documents. col_BP (Incorporation date) must never be cited
    from Definitions.
    """
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


# 证据来自「检索结论」而非文档原文片段的来源：没有可引用的页码，
# 由 validate.check_allot 拿 greenshoe.json / cornerstone_absence.json 做确定性核对。
SEARCH_SOURCES = {"greenshoe_lapse", "greenshoe_search", "cornerstone_absence", "da_formula"}


def evidence_issues(record: dict, packet_path: Path, schema: dict,
                    alt_texts: dict[str, str] | None = None,
                    target: str = "prospectus", context: dict | None = None) -> list[str]:
    """确认引用页存在、且引文能在**该页**找到连续原文片段（防编造）。

    alt_texts 提供替代证据文档（目前用于 col_CV 的「行使超额配售权公告」）：
    字段条目里带 source="greenshoe" 时，页码/引文改为对行使公告核对。
    source="greenshoe_lapse"/"greenshoe_search" 是检索结论而非引文，
    由 validate.check_allot 拿 greenshoe.json 做确定性核对，这里跳过。
    """
    try:
        text = packet_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"packet unreadable: {exc}"]
    alt_texts = alt_texts or {}
    pages = {int(x) for x in re.findall(r"<<<PAGE\s+(\d+)>>>", text)}
    by_key = {f["key"]: f for f in schema["fields"]}
    issues = []
    for key, entry in record.get("fields", {}).items():
        if key not in by_key or not isinstance(entry, dict):
            continue
        value, page, quote = entry.get("value"), entry.get("page"), entry.get("quote", "")
        if is_missing(value, by_key[key].get("kind", "text")):
            continue
        source = entry.get("source") or "allotment"
        if derived_allowed(record, key, target, context):
            continue
        if source == "greenshoe":
            alt = alt_texts.get("greenshoe")
            if not alt:
                issues.append(f"{key}: 引用绿鞋公告但本地无该公告原文")
                continue
            alt_pages = {int(x) for x in re.findall(r"<<<PAGE\s+(\d+)>>>", alt)}
            if page not in alt_pages:
                issues.append(f"{key}: 绿鞋公告第 {page} 页不存在")
                continue
            pg_text = _page_text(alt, page)
            haystack = pg_text
            text_for_tokens = haystack
        elif source == "prospectus":
            full = alt_texts.get("prospectus")
            if not full:
                issues.append(f"{key}: 引用招股书原文但本地无该招股书全文")
                continue
            full_pages = {int(x) for x in re.findall(r"<<<PAGE\s+(\d+)>>>", full)}
            if page not in full_pages:
                issues.append(f"{key}: 招股书第 {page} 页不存在")
                continue
            pg_text = _page_text(full, page)
            haystack = pg_text
            text_for_tokens = haystack
        else:
            preamble = text.split("<<<PAGE", 1)[0]
            if page in pages:
                pg_text = _page_text(text, page)
                haystack = pg_text + "\n" + preamble
            else:
                # 招股书 packet 只是种子切片；代理用 tools_search 在全文命中的页
                # 必须也能过闸门。alt_texts["prospectus"] 是带 <<<PAGE n>>> 的全文。
                full = alt_texts.get("prospectus")
                if not full:
                    issues.append(f"{key}: cited page {page} is not present in packet")
                    continue
                full_pages = {int(x) for x in re.findall(r"<<<PAGE\s+(\d+)>>>", full)}
                if page not in full_pages:
                    issues.append(f"{key}: cited page {page} is not present in prospectus text")
                    continue
                pg_text = _page_text(full, page)
                haystack = pg_text + "\n" + preamble
            text_for_tokens = haystack
        if key in CONSOLIDATED_FINANCIAL_FIELDS and is_company_level_statement(pg_text):
            issues.append(f"{key}: cited page {page} is from company-level (parent) statement ('...OF THE COMPANY'); "
                          "financial metrics must be extracted from CONSOLIDATED/group statements")
            continue
        if key == "col_BP" and is_definitions_page(pg_text):
            issues.append(f"{key}: cited page {page} is from DEFINITIONS section; "
                          "incorporation date must be cited from Statutory and General Information (Appendix V), "
                          "History and Development, or Accountants' Report, NOT Definitions")
            continue
        tokens = [x.lower() for x in re.findall(r"[A-Za-z0-9]{3,}|[\u4e00-\u9fff]{2,}", quote)]
        if tokens:
            hay_lower = text_for_tokens.lower()
            overlap = sum(1 for t in set(tokens) if t in hay_lower) / len(set(tokens))
            if overlap < 0.25:
                issues.append(f"{key}: 引文与第 {page} 页重合度过低 (overlap={overlap:.2f})")
                continue
        if not _has_verbatim_span(quote, haystack):
            issues.append(f"{key}: 引文在第 {page} 页找不到连续原文片段，疑似拼接/编造")
    return issues


DERIVED_WHITELIST = {
    ("allot", "col_CV", "greenshoe_search"),
    ("allot", "col_CV", "greenshoe_lapse"),
    ("allot", "col_CK", "cornerstone_absence"),
    *(("allot", key, "da_formula") for key in ("col_DA", "col_DB", "col_DC")),
}
DA_DESCRIPTION = ("Free float denominator = total issued shares upon listing (col_CZ); "
                  "numerator = offer shares minus cornerstone allocation")


def derived_allowed(record, key, target="prospectus", context=None):
    fields = record.get("fields", {})
    entry = fields.get(key, {})
    source, value = entry.get("source"), entry.get("value")
    if (target, key, source) not in DERIVED_WHITELIST:
        return False
    ctx = context or {}
    if source == "da_formula":
        values = [(fields.get(k) or {}).get("value") for k in ("col_CS", "col_CK", "col_CZ")]
        if not all(finite_number(v) for v in values) or values[2] <= 0:
            return False
        cs, ck, cz = values
        expected = {"col_DA": round(cs * (1 - ck) / cz, 4),
                    "col_DC": int(round(cz)), "col_DB": DA_DESCRIPTION}[key]
        return value == expected
    if source == "cornerstone_absence":
        ca = ctx.get("cornerstone") or {}
        return value == 0 and ca.get("verdict") == "absent" and ca.get("evidence_complete") is True
    gre = ctx.get("greenshoe") or {}
    if source == "greenshoe_lapse":
        return (value == 0 and gre.get("status") == "ok" and gre.get("exercised") is False
                and any(m.get("kind") == "lapse" for m in gre.get("matches", [])))
    return (value == 0 and gre.get("status") == "ok" and gre.get("exercised") is False
            and gre.get("window_closed") is True)


def source_issues(record, target="prospectus", context=None):
    return [f"{key}: unauthorized or unverified derived source {entry['source']}"
            for key, entry in record.get("fields", {}).items()
            if isinstance(entry, dict) and entry.get("source") in SEARCH_SOURCES
            and not derived_allowed(record, key, target, context)]


def range_issues(record, schema):
    issues = []
    for field in schema["fields"]:
        entry = record.get("fields", {}).get(field["key"], {})
        value = entry.get("value") if isinstance(entry, dict) else None
        if finite_number(value):
            low = field.get("minimum", 0 if field.get("unit") == "decimal" else None)
            high = field.get("maximum", 1 if field.get("unit") == "decimal" else None)
            if ((low is not None and value < low) or
                    (high is not None and value > high)):
                issues.append(f"{field['key']}: {value} outside schema range [{low}, {high}]")
    return issues
