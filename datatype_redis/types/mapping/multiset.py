from .dict import Dict
from ..operator import op_left, op_right, inplace
import operator, collections


class MultiSet(Dict):
    """
    Redis hash <-> Python dict <-> Python's collections.Counter.
    """

    def __init__(self, iterable=None, key=None, **kwargs):
        super(MultiSet, self).__init__(key=key)
        self.update(iterable=iterable, **kwargs)

    @property
    def value(self):
        value = super(MultiSet, self).value
        kwargs = dict([(k, int(v)) for k, v in value.items()])
        return collections.Counter(**kwargs)

    __add__ = op_left(operator.add)
    __sub__ = op_left(operator.sub)
    __and__ = op_left(operator.and_)
    __or__ = op_left(operator.or_)
    __radd__ = op_right(operator.add)
    __rsub__ = op_right(operator.sub)
    __rand__ = op_right(operator.and_)
    __ror__ = op_right(operator.or_)
    __iadd__ = inplace("update")
    __isub__ = inplace("subtract")
    __iand__ = inplace("intersection_update")
    __ior__ = inplace("union_update")

    # Return 0 as a default, which allows bitwise ops to work correctly
    # in Python 3, as its Counter type no longer supports working with
    # missing values.
    def __getitem__(self, name):
        try:
            return super(MultiSet, self).__getitem__(name)
        except KeyError:
            return 0

    def __delitem__(self, name):
        try:
            super(MultiSet, self).__delitem__(name)
        except KeyError:
            pass

    def __repr__(self):
        bits = (self.__class__.__name__, repr(dict(self.value)), self.key)
        return "%s(%s, '%s')" % bits

    def values(self):
        values = super(MultiSet, self).values()
        return [int(v) for v in values]

    def get(self, key, default=None):
        value = self.hget(key)
        return int(value) if value is not None else default

    def _merge(self, iterable=None, **kwargs):
        if iterable:
            try:
                try:
                    # Python 2.
                    items = iterable.iteritems()
                except AttributeError:
                    # Python 3.
                    items = iterable.items()
            except AttributeError:
                for k in iterable:
                    kwargs[k] = kwargs.get(k, 0) + 1
            else:
                for k, v in items:
                    kwargs[k] = kwargs.get(k, 0) + v
        return kwargs.items()

    def _flatten(self, iterable, **kwargs):
        for k, v in self._merge(iterable, **kwargs):
            yield k
            yield v

    def _update(self, iterable, multiplier, **kwargs):
        for k, v in self._merge(iterable, **kwargs):
            self.hincrby(k, v * multiplier)

    def update(self, iterable=None, **kwargs):
        self._update(iterable, 1, **kwargs)

    def subtract(self, iterable=None, **kwargs):
        self._update(iterable, -1, **kwargs)

    def intersection_update(self, iterable=None, **kwargs):
        self.multiset_intersection_update(*self._flatten(iterable, **kwargs))

    def union_update(self, iterable=None, **kwargs):
        self.multiset_union_update(*self._flatten(iterable, **kwargs))

    def elements(self):
        for k, count in self.iteritems():
            for i in range(count):
                yield k

    def most_common(self, n=None):
        values = sorted(self.iteritems(), key=lambda v: v[1], reverse=True)
        if n:
            values = values[:n]
        return values

    def multiset_intersection_update(self, *args):
        pass


collections.MutableMapping.register(MultiSet)
