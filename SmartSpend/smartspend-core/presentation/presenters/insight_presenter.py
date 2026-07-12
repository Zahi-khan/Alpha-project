"""Present verified insights without inventing financial claims."""

from presentation.formatting.confidence_formatter import format_confidence
from presentation.formatting.percentage_formatter import format_percentage
from presentation.formatting.currency_formatter import format_currency
from presentation.models.views import InsightView
from presentation.semantics.icon_mapping import icon_for_insight_type
from presentation.semantics.severity_mapping import tone_for_severity


class InsightPresenter:
    def present(self, insight, context):
        primary = insight.supporting_metrics.get("percent_change")
        if primary is not None:
            primary_metric = ("+" if primary > 0 else "") + format_percentage(primary, context.display_precision)
        elif "savings_rate" in insight.supporting_metrics:
            primary_metric = format_percentage(insight.supporting_metrics["savings_rate"], context.display_precision)
        elif "projected_net" in insight.supporting_metrics:
            primary_metric = format_currency(insight.supporting_metrics["projected_net"], context.currency)
        elif "potential_savings" in insight.supporting_metrics:
            primary_metric = format_currency(insight.supporting_metrics["potential_savings"], context.currency)
        elif "average_monthly_cost" in insight.supporting_metrics:
            primary_metric = format_currency(insight.supporting_metrics["average_monthly_cost"], context.currency)
        else:
            primary_metric = None
        return InsightView(
            id=insight.id, type=insight.insight_type.value, title=insight.title, summary=self._summary(insight, context),
            primary_metric=primary_metric, severity=insight.severity, tone=tone_for_severity(insight.severity),
            confidence=insight.confidence, confidence_label=format_confidence(insight.confidence),
            evidence_preview=insight.supporting_evidence[:2], tags=insight.tags, generated_at=insight.generated_at,
            action={"label": "See why", "target": f"/presentation/explanations/{insight.id}", "icon_key": icon_for_insight_type(insight.insight_type.value)},
        )

    @staticmethod
    def _summary(insight, context):
        metrics = insight.supporting_metrics
        if insight.insight_type.value == "savings" and "category_expense" in metrics:
            return f"You spent {format_currency(metrics['category_expense'], context.currency)} here. Cutting it by 10% could free about {format_currency(metrics['potential_savings'], context.currency)} over a similar period."
        if insight.insight_type.value == "recurring" and "recurring_total" in metrics:
            months = metrics["months_observed"]
            return f"This expense appeared in {months} statement months. You spent {format_currency(metrics['recurring_total'], context.currency)} in total, or about {format_currency(metrics['average_monthly_cost'], context.currency)} each month."
        if insight.insight_type.value == "financial_health" and "savings" in metrics:
            return f"After income and expenses, {format_currency(metrics['savings'], context.currency)} remained. That is a {format_percentage(metrics['savings_rate'], context.display_precision)} savings rate."
        if insight.insight_type.value == "forecast" and "projected_net" in metrics:
            return f"Based on {metrics['months_observed']} statement months, your next month may end near {format_currency(metrics['projected_net'], context.currency)}. This is a projection, not a guarantee."
        return insight.summary
