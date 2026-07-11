"""Application planning use cases built on goal and planning services."""

from datetime import datetime
from decimal import Decimal

from application.dto.serializers import plan_dto, progress_dto
from application.errors.not_found_error import NotFoundError
from models.financial_plan import FinancialPlan
from planning.planning_engine import PlanningEngine


class PlanningService:
    def __init__(self, goals, engine: PlanningEngine):
        self._goals, self._engine = goals, engine
        self._plans: dict[str, FinancialPlan] = {}
        self._progress: dict[str, object] = {}

    def create_plan(self, plan: FinancialPlan) -> dict:
        self._goals.get(plan.goal_id)
        self._plans[plan.id] = plan
        return plan_dto(plan)

    def evaluate(self, plan_id: str, current_amount: Decimal, as_of: datetime) -> dict:
        plan = self._plans.get(plan_id)
        if plan is None: raise NotFoundError("Plan not found.")
        progress = self._engine.evaluate(self._goals.get(plan.goal_id), plan, current_amount, as_of)
        self._progress[plan.goal_id] = progress
        return progress_dto(progress)

    def get_progress(self, goal_id: str) -> dict:
        progress = self._progress.get(goal_id)
        if progress is None: raise NotFoundError("Goal progress not found.")
        return progress_dto(progress)
