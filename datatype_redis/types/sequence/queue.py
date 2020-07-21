from .list import List
import time
from ..set.set import Set

class Queue(List):
    """
    Redis list <-> Python list <-> Python's Queue.
    """

    maxsize = 0

    def __init__(self, maxsize=None, **kwargs):
        if maxsize is not None:
            self.maxsize = maxsize
        super(Queue, self).__init__(**kwargs)

    @property
    def queue(self):
        return self

    def qsize(self):
        return len(self)

    def empty(self):
        return self.qsize() == 0

    def full(self):
        return self.maxsize > 0 and self.qsize() >= self.maxsize

    def put(self, item, block=True, timeout=None):
        if self.maxsize == 0:
            self.append(item)
        else:
            if not block:
                timeout = 0
            start = time.time()
            while True:
                if self.queue_put(item, self.maxsize):
                    break
                if timeout is not None and time.time() - start >= timeout:
                    raise queue.Full
                time.sleep(.1)

    def put_nowait(self, item):
        self.put(item, block=False)

    def get(self, block=True, timeout=None):
        if block:
            item = self.blpop(timeout=timeout)
            if item is not None:
                item = item[1]
        else:
            item = self.pop()
        if item is None:
            raise queue.Empty
        return item

    def get_nowait(self):
        return self.get(block=False)

    def join(self):
        while not self.empty():
            time.sleep(.1)

class LifoQueue(Queue):
    """
    Redis list <-> Python list <-> Python's Queue.LifoQueue.
    """

    def append(self, item):
        self.lpush(item)


class SetQueue(Queue):
    """
    Redis list + Redis set <-> Queue with only unique items.
    """

    def __init__(self, *args, **kwargs):
        super(SetQueue, self).__init__(*args, **kwargs)
        self.set = Set(key="%s-set" % self.key)

    def get(self, *args, **kwargs):
        item = super(SetQueue, self).get(*args, **kwargs)
        self.set.remove(item)
        return item

    def put(self, item, *args, **kwargs):
        if self.set.sadd(item) > 0:
            super(SetQueue, self).put(item, *args, **kwargs)

    def delete(self):
        self._dispatch("delete")
        self.set.delete()


class LifoSetQueue(LifoQueue, SetQueue):
    """
    Redis list + Redis set <-> LifoQueue with only unique items.
    """
    pass