"""Calendar-month endpoints shared by market and lockup event panels."""
from __future__ import annotations

import calendar
import datetime as dt


def add_calendar_months(day: dt.date, months: int) -> dt.date:
    """Shift by calendar months, clipping month-end to the last valid day."""
    total = day.year * 12 + day.month - 1 + months
    year, month = divmod(total, 12)
    month += 1
    return dt.date(year, month, min(day.day, calendar.monthrange(year, month)[1]))
