"""Maximum metric."""
from decimal import Decimal
from query.metrics._base import amounts
class MaxMetric:
    name = "max"
    def calculate(self, items): return max(amounts(items), default=Decimal("0.00"))
