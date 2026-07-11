"""Flag grouped values that are unusually large relative to the group average."""

from decimal import Decimal

from analytics.core.analytics_context import AnalyticsContext
from analytics.core.insight import FinancialInsight
from analytics.core.insight_type import InsightType


class AnomalyAnalysis:
    name = "anomalies"

    def analyze(self, context: AnalyticsContext) -> None:
        rows = [row for row in context.query_result.rows if isinstance(row.values.get("sum"), Decimal)]
        if len(rows) < 3:
            return
        values = [abs(row.values["sum"]) for row in rows]
        average = sum(values, Decimal("0")) / len(values)
        outlier = max(rows, key=lambda row: abs(row.values["sum"]))
        if average == 0 or abs(outlier.values["sum"]) < average * 2:
            return
        context.add_insight(FinancialInsight(
            InsightType.ANOMALY,
            f"Unusually large value in {outlier.group}",
            f"{outlier.group} is at least twice the average grouped total.",
            severity="high",
            confidence=0.80,
            supporting_evidence=(f"Group total: {outlier.values['sum']}; average: {average}.",),
            supporting_metrics={"group_total": outlier.values['sum'], "average": average},
        ))
