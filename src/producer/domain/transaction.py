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

    def serialize(self):
        return json.dumps(
            {
                "id": str(self.id),
                "timestamp": self.timestamp,
                "amount": self.amount,
                "merchant": self.merchant,
                "customer_id": str(self.customer_id),
                "payment_method": self.payment_method.value,
            }
        ).encode("utf-8")
