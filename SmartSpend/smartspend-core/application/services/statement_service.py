"""Safe, idempotent CSV statement ingestion workflow."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pandas as pd

from application.dto.serializers import transaction_dto
from application.errors.processing_error import ProcessingError
from application.errors.validation_error import ValidationError
from intelligence.pipeline.pipeline import EnrichmentPipeline
from memory.memory_store import MemoryStore
from parsers.csv_parser import dataframe_to_transactions
from reasoning.explainability_graph import ExplainabilityGraph


class StatementService:
    """Coordinates parser → enrichment → memory without embedding engine logic."""

    def __init__(self, pipeline: EnrichmentPipeline, memory: MemoryStore, graph: ExplainabilityGraph):
        self._pipeline, self._memory, self._graph = pipeline, memory, graph
        self._imports: dict[str, dict] = {}
        self._fingerprints: set[str] = set()

    def preview_statement(self, file_bytes: bytes, filename: str) -> dict:
        transactions = self._parse_csv(file_bytes, filename)
        enriched = [self._pipeline.run(self._with_id(transaction)) for transaction in transactions]
        return {"source_filename": Path(filename).name, "total_rows": len(transactions), "data": [transaction_dto(item) for item in enriched]}

    def import_statement(self, file_bytes: bytes, filename: str) -> dict:
        started_at = datetime.utcnow()
        transactions = self._parse_csv(file_bytes, filename)
        accepted, duplicates, warnings, ids = 0, 0, [], []
        for transaction in transactions:
            transaction = self._with_id(transaction)
            fingerprint = self._fingerprint(transaction)
            if fingerprint in self._fingerprints:
                duplicates += 1
                continue
            enriched = self._pipeline.run(transaction)
            self._memory.process(enriched)
            self._graph.add_enriched_transaction(enriched)
            self._fingerprints.add(fingerprint)
            accepted += 1
            ids.append(enriched.transaction.id)
            warnings.extend(enriched.warnings)
        import_id = f"import_{uuid4().hex}"
        result = {
            "import_id": import_id, "source_filename": Path(filename).name, "detected_format": "csv",
            "detected_bank": None, "total_rows": len(transactions), "accepted_rows": accepted,
            "rejected_rows": 0, "duplicate_rows": duplicates, "enriched_transaction_ids": tuple(ids),
            "warnings": tuple(dict.fromkeys(warnings)), "errors": (), "started_at": started_at,
            "completed_at": datetime.utcnow(),
        }
        self._imports[import_id] = result
        return result

    def get_import_status(self, import_id: str) -> dict | None:
        return self._imports.get(import_id)

    @staticmethod
    def _parse_csv(file_bytes: bytes, filename: str):
        if not filename or not filename.lower().endswith(".csv"):
            raise ValidationError("Only CSV statement files are supported.")
        if not file_bytes:
            raise ValidationError("Statement file is empty.")
        try:
            return dataframe_to_transactions(pd.read_csv(BytesIO(file_bytes)))
        except ValueError as error:
            raise ValidationError(str(error)) from error
        except pd.errors.ParserError as error:
            raise ProcessingError("Unable to parse the CSV statement.") from error

    @staticmethod
    def _fingerprint(transaction) -> str:
        account_id = transaction.account.id if transaction.account else ""
        parts = (account_id, str(transaction.date), str(transaction.amount), transaction.description.casefold().strip())
        return sha256("|".join(parts).encode()).hexdigest()

    def _with_id(self, transaction):
        return replace(transaction, id=f"txn_{self._fingerprint(transaction)[:24]}")
