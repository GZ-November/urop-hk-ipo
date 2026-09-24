"""Resolve an IPO issuer cohort from runtime input and a workbook."""
from __future__ import annotations

import datetime as dt
import os
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_-")


def _cohort_for_period(start: dt.date, end: dt.date) -> str:
    start_q = (start.month - 1) // 3 + 1
    end_q = (end.month - 1) // 3 + 1
    if start.year == end.year and start_q == end_q:
        return f"{start.year} Q{start_q}"
    return f"{start.isoformat()} to {end.isoformat()}"


def _to_date(value: Any) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        value = value.strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
            try:
                return dt.datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def _workbook_path(cfg: dict) -> Path:
    path = Path(cfg.get("workbook_path") or cfg.get("_workbook_path") or cfg["workbook"])
    return path if path.is_absolute() else WS / path


def _read_workbook_issuers(cfg: dict) -> list[dict[str, Any]]:
    """Read normalized issuer fields without applying a period filter."""
    import openpyxl
    from openpyxl.utils import column_index_from_string

    wb = openpyxl.load_workbook(_workbook_path(cfg), read_only=True, data_only=True)
    try:
        ws = wb[cfg["sheet"]]
        columns = cfg["id_columns"]
        positions = {
            key: column_index_from_string(column) - 1
            for key, column in columns.items()
        }
        required = {"file_no", "stock_code", "name", "prospectus_date", "listing_date"}
        missing = required - positions.keys()
        if missing:
            raise ValueError(f"id_columns is missing required fields: {', '.join(sorted(missing))}")

        companies = []
        for row_number, values in enumerate(
            ws.iter_rows(
                min_row=cfg["data_start_row"],
                max_col=max(positions.values()) + 1,
                values_only=True,
            ),
            cfg["data_start_row"],
        ):
            code = values[positions["stock_code"]]
            if code in (None, ""):
                continue
            company = {
                "row": row_number,
                "file_no": values[positions["file_no"]],
                "code": str(code).strip(),
                "name": str(values[positions["name"]] or "").strip(),
                "prospectus_date": _to_date(values[positions["prospectus_date"]]),
                "listing_date": _to_date(values[positions["listing_date"]]),
            }
            offer_price_index = positions.get("offer_price")
            company["offer_price"] = (
                values[offer_price_index] if offer_price_index is not None else None
            )
            companies.append(company)
        return companies
    finally:
        wb.close()


def _membership_date(company: dict[str, Any]) -> dt.date | None:
    return company["listing_date"] or company["prospectus_date"]


def load_cfg(
    workbook_override: str | None = None,
    period_start_override: str | None = None,
    period_end_override: str | None = None,
) -> dict:
    """Resolve workbook, date interval, paths, and dataset identity for one run.

    With no date overrides, the configured period remains the default. If only
    one endpoint is supplied, the missing endpoint is inferred from the minimum
    or maximum issuer membership date in the selected workbook.
    """
    workbook_override = workbook_override or os.environ.get("HKIPO_WORKBOOK")
    period_start_override = period_start_override or os.environ.get("HKIPO_PERIOD_START")
    period_end_override = period_end_override or os.environ.get("HKIPO_PERIOD_END")
    with (ROOT / "config.yaml").open(encoding="utf-8") as stream:
        cfg = yaml.safe_load(stream)

    base_workbook = cfg["workbook"]
    if workbook_override:
        cfg["workbook"] = workbook_override
    cfg["_root"] = ROOT
    cfg["_ws"] = WS
    cfg["_workbook_path"] = _workbook_path(cfg)

    dataset = cfg.setdefault("dataset", {})
    has_period_override = bool(period_start_override or period_end_override)
    has_workbook_override = bool(
        workbook_override
        and _workbook_path({"workbook": workbook_override}).resolve()
        != _workbook_path({"workbook": base_workbook}).resolve()
    )
    cfg["filter_period"] = not has_workbook_override or has_period_override

    if has_period_override:
        start = dt.date.fromisoformat(period_start_override) if period_start_override else None
        end = dt.date.fromisoformat(period_end_override) if period_end_override else None
        if start is None or end is None:
            membership_dates = [
                date
                for company in _read_workbook_issuers(cfg)
                if (date := _membership_date(company)) is not None
            ]
            if not membership_dates:
                raise ValueError(
                    "Cannot infer a missing period endpoint: the selected workbook has no issuer dates."
                )
            start = start or min(membership_dates)
            end = end or max(membership_dates)
    else:
        start = dt.date.fromisoformat(dataset["period_start"])
        end = dt.date.fromisoformat(dataset["period_end"])

    if start > end:
        raise ValueError("--period-start must be on or before --period-end")
    dataset["period_start"] = start.isoformat()
    dataset["period_end"] = end.isoformat()

    if has_period_override:
        dataset["cohort"] = _cohort_for_period(start, end)
        period_id = f"{start.isoformat()}_{end.isoformat()}"
        workbook_id = f"_{_slug(Path(workbook_override).stem)}" if has_workbook_override else ""
        dataset["id"] = f"HKIPO_{period_id}{workbook_id}"
    elif has_workbook_override:
        dataset["id"] = _slug(Path(workbook_override).stem)
        dataset["cohort"] = Path(workbook_override).stem

    # Default data keeps canonical paths; overrides get isolated state and outputs.
    if has_period_override or has_workbook_override:
        dataset_root = ROOT / "datasets" / _slug(dataset["id"])
        for key, value in cfg["paths"].items():
            relative = Path(value)
            try:
                suffix = relative.relative_to("prospectus_pipeline")
            except ValueError:
                suffix = relative
            cfg["paths"][key] = str(
                Path("prospectus_pipeline/datasets") / _slug(dataset["id"]) / suffix
            )
        cfg["state_dir"] = dataset_root / ".pipeline_state"

    for key, value in cfg["paths"].items():
        path = WS / value
        path.mkdir(parents=True, exist_ok=True)
        cfg["paths"][key] = path
    return cfg


def read_companies(cfg: dict) -> list[dict[str, Any]]:
    """Return normalized issuers in the configured inclusive date interval."""
    companies = _read_workbook_issuers(cfg)
    start = dt.date.fromisoformat(cfg["dataset"]["period_start"])
    end = dt.date.fromisoformat(cfg["dataset"]["period_end"])
    if cfg.get("filter_period", True):
        companies = [
            company
            for company in companies
            if (membership_date := _membership_date(company)) is not None
            and start <= membership_date <= end
        ]
    elif companies:
        observed_dates = [
            date
            for company in companies
            for date in (company["listing_date"], company["prospectus_date"])
            if date is not None
        ]
        if observed_dates:
            cfg["dataset"]["period_start"] = min(observed_dates).isoformat()
            cfg["dataset"]["period_end"] = max(observed_dates).isoformat()

    selected_codes = cfg.get("_selected_codes")
    if selected_codes is not None:
        selected = set(selected_codes)
        companies = [company for company in companies if company["code"] in selected]
    return companies
