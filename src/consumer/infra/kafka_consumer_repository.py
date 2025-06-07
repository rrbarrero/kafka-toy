from kafka import KafkaConsumer
from config import settings


class KafkaConsumerRepository:
    def __init__(self, consumer):
        self.consumer = consumer

    def list_topics(self):
        return self.consumer.topics()

    @classmethod
    def from_env(cls):

        consumer = KafkaConsumer(
            bootstrap_servers=settings.kafka_host,
            client_id="test_consumer",
            group_id="test_group",
            auto_offset_reset="earliest",
        )

        return cls(consumer)
