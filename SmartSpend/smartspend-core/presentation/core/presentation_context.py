"""Non-financial settings used for consistent human-facing representation."""

from __future__ import annotations

from dataclasses import field
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class PresentationContext:
    currency: str = "INR"
    locale: str = "en-IN"
    timezone: str = "Asia/Kolkata"
    session_id: str | None = None
    reduced_motion: bool = False
    display_precision: int = 1
    account_mask: str | None = None
    options: dict[str, Any] = field(default_factory=dict)
