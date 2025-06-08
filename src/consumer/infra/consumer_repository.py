from typing import Protocol

from common.domain.transaction import Transaction


class ConsumerRepository(Protocol):
    def get_batch(self, size: int = 10) -> list[Transaction] | None: ...
    def client_id(self) -> str: ...
