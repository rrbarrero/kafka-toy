import time
from producer.infra.producer_repository import ProducerRepository
from producer.services.transactions_factory import TransactionsFactory
from config import settings


class ProducerService:
    def __init__(
        self,
        kafka_repository: ProducerRepository,
        transaction_factory: TransactionsFactory,
    ):
        self.kafka_repository = kafka_repository
        self.transaction_factory = transaction_factory

    def start(self, interval_seconds: int = 30):
        print(
            f"Starting producer loop (interval: {interval_seconds}s)... Control+c to cancel the loop"
        )
        try:
            while True:
                transaction = self.transaction_factory.generate()
                self.kafka_repository.send(
                    settings.transaction_topic, value=transaction
                )
                print(f"✅ Sent transaction: {transaction.id}")
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n🛑 Producer stopped by user.")
