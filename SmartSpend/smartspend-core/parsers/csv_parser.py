from __future__ import annotations

from io import BytesIO
from decimal import Decimal, InvalidOperation
import re
from preprocessing.cleaner import clean_transactions


import pandas as pd

from models.transaction import Transaction
from parsers.column_mapper import map_columns, normalize

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
            date_value = str(row["date"]).strip()
            transaction_date = pd.to_datetime(
                date_value,
                dayfirst=bool(re.fullmatch(r"\d{2}[./-]\d{2}[./-]\d{2,4}", date_value)),
                errors="raise",
            ).to_pydatetime()
        except (TypeError, ValueError):
            continue

        vendor = _source_value(row, "source_vendor")
        transaction = Transaction(
            date=transaction_date,
            description=vendor or str(row["description"]).strip(),
            amount=amount,
            transaction_type="income" if amount > 0 else "expense",
            metadata={
                key.removeprefix("source_"): value
                for key in ("source_description", "source_vendor", "source_category", "source_mode", "source_type", "source_transaction_id", "source_balance")
                if (value := _source_value(row, key)) is not None
            },
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
    _copy_source_column(canonical, df, "source_description", mapping["description"])
    _copy_source_column(canonical, df, "source_vendor", _find_column(df, ("vendor", "merchant", "payee")))
    _copy_source_column(canonical, df, "source_category", _find_column(df, ("category", "spending category")))
    _copy_source_column(canonical, df, "source_mode", mapping.get("mode"))
    _copy_source_column(canonical, df, "source_type", mapping.get("transaction_type"))
    _copy_source_column(canonical, df, "source_transaction_id", _find_column(df, ("txnid", "transaction id", "reference number")))
    _copy_source_column(canonical, df, "source_balance", mapping.get("balance"))
    debit_column = _find_column(df, ("debit", "debit amount", "debit amt", "withdrawal", "withdrawal amount", "withdrawal amt"))
    credit_column = _find_column(df, ("credit", "credit amount", "credit amt", "deposit", "deposit amount", "deposit amt"))

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
    columns = {normalize(column): column for column in df.columns}
    return next((columns[normalize(alias)] for alias in aliases if normalize(alias) in columns), None)


def _copy_source_column(canonical: pd.DataFrame, source: pd.DataFrame, target: str, column: str | None) -> None:
    if column is not None:
        canonical[target] = source[column]


def _source_value(row, key: str) -> str | None:
    if key not in row or pd.isna(row[key]):
        return None
    value = str(row[key]).strip()
    return value or None


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
