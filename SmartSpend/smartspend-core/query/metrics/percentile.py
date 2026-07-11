"""Nearest-rank percentile metric."""
from math import ceil
from decimal import Decimal
from query.metrics._base import amounts
class PercentileMetric:
    def __init__(self, percentile: float):
        if not 0 < percentile <= 100: raise ValueError("Percentile must be in (0, 100].")
        self.percentile, self.name = percentile, f"p{percentile:g}"
    def calculate(self, items):
        values = sorted(amounts(items))
        return values[ceil(self.percentile / 100 * len(values)) - 1] if values else Decimal("0.00")
