import unittest
import datatype_redis
import os
import pytest

# Env var specifying the precision for assertAlmostEqual - we may want
# to define this for alternate Lua implementations, like LuaJ.
TEST_PRECISION = int(os.environ.get("HOT_REDIS_TEST_PRECISION", 0)) or None

keys = []


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            f.write(rep.longreprtext + "\n")


def base_wrapper(init):
    def wrapper(*args, **kwargs):
        init(*args, **kwargs)
        keys.append(args[0].key)

    return wrapper


datatype_redis.configure(
    host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", "6379")
)
datatype_redis.Base.__init__ = base_wrapper(datatype_redis.Base.__init__)


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

    def tearDown(self):
        client = datatype_redis.default_client()
        while keys:
            client.delete(keys.pop())

    # Removed in Python 3.
    def assertItemsEqual(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    # Configurable precision.
    def assertAlmostEqual(self, a, b):
        kwargs = {"places": TEST_PRECISION}
        return super(BaseTestCase, self).assertAlmostEqual(a, b, **kwargs)
