from prepare import BaseTestCase, datatype_redis, unittest


class FloatTests(BaseTestCase):
    def test_value(self):
        a = 420.666
        self.assertAlmostEqual(datatype_redis.Float(a), a)

    def test_empty(self):
        self.assertEqual(datatype_redis.Int(), 0.0)

    def test_set(self):
        a = 420.666
        b = datatype_redis.Float()
        b.value = a
        self.assertAlmostEqual(b, a)
        b.value = 0.0
        self.assertAlmostEqual(b, 0.0)

    def test_add(self):
        a = 420.666
        b = 9000.666
        self.assertAlmostEqual(a + b, datatype_redis.Float(a) + datatype_redis.Float(b))
        self.assertAlmostEqual(a + b, datatype_redis.Float(a) + b)
        c = datatype_redis.Float(a)
        d = datatype_redis.Float(b)
        d += c
        c += b
        self.assertAlmostEqual(a + b, c)
        self.assertAlmostEqual(b + a, d)

    def test_mul(self):
        a = 420.666
        b = datatype_redis.Float(a)
        i = 9000.666
        self.assertAlmostEqual(a * i, datatype_redis.Float(a) * i)
        b *= i
        self.assertAlmostEqual(a * i, b)

    def test_sub(self):
        a = 420.666
        b = 9000.666
        self.assertAlmostEqual(a - b, datatype_redis.Float(a) - datatype_redis.Float(b))
        self.assertAlmostEqual(a - b, datatype_redis.Float(a) - b)
        c = datatype_redis.Float(a)
        d = datatype_redis.Float(b)
        d -= c
        c -= b
        self.assertAlmostEqual(a - b, c)
        self.assertAlmostEqual(b - a, d)

    def test_div(self):
        a = 420.666
        b = 9000.666
        self.assertAlmostEqual(a / b, datatype_redis.Float(a) / datatype_redis.Float(b))
        self.assertAlmostEqual(a / b, datatype_redis.Float(a) / b)
        c = datatype_redis.Float(a)
        d = datatype_redis.Float(b)
        d /= c
        c /= b
        self.assertAlmostEqual(a / b, c)
        self.assertAlmostEqual(b / a, d)

    def test_mod(self):
        a = 420.666
        b = 9000.666
        self.assertAlmostEqual(a % b, datatype_redis.Float(a) % datatype_redis.Float(b))
        self.assertAlmostEqual(a % b, datatype_redis.Float(a) % b)
        c = datatype_redis.Float(a)
        d = datatype_redis.Float(b)
        d %= c
        c %= b
        self.assertAlmostEqual(a % b, c)
        self.assertAlmostEqual(b % a, d)

    def test_pow(self):
        a = 4.666
        b = 20.666
        c = 4
        d = 2
        self.assertAlmostEqual(
            a ** b, datatype_redis.Float(a) ** datatype_redis.Float(b)
        )
        self.assertAlmostEqual(a ** b, datatype_redis.Float(a) ** b)
        e = datatype_redis.Float(a)
        f = datatype_redis.Float(b)
        f **= c
        e **= d
        self.assertAlmostEqual(a ** d, e)
        self.assertAlmostEqual(b ** c, f)
