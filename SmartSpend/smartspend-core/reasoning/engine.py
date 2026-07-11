"""Coordinates rules only; it has no recommendation or presentation logic."""

from intelligence.core.insight import FinancialInsight
from reasoning.context import ReasoningContext
from reasoning.registry import ReasoningRegistry


class ReasoningEngine:
    def __init__(self, registry: ReasoningRegistry):
        self._registry = registry

    def reason(self, insights: tuple[FinancialInsight, ...]) -> tuple:
        context = ReasoningContext(insights=insights)
        for rule in self._registry.rules():
            rule.apply(context)
        return tuple(context.conclusions)
