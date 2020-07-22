from .dict import Dict
from ..pubsub import PubSub
from threading import Lock
from pylru import WriteThroughCacheManager

class PubSubDict(Dict, PubSub):
    def __init__(self, *args, **kwargs):
        super(PubSubDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super(PubSubDict, self).__setitem__(key, value)
        self.publish("update", key)

    def __delitem__(self, key):
        super(PubSubDict, self).__delitem__(key)
        self.publish("delete", key)
