from ..cache import PubSubCache
from .dict import Dict


NoneKey = object()


class PubSubCacheDict(PubSubCache):
    def _update_key(self, key):
        with self.mutex:
            if key in self.cache:
                self.cache[key] = self.store[key]

    def _delete_key(self, key):
        with self.mutex:
            if key in self.cache:
                del self.cache[key]

    def __contains__(self, key):
        # Check the cache first. If it is there we can return quickly.
        # if you want just local keys chack cache
        if str(key) in self.cache:
            return True

        # Not in the cache. Might be in the underlying store.
        return key in self.store

    def __getitem__(self, key):
        # First we try the cache. If successful we just return the value. If
        # not we catch KeyError and ignore it since that just means the key
        # was not in the cache.
        skey = str(key)
        with self.mutex:
            try:
                cache = self.cache[skey]
            except KeyError:
                pass
            else:
                if cache is NoneKey:
                    raise KeyError
                return cache

            # It wasn't in the cache. Look it up in the store, add the entry to
            # the cache, and return the value.
            try:
                value = self.store[key]
                self.cache[skey] = value
                return value
            except KeyError:
                self.cache[skey] = NoneKey
                raise KeyError

    def __setitem__(self, key, value):
        # Add the key/value pair to the cache and store.
        with self.mutex:
            self.cache[str(key)] = value
            self.store[key] = value

    def __delitem__(self, key):
        # Write-through behavior cache and store should be consistent. Delete
        # it from the store.
        del self.store[key]
        try:
            # Ok, delete from the store was successful. It might also be in
            # the cache, try and delete it. If not we catch the KeyError and
            # ignore it.
            del self.cache[str(key)]
        except KeyError:
            pass

    def close(self):
        self.store.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()
