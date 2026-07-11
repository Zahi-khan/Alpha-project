"""Safe DTO conversion that excludes unnecessary internal object structure."""

from __future__ import annotations

from decimal import Decimal

from intelligence.core.insight import FinancialInsight
from memory.enriched_transaction import EnrichedTransaction
from models.financial_conclusion import FinancialConclusion
from models.financial_goal import FinancialGoal
from models.financial_plan import FinancialPlan
from models.goal_progress import GoalProgress
from models.recommendation import Recommendation


def transaction_dto(item: EnrichedTransaction) -> dict:
    transaction = item.transaction
    return {
        "id": transaction.id,
        "date": transaction.date,
        "description": transaction.description,
        "cleaned_description": transaction.cleaned_description,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "account_id": transaction.account.id if transaction.account else None,
        "merchant": item.merchant.canonical_name if item.merchant else None,
        "category": item.category.name if item.category else None,
        "industry": item.industry.name if item.industry else None,
        "payment_method": item.payment.method if item.payment else transaction.payment_method,
        "transaction_type": item.transaction_type,
        "confidence": item.confidence,
        "warnings": item.warnings,
    }


def insight_dto(item: FinancialInsight) -> dict:
    return {
        "id": item.id, "type": item.insight_type.value, "title": item.title,
        "summary": item.summary, "severity": item.severity, "confidence": item.confidence,
        "metrics": item.supporting_metrics, "tags": item.tags,
        "generated_at": item.generated_at, "explanation_available": True,
    }


def conclusion_dto(item: FinancialConclusion) -> dict:
    return {
        "id": item.id, "title": item.title, "summary": item.summary,
        "confidence": item.confidence, "severity": item.severity,
        "supporting_insight_ids": item.supporting_insight_ids, "tags": item.tags,
        "generated_at": item.generated_at,
    }


def goal_dto(item: FinancialGoal) -> dict:
    return {
        "id": item.id, "name": item.name, "target_amount": item.target_amount,
        "target_date": item.target_date, "currency": item.currency, "priority": item.priority,
        "category_id": item.category_id,
    }


def plan_dto(item: FinancialPlan) -> dict:
    return {"id": item.id, "goal_id": item.goal_id, "planned_monthly_contribution": item.planned_monthly_contribution}


def progress_dto(item: GoalProgress) -> dict:
    return {
        "goal_id": item.goal_id, "as_of": item.as_of, "current_amount": item.current_amount,
        "remaining_amount": item.remaining_amount, "progress_ratio": item.progress_ratio,
        "required_monthly_contribution": item.required_monthly_contribution,
        "planned_monthly_contribution": item.planned_monthly_contribution,
        "monthly_gap": item.monthly_gap, "on_track": item.on_track,
        "projected_completion": item.projected_completion,
    }


def recommendation_dto(item: Recommendation) -> dict:
    return {
        "id": item.id, "title": item.title, "summary": item.summary,
        "priority": item.priority, "confidence": item.confidence,
        "expected_impact": item.expected_impact, "goal_alignment": item.goal_alignment,
        "reasoning_path": item.reasoning_path, "suggested_actions": item.suggested_actions,
    }
