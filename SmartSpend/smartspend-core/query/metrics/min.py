"""Minimum metric."""
from decimal import Decimal
from query.metrics._base import amounts
class MinMetric:
    name = "min"
    def calculate(self, items): return min(amounts(items), default=Decimal("0.00"))
