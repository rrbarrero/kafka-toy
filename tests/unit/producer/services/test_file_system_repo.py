import json
import os
from consumer.infra.filesystem_repo import FileSystemRepo
from builders import new_transaction_fixture_from


def test_append(tmpdir):
    repo = FileSystemRepo(output_path=tmpdir)
    transaction = new_transaction_fixture_from()
    file_name = "test_file"
    repo.append(transaction, file_name)

    file_path = repo.output_path / f"{file_name}.json"
    assert os.path.exists(file_path)
    with open(file_path, "r") as fr:
        rows = json.load(fr)
        assert len(rows) == 1
        assert rows[0] == transaction.to_dict()


def test_append_multiple(tmpdir):
    repo = FileSystemRepo(output_path=tmpdir)
    transactions = [
        new_transaction_fixture_from({"amount": 100, "merchant": "merchant_name"}),
        new_transaction_fixture_from({"amount": 200, "merchant": "another_merchant"}),
    ]
    file_name = "test_file"
    for transaction in transactions:
        repo.append(transaction, file_name)

    file_path = repo.output_path / f"{file_name}.json"
    assert os.path.exists(file_path)
    with open(file_path, "r") as fr:
        rows = json.load(fr)
        assert len(rows) == 2
        for i, transaction in enumerate(transactions):
            assert rows[i] == transaction.to_dict()


def test_append_existing_file(tmpdir):
    repo = FileSystemRepo(output_path=tmpdir)
    transaction1 = new_transaction_fixture_from({"amount": 1})
    file_name = "test_file"
    repo.append(transaction1, file_name)

    transaction2 = new_transaction_fixture_from({"amount": 2})
    repo.append(transaction2, file_name)

    file_path = repo.output_path / f"{file_name}.json"
    assert os.path.exists(file_path)
    with open(file_path, "r") as fr:
        rows = json.load(fr)
        assert len(rows) == 2
        for i, transaction in enumerate([transaction1, transaction2]):
            assert rows[i] == transaction.to_dict()
