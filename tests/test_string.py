from prepare import BaseTestCase, datatype_redis, unittest


class StringTests(BaseTestCase):
    def test_value(self):
        a = "wagwaan"
        self.assertEqual(datatype_redis.String(a), a)

    def test_empty(self):
        self.assertEqual(datatype_redis.String(), "")

    def test_add(self):
        a = "wagwaan"
        b = "hotskull"
        c = datatype_redis.String(a)
        d = datatype_redis.String(b)
        self.assertEqual(a + b, datatype_redis.String(a) + datatype_redis.String(b))
        self.assertEqual(a + b, datatype_redis.String(a) + b)
        d += c
        c += b
        self.assertEqual(a + b, c)
        self.assertEqual(b + a, d)

    def test_mul(self):
        a = "wagwaan"
        b = datatype_redis.String(a)
        i = 9000
        self.assertEqual(a * i, datatype_redis.String(a) * i)
        b *= i
        self.assertEqual(a * i, b)

    def test_len(self):
        a = "wagwaan"
        self.assertEqual(len(a), len(datatype_redis.String(a)))

    def test_set(self):
        a = "wagwaan hotskull"
        b = "flute don"
        for i in range(0, len(b)):
            for j in range(i, len(b)):
                c = list(a)
                d = datatype_redis.String(a)
                c[i:j] = list(b)
                d[i:j] = b
                c = "".join(c)
                self.assertEqual(d, c)

    def test_get(self):
        a = "wagwaan hotskull"
        b = datatype_redis.String(a)
        self.assertEqual(a[4], b[4])
        self.assertEqual(a[3:12], b[3:12])
        self.assertEqual(a[:-5], b[:-5])
        self.assertRaises(IndexError, lambda: b[len(b)])

    def test_mutability(self):
        a = "wagwaan hotskull"
        b = "flute don"
        c = datatype_redis.String(a)
        d = datatype_redis.ImmutableString(a)
        keyC = c.key
        keyD = d.key
        a += b
        c += b
        d += b
        self.assertEqual(a, c)
        self.assertEqual(a, d)
        self.assertEqual(c.key, keyC)
        self.assertNotEqual(d.key, keyD)
        keyD = d.key
        i = 9000
        a *= i
        c *= i
        d *= i
        self.assertEqual(a, c)
        self.assertEqual(a, d)
        self.assertEqual(c.key, keyC)
        self.assertNotEqual(d.key, keyD)

        def immutable_set():
            d[0] = b

        self.assertRaises(TypeError, immutable_set)
