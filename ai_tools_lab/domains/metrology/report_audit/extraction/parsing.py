"""Small text -> value coercion helpers shared by the extraction modules."""
from __future__ import annotations

import re
from datetime import date, datetime

_DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日")
_NUMBER_PATTERN = re.compile(r"-?\d+(\.\d+)?")


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    value = value.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    match = _NUMBER_PATTERN.search(value.replace("±", ""))
    return float(match.group()) if match else None
