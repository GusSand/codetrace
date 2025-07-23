from typing import TypeAlias
__typ1 : TypeAlias = "bool"
from typing import Callable


class __typ0:
    def __init__(__tmp1, total, __tmp2, run_both_on_every: __typ1, __tmp4):
        __tmp1._total = total
        __tmp1._every_nth = __tmp2
        __tmp1._run_both_on_every = run_both_on_every
        __tmp1._run_on_start = __tmp4

    def __tmp2(__tmp1, every_nth_action: Callable[[int], None], __tmp0: Callable[[int, __typ1], None]):
        def must_run_nth(__tmp3: <FILL>) -> __typ1:
            if __tmp3 == 0 and __tmp1._run_on_start:
                return True
            if __tmp3 == 0:
                return False
            return __tmp3 % __tmp1._every_nth == 0

        for i in range(__tmp1._total+1):
            must = must_run_nth(i)
            if must:
                every_nth_action(i)
            if must and not __tmp1._run_both_on_every:
                continue
            __tmp0(i, must)