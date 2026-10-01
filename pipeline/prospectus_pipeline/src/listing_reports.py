"""Find official HKEX Main Board new-listing reports for a date interval.

The annual report is the source of issuer membership.  A cached report is
reused only when it covers the requested dates; otherwise the current report
is refreshed from HKEX.  Missing coverage is an error, never an empty cohort.
"""
from __future__ import annotations

import datetime as dt
import os
import re
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlparse

import openpyxl
import requests

MAIN_BOARD_REPORTS = (
    "https://www2.hkexnews.hk/New-Listings/New-Listing-Information/"
    "Main-Board?sc_lang=en"
)
_REPORT_NAME = re.compile(r"(?:NLR)?(19\d{2}|20\d{2})(?:_Eng)?\.xlsx?$", re.I)
_AS_OF = re.compile(r"up to\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})", re.I)
_OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")


class _ReportLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.by_year: dict[int, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href") or ""
        url = urljoin(MAIN_BOARD_REPORTS, href)
        parsed = urlparse(url)
        if parsed.hostname != "www2.hkexnews.hk" or "/New-Listing-Report/Main/" not in parsed.path:
            return
        name = unquote(parsed.path.rsplit("/", 1)[-1])
        match = _REPORT_NAME.fullmatch(name)
        if match:
            self.by_year[int(match.group(1))] = url


def report_links(html: str) -> dict[int, str]:
    parser = _ReportLinks()
    parser.feed(html)
    return parser.by_year


def _local_report(source_dir: Path, year: int) -> Path | None:
    for name in (
        f"NLR{year}_Eng.xlsx", f"NLR{year}_Eng.xls",
        f"{year}.xlsx", f"{year}.xls", f"{year}.XLS",
    ):
        path = source_dir / name
        if path.is_file():
            return path
    return None


def report_as_of(path: Path) -> dt.date | None:
    """Read the coverage date printed in the first cell, when supplied."""
    if path.suffix.lower() == ".xlsx":
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        try:
            title = str(wb.active.cell(1, 1).value or "")
        finally:
            wb.close()
    else:
        import xlrd

        wb = xlrd.open_workbook(str(path), on_demand=True)
        try:
            title = str(wb.sheet_by_index(0).cell_value(0, 0) or "")
        finally:
            wb.release_resources()
    match = _AS_OF.search(title)
    if not match:
        return None
    try:
        return dt.datetime.strptime(match.group(1), "%d %B %Y").date()
    except ValueError:
        return None


def _covers(path: Path, year: int, requested_end: dt.date, today: dt.date) -> bool:
    as_of = report_as_of(path)
    if as_of is None:
        # A current-year report without a coverage date cannot prove completeness.
        return year < today.year
    if requested_end <= as_of:
        return True
    # Archived annual reports close on HKEX's final listing day, which can
    # precede 31 December.  Only treat a late-December historical report as final.
    return year < today.year and as_of.year == year and as_of.month == 12 and as_of.day >= 28


def _save_report(session: requests.Session, url: str, source_dir: Path) -> Path:
    name = unquote(urlparse(url).path.rsplit("/", 1)[-1])
    if not _REPORT_NAME.fullmatch(name):
        raise ValueError(f"Unexpected HKEX report filename: {name}")
    response = session.get(url, timeout=90)
    response.raise_for_status()
    payload = response.content
    is_xlsx = name.lower().endswith(".xlsx")
    if not (payload.startswith(b"PK\x03\x04") if is_xlsx else payload.startswith(_OLE_MAGIC)):
        raise ValueError(f"HKEX returned a non-Excel response for {name}")
    source_dir.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".hkex-report-", dir=source_dir)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        destination = source_dir / name
        os.replace(temporary, destination)
        return destination
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def reports_for_interval(
    start: dt.date,
    end: dt.date,
    source_dir: Path,
    *,
    session: requests.Session | None = None,
    today: dt.date | None = None,
) -> list[Path]:
    """Return complete annual reports or list every year whose coverage failed."""
    today = today or dt.date.today()
    if start > end:
        raise ValueError("period start must be on or before period end")
    if end > today:
        raise ValueError(f"period end {end} is in the future")

    source_dir = Path(source_dir)
    own_session = session is None
    session = session or requests.Session()
    links: dict[int, str] | None = None
    reports: list[Path] = []
    missing: list[str] = []
    try:
        for year in range(start.year, end.year + 1):
            end_in_year = min(end, dt.date(year, 12, 31))
            local = _local_report(source_dir, year)
            if local:
                try:
                    if _covers(local, year, end_in_year, today):
                        reports.append(local)
                        continue
                except Exception:
                    # A damaged cache must be replaced from the official source.
                    pass
            try:
                if links is None:
                    page = session.get(MAIN_BOARD_REPORTS, timeout=40)
                    page.raise_for_status()
                    links = report_links(page.text)
                if year not in links:
                    raise ValueError("no official Main Board report link")
                downloaded = _save_report(session, links[year], source_dir)
                if not _covers(downloaded, year, end_in_year, today):
                    as_of = report_as_of(downloaded)
                    raise ValueError(f"report covers through {as_of}, requested through {end_in_year}")
                reports.append(downloaded)
            except (OSError, ValueError, requests.RequestException) as exc:
                missing.append(f"{year}: {exc}")
    finally:
        if own_session:
            session.close()
    if missing:
        raise ValueError("Official Main Board listing-report coverage missing: " + "; ".join(missing))
    return reports


_SUPPLEMENT_NAME = re.compile(r"NLR(19\d{2}|20\d{2})_Supplement_\d{8}\.ya?ml$", re.I)


