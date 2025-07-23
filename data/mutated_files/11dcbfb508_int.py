from typing import TypeAlias
__typ0 : TypeAlias = "bool"
from typing import Callable


class ForWithProgress:
    def __init__(__tmp1, total, every_nth: <FILL>, run_both_on_every: __typ0, run_on_start: __typ0):
        __tmp1._total = total
        __tmp1._every_nth = every_nth
        __tmp1._run_both_on_every = run_both_on_every
        __tmp1._run_on_start = run_on_start

    def every_nth(__tmp1, every_nth_action, every_action: Callable[[int, __typ0], None]):
        def must_run_nth(__tmp0: int) :
            if __tmp0 == 0 and __tmp1._run_on_start:
                return True
            if __tmp0 == 0:
                return False
            return __tmp0 % __tmp1._every_nth == 0

        for i in range(__tmp1._total+1):
            must = must_run_nth(i)
            if must:
                every_nth_action(i)
            if must and not __tmp1._run_both_on_every:
                continue
            every_action(i, must)