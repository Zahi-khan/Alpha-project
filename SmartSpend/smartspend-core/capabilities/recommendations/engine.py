"""Produce traceable recommendations without recalculating financial facts."""

from __future__ import annotations

from capabilities.context import CapabilityContext
from models.recommendation import Recommendation


class RecommendationCapability:
    """Aligns relevant conclusions with off-track user financial goals."""

    name = "recommendations"
    required_inputs = ("conclusions", "goals", "plans", "goal_progress", "constraints")
    produced_outputs = ("recommendations",)

    def execute(self, context: CapabilityContext) -> None:
        goals = {goal.id: goal for goal in context.goals}
        for progress in context.goal_progress:
            if progress.on_track or progress.monthly_gap <= 0:
                continue
            goal = goals.get(progress.goal_id)
            if goal is None:
                continue
            for conclusion in context.conclusions:
                if not self._is_relevant(conclusion.tags, goal.category_id):
                    continue
                context.add_recommendation(Recommendation(
                    title=f"Protect progress toward {goal.name}",
                    summary=(
                        f"{conclusion.summary} Closing a monthly gap of "
                        f"{progress.monthly_gap} would keep this goal on track."
                    ),
                    supporting_conclusion_ids=(conclusion.id,),
                    priority="high" if goal.priority == "high" else "normal",
                    confidence=min(float(conclusion.confidence), 0.95),
                    expected_impact={"monthly_gap": progress.monthly_gap, "goal_id": goal.id},
                    goal_alignment={"goal_id": goal.id, "on_track": False},
                    evidence=conclusion.evidence,
                    reasoning_path=(conclusion.id, *conclusion.supporting_insight_ids),
                    suggested_actions=(
                        f"Increase monthly goal contributions by {progress.monthly_gap}.",
                    ),
                    metadata={"capability": self.name},
                ))

    @staticmethod
    def _is_relevant(tags: tuple[str, ...], category_id: str | None) -> bool:
        return category_id is None or category_id in tags
