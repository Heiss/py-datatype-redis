from .bitwise import Bitwise
from ..operator import inplace
from ..pubsub import PubSub


class Bool(Bitwise):
    """
    Redis integer <-> Python integer.
    """

    @property
    def value(self):
        return bool(self.client.get(self.prefixer(self.key)) or False)

    @value.setter
    def value(self, value):
        if value is not None:
            self.client.set(self.prefixer(self.key), bool(value))

    __iand__ = inplace("number_and")
    __ior__ = inplace("number_or")
    __ixor__ = inplace("number_xor")
    __ilshift__ = inplace("number_lshift")
    __irshift__ = inplace("number_rshift")


class PubSubBool(Bool, PubSub):
    pass
