from .dict import Dict
from ..operator import op_left, op_right, inplace
import operator
import collections
import logging

LOGGER = logging.getLogger(__name__)


class MultiSet(Dict):
    """
    Redis hash <-> Python dict <-> Python's collections.Counter.
    """

    def __init__(self, iterable=None, key=None, **kwargs):
        super().__init__(key=key)
        self.update(iterable=iterable, **kwargs)

    @property
    def value(self):
        value = super().value
        kwargs = dict([(k, int(v))
                       for k, v in value.items()])
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
            return super().__getitem__(name)
        except KeyError:
            return 0

    def __delitem__(self, name):
        try:
            super().__delitem__(name)
        except KeyError:
            pass

    def __repr__(self):
        bits = (self.__class__.__name__, repr(dict(self.value)), self.key)
        return "%s(%s, '%s')" % bits

    def values(self):
        values = super().values()
        return [int(v) for v in values]

    def get(self, key, default=None):
        value = super().get(key)
        return int(value) if value is not None else default

    def _merge(self, iterable=None, **kwargs):
        if iterable:
            try:
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
            yield k, v

    def _update(self, iterable, multiplier, **kwargs):
        for k, v in self._merge(iterable, **kwargs):
            LOGGER.debug(
                f"update - key: {k}, value: {v}, multiplier: {multiplier}")
            self[k] = self.get(k, 0) + v * multiplier
            LOGGER.debug(f"value: {self[k]}")

    def update(self, iterable=None, **kwargs):
        self._update(iterable, 1, **kwargs)

    def subtract(self, iterable=None, **kwargs):
        self._update(iterable, -1, **kwargs)

    def intersection_update(self, iterable=None, **kwargs):
        self.multiset_intersection_update(*self._flatten(iterable, **kwargs))
        return self

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

    def multiset_intersection_update(self, *flatten):
        intersect_dict = {}
        for key, value in flatten:
            intersect_dict[key] = value

        keys = set([x for x in self.keys()])
        filterKeys = set(intersect_dict.keys())

        intersect_keys = keys & filterKeys

        LOGGER.debug(
            f"intersection - keys: {keys}, filterKeys: {filterKeys} remove keys: {intersect_keys}")

        for k in intersect_keys:
            if self[k] < intersect_dict[k]:
                self[k] = intersect_dict[k]

        for k in keys - intersect_keys:
            del self[k]

    def multiset_union_update(self, *flatten):
        for key, value in flatten:
            if self[key] < value:
                self[key] = value


collections.MutableMapping.register(MultiSet)
