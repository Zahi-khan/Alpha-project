"""End-to-end anonymous statement analysis workflow."""

from __future__ import annotations

from application.dto.serializers import transaction_dto
from decimal import Decimal
from application.sessions.session_status import SessionStatus
from query.builder import FinancialQueryBuilder
from query.grouping.category import CategoryGrouping
from query.grouping.merchant import MerchantGrouping
from query.grouping.month import MonthGrouping
from query.grouping.transaction_type import TransactionTypeGrouping
from query.grouping.merchant_month_category import MerchantMonthCategoryGrouping
from query.filters.amount_filter import AmountFilter
from query.metrics.count import CountMetric
from query.metrics.sum import SumMetric


class AnalyzeStatementWorkflow:
    def analyze(
        self,
        session,
        file_bytes: bytes | None = None,
        filename: str | None = None,
        preview_id: str | None = None,
    ) -> dict:
        session.status = SessionStatus.PROCESSING
        try:
            if preview_id:
                imported = session.container.statement_service.import_preview(preview_id)
            elif file_bytes is not None and filename is not None:
                imported = session.container.statement_service.import_statement(file_bytes, filename)
            else:
                raise ValueError("A statement file or preview is required.")
            queries = (
                FinancialQueryBuilder().metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().group(MonthGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().where(AmountFilter(maximum=Decimal("-0.01"))).group(CategoryGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().where(AmountFilter(maximum=Decimal("-0.01"))).group(MerchantGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().group(TransactionTypeGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
                FinancialQueryBuilder().where(AmountFilter(maximum=Decimal("-0.01"))).group(MerchantMonthCategoryGrouping()).metric(SumMetric()).metric(CountMetric()).build(),
            )
            query_results = [session.container.query_service.execute(query) for query in queries]
            insights = [
                insight
                for query, query_result in zip(queries, query_results)
                for insight in session.container.insight_service.generate(query, query_result)
            ]
            insight_objects = session.container.insight_service.objects()
            conclusions = session.container.reasoning_service.generate(insight_objects)
            session.analysis_result = {
                "import": imported,
                "transaction_count": imported["accepted_rows"],
                "query": {
                    "summary": dict(query_results[0].summary), "query_id": queries[0].id,
                    "warnings": query_results[0].warnings,
                },
                "insights": insights,
                "conclusions": conclusions,
            }
            session.warnings.extend(imported["warnings"])
            session.status = SessionStatus.ANALYZED
            return session.analysis_result
        except Exception as error:
            session.status = SessionStatus.FAILED
            session.error = "Analysis could not be completed."
            raise
