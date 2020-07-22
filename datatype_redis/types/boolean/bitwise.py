from ..base import Base, op_left, op_right, operator, ValueDecorator


class Bitwise(Base):
    """
    Base class for bitwise types and relevant operators.
    """

    __and__ = op_left(operator.and_)
    __or__ = op_left(operator.or_)
    __xor__ = op_left(operator.xor)
    __lshift__ = op_left(operator.lshift)
    __rshift__ = op_left(operator.rshift)
    __rand__ = op_right(operator.and_)
    __ror__ = op_right(operator.or_)
    __rxor__ = op_right(operator.xor)
    __rlshift__ = op_right(operator.lshift)
    __rrshift__ = op_right(operator.rshift)

    @ValueDecorator
    def bit_or(self, other):
        value = self.value | other
        self.value = value
        return value

    @ValueDecorator
    def bit_and(self, other):
        value = self.value & other
        self.value = value
        return value

    @ValueDecorator
    def bit_not(self):
        value = ~self
        self.value = value
        return value

    @ValueDecorator
    def bit_xor(self, other):
        value = self.value ^ other
        self.value = value
        return value

    @ValueDecorator
    def bit_lshift(self, bits):
        value = self.value << bits
        self.value = value
        return value

    @ValueDecorator
    def bit_rshift(self, bits):
        value = self.value >> bits
        self.value = value
        return value

