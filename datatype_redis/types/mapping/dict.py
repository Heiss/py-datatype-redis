from ..base import Base
from ...client import transaction, default_client


class Dict(Base):
    """
    Redis hash <-> Python dict
    """

    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)

        self.prefixer = "{}/{}/{{}}".format(self.prefix, self.key).format

    @property
    def value(self):
        return dict(self.items())

    @value.setter
    def value(self, value=None):
        if not isinstance(value, dict):
            try:
                value = dict(value)
            except TypeError:
                value = None

        if value is not None:
            with transaction() as _:
                self.update(value)

    def __len__(self):
        return sum(1 for k in self._keys())

    def __contains__(self, key):
        return self.exists(self.prefixer(key))

    def __iter__(self):
        return self.keys()

    def __setitem__(self, key, value):
        self.set(self.prefixer(key), self.dumps(value))

    def __getitem__(self, key):
        value = self.loads(self.get(self.prefixer(key)))
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key):
        if self.delete(self.prefixer(key)) == 0:
            raise KeyError(key)

    def _keys(self):
        match = self.prefixer("*")
        return self.scan_iter(match=match)

    def keys(self):
        prefix = self.prefixer("")
        return (k.strip(prefix) for k in self._keys())

    def values(self):
        return (self[k] for k in self.keys())

    def update(self, value):
        with transaction() as _:
            self.clear()
            for key, val in value.items():
                self[key] = val

    def items(self):
        return ((k, self[k]) for k in self.keys())

    def setdefault(self, key, value=None):
        if self.setnx(self.prefixer(key), self.dumps(value)) == 1:
            return value
        else:
            return self.get(self.prefixer(key))

    def get(self, key, default=None):
        value = super().get(self.prefixer(key))
        return value if value is not None else default

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

    def _dispatch(self, name):
        return func(getattr(self, name))

    @classmethod
    def fromkeys(cls, *args):
        if len(args) == 1:
            args += ("",)
        return cls({}.fromkeys(*args))

    def _dispatch(self, name):
        func = getattr(self.client or default_client(), name)
        return lambda *a, **k: func(*a, **k)


class DefaultDict(Dict):
    """
    Redis hash <-> Python dict <-> Python's collections.DefaultDict.
    """

    def __init__(self, default_factory, *args, **kwargs):
        self.default_factory = default_factory
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        return self.setdefault(key, self.default_factory())
