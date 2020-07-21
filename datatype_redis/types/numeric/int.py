from .numeric import Numeric
from ..boolean.bitwise import Bitwise
from ..operator import inplace
from ..pubsub import PubSub

class Int(Numeric, Bitwise):
    """
    Redis integer <-> Python integer.
    """

    @property
    def value(self):
        return int(float(self.get() or 0))

    @value.setter
    def value(self, value):
        if value is not None:
            self.set(value)

    __iand__    = inplace("number_and")
    __ior__     = inplace("number_or")
    __ixor__    = inplace("number_xor")
    __ilshift__ = inplace("number_lshift")
    __irshift__ = inplace("number_rshift")


class PubSubInt(Int, PubSub):
    pass