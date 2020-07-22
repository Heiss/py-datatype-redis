from pylru import WriteThroughCacheManager
from threading import Lock
from .pubsub import PubSub


class PubSubCache(WriteThroughCacheManager):
    def __init__(self, store, cache):
        super().__init__()

        if not isinstance(store, PubSub):
            raise ValueError("Store is not a valid pubsub-type.")

        self.store = store

        self.mutex = Lock()
        self.cache = cache

        if hasattr(store, "pubsub"):
            store.subscribe(update=self._update_key, delete=self._delete_key)

    def _update_key(self, key):
        raise NotImplementedError()

    def _delete_key(self, key):
        raise NotImplementedError()


class PubSubCacheAtomic(PubSubCache):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_key(self, key):
        with self.mutex:
            if key == self.get_redis_key_full():
                self.cache.value = self.store.value

    def _delete_key(self, key):
        with self.mutex:
            self.cache.value = None

    @property
    def value(self):
        with self.mutex:
            if self.cache.value is None:
                value = self.store.value
                self.cache.value = value

            return self.cache.value

    @value.setter
    def value(self, value):
        with self.mutex:
            self.store.value = value
            self.cache.value = None
            self.publish("update")

