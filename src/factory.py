from common.services.transactions_factory import TransactionsFactory
from consumer.infra.filesystem_repo import FileSystemRepo
from consumer.infra.kafka_consumer_repository import KafkaConsumerRepository
from consumer.services.processors.customer_balance_processor import (
    CustomerBalanceProcesor,
)
from consumer.services.processors.high_value_seeker_processor import HighValueProcessor
from consumer.services.consumer_service import ConsumerService
from producer.infra.kafka_producer_repository import KafkaProducerRepository
from producer.services.producer_service import ProducerService


def create_kafka_consumer_repository(client_id: str) -> KafkaConsumerRepository:
    return KafkaConsumerRepository.default_with(client_id)


def create_producer_service() -> ProducerService:
    return ProducerService(
        kafka_repository=KafkaProducerRepository.from_env(),
        transaction_factory=TransactionsFactory(),
    )


def create_consumer_service_zulu(consumer_client_id: str):
    return ConsumerService(
        processors=[create_high_value_processor(consumer_client_id)],
        kafka_repository=create_kafka_consumer_repository(consumer_client_id),
    )


def create_consumer_service_bravo(consumer_client_id: str):
    return ConsumerService(
        processors=[create_consumer_balance_processor(consumer_client_id)],
        kafka_repository=create_kafka_consumer_repository(consumer_client_id),
    )


def create_high_value_processor(consumer_client_id):
    return HighValueProcessor(consumer_client_id, FileSystemRepo())


def create_consumer_balance_processor(consumer_client_id):
    return CustomerBalanceProcesor(consumer_client_id, FileSystemRepo())
