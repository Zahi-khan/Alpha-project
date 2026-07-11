"""Canonical transaction model shared by every SmartSpend pipeline stage."""

from __future__ import annotations

from dataclasses import field
from datetime import datetime
from decimal import Decimal
from typing import Any

from models._dataclasses import slotted_dataclass
from models.account import Account
from models.merchant import Merchant


@slotted_dataclass
class Transaction:
    """A transaction enriched in place as it moves through the pipeline."""

    # Identity
    id: str | None = None

    # Source
    account: Account | None = None

    # Raw data
    date: datetime | None = None
    description: str = ""
    amount: Decimal = Decimal("0.00")
    currency: str = "INR"

    # Cleaned data
    cleaned_description: str | None = None

    # Knowledge
    merchant: Merchant | None = None

    # Classification
    transaction_type: str | None = None
    payment_method: str | None = None

    # Analytics
    is_recurring: bool = False
    is_essential: bool = False

    # Confidence
    confidence: float = 0.0

    # Bank- or source-specific fields that do not belong in the core schema.
    metadata: dict[str, Any] = field(default_factory=dict)
