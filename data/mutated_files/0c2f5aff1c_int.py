from typing import TypeAlias
__typ1 : TypeAlias = "bool"
from typing import Callable


class __typ0:
    def __tmp5(__tmp2, __tmp1: <FILL>, __tmp8: int, __tmp6, __tmp9: __typ1):
        __tmp2._total = __tmp1
        __tmp2._every_nth = __tmp8
        __tmp2._run_both_on_every = __tmp6
        __tmp2._run_on_start = __tmp9

    def __tmp8(__tmp2, __tmp7: Callable[[int], None], __tmp0):
        def __tmp3(__tmp4) :
            if __tmp4 == 0 and __tmp2._run_on_start:
                return True
            if __tmp4 == 0:
                return False
            return __tmp4 % __tmp2._every_nth == 0

        for i in range(__tmp2._total+1):
            must = __tmp3(i)
            if must:
                __tmp7(i)
            if must and not __tmp2._run_both_on_every:
                continue
            __tmp0(i, must)