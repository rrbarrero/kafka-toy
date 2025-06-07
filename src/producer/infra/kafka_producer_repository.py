from kafka import KafkaProducer
import json
from config import settings
from producer.domain.transaction import Transaction


class KafkaProducerRepository:
    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def send(self, topic: str, value: Transaction, key: str | None = None):
        self.producer.send(topic, key=key, value=value)
        self.producer.flush()

    @classmethod
    def from_env(cls):

        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_host,
            value_serializer=lambda v: Transaction.serializer(v),
        )

        return cls(producer)
