"""Population standard-deviation metric."""
from decimal import Decimal
from query.metrics._base import amounts
class StdDevMetric:
    name = "std_dev"
    def calculate(self, items):
        values = amounts(items)
        if not values: return Decimal("0.00")
        average = sum(values, Decimal("0.00")) / len(values)
        variance = sum((value - average) ** 2 for value in values) / len(values)
        return variance.sqrt()
