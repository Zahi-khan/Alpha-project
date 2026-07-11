"""Locale-neutral clear date labels."""

from __future__ import annotations


def format_date(value) -> str | None:
    return value.strftime("%d %b %Y") if value is not None else None
