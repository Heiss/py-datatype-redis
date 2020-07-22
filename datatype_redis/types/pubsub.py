from .base import Base



class PubSub(Base):
    def __init__(self):
        self.subscriber = None
        self.pubsub = self.client.pubsub()

        try:
            self.value.fset = super().publish_wrap(super().value.fset)
        except NameError:
            pass

    @staticmethod
    def publish_wrap(fn):
        def wrapper(*args, **kwargs):
            self = args[0]
            fn(*args, **kwargs)
            self.publish("update", **kwargs)

        return wrapper

    def subscribe(self, **callbacks):
        """Register callbacks to deal with update and delete events
        """
        self.callback = callbacks

        if self.subscriber is None:
            ps = self.pubsub
            handelers = {
                self.prefixer(action): self._handel_factory(callback)
                for action, callback in callbacks.items()
            }
            ps.subscribe(**handelers)
            self.subscriber = ps.run_in_thread(sleep_time=0.01, daemon=True)

    def _handel_factory(self, callback):
        def handeler(mesg):
            callback(mesg["data"])

        return handeler

    def publish(self, action, key=None):
        if key is None:
            key = self.get_redis_key_full()
        self.publish(self.prefixer(action), str(key))

    def close(self):
        if hasattr(self, "pubsub"):
            self.pubsub.close()
            self.subscriber.stop()
            self.subscriber.join()

    def __del__(self):
        self.publish("delete", self.get_redis_key_full())
        self.close()
