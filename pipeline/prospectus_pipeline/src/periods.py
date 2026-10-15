"""Deterministic Track Record Period resolution (year-1 / year-2 / year-3).

Rule (teacher's manual §2.3 "most recent data, annualised if not a full year", restricted to the
audited Track Record; confirmed 2026-10-14; docs/specs/数据规则确认表.md):

* year-1 is the latest period of the audited Track Record, as defined by the prospectus's
  "Track Record Period" glossary entry or the Accountants' Report. When that period is a stub
  (3M-11M), year-1 *is* the stub: balance-sheet fields use the stub end date, col_AT is the
  stub end, and BC = months/12.
* Unaudited periods outside the Track Record are never year-1: interim or quarterly figures in
  an appendix (e.g. an A-share Q1 report), "recent developments", profit estimates or forecasts.
  A definition that lists full years only makes the last full year year-1 even when a later
  contiguous stub appears elsewhere.
* year-2 / year-3 are the two complete financial years of the Track Record before year-1.
* Only year-1 net sales, profit before tax and profit for the period (col_AH/AK/AN) are
  annualised (×12/months). Every other year-1 field keeps the stub's original value.

Resolution order: glossary definition, then the Accountants' Report wording (the two must agree
when both exist); only without either are period mentions on the financial-statement pages
counted. Forward-looking phrases and dates after ``today`` are never periods, a stub must start
the day after the latest complete year, and comparison periods are never manufactured by
subtraction.
"""
from __future__ import annotations

import calendar
import datetime as dt
import math
import re
from dataclasses import dataclass, field

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], start=1)}
_MON = "|".join(m.capitalize() for m in MONTHS)
_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
          "eight": 8, "nine": 9, "ten": 10, "eleven": 11}
_COUNT = r"(?P<count>" + "|".join(_WORDS) + r"|\d{1,2})"
# "30 June 2025" | "June 30, 2025" | table headers "June 30,\n2024 2025" (the last year wins).
_YEARS = r"(?P<years>20\d\d(?:\s*,?\s*(?:and\s+)?20\d\d)*)"
_DATE = (rf"(?:(?P<d1>\d{{1,2}})\s+(?P<m1>{_MON})|(?P<m2>{_MON})\s+(?P<d2>\d{{1,2}}))"
         rf",?\s+{_YEARS}")
STUB_RE = re.compile(rf"\b{_COUNT}[\s-]+months?(?:[\s-]+(?:period|financial\s+period))?\s+"
                     rf"ended\s+(?:on\s+)?{_DATE}", re.I)
YEAR_RE = re.compile(rf"\b(?:financial\s+)?years?\s+ended\s+(?:on\s+)?{_DATE}", re.I)
STATEMENT_RE = re.compile(r"CONSOLIDATED STATEMENTS? OF (?:PROFIT OR LOSS|COMPREHENSIVE|"
                          r"FINANCIAL POSITION|CASH FLOWS?)|ACCOUNTANTS. REPORT|"
                          r"SUMMARY OF HISTORICAL FINANCIAL INFORMATION|"
                          r"SUMMARY OF CONSOLIDATED STATEMENTS", re.I)
ANNUALISED_FIELDS = ("col_AH", "col_AK", "col_AN")


@dataclass(frozen=True)
class Period:
    start: dt.date
    end: dt.date
    months: int

    @property
    def label(self) -> str:
        return f"FY{self.end.year}@{self.end:%m-%d}" if self.months == 12 else f"{self.months}M{self.end.year}@{self.end:%m-%d}"


@dataclass
class TrackRecord:
    status: str                      # ok | unresolved
    reason: str = ""
    year1: Period | None = None
    year2: Period | None = None
    year3: Period | None = None
    annual_ends: list[dt.date] = field(default_factory=list)
    stubs: list[tuple[dt.date, int, int]] = field(default_factory=list)   # (end, months, mentions)
    source: str = ""
    definition: str = ""             # glossary text when source == track_record_definition

    @property
    def annualisation(self) -> float | None:
        return 12 / self.year1.months if self.year1 else None


def month_end(year: int, month: int) -> dt.date:
    return dt.date(year, month, calendar.monthrange(year, month)[1])


