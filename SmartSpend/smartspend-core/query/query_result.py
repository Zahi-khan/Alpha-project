"""Immutable output returned by the financial query engine."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import field
from typing import Any

from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class QueryRow:
    group: str | None
    values: Mapping[str, Any]


@slotted_dataclass(frozen=True)
class QueryResult:
    rows: tuple[QueryRow, ...]
    summary: Mapping[str, Any]
    execution_time_ms: float
    metadata: Mapping[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()
    query_id: str | None = None
