"""Inputs and outputs shared by independent feature-domain capabilities."""

from __future__ import annotations

from dataclasses import field

from intelligence.core.insight import FinancialInsight
from models.financial_conclusion import FinancialConclusion
from models.financial_constraint import FinancialConstraint
from models.financial_goal import FinancialGoal
from models.financial_plan import FinancialPlan
from models.goal_progress import GoalProgress
from models.recommendation import Recommendation
from models._dataclasses import slotted_dataclass


@slotted_dataclass
class CapabilityContext:
    insights: tuple[FinancialInsight, ...] = ()
    conclusions: tuple[FinancialConclusion, ...] = ()
    goals: tuple[FinancialGoal, ...] = ()
    plans: tuple[FinancialPlan, ...] = ()
    constraints: tuple[FinancialConstraint, ...] = ()
    goal_progress: tuple[GoalProgress, ...] = ()
    recommendations: list[Recommendation] = field(default_factory=list)

    def add_recommendation(self, recommendation: Recommendation) -> None:
        self.recommendations.append(recommendation)
