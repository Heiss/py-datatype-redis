from .bitwise import Bitwise
from ..operator import inplace

class Bool(Bitwise):
    """
    Redis integer <-> Python integer.
    """

    @property
    def value(self):
        return bool(self.get() or False)

    @value.setter
    def value(self, value):
        if value is not None:
            self.set(bool(value))

    __iand__    = inplace("number_and")
    __ior__     = inplace("number_or")
    __ixor__    = inplace("number_xor")
    __ilshift__ = inplace("number_lshift")
    __irshift__ = inplace("number_rshift")