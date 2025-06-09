import json
from pathlib import Path
from common.domain.transaction import Transaction
from config import settings
from os import path
import polars as pl


class FileSystemRepo:
    def __init__(self, output_path: Path | None = None):
        self.output_path = output_path or settings.output_path

    def add_transaction(self, transaction: Transaction, file_name: str):
        normalized = self._normalize_file_name(file_name)
        file_path = self.output_path / f"{normalized}.json"

        rows: list[dict] = []

        if path.exists(file_path):
            with open(file_path, "r") as fr:
                rows = json.load(fr)

        with open(file_path, "w") as fw:
            rows.append(transaction.to_dict())
            json.dump(rows, fw)

    def read_parquet(self, file_name: str):
        normalized = self._normalize_file_name(file_name)
        file_path = self.output_path / f"{normalized}.parquet"

        if path.exists(file_path):
            return pl.read_parquet(file_path)

    def write_parquet(self, df: pl.DataFrame, file_name: str):
        normalized = self._normalize_file_name(file_name)
        file_path = self.output_path / f"{normalized}.parquet"

        df.write_parquet(file_path)

    def _normalize_file_name(self, file_name: str):
        if "🔵 " in file_name:
            return file_name.replace("🔵 ", "").lower()
        if "🟣 " in file_name:
            return file_name.replace("🟣 ", "").lower()
        return file_name.lower()
