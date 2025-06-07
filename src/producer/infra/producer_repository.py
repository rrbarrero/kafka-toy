from typing import Protocol

from producer.domain.transaction import Transaction


class ProducerRepository(Protocol):
    def send(self, topic: str, key: str, value: Transaction): ...
