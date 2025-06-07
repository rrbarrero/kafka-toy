from kafka import KafkaConsumer
from common.domain.transaction import Transaction
from config import settings


class KafkaConsumerRepository:
    def __init__(self, consumer):
        self.consumer = consumer

    def pull_queue(self, size: int = 10):

        buffer: list[Transaction] = []

        for msg in self.consumer:
            buffer.append(Transaction.deserialize(msg.value))
            if len(buffer) >= size:
                self.consumer.commit()
                return buffer

    def list_topics(self):
        return self.consumer.topics()

    @classmethod
    def from_env(cls):

        consumer = KafkaConsumer(
            settings.transaction_topic,
            bootstrap_servers=settings.kafka_host,
            client_id="test_consumer",
            group_id="test_group",
            auto_offset_reset="earliest",
        )

        return cls(consumer)
