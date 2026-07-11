"""Stable descriptions of financial containers that transactions affect."""

from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, Any

from models._dataclasses import slotted_dataclass

if TYPE_CHECKING:
    from models.bank import Bank


@slotted_dataclass
class Account:
    """A financial account's identity and characteristics, not its activity."""

    # Identity and ownership
    id: str | None = None
    display_name: str = ""
    owner_id: str | None = None

    # Banking information
    bank: Bank | None = None
    currency: str = "INR"
    country: str | None = None
    branch: str | None = None

    # Account characteristics and lifecycle
    account_type: str | None = None
    masked_identifier: str | None = None
    nickname: str | None = None
    status: str = "active"

    # Bank- and account-specific details, such as IFSC or IBAN.
    metadata: dict[str, Any] = field(default_factory=dict)
