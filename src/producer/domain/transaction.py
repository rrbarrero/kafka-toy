from dataclasses import dataclass
import datetime
from enum import Enum
import json
from uuid import UUID, uuid4


class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"


@dataclass
class Transaction:
    id: UUID
    timestamp: float
    amount: float
    merchant: str
    customer_id: UUID
    payment_method: PaymentMethod

    @staticmethod
    def new(**kwargs):
        kwargs["payment_method"] = PaymentMethod(kwargs["payment_method"])
        return Transaction(
            id=uuid4(), timestamp=datetime.datetime.now().timestamp(), **kwargs
        )

    @staticmethod
    def serializer(transaction: "Transaction"):
        return json.dumps(
            {
                "id": str(transaction.id),
                "timestamp": transaction.timestamp,
                "amount": transaction.amount,
                "merchant": transaction.merchant,
                "customer_id": str(transaction.customer_id),
                "payment_method": transaction.payment_method.value,
            }
        ).encode("utf-8")
