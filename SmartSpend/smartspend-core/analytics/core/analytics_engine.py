"""Runs registered analysis modules; contains no financial interpretation itself."""

from analytics.core.analytics_context import AnalyticsContext
from analytics.core.registry import AnalyticsRegistry


class AnalyticsEngine:
    def __init__(self, registry: AnalyticsRegistry):
        self._registry = registry

    def analyze(self, context: AnalyticsContext) -> tuple:
        for module in self._registry.modules():
            module.analyze(context)
        return tuple(context.insights)
