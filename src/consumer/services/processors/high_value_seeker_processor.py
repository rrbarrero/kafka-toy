from common.domain.transaction import Transaction
from consumer.infra.filesystem_repo import FileSystemRepo


class HighValueProcessor:
    def __init__(self, consumer_client_id: str, filesystem_repo: FileSystemRepo):
        self.filesystem_repo = filesystem_repo
        self.consumer_client_id = consumer_client_id

    def handle(self, batch: list[Transaction] | None):
        if batch:
            for transaction in batch:
                if transaction.amount > 500:
                    self.filesystem_repo.append(
                        transaction, f"high_value_{self.consumer_client_id}"
                    )
