from tests.prepare import BaseTestCase, datatype_redis, unittest


class IntTests(BaseTestCase):
    def test_value(self):
        a = 420
        self.assertEqual(datatype_redis.Int(a), a)

    def test_empty(self):
        self.assertEqual(datatype_redis.Int(), 0)

    def test_set(self):
        a = 420
        b = datatype_redis.Int()
        b.value = a
        self.assertEqual(b, a)
        b.value = 0
        self.assertEqual(b, 0)

    def test_add(self):
        a = 420
        b = 9000
        self.assertEqual(a + b, datatype_redis.Int(a) + datatype_redis.Int(b))
        self.assertEqual(a + b, datatype_redis.Int(a) + b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d += c
        c += b
        self.assertEqual(a + b, c)
        self.assertEqual(b + a, d)

    def test_mul(self):
        a = 420
        b = datatype_redis.Int(a)
        i = 9000
        self.assertEqual(a * i, datatype_redis.Int(a) * i)
        b *= i
        self.assertEqual(a * i, b)

    def test_sub(self):
        a = 420
        b = 9000
        self.assertEqual(a - b, datatype_redis.Int(a) - datatype_redis.Int(b))
        self.assertEqual(a - b, datatype_redis.Int(a) - b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d -= c
        c -= b
        self.assertEqual(a - b, c)
        self.assertEqual(b - a, d)

    def test_div(self):
        a = 420
        b = 9000
        self.assertEqual(a / b, datatype_redis.Int(a) / datatype_redis.Int(b))
        self.assertEqual(a / b, datatype_redis.Int(a) / b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d /= c
        c /= b
        self.assertEqual(a / b, c)
        self.assertEqual(b / a, d)

    def test_mod(self):
        a = 420
        b = 9000
        self.assertEqual(a % b, datatype_redis.Int(a) % datatype_redis.Int(b))
        self.assertEqual(a % b, datatype_redis.Int(a) % b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d %= c
        c %= b
        self.assertEqual(a % b, c)
        self.assertEqual(b % a, d)

    def test_pow(self):
        a = 4
        b = 20
        self.assertEqual(a ** b, datatype_redis.Int(a) ** datatype_redis.Int(b))
        self.assertEqual(a ** b, datatype_redis.Int(a) ** b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d **= c
        c **= b
        self.assertEqual(a ** b, c)
        self.assertEqual(b ** a, d)

    def test_and(self):
        a = 420
        b = 9000
        self.assertEqual(a & b, datatype_redis.Int(a) & datatype_redis.Int(b))
        self.assertEqual(a & b, datatype_redis.Int(a) & b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d &= c
        c &= b
        self.assertEqual(a & b, c)
        self.assertEqual(b & a, d)

    def test_or(self):
        a = 420
        b = 9000
        self.assertEqual(a | b, datatype_redis.Int(a) | datatype_redis.Int(b))
        self.assertEqual(a | b, datatype_redis.Int(a) | b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d |= c
        c |= b
        self.assertEqual(a | b, c)
        self.assertEqual(b | a, d)

    def test_xor(self):
        a = 420
        b = 9000
        self.assertEqual(a ^ b, datatype_redis.Int(a) ^ datatype_redis.Int(b))
        self.assertEqual(a ^ b, datatype_redis.Int(a) ^ b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d ^= c
        c ^= b
        self.assertEqual(a ^ b, c)
        self.assertEqual(b ^ a, d)

    def test_lshift(self):
        a = 4
        b = 20
        self.assertEqual(a << b, datatype_redis.Int(a) << datatype_redis.Int(b))
        self.assertEqual(a << b, datatype_redis.Int(a) << b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d <<= c
        c <<= b
        self.assertEqual(a << b, c)
        self.assertEqual(b << a, d)

    def test_rshift(self):
        a = 9000
        b = 4
        self.assertEqual(a >> b, datatype_redis.Int(a) >> datatype_redis.Int(b))
        self.assertEqual(a >> b, datatype_redis.Int(a) >> b)
        c = datatype_redis.Int(a)
        d = datatype_redis.Int(b)
        d >>= c
        c >>= b
        self.assertEqual(a >> b, c)
        self.assertEqual(b >> a, d)
