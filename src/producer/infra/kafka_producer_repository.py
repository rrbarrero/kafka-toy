from kafka import KafkaProducer
import json
from common.domain.transaction import Transaction
from config import settings


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
            value_serializer=lambda v: v.serialize(),
        )

        return cls(producer)
