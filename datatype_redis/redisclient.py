from redis import Redis, StrictRedis


class RedisClient(StrictRedis):
    """
    A Redis client wrapper
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("decode_responses", True)
        super(RedisClient, self).__init__(*args, **kwargs)

