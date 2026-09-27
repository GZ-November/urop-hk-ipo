#!/usr/bin/env python3
"""out/master/ 面板交付物的契约：文件名、必需列、fail-closed 加载。

producer（stabilization/market/lockup/relational panels）与 consumer
（expansion_mapping）共享同一组常量；此前文件名与列名是两侧各自拼写
的字符串，文件缺失被静默跳过、列改名到写回时才 KeyError。
本 module 让契约违背在加载时立即报错。
"""
from __future__ import annotations

import csv
from pathlib import Path

# 文件名
STABILIZATION_EVENTS = "stabilization_events.csv"
DAILY_MARKET_PANEL = "daily_market_panel.csv"
HORIZON_SUMMARY = "horizon_summary.csv"
LOCKUP_EVENTS = "lockup_events.csv"
INVESTOR_RELATIONAL = "investor_relational.csv"
UNDERWRITER_RELATIONAL = "underwriter_relational.csv"

# 各文件的必需列（消费方直接下标访问的最小集合；.get() 容错访问不在其列）
STABILIZATION_EVENTS_COLS = ["stock_code"]
HORIZON_SUMMARY_COLS = ["stock_code", "horizon"]
DAILY_MARKET_PANEL_COLS = ["stock_code", "amihud_illiq", "zero_volume_flag", "daily_return", "max_drawdown"]
LOCKUP_EVENTS_COLS = ["stock_code", "lockup_category"]
INVESTOR_RELATIONAL_COLS = ["stock_code"]
UNDERWRITER_RELATIONAL_COLS = ["stock_code"]


def require_headers(path: Path, required: list[str]) -> None:
    """文件存在且表头包含全部必需列，否则抛错（fail-closed）。"""
    if not path.is_file():
        raise FileNotFoundError(
            f"master 面板交付物缺失：{path}；请先运行对应面板阶段（market/stabilization/lockup panel）")
    with path.open("r", encoding="utf-8-sig") as fh:
        header = next(csv.reader(fh), [])
    missing = [c for c in required if c not in header]
    if missing:
        raise ValueError(f"{path.name} 缺少契约列 {missing}；producer 与 consumer 必须共享 master_contracts 常量")


def load_rows(path: Path, required: list[str]) -> list[dict[str, str]]:
    """fail-closed 地读取一个面板交付物的全部行。"""
    require_headers(path, required)
    with path.open("r", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load_grouped(path: Path, required: list[str], key: str = "stock_code") -> dict[str, list[dict[str, str]]]:
    """fail-closed 读取并按 key 分组。"""
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in load_rows(path, required):
        grouped.setdefault(row[key], []).append(row)
    return grouped


def load_rows_if_present(path: Path, required: list[str]) -> list[dict[str, str]]:
    """可选交付物：文件缺失时返回空列表；存在但缺契约列则报错。"""
    if not path.is_file():
        return []
    return load_rows(path, required)
