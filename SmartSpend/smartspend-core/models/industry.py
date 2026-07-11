"""Business-sector knowledge kept independent from the spending taxonomy."""

from __future__ import annotations

from dataclasses import field
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass
class Industry:
    """A stable business-sector node that can be shared by many merchants."""

    # Identity
    id: str = ""
    name: str = ""
    description: str | None = None

    # Alternate sector names used by external data sources or matching engines.
    aliases: list[str] = field(default_factory=list)

    # Industry-sector hierarchy, independent of the Category taxonomy.
    parent: Industry | None = None
    children: list[Industry] = field(default_factory=list)

    # Future enrichment such as standard industry codes or regional mappings.
    metadata: dict[str, Any] = field(default_factory=dict)
