"""Storage-independent contracts for SmartSpend knowledge repositories."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from models.category import Category
from models.industry import Industry
from models.merchant import Merchant

if TYPE_CHECKING:
    from models.bank import Bank
    from models.payment import Payment


class MerchantRepository(ABC):
    """Retrieves canonical merchants by identifier, name, or alias."""

    @abstractmethod
    def find(self, query: str) -> Merchant | None:
        """Return a merchant matching ``query``, or ``None`` when unknown."""


class TaxonomyRepository(ABC):
    """Retrieves category and industry knowledge without exposing storage."""

    @abstractmethod
    def find_category(self, category_id: str) -> Category | None:
        """Return the category identified by ``category_id``."""

    @abstractmethod
    def find_industry(self, industry_id: str) -> Industry | None:
        """Return the industry identified by ``industry_id``."""


class BankRepository(ABC):
    """Contract reserved for the future Bank knowledge model."""

    @abstractmethod
    def find_bank(self, query: str) -> Bank | None:
        """Return a bank matching ``query``, or ``None`` when unknown."""


class PaymentRepository(ABC):
    """Contract reserved for the future Payment knowledge model."""

    @abstractmethod
    def find_payment_method(self, query: str) -> Payment | None:
        """Return a payment method matching ``query``, or ``None`` when unknown."""
