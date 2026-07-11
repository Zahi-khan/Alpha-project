"""Present verified insights without inventing financial claims."""

from presentation.formatting.confidence_formatter import format_confidence
from presentation.formatting.percentage_formatter import format_percentage
from presentation.models.views import InsightView
from presentation.semantics.icon_mapping import icon_for_insight_type
from presentation.semantics.severity_mapping import tone_for_severity


class InsightPresenter:
    def present(self, insight, context):
        primary = insight.supporting_metrics.get("percent_change")
        primary_metric = ("+" if primary and primary > 0 else "") + format_percentage(primary, context.display_precision) if primary is not None else None
        return InsightView(
            id=insight.id, type=insight.insight_type.value, title=insight.title, summary=insight.summary,
            primary_metric=primary_metric, severity=insight.severity, tone=tone_for_severity(insight.severity),
            confidence=insight.confidence, confidence_label=format_confidence(insight.confidence),
            evidence_preview=insight.supporting_evidence[:2], tags=insight.tags, generated_at=insight.generated_at,
            action={"label": "See why", "target": f"/presentation/explanations/{insight.id}", "icon_key": icon_for_insight_type(insight.insight_type.value)},
        )
