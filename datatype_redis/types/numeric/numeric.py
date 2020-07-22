from ..base import Base, op_left, op_right, operator, inplace, ValueDecorator


class Numeric(Base):
    """
    Base class for numeric types and relevant operators.
    """

    __add__ = op_left(operator.add)
    __sub__ = op_left(operator.sub)
    __mul__ = op_left(operator.mul)
    __floordiv__ = op_left(operator.floordiv)
    __truediv__ = op_left(operator.truediv)
    __mod__ = op_left(operator.mod)
    __divmod__ = op_left(divmod)
    __pow__ = op_left(operator.pow)
    __radd__ = op_right(operator.add)
    __rsub__ = op_right(operator.sub)
    __rmul__ = op_right(operator.mul)
    __rtruediv__ = op_right(operator.truediv)
    __rfloordiv__ = op_right(operator.floordiv)
    __rmod__ = op_right(operator.mod)
    __rdivmod__ = op_right(divmod)
    __rpow__ = op_right(operator.pow)
    __iadd__ = inplace("incr")
    __isub__ = inplace("decr")
    __imul__ = inplace("number_multiply")
    __idiv__ = inplace("number_divide")
    __ifloordiv__ = inplace("number_floordiv")
    __imod__ = inplace("number_mod")
    __ipow__ = inplace("number_pow")

    @ValueDecorator
    def incr(self, other):
        value = self.value + other
        self.value = value
        return value

    @ValueDecorator
    def decr(self, other):
        value = self.value - other
        self.value = value
        return value

    @ValueDecorator
    def number_multiply(self, other):
        value = self.value * other
        self.value = value
        return value

    @ValueDecorator
    def number_divide(self, other):
        value = self.value / other
        self.value = value
        return value

    @ValueDecorator
    def number_floordiv(self, other):
        value = self.value // other
        self.value = value
        return value

    @ValueDecorator
    def number_mod(self, other):
        value = self.value % other
        self.value = value
        return value

    @ValueDecorator
    def number_pow(self, other):
        value = self.value ** other
        self.value = value
        return value
