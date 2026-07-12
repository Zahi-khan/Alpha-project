"""Resolve category from merchant knowledge, never from merchant aliases."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage
from models.category import Category


class CategoryResolutionStage(EnrichmentStage):
    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        supplied_category = str(context.transaction.metadata.get("category", "")).strip()
        if supplied_category:
            context.resolved_category = Category(
                id=f"source_category:{_identifier(supplied_category)}",
                name=supplied_category,
                metadata={"source": "statement_category"},
            )
            context.add_evidence(
                Evidence(
                    EvidenceType.CATEGORY_LINK,
                    f'Statement category "{supplied_category}" was used for classification.',
                    source="statement_category",
                    score=0.90,
                )
            )
            return context
        merchant = context.resolved_merchant
        if merchant is None or merchant.category is None:
            return context
        context.resolved_category = merchant.category
        context.add_evidence(
            Evidence(
                EvidenceType.CATEGORY_LINK,
                f'Merchant "{merchant.canonical_name}" links to "{merchant.category.name}".',
                source="merchant_knowledge",
            )
        )
        return context


def _identifier(value: str) -> str:
    return "-".join("".join(character if character.isalnum() else " " for character in value.casefold()).split())
