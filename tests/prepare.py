import unittest
import datatype_redis
import os

# Env var specifying the precision for assertAlmostEqual - we may want
# to define this for alternate Lua implementations, like LuaJ.
TEST_PRECISION = int(os.environ.get("HOT_REDIS_TEST_PRECISION", 0)) or None

keys = []


def base_wrapper(init):
    def wrapper(*args, **kwargs):
        init(*args, **kwargs)
        keys.append(args[0].key)

    return wrapper


datatype_redis.Base.__init__ = base_wrapper(datatype_redis.Base.__init__)


class BaseTestCase(unittest.TestCase):
    def tearDown(self):
        client = prepare.datatype_redis.default_client()
        while prepare.keys:
            client.delete(prepare.keys.pop())

    # Removed in Python 3.
    def assertItemsEqual(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    # Configurable precision.
    def assertAlmostEqual(self, a, b):
        kwargs = {"places": TEST_PRECISION}
        return super(BaseTestCase, self).assertAlmostEqual(a, b, **kwargs)

