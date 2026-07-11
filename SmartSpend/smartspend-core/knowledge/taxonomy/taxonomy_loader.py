"""JSON-backed repository for category and industry knowledge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from knowledge.repositories import TaxonomyRepository
from models.category import Category
from models.industry import Industry


def _load_records(path: Path) -> dict[str, dict[str, Any]]:
    """Load an object keyed by stable IDs from a JSON knowledge file."""
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid knowledge JSON: {path}") from error

    if not isinstance(data, dict):
        raise ValueError(f"Knowledge JSON must contain an object: {path}")

    records: dict[str, dict[str, Any]] = {}
    for identifier, value in data.items():
        if not isinstance(identifier, str) or not isinstance(value, dict):
            raise ValueError(f"Knowledge records must be string-keyed objects: {path}")
        records[identifier] = value
    return records


class JsonTaxonomyRepository(TaxonomyRepository):
    """Builds navigable category and industry trees from JSON records."""

    def __init__(self, categories_path: str | Path, industries_path: str | Path):
        self._category_records = _load_records(Path(categories_path))
        self._industry_records = _load_records(Path(industries_path))
        self._categories: dict[str, Category] = {}
        self._industries: dict[str, Industry] = {}
        self._build_categories()
        self._build_industries()

    def find_category(self, category_id: str) -> Category | None:
        return self._categories.get(category_id)

    def find_industry(self, industry_id: str) -> Industry | None:
        return self._industries.get(industry_id)

    def _build_categories(self) -> None:
        for identifier, record in self._category_records.items():
            self._categories[identifier] = Category(
                id=identifier,
                name=str(record.get("name", identifier)),
                description=record.get("description"),
                is_essential=bool(record.get("is_essential", False)),
                budget_priority=record.get("budget_priority"),
                keywords=list(record.get("keywords", [])),
                metadata=dict(record.get("metadata", {})),
            )

        for identifier, record in self._category_records.items():
            category = self._categories[identifier]
            parent_id = record.get("parent")
            if isinstance(parent_id, str) and parent_id in self._categories:
                parent = self._categories[parent_id]
                category.parent = parent
                if category not in parent.children:
                    parent.children.append(category)

            for related_id in record.get("related_categories", []):
                related = self._categories.get(related_id)
                if related is not None and related not in category.related_categories:
                    category.related_categories.append(related)

    def _build_industries(self) -> None:
        for identifier, record in self._industry_records.items():
            self._industries[identifier] = Industry(
                id=identifier,
                name=str(record.get("name", identifier)),
                description=record.get("description"),
                aliases=list(record.get("aliases", [])),
                metadata=dict(record.get("metadata", {})),
            )

        for identifier, record in self._industry_records.items():
            industry = self._industries[identifier]
            parent_id = record.get("parent")
            if isinstance(parent_id, str) and parent_id in self._industries:
                parent = self._industries[parent_id]
                industry.parent = parent
                if industry not in parent.children:
                    parent.children.append(industry)
