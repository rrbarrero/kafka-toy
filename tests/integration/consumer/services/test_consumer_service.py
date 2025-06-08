import pytest
from common.domain.transaction import Transaction
from consumer.infra.fake_consumer_repository import FakeConsumerRepository
from consumer.services.consumer_service import ConsumerService
from consumer.services.processors.fake_processor import FakeProcessor

RAW_TRANSACTION_DATA = {
    "first": {
        "id": "8d58d049-e878-4a49-946d-e5d358b6b216",
        "timestamp": 1749370618.467889,
        "amount": 732.42,
        "merchant": "Ortiz, Rodriguez and Clark",
        "customer_id": "6bb9c72b-ea5a-4c9c-b6db-dcd8057ee71a",
        "payment_method": "credit_card",
    },
    "second": {
        "id": "f6f7d5c6-83b9-4f75-8734-62a479b1a0a0",
        "timestamp": 1749370618.47021,
        "amount": 616.95,
        "merchant": "Thompson-Fernandez",
        "customer_id": "592ab54b-856b-4af6-9a6a-647d9aa2e792",
        "payment_method": "debit_card",
    },
}


@pytest.fixture
def expected_transactions():
    return [
        Transaction.new_from_dict(RAW_TRANSACTION_DATA["first"]),
        Transaction.new_from_dict(RAW_TRANSACTION_DATA["second"]),
    ]


@pytest.fixture
def processors():
    p1 = FakeProcessor()
    p2 = FakeProcessor(filter_by_amount=600)
    return p1, p2


@pytest.fixture
def consumer_service(processors):
    p1, p2 = processors
    return ConsumerService([p1, p2], FakeConsumerRepository("zulu"))


def test_consumer_service_processes_and_stops(
    consumer_service, expected_transactions, capsys
) -> None:
    consumer_service.start(daemon=False)

    p1, p2 = consumer_service.processors

    assert p1.handled_batches == [expected_transactions[0]]

    assert p2.handled_batches == expected_transactions

    captured_output = capsys.readouterr().out

    assert "Starting consumer loop. Control+c to cancel the loop" in captured_output
    assert "[client zulu] Received batch of 10 transactions\n" in captured_output
