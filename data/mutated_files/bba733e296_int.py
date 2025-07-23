class WorkSchedule:
    def __init__(__tmp0, __tmp1: int, __tmp3, __tmp8: int, maxWorkingWeekend, minConsecutiveWorkingDays: <FILL>, __tmp9: int):
        __tmp0._minTotalMinutes = __tmp1
        __tmp0._maxTotalMinutes = __tmp3
        __tmp0._maxShiftNumber = __tmp8
        __tmp0._maxWorkingWeekend = maxWorkingWeekend
        __tmp0._minConsecutiveWorkingDays = minConsecutiveWorkingDays
        __tmp0._maxConsecutiveWorkingDays = __tmp9

    @property
    def MinTotalMinutes(__tmp0) -> int:
        return __tmp0._minTotalMinutes

    @property
    def __tmp6(__tmp0) -> int:
        return __tmp0._maxTotalMinutes

    @property
    def __tmp5(__tmp0) :
        return __tmp0._maxShiftNumber

    @property
    def __tmp7(__tmp0) -> int:
        return __tmp0._maxWorkingWeekend

    @property
    def __tmp2(__tmp0) :
        return __tmp0._minConsecutiveWorkingDays

    @property
    def __tmp4(__tmp0) :
        return __tmp0._maxConsecutiveWorkingDays