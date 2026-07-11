"""Calculate factual goal progress from a goal, plan, and current savings."""

from __future__ import annotations

from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from models.financial_goal import FinancialGoal
from models.financial_plan import FinancialPlan
from models.goal_progress import GoalProgress


class PlanningEngine:
    """Evaluates whether a plan reaches its goal without recommending actions."""

    def evaluate(
        self,
        goal: FinancialGoal,
        plan: FinancialPlan,
        current_amount: Decimal,
        as_of: datetime,
    ) -> GoalProgress:
        if goal.id != plan.goal_id:
            raise ValueError("The plan must belong to the supplied goal.")
        remaining = max(Decimal("0"), goal.target_amount - current_amount)
        months = self._months_until(as_of, goal.target_date)
        required = remaining / months if months else remaining
        gap = required - plan.planned_monthly_contribution
        projected = self._project_completion(as_of, remaining, plan.planned_monthly_contribution)
        return GoalProgress(
            goal_id=goal.id,
            as_of=as_of,
            current_amount=current_amount,
            remaining_amount=remaining,
            progress_ratio=(current_amount / goal.target_amount if goal.target_amount else Decimal("1")),
            required_monthly_contribution=required,
            planned_monthly_contribution=plan.planned_monthly_contribution,
            monthly_gap=gap,
            on_track=gap <= 0,
            projected_completion=projected,
        )

    @staticmethod
    def _months_until(start: datetime, end: datetime) -> int:
        return max(0, (end.year - start.year) * 12 + end.month - start.month)

    @staticmethod
    def _project_completion(as_of: datetime, remaining: Decimal, monthly: Decimal) -> datetime | None:
        if monthly <= 0:
            return None
        months = int((remaining / monthly).to_integral_value(rounding="ROUND_CEILING"))
        year = as_of.year + (as_of.month - 1 + months) // 12
        month = (as_of.month - 1 + months) % 12 + 1
        return as_of.replace(year=year, month=month, day=min(as_of.day, monthrange(year, month)[1]))
