import uuid
from ..client import default_client, transaction, get_prefix
from .operator import *
import operator

class Base(Object):
    def __init__(self, initial=None, key=None, serializer=None, client=None, **kwargs):
        """
        Base type that all others inherit. Contains the basic comparison
        operators as well as the dispatch for proxying to methods on the
        Redis client.
        """

        try:
            self.client = client(kwargs)
        except Exception:
            self.client = None

        self.key = key if key is not None else uuid.uuid4()

        if serializer is not None:
            if not hasattr(serializer, "loads") or not hasattr(serializer, "dumps"):
                raise ValueError("serializer does not have loads or dumps method.")

            self.loads = serializer.loads
            self.dumps = serializer.dumps
        else:
            from msgpack import dumps, loads
            self.loads = loads
            self.dumps = dumps

        self.key = key or str(uuid.uuid4())

        self.prefix = get_prefix
        self.prefixer = '{}/{{}}'.format(self.prefix).format

        if initial is not None:
            if key is None:
                self.value = initial
            else:
                # Ensure previous value removed if key and initial
                # value provided.
                with transaction():
                    self.delete()
                    self.value = initial

    __eq__ = op_left(operator.eq)
    __lt__ = op_left(operator.lt)
    __le__ = op_left(operator.le)
    __gt__ = op_left(operator.gt)
    __ge__ = op_left(operator.ge)

    def __repr__(self):
        bits = (self.__class__.__name__, repr(self.value), self.key)
        return "%s(%s, '%s')" % bits

    def __getattr__(self, name):
        return self._dispatch(name)

    def _dispatch(self, name):
        try:
            func = getattr(self.client or default_client(), name)
        except AttributeError:
            raise
        return lambda *a, **k: func(self.key, *a, **k)

    def rename(self, new_redis_key):
        """Moves the value to a new key. 
        
        If the key is already in use, it returns False

        Args:
            new_redis_key (string): The new key for this object.

        Returns:
            bool: True, if rename process was a success, otherwise False
        """
        if not self.exists(new_redis_key):
            self.rename(self.key, new_redis_key)
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

