"""Merchant-resolution output with provenance."""

from models._dataclasses import slotted_dataclass
from models.merchant import Merchant


@slotted_dataclass
class ResolvedMerchant:
    merchant: Merchant
    strategy: str
