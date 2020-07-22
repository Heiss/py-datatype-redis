from tests.prepare import BaseTestCase, datatype_redis, unittest

class ListTests(BaseTestCase):

    def test_initial(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        c = datatype_redis.List(a, key=b.key)
        self.assertItemsEqual(a, c)

    def test_value(self):
        a = ["wagwaan", "hot", "skull"]
        self.assertEqual(datatype_redis.List(a), a)

    def test_empty(self):
        self.assertEqual(datatype_redis.List(), [])

    def test_iter(self):
        a = ["wagwaan", "hot", "skull"]
        for i, x in enumerate(datatype_redis.List(a)):
            self.assertEqual(x, a[i])

    def test_add(self):
        a = ["wagwaan", "hot", "skull"]
        b = ["nba", "hang", "time"]
        self.assertEqual(a + b, datatype_redis.List(a) + datatype_redis.List(b))
        self.assertEqual(a + b, datatype_redis.List(a) + b)
        c = datatype_redis.List(a)
        d = datatype_redis.List(b)
        d += c
        c += b
        self.assertEqual(a + b, c)
        self.assertEqual(b + a, d)

    
    def test_mul(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        i = 10
        self.assertEqual(a * i, datatype_redis.List(a) * i)
        b *= i
        self.assertEqual(a * i, b)

    def test_len(self):
        a = ["wagwaan", "hot", "skull"]
        self.assertEqual(len(a), len(datatype_redis.List(a)))

    def test_get(self):
        a = ["wagwaan", "hot", "skull"] * 10
        b = datatype_redis.List(a)
        self.assertEqual(a[4], b[4])
        self.assertEqual(a[3:12], b[3:12])
        self.assertEqual(a[:-5], b[:-5])
        self.assertRaises(IndexError, lambda: b[len(b)])

    def test_set(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        i = "popcaan"
        a[1] = i
        self.assertNotEqual(a, b)
        b[1] = i
        self.assertEqual(a, b)
        # todo: slice

    
    def test_del(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        del a[1]
        self.assertNotEqual(a, b)
        del b[1]
        self.assertEqual(a, b)
        # todo: slice?

    def test_contains(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        self.assertIn("wagwaan", a)
        self.assertNotIn("hotskull", a)

    def test_extend(self):
        a = ["wagwaan", "hot", "skull"]
        b = ["nba", "hang", "time"]
        c = datatype_redis.List(a)
        a.extend(b)
        c.extend(b)
        self.assertEqual(a, c)

    def test_append(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        i = "popcaan"
        a.append(i)
        b.append(i)
        self.assertEqual(a, b)

    
    def test_insert(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        i = "popcaan"
        a.insert(1, i)
        b.insert(1, i)
        self.assertEqual(a, b)

    
    def test_pop(self):
        a = ["wagwaan", "hot", "skull"] * 10
        b = datatype_redis.List(a)
        a.pop()
        b.pop()
        self.assertEqual(a, b)
        a.pop(0)
        b.pop(0)
        self.assertEqual(a, b)
        a.pop(-1)
        b.pop(-1)
        self.assertEqual(a, b)
        a.pop(20)
        b.pop(20)
        self.assertEqual(a, b)

    
    def test_reverse(self):
        a = ["wagwaan", "hot", "skull"]
        b = datatype_redis.List(a)
        a.reverse()
        b.reverse()
        self.assertEqual(a, b)

    def test_index(self):
        a = ["wagwaan", "hot", "skull"] * 10
        b = datatype_redis.List(a)
        c = "wagwaan"
        self.assertEqual(a.index(c), b.index(c))
        self.assertRaises(ValueError, lambda: b.index("popcaan"))

    def test_count(self):
        a = ["wagwaan", "hot", "skull"] * 10
        b = datatype_redis.List(a)
        self.assertEqual(a.count("wagwaan"), b.count("wagwaan"))
        self.assertEqual(a.count("popcaan"), b.count("popcaan"))

    def test_sort(self):
        a = ["wagwaan", "hot", "skull"] * 10
        b = datatype_redis.List(a)
        a.sort()
        b.sort()
        self.assertEqual(a, b)
        a.sort(reverse=True)
        b.sort(reverse=True)
        self.assertEqual(a, b)
