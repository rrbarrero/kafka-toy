from typing import Protocol

from producer.domain.transaction import Transaction


class ProducerRepository(Protocol):
    def send(self, topic: str, value: Transaction, key: str | None = None): ...
