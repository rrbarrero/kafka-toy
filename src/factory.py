from consumer.infra.kafka_consumer_repository import KafkaConsumerRepository


def create_kafka_repository():
    return KafkaConsumerRepository.from_env()
