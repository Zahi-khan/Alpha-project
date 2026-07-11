from models.transaction import Transaction


def remove_duplicates(transactions: list[Transaction]):

    unique = {}

    for transaction in transactions:

        key = (
            transaction.date,
            transaction.description,
            transaction.amount
        )

        unique[key] = transaction

    return list(unique.values())