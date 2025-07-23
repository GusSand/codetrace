from typing import TypeAlias
__typ1 : TypeAlias = "WorkSchedule"
__typ0 : TypeAlias = "Action"
from typing import List, Dict
from action import Action
from workSchedule import WorkSchedule

class __typ2:
    def __tmp8(__tmp0, __tmp11: <FILL>, workSchedule, __tmp4):
        __tmp0._index = __tmp11
        __tmp0._shifts = {}
        __tmp0._workSchedule = workSchedule
        __tmp0._totalWorkedMinutes = 0
        __tmp0._shiftCount = 0
        __tmp0._workingWeekendCount = 0
        __tmp0._consecutiveWorkingDays = 0
        __tmp0._dayOffs = {}

        for dayOff in __tmp4:
            __tmp0._dayOffs[dayOff] = True

    def __tmp7(__tmp0, action):
        if action.DayIndex in __tmp0._shifts:
            del __tmp0._shifts[action.DayIndex]

    def __tmp2(__tmp0, action):
        shiftLength = 8 * 60

        if not action.DayIndex in __tmp0._shifts:
            __tmp0._shifts[action.DayIndex] = action.ShiftIndex
            __tmp0._tryAddWeekend(action)
            __tmp0._tryIncrementConsecutiveWorkingDays(action)
            __tmp0._totalWorkedMinutes += shiftLength
            __tmp0._shiftCount += 1

    def __tmp10(__tmp0):
        __tmp0._shifts = {}
        __tmp0._totalWorkedMinutes = 0
        __tmp0._shiftCount = 0
        __tmp0._workingWeekendCount = 0
        __tmp0._consecutiveWorkingDays = 0

    def hasAssignmentOnDay(__tmp0, day) :
        return day in __tmp0._shifts

    def __tmp9(__tmp0, day) :
        return day in __tmp0._dayOffs

    def _tryAddWeekend(__tmp0, action):
        isSaturday = action.DayIndex % 5 == 0
        isSunday = action.DayIndex % 6 == 0

        if isSaturday and not action.DayIndex + 1 in __tmp0._shifts:
            __tmp0._workingWeekendCount += 1
            return

        if isSunday and not action.DayIndex - 1 in __tmp0._shifts:
            __tmp0._workingWeekendCount += 1
            return

    def _tryRemoveWeekend(__tmp0, action):
        isSaturday = action.DayIndex % 5 == 0
        isSunday = action.DayIndex % 6 == 0

        if isSaturday and not action.DayIndex + 1 in __tmp0._shifts:
            __tmp0._workingWeekendCount -= 1
            return

        if isSunday and not action.DayIndex - 1 in __tmp0._shifts:
            __tmp0._workingWeekendCount -= 1
            return

    def _tryIncrementConsecutiveWorkingDays(__tmp0, action):
        __tmp0._consecutiveWorkingDays = 1
        previousDayIndex = action.DayIndex - 1
        nextDayIndex = action.DayIndex + 1
        numberOfDaysToCheck = __tmp0._workSchedule.MaxConsecutiveWorkingDays - 2

        for i in range(previousDayIndex, previousDayIndex - numberOfDaysToCheck):
            if i in __tmp0._shifts:
                __tmp0._consecutiveWorkingDays += 1
            else:
                break
        
        for i in range(nextDayIndex, nextDayIndex + numberOfDaysToCheck):
            if i in __tmp0._shifts:
                __tmp0._consecutiveWorkingDays += 1
            else:
                break

    @property
    def __tmp5(__tmp0) :
        return __tmp0._totalWorkedMinutes

    @property
    def __typ1(__tmp0) :
        return __tmp0._workSchedule

    @property
    def __tmp3(__tmp0) :
        return __tmp0._shiftCount

    @property
    def __tmp6(__tmp0) :
        return __tmp0._workingWeekendCount

    @property
    def ConsecutiveWorkingDays(__tmp0) :
        return __tmp0._consecutiveWorkingDays

    @property
    def __tmp1(__tmp0) :
        return __tmp0._shifts