"""Discovery registry for independent analysis modules."""

from __future__ import annotations

from typing import Protocol

from analytics.core.analytics_context import AnalyticsContext


class AnalysisModule(Protocol):
    name: str
    def analyze(self, context: AnalyticsContext) -> None:
        """Append zero or more insights to the context."""


class AnalyticsRegistry:
    def __init__(self):
        self._modules: dict[str, AnalysisModule] = {}

    def register(self, module: AnalysisModule) -> None:
        self._modules[module.name] = module

    def modules(self) -> tuple[AnalysisModule, ...]:
        return tuple(self._modules.values())
