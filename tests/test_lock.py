from tests.prepare import BaseTestCase, datatype_redis, unittest


class LockTests(BaseTestCase):
    def test_semaphore(self):
        semaphore = datatype_redis.Semaphore()
        self.assertEqual(semaphore.acquire(), True)
        self.assertEqual(semaphore.release(), None)
        self.assertEqual(semaphore.release(), None)

    def test_bounded_semaphore(self):
        max_size = 2
        semaphore = datatype_redis.BoundedSemaphore(value=max_size)
        self.assertEqual(semaphore.acquire(), True)
        self.assertEqual(semaphore.release(), None)
        with semaphore:
            with semaphore:
                self.assertEqual(semaphore.acquire(block=False), False)
        self.assertRaises(RuntimeError, semaphore.release)

    def test_lock(self):
        lock = datatype_redis.Lock()
        self.assertEqual(lock.acquire(), True)
        self.assertEqual(lock.release(), None)
        with lock:
            self.assertEqual(lock.acquire(block=False), False)
        self.assertRaises(RuntimeError, lock.release)