def add_months(day: dt.date, months: int) -> dt.date:
    index = day.year * 12 + day.month - 1 + months
    year, month = divmod(index, 12)
    return dt.date(year, month + 1, min(day.day, calendar.monthrange(year, month + 1)[1]))


def period_ending(end: dt.date, months: int) -> Period:
    """Calendar-month period of ``months`` ending on ``end`` (month-end convention)."""
    start = add_months(end.replace(day=1), -(months - 1)) if _is_month_end(end) \
        else add_months(end, -months) + dt.timedelta(days=1)
    return Period(start, end, months)


def _is_month_end(day: dt.date) -> bool:
    return day.day == calendar.monthrange(day.year, day.month)[1]


def parse_date(value) -> dt.date | None:
    """Parse col_AT style dates (31/12/25, 31/12/2025, 2025-12-31, 31 December 2025)."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    text = str(value or "").strip()
    if not text or text.upper() in {"NA", "NAN", "NONE"}:
        return None
    match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if match:
        year, month, day = (int(x) for x in match.groups())
    else:
        match = re.search(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})\b", text)
        if match:
            day, month, year = (int(x) for x in match.groups())
            year = year + 2000 if year < 100 else year
        else:
            match = re.search(rf"\b(\d{{1,2}})\s+({_MON})\s+(\d{{4}})\b", text, re.I)
            if not match:
                return None
            day, month, year = int(match.group(1)), MONTHS[match.group(2).lower()], int(match.group(3))
    try:
        return dt.date(year, month, day)
    except ValueError:
        return None


def _dates(match: re.Match) -> list[dt.date]:
    day = int(match.group("d1") or match.group("d2"))
    month = MONTHS[(match.group("m1") or match.group("m2")).lower()]
    out = []
    for year in re.findall(r"20\d\d", match.group("years")):
        try:
            out.append(dt.date(int(year), month, day))
        except ValueError:
            continue
    return out


# Forward-looking mentions ("For the year ended December 31, 2026, we expect to pay ...") are not periods.
_FORWARD_RE = re.compile(r"\b(?:expect|estimat|forecast|anticipat|budget|project(?:ed|ion)|will|shall)", re.I)


def _forward_looking(text: str, match: re.Match) -> bool:
    tail = re.split(r"\.|\bended\b", text[match.end(): match.end() + 80], maxsplit=1)[0]   # this phrase only
    return bool(_FORWARD_RE.search(tail))


def _scan(texts: list[str], max_date: dt.date) -> tuple[dict[dt.date, int], dict[tuple[dt.date, int], int]]:
    """Mention counts of year ends and of (stub end, months), skipping forward-looking phrases."""
    annual: dict[dt.date, int] = {}
    stubs: dict[tuple[dt.date, int], int] = {}
    for text in texts:
        for match in STUB_RE.finditer(text):
            raw = match.group("count").lower()
            months = _WORDS.get(raw) or int(raw)
            if not 1 <= months <= 11 or _forward_looking(text, match):
                continue
            for end in _dates(match):
                if end <= max_date:
                    stubs[(end, months)] = stubs.get((end, months), 0) + 1
        for match in YEAR_RE.finditer(text):
            if _forward_looking(text, match):
                continue
            for end in _dates(match):
                if end <= max_date:
                    annual[end] = annual.get(end, 0) + 1
    return annual, stubs


# ---------------------------------------------------------------- glossary definition
# '"Track Record Period" the three years ended December 31, 2025 and the four months ended April 30, 2026'
# is the issuer's own statement of which periods the accountants' report covers. Narrative uses such as
# '(the "Track Record Period") and ...' start with a bracket and are not definitions.
_QUOTE = "[“”\"'‘’]"
DEFINITION_RE = re.compile(
    _QUOTE + r"{1,2}\s*Track\s+Record\s+Period\s*" + _QUOTE + r"{1,2}\s*(?![),])"
    r"(?:means\s+|refers\s+to\s+)?(?P<body>[^“‘\";]{0,300})", re.I)
_DEF_YEAR_RE = re.compile(rf"\b(?:{_COUNT}\s+)?(?:financial\s+)?years?(?:\s*/\s*periods?)?\s+ended\s+"
                          rf"(?:on\s+)?{_DATE}", re.I)
_FY_RE = re.compile(r"(?<![\dM])FY\s?(20\d\d)\b")                 # FY2025
_FY_STUB_RE = re.compile(r"\b(\d{1,2})\s?M(?:FY)?\s?(20\d\d)\b")   # 6M2026, 10MFY2025


@dataclass(frozen=True)
class Definition:
    text: str
    annual: tuple[dt.date, ...] = ()       # explicit year ends ("years ended December 31, 2023, 2024 and 2025")
    fy_years: tuple[int, ...] = ()         # FY shorthand; fiscal year end comes from the statements
    stub_months: int | None = None
    stub_end: dt.date | None = None        # None for shorthand stubs ("6M2026"): contiguity fixes the end


def _years_back(day: dt.date, years: int) -> dt.date:
    try:
        return day.replace(year=day.year - years)
    except ValueError:                     # 29 February
        return day.replace(year=day.year - years, day=28)


def parse_definition(body: str) -> Definition | None:
    """Periods named by a "Track Record Period" glossary entry, or None if it names no year."""
    body = re.sub(r"[\s\x00-\x1f]+", " ", body).strip()
    annual: list[dt.date] = []
    for match in _DEF_YEAR_RE.finditer(body):
        ends = sorted(_dates(match))
        raw = (match.group("count") or "").lower()
        count = _WORDS.get(raw) or (int(raw) if raw.isdigit() else 0)
        if len(ends) == 1 and count > 1:   # "the three years ended December 31, 2025"
            ends = [_years_back(ends[0], back) for back in range(count - 1, 0, -1)] + ends
        annual.extend(ends)
    stub_months = stub_end = None
    for match in STUB_RE.finditer(body):
        raw = match.group("count").lower()
        months = _WORDS.get(raw) or int(raw)
        ends = _dates(match)
        if 1 <= months <= 11 and ends:
            stub_months, stub_end = months, max(ends)
    for match in _FY_STUB_RE.finditer(body):
        if stub_months is None and 1 <= int(match.group(1)) <= 11:
            stub_months = int(match.group(1))
    fy_years = tuple(sorted({int(y) for y in _FY_RE.findall(body)}))
    if not annual and not fy_years:
        return None
    return Definition(body, tuple(sorted(set(annual))), fy_years, stub_months, stub_end)


# Accountants' Report: "... for each of the three years ended 31 December 2025 and the three months
# ended 31 March 2026 (the "Track Record Period")" -- the audited periods precede the bracketed term.
REPORT_DEFINITION_RE = re.compile(r"\((?:together,\s+)?the\s+" + _QUOTE + r"{1,2}\s*Track\s+Record\s+Period\s*"
                                  + _QUOTE + r"{1,2}\)", re.I)


def find_definition(pages: list[dict]) -> Definition | None:
    """The glossary entry ('"Track Record Period" the years ended ...'), first one that names a year."""
    for page in pages:
        text = re.sub(r"[\s\x00-\x1f]+", " ", page.get("text") or "")
        for match in DEFINITION_RE.finditer(text):
            definition = parse_definition(match.group("body"))
            if definition is not None:
                return definition
    return None


def find_report_definition(pages: list[dict]) -> Definition | None:
    """The Accountants' Report wording ('for each of the ... (the "Track Record Period")')."""
    for page in pages:
        text = re.sub(r"[\s\x00-\x1f]+", " ", page.get("text") or "")
        for match in REPORT_DEFINITION_RE.finditer(text):
            window = text[max(0, match.start() - 300): match.start()]
            cut = max(window.rfind("for each of"), window.rfind("for the "))
            definition = parse_definition(window[cut:]) if cut >= 0 else None
            if definition is not None:
                return definition
    return None


