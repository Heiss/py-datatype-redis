import uuid
from ..client import default_client, transaction, get_prefix
from .operator import op_left, op_right, inplace
import operator
from functools import wraps
from redis.exceptions import ResponseError


def ValueDecorator(fn):
    @wraps(fn)
    def wrapper(self, *args):
        try:
            arguments = list(args)
            arguments[0] = arguments[0].value
            args = tuple(arguments)
        except AttributeError:
            pass

        return fn(self, *args)

    return wrapper


class Base(object):
    def __init__(
        self,
        initial=None,
        key=None,
        serializer=None,
        client=None,
        namespace=None,
        prefix_format = "{}/{{}}",
        **kwargs
    ):
        """Base type that all others inherit. Contains the basic comparison
        operators as well as the dispatch for proxying to methods on the
        Redis client.

        Args:
            initial (object, optional): Set the value to this initial value. Defaults to None.
            key (string, optional): Set the key of this object to this value. Defaults to None.
            serializer (object, optional): Use this serializer. Needs `loads` and `dumps` method. Defaults to None.
            client (object, optional): Use this (redis) client. Defaults to None.
            namespace (string, optional): Use this namespace. Overwrites prefix from configure. Defaults to None.

        Raises:
            ValueError: Raises, when the serializer is not valid.
        """

        try:
            self.client = client(kwargs)
        except TypeError:
            self.client = client
        except Exception:
            self.client = None

        if serializer is not None:
            if not hasattr(serializer, "loads") or not hasattr(serializer, "dumps"):
                raise ValueError(
                    "serializer does not have loads or dumps method.")

            self.loads = serializer.loads
            self.dumps = serializer.dumps
        else:
            from msgpack import dumps, loads

            self.loads = loads
            self.dumps = dumps

        self.key = key or str(uuid.uuid4())

        self._prefix = namespace or get_prefix
        self.prefixer =  prefix_format.format(self.prefix).format

        if initial is not None:
            if key is None:
                self.value = initial
            else:
                # Ensure previous value removed if key and initial
                # value provided.
                with transaction():
                    self.client.delete(self.prefixer(self.key))
                    self.value = initial

    __eq__ = op_left(operator.eq)
    __lt__ = op_left(operator.lt)
    __le__ = op_left(operator.le)
    __gt__ = op_left(operator.gt)
    __ge__ = op_left(operator.ge)

    @property
    def prefix(self):
        if isinstance(self._prefix, str):
            return self._prefix
        return self._prefix()

    @property
    def value(self):
        raise NotImplementedError()

    @value.setter
    def value(self, value):
        raise NotImplementedError()

    @property
    def client(self):
        return self._client or default_client()

    @client.setter
    def client(self, value):
        self._client = value

    def __repr__(self):
        bits = (self.__class__.__name__, repr(self.value), self.key)
        return "%s(%s, '%s')" % bits


    def clear(self):
        self.client.delete(self.prefixer(self.key))

    def rename(self, new_redis_key):
        """Moves the value to a new key. 

        If the key is already in use, it returns False

        Args:
            new_redis_key (string): The new key for this object.

        Returns:
            bool: True, if rename process was a success, otherwise False
        """
        if not self.client.exists(self.prefixer(self.key), new_redis_key):
            self.client.rename(self.prefixer(self.key), new_redis_key)
            self.key = new_redis_key
            return True

        return False

    def get_redis_key(self):
        """Returns the redis key without prefix.

        This key is not equal to a dict key and cannot be used to interact with redis!

        Returns:
            string: The shortened redis key
        """
        return self.key

    def get_redis_key_full(self):
        """Returns the full redis key with prefix.

        This key can be used to interact with redis.

        Returns:
            string: The full redis key
        """
        return self.prefixer(self.key)
