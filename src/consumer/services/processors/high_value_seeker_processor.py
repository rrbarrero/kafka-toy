from common.domain.transaction import Transaction
from consumer.infra.filesystem_repo import FileSystemRepo


class HighValueProcessor:
    def __init__(self, filesystem_repo: FileSystemRepo):
        self.filesystem_repo = filesystem_repo

    def handle(self, batch: list[Transaction] | None):
        if batch:
            for transaction in batch:
                if transaction.amount > 500:
                    self.filesystem_repo.append(transaction, "high_value")
