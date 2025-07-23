from typing import TypeAlias
__typ1 : TypeAlias = "object"
import gc
import time

from typing import Mapping, Optional


class __typ0:
    """Context manager to log GC stats and overall time."""

    def __enter__(__tmp0) -> 'GcLogger':
        __tmp0.gc_start_time = None  # type: Optional[float]
        __tmp0.gc_time = 0.0
        __tmp0.gc_calls = 0
        __tmp0.gc_collected = 0
        __tmp0.gc_uncollectable = 0
        gc.callbacks.append(__tmp0.gc_callback)
        __tmp0.start_time = time.time()
        return __tmp0

    def gc_callback(__tmp0, phase: <FILL>, info) :
        if phase == 'start':
            assert __tmp0.gc_start_time is None, "Start phase out of sequence"
            __tmp0.gc_start_time = time.time()
        elif phase == 'stop':
            assert __tmp0.gc_start_time is not None, "Stop phase out of sequence"
            __tmp0.gc_calls += 1
            __tmp0.gc_time += time.time() - __tmp0.gc_start_time
            __tmp0.gc_start_time = None
            __tmp0.gc_collected += info['collected']
            __tmp0.gc_uncollectable += info['uncollectable']
        else:
            assert False, "Unrecognized gc phase (%r)" % (phase,)

    def __exit__(__tmp0, *args: __typ1) -> None:
        while __tmp0.gc_callback in gc.callbacks:
            gc.callbacks.remove(__tmp0.gc_callback)

    def get_stats(__tmp0) -> Mapping[str, float]:
        end_time = time.time()
        result = {}
        result['gc_time'] = __tmp0.gc_time
        result['gc_calls'] = __tmp0.gc_calls
        result['gc_collected'] = __tmp0.gc_collected
        result['gc_uncollectable'] = __tmp0.gc_uncollectable
        result['build_time'] = end_time - __tmp0.start_time
        return result
