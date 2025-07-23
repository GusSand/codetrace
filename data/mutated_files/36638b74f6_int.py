from typing import TypeAlias
__typ0 : TypeAlias = "timedelta"
from datetime import datetime, timedelta
from typing import Optional


class RestartStatistics:

    def __tmp3(__tmp1, __tmp4: <FILL>, __tmp2) :
        __tmp1.__failures_items = []
        for i in range(0, __tmp4):
            __tmp1.__failures_items.append(__tmp2 or datetime.now())

    @property
    def __tmp4(__tmp1) -> int:
        return len(__tmp1.__failures_items)

    def fail(__tmp1) -> None:
        __tmp1.__failures_items.append(datetime.now())

    def __tmp5(__tmp1) -> None:
        __tmp1.__failures_items.clear()

    def number_of_failures(__tmp1, __tmp0) :
        res = 0

        if __tmp0 is not None:
            for failure_item in __tmp1.__failures_items:
                if datetime.now() - failure_item < __tmp0:
                    res += 1
        else:
            res = len(__tmp1.__failures_items)

        return res
