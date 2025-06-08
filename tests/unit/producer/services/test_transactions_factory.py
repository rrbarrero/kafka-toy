from common.domain.transaction import Transaction
from common.services.transactions_factory import TransactionsFactory


def test_transactions_factory():
    factory = TransactionsFactory()

    current = [factory.generate() for _ in range(10)]

    assert len(current) == 10
    assert all([isinstance(x, Transaction) for x in current])
