"""Industry-resolution output with provenance."""

from models._dataclasses import slotted_dataclass
from models.industry import Industry


@slotted_dataclass
class ResolvedIndustry:
    industry: Industry
    source: str
