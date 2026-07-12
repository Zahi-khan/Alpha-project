"""Present transactions while making uncertainty visible and hiding raw internals."""

from presentation.formatting.confidence_formatter import format_confidence
from presentation.formatting.currency_formatter import format_currency
from presentation.formatting.date_formatter import format_date
from presentation.models.views import TransactionView


class TransactionPresenter:
    def present(self, item, context):
        transaction = item.transaction
        source = transaction.metadata
        low_confidence = item.confidence < 0.70
        return TransactionView(
            id=transaction.id, formatted_date=format_date(transaction.date),
            merchant_name=item.merchant.canonical_name if item.merchant and not low_confidence else None,
            fallback_description=transaction.cleaned_description or transaction.description,
            original_description=source.get("description"),
            category_name=item.category.name if item.category else None,
            industry_name=item.industry.name if item.industry else None,
            payment_name=item.payment.method if item.payment else transaction.payment_method,
            source_type=source.get("type"),
            statement_reference=source.get("transaction_id"),
            balance=source.get("balance"),
            amount=transaction.amount, formatted_amount=format_currency(transaction.amount, context.currency),
            direction="income" if transaction.amount > 0 else "expense",
            confidence_label=format_confidence(item.confidence), warning_flags=item.warnings,
            review_required=low_confidence,
        )
