from typing import TypeAlias
__typ0 : TypeAlias = "int"
from datetime import datetime, timedelta
from typing import Optional


class RestartStatistics:

    def __tmp3(__tmp1, failure_count: __typ0, last_failure_time) :
        __tmp1.__failures_items = []
        for i in range(0, failure_count):
            __tmp1.__failures_items.append(last_failure_time or datetime.now())

    @property
    def failure_count(__tmp1) -> __typ0:
        return len(__tmp1.__failures_items)

    def __tmp2(__tmp1) -> None:
        __tmp1.__failures_items.append(datetime.now())

    def __tmp4(__tmp1) -> None:
        __tmp1.__failures_items.clear()

    def number_of_failures(__tmp1, __tmp0: <FILL>) -> __typ0:
        res = 0

        if __tmp0 is not None:
            for failure_item in __tmp1.__failures_items:
                if datetime.now() - failure_item < __tmp0:
                    res += 1
        else:
            res = len(__tmp1.__failures_items)

        return res
