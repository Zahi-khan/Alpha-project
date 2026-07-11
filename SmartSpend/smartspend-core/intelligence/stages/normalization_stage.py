"""Normalize bank-statement text without attempting to resolve meaning."""

from __future__ import annotations

import re

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage


class NormalizationStage(EnrichmentStage):
    """Removes common bank prefixes and standardizes statement descriptions."""

    _PREFIX = re.compile(r"^(?:UPI|NEFT|IMPS|RTGS|POS|ECOM|CARD)[\s/:_-]+", re.IGNORECASE)
    _SEPARATORS = re.compile(r"[/:_|-]+")

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        value = context.transaction.description.strip()
        value = self._PREFIX.sub("", value)
        value = self._SEPARATORS.sub(" ", value)
        value = re.sub(r"\s+", " ", value).strip().upper()
        context.normalized_description = value
        context.add_evidence(
            Evidence(
                EvidenceType.NORMALIZATION,
                f'Normalized description to "{value}".',
                source="normalization_stage",
            )
        )
        return context
