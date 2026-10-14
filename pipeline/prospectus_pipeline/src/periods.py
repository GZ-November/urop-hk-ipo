"""Deterministic Track Record Period resolution (year-1 / year-2 / year-3).

Dataset convention (canonical 2026Q1 workbook, docs/specs/数据规则确认表.md):

* year-1 is the latest financial period of the track record. When that period is a
  stub (3M/4M/5M/6M/7M/8M/9M/10M/11M), year-1 *is* the stub; balance-sheet fields use the
  stub end date and col_AT is the stub end.
* year-2 / year-3 are the two complete financial years before year-1.
* Only year-1 net sales, profit before tax and profit for the period (col_AH/AK/AN) are
  annualised (×12/months). Every other year-1 field keeps the stub's original value.

A stub is accepted only when it starts the day after the latest complete financial year;
a stray "nine months ended 30 September 2022" mention can therefore never displace a later
annual period, and comparison periods are never manufactured by subtraction.
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
TRACK_RECORD_RE = re.compile(r"Track\s+Record\s+Period", re.I)
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


def _scan(texts: list[str], max_year: int) -> tuple[set[dt.date], dict[tuple[dt.date, int], int]]:
    annual: set[dt.date] = set()
    stubs: dict[tuple[dt.date, int], int] = {}
    for text in texts:
        for match in STUB_RE.finditer(text):
            raw = match.group("count").lower()
            months = _WORDS.get(raw) or int(raw)
            if not 1 <= months <= 11:
                continue
            for end in _dates(match):
                if end.year <= max_year:
                    stubs[(end, months)] = stubs.get((end, months), 0) + 1
        for match in YEAR_RE.finditer(text):
            annual.update(end for end in _dates(match) if end.year <= max_year)
    return annual, stubs


def _track_record_windows(pages: list[dict]) -> list[str]:
    windows = []
    for page in pages:
        text = page.get("text") or ""
        for match in TRACK_RECORD_RE.finditer(text):
            windows.append(text[max(0, match.start() - 400): match.end() + 400])
    return windows


def resolve(pages: list[dict], *, today: dt.date | None = None) -> TrackRecord:
    """Resolve year-1/2/3 from page-level prospectus text ({"page", "text"} dicts)."""
    max_year = (today or dt.date.today()).year
    body = pages[:500] + pages[-500:] if len(pages) > 1000 else pages
    statement_pages = [p.get("text") or "" for p in body if STATEMENT_RE.search(p.get("text") or "")]
    trp_annual, trp_stubs = _scan(_track_record_windows(pages), max_year)
    stmt_annual, stmt_stubs = _scan(statement_pages or [p.get("text") or "" for p in body], max_year)

    # The "Track Record Period" definition is the authoritative list of complete years.
    annual_source = trp_annual if len(trp_annual) >= 2 else (trp_annual | stmt_annual)
    source = "track_record_definition" if len(trp_annual) >= 2 else "statement_headers"
    stubs: dict[tuple[dt.date, int], int] = dict(stmt_stubs)
    for key, count in trp_stubs.items():
        stubs[key] = stubs.get(key, 0) + count + 2      # a definition mention is decisive
    result = TrackRecord(status="unresolved", source=source,
                         stubs=sorted((end, months, n) for (end, months), n in stubs.items()))
    if not annual_source:
        result.reason = "no complete financial year found ('year(s) ended ...')"
        return result

    latest = max(annual_source)
    fiscal = (latest.month, latest.day)
    annual = sorted(d for d in annual_source
                    if (d.month, d.day) == fiscal
                    or (fiscal == (2, 29) and (d.month, d.day) == (2, 28))
                    or (fiscal == (2, 28) and (d.month, d.day) == (2, 29)))
    result.annual_ends = annual
    following = latest + dt.timedelta(days=1)
    contiguous = [(end, months, n) for (end, months), n in stubs.items()
                  if end > latest and period_ending(end, months).start == following]
    if contiguous:
        end, months, _ = max(contiguous, key=lambda item: (item[0], item[1]))
        result.year1 = period_ending(end, months)
        prior = annual
    else:
        later = sorted({end for (end, _) in stubs if end > latest})
        if later:
            result.reason = (f"interim period(s) after FY{latest:%Y-%m-%d} found ({', '.join(map(str, later))}) "
                             "but none starts the day after that year end")
            return result
        result.year1 = period_ending(latest, 12)
        prior = annual[:-1]
    complete = [period_ending(end, 12) for end in prior[-2:]]
    for older, newer in zip(complete, complete[1:]):
        if newer.start != older.end + dt.timedelta(days=1):
            result.reason = f"complete years are not consecutive: {older.label}, {newer.label}"
            result.year1 = None
            return result
    if complete and complete[-1].end + dt.timedelta(days=1) != result.year1.start:
        result.reason = f"year-2 {complete[-1].label} does not end the day before year-1 {result.year1.label}"
        result.year1 = None
        return result
    if not complete:
        result.reason = "no complete financial year before year-1"
        result.year1 = None
        return result
    result.year2 = complete[-1]
    result.year3 = complete[-2] if len(complete) == 2 else None
    result.status = "ok"
    return result


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
                if traceable(value, entry.get("quote") or "", factors=(12 / months,), rel_tol=0.002)}
        if len(hits) == 1:
            months = hits.pop()
            votes[months] = votes.get(months, 0) + 1
    if not votes:
        return None
    best = max(votes.items(), key=lambda item: item[1])
    return best[0] if list(votes.values()).count(best[1]) == 1 else None
