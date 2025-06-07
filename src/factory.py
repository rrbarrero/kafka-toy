from consumer.infra.kafka_consumer_repository import KafkaConsumerRepository
from producer.infra.kafka_producer_repository import KafkaProducerRepository
from producer.services.producer_service import ProducerService
from producer.services.transactions_factory import TransactionsFactory


def create_kafka_consumer_repository():
    return KafkaConsumerRepository.from_env()


def create_producer_service():
    ProducerService(
        kafka_repository=KafkaProducerRepository.from_env(),
        transaction_factory=TransactionsFactory(),
    )
