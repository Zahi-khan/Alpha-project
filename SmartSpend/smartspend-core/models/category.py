"""Timeless financial-taxonomy knowledge used to classify merchants."""

from __future__ import annotations

from dataclasses import field
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass
class Category:
    """A node in SmartSpend's financial taxonomy, independent of user activity."""

    # Identity
    id: str = ""
    name: str = ""
    description: str | None = None

    # Position in the taxonomy
    parent: Category | None = None
    children: list[Category] = field(default_factory=list)

    # Classification metadata
    is_essential: bool = False
    budget_priority: str | None = None

    # Search and semantic relationships
    keywords: list[str] = field(default_factory=list)
    related_categories: list[Category] = field(default_factory=list)

    # Future enrichment such as tax treatment or localization rules.
    metadata: dict[str, Any] = field(default_factory=dict)
