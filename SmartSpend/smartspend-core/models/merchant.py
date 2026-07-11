"""Passive, enduring knowledge about real-world businesses."""

from __future__ import annotations

from dataclasses import field
from typing import Any

from models._dataclasses import slotted_dataclass
from models.category import Category
from models.industry import Industry


@slotted_dataclass
class Merchant:
    """Canonical knowledge record for a merchant, independent of transactions."""

    # Identity
    id: str | None = None
    canonical_name: str = ""

    # Names used by banks, payment networks, and customers.
    aliases: list[str] = field(default_factory=list)

    # Classification
    industry: Industry | None = None
    category: Category | None = None
    merchant_type: str | None = None

    # Behavioural properties of the business itself.
    accepts_recurring: bool = False
    supports_refunds: bool = False
    is_government: bool = False
    is_financial_institution: bool = False
    is_subscription_service: bool = False
    essential_service: bool = False

    # Geography
    country: str | None = None
    region: str | None = None

    # Source-specific or future enrichment, such as website or GST number.
    metadata: dict[str, Any] = field(default_factory=dict)
