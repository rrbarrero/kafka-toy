import json
from uuid import UUID, uuid4
from producer.domain.transaction import PaymentMethod, Transaction
from tests.builders import new_transaction_fixture_from


def test_new_transaction():
    current = new_transaction_fixture_from()

    assert isinstance(current.id, UUID)
    assert current.amount == 100
    assert current.merchant == "merchant_name"
    assert current.customer_id == UUID("95cd471e-422c-45e7-83e0-06a3cfd3b92b")


def test_transaction_serialize():

    transaction = new_transaction_fixture_from()
    serialized = Transaction.serializer(transaction)

    deserialized = json.loads(serialized.decode("utf-8"))

    assert deserialized["id"] == str(transaction.id)
    assert deserialized["timestamp"] == transaction.timestamp
    assert deserialized["amount"] == transaction.amount
    assert deserialized["merchant"] == transaction.merchant
    assert deserialized["customer_id"] == str(transaction.customer_id)
    assert deserialized["payment_method"] == transaction.payment_method.value
