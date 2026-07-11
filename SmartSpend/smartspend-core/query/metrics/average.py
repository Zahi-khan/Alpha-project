"""Average metric."""
from decimal import Decimal
from query.metrics._base import amounts
class AverageMetric:
    name = "average"
    def calculate(self, items):
        values = amounts(items)
        return sum(values, Decimal("0.00")) / len(values) if values else Decimal("0.00")
