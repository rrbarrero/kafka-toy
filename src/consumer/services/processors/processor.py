from typing import Any, Protocol

from common.domain.transaction import Transaction


class Processor(Protocol):
    def handle(self, batch: list[Transaction] | None) -> Any: ...
