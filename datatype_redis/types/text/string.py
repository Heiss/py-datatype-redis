from ..base import Base
from ..operator import inplace
from ..pubsub import PubSub
from ..sequence.sequential import Sequential


class String(Sequential):
    """
    Redis string <-> Python string (although mutable).
    """

    @property
    def value(self):
        return self.get() or ""

    @value.setter
    def value(self, value):
        if value:
            self.set(value)

    __iadd__ = inplace("append")
    __imul__ = inplace("string_multiply")

    def __len__(self):
        return self.strlen()

    def __setitem__(self, i, s):
        if isinstance(i, slice):
            start = i.start if i.start is not None else 0
            stop = i.stop
        else:
            start = i
            stop = None
        if stop is not None and stop < start + len(s):
            self.string_setitem(start, stop, s)
        else:
            self.setrange(start, s)

    def __getitem__(self, i):
        if not isinstance(i, slice):
            i = slice(i, i + 1)
        start = i.start if i.start is not None else 0
        stop = i.stop if i.stop is not None else 0
        s = self.getrange(start, stop - 1)
        if not s:
            raise IndexError
        return s

    def __iter__(self):
        return iter(self.value)


class ImmutableString(String):
    """
    Redis string <-> Python string (actually immutable).
    """

    def __iadd__(self, other):
        self.key = self.__class__(self + other).key
        return self

    def __imul__(self, i):
        self.key = self.__class__(self * i).key
        return self

    def __setitem__(self, i):
        raise TypeError


class PubSubString(String, PubSub):
    __setitem__ = PubSub.publish_wrap(String.__setitem__)
