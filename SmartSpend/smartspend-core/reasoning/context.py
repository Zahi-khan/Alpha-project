"""Shared workspace for conclusion-building rules."""

from __future__ import annotations

from dataclasses import field

from intelligence.core.insight import FinancialInsight
from models._dataclasses import slotted_dataclass
from models.financial_conclusion import FinancialConclusion


@slotted_dataclass
class ReasoningContext:
    insights: tuple[FinancialInsight, ...]
    conclusions: list[FinancialConclusion] = field(default_factory=list)

    def add_conclusion(self, conclusion: FinancialConclusion) -> None:
        self.conclusions.append(conclusion)
