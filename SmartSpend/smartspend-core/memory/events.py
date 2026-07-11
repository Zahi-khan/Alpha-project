"""Domain events emitted when an enriched transaction enters memory."""

from memory.enriched_transaction import EnrichedTransaction
from models._dataclasses import slotted_dataclass


@slotted_dataclass(frozen=True)
class TransactionProcessed:
    enriched_transaction: EnrichedTransaction
