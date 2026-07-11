from models.transaction import Transaction


def validate_transaction(transaction: Transaction):

    if transaction.description == "":
        return False

    if transaction.amount == 0:
        return False

    return True