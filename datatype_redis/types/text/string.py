from ..base import Base, ValueDecorator
from ..operator import inplace
from ..pubsub import PubSub
from ..sequence.sequential import Sequential


class String(Sequential):
    """
    Redis string <-> Python string (although mutable).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None

    @property
    def value(self):
        return str(self.client.get(self.prefixer(self.key)) or b"", "utf-8")

    @value.setter
    def value(self, value):
        if value is not None:
            self.client.set(self.prefixer(self.key), value)

    __iadd__ = inplace("append")
    __imul__ = inplace("multiply")

    def __len__(self):
        return self.client.strlen(self.prefixer(self.key))

    @ValueDecorator
    def append(self, other):
        value = self.value + other
        self.value = value
        return value

    def setitem(self, start, stop, s):
        value = self.value
        value = value[:start] + s + value[stop:]
        self.value = value
        return value

    @ValueDecorator
    def multiply(self, other):
        value = self.value * other
        self.value = value
        return value

    def __setitem__(self, i, s):
        if isinstance(i, slice):
            start = i.start if i.start is not None else 0
            stop = i.stop
        else:
            start = i
            stop = None
        if stop is not None and stop < start + len(s):
            self.setitem(start, stop, s)
        else:
            self.client.setrange(self.prefixer(self.key), start, s)

    def __getitem__(self, i):
        if not isinstance(i, slice):
            i = slice(i, i + 1)
        start = i.start if i.start is not None else 0
        stop = i.stop if i.stop is not None else 0
        s = self.client.getrange(self.prefixer(self.key), start, stop - 1)
        if not s:
            raise IndexError
        return s.decode("utf-8")

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

    def __setitem__(self, i, s):
        raise TypeError


class PubSubString(String, PubSub):
    __setitem__ = PubSub.publish_wrap(String.__setitem__)
