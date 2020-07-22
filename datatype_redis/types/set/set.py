from ..boolean.bitwise import Bitwise
from ..operator import inplace, op_right
import operator, uuid
from functools import reduce


class Set(Bitwise):
    """
    Redis set <-> Python set
    """

    @property
    def value(self):
        return self.smembers()

    @value.setter
    def value(self, item):
        self.update(item)

    def _all_redis(self, sets):
        return all([isinstance(s, self.__class__) for s in sets])

    def _to_keys(self, sets):
        return [s.key for s in sets]

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
        return self.scard()

    def __contains__(self, item):
        return self.sismember(item)

    def __iter__(self):
        return iter(self.value)

    def add(self, item):
        self.update([item])

    def update(self, *sets):
        self.sadd(*reduce(operator.or_, sets))

    def pop(self):
        return self.spop()

    def clear(self):
        self.delete()

    def remove(self, item):
        if self.srem(item) == 0:
            raise KeyError(item)

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def intersection(self, *sets):
        if self._all_redis(sets):
            return self.sinter(*self._to_keys(sets))
        else:
            return reduce(operator.and_, (self.value,) + sets)

    def intersection_update(self, *sets):
        if self._all_redis(sets):
            self.sinterstore(self.key, *self._to_keys(sets))
        else:
            sets = list(reduce(operator.and_, sets))
            self.set_intersection_update(*sets)
        return self

    def union(self, *sets):
        if self._all_redis(sets):
            return self.sunion(*self._to_keys(sets))
        else:
            return reduce(operator.or_, (self.value,) + sets)

    def difference(self, *sets):
        if self._all_redis(sets):
            return self.sdiff(*self._to_keys(sets))
        else:
            return reduce(operator.sub, (self.value,) + sets)

    def difference_update(self, *sets):
        if self._all_redis(sets):
            self.sdiffstore(self.key, *self._to_keys(sets))
        else:
            key = str(uuid.uuid4())
            flattened = [key]
            for s in sets:
                flattened.extend(s)
                flattened.append(key)
            self.set_difference_update(*flattened)
        return self

    def symmetric_difference(self, other):
        if isinstance(other, self.__class__):
            return set(self.set_symmetric_difference("return", other.key))
        else:
            return self.value ^ other

    def symmetric_difference_update(self, other):
        if isinstance(other, self.__class__):
            self.set_symmetric_difference("update", other.key)
        else:
            self.set_symmetric_difference("create", *other)
        return self

    def isdisjoint(self, other):
        return not self.intersection(other)

    def issubset(self, other):
        return self <= other

    def issuperset(self, other):
        return self >= other

    def set_intersection_update(self, *args):
        pass

    def set_difference_update(self, *args):
        pass

    def set_symmetric_difference(self, *args):
        pass
