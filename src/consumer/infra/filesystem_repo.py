from common.domain.transaction import Transaction
from config import settings


class FileSystemRepo:
    def __init__(self):
        self.output_path = settings.output_path

    def append(self, transaction: Transaction, file_name: str):
        with open(self.output_path / f"{file_name}.json", "a") as f:
            f.write(transaction.serialize().decode("utf-8"))
