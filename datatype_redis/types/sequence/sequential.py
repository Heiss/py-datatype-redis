from ..base import Base, op_left, op_right, operator

class Sequential(Base):
    """
    Base class for sequence types and relevant operators.
    """
    __add__       = op_left(operator.add)
    __mul__       = op_left(operator.mul)
    __radd__      = op_right(operator.add)
    __rmul__      = op_right(operator.mul)