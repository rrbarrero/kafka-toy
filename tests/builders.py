from uuid import UUID
from producer.domain.transaction import Transaction


def new_transaction_fixture_from(data: dict = {}) -> Transaction:
    return Transaction.new(
        amount=data.get("amount", 100),
        merchant=data.get("merchant", "merchant_name"),
        customer_id=data.get(
            "customer_id", UUID("95cd471e-422c-45e7-83e0-06a3cfd3b92b")
        ),
        payment_method=data.get("payment_method", "credit_card"),
    )
