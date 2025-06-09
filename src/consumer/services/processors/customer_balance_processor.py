import polars as pl

from common.domain.transaction import Transaction
from consumer.infra.filesystem_repo import FileSystemRepo


class CustomerBalanceProcesor:
    def __init__(self, consumer_client_id: str, filesystem_repo: FileSystemRepo):
        self.consumer_client_id = consumer_client_id
        self.filesystem_repo = filesystem_repo

    def handle(self, batch: list[Transaction] | None):
        if batch is None or not batch:
            return None

        historic_df = self._normalize_schema(self._get_historic_df())
        batch_grouped = self._aggregate_current(batch)

        if historic_df.is_empty():
            final_df = batch_grouped.with_columns(
                pl.col("merchants")
                .list.len()
                .cast(pl.UInt32)
                .alias("unique_merchants_count")
            )
            self._save_df(final_df)
            return None

        if "unique_merchants_count" in historic_df.columns:
            historic_df = historic_df.drop("unique_merchants_count")

        combined = pl.concat([historic_df, batch_grouped])

        final_df = (
            combined.group_by("customer_id")
            .agg(
                [
                    pl.col("total_amount").sum(),
                    pl.col("transaction_count").sum(),
                    pl.col("merchants").explode().unique().alias("merchants"),
                    pl.col("payment_methods")
                    .explode()
                    .unique()
                    .alias("payment_methods"),
                ]
            )
            .with_columns(
                pl.col("merchants")
                .list.len()
                .cast(pl.UInt32)
                .alias("unique_merchants_count")
            )
        )

        self._save_df(final_df)

    def _save_df(self, final_df):
        final_df = final_df.select(
            "customer_id",
            "total_amount",
            "transaction_count",
            "unique_merchants_count",
            "merchants",
            "payment_methods",
        )
        self.filesystem_repo.write_parquet(
            final_df, f"customer_balance_{self.consumer_client_id}"
        )

    def _aggregate_current(self, batch):
        records = [tx.to_dict() for tx in batch]
        df = pl.DataFrame(records)

        batch_grouped = df.group_by("customer_id").agg(
            [
                pl.col("amount").sum().alias("total_amount"),
                pl.count().alias("transaction_count"),
                pl.col("merchant").unique().alias("merchants"),
                pl.col("payment_method").unique().alias("payment_methods"),
            ]
        )

        return batch_grouped

    def _get_historic_df(self):
        historic_df = self.filesystem_repo.read_parquet(
            f"customer_balance_{self.consumer_client_id}"
        )
        if historic_df is None:
            historic_df = pl.DataFrame()

        return historic_df

    def _normalize_schema(self, df: pl.DataFrame) -> pl.DataFrame:
        if df.is_empty():
            return df

        for col in ["merchants", "payment_methods"]:
            if col in df.columns:
                dtype = df.schema[col]

                if dtype == pl.Utf8:
                    df = df.with_columns(
                        pl.col(col).str.json_decode().cast(pl.List(pl.Utf8))
                    )
        return df
