import json
from pathlib import Path
from common.domain.transaction import Transaction
from config import settings
from os import path


class FileSystemRepo:
    def __init__(self, output_path: Path | None = None):
        self.output_path = output_path or settings.output_path

    def append(self, transaction: Transaction, file_name: str):
        file_path = self.output_path / f"{file_name}.json"

        rows: list[dict] = []

        if path.exists(file_path):
            with open(file_path, "r") as fr:
                rows = json.load(fr)

        with open(file_path, "w") as fw:
            rows.append(transaction.to_dict())
            json.dump(rows, fw)
