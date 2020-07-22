from .numeric import Numeric
from ..operator import inplace
from ..pubsub import PubSub

class Float(Numeric):
    """
    Redis float <-> Python float.
    """

    @property
    def value(self):
        return float(self.get() or 0)

    @value.setter
    def value(self, value):
        if value is not None:
            self.set(value)

    def __isub__(self, f):
        self.incrbyfloat(f * -1)
        return self

    def __iadd__(self, f):
        self.incrbyfloat(f * 1) # this fixes conversion
        return self

class PubSubFloat(Float, PubSub):
    pass