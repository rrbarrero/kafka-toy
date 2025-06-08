import time
from kafka import KafkaConsumer
from common.domain.transaction import Transaction
from config import settings


class KafkaConsumerRepository:
    def __init__(self, client_id: str, consumer: KafkaConsumer):
        self.consumer = consumer
        self._client_id = client_id

    def get_batch(
        self,
        size: int = 3,
        max_wait_s: float = 2.0,
        poll_interval_ms: int = 500,
    ) -> list[Transaction] | None:
        buffer: list[Transaction] = []
        start_time: float | None = None

        while True:
            records = self.consumer.poll(timeout_ms=poll_interval_ms)

            for msgs in records.values():
                for msg in msgs:
                    if start_time is None:
                        start_time = time.monotonic()
                    buffer.append(Transaction.deserialize(msg.value))
                    if len(buffer) >= size:
                        self.consumer.commit()
                        return buffer

            if start_time is not None:
                elapsed = time.monotonic() - start_time
                if elapsed >= max_wait_s:
                    self.consumer.commit()
                    return buffer

            if start_time is None and max_wait_s <= poll_interval_ms / 1000:
                return None

    def list_topics(self):
        return self.consumer.topics()

    def client_id(self) -> str:
        return f"client {self._client_id}"

    @classmethod
    def default_with(cls, client_id: str):
        consumer = KafkaConsumer(
            settings.transaction_topic,
            bootstrap_servers=settings.kafka_host,
            client_id=client_id,
            group_id=f"test_group_{client_id.lower()}",
            auto_offset_reset="earliest",
            fetch_min_bytes=1,
            fetch_max_wait_ms=200,
            max_poll_records=10,
        )

        return cls(client_id, consumer)
