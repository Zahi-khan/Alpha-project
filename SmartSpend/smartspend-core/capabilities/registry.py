"""Discovery registry for independent SmartSpend capabilities."""

from capabilities.capability import Capability


class CapabilityRegistry:
    def __init__(self):
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        self._capabilities[capability.name] = capability

    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(self._capabilities.values())
