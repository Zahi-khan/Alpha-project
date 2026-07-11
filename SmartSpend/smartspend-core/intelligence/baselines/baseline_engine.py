"""Consistent baseline comparisons used by every intelligence capability."""

from __future__ import annotations

from decimal import Decimal


class BaselineEngine:
    @staticmethod
    def percent_change(current: Decimal, baseline: Decimal) -> Decimal | None:
        if baseline == 0:
            return None
        return (current - baseline) / abs(baseline) * Decimal("100")
