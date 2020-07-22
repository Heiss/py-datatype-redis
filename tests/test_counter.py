from prepare import BaseTestCase, datatype_redis, unittest
import collections


class CounterTests(BaseTestCase):
    def test_value(self):
        a = "wagwaan"
        b = {"hot": 420, "skull": -9000}
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        e = collections.Counter(**b)
        f = datatype_redis.MultiSet(**b)
        self.assertEqual(d, c)
        self.assertEqual(f, e)

    def test_empty(self):
        self.assertEqual(datatype_redis.MultiSet(), collections.Counter())

    def test_values(self):
        a = "wagwaan"
        b = {"hot": 420, "skull": -9000}
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        e = collections.Counter(**b)
        f = datatype_redis.MultiSet(**b)
        self.assertItemsEqual(c.values(), d.values())
        self.assertItemsEqual(e.values(), f.values())

    def test_get(self):
        a = "wagwaan"
        b = {"hot": 420, "skull": -9000}
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        e = collections.Counter(**b)
        f = datatype_redis.MultiSet(**b)
        self.assertEqual(c.get("a"), d.get("a"))
        self.assertEqual(c.get("flute", "don"), d.get("flute", "don"))
        self.assertEqual(e.get("hot"), f.get("hot"))
        self.assertEqual(e.get("skull"), f.get("skull"))
        self.assertEqual(e.get("flute", "don"), e.get("flute", "don"))

    def test_del(self):
        a = datatype_redis.MultiSet("wagwaan")
        del a["hotskull"]

    def test_update(self):
        a = "wagwaan"
        b = {"hotskull": 420}
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.update(datatype_redis.MultiSet(a))
        d.update(datatype_redis.MultiSet(a))
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.update(collections.Counter(a))
        d.update(collections.Counter(a))
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.update(a)
        d.update(a)
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.update(b)
        d.update(b)
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.update(**b)
        d.update(**b)
        self.assertEqual(d, c)

    def test_subtract(self):
        a = "wagwaan"
        b = {"hotskull": 420}
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.subtract(datatype_redis.MultiSet(a))
        d.subtract(datatype_redis.MultiSet(a))
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.subtract(collections.Counter(a))
        d.subtract(collections.Counter(a))
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.subtract(a)
        d.subtract(a)
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.subtract(b)
        d.subtract(b)
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c.subtract(**b)
        d.subtract(**b)
        self.assertEqual(d, c)

    def test_intersection(self):
        a = "wagwaan"
        b = "flute don"
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c &= datatype_redis.MultiSet(b)
        d &= datatype_redis.MultiSet(b)
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c &= collections.Counter(b)
        d &= collections.Counter(b)
        self.assertEqual(d, c)

    def test_union(self):
        a = "wagwaan"
        b = "flute don"
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c |= datatype_redis.MultiSet(b)
        d |= datatype_redis.MultiSet(b)
        self.assertEqual(d, c)
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        c |= collections.Counter(b)
        d |= collections.Counter(b)
        self.assertEqual(d, c)

    def test_elements(self):
        a = "wagwaan"
        b = {"hotskull": 420}
        c = collections.Counter(a)
        d = datatype_redis.MultiSet(a)
        e = collections.Counter(**b)
        f = datatype_redis.MultiSet(**b)
        self.assertItemsEqual(sorted(c.elements()), sorted(d.elements()))
        self.assertItemsEqual(sorted(e.elements()), sorted(f.elements()))

    def test_most_common(self):
        a = "wagwaan"
        b = collections.Counter(a)
        c = datatype_redis.MultiSet(a)
        d = 420
        check = b.most_common(d)
        for i, e in enumerate(c.most_common(d)):
            self.assertEqual(e[1], check[i][1])
        check = b.most_common()
        for i, e in enumerate(c.most_common()):
            self.assertEqual(e[1], check[i][1])
