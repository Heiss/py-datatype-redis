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

    def method(self, other):
        getattr(self, method_name)(value_left(self, other))
        return self

    return method


def to_bits(m):
    return bin(m)


def tbl_to_number(m):
    return int(m)


def bit_or(m, n):
    return m | n


def bit_and(m, n):
    return m & n


def bit_not(m):
    return ~m


def bit_xor(m, n):
    return m ^ n


def bit_lshift(m, bits):
    return m << bits


def bit_rshift(m, bits):
    return m >> bits


def number_or(left, right):
    value = bit_or(left.value(), right.value())
    left.value(value)
    return value


def number_and(left, right):
    value = bit_and(left.value(), right.value())
    left.value(value)
    return value


def number_xor(left, right):
    value = bit_xor(left.value(), right.value())
    left.value(value)
    return value


def number_lshift(left, right):
    value = bit_lshift(left.value(), right.value())
    left.value(value)
    return value


def number_rshift(left, right):
    value = bit_rshift(left.value(), right.value())
    left.value(value)
    return value


def number_multiply(left, right):
    value = left.value() * right.value()
    left.value(value)
    return value


def number_divide(left, right):
    value = left.value() / right.value()
    left.value(value)
    return value


def number_floordiv(left, right):
    value = left.value() // right.value()
    left.value(value)
    return value


def number_mod(left, right):
    value = left.value() % right.value()
    left.value(value)
    return value


def number_pow(left, right):
    value = left.value() ** right.value()
    left.value(value)
    return value


def string_multiply(left, right):
    value = left.value() + right.value()
    left.value(value)
    return value


def string_setitem(left, right):
    value = left.value() + right.value()
    left.value(value)
    return value

def list_pop(left, right):
    pass

def list_insert(left, right):
    pass

def list_reverse(left, right):
    pass

def list_multiply(left, right):
    pass

def set_intersection_update(left, right):
    pass

def set_difference_update(left, right):
    pass

def set_symmetric_difference(left, right):
    pass

def queue_put(left, right):
    pass

def multiset_intersection_update(left, right):
    pass


