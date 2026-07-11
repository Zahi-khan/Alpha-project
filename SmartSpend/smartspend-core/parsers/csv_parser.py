from io import BytesIO
from decimal import Decimal
from preprocessing.cleaner import clean_transactions


import pandas as pd

from models.transaction import Transaction

REQUIRED_COLUMNS = {
    "date",
    "description",
    "amount"
}


def dataframe_to_transactions(df: pd.DataFrame):

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
        amount = Decimal(str(row["amount"]))
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


def parse_csv(file_path: str):
    df = pd.read_csv(file_path)

    transactions = dataframe_to_transactions(df)

    return clean_transactions(transactions)


def parse_uploaded_csv(file_bytes: bytes):
    df = pd.read_csv(BytesIO(file_bytes))

    transactions = dataframe_to_transactions(df)

    return clean_transactions(transactions)
