from common.services.transactions_factory import TransactionsFactory
from consumer.infra.filesystem_repo import FileSystemRepo
from consumer.infra.kafka_consumer_repository import KafkaConsumerRepository
from consumer.services.processors.high_value_seeker_processor import HighValueProcessor
from consumer.services.consumer_service import ConsumerService
from producer.infra.kafka_producer_repository import KafkaProducerRepository
from producer.services.producer_service import ProducerService


def create_kafka_consumer_repository() -> KafkaConsumerRepository:
    return KafkaConsumerRepository.from_env()


def create_producer_service() -> ProducerService:
    return ProducerService(
        kafka_repository=KafkaProducerRepository.from_env(),
        transaction_factory=TransactionsFactory(),
    )


def create_processors_service():
    return ConsumerService(
        processors=[create_high_value_processor()],
        kafka_repository=create_kafka_consumer_repository(),
    )


def create_high_value_processor():
    return HighValueProcessor(FileSystemRepo())
