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
    def new_from_dict(data: dict):
        data["payment_method"] = PaymentMethod(data["payment_method"])
        data["id"] = UUID(data["id"])
        data["customer_id"] = UUID(data["customer_id"])
        return Transaction(**data)

    def to_dict(self):
        return {
            "id": str(self.id),
            "timestamp": self.timestamp,
            "amount": self.amount,
            "merchant": self.merchant,
            "customer_id": str(self.customer_id),
            "payment_method": self.payment_method.value,
        }

    def serialize(self):
        return json.dumps(self.to_dict()).encode("utf-8")

    @staticmethod
    def deserialize(data: bytes):
        _data = json.loads(data.decode("utf-8"))
        _data["payment_method"] = PaymentMethod(_data["payment_method"])
        _data["id"] = UUID(_data["id"])
        _data["customer_id"] = UUID(_data["customer_id"])
        return Transaction(**_data)
