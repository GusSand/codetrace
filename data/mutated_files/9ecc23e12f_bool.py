from typing import Callable


class ForWithProgress:
    def __init__(__tmp0, total: int, every_nth, run_both_on_every, run_on_start: <FILL>):
        __tmp0._total = total
        __tmp0._every_nth = every_nth
        __tmp0._run_both_on_every = run_both_on_every
        __tmp0._run_on_start = run_on_start

    def every_nth(__tmp0, every_nth_action, every_action: Callable[[int, bool], None]):
        def must_run_nth(current) :
            if current == 0 and __tmp0._run_on_start:
                return True
            if current == 0:
                return False
            return current % __tmp0._every_nth == 0

        for i in range(__tmp0._total+1):
            must = must_run_nth(i)
            if must:
                every_nth_action(i)
            if must and not __tmp0._run_both_on_every:
                continue
            every_action(i, must)