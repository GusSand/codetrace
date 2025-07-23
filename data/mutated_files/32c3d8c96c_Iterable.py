from typing import TypeAlias
__typ1 : TypeAlias = "Any"
from typing import Iterable, Any
from inspect import isgenerator
from itertools import islice

class __typ0(object):
    """Wraps a generator and lazily caches returned objects.
    The cache can be iterated over multiple times, unlike a standard generator.
    """
    def __tmp1(__tmp0, gen: <FILL>) :
        __tmp0.generator: Iterable[__typ1] = gen
        __tmp0.cache: List[__typ1] = []

    def __iter__(__tmp0) -> Iterable:
        __tmp0._position = 0
        return __tmp0
    
    def __tmp2(__tmp0) :
        if len(__tmp0.cache) > __tmp0._position:
            item = __tmp0.cache[__tmp0._position]
        else:
            item = next(__tmp0.generator)
            __tmp0.cache.append(item)
        __tmp0._position += 1 
        return item
        
            
