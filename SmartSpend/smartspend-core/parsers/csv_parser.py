from __future__ import annotations

from io import BytesIO
from decimal import Decimal, InvalidOperation
from preprocessing.cleaner import clean_transactions


import pandas as pd

from models.transaction import Transaction
from parsers.column_mapper import map_columns

REQUIRED_COLUMNS = {
    "date",
    "description",
    "amount"
}


def dataframe_to_transactions(df: pd.DataFrame):
    df = _canonicalize_columns(df)

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    transactions = []

    for _, row in df.iterrows():

        if pd.isna(row["date"]) or pd.isna(row["description"]) or pd.isna(row["amount"]):
            continue

        # Convert through text to avoid binary floating-point currency errors.
        try:
            amount = _parse_amount(row["amount"])
        except (InvalidOperation, ValueError):
            continue
        try:
            transaction_date = pd.to_datetime(row["date"], errors="raise").to_pydatetime()
        except (TypeError, ValueError):
            continue

        transaction = Transaction(
            date=transaction_date,
            description=str(row["description"]).strip(),
            amount=amount,
            transaction_type="income" if amount > 0 else "expense"
        )

        transactions.append(transaction)

    return transactions


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map common bank-export headers into SmartSpend's canonical CSV shape."""
    mapping = map_columns(list(df.columns))
    missing = {field for field in ("date", "description") if field not in mapping}
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    canonical = pd.DataFrame({
        "date": df[mapping["date"]],
        "description": df[mapping["description"]],
    })
    debit_column = _find_column(df, ("debit", "withdrawal"))
    credit_column = _find_column(df, ("credit", "deposit"))

    if debit_column and credit_column:
        canonical["amount"] = df[credit_column].map(_parse_amount) - df[debit_column].map(_parse_amount)
        return canonical

    amount_column = mapping.get("amount")
    if not amount_column:
        raise ValueError("Missing required columns: amount")

    amounts = df[amount_column].map(_parse_amount)
    normalized_amount_column = str(amount_column).strip().lower()
    if normalized_amount_column in {"debit", "withdrawal"}:
        amounts = -amounts.abs()
    elif normalized_amount_column in {"credit", "deposit"}:
        amounts = amounts.abs()
    else:
        transaction_type_column = mapping.get("transaction_type")
        if transaction_type_column:
            directions = df[transaction_type_column].fillna("").astype(str).str.strip().str.lower()
            amounts = amounts.where(~directions.str.startswith(("dr", "debit")), -amounts.abs())
            amounts = amounts.where(~directions.str.startswith(("cr", "credit")), amounts.abs())

    canonical["amount"] = amounts
    return canonical


def _find_column(df: pd.DataFrame, aliases: tuple[str, ...]) -> str | None:
    columns = {str(column).strip().lower(): column for column in df.columns}
    return next((columns[alias] for alias in aliases if alias in columns), None)


def _parse_amount(value) -> Decimal:
    if pd.isna(value):
        return Decimal("0")
    text = str(value).strip().replace(",", "").replace("₹", "").replace("$", "")
    if text.startswith("(") and text.endswith(")"):
        text = f"-{text[1:-1]}"
    return Decimal(text or "0")


def parse_csv(file_path: str):
    df = pd.read_csv(file_path)

    transactions = dataframe_to_transactions(df)

    return clean_transactions(transactions)


def parse_uploaded_csv(file_bytes: bytes):
    df = pd.read_csv(BytesIO(file_bytes))

    transactions = dataframe_to_transactions(df)

    return clean_transactions(transactions)
