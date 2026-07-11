"""Minimal orchestration for ordered enrichment stages."""

from __future__ import annotations

from typing import Iterable

from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage
from models.transaction import Transaction


class EnrichmentPipeline:
    """Runs stages in order; it contains no matching or domain logic itself."""

    def __init__(self, stages: Iterable[EnrichmentStage]):
        self._stages = tuple(stages)

    def run_context(self, transaction: Transaction) -> EnrichmentContext:
        context = EnrichmentContext(transaction=transaction)
        for stage in self._stages:
            context = stage.enrich(context)
        return context

    def run(self, transaction: Transaction):
        """Return the immutable record handed off to the financial memory layer."""
        return self.run_context(transaction).to_enriched_transaction()
