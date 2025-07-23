from typing import TypeAlias
__typ0 : TypeAlias = "WorkSchedule"
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "int"
from typing import List, Dict
from action import Action
from workSchedule import WorkSchedule

class __typ3:
    def __tmp10(__tmp1, __tmp15: __typ1, workSchedule: __typ0, __tmp2: List[__typ1]):
        __tmp1._index = __tmp15
        __tmp1._shifts = {}
        __tmp1._workSchedule = workSchedule
        __tmp1._totalWorkedMinutes = 0
        __tmp1._shiftCount = 0
        __tmp1._workingWeekendCount = 0
        __tmp1._consecutiveWorkingDays = 0
        __tmp1._dayOffs = {}

        for dayOff in __tmp2:
            __tmp1._dayOffs[dayOff] = True

    def __tmp9(__tmp1, action):
        if action.DayIndex in __tmp1._shifts:
            del __tmp1._shifts[action.DayIndex]

    def __tmp4(__tmp1, action: Action):
        shiftLength = 8 * 60

        if not action.DayIndex in __tmp1._shifts:
            __tmp1._shifts[action.DayIndex] = action.ShiftIndex
            __tmp1._tryAddWeekend(action)
            __tmp1._tryIncrementConsecutiveWorkingDays(action)
            __tmp1._totalWorkedMinutes += shiftLength
            __tmp1._shiftCount += 1

    def __tmp14(__tmp1):
        __tmp1._shifts = {}
        __tmp1._totalWorkedMinutes = 0
        __tmp1._shiftCount = 0
        __tmp1._workingWeekendCount = 0
        __tmp1._consecutiveWorkingDays = 0

    def __tmp8(__tmp1, __tmp5: __typ1) -> __typ2:
        return __tmp5 in __tmp1._shifts

    def __tmp12(__tmp1, __tmp5: __typ1) -> __typ2:
        return __tmp5 in __tmp1._dayOffs

    def _tryAddWeekend(__tmp1, action: Action):
        isSaturday = action.DayIndex % 5 == 0
        isSunday = action.DayIndex % 6 == 0

        if isSaturday and not action.DayIndex + 1 in __tmp1._shifts:
            __tmp1._workingWeekendCount += 1
            return

        if isSunday and not action.DayIndex - 1 in __tmp1._shifts:
            __tmp1._workingWeekendCount += 1
            return

    def __tmp13(__tmp1, action: <FILL>):
        isSaturday = action.DayIndex % 5 == 0
        isSunday = action.DayIndex % 6 == 0

        if isSaturday and not action.DayIndex + 1 in __tmp1._shifts:
            __tmp1._workingWeekendCount -= 1
            return

        if isSunday and not action.DayIndex - 1 in __tmp1._shifts:
            __tmp1._workingWeekendCount -= 1
            return

    def _tryIncrementConsecutiveWorkingDays(__tmp1, action: Action):
        __tmp1._consecutiveWorkingDays = 1
        previousDayIndex = action.DayIndex - 1
        nextDayIndex = action.DayIndex + 1
        numberOfDaysToCheck = __tmp1._workSchedule.MaxConsecutiveWorkingDays - 2

        for i in range(previousDayIndex, previousDayIndex - numberOfDaysToCheck):
            if i in __tmp1._shifts:
                __tmp1._consecutiveWorkingDays += 1
            else:
                break
        
        for i in range(nextDayIndex, nextDayIndex + numberOfDaysToCheck):
            if i in __tmp1._shifts:
                __tmp1._consecutiveWorkingDays += 1
            else:
                break

    @property
    def __tmp6(__tmp1) -> __typ1:
        return __tmp1._totalWorkedMinutes

    @property
    def __typ0(__tmp1) -> __typ0:
        return __tmp1._workSchedule

    @property
    def __tmp3(__tmp1) -> __typ1:
        return __tmp1._shiftCount

    @property
    def __tmp7(__tmp1) -> __typ1:
        return __tmp1._workingWeekendCount

    @property
    def __tmp11(__tmp1) -> __typ1:
        return __tmp1._consecutiveWorkingDays

    @property
    def __tmp0(__tmp1) :
        return __tmp1._shifts