from consumer.infra.consumer_repository import ConsumerRepository
from consumer.services.processors.processor import Processor


class ConsumerService:
    def __init__(
        self, processors: list[Processor], kafka_repository: ConsumerRepository
    ):
        self.processors = processors
        self.kafka_repository = kafka_repository

    def start(self, daemon=True):
        print(
            f"[{self.kafka_repository.client_id()}] Starting consumer loop. Control+c to cancel the loop"
        )
        try:
            while True:
                batch = self.kafka_repository.get_batch()
                if not batch:
                    continue
                print(
                    f"[{self.kafka_repository.client_id()}] Received batch of {len(batch)} transactions",
                    flush=True,
                )
                for processor in self.processors:
                    processor.handle(batch)
                if not daemon:
                    break
        except KeyboardInterrupt:
            print("\nConsumer stopped by user.")
