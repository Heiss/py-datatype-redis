from .numeric import Numeric
from ..operator import inplace

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

    __iadd__ = inplace("incrbyfloat")

    def __isub__(self, f):
        self.incrbyfloat(f * -1)
        return self