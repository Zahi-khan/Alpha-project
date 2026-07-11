"""Default reasoning-rule composition."""

from reasoning.registry import ReasoningRegistry
from reasoning.rules import CorroboratedTagRule


def build_default_reasoning_registry() -> ReasoningRegistry:
    registry = ReasoningRegistry()
    registry.register(CorroboratedTagRule())
    return registry
