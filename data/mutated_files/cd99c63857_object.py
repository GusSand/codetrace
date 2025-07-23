from typing import TypeAlias
__typ1 : TypeAlias = "str"
import gc
import time

from typing import Mapping, Optional


class __typ0:
    """Context manager to log GC stats and overall time."""

    def __tmp2(__tmp0) :
        __tmp0.gc_start_time = None  # type: Optional[float]
        __tmp0.gc_time = 0.0
        __tmp0.gc_calls = 0
        __tmp0.gc_collected = 0
        __tmp0.gc_uncollectable = 0
        gc.callbacks.append(__tmp0.gc_callback)
        __tmp0.start_time = time.time()
        return __tmp0

    def gc_callback(__tmp0, __tmp4, __tmp5) :
        if __tmp4 == 'start':
            assert __tmp0.gc_start_time is None, "Start phase out of sequence"
            __tmp0.gc_start_time = time.time()
        elif __tmp4 == 'stop':
            assert __tmp0.gc_start_time is not None, "Stop phase out of sequence"
            __tmp0.gc_calls += 1
            __tmp0.gc_time += time.time() - __tmp0.gc_start_time
            __tmp0.gc_start_time = None
            __tmp0.gc_collected += __tmp5['collected']
            __tmp0.gc_uncollectable += __tmp5['uncollectable']
        else:
            assert False, "Unrecognized gc phase (%r)" % (__tmp4,)

    def __tmp3(__tmp0, *args: <FILL>) :
        while __tmp0.gc_callback in gc.callbacks:
            gc.callbacks.remove(__tmp0.gc_callback)

    def __tmp1(__tmp0) :
        end_time = time.time()
        result = {}
        result['gc_time'] = __tmp0.gc_time
        result['gc_calls'] = __tmp0.gc_calls
        result['gc_collected'] = __tmp0.gc_collected
        result['gc_uncollectable'] = __tmp0.gc_uncollectable
        result['build_time'] = end_time - __tmp0.start_time
        return result
