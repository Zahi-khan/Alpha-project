"""Group by payment method."""
class PaymentGrouping:
    def key_for(self, item): return item.payment.method if item.payment else "Unknown"
