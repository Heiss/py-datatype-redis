from tests.prepare import BaseTestCase, datatype_redis, unittest
import time
import queue


class QueueTests(BaseTestCase):
    def test_put(self):
        a = "wagwaan"
        b = "hotskull"
        q = datatype_redis.Queue(maxsize=2)
        q.put(a)
        self.assertIn(a, q)
        q.put(b)
        self.assertIn(b, q)
        self.assertRaises(
            queue.Full, lambda: q.put("popcaan", block=False)
        )
        start = time.time()
        timeout = 2
        try:
            q.put("popcaan", timeout=timeout)
        except queue.Full:
            pass
        self.assertTrue(time.time() - start >= timeout)

    def test_get(self):
        a = "wagwaan"
        b = "hotskull"
        q = datatype_redis.Queue()
        q.put(a)
        q.put(b)
        self.assertEqual(a, q.get())
        self.assertNotIn(a, q)
        self.assertEqual(b, q.get())
        self.assertNotIn(b, q)
        self.assertRaises(queue.Empty, lambda: q.get(block=False))
        start = time.time()
        timeout = 2
        try:
            q.get(timeout=timeout)
        except queue.Empty:
            pass
        self.assertTrue(time.time() - start >= timeout)

    def test_empty(self):
        q = datatype_redis.Queue()
        self.assertTrue(q.empty())
        q.put("wagwaan")
        self.assertFalse(q.empty())
        q.get()
        self.assertTrue(q.empty())

    def test_full(self):
        q = datatype_redis.Queue(maxsize=2)
        self.assertFalse(q.full())
        q.put("wagwaan")
        self.assertFalse(q.full())
        q.put("hotskull")
        self.assertTrue(q.full())
        q.get()
        self.assertFalse(q.full())

    def test_size(self):
        q = datatype_redis.Queue()
        self.assertEqual(q.qsize(), 0)
        q.put("wagwaan")
        self.assertEqual(q.qsize(), 1)
        q.put("hotskull")
        self.assertEqual(q.qsize(), 2)
        q.get()
        self.assertEqual(q.qsize(), 1)

    def test_lifo_queue(self):
        a = "wagwaan"
        b = "hotskull"
        q = datatype_redis.LifoQueue()
        q.put(a)
        q.put(b)
        self.assertEqual(b, q.get())
        self.assertNotIn(b, q)
        self.assertEqual(a, q.get())
        self.assertNotIn(a, q)

    def test_set_queue(self):
        a = "wagwaan"
        q = datatype_redis.SetQueue()
        q.put(a)
        self.assertEqual(q.qsize(), 1)
        q.put(a)
        self.assertEqual(q.qsize(), 1)
        self.assertEqual(q.get(), a)
        self.assertEqual(q.qsize(), 0)

