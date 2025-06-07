from common.domain.transaction import Transaction
from consumer.infra.kafka_consumer_repository import KafkaConsumerRepository
from consumer.services.processors.processor import Processor


class ConsumerService:
    def __init__(
        self, processors: list[Processor], kafka_repository: KafkaConsumerRepository
    ):
        self.processors = processors
        self.kafka_repository = kafka_repository

    def start(self):
        print(f"Starting consumer loop. Control+c to cancel the loop")
        try:
            while True:
                batch = self.kafka_repository.pull_queue()
                if not batch:
                    continue
                print(f"📦 Received batch of {len(batch)} transactions")
                for processor in self.processors:
                    processor.handle(batch)
        except KeyboardInterrupt:
            print("\n🛑 Consumer stopped by user.")
