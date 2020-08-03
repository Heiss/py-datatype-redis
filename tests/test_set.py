from tests.prepare import BaseTestCase, datatype_redis, unittest


class SetTests(BaseTestCase):
    def test_value(self):
        a = set(["wagwaan", "hot", "skull"])
        self.assertEqual(datatype_redis.Set(a), a)

    def test_empty(self):
        self.assertEqual(datatype_redis.Set(), set())

    def test_empty_put(self):
        a = "wagwaan"
        s = datatype_redis.Set()
        s.add(a)
        self.assertEqual(set([a]), s)

    def test_add(self):
        a = set(["wagwaan", "hot", "skull"])
        b = datatype_redis.Set(a)
        i = "popcaan"
        a.add(i)
        b.add(i)
        self.assertEqual(b, a)

    def test_update(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["nba", "hang", "time"])
        c = set(["rap", "dot", "mom"])
        d = datatype_redis.Set(a)
        a.update(b, c)
        d.update(b, c)
        self.assertEqual(d, a)

    def test_pop(self):
        a = datatype_redis.Set(["wagwaan", "hot", "skull"])
        i = len(a)
        b = a.pop()
        self.assertEqual(len(a), i - 1)
        self.assertNotIn(b, a)

    def test_clear(self):
        a = datatype_redis.Set(["wagwaan", "hot", "skull"])
        a.clear()
        self.assertEqual(len(a), 0)

    def test_remove(self):
        a = datatype_redis.Set(["wagwaan", "hot", "skull"])
        i = len(a)
        b = "wagwaan"
        a.remove(b)
        self.assertEqual(len(a), i - 1)
        self.assertNotIn(b, a)
        self.assertRaises(KeyError, lambda: a.remove("popcaan"))

    def test_discard(self):
        a = datatype_redis.Set(["wagwaan", "hot", "skull"])
        i = len(a)
        b = "wagwaan"
        a.discard(b)
        self.assertEqual(len(a), i - 1)
        self.assertNotIn(b, a)
        self.assertEqual(a.discard("popcaan"), None)

    def test_len(self):
        a = set(["wagwaan", "hot", "skull"])
        b = datatype_redis.Set(a)
        self.assertEqual(len(a), len(b))

    def test_contains(self):
        a = datatype_redis.Set(["wagwaan", "hot", "skull"])
        self.assertIn("wagwaan", a)
        self.assertNotIn("popcaan", a)

    def test_intersection(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["wagwaan", "flute", "don"])
        c = set(["wagwaan", "worldstar", "hiphop"])
        d = datatype_redis.Set(a)
        e = a.intersection(b, c)
        self.assertEqual(a.intersection(b), d.intersection(b))
        self.assertEqual(e, d.intersection(b, c))
        self.assertEqual(e, d.intersection(datatype_redis.Set(b), c))
        self.assertEqual(e, d.intersection(b, datatype_redis.Set(c)))
        self.assertEqual(
            e, d.intersection(datatype_redis.Set(b), datatype_redis.Set(c))
        )

    def test_intersection_update(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["wagwaan", "flute", "don"])
        c = set(["wagwaan", "worldstar", "hiphop"])
        d = a.copy()
        d.intersection_update(b)
        e = datatype_redis.Set(a)
        e.intersection_update(b)
        self.assertEqual(e, d)
        d = a.copy()
        d.intersection_update(b, c)
        e = datatype_redis.Set(a)
        e.intersection_update(b, c)
        self.assertEqual(e, d)
        e = datatype_redis.Set(a)
        e.intersection_update(datatype_redis.Set(b), c)
        self.assertEqual(e, d)
        e = datatype_redis.Set(a)
        e.intersection_update(b, datatype_redis.Set(c))
        self.assertEqual(e, d)
        e = datatype_redis.Set(a)
        e.intersection_update(datatype_redis.Set(b), datatype_redis.Set(c))
        self.assertEqual(e, d)

    def test_difference(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["wagwaan", "flute", "don"])
        c = set(["wagwaan", "worldstar", "hiphop"])
        d = datatype_redis.Set(a)
        e = a.difference(b, c)
        self.assertEqual(a.difference(b), d.difference(b))
        self.assertEqual(e, d.difference(b, c))
        self.assertEqual(e, d.difference(datatype_redis.Set(b), c))
        self.assertEqual(e, d.difference(b, datatype_redis.Set(c)))
        self.assertEqual(e, d.difference(
            datatype_redis.Set(b), datatype_redis.Set(c)))

    def test_difference_update(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["wagwaan", "flute", "don"])
        c = set(["wagwaan", "worldstar", "hiphop"])
        d = a.copy()
        d.difference_update(b)
        e = datatype_redis.Set(a)
        e.difference_update(b)
        self.assertEqual(e, d)
        d = a.copy()
        d.difference_update(b, c)
        e = datatype_redis.Set(a)
        e.difference_update(b, c)
        self.assertEqual(e, d)
        e = datatype_redis.Set(a)
        e.difference_update(datatype_redis.Set(b), c)
        self.assertEqual(e, d)
        e = datatype_redis.Set(a)
        e.difference_update(b, datatype_redis.Set(c))
        self.assertEqual(e, d)
        e = datatype_redis.Set(a)
        e.difference_update(datatype_redis.Set(b), datatype_redis.Set(c))
        self.assertEqual(e, d)

    def test_symmetric_difference(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["wagwaan", "flute", "don"])
        c = datatype_redis.Set(a)
        d = a.symmetric_difference(b)
        self.assertEqual(d, c.symmetric_difference(b))
        self.assertEqual(d, c.symmetric_difference(datatype_redis.Set(b)))
        self.assertEqual(d, a.symmetric_difference(datatype_redis.Set(b)))

    def test_symmetric_difference_update(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["wagwaan", "flute", "don"])
        c = a.copy()
        c.difference_update(b)
        d = datatype_redis.Set(a)
        d.difference_update(b)
        self.assertEqual(d, c)
        d = datatype_redis.Set(a)
        d.difference_update(datatype_redis.Set(b))
        self.assertEqual(d, c)

    def test_disjoint(self):
        a = set(["wagwaan", "hot", "skull"])
        b = datatype_redis.Set(a)
        c = datatype_redis.Set(["wagwaan", "flute", "don"])
        d = set(["nba", "hang", "time"])
        e = datatype_redis.Set(d)
        self.assertFalse(b.isdisjoint(a))
        self.assertFalse(b.isdisjoint(c))
        self.assertTrue(b.isdisjoint(d))
        self.assertTrue(b.isdisjoint(e))

    def test_cmp(self):
        a = set(["wagwaan", "hot", "skull"])
        b = set(["nba", "hang", "time"])
        c = datatype_redis.Set(a)
        d = datatype_redis.Set(b)
        self.assertEqual(a > b, c > d)
        self.assertEqual(a < b, c < d)
        self.assertEqual(a > b, c > b)
        self.assertEqual(a < b, c < b)
        self.assertEqual(a >= b, c >= d)
        self.assertEqual(a <= b, c <= d)
        self.assertEqual(a >= b, c >= b)
        self.assertEqual(a <= b, c <= b)
        self.assertEqual(a.issubset(b), c.issubset(d))
        self.assertEqual(a.issuperset(b), c.issuperset(d))
        self.assertEqual(a.issubset(b), c.issubset(b))
        self.assertEqual(a.issuperset(b), c.issuperset(b))