def _normalize_supplement_code(raw: Any) -> str:
    digits = "".join(ch for ch in str(raw or "") if ch.isdigit())
    if not digits:
        raise ValueError(f"supplement entry has no usable stock code: {raw!r}")
    return f"{int(digits):04d}.HK"


def _entry_date(entry: dict, field: str, code: str) -> dt.date:
    value = entry.get(field)
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    parsed = None
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                parsed = dt.datetime.strptime(value.strip(), fmt).date()
                break
            except ValueError:
                continue
    if parsed is None:
        raise ValueError(f"supplement entry {code} is missing a usable {field}")
    return parsed


def _supplement_paths(source_dir: Path, year: int) -> list[Path]:
    if not source_dir.is_dir():
        return []
    return sorted(
        path for path in source_dir.iterdir()
        if (match := _SUPPLEMENT_NAME.fullmatch(path.name)) and int(match.group(1)) == year
    )


def load_supplement(
    source_dir: Path,
    year: int,
    start: dt.date,
    end: dt.date,
    *,
    covered_through: dt.date,
) -> list[dict[str, Any]]:
    """Load reviewed supplemental issuer entries beyond an annual report's coverage.

    The supplement never replaces the annual report: it may only extend coverage
    past the report's printed date (``covered_through``).  Every entry must list
    its listing date inside ``(covered_through, end]`` and cite at least one
    official source URL, or the loader fails closed.
    """
    import yaml

    source_dir = Path(source_dir)
    paths = _supplement_paths(source_dir, year)
    if not paths:
        return []
    candidates: list[dict[str, Any]] = []
    for path in paths:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if int(document.get("year", 0)) != year:
            raise ValueError(f"supplement {path.name} declares year {document.get('year')!r}, expected {year}")
        for entry in document.get("entries") or []:
            code = _normalize_supplement_code(entry.get("stock_code"))
            listing = _entry_date(entry, "listing_date", code)
            if not covered_through < listing <= end:
                raise ValueError(
                    f"supplement entry {code} lists on {listing.isoformat()}, outside the "
                    f"gap ({covered_through.isoformat()}, {end.isoformat()}] the supplement is allowed to cover"
                )
            if start > listing:
                continue
            sources = entry.get("sources") or []
            if not any(isinstance(source, dict) and source.get("url") for source in sources):
                raise ValueError(f"supplement entry {code} cites no official source URL")
            offer_price = entry.get("offer_price_hkd")
            candidates.append({
                "file_no": entry.get("file_no"),
                "raw_code": code.split(".")[0],
                "stock_code": code,
                "company_name": str(entry.get("company_name") or "").strip(),
                "prospectus_date": _entry_date(entry, "prospectus_date", code),
                "listing_date": listing,
                "cohort_year": year,
                "sponsors": str(entry.get("sponsors") or "").strip(),
                "auditor": str(entry.get("auditor") or "").strip(),
                "valuer": entry.get("valuer"),
                "funds_raised_public_hkd": entry.get("funds_raised_public_hkd"),
                "funds_raised_int_hkd": entry.get("funds_raised_int_hkd"),
                "offer_price_hkd": float(offer_price) if offer_price is not None else None,
                "raw_price_str": str(entry.get("offer_price_hkd") or "").strip(),
                "raw_funds_str": str(entry.get("funds_raised_public_hkd") or "").strip(),
                "supplement_source": path.name,
                "supplement_sources": [
                    source.get("url") for source in sources if isinstance(source, dict) and source.get("url")
                ],
            })
    return candidates


def reports_and_supplement(
    start: dt.date,
    end: dt.date,
    source_dir: Path,
    *,
    today: dt.date | None = None,
) -> tuple[list[Path], list[dict[str, Any]]]:
    """Return annual reports plus reviewed supplement entries covering [start, end].

    ``reports_for_interval`` fails closed when an annual report lags the requested
    end.  This wrapper keeps that rule but allows a reviewed supplement file
    (``load_supplement``) to cover only the days after the report's printed
    coverage date; the annual report itself is always required.
    """
    today = today or dt.date.today()
    try:
        return reports_for_interval(start, end, source_dir, today=today), []
    except ValueError:
        pass
    reports: list[Path] = []
    supplement: list[dict[str, Any]] = []
    problems: list[str] = []
    seen_reports: set[Path] = set()
    for year in range(start.year, end.year + 1):
        year_start = max(start, dt.date(year, 1, 1))
        year_end = min(end, dt.date(year, 12, 31))
        local = _local_report(source_dir, year)
        if local is not None:
            try:
                if _covers(local, year, year_end, today):
                    if local not in seen_reports:
                        reports.append(local)
                        seen_reports.add(local)
                    continue
            except Exception:
                pass
        as_of = report_as_of(local) if local is not None else None
        if local is None or as_of is None:
            problems.append(f"{year}: no complete official report and no usable cache")
            continue
        if year_start > as_of:
            problems.append(
                f"{year}: report covers through {as_of.isoformat()}, before {year_start.isoformat()}; "
                "a supplement may only extend, not replace, the annual report"
            )
            continue
        reports.append(local)
        seen_reports.add(local)
        if year_end > as_of and not _supplement_paths(source_dir, year):
            problems.append(
                f"{year}: report covers through {as_of.isoformat()}, requested through "
                f"{year_end.isoformat()}; no reviewed supplement file covers the remaining days"
            )
            continue
        supplement.extend(
            load_supplement(source_dir, year, year_start, year_end, covered_through=as_of)
        )
    if problems:
        raise ValueError("Official Main Board listing-report coverage missing: " + "; ".join(problems))
    return reports, supplement
