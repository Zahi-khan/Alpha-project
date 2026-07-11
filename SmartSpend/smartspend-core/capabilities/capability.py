"""Plugin contract for a self-contained SmartSpend feature domain."""

from __future__ import annotations

from typing import Protocol

from capabilities.context import CapabilityContext


class Capability(Protocol):
    name: str
    required_inputs: tuple[str, ...]
    produced_outputs: tuple[str, ...]

    def execute(self, context: CapabilityContext) -> None:
        """Consume engine outputs and append only this capability's outputs."""
