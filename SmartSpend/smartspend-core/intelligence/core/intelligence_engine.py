"""Read-only coordinator for registered financial-intelligence capabilities."""

from intelligence.core.intelligence_context import IntelligenceContext
from intelligence.core.registry import IntelligenceRegistry


class FinancialIntelligenceEngine:
    def __init__(self, registry: IntelligenceRegistry):
        self._registry = registry

    def evaluate(self, context: IntelligenceContext) -> tuple:
        for capability in self._registry.capabilities():
            capability.evaluate(context)
        return tuple(context.insights)
