from ..boolean.bitwise import Bitwise
from ..operator import inplace, op_right
import operator
import uuid
from functools import reduce
import logging

LOGGER = logging.getLogger(__name__)


class Set(Bitwise):
    """
    Redis set <-> Python set
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.value) == 0:
            self.clear()

    @property
    def value(self):
        def loads(items):
            val = []
            for item in items:
                val.append(self.loads(item, raw=False))
            return val

        return set(loads(self.client.smembers(self.prefixer(self.key))))

    @value.setter
    def value(self, item):
        self.clear()
        self.update(item)

    def _all_redis(self, sets):
        return False
        """TODO
        all([isinstance(s, self.__class__) for s in sets])"""

    def _to_keys(self, sets):
        return [s.prefixer(s.key) for s in sets]

    __iand__ = inplace("intersection_update")
    __ior__ = inplace("update")
    __ixor__ = inplace("symmetric_difference_update")
    __isub__ = inplace("difference_update")
    __rsub__ = op_right(operator.sub)

    def __and__(self, value):
        return self.intersection(value)

    def __or__(self, value):
        return self.union(value)

    def __xor__(self, value):
        return self.symmetric_difference(value)

    def __sub__(self, value):
        return self.difference(value)

    def __len__(self):
        return self.client.scard(self.prefixer(self.key))

    def __contains__(self, item):
        return self.client.sismember(self.prefixer(self.key), self.dumps(item))

    def __iter__(self):
        return iter(self.value)

    def __eq__(self, other):
        if isinstance(other, set):
            return self.value == other

        if isinstance(other, Set):
            return self.value == other.value

        return False

    def add(self, item):
        if isinstance(item, (tuple, list)):
            return self.update(*item)
        return self.update([item])

    def update(self, *sets):
        LOGGER.warning("update: prefix: {}, sets: {}".format(
            self.prefixer(self.key), sets))

        def dumps(items):
            return [self.dumps(item) for item in items]

        val = dumps(reduce(operator.or_, sets))
        LOGGER.warning("set value: {}".format(val))

        return self.client.sadd(self.prefixer(self.key), *val) > 0

    def pop(self):
        return self.client.spop(self.prefixer(self.key))

    def clear(self):
        self.client.delete(self.prefixer(self.key))

    def remove(self, item):
        if self.client.srem(self.prefixer(self.key), self.dumps(item)) == 0:
            raise KeyError(item)

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def intersection(self, *sets):
        if self._all_redis(sets):
            return self.client.sinter(self.prefixer(self.key), *self._to_keys(sets))
        else:
            return reduce(operator.and_, (self.value,) + sets)

    def intersection_update(self, *sets):
        if self._all_redis(sets):
            self.client.sinterstore(self.key, *self._to_keys(sets))
        else:
            self.value = self.intersection(*sets)

        return self

    def union(self, *sets):
        if self._all_redis(sets):
            return self.client.sunion(*self._to_keys(sets))
        else:
            return reduce(operator.or_, (self.value,) + sets)

    def difference(self, *sets):
        if self._all_redis(sets):
            return self.client.sdiff(*self._to_keys(sets))
        else:
            return reduce(operator.sub, (self.value,) + sets)

    def difference_update(self, *sets):
        if self._all_redis(sets):
            self.client.sdiffstore(self.prefixer(
                self.key), *self._to_keys(sets))
        else:
            self.value = self.difference(*sets)
        return self

    def symmetric_difference(self, other):
        if isinstance(other, self.__class__):
            return self.value.symmetric_difference(other)
        else:
            return self.value ^ other

    def symmetric_difference_update(self, other):
        self.value = self.value.symmetric_difference(other)
        return self

    def isdisjoint(self, other):
        return not self.intersection(other)

    def issubset(self, other):
        return self <= other

    def issuperset(self, other):
        return self >= other
