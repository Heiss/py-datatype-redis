from redis import Redis


class RedisClient(Redis):
    """
    A Redis client wrapper
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("decode_responses", True)
        super().__init__(*args, **kwargs)

