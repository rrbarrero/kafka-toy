from typing import Any
from common.domain.transaction import Transaction


class FakeProcessor:
    def __init__(self, filter_by_amount=700):
        self.handled_batches = []
        self.filter_by_amount = filter_by_amount

    def handle(self, batch: list[Transaction] | None) -> Any:
        self.handled_batches.extend(
            list(filter(lambda x: x.amount > self.filter_by_amount, batch))  # type: ignore
        )
