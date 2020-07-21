from .client import *
from .types.boolean import *
from .types.mapping import *
from .types.numeric import *
from .types.sequence import *
from .types.set import *
from .types.text import *
from .types.semaphore import *
from .types.base import Base

def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value
        
__version__ = '0.1'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    "Base",
    "Bool",
    "Int",
    "Float",
    "String",
    "List",
    "Queue",
    "LifoQueue",
    "SetQueue",
    "LifoSetQueue",
    "Set",
    "Dict",
    "PubSubDict",
    "PubSubCacheDict",
    "DefaultDict",
    "MultiSet",
    "BoundedSemaphore",
    "Semaphore",
    "Lock",
    "RLock",
]