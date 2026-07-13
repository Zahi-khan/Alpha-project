import re


COLUMN_ALIASES = {
    "date": [
        "date",
        "transaction date",
        "txn date",
        "value date",
        "value dt",
    ],

    "description": [
        "description",
        "details",
        "narration",
        "remarks",
        "name",
    ],

    "amount": [
        "amount",
        "transaction amount",
        "withdrawal",
        "withdrawal amount",
        "withdrawal amt",
        "deposit",
        "deposit amount",
        "deposit amt",
        "debit",
        "debit amount",
        "debit amt",
        "credit",
        "credit amount",
        "credit amt",
    ],

    "transaction_type": [
        "drcr",
        "type",
        "transaction type",
        "debit/credit",
    ],

    "balance": [
        "balance",
        "closing balance",
    ],

    "mode": [
        "mode",
        "payment mode",
    ]
}


def normalize(text: str) -> str:
    """Ignore bank-specific spaces and punctuation when matching headers."""
    return re.sub(r"[^a-z0-9]+", "", str(text).strip().lower())


def find_matching_column(columns, aliases):

    normalized = {
        normalize(column): column
        for column in columns
    }

    for alias in aliases:
        normalized_alias = normalize(alias)
        if normalized_alias in normalized:
            return normalized[normalized_alias]

    return None


def map_columns(columns):

    mapping = {}

    for field, aliases in COLUMN_ALIASES.items():

        match = find_matching_column(
            columns,
            aliases
        )

        if match:
            mapping[field] = match

    return mapping
