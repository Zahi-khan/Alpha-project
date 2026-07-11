"""Thin coordinator that discovers and runs registered feature capabilities."""

from capabilities.context import CapabilityContext
from capabilities.registry import CapabilityRegistry


class CapabilityEngine:
    def __init__(self, registry: CapabilityRegistry):
        self._registry = registry

    def execute(self, context: CapabilityContext) -> tuple:
        for capability in self._registry.capabilities():
            capability.execute(context)
        return tuple(context.recommendations)
