
####################################################################
#                                                                  #
#  The following functions are all used for creating methods that  #
#  get assigned to all the magic operator names for each type,     #
#  and make much more sense further down where they're applied.    #
#                                                                  #
####################################################################

def value_left(self, other):
    """
    Returns the value of the other type instance to use in an
    operator method, namely when the method's instance is on the
    left side of the expression.
    """
    return other.value if isinstance(other, self.__class__) else other


def value_right(self, other):
    """
    Returns the value of the type instance calling an to use in an
    operator method, namely when the method's instance is on the
    right side of the expression.
    """
    return self if isinstance(other, self.__class__) else self.value


def op_left(op):
    """
    Returns a type instance method for the given operator, applied
    when the instance appears on the left side of the expression.
    """
    def method(self, other):
        return op(self.value, value_left(self, other))
    return method


def op_right(op):
    """
    Returns a type instance method for the given operator, applied
    when the instance appears on the right side of the expression.
    """
    def method(self, other):
        return op(value_left(self, other), value_right(self, other))
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