def _fiscal_end(years: tuple[int, ...], annual_counts: dict[dt.date, int]) -> tuple[int, int]:
    """(month, day) of the FY shorthand years, voted from 'year(s) ended ...' mentions; default 31 Dec."""
    votes: dict[tuple[int, int], int] = {}
    for end, n in annual_counts.items():
        if end.year in years:
            votes[(end.month, end.day)] = votes.get((end.month, end.day), 0) + n
    return max(votes.items(), key=lambda item: item[1])[0] if votes else (12, 31)


def _close(result: TrackRecord, year1: Period, prior: list[dt.date]) -> TrackRecord:
    """year-2/year-3 are the two complete years before year-1; they must be consecutive."""
    complete = [period_ending(end, 12) for end in prior[-2:]]
    for older, newer in zip(complete, complete[1:]):
        if newer.start != older.end + dt.timedelta(days=1):
            result.reason = f"complete years are not consecutive: {older.label}, {newer.label}"
            return result
    if not complete:
        result.reason = "no complete financial year before year-1"
        return result
    if complete[-1].end + dt.timedelta(days=1) != year1.start:
        result.reason = f"year-2 {complete[-1].label} does not end the day before year-1 {year1.label}"
        return result
    result.year1, result.year2 = year1, complete[-1]
    result.year3 = complete[-2] if len(complete) == 2 else None
    result.status = "ok"
    return result


