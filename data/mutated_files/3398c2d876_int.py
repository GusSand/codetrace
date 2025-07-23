class WorkSchedule:
    def __init__(__tmp0, minTotalMinutes, __tmp2: int, maxShiftNumber: <FILL>, __tmp3: int, minConsecutiveWorkingDays: int, maxConsecutiveWorkingDays: int):
        __tmp0._minTotalMinutes = minTotalMinutes
        __tmp0._maxTotalMinutes = __tmp2
        __tmp0._maxShiftNumber = maxShiftNumber
        __tmp0._maxWorkingWeekend = __tmp3
        __tmp0._minConsecutiveWorkingDays = minConsecutiveWorkingDays
        __tmp0._maxConsecutiveWorkingDays = maxConsecutiveWorkingDays

    @property
    def __tmp5(__tmp0) :
        return __tmp0._minTotalMinutes

    @property
    def MaxTotalMinutes(__tmp0) :
        return __tmp0._maxTotalMinutes

    @property
    def MaxShiftNumber(__tmp0) :
        return __tmp0._maxShiftNumber

    @property
    def __tmp4(__tmp0) -> int:
        return __tmp0._maxWorkingWeekend

    @property
    def __tmp1(__tmp0) :
        return __tmp0._minConsecutiveWorkingDays

    @property
    def MaxConsecutiveWorkingDays(__tmp0) :
        return __tmp0._maxConsecutiveWorkingDays