from tests.prepare import BaseTestCase, datatype_redis, unittest


class TransactionTests(BaseTestCase):
    def test_transaction(self):
        with_transaction = datatype_redis.List([1])
        without_transaction = datatype_redis.List(
            key=with_transaction.key, client=datatype_redis.HotClient()
        )
        with datatype_redis.transaction():
            with_transaction.append(1)
            self.assertEqual(len(without_transaction), 1)
        self.assertEqual(len(without_transaction), 2)
