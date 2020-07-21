from ..base import Base, op_left, op_right, operator

class Bitwise(Base):
    """
    Base class for bitwise types and relevant operators.
    """
    __and__       = op_left(operator.and_)
    __or__        = op_left(operator.or_)
    __xor__       = op_left(operator.xor)
    __lshift__    = op_left(operator.lshift)
    __rshift__    = op_left(operator.rshift)
    __rand__      = op_right(operator.and_)
    __ror__       = op_right(operator.or_)
    __rxor__      = op_right(operator.xor)
    __rlshift__   = op_right(operator.lshift)
    __rrshift__   = op_right(operator.rshift)