"""Compatibility wrapper around evidence-based confidence scoring."""

from intelligence.evidence.score import score_evidence


def score_context(context):
    return score_evidence(context)
