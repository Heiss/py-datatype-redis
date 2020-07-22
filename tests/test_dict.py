from tests.prepare import BaseTestCase, datatype_redis, unittest

class DictTests(BaseTestCase):

    def test_value(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        self.assertEqual(datatype_redis.Dict(a), a)

    def test_empty(self):
        self.assertEqual(datatype_redis.Dict(), {})

    def test_update(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        b = {"wagwaan": "hotskull", "nba": "hangtime"}
        c = datatype_redis.Dict(a)
        a.update(b)
        c.update(b)
        self.assertEqual(a, c)

    def test_iter(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        self.assertItemsEqual(iter(a), iter(datatype_redis.Dict(a)))

    def test_keys(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        self.assertItemsEqual(a.keys(), datatype_redis.Dict(a).keys())

    def test_values(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        self.assertItemsEqual(a.values(), datatype_redis.Dict(a).values())

    def test_items(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        self.assertItemsEqual(a.items(), datatype_redis.Dict(a).items())

    def test_setdefault(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        b = datatype_redis.Dict(a)
        c = "nba"
        d = "hangtime"
        e = b.setdefault(c, d)
        self.assertEqual(e, d)
        self.assertEqual(b[c], d)
        self.assertEqual(a.setdefault(c, d), e)
        e = b.setdefault(c, c)
        self.assertEqual(e, d)
        self.assertEqual(a.setdefault(c, c), e)

    def test_get(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        b = datatype_redis.Dict(a)
        self.assertEqual(a["wagwaan"], b["wagwaan"])
        self.assertEqual(a.get("wagwaan"), b.get("wagwaan"))
        self.assertRaises(KeyError, lambda: b["hotskull"])
        self.assertEqual(a.get("hotskull"), b.get("hotskull"))
        self.assertEqual(a.get("hotskull", "don"), b.get("hotskull", "don"))
        self.assertNotEqual(a.get("hotskull", "don"), b.get("hotskull", "x"))

    def test_set(self):
        a = datatype_redis.Dict({"wagwaan": "popcaan", "flute": "don"})
        a["wagwaan"] = "hotskull"
        self.assertEqual(a["wagwaan"], "hotskull")

    def test_del(self):
        a = datatype_redis.Dict({"wagwaan": "popcaan", "flute": "don"})
        del a["wagwaan"]
        self.assertRaises(KeyError, lambda: a["wagwaan"])
        def del_missing():
            del a["hotskull"]
        self.assertRaises(KeyError, del_missing)

    def test_len(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        b = datatype_redis.Dict(a)
        self.assertEqual(len(a), len(b))

    def test_contains(self):
        a = {"wagwaan": "popcaan", "flute": "don"}
        b = datatype_redis.Dict(a)
        self.assertIn("wagwaan", a)
        self.assertNotIn("hotskull", a)

    def test_copy(self):
        a = datatype_redis.Dict({"wagwaan": "popcaan", "flute": "don"})
        b = a.copy()
        self.assertEqual(type(a), type(b))
        self.assertNotEqual(a.key, b.key)

    def test_clear(self):
        a = datatype_redis.Dict({"wagwaan": "popcaan", "flute": "don"})
        a.clear()
        self.assertEqual(len(a), 0)

    def test_fromkeys(self):
        a = ["wagwaan", "hot", "skull"]
        b = "popcaan"
        c = datatype_redis.Dict.fromkeys(a)
        self.assertItemsEqual(sorted(a), sorted(c.keys()))
        self.assertFalse(c["wagwaan"])
        c = datatype_redis.Dict.fromkeys(a, b)
        self.assertEqual(c["wagwaan"], b)

    
    def test_defaultdict(self):
        a = "wagwaan"
        b = "popcaan"
        c = datatype_redis.DefaultDict(lambda: b)
        self.assertEqual(c[a], b)
        c[b] += a
        self.assertEqual(c[b], b + a)





