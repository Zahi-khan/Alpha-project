"""Single-responsibility contract for intelligence pipeline stages."""

from __future__ import annotations

from typing import Protocol

from intelligence.pipeline.context import EnrichmentContext


class EnrichmentStage(Protocol):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        """Add one kind of knowledge to a context and return it."""
