"""Sum metric."""
from decimal import Decimal
from query.metrics._base import amounts
class SumMetric:
    name = "sum"
    def calculate(self, items): return sum(amounts(items), Decimal("0.00"))
