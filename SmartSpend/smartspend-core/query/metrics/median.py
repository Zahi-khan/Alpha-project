"""Median metric."""
from decimal import Decimal
from query.metrics._base import amounts
class MedianMetric:
    name = "median"
    def calculate(self, items):
        values = sorted(amounts(items)); count = len(values)
        if not count: return Decimal("0.00")
        middle = count // 2
        return values[middle] if count % 2 else (values[middle - 1] + values[middle]) / 2
