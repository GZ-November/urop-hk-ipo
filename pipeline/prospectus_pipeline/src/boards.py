"""Board identity and source isolation, independent of stock-code heuristics."""
from __future__ import annotations

from pathlib import Path


def normalize_board(value: str | None) -> str:
    normalized = str(value or "main").lower().replace(" ", "").replace("_", "")
    if normalized in ("main", "mainboard", "mb"):
        return "main"
    if normalized == "gem":
        return "gem"
    raise ValueError(f"Unsupported listing board: {value}")


def board_label(value: str | None) -> str:
    return "GEM" if normalize_board(value) == "gem" else "Main Board"


def board_prefix(value: str | None) -> str:
    return "HKIPO-GEM" if normalize_board(value) == "gem" else "HKIPO-MB"


def report_source_dir(ws: Path, board: str | None) -> Path:
    return ws / "sources" / "GEM" if normalize_board(board) == "gem" else ws / "sources"


def report_page(board: str | None) -> str:
    segment = "GEM" if normalize_board(board) == "gem" else "Main-Board"
    return f"https://www2.hkexnews.hk/New-Listings/New-Listing-Information/{segment}?sc_lang=en"
