"""Application-facing retrieval of immutable enriched transactions."""

from application.dto.serializers import transaction_dto
from application.errors.not_found_error import NotFoundError
from memory.memory_store import MemoryStore
from query.engine.query_engine import QueryEngine


class TransactionService:
    def __init__(self, memory: MemoryStore, query_engine: QueryEngine):
        self._memory, self._query_engine = memory, query_engine

    def list_transactions(self) -> list[dict]:
        return [transaction_dto(item) for item in self._memory.transactions]

    def get_transaction(self, transaction_id: str) -> dict:
        for item in self._memory.transactions:
            if item.transaction.id == transaction_id:
                return transaction_dto(item)
        raise NotFoundError("Transaction not found.")

    def get_transaction_evidence(self, transaction_id: str) -> list[dict]:
        for item in self._memory.transactions:
            if item.transaction.id == transaction_id:
                return [evidence.to_dict() for evidence in item.evidence]
        raise NotFoundError("Transaction not found.")
