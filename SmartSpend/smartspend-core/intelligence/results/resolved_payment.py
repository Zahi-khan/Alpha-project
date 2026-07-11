"""Payment-detection output."""

from models._dataclasses import slotted_dataclass


@slotted_dataclass
class ResolvedPayment:
    family: str
    method: str
