from redis import Redis, StrictRedis
import threading

_thread = threading.local()
_config = {}

def default_client():
    try:
        _thread.client
    except AttributeError:
        client = _config["client"](**_config["client_config"])
        if not isinstance(client, StrictRedis):
            raise ValueError("Given client is not a StrictRedis-Class.")

        setattr(_thread, "client", client)
    return _thread.client

def configure(**kwargs):
    global _config

    if "client" in kwargs:
        _config["client"] = kwargs["client"]
        del kwargs["client"]
    else:
        _config["client"] = StrictRedis

    _config["client_config"] = kwargs


@contextlib.contextmanager
def transaction():
    """
    Swaps out the current client with a pipeline instance,
    so that each Redis method call inside the context will be
    pipelined. Once the context is exited, we execute the pipeline.
    """
    client = default_client()
    _thread.client = client.pipeline()
    try:
        yield
        _thread.client.execute()
    finally:
        _thread.client = client