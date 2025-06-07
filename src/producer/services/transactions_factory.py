from uuid import uuid4
from faker import Faker
from producer.domain.transaction import PaymentMethod, Transaction


class TransactionsFactory:
    def __init__(self):
        self.fake = Faker()

    def generate(self) -> Transaction:

        payment_methods: list[str] = [x.value for x in PaymentMethod]

        return Transaction.new(
            amount=self.fake.pyfloat(min_value=10, max_value=1000, right_digits=2),
            merchant=self.fake.company(),
            customer_id=uuid4(),
            payment_method=self.fake.random_element(payment_methods),
        )
