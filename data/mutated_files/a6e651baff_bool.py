from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import Callable


class __typ1:
    def __tmp4(__tmp1, total, every_nth, run_both_on_every: <FILL>, __tmp6):
        __tmp1._total = total
        __tmp1._every_nth = every_nth
        __tmp1._run_both_on_every = run_both_on_every
        __tmp1._run_on_start = __tmp6

    def every_nth(__tmp1, __tmp5, __tmp0: Callable[[__typ0, bool], None]):
        def __tmp2(__tmp3) -> bool:
            if __tmp3 == 0 and __tmp1._run_on_start:
                return True
            if __tmp3 == 0:
                return False
            return __tmp3 % __tmp1._every_nth == 0

        for i in range(__tmp1._total+1):
            must = __tmp2(i)
            if must:
                __tmp5(i)
            if must and not __tmp1._run_both_on_every:
                continue
            __tmp0(i, must)