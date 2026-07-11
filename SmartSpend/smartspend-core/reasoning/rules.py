"""Declarative, explainable rules for combining related insights."""

from __future__ import annotations

from collections import defaultdict

from intelligence.core.insight import FinancialInsight
from models.financial_conclusion import FinancialConclusion
from reasoning.context import ReasoningContext


class CorroboratedTagRule:
    """Conclude a tagged pattern only when multiple insights support it."""

    name = "corroborated_tag"

    def apply(self, context: ReasoningContext) -> None:
        by_tag: dict[str, list[FinancialInsight]] = defaultdict(list)
        for insight in context.insights:
            for tag in insight.tags:
                by_tag[tag].append(insight)

        for tag, insights in by_tag.items():
            if len(insights) < 2:
                continue
            average_confidence = sum(item.confidence for item in insights) / len(insights)
            context.add_conclusion(FinancialConclusion(
                title=f"{tag.replace('_', ' ').title()} pattern is corroborated",
                summary=f"{len(insights)} independent insights point to a {tag.replace('_', ' ')} pattern.",
                supporting_insight_ids=tuple(item.id for item in insights),
                confidence=average_confidence,
                severity=max((item.severity for item in insights), key=self._severity_rank),
                evidence=tuple(item.summary for item in insights),
                tags=(tag,),
            ))

    @staticmethod
    def _severity_rank(value: str) -> int:
        return {"informational": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}.get(value, 0)
