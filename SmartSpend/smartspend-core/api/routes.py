"""Thin HTTP adapters over application services; no core orchestration lives here."""

from datetime import datetime
from decimal import Decimal
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.dependencies import get_container
from application.errors.application_error import ApplicationError
from application.errors.validation_error import ValidationError
from models.financial_goal import FinancialGoal
from models.financial_plan import FinancialPlan
from query.builder import FinancialQueryBuilder
from query.filters.category_filter import CategoryFilter
from query.filters.confidence_filter import ConfidenceFilter
from query.filters.date_filter import DateFilter
from query.grouping.month import MonthGrouping
from query.grouping.category import CategoryGrouping
from query.metrics.average import AverageMetric
from query.metrics.count import CountMetric
from query.metrics.sum import SumMetric

router = APIRouter()
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


def _application_error(error: ApplicationError):
    raise HTTPException(status_code=error.status_code, detail={"code": error.code, "message": str(error)})


@router.post("/statements/preview")
async def preview_statement(file: UploadFile = File(...), container=Depends(get_container)):
    return await _statement_operation(container.statement_service.preview_statement, file)


@router.post("/statements/import")
async def import_statement(file: UploadFile = File(...), container=Depends(get_container)):
    return await _statement_operation(container.statement_service.import_statement, file)


@router.get("/statements/{import_id}")
def get_import(import_id: str, container=Depends(get_container)):
    result = container.statement_service.get_import_status(import_id)
    if result is None: raise HTTPException(status_code=404, detail="Import not found.")
    return result


@router.get("/transactions")
def list_transactions(container=Depends(get_container)):
    return {"data": container.transaction_service.list_transactions()}


@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str, container=Depends(get_container)):
    try: return container.transaction_service.get_transaction(transaction_id)
    except ApplicationError as error: _application_error(error)


@router.get("/transactions/{transaction_id}/evidence")
def get_transaction_evidence(transaction_id: str, container=Depends(get_container)):
    try: return {"data": container.transaction_service.get_transaction_evidence(transaction_id)}
    except ApplicationError as error: _application_error(error)


@router.post("/financial-queries")
def execute_query(payload: dict, container=Depends(get_container)):
    try:
        query = _build_query(payload)
        result = container.query_service.execute(query)
        return _query_result_dto(result)
    except (ApplicationError, ValueError) as error: _application_error(ValidationError(str(error)))


@router.post("/insights/generate")
def generate_insights(payload: dict, container=Depends(get_container)):
    try:
        query = _build_query(payload)
        result = container.query_service.execute(query)
        return {"data": container.insight_service.generate(query, result), "query_id": query.id}
    except (ApplicationError, ValueError) as error: _application_error(ValidationError(str(error)))


@router.get("/insights")
def list_insights(container=Depends(get_container)):
    return {"data": container.insight_service.list()}


@router.post("/goals")
def create_goal(payload: dict, container=Depends(get_container)):
    try:
        goal = FinancialGoal(
            name=payload["name"], target_amount=Decimal(str(payload["target_amount"])),
            target_date=datetime.fromisoformat(payload["target_date"]), currency=payload.get("currency", "INR"),
            priority=payload.get("priority", "normal"), category_id=payload.get("category_id"),
        )
        return container.goal_service.create(goal)
    except (ApplicationError, KeyError, ValueError) as error: _application_error(ValidationError(str(error)))


@router.get("/goals")
def list_goals(container=Depends(get_container)):
    return {"data": container.goal_service.list()}


@router.post("/plans")
def create_plan(payload: dict, container=Depends(get_container)):
    try:
        plan = FinancialPlan(payload["goal_id"], Decimal(str(payload["planned_monthly_contribution"])))
        return container.planning_service.create_plan(plan)
    except (ApplicationError, KeyError, ValueError) as error: _application_error(ValidationError(str(error)))


@router.post("/plans/{plan_id}/evaluate")
def evaluate_plan(plan_id: str, payload: dict, container=Depends(get_container)):
    try:
        return container.planning_service.evaluate(plan_id, Decimal(str(payload["current_amount"])), datetime.fromisoformat(payload["as_of"]))
    except (ApplicationError, KeyError, ValueError) as error: _application_error(ValidationError(str(error)))


@router.get("/explanations/{root_id}")
def trace_explanation(root_id: str, container=Depends(get_container)):
    try: return container.explainability_service.trace(root_id)
    except ApplicationError as error: _application_error(error)


@router.post("/upload")
async def legacy_upload(file: UploadFile = File(...), container=Depends(get_container)):
    return await _statement_operation(container.statement_service.import_statement, file)


async def _read_upload(file: UploadFile) -> tuple[bytes, str]:
    filename = Path(file.filename or "").name
    if not filename.lower().endswith(".csv"): raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if not content: raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES: raise HTTPException(status_code=413, detail="Uploaded file exceeds the 10 MB limit.")
    return content, filename


async def _statement_operation(operation, file: UploadFile):
    content, filename = await _read_upload(file)
    try:
        return operation(content, filename)
    except ApplicationError as error:
        _application_error(error)


def _build_query(payload: dict):
    builder = FinancialQueryBuilder()
    if category_id := payload.get("category_id"): builder.where(CategoryFilter(category_id))
    if minimum_confidence := payload.get("minimum_confidence"): builder.where(ConfidenceFilter(float(minimum_confidence)))
    if payload.get("start") or payload.get("end"):
        builder.where(DateFilter(datetime.fromisoformat(payload["start"]) if payload.get("start") else None, datetime.fromisoformat(payload["end"]) if payload.get("end") else None))
    if payload.get("group_by") == "month": builder.group(MonthGrouping())
    elif payload.get("group_by") == "category": builder.group(CategoryGrouping())
    elif payload.get("group_by"): raise ValueError("Unsupported grouping.")
    metric_map = {"sum": SumMetric, "count": CountMetric, "average": AverageMetric}
    for name in payload.get("metrics", ["sum"]):
        if name not in metric_map: raise ValueError(f"Unsupported metric: {name}")
        builder.metric(metric_map[name]())
    if payload.get("limit"): builder.take(int(payload["limit"]))
    return builder.build()


def _query_result_dto(result):
    return {"rows": [{"group": row.group, "values": dict(row.values)} for row in result.rows], "summary": dict(result.summary), "execution_time_ms": result.execution_time_ms, "metadata": dict(result.metadata), "warnings": result.warnings, "query_id": result.query_id}
