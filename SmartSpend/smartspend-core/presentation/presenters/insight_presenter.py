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
        else:
            primary_metric = None
        return InsightView(
            id=insight.id, type=insight.insight_type.value, title=insight.title, summary=insight.summary,
            primary_metric=primary_metric, severity=insight.severity, tone=tone_for_severity(insight.severity),
            confidence=insight.confidence, confidence_label=format_confidence(insight.confidence),
            evidence_preview=insight.supporting_evidence[:2], tags=insight.tags, generated_at=insight.generated_at,
            action={"label": "See why", "target": f"/presentation/explanations/{insight.id}", "icon_key": icon_for_insight_type(insight.insight_type.value)},
        )