def _from_definition(result: TrackRecord, definition: Definition,
                     annual_counts: dict[dt.date, int]) -> TrackRecord:
    annual = list(definition.annual)
    if not annual:
        month, day = _fiscal_end(definition.fy_years, annual_counts)
        annual = [dt.date(year, month, min(day, calendar.monthrange(year, month)[1]))
                  for year in definition.fy_years]
    result.annual_ends = annual
    latest = annual[-1]
    if definition.stub_months is None:     # only complete years: the last one is year-1
        return _close(result, period_ending(latest, 12), annual[:-1])
    start = latest + dt.timedelta(days=1)
    end = add_months(start, definition.stub_months) - dt.timedelta(days=1)
    if definition.stub_end is not None and definition.stub_end != end:
        result.reason = (f"defined {definition.stub_months}-month period ended {definition.stub_end} does not "
                         f"start the day after FY{latest:%Y-%m-%d}")
        return result
    return _close(result, Period(start, end, definition.stub_months), annual)


# Without a definition, a contiguous stub is year-1 only when the statements cite it at least this
# often relative to the last complete year. Track Record stubs are cited 1.4-3x as often as that year
# (2025Q4-2026Q3 sample); appended post-track-record quarters (A-share Q1 reports) at most 0.5x.
STUB_CITATION_RATIO = 0.75


