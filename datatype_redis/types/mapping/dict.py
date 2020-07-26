from ..base import Base
from ...client import transaction, default_client
import logging
import inspect

LOGGER = logging.getLogger(__name__)


class Dict(Base):
    """
    Redis hash <-> Python dict
    """

    def __init__(self,
                 initial=None,
                 key=None,
                 serializer=None,
                 client=None,
                 namespace=None,
                 prefix_format="{}/{}/{{}}",
                 **kwargs):

        super().__init__(key=key,
                         serializer=serializer,
                         client=client,
                         namespace=namespace)

        self.prefixer = prefix_format.format(self.prefix, self.key).format

        if initial is not None:
            if key is None:
                self.value = initial
            else:
                # Ensure previous value removed if key and initial
                # value provided.
                with transaction():
                    for k in self.keys():
                        del self[k]
                    self.value = initial

    @property
    def value(self):
        d = {}
        d.update(dict(self.items()))
        return d

    @value.setter
    def value(self, value=None):
        if value is not None:
            self.update(value)

    def __len__(self):
        return sum(1 for k in self._keys())

    def __contains__(self, key):
        return self.client.exists(self.prefixer(key))

    def __iter__(self):
        return self.keys()

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key):
        if self.client.delete(self.prefixer(key)) == 0:
            raise KeyError(key)

    def _keys(self):
        match = self.prefixer("*")
        return self.client.scan_iter(match=match)

    def keys(self):
        prefix = self.prefixer("")
        for k in self._keys():
            val = k.decode("utf-8").replace(prefix, "", 1)
            LOGGER.warning("key: {} val: {}".format(k, val))
            yield val

    def values(self):
        return (self[k] for k in self.keys())

    def update(self, value):
        if not isinstance(value, (dict, Dict)):
            try:
                value = dict(value)
            except TypeError:
                raise

        for key, val in value.items():
            with transaction():
                self[key] = val

    def items(self):
        return ((k, self[k]) for k in self.keys())

    def setdefault(self, key, value=None):
        if self.client.setnx(self.prefixer(key), self.dumps(value)) == 1:
            return value
        else:
            return self.get(key)

    def get(self, key, default=None):
        try:
            return self.loads(self.client.get(self.prefixer(key)), raw=False)
        except (KeyError, TypeError) as e:
            LOGGER.error(e)
            return default

    def set(self, key, value):
        self.client.set(self.prefixer(key), self.dumps(value))

    def has_key(self, key):
        return key in self.keys()

    def copy(self):
        return self.__class__(self.value)

    def clear(self):
        for k in self.keys():
            del self[k]

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self.values())

    def iteritems(self):
        return iter(self.items())

    def __eq__(self, other):
        if isinstance(other, (dict)):
            return other == self.value

        if isinstance(other, (Dict)):
            return other.value == self.value

        return False

    @classmethod
    def fromkeys(cls, *args):
        if len(args) == 1:
            args += ("",)
        return cls({}.fromkeys(*args))


class DefaultDict(Dict):
    """
    Redis hash <-> Python dict <-> Python's collections.DefaultDict.
    """

    def __init__(self, default_factory, *args, **kwargs):
        self.default_factory = default_factory
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        return self.setdefault(key, self.default_factory())
