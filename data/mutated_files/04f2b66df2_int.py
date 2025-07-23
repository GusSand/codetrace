class __typ0:
    def __init__(__tmp0, __tmp1: <FILL>, maxTotalMinutes, __tmp3: int, maxWorkingWeekend, minConsecutiveWorkingDays: int, __tmp5):
        __tmp0._minTotalMinutes = __tmp1
        __tmp0._maxTotalMinutes = maxTotalMinutes
        __tmp0._maxShiftNumber = __tmp3
        __tmp0._maxWorkingWeekend = maxWorkingWeekend
        __tmp0._minConsecutiveWorkingDays = minConsecutiveWorkingDays
        __tmp0._maxConsecutiveWorkingDays = __tmp5

    @property
    def __tmp4(__tmp0) :
        return __tmp0._minTotalMinutes

    @property
    def MaxTotalMinutes(__tmp0) :
        return __tmp0._maxTotalMinutes

    @property
    def MaxShiftNumber(__tmp0) :
        return __tmp0._maxShiftNumber

    @property
    def __tmp2(__tmp0) :
        return __tmp0._maxWorkingWeekend

    @property
    def MinConsecutiveWorkingDays(__tmp0) -> int:
        return __tmp0._minConsecutiveWorkingDays

    @property
    def MaxConsecutiveWorkingDays(__tmp0) -> int:
        return __tmp0._maxConsecutiveWorkingDays