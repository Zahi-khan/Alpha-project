from models.transaction import Transaction

from preprocessing.enrichment import (
    DescriptionNormalizationStage,
    EnrichmentPipeline,
    MerchantCandidateStage,
)
from preprocessing.validator import (
    validate_transaction,
)
from preprocessing.deduplicator import (
    remove_duplicates,
)


def clean_transactions(
    transactions: list[Transaction]
):

    cleaned = []
    pipeline = EnrichmentPipeline(
        [DescriptionNormalizationStage(), MerchantCandidateStage()]
    )

    for transaction in transactions:
        if validate_transaction(transaction):
            cleaned.append(pipeline.run_context(transaction).to_transaction())

    return remove_duplicates(cleaned)
