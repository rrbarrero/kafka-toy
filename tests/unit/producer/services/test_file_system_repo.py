import json
import pytest

from common.domain.transaction import Transaction
from consumer.infra.filesystem_repo import FileSystemRepo
from builders import new_transaction_fixture_from


def read_rows(filesystem_repo: FileSystemRepo, file_name: str):

    file_path = filesystem_repo.output_path / f"{file_name}.json"
    assert file_path.exists(), f"Expected file {file_path} to exist"
    with file_path.open("r") as fr:
        return json.load(fr)


@pytest.mark.parametrize(
    "transactions",
    [
        [new_transaction_fixture_from()],
        [
            new_transaction_fixture_from({"amount": 100, "merchant": "merchant_name"}),
            new_transaction_fixture_from(
                {"amount": 200, "merchant": "another_merchant"}
            ),
        ],
    ],
)
def test_append_transactions(
    filesystem_repo: FileSystemRepo, transactions: list[Transaction]
):
    file_name = "test_file"

    for tx in transactions:
        filesystem_repo.add_transaction(tx, file_name)

    rows = read_rows(filesystem_repo, file_name)
    assert len(rows) == len(transactions), "Should be the same rows than transactions"

    expected = [tx.to_dict() for tx in transactions]
    assert rows == expected
