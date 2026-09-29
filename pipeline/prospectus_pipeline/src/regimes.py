"""监管制度分期的唯一事实来源：按上市日期推导 FINI 与 2025 定价改革体制。

Col 201 (FINI digital settlement regime) 与 Col 202 (2025 pricing reform regime)
只由上市日期决定。缺日期时 fail-closed 报错，绝不静默默认为 POST_*。
"""
from __future__ import annotations

import datetime as dt
from typing import Any

# FINI 官方上线实施日：2023 年 11 月 22 日
FINI_CUTOFF_DATE = dt.date(2023, 11, 22)
# 2025 年定价与发售机制改革生效日（Mechanism A/B 取代 PN18 回拨）
REFORM_2025_DATE = dt.date(2025, 8, 4)


def _as_date(listing_date: Any, code: str) -> dt.date:
    if isinstance(listing_date, dt.datetime):
        return listing_date.date()
    if isinstance(listing_date, dt.date):
        return listing_date
    if isinstance(listing_date, str) and listing_date.strip():
        try:
            return dt.date.fromisoformat(listing_date.strip()[:10])
        except ValueError:
            pass
    raise ValueError(f"{code or 'issuer'}: cannot derive regime without a valid listing date (got {listing_date!r})")


def fini_regime(listing_date: Any, code: str = "") -> str:
    """POST_FINI 当且仅当上市日期 >= 2023-11-22。"""
    return "POST_FINI" if _as_date(listing_date, code) >= FINI_CUTOFF_DATE else "PRE_FINI"


def pricing_reform_regime(listing_date: Any, code: str = "") -> str:
    """POST_2025_REFORM 当且仅当上市日期 >= 2025-08-04。"""
    return "POST_2025_REFORM" if _as_date(listing_date, code) >= REFORM_2025_DATE else "PRE_2025_REFORM"
