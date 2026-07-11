"""Category-resolution output with provenance."""

from models._dataclasses import slotted_dataclass
from models.category import Category


@slotted_dataclass
class ResolvedCategory:
    category: Category
    source: str
