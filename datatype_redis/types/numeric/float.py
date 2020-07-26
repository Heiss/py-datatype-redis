from .numeric import Numeric
from ..operator import inplace
from ..pubsub import PubSub

class Float(Numeric):
    """
    Redis float <-> Python float.
    """

    @property
    def value(self):
        return float(self.client.get(self.prefixer(self.key)) or 0)

    @value.setter
    def value(self, value):
        if value is not None:
            self.client.set(self.prefixer(self.key), value)

    def __isub__(self, f):
        self.client.incrbyfloat(self.prefixer(self.key), f * -1)
        return self

    def __iadd__(self, f):
        self.client.incrbyfloat(self.prefixer(self.key), f * 1) # this fixes conversion
        return self

class PubSubFloat(Float, PubSub):
    pass