"""Pure reusable calculations; no query access or insight generation."""

from __future__ import annotations

from decimal import Decimal


class Statistics:
    @staticmethod
    def mean(values: list[Decimal]) -> Decimal:
        return sum(values, Decimal("0")) / len(values) if values else Decimal("0")

    @staticmethod
    def variance(values: list[Decimal]) -> Decimal:
        if not values:
            return Decimal("0")
        mean = Statistics.mean(values)
        return sum((value - mean) ** 2 for value in values) / len(values)

    @staticmethod
    def volatility(values: list[Decimal]) -> Decimal:
        return Statistics.variance(values).sqrt()

    @staticmethod
    def z_score(value: Decimal, values: list[Decimal]) -> Decimal:
        deviation = Statistics.volatility(values)
        return (value - Statistics.mean(values)) / deviation if deviation else Decimal("0")

    @staticmethod
    def moving_average(values: list[Decimal], window: int) -> list[Decimal]:
        if window < 1:
            raise ValueError("Window must be positive.")
        return [Statistics.mean(values[max(0, index - window + 1):index + 1]) for index in range(len(values))]
