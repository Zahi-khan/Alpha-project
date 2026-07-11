"""JSON-backed repository for canonical merchant knowledge and aliases."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge.repositories import MerchantRepository, TaxonomyRepository
from knowledge.taxonomy.taxonomy_loader import _load_records
from models.merchant import Merchant


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def _load_aliases(path: Path) -> dict[str, list[str]]:
    """Load either canonical-to-list or structured merchant alias records."""
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid alias JSON: {path}") from error

    if not isinstance(data, dict):
        raise ValueError(f"Alias JSON must contain an object: {path}")

    aliases: dict[str, list[str]] = {}
    for canonical_id, value in data.items():
        if isinstance(value, list):
            aliases[canonical_id] = [str(alias) for alias in value]
        elif isinstance(value, dict):
            values = value.get("aliases", [])
            if not isinstance(values, list):
                raise ValueError(f"Aliases must be a list: {path}")
            aliases[canonical_id] = [str(alias) for alias in values]
        elif isinstance(value, str):
            aliases.setdefault(value, []).append(canonical_id)
        else:
            raise ValueError(f"Alias records must be lists, objects, or strings: {path}")
    return aliases


class JsonMerchantRepository(MerchantRepository):
    """Resolves merchant IDs, names, and aliases to canonical Merchant objects."""

    def __init__(
        self,
        merchants_path: str | Path,
        aliases_path: str | Path,
        taxonomy: TaxonomyRepository,
    ):
        self._records = _load_records(Path(merchants_path))
        self._aliases = _load_aliases(Path(aliases_path))
        self._taxonomy = taxonomy
        self._merchants: dict[str, Merchant] = {}
        self._index: dict[str, str] = {}
        self._build_merchants()

    def find(self, query: str) -> Merchant | None:
        merchant_id = self._index.get(_normalize(query))
        if merchant_id is None:
            return None
        return self._merchants[merchant_id]

    def _build_merchants(self) -> None:
        for identifier, record in self._records.items():
            aliases = list(record.get("aliases", []))
            aliases.extend(self._aliases.get(identifier, []))
            merchant = Merchant(
                id=identifier,
                canonical_name=str(record.get("canonical_name", record.get("name", identifier))),
                aliases=list(dict.fromkeys(aliases)),
                category=self._taxonomy.find_category(record["category"])
                if isinstance(record.get("category"), str)
                else None,
                industry=self._taxonomy.find_industry(record["industry"])
                if isinstance(record.get("industry"), str)
                else None,
                merchant_type=record.get("merchant_type"),
                accepts_recurring=bool(record.get("accepts_recurring", False)),
                supports_refunds=bool(record.get("supports_refunds", False)),
                is_government=bool(record.get("is_government", False)),
                is_financial_institution=bool(record.get("is_financial_institution", False)),
                is_subscription_service=bool(record.get("is_subscription_service", False)),
                essential_service=bool(record.get("essential_service", False)),
                country=record.get("country"),
                region=record.get("region"),
                metadata=dict(record.get("metadata", {})),
            )
            self._merchants[identifier] = merchant
            for name in [identifier, merchant.canonical_name, *merchant.aliases]:
                self._index[_normalize(name)] = identifier
