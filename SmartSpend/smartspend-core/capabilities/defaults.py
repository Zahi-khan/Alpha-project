"""Default capability composition."""

from capabilities.recommendations.engine import RecommendationCapability
from capabilities.registry import CapabilityRegistry


def build_default_capability_registry() -> CapabilityRegistry:
    registry = CapabilityRegistry()
    registry.register(RecommendationCapability())
    return registry
