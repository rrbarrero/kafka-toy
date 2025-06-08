from common.domain.transaction import Transaction
from common.utils import load_fixture


class FakeConsumerRepository:
    def __init__(self, initial_data: list[Transaction] | None = None):
        self._data = initial_data or self._load_fixture()

    def get_batch(self, size: int = 10) -> list[Transaction] | None:
        return self._data[:size] if self._data else None  # type: ignore

    def _load_fixture(self) -> list[Transaction]:
        data = load_fixture("transactions.json")
        return [Transaction.new_from_dict(item) for item in data]
