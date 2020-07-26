from .numeric import Numeric
from ..boolean.bitwise import Bitwise
from ..operator import inplace
from ..pubsub import PubSub
from ..base import ValueDecorator


class Int(Numeric, Bitwise):
    """
    Redis integer <-> Python integer.
    """

    @property
    def value(self):
        return int(float(self.client.get(self.prefixer(self.key)) or 0))

    @value.setter
    def value(self, value):
        if value is not None:
            self.client.set(self.prefixer(self.key), value)

    __iand__ = inplace("number_and")
    __ior__ = inplace("number_or")
    __ixor__ = inplace("number_xor")
    __ilshift__ = inplace("number_lshift")
    __irshift__ = inplace("number_rshift")
    
    number_or = inplace("bit_or")
    number_and = inplace("bit_and")
    number_xor = inplace("bit_xor")
    number_lshift = inplace("bit_lshift")
    number_rshift = inplace("bit_rshift")


class PubSubInt(Int, PubSub):
    pass
