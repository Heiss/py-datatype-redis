from .sequential import Sequential
from ..operator import inplace
from ..base import ValueDecorator

import redis


class List(Sequential):
    """
    Redis list <-> Python list
    """

    @property
    def value(self):
        return self[:]

    @value.setter
    def value(self, value):
        self.clear()
        self.extend(value)

    def clear(self):
        self.client.delete(self.prefixer(self.key))

    __iadd__ = inplace("extend")
    __imul__ = inplace("list_multiply")

    def __len__(self):
        return self.client.llen(self.prefixer(self.key))

    def __setitem__(self, i, item):
        try:
            self.client.lset(self.prefixer(self.key), i, self.dumps(item))
        except redis.exceptions.ResponseError:
            raise IndexError

    def __getitem__(self, i):
        if isinstance(i, slice):
            start = i.start if i.start is not None else 0
            stop = i.stop if i.stop is not None else 0
            return [self.loads(item, raw=False) for item in self.client.lrange(self.prefixer(self.key), start, stop - 1)]

        item = self.client.lindex(self.prefixer(self.key), i)
        if item is None:
            raise IndexError
        return self.loads(item, raw=False)

    def __delitem__(self, i):
        self.pop(i)

    def __iter__(self):
        return iter(self.value)

    def append(self, item):
        if isinstance(item, (list, tuple)):
            self.extend(item)
        else:
            self.extend([item])

    def extend(self, other):
        self.client.rpush(
            self.prefixer(self.key),
            *[self.dumps(o) for o in other]
        )

    def insert(self, i, item):
        if i == 0:
            self.client.lpush(self.prefixer(self.key), self.dumps(item))
        else:
            self.list_insert(i, item)

    def pop(self, i=-1):
        if i == -1:
            return self.client.rpop(self.prefixer(self.key))
        elif i == 0:
            return self.client.lpop(self.prefixer(self.key))
        else:
            return self.list_pop(i)

    def reverse(self):
        self.list_reverse()

    def index(self, item):
        return self.value.index(item)

    def count(self, item):
        return self.value.count(item)

    def sort(self, reverse=False):
        self.client.sort(self.prefixer(self.key),
                         desc=reverse,
                         store=self.prefixer(self.key),
                         alpha=True
                         )

    @ValueDecorator
    def list_pop(self, i):
        value = list(self.value)
        del value[i]
        self.value = value
        return value

    @ValueDecorator
    def list_insert(self, i, item):
        value = list(self.value)
        value.insert(i, item)
        self.value = value
        return value

    def list_reverse(self):
        value = list(self.value)
        value.reverse()
        self.value = value
        return value

    @ValueDecorator
    def list_multiply(self, f):
        value = self.value * f
        self.value = value
        return value
