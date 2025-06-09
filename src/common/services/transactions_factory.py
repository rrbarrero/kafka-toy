from uuid import UUID, uuid4
from faker import Faker

from common.domain.transaction import PaymentMethod, Transaction


class TransactionsFactory:
    def __init__(self):
        self.fake = Faker()
        self._customers = [
            UUID(x)
            for x in {
                "a6e1cbac-0a7e-422f-b741-4f16e9e05026",
                "f27333b3-7a6c-4ca4-ac90-e2db1f9fe8e2",
                "b4be53f1-d81f-41bb-a3e5-0c3a059465f4",
                "d04845d4-f97b-46ed-86a0-7bbc0a7a40c5",
                "ef9d3ea3-0b84-4a94-adcf-ed18133468d3",
            }
        ]

    def generate(self) -> Transaction:

        payment_methods: list[str] = [x.value for x in PaymentMethod]

        return Transaction.new(
            amount=self.fake.pyfloat(min_value=10, max_value=1000, right_digits=2),
            merchant=self.fake.company(),
            customer_id=self.fake_customer_generator(),
            payment_method=self.fake.random_element(payment_methods),
        )

    def generate_batch(self, size: int = 10) -> list[Transaction]:
        return [self.generate() for _ in range(size)]

    def fake_customer_generator(self) -> UUID:
        return self.fake.random_element(self._customers)
