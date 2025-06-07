from infra.KafkaRepository import KafkaRepository


def create_kafka_repository():
    return KafkaRepository.from_env()
