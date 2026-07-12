"""Resolve category from merchant knowledge, never from merchant aliases."""

from intelligence.evidence.evidence import Evidence
from intelligence.evidence.evidence_types import EvidenceType
from intelligence.pipeline.context import EnrichmentContext
from intelligence.pipeline.stage import EnrichmentStage
from models.category import Category


class CategoryResolutionStage(EnrichmentStage):
    _FALLBACK_CATEGORIES = (
        ("Shopping", ("MYNTRA", "MEESHO", "AMAZON", "FLIPKART", "MARKET 99", "RELIANCE DIGITAL", "CROMA")),
        ("Food", ("SWIGGY", "ZOMATO", "PABBAS", "CAFE", "RESTAURANT", "FIZA")),
        ("Fuel", ("PETROL", "FUEL")),
        ("Mobile and utilities", ("JIO", "AIRTEL", "ELECTRICITY", "WATER BILL", "GAS")),
        ("Investment", ("MUTUAL FUND", "WEALTH MANAGEMENT", "SIP")),
        ("Subscription", ("NETFLIX", "SPOTIFY", "GOOGLE ONE", "CHATGPT")),
    )

    def enrich(self, context: EnrichmentContext) -> EnrichmentContext:
        if context.metadata.get("merchant_visibility") == "not_visible":
            return context
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
        if merchant is not None and merchant.category is not None:
            context.resolved_category = merchant.category
            context.add_evidence(
                Evidence(
                    EvidenceType.CATEGORY_LINK,
                    f'Merchant "{merchant.canonical_name}" links to "{merchant.category.name}".',
                    source="merchant_knowledge",
                )
            )
            return context
        raw = f"{context.transaction.description} {context.transaction.metadata.get('description', '')}".upper()
        for name, keywords in self._FALLBACK_CATEGORIES:
            if any(keyword in raw for keyword in keywords):
                context.resolved_category = Category(
                    id=f"inferred_category:{_identifier(name)}",
                    name=name,
                    metadata={"source": "keyword_fallback"},
                )
                context.add_evidence(
                    Evidence(
                        EvidenceType.CATEGORY_LINK,
                        f'Keywords in the statement indicate "{name}".',
                        source="keyword_fallback",
                        score=0.65,
                    )
                )
                return context
        return context


def _identifier(value: str) -> str:
    return "-".join("".join(character if character.isalnum() else " " for character in value.casefold()).split())
