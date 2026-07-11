COLUMN_ALIASES = {
    "date": [
        "date",
        "transaction date",
        "txn date",
        "value date",
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
        "deposit",
        "debit",
        "credit",
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
    return text.strip().lower()


def find_matching_column(columns, aliases):

    normalized = {
        normalize(column): column
        for column in columns
    }

    for alias in aliases:
        if alias in normalized:
            return normalized[alias]

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