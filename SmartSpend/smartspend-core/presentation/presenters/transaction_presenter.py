"""Present transactions while making uncertainty visible and hiding raw internals."""

from presentation.formatting.confidence_formatter import format_confidence
from presentation.formatting.currency_formatter import format_currency
from presentation.formatting.date_formatter import format_date
from presentation.models.views import TransactionView
from analytics.spending_policy import spending_type


class TransactionPresenter:
    def present(self, item, context):
        transaction = item.transaction
        source = transaction.metadata
        low_confidence = item.confidence < 0.70
        payment_initiator = item.processing_metadata.get("payment_initiator")
        merchant_visibility = item.processing_metadata.get("merchant_visibility")
        fallback = (
            f"Paid through {payment_initiator} — final merchant not visible"
            if merchant_visibility == "not_visible" and payment_initiator
            else transaction.cleaned_description or transaction.description
        )
        return TransactionView(
            id=transaction.id, date=transaction.date.date().isoformat() if transaction.date else None, formatted_date=format_date(transaction.date),
            merchant_name=item.merchant.canonical_name if item.merchant and not low_confidence else None,
            fallback_description=fallback,
            original_description=source.get("description"),
            category_name=item.category.name if item.category else None,
            spending_type=spending_type(item.category.name if item.category else None),
            industry_name=item.industry.name if item.industry else None,
            payment_name=item.payment.method if item.payment else transaction.payment_method,
            payment_initiator=payment_initiator,
            counterparty=item.processing_metadata.get("counterparty"),
            beneficiary_vpa=item.processing_metadata.get("beneficiary_vpa"),
            payment_reference=item.processing_metadata.get("payment_reference"),
            merchant_visibility=merchant_visibility,
            source_type=source.get("type"),
            statement_reference=source.get("transaction_id"),
            balance=source.get("balance"),
            amount=transaction.amount, formatted_amount=format_currency(transaction.amount, context.currency),
            direction="income" if transaction.amount > 0 else "expense",
            confidence_label=format_confidence(item.confidence), warning_flags=item.warnings,
            review_required=low_confidence,
        )
