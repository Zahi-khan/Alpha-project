"""Weighted scoring of accumulated evidence."""

from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext


_DEFAULT_SCORES = {
    EvidenceType.NORMALIZATION: 0.05,
    EvidenceType.MERCHANT_MATCH: 0.75,
    EvidenceType.PAYMENT_DETECTION: 0.05,
    EvidenceType.CATEGORY_LINK: 0.10,
    EvidenceType.INDUSTRY_LINK: 0.10,
}


def score_evidence(context: EnrichmentContext) -> float:
    score = sum(
        evidence.score
        if evidence.score is not None
        else _DEFAULT_SCORES.get(evidence.evidence_type, 0.0)
        for evidence in context.evidence
    )
    score -= min(0.20, 0.05 * len(context.warnings))
    return max(0.0, min(1.0, score))
