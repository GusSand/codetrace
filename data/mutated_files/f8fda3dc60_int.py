class __typ0:
    def __tmp3(__tmp0, __tmp1, maxTotalMinutes, maxShiftNumber, maxWorkingWeekend, __tmp2, __tmp4: <FILL>):
        __tmp0._minTotalMinutes = __tmp1
        __tmp0._maxTotalMinutes = maxTotalMinutes
        __tmp0._maxShiftNumber = maxShiftNumber
        __tmp0._maxWorkingWeekend = maxWorkingWeekend
        __tmp0._minConsecutiveWorkingDays = __tmp2
        __tmp0._maxConsecutiveWorkingDays = __tmp4

    @property
    def MinTotalMinutes(__tmp0) :
        return __tmp0._minTotalMinutes

    @property
    def MaxTotalMinutes(__tmp0) :
        return __tmp0._maxTotalMinutes

    @property
    def MaxShiftNumber(__tmp0) :
        return __tmp0._maxShiftNumber

    @property
    def MaxWorkingWeekend(__tmp0) :
        return __tmp0._maxWorkingWeekend

    @property
    def MinConsecutiveWorkingDays(__tmp0) :
        return __tmp0._minConsecutiveWorkingDays

    @property
    def MaxConsecutiveWorkingDays(__tmp0) :
        return __tmp0._maxConsecutiveWorkingDays