def resolve(pages: list[dict], *, today: dt.date | None = None) -> TrackRecord:
    """Resolve year-1/2/3 from page-level prospectus text ({"page", "text"} dicts).

    The "Track Record Period" glossary definition is authoritative: when it lists only complete years,
    year-1 is the last of them even if later interim figures (A-share quarterly reports, recent
    developments, profit estimates) appear elsewhere. Without a definition, period mentions on the
    financial-statement pages are counted (see STUB_CITATION_RATIO). ``today`` bounds accepted period
    ends (default: the current date).
    """
    max_date = today or dt.date.today()
    body = pages[:500] + pages[-500:] if len(pages) > 1000 else pages
    statement_pages = [p.get("text") or "" for p in body if STATEMENT_RE.search(p.get("text") or "")]
    annual_counts, stubs = _scan(statement_pages or [p.get("text") or "" for p in body], max_date)
    result = TrackRecord(status="unresolved", stubs=sorted((end, months, n) for (end, months), n in stubs.items()))

    glossary, report = find_definition(pages), find_report_definition(pages)
    if glossary is not None or report is not None:
        definition = glossary or report
        result.source = "track_record_definition" if glossary is not None else "accountants_report"
        result.definition = definition.text
        resolved = _from_definition(result, definition, annual_counts)
        if glossary is not None and report is not None and resolved.status == "ok":
            check = _from_definition(TrackRecord(status="unresolved"), report, annual_counts)
            if check.status == "ok" and check.year1 != resolved.year1:
                return TrackRecord(status="unresolved", source=result.source, definition=definition.text,
                                   stubs=result.stubs, annual_ends=result.annual_ends,
                                   reason=f"glossary defines year-1 {resolved.year1.label} but the Accountants' "
                                          f"Report defines {check.year1.label}")
        return resolved

    result.source = "statement_headers"
    # The latest stub cited with its prior-year comparative is the reported interim period; a
    # "year ended" date whose year contains it (a current-year profit estimate) is not a complete year.
    interim = max((end for (end, months) in stubs if (_years_back(end, 1), months) in stubs), default=None)
    if interim is not None:
        annual_counts = {year_end: n for year_end, n in annual_counts.items()
                         if not _years_back(year_end, 1) < interim < year_end}
    if not annual_counts:
        result.reason = "no complete financial year found ('year(s) ended ...')"
        return result

    def fiscal_key(day: dt.date) -> tuple[int, int]:
        return (2, 28) if (day.month, day.day) == (2, 29) else (day.month, day.day)

    votes: dict[tuple[int, int], int] = {}
    for year_end, n in annual_counts.items():
        votes[fiscal_key(year_end)] = votes.get(fiscal_key(year_end), 0) + n
    fiscal = max(votes.items(), key=lambda item: item[1])[0]
    annual = sorted(d for d in annual_counts if fiscal_key(d) == fiscal)
    result.annual_ends = annual
    latest = annual[-1]
    threshold = STUB_CITATION_RATIO * annual_counts[latest]
    following = latest + dt.timedelta(days=1)
    contiguous = [(n, end, months) for (end, months), n in stubs.items()
                  if end > latest and n >= threshold and period_ending(end, months).start == following]
    if contiguous:
        _, end, months = max(contiguous)
        return _close(result, period_ending(end, months), annual)
    later = sorted({end for (end, _), n in stubs.items() if end > latest and n >= threshold})
    if later:
        result.reason = (f"interim period(s) after FY{latest:%Y-%m-%d} found ({', '.join(map(str, later))}) "
                         "but none starts the day after that year end")
        return result
    return _close(result, period_ending(latest, 12), annual[:-1])


def _numbers(text: str) -> list[tuple[float, int]]:
    """(number, decimals) in a quote; parenthesised accounting negatives keep their sign."""
    values = []
    for token in re.findall(r"\(?-?\d[\d,]*(?:\.\d+)?\)?", str(text or "")):
        raw = token.strip("()").replace(",", "")
        try:
            number = float(raw)
        except ValueError:
            continue
        if number:
            decimals = len(raw.split(".", 1)[1]) if "." in raw else 0
            values.append((-abs(number) if token.startswith("(") and token.endswith(")") else number, decimals))
    return values


SCALES = (1, 1_000, 10_000, 1_000_000, 100_000_000, 1_000_000_000)


def traceable(value, quote: str, *, factors=(1.0,), rel_tol: float = 0.0015, scales=SCALES) -> bool:
    """Whether ``value`` equals a quoted number × unit scale × factor (sign-insensitive).

    The quoted figure's own rounding is honoured: "RMB1,073.3 million" supports any value
    within ±0.05 million.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        return True
    if value == 0:
        return True
    for number, decimals in _numbers(quote):
        for scale in scales:
            for factor in factors:
                target = abs(number) * scale * factor
                rounding = 0.5 * 10 ** -decimals * scale * factor if decimals else 0.0
                if abs(abs(value) - target) <= max(rel_tol * target, rounding):
                    return True
    return False


def payload_months(fields: dict) -> int | None:
    """Year-1 period length implied by annualised col_AH/AK/AN versus their quoted originals."""
    votes: dict[int, int] = {}
    for key in ANNUALISED_FIELDS:
        entry = fields.get(key) or {}
        value = entry.get("value")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not value:
            continue
        hits = {months for months in range(1, 13)
                if traceable(value, entry.get("quote") or "", factors=(12 / months,), rel_tol=0.0015)}
        if len(hits) == 1:
            months = hits.pop()
            votes[months] = votes.get(months, 0) + 1
    if not votes:
        at_q = (fields.get("col_AT") or {}).get("quote") or ""
        m = STUB_RE.search(at_q)
        if m:
            cnt = m.group("count").lower()
            return _WORDS.get(cnt) or int(cnt)
        return None
    best = max(votes.items(), key=lambda item: item[1])
    return best[0] if list(votes.values()).count(best[1]) == 1 else None

