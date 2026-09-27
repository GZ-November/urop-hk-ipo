"""Load and normalize the daily market observations shared by event panels."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from market_fetcher import parse_bar_date


def read_daily_market_panel(path: Path) -> dict[str, list[dict[str, Any]]]:
    """Read daily bars once into per-issuer, date-sorted observations.

    A missing file produces an empty mapping. Rows are grouped by stock code,
    trade dates are normalized with the market fetcher's date parser, and an
    empty daily return is treated as zero to match the panel consumers' prior
    behavior.
    """
    if not path.exists():
        return {}

    daily_bars: dict[str, list[dict[str, Any]]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            code = row["stock_code"]
            daily_bars.setdefault(code, []).append({
                "date": parse_bar_date(row["trade_date"]),
                "close": float(row["close"]),
                "turnover": float(row["turnover"]),
                "daily_return": float(row["daily_return"]) if row.get("daily_return") else 0.0,
            })

    for bars in daily_bars.values():
        bars.sort(key=lambda bar: bar["date"])
    return daily_bars
