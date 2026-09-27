#!/usr/bin/env python3
"""分析入口：把 master 面板加载为 registry 驱动的 pandas DataFrame。

用法（研究分析侧；采集流水线本身不依赖 pandas，此处惰性导入）：

    import sys
    sys.path.insert(0, "prospectus_pipeline/src")
    from panel import available_slugs, load_master

    available_slugs()                    # 浏览全部 slug / 类型 / 层级
    df = load_master()                   # 全量 202 变量 + 标识列
    df = load_master(slugs=[
        "ipo_subscription_price_hk",
        "filing_price_revision_pct",
    ])                                   # 只取需要的列，自动附带标识列

约定：
  - 列名由原始表头换成注册表 slug（HKIPO_Variable_Registry.yaml 为单一事实来源）；
  - dtype 按注册表解析：date -> datetime64，numeric/boolean -> 数值，string 保持文本；
  - `cohort`、`cross_cohort_duplicate`、`stock_code` 作为标识列始终保留；
  - 汇率相关折算与单位归一有意不在此层处理（口径未定）。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from master_panel import (  # noqa: E402
    DERIVED_SPECS,
    MASTER_STEM,
    REGISTRY_NAME,
    load_registry,
)

IDENTITY_COLUMNS = ["cohort", "cross_cohort_duplicate", "stock_code"]

_NUMERIC_DTYPES = {"numeric", "boolean"}

_DERIVED_NAMES = {name for name, _ in DERIVED_SPECS}


def available_slugs(
    ws: Path | None = None, registry_path: Path | None = None
) -> list[dict[str, Any]]:
    """列出注册表全部变量的 slug 元数据，供分析前选列。"""
    ws = Path(ws) if ws else WS
    registry_path = Path(registry_path) if registry_path else ws / "registry" / REGISTRY_NAME
    if not registry_path.is_file():
        raise FileNotFoundError(f"变量注册表不存在（{registry_path}）；先运行 `python3 run.py registry`")
    registry = load_registry(registry_path)
    keys = ("slug", "header", "dtype", "layer", "unit", "description_zh")
    return [{k: v.get(k) for k in keys} for v in registry["variables"]]


def load_master(
    slugs: list[str] | None = None,
    *,
    ws: Path | None = None,
    master_path: Path | None = None,
    registry_path: Path | None = None,
):
    """把 master 面板读成按注册表重命名并解析 dtype 的 DataFrame。

    slugs 给定时只返回标识列 + 指定列；slug 不存在时列出可用项帮助排查。
    """
    import pandas as pd

    ws = Path(ws) if ws else WS
    master_path = Path(master_path) if master_path else ws / "exports" / f"{MASTER_STEM}_clean.csv"
    if not master_path.is_file():
        raise FileNotFoundError(f"master 面板不存在（{master_path}）；先运行 `python3 run.py master`")
    registry_path = Path(registry_path) if registry_path else ws / "registry" / REGISTRY_NAME
    if not registry_path.is_file():
        raise FileNotFoundError(f"变量注册表不存在（{registry_path}）；先运行 `python3 run.py registry`")

    registry = load_registry(registry_path)
    header_to_slug = {v["header"]: v["slug"] for v in registry["variables"]}
    slug_to_dtype = {v["slug"]: v["dtype"] for v in registry["variables"]}

    frame = pd.read_csv(master_path, encoding="utf-8-sig")
    frame = frame.rename(columns={c: header_to_slug[c] for c in frame.columns if c in header_to_slug})

    for column in frame.columns:
        dtype = slug_to_dtype.get(column)
        if dtype == "date":
            frame[column] = pd.to_datetime(frame[column], errors="coerce")
        elif dtype in _NUMERIC_DTYPES or column in _DERIVED_NAMES:
            # 派生比率列不在注册表中，但同为数值列（--derive 生成的 master）
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    if slugs is not None:
        unknown = [slug for slug in slugs if slug not in slug_to_dtype]
        if unknown:
            raise ValueError(
                f"注册表中不存在这些 slug：{unknown}；用 available_slugs() 查看全部 {len(slug_to_dtype)} 个"
            )
        keep = [c for c in dict.fromkeys([*IDENTITY_COLUMNS, *slugs]) if c in frame.columns]
        frame = frame[keep]
    return frame
