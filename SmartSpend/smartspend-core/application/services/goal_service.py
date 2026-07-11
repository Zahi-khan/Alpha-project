"""In-memory application lifecycle for user-defined financial goals."""

from application.dto.serializers import goal_dto
from application.errors.not_found_error import NotFoundError
from application.errors.validation_error import ValidationError
from models.financial_goal import FinancialGoal


class GoalService:
    def __init__(self): self._goals: dict[str, FinancialGoal] = {}

    def create(self, goal: FinancialGoal) -> dict:
        if goal.target_amount <= 0:
            raise ValidationError("Goal target amount must be positive.")
        self._goals[goal.id] = goal
        return goal_dto(goal)

    def get(self, goal_id: str) -> FinancialGoal:
        goal = self._goals.get(goal_id)
        if goal is None: raise NotFoundError("Goal not found.")
        return goal

    def list(self) -> list[dict]: return [goal_dto(goal) for goal in self._goals.values()]
