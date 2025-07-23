class WorkSchedule:
    def __init__(__tmp0, __tmp1, maxTotalMinutes: <FILL>, __tmp9: int, __tmp6, __tmp2, __tmp11):
        __tmp0._minTotalMinutes = __tmp1
        __tmp0._maxTotalMinutes = maxTotalMinutes
        __tmp0._maxShiftNumber = __tmp9
        __tmp0._maxWorkingWeekend = __tmp6
        __tmp0._minConsecutiveWorkingDays = __tmp2
        __tmp0._maxConsecutiveWorkingDays = __tmp11

    @property
    def __tmp10(__tmp0) -> int:
        return __tmp0._minTotalMinutes

    @property
    def __tmp7(__tmp0) :
        return __tmp0._maxTotalMinutes

    @property
    def __tmp5(__tmp0) -> int:
        return __tmp0._maxShiftNumber

    @property
    def __tmp8(__tmp0) -> int:
        return __tmp0._maxWorkingWeekend

    @property
    def __tmp3(__tmp0) -> int:
        return __tmp0._minConsecutiveWorkingDays

    @property
    def __tmp4(__tmp0) -> int:
        return __tmp0._maxConsecutiveWorkingDays