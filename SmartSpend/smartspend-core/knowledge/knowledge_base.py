"""Single application-facing entry point for SmartSpend domain knowledge."""

from __future__ import annotations

from pathlib import Path

from knowledge.merchants.merchant_loader import JsonMerchantRepository
from knowledge.repositories import (
    BankRepository,
    MerchantRepository,
    PaymentRepository,
    TaxonomyRepository,
)
from knowledge.taxonomy.taxonomy_loader import JsonTaxonomyRepository
from models.category import Category
from models.industry import Industry
from models.merchant import Merchant


class KnowledgeBase:
    """Retrieves domain knowledge without exposing its storage implementation."""

    def __init__(
        self,
        merchants: MerchantRepository,
        taxonomy: TaxonomyRepository,
        banks: BankRepository | None = None,
        payments: PaymentRepository | None = None,
    ):
        self._merchants = merchants
        self._taxonomy = taxonomy
        self._banks = banks
        self._payments = payments

    @classmethod
    def from_json(cls, root: str | Path | None = None) -> KnowledgeBase:
        """Create the default JSON-backed knowledge base."""
        knowledge_root = Path(root) if root is not None else Path(__file__).parent
        taxonomy = JsonTaxonomyRepository(
            knowledge_root / "taxonomy" / "categories.json",
            knowledge_root / "taxonomy" / "industries.json",
        )
        merchants = JsonMerchantRepository(
            knowledge_root / "merchants" / "merchants.json",
            knowledge_root / "merchants" / "aliases.json",
            taxonomy,
        )
        return cls(merchants=merchants, taxonomy=taxonomy)

    def find_merchant(self, query: str) -> Merchant | None:
        return self._merchants.find(query)

    def find_category(self, category_id: str) -> Category | None:
        return self._taxonomy.find_category(category_id)

    def find_industry(self, industry_id: str) -> Industry | None:
        return self._taxonomy.find_industry(industry_id)

    def find_bank(self, query: str):
        return self._banks.find_bank(query) if self._banks is not None else None

    def find_payment_method(self, query: str):
        return (
            self._payments.find_payment_method(query)
            if self._payments is not None
            else None
        )
