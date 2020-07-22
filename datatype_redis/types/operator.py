import sys


def value_left(self, right):
    """
    Returns the value of the right type instance to use in an
    operator method, namely when the method's instance is on the
    left side of the expression.
    """
    return right.value if isinstance(right, self.__class__) else right


def value_right(self, right):
    """
    Returns the value of the type instance calling an to use in an
    operator method, namely when the method's instance is on the
    right side of the expression.
    """
    return self if isinstance(right, self.__class__) else self.value


def op_left(op):
    """
    Returns a type instance method for the given operator, applied
    when the instance appears on the left side of the expression.
    """

    def method(self, right):
        return op(self.value, value_left(self, right))

    return method


def op_right(op):
    """
    Returns a type instance method for the given operator, applied
    when the instance appears on the right side of the expression.
    """

    def method(self, right):
        return op(value_left(self, right), value_right(self, right))

    return method


def inplace(method_name):
    """
    Returns a type instance method that will call the given method
    name, used for inplace operators such as __iadd__ and __imul__.
    """

    def method(self, *args):
        getattr(self, method_name)(*args)
        return self

    return method


def to_bits(m):
    return bin(m)


def tbl_to_number(m):
    return int(m)





