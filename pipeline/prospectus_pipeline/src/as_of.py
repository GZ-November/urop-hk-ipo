"""Observation cutoff shared by market, aftermarket and event engines.

A historical snapshot must not contain bars observed after its cutoff. The cutoff is a Hong Kong
calendar date taken from an explicit argument, then PIPELINE_AS_OF, then today's Hong Kong date.
"""
from __future__ import annotations

import datetime as dt
import os

HK_TZ = dt.timezone(dt.timedelta(hours=8))


def resolve_as_of(value=None) -> dt.date:
    if value is None or value == "":
        value = os.environ.get("PIPELINE_AS_OF") or None
    if value is None:
        return dt.datetime.now(HK_TZ).date()
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value))


def truncate_bars(bars, as_of):
    """Drop observations dated after the cutoff (bars carry a `date` of type date)."""
    return [b for b in bars if b["date"] <= as_of]
