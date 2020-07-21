from ..sequence.queue import Queue
import queue

class BoundedSemaphore(Queue):
    """
    Redis list <-> Python list <-> Queue <-> threading.BoundedSemaphore.
    BoundedSemaphore's ``value`` arg maps to Queue's ``maxsize``.
    BoundedSemaphore's acquire/release methods maps to Queue's put/get
    methods repectively, providing blocking/timeout mechanics.
    """

    maxsize = 1

    def __init__(self, value=None, **kwargs):
        super(BoundedSemaphore, self).__init__(value, **kwargs)

    def acquire(self, block=True, timeout=None):
        try:
            self.put(1, block, timeout)
        except queue.Full:
            return False
        return True

    def release(self):
        try:
            self.get(block=False)
        except queue.Empty:
            raise RuntimeError("Cannot release unacquired lock")

    def __enter__(self):
        self.acquire()

    def __exit__(self, t, v, tb):
        self.release()


class Semaphore(BoundedSemaphore):
    """
    Redis list <-> Python list <-> Queue <-> threading.Semaphore.
    Same implementation as BoundedSemaphore, but without a queue size.
    """

    def release(self):
        try:
            super(Semaphore, self).release()
        except RuntimeError:
            pass


class Lock(BoundedSemaphore):
    """
    Redis list <-> Python list <-> Queue <-> threading.Lock.
    Same implementation as BoundedSemaphore, but with a fixed
    queue size of 1.
    """

    def __init__(self, **kwargs):
        kwargs["value"] = None
        super(Lock, self).__init__(**kwargs)


class RLock(Lock):
    """
    Redis list <-> Python list <-> Queue <-> threading.RLock.
    Same implementation as BoundedSemaphore, but with a fixed
    queue size of 1, and as per re-entrant locks, can be acquired
    multiple times.
    """

    def __init__(self, *args, **kwargs):
        self.acquires = 0
        super(RLock, self).__init__(*args, **kwargs)

    def acquire(self, *args, **kwargs):
        result = True
        if self.acquires == 0:
            result = super(RLock, self).acquire(*args, **kwargs)
        if result:
            self.acquires += 1
        return result

    def release(self):
        if self.acquires > 1:
            self.acquires -= 1
            if self.acquires > 0:
                return
        super(RLock, self).release()