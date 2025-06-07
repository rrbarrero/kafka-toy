from consumer.infra.KafkaRepository import KafkaConsumerRepository


def create_kafka_repository():
    return KafkaConsumerRepository.from_env()
