"""Offer-unit registry: how many underlying shares one quoted offer unit represents.

Ordinary listings quote price, offer quantity, applications, volume and lot size
in shares, so the ratio is 1. Depositary-receipt listings (e.g. HDRs) quote all
of these per receipt while share capital is counted in underlying shares.
Offer-quantity fields therefore stay in the quoted unit and only comparisons
against share capital convert with the ratio recorded here. A ratio is accepted
only with cited evidence; see data/manual/offer_units.json.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

REGISTRY = Path(__file__).resolve().parent.parent / "data" / "manual" / "offer_units.json"

# Offer quantities quoted by the announcement/prospectus in offer units.
QUANTITY_FIELDS_PROSPECTUS = ("col_M", "col_R", "col_S")
QUANTITY_FIELDS_ALLOT = ("col_CS", "col_CT", "col_CU")

_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?")


def load_registry(path=None):
    path = Path(path) if path else REGISTRY
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def units_per_offer_unit(code, registry=None):
    """Underlying shares per quoted offer unit (1 unless registered with evidence)."""
    reg = load_registry() if registry is None else registry
    entry = reg.get(code)
    if not entry:
        return 1
    ratio = entry.get("underlying_shares_per_offer_unit")
    if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or not math.isfinite(ratio) or ratio <= 0:
        raise ValueError(f"{code}: offer-unit registry ratio must be a positive number")
    if not entry.get("evidence"):
        raise ValueError(f"{code}: offer-unit ratio requires cited evidence")
    return ratio


def numbers_in(text):
    values = []
    for token in _NUMBER.findall(text or ""):
        try:
            values.append(float(token.replace(",", "")))
        except ValueError:
            continue
    return values


def quote_unit_conflict(value, quote):
    """Return the power-of-ten factor between a stored quantity and its quote, else None.

    A stored quantity equal to a number in its own quote is consistent. If it is
    not, but equals a quoted number scaled by an exact power of ten, the value
    and the evidence are in different units and the record must not be written
    back until the unit mapping is resolved. Quotes with no related number are
    left to the ordinary evidence checks.
    """
    if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value) or value <= 0:
        return None
    candidates = [n for n in numbers_in(quote) if n >= 1000]
    if not candidates:
        return None
    if any(abs(value - n) <= 0.5 for n in candidates):
        return None
    for n in candidates:
        ratio = value / n
        exponent = round(math.log10(ratio))
        if exponent != 0 and abs(ratio - 10 ** exponent) <= 1e-9 * max(1.0, abs(ratio)):
            return 10 ** exponent
    return None


def quantity_conflicts(fields, keys):
    """List `key: ...` messages for quantity fields whose value/quote units disagree."""
    issues = []
    for key in keys:
        entry = fields.get(key)
        if not isinstance(entry, dict):
            continue
        factor = quote_unit_conflict(entry.get("value"), entry.get("quote", ""))
        if factor is not None:
            issues.append(f"{key}: stored value is {factor:g}x a number in its own quote "
                          f"(value={entry.get('value'):,.0f}); resolve the offer-unit mapping "
                          "before write-back")
    return issues
