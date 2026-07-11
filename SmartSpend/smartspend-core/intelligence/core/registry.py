"""Discovery registry for independently deployable intelligence engines."""

from intelligence.core.capability import IntelligenceCapability


class IntelligenceRegistry:
    def __init__(self):
        self._capabilities: dict[str, IntelligenceCapability] = {}

    def register(self, capability: IntelligenceCapability) -> None:
        self._capabilities[capability.name] = capability

    def capabilities(self) -> tuple[IntelligenceCapability, ...]:
        return tuple(self._capabilities.values())